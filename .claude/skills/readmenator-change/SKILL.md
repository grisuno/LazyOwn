---
name: readmenator-change
description: Safe-change protocol for ReadMenator-indexed repositories. Use before editing, refactoring, deleting, or adding code, and before declaring a task done, to check blast radius, cycles, findings, project rules, and the minimum deliverables recorded in MEMORY.md.
---

# ReadMenator: change code without breaking the map

## Before editing

1. Rules: read sections 3-5 of `readmenator-agent/MEMORY.md` (constraints, style norms,
   minimum deliverables). Declared rules are quoted from the project's instruction files;
   measured baselines are what the code does today. Do not go below a baseline.
2. Blast radius of every file you will touch:

   ```bash
   grep -n '<file>' readmenator-agent/GOTCHAS.md readmenator-agent/SECURITY.md
   ```

   God nodes and high Blast Radius entries need extra tests; a file in a cycle should not gain
   new imports from the other cycle members.
3. Who depends on it: `grep -n '<file>' readmenator-agent/INDEX*.md` (Used by column) or
   `readmenator . ask "<file> dependents" --local`.
4. Grounded recipes: `readmenator-agent/recipes/` (add-function, change-impact, fix-cycle,
   fix-security, reduce-complexity) name the real files of this project.

## While editing

- Match the measured style in MEMORY.md section 4 (naming case, docstring coverage, file size).
- Keep new findings out: `readmenator . audit` lists security findings with fix hints.

## Before saying "done"

1. Run the test command listed in MEMORY.md section 2 and report the result honestly.
2. Check the minimum deliverables in MEMORY.md section 5 one by one.
3. Refresh the knowledge outputs so the next session sees the change:

   ```bash
   readmenator . --rebuild        # or: readmenator . update (incremental)
   readmenator . lint             # architecture linter, exit 1 on errors
   ```

4. Record what the next session must know (see `readmenator-memory`):

   ```bash
   readmenator . remember "Payments retries are capped at 3 because the bank API bans clients" --kind business
   ```
