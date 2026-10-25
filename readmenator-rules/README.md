<!-- readmenator:folder-readme -->
# readmenator-rules

Rules: Semgrep rules suggested from patterns actually found in the code, plus the YARA-lite rules and the false-positive exclusion list used by the security audit.

Generated offline by ReadMenator (static analysis, zero LLM tokens). Files here are rewritten on every run, so do not edit them by hand. To keep a hand-written README in this folder instead, delete the first line of this file.

## Contents

| Path | What it is |
|---|---|
| `readmenator_*.yml` | Suggested Semgrep rules (all languages and per language) |

## How to use

- Run the suggestions: `semgrep --config readmenator-rules/`.
- Validate the YARA-lite rules: `readmenator . validate-rules`.

## Regenerate

    readmenator . export-rules
    readmenator . --rebuild
