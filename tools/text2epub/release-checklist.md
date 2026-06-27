---
layout: tool-doc
title: "text2epub release checklist"
description: "Steps to publish a text2epub release"
permalink: /tools/text2epub/release-checklist/
nav_tool: text2epub
generated_from: text2epub/docs
source_path: docs/release-checklist.md
---
<!-- GENERATED from text2epub/docs. Do not edit by hand. -->

# Release checklist

Use this checklist before publishing a package or tagging a release.

## Required checks

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m compileall -q text2epub tests
python -m text2epub version
```

Run Ruff when the dependency is installed:

```bash
python -m ruff check .
python -m ruff format --check .
```

Build and inspect distributions from a git checkout or release archive:

```bash
python -m build
python -m twine check dist/*
```

## Manual review

- Confirm the version produced by package metadata, `text2epub.__version__`, and `text2epub version` is identical.
- Confirm `LICENSE` exists and matches the configured project license and classifiers.
- Run EPUBCheck against generated sample EPUBs.
- Test the CLI against a real `booktx` extraction manifest.
- Confirm docs build with `python -m sphinx -b html docs docs/_build/html`.
- Confirm release notes describe any manifest schema, safety, or CLI behavior changes.

## Current validation boundary

`validate_epub_package` is a basic package-level check. It is suitable as a smoke test but not as a publication-grade EPUB validator.
