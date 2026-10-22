{{- $lines := split (trim .Inner "\n ") "\n" }}
{{ range $lines }}> {{ . }}
{{ end }}{{ if or (.Get "source") (.Get "author") }}>
> — {{ with .Get "author" }}{{ . }}{{ if $.Get "source" }}, {{ end }}{{ end }}{{ with .Get "source" }}{{ if $.Get "url" }}[{{ . }}]({{ $.Get "url" }}){{ else }}{{ . }}{{ end }}{{ end }}
{{ end }}
