---
title: "State of the Broker: October 2026"
description: "The first full month of the open-source Agentic Identity Broker: security hardening, third-party OAuth 2.0 features, session fixes, Spec Kit automation and the first outside write-ups."
claim: "In its first full month as open source, the Agentic Identity Broker gained third-party OAuth 2.0 features and its first outside contributors, while session stability and running Spec Kit on GitHub took the most work."
lead: "October was our first full month as an open-source project. We hardened the release, connected more third-party OAuth 2.0 services, fought lost sessions, moved Spec Kit onto GitHub, and three people landed their first commits."
date: 2026-11-06
slug: state-of-the-broker-october-2026
tags: ["agentic-engineering", "oauth2", "open-source"]
series: "state-of-the-broker"
findings:
  - id: sotb-2026-10-activity
    text: "In October 2026, its first full month as open source, the Agentic Identity Broker merged 95 pull requests, published 60 releases and gained 3 first-time contributors."
  - id: sotb-2026-10-sessions
    text: "Lost third-party sessions were the broker's most visible problem in October 2026; the fixes cover unnecessary logouts, re-consent after a failed refresh, proactive refresh and refresh tokens that a provider rejected with invalid_grant."
  - id: sotb-2026-10-speckit
    text: "The broker's Spec Kit phases now run as GitHub Agentic Workflows that maintainers steer with slash commands; getting there took 8 fixes and 9 failed or incomplete runs in October 2026."
draft: true
---

