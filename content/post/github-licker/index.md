---
id: jb-github-licker
imageDecorative: true
title: "How to Check Github Licenses"
description: "Github Licker is a Github License Checker command line tool that helps you to keep an overview over your organisations OSS licenses. Try it out now!"
claim: "Github-Licker is a small Python command-line tool that uses the GitHub Licenses API to list the licenses of an organization's repositories and find repositories without a license file."
slug: github-license-checker
date: 2015-03-25
lastmod: 2017-04-17
draft: false
weight: 50
image: github-licker.webp
tags: ["open-source", "git"]
---
On Github, every organization with a fast growing open-source codebase quickly figures out a couple of shortcomings regarding the Github web interface. Especially, when it comes to Github organizations that are already around for some time, you often find some information missing that could probably help managing and controlling your organizations repositories...

## Github & Licenses

For months now, Github addresses in particular the often discussed license-problematic by implementing the [License Picker](https://help.github.com/articles/open-source-licensing/) feature and introducing the [choosealicense.com](http://choosealicense.com/) information page. That's great if you start with new projects and repositories, but what's missing is some kind of license overview and maintaining functionality that allows dealing with licenses of already existing repos.

For that reason, I just built a small Python tool to help you getting an overview of your repos licenses: [Github-Licker](https://github.com/jbspeakr/github-licker), a Github License Checker!

## Github License Checker

Using the [Github API v3](https://developer.github.com/v3/) including the [Licenses API](https://developer.github.com/v3/licenses/) developer preview, Licker is able to check licenses of all repositories in your Github organization. It searches all your own repositories (no forks!) and especially helps  identifying repos without license files.

```bash
pip install github-licker
licker -h

usage:
    licker [TOKEN] [options]

options:
    -o, --organisation=ORGANIZATION  the Github organization you want to check [default: ImmobilienScout24]
```

Github-Licker itself is licensed under [Apache License, Version 2.0](https://github.com/ImmobilienScout24/aws-monocyte/blob/master/LICENSE.txt), for what reason you can easily [help me to improve it](https://github.com/jbspeakr/github-licker)!