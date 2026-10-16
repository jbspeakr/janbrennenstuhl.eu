# janbrennenstuhl.eu: Review and Modernization Plan

Oct 13, 2026 · Jan Brennenstuhl

## Summary

The writing is strong; the site around it is a stock theme with a few real bugs. Main still runs Hugo Theme Stack v4 with a sidebar, widgets and card tiles that make a principal security engineer's blog look like every other Stack blog. The redesign branch fixed the engineering underneath but chose a quiet beige "editorial paper" look and wrapped a 45-page blog in a Python, Node and Hugo toolchain.

Five moves matter most, in this order:

1. **Stop the production risks this week.** The deploy workflow also runs on `pull_request`, so any same-repo PR uploads to BunnyCDN with `remove: true` and purges the zone. The JSON-LD on main is invalid (trailing commas, nested `@context`, a literal "CET" suffix on dates).
2. **Keep the redesign's plumbing, drop its look.** Owned templates, serialized JSON-LD, per-page Markdown, the content catalog and the safe deploy are worth merging. The beige theme, Georgia headings and Python social cards are not.
3. **Build one signature visual system** around the site's actual subject: trust boundaries, tokens and delegation. Generated diagrams per article, a real display typeface, and dark-first contrast instead of a paper palette.
4. **Make agents a designed audience,** not an export: `llms.txt` plus `llms-full.txt`, Markdown twins with content negotiation, a JSON Feed, stable citation anchors and an MCP-friendly catalog.
5. **Turn the knowledge base from link lists into a citable reference:** one claim-led entry per topic, key-findings boxes, quotable pull quotes with deep links, and a review date on every entry.

The roadmap at the end sequences this into five phases (0–4). Nothing here needs a framework change: Hugo stays, and the whole site should ship under 50 kB per page.

## Where main stands today

Main is a well-maintained Stack v4 starter with 35 posts, 11 knowledge-base pages and good recent writing. These are the findings, worst first.

| Area | Finding | Evidence | Severity |
| --- | --- | --- | --- |
| Release | Deploy job runs on `pull_request` as well as `push`, with `remove: true`, zone purge and IndexNow | `.forgejo/workflows/deploy.yml` | Critical |
| Release | Account-wide Bunny API key used for routine deploys; third-party actions pinned to tags, not commits | same file | High |
| SEO / agents | JSON-LD is invalid: trailing commas after objects, a second `@context` nested inside `@graph`, dates formatted with a hardcoded "CET" string, empty `inLanguage` (reads `languageCode`, which is unset) | `layouts/_partials/head/custom.html` | High |
| SEO / agents | Article `image` in JSON-LD is the bare front-matter filename, not an absolute URL; the breadcrumb's `index .Params.categories 0` fails the build for a post without a category | same file | Medium |
| Tooling drift | `AGENTS.md` says Hugo 0.161.1, CI installs 0.166.0; `go.mod` says Go 1.26, CI uses 1.27; module path is still `CaiJimmy/hugo-theme-stack-starter` | `AGENTS.md`, `go.mod`, workflow | Medium |
| Performance | Lato loaded by injecting a stylesheet from fonts.bunny.net with JavaScript, so text reflows after load; Plausible inline script; Stack ships its own JS bundle | `custom-font.html`, `custom.html` | Medium |
| Content hygiene | 2.7 MB `account-security.png` committed next to its 269 kB WebP; two KB pages are draft stubs with only bare links (`oidc/tokens`, `oidc/step-up-authentication`); `type: docs` front matter left over from an older theme | content tree | Low |
| Taxonomy | Five categories with SEO-written descriptions ("Fortify your digital presence…") that also feed `llms.txt` verbatim | `content/categories/*/_index.md`, live `llms.txt` | Medium |
| Discovery | Homepage paginates at 5 posts; categories, tags, archives and search are four overlapping ways to browse | `config.toml`, live sidebar | Medium |
| Markup | `goldmark.renderer.unsafe = true` and math passthrough enabled with `math = false` | `markup.toml`, `params.toml` | Low |

