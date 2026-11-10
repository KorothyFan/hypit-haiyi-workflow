"""Offline migration and actual request inspection, never calls the platform."""
import importlib.util
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
NODE = os.environ.get('KORO_TEST_NODE') or shutil.which('node')
SPEC = importlib.util.spec_from_file_location('migration', ROOT / 'skills/koroflow/scripts/migration.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class MigrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='迁移 中文 path ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for folder in ('workspace', 'assets', 'deliveries'):
            (self.root / folder).mkdir()
        image = self.root / 'assets/角色 image.bin'
        image.write_bytes(b'local fixture, not production media')
        self.fingerprint = m.digest(image)
        self.assets = {'assets': [{'id': 'hero', 'path': image.name, 'purpose': 'identity', 'sha256': self.fingerprint}]}
        self.config = {'route': 'planning', 'workspace': './workspace', 'asset_root': './assets', 'delivery_root': './deliveries', 'asset_manifest': './assets.json', 'timezone': 'UTC', 'policy': {'require_native_audio': True}}
        self.request = {'reference_kind': 'images-only', 'payload': {'parameters': {'prompt': '图片1负责身份，完成动作和结尾。', 'images': ['https://example.invalid/image'], 'roleMode': 'reference', 'generateAudio': True}}, 'bindings': [{'label': '图片1', 'field': 'images[0]', 'asset_id': 'hero', 'sha256': self.fingerprint}], 'sound_plan': '动作环境声及正常反应，无BGM。'}

    def check(self):
        for name, data in [('machine', self.config), ('assets', self.assets), ('request', self.request)]:
            (self.root / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        return m.inspect(self.root / 'machine.json', self.root / 'request.json')

    def test_relative_unicode_paths_and_request_do_not_run_executor(self):
        with patch.object(m.subprocess, 'run', side_effect=AssertionError('planning needs no execution')):
            result = self.check()
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['paid_requests'], 0)
        self.assertTrue(result['offline'])

    def test_native_audio_does_not_depend_on_bgm_or_old_track(self):
        for value in (False, None, 'true', 1):
            self.request['payload']['parameters']['generateAudio'] = value
            self.assertFalse(self.check()['ok'])
        self.request['payload']['parameters']['generateAudio'] = False
        self.request['explicit_silent_reason'] = 'User explicitly requests silent output for this task'
        self.assertTrue(self.check()['ok'])

    def test_pure_images_reject_video_fields_and_phantom_label(self):
        self.request['payload']['parameters']['video'] = ''
        self.assertFalse(self.check()['ok'])
        del self.request['payload']['parameters']['video']
        self.request['payload']['parameters']['prompt'] = '严格参考视频1'
        self.assertFalse(self.check()['ok'])

    def test_binding_hash_index_and_literal_frame_are_checked(self):
        self.request['bindings'][0]['field'] = 'images[1]'
        self.assertFalse(self.check()['ok'])
        self.request['bindings'][0]['field'] = 'images[0]'
        self.request['bindings'][0]['sha256'] = '0' * 64
        self.assertFalse(self.check()['ok'])
        self.request['bindings'][0]['sha256'] = self.fingerprint
        self.request['payload']['parameters']['roleMode'] = 'frame'
        self.assertFalse(self.check()['ok'])

    def test_changed_or_escaping_asset_and_unknown_task_fail(self):
        self.request['previous_task_status'] = 'unknown'
        self.assertFalse(self.check()['ok'])
        del self.request['previous_task_status']
        (self.root / 'assets/角色 image.bin').write_bytes(b'changed')
        self.assertFalse(self.check()['ok'])
        self.assets['assets'][0]['path'] = '../outside.bin'
        self.assertFalse(self.check()['ok'])

    def test_missing_tool_and_cli_structured_failure(self):
        self.config['route'] = 'direct-haiyi'
        self.config['tools'] = {'python': 'intentionally-missing-python-abc'}
        self.assertFalse(self.check()['ok'])
        result = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'scripts/migration.py'), '--config', str(self.root / 'missing.json')], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['ok'])

    @unittest.skipUnless(NODE, 'Node required for extracted skill inspection')
    def test_extracted_and_core_installed_inspector_is_self_contained(self):
        self.check()
        node = NODE
        archive = self.root / 'source.zip'
        subprocess.run([node, str(ROOT / 'scripts/bundle.mjs'), str(archive)], check=True, capture_output=True)
        with zipfile.ZipFile(archive) as z:
            z.extractall(self.root / 'unpacked')
        extracted = self.root / 'unpacked/hypit-haiyi-workflow'
        codex = self.root / 'new codex'
        subprocess.run([node, str(extracted / 'scripts/workflow.mjs'), 'install-skill', '--core-only'], check=True, capture_output=True, env={**os.environ, 'CODEX_HOME': str(codex)})
        for entry in (extracted / 'scripts/migration.py', codex / 'skills/koroflow/scripts/migration.py'):
            result = subprocess.run([sys.executable, '-X', 'utf8', str(entry), '--config', str(self.root / 'machine.json'), '--request', str(self.root / 'request.json')], check=True, capture_output=True, text=True, encoding='utf-8')
            self.assertTrue(json.loads(result.stdout)['ok'])
        self.assertTrue((codex / 'skills/koroflow/assets/templates/machine.example.json').is_file())


if __name__ == '__main__':
    unittest.main()
