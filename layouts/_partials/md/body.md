{{- /* A page's body as Markdown: shortcodes rendered by their Markdown variants, links made absolute,
       and an explicit anchor before each heading that matches the HTML heading ID. */ -}}
{{- $base := .Permalink -}}
{{- $src := string .RenderShortcodes -}}
{{- $src = replaceRE `\]\(/` (printf "](%s" site.BaseURL) $src -}}
{{- $src = replaceRE `(href|src)="/` (printf `$1="%s` site.BaseURL) $src -}}
{{- $src = replaceRE `\]\(#` (printf "](%s#" $base) $src -}}
{{- $src = replaceRE `\]\(([A-Za-z0-9][A-Za-z0-9._-]*\.(?:webp|png|jpe?g|gif|svg|pdf|avif))` (printf "](%s$1" $base) $src -}}
{{- $out := slice }}{{ $fence := "" }}{{ $seen := dict -}}
{{- range split $src "\n" -}}
  {{- $line := . -}}
  {{- $m := findRESubmatch "^\\s{0,3}(\\x60{3,}|~{3,})" $line 1 -}}
  {{- if $m }}{{ $mark := index (index $m 0) 1 }}{{ if not $fence }}{{ $fence = $mark }}{{ else if hasPrefix $mark $fence }}{{ $fence = "" }}{{ end }}{{ end -}}
  {{- if and (not $fence) (not $m) (findRE `^#{2,6}\s+\S` $line 1) -}}
    {{- $text := replaceRE `^#{2,6}\s+` "" $line | replaceRE `\s+#+\s*$` "" -}}
    {{- $id := $text | markdownify | plainify | htmlUnescape | anchorize -}}
    {{- with index $seen $id }}{{ $seen = merge $seen (dict $id (add . 1)) }}{{ $id = printf "%s-%d" $id . }}{{ else }}{{ $seen = merge $seen (dict $id 1) }}{{ end -}}
    {{- $out = $out | append (printf "<a id=\"%s\"></a>" $id) -}}
  {{- end -}}
  {{- $out = $out | append $line -}}
{{- end -}}
{{- return delimit $out "\n" -}}
