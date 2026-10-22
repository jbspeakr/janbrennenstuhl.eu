---
id: jb-guide-jwt-anatomy
title: "What is inside a JWT?"
linkTitle: "JWT anatomy"
description: "The 3 parts of a signed JSON Web Token, what each one contains, and why reading a token is not the same as trusting it."
answer: "A signed JWT is 3 base64url-encoded parts joined by dots: a header that names the algorithm, a payload of claims, and a signature over both. The payload is encoded, not encrypted, so anyone holding the token can read it; only a signature check with a key you trust tells you whether to believe it."
claim: "A signed JWT's claims are readable by anyone who holds it; trust comes only from verifying the signature with an allowed algorithm and a trusted key."
slug: jwt-anatomy
date: 2026-10-13
draft: false
weight: 20
topics: [tokens-jwt, identity-authentication]
scripts: [jwt]
---

## Key findings

{{< finding id="jwt-claims-in-jws-or-jwe" source="RFC 7519, JSON Web Token (JWT), Section 2" url="https://www.rfc-editor.org/rfc/rfc7519#section-2" >}}A JWT is a set of claims encoded as a JSON object inside a JWS or a JWE, so the same token format can be signed, encrypted, or both.{{< /finding >}}

{{< finding id="jwt-payload-is-readable" source="RFC 7519, Section 12, Privacy Considerations" url="https://www.rfc-editor.org/rfc/rfc7519#section-12" >}}The payload of a signed JWT is only base64url-encoded, so a token that carries privacy-sensitive claims needs encryption or must not reach parties who should not read it.{{< /finding >}}

{{< finding id="jwt-registered-claims-optional" source="RFC 7519, Section 4.1" url="https://www.rfc-editor.org/rfc/rfc7519#section-4.1" >}}RFC 7519 registers 7 claim names, iss, sub, aud, exp, nbf, iat and jti, and none of them is mandatory in every case; each application profile decides which it requires.{{< /finding >}}

{{< finding id="jwt-allowlist-algorithms" source="RFC 8725, JSON Web Token Best Current Practices, Section 3.1" url="https://www.rfc-editor.org/rfc/rfc8725#section-3.1" >}}JWT libraries must let the caller specify the supported algorithms and must not use any other algorithm, which closes the door on tokens whose header was changed to "none".{{< /finding >}}

## Evidence

{{< studies caption="Specifications" >}}
{{< study title="RFC 7519: JSON Web Token (JWT)" org="IETF" year="2015" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc7519" >}}Defines the JWT format, the registered claim names and the privacy considerations for claims.{{< /study >}}
{{< study title="RFC 7515: JSON Web Signature (JWS)" org="IETF" year="2015" sample="n/a" method="Specification" url="https://www.rfc-editor.org/rfc/rfc7515" >}}Defines the compact serialization: base64url header, payload and signature joined by dots.{{< /study >}}
{{< study title="RFC 8725: JSON Web Token Best Current Practices" org="IETF (BCP 225)" year="2020" sample="n/a" method="Best current practice" url="https://www.rfc-editor.org/rfc/rfc8725" >}}Requires algorithm allowlists in libraries and audience, issuer and key validation in applications.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

- Treat a decoded payload as untrusted input until the signature verifies. Pin the algorithms you accept instead of reading `alg` from the token, and resolve the key by `kid` only from a key set you trust, such as the issuer's [JWKS]({{< ref "/post/jwks" >}}).
- After the signature, check `exp`, `nbf`, `iss` and `aud`. RFC 8725 makes audience validation a must whenever one issuer serves several relying parties.
- Keep secrets and personal data out of signed tokens. If a token has to carry them, use [JWE]({{< ref "/post/jwe-token" >}}) or keep the data on the server and put a reference in the token.

### For product and UX

- Tokens end up in logs, browser storage and support tickets. Anything in the payload should be safe to show to whoever might see it there.
- Short token lifetimes are a product decision as much as a security one: they decide how often a session has to be refreshed.

## Try it

{{< explainer "jwt" "Decode a token in your browser" >}}
The example token below has 3 parts. Paste your own token into the decoder to split and decode it. Decoding happens only in your browser; nothing is sent anywhere, and the signature is not verified.

`eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjIwMjYtMTAifQ.eyJpc3MiOiJodHRwczovL2lkLmV4YW1wbGUuY29tIiwic3ViIjoidXNlci0xMjMiLCJhdWQiOiJodHRwczovL2FwaS5leGFtcGxlLmNvbSIsImV4cCI6MTc5MTkwMDAwMCwiaWF0IjoxNzkxODk2NDAwLCJqdGkiOiI3ZjNjOWEifQ.cGxhY2Vob2xkZXIgc2lnbmF0dXJlLCBub3QgdmFsaWQ`

- **Header** decodes to `{"alg":"ES256","typ":"JWT","kid":"2026-10"}`: an ECDSA P-256 signature, and the ID of the key that made it.
- **Payload** decodes to `{"iss":"https://id.example.com","sub":"user-123","aud":"https://api.example.com","exp":1791900000,"iat":1791896400,"jti":"7f3c9a"}`: issued at 13:00 UTC on 13 October 2026, expiring 1 hour later.
- **Signature** is a placeholder in this example. In a real token it is the ES256 signature over the encoded header and payload, checked with the issuer's public key from its JWKS.
{{< /explainer >}}

## How the parts fit together

The header and payload are JSON objects. Each is encoded with base64url, a URL-safe variant of base64 without padding, and the two results are joined with a dot. The signer signs that string with the algorithm named in the header and appends the base64url-encoded signature after a second dot. That is the JWS compact serialization from RFC 7515.

A verifier reverses the steps: split at the dots, decode the header, pick the key and algorithm it allows, and verify the signature over the first 2 parts exactly as received. Only then does it decode the payload and evaluate the claims. The essays on [the purpose of JWT]({{< ref "/post/purpose-of-jwt" >}}), [JSON Web Algorithms]({{< ref "/post/jwa" >}}) and [JWT versus OAuth 2.0]({{< ref "/post/jwt-vs-oauth" >}}) go deeper.

## Related

- [How does OAuth 2.0 Token Exchange keep provider tokens away from agents?]({{< ref "/knowledge-base/agent-identity/token-exchange" >}})
- [Where do OpenID Connect implementations break?]({{< ref "/knowledge-base/oidc/oidc-security" >}})
