---
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

Magnus is my mentor and the mastermind behind the broker, and I've been his sidekick since we started at the end of 2025. We built the broker with coding agents from the first prototype in January 2026. Over those 10 months, I switched agent harnesses 6 times and worked with 9 models from Anthropic and OpenAI. What kept the project on track through all those changes was the spec work we did up front and the effort we put into verifying every change. Most of what I learned is about those 2 things.

## Why We Started With Agent Identity

Around the end of 2025, new Claude Sonnet and Opus models pushed the hype around agents through the roof. From a platform and security perspective, Magnus and I could see where that would lead. Without central capabilities that come with guardrails, every team would connect its agents to tools in its own way, and consolidating that wild west later would be very difficult. So we set out to solve the hard parts first: agent identity and access to tools.

The quickest way to connect an agent to a tool is a robot account, where the agent holds a long-lived credential for each Model Context Protocol (MCP) server or API it calls. That breaks down as soon as several people share the agent. The agent then acts with the combined permissions of all its users, nobody can tell whose request was whose, and anything that tricks the agent can reach for those credentials. I made the case for [delegation and consent infrastructure]({{< ref "/post/appsec-agentic-engineering/index.md" >}} "AppSec in the Age of Agentic Engineering") from the AppSec side already earlier this year.

The broker keeps both the user and the agent in every authorization decision. A user grants an agent access to a service with a chosen permission set and an optional expiry, and can revoke that grant at any time. The broker stores the provider tokens encrypted. On each tool call, a gateway such as agentgateway exchanges the agent's token for the matching provider token through [OAuth 2.0 Token Exchange (RFC 8693)](https://www.rfc-editor.org/rfc/rfc8693 "RFC 8693: OAuth 2.0 Token Exchange"), so the provider token never reaches the agent.

As far as we could tell, no product covered this when we started, and the big vendors were still working out which agentic engineering problems needed solving. The standards are still catching up today.

