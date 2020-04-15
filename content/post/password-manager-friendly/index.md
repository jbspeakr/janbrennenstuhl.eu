---
title: "How to: Password-Manager Friendly Login Forms"
linkTitle: "How to: Password-Manager Friendly Login Forms"
description: "Password Security | Use HTML features to create password-manager friendly login forms for a seamless user experience & enhanced web security"
excerpt: "In this article, I explore the importance of creating password-manager friendly login forms for a seamless user experience and enhanced web security."
lead: "Boosting password security by making it easier for your users to use password managers"
slug: password-security-manager-friendly
date: 2023-04-23
lastmod: 2025-06-08
draft: false
weight: 50
image: effortless-login.webp
categories: ["identity-access-management"]
tags: ["password-security", "password-manager"]
pinned: false
homepage: false
---

Do you ever get tired of manually typing in your login credentials every time you need to access an online account? Luckily, there is a solution: password managers. These handy tools can automatically generate and store strong passwords, but they're only truly useful if  login forms are password-manager friendly. In this article, I explore how you can make your login forms more compatible with password managers to improve the user experience and enhance security. So, let's dive in and unlock the key to effortless login!

## What is a password manager?

A password manager (PWM) is powerful a software application designed to help users store and manage their login credentials and other sensitive information securely. It typically works by generating strong, unique passwords for each of the user's online accounts and storing them in an encrypted database. The user only needs to remember a single master password or use other authentication methods such as biometrics to access the PWM, and it can automatically fill in the login details for the user when they visit your website or application. This can help users avoid the pitfalls of weak, reused, or easily guessed passwords, and enhance the overall security of their digital identities.

If you want my recommendation for one of the best password managers, I've always used [1Password](https://1password.com).

## Understanding the limitations of traditional login forms

The internet seems to be full of sites that do things that are very unfriendly to users of a PWM. Common mistakes include disabling copy-pasting (or autofill) features or enforcing [dumb password composition policies](https://dumbpasswordrules.com/sites/).

Just imagine you're in a hurry to purchase that limited pair of sneakers online and need to create an account to complete the transaction. You type in your email address and password, only to realize that the site's password requirements are arbitrarily strict and your usual password composition strategy doesn't meet them. Frustrated, you spend precious minutes creating a new password that you know you'll probably forget later.

With modern password manager support, your login form could have easily supported a users PWM with generating a strong, unique, suitable password in seconds and saved it for future use. As identity providers and login form maintainers we must make using a password manager on our sites as easy as possible!

## Best practices for designing password-manager friendly login forms

**Form element improvements** – To improve the ease of use of password managers on your site make sure that you help browsers and tooling to autofill the password for the correct input field. Although some browsers can find the correct input heuristically even if the login form is not optimized for this purpose, web developers should correctly annotate HTML `input` elements using the `autocomplete` attribute.

For example, the account creation form should indicate that it's expecting a new password and that the password generator should create a new password for this input:

```html
<input type="password" autocomplete="new-password" id="new-password" …>
```

In context of user authentication, the login form should explicitly indicate that it's expecting the email address and the current password for the user:

```html
<input type="email" autocomplete="email" id="email" …>
<input type="password" autocomplete="current-password" id="current-password" …>
```

**Strong password policies** – Balancing effortless login with improved password security means that arbitrary password composition policies are rightfully considered counter-productive and even harmful nowadays. Researchers and security experts suggest that the single most important characteristic of a password is its length.

Password length requirements can directly be added to the password `input` element using the `pattern` attribute:

```html
<input type="password" pattern=".{12,70}" autocomplete="new-password" id="new-password" …>
```

This length requirement pattern will tell password managers to generate and autofill a new random password of at least 12 characters. While for many manually typing users without an automated password generator this is still achievable, it means to somewhat mis out on the great capabilities of password managers.

Luckily there is a way to have your login form tell 1Password, or other tools generating passwords for you, to apply [a way more elaborate password policy]({{< ref "/post/password-policy/index.md" >}} "How to create a strong password policy") using the `passwordrules` attribute on the `input`:

```html
<input type="password" passwordrules="minlength: 52; maxlength: 70; required: lower; required: upper; required: digit; required: [-];" …>
```

Password managers like 1Password, will now auto-generate a complex password of at least 52 character length and including a good mixture of character classes.

Although the `passwordrules` attribute [is still a proposal](https://github.com/whatwg/html/issues/3518), 1Password recommends to [provide these password requirements](https://developer.1password.com/docs/web/compatible-website-design/#provide-password-requirements).


{{< details "<strong>A Well-Known URL for Changing Passwords</strong>" open >}}
Password managers can warn users about [breached credentials]({{< ref "/knowledge-base/account-security/compromised-credentials/index.md" >}} "How to check for compromised credentials?!"), but the lack of account security industry standards results in a lot of friction when asking users to change password. The [change password URL standard by W3C](https://w3c.github.io/webappsec-change-password-url/) solves that problem by defining a well-known URL that sites and service provider can use to make their change password forms discoverable by automated tools: `/.well-known/change-password`

If you use the 1Password browser extension like I am, that leads to a really nice experience. Your users will be happy!
{{< /details >}}

## Improving accessibility with password-manager friendly login forms

Applying modern password security best practices on your sites and making your account creation and authentication forms more password manager friendly is possible and will result in effortless login experiences for your users. Automated login and form-filling features will have huge time-saving benefits for users with password managers.

Actively supporting PWMs in authentication processes will resolve your users from friction by leveraging more automation. Users will gladly benefit from simplified password management across multiple accounts and platforms.

## Increasing security with password-manager friendly login forms

Becoming password-manager friendly will directly result in more super strong passwords being used by your customers. Moving the responsibility of generating strong, complex passwords from the users to their password managers enables identity providers and account security experts to truly leverage the advantages of complex password composition policies and length requirements.

Helping password managers to better help your users means increasing protection against common threats not only for your users but also for your service or site. Improved overall security is a direct consequence.

## Conclusion

While we wait for the emerging technologies and techniques like [passwordless authentication]({{< ref "/post/passwordless-authentication/index.md" >}} "Passwordless Authentication – The Future of Login") and [FIDO Passkeys]({{< ref "/post/passkeys-controversy/index.md" >}} "Critical Notes on Passkeys") to become commodities and eventually resolve us from simple password schemes, we can and should make passwords easier to use. Getting rid of outdated and frustration-prone password policies while investing on making login forms more password manager friendly is a must for identity providers and web developers maintaining authentication experiences.

With modern form element improvements like `autocomplete`, `pattern` and `passwordrules` attributes, your sign-in process will become best friends with many password managers out in the wild!

Feel free to [drop me message on Mastodon](https://infosec.exchange/@jbspeakr) if you have any suggestions or comments!
