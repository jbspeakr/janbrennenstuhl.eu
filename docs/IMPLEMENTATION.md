# Implementation notes: phases 1–4

Implements phases 1–4 of the modernization plan (13 October 2026) on the `modernize` branch, on top of the redesign's templates and release workflow. Nothing has been deployed and no live Bunny setting has been changed.

## Phase 1: own the foundation

- **Hugo only.** The Python build (`build.py`, `social_cards.py`, `verify.py`, the bs4/markdownify/Pillow venv) and the committed DejaVu fonts are gone. Markdown twins, catalog, findings, search index, feeds, `llms.txt`, `llms-full.txt`, redirects and social cards are Hugo output formats and image filters. Hugo pinned to 0.168.0 with a verified Linux checksum.
- **Release gates** in `scripts/check.py` (stdlib only): all 147 baseline routes and their heading anchors; one `h1`, description, canonical, `lang`, alt text and no skipped heading levels on every page; JSON-LD structure and dates; internal links, `srcset` and fragments; HTML/Markdown/catalog parity; agent files resolve; findings anchors resolve; feeds parse; redirects land; inline-script CSP hashes are documented; no build-machine paths leak; budgets. Hugo itself fails the build on broken `ref`s, missing image alt text and broken bundle links.
- **Derived front matter.** `kind` from the section, `id` from the bundle path (existing IDs kept), `topics` from tags through `data/topics.toml`, review status from `reviewed`. Categories and tags collapsed into six topics; the old category, tag and pagination routes redirect (96 in `/redirects.json`).
- **Render hooks** for headings, links (external marked, bundle files resolved), images (AVIF + WebP `srcset` at 480/960/1440, explicit dimensions), tables (focusable scroll region) and code blocks (filename, highlighted lines, copy).
- **Delivery:** three-job workflow kept, plus an opt-in staging preview for same-repo PRs with separate credentials. Bunny cache, MIME, 301, CSP, negotiation and MCP settings are written down in `docs/DELIVERY.md`.

## Phase 2: Trust Boundaries

- Dark-first OKLCH tokens with an equal light theme, Geist and Geist Mono self-hosted with metric-matched fallback, nothing under 13px. Contrast for every text pair is in `docs/DESIGN.md`.
- The generated flow drawing for every page: composition and hue from a hash of the page's identity, no labels, inline and theme-aware; the highlighted path draws in once, static under reduced motion; carries across navigation with view transitions.
- New home (statement, flagship, Now strip, recent essays, topic rows), article template (diagram header, key findings, sticky TOC with reading progress, series navigator, cite block), field-guide entry template, topic hubs, writing, Now, talks with a speaker bio, accessibility statement, 404 with search.
- ⌘K / Ctrl+K command palette, light/dark theme toggle, speculation rules, print styles.
- Social cards rendered by Hugo from per-topic diagram plates.

**Not done:** the plan's mock-first step. I built the design directly and reviewed screenshots at 360 and 1440px in both themes; your sign-off on the actual pages replaces the mocks. No headshot exists in the repository, so the speaker block shows one only when `params.headshot` is set. Sidenotes were not built: no current article uses footnotes.

## Phase 3: agents and the field guide

- `llms.txt` (every entry with a one-sentence claim and its Markdown link), `llms-full.txt`, Markdown twins for every page and section, `Accept: text/markdown` negotiation (edge script plus local server), `catalog.json` with topics and content hashes, `findings.json`, JSON Feed and RSS per site, topic and field guide (the latter ordered by last change, with the change note), Scholar citation tags, JSON-LD with `about`, `isPartOf`, `citation`, `license`, breadcrumbs and a `DefinedTermSet` for the glossary, RFC 9727 `api-catalog`, `robots.txt` and `tdmrep.json` (no reservation; CC BY 4.0 covers training, see docs/DECISIONS.md), an `/agents/` policy page.
- Field guide: all seven existing entries rewritten as question-led entries with 30 sourced findings and evidence tables; the three draft stubs removed; a new **Agent identity** area with four entries (17 findings, MCP revision 2026-07-28); two new entries, "What is inside a JWT?" and "What should a password policy require?" (NIST SP 800-63B-4); a 62-term glossary whose acronyms link and expand on first use.
- Claims for all 37 essays, talks and projects; three key findings on each of the five 2026 essays. 70 findings in total, each with an anchor, "copy quote with link" and a 1200×630 share card.

