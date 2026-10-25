# Subsystem: sinks

## modules/sinks/__init__.py
- Doc: Outcome sink adapters.
- Layer: utility
- Language: py

## modules/sinks/attack_graph.py
- Doc: Attack-graph sink: rebuild the attack surface after meaningful outcomes.
- Layer: utility
- Language: py
- Symbols:
  - `apply` (function, line 13) `def apply(event)`
- Depends on: `modules/attack_surface3d.py`, `modules/outcome_bus.py`
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

## modules/sinks/event_bus.py
- Doc: Unified event-bus sink: publish every outcome once.
- Layer: infrastructure
- Language: py
- Symbols:
  - `apply` (function, line 9) `def apply(event)`
- Depends on: `modules/event_bus.py`, `modules/outcome_bus.py`

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
- Depends on: `modules/lazy_intel.py`, `modules/outcome_bus.py`
- Imported by: `skills/lazyown_mcp.py`

## modules/sinks/world_model.py
- Doc: World-model sink: hosts, services, vulnerabilities and credentials.
- Layer: business_logic
- Language: py
- Symbols:
  - `apply` (function, line 12) `def apply(event)`
- Depends on: `modules/obs_parser.py`, `modules/outcome_bus.py`, `modules/world_model.py`
