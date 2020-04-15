---
title: "Password Strength Meter Studies"
linkTitle: "Protect Your Accounts: 5 Studies on Password Strength Meters"
description: "Worried about weak passwords? Check out the latest research on Password Strength Meters to keep your accounts secure! Click here to learn more."
lead: ""
date: 2023-05-03
lastmod: 2023-05-03
draft: false
image: password-strength-meter-illustration.webp
type: docs
menu:
  knowledge-base:
    parent: "account-security"
    identifier: "password-policy"
weight: 115
toc: true
slug: password-strength-meter
---

## Impact of Password Meters on Password Selection

Researchers from Berkeley, Vancouver and Microsoft performed *"a laboratory experiment to examine whether [password] meters influenced users’ password selections when they were forced to change their real passwords"*. 

Unsurprisingly, these meters only make a difference *"when users are forced to change existing passwords"*. Pure visual indicators seem to have no significant effect.

<b><a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/chi13b.pdf" role="button">→ Read the Paper</a></b> (.pdf)

## Analyzing Password-Strength Meters

Researchers from Concordia University analyzed the weaknesses and inconsistencies of password-strength meters employed by selected popular websites. While the study was published already in 2014, most of the finding can still today be observed in the open wild. The authors conclude that designing password strength indicators deserves thorough expertise, research and dedication: Password-strength *"meters should avoid providing misleading strength outcomes, especially for weak passwords."*  

<b><a href="https://madiba.encs.concordia.ca/~x_decarn/papers/password-meters-ndss2014.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Low-Budget Password Strength Estimation

In this reference paper for the popular zxcvbn framework by Dropbox, Daniel Lowe Wheeler outlines why *"1.5 MB of compressed storage is sufficient to accurately estimate the best-known guessing attacks up to 105 guesses"*. The paper not only demonstrated how their approach compares against the best guessing attacks, but also advertises it as a smarter way to solve password composition requirements. A great addition for every strength meter!

<b><a href="https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_wheeler.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Modeling Password Guessability Using Neural Networks

In 2016, researchers from Carnegie Mellon University presented that artificial neural networks can often guess passwords more effectively while also being compressable without worsening guessing effectiveness. As a result they came up with an approach to measure password strength based on guessability in client Javascript code.

*"While we measured client-side strength metrics based on guessing effectiveness, a remaining challenge is giving user-interpretable advice to improve passwords during password creation."*

<b><a href="https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_melicher.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Practical Recommendations for Stronger, More Usable Passwords 

In their study from 2020, Carnegie Mellon University researchers formulated *"concrete recommendations for policy configurations that produce a good balance of security and usability"*. They give clear guidance on composition requirements, blocklists, and neural-network-driven minimum-strength requirements. 

*"We recommend a 1c12+NN10 minimum-strength policy for organizations that wish to protect high-value accounts without a substantial negative usability impact."*

This paper is likely one of the most comprehensive and influential collections of best practices for authentication systems.   

<b><a href="https://dl.acm.org/doi/pdf/10.1145/3372297.3417882" rel="noopener">→ Read the Paper</a></b> (.pdf)
