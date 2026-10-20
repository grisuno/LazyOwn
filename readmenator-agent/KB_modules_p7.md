# Subsystem: modules (page 7 of 15)
Previous: [KB_modules_p6.md](KB_modules_p6.md)

## modules/killchain.py
- Doc: Unified kill-chain — single source of truth consumed by all surfaces.
- Layer: utility
- Language: py
- Symbols:
  - `KillChainConfig` (class, line 38) `class KillChainConfig`
  - `PhaseStatus` (class, line 136) `class PhaseStatus`
  - `KillChain` (class, line 145) `class KillChain`
  - `get_killchain` (function, line 453) `def get_killchain()`
  - `world_model_path` (method, line 116) `def world_model_path(self)`
  - `phase_index` (method, line 120) `def phase_index(self, phase)`
  - `is_valid_phase` (method, line 127) `def is_valid_phase(self, phase)`
  - `config` (method, line 154) `def config()`
  - `phases` (method, line 159) `def phases()`
  - `phase_labels` (method, line 164) `def phase_labels()`
  - `phase_colors` (method, line 169) `def phase_colors()`
  - `phase_rich_colors` (method, line 174) `def phase_rich_colors()`
  - `engagement_phase_to_cli` (method, line 179) `def engagement_phase_to_cli(engagement_value)`
  - `cli_phase_to_host_state` (method, line 191) `def cli_phase_to_host_state(phase)`
  - `current_phase` (method, line 204) `def current_phase(world_model_path)`
  - `advance_phase` (method, line 251) `def advance_phase(new_phase, world_model_path, host)`
  - `get_progress` (method, line 328) `def get_progress(world_model_path)`
  - `compact_progress` (method, line 377) `def compact_progress(current_phase, phases_entered)`
  - `phases_for_display` (method, line 397) `def phases_for_display()`
  - `phase_index` (method, line 408) `def phase_index(phase)`
  - `snapshot` (method, line 413) `def snapshot(world_model_path)`
