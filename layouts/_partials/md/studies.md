
**{{ .Get "caption" | default "Evidence" }}**

| Study | Year | Sample | Method | Finding |
| --- | --- | --- | --- | --- |
{{ trim .Inner "\n " }}
