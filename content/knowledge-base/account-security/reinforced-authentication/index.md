---
id: jb-research-reinforced-authentication
kind: research
status: published
reviewStatus: not-reviewed
topics: ['identity-authentication']
imageDecorative: true
title: "Reinforced Authentication Studies"
linkTitle: "Reinforced Authentication: Studies Redefine Account Security"
description: "Security research studies that discover the power of reinforced authentication methods like advanced login challenges and behavioral analysis."
lead: "In an era of escalating cyber threats, traditional username and password combinations are no longer sufficient to safeguard our online accounts. Enter reinforced authentication — a powerful approach that promises enhanced security and peace of mind. The following security research papers take a deep dive into reinforced authentication methods, such as advanced login challenges, the incorporation of side information, and behavioral analysis. Discover how these advanced techniques can fortify your digital defenses and thwart unauthorized access attempts. These studies will provide you with the knowledge and tools to strengthen your authentication and protect your users' accounts. Get ready to embark on a journey to more secure accounts."
slug: "reinforced-authentication-studies"
date: 2023-04-27
lastmod: 2023-04-27
draft: false
image: reinforced-authentication-methods.webp
type: docs
menu:
  knowledge-base:
    parent: "account-security"
    identifier: "reinforced-authentication"
weight: 150
toc: true

---

## Evaluating Login Challenges as a Defense Against Account Takeover

Google and the New York University teamed up to *"study the efficacy of login challenges at preventing account takeover"* and to *"evaluate the amount of friction these challenges create for normal users"*.

While it is interesting to see the various different classes of challenges they looked at (device-based, delegation-based, knowledge-based, and resource-based challenges), the conclusion is rather sobering:

*"Our results illustrate that login challenges act as an important barrier to hijacking, but that friction in the process leads to 52% of legitimate users failing to sign-in—though 97% of users eventually access their account in a short period."*

<b><a href="https://damonmccoy.com/papers/loginchallenges.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Using Guessed Passwords to Thwart Online Guessing

This paper from Microsoft Research and Carnegie Mellon University, aims to provide practitioners, who seek to defend password-protected resources from online guessing attacks, with a set of techniques to better balance friction and security:

*"Among our contributions are features to make better benign/attack traffic classification decisions. These include mechanisms to penalize fail events with commonly guessed passwords more, to protect accounts with weak passwords better, and to distinguish user-generated typos from other fails. We do all of these without storing any information which exposes accounts to new risk in the event of a server breach. These innovations allow much greater flexibility over the previous state-of-the-art, which treats all failures equally"*

<b><a href="https://www.microsoft.com/en-us/research/uploads/prod/2018/06/stopGuessingTR.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## A Statistical Approach to Measuring User Authenticity

Researchers from LinkedIn, Ruhr-Universität Bochum and Universita di Cagliari  have evaluated a statistical framework *"to strengthening password-based authentication by classifying login attempts into normal and suspicious activity based on parameters available during login."*

The approach was tested against real-life login data from LinkedIn as well as simulated attacks and showed a promising *"recall of up to 89% for a false-positive rate of 10%"*.

<b><a href="http://dx.doi.org/10.14722/ndss.2016.23240" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Distinguishing Attacks from Legitimate Traffic at an Authentication Server

In this paper, Microsoft researchers explore how to more effectively defend against breadth-first attacks that spread guesses very widely. They describe *"a simple robust procedure to estimate the ratio of bad-to-good traffic and show how this can be used to calculate the likelihood that any particular observation is indicative of malice."*

The authors conclude that their *"approach has the advantage over three strikes type lockout and variants that it has no dependence on arbitrary thresholds and we avoid base rate neglect. It has the advantages over machine learning schemes that it requires no labels, and does not assume stationarity of attack traffic."*

<b><a href="https://www.microsoft.com/en-us/research/uploads/prod/2018/06/distinguishingBotsFromLegit.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)