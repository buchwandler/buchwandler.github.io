---
goal: "Mirror the ledgerwerk.github.io Jekyll tool-docs structure into buchwandler.github.io, sourcing the per-tool docs from the local epub2text, text2epub, phrasplit, and booktx repositories."
files:
  - "@scripts/sync_tool_docs.py"
  - "@_layouts/default.html"
  - "@_layouts/tool-doc.html"
  - "@assets/css/site.css"
  - "@index.md"
  - "@tools/index.md"
  - "@_data/tool_nav/"
test_commands:
  - "python3 scripts/sync_tool_docs.py --source ../../odoo17/booktx/docs --dest tools/booktx --tool booktx"
  - "bundle exec jekyll build --config _config.yml 2>&1 | tail -20"
expected_outputs:
  - "sync writes tools/<tool>/*.md and _data/tool_nav/<tool>.yml for all four tools"
  - "jekyll build exits 0 with no missing-layout or permalink errors"
acceptance_criteria:
  - id: ac-0001
    text: "Jekyll scaffolding copied from ledgerwerk and rebranded for buchwandler: _layouts/default.html and _layouts/tool-doc.html, assets/css/site.css, home index.md, and tools/index.md exist and the site builds/serves without errors."
    mandatory: true
  - id: ac-0002
    text: "scripts/sync_tool_docs.py registers epub2text, text2epub, phrasplit, booktx as --tool choices and reads both MyST .md and Sphinx .rst docs, emitting Jekyll tool-doc pages with tool-doc front matter."
    mandatory: true
  - id: ac-0003
    text: "Generated docs exist for all four tools under tools/<tool>/ and a _data/tool_nav/<tool>.yml nav file exists for each tool."
    mandatory: true
  - id: ac-0004
    text: "Site navigation, brand, footer, and generated headers reference buchwandler and the four tools; no stale ledgerwerk references remain in rendered pages or nav."
    mandatory: true
todos:
  - id: plan-todo-0001
    text: "Copy _layouts/default.html and _layouts/tool-doc.html from ledgerwerk and rebrand to buchwandler (brand text, nav links to the four tools, footer)."
    mandatory: true
    validation_hint: "grep for 'ledgerwerk' under _layouts and confirm it is gone; verify nav links point at epub2text/text2epub/phrasplit/booktx."
  - id: plan-todo-0002
    text: "Copy assets/css/site.css from ledgerwerk unchanged."
    mandatory: true
    validation_hint: "assets/css/site.css exists and is referenced by _config default layout."
  - id: plan-todo-0003
    text: "Adapt scripts/sync_tool_docs.py: replace TOOL_REPOS/TITLE_OVERRIDES/DESCRIPTION_OVERRIDES/CARD_LABELS with the four buchwandler tools (https://github.com/buchwandler/<tool>), default TOOL to a buchwandler tool, and accept the new --tool choices."
    mandatory: true
    validation_hint: "python3 scripts/sync_tool_docs.py --help shows the four tools; running sync for each tool exits 0."
  - id: plan-todo-0004
    text: "Add .rst handling to scripts/sync_tool_docs.py mirroring the existing MyST transforms: gather both .md and .rst, convert RST title underlines to # headings, convert .. code-block:: to fenced code, convert .. automodule:: to a module list, convert .. toctree:: to the card grid, and strip the Indices and tables section."
    mandatory: true
    validation_hint: "tools/epub2text/*.md and tools/phrasplit/*.md are generated from the RST sources and render headings and code fences correctly."
  - id: plan-todo-0005
    text: "Create home index.md (hero plus cards for the four tools) and tools/index.md (tool index listing the four tools)."
    mandatory: true
    validation_hint: "Both files build with layout: default and link to /tools/<tool>/."
  - id: plan-todo-0006
    text: "Run the sync script for epub2text, text2epub, phrasplit, and booktx from ../../odoo17/<tool>/docs into tools/<tool>."
    mandatory: true
    validation_hint: "tools/<tool>/*.md and _data/tool_nav/<tool>.yml exist for all four tools."
  - id: plan-todo-0007
    text: "Build/serve the site and verify pages render; confirm no ledgerwerk references remain in the repo content."
    mandatory: true
    validation_hint: "bundle exec jekyll build exits 0; grep -ri ledgerwerk . shows no unintended hits."
