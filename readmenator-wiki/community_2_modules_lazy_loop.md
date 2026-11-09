# modules: lazy_loop

*Community 2 | 132 files | cohesion 0.51*

## Definition

This community groups 132 file(s) rooted at `tests` with dominant language py (cohesion 0.51). Central symbols: `ActivityLog`, `AdLabCaptureSpec`, `AdLabCatalogueSpec`, `AdLabGymDefinitionsSpec`, `AdLabRuntimeSpec`, `AssetGate`, `AssetGraph`, `AssetNode`. Core file: `modules/lazy_loop.py` (457 symbols). Documented purpose: Lazy queue and misc command set.  Engine-backed operator surface with ``lazy_`` names. Every command here reads or writes the single ``modules.lazy_engine`` sto.

## Files

### `tests` (72 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/conftest.py` | py | testing | 11 | yes |
| `tests/test_ad_lab_gym.py` | py | testing | 25 | yes |
| `tests/test_asset_gate.py` | py | testing | 16 | yes |

### `modules` (42 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/auto_loop_memory.py` | py | utility | 26 | yes |
| `modules/auto_registry.py` | py | utility | 45 | yes |

### `modules/loop` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/loop/__init__.py` | py | utility | 0 | no |
| `modules/loop/worker_agentic.py` | py | utility | 18 | no |
| `modules/loop/worker_execution.py` | py | utility | 12 | no |

### `cli/commands` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/exploitdb.py` | py | utility | 10 | no |
| `cli/commands/lazyloop.py` | py | utility | 13 | yes |

### `modules/tools` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/tools/__init__.py` | py | utility | 0 | yes |
| `modules/tools/loop_smoke.py` | py | utility | 10 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/lazy_monitor.py` | py | utility | 46 | yes |
| `cli/session_brief.py` | py | utility | 10 | yes |

### `modules/sinks` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/chain_feed.py` | py | utility | 1 | yes |
| `modules/sinks/findings.py` | py | utility | 5 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/terminal_guard.py` | py | utility | 8 | yes |

### `lazyc2/blueprints` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/orchestrator.py` | py | presentation | 17 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 6 | yes |

*... and 112 more files in this community.*


## Key Symbols

