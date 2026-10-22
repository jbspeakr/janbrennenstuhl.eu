{{- /* Section and topic hubs as Markdown: intro plus the list of entries with their Markdown twins. */ -}}
{{- $pages := .RegularPagesRecursive.ByDate.Reverse -}}
{{- with .Params.topic }}{{ $t := . }}{{ $pages = slice }}{{ range partialCached "eligible.html" $ "all" }}{{ if in (partial "data/topics.html" .) $t }}{{ $pages = $pages | append . }}{{ end }}{{ end }}{{ end -}}
---
title: {{ .Title | jsonify }}
canonical_url: {{ .Permalink }}
author: {{ site.Params.author }}
---

# {{ .Title }}

{{ .Description }}

{{ partial "md/body.md" . }}

## Entries
{{ range $pages }}
- [{{ .Title }}]({{ .Permalink }}) ({{ .Date.Format "2006-01-02" }}, {{ partial "data/kind.html" . }}): {{ .Params.claim | default .Description }}{{ with .OutputFormats.Get "markdown" }} Markdown: {{ .Permalink }}{{ end }}
{{- end }}
