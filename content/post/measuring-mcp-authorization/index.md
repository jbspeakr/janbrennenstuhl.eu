---
title: "Measuring How MCP Servers Authorize Agents"
linkTitle: "Letsauth Lab: Measuring MCP Authorization"
description: "Letsauth Lab is my open lab at letsauth.eu: a passive scanner checks public MCP servers every night and records which parts of the MCP Authorization specification they support."
claim: "Public MCP servers implement the MCP Authorization specification unevenly, and Letsauth Lab records each difference as a dated observation with evidence."
lead: "I wanted to know how many major MCP providers support the full MCP authorization specification. My scanner now checks 39 public servers every night, and most of them still point to an authorization server that offers dynamic client registration, which the current revision deprecates."
date: 2026-11-02
slug: measuring-mcp-authorization
tags: ["oauth2", "agentic-engineering", "open-source", "eurostack"]
findings:
  - id: letsauth-dcr-over-cimd
    text: "Early November 2026, 28 of 39 listed servers still point to an authorization server that offers dynamic client registration (DCR), which the current MCP Authorization revision deprecates, while 9 advertise support for the recommended CIMD (Client ID Metadata Documents) and 9 advertise that they return the issuer identifier in authorization responses."
  - id: letsauth-passive-line
    text: "The current Letsauth Lab scanner sends at most 8 unauthenticated requests per server, reads only public metadata and the 401 challenge header, and never runs an authorization flow or holds a client credential."
---

