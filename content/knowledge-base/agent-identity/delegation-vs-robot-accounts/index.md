---
id: jb-guide-delegation-vs-robot-accounts
title: "Should an agent use a robot account or delegated access?"
linkTitle: "Robot accounts and delegation"
description: "Why an agent that acts for people needs delegated access tied to each person, and when a robot account still fits."
answer: "When an agent acts for a person, give it delegated access that names both the person and the agent, with narrow scopes, an expiry, and a way to revoke it. A robot account shared by several people gives the agent their combined permissions and hides whose request was whose."
claim: "An agent that acts for a person should use delegated access that names both the person and the agent."
slug: delegation-vs-robot-accounts
date: 2026-10-13
draft: false
weight: 10
topics: [agentic-engineering, identity-authentication]
---

## Key findings

{{< finding id="agent-robot-account-combined-permissions" source="What I Learned Building an Identity Broker With Coding Agents (janbrennenstuhl.eu, 2026)" url="https://www.janbrennenstuhl.eu/agentic-identity-broker/" >}}When several people share an agent that holds a robot account, the agent acts with the combined permissions of all its users, and nobody can tell whose request was whose.{{< /finding >}}

{{< finding id="agent-delegation-keeps-actor-identity" source="RFC 8693, OAuth 2.0 Token Exchange (IETF, 2020), Section 1.1" url="https://www.rfc-editor.org/rfc/rfc8693#section-1.1" >}}Under the delegation semantics of OAuth 2.0 Token Exchange, the acting party keeps its own identity, separate from the person whose rights it uses.{{< /finding >}}

{{< finding id="agent-token-least-privilege" source="RFC 9700, Best Current Practice for OAuth 2.0 Security (IETF, 2025), Section 2.3" url="https://www.rfc-editor.org/rfc/rfc9700#section-2.3" >}}The OAuth 2.0 security best current practice says an access token's privileges should be restricted to the minimum the use case requires, and the token should be audience-restricted to a specific resource server.{{< /finding >}}

{{< finding id="agent-no-long-lived-keys" source="AppSec in the Age of Agentic Engineering (janbrennenstuhl.eu, 2026)" url="https://www.janbrennenstuhl.eu/appsec-agentic-engineering/" >}}Coding agents should not hold persistent identity and access management (IAM) roles or long-lived API keys; an identity broker can issue short-lived, task-scoped credentials on demand instead.{{< /finding >}}

## Evidence

{{< studies caption="Primary sources on robot accounts and delegated agent access" >}}
{{< study title="OAuth 2.0 Token Exchange (RFC 8693)" org="IETF" year="2020" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc8693" >}}Defines delegation and impersonation semantics and the act claim that names the acting party.{{< /study >}}
{{< study title="Best Current Practice for OAuth 2.0 Security (RFC 9700)" org="IETF" year="2025" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc9700" >}}Asks for least-privilege, audience-restricted tokens and warns when resource servers can't tell client tokens from user tokens.{{< /study >}}
{{< study title="Model Context Protocol: Authorization (revision 2026-07-28)" org="Model Context Protocol" year="2026" sample="n/a" method="Specification" url="https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization" >}}Treats clients acting for a user differently from clients acting on their own behalf.{{< /study >}}
{{< study title="What I Learned Building an Identity Broker With Coding Agents" org="this site" year="2026" sample="n/a" method="Field report" url="https://www.janbrennenstuhl.eu/agentic-identity-broker/" >}}Explains why the Agentic Identity Broker keeps both the user and the agent in every authorization decision.{{< /study >}}
{{< study title="AppSec in the Age of Agentic Engineering" org="this site" year="2026" sample="n/a" method="Essay" url="https://www.janbrennenstuhl.eu/appsec-agentic-engineering/" >}}Argues for short-lived, task-scoped credentials and user-revocable delegation for agents.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

Ask first whom the agent acts for. If it runs a job on its own behalf, a dedicated client with its own narrow permissions is a reasonable fit. The [MCP authorization specification]({{< ref "/knowledge-base/agent-identity/mcp-authorization" >}}) explicitly mentions such `client_credentials` clients. If it acts for a person, use a grant that names that person and that agent, and keep it narrow and short-lived as [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700#section-2.3) asks.

Prefer delegation over impersonation. A delegated token can carry the agent as the actor next to the person as the subject, so a resource server and your logs can tell them apart. RFC 9700 also warns that a resource server that can't distinguish tokens obtained with a person's involvement from tokens a client obtained on its own may let that client reach the person's resources.

Keep provider credentials out of the agent's context. [Token exchange]({{< ref "/knowledge-base/agent-identity/token-exchange" >}}) shows how a gateway can do this on each tool call.

### For product and UX

Show people which agent holds access to which service, with what permissions and until when. Give them one place to [revoke that access]({{< ref "/knowledge-base/agent-identity/consent-and-revocation" >}}). If several people use the same agent, show each of them only the grants they made.

## How it works

With a robot account, the agent holds a long-lived credential for each MCP server or API it calls. In OAuth terms, that is closest to a client that gets tokens for itself, without a person in the flow. RFC 9700 quotes the JSON Web Token (JWT) profile for access tokens (RFC 9068): the `sub` claim of such a token should identify the client application, while a token obtained with a person's involvement should identify that person. A robot account therefore can't express who asked for an action. In [my retrospective]({{< ref "/post/agentic-identity-broker" >}}), I describe the consequences once several people share the agent: combined permissions, no attribution, and credentials within reach of anything that tricks the agent.

[RFC 8693](https://www.rfc-editor.org/rfc/rfc8693#section-1.1) describes 2 ways one party can use another's rights. With impersonation, party A gets B's rights and is indistinguishable from B in that context. With delegation, A keeps its own identity, and it's explicitly understood that A acts for B. The RFC uses this exact phrase: "In a sense, A is an agent for B." A token that carries both identities is a composite token. In a JWT, the `act` claim names the acting party.

The Agentic Identity Broker that Magnus Jungsbluth and I built applies delegation. A user grants an agent access to a service with a chosen permission set and an optional expiry and can revoke the grant at any time. The broker keeps both the user and the agent in every authorization decision. The essay and our [AGNTCon + MCPCon talk]({{< ref "/talks/economies-of-scale-for-mcp" >}}) explain the design, and the [project page]({{< ref "/projects/agentic-identity-broker" >}}) links the code.

This model covers agents that act for a person. For autonomous agents with no human in the loop, I wrote in the retrospective that every approach I know of is still brittle.

## Related

- [How does OAuth 2.0 Token Exchange keep provider tokens away from agents?]({{< ref "/knowledge-base/agent-identity/token-exchange" >}})
- [How should people grant and revoke an agent's access?]({{< ref "/knowledge-base/agent-identity/consent-and-revocation" >}})
- [How does authorization work for MCP servers?]({{< ref "/knowledge-base/agent-identity/mcp-authorization" >}})
- [AppSec in the Age of Agentic Engineering]({{< ref "/post/appsec-agentic-engineering" >}})
