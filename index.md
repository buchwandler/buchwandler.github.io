---
layout: default
title: Home
description: Open source tools for ebook text and conversion workflows
---

<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow">Open source tools for ebook workflows</p>
    <h1>Process books with confidence.</h1>
    <p class="hero-lede">buchwandler builds small, inspectable tools for ebook text and conversion workflows. Each tool handles one step in the pipeline and stays close to your files.</p>
    <div class="hero-actions">
      <a class="button button-primary" href="{{ '/tools/' | relative_url }}">Browse documentation</a>
      <a class="button button-secondary" href="https://github.com/buchwandler" rel="external noopener">Explore on GitHub</a>
    </div>
  </div>
  <div class="hero-panel" aria-label="buchwandler toolkit summary">
    <div class="hero-panel-label">The toolkit</div>
    <div class="hero-stat">5<span>focused tools</span></div>
    <p>File-based, reviewable state for ebook text and conversion pipelines.</p>
  </div>
</section>

<section class="principles" aria-labelledby="principles-title">
  <div>
    <p class="eyebrow">Designed for the long book</p>
    <h2 id="principles-title">Inspectable tools for ebook work.</h2>
  </div>
  <p>Each tool owns one step in the pipeline: extracting text, building EPUBs, splitting passages, managing translation profiles. The output stays readable in code review and runs without a black box.</p>
</section>

<section class="tool-section" aria-labelledby="tools-title">
  <div class="section-heading">
    <div>
      <p class="eyebrow">The toolkit</p>
      <h2 id="tools-title">Tools for the ebook pipeline</h2>
    </div>
    <a class="text-link" href="{{ '/tools/' | relative_url }}">View documentation <span aria-hidden="true">↗</span></a>
  </div>
  <div class="cards tool-cards">
    {% for tool in site.data.tools %}
    <article class="card tool-card">
      <p class="card-label">buchwandler tool</p>
      <h3>{{ tool.name }}</h3>
      <p>{{ tool.description }}</p>
      <div class="card-links">
        {% if tool.docs_url %}
        <a href="{{ tool.docs_url | relative_url }}">Read docs <span aria-hidden="true">↗</span></a>
        {% endif %}
        <a href="{{ tool.repo_url }}" rel="external noopener">GitHub <span aria-hidden="true">↗</span></a>
      </div>
    </article>
    {% endfor %}
  </div>
</section>

<section class="next-step">
  <p class="eyebrow">Start where the work is</p>
  <h2>Choose the step you need to make reliable.</h2>
  <p>Use the Tools menu to jump to documentation, or open any project on GitHub to install it and inspect its source.</p>
</section>
