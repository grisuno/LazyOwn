# Dual graph + fact-gated todolist

Status: increment 1 shipped (fact gate live, fail-open). This document maps the
four ARTEX campaign-stability mechanisms onto LazyOwn's existing primitives,
states honestly what already exists, and specifies the remaining increments.

## The four mechanisms and where LazyOwn stands

| ARTEX mechanism | LazyOwn today | Gap |
|-----------------|---------------|-----|
| Double graph: global dedup'd asset graph + per-task exploration graph joined by anchors | `AssetGraph` (global, dedupe keys, `coverage`, `coverage_for`, `untested_for`, `scoped`) and `ExplorationGraph` (per-task goal/intent/fact/finding/hint) joined by `ExplorationGraph.anchor` / `anchors_for` | Present. Coverage is not yet the primary driver of the planner frontier. |
| Shared todolist with dispatch gated by facts | Planner emits candidate intents each round; `_initial_access_candidate` guarantees the foothold intent | The dependency gate was missing. Increment 1 adds it (`modules/fact_gated_todolist.py`). |
| Event-driven engine (graph mutation wakes the planner) | Outcome bus + `events.jsonl` + wake waiters + round heartbeat | Round clock is still primary; graph-mutation-as-clock is a later increment. |
| Cross-worker trace exchange | `traffic_<task>.jsonl` + `activity_<task>.jsonl` + trigram evidence index + `vector_facts` TF-IDF digest | The per-step cross-worker query surface is not yet exposed as a tool. |

The dual graph is ~70% built. The net-new contract is the fact gate.

## Fact-gated todolist contract (increment 1, shipped)

`modules/fact_gated_todolist.py` is a pure, framework-free contract:

- `unmet_requirements(requires, facts) -> list[str]` — the predicates no fact
  satisfies (case-insensitive substring match).
- `gate(items, facts) -> {"ready": [...], "blocked": [{"item", "missing"}]}` —
  partitions todolist items by whether their declared `requires` predicates are
  met.

The planner consumes it through `Planner._fact_gate_candidates`, gated by
`payload.json:loop_fact_gate` (default on) and fail-open: a foothold-dependent
candidate (lateral, privesc, exfil per `_foothold_dependent_intent`) is held
back until the engagement proves a foothold fact, so the campaign advances in
evidence order instead of queueing steps that cannot yet succeed. The
initial-access candidate declares no dependency and is never deferred.

Deferral is advisory in effect: a held-back candidate is simply not created this
round; the next planner wake re-evaluates it against the then-current facts, so
a foothold proven mid-campaign releases the dependents automatically.

## Remaining increments (not yet built)

1. Richer predicates: derive `requires` per candidate from its phase and the
   asset/coverage graph (for example, a lateral candidate requires a credential
   fact and a reachable neighbour asset), instead of the single `foothold`
   predicate.
2. Coverage-driven frontier: rank candidates by `AssetGraph.untested_for` so the
   planner explores uncovered scoped assets first.
3. Graph-mutation clock: wake the planner on outcome-bus mutations as the
   primary signal, with the round loop as fallback heartbeat.
4. Cross-worker trace tools: expose `search_all_worker_traces` /
   `get_worker_trace` over the existing trigram index as MCP tools and SDK
   facade methods.

## Tests

- `tests/test_fact_gated_todolist.py` — contract partitioning and the planner
  gate (defer without foothold, release after, flag default, fail-open).
