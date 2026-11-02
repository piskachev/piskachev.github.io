---
layout: archive
title: "Service"
permalink: /service/
author_profile: true
---

{% for section in site.data.service %}
<h3>{{ section.title }}</h3>
<ul>
{% for item in section.items %}
  <li>{{ item | markdownify | remove: '<p>' | remove: '</p>' }}</li>
{% endfor %}
</ul>
{% endfor %}
