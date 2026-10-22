---
id: jb-guide-consent-and-revocation
title: "How should people grant and revoke an agent's access?"
linkTitle: "Consent and revocation"
description: "How to let people give an agent narrow, time-limited access to a service and take it back, based on the OAuth revocation and security RFCs."
answer: "Let people grant each agent access per service, with a permission set they choose and an expiry, and let them revoke that grant at any time. Revoking the grant has to stop every token derived from it, so keep issued tokens short-lived and check the grant whenever a new token is issued."
claim: "People should grant an agent access per service with chosen permissions and an expiry, and be able to revoke that grant at any time."
slug: consent-and-revocation
date: 2026-10-13
draft: false
weight: 30
topics: [agentic-engineering, identity-authentication]
---

## Key findings

{{< finding id="agent-grant-scope-expiry-revoke" source="What I Learned Building an Identity Broker With Coding Agents (janbrennenstuhl.eu, 2026)" url="https://www.janbrennenstuhl.eu/agentic-identity-broker/" >}}In the Agentic Identity Broker, a user grants an agent access to a service with a chosen permission set and an optional expiry, and can revoke that grant at any time.{{< /finding >}}

{{< finding id="agent-revocation-cascades-to-grant" source="RFC 7009, OAuth 2.0 Token Revocation (IETF, 2013), Section 2.1" url="https://www.rfc-editor.org/rfc/rfc7009#section-2.1" >}}Under RFC 7009, revoking a refresh token should also invalidate all access tokens based on the same authorization grant if the authorization server supports access token revocation.{{< /finding >}}

{{< finding id="agent-self-contained-token-revocation" source="RFC 7009, OAuth 2.0 Token Revocation (IETF, 2013), Section 3" url="https://www.rfc-editor.org/rfc/rfc7009#section-3" >}}Immediate revocation of self-contained access tokens needs backend coordination that RFC 7009 calls non-standardized, and short-lived access tokens limit how long a revoked token stays in use.{{< /finding >}}

{{< finding id="agent-refresh-token-bound-to-consent" source="RFC 9700, Best Current Practice for OAuth 2.0 Security (IETF, 2025), Section 4.14.2" url="https://www.rfc-editor.org/rfc/rfc9700#section-4.14.2" >}}Refresh tokens must be bound to the scope and resource servers the resource owner consented to.{{< /finding >}}

## Evidence

{{< studies caption="Primary sources on agent consent and revocation" >}}
{{< study title="OAuth 2.0 Token Revocation (RFC 7009)" org="IETF" year="2013" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc7009" >}}Defines a revocation endpoint and how revoking one token can revoke related tokens and the grant.{{< /study >}}
{{< study title="Best Current Practice for OAuth 2.0 Security (RFC 9700)" org="IETF" year="2025" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc9700" >}}Binds refresh tokens to the consented scope and resources and lets them expire after inactivity.{{< /study >}}
{{< study title="Resource Indicators for OAuth 2.0 (RFC 8707)" org="IETF" year="2020" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc8707" >}}Lets the authorization server tell the user which resources a client will access on their behalf.{{< /study >}}
{{< study title="OAuth 2.0 Token Exchange (RFC 8693)" org="IETF" year="2020" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc8693" >}}Leaves revocation of tokens issued by an exchange to the implementation.{{< /study >}}
{{< study title="Model Context Protocol: Authorization (revision 2026-07-28)" org="Model Context Protocol" year="2026" sample="n/a" method="Specification" url="https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization" >}}Asks clients to request minimal scopes first and add scopes through step-up authorization.{{< /study >}}
{{< study title="What I Learned Building an Identity Broker With Coding Agents" org="this site" year="2026" sample="n/a" method="Field report" url="https://www.janbrennenstuhl.eu/agentic-identity-broker/" >}}Describes per-agent grants with chosen permissions, optional expiry and revocation at any time.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

Model the grant as a record of its own that names the person, the agent, the service, the permissions and the expiry, and issue every token from it. Check that record whenever you issue or exchange a token, so a revocation takes effect at the next tool call. Expiring tokens are the fallback for tokens you can't recall.

Wire revocation through every layer you control. Call the [RFC 7009](https://www.rfc-editor.org/rfc/rfc7009) revocation endpoint where the provider offers one, and don't stop at the first token. RFC 8693 says tokens issued by a [token exchange]({{< ref "/knowledge-base/agent-identity/token-exchange" >}}) aren't linked to their input token, so revoking one doesn't reach the other unless you build that.

Ask for the least access first. The [MCP authorization specification]({{< ref "/knowledge-base/agent-identity/mcp-authorization" >}}) describes this as step-up authorization: request minimal scopes and add more when a server asks for them.

### For product and UX

Show each grant with the agent, the service, the permissions and the expiry in plain words, and put the revoke action next to it. Default to an expiry instead of open-ended access. When an agent needs more access, ask at that moment for that specific permission.

## How it works

Granting access in OAuth starts with an authorization request. The client names the access it wants in `scope` and, with [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707#section-2.1), the resources in `resource`. RFC 8707 notes that the authorization server can use those resource values to inform the user about the resources the client will access on their behalf. The consent screen can then name the service, not only a list of scopes.

In the Agentic Identity Broker, which Magnus Jungsbluth and I built, a user grants an agent access to a service with a chosen permission set and an optional expiry. The broker keeps both the user and the agent in every authorization decision. I describe the design in the [retrospective]({{< ref "/post/agentic-identity-broker" >}}), and my [AppSec essay]({{< ref "/post/appsec-agentic-engineering" >}}) argues for narrow, time-limited permissions that the user can revoke at any moment.

Revoking access in OAuth uses the revocation endpoint from RFC 7009. A client sends the token it wants revoked, and the server invalidates it and, depending on policy, related tokens and the grant itself. RFC 7009 gives 2 reasons this matters for people: it stops a grant from staying valid without the user's knowledge, and revoked grants disappear from any list of grants the authorization server shows the user. The server answers with HTTP 200 even for an invalid token. A 503 means the client must assume the token still exists.

Self-contained tokens make revocation harder. A resource server can check a self-contained token, such as a JSON Web Token (JWT), without asking the authorization server, so it won't learn about a revocation on its own. RFC 7009 names short-lived access tokens with refresh tokens as one alternative. RFC 9700 adds that refresh tokens must stay bound to the consented scope and resources, should expire after a period of inactivity, and may be revoked on security events such as a password change or logout.

## Related

- [Should an agent use a robot account or delegated access?]({{< ref "/knowledge-base/agent-identity/delegation-vs-robot-accounts" >}})
- [How does OAuth 2.0 Token Exchange keep provider tokens away from agents?]({{< ref "/knowledge-base/agent-identity/token-exchange" >}})
- [Economies of Scale for MCP and Agents]({{< ref "/talks/economies-of-scale-for-mcp" >}})
- [Agentic Identity Broker]({{< ref "/projects/agentic-identity-broker" >}})
