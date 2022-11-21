## Overview

Generated at: {{ now.UTC.Format "02 Jan 06 15:04 MST" }}, with Hugo (version={{hugo.Version}}), in 
{{ if hugo.IsProduction }}_Production_{{ else }}_Development_{{end}} mode.

## Pages

{{ $posts := .Site.GetPage "section" "posts" -}}

| Entry           | Count                                              |
| --------------- | -------------------------------------------------- |
| Posts           | {{ len $posts.RegularPages }}                      |
| Drafts          | {{ len (where $posts.RegularPages "Draft" true) }} |
| **Total Pages** | **{{ len .Site.Pages }}**                          |

## Tags

{{ $tags := .Site.GetPage "/tags" -}}

Counts (>1):

| Tag | Item Count |
| --- | ---------- |
{{ range (where $tags.Data.Terms.ByCount "Count" ">" 1) -}}
| [{{ .Page.Title }}]({{ .Page.RelPermalink }}) | {{ .Count }} | 
{{ end }}

Orphaned Tags:

{{ range (where $tags.Data.Terms.ByCount "Count" "==" 1) -}}
{{- $page := index .Pages 0 -}}
- {{ .Page.Title }}: [{{ $page.File.Path }}]({{ $page.RelPermalink }})
{{ end -}}

