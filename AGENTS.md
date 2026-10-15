# Working on janbrennenstuhl.eu

A static publication for people and agents. **Hugo extended is the only build dependency** (version in `.hugo-version`). Release scripts and checks use the Python 3.11+ standard library. Node is only for browser QA, Lighthouse and edge-script tests.

## Commands

```sh
./scripts/bootstrap.sh              # Hugo at the pinned version (Linux x86-64 downloads and verifies it)
./scripts/verify.sh                 # production build + scripts/check.py + unit tests
python3 scripts/serve.py            # serve public/ on :8000 like the edge (404s, MIME, Markdown negotiation)
npm ci && npx playwright install chromium
npm run test:browser                # axe matrix, keyboard, no-JS, reflow, palette, explainers, redirects
npm run test:lighthouse             # lab gate on three routes
npm run test:edge                   # MCP server and negotiation unit tests
```

`hugo server` is fine for template work. Do not edit `public/`, `resources/`, `.tools/`, `node_modules/` or `test-results/`.

## Architecture

- `content/`: Markdown page bundles. Preserve published URLs and heading anchors.
- `layouts/`: owned templates. `_partials/eligible.html` selects every substantive page; `_partials/data/*` derive id, kind, topics, series and status; `_partials/md/*` are the Markdown versions of shortcodes; `_partials/diagram.html` draws the trust-boundary diagrams.
- Output formats (config/_default/config.toml): `index.md` twins, `llms.txt`, `llms-full.txt`, `catalog.json`, `findings.json`, `feed.json`, `search/index.json`, `redirects.json`.
- `data/`: `topics.toml` (six topics and tag mapping), `series.toml`, `glossary.toml`, `redirects.toml`.
- `assets/css/site.css`: tokens, layout, both themes, print. `assets/js/`: `site.js` (shared), `palette.js` and `search.js` (on demand), `explainers/*` (per page).
- `edge/`: Bunny Edge Scripts for Markdown negotiation and the read-only MCP server.
- `scripts/check.py`: release gates. `tests/fixtures/baseline-routes.json`: the 147 original routes and heading anchors; never weaken it to hide a regression.

## Content contract

See `docs/CONTENT-CONTRACT.md`. Authors write `title`, `description`, `date`, `tags` (and `slug` for posts). Everything else is derived. Existing `id` values are permanent. `lastmod` means a meaningful content change. `reviewed` requires an actual editorial review by Jan; never add it on someone's behalf, and a missing review date must never be presented as freshness.

Field-guide entries are question-led: `answer`, key findings as `finding` shortcodes with sources, an evidence table, what to do, and a `changes` log. Numbers come from the cited source or are left out. Every shortcode needs a Markdown variant; interactive explainers need a static explanation that stands alone.

## Design contract

See `docs/DESIGN.md`. Dark-first OKLCH tokens with an equal light theme; Geist and Geist Mono self-hosted; calm graphite tones with one soft accent (rose, from the site icon) per view; generated flow drawings; nothing below 13px; visible focus; reduced-motion support; everything usable without JavaScript.

Budgets (compressed): CSS ≤ 15 kB, article JS ≤ 8 kB, HTML per article ≤ 30 kB, preloaded font ≤ 35 kB, inline diagram ≤ 6 kB, zero third-party requests. Test 360/768/1440 px in both themes and reflow at 320 px. Passing tests is not design approval.

## Release contract

Read `docs/DELIVERY.md` before touching deployment. No production credentials in PR jobs; publish only from `main`; never rebuild between verification and deployment; never delete remote files during upload; no account-wide Bunny API key. The inline theme script is allowed by a CSP hash documented in `docs/DELIVERY.md`; `check.py` fails until the doc and the edge match the build. Edge caching, MIME, 301s, negotiation, rollback and screen-reader checks are release gates that local tests cannot certify.

## Adding content

Use the archetypes; never hand-copy front matter from another page.

- Essay: `hugo new content post/<slug>`
- Field-guide entry: `hugo new content knowledge-base/<area>/<slug>` (areas: account-security, oidc, agent-identity)
- Talk: `hugo new content talks/<slug>`
- Project: `hugo new content projects/<slug>`

Then fill in the fields marked in the file, replace `CHANGE-ME` finding IDs with permanent unique IDs, remove `draft: true`, and run `./scripts/verify.sh`. See docs/CONTENT-CONTRACT.md for the rules.
