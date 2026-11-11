---
title: "How do I auto-merge Dependabot updates securely?"
linkTitle: "Dependabot auto-merge"
description: "How to configure Dependabot so that it opens few, aged pull requests, and which conditions a workflow should check before it merges one of them without a person."
answer: "Let a workflow merge only patch-level Dependabot updates, on a branch that requires named status checks, after it has verified the pull request author and Dependabot's own metadata. Leave version updates behind a release-age cooldown, and keep minor and major updates and anything that deploys by itself for a person, because passing tests don't show that a release is benign."
claim: "Auto-merging Dependabot updates is defensible for patch-level updates that have passed a release-age cooldown and required status checks, in a workflow that checks the pull request author and never the triggering actor."
slug: dependabot-auto-merge
date: 2026-11-11
weight: 10
topics: [application-security, engineering-practice]
changes:
  - date: 2026-11-11
    note: "First version."
---

This entry covers Dependabot on github.com as GitHub documented it on 11 November 2026. Dependabot does two jobs. Security updates answer a published advisory with a pull request to the patched version, and version updates keep dependencies current on a schedule. The two behave differently in almost every setting below.

## Key findings

{{< finding id="deps-dependabot-no-native-automerge" source="GitHub, dependabot-core issue 1973 (2020)" url="https://github.com/dependabot/dependabot-core/issues/1973#issuecomment-640918321" >}}Dependabot has no auto-merge of its own by design: GitHub wrote in 2020 that it was "concerned about auto-merge being used to quickly propagate a malicious package across the ecosystem".{{< /finding >}}

{{< finding id="deps-dependabot-run-read-only" source="GitHub Changelog, 18 February 2021" url="https://github.blog/changelog/2021-02-18-github-actions-workflows-triggered-by-dependabot-prs-will-run-with-read-only-permissions/" >}}Since March 2021, workflow runs that Dependabot triggers get a read-only `GITHUB_TOKEN` and no repository secrets, a change GitHub made "to prevent potentially compromised dependencies from capturing secrets".{{< /finding >}}

{{< finding id="deps-actor-check-confused-deputy" source="Hugo Vincent, GitHub Actions exploitation: Dependabot (Synacktiv, 2024)" url="https://www.synacktiv.com/publications/github-actions-exploitation-dependabot.html" >}}An auto-merge workflow on `pull_request_target` that only checks `github.actor == 'dependabot[bot]'` can be made to merge an attacker's pull request, because `github.actor` names whoever caused the latest event and an attacker can make Dependabot force-push to a pull request from a fork.{{< /finding >}}

{{< finding id="deps-security-update-no-cooldown" source="GitHub Docs, Dependabot options reference" url="https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference" >}}Dependabot's default cooldown of 3 days applies to version updates only, so a security update can propose a release on the day it was published.{{< /finding >}}

{{< finding id="deps-renovate-14-days-automerge" source="Renovate Docs, Upgrade best practices" url="https://docs.renovatebot.com/upgrade-best-practices/" >}}The maintainers of Renovate, the other widely used update bot, recommend a minimum release age of 14 days before automerging third-party dependencies.{{< /finding >}}

## Evidence

