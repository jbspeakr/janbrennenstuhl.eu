#!/usr/bin/env bash
# Builds the browser search index (Pagefind) into public/pagefind/ from the built HTML. Run after Hugo;
# scripts/verify.sh does. Pages opt in with data-pagefind-body (layouts/page.html, glossary.html), so the
# index covers the same entries as catalog.json; scripts/check.py compares the two.
set -euo pipefail
cd "$(dirname "$0")/.."
PAGEFIND=${PAGEFIND:-pagefind}
if [[ -x .tools/pagefind ]]; then PAGEFIND="$PWD/.tools/pagefind"; fi
required=$(cat .pagefind-version)
"$PAGEFIND" --version | grep -Fq "$required" || { echo "Pagefind ${required} required, found: $("$PAGEFIND" --version 2>&1)" >&2; exit 1; }
rm -rf public/pagefind
# Navigation, tools and labels around the text are not content: a search for "copy" should not match every page.
"$PAGEFIND" --site public --output-subdir pagefind --quiet \
  --exclude-selectors ".toc, .cite, .related, .finding-tools, .heading-anchor, .series-nav, .guide-nav, .project-series, .byline, .eyebrow, .notice, .article-art, .glossary-index, .to-contents, button"
# Only the search API ships: the prebuilt UI components and the highlight helper are not used.
find public/pagefind -maxdepth 1 -type f \( -name 'pagefind-ui*' -o -name 'pagefind-modular-ui*' -o -name 'pagefind-component-ui*' -o -name 'pagefind-highlight.js' \) -delete
