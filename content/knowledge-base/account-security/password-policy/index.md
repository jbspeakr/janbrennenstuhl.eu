---
id: jb-research-password-policy
imageDecorative: true
title: "Do password strength meters work?"
linkTitle: "Password strength meters"
description: "When password strength meters change behavior, why many deployed meters mislead, and how to build a meter and policy that help."
answer: "Meters work under the right conditions. In one study they produced stronger passwords when people changed passwords on important accounts, and made no observable difference for an unimportant one. Many deployed meters also label weak passwords as strong, so a useful meter has to estimate how guessable a password really is."
date: 2023-05-03
lastmod: 2026-10-13
draft: false
image: password-strength-meter-illustration.webp
weight: 115
slug: password-strength-meter
topics: [passwords]
claim: "Password strength meters produce stronger passwords when users change passwords on important accounts, but make no observable difference on unimportant ones."
changes:
  - date: 2026-10-13
    note: "Rewritten as a field-guide entry: question title, short answer, key findings and evidence table. Study summaries kept. Corrected the summary of the meter experiment and the zxcvbn guess count (10^5, not 105)."
---

## Key findings

{{< finding id="meter-important-accounts" source="Egelman et al., Does My Password Go up to Eleven? (CHI 2013)" url="https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/chi13b.pdf" >}}Password meters produced significantly stronger passwords when people had to change their real passwords on important accounts.{{< /finding >}}

{{< finding id="meter-unimportant-no-effect" source="Egelman et al., Does My Password Go up to Eleven? (CHI 2013)" url="https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/chi13b.pdf" >}}When people created a password for an unimportant account, meters made no observable difference because they reused weak passwords from similar low-risk accounts.{{< /finding >}}

{{< finding id="meter-inconsistent-labels" source="de Carné de Carnavalet and Mannan, From Very Weak to Very Strong: Analyzing Password-Strength Meters (NDSS 2014)" url="https://xavier2dc.fr/papers/password-meters-ndss2014.pdf" >}}Password meters at popular web services gave highly inconsistent ratings for the same password and labeled many weak passwords as strong or even very strong.{{< /finding >}}

{{< finding id="meter-zxcvbn-1-5mb" source="Wheeler, zxcvbn: Low-Budget Password Strength Estimation (USENIX Security 2016)" url="https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_wheeler.pdf" >}}A strength estimator with 1.5 MB of compressed data can accurately estimate the best-known guessing attacks up to 10^5 guesses.{{< /finding >}}

{{< finding id="meter-policy-strength-length" source="Tan et al., Practical Recommendations for Stronger, More Usable Passwords (CCS 2020)" url="https://dl.acm.org/doi/pdf/10.1145/3372297.3417882" >}}Researchers recommend combining minimum-strength and minimum-length password requirements for high-value accounts, and found that adding blocklists provides no further gains.{{< /finding >}}

## Evidence

{{< studies caption="Password strength meter studies" >}}
{{< study title="Does My Password Go up to Eleven? The Impact of Password Meters on Password Selection" org="UC Berkeley, University of British Columbia, Microsoft Research" year="2013" sample="47 lab participants; 541 field participants" method="Laboratory experiment with real password changes, field experiment" url="https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/chi13b.pdf" >}}Meters helped on important accounts and made no observable difference on an unimportant one.{{< /study >}}
{{< study title="From Very Weak to Very Strong: Analyzing Password-Strength Meters" org="Concordia University" year="2014" sample="13 meters from 11 web services; nearly 4 million passwords" method="Black-box testing with password dictionaries" url="https://xavier2dc.fr/papers/password-meters-ndss2014.pdf" >}}Meters disagree with each other and rate many weak passwords as strong.{{< /study >}}
{{< study title="zxcvbn: Low-Budget Password Strength Estimation" org="Dropbox" year="2016" sample="Leaked password sets" method="Comparison against 4 modern guessing attacks" url="https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_wheeler.pdf" >}}1.5 MB is enough to estimate guessing attacks accurately up to 10^5 guesses.{{< /study >}}
{{< study title="Fast, Lean, and Accurate: Modeling Password Guessability Using Neural Networks" org="Carnegie Mellon University" year="2016" sample="n/a" method="Neural network guessing models, client-side JavaScript implementation" url="https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_melicher.pdf" >}}Neural networks often guess passwords better than earlier models and compress to hundreds of kilobytes.{{< /study >}}
{{< study title="Practical Recommendations for Stronger, More Usable Passwords" org="Carnegie Mellon University" year="2020" sample="n/a" method="2 online experiments" url="https://dl.acm.org/doi/pdf/10.1145/3372297.3417882" >}}Combine minimum-strength and minimum-length requirements; blocklists add no further gains.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

