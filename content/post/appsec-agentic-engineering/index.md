---
id: jb-appsec-agentic-engineering
imageDecorative: true
title: "AppSec in the Age of Agentic Engineering"
linkTitle: "AppSec in the Age of Agentic Engineering"
description: "How AppSec teams can keep up with coding agents: fix findings inside the agent loop, ship security tooling to agents, and manage risk with SRE and platform teams."
claim: "AppSec teams keep up with coding agents by fixing findings inside the agent loop, shipping security tooling to agents, and managing risk budgets together with SRE and platform teams."
lead: "Coding agents write code faster than security teams can triage the findings. AppSec teams that build tooling, automate remediation at scale, and measure risk together with SRE and platform teams are in the best position to keep up."
slug: appsec-agentic-engineering
image: agentic-engineering-appsec.webp
imageCredit:
  name: "A R C"
  url: "https://unsplash.com/de/fotos/ein-rot-schwarzes-foto-einer-person-die-einen-regenschirm-halt-YSqnP5GcW2I"
date: 2026-05-14
lastmod: 2026-09-24
draft: false
featured: true
weight: 50
tags: ["agentic-engineering", "sdlc"]
series: agentic-appsec
findings:
  - id: appsec-agentic-backlog
    text: "In Edgescan's 2025 report, enterprises with more than 1,000 employees still had 45.4% of the vulnerabilities discovered within 12 months open, and the high and critical findings most likely to be exploited took 115.7 days on average to fix."
  - id: appsec-agentic-risk-budget
    text: "A risk budget sets how long a high-risk, reachable vulnerability may stay open in production before it burns the service's error budget, and reachability analysis keeps a CVE in dead code from counting."
  - id: appsec-agentic-sandbox-first
    text: "The first step is to sandbox the coding agents engineers already run and replace their long-lived credentials with short-lived, task-scoped ones, because the exposure exists as soon as an agent runs on an engineer's machine."
---

