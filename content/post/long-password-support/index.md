---
id: jb-long-password-support
imageDecorative: true
title: "How to Support Long Passwords in a Login System"
linkTitle: "How to Support Long Passwords"
description: "Where length limits hide in a login system, why bcrypt stops at 72 bytes, and how to set a single explicit maximum without truncating passwords."
claim: "Login systems should accept long passwords from users and password managers, hash them with Argon2id or scrypt, and still set an explicit maximum length to prevent hashing denial of service."
excerpt: "Where length limits hide in a login system, why bcrypt stops at 72 bytes, and how to set a single explicit maximum without truncating passwords."
lead: "Accept at least 64 characters, never truncate, and set a single explicit maximum on purpose."
slug: long-password-support
aliases: ["/long-password-login-system/"]
date: 2023-05-06
lastmod: 2026-11-13
draft: false
weight: 50
image: long-password-login-system.webp
tags: ["password-security", "ux-security"]
keywords: long password, login system, secure hashing
series: passwords
---

A login system should accept passwords of at least 64 characters, check every character of them, and reject input above a maximum that somebody chose on purpose. Often the limit was never chosen: a form attribute, a database column or the hash function sets it. In this article I go through the places where such limits hide and how I would replace them with a single explicit one.

{{< callout title="Update, November 2026: rewritten and shortened" >}}
I reworked this article with the help of a coding agent. The 2023 version was long and repeated itself, and it recommended keeping the old and the new password hash side by side during a migration, which leaves the weaker hash in the database. The hashing parameters and length numbers now follow the current OWASP cheat sheets and NIST SP 800-63B-4.
{{< /callout >}}

## Start with the two numbers

<span id="the-importance-of-password-security"></span><span id="the-rise-of-long-passwords"></span><span id="password-maximum-length-limitations"></span><span id="common-password-max-length-limits"></span><span id="the-consequences-of-short-password-limits"></span><span id="the-benefits-of-long-passwords"></span><span id="secure-password-enhanced-security-through-entropy"></span><span id="resistance-to-brute-force-attacks"></span>The US National Institute of Standards and Technology (NIST) sets both ends in [SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ "NIST SP 800-63B-4: Authenticator and Verifier Requirements"). The minimum is 15 characters when the password is the only factor, and 8 when multi-factor authentication is always required. For the maximum, services "SHOULD permit a maximum password length of at least 64 characters". I explain the reasoning behind these numbers in my article on [password length]({{< ref "/post/password-length-recommendation/index.md" >}} "Password Length: The Minimum and Maximum NIST Recommends").

