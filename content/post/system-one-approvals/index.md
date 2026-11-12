---
title: "System One for Tool Approvals: Show People Only the Critical Calls"
linkTitle: "System One for Tool Approvals"
description: "People approve agent tool calls by reflex. I explore how a System One model could answer narrow, typed questions about a call's arguments, so that a policy auto-approves the harmless calls and a person gets far fewer approval requests, only for the critical ones."
claim: "People get fewer approval requests, and less approval fatigue, when a System One model answers bounded questions about a tool call's arguments and a policy auto-approves the calls that those answers show to be harmless."
date: 2026-11-10
slug: system-one-approvals
tags: ["agentic-engineering", "defensive-security", "ux-security"]
findings:
  - id: approval-prompts-reflex
    text: "Anthropic reports that Claude Code users approve 97% of permission prompts, and that in a controlled study with 1,053 paid testers, human review caught 13.6% of the dangerous commands that were swapped into a prompt."
  - id: system-one-questions-not-decisions
    text: "In my proposal for the Agentic Identity Broker, a System One model answers bounded questions about the arguments of a tool call, such as whether the call gives access or data to a party outside the organisation. A policy that an operator configures auto-approves the calls whose answers are harmless, so a person is only asked about the rest."
  - id: system-one-fails-to-person
    text: "An unavailable model, a malformed answer or an uncertain answer must never auto-approve a tool call and never override a policy denial. In each of these cases the request stays a pending approval for a person."
draft: true
---

Asking a person before an agent runs a tool is the control that people expect in an agent loop. Many coding agents often ask before they e.g. run a shell command, and the [Agentic Identity Broker]({{< ref "/projects/agentic-identity-broker" >}}) (AIB) that I co-maintain can hold a tool call until a person approves based on a short description of the tool call. As much as it is commodity, it is also a very controversial feature. Public numbers and my own experience observing myself, fiends, family and colleagues suggest that people approve nearly everything they are shown. An approval prompt that is answered by reflex protects little, but still interrupts the agent's session flow.

