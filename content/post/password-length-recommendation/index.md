---
id: jb-password-length-recommendation
imageDecorative: true
title: "Password Length: The Minimum and Maximum NIST Recommends"
linkTitle: "Password Length: Minimum and Maximum"
description: "How long a password should be and how long a service should allow it to be, based on NIST SP 800-63B-4 and the OWASP cheat sheets."
claim: "A password used on its own should have at least 15 characters, a service should accept at least 64, and a maximum far above that is still reasonable to keep password hashing cheap."
excerpt: "How long a password should be and how long a service should allow it to be, based on NIST SP 800-63B-4 and the OWASP cheat sheets."
lead: "At least 15 characters for a password used on its own, at least 64 accepted by the service, and no composition rules."
slug: max-password-length
aliases: ["/max-password-length-recommendation/"]
date: 2023-05-04
lastmod: 2026-11-13
draft: false
weight: 50
image: max-password-length-guide.webp
tags: ["password-security", "password-manager"]
keywords: password length recommendations, max password length, recommended password length, minimum password length, maximum password length, nist password length
series: passwords
---

A password that is the only thing protecting an account should have at least 15 characters, and the service behind it should accept at least 64. Both numbers come from the US National Institute of Standards and Technology (NIST), and they are the numbers I recommend. In this article I explain where the numbers come from, why they are about length and not about special characters, and why a service may still set an upper limit.

{{< callout title="Update, November 2026: rewritten for the 2025 NIST guideline" >}}
I reworked this article with the help of a coding agent. The 2023 version was based on the NIST guideline from 2017 and recommended 12 to 16 characters. It also claimed that NIST asks for complex passwords, which was wrong then and is wrong now. This version follows the 2025 revision.
{{< /callout >}}

## What NIST and OWASP recommend today

<span id="password-length-recommendations"></span><span id="the-nist-guidelines"></span><span id="so-whats-the-ideal-length"></span>NIST published the fourth revision of its guideline on authentication, [SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ "NIST SP 800-63B-4: Authenticator and Verifier Requirements"), in 2025. It is written for US government systems, but OWASP and many others refer to it as well. Section 3.1.1.2 lists what a service that verifies passwords has to do. The OWASP [Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html "OWASP Authentication Cheat Sheet"), for example, repeats the same length numbers and names NIST as its source.

| Question | NIST SP 800-63B-4 |
|----------|-------------------|
| Minimum length when the password is the only factor | 15 characters |
| Minimum length when multi-factor authentication (MFA) is always required | 8 characters |
| Maximum length a service should at least accept | 64 characters |
| Rules such as "one digit, one symbol, one uppercase letter" | Not allowed |
| Checking only the first part of a long password | Not allowed |
| Forced password changes on a schedule | Not allowed |

The 64 in this table is easy to misread, and my 2023 version of this article was not clear about it either. NIST says services "SHOULD permit a maximum password length of at least 64 characters". A limit of 64 is therefore the smallest acceptable one, and a limit of 20 or 32 characters doesn't meet the guideline.

If you want to compare an existing policy against the full list of requirements, I keep a checker in my field-guide entry on [what a password policy should require]({{< ref "/knowledge-base/account-security/password-policy-requirements" >}} "What should a password policy require?").

## Why the guideline counts characters and not character types

