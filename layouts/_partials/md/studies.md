
**{{ .Get "caption" | default "Evidence" }}**

| Study | Year | Sample | Method | Finding |
| --- | --- | --- | --- | --- |
{{ replaceRE `\n\s*\n` "\n" (trim .Inner "\n ") }}
