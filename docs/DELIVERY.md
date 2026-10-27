# Deployment and rollback

## Build once, verify, publish

Two workflows split verification from release. `.github/workflows/verify.yml` runs `verify`, `browser` and `preview` on every push and PR and holds no production credentials. `.github/workflows/publish.yml` runs `publish` only after a successful `Verify` run for a push to `main` in this repository. It is triggered by `workflow_run`, so GitHub always runs the copy on `main`: a pull request cannot change what publishes or reach the production secrets.

| Job | Runs on | Credentials | Does |
| --- | --- | --- | --- |
| `verify` | every push and PR | none | `bootstrap.sh` (Hugo only), `verify.sh` (build + `check.py` + unit tests), deploy dry run, edge-rule dry run (artifact `edge-rules`), `release.py` packages a checksummed artifact kept for 90 days |
| `browser` | every push and PR | none | tests that same artifact: axe matrix, keyboard, no-JS, reflow, redirects, Markdown negotiation, Lighthouse lab gate |
| `preview` | same-repo PRs, only if `vars.PREVIEW_HOST` is set | staging zone only | builds for the preview host and uploads to the staging storage zone |
| `publish` (publish.yml) | after `Verify` succeeds on a push to `main` | production storage password; account API key for the edge-rule sync | checks artifact checksums and revision, uploads the same bytes, then syncs the edge rules |

Third-party actions are pinned to commit SHAs. Verify serializes runs per ref; Publish serializes all releases and never cancels an upload halfway. Do not start a second deployment outside this workflow.

Uploads use only the storage-zone password. The account API key is used by one step, the edge-rule sync in `publish`, because Bunny has no scoped key for edge rules (docs/DECISIONS.md). Assets upload before HTML and Markdown; feeds and catalogs follow; the release manifest is last. No remote file is ever deleted, so prior fingerprinted assets stay available. This is an ordered upload, **not an atomic switch**: for a short time HTML can span two versions.

Secrets and variables: the production ones (`STORAGE_*`, `ACCOUNT_API_KEY`, `BUNNY_*`, `INDEXNOW_KEY`) belong to the `production` environment, which only the `publish` job uses. So does `INDEXNOW_KEY`. The `PREVIEW_*` values are repository-level, because `preview` runs without an environment.

- `STORAGE_NAME`, `STORAGE_PASSWORD` (secrets): production storage zone. Only the `publish` job in publish.yml sees them.
- `ACCOUNT_API_KEY` (secret), `BUNNY_PULL_ZONE_ID` (variable): the edge-rule sync. Only its step in `publish` sees the key, and `edge_rules.py --apply` refuses to run outside a main-branch push.
- `BUNNY_SYNC_EDGE_RULES` (variable): set to `true` to enable the sync (see below).
- `BUNNY_STORAGE_HOST` (variable, optional): regional storage endpoint, default `storage.bunnycdn.com`.
- `INDEXNOW_KEY` (production environment secret, optional): IndexNow key. It is served at `/<key>.txt` but kept out of the repository, the build and the logs so it cannot be guessed. `deploy.py` uploads `<key>.txt` after the artifact, outside the release manifest; after a successful upload only catalog entries whose `content_hash` changed are submitted.
- `PREVIEW_HOST` (variable), `PREVIEW_STORAGE_NAME`, `PREVIEW_STORAGE_PASSWORD` (secrets): optional staging pull zone for PR previews. `deploy.py --preview` refuses to run if production variables are present. The preview is rebuilt with the preview base URL; it is a review copy, not the release artifact.

## Bunny pull zone configuration

Edge rules are code. `edge/rules.toml` holds security headers, CSP, caching and MIME types; `scripts/edge_rules.py` adds the Markdown negotiation rule and one 301 rule per redirect target from the built `/redirects.json`, then the `publish` job syncs them after the upload. Managed rules carry the description prefix `[repo] `; the sync creates, updates and deletes only those and leaves hand-made rules alone. Run `python3 scripts/edge_rules.py` to see the rules without changing anything.

Bunny allows 50 edge rules per pull zone by default, hand-made ones included (about 47 are managed today; every renamed page with a new target adds one). The dry run fails a PR that goes over `maxRules`, and the sync refuses to run if hand-made rules would push the zone over it. Ask Bunny support to raise the limit, then update `maxRules`.

