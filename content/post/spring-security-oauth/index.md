---
id: jb-spring-security-oauth
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['identity-authentication', 'application-security']
imageDecorative: true
title: "On Making Spring Security OAuth RFC-compliant"
description: "Open-Source Contribution | I fixed a small HTTP header extractor in Spring Security OAuth. Here's what happened & what I learned."
excerpt: "On Fixing Spring Security OAuth: I fixed a small HTTP header extractor for the Spring Security OAuth open source project recently. Here's what happened & what I learned..."
slug: spring-security-oauth-rfc
date: 2017-02-01
lastmod: 2017-02-16
draft: false
weight: 50
image: open-source-inspiration.webp
categories: ["appsec"]
tags: ["open-source", "java", "oauth2"]
pinned: false
homepage: false
---

Often supporting open source software is just fixing one tiny thing you stumbled upon. However, getting ready and diving into even the smallest piece of source-code can lead to surprising results. I fixed a small HTTP header extractor for the [Spring Security OAuth](https://github.com/spring-projects/spring-security-oauth) project recently. Here's what happened.

## I fixed something for me

At the very least, fixing this issue has made me happier. The problem was that the Spring Security OAuth `BearerTokenExtractor` was not acting in compliance to [RFC7230](https://tools.ietf.org/html/rfc7230#section-3.2.2).

Every time someone sends a request with multiple, comma-separated Authorization-Header values towards an application I am currently developing the extractor would fail in doing its job. The application would simply not accept the yet valid (and RFC compliant) request.

> **RFC7230, Section 3.2.2** - A sender MUST NOT generate multiple header fields with the same field name in a message
unless either the entire field value for that header field is defined as a comma-separated list [i.e., #(values)] ...

## I fixed something for someone else
This is a guess, but if I found this an issue then we can presume at least one other person out there on the internet did. Also, being RFC-compliant usually is a good thing and every library should handle user-generated input as resilient as possible.

## I learned more about Library Maintenance
I started by making a mistake. My original fix was a custom implementation of the `TokenExtractor` interface that is also implemented by the original `BearerTokenExtractor` within my application. This however would require me to maintain and test this piece of code that is not part of my actual business logic. I would totally loose the advantages of abstraction through a battle-proven library. It also ignored the problems true essence.

That thought lead me to try again. This time I cloned the Spring Security OAuth project and tried copy-and-pasting my slim Java8 Streams API based `TokenExtractor` and its tests into the library. This lead to a bunch of discoveries about library maintenance — Spring Security OAuth...

- ... is written in Java6,
- ... has only other Spring projects as dependencies,
- ... needs to be backward compatible.

So, if you plan to support a project that is out there for a while, keep in mind to leave all your fancy tooling at home. Also try to read and follow the projects code and style guidelines before receiving requests for change in your pull-requests.

Of course, as with anything around the globe, [there is even more to this than meet the eye](https://github.com/spring-projects/spring-security-oauth/blob/master/CODE_OF_CONDUCT.adoc). However, this was [my resulting pull request](https://github.com/spring-projects/spring-security-oauth/pull/895) ~~and it is waiting to get merged~~.

## I learned more about HTTP Headers
In the beginning, I learned about the diversity of HTTP Headers. Being spoiled by all these framework abstraction layers nowadays, it hit me that HTTP Headers are simply yet another interface. And we want to handle all interface interaction in the most resilient way.

Inspired by some of my colleagues, I started to delve into RFCs. I started with [RFC6750](https://tools.ietf.org/html/rfc6750) (describing the Bearer Token Usage within OAuth 2.0) and ended up in the even more fundamental [RFC7230](https://tools.ietf.org/html/rfc7230) (on Message Syntax and Routing of the Hypertext Transfer Protocol).

Now I am more familiar with the possible appearances of HTTP Headers and the work behind the Spring Security OAuth project.

~~With my fix in one of the next releases, Spring Security OAuth is going to also be able to handle requests like this:~~

```
GET /presence/alice HTTP/1.1
Host: server.example.com
Authorization: Basic YXNkZnNhZGZzYWRmOlZLdDVOMVhk, Bearer mF_9.B5f-4.1JqM
```

**Update 16.02.2017:** As Joe Grandja (Spring Security Engineer) argued, the user agent is supposed to choose _"only 1 of the challenges (if there is more than 1 challenge) to authenticate against"_, so my pull request was rejected. Feel free to read all the comments in the [corresponding issue](https://github.com/spring-projects/spring-security-oauth/issues/894) for all the details.

## The simplest piece of work can lead you anywhere

I just wanted to make the Bearer Token extraction more resilient. Yet, this lead to a ticket and a pull request, a rabbit hole of discovery about HTTP Headers and open source library maintenance and the motivation to write a blog post about it. Ultimately, I did get what I wanted in the first place though: More fun during work.

Open source is a lot of things to a lot of people. To me, it's a way to learn while I help, however small the task may seem. I'd love for you to share with [me on Twitter](https://twitter.com/jbspeakr) what open source means to you.

---
<small>This post was heavily [inspired by Phil Nash](https://philna.sh/blog/2017/01/27/on-fixing-a-favicon/).</small>