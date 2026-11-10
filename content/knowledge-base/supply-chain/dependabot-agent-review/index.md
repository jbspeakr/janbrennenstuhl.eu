---
title: "How can a coding agent review Dependabot security updates?"
linkTitle: "Dependabot agent review"
description: "A pragmatic way to handle Dependabot security updates on GitHub: grouped updates and a narrow auto-merge rule as the baseline, a coding agent with a read-only token as the reviewer, and the limits of Copilot's Agent Merge."
answer: "Keep Dependabot's security updates on, group them, and let a deterministic workflow merge only the patch-level updates that pass the required checks. A coding agent can review and fix the other pull requests in a job with a read-only token, while Copilot's Agent Merge only reacts to failed workflows and merge conflicts and reviews nothing."
claim: "A coding agent can review and fix Dependabot security updates with a read-only token when a separate, deterministic job decides what gets pushed and merged."
slug: dependabot-agent-review
date: 2026-11-10
weight: 10
topics: [application-security, agentic-engineering]
changes:
  - date: 2026-11-10
    note: "First version."
---

Security patches for dependencies are the one kind of update I don't want to delay, and also the kind I'm most tempted to merge unread. This entry describes a middle way: Dependabot keeps opening the pull requests, plain workflow rules decide what merges, and a coding agent does the reading in between. I had my coding agent write the workflow for [Atlas of a Life](https://github.com/jbspeakr/atlas-of-life), a small map side project that I maintain alone. The [pull request](https://github.com/jbspeakr/atlas-of-life/pull/19 "ci: review and fix Dependabot security updates with Claude") was still open on 10 November 2026 and the workflow has not processed a real Dependabot pull request yet, so I describe a design that still has to prove itself. The statements about GitHub's features come from GitHub's documentation as of the same day.

## Key findings

{{< finding id="deps-agent-deterministic-merge-gate" source="GitHub Docs, Automating Dependabot with GitHub Actions" url="https://docs.github.com/en/code-security/dependabot/working-with-dependabot/automating-dependabot-with-github-actions" >}}GitHub's Dependabot documentation suggests agentic workflows for dependency analysis, update summaries and remediation recommendations, while security enforcement and merge gating stay in deterministic GitHub Actions workflows.{{< /finding >}}

{{< finding id="deps-cooldown-not-for-known-vulns" source="OpenSSF, Concise Guide for Developing More Secure Software" url="https://best.openssf.org/Concise-Guide-for-Developing-More-Secure-Software" >}}OpenSSF recommends a cooldown of typically about 3 days for updating components without known vulnerabilities, and quick updates for vulnerable dependencies.{{< /finding >}}

{{< finding id="deps-dependabot-run-read-only" source="GitHub Docs, Troubleshooting Dependabot on GitHub Actions" url="https://docs.github.com/en/code-security/dependabot/troubleshooting-dependabot/troubleshooting-dependabot-on-github-actions" >}}A workflow run that Dependabot triggers gets a read-only `GITHUB_TOKEN` by default, and the only secrets available to it are Dependabot secrets, not GitHub Actions secrets.{{< /finding >}}

{{< finding id="deps-security-update-no-cooldown" source="GitHub Docs, Dependabot options reference" url="https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference" >}}Dependabot's default cooldown of 3 days applies to version updates only, so a security update can propose a release on the day it was published.{{< /finding >}}

{{< finding id="deps-agent-merge-no-review" source="GitHub Docs, Getting pull requests ready to merge with Agent Merge" url="https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/watch-and-fix-pull-requests" >}}Copilot's Agent Merge fixes failed GitHub Actions workflows and merge conflicts on a pull request, its automatic setting covers only pull requests the user creates, and GitHub states that it does not remove the need for human review.{{< /finding >}}

## Evidence

{{< studies caption="Sources on Dependabot automation, its critics, Copilot and auto-merge" >}}
{{< study title="ci: review and fix Dependabot security updates with Claude (pull request 19)" org="jbspeakr/atlas-of-life" year="2026" sample="n/a" method="Pull request" url="https://github.com/jbspeakr/atlas-of-life/pull/19" >}}Adds the Dependabot configuration and the workflow with an agent job and an apply job that this entry describes.{{< /study >}}
{{< study title="Automating Dependabot with GitHub Actions" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/code-security/dependabot/working-with-dependabot/automating-dependabot-with-github-actions" >}}Shows the `fetch-metadata` action and an auto-merge example, and says the built-in token can't add pull requests to a merge queue.{{< /study >}}
{{< study title="Troubleshooting Dependabot on GitHub Actions" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/code-security/dependabot/troubleshooting-dependabot/troubleshooting-dependabot-on-github-actions" >}}Explains that runs triggered by Dependabot are treated like runs from a fork, and how a workflow gets secrets and wider token permissions anyway.{{< /study >}}
{{< study title="Dependabot security updates" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates" >}}Says a security update raises the dependency to the minimum version that includes the patch, and describes grouped security updates.{{< /study >}}
{{< study title="Concise Guide for Developing More Secure Software" org="OpenSSF Best Practices Working Group" year="2026" sample="n/a" method="Guidance" url="https://best.openssf.org/Concise-Guide-for-Developing-More-Secure-Software" >}}Recommends quick updates for vulnerable dependencies and a cooldown for components without known vulnerabilities.{{< /study >}}
{{< study title="Dependency Management and Cooldown Policies" org="OWASP DevSecOps Guideline" year="2026" sample="n/a" method="Guidance" url="https://owasp.github.io/DevSecOpsGuideline/2-Process/2-3-Build/2-3-2-Software-Composition-Analysis/2-3-2-2-Dependency-Management-and-Cooldown-Policies/" >}}Describes cooldown policies for update bots and package managers, and the exceptions for emergency patches.{{< /study >}}
{{< study title="Upgrade best practices" org="Renovate Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.renovatebot.com/upgrade-best-practices/" >}}Recommends a minimum release age of 14 days before Renovate automerges third-party dependencies.{{< /study >}}
{{< study title="Turn Dependabot Off" org="Filippo Valsorda" year="2026" sample="n/a" method="Essay" url="https://words.filippo.io/dependabot/" >}}Argues that Dependabot's alerts ignore whether the vulnerable code is reachable, and replaces it with `govulncheck` and a scheduled test run against the latest dependencies.{{< /study >}}
{{< study title="Why Every Developer Thinks Dependabot Sucks (And They're Right)" org="Shivam Saraswat" year="2025" sample="n/a" method="Essay" url="https://blog.shivamsaraswat.com/dependabot-sucks/" >}}Lists alert fatigue, missing reachability context and gaps in transitive dependency coverage, and names the cases where Dependabot is still good enough.{{< /study >}}
{{< study title="Dependabot alerts are now assignable to AI agents for remediation" org="GitHub Changelog" year="2026" sample="n/a" method="Changelog" url="https://github.blog/changelog/2026-04-07-dependabot-alerts-are-now-assignable-to-ai-agents-for-remediation/" >}}Announces that Copilot, Claude and Codex can take a Dependabot alert and open a draft pull request with a proposed fix.{{< /study >}}
{{< study title="Getting pull requests ready to merge with Agent Merge" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/watch-and-fix-pull-requests" >}}Describes how Copilot fixes failed workflows and merge conflicts on a watched pull request, and that it replaces neither review nor merge requirements.{{< /study >}}
{{< study title="REST API endpoints for Agent Merge" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/rest/pulls/agent-merge" >}}Documents the `PUT` endpoint that enrolls a pull request, and who may call it.{{< /study >}}
{{< study title="Copilot automations" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations" >}}Describes prompt-based automations with event triggers, which are limited to private and internal repositories and aren't committed to Git.{{< /study >}}
{{< study title="Automatically merging a pull request" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request" >}}Defines auto-merge as merging after all required reviews and status checks pass.{{< /study >}}
{{< study title="GITHUB_TOKEN" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/actions/concepts/security/github_token" >}}Lists which events created with the built-in token start a workflow run.{{< /study >}}
{{< study title="Keeping your GitHub Actions and workflows secure Part 1: Preventing pwn requests" org="GitHub Security Lab" year="2021" sample="n/a" method="Security guidance" url="https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/" >}}Recommends building untrusted code in an unprivileged job and handing results to a privileged one as artifacts, which stay untrusted.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

Start without an agent. Enable Dependabot alerts and security updates, group the security updates per ecosystem and require status checks on the default branch. GitHub's own auto-merge example then merges patch-level updates once the checks pass, and it needs no model and no extra credentials.

Keep a release-age cooldown on every update that fixes no known vulnerability, and let security updates through. OpenSSF's guide suggests about 3 days, Dependabot applies 3 days to version updates by default, and my essay on [dependency updates]({{< ref "/post/automatic-dependency-updates" >}}) argues for 7.

Check whether your code calls the vulnerable function before you treat an alert as urgent. A scanner that traces the call graph, such as `govulncheck` for Go, answers that question. Dependabot's alerts don't.

Add the agent as a reviewer once reading the updates is the bottleneck, and split its work into 2 jobs. The agent job gets `contents: read` and `pull-requests: read`, checks the pull request out without persisted credentials and lets the agent commit locally only. The commits leave the job as a patch artifact. The apply job holds the write token, has no model API key and runs no package code. It applies the patch, refuses it when it touches protected paths such as `.github/`, and pushes only when the tests pass after the agent's fix.

Trigger the workflow on `pull_request` and run it only when both the pull request author and the triggering actor are `dependabot[bot]`. Store the model API key as a Dependabot secret, because Dependabot runs don't receive GitHub Actions secrets.

Tell the agent in the prompt that release notes, changelogs and the pull request text are third-party content, and allow it only the commands it needs: tests, lint, type checks and local `git`. Deny `git push` and edits to workflow files explicitly.

Dispatch what the built-in token won't start. A push or merge made with `GITHUB_TOKEN` creates no new `push` workflow run, so the apply job calls `gh workflow run` for the verification and the deployment after it pushes a fix or merges.

### For security and platform teams

Decide which updates may merge without a person, and check those conditions in the workflow's shell steps: the update type, the number of commits the agent made, and the test results on the exact head commit. The agent's verdict is one more condition next to them.

Decide who looks at a release that skips the cooldown. The OWASP DevSecOps Guideline accepts advisory-driven security updates as an exception that bypasses the delay by design, and it asks for a human review of the release before any other override. Renovate's maintainers recommend a minimum release age of 14 days before automerging third-party dependencies. An auto-merge rule for security updates on the day of the release goes further than both.

Treat the agent job as an untrusted workload, as I describe in [AppSec in the Age of Agentic Engineering]({{< ref "/post/appsec-agentic-engineering" >}}). Give it a dedicated model API key with a spending limit. The updated package's code runs in that job during `npm ci` and the tests, and it can read the key there.

Pin the actions that the workflow uses to commit SHAs. The listing below keeps the version tags from my pull request for readability.

## Why I keep Dependabot's security updates on

Just to set the tone right, the critics of Dependabot have a point. In February 2026, Filippo Valsorda published a security fix for a method of his Go package `filippo.io/edwards25519` that, in his words, essentially no one uses. He reports in [Turn Dependabot Off](https://words.filippo.io/dependabot/ "Filippo Valsorda: Turn Dependabot Off") that Dependabot then "opened thousands of PRs against unaffected repositories", including a repository that imports only an unaffected sub-package. He replaced Dependabot with 2 scheduled GitHub Actions. The first runs `govulncheck`, which reports a vulnerability only when the code can reach the vulnerable function. The second runs the test suite against the latest dependency versions. Shivam Saraswat's [Why Every Developer Thinks Dependabot Sucks](https://blog.shivamsaraswat.com/dependabot-sucks/) adds alert fatigue, missing context on reachability and gaps in transitive dependency coverage, and still concludes that Dependabot "works okay for small teams or projects where someone can manually triage alerts".

I agree with the noise argument, and Dependabot's version updates are off in this setup because of it. I keep the security updates for two reasons. `govulncheck` is a Go tool and Atlas of a Life is an npm project, where `npm audit` matches package versions and knows nothing about the functions my code calls. A security update also arrives as a pull request that, according to GitHub, raises the dependency "to the minimum version that includes the patch", so my CI and the agent have a concrete change to test.

The agent's review covers part of the triage that the critics miss. It looks up where my code uses the updated package and whether the release changes those calls. It doesn't decide whether the vulnerability was reachable in the first place, and a model reading code is weaker evidence than a call graph. On a project with a reachability-aware scanner I'd run that scanner first and let it decide which alerts deserve a pull request at all.

## How the workflow splits the work

Dependabot only opens security updates in this setup. The `dependabot.yml` turns version updates off with a pull request limit of 0, which security updates ignore. "Dependabot alerts" and "Dependabot security updates" have to be enabled in the repository settings too.

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: daily
    open-pull-requests-limit: 0
    labels: [dependencies, security]
```

The workflow then runs on every pull request that Dependabot opens or updates. I shortened the listing to the parts that carry the design, and the [full file](https://github.com/jbspeakr/atlas-of-life/pull/19/files) is in the pull request.

```yaml
on:
  pull_request:
    types: [opened, reopened, synchronize]
permissions: {}
jobs:
  agent:
    if: github.event.pull_request.user.login == 'dependabot[bot]' && github.actor == 'dependabot[bot]'
    permissions:
      contents: read
      pull-requests: read
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          persist-credentials: false
      - id: meta
        uses: dependabot/fetch-metadata@v2
      # npm ci, then the tests on Dependabot's change
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          allowed_bots: dependabot[bot]
          prompt: |
            Review the update, fix the code only if the tests fail,
            commit locally, write review.md and end with a verdict.
          claude_args: |
            --allowedTools "Read,Glob,Grep,Edit,Write,Bash(npm test:*),Bash(git commit:*)"
            --disallowedTools "Bash(git push:*),Edit(.github/**),Write(.github/**)"
      # the tests again, then git format-patch and upload-artifact
  apply:
    needs: agent
    permissions:
      contents: write
      pull-requests: write
      actions: write
    steps:
      # git am, path guard, push, comment, merge rule
```

The agent job first runs the repository's quick test gate on Dependabot's change. Claude, through the official `claude-code-action`, then finds every place the repository uses the updated packages, reads what changed between the 2 versions in `node_modules` and fixes my code only when the gate failed or the review found a break. It writes a review of under 300 words that ends in one of 3 verdicts: "Safe to merge", "Safe after local full verification" or "Needs a human". The job runs the gate a second time after Claude and uploads the review, the logs and the commits as an artifact.

The apply job downloads that artifact outside the workspace and applies the patches with `git am`. It refuses the fix when a changed file lies under a protected path or when the second gate failed. Otherwise it pushes to Dependabot's branch, dispatches the verification on the new head and posts the review as a comment with a table of both gate results. A prompt injected through release notes can therefore make the agent write a wrong review, but it can't push workflow changes, because the job that reads the release notes has no write token.

## Where Agent Merge and alert assignment fall short

GitHub offers 2 Copilot features that touch dependency updates. Since April 2026, I can assign a Dependabot alert to an AI agent, which is Copilot by default and can be Claude or Codex when they are enabled for the repository. Since October 2026, [Agent Merge](https://github.blog/changelog/2026-10-28-agent-merge-watches-and-fixes-pull-requests-in-the-cloud/ "GitHub Changelog: Agent Merge watches and fixes pull requests in the cloud") lets Copilot watch a pull request and fix failed workflows and merge conflicts. The table compares both with the workflow, going by GitHub's documentation. I haven't run the 3 options side by side.

| | Alert assigned to an agent | Agent Merge | Workflow in this entry |
| --- | --- | --- | --- |
| Starts when | A person assigns the alert in the UI or through the REST API | A person clicks "Watch and fix", or a REST API call enrolls the pull request with that person's token | Dependabot opens or updates a pull request |
| Result | A separate draft pull request | Fix commits on the watched pull request | A review comment with a verdict, plus fix commits on Dependabot's pull request |
| Needs | GitHub Code Security or GitHub Advanced Security, including for public repositories, and a Copilot plan with coding agent access | A paid Copilot plan and the repository's "Enable automations" policy | A model API key as a Dependabot secret |
| Merges | No | No, but it can be combined with auto-merge | Patch-level updates under the rule below |

Agent Merge is the simpler alternative on paper. Its [REST API](https://docs.github.com/en/rest/pulls/agent-merge "GitHub Docs: REST API endpoints for Agent Merge") enrolls a pull request with a single `PUT` call, so a short workflow could enroll every Dependabot pull request and switch on auto-merge. I haven't run the following sketch.

```yaml
on:
  pull_request:
    types: [opened]
jobs:
  enroll:
    if: github.event.pull_request.user.login == 'dependabot[bot]'
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ secrets.AGENT_MERGE_PAT }}
      REPO: ${{ github.repository }}
      PR: ${{ github.event.pull_request.number }}
    steps:
      - run: |
          gh api -X PUT "/agents/repos/$REPO/pulls/$PR/agent-merge" \
            -f 'allowed_actions[]=fix_ci' \
            -f 'allowed_actions[]=resolve_merge_conflicts'
          gh pr merge --auto --squash "$PR" -R "$REPO"
```

The enrollment needs a person behind it. Agent Merge can switch itself on automatically, but GitHub offers that setting for "pull requests I create", and Dependabot creates its own. I found no equivalent setting for a repository or an organization. The `PUT` endpoint is "only available to users with a Copilot subscription, excluding Copilot Free users", and the caller needs write access to the repository. A run that Dependabot triggers gets a read-only `GITHUB_TOKEN`, so I expect the call to need a personal access token (PAT) of a Copilot user, stored as a Dependabot secret. The AI credits are then charged to that user. GitHub's documentation doesn't mention Dependabot pull requests. Its only stated exclusions are stacked pull requests and pull requests from forks, so Dependabot's branches look eligible, but I haven't seen that confirmed.

Agent Merge also reviews nothing. It starts on a failed workflow or a merge conflict, and an update that passes CI gets no second look. The workflow in this entry comments on every Dependabot pull request, including the green ones, and says whether anything my code calls changed behaviour.

Combined with auto-merge, Copilot's fix merges as soon as the required checks pass, unless a branch rule also requires an approving review. GitHub states that "Agent Merge does not remove the need for human review." The agent that repairs a failing workflow also produces the green check that auto-merge waits for. Repository custom instructions can ask Copilot to leave certain paths alone, but I can't declare in YAML which paths a fix may touch, or that a fixed update has to wait for me.

Copilot's commits change how Dependabot treats the pull request too. Every Dependabot pull request carries the note "Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself." The same limit applies to my workflow as soon as the apply job pushes a fix.

Two more Copilot routes exist. A shared [Copilot automation](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations "GitHub Docs: Copilot automations") runs a prompt when a pull request is opened and needs no YAML. Automations are limited to private and internal repositories, which rules them out for my public one. By default they ignore events from users without write access, and GitHub doesn't document whether Dependabot passes that check. GitHub stores them outside the repository's contents, so nobody reviews a change to the prompt in a pull request. An assigned alert waits until someone assigns it, and the agent then opens its own draft pull request next to Dependabot's. I'd use that for a breaking upgrade where a version bump alone doesn't fix the build.

If you already pay for Copilot and a branch rule requires an approving review, the enrollment workflow could be all you need: Copilot repairs the red pull requests and a person approves each one. GitHub's own [Agentic Workflows](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-github-agentic-workflows "GitHub Docs: GitHub Agentic Workflows") are the closer match when you want custom triage logic, another model, or the automation reviewed as code. They use read-only agents and declared "safe outputs", which is the same idea as the split in the previous section. The workflow in this entry is plain GitHub Actions YAML and doesn't use them.

## Where auto-merge stops

GitHub's auto-merge merges a pull request "automatically after all required reviews and status checks pass". Someone has to enable it for the repository, and GitHub offers it only on pull requests that can't be merged immediately, for example because a branch protection rule requires a status check that hasn't passed yet. GitHub's Dependabot example therefore comes with the advice to require status checks on the target branch. On a branch with a merge queue, the built-in `GITHUB_TOKEN` can't add pull requests to the queue at all, and the workflow needs a personal access token or a GitHub App token.

Required checks are also everything auto-merge looks at. It doesn't know whether an update is a patch or a major release, and it doesn't know whether an agent rewrote my code to make the tests pass. The workflow from my pull request needs neither the auto-merge setting nor branch protection. The apply job calls `gh pr merge --match-head-commit` itself, and only when all of these hold:

- `fetch-metadata` reports the update type `version-update:semver-patch`.
- Claude committed nothing.
- The quick gate passed before and after Claude.
- The last line of the review says "Safe to merge".
- The `quick` check on that exact head commit concluded with `success`. The job waits up to 10 minutes for it.

Minor and major updates, and every update the agent had to fix, wait for me. This rule has limits of its own:

- The verdict is model output. The other 4 conditions are deterministic, so a wrong verdict can at most merge a patch-level update that left my code unchanged and passed the tests.
- Green tests and a clean review are no malware check. Security updates skip Dependabot's cooldown, so the merged patch can be a release that is a few hours old. That is earlier than the release-age cooldown I recommend in my essay on [dependency updates]({{< ref "/post/automatic-dependency-updates" >}}), and earlier than the 14 days that Renovate's maintainers recommend before automerging. The workflow currently accepts that to close a known vulnerability quickly, and it doesn't check the release age of the fixed version. A team with more to lose than my side project could add that condition, or leave the merge of security updates to a person.
- A merge made with `GITHUB_TOKEN` starts no `push` workflow, so the apply job dispatches the deployment afterwards.
- Once the workflow pushes a fix, Dependabot stops resolving conflicts on that pull request. Commenting `@dependabot recreate` starts over.
- My hosted CI can't run the pixel and GPU checks of the atlas. The prompt names the rendering packages, and their updates get the verdict "Safe after local full verification" at best.

## Related

- [Dependency Updates: latest Is Not a Security Strategy]({{< ref "/post/automatic-dependency-updates" >}})
- [AppSec in the Age of Agentic Engineering]({{< ref "/post/appsec-agentic-engineering" >}})
- [Guest Lecture at HTW Berlin: AppSec in the Age of Agentic Engineering]({{< ref "/post/htw-berlin-agentic-appsec" >}})
