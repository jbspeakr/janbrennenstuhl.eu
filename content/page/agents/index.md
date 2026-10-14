---
title: For agents
slug: agents
description: How software agents can find, read, quote and cite this site, and what the reuse policy is.
date: 2026-10-13
lastmod: 2026-10-13
---

Everything on this site is written for people first, and every page is also available in a form that software can read without parsing HTML.

## Where to start

- [`/llms.txt`](/llms.txt) lists every entry with a one-sentence claim and a link to its Markdown version.
- [`/llms-full.txt`](/llms-full.txt) is the whole corpus as one Markdown file, newest first.
- Every page has a Markdown twin: add `index.md` to its URL, for example [`/agentic-identity-broker/index.md`](/agentic-identity-broker/index.md). Requesting a page with `Accept: text/markdown` returns the same twin. Each HTML page links to its twin with `<link rel="alternate" type="text/markdown">`.
- [`/catalog.json`](/catalog.json) holds IDs, canonical URLs, publication, modification and review dates, topics, license and a content hash for each entry.
- [`/findings.json`](/findings.json) lists every quotable finding with its anchor URL, the source it rests on and the review status of the page.
- [`/feed.json`](/feed.json) (JSON Feed 1.1) and [`/index.xml`](/index.xml) (RSS) carry full content. Each topic has its own feeds, for example [`/topics/passwords/feed.json`](/topics/passwords/feed.json).
- [`/.well-known/api-catalog`](/.well-known/api-catalog) (RFC 9727) points to all of the above.

## Citing

Findings and headings have permanent anchors such as `#f-pw-reuse-43-51pct`. Link the canonical HTML URL with the anchor, not the Markdown twin. The catalog's `reviewed` field is empty until an entry has had an editorial review; a recent build or modification date does not mean the advice was checked again.

## Reuse policy

Original writing is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless a page says otherwise: quote it, summarize it and link it with attribution. Credited third-party images keep their own rights.

- Search engines and agents fetching pages for a person's question are welcome. [`robots.txt`](/robots.txt) allows them by name.
- Training: I reserve text and data mining for AI model training. `robots.txt` disallows the known training crawlers and [`/.well-known/tdmrep.json`](/.well-known/tdmrep.json) declares the reservation in the TDMRep format. If you want to use the corpus for training, ask first.

Questions or corrections: see the [imprint]({{< ref "/page/imprint" >}}).