- Depends on: `core/logging.py`, `modules/world_model.py`
- Imported by: `cli/commands/ai.py`, `cli/dashboard_tui.py`, `cli/killchain.py`, `cli/ops_commands.py`, `cli/recon_plan.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `lazygui/panels/killchain_panel.py`, `modules/kill_chain_viz.py`, `modules/lazy_cli_bridge.py`, `modules/lazyown_bridge.py`, `modules/opsec_scorer.py`, `modules/sinks/killchain.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/hermes-lazyown/constants.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified_v2.py`

## modules/kivi.py
- Layer: utility
- Language: py
- Symbols:
  - `ReverseShellApp` (class, line 11) `class ReverseShellApp(App)`
  - `build` (method, line 12) `def build(self)`
  - `connect_to_server` (method, line 27) `def connect_to_server(self, instance)`

## modules/lazy_agent.py
- Doc: Agentic tool-calling bridge for the loop and the main agent.
- Layer: utility
- Language: py
- Symbols:
  - `model_timeout_sec` (function, line 41) `def model_timeout_sec()`
  - `tool_calling_enabled` (function, line 57) `def tool_calling_enabled()`
  - `max_iterations` (function, line 72) `def max_iterations()`
  - `resolve_agentic_model` (function, line 83) `def resolve_agentic_model(exclude)`
  - `_enable_streaming` (function, line 123) `def _enable_streaming(runner, on_event)`
  - `ObservableAgentRunner` (class, line 145) `class ObservableAgentRunner(AgentRunner)`
  - `_json_default` (function, line 221) `def _json_default(value)`
  - `_deep_clean` (function, line 237) `def _deep_clean(value, _depth)`
  - `_json_safe` (function, line 253) `def _json_safe(messages)`
  - `ConversationStore` (class, line 261) `class ConversationStore`
  - `register_tools` (function, line 322) `def register_tools(runner, specs)`
  - `run_worker_session` (function, line 335) `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)`
  - `run_main_session` (function, line 374) `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)`
  - `run_external_opencode` (function, line 396) `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)`
  - `run_external_hermes` (function, line 472) `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)`
  - `_session_from_line` (function, line 556) `def _session_from_line(line)`
  - `_process_watchdog` (function, line 578) `def _process_watchdog(timeout_sec, process)`
  - `__init__` (method, line 148) `def __init__(self, model, system_prompt, max_iterations, on_event)`
  - `_process_tool_call` (method, line 159) `def _process_tool_call(self, tool_call)`
  - `run` (method, line 168) `def run(self, user_input)`
  - `_call_model` (method, line 174) `def _call_model(self)`
  - `__init__` (method, line 264) `def __init__(self, task_id)`
  - `_load` (method, line 269) `def _load(self)`
  - `intent_messages` (method, line 273) `def intent_messages(self, intent_id)`
  - `save_intent` (method, line 278) `def save_intent(self, intent_id, messages)`
  - `session` (method, line 287) `def session(self, session_id)`
  - `sessions` (method, line 291) `def sessions(self)`
  - `save_session` (method, line 305) `def save_session(self, session_id, messages, title)`
  - `reset_intents` (method, line 315) `def reset_intents(self)`
  - `_kill` (function, line 583) `def _kill()`
  - `_invoke` (function, line 190) `def _invoke()`
  - `_tick` (function, line 196) `def _tick()`
- Depends on: `core/config.py`, `modules/__init__.py`, `modules/agent_runner.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop_ai_bridge.py`
- Imported by: `cli/commands/lazyops.py`, `tests/conftest.py`, `tests/test_lazy_agent.py`

## modules/lazy_bridge.py
- Doc: Bidirectional LAZY <-> LazyOwn bridge.
- Layer: utility
- Language: py
- Symbols:
  - `_data_dir` (function, line 35) `def _data_dir()`
  - `_read_json` (function, line 47) `def _read_json(path, default)`
  - `_read_jsonl` (function, line 64) `def _read_jsonl(path)`
  - `lazy_tasks` (function, line 88) `def lazy_tasks()`
  - `lazy_assets` (function, line 99) `def lazy_assets()`
  - `lazy_graph` (function, line 110) `def lazy_graph(task_id)`
  - `lazy_activity` (function, line 123) `def lazy_activity(task_id)`
  - `lazy_traffic` (function, line 135) `def lazy_traffic(task_id)`
  - `lazy_guard_audit` (function, line 147) `def lazy_guard_audit(task_id)`
  - `bridge_status` (function, line 159) `def bridge_status()`
  - `_extract_hosts_from_graph` (function, line 180) `def _extract_hosts_from_graph(graph)`
  - `pull_to_world_model` (function, line 206) `def pull_to_world_model()`
  - `pull_to_objectives` (function, line 251) `def pull_to_objectives()`
  - `pull_findings_to_lifecycle` (function, line 286) `def pull_findings_to_lifecycle()`
  - `_read_new_traffic` (function, line 314) `def _read_new_traffic(path, offset)`
  - `_notify` (function, line 351) `def _notify(progress, text)`
  - `pull_traffic_to_recorder` (function, line 361) `def pull_traffic_to_recorder(progress)`
  - `push_objective_to_lazy` (function, line 429) `def push_objective_to_lazy(goal, scope)`
  - `push_tasks_to_c2` (function, line 454) `def push_tasks_to_c2(only)`
  - `sync_all` (function, line 519) `def sync_all(progress)`
  - `_record_sync` (function, line 545) `def _record_sync(action, summary)`
- Depends on: `modules/finding_lifecycle.py`, `modules/traffic_recorder.py`, `modules/world_model.py`
- Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_lazy_loop.py`

