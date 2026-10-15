---
title: "{{ replace .File.ContentBaseName "-" " " | title }}?"   # the question, e.g. "How common is password reuse?"
linkTitle: ""     # short label for navigation
description: ""   # one plain sentence
answer: ""        # two sentences that stand on their own as a quote
claim: ""         # one quotable sentence for llms.txt, feeds and the catalog
slug: {{ .File.ContentBaseName }}
date: {{ .Date }}
weight: 100
# scripts: []     # interactive explainers, e.g. [jwt]
changes:
  - date: {{ .Date | time.Format "2006-01-02" }}
    note: "First version."
draft: true
---

## Key findings

{{`{{< finding id="CHANGE-ME" source="Author et al., Paper title (Venue Year)" url="https://" >}}`}}One claim, taken from the source, with its number.{{`{{< /finding >}}`}}

## Evidence

{{`{{< studies caption="Studies" >}}`}}
{{`{{< study title="" org="" year="" sample="" method="" url="https://" >}}`}}What this study found, in one sentence.{{`{{< /study >}}`}}
{{`{{< /studies >}}`}}

## What to do

### For engineers

-

### For product and UX

-
