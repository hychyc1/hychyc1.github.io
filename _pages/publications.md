---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if site.author.googlescholar %}
  <div class="wordwrap">You can also find my articles on <a href="{{site.author.googlescholar}}">my Google Scholar profile</a>.</div>
{% endif %}

{% include base_path %}

{% assign working_papers = site.publications | where_exp: "post", "post.working == 'y'" | sort: "date" | reverse %}
{% assign published_papers = site.publications | where_exp: "post", "post.working != 'y'" | sort: "date" | reverse %}

{% for post in working_papers %}
  {% include publication-entry.html %}
{% endfor %}

{% for post in published_papers %}
  {% include publication-entry.html %}
{% endfor %}
