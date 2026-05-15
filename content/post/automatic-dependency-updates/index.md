---
title: "Dependency Updates: latest Is Not a Security Strategy"
linkTitle: "latest Is Not a Security Strategy"
description: "Automatic dependency updates spread compromised packages faster than humans can react. Version pinning, provenance verification, and repository proxies turn blind trust into controlled trust."
excerpt: "Automatic dependency updates spread compromised packages faster than humans can react. Version pinning, provenance verification, and repository proxies turn blind trust into controlled trust."
lead: "Past and present supply chain compromises prove that automatic dependency updates are attack amplifiers. Here is what controlled trust looks like in practice."
slug: automatic-dependency-updates
image: automatic-dependency-updates.webp
date: 2026-05-15
lastmod: 2026-05-15
draft: false
weight: 50
categories: ["appsec"]
tags: ["supply-chain-protection", "sdlc"]
---

On March 31, 2026, [North Korean state actors compromised Axios](https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/ "Microsoft: Mitigating the Axios npm supply chain compromise"), an npm package with over 70 million weekly downloads. Any project declaring `axios@^1.14.0` connected to attacker C2 infrastructure the next time `npm update` ran. Six weeks later, a [self-propagating worm hit 42 TanStack packages](https://snyk.io/blog/tanstack-npm-packages-compromised/ "Snyk: TanStack npm packages compromised"). It reached Mistral AI and UiPath within hours. It also carried valid [SLSA provenance](https://slsa.dev/spec/v1.0/levels "SLSA security levels") attestations, signed by the legitimate build pipeline.

The same infrastructure that helps us stay current also amplified these attacks. Automated dependency updates pushed the compromised packages into production builds faster than any human could react.

We learned that outdated dependencies are dangerous. That is true. But many teams have flipped the lesson around. _Newer_ is treated as _safer_. It is not.

## The Trust Problem

Modern package managers are not static library linkers. They are code execution pipelines. A single `npm install` can run [arbitrary install scripts](https://docs.npmjs.com/cli/v11/using-npm/scripts "npm scripts documentation"), read credentials, and run with full CI permissions. It does this across hundreds of transitive packages that nobody on the team has reviewed. Every dependency expands your [trusted computing base](https://en.wikipedia.org/wiki/Trusted_computing_base "Trusted Computing Base").

{{< quote author="Ben Hoyt" source="Every dependency you add is a supply chain attack waiting to happen" url="https://benhoyt.com/writings/dependencies/" >}}
It's not every dependency you add that's a problem; it's every dependency you update.
{{< /quote >}}

Two problems arise here:

1. Version ranges like `^1.14.0` do not mean _"I trust version 1.14.0"_. They mean _"I trust every future release that matches this constraint"_. That is a large, open-ended trust delegation. The Axios attackers used exactly that. Version `1.14.1` was a [manifest-only change](https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/ "Microsoft: Mitigating the Axios npm supply chain compromise") that added a malicious dependency while leaving the Axios source code untouched. [Semantic versioning](https://semver.org/ "Semantic Versioning Specification") signals maintainer intent, not trustworthiness. The same applies to [floating Docker tags](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html "OWASP Docker Security Cheat Sheet"), [unpinned GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-third-party-actions "GitHub: Security hardening for GitHub Actions"), and `latest` tags everywhere.

2. Tools like [Dependabot](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart-guide) and [Renovate](https://docs.renovatebot.com/) normalized constant dependency updates. At scale, they improve visibility and shorten the window for known CVEs. But they also changed how we consume trust. Security automation quietly became trust automation. Dependency update PRs receive less review than internal code, even though they run with the same or higher privilege. The volume is overwhelming. Eventually the workflow shrinks to: CI passes → vulnerability score drops → merge. That creates a dangerous illusion. _"No known CVEs"_ does not mean _"safe"_. Supply-chain attacks are newly published, initially undetected, semantically valid, and technically _"up to date"_.

{{< quote author="Filippo Valsorda" source="Turn Dependabot Off" url="https://words.filippo.io/dependabot/" >}}
False positive alerts are not only a waste of time, they also reduce security by causing alert fatigue and making proper triage impractical.
{{< /quote >}}

The [XZ Utils backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor "XZ Utils backdoor") in 2024 showed how long-running social engineering can compromise critical infrastructure. The [Mini Shai-Hulud](https://www.wiz.io/blog/shai-hulud-2-0-ongoing-supply-chain-attack "Wiz: Shai-Hulud 2.0 Supply Chain Attack") incidents in 2025 and the ongoing supply chain attacks show that the attack surface extends well beyond maintainer compromise. It reaches into version ranges, build pipelines, provenance systems, and the update automation that ties them together. These are not theoretical risks. They are documented, attributed attacks against the most popular packages in the ecosystem.

## What Controlled Trust Looks Like

There is no perfect fix for supply-chain risk. There are practical ways to replace blind trust with controlled trust:

### Pin Versions

Remove `^` and `~` from `package.json` or whatever dependency manifest you use. Use exact versions. For transitive dependencies, force the version with [overrides](https://docs.npmjs.com/cli/v11/configuring-npm/package-json#overrides "npm overrides"):

```json
{
  "dependencies": { "axios": "1.14.0" },
  "overrides": { "axios": "1.14.0" }
}
```

Lockfiles like `package-lock.json`, `pnpm-lock.yaml`, `Cargo.lock`, and `poetry.lock` do not make dependencies safe. They make dependency state reproducible. You cannot investigate what you cannot reproduce.

### Enforce Release-Age Cooldowns

Supply-chain attacks have a short half-life. The compromised TanStack versions lasted about three hours before someone caught them. A [release-age cooldown](https://nesbitt.io/2026/03/04/package-managers-need-to-cool-down.html "Package Managers Need to Cool Down") rejects packages younger than a threshold. That gives the community time to spot compromises before they reach your builds:

```ini
# ~/.npmrc
min-release-age=7

# pnpm-workspace.yaml
minimumReleaseAge: 1440

# ~/.bunfig.toml
[install]
minimumReleaseAge = 604800

# ~/.config/uv/uv.toml
exclude-newer = "7 days"
```

A seven-day cooldown would have prevented both the Axios and TanStack compromises.

### Control Upgrade Cadence

Filippo Valsorda [recommends a better model](https://words.filippo.io/dependabot/#test-against-latest-instead-of-updating "Test against latest instead of updating") than auto-updating: Run your test suite against the latest dependency versions daily in a sandboxed CI job. You get early warning of breakage without pulling untrusted code into production. You still update. You do it on your schedule, after review, when you are ready.

### Verify Provenance, But Do Not Trust It Alone

The TanStack attack is the first documented case of malicious npm packages carrying valid [SLSA Build Level 3](https://slsa.dev/spec/v1.0/levels#build-l3 "SLSA Build Level 3") attestations. Provenance verification is necessary but not sufficient. Pair it with [install-time behavioral analysis](https://socket.dev "Socket: Supply Chain Security") to catch suspicious network calls, filesystem access, and hidden scripts before they run.

### Deploy Repository Proxies

Place package managers behind a properly configured repository proxy like [Sonatype Nexus](https://www.sonatype.com/products/sonatype-nexus-repository), [JFrog Artifactory](https://jfrog.com/artifactory/), or an internal mirror. These proxies should be configured not only to mirror (ideally approved) dependencies, but also quarantine suspicious releases and scan for known malware. But keep in mind that most scanners only detect known threats. Sophisticated attacks are novel by design. Proxy scanning is one layer, not a replacement for version pinning and controlled upgrades.

### Use Reachability-Aware Scanning

Not every CVE in your dependency tree matters. A vulnerability in a function you never call does not deserve the same urgency as one that is on your hot path. Go's [govulncheck](https://go.dev/doc/tutorial/govulncheck "Go Vulnerability Checking") traces your actual call graph and filters out findings in code your application never reaches. Other ecosystems are catching up. At a minimum, make sure your scanner can tell whether a vulnerable package is actually used. The best scanners go further and trace the call graph down to the specific vulnerable function.

### Reduce Dependency Surface Area

{{< quote source="Go Proverbs" url="https://go-proverbs.github.io/" >}}
A little copying is better than a little dependency.
{{< /quote >}}

Every package adds code, maintainers, credentials, infrastructure, and trust assumptions. Modern ecosystems normalize [absurd dependency depth](https://research.swtch.com/deps "Russ Cox: Our Software Dependency Problem"). Before adding a package, ask: can we write this in 30 lines? If yes, write it. A [coding agent]({{< ref "/tags/agentic-engineering/">}}) can do most of the work for you.

## Controlled Trust, Not Blind Trust

The lesson from 2025 and 2026 supply-chain attacks is not _"never update"_. Stale dependencies become liabilities too. The lesson is that **blind trust does not become safer just because it is automated**.

Secure software supply chains are built on controlled trust: Pinned versions. Enforced cooldowns. Verified provenance. Proxy repository managers. Reachability-aware scanning. A small dependency surface. The fastest update is not always the safest. Sometimes the safest thing to do is wait.
