# Subsystem: sinks

## modules/sinks/__init__.py
- Doc: Outcome sink adapters.
- Layer: utility
- Language: py
- Imported by: `tests/test_lazy_ledger.py`

## modules/sinks/attack_graph.py
- Doc: Attack-graph sink: rebuild the attack surface after meaningful outcomes.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 13) `def apply(event)`
- Depends on: `modules/attack_surface3d.py`, `modules/outcome_bus.py`
- Imported by: `tests/test_outcome_bus.py`

## modules/sinks/beacon_dispatch.py
- Doc: Beacon dispatch sink: on a foothold, stage the catch-back command.
- Layer: utility
- Language: py
- Symbols:
  - `_load_payload` (function, line 23) `def _load_payload()`
  - `_copy_clipboard` (function, line 34) `def _copy_clipboard(text)`
  - `apply` (function, line 46) `def apply(event)`
- Depends on: `core/config.py`, `core/hardening.py`, `modules/outcome_bus.py`, `modules/payload_factory.py`
- Imported by: `tests/test_outcome_bus.py`

## modules/sinks/c2_surfaces.py
- Doc: C2 dashboard sink: banners, CVEs and operator notes.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 11) `def apply(event)`
- Depends on: `modules/c2_surfaces.py`, `modules/outcome_bus.py`
- Imported by: `tests/test_outcome_bus.py`

## modules/sinks/campaign_db.py
- Doc: Campaign database sink: opt-in host and vulnerability mirror.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 9) `def apply(event)`
- Depends on: `modules/db.py`, `modules/outcome_bus.py`

## modules/sinks/chain_feed.py
- Doc: Chain-feed sink: stream chain steps into the autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 22) `def apply(event)`
- Depends on: `modules/lazy_loop.py`, `modules/outcome_bus.py`
- Imported by: `tests/test_sink_chain_feed.py`

## modules/sinks/event_bus.py
- Doc: Unified event-bus sink: publish every outcome once.
- Layer: infrastructure
- Language: py
- Symbols:
  - `apply` (function, line 9) `def apply(event)`
- Depends on: `modules/event_bus.py`, `modules/outcome_bus.py`

## modules/sinks/findings.py
- Doc: Findings sink: append engagement finding transitions to the ledger.
- Layer: utility
- Language: py
- Symbols:
  - `limits_for` (function, line 22) `def limits_for()`
  - `apply` (function, line 42) `def apply(event)`
  - `ledger_for` (function, line 72) `def ledger_for(engagement_id)`
  - `handoff` (function, line 88) `def handoff(engagement_id, status, rounds)`
  - `ingest_discarded` (function, line 107) `def ingest_discarded(engagement_id, entries)`
- Depends on: `core/logging.py`, `modules/__init__.py`, `modules/orchestrator_config.py`, `modules/outcome_bus.py`
- Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`

## modules/sinks/intel_graph.py
- Doc: Intel-graph sink: rebuild the fused graph after meaningful outcomes.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 13) `def apply(event)`
- Depends on: `modules/intel_fusion.py`, `modules/outcome_bus.py`
- Imported by: `tests/test_outcome_bus.py`

## modules/sinks/killchain.py
- Doc: Kill-chain sink: advance the unified phase from proven outcomes.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 11) `def apply(event)`
- Depends on: `modules/killchain.py`, `modules/outcome_bus.py`
- Imported by: `tests/test_outcome_bus.py`

## modules/sinks/objectives.py
- Doc: Objectives sink: turn proven outcomes into follow-up work.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 16) `def apply(event)`
- Depends on: `modules/outcome_bus.py`
- Imported by: `tests/test_outcome_bus.py`

## modules/sinks/routing.py
- Doc: Routing-prior sink: learn from terminal outcomes.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 9) `def apply(event)`
- Depends on: `modules/lazy_intel.py`, `modules/lazy_ledger.py`, `modules/outcome_bus.py`
- Imported by: `skills/lazyown_mcp.py`

## modules/sinks/world_diff.py
- Doc: World-diff sink: snapshot hosts and record what changed per outcome.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 14) `def apply(event)`
  - `_stored_host` (function, line 52) `def _stored_host(root, host)`
  - `_current_host` (function, line 58) `def _current_host(root, host)`
  - `_store_host` (function, line 65) `def _store_host(root, host, snapshot)`
- Depends on: `modules/lazy_world_diff.py`, `modules/outcome_bus.py`, `modules/world_model.py`
- Imported by: `tests/test_outcome_bus.py`, `tests/test_world_diff_retest.py`

## modules/sinks/world_model.py
- Doc: World-model sink: hosts, services, vulnerabilities and credentials.
- Layer: business_logic
- Language: py
- Symbols:
  - `apply` (function, line 12) `def apply(event)`
- Depends on: `modules/obs_parser.py`, `modules/outcome_bus.py`, `modules/world_model.py`
