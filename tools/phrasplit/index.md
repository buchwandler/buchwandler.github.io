---
layout: tool-doc
title: "phrasplit"
description: "Split text into sentences, clauses, or paragraphs"
permalink: /tools/phrasplit/
nav_tool: phrasplit
generated_from: phrasplit/docs
source_path: docs/index.md
---
<!-- GENERATED from phrasplit/docs. Do not edit by hand. -->

# phrasplit Documentation

A Python library for splitting text into sentences, clauses, or paragraphs. Designed for
audiobook creation and text-to-speech processing.

phrasplit supports two processing modes:

- **spaCy mode** (optional): High-accuracy NLP-based splitting using spaCy
- **Simple mode**: Lightweight regex-based splitting with no dependencies

## Features

- **Sentence splitting**: Intelligent sentence boundary detection
- **Clause splitting**: Split sentences at commas for natural pause points
- **Paragraph splitting**: Split text at double newlines
- **Long line splitting**: Break long lines at sentence/clause boundaries
- **Abbreviation handling**: Correctly handles Mr., Dr., U.S.A., etc.
- **Ellipsis support**: Preserves ellipses without incorrect splitting
- **Flexible installation**: Works with or without spaCy
- **Auto-detection**: Automatically uses the best available mode

## Mode Comparison

| Feature               | Simple Mode       | spaCy Mode          |
| --------------------- | ----------------- | ------------------- |
| Dependencies          | None (regex only) | spaCy + models      |
| Installation size     | Minimal           | ~500MB+ with models |
| Speed                 | Very fast         | Fast                |
| Memory usage          | Low               | Medium-High         |
| Accuracy              | Good              | Excellent           |
| Complex abbreviations | Basic support     | Full support        |
| Dependency parsing    | No                | Yes                 |
| Multi-language        | Limited           | Extensive           |

## Installation

Install without spaCy (lightweight):

```bash
pip install phrasplit
```

Install with spaCy support (recommended):

```bash
pip install phrasplit[nlp]
python -m spacy download en_core_web_sm
```

## Quick Start

```python
from phrasplit import split_sentences, split_clauses, split_paragraphs

# Split text into sentences (works with or without spaCy)
text = "Dr. Smith is here. She has a Ph.D. in Chemistry."
sentences = split_sentences(text)
# ['Dr. Smith is here.', 'She has a Ph.D. in Chemistry.']

# Explicitly use simple mode (no spaCy required)
sentences = split_sentences(text, use_spacy=False)

# Split sentences into comma-separated parts
text = "I like coffee, and I like tea."
clauses = split_clauses(text)
# ['I like coffee,', 'and I like tea.']

# Split text into paragraphs
text = "First paragraph.\n\nSecond paragraph."
paragraphs = split_paragraphs(text)
# ['First paragraph.', 'Second paragraph.']
```

## Table of Contents

<div class="cards">
  <section class="card"><h3><a href="{{ '/tools/phrasplit/installation/' | relative_url }}">Installation</a></h3><p>Install phrasplit with or without spaCy.</p></section>
  <section class="card"><h3><a href="{{ '/tools/phrasplit/usage/' | relative_url }}">Usage guide</a></h3><p>Splitting modes and command workflows.</p></section>
  <section class="card"><h3><a href="{{ '/tools/phrasplit/cli/' | relative_url }}">CLI</a></h3><p>Command-line interface reference.</p></section>
  <section class="card"><h3><a href="{{ '/tools/phrasplit/api/' | relative_url }}">Python API</a></h3><p>Public API functions and the Segment type.</p></section>
  <section class="card"><h3><a href="{{ '/tools/phrasplit/examples/' | relative_url }}">Examples</a></h3><p>Worked examples for each splitting mode.</p></section>
</div>
