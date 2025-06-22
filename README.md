# janbrennenstuhl.eu

This repository contains the source code, content and deployment job for [janbrennenstuhl.eu](https://www.janbrennenstuhl.eu/), the personal website and blog of Jan Brennenstuhl, a product-minded principal software engineer with focus on usable security & web authentication. The website is built using the Hugo static site generator and the Hugo Theme Stack.

## Project Overview

janbrennenstuhl.eu serves as a platform for sharing articles, insights, and information related to software engineering, web security, and other technical topics. The site emphasizes clean code practices and interdisciplinary software development.

## Licensing

This project utilizes different licenses for its content and theme:

* **Content License (CC BY 4.0):** All original content within the `content/` directory of this repository is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to share and adapt the material for any purpose, even commercially, as long as you provide attribution to Jan Brennenstuhl.

* **Theme License (GPL 3.0):** The website's theme, [hugo-theme-stack](https://github.com/CaiJimmy/hugo-theme-stack), is licensed under the [GNU General Public License v3.0 (GPL 3.0)](https://www.gnu.org/licenses/gpl-3.0.en.html). This means that if you distribute, modify, or use the theme, you must do so under the terms of the GPL 3.0.

* **Hugo:** The website is powered by [Hugo](https://gohugo.io/), an open-source static site generator. Hugo itself is licensed under the Apache License 2.0.

## Development

The site is built with Hugo. To run it locally, you will need to have Hugo installed.

```
hugo --gc --minify serve
```