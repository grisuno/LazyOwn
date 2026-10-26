# API (page 21 of 24)
Previous: [API_p20.md](API_p20.md)

## skills/mcp_tool_generator.py
- `load_command_index` (function) `skills/mcp_tool_generator.py:29` `def load_command_index()`
- `extract_commands` (function) `skills/mcp_tool_generator.py:34` `def extract_commands(index)` -- Return {command_name: summary} for all unique non-duplicate commands.
- `extract_existing_handlers` (function) `skills/mcp_tool_generator.py:55` `def extract_existing_handlers()` -- Parse lazyown_mcp.py for all defined MCP tool names.
- `sanitize_description` (function) `skills/mcp_tool_generator.py:72` `def sanitize_description(summary, max_len)` -- Truncate and clean a command summary for use as a tool description.
- `sanitize_docstring` (function) `skills/mcp_tool_generator.py:85` `def sanitize_docstring(text)` -- Escape backslashes and quotes for triple-quoted docstrings.
- `generate_module` (function) `skills/mcp_tool_generator.py:106` `def generate_module(commands, existing_handlers, limit)` -- Build the complete Python source for mcp_generated_tools.py.
- `verify_coverage` (function) `skills/mcp_tool_generator.py:203` `def verify_coverage(commands, existing_handlers)` -- Compare indexed commands against existing MCP tool coverage.
- `main` (function) `skills/mcp_tool_generator.py:220` `def main()`

## skills/sessions_watcher.py
Depends on: `core/logging.py`, `modules/event_engine.py`, `modules/logging_config.py`, `skills/lazyown_facts.py`, `skills/lazyown_objective.py`
Imported by: `skills/lazyown_daemon.py`
- `_Handler.on_created` (method) `skills/sessions_watcher.py:376` `def on_created(self, event)`
- `_Handler.on_modified` (method) `skills/sessions_watcher.py:380` `def on_modified(self, event)`
- `main` (function) `skills/sessions_watcher.py:430` `def main()`

## skills/setup.sh
- `info` (function) `skills/setup.sh:15`
- `warn` (function) `skills/setup.sh:16`
- `die` (function) `skills/setup.sh:17`
- `paths_for_sudo` (function) `skills/setup.sh:61` -- Collect paths that exist on this system
- `add_nopasswd` (function) `skills/setup.sh:92`

