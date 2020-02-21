---
layout: page
show_meta: false
title: "Recipes"
permalink: "/recipes/"
---
<ul>
    {% for post in site.categories.recipes %}
    <li><a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>