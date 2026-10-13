---
id: jb-research-compromised-credentials
kind: research
status: published
reviewStatus: not-reviewed
topics: ['identity-authentication']
imageDecorative: true
title: "Compromised Credentials Research"
linkTitle: "Security Research: Credential Stuffing & Compromised Credentials"
description: "How to defend against credential stuffing? How to check for compromised credentials? These top security research papers give answers ➢ User Account Security"
lead: "How to recognize compromised credentials and how to defend against credential stuffing attacks? These selected security research papers give answers …"
slug: compromised-credentials-stuffing
date: 2023-04-21
lastmod: 2023-04-27
draft: false
image: compromised-credentials-credential-stuffing.webp
type: docs
menu:
  knowledge-base:
    parent: "account-security"
    identifier: "compromised-credentials"
weight: 100
toc: true
---

## Protocols for Checking Compromised Credentials

*"To prevent credential stuffing attacks, industry best practice now proactively checks if user credentials are present in known data breaches."* 

For this paper, Cornell Tech and Cloudflare researchers analyzed existing compromised credential checking (C3) services and formulated a formal description including operational requirements, and relevant threat models. The cherry on the cake are *"two protocols that provide stronger protection for users’ passwords"* that according to the authors are still practical to deploy.

<b><a href="https://rist.tech.cornell.edu/papers/c3.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Protecting accounts from credential stuffing with password breach alerting

This paper by Google and Stanford researchers describes how Googles password breach alerting functions under the hood, what constrains and hard requirements it adheres to and which cryptographic protocols are being leveraged.

*"Our protocol relies on a combination of computationally expensive hashing, k-anonymity, and private set intersection. Our approach improves on existing protocols by taking into account both an adversarial client and server, while also minimizing the chance of false positives."*

<b><a href="https://storage.googleapis.com/pub-tools-public-publication-data/pdf/33bc2203e7bcb5c0abe289f7432e11563fb2a238.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## Data Breaches, Phishing, or Malware? Understanding the Risks of Stolen Credentials

Using billions of breached credentials, researchers from Google, Berkeley and the International Computer Science Institute *"explore to what degree the stolen passwords […] enable an attacker to obtain a victim’s valid email credentials — and thus complete control of their online identity due to transitive trust".* They also provide helpful risk signals to mitigate the risk of hijacking.

Although the study is from 2017, the findings about password reuse and presented mitigation approaches, like blocking login attempts that fail to match a user’s historical login behavior or device profile, are still relevant today! 

<b><a href="https://dl.acm.org/doi/pdf/10.1145/3133956.3134067" rel="noopener">→ Read the Paper</a></b> (.pdf)