## skills/swan_agent.py
Depends on: `core/logging.py`, `modules/detection_oracle.py`, `modules/logging_config.py`, `modules/moe_router.py`, `modules/rl_trainer.py`, `skills/hive_mind.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_policy.py`
Imported by: `modules/loop_ai_bridge.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `skills/unified_orchestrator.py`, `tests/test_moe_rl_swan.py`
- `SwanResult.is_success` (method) `skills/swan_agent.py:167` `def is_success(self)`
- `IResultAggregator.aggregate` (method) `skills/swan_agent.py:209` `def aggregate(self, task_type, goal, votes)` -- Return (synthesis_text, consensus_confidence).
- `ISwanOrchestrator.run` (method) `skills/swan_agent.py:226` `def run(self, task_type, goal, engagement_phase, timeout)` -- Execute with the best single expert and return result.
- `ISwanOrchestrator.ensemble_run` (method) `skills/swan_agent.py:236` `def ensemble_run(self, task_type, goal, n_experts, engagement_phase, timeout)` -- Execute with top-N experts in parallel and synthesize results.
- `WeightedTextAggregator.aggregate` (method) `skills/swan_agent.py:264` `def aggregate(self, task_type, goal, votes)`
- `ExpertExecutor.execute` (method) `skills/swan_agent.py:351` `def execute(self, expert_id, backend, model, goal, task_type, timeout, api_key)` -- Run the expert and return a SwanResult.
- `OutcomeEvaluator.evaluate` (method) `skills/swan_agent.py:479` `def evaluate(self, result, task_type)` -- Return (reward, detection_prob).
- `SwanOrchestrator.__init__` (method) `skills/swan_agent.py:572` `def __init__(self, executor, evaluator, aggregator, api_key)`
- `SwanOrchestrator.run` (method) `skills/swan_agent.py:592` `def run(self, task_type, goal, engagement_phase, timeout)` -- Execute the task with the best single expert selected by the MoE+RL router.
- `SwanOrchestrator.ensemble_run` (method) `skills/swan_agent.py:680` `def ensemble_run(self, task_type, goal, n_experts, engagement_phase, timeout)` -- Execute with top-N experts in parallel and synthesize results.
- `SwanOrchestrator.status` (method) `skills/swan_agent.py:763` `def status(self)` -- Return a diagnostic snapshot of the SWAN system.
- `mcp_swan_run` (function) `skills/swan_agent.py:945` `def mcp_swan_run(task_type, goal, phase)` -- Route and execute a task with the best MoE+RL-selected expert.
- `mcp_swan_ensemble` (function) `skills/swan_agent.py:968` `def mcp_swan_ensemble(task_type, goal, n_experts, phase)` -- Run top-N experts in parallel and return a synthesized result.
- `mcp_swan_status` (function) `skills/swan_agent.py:996` `def mcp_swan_status()` -- Return SWAN system status: expert weights, RL epsilon, performance.
- `mcp_swan_route` (function) `skills/swan_agent.py:1003` `def mcp_swan_route(task_type, goal)` -- Show which expert would be selected for a task without executing.
- `get_swan` (function) `skills/swan_agent.py:1039` `def get_swan(api_key)` -- Return (or create) the module-level singleton SwanOrchestrator.

## skills/toposwarm_autonomous.py
Depends on: `core/logging.py`, `modules/logging_config.py`, `modules/reactive_engine.py`, `modules/toposwarm_bridge.py`
- `PentestState.add_finding` (method) `skills/toposwarm_autonomous.py:145` `def add_finding(self, phase_name, text)`
- `PentestState.summary` (method) `skills/toposwarm_autonomous.py:149` `def summary(self)`
- `PentestState.to_dict` (method) `skills/toposwarm_autonomous.py:160` `def to_dict(self)`
- `AutonomousAgent.__init__` (method) `skills/toposwarm_autonomous.py:310` `def __init__(self, state, no_model, verbose, effort, max_phases, json_out)`
- `AutonomousAgent.run` (method) `skills/toposwarm_autonomous.py:432` `def run(self, start_phase)`
- `main` (function) `skills/toposwarm_autonomous.py:489` `def main(argv)`

## skills/unified_orchestrator.py
Depends on: `modules/engage_summary.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/swan_agent.py`
Imported by: `lazyown.py`, `tests/test_improvements_spec.py`
- `OrchestratorConfig.from_payload` (method) `skills/unified_orchestrator.py:111` `def from_payload(cls, payload)` -- Return a config with ``payload.json`` overrides applied.
- `OrchestratorGoal.with_defaults` (method) `skills/unified_orchestrator.py:156` `def with_defaults(self, config)` -- Return a copy with empty fields populated from ``config``.
- `OrchestratorResult.to_dict` (method) `skills/unified_orchestrator.py:197` `def to_dict(self)` -- Return a JSON-serialisable dictionary of the result.
- `IOrchestratorBackend.available` (method) `skills/unified_orchestrator.py:215` `def available(self)` -- Return ``True`` when this backend can satisfy a request.
- `IOrchestratorBackend.run` (method) `skills/unified_orchestrator.py:219` `def run(self, goal)` -- Execute ``goal`` and return a normalised :class:`OrchestratorResult`.
- `EventBus.__init__` (method) `skills/unified_orchestrator.py:233` `def __init__(self, config, root)` -- Bind the bus to the active config.
- `EventBus.path` (method) `skills/unified_orchestrator.py:252` `def path(self)` -- Return the resolved event file path.
- `EventBus.emit` (method) `skills/unified_orchestrator.py:256` `def emit(self, event)` -- Append a single sanitised event to the bus.
- `BackendRegistry.__init__` (method) `skills/unified_orchestrator.py:303` `def __init__(self, backends)` -- Bind the registry to a fixed-order tuple of backends.
- `BackendRegistry.names` (method) `skills/unified_orchestrator.py:327` `def names(self)` -- Return the registered backend names in declaration order.
- `BackendRegistry.get` (method) `skills/unified_orchestrator.py:331` `def get(self, name)` -- Return the backend registered as ``name`` or ``None``.
- `BackendRegistry.available` (method) `skills/unified_orchestrator.py:335` `def available(self)` -- Return every backend that currently reports availability.
- `RouterPolicy.__init__` (method) `skills/unified_orchestrator.py:347` `def __init__(self, config, registry)` -- Bind the policy to config and backend registry.
- `RouterPolicy.choose` (method) `skills/unified_orchestrator.py:352` `def choose(self, goal)` -- Return the backend that should execute ``goal``.
- `DaemonBackend.__init__` (method) `skills/unified_orchestrator.py:413` `def __init__(self, config, factory, payload)` -- Bind to config, optional engine factory and payload mapping.
- `DaemonBackend.available` (method) `skills/unified_orchestrator.py:435` `def available(self)` -- Return ``True`` when the underlying engine can be imported.
- `DaemonBackend.run` (method) `skills/unified_orchestrator.py:445` `def run(self, goal)` -- Execute a single-target kill-chain engagement.
- `DaemonBackend.effective_target` (method) `skills/unified_orchestrator.py:489` `def effective_target(self, goal)` -- Return the daemon target this backend would use for ``goal``.
- `HiveBackend.__init__` (method) `skills/unified_orchestrator.py:610` `def __init__(self, config, factory)` -- Bind to config and an optional queen factory.
- `HiveBackend.available` (method) `skills/unified_orchestrator.py:619` `def available(self)` -- Return ``True`` when the hive engine is importable.
- `HiveBackend.run` (method) `skills/unified_orchestrator.py:629` `def run(self, goal)` -- Plan, dispatch, collect and synthesise via the hive.
- `SwanBackend.__init__` (method) `skills/unified_orchestrator.py:711` `def __init__(self, config, factory)` -- Bind to config and an optional orchestrator factory.
- `SwanBackend.available` (method) `skills/unified_orchestrator.py:720` `def available(self)` -- Return ``True`` when the SWAN engine is importable.
- `SwanBackend.run` (method) `skills/unified_orchestrator.py:730` `def run(self, goal)` -- Execute a single SWAN task and normalise the result.
- `GoalValidator.__init__` (method) `skills/unified_orchestrator.py:814` `def __init__(self, config)` -- Bind the validator to the active configuration.
- `GoalValidator.validate` (method) `skills/unified_orchestrator.py:818` `def validate(self, goal, mode, phase, task_type, target, drones, timeout, api_key, metadata)` -- Return a normalised goal or raise :class:`ValueError`.
- `UnifiedOrchestrator.__init__` (method) `skills/unified_orchestrator.py:874` `def __init__(self, config, registry, router, validator, bus)` -- Bind the orchestrator to its collaborators.
- `UnifiedOrchestrator.backends` (method) `skills/unified_orchestrator.py:890` `def backends(self)` -- Return the registered backend names in declaration order.
- `UnifiedOrchestrator.execute` (method) `skills/unified_orchestrator.py:894` `def execute(self, goal, mode, phase, task_type, target, drones, timeout, api_key, metadata)` -- Validate, route, execute and emit one goal end-to-end.
- `build_default_orchestrator` (function) `skills/unified_orchestrator.py:995` `def build_default_orchestrator(payload, sessions_dir)` -- Wire the canonical three-backend orchestrator.

## skills/update_knowledge.py
Depends on: `core/logging.py`, `modules/logging_config.py`, `skills/lazyown_parquet_db.py`
- `main` (function) `skills/update_knowledge.py:40` `def main(argv)`

## slack_c2_bot.py
Depends on: `core/parsers.py`, `lazyown.py`, `modules/llm_adapter.py`, `utils.py`
- `SecureSessionManager.__init__` (method) `slack_c2_bot.py:29` `def __init__(self)`
- `SecureSessionManager.register_failed_attempt` (method) `slack_c2_bot.py:34` `def register_failed_attempt(self, user_id)`
- `SecureSessionManager.check_lockout` (method) `slack_c2_bot.py:42` `def check_lockout(self, user_id)`
- `SecureSessionManager.check_rate_limit` (method) `slack_c2_bot.py:52` `def check_rate_limit(self, user_id)`
- `SecureSessionManager.create_session` (method) `slack_c2_bot.py:63` `def create_session(self, user_id)`
- `SecureSessionManager.validate_session` (method) `slack_c2_bot.py:71` `def validate_session(self, user_id)`
- `SecureSessionManager.set_client` (method) `slack_c2_bot.py:81` `def set_client(self, user_id, client_id)`
- `SecureSessionManager.get_client` (method) `slack_c2_bot.py:85` `def get_client(self, user_id)`
- `capture_shell_output` (function) `slack_c2_bot.py:95` `def capture_shell_output(cmd)`
- `handle_message` (function) `slack_c2_bot.py:113` `def handle_message(event, say, logger)`
- `cmd_addcli` (function) `slack_c2_bot.py:177` `def cmd_addcli(ack, respond, command)`
- `cmd_clients` (function) `slack_c2_bot.py:195` `def cmd_clients(ack, respond, command)`
- `cmd_download` (function) `slack_c2_bot.py:209` `def cmd_download(ack, respond, command)`
- `handle_file` (function) `slack_c2_bot.py:240` `def handle_file(event, say, logger)`
- `mentioned` (function) `slack_c2_bot.py:252` `def mentioned(ack, say, event)`

## static/js/3d-force-graph-1.73.4.min.js
Depends on: `cli/assign.py`, `lazyown-docker/init.sh`, `modules/exp.c`
- `is` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `newNode` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `update` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `insertBodies` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `insert` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `isSamePosition` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `updateBoundingBox` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `resetBoundingBox` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `Te` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `c` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `Vr` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `l` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `y` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `u` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `s` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `g` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `c` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `b` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `u` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `differentBody` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `coefficient` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `h` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `v` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `l` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `s` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `hh` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `s` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `a` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `Hh` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `Jh` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `y` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `uu` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:2` -- Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `that` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `signature` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `signature` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `signature` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `t` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `i` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `ld` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `pd` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `y` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `I` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `Md` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `cf` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `Ef` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `r` (function) `static/js/3d-force-graph-1.73.4.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...

## static/js/bootstrap-4.5.2.min.js
Depends on: `cli/show.py`
- `r` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `i` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `n` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `s` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `d` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `h` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !
- `i` (function) `static/js/bootstrap-4.5.2.min.js:6` -- !

## static/js/bootstrap-5.3.0.bundle.min.js
Depends on: `cli/assign.py`, `cli/show.py`
- `n` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `i` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `o` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `a` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `r` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `n` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `i` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `n` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `h` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !
- `M` (function) `static/js/bootstrap-5.3.0.bundle.min.js:6` -- !

## static/js/chart.min.js
Depends on: `cli/assign.py`, `cli/show.py`, `lazyown-docker/init.sh`, `modules/notify.py`
- `i` (function) `static/js/chart.min.js:7` -- !
- `h` (function) `static/js/chart.min.js:7` -- !
- `r` (function) `static/js/chart.min.js:7` -- !
- `it` (function) `static/js/chart.min.js:7` -- !
- `yt` (function) `static/js/chart.min.js:13`
- `e` (function) `static/js/chart.min.js:13`
- `s` (function) `static/js/chart.min.js:13`
- `ye` (function) `static/js/chart.min.js:13`
- `o` (function) `static/js/chart.min.js:13`
- `m` (function) `static/js/chart.min.js:13`
- `s` (function) `static/js/chart.min.js:13`
- `Ue` (function) `static/js/chart.min.js:13`
- `Ge` (function) `static/js/chart.min.js:13`
- `i` (function) `static/js/chart.min.js:13`
- `y` (function) `static/js/chart.min.js:13`
- `a` (function) `static/js/chart.min.js:13`
- `Xs` (function) `static/js/chart.min.js:13`
- `e` (function) `static/js/chart.min.js:13`
- `a` (function) `static/js/chart.min.js:13`
- `bn` (function) `static/js/chart.min.js:13`
- `a` (function) `static/js/chart.min.js:13`
- `l` (function) `static/js/chart.min.js:13`
- `o` (function) `static/js/chart.min.js:13`
- `e` (function) `static/js/chart.min.js:13`
- `t` (function) `static/js/chart.min.js:13`
- `p` (function) `static/js/chart.min.js:13`
- `e` (function) `static/js/chart.min.js:13`
- `s` (function) `static/js/chart.min.js:13`
- `a` (function) `static/js/chart.min.js:13`
- `e` (function) `static/js/chart.min.js:13`
- `s` (function) `static/js/chart.min.js:13`
- `s` (function) `static/js/chart.min.js:13`
- `Se` (function) `static/js/chart.min.js:13`
- `s` (function) `static/js/chart.min.js:13`
- `r` (function) `static/js/chart.min.js:13`
- `i` (function) `static/js/chart.min.js:13`
- `e` (function) `static/js/chart.min.js:13`
- `d` (function) `static/js/chart.min.js:13`
- `s` (function) `static/js/chart.min.js:13`
- `e` (function) `static/js/chart.min.js:13`
- `n` (function) `static/js/chart.min.js:13`
- `o` (function) `static/js/chart.min.js:13`
- `s` (function) `static/js/chart.min.js:13`
- `n` (function) `static/js/chart.min.js:13`
- `o` (function) `static/js/chart.min.js:13`
- `y` (function) `static/js/chart.min.js:13`
- `g` (function) `static/js/chart.min.js:13`
- `p` (function) `static/js/chart.min.js:13`

## static/js/force-graph-1.43.5.min.js
Depends on: `cli/assign.py`, `cli/style.py`, `modules/exp.c`
- `n` (function) `static/js/force-graph-1.43.5.min.js:2` -- Version 1.43.5 force-graph - https://github.com/vasturiano/force-graph
- `n` (function) `static/js/force-graph-1.43.5.min.js:2` -- Version 1.43.5 force-graph - https://github.com/vasturiano/force-graph
- `Cn` (function) `static/js/force-graph-1.43.5.min.js:2` -- Version 1.43.5 force-graph - https://github.com/vasturiano/force-graph
- `Tr` (function) `static/js/force-graph-1.43.5.min.js:2` -- Version 1.43.5 force-graph - https://github.com/vasturiano/force-graph
- `o` (function) `static/js/force-graph-1.43.5.min.js:2` -- Version 1.43.5 force-graph - https://github.com/vasturiano/force-graph
- `ti` (function) `static/js/force-graph-1.43.5.min.js:2` -- Version 1.43.5 force-graph - https://github.com/vasturiano/force-graph
- `e` (function) `static/js/force-graph-1.43.5.min.js:2` -- Version 1.43.5 force-graph - https://github.com/vasturiano/force-graph
- `t` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `h` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `u` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `y` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `l` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `b` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `h` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `s` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `f` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `i` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `e` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `Fi` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `r` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `n` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `sa` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `ha` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `v` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `o` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...
- `c` (function) `static/js/force-graph-1.43.5.min.js:5` -- <http://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef (WCAG Version 2) Analyze the 2 colors and returns...


Next: [API_p22.md](API_p22.md)
