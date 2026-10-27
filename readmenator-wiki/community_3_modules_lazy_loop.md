# modules: lazy_loop

*Community 3 | 108 files | cohesion 0.58*

## Definition

This community groups 108 file(s) rooted at `tests` with dominant language py (cohesion 0.58). Central symbols: `ActivityLog`, `ActivityLogPort`, `AssetGate`, `AssetGraph`, `AssetNode`, `AutoVerb`, `Budget`, `BuildAgentProfiles`. Core file: `modules/lazy_loop.py` (466 symbols). Documented purpose: Lazy queue and misc command set.  Engine-backed operator surface with ``lazy_`` names. Every command here reads or writes the single ``modules.lazy_engine`` sto.

## Files

### `tests` (52 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/conftest.py` | py | testing | 11 | yes |
| `tests/test_asset_gate.py` | py | testing | 16 | yes |
| `tests/test_auto_registry.py` | py | testing | 20 | yes |

### `modules` (35 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/auto_registry.py` | py | utility | 43 | yes |
| `modules/custom_tools.py` | py | utility | 11 | yes |

### `modules/mediation` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/mediation/__init__.py` | py | utility | 0 | yes |
| `modules/mediation/chain_mediator.py` | py | utility | 8 | yes |
| `modules/mediation/contracts.py` | py | utility | 12 | yes |

### `cli` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/lazy_monitor.py` | py | utility | 46 | yes |
| `cli/lazy_orchestrator.py` | py | utility | 46 | yes |
| `cli/orchestrator_assets_tabs.py` | py | utility | 62 | yes |

### `modules/tools` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/tools/__init__.py` | py | utility | 0 | yes |
| `modules/tools/loop_smoke.py` | py | utility | 10 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/lazyloop.py` | py | utility | 12 | yes |
| `cli/commands/lazyops.py` | py | utility | 71 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/terminal_guard.py` | py | utility | 8 | yes |

### `lazyc2/blueprints` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/orchestrator.py` | py | presentation | 17 | yes |

### `modules/sinks` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/routing.py` | py | utility | 1 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 6 | yes |

*... and 88 more files in this community.*


## Key Symbols

