---
title: "System One for Tool Approvals: Let the Model Answer Questions, Not Decide"
linkTitle: "System One for Tool Approvals"
description: "People approve agent tool calls by reflex, and the Agentic Identity Broker's only risk signal today is a static risk level per tool. I propose a System One model that answers narrow, typed questions about a call's arguments, while configured rules and, in doubt, a person keep the decision."
claim: "A System One model can take reflex approvals off people if it only answers bounded questions about a tool call's arguments, configured rules turn those answers into a recommendation or an auto-approval, and an outage, a malformed answer or disagreeing answers send the request to a person."
date: 2026-11-10
slug: system-one-approvals
tags: ["agentic-engineering", "defensive-security", "ux-security"]
findings:
  - id: approval-prompts-reflex
    text: "Anthropic reports that Claude Code users approve 97% of permission prompts, and that in a controlled study with 1,053 paid testers, human review caught 13.6% of the dangerous commands that were swapped into a prompt."
  - id: system-one-questions-not-decisions
    text: "In my proposal for the Agentic Identity Broker, a System One model, which returns typed answers with probabilities and no generated text, answers bounded questions about the arguments of a tool call, such as whether the call gives access or data to a party outside the organisation, and rules configured in the broker make the decision. The model is never asked whether to approve or deny."
  - id: system-one-fails-to-person
    text: "An unavailable model, a malformed answer or answers that disagree must never auto-approve a tool call and never override a policy denial. In each of these cases the request stays a pending approval for a person."
draft: true
---

The [Agentic Identity Broker]({{< ref "/projects/agentic-identity-broker" >}}) (AIB) that Magnus Jungsbluth and I started can hold an agent's tool call until a person has approved it. An Open Policy Agent (OPA) policy decides which calls need that. The broker then creates a pending approval, and the person gets a page with a description of the call and a risk level. I think this page protects less than it looks like. People approve most of these requests by reflex, and each request still interrupts the agent's session.

