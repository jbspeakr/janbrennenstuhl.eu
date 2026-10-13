#!/usr/bin/env python3
"""Notify only changed canonical entries, after a successful upload. Optional."""
import json,os,re
from pathlib import Path
from urllib.request import Request,urlopen

def changed_urls(previous,current):
    before={x['id']:x.get('content_hash') for x in previous.get('items',[])}
    return [x['canonical_url'] for x in current['items'] if before.get(x['id'])!=x.get('content_hash')]

def notify(previous,current,key):
    if not key:return
    if not re.fullmatch(r'[A-Za-z0-9-]{8,128}',key):raise ValueError('Invalid IndexNow verification key')
    urls=changed_urls(previous,current)
    if not urls:return
    body=json.dumps({'host':'www.janbrennenstuhl.eu','key':key,'keyLocation':f'https://www.janbrennenstuhl.eu/{key}.txt','urlList':urls}).encode()
    with urlopen(Request('https://api.indexnow.org/indexnow',data=body,headers={'Content-Type':'application/json'}),timeout=30) as response:
        if response.status not in (200,202):raise RuntimeError('IndexNow submission failed')
    print(f'IndexNow accepted {len(urls)} changed canonical URLs.')
