---
name: readmenator-ask
description: Answer questions about a ReadMenator-indexed codebase with GraphRAG retrieval (BM25 + Personalized PageRank over files, symbols, concepts, and source excerpts; map-reduce over community reports). Use for "where/how/why does X", "what handles Y", "what are the main subsystems or risks", before opening source files.
---

# ReadMenator: ask the graph

The GraphRAG index in `readmenator-graphrag/` was built offline from the static scan (zero LLM
tokens). Querying it returns a compact, cited Markdown context; you spend tokens only on reading
the answer.

## Commands

```bash
readmenator . ask "how are communities detected"            # auto: local or global
readmenator . ask "PersonalizedPageRank seeds" --local      # entity-centric
readmenator . ask "main subsystems and risks" --global      # corpus-wide, from community reports
readmenator . ask "taint propagation" --budget 1500         # cap the context (tokens)
readmenator . graphrag                                      # rebuild only the index
```

MCP: `readmenator.graphrag {"query": "...", "mode": "auto|local|global", "budget_tokens": 0}`;
resource `readmenator://graphrag` returns all community reports.

## Which mode

- **local** (specific names, behaviours, "where is", "how does X work"): BM25 finds matching
  entities and source chunks, Personalized PageRank spreads relevance through imports, calls,
  inheritance and definitions, and you get Entities (with `file:line`), Relationships,
  Community reports, and Sources (real code excerpts).
- **global** (architecture, themes, risks, "overview of"): community reports are scored
  against the query and their matching findings are mapped and reduced into one context,
  headed by the project root report.
- **auto** picks global for broad words or when no entity matches.

## How to use the answer

1. Trust `file:line` citations and open only the cited lines (`sed -n 'A,Bp' file`).
2. Follow Relationships to neighbouring files instead of globbing.
3. Ratings in community reports are 7 x PageRank share + 3 x severity-weighted risk: high
   rating means central and risky, so read its GOTCHAS before editing.
4. If the context says "No entity matches", rephrase with identifiers or switch to `--global`.
5. Session-log notes from `readmenator-agent/MEMORY.md` are indexed as `memory` sources: a hit
   there is a recorded business rule or decision and outranks your inference.
