---
id: jb-guide-token-exchange
title: "How does OAuth 2.0 Token Exchange keep provider tokens away from agents?"
linkTitle: "Token exchange"
description: "How RFC 8693 token exchange lets a gateway trade an agent's token for a provider token so the agent never holds the provider token."
answer: "OAuth 2.0 Token Exchange (RFC 8693) lets a client trade one token for another token meant for a specific target service. When a gateway runs that exchange on each tool call, as in the Agentic Identity Broker, the provider token stays between the broker, the gateway and the provider and never reaches the agent."
claim: "OAuth 2.0 Token Exchange (RFC 8693) lets a gateway trade an agent's token for a provider token, so the provider token never has to reach the agent."
slug: token-exchange
date: 2026-10-13
draft: false
weight: 20
topics: [agentic-engineering, identity-authentication]
scripts: [delegation]
---

## Key findings

{{< finding id="agent-rfc8693-security-token-service" source="RFC 8693, OAuth 2.0 Token Exchange (IETF, 2020), Section 1" url="https://www.rfc-editor.org/rfc/rfc8693#section-1" >}}RFC 8693 lets a client present a security token to an OAuth 2.0 authorization server acting as a Security Token Service and receive a new token, for example one scoped more narrowly for a downstream service.{{< /finding >}}

{{< finding id="agent-broker-provider-token-stays-out" source="What I Learned Building an Identity Broker With Coding Agents (janbrennenstuhl.eu, 2026)" url="https://www.janbrennenstuhl.eu/agentic-identity-broker/" >}}In the Agentic Identity Broker, an MCP gateway exchanges the agent's token for the matching provider token through RFC 8693 on each tool call, so the provider token never reaches the agent.{{< /finding >}}

{{< finding id="agent-exchange-client-authentication" source="RFC 8693, OAuth 2.0 Token Exchange (IETF, 2020), Section 2.1" url="https://www.rfc-editor.org/rfc/rfc8693#section-2.1" >}}RFC 8693 warns that without client authentication at the token endpoint, anyone holding a compromised token can trade it for other tokens.{{< /finding >}}

{{< finding id="agent-act-claim-current-actor" source="RFC 8693, OAuth 2.0 Token Exchange (IETF, 2020), Section 4.1" url="https://www.rfc-editor.org/rfc/rfc8693#section-4.1" >}}In a JWT issued through token exchange, access control decisions must consider only the top-level claims and the current actor named in the act claim, while nested prior actors are informational.{{< /finding >}}

{{< finding id="agent-exchange-no-revocation-link" source="RFC 8693, OAuth 2.0 Token Exchange (IETF, 2020), Section 2.1" url="https://www.rfc-editor.org/rfc/rfc8693#section-2.1" >}}A token exchange creates no tight link between the input and output tokens, so passing revocation from one to the other depends on the implementation and isn't a property of the protocol.{{< /finding >}}

## Evidence

{{< studies caption="Primary sources on token exchange for agents" >}}
{{< study title="OAuth 2.0 Token Exchange (RFC 8693)" org="IETF" year="2020" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc8693" >}}Defines the token exchange grant, its request and response parameters, and the act and may_act claims.{{< /study >}}
{{< study title="Resource Indicators for OAuth 2.0 (RFC 8707)" org="IETF" year="2020" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc8707" >}}Defines the resource parameter that tells the authorization server where a token will be used.{{< /study >}}
{{< study title="What I Learned Building an Identity Broker With Coding Agents" org="this site" year="2026" sample="n/a" method="Field report" url="https://www.janbrennenstuhl.eu/agentic-identity-broker/" >}}Describes how a gateway exchanges the agent's token for the matching provider token on each tool call.{{< /study >}}
{{< study title="Economies of Scale for MCP and Agents" org="this site" year="2026" sample="n/a" method="Talk" url="https://www.janbrennenstuhl.eu/talks/economies-of-scale-for-mcp/" >}}Presents the broker's delegation model at AGNTCon + MCPCon Europe 2026.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

Put the exchange in a component the agent can't control, such as a gateway, and authenticate that component at the token endpoint. Name the target with `resource` or `audience` and ask for the smallest `scope` the tool call needs. RFC 8693 points out that broad requests across many target services are more likely to be refused.

Treat revocation as your own job. The RFC leaves it to the implementation whether revoking a grant or an input token affects tokens already issued, so keep issued tokens short-lived and check the grant at exchange time. [Consent and revocation]({{< ref "/knowledge-base/agent-identity/consent-and-revocation" >}}) covers the rest.

If an agent's token can travel further, use the `act` claim to record the agent as the actor and the `may_act` claim to state who may act for the subject.

### For product and UX

Users don't see the exchange, but they see its effects. When a tool call fails because a grant expired or was revoked, tell the user which service and which agent were affected and how to grant access again.

## How it works

RFC 8693 defines the exchange as 1 request and 1 response at an authorization server's token endpoint. With a gateway between an agent and its tools, the exchange runs like this:

{{< explainer "delegation" "Step through the exchange" >}}
1. The agent calls a tool through the gateway and presents its own token.
2. The gateway acts as the RFC 8693 client. It sends a `POST` to the token endpoint with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, a `subject_token` that represents the person on whose behalf the request is made, and its `subject_token_type`. Optional parameters name the target (`resource`, `audience`), the access wanted (`scope`), and the token type wanted (`requested_token_type`).
3. The gateway authenticates with the normal OAuth 2.0 client authentication methods.
4. The authorization server validates the presented tokens and decides by policy whether to issue a token for the named target. If it refuses, it answers with `invalid_request`, or with `invalid_target` when it won't issue a token for the requested target.
5. A successful response is a normal OAuth token response: `access_token` carries the issued token, together with `issued_token_type`, `token_type`, and, as recommended, `expires_in`. The issued token doesn't have to be an OAuth access token.
6. The gateway calls the target service with the issued token and returns only the result to the agent.
{{< /explainer >}}

The following request shows step 2 with placeholder hosts and tokens. It illustrates the RFC parameters and isn't the broker's API. I've left the values unencoded and added line breaks for readability; a real request URL-encodes the form body.

```http {filename="token-exchange.http"}
POST /token HTTP/1.1
Host: broker.example.com
Authorization: Basic <gateway client credentials>
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=<token the agent presented>
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&resource=https://api.provider.example/
&scope=<permissions the tool call needs>
```

The Agentic Identity Broker that Magnus Jungsbluth and I built uses this pattern, as I describe in the [retrospective]({{< ref "/post/agentic-identity-broker" >}}). A user grants an agent access to a service, such as GitHub, with a chosen permission set and an optional expiry, and the broker stores the provider tokens encrypted. On each tool call, an MCP gateway such as agentgateway exchanges the agent's token for the matching provider token, so the provider token never reaches the agent.

RFC 8693 also defines an optional `actor_token` for the party that will act on behalf of the subject. In the issued JWT, the `act` claim can record that actor, and nested `act` claims record a chain of earlier actors. The [broker roadmap](https://github.com/zalando-incubator/agentic-identity-broker#roadmap "Agentic Identity Broker roadmap") lists token exchange for agent-to-agent calls as planned work.

## Related

- [Should an agent use a robot account or delegated access?]({{< ref "/knowledge-base/agent-identity/delegation-vs-robot-accounts" >}})
- [How does authorization work for MCP servers?]({{< ref "/knowledge-base/agent-identity/mcp-authorization" >}})
- [Economies of Scale for MCP and Agents]({{< ref "/talks/economies-of-scale-for-mcp" >}})
- [Agentic Identity Broker]({{< ref "/projects/agentic-identity-broker" >}})
