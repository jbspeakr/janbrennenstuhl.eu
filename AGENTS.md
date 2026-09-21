# AGENTS.md

Hugo 0.161.1 (extended) blog using Hugo Theme Stack v4.

## Repository layout

```
assets/              Hugo asset-pipeline inputs: SCSS, images, and icons
config/_default/     Site, navigation, markup, and theme configuration
content/              Page bundles: posts, pages, knowledge base, categories, and tags
layouts/             Local Hugo Theme Stack overrides
static/              Files copied to the site unchanged
.forgejo/workflows/  CI build and BunnyCDN deployment
go.mod, go.sum       Hugo module and pinned theme dependency
public/              Generated site output; do not edit
resources/           Hugo cache/generated assets; do not edit
```

## Commands

```sh
hugo --gc --minify serve  # run the local development server
hugo --minify             # build exactly as CI does
```

## Conventions

- Create articles as `content/post/<slug>/index.md`; keep referenced media in that bundle.
- Match existing YAML front matter: `title`, `description`, `excerpt`, `lead`, `slug`, `image`, `date`, `lastmod`, `draft`, categories, and tags.
- Use `{{< ref "/post/<slug>/index.md" >}}` for internal article links.
- Put Hugo asset-pipeline inputs in `assets/`; use `static/` only for unchanged files.
- Prefer configuration in `config/_default/`; override theme templates only in `layouts/`.
- Original `content/` is CC BY 4.0; do not edit generated `public/` or `resources/`.

