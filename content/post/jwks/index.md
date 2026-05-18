---
title: "Mastering JWKS: JSON Web Key Sets Explained"
linkTitle: "Mastering JWKS: JSON Web Key Sets Explained"
description: "Demystify JWKS with this simplified guide. Learn about JSON Web Key Sets, their purpose, and how to implement them successfully. Master JWKS now!"
excerpt: "Implementing JSON Web Key Sets (JWKS) is crucial for organizations that want to leverage modern, decentralized authentication and authorization protocols. In this article I discuss the purpose of JWKS, guide you though their technical specification and outline benefits as well as best-practices to securely exposing public key material."
lead: "Securely Expose Public Key Material"
slug: jwks-json-web-key-set
date: 2023-06-02
lastmod: 2023-06-02
draft: false
weight: 50
image: "jwks-json-web-key-sets.webp"
categories: ["identity-access-management"]
tags: ["jwt", "oidc"]
---

## TL;DR
- JWKS (JSON Web Key Set) is a tool for standardizing the representation and management of cryptographic keys via a JSON object.
- The technology, defined in RFC 7517, enables client-local [JWT (JSON Web Tokens)]({{< ref "/tags/jwt/" >}} "JWT Security: Best practices and when to use JSON Web Token") verification and is integral for decentralized authentication protocols such as OpenID Connect and [OAuth2]({{< ref "/tags/oauth2/" >}} "OAuth 2.0 in Action").
- Implementing JWKS simplifies key management, eases key rotation, and secures key distribution across multiple servers.

## Technical Specifications of JWK and JWKS

