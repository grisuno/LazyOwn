# Subsystem: modules (page 7 of 15)
Previous: [KB_modules_p6.md](KB_modules_p6.md)

## modules/lazy_engine.py
- Doc: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- Layer: utility
- Language: py
- Symbols:
  - `LazyEngine` (class, line 55) `class LazyEngine(LazyLoopEngine)`
- Depends on: `modules/lazy_loop.py`
- Imported by: `cli/commands/lazyloop.py`, `cli/commands/lazyops.py`, `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `modules/lazy_loop.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/tools/loop_smoke.py`, `modules/tools/monitor_smoke.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_worker_safety.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_broadcast.py`, `tests/test_loop_cold_overview.py`, `tests/test_loop_force_graph.py`, `tests/test_loop_guard_audit.py`, `tests/test_loop_intent_delete.py`, `tests/test_loop_llm_resilience.py`, `tests/test_loop_scope_traffic_evidence.py`, `tests/test_loop_spawn_side.py`, `tests/test_loop_supervision.py`, `tests/test_loop_worker_traces.py`

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