In agentic engineering, engineers hand tasks to coding agents that write code, run it, and fix their own mistakes in fast loops. Bartosz Ocytko recently mapped [where agentic engineering is heading](https://ocytko.net/posts/quo-vadis-agentic-engineering/ "Quo Vadis, Agentic Engineering?"), from a surge of commits on GitHub to bottlenecks in verification, open source, and compute. Most security tooling and processes weren't built for that volume of change. While reading his piece, I kept coming back to 1 question: what does this shift mean for application security (AppSec)?

Ocytko argues that agentic engineering [will reward organizations with strong engineering foundations](https://www.linkedin.com/posts/bartoszocytko_agentic-engineering-relocates-engineering-share-7455367680225677313-04IU "Bartosz Ocytko via LinkedIn"): those that can verify, coordinate, and safely absorb machine-generated change. I think AppSec is part of that foundation. AppSec teams that already build tooling, run large-scale remediation, and treat risk quantitatively are well placed to make agentic engineering safe at scale. Attackers raise the stakes for strong security engineering, too: [Google's Threat Intelligence Group reports](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access "Adversaries Leverage AI for Vulnerability Exploitation, Augmented Operations, and Initial Access") that AI models lower the barrier for adversaries to develop exploits. In May 2026, the group reported the first threat actor it believes used a zero-day exploit developed with AI.

The same agents that create the volume can also help with problems that AppSec teams couldn't solve at human scale: too many findings, too few security engineers, and feedback that arrived long after the code was written. I see 3 shifts that decide which AppSec teams keep up:

- From detection to mitigation: prevent findings inside the agent's loop and fix the backlog at fleet scale.
- From writing policies to building tools: ship security tooling into the context that coding agents work in.
- From gatekeeping to partnership: manage security risk together with site reliability engineering (SRE), platform, and cloud engineering teams, the way they already manage reliability.

## Findings Pile Up Faster Than Teams Fix Them

Most mature organizations already have good visibility into known vulnerability classes. Their scanners cover infrastructure, cloud platforms, application code, and continuous integration and delivery (CI/CD) pipelines. AI adds even more findings: HackerOne argues that [AI-powered vulnerability discovery has improved by an order of magnitude](https://www.hackerone.com/blog/ai-vulnerability-discovery-remediation-gap "Finding Fast, Fixing Slow: The Crisis of Asymmetric Remediation"), while remediation hasn't kept up.

Backlog data shows how far remediation lags behind. Edgescan, a vulnerability management vendor, analyzed its 2024 scanning and penetration testing results in its [Vulnerability Statistics Report 2025](https://info.edgescan.com/hubfs/23DOWNLOADABLE%20CONTENT/Vulnerability%20Statistics%20Reports/Edgescan_VulnerabilityStatsReport_2025.pdf "Edgescan Vulnerability Statistics Report 2025"). At enterprises with more than 1,000 employees, 45.4% of the vulnerabilities discovered within 12 months were still open. High and critical findings with the highest predicted exploit probability (an Exploit Prediction Scoring System score above 0.7) took 115.7 days on average to fix, slightly longer than the 109.4 days for those least likely to be exploited. Every finding that nobody fixes grows the backlog and extends the exposure window, the time during which an attacker can exploit the vulnerability in production.

Coding agents make this worse. They generate code at machine speed, so new findings appear faster. Lars Janssen calls the growing gap between how fast teams generate code and how fast they can check it [verification debt](https://fazy.medium.com/agentic-coding-ais-adolescence-b0d13452f981 "Verification debt: the hidden cost of AI-generated code"). If remediation still depends on engineers picking up tickets between feature work, the backlog keeps growing. Risk only goes down when teams fix findings faster than scanners discover new ones.

That requires AppSec teams to move from _"we found it, you fix it"_ to _"we prevent it, and we fix what slips through"_.

## Move Security Feedback Into the Agent Loop

In the traditional loop, a scanner reports an issue in the pipeline, someone files a ticket, and an engineer fixes it when there's time. In the agentic loop, the scan results go straight back to the coding agent, which rewrites the code in the same session until the checks pass. Many findings never reach a ticket because the agent fixes them before anyone commits the code. GitHub's [Copilot Autofix](https://github.blog/news-insights/product-news/secure-code-more-than-three-times-faster-with-copilot-autofix/ "Secure code more than three times faster with Copilot Autofix") suggests fixes directly in the pull request, which comes close to this loop. During its 2024 public beta, developers fixed new code scanning alerts in pull requests in a median of 28 minutes, compared with 1.5 hours without Autofix.

Today's security gates weren't built for this loop. When a coding agent opens a pull request (PR) in seconds, a security gate that takes minutes becomes the slowest step. Binary gates also break down at this volume: _"block on medium severity"_ blocks everything, and _"ignore everything below critical"_ leaves real risks open. The risk budgets I describe further down give teams a better decision rule.

Some findings will still slip through, and most organizations already carry a large backlog. Fixing them 1 ticket at a time doesn't scale. In campaign-based remediation, AppSec targets a whole vulnerability class at once, such as an outdated dependency, an infrastructure as code (IaC) misconfiguration, or an insecure pattern repeated across hundreds of services.

Spotify's [fleetshift](https://engineering.atspotify.com/2023/05/fleet-management-at-spotify-part-3-fleet-wide-refactoring/ "Fleet Management at Spotify (Part 3): Fleet-wide Refactoring") is a good mental model: it makes fleet-wide code changes by running a Docker image against each repository. Spotify reports that fleetshift created more than 270,000 PRs in 2022 and merged 77% of them automatically, and that it patched 80% of its production backend services within 9 hours of the Log4j disclosure.

With coding agents, the AppSec team designs the campaign, and agents open, test, and verify the remediation PRs across the fleet. GitHub already supports part of this: in [security campaigns](https://docs.github.com/en/code-security/securing-your-organization/fixing-security-alerts-at-scale/about-security-campaigns "About security campaigns"), teams can assign alerts to the Copilot cloud agent, which opens pull requests with fixes.

## Build and Ship Security Tooling

In this model, AppSec engineers build and ship security tooling and contribute remediation code directly. Their goal is infrastructure that makes coding agents produce secure code by default.

### Security Skills and Machine-Readable Policy

Skills are packaged instructions that coding agents load when a task needs them, and they follow an [open specification](https://agentskills.io/specification "Agent Skills Specification"). [Project CodeGuard](https://github.com/cosai-oasis/project-codeguard) from the Coalition for Secure AI (CoSAI) publishes general security skills for cryptography, input validation, authentication and authorization, and supply chain security. Organization-specific skills go further and encode internal policies (_"use the central auth SDK, not raw JWT handling"_), approved libraries, and deployment constraints. If the organization distributes skills centrally, AppSec can publish a skill update when a new vulnerability class appears, and every agent in the organization has it the same day.

The security policy itself needs the same treatment, because a coding agent can't do much with a 50-page PDF. AppSec teams can turn it into agent instructions, a searchable vector database, or [policy-as-code](https://www.openpolicyagent.org/) rules that agents check while they work. The agent then verifies compliance mid-task without waiting for a human reviewer, and AppSec's work moves from reviewing individual changes to maintaining the policies and risk models that agents enforce.

### Local Scanners and Review Agents

Security scanning can't live only in version control platforms and CI pipelines anymore. Coding agents need static application security testing (SAST), dynamic application security testing (DAST), and reviewers based on large language models (LLMs) on the engineer's machine, so they can check their own output before they push. AppSec teams package these tools as command-line interfaces (CLIs) or [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers and manage their configuration and policies centrally. MCP gives agents a standard way to call tools. Engineering teams then get scanning that works without setup.

Dedicated review agents combine security skills with local tooling. They check code against organization-specific policies and report issues in a form the coding agent can act on directly. [roborev](https://www.roborev.io/) points in this direction: it's a local daemon that reviews each commit in the background through a git hook and [reports every finding](https://www.roborev.io/docs/guides/reviewing-code/ "roborev: Reviewing code") with a severity and a file and line location before the code reaches a PR.

A shared review ledger ties these checks together. Every source, whether static analyzer, dynamic scanner, or LLM-based reviewer, writes to the same structured log, typically in the [Static Analysis Results Interchange Format (SARIF)](https://sarifweb.azurewebsites.net/). The coding agent reads the ledger after each iteration and knows which checks passed, which failed, and what to fix next. LLM-based reviewers can catch context-dependent issues that rule-based scanners miss, but they don't return the same result on every run, so the ledger needs both.

### Sandboxes and Short-Lived Credentials

Coding agents are most useful when they can run the code they write: they implement a change, run the tests, read the failure, and try again. That makes every agent task an untrusted workload running arbitrary code, often on an engineer's laptop. For AppSec, this adds up to a large internal remote code execution (RCE) surface, and securing it touches workstation setup as well as engineering practice.

Sandboxing and prompt injection defense go together. A coding agent reads external input such as dependency metadata, issue descriptions, PR comments, and documentation, and each of these can carry a [prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/ "OWASP LLM01:2025 Prompt Injection") that tells the agent to do something else. A sandbox limits the damage when that happens, and the common options differ in isolation strength and cost:

- Lightweight virtual machines (micro-VMs) such as [Firecracker](https://firecracker-microvm.github.io/) and [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/get-started/ "Docker Sandboxes") give each task a disposable environment with its own kernel.
- OS-level sandboxes are lighter. [nono](https://nono.sh/os-sandbox) applies irrevocable, kernel-enforced filesystem allow-lists through Landlock on Linux and Seatbelt on macOS, and [Sandvault](https://github.com/webcoyote/sandvault) runs agents as a separate macOS user inside `sandbox-exec`. The nono authors point out that OS-level sandboxing doesn't give the memory isolation of a virtual machine.
- Containers share the host kernel, so [escaping 1 container puts the attacker on the host](https://mrinal.com/articles/agent-sandboxes/ "Agent Sandboxes: how to create millions of them").

AppSec picks the isolation boundary that fits each workload's trust level and, together with platform teams, ships the sandbox setup as the default configuration engineers get out of the box.

Credentials need the same care. Coding agents should never hold persistent identity and access management (IAM) roles or long-lived API keys. An identity broker issues short-lived, task-scoped credentials on demand and revokes them when the task completes. AppSec can build the broker together with platform and IAM teams and hide it behind the agent's tooling, so agents exchange tokens automatically and never fall back on whatever credential is at hand.

Beyond internal credentials, agents increasingly act on behalf of users in third-party services. That needs [delegation and consent](https://oauth.net/2.1/) infrastructure with narrow, time-limited permissions the user can revoke at any moment. Without it, teams end up storing tokens in agent contexts or hard-coding service accounts, and both fail as soon as an attacker compromises an agent or the agent misreads a prompt.

### Threat Modeling and Offensive Testing

Traditional scanners catch known vulnerabilities listed as Common Vulnerabilities and Exposures (CVEs), common misconfigurations, and obvious injection points. They miss logic flaws such as broken access control across multi-step workflows, business logic bypasses, and race conditions. To catch design-level flaws, AppSec teams have to encode their domain knowledge into agents.

Threat modeling, where a team maps how an attacker could abuse a system's design, usually happens in periodic workshops. Jack Naglieri [built threat models with AI agents and MCP](https://www.detectionatscale.com/p/threat-modeling-ai-agents-mcp "Building Threat Models with MCP and AI Agents") and argues that agents remove the weeks of meetings and documentation review that kept threat modeling a once-a-year exercise. Naglieri's example comes from detection engineering, but the approach carries over to applications. AppSec teams can build agent setups that regularly review applications and repositories, analyze access control patterns, data flow boundaries, and trust assumptions, and report drift from the organization's security posture.

Agentic penetration testing (pentesting) complements this, and AppSec can offer it to engineering teams as an internal service. These agents explore the application's business logic and look for the flaws a human pentester would target: authorization boundaries, multi-step attack paths, and privilege escalation. To build them, AppSec teams turn their offensive expertise into repeatable attack strategies. Public setups today still keep a human in the loop. In [AI-assisted web pentesting with Claude Code and Burp MCP](https://labs.secengai.com/p/ai-assisted-web-pentesting-using-claude-code-burp-mcp "AI-assisted Web Pentesting Using Claude Code + Burp MCP"), for example, the agent suggests the next test and the pentester decides whether to run it.

## Partner With SRE and Platform Teams

{{< quote source="Building Secure and Reliable Systems" url="https://google.github.io/building-secure-and-reliable-systems/raw/pr01.html" >}}
Can a system ever truly be considered reliable if it isn't fundamentally secure? Or can it be considered secure if it's unreliable?
{{< /quote >}}

In SRE, the product owner sets a [service level objective (SLO)](https://sre.google/sre-book/service-level-objectives/ "Google SRE Book: Service Level Objectives") such as 99.9% availability, and the remaining 0.1% becomes the service's [error budget](https://sre.google/sre-book/embracing-risk/ "Google SRE Book: Embracing Risk"), which the team can spend on outages and risky releases. AppSec can join that model with a **risk budget**. The risk budget sets how long a high-risk, reachable vulnerability may stay open in production before it burns error budget, just like downtime does. AppSec provides the framework and the tooling, and the product owner sets the target, just as for the SLO.

A risk budget helps with a problem that agentic engineering makes worse. Coding agents generate change faster than people can triage the findings, and without a quantitative target every finding competes for the same attention. With a risk budget, teams fix what burns the budget and defer what doesn't. The conversation moves from _"fix all the bugs"_ to _"manage the exposure window"_, and security becomes an operational concern that AppSec shares with the teams running the service.

Teams can only use a risk budget if they can tell real exposure from noise, and that requires **reachability analysis**: tracing the call graph from the vulnerable code to the application's entry points. A CVE in dead code doesn't burn budget, but the same CVE behind a public API does. At the CI gate, teams then block only changes that introduce _reachable_ risk and stop failing builds on raw finding counts. In production, a monitoring layer tracks how long reachable findings stay open and burns error budget accordingly.

Platform and cloud engineering teams already ship the paved roads that engineering teams build on: base images, service templates, IaC modules, identity primitives, and networking defaults. AppSec teams get the most reach by building security into those [golden paths](https://www.redhat.com/en/topics/platform-engineering/golden-paths "What is a Golden Path for software development?"). A hardened base image or a secure-by-default service template then carries security to every service that uses it, including the code that agents write. Platform engineering owns the templates and modules, and AppSec owns the security defaults inside them. I cover this model in more detail in [Shift Down]({{< ref "/post/appsec-shift-down/index.md" >}} "Shift Down: Why Agentic Engineering Demands Platform-Level Security").

## Where to Start

None of this has to happen at once. A team that wants to start can work through these steps in order:

1. Sandbox the coding agents that engineers already run, and replace their long-lived credentials with short-lived, task-scoped ones.
2. Package the existing scanners as CLIs or MCP servers with central configuration, and make them write SARIF.
3. Publish an organization-specific security skill that encodes the internal policies that matter most.
4. Pick 1 vulnerability class from the backlog and fix it across the fleet as a campaign.
5. Agree on a risk budget for reachable vulnerabilities with 1 service owner and their SRE team.

The sandbox comes first because the exposure exists as soon as an engineer runs an agent with access to their machine.
