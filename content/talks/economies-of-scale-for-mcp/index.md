---
title: Economies of Scale for MCP and Agents
description: Why you need an identity broker — with Magnus Jungsbluth at AGNTCon + MCPCon Europe.
claim: "Agents should not hold shared, long-lived provider credentials; an identity broker ties delegated access to both person and agent, and a gateway keeps provider tokens out of the agent."
id: jb-talk-agntcon-2026
date: 2026-09-18
topics: [agentic-engineering, identity-authentication]
---
Presented by Magnus Jungsbluth and Jan Brennenstuhl at AGNTCon + MCPCon Europe in Amsterdam on 18 September 2026.

## Materials

- [Presentation slides (PDF)](https://agenticidentitybroker.dev/docs/presentations/2026-09-18_agntcon-mcpcon-agentic-identity-broker.pdf)
- [Session information](https://agntconmcpconeu26.sched.com/event/2RBAI)
- [Supporting article: What I Learned Building an Identity Broker With Coding Agents]({{< ref "/post/agentic-identity-broker" >}})

## Reading companion

An agent should not hold a shared, long-lived provider credential. The broker ties delegated access to both the person and the agent, with chosen permissions and optional expiry. On a tool call, a gateway exchanges the agent's token for a provider token; the provider token does not enter the agent's context.

This is a short reading companion, not a transcript. The supporting article explains the identity model and the engineering lessons in accessible HTML.
