---
id: jb-python-tuple-list-to-dict
kind: essay
status: published
reviewStatus: not-reviewed
topics: ['software-engineering']
imageDecorative: true
title: "Python Docopt: Convert Tuple List to Dictionary"
description: "Python Docopt: How to convert a list of tuples into a dictionary in Python. A quick and easy solution for beautiful command-line interfaces …"
excerpt: "How to convert a list of tuples into a dictionary in Python. A quick and easy solution for beautiful command-line interfaces …"
slug: howto-convert-tuplelist-dictionary
date: 2015-04-28
lastmod: 2023-04-15
draft: false
weight: 50
image: howto-python-docopt-hack.webp
categories: ["software-engineering"]
tags: ["open-source", "python"]
pinned: false
homepage: false
---

Using [Python Docopt](https://github.com/docopt/docopt) (for beautiful command-line interfaces) I recently had the problem of converting a list of tuples into a dictionary. In this post I'd like to document [the solution](https://gist.github.com/jbspeakr/c7c4fcb9ee143cf7e9eb)…

```python
"""
usage:
    mytool [options]

options:
    --foo-bar=PARAM1,PARAM2,... params to do stuff with
        [default: key1.value1,key1.value2,key2.value2]
"""

from docopt import docopt
from collections import defaultdict


def run():
    params = [tuple(param.strip().split('.')) for param in arguments["--foo-bar"].split(",")]
    params = convert_tuple_list_to_dictionary(ignored_resources)

def convert_tuple_list_to_dictionary(list_of_tuple):
    dictionary = defaultdict(list)
    for k, v in list_of_tuple:
        dictionary[k].append(v)

    return dictionary

if __name__ == "__main__":
    run()
```

This code is able to convert the parameter value string `key1.value1,key1.value2,key2.value2` into the following dictionary:

```bash
{
	'key1': ['value1', 'value2'],
    'key2': ['value2']
}
```

If you know a leaner solution to solve this problem, let me know!