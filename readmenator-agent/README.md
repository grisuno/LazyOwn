<!-- readmenator:folder-readme -->
# readmenator-agent

Agent docs: flat, grep-optimized Markdown written for AI coding agents (and humans in a hurry). Every line is self-contained so a single grep answers where a symbol lives, who imports a file, and what is risky to touch.

Generated offline by ReadMenator (static analysis, zero LLM tokens). Files here are rewritten on every run, so do not edit them by hand. To keep a hand-written README in this folder instead, delete the first line of this file.

## Contents

| Path | What it is |
|---|---|
| `MEMORY.md` | Project memory: purpose, workflow commands, declared rules with file:line, style, done criteria, risks, preserved session log |
| `MANIFEST.json` | Freshness stamp (git commit, source fingerprint), subsystems, entry points, read order, document inventory |
| `INDEX*.md` | One row per file: purpose, subsystem, symbol count, importers |
| `SYMBOLS*.md` | One line per symbol with kind and file:line |
| `API*.md` | One line per public function or method with signature and first doc sentence |
| `ARCHITECTURE*.md` | Internal dependency pairs and external imports per file |
| `GOTCHAS*.md` | God nodes, blast radius, hotspots, cycles, layer violations, dataflow leads |
| `SECURITY*.md` | Security findings by severity with CWE and fix hints |
| `CONCEPTS*.md` | Semantic concept vocabulary (nouns and verbs of the codebase) |
| `KB_*.md` | One knowledge page per subsystem (directory) |
| `recipes/` | Grounded task recipes: add a function, change impact, fix a cycle, fix security, reduce complexity |

## How to use

- Start with `cat readmenator-agent/MEMORY.md`, then check freshness with `readmenator . fresh`.
- Locate before reading sources: `grep -n '<keyword>' readmenator-agent/INDEX*.md readmenator-agent/SYMBOLS*.md`.
- Before editing a file: `grep -n '<file>' readmenator-agent/GOTCHAS*.md readmenator-agent/SECURITY*.md`.
- Large documents are paged as `NAME_p2.md`; always grep with `NAME*.md`.

## Regenerate

    readmenator . --rebuild
