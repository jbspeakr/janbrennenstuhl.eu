#!/usr/bin/env python3
"""Upload an already verified artifact to Bunny Storage. Never deletes remote files."""
from __future__ import annotations
import argparse,hashlib,json,mimetypes,os,re,sys,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from urllib.parse import quote

def upload_order(root):
    assets=[];documents=[];discovery=[]
    for path in sorted(root.rglob('*')):
        if not path.is_file():continue
        rel=path.relative_to(root).as_posix()
        if path.suffix in ('.html','.md'):documents.append(path)
        elif path.suffix in ('.json','.xml','.txt'):discovery.append(path)
        else:assets.append(path)
    return assets+documents+[p for p in discovery if p.name!='release-manifest.json']+[p for p in discovery if p.name=='release-manifest.json']

def mime(path):
    if path.name=='api-catalog':return 'application/linkset+json'
    if path.name=='feed.json':return 'application/feed+json; charset=utf-8'
    return {'.md':'text/markdown; charset=utf-8','.txt':'text/plain; charset=utf-8','.xml':'application/xml; charset=utf-8','.json':'application/json; charset=utf-8','.woff2':'font/woff2','.avif':'image/avif','.webp':'image/webp'}.get(path.suffix,mimetypes.guess_type(path.name)[0] or 'application/octet-stream')

def upload_file(path,root,host,zone,key):
    data=path.read_bytes();url=f'https://{host}/{quote(zone,safe="")}/{quote(path.relative_to(root).as_posix(),safe="/")}'
    request=Request(url,data=data,method='PUT',headers={'AccessKey':key,'Content-Type':mime(path),'Checksum':hashlib.sha256(data).hexdigest().upper()})
    for attempt in range(3):
        try:
            with urlopen(request,timeout=60) as response:
                if response.status not in (200,201):raise RuntimeError(f'Upload failed ({response.status})')
            return
        except HTTPError as error:
            if error.code<500 and error.code!=429:raise RuntimeError(f'Upload rejected ({error.code}) for {path.relative_to(root)}') from None
            if attempt==2:raise RuntimeError(f'Upload failed for {path.relative_to(root)}') from None
        except (URLError,TimeoutError):
            if attempt==2:raise RuntimeError(f'Upload failed for {path.relative_to(root)}') from None
        time.sleep(2**attempt)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path('public'));parser.add_argument('--dry-run',action='store_true');parser.add_argument('--preview',action='store_true',help='Upload to the staging zone (BUNNY_PREVIEW_* variables only)');args=parser.parse_args()
    root=args.root.resolve()
    if not (root/'catalog.json').is_file():raise SystemExit('Verified artifact required')
    files=upload_order(root)
    if args.dry_run:
        print(json.dumps({'files':len(files),'first':files[0].relative_to(root).as_posix(),'last':files[-1].relative_to(root).as_posix(),'deletes':0}));return
    if args.preview:
        # Staging only: separate credentials, never IndexNow, never the production variables.
        if os.environ.get('BUNNY_STORAGE_ZONE') or os.environ.get('BUNNY_STORAGE_PASSWORD'):raise SystemExit('Preview uploads must not see production credentials')
        host=(os.environ.get('BUNNY_PREVIEW_HOST') or 'storage.bunnycdn.com');zone=os.environ['BUNNY_PREVIEW_ZONE'];key=os.environ['BUNNY_PREVIEW_PASSWORD']
        if host!='storage.bunnycdn.com' and not re.fullmatch(r'[a-z0-9-]+\.storage\.bunnycdn\.com',host):raise SystemExit('Invalid Bunny Storage host')
        if not re.fullmatch(r'[A-Za-z0-9_-]+',zone):raise SystemExit('Invalid storage zone')
        for path in files:upload_file(path,root,host,zone,key)
        print(f'Preview uploaded: {len(files)} files to staging zone {zone}.');return
    if os.environ.get('FORGEJO_EVENT_NAME')!='push' or os.environ.get('FORGEJO_REF')!='refs/heads/main':raise SystemExit('Production upload requires a main-branch push')
    host=(os.environ.get('BUNNY_STORAGE_HOST') or 'storage.bunnycdn.com');zone=os.environ['BUNNY_STORAGE_ZONE'];key=os.environ['BUNNY_STORAGE_PASSWORD']
    if host!='storage.bunnycdn.com' and not re.fullmatch(r'[a-z0-9-]+\.storage\.bunnycdn\.com',host):raise SystemExit('Invalid Bunny Storage host')
    if not re.fullmatch(r'[A-Za-z0-9_-]+',zone):raise SystemExit('Invalid storage zone')
    index_key=os.environ.get('INDEXNOW_KEY','')
    previous={}
    if index_key:
        if not (root/(index_key+'.txt')).is_file():raise SystemExit('IndexNow key missing from verified artifact')
        try:
            with urlopen(Request('https://www.janbrennenstuhl.eu/catalog.json',headers={'Cache-Control':'no-cache'}),timeout=30) as response:previous=json.load(response)
        except (HTTPError,URLError,ValueError):
            print('Previous catalog unavailable; changed-URL notification will be skipped.')
            index_key=''
    for path in files:upload_file(path,root,host,zone,key)
    if index_key:
        from indexnow import notify
        try:notify(previous,json.loads((root/'catalog.json').read_text()),index_key)
        except (HTTPError,URLError,RuntimeError,ValueError):print('Deployment succeeded; IndexNow failed and can be retried separately.')
    print(f'Uploaded {len(files)} files. Prior assets retained. No account-wide credential used.')
if __name__=='__main__':main()
