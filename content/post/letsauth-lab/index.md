---
title: "Why I Built Letsauth Lab to Measure How MCP Servers Authorize Agents"
linkTitle: "Letsauth Lab: Measuring MCP Authorization"
description: "Letsauth Lab is my open lab at letsauth.eu: a passive scanner checks public MCP servers every night and records which parts of the MCP Authorization specification they support."
claim: "Public MCP servers implement the MCP Authorization specification unevenly, and Letsauth Lab records each difference as a dated observation with evidence a reviewer can open."
lead: "I wanted to know how many large MCP providers support the full authorization specification. My scanner now checks 39 public servers every night, and most of them still rely on dynamic client registration, which the current revision deprecates."
date: 2026-11-02
slug: letsauth-lab
tags: ["oauth2", "agentic-engineering", "open-source", "eurostack"]
findings:
  - id: letsauth-unknown-not-failure
    text: "In the Letsauth Lab export of 2 November 2026, 337 of 897 cells in the MCP auth atlas read unknown, mostly for requirements the currently passive scanner cannot observe, such as how a server validates tokens or rotates refresh tokens."
  - id: letsauth-dcr-over-cimd
    text: "In the Letsauth Lab export of 2 November 2026, 28 of 39 listed servers point to an authorization server that offers dynamic client registration (DCR), which the current MCP Authorization revision deprecates, while 9 support the recommended CIMD (Client ID Metadata Documents) and 9 return the issuer identifier in authorization responses."
  - id: letsauth-passive-line
    text: "The current Letsauth Lab scanner sends at most 8 unauthenticated requests per server, reads only public metadata and the 401 challenge header, and never runs an authorization flow or holds a client credential."
draft: true
---