JWKS is an acronym for JSON Web Key Set. It is a collection of JSON Web Keys (JWKs) used to verify JSON Web Tokens (JWTs). Both constructs are defined in [RFC 7517](https://datatracker.ietf.org/doc/html/rfc7517 "RFC 7517: JSON Web Key (JWK)"), yet another integral member of the famous JOSE standards family. JWK Sets provide a standardized way and format for servers to obtain the public keys required to verify asymmetrically signed JWTs locally.

### What is JSON Web Key (JWK)?

A JWK is a JSON object data structure that represents a cryptographic key. It contains the key type, key operations, algorithm, and all relevant material to reconstruct the signature verification key. All officially supported [JSON Web Algorithms (JWA)]({{< ref "/post/jwa/index.md" >}} "What is JWA?") are defined in [RFC 7518](https://datatracker.ietf.org/doc/html/rfc7518 "RFC 7518: JSON Web Algorithms (JWA)"). 

The JSON data structure of the JWK format allows for easy, web-native exchange of public keys. The representation of an Elliptic Curve signature key of curve P-256 could look like this:

```json
{
    "kty": "EC", 
    "use": "sig",
    "crv": "P-256",
    "kid": "01H1SG7BX197N040C0MHTDV1HR",
    "x": "SEfcECpwqQg-vZ6Lv99RyV0Qkatngz1RV25nI5SOrPg",
    "y": "YU2PRA6pXZ62OW_XuzjJqplqmBUtBwT2pKUZUVxUYfc",
    "alg": "ES256"
} 
```

### What is JSON Web Key Set (JWKS)?

A JWKS is a JSON object that represents a set of JWKs. It must contain a "keys" member and an array of JWKs. JSON Web Key Sets enable identity providers to support and expose more than one public key under a well-known resource. The following example JWK Set format contains two public cryptographic keys – one using an Elliptic Curve (EC) algorithm and a second one using an RSA algorithm:

```
{"keys": 
    [{
        "kty": "EC", 
        "use": "sig",
        "crv": "P-256",
        "kid": "01H1SG7BX197N040C0MHTDV1HR",
        "x": "SEfcECpwqQg-vZ6Lv99RyV0Qkatngz1RV25nI5SOrPg",
        "y": "YU2PRA6pXZ62OW_XuzjJqplqmBUtBwT2pKUZUVxUYfc",
        "alg": "ES256"
    }, {
        "kty":"RSA",
        "n": "1qrQCTst3RF04aMC9Ye_kGbsE0sftL4FOtB_WrzBDOFdrfVwLfflQuPX5kJ-0iYv9r2mjD5YIDy8b-iJKwevb69ISeoOrmL3tj6MStJesbbRRLVyFIm_6L7alHhZVyqHQtMKX7IaNndrfebnLReGntuNk76XCFxBBnRaIzAWnzr3WN4UPBt84A0KF74pei17dlqHZJ2HB2CsYbE9Ort8m7Vf6hwxYzFtCvMCnZil0fCtk2OQ73l6egcvYO65DkAJibFsC9xAgZaF-9GYRlSjMPd0SMQ8yU9i3W7beT00Xw6C0FYA9JAYaGaOvbT87l_6ZkAksOMuvIPD_jNVfTCPLQ",
        "e":"AQAB",
        "alg":"RS256",
        "kid":"01H1SGVCX7GKBGE2J2QMQREAGN"
    }]
}
```

### Locate JSON Web Key Sets

Many modern identity providers like Google expose their JWK Sets via the `jwks_uri` attribute within the [well-known discovery endpoint](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig "OpenID Connect Discovery Spec") of OpenID Connect (OIDC) located at `https://{identity-provider}/.well-known/openid-configuration` which often points to `https://{identity-provider}/.well-known/jwks.json` or a similar resource.

## Benefits of Using JWKS

### Easy Management of Keys with JWK Sets

One of the main benefits of using JWKs is that they provide an easy way to manage and distribute keys across multiple servers or locations. Instead of hardcoding public keys into application code, token issuers (authorization servers) only need to provide their clients with an URL for their JSON Web Key Set. 

Any application that needs access to the keys can retrieve them from that remote location. This eliminates the need for manual key distribution, resolves, and ensures all applications use the same set of keys. This makes it easier to manage multiple keys and rotate them when necessary.

### Simplified Key Rotation Process Using JWKs

Rotating keys is essential for maintaining security in any system that uses cryptography. However, manually replacing these keys can take time and effort. JWKS can simplify this process by automating key rotation.

As JWKs decouple the authorization server from relying party applications, token issuers can generate new asymmetric key pairs whenever necessary. Setting up regular intervals for key rotation, publishing the new public key material, and using the latest private key automatically after some grace period, can ensure that the amount of keys signed with a particular key has a natural upper limit.

### Compatibility with Various Protocols and Applications

Finally, the JSON Web Key Set standard is compatible with various protocols and applications. This means it can enable local token validation in the context of web applications, APIs, mobile apps, and more. Popular authentication protocols such as OAuth 2.0 and OpenID Connect support JSON Web Key Set.

## Best Practices & Security Considerations

Dealing with cryptographic and primarily private keys is a highly sensitive undertaking. The security issues relevant to any cryptographic application must also be considered when dealing with JSON Web Token (JWT) and JSON Web Signature (JWS). It is essential to implement JSON Web Key Set (JWKS) correctly to ensure the security and integrity of the entire infrastructure. Here are some best practices for implementing JWKS.

### Use Transport Layer Security

Serving a JSON Web Key over HTTP poses significant security risks as it can be intercepted or modified in transit. Therefore, it is crucial to use HTTPS also when serving JWKS. HTTPS ensures that all communication between the client and server is encrypted, preventing unauthorized access or in-transit modification.

### Make sure JWKS is correct and current

The entire system's security relies on having up-to-date and accurate JWKS. If any cryptographic keys in the set expire or become invalid, it could result in rejected tokens or, worse yet, accepted but fraudulent tokens being used throughout the system. It's essential to have processes in place to monitor and update JSON Web Keys regularly. This includes rotating keys, removing EOL keys, and adding new keys as necessary. Cryptographic key management should be automated to ensure that all cryptographic keys are always up-to-date. Symmetric keys must not be exposed!

### Validate the signatures of incoming JWTs using JWKs

One of the primary purposes of implementing JWKS is to verify the authenticity of incoming JWTs – be it access token or ID token. To do this, all applications that perform authorization decisions based on JSON [Web Token]({{< ref "/post/single-use-jwt/index.md" >}} "Single-Use JWT: The Power of Stateless One Time Token"), should fetch the entire JSON Web Key Set per the corresponding cache-control headers. 

Validating a JWT starts with fetching the `kid` (key ID) parameter from its header. This key identifier specifies which cryptographic key in the JWKS was used by the authorization server to sign the token. The identified key can then be used to verify the signature by comparing it against the one included in the token's signature.

If the signature is valid, the token was issued by a trusted party and can be processed accordingly. An invalid token must be rejected immediately.

### Consider rotating your JWKS keys periodically

Rotating JSON Web Keys periodically is an essential best practice for maintaining a proper security posture. Doing so reduces the risk of compromised keys being used maliciously throughout the system. Rotating keys effectively requires creating a new set before retiring any old ones. This will ensure no gaps in coverage during the transition period.

## Conclusion: The Importance of Using JSON Web Key Sets

Implementing JSON Web Key Sets (JWKS) is crucial for organizations that leverage decentralized authentication protocols like OpenID Connect or authorization delegation protocols like plain OAuth2. Truly benefiting from public-key cryptography requires client applications to verify issued tokens locally, without indispensable synchronous HTTP requests. 

Using a data interchange format like JSON Web Key (JWK), which is based on JavaScript Object Notation (JSON), and hosting the cryptographic keys on publicly accessible, standardized discovery endpoints allows maintaining decoupled service architectures while shifting effort to the client-side following a pull principle.