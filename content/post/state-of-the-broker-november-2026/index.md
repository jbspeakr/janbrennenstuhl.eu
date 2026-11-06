---
title: "State of the Broker: November 2026"
description: "[PLACEHOLDER: one plain sentence on November in the Agentic Identity Broker, written once the month is over.]"
claim: ""         # optional: the one quotable sentence that states the main point
lead: "[PLACEHOLDER: two sentences on what November was about.]"
date: 2026-12-01
slug: state-of-the-broker-november-2026
tags: ["agentic-engineering", "oauth2", "open-source"]
series: "state-of-the-broker"
# findings:       # up to three; IDs are permanent and unique site-wide (sotb-2026-11-...)
#   - id: ""
#     text: ""
draft: true
---

[PLACEHOLDER: opening paragraph on what November was about. Notes collected until 6 November follow in each section; replace them with prose at the end of the month.]

## [PLACEHOLDER: focus area heading]

Notes from 1 to 6 November:

- The first feature that our Spec Kit workflow on GitHub implemented end to end landed on 4 November: agents can now be the subject of an impersonation ([#293](https://github.com/zalando-incubator/agentic-identity-broker/pull/293), spec in issue [#222](https://github.com/zalando-incubator/agentic-identity-broker/issues/222)).
- I made the token endpoint adhere strictly to the RFC ([#276](https://github.com/zalando-incubator/agentic-identity-broker/pull/276)) and changed the broker to record an observed refresh-token rejection instead of a predicted expiry ([#378](https://github.com/zalando-incubator/agentic-identity-broker/pull/378)).
- We reworked logging: principals now go through a single policy handler, secrets are redacted in log output, and CodeQL blocks log output outside `slog` ([#363](https://github.com/zalando-incubator/agentic-identity-broker/pull/363), [#373](https://github.com/zalando-incubator/agentic-identity-broker/pull/373), [#411](https://github.com/zalando-incubator/agentic-identity-broker/pull/411)).
- We added coding standards for structured logging and OpenTelemetry and made them binding in the architecture review ([#338](https://github.com/zalando-incubator/agentic-identity-broker/pull/338), [#355](https://github.com/zalando-incubator/agentic-identity-broker/pull/355), [#426](https://github.com/zalando-incubator/agentic-identity-broker/pull/426)).
- We documented agentgateway's native `oauthTokenExchange` policy against the broker ([#275](https://github.com/zalando-incubator/agentic-identity-broker/pull/275)).

## [PLACEHOLDER: obstacles heading]

Notes from 1 to 6 November:

- Spec Kit automation kept needing fixes: CI and container test repair after implementation, App permissions, the sandbox for security scanners ([#370](https://github.com/zalando-incubator/agentic-identity-broker/pull/370), [#375](https://github.com/zalando-incubator/agentic-identity-broker/pull/375), [#391](https://github.com/zalando-incubator/agentic-identity-broker/pull/391), [#423](https://github.com/zalando-incubator/agentic-identity-broker/pull/423)).
- [PLACEHOLDER: anything else that got in the way.]

## Thank you, new contributors

[PLACEHOLDER: first-time contributors in November. None as of 6 November.]

## The month in numbers

| Measure | November 2026 |
| --- | --- |
| Commits on `main` | [PLACEHOLDER] (64 until 6 November, of which 5 from Dependabot) |
| Pull requests opened / merged | [PLACEHOLDER] |
| Issues opened / closed | [PLACEHOLDER] |
| Releases | [PLACEHOLDER: from `v0.1.129` to ...] (`v0.1.141` on 6 November) |
| People with commits | [PLACEHOLDER] |
| Stars | [PLACEHOLDER: count on 30 November, from 34 on 30 October] |
| Forks | [PLACEHOLDER] |

## Who wrote about the broker

I posted the broker as a [Show HN](https://news.ycombinator.com/item?id=50393235 "Show HN: Agentic Identity Broker, OAuth Delegation for AI Agents") on 6 November. By the evening it had 18 points and 3 comments, with questions about why OAuth delegation alone isn't enough and how the broker handles transitive delegation. [PLACEHOLDER: final points and comments, and whether we answered the questions.]

[PLACEHOLDER: other articles, talks and social media in November.]

## What we look at next

[PLACEHOLDER: open issues and trends; confirm each before naming it.]