[Letsauth Lab](https://letsauth.eu/ "Letsauth Lab: an open lab for agent authorization") at letsauth.eu is my attempt to measure how AI agents are authorized, and as much a public research project as my own learning exercise. I publish everything the scanner records as open data under CC BY 4.0.

The letsauth.eu domain had been sitting around in my pet-projects basket for quite some time, originally for a newsletter about modern web authentication, passkeys and the like. What changed my mind was a set of conversations with colleagues and friends about provider-specific OAuth behaviour, such as refresh token rotation and session lifetimes with inactivity and absolute limits. Many providers have their own quirks and spec interpretations. I have built OAuth and OpenID Connect providers myself, and I know that cherry-picking pieces of a specification is common practice. The specifications are full of "SHOULD" requirements, and 2 providers can both claim conformance while behaving differently on the parts that actually matter for integrators.

That made me wonder whether the still young Model Context Protocol (MCP) servers had already grown the same kind of quirks, and how many of the large MCP providers actually support the full, latest [MCP Authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization "MCP Authorization, revision 2026-07-28") at all. I couldn't find anyone who had measured that across servers and over time, so on 13 October 2026 I registered the [Letsauth Lab repo](https://github.com/letsauthlab/letsauth "Letsauth Lab source repository") on GitHub and decided to automate the discovery.

## The rules I set for myself

I didn't want to publish the next AI-composed meta study of the public web, so the lab had to involve actual software tooling and produce something a language model cannot get by summarising. And because I don't scale well, a single person had to be able to keep it correct: coding agents help with the building, and the scanner does the updating. I wrote these conditions down as "honesty tests" in the project's constitution. I described how I work with agents and spec-driven development in [my retrospective on the Agentic Identity Broker]({{< ref "/post/agentic-identity-broker/index.md" >}} "What I Learned Building an Identity Broker With Coding Agents"), so I won't repeat it here.

For the data, I added 2 rules. Each requirement cites the section of the specification revision it comes from, and when the specification changes, the atlas keeps the old reading next to the new one. Each status is a dated observation with a method and evidence a reviewer can open, and because I keep the observations append-only, the dataset also records how a server changed over time.

## What the atlas shows today

The [MCP auth atlas](https://letsauth.eu/mcp/ "MCP auth atlas") lists 39 public MCP servers in alphabetical order, from Airtable to Zoom, against 29 requirements of the current specification revision from 28 July 2026. Of those requirements, 23 fall on the MCP server or its authorization server and get a cell per server. The other 6 are client requirements, such as sending PKCE, and have no cells because the lab doesn't observe clients. Every night the [scanner](https://letsauth.eu/mcp/scanner/ "Letsauth Lab scanner") judges what is observable without a token, from metadata discovery to PKCE, client registration and HTTPS, and records each judgement with the URL it read as evidence. A run ends in a single pull request, and a report per server, such as [the one for Notion](https://letsauth.eu/mcp/servers/notion/scan/ "Scan report for the Notion MCP server"), shows how each cell was decided.

The numbers below come from the [atlas export](https://letsauth.eu/mcp/data.json "MCP atlas data export") of 2 November 2026. With 39 servers, I read them as a first picture and not as a statement about the MCP ecosystem.

| Status | Cells | Of 897 |
|---|---|---|
| supported | 361 | 40 % |
| unknown | 337 | 38 % |
| unsupported | 107 | 12 % |
| not applicable | 87 | 10 % |
| partial | 5 | 1 % |

Of the 1,673 observations behind those cells, 1,463 came from the scanner, 209 are vendor claims I recorded from documentation during a first pass, and a single one is manual. The unknown share is the figure I'd ask readers to look at first, and most of it is structural. A passive scanner can't see how a server behaves on real calls, such as validating the token audience or answering 403 with `insufficient_scope` for step-up. It also can't check refresh token rotation or resource indicators, which need a client that completes a flow. Those rows read unknown for nearly every server, and unknown is never a failure.

A few rows do say something already. In this snapshot, 28 of the 39 servers point to an authorization server that offers dynamic client registration, while 9 accept Client ID Metadata Documents and 9 return the issuer identifier in authorization responses. The current revision marks dynamic client registration as deprecated, recommends Client ID Metadata Documents with a "SHOULD", and says authorization servers should return the issuer in authorization responses, so most servers in the atlas still follow the older registration path. I had no strong expectations going in, and I still don't, but that gap matches what I know from related work: client registration, for public and confidential clients alike, is where providers get opinionated, and that is exactly what makes integrating many of them at once hard.

Discovery is more uniform. Of the 39 servers, 27 offer both ways to find their protected resource metadata, 4 only the `resource_metadata` pointer in the 401 challenge, and 2 only the well-known URI. Only 5 include a scope in that challenge, and 6 advertise `offline_access`, although the specification says a server should not. From their documentation, I also classified access: 34 servers are open to the public, 4 need an administrator or an enterprise contract, and 3 of the public ones need no authentication at all.

## Where I draw the passive line

The scanner is the only part of the lab that contacts other people's servers, and deciding what it may send took some back and forth with myself. I don't want to create junk data on the provider side, I don't want to automate consent flows that were designed for a human to click through, and I don't want to hold hundreds of client credentials. So the constitution makes scanning passive by default: public metadata only, no credentials, no authorization flows.

The first version read 5 well-known documents and never touched the MCP endpoint itself. That left a gap, because the specification also allows a server to announce its metadata through a `resource_metadata` parameter in the `WWW-Authenticate` header of a 401 response. Servers that chose that route, Atlassian, Plaid and Stack Overflow in the first nightly run, got no grade at all.

I decided that the challenge a server returns to an unauthenticated request is public metadata, because the specification requires the server to tell every client that much without a token. So the scanner now sends a single `GET` to the endpoint with the headers an MCP client sends. Streamable HTTP servers may answer `GET` with 405 before they authenticate, so when the `GET` returns a definite status other than 401, the scanner follows up with an empty `POST` that carries no JSON-RPC message. It reads only the status and the challenge header and cancels the body before consuming a byte. Together with the metadata documents, that makes at most 8 unauthenticated requests per server. My [spec for that change](https://github.com/letsauthlab/letsauth/blob/main/specs/008-discovery-challenge/spec.md "Spec 008: discovery challenge check") records the reasoning so a reader can disagree with it. The unknown rows above are the price of this line. I sleep better that way, and I'll see how it evolves.

## The views around the matrix

The other parts of the lab read from the same data model. On the [standards map](https://letsauth.eu/standards/ "Agent auth atlas: the standards map"), I put the specifications, drafts and EU acts behind agent authorization on one graph, with 41 documents and 69 relations: what builds on, profiles, competes with or replaces what, with maturity and dated revisions per document. The requirement a matrix cell cites is a node on this map.

The [delegation chain explorer](https://letsauth.eu/explorer/ "Delegation chain explorer") steps through 3 scenarios of how authority travels from a person to an agent to an API: an MCP client obtaining a token for an MCP server, an enterprise identity provider brokering the token, and an orchestrator delegating to a sub-agent with token exchange. Each hop shows the decoded token and cites a specification revision, and toggles replay the attacks and misconfigurations that break the chain.

For the [breach anatomy](https://letsauth.eu/breaches/ "Breach anatomy"), I wrote up 5 published vulnerabilities and incidents in how agents were authorized, each traced from its advisory to the missing control and the atlas requirement that stands for it. For 3 of them, an explorer toggle replays the attack. The site is static and ships no exploit recipes, so the breach pages offer nothing beyond those toggles.

## How to read the data without turning it into a ranking

My biggest worry about Letsauth Lab is that people read the matrix as a league table. I list the rows alphabetically, the atlas never compares servers with each other, and a grade in a scan report only counts supported requirements per level. A server with 2 unsupported `SHOULD` rows may be a perfectly reasonable integration target, and a server with every passive row green may still validate audiences badly. If you evaluate an MCP server for your agents, use the atlas to find out what to check next, and then check it against your own client.

## Made in Europe

European sovereignty in technology matters to me as a European tech professional, especially in AI, where Europe can and must do better. So my lab runs on European services on purpose: Bunny for hosting and delivery, Plausible for cookieless analytics and Scaleway for the scanner's nightly job, all in EU regions. The [Made in Europe page](https://letsauth.eu/made-in-europe/ "Made in Europe, hosted in the EU") lists every service the lab depends on, including the single one outside the EU.

## What comes next

The [roadmap](https://github.com/letsauthlab/letsauth/blob/main/docs/roadmap.md "Letsauth Lab roadmap") names 3 planned features. eIDAS 2.0 with the EU Digital Identity Wallet, the AI Act and NIS2 all touch how an agent may receive authority, and they are already documents on the standards map. With "Agents under EU rules", I want to turn their mandates, oversight duties and obligations into explorer scenarios and long-form pages. Once there is enough change to report, I plan to generate a changelog and newsletter from merged data and content changes, which brings the original newsletter idea back in a form that can't drift from the data. And a visual redesign will move the lab to the same calm system my blog uses.

The most useful contribution is an observation: what a server you know does, with evidence a reviewer can open. The repository has an [issue template for observations](https://github.com/letsauthlab/letsauth/issues/new/choose "Open an issue on Letsauth Lab") and a [contributing guide](https://github.com/letsauthlab/letsauth/blob/main/CONTRIBUTING.md "Contributing to Letsauth Lab") for that, and corrections, servers, specification revisions and code are welcome too. If you run an MCP server and the atlas has you wrong, the evidence link in the cell is where I'd start the conversation.
