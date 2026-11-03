#!/usr/bin/env python3
"""Upload an already verified artifact to Bunny Storage. Never deletes remote files.

Files go up in four phases (assets, documents, feeds and catalogs, release manifest); each phase
uploads in parallel and finishes before the next starts. A production upload skips files whose
checksum matches the release manifest already in the storage zone, which is written last and so
describes the last release that finished. --full uploads everything."""
from __future__ import annotations
import argparse,hashlib,json,mimetypes,os,re,sys,tempfile,time
from concurrent.futures import FIRST_EXCEPTION,ThreadPoolExecutor,wait
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from urllib.parse import quote

WORKERS=8
MANIFEST='release-manifest.json'

def upload_phases(root):
    """Assets, then HTML and Markdown, then feeds and catalogs, then the release manifest alone."""
    assets=[];documents=[];discovery=[];manifest=[]
    for path in sorted(root.rglob('*')):
        if not path.is_file():continue
        if path.relative_to(root).as_posix()==MANIFEST:manifest.append(path)
        elif path.suffix in ('.html','.md'):documents.append(path)
        elif path.suffix in ('.json','.xml','.txt'):discovery.append(path)
        else:assets.append(path)
    return [assets,documents,discovery,manifest]

def upload_order(root):
    return [path for phase in upload_phases(root) for path in phase]

def unchanged(phases,root,previous):
    """Drop files whose bytes match the previous release. The manifest itself always uploads."""
    if not previous:return phases,0
    kept=[];skipped=0
    for phase in phases:
        out=[]
        for path in phase:
            rel=path.relative_to(root).as_posix()
            if rel!=MANIFEST and previous.get(rel)==hashlib.sha256(path.read_bytes()).hexdigest():skipped+=1
            else:out.append(path)
        kept.append(out)
    return kept,skipped

def previous_manifest(host,zone,key):
    """The manifest of the last finished release, read from storage (not the CDN). {} means upload everything."""
    url=f'https://{host}/{quote(zone,safe="")}/{MANIFEST}'
    try:
        with urlopen(Request(url,headers={'AccessKey':key}),timeout=30) as response:files=json.load(response).get('files')
    except (HTTPError,URLError,TimeoutError,ValueError,AttributeError):return {}
    if not isinstance(files,dict) or not all(isinstance(k,str) and isinstance(v,str) for k,v in files.items()):return {}
    return files

def upload_phased(phases,root,host,zone,key):
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for phase in phases:
            futures=[pool.submit(upload_file,path,root,host,zone,key) for path in phase]
            done,pending=wait(futures,return_when=FIRST_EXCEPTION)
            for future in pending:future.cancel()
            for future in done:future.result()

def mime(path):
    if path.name=='api-catalog':return 'application/linkset+json'
    if path.name=='traffic-advice':return 'application/trafficadvice+json'
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
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path('public'));parser.add_argument('--dry-run',action='store_true');parser.add_argument('--full',action='store_true',help='Upload every file, even ones the previous release already has');parser.add_argument('--preview',action='store_true',help='Upload to the staging zone (BUNNY_PREVIEW_* variables only)');args=parser.parse_args()
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
        upload_phased(upload_phases(root),root,host,zone,key)
        print(f'Preview uploaded: {len(files)} files to staging zone {zone}.');return
    if os.environ.get('RELEASE_EVENT')!='push' or os.environ.get('RELEASE_REF')!='refs/heads/main':raise SystemExit('Production upload requires a main-branch push')
    host=(os.environ.get('BUNNY_STORAGE_HOST') or 'storage.bunnycdn.com');zone=os.environ['BUNNY_STORAGE_ZONE'];key=os.environ['BUNNY_STORAGE_PASSWORD']
    if host!='storage.bunnycdn.com' and not re.fullmatch(r'[a-z0-9-]+\.storage\.bunnycdn\.com',host):raise SystemExit('Invalid Bunny Storage host')
    if not re.fullmatch(r'[A-Za-z0-9_-]+',zone):raise SystemExit('Invalid storage zone')
    index_key=os.environ.get('INDEXNOW_KEY','')
    verification_key=index_key
    previous={}
    if index_key:
        if not re.fullmatch(r'[A-Za-z0-9-]{8,128}',index_key):raise SystemExit('Invalid IndexNow key')
        try:
            with urlopen(Request('https://www.janbrennenstuhl.eu/catalog.json',headers={'Cache-Control':'no-cache'}),timeout=30) as response:previous=json.load(response)
        except (HTTPError,URLError,ValueError):
            print('Previous catalog unavailable; changed-URL notification will be skipped.')
            index_key=''
    phases,skipped=unchanged(upload_phases(root),root,{} if args.full else previous_manifest(host,zone,key))
    upload_phased(phases,root,host,zone,key)
    if verification_key:
        # The verification file stays out of the artifact so the key never reaches verify or PR builds.
        with tempfile.TemporaryDirectory() as tmp:
            keyfile=Path(tmp)/f'{verification_key}.txt';keyfile.write_text(verification_key+'\n')
            upload_file(keyfile,Path(tmp),host,zone,key)
    if index_key:
        from indexnow import notify
        try:notify(previous,json.loads((root/'catalog.json').read_text()),index_key)
        except (HTTPError,URLError,RuntimeError,ValueError):print('Deployment succeeded; IndexNow failed and can be retried separately.')
    print(f'Uploaded {len(files)-skipped} of {len(files)} files ({skipped} unchanged since the last release). Prior assets retained. No account-wide credential used.')
if __name__=='__main__':main()