It seems fair to assume that most approval prompts should never reach a human, and the few that do should be the most critical ones and carry sufficient information to make a truly informed decision. Fewer requests mean less noise, and with that hopefully less approval fatigue. Pretty much riding the Jev-Model wave, I proposed (a smarter tool approval approach)(https://github.com/zalando-incubator/agentic-identity-broker/issues/206 "AIB issue #206: Pluggable interface for an external decision model") to AIB: a fast "System One" model could read the actual arguments of a tool call and answers a few narrow questions about them. These answers could then feed into a predefined operator policy which could then auto-approve harmless calls, and only exceptionally prompt the human user for approval. The idea is similar to the auto mode in Claude Code, where a safety check in the background replaces most permission prompts. None of this is built yet, and before I start I'd like to explore where the design and its UX breaks.

## People Approve Most Tool Calls Without Reading Them

The best public numbers on reflex approvals I know of come from Anthropic. When the company [made auto mode the default in Claude Code](https://claude.com/resources/articles/auto-mode-default-in-claude-code "Auto mode is now the default in Claude Code for Pro, Max, Ultra, and Team plans"), it reported that their usage data shows that Claude Code users approve 97% of permission prompts. Anthropic also ran a controlled study with 1,053 paid testers and swapped a single prompt per session for a clearly dangerous command. The testers caught that command in 143 of 1,053 sessions, which is 13.6%. They also got worse over time: early in a session they blocked about 17% of the dangerous commands, and after 50 or more prompts about 5%.

Our own AIB gives the approver little to work with today. The Open Policy Agent (OPA) policy that sends a call to approval can attach a description and a `risk_level`, and that level is currently the only risk signal the approver gets. It is static per tool. A tool like `drive.share_file` is `medium` whether the agent shares a file with a colleague or hands editor rights to `thirdparty.example.com`. A policy author could write rules about single arguments, because OPA receives the arguments of the call. But someone would have to write such a rule for every tool and every argument that matters, and I don't see that happening when we face an ever growig number of evolving Model Context Protocol (MCP) tools.

## The Model Answers Questions and a Policy Auto-Approves

A [System One model](https://systemonemodels.org/guides/what-is-a-system-one-model/ "What is a System One (System 1) model?") doesn't generate text. It takes some content and a set of typed questions, and it returns typed answers with probabilities. TypeSafe AI coined the term in September when it announced Jev. The following is an illustrative example I wrote against a local `laya:en`, an open-weights System One model that I run with [Ollaya](https://ollaya.dev/ "Ollaya: Run decision models locally"):

```shell {filename="system-one-request.sh"}
curl http://localhost:11435/v1/systemone -d '{
  "model": "laya:en",
  "state": {
    "mcp_server": "google-drive-mcp",
    "tool_name": "drive.share_file",
    "policy_risk_level": "medium",
    "arguments": {
      "role": "editor",
      "grantee_domain": "thirdparty.example.com",
      "transfer_ownership": false
    }
  },
  "questions": {
    "leaves_organisation": {
      "type": "noul",
      "instructions": "Does this call give access or data to a party outside the organisation?"
    },
    "changes_access": {
      "type": "noul",
      "instructions": "Does this call change who can access a resource?"
    },
    "reversibility": {
      "type": "score",
      "criteria": [
        "no persistent effect",
        "reversible with effort",
        "irreversible or externally visible"
      ]
    }
  }
}'
```

The model gets the tool, the policy's risk level and the arguments. A `noul` question is a yes/no question, and the model returns the probability that the answer is yes. A `score` question places the content on an ordered scale that the caller defines. In this case, a useful model would return a probability close to 1 for the first two questions and a score around the middle level, "reversible with effort". A policy would then decide what follows. An operator could configure that a call is approved automatically when both probabilities are close to 0 and the score sits at "no persistent effect". The person never sees such a call. Everything else, like the call above, shows up on the approval page with the three answers next to it.

The beauty about this approach is that the model only answers questions while the approval itself is still a deterministic rule in a policy that can be reviewed and reasoned about. "Auto-approve when nothing leaves the organisation and the call has no persistent effect" is a sentence a security team can agree to, test and find again in an audit log next to the answers that triggered it.

Reducing the potential for prompt injection is another good reason for this approach. The arguments of a tool call are externally controlled content, and a model that reads them can be talked into things. A model whose whole output is two probabilities and a score has less room to be talked into an approval than a model that writes a verdict with a rationale. It can still be wrong.

Fixed answers also help shaping approval screen UX. OWASP's guidance on [Human-Agent Trust Exploitation](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ "OWASP Top 10 for Agentic Applications for 2026") (ASI09) asks for a "plain-language risk summary (not model-generated rationales)". "Gives editor access to thirdparty.example.com" is such a summary. A paragraph in which a model explains why the call is probably fine is the persuasive text that the OWASP entry warns about, and a System One model can't write one.

Auto modes in modern harnesses, commonly have the same goal. Instead of prompting the user, a classifier checks each tool call in the background and blocks the risky ones. Anthropic reports that the classifier blocked 89% of the dangerous commands in the study above, so a model that reads every call clearly beats a tired, fatigued human. The difference is who makes the call. In auto mode the classifier allows or blocks. The broker sits between many agents and many MCP servers in an organisation, and its operators have to explain why a call went through without a person. Fixed questions and a verifiable policy give them that explanation.

## A Failing Model Never Approves Anything

The model will be unreachable at times, it will return answers that don't parse, and its answers will be uncertain or contradict each other. In all of these cases the request stays what it was before the model existed: a pending approval for the human in the loop. How the broker will detect an uncertain answer isn't something I have specified yet, but a probability near the middle is one candidate. What is abundandly clear though is, that a model's answers must never turn a policy denial into an approval. The same holds for a permanent denial that a person has set for a tool, which the broker's [approval API](https://agenticidentitybroker.dev/docs/api/approval-endpoints "Agentic Identity Broker: Tool Approval API") already puts above any matching approval.

So we want the model to only take approvals off a person for calls that this person would have been allowed to approve anyway. The worst outcome of an outage is today's approval page and an interrupted agent session.

## Two Questions Are Open Before I Build It

The first one is where the assessment runs. One idea is to put it at the policy decision point, where the model's answers would be one more input to the OPA policy and the placement wouldn't "make the broker the bottleneck for each tool call". The alternative is to run the assessment in the broker after the pending approval exists, so that a person can act on the request while the model is slow or down. I like that Magnus's placement keeps the decision in one place, but I'd also like human review to keep working when the model doesn't, and I don't have a settled answer yet.

The second one is what the model may see. MCP arguments can hold anything: the body of an email, a customer record, the content of a file. This makes a strong case for running a local model, close to the broker, so that the arguments don't leave the organisation. 

If you run tool approvals for agents, or you have an opinion on either question, please comment on [issue #206](https://github.com/zalando-incubator/agentic-identity-broker/issues/206 "AIB issue #206: Pluggable interface for an external decision model"). I'd also like to hear which questions you'd ask the model beyond my three.
