---
id: jb-svn-to-git
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['software-engineering']
imageDecorative: true
title: "How to Migrate SVN to GIT with History?"
description: "Version Control System (VCS) Migration: A short guide on how to migrate SVN to GIT while preserving source code authors and commit history."
excerpt: "A small step-by-step example on how to move your source code from SVN to GIT."
slug: howto-convert-svn-git
date: 2015-04-15
lastmod: 2025-06-01
draft: false
weight: 50
image: svn-to-git.webp
categories: ["software-engineering"]
tags: ["open-source", "git"]
pinned: false
homepage: false
---

Today I'd like to share my solution for a common problem a lot of IT companies experience when finally moving from Subversion (SVN) to Git as their central version control system (VCS): Converting a SVN repository into a Git repo including its commit history and authors.

To achieve this, I decided to split this issue into smaller pieces:

1. Extracting all authors of the SVN repository,
2. Creating a proper authors file mapping SVN users to Git users,
3. Converting SVN repo to Git including its history and authors.

Here is what I did:

## Converting SVN to GIT w/ History & Authors

Checkout your SVN repository.

```bash
svn co SVN_REPO_URL
```

Go into the repo directory and extract authors from the SVN repo [using this statement](http://stackoverflow.com/questions/2159567/what-is-the-format-of-an-authors-file-for-git-svn-specifically-for-special-char).

```bash
svn log --xml | grep author | sort -u | perl -pe 's/.>(.?)<./$1 = /'
```

Using this information, create an authors.txt file like this:

```bash
# SVN_AUTHOR_HANDLE = GIT_AUTHOR_HANDLE <GIT_AUTHOR_EMAIL>
jbrennenstuhl = janbrennenstuhl <xyz@brnnnsthl.eu>
...
```

Using this file you now can start converting your SVN repo into a Git repo.

```bash
git svn clone -A authors.txt SVN_REPO_URL
```

This will convert the old SVN repo into a new Git repo including the complete SVN history and mapping its authors following the mapping in authors.txt. Depending on the dimension of the SVN repo history, this can take several minutes or even hours!

If you don't want to have the entire SVN history you could choose to start from a specific revision like this:

```bash
git svn clone -rSVN_REVISION:HEAD -A authors.txt SVN_REPO_URL
```

Still using SVN? Start converting to Git now!