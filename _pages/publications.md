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

{% include base_path %}

{% assign manuscripts = site.publications | where_exp: "post", "post.working == 'y' and post.venue != 'In submission'" | sort: "date" | reverse %}
{% assign publications = site.publications | where_exp: "post", "post.working != 'y'" | sort: "date" | reverse %}

<h2>Manuscripts</h2>
{% if manuscripts.size > 0 %}
  {% for post in manuscripts %}
    {% include publication-entry.html show_venue=false %}
  {% endfor %}
{% else %}
  <p>No manuscripts at the moment.</p>
{% endif %}

<h2>Publications</h2>
{% if publications.size > 0 %}
  {% for post in publications %}
    {% include publication-entry.html show_venue=true %}
  {% endfor %}
{% else %}
  <p>No publications at the moment.</p>
{% endif %}
