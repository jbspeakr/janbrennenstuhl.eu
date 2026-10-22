# Brennenstuhl on Security

The source of [janbrennenstuhl.eu](https://www.janbrennenstuhl.eu): Jan Brennenstuhl's essays, field guide and research notes on application security, identity, passwords, tokens and agentic engineering. Built with Hugo, hosted on Bunny in the EU, maintained on Codeberg.

## Build

The only build dependency is Hugo extended at the version in `.hugo-version`.

```sh
./scripts/bootstrap.sh     # installs or checks Hugo
./scripts/verify.sh        # builds public/ and runs every static release gate
python3 scripts/serve.py   # http://127.0.0.1:8000, with real 404s and Markdown negotiation
```

Browser and lab checks (Node, test-only):

```sh
npm ci
npx playwright install chromium
npm run test:browser
npm run test:lighthouse
npm run test:edge
```

## For agents

- [`/llms.txt`](https://www.janbrennenstuhl.eu/llms.txt) and [`/llms-full.txt`](https://www.janbrennenstuhl.eu/llms-full.txt)
- Markdown twin of every page at `<url>index.md`, or with `Accept: text/markdown`
- [`/catalog.json`](https://www.janbrennenstuhl.eu/catalog.json), [`/findings.json`](https://www.janbrennenstuhl.eu/findings.json), [`/feed.json`](https://www.janbrennenstuhl.eu/feed.json)
- [`/.well-known/api-catalog`](https://www.janbrennenstuhl.eu/.well-known/api-catalog) (RFC 9727)
- A read-only MCP server (`edge/mcp/`), deployable as a Bunny Edge Script
- Policy: [`/agents/`](https://www.janbrennenstuhl.eu/agents/). Search and retrieval are welcome; AI training is reserved.

## Documentation

- [Content contract](docs/CONTENT-CONTRACT.md): front matter, field-guide shape, shortcodes, machine outputs
- [Design system](docs/DESIGN.md): tokens, contrast, type, the diagram, budgets
- [Delivery](docs/DELIVERY.md): CI, Bunny configuration, CSP, redirects, MCP, rollback
- [Implementation notes](docs/IMPLEMENTATION.md): what changed and what is still open

## Licenses

Original writing under `content/` is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless a page says otherwise. Credited third-party media keep their own rights. Geist and Geist Mono are under the SIL Open Font License 1.1 (`static/fonts/OFL.txt`). Hugo is Apache-2.0.
