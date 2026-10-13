---
id: jb-jwa
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['identity-authentication']
imageDecorative: true
title: "What is JWA? A Deep Dive into JSON Web Algorithms"
linkTitle: "What is JWA? A Deep Dive into JSON Web Algorithms"
description: "JSON Web Algorithms (JWA) power all JWT use cases. Learn how to decode JWA short names, what algorithms there are and why JWA matters for OpenID Connect."
excerpt: "The JSON Web Algorithms (JWA) standard provides definitions for several cryptographic algorithms. These algorithms enable a variety of purposes. In this article I'll introduce you to the essential ideas of JWA and outline how it helps to power e.g. OpenID Connect (OIDC)."
lead: "Algorithms for Modern Identity & Access Management (IAM)"
slug: jwa-json-web-algorithms
date: 2023-06-08
lastmod: 2025-06-22
draft: false
weight: 50
image: json-web-algorithms-jwa.webp
categories: ["identity-access-management"]
tags: ["jwt"]
pinned: false
homepage: false
---

## Definition of JWA

*JSON Web Algorithms (JWA)* is a specification providing a list of cryptographic algorithms. It's an integral part of the *JSON Object Signing and Encryption (JOSE)* family of standards. JOSE includes, for example, *JSON Web Tokens (JWT)*, *JSON Web Signature (JWS)*, and *[JSON Web Encryption (JWE)]({{< ref "/post/jwe-token/index.md" >}} "An Exploration into JSON Web Encryption Standards (JWE)")*.

JWA provides definitions for several cryptographic algorithms. These algorithms enable various purposes.

In this guide, you’ll learn the following:
- <mark>How to decode JWA short names</mark>
- <mark>What JWAs there are</mark>
- <mark>Why JWA matters for OpenID Connect</mark>

## Anatomy of JSON Web Algorithms

The JWA specification defines a unique name for every algorithm. These names are short strings encoding the particular algorithm family and hashing algorithm. Variants for SHA-256, SHA-384, and SHA-512 exist for most signing algorithms.

The most common algorithm names defined in the JWA specification include the following:

| Algorithm Name | Algorithm Description         |
|----------|-------------------------------------|
| HS256    | HMAC with SHA-256                   |
| RS256    | RSA signature with SHA-256          |
| ES256    | ECDSA using P-256 and SHA-256       |
| RSA-OAEP | RSAES OAEP using default parameters |
| A128KW   | AES key wrap with 128-bit key       |
{.table-striped}

[RFC 7518](https://datatracker.ietf.org/doc/html/rfc7518 "RFC: JSON Web Algorithms (JWA)") defines the fundamental base JSON Web Algorithms. The [JOSE IANA registry](https://www.iana.org/assignments/jose/jose.xhtml#web-signature-encryption-algorithms "JSON Web Signature and Encryption Algorithms") provides a complete list of supported algorithms. These unique references allow receivers to identify the correct cryptographical procedure. They are part of the JOSE header.

## Different Types of JSON Web Algorithms

The JWA specification defines many cryptographic algorithms powering various use cases, including:

- **Signing with JSON Web Signature (JWS)** ensures a token's integrity during transit.
- **Encryption with JSON Web Encryption (JWE)** to safeguard the confidentiality of token payload.
- **Distribution with JSON Web Keys (JWK)** to enable distributed JWT validation.

All JSON Web Algorithms are either symmetric or asymmetric.

### Understanding the Symmetric Key Algorithms

Hash-Based Message Authentication Codes (HMAC) are a popular algorithm class for signed JWTs. HMACs like HS256 provide a way of signing messages using a shared key. They belong to the family of symmetric cryptographic algorithms.

Symmetric algorithms need all involved parties to know the same key. They are helpful when all clients can guarantee the secrecy of the shared key. Their permissive nature allows all key possessors to create and verify JWTs. HMACs are best used in setups with one central issuer/ verifier.

### Delving into Asymmetric Key Algorithms

JWA specifies two asymmetric encryption and digital signature algorithm families – RSA and ECDSA. Public-private key pairs form the foundation of asymmetric algorithms. They enable decoupling verification or decryption of a token from being able to forge a new one. This is essential for distributed token validation scenarios. It allows decentralized authorization decision-making in OAuth 2.0 and OpenID Connect (OIDC).

## Practical Applications of JWA

A widespread use case is decentralized token signature verification for asymmetrically signed JWT. It's a key enabler for OpenID Connect.

At the forefront of this practical application is a central authorization server. This token issuer holds a private signing key and exposes its public key material. Clients in need to verify tokens fetch the public keys from the [well-known JWK endpoint]({{< ref "/post/jwks/index.md" >}} "JSON Web Key Sets Explained"). Based on cryptographic meta information carried in the JWT header, clients identify the matching key and JWA. This way, relying parties can verify a token's integrity without the need for centralized introspection.

## Conclusion

JWA is part of the JSON Web Token (JWT) suite of technologies. It's a collection of cryptographic algorithms. Being a vital ingredient of every JWT, JWA powers the entire JOSE toolbox. These JOSE technologies build secure systems that can interoperate easily. OpenID Connect is a famous example of such a framework.

Please note that each JSON Web Algorithm has its security implications. Appropriate use cases depend on the specifics of the implementation. It is paramount to choose algorithms that best meet your specific security requirements.