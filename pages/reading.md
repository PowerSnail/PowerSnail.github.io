---
layout: page
show_meta: false
title: "Reading"
permalink: "/reading/"
---
<ul>
    {% for post in site.categories.reading %}
    <li><a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>