#!/usr/bin/env python3
"""Apply build-only compatibility fixes to checked-out documentation sources."""

from __future__ import annotations

from pathlib import Path

LEGACY_G2LEX_PATH_SETUP = 'sys.path.insert(0, os.path.abspath("../g2lex"))\n'
PHONODIST_IMPORT = "import phonodist  # noqa: E402\n"
PHONODIST_BACKEND_STUB = """try:
    import panphon  # noqa: E402
except ModuleNotFoundError as error:
    if error.name != "panphon":
        raise
    # Metric functions are documented but never executed during this build.
    from types import ModuleType

    panphon = ModuleType("panphon")
    panphon.FeatureTable = type("FeatureTable", (), {})
    sys.modules["panphon"] = panphon

"""



def main() -> None:
    """Patch upstream configs for build-only compatibility."""
    _patch_legacy_g2lex_configs()
    _patch_phonodist_configs()



def _patch_legacy_g2lex_configs() -> None:
    """Remove the g2lex path entry that shadows Python's stdlib modules."""
    source_root = Path(".sphinxpress/sources/g2lex")
    if not source_root.exists():
        return

    for conf_path in source_root.glob("*/docs/conf.py"):
        text = conf_path.read_text(encoding="utf-8")
        if LEGACY_G2LEX_PATH_SETUP in text:
            conf_path.write_text(
                text.replace(LEGACY_G2LEX_PATH_SETUP, ""), encoding="utf-8"
            )



def _patch_phonodist_configs() -> None:
    """Stub PanPhon during docs builds when it's absent from the build env."""
    source_root = Path(".sphinxpress/sources/phonodist")
    if not source_root.exists():
        return

    for conf_path in source_root.glob("*/docs/conf.py"):
        text = conf_path.read_text(encoding="utf-8")
        if PHONODIST_IMPORT in text and PHONODIST_BACKEND_STUB not in text:
            conf_path.write_text(
                text.replace(
                    PHONODIST_IMPORT,
                    PHONODIST_BACKEND_STUB + PHONODIST_IMPORT,
                ),
                encoding="utf-8",
            )



if __name__ == "__main__":
    main()
