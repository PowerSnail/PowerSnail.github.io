---
layout: page
show_meta: false
title: "Studies"
permalink: "/studies/"
---
<ul>
    {% for post in site.categories.studies %}
    <li><a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>