- `_engine` (function, `cli/commands/lazyloop.py:22`) `def _engine()` - Return a fresh engine handle over the persisted lazy store.
- `LazyQueueCommandSet` (class, `cli/commands/lazyloop.py:29`) `class LazyQueueCommandSet(LazyOwnCommandSet)` - Lazy queue controls backed by the loop engine.
- `do_lazy_sync` (method, `cli/commands/lazyloop.py:36`) `def do_lazy_sync(self, line)` - Run bidirectional LAZY sync into world model and objectives.
- `do_lazy_intents` (method, `cli/commands/lazyloop.py:51`) `def do_lazy_intents(self, line)` - List engine intents for a task, optionally filtered by state.
- `do_lazy_delete` (method, `cli/commands/lazyloop.py:71`) `def do_lazy_delete(self, line)` - Delete an engine intent; soft keeps outputs, hard cascades.
- `do_lazy_findings` (method, `cli/commands/lazyloop.py:110`) `def do_lazy_findings(self, line)` - List engine findings for a task, optionally filtered by status.
- `do_lazy_verdict` (method, `cli/commands/lazyloop.py:132`) `def do_lazy_verdict(self, line)` - Record a manual retest verdict on an engine finding.
- `do_lazy_mention` (method, `cli/commands/lazyloop.py:155`) `def do_lazy_mention(self, line)` - Search @ mention candidates with scroll pagination.
- `do_lazy_approve` (method, `cli/commands/lazyloop.py:190`) `def do_lazy_approve(self, line)` - List engine guard reviews filtered by decision and source.
- `do_lazy_fleet` (method, `cli/commands/lazyloop.py:212`) `def do_lazy_fleet(self, line)` - Cross-task fleet: list \| graph <task> \| findings <task> \| traces <task> [query] \| node <task> <id> \|
- `do_lazy_orchestrator` (method, `cli/commands/lazyloop.py:277`) `def do_lazy_orchestrator(self, line)` - Admin console for the loop (Textual TUI).
- `do_lazy_view` (method, `cli/commands/lazyloop.py:306`) `def do_lazy_view(self, line)` - Attach the live worker monitor to a task (or the newest task).
- `_engine` (function, `cli/commands/lazyops.py:28`) `def _engine()` - Import LazyEngine lazily so the shell boots without it.
- `LazyCommandSet` (class, `cli/commands/lazyops.py:35`) `class LazyCommandSet(LazyOwnCommandSet)` - Lazy double-graph autonomous loop: planner, workers, guard, retest.
- `_task_id` (method, `cli/commands/lazyops.py:41`) `def _task_id(self, args)` - Resolve --task flag or fall back to the newest task.
- `_require_task` (method, `cli/commands/lazyops.py:54`) `def _require_task(self, args)` - Return task id or print usage error and empty string.
- `_free_text` (method, `cli/commands/lazyops.py:62`) `def _free_text(args)` - Return positional words with flag values stripped.
- `do_lazy_dispatch` (method, `cli/commands/lazyops.py:88`) `def do_lazy_dispatch(self, line)` - Dispatch one detached task to an external agent: opencode\|hermes [--in DIR] [--resume S] [--max-turn
- `do_lazy_task` (method, `cli/commands/lazyops.py:147`) `def do_lazy_task(self, line)` - Create/list/show/pause/resume/delete/spawn/queue/limit/drain tasks. Usage: lazy_task create <goal> \|
- `do_lazy_graph` (method, `cli/commands/lazyops.py:269`) `def do_lazy_graph(self, line)` - Show planner-facing graph overview. Usage: lazy_graph [--task T]
- `do_lazy_context` (method, `cli/commands/lazyops.py:298`) `def do_lazy_context(self, line)` - Render the bounded prompt context the planner/worker LLMs receive. Usage: lazy_context [--task T] [-
- `do_lazy_skill` (method, `cli/commands/lazyops.py:319`) `def do_lazy_skill(self, line)` - Skills: list\|show <name>\|preview\|inject <name...>\|clear\|auto on\|off\|mirror [name]\|register-hermes. U
- `do_lazy_workspace` (method, `cli/commands/lazyops.py:403`) `def do_lazy_workspace(self, line)` - Confined workspace files: list [path]\|read <path>\|write <path> <text>\|mkdir <path>\|rm <path>\|path. U
- `do_lazy_selfupdate` (method, `cli/commands/lazyops.py:456`) `def do_lazy_selfupdate(self, line)` - Self-update: check [--branch B]\|apply [--yes] [--branch B]. Usage: lazy_selfupdate ...
- `do_lazy_planner` (method, `cli/commands/lazyops.py:484`) `def do_lazy_planner(self, line)` - Run one planner wakeup (emits 0..N intents). Usage: lazy_planner [--task T]
- `do_lazy_frontier` (method, `cli/commands/lazyops.py:503`) `def do_lazy_frontier(self, line)` - Show pending intent queue. Usage: lazy_frontier [--task T]
- `do_lazy_worker` (method, `cli/commands/lazyops.py:515`) `def do_lazy_worker(self, line)` - Claim ONE intent and execute it with real tools. Usage: lazy_worker [--task T] [--intent N]
- `do_lazy_trace` (method, `cli/commands/lazyops.py:555`) `def do_lazy_trace(self, line)` - Worker trace exchange. Usage: lazy_trace list\|search <q>\|search-all <q>\|get <intent>\|steps <intent>
- `do_lazy_broadcast` (method, `cli/commands/lazyops.py:608`) `def do_lazy_broadcast(self, line)` - Exploration timeline. Usage: lazy_broadcast [--task T] [--kind K] [--q Q] [--asc] [--page N] [--limi
- `do_lazy_hint` (method, `cli/commands/lazyops.py:643`) `def do_lazy_hint(self, line)` - Inject steering hint. Usage: lazy_hint <text> [--task T]

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 786
- Cross-boundary resolved imports (EXTRACTED): 387

## Connections

- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.
- [EXTRACTED] depends_on community 9 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_pool.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/harness.py` via `subprocess` (5 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/mcp_agent_bridge.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `modules/__init__.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/reactive_engine.py` be broken with an interface?
- What would break if the most connected file in modules: lazy_loop changed?
- Should modules: lazy_loop be split, given cohesion 0.58?

## Sources

- `cli/commands/lazyloop.py`
- `cli/commands/lazyops.py`
- `cli/lazy_monitor.py`
- `cli/lazy_orchestrator.py`
- `cli/orchestrator_assets_tabs.py`
- `cli/session_brief.py`
- `cli/tui_forms.py`
- `core/terminal_guard.py`
- `lazyc2/blueprints/orchestrator.py`
- `modules/__init__.py`
- `modules/auto_registry.py`
- `modules/custom_tools.py`
- `modules/harness.py`
- `modules/jsonl_tail.py`
- `modules/lazy_agent.py`
- `modules/lazy_bridge.py`
- `modules/lazy_cli_bridge.py`
- `modules/lazy_engine.py`
- `modules/lazy_installer.py`
- `modules/lazy_intel.py`
- *... and 88 more*
