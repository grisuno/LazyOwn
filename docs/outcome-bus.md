# Outcome Bus

I route every engagement outcome through one contract. Exploits,
emulation steps, chain results and loop findings publish an
`OutcomeEvent`; the bus calls the configured sink adapters in order and
writes one audit row.

## Why

Before the bus, each execution path fed a different subset of the
surfaces. An exploit updated the world model, the kill-chain and the C2
tables; a playbook step updated only the world model; a chain updated
nothing. Identical results produced different intelligence depending on
which door ran them. The bus closes that gap without making any caller
know every surface.

## Event

`modules/outcome_bus.py` defines `OutcomeEvent`:

- identity: `kind`, `target`, `host`, `task_id`, `intent_id`, `source`;
- content: `title`, `description`, `severity`, `cve`, `mitre_id`,
  `confidence`, `command`, `output`;
- proof: `success`, `shell`, `artifacts`;
- service context: `port`, `protocol`, `service`, `banner`;
- routing: `sinks`, `metadata`.

`OutcomeEvent.key()` is the idempotency key. Repeating the same event in
one process returns the cached statuses with `_deduplicated` set and
does not call the sinks again.

## Sinks

Sinks live in `modules/sinks/`, one file per surface, each exposing
`apply(event) -> bool`. The bus owns ordering, payload toggles and
failure isolation. A sink exception becomes `False`; the remaining
sinks still run.

Default order follows `SINK_LOADERS`: `world_model`, `killchain`,
`lazy_intel`, `findings`, `routing`, `c2_surfaces`, `objectives`,
`event_bus`, `intel_graph`, `attack_graph`, `world_diff`,
`beacon_dispatch`, `report`, `campaign_db`, `chain_feed`.

`campaign_db` is now a default sink. It no longer opens SQLite on the hot
path: the sink hands its host and vulnerability mirror to the
single-writer queue in `modules/db_writer.py`, which applies the write on
one dedicated writer thread bound to one WAL-mode connection. The sink
returns as soon as the operation is accepted, so routine loop traffic
never blocks on database I/O. A full queue drops the write with a debug
log rather than blocking the caller, and `DBWriteQueue.flush()` drains the
queue for tests and graceful shutdown. Disable the sink per profile with
`config/orchestrator.yaml -> profiles.<name>.sinks.campaign_db: false`.

## Configuration

`config/orchestrator.yaml -> profiles.<name>.sinks` toggles every sink.
`payload.json -> orchestrator` can override the same names. Explicit
callers may pass `sinks=[...]`; the event `sinks` list is additive.

## Audit

Every decision appends to `sessions/outcomes.jsonl`:

```json
{"ts": 0, "event": {"kind": "exploit", "...": "..."}, "sinks": {"world_model": true, "attack_graph": true}}
```

The audit row is best-effort; a full disk never blocks an engagement.

## Tests

- `tests/test_outcome_bus.py`: fan-out, dedupe, toggles, failure
  isolation, C2/objectives/report/graph sinks, bridge mapping, and the
  non-blocking `campaign_db` default sink.
- `tests/test_db_writer.py`: single-writer persistence, non-blocking
  submit under a full queue, failure isolation, synchronous mode.
- `tests/run_mutation_outcome_bus.py`: four mutants, all killed.
