#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -x .tools/hugo ]]; then export HUGO="$PWD/.tools/hugo"; fi
.venv/bin/python scripts/build.py "$@"
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
