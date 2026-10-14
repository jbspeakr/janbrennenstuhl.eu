---
id: jb-research-account-recovery
imageDecorative: true
title: "How secure are email-based password resets?"
linkTitle: "Account recovery"
description: "What a 2021 analysis of 366 websites found about email-based password reset flows, and which controls close the gaps."
answer: "Often not very: in a 2021 study of 366 websites from the Alexa Top 5K, 72% of account recovery mechanisms had at least one implementation weakness. Common gaps were multiple valid reset tokens, missing change notifications and long-lived reset links."
slug: account-recovery
date: 2023-04-21
lastmod: 2026-10-13
draft: false
image: account-recovery-password-reset.webp
weight: 100
topics: [identity-authentication]
claim: "72% of the website account recovery mechanisms studied had at least one implementation weakness."
changes:
  - date: 2026-10-13
    note: "Rewritten as a field-guide entry: question title, short answer, key findings and evidence table. Study summary kept and extended with the paper's measured results."
---

## Key findings

{{< finding id="recovery-72pct-weakness" source="Innocenti et al., You've Got (a Reset) Mail (DIMVA 2021)" url="https://kharraz.org/publications/dimva2021youvegotmail.pdf" >}}In a study of 366 popular websites, 72% of account recovery mechanisms had at least one implementation weakness.{{< /finding >}}

{{< finding id="recovery-40pct-multiple-tokens" source="Innocenti et al., You've Got (a Reset) Mail (DIMVA 2021)" url="https://kharraz.org/publications/dimva2021youvegotmail.pdf" >}}40% of the websites studied generated multiple valid password reset tokens at the same time.{{< /finding >}}

{{< finding id="recovery-45pct-no-notification" source="Innocenti et al., You've Got (a Reset) Mail (DIMVA 2021)" url="https://kharraz.org/publications/dimva2021youvegotmail.pdf" >}}45% of the websites studied did not notify the account owner after a password change, so an unauthorised reset went unnoticed.{{< /finding >}}

{{< finding id="recovery-13pct-owasp" source="Innocenti et al., You've Got (a Reset) Mail (DIMVA 2021)" url="https://kharraz.org/publications/dimva2021youvegotmail.pdf" >}}Only 13% of the websites studied followed the OWASP guidelines for password reset.{{< /finding >}}

## Evidence

{{< studies caption="Account recovery studies" >}}
{{< study title="You've Got (a Reset) Mail: A Security Analysis of Email-Based Password Reset Procedures" org="Northeastern University, University of Trento, KU Leuven, Florida International University" year="2021" sample="366 websites from the Alexa Top 5K" method="Manual registration and semi-automated checks against 8 OWASP-based controls" url="https://kharraz.org/publications/dimva2021youvegotmail.pdf" >}}72% had at least one weakness; only 13% followed the OWASP guidelines.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

The weaknesses Innocenti et al. measured map to concrete controls:

- Keep one valid reset token per account. Invalidate older tokens when a user requests a new one, and accept each token only once.
- Give reset links a short expiry. The study counted any link still valid after 24 hours as a weakness, and found that in 75 websites.
- Send reset links over HTTPS only. 52 websites sent tokens in insecure links.
- End existing sessions after a reset. 38% of the websites kept them alive.
- Protect the flow against login CSRF and header manipulation. Build reset links from configuration, not from the request's host header.

Treat recovery as a high-risk action that deserves the same scrutiny as login. [Step-up authentication]({{< ref "/post/stepup-authentication" >}}) shows how to require more proof for sensitive actions.

### For product and UX

- Notify the account owner after every password change, and include a way to report "this wasn't me".
- Keep the reset email plain and predictable, so users can spot a fake one.
- Recovery is also an account takeover path. The [account hijacking entry]({{< ref "/knowledge-base/account-security/account-hijacking" >}}) covers attacks that start before sign-up.

## The studies in detail

### Security Analysis of Email-Based Password Reset Procedures

An international group of researchers from the USA, Italy and Belgium analysed the email-based account recovery mechanisms of websites in the Alexa Top 5K. They manually registered accounts and triggered password recovery on sites from 3 popularity groups, ending up with 366 websites. They checked each site against 8 implementation controls derived from the OWASP guidelines.

The paper describes a heterogeneous reality. 72% of the websites had at least one weakness, and only 13% followed the OWASP guidelines. 40% generated multiple valid tokens, 45% sent no notification after a password change, and 22% were vulnerable to login CSRF. The authors also outline concrete password-recovery attacks that can lead to account takeover.

"We hope that this paper will pave the way in highlighting the importance of improving the email-based account recovery mechanisms in real-world websites."

[Read the paper (PDF)](https://kharraz.org/publications/dimva2021youvegotmail.pdf)

## Related

- [How do attackers take over accounts?]({{< ref "/knowledge-base/account-security/account-hijacking" >}})
- [Do login challenges and risk scoring stop account takeover?]({{< ref "/knowledge-base/account-security/reinforced-authentication" >}})
