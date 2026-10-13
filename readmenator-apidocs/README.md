<!-- readmenator:folder-readme -->
# readmenator-apidocs

API reference in the style of Sphinx and Doxygen: every module, class, function and constant with exact signatures, parsed docstrings, inheritance, callers and callees, documentation coverage and doc warnings.

Generated offline by ReadMenator (static analysis, zero LLM tokens). Files here are rewritten on every run, so do not edit them by hand. To keep a hand-written README in this folder instead, delete the first line of this file.

## Contents

| Path | What it is |
|---|---|
| `index.md` | Modules by package with coverage |
| `modules/` | One Markdown page per module (signatures, parameters, returns, raises, call graph) |
| `classes.md` | Class hierarchy |
| `genindex.md` | A-Z general index |
| `COVERAGE.md` | Documentation coverage and DOC00x warnings |
| `architecture.md` | Tiered architecture and execution flows (Mermaid) |
| `flows.html` | Interactive architecture and execution-flow diagrams |
| `index.html` | Offline searchable HTML API browser (open in a browser) |
| `api/index.json` | Machine-readable model index: meta, coverage, module list, grep examples |
| `api/modules/` | One JSON Lines file per module, one entity per line |
| `api/warnings.jsonl` | One documentation warning per line |

## How to use

- Humans: open `readmenator-apidocs/index.html` or start at `index.md`.
- Agents: `grep -h '"name":"<Name>"' readmenator-apidocs/api/modules/*.jsonl`.
- Gate documentation in CI: `readmenator . doc-coverage --fail-under 80`.

## Regenerate

    readmenator . apidocs
    readmenator . --rebuild
