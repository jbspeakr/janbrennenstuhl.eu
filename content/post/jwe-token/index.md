---
id: jb-jwe-token
imageDecorative: true
title: "JSON Web Encryption: Exploring JWE Token"
linkTitle: "JSON Web Encryption: Exploring JWE Token"
description: "Explore the world of JWE token with this in-depth guide. Gain understanding of JSON Web Encryption standards."
claim: "JWE keeps a JWT's payload confidential through authenticated encryption, but its security depends on careful algorithm choice, key management, token expiry and keeping sensitive data out of headers."
excerpt: "Have you ever wondered about the intricacies of JSON Web Encryption Standards? Get ready to decode the enigma with this deep dive into JWE Tokens. Gain insightful knowledge and grasp common data security use cases."
lead: "Encrypted JWTs: Understanding JSON Web Encryption"
slug: jwe
aliases: ["/jwe-token-json-web-encryption/"]
date: 2023-05-29
lastmod: 2025-06-15
draft: false
weight: 50
image: jwe-token-json-web-encryption.webp
tags: ["jwt", "oidc", "oauth2"]
series: jwt
---

## TL;DR

- JSON Web Encryption (JWE) is a standard for securing data transmission between parties, providing confidentiality, integrity, and authentication. It uses encryption to protect the payload of a [JSON Web Token (JWT)]({{< ref "/topics/tokens-jwt/" >}} "JWT Security: Best practices and when to use JSON Web Token") and supports both symmetric and asymmetric encryption techniques. It also allows creating nested JWTs, combining the advantages of JWE and JSON Web Signature (JWS).
- A **JWE token** consists of five parts: the Protected Header, the Content Encryption Key, the Initialization Vector, the Ciphertext, and the Authentication Tag. It supports various encryption algorithms like RSA-OAEP, AES-GCM, and ECDH-ES and requires using authenticated encryption to ensure the token's integrity and confidentiality.
- Modern authentication and authorization frameworks like OAuth2 and [OpenID Connect (OIDC)]({{< ref "/topics/identity-authentication/" >}} "OpenID Connect: User Authentication & Identity") use **JWE tokens** as bearer tokens. Proper key management is crucial to maintain the security guarantees of JWE.

## JSON Web Encryption (JWE) Token: A Comprehensive Guide

JWE is a widely-used standard for **securing data transmission** between parties. The industry standard describes a JSON Web Token (JWT) type that uses encryption to protect its **payload**. It provides **confidentiality** by encrypting the transmitted data, ensuring only **authorized parties** can access and read it.

In addition to providing confidentiality, **JWE tokens** offer **integrity** protection through message authentication codes (MACs). These codes ensure the receiver can detect tampering with the **encrypted payload**. Depending on the key management mode, it can also provide authentication.

JWE is relevant for modern AAA concepts in distributed, stateless environments as it enables an exchange of **sensitive information** statelessly.

### The Structure of an Encrypted JWT

