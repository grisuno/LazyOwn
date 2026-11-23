# LLM Circuit Breaker Doctrine

Formal pattern, already implemented. This document is the contract every
LLM consumer must honor. Reinforce, do not reimplement.

## Components

| Component | Home | Responsibility |
|---|---|---|
| `HealthRegistry` | `modules/llm_pool.py` | Per-member breaker state, persisted to `sessions/lazy/llm_health.json` |
| `LlmPool.complete` | `modules/lazy_loop.py` | Chain failover, consults + feeds the registry |
| `LLMConnectRetries` | `modules/lazy_loop.py` | Bounded connect retries with short backoff |

## Breaker tiers

1. **Soft trip** — 3 consecutive transient failures park a member.
   Backoff tiers: 1m → 5m → 30m. Next success resets the counter.
2. **Hard trip** — auth/quota errors (401/402/quota wording) park a
   member immediately until the tier window expires.
3. **TPD trip** — daily-quota wording (429 tokens-per-day) parks the
   member for 4 hours, not one backoff tier.

## Call contract

- `complete()` skips every parked member (logged as
  `"<name> parked by breaker; trying next member"`).
- When every member is parked or fails, `complete()` returns `""`.
  It never raises through the workflow.
- Every caller MUST degrade on `""`:

  | Caller | Degradation |
  |---|---|
  | Command judge | `fail_policy` (`ALLOW`/`DENY` per configured policy) |
  | Planner `_candidates()` | heuristic intent proposals from scan briefs/verb priors |
  | Workers | deterministic verb chain (no LLM step) |
  | `daemon_selectors` | falls back to direct backend, then to none |

## Rules for new LLM consumers

1. Resolve the pool through `modules.llm_pool` / `lazy_loop.LlmPool`.
   Never call `llm_factory.complete` directly in a loop path.
2. Treat the empty string as "LLM unavailable" and ship a working
   heuristic branch in the same PR.
3. Never sleep on failures outside the pool: the registry owns pacing.
4. Report outcomes: success/failure flow through `pool.complete`
   automatically; ad-hoc `HealthRegistry` writes are reserved for the
   pool itself.