What already works: CC BY 4.0 licensing, an `llms.txt` output format, `security.txt`, full-content RSS, IndexNow, EU hosting, and a writing skill in `.agents/` that keeps the voice consistent.

The knowledge base is the weakest part. Its two sections hold 9 published pages; most are an intro paragraph plus a list of papers, each ending in "→ Read the Paper (.pdf)". There is no claim per page, no summary of what the studies agree on, no review date, and nothing short enough to quote.

## Why the redesign branch falls short

The redesign is good engineering aimed at the wrong target. It optimizes for auditability and caution; you asked for something exciting and first-class. Its single commit (13 Oct 2026) replaces Stack with owned templates, which is the right call, then stops short in three ways.

**It looks like a template, just a different one.** Warm paper `#f6f3ed`, graphite text, one raspberry accent, Georgia for headings and `system-ui` for everything else. That is the default "editorial minimal" look of 2019–2023 and reads closer to a literary magazine than a security engineer's lab. There is one piece of original art (a delegation illustration) reused on the homepage and one article; every other article has either its old stock WebP hero or nothing. Social cards are Pillow-rendered DejaVu Serif on beige.

**The type has no voice.** No display face, no variable fonts, no optical sizing; headings depend on whatever Georgia renders on each OS. Small UI text is set at 10–13 px (nav 13 px, eyebrows and tags 10–11 px mono), which hurts legibility and makes the page feel timid.

**The toolchain outgrew the site.** A 45-page static blog now needs Hugo, a Python venv (`build.py`, `deploy.py`, `verify.py`, `social_cards.py` and five more scripts), Node with Playwright and axe, and 1.1 MB of committed DejaVu fonts. Markdown export works by converting rendered HTML back to Markdown in Python, which is fragile and duplicates what Hugo's own output formats can do. Writing a post should not require reading `CONTENT-CONTRACT.md` and adding `id`, `kind`, `status` and `reviewStatus` by hand.

**Keep these from the branch:**

- Owned Hugo templates and no theme dependency
- Serialized JSON-LD via `dict … | jsonify` instead of hand-written JSON
- Per-page Markdown, `content-index.json` catalog, cite-and-share block, heading anchors
- The three-job Forgejo workflow: verify, browser test, publish only from `main`, no account-wide API key, no deletes
- The budgets (CSS ≤ 25 kB, JS ≤ 15 kB gzip, no third-party scripts) and the axe browser matrix
- Topic hubs, projects and talks sections, a real 404

