#!/usr/bin/env python3
"""Release contracts: routes, anchors, semantic metadata, parity, feeds and budgets."""
import gzip,hashlib,json,re,sys
from pathlib import Path
from urllib.parse import urlsplit,unquote,urljoin
from datetime import datetime,timezone
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import yaml
R=Path(__file__).resolve().parents[1];P=R/'public';errors=[]
def check(ok,message):
    if not ok:errors.append(message)
def local_path(url):
    path=unquote(urlsplit(url).path).lstrip('/')
    target=P/path
    if not target.suffix or urlsplit(url).path.endswith('/'):target=target/'index.html'
    return target
soups={p:BeautifulSoup(p.read_text(),'html.parser') for p in P.rglob('*.html')}
for route,old in json.loads((R/'tests/fixtures/baseline-routes.json').read_text()).items():
    path=P/route.lstrip('/')
    check(path in soups,f'Lost route: {route}')
    if path not in soups:continue
    ids={e.get('id') for e in soups[path].select('[id]')}
    for heading in old['headings']:check(heading in ids,f'Lost heading {route}#{heading}')
for path,soup in soups.items():
    route='/'+path.relative_to(P).as_posix().removesuffix('index.html')
    redirect=soup.find('meta',attrs={'http-equiv':'refresh'})
    if not redirect:
        check(bool(soup.title and soup.title.get_text().strip()),f'Empty title {route}')
        check(len(soup.select('h1'))==1,f'Expected one h1 {route}')
        check(bool(soup.find('main')),f'Missing main {route}')
        canonical=soup.find('link',rel='canonical')
        check(bool(canonical),f'Missing canonical {route}')
        if canonical and path.name=='index.html':check(urlsplit(canonical['href']).path==route,f'Canonical mismatch {route}: {canonical["href"]}')
        for script in soup.select('script[type="application/ld+json"]'):
            try:
                data=json.loads(script.string)
                for entity in data.get('@graph',[]):
                    if entity.get('inLanguage') is not None:check(entity['inLanguage']=='en-GB',f'Language {route}')
                    for key in ('datePublished','dateModified'):
                        if key in entity:check(datetime.fromisoformat(entity[key]).tzinfo is not None,f'Naive schema date {route}')
                    if entity.get('image'):check(entity['image'].startswith('https://'),f'Relative schema image {route}')
                    if entity.get('@type') in ('Article','BlogPosting','TechArticle'):check(bool(soup.select('[data-article-body]')),f'Article schema on utility page {route}')
            except Exception as e:errors.append(f'JSON-LD {route}: {e}')
        for link in soup.select('.pagination a[href]'):
            check(link['href']!=route,f'Pagination points to itself {route}')
            check('//' not in link['href'],f'Malformed pagination link {route}')
        for image in soup.select('img'):check(image.has_attr('alt'),f'Image lacks alt {route}')
        for node in soup.select('script[src],link[rel="stylesheet"]'):check(not node.get('src',node.get('href','')).startswith('https://'),f'Third-party initial dependency {route}')
    ids=[e['id'] for e in soup.select('[id]')]
    check(len(ids)==len(set(ids)),f'Duplicate IDs {route}')
    for el in soup.select('a[href],img[src],script[src],link[href]'):
        raw=el.get('href',el.get('src',''))
        if not raw or raw.startswith(('mailto:','tel:','data:')):continue
        url=urlsplit(urljoin('https://www.janbrennenstuhl.eu'+route,raw))
        if url.netloc!='www.janbrennenstuhl.eu':continue
        target=local_path(url.geturl())
        check(target.exists(),f'Missing local target {route} -> {raw}')
        if url.fragment and target in soups and not soups[target].find('meta',attrs={'http-equiv':'refresh'}):
            check(bool(soups[target].find(id=unquote(url.fragment))),f'Broken fragment {route} -> {raw}')
