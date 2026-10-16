---
title: "AppSec in the Age of Agentic Engineering"
description: "Guest lecture for the cybersecurity course at HTW Berlin on how coding agents move AppSec toward harness design, platform constraints and measurable risk."
claim: "AppSec teams should shape the harness, platform and risk model that coding agents work inside, because finding problems after the code is written cannot keep up with agents."
date: 2026-07-03
tags: ["agentic-engineering", "sdlc", "platform-engineering"]
---
Guest lecture by Jan Brennenstuhl for the cybersecurity course at Hochschule für Technik und Wirtschaft Berlin (HTW), summer term 2026.

## Materials

- [Slides (PDF)](/new-appsec-operating-model/htw-berlin-agentic-appsec-slides.pdf)
- [Supporting essay: Guest Lecture at HTW Berlin: AppSec in the Age of Agentic Engineering]({{< ref "/post/htw-berlin-agentic-appsec" >}})

## Reading companion

Coding agents write a growing share of production code, so security feedback that arrives after the code exists cannot keep up. The lecture argues that AppSec teams get the most leverage from the harness the agent runs in: the rules, tools, sandboxes and credentials around the model, not the model itself. Three practices follow: deliver security findings while the task is still in the agent's context, run agent tasks in disposable sandboxes with short-lived task-scoped credentials, and measure risk per change instead of per release.

This is a short reading companion, not a transcript. The supporting essay is the condensed lecture with context and references in accessible HTML.
