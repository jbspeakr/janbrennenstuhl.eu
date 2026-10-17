---
id: jb-research-compromised-credentials
imageDecorative: true
title: "How do you protect accounts from stolen credentials?"
linkTitle: "Compromised credentials"
description: "What 3 studies found about breached credentials, credential stuffing and privacy-preserving breach checks, and how to apply it."
answer: "Check usernames and passwords against breach data with a privacy-preserving protocol, and add risk signals such as known devices and locations to the login decision. Breached credentials show up in about 1.5% of logins on the web, and in one study 7-25% of exposed passwords matched the victim's Google account."
slug: credential-stuffing
aliases: ["/knowledge-base/account-security/compromised-credentials-stuffing/"]
date: 2023-04-21
lastmod: 2026-10-13
draft: false
image: compromised-credentials-credential-stuffing.webp
weight: 100
topics: [passwords, application-security]
claim: "Checking credentials against breach data and adding device and location risk signals to the login decision reduce the risk from stolen passwords."
changes:
  - date: 2026-10-13
    note: "Rewritten as a field-guide entry: question title, short answer, key findings and evidence table. Study summaries kept. Replaced the broken link to the password breach alerting paper with the USENIX copy."
---

## Key findings

{{< finding id="cred-breached-logins-1-5pct" source="Thomas et al., Protecting accounts from credential stuffing with password breach alerting (USENIX Security 2019)" url="https://www.usenix.org/system/files/sec19-thomas.pdf" >}}Telemetry from nearly 670,000 users and 21 million logins showed that 1.5% of logins on the web involve breached credentials.{{< /finding >}}

{{< finding id="cred-alert-26pct-new-password" source="Thomas et al., Protecting accounts from credential stuffing with password breach alerting (USENIX Security 2019)" url="https://www.usenix.org/system/files/sec19-thomas.pdf" >}}26% of breach warnings shown at login led users to switch to a new password at least as strong as the original.{{< /finding >}}

{{< finding id="cred-google-match-7-25pct" source="Thomas et al., Data Breaches, Phishing, or Malware? (CCS 2017)" url="https://dl.acm.org/doi/pdf/10.1145/3133956.3134067" >}}Between 7% and 25% of passwords exposed through breaches, phishing kits and keyloggers matched the victim's Google account.{{< /finding >}}

{{< finding id="cred-hash-prefix-12x" source="Li et al., Protocols for Checking Compromised Credentials (CCS 2019)" url="https://rist.tech.cornell.edu/papers/c3.pdf" >}}In some contexts, the hash prefixes that common breach-checking services receive make remote guessing attacks 12 times more effective.{{< /finding >}}

## Evidence

{{< studies caption="Compromised credential studies" >}}
{{< study title="Protocols for Checking Compromised Credentials" org="Cornell Tech, Cloudflare" year="2019" sample="Existing C3 services (HaveIBeenPwned, Google Password Checkup)" method="Formal analysis, leakage simulation, protocol design" url="https://rist.tech.cornell.edu/papers/c3.pdf" >}}Hash-prefix leakage can make guessing 12 times more effective; 2 stronger protocols remain practical.{{< /study >}}
{{< study title="Protecting accounts from credential stuffing with password breach alerting" org="Google, Stanford" year="2019" sample="Over 4 billion breached credentials; nearly 670,000 users and 21 million logins" method="Protocol design, Chrome extension telemetry" url="https://www.usenix.org/system/files/sec19-thomas.pdf" >}}1.5% of logins involve breached credentials; 26% of warnings led to a new password.{{< /study >}}
{{< study title="Data Breaches, Phishing, or Malware? Understanding the Risks of Stolen Credentials" org="Google, UC Berkeley, ICSI" year="2017" sample="1.9 billion breached credentials, 12.4 million phishing and 788,000 keylogger victims" method="Longitudinal measurement, March 2016 to March 2017" url="https://dl.acm.org/doi/pdf/10.1145/3133956.3134067" >}}7-25% of exposed passwords matched the victim's Google account.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

- Check credentials against breach data at sign-up, password change and login. Use a protocol that never sends the password or its full hash to the checking service. Thomas et al. combine "computationally expensive hashing, k-anonymity, and private set intersection"; Li et al. show that a plain hash prefix leaks more than most teams assume.
- Don't decide a login on the password alone. Thomas et al. (2017) show that risk signals such as a user's historical geolocations and device profiles reduce the hijacking risk from stolen passwords. The [reinforced authentication entry]({{< ref "/knowledge-base/account-security/reinforced-authentication" >}}) collects studies on login risk scoring.
- Watch for stuffing and spraying patterns across accounts, not only per account. See [password spraying]({{< ref "/post/password-spraying" >}}) and [honeytokens]({{< ref "/post/honeytoken" >}}) for detection ideas.

### For product and UX

- Tell users when their credentials appear in a breach, and make the next step a single action. In the Google study, 26% of warnings led to a new password that was at least as strong.
- Expect most users not to act on a warning alone. The [password reuse entry]({{< ref "/knowledge-base/account-security/password-reuse" >}}) covers what makes a notification work and where notifications fall short.

## The studies in detail

### Protocols for Checking Compromised Credentials

"To prevent credential stuffing attacks, industry best practice now proactively checks if user credentials are present in known data breaches."

For this paper, researchers from Cornell Tech and Cloudflare analysed existing compromised credential checking (C3) services such as HaveIBeenPwned and Google Password Checkup. They give the first formal description of C3 services, including operational requirements and threat models. Current services have the client share a short prefix of a password hash. The authors show that in some contexts this prefix makes remote guessing 12 times more effective. They then propose "two new protocols that provide stronger protection for users' passwords", implement them, and show that they remain practical to deploy.

[Read the paper (PDF)](https://rist.tech.cornell.edu/papers/c3.pdf)

### Protecting accounts from credential stuffing with password breach alerting

Researchers from Google and Stanford describe how Google's password breach alerting works under the hood, which constraints and hard requirements it meets, and which cryptographic protocols it uses. Their cloud service covered over 4 billion breached credentials, and a Chrome extension served as the first client.

> "Our protocol relies on a combination of computationally expensive hashing, k-anonymity, and private set intersection. Our approach improves on existing protocols by taking into account both an adversarial client and server, while also minimizing the chance of false positives."

Anonymous telemetry from nearly 670,000 users and 21 million logins showed that 1.5% of logins on the web involved breached credentials. 26% of the warnings led users to migrate to a new password at least as strong as the original.

[Read the paper (PDF)](https://www.usenix.org/system/files/sec19-thomas.pdf)

### Data Breaches, Phishing, or Malware? Understanding the Risks of Stolen Credentials

Between March 2016 and March 2017, researchers from Google, UC Berkeley and the International Computer Science Institute identified 788,000 potential keylogger victims, 12.4 million potential phishing kit victims and 1.9 billion usernames and passwords exposed in data breaches. With this data, they "explore to what degree the stolen passwords […] enable an attacker to obtain a victim's valid email credentials — and thus complete control of their online identity due to transitive trust". In their case study of Google accounts, 7-25% of exposed passwords matched the victim's Google account.

The study is from 2017, but its mitigation still applies today: the authors show that adding risk signals, such as a user's historical geolocations and device profiles, to authentication helps mitigate hijacking with a correct but stolen password.

[Read the paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3133956.3134067)

## Related

- [How common is password reuse?]({{< ref "/knowledge-base/account-security/password-reuse" >}})
- [Do login challenges and risk scoring stop account takeover?]({{< ref "/knowledge-base/account-security/reinforced-authentication" >}})
- [Step-up authentication]({{< ref "/post/stepup-authentication" >}})
