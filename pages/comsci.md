---
layout: page
show_meta: false
title: "Computer Science"
permalink: "/comsci/"
---
<ul>
    {% for post in site.categories.comsci %}
    <li><a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>