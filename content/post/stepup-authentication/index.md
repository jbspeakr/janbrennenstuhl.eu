---
title: "Step-Up Authentication: Elevating Security with OpenID Connect (OIDC)"
linkTitle: "Enhancing Security: A Guide to Step-Up Authentication"
description: "Delve into this guide on Step-Up Authentication using OpenID Connect. Learn to balance security with friction & how to elevate authentication levels."
excerpt: "Discover how Step-Up Authentication and OpenID Connect (OIDC) join forces to revolutionize online security, offering a seamless user experience while fortifying digital identity protection like never before."
lead: "Finding a balance between security and friction"
slug: step-up-authentication
date: 2023-05-14
lastmod: 2023-06-03
draft: false
weight: 50
image: step-up-authentication.webp
categories: ["identity-access-management"]
tags: ["oidc", "passwordless", "defensive-security", "ux-security"]
pinned: true
homepage: false
keywords: "step up authentication, adaptive challenges, adaptive challenge, adaptive authorization, adaptive authentication"
---

Security measures are effective when they cause the least friction while providing the highest level of security necessary for the targeted, user-friendly business process. Asking for too little gives users (or whoever is posing as them) too much freedom, but asking for too much, especially up front, generates obtrusive friction.

Minimal friction is essential to success, especially in conversion-sensitive flows like sales funnels. Services or apps are meant to be simple to access, and customers who want to utilize a product or purchase within as little time as possible may do so with as little friction. Making authentication even slightly more complicated risks alienating prospective customers.

## What is Step-Up Authentication?

Step-up authentication is one way of balancing friction and security that has received much attention and application in recent years. Step-up authentication ensures that users can access specific resources or execute the most typical actions with a single set of credentials. Users will be prompted for additional authentication factors when requesting to access sensitive resources or initiating privileged operations.

### The Rationale Behind Step-Up Authentication

Step-up authentication aims to tailor identity requests to the value of the resource and the local risk level and anticipated impact if it is compromised. By enabling risk-based authentication, step-up authentication allows organizations to provide easy access to one tier of non-critical resources while providing secure access to another.

As a result, security stays out of the way most of the time and only intervenes when further proofs of authenticity are absolutely required. This makes authentication work for both organizations and customers since both can be certain that their most sensitive resources are safe and secure.

It also opens new ways to conduct authorization by allowing organizations to privilege access for paying users.

### Step-Up Authentication vs Single-Factor Authentication

Although ubiquitous, single-factor authentication (SFA) frequently falls short of offering adequate security against common identity attacks. This traditional approach, which usually requires only a username and password, is widely regarded as insufficient due to its susceptibility to breaches ranging from brute-force attacks like [password spaying]({{< ref "/post/password-spraying/index.md" >}} "What is Password Spraying, How It Works & How to Prevent It") to phishing schemes.

In contrast, step-up authentication provides a more dynamic and context-sensitive security barrier. Instead of depending on a single, static layer of protection, it adjusts to changing risk levels by providing additional verification steps as needed. Step-up authentication provides a more sophisticated and scalable approach to security, delivering a higher level of protection without losing user convenience under normal conditions.

### Step-Up Authentication vs Multi-Factor Authentication

In many security-conscious environments, multi-factor authentication (MFA) has become the gold standard, requiring users to present a second factor (or multiple authentication factors) to access their online accounts. While MFA considerably improves security over single-factor authentication, it may cause user annoyance, particularly if additional verification steps are required for every login or transaction, regardless of the associated risk.

Step-up authentication is a flexible form of multifactor authentication, adding additional security layers only when necessary, such as during high-risk transactions or unusual account activity. This method ensures essential security requirements and improves the user experience by reducing unnecessary disruptions.

### Step-Up Authentication vs Adaptive Authentication

Adaptive authentication, like step-up authentication, is a more intelligent, context-aware approach to account security. It dynamically increases the level of necessary user authentication based on a risk assessment of each individual login or access attempt, considering parameters like geolocation (e.g., impossible travel), [IP reputation, device characteristics, and behavior patterns]({{< ref "/knowledge-base/account-security/reinforced-authentication/index.md" >}} "Reinforced Authentication: Studies Redefine Account Security"), or user's risk profile.

However, there is a subtle distinction between the two. While responding to perceived risks, step-up authentication often initiates additional authentication processes in predetermined conditions and based on static risk assessments, such as when a user attempts a high-value transaction.

In contrast, adaptive authentication uses advanced risk analysis algorithms, sometimes powered by artificial intelligence or machine learning, to assess the need for extra real-time authentication steps. While both give a more personalized and responsive approach to security compared to previous static techniques, Adaptive Authentication provides a more granular and automated risk assessment, possibly providing a higher level of protection and user experience when applied successfully.

## How Step-Up Authentication Works

Step-up authentication generally requires multiple stages of verification. When a user initiates an action that requires enhanced security, such as accessing confidential documents or conducting financial transactions, the system prompts the user for multi-factor authentication. This step up can manifest itself in a variety of ways, including, but not limited to:

- **Two-Factor Authentication (2FA)** – To verify a user's authenticity, this method combines something the user knows (e.g., a password) with something the user owns (possession factor), such as a unique code generated by a mobile app.
- **Biometric Authentication** – Biometric authentication delivers high security and convenience for users by using unique biological traits (inherence factor) such as fingerprints, facial recognition, or iris scans.

## Implementing Step-Up Authentication

In traditional authentication systems, step-up authentication was handled by integrating the relevant business logic within the web applications. Custom engineering efforts and heterogeneous implementations could have used more resources by neglecting to reuse well-tested code and incurring ongoing maintenance costs. Still, they also increased the possibility of security flaws.

