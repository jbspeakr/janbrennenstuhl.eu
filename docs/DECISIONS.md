# Decisions

Settled questions from the modernization review. Each entry says what was decided, why, and what it
rules out, so a later PR does not reopen it by accident. Dates are when the decision was taken.

## Licence and training (15 October 2026)

**CC BY 4.0 governs, including AI training.** The licence already permits reuse with attribution; a
text-and-data-mining reservation on top of it would contradict the grant. `robots.txt` allows every
crawler and carries no `Content-Signal` line: that directive is a Cloudflare proposal, not part of
RFC 9309, and SEO audits such as Semrush flag it as invalid (removed 3 November 2026; revisit if the
IETF aipref vocabulary is published); `/.well-known/tdmrep.json` declares `tdm-reservation: 0`;
`/agents/` explains that attribution is the condition. Rules out: per-crawler disallow lists, a
"ask first" training policy, licence exceptions per page except `license: false` for legal pages.

## Analytics (15 October 2026)

**Plausible stays, proxied through our own host (9 November 2026).** Ad blockers that list
`plausible.io` blocked the script and its beacon, so the www pull zone now maps the neutral paths `/r/s.js` and
`/r/e.json` to the Plausible script and event API with Change Origin URL edge rules (`[[proxy]]` in
`edge/rules.toml`, the same setup as urbanartcore.com and rucksackrebellen.de; 11 November 2026), and the site makes no third-party request. `assets/js/theme.js` carries
the queue stub, with `endpoint: '/r/e.json'`, inside the already-hashed inline script, `baseof.html` puts the script URL on `<body>`
only when the build's base URL is the production host, `site.js` injects it after the load event so
it never competes with content (a plain `async` tag cost one simulated round trip of LCP in the
Lighthouse gate), and `scripts/check.py` requires a same-origin `/r/` path. The CSP needs only
`'self'`. Rules out:
inline analytics snippets, self-hosted Plausible or Umami, a web-vitals beacon.

## Newsletter and webmentions (14 October 2026)

**Neither.** RSS, JSON Feed, the field-guide change feed and Mastodon are the distribution channels.
A newsletter adds a provider, a privacy page and a backlog; webmentions add moderation. Rules out:
listmonk, Buttondown, webmention.io, a comments widget.

## Monitoring (15 October 2026)

**No external monitoring.** Bunny terminates TLS and renews certificates; the site is static, so the
failure modes are a bad deploy (caught by the verify and browser jobs before publish, and by
`scripts/smoke.py` after it) or a Bunny outage (not ours to watch). Rules out: uptime pingers,
certificate-expiry checks, a CSP report collector. The CSP is enforced without one (11 November 2026):
the browser suite loads every page type with the policy enforced and fails on a violation, which is
the evidence a collector would have gathered.

## Bunny configuration as code (17 October 2026, replaces "Deferred" of 15 October)

**Edge rules are generated and synced from CI.** Renaming slugs added redirects with every rename,
and hand-made rules drift from the build (CSP hash, redirects). `edge/rules.toml` and the built
`/redirects.json` are the source of truth; `scripts/edge_rules.py --apply` syncs them in the
`publish` job after the upload, the same way rucksackrebellen does. The cost: Bunny has no scoped key
for edge rules, so the account API key is now a repository secret, exposed to that one step on
main-branch pushes only. Accepted by Jan. Rules out: hand-editing managed (`[repo] `) rules in the
dashboard, an account key in any other job. Zone settings that are not edge rules stay manual.

## Search (11 November 2026, replaces "Search index" of 15 October)

**Browsers search with Pagefind; `/search/index.json` stays for the MCP server.** The full-text
index every search downloaded had reached 172 kB of its 200 kB budget and grew with each essay, and
the October decision already named Pagefind as the next step. `scripts/search-index.sh` runs the
pinned Pagefind (`.pagefind-version`, checksum verified like Hugo) over the built pages that carry
`data-pagefind-body`, which are exactly the catalog entries (`check.py` compares the counts). The
command palette and `/search/` call its API directly; none of its UI components ship.

- **Cost.** Before any query a browser fetches 86 kB (API, worker, WebAssembly engine, metadata),
  budgeted at 100 kB. A query then fetches the index chunks it needs (about 33 kB each, seven
  today) and one fragment of 2 to 7 kB per result shown. A first search costs about what the old
  index did today; the difference is that it stops growing with the archive.
- **CSP.** The engine is a same-origin WebAssembly module, so `script-src` gains
  `'wasm-unsafe-eval'`. That allows WebAssembly compilation only, not `eval()` or inline script.
- **Matching.** Pagefind matches word stems and prefixes, not arbitrary substrings. When no indexed
  word starts with a query word it falls back to a loosely related word, so `search-core.js` first
  checks each query word on its own and returns nothing when one of them is unknown.
- **`/search/index.json`** is no longer fetched by any page. The MCP edge script reads it for
  `search_site`, so its budget is its own now (400 kB). If that is reached, trim what the edge
  script reads; do not point browsers back at it.

Rules out: a hosted search service, Pagefind's prebuilt UI, loading the engine before the reader asks
to search.

## Dates and review cadence (15 October 2026)

- `lastmod` is set only for a meaningful content change; the values carried over from the Stack site
  are kept as they were set by the author.
- Field-guide entries are reviewed at least every twelve months; essays on fast-moving topics show
  the older-guidance notice after five years unless reviewed. `python3 scripts/review-queue.py`
  lists what is due. A review sets `reviewed:` and, for field-guide entries, a `changes` line.
- Essays, talks and projects are written and published by Jan, so publication is their first
  review: they show no review label until a later review (17 October 2026). Field-guide
  entries were rewritten in a new form and stay unreviewed until Jan signs each one off.
- Old essays are not retired. The notice and the topic index handle age; a post is archived
  (`status: archived`) only when its advice is wrong, and superseded (`status: superseded`,
  `supersededBy`) when a newer page replaces it.
- Exception (13 November 2026): Jan removed the two whaling essays from 2023 after a quality review
  of the archive. Their routes and aliases redirect to `/topics/application-security/`
  (`data/redirects.toml`), and their baseline entries are now redirects without heading anchors.

## Dependencies (15 October 2026)

- Hugo is bumped by `scripts/bump-hugo.sh <version>` (pin plus verified Linux checksum), followed by
  a full local `./scripts/verify.sh` and `npm run test:browser` on that version. Cadence: when a
  release is at least two weeks old, at most quarterly unless a fix is needed.
- Pagefind is bumped the same way by `scripts/bump-pagefind.sh <version>`. Its API, worker and engine
  ship to readers, so read the release notes and rerun the search checks in `npm run test:browser`.
- Browser QA packages are pinned exactly; `renovate.json` groups them into one monthly PR if a
  Renovate runner is attached to the repository. Nothing in `package.json` ships to readers.
- GitHub Actions stay pinned to commit SHAs with the tag in a comment.
