---
title: "How can a coding agent review Dependabot security updates?"
linkTitle: "Dependabot agent review"
description: "A GitHub Actions workflow that lets a coding agent review and fix Dependabot security updates with a read-only token, compared with Dependabot's Copilot integration and GitHub's auto-merge."
answer: "Run the coding agent on every Dependabot pull request in a job with a read-only token, and let a second job without the agent apply its fixes, post its review and merge only patch-level updates that needed no code change. Dependabot's own Copilot integration starts from an alert that someone assigns and needs a GitHub Code Security license, and GitHub's auto-merge only waits for required reviews and status checks."
claim: "A coding agent can review and fix Dependabot security updates with a read-only token when a separate, deterministic job decides what gets pushed and merged."
slug: dependabot-agent-review
date: 2026-11-10
weight: 10
topics: [application-security, agentic-engineering]
changes:
  - date: 2026-11-10
    note: "First version."
---

This entry describes a workflow that I had my coding agent write for [Atlas of a Life](https://github.com/jbspeakr/atlas-of-life), a small map side project that I maintain alone. The [pull request](https://github.com/jbspeakr/atlas-of-life/pull/19 "ci: review and fix Dependabot security updates with Claude") was still open on 10 November 2026 and the workflow has not processed a real Dependabot pull request yet, so I describe a design that still has to prove itself. The statements about GitHub's features come from GitHub's documentation as of the same day.

## Key findings

{{< finding id="deps-agent-deterministic-merge-gate" source="GitHub Docs, Automating Dependabot with GitHub Actions" url="https://docs.github.com/en/code-security/dependabot/working-with-dependabot/automating-dependabot-with-github-actions" >}}GitHub's Dependabot documentation suggests agentic workflows for dependency analysis, update summaries and remediation recommendations, while security enforcement and merge gating stay in deterministic GitHub Actions workflows.{{< /finding >}}

{{< finding id="deps-alert-agent-needs-license" source="GitHub Docs, Dependabot alerts" url="https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts" >}}Assigning a Dependabot alert to Copilot or another AI agent requires a license for GitHub Code Security or GitHub Advanced Security, including for public repositories, and the agent answers with a draft pull request of its own.{{< /finding >}}

{{< finding id="deps-dependabot-run-read-only" source="GitHub Docs, Troubleshooting Dependabot on GitHub Actions" url="https://docs.github.com/en/code-security/dependabot/troubleshooting-dependabot/troubleshooting-dependabot-on-github-actions" >}}A workflow run that Dependabot triggers gets a read-only `GITHUB_TOKEN` by default, and the only secrets available to it are Dependabot secrets, not GitHub Actions secrets.{{< /finding >}}

{{< finding id="deps-github-token-starts-no-run" source="GitHub Docs, GITHUB_TOKEN" url="https://docs.github.com/en/actions/concepts/security/github_token" >}}A push or merge made with the repository's `GITHUB_TOKEN` creates no new `push` workflow run, while `workflow_dispatch` and `repository_dispatch` events always create runs.{{< /finding >}}

{{< finding id="deps-security-update-no-cooldown" source="GitHub Docs, Dependabot options reference" url="https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference" >}}Dependabot's default cooldown of 3 days applies to version updates only, so a security update can propose a release on the day it was published.{{< /finding >}}

## Evidence

{{< studies caption="Sources on Dependabot automation, Copilot and auto-merge" >}}
{{< study title="ci: review and fix Dependabot security updates with Claude (pull request 19)" org="jbspeakr/atlas-of-life" year="2026" sample="n/a" method="Pull request" url="https://github.com/jbspeakr/atlas-of-life/pull/19" >}}Adds the Dependabot configuration and the workflow with an agent job and an apply job that this entry describes.{{< /study >}}
{{< study title="Automating Dependabot with GitHub Actions" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/code-security/dependabot/working-with-dependabot/automating-dependabot-with-github-actions" >}}Shows the `fetch-metadata` action and an auto-merge example, and says the built-in token can't add pull requests to a merge queue.{{< /study >}}
{{< study title="Troubleshooting Dependabot on GitHub Actions" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/code-security/dependabot/troubleshooting-dependabot/troubleshooting-dependabot-on-github-actions" >}}Explains that runs triggered by Dependabot are treated like runs from a fork, and how a workflow gets secrets and wider token permissions anyway.{{< /study >}}
{{< study title="Dependabot alerts are now assignable to AI agents for remediation" org="GitHub Changelog" year="2026" sample="n/a" method="Changelog" url="https://github.blog/changelog/2026-04-07-dependabot-alerts-are-now-assignable-to-ai-agents-for-remediation/" >}}Announces that Copilot, Claude and Codex can take a Dependabot alert and open a draft pull request with a proposed fix.{{< /study >}}
{{< study title="Getting pull requests ready to merge with Agent Merge" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/watch-and-fix-pull-requests" >}}Describes how Copilot fixes failed workflows and merge conflicts on a watched pull request, and that it replaces neither review nor merge requirements.{{< /study >}}
{{< study title="Automatically merging a pull request" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request" >}}Defines auto-merge as merging after all required reviews and status checks pass.{{< /study >}}
{{< study title="GITHUB_TOKEN" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/actions/concepts/security/github_token" >}}Lists which events created with the built-in token start a workflow run.{{< /study >}}
{{< study title="Keeping your GitHub Actions and workflows secure Part 1: Preventing pwn requests" org="GitHub Security Lab" year="2021" sample="n/a" method="Security guidance" url="https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/" >}}Recommends building untrusted code in an unprivileged job and handing results to a privileged one as artifacts, which stay untrusted.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

Split the work into 2 jobs. The agent job gets `contents: read` and `pull-requests: read`, checks the pull request out without persisted credentials and lets the agent commit locally only. The commits leave the job as a patch artifact. The apply job holds the write token, has no model API key and runs no package code. It applies the patch, refuses it when it touches protected paths such as `.github/`, and pushes only when the tests pass after the agent's fix.

Trigger the workflow on `pull_request` and run it only when both the pull request author and the triggering actor are `dependabot[bot]`. Store the model API key as a Dependabot secret, because Dependabot runs don't receive GitHub Actions secrets.

Tell the agent in the prompt that release notes, changelogs and the pull request text are third-party content, and allow it only the commands it needs: tests, lint, type checks and local `git`. Deny `git push` and edits to workflow files explicitly.

Dispatch what the built-in token won't start. After the apply job pushes a fix or merges, it calls `gh workflow run` for the verification and the deployment, since `workflow_dispatch` always creates a run.

### For security and platform teams

Decide which updates may merge without a person, and check those conditions in the workflow's shell steps: the update type, the number of commits the agent made, and the test results on the exact head commit. The agent's verdict is one more condition next to them.

Give the agent job a dedicated model API key with a spending limit. The updated package's code runs in that job during `npm ci` and the tests, and it can read the key there.

Pin the actions that the workflow uses to commit SHAs. The listing below keeps the version tags from my pull request for readability.

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

## Where Dependabot's Copilot integration falls short

GitHub offers 2 Copilot features that touch dependency updates. Since April 2026, I can assign a Dependabot alert to an AI agent, which is Copilot by default and can be Claude or Codex when they are enabled for the repository. Since October 2026, [Agent Merge](https://github.blog/changelog/2026-10-28-agent-merge-watches-and-fixes-pull-requests-in-the-cloud/ "GitHub Changelog: Agent Merge watches and fixes pull requests in the cloud") lets Copilot watch a pull request and fix failed workflows and merge conflicts. The table compares both with the workflow, going by GitHub's documentation. I haven't run the 3 options side by side.

| | Alert assigned to an agent | Agent Merge | Workflow in this entry |
| --- | --- | --- | --- |
| Starts when | A person assigns the alert in the UI or through the REST API | A person clicks "Watch and fix" on the pull request | Dependabot opens or updates a pull request |
| Result | A separate draft pull request | Fix commits on the watched pull request | A review comment with a verdict, plus fix commits on Dependabot's pull request |
| Needs | GitHub Code Security or GitHub Advanced Security, including for public repositories, and a Copilot plan with coding agent access | A paid Copilot plan and the repository's "Enable automations" policy | A model API key as a Dependabot secret |
| Merges | No | No, but it can be combined with auto-merge | Patch-level updates under the rule below |

For my one-person public repository, the starting point matters most. Agent Merge can switch itself on automatically, but GitHub documents that setting for "pull requests I create", and Dependabot creates its own. An alert waits until I assign it. In both cases I'm back to opening every update by hand, which is the part I wanted to delegate.

Neither feature reviews the pull request that Dependabot already opened. Agent Merge only starts on a failed workflow or a merge conflict, and an assigned agent opens its own fix next to Dependabot's. An update that passes CI gets no second look. The workflow comments on every Dependabot pull request, including the green ones, and says whether anything my code calls changed behaviour.

GitHub's assign dialog does accept a custom prompt and a model choice, so the alert route is configurable. It doesn't give me the split from the previous section, where I decide in YAML which paths an agent's fix may touch and which conditions lead to a merge. GitHub's own [Agentic Workflows](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-github-agentic-workflows "GitHub Docs: GitHub Agentic Workflows") follow the same idea with read-only agents and declared "safe outputs". The workflow in this entry is plain GitHub Actions YAML and doesn't use them.

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
- Green tests and a clean review are no malware check. Security updates skip Dependabot's cooldown, so the merged patch can be a release that is a few hours old. That is earlier than the release-age cooldown I recommend in my essay on [dependency updates]({{< ref "/post/automatic-dependency-updates" >}}), and the workflow accepts that to close a known vulnerability quickly.
- A merge made with `GITHUB_TOKEN` starts no `push` workflow, so the apply job dispatches the deployment afterwards.
- Once the workflow pushes a fix, Dependabot stops rebasing that pull request. Commenting `@dependabot recreate` starts over.
- My hosted CI can't run the pixel and GPU checks of the atlas. The prompt names the rendering packages, and their updates get the verdict "Safe after local full verification" at best.

## Related

- [Dependency Updates: latest Is Not a Security Strategy]({{< ref "/post/automatic-dependency-updates" >}})
- [AppSec in the Age of Agentic Engineering]({{< ref "/post/appsec-agentic-engineering" >}})
