---
title: "JWT vs OAuth 2.0: Understanding the Key Differences"
linkTitle: "JWT vs OAuth 2.0: Understanding the Key Differences"
description: "Learn the key differences between JWT and OAuth 2.0 from our expert guide on JWT vs OAuth. Understand which one to choose for authentication."
excerpt: "The interplay of tokens and protocols has fundamentally transformed how we authenticate, authorize, and securely communicate data over the Internet. Two important players in this realm are JSON Web Tokens (JWT) and OAuth 2.0. Though they serve different purposes, there's often confusion about their functionalities and application. How do they differ? Can one replace the other?"
lead: "JSON Web Token as Stateless Bearer Tokens"
slug: "jwt-vs-oauth"
toc: true
aliases: []
date: 2023-05-24
lastmod: 2023-05-28
draft: false
weight: 50
image: jwt-vs-oauth.webp
categories: ["identity-access-management"]
tags: ["jwt", "oidc", "oauth2"]
pinned: false
homepage: false
keywords: "jwt vs oauth"
---

## TL;DR

- **OAuth 2.0** is an open standard that describes an authorization framework. It allows a third-party application to access a user’s resources without user credentials.
- **JWT** (JSON Web Tokens) is a standard that describes a JSON-based token format used to securely transfer information between two parties across an insecure environment.
- **Combining OAuth 2.0 and JWT:** JWT can be integral to the [OAuth 2.0 framework]({{< ref "/tags/oauth2/" >}} "OAuth 2.0 in Action") . In fact, JWT has often been used as the bearer token in OAuth 2.0 implementations.
- **OpenID Connect (OIDC):** Modern authentication and authorization mechanisms leverage the OAuth 2.0 fundamentals with JWT tokens by following [OpenID Connect]({{< ref "/tags/oidc/" >}} "OpenID Connect: Streamlining User Authentication & Identity") protocols.

## Introduction to JWT vs OAuth 2.0

Most people encounter OAuth2 and JSON Web Tokens (JWT) in the context of authentication and authorization for web applications. While both concepts nowadays get used together, comparing **OAuth2 vs JWT** is like comparing apples to kittens.

10 years after the last update to the OAuth 2.0 Authorization Framework standard ([RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749 "The OAuth 2.0 Authorization Framework")) and over eight years after JSON Web Tokens got unleashed to the world, there is still a lot of confusion around these two widespread open standards among software engineers and security engineering novices. In this article, I will explain why comparisons like *"JWT vs OAuth 2.0"* or questions like *"OAuth vs JWT which is best"* make little sense.

### What is OAuth2?

OAuth2 is an open standard describing an authorization framework that allows a third-party application to access a user's resources without giving them the user's credentials. The keywords here are **authorization protocol** and **delegated access**. It does this by providing the concept of **access tokens** that can be used by a client application to access protected resources (like an API) exposed by a resource server on behalf of the resource owner (a user). These opaque tokens are issued by an authorization server after the user grants permission to the third-party application.

### What is JWT?

On the other hand, the JWT standards describe a **JSON-based token format** and how it can **securely transfer information** between two parties across an insecure environment (like HTTP or HTTPS). Their multipart JSON format structure allows JWTs to carry **custom claims** as payloads and additional cryptographic accessories. They are self-contained and usually occur in their JSON Web Signature form, signed with a secret key or public/private key pair. I wrote about "[The Purpose of JWT]({{< ref "/post/purpose-of-jwt/index.md" >}} "The Purpose of JWT: Stateless Authentication")" a few years ago.

## When to Use OAuth 2.0 vs When to Use JWT

**Use OAuth 2.0 with HTTPS when authorizing third-party access.** 

OAuth 2.0 is a protocol that allows users to grant limited access to resources on one site, such as Facebook, to another location or application, without sharing their credentials or giving them complete control over their account. It provides a secure way of authorizing third-party access to your resources by using access tokens in the form of bearer tokens.

After the resource owner grants permission for the client application to access their resources using OAuth2, the responsible authorization server issues the proof of authentication. These tokens are then sent with each request made by the client application to the resource server, verifying them and granting or denying access based on the services requested and claims provided.

Bearer tokens are a type of access token that can be used by arbitrary parties in possession of them to gain access to the protected resources they represent. They do not contain any cryptographic proof of authenticity other than possession itself, so they must be kept secret and transmitted securely.

OAuth 2.0 is an excellent choice when you must permit controlled interaction between third-party applications or services managed by different entities or individuals with your system without compromising sensitive information or risking unauthorized access. This is possible through various security mechanisms such as opaque tokens, bearer tokens, identity servers, and refresh tokens.

**Use JWT when securely transmitting information between parties in a stateless form.**

JSON Web Tokens are basically use cases agnostic and can generally be used for securely transmitting information between parties in stateless form. It provides a simple way of representing claims (e.g., user identity, permissions) as JSON objects that can be signed and/or encrypted using industry-standard algorithms.

