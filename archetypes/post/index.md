---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
description: ""   # one plain sentence for search results, feeds and llms.txt
claim: ""         # optional: the one quotable sentence that states the main point
date: {{ .Date }}
slug: {{ .File.ContentBaseName }}
tags: []          # mapped to topics via data/topics.toml
# series: ""      # an ID from data/series.toml
# findings:       # up to three; IDs are permanent and unique site-wide
#   - id: ""
#     text: ""
draft: true
---

Open with the point. Keep media for this post in this bundle folder.
