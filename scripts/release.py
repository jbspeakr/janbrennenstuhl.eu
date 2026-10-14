#!/usr/bin/env python3
"""Record deterministic checksums and retain a local rollback archive."""
import hashlib,json,subprocess,tarfile
from pathlib import Path
root=Path('public');rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
if subprocess.check_output(['git','status','--porcelain'],text=True).strip():raise SystemExit('Commit source changes and rebuild before packaging a release')
catalog=json.loads((root/'catalog.json').read_text())
if any(item['source_revision']!=rev for item in catalog['items']):raise SystemExit('Rebuild the clean source revision before packaging')
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and p.name!='release-manifest.json'}
(root/'release-manifest.json').write_text(json.dumps({'revision':rev,'files':manifest},sort_keys=True)+'\n')
Path('releases').mkdir(exist_ok=True)
with tarfile.open(f'releases/{rev}.tar.gz','w:gz') as archive:archive.add(root,arcname='public')
print(f'Release {rev}: {len(manifest)} files; releases/{rev}.tar.gz')
