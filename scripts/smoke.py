#!/usr/bin/env python3
"""Read-only post-deployment checks. Run after the configured edge TTL."""
import argparse,json,re
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler,Request,build_opener,urlopen
from urllib.error import HTTPError
parser=argparse.ArgumentParser();parser.add_argument('--base',default='https://www.janbrennenstuhl.eu');args=parser.parse_args();base=args.base.rstrip('/')
paths=['/','/agentic-identity-broker/','/agentic-identity-broker/index.md','/catalog.json','/findings.json','/feed.json','/search/index.json','/index.xml','/sitemap.xml','/llms.txt','/llms-full.txt']
for path in paths:
    with urlopen(Request(base+path,headers={'Cache-Control':'no-cache','Accept-Encoding':'identity'}),timeout=30) as response:
        body=response.read();headers=response.headers
        if response.status!=200:raise SystemExit(f'{path}: unexpected {response.status}')
        control=headers.get('Cache-Control','')
        age=re.search(r'(?:^|,)\s*max-age=(\d+)',control)
        if not (('no-cache' in control) or ('no-store' in control) or (age and int(age[1])==0)):raise SystemExit(f'{path}: mutable browser caching still unsafe: {control}')
        if path.endswith('.md') and 'text/markdown' not in headers.get('Content-Type',''):raise SystemExit(f'{path}: wrong MIME type')
        if path=='/catalog.json':
            catalog=json.loads(body)
            if not str(catalog.get('schema_version','')).startswith('1.'):raise SystemExit('Catalog version mismatch')
        conditional={}
        if headers.get('ETag'):conditional['If-None-Match']=headers['ETag']
        elif headers.get('Last-Modified'):conditional['If-Modified-Since']=headers['Last-Modified']
        if not conditional:raise SystemExit(f'{path}: missing validator')
        try:
            with urlopen(Request(base+path,headers=conditional),timeout=30) as second:raise SystemExit(f'{path}: conditional request returned {second.status}, expected 304')
        except HTTPError as error:
            if error.code!=304:raise
    print(path,'OK')
try:
    with urlopen(base+'/__release-smoke-missing-page__/',timeout=30) as response:raise SystemExit(f'Missing page returned {response.status}')
except HTTPError as error:
    if error.code!=404:raise
# Every retired route gets a real 301 from the edge rules, not the HTML fallback page.
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args):return None
opener=build_opener(NoRedirect)
with urlopen(base+'/redirects.json',timeout=30) as response:redirects=json.load(response)['redirects']
for r in redirects:
    try:
        with opener.open(base+r['from'],timeout=30) as response:raise SystemExit(f"{r['from']}: returned {response.status}, expected 301 (edge rules not synced?)")
    except HTTPError as error:
        location=error.headers.get('Location','')
        if error.code!=r['status'] or urlsplit(location).path!=r['to']:raise SystemExit(f"{r['from']}: {error.code} to {location}, expected {r['status']} to {r['to']}")
print(f'{len(redirects)} redirects OK')
print('Live mutable-cache, MIME, conditional retrieval, 404 and redirect checks passed.')
