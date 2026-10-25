# modules/guardrails

Execution guardrail harness for the autonomous loop, the APT chain and
the orchestrator admin console. Every execution is classified into an
immutable task class, runs under bounded capacity accounting, degrades
gracefully under saturation and recovers from the last checkpoint
instead of crashing the process.

## Contracts

| File | Contract |
|------|----------|
| `contracts.py` | `TaskClass` (CORE=0, MISSION=1, SUPPORT=2), `RunTicket`, `GuardrailContract`, `HarnessAdminPort`, `CONFIG_SECTION` |
| `budget.py` | `CapacityEnvelope`: fixed per-tier capacity, priority reservation (`admit`), accounting (`account`/`release`/`reclaim`), saturation threshold |
| `checkpoints.py` | `CheckpointLedger`: bounded per-key snapshots, `capture`/`restore`, `warm_restart` that never raises |
| `advisories.py` | `AdvisoryLedger`: bounded non-blocking notices; `FeatureGate`: optional-feature suspension |
| `harness.py` | `GuardHarness` facade: `run_guarded`, `warm_restart`, `suspend`/`rearm`, `describe`; `global_harness()` process singleton |

## Execution tiers

| Class | Meaning | Failure policy |
|-------|---------|----------------|
| `CORE` | Loop control cycle, state persistence, safety | Capture checkpoint, warm-restart, retry once, never crash |
| `MISSION` | Task execution, exploit steps, LLM planning | Advisory + None (caller keeps control cycle) |
| `SUPPORT` | Rendering, secondary telemetry, audit tail | Refused first when any higher tier saturates |

Priority rule: a tier may never consume capacity while a higher tier
sits at or above the saturation threshold (default 0.85). `reclaim()`
purges SUPPORT allocations; suspended features resume only through
`rearm()` (operator review) or a clean warm restart.

## Configuration

Settings live in `payload.json` under `orchestrator.guardrails`:

```json
{
  "orchestrator": {
    "guardrails": {
      "saturation_threshold": 0.85,
      "capacity": {"core": 10000, "mission": 2000, "support": 512}
    }
  }
}
```

Administration happens in `cli/lazy_orchestrator.py` (Harness tab):
per-tier usage table, advisories tail, suspended features, warm-restart
and re-arm buttons.

## Wiring

- `modules/lazy_loop.py`: round execution guarded at CORE, worker
  executions guarded at MISSION, harness configured per profile.
- `cli/apt_chain_support.py`: recovery LLM calls guarded at MISSION;
  durable chain checkpoints (`modules/chain_state.py`) carry resume
  state across restarts.
