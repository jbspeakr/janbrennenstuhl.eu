#!/usr/bin/env bash
# Draws the social-card plates (assets/cards/pages/<id>.png) from a throwaway build, so the real
# build can write titles onto them. Needs Node and Playwright's Chromium; run before verify.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
HUGO=${HUGO:-hugo}
if [[ -x .tools/hugo ]]; then HUGO="$PWD/.tools/hugo"; fi
port=${PORT:-8000}
rm -rf assets/cards/pages
"$HUGO" --minify --cleanDestinationDir --quiet
python3 scripts/serve.py "$port" >/dev/null 2>&1 &
server=$!
trap 'kill "$server"' EXIT
for _ in $(seq 50); do curl -fs "http://127.0.0.1:$port/" >/dev/null && break; sleep 0.1; done
PORT="$port" PLATES=pages node scripts/card-plates.cjs
