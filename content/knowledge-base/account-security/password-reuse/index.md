---
id: jb-research-password-reuse
kind: research
status: published
reviewStatus: not-reviewed
topics: ['identity-authentication']
imageDecorative: true
title: "Password Reuse Studies"
linkTitle: "Data Breaches: 5 Alarming Password Reuse Studies"
description: "Security Research | Explore 5 alarming password reuse studies revealing the dangers of reusing passwords. Compromised Credentials ➢ Password Security"
lead: "Passwords are still the keys that unlock our online lives. Unfortunately, many of us make the grave mistake of reusing the same password across multiple accounts, putting our sensitive data at risk. These security research papers explore the dangers of password reuse and reveal the true extent of the problem."
slug: password-reuse-studies-security
date: 2023-04-27
lastmod: 2023-05-17
draft: false
image: password-reuse-research.webp
type: docs
menu:
  knowledge-base:
    parent: "account-security"
    identifier: "password-reuse"
weight: 110
toc: true
---

From data breaches to identity theft, studies from around the globe examine the consequences of password reuse and provide practical tips to help you safeguard online security – especially if you don't have any means to do [step-up authentication]({{< ref "/post/stepup-authentication/index.md" >}} "Enhancing Security: A Guide to Step-Up Authentication"). So buckle up and get ready to learn about the bad password habit of using same or similar passwords everywhere!

## Observing Passwords in Their Natural Habitat

For this study Carnegie Mellon, Google and the International Computer Science Institut researchers surveilled devices of 154 participants for an average of 147 days each to *"analysis password characteristics and behaviors across the full range of participants’ web-based accounts"*.

Among other discoveries, the analyzed data surfaced that "[…] the use of symbols and digits in passwords predicts increased likelihood of reuse, while increased password strength predicts decreased likelihood of reuse; that password reuse is more prevalent than previously believed, especially when partial reuse is taken into account […]".

<b><a href="https://dl.acm.org/doi/pdf/10.1145/3133956.3133973" rel="noopener">→ Read the Paper</a></b> (.pdf)

## The Tangled Web of Password Reuse

This study from 2014, used several hundred thousand leaked passwords from multiple sites and a user survey on password reuse to unveil the not so shocking estimation that *"43-51% of users reuse the same password across multiple sites"*. But the researchers from Princeton and Indiana University went a step further, also identified "a few simple tricks users often employ to transform a basic password between sites" and developed a prototypical cross-site password-guessing algorithm.

The research underlines the importance of using truly unique passwords, as an attacker with a leaked, even nonidentical password *"can mount an online guessing attack with orders of magnitude higher success than an attacker without a leaked password."*

<b><a href="https://www.ndss-symposium.org/wp-content/uploads/2017/09/06_1_1.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Understanding Password Choices: How Frequently Entered Passwords are Re-used Across Websites

A Michigan State University research found in 2016, that *"people do tend to re-use each password on 1.7–3.4 different websites"* and that *"they reuse passwords that are more complex, and mostly they tend to re-use passwords that they have to enter frequently"*.

The most interesting observation though is the unexpected interdependence they found between accounts and which underlines nicely the ambivalence of arbitrary password composition requirements:

*"[…] if users must memorize a strong password on a website where they have to enter it frequently, they then re-use it elsewhere. This results in stronger passwords on more websites. This practice puts users at greater risk of cross-site password guessing attacks […]"*

<b><a href="https://www.usenix.org/system/files/conference/soups2016/soups2016-paper-wash.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## A Large-Scale Study of Web Password Habits

Microsoft researchers investigated password use and password re-use habits of half a million users over a the course of a three month period. This study from 2007 was the first large scale study of its kind, and yields numerous findings, that *"particularly confirm the conventional wisdom about the large number and poor quality of user passwords. In addition passwords are re-used and forgotten a great deal."*

<b><a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/11/www2007.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Designing Password-Reuse Notifications

When companies notice password reuse or compromised credentials, they may require their users to perform password reset procedures and send affected users a notification. Two user studies, run by a group of security researchers from Germany and the USA in 2018, provide
insight into such notifications. They discuss *"best practices for password-reuse notifications and how notifications alone appear insufficient in solving password reuse"*.

A very valuable read for everyone working on balancing account security and usability!

<b><a href="https://dl.acm.org/doi/pdf/10.1145/3243734.3243767" rel="noopener">→ Read the Paper</a></b> (.pdf)