{{< studies caption="Sources on Dependabot configuration and auto-merge" >}}
{{< study title="Support auto merge in Dependabot (issue 1973)" org="dependabot/dependabot-core" year="2020" sample="n/a" method="Maintainer statement" url="https://github.com/dependabot/dependabot-core/issues/1973#issuecomment-640918321" >}}States that GitHub-native Dependabot won't support auto-merge for the foreseeable future, and why.{{< /study >}}
{{< study title="Workflows triggered by Dependabot PRs will run with read-only permissions" org="GitHub Changelog" year="2021" sample="n/a" method="Changelog" url="https://github.blog/changelog/2021-02-18-github-actions-workflows-triggered-by-dependabot-prs-will-run-with-read-only-permissions/" >}}Treats runs triggered by Dependabot like runs from a fork: read-only token, no secrets.{{< /study >}}
{{< study title="Automating Dependabot with GitHub Actions" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/code-security/dependabot/working-with-dependabot/automating-dependabot-with-github-actions" >}}Shows the auto-merge workflow this entry builds on, advises required status checks, and says the built-in token can't add pull requests to a merge queue.{{< /study >}}
{{< study title="dependabot/fetch-metadata" org="GitHub" year="2026" sample="n/a" method="Documentation" url="https://github.com/dependabot/fetch-metadata" >}}Documents the outputs `update-type` and `dependency-type`, and that they are only populated for pull requests opened by Dependabot that contain only Dependabot's commits.{{< /study >}}
{{< study title="GitHub Actions exploitation: Dependabot" org="Synacktiv" year="2024" sample="2 projects shown" method="Security research" url="https://www.synacktiv.com/publications/github-actions-exploitation-dependabot.html" >}}Demonstrates the `github.actor` bypass on the auto-merge workflows of spring-security and trpc.{{< /study >}}
{{< study title="Weaponizing Dependabot: Pwn Request at its Finest" org="Boost Security Labs" year="2025" sample="n/a" method="Security research" url="https://labs.boostsecurity.io/articles/weaponizing-dependabot-pwn-request-at-its-finest/" >}}Lists which GitHub context values an attacker can influence, and describes a branch protection bypass when Dependabot is on the bypass list.{{< /study >}}
{{< study title="The case for a cooldown: Why Dependabot now waits before issuing version updates" org="The GitHub Blog" year="2026" sample="21 incidents, 2018 to 2026" method="Vendor analysis" url="https://github.blog/security/supply-chain-security/the-case-for-a-cooldown-why-dependabot-now-waits-before-issuing-version-updates/" >}}Explains the 3-day default, why security updates are exempt, and which attacks a cooldown doesn't stop.{{< /study >}}
{{< study title="Tame Dependabot: Group your updates, slow the cadence, keep security fast" org="The GitHub Blog" year="2026" sample="n/a" method="Vendor guidance" url="https://github.blog/security/supply-chain-security/tame-dependabot-group-your-updates-slow-the-cadence-keep-security-fast/" >}}Recommends grouped version updates on a weekly or monthly schedule, with security updates left immediate.{{< /study >}}
{{< study title="Concise Guide for Developing More Secure Software" org="OpenSSF Best Practices Working Group" year="2023" sample="n/a" method="Guidance" url="https://best.openssf.org/Concise-Guide-for-Developing-More-Secure-Software" >}}Asks for quick updates of vulnerable dependencies and a cooldown of typically about 3 days for components without known vulnerabilities.{{< /study >}}
{{< study title="Upgrade best practices" org="Renovate Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.renovatebot.com/upgrade-best-practices/" >}}Recommends 14 days of release age before automerging third-party dependencies.{{< /study >}}
{{< study title="Dependabot guidelines" org="UK Ministry of Justice Developer Portal" year="2026" sample="n/a" method="Organization guidance" url="https://developer-portal.service.justice.gov.uk/guidelines/dependabot-guidelines" >}}Advises small groups by purpose and risk, and individual pull requests for production dependencies and security fixes.{{< /study >}}
{{< study title="Automattic/dependabot-auto-merge-action" org="Automattic" year="2026" sample="n/a" method="Open-source workflow" url="https://github.com/Automattic/dependabot-auto-merge-action" >}}Merges security updates only after 4 gates: an advisory ID, a CVSS score of 7.0 or higher, a compatibility score of 80% or higher, and 7 days of age.{{< /study >}}
{{< study title="Turn Dependabot Off" org="Filippo Valsorda" year="2026" sample="n/a" method="Essay" url="https://words.filippo.io/dependabot/" >}}Argues that Dependabot's alerts ignore whether the vulnerable code is reachable, and replaces them with `govulncheck` and scheduled tests against the latest dependencies.{{< /study >}}
{{< study title="Automatic merging of dependency update PRs" org="Thoughtworks Technology Radar" year="n/a" sample="n/a" method="Practitioner assessment" url="https://www.thoughtworks.com/radar/techniques/automatic-merging-of-dependency-update-prs" >}}Advocates automatic merging when a green pipeline, including functional tests and security scanning, means the software is ready for production.{{< /study >}}
{{< study title="GITHUB_TOKEN" org="GitHub Docs" year="2026" sample="n/a" method="Documentation" url="https://docs.github.com/en/actions/concepts/security/github_token" >}}Lists which events created with the built-in token start a workflow run.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

Reduce what Dependabot opens before you automate what it merges. Keep security updates enabled, put version updates on a weekly or monthly schedule, group minor and patch updates, and keep the cooldown for version updates at the default of 3 days or longer.

Require at least one named status check on the default branch and allow auto-merge in the repository settings. GitHub's auto-merge waits for required reviews and status checks, so it has nothing to wait for on a branch without them.

Write the merge workflow on the `pull_request` trigger. Check `github.event.pull_request.user.login`, the author of the pull request, and never `github.actor` alone. Read the update type from the official `dependabot/fetch-metadata` action and enable auto-merge only for `version-update:semver-patch`.

Give that job `contents: write` and `pull-requests: write` and nothing else. It needs no checkout and should run no code from the pull request. Pin the actions it uses to full commit SHAs.

Keep the CI jobs that install and test the update on the read-only token that Dependabot runs get by default. Don't move them to `pull_request_target` to reach secrets.

### For security and platform teams

Decide which updates may merge without a person and write the rule down. A common first rule is patch level only, with required checks, and with dependencies in the build and deployment path excluded. Microsoft's [Zero Trust workshop guidance](https://microsoft.github.io/zerotrustassessment/docs/workshop-guidance/devsecops/DS_020 "Microsoft Zero Trust: Enable Dependabot alerts and security updates") adds a dependency review without new vulnerabilities or license issues and a tested rollback path.

Decide separately what happens to security updates. They skip the cooldown, so auto-merging them trades the waiting time for a fast fix. Automattic's public workflow keeps an age gate of 7 days even for security fixes and sends everything that fails a gate to human review.

Keep a gate between an automatic merge and a release. An auto-merged update that deploys or publishes by itself removes the last point where someone could notice a bad release.

Keep Dependabot off the bypass list of branch protection rules and rulesets. If it has to be on the list, protect the `dependabot/**` branches like the default branch, as Boost Security recommends.

Scan workflow files for the `github.actor` pattern. Boost Security's [`poutine`](https://boostsecurityio.github.io/poutine/rules/confused_deputy_auto_merge/ "poutine: Confused Deputy Auto-Merge") has a rule for it, and Synacktiv points to its own `octoscan`.

## Why Dependabot doesn't merge by itself

The preview version of Dependabot could merge its own pull requests. GitHub dropped the feature when it integrated Dependabot, and a member of the Dependabot team explained in 2020 that auto-merge "will not be supported in GitHub-native Dependabot for the foreseeable future", because of the concern "about auto-merge being used to quickly propagate a malicious package across the ecosystem". The issue is still open.

The following year GitHub also cut the privileges of the workflows that run on Dependabot's pull requests. Such a run is treated like a run from a fork, with a read-only `GITHUB_TOKEN` and no repository secrets, "to prevent potentially compromised dependencies from capturing secrets referenced in your workflows". A workflow can raise the token's permissions with the `permissions` key and can read secrets stored as Dependabot secrets. Every auto-merge setup relies on one of the two, so it should ask for as little as possible.

## How to get fewer and older pull requests

Version updates are where the noise comes from, and GitHub's own advice in 2026 is to slow them down. Its blog recommends a weekly or monthly schedule and groups, so that 10 pull requests become one. Since mid-2026, Dependabot also waits 3 days after a release before it opens a version update. GitHub reviewed 21 widely reported supply chain incidents between 2018 and 2026 and found that the malicious versions were typically pulled within hours, so a short delay filters most of them out. The `cooldown` option widens that window.

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
      semver-major-days: 30
    groups:
      minor-and-patch:
        applies-to: version-updates
        patterns: ["*"]
        update-types: [minor, patch]
```

Major updates stay out of the group in this example and arrive as individual pull requests. How far to take grouping is disputed. GitHub's blog starts with a single wildcard group for everything. The UK Ministry of Justice's guidelines call that an anti-pattern and keep production dependencies and security fixes in pull requests of their own, so that a fix is easy to track and to revert. A group also changes what an automatic merge covers. `fetch-metadata` reports the highest semver change in the pull request, so a rule for patch updates merges the whole group at once.

Security updates ignore the schedule, the cooldown and an `open-pull-requests-limit` of 0, which is the documented way to run Dependabot for security updates only. They can be grouped with `applies-to: security-updates`.

Dependabot's alerts have a known weakness. They match package versions and, by default, don't check whether the code calls the vulnerable function. Filippo Valsorda describes a fix to a method of his Go package that "essentially no one uses", after which Dependabot "opened thousands of PRs against unaffected repositories". He replaced Dependabot with `govulncheck`, which reports a vulnerability only when the vulnerable symbol is reachable, and a scheduled test run against the latest dependencies. GitHub has a reachability analysis for Dependabot alerts in public preview, for JavaScript and TypeScript only. Where a reachability-aware scanner exists for the ecosystem, it is the better source for deciding which alerts are urgent.

## A workflow that merges patch updates

This workflow follows the example in GitHub's documentation. It doesn't check out the repository and runs nothing from the pull request. The commit SHA of `fetch-metadata` is the one that GitHub's documentation pins, so check for a newer release before you copy it.

```yaml
name: Dependabot auto-merge
on: pull_request
permissions: {}
jobs:
  automerge:
    if: github.event.pull_request.user.login == 'dependabot[bot]'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - id: meta
        uses: dependabot/fetch-metadata@d7267f607e9d3fb96fc2fbe83e0af444713e90b7
      - if: steps.meta.outputs.update-type == 'version-update:semver-patch'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ github.token }}