Enabling the sync, once: delete the hand-made rules that `edge/rules.toml` replaces (security headers, `Cache-Control`, redirects; the old site also sends `X-XSS-Protection` and `Referrer-Policy: strict-origin`), add `ACCOUNT_API_KEY` and `BUNNY_PULL_ZONE_ID`, set `BUNNY_SYNC_EDGE_RULES=true`, and run `publish`. Then run `scripts/smoke.py`. Rehearse on the staging zone first: `edge_rules.py --apply --host <preview host>` with the staging pull zone ID runs from a laptop; for the production host the script only runs on a main-branch push.

Zone settings that are not edge rules stay manual: Brotli and gzip, validators, the 404 page, the root-domain redirect. `scripts/smoke.py` checks the observable parts after deployment, including a 301 for every entry in `/redirects.json`.

### Caching

The values below are in `edge/rules.toml`; change them there.

| Resource | Browser `Cache-Control` | Edge TTL |
| --- | --- | --- |
| HTML, `index.md`, `*.json`, `*.xml`, `llms.txt`, `llms-full.txt`, `robots.txt`, `/.well-known/*`, `release-manifest.json` | `public, max-age=0, must-revalidate` | 300 s |
| Fingerprinted `/css/*.css`, `/js/*.js` (hash in the file name) and processed images (`*_hu_*`) | `public, max-age=31536000, immutable` | 1 year |
| `/fonts/*` (version in the file name) | `public, max-age=31536000, immutable` | 1 year |
| `social.png`, favicons, `site.webmanifest`, original bundle images | `public, max-age=86400` | 1 day |

Enable Brotli and gzip. Make sure `ETag` or `Last-Modified` validators produce `304` responses. A CDN purge cannot clear browser caches filled under the old 30-day policy; expect that migration lag once.

### MIME types

Edge rules from `edge/rules.toml` set:

| Path | Content-Type |
| --- | --- |
| `*.md`, `llms-full.txt` (Markdown in a .txt) | `text/markdown; charset=utf-8` for `.md`, `text/plain; charset=utf-8` for `.txt` |
| `feed.json`, `*/feed.json` | `application/feed+json; charset=utf-8` |
| `/.well-known/api-catalog` (no extension) | `application/linkset+json` |
| `/.well-known/tdmrep.json`, other `*.json` | `application/json; charset=utf-8` |
| `*.woff2` | `font/woff2` |
| `*.avif` | `image/avif` |

`deploy.py` sends these types on upload as well.

### Errors and redirects

- Custom error page: `/404.html` with a real **404** status, not a 200 fallback.
- Retired routes: `/redirects.json` lists every old URL (former home pagination, categories, tags, section pagination, front-matter aliases) with its new target. The synced edge rules answer each with a **301**, one rule per target; patterns include the host, so `/1/` never matches `/knowledge-base/account-security/1/`. The HTML redirect pages in the artifact remain as a fallback for clients that reach the origin. Old pagination URLs (`/2/`, `/tags/x/1/`) get only that HTML page, no edge rule: they were never linked, and the zone has 50 rules. Old `…/index.md` twins of renamed pages are not redirected.
- Directory URLs: `/about/index.html` and `/about` **301** to `/about/` at any depth (`%{Url.Directory}`), keeping a query string on the `index.html` redirect. Extensionless `/.well-known/*` files are excluded by URL.
- Root domain, the zone's `*.b-cdn.net` hostname and `jbspeakr.cc` (with `www`) to `www.janbrennenstuhl.eu`: one managed **301** rule (`canonicalFrom` in `edge/rules.toml`), so only one edge domain is ever indexed.

### Headers and CSP

`edge/rules.toml` sets HSTS, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()`, `X-Frame-Options: DENY` (enforces `frame-ancestors 'none'` while the CSP is report-only) and the CSP, which starts in **report-only** mode (`[csp] header`).

- The `sha256` source allows exactly one inline script: the theme snippet in `<head>` (`assets/js/theme.js`, which also carries the Plausible queue stub), inlined so it never waits for the stylesheet. `https://plausible.io` in `script-src` and `connect-src` is for the analytics script (injected by `site.js` after the load event) and its beacon, the only third-party origin (docs/DECISIONS.md). `scripts/check.py` fails the build when an inline script has no hash in `edge/rules.toml` or a hash there is no longer used; the next publish syncs the change.
- `'inline-speculation-rules'` allows the `<script type="speculationrules">` block that prerenders same-site pages on hover in Chromium.
- No styles are inlined; critical CSS stays in the fingerprinted file so `style-src 'self'` holds (see docs/DESIGN.md for the LCP trade-off).

