#!/usr/bin/env python3
"""Static release gates for the built site in public/. Standard library only.

Fails (exit 1) on: lost baseline routes or heading anchors, broken internal links or fragments,
pages without exactly one h1, a description, a canonical URL or alt text, skipped heading levels,
invalid structured data, Markdown twins that drift from the HTML, agent files that point nowhere,
broken feeds or redirects, draft leakage, and budget overruns.
"""
from __future__ import annotations

import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SITE = "https://www.janbrennenstuhl.eu"
HOST = "www.janbrennenstuhl.eu"

# Compressed budgets in bytes (docs/DESIGN.md).
BUDGET = {"css": 15_000, "js_article": 8_000, "html_article": 30_000, "font_preload": 35_000, "diagram": 6_000, "search_index": 200_000}
# The only third-party script allowed on any page (docs/DECISIONS.md): Plausible analytics.
ALLOWED_SCRIPT_HOSTS = {"plausible.io"}

errors: list[str] = []
warnings: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        errors.append(message)


def gz(data: bytes) -> int:
    return len(gzip.compress(data, compresslevel=9, mtime=0))


class Page(HTMLParser):
    """Collects what the gates need from one HTML document."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.ids: list[str] = []
        self.headings: list[tuple[int, str]] = []
        self.body_ids: list[str] = []
        self.body_links: list[tuple[str, str]] = []
        self.scripts: dict[str, list[str]] = {}
        self.svg_sizes: list[int] = []
        self.title = ""
        self.lang = ""
        self._script_type: str | None = None
        self._script_id = ""
        self._buffer: list[str] = []
        self._in_title = False
        self._body_depth = 0
        self._main = False
        self._svg_start: int | None = None
        self._raw = ""

    def feed_document(self, raw: str) -> "Page":
        self._raw = raw
        self.feed(raw)
        return self

    def handle_starttag(self, tag: str, attrs_list) -> None:
        attrs = {k: (v or "") for k, v in attrs_list}
        self.tags.append((tag, attrs))
        if tag == "html":
            self.lang = attrs.get("lang", "")
        if "id" in attrs:
            self.ids.append(attrs["id"])
            if self._body_depth:
                self.body_ids.append(attrs["id"])
        if tag == "main":
            self._main = True
        if re.fullmatch(r"h[1-6]", tag) and self._main:
            self.headings.append((int(tag[1]), attrs.get("id", "")))
        if tag == "div":
            if self._body_depth:
                self._body_depth += 1
            elif "data-article-body" in attrs:
                self._body_depth = 1
        if tag == "a" and self._body_depth and "href" in attrs:
            self.body_links.append((attrs["href"], attrs.get("class", "")))
        if tag == "script":
            self._script_type = attrs.get("type", "text/javascript")
            self._script_id = attrs.get("id", "")
            self._buffer = []
        if tag == "title":
            self._in_title = True
        if tag == "svg" and "diagram" in attrs.get("class", "") and self._svg_start is None:
            self._svg_start = self._offset()

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self._body_depth:
            self._body_depth -= 1
        if tag == "script" and self._script_type is not None:
            key = self._script_id or self._script_type
            self.scripts.setdefault(key, []).append("".join(self._buffer))
            self._script_type = None
        if tag == "title":
            self._in_title = False
        if tag == "main":
            self._main = False
        if tag == "svg" and self._svg_start is not None:
            end = self._raw.find("</svg>", self._svg_start)
            self.svg_sizes.append(gz(self._raw[self._svg_start:end + 6].encode()))
            self._svg_start = None

    def handle_data(self, data: str) -> None:
        if self._script_type is not None:
            self._buffer.append(data)
        if self._in_title:
            self.title += data

    def _offset(self) -> int:
        line, col = self.getpos()
        lines = self._raw.split("\n")
        return sum(len(x) + 1 for x in lines[: line - 1]) + col

    def find(self, tag: str, **want: str) -> list[dict[str, str]]:
        out = []
        for name, attrs in self.tags:
            if name == tag and all(want_value in attrs.get(k, "").split() if k in ("rel", "class") else attrs.get(k) == want_value for k, want_value in want.items()):
                out.append(attrs)
        return out


def route_of(path: Path) -> str:
    rel = path.relative_to(PUBLIC).as_posix()
    return "/" + rel.removesuffix("index.html")


def target_of(url: str) -> Path:
    path = unquote(urlsplit(url).path).lstrip("/")
    target = PUBLIC / path
    if target.is_file():
        return target
    if urlsplit(url).path.endswith("/") or not target.suffix:
        target = target / "index.html"
    return target


def local(url: str) -> bool:
    return urlsplit(url).netloc in ("", HOST)


# --- Parse every HTML document once -------------------------------------------------------------
pages: dict[Path, Page] = {}
raw_html: dict[Path, bytes] = {}
for path in sorted(PUBLIC.rglob("*.html")):
    data = path.read_bytes()
    raw_html[path] = data
    pages[path] = Page().feed_document(data.decode("utf-8"))


def is_redirect(page: Page) -> bool:
    return any(attrs.get("http-equiv", "").lower() == "refresh" for attrs in page.find("meta"))


def redirect_target(page: Page) -> str:
    refresh = next(a for a in page.find("meta") if a.get("http-equiv", "").lower() == "refresh")
    return refresh.get("content", "").split("url=", 1)[-1]


# --- Baseline routes and heading anchors ---------------------------------------------------------
baseline = json.loads((ROOT / "tests/fixtures/baseline-routes.json").read_text())
for route, old in baseline.items():
    path = PUBLIC / route.lstrip("/")
    check(path in pages, f"Lost route {route}")
    if path in pages and old["headings"]:
        # A renamed page keeps its old route as a 301 (front-matter alias); fragments survive the
        # redirect, so the anchors must exist on the page it points to.
        if is_redirect(pages[path]):
            path = target_of(redirect_target(pages[path]))
            check(path in pages and not is_redirect(pages[path]), f"Route with headings must redirect to a page: {route}")
            if path not in pages:
                continue
        ids = set(pages[path].ids)
        for heading in old["headings"]:
            check(heading in ids, f"Lost heading anchor {route}#{heading}")

# --- Per-page semantics, structured data, links ---------------------------------------------------
article_types = {"BlogPosting", "TechArticle", "Article"}
for path, page in pages.items():
    route = route_of(path)
    if is_redirect(page):
        dest = redirect_target(page)
        if local(dest):
            check(target_of(dest).exists(), f"Redirect {route} points to missing {dest}")
        continue
    check(bool(page.title.strip()), f"Empty <title> {route}")
    check(page.lang == "en-GB", f"Missing lang {route}")
    check(len([h for h in page.headings if h[0] == 1]) == 1, f"Expected exactly one h1 {route}")
    previous = 1
    for level, hid in page.headings:
        check(level <= previous + 1, f"Skipped heading level h{previous}->h{level} at #{hid} {route}")
        previous = level
    check(bool(page.find("main")), f"Missing <main> {route}")
    desc = page.find("meta", name="description")
    check(bool(desc) and bool(desc[0].get("content", "").strip()), f"Missing description {route}")
    canonical = page.find("link", rel="canonical")
    check(bool(canonical), f"Missing canonical {route}")
    if canonical and path.name == "index.html":
        check(urlsplit(canonical[0]["href"]).path == route, f"Canonical mismatch {route}: {canonical[0]['href']}")
    for img in page.find("img"):
        check("alt" in img, f"Image without alt {route}: {img.get('src')}")
    for script in page.find("script"):
        check(not script.get("src", "").startswith(("http:", "https:", "//")), f"Third-party script {route}")
    for body in page.find("body"):  # the analytics loader in site.js reads this attribute after the load event
        analytics = body.get("data-analytics", "")
        check(not analytics or urlsplit(analytics).hostname in ALLOWED_SCRIPT_HOSTS, f"Analytics host not allowed {route}: {analytics}")
    for link in page.find("link", rel="stylesheet"):
        check(not link.get("href", "").startswith(("http:", "https:", "//")), f"Third-party stylesheet {route}")
    check(len(page.ids) == len(set(page.ids)), f"Duplicate IDs {route}: {sorted({i for i in page.ids if page.ids.count(i) > 1})}")
    for size in page.svg_sizes:
        check(size <= BUDGET["diagram"], f"Diagram budget {route}: {size} B")

    for block in page.scripts.get("application/ld+json", []):
        try:
            data = json.loads(block)
            check(data.get("@context") == "https://schema.org", f"JSON-LD context {route}")
            graph = data.get("@graph", [])
            check(bool(graph), f"JSON-LD without @graph {route}")
            for entity in graph:
                check("@type" in entity, f"JSON-LD entity without @type {route}")
                check("@context" not in entity, f"Nested JSON-LD @context {route}")
                if "inLanguage" in entity:
                    check(entity["inLanguage"] == "en-GB", f"JSON-LD language {route}")
                for key in ("datePublished", "dateModified"):
                    if key in entity:
                        check(datetime.fromisoformat(entity[key]).tzinfo is not None, f"Naive {key} {route}")
                if "image" in entity:
                    check(str(entity["image"]).startswith("https://"), f"Relative JSON-LD image {route}")
                    check(target_of(entity["image"]).exists() or Path(PUBLIC / urlsplit(entity["image"]).path.lstrip("/")).exists(), f"JSON-LD image missing {route}")
                if entity.get("@type") in article_types:
                    for key in ("headline", "datePublished", "dateModified", "author", "url"):
                        check(key in entity, f"{entity['@type']} without {key} {route}")
                if entity.get("@type") == "BreadcrumbList":
                    positions = [i.get("position") for i in entity.get("itemListElement", [])]
                    check(positions == list(range(1, len(positions) + 1)), f"Breadcrumb positions {route}")
        except (ValueError, TypeError) as exc:
            errors.append(f"Invalid JSON-LD {route}: {exc}")

    og = page.find("meta", property="og:image")
    if og:
        check(target_of(og[0]["content"]).exists() or (PUBLIC / urlsplit(og[0]["content"]).path.lstrip("/")).exists(), f"Missing og:image file {route}")

    for tag, attrs in page.tags:
        for attr in ("href", "src"):
            raw = attrs.get(attr)
            if not raw or tag in ("a",) and raw.startswith(("mailto:", "tel:")) or raw.startswith("data:"):
                continue
            url = urljoin(SITE + route, raw)
            if not local(url):
                continue
            target = target_of(url)
            check(target.exists(), f"Broken internal link {route} -> {raw}")
            fragment = urlsplit(url).fragment
            if fragment and target in pages and not is_redirect(pages[target]):
                check(unquote(fragment) in set(pages[target].ids), f"Broken fragment {route} -> {raw}")
        if attrs.get("srcset"):
            for candidate in attrs["srcset"].split(","):
                src = candidate.strip().split()[0]
                check(target_of(urljoin(SITE + route, src)).exists(), f"Broken srcset {route} -> {src}")

# --- Catalog, Markdown twins, metadata parity ------------------------------------------------------
catalog = json.loads((PUBLIC / "catalog.json").read_text())
items = catalog["items"]
check(catalog.get("schema_version", "").startswith("1."), "Catalog schema version")
check(len({i["id"] for i in items}) == len(items), "Duplicate catalog IDs")
required = ("id", "title", "description", "canonical_url", "markdown_url", "kind", "topics", "published", "modified", "review_status", "status", "license", "content_hash")
for item in items:
    for key in required:
        check(key in item and item[key] not in (None, ""), f"Catalog {item.get('id')}: missing {key}")
    check(item["review_status"] != "reviewed" or bool(item.get("reviewed")), f"Catalog {item['id']}: reviewed without date")
    html_path = target_of(item["canonical_url"])
    md_path = PUBLIC / urlsplit(item["markdown_url"]).path.lstrip("/")
    check(html_path in pages, f"Catalog URL missing {item['id']}")
    check(md_path.exists(), f"Markdown twin missing {item['id']}")
    if html_path not in pages or not md_path.exists():
        continue
    page, md = pages[html_path], md_path.read_text()
    check(md.startswith("---\n") and "\n---\n" in md[4:], f"Markdown front matter {item['id']}")
    front = md.split("\n---\n", 1)[0]
    for key in ("id", "title", "canonical_url", "author", "published", "license"):
        check(re.search(rf"^{key}:", front, re.M) is not None, f"Markdown front matter lacks {key}: {item['id']}")
    check(f"id: {item['id']}" in front, f"Markdown id parity {item['id']}")
    for leak in ("{{<", "{{%", "HAHAHUGOSHORTCODE"):
        check(leak not in md, f"Unrendered shortcode in Markdown {item['id']}")
    meta = page.scripts.get("content-metadata")
    if meta:
        html_meta = json.loads(meta[0])
        for key in ("id", "title", "canonical_url", "published", "modified", "review_status", "topics", "content_hash"):
            check(html_meta.get(key) == item.get(key), f"HTML/catalog metadata parity {item['id']}: {key}")
    for hid in page.body_ids:
        if re.fullmatch(r"(f|q)-.+", hid) or any(hid == h for _, h in page.headings):
            check(f'<a id="{hid}"></a>' in md, f"Anchor missing from Markdown {item['id']}#{hid}")
    for href, cls in page.body_links:
        if any(c in cls.split() for c in ("heading-anchor", "term", "finding-id", "finding-card")):
            continue
        absolute = urljoin(item["canonical_url"], href)
        check(absolute in md or href in md, f"Link missing from Markdown {item['id']}: {href}")
    html_size = gz(raw_html[html_path])
    if item["kind"] in ("essay", "guide"):
        check(html_size <= BUDGET["html_article"], f"HTML budget {item['id']}: {html_size} B")

# Every page that advertises a Markdown twin must have one.
for path, page in pages.items():
    for alt in page.find("link", rel="alternate"):
        if alt.get("type") == "text/markdown":
            check((PUBLIC / urlsplit(alt["href"]).path.lstrip("/")).exists(), f"Advertised Markdown missing {route_of(path)}")

# --- Agent files -----------------------------------------------------------------------------------
llms = (PUBLIC / "llms.txt").read_text()
for url in re.findall(r"\]\((https://www\.janbrennenstuhl\.eu[^)\s]*)\)", llms):
    path = PUBLIC / urlsplit(url).path.lstrip("/")
    check(path.exists() or target_of(url).exists(), f"llms.txt link does not resolve: {url}")
full = (PUBLIC / "llms-full.txt").read_text()
for item in items:
    check(item["markdown_url"] in llms, f"llms.txt missing {item['id']}")
    check(item["canonical_url"] in full, f"llms-full.txt missing {item['id']}")
check("{{<" not in full and "HAHAHUGOSHORTCODE" not in full, "Unrendered shortcode in llms-full.txt")

findings = json.loads((PUBLIC / "findings.json").read_text())["items"]
check(len({f["id"] + f["article_url"] for f in findings}) == len(findings), "Duplicate finding IDs")
check(len({f["id"] for f in findings}) == len(findings), "Finding IDs must be unique site-wide")
for finding in findings:
    target = target_of(finding["url"])
    check(target in pages and unquote(urlsplit(finding["url"]).fragment) in set(pages[target].ids), f"Finding anchor does not resolve: {finding['url']}")
    check(bool(finding["text"].strip()), f"Empty finding {finding['id']}")

search = json.loads((PUBLIC / "search/index.json").read_text())
check({s["id"] for s in search} == {i["id"] for i in items}, "Search index and catalog cover different entries")

redirects = json.loads((PUBLIC / "redirects.json").read_text())["redirects"]
for r in redirects:
    source = target_of(r["from"])
    check(source in pages and is_redirect(pages[source]), f"Redirect page missing for {r['from']}")
    check(target_of(r["to"]).exists(), f"Redirect target missing {r['from']} -> {r['to']}")

for name in ("api-catalog", "tdmrep.json"):
    json.loads((PUBLIC / ".well-known" / name).read_text())
for href in re.findall(r'"href": "([^"]+)"', (PUBLIC / ".well-known/api-catalog").read_text()):
    check((PUBLIC / urlsplit(href).path.lstrip("/")).exists() or target_of(href).exists(), f"api-catalog link missing: {href}")

# --- Feeds -------------------------------------------------------------------------------------------
for path in PUBLIC.rglob("*.xml"):
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        errors.append(f"Invalid XML {path.relative_to(PUBLIC)}: {exc}")
for path in PUBLIC.rglob("feed.json"):
    feed = json.loads(path.read_text())
    check(feed.get("version") == "https://jsonfeed.org/version/1.1", f"JSON Feed version {path.relative_to(PUBLIC)}")
    for entry in feed.get("items", []):
        check(target_of(entry["url"]).exists(), f"JSON Feed item missing {entry['url']}")
        check(bool(entry.get("content_html")), f"JSON Feed item without content {entry['url']}")
rss = ET.parse(PUBLIC / "index.xml").getroot()
check(len(rss.findall("./channel/item")) == len(items), "Home RSS should carry every entry")
for desc in rss.iter("description"):
    check(' href="/' not in (desc.text or "") and ' src="/' not in (desc.text or ""), "Relative URL in RSS content")

# --- CSP: inline scripts and the hashes the edge allows must match exactly ---------------------------
import base64
import hashlib
import tomllib
script_src = tomllib.loads((ROOT / "edge/rules.toml").read_text())["csp"]["directives"]["script-src"].split()
inline_hashes = set()
for page in pages.values():
    for kind, blocks in page.scripts.items():
        if kind in ("text/javascript",):
            for block in blocks:
                if block.strip():
                    inline_hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(block.encode()).digest()).decode() + "'")
for digest in inline_hashes:
    check(digest in script_src, f"Inline script hash {digest} is not in script-src in edge/rules.toml")
for digest in (s for s in script_src if s.startswith("'sha256-")):
    check(digest in inline_hashes, f"Unused hash {digest} in script-src in edge/rules.toml; remove it")

# --- No build-machine details in the artifact -----------------------------------------------------
for path in PUBLIC.rglob("*"):
    if path.is_file() and path.suffix in (".html", ".json", ".md", ".txt", ".xml"):
        check(str(ROOT) not in path.read_text(errors="ignore"), f"Local path leaked into {path.relative_to(PUBLIC)}")

# --- Drafts, security.txt ---------------------------------------------------------------------------
titles = {i["title"] for i in items}
for path in (ROOT / "content").rglob("*.md"):
    text = path.read_text()
    match = re.search(r"^draft:\s*true\s*$", text.split("---", 2)[1] if text.startswith("---") else "", re.M)
    if match:
        title = re.search(r'^title:\s*"?(.*?)"?\s*$', text, re.M)
        check(not title or title.group(1) not in titles, f"Draft leaked: {path}")
expiry = re.search(r"^Expires: (.+)$", (PUBLIC / ".well-known/security.txt").read_text(), re.M)
days = (datetime.fromisoformat(expiry[1].replace("Z", "+00:00")) - datetime.now(timezone.utc)).days
check(days > 0, "security.txt expired")
if days < 60:
    warnings.append(f"security.txt expires in {days} days")

# --- Budgets ----------------------------------------------------------------------------------------
css = sum(gz(p.read_bytes()) for p in (PUBLIC / "css").glob("*.css"))
check(css <= BUDGET["css"], f"CSS budget: {css} B > {BUDGET['css']} B")
js_dir = PUBLIC / "js"
article_js = sum(gz(p.read_bytes()) for p in js_dir.glob("*.js") if p.name.startswith(("site.", "theme.")))
check(article_js <= BUDGET["js_article"], f"Article JS budget: {article_js} B > {BUDGET['js_article']} B")
font = (PUBLIC / "fonts/Geist-Variable-1.7.2.woff2").stat().st_size
check(font <= BUDGET["font_preload"], f"Preloaded font budget: {font} B")
search_index = gz((PUBLIC / "search/index.json").read_bytes())
check(search_index <= BUDGET["search_index"], f"Search index budget: {search_index} B > {BUDGET['search_index']} B")

print(f"Checked {len(pages)} HTML files, {len(items)} catalog entries, {len(findings)} findings, {len(redirects)} redirects.")
print(f"Compressed: CSS {css} B, article JS {article_js} B, preloaded font {font} B, search index {search_index} B.")
for warning in warnings:
    print("WARNING:", warning)
if errors:
    print(f"\n{len(errors)} problem(s):")
    print("\n".join(sorted(set(errors))))
    sys.exit(1)
print("All static release gates passed.")
