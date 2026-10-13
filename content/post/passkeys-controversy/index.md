---
id: jb-passkeys-controversy
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['identity-authentication']
imageDecorative: true
title: "Passwordless: Critical Notes on FIDO2 Passkeys"
linkTitle: "Passwordless: Critical Notes on FIDO2 Passkeys"
description: "Critical notes on passwordless authentication with FIDO2 Passkeys. Potential risks and challenges of passkey concepts & implications for users."
excerpt: "Explore the untold story of FIDO2 Passkeys and delve into the potential risks and challenges of the hyped passwordless authentication approach. Uncover the dark side of this innovative technology and gain valuable insights into its implications for users and online services alike."
lead: "Knowledge vs. Possession and other Passkey Controversies"
slug: "fido-passkeys"
date: 2023-05-08
lastmod: 2025-06-09
draft: false
weight: 50
image: fido-passkeys.webp
categories: ["identity-access-management"]
tags: ["password-security", "passwordless", "passkeys"]
pinned: false
homepage: false
keywords: ""
aliases: []
---

Passkeys are currently on everyone’s lips, thanks to recent announcements to enable Passkeys for authentication on Google accounts. And, while the passwordless hype train did not stop in front of my desk either, there are some problems surrounding the imminent password killer, disregarded mainly by the relatively uncritical media coverage. In this essay, I'll consider some of the biggest concerns.

I briefly mentioned Passkeys in my recent piece about [passwordless authentication]({{< ref "/post/passwordless-authentication/index.md" >}} "Passwordless Authentication: The Future of Cybersecurity"), so I'll keep this introduction brief. Let's get started!

## Introduction to FIDO2 & Passkeys

The FIDO Alliance developed FIDO2 as an open standard that enables secure and user-friendly passwordless authentication. One of FIDO2's key goals is to provide passwordless authentication, removing the need for users to remember and manage multiple passwords. [Members of the FIDO Alliance](https://fidoalliance.org/members/) include the whole Big Tech ecosystem, from 1Password through Amazon, Apple, Google, Meta, and Microsoft, as well as Yahoo and Yubico.

### Phishing-resistant Passwordless Authentication

