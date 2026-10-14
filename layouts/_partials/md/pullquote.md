{{ with .Get "id" }}<a id="q-{{ . }}"></a>
{{ end }}> {{ trim .Inner " \n" }}
