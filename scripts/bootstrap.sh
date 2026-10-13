#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Python 3.11+; Hugo's exact version is the only runtime binary dependency.
python3 -c 'import sys; assert sys.version_info >= (3,11), "Python 3.11+ required"'
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt
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
printf 'Ready. Run ./scripts/verify.sh\n'
