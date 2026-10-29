# Brennenstuhl on Security

[![Verify](https://github.com/jbspeakr/janbrennenstuhl.eu/actions/workflows/verify.yml/badge.svg)](https://github.com/jbspeakr/janbrennenstuhl.eu/actions/workflows/verify.yml)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)

The source of **[janbrennenstuhl.eu](https://www.janbrennenstuhl.eu)**: essays, a field guide and research notes on application security, identity, passwords, tokens and agent identity, by Jan Brennenstuhl.

The site is a static publication for two audiences: people who read it in a browser, and agents that search, cite and quote it. Every page has a Markdown twin, every key finding has a stable anchor, and the whole thing ships without a framework.

- **Built with** [Hugo](https://gohugo.io) extended, owned templates, no theme
- **Hosted on** [Bunny](https://bunny.net) in the EU, released from `main` by GitHub Actions
- **Budgets:** at most 15 kB of CSS and 8 kB of JavaScript per article, no third-party requests except privacy-friendly analytics
- **Usable** without JavaScript, in both themes, down to 320 px

## Quick start

Hugo extended at the version in [`.hugo-version`](.hugo-version) is the only build dependency, except for the social cards: CI draws each article's card plate with Chromium first (`scripts/card-plates.sh`), and local builds fall back to the topic plate. The release scripts and checks use the Python 3.11+ standard library.

```sh
./scripts/bootstrap.sh     # install or check the pinned Hugo
./scripts/verify.sh        # build public/ and run every static release gate
python3 scripts/serve.py   # http://127.0.0.1:8000, with real 404s and Markdown negotiation
```

`hugo server` is fine for template work.

Browser, Lighthouse and edge-script checks need Node and are for QA only:

```sh
npm ci
npx playwright install chromium
npm run test:browser       # axe, keyboard, no-JS, reflow, explainers, redirects
npm run test:lighthouse    # lab gate on three routes
npm run test:edge          # MCP server and Markdown negotiation
```

## Repository layout

| Path | What it holds |
| --- | --- |
| `content/` | The writing: essays (`post/`), the field guide (`knowledge-base/`), talks, projects and pages, as Markdown page bundles |
| `layouts/` | Owned Hugo templates, shortcodes and their Markdown variants, the trust-boundary diagrams |
| `assets/` | CSS tokens and themes, small JavaScript modules, icons, social-card plates |
| `data/` | Topics, series, glossary and redirects |
| `edge/` | Edge rules (headers, CSP, caching) and Bunny Edge Scripts for Markdown negotiation and the MCP server |
| `scripts/` | Build, release gates, deploy, link checks (Python standard library) |
| `tests/` | Browser, Lighthouse and edge tests, plus the baseline of every original route |
| `docs/` | How the site works and why (see below) |

## For agents

Search, retrieval and training are welcome under CC BY 4.0. Attribution is the condition. The policy is at [`/agents/`](https://www.janbrennenstuhl.eu/agents/).

- [`/llms.txt`](https://www.janbrennenstuhl.eu/llms.txt) and [`/llms-full.txt`](https://www.janbrennenstuhl.eu/llms-full.txt)
- [`/capabilities.txt`](https://www.janbrennenstuhl.eu/capabilities.txt) and [`/.well-known/capabilities.json`](https://www.janbrennenstuhl.eu/.well-known/capabilities.json)
- A Markdown twin of every page at `<url>index.md`, or with `Accept: text/markdown`
- [`/catalog.json`](https://www.janbrennenstuhl.eu/catalog.json), [`/findings.json`](https://www.janbrennenstuhl.eu/findings.json) and [`/feed.json`](https://www.janbrennenstuhl.eu/feed.json)
- [`/.well-known/api-catalog`](https://www.janbrennenstuhl.eu/.well-known/api-catalog) (RFC 9727)
- A read-only MCP server in [`edge/mcp/`](edge/mcp/), with an MCP Registry entry as `eu.janbrennenstuhl/site`

## Documentation

- [Content contract](docs/CONTENT-CONTRACT.md): front matter, field-guide shape, shortcodes, machine outputs
- [Design system](docs/DESIGN.md): tokens, contrast, type, the diagram, budgets
- [Delivery](docs/DELIVERY.md): CI, Bunny configuration, CSP, redirects, MCP, rollback
- [Decisions](docs/DECISIONS.md): settled questions, such as licence and training, and analytics
- [Implementation notes](docs/IMPLEMENTATION.md): what changed and what is still open
- [`AGENTS.md`](AGENTS.md): the working guide for coding agents in this repository

## Corrections

This is a personal publication, so the repository does not take issues or pull requests. Corrections are still welcome: for a factual error, a broken link or an accessibility problem, use the contact details in the [imprint](https://www.janbrennenstuhl.eu/imprint/), which every article links as "Send a correction". Security reports follow [`/.well-known/security.txt`](https://www.janbrennenstuhl.eu/.well-known/security.txt).

## Licenses

This repository holds two kinds of work under two licenses.

| What | License |
| --- | --- |
| **Writing:** everything under `content/`, and the prose in `data/` (topic, series and glossary descriptions) | [CC BY 4.0](LICENSE-CONTENT), including AI training, unless a page says otherwise |
| **Code:** templates, CSS, JavaScript, scripts, edge scripts, tests, configuration and documentation | [MIT](LICENSE) |

The CC BY grant does not cover:

- Pages marked `license: false` in their front matter: the imprint, the privacy policy, the affiliate disclaimer and the about page.
- Credited third-party images and quotations in the writing. They keep their own rights.
- Portraits of Jan Brennenstuhl, and the Bunny logos in `static/images/`, which are trademarks of their owner.

Bundled third-party work:

- [Geist and Geist Mono](https://vercel.com/font) fonts, © Vercel, under the SIL Open Font License 1.1 ([`static/fonts/OFL.txt`](static/fonts/OFL.txt), [`assets/fonts/OFL-Geist.txt`](assets/fonts/OFL-Geist.txt)).
- Icons in `assets/icons/` from [Tabler Icons](https://tabler.io/icons), © Paweł Kuna, under the MIT License.
- [Hugo](https://github.com/gohugoio/hugo), downloaded at build time, is under the Apache License 2.0.

To reuse an article, name the author, link the canonical URL and say if you changed it. For example: *"Title" by Jan Brennenstuhl, https://www.janbrennenstuhl.eu/…, CC BY 4.0.*
