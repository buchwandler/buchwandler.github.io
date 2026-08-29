#!/usr/bin/env python3
"""Apply build-only compatibility fixes to checked-out documentation sources."""

from __future__ import annotations

from pathlib import Path

LEGACY_G2LEX_PATH_SETUP = 'sys.path.insert(0, os.path.abspath("../g2lex"))\n'


def main() -> None:
    """Remove the legacy g2lex path entry that shadows Python's stdlib modules."""
    source_root = Path(".sphinxpress/sources/g2lex")
    if not source_root.exists():
        return

    for conf_path in source_root.glob("*/docs/conf.py"):
        text = conf_path.read_text(encoding="utf-8")
        if LEGACY_G2LEX_PATH_SETUP in text:
            conf_path.write_text(
                text.replace(LEGACY_G2LEX_PATH_SETUP, ""), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
