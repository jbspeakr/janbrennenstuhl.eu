---
id: jb-bunny-shield-review
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['application-security']
imageDecorative: true
title: "Bunny Shield Review: 3 Things Need Improvement"
linkTitle: "Bunny Shield Review: 3 Things Need Improvement"
description: "I tested Bunny Shield by Bunny.net – Three things that need attention: False positives, bot management & observability."
excerpt: "Bunny Shield is really easy to use and makes the most of your first experience. It's a solid start for an accessible WAF, but there are a few key improvements needed to make it a production-ready web security product."
lead: "False positives, bot management & observability"
slug: bunny-shield-review
date: 2025-06-07
lastmod: 2025-06-22
draft: false
weight: 50
image: bunny-shield-preview-review.webp
categories: ["appsec"]
tags: ["eurostack", "operational-excellence"]

links:
  - title: "Go European: Host with Bunny CDN"
    description: Looking for an European CDN? Join Team Bunny!
    website: https://bunny.net?ref=4pdc7xubq5
    image: /images/bunny.svg
---

Bunny.net launched the **Bunny Shield Preview** earlier this year. It's an integrated Web Application Firewall (WAF), DDoS mitigation and rate-limiting controls solution all bundled into their Content Delivery Network (CDN) platform. I've been testing it on a few real-world projects over the last few weeks to see how ready it is and how easy it is to use.

*<b>Spoiler:</b> Bunny Shield is straightforward to use and makes the most of your first experience. It's a solid start for an accessible WAF, but there are a few key improvements needed to make it a production-ready web security product.*

Here's a quick rundown of the things I noticed and the problems I came across. It's meant to show what's working well now and where Bunny.net could  improve their security tooling before it leaves the "Preview" stage.

## What Bunny Shield Gets Right

### Initial User Experience & Setup Simplicity

Bunny Shield carries on the tradition of Bunny.net of offering clean and usable interfaces. As always, you only need to do the bare minimum to get things done. It was easy enough to enable the service and set up firewall or rate limit rules. For smaller sites and teams without dedicated security personnel, this kind of usability is invaluable.

### Default Security Coverage

The out-of-the-box rules catalogue seems pretty reasonable to me, catching common threats without overwhelming users with complex tuning. For most users, this makes Bunny Shield a no-brainer for **basic web protection**.

## What Bunny Shield Needs to Improve

### Certificate Renewal Blocked by WAF

One of the most critical issues I encountered was Bunny Shield **blocking HTTP-01 challenges from Let's Encrypt**. This sometimes seems to stop the automatic TLS certificate renewals through Bunny's own certificate mechanism, which could cause service disruptions if not caught in time.

The good news is that Bunny's support team have already said they know about the problem and are working on a fix. For now, users relying on [HTTP-01 validation](https://letsencrypt.org/docs/challenge-types/ "Let's Encrypt Challenge Types") (e.g. by using the built-in Bunny CDN certificate management) should proceed with caution or disable the WAF.

### No Bot Allowlisting for Good Bots like Ahrefs or Semrush

Currently, Bunny Shield doesn't offer any particular bot management solution. This means there's no way to tell the difference between **harmful bots and legit crawlers** (like Ahrefs, Semrush, and other SEO tools). I saw this causing these "good bots" to be blocked, which harmed my SEO audits and (potentially) visibility.

It'd be great to add a bot management layer or at least some simple allow listing functionality for expected crawlers. The opposite is also true: I'm sure some people would love to trap rogue or misbehaving [AI scraper bots in a maze](https://zadzmo.org/code/nepenthes/ "Nepenthes: A web crawler tarpit").

Overall, I'd love to see Bunny hop on board with the [HTTP Message Signatures](https://blog.cloudflare.com/web-bot-auth/ "Forget IPs: using cryptography to verify bot and agent traffic") bandwagon that Cloudflare recently kicked off.

### Limited Logging and Visibility into WAF Events

There's a clear difference between the 403 traffic logs and the WAF event logs. I can see that requests were blocked, but there's **no clear traceability** to what specific WAF rule was triggered and why. This makes it tricky to debug false positives or fine-tune firewall behaviour, especially when you're dealing with a lot of data.

### Missing WAF Error Code Lookup Tool

When Bunny Shield blocks a request, it returns a 403 with a **unique deny code** (e.g. `WAF403-XXXX`). Unfortunately, there doesn't seem to be a lookup tool for these codes at the moment. If we could get a dashboard-integrated lookup, that'd make a big difference to **WAF rule debugging**.

## Final Thoughts: Promising Foundations, But Still in Beta

All in all, the Bunny Shield Preview is doing really well, especially when it comes to how easy it is to use. It's accessible, integrated tightly into the Bunny.net platform, and it's already solving basic security needs for many developers.

That said, there are a few key things that need to be sorted for Bunny Shield to become a great product. For example, observability, bot management and configurability need to be improved.

I'm excited to see how this product develops, and I'll definitely be keeping an eye on the next updates.

## Got Feedback or Similar Experiences?

Have you had a chance to try out Bunny Shield yet? Did you encounter similar issues? Found any workarounds yet? I'd love to hear about your experience – just send me a message on [Bluesky](https://bsky.app/profile/janbrennenstuhl.eu "Jan Brennenstuhl on Bluesky") or [Mastodon](https://infosec.exchange/@jbspeakr "Jan Brennenstuhl on Mastodon").

Let's help make Bunny Shield a secure, modern WAF that everyone can use.