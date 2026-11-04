---
title: "Letsauth Lab"
description: "An open lab at letsauth.eu that measures how public MCP servers implement the MCP Authorization specification, for people who build or integrate agent authorization."
claim: "Letsauth Lab records what public MCP servers serve of the MCP Authorization specification as dated observations with evidence, so agent authorization can be checked against measured data."
date: 2026-10-13
tags: ["oauth2", "agentic-engineering", "open-source", "eurostack"]
draft: true
---

I started Letsauth Lab to find out how many public MCP servers support the current MCP Authorization specification. A passive scanner reads their public OAuth metadata every night and records each result as a dated observation with evidence, without tokens, client credentials or authorization flows. Around the resulting MCP auth atlas, the lab has a standards map, a delegation chain explorer and breach anatomies that read from the same data.

## Links

- [Letsauth Lab](https://letsauth.eu/ "Letsauth Lab: an open lab for agent authorization")
- [MCP auth atlas](https://letsauth.eu/mcp/ "MCP auth atlas") and its [data export](https://letsauth.eu/mcp/data.json "MCP atlas data export")
- [Source code and data](https://github.com/letsauthlab/letsauth "Letsauth Lab source repository")
- [Roadmap](https://github.com/letsauthlab/letsauth/blob/main/docs/roadmap.md "Letsauth Lab roadmap")
- [Contributing guide](https://github.com/letsauthlab/letsauth/blob/main/CONTRIBUTING.md "Contributing to Letsauth Lab")

## Writing and talks

- [Why I built Letsauth Lab]({{< ref "/post/measuring-mcp-authorization/index.md" >}} "Why I Built Letsauth Lab to Measure How MCP Servers Authorize Agents")

The code is licensed under MIT and the data under CC BY 4.0. The atlas changes every night, so the lab itself is the current source for any number.
