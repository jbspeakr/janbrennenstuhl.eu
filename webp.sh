#!/usr/bin/env bash
# Explicit, non-destructive conversion; source masters are never replaced.
set -euo pipefail
if [[ $# != 2 ]]; then printf 'Usage: %s source.png output.webp\n' "$0" >&2; exit 2; fi
case "$1" in *.png|*.jpg|*.jpeg) ;; *) printf 'Source must be PNG or JPEG.\n' >&2; exit 2;; esac
case "$2" in *.webp) ;; *) printf 'Output must be WebP.\n' >&2; exit 2;; esac
if [[ -e "$2" ]]; then printf 'Output already exists; choose a new filename.\n' >&2; exit 1; fi
cwebp -q 80 -m 6 -metadata none "$1" -o "$2"
