# Deployment and rollback

## Build once, verify, publish

The Forgejo workflow has three jobs. `verify` creates and retains a checksummed artifact for 90 days. `browser` tests that artifact without production credentials. `publish` runs only for a push to `main`, after both jobs succeed, verifies artifact checksums and source revision, and uploads those same bytes. Third-party actions are pinned to immutable revisions; artifact actions are Forgejo’s patched v4 variants.

The workflow requests serialized, non-cancelled main-branch runs. Forgejo concurrency is best-effort; do not start a second deployment outside this workflow while one is running. A repeated older workflow must not be used as an accidental rollback.

Only the storage-zone password is used. The account-wide API key and pull-zone purge are no longer part of routine publishing. Assets upload before HTML/Markdown; feeds/catalogs follow, and the release manifest is last. Uploads retry transient failures and fail closed on errors. No remote files are deleted. This is ordered deployment, **not an atomic release switch**; HTML can briefly span two versions while uploading. Prior fingerprinted assets remain available.

Required secrets: existing `STORAGE_NAME`, `STORAGE_PASSWORD`. Optional variable `BUNNY_STORAGE_HOST` selects the actual regional Storage endpoint (default `storage.bunnycdn.com`). Validate it against the existing zone’s region before the first deployment.

Optional `INDEXNOW_KEY` is a **public repository variable**, not a credential: verification files are intentionally public. The build includes it in the artifact. After a successful upload, only catalog entries with changed content hashes are submitted. A failed/missing prior catalog skips notification; a notification failure does not turn a successful upload into a failed deployment. Move the existing secret value into this variable if retaining IndexNow.

## Bunny settings that must be applied before release

Source code cannot configure the authenticated pull zone. A `_headers` file would not configure Bunny, so none is shipped. Apply and verify these rules in the actual pull zone:

| Resource | Browser policy | Edge policy |
| --- | --- | --- |
| HTML, redirects, Markdown, XML, JSON, `llms.txt`, `security.txt`, release manifest | `public, max-age=0, must-revalidate` (or equivalent revalidation) | Separately configured short TTL, initially 300 seconds |
| Content-fingerprinted CSS/JS/images | `public, max-age=31536000, immutable` | Long TTL |
| Unfingerprinted images, social cards, icons and manifests | Revalidation or a deliberately short lifetime | Short/moderate TTL |

Do not classify every image as immutable: source-bundle URLs and `social.png` are mutable. Preserve existing HSTS, nosniff, referrer policy and frame protection. Enable appropriate compression and confirm the MIME types, especially `text/markdown; charset=utf-8`. Ensure ETag or Last-Modified validators yield 304 responses. A CDN purge cannot clear an already-fresh browser cache from the old 30-day policy; allow for that migration limitation explicitly.

Configure the custom error page so nonexistent URLs return **404**, not a 200 fallback. Existing aliases are preserved as Hugo redirect pages; verify whether Bunny should replace these with HTTP 301/308 redirects. No blanket redirect claim is made by local tests.

Start CSP in report-only mode. A starting candidate for this no-analytics, no-embed build is:

```
default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' https: data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'
```

Configure a real report destination if using reporting. Inspect legitimate violations, including author HTML and generated code, before enforcement. The theme initialization is external, so it does not require `unsafe-inline`. Do not silently expand allowlists.

## Dry run and live smoke checks

```sh
./scripts/verify.sh
npm run test:browser
.venv/bin/python scripts/deploy.py --dry-run
.venv/bin/python scripts/release.py
.venv/bin/python scripts/check_release.py
```

After deploying, wait for the chosen edge TTL, then run:

```sh
python3 scripts/smoke.py
```

The read-only smoke command verifies mutable-cache policies, Markdown MIME, validators/304s, catalog version and genuine 404 status. Also inspect response compression, representative image selection, alias redirect status, and the deployed revision manually. No live hosting settings were changed during implementation.

## Rollback rehearsal

Download the **previous** retained `verified-site` artifact from Forgejo and extract it into an isolated directory. Compare its manifest to the intended rollback revision; do not rebuild an old commit with new dependencies. Point the uploader’s `--root` at that extracted `public/` and dry-run. Re-upload its existing bytes through an explicitly operated main-branch release/rollback workflow with the same ordering; there is deliberately no unguarded local production-upload command. Confirm live revision, HTML, feeds and agent catalog after edge expiry.

A real rollback still requires a rehearsal against an authorized staging zone. Local archive extraction and checksum verification only prove artifact integrity. Preserve prior hashed assets for at least the 90-day rollback-artifact window; pruning is a separate reviewed operation. Before removing any public content, replace retired mutable URLs with explicit redirects or tombstones—retaining old files is not a content-removal mechanism.

## References

- [Forgejo concurrency reference](https://forgejo.org/docs/latest/user/actions/reference/#concurrency)
- [Forgejo artifact support](https://forgejo.org/docs/latest/user/actions/advanced-features/)
- [Bunny Storage upload API](https://bunny.net/docs/api-reference/storage/manage-files/upload-file)
- [HTTP caching semantics](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
