#!/usr/bin/env python3
"""Editorial review queue (docs/CONTENT-CONTRACT.md, "Review cadence").

Lists, oldest first, the pages whose advice is due for a review:
  - field-guide entries never reviewed, or reviewed more than REVIEW_DAYS ago;
  - essays on fast-moving topics (config/_default/params.toml) within WARN_YEARS of the
    "older guidance" notice, or already showing it, unless reviewed more recently.
Reads only front matter; needs nothing but the standard library. Exit 0 always: this is a to-do list,
not a gate. `--json` prints machine-readable rows.
"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_DAYS = 365
WARN_YEARS = 1


def front_matter(path: Path) -> dict:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm: dict = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if km:
            fm[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return fm


def to_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def topics_of(fm: dict, mapping: dict) -> set[str]:
    raw = fm.get("topics") or ""
    if raw:
        return {t.strip().strip('"') for t in raw.strip("[]").split(",") if t.strip()}
    tags = [t.strip().strip('"') for t in (fm.get("tags") or "").strip("[]").split(",") if t.strip()]
    return {mapping[t] for t in tags if t in mapping}


def main() -> int:
    params = tomllib.loads((ROOT / "config/_default/params.toml").read_text())
    fast = set(params.get("fastMovingTopics", []))
    outdated_after = int(params.get("outdatedAfterYears", 5))
    topics = tomllib.loads((ROOT / "data/topics.toml").read_text())
    tag_map = {tag: topic["id"] for topic in topics.get("topic", []) for tag in topic.get("tags", [])}
    today = date.today()
    rows = []
    for path in sorted((ROOT / "content").rglob("index.md")):
        fm = front_matter(path)
        if fm.get("draft") == "true":
            continue
        rel = path.relative_to(ROOT / "content").parent.as_posix()
        reviewed = to_date(fm.get("reviewed"))
        published = to_date(fm.get("date"))
        if rel.startswith("knowledge-base/"):
            if reviewed is None:
                rows.append({"page": rel, "kind": "guide", "reason": "never reviewed", "since": fm.get("date", "")})
            elif (today - reviewed).days > REVIEW_DAYS:
                rows.append({"page": rel, "kind": "guide", "reason": f"reviewed {(today - reviewed).days} days ago", "since": str(reviewed)})
        elif rel.startswith("post/") and published:
            if not (topics_of(fm, tag_map) & fast):
                continue
            anchor = reviewed or published
            age_years = (today - anchor).days / 365.25
            if age_years >= outdated_after:
                rows.append({"page": rel, "kind": "essay", "reason": "shows the older-guidance notice", "since": str(anchor)})
            elif age_years >= outdated_after - WARN_YEARS:
                rows.append({"page": rel, "kind": "essay", "reason": f"notice in {int((outdated_after - age_years) * 12)} months", "since": str(anchor)})
    rows.sort(key=lambda r: r["since"])
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=2))
        return 0
    if not rows:
        print("Nothing due for review.")
        return 0
    width = max(len(r["page"]) for r in rows)
    for r in rows:
        print(f"{r['page']:<{width}}  {r['kind']:<5}  {r['since']:<10}  {r['reason']}")
    print(f"\n{len(rows)} page(s) due. Review, then set `reviewed:` (and `changes` for field-guide entries).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
