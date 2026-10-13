# Enhancement implementation — 13 October 2026

Based on the modernization review of commit `bc528e7905f6cb3fef08169d85774754b697fb7f`. This branch implements the core repository changes. It has not changed the live Bunny configuration or published the site.

## What changed

| Plan area | Implementation |
| --- | --- |
| Foundation | Owned Hugo templates; no Stack/Go dependency; exact Hugo version and verified Linux binary; pinned Python and browser dependencies; bootstrap and verification commands; portable agent-skill symlink |
| Release safety | Separate build/browser/publish jobs; main-push-only credentials and uploader guard; immutable artifact handoff; checksums; serialized deployment; assets first; prior assets retained; optional changed-only IndexNow |
| Metadata | Serialized JSON-LD with correct page types, absolute images, language and offset-aware dates; self-canonical pagination; no build timestamp masquerading as review date; refreshed security contact |
| Content | Stable IDs and explicit kinds/topics/status on the existing 42 substantive pages; source bodies preserved; one case-sensitive broken hero path fixed; credits retained; research clearly labeled |
| Agent access | Resolved per-page Markdown; heading/citation IDs; versioned catalog; source revision, author, license, freshness and hashes; discovery links; no raw shortcode leakage |
| Reading | Editorial type/spacing, compact navigation, two themes, keyboard theme selection, TOC, anchor links, copy actions, responsive images, local table/code overflow, print styles, substantive no-JS HTML |
| Discovery | Homepage composition, selected essay, writing index, topic hubs, all-content search with type/topic filters and section links, URL/history support, projects and speaking pages, useful 404, visible RSS |
| Visuals | Original delegation artwork used on the homepage and flagship article; deterministic title-based social cards; no runtime font fetches or third-party scripts |
| Maintenance | Architecture/content/release contracts, route/anchor fixtures, semantic and cross-format tests, browser/axe suite, budget checks, non-destructive image conversion |

The existing Plausible scripts and remote font loading were removed. The privacy page now accurately describes local theme storage and query URLs instead of claiming nothing is stored in the browser. Existing privacy-page anchors were preserved. No historical article’s technical review date was artificially advanced.

## Verification evidence

- Production **and unminified** pipelines pass.
- All **147 original HTML routes**, including aliases and pagination, remain present; all captured article/guide heading anchors remain.
- **160 HTML routes** validated after additions, with working local link/fragment targets, nonempty titles, a single h1 and valid structured data.
- **45 content entries** share consistent HTML/Markdown/catalog metadata: 35 essays, 7 research entries, author profile, one project and one talk. Search uses the same set; no drafts appear.
- Conversion tests preserve quotation attribution, absolute links, stable headings and other IDs, code fences/content, tables, figure descriptions, captions and expanded details. Existing code/link fidelity is checked across the corpus.
- Four focused unit tests cover conversion fidelity, ordered upload, Markdown MIME and changed-only IndexNow selection.
- **30 browser combinations** (home, long article, guide, search, topic × 360/768/1440px × light/dark) pass axe WCAG A/AA rules with **zero findings** and no page-wide overflow.
- Additional browser checks pass: skip-link focus, pagination neighbors, theme persistence/system reset, legacy search query parameter, empty results/history navigation, no-JS article and archive access, 320px reflow, increased text spacing, and HTTP 404.
- Screenshots were inspected for actual mobile/desktop home, article and guide layouts. The article’s large white project-logo hero was replaced by the coherent delegation illustration.
- Shared assets: **4,455 B CSS + 740 B JavaScript gzip**. No runtime fonts. Search adds **1,295 B script + 133,002 B index gzip**, only on a search request.
- The deployment dry run has zero deletes. Bootstrap was exercised from scratch; source/byte checks pass. Actual Forgejo runners and authenticated Bunny writes have not been exercised here.

## Local performance measurements

Lighthouse **12.8.2**, headless Chromium **138**, default simulated mobile profile; three successful runs per route. Served locally without HTTP compression. These are diagnostic lab results, not live CWV or an INP measurement. One interrupted request during a concurrent rebuild was discarded and rerun.

| Route | Median performance score | Median LCP | Median CLS | Median TBT |
| --- | ---: | ---: | ---: | ---: |
| Home | 100 | 1.05 s | 0.0053 | 0 ms |
| Article | 100 | 1.15 s | 0.0053 | 0 ms |
| Guide | 100 | 1.50 s | 0.0053 | 0 ms |

All three representative routes meet the ≥95 lab target. The guide is approximately at the 1.5-second stretch LCP target; field performance remains unverified. The full numerical runs are in `docs/measurements.json`. Nothing here claims p75 user performance or WCAG conformance.

## Search decision

A separate **Pagefind 1.3.0** prototype indexed the same 45 article bodies (4,110 words). The default UI was not included. Cold searches fetched the core/WASM/index plus the first five result records:

| Query | Pagefind gzip-equivalent bytes | Requests |
| --- | ---: | ---: |
| password | 140,801 | 10 |
| agent identity | 175,373 | 11 |
| CodeQL | 142,140 | 10 |
| OIDC | 137,596 | 10 |
| strength meter | 176,375 | 10 |

The implemented search costs about **134.3 kB gzip** for its script and full index on the first query, then needs no further network requests. At this corpus size it is simpler and smaller for the tested cold journeys, while delivering section links and type/topic filters. The prototype is version-specific, not a claim about the latest Pagefind or all future workloads. Revisit chunking/stemming when the corpus grows or measured search quality warrants it. Local benchmark timings are not user-network performance measurements.

## Remaining release work

1. **Bunny configuration:** apply browser/edge cache separation, MIME, compression/validators and staged CSP; verify real redirect and 404 behavior. The repository includes a concrete policy and live smoke command, not a fictitious `_headers` solution.
2. **Hosted delivery:** run the new Forgejo workflow against a staging zone, inspect artifact handoff, perform a real rollback rehearsal and then release the reviewed branch. Credentials were not available in this implementation session.
3. **Human accessibility review:** VoiceOver/Safari and NVDA/Firefox (or Chrome), touch-device review and user design approval remain. Zero axe findings do not establish WCAG conformance.
4. **Field performance:** deployed mobile/desktop p75 LCP, INP and CLS need real traffic. Local lab results cannot establish those targets.
5. **Ongoing editorial work:** review old security guidance individually; add exact research prerequisites/review dates only after that review. Further bespoke diagram families and opt-in explainers are the plan’s ongoing phase, not automatically generated technical claims.

Comments, accounts, newsletter infrastructure, service workers and an answer chatbot remain deferred as the plan specifies.
