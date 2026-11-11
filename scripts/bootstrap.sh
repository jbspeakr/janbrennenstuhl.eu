#!/usr/bin/env bash
# Installs the build tools: Hugo extended (.hugo-version) and Pagefind (.pagefind-version).
# Release scripts and checks use only the Python 3.11+ standard library.
set -euo pipefail
cd "$(dirname "$0")/.."
required=$(cat .hugo-version)
if command -v hugo >/dev/null && hugo version | grep -Fq "v${required}"; then
  printf 'Using installed Hugo %s\n' "$required"
elif [[ $(uname -s) == Linux && $(uname -m) == x86_64 ]]; then
  mkdir -p .tools
  archive="hugo_extended_${required}_linux-amd64.tar.gz"
  curl --fail --location --retry 3 "https://github.com/gohugoio/hugo/releases/download/v${required}/${archive}" -o ".tools/${archive}"
  (cd .tools && sha256sum -c ../scripts/hugo-linux-amd64.sha256)
  tar -xzf ".tools/${archive}" -C .tools hugo
else
  printf 'Install Hugo extended %s for your platform, then rerun this command.\n' "$required" >&2
  exit 1
fi
# Pagefind builds the browser search index from the rendered pages (scripts/search-index.sh).
pagefind=$(cat .pagefind-version)
if command -v pagefind >/dev/null && pagefind --version | grep -Fq "$pagefind"; then
  printf 'Using installed Pagefind %s\n' "$pagefind"
elif [[ $(uname -s) == Linux && $(uname -m) == x86_64 ]]; then
  mkdir -p .tools
  archive="pagefind-v${pagefind}-x86_64-unknown-linux-musl.tar.gz"
  curl --fail --location --retry 3 "https://github.com/Pagefind/pagefind/releases/download/v${pagefind}/${archive}" -o ".tools/${archive}"
  (cd .tools && sha256sum -c ../scripts/pagefind-linux-amd64.sha256)
  tar -xzf ".tools/${archive}" -C .tools pagefind
else
  printf 'Install Pagefind %s for your platform (https://pagefind.app/docs/installation/), then rerun this command.\n' "$pagefind" >&2
  exit 1
fi
python3 -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ is needed for the checks"'
printf 'Ready. Run ./scripts/verify.sh\n'
