---
name: readmenator-memory
description: Persist and recall cross-session project knowledge (business rules, decisions and their reasons, workflow, constraints, style norms, done criteria) in readmenator-agent/MEMORY.md. Use at session start to recall, whenever the user states a rule or preference that the code cannot show, after a non-obvious decision, and at session end.
---

# ReadMenator: project memory between sessions

`readmenator-agent/MEMORY.md` has two halves:

- **Generated (sections 1-6)**, rebuilt on every `readmenator . --rebuild` with zero tokens:
  purpose and domain vocabulary, detected workflow commands, declared rules quoted from
  AGENTS.md / CLAUDE.md / CONTRIBUTING.md / .cursorrules (with `file:line`), measured style and
  quality baselines, and structural risks.
- **Session log (section 7)**, written by agents and humans, preserved byte for byte across
  rebuilds and committed with the repo. This is where knowledge that is not in the code lives.

## Recall

```bash
cat readmenator-agent/MEMORY.md                 # or MCP: readmenator.memory
readmenator . ask "<topic>"                     # notes are indexed as GraphRAG sources too
```

## Record

```bash
readmenator . remember "<one-line note>" --kind <kind>
```

MCP: `readmenator.remember {"note": "...", "kind": "decision"}`.

| kind | Use for |
|------|---------|
| business | Domain rules the code cannot express (limits, regulations, customer promises) |
| decision | A choice and its reason ("chose X over Y because Z") |
| rule | A constraint the user stated ("never touch the legacy schema") |
| workflow | How work is done here (release steps, review, environments) |
| style | Conventions not visible in the code |
| deliverable | What "done" means for this team |
| gotcha | A trap you hit and how to avoid it |
| todo | Follow-up that must not be forgotten |
| note | Anything else worth keeping |

## What makes a good note

- One line, self-contained, with the reason: future readers have no conversation context.
- Facts and decisions, not progress logs. Do not store secrets, credentials, or personal data.
- If a note contradicts the code, say which file and line, so the next session can verify.
- Prefer adding the rule to AGENTS.md when it is permanent policy; it then appears in section
  3-5 automatically on the next rebuild.
