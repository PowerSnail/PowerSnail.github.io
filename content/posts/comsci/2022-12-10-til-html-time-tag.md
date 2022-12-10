---
title: "TIL: HTML Has a `<time>` Tag"
description: 
date: 2022-12-10T09:41:12Z
slug: til-html-time-tag
tags: 
    - html
    - computer science
    - TIL
draft: false
commentid: 109488773969656531
---

Today I learned that HTML has a `<time>` tag which supplements a written date and time with a machine-readable format.[^1] Supposedly, this helps with parsability, and in turn, good for accessibility. I've added this into my Hugo template for metadata.

```html
{{- $isoFormat := "2006-01-02T15:04:05" -}}
{{- $humanFormat := "02 Jan 2006" -}}
...
<time datetime="{{ .Params.date.Format $isoFormat }}">{{ .Params.date.Format $humanFormat }}</time>
...
```




[^1]: MDN Web Docs. _https://developer.mozilla.org/en-US/docs/Web/HTML/Element/time_