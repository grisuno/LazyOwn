# Outcome Bus Specification

I define one fan-out contract for engagement outcomes. Every exploit,
emulation step, chain result and loop finding publishes one event.

## Event

`modules/outcome_bus.py`:

- identity: `kind`, `target`, `host`, `task_id`, `intent_id`, `source`;
- content: `title`, `description`, `severity`, `cve`, `mitre_id`,
  `confidence`, `command`, `output`;
- proof: `success`, `shell`, `artifacts`;
- service: `port`, `protocol`, `service`, `banner`;
- routing: `sinks`, `metadata`.

`key()` hashes identity and proof fields. Repeating the same event in one
process returns the cached statuses with `_deduplicated` and does not run
the sinks again.

## Sinks

Sinks live in `modules/sinks/` and expose `apply(event) -> bool`.
Default order:

1. `world_model`
2. `killchain`
3. `routing`
4. `c2_surfaces`
5. `objectives`
6. `event_bus`
7. `intel_graph`
8. `attack_graph`
9. `report`

`campaign_db` is available but opt-in.

The bus owns ordering, payload toggles from
`config/orchestrator.yaml -> profiles.<name>.sinks`, and failure
isolation. One sink exception becomes `False`; the rest still run.

## Audit

Every decision appends to `sessions/outcomes.jsonl` with the event and
per-sink status. The write is best-effort and never raises.

## Acceptance

- Default sinks cover the world model, kill-chain, routing, C2, objectives,
  event bus, intel graph, attack graph and report.
- A failing sink does not block the others.
- Payload toggles remove sinks.
- Duplicate events run once per process.
- Tests: `tests/test_outcome_bus.py`.
- Mutation: `tests/run_mutation_outcome_bus.py`.
