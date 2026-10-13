# Brennenstuhl on Security

The source of [janbrennenstuhl.eu](https://www.janbrennenstuhl.eu): Jan Brennenstuhl’s independent publication on application security, identity, and agentic engineering. Built with Hugo, hosted on Bunny, and maintained on Codeberg.

The presentation is a small, owned editorial design system: static HTML, system fonts, responsive images, dark/light/system themes, full-content feeds, and progressive enhancement. There is no client application or theme dependency.

## Develop

Requirements: Python 3.11+, Git, and Hugo extended at the version in `.hugo-version`. On Linux x86-64, bootstrap downloads and checks the pinned Hugo binary automatically. On other platforms install the matching Hugo release first. Build requirements are installed in a local virtual environment.

```sh
./scripts/bootstrap.sh
./scripts/verify.sh
.venv/bin/python scripts/serve.py
```

Open `http://127.0.0.1:8000`. `verify.sh` builds canonical HTML, resolved Markdown, the content catalog, search index, and social cards; then checks source metadata, routes, fragments, fidelity, structured data, feeds, drafts, and asset budgets. `./scripts/verify.sh --unminified` checks the unminified build too.

For quick template iteration, `hugo server` works, but generated machine/search/social outputs require the complete build. Do not deploy a bare Hugo build.

```sh
npm ci
npx playwright install --with-deps chromium
npm run test:browser
```

Browser tests start their own server and cover five page types at three widths in both themes, axe checks, keyboard navigation, theme persistence, search history, no-JS browsing, text spacing, 320px reflow, and a real 404 response. Set `CHROMIUM_EXECUTABLE` only to use an existing compatible browser installation. Test dependencies are not shipped to readers.

## Read with an agent

- `/llms.txt`: orientation and per-entry Markdown links.
- `/content-index.json`: versioned metadata, canonical URLs, provenance, section descriptors and SHA-256 hashes.
- `/<existing-route>/index.md`: faithful rendered content with attribution, dates and stable section anchors.
- `/index.xml`: full-content RSS, including knowledge-base entries.
- `/search/`: all eligible content, with type/topic filters and query URLs; its index is loaded only when searching.

See [the content contract](docs/CONTENT-CONTRACT.md), [release procedures](docs/DELIVERY.md), and [implementation evidence and remaining release work](docs/IMPLEMENTATION.md).

## Licenses

Original writing under `content/` is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), except where an individual page specifies otherwise. Credited third-party media retain their own rights. The old Stack presentation dependency has been removed. Build-only social-card fonts include their upstream license under `assets/fonts/LICENSE`; fonts are not downloaded by readers. Hugo is Apache-2.0 licensed.
