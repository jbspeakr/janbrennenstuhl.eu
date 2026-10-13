# Content and representation contract

`layouts/_partials/eligible.html` selects published substantive pages and the author profile. Hugo excludes drafts, expired pages and future publications before that selection. Homepage selection is independently restricted to posts. Utilities, search results and taxonomy listings are not dumped into the content catalog.

## Identity and dates

`id` is a stable editorial identifier assigned in source. `canonical_url` is the existing public HTML URL; `markdown_url` appends `index.md`. Changing a title does not change identity. Preserve a slug or add an alias/redirect if a deliberate move is required.

Publication dates, meaningful modification dates, and technical review dates are distinct. Builds do not use Git timestamps as content freshness. `review_status: not-reviewed` means no separate editorial review has been recorded; it does not claim an article is wrong. Archive/supersession status is visible in the article. `source_revision` is build provenance, not a review date.

The catalog’s `schema_version: "1.0"` is a site-owned contract. An incompatible change requires a major version change. New optional properties are additive.

## Generated representations

1. Hugo renders the source, including `ref`, `quote`, `details`, image hooks and code highlighting.
2. The exporter selects the article lead, hero/caption and substantive body; navigation, controls and related links are excluded.
3. Links and image URLs become absolute. Headings and other citation IDs receive explicit anchors in Markdown. Code fences preserve code and language; quotations retain sources; tables, footnotes, details and image descriptions have conversion fixtures.
4. Metadata is serialized, not hand-built. `index.md` carries metadata and body. Its SHA-256 hash is stored in the catalog and HTML metadata. This hash detects changes; it is not a signature.
5. Search uses the same eligible collection and rendered body. The catalog stays metadata-only; the search index additionally contains full text and section excerpts.

Markdown excludes build-only revision fields so an unrelated build does not change every document hash. Exact source revision and source URLs remain available in the catalog. Dirty local builds identify themselves with a `-dirty` revision and are not release artifacts; create release archives from clean commits.

For pages with `license: false`, machine metadata says “Not specified”; it does not silently grant CC BY. Third-party media rights are explicitly excluded from the original-writing license.

## Authoring new entries

```yaml
id: jb-example-unique-id
kind: essay # essay | research | guide | project | talk
status: published # published | archived | superseded
reviewStatus: not-reviewed
title: An exact and useful title
description: A concise description of the article.
slug: existing-or-new-slug
date: 2026-10-13
topics: [application-security]
image: example.webp
imageAlt: A concrete description of the informative image.
```

Use `imageDecorative: true` instead of alt text only for decorative art. A technical diagram must have a meaningful alternative and an equivalent prose explanation. Optional `related` is a list of Hugo page references, taking precedence over related-by-tags/series ranking. Broad categories no longer dominate relevance.

Test new shortcodes against Markdown, RSS and no-JS HTML. Do not pass unrendered `.RawContent` to agents or duplicate claims in a second manually maintained document. Avoid global JavaScript for article-specific interactives.
