---
permalink: /
title: "Home"
excerpt: "Home"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

This is my webpage!

There's nothing here yet.


## Latest Posts
<div>
{% capture written_year %}'None'{% endcapture %}
{% for post in site.posts limit:2 %}
  {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
  {% if year != written_year %}
    <h2 id="{{ year | slugify }}" class="archive__subtitle">{{ year }}</h2>
    {% capture written_year %}{{ year }}{% endcapture %}
  {% endif %}
    <a href="{{ post.url }}">{{ post.title }}</a>
    {{ post.excerpt }}
{% endfor %}
</div>