[Letsauth Lab](https://letsauth.eu/ "Letsauth Lab: an open lab for agent authorization") at letsauth.eu is my attempt to measure how AI agents are authorized by MCP providers. It is as much a public research project as my own learning exercise. I publish everything the scanner records as open data under CC BY 4.0.

The letsauth.eu domain had been sitting around in my pet-projects basket for quite some time, originally for a newsletter about modern web authentication, passkeys and the like. What eventually made me use it for something else was a set of conversations with colleagues and friends about provider-specific OAuth behaviour, such as refresh token rotation and session lifetimes with inactivity and absolute limits. Many providers have their own quirks and spec interpretations. I have built OAuth and OpenID Connect providers myself, and I know that cherry-picking pieces of a specification is common practice. The specifications are full of "SHOULD" requirements and gaps, and two providers can both claim conformance while behaving differently on the parts that actually matter for integrators.

MCP itself is still young and has seen quite some drastic changes in the last year. So I wondered whether early-adopting providers had already grown the same kind of quirks, and how many of the large MCP offers support the full, latest [MCP Authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization "MCP Authorization, revision 2026-07-28") at all. I couldn't find anyone who had measured that across a multitude of providers and over time. So I decided to automate the discovery, and on 13 October 2026 I registered the [Letsauth Lab org and repo](https://github.com/letsauthlab/letsauth "Letsauth Lab source repository") on GitHub.

## The rules I set for myself

Just to set the tone right, I didn't want to publish yet another AI-composed meta study of the public web, so the lab had to involve actual software tooling and produce something a language model cannot get by summarising. And because I don't scale well, a single person had to be able to keep it correct: coding agents help with the building, and the scanner does the updating. I wrote these conditions down as "honesty tests" in the project's constitution. In case you want to learn more about how I work with agents and spec-driven development, read [my retrospective on the Agentic Identity Broker]({{< ref "/post/agentic-identity-broker/index.md" >}} "What I Learned Building an Identity Broker With Coding Agents"). I won't repeat it here.

For the data, I added two rules. First, each requirement cites the section of the actual spec revision it comes from, and when the MCP specification changes next time, my atlas will keep the old reading next to the new one. Second, each status is a dated observation with a method and evidence a reviewer can open, and because I keep the observations append-only, the dataset also records how a server changed over time.

## What the atlas shows today

My [MCP auth atlas](https://letsauth.eu/mcp/ "MCP auth atlas") lists 39 public MCP servers in alphabetical order, from Airtable to Zoom, against 29 requirements of the current specification revision from 28 July 2026. Of those requirements, 23 fall on the MCP server or its authorization server and get a cell per server. The other 6 are client requirements, such as sending PKCE, and have no cells because the lab doesn't observe clients. Every night the [scanner](https://letsauth.eu/mcp/scanner/ "Letsauth Lab scanner") judges what is observable without a token, from metadata discovery to PKCE support, client registration and TLS, and records each judgement with the source URL as evidence. A run ends in a single pull request, and each server has its own page, such as [the one for Notion](https://letsauth.eu/mcp/servers/notion/ "Notion in the MCP auth atlas"), with the observation history and evidence behind every cell.

The numbers below come from the [atlas export](https://letsauth.eu/mcp/data.json "MCP atlas data export") of 2 November 2026. With currently 39 servers, I suggest reading them as a first picture and not as a statement about the MCP ecosystem.

| Status | Cells | Of 897 |
|---|---|---|
| supported | 361 | 40 % |
| unknown | 337 | 38 % |
| unsupported | 107 | 12 % |
| not applicable | 87 | 10 % |
| partial | 5 | 1 % |

Of the underlying 1,673 observations, 1,463 came from the scanner, 209 are vendor claims I had my agent record from vendor documentation as a baseline, and a single one was added manually by me. The unknown share is the figure I'd ask readers to look at first, and most of it is structural. A passive scanner can't see how a server behaves on real calls, such as validating the token audience or answering 403 with `insufficient_scope` for step-up. It also can't check refresh token rotation or resource indicators, which need a client that completes a flow. Those rows today still read unknown for nearly every server, and I never count unknown as a failure.

A few rows do say something already. In this snapshot, 28 of the 39 servers point to an authorization server that offers dynamic client registration (DCR), while 9 advertise support for Client ID Metadata Documents (CIMD) and 9 advertise that they return the issuer identifier in authorization responses. The current revision [deprecates DCR and recommends CIMD](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization#client-registration "MCP Authorization, revision 2026-07-28: Client Registration") with a "SHOULD", and it says authorization servers "SHOULD include the iss parameter" in their responses. So most servers in the atlas still follow the older registration path. I had no strong expectations going in, but that gap matches what I know from building OAuth providers myself: client registration, for public and confidential clients alike, is where providers get opinionated, and that is exactly what makes integrating many of them at once hard.

Discovery is more uniform. Of the 39 servers, 27 offer both ways to find their protected resource metadata, 4 only the `resource_metadata` pointer in the 401 challenge, and 2 only the well-known URI. Only 5 include a scope in that challenge, and 6 list `offline_access` in the `scopes_supported` of their protected resource metadata, although the specification says an MCP server ["SHOULD NOT" advertise it there](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization#refresh-tokens "MCP Authorization, revision 2026-07-28: Refresh Tokens"), because refresh tokens are not a resource requirement.

Listed in the atlas doesn't mean anyone can connect, so I had my agent classify access from vendor documentation as well. By that reading, 34 servers are open to the public, 4 need an administrator or an enterprise contract, and for 1 the documentation leaves it open. Of the public ones, 3 need no authentication at all.

## Where I draw the passive line

The scanner is the only part of the lab that contacts other people's servers, and deciding what it may send took some back and forth with myself. I don't want to create junk data on the provider side, automate consent flows that were designed for a human to click through, violate any T&Cs or hold hundreds of client credentials. So my project's constitution makes scanning passive by default: public metadata only, no credentials, no authorization flows.

The first version read 5 well-known documents and never touched the MCP endpoint itself. That left a gap, because the specification also allows a server to announce its metadata through a `resource_metadata` parameter in the `WWW-Authenticate` header of a 401 response. Servers that chose that route, such as Atlassian, Plaid and Stack Overflow, got few details in the first nightly run.

I decided that the challenge a server returns to an unauthenticated request is public metadata, because the specification requires the server to tell every client that much without a token. So the scanner now sends a single `GET` to the endpoint with the headers an MCP client sends. Streamable HTTP servers may answer `GET` with 405 before they authenticate, so when the `GET` returns a definite status other than 401, the scanner follows up with an empty `POST` that carries no JSON-RPC message. It reads only the status and the challenge header and cancels the body before consuming a byte. Together with the metadata documents, that makes at most 8 unauthenticated requests per server. My [spec for that change](https://github.com/letsauthlab/letsauth/blob/main/specs/008-discovery-challenge/spec.md "Spec 008: discovery challenge check") records the reasoning so a reader can disagree with it. The unknown rows above are the price of this line. I sleep better that way, and I'll see how that line evolves.

## The views around the matrix

The other parts of the lab read from the same data model and explore different MCP-related angles. On the [standards map](https://letsauth.eu/standards/ "Agent auth atlas: the standards map"), I put the specifications, drafts and EU acts behind agent authorization on one graph, currently with 41 documents and 67 relations: what builds on, profiles, competes with or replaces what, with maturity and dated revisions per document. The requirement a matrix cell cites is a node on this map.

The [delegation chain explorer](https://letsauth.eu/explorer/ "Delegation chain explorer") steps through three scenarios of how authority travels from a person to an agent to an API: an MCP client obtaining a token for an MCP server, an enterprise identity provider brokering the token, and an orchestrator delegating to a sub-agent with token exchange. Each hop shows the decoded token and cites a specification revision, and toggles replay the attacks and misconfigurations that break the chain.

For the [breach anatomy](https://letsauth.eu/breaches/ "Breach anatomy"), I wrote up 5 published vulnerabilities and incidents in how agents were authorized, each traced from its advisory to the missing control and the atlas requirement that stands for it. For three of them, an explorer toggle replays the attack. My lab site is static and ships no exploit recipes, so for now those toggles are the only interactive part of the breach pages.

## How to read the data without turning it into a ranking

My biggest worry about Letsauth Lab is that people read the matrix as a league table. I list the rows alphabetically, the atlas never compares servers with each other, and a server page only counts supported requirements per level, without a score. A server with two unsupported `SHOULD` rows may be a perfectly reasonable integration target, and a server with every passive row green may still validate audiences badly. If you evaluate an MCP server for your agents, use the atlas to find out what to check next, and then check it using your own client.

## Made in Europe

European sovereignty in technology matters to me as a European tech professional, especially in AI-related domains, where Europe can and must do better. So my lab runs on European services on purpose: Bunny for hosting and delivery, Plausible for cookieless analytics and Scaleway for the scanner's nightly job, all in EU regions. The [Made in Europe page](https://letsauth.eu/made-in-europe/ "Made in Europe, hosted in the EU") lists every service the lab depends on, including the single one outside the EU.

## What comes next

My [Letsauth Lab project page]({{< ref "/projects/letsauth-lab/index.md" >}} "Letsauth Lab") keeps the current links and licences, and the [roadmap](https://github.com/letsauthlab/letsauth/blob/main/docs/roadmap.md "Letsauth Lab roadmap") lists what I plan next. I want to grow the MCP coverage in both directions: more servers in the atlas and more requirements the scanner can check. As it grows, I also want better agent support for reviewing the data, so that the atlas stays correct and complete. I'd also like to turn the observations into talks and presentations.

If you know something about a server that my scanner can't see, such as how it validates tokens or rotates refresh tokens, please add it to the atlas with evidence a reviewer can open. The [issue template for observations](https://github.com/letsauthlab/letsauth/issues/new/choose "Open an issue on Letsauth Lab") is the quickest way, and the [contributing guide](https://github.com/letsauthlab/letsauth/blob/main/CONTRIBUTING.md "Contributing to Letsauth Lab") explains what a data pull request needs. New servers, corrections and code are welcome too. If you run an MCP server and the atlas has you wrong, the evidence link in the cell is where I'd start the conversation.
