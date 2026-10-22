#!/usr/bin/env bash
# Production build plus every static release gate. The artifact in public/ is what gets deployed.
set -euo pipefail
cd "$(dirname "$0")/.."
HUGO=${HUGO:-hugo}
if [[ -x .tools/hugo ]]; then HUGO="$PWD/.tools/hugo"; fi
required=$(cat .hugo-version)
"$HUGO" version | grep -Fq "v${required}" || { echo "Hugo ${required} required, found: $("$HUGO" version)" >&2; exit 1; }
revision=$(git rev-parse HEAD)
if [[ -n $(git status --porcelain) ]]; then revision="${revision}-dirty"; fi
rm -rf public
HUGO_PARAMS_SOURCE_REVISION="$revision" HUGO_INDEXNOW_KEY="${INDEXNOW_KEY:-}" "$HUGO" --minify --gc --cleanDestinationDir "$@"
python3 scripts/check.py
python3 -m unittest discover -s tests -p 'test_*.py'
if command -v node >/dev/null; then node --test tests/; else echo 'Node not found: edge-script tests skipped' >&2; fi
