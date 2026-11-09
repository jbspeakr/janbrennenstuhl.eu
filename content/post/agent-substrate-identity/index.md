---
title: "Agent Substrate Knows Which Agent Is Calling, but Not for Whom"
linkTitle: "Agent Substrate and Delegation"
description: "Agent Substrate 1.0, kagent and agentgateway form a Kubernetes agent platform that keeps credentials out of the sandbox, but every identity in it names only the agent. A proof of concept shows how the Agentic Identity Broker can add the person behind the agent, and that neither the platform nor the broker is ready for it yet."
claim: "Agent Substrate tells a credential provider which actor is asking but not which person delegated. The Agentic Identity Broker can check the person's grant behind the egress gateway, but only the platform can attest which person an actor runs for."
date: 2026-11-09
slug: agent-substrate-identity
tags: ["agentic-engineering", "oauth2", "platform-engineering"]
findings:
  - id: substrate-provider-actor-only
    text: "Agent Substrate's egress gateway asks a credential provider for a secret with exactly 2 fields, the credential URI and the verified actor's SPIFFE ID, so the provider can authorize the actor but never learns on whose behalf it acts, whether that is a person, a workload or another agent."
  - id: kagent-person-or-agent
    text: "On kagent 1.0, a tool receives either the caller's own bearer token or a minted actor JWT, so it sees the person without the agent or the agent without the person, and neither option is delegation in the sense of RFC 8693."
  - id: substrate-broker-behind-gateway
    text: "In a local proof of concept on Substrate's agentgateway dataplane, the Agentic Identity Broker worked as a credential provider behind a small shim, but a revoked grant only denied the next request from a running actor after I disabled agentgateway's default 300-second credential cache for that provider. Which person the actor acted for came from a mapping I wrote by hand, because the platform doesn't provide that information yet."
---

