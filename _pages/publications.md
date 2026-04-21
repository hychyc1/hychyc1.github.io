---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if site.author.googlescholar %}
  <div class="wordwrap">You can also find my articles on <a href="{{site.author.googlescholar}}">my Google Scholar profile</a> and <a href="https://dblp.org/pid/130/4010-1.html">DBLP</a>.</div>
{% endif %}

<p>Authors are listed alphabetically unless they are not, in which case (*) denotes equal contribution.</p>

{% assign sorted_publications = site.publications | sort: "date" | reverse %}

<h2>Manuscripts</h2>
{% assign has_manuscripts = false %}
{% for post in sorted_publications %}
{% if post.working == 'y' and post.venue != 'In submission' %}
{% assign has_manuscripts = true %}
{% include publication-entry.html show_venue=false %}
{% endif %}
{% endfor %}
{% if has_manuscripts == false %}
  <p>No manuscripts at the moment.</p>
{% endif %}

<h2>Publications</h2>
{% assign has_publications = false %}
{% for post in sorted_publications %}
{% if post.working != 'y' %}
{% assign has_publications = true %}
{% include publication-entry.html show_venue=true %}
{% endif %}
{% endfor %}
{% if has_publications == false %}
  <p>No publications at the moment.</p>
{% endif %}
