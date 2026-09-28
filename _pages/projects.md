---
title: "Projects"
permalink: /projects/
classes: wide
description: "Applied AI and embedded-systems portfolio projects across ADAS perception, CAN cybersecurity, sensor fusion, control, and compliance-aware engineering."
image: /assets/images/projects-fusion.svg
---

Below are selected projects connecting my embedded systems experience with modern AI/ML applications. Completed work is presented first; roadmap projects follow separately.

{% assign completed_projects = site.projects | where: 'phase', 'completed' | sort: 'order' %}
{% assign active_projects = site.projects | where_exp: 'project', "project.phase != 'completed'" | sort: 'order' %}

## Completed Work

<div class="card-grid">
{% for project in completed_projects %}
  {% include project-card.html %}
{% endfor %}
</div>

## Planned Projects

<div class="card-grid">
{% for project in active_projects %}
  {% include project-card.html %}
{% endfor %}
</div>
