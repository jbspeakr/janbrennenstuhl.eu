#!/usr/bin/env bash
# Moves the pinned Pagefind version: writes .pagefind-version and the Linux checksum that
# scripts/bootstrap.sh checks in CI. Then run ./scripts/bootstrap.sh, ./scripts/verify.sh and
# npm run test:browser before opening the PR. Usage: ./scripts/bump-pagefind.sh 1.6.0
set -euo pipefail
cd "$(dirname "$0")/.."
version=${1:?usage: bump-pagefind.sh <version>}
archive="pagefind-v${version}-x86_64-unknown-linux-musl.tar.gz"
line=$(curl --fail --location --silent --retry 3 \
  "https://github.com/Pagefind/pagefind/releases/download/v${version}/${archive}.sha256")
[[ $line == *"${archive}"* ]] || { echo "No checksum for ${archive} in the v${version} release" >&2; exit 1; }
printf '%s\n' "$line" > scripts/pagefind-linux-amd64.sha256
printf '%s\n' "$version" > .pagefind-version
printf 'Pinned Pagefind %s. Now: ./scripts/bootstrap.sh, ./scripts/verify.sh and npm run test:browser, then commit.\n' "$version"
