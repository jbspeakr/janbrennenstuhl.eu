---
id: jb-guide-password-policy-requirements
title: "What should a password policy require?"
linkTitle: "Password policy requirements"
description: "What NIST SP 800-63B-4 requires from a password policy, and a checker that compares your own policy against it."
answer: "Under NIST SP 800-63B-4, a password used on its own must have at least 15 characters, or 8 when it is one factor of multi-factor authentication, and systems should accept at least 64. Composition rules, forced periodic changes, hints and security questions are out; a blocklist of common and breached passwords is in."
claim: "NIST SP 800-63B-4 sets a 15-character minimum for single-factor passwords, forbids composition rules and periodic changes, and requires blocklist checks and support for password managers."
slug: password-policy-requirements
date: 2026-10-13
draft: false
weight: 15
topics: [passwords]
scripts: [password-policy]
---

## Key findings

{{< finding id="nist-min-length-15" source="NIST SP 800-63B-4, Section 3.1.1.2" url="https://pages.nist.gov/800-63-4/sp800-63b/authenticators/" >}}NIST SP 800-63B-4 requires passwords used as the only authentication factor to be at least 15 characters long, and at least 8 when the password is used only as part of multi-factor authentication.{{< /finding >}}

{{< finding id="nist-no-composition-no-rotation" source="NIST SP 800-63B-4, Section 3.1.1.2" url="https://pages.nist.gov/800-63-4/sp800-63b/authenticators/" >}}Verifiers shall not impose composition rules such as mixing character types, and shall not require periodic password changes, but shall force a change when there is evidence of compromise.{{< /finding >}}

{{< finding id="nist-blocklist-with-reason" source="NIST SP 800-63B-4, Section 3.1.1.2" url="https://pages.nist.gov/800-63-4/sp800-63b/authenticators/" >}}A new password shall be compared in full against a blocklist of commonly used, expected or compromised passwords, and a rejected user shall be told why.{{< /finding >}}

{{< finding id="nist-password-managers" source="NIST SP 800-63B-4, Section 3.1.1.2" url="https://pages.nist.gov/800-63-4/sp800-63b/authenticators/" >}}Verifiers shall allow password managers and autofill, should permit paste, and should accept passwords of at least 64 characters.{{< /finding >}}

## Evidence

{{< studies caption="Sources" >}}
{{< study title="NIST SP 800-63B-4: Digital Identity Guidelines, Authentication and Authenticator Management" org="NIST" year="2025" sample="n/a" method="Standard" url="https://pages.nist.gov/800-63-4/sp800-63b/authenticators/" >}}Section 3.1.1.2 sets the password verifier requirements summarized here.{{< /study >}}
{{< study title="SP 800-63B-4 Appendix A: Strength of Passwords" org="NIST" year="2025" sample="n/a" method="Informative appendix" url="https://pages.nist.gov/800-63-4/sp800-63b/passwords/" >}}Explains why length and blocklists matter more than composition rules.{{< /study >}}
{{< /studies >}}

## What to do

### For engineers

- Set the minimum by how the password is used: 15 characters where it is the only factor, 8 only where a second factor is always required.
- Accept long passwords and verify them in full; the essay on [long password support]({{< ref "/post/long-password-support" >}}) covers hashing limits and denial-of-service concerns.
- Replace composition rules with a blocklist check against breached and common passwords. The field-guide entry on [stolen credentials]({{< ref "/knowledge-base/account-security/compromised-credentials" >}}) covers privacy-preserving breach checks.
- Make forms work with password managers: the right `autocomplete` values and no paste blocking. See [password-manager friendly login forms]({{< ref "/post/password-manager-friendly" >}}).

### For product and UX

- Explain a rejection in plain words ("this password appears in known breaches") instead of listing rules after the fact. NIST requires a reason.
- Drop scheduled password expiry. Forced changes are for evidence of compromise, which makes them rarer and easier to explain.
- My [2023 password policy essay]({{< ref "/post/password-policy" >}}) recommended at least 12 characters. For passwords used on their own, the final SP 800-63B-4 now sets 15.

## Check your policy

{{< explainer "password-policy" "Compare a policy with SP 800-63B-4" >}}
The checker on this page compares the settings of a password policy with the requirements below. Without JavaScript, use the list as a checklist. "Shall" is a requirement, "should" a recommendation.

- **Shall:** at least 15 characters for single-factor passwords; at least 8 if the password is only one factor of MFA.
- **Should:** accept at least 64 characters, all printing ASCII characters, the space character and Unicode; count each Unicode code point as one character.
- **Shall not:** impose composition rules, such as requiring digits, symbols or mixed case.
- **Shall not:** require periodic password changes. **Shall:** force a change when there is evidence of compromise.
- **Shall not:** offer password hints to unauthenticated users, or prompt for security questions when a password is chosen.
- **Shall:** verify the whole password, never a truncated or partial one.
- **Shall:** check new passwords against a blocklist, and tell the user why a password was rejected.
- **Shall:** rate-limit failed authentication attempts.
- **Shall:** allow password managers and autofill. **Should:** allow paste and offer to show the password.
- **Shall:** store passwords salted and hashed with a suitable password hashing scheme, with a salt of at least 32 bits.
{{< /explainer >}}

## Related

- [Do password strength meters work?]({{< ref "/knowledge-base/account-security/password-policy" >}})
- [How common is password reuse?]({{< ref "/knowledge-base/account-security/password-reuse" >}})
- [Max password length: a secure password guide]({{< ref "/post/password-length-recommendation" >}})
