#!/usr/bin/env python3
"""Bunny edge rules from edge/rules.toml and the built /redirects.json.

    python3 scripts/edge_rules.py [--root public]    prints the rules as JSON, changes nothing
    python3 scripts/edge_rules.py --apply            syncs them (publish job, main-branch push only)
    python3 scripts/edge_rules.py --apply --host <staging host>    rehearses on the staging zone

--apply needs BUNNY_API_KEY (the account API key: Bunny has no scoped keys for edge rules) and
BUNNY_PULL_ZONE_ID. Only rules whose description starts with managedPrefix are created, updated or
deleted; rules added by hand in the dashboard are left alone.
API: https://docs.bunny.net/api-reference/core/pull-zone/addupdate-edge-rule
"""
from __future__ import annotations
import argparse, json, os, re, sys, tomllib
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.bunny.net"

# Enums from Bunny's core OpenAPI spec (EdgeRuleActionType, TriggerTypes, TriggerMatchingTypes).
REDIRECT, OVERRIDE_CACHE_TIME, SET_RESPONSE_HEADER = 1, 3, 5
URL, REQUEST_HEADER = 0, 1
ANY, ALL, NONE = 0, 1, 2
# https://docs.bunny.net/cdn/limits
MAX_TRIGGERS, MAX_PATTERNS = 5, 5


def action(kind, p1=None, p2=None):
    return {"ActionType": kind, "ActionParameter1": p1, "ActionParameter2": p2, "ActionParameter3": None}


def trigger(patterns, kind=URL, matching=ANY, parameter=None):
    return {"Type": kind, "PatternMatches": list(patterns), "PatternMatchingType": matching, "Parameter1": parameter}


def rule(description, main, triggers, matching=ANY, extra=()):
    if len(triggers) > MAX_TRIGGERS or any(len(t["PatternMatches"]) > MAX_PATTERNS for t in triggers):
        raise ValueError(f"Edge rule exceeds Bunny's trigger limits: {description}")
    return {"Description": description, "Enabled": True, **main, "Triggers": triggers,
            "TriggerMatchingType": matching, "ExtraActions": list(extra)}


def url_rule(description, main, patterns, exclude=(), extra=()):
    """Fires on any of `patterns` and none of `exclude`."""
    patterns = list(patterns)
    if exclude:  # triggers combine with All, so the included patterns must fit one trigger
        return rule(description, main, [trigger(patterns), trigger(exclude, matching=NONE)], ALL, extra)
    chunks = [patterns[i:i + MAX_PATTERNS] for i in range(0, len(patterns), MAX_PATTERNS)]
    return rule(description, main, [trigger(c) for c in chunks], ANY, extra)


def csp(config):
    return config["csp"]["header"], "; ".join(f"{k} {v}".strip() for k, v in config["csp"]["directives"].items())


def build(config, redirects):
    prefix, host = config["managedPrefix"], config["host"]
    headers = dict(config["headers"])
    name, value = csp(config)
    headers[name] = value
    (first, first_value), *more = headers.items()
    rules = [url_rule(prefix + "Security headers", action(SET_RESPONSE_HEADER, first, first_value), ["*"],
                      extra=[action(SET_RESPONSE_HEADER, k, v) for k, v in more])]
    for c in config["cache"]:
        rules.append(url_rule(f"{prefix}Cache: {c['name']}", action(SET_RESPONSE_HEADER, "Cache-Control", c["browser"]),
                              c["patterns"], c.get("exclude", ()), [action(OVERRIDE_CACHE_TIME, str(c["edge"]))]))
    for m in config["mime"]:
        rules.append(url_rule(f"{prefix}Content-Type: {m['type']}", action(SET_RESPONSE_HEADER, "Content-Type", m["type"]),
                              m["patterns"]))
    # Agents asking for Markdown on an HTML URL get the twin. Edge-rule redirects are not cached.
    rules.append(rule(prefix + "Markdown twin for Accept: text/markdown",
                      action(REDIRECT, f"https://{host}{{{{path}}}}index.md", "302"),
                      [trigger(["*text/markdown*"], REQUEST_HEADER, parameter="Accept"), trigger(["*/"])], ALL))
    # One rule per target keeps the count far below one per redirect. Patterns carry the host so
    # /1/ cannot also match /knowledge-base/account-security/1/.
    groups: dict[tuple[str, int], list[str]] = {}
    for r in redirects:
        groups.setdefault((r["to"], r["status"]), []).append(r["from"])
    size = MAX_TRIGGERS * MAX_PATTERNS
    for (to, status), sources in sorted(groups.items()):
        patterns = [f"*://{host}{s}" for s in sorted(sources)]
        parts = [patterns[i:i + size] for i in range(0, len(patterns), size)]
        for i, part in enumerate(parts, 1):
            label = f" ({i}/{len(parts)})" if len(parts) > 1 else ""
            rules.append(url_rule(f"{prefix}Redirect to {to}{label}", action(REDIRECT, f"https://{host}{to}", str(status)), part))
    if len(rules) > config["maxRules"]:
        raise SystemExit(f"{len(rules)} edge rules exceed maxRules ({config['maxRules']}) in edge/rules.toml; "
                         "ask Bunny support to raise the limit, then update maxRules")
    return rules


