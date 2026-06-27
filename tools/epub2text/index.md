---
layout: tool-doc
title: "epub2text"
description: "Extract text from EPUB files with smart cleaning and navigation"
permalink: /tools/epub2text/
nav_tool: epub2text
generated_from: epub2text/docs
source_path: docs/index.md
---
<!-- GENERATED from epub2text/docs. Do not edit by hand. -->

# epub2text Documentation

A niche CLI tool to extract text from EPUB files with smart cleaning capabilities.

## Features

- **Smart Navigation Parsing**: Supports both EPUB3 (NAV HTML) and EPUB2 (NCX)
  navigation formats
- **Multiple Extraction Modes**:
  - Chapter-based extraction with selective range support
  - Page-based extraction (using EPUB page-list or synthetic pages)
  - Project Gutenberg format output with proper formatting
- **Interactive Terminal Reader**:
  - Vim-style navigation (j/k, Space/b, n/p for chapters)
  - Bookmark support with automatic resume
  - Adjustable page size and content width
- **Flexible Output Formatting**:
  - One paragraph per line with customizable separators
  - One sentence per line using spaCy NLP
  - One clause per line (split at commas, semicolons)
  - Automatic line splitting at clause boundaries for long lines
- **Smart Text Cleaning**:
  - Remove bracketed footnotes (`[1]`, `[42]`)
  - Remove page numbers (standalone, at line ends, with dashes)
  - Normalize whitespace and paragraph breaks
  - Preserve ordered lists with proper numbering
  - Optional front matter/TOC filtering
- **Rich Interactive UI**: Beautiful terminal output with tables and tree views
- **Pipe-Friendly**: Works as both CLI tool and Python library
- **Nested Chapter Support**: Handles hierarchical chapter structures
- **Full Dublin Core Metadata**: Extract all EPUB metadata fields
- **URL Support**: Extract text directly from EPUB files hosted online

## Quick Start

Install epub2text:

```bash
pip install epub2text
```

Extract text from an EPUB file:

```bash
epub2text extract book.epub
```

Extract by pages:

```bash
epub2text extract-pages book.epub
```

List chapters:

```bash
epub2text list book.epub
```

List pages:

```bash
epub2text pages book.epub
```

Read interactively:

```bash
epub2text read book.epub
```

Show metadata:

```bash
epub2text info book.epub
```

<div class="cards">
  <section class="card"><h3><a href="{{ '/tools/epub2text/installation/' | relative_url }}">Installation</a></h3><p>Install epub2text from PyPI or source.</p></section>
  <section class="card"><h3><a href="{{ '/tools/epub2text/usage/' | relative_url }}">Usage guide</a></h3><p>Extraction modes, text cleaning, and the interactive reader.</p></section>
  <section class="card"><h3><a href="{{ '/tools/epub2text/api/' | relative_url }}">Python API</a></h3><p>Public API classes and functions for epub2text.</p></section>
  <section class="card"><h3><a href="{{ '/tools/epub2text/changelog/' | relative_url }}">Changelog</a></h3><p>Release history for epub2text.</p></section>
</div>
