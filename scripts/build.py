#!/usr/bin/env python3
"""Build all public representations from canonical Hugo HTML, then validate."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
import yaml

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'

class ArticleMarkdown(MarkdownConverter):
    def convert_hN(self, n, el, text, parent_tags):
        heading = super().convert_hN(n, el, text, parent_tags)
        return f'\n<a id="{el["id"]}"></a>\n' + heading if el.get('id') else heading
    def convert_a(self, el, text, parent_tags):
        anchor = f'<a id="{el["id"]}"></a>' if el.get("id") else ""
        return anchor + super().convert_a(el, text, parent_tags)
    def convert_pre(self, el, text, parent_tags):
        code = el.find('code')
        source = code.get_text() if code else el.get_text()
        language = (code.get('data-lang', '') if code else '')
        fence = '`' * max(3, max((len(x) + 1 for x in re.findall(r'`+', source)), default=3))
        return f'\n\n{fence}{language}\n{source.rstrip()}\n{fence}\n\n'
    def convert_details(self, el, text, parent_tags):
        return '\n\n' + text.strip() + '\n\n'
    def convert_summary(self, el, text, parent_tags):
        return '\n\n**' + text.strip() + '**\n\n'

def read_frontmatter(path):
    return yaml.safe_load(path.read_text().split('---', 2)[1]) or {}

def validate_source():
    seen = set()
    from datetime import date, datetime, timezone
    for path in sorted((ROOT / 'content').rglob('*.md')):
        data = read_frontmatter(path)
        if data.get('draft') or path.name != 'index.md' or path.relative_to(ROOT / 'content').parts[0] not in ('post','knowledge-base','projects','talks'): continue
        for field in ('id','title','description','date','kind','topics','status','reviewStatus'):
            if not data.get(field): raise ValueError(f'{path}: missing {field}')
        if data['id'] in seen: raise ValueError(f'Duplicate id: {data["id"]}')
        seen.add(data['id'])
        if data['kind'] not in ('essay','research','guide','project','talk'): raise ValueError(f'{path}: invalid kind')
        if data['status'] not in ('published','archived','superseded'): raise ValueError(f'{path}: invalid status')
        if data['status'] == 'superseded' and not data.get('supersededBy'): raise ValueError(f'{path}: supersededBy required')
        if data['reviewStatus'] not in ('not-reviewed','reviewed'): raise ValueError(f'{path}: invalid review status')
        if data['reviewStatus'] == 'reviewed' and not data.get('reviewed'): raise ValueError(f'{path}: reviewed date required')
        if not isinstance(data['topics'],list) or not all(isinstance(t,str) for t in data['topics']): raise ValueError(f'{path}: topics must be strings')
        def as_datetime(value):
            if isinstance(value, datetime): return value.replace(tzinfo=value.tzinfo or timezone.utc)
            if isinstance(value, date): return datetime.combine(value,datetime.min.time(),timezone.utc)
            return datetime.fromisoformat(str(value)).replace(tzinfo=timezone.utc)
        if as_datetime(data.get('lastmod',data['date'])) < as_datetime(data['date']): raise ValueError(f'{path}: lastmod precedes publication')
        if data.get('image') and not (data.get('imageAlt') or data.get('imageDecorative') is True): raise ValueError(f'{path}: image needs alt text or imageDecorative: true')
        if data.get('image') and not (path.parent / data['image']).is_file(): raise ValueError(f'{path}: missing image')
    return len(seen)

def absolute_links(soup, canonical):
    for el in soup.select('[href], [src], [srcset]'):
        for attr in ('href','src'):
            if el.get(attr): el[attr] = urljoin(canonical, el[attr])
        if el.get('srcset'):
            el['srcset'] = ', '.join(urljoin(canonical, x.strip().split()[0]) + ' ' + ' '.join(x.strip().split()[1:]) for x in el['srcset'].split(','))

def export_article(soup, item):
    body = soup.select_one('[data-article-body]')
    if body is None: raise ValueError(f'No article body: {item["canonical_url"]}')
    fragment = BeautifulSoup('', 'html.parser')
    for selector in ('.article-header .lead', '.article-hero', '[data-article-body]'):
        el = soup.select_one(selector)
        if el: fragment.append(BeautifulSoup(str(el), 'html.parser'))
    for a in fragment.select('.heading-anchor'): a.decompose()
    absolute_links(fragment, item['canonical_url'])
    for node in list(fragment.select('[id]')):
        if node.name not in ('a','h1','h2','h3','h4','h5','h6'):
            anchor = fragment.new_tag('a', id=node['id'])
            node.insert_before(anchor)
            del node['id']
    sections=[]
    for heading in fragment.select('h2[id],h3[id],h4[id],h5[id],h6[id]'):
        chunks=[]
        for sibling in heading.next_siblings:
            if getattr(sibling,'name',None) in ('h2','h3','h4','h5','h6'):break
            chunks.append(sibling.get_text(' ',strip=True) if hasattr(sibling,'get_text') else str(sibling))
        sections.append({'id':heading['id'],'title':heading.get_text(' ',strip=True),'text':' '.join(chunks)})
    content = ArticleMarkdown(heading_style='ATX', bullets='-', table_infer_header=True).convert(str(fragment)).strip()
    if re.search(r'\{\{[<%]',content):raise ValueError(f'Unresolved shortcode: {item["id"]}')
    metadata={k:v for k,v in item.items() if k not in ('content_hash','sections','source_revision','source_url')}
    # Revision metadata belongs in the catalog. Markdown remains stable across unrelated builds.
    header=yaml.safe_dump(metadata,sort_keys=False,allow_unicode=True).strip()
    markdown=f'---\n{header}\n---\n\n# {item["title"]}\n\n{content}\n'
    return markdown, sections, fragment.get_text(' ',strip=True)

def finish_outputs():
    catalog = json.loads((PUBLIC/'content-index.json').read_text())
    by_url={item['canonical_url']:item for item in catalog['items']}
    search=[]
    for path in sorted(PUBLIC.rglob('*.html')):
        soup=BeautifulSoup(path.read_text(),'html.parser')
        if soup.find('meta',attrs={'http-equiv':'refresh'}): continue
        # HTML semantics and overflow behavior must also work without JavaScript.
        for table in soup.select('.prose table'):
            region=soup.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','role':'region','aria-label':'Scrollable table'})
            table.wrap(region)
        for pre in soup.select('pre'):pre['tabindex']='0'
        for link in soup.select('a[role="button"]'):del link['role']
        canonical=soup.find('link',rel='canonical')
        item=by_url.get(canonical.get('href')) if canonical else None
        if item:
            markdown,sections,plain=export_article(soup,item)
            path.with_name('index.md').write_text(markdown)
            item['content_hash']='sha256:'+hashlib.sha256(markdown.encode()).hexdigest()
            item['sections']=[{'id':s['id'],'title':s['title'],'url':item['canonical_url']+'#'+s['id']} for s in sections]
            # Keep metadata and catalog consistent, excluding only bulky section descriptors.
            soup.select_one('#content-metadata').string=json.dumps({k:v for k,v in item.items() if k!='sections'},ensure_ascii=False).replace('<','\\u003c')
            search.append({k:item[k] for k in ('id','title','description','canonical_url','kind','topics','published')} | {'content':plain,'sections':sections})
        path.write_text(str(soup))
    (PUBLIC/'content-index.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n')
    (PUBLIC/'search/index.json').write_text(json.dumps(search,ensure_ascii=False,separators=(',',':'))+'\n')
    # Feed clients need absolute article links and image URLs.
    import xml.etree.ElementTree as ET
    for path in PUBLIC.rglob('*.xml'):
        if path.name != 'index.xml':continue
        tree=ET.parse(path)
        for entry in tree.findall('./channel/item'):
            desc=entry.find('description')
            if desc is not None and desc.text:
                fragment=BeautifulSoup(desc.text,'html.parser')
                absolute_links(fragment,entry.findtext('link'))
                desc.text=str(fragment)
        tree.write(path,encoding='utf-8',xml_declaration=True)
    print(f'Exported {len(search)} faithful Markdown documents and searchable entries.')

def build(minify=True):
    os.chdir(ROOT)
    count=validate_source()
    hugo=os.environ.get('HUGO','hugo')
    version=subprocess.check_output([hugo,'version'],text=True)
    required=(ROOT/'.hugo-version').read_text().strip()
    if not re.search(r'v'+re.escape(required)+r'(?:-|\+|\s)',version):raise ValueError(f'Hugo {required} required, found {version.strip()}')
    env=os.environ.copy()
    revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if subprocess.check_output(['git','status','--porcelain'],text=True).strip():revision+='-dirty'
    env['HUGO_PARAMS_SOURCE_REVISION']=revision
    shutil.rmtree(PUBLIC,ignore_errors=True)
    subprocess.run([hugo,'--minify'] if minify else [hugo],check=True,env=env)
    index_key = os.environ.get("INDEXNOW_KEY", "")
    if index_key:
        if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", index_key): raise ValueError("Invalid public IndexNow key")
        (PUBLIC / (index_key + ".txt")).write_text(index_key + "\n")
    finish_outputs()
    subprocess.run([sys.executable,'scripts/social_cards.py'],check=True)
    subprocess.run([sys.executable,'scripts/verify.py'],check=True)
    print(f'Build verified; {count} substantive source pages. Revision {revision}')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--unminified',action='store_true');args=parser.parse_args()
    build(not args.unminified)
