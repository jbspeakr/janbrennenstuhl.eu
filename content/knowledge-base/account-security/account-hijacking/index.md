---
id: jb-research-account-hijacking
imageDecorative: true
title: "How do attackers take over accounts?"
linkTitle: "Account hijacking"
description: "What 2 studies found about account pre-hijacking at sign-up and the hack-for-hire market, and how to defend against both."
answer: "Some attackers prepare an account before the victim even signs up: at least 35 of 75 popular services studied were vulnerable to such pre-hijacking. Others are paid to break into a specific account and mostly use tailored phishing that can get past SMS two-factor authentication."
date: 2023-04-21
lastmod: 2026-10-13
draft: false
image: account-hijacking-attacks.webp
weight: 90
slug: account-takeover
aliases: ["/knowledge-base/account-security/account-hijacking-attacks/"]
topics: [identity-authentication, application-security]
claim: "At least 35 of 75 popular online services studied were vulnerable to account pre-hijacking attacks."
changes:
  - date: 2026-10-13
    note: "Rewritten as a field-guide entry: question title, short answer, key findings and evidence table. Study summaries kept and extended with numbers from the papers."
---

## Key findings

{{< finding id="hijack-prehijack-35-of-75" source="Sudhodanan and Paverd, Pre-hijacked accounts (USENIX Security 2022)" url="https://arxiv.org/pdf/2205.10174.pdf" >}}At least 35 of 75 popular online services were vulnerable to one or more account pre-hijacking attacks.{{< /finding >}}

{{< finding id="hijack-prehijack-email-only" source="Sudhodanan and Paverd, Pre-hijacked accounts (USENIX Security 2022)" url="https://arxiv.org/pdf/2205.10174.pdf" >}}In an account pre-hijacking attack, an attacker who knows only the victim's email address acts before the victim creates an account and gains access after the victim has signed up.{{< /finding >}}

{{< finding id="hijack-hire-5-of-27" source="Mirian et al., Hack for Hire (WWW 2019)" url="https://dl.acm.org/doi/pdf/10.1145/3308558.3313489" >}}Of 27 hack-for-hire services that researchers approached as buyers, only 5 succeeded in attacking the email accounts of the test identities.{{< /finding >}}

{{< finding id="hijack-hire-phishing-sms-2fa" source="Mirian et al., Hack for Hire (WWW 2019)" url="https://dl.acm.org/doi/pdf/10.1145/3308558.3313489" >}}Hack-for-hire attackers relied mainly on tailored phishing messages that were sophisticated enough to bypass SMS two-factor authentication.{{< /finding >}}

## Evidence

{{< studies caption="Account hijacking studies" >}}
{{< study title="Pre-hijacked accounts: An Empirical Study of Security Failures in User Account Creation on the Web" org="Independent researcher, Microsoft Security Response Center" year="2022" sample="75 popular online services" method="Attack design and testing against live services" url="https://arxiv.org/pdf/2205.10174.pdf" >}}At least 35 services were vulnerable to one or more of 5 pre-hijacking attacks.{{< /study >}}
{{< study title="Hack for Hire: Exploring the Emerging Market for Account Hijacking" org="UC San Diego, Google" year="2019" sample="27 English, Russian and Chinese hack-for-hire services" method="Posing as buyers against synthetic victim identities" url="https://dl.acm.org/doi/pdf/10.1145/3308558.3313489" >}}5 services succeeded, mostly through tailored phishing.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

- Don't let anyone use an account before they have proven they control its identifier. Verify the email address before the account becomes usable, and before you merge a password account with a federated login for the same address.
- Only trust email addresses from identity providers that verify them. One of the 5 attacks relies on a non-verifying identity provider.
- End all sessions and expire pending email-change links when the password is reset or the email address changes. Two of the attacks rely on unexpired sessions and email changes.
- Offer phishing-resistant factors. The hack-for-hire services got past SMS codes with phishing. See [passwordless authentication]({{< ref "/post/passwordless-authentication" >}}) and my [critical notes on passkeys]({{< ref "/post/passkeys-controversy" >}}).

### For product and UX

- Show users which sign-in methods are linked to their account, and notify them when one is added.
- When someone signs up with an address that already has a pending or unverified account, guide them through verification instead of silently signing them in.
- Recovery flows are another takeover path. The [account recovery entry]({{< ref "/knowledge-base/account-security/account-recovery" >}}) lists the common weaknesses.

## The studies in detail

### Account Pre-Hijacking Attacks: Security Failures in User Account Creation

"The ubiquity of user accounts in websites and online services makes account hijacking a serious security concern. Although previous research has studied various techniques through which an attacker can gain access to a victim's account, relatively little attention has been directed towards the process of account creation."

In this study, Avinash Sudhodanan and Andrew Paverd show that there is a whole class of **account pre-hijacking attacks**. The key point: "The distinctive feature of these attacks is that the attacker performs some action before the victim creates an account, which makes it trivial for the attacker to gain access after the victim has created/recovered the account."

The authors assume a realistic attacker who knows only the victim's email address. They describe 5 attacks: Classic-Federated Merge, Unexpired Session, Trojan Identifier, Unexpired Email Change and Non-verifying IdP. Of 75 popular services they analysed, at least 35 were vulnerable to one or more of them. Some attacks were completely undetectable from the victim's point of view. The paper closes with security requirements that prevent these vulnerabilities.

[Read the paper (PDF)](https://arxiv.org/pdf/2205.10174.pdf)

### Hack for Hire: Exploring the Emerging Market for Account Hijacking

In this paper, researchers from UC San Diego and Google "study a segment of targeted attackers known as 'hack for hire' services to understand the playbook that attackers use to gain access to victim accounts."

Posing as buyers, they contacted 27 English, Russian and Chinese black-market services, and only 5 succeeded in attacking the synthetic but realistic identities the researchers controlled. The attackers mostly used tailored phishing that could bypass SMS two-factor authentication. The authors also observed low volume, poor customer service and multiple scammers in this market. The paper is a good read if you want to understand the commercial account hijacking ecosystem and the techniques criminals use.

[Read the paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3308558.3313489)

## Related

- [How secure are email-based password resets?]({{< ref "/knowledge-base/account-security/account-recovery" >}})
- [Do login challenges and risk scoring stop account takeover?]({{< ref "/knowledge-base/account-security/reinforced-authentication" >}})
- [Where do OpenID Connect implementations break?]({{< ref "/knowledge-base/oidc/oidc-security" >}})
