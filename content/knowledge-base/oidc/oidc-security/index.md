---
id: jb-research-oidc-security
imageDecorative: true
title: "Where do OpenID Connect implementations break?"
linkTitle: "OpenID Connect security"
description: "The attacks that work against OpenID Connect clients and providers, documented by Ruhr-University Bochum, and the checks that prevent them."
answer: "Implementations break mostly where tokens and redirects get checked. Documented attacks on relying parties include token substitution, key confusion and replay, and attacks on providers include redirect URI manipulation, PKCE downgrade and sub claim spoofing. Certification doesn't rule these out, as a 2020 lab analysis of OpenID Certified implementations disclosed 12 flaws."
date: 2023-05-15
lastmod: 2026-10-13
draft: false
image: openid-connect-security.webp
weight: 100
slug: openid-connect-security
aliases: ["/knowledge-base/oidc/openid-connect-security-research/"]
topics: [identity-authentication]
claim: "Testing 6 certified OpenID providers and 8 relying parties against 18 known attacks uncovered 12 implementation flaws."
changes:
  - date: 2026-10-13
    note: "Rewritten as a field-guide entry: question title, short answer, key findings and evidence table. Study summaries kept and extended with numbers from the thesis abstract."
---

## Key findings

{{< finding id="oidc-certified-12-flaws" source="Fries, Security Analysis of Real-Life OpenID Connect Implementations (Master's thesis, Ruhr-University Bochum, 2020)" url="https://www.nds.ruhr-uni-bochum.de/media/ei/arbeiten/2021/05/03/masterthesis.pdf" >}}Testing 6 OpenID Certified identity providers and 8 service providers against 11 service provider attacks and 7 identity provider attacks uncovered 12 implementation flaws.{{< /finding >}}

{{< finding id="oidc-spec-flaws" source="Mladenov and Mainka, OpenID Connect Security Considerations (Ruhr-University Bochum, 2017)" url="https://www.nds.ruhr-uni-bochum.de/media/ei/veroeffentlichungen/2017/01/13/OIDCSecurity_1.pdf" >}}Mladenov and Mainka classify session overwriting and IdP confusion as flaws in the OpenID Connect specification itself, separate from implementation bugs.{{< /finding >}}

{{< finding id="oidc-attacker-needs-no-network" source="Mladenov and Mainka, OpenID Connect Security Considerations (Ruhr-University Bochum, 2017)" url="https://www.nds.ruhr-uni-bochum.de/media/ei/veroeffentlichungen/2017/01/13/OIDCSecurity_1.pdf" >}}The attacks in the OpenID Connect Security Considerations report work for a web attacker who sends ordinary HTTP requests and has no control over the network.{{< /finding >}}

## Evidence

{{< studies caption="OpenID Connect security studies" >}}
{{< study title="Security Analysis of Real-Life OpenID Connect Implementations" org="Ruhr-University Bochum" year="2020" sample="6 identity providers, 8 service providers" method="Docker lab with PrOfESSOS, automatic and manual tests" url="https://www.nds.ruhr-uni-bochum.de/media/ei/arbeiten/2021/05/03/masterthesis.pdf" >}}18 attack types tested; 12 implementation flaws disclosed.{{< /study >}}
{{< study title="OpenID Connect Security Considerations" org="Ruhr-University Bochum" year="2017" sample="n/a" method="Technical report on specification and implementation flaws" url="https://www.nds.ruhr-uni-bochum.de/media/ei/veroeffentlichungen/2017/01/13/OIDCSecurity_1.pdf" >}}Catalogues attacks on clients and providers with defence recommendations.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

On the relying party:

- Validate every {{< term "id-token" >}}: signature with a key from the expected issuer's key set, algorithm, issuer, audience, expiry and nonce. Signature manipulation, key confusion, token recipient confusion and replay attacks all exploit a missing check. My essays on [JWKS]({{< ref "/post/jwks" >}}) and [the purpose of JWT]({{< ref "/post/purpose-of-jwt" >}}) cover the token side.
- Bind each login to the browser session that started it, and remember which identity provider you sent the user to. Session overwriting and IdP confusion exploit clients that don't.
- Identify users by issuer and subject together, never by subject or email alone.

On the OpenID provider:

- Compare redirect URIs exactly against the registered values.
- Enforce {{< term "pkce" >}} for clients that started with it, so an attacker can't downgrade the flow.
- Accept each authorization code once and only from the client it was issued to.

### For product and UX

- Treat "OpenID Certified" as a conformance signal, not a security audit. Fries tested certified implementations and still disclosed 12 flaws. When you choose a library or vendor, ask for penetration test results that cover these attack classes.
- If your product offers several identity providers, show users which one they're signing in with. IdP confusion attacks rely on the client mixing them up.

## The studies in detail

### Security Analysis of Real-Life OpenID Connect Implementations

In this Master's thesis from December 2020, Christian Fries presents a Docker-based lab environment for developers and penetration testers. The lab helps to find security flaws in real-world OpenID Connect Certified service provider and identity provider implementations, and it includes the PrOfESSOS tool for automatic tests. Fries selected 6 identity providers and 8 service providers that support the implicit and hybrid flows. He tested them against 11 service provider attacks and 7 identity provider attacks and disclosed 12 implementation flaws to the developers.

The thesis also describes common threats and attack scenarios. These include single- and cross-phase attacks on relying parties, like token substitution, key confusion and replay attacks. It also covers attacks on OpenID providers, like message flow confusion, PKCE downgrade and sub claim spoofing.

[Read the paper (PDF)](https://www.nds.ruhr-uni-bochum.de/media/ei/arbeiten/2021/05/03/masterthesis.pdf)

### OpenID Connect Security Considerations

In this 2017 technical report, Vladislav Mladenov and Christian Mainka from Ruhr-University Bochum look at OpenID Connect specification flaws and implementation issues that open up attack vectors. They outline attack scenarios like session overwriting, redirect URI manipulation and token recipient confusion, and give recommendations for defending against them.

[Read the paper (PDF)](https://www.nds.ruhr-uni-bochum.de/media/ei/veroeffentlichungen/2017/01/13/OIDCSecurity_1.pdf)

## Related

- [Step-up authentication with OpenID Connect]({{< ref "/post/stepup-authentication" >}})
- [How do attackers take over accounts?]({{< ref "/knowledge-base/account-security/account-hijacking" >}})
- [Glossary]({{< ref "/page/glossary" >}})