## modules/lazy_cli_bridge.py
- Doc: Full CLI catalog for the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `_source_files` (function, line 74) `def _source_files()`
  - `_source_mtimes` (function, line 82) `def _source_mtimes()`
  - `_discover` (function, line 93) `def _discover()`
  - `cli_verbs` (function, line 106) `def cli_verbs()`
  - `is_cli_verb` (function, line 125) `def is_cli_verb(name)`
  - `phase_for` (function, line 131) `def phase_for(verb)`
  - `risk_for` (function, line 140) `def risk_for(verb)`
  - `needs_target_for` (function, line 150) `def needs_target_for(verb)`
  - `build_cli_command` (function, line 158) `def build_cli_command(verb, target)`
  - `search_cli_verbs` (function, line 185) `def search_cli_verbs(query, phase, limit)`
  - `cli_catalog_for_phase` (function, line 211) `def cli_catalog_for_phase(phase, limit)`
  - `catalog_cli_for_phase` (function, line 219) `def catalog_cli_for_phase(limit)`
  - `full_cli_enabled` (function, line 253) `def full_cli_enabled()`
  - `set_full_cli` (function, line 276) `def set_full_cli(enabled)`
- Depends on: `core/config.py`, `modules/killchain.py`, `modules/verb_catalog.py`
- Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/verb_catalog.py`, `tests/test_loop_cli_catalog.py`

## modules/lazy_engine.py
- Doc: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- Layer: utility
- Language: py
- Symbols:
  - `LazyEngine` (class, line 55) `class LazyEngine(LazyLoopEngine)`
- Depends on: `modules/lazy_loop.py`
- Imported by: `cli/commands/lazyloop.py`, `cli/commands/lazyops.py`, `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `cli/orchestrator_assets_tabs.py`, `cli/session_brief.py`, `modules/lazy_loop.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/tools/loop_smoke.py`, `modules/tools/monitor_smoke.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_worker_safety.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_broadcast.py`, `tests/test_loop_cold_overview.py`, `tests/test_loop_force_graph.py`, `tests/test_loop_guard_audit.py`, `tests/test_loop_intent_delete.py`, `tests/test_loop_llm_resilience.py`, `tests/test_loop_scope_traffic_evidence.py`, `tests/test_loop_spawn_side.py`, `tests/test_loop_supervision.py`, `tests/test_loop_worker_traces.py`, `tests/test_session_brief.py`

## modules/lazy_installer.py
- Doc: Capability installer for the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `installer_enabled` (function, line 41) `def installer_enabled()`
  - `set_installer_enabled` (function, line 58) `def set_installer_enabled(enabled)`
  - `install_command_for` (function, line 70) `def install_command_for(tool)`
  - `intent_for` (function, line 75) `def intent_for(tool)`
  - `tool_from_intent` (function, line 80) `def tool_from_intent(text)`
  - `steps_for_install` (function, line 88) `def steps_for_install(text)`
- Depends on: `core/config.py`, `modules/auto_registry.py`
- Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`

## modules/lazy_intel.py
- Doc: Intel feed from the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `_now` (function, line 30) `def _now()`
  - `_log_path` (function, line 35) `def _log_path()`
  - `_mask` (function, line 41) `def _mask(text)`
  - `_append` (function, line 70) `def _append(record)`
  - `infer_source` (function, line 79) `def infer_source(command, intent_text)`
  - `describe_command` (function, line 105) `def describe_command(command)`
  - `record_routing_decision` (function, line 120) `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)`
  - `record_routing_outcome` (function, line 160) `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)`
  - `read_decisions` (function, line 202) `def read_decisions(task_id, limit)`
  - `mask_configured` (function, line 228) `def mask_configured(text)`
  - `stack_signature` (function, line 254) `def stack_signature(assets)`
  - `_is_ip_literal` (function, line 274) `def _is_ip_literal(value)`
  - `fuse_routing_decisions` (function, line 285) `def fuse_routing_decisions(task_id)`
  - `export_spans` (function, line 324) `def export_spans(task_id, out)`
- Depends on: `core/config.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_loop.py`, `modules/world_model.py`, `utils.py`
- Imported by: `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/sinks/routing.py`, `tests/test_loop_supervision.py`


Next: [KB_modules_p8.md](KB_modules_p8.md)
