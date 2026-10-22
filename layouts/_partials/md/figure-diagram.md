{{- $r := .Page.Resources.Get (.Get "src") }}
![{{ .Get "alt" }}]({{ $r.Permalink }})

*{{ .Get "caption" }}*

**What this shows:** {{ trim .Inner "\n " }}
