# Content contract

Hugo is the only build tool. Every published representation (HTML, Markdown twin, feeds, catalog, findings, search index, `llms.txt`, `llms-full.txt`, social card) is generated from the same source in one build.

## What an author writes

```yaml
---
title: "An exact and useful title"
description: "One plain sentence for search results, feeds and llms.txt."
date: 2026-10-13
tags: ["oidc", "passkeys"]
slug: a-short-keyword-slug         # posts, pages and field-guide entries
---
```

Slugs are short and keyword-led: two or three words, no `howto`, `what-is` or filler. Renaming a published slug keeps the old URL as a front-matter alias (`aliases: ["/old-slug/"]`), which becomes a 301 in `/redirects.json`; never drop an alias. Heading anchors must survive the rename, `scripts/check.py` follows the alias to verify them.

Optional:

| Field | Meaning |
| --- | --- |
| `lead` | A longer opening shown under the title; defaults to `description`. |
| `claim` | One quotable sentence stating the main point; used in `llms.txt`, feeds and the catalog. |
| `findings` | Up to three key findings for essays: `[{id, text}]`. Each gets the anchor `#f-<id>`. IDs are permanent and unique site-wide. |
| `series` | A series ID from `data/series.toml`; adds the series navigator. |
| `topics` | Overrides the topics derived from tags (see `data/topics.toml`). |
| `lastmod` | A meaningful content change. Not a rebuild, not a metadata tweak. |
| `reviewed` | Date of an actual editorial review of the advice after publication. Never set it without a review. Essays, talks and projects count as reviewed on publication (`review_basis: publication`, dated to the publish date); a later `reviewed` replaces that (`review_basis: editorial`). Field-guide entries stay `not-reviewed` until one is set. |
| `status` | `archived` or `superseded` (with `supersededBy`); default `published`. |
| `image`, `imageAlt` | Shown only when informative (`imageAlt` set and not `imageDecorative`). Every article gets the generated diagram anyway. |
| `scripts` | Interactive explainers to load, e.g. `[jwt]` for `assets/js/explainers/jwt.js`. |
| `license: false` | No CC BY grant for this page. |

Derived, never written by hand: `kind` from the section (`post` → essay, `knowledge-base` → guide, `projects` → project, `talks` → talk), `id` from the bundle path (`post/x` → `jb-x`, `knowledge-base/a/b` → `jb-knowledge-base-a-b`) unless an `id` is already assigned, `topics` from tags, review status and basis from `reviewed` and the kind. **Existing `id` values are permanent**; never change one because a title or slug changed.

## Field-guide entries

Under `content/knowledge-base/<area>/<entry>/index.md`. One question per entry:

- `title` is the question; `linkTitle` the short label; `answer` two sentences quotable on their own.
- Body order: `## Key findings` (3–5 `finding` shortcodes, each with a source), `## Evidence` (`studies`/`study` table), `## What to do` (`### For engineers`, `### For product and UX`), details, related.
- Record each meaningful revision in `changes: [{date, note}]`; it feeds the field guide's change feeds.
- Numbers must come from the cited source. If a value is not in the source, write `n/a`.

## Review cadence

Decided in `docs/DECISIONS.md`. Field-guide entries are reviewed at least every twelve months; essays on fast-moving topics (`fastMovingTopics` in `config/_default/params.toml`) show the older-guidance notice five years after `date` or the last `reviewed`. `python3 scripts/review-queue.py` lists what is due, oldest first. A review means reading the entry against current sources, fixing what changed, then setting `reviewed:` to that day and adding a `changes` line for field-guide entries. `lastmod` moves only when the content changed. External sources are checked monthly by `scripts/links.py` (CI workflow `links`); replace a dead source with an archived copy or a DOI rather than dropping the claim.

## Shortcodes

Each shortcode has an HTML template and a Markdown variant (`layouts/_partials/md/<name>.md`, used by the Markdown twin and `llms-full.txt`). A new shortcode needs both, plus a `.llmsfull.txt` wrapper.

| Shortcode | Purpose |
| --- | --- |
| `finding id= source= url=` | A quotable claim with a permanent anchor `#f-<id>`; collected into `/findings.json`. |
| `studies caption=` / `study title= org= year= sample= method= url=` | Evidence table; study URLs become `citation` in JSON-LD. |
| `pullquote id=` | Large quote with "copy quote with link" and anchor `#q-<id>`. |
| `callout title=` | Aside. |
| `term "<glossary id>"` | Link to a glossary term with its expansion. |
| `explainer "<name>" "<heading>"` | Interactive explainer; the inner Markdown is the static explanation and must stand on its own. |
| `figure-diagram src= alt= caption=` | Inline SVG figure with a "What this shows" prose description. Never decorative. |
| `quote`, `details`, `youtube` | Existing components. |
| `glossary` | Renders `data/glossary.toml` (glossary page only). |

Internal links use `ref` (`{{</* ref "/post/jwks" */>}}`); a missing target fails the build. Images need alt text (or the title `"decorative"`); a missing alt fails the build.

## Glossary and topics

- `data/glossary.toml`: terms with optional `abbr`, `expansion`, `see`. Terms with `autolink = true` are linked and expanded on their first plain-paragraph use in essays and guides. Only unambiguous acronyms get `autolink`.
- `data/topics.toml`: the six topics, their human descriptions (these feed `llms.txt` and topic feeds) and the tags that map to them.
- `data/redirects.toml`: retired routes and their targets.

## Machine-readable outputs

| Output | Source |
| --- | --- |
| `<url>index.md` | `page.markdown.md`: YAML front matter (id, title, dates, review status, topics, license, canonical URL) and the body with shortcodes rendered as Markdown, absolute links and `<a id>` anchors matching the HTML heading IDs. |
| `/catalog.json` | Every entry's metadata, sections and a `content_hash` (SHA-256 of title, description, last modified date and source). The hash detects changes; it is not a signature. |
| `/findings.json` | Every finding with its URL, source, entry and review status. |
| `/llms.txt`, `/llms-full.txt` | Orientation with claims and twin links; the full corpus. |
| `/feed.json`, `/index.xml` and per topic / field guide | Full-content JSON Feed 1.1 and RSS. |
| `/search/index.json` | Search page and command palette. |

`scripts/check.py` enforces parity between HTML, Markdown and the catalog, that every advertised link resolves, and that no shortcode syntax leaks.