Magnus and I describe the platform around the broker and the reasoning behind its design in [the post that announced the release](https://engineering.zalando.com/posts/2026/09/agentic-platform-open-sourcing-agentic-identity-broker.html "Agentic Platform: Open-Sourcing the Agentic Identity Broker"), and our [talk slides](https://agenticidentitybroker.dev/docs/presentations/2026-09-18_agntcon-mcpcon-agentic-identity-broker.pdf "Economies of Scale for MCP and Agents") explain the delegation model. Alejandro Saucedo, who adopted the broker for his Kubernetes Agent Orchestration System (KAOS), covers the identity side in his series [Agentic Security & Identity](https://ethical.institute/blog/agentic-security-and-identity-part-1/ "Agentic Security & Identity, Part 1").

## We Used Spec Kit From the First Day

Magnus had already experimented with GitHub's [Spec Kit](https://github.com/github/spec-kit "Spec Kit source repository") before we started, and he did most of the heavy upfront work on our constitution. With Spec Kit, a team writes its binding principles into a constitution. For each feature, an agent then drafts a specification, a technical plan, and a task list before it writes any code. A newer command, [`/speckit.converge`](https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md "Spec Kit: Agentic spec-driven development"), checks the implementation against all 3 and appends tasks for the gaps it finds. We repeat implement and converge until converge reports no gaps.

The broker repository shows how much of this piled up in 10 months: 42 feature specs, 36 architecture decision records (ADRs), and a [constitution](https://github.com/zalando-incubator/agentic-identity-broker/blob/main/.specify/memory/constitution.md "Agentic Identity Broker constitution") with 13 principles, now at version 1.9.1. Among other things, the principles require that the broker fails closed and forbid custom cryptography. An `AGENTS.md` file at the root sends every agent to the constitution, the relevant ADRs, and more specific `AGENTS.md` files for each part of the code base.

All that setup cost time before the first feature existed, and it pays off every day now. Whether I start an agent on a feature or a new contributor does, the agent reads the same principles, decisions, and earlier specs. Being early adopters also meant we had our share of fun whenever we upgraded Spec Kit itself.

If another engineer asked me how to start a similar project, I'd tell them to own the spec work and hand the building and the reviewing to agents.

## Early Models Wrote Tests That Tested Nothing

For the first 4 months, I used Claude Code, mostly with Sonnet 4.5 and 4.6 and some Opus 4.6 on the side. In that time, we went from the first prototype in January 2026 to the first MCP server in production around March and the first users around April.

The early models failed mostly by inventing things I never asked for, claiming things that weren't true, and hallucinating. Their support for the languages, libraries, and tools we used was really bad. Tests were our biggest problem, and for code that holds other people's credentials, a passing test suite has to mean something. Green test suites with broken behavior were super common in early 2026. Agents implemented tests halfway or wrote assertions that didn't check anything. Magnus and I spent most of our time getting them to write proper tests, and it was hard.

The constitution records that fight. It requires red-green-refactor test-driven development (TDD), where every test fails before the implementation exists, and a 1:1 mapping from each spec to an end-to-end (E2E) test that covers a complete user flow. Its version history shows that we added the E2E principle later, extended it to browser tests for the frontend, and clarified the rules for the red phase twice.

Less common libraries caused the second big problem. The broker encrypts tokens before storing them with the Go releases of the AWS Encryption SDK and the AWS Cryptographic Material Providers Library, and Claude failed hard at wiring them together. So I wrote a dedicated [skill](https://github.com/zalando-incubator/agentic-identity-broker/tree/main/.agents/skills/aws-crypto-go "aws-crypto-go skill") that the agent loads when a task touches encryption. The skill explains how the pieces fit together, includes a reference and complete examples, and tells the agent never to answer from its training data alone. I still make the cryptography decisions myself.

Today the public repository contains about 101,000 lines of Go test code and about 46,000 lines of Go production code (counting non-blank, non-comment lines). We didn't plan that ratio. At one point we invested a lot in the verification framework, and I still think the broker needs more tests today. Right now my agents and I are working on the stability, performance, and structure of the test suites.

## Why I Switched Harnesses 6 Times

After 4 months with Claude Code, I moved to [Pi](https://pi.dev/ "Pi coding agent") and spent 2 months customizing it. Then I went back and forth between Pi and [oh-my-pi (OMP)](https://omp.sh/ "oh-my-pi"), an opinionated fork of Pi, for about a month. The full sequence was Claude Code, Pi, OMP, Pi, OMP, Pi, and finally OMP, which has been my only harness for the last 2 months.

Most switches came down to harness details. Early OMP felt more autonomous and proactive than Pi, which helped in some situations and got in the way in others. In Pi, I really liked the [pi-lens](https://github.com/apmantza/pi-lens "pi-lens source repository") extension's support for [Opengrep](https://github.com/opengrep/opengrep "Opengrep source repository"), an open-source static analysis engine. OMP is much better nowadays, although I still fight with its advisor, a second model that reads every turn of the main agent and adds notes. I regularly turn the advisor off and (a few days later) on again.

The models changed along the way, too. With Pi, I moved from Claude models to GPT-5.4, then GPT-5.5 and GPT-5.6 Terra. Since we published the broker, I've worked with GPT-6 Sol, GPT-6 Astra, and Claude Fable 5.1. The agents got better with each step. I talked about my setup in more detail on the [Beyond Vibe Coding podcast](https://bvc.fm/2026/08/13/010.html "When Coding Agents Ship at Machine Speed, AppSec Has to Move Into the Loop") in August.

If you're starting now, use a strong harness with good tool support, such as documentation lookup through [Context7](https://context7.com/ "Context7") or web search through [Exa](https://exa.ai/ "Exa"), and don't shy away from frontier models. I found them worth every penny for the broker.

## Review Takes More Agents Than Writing

Nowadays, some agents are always working on the broker. They harden security, improve the test suites and continuous integration (CI), prepare and implement specs for new features, and review changes. Each agent works in its own git worktree, so parallel agents don't overwrite each other's changes. I try to keep it to 2 or 3 agents at a time, but depending on the day and my meeting schedule, it can be 6 to 8. I start most of them myself, and CI starts some of the reviews.

Reviewing is the hard part. Early on, I expected [roborev](https://www.roborev.io/ "roborev"), a local daemon that reviews each commit in the background, to be a great addition to my harness, and I used it extensively. It regularly got lost in endless loops where it fixed and discussed the same or similar issues again and again. Over time it produced more noise and distraction than help. As the models got better and the harnesses got stronger, I left it behind and replaced it with really good custom review skills.

Today I regularly have more agents reviewing in parallel than writing code. The README promises that we review every pull request, and I still review the E2E tests and the specs myself.

## Agents Helped Prepare the Public Release

For the release on 15 September, I squashed the private history into a single public commit. Agents helped remove internal references, build the documentation site, and run security reviews, while I worked on the [OpenSSF Scorecard](https://github.com/ossf/scorecard "OpenSSF Scorecard"), designed the wordmark logo, and set up the domain's DNS.

In the first 10 days after the release (15 to 24 September), the repository received 93 pull requests, and we merged 58 of them. Dependabot opened 26 of those pull requests, and besides Magnus and me, Alejandro Saucedo and Farasath Ahamed opened the rest.

## What We Haven't Solved Yet

The broker solves cases where an agent acts on behalf of a human. Autonomous agents are harder: when no human is in the loop and machines or other agents call internal and external tools such as MCP servers, every approach I know of is still brittle. Large vendors and new kids on the block promise to have better solutions for these cases today, but I don't think they are complete yet. The broker's roadmap includes central tool approvals, activity logs and audit connectors as well as token exchange for agent-to-agent calls.

[AGNTCon](https://agntconmcpconeu26.sched.com/ "AGNTCon + MCPCon Europe 2026 schedule") left me with the impression that the whole industry is still working on the same questions: the talk by Christian Posta from Solo.io answered "What IS an Agent's Identity?". The Identity Assertion JWT Authorization Grant (ID-JAG) talk by Aaron Parecki from Okta, Paul Carleton from Anthropic, and Joey Orlando from Archestra.AI names SaaS provider adoption as the missing piece. Many actors seemingly try to position their early products and solutions, while others are still working hard on the underlying specs.

If you want to try the broker, point your coding agent at the [repository](https://github.com/zalando-incubator/agentic-identity-broker "Agentic Identity Broker source repository") and ask it how the broker would fit your setup, or run the [local stack](https://agenticidentitybroker.dev/docs/get-started "Get started with the Agentic Identity Broker") and walk through a delegation yourself. Please report vulnerabilities through the process on the [security page](https://agenticidentitybroker.dev/docs/resources/security "Security posture"). If you want to exchange ideas on approaches or features, open an issue or reach out to me directly.
