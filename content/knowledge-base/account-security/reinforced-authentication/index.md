---
id: jb-research-reinforced-authentication
imageDecorative: true
title: "Do login challenges and risk scoring stop account takeover?"
linkTitle: "Reinforced authentication"
description: "What 4 studies found about login challenges, login risk scoring and defences against online password guessing."
answer: "They are an important barrier if you pick the right challenge: device-based challenges blocked over 94% of phishing-rooted hijacking attempts at Google, while knowledge-based challenges stopped as few as 10%. The cost is friction, as 52% of legitimate users who got a challenge failed to sign in at first."
slug: "reinforced-authentication-studies"
date: 2023-04-27
lastmod: 2026-10-13
draft: false
image: reinforced-authentication-methods.webp
weight: 150
topics: [identity-authentication]
claim: "Device-based login challenges block far more account takeover attempts than knowledge-based ones."
changes:
  - date: 2026-10-13
    note: "Rewritten as a field-guide entry: question title, short answer, key findings and evidence table. Study summaries kept and extended with numbers from the papers."
---

## Key findings

{{< finding id="login-device-challenge-94pct" source="Doerfler et al., Evaluating Login Challenges as a Defense Against Account Takeover (WWW 2019)" url="https://damonmccoy.com/papers/loginchallenges.pdf" >}}Device-based login challenges blocked over 94% of hijacking attempts rooted in phishing and 100% of automated hijacking attempts.{{< /finding >}}

{{< finding id="login-knowledge-challenge-10pct" source="Doerfler et al., Evaluating Login Challenges as a Defense Against Account Takeover (WWW 2019)" url="https://damonmccoy.com/papers/loginchallenges.pdf" >}}Knowledge-based login challenges prevented as few as 10% of hijacking attempts rooted in phishing.{{< /finding >}}

{{< finding id="login-challenge-friction-52pct" source="Doerfler et al., Evaluating Login Challenges as a Defense Against Account Takeover (WWW 2019)" url="https://damonmccoy.com/papers/loginchallenges.pdf" >}}Login challenges caused 52% of legitimate users to fail to sign in, although 97% got into their account within a short period.{{< /finding >}}

{{< finding id="login-risk-score-recall-89pct" source="Freeman et al., Who Are You? A Statistical Approach to Measuring User Authenticity (NDSS 2016)" url="https://www.ndss-symposium.org/wp-content/uploads/2017/09/who-are-you-statistical-approach-measuring-user-authenticity.pdf" >}}A statistical login classifier using IP and user-agent history reached a recall of up to 89% at a 10% false-positive rate on LinkedIn login data.{{< /finding >}}

{{< finding id="login-protect-frequent-guesses" source="Tian, Herley and Schechter, StopGuessing: Using Guessed Passwords to Thwart Online Guessing" url="https://www.microsoft.com/en-us/research/uploads/prod/2018/06/stopGuessingTR.pdf" >}}If you can implement only one defence against online guessing, protect users whose passwords attackers guess frequently more aggressively than others.{{< /finding >}}

## Evidence

{{< studies caption="Reinforced authentication studies" >}}
{{< study title="Evaluating Login Challenges as a Defense Against Account Takeover" org="Google, New York University" year="2019" sample="Over 350,000 hijacking attempts; 1.2 million legitimate users" method="Case study of 14 challenge types at Google" url="https://damonmccoy.com/papers/loginchallenges.pdf" >}}Device-based challenges work best; 52% of legitimate users failed at first.{{< /study >}}
{{< study title="StopGuessing: Using Guessed Passwords to Thwart Online Guessing" org="Carnegie Mellon University, Microsoft Research" year="n/a" sample="n/a" method="Open-source implementation and attack simulations" url="https://www.microsoft.com/en-us/research/uploads/prod/2018/06/stopGuessingTR.pdf" >}}Penalise failures with frequently guessed passwords and forgive typos.{{< /study >}}
{{< study title="Who Are You? A Statistical Approach to Measuring User Authenticity" org="LinkedIn, Ruhr-Universität Bochum, Università di Cagliari" year="2016" sample="LinkedIn login data and simulated attacks" method="Statistical classifier, prototype evaluation" url="https://www.ndss-symposium.org/wp-content/uploads/2017/09/who-are-you-statistical-approach-measuring-user-authenticity.pdf" >}}Recall of up to 89% at a 10% false-positive rate.{{< /study >}}
{{< study title="Distinguishing Attacks from Legitimate Traffic at an Authentication Server" org="Microsoft Research" year="n/a" sample="n/a" method="Statistical estimation with sensitivity analysis" url="https://www.microsoft.com/en-us/research/uploads/prod/2018/06/distinguishingBotsFromLegit.pdf" >}}Estimating the bad-to-good traffic ratio avoids fixed lockout thresholds.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

