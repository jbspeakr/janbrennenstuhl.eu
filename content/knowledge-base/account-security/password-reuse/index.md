---
id: jb-research-password-reuse
imageDecorative: true
title: "How common is password reuse?"
linkTitle: "Password reuse"
description: "What 5 studies from 2007 to 2018 measured about password reuse, and what engineers and product teams can do about it."
answer: "Very common: one study estimates that 43-51% of users reuse the same password across sites, and an in situ study found exact or partial reuse in about 60% of unique passwords. An attacker who holds a user's password from one site can guess that user's password elsewhere far more easily."
slug: password-reuse
aliases: ["/knowledge-base/account-security/password-reuse-studies-security/"]
date: 2023-04-27
lastmod: 2026-10-13
draft: false
image: password-reuse-research.webp
weight: 110
topics: [passwords]
claim: "Somewhere between 43% and 51% of users reuse the same password across multiple sites."
changes:
  - date: 2026-10-13
    note: "Rewritten as a field-guide entry: question title, short answer, key findings and evidence table. Study summaries kept. Added sample sizes and numbers from the papers' own text and corrected the affiliations for The Tangled Web of Password Reuse."
---

## Key findings

{{< finding id="pw-reuse-43-51pct" source="Das et al., The Tangled Web of Password Reuse (NDSS 2014)" url="https://www.ndss-symposium.org/wp-content/uploads/2017/09/06_1_1.pdf" >}}An estimated 43-51% of users reuse the same password across multiple sites.{{< /finding >}}

{{< finding id="pw-reuse-cross-site-guessing" source="Das et al., The Tangled Web of Password Reuse (NDSS 2014)" url="https://www.ndss-symposium.org/wp-content/uploads/2017/09/06_1_1.pdf" >}}With a user's password from another site, a cross-site guessing algorithm guessed 30% of transformed passwords within 100 attempts, compared with 14% for a standard guessing algorithm.{{< /finding >}}

{{< finding id="pw-reuse-partial-60pct" source="Pearman et al., Let's Go in for a Closer Look: Observing Passwords in Their Natural Habitat (CCS 2017)" url="https://dl.acm.org/doi/pdf/10.1145/3133956.3133973" >}}When researchers observed 154 people's real logins for an average of 147 days, about 60% of their unique passwords were exactly or partially reused.{{< /finding >}}

{{< finding id="pw-reuse-frequent-entry" source="Wash et al., Understanding Password Choices (SOUPS 2016)" url="https://www.usenix.org/system/files/conference/soups2016/soups2016-paper-wash.pdf" >}}People reuse each password on 1.7-3.4 websites, and they mostly reuse the complex passwords they have to enter frequently.{{< /finding >}}

{{< finding id="pw-reuse-notifications-third" source="Golla et al., Designing Password-Reuse Notifications (CCS 2018)" url="https://dl.acm.org/doi/pdf/10.1145/3243734.3243767" >}}Fewer than a third of people shown a typical password-reuse notification said they intended to change any passwords.{{< /finding >}}

## Evidence

{{< studies caption="Password reuse studies" >}}
{{< study title="Let's Go in for a Closer Look: Observing Passwords in Their Natural Habitat" org="Carnegie Mellon University, ICSI, Google" year="2017" sample="154 participants, 147 days on average" method="In situ measurement on participants' computers" url="https://dl.acm.org/doi/pdf/10.1145/3133956.3133973" >}}About 60% of unique passwords were exactly or partially reused.{{< /study >}}
{{< study title="The Tangled Web of Password Reuse" org="University of Illinois, Princeton, Indiana University" year="2014" sample="Several hundred thousand leaked passwords from 11 sites; 224 survey responses" method="Leak analysis, survey, guessing experiment" url="https://www.ndss-symposium.org/wp-content/uploads/2017/09/06_1_1.pdf" >}}Estimated 43-51% of users reuse the same password across sites.{{< /study >}}
{{< study title="Understanding Password Choices: How Frequently Entered Passwords are Re-used Across Websites" org="Michigan State University, Macalester College" year="2016" sample="134 participants over 6 weeks" method="Survey combined with measured online behaviour" url="https://www.usenix.org/system/files/conference/soups2016/soups2016-paper-wash.pdf" >}}Each password is reused on 1.7-3.4 websites, mostly the frequently entered ones.{{< /study >}}
{{< study title="A Large-Scale Study of Web Password Habits" org="Microsoft Research" year="2007" sample="Over half a million users, 3 months" method="Client-side measurement" url="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/11/www2007.pdf" >}}The average user had 6.5 passwords, each shared across 3.9 sites.{{< /study >}}
{{< study title="Designing Password-Reuse Notifications" year="2018" sample="180 and 588 respondents" method="2 online user studies of notification designs" url="https://dl.acm.org/doi/pdf/10.1145/3243734.3243767" >}}Fewer than a third of respondents in study 1 intended to change any password.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

