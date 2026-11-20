# modules: lazy_loop

*Community 2 | 162 files | cohesion 0.52*

## Definition

This community groups 162 file(s) rooted at `tests` with dominant language py (cohesion 0.52). Central symbols: `ActivityLog`, `ActivityLogPort`, `AssetGate`, `AssetGraph`, `AssetNode`, `AttributionLedger`, `BlindspotFinding`, `BlindspotReview`. Core file: `modules/lazy_loop.py` (510 symbols). Documented purpose: Lazy autonomous loop commands (single orchestrator, lazy_* surface).  Every subsystem is invocable individually so the operator sees what it does, plus ``lazy_l.

## Files

### `tests` (79 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_loop_memory.py` | py | testing | 19 | yes |
| `tests/test_autonomous_ops.py` | py | testing | 15 | yes |
| `tests/test_chain_family.py` | py | testing | 8 | yes |

### `modules` (44 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/auto_loop_memory.py` | py | utility | 26 | yes |
| `modules/chain_family.py` | py | utility | 13 | yes |
| `modules/custom_tools.py` | py | utility | 12 | yes |

### `modules/loop` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/loop/__init__.py` | py | utility | 0 | no |
| `modules/loop/boundary.py` | py | utility | 8 | yes |

### `skills/mcp_tools` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/auto_loop.py` | py | utility | 3 | yes |
| `skills/mcp_tools/lazy_board.py` | py | utility | 1 | yes |

### `modules/mediation` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/mediation/__init__.py` | py | utility | 0 | yes |
| `modules/mediation/chain_mediator.py` | py | utility | 8 | yes |

### `cli` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/headless.py` | py | utility | 6 | yes |
| `cli/lazy_monitor.py` | py | utility | 46 | yes |

### `modules/tools` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/tools/__init__.py` | py | utility | 0 | yes |
| `modules/tools/loop_smoke.py` | py | utility | 10 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/atomic_store.py` | py | data_access | 6 | yes |
| `core/terminal_guard.py` | py | utility | 8 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/lazyops.py` | py | utility | 77 | yes |

### `modules/sinks` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/chain_feed.py` | py | utility | 1 | yes |

*... and 142 more files in this community.*


## Key Symbols

