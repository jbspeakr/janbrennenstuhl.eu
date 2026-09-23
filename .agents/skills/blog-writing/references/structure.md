# Blog Structure and Hugo Presentation

Read this together with [voice.md](voice.md). This file owns article shape, headings, openings, lists, and Hugo mechanics. Voice rules still apply to every authored part; formatting never provides an exception to a banned construction.

## Choose the Reader's Route

Identify the article's useful contribution before outlining: an artifact, method, measured result, reusable model, or honestly framed observation. Decide what the reader should understand or be able to do afterward. Use the structure that fits that contribution.

### Argument

Open with a concrete problem, event, artifact, or observation. State the thesis within the first 2 paragraphs. Order supporting sections by their importance to the reader's decision, with necessary context before claims that depend on it. Put evidence and material limitations beside the claims they qualify.

An argument will often need 3 to 5 H2 sections. Treat that as a sizing guide, not a quota: do not invent sections or compress distinct reasoning to hit a count.

### Build or Reproduction

Open with the motivation and the artifact or result. Give the reader the prerequisites and approach in the order needed to follow the work. Show results where they arise, including failed attempts that explain a decision. End with a supported limitation, unresolved question, or useful next step when there is one.

Use 1 H2 per meaningful phase of the reader's reasoning. Do not force an argument's thesis deadline or section count onto a walkthrough, but make its purpose clear in the opening.

### Field Note or Public Talk

Open with the public context or the author's supplied firsthand observation. State the lesson early, support it with evidence or a concrete example, and give reusable guidance or a relevant pointer. Do not invent attendance, conversations, or private context.

Use 1 H2 per distinct point or phase. Keep event background proportional to what the reader needs to understand the lesson.

## Organize Sections Around Reader Questions

Each section develops 1 self-contained point. Give every proposed H2 a private, 1-sentence purpose during outlining; merge sections with the same purpose. A section may contain several pieces of evidence for its point.

Headings should tell the reader what someone does, finds, or needs to decide. Keep actors visible when a heading describes an action. Use specific headings, not generic labels such as "Overview" or "Key takeaways". Short reference labels such as "Prerequisites" are fine when they help navigation. Do not repeat the heading in the first sentence beneath it.

Use H2 (`##`) for main sections and H3 (`###`) for necessary subsections. Rarely go deeper. Do not add a subsection for a single sentence that belongs in the surrounding paragraph.

Guide the reader through the order of information. End a section when its point is complete; do not add a teaser, reaction, or repetitive bridge to manufacture momentum. A conclusion is optional. If the final section already completes the argument, stop there. A separate ending must add a concrete decision, implication, limitation, or next action, not recap the article.

## Keep Evidence Close

Distinguish documented facts, the author's observations, inferences, and recommendations in natural prose. These are drafting distinctions, not mandatory labels before every sentence.

- Technical work, outcomes, and professional experience require public or inspectable support, such as a repository, talk, slide deck, published result, or primary source. Personal preferences and supplied lived observations can stand alone when honestly framed and free of employer context.
- For quantitative comparisons, name the baseline, units, method, scope, and source. For standalone quantities, give the relevant unit, scope, and source; do not invent a comparison baseline. Never manufacture precision.
- Prefer primary sources for material external claims. Attribute a vendor's estimate or claim to the vendor; a source link alone does not make the claim independently established.
- Put the decisive evidence into the section when a strong conclusion needs it. The reader should not have to open a link to discover the reasoning or a material limitation.
- Preserve uncertainty and counterevidence that could change the reader's decision. Do not turn a personal observation into a universal claim.

Use descriptive inline anchors. Add a title attribute only when the destination title adds context: `[anchor text](url "Title")`. Prefer stable official documentation, research papers, public incident reports, vendor security reports, and relevant established personal blogs. Choose sources for what they substantiate, not to meet a link quota.

For a historical event or well-documented attack, give the context needed for the current argument and link the primary source. Do not retell the full incident unless the analysis depends on those details.

## Choose Formatting for the Content

- Use bullets for genuinely parallel items of equal weight, and numbered lists for ordered steps. Keep list items grammatically parallel. Do not use lists as paragraph substitutes or repeat prose as a benefit list.
- Do not create runs of bolded-lead bullets. Use bold sparingly for a key term on first introduction, not to manufacture rhythm or emphasis in every paragraph.
- Use tables only for comparisons along structured dimensions, not to lay out prose.
- Use fenced code blocks for minimal, runnable configuration or code examples. Preserve technical correctness while editing the surrounding prose.
- Use genuine, attributed source quotations sparingly. Follow the existing Hugo `quote` shortcode convention where appropriate. Never turn an authored aphorism into a pull quote.
- Use a concrete comparison only when it explains a specific mechanism. Map it explicitly and return to technical language. Do not write metaphor equations, extend an analogy for decoration, or add an analogy to meet a quota.

## Hugo Page Bundles

Create articles at `content/post/<slug>/index.md`. Keep referenced media and documents in that bundle. Do not edit generated `public/` or `resources/` files.

Use `{{< ref "/post/<slug>/index.md" >}}` for internal article links. Confirm that the target exists and resolves. Verify local assets and document links as well as balanced shortcodes. Use the repository's existing shortcode syntax; inspect a working example before adding an unfamiliar shortcode.

Preserve valid existing front matter when editing. New articles use the following template with actual metadata and a real image path. Do not invent an asset or attribution to fill a field. Set dates deliberately, match existing category and tag names, and follow the requested publication state. `featured: true` is only for deliberate promotion; include `imageCredit` when attribution is required.

```yaml
---
title: "Full Article Title"
linkTitle: "Short Title for Navigation"
description: "One-sentence summary for SEO and social cards."
excerpt: "Same or similar to description."
lead: "Slightly longer hook for article listing pages."
slug: url-friendly-slug
image: featured-image.webp
# imageCredit:
#   name: "Creator name"
#   url: "https://example.com/source"
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
draft: false
weight: 50
categories: ["primary-category"]
tags: ["tag-1", "tag-2"]
featured: false
---
```

Replace sample values before delivery. `draft: false` represents a publication-ready article; use `true` when the assignment is to prepare an unpublished draft. Front matter summaries serve different surfaces and may overlap; the no-repetition rule does not require unrelated summaries of the same article.

For article file changes, verify metadata, bundle assets, internal references, shortcode balance, and quoted statistics against their sources. Run `hugo --minify` before delivery. If the changed article remains a draft, also build with drafts included so that the edited page is actually rendered. Inspect the rendered article when changing its visual presentation. A review-only assignment or a skill-documentation change does not require a site build.
