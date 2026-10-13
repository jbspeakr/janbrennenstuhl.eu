#!/usr/bin/env python3
import hashlib,json,subprocess
from pathlib import Path
root=Path('public');manifest=json.loads((root/'release-manifest.json').read_text())
revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
if manifest['revision']!=revision:raise SystemExit('Artifact/source revision mismatch')
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='release-manifest.json'}
if actual!=set(manifest['files']):raise SystemExit('Artifact file inventory mismatch')
for name,expected in manifest['files'].items():
    if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:raise SystemExit(f'Checksum mismatch: {name}')
print('Release integrity verified.')