- Estimate strength from guessability, using a model such as zxcvbn or a neural network, and stop counting character classes. Wheeler calls counts of lower- and uppercase letters, digits and symbols "a conclusively burdensome and ineffective security practice".
- For high-value accounts, combine a minimum length with a minimum-strength check. Tan et al. found that character-class requirements may provide very little improvement against expert attackers "and may even reduce effective security".
- Allow long passwords and passphrases so the strength check has something to reward. See [password length]({{< ref "/post/password-length-recommendation" >}}) and [long password support]({{< ref "/post/long-password-support" >}}).

### For product and UX

- Never show "strong" for a weak password. de Carné de Carnavalet and Mannan conclude that meters "should avoid providing misleading strength outcomes, especially for weak passwords".
- Give advice people can act on, not only a coloured bar. Melicher et al. name "giving user-interpretable advice to improve passwords during password creation" as the remaining challenge.
- Put effort into meters where they matter: password changes on important accounts. On throwaway sign-ups, a meter won't stop people from reusing a weak password. My [password policy guide]({{< ref "/post/password-policy" >}}) covers the rest of the policy.

## The studies in detail

### Impact of Password Meters on Password Selection

Researchers from UC Berkeley, the University of British Columbia and Microsoft Research performed "a laboratory experiment to examine whether [password] meters influenced users' password selections when they were forced to change their real passwords". The 47 participants didn't know that their passwords were the subject of the study, and the meters yielded significantly stronger passwords.

A follow-up field experiment with 541 participants tested a different scenario: creating a password for an unimportant account. There the meters made no observable difference, as participants simply reused weak passwords from similar low-risk accounts. The authors conclude that meters help "when users are forced to change existing passwords on 'important' accounts" and that individual meter design decisions likely have a marginal impact.

[Read the paper (PDF)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/chi13b.pdf)

### Analyzing Password-Strength Meters

Researchers from Concordia University tested 13 password meters from 11 popular web services, including Google, Yahoo! and PayPal, with nearly 4 million passwords from password dictionaries. They found highly inconsistent ratings for the same password across meters and many weak passwords labeled as strong or very strong. The study is from 2014, but I still see most of these problems on live sites. The authors argue that meter design deserves real expertise and research, and that, at least, "the current meters should avoid providing misleading strength outcomes, especially for weak passwords."

[Read the paper (PDF)](https://xavier2dc.fr/papers/password-meters-ndss2014.pdf)

### Low-Budget Password Strength Estimation

In this reference paper for the zxcvbn strength estimator from Dropbox, Daniel Lowe Wheeler shows that 1.5 MB of compressed storage is enough to accurately estimate the best-known guessing attacks up to 10^5 guesses. With 245 kB and 29 kB, zxcvbn covers 10^4 and 10^3 guesses respectively. The paper compares the estimator against 4 modern guessing attacks and presents it as a better replacement for composition requirements.

[Read the paper (PDF)](https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_wheeler.pdf)

### Modeling Password Guessability Using Neural Networks

In 2016, researchers from Carnegie Mellon University showed that artificial neural networks can often guess passwords more effectively than probabilistic context-free grammars and Markov models. The networks can be compressed to as little as hundreds of kilobytes without substantially worsening guessing effectiveness. With this result, the authors built the first principled client-side model of password guessing in JavaScript.

> "While we measured client-side strength metrics based on guessing effectiveness, a remaining challenge is giving user-interpretable advice to improve passwords during password creation."

[Read the paper (PDF)](https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_melicher.pdf)

### Practical Recommendations for Stronger, More Usable Passwords

In their 2020 study, Carnegie Mellon University researchers ran 2 online experiments and formulated "concrete recommendations for policy configurations that produce a good balance of security and usability". They give clear guidance on composition requirements, blocklists, and minimum-strength requirements driven by neural-network strength estimates.

> "We recommend a 1c12+NN10 minimum-strength policy for organizations that wish to protect high-value accounts without a substantial negative usability impact."

In plain terms, the recommended policy requires at least 12 characters and a password that passes the neural-network strength check. I consider this paper one of the most comprehensive and influential collections of best practices for password policies.

[Read the paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3372297.3417882)

## Related

- [How common is password reuse?]({{< ref "/knowledge-base/account-security/password-reuse" >}})
- [How do you protect accounts from stolen credentials?]({{< ref "/knowledge-base/account-security/compromised-credentials" >}})
- [Password-manager-friendly login forms]({{< ref "/post/password-manager-friendly" >}})
