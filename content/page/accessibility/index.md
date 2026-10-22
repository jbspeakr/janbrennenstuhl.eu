---
title: Accessibility
slug: accessibility
description: The accessibility standard this site aims for, how it is tested, and how to report a barrier.
date: 2026-10-13
lastmod: 2026-10-14
---

This site aims to meet the [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/) at level AA. This statement describes what that means in practice and where it is known to fall short.

## What the site does

- Text and controls meet AA contrast in both the dark and the light theme. No text is set below 13 pixels.
- Everything works with a keyboard. A skip link leads to the content, focus is always visible, and search (also on <kbd>Ctrl</kbd> + <kbd>K</kbd> or <kbd>⌘</kbd> + <kbd>K</kbd>) announces its results.
- Pages work without JavaScript. Search falls back to a complete list, code and tables scroll inside their own focusable regions, and content reflows at 320 pixels and 200% zoom without horizontal scrolling.
- Explanatory diagrams have a text alternative and are followed by a prose description of what they show. The decorative drawing at the top of each page is hidden from screen readers. Interactive explainers come with a static explanation.
- Animations are short, never loop, and stop entirely when your system asks for reduced motion.
- A button in the header switches between the light and the dark theme. Your choice is stored only in your browser; without it, the site follows your system setting.
- Acronyms such as OIDC are linked to the [glossary]({{< ref "/page/glossary" >}}) and expanded on first use.

## How it is tested

Every change runs automated checks with axe-core on the main page types at 360, 768 and 1440 pixels in both themes, plus keyboard, reflow, text-spacing and no-JavaScript checks. Automated tools find only part of the problems. A manual pass with VoiceOver on Safari and NVDA on Firefox is part of the release checklist; the first full pass for this design is still to be done, and this statement will be updated when it is.

## Known limitations

- Talk slides are linked as PDFs that have not been checked for accessibility. Each talk has a written reading companion in HTML.

## Report a barrier

If something does not work for you, please tell me through the contact details on the [imprint]({{< ref "/page/imprint" >}}).