check(soups[P/'index.html'].select_one('.pagination a')['href']=='/2/','Homepage next page must be /2/')
check([a['href'] for a in soups[P/'2/index.html'].select('.pagination a')]==['/','/3/'],'Page 2 navigation must reach neighbors')
catalog=json.loads((P/'content-index.json').read_text());search=json.loads((P/'search/index.json').read_text())
check(catalog['schema_version']=='1.0','Catalog version')
check({x['id'] for x in catalog['items']}=={x['id'] for x in search},'Search/catalog coverage differs')
check(len([i for i in catalog['items'] if i['kind']=='research'])==7,'Expected seven existing research articles')
check(len({i['id'] for i in catalog['items']})==len(catalog['items']),'Duplicate catalog IDs')
for item in catalog['items']:
    path=local_path(item['canonical_url']);soup=soups[path];mdpath=path.with_name('index.md');md=mdpath.read_text()
    check(hashlib.sha256(md.encode()).hexdigest()==item['content_hash'].removeprefix('sha256:'),f'Hash {item["id"]}')
    fm=yaml.safe_load(md.split('---',2)[1]);htmlmeta=json.loads(soup.select_one('#content-metadata').string)
    for key in ('id','title','description','canonical_url','author','published','modified','review_status','license','topics'):
        check(fm[key]==item[key]==htmlmeta[key],f'Metadata parity {item["id"]}: {key}')
    check('{{<' not in md and '{{%' not in md,f'Shortcode leaked {item["id"]}')
    check(path.with_name('social.png').exists(),f'Missing social card {item["id"]}')
    check(soup.find('link',attrs={'type':'text/markdown'})['href']==item['markdown_url'],f'Discovery {item["id"]}')
    for heading in soup.select('[data-article-body] h2[id],[data-article-body] h3[id]'):
        check(f'<a id="{heading["id"]}"></a>' in md,f'Markdown anchor missing {item["id"]}#{heading["id"]}')
    for code in soup.select('[data-article-body] pre code'):
        check(code.get_text().rstrip() in md,f'Code fidelity {item["id"]}')
    for link in soup.select('[data-article-body] a[href]:not(.heading-anchor)'):
        check(urljoin(item['canonical_url'],link['href']) in md,f'Link fidelity {item["id"]}: {link["href"]}')
    for img in soup.select('[data-article-body] img'):
        check(img.get('alt','') in md,f'Image description lost {item["id"]}')
    check(item['canonical_url']+'index.md' in (P/'llms.txt').read_text(),f'Directory missing {item["id"]}')
# Detect draft leakage against source routes and distinctive titles.
for path in (R/'content').rglob('*.md'):
    data=yaml.safe_load(path.read_text().split('---',2)[1]) or {}
    if data.get('draft'):
        check(not any(i['title']==data.get('title') for i in catalog['items']),f'Draft leaked: {path}')
for path in P.rglob('*.xml'):
    try:ET.parse(path)
    except ET.ParseError as e:errors.append(f'XML {path}: {e}')
expiry=re.search(r'^Expires: (.+)$',(P/'.well-known/security.txt').read_text(),re.M)
days=(datetime.fromisoformat(expiry[1].replace('Z','+00:00'))-datetime.now(timezone.utc)).days
check(days>0,'security.txt expired')
if days<60:print(f'WARNING: security.txt expires in {days} days')
css=sum(len(gzip.compress(p.read_bytes(),mtime=0)) for p in (P/'css').glob('*.css'))
js=sum(len(gzip.compress(p.read_bytes(),mtime=0)) for p in (P/'js').glob('*.js') if not p.name.startswith('search.'))
check(css<=25000,f'CSS budget: {css}')
check(js<=15000,f'JS budget: {js}')
print(f'Checked {len(soups)} HTML routes; {len(catalog["items"])} machine-readable entries. Gzip: CSS {css} B; shared JS {js} B.')
if errors:
    print('\n'.join(errors));sys.exit(1)
print('All static release contracts passed.')
