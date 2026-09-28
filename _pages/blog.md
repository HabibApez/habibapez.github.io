---
title: "Blog"
permalink: /blog/
classes: wide
description: "Technical writing on embedded systems to AI transition, including machine learning, computer vision, and safety-critical engineering insights."
image: /assets/images/projects-yolo.svg
---

Insights on machine learning, deep learning, automotive systems, and career transition from embedded engineering to AI research.

<div class="card-grid">
{% for post in site.posts %}
  <article class="blog-card fade-reveal">
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <p><strong>Date:</strong> {{ post.date | date: "%B %d, %Y" }}</p>
    <p><strong>Reading time:</strong> {% assign mins = post.content | number_of_words | divided_by: 200 | ceil %}{{ mins }} min</p>
    {% if post.tags %}
    <div class="tech-tags">
      {% for t in post.tags %}
      <span class="tech-tag">{{ t }}</span>
      {% endfor %}
    </div>
    {% endif %}
    <p>{{ post.excerpt | strip_html | truncate: 170 }}</p>
  </article>
{% endfor %}
</div>