---

## Goal

Replicate the ledgerwerk.github.io Jekyll "tool docs hub" pattern in buchwandler.github.io, but pointed at four local source repositories: epub2text, text2epub, phrasplit, and booktx (all under ../../odoo17/). The result is a reviewable generated projection of each tool's docs under tools/<tool>/, driven by the sync script, just like ledgerwerk does for archledger/taskledger/releaseledger/ledgercore.

## Context / current state

- buchwandler.github.io already copied the ledgerwerk scaffolding: _config.yml (title buchwandler, url https://buchwandler.de), CNAME (buchwandler.de), Gemfile, Justfile, _config_termux.yml, impressum.md, datenschutz.md, robots.txt.
- scripts/sync_tool_docs.py is byte-identical to ledgerwerk's version (it is hardcoded to the four ledgerwerk tools and only globs *.md).
- Missing vs ledgerwerk: _layouts/ (default.html, tool-doc.html), assets/css/site.css, _data/tool_nav/, tools/, and a home index.md.

## Source repos (all docs/ directories, remotes github.com/buchwandler/<tool>)

- epub2text ../../odoo17/epub2text/docs - 6 .rst (api, changelog, index, installation, structured_extraction, usage)
- phrasplit ../../odoo17/phrasplit/docs - 8 .rst + 1 .md integration.md (api, cli, examples, index, installation, offsets, streaming, usage)
- text2epub ../../odoo17/text2epub/docs - 7 .md (api, cli, getting-started, index, markdown, rebuild, release-checklist)
- booktx ../../odoo17/booktx/docs - 15 .md (agent-workflow, api, architecture, commands, concepts, context, development, epub, index, markdown, profiles, project-layout, quickstart, translation-contract, troubleshooting)

## Key decision: RST handling

ledgerwerk's script only handles MyST .md. Two of the four buchwandler sources are Sphinx .rst (epub2text, phrasplit). "Copy the docs similar to ledgerwerk" therefore requires extending the sync script to read .rst as well as .md and to convert the common Sphinx constructs to Jekyll-friendly markdown, mirroring the existing MyST transforms:

- RST title underlines (=====, -----, ~~~~~ under a line) -> # / ## / ### headings.
- `.. code-block:: lang` and `::` -> fenced ```lang code blocks.
- `.. automodule:: module` blocks -> the same module-list rendering already used for MyST automodule.
- `.. toctree::` blocks -> the existing card grid.
- Strip the `## Indices and tables` section (mirrors the MyST indices strip).
- glob both *.md and *.rst per source dir; output is always *.md.

If the user prefers to keep RST out of scope, plan-todo-0004 can be dropped and epub2text/phrasplit would only carry their .md files (phrasplit's integration.md); the rest of the plan is unaffected.

## Implementation notes

- Rebrand only the human-facing strings: site title/nav/footer (already buchwandler in _config.yml and CNAME). The layouts are copies of ledgerwerk's with the brand, nav links, and footer updated to buchwandler + the four tools.
- The sync script is the single generation mechanism; do not hand-edit generated tools/<tool>/*.md. The header comment and _data/tool_nav/<tool>.yml are regenerated.
- TOOL_REPOS maps the four tools to https://github.com/buchwandler/<tool> (used only for --tool validation and choices, matching ledgerwerk's usage).
- Keep the existing MyST transforms intact so text2epub and booktx .md docs render the same way ledgerwerk's markdown docs do.

## Validation plan

- Run the sync script for each tool from its local docs/ into tools/<tool> and confirm generated files plus _data/tool_nav/<tool>.yml exist.
- Build the site (bundle exec jekyll build or jekyll serve) and confirm no missing-layout, permalink, or Liquid errors.
- grep -ri ledgerwerk . across the repo content to confirm rebranding is complete (expected hits only in .git history, if any).
- Spot-check one RST-derived page (e.g. tools/epub2text/usage/) and one MD-derived page (e.g. tools/booktx/quickstart/) for correct headings, code fences, and nav.
