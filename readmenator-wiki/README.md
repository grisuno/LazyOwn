<!-- readmenator:folder-readme -->
# readmenator-wiki

Agent wiki: the big picture as a navigable, progressively disclosed wiki. One page per code community (group of files that import each other), plus typed connections between them and an honest audit of what was extracted vs inferred.

Generated offline by ReadMenator (static analysis, zero LLM tokens). Files here are rewritten on every run, so do not edit them by hand. To keep a hand-written README in this folder instead, delete the first line of this file.

## Contents

| Path | What it is |
|---|---|
| `index.md` | Entry point: overview, stats, reading order, god nodes, strongest connections |
| `community_*.md` | One page per community: definition, files, key symbols, edges, risks, open questions |
| `connections.json` | Typed bridges between communities with confidence and strength |
| `concepts.md` | Concept graph summary |
| `concept_graph.json` | Concept graph data (nouns as nodes, verbs as edges) |
| `queries.md` | Suggested questions plus an append-only answer log |
| `REPORT.md` | Audit: EXTRACTED vs INFERRED vs AMBIGUOUS counts, coverage, orphans, limits |

## How to use

- Read `readmenator-wiki/index.md` first, then open the community page of the area you touch.
- Check health with `readmenator . lint-wiki` (exit 1 on issues).

## Regenerate

    readmenator . wiki
    readmenator . --rebuild
