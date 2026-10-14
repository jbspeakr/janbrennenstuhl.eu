# Trust Boundaries: design system

A dark-first, high-contrast technical look for a site about systems, boundaries and the flows that cross them. Light is equal quality. One accent per view.

## Tokens

Defined once in `assets/css/site.css` as OKLCH pairs resolved by `light-dark()`. `:root[data-theme]` overrides the system choice; nothing else switches colour.

| Token | Dark | Light | Use |
| --- | --- | --- | --- |
| `--ground` | `oklch(16% 0.02 260)` | `oklch(98.5% 0.005 90)` | page |
| `--ground-2` | `oklch(20% 0.025 260)` | `oklch(95.5% 0.008 90)` | raised panels, diagram plate |
| `--ink` | `oklch(94% 0.01 260)` | `oklch(22% 0.02 260)` | text |
| `--ink-2` | `oklch(76% 0.02 260)` | `oklch(45% 0.02 260)` | secondary text |
| `--signal` | `oklch(82% 0.17 75)` | `oklch(50% 0.14 58)` | links in prose, focus, the one accent |
| `--boundary` | `oklch(78% 0.11 210)` | `oklch(47% 0.09 215)` | trust boundaries, topic labels |
| `--threat` | `oklch(72% 0.16 25)` | `oklch(50% 0.18 25)` | attacker paths, warnings |
| `--green` | `oklch(80% 0.12 150)` | `oklch(46% 0.12 150)` | reviewed state, code strings |

### Contrast (WCAG 2.x ratio)

Computed from the OKLCH values (sRGB, relative luminance). Every text pair passes AA at the sizes used; the lowest is light `--signal` on `--ground-2` at 5.5:1.

| Text on | dark ground | dark ground-2 | light ground | light ground-2 |
| --- | --- | --- | --- | --- |
| ink | 16.3 | 15.2 | 16.6 | 15.2 |
| ink-2 | 9.0 | 8.4 | 7.1 | 6.5 |
| signal | 10.7 | 10.0 | 6.0 | 5.5 |
| boundary | 10.1 | 9.4 | 6.3 | 5.7 |
| threat | 7.3 | 6.8 | 6.3 | 5.8 |
| green | 10.9 | 10.1 | 6.5 | 5.9 |

Meaning never rests on colour alone: findings carry IDs and labels, verdicts say "Meets"/"Fails", threat paths have text labels.

## Type

- **Geist** (variable, 100–900, Latin subset, 26 kB woff2) for headings, UI and body; preloaded. Italic is a separate 27 kB file, fetched only when a page uses italics.
- **Geist Mono** (variable, 21 kB) for code, metadata, eyebrows, finding IDs and diagram labels.
- Fallback `Geist Fallback` is Arial with `size-adjust: 104.71%`, `ascent-override: 95.98%`, `descent-override: 28.17%`, computed from both fonts' metrics, so the swap does not move text.
- Headings 700–780, tracking −0.02 to −0.045em; the home statement scales to 6rem. Body 18–19px, line height 1.65, 66-character measure. Nothing below 13px.
- Fonts: OFL 1.1 (`static/fonts/OFL.txt`), Geist 1.7.2. File names carry the version so they can be cached immutably.

Reader settings (header "Aa") change theme, text size (93.75/100/112.5%) and line height (1.65/1.85). They are stored in `localStorage` under `jb-reader` and applied before first paint.

## The diagram

`layouts/_partials/diagram.html` draws a deterministic SVG for any page. The page's primary topic picks the grammar; an MD5 of its ID and title varies node heights, boundary padding, curve lift, the threat's position and the plate number (`TB-XXXX`).

| Topic | Nodes and flows | Boundaries | Threat |
| --- | --- | --- | --- |
| Agentic engineering | user → agent → gateway → tool, gateway ↔ broker | agent runtime, platform | injection |
| Identity & auth | user → client → IdP, IdP → client (tokens), client → API | issuer, resource | replay |
| AppSec | code → pipeline → platform → prod | paved road | dependency |
| Passwords | user → login → hash store, manager → login | account system | stuffing |
| Tokens & JWT | issuer → holder → verifier, issuer → verifier (JWKS) | signing keys, verify | forged |
| Engineering practice | client → edge → service → data | EU region | none |

Colours come from the tokens, so the same SVG works in both themes. Flows draw in once on load (staggered `stroke-dashoffset`), the threat fades in; under `prefers-reduced-motion` everything is static. Article headers render it with `role="img"` and a title; on the home page and in cards it is decorative. The same `view-transition-name` on the home flagship and its article lets the drawing carry across the navigation (`@view-transition { navigation: auto; }`, CSS only).

Social cards reuse it: `assets/cards/<topic>.png` are the diagram plates rendered once at 1200×630 in the dark theme; Hugo's `images.Text` writes the title (Geist Bold) and the topic label (Geist Mono) at build time. To regenerate the plates after changing the grammar or the palette: build, serve on port 8000, then run `node scripts/card-plates.cjs`.

## Layout

- **Home:** statement, flagship essay with full-width diagram, the Now strip, the index of all essays grouped by topic (table of contents, not cards), latest field-guide entries.
- **Article:** diagram header, eyebrow (kind / topics / series), title, lead or short answer, byline with published, updated and reviewed dates; sticky table of contents on wide screens (collapsed above the text on narrow ones); key findings; body; series navigator; cite block (plain, APA, BibTeX); related.
- **Field-guide entry:** question title, short answer, key findings as `finding` blocks with anchors and "copy quote with link", evidence table, what to do for engineers and for product/UX, details, review status and change log.
- **Code:** filename caption, line highlighting via Hugo options, copy button, scrollable focusable region, palette-matched highlighting.
- **Search:** ⌘K / Ctrl+K command palette (loaded on demand) and `/search/` with type and topic filters; both use the same index. Without JS, `/search/` lists everything.

## Budgets

Compressed transfer, enforced by `scripts/check.py` (and Lighthouse in CI):

| Budget | Limit | Current |
| --- | --- | --- |
| CSS (one fingerprinted file) | 15 kB | 7.6 kB |
| JS on an article (site module; explainers only where used) | 8 kB | 1.6 kB |
| HTML per essay or guide entry | 30 kB | ~12 kB typical |
| Preloaded font | 35 kB | 26.4 kB |
| Inline diagram | 6 kB | ~2 kB |
| Third-party requests | 0 | 0 |

### LCP and the CSP

Lighthouse 13.5 (simulated mobile, gzip) scores 100 for performance, accessibility, best practices and SEO on home, an essay and a field-guide entry, with CLS 0 and TBT 0. LCP is 1.35–1.5 s, above the plan's 1.2 s. What remains is the round trip for the render-blocking stylesheet. Inlining critical CSS would remove it, but would need `style-src 'unsafe-inline'` or a per-build style hash at the edge. I kept the strict CSP; the Lighthouse gate allows 1.6 s. Revisit if field data (CrUX) shows a real problem.
