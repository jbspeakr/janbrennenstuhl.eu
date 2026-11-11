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

Asking a person before an agent runs a tool is the control that people expect in an agent loop. Coding agents ask before they run a shell command, and the [Agentic Identity Broker]({{< ref "/projects/agentic-identity-broker" >}}) (AIB) that Magnus Jungsbluth and I started holds a tool call until a person has approved it on a page with a description of the call and a risk level. The feature is also controversial, because the public numbers suggest that people approve nearly everything they are shown. A prompt that people answer by reflex protects little, and it still interrupts the agent's session.

I'd like to reduce the number of approvals a person gets presented. Most calls should never reach a person, and the few that do should be the critical ones and come with enough information to decide. Fewer requests mean less noise, and with that hopefully less approval fatigue. In October I opened [issue #206](https://github.com/zalando-incubator/agentic-identity-broker/issues/206 "AIB issue #206: Pluggable interface for an external decision model") with a proposal for AIB. A fast "System One" model reads the actual arguments of a call and answers a few narrow questions about them, such as whether the call gives data to someone outside the organisation. A policy that an operator configures then auto-approves the calls whose answers are harmless, and only the rest go to a person. The idea is similar to the auto mode in Claude Code, where a safety check in the background replaces most permission prompts. None of this is built yet, and before I start I'd like to know where the design breaks.

## People Approve Most Tool Calls Without Reading Them

