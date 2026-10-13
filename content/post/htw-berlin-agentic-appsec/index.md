---
id: jb-htw-berlin-agentic-appsec
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['agentic-engineering', 'application-security']
imageDecorative: true
title: "Guest Lecture at HTW Berlin: AppSec in the Age of Agentic Engineering"
linkTitle: "HTW Berlin Guest Lecture"
description: "My HTW Berlin guest lecture explains why agentic engineering moves AppSec toward harness design, platform constraints, and measurable risk."
excerpt: "My HTW Berlin guest lecture explains why agentic engineering moves AppSec toward harness design, platform constraints, and measurable risk."
lead: "HTW Berlin invited me to speak to its cybersecurity course about the AppSec challenges that coding agents make impossible to ignore."
slug: new-appsec-operating-model
image: htw-guest-lecture.webp
date: 2026-07-03
lastmod: 2026-09-23
draft: false
weight: 50
categories: ["appsec"]
tags: ["agentic-engineering", "sdlc", "platform-engineering"]
featured: false
---

I recently gave a guest lecture to the cybersecurity course at Hochschule für Technik und Wirtschaft Berlin (HTW). The topic was application security (AppSec) in the age of agentic engineering, and how coding agents change the daily work of developers and AppSec teams.

My central argument: AppSec teams have to move from finding problems after code is written to shaping the systems that coding agents write code inside. Agentic engineering makes weak defaults, slow handoffs, and local exceptions more expensive, so the biggest wins now come from the harness, the platform, and the risk model.

The [full slide deck](htw-berlin-agentic-appsec-slides.pdf "Application Security in the Age of Agentic Engineering") contains the key points, examples, and references from the session. Below is a condensed version of the lecture with some additional context and links.

## Fixing Findings Is the New Bottleneck

The adoption numbers make this hard to dismiss. [Google's New SDLC whitepaper](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding "The New SDLC With Vibe Coding") estimates that as of early 2026, 85% of professional developers use AI coding agents regularly, 51% use them daily, and roughly 41% of new code is AI-generated. Addy Osmani, one of the authors, wrote a [readable summary](https://addyosmani.com/blog/new-sdlc-vibe-coding/ "The New Software Lifecycle") if you don't want to read the whole paper.

Coding agents don't write one function and wait for review. They write, test, read the failures, rewrite, and verify, often several times per hour. Security scanners can keep up with that loop. The old queue of triage, ticketing, and human remediation can't. At that speed, an AppSec team has plenty of findings and lacks a fast way to turn them into fixes.

The way to close that gap is to return security feedback while the agent still holds the task in its context, so it can repair the problem in the same session. I'd reserve tickets for 2 cases: the in-session loop failed, or new findings surface in artifacts that are already deployed.

Remediation also changes shape at fleet scale. Instead of hunting down individual findings, the AppSec team designs the fix for a whole vulnerability class, and agents apply it to every affected service. I describe this model in more detail in [AppSec in the Age of Agentic Engineering]({{< ref "/post/appsec-agentic-engineering/index.md" >}} "AppSec in the Age of Agentic Engineering").

## The Harness Is the Control Plane

The whitepaper offers a useful mental model: an agent is a model plus a harness. The harness is everything around the model: instructions and rule files, tools and Model Context Protocol (MCP) servers, guardrails, sandboxes, orchestration, and observability. The authors estimate the split at roughly 10% model and 90% harness. Osmani gives a public example in his summary: on Terminal Bench 2.0, 1 team moved a coding agent from outside the top 30 into the top 5 by changing only the harness and keeping the same model underneath.

The harness is also where an AppSec team has the most control. A stronger model helps, but it won't fix unsafe access defaults, missing tests, or an insecure tool configuration on its own. So I'd ship security skills, local scanning, and review feedback into the harness, where agents can check and improve their own work before a pull request exists.

## Shift Security Down into the Platform

Shift-left still catches mistakes early, but it doesn't remove the security decisions that every team and every agent has to make. At agent speed, each local workaround becomes a reusable pattern, and architectural drift compounds across the fleet.

That's why I argued for [shift-down security](https://github.com/kubernetes/sig-security/blob/main/sig-security-docs/papers/shift-down/shift-down-security.md "Kubernetes SIG Security: Shifting Down Security"). Instead of asking whether a team implemented authentication correctly, ask why the team needs to implement authentication at all. A mature platform makes that question unnecessary: it exposes APIs with authentication built in, gives workloads scoped identity, and offers a deployment path that is secure by default.

Hardened base images, service templates, platform-owned delivery pipelines, and workload identity remove whole categories of errors and make the secure path the easy path. In my experience, agents follow it. These constraints move undifferentiated choices into a maintained platform, and teams keep the engineering decisions that make their product different. [Shift Down: Why Agentic Engineering Demands Platform-Level Security]({{< ref "/post/appsec-shift-down/index.md" >}} "Shift Down: Why Agentic Engineering Demands Platform-Level Security") explains this platform role in more detail.

## Give Risk an Operational Budget

Agentic engineering also needs security decisions that work at machine speed. Blocking every finding doesn't scale, and neither does ignoring them. I suggested borrowing the [error-budget model](https://sre.google/sre-book/embracing-risk/ "Embracing Risk") from site reliability engineering (SRE) and applying it to security exposure.

A **risk budget** caps how long a high-risk, reachable vulnerability may stay in production. Reachability analysis turns raw findings into business exposure: a known vulnerability (CVE) in dead code doesn't consume the same budget as the same CVE behind a public API. The budget gives people and agents a clear decision rule: fix what burns the budget, defer what doesn't.

Security then becomes a shared operating concern with an accountable number attached. Instead of an impossible demand (fix every finding), the team decides on an exposure window and defends it.

## The Coding Agent Is an Attack Surface

The agent itself belongs in the threat model. Each task is an untrusted workload: it executes arbitrary code and reads dependency metadata, issue descriptions, pull-request comments, and documentation. That creates a large internal code-execution surface and exposes the agent to [prompt injection and excessive agency](https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for Large Language Model Applications").

A warning in a rule file won't protect against that. Run agent tasks in disposable cages, such as [nono](https://nono.sh/) OS-level sandboxes or [Firecracker microVMs](https://firecracker-microvm.github.io/ "Firecracker"), and issue short-lived, task-scoped credentials through an identity broker. Persistent roles and long-lived API keys don't belong in an agent context.

## What I Asked the Students to Learn

I closed the session with direct advice: learn software engineering deeply, and learn to think in platforms. Get comfortable with distributed systems, identity and access management (IAM), observability, infrastructure as code, and the economics of risk.

Agentic engineering makes AppSec more structural and more software-heavy. The next generation of AppSec engineers will still understand attacks and secure coding, but their biggest impact will come from building paved roads (maintained, secure defaults that teams use without asking), hardening harnesses, and designing systems where insecure choices are rare.
