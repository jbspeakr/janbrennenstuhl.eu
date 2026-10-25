# Decisions

Settled questions from the modernization review. Each entry says what was decided, why, and what it
rules out, so a later PR does not reopen it by accident. Dates are when the decision was taken.

## Licence and training (15 October 2026)

**CC BY 4.0 governs, including AI training.** The licence already permits reuse with attribution; a
text-and-data-mining reservation on top of it would contradict the grant. `robots.txt` allows every
crawler and signals `ai-train=yes`; `/.well-known/tdmrep.json` declares `tdm-reservation: 0`;
`/agents/` explains that attribution is the condition. Rules out: per-crawler disallow lists, a
"ask first" training policy, licence exceptions per page except `license: false` for legal pages.

## Analytics (15 October 2026)

**Plausible stays.** It is the one third-party request the site makes: `assets/js/theme.js` carries
the queue stub inside the already-hashed inline script, `baseof.html` puts the script URL on `<body>`
only when the build's base URL is the production host, `site.js` injects it after the load event so
it never competes with content (a plain `async` tag cost one simulated round trip of LCP in the
Lighthouse gate), and `scripts/check.py` allows exactly that host.
The CSP in `docs/DELIVERY.md` lists `https://plausible.io` in `script-src` and `connect-src`. No
proxying through Bunny for now; revisit only if ad blockers make the numbers useless. Rules out:
inline analytics snippets, self-hosted Plausible or Umami, a web-vitals beacon.

## Newsletter and webmentions (14 October 2026)

**Neither.** RSS, JSON Feed, the field-guide change feed and Mastodon are the distribution channels.
A newsletter adds a provider, a privacy page and a backlog; webmentions add moderation. Rules out:
listmonk, Buttondown, webmention.io, a comments widget.

## Monitoring (15 October 2026)

**No external monitoring.** Bunny terminates TLS and renews certificates; the site is static, so the
failure modes are a bad deploy (caught by the verify and browser jobs before publish, and by
`scripts/smoke.py` after it) or a Bunny outage (not ours to watch). Rules out: uptime pingers,
certificate-expiry checks, a CSP report collector for now.

## Bunny configuration as code (17 October 2026, replaces "Deferred" of 15 October)

**Edge rules are generated and synced from CI.** Renaming slugs added redirects with every rename,
and hand-made rules drift from the build (CSP hash, redirects). `edge/rules.toml` and the built
`/redirects.json` are the source of truth; `scripts/edge_rules.py --apply` syncs them in the
`publish` job after the upload, the same way rucksackrebellen does. The cost: Bunny has no scoped key
for edge rules, so the account API key is now a repository secret, exposed to that one step on
main-branch pushes only. Accepted by Jan. Rules out: hand-editing managed (`[repo] `) rules in the
dashboard, an account key in any other job. Zone settings that are not edge rules stay manual.

## Search index (15 October 2026)

**Full text stays in `/search/index.json`** so the command palette can search bodies, not only
titles. The budget is 200 kB compressed (about 150 kB today for 52 entries). When the budget is hit,
switch to a chunked index (Pagefind) instead of trimming bodies.

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

## Dependencies (15 October 2026)

- Hugo is bumped by `scripts/bump-hugo.sh <version>` (pin plus verified Linux checksum), followed by
  a full local `./scripts/verify.sh` and `npm run test:browser` on that version. Cadence: when a
  release is at least two weeks old, at most quarterly unless a fix is needed.
- Browser QA packages are pinned exactly; `renovate.json` groups them into one monthly PR if a
  Renovate runner is attached to the repository. Nothing in `package.json` ships to readers.
- GitHub Actions stay pinned to commit SHAs with the tag in a comment.
