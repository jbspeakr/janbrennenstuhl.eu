---
title: "AppSec in the Age of Agentic Engineering"
linkTitle: "AppSec in the Age of Agentic Engineering"
description: "Agentic engineering will reward AppSec teams that turn security from a post-commit gate into a pre-commit engineering capability, built hands-on with SRE and platform engineering."
excerpt: "Agentic engineering will reward AppSec teams that turn security from a post-commit gate into a pre-commit engineering capability, built hands-on with SRE and platform engineering."
lead: "Agentic engineering will reward AppSec teams with strong engineering foundations: those building tooling, automating remediation at scale, and treating risk quantitatively alongside SRE and platform peers."
slug: appsec-agentic-engineering
image: agentic-engineering-appsec.webp
date: 2026-05-14
lastmod: 2026-05-14
draft: false
featured: true
weight: 50
categories: ["appsec"]
tags: ["agentic-engineering", "sdlc"]
---

Agentic engineering is collapsing the Software Development Life-Cycle (SDLC) into fast, autonomous loops. AI-augmented engineers ship code at a volume our security tooling and processes were never built for. Bartosz Ocytko recently mapped [where agentic engineering is heading](https://ocytko.net/posts/quo-vadis-agentic-engineering/ "Quo Vadis, Agentic Engineering?"), pointing at bottlenecks in verification, open source, and compute. Reading his piece, one question stayed with me: what does this shift mean for Application Security?

Agentic shifts [will reward organizations with strong engineering foundations](https://www.linkedin.com/posts/bartoszocytko_agentic-engineering-relocates-engineering-share-7455367680225677313-04IU "Bartosz Ocytko via LinkedIn"): those that can verify, coordinate, and safely absorb machine-generated change. AppSec is part of that foundation. Teams that already build tooling, run large-scale remediation, and treat risk quantitatively are well placed to enable agentic engineering at scale. The threat side reinforces this: as top-tier models [lower the barrier for attackers](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access "Google: Adversaries Leverage AI for Vulnerability Exploitation, Augmented Operations, and Initial Access"), strong security engineering becomes more valuable, not less.

Three concrete shifts decide which AppSec teams will thrive:

- **From detection to mitigation.** Fix faster than we discover.
- **From policy authors to engineers.** Ship security tooling into the coding agent's context.
- **From gatekeepers to partners.** Join forces with SRE, platform, and cloud engineering teams to treat risk like reliability.

## The Mitigation Gap

Most mature organizations have solved detection. Scanners cover infrastructure, cloud platforms, application code, and CI/CD pipelines. [AI-powered vulnerability discovery](https://www.hackerone.com/blog/ai-vulnerability-discovery-remediation-gap) pushed detection even further. The visibility is there. The ability to fix what we find at scale is not.

A typical large engineering org sits on millions of findings, tens of thousands of open risk issues, and a handful of critical ones [that linger too long](https://www.edgescan.com/the-vulnerability-backlog-crisis-why-45-of-enterprise-vulnerabilities-never-get-fixed/ "The Vulnerability Backlog Crisis"). The bottleneck is not discovery anymore. It is remediation. Detection without mitigation only grows the backlog and extends exposure windows.

Agentic engineering widens this gap. Coding agents generate code at machine speed, so new findings appear faster too and the [verification debt](https://fazy.medium.com/agentic-coding-ais-adolescence-b0d13452f981 "Verification debt: the hidden cost of AI-generated code") grows. If remediation still depends on humans picking up tickets between feature work, the backlog wins. Risk only decreases when we fix faster than we discover.

The way out is also agentic. If review results feed back into the coding agent's evaluation loop, many findings never reach a ticket. The agent rewrites the code mid-task, before it is ever committed. Prevention inside the loop beats remediation after the fact.

The catch: our tools are not built for that loop. When a coding agent submits a PR in seconds, a security gate that takes minutes is the constraint. Binary gates do not work at this volume either. _"Block on medium severity"_ blocks everything. _"Ignore everything below critical"_ leaves real risks open.

We need to move from _"we found it, you fix it"_ to _"we prevent it, and we fix what slips through"_.

## From Detection to Mitigation

The traditional loop is built for human speed: Code → Scan → Ticket → Human Fix.

The agentic loop compresses to: Code → Scan → Feedback → Agent Rewrites → Verified. The agent acts on findings in the same context where the code was written. No ticket. No handoff. Designing, building, and maintaining tooling for that loop is the new AppSec day job.

Distribution changes too. Security scanning can no longer live only in version control platforms and CI pipelines. Every engineer needs SAST, DAST, and LLM-based reviewers available locally so their agents can run checks before opening a PR. AppSec owns the packaging, the configuration, and the policy. The job shifts from tuning the CI scanner to shipping the tooling that runs everywhere coding agents do.

## Shift-Left: AppSec as an Engineering Discipline

AppSec roles shift from vulnerability hunter to engineer who builds and ships security tooling and contributes remediation code directly. This is not about configuring scanners or writing policies that block deployments. It is about building the infrastructure that makes coding agents produce secure code by default.

### Campaigns, Not Tickets

Handling vulnerabilities one by one does not scale. Campaign-based remediation targets entire vulnerability classes at once: dependency upgrades, IaC misconfigurations, repeated insecure patterns across hundreds of services. Spotify's [fleetshift](https://engineering.atspotify.com/2023/05/fleet-management-at-spotify-part-3-fleet-wide-refactoring/) is a good mental model.

AppSec designs the campaign. [Coding agents open](https://github.blog/news-insights/product-news/secure-code-more-than-three-times-faster-with-copilot-autofix/ "GitHub Copilot Autofix"), test, and verify the remediation PRs across the fleet. Impact per engineer-hour goes up by an order of magnitude. We stop being a reporting function and start being an engineering multiplier.

### Security Tooling for Coding Agents

There are at least three categories of tooling that AppSec builds and maintains:

**Security skills and agent instructions.** General [agentic security skills](https://github.com/cosai-oasis/project-codeguard) cover cryptography, input validation, auth, and supply chain. [The format is standardised](https://agentskills.io/specification "Agent Skills Spec") and coding agents consume them before and during code generation. Organization-specific skill libraries go further: internal policies (_"use the central auth SDK, not raw JWT handling"_), approved libraries, deployment constraints. When a new vulnerability class appears, AppSec publishes a skill update and every agent in the org has it the same day.

**Local security scanning infrastructure.** SAST and DAST available via CLI or [MCP](https://modelcontextprotocol.io/), with centrally managed configuration and policies. The agent self-checks its output locally, before pushing. Engineering teams get scanning that works without setup.

**Security review agents.** Specialized agents that combine security skills with local tooling. They enforce org-specific policies and surface issues the coding agent can act on directly. Tools like [roborev](https://www.roborev.io/) point in this direction: a local daemon that runs automated agentic code reviews on a post-commit hook, delivering findings with file paths, line numbers, and severity before the code reaches CI.

The integration pattern is a shared **review ledger**: every signal source (static analyzer, dynamic scanner, LLM-based reviewer) writes to the same structured log, typically in [SARIF](https://sarifweb.azurewebsites.net/ "Static Analysis Results Interchange Format (SARIF)"). The coding agent reads the ledger after each iteration and knows which checks passed, which failed, and what to fix next.

### Securing the Coding Agent

Coding agents are productive when they can **execute** the code they write. They implement, run the tests, see the failure, and improve. Every agent task is therefore an untrusted workload running arbitrary code. This creates a large internal Remote Code Execution (RCE) surface that touches workstation setup and engineering practice.

**Sandboxing and prompt injection defense** are tightly coupled. A coding agent consumes external inputs: dependency metadata, issue descriptions, PR comments, documentation. Each one is a potential [prompt injection](https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for LLM Applications") vector. **Micro-VM isolation** with [Firecracker](https://firecracker-microvm.github.io/), [Sandvault](https://github.com/webcoyote/sandvault), or [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/get-started/ "Docker Sandboxes") gives each task a disposable environment. **Kernel-level sandboxing** with tools like [nono](https://nono.sh/os-sandbox) applies irrevocable filesystem allow-lists via Landlock (Linux) and Seatbelt (macOS), without daemons, containers, or runtime overhead. Containers offer [weaker isolation than their reputation suggests](https://nono.sh/os-sandbox#kernel-sandboxing-vs-the-alternatives). AppSec picks the right [isolation boundary](https://mrinal.com/articles/agent-sandboxes/ "Agent Sandboxes") per workload type and ships the sandbox setup as a paved-road default, together with platform teams.

**Identity brokerage and delegation.** Coding agents should never hold persistent IAM roles or long-lived API keys. An identity broker issues short-lived, task-scoped credentials on demand and revokes them when the task completes. Beyond internal credentials, coding agents increasingly act on behalf of users across third-party services. That needs proper [delegation and consent](https://oauth.net/2.1/) infrastructure with narrow, time-limited permissions the user can revoke at any moment. Without this, teams end up storing tokens in agent contexts or hard-coding service accounts. Both fail the moment an agent is compromised or a prompt misinterpreted. AppSec builds the broker together with the platform and IAM teams, and abstracts it away so coding agents transparently exchange tokens instead of reusing whatever credential is at hand.

### Threat Modeling and Offensive Testing

Traditional scanners catch known CVEs, common misconfigurations, and obvious injection points. They miss logic flaws: broken access control across multi-step workflows, business logic bypasses, race conditions in state. Catching design-level flaws means encoding domain knowledge into agents. Security expertise becomes infrastructure.

**Agentic threat modeling** turns a periodic exercise into a continuous practice. [AppSec builds agent setups](https://www.detectionatscale.com/p/threat-modeling-ai-agents-mcp "Building Threat Models with MCP and AI Agents") that review applications and repositories regularly, analyzing access control patterns, data flow boundaries, and trust assumptions. They run continuously and surface drift against the org's security posture.

**Continuous offensive simulation** complements this: agentic pentesting as a service. Not scanners running pattern matching but agents that understand the application's business logic and actively look for the flaws a human pentester would target: authorization boundaries, multi-step attack paths, [privilege escalation opportunities](https://labs.secengai.com/p/ai-assisted-web-pentesting-using-claude-code-burp-mcp "AI-assisted Web Pentesting Using Claude Code + Burp MCP"). Building them means turning years of offensive expertise into repeatable strategies.

## Converging with SRE and Platform Engineering: Risk as Reliability

{{< quote source="Building Secure and Reliable Systems" url="https://google.github.io/building-secure-and-reliable-systems/raw/toc.html" >}}
A system cannot be reliable if it is insecure, and it cannot be secure if it is operationally unreliable.
{{< /quote >}}

Engineering teams already manage [error budgets](https://sre.google/sre-book/embracing-risk/ "Google SRE Book: Embracing Risk") for availability, and security can join that model. A **risk budget** caps how long a high-risk, reachable vulnerability is allowed to exist in production before it burns error budget, just like downtime does. AppSec provides the framework and the tooling; the business owner sets the target like any other [SLO](https://sre.google/sre-book/service-level-objectives/ "Google SRE Book: Service Level Objectives").

This directly addresses a problem of the agentic SDLC: coding agents generate change faster than human triage can process it, so without quantitative targets every finding competes for attention equally and nothing gets prioritized. Risk budgets give a decision rule: fix what burns the budget, defer what does not.

The conversation shifts from _"fix all the bugs"_ to _"manage the exposure window"_. Security becomes a shared operational concern rather than a separate checklist.

Risk budgets only work if we can tell real exposure from noise. That requires **reachability analysis**: tracing the call graph from vulnerable code to entry points. A CVE in dead code does not burn budget. The same CVE behind a public API does. At the CI gate, this means blocking only changes that introduce *reachable* risk instead of failing on raw counts. In production, a monitoring layer tracks how long reachable findings stay open and burns error budget accordingly.

The convergence goes further than SRE. Platform and cloud engineering teams already ship the paved roads that engineering teams build on: base images, service templates, IaC modules, identity primitives, networking defaults. AppSec wins by shifting security *into* [those golden pathes](https://www.redhat.com/en/topics/platform-engineering/golden-paths "What is a Golden Path for software development?"), not by stacking parallel guardrails on top. Hardened base images, secure-by-default service templates, opinionated IaC modules, and central identity primitives carry security with them. The job is co-owned: platform engineering ships the road, AppSec ships the security defaults inside it.

On the policy side, make security policy machine-readable. The 50-page Security Policy PDF turns into agent instructions, a vector database, or [policy-as-code](https://www.openpolicyagent.org/) rules that coding agents check in real time. When policy is code, the agent verifies compliance mid-task without a human gate. AppSec shifts from reviewing individual changes to maintaining the policies and risk models that agents enforce continuously.

## From Gate to Force Multiplier

The shift from traditional to agentic AppSec touches every part of how we think about security in the SDLC:

| Dimension | Where we've been | Where we're heading |
|---|---|---|
| **Focus** | Detection and reporting | Mitigation and prevention |
| **Verification** | Periodic, gate-based | Continuous, real-time |
| **Remediation** | Human-led via tickets | Coding-agent-led auto-fix loops |
| **Trust Model** | Developer-centric | Zero-trust, actor-centric |
| **Scanners** | Deterministic rules | Probabilistic, context-aware |
| **Scale** | One issue at a time | Campaign-based, fleet-wide |
| **Velocity** | Slowed down by triage | Accelerated by auto-verification |

For years, we carried structural problems that were unsolvable at human scale: too many findings, too few engineers, a feedback loop that was too slow. Agentic engineering does not just create new challenges. It hands us the tools to finally solve the old ones. Auto-remediation loops have the potential to close the gap between finding and fixing. Contextual risk assessment filters the noise. Machine-readable policies spread security expertise beyond the security team. Campaign-based remediation clears backlogs that have grown for years.

The industry bottleneck is shifting from code generation to verification and mitigation. Agentic shifts will reward AppSec teams with strong engineering foundations: teams that move from detection to mitigation, turn security into a hands-on engineering discipline, and partner with SRE, platform, and cloud engineering to treat risk like reliability. These teams will not just keep pace. They will become the force multipliers that make agentic engineering safe enough to trust at scale.