The best public numbers on reflex approvals I know of come from Anthropic. When the company [made auto mode the default in Claude Code](https://claude.com/resources/articles/auto-mode-default-in-claude-code "Auto mode is now the default in Claude Code for Pro, Max, Ultra, and Team plans"), it reported that users approve 97% of permission prompts. Anthropic also ran a controlled study with 1,053 paid testers and swapped a single prompt per session for a clearly dangerous command. The testers caught that command in 143 of 1,053 sessions, which is 13.6%. They also got worse over time: early in a session they blocked about 17% of the dangerous commands, and after 50 or more prompts about 5%. These are a vendor's numbers about its own product, and the study ran in a test environment, so I read them as an indication and not as a measurement of approval pages in general.

The [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ "OWASP Top 10 for Agentic Applications for 2026") lists the consequence as ASI09, Human-Agent Trust Exploitation. The entry describes people who "over-rely on autonomous recommendations or unverifiable rationales, approving actions without independent validation". The approval then even works against the defender, because the person performs "the final, audited action" and the agent's part in it disappears from the record.

AIB gives the approver little to work with today. The Open Policy Agent (OPA) policy that sends a call to approval can attach a description and a `risk_level`, and that level is currently the only risk signal the approver gets. It is static per tool. A tool like `drive.share_file` is `medium` whether the agent shares a file with a colleague or hands editor rights to `thirdparty.com`. A policy author could write rules about single arguments, because OPA receives the arguments of the call. But someone would have to write such a rule for every tool and every argument that matters, and I don't see that happening for hundreds of Model Context Protocol (MCP) tools.

## The Model Answers Questions and a Policy Auto-Approves

A [System One model](https://systemonemodels.org/guides/what-is-a-system-one-model/ "What is a System One (System 1) model?") doesn't generate text. It takes some content and a set of typed questions, and it returns typed answers with probabilities. TypeSafe AI coined the term in September when it announced its model Jev. The issue contains an illustrative request, which is a sketch and not a specification. I wrote it against `laya:en`, an open-weights System One model that I run with [Ollaya](https://ollaya.dev/ "Ollaya: Run decision models locally"), simply because that was the model I had locally at hand:

```shell {filename="system-one-request.sh"}
curl http://localhost:11435/v1/systemone -d '{
  "model": "laya:en",
  "state": {
    "mcp_server": "google-drive-mcp",
    "tool_name": "drive.share_file",
    "policy_risk_level": "medium",
    "arguments": {
      "role": "editor",
      "grantee_domain": "thirdparty.com",
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

The model gets the tool, the policy's risk level and the arguments. A `noul` question is a yes/no question, and the model returns the probability that the answer is yes. A `score` question places the content on an ordered scale that the caller defines. For this call, a useful model returns a probability close to 1 for the first two questions and a score around the middle level, "reversible with effort". A policy then decides what follows. An operator could configure that a call is approved automatically when both probabilities are close to 0 and the score sits at "no persistent effect". The person never sees such a call. Everything else, like the call above, shows up on the approval page with the three answers next to it.

I haven't checked how well `laya:en` answers such questions. Its makers describe it as a base to specialise, so I'd expect any model to need tuning and calibration before a threshold in a rule means much.

I let the model answer questions and keep the approval itself in a policy, mainly because an operator can review a rule. "Auto-approve when nothing leaves the organisation and the call has no persistent effect" is a sentence a security team can agree to, test and find again in an audit log next to the answers that triggered it. A model that returns "approve" leaves only the model to ask why.

Prompt injection is another reason. The arguments of a tool call are content that an attacker may have written, and a model that reads them can be talked into things. A model whose whole output is two probabilities and a score has less room to be talked into an approval than a model that writes a verdict with a rationale. It can still be wrong. The guide linked above notes that a System One model "can pick the wrong option with high confidence", and that Jev by default treats everything in its input as data and not as potentially hostile.

Fixed answers also change what the approver sees on the calls that still reach them. OWASP's guidance for ASI09 asks for a "plain-language risk summary (not model-generated rationales)". "Gives editor access to thirdparty.com" is such a summary. A paragraph in which a model explains why the call is probably fine is the persuasive text that the OWASP entry warns about, and a System One model can't write one. Still, I expect a recommendation to pull people towards accepting it, and I don't know yet how strong that pull is.

Claude Code's auto mode has the same goal. Instead of prompting the user, a classifier checks each tool call in the background and blocks the risky ones. Anthropic reports that the classifier blocked 89% of the dangerous commands in the study above, so a model that reads every call clearly beats a tired person. The difference is who makes the call. In auto mode the classifier allows or blocks. The broker sits between many agents and many MCP servers in an organisation, and its operators have to explain why a call went through without a person. Fixed questions and a configured policy give them that explanation.

## A Failing Model Never Approves Anything

The model will be unreachable at times, it will return answers that don't parse, and its answers will be uncertain or contradict each other. In all of these cases the request stays what it was before the model existed: a pending approval for a person. How the broker detects an uncertain answer isn't specified yet, and a probability near the middle is one candidate. The model's answers can also never turn a policy denial into an approval. The same holds for a permanent denial that a person has set for a tool, which the broker's [approval API](https://agenticidentitybroker.dev/docs/api/approval-endpoints "Agentic Identity Broker: Tool Approval API") already puts above any matching approval.

So the model can only take approvals off a person for calls that this person would have been allowed to approve anyway. The worst outcome of an outage is today's approval page. The worst outcome of a wrong answer is bigger, because a call goes through that a person might have stopped. That's why an operator has to turn auto-approval on and decides which answers are harmless enough for it.

## Two Questions Are Open Before I Build It

The first one is where the assessment runs. Magnus answered on the issue that it belongs at the policy decision point, where the model's answers would be one more input to the OPA policy and the placement "does not make the broker the bottleneck for each tool call". The alternative is to run the assessment in the broker after the pending approval exists, so that a person can act on the request while the model is slow or down. I like that Magnus's placement keeps the decision in one place, but I'd also like human review to keep working when the model doesn't, and I don't have a settled answer yet.

The second one is what the model may see. MCP arguments can hold anything: the body of an email, a customer record, the content of a file. If the model runs outside the deployment, every assessed call sends that content to one more party, so forwarding the complete argument map can't be the default. The three questions above need `role`, `grantee_domain` and `transfer_ownership`, and they don't need the file. An operator could name, per tool, the fields that the model may see, or keep the model inside their own deployment. `laya:en` has 421M parameters and runs on a CPU, and Ollaya listens on `127.0.0.1` by default, so in the setup above no argument leaves the machine.

If you run tool approvals for agents, or you have an opinion on either question, please comment on [issue #206](https://github.com/zalando-incubator/agentic-identity-broker/issues/206 "AIB issue #206: Pluggable interface for an external decision model"). I'd also like to hear which questions you'd ask the model beyond my three.
