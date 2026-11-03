---
title: "How I Gave This Blog a Read-Only MCP Server on a Bunny Edge Script"
description: "This site has a read-only Model Context Protocol server, written as one Bunny edge script and listed in the official MCP Registry with an ECDSA P-384 DNS proof."
claim: "A blog's MCP server will see little traffic, but a live read-only server is a working example for anyone who writes about agent identity, and the registry's P-384 DNS login needs an undocumented flag."
lead: "Since 28 October 2026, agents can search, read and cite this site through an MCP server at mcp.janbrennenstuhl.eu. It is a single Bunny edge script with 4 tools, and it is listed in the official MCP Registry. This is what it does, why it runs where it runs, and the one flag the registry guide forgets to mention."
date: 2026-10-28
slug: blog-mcp-server
tags: ["agentic-engineering", "jamstack"]
findings:
  - id: mcp-publisher-p384-flag
    text: "The ECDSA P-384 login command in the official MCP Registry authentication guide omits the algorithm flag. mcp-publisher defaults to Ed25519, so a P-384 key only logs in with `--algorithm ecdsap384`."
  - id: mcp-edge-script-own-zone
    text: "A standalone Bunny edge script that answers POST requests needs its own pull zone: the static site's zone redirects directory URLs to their trailing-slash form with a 301, which breaks MCP clients."
  - id: mcp-server-four-files
    text: "The server reads only 4 public files of the site itself (search index, catalog, findings and the Markdown twins), caches them for 5 minutes and never fetches a URL taken from a request."
draft: true
---

