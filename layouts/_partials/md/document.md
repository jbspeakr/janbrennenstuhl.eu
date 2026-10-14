{{- /* Full Markdown twin: YAML front matter, title, lead or answer, key findings, body, citation footer. */ -}}
{{- $meta := partial "metadata.html" . -}}
{{- $fm := dict -}}
{{- range $k, $v := $meta }}{{ if not (in (slice "source_url" "source_revision" "content_hash" "claim") $k) }}{{ $fm = merge $fm (dict $k $v) }}{{ end }}{{ end -}}
---
{{ transform.Remarshal "yaml" $fm | strings.TrimSpace }}
---

# {{ .Title }}
{{ with .Params.answer }}
**Short answer:** {{ . }}
{{ else }}{{ with .Params.lead | default .Description }}
{{ . }}
{{ end }}{{ end }}
{{- with .Params.findings }}
## Key findings
{{ range $i, $f := . }}
<a id="f-{{ $f.id }}"></a>
{{ add $i 1 }}. {{ $f.text }} ({{ $.Permalink }}#f-{{ $f.id }})
{{- end }}
{{ end }}
{{ partial "md/body.md" . }}

---

Cite as: Jan Brennenstuhl. "{{ .Title }}." {{ site.Title }}, {{ .PublishDate.Format "2 January 2006" }}. {{ .Permalink }}
{{ if ne .Params.license false }}License: CC BY 4.0 ({{ site.Params.license.url }}) for the original text; credited third-party media keep their own rights.{{ else }}License: not specified.{{ end }}