In October I opened [issue #206](https://github.com/zalando-incubator/agentic-identity-broker/issues/206 "AIB issue #206: Pluggable interface for an external decision model") with a proposal. A fast "System One" model reads the actual arguments of a call and answers a few narrow questions about them: does this call give data to someone outside the organisation, does it change who has access, can it be undone? Rules that an operator configures in the broker turn the answers into a recommendation for the approver or, if the operator enables it, into an automatic approval. Nobody asks the model whether to approve, and when its answers disagree, the request goes to a person.

A [System One model](https://systemonemodels.org/guides/what-is-a-system-one-model/ "What is a System One (System 1) model?") is a rather new kind of model. TypeSafe AI coined the term in September when it announced Jev, and a bunch of hosted and open-weight models have followed since. Such a model doesn't generate text. It takes some content and a set of typed questions, and it returns an answer of the declared type with a probability for each. The name borrows from Daniel Kahneman's "Thinking, Fast and Slow", where System 1 is the fast, intuitive mode of thinking. A person who clicks through approval prompts is in that mode too, but without having read the arguments. None of my proposal is built yet, and before I start I'd like to know where the design breaks.

## People Approve Most Tool Calls Without Reading Them

The best public numbers on reflex approvals I know of come from Anthropic. When the company [made auto mode the default in Claude Code](https://claude.com/resources/articles/auto-mode-default-in-claude-code "Auto mode is now the default in Claude Code for Pro, Max, Ultra, and Team plans"), it reported that users approve 97% of permission prompts. Anthropic also ran a controlled study with 1,053 paid testers and swapped a single prompt per session for a clearly dangerous command. The testers caught that command in 143 of 1,053 sessions, which is 13.6%. They also got worse over time: early in a session they blocked about 17% of the dangerous commands, and after 50 or more prompts about 5%. These are a vendor's numbers about its own product, and the study ran in a test environment, so I read them as an indication and not as a measurement of approval pages in general.

Knowing better doesn't help much. In Sonar's [State of Code survey](https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/ "Sonar Data Reveals Critical Verification Gap in AI Coding") of more than 1,100 developers, 96% said they don't fully trust that AI-generated code is functionally correct, and only 48% said they always check it before they commit. That survey is about code and not about tool calls, but it shows the same gap between distrust and the work of checking.

The [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ "OWASP Top 10 for Agentic Applications for 2026") lists the consequence as ASI09, Human-Agent Trust Exploitation. The entry describes people who "over-rely on autonomous recommendations or unverifiable rationales, approving actions without independent validation". The approval then even works against the defender, because the person performs "the final, audited action" and the agent's part in it disappears from the record.

The broker gives the approver little to work with today. The OPA policy can attach a description and a `risk_level` to a call that needs approval, and that level is currently the only risk signal the approver gets. It is static per tool. A tool like `drive.share_file` is `medium` whether the agent shares a file with a colleague or hands editor rights to `thirdparty.com`. A policy author could write rules about single arguments, because the broker's gateway sidecar passes the parsed call to OPA. But someone would have to write such a rule for every tool and every argument that matters, and I don't see that happening for hundreds of Model Context Protocol (MCP) tools.

## I Ask the Model Questions and Let Rules Decide

The issue contains an illustrative request in shorthand. It is a sketch and not a specification. The model I have in mind for it is `laya:en`, the English checkpoint of [Laya](https://systemonemodels.org/models/laya/ "Laya by Convai Innovations"), an open-weights System One model from Convai Innovations, served locally by [Ollaya](https://ollaya.dev/ "Ollaya: Run decision models locally"). Ollaya is a community project that runs decision models the way Ollama runs LLMs, and its `/v1/systemone` endpoint takes the same request format as TypeSafe's Jev. Written out for that endpoint, the sketch looks like this:

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

The model gets the tool, the policy's risk level and the arguments. `noul` and `score` are two of the question types that System One decision models share. A Noul question is a yes/no question, and the model returns the probability that the answer is yes. A Score question places the content on an ordered scale that the caller defines. For this call, a useful model returns a probability close to 1 for the first two questions and a score around the middle level, "reversible with effort". A rule in the broker then decides what follows. An operator could configure that a call is approved automatically when both probabilities are close to 0 and the score sits at "no persistent effect", and that everything else shows up on the approval page with the three answers next to it.

Whether `laya:en` answers such questions well enough is open. Convai describes Laya as "a fast base to specialise, not a zero-shot decision engine", and Ollaya's model page says the raw checkpoints are over-confident until someone refits their calibration on labelled data. Thresholds in a rule are only worth something after that work.

I keep the decision away from the model mainly because an operator can review a rule. "Auto-approve when nothing leaves the organisation and the call has no persistent effect" is a sentence a security team can agree to, test and find again in an audit log next to the answers that triggered it. A model that returns "approve" leaves only the model to ask why. I made a similar point about reviewers based on large language models in [AppSec in the Age of Agentic Engineering]({{< ref "/post/appsec-agentic-engineering/index.md" >}} "AppSec in the Age of Agentic Engineering"): they catch things that rules miss, but they don't return the same result on every run, so they need something deterministic next to them.

Prompt injection is another reason. The arguments of a tool call are content that an attacker may have written, and a model that reads them can be talked into things. A model whose whole output is two probabilities and a score has less room to be talked into an approval than a model that writes a verdict with a rationale. It can still be wrong. The guide linked above notes that a System One model "can pick the wrong option with high confidence", and that Jev by default treats everything in its input as data and not as potentially hostile. That's why uncertain and disagreeing answers matter. How the broker detects them isn't specified yet. A probability near the middle is one candidate, and answers that contradict each other are another.

Fixed answers also change what the approver sees. OWASP's guidance for ASI09 asks for a "plain-language risk summary (not model-generated rationales)". "Gives editor access to thirdparty.com" is such a summary. A paragraph in which a model explains why the call is probably fine is the persuasive text that the OWASP entry warns about, and a System One model can't write one. Still, I expect a recommendation to pull people towards accepting it, and I don't know yet how strong that pull is.

Claude Code's auto mode takes the other route: a classifier looks at each tool call and allows or blocks it. Anthropic reports that the classifier blocked 89% of the dangerous commands in the study above, so a model that reads every call clearly beats a tired person. I don't doubt that. My concern is a different setting. The broker sits between many agents and many MCP servers in an organisation, and its operators have to explain why a call went through. Fixed questions and configured rules give them that explanation.

## Where the Assessment Runs Is Still Open

Magnus answered on the issue that the assessment belongs at the policy decision point, in line with attribute-based access control (ABAC) systems. The model's answers would be one more input to the OPA policy, which "can override / augment the output before it reaches the broker". His argument is about scale: the policy engine and the broker scale separately, and this placement "does not make the broker the bottleneck for each tool call".

The alternative is to run the assessment in the broker, after the pending approval exists. As far as I can see, the broker isn't on the path of every call then either, because only calls that the policy already sent to approval get assessed. The pending approval is there first, so the person can act on it while the model is slow or down, and the assessment arrives later as a recommendation or as an auto-approval.

Repo Assist, an automated workflow that comments on our issues, looked at the code for both options. The sidecar already gives OPA the MCP arguments, so the policy route needs no new plumbing for the input. On the other side, the broker's `ApprovalContext` carries only `description` and `risk_level`. Structured answers need a new contract between policy, broker and approval page, whichever route we take.

I don't have a settled answer yet. Magnus's placement keeps the decision in one place, which I like. But it puts a model call with a timeout into the request path of every assessed call, and I'd like human review to keep working when the model doesn't.

## The Whole Argument Map Must Not Leave by Default

MCP arguments can hold anything: the body of an email, a customer record, the content of a file. If the model runs outside the deployment, every assessed call sends that content to one more party. Forwarding the complete argument map can't be the default for that reason. Repo Assist put it as the second open decision on the issue: which argument fields may leave the deployment, and which timeout and retention apply.

The example above hints at an answer. The three questions need `role`, `grantee_domain` and `transfer_ownership`, and they don't need the file. An operator could name, per tool, the fields that the model may see, and a tool without such a list would never be assessed. The interface is meant to be pluggable, so an operator could also keep the model inside their own deployment. `laya:en` has 421M parameters and runs on a CPU, and Ollaya listens on `127.0.0.1` by default, so in the setup above no argument leaves the machine. I'd make the operator choose in both cases.

## A Failing Model Never Approves Anything

The model will be unreachable at times, it will return answers that don't parse, and its answers will contradict each other. In all three cases the request stays what it was before the model existed: a pending approval for a person. The model's answers can also never turn a policy denial into an approval. The same holds for a permanent denial that a person has set for a tool, which the broker's [approval API](https://agenticidentitybroker.dev/docs/api/approval-endpoints "Agentic Identity Broker: Tool Approval API") already puts above any matching approval.

So the model can only remove friction from calls that the policy would have let a person approve anyway. The worst outcome of an outage is today's approval page. The worst outcome of a wrong answer is bigger, because with auto-approval enabled, a call goes through that a person might have stopped. That's why auto-approval is off unless an operator turns it on, and why I'd start with recommendations.

## The Protocols Leave Open Who Decides

Three proposals on the MCP [Specification Enhancement Proposal (SEP) tracker](https://plan.modelcontextprotocol.io/seps "MCP SEP tracker") and one IETF draft work on the same area. The tracker lists all three SEPs as proposals without a sponsor.

[SEP-2793](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2793 "SEP-2793: Tool Risk Metadata") adds graded risk metadata to a tool's annotations, with fields such as `riskLevel`, `blastRadius` and `reversibility`. That would standardize what the broker's `risk_level` does today, and it has the same limit: the server declares the values per tool, before anyone knows the arguments.

[SEP-2848](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2848 "SEP-2848: Asynchronous Approval for Tool Calls") lets a server answer a tool call with a task handle while an approval is pending, so that the original request doesn't have to stay open. The draft binds the pending task to a digest of the call's arguments and re-evaluates the policy before it executes the tool. It leaves open who approves: "a human reviewer, a supervising agent, a policy or risk engine". The IETF's [Deferred Token Response](https://datatracker.ietf.org/doc/draft-ietf-oauth-deferred-token-response/ "draft-ietf-oauth-deferred-token-response") does the same one layer below. The OAuth working group adopted the draft in September and published its second revision on 31 October. With it, a token endpoint can answer "later" with a `deferral_code` and a polling interval. The draft names agents that request more access than they were given as a use case and supports decisions that "a different user, a different system, or no human at all" completes. The protocol between the authorization server and whatever makes that decision is out of scope.

[SEP-2672](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2672 "SEP-2672: Per-Call Passkey Verified Approval for MCP Tool Calls") goes the other way and makes a single approval stronger. The person confirms a specific call and its arguments with a passkey. The maintainers closed the pull request in September so that it can come back through a working group. I like the idea for the calls that matter. It's [step-up authentication]({{< ref "/post/stepup-authentication/index.md" >}} "Step-Up Authentication: Elevating Security with OpenID Connect (OIDC)") for agents, and step-up only works if the extra friction is kept for sensitive actions. A passkey prompt on every call would train the same reflex with a fingerprint.

So the protocols are getting ready for calls that wait and for approvals that are bound to arguments. They leave to each deployment how to find out whether a person has to look at a call at all. That is the part #206 is about.

## Tell Me Where This Breaks Before I Build It

If you run tool approvals for agents, or you have an opinion on any of the open points, please comment on [issue #206](https://github.com/zalando-incubator/agentic-identity-broker/issues/206 "AIB issue #206: Pluggable interface for an external decision model"). I'm most interested in three things: whether the assessment belongs at the policy decision point or in the broker, which argument fields you'd let leave your deployment, and which questions you'd ask the model beyond my three. In case you want to see how approvals fit next to the grants that people give agents in the first place, my [field guide entry on consent and revocation]({{< ref "/knowledge-base/agent-identity/consent-and-revocation" >}}) covers that side.
