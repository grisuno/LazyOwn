---
name: readmenator-receipts
description: Ingest deploynator release receipts into the repository knowledge base and turn observed release evidence into graph edges, RELEASES.md and predictions. Use whenever the user mentions release receipts, "what did the last release actually do", deploynator --receipt/--trace output, release evidence, or asks to reconcile observed versus candidate versus predicted edges.
---

# ReadMenator: release receipts as evidence, not prose

Deploynator can write a receipt JSON on every release (`deploynator release --receipt`,
or `--dry-run --trace` for a feasible plan). `readmenator . receipts` reconciles those
receipts against this repository's static symbol index and writes the release layer of
the knowledge base.

## Golden rule

`Fact = observed step (exit_code)`. `Candidate = feasible set from config/CLI/interface`.
`Predicted = model, always labeled with version and provenance`. A prediction is never
presented as fact.

## 1. Ingest

```bash
readmenator . receipts [dir]     # default dir: release-receipts/
```

Reads every receipt JSON (oldest first, invalid files skipped, bounded history), maps
captured commands to callers (`git` -> GitOperations, `gh`/`glab`/`bb` -> platform CLIs,
stages like `release:<platform>` -> `Platform.create_release`), and writes:

| Output | Content |
|--------|---------|
| `readmenator-releases/RELEASES.md` | One section per release: version, mode, status, platforms, key facts |
| `readmenator-releases/release-edges.json` | `confirmed_edges` (observed implements candidate), `unobserved_edges` (candidate with no receipt evidence), `predicted_edges` (model, with confidence + provenance + model version) |

Predictions stay in the JSON; RELEASES.md lists only confirmed and unobserved edges.

## 2. Classify before you conclude

- `confirmed` edge: the candidate caller had a receipt command with `exit_code == 0`.
- `unobserved` edge: the interface makes it possible (config/CLI/contract) but no
  receipt ever observed it. Report it as feasible, not as history.
- `predicted` edge: produced by `readmenator/_uncertainty.py` (heuristic scorer plus
  optional sklearn random forest). Always carries `provenance: predicted` and a model
  version. Quote the confidence number; never round it up in prose.

## 3. Validate LLM/agent proposals (optional, offline)

Hypotheses (`readmenator/_hypotheses.py`) are constrained by the symbol index:

```bash
readmenator . receipts [dir]   # then inspect release-edges.json predicted_edges
```

An LLM may propose new edges as JSON; the validator rejects them unless the callee
exists in `SYMBOLS*.md` evidence. Unverifiable proposals stay `unobserved`, never
`confirmed`. Proposing without validation is a contract violation.

## 4. Chain with other layers

- Caller/callee symbols: grep `readmenator-agent/SYMBOLS*.md`.
- Workflow context: `readmenator-agent/MEMORY.md` section 7.
- Question answering over releases: `readmenator . ask "<question>"` after ingestion.

## Signage cheat sheet

| Need | Where |
|------|-------|
| Release narrative | `readmenator-releases/RELEASES.md` |
| Edge evidence with confidence | `readmenator-releases/release-edges.json` |
| Raw receipt source of truth | `release-receipts/*.json` |
| Symbol existence check | `readmenator-agent/SYMBOLS*.md` |
