{{- $id := .Get 0 }}{{ $found := dict }}{{ range hugo.Data.glossary.term }}{{ if eq .id $id }}{{ $found = . }}{{ end }}{{ end -}}
[{{ .Get 1 | default ($found.abbr | default $found.term) }}]({{ printf "glossary/#%s" $id | absURL }})
{{- /* chomp */ -}}
