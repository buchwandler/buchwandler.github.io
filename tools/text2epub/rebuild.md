---
layout: tool-doc
title: "text2epub safe rebuilds"
description: "Idempotent EPUB rebuild workflows"
permalink: /tools/text2epub/rebuild/
nav_tool: text2epub
generated_from: text2epub/docs
source_path: docs/rebuild.md
---
<!-- GENERATED from text2epub/docs. Do not edit by hand. -->

# Safe EPUB rebuilds

The rebuild workflow applies text replacements to an existing EPUB using an extraction manifest. It is designed for automated translation or post-processing systems that must preserve source package entries whenever possible.

## Replacement plan

```python
from pathlib import Path

from text2epub import Replacement, ReplacementPlan, rebuild_epub

report = rebuild_epub(
    ReplacementPlan(
        source_epub=Path("source.epub"),
        extraction_manifest=Path("manifest.json"),
        replacements=[
            Replacement(
                block_id="spine-0001:block-000001",
                text="Translated paragraph.",
                expected_source="Original paragraph.",
                allow_inline_xhtml=False,
            )
        ],
    ),
    Path("rebuilt.epub"),
)

print(report.changed_entries)
```

## Manifest shape

The extraction manifest can be supplied as a mapping or JSON file. The expected schema is intentionally small:

```json
{
  "schema_version": 1,
  "source_sha256": "sha256-of-source-epub",
  "entries": [
    {
      "href": "OEBPS/Text/chapter01.xhtml",
      "media_type": "application/xhtml+xml",
      "spine_index": 1,
      "raw_sha256": "sha256-of-entry-bytes",
      "blocks": [
        {
          "block_id": "spine-0001:block-000001",
          "text": "Original paragraph.",
          "source_start": 128,
          "source_end": 147,
          "replacement_mode": "text_node_sequence"
        }
      ]
    }
  ]
}
```

`source_sha256` and `raw_sha256` are optional, but strongly recommended. When present, they protect against applying replacements to the wrong source file or a stale ZIP entry.

## Replacement modes

`text_node_sequence` replaces the byte-decoded text range from `source_start` to `source_end`.

`whole_block_body` replaces `body_source_start` to `body_source_end` when present, otherwise it falls back to `source_start` and `source_end`. This mode supports safe inline XHTML fragments.

## Safety checks

A rebuild fails when:

- the source EPUB fails basic package validation,
- the manifest source hash does not match the source EPUB,
- a replacement references an unknown or duplicate block,
- source offsets are missing, invalid, outside the entry, or overlapping,
- the current source fragment differs from the manifest fragment,
- a replacement leaks configured internal placeholder tokens,
- an inline XHTML fragment contains forbidden tags, attributes, event handlers, JavaScript links, or malformed XML.

No-op plans and identity replacements copy the source EPUB without rewriting entries. Rebuilds do not operate in place; use a distinct output path.
