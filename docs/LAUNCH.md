# Launch: cutover from the Stack site

The modernize branch replaces the live Hugo Theme Stack site on the same domain and storage zone. The
release workflow handles bytes; this list handles everything around them. Work top to bottom; nothing
below "Publish" happens before everything above it is ticked.

## Before merging

- [ ] Editorial sign-off on the rewritten field-guide entries; set `reviewed:` only on entries that
      were actually reviewed (`python3 scripts/review-queue.py` shows the queue).
- [ ] Design sign-off on the screenshots the browser job uploads (`screenshots` artifact: home,
      article and guide at 360/768/1440 px in both themes).
- [ ] Manual screen-reader pass (VoiceOver/Safari, NVDA/Firefox); update the accessibility statement
      with the date.
- [ ] `./scripts/verify.sh`, `npm run test:browser`, `npm run test:lighthouse` and
      `python3 scripts/links.py` green on the merge candidate.
- [ ] Bunny: cache, MIME, 404 and 301 rules, headers and the report-only CSP from `docs/DELIVERY.md`
      applied to the staging zone; `python3 scripts/smoke.py` against staging; rollback rehearsed
      there once (`docs/DELIVERY.md`, "Rollback").
- [ ] Content freeze on `main` from this point: no post edits until the cutover is done.
- [ ] Save the current live site to the Wayback Machine (home, `/llms.txt`, a few posts) so the old
      rendering is retrievable.

## Publish

- [ ] Merge `modernize` into `main` with a merge commit (keeps both histories).
- [ ] Apply the same Bunny rules to the production zone (`docs/DELIVERY.md`), then purge once.
- [ ] Watch the `publish` job; the upload order is assets, HTML and Markdown, feeds and catalogs,
      manifest.
- [ ] `python3 scripts/smoke.py` against production after the edge TTL. By hand: compression,
      AVIF/WebP selection, three retired routes return 301, `Accept: text/markdown` returns a twin.

## First hour

- [ ] Every route in `tests/fixtures/baseline-routes.json` answers 200 on the live host
      (`python3 scripts/smoke.py` covers this when run with the fixture).
- [ ] Mastodon profile link verification still shows the green check (`rel="me"` moved into the new
      head partial).
- [ ] IndexNow accepted the submission (job log); Search Console shows the new sitemap.
- [ ] Plausible receives page views from the production host and none from the preview host.
- [ ] Deploy the MCP edge script if wanted and add it to `static/.well-known/api-catalog`.

## First week

- [ ] Check CSP report-only violations in Bunny logs if a collector was configured; otherwise skip.
- [ ] Search Console: crawl errors, soft 404s, redirect chains.
- [ ] Lift the content freeze; announce the field guide and the agents page on Mastodon.
- [ ] Delete the `redesign` branch; keep `modernize` until the first post-launch release is out.
