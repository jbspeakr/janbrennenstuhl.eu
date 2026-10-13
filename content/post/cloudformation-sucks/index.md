---
id: jb-cloudformation-sucks
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['software-engineering']
imageDecorative: true
title: "Abusing JSON: Why AWS CloudFormation sucks?!"
description: "Infrastructure as code is great but AWS Cloudformation is not! Learn why JSON-based Cloudformation is bad and what alternatives exist. Devops ✓ AWS ✗ JSON ✗"
excerpt: "Infrastructure as code is great but AWS Cloudformation is not! Learn why JSON-based Cloudformation is bad and what alternatives exist …"
slug: why-aws-cloudformation-sucks
date: 2015-05-21
lastmod: 2025-06-22
draft: false
weight: 50
image: aws-cloudformation-sucks.webp
categories: ["software-engineering"]
tags: ["operational-excellence", "aws"]
pinned: false
homepage: false
---

[AWS CloudFormation](https://aws.amazon.com/cloudformation/) (CFN) is a file-based interface for provisioning AWS resources and in that way is Amazons answer on the '[Infrastructure as Code](http://www.thoughtworks.com/insights/blog/infrastructure-code-reason-smile)' paradigm. I am a huge fan of this approach and CFN is a big step into the right direction as it supports not just common DevOps ideas, by allowing devs to create, update and delete the operational infrastructure they need with their own tools (a text editor, version control and tests).

It also enables you to think different about your IT infrastructure and how to work with it (e.g. just think about immutable stacks). However, I see some issues that become more important if you work with CloudFormation on a daily basis ...

## JSON Lang, WTF?!

CloudFormation templates are simple JSON-formatted text files that (in theory) can easily be created and maintained by hand as nowadays every dev (and/ or ops) should be able to read and write valid JSON. However, AWS CloudFormation uses the originally static *[lightweight data-interchange format](https://www.json.org/json-en.html)* as a scripting language, allowing e.g. the definition and usage of parameter and (somehow crazy) [intrinsic function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html) references.

In my eyes, this is a heavy misusage that leads to several problems regarding complexity and comprehensibility. You can find several deterrent examples that illustrate this right in the official AWS developers guide. If you still don't think JSON is a syntax-bloated, hard-to-read data format just have a look on how to define [DataPipelines using CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#d0e32425) and tell me you like it and that you are able to easily understand all the definitions as well as their interactions. It took me some time...

But that's not even the worst part. JSON also lacks some feature substance that some devs would regard heavily essential. In contrast to its technical superset YAML, JSON is not aware of e.g. comments or user defined data types. In my eyes, this is a huge downside and a massive argument against Amazons classical CloudFormation design.

All in all I don't quite get the whys and reasons which made Amazons engineers believe that the abuse of JSON for scripting would be a better and more innovative idea than go for something like an established scripting language like Python or JavaScript.

But enough JSON-bashing for now. Let's solve at least some of our AWS CloudFormation issues.

## CFN-Sphere

Currently there are a couple of tools around that sit on top of CFN as an abstraction layer and offer not just a YAML-based config approach, but also further functionality that comes in handy if you work with infrastructure as code during your everyday business.

One of those tools is [CFN-Sphere](https://github.com/cfn-sphere/cfn-sphere), a lightweight Python-tool that aims to simplify AWS CloudFormation handling not just for infrasturcture automation but also for human interaction. Initially built by [Marco Hoyer](https://github.com/marco-hoyer) (a former colleague and friend of mine) CFN-Sphere comes with fundamental support for e.g. cross stack parameter references and automatic stack dependency resolution including circular dependency detection. Both are amazing features also for smaller AWS infrastructure definitions like the backup and staging environment for DynamoDB tables I am currently working on (More on that topic in one of the upcoming posts).

So if you are struggling with your with your CloudFormation config or if you have a certain feeling that CFN files having around several hundred lines of code are almost unmaintainable, make sure to check out CFN-Sphere and its stack template feature. And help making it even greater by becoming a contributor!