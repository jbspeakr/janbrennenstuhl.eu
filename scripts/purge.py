#!/usr/bin/env python3
"""Purge the whole Bunny pull zone after a release, so the edge serves the new files at once.

    python3 scripts/purge.py    publish job, main-branch push only

Needs BUNNY_API_KEY (the account API key) and BUNNY_PULL_ZONE_ID.
API: https://docs.bunny.net/api-reference/core/pull-zone/purge-cache
"""
import os, re
from edge_rules import api

if __name__ == "__main__":
    if not (os.environ.get("FORGEJO_EVENT_NAME") == "push" and os.environ.get("FORGEJO_REF") == "refs/heads/main"):
        raise SystemExit("Purging the production pull zone requires a main-branch push")
    key, zone = os.environ["BUNNY_API_KEY"], os.environ["BUNNY_PULL_ZONE_ID"]
    if not re.fullmatch(r"\d+", zone):
        raise SystemExit("Invalid pull zone ID")
    api("POST", f"/pullzone/{zone}/purgeCache", key)
    print(f"Purged pull zone {zone}.")