JWTs are often used for transporting proof of authenticity across multiple domains or applications without storing session data on the server side, significantly contributing to performance. They are also helpful for implementing single sign-on (SSO) functionality, where a user logs in once and gains access to multiple applications or services without claiming their identity again. And this is basically where OAuth 2.0 and JWT touch on each other.

## Combining OAuth 2.0 and JWT: How to Use Them Together

The apparent overlap between JWT and OAuth 2.0 springs from a misunderstanding of their distinct roles in digital communications. JWT can be an integral part of the OAuth 2.0 framework. In fact, JWT often serves as the bearer token in OAuth 2.0 implementations, becoming the vehicle by which authorization information is conveyed.

### JWT as Bearer Token

JWTs can be used by an app as [OAuth2 bearer tokens](https://www.rfc-editor.org/rfc/rfc6750 "The OAuth 2.0 Authorization Framework: Bearer Token Usage (RFC)") to enable stateless authentication and local authorization by a resource server to grant access to a protected resource.

**Bearer tokens are a type of token** that is widely used in authentication protocols like OAuth 2.0. They are used to grant access to protected resources, and they come in two types: access tokens and refresh tokens. While access tokens are short-lived, refresh tokens can be renewed, allowing users to maintain their session for an extended period.

JWTs are often used in combination with OAuth 2.0 as a means of transmitting state and user data (claims) between the authorization server and the resource server. They can also be used for client-side authentication, where a JWT is issued by an **identity provider** after successful login and then sent to the client application, which uses it to authenticate itself on behalf of the actual user with other services.

### Advantages of Using JWT with OAuth 2.0

One significant advantage of using JWT with OAuth 2.0 is eliminating the need for multiple tokens for different app purposes. One token can contain all the necessary information for authentication and authorization purposes.

Another benefit can be improved performance through stateless authentication. Since [JWT tokens](https://auth0.com/learn/json-web-tokens "Get Started with JSON Web Tokens") are self-contained and signed with a secret key or public/private key pair, there is less reliance on external servers for validation and introspection. JWT is very suitable for stateless applications as they relieve the server side from the need to store any particular session data between requests from the clients.

Instead, all necessary data is carried around within each JWT token itself, making it easy for clients and servers alike to verify its authenticity without looking up anything outside of it. This reduces the number of database lookups required during token verification, leading to faster response times, increased reliability due to fewer bottlenecks, and a potentially cleaner architecture.

## Which Bearer Token Format is Right for You?

Choosing the suitable OAuth 2.0 access token format can be a daunting task. Both **stateful tokens** and **stateless JWT** have their strengths and weaknesses. It ultimately depends on specific use cases, requirements, and infrastructural preconditions.

Modern authentication and authorization mechanisms leverage the **OAuth 2.0 fundamentals** together with JWT tokens by following **OpenID Connect** (OIDC) protocols, which is an extension on top of OAuth 2.0 that introduces the concept of an identity provider (aka identity server) and uses JWTs instead of opaque tokens.

## JWT + OAuth2 = OpenID Connect (OIDC)

Big tech organizations such as Google, Facebook, and Microsoft are OIDC power users:

- [Google Identity uses OIDC](https://developers.google.com/identity/openid-connect/openid-connect "Google's OAuth 2.0 APIs") and its identity token to transport user details.
- [Facebook also uses OIDC with JWTs](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-oidc "OIDC Tokens in Facebook Login") in its Graph API authentication mechanism.
- [Microsoft's Azure Active Directory](https://learn.microsoft.com/en-us/azure/active-directory/develop/access-tokens "Microsoft identity platform access tokens") (AAD) also leverages the JWT token to implement OIDC.

Whether you choose classic OAuth 2.0 with opaque, non-JWT tokens, OAuth 2.0 with JWT bearer token, or OIDC, make sure you understand how these frameworks work under the hood, embrace their core concepts and get your implementation externally certified to ensure maximum security for your users' data while also providing seamless access to your application's features and resources. The better way, however, is to outsource the authentication to Google, Microsoft, Okta, or someone else and let them deal with all the nifty little details in these specifications.

## Conclusion: Choosing Between JWT and OAuth2

Combining OAuth 2.0 and JWT can give you the best of both worlds. OpenID Connect is built on both open standards, embracing OAuth 2.0 concepts to **delegate access with external services** while using JWT as a bearer to **transport claims from the authorization server** to resource servers for stateless authorization.

JWTs allow client-side introspection of ID tokens, enable resource server serving APIs to verify access tokens locally, and even be used as refresh tokens. Although slightly controversial, JSON web tokens are versatile and can be used [as one-time token]({{< ref "/post/single-use-jwt/index.md" >}} "Single-Use JWT: The Power of Stateless One Time Token") (OTT).
