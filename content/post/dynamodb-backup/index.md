---
title: "AWS DynamoDB: Backup & Recovery Strategy"
linkTitle: "AWS DynamoDB: Backup & Recovery Strategy"
description: "Exploring a backup and recovery strategy for AWS DynamoDB, for optimal system performance and reliability"
excerpt: "In this article, I outline a DynamoDB backup and recovery strategy based on Datapipelines, S3 & AWS Lambdas."
lead: "Orchestrating AWS DynamoDB with Datapipelines, S3 & AWS Lambdas"
slug: aws-dynamodb-backup-recovery
date: 2016-01-18
lastmod: 2025-06-08
draft: false
weight: 50
image: aws-dynamodb-backup-recovery.webp
categories: ["software-security"]
tags: ["aws"]
pinned: false
homepage: false
---

_"Amazon DynamoDB is a fully managed NoSQL database service [...]"_. That's what Amazon states in the [DynamoDB FAQs](https://aws.amazon.com/dynamodb/faqs/). However, their definition is not quite what I would understand as fully managed. It's missing counter-measures against the human error. For that reason, we need a DynamoDB backup and recovery solution, our DynamoDB safety-net...

## DynamoDB Threat Scenario

Imagine your entire AWS infrastructure, including your DynamoDB tables, is defined and set up via AWS Cloudformation (btw, make sure to read [why Cloudformation sucks]({{< ref "/post/cloudformation-sucks/index.md" >}} "Abusing JSON: Why AWS CloudFormation sucks!")) or even worse by hand. Further imagine you actually use your tables to store more or less important data. And finally imagine someone deleting your tables and/ or stacks by accident or your software behaving somehow unexpected, dropping tables. See?! DynamoDB does not ship with built-in backup and recovery implementations, so we had to set up our own protective strategy.

The solution we came up with basically orchestrates AWS DynamoDB with Datapipelines, S3 and Amazons Lambdas to establish not just a daily backup mechanism but also to allow simple staging (production to testing environment) and recovery possibilities. This is how it works:

![A backup & recovery strategy for DynamoDB](DynamoDB-backup-staging.webp "DynamoDB Backup Components")


## DynamoDB w\ AWS Datapipeline & Lambda

In addition to the table definitions, our Cloudformation-based infrastructure setup also describes Datapipelines for the tables in our production environment which nightly backup DynamoDB tables to S3. Furthermore, these Datapipelines' ObjectCreated-Events trigger a small AWS Lambda function we also have in place, which is responsible for deletion and recreation of the corresponding tables in our testing environment. Separated in time, additional Datapipelines refill these empty tables with the productive backups created earlier.

In that way, we established a battle-proven backup and staging solution for AWS DynamoDB. But is this of any help when we have to deal with a real DynamoDB disaster, e.g. accidental table deletion or data corruption? Yes, it is:

Due to the infrastructure as code approach, we can easily recreate entire stacks of DynamoDB tables and Datapipelines (yes, we run tables and pipelines in separated stacks) and use our latest backups to recreate a stable state. Everything with just two or three commands.

However, we don't have any automation in disaster recognition yet as in my eyes it's quite hard to identify possible disasters and (especially) distinguish those from intentional table changes. Also, with this setup we don't have any chance to properly react on DynamoDB (region, AZ, etc.) not reachable/ available issues.

Further downsides: Our approach is heavily dependent on Datapipelines (I already have a 'Why I hate AWS Datapipelines' post in my pipeline ;D) and due to the orchestration of four Amazon Web Services it is not as simple nor cost-efficient as I would want a proper solution for this common problem to be.

Hope you got some inspiration for your future DynamoDB setup. If you have any questions or improvement suggestions make sure to leave a comment or contact me directly.
