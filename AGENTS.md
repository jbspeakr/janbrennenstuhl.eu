# Working on janbrennenstuhl.eu

A static editorial publication for human readers and HTTP clients. Hugo extended is pinned in `.hugo-version`; Python build dependencies are pinned in `requirements.txt`. No Go module or frontend application runtime is required. Node dependencies are only for browser QA.

## Commands

```sh
./scripts/bootstrap.sh
./scripts/verify.sh                 # production build, exports, all static contracts
.venv/bin/python scripts/serve.py    # verified output on http://127.0.0.1:8000
npm ci
npx playwright install chromium
npm run test:browser                # starts its own local server
```

Use `hugo server` for quick template iteration; the complete Markdown, search, social-card, and catalog outputs require `verify.sh`. Do not edit `public/`, `resources/`, `.venv/`, `.tools/`, or `test-results/`.

## Architecture

- `content/`: authoritative Markdown page bundles. Preserve published URLs and headings.
- `layouts/`: owned Hugo templates. `eligible.html` selects all substantive public content independently of the homepage.
- `assets/css/site.css`: design tokens, responsive layouts, both themes and print.
- `assets/js/`: small progressive enhancements. Only search loads the search module/index.
- `scripts/build.py`: source validation → Hugo → rendered-HTML-to-Markdown/catalog/search → social cards → static validation.
- `tests/fixtures/baseline-routes.json`: original 147 routes and heading anchors from `bc528e7905f6cb3fef08169d85774754b697fb7f`. Do not weaken the fixture to conceal a regression.
- `.forgejo/workflows/deploy.yml`: unprivileged verification/browser jobs; main-push-only publication of the same checksummed artifact.

## Content contract

Published essays, research, projects and talks require `id`, `title`, `description`, `date`, `kind`, `topics`, `status`, `reviewStatus`. Assign the ID once; never derive a new ID from a renamed title. Keep existing slugs. `lastmod` means a meaningful content change; `reviewed` and `reviewStatus: reviewed` require an actual editorial review. Missing review dates must never imply freshness. Status is `published`, `archived`, or `superseded`; the last requires `supersededBy` pointing to another page.

`description` is metadata; `excerpt` and `lead` default to it when omitted. A hero needs `imageAlt` or explicit `imageDecorative: true`. Never treat an informative diagram as decorative. Preserve credits and original media rights. Existing original content is CC BY 4.0; check individual exceptions.

Use Hugo `ref` for internal source references. `quote`, `details`, `youtube` (external link), and `callout` are supported. All substantive content must survive HTML-to-Markdown conversion. Add parity fixtures for new components, including captions, quotations, code, tables, footnotes and static explanations for interactive content.

## Design contract

Warm paper `#f6f3ed`, graphite `#20232a`, raspberry `#ac174d`; separate dark tokens. Editorial serif headings, system sans UI/body, system monospace code. Maintain the compact header, readable article column, native controls, visible focus, reduced-motion support, no-JS navigation/search browse fallback, and locally scrollable code/tables.

Budgets: shared CSS ≤25 kB gzip; shared initial JS ≤15 kB gzip; no runtime fonts or third-party scripts; initial article target ≤300 kB transfer. Test 360/768/1440px in both themes and reflow at 320px. Browser tests are necessary for presentation changes; passing a build alone is not visual approval.

## Release contract

No production credentials in PR jobs. Never publish from a pull request, rebuild between verification and deployment, delete old assets during upload, or introduce an account-wide Bunny API key. Read `docs/DELIVERY.md` before touching deployment. Edge caching, MIME, validators, live redirect status, rollback, and screen-reader checks are explicit release gates; local tests cannot certify them.
