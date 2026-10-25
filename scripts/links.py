#!/usr/bin/env python3
"""External link check for the content tree (standard library only).

The release gate (scripts/check.py) validates internal links; this script covers the external
sources the field guide and essays cite. It is run monthly by .github/workflows/links.yml and by hand
before an editorial review. Not a release gate: link rot is an editorial task, not a build failure.

Exit 1 when any link fails. `--report <path>` writes a Markdown report. Local DNS filters can block
live hosts; prefer the CI run or a public resolver when a result looks wrong.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "Mozilla/5.0 (compatible; janbrennenstuhl.eu link check; +https://www.janbrennenstuhl.eu/agents/)"
TIMEOUT = 20
# Hosts that answer automated requests with 403/429 regardless of the link's health.
SKIP_HOSTS = {"www.linkedin.com", "linkedin.com", "x.com", "twitter.com"}
URL = re.compile(r"""https?://[^\s<>()"'\]\[]+""")
TRAIL = ".,;:!?)'\"`"


def links() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for path in list((ROOT / "content").rglob("*.md")) + list((ROOT / "data").glob("*.toml")):
        text = path.read_text(errors="replace")
        for raw in URL.findall(text):
            url = raw.rstrip(TRAIL)
            host = url.split("/", 3)[2]
            if host.endswith(("janbrennenstuhl.eu", ".example", "example.com", "example.org", "example.net")) or "{" in url:
                continue  # own host, RFC 2606 documentation hosts, or a placeholder such as https://{identity-provider}/
            found.setdefault(url, set()).add(path.relative_to(ROOT).as_posix())
    return found


def fetch(url: str) -> tuple[str, int | str]:
    host = url.split("/", 3)[2]
    if host in SKIP_HOSTS:
        return url, "skipped"
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                return url, response.status
        except urllib.error.HTTPError as error:
            if method == "HEAD" and error.code in (403, 405, 404, 500, 501):
                continue
            return url, error.code
        except Exception as error:  # noqa: BLE001 - any transport failure is a finding
            if method == "HEAD":
                continue
            return url, type(error).__name__
    return url, "unreachable"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    found = links()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = dict(pool.map(fetch, sorted(found)))
    # 401/403 are almost always bot walls (Stack Exchange, Unsplash); listed, but not counted as rot.
    blocked = {u: r for u, r in results.items() if r in (401, 403)}
    failed = {u: r for u, r in results.items() if not (r == "skipped" or u in blocked or (isinstance(r, int) and r < 400))}
    lines = [f"# External links: {len(found)} checked, {len(failed)} failed, {len(blocked)} blocked for bots", ""]
    for title, group in (("## Failed", failed), ("## Blocked for bots (check by hand)", blocked)):
        if group:
            lines.append(title)
        for url, result in sorted(group.items()):
            lines.append(f"- `{result}` {url}")
            for source in sorted(found[url]):
                lines.append(f"  - {source}")
        lines.append("")
    report = "\n".join(lines) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report)
    print(report)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
