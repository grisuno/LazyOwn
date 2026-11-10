# static/js

*Community 9 | 49 files | cohesion 0.47*

## Definition

This community groups 49 file(s) rooted at `static/js` with dominant language py (cohesion 0.47). Central symbols: `A`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`, `AddonYamlRenderer`, `As`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

### `static/js` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |

### `tests` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_crypto.py` | py | testing | 22 | yes |
| `tests/test_cli_assign.py` | py | testing | 44 | yes |

### `cli` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/session_resumer.py` | py | utility | 6 | yes |

### `core` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/param_registry.py` | py | utility | 17 | yes |
| `core/payload_schema.py` | py | utility | 30 | yes |

### `poc_tui` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | utility | 0 | yes |
| `poc_tui/app.py` | py | utility | 47 | yes |

### `skills/mcp_tools` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/create_param.py` | py | utility | 1 | yes |
| `skills/mcp_tools/delete_param.py` | py | utility | 1 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/exp.c` | c | utility | 58 | yes |
| `modules/lazy_verify.py` | py | utility | 8 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/params_ops.py` | py | utility | 2 | yes |

### `lazyc2` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 39 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `gyms/docker/php2shell/src` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `gyms/docker/php2shell/src/info.php` | php | utility | 0 | no |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `static/hexabot` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/hexabot/hexabot-spinner.js` | js | utility | 24 | no |

*... and 29 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:42`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `ParamCommandSet` (class, `cli/commands/params_ops.py:31`) `class ParamCommandSet(LazyOwnCommandSet)` - Create, inspect and delete the shared parameters.
- `do_param` (method, `cli/commands/params_ops.py:38`) `def do_param(self, line)` - Manage the shared parameter catalog used by addons and aliases.
- `_strip_shell_quotes` (function, `cli/commands/session_ops.py:72`) `def _strip_shell_quotes(value)` - Drop one pair of matching wrapping quotes kept by ``posix=False`` parsing.
- `SessionOpsCommandSet` (class, `cli/commands/session_ops.py:86`) `class SessionOpsCommandSet(LazyOwnCommandSet)` - Session and campaign operations.
- `do_note` (method, `cli/commands/session_ops.py:93`) `def do_note(self, line)` - Capture a quick operator note attached to the current target and phase.
- `do_l00t` (method, `cli/commands/session_ops.py:118`) `def do_l00t(self, line)` - Unified loot: show, search, reuse, graph, and mark credentials.
- `do_loot` (method, `cli/commands/session_ops.py:167`) `def do_loot(self, line)` - Alias for ``l00t`` — unified loot (show/search/reuse/graph/mark).
- `do_pivot` (method, `cli/commands/session_ops.py:175`) `def do_pivot(self, line)` - Record a newly discovered pivot target or show the pivot chain.
- `do_tasks` (method, `cli/commands/session_ops.py:200`) `def do_tasks(self, line)` - View and manage the task queue from sessions/tasks.json.
- `do_scans` (method, `cli/commands/session_ops.py:233`) `def do_scans(self, line)` - List nmap scan files in sessions/ with age, size, and open ports.
- `do_sitrep` (method, `cli/commands/session_ops.py:250`) `def do_sitrep(self, line)` - Print a unified operational situation report.
- `do_assign` (method, `cli/commands/session_ops.py:267`) `def do_assign(self, line)` - assign a parameter value, persist to payload.json and refresh aliases.
- `do_tenant` (method, `cli/commands/session_ops.py:332`) `def do_tenant(self, line)` - Manage multi-tenancy: list, switch, or create engagement tenants.
- `do_scope` (method, `cli/commands/session_ops.py:405`) `def do_scope(self, line)` - Manage the authorized engagement scope and the scope-guard posture.
- `do_show` (method, `cli/commands/session_ops.py:471`) `def do_show(self, line)` - Show params, modules, payloads, or active module options.
- `do_list` (method, `cli/commands/session_ops.py:547`) `def do_list(self, line)` - Lists all available scripts in the modules directory.
- `do_run` (method, `cli/commands/session_ops.py:576`) `def do_run(self, line)` - Runs a specific LazyOwn script or active module.
- `do_payload` (method, `cli/commands/session_ops.py:615`) `def do_payload(self, line)` - Load parameters from a specified payload JSON file.
- `do_next` (method, `cli/commands/session_ops.py:666`) `def do_next(self, line)` - Show next-step recommendations or execute the active autosuggest.
- `do_frontier` (method, `cli/commands/session_ops.py:710`) `def do_frontier(self, line)` - Preview the planner intents the autonomous loops would run next.
- `do_traces` (method, `cli/commands/session_ops.py:754`) `def do_traces(self, line)` - Show recent autonomous step traces with evidence and traffic ids.
- `do_chainmode` (method, `cli/commands/session_ops.py:835`) `def do_chainmode(self, line)` - Toggle interactive kill-chain chaining after every command.
- `do_engage` (method, `cli/commands/session_ops.py:886`) `def do_engage(self, line)` - Drive a single target through the full kill-chain in one command.
- `_flag_value` (function, `cli/commands/session_ops.py:950`) `def _flag_value(flag_name)`
- `do_pipeline` (method, `cli/commands/session_ops.py:1013`) `def do_pipeline(self, line)` - Declarative composition layer: run a YAML pipeline of LazyOwn commands.
- `_flag_value` (function, `cli/commands/session_ops.py:1062`) `def _flag_value(flag_name)`
- `do_lazyscript` (method, `cli/commands/session_ops.py:1104`) `def do_lazyscript(self, line)` - Executes commands defined in a lazyscript file.
- `do_hunt` (method, `cli/commands/session_ops.py:1136`) `def do_hunt(self, line)` - Run an autonomous exploitation chain against a target.
- `do_resume` (method, `cli/commands/session_ops.py:1227`) `def do_resume(self, line)` - Browse previous sessions and load a target from a past engagement.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 310
- Cross-boundary resolved imports (EXTRACTED): 145

## Connections

- [EXTRACTED] depends_on community 6 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/param_registry.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/process.py` via `subprocess` (5 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `modules/opsec_scorer.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`

## Open Questions

- Why do 10 file(s) lack file-level docs (e.g. `gyms/docker/php2shell/src/info.php`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` be broken with an interface?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.47?

## Sources

- `cli/assign.py`
- `cli/commands/params_ops.py`
- `cli/commands/session_ops.py`
- `cli/session_resumer.py`
- `cli/show.py`
- `cli/style.py`
- `core/param_registry.py`
- `core/payload_schema.py`
- `core/process.py`
- `core/prompt.py`
- `gyms/docker/php2shell/src/info.php`
- `key.py`
- `lazyc2/addon_creator.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/exp.c`
- `modules/lazy_verify.py`
- `modules/search.py`
- `poc_tui/__main__.py`
- `poc_tui/app.py`
- *... and 29 more*
