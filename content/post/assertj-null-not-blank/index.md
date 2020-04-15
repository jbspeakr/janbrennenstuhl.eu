---
title: "Learning AssertJ: Null ain't Blank"
description: "This AssertJ bug could lead to severe issues: In Java, a blank String is a CharSequence that is empty, null or whitespace only – except when you use AssertJ!"
excerpt: "This AssertJ bug could lead to severe issues: In Java, a blank String is a CharSequence that is empty, null or whitespace only – except when you use AssertJ!"
lead: "Popular assertions framework AssertJ surprises Java engineers with handling NULL-values different from what is commonly expected"
slug: assertj-null-not-blank
date: 2017-09-05
lastmod: 2025-01-18 
draft: false
weight: 50
image: java-assertj-blank.webp
categories: ["software-engineering"]
tags: ["open-source", "java"]
pinned: false
homepage: false
---

Try it yourself: Google “how to check for blank string” – I got about 44 million results. Strings are probably the most common data structures we programmers hand around. In the cross-language String-environment there are well established meanings and commonly shared understandings. 

Especially when it comes to the well-known difficulties regarding [null strings](https://josjong.com/2017/10/16/null-vs-empty-strings-why-oracle-was-right-and-apple-is-not/) vs empty strings (and blank strings) it is worth for everyone to follow already wide-spread naming conventions.

![Toilet rolls representing blank and null states](toilet-rolls.webp "AssertJ – Blank vs Null Strings")

With [Apache Commons StringUtils](https://commons.apache.org/proper/commons-lang/apidocs/org/apache/commons/lang3/StringUtils.html#isBlank-java.lang.CharSequence-) and [Hibernate Validator Constraints](https://docs.jboss.org/hibernate/validator/5.4/api/org/hibernate/validator/constraints/NotBlank.html) two popular and [widely adapted](https://mvnrepository.com/artifact/org.apache.commons/commons-lang3/usages) projects already established a de-facto definition for a blank string:

> “A blank String is a CharSequence that is empty (""), null or whitespace only.”

While recently investigating a bug in one of our systems, I stumbled upon a slight divergent and unexpected string handling in AssertJ, a fluent assertions framework for Java. This [AssertJ misbehavior](https://github.com/joel-costigliola/assertj-core/issues/1069) has potential to lead to severe troubles – which is why I would argue it's a bug. As it turns out ...  

```java
String s = null;
assertThat(s).isNotBlank();
```

... passes. This is definitely not expected behavior, since (following the definition above) a null string is commonly considered to be a blank string and vise-versa. So if you're also used to Apache Commons StringUtils and Hibernate Validators behavior, you wanna make sure your tests actually also expect the correct behavior.

Do you know further libraries that follow a different blank string definition or if you have a different opinion about all of this, drop me message [via Mastodon](https://infosec.exchange/@jbspeakr)!