- Assume that some of your users' passwords are already in another site's breach. Check passwords against breach data at sign-up, password change and login. The [compromised credentials entry]({{< ref "/knowledge-base/account-security/compromised-credentials" >}}) covers protocols that do this without sending the password to a third party.
- Treat a correct password as one signal among several. Das et al. show that a leaked password from another site gives an online attacker a large head start, so rate limits alone aren't enough. See [reinforced authentication]({{< ref "/knowledge-base/account-security/reinforced-authentication" >}}) and [step-up authentication]({{< ref "/post/stepup-authentication" >}}).
- Make unique passwords cheap for users: allow paste, long passwords and autofill so a password manager works. I wrote about this in [password-manager-friendly login forms]({{< ref "/post/password-manager-friendly" >}}) and [long password support]({{< ref "/post/long-password-support" >}}).
- Where you can, offer a factor that can't be reused at all, such as passkeys. See my [critical notes on passkeys]({{< ref "/post/passkeys-controversy" >}}).

### For product and UX

- Composition rules can backfire. Wash et al. found that people memorise a strong password for a site they log into often and then reuse it elsewhere. Read [password policy]({{< ref "/post/password-policy" >}}) before adding another character-class rule.
- Don't rely on a notification alone. Golla et al. conclude that "notifications alone appear insufficient in solving password reuse". Pair the message with a forced reset and a clear next step, such as using a password manager.

## The studies in detail

### Observing Passwords in Their Natural Habitat

Researchers from Carnegie Mellon University, the International Computer Science Institute and Google instrumented the computers of 154 participants for an average of 147 days each. They wanted to analyse "password characteristics and behaviors across the full range of participants' web-based accounts".

Among other things, the data showed "that the use of symbols and digits in passwords predicts increased likelihood of reuse, while increased password strength predicts decreased likelihood of reuse; that password reuse is more prevalent than previously believed, especially when partial reuse is taken into account". Of 1,578 unique passwords, 32% were exactly reused and about 60% showed some form of reuse.

[Read the paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3133956.3133973)

### The Tangled Web of Password Reuse

This 2014 study by researchers from the University of Illinois, Princeton and Indiana University used several hundred thousand leaked passwords from 11 websites and a user survey with 224 responses. The authors estimate that "43-51% of users reuse the same password across multiple sites". They also identified "a few simple tricks users often employ to transform a basic password between sites" and built the first cross-site password-guessing algorithm.

That algorithm guessed 30% of transformed passwords within 100 attempts, compared with 14% without knowledge of the other site's password. A leaked password helps the attacker even when the user changed it slightly for the next site.

[Read the paper (PDF)](https://www.ndss-symposium.org/wp-content/uploads/2017/09/06_1_1.pdf)

### Understanding Password Choices: How Frequently Entered Passwords are Re-used Across Websites

Researchers from Michigan State University and Macalester College combined survey answers with the measured online behaviour of 134 participants over 6 weeks. They found "that people do tend to re-use each password on 1.7–3.4 different websites" and that "they reuse passwords that are more complex, and mostly they tend to re-use passwords that they have to enter frequently".

The most interesting observation is how accounts depend on each other, which shows the trouble with arbitrary password composition requirements:

> "[…] if users must memorize a strong password on a website where they have to enter it frequently, they then re-use it elsewhere. This results in stronger passwords on more websites. This practice puts users at greater risk of cross-site password guessing attacks […]"

[Read the paper (PDF)](https://www.usenix.org/system/files/conference/soups2016/soups2016-paper-wash.pdf)

### A Large-Scale Study of Web Password Habits

Microsoft researchers measured the password use and reuse of over half a million users over 3 months in 2007, using a client component on users' machines. It was the first large-scale study of its kind. The average user had 6.5 passwords, each shared across 3.9 different sites, and about 25 accounts that required a password. The authors write that the results "particularly confirm the conventional wisdom about the large number and poor quality of user passwords. In addition passwords are re-used and forgotten a great deal."

[Read the paper (PDF)](https://www.microsoft.com/en-us/research/wp-content/uploads/2006/11/www2007.pdf)

### Designing Password-Reuse Notifications

When companies find stolen credentials and notice password reuse, they may require a password reset and notify affected users. Researchers from Germany and the USA ran 2 user studies in 2018 to learn how people react to such notifications. In the first, 180 respondents each saw 1 of 6 notifications that real companies had used, and fewer than a third reported an intention to change any passwords. In the second, 588 respondents saw 1 of 15 variations of a model notification. The authors discuss "best practices for password-reuse notifications and how notifications alone appear insufficient in solving password reuse".

I recommend the paper to anyone who has to balance account security and usability.

[Read the paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3243734.3243767)

## Related

- [How do you protect accounts from stolen credentials?]({{< ref "/knowledge-base/account-security/compromised-credentials" >}})
- [Do password strength meters work?]({{< ref "/knowledge-base/account-security/password-policy" >}})
- [Password spraying]({{< ref "/post/password-spraying" >}})
- [How long a password should be allowed to be]({{< ref "/post/password-length-recommendation" >}})