[The FIDO master plan](https://media.fidoalliance.org/wp-content/uploads/2022/03/How-FIDO-Addresses-a-Full-Range-of-Use-Cases-March24.pdf) is to turn every mobile phone into a phishing-resistant, roaming authenticator by augmenting the FIDO WebAuthn specs with a protocol that uses Bluetooth to communicate between the FIDO authenticator (a mobile phone) and the device from which a user is attempting to authenticate. Specialized security keys (hardware tokens like YubiKeys) will be rendered obsolete.

The term *"Passkeys"* refers to the credentials used in this authentication procedure based on cryptographic concepts. Passkeys for FIDO2 allow users to authenticate themselves without entering a [long password]({{< ref "/post/password-length-recommendation/index.md" >}} "Password Length Recommendation: The Ultimate Guide to Strong Passwords"), lowering the risk of password-related security breaches.

### Public-Key Cryptography

Unlike many other passwordless login approaches, FIDO2 Passkeys provide a robust authentication mechanism immune to phishing attacks, man-in-the-middle, and replay attacks. This is accomplished through public-key cryptography, a cryptographic technique that employs two keys: a public key and a private key.

Data is encrypted using the public key and decrypted using the private key. In FIDO2 authentication, the private key is securely maintained on the user’s device, while the public key is registered with the online service. The Passkeys protocol defines proof of possession challenges that allow holders of a public key to verify whether the authenticating actor owns the corresponding private key (possession factor). This is a more secure solution than traditional password-based authentication methods (knowledge factor) in most end-user use cases.

Even if your favorite e-commerce site or platform is compromised, malicious actors will only have access to the public component of your key pair, which they will find absolutely useless.

### Biometrics

Now that the most essential authentication proof is stored on a mobile device, FIDO experts anticipate that Big Tech companies will protect access to the private keys as they protect screen lock, with biometric authentication incorporated into the user’s personal device OS. Using Face ID, Touch ID, or any other equivalent facial recognition or fingerprint scanning technology on a Microsoft or Android device to gain access to the valuable private key material, which is then used to sign in with a relying party, effectively results in a multi-factor authentication (MFA) process, combining an inherence factor and a possession factor.

## Passkeys Controversies

### Possession & Biometrics over Knowledge

The most crucial conceptual objective of Passkeys is to shift the broad consumer market away from knowledge-based authentication systems and toward possession-based authentication systems. Although this is undoubtedly a quantum leap forward in account security, far-reaching repercussions may still need to be fully recognized.

For example, something only you know cannot be taken away as quickly as something physical that you own. A secret in someone's head cannot be found anyplace else and can only be gained from that individual. Of course, there's blackmailing, *"rubber-hose cryptanalysis,"* and other methods, but these appear to take much more effort than merely having access to an unlocked cellphone.

Losing that knowledge component makes you more vulnerable to police seizures of electronics and keys, for example. Forcing someone to give up a password is considered a violation of the Fifth Amendment to the United States Constitution by courts in the United States. However, forcing someone to unlock biometrically secured devices is entirely legal. A similar situation might exist in other jurisdictions as well.

While the combination of possession- and inherence factors that FIDO Passkeys promise provides a significant convenience advantage over password-based authentication methods, they appear less effective against close-proximity, physical attacks.

### Device Lock-in

Possession-based systems, in general, rely on tangible items that can be misplaced, stolen, or damaged, potentially locking users out of their accounts.

The FIDO Alliance anticipates that FIDO authenticator providers, particularly influential organizations who embed FIDO authenticators within their operating systems, will make the Passkeys consumer market usable by overcoming the difficulty of making FIDO credentials multi-device available.

Of course, for all of this to function, you'll need a reliable, modern computer or phone. This means owning a current iPhone, Pixel, or computer that supports Windows Hello, Apple Touch ID, or other biometrics. You also need multiple devices because you are only safe against single device failure if you have a backup device.

Passkeys are likely to be risky to use, if not utterly inaccessible to the poor, underprivileged, or anyone who does not own or operate their own devices.

### Vendor Lock-in

Vendor lock-in shouldn't be necessary by design, but it may be in reality. Even the FIDO Alliance does not guarantee interoperability when syncing the cryptographic keys of FIDO credentials between devices from different vendors. This is where the additional cross-device authentication Bluetooth protocol comes into play because FIDO believes that users will always have another (backup?) device nearby with all the necessary Passkeys.

This is at least a partial vendor lock-in and disregards the reality of life for many individuals outside of Silicon Valley.

### Proprietary-only

The FIDO Passkey standard deliberately excludes any explicit vendor agnosticism. Implementations still heavily rely on proprietary software embedded into Apple, Google, Microsoft, and others' devices and solutions. The general strategy results in Big Tech creating and overseeing the key storage. There are no OSS implementations for creating and exchanging keys yet.

As a result, the Passkey concept pushes data ownership one step closer to the Big Tech industry. Taking another vital element of informational self-determination out of the hands of end users by favoring possession- and biometric-based authentication factors over something that is actually available solely to the user is an intentional feature of Passkey rather than a flaw.

### 100% Trust in Big Tech

Although FIDO specifies [privacy principles](https://fidoalliance.org/fido-authentication/privacy-principles/) that must be followed in designing and implementing FIDO authenticators, clients, and servers, it is still determined how strictly these guiding principles will be enforced and by whom.

The fact that Passkeys is strengthening the need to trust massive tech corporations, whose business model frequently entails selling data and information, is critical. Having FIDO credentials, which basically log end-users into every service they use while vowing not to do evil with them, necessitates some level of trust by the users.

## Conclusion

FIDO2 Passkeys provide a passwordless authentication solution that is secure, user-friendly, and scalable. Unlike passwords, they provide increased protection against common threats and a better user experience for those who can afford it by utilizing public-key cryptography. While there are compelling reasons to join the password-killer bandwagon, and I honestly believe that Passkeys will solve many problems for the general "my password is password" end-user market, there is an undercurrent.

Despite being a multi-national tech industry association, some people see the FIDO Alliance and their Passkeys as another large Silicon Valley solution that doesn't care about all their users. Potential downsides, such as device dependence, compatibility, and interoperability difficulties, contribute to this debate and should be considered when advocating for FIDO2 Passkeys.

Given the widespread support and work that Big Tech is putting towards modern passwordless authentication, I am confident that adoption rates will skyrocket soon. And some security-conscious individuals will continue to place their stack of unique, complex passwords in a credible password manager with 2FA as a second line of defense rather than a select handful of Big Tech gatekeeping providers.

I advise everyone else to **wait until passkeys gain broader support** and for the ecosystem to mature before going all-in! Only switch to Passkey-only authentication once you know how it works, [how to set it up](https://www.elliotali.com/passkeys/ "An easy introduction to Passkeys"), and how to back it up.

## FAQs

### What is FIDO2?
The FIDO Alliance created FIDO2, an open standard to enable secure and user-friendly passwordless authentication using public-key cryptography.

### How do FIDO2 Passkeys work?
Upon registration, FIDO2 Passkeys produce a one-of-a-kind public-private key pair on the user's device. The public key is supplied to the web service, while the private key is kept protected on the device. During authentication, the machine uses its private key to satisfy a cryptographic challenge given by the service, and the service verifies the signature using the stored public key.

### What are the benefits of FIDO2 Passkeys?
FIDO2 Passkeys improve security, user experience, and scalability across various devices, platforms, and services.

### What are the potential drawbacks of FIDO2 Passkeys?
Device dependence, which could result in users losing access to their accounts if their device is lost or broken, and compatibility difficulties, as not all online services offer FIDO2 authentication yet, are potential downsides of FIDO2 Passkeys. Switching from knowledge to possession factors has its own set of issues.

### Can I use FIDO2 Passkeys on multiple devices?
Yes, FIDO2 Passkeys can be used on numerous devices as long as they support FIDO2 authentication and the online service supports multiple device registrations.
