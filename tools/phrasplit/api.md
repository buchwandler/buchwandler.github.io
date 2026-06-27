---
layout: tool-doc
title: "phrasplit Python API"
description: "Python API functions and the Segment type for phrasplit"
permalink: /tools/phrasplit/api/
nav_tool: phrasplit
generated_from: phrasplit/docs
source_path: docs/api.md
---
<!-- GENERATED from phrasplit/docs. Do not edit by hand. -->

# API Reference

This page contains the complete API reference for phrasplit.

## Main Functions


### split_sentences

Documented via Sphinx autodoc in the source repository:
- `phrasplit.split_sentences`
**Example:**

```python
from phrasplit import split_sentences

text = "Dr. Smith is here. She has a Ph.D. in Chemistry."
sentences = split_sentences(text)
# ['Dr. Smith is here.', 'She has a Ph.D. in Chemistry.']

# Use simple mode (no spaCy required)
sentences = split_sentences(text, use_spacy=False)

# split_on_colon is deprecated (kept for compatibility only)
text = "Note: This is important."
sentences = split_sentences(text, split_on_colon=False)
```

### split_clauses

Documented via Sphinx autodoc in the source repository:
- `phrasplit.split_clauses`
**Example:**

```python
from phrasplit import split_clauses

text = "I like coffee, and I like tea."
clauses = split_clauses(text)
# ['I like coffee,', 'and I like tea.']

# Use simple mode for faster processing
clauses = split_clauses(text, use_spacy=False)
```

### split_paragraphs

Documented via Sphinx autodoc in the source repository:
- `phrasplit.split_paragraphs`
**Example:**

```python
from phrasplit import split_paragraphs

text = "First paragraph.\n\nSecond paragraph."
paragraphs = split_paragraphs(text)
# ['First paragraph.', 'Second paragraph.']
```

### split_text

Documented via Sphinx autodoc in the source repository:
- `phrasplit.split_text`
**Example:**

```python
from phrasplit import split_text, Segment

text = "First sentence. Second sentence.\n\nNew paragraph."
segments = split_text(text, mode="sentence")

for seg in segments:
    print(f"P{seg.paragraph} S{seg.sentence}: {seg.text}")
# P0 S0: First sentence.
# P0 S1: Second sentence.
# P1 S0: New paragraph.

# Clause mode for finer granularity
text = "Hello, world.\n\nGoodbye, friend."
segments = split_text(text, mode="clause")
# Returns clauses with paragraph and sentence indices

# Use simple mode (no spaCy)
segments = split_text(text, mode="sentence", use_spacy=False)
```

### split_long_lines

Documented via Sphinx autodoc in the source repository:
- `phrasplit.split_long_lines`
**Example:**

```python
from phrasplit import split_long_lines

text = "This is a very long sentence that needs to be split into smaller parts."
lines = split_long_lines(text, max_length=40)

# Use simple mode
lines = split_long_lines(text, max_length=40, use_spacy=False)
```

## Data Types

### Segment

Documented via Sphinx autodoc in the source repository:
- `phrasplit.Segment`
A named tuple representing a text segment with position information.

**Fields:**

- `text` (str): The text content of the segment
- `paragraph` (int): Paragraph index (0-based) within the document
- `sentence` (int | None): Sentence index (0-based) within the paragraph. None for
  paragraph mode.

**Example:**

```python
from phrasplit import split_text, Segment

segments = split_text("Hello world.", mode="sentence")
seg = segments[0]

# Access by name
print(seg.text)       # "Hello world."
print(seg.paragraph)  # 0
print(seg.sentence)   # 0

# Access by index
print(seg[0])  # "Hello world."
print(seg[1])  # 0
print(seg[2])  # 0

# Unpack
text, para, sent = seg
```

## Module Contents

### splitter module

Documented via Sphinx autodoc in the source repository:
- `phrasplit.splitter`
## Type Information

phrasplit is fully typed and includes a `py.typed` marker file for PEP 561 compliance.
You can use it with mypy and other type checkers.

Function signatures:

```python
from typing import NamedTuple

class Segment(NamedTuple):
    text: str
    paragraph: int
    sentence: int | None = None

def split_sentences(
    text: str,
    language_model: str = "en_core_web_sm",
    apply_corrections: bool = True,
    split_on_colon: bool = True,
    use_spacy: bool | None = None,
) -> list[str]: ...

def split_clauses(
    text: str,
    language_model: str = "en_core_web_sm",
    use_spacy: bool | None = None,
) -> list[str]: ...

def split_paragraphs(text: str) -> list[str]: ...

def split_text(
    text: str,
    mode: str = "sentence",
    language_model: str = "en_core_web_sm",
    apply_corrections: bool = True,
    split_on_colon: bool = True,
    use_spacy: bool | None = None,
) -> list[Segment]: ...

def split_long_lines(
    text: str,
    max_length: int,
    language_model: str = "en_core_web_sm",
    use_spacy: bool | None = None,
) -> list[str]: ...
```
