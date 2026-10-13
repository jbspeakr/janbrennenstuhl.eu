---
id: jb-agentic-identity-broker
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['agentic-engineering']
imageDecorative: true
heroArtwork: delegation
title: "What I Learned Building an Identity Broker With Coding Agents"
linkTitle: "Agentic Identity Broker Retrospective"
description: "Lessons from 10 months of building the open-source Agentic Identity Broker with coding agents: Spec Kit, tests that tested nothing, 6 harness switches, and review."
excerpt: "Lessons from 10 months of building the open-source Agentic Identity Broker with coding agents: Spec Kit, tests that tested nothing, 6 harness switches, and review."
lead: "Magnus Jungsbluth and I built the open-source Agentic Identity Broker with coding agents from the first prototype. Over 10 months, I switched agent harnesses 6 times and used 9 models, and most of my lessons are about specs, tests, and review."
slug: agentic-identity-broker
image: agentic-identity-broker.webp
date: 2026-09-24
lastmod: 2026-09-27
draft: false
featured: true
weight: 50
categories: ["software-engineering"]
tags: ["agentic-engineering", "coding-agents", "open-source"]
---

On 18 September 2026, Magnus Jungsbluth and I presented the [Agentic Identity Broker](https://agenticidentitybroker.dev/ "Agentic Identity Broker documentation") at [AGNTCon + MCPCon Europe](https://agntconmcpconeu26.sched.com/event/2RBAI "Economies of Scale for MCP and Agents: Why You Need an Identity Broker") in Amsterdam. We had published [its source code](https://github.com/zalando-incubator/agentic-identity-broker "Agentic Identity Broker source repository") under the MIT license 3 days earlier. The broker lets people in enterprise environments give an AI agent scoped, revocable access to services such as GitHub or Google without handing the agent their credentials.

Magnus is my mentor and the mastermind behind the broker, and I've been his sidekick since we started at the end of 2025. We built the broker with coding agents from the first prototype in January 2026, put the first Model Context Protocol (MCP) server behind it in production in March, and had the first users in April. Over those 10 months, I switched agent harnesses 6 times and worked with 9 models from Anthropic and OpenAI. What kept the project on track through all those changes was the spec work we did up front and the effort we put into verifying every change. Most of what I learned is about specs, tests, and review.

## Why We Started With Agent Identity

Around the end of 2025, new Claude Sonnet and Opus models pushed the hype around agents through the roof. From a platform and security perspective, Magnus and I could see where that would lead. Without central capabilities that come with guardrails, every team would connect its agents to tools in its own way, and cleaning that up later would be very difficult. So we set out to solve the hard parts first: agent identity and access to tools. As far as we could tell, no product covered this at the time.

The quickest way to connect an agent to a tool is a robot account, where the agent holds a long-lived credential for each MCP server or API it calls. That breaks down as soon as several people share the agent. The agent then acts with the combined permissions of all its users, nobody can tell whose request was whose, and anything that tricks the agent can reach for those credentials. I made the case for [delegation and consent infrastructure]({{< ref "/post/appsec-agentic-engineering/index.md" >}} "AppSec in the Age of Agentic Engineering") from the AppSec side earlier this year.

The broker keeps both the user and the agent in every authorization decision. A user grants an agent access to a service with a chosen permission set and an optional expiry, and can revoke that grant at any time. The broker stores the provider tokens encrypted. On each tool call, an MCP gateway such as [agentgateway](https://agentgateway.dev/ "agentgateway") exchanges the agent's token for the matching provider token through [OAuth 2.0 Token Exchange (RFC 8693)](https://www.rfc-editor.org/rfc/rfc8693 "RFC 8693: OAuth 2.0 Token Exchange"), so the provider token never reaches the agent.

Magnus and I describe the platform around the broker and the reasoning behind its design in [the post that announced the release](https://engineering.zalando.com/posts/2026/09/agentic-platform-open-sourcing-agentic-identity-broker.html "Agentic Platform: Open-Sourcing the Agentic Identity Broker"), and our [talk slides](https://agenticidentitybroker.dev/docs/presentations/2026-09-18_agntcon-mcpcon-agentic-identity-broker.pdf "Economies of Scale for MCP and Agents") explain the delegation model. Alejandro Saucedo, who adopted the broker for his Kubernetes Agent Orchestration System (KAOS), covers the identity side in his series [Agentic Security & Identity](https://ethical.institute/blog/agentic-security-and-identity-part-1/ "Agentic Security & Identity, Part 1").

## We Used Spec Kit From the First Day

Magnus had already experimented with GitHub's [Spec Kit](https://github.com/github/spec-kit "Spec Kit source repository") before we started, and he did most of the heavy upfront work on our constitution. With Spec Kit, a team writes its binding principles into a constitution. For each feature, an agent then drafts a specification, a technical plan, and a task list before it writes any code. A newer command, [`/speckit.converge`](https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md "Spec Kit: Agentic spec-driven development"), checks the implementation against all 3 and appends tasks for the gaps it finds. We run implement and converge in turns until converge reports no gaps.

The broker repository shows how much of this piled up in 10 months. As of 26 September, it holds 42 feature specs, 38 architecture decision records (ADRs), and a [constitution](https://github.com/zalando-incubator/agentic-identity-broker/blob/main/.specify/memory/constitution.md "Agentic Identity Broker constitution") with 13 principles at version 2.1.0. Among other things, the principles require that the broker fails closed and forbid custom cryptography. An `AGENTS.md` file at the root sends every agent to the constitution, the relevant ADRs, and more specific `AGENTS.md` files for each part of the code base.

All that setup cost time before the first feature existed, and it pays off every day now. Whether I start an agent on a feature or a new contributor does, the agent reads the same principles, decisions, and earlier specs.

To start a similar project today, I'd own the spec work myself, hand the building to agents, and put more agents on review than on writing.

## Early Models Wrote Tests That Tested Nothing

The models I used in the first months of 2026 failed mostly by inventing things I never asked for and claiming things that weren't true. Tests were our biggest problem, and for code that holds other people's credentials, a passing test suite has to mean something. In those months, I regularly got green test suites for broken behavior. Agents implemented tests halfway or wrote assertions that didn't check anything. Magnus and I spent most of our time getting them to write proper tests.

The constitution records that fight. It requires red-green-refactor test-driven development (TDD), where every test fails before the implementation exists, and a 1:1 mapping from each spec to an end-to-end (E2E) test that covers a complete user flow. Its version history shows that we added the E2E principle later, extended it to browser tests for the frontend, and clarified the rules for the red phase twice.

As of 26 September, the public repository contains about 105,000 lines of Go test code and about 49,000 lines of Go production code, counting non-blank, non-comment lines. We didn't plan that ratio. About a quarter of the test code is E2E tests, which the constitution requires for every spec. I still think the broker needs more tests. I'd love to have a performance test suite and dedicated compliance checks against the RFCs the broker implements. Right now my agents and I are working on the stability, structure, and run time of the existing suites.

## I Wrote Skills for the Libraries the Models Didn't Know

The models' knowledge of the less common libraries we use was really bad. The broker encrypts tokens before storing them with the Go releases of the AWS Encryption SDK and the AWS Cryptographic Material Providers Library, and Claude failed hard at wiring them together. So I wrote a dedicated [skill](https://github.com/zalando-incubator/agentic-identity-broker/tree/main/.agents/skills/aws-crypto-go "aws-crypto-go skill") that the agent loads when a task touches encryption. The skill explains how the pieces fit together, includes a reference and complete examples, and tells the agent never to answer from its training data alone. I still make the cryptography decisions myself.

The repository holds a second [skill](https://github.com/zalando-incubator/agentic-identity-broker/tree/main/.agents/skills/jwx-guide-v4 "jwx-guide-v4 skill") of this kind for version 4 of jwx, the library the broker uses for JSON Web Tokens (JWTs). It tells the agent where to look up the current API before it answers, because earlier versions of that library have a different API.

## Why I Switched Harnesses 6 Times

For the first 4 months, I used Claude Code, mostly with Sonnet 4.5 and 4.6 and some Opus 4.6 on the side. It felt too heavy and talkative for me, so I moved to [Pi](https://pi.dev/ "Pi coding agent") and spent 2 months customizing it. With Pi, I switched from Claude models to GPT-5.4, then GPT-5.5 and GPT-5.6 Terra. After that, I went back and forth between Pi and [oh-my-pi (OMP)](https://omp.sh/ "oh-my-pi"), an opinionated fork of Pi, for about a month. The full sequence was Claude Code, Pi, OMP, Pi, OMP, Pi, and finally OMP, which has been my only harness for the last 2 months. Since we published the broker, I've worked with GPT-6 Sol, GPT-6 Astra, and Claude Fable 5.1, and the agents got better with each step.

Most switches came down to harness details. Early OMP felt more autonomous and proactive than Pi, which I didn't always want. In Pi, I really liked the [pi-lens](https://github.com/apmantza/pi-lens "pi-lens source repository") extension's support for [Opengrep](https://github.com/opengrep/opengrep "Opengrep source repository"), an open-source static analysis engine. OMP is much better nowadays, although I still fight with its advisor, a second model that reads every turn of the main agent and adds notes. I regularly turn the advisor off and (a few days later) on again. I talked about my setup in more detail on the [Beyond Vibe Coding podcast](https://bvc.fm/2026/08/13/010.html "When Coding Agents Ship at Machine Speed, AppSec Has to Move Into the Loop") in August.

What the agents knew about the project never depended on the harness, because the constitution, the specs, the ADRs, the `AGENTS.md` files, and the skills live in the repository.

Anyone starting now should pick a strong harness with good tool support, such as documentation lookup through [Context7](https://context7.com/ "Context7") or web search through [Exa](https://exa.ai/ "Exa"), and shouldn't shy away from frontier models. I found them worth every penny for the broker.

## Review Takes More Agents Than Writing

For the release on 15 September, I squashed the private history into a single public commit. Agents helped remove internal references, build the documentation site, and run security reviews, while I worked on our [OpenSSF Scorecard](https://github.com/ossf/scorecard "OpenSSF Scorecard") results (the Open Source Security Foundation's automated checks of a repository's security practices), designed the wordmark logo, and set up the domain's DNS.

In the first 10 days after the release (15 to 24 September), the repository received 93 pull requests: 51 from me, 7 from Magnus, 26 from Dependabot (GitHub's dependency update bot), and 9 from additional 2 contributors, Alejandro Saucedo and Farasath Ahamed. We merged 58 of them by 24 September.

Nowadays, some agents are always working on the broker. They harden security, improve the test suites and continuous integration (CI), prepare and implement specs for new features, and review changes. Each agent works in its own git worktree, so parallel agents don't overwrite each other's changes. I try to keep it to 2 or 3 agents at a time, but depending on the day and my meeting schedule, it can be 6 to 8. I start most of them myself.

Reviewing is the hard part. Early on, I expected [roborev](https://www.roborev.io/ "roborev"), a local daemon that reviews each commit in the background, to be a great addition to my harness, and I used it extensively. It regularly got lost in endless loops where it fixed and discussed the same or similar issues again and again. Over time it produced more noise and distraction than help. As the models got better and the harnesses got stronger, I left it behind and replaced it with custom review skills in my harness.

The [architecture review agent](https://github.com/zalando-incubator/agentic-identity-broker/blob/main/.github/agents/architecture-review.agent.md "Architecture review agent") in the repository is one example. It reads the constitution, the ADRs, and the port interfaces from the base branch, so a pull request can't rewrite the rules we judge it by. It defaults to skepticism and looks for what agent-written pull requests tend to do: introduce a parallel mechanism instead of extending an existing one, add domain services that only delegate to repositories, and label tests as end-to-end when they cover a single segment of a flow.

Today I regularly have more agents reviewing in parallel than writing code. The README promises that we review every pull request. Agents review the code, and I still review the specs and the E2E tests myself.

## What We Haven't Solved Yet

The broker solves cases where an agent acts on behalf of a human. Autonomous agents are harder: when no human is in the loop and machines or other agents call internal and external tools such as MCP servers, every approach I know of is still brittle. Central tool approvals are in the works, and the [roadmap](https://github.com/zalando-incubator/agentic-identity-broker#roadmap "Agentic Identity Broker roadmap") lists token exchange for agent-to-agent calls, intent-based authorization, and user-facing activity logs.

[AGNTCon](https://agntconmcpconeu26.sched.com/ "AGNTCon + MCPCon Europe 2026 schedule") left me with the impression that the whole industry is still working on the same questions, and the standards are still catching up. Christian Posta from Solo.io gave a talk titled "What IS an Agent's Identity?", and the Identity Assertion JWT Authorization Grant (ID-JAG) talk by Aaron Parecki from Okta, Paul Carleton from Anthropic, and Joey Orlando from Archestra.AI named adoption by software-as-a-service (SaaS) providers as the missing piece. Some vendors already position early products, while working groups are still writing the underlying specs.

If you want to try the broker, point your coding agent at the [repository](https://github.com/zalando-incubator/agentic-identity-broker "Agentic Identity Broker source repository") and ask it how the broker would fit your setup, or run the [local stack](https://agenticidentitybroker.dev/docs/get-started "Get started with the Agentic Identity Broker") and walk through a delegation yourself. Please report vulnerabilities through the process on the [security page](https://agenticidentitybroker.dev/docs/resources/security "Security posture"). If you want to exchange ideas on approaches or features, open an issue or reach out to me directly.