Since 28 October 2026, this site has a read-only [Model Context Protocol (MCP)](https://modelcontextprotocol.io/ "Model Context Protocol") server at `https://mcp.janbrennenstuhl.eu/mcp`. An agent can add it as a remote server and search the essays and the field guide, read any entry as Markdown, and pull quotable findings with their anchor URLs. The whole thing is 1 Bunny edge script of about 200 lines, and since the same day it is listed in the [official MCP Registry](https://registry.modelcontextprotocol.io/ "MCP Registry") as `eu.janbrennenstuhl/site`. The [source is public](https://github.com/jbspeakr/janbrennenstuhl.eu/tree/main/edge/mcp "edge/mcp in the site repository").

I don't expect many people to add a blog to their MCP client, so direct traffic will stay small. I built it anyway because I write about agent identity and MCP authorization, and a live, small, well-behaved server is a working example I can point to when I argue about how such a server should look. Building it also took me through the publishing side of the ecosystem, and that side has a gap in its documentation.

## What the server offers and what it refuses

The site already publishes everything in machine-readable form: Markdown twins of every page, a catalog, a findings file, a search index and `llms.txt`. I describe those on the [page for agents]({{< ref "/page/agents" >}} "For agents"). The MCP server adds nothing to that content. It wraps the same files in 4 tools so an agent doesn't have to know the file layout:

- `search_site` runs a full-text search over essays, field-guide entries, talks, projects, the glossary and the profile page, optionally filtered by kind or topic.
- `get_entry` returns the full Markdown of 1 entry, by catalog id or canonical URL.
- `get_findings` lists quotable findings with their anchor URL, source and review status.
- `list_topics` returns the 6 topics with descriptions and entry counts.

Each tool carries the `readOnlyHint` and `openWorldHint: false` annotations, and the server's instructions tell the client to cite canonical URLs and name the CC BY 4.0 condition. The server fetches only 4 kinds of files from `www.janbrennenstuhl.eu`: the search index, the catalog, the findings file and the Markdown twins. It caches them for 5 minutes, and it never fetches a URL that arrives in a request. `get_entry` resolves an id or URL against the catalog first, so a caller can't turn the server into a proxy. There is no sign-in, because everything it serves is public anyway, and the pull zone in front of it rate-limits each client.

On the wire, the server speaks 2 generations of the protocol. For the current [revision 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http "MCP 2026-07-28: Streamable HTTP") it is stateless: each request carries its protocol version in `_meta`, and the script checks that the mirrored `MCP-Protocol-Version`, `Mcp-Method` and `Mcp-Name` headers match the body before it answers. For clients from 2025-03-26 to 2025-11-25 it still answers the `initialize` handshake. Requests from a browser origin other than the site are rejected, anything but `POST` gets a 405, and every response is marked `no-store`.

## Why it runs as a standalone edge script on its own zone

The site is static and lives on Bunny's CDN, so the natural place for a small dynamic endpoint was a [Bunny edge script](https://docs.bunny.net/docs/edge-scripting "Bunny Edge Scripting"). Bunny runs these on Deno, and a standalone script answers every request to its pull zone itself. I didn't want a second host or a container for 4 read-only tools.

The script does not live on the www zone, because that zone would get in its way. Its rules redirect directory URLs to their trailing-slash form, so `/mcp` would become a 301 to `/mcp/`, and a redirect breaks clients that POST JSON-RPC. The zone's caching and Content Security Policy headers are built for static files too. So the server has its own pull zone with its own hostname, certificate and rate limit, and if something goes wrong I can switch it off without touching the site.

Bunny accepts 1 file per script, and I wanted the handler to stay testable on its own. A small Python script in the repository inlines `handler.ts` into `main.ts`, the continuous integration (CI) job that verifies a release builds that bundle and stores it as an artifact, and the publish job deploys exactly those bytes with the script's own deployment key. The account-wide API key is never involved. The bundle is deployed with every release of the site, so a change to the tools goes live the same way a new essay does.

## Registering it with a P-384 DNS proof

The registry needs proof that I control the namespace a server is published under. For a domain-based name such as `eu.janbrennenstuhl/site`, the [authentication guide](https://modelcontextprotocol.io/registry/authentication#dns-authentication "How to authenticate when publishing to the MCP Registry") offers a DNS TXT record on the apex domain that holds a public key, and the `mcp-publisher` command line tool signs a challenge with the matching private key. The guide shows the procedure for Ed25519 and for ECDSA P-384. I took the P-384 route because the `openssl` that ships with macOS is LibreSSL, and LibreSSL 3.3.6 answers the guide's first command with `Algorithm Ed25519 not found`.

Generating the key and the record works as documented:

```sh
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:secp384r1 -out key.pem
PUBLIC_KEY="$(openssl ec -in key.pem -text -noout -conv_form compressed \
  | grep -A4 "pub:" | tail -n +2 | tr -d ' :\n' | xxd -r -p | base64)"
echo "janbrennenstuhl.eu. IN TXT \"v=MCPv1; k=ecdsap384; p=${PUBLIC_KEY}\""
```

The login step is where the guide falls short. Its P-384 login command is identical to the Ed25519 one apart from how the private key is extracted, and with that command the login fails:

```
Logging in with dns...
Signing in process using key algorithm ed25519
Error: failed to get token: failed to sign timestamp: invalid seed length: expected 32 bytes, got 49
```

The second line gives it away. The reason is in the [publisher's source](https://github.com/modelcontextprotocol/registry/blob/main/cmd/publisher/commands/login.go "mcp-publisher login command"): the login command has an `--algorithm` flag that accepts `ed25519` or `ecdsap384` and defaults to Ed25519, and the guide never mentions it. The command that works is:

```sh
PRIVATE_KEY="$(openssl ec -in key.pem -noout -text | grep -A4 "priv:" | tail -n +2 | tr -d ' :\n')"
mcp-publisher login dns --algorithm ecdsap384 --domain janbrennenstuhl.eu --private-key "${PRIVATE_KEY}"
mcp-publisher publish
```

The second command runs in the directory that holds the `server.json`. Mine declares the name, the repository with its `edge/mcp` subfolder, a `websiteUrl` pointing to the agents page, and 1 remote of type `streamable-http`. The private key stays outside the repository. A unit test keeps the version in `server.json` in step with the version the server reports and with the URL in the site's `/.well-known/api-catalog`, so I can't publish an entry that disagrees with the running server. The Registry lists the entry as active [since 28 October 2026](https://registry.modelcontextprotocol.io/v0.1/servers?search=janbrennenstuhl "Registry entry for eu.janbrennenstuhl/site").

## What I expect from it

Little direct traffic, as I said. An MCP server for a personal site is useful in about the same way a well-kept `llms.txt` is: it lowers the effort for the few agents that look, and the files it serves are generated with every release anyway. What it gives me is a reference. When I write that a read-only server should carry tool annotations, refuse arbitrary fetches, validate the mirrored headers of the stateless protocol revision, and prove its namespace to the registry, I can now link to a server that does all of that and to the 200 lines behind it.

The server has no authorization at all, and that is the one thing it can't demonstrate. I measure how public MCP servers handle the authorization specification in the [MCP auth atlas at Letsauth Lab](https://letsauth.eu/mcp/ "MCP auth atlas"), and a server with nothing to protect would only add an empty row there. If I ever add a tool that is worth protecting, this is where the next essay starts.
