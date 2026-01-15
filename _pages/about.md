---
permalink: /
excerpt: "Home"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Hi, I'm Samuel!

I'm doing a PhD at University of Cambridge in Computer Science.
I enjoy working with computer architecture, computer graphics, and GPUs.
My inspiration was video games, and I've worked on a few, but now I'm leaning more towards hardware and architecture.

## Recent Posts
<div>
{% for post in site.posts limit:2 %}
{% include archive-single.html %}
{% endfor %}
</div>

## In Academia
<div>
{% for post in site.publications reversed %}
<p>
    <!-- <img src=
      {% if post.header.teaser contains "://" %}
        "{{ post.header.teaser }}"
      {% else %}
        "{{ post.header.teaser | prepend: "/images/" | prepend: base_path }}"
      {% endif %}
      alt=""> -->
    <i>{{ post.citation }}</i><br/>
    {{ post.excerpt }}
    <a href="{{ post.url }}">Project details</a><br/>
</p>
{% endfor %}
</div>