Corrections made while rewriting (worth your review): a dead Google-hosted PDF replaced with the USENIX copy; "up to 105 guesses" corrected to 10^5 for zxcvbn; the Egelman et al. summary aligned with its abstract; the University of Illinois added to the Tangled Web affiliations; the `readme-1` description replaced (it described a different post).

**Unverified and flagged:** the quotation "We recommend a 1c12+NN10 minimum-strength policy…" on the strength-meter entry is kept from the old page; the full text was not reachable to confirm it. The years of the two Microsoft Research reports are shown as n/a.

## Phase 4: ongoing

- Three explainers, each loaded only on its page and readable without JavaScript: a JWT decoder (local only, flags `alg: none`, expiry, missing audience), a password-policy checker against SP 800-63B-4, and a stepper through the RFC 8693 exchange.
- A read-only MCP server (`edge/mcp/`) for Bunny Edge Scripting with `search_site`, `get_entry`, `get_findings` and `list_topics`, speaking MCP 2026-07-28 statelessly and the 2025-era `initialize` handshake. Not deployed.
- Newsletter and webmentions are skipped by decision; the footer offers RSS, JSON Feed, Mastodon and the field-guide change feed.

**Not done:** the plain-language summary toggle (needs written summaries), Markdown lint and a spell check with a security dictionary (structural checks are covered by `check.py`; a spell check needs a curated dictionary pass over the old posts).

## Evidence (local, 14 October 2026)

- `scripts/check.py`: 171 HTML files, 52 catalog entries, 70 findings, 96 redirects, all gates pass. Compressed CSS 7.6 kB, article JS 1.4 kB, preloaded font 26.4 kB, essay HTML around 12 kB.
- `npm run test:browser`: 42 page × width × theme combinations (home, essay, field guide, explainer, search, topic, glossary at 360/768/1440 in light and dark) with zero axe WCAG 2.2 A/AA violations and no horizontal overflow; skip link, palette keyboard use and its own axe check, theme toggle persistence, search history, the three explainers, 320px reflow, text spacing, 404 status, old-route redirect, no-JS reading and search, Markdown negotiation.
- `npm run test:lighthouse` (Lighthouse 13.5.0, simulated mobile, gzip, median of 3): performance, accessibility, best practices and SEO 100 on home, essay and field-guide entry; CLS 0; TBT 0; LCP 1.35–1.5 s (target 1.2 s; see the CSP trade-off in `docs/DESIGN.md`).
- `npm run test:edge`: 10 MCP and negotiation tests. `python3 -m unittest`: release ordering, IndexNow and MIME tests.

## Still open before release

1. Your design and content review, including the rewritten field-guide entries (none carries a review date) and the corrections above.
2. A manual screen-reader pass with VoiceOver/Safari and NVDA/Firefox; the accessibility statement says this is pending.
3. Bunny configuration from `docs/DELIVERY.md`: zone settings by hand, edge rules (cache, MIME, 301s, CSP report-only, negotiation) synced by `scripts/edge_rules.py`, rehearsed on staging with the live smoke test and a rollback.
4. Deploying the MCP edge script and adding it to the api-catalog, if you want it live.

Resolved on 15 October 2026 (see `docs/DECISIONS.md` and `docs/LAUNCH.md`): CC BY 4.0 governs training, so the TDM reservation is gone; Plausible is back as the one allowed third-party script; no newsletter, webmentions or external monitoring; Bunny configuration as code and a CSP collector are deferred. Added: `scripts/review-queue.py` (editorial queue), `scripts/links.py` with a monthly `links` workflow, `scripts/bump-hugo.sh` and `renovate.json`, a search-index budget, screenshot artifacts from the browser job, and the HTW lecture as a talk.
