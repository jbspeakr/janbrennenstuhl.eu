---
title: "Guest Lecture at HTW Berlin: AppSec in the Age of Agentic Engineering"
linkTitle: "HTW Berlin Guest Lecture"
description: "My HTW Berlin guest lecture explains why agentic engineering moves AppSec toward harness design, platform constraints, and measurable risk."
excerpt: "My HTW Berlin guest lecture explains why agentic engineering moves AppSec toward harness design, platform constraints, and measurable risk."
lead: "HTW Berlin invited me to speak to its cybersecurity course about the AppSec challenges that coding agents make impossible to ignore."
slug: new-appsec-operating-model
image: htw-guest-lecture.webp
date: 2026-07-03
lastmod: 2026-09-01
draft: false
weight: 50
categories: ["appsec"]
tags: ["agentic-engineering", "sdlc", "platform-engineering"]
featured: false
---

I recently gave a guest lecture to the cybersecurity course at Hochschule für Technik und Wirtschaft Berlin (HTW). The topic was **Application Security in the Age of Agentic Engineering**: a shift that changes the work of developers and AppSec teams.

My central argument is simple: **AppSec must move from finding problems after code is written to shaping the systems that coding agents write code inside.** Agentic engineering makes weak defaults, slow handoffs, and local exceptions more expensive, so the leverage now sits in the harness, the platform, and the risk model.

The [full slide deck](htw-berlin-agentic-appsec-slides.pdf "Application Security in the Age of Agentic Engineering") contains the key points, examples, and references from the session. The following is a condensed version of the lecture, with some additional context and links.

## The Gap Is Between Findings and Fixes

The problem that makes a new operating model for AppSec necessary is clear: [Early 2026 data show that 85% of professional developers use AI coding agents regularly, and 51% use them daily](https://addyosmani.com/blog/new-sdlc-vibe-coding/ "The New Software Lifecycle"). The same source estimates that AI generates roughly 41% of new code.

Our coding agents do not write one function and wait for review. They write, test, read failures, rewrite, and verify. Regular security scanning can keep up with that loop, but old-school queues for triage, ticketing, and human remediation cannot. Detection is no longer the main bottleneck. Mitigation is.

AppSec needs to return security feedback while the agent is still in the session context. A ticket matters only once that loop has failed or when new findings surface in already deployed artifacts. 

At fleet scale, remediation also changes shape: instead of hunting down individual findings, AppSec designs the fix for an entire vulnerability class, and agents apply it to every affected service. I explore this remediation model in more detail in [AppSec in the Age of Agentic Engineering]({{< ref "/post/appsec-agentic-engineering/index.md" >}} "AppSec in the Age of Agentic Engineering").

## The Harness Is the Control Plane

A useful mental model comes from [Google's New SDLC whitepaper](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding "The New SDLC With Vibe Coding"): an agent is a model plus a harness. Everything around the model is the harness: instructions and rule files, tools and MCP servers, guardrails, sandboxes, orchestration, and observability. The paper estimates the split at roughly 10% model and 90% harness. Public benchmark results point the same way: on Terminal Bench 2.0, one team moved a coding agent from outside the top 30 into the top 5 by changing only the harness, keeping the same model underneath.

That is where AppSec has the most control. A stronger model helps, but it does not fix unsafe access defaults, missing tests, or insecure tool configuration on its own. AppSec teams should ship security skills, local scanning, and review feedback into the harness so that agents can check and improve their work before a pull request even exists.

The lesson is not to trust agent output less. It is to design the system that produces that output with more care.

## Shift Security Down into the Platform

Shift-left remains useful because it catches mistakes early, but it does not remove the security decisions that every team and every agent still has to make. At agent speed, each local workaround becomes a reusable pattern, and architectural drift compounds across the fleet.

This is the case for [shift-down security](https://github.com/kubernetes/sig-security/blob/main/sig-security-docs/papers/shift-down/shift-down-security.md "Kubernetes SIG Security: Shifting Down Security"). Instead of asking whether a team implemented authentication correctly, ask why the team needs to implement authentication at all. A mature platform makes that question unnecessary. It exposes APIs with authentication built in, gives workloads scoped identity, and offers a deployment path that is secure by default.

Hardened base images, service templates, platform-owned delivery pipelines, and workload identity remove whole categories of errors and make the secure path the easy path. In my experience, agents follow it. Constraints do not remove valuable engineering freedom. They move undifferentiated choices into a maintained platform. [Shift Down: Why Agentic Engineering Demands Platform-Level Security]({{< ref "/post/appsec-shift-down/index.md" >}} "Shift Down: Why Agentic Engineering Demands Platform-Level Security") explains this platform role in more detail.

## Give Risk an Operational Budget

Agentic engineering also needs security decisions that can operate at machine speed. Neither blocking everything nor ignoring everything scales. I suggested borrowing the [error-budget model from SRE](https://sre.google/sre-book/embracing-risk/ "Embracing Risk") and applying it to security exposure:

A **risk budget** caps how long a high-risk, reachable vulnerability may remain in production. Because a CVE in dead code does not consume the same budget as the same CVE behind a public API, reachability analysis turns raw findings into business exposure. The budget gives people and agents a clear decision rule: fix what burns it, defer what does not.

This makes security a shared operating concern. It also changes the conversation: an impossible demand (fix every finding) becomes an accountable decision about the exposure window.

## The Coding Agent Is an Attack Surface

The agent itself belongs in the threat model. Each task is an untrusted workload: it executes arbitrary code and consumes dependency metadata, issue descriptions, pull-request comments, and documentation. That creates a large internal code-execution surface and exposes the agent to [prompt injection and excessive agency](https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for Large Language Model Applications").

The answer is engineering, not another warning. Run agent tasks in disposable cages, such as [nono OS-level sandboxes](https://nono.sh/) or [Firecracker microVMs](https://firecracker-microvm.github.io/ "Firecracker"), and issue short-lived, task-scoped access through an identity broker. Persistent roles and long-lived API keys do not belong in an agent context.

## The Work Ahead

I closed the session at HTW with direct advice for the students: Learn software engineering deeply. Learn to think in platforms. Get comfortable with distributed systems, identity and access management (IAM), observability, infrastructure as code, and the economics of risk.

Agentic engineering does not make AppSec less important. It makes the field more structural and more software-heavy. The next AppSec engineers will still understand attacks and secure coding. Their greatest leverage, though, will come from building paved roads (maintained, secure defaults that teams use without asking), hardening harnesses, and designing systems where insecure choices are rare. Security expertise becomes software.
