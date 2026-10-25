# modules/guardrails

*Community 16 | 6 files | cohesion 0.67*

## Definition

This community groups 6 file(s) rooted at `modules/guardrails` with dominant language py (cohesion 0.67). Central symbols: `AdvisoryLedger`, `CapacityEnvelope`, `CheckpointLedger`, `FeatureGate`, `GuardHarness`, `GuardrailContract`, `HarnessAdminPort`, `RunTicket`. Core file: `modules/guardrails/budget.py` (16 symbols). Documented purpose: Operator-facing guardrail harness: tiers, capacity, checkpoints.  Exposes the harness contracts used by the autonomous loop, the APT chain and the orchestrator .

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/guardrails/__init__.py` | py | utility | 0 | yes |
| `modules/guardrails/advisories.py` | py | utility | 15 | yes |
| `modules/guardrails/budget.py` | py | utility | 16 | yes |
| `modules/guardrails/checkpoints.py` | py | utility | 7 | yes |
| `modules/guardrails/contracts.py` | py | utility | 10 | yes |
| `modules/guardrails/harness.py` | py | utility | 11 | yes |

## Key Symbols

- `AdvisoryLedger` (class, `modules/guardrails/advisories.py:17`) `class AdvisoryLedger` - Bounded non-blocking notice stream (newest first).
- `__init__` (method, `modules/guardrails/advisories.py:20`) `def __init__(self, limit)` - Create an empty ledger.
- `notice` (method, `modules/guardrails/advisories.py:31`) `def notice(self, code, message)` - Record one advisory without blocking the caller.
- `tail` (method, `modules/guardrails/advisories.py:49`) `def tail(self, limit)` - Return the newest notices up to the limit.
- `clear` (method, `modules/guardrails/advisories.py:54`) `def clear(self)` - Drop every notice, returning the discarded count.
- `describe` (method, `modules/guardrails/advisories.py:61`) `def describe(self)` - Return the ledger summary for the admin console.
- `tail_locked` (method, `modules/guardrails/advisories.py:66`) `def tail_locked(self, limit)` - Tail helper used by describe; caller holds the lock.
- `FeatureGate` (class, `modules/guardrails/advisories.py:71`) `class FeatureGate` - Optional-feature suspension registry for graceful degradation.
- `__init__` (method, `modules/guardrails/advisories.py:74`) `def __init__(self, features)` - Create a gate limited to the known optional features.
- `suspend` (method, `modules/guardrails/advisories.py:84`) `def suspend(self, feature, reason)` - Suspend one optional feature.
- `resume` (method, `modules/guardrails/advisories.py:102`) `def resume(self, feature)` - Resume one suspended feature, returning True when it changed.
- `resume_all` (method, `modules/guardrails/advisories.py:108`) `def resume_all(self)` - Resume every suspended feature, returning the resumed count.
- `is_suspended` (method, `modules/guardrails/advisories.py:115`) `def is_suspended(self, feature)` - Return True when the feature is currently suspended.
- `suspended` (method, `modules/guardrails/advisories.py:120`) `def suspended(self)` - Return the suspended feature map (feature -> reason).
- `describe` (method, `modules/guardrails/advisories.py:125`) `def describe(self)` - Return the gate state for the admin console.
- `CapacityEnvelope` (class, `modules/guardrails/budget.py:25`) `class CapacityEnvelope` - Fixed-capacity ledger per task class with priority reservation.
- `__init__` (method, `modules/guardrails/budget.py:28`) `def __init__(self, capacities, threshold)` - Seed capacities and the saturation threshold.
- `_default_capacities` (method, `modules/guardrails/budget.py:42`) `def _default_capacities()` - Return the built-in per-class capacity table.
- `configure` (method, `modules/guardrails/budget.py:50`) `def configure(self, capacities, threshold)` - Apply capacity and threshold settings, clamping invalid values.
- `admit` (method, `modules/guardrails/budget.py:78`) `def admit(self, task_class, units)` - Reserve units for one tier honouring the priority contract.
- `account` (method, `modules/guardrails/budget.py:109`) `def account(self, task_class, units)` - Record consumed units for one tier (idempotent on refusal).
- `release` (method, `modules/guardrails/budget.py:118`) `def release(self, task_class, units)` - Return units to a tier ledger once an execution finishes.
- `purge` (method, `modules/guardrails/budget.py:126`) `def purge(self, task_class)` - Zero one tier ledger, returning the freed unit count.
- `reclaim` (method, `modules/guardrails/budget.py:136`) `def reclaim(self)` - Purge SUPPORT allocations, returning the freed unit count.
- `usage` (method, `modules/guardrails/budget.py:140`) `def usage(self, task_class)` - Return current consumed units for one tier.
- `capacity` (method, `modules/guardrails/budget.py:147`) `def capacity(self, task_class)` - Return configured capacity for one tier.
- `saturated` (method, `modules/guardrails/budget.py:154`) `def saturated(self, task_class)` - Return True when the tier usage ratio reaches the threshold.
- `threshold` (method, `modules/guardrails/budget.py:161`) `def threshold(self)` - Return the configured saturation threshold.
- `describe` (method, `modules/guardrails/budget.py:166`) `def describe(self)` - Return a per-tier usage snapshot for the admin console.
- `_usage_ratio` (method, `modules/guardrails/budget.py:171`) `def _usage_ratio(self, tier)` - Compute the usage ratio for one tier; caller holds the lock.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 10
- Cross-boundary resolved imports (EXTRACTED): 10

## Connections

- [EXTRACTED] depends_on community 7 <-> 16 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules/guardrails changed?
- Should modules/guardrails be split, given cohesion 0.67?

## Sources

- `modules/guardrails/__init__.py`
- `modules/guardrails/advisories.py`
- `modules/guardrails/budget.py`
- `modules/guardrails/checkpoints.py`
- `modules/guardrails/contracts.py`
- `modules/guardrails/harness.py`
