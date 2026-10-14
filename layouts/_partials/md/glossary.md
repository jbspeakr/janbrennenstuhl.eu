{{ range sort hugo.Data.glossary.term "term" }}
<a id="{{ .id }}"></a>
**{{ .term }}**{{ with .expansion }} ({{ . }}){{ end }}: {{ .definition }}
{{ end }}
