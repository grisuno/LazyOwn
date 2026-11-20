# modules/loop

Cohesive behaviour mixins extracted from the two god classes in
`modules/lazy_loop.py` (`Worker` and `LazyLoopEngine`). Each mixin owns one
responsibility so a change to scope policy, worker memory or the recorder proxy
touches a small file instead of the thousand-line host class. The mixins follow
the house pattern already used by
`cli/orchestrator_assets_tabs.py` (`OrchestratorAssetsMixin`): plain classes
that bind to the host object through `self` and carry no state of their own.

## Files

| File | Role |
|------|------|
| `__init__.py` | Re-exports the mixins for `from modules.loop import ...`. |
| `worker_gating.py` | `WorkerGatingMixin`: scope, operating-system and passwordless-sudo gates applied before a command reaches the shell. |
| `worker_memory.py` | `WorkerMemoryMixin`: durable failure memory, task-scoped vector memory and reactive absorption of command output. |
| `worker_execution.py` | `WorkerExecutionMixin`: command dispatch through the executor or registry, tracked background jobs, the persistent bash session, alias resolution and the deny/auto-approve/missing-binary admissibility helpers. |
| `worker_agentic.py` | `WorkerAgenticMixin`: the guard-enforced tool catalogue, the agent system prompt, the multi-attempt tool-calling session, operator-steer drainage, stop-reason checkpoints and the deterministic LLM step suggestions. |
| `engine_proxy.py` | `EngineProxyMixin`: the `LazyLoopEngine` recorder-proxy lifecycle (`proxy_start`/`stop`/`status`/`env`), per-task traffic ingestion, body search and the retention sweep. |
| `triage_scheduler.py` | `TriageScheduler` + `estimate_difficulty`: difficulty-triage scheduling for the multi-target queue (easy-first ordering, deadline salvage of partials, stop-loss). Pure; `LazyLoopEngine.drain_queue` uses it when `loop_triage_enabled` is set. |
| `state_db.py` | Shared SQLite WAL substrate (`sessions/db/loop_state.db`, gitignored) with `connect`/`thread_connection`; one file backs claim leases and token usage. |
| `leases.py` | `LeaseStore`: transactional claim leases keyed by `(task_id, node_id)` — CAS claim under `BEGIN IMMEDIATE`, heartbeat, settle (a settled intent never re-claims), release and sweep of provably-dead claims back to pending. `ExplorationGraph.compare_and_claim` acquires the lease before the flock-persist, `set_state` settles/releases on terminal/requeue transitions, `Budget.record_toolcall` heartbeats the claim, and the engine run loop sweeps expired leases each round. Config: orchestrator profile `leases: {enabled, ttl_sec, heartbeat_sec}`. |
| `tokens.py` | `TokenLedger` (SQLite) + `TerminationPolicy`: estimated token spend per task and per intent (prompt/completion characters registered as an `llm_pool` usage sink), a wrap-up reserve kept aside, and the `save_tokens` vs `try_hard` termination modes — `save_tokens` wraps the loop up cleanly when the spend cap is reached (no terminal auto_pwn fallback), `try_hard` degrades to the deterministic layer only (planner stops emitting LLM intents). `Budget.check` reports the token verdict; `Planner.plan` honours `deterministic_only`. Config: profile `termination: {mode, max_tokens_per_task, max_tokens_per_intent, wrapup_reserve_pct, wrapup_reserve_tokens}`. |
| `boundary.py` | Untrusted-data boundary: `fence(label, content)` wraps tool-result/finding blocks in per-instance nonce marker pairs, `code_tail()` returns the fixed code-owned rule text, `check_leakage(prompt)` flags fences that were tampered with, `fence_result` is the short per-tool-result variant. Applied to `build_prompt_context` (digests/findings/facts), `judge_command`, the agent system and launch prompts, and every `agent_runner` tool result. Config: profile `boundary: {enabled}` (default True). |
| `evidence.py` | Verbatim citation verification: `verbatim_contains` (whitespace-normalised), `extract_quote`, and `CitationService.verify/replay/annotate` over the task traffic log. `FindingService.report` stores the extracted quote in the finding meta; `Retester._citation_verdict` returns `reproduced` with zero executions when the quote binds to fresh captured output, before any replay. Config: profile `evidence: {citation_enabled, citation_max_age_sec, replay_enabled}`. |
| `planner_bridge.py` | Single-planner-pipeline bridge: `modules.planner` technique candidates (ranked `PlanCandidate` steps) are converted into intent summaries and fed into the loop `Planner._candidates()`, deduped against existing intents. Config: profile `planner: {bridge_enabled}` (default True). |

## How it works

`modules.lazy_loop.Worker` inherits the worker mixins
(`class Worker(WorkerAgenticMixin, WorkerExecutionMixin, WorkerGatingMixin, WorkerMemoryMixin)`)
and `modules.lazy_loop.LazyLoopEngine` inherits `EngineProxyMixin`.
Method resolution keeps the public surface identical, so every caller that used
`worker._os_gate(...)`, `worker._run(...)`, `worker._agentic_try(...)` or
`engine.proxy_start(...)` keeps working without change. The mixins never import `lazy_loop` at module load time;
module-level helpers that still live in `lazy_loop` (`_store_path`, `_now`,
`AssetGate`, `FindingService`, `LlmPool`, `constraint_block`,
`build_prompt_context`, `task_llm_chain`, `plausible_command`,
`MAX_WORKER_STEPS`) are imported lazily inside the methods that need them,
matching the dominant import style of `lazy_loop.py` and keeping the dependency
acyclic. Names used only in type annotations are imported under
`if TYPE_CHECKING:` so they never execute at runtime.

Collaborators the mixins rely on are set by `Worker.__init__`
(`self.activity`, `self.store`, `self.task_id`, `self._fact_store`) and the two
helpers that remain on the coordinator (`self._target_for`,
`self._resolved_command`).

## Adding a mixin

1. Create `worker_<concern>.py` with a `Worker<Concern>Mixin` class holding the
   methods for one responsibility only.
2. Keep every cross-module dependency on `lazy_loop` as a lazy import inside the
   method; import stable providers (for example `modules.loop_guardrails`) at
   module level.
3. Re-export the class from `__init__.py` and add it to the `Worker` base list.
4. Delete the moved method bodies from `modules/lazy_loop.py`.
5. Run the loop test suite (`pytest tests/test_lazy_loop.py tests/test_asset_gate.py`
   and the scope/evidence suites) to confirm the public surface is unchanged.

## Adding a substrate module

The leases/tokens/boundary/evidence/planner_bridge files are not mixins but
standalone contracts the god class delegates to (composition over a growing
`lazy_loop.py`). Follow the same pattern: one file per contract, config read
from an orchestrator profile section (fallback < YAML profile < payload
`orchestrator.<section>`), SQLite persistence through `state_db` when the
concern needs transactional cross-process semantics, and pytest coverage in a
dedicated `tests/test_loop_<concern>.py`.