- `_engine` (function, `cli/commands/lazyops.py:35`) `def _engine()` - Import LazyEngine lazily so the shell boots without it.
- `LazyCommandSet` (class, `cli/commands/lazyops.py:42`) `class LazyCommandSet(LazyOwnCommandSet)` - Lazy double-graph autonomous loop: planner, workers, guard, retest.
- `_task_id` (method, `cli/commands/lazyops.py:48`) `def _task_id(self, args)` - Resolve --task flag or fall back to the newest task.
- `_require_task` (method, `cli/commands/lazyops.py:61`) `def _require_task(self, args)` - Return task id or print usage error and empty string.
- `_free_text` (method, `cli/commands/lazyops.py:69`) `def _free_text(args)` - Return positional words with flag values stripped.
- `do_lazy_dispatch` (method, `cli/commands/lazyops.py:95`) `def do_lazy_dispatch(self, line)` - Dispatch one detached task to an external agent: opencode\|hermes [--in DIR] [--resume S] [--max-turn
- `do_lazy_task` (method, `cli/commands/lazyops.py:154`) `def do_lazy_task(self, line)` - Create/list/show/pause/resume/delete/spawn/queue/limit/drain tasks. Usage: lazy_task create <goal> \|
- `do_lazy_graph` (method, `cli/commands/lazyops.py:276`) `def do_lazy_graph(self, line)` - Show planner-facing graph overview. Usage: lazy_graph [--task T]
- `do_lazy_context` (method, `cli/commands/lazyops.py:305`) `def do_lazy_context(self, line)` - Render the bounded prompt context the planner/worker LLMs receive. Usage: lazy_context [--task T] [-
- `do_lazy_skill` (method, `cli/commands/lazyops.py:326`) `def do_lazy_skill(self, line)` - Skills: list\|show <name>\|preview\|inject <name...>\|clear\|auto on\|off\|mirror [name]\|register-hermes. U
- `do_lazy_workspace` (method, `cli/commands/lazyops.py:410`) `def do_lazy_workspace(self, line)` - Confined workspace files: list [path]\|read <path>\|write <path> <text>\|mkdir <path>\|rm <path>\|path. U
- `do_lazy_selfupdate` (method, `cli/commands/lazyops.py:463`) `def do_lazy_selfupdate(self, line)` - Self-update: check [--branch B]\|apply [--yes] [--branch B]. Usage: lazy_selfupdate ...
- `do_lazy_planner` (method, `cli/commands/lazyops.py:491`) `def do_lazy_planner(self, line)` - Run one planner wakeup (emits 0..N intents). Usage: lazy_planner [--task T]
- `do_lazy_frontier` (method, `cli/commands/lazyops.py:510`) `def do_lazy_frontier(self, line)` - Show pending intent queue. Usage: lazy_frontier [--task T]
- `do_lazy_worker` (method, `cli/commands/lazyops.py:522`) `def do_lazy_worker(self, line)` - Claim ONE intent and execute it with real tools. Usage: lazy_worker [--task T] [--intent N]
- `do_lazy_trace` (method, `cli/commands/lazyops.py:562`) `def do_lazy_trace(self, line)` - Worker trace exchange. Usage: lazy_trace list\|search <q>\|search-all <q>\|get <intent>\|steps <intent>
- `do_lazy_broadcast` (method, `cli/commands/lazyops.py:615`) `def do_lazy_broadcast(self, line)` - Exploration timeline. Usage: lazy_broadcast [--task T] [--kind K] [--q Q] [--asc] [--page N] [--limi
- `do_lazy_commander` (method, `cli/commands/lazyops.py:650`) `def do_lazy_commander(self, line)` - Allocate work slices across the task fleet. Usage: lazy_commander [--minutes N] [--slices N] [--work
- `_complete` (function, `cli/commands/lazyops.py:670`) `def _complete(prompt, max_tokens)`
- `do_lazy_deviations` (method, `cli/commands/lazyops.py:698`) `def do_lazy_deviations(self, line)` - List planned-versus-actual deviations. Usage: lazy_deviations [scope] [--limit N] [--md]
- `do_lazy_blindspot` (method, `cli/commands/lazyops.py:736`) `def do_lazy_blindspot(self, line)` - Review graph blindspots into hints. Usage: lazy_blindspot [--task T]
- `do_lazy_hint` (method, `cli/commands/lazyops.py:762`) `def do_lazy_hint(self, line)` - Inject steering hint. Usage: lazy_hint <text> [--task T]
- `do_lazy_intent` (method, `cli/commands/lazyops.py:774`) `def do_lazy_intent(self, line)` - Inject high-priority intent. Usage: lazy_intent <summary> [--task T] [--priority N]
- `do_lazy_intent_delete` (method, `cli/commands/lazyops.py:799`) `def do_lazy_intent_delete(self, line)` - Delete an intent. Usage: lazy_intent_delete <id> --reason <text> [--hard] [--task T] [--yes]
- `do_lazy_goal` (method, `cli/commands/lazyops.py:842`) `def do_lazy_goal(self, line)` - Goals: list\|set <t1;t2>\|edit <id> <text>\|delete <id>\|prove <goal> <evidence> <reason>\|met <reason>.
- `do_lazy_constraint` (method, `cli/commands/lazyops.py:881`) `def do_lazy_constraint(self, line)` - Constraints: add <allow\|deny> <text> \| list. Usage: lazy_constraint ... [--task T]
- `do_lazy_scope` (method, `cli/commands/lazyops.py:899`) `def do_lazy_scope(self, line)` - Scope: add <kind> <value> [reason] \| list. Usage: lazy_scope ... [--task T]
- `do_lazy_todo` (method, `cli/commands/lazyops.py:917`) `def do_lazy_todo(self, line)` - Serial chain todos: add <text> \| done <id> \| list. Usage: lazy_todo ... [--task T]
- `do_lazy_asset` (method, `cli/commands/lazyops.py:939`) `def do_lazy_asset(self, line)` - Assets: add <kind> <value> \| list [kind] \| scoped [--kind K] \| coverage \| untested. Usage: lazy_asse
- `do_lazy_enrich` (method, `cli/commands/lazyops.py:980`) `def do_lazy_enrich(self, line)` - Enrich asset with DNS/HTTP. Usage: lazy_enrich <host-or-url>

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 686
- Cross-boundary resolved imports (EXTRACTED): 639

## Connections

- [EXTRACTED] depends_on community 5 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.
- [EXTRACTED] depends_on community 11 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/sidequestion.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `utils.py` -> `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `utils.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/loop/target_os.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`

## Open Questions

- Why do 5 file(s) lack file-level docs (e.g. `modules/loop/__init__.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` be broken with an interface?
- What would break if the most connected file in modules: lazy_loop changed?
- Should modules: lazy_loop be split, given cohesion 0.52?

## Sources

- `cli/commands/lazyops.py`
- `cli/headless.py`
- `cli/lazy_monitor.py`
- `cli/session_brief.py`
- `core/atomic_store.py`
- `core/terminal_guard.py`
- `modules/auto_loop_memory.py`
- `modules/chain_family.py`
- `modules/custom_tools.py`
- `modules/digest.py`
- `modules/evidence_store.py`
- `modules/fact_gated_todolist.py`
- `modules/finding_enrich.py`
- `modules/guard_rules.py`
- `modules/jsonl_tail.py`
- `modules/lazy_blindspot.py`
- `modules/lazy_cli_bridge.py`
- `modules/lazy_commander.py`
- `modules/lazy_drafts.py`
- `modules/lazy_engine.py`
- *... and 142 more*