Inspect real violations before enforcing. Do not expand the allowlists silently.

### Markdown content negotiation

Every page has a Markdown twin at `<url>index.md`. Two ways to serve it for `Accept: text/markdown` on the HTML URL:

1. **Edge rule, synced by default:** condition "Request header `Accept` contains `text/markdown`" and URL ends in `/`; action "Redirect to `{{path}}index.md`" with status 302. Redirects from edge rules are not cached, and agents follow them. Unlike the edge script it ignores q-values.
2. **Edge script:** `edge/negotiate.ts` (middleware on the www pull zone) rewrites the origin request to the twin and adds `Vary: Accept`. Middleware runs on cache misses only, so add an edge rule that **bypasses the cache** when `Accept` contains `text/markdown`; otherwise a twin could be cached under the HTML URL. Bundle `negotiate.ts` with `negotiate-core.ts` before upload (for example `deno bundle` or esbuild).

`npm run test:edge` covers the negotiation rule; `scripts/serve.py` behaves the same way locally.

### Read-only MCP server

`edge/mcp/` is a standalone Bunny Edge Script serving MCP at `https://mcp.janbrennenstuhl.eu/mcp` (suggested host). It is dual-era: MCP revision 2026-07-28 (stateless, per-request `_meta`, mirrored headers validated) and the `initialize` handshake for 2025-03-26 to 2025-11-25 clients. Tools: `search_site`, `get_entry`, `get_findings`, `list_topics`. It only fetches the site's own `search/index.json`, `catalog.json`, `findings.json` and Markdown twins, caches them for 5 minutes, and never fetches a URL taken from a request. No authentication: everything it serves is public. Set a rate limit on its pull zone. After deploying, add it to `static/.well-known/api-catalog`.

## Dry run and live checks

```sh
./scripts/verify.sh
npm run test:browser
npm run test:lighthouse
python3 scripts/deploy.py --dry-run
python3 scripts/release.py
python3 scripts/check_release.py
```

After deploying, wait for the edge TTL, then run `python3 scripts/smoke.py`. It checks mutable-cache policies, Markdown MIME, validators and 304s, the catalog version and a genuine 404. Also check compression, image format selection (AVIF/WebP), Markdown negotiation and the deployed revision by hand.

## Dependencies

Hugo moves with `scripts/bump-hugo.sh <version>`, which rewrites `.hugo-version` and the verified Linux checksum that `scripts/bootstrap.sh` enforces; verify and run the browser tests locally on the new version before opening the PR. Browser QA packages are exactly pinned in `package.json`; `renovate.json` describes a monthly grouped update for any Renovate runner attached to the repository. Actions stay pinned to commit SHAs. Cadence and reasoning: `docs/DECISIONS.md`.

## Rollback

Download the **previous** retained `verified-site` artifact from GitHub Actions and extract it into an isolated directory. Compare its manifest with the intended rollback revision; do not rebuild an old commit with new dependencies. Dry-run `deploy.py --root <extracted>/public`, then re-upload those bytes through an explicitly operated main-branch run with the same ordering. There is deliberately no unguarded local production upload. Rehearse this against the staging zone before the first real release.

Prior fingerprinted assets remain for at least the 90-day artifact window; pruning is a separate reviewed operation. Retiring a page needs a redirect or a tombstone; leaving old files in storage is not a removal mechanism.

## References

- [GitHub Actions concurrency](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#concurrency)
- [Bunny Storage upload API](https://bunny.net/docs/api-reference/storage/manage-files/upload-file)
- [Bunny Edge Scripting SDK](https://github.com/bunnyway/edge-script-sdk)
- [Bunny edge rule API](https://docs.bunny.net/api-reference/core/pull-zone/addupdate-edge-rule) and [CDN limits](https://docs.bunny.net/cdn/limits)
- [MCP 2026-07-28: Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [RFC 9727: api-catalog](https://www.rfc-editor.org/rfc/rfc9727)
- [HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
