---
id: jb-research-oidc-security
kind: research
status: published
reviewStatus: not-reviewed
topics: ['identity-authentication']
imageDecorative: true
title: "OIDC Security Research"
linkTitle: "Threats & Attacks: Security Research on OpenId Connect (OIDC)"
description: "Dive into OpenID Connect security, learn from security researchers, and enhance your knowledge on OIDC threats and attack scenarios."
lead: "While OpenID Connect represents an important step forward in online security, it is not without risks and attack scenarios. From phishing attempts to session hijacking, cybercriminals continue to develop sophisticated techniques to exploit vulnerabilities. Unauthorized individuals could exploit poorly built OpenID systems, resulting in catastrophic data breaches. This highlights the significance of comprehending the complexities of OpenID Connect threats and attack scenarios. We may continue to use this valuable tool to improve our digital defenses while limiting potential hazards by remaining aware and extra vigilant."
date: 2023-05-15
lastmod: 2023-05-15
draft: false
image: openid-connect-security.webp
type: docs
menu:
  knowledge-base:
    parent: "oidc"
    identifier: "oidc-security"
weight: 100
toc: true
slug: openid-connect-security-research
---

## Security Analysis of Real-Life OpenID Connect Implementations

In this Master's thesis, Christian Fries presents a lab environment for developers and penetration-testers to unveil security flaws in real-world OpenID Connect Certified Service Provider and Identity Provider implementations. 

In addition, the paper describes common threats and attack scenarios including single- and cross-phase attacks on relying parties, like token substitution, key confusion and replay attacks. Also OpenID provider attacks, like message flow confusion, PKCE downgrade or sub claim spoofing are covered.  

<b><a href="https://www.nds.ruhr-uni-bochum.de/media/ei/arbeiten/2021/05/03/masterthesis.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)

## OpenID Connect Security Considerations

This paper from security researchers of the Ruhr-University Bochum looked at OpenID Connect specification flaws and implementation issues opening up attack vectors. They outline common attack scenarios like session overwriting, redirect URI manipulation or token recipient confusion and give attack defense recommendations.

This crisp technical report is definitely a great source of inspiration for everyone who plans to conduct any form of OIDC pen-testing.  

<b><a href="https://www.nds.ruhr-uni-bochum.de/media/ei/veroeffentlichungen/2017/01/13/OIDCSecurity_1.pdf" rel="noopener">→ Read the Paper</a></b> (.pdf)