A low maximum mostly hurts the users who do things right. A password manager can generate 40 random characters without effort, and a passphrase of five or six words is longer than 20 characters. The [Dumb Password Rules](https://dumbpasswordrules.com "A compilation of sites with dumb password rules") compilation collects many sites with such limits.

## Keep a maximum, but choose it yourself

<span id="maximum-password-length-why-do-length-limits-exist"></span><span id="long-password-denial-of-service"></span>Accepting passwords of any size is not the answer either. Password hashing is slow on purpose, and an attacker can use that against the server. The Django project described the problem in a [security release from 2013](https://www.djangoproject.com/weblog/2013/sep/15/security/ "Django security releases: denial-of-service via large passwords"). Django had no maximum length back then, and its default hasher needed more time for longer input:

{{< quote source="Django security release, 15 September 2013" url="https://www.djangoproject.com/weblog/2013/sep/15/security/" >}}
A password one megabyte in size, for example, will require roughly one minute of computation to check when using the PBKDF2 hasher.
{{< /quote >}}

A few such requests in parallel keep a server busy, and they don't need a valid account. Django's fix was to fail authentication for every password above 4096 bytes. NIST comes to the same conclusion in its [appendix on password strength](https://pages.nist.gov/800-63-4/sp800-63b/passwords/ "NIST SP 800-63B-4, Appendix A: Strength of Passwords"): users should be able to make passwords "as long as they want within reason", and "it is reasonable to have some limit".

I would pick the maximum between 64 characters and a few thousand bytes, write it into the password policy, and enforce the same value in every component that sees the password. A request size limit in front of the login endpoint is a good second line of defense, because it stops oversized input before it reaches the hasher.

## Check what the hash function accepts

<span id="how-to-support-long-passwords-in-your-login-system"></span><span id="updating-your-database-and-storage"></span><span id="adapting-to-longer-password-storage"></span><span id="the-importance-of-secure-hashing"></span>Long passwords don't need more storage. A password hash has the same size for 8 and for 800 characters, so the database column for the hash stays as it is. A column that still holds the password itself is a different and much bigger problem.

The hash function can set a limit of its own. The OWASP [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "OWASP Password Storage Cheat Sheet") currently recommends these settings:

| Algorithm | Minimum configuration (OWASP) | Input limit |
|-----------|-------------------------------|-------------|
| Argon2id | 19 MiB of memory, 2 iterations, 1 degree of parallelism | None that matters in practice |
| scrypt | CPU/memory cost 2^17, block size 8, parallelization 1 | None that matters in practice |
| bcrypt (legacy systems) | Work factor 10 or more | 72 bytes in most implementations |

The bcrypt limit is the one to watch. Many implementations silently ignore everything after byte 72. The limit counts bytes, while NIST wants every Unicode code point counted as a single character. A character can take up to 4 bytes in UTF-8, so a bcrypt system can't promise more than 18 characters to a user who types emoji. OWASP's advice for bcrypt is to enforce a maximum of 72 bytes.

A common workaround is to run the password through a fast hash such as SHA-256 first and to give the result to bcrypt. OWASP calls this approach dangerous, because the hash output can contain null bytes and because it enables an attack called password shucking. If I needed more than 72 bytes, I would move to Argon2id instead.

If you accept Unicode, NIST also suggests normalizing the password (NFC) before hashing. Otherwise the same password typed on two devices can produce two different byte sequences.

## Never truncate, in the form or on the server

<span id="implementing-front-end-changes"></span><span id="adapting-user-interface-elements"></span><span id="enabling-client-side-input-validation"></span><span id="back-end-considerations"></span><span id="implementing-server-side-password-validation"></span>NIST requires services to "verify the entire submitted password (e.g., not truncate it)". Truncation is dangerous because nobody notices it. The user believes the account has a 40-character password, while the system only ever checks the first 16.

The HTML `maxlength` attribute is the most common place where this happens. Browsers don't show an error when a pasted password is longer than `maxlength`. They cut the input, and the form submits the shortened value. If the sign-up form and the login form then use different values, the user can't log in with the password they just set.

I would leave `maxlength` off password fields, or set it well above the real maximum, and show a clear message when the input is too long:

```html
<input type="password" id="new-password" autocomplete="new-password" minlength="15" required>
<p id="new-password-error" hidden>Please use at most 256 characters.</p>
```

The 256 here is an example value. Client-side checks only help the user, so the server has to apply the same minimum and maximum again and reject a password that is too long. It must not shorten it.

<span id="testing--monitoring-your-updated-system"></span>A few test cases catch most mistakes: a password exactly at the maximum, a password a single character above it, and a password with multi-byte characters. Run them through sign-up, login, password change and password reset. Every component on the way, such as a gateway or a mobile app, has to pass the password on unchanged.

## Move existing users without a reset

<span id="transitioning-existing-user-data"></span><span id="ensuring-backward-compatibility"></span>Raising the maximum doesn't affect existing passwords, as all of them are shorter than the new limit. Changing the hash function needs more care, because a stored hash can't be converted.

The usual approach is to rehash at login. NIST recommends storing a reference to the hashing scheme and its cost factor with every hash "to allow migration to new algorithms and work factors". When a user logs in and the stored hash still uses the old scheme, the server verifies the password against it, computes the new hash from the password it just received, and replaces the old hash. Accounts that never log in keep the old hash, so plan what happens to them after a deadline.

One case needs a decision up front: a system that truncated passwords in the past. I haven't seen this covered by NIST or OWASP, so take it as my own reasoning. The stored hashes of affected users belong to the shortened password. Once the system checks the full password, these users fail to log in although they type the correct one. The server could retry a failed login with the old truncation rule for hashes that are marked as old, and rehash the full password when that retry succeeds.

<span id="encouraging-the-use-of-password-managers"></span><span id="password-manager-support"></span><span id="encouraging-strong-password-practices"></span><span id="best-practices-for-long-password-support"></span><span id="adopting-a-balanced-password-policy"></span><span id="regularly-reviewing--updating-security-measures"></span><span id="staying-informed-about-new-threats--trends"></span><span id="summary"></span><span id="frequently-asked-questions-faqs"></span>Long password support pays off most for users with a password manager. In case you want to learn how forms can tell a password manager which lengths and characters they accept, read [How to: Password-Manager Friendly Login Forms]({{< ref "/post/password-manager-friendly/index.md" >}} "How to: Password-Manager Friendly Login Forms"). The rest of a policy, such as blocklists and strength estimation, is covered in [How to Design a Strong & Usable Password Policy]({{< ref "/post/password-policy/index.md" >}} "How to Design a Strong & Usable Password Policy").