<span id="a-look-into-password-length"></span><span id="complex-passwords--the-importance-of-unpredictability"></span><span id="how-does-password-length-affect-security--brute-force-attacks"></span>An attacker who steals a database of password hashes can try guesses on their own hardware, without any rate limit. In its appendix on the [strength of passwords](https://pages.nist.gov/800-63-4/sp800-63b/passwords/ "NIST SP 800-63B-4, Appendix A: Strength of Passwords"), NIST speaks of "many billions of hashes per second" for such offline attacks. Every additional character multiplies the number of candidates the attacker has to try, so length is what makes guessing expensive.

Composition rules were meant to have the same effect, but people respond to them in predictable ways. NIST gives this example:

{{< quote source="NIST SP 800-63B-4, Appendix A" url="https://pages.nist.gov/800-63-4/sp800-63b/passwords/" >}}
For example, a user who might have chosen "password" as their password would be relatively likely to choose "Password1" if required to include an uppercase letter and a number or "Password1!" if a symbol is also required.
{{< /quote >}}

Attackers know these patterns and try them first. For that reason NIST dropped composition rules and asks services to compare new passwords against a blocklist of common and breached passwords. I describe how such a policy could look in [How to Design a Strong & Usable Password Policy]({{< ref "/post/password-policy/index.md" >}} "How to Design a Strong & Usable Password Policy").

Length alone has limits. A long password that appears in a breach list, or that is reused on a second site, is still easy to guess. The same appendix also points out that phishing and keystroke logging work as well against a long password as against a short one.

## Why a service may still set a maximum

<span id="why-no-max-length"></span><span id="what-is-the-max-password-length-recommendation"></span>A stored password hash has the same size for a short and for a long password, so storage is no reason for a low limit. NIST still doesn't ask for unlimited input:

{{< quote source="NIST SP 800-63B-4, Appendix A" url="https://pages.nist.gov/800-63-4/sp800-63b/passwords/" >}}
Users should be encouraged to make their passwords as long as they want within reason. [...] However, extremely long passwords (perhaps megabytes long) could require excessive processing time to hash, so it is reasonable to have some limit.
{{< /quote >}}

Password hashing is slow on purpose, and for some algorithms the time grows with the length of the input. An attacker can abuse this by sending huge passwords to the login endpoint. The Django project had exactly this problem in 2013, and its [security release](https://www.djangoproject.com/weblog/2013/sep/15/security/ "Django security releases: denial-of-service via large passwords") rejected every password above 4096 bytes.

My reading is that the upper limit belongs somewhere between 64 characters and a few thousand. It should be so high that neither a person with a passphrase nor a password manager reaches it. In case you run a login system and want to know how to implement such a limit, read my article on [long password support]({{< ref "/post/long-password-support/index.md" >}} "How to Support Long Passwords in a Login System").

## What this means for your own passwords

<span id="creating-strong-passwords"></span><span id="use-a-password-manager"></span><span id="common-password-pitfalls"></span><span id="short-passwords"></span><span id="what-is-a-password-manager-and-how-can-it-help-me"></span>The NIST numbers are written for services, but they translate well to personal use. My recommendation is a password manager, and I use 1Password myself. A password manager generates a random password for every account and fills it in, so a length of 20 or 30 characters costs no extra effort. Set the generator to at least 15 characters, and to more where the site accepts it.

<span id="passphrases-a-password-manager-alternative"></span><span id="what-is-a-passphrase--how-is-it-different-from-a-password"></span>Some passwords have to be typed by hand, for example the one that unlocks your computer or the password manager itself. For those, a passphrase of several random words is easier to type than random characters and reaches 15 characters quickly. The words have to be random: a quote or a song line is something an attacker's word list may contain.

<span id="reusing-passwords"></span><span id="why-should-i-avoid-reusing-passwords"></span>A long password protects only the accounts it is not shared with. When a site leaks its passwords, attackers try the same email and password combination on other sites. I collected the numbers on that in [How common is password reuse?]({{< ref "/knowledge-base/account-security/password-reuse/index.md" >}} "How common is password reuse?").

<span id="writing-passwords-down"></span><span id="ignoring-two-factor-authentication"></span><span id="faqs"></span><span id="conclusion"></span><span id="additional-tips-for-strengthening-your-password-security"></span>Three more points follow from the guideline:

- Writing passwords down is acceptable if the note is stored safely. NIST says that recording passwords is "not necessarily vulnerable", although some ways of doing it are. [Troy Hunt](https://www.troyhunt.com/only-secure-password-is-one-you-cant/ "Troy Hunt: The only secure password is the one you can't remember") made the same argument years ago.
- A good password doesn't need to be changed on a schedule. Change it when there is a sign that it leaked.
- Length doesn't help against phishing. Turn on MFA where a site offers it, or use [passkeys]({{< ref "/post/passkeys-controversy/index.md" >}} "Passwordless: Critical Notes on FIDO2 Passkeys") if they fit your setup.
