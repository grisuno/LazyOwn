---
name: readmenator-orient
description: Start-of-session orientation for any repository that has ReadMenator outputs (readmenator-agent/, readmenator-wiki/, KNOWLEDGE_BASE.md). Use at the beginning of every session, after a long break, or whenever you are unsure how the project is organised, before searching or reading source files.
---

# ReadMenator: orient before you read code

ReadMenator writes a static, zero-token map of the repository. Reading it first costs a few
hundred tokens and replaces dozens of file reads. Follow these steps in order and stop as soon
as you have what you need.

## 1. Load the project memory (business rules, workflow, constraints)

```bash
cat readmenator-agent/MEMORY.md
```

Sections 1-6 are regenerated from the code (rules are quoted with `file:line`). Section 7 is
the session log written by previous agents and humans: decisions, business rules, gotchas.
Treat section 7 as authoritative project knowledge unless the user says otherwise.

## 2. Check freshness

```bash
readmenator . fresh || readmenator . --rebuild
```

Exit code 1 means the docs predate the current sources. Without the CLI, compare `git_commit`
in `readmenator-agent/MANIFEST.json` with `git rev-parse HEAD`.

## 3. Big picture

Read `readmenator-wiki/index.md`: communities (subsystems), god nodes (files that everything
depends on), reading order. For a hierarchical summary read
`readmenator-graphrag/REPORTS.md` (root report first, then themes, then communities).

## 4. Locate before you glob

```bash
grep -n '<keyword>' readmenator-agent/INDEX*.md readmenator-agent/SYMBOLS*.md
```

Large docs are paged (`NAME_p2.md`), so always grep `NAME*.md`. For natural-language
questions use the `readmenator-ask` skill instead of grepping.

## 5. Subsystem context

```bash
cat readmenator-agent/KB_<subsystem>.md
```

## Signage cheat sheet

| Need | Where |
|------|-------|
| Business rules, decisions, workflow, style, done criteria | `readmenator-agent/MEMORY.md` |
| What a file is for, who uses it | `readmenator-agent/INDEX*.md` |
| Public functions with signatures | `readmenator-agent/API*.md` |
| Blast radius, cycles, hotspots | `readmenator-agent/GOTCHAS.md` |
| Security findings with fixes | `readmenator-agent/SECURITY.md` |
| Grounded task steps | `readmenator-agent/recipes/*.md` |
| Subsystem overview | `readmenator-wiki/community_*.md` |
| Question answering context | `readmenator . ask "<question>"` |
| Everything, for humans | `KNOWLEDGE_BASE.md`, `readmenator-maps/index.html` |

MCP clients can call `readmenator.memory`, `readmenator.graphrag`, `readmenator.summary`,
`readmenator.explain`, and `readmenator.path` instead of reading files
(`readmenator-mcp .` starts the server).