```

Three details carry the security of it. The `if` condition reads the author of the pull request. In the attack that Synacktiv published in 2024, the attacker opens a pull request from a Dependabot branch in a fork and then comments `@dependabot recreate` in the fork. Dependabot force-pushes, the victim's `pull_request_target` workflow runs again, and `github.actor` is now `dependabot[bot]`. The author of that pull request is still the attacker, so the author check fails where the actor check passed. Boost Security reports that this pattern was exploited against the Kong Ingress Controller in December 2024.

The `fetch-metadata` action adds a second check. Its outputs are only populated when Dependabot opened the pull request and the pull request contains only Dependabot's commits, with a verified signature unless `skip-commit-verification` is set. A commit that someone pushed onto Dependabot's branch therefore stops the merge.

`gh pr merge --auto` doesn't merge. It asks GitHub to merge once the required reviews and status checks have passed, which is why the branch needs a named required check. The CI that produces that check runs the updated package's code, including install scripts, and it does so with the read-only token and without secrets.

## What auto-merge can't see

Required checks are all that auto-merge looks at, and tests rarely notice a release that steals credentials. The release-age cooldown is the control for that case, and it only covers version updates. A security update has no cooldown, and `fetch-metadata` reports no release date, so a rule that merges security patches on arrival can merge a release that is a few hours old. Renovate's maintainers recommend 14 days before automerging, and Automattic's workflow merges security fixes from a scheduled job after 7 days. OpenSSF asks for the opposite priority on known vulnerabilities, "quickly update vulnerable dependencies", so this is a trade-off to decide per repository.

A cooldown has limits of its own. GitHub writes that it "does little against attacks that play a longer game, including backdoors planted in releases and left dormant, maintainer sabotage, or a compromised build system".

The semver level is the maintainer's label and no guarantee. A patch release can break behaviour, and a malicious release can carry a patch version number.

Two platform details affect the setup. On a branch with a merge queue, the built-in `GITHUB_TOKEN` can't add pull requests to the queue, and the workflow needs a personal access token or a GitHub App token. A merge made with the `GITHUB_TOKEN` creates no `push` workflow run, so a deployment that starts on `push` to the default branch doesn't start after such a merge. That gap can serve as the gate between merge and release. Closing it with a stronger token turns auto-merge into auto-deploy.

Thoughtworks takes the most permissive position among the sources here. It advocates automatic merging, major updates of indirect dependencies included, when the pipeline has functional and performance tests and security scanning and a green run means the software is ready for production. That condition is about test coverage. It doesn't answer the malicious release, which is why the age gate matters even with good tests.

## Where coding agents fit

GitHub's Dependabot documentation suggests agentic workflows "for dependency analysis, update summaries, and remediation recommendations, while keeping security enforcement and merge gating in deterministic GitHub Actions workflows". That matches the split in this entry: an agent can read the changelog and the call sites and write a review, and the rule that merges stays in YAML.

GitHub also offers 2 Copilot features in this area. A Dependabot alert can be assigned to Copilot or another coding agent, which opens a draft pull request with a proposed fix. This requires GitHub Code Security or GitHub Advanced Security, including for public repositories. Agent Merge lets Copilot fix failed workflows and merge conflicts on a pull request, and GitHub states that it "does not replace your review of the changes or the repository's merge requirements". Both help with updates that break something. Neither changes which updates are safe to merge unread.

## Related

- [Dependency Updates: latest Is Not a Security Strategy]({{< ref "/post/automatic-dependency-updates" >}})
- [AppSec in the Age of Agentic Engineering]({{< ref "/post/appsec-agentic-engineering" >}})