On 5 November, Google [handed Agent Substrate to the CNCF](https://opensource.googleblog.com/2026/11/sandboxing-untrusted-ai-agents-at-scale.html "Sandboxing Untrusted AI Agents at Scale: Google Donates Agent Substrate and gVisor to the CNCF"), and [Substrate 1.0](https://github.com/agent-substrate/substrate/releases "Agent Substrate releases") came out the same day. Substrate is a runtime for sandboxed agents on Kubernetes. It suspends idle agents to snapshots and wakes them when the next request arrives, and it gives every agent an identity and a guarded way out to the network.

For me, the stack that forms around Substrate matters more than the donation. Substrate is the bottom layer: it runs the sandboxes and the egress gateway that every request leaves through. That gateway comes in an Envoy flavour, the default, and an [agentgateway](https://agentgateway.dev/ "agentgateway") flavour, and agentgateway is the gateway that the token-exchange integration of the [Agentic Identity Broker]({{< ref "/projects/agentic-identity-broker" >}}) (AIB) I co-authored already targets. On top, [kagent](https://kagent.dev/ "kagent"), the Kubernetes agent framework that Solo.io started and donated to the CNCF, has moved its runtime off Kubernetes Deployments and onto Substrate. With [kagent 1.0](https://kagent.dev/docs/kagent/1.x/reference/release-notes/1.0/ "kagent 1.0 release notes"), released on 9 November, every conversation gets its own Substrate sandbox.

A Kubernetes-native agent platform is taking shape out of parts that Magnus Jungsbluth and I have worked with since we started the broker, and I wanted to know where it fits into that platform. Substrate makes the rule we have been preaching, keep provider tokens out of the agent, a platform default. But every identity it issues is a workload identity. When its gateway asks a credential provider for a secret, the provider learns which agent is asking but never on whose behalf. In the terms of RFC 8693, the OAuth 2.0 token exchange standard, the request carries the actor but no subject, whoever that subject is: a person, a workload or another agent. The case I currently care about is the person, because a person granting and revoking an agent's access is exactly what Magnus and I initially built the broker for.

So I had a coding agent plug the AIB into Substrate as a credential provider to explore the expected rough edges. The token exchange worked, but only because I supplied the person by hand. Neither side is ready for this setup today: Substrate and kagent don't pass the person on to the credential provider, and the broker's third-party exchange can't yet accept Substrate's token for the agent next to the person's token, which a proper delegation exchange needs.

## Substrate Keeps Credentials Out of the Sandbox

Substrate calls each stateful workload an actor and runs it on a pool of pre-started workers. The project's [security principles](https://github.com/agent-substrate/substrate/blob/main/docs/security/security.md "Agent Substrate: Security") put the default in one sentence: "Default actor sandboxes execute completely credential-free."

To call an API that needs a bearer token, an actor sends a placeholder. The actor reaches the network only through Substrate's egress gateway, and an `EgressPolicy` rule can tell that gateway to replace a header on the way out:

```yaml {filename="egress-policy.yaml"}
rules:
- https:
    hostnames: ["api.example.com"]
    effects:
      replaceHeaders:
      - header: Authorization
        prefix: "Bearer "
        credentialUri: ate-secret://k8s.io/default/ns1/example-api/token
```

The actor sends `Authorization: Bearer placeholder`. The gateway terminates the actor's TLS for that host, asks a credential provider for the secret behind the URI, swaps the placeholder for the real value and opens a fresh TLS connection to the origin, so the token never exists inside the sandbox. If the provider says no or is down, the request fails closed, as the [credential injection guide](https://ate.dev/docs/guides/egress-credential-injection/ "Agent Substrate: Egress credential injection") describes.

Instead of a stored secret, the rule can also ask for an actor JSON Web Token (JWT). Substrate's API server mints it for the calling actor, and the gateway injects it the same way. The actor never touches this token either. Substrate makes sure that nothing inside the sandbox can speak for the actor. The gateway reads the actor's identity from a client certificate that `atunnel`, a process outside the sandbox, presents on the tunnel. Substrate's API server signs that certificate for the actor's current UID, and the gateway accepts it only while the actor still exists under that UID and is running or resuming. Nothing the actor writes into a request contributes to that decision.

So Substrate basically applies [Shift Down]({{< ref "/post/appsec-shift-down/index.md" >}} "Shift Down: Why Agentic Engineering Demands Platform-Level Security") concepts to agents: it treats the agent as untrusted code, keeps secrets outside its boundary and decides at a point the platform controls. Until now, a platform team had to build that. With Substrate, it comes with the runtime.

## Substrate Never Tells Anyone Whom the Agent Works For

When the gateway asks a credential provider for a secret, it sends exactly two fields, over mTLS with its own workload identity. This is the complete request from Substrate's [credential provider API](https://github.com/agent-substrate/substrate/blob/main/api/credprovider/v1/credprovider.proto "credprovider.proto"), with the comments shortened:

```protobuf {filename="credprovider.proto"}
message FetchSecretRequest {
  // ate-secret://<provider name>/<provider tail>
  string uri = 1;
  // The SPIFFE ID of the actor on whose behalf the secret is fetched,
  // as verified by the egress gateway.
  string actor_spiffe_id = 2;
}
```

The provider learns which secret is wanted and which actor wants it, and nothing else. The field comment calls the actor the party "on whose behalf the secret is fetched", so in Substrate's model the actor is the subject, and nobody stands behind it. Substrate's docs ask providers to authorize the actor, and the bundled Kubernetes Secrets provider does just that: it maps each atespace, Substrate's tenancy boundary, to the namespaces whose Secrets its actors may read. That's fine for a shared API key. A delegated token is a different story: a person's GitHub token, or a token a workload handed to the agent for one job. The provider should only hand it out if that subject allowed this agent to act for them.

The actor JWT has the same limitation. Its subject is `actor/<atespace>/<name>`, and its claims carry the atespace, the actor name and the actor's UID. Every claim describes the workload, and none names a delegating subject. According to Substrate's [actor JWT guide](https://ate.dev/docs/guides/actor-jwts/ "Agent Substrate: Actor JWTs"), the token also can't be revoked, so it stays valid for up to an hour, even after its actor is deleted. The gateway also caches tokens by actor name. The guide lists the consequence as a known limitation: an actor that is deleted and recreated under the same name "can get its predecessor's token until that token's refresh point, up to two thirds of its lifetime, and that token's UID claim names the old actor."

For a general-purpose runtime, that's the intended boundary. Substrate's security principles place the application outside it: "Your application is outside these boundaries: it authenticates end users and decides which actors they can reach." The same document lists agent lineage, "who made this sub-sub-sub agent", as the application's job and marks sub-actor provenance as out of scope. It does mean though that an agent using a Secret behind `credentialUri` pretty much acts as a robot account, just with better hygiene. When several people share such an agent, it acts with their combined permissions, and the service at the other end can't tell whose request was whose. I wrote up why that matters in my [field guide entry on robot accounts and delegation]({{< ref "/knowledge-base/agent-identity/delegation-vs-robot-accounts" >}}).

## kagent Passes Either the Person or the Agent

kagent runs each Session, a single conversation, as its own actor. kagent's [identity documentation](https://kagent.dev/docs/kagent/1.x/about/substrate-runtime/identity/ "kagent: Identity") shows the actor JWT for such a Session:

```json {filename="actor-jwt-claims.json"}
{
  "iss": "https://idp.ate-system.svc",
  "sub": "actor/kagent/session-01a18e6c-4454-7597-ba2b-e962d0f53967",
  "aud": ["ticket-api"],
  "actor.ate.dev": {
    "atespace": "kagent",
    "actorName": "session-01a18e6c-4454-7597-ba2b-e962d0f53967",
    "actorUID": "3d0d0f07-40fb-4493-a7cd-3cb7f2d79c3b"
  }
}
```

kagent offers two options that come close to answering "for whom", and its [tools documentation](https://kagent.dev/docs/kagent/1.x/skills-and-mcp/about-tools/ "kagent: About tools") describes the trade-off. With `tokenPassthrough: true`, the agent sends the bearer token from the incoming Agent2Agent (A2A) request to the MCP server, which identifies the user who started the Session. With `actorJwt`, the gateway injects a token like the one above, which identifies the calling actor.

Neither option is delegation as [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693#section-1.1 "RFC 8693, Section 1.1: Delegation vs. Impersonation Semantics") defines it. Passthrough has the RFC's impersonation semantics: the Model Context Protocol (MCP) server sees the person and has no way to know that an agent is acting for them. It also only works where the token that authenticated the person to kagent was issued for the MCP server too, because the [MCP authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization#token-handling "MCP Authorization: Token Handling") requires servers to "validate that access tokens were issued specifically for them as the intended audience". That is a deployment choice, and it still doesn't tell the server that an agent is in the loop.

The actor JWT is the mirror image: it names the agent and drops the person. Delegation needs both parties in the exchange: the delegating subject, here the person, as the subject token and the agent as the actor token. When the broker issues the resulting token itself, both end up in it, the person as `sub` and the agent in the `act` claim. When the result is a third-party token such as a GitHub token, that token can't carry an `act` claim, so the record of who delegated to whom has to live wherever the exchange happens. My [guide on token exchange]({{< ref "/knowledge-base/agent-identity/token-exchange" >}}) walks through how a gateway gets such a token.

Interestingly, the delegating subject seems only one lookup away. kagent records a creator on every Session, which is the principal of the call that created it, and each Session runs as its own actor. So the chain from actor to Session to creator sits in kagent's database and never leaves it. Even `ResolveAgentIdentity`, the method a service can call with an actor token, returns the Agent, the Session ID and the revision, but not the creator. And the creator isn't necessarily a person. A workload can create Sessions as its Kubernetes ServiceAccount, and kagent can verify that token with the Kubernetes API if an operator turns the option on. A person's token is a different matter. In the default `insecure` mode, the caller names its own principal in a header. The `trusted-proxy` mode decodes the bearer token without verifying it and trusts a proxy in front to have done that, which works as long as nothing can reach the controller around the proxy. kagent's own docs add that creator scoping, which hides one creator's Sessions from another, "is not a security boundary". Its [design notes on credential injection](https://github.com/kagent-dev/kagent/blob/main/docs/architecture/credential-injection.md "kagent: Credential injection") are just as clear about the other side: "Kagent never names a credential provider", and kagent doesn't exchange actor JWTs for anything. A [feature request](https://github.com/kagent-dev/kagent/issues/3470 "kagent issue #3470: Anthropic Workload Identity Federation via Substrate token exchange") for such an exchange was closed as not planned on 1 November.

The creator could still find its way to the egress side. Two open issues from 29 October ask for exactly that: Jose Armesto from Giant Swarm proposed to [give egress policy compilers the Session, including its creator](https://github.com/kagent-dev/kagent/issues/3441 "Egress policy compilers: give them the Session, and let a Session add destinations"), so that whoever builds the actor's egress policy knows whom the Session belongs to, and [a per-turn phase for credentials](https://github.com/kagent-dev/kagent/issues/3440 "Egress policy compilers: a per-turn phase for credentials that should exist only while a turn runs"), so that a credential bound to that person exists only while a turn runs and not for the actor's whole life. The kagent maintainers pushed back on both designs the same day, and he has since reworked them: a Session's destinations would live on the Session itself, and an admission hook in `CreateSession` would see the caller. His team runs a version of this in their fork and has offered the code. Nothing has landed upstream yet.

## Where the Agentic Identity Broker Fits

The Agentic Identity Broker answers the question that `FetchSecretRequest` leaves open. A user grants an agent access to a service with a chosen permission set and an optional expiry, and can revoke that grant at any time. On a tool call, a privileged gateway authenticates to the broker with a signed client assertion and presents a subject token that names the user (`sub` by default) and the agent (`azp` by default). The broker checks for an active grant for that user, agent and service, and only then hands over the stored provider token. Like Substrate, the broker keeps provider tokens away from the agent, because its gateway integration [exchanges tokens on each tool call]({{< ref "/knowledge-base/agent-identity/token-exchange" >}}). The [token exchange documentation](https://agenticidentitybroker.dev/docs/concepts/token-exchange "Agentic Identity Broker: Token exchange") has the details.

Put that next to Substrate and the pieces line up with the architecture Magnus and I presented at [AGNTCon + MCPCon]({{< ref "/talks/economies-of-scale-for-mcp" >}}), just on a new runtime. The gateway in front of the agent is Substrate's egress gateway, which already holds each request at the moment the broker wants to decide. The agent's identity is the actor JWT, which could make a proper RFC 8693 `actor_token`. Or it is simply the actor SPIFFE ID that the gateway already attests to the provider. The person's identity is their own token, the `subject_token`. The exchange happens at the gateway, and the provider token travels from the broker through the gateway to the upstream without ever entering the sandbox. Substrate has built the gateway half of our talk into the platform, and the broker's existing integration already runs inside agentgateway, which Substrate offers as its second dataplane.

## Wiring the Broker Into Substrate

The broker can't do its half of that exchange yet. Its third-party exchange today reads both the user and the agent from one subject token, and accepting a Substrate actor JWT as a separate actor token is work I'd like to see us do. But the two looked close enough that I had a coding agent build a local proof of concept (POC) with what exists now, and I ran it on 9 November on Substrate's agentgateway dataplane, after a first run on Envoy four days earlier. The setup was the broker's Docker Compose stack next to a Substrate build from 5 November, the day 1.0 came out, on a kind cluster with gVisor actors and agentgateway v1.7.0 as both ingress router and egress gateway, plus a small gRPC shim that implements `CredentialProvider.FetchSecret` and talks to the broker. On each call, the shim looked up the verified actor SPIFFE ID in a read-only Kubernetes Secret that mapped it to a person's broker subject token, which I had exported by hand. It then ran a token exchange at the broker, without caching. The upstream was a mock GitHub-style `/user` endpoint that verified the provider token.

The first run simply worked. A sandboxed actor sent `Authorization: Bearer placeholder` to the mock, the gateway called the shim with `ate-secret://aib.local/github/token` and the actor's SPIFFE ID, the broker logged a third-party exchange for the person, the agent and the grant, and the actor got its 200. The token fingerprint in the shim's log matched the one the mock received. The actor's response and its container logs contained neither the provider token nor its fingerprint.

The test I actually cared about was revocation. I withdrew the grant in the broker and sent exactly one more request from the same running actor, through the same gateway, with the same unexpired subject token, without restarting or redeploying anything. On agentgateway, that request still succeeded, and the broker was never asked. Only after I turned caching off for the broker's provider did the request after revocation come back as a 403, backed by a fresh broker exchange that reported `access_denied`. The remaining cases failed closed as well: a grant whose provider session had been removed got a 403 with the broker's distinct `invalid_grant` error, an actor without a binding got a 403 before the shim even contacted the broker, and an unreachable broker produced a retryable 503.

Revocation is where a grant in the broker differs most from an actor JWT. An actor JWT can't be revoked, and the gateway mints a fresh one whenever a resumed actor makes its next call, however long ago the person last looked. Substrate can cut an actor's egress entirely, which its security status lists as dynamic egress revocation, but that is an operator stopping the agent, not a person withdrawing their delegation. Because the broker checks the grant on each exchange, the agent gets no new provider token after a person revokes the grant, whether its actor was running or suspended in the meantime. That holds only as long as the gateway actually asks: a credential cache in front of the provider delays the decision by its TTL, and provider tokens that were already issued stay valid until they expire.

Of course, a POC that only shows what works isn't worth much. The discovered gaps and workarounds I needed say more than the success:

- My coding agent wrote a gRPC shim that turns `FetchSecret` into a broker token exchange. The broker can't act as a Substrate credential provider on its own yet, and its third-party exchange can't take the actor JWT as a separate actor token.
- I mapped each actor to a person in a Kubernetes Secret, keyed on the actor's SPIFFE ID, which names the atespace and the actor, not its UID. Neither Substrate nor kagent provides that link.
- The shim borrowed the client identity of the broker's agentgateway integration, so the broker couldn't tell the two apart.
- The person's subject token was a copy I exported by hand. Nothing in the setup brought the person's own token to the broker.
- agentgateway's default credential cache delayed revocation by up to 5 minutes without any sign of it. Substrate's provider API has no way for a provider to say that its answers must not be cached.
- When a grant or a provider session was missing, the broker's consent or recovery link went nowhere. `FetchSecret` returns opaque bytes or a gRPC error, and the gateway turns both into a 403 or 503 with a generic body. Substrate has no way to bring that link back to the person, who is the only one able to fix the problem.

The token exchange itself works, but today neither the platform, Substrate and kagent, nor the AIB makes this integration easy. Each item on that list is a piece that someone still has to build.

## What It Takes to Make This Work

The most important piece is the link from actor to person. The broker must not trust the actor, or anything the actor writes into a request, to say whom it acts for, so the person has to come from the platform. The link should also name the actor's UID, not just its name, because a recreated actor inherits its predecessor's name and potentially its cached token. I see at least two ways to get there:

1. kagent binds the Session's creator to the actor when it creates the Session, in the direction of issue #3441, and the provider reads that binding. This also covers unattended, headless agent runs, where no person is present. But it only means something once kagent actually authenticates the creator. The default `insecure` mode lets the caller name its own principal, so it has no place in such a setup; `trusted-proxy` is fine as long as the verifying proxy is the only way in.
2. The gateway carries the person's own token for the length of a turn and exchanges it at the broker. kagent seems to move that way: a [change merged on 20 October](https://github.com/kagent-dev/kagent/pull/3263 "feat: support gateway token passthrough for embedded controllers") lets a controller that embeds kagent deliver the caller's token at the egress gateway instead of through the agent, and the proposed #3440 would limit such credentials to the time a turn runs. The broker already ships this for agentgateway as an [ExtProc sidecar](https://agenticidentitybroker.dev/docs/guides/token-exchange-gateway "Agentic Identity Broker: Set up token exchange at the gateway"): agentgateway validates the person's token and hands it to the sidecar, which runs the exchange, so the token reaches the broker and never the MCP server. Since v1.5.0, agentgateway can also run that exchange natively, without the sidecar. Combined with the actor's identity, it would be the full delegation exchange from our talk, running at Substrate's gateway.

Substrate's credential provider API is the harder constraint. `FetchSecretRequest` carries a URI and a SPIFFE ID and nothing else, so a native credential provider could never receive the person's token or an actor JWT. Either the API grows a request context, or the exchange moves out of the provider path and into the gateway itself, where the broker's ExtProc already runs and agentgateway's native token exchange already exists. The API also needs a way for a provider to forbid caching of what it returns, and a way to get a consent or recovery link back to the person. The broker's sidecar returns such a link both as a `WWW-Authenticate` challenge and as an MCP URL elicitation, while Substrate's gateway today turns every provider error into a generic 403. The broker needs work on its side too: its third-party exchange has to accept Substrate's actor JWT as the actor token next to the person's subject token, so that one exchange carries both parties. The broker's impersonation profile already takes an actor token and writes an `act` claim, so the groundwork exists.

## If You Work on Substrate or kagent

On the broker side, accepting Substrate's actor JWT as the actor token is the piece I want to discuss with the AIB contributors. The platform side is yours. If you work on Substrate's credential provider API or on kagent's Session egress and see a better place for the person to enter the picture, I'd like to hear about it, in an issue on the [broker repository](https://github.com/zalando-incubator/agentic-identity-broker "Agentic Identity Broker source repository") or directly. If you are new to the broker, my [retrospective]({{< ref "/post/agentic-identity-broker/index.md" >}} "What I Learned Building an Identity Broker With Coding Agents") explains why we started with agent identity in the first place.
