#!/usr/bin/env python3
"""Sync Sphinx/MyST Markdown docs into Jekyll-compatible tool docs.

This script intentionally does not modify source repositories. It creates a
reviewable generated Jekyll projection in buchwandler.github.io/tools/<tool>/.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

DEFAULT_TOOL = "booktx"

TOOL_REPOS = {
    "epub2text": "https://github.com/buchwandler/epub2text",
    "text2epub": "https://github.com/buchwandler/text2epub",
    "phrasplit": "https://github.com/buchwandler/phrasplit",
    "booktx": "https://github.com/buchwandler/booktx",
}

TITLE_OVERRIDES = {
    "epub2text": {
        "index": "epub2text",
        "installation": "epub2text installation",
        "usage": "epub2text usage guide",
        "api": "epub2text Python API",
        "structured_extraction": "epub2text structured extraction",
        "changelog": "epub2text changelog",
    },
    "text2epub": {
        "index": "text2epub",
        "getting-started": "text2epub getting started",
        "markdown": "text2epub markdown to EPUB",
        "rebuild": "text2epub safe rebuilds",
        "cli": "text2epub command-line interface",
        "api": "text2epub Python API",
        "release-checklist": "text2epub release checklist",
    },
    "phrasplit": {
        "index": "phrasplit",
        "installation": "phrasplit installation",
        "usage": "phrasplit usage guide",
        "cli": "phrasplit command-line interface",
        "api": "phrasplit Python API",
        "examples": "phrasplit examples",
        "integration": "phrasplit integration contract",
        "offsets": "phrasplit offset-preserving segmentation",
        "streaming": "phrasplit streaming API",
    },
    "booktx": {
        "index": "booktx",
        "quickstart": "booktx quickstart",
        "project-layout": "booktx project layout",
        "profiles": "booktx profiles",
        "concepts": "booktx concepts",
        "commands": "booktx commands",
        "context": "booktx context",
        "agent-workflow": "booktx agent workflow",
        "translation-contract": "booktx translation contract",
        "markdown": "booktx markdown handling",
        "epub": "booktx EPUB handling",
        "architecture": "booktx architecture",
        "api": "booktx Python API",
        "development": "booktx development",
        "troubleshooting": "booktx troubleshooting",
    },
}

DESCRIPTION_OVERRIDES = {
    "epub2text": {
        "index": "Extract text from EPUB files with smart cleaning and navigation",
        "installation": "Install epub2text from PyPI or source",
        "usage": "Extraction modes, text cleaning, and the interactive reader",
        "api": "Python API classes and functions for epub2text",
        "structured_extraction": "Structured extraction of EPUB content into blocks and segments",
        "changelog": "epub2text release history",
    },
    "text2epub": {
        "index": "Build EPUB ebooks from Markdown and text sources",
        "getting-started": "Install text2epub and build a first EPUB",
        "markdown": "Markdown book and chapter conversion model",
        "rebuild": "Idempotent EPUB rebuild workflows",
        "cli": "text2epub command-line interface reference",
        "api": "Python API modules for text2epub",
        "release-checklist": "Steps to publish a text2epub release",
    },
    "phrasplit": {
        "index": "Split text into sentences, clauses, or paragraphs",
        "installation": "Install phrasplit with or without spaCy",
        "usage": "Splitting modes and command workflows for phrasplit",
        "cli": "phrasplit command-line interface reference",
        "api": "Python API functions and the Segment type for phrasplit",
        "examples": "Worked examples for each phrasplit splitting mode",
        "integration": "Pipeline integration contract for phrasplit",
        "offsets": "Offset-preserving text segmentation",
        "streaming": "Streaming and iterator APIs for phrasplit",
    },
    "booktx": {
        "index": "Profile-first translation toolchain for ebooks",
        "quickstart": "Profile-first workflow walkthrough",
        "project-layout": "Shared versus profile-local booktx state",
        "profiles": "Translation profile isolation model",
        "concepts": "Core booktx concepts and terminology",
        "commands": "booktx CLI command reference",
        "context": "Translation context files and conventions",
        "agent-workflow": "Operating rules for coding agents using booktx",
        "translation-contract": "Translation contract for source and target",
        "markdown": "Markdown handling for booktx",
        "epub": "EPUB build and packaging for booktx",
        "architecture": "booktx architecture overview",
        "api": "Python API modules for booktx",
        "development": "Development setup and release workflow for booktx",
        "troubleshooting": "Common booktx problems and fixes",
    },
}

CARD_LABELS = {
    "epub2text": {
        "installation": ("Installation", "Install epub2text from PyPI or source."),
        "usage": ("Usage guide", "Extraction modes, text cleaning, and the interactive reader."),
        "api": ("Python API", "Public API classes and functions for epub2text."),
        "changelog": ("Changelog", "Release history for epub2text."),
    },
    "text2epub": {
        "getting-started": ("Getting started", "Install text2epub and build a first EPUB."),
        "markdown": ("Markdown to EPUB", "Markdown book and chapter conversion model."),
        "rebuild": ("Safe rebuilds", "Idempotent EPUB rebuild workflows."),
        "cli": ("CLI", "Command-line interface reference."),
        "api": ("Python API", "Public models and builder functions."),
        "release-checklist": ("Release checklist", "Steps to publish a text2epub release."),
    },
    "phrasplit": {
        "installation": ("Installation", "Install phrasplit with or without spaCy."),
        "usage": ("Usage guide", "Splitting modes and command workflows."),
        "cli": ("CLI", "Command-line interface reference."),
        "api": ("Python API", "Public API functions and the Segment type."),
        "examples": ("Examples", "Worked examples for each splitting mode."),
    },
    "booktx": {
        "quickstart": ("Quickstart", "Profile-first workflow walkthrough."),
        "project-layout": ("Project layout", "Shared versus profile-local state."),
        "profiles": ("Profiles", "Translation profile isolation model."),
        "concepts": ("Concepts", "Core concepts and terminology."),
        "commands": ("Commands", "booktx CLI command reference."),
        "context": ("Context", "Translation context files and conventions."),
        "agent-workflow": ("Agent workflow", "Operating rules for coding agents."),
        "translation-contract": ("Translation contract", "Contract for source and target texts."),
        "markdown": ("Markdown", "Markdown handling for booktx."),
        "epub": ("EPUB", "EPUB build and packaging."),
        "architecture": ("Architecture", "booktx architecture overview."),
        "api": ("Python API", "Public API modules for booktx."),
        "development": ("Development", "Development setup and release workflow."),
        "troubleshooting": ("Troubleshooting", "Common problems and fixes."),
    },
}


def generated_header(tool: str) -> str:
    return f"<!-- GENERATED from {tool}/docs. Do not edit by hand. -->"


def extract_h1(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def yaml_string(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def convert_code_block_directives(text: str) -> str:
    """Convert common MyST code-block fences to standard Markdown fences."""
    text = re.sub(r"^(```+)\{code-block\}\s+([A-Za-z0-9_+-]+)\s*$", r"\1\2", text, flags=re.MULTILINE)
    return re.sub(r"^(```+)\{code-block\}\s*$", r"\1", text, flags=re.MULTILINE)


def convert_myst_anchors(text: str) -> str:
    """Convert MyST explicit anchors, e.g. (init)=, to stable HTML anchors."""
    return re.sub(
        r"^\(([A-Za-z0-9_.:-]+)\)=$",
        r'<a id="\1"></a>',
        text,
        flags=re.MULTILINE,
    )


def extract_automodule_names(text: str) -> list[str]:
    modules = re.findall(
        r"^```\{automodule\}\s+([^\n]+)\n.*?^```\s*$",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    return [module.strip() for module in modules]


def convert_automodule_page(text: str) -> str:
    """Replace Sphinx automodule directives with a Jekyll-friendly module list."""
    modules = extract_automodule_names(text)
    if not modules:
        return text

    lines = [
        "# " + extract_h1(text, "API reference"),
        "",
        "The public Python API is organized around these modules:",
        "",
    ]
    lines.extend(f"- `{module}`" for module in modules)
    lines.extend(
        [
            "",
            "Install the package locally to inspect generated API details with Python help tools, IDE indexers, or the Sphinx package docs.",
            "",
        ]
    )
    return "\n".join(lines)



def convert_eval_rst_blocks(text: str) -> str:
    """Replace MyST {eval-rst} blocks with a compact autodoc target list.

    Converted buchwandler docs embed Sphinx autodoc directives
    (.. autoclass::, .. autofunction::, .. automodule::) inside {eval-rst}
    blocks. Jekyll cannot run autodoc, so render each block as a markdown
    bullet list of the referenced targets. Pure-context directives such as
    .. module:: produce no target and the block is dropped.
    """

    def render(match: "re.Match[str]") -> str:
        inner = match.group(1)
        targets = re.findall(
            r"^\s*\.\.\s+(?:autoclass|autofunction|automodule)::\s+(\S+)",
            inner,
            flags=re.MULTILINE,
        )
        if not targets:
            return ""
        lines = ["Documented via Sphinx autodoc in the source repository:"]
        lines += [f"- `{target}`" for target in targets]
        return "\n".join(lines)

    return re.sub(
        r"^```{eval-rst}\n(.*?)^```\s*$",
        render,
        text,
        flags=re.DOTALL | re.MULTILINE,
    )


def convert_myst_note(text: str) -> str:
    """Convert MyST {note} admonitions to markdown blockquotes."""

    def render(match: "re.Match[str]") -> str:
        body = match.group(1).strip()
        if not body:
            return ""
        lines = []
        for line in body.splitlines():
            lines.append(f"> {line}" if line else ">")
        return "\n".join(lines)

    return re.sub(
        r"^```{note}\n(.*?)^```\s*$",
        render,
        text,
        flags=re.DOTALL | re.MULTILINE,
    )

def parse_toctree_entries(text: str) -> list[str]:
    entries: list[str] = []
    for block in re.findall(r"^```\{toctree\}\n(.*?)^```\s*$", text, flags=re.DOTALL | re.MULTILINE):
        for raw_line in block.splitlines():
            line = raw_line.strip()
            if not line or line.startswith(":"):
                continue
            titled = re.match(r"^.+<([A-Za-z0-9_./-]+)>$", line)
            target = titled.group(1) if titled else line
            if re.match(r"^[A-Za-z0-9_./-]+$", target):
                entries.append(Path(target).stem)

    seen: set[str] = set()
    deduped: list[str] = []
    for entry in entries:
        if entry not in seen:
            seen.add(entry)
            deduped.append(entry)
    return deduped


def strip_sphinx_indices_section(text: str) -> str:
    return re.sub(
        r"\n*#{1,6}\s+Indices and tables\s*\n+(?:[-*]\s+\{ref\}`[^`]+`\s*\n?)+",
        "\n",
        text,
        flags=re.MULTILINE,
    )


def card_label(tool: str, entry: str) -> tuple[str, str]:
    labels = CARD_LABELS.get(tool, {})
    return labels.get(entry, (entry.replace("_", " ").replace("-", " ").title(), "Documentation page."))


def convert_toctree_index(text: str, tool: str) -> str:
    """Replace Sphinx toctree blocks with the card grid used by buchwandler."""
    if "```{toctree}" not in text:
        return text

    entries = parse_toctree_entries(text)
    intro = re.sub(r"\n?^```\{toctree\}\n.*?^```\s*\n?", "\n", text, flags=re.DOTALL | re.MULTILINE)
    intro = strip_sphinx_indices_section(intro).strip()

    cards = ['<div class="cards">']
    for entry in entries:
        label, description = card_label(tool, entry)
        href = "{{ '/tools/" + tool + "/" + entry + "/' | relative_url }}"
        cards.append(
            f'  <section class="card"><h3><a href="{href}">{label}</a></h3>'
            f"<p>{description}</p></section>"
        )
    cards.append("</div>")

    return intro + "\n\n" + "\n".join(cards) + "\n"


def transform_body(text: str, tool: str) -> str:
    body = text.replace("\r\n", "\n").replace("\r", "\n")
    body = convert_code_block_directives(body)
    body = convert_myst_anchors(body)
    body = convert_automodule_page(body)
    body = convert_eval_rst_blocks(body)
    body = convert_myst_note(body)
    body = convert_toctree_index(body, tool)
    return body.strip() + "\n"


def front_matter(slug: str, source_name: str, tool: str, source_text: str) -> str:
    permalink = f"/tools/{tool}/" if slug == "index" else f"/tools/{tool}/{slug}/"
    fallback_title = extract_h1(source_text, f"{tool} {slug.replace('_', ' ').replace('-', ' ')}")
    title = TITLE_OVERRIDES.get(tool, {}).get(slug, fallback_title)
    description = DESCRIPTION_OVERRIDES.get(tool, {}).get(slug, f"{title} documentation")

    return "\n".join(
        [
            "---",
            "layout: tool-doc",
            f"title: {yaml_string(title)}",
            f"description: {yaml_string(description)}",
            f"permalink: {permalink}",
            f"nav_tool: {tool}",
            f"generated_from: {tool}/docs",
            f"source_path: docs/{source_name}",
            "---",
            "",
        ]
    )


def render_page(src: Path, tool: str) -> str:
    slug = src.stem
    source_text = src.read_text(encoding="utf-8")
    body = transform_body(source_text, tool)
    return front_matter(slug, src.name, tool, source_text) + generated_header(tool) + "\n\n" + body


def nav_entries(tool: str, source_files: list[Path]) -> list[dict]:
    """Build ordered nav entries for a tool.

    Order: index first, then the curated TITLE_OVERRIDES keys, then any
    remaining source files sorted by stem. Each entry has slug, title, url.
    """
    curated = TITLE_OVERRIDES.get(tool, {})
    stems = {path.stem: path for path in source_files}

    order: list[str] = []
    seen: set[str] = set()
    if "index" in stems:
        order.append("index")
        seen.add("index")
    for slug in curated:
        if slug in stems and slug not in seen:
            order.append(slug)
            seen.add(slug)
    for slug in sorted(stems):
        if slug not in seen:
            order.append(slug)
            seen.add(slug)

    entries: list[dict] = []
    for slug in order:
        title = curated.get(slug, slug.replace("_", " ").replace("-", " ").title())
        permalink = f"/tools/{tool}/" if slug == "index" else f"/tools/{tool}/{slug}/"
        entries.append({"slug": slug, "title": title, "url": permalink})
    return entries


def render_nav_yaml(tool: str, entries: list[dict]) -> str:
    lines = [
        f"# GENERATED from {tool}/docs. Do not edit by hand.",
        f"tool: {tool}",
        f"repo_url: {yaml_string(TOOL_REPOS[tool])}",
        "entries:",
    ]
    for entry in entries:
        lines.append(f"  - slug: {entry['slug']}")
        lines.append(f"    title: {yaml_string(entry['title'])}")
        lines.append(f"    url: {entry['url']}")
    return "\n".join(lines) + "\n"


def write_nav_data(tool: str, entries: list[dict], data_dir: Path) -> Path:
    nav_dir = data_dir / "tool_nav"
    nav_dir.mkdir(parents=True, exist_ok=True)
    out = nav_dir / f"{tool}.yml"
    out.write_text(render_nav_yaml(tool, entries), encoding="utf-8", newline="\n")
    return out


def sync_docs(
    source_dir: Path,
    dest_dir: Path,
    tool: str,
    clean: bool,
    data_dir: Path | None = None,
) -> tuple[list[Path], Path | None]:
    if tool not in TOOL_REPOS:
        raise SystemExit(f"unsupported tool: {tool}")
    if not source_dir.is_dir():
        raise SystemExit(f"source docs directory does not exist: {source_dir}")

    if data_dir is None:
        # tools/<tool> -> tools -> repo root -> _data
        data_dir = dest_dir.resolve().parent.parent / "_data"

    if clean and dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    source_files = sorted(source_dir.glob("*.md"))
    if not source_files:
        raise SystemExit(f"no markdown files found in {source_dir}")

    written: list[Path] = []
    for src in source_files:
        out = dest_dir / src.name
        out.write_text(render_page(src, tool), encoding="utf-8", newline="\n")
        written.append(out)

    nav_file = write_nav_data(tool, nav_entries(tool, source_files), data_dir)

    return written, nav_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path, help="Path to a buchwandler tool docs directory")
    parser.add_argument("--dest", required=True, type=Path, help="Destination, e.g. tools/booktx")
    parser.add_argument("--tool", default=DEFAULT_TOOL, choices=sorted(TOOL_REPOS))
    parser.add_argument("--no-clean", action="store_true", help="Do not delete destination before writing")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Repository _data directory for the generated tool_nav files (default: <dest>/../../_data)",
    )
    args = parser.parse_args()

    written, nav_file = sync_docs(
        source_dir=args.source,
        dest_dir=args.dest,
        tool=args.tool,
        clean=not args.no_clean,
        data_dir=args.data_dir,
    )
    for path in written:
        print(path)
    if nav_file is not None:
        print(nav_file)


if __name__ == "__main__":
    main()
