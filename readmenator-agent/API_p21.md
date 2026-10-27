# API (page 21 of 24)
Previous: [API_p20.md](API_p20.md)

## skills/lazyown_policy.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/detection_oracle.py`, `modules/logging_config.py`
Imported by: `cli/recommendation_signals.py`, `modules/unified_dashboard.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/swan_agent.py`, `tests/test_engage_orchestrator.py`, `tests/test_moe_rl_swan.py`, `tests/test_scope_bound_auto_gate.py`
- `Config.default` (method) `skills/lazyown_policy.py:82` `def default(cls)` -- Construct configuration anchored to this file's repository root.
- `Config.ollama_url` (method) `skills/lazyown_policy.py:123` `def ollama_url(self)` -- Full URL for the Ollama generate endpoint.
- `infer_category` (function) `skills/lazyown_policy.py:267` `def infer_category(command, args)` -- Return the ActionCategory best matching the command and its arguments.
- `ClassificationResult.unknown` (method) `skills/lazyown_policy.py:317` `def unknown(cls, tier)` -- Produce a result indicating the tier could not classify.
- `EpisodeRecord.to_dict` (method) `skills/lazyown_policy.py:357` `def to_dict(self)` -- Serialise to a plain dict suitable for JSON encoding.
- `EpisodeRecord.from_dict` (method) `skills/lazyown_policy.py:362` `def from_dict(cls, d)` -- Deserialise from a dict produced by to_dict.
- `IOutputClassifier.classify` (method) `skills/lazyown_policy.py:376` `def classify(self, command, args, output, exit_code)` -- Classify the outcome of one command execution.
- `ExitCodeClassifier.classify` (method) `skills/lazyown_policy.py:401` `def classify(self, command, args, output, exit_code)` -- Return a low-confidence result based solely on the exit code.
- `HeuristicClassifier.classify` (method) `skills/lazyown_policy.py:444` `def classify(self, command, args, output, exit_code)` -- Scan output for known success or failure signatures.
- `_OllamaClassifierBase.__init__` (method) `skills/lazyown_policy.py:496` `def __init__(self, cfg, model, tier_name)`
- `_OllamaClassifierBase.classify` (method) `skills/lazyown_policy.py:570` `def classify(self, command, args, output, exit_code)` -- Send the command context to Ollama and parse the JSON reply.
- `OllamaSmallClassifier.__init__` (method) `skills/lazyown_policy.py:591` `def __init__(self, cfg)`
- `OllamaLargeClassifier.__init__` (method) `skills/lazyown_policy.py:601` `def __init__(self, cfg)`
- `UserInteractiveClassifier.classify` (method) `skills/lazyown_policy.py:616` `def classify(self, command, args, output, exit_code)` -- Prompt the operator and return their authoritative verdict.
- `CascadeClassifier.__init__` (method) `skills/lazyown_policy.py:666` `def __init__(self, cfg, interactive)`
- `CascadeClassifier.classify` (method) `skills/lazyown_policy.py:677` `def classify(self, command, args, output, exit_code)` -- Return the first sufficiently confident result, or the best available.
- `DetectionRiskAssessor.__init__` (method) `skills/lazyown_policy.py:715` `def __init__(self)`
- `DetectionRiskAssessor.assess_probability` (method) `skills/lazyown_policy.py:733` `def assess_probability(self, command, args, category)` -- Return detection probability in [0.0, 1.0].
- `DetectionRiskAssessor.is_high_risk` (method) `skills/lazyown_policy.py:746` `def is_high_risk(self, command, args, category)` -- Return True when detection probability meets or exceeds the threshold.
- `RewardCalculator.__init__` (method) `skills/lazyown_policy.py:773` `def __init__(self, cfg, risk_assessor)`
- `RewardCalculator.calculate` (method) `skills/lazyown_policy.py:783` `def calculate(self, category, outcome)` -- Return the reward integer for the given (category, outcome) pair.
- `RewardCalculator.calculate_with_detection` (method) `skills/lazyown_policy.py:798` `def calculate_with_detection(self, category, outcome, command, args)` -- Return (reward, detection_probability) for the given execution.
- `CSVSessionReader.__init__` (method) `skills/lazyown_policy.py:850` `def __init__(self, cfg)`
- `CSVSessionReader.read` (method) `skills/lazyown_policy.py:855` `def read(self)` -- Parse the CSV and return all classifiable rows as StepRecord instances.
- `IEpisodeStore.append_step` (method) `skills/lazyown_policy.py:903` `def append_step(self, step)` -- Add a step to the episode for its target, creating the episode if needed.
- `IEpisodeStore.load_all` (method) `skills/lazyown_policy.py:907` `def load_all(self)` -- Load every stored episode.
- `IEpisodeStore.get_episode` (method) `skills/lazyown_policy.py:911` `def get_episode(self, target)` -- Return the episode for the given target, or None.
- `JSONLEpisodeStore.__init__` (method) `skills/lazyown_policy.py:923` `def __init__(self, cfg)`
- `JSONLEpisodeStore.append_step` (method) `skills/lazyown_policy.py:927` `def append_step(self, step)` -- Upsert the step into its target's episode and persist.
- `JSONLEpisodeStore.load_all` (method) `skills/lazyown_policy.py:947` `def load_all(self)` -- Deserialise all episodes from the .jsonl file.
- `JSONLEpisodeStore.get_episode` (method) `skills/lazyown_policy.py:963` `def get_episode(self, target)` -- Return the episode for target, or None if not found.
- `TransitionTable.__init__` (method) `skills/lazyown_policy.py:987` `def __init__(self, cfg)`
- `TransitionTable.record` (method) `skills/lazyown_policy.py:993` `def record(self, from_state, to_category, outcome)` -- Increment the counter for the given transition and persist.
- `TransitionTable.query` (method) `skills/lazyown_policy.py:1003` `def query(self, from_state)` -- Return (next_category, success_rate, total_count) tuples for the given from_state, filtered by min_transition_count...
- `PolicyEngine.__init__` (method) `skills/lazyown_policy.py:1107` `def __init__(self, cfg, transitions)`
- `PolicyEngine.recommend` (method) `skills/lazyown_policy.py:1111` `def recommend(self, recent_steps)` -- Return up to top_k dicts with keys: category, reason, confidence, source.
- `SessionClassificationPipeline.__init__` (method) `skills/lazyown_policy.py:1202` `def __init__(self, cfg, interactive)`
- `SessionClassificationPipeline.process` (method) `skills/lazyown_policy.py:1210` `def process(self, target, command, args, output, exit_code, timestamp)` -- Classify, reward, store, and return a StepRecord for the given execution.
- `PolicyAdvisor.__init__` (method) `skills/lazyown_policy.py:1267` `def __init__(self, cfg)`
- `PolicyAdvisor.advise` (method) `skills/lazyown_policy.py:1272` `def advise(self, target)` -- Return the policy engine's recommendations for the given target.
- `PolicyAdvisor.episode_summary` (method) `skills/lazyown_policy.py:1277` `def episode_summary(self, target)` -- Return a high-level summary dict for the target's episode.
- `LazyOwnPolicyIntegration.__init__` (method) `skills/lazyown_policy.py:1302` `def __init__(self, cfg)`
- `LazyOwnPolicyIntegration.on_command_complete` (method) `skills/lazyown_policy.py:1307` `def on_command_complete(self, target, command, args, output, exit_code)` -- Classify a completed command and record it in the episode store.
- `LazyOwnPolicyIntegration.get_recommendations` (method) `skills/lazyown_policy.py:1318` `def get_recommendations(self, target)` -- Return ranked next-action recommendations for the target.
- `ApprovalOutcome.is_approved` (method) `skills/lazyown_policy.py:1365` `def is_approved(self)` -- True when the gate authorised execution.
- `ApprovalOutcome.is_denied` (method) `skills/lazyown_policy.py:1370` `def is_denied(self)` -- True when the gate denied execution.
- `IApprovalSink.announce` (method) `skills/lazyown_policy.py:1384` `def announce(self, request)` -- Publish the request so operators can see and resolve it.
- `IApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1388` `def resolution_for(self, approval_id)` -- Return the latest resolution for the request or None if pending.
- `FileApprovalSink.__init__` (method) `skills/lazyown_policy.py:1400` `def __init__(self, sessions_dir)`
- `FileApprovalSink.path` (method) `skills/lazyown_policy.py:1405` `def path(self)` -- Absolute path of the underlying JSONL file.
- `FileApprovalSink.announce` (method) `skills/lazyown_policy.py:1409` `def announce(self, request)`
- `FileApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1426` `def resolution_for(self, approval_id)`
- `BroadcastApprovalSink.__init__` (method) `skills/lazyown_policy.py:1463` `def __init__(self, narrator, file_sink)`
- `BroadcastApprovalSink.announce` (method) `skills/lazyown_policy.py:1471` `def announce(self, request)`
- `BroadcastApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1499` `def resolution_for(self, approval_id)`
- `StdinApprovalSink.__init__` (method) `skills/lazyown_policy.py:1513` `def __init__(self, stream)`
- `StdinApprovalSink.announce` (method) `skills/lazyown_policy.py:1523` `def announce(self, request)`
- `StdinApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1552` `def resolution_for(self, approval_id)`
- `CompositeApprovalSink.__init__` (method) `skills/lazyown_policy.py:1564` `def __init__(self, sinks)`
- `CompositeApprovalSink.announce` (method) `skills/lazyown_policy.py:1569` `def announce(self, request)`
- `CompositeApprovalSink.resolution_for` (method) `skills/lazyown_policy.py:1576` `def resolution_for(self, approval_id)`
- `ApprovalGate.__init__` (method) `skills/lazyown_policy.py:1634` `def __init__(self, sink, payload_path, poll_interval_s, poll_timeout_s, sleep_fn)`
- `ApprovalGate.request` (method) `skills/lazyown_policy.py:1667` `def request(self, target, phase, command, reason)` -- Return an ApprovalOutcome for the proposed execution.
- `ScopeBoundAutoGate.__init__` (method) `skills/lazyown_policy.py:1850` `def __init__(self, payload_path, in_scope_fn)`
- `ScopeBoundAutoGate.request` (method) `skills/lazyown_policy.py:1866` `def request(self, target, phase, command, reason)` -- Return an ApprovalOutcome without ever prompting a human.
- `HistoryBootstrapper.__init__` (method) `skills/lazyown_policy.py:1928` `def __init__(self, cfg)`
- `HistoryBootstrapper.run` (method) `skills/lazyown_policy.py:1934` `def run(self)` -- Process all CSV rows and return the total number of steps indexed.
- `main` (function) `skills/lazyown_policy.py:2036` `def main()` -- Parse CLI arguments and dispatch to the appropriate command handler.

