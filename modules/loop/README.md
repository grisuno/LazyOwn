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
