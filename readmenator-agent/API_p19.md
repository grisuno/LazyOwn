# API (page 19 of 24)
Previous: [API_p18.md](API_p18.md)

## skills/autonomous_daemon.py
Depends on: `core/logging.py`, `modules/asset_graph.py`, `modules/db.py`, `modules/detection_oracle.py`, `modules/enrich.py`, `modules/event_consumers.py`, `modules/evidence.py`, `modules/finding_lifecycle.py`, `modules/goals.py`, `modules/intercept.py`, `modules/killchain.py`, `modules/llm_pool.py`, `modules/logging_config.py`, `modules/metrics.py`, `modules/notify.py`, `modules/obs_parser.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `modules/reactive_engine.py`, `modules/rl_trainer.py`, `modules/toolset.py`, `modules/traffic_recorder.py`, `skills/daemon_control.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_helpers.py`, `skills/lazyown_objective.py`, `skills/lazyown_policy.py`, `skills/swan_agent.py`
Imported by: `cli/commands/database.py`, `cli/commands/session_ops.py`, `modules/pipeline_engine.py`, `skills/autonomous_replay.py`, `skills/lazyown_mcp.py`, `skills/tests/test_autonomous_daemon.py`, `skills/unified_orchestrator.py`, `tests/test_autonomous_replay.py`, `tests/test_daemon_loop.py`, `tests/test_engage_gates.py`, `tests/test_engage_orchestrator.py`, `tests/test_metrics_aware_selector.py`, `tests/test_moe_rl_swan.py`, `tests/test_pipeline_engine.py`, `tests/test_scope_bound_auto_gate.py`
- `compute_decision_seed` (function) `skills/autonomous_daemon.py:394` `def compute_decision_seed(objective_id, step_n, source)` -- Return a deterministic identifier for a daemon decision.
- `ICommandRunner.run` (method) `skills/autonomous_daemon.py:426` `def run(self, command, timeout)` -- Execute command within timeout seconds.
- `ICommandRunner.name` (method) `skills/autonomous_daemon.py:431` `def name(self)` -- Human-readable identifier for this runner.
- `MCPCommandRunner.name` (method) `skills/autonomous_daemon.py:482` `def name(self)`
- `MCPCommandRunner.run` (method) `skills/autonomous_daemon.py:485` `def run(self, command, timeout)` -- Try to import and call the MCP runner.
- `PTYCommandRunner.name` (method) `skills/autonomous_daemon.py:502` `def name(self)`
- `PTYCommandRunner.run` (method) `skills/autonomous_daemon.py:505` `def run(self, command, timeout)` -- Execute command via PTY.
- `CommandRunnerChain.__init__` (method) `skills/autonomous_daemon.py:592` `def __init__(self, runners)`
- `CommandRunnerChain.name` (method) `skills/autonomous_daemon.py:598` `def name(self)`
- `CommandRunnerChain.run` (method) `skills/autonomous_daemon.py:601` `def run(self, command, timeout)` -- Try each runner in sequence.
- `ICommandSelector.select` (method) `skills/autonomous_daemon.py:689` `def select(self, target, phase, context)` -- Return a CommandDecision or None if this selector has no suggestion.
- `ReactiveSelector.__init__` (method) `skills/autonomous_daemon.py:704` `def __init__(self, reactive_engine)`
- `ReactiveSelector.register_output` (method) `skills/autonomous_daemon.py:708` `def register_output(self, output, command, platform)` -- Feed reactive engine with last command output to generate new decisions.
- `ReactiveSelector.select` (method) `skills/autonomous_daemon.py:735` `def select(self, target, phase, context)` -- Pop and return the pending reactive decision if present.
- `ParquetSelector.__init__` (method) `skills/autonomous_daemon.py:750` `def __init__(self, pdb, fail_counts)`
- `ParquetSelector.select` (method) `skills/autonomous_daemon.py:754` `def select(self, target, phase, context)` -- Return the most-frequent successful command for this phase.
- `BridgeSelector.__init__` (method) `skills/autonomous_daemon.py:796` `def __init__(self, dispatcher, fail_counts)`
- `BridgeSelector.select` (method) `skills/autonomous_daemon.py:800` `def select(self, target, phase, context)` -- Return a bridge catalog suggestion for this phase.
- `LLMSelector.select` (method) `skills/autonomous_daemon.py:866` `def select(self, target, phase, context)` -- Return an LLM-suggested command with catalog context, or None if disabled.
- `SWANSelector.select` (method) `skills/autonomous_daemon.py:988` `def select(self, target, phase, context)` -- Ask the best MoE expert for a command recommendation.
- `FallbackSelector.select` (method) `skills/autonomous_daemon.py:1034` `def select(self, target, phase, context)` -- Return the static fallback command for this phase.
- `MetricsAwareSelector.__init__` (method) `skills/autonomous_daemon.py:1071` `def __init__(self, wrapped, metrics_source, min_success_rate, min_attempts, window_seconds, cache_ttl_s, clock)` -- Initialise the decorator.
- `MetricsAwareSelector.wrapped` (method) `skills/autonomous_daemon.py:1117` `def wrapped(self)` -- Return the underlying selector for introspection in tests.
- `MetricsAwareSelector.select` (method) `skills/autonomous_daemon.py:1203` `def select(self, target, phase, context)` -- Honour the :class:`ICommandSelector` contract.
- `CredentialSpraySelector.__init__` (method) `skills/autonomous_daemon.py:1304` `def __init__(self, fail_counts)`
- `CredentialSpraySelector.select` (method) `skills/autonomous_daemon.py:1308` `def select(self, target, phase, context)` -- Return a spray command when credentials + matching service are available.
- `CascadeStrategy.__init__` (method) `skills/autonomous_daemon.py:1344` `def __init__(self, selectors)`
- `CascadeStrategy.next_command` (method) `skills/autonomous_daemon.py:1347` `def next_command(self, target, phase, context)` -- Try each selector in order.
- `StrategyEngine.__init__` (method) `skills/autonomous_daemon.py:1382` `def __init__(self, runner, selectors)`
- `StrategyEngine.register_output` (method) `skills/autonomous_daemon.py:1409` `def register_output(self, output, command, platform, success)` -- Feed the reactive selector with the last command output.
- `StrategyEngine.next_command` (method) `skills/autonomous_daemon.py:1423` `def next_command(self, target, phase, services, os_hint)` -- Select the next command for target/phase using the cascade.
- `IObjectiveHandler.handle` (method) `skills/autonomous_daemon.py:1457` `def handle(self, objective_id, objective_text, target, context)` -- Execute objective and return a list of step results.
- `ExecutionEngine.__init__` (method) `skills/autonomous_daemon.py:1479` `def __init__(self, strategy, max_steps, world_model, obs_parser, facts, loop)`
- `ExecutionEngine.handle` (method) `skills/autonomous_daemon.py:1495` `def handle(self, objective_id, objective_text, target, context)` -- Synchronous entry point.
- `ExecutionEngine.run_async` (method) `skills/autonomous_daemon.py:1505` `def run_async(self, objective_id, objective_text, target)` -- Asyncio entry point used by objective_loop.
- `DroneCoordinator.__init__` (method) `skills/autonomous_daemon.py:2814` `def __init__(self)`
- `DroneCoordinator.process_findings` (method) `skills/autonomous_daemon.py:2819` `def process_findings(self, findings, target, objective_id, payload_key)` -- Launch drones for relevant findings.
- `EnginePhaseResult.did_switch` (method) `skills/autonomous_daemon.py:3120` `def did_switch(self)` -- True when the orchestrator used a fallback tool.
- `IToolFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:3129` `def next_tool(self, failed_command, phase, attempt)` -- Return the next candidate command or None when exhausted.
- `StaticFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:3146` `def next_tool(self, failed_command, phase, attempt)`
- `BridgeFallbackResolver.__init__` (method) `skills/autonomous_daemon.py:3168` `def __init__(self, dispatcher)`
- `BridgeFallbackResolver.next_tool` (method) `skills/autonomous_daemon.py:3193` `def next_tool(self, failed_command, phase, attempt)`
- `_ShellDetector.__init__` (method) `skills/autonomous_daemon.py:3220` `def __init__(self, narrator)`
- `_ShellDetector.poll` (method) `skills/autonomous_daemon.py:3225` `def poll(self, target)` -- Return the newly-detected client_ids since the previous poll.
- `_ShellDetector.detect_in_output` (method) `skills/autonomous_daemon.py:3266` `def detect_in_output(self, output, target)` -- Return True when a shell/root-shell signal appears in command output.
- `EngageOrchestrator.__init__` (method) `skills/autonomous_daemon.py:3312` `def __init__(self, target, runner, narrator, approval_gate, fallback_resolver, shell_detector, plan...`
- `EngageOrchestrator.engagement_id` (method) `skills/autonomous_daemon.py:3357` `def engagement_id(self)` -- Stable id for this engagement (correlates events in logs).
- `EngageOrchestrator.run` (method) `skills/autonomous_daemon.py:3361` `def run(self)` -- Drive the full plan against the configured target.
- `mcp_engage_target` (function) `skills/autonomous_daemon.py:4005` `def mcp_engage_target(target, max_switches_per_step, detach, auto)` -- Public MCP / CLI entry point for the engage verb.
- `mcp_engage_status` (function) `skills/autonomous_daemon.py:4095` `def mcp_engage_status(last_n)` -- Return the last N lines of sessions/engagement.log plus pending approvals.
- `mcp_engage_approve` (function) `skills/autonomous_daemon.py:4121` `def mcp_engage_approve(approval_id, decision, operator)` -- Resolve a pending approval. decision must be 'approved' or 'denied'.
- `mcp_engage_list_pending` (function) `skills/autonomous_daemon.py:4146` `def mcp_engage_list_pending()` -- List every pending approval awaiting an operator decision.
- `cmd_engage` (function) `skills/autonomous_daemon.py:4164` `def cmd_engage(target, max_switches_per_step, detach)` -- CLI helper bound to the `engage <ip>` daemon subcommand.
- `objective_loop` (function) `skills/autonomous_daemon.py:4203` `def objective_loop(max_steps, loop)` -- Root autonomous loop: takes pending objectives from objectives.jsonl and executes them without waiting for Claude...
- `world_model_watcher` (function) `skills/autonomous_daemon.py:4346` `def world_model_watcher(loop)` -- Watch world_model.json.
- `heartbeat_loop` (function) `skills/autonomous_daemon.py:4537` `def heartbeat_loop()` -- Emit heartbeat and write status every HEARTBEAT_S seconds.
- `cmd_run` (function) `skills/autonomous_daemon.py:4664` `def cmd_run(max_steps)` -- Run daemon in foreground (debug mode).
- `cmd_start` (function) `skills/autonomous_daemon.py:4673` `def cmd_start(max_steps)` -- Fork, detach, and run daemon in background.
- `cmd_stop` (function) `skills/autonomous_daemon.py:4703` `def cmd_stop()` -- Send SIGTERM to the running daemon.
- `cmd_status` (function) `skills/autonomous_daemon.py:4720` `def cmd_status()` -- Print current daemon status to stdout.
- `cmd_inject` (function) `skills/autonomous_daemon.py:4736` `def cmd_inject(text, priority)` -- Inject an objective from the CLI, split into verifiable sub-goals.
- `mcp_autonomous_start` (function) `skills/autonomous_daemon.py:4770` `def mcp_autonomous_start(max_steps, backend)` -- Start the autonomous daemon in a background thread (for MCP calls).
- `mcp_autonomous_stop` (function) `skills/autonomous_daemon.py:4812` `def mcp_autonomous_stop()` -- Stop the autonomous daemon.
- `mcp_autonomous_status` (function) `skills/autonomous_daemon.py:4828` `def mcp_autonomous_status()` -- Current daemon state: objectives, steps, drones, phase.
- `mcp_autonomous_inject` (function) `skills/autonomous_daemon.py:4841` `def mcp_autonomous_inject(text, priority, target)` -- Inject an objective into the daemon queue and into sessions/tasks.json.
- `mcp_autonomous_events` (function) `skills/autonomous_daemon.py:4885` `def mcp_autonomous_events(last_n)` -- Read the last N events from autonomous_events.jsonl.

## skills/autonomous_replay.py
Depends on: `core/logging.py`, `skills/autonomous_daemon.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_autonomous_replay.py`
- `ReplayReport.to_dict` (method) `skills/autonomous_replay.py:114` `def to_dict(self)` -- Return the report as a JSON-serialisable dictionary.
- `EventLogReader.__init__` (method) `skills/autonomous_replay.py:136` `def __init__(self, path)` -- Initialise the reader.
- `EventLogReader.path` (method) `skills/autonomous_replay.py:147` `def path(self)` -- Return the source path.
- `EventLogReader.read` (method) `skills/autonomous_replay.py:152` `def read(self)` -- Return every event in the log, oldest first.
- `EventLogReader.slice` (method) `skills/autonomous_replay.py:177` `def slice(self, events, from_event_id, to_event_id)` -- Return the inclusive subrange of *events* by ``id``.
- `ReplayDispatcher.__init__` (method) `skills/autonomous_replay.py:221` `def __init__(self, reader, seed_fn)` -- Initialise the dispatcher.
- `ReplayDispatcher.trace` (method) `skills/autonomous_replay.py:325` `def trace(self, from_event_id, to_event_id)` -- Replay the recorded decision sequence without executing it.
- `ReplayDispatcher.execute` (method) `skills/autonomous_replay.py:357` `def execute(self, from_event_id, to_event_id, runner, timeout)` -- Replay the recorded sequence and re-run each command.
- `replay` (function) `skills/autonomous_replay.py:473` `def replay(from_event_id, to_event_id, mode, events_path, runner, timeout)` -- Convenience entry point used by the MCP tool layer.

## skills/claude_md_orchestrator/bdd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/tdd_agent.py`, `skills/claude_md_orchestrator/validators.py`
- `run` (function) `skills/claude_md_orchestrator/bdd_agent.py:151` `def run(contract, spec, suite, config)` -- Run the implementation agent for one contract.

## skills/claude_md_orchestrator/boy_scout.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `run` (function) `skills/claude_md_orchestrator/boy_scout.py:90` `def run(state, config)` -- Run the boy scout pass for one contract.
- `write_report` (function) `skills/claude_md_orchestrator/boy_scout.py:110` `def write_report(report, config)` -- Persist the boy scout proposal to disk.

## skills/claude_md_orchestrator/cicd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
- `run` (function) `skills/claude_md_orchestrator/cicd_agent.py:177` `def run(contract, spec, report, config)` -- Run the CI and CD agent for one contract.

## skills/claude_md_orchestrator/config.py
Imported by: `skills/claude_md_orchestrator/__init__.py`, `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/cicd_agent.py`, `skills/claude_md_orchestrator/documentation_agent.py`, `skills/claude_md_orchestrator/orchestrator.py`, `skills/claude_md_orchestrator/parser.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`
- `Config.ensure` (method) `skills/claude_md_orchestrator/config.py:112` `def ensure(self)` -- Create the run subdirectories if they do not exist.
- `Config.state_path` (method) `skills/claude_md_orchestrator/config.py:122` `def state_path(self)` -- Return the absolute path of the cycle state file.
- `Config.specs_dir` (method) `skills/claude_md_orchestrator/config.py:126` `def specs_dir(self)` -- Return the absolute path of the spec directory.
- `Config.tests_dir` (method) `skills/claude_md_orchestrator/config.py:130` `def tests_dir(self)` -- Return the absolute path of the test directory.
- `Config.src_dir` (method) `skills/claude_md_orchestrator/config.py:134` `def src_dir(self)` -- Return the absolute path of the implementation directory.
- `Config.review_dir` (method) `skills/claude_md_orchestrator/config.py:138` `def review_dir(self)` -- Return the absolute path of the review directory.
- `Config.docs_dir` (method) `skills/claude_md_orchestrator/config.py:142` `def docs_dir(self)` -- Return the absolute path of the documentation directory.
- `Config.logs_dir` (method) `skills/claude_md_orchestrator/config.py:146` `def logs_dir(self)` -- Return the absolute path of the log directory.
- `Config.log_path` (method) `skills/claude_md_orchestrator/config.py:150` `def log_path(self)` -- Return the absolute path of the JSONL log for the active run.
- `load_config` (function) `skills/claude_md_orchestrator/config.py:155` `def load_config()` -- Build a Config from environment variables and return it.
- `resolve_optional` (function) `skills/claude_md_orchestrator/config.py:164` `def resolve_optional(config, key)` -- Return the environment value for a key or None when missing.

## skills/claude_md_orchestrator/documentation_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
- `run` (function) `skills/claude_md_orchestrator/documentation_agent.py:123` `def run(contract, spec, report, config)` -- Run the documentation agent for one contract.

## skills/claude_md_orchestrator/models.py
Depends on: `cli/commands/enum.py`
Imported by: `skills/claude_md_orchestrator/__init__.py`, `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/cicd_agent.py`, `skills/claude_md_orchestrator/documentation_agent.py`, `skills/claude_md_orchestrator/orchestrator.py`, `skills/claude_md_orchestrator/parser.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`, `skills/claude_md_orchestrator/validators.py`
- `Contract.to_dict` (method) `skills/claude_md_orchestrator/models.py:91` `def to_dict(self)` -- Return a JSON friendly view of the contract.
- `Contract.from_dict` (method) `skills/claude_md_orchestrator/models.py:96` `def from_dict(cls, data)` -- Build a Contract from a JSON friendly dictionary.
- `SadPath.to_dict` (method) `skills/claude_md_orchestrator/models.py:120` `def to_dict(self)` -- Return a JSON friendly view of the sad path.
- `SadPath.from_dict` (method) `skills/claude_md_orchestrator/models.py:125` `def from_dict(cls, data)` -- Build a SadPath from a JSON friendly dictionary.
- `Spec.to_dict` (method) `skills/claude_md_orchestrator/models.py:166` `def to_dict(self)` -- Return a JSON friendly view of the spec.
- `Spec.from_dict` (method) `skills/claude_md_orchestrator/models.py:173` `def from_dict(cls, data)` -- Build a Spec from a JSON friendly dictionary.
- `Spec.validate` (method) `skills/claude_md_orchestrator/models.py:189` `def validate(self, min_sad_paths)` -- Return the list of DoD violations the spec carries.
- `TestSuite.to_dict` (method) `skills/claude_md_orchestrator/models.py:236` `def to_dict(self)` -- Return a JSON friendly view of the test suite.
- `TestSuite.from_dict` (method) `skills/claude_md_orchestrator/models.py:243` `def from_dict(cls, data)` -- Build a TestSuite from a JSON friendly dictionary.
- `Finding.to_dict` (method) `skills/claude_md_orchestrator/models.py:270` `def to_dict(self)` -- Return a JSON friendly view of the finding.
- `Finding.from_dict` (method) `skills/claude_md_orchestrator/models.py:280` `def from_dict(cls, data)` -- Build a Finding from a JSON friendly dictionary.
- `ReviewReport.blockers` (method) `skills/claude_md_orchestrator/models.py:315` `def blockers(self)` -- Return the list of blocker findings.
- `ReviewReport.to_dict` (method) `skills/claude_md_orchestrator/models.py:319` `def to_dict(self)` -- Return a JSON friendly view of the report.
- `ReviewReport.from_dict` (method) `skills/claude_md_orchestrator/models.py:333` `def from_dict(cls, data)` -- Build a ReviewReport from a JSON friendly dictionary.
- `CicleState.to_dict` (method) `skills/claude_md_orchestrator/models.py:383` `def to_dict(self)` -- Return a JSON friendly view of the state.
- `CicleState.from_dict` (method) `skills/claude_md_orchestrator/models.py:402` `def from_dict(cls, data)` -- Build a CicleState from a JSON friendly dictionary.
- `CicleStateFile.to_dict` (method) `skills/claude_md_orchestrator/models.py:440` `def to_dict(self)` -- Return a JSON friendly view of the state file.
- `CicleStateFile.from_dict` (method) `skills/claude_md_orchestrator/models.py:450` `def from_dict(cls, data)` -- Build a CicleStateFile from a JSON friendly dictionary.
- `CicleStateFile.save` (method) `skills/claude_md_orchestrator/models.py:459` `def save(self, path)` -- Persist the state to disk as pretty JSON.
- `CicleStateFile.load` (method) `skills/claude_md_orchestrator/models.py:467` `def load(cls, path)` -- Read the state from disk.
- `write_jsonl` (function) `skills/claude_md_orchestrator/models.py:480` `def write_jsonl(path, event)` -- Append a single JSONL event to the log file.

## skills/claude_md_orchestrator/orchestrator.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/parser.py`
Imported by: `skills/claude_md_orchestrator/__init__.py`
- `run` (function) `skills/claude_md_orchestrator/orchestrator.py:275` `def run(config, options)` -- Run the orchestrator for the current run directory.
- `summary_to_dict` (function) `skills/claude_md_orchestrator/orchestrator.py:306` `def summary_to_dict(summary)` -- Return a JSON friendly view of the summary.
- `main` (function) `skills/claude_md_orchestrator/orchestrator.py:393` `def main(argv)` -- Run the orchestrator CLI and return the process exit code.

## skills/claude_md_orchestrator/parser.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`
Imported by: `pwntomate.py`, `skills/claude_md_orchestrator/orchestrator.py`, `static/js/xterm.js`, `utils.py`
- `flush_body` (function) `skills/claude_md_orchestrator/parser.py:97` `def flush_body()`
- `parse_claude_md` (function) `skills/claude_md_orchestrator/parser.py:167` `def parse_claude_md(path)` -- Parse a CLAUDE.md file and return the list of contracts.
- `load_contracts` (function) `skills/claude_md_orchestrator/parser.py:225` `def load_contracts(config, seeds)` -- Return the contracts the orchestrator should process.

## skills/claude_md_orchestrator/reviewer_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `run` (function) `skills/claude_md_orchestrator/reviewer_agent.py:171` `def run(state, config)` -- Run the reviewer for one contract.
- `write_report` (function) `skills/claude_md_orchestrator/reviewer_agent.py:225` `def write_report(report, config)` -- Persist the report as JSON inside the run review directory.

## skills/claude_md_orchestrator/sdd_agent.py
Depends on: `modules/llm_factory.py`, `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
- `run` (function) `skills/claude_md_orchestrator/sdd_agent.py:204` `def run(contract, config)` -- Run the spec agent for one contract.

## skills/claude_md_orchestrator/tdd_agent.py
Depends on: `skills/claude_md_orchestrator/config.py`, `skills/claude_md_orchestrator/models.py`, `skills/claude_md_orchestrator/validators.py`
Imported by: `skills/claude_md_orchestrator/bdd_agent.py`
- `run` (function) `skills/claude_md_orchestrator/tdd_agent.py:175` `def run(contract, spec, config)` -- Run the test agent for one contract.
- `read_test_source` (function) `skills/claude_md_orchestrator/tdd_agent.py:228` `def read_test_source(test_path)` -- Return the test source for inspection.

## skills/claude_md_orchestrator/validators.py
Depends on: `core/hardening.py`, `skills/claude_md_orchestrator/models.py`
Imported by: `skills/claude_md_orchestrator/bdd_agent.py`, `skills/claude_md_orchestrator/boy_scout.py`, `skills/claude_md_orchestrator/reviewer_agent.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `skills/claude_md_orchestrator/tdd_agent.py`, `tests/test_security_alerts_fix.py`
- `_EmojiSpan.__init__` (method) `skills/claude_md_orchestrator/validators.py:60` `def __init__(self, start, text)` -- Store match offset and matched text.
- `_EmojiSpan.start` (method) `skills/claude_md_orchestrator/validators.py:65` `def start(self)` -- Return the match offset.
- `_EmojiSpan.group` (method) `skills/claude_md_orchestrator/validators.py:69` `def group(self, index)` -- Return the matched text.
- `_EmojiPattern.finditer` (method) `skills/claude_md_orchestrator/validators.py:81` `def finditer(self, content)` -- Yield one span per emoji character in encounter order.
- `CheckResult.passed` (method) `skills/claude_md_orchestrator/validators.py:107` `def passed(self)` -- Return True when the result has no findings.
- `CheckResult.blocks` (method) `skills/claude_md_orchestrator/validators.py:111` `def blocks(self)` -- Return the blocker findings only.
- `find_block_comments` (function) `skills/claude_md_orchestrator/validators.py:116` `def find_block_comments(source)` -- Return the start and end line of every block comment in source.
- `find_inline_comments` (function) `skills/claude_md_orchestrator/validators.py:138` `def find_inline_comments(source)` -- Return the line numbers of every inline comment in source.
- `check_no_comments` (function) `skills/claude_md_orchestrator/validators.py:155` `def check_no_comments(source, path)` -- Return a finding for every comment in the source code.
- `check_no_emoji` (function) `skills/claude_md_orchestrator/validators.py:186` `def check_no_emoji(content, path)` -- Return a finding for every emoji the content carries.
- `check_no_forbidden_markers` (function) `skills/claude_md_orchestrator/validators.py:208` `def check_no_forbidden_markers(content, path)` -- Return a finding for every TODO, FIXME, XXX, or HACK marker.
- `check_english_only` (function) `skills/claude_md_orchestrator/validators.py:225` `def check_english_only(source, path)` -- Return a finding for every Spanish hint the source carries.
- `check_docstrings` (function) `skills/claude_md_orchestrator/validators.py:249` `def check_docstrings(source, path)` -- Return a finding for every public function or class without a docstring.
- `check_no_hardcoded_paths_or_ips` (function) `skills/claude_md_orchestrator/validators.py:290` `def check_no_hardcoded_paths_or_ips(source, path)` -- Return a finding for every absolute path or IP literal.
- `check_magic_numbers` (function) `skills/claude_md_orchestrator/validators.py:324` `def check_magic_numbers(source, path, allow)` -- Return a finding for every numeric literal that is not in the allow list.
- `check_source` (function) `skills/claude_md_orchestrator/validators.py:359` `def check_source(source, path, allow_numbers)` -- Run every source level DoD check and return the findings.
- `check_markdown` (function) `skills/claude_md_orchestrator/validators.py:372` `def check_markdown(content, path)` -- Run every markdown level DoD check and return the findings.
- `check_spec` (function) `skills/claude_md_orchestrator/validators.py:381` `def check_spec(spec, min_sad_paths)` -- Run the spec level DoD check and return the findings.

## skills/daemon_control.py
Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_daemon_control.py`
- `PendingAction.is_expired` (method) `skills/daemon_control.py:79` `def is_expired(self, now)` -- Return ``True`` when a still-pending action has exceeded its TTL.
- `ControlState.to_dict` (method) `skills/daemon_control.py:110` `def to_dict(self)` -- Serialise the state to a plain JSON-ready dict.
- `ControlState.from_dict` (method) `skills/daemon_control.py:121` `def from_dict(cls, data)` -- Build a state from JSON data, sanitising malformed input.
- `DaemonControl.__init__` (method) `skills/daemon_control.py:171` `def __init__(self, sessions_dir)` -- Pin the control file to ``<sessions_dir>/daemon_control.json``.
- `DaemonControl.path` (method) `skills/daemon_control.py:184` `def path(self)` -- Absolute path of the control file on disk.
- `DaemonControl.load` (method) `skills/daemon_control.py:188` `def load(self)` -- Return the current state or defaults when the file is missing.
- `DaemonControl.save` (method) `skills/daemon_control.py:201` `def save(self, state)` -- Persist ``state`` atomically.
- `DaemonControl.set_mode` (method) `skills/daemon_control.py:231` `def set_mode(self, mode)` -- Switch between :data:`MODE_AUTO`, :data:`MODE_APPROVAL`, :data:`MODE_PAUSED`.
- `DaemonControl.pause` (method) `skills/daemon_control.py:240` `def pause(self)` -- Convenience wrapper for ``set_mode(MODE_PAUSED)``.
- `DaemonControl.resume` (method) `skills/daemon_control.py:244` `def resume(self)` -- Convenience wrapper for ``set_mode(MODE_AUTO)``.
- `DaemonControl.require_approval` (method) `skills/daemon_control.py:248` `def require_approval(self)` -- Convenience wrapper for ``set_mode(MODE_APPROVAL)``.
- `DaemonControl.add_veto` (method) `skills/daemon_control.py:252` `def add_veto(self, command_token)` -- Append a first-token name to the veto list.
- `DaemonControl.remove_veto` (method) `skills/daemon_control.py:267` `def remove_veto(self, command_token)` -- Remove a previously vetoed command from the list.
- `DaemonControl.clear_vetoes` (method) `skills/daemon_control.py:275` `def clear_vetoes(self)` -- Remove every entry from the veto list.
- `DaemonControl.set_focus` (method) `skills/daemon_control.py:282` `def set_focus(self, targets)` -- Replace the focus-target list.
- `DaemonControl.propose` (method) `skills/daemon_control.py:290` `def propose(self, command)` -- Daemon-side: register a pending action awaiting approval.
- `DaemonControl.decide` (method) `skills/daemon_control.py:317` `def decide(self, action_id, decision)` -- Operator-side: approve or veto the pending action.
- `DaemonControl.consume` (method) `skills/daemon_control.py:343` `def consume(self, action_id)` -- Daemon-side: read the final decision and clear the slot.
- `DaemonControl.is_paused` (method) `skills/daemon_control.py:375` `def is_paused(self)` -- Return ``True`` when the daemon must stop before executing.
- `DaemonControl.is_vetoed` (method) `skills/daemon_control.py:379` `def is_vetoed(self, command)` -- Return ``True`` when the command's first token is in the veto list.
- `DaemonControl.target_in_focus` (method) `skills/daemon_control.py:386` `def target_in_focus(self, target)` -- Return ``True`` when no focus is configured or ``target`` is in focus.
- `wait_for_decision` (function) `skills/daemon_control.py:394` `def wait_for_decision(control, action)` -- Block until the operator decides or the TTL expires.
- `wait_until_unpaused` (function) `skills/daemon_control.py:445` `def wait_until_unpaused(control)` -- Block while the daemon is paused, returning when it resumes.

## skills/daemon_health.py
Imported by: `lazyc2.py`
- `is_daemon_alive` (function) `skills/daemon_health.py:36` `def is_daemon_alive(timeout)` -- Check whether the autonomous daemon wrote a heartbeat recently.
- `daemon_status` (function) `skills/daemon_health.py:58` `def daemon_status(timeout)` -- Return the full daemon health snapshot.
- `DaemonHealth.__init__` (method) `skills/daemon_health.py:102` `def __init__(self, interval, health_file)`
- `DaemonHealth.error_count` (method) `skills/daemon_health.py:114` `def error_count(self)`
- `DaemonHealth.error_count` (method) `skills/daemon_health.py:119` `def error_count(self, value)`
- `DaemonHealth.phase` (method) `skills/daemon_health.py:124` `def phase(self)`
- `DaemonHealth.phase` (method) `skills/daemon_health.py:129` `def phase(self, value)`
- `DaemonHealth.start` (method) `skills/daemon_health.py:155` `def start(self)` -- Launch the heartbeat thread.
- `DaemonHealth.stop` (method) `skills/daemon_health.py:164` `def stop(self)` -- Stop the heartbeat thread.
- `DaemonHealth.record_error` (method) `skills/daemon_health.py:175` `def record_error(self)` -- Increment the error counter.
- `DaemonHealth.set_phase` (method) `skills/daemon_health.py:180` `def set_phase(self, phase)` -- Update the current daemon phase.
- `DaemonHealth.increment_cycles` (method) `skills/daemon_health.py:185` `def increment_cycles(self)` -- Increment the completed cycles counter.

## skills/heartbeat.py
Depends on: `modules/event_engine.py`, `modules/session_state.py`, `modules/timeline_narrator.py`
- `write_pid` (function) `skills/heartbeat.py:53` `def write_pid()`
- `clear_pid` (function) `skills/heartbeat.py:57` `def clear_pid()`
- `is_running` (function) `skills/heartbeat.py:62` `def is_running()` -- Return (is_running, pid).
- `run_loop` (function) `skills/heartbeat.py:74` `def run_loop(interval, once)`
- `main` (function) `skills/heartbeat.py:127` `def main()`

## skills/hermes-lazyown/claudemd_rules.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `RuleSetBuilder.__init__` (method) `skills/hermes-lazyown/claudemd_rules.py:24` `def __init__(self)`
- `RuleSetBuilder.with_phase` (method) `skills/hermes-lazyown/claudemd_rules.py:31` `def with_phase(self, phase)` -- Set the current engagement phase.
- `RuleSetBuilder.with_target` (method) `skills/hermes-lazyown/claudemd_rules.py:36` `def with_target(self, rhost)` -- Set the active target IP.
- `RuleSetBuilder.with_services` (method) `skills/hermes-lazyown/claudemd_rules.py:41` `def with_services(self, services)` -- Set discovered services (e.g., ['http:80', 'smb:445']).
- `RuleSetBuilder.with_creds` (method) `skills/hermes-lazyown/claudemd_rules.py:46` `def with_creds(self, found)` -- Set whether credentials have been discovered.
- `RuleSetBuilder.with_hermes` (method) `skills/hermes-lazyown/claudemd_rules.py:51` `def with_hermes(self, is_hermes)` -- Set whether running inside a Hermes session.
- `RuleSetBuilder.build` (method) `skills/hermes-lazyown/claudemd_rules.py:56` `def build(self)` -- Build and return the complete rule set markdown.
- `generate_rules` (function) `skills/hermes-lazyown/claudemd_rules.py:185` `def generate_rules(phase, rhost, services, creds_found, is_hermes)` -- Convenience function: build a rule set from parameters.

## skills/hermes-lazyown/config_bridge.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `ConfigBridge.__init__` (method) `skills/hermes-lazyown/config_bridge.py:35` `def __init__(self, payload_path)`
- `ConfigBridge.get` (method) `skills/hermes-lazyown/config_bridge.py:42` `def get(self, key, default)` -- Return the value for *key*, or *default* if not found anywhere.
- `ConfigBridge.get_required` (method) `skills/hermes-lazyown/config_bridge.py:46` `def get_required(self, key)` -- Return the value for *key*, raising ConfigBridgeError if missing.
- `ConfigBridge.get_str` (method) `skills/hermes-lazyown/config_bridge.py:53` `def get_str(self, key, default)` -- Return the string value for *key*.
- `ConfigBridge.get_int` (method) `skills/hermes-lazyown/config_bridge.py:58` `def get_int(self, key, default)` -- Return the integer value for *key*.
- `ConfigBridge.get_bool` (method) `skills/hermes-lazyown/config_bridge.py:66` `def get_bool(self, key, default)` -- Return the boolean value for *key*.
- `ConfigBridge.refresh` (method) `skills/hermes-lazyown/config_bridge.py:75` `def refresh(self)` -- Invalidate all caches so the next read reloads from disk.
- `ConfigBridge.active_target` (method) `skills/hermes-lazyown/config_bridge.py:80` `def active_target(self)` -- Return a dict with the minimal target context (rhost, domain, os_id).
- `ConfigBridge.attacker_context` (method) `skills/hermes-lazyown/config_bridge.py:90` `def attacker_context(self)` -- Return a dict with the attacker context (lhost, lport, etc.).
- `ConfigBridge.is_hermes_session` (method) `skills/hermes-lazyown/config_bridge.py:99` `def is_hermes_session(self)` -- Return True if running inside a Hermes agent session.

## skills/hermes-lazyown/constants.py
Depends on: `modules/killchain.py`
Imported by: `skills/hermes-lazyown/claudemd_rules.py`, `skills/hermes-lazyown/config_bridge.py`, `skills/hermes-lazyown/executor.py`, `skills/hermes-lazyown/hermes_sync.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/hermes-lazyown/output_compactor.py`
- `Paths.lazyown_dir` (method) `skills/hermes-lazyown/constants.py:106` `def lazyown_dir()` -- Return the LazyOwn project root directory.
- `Paths.payload_file` (method) `skills/hermes-lazyown/constants.py:115` `def payload_file()` -- Return the path to payload.json.
- `Paths.sessions_dir` (method) `skills/hermes-lazyown/constants.py:120` `def sessions_dir()` -- Return the path to the sessions directory.
- `Paths.scan_file` (method) `skills/hermes-lazyown/constants.py:125` `def scan_file(rhost)` -- Return the expected nmap scan file for a target.
- `Paths.vulns_file` (method) `skills/hermes-lazyown/constants.py:130` `def vulns_file(rhost)` -- Return the expected vulnerability scan file for a target.
- `Paths.world_model_file` (method) `skills/hermes-lazyown/constants.py:135` `def world_model_file()` -- Return the path to world_model.json.
- `Paths.objectives_file` (method) `skills/hermes-lazyown/constants.py:140` `def objectives_file()` -- Return the path to objectives.jsonl.
- `Paths.tasks_file` (method) `skills/hermes-lazyown/constants.py:145` `def tasks_file()` -- Return the path to tasks.json.
- `Paths.soul_file` (method) `skills/hermes-lazyown/constants.py:150` `def soul_file()` -- Return the path to soul.md.
- `Paths.claude_md_file` (method) `skills/hermes-lazyown/constants.py:155` `def claude_md_file()` -- Return the path to CLAUDE.md.

## skills/hermes-lazyown/executor.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `ExecutionResult.__init__` (method) `skills/hermes-lazyown/executor.py:24` `def __init__(self, stdout, stderr, returncode, timed_out, duration_ms)`
- `ExecutionResult.combined` (method) `skills/hermes-lazyown/executor.py:39` `def combined(self)` -- Return stdout and stderr combined.
- `ExecutionResult.success` (method) `skills/hermes-lazyown/executor.py:47` `def success(self)` -- Return True if the command exited cleanly and did not time out.
- `LazyOwnExecutor.__init__` (method) `skills/hermes-lazyown/executor.py:66` `def __init__(self, lazyown_dir, timeout)`
- `LazyOwnExecutor.execute` (method) `skills/hermes-lazyown/executor.py:77` `def execute(self, command, timeout)` -- Execute a single LazyOwn command string.
- `LazyOwnExecutor.execute_batch` (method) `skills/hermes-lazyown/executor.py:98` `def execute_batch(self, commands, timeout)` -- Execute multiple commands in a single LazyOwn session.

## skills/hermes-lazyown/hermes_sync.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `CheckpointSerializer.__init__` (method) `skills/hermes-lazyown/hermes_sync.py:33` `def __init__(self, sessions_dir)`
- `CheckpointSerializer.write` (method) `skills/hermes-lazyown/hermes_sync.py:37` `def write(self, state)` -- Write a checkpoint to disk.
- `CheckpointSerializer.read` (method) `skills/hermes-lazyown/hermes_sync.py:49` `def read(self)` -- Read the latest checkpoint, or None if absent / stale.
- `CheckpointSerializer.clear` (method) `skills/hermes-lazyown/hermes_sync.py:64` `def clear(self)` -- Remove the checkpoint file.
- `ObjectiveTodoSync.__init__` (method) `skills/hermes-lazyown/hermes_sync.py:82` `def __init__(self, objectives_path)`
- `ObjectiveTodoSync.pending_objectives` (method) `skills/hermes-lazyown/hermes_sync.py:85` `def pending_objectives(self)` -- Return all pending objectives from objectives.jsonl.
- `ObjectiveTodoSync.mark_done` (method) `skills/hermes-lazyown/hermes_sync.py:106` `def mark_done(self, objective_text)` -- Mark an objective as done by appending a completion record.
- `ObjectiveTodoSync.inject_objective` (method) `skills/hermes-lazyown/hermes_sync.py:127` `def inject_objective(self, text, priority, notes)` -- Inject a new objective into the LazyOwn queue.
- `DelegationPlanner.plan_for_service` (method) `skills/hermes-lazyown/hermes_sync.py:154` `def plan_for_service(self, service, port, rhost)` -- Return a list of delegation task descriptors for a discovered service.
- `DelegationPlanner.plan_for_credential` (method) `skills/hermes-lazyown/hermes_sync.py:233` `def plan_for_credential(self, cred_type, value, rhost)` -- Return delegation tasks triggered by a newly found credential.

## skills/hermes-lazyown/mcp_server.py
Depends on: `modules/backdoor/server.c`, `skills/hermes-lazyown/claudemd_rules.py`, `skills/hermes-lazyown/config_bridge.py`, `skills/hermes-lazyown/constants.py`, `skills/hermes-lazyown/executor.py`, `skills/hermes-lazyown/hermes_sync.py`, `skills/hermes-lazyown/output_compactor.py`
- `list_tools` (function) `skills/hermes-lazyown/mcp_server.py:329` `def list_tools()`
- `call_tool` (function) `skills/hermes-lazyown/mcp_server.py:334` `def call_tool(name, arguments)` -- Dispatch incoming tool calls to the appropriate handler.
- `main` (function) `skills/hermes-lazyown/mcp_server.py:751` `def main()`

## skills/hermes-lazyown/output_compactor.py
Depends on: `skills/hermes-lazyown/constants.py`
Imported by: `skills/hermes-lazyown/mcp_server.py`
- `CompactionResult.__init__` (method) `skills/hermes-lazyown/output_compactor.py:20` `def __init__(self, compacted, original_lines, compacted_lines)`
- `CompactionResult.reduction_ratio` (method) `skills/hermes-lazyown/output_compactor.py:26` `def reduction_ratio(self)` -- Return the ratio of lines removed (0.0 to 1.0).
- `CompactionStrategy.compact` (method) `skills/hermes-lazyown/output_compactor.py:40` `def compact(self, raw_output, tool_name)` -- Compact *raw_output* and return a CompactionResult.
- `ReconCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:55` `def compact(self, raw_output, tool_name)`
- `EnumCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:93` `def compact(self, raw_output, tool_name)`
- `ExploitCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:124` `def compact(self, raw_output, tool_name)`
- `PrivescCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:151` `def compact(self, raw_output, tool_name)`
- `DefaultCompaction.__init__` (method) `skills/hermes-lazyown/output_compactor.py:165` `def __init__(self, max_lines)`
- `DefaultCompaction.compact` (method) `skills/hermes-lazyown/output_compactor.py:168` `def compact(self, raw_output, tool_name)`
- `OutputCompactor.__init__` (method) `skills/hermes-lazyown/output_compactor.py:196` `def __init__(self, default_max_lines)`
- `OutputCompactor.compact` (method) `skills/hermes-lazyown/output_compactor.py:200` `def compact(self, raw_output, phase, tool_name)` -- Compact *raw_output* according to *phase*.

## skills/hive_mind.py
Depends on: `core/logging.py`, `modules/logging_config.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_llm.py`, `skills/lazyown_parquet_db.py`
Imported by: `modules/loop_ai_bridge.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`, `skills/swan_agent.py`, `skills/tests/test_hive_mind.py`, `skills/unified_orchestrator.py`
- `IReadableMemory.recall` (method) `skills/hive_mind.py:149` `def recall(self, query, top_k)` -- Return top_k items matching query.
- `IWritableMemory.store` (method) `skills/hive_mind.py:157` `def store(self, content)` -- Persist content and return an opaque event_id.
- `ICommandRunner.run` (method) `skills/hive_mind.py:175` `def run(self, command, timeout)` -- Execute command within timeout seconds and return text output.
- `ICommandRunner.name` (method) `skills/hive_mind.py:180` `def name(self)` -- Human-readable identifier for this runner.
- `EpisodicStore.__init__` (method) `skills/hive_mind.py:215` `def __init__(self, db_path)`
- `EpisodicStore.store` (method) `skills/hive_mind.py:235` `def store(self, content, agent_id, role, event_type, meta, session_tag)` -- Insert a row into hive_events and return event_id.
- `EpisodicStore.recall` (method) `skills/hive_mind.py:274` `def recall(self, query, top_k, role, event_type)` -- Keyword search via FTS5.
- `EpisodicStore.stats` (method) `skills/hive_mind.py:322` `def stats(self)` -- Return row counts for status reporting.
- `EpisodicStore.forget` (method) `skills/hive_mind.py:329` `def forget(self, older_than_hours, topic)` -- Delete old or topic-matching rows.
- `SemanticStore.__init__` (method) `skills/hive_mind.py:358` `def __init__(self, chroma_dir, episodic_fallback)`
- `SemanticStore.available` (method) `skills/hive_mind.py:380` `def available(self)` -- True when ChromaDB is operational.
- `SemanticStore.store` (method) `skills/hive_mind.py:386` `def store(self, content, agent_id, role, event_type, meta, session_tag, event_id)` -- Add a document to ChromaDB.
- `SemanticStore.recall` (method) `skills/hive_mind.py:434` `def recall(self, query, top_k, where)` -- Vector similarity search.
- `SemanticStore.count` (method) `skills/hive_mind.py:477` `def count(self)` -- Return number of vectors stored.
- `LongtermStore.store` (method) `skills/hive_mind.py:515` `def store(self, content)` -- Parquet store is read-only from here.
- `LongtermStore.recall` (method) `skills/hive_mind.py:519` `def recall(self, query, top_k)` -- Keyword search across Parquet knowledge files.
- `build_default_hive_memory` (function) `skills/hive_mind.py:558` `def build_default_hive_memory(db_path)` -- Factory that creates HiveMemory with the default three-layer backend.
- `HiveMemory.__init__` (method) `skills/hive_mind.py:582` `def __init__(self, stores, episodic, semantic, longterm)`
- `HiveMemory.store` (method) `skills/hive_mind.py:596` `def store(self, content, agent_id, role, event_type, meta, session_tag)` -- Store content in all writable layers.
- `HiveMemory.recall_episodic` (method) `skills/hive_mind.py:633` `def recall_episodic(self, query, top_k, role, event_type)` -- Keyword search across hive episodic memory.
- `HiveMemory.recall_semantic` (method) `skills/hive_mind.py:647` `def recall_semantic(self, query, top_k, where)` -- Vector similarity search in ChromaDB.
- `HiveMemory.recall_longterm` (method) `skills/hive_mind.py:660` `def recall_longterm(self, query, top_k)` -- Keyword search across Parquet knowledge files.
- `HiveMemory.recall` (method) `skills/hive_mind.py:668` `def recall(self, query, top_k)` -- Unified recall: semantic (ChromaDB) + episodic (SQLite) + longterm (Parquet).
- `HiveMemory.stats` (method) `skills/hive_mind.py:694` `def stats(self)` -- Return combined statistics from all layers.
- `HiveMemory.forget` (method) `skills/hive_mind.py:704` `def forget(self, older_than_hours, topic)` -- Prune old or topic-matched entries.
- `HiveBus.__init__` (method) `skills/hive_mind.py:736` `def __init__(self)`
- `HiveBus.publish` (method) `skills/hive_mind.py:740` `def publish(self, msg)` -- Deliver msg to recipient mailbox (and to "*" broadcast).
- `HiveBus.receive` (method) `skills/hive_mind.py:746` `def receive(self, agent_id, max_msgs)` -- Drain mailbox for agent_id (includes broadcast).
- `HiveBus.ack_broadcast` (method) `skills/hive_mind.py:754` `def ack_broadcast(self, agent_id, msg_id)` -- Mark a broadcast message as seen by agent_id (minimal bus — no-op).
- `HiveBus.pending_count` (method) `skills/hive_mind.py:758` `def pending_count(self, agent_id)` -- Count messages waiting for agent_id.
- `ConsensusProtocol.__init__` (method) `skills/hive_mind.py:943` `def __init__(self, risk_assessor)`
- `ConsensusProtocol.evaluate` (method) `skills/hive_mind.py:946` `def evaluate(self, role, goal)` -- Run the consensus vote for the given (role, goal) pair.
- `DroneAgent.__init__` (method) `skills/hive_mind.py:1091` `def __init__(self, drone_id, role, goal, backend, memory, bus, max_iterations, api_key, model, runner, on_state_change)`
- `DroneAgent.start` (method) `skills/hive_mind.py:1128` `def start(self)` -- Spawn the drone thread.
- `DroneAgent.join` (method) `skills/hive_mind.py:1137` `def join(self, timeout)` -- Block until the drone thread finishes.
- `QueenBrain.__init__` (method) `skills/hive_mind.py:1301` `def __init__(self, memory, bus, pool, consensus)`
- `QueenBrain.plan` (method) `skills/hive_mind.py:1313` `def plan(self, goal, n_drones)` -- Decompose a high-level goal into per-drone task specs.
- `QueenBrain.dispatch` (method) `skills/hive_mind.py:1332` `def dispatch(self, tasks, backend, api_key, max_iterations)` -- Spawn one drone per task in parallel.
- `QueenBrain.plan_and_dispatch` (method) `skills/hive_mind.py:1405` `def plan_and_dispatch(self, goal, n_drones, backend, api_key, max_iterations)` -- Convenience: plan + dispatch in one call.
- `QueenBrain.collect` (method) `skills/hive_mind.py:1417` `def collect(self, drone_ids, timeout, poll_interval)` -- Wait for all drones to finish (up to timeout seconds).
- `QueenBrain.synthesize` (method) `skills/hive_mind.py:1447` `def synthesize(self, drone_ids, original_goal)` -- Read hive memory results for these drones and produce a synthesis summary.
- `QueenBrain.read_bus` (method) `skills/hive_mind.py:1471` `def read_bus(self)` -- Drain queen's mailbox from drone result messages.
- `DroneStateStore.__init__` (method) `skills/hive_mind.py:1513` `def __init__(self, db_path)`
- `DroneStateStore.upsert` (method) `skills/hive_mind.py:1523` `def upsert(self, state)` -- Insert or replace a drone state record.
- `DroneStateStore.load_all` (method) `skills/hive_mind.py:1553` `def load_all(self, limit)` -- Load all persisted drone states ordered by most recently updated.
- `DroneStateStore.mark_interrupted` (method) `skills/hive_mind.py:1588` `def mark_interrupted(self)` -- Called on daemon startup: any drone that was queued/running when the process died is now in an unknown state.
- `DroneStateStore.load_interrupted` (method) `skills/hive_mind.py:1609` `def load_interrupted(self)` -- Return all drones currently in 'interrupted' state.
- `DroneStateStore.delete_older_than` (method) `skills/hive_mind.py:1643` `def delete_older_than(self, days)` -- Prune records older than N days.
- `DronePool.__init__` (method) `skills/hive_mind.py:1673` `def __init__(self, memory, bus, state_store)`
- `DronePool.recover_from_store` (method) `skills/hive_mind.py:1687` `def recover_from_store(self)` -- Load persisted drone states from a previous run.
- `DronePool.spawn` (method) `skills/hive_mind.py:1708` `def spawn(self, role, goal, backend, api_key, model, max_iterations, runner)` -- Create and start a DroneAgent.
- `DronePool.requeue_interrupted` (method) `skills/hive_mind.py:1741` `def requeue_interrupted(self, backend, api_key, max_iterations)` -- Re-spawn all drones previously marked 'interrupted'.
- `DronePool.get_state` (method) `skills/hive_mind.py:1767` `def get_state(self, drone_id)` -- Return the current state snapshot for a drone, or None if unknown.
- `DronePool.list_all` (method) `skills/hive_mind.py:1776` `def list_all(self, limit)` -- Return a sorted list of drone summary dicts (most recent first).
- `DronePool.active_count` (method) `skills/hive_mind.py:1801` `def active_count(self)` -- Return number of live drones currently in queued or running state.
- `HiveMind.__init__` (method) `skills/hive_mind.py:1818` `def __init__(self)`
- `HiveMind.spawn` (method) `skills/hive_mind.py:1829` `def spawn(self, goal, role, backend, api_key, max_iterations)` -- Spawn a single drone.
- `HiveMind.spawn_hive` (method) `skills/hive_mind.py:1846` `def spawn_hive(self, goal, n_drones, backend, api_key, max_iterations)` -- Queen plans and dispatches multiple drones in parallel.
- `HiveMind.status` (method) `skills/hive_mind.py:1863` `def status(self)` -- Return hive-wide status dict including historical drones from previous runs.
- `HiveMind.recall` (method) `skills/hive_mind.py:1878` `def recall(self, query, top_k)` -- Unified recall from all memory layers.
- `HiveMind.drone_result` (method) `skills/hive_mind.py:1882` `def drone_result(self, drone_id)` -- Return result dict for a specific drone.
- `HiveMind.collect_and_synthesize` (method) `skills/hive_mind.py:1896` `def collect_and_synthesize(self, drone_ids, goal)` -- Synthesize results from multiple drones.
- `HiveMind.forget` (method) `skills/hive_mind.py:1900` `def forget(self, older_than_hours, topic)` -- Prune hive memory.
- `get_hive` (function) `skills/hive_mind.py:1911` `def get_hive()` -- Return the process-wide HiveMind singleton, creating it if necessary.
- `mcp_hive_spawn` (function) `skills/hive_mind.py:1926` `def mcp_hive_spawn(goal, role, n_drones, backend, max_iterations, api_key)` -- Spawn one or more hive drones for a goal.
- `mcp_hive_status` (function) `skills/hive_mind.py:1976` `def mcp_hive_status()` -- Return full hive status: active drones, memory stats, queen mailbox.
- `mcp_hive_recall` (function) `skills/hive_mind.py:1981` `def mcp_hive_recall(query, top_k)` -- Semantic + episodic + longterm recall from hive memory.
- `mcp_hive_plan` (function) `skills/hive_mind.py:1995` `def mcp_hive_plan(goal, n_drones)` -- Queen generates task decomposition without spawning drones.
- `mcp_hive_result` (function) `skills/hive_mind.py:2004` `def mcp_hive_result(drone_id)` -- Get result from a specific drone.
- `mcp_hive_collect` (function) `skills/hive_mind.py:2010` `def mcp_hive_collect(drone_ids_csv, goal)` -- Wait for drones to finish and return synthesized result. drone_ids_csv: comma-separated drone IDs.
- `mcp_hive_forget` (function) `skills/hive_mind.py:2021` `def mcp_hive_forget(older_than_hours, topic)` -- Prune hive memory.
- `mcp_hive_recover` (function) `skills/hive_mind.py:2027` `def mcp_hive_recover(backend, api_key, max_iterations)` -- Re-queue all drones that were interrupted by a previous process crash/restart.

## skills/lazyown_automapper.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_mcp.py`
- `AutoMapper.__init__` (method) `skills/lazyown_automapper.py:341` `def __init__(self, lazyown_dir)`
- `AutoMapper.rescan` (method) `skills/lazyown_automapper.py:364` `def rescan(self)` -- Force a rescan of all source directories.
- `AutoMapper.mcp_tools` (method) `skills/lazyown_automapper.py:368` `def mcp_tools(self)` -- Return list of mcp types.Tool objects for all discovered extensions.
- `AutoMapper.dispatch` (method) `skills/lazyown_automapper.py:389` `def dispatch(self, name, arguments, config, run_command_fn)` -- Execute a dynamic tool.
- `AutoMapper.update_skills_md` (method) `skills/lazyown_automapper.py:524` `def update_skills_md(self, skills_md_path)` -- Append / replace the auto-discovered section in skills/lazyown.md.
- `AutoMapper.stats` (method) `skills/lazyown_automapper.py:571` `def stats(self)`
- `AutoMapper.list_specs` (method) `skills/lazyown_automapper.py:581` `def list_specs(self)` -- Return raw spec dicts (useful for debugging / reporting).

## skills/lazyown_campaign.py
Depends on: `core/logging.py`, `modules/lesson_ingestor.py`, `modules/logging_config.py`
Imported by: `skills/lazyown_mcp.py`
- `is_ip_in_scope` (function) `skills/lazyown_campaign.py:64` `def is_ip_in_scope(ip, scope)` -- Return True if *ip* belongs to any entry in *scope*.
- `Campaign.is_active` (method) `skills/lazyown_campaign.py:148` `def is_active(self)` -- Return True when the campaign has not been completed yet.
- `Campaign.to_dict` (method) `skills/lazyown_campaign.py:152` `def to_dict(self)` -- Serialise to a plain dict suitable for JSON persistence.
- `Campaign.from_dict` (method) `skills/lazyown_campaign.py:157` `def from_dict(cls, data)` -- Deserialise from a dict loaded out of JSON.
- `LessonLearned.to_dict` (method) `skills/lazyown_campaign.py:189` `def to_dict(self)`
- `EpisodeReflectionEngine.__init__` (method) `skills/lazyown_campaign.py:256` `def __init__(self, hive_memory)` -- Parameters hive_memory: Optional HiveMemory instance for semantic storage.
- `EpisodeReflectionEngine.reflect` (method) `skills/lazyown_campaign.py:268` `def reflect(self, campaign)` -- Extract lessons from *campaign* and persist them.
- `CampaignStore.__init__` (method) `skills/lazyown_campaign.py:382` `def __init__(self, campaign_file)`
- `CampaignStore.load` (method) `skills/lazyown_campaign.py:395` `def load(self)` -- Load the current campaign from disk.
- `CampaignStore.create` (method) `skills/lazyown_campaign.py:414` `def create(self, name, scope, notes)` -- Create and persist a brand-new campaign.
- `CampaignStore.complete` (method) `skills/lazyown_campaign.py:445` `def complete(self, notes, run_reflection, hive_memory)` -- Mark the active campaign as completed and optionally run reflection.
- `CampaignStore.update_phase` (method) `skills/lazyown_campaign.py:500` `def update_phase(self, host, phase)` -- Set (or update) the attack phase for *host*.
- `CampaignStore.add_milestone` (method) `skills/lazyown_campaign.py:516` `def add_milestone(self, host, milestone_type, notes)` -- Record a milestone achievement for *host*.
- `CampaignStore.add_to_scope` (method) `skills/lazyown_campaign.py:540` `def add_to_scope(self, ip_or_cidr)` -- Append *ip_or_cidr* to the campaign scope (idempotent).
- `CampaignStore.in_scope` (method) `skills/lazyown_campaign.py:559` `def in_scope(self, ip)` -- Return True if *ip* falls within the campaign scope.
- `CampaignStore.summary` (method) `skills/lazyown_campaign.py:566` `def summary(self)` -- Return a human-readable multi-line summary of the campaign.
- `main` (function) `skills/lazyown_campaign.py:667` `def main(argv)`

## skills/lazyown_claudemd.py
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `ClaudeMdLoader.__init__` (method) `skills/lazyown_claudemd.py:32` `def __init__(self, cwd)`
- `ClaudeMdLoader.load` (method) `skills/lazyown_claudemd.py:35` `def load(self)` -- Return merged instructions string from all applicable levels.
- `ClaudeMdLoader.list_files` (method) `skills/lazyown_claudemd.py:90` `def list_files(self)` -- Return metadata for all CLAUDE.md files that exist.
- `ClaudeMdLoader.create_user_file` (method) `skills/lazyown_claudemd.py:115` `def create_user_file(self, content)` -- Create/overwrite ~/.lazyown/CLAUDE.md.
- `ClaudeMdLoader.create_project_file` (method) `skills/lazyown_claudemd.py:121` `def create_project_file(self, content, local)` -- Create CLAUDE.md (or CLAUDE.local.md) in cwd.
- `ClaudeMdLoader.add_rule` (method) `skills/lazyown_claudemd.py:127` `def add_rule(self, rule_name, content)` -- Add a named rule file to .lazyown/rules/.
- `ClaudeMdLoader.status_text` (method) `skills/lazyown_claudemd.py:135` `def status_text(self)`

## skills/lazyown_context.py
Imported by: `skills/lazyown_mcp.py`, `skills/lazyown_session.py`, `skills/tests/test_harness_e2e.py`
- `CompactionResult.summary` (method) `skills/lazyown_context.py:57` `def summary(self)`
- `ContextCompactor.__init__` (method) `skills/lazyown_context.py:72` `def __init__(self, budget_override, snip_threshold, collapse_threshold)`
- `ContextCompactor.apply_budget` (method) `skills/lazyown_context.py:84` `def apply_budget(self, content, tool_name)` -- Hard-cap output.
- `ContextCompactor.snip` (method) `skills/lazyown_context.py:99` `def snip(self, content)` -- Remove duplicate consecutive lines (log noise).
- `ContextCompactor.microcompact` (method) `skills/lazyown_context.py:120` `def microcompact(self, content)` -- Strip known low-signal patterns.
- `ContextCompactor.collapse` (method) `skills/lazyown_context.py:136` `def collapse(self, content, tool_name)` -- Replace repetitive sections with a structural summary.
- `ContextCompactor.auto_compact_session` (method) `skills/lazyown_context.py:159` `def auto_compact_session(entries)` -- Template-based session summary when full pipeline is insufficient. entries: list of {"type": str, "data": dict} from...
- `ContextCompactor.compact` (method) `skills/lazyown_context.py:203` `def compact(self, content, tool_name)` -- Apply all applicable layers in order.
- `compact_output` (function) `skills/lazyown_context.py:237` `def compact_output(content, tool_name)` -- Convenience wrapper: compact and return string.

## skills/lazyown_daemon.py
Depends on: `core/logging.py`, `modules/event_engine.py`, `modules/logging_config.py`, `modules/session_state.py`, `modules/timeline_narrator.py`, `skills/sessions_watcher.py`
- `process_new_rows` (function) `skills/lazyown_daemon.py:108` `def process_new_rows()`
- `file_watcher_loop` (function) `skills/lazyown_daemon.py:150` `def file_watcher_loop(queue)` -- Watch sessions/ for new/modified files and dispatch handlers.
- `_Handler.on_created` (method) `skills/lazyown_daemon.py:201` `def on_created(self, event)`
- `_Handler.on_modified` (method) `skills/lazyown_daemon.py:205` `def on_modified(self, event)`
- `file_event_consumer` (function) `skills/lazyown_daemon.py:223` `def file_event_consumer(queue)` -- Consume FILE events from the queue and call _dispatch in executor.
- `event_engine_loop` (function) `skills/lazyown_daemon.py:240` `def event_engine_loop()` -- Tail CSV, match rules, emit events — every ENGINE_INTERVAL_S seconds.
- `heartbeat_loop` (function) `skills/lazyown_daemon.py:280` `def heartbeat_loop()` -- Emit HEARTBEAT event and write daemon_status.json every 30 seconds.
- `toposwarm_keepalive_loop` (function) `skills/lazyown_daemon.py:332` `def toposwarm_keepalive_loop()` -- Keeps the TopoSwarm MCP server alive as a subprocess.
- `cmd_run` (function) `skills/lazyown_daemon.py:453` `def cmd_run()` -- Run in foreground.
- `cmd_start` (function) `skills/lazyown_daemon.py:462` `def cmd_start()` -- Fork, detach, and run in background.
- `cmd_stop` (function) `skills/lazyown_daemon.py:495` `def cmd_stop()` -- Send SIGTERM to the running daemon.
- `cmd_status` (function) `skills/lazyown_daemon.py:513` `def cmd_status()` -- Print status from daemon_status.json.


Next: [API_p20.md](API_p20.md)
