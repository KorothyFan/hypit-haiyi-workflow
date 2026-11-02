#!/usr/bin/env node
import { cp, mkdtemp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { crc32, deflateRawSync } from 'node:zlib';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const destination = resolve(process.argv[2] || join(root, '..', 'hypit-haiyi-workflow.zip'));
const entries = ['README.md', 'NOTICE.md', 'AGENTS.md', 'package.json', '.gitignore', '.gitattributes', '.env.example', 'upstream.json',
  'plugin.json', '.agents/plugins/marketplace.json', 'docs/operations.md',
  'scripts/operations.py', 'tests/test_operations.py', 'tests/test_distribution.py',
  'scripts/koroflow.py', 'tests/test_workflow.py', 'docs/architecture.md', 'docs/haiyi-hypit.md', 'CHANGELOG.md',
  'schemas/work.schema.json', 'schemas/adapter.schema.json',
  'skills/koroflow/SKILL.md', 'skills/koroflow/agents/openai.yaml',
  'skills/koroflow/references/defaults.json', 'skills/koroflow/references/adapters.md',
  'skills/koroflow/references/workflow.md', 'skills/koroflow/references/production-standard.md', 'skills/koroflow/scripts/workflow.py',
  'skills/koroflow/references/production-paths.md',
  'skills/koroflow/references/production-paths/source-video-edit.md',
  'skills/koroflow/references/production-paths/reference-rebuild.md',
  'skills/koroflow/references/production-paths/scene-to-video.md',
  'skills/koroflow/references/production-paths/state-and-prop-continuity.md',
  'skills/koroflow/references/cases/knitted-dolls.md',
  'skills/koroflow/references/production-paths/visual-only-audio-preserve.md',
  'skills/koroflow/references/production-paths/audio-repair.md',
  'skills/koroflow/references/production-paths/sequential-comic.md',
  'skills/koroflow/references/production-paths/intake-and-compilation.md',
  'skills/koroflow/assets/templates/work.example.json', 'skills/koroflow/assets/templates/review.example.json',
  'skills/koroflow/assets/templates/path-experience.md',
  'skills/koroflow/assets/templates/state-asset-binding.md',
  'skills/koroflow/assets/templates/adapter.example.json',
  'skills/koroflow/scripts/koroflow_core/__init__.py', 'skills/koroflow/scripts/koroflow_core/core.py',
  'skills/koro-operations/SKILL.md', 'skills/koro-operations/agents/openai.yaml',
  'skills/koro-operations/scripts/operations.py',
  'skills/koro-operations/references/setup.md', 'skills/koro-operations/references/records.md',
  'skills/koro-operations/references/publication.md',
  'scripts/workflow.mjs', 'scripts/test-bootstrap.mjs', 'scripts/bundle.mjs',
  'skills/hypit-haiyi/SKILL.md', 'skills/hypit-haiyi/agents/openai.yaml',
  'skills/hypit-haiyi/references/setup.md', 'skills/hypit-haiyi/references/capabilities.md',
  'skills/hypit-haiyi/references/production.md', 'templates', 'third-party', 'packages/provider-haiyi/package.json',
  'skills/hypit-haiyi/references/character-replacement.md',
  'skills/hypit-haiyi/references/multi-version-recreation.md',
  'skills/hypit-haiyi/references/prompt-direction.md', 'skills/hypit-haiyi/references/h3-integration.md',
  'skills/video-director/SKILL.md', 'skills/video-director/agents/openai.yaml',
  'skills/video-director/references/storyboard-handoff.md',
  'skills/video-director/references/reference-adaptation.md',
  'packages/provider-haiyi/tsconfig.json', 'packages/provider-haiyi/src', 'packages/provider-haiyi/test'];
const temp = await mkdtemp(join(tmpdir(), 'hypit-haiyi-bundle-'));
try {
  const stage = join(temp, 'hypit-haiyi-workflow');
  for (const entry of entries) {
    await mkdir(dirname(join(stage, entry)), { recursive: true });
    await cp(join(root, entry), join(stage, entry), { recursive: true });
  }
  await mkdir(dirname(destination), { recursive: true });
  // Small source archive: standard ZIP/deflate with UTF-8 filenames; no platform archive tool needed.
  const files = [];
  async function walk(dir, prefix) {
    for (const entry of (await readdir(dir, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
      const name = `${prefix}/${entry.name}`;
      if (entry.isSymbolicLink()) throw new Error(`Refusing to package a symbolic link: ${name}`);
      if (entry.isDirectory()) await walk(join(dir, entry.name), name);
      else if (entry.isFile()) files.push({ name, data: await readFile(join(dir, entry.name)) });
    }
  }
  await walk(stage, 'hypit-haiyi-workflow');
  const local = [], central = [];
  let offset = 0, centralSize = 0;
  for (const { name, data } of files) {
    const filename = Buffer.from(name, 'utf8'), packed = deflateRawSync(data), checksum = crc32(data);
    const header = Buffer.alloc(30);
    header.writeUInt32LE(0x04034b50, 0); header.writeUInt16LE(20, 4); header.writeUInt16LE(0x800, 6);
    header.writeUInt16LE(8, 8); header.writeUInt16LE(33, 12); // Jan 1, 1980, deterministic archive date.
    header.writeUInt32LE(checksum, 14); header.writeUInt32LE(packed.length, 18);
    header.writeUInt32LE(data.length, 22); header.writeUInt16LE(filename.length, 26);
    const directory = Buffer.alloc(46);
    directory.writeUInt32LE(0x02014b50, 0); directory.writeUInt16LE(20, 4); directory.writeUInt16LE(20, 6);
    directory.writeUInt16LE(0x800, 8); directory.writeUInt16LE(8, 10); directory.writeUInt16LE(33, 14);
    directory.writeUInt32LE(checksum, 16); directory.writeUInt32LE(packed.length, 20);
    directory.writeUInt32LE(data.length, 24); directory.writeUInt16LE(filename.length, 28);
    directory.writeUInt32LE(offset, 42);
    local.push(header, filename, packed); central.push(directory, filename);
    offset += header.length + filename.length + packed.length;
    centralSize += directory.length + filename.length;
  }
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0); end.writeUInt16LE(files.length, 8); end.writeUInt16LE(files.length, 10);
  end.writeUInt32LE(centralSize, 12); end.writeUInt32LE(offset, 16);
  await writeFile(destination, Buffer.concat([...local, ...central, end]));
  console.log(`Source + skill archive: ${destination}`);
} finally {
  await rm(temp, { recursive: true, force: true });
}
