---
id: jb-guide-mcp-authorization
title: "How does authorization work for MCP servers?"
linkTitle: "MCP authorization"
description: "What the Model Context Protocol authorization specification, revision 2026-07-28, requires from MCP servers, clients and authorization servers."
answer: "In the MCP authorization specification (revision 2026-07-28), a protected MCP server over HTTP is an OAuth 2.1 resource server: it publishes Protected Resource Metadata that points clients to its authorization server and accepts only tokens issued for itself. MCP clients discover that authorization server, run the authorization code flow with PKCE, and name the MCP server in a resource parameter on every authorization and token request."
claim: "In MCP revision 2026-07-28, a protected MCP server over HTTP is an OAuth 2.1 resource server that accepts only tokens issued for itself."
slug: mcp-authorization
date: 2026-10-13
draft: false
weight: 40
topics: [agentic-engineering, identity-authentication]
---

This entry describes the Model Context Protocol (MCP) [authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) as of revision 2026-07-28, which the MCP versioning page listed as the current revision on 13 October 2026. Later revisions may change these requirements.

## Key findings

{{< finding id="agent-mcp-protected-resource-metadata" source="Model Context Protocol, Authorization, revision 2026-07-28" url="https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization" >}}As of MCP revision 2026-07-28, MCP servers must implement OAuth 2.0 Protected Resource Metadata (RFC 9728), and MCP clients must use it to discover the authorization server.{{< /finding >}}

{{< finding id="agent-mcp-resource-parameter" source="Model Context Protocol, Authorization, revision 2026-07-28" url="https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization" >}}MCP clients must send the RFC 8707 resource parameter with the MCP server's canonical URI in both authorization and token requests, whether or not the authorization server supports it.{{< /finding >}}

{{< finding id="agent-mcp-audience-validation" source="Model Context Protocol, Authorization, revision 2026-07-28" url="https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization" >}}MCP servers must validate that an access token was issued specifically for them as the intended audience and must not accept or transit any other tokens.{{< /finding >}}

{{< finding id="agent-mcp-no-token-passthrough" source="Model Context Protocol, Authorization Security Considerations, revision 2026-07-28" url="https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations" >}}An MCP server that calls upstream APIs must use a separate token from the upstream authorization server and must not pass through the token it received from the MCP client.{{< /finding >}}

## Evidence

{{< studies caption="Primary sources on MCP authorization" >}}
{{< study title="Model Context Protocol: Authorization (revision 2026-07-28)" org="Model Context Protocol" year="2026" sample="n/a" method="Specification" url="https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization" >}}Defines roles, discovery, the authorization flow, the resource parameter, token handling and step-up authorization for HTTP transports.{{< /study >}}
{{< study title="Model Context Protocol: Authorization Security Considerations (revision 2026-07-28)" org="Model Context Protocol" year="2026" sample="n/a" method="Specification" url="https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations" >}}Requires audience binding, PKCE, exact redirect URI matching and a ban on token passthrough.{{< /study >}}
{{< study title="OAuth 2.0 Protected Resource Metadata (RFC 9728)" org="IETF" year="2025" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc9728" >}}Defines the metadata document and the WWW-Authenticate parameter that point a client to a resource's authorization servers.{{< /study >}}
{{< study title="Resource Indicators for OAuth 2.0 (RFC 8707)" org="IETF" year="2020" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc8707" >}}Defines the resource parameter and asks authorization servers to audience-restrict tokens to it.{{< /study >}}
{{< study title="Economies of Scale for MCP and Agents" org="this site" year="2026" sample="n/a" method="Talk" url="https://www.janbrennenstuhl.eu/talks/economies-of-scale-for-mcp/" >}}States that an agent should not hold a shared, long-lived provider credential and presents the broker's delegation model.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

For an MCP server over HTTP, publish Protected Resource Metadata, answer unauthenticated requests with a 401 that points to it, and check the audience of every token. Put the scopes an operation needs in the `WWW-Authenticate` challenge, all at once. If the server calls other APIs, get its own token for each of them. The [token exchange entry]({{< ref "/knowledge-base/agent-identity/token-exchange" >}}) shows one way to do that.

For an MCP client, implement both discovery mechanisms, PKCE with `S256`, the `resource` parameter, and the issuer check. Never put tokens in the query string.

An MCP server on the STDIO transport is outside this specification, which says such servers should take credentials from the environment. Keep those credentials short-lived and task-scoped, as my [AppSec essay]({{< ref "/post/appsec-agentic-engineering" >}}) recommends for coding agents.

### For product and UX

Start with the minimal scopes and ask for more only when an operation needs them. The specification warns that misconfigured scopes may require frequent user interaction, and that challenging one scope at a time forces several authorization round-trips for one operation.

## How it works

The specification defines 3 roles. The MCP server is an OAuth 2.1 resource server, the MCP client is an OAuth 2.1 client acting for a resource owner, and the authorization server issues the tokens. Authorization is optional for MCP implementations. Implementations on HTTP-based transports should conform to the specification, and STDIO implementations should not.

A first connection follows these steps:

1. The client sends an MCP request without a token. The server answers with HTTP 401 and a `WWW-Authenticate` header that carries the `resource_metadata` URL from RFC 9728 and, as the specification recommends, the required `scope`.
2. The client fetches the Protected Resource Metadata and picks an authorization server from it. It then reads that server's metadata through OAuth 2.0 Authorization Server Metadata (RFC 8414) or OpenID Connect Discovery. Clients must support both, and if the metadata doesn't list `code_challenge_methods_supported`, the client must refuse to proceed.
3. The client gets a client ID. It uses pre-registered client information if it has some, then Client ID Metadata Documents if the authorization server supports them. Dynamic Client Registration is deprecated and kept only as a fallback for backwards compatibility.
4. The client starts the authorization code flow with PKCE, the `resource` parameter and the selected scopes, and records the expected issuer. When the response comes back, it validates the `iss` parameter (RFC 9207) before it redeems the code.
5. The client redeems the code with the `code_verifier` and the `resource` parameter, then sends the access token in the `Authorization: Bearer` header on every request.

When a token lacks a scope at runtime, the server answers with 403 and `error="insufficient_scope"`. The client then runs a step-up flow with the union of its previous scopes and the new ones.

Revision 2026-07-28 doesn't cover token exchange in its core authorization pages. Optional authorization extensions live in a separate repository. In the Agentic Identity Broker, which Magnus Jungsbluth and I built, an MCP gateway exchanges the agent's token for the matching provider token through RFC 8693, so the provider token never reaches the agent. I describe that design in the [retrospective]({{< ref "/post/agentic-identity-broker" >}}), and we presented it in our [AGNTCon + MCPCon talk]({{< ref "/talks/economies-of-scale-for-mcp" >}}).

## Related

- [Should an agent use a robot account or delegated access?]({{< ref "/knowledge-base/agent-identity/delegation-vs-robot-accounts" >}})
- [How should people grant and revoke an agent's access?]({{< ref "/knowledge-base/agent-identity/consent-and-revocation" >}})
- [Agentic Identity Broker]({{< ref "/projects/agentic-identity-broker" >}})
