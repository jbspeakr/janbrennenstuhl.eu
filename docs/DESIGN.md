# Trust Boundaries: design system

A calm, dark-first look for a site about systems, boundaries and the flows that cross them: graphite neutrals, desaturated support colours and one soft accent per view. Light is equal quality. Nothing shouts; the writing carries the page.

## Tokens

Defined once in `assets/css/site.css` as OKLCH pairs resolved by `light-dark()`. `:root[data-theme]` overrides the system choice; nothing else switches colour. The accent is a soft rose taken from the pink of the site icon; the neutrals sit next to the icon's graphite (`#212529`).

| Token | Dark | Light | Use |
| --- | --- | --- | --- |
| `--ground` | `oklch(21% 0.008 255)` | `oklch(98.7% 0.002 250)` | page |
| `--ground-2` | `oklch(23.5% 0.009 255)` | `oklch(96.3% 0.004 250)` | raised panels, drawing plate |
| `--ink` | `oklch(91% 0.005 255)` | `oklch(24% 0.01 255)` | text |
| `--ink-2` | `oklch(72% 0.01 255)` | `oklch(47% 0.012 255)` | secondary text |
| `--signal` | `oklch(78% 0.075 8)` | `oklch(52% 0.13 8)` | links in prose, focus, the one accent |
| `--boundary` | `oklch(76% 0.05 230)` | `oklch(48% 0.06 230)` | topic links, code keywords |
| `--threat` | `oklch(79% 0.075 70)` | `oklch(52% 0.1 60)` | warnings, failing verdicts |
| `--green` | `oklch(78% 0.06 155)` | `oklch(48% 0.07 155)` | reviewed state, code strings |

### Contrast (WCAG 2.x ratio)

Computed from the OKLCH values (sRGB, relative luminance). Every text pair passes AA at the sizes used; the lowest is light `--threat` on `--ground-2` at 5.1:1.

| Text on | dark ground | dark ground-2 | light ground | light ground-2 |
| --- | --- | --- | --- | --- |
| ink | 13.6 | 12.8 | 15.8 | 14.8 |
| ink-2 | 7.1 | 6.7 | 6.6 | 6.1 |
| signal | 8.6 | 8.1 | 5.7 | 5.3 |
| boundary | 8.3 | 7.9 | 6.2 | 5.8 |
| threat | 9.1 | 8.5 | 5.5 | 5.1 |
| green | 9.1 | 8.5 | 6.1 | 5.7 |

Meaning never rests on colour alone: findings carry IDs and labels, verdicts say "Meets"/"Fails".

## Type

- **Geist** (variable, 100–900, Latin subset, 26 kB woff2) for headings, UI and body; preloaded. Italic is a separate 27 kB file, fetched only when a page uses italics.
- **Geist Mono** (variable, 21 kB) for code, keyboard keys and finding IDs only. Labels, eyebrows, dates and table heads are set in Geist, sentence case, with tabular figures where numbers line up.
- Fallback `Geist Fallback` is Arial with `size-adjust: 104.71%`, `ascent-override: 95.98%`, `descent-override: 28.17%`, computed from both fonts' metrics, so the swap does not move text.
- Headings weight 600, tracking −0.015 to −0.03em. The home statement tops out at 3.75rem, article titles at 3.1rem. Body 17–18px, line height 1.7, 66-character measure. Nothing below 13px.
- Rules are 1px; accent bars (answer, findings) 2px.
- Fonts: OFL 1.1 (`static/fonts/OFL.txt`), Geist 1.7.2. File names carry the version so they can be cached immutably.

The header has one setting: a light/dark toggle. It follows the system until used, stores `{theme}` in `localStorage` under `jb-reader`, and is applied before first paint by the inline `assets/js/theme.js`.

## The drawing

`layouts/_partials/diagram.html` draws a deterministic, label-free SVG for any page. An MD5 of the page's ID and title (or a `seed`, such as a topic ID on topic pages) decides everything:

- 3–5 columns of nodes, 1–3 nodes per middle column and 1–2 at the ends, with small offsets;
- links so every node has a way in and out, drawn as thin neutral curves;
- one highlighted path, one node per column, in the page's tone, ending in a node with a soft halo;
- one dashed trust boundary around one or two neighbouring columns (never the first);
- the page's hue, one of eight (10, 55, 100, 150, 195, 235, 275, 320). Lightness and chroma are shared, so every hue is equally quiet.

So no two pages share a composition, and pages in the same topic no longer look alike. The drawing is always decorative (`aria-hidden`); explanatory figures use `figure-diagram` with a text alternative. Colours come from the tokens and `--h`, so the same SVG works in both themes. The highlighted path draws in once on load; under `prefers-reduced-motion` everything is static. The same `view-transition-name` on the home flagship and its article lets the drawing carry across the navigation (`@view-transition { navigation: auto; }`, CSS only). Article and flagship drawings sit inside the content width as a rounded plate, 4:1 on wide screens and 5:2 on narrow ones.

Social cards reuse it: `assets/cards/<topic>.png` are the topic drawings rendered once at 1200×630 in the dark theme; Hugo's `images.Text` writes the title (Geist Bold) and the topic label (Geist Mono) at build time. To regenerate the plates after changing the drawing or the palette: build, serve on port 8000, then run `node scripts/card-plates.cjs`.

## Layout

- **Home:** statement, flagship essay with full-width diagram, the Now strip, the index of all essays grouped by topic (table of contents, not cards), latest field-guide entries.
- **Article:** drawing, eyebrow (kind / topics / series), title, lead or short answer, byline with published, updated and reviewed dates; sticky table of contents on wide screens (collapsed above the text on narrow ones); key findings; body; series navigator; cite block (plain, APA, BibTeX); related.
- **Field-guide entry:** question title, short answer, key findings as `finding` blocks with anchors and "copy quote with link", evidence table, what to do for engineers and for product/UX, details, review status and change log.
- **Code:** filename caption, line highlighting via Hugo options, copy button, scrollable focusable region, palette-matched highlighting.
- **Search:** ⌘K / Ctrl+K command palette (loaded on demand) and `/search/` with type and topic filters; both use the same index. Without JS, `/search/` lists everything.

## Budgets

Compressed transfer, enforced by `scripts/check.py` (and Lighthouse in CI):

| Budget | Limit | Current |
| --- | --- | --- |
| CSS (one fingerprinted file) | 15 kB | 7.2 kB |
| JS on an article (site module; explainers only where used) | 8 kB | 1.3 kB |
| HTML per essay or guide entry | 30 kB | ~12 kB typical |
| Preloaded font | 35 kB | 26.4 kB |
| Inline diagram | 6 kB | ~2 kB |
| Third-party requests | 0 | 0 |

### LCP and the CSP

Lighthouse 13.5 (simulated mobile, gzip) scores 100 for performance, accessibility, best practices and SEO on home, an essay and a field-guide entry, with CLS 0 and TBT 0. LCP is 1.35–1.5 s, above the plan's 1.2 s. What remains is the round trip for the render-blocking stylesheet. Inlining critical CSS would remove it, but would need `style-src 'unsafe-inline'` or a per-build style hash at the edge. I kept the strict CSP; the Lighthouse gate allows 1.6 s. Revisit if field data (CrUX) shows a real problem.
