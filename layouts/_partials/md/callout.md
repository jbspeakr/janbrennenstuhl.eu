{{ $lines := split (trim .Inner "\n ") "\n" }}
> {{ with .Get "title" }}**{{ . }}**{{ end }}
>
{{ range $lines }}> {{ . }}
{{ end }}
