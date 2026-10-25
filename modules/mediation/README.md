# Mediation Layer

Coordination without coupling. Colleagues talk to specialised mediators,
never to each other, so no god object appears: each mediator owns one
concern and the hub routes by domain key.

## Structure

| File | Contract |
|------|----------|
| `contracts.py` | Domain keys, ports (`ActivityLogPort`, `LlmCompletionPort`), `resolve()` |
| `hub.py` | `MediationHub` (thin registry, zero business logic), `get_hub()` singleton |
| `intel_mediator.py` | Domain `loop.intel` — lazy_intel routing/masking/signatures + activity log factory |
| `feedback_mediator.py` | Domain `loop.feedback` — orchestrator feedback step ordering |
| `telemetry_mediator.py` | Domain `loop.telemetry` — loop_ai_bridge events, MoE/RL, SWAN |
| `chain_mediator.py` | Domain `chain` — LLM completion port for the apt_chain pipeline |

## Rules

1. Consumers use `resolve(MediationDomains.X)` or `get_hub().mediator_for(x)` — never import the peer module.
2. Each specialised mediator lazily imports its peer at call time, so monkeypatching the peer stays effective and import cycles die.
3. The loop engine registers its own collaborators (`register_activity_log_factory`) at construction.
4. Tests/gym code injects fake ports via `register_llm_port`.
5. Adding a coordination domain = new mediator class + registration in `hub._build_default`; consumers unchanged (OCP).

## Coupled edges mediated (origin)

| Edge | Was | Now |
|------|-----|-----|
| `cli/apt_chain_support.build_llm_recovery_chain -> modules.lazy_loop.LlmPool` | chain importing loop god file | `chain` mediator port |
| `modules/lazy_intel.export_spans -> modules.lazy_loop.ActivityLog` | intel importing loop god file (import cycle) | `loop.intel` activity factory port |
| `modules/lazy_loop -> loop_ai_bridge` (7 call sites) | loop importing bridge directly | `loop.telemetry` mediator |
| `modules/lazy_loop -> lazy_intel / lazy_orchestrator_feedback` (4 call sites) | loop importing peers directly | `loop.intel` / `loop.feedback` mediators |

Tests: `tests/test_mediation.py`.