The JWE standard ([RFC 7516](https://datatracker.ietf.org/doc/html/rfc7516 "JSON Web Encryption (JWE)")) is the go-to solution for developers who need to transmit JSON objects over the internet securely. JWE is a standard that defines how to encrypt and decrypt data in **JSON format** using various algorithms. In this section, I will discuss some of the core concepts of JWE tokens.

A typical, compact serialized, **encrypted JWT** is a dot (.) separated string that contains five parts:

- The JWE Protected Header is a base64url-encoded string representing the token metadata. It describes the JWE, how it was encrypted, and the media type of the encrypted payload. Protected JWE headers can’t be encrypted as they carry all information necessary for decryption.
- The JWE Encrypted Key (CEK) is another base64url-encoded string representing the encrypted, symmetric key used to encrypt the payload.
- The JWE Initialization Vector (IV) is a base64-encoded unique, random value string used when encrypting the plaintext and helps prevent attackers from exploiting patterns in plaintext or ciphertext.
- The JWE Ciphertext, the actual encrypted payload, also base64url-encoded, which was encrypted using the CEK, along with the IV and the additional authenticated data (AAD).
- The JWE Authentication Tag (MAC) results from performing **authenticated encryption** and allows a verifier to prove the integrity of the ciphertext and the AAD (the encoded protected header when using compact serialization). It ensures integrity during decryption.

### Support for Symmetric and Asymmetric Encryption Algorithms

Encrypted JWTs support asymmetric and **symmetric encryption** techniques to provide **end-to-end security** for the transmitted data. Symmetric **encryption algorithms** use the same key for encryption and decryption, while asymmetric  algorithms use a pair of keys.

The sender encrypts the plaintext payload using a randomly generated symmetric CEK, then encrypts the key using the recipient's public key or a shared secret key (a long-lived key encryption key). The recipient can then decrypt the encrypted key using their private secret key and use it to decrypt the payload.

As they are self-contained and carry their corresponding symmetric key (CEK), encrypted JWTs also support hybrid encryption, which allows combining the performance of symmetric encryption with the assurances of public-key cryptography. This flexibility lets developers choose between different encryption algorithms based on their needs.

### Nested JWTs

Another exciting feature of JWE is the ability to create nested JWTs. As the JWE standard allows arbitrary data to be packaged into the payload, it also allows nesting a signed JWT (JWS) inside an encrypted JWT (JWE). Wrapping a JWS into a JWE can be helpful when dealing with asymmetrically encrypted JWE, as these alone do not allow to verify that the JWT was produced by a specific token issuer, merely that someone who possessed the issuer's public key forged the token. Nested JWTs combine the advantages of JWE and JWS. Symmetrically encrypted JWEs provide all the above security properties without creating nested tokens.

## Working with Different JWE Algorithms

The [JSON Web Algorithms (JWA)]({{< ref "/post/jwa/index.md" >}} "What is JWA?") standard registers all cryptographic algorithms supported by the JWT ecosystem in [RFC 7518](https://datatracker.ietf.org/doc/html/rfc7518 "JSON Web Algorithms (JWA)"). The most commonly recommended option for asymmetric key encryption is ECDH-ES, while AES-GCM (with key wrapping) is the recommended alternative for symmetric encryption setups.  

### JWE with AES Algorithms

AES (Advanced Encryption Standard) algorithm is still the de-facto standard of a symmetric algorithm that can be used with JWE. It involves using the same secret key to encrypt and decrypt data. The **JWE token can be encrypted using** AES-GCM (Galois/Counter Mode), which provides authenticated encryption with associated data (AEAD). AES128 should be fine for "short-lived" tokens ([<34 million years](https://crypto.stackexchange.com/questions/76738/has-aes-128-been-fully-broken/76746#76746 "Has AES-128 been fully broken?")).

### JWE with RSA Algorithms

RSA (Rivest-Shamir-Adleman) is an example of an asymmetric encryption algorithm supported by JWE. It involves generating a key pair where the public key encrypts data while the private key allows to decrypt it. Commonly used in JWE token contexts is RSA-OAEP (Optimal Asymmetric Encryption Padding).

### JWE with Elliptic Curve Algorithms

Elliptic Curve Cryptography (ECC) is another example of an asymmetric cryptography system supported by JWE. It involves generating a key pair based on elliptic curves rather than prime numbers. The JWE token can be encrypted using ECDH-ES (Elliptic Curve Diffie-Hellman Key Agreement with Elliptic Curve Cryptography) or ECDH-ES+A128KW (ECDH-ES with AES key wrap).

### Authenticated Encryption Algorithms

JWE requires using authenticated encryption (AE) to ensure that the token is encrypted and integrity protected, supporting multiple AE algorithms. Two distinct classes exist, authenticated encryption with AES/CBC/HMAC/SHA and AES/GCM. The latter also supports Authenticated Encryption with Associated Data (AEAD), which provides confidentiality, integrity, and **authenticity** of the encrypted message and additional authenticated data. It ensures that the message has not been tampered with during transmission.

## JWE Token Generation Process

### Encryption Algorithm: Choosing the Right One for Your Needs

Choosing a suitable algorithm is crucial when generating a JWE token. There are several options available, including AES-GCM, AES-CBC-HMAC-SHA2, and RSA-OAEP. Each algorithm has strengths and weaknesses, so choosing one that aligns with specific needs and requirements is essential.

### Generating Keys: Private Key vs Secret Key

The process of generating keys for JWE tokens differs depending on the form of encryption. Applying symmetric encryption requires generating a random secret key that both the sender and receiver can use to encrypt and decrypt data. Asymmetric encryption involves creating a public-private key pair.

### Complete JOSE Header

The process of generating a JWE token is complex and involves several steps. The first step is the creation of a complete JOSE header that contains information about the encryption algorithm, **key management** algorithm, key ID (kid), and other critical details. This header is essential because it provides the foundation for creating a secure and valid JWE token.

### Encryption & Serialization: Creating Valid JWE Tokens

Once a suitable encryption algorithm is chosen and keys generated, it's time to encrypt the payload involving an appropriate initialization vector (IV). After successfully calculating the ciphertext and the corresponding authentication tag, all individual parts are appropriately encoded and joined into their compact serialization format. As JWE deals with various cryptographic algorithms, is somewhat complex, and can become confusing, I recommend leveraging standard libraries to create encrypted and properly serialized JWT.

## JWE Token Decryption Process

### Decoding the JWE Compact Serialization

Decrypting a JWE token starts with decoding the JWE compact serialization. The JWE compact serialization is a string comprising five parts separated by dots: the JWE header, the encrypted key, the initialization vector, the JWE ciphertext, and the authentication tag. It is the most commonly used type compared to the less popular JWE JSON serialization.

The protected header contains information about the encryption and key management algorithms used to encrypt the payload. This information is required to decrypt the token. Once being (base64url) decoded, these claims are accessible for introspection.

### Key Decryption

Access to the private secret key initially used to encrypt is required to decrypt the JWE token. The **decryption algorithm** referenced in the JOSE header defines the cryptographic procedure for the CEK. Only after decryption can it unlock the actual payload. In the case of public key cryptography, the associated private key must be available. Single-key encryption requires the corresponding secret shared between both parties to be present.

### Payload Decryption

The IV value initializes the cipher instance with an appropriate mode like CBC, GCM, etc. The previously obtained JWE encrypted key (CEK) can decrypt the JWE ciphertext value, yielding a plain text (often a JSON object) after successful decryption. The integrity of the ciphertext and its additional authenticated data (AAD), in this case, the JWE header elements, is verified using the authentication tag value provided in the last part of the serialized JWE object.

## Security Considerations

### Authentication Tag and Additional Authenticated Data

One key feature that makes JWE tokens secure is using an authentication tag and additional authenticated data (AAD). The authentication tag is a small piece of data at the end of the encrypted JWT, which allows recipients to verify that the message has not been tampered with during transmission. AAD provides an extra layer of security by enabling the sender to include additional data in the encryption process that the recipient will verify.

However, not all JWE tokens have an authentication tag or AAD. There are JWA encryption algorithms that do not use an authentication tag, in which case the value is supposed to be an empty octet sequence.

### Leaky Headers

Another potential security concern when using JWE tokens is custom header elements. JWT headers include public claims by design that are integrity protected at max. Using customer header claims means they can potentially leak sensitive information if mismanaged. It's crucial to handle custom header claims carefully and only include necessary information. If confidentiality is needed, custom fields belong in the payload. If there is a need for public hints, the header metadata is just fine.

### Key Management and Token Expiry

Proper key management is essential for maintaining the security of JWE tokens. Identity providers must store the long-lived key management keys securely and rotate them regularly to prevent unauthorized access, as compromise might result in disclosing all contents protected with that key. 

Similarly, successful attacks on the CEK will strip all confidentiality properties from the corresponding token. Implementing token expiry to limit the amount of time token usage before it becomes invalid is necessary for all everyday use cases.

### Weak algorithms

The JWE specification includes a limited range of supported encryption algorithms. And also, the officially supported ones rarely convince security experts: The ECDH-ES algorithm [allows an attacker to recover the private key](https://web.archive.org/web/20201130103442/https://blogs.adobe.com/security/2017/03/critical-vulnerability-uncovered-in-json-encryption.html "Critical Vulnerability Uncovered in JSON Encryption") if not adequately implemented. [GCM is likely fragile](https://rwc.iacr.org/2017/Slides/nguyen.quan.pdf "Practical Cryptanalysis of Json Web Token and Galois Counter Mode’s Implementations"), as Google researchers claim. And [RSA encryption with PKCS1v1.5](https://archiv.infsec.ethz.ch/education/fs08/secsem/bleichenbacher98.pdf "Chosen Ciphertext Attacks Against Protocols Based on the RSA Encryption Standard PKCS #1") padding is broken.

When leveraging JWE, I recommend supporting short notice and timely transitioning to alternative encryption algorithms.

## Comparison of JWE and Other JSON Security Standards

### JWE vs JWT

While both JWE and JWT are part of the JSON Object Signing and Encryption (JOSE) security framework, they [serve different purposes]({{< ref "/post/purpose-of-jwt/index.md" >}} "The Purpose of JWT: Stateless Authentication"). As mentioned, JWEs provide JSON data encryption, while unsecured JWTs ([RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519 "JSON Web Token (JWT)")) provide no particular security properties. In identity and access management (IAM) scenarios where a client sends a token to a resource server as proof of identity, JSON Web Tokens commonly appear in their signed JWS form.

### JWE vs JWS (JSON Web Signature)

JWS is a JSON-based format for representing digital signatures ([RFC 7515](https://datatracker.ietf.org/doc/html/rfc7515 "JSON Web Signature (JWS)")). JWS assures integrity and authentication, but it does not provide confidentiality. JWS tokens contain three elements: the JOSE header, payload, and signature. On the other hand, JSON Web Encryption (JWE) is a standard for encrypting JSON data. JWE tokens protect sensitive data by also providing confidentiality.

### JWE vs JWK (JSON Web Key)

JWK is another standard in the JOSE family (RFC 7517) that defines JSON format for cryptographic keys. A [JWK Key Set (JWKS)]({{< ref "/post/jwks/index.md" >}} "Mastering JWKS: JSON Web Key Sets Explained") can contain keys used for either encryption or signing, depending on their type. JWKs can be used with both JWS and JWE standards to provide cryptographic operations such as decryption or verification of digital signatures.

## Practical Applications of JWE Tokens

The nature of JWE tokens makes them ideal for enabling stateless information exchange in modern AAA processes or exotic [one-time-token]({{< ref "/post/single-use-jwt/index.md" >}} "Single-Use JWT: The Power of Stateless One Time Token") (OTT) scenarios. In this section, I will discuss some practical applications of JWEs.

### Bearer Token: A Powerful Authentication and Authorization Tool

JWEs often appear as bearer tokens to authenticate and authorize access to protected resources. Bearer tokens are powerful tools because they allow users to access resources without repeatedly providing credentials. Instead, the bearer token serves as proof of identity and authorization.

### JWE in OAuth2 and OIDC

[OAuth2]({{< ref "/topics/identity-authentication/" >}} "Delegated Authorization with OAuth 2.0") and OpenID Connect (OIDC) are widely used authentication/ authorization protocols, often used for securing web APIs. They allow users to grant access to their resources without sharing their credentials with third-party applications. These protocols can use JWE Tokens to provide an additional layer of security by encrypting the access token. Enforcing clients to treat them as genuinely opaque tokens allows the token issuer (authorization server) to transport sensitive information like PII statelessly. At the same time, it also ensures that even if an attacker intercepts the token, they cannot read its contents without the **decryption key**.

### JWE for Data at Rest

Data at rest refers to data stored on disk or other storage media. This data is vulnerable to attacks if it is not adequately secured. Although not common, JWE tokens can encrypt sensitive data before storing it on disk, ensuring that even if an attacker gains access to the storage media, they cannot read its contents without the decryption key.

## Conclusion

JSON Web Encryption (JWE) is a powerful tool for ensuring the confidentiality and security of data transmissions. JWE tokens carry an encrypted payload between multiple parties. The secured data can only be read with the proper decryption key, even if intercepted. Authenticated encryption ensures that sensitive information remains confidential and tamper-proof, providing both senders and receivers peace of mind.

The use cases for JWE tokens are varied and versatile. Use JWE in situations where confidential data exchange is necessary. When used as a bearer token within modern authorization and authentication frameworks like OpenID Connect (OIDC), JWE tokens transport sensitive information often as access tokens.

## Frequently Asked Questions (FAQs)

- <b>What is the purpose of JWE?</b> – JWE tokens securely transmit data between parties in a JSON format. They provide confidentiality, integrity, and authenticity to the transmitted data.
- <b>How does JWE differ from JWT?</b> JWE focuses on encrypting the payload, while plain JWT provides no additional security properties.
- <b>What are standard encryption algorithms used in JWE?</b> Some common encryption algorithms include RSA-OAEP, AES-GCM, and ECDH-ES.
- <b>Is it safe to use JWE tokens for sensitive data?</b> Yes, as long as proper security measures are taken, such as using robust encryption algorithms and protecting the encryption and decryption keys.
- <b>Can JWE be used with other JSON security standards?</b> JWE can be combined with other JOSE, such as JWS, to support even more complex scenarios with nested JWTs.