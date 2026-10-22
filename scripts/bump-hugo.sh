#!/usr/bin/env bash
# Moves the pinned Hugo version: writes .hugo-version and the verified Linux checksum that
# scripts/bootstrap.sh checks in CI. Then run ./scripts/verify.sh with that Hugo installed locally
# before opening the PR. Usage: ./scripts/bump-hugo.sh 0.168.0
set -euo pipefail
cd "$(dirname "$0")/.."
version=${1:?usage: bump-hugo.sh <version>}
archive="hugo_extended_${version}_linux-amd64.tar.gz"
line=$(curl --fail --location --silent --retry 3 \
  "https://github.com/gohugoio/hugo/releases/download/v${version}/hugo_${version}_checksums.txt" | grep -F " ${archive}")
[[ -n $line ]] || { echo "No checksum for ${archive} in the v${version} release" >&2; exit 1; }
printf '%s\n' "$line" > scripts/hugo-linux-amd64.sha256
printf '%s\n' "$version" > .hugo-version
sed -i.bak -E "s/Hugo pinned to [0-9.]+/Hugo pinned to ${version}/" docs/IMPLEMENTATION.md && rm -f docs/IMPLEMENTATION.md.bak
printf 'Pinned Hugo %s. Now: install it locally, run ./scripts/verify.sh and npm run test:browser, then commit.\n' "$version"