**Drop or replace:** the paper palette and Georgia, the Python Markdown converter (use a Hugo output format), Python social cards (use Hugo's image `Text` filter or a build-time SVG), the committed DejaVu fonts, and most of the manual front-matter contract (derive `kind` from section, `id` from the path).

## Technical foundation

One tool builds the site: Hugo. Everything the redesign does in Python moves into Hugo templates, output formats and render hooks, so a fresh clone builds with `hugo` and nothing else.

**Stack**

- Hugo extended, pinned once in a `.hugo-version` file that CI, `AGENTS.md` and local dev all read. Drop `go.mod` entirely once Stack is gone.
- CSS: plain modern CSS through Hugo Pipes (`css.Build` or `resources.Concat` + `minify` + `fingerprint`). Native nesting, `@layer`, container queries, `light-dark()`, `color-mix()` and OKLCH colors replace SCSS.
- JS: a few ES modules built with `js.Build` (esbuild, already inside Hugo). No framework, no npm runtime dependency.
- Node only as a dev dependency for the browser test job (Playwright + axe), never needed to write or build.

**Content model**

- Derive what can be derived. `kind` comes from the section, `id` from the bundle path, `topics` from a small mapping of tags. Authors write `title`, `description`, `date`, `tags` and an optional `reviewed` date, nothing else.
- Collapse categories and tags into one taxonomy of about 6 topics (Agentic engineering, Identity & auth, AppSec, Passwords, Tokens & JWT, Engineering practice). Rewrite their descriptions for humans; they feed `llms.txt`.
- Add `series` for multi-part writing (JWT, passwords, agentic AppSec) and render a series navigator.
- Use render hooks for links (mark external links, validate internal ones at build), images (responsive `srcset`, AVIF + WebP, width and height always set), headings (stable anchors) and code blocks (copy button, filename, highlighted lines).
- Shortcodes, each with a Markdown and RSS rendering: `finding` (a quotable claim with a citation ID), `figure-diagram`, `study` (paper, year, sample size, key result), `callout`, `details`.

**Release**

- Take the redesign's three-job workflow as is: build once, test the artifact, publish the same bytes only from `main`.
- Add a staging pull zone that PR builds deploy to, with a preview URL posted on the PR.
- Pin third-party actions to commit SHAs. Keep the account API key for the post-deploy pull zone purge, available only to the `main`-only publish job.
- Bunny edge rules: HTML/Markdown/JSON revalidate (`max-age=0, must-revalidate`, 5-minute edge TTL); fingerprinted assets `max-age=31536000, immutable`; real 404 status; 301s for old aliases; HSTS, CSP (report-only first), `Referrer-Policy`, `Permissions-Policy`.

**Quality gates in CI**

- Build fails on broken internal links, missing `alt`, missing `description`, invalid JSON-LD (validate with a schema check) and budget overruns.
- Lighthouse CI on 3 representative routes with assertions (performance 100, accessibility 100, LCP < 1.2 s on simulated mobile).
- Markdown lint and a spell check with a security-terms dictionary.

## Visual direction: "Trust Boundaries"

The site should look like the subject it covers: systems, boundaries and the flows that cross them. The working name for the direction is **Trust Boundaries**, a dark-first, high-contrast technical look with one signature device, the generated boundary diagram.

**Signature device: a generated diagram for every article.** Each post gets a deterministic SVG cover drawn by a Hugo partial from its title hash and topic: a few nodes, dashed trust-boundary rectangles, and token flows crossing them. Agentic posts draw delegation chains, password posts draw credential stores and attackers, JWT posts draw issuer, holder and verifier. Same grammar everywhere, so the site is recognizable from a thumbnail. The SVG is inline (a few kB, no request), animates its flows once on load with a scroll-driven animation, and is static under `prefers-reduced-motion`. Hand-drawn diagrams for flagship posts use the same grammar.

**Type with a voice.** Two self-hosted variable fonts, subset to Latin, about 60 kB in total:

- **Geist** for headings, UI and body. Headings set big and tight (clamp 44–96 px, weight 700–800, tracking −0.035em); body at 18–19 px with a 66-character measure.
- **Geist Mono** for code, metadata, eyebrows, citation IDs and the diagram labels, at no less than 13 px.

Alternative if you want more contrast: **Newsreader** (variable, optical sizes) for long-form body with Geist for display and UI. Either way, no system-font headings.

**Color.** Dark is the default, light is equal quality, both defined in OKLCH with `light-dark()`:

| Token | Dark | Light | Use |
| --- | --- | --- | --- |
| Ground | near-black blue, oklch(16% 0.02 260) | warm white, oklch(98.5% 0.005 90) | page |
| Ink | oklch(94% 0.01 260) | oklch(22% 0.02 260) | text |
| Signal | electric amber, oklch(82% 0.17 75) | deep amber, oklch(55% 0.16 60) | links, focus, the one accent per view |
| Boundary | cyan, oklch(78% 0.11 210) | teal, oklch(48% 0.09 210) | diagram boundaries, topic chips |
| Threat | coral, oklch(70% 0.17 25) | oklch(52% 0.18 25) | attacker paths in diagrams, warnings |

All text pairs must reach WCAG AA at the sizes used; Signal on Ground is the brand moment, used sparingly.

**Layout.**

- **Home as a lab index.** A one-line statement set huge ("Security that makes the secure path the easy one."), the latest flagship essay with its diagram at full width, then a dense, scannable index of all writing grouped by topic, like a table of contents, not a card grid. A "Now" strip carries the Agentic Identity Broker, recent talks and the HTW lecture.
- **Articles.** Full-bleed diagram header; a Key findings box under the title (3 claims, each linkable); 66-character column; sidenotes for sources and footnotes on wide screens, inline on mobile; a sticky reading-progress table of contents; pull quotes with a "copy quote with link" action; series navigator at the end.
- **Code blocks** with filename tabs, highlighted lines, a copy button and a theme matched to the palette.

**Motion and polish.** Cross-page View Transitions (`@view-transition { navigation: auto; }`, CSS only) so the diagram morphs from index to article; scroll-driven reveal of diagram flows; hover states that draw the token path under a link. All motion off under reduced motion, nothing that blocks reading.

**Social cards** come from the same diagram grammar: Hugo's image filters (`images.Text` over a per-topic base PNG) render 1200×630 cards at build time, no Python.

Before committing to code, I'd mock three screens (home, a long article, a KB entry) in both themes and pick the type pairing from those.

## Performance

Target: every page fully usable from the first HTML response, under 50 kB compressed before images, LCP under 1 s on a mid-range phone in the EU. The redesign's lab numbers (home 31 kB, article 48 kB, Lighthouse 100) show this is reachable; I could not run Lighthouse against the live Stack site from here, so main's baseline still needs measuring.

| Budget | Limit (compressed) |
| --- | --- |
| HTML per article | 30 kB |
| CSS, inlined critical + one fingerprinted file | 15 kB |
| JS, all modules on an article | 8 kB |
| Fonts, preloaded body face only | 35 kB |
| Hero diagram (inline SVG) | 6 kB |
| Third-party requests | 0 |

How to get there:

- **Inline critical CSS** for the first view and load the rest normally; no render-blocking font CSS from a third party.
- **Self-host fonts** with `font-display: swap`, a `size-adjust` fallback metric so swapping causes no layout shift, and `<link rel=preload>` for the body face only.
- **Images** through a render hook: AVIF with WebP fallback, `srcset` at 480/960/1440, explicit `width`/`height`, `loading=lazy` and `decoding=async` below the fold, `fetchpriority=high` on the LCP image. Delete source PNGs that have WebP twins.
- **Speculation Rules** (`<script type=speculationrules>` with `prerender` on hover for same-site links), so next-page navigation is near-instant in Chromium; harmless elsewhere.
- **Compression and caching** at Bunny: Brotli, long immutable cache for fingerprinted assets, revalidation for HTML.
- **Search** loads only on `/search/` or when the command palette opens. At 45 entries the redesign's 133 kB single index is fine; switch to Pagefind's chunked index past roughly 150 entries.
- **Analytics:** if you want numbers, keep Plausible but load it as a deferred external script from your own domain via a Bunny edge rule, or switch to server-side Bunny logs. No inline script either way, so CSP stays strict.
- **Field data:** add a tiny `web-vitals` beacon only if you want real p75 LCP/INP/CLS; otherwise rely on CrUX once traffic qualifies.

## Accessibility

The goal is WCAG 2.2 AA, verified by people as well as tools. A boldly dark, diagram-heavy design is where accessibility usually slips, so these rules are part of the design, not a later audit.

- **Contrast** checked for every token pair in both themes (APCA as a second check for thin weights); no text under 13 px; the amber accent never carries meaning alone.
- **Diagrams** have `role=img`, a title, and a prose equivalent directly under them ("What this shows"). Flows are also listed as steps for screen readers.
- **Keyboard:** skip link, visible 3 px focus ring in Signal, logical tab order through TOC, sidenotes and copy buttons; the command palette (⌘K / Ctrl+K) is fully keyboard-operated and announces results with `aria-live`.
- **Motion:** every animation and the view transitions respect `prefers-reduced-motion`; nothing autoplays.
- **Reading comfort:** a reader-settings popover with text size, line height and a light/dark/system choice, stored locally; content reflows at 320 px and at 200% zoom without horizontal scroll.
- **Structure:** one `h1`, no skipped heading levels (lint at build), landmarks, `lang` set, link text that makes sense alone, `abbr` with expansions for OIDC, JWT, JWE and other acronyms on first use.
- **Code and tables** scroll inside focusable regions with labels (the redesign already does this).
- **Media:** the HTW talk and future talks get a transcript or detailed reading companion; slides PDFs get an HTML summary.
- **Testing:** keep the redesign's axe × viewport × theme matrix in CI, and do one manual pass with VoiceOver/Safari and NVDA/Firefox before launch. Publish an accessibility statement page.

## Agents as first-class readers

An agent should be able to find, read, quote and cite any page without parsing HTML. Today `llms.txt` lists 4 featured posts with SEO copy and nothing else is machine-readable beyond RSS and broken JSON-LD.

| Surface | What it serves | How in Hugo |
| --- | --- | --- |
| `/llms.txt` | Who you are, the 6 topics, every article with a one-sentence claim and its `.md` link, where the feeds and catalog are | rewrite `home.llms.txt` to range all pages, not only `featured` |
| `/llms-full.txt` | The whole corpus as one Markdown file, newest first | second plain-text output format on home |
| `/<slug>/index.md` | Each page as clean Markdown with YAML front matter (title, author, dates, license, canonical URL, topics) | a Markdown output format using `.RenderShortcodes`, with `.md` variants of each shortcode, instead of the redesign's HTML-to-Markdown Python step |
| Content negotiation | `Accept: text/markdown` on any URL returns the twin | Bunny edge rule or Edge Script; plus `<link rel="alternate" type="text/markdown">` in every head |
| `/catalog.json` | Versioned index: id, URLs, dates, review date, topics, license, content hash | keep the redesign's `home.catalog.json` |
| `/findings.json` | Every quotable finding with its text, anchor URL, source article and supporting citations | collected from the `finding` shortcode via `.Store` |
| Feeds | Full-content Atom/RSS plus JSON Feed 1.1, per topic as well as site-wide | output formats on home and taxonomy terms |
| JSON-LD | `BlogPosting` / `TechArticle` with `citation`, `about` topics, `isPartOf` series, `license`; `Person` with `knowsAbout` | serialized with `jsonify`, validated in CI |
| Scholar tags | `citation_title`, `citation_author`, `citation_publication_date`, `citation_pdf_url` meta | head partial; Zotero and Google Scholar pick these up |
| Discovery | `/.well-known/api-catalog` (RFC 9727 linkset) pointing to feeds, catalog and `llms.txt` | static file |
| Usage policy | `robots.txt` with an explicit choice per AI crawler; `/.well-known/tdmrep.json` for the EU text-and-data-mining opt-in or reservation | static files |

Two things make the site more than readable for agents:

1. **Stable, quotable units.** Every heading and every finding gets a permanent anchor (`#f-pw-reuse-43pct`). An agent quoting "43–51% of users reuse passwords" can link straight to the sentence, and the catalog tells it when that page was last reviewed.
2. **An optional read-only MCP server** (later phase) on a Bunny Edge Script: `search`, `get_article`, `get_findings`, `list_topics`, backed by the same JSON files. Fitting for someone who builds agent identity infrastructure, and a good talk demo.

CI checks that every HTML page has its Markdown twin, that every `llms.txt` link resolves, and that Markdown contains no raw shortcode syntax.

The CC BY 4.0 license already allows reuse with attribution; decide once whether training crawlers are welcome and state it in `robots.txt` and `tdmrep.json` so the policy is explicit rather than implied.

## Evolving the knowledge base

Turn the knowledge base from reading lists into a **field guide**: short, claim-led reference entries that the essays link to and that people and agents quote. Each entry answers one question, shows the evidence, and says when it was last checked.

**Every entry has the same shape:**

1. **The question as the title.** "How common is password reuse?" instead of "Password Reuse Studies".
2. **The answer in two sentences,** written to be quoted on its own.
3. **Key findings,** 3–5 numbered claims, each a `finding` with its own anchor, source and a "copy quote with link" button.
4. **Evidence table** built from `study` shortcodes: study, year, sample, method, result, link.
5. **What to do,** split for engineers and for product/UX, linking the relevant essays.
6. **Footer:** reviewed date, what changed since the last review, Cite this (plain, BibTeX, APA), and the Markdown twin.

**Example, the password reuse page rewritten:**

> **How common is password reuse?** Roughly half of users reuse the same password across sites, and partial reuse with small tweaks makes it worse. A leaked password, even a different one, gives attackers a far better guessing start on other sites.

| Study | Year | Sample | Finding |
| --- | --- | --- | --- |
| Princeton & Indiana University | 2014 | several hundred thousand leaked passwords + survey | 43–51% reuse the same password across sites |
| Michigan State University | 2016 | user study | each password reused on 1.7–3.4 sites; frequently typed, complex passwords are reused most |
| Carnegie Mellon, Google, ICSI | not on page | 154 participants, avg 147 days | reuse more common than previously believed once partial reuse counts |
| Microsoft Research | 2007 | ~500,000 users, 3 months | first large-scale study; many weak, reused, forgotten passwords |

Every number above already exists on the current page; the rewrite only moves it into a shape people can scan and cite.

**Scope changes:**

- Rename the section to **Field Guide** (or "Reference") and move it to the main navigation next to Writing.
- Fill or delete the two draft stubs (`oidc/tokens`, `oidc/step-up-authentication`); a stub with two Auth0 links should not be public.
- Add a third area where your current work is: **Agent identity**, covering delegation vs robot accounts, OAuth 2.0 Token Exchange (RFC 8693), consent and revocation, MCP authorization. The Agentic Identity Broker essay and talk become its anchor sources.
- A **glossary** of 40–60 terms (OIDC, PKCE, JWE, step-up, credential stuffing…) as `DefinedTerm` pages; terms auto-link on first use in essays with an accessible tooltip.

**Making it engaging without a chatbot:**

- One small interactive explainer per area, progressively enhanced and fully readable without JS: a JWT anatomy viewer (paste a token, see header, claims and signature parts, decoded locally), a password policy checker against NIST SP 800-63B, a delegation-flow stepper for the broker.
- A **finding card** per key finding, rendered at build as a 1200×630 image, so sharing a single claim on Mastodon or LinkedIn carries its source.
- A "changes" feed for the field guide, so readers and agents see when guidance was reviewed or revised.
- A plain-language summary toggle on the denser entries, for non-specialist readers such as product managers.

## Feature gaps

The gaps below are what a reader of a top-tier engineering blog expects and does not find today, ranked by value for effort.

| Feature | Why it matters | Effort |
| --- | --- | --- |
| Topic hubs (6) replacing categories + tags | One clear way to browse; each hub opens with a short essay and its best entry points | M |
| Series navigation | JWT, passwords and agentic AppSec are already series in all but name | S |
| Command palette search (⌘K) with type and topic filters | Fast keyboard access; reuses the redesign's search index | M |
| Newsletter by email, via an EU-hosted provider or self-hosted listmonk | RSS alone loses most readers; your audience is practitioners | S |
| Projects and Talks pages | The broker, HTW lecture and AGNTCon talk are currently hidden in posts | S (redesign has them) |
| Cite this + copy quote with link | Makes essays and findings quotable | S |
| Updated-on and reviewed-on dates, with an "outdated" banner for posts older than ~5 years on fast-moving topics | Security advice ages; readers need to know | S |
| Webmentions or Mastodon replies as comments | Discussion without a tracking comment widget; fits your fediverse presence | M |
| Real 404 with search, and 301s for old URLs | Trust and SEO | S |
| "Now" page and a short speaker bio with headshot | Conference organizers look for this | S |
| Print stylesheet and reader settings | Long technical essays get printed and read offline | S |
| German summaries or translations for selected pieces | Optional; HTW and EU audience | L |

Not recommended: an on-site chatbot, comments with accounts, a service worker. They add risk and weight without helping the reading experience.

## Roadmap

Safety first, then the foundation, then the look, then agents and the field guide. Phase 0 is small enough to do this week; each later phase opens only when its gate passes.

| Phase | Scope | Gate |
| --- | --- | --- |
| 0 · Make it safe (now) | Deploy only from main; pin actions to commit SHAs; keep the Bunny account key out of PR builds. Fix main's JSON-LD; unpublish the two KB stubs; delete the 2.7 MB PNG | No pull request can reach production |
| 1 · Own the foundation | Merge the redesign's templates, JSON-LD, catalog and workflow; drop its Python and its look. Hugo-only Markdown output; 6 topics; render hooks; Bunny cache, CSP and 404 rules; CI gates | All 147 old routes resolve, Lighthouse 100, zero axe findings |
| 2 · Trust Boundaries visual system | Mock home, article and field-guide entry in both themes; pick the fonts; build the tokens. Diagram partial, new templates, social cards, view transitions, command palette | Your design sign-off and a manual screen-reader pass |
| 3 · Agents and the field guide | llms.txt and llms-full.txt, Markdown twins with negotiation, findings.json, JSON Feed. Rewrite 3 KB entries in the new shape; add the Agent identity area and the glossary | An agent can cite any finding by URL; Markdown parity checks pass |
| 4 · Ongoing | Remaining KB entries, interactive explainers, newsletter, webmentions, read-only MCP server | — |

Phases 2 and 3 can overlap once Phase 1 is merged, because the agent outputs and the KB rewrite do not depend on the final visual design.

**Phase 0 checklist**

- [ ] Remove `pull_request` from the deploy trigger, or split build and publish so PRs only build
- [ ] Pin third-party actions to commit SHAs; keep `ACCOUNT_API_KEY` for the cache purge, used only by the `main`-only deploy job
- [ ] Replace the hand-written JSON-LD with a `dict … | jsonify` version (the redesign's `head.html` is a ready start)
- [ ] Set `draft: true` on `oidc/step-up-authentication` or fill it; delete `account-security.png`
- [ ] Align the Hugo version in `AGENTS.md`, CI and a `.hugo-version` file

Sources: the [main branch](https://codeberg.org/brennenstuhl/janbrennenstuhl.eu) at commit bc528e7, the [redesign branch](https://codeberg.org/brennenstuhl/janbrennenstuhl.eu/src/branch/redesign) and its `docs/` folder, and the live [janbrennenstuhl.eu](https://www.janbrennenstuhl.eu) including [llms.txt](https://www.janbrennenstuhl.eu/llms.txt), read on 13 Oct 2026.

## Addendum, 15 October 2026: gaps and decisions

A second review found the plan silent on operations after launch and on the processes it asserted. Decisions taken and where they now live in the repository:

- **Licence:** CC BY 4.0 governs, training included; no TDM reservation (`docs/DECISIONS.md`, `robots.txt`, `tdmrep.json`, `/agents/`).
- **Analytics:** Plausible stays as the one third-party request, production host only, with its CSP allowance documented (`docs/DECISIONS.md`, `docs/DELIVERY.md`).
- **Not doing:** newsletter, webmentions, external monitoring, Bunny config as code, a CSP report collector (deferred).
- **Editorial process:** review cadence and `lastmod` policy in `docs/CONTENT-CONTRACT.md`; `scripts/review-queue.py` lists what is due; `scripts/links.py` checks external sources monthly (`links` workflow).
- **Launch:** `docs/LAUNCH.md` is the cutover checklist.
- **Upkeep:** `scripts/bump-hugo.sh` and `renovate.json`; search index budget of 200 kB in `check.py`; screenshots uploaded from the browser job for design review; the HTW lecture listed under Speaking.
