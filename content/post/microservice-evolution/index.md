---
id: jb-microservice-evolution
imageDecorative: true
title: "Evolution of a Microservice: A Git History Visualisation"
description: "Keeping microservices micro is a must if you want to benefit from them. How to visualize git histories and what you can learn from it. Devops ✓ Git ✓ Gource ✓"
claim: "Microservices keep their benefits only if teams cut them down regularly: one service grew from 5k to 15k lines of code in a year and shrank back to about 5k after a split."
excerpt: "Keeping microservices micro is a must if you want to benefit from them. I take a deep dive into the evolution of a microservice …"
lead: "A deep dive into the evolution of a microservice, from its inception as a small, independent module to its growth into a complex kraken"
slug: microservice-evolution
date: 2015-05-21
lastmod: 2023-04-21
draft: false
weight: 50
image: microservice-evolution-software-architecture.webp
tags: ["git"]
---

Microservices have revolutionized the way we develop and deploy software applications. But with great power comes great complexity. As microservices become more and more ubiquitous, developers must grapple with new challenges, such as managing dependencies, ensuring scalability, and maintaining consistency across services. In this article, I take a deep dive into the evolution of a microservice, from its inception as a small, independent module to its growth into a complex kraken…

Following the common pendulum theory, every tech debate oscillates between at least two currently trending topics. The same is true when it comes to micro-services (vs. integrated systems). One of my former teams decided to follow a radical microservices approach, favoring the benefits of smallest possible deployment units over integration (and its advantages) and preferring infrastructure as well as communication complexity over tight coupling. Why we chose to do so and how we make sure to keep our services micro, I'm going to explain in more detail...

## Microservices, Self-contained Systems & Integrated Applications

Back then my team was responsible for parts of one a core selling flows. With thousands of customers-to-be every day and direct major business impact, we not just need to be reliable as well as always up-and-running, but also fairly flexible and (even more important) fast, allowing product improvements, bug fixes and multi-variant tests to be rolled out in near-realtime. Helping us to achieve those goals are our continuous live deployment (CLD) infrastructure, our near-realtime monitoring as well as alarming setup and most importantly our constantly evolving, stateless micro-services...

The [micro-services architecture](http://microservices.io/patterns/microservices.html) I am referring to in this article is the probably most remote antipole of what is commonly known as monolithic, integrated system (or what some companies call legacy, heritage or mothership). Between those two extrema, there is a whole bunch of manifestations, variations and adoptions like the so-called [Self-contained System](http://scs-architecture.org/index.html) (SCS) architecture. However, I am usually not a big fan of some technical middle courses as in my experience they often combine not the intended advantages but the downsides of two radical different ideas. Furthermore, if a framework (and an architecture is nothing else) allows people to implement their first gut feelings instead of understanding the greater ideas, concepts and reasons, they tend to do so.

On the other hand, sticking with and optimizing your infrastructure for one clean approach (not in a religious but explaining manner) generally helps creating easy repeatable and comprehensible software architecture - as long as you can handle possible drawbacks. Having implemented a strict microservices-based deployment architecture in our core business, we now benefit from a couple of great possibilities even our business people find it great to work with:

{{< youtube 12IU4m16bJM >}}

## Microservices, Don't let'em grow!

We have tiny, decoupled applications that are deployed independently. Due to their small footprint, each of them is easier to understand (even by new colleagues) and can be cloned and built in almost no time, which speeds up not just our dev productivity but also our deployments. Additionally, our microservices enable us to exchange parts of our tech stack pretty easy and make us in that way eager to try out new things. Whether it's about server-side vs. client-side rendering, SQL vs. NoSQL databases, Play vs. Spring or any other major design decision, we don't need to compromise, we can use whatever fits best and helps us to solve the microservices single purpose. It's a great feeling and even better: It helps us reducing complexity and dependencies in each of our deployment units. However, to be able to enjoy these advantages you need to be beware of its drawbacks...

In my eyes the major challenge of a microservices architecture is not that shifted complexity of its distribution, but that you need to cut. It's a big drawback, because every software tends to grow bigger - it's just a matter of time until a single-purpose microservice becomes a multi-purpose legacy app. There's no way to prevent your software from doing so. Whether you cut your services functional or by following business use-cases, you have no other chance than to be fully-aware of that fact, and you need to cut carefully and (most importantly) you need to cut often.

The video above visualizes the evolution of one of our microservices on a source-code level. As almost every green field software, it starts fairly simple but quickly outgrow its originally intended size and (even worse) its single-purpose approach. Although fighting back with more or less effective refactorings, the service grew from 5k up to 15k lines-of-code (LoC) within a year until we started to actively enforce our microservice-policy. As the [Gource](http://gource.io/) visualization shows, we started to decouple our service's back- and frontend functionality by migrating from server- to client-side rendering and by introducing a separate, Grunt-based build-process for our frontend-resources (see 01:30).

Next, we where able to identify further decoupling possibilities more easily and started moving major backend functionality to a new, separately created microservice, shrinking down the code-base of this particular service (which basically serves a couple of public webpages) back to round about 5k LoC (see 01:50). Being done with that, our service now is in a state where we can directly benefit from all the advantages we discussed before. Furthermore, we ended up with a clean decoupling between mainly enduser-centric code and a more business-administration REST-API.

## tl;dr - Take a radical approach!

When it comes to tech decisions, going all-in and optimizing for one strict approach (one pole of the spectrum) and being aware of its possible drawbacks is always better than mixing contradictory ideas, patterns or philosophies. Although in theory, combining  contradictory approaches might sometimes sound like a great idea (_"hey, let's combine the best of'em all!"_), in practice they're usually not.

Whether it's about server-side vs. client-side rendering, [serverless](https://aws.amazon.com/blogs/compute/microservices-without-the-servers/) vs. servers-as-cattle, or the red vs. blue pill, you want to settle for exactly one extrema. However, you need to know and understand the drawbacks. Establishing and maintaining e.g. an microservices architecture is continuous work. Evaluating the actual size as well as purpose of your services (and service landscape) is essential and cutting down your services regularly is a must if you want to benefit from your architectural decision for microservices.