Since federation protocols like OpenID Connect (OIDC) are becoming increasingly popular for modern applications that want to improve security by relying on a reliable identity provider, there are also better, standardized options for implementing step-up authentication.

### Step-up Authentication with OpenID Connect

OIDC is [an open standard](https://openid.net/specs/openid-connect-core-1_0.html "OpenID Connect Specification") with built-in support for relying parties (RP) that require more potent authentication methods (AMR) to be used depending on the authentication context classes. Because conventional federation protocols such as OIDC are business context agnostic and do not track every user interaction, business apps must initiate step-up scenarios independently.

### Forced Re-Authentication Methods

Following successful authentication, IdPs frequently provide long-running login sessions bound to user agents. The goal is to eliminate consumer friction by removing the need for regular active credential authentication. However, depending on an RP’s local risk assessment, certain business operations may require the most recent functional proof of authenticity check to be no more than a particular period old.

Relying parties use the optional authentication request variable `max_age` to communicate session age expectations to an IdP service. OIDC-compliant IdPs ensure that all session age requirements are met by requiring authentication as needed.

```bash
GET /authorize? 
	response_type=code 
	&scope=openid%20profile%20email 
	&client_id=s6BhdRkqt3
	&state=af0ifjsldkj 
	&redirect_uri=https%3A%2F%2Fclient.example.org%2Fcb 
	&max_age=300 HTTP/1.1 
Host: server.example.com
```

Requiring re-authentication of existing sessions every time a user attempts to access sensitive information or protected areas of an application adds friction to the user experience. Session elevation can be used to successfully achieve a balance between a smooth user experience and security considerations.

The authentication context class concept allows apps to build such scenarios and coordinate with an identity provider (IdP) for smooth step-up service in a declarative policy-driven method.

### Authentication Context Class Reference (ACR)

The optional authentication request parameter `acr_values` is a space-separated list of ACRs that determines the client application’s minimum degree of authentication. If the parameter is present, the IdP takes all measures necessary to verify and match the requested class. Users may be asked to re-authenticate using additional or different authentication methods to achieve this objective.

The authentication context class met by the completed identity authentication is returned as the ACR claim value within the provided identity token, which can then be utilized for authorized purposes by the RP.

ACR values and their semantics must be established, aligned, and documented between IdP and RPs out of the band. Only then business owners effectively employ them to precisely determine what ACR relates to the local risk assessment of their specific business operations.

### Authentication Level Elevation

Access to sensitive information and operations must be logged appropriately and authorized by resource servers. Verifying the validity of the provided bearer token is required to ensure that a client is eligible to undertake a specific operation.

The goal of session authentication and assurance level elevation is to provide a relatively seamless user experience by maintaining a minimum level of assurance for a user session when the user first authenticates to the application and then raising their authenticity levels based on local risk assessments:

1. Assuming that a user successfully established a session after [logging in with a username and password]({{< ref "/post/password-manager-friendly/index.md" >}} "How to Make Your Login Forms Password-Manager Friendly") and now attempts to access a sensitive resource, they are prompted to apply extra authentication factors.
2. The session is upgraded to a higher assurance level after a successful step-up using an additional authentication method.
3. Because their session is already at the raised authentication levels, no extra authentication challenge will be prompted the next time users enter the sensitive section within the specified duration.

```bash
GET /authorize? 
	response_type=code 
	&scope=openid%20profile%20email 
	&client_id=s6BhdRkqt3
	&state=af0ifjsldkj 
	&redirect_uri=https%3A%2F%2Fclient.example.org%2Fcb 
	&acr_values=mfa 
	&max_age=300 HTTP/1.1 
Host: server.example.com\
```

## Conclusion

Step-up authentication aims to adapt authentication requirements to the significance associated with a resource and the level of risk if it is exposed. It is one way to strike a balance between friction and security by allowing customers to continue using already known, established, and understood authentication concepts (username and password, for example) to access regular resources while prompting them for additional proof of authenticity and a different form of two-step authentication (such as confirmation via email or push notifications) in the context of more sensitive business operations (such as financial transactions or accessing sensitive data).

Enabling session authentication level elevation and step-up authentication can resolve the target conflict of providing customers with a smooth experience on the one hand and enforcing more significant security standards for specified operations or resources on the other.

## Frequently Asked Questions (FAQs)

### What are the minimum requirements to implement Step-Up Authentication?

First and foremost, a reliable and secure primary authentication mechanism, such as a secure password system or biometric identification method, is essential. Second, an additional authentication method, such as text message verification, email confirmation codes, security questions, or biometric checks, must be available and compatible with the user base.

The user’s technological capabilities and the amount of security required to determine which to utilize. Third, an effective risk assessment system must be established to detect circumstances requiring more verification. Finally, to support all the complex procedures involved in step-up authentication, an IT infrastructure that is both adaptable and secure is necessary.

### How does Step-Up Authentication improve user experience?

Step-up authentication is intended to improve the user experience by requiring further verification only when necessary. Step-up authentication, as opposed to standard static multi-factor authentication, which requires additional steps every time a user signs in or performs specific actions, only increases security measures in the context of higher-risk activities.

This means that for most ordinary actions, consumers may enjoy a frictionless, seamless experience without being burdened by additional security precautions. However, when it comes to more sensitive procedures, such as changing personal information or completing large transactions, consumers can welcome the added degree of protection, knowing their accounts and data are secure. 

### How can Step-Up Authentication prevent data breaches?

Step-up authentication is a powerful technique that adds complexity and layers to the authentication process. Step-up authentication adapts to the perceived risk level of a user’s activity. This means that even if an attacker successfully steals or guesses a user’s primary credentials, they will still face additional, often unanticipated, obstacles before getting access. Many cyberattacks are deterred by this since it considerably increases the work and skill required to compromise an account.