- Score every login on signals the user doesn't type, such as IP address history, device and browser. Freeman et al. reached a recall of up to 89% using IP and user-agent history.
- Prefer device-based challenges, such as a prompt on a known device, over knowledge questions. Doerfler et al. measured a large gap between the two. My essay on [step-up authentication]({{< ref "/post/stepup-authentication" >}}) shows how to request a stronger factor only when the risk justifies it.
- Count failed logins by how likely they are to be an attack. Penalise failures with frequently guessed passwords, protect accounts with weak passwords harder, and be lenient with typos. Tian et al. do this without storing anything that would expose accounts if leaked.
- Breadth-first guessing spreads attempts thinly over many accounts, so per-account lockouts don't see it. Herley and Schechter estimate the share of attack traffic instead of relying on fixed thresholds. See [password spraying]({{< ref "/post/password-spraying" >}}) and [honeytokens]({{< ref "/post/honeytoken" >}}) for related detection.

### For product and UX

- Budget for friction. A challenge that half of your legitimate users fail at first needs a clear path back in, or it turns into support tickets and lost users.
- Challenge only suspicious logins, so most users never see a challenge. The 2 risk-scoring studies above show how to pick them out.

## The studies in detail

### Evaluating Login Challenges as a Defense Against Account Takeover

Google and New York University teamed up to "study the efficacy of login challenges at preventing account takeover" and to "evaluate the amount of friction these challenges create for normal users". Using Google as a case study, they evaluated 14 device-based, delegation-based, knowledge-based and resource-based challenges against over 350,000 real-world hijacking attempts, and measured usability on a sample of 1.2 million legitimate users.

Device-based challenges blocked over 94% of phishing-rooted attempts and all automated ones. Knowledge-based challenges stopped as few as 10% of phishing-rooted attempts and 73% of automated ones. The conclusion is sobering:

> "Our results illustrate that login challenges act as an important barrier to hijacking, but that friction in the process leads to 52% of legitimate users failing to sign-in—though 97% of users eventually access their account in a short period."

[Read the paper (PDF)](https://damonmccoy.com/papers/loginchallenges.pdf)

### Using Guessed Passwords to Thwart Online Guessing

This paper from Microsoft Research and Carnegie Mellon University gives practitioners who defend password-protected resources against online guessing a set of techniques to better balance friction and security:

> "Among our contributions are features to make better benign/attack traffic classification decisions. These include mechanisms to penalize fail events with commonly guessed passwords more, to protect accounts with weak passwords better, and to distinguish user-generated typos from other fails. We do all of these without storing any information which exposes accounts to new risk in the event of a server breach. These innovations allow much greater flexibility over the previous state-of-the-art, which treats all failures equally"

The authors publish an open-source implementation and a guessing-attack simulator. If practitioners can implement only one of the techniques, they recommend protecting users who rely on frequently guessed passwords more aggressively.

[Read the paper (PDF)](https://www.microsoft.com/en-us/research/uploads/prod/2018/06/stopGuessingTR.pdf)

### A Statistical Approach to Measuring User Authenticity

Researchers from LinkedIn, Ruhr-Universität Bochum and Università di Cagliari evaluated a statistical framework for "strengthening password-based authentication by classifying login attempts into normal and suspicious activity based on parameters available during login". Suspicious attempts can then get an extra verification step, such as a phone-based one.

They tested the approach on real-life login data from LinkedIn and on simulated attacks. Using the user's IP history and user-agent history, it showed a "recall of up to 89% for a false-positive rate of 10%".

[Read the paper (PDF)](https://www.ndss-symposium.org/wp-content/uploads/2017/09/who-are-you-statistical-approach-measuring-user-authenticity.pdf)

### Distinguishing Attacks from Legitimate Traffic at an Authentication Server

In this paper, Microsoft researchers look at how to defend against breadth-first attacks that spread guesses very widely. Lockout rules such as "three strikes" work against attacks on one account, but at large providers breadth-first attacks can send millions of guesses without triggering them. The authors describe "a simple robust procedure to estimate the ratio of bad-to-good traffic and show how this can be used to calculate the likelihood that any particular observation is indicative of malice."

They conclude that their "approach has the advantage over three strikes type lockout and variants that it has no dependence on arbitrary thresholds and we avoid base rate neglect. It has the advantages over machine learning schemes that it requires no labels, and does not assume stationarity of attack traffic."

[Read the paper (PDF)](https://www.microsoft.com/en-us/research/uploads/prod/2018/06/distinguishingBotsFromLegit.pdf)

## Related

- [How do you protect accounts from stolen credentials?]({{< ref "/knowledge-base/account-security/compromised-credentials" >}})
- [How do attackers take over accounts?]({{< ref "/knowledge-base/account-security/account-hijacking" >}})
- [How common is password reuse?]({{< ref "/knowledge-base/account-security/password-reuse" >}})