## skills/lazyown_session.py
Depends on: `skills/lazyown_context.py`
Imported by: `skills/lazyown_mcp.py`, `skills/tests/test_harness_e2e.py`
- `SessionTranscript.__init__` (method) `skills/lazyown_session.py:82` `def __init__(self, sessions_dir, session_id)`
- `SessionTranscript.append` (method) `skills/lazyown_session.py:106` `def append(self, event_type, data)` -- Append a single event.
- `SessionTranscript.get_recent` (method) `skills/lazyown_session.py:143` `def get_recent(self, n)` -- Return the last n events.
- `SessionTranscript.get_all` (method) `skills/lazyown_session.py:161` `def get_all(self)`
- `SessionTranscript.count` (method) `skills/lazyown_session.py:164` `def count(self)`
- `SessionTranscript.maybe_auto_compact` (method) `skills/lazyown_session.py:174` `def maybe_auto_compact(self, threshold)` -- If event count since the last compact_boundary exceeds threshold, generate a template summary of those events and...
- `SessionTranscript.add_compact_boundary` (method) `skills/lazyown_session.py:209` `def add_compact_boundary(self, summary, preserved_uuids)` -- Mark a compaction point.
- `SessionTranscript.fork` (method) `skills/lazyown_session.py:227` `def fork(self, new_id)` -- Create a new transcript forked from this one.
- `SessionTranscript.status_text` (method) `skills/lazyown_session.py:257` `def status_text(self)`
- `get_transcript` (function) `skills/lazyown_session.py:281` `def get_transcript(sessions_dir, session_id)` -- Return the active transcript singleton.
- `reset_transcript` (function) `skills/lazyown_session.py:294` `def reset_transcript(sessions_dir, session_id)` -- Force a new transcript (e.g., after fork or session reset).

## skills/mcp_generated_tools.py
- `get_generated_tool_definitions` (function) `skills/mcp_generated_tools.py:659` `def get_generated_tool_definitions()` -- Return list[types.Tool] entries for all generated tools.
- `register_all_generated_handlers` (function) `skills/mcp_generated_tools.py:684` `def register_all_generated_handlers(register_handler_fn, make_text_fn, run_lazyown_cmd_fn)` -- Register every generated handler via *register_handler_fn*.

## skills/mcp_lazy.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_mcp_lazy.py`
- `ensure_optional` (function) `skills/mcp_lazy.py:18` `def ensure_optional(namespace, flag, loader)` -- Return the cached flag or run ``loader`` once to compute it.

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
