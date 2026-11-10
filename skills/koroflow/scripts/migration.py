"""Offline machine/asset/request inspection. Never logs in or submits media."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def located(base, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Path is missing')
    p = Path(value).expanduser()
    return p.resolve() if p.is_absolute() else (base / p).resolve()


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def inspect(config_path, request_path=None):
    config_path = Path(config_path).resolve()
    config = read(config_path)
    if not isinstance(config, dict):
        raise ValueError('machine configuration must be an object')
    base = config_path.parent
    errors, warnings, checks = [], [], []
    route = config.get('route')
    if route not in {'planning', 'direct-haiyi', 'hypit'}:
        errors.append('route must be planning, direct-haiyi or hypit')
    policy = config.get('policy', {})
    if not isinstance(policy, dict) or not isinstance(policy.get('require_native_audio'), bool):
        errors.append('policy.require_native_audio must be explicitly true or false')
        policy = {}
    try:
        ZoneInfo(config.get('timezone', ''))
    except (ValueError, TypeError, ZoneInfoNotFoundError):
        errors.append('timezone unavailable: use a valid IANA name; install tzdata if needed')
    for key in ('workspace', 'asset_root', 'delivery_root'):
        try:
            p = located(base, config.get(key))
            if not p.is_dir():
                errors.append(f'{key}: directory missing')
            else:
                checks.append(f'{key}: readable directory')
        except ValueError as exc:
            errors.append(f'{key}: {exc}')
    tools = config.get('tools', {})
    if not isinstance(tools, dict):
        raise ValueError('tools must be an object')
    required = [] if route == 'planning' else ['python', 'ffmpeg', 'ffprobe'] if route == 'direct-haiyi' else ['node', 'git', 'ffmpeg', 'ffprobe']
    resolved_tools = {}
    for name in required:
        value = tools.get(name, '')
        exe = None
        if isinstance(value, str) and value:
            if '/' in value or '\\' in value:
                p = located(base, value)
                exe = str(p) if p.is_file() else None
            else:
                exe = shutil.which(value)
        if not exe:
            errors.append(f'tool {name}: not found; configure tools.{name}')
            continue
        resolved_tools[name] = exe
        try:
            result = subprocess.run([exe, '-version' if name in {'ffmpeg', 'ffprobe'} else '--version'], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=15)
            version = (result.stdout or result.stderr).splitlines()
            if result.returncode:
                errors.append(f'tool {name}: version command failed')
            else:
                checks.append(f'{name}: {version[0] if version else "available"}')
                match = re.search(r'(\d+)\.(\d+)', '\n'.join(version))
                if name == 'python' and (not match or tuple(map(int, match.groups())) < (3, 11)):
                    errors.append('python: requires >=3.11')
                if name == 'node' and (not match or tuple(map(int, match.groups())) < (22, 15)):
                    errors.append('node: requires >=22.15')
        except (OSError, subprocess.TimeoutExpired):
            errors.append(f'tool {name}: cannot run version check')
    entry = config.get('executor', '')
    if route != 'planning':
        if not entry or not located(base, entry).is_file():
            errors.append('executor: entry file missing')
        if not config.get('auth_source'):
            errors.append('auth_source: name the new-machine authorization method, never paste a token')
    if route == 'direct-haiyi' and 'python' in resolved_tools:
        result = subprocess.run([resolved_tools['python'], '-c', 'import requests'], capture_output=True, timeout=15)
        if result.returncode:
            errors.append('direct-haiyi Python requires requests; install into the selected interpreter')

    manifest = read(located(base, config.get('asset_manifest')))
    if not isinstance(manifest, dict) or not isinstance(manifest.get('assets'), list):
        raise ValueError('manifest.assets must be an array')
    root = located(base, config.get('asset_root'))
    assets = {}
    for asset in manifest.get('assets', []):
        if not isinstance(asset, dict):
            raise ValueError('asset entry must be an object')
        aid = asset.get('id')
        if not isinstance(aid, str) or not aid or aid in assets:
            errors.append('asset id missing or duplicate')
            continue
        assets[aid] = asset
        p = located(root, asset.get('path'))
        try:
            p.relative_to(root)
        except ValueError:
            errors.append(f'asset {aid}: path must stay within asset_root')
            continue
        expected = asset.get('sha256', '')
        if not re.fullmatch(r'[0-9a-f]{64}', expected):
            errors.append(f'asset {aid}: expected SHA256 missing or invalid')
        if not p.is_file():
            errors.append(f'asset {aid}: file missing')
        elif digest(p) != expected:
            errors.append(f'asset {aid}: SHA256 mismatch')
        else:
            checks.append(f'asset {aid}: SHA256 matches')
        if asset.get('purpose') == 'voice' and asset.get('default_bind') and not asset.get('adoption_evidence'):
            errors.append(f'asset {aid}: default voice binding needs adoption evidence')
    if not assets:
        warnings.append('No assets listed; select approved identities before production')

    if request_path:
        request = read(request_path)
        if not isinstance(request, dict) or not isinstance(request.get('payload'), dict):
            raise ValueError('request.payload must be an object')
        payload = request.get('payload', {})
        parameters = payload.get('parameters', {})
        if not isinstance(parameters, dict):
            raise ValueError('request.payload.parameters must be an object')
        kind = request.get('reference_kind')
        prompt = parameters.get('prompt', '')
        if kind not in {'images-only', 'video', 'text-only'}:
            errors.append('request.reference_kind is required')
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append('actual parameters.prompt missing')
            prompt = ''
        if policy.get('require_native_audio'):
            silent = request.get('explicit_silent_reason')
            if parameters.get('generateAudio') is not True:
                if parameters.get('generateAudio') is False and isinstance(silent, str) and silent.strip():
                    warnings.append('Explicit silent exception recorded; operator must verify user instruction')
                else:
                    errors.append('native audio policy requires actual generateAudio: true')
        if not request.get('sound_plan'):
            errors.append('sound_plan: record character/action/environment sound and BGM choices')
        video_fields = ('video', 'videos', 'referenceVideo', 'referenceVideos')
        if kind in {'images-only', 'text-only'}:
            if any(key in parameters or key in payload for key in video_fields):
                errors.append('non-video request must omit video fields, including empty fields')
            if re.search(r'(?:@?视频\s*\d+|\bvideo\s*\d+\b)', prompt, re.I):
                errors.append('prompt refers to a video label absent from this request')
        if kind == 'images-only':
            if not parameters.get('images') or parameters.get('roleMode') not in {'reference', 'frame'}:
                errors.append('images-only: actual images and explicit reference/frame roleMode required')
            if parameters.get('roleMode') == 'frame' and not request.get('literal_boundary_evidence'):
                errors.append('frame mode needs explicit literal boundary-frame instruction')
        if kind == 'video' and not any(parameters.get(key) for key in video_fields):
            errors.append('video reference kind needs an actual video attachment')
        if request.get('previous_task_status') in {'submitted', 'running', 'unknown'}:
            errors.append('query the original task before preparing another submission')
        bound = {}
        for binding in request.get('bindings', []):
            if not isinstance(binding, dict):
                raise ValueError('binding must be an object')
            aid, field = binding.get('asset_id'), binding.get('field', '')
            if aid not in assets:
                errors.append('binding references an unknown asset id')
                continue
            match = re.fullmatch(r'(images|audios|videos)\[(\d+)\]|(video)', field)
            if not match or field in bound:
                errors.append('binding field invalid or duplicated')
                continue
            try:
                value = parameters['video'] if match.group(3) else parameters[match.group(1)][int(match.group(2))]
            except (KeyError, IndexError, TypeError):
                errors.append(f'binding {field}: actual request field missing')
                continue
            if not value:
                errors.append(f'binding {field}: actual attachment is empty')
            if binding.get('sha256') != assets[aid].get('sha256'):
                errors.append(f'binding {field}: fingerprint differs from manifest')
            bound[field] = binding.get('label')
        for key in ('images', 'audios', 'videos'):
            values = parameters.get(key, [])
            if not isinstance(values, list):
                errors.append(f'{key}: expected an array')
                continue
            for index in range(len(values)):
                if f'{key}[{index}]' not in bound:
                    errors.append(f'{key}[{index}]: missing binding')
        if parameters.get('video') and 'video' not in bound:
            errors.append('video: missing binding')
        # Image/video text labels must agree with actual array positions, not just exist somewhere.
        for label, num in re.findall(r'(图片|视频)\s*(\d+)', prompt):
            expected_field = f'images[{int(num)-1}]' if label == '图片' else 'video' if 'video' in parameters and num == '1' else f'videos[{int(num)-1}]'
            if bound.get(expected_field) != label + num:
                errors.append(f'{label}{num}: label does not match actual binding index')
        checks.append('Request inspected locally; not submitted; uploaded URL contents not authenticated')
    return {'ok': not errors, 'offline': True, 'paid_requests': 0, 'errors': errors, 'warnings': warnings, 'checks': checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, help='Private machine JSON; relative paths resolve beside it')
    parser.add_argument('--request', help='Optional actual-payload handoff JSON; inspected, never submitted')
    args = parser.parse_args()
    try:
        result = inspect(args.config, args.request)
    except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired) as exc:
        result = {'ok': False, 'offline': True, 'paid_requests': 0, 'errors': [f'Invalid local input: {type(exc).__name__}; check config paths and JSON structure']}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
