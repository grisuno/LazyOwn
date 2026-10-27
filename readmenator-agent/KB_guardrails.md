# Subsystem: guardrails

## modules/guardrails/__init__.py
- Doc: Operator-facing guardrail harness: tiers, capacity, checkpoints.
- Layer: utility
- Language: py
- Depends on: `modules/guardrails/advisories.py`, `modules/guardrails/budget.py`, `modules/guardrails/checkpoints.py`, `modules/guardrails/contracts.py`, `modules/guardrails/harness.py`
- Imported by: `cli/apt_chain_support.py`, `cli/orchestrator_assets_tabs.py`, `modules/lazy_loop.py`, `tests/test_guardrails.py`

## modules/guardrails/advisories.py
- Doc: Non-blocking advisories and feature degradation.
- Layer: utility
- Language: py
- Symbols:
  - `AdvisoryLedger` (class, line 17) `class AdvisoryLedger`
  - `FeatureGate` (class, line 71) `class FeatureGate`
  - `__init__` (method, line 20) `def __init__(self, limit)`
  - `notice` (method, line 31) `def notice(self, code, message)`
  - `tail` (method, line 49) `def tail(self, limit)`
  - `clear` (method, line 54) `def clear(self)`
  - `describe` (method, line 61) `def describe(self)`
  - `tail_locked` (method, line 66) `def tail_locked(self, limit)`
  - `__init__` (method, line 74) `def __init__(self, features)`
  - `suspend` (method, line 84) `def suspend(self, feature, reason)`
  - `resume` (method, line 102) `def resume(self, feature)`
  - `resume_all` (method, line 108) `def resume_all(self)`
  - `is_suspended` (method, line 115) `def is_suspended(self, feature)`
  - `suspended` (method, line 120) `def suspended(self)`
  - `describe` (method, line 125) `def describe(self)`
- Imported by: `modules/guardrails/__init__.py`, `modules/guardrails/harness.py`

## modules/guardrails/budget.py
- Doc: Bounded capacity accounting with strict priority reservation.
- Layer: utility
- Language: py
- Symbols:
  - `CapacityEnvelope` (class, line 25) `class CapacityEnvelope`
  - `__init__` (method, line 28) `def __init__(self, capacities, threshold)`
  - `_default_capacities` (method, line 42) `def _default_capacities()`
  - `configure` (method, line 50) `def configure(self, capacities, threshold)`
  - `admit` (method, line 78) `def admit(self, task_class, units)`
  - `account` (method, line 109) `def account(self, task_class, units)`
  - `release` (method, line 118) `def release(self, task_class, units)`
  - `purge` (method, line 126) `def purge(self, task_class)`
  - `reclaim` (method, line 136) `def reclaim(self)`
  - `usage` (method, line 140) `def usage(self, task_class)`
  - `capacity` (method, line 147) `def capacity(self, task_class)`
  - `saturated` (method, line 154) `def saturated(self, task_class)`
  - `threshold` (method, line 161) `def threshold(self)`
  - `describe` (method, line 166) `def describe(self)`
  - `_usage_ratio` (method, line 171) `def _usage_ratio(self, tier)`
  - `_snapshot_locked` (method, line 176) `def _snapshot_locked(self)`
- Depends on: `modules/guardrails/contracts.py`
- Imported by: `modules/guardrails/__init__.py`, `modules/guardrails/harness.py`

## modules/guardrails/checkpoints.py
- Doc: Checkpoint ledger with warm-restart recovery.
- Layer: utility
- Language: py
- Symbols:
  - `CheckpointLedger` (class, line 18) `class CheckpointLedger`
  - `__init__` (method, line 21) `def __init__(self, history)`
  - `capture` (method, line 33) `def capture(self, key, state)`
  - `restore` (method, line 51) `def restore(self, key)`
  - `keys` (method, line 59) `def keys(self)`
  - `warm_restart` (method, line 64) `def warm_restart(self, core_key)`
  - `describe` (method, line 92) `def describe(self)`
- Imported by: `modules/guardrails/__init__.py`, `modules/guardrails/harness.py`

## modules/guardrails/contracts.py
- Doc: Contracts for the execution guardrail harness.
- Layer: utility
- Language: py
- Symbols:
  - `TaskClass` (class, line 19) `class TaskClass(IntEnum)`
  - `RunTicket` (class, line 40) `class RunTicket`
  - `GuardrailContract` (class, line 49) `class GuardrailContract(Protocol)`
  - `HarnessAdminPort` (class, line 73) `class HarnessAdminPort(Protocol)`
  - `is_known` (method, line 31) `def is_known(cls, value)`
  - `describe` (method, line 52) `def describe(self)`
  - `run_guarded` (method, line 56) `def run_guarded(self, task_class, fn)`
  - `warm_restart` (method, line 68) `def warm_restart(self)`
  - `configure` (method, line 76) `def configure(self, settings)`
  - `rearm` (method, line 80) `def rearm(self)`
- Depends on: `cli/commands/enum.py`
- Imported by: `modules/guardrails/__init__.py`, `modules/guardrails/budget.py`, `modules/guardrails/harness.py`

## modules/guardrails/harness.py
- Doc: Execution harness facade: guarded runs, warm restart, degradation.
- Layer: utility
- Language: py
- Symbols:
  - `GuardHarness` (class, line 25) `class GuardHarness`
  - `global_harness` (function, line 232) `def global_harness()`
  - `reset_global_harness` (function, line 241) `def reset_global_harness()`
  - `__init__` (method, line 28) `def __init__(self, threshold, capacities)`
  - `configure` (method, line 48) `def configure(self, settings)`
  - `run_guarded` (method, line 63) `def run_guarded(self, task_class, fn)`
  - `warm_restart` (method, line 124) `def warm_restart(self, core_key)`
  - `suspend` (method, line 138) `def suspend(self, feature, reason)`
  - `rearm` (method, line 153) `def rearm(self)`
  - `describe` (method, line 165) `def describe(self)`
  - `_on_failure` (method, line 174) `def _on_failure(self, tier, ticket, key, fn, args, kwargs, exc)`
- Depends on: `modules/guardrails/advisories.py`, `modules/guardrails/budget.py`, `modules/guardrails/checkpoints.py`, `modules/guardrails/contracts.py`
- Imported by: `modules/guardrails/__init__.py`, `tests/conftest.py`
