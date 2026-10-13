<!-- readmenator:folder-readme -->
# readmenator-graphrag

Zero-token GraphRAG index: entities, relationships, community reports and source text units built deterministically from the code graph, so questions can be answered with ranked, budgeted context instead of reading the whole repository.

Generated offline by ReadMenator (static analysis, zero LLM tokens). Files here are rewritten on every run, so do not edit them by hand. To keep a hand-written README in this folder instead, delete the first line of this file.

## Contents

| Path | What it is |
|---|---|
| `index.json` | Index header with schema version and counts |
| `entities.jsonl` | One entity per line: files, symbols, concepts, externals |
| `relationships.jsonl` | One relationship per line: imports, calls, inherits, defines, documents |
| `communities.jsonl` | Community report hierarchy (communities, themes, root) |
| `text_units.jsonl` | Source text units per symbol (empty in privacy mode) |
| `REPORTS.md` | Human-readable community reports |

## How to use

- Ask questions: `readmenator . ask "<question>"` (`--global` for overviews, `--local` for specifics).
- The JSONL files are one record per line, so `grep` works directly on them.

## Regenerate

    readmenator . graphrag
    readmenator . --rebuild
