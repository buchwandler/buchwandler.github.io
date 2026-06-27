---
layout: tool-doc
title: "booktx Python API"
description: "Python API modules for booktx"
permalink: /tools/booktx/api/
nav_tool: booktx
generated_from: booktx/docs
source_path: docs/api.md
---
<!-- GENERATED from booktx/docs. Do not edit by hand. -->

# API reference

This page exposes the internal modules through Sphinx autodoc. The public command-line interface is more stable than the Python internals.

## Stability notes

- **Stable public API**: The CLI commands (`booktx init`, `booktx extract`, `booktx translate next`, etc.) and their JSON output shapes are the primary stable interface.
- **Stable models**: Pydantic models in `booktx.models` (Chunk, Record, TranslationStore, TranslationTask, Manifest) are serialization contracts used by the CLI and external tools.
- **Service modules**: `booktx.status`, `booktx.tasks`, `booktx.submissions`, `booktx.acceptance`, `booktx.rendering`, `booktx.io_utils` contain the extracted service logic. Their public functions are stable within a release cycle.
- **Internal helpers**: `booktx.config`, `booktx.context`, `booktx.validate`, `booktx.build`, `booktx.chunking`, `booktx.placeholders` are intended stable but may change between minor releases.
- **Legacy**: `booktx.html_io` contains shared XHTML helpers that may be consolidated in future releases.

Documented via Sphinx autodoc in the source repository:
- `booktx.config`
- `booktx.models`
- `booktx.context`
- `booktx.chunking`
- `booktx.placeholders`
- `booktx.markdown_io`
- `booktx.epub_io`
- `booktx.epub_manifest`
- `booktx.chapters`
- `booktx.validate`
- `booktx.build`
- `booktx.status`
- `booktx.tasks`
- `booktx.submissions`
- `booktx.acceptance`
- `booktx.rendering`
- `booktx.io_utils`
- `booktx.record_refs`
- `booktx.translation_store`
- `booktx.versioning`