October was the first full month of the [Agentic Identity Broker](https://github.com/zalando-incubator/agentic-identity-broker "Agentic Identity Broker source repository") as an open-source project. The team spent the first half of it hardening what we had published on 15 September, and the second half adding the features that people asked for once they connected the broker to real third-party services. Along the way, three people landed their first commits, and we moved most of our spec-driven workflow onto GitHub.

This is the first post of a monthly series. Each month, I want to write down what changed in the broker, how the project numbers moved, who wrote about it, what got in the way and what we look at next. If you are new to the broker, my [retrospective on building it with coding agents]({{< ref "/post/agentic-identity-broker/index.md" >}} "What I Learned Building an Identity Broker With Coding Agents") explains what it does and why we built it.

## Hardening what we released

The first two weeks of October were mostly security fixes, some of them for findings from dependency and code scanners ([#192](https://github.com/zalando-incubator/agentic-identity-broker/pull/192), [#272](https://github.com/zalando-incubator/agentic-identity-broker/pull/272)) as well as agentic security assessments using Claude Mythos 5.1 and OpenAI's Daybreak Blue. I made the broker reject wildcard CORS origins ([#170](https://github.com/zalando-incubator/agentic-identity-broker/pull/170)), redact rejected PostgreSQL connection URLs from its logs ([#167](https://github.com/zalando-incubator/agentic-identity-broker/pull/167)) and limit where its admin API is reachable ([#155](https://github.com/zalando-incubator/agentic-identity-broker/pull/155)). I also restricted the TLS bypass for the key management service to explicit development setups ([#168](https://github.com/zalando-incubator/agentic-identity-broker/pull/168)) and closed a server-side request forgery (SSRF) bypass in the fetcher for Client ID Metadata Documents (CIMD) in production ([#169](https://github.com/zalando-incubator/agentic-identity-broker/pull/169)).

The second theme was observability. I taught the broker to classify why it denies a grant authorization ([#197](https://github.com/zalando-incubator/agentic-identity-broker/pull/197)) and to record grant lifecycle changes in its audit log ([#201](https://github.com/zalando-incubator/agentic-identity-broker/pull/201)). My refactoring of the classification contract had a side effect: it dropped audit fields from the Open Policy Agent (OPA) integration, and we had to restore them a few days later ([#219](https://github.com/zalando-incubator/agentic-identity-broker/pull/219)).

## Connecting more third-party services

Most new features that arrived in October make it easier to connect the broker to OAuth 2.0 services that we don't control. The team added discovery of OAuth 2.0 protected resources for third-party services ([#191](https://github.com/zalando-incubator/agentic-identity-broker/pull/191)), so an operator no longer has to list every protected resource by hand. We also made it possible to supply a trust anchor's public keys inline or from a file ([#221](https://github.com/zalando-incubator/agentic-identity-broker/pull/221)) instead of fetching them from a JSON Web Key Set (JWKS) URL. I added filesystem credential sources ([#183](https://github.com/zalando-incubator/agentic-identity-broker/pull/183)), so client secrets for third-party services can come from mounted files.

CIMD clients can now authenticate with `private_key_jwt` ([#237](https://github.com/zalando-incubator/agentic-identity-broker/pull/237)), which unblocks ChatGPT as a client ([#220](https://github.com/zalando-incubator/agentic-identity-broker/issues/220)). A token exchange can now expect a different audience in its client assertion ([#283](https://github.com/zalando-incubator/agentic-identity-broker/pull/283)). We also added public outbound CIMD clients ([#280](https://github.com/zalando-incubator/agentic-identity-broker/pull/280)) and allowlisted private-use redirect URIs for agents ([#273](https://github.com/zalando-incubator/agentic-identity-broker/pull/273)).

For people running the broker in Kubernetes, the Helm chart can now deploy extra manifests ([#254](https://github.com/zalando-incubator/agentic-identity-broker/pull/254)) and schedule the job that sweeps expired sessions, and the broker reports session health metrics ([#247](https://github.com/zalando-incubator/agentic-identity-broker/pull/247)).

## Keeping users logged in to third-party services

The most visible problem in October was that users lost their third-party sessions too often. When a provider session ends, the user has to go back to the consent screen before the agent can use that service again. We attacked this from several sides. I reduced unnecessary session logouts ([#218](https://github.com/zalando-incubator/agentic-identity-broker/pull/218)) and fixed how the broker asks for consent again when a refresh fails ([#200](https://github.com/zalando-incubator/agentic-identity-broker/pull/200)). We specified proactive token refresh ([#196](https://github.com/zalando-incubator/agentic-identity-broker/pull/196)), and I added regression tests for it ([#217](https://github.com/zalando-incubator/agentic-identity-broker/pull/217)). At the end of the month, we made the broker stop refreshing a refresh token that the provider has already rejected with `invalid_grant` ([#271](https://github.com/zalando-incubator/agentic-identity-broker/pull/271)), and the session card in the UI now offers a new login only when the session can no longer be renewed ([#300](https://github.com/zalando-incubator/agentic-identity-broker/pull/300)).

[PLACEHOLDER: Jan, add whether users still report lost sessions after these fixes. I could not verify that from public sources.]

## Running Spec Kit on GitHub

We build the broker spec-first with [Spec Kit](https://github.com/github/spec-kit "Spec Kit"), and until October that workflow ran in each maintainer's local agent harness. In October, we moved it onto GitHub. Since [#238](https://github.com/zalando-incubator/agentic-identity-broker/pull/238), [GitHub Agentic Workflows](https://github.github.com/gh-aw/ "GitHub Agentic Workflows") run the Spec Kit phases (specify, plan, implement) with the Pi coding agent, and maintainers steer them with slash commands in pull requests ([#295](https://github.com/zalando-incubator/agentic-identity-broker/pull/295)). A maintainer now signs off on a decision with a single 👍 ([#315](https://github.com/zalando-incubator/agentic-identity-broker/pull/315)), and each pull request gets one status comment instead of a wall of them ([#317](https://github.com/zalando-incubator/agentic-identity-broker/pull/317)). On 30 October, we also added a grumpy reviewer, a workflow that answers questions about the repository, and an architecture review agent that only a maintainer can start ([#326](https://github.com/zalando-incubator/agentic-identity-broker/pull/326), [#327](https://github.com/zalando-incubator/agentic-identity-broker/pull/327), [#328](https://github.com/zalando-incubator/agentic-identity-broker/pull/328)).

Getting there took quite some iterations. In October, the workflows filed 9 issues about their own failed or incomplete runs, and we merged 8 fixes for phase handoffs, feature selection and the sandbox of the implement phase. We also changed our constitution twice: version 4.1.0 keeps each feature within its scope and defers unrelated findings ([#228](https://github.com/zalando-incubator/agentic-identity-broker/pull/228)), and version 4.2.0 requires concrete examples in every feature spec ([#229](https://github.com/zalando-incubator/agentic-identity-broker/pull/229)).

## Thank you, new contributors

Three people landed their first commits in October. Santhosh K made the Helm chart deploy extra manifests ([#254](https://github.com/zalando-incubator/agentic-identity-broker/pull/254)), scheduled the session sweep from the chart with session health metrics ([#247](https://github.com/zalando-incubator/agentic-identity-broker/pull/247)) and fixed several session and token endpoint issues, such as refreshing tokens that a provider had already rejected ([#271](https://github.com/zalando-incubator/agentic-identity-broker/pull/271)). João Santos added `private_key_jwt` authentication for CIMD clients ([#237](https://github.com/zalando-incubator/agentic-identity-broker/pull/237)). XY picked up a good first issue and added the client assertion audience for token exchange ([#283](https://github.com/zalando-incubator/agentic-identity-broker/pull/283)). Thank you!

## The month in numbers

| Measure | October 2026 |
| --- | --- |
| Commits on `main` | 93, of which 12 from Dependabot |
| Pull requests opened / merged | 139 / 95 |
| Issues opened / closed | 33 / 15 |
| Releases | 60, from `v0.1.69` to `v0.1.128` |
| People with commits | 7, of them 3 for the first time |
| Stars | 34 on 30 October, from 27 on 1 October |
| Forks | 5 on 30 October |

The broker publishes a release for almost every merge to `main`, so the release count says more about our merge rate than about features. The two of us who maintain the broker still wrote most of the commits: 67 of 93, 35 of them mine.

## Who wrote about the broker

Alejandro Saucedo published [the second part of his series on agent security and identity](https://ethical.institute/newsletter/407/ "Agentic Security & Identity, Part 2") on 4 October. He runs the broker on a local Kubernetes cluster with his Kubernetes Agent Orchestration System (KAOS) and walks through allowed and denied requests for two users and two agents. HackerNoon republished [part 1](https://hackernoon.com/agent-security-and-identity-part-1-who-are-you-whos-your-agent-and-what-should-they-be-allowed "Agent Security & Identity (Part 1)") on 21 October and [part 2](https://hackernoon.com/agent-security-and-identity-part-2-who-are-you-whos-your-agent-and-what-should-they-be-allowed "Agent Security & Identity (Part 2)") on 23 October. The [KAOS documentation](https://axsaucedo.github.io/kaos/dev/security/walkthrough-agent-identity.html "KAOS: Agent identity") also lists the broker as one of three agent identity issuers.

On 9 October, Mike Moore from Solo.io, the company that created agentgateway, published [a guide to token exchange in agentgateway](https://webofmike.com/agentgateway-token-exchange/ "agentgateway Token Exchange for AI Agents") with a case study on the broker. He points out that our gateway guide used the broker's own external processing sidecar instead of agentgateway's native `oauthTokenExchange` policy. That was true at the time, and we documented the native policy at the start of November ([#275](https://github.com/zalando-incubator/agentic-identity-broker/pull/275)).

## What we look at next

Three topics take most of our attention right now:

- Moving beyond on-behalf-of cases, where a person delegates to an agent, so that the broker also supports headless agents that a machine invokes instead of a human.
- An activity and audit ledger that will power the activity UI I proposed in an [issue for an activity API](https://github.com/zalando-incubator/agentic-identity-broker/issues/188 "Activity API for the broker UI") and other auditing interfaces.
- Making the repository more ready for agents and improving the agentic support for maintaining it, building on the Spec Kit workflows from October.

We also opened several design issues in October that show where the broker could go. One proposes an [AuthZEN Access Evaluation endpoint](https://github.com/zalando-incubator/agentic-identity-broker/issues/289 "Broker AuthZEN Access Evaluation endpoint as Delegation Policy Information Point"), so that policy engines can ask the broker about delegations in a standard format. Another proposes [incremental authorization with per-service virtual scopes](https://github.com/zalando-incubator/agentic-identity-broker/issues/299 "Incremental authorization: per-service virtual scopes for MCP step-up") for MCP step-up, which would fix a re-authentication loop with optional services. A third reopens the [granularity of the consent screen](https://github.com/zalando-incubator/agentic-identity-broker/issues/285 "design: Overhaul Consent Screen Granularity"). I also opened an issue for a [pluggable interface for an external decision model](https://github.com/zalando-incubator/agentic-identity-broker/issues/206 "Pluggable interface for an external decision model").

[PLACEHOLDER: trends you saw in October, for example in IETF work on agent identity or vendor products. Add only what you can link.]

If you run the broker and something gets in your way, please [open an issue](https://github.com/zalando-incubator/agentic-identity-broker/issues "Agentic Identity Broker issues"). In October, people outside the maintainers asked for `client_secret_basic` on the token endpoint ([#314](https://github.com/zalando-incubator/agentic-identity-broker/issues/314)) and for Google scope hierarchies in token exchange ([#313](https://github.com/zalando-incubator/agentic-identity-broker/issues/313)), and I'd like to cover more of these requests in next month's post.