def comparable(r):
    """The fields we manage, normalised the way the API echoes them back."""
    actions = lambda items: [(a["ActionType"], a.get("ActionParameter1") or "", a.get("ActionParameter2") or "",
                              a.get("ActionParameter3") or "") for a in items or []]
    triggers = [(t["Type"], list(t.get("PatternMatches") or []), t.get("PatternMatchingType", 0), t.get("Parameter1") or "")
                for t in r.get("Triggers") or []]
    return (actions([r]), triggers, r.get("TriggerMatchingType", 0), actions(r.get("ExtraActions")), bool(r.get("Enabled")))


def api(method, path, key, body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = Request(API + path, data=data, method=method,
                      headers={"AccessKey": key, "Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urlopen(request, timeout=30) as response:
            text = response.read()
    except HTTPError as error:
        raise SystemExit(f"Bunny API {method} {path}: {error.code} {error.read()[:300].decode(errors='replace')}") from None
    return json.loads(text) if text.strip() else None


def sync(rules, config, key, zone):
    prefix = config["managedPrefix"]
    current = api("GET", f"/pullzone/{zone}", key).get("EdgeRules") or []
    managed, stale = {}, []
    for r in current:
        description = r.get("Description") or ""
        if not description.startswith(prefix):
            continue
        if description in managed:  # a duplicate from an interrupted run
            stale.append(r)
        else:
            managed[description] = r
    unmanaged = len(current) - len(managed) - len(stale)
    if unmanaged + len(rules) > config["maxRules"]:
        raise SystemExit(f"{len(rules)} managed and {unmanaged} hand-made edge rules exceed maxRules ({config['maxRules']}); "
                         "remove hand-made rules the repo now manages or raise the limit")
    wanted = {r["Description"] for r in rules}
    stale += [r for d, r in managed.items() if d not in wanted]
    # Delete first so the zone never exceeds its limit mid-sync.
    for r in stale:
        api("DELETE", f"/pullzone/{zone}/edgerules/{r['Guid']}", key)
        print(f"deleted    {r['Description']}")
    for r in rules:
        existing = managed.get(r["Description"])
        if existing and comparable(existing) == comparable(r):
            print(f"unchanged  {r['Description']}")
            continue
        api("POST", f"/pullzone/{zone}/edgerules/addOrUpdate", key, {**r, "Guid": existing["Guid"] if existing else None})
        print(f"{'updated' if existing else 'created':<10} {r['Description']}")
    print(f"{len(rules)} managed edge rules in sync, {unmanaged} hand-made left alone.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT / "public")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--host", help="another pull zone's hostname, for a staging rehearsal")
    args = parser.parse_args()
    config = tomllib.loads((ROOT / "edge/rules.toml").read_text())
    production = config["host"]
    if args.host:
        if not re.fullmatch(r"[a-z0-9.-]+", args.host):
            raise SystemExit("Invalid host")
        config["host"] = args.host
    redirects = json.loads((args.root / "redirects.json").read_text())["redirects"]
    rules = build(config, redirects)
    if not args.apply:
        json.dump({"limit": config["maxRules"], "count": len(rules), "rules": rules}, sys.stdout, indent=2)
        print(f"\n{len(rules)} of {config['maxRules']} edge rules", file=sys.stderr)
        return
    main_push = os.environ.get("FORGEJO_EVENT_NAME") == "push" and os.environ.get("FORGEJO_REF") == "refs/heads/main"
    if config["host"] == production and not main_push:
        raise SystemExit("Edge-rule sync for the production host requires a main-branch push")
    key, zone = os.environ["BUNNY_API_KEY"], os.environ["BUNNY_PULL_ZONE_ID"]
    if not re.fullmatch(r"\d+", zone):
        raise SystemExit("Invalid pull zone ID")
    sync(rules, config, key, zone)


if __name__ == "__main__":
    main()
