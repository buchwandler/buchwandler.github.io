---
layout: default
title: Home
description: Open source tools for book processing, translation, text normalization, speech synthesis, and audiobook workflows.
workflow_stages:
  - id: source
    title: Source
    description: Start with a book or text.
  - id: structure
    title: Structure
    description: Extract and segment useful content.
  - id: normalize
    title: Normalize
    description: Prepare text and speech markup.
  - id: pronounce
    title: Pronounce
    description: Resolve words into pronunciation.
  - id: synthesize
    title: Synthesize
    description: Turn prepared text into speech.
  - id: output
    title: Output
    description: Listen, publish, or build a new book.
tool_categories:
  - books
  - text
  - pronunciation
  - speech
  - audio
  - infrastructure
---
{% assign booktx = site.data.tools | where: "name", "booktx" | first %}
{% assign readio = site.data.tools | where: "name", "readio" | first %}
{% assign ttsforge = site.data.tools | where: "name", "ttsforge" | first %}

<section class="hero" aria-labelledby="home-title">
  <div class="hero-copy">
    <p class="eyebrow">Open source tools for books and speech</p>
    <h1 id="home-title">Small tools. Complete book workflows.</h1>
    <p class="hero-lede">Open-source building blocks for turning books and text into structured content, translations, speech, and audio.</p>
    <div class="hero-actions">
      <a class="button button-primary" href="#outcomes">Explore workflows</a>
      <a class="button button-secondary" href="{{ '/tools/' | relative_url }}">Browse all tools</a>
    </div>
  </div>
  <div class="hero-panel" aria-label="A modular toolchain for books and speech">
    <div class="hero-panel-label">One modular ecosystem</div>
    <p>Start with a complete workflow, or combine focused building blocks in your own pipeline.</p>
    <ul class="hero-highlights">
      <li>Book processing and translation</li>
      <li>Text preparation and pronunciation</li>
      <li>Speech synthesis and audio</li>
    </ul>
  </div>
</section>

<section class="outcome-section" id="outcomes" aria-labelledby="outcomes-title">
  <div class="section-heading">
    <div>
      <p class="eyebrow">Choose an outcome</p>
      <h2 id="outcomes-title">What are you trying to do?</h2>
    </div>
  </div>
  <div class="outcome-grid">
    <article class="outcome-card">
      <p class="card-label">Book workflow</p>
      <h3>Translate an ebook</h3>
      <p>Prepare, translate, review, and rebuild EPUB and Markdown books.</p>
      <a class="outcome-link" href="{{ booktx.docs_url | relative_url }}">Start with {{ booktx.name }} <span aria-hidden="true">→</span></a>
    </article>
    <article class="outcome-card">
      <p class="card-label">Speech application</p>
      <h3>Read text aloud</h3>
      <p>Stream text through configurable speech engines directly from the terminal.</p>
      <a class="outcome-link" href="{{ readio.docs_url | relative_url }}">Start with {{ readio.name }} <span aria-hidden="true">→</span></a>
    </article>
    <article class="outcome-card">
      <p class="card-label">Audiobook workflow</p>
      <h3>Create an audiobook</h3>
      <p>Turn books and long-form text into an automated speech workflow.</p>
      <a class="outcome-link" href="{{ ttsforge.docs_url | relative_url }}">Start with {{ ttsforge.name }} <span aria-hidden="true">→</span></a>
    </article>
    <article class="outcome-card outcome-card-secondary">
      <p class="card-label">Developer workflow</p>
      <h3>Build a speech pipeline</h3>
      <p>Combine segmentation, normalization, pronunciation, synthesis, and audio components.</p>
      <a class="outcome-link" href="#workflows">Explore speech components <span aria-hidden="true">→</span></a>
    </article>
  </div>
</section>

<section class="workflow-section" id="workflows" aria-labelledby="workflow-title">
  <div class="section-heading">
    <div>
      <p class="eyebrow">Composable building blocks</p>
      <h2 id="workflow-title">From source to speech and beyond</h2>
      <p>Conceptual stages show where tools fit; they are not a claim that every tool is a direct dependency of the next.</p>
    </div>
  </div>
  <div class="workflow-map" aria-label="Book and speech workflow stages">
    {% for stage in page.workflow_stages %}
    <section class="workflow-stage" aria-labelledby="workflow-stage-{{ stage.id }}">
      <span class="workflow-stage-number">{{ forloop.index | prepend: '0' }}</span>
      <h3 id="workflow-stage-{{ stage.id }}">{{ stage.title }}</h3>
      <p class="workflow-stage-description">{{ stage.description }}</p>
      <div class="workflow-stage-tools">
        {% for tool in site.data.tools %}
        {% if tool.stages contains stage.id %}
        <a class="workflow-tool" href="{{ tool.docs_url | relative_url }}">
          <strong>{{ tool.name }}</strong>
          <span>{{ tool.description }}</span>
        </a>
        {% endif %}
        {% endfor %}
      </div>
    </section>
    {% unless forloop.last %}<span class="workflow-connector" aria-hidden="true">→</span>{% endunless %}
    {% endfor %}
  </div>
</section>

<section class="tool-section compact-tool-directory" aria-labelledby="directory-title">
  <div class="section-heading">
    <div>
      <p class="eyebrow">Explore the ecosystem</p>
      <h2 id="directory-title">The building blocks</h2>
    </div>
    <a class="text-link" href="{{ '/tools/' | relative_url }}">View the complete catalog <span aria-hidden="true">↗</span></a>
  </div>
  <div class="tool-groups">
    {% for category in page.tool_categories %}
    <section class="tool-group" aria-labelledby="tool-group-{{ category }}">
      <h3 id="tool-group-{{ category }}">{{ category | replace: '-', ' ' | capitalize }}</h3>
      <ul class="tool-list">
        {% for tool in site.data.tools %}
        {% if tool.category == category %}
        <li class="tool-list-item">
          <a href="{{ tool.docs_url | relative_url }}">
            <strong>{{ tool.name }}</strong>
            <span class="tool-role">{{ tool.role | replace: '-', ' ' | capitalize }}</span>
            <span class="tool-description">{{ tool.description }}</span>
          </a>
        </li>
        {% endif %}
        {% endfor %}
      </ul>
    </section>
    {% endfor %}
  </div>
  <div class="directory-cta">
    <p>Use a complete workflow or combine components for your own pipeline.</p>
    <a class="button button-secondary" href="{{ '/tools/' | relative_url }}">Browse all tools</a>
  </div>
</section>