- `ExploitdbCommands` (class, `cli/commands/exploitdb.py:11`) `class ExploitdbCommands`
- `do_exploitdb_sync` (method, `cli/commands/exploitdb.py:19`) `def do_exploitdb_sync(self, args)`
- `do_exploitdb_scan` (method, `cli/commands/exploitdb.py:33`) `def do_exploitdb_scan(self, args)`
- `do_exploitdb_gen` (method, `cli/commands/exploitdb.py:45`) `def do_exploitdb_gen(self, args)`
- `do_exploitdb_cscan` (method, `cli/commands/exploitdb.py:76`) `def do_exploitdb_cscan(self, args)`
- `do_exploitdb_ccompile` (method, `cli/commands/exploitdb.py:87`) `def do_exploitdb_ccompile(self, args)`
- `ExploitdbCCommands` (class, `cli/commands/exploitdb.py:94`) `class ExploitdbCCommands`
- `do_exploitdb_cscan` (method, `cli/commands/exploitdb.py:99`) `def do_exploitdb_cscan(self, args)`
- `do_exploitdb_ccompile` (method, `cli/commands/exploitdb.py:110`) `def do_exploitdb_ccompile(self, args)`
- `do_exploitdb_run` (method, `cli/commands/exploitdb.py:124`) `def do_exploitdb_run(self, args)`
- `_engine` (function, `cli/commands/lazyloop.py:22`) `def _engine()` - Return a fresh engine handle over the persisted lazy store.
- `LazyQueueCommandSet` (class, `cli/commands/lazyloop.py:29`) `class LazyQueueCommandSet(LazyOwnCommandSet)` - Lazy queue controls backed by the loop engine.
- `do_lazy_sync` (method, `cli/commands/lazyloop.py:36`) `def do_lazy_sync(self, line)` - Run bidirectional LAZY sync into world model and objectives.
- `do_lazy_intents` (method, `cli/commands/lazyloop.py:51`) `def do_lazy_intents(self, line)` - List engine intents for a task, optionally filtered by state.
- `do_lazy_delete` (method, `cli/commands/lazyloop.py:71`) `def do_lazy_delete(self, line)` - Delete an engine intent; soft keeps outputs, hard cascades.
- `do_lazy_findings` (method, `cli/commands/lazyloop.py:110`) `def do_lazy_findings(self, line)` - List engine findings for a task, optionally filtered by status.
- `do_lazy_handoff` (method, `cli/commands/lazyloop.py:180`) `def do_lazy_handoff(self, line)` - Print the operator handoff for a finished loop task.
- `do_lazy_verdict` (method, `cli/commands/lazyloop.py:190`) `def do_lazy_verdict(self, line)` - Record a manual retest verdict on an engine finding.
- `do_lazy_mention` (method, `cli/commands/lazyloop.py:213`) `def do_lazy_mention(self, line)` - Search @ mention candidates with scroll pagination.
- `do_lazy_approve` (method, `cli/commands/lazyloop.py:248`) `def do_lazy_approve(self, line)` - List engine guard reviews filtered by decision and source.
- `do_lazy_fleet` (method, `cli/commands/lazyloop.py:270`) `def do_lazy_fleet(self, line)` - Cross-task fleet: list \| graph <task> \| findings <task> \| traces <task> [query] \| node <task> <id> \|
- `do_lazy_orchestrator` (method, `cli/commands/lazyloop.py:335`) `def do_lazy_orchestrator(self, line)` - Admin console for the loop (Textual TUI).
- `do_lazy_view` (method, `cli/commands/lazyloop.py:364`) `def do_lazy_view(self, line)` - Attach the live worker monitor to a task (or the newest task).
- `_engine` (function, `cli/commands/lazyops.py:28`) `def _engine()` - Import LazyEngine lazily so the shell boots without it.
- `LazyCommandSet` (class, `cli/commands/lazyops.py:35`) `class LazyCommandSet(LazyOwnCommandSet)` - Lazy double-graph autonomous loop: planner, workers, guard, retest.
- `_task_id` (method, `cli/commands/lazyops.py:41`) `def _task_id(self, args)` - Resolve --task flag or fall back to the newest task.
- `_require_task` (method, `cli/commands/lazyops.py:54`) `def _require_task(self, args)` - Return task id or print usage error and empty string.
- `_free_text` (method, `cli/commands/lazyops.py:62`) `def _free_text(args)` - Return positional words with flag values stripped.
- `do_lazy_dispatch` (method, `cli/commands/lazyops.py:88`) `def do_lazy_dispatch(self, line)` - Dispatch one detached task to an external agent: opencode\|hermes [--in DIR] [--resume S] [--max-turn
- `do_lazy_task` (method, `cli/commands/lazyops.py:147`) `def do_lazy_task(self, line)` - Create/list/show/pause/resume/delete/spawn/queue/limit/drain tasks. Usage: lazy_task create <goal> \|

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 783
- Cross-boundary resolved imports (EXTRACTED): 551

## Connections

- [EXTRACTED] depends_on community 6 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/__init__.py.
- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_pool.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/mcp_agent_bridge.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/payload_schema.py`

## Open Questions

- Why do 7 file(s) lack file-level docs (e.g. `cli/commands/exploitdb.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- What would break if the most connected file in modules: lazy_loop changed?
- Should modules: lazy_loop be split, given cohesion 0.51?

## Sources

- `cli/commands/exploitdb.py`
- `cli/commands/lazyloop.py`
- `cli/commands/lazyops.py`
- `cli/lazy_monitor.py`
- `cli/session_brief.py`
- `core/terminal_guard.py`
- `lazyc2/blueprints/orchestrator.py`
- `modules/__init__.py`
- `modules/auto_loop_memory.py`
- `modules/auto_registry.py`
- `modules/custom_tools.py`
- `modules/digest.py`
- `modules/gym_winbox_runner.py`
- `modules/harness.py`
- `modules/jsonl_tail.py`
- `modules/lazy_agent.py`
- `modules/lazy_bridge.py`
- `modules/lazy_cli_bridge.py`
- `modules/lazy_drafts.py`
- `modules/lazy_engine.py`
- *... and 112 more*
