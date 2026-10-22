{{- $id := .Get "id" }}
<a id="f-{{ $id }}"></a>
> **Finding f-{{ $id }}:** {{ trim .Inner " \n" }}
{{- with .Get "source" }}
>
> Source: {{ if $.Get "url" }}[{{ . }}]({{ $.Get "url" }}){{ else }}{{ . }}{{ end }}{{ end }}
> Link: {{ .Page.Permalink }}#f-{{ $id }}
