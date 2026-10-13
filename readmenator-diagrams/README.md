<!-- readmenator:folder-readme -->
# readmenator-diagrams

Component diagrams: the codebase as a handful of components (code communities) with the relations between them, method-level key edges and call-site evidence.

Generated offline by ReadMenator (static analysis, zero LLM tokens). Files here are rewritten on every run, so do not edit them by hand. To keep a hand-written README in this folder instead, delete the first line of this file.

## Contents

| Path | What it is |
|---|---|
| `analysis.json` | Component model: files, methods index, components, relations |
| `overview.md` | Top-level `graph LR` diagram with related classes and methods |
| `*.md` | One page per expandable component (nested diagram) |
| `index.html` | Offline interactive layered diagram |

## How to use

- Start at `readmenator-diagrams/overview.md` or open `index.html`.

## Regenerate

    readmenator . components
    readmenator . --rebuild
