---
id: jb-monocyte
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['application-security']
imageDecorative: true
title: "AWS Monocyte: Let's Build a Cloud Immune System"
description: "Monocyte: A AWS Immune System. Comply to EU regulations by finding and deleting AWS resources in regions outside of Europe with AWS Monocyte!"
excerpt: "Monocyte: A AWS Immune System. Comply to EU regulations by finding and deleting AWS resources in regions outside of Europe with AWS Monocyte!"
slug: aws-cloud-immune-system
date: 2015-03-18
lastmod: 2025-06-22
draft: false
weight: 50
image: monocyte.webp
categories: ["software-security"]
tags: ["open-source", "aws", "operational-excellence"]
pinned: false
homepage: false
---

With Ireland and Frankfurt being available as AWS regions nowadays, Amazon (more or less) tried to extinguish EU and especially German legal concerns regarding storage and processing of privacy-related data. However, for European companies it remains difficult to prevent (accidental) usage of services and resources outside the EU, as there is still no standardized way to restrict AWS-account rights on this region-level. Especially in open, [DevOps](https://en.wikipedia.org/wiki/DevOps)-inspired company cultures this becomes a major issue:

## AWS & YBIYRI

The majority of European companies my colleagues and I recently interviewed about their AWS infrastructure, implemented (or plan to implement) some kind of multi-account setup, meaning that single product teams own their own accounts (which usually are aggregated via [consolidated billing](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html)). One reason for this decision is (in addition to hard AWS API limits) that they try to implement the so-called *"You built it; You run it"*-approach, which is also [propagated by Amazon](https://www.safaribooksonline.com/library/view/programming-amazon-ec2/9781449303617/ch01s03.html). This trending approach implies that every AWS account is managed entirely and autonomously by its corresponding development team, which eventually is not anymore just responsible for building software components and products but also becomes responsible for operating the required infrastructure.

This (of course!) leads to several conflicts of goals. On the one hand companies often want their teams to work with AWS independently and manage their own accounts mostly autonomously. On the other hand they are usually bound to legal frameworks (e.g. the [EU Data Protection Directive](https://en.wikipedia.org/wiki/Data_Protection_Directive) and/ or German privacy laws) and for that reason want to search and destroy non-EU AWS resources relentlessly.

## A Cloud Immune System

To accomplish that, we built our own base-layer of what we call a cloud immune system: [AWS Monocyte](https://github.com/ImmobilienScout24/aws-monocyte). The name Monocyte is related to a [type of white blood cells](https://en.wikipedia.org/wiki/Monocyte) that are part of e.g. a human's innate immune system, the first line of defense being responsible for searching and destroying alien organisms to prevent unwanted infections.

As [Arne Hilmann](https://arnehilmann.github.io/) and I explained during the [AWS UserGroup Meetup](http://www.meetup.com/AWS-Berlin/events/220609022/) this March at the Immobilien Scout HQ in Berlin, our tool is (in that biological sense) able to find and delete AWS resources in regions outside the EU. This allows companies to make sure that (accidentally) created non-EU resources are destroyed on a regular basis and helps in that way to (unfortunately reactively) enforce legal requirements.

Right now, AWS Monocyte is able to handle just a subset of the plenty Amazon Services, including Cloudformation Stacks, EC2 Instances, EC2 Volumes, RDS Instances, RDS Snapshots, DynamoDB Tables and S3 Bucket. Implementing support for further Amazon Web Services is pretty easy and I hereby ask you to [fork our project](https://github.com/ImmobilienScout24/aws-monocyte) and help extending its power!
