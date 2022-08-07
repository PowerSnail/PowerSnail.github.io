## Overview

Generated at: {{ .Site.LastChange }}, with Hugo (version={{hugo.Version}}), in 
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
| {{ .Page.Title }} | {{ .Count }} | 
{{ end }}

Orphaned Tags:

{{ $orphanedTags := dict }}
{{ range (where $tags.Data.Terms.ByCount "Count" "==" 1) -}}
{{ $page := index .Pages 0 }}
{{ $array := index $orphanedTags $page.File.Path }}
{{ $array = $array | append . }}
{{ $orphanedTags = merge $orphanedTags ( dict $page.File.Path $array ) }}
{{ end }}

{{ range $key, $value := $orphanedTags -}}
- {{ $key }} {{ range $value }}
  - {{ .Page.Title }} {{ end }}
{{ end }}
