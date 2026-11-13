# API (page 17 of 28)
Previous: [API_p16.md](API_p16.md)

## modules/llm_pool.py
Imported by: `cli/commands/ai.py`, `modules/lazy_loop.py`, `modules/llm_orchestrator.py`, `skills/autonomous_daemon.py`, `tests/conftest.py`, `tests/test_autonomous_ops.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_runner.py`, `tests/test_llm_orchestrator.py`
- `shared_registry` (function) `modules/llm_pool.py:50` `def shared_registry(config)` -- Return the process-wide health registry (LAZY Registry parity).
- `HealthRegistry.__init__` (method) `modules/llm_pool.py:83` `def __init__(self, config)` -- Initialize counters from the persisted breaker state.
- `HealthRegistry.report_success` (method) `modules/llm_pool.py:135` `def report_success(self, member_id)` -- Clear failure state for a member.
- `HealthRegistry.report_failure` (method) `modules/llm_pool.py:143` `def report_failure(self, member_id, error)` -- Record a failure; auth/quota errors trip immediately.
- `HealthRegistry.healthy` (method) `modules/llm_pool.py:163` `def healthy(self, member_id)` -- Return True when a member may serve traffic.
- `LLMPool.__init__` (method) `modules/llm_pool.py:179` `def __init__(self, members, health, config)` -- Order members by descending rank (RR within equal rank).
- `LLMPool.members` (method) `modules/llm_pool.py:192` `def members(self)` -- Return chain members in order.
- `LLMPool.session_key` (method) `modules/llm_pool.py:196` `def session_key(self, conversation_id, role, index)` -- Build a sticky session header (LAZY session_header parity).
- `LLMPool.complete` (method) `modules/llm_pool.py:237` `def complete(self, prompt, max_tokens, session_key, overflow_dir)` -- Complete a prompt with pre-token failover across members.

## modules/llm_prompts.py
Depends on: `modules/colors.py`
Imported by: `cli/commands/ai.py`, `modules/llm_adapter.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_orchestrator.py`, `tests/test_llm_prompts.py`
- `default_project_root` (function) `modules/llm_prompts.py:67` `def default_project_root()` -- Return the repository root that owns the LLM prompt configuration.
- `resolve_model` (function) `modules/llm_prompts.py:76` `def resolve_model(model)` -- Resolve an explicit model or fall back to the randomized Groq model.
- `truncate_message` (function) `modules/llm_prompts.py:95` `def truncate_message(message, max_chars)` -- Truncate a message with an ellipsis marker when it exceeds the limit.
- `LlmPromptConfig.from_defaults` (method) `modules/llm_prompts.py:130` `def from_defaults(cls, project_root)` -- Build a config rooted at the given project root.
- `LlmPromptConfig.knowledge_base_path` (method) `modules/llm_prompts.py:150` `def knowledge_base_path(self, domain)` -- Return the absolute path for a knowledge-base domain file.
- `LlmPromptConfig.load_payload_context` (method) `modules/llm_prompts.py:161` `def load_payload_context(self)` -- Load the operator context keyed by :data:`PAYLOAD_KEY_ORDER`.
- `LlmPromptConfig.load_event_tool_output` (method) `modules/llm_prompts.py:176` `def load_event_tool_output(self, event_name)` -- Load tool output attached to a named event in event_config.json.
- `LlmPromptConfig.load_plan_history` (method) `modules/llm_prompts.py:203` `def load_plan_history(self)` -- Load the session plan history text if present.
- `LlmPromptConfig.load_report_context` (method) `modules/llm_prompts.py:218` `def load_report_context(self)` -- Load the JSON artefacts consumed by the report template.
- `LlmPromptConfig.knowledge_store` (method) `modules/llm_prompts.py:238` `def knowledge_store(self, domain)` -- Build a knowledge store bound to a domain file.
- `LlmPromptConfig.render` (method) `modules/llm_prompts.py:249` `def render(self, template, base_prompt)` -- Render a named template with shared knowledge and context.
- `render_kb_tail` (function) `modules/llm_prompts.py:271` `def render_kb_tail(lines)` -- Join the most recent knowledge lines for embedding into a prompt.
- `KnowledgeStore.__init__` (method) `modules/llm_prompts.py:289` `def __init__(self, path)` -- Initialize a store bound to a single JSON file.
- `KnowledgeStore.load` (method) `modules/llm_prompts.py:297` `def load(self)` -- Load the knowledge-base records from disk.
- `KnowledgeStore.save` (method) `modules/llm_prompts.py:312` `def save(self, records)` -- Persist a full record list to disk, creating parent directories.
- `KnowledgeStore.add` (method) `modules/llm_prompts.py:324` `def add(self, prompt, response)` -- Append a prompt/response record to the knowledge base.
- `KnowledgeStore.relevant` (method) `modules/llm_prompts.py:335` `def relevant(self, prompt, limit)` -- Return knowledge responses whose text shares keywords with the prompt.

## modules/log_tamper.py
Imported by: `cli/commands/opsec_cleanup.py`
- `LogTamper.__init__` (method) `modules/log_tamper.py:105` `def __init__(self, config)`
- `LogTamper.windows_clear_commands` (method) `modules/log_tamper.py:108` `def windows_clear_commands(self)` -- Generate Windows Event Log clearing commands.
- `LogTamper.linux_clear_commands` (method) `modules/log_tamper.py:176` `def linux_clear_commands(self)` -- Generate Linux log clearing commands.
- `LogTamper.macos_clear_commands` (method) `modules/log_tamper.py:243` `def macos_clear_commands(self)` -- Generate macOS log clearing commands.
- `LogTamper.generate_all` (method) `modules/log_tamper.py:295` `def generate_all(self)` -- Generate log tampering commands for all platforms.
- `LogTamper.auditd_disable_commands` (method) `modules/log_tamper.py:307` `def auditd_disable_commands(self)` -- Commands to temporarily disable or reconfigure auditd on Linux.
- `LogTamper.sysmon_disable_commands` (method) `modules/log_tamper.py:341` `def sysmon_disable_commands(self)` -- Commands to disable or degrade Sysmon on Windows.

## modules/logging_config.py
Depends on: `core/logging.py`
Imported by: `lazy_sentinel4.py`, `lazyc2.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/lazyownerweb.py`, `modules/lilsplunky.py`, `modules/vulnbot.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`
- `ColoredFormatter.format` (method) `modules/logging_config.py:39` `def format(self, record)`
- `JsonFormatter.format` (method) `modules/logging_config.py:72` `def format(self, record)`
- `CorrelationFilter.filter` (method) `modules/logging_config.py:94` `def filter(self, record)`
- `ResilientRotatingFileHandler.emit` (method) `modules/logging_config.py:116` `def emit(self, record)` -- Write one record, no-op after the file has become unwritable.
- `ResilientRotatingFileHandler.handleError` (method) `modules/logging_config.py:122` `def handleError(self, record)` -- Suppress the default per-record traceback; notify once via stderr.
- `set_correlation_id` (function) `modules/logging_config.py:134` `def set_correlation_id(cid)` -- Set the correlation ID for the current async/task context.
- `get_correlation_id` (function) `modules/logging_config.py:139` `def get_correlation_id()` -- Return the current correlation ID, or None.
- `clear_correlation_id` (function) `modules/logging_config.py:144` `def clear_correlation_id()` -- Reset the correlation ID for the current context.
- `configure` (function) `modules/logging_config.py:244` `def configure(level, log_dir, console, file, format_console, format_file, max_bytes, backup_count, module_levels)` -- Configure LazyOwn's centralized logging system.
- `get_logger` (function) `modules/logging_config.py:328` `def get_logger(name, level)` -- Get a logger with the given name.
- `set_level` (function) `modules/logging_config.py:357` `def set_level(name, level)` -- Set the log level for a specific logger.
- `set_quiet` (function) `modules/logging_config.py:367` `def set_quiet()` -- Silence all logging below WARNING level.
- `set_verbose` (function) `modules/logging_config.py:373` `def set_verbose()` -- Enable DEBUG level logging.
- `silence_module` (function) `modules/logging_config.py:379` `def silence_module(name)` -- Completely silence a noisy module.
- `reset` (function) `modules/logging_config.py:388` `def reset()` -- Reset the logging system to defaults.

## modules/loop/decision_log.py
- `digest` (function) `modules/loop/decision_log.py:51` `def digest(text)` -- Return the stable short digest used to fingerprint a decision input.
- `context_digest` (function) `modules/loop/decision_log.py:90` `def context_digest(ctx)` -- Fingerprint a selection context independent of field ordering.
- `config_digest` (function) `modules/loop/decision_log.py:115` `def config_digest(config)` -- Fingerprint the config keys that change a decision's reproducibility.
- `new_run_id` (function) `modules/loop/decision_log.py:137` `def new_run_id()` -- Return a fresh identifier grouping all decisions of one loop run.
- `record` (function) `modules/loop/decision_log.py:192` `def record(rec, path)` -- Append one decision to the ledger, rotating it when oversized.
- `read_records` (function) `modules/loop/decision_log.py:221` `def read_records(path)` -- Return every decision row in order, for audit or deterministic replay.
- `filtered_rows` (function) `modules/loop/decision_log.py:248` `def filtered_rows(items)` -- Shape ``(command, reason)`` pairs into ledger-ready rejection rows.

## modules/loop/engine_proxy.py
Depends on: `modules/__init__.py`, `modules/lazy_loop.py`, `modules/traffic_recorder.py`
Imported by: `modules/loop/__init__.py`
- `EngineProxyMixin.proxy_start` (method) `modules/loop/engine_proxy.py:16` `def proxy_start(self, host, port, task_id, trust, upstream)` -- Start the shared recorder proxy and apply its trust environment.
- `EngineProxyMixin.proxy_stop` (method) `modules/loop/engine_proxy.py:52` `def proxy_stop(self)` -- Stop the recorder proxy and clear its trust environment.
- `EngineProxyMixin.proxy_status` (method) `modules/loop/engine_proxy.py:60` `def proxy_status(self)` -- Return recorder proxy state (running, address, CA, exchanges).
- `EngineProxyMixin.proxy_env` (method) `modules/loop/engine_proxy.py:66` `def proxy_env(self)` -- Return the environment overrides that route tools via proxy.
- `EngineProxyMixin.ingest_proxy_traffic` (method) `modules/loop/engine_proxy.py:75` `def ingest_proxy_traffic(self, task_id, limit)` -- Mirror new recorder exchanges into the task traffic log.
- `EngineProxyMixin.search_proxy_body` (method) `modules/loop/engine_proxy.py:130` `def search_proxy_body(self, task_id, query, limit)` -- Full-text search proxy bodies scoped to one task's exchanges.

## modules/loop/triage_scheduler.py
Imported by: `modules/lazy_loop.py`, `modules/loop/__init__.py`, `tests/test_triage_scheduler.py`
- `estimate_difficulty` (function) `modules/loop/triage_scheduler.py:36` `def estimate_difficulty(facts)` -- Estimate a target's difficulty in ``[0.0, 1.0]`` from known facts.
- `TriageScheduler.__init__` (method) `modules/loop/triage_scheduler.py:92` `def __init__(self, stop_loss_attempts, salvage_progress, hard_threshold)` -- Initialize the scheduler with its policy thresholds.
- `TriageScheduler.should_stop` (method) `modules/loop/triage_scheduler.py:110` `def should_stop(self, record)` -- Return True when a target has burned its attempt budget unproductively.
- `TriageScheduler.route` (method) `modules/loop/triage_scheduler.py:122` `def route(self, record)` -- Return the worker tier for a target: ``general`` (hard) or ``soldier``.
- `TriageScheduler.order` (method) `modules/loop/triage_scheduler.py:133` `def order(self, records)` -- Return records ordered for draining.
- `normal_key` (function) `modules/loop/triage_scheduler.py:156` `def normal_key(record)`
- `salvage_key` (function) `modules/loop/triage_scheduler.py:163` `def salvage_key(record)`
- `TriageScheduler.pick_next` (method) `modules/loop/triage_scheduler.py:172` `def pick_next(self, records)` -- Return the single record to drain next, or None when empty.

## modules/loop/worker_agentic.py
Depends on: `core/config.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/guard_rules.py`, `modules/harness.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/lazy_skills.py`, `modules/loop/__init__.py`, `modules/outcome_attribution.py`
Imported by: `modules/loop/__init__.py`, `tests/test_lazy_worker_safety.py`, `tests/test_loop_decision_log.py`, `tests/test_loop_deterministic_mode.py`, `tests/test_outcome_attribution.py`
- `run_command` (function) `modules/loop/worker_agentic.py:308` `def run_command(command, background)` -- Run one shell probe/verb through scope, guard and audit.
- `record_fact` (function) `modules/loop/worker_agentic.py:335` `def record_fact(text)` -- Persist one observed or inferred fact on the exploration graph.
- `report_finding` (function) `modules/loop/worker_agentic.py:344` `def report_finding(name, evidence, severity)` -- Record a verified vulnerability with its evidence.
- `traffic_search` (function) `modules/loop/worker_agentic.py:355` `def traffic_search(query)` -- Search captured command/traffic records by keyword.
- `graph_state` (function) `modules/loop/worker_agentic.py:368` `def graph_state()` -- Compact exploration overview: intents, facts, findings.
- `shell_open` (function) `modules/loop/worker_agentic.py:383` `def shell_open()` -- Open a persistent bash session for multi-step shell work.
- `shell_send` (function) `modules/loop/worker_agentic.py:387` `def shell_send(command)` -- Run one guarded command in the persistent shell session.
- `job_status` (function) `modules/loop/worker_agentic.py:391` `def job_status(job_id)` -- Report whether one background job is still running.
- `job_output` (function) `modules/loop/worker_agentic.py:399` `def job_output(job_id)` -- Return the tail of one background job's output.

## modules/loop_ai_bridge.py
Depends on: `core/config.py`, `modules/detection_oracle.py`, `modules/event_bus.py`, `modules/moe_router.py`, `modules/opsec_scorer.py`, `modules/orchestrator_config.py`, `modules/rl_trainer.py`, `skills/hive_mind.py`, `skills/swan_agent.py`
Imported by: `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/mediation/telemetry_mediator.py`, `tests/conftest.py`, `tests/test_lazy_streaming.py`, `tests/test_loop_ai_bridge.py`, `tests/test_mediation.py`
- `publish_loop_event` (function) `modules/loop_ai_bridge.py:74` `def publish_loop_event(task_id, worker, kind, text, severity)` -- Publish one loop activity to the unified bus and Hive memory.
- `assess_opsec` (function) `modules/loop_ai_bridge.py:125` `def assess_opsec(command, rhost)` -- Return a pre-execution OPSEC gate assessment, or None when unavailable.
- `intent_tool_class` (function) `modules/loop_ai_bridge.py:169` `def intent_tool_class(summary)` -- Return the coarse tool class an intent summary belongs to.
- `record_outcome_quality` (function) `modules/loop_ai_bridge.py:213` `def record_outcome_quality(worker, intent_summary, facts, findings)` -- Feed one intent's net yield back to MoE/RL as a decision-quality reward.
- `tool_class_yields` (function) `modules/loop_ai_bridge.py:240` `def tool_class_yields(summaries, phase)` -- Return the learned decision-quality yield for each candidate summary.
- `annotate_detection` (function) `modules/loop_ai_bridge.py:280` `def annotate_detection(command, action_category)` -- Return oracle details for one command, or None when unavailable.
- `moe_route` (function) `modules/loop_ai_bridge.py:304` `def moe_route(task_type, goal)` -- Return the MoE router's preferred expert for a task type, or None.
- `moe_record_outcome` (function) `modules/loop_ai_bridge.py:321` `def moe_record_outcome(expert_id, task_type, reward, detection_prob)` -- Feed one execution outcome back to the MoE performance store.
- `rl_select` (function) `modules/loop_ai_bridge.py:340` `def rl_select(task_type, phase, candidates, deterministic)` -- Pick an expert with the RL policy; first candidate when unavailable.
- `rl_update` (function) `modules/loop_ai_bridge.py:362` `def rl_update(task_type, phase, action, reward, candidates, detection_prob)` -- Apply one Q-learning update for an executed action.
- `rl_save` (function) `modules/loop_ai_bridge.py:385` `def rl_save()` -- Persist the RL tables after a run.
- `record_step` (function) `modules/loop_ai_bridge.py:404` `def record_step(task_id, worker, command, output, detection_prob)` -- Feed one executed command outcome to MoE and the RL trainer.
- `swan_available` (function) `modules/loop_ai_bridge.py:419` `def swan_available()` -- Return True when the SWAN orchestrator can be constructed.
- `swan_consult` (function) `modules/loop_ai_bridge.py:432` `def swan_consult(prompt, task_type, phase, timeout)` -- Ask SWAN for an ensemble answer; empty string when unavailable.
- `stream_enabled` (function) `modules/loop_ai_bridge.py:459` `def stream_enabled()` -- Return whether token streaming into the activity log is enabled.
- `ai_snapshot` (function) `modules/loop_ai_bridge.py:469` `def ai_snapshot()` -- Compact status of the wired AI stack for the operator log.

## modules/loop_audit.py
Depends on: `core/parsers.py`
- `step_context` (function) `modules/loop_audit.py:80` `def step_context(task_id)` -- Annotate every command executed inside the block with step context.
- `audit_path` (function) `modules/loop_audit.py:109` `def audit_path(task_id)` -- Return the audit file path for one task.
- `LoopAudit.__init__` (method) `modules/loop_audit.py:123` `def __init__(self, task_id, path)` -- Bind the audit file and start the run clock.
- `LoopAudit.path` (method) `modules/loop_audit.py:131` `def path(self)` -- Return the timeline file path.
- `LoopAudit.record` (method) `modules/loop_audit.py:135` `def record(self, kind)` -- Append one event and enforce the file cap.
- `LoopAudit.run_start` (method) `modules/loop_audit.py:155` `def run_start(self, goal, target, rounds, workers, mode, profile)` -- Record the loop lifecycle start.
- `LoopAudit.preflight` (method) `modules/loop_audit.py:168` `def preflight(self, outcome)` -- Record the target preflight verdict.
- `LoopAudit.blocked` (method) `modules/loop_audit.py:178` `def blocked(self, source, reason, command, worker, intent)` -- Record a command that never ran because a gate blocked it.
- `LoopAudit.verdict` (method) `modules/loop_audit.py:189` `def verdict(self, verdict)` -- Record the independent goal-evaluation verdict.
- `LoopAudit.run_end` (method) `modules/loop_audit.py:203` `def run_end(self, status, rounds, verdict, error)` -- Record the loop lifecycle end with the final engine status.
- `LoopAudit.record_command` (method) `modules/loop_audit.py:216` `def record_command(self, command, output, duration, ok, task_id)` -- Record one executed command with its trigger context.
- `start` (function) `modules/loop_audit.py:320` `def start(task_id)` -- Create and register the audit for one task.
- `audit_for` (function) `modules/loop_audit.py:338` `def audit_for(task_id)` -- Return the active audit for one task, or None when not started.
- `stop` (function) `modules/loop_audit.py:349` `def stop(task_id)` -- Forget the registered audit for one task.
- `guard_rows` (function) `modules/loop_audit.py:360` `def guard_rows(task_id)` -- Return guard decisions recorded for one task.
- `activity_rows` (function) `modules/loop_audit.py:365` `def activity_rows(task_id)` -- Return engine activity rows for one task.
- `timeline` (function) `modules/loop_audit.py:415` `def timeline(task_id, audit)` -- Merge audit, guard and lifecycle rows into one timeline.
- `render` (function) `modules/loop_audit.py:505` `def render(task_id, limit, audit)` -- Render the merged campaign timeline for one task.
- `list_runs` (function) `modules/loop_audit.py:526` `def list_runs(limit)` -- Summarize every recorded loop run, newest first.
- `render_summary` (function) `modules/loop_audit.py:563` `def render_summary(summaries)` -- Render ``list_runs`` summaries as an operator table.

## modules/loop_guardrails.py
Depends on: `modules/__init__.py`
Imported by: `modules/chain_runner.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `modules/loop/worker_memory.py`, `tests/test_loop_guardrails.py`, `tests/test_orchestrator_pacing.py`, `tests/test_pacing.py`, `tests/test_repeat_shapes.py`, `tests/test_writeback_hygiene.py`
- `RepeatDetector.__init__` (method) `modules/loop_guardrails.py:117` `def __init__(self, window)`
- `RepeatDetector.record` (method) `modules/loop_guardrails.py:125` `def record(self, command)` -- Add one executed command; returns True when the window fills.
- `RepeatDetector.stuck` (method) `modules/loop_guardrails.py:182` `def stuck(self)` -- True when the loop is visibly not progressing.
- `RepeatDetector.describe` (method) `modules/loop_guardrails.py:200` `def describe(self)` -- Human sentence of the stuck shape for activity lines.
- `RepeatDetector.oscillation_pair` (method) `modules/loop_guardrails.py:222` `def oscillation_pair(self)` -- Return the detected alternating pair, ('', '') when none.
- `RepeatDetector.cycle` (method) `modules/loop_guardrails.py:226` `def cycle(self)` -- Return the detected repeating block, empty when none.
- `RepeatDetector.last_commands` (method) `modules/loop_guardrails.py:230` `def last_commands(self)` -- Snapshot of the recent command window (oldest first).
- `RepeatDetector.reset` (method) `modules/loop_guardrails.py:234` `def reset(self)` -- Clear the window (operator intervention acknowledged).
- `EdrPacer.__init__` (method) `modules/loop_guardrails.py:258` `def __init__(self, duration_threshold)` -- Configure the pacer.
- `EdrPacer.parse_windows` (method) `modules/loop_guardrails.py:304` `def parse_windows(raw)` -- Parse ``HH:MM-HH:MM`` window strings into minute tuples.
- `EdrPacer.from_config` (method) `modules/loop_guardrails.py:326` `def from_config(cls)` -- Build a pacer from the orchestrator pacing configuration.
- `EdrPacer.observe` (method) `modules/loop_guardrails.py:357` `def observe(self, command, duration_sec, output)` -- Feed one executed step and update the telemetry estimate.
- `EdrPacer.decay` (method) `modules/loop_guardrails.py:379` `def decay(self, factor)` -- Cool the estimate down (call once per completed step).
- `EdrPacer.level` (method) `modules/loop_guardrails.py:385` `def level(self)` -- Current pacing level: 0 calm, 1 cautious, 2 stealth.
- `EdrPacer.signal` (method) `modules/loop_guardrails.py:395` `def signal(self)` -- Human-readable reason for the current level (may be empty).
- `EdrPacer.in_sleeper_window` (method) `modules/loop_guardrails.py:426` `def in_sleeper_window(self, now)` -- True when local time falls inside a configured quiet window.
- `EdrPacer.windows_delay` (method) `modules/loop_guardrails.py:432` `def windows_delay(windows, now)` -- Static quiet-window delay for callers without a pacer instance.
- `EdrPacer.sleeper_delay` (method) `modules/loop_guardrails.py:459` `def sleeper_delay(self, now)` -- Recommended sleep because of a quiet window (0 when outside).
- `EdrPacer.inter_step_delay` (method) `modules/loop_guardrails.py:472` `def inter_step_delay(self)` -- Recommended sleep before the next step at the current level.
- `EdrPacer.quieten` (method) `modules/loop_guardrails.py:489` `def quieten(self, command)` -- Return a quieter variant of the command at the current level.
- `EdrPacer.describe` (method) `modules/loop_guardrails.py:504` `def describe(self)` -- Return a snapshot of the pacer state for admin surfaces.
- `TargetLimiter.__init__` (method) `modules/loop_guardrails.py:527` `def __init__(self, max_concurrent)`
- `TargetLimiter.max_concurrent` (method) `modules/loop_guardrails.py:534` `def max_concurrent(self)` -- Configured upper bound of simultaneous targets.
- `TargetLimiter.active_targets` (method) `modules/loop_guardrails.py:539` `def active_targets(self)` -- How many distinct targets currently hold a slot.
- `TargetLimiter.slot` (method) `modules/loop_guardrails.py:545` `def slot(self, target)` -- Hold one of at most ``max_concurrent`` target slots.
- `FactVectorStore.__init__` (method) `modules/loop_guardrails.py:597` `def __init__(self, path, max_facts)`
- `FactVectorStore.path` (method) `modules/loop_guardrails.py:605` `def path(self)` -- Backing file path.
- `FactVectorStore.add` (method) `modules/loop_guardrails.py:626` `def add(self, text, meta)` -- Embed and store one fact; returns False for duplicates.
- `FactVectorStore.search` (method) `modules/loop_guardrails.py:660` `def search(self, query, k)` -- Return the ``k`` facts most similar to the query.
- `FactVectorStore.search_block` (method) `modules/loop_guardrails.py:690` `def search_block(self, query, k, max_chars)` -- Render retrieved facts as a prompt-ready block (may be empty).
- `FactVectorStore.clear` (method) `modules/loop_guardrails.py:699` `def clear(self)` -- Drop every fact (manual reset path).
- `FactVectorStore.save` (method) `modules/loop_guardrails.py:705` `def save(self)` -- Persist atomically; I/O errors never surface to the loop.
- `listing_forbidden` (function) `modules/loop_guardrails.py:759` `def listing_forbidden(command)` -- Return the listing veto reason, empty when the command may run.
- `ListingNoiseDetector.observe` (method) `modules/loop_guardrails.py:798` `def observe(self, command, output)` -- Return True when the step is a pure directory listing dump.

## modules/loop_manager.py
Imported by: `lazyc2.py`, `lazyc2/blueprints/loops.py`, `tests/test_loop_manager.py`
- `LoopValidationError.__init__` (method) `modules/loop_manager.py:91` `def __init__(self, field, message)` -- Store the offending field alongside the human message.
- `validate_target` (function) `modules/loop_manager.py:101` `def validate_target(raw)` -- Return the canonical string form of a validated IP address target.
- `sanitize_goal` (function) `modules/loop_manager.py:124` `def sanitize_goal(raw)` -- Return a safe goal string accepted by the loop parser.
- `clamp_int` (function) `modules/loop_manager.py:151` `def clamp_int(raw, field, default, minimum, maximum)` -- Parse and clamp an integer knob to the supported range.
- `clamp_float` (function) `modules/loop_manager.py:176` `def clamp_float(raw, field, default, minimum, maximum)` -- Parse and clamp a float knob to the supported range.
- `validate_loop_id` (function) `modules/loop_manager.py:201` `def validate_loop_id(loop_id)` -- Validate a loop id and return its normalized hex form.
- `LoopManager.__init__` (method) `modules/loop_manager.py:328` `def __init__(self, loops_dir, python_executable, max_concurrent, repo_root, lazyown_script)` -- Create the manager and its persistence lock.
- `LoopManager.loops_dir` (method) `modules/loop_manager.py:350` `def loops_dir(self)` -- Return the root directory for loop workspaces.
- `LoopManager.start` (method) `modules/loop_manager.py:354` `def start(self, spec, operator)` -- Validate, spawn and register one autonomous loop.
- `LoopManager.list_loops` (method) `modules/loop_manager.py:549` `def list_loops(self)` -- Return every registry record with refreshed live status.
- `LoopManager.get_loop` (method) `modules/loop_manager.py:584` `def get_loop(self, loop_id)` -- Return one registry record by id.
- `LoopManager.read_log` (method) `modules/loop_manager.py:603` `def read_log(self, loop_id, offset)` -- Read one chunk of a loop's output log.
- `LoopManager.stop` (method) `modules/loop_manager.py:670` `def stop(self, loop_id)` -- Stop one running loop by terminating its process group.
- `LoopManager.summary` (method) `modules/loop_manager.py:735` `def summary(self)` -- Return an aggregate view of loop activity for the report.
- `default_manager` (function) `modules/loop_manager.py:853` `def default_manager()` -- Return the process-wide loop manager singleton.

## modules/loop_preflight.py
Depends on: `modules/__init__.py`
- `lab_state_for` (function) `modules/loop_preflight.py:38` `def lab_state_for(target, scenarios, running, existing, ip_lookup)` -- Map a target IP to its lab scenario and container state.
- `probe_tcp_detailed` (function) `modules/loop_preflight.py:83` `def probe_tcp_detailed(target, ports, timeout)` -- Probe TCP ports in parallel and classify the answers.
- `probe_tcp` (function) `modules/loop_preflight.py:125` `def probe_tcp(target, ports, timeout)` -- Probe TCP ports in parallel and return the open ones.
- `check_target` (function) `modules/loop_preflight.py:145` `def check_target(target, ports, connect_timeout, lab)` -- Decide whether a loop may be spent against this target.
- `recovery_hint` (function) `modules/loop_preflight.py:211` `def recovery_hint(outcome)` -- Return the operator-facing recovery line for a failed preflight.

## modules/loop_progress.py
Depends on: `core/safe_console.py`
Imported by: `cli/lazy_monitor.py`, `modules/lazy_runner.py`, `tests/test_lazy_runner.py`, `tests/test_loop_progress.py`
- `snapshot_from_overview` (function) `modules/loop_progress.py:99` `def snapshot_from_overview(overview, record, activity_tail, elapsed_sec)` -- Build a snapshot from a graph overview dict plus task record.
- `snap_to_states` (function) `modules/loop_progress.py:123` `def snap_to_states(snapshot)` -- Infer done/active/pending per chain stage from a snapshot.
- `sanitize_line` (function) `modules/loop_progress.py:151` `def sanitize_line(line, keep_ansi)` -- Strip ANSI codes and carriage returns from a transcript line.
- `LoopProgress.live_mode` (method) `modules/loop_progress.py:195` `def live_mode(self)` -- True only when the sink supports a real live region.
- `LoopProgress.start` (method) `modules/loop_progress.py:202` `def start(self)` -- Open the Live display, or print the header in line mode.
- `LoopProgress.stop` (method) `modules/loop_progress.py:229` `def stop(self)` -- Freeze the final panel on screen (both modes).
- `LoopProgress.refresh` (method) `modules/loop_progress.py:246` `def refresh(self, snapshot)` -- Re-render milestones from a fresh snapshot (thread-safe).
- `LoopProgress.emit` (method) `modules/loop_progress.py:268` `def emit(self, line)` -- Print a transcript line above the live panel, colors preserved.

## modules/loop_triggers.py
Depends on: `modules/__init__.py`, `modules/auto_registry.py`, `modules/lazy_heat.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`, `modules/world_model.py`
Imported by: `cli/commands/netattack.py`, `cli/orchestrator_assets_tabs.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`, `tests/test_loop_trigger_hints.py`, `tests/test_orchestrator_triggers.py`, `tests/test_trigger_policy.py`
- `hint_fingerprint` (function) `modules/loop_triggers.py:28` `def hint_fingerprint(row)` -- Return the evidence signature of one hot-CVE candidate.
- `prune_hint_fingerprints` (function) `modules/loop_triggers.py:60` `def prune_hint_fingerprints(store, now, ttl)` -- Return only the fresh fingerprints of a stored fingerprint map.
- `TriggerStore.__init__` (method) `modules/loop_triggers.py:91` `def __init__(self, task_id)` -- Bind trigger table (global when task_id empty).
- `TriggerStore.add` (method) `modules/loop_triggers.py:101` `def add(self, kind, arg, every_sec)` -- Register a trigger; interval needs every_sec, events fire on new rows.
- `TriggerStore.upsert_defaults` (method) `modules/loop_triggers.py:123` `def upsert_defaults(self, seeds)` -- Merge declarative seeds without duplicating or re-enabling.
- `TriggerStore.remove` (method) `modules/loop_triggers.py:165` `def remove(self, trigger_id)` -- Delete a trigger.
- `TriggerStore.set_enabled` (method) `modules/loop_triggers.py:176` `def set_enabled(self, trigger_id, enabled)` -- Flip one trigger's enabled flag in place.
- `TriggerStore.list` (method) `modules/loop_triggers.py:190` `def list(self)` -- Return all triggers.
- `TriggerStore.ensure_service_trigger` (method) `modules/loop_triggers.py:194` `def ensure_service_trigger(self)` -- Register the catalog trigger once so services fire the loop.
- `TriggerStore.ensure_cve_hot_trigger` (method) `modules/loop_triggers.py:207` `def ensure_cve_hot_trigger(self)` -- Register the hot-CVE trigger once so fresh intel fires the loop.
- `TriggerStore.ensure_ad_surface_trigger` (method) `modules/loop_triggers.py:220` `def ensure_ad_surface_trigger(self)` -- Register the AD-surface trigger once so Windows identity fires it.
- `TriggerStore.due` (method) `modules/loop_triggers.py:233` `def due(self, task_id, graph, activity, assets, store)` -- Evaluate triggers like the scheduler tick; fires at most once each.
- `read_signing_evidence` (function) `modules/loop_triggers.py:499` `def read_signing_evidence(store_dir)` -- Load operator-attested SMB signing evidence per host.

## modules/macos_payloads.py
Imported by: `cli/commands/payload_arsenal.py`
- `MacOSPayloadFactory.__init__` (method) `modules/macos_payloads.py:111` `def __init__(self, config, output_dir)`
- `MacOSPayloadFactory.generate_app_bundle` (method) `modules/macos_payloads.py:137` `def generate_app_bundle(self)` -- Generate a macOS .app bundle with embedded reverse shell.
- `MacOSPayloadFactory.generate_launchd_persistence` (method) `modules/macos_payloads.py:212` `def generate_launchd_persistence(self)` -- Generate a LaunchDaemon or LaunchAgent plist for persistence.
- `MacOSPayloadFactory.generate_tcc_bypass` (method) `modules/macos_payloads.py:268` `def generate_tcc_bypass(self)` -- Generate a TCC bypass script targeting common permissions.
- `MacOSPayloadFactory.generate_osascript_dropper` (method) `modules/macos_payloads.py:314` `def generate_osascript_dropper(self)` -- Generate an AppleScript-based dropper that downloads and executes a stage.
- `MacOSPayloadFactory.generate_swift_stager` (method) `modules/macos_payloads.py:335` `def generate_swift_stager(self)` -- Generate a Swift reverse shell stager.
- `MacOSPayloadFactory.generate_persistence_scripts` (method) `modules/macos_payloads.py:398` `def generate_persistence_scripts(self)` -- Generate all available macOS persistence scripts.
- `MacOSPayloadFactory.generate_phishing_dialog` (method) `modules/macos_payloads.py:447` `def generate_phishing_dialog(self)` -- Generate an AppleScript credential phishing dialog.
- `MacOSPayloadFactory.generate_all` (method) `modules/macos_payloads.py:470` `def generate_all(self)` -- Generate all macOS payload artifacts.
- `MacOSPayloadFactory.list_tcc_services` (method) `modules/macos_payloads.py:517` `def list_tcc_services()` -- Return the list of known TCC service identifiers.
- `MacOSPayloadFactory.list_persistence_methods` (method) `modules/macos_payloads.py:522` `def list_persistence_methods()` -- Return the list of available persistence methods for macOS.

## modules/mario.py
- `check_collision` (function) `modules/mario.py:105` `def check_collision(x, y, layer)`

## modules/mcp_agent_bridge.py
Depends on: `core/logging.py`, `modules/llm_factory.py`
Imported by: `modules/unified_bridge.py`, `skills/lazyown_mcp.py`, `skills/mcp_tools/agent_result.py`, `skills/mcp_tools/agent_status.py`, `skills/mcp_tools/list_agents.py`, `skills/mcp_tools/run_agent.py`, `skills/mcp_tools/subagent_run.py`
- `get_agent_status` (function) `modules/mcp_agent_bridge.py:163` `def get_agent_status(agent_id)` -- Public: returns current status dict for an agent.
- `get_agent_result` (function) `modules/mcp_agent_bridge.py:188` `def get_agent_result(agent_id)` -- Public: returns final result + full action log.
- `list_agents` (function) `modules/mcp_agent_bridge.py:211` `def list_agents(limit)` -- List recent agents sorted by start time.
- `GroqAgentWorker.__init__` (method) `modules/mcp_agent_bridge.py:235` `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)`
- `GroqAgentWorker.run` (method) `modules/mcp_agent_bridge.py:264` `def run(self)`
- `OllamaReActWorker.__init__` (method) `modules/mcp_agent_bridge.py:368` `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)`
- `OllamaReActWorker.run` (method) `modules/mcp_agent_bridge.py:389` `def run(self)`
- `AgentBridgeWorker.__init__` (method) `modules/mcp_agent_bridge.py:471` `def __init__(self, agent_id, goal, backend, run_cmd, max_iterations)`
- `AgentBridgeWorker.run` (method) `modules/mcp_agent_bridge.py:478` `def run(self)`
- `start_agent` (function) `modules/mcp_agent_bridge.py:508` `def start_agent(goal, backend, lazyown_runner_fn, max_iterations)` -- Start an agent in a background thread.
- `dummy_runner` (function) `modules/mcp_agent_bridge.py:531` `def dummy_runner(cmd)`

## modules/mediation/chain_mediator.py
Depends on: `modules/lazy_loop.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`, `tests/test_guardrails.py`
- `LlmPoolPort.complete` (method) `modules/mediation/chain_mediator.py:16` `def complete(self, prompt, max_tokens, task_id)` -- Complete one prompt through the LLM pool.
- `LlmPoolPort.has_members` (method) `modules/mediation/chain_mediator.py:34` `def has_members(self)` -- Report whether any LLM member is configured.
- `ChainMediator.__init__` (method) `modules/mediation/chain_mediator.py:53` `def __init__(self)` -- Start with the default pool port.
- `ChainMediator.register_llm_port` (method) `modules/mediation/chain_mediator.py:57` `def register_llm_port(self, port)` -- Replace the completion port (injection point for tests/gyms).
- `ChainMediator.llm` (method) `modules/mediation/chain_mediator.py:65` `def llm(self)` -- Return the completion port for pipeline requests.
- `ChainMediator.describe` (method) `modules/mediation/chain_mediator.py:73` `def describe(self)` -- Return mediator metadata for diagnostics.

## modules/mediation/contracts.py
Depends on: `modules/mediation/hub.py`
Imported by: `modules/loop/worker_memory.py`, `modules/mediation/__init__.py`, `modules/mediation/engine_mediator.py`, `modules/mediation/hub.py`, `tests/test_engine_mediator.py`
- `MediationDomains.is_known` (method) `modules/mediation/contracts.py:24` `def is_known(cls, domain)` -- Check whether a domain key is registered in the default set.
- `ActivityLogPort.read` (method) `modules/mediation/contracts.py:45` `def read(self, limit)` -- Return the latest activity records oldest-first.
- `LlmCompletionPort.complete` (method) `modules/mediation/contracts.py:61` `def complete(self, prompt, max_tokens, task_id)` -- Complete one prompt with the configured LLM pool.
- `LlmCompletionPort.has_members` (method) `modules/mediation/contracts.py:79` `def has_members(self)` -- Report whether any LLM member is configured.
- `MediatorContract.describe` (method) `modules/mediation/contracts.py:90` `def describe(self)` -- Return introspection metadata for diagnostics.
- `MediationHubContract.mediator_for` (method) `modules/mediation/contracts.py:99` `def mediator_for(self, domain)` -- Return the mediator registered for a domain key, or None.
- `resolve` (function) `modules/mediation/contracts.py:104` `def resolve(domain)` -- Return the default-hub mediator for a domain key.

## modules/mediation/engine_mediator.py
Depends on: `modules/ai_exploit_chain.py`, `modules/autonomous_exploit_engine.py`, `modules/mediation/contracts.py`, `modules/reactive_engine.py`
Imported by: `modules/mediation/hub.py`, `tests/test_engine_mediator.py`
- `ExploitRetryPort.retry_with_credentials` (method) `modules/mediation/engine_mediator.py:37` `def retry_with_credentials(self, target, credentials)` -- Queue one retry attempt per captured credential pair.
- `ReactionPort.analyse` (method) `modules/mediation/engine_mediator.py:54` `def analyse(self, output, command, platform)` -- Analyse one command's output for next-action decisions.
- `ReasoningPort.reason` (method) `modules/mediation/engine_mediator.py:72` `def reason(self, target)` -- Return the next exploit strategy for a target.
- `EngineMediator.describe` (method) `modules/mediation/engine_mediator.py:89` `def describe(self)` -- Return introspection metadata for diagnostics.
- `EngineMediator.retry_with_credentials` (method) `modules/mediation/engine_mediator.py:97` `def retry_with_credentials(self, target, credentials)` -- Queue captured credentials into the exploit engine's retry loop.
- `EngineMediator.analyse` (method) `modules/mediation/engine_mediator.py:118` `def analyse(self, output, command, platform)` -- Run reactive-engine analysis over one step's output.
- `EngineMediator.reason` (method) `modules/mediation/engine_mediator.py:136` `def reason(self, target)` -- Return the exploit-chain strategy for a target.

## modules/mediation/feedback_mediator.py
Depends on: `modules/lazy_orchestrator_feedback.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `FeedbackMediator.describe` (method) `modules/mediation/feedback_mediator.py:18` `def describe(self)` -- Return mediator metadata for diagnostics.
- `FeedbackMediator.order_steps` (method) `modules/mediation/feedback_mediator.py:22` `def order_steps(self, steps, stack)` -- Reorder worker steps with cross-task priors.

## modules/mediation/hub.py
Depends on: `modules/mediation/chain_mediator.py`, `modules/mediation/contracts.py`, `modules/mediation/engine_mediator.py`, `modules/mediation/feedback_mediator.py`, `modules/mediation/intel_mediator.py`, `modules/mediation/telemetry_mediator.py`
Imported by: `modules/loop/worker_memory.py`, `modules/mediation/__init__.py`, `modules/mediation/contracts.py`, `tests/test_mediation.py`
- `MediationHub.__init__` (method) `modules/mediation/hub.py:22` `def __init__(self)` -- Start with an empty registry.
- `MediationHub.register` (method) `modules/mediation/hub.py:26` `def register(self, mediator)` -- Register a mediator under its declared domain.
- `MediationHub.mediator_for` (method) `modules/mediation/hub.py:35` `def mediator_for(self, domain)` -- Return the mediator registered for a domain key, or None.
- `MediationHub.snapshot` (method) `modules/mediation/hub.py:46` `def snapshot(self)` -- Return high-level metadata for every registered mediator.
- `default_hub` (function) `modules/mediation/hub.py:75` `def default_hub()` -- Return a fresh default-configured hub (test-safe, no singleton).
- `get_hub` (function) `modules/mediation/hub.py:80` `def get_hub()` -- Return the process-wide hub, building it on first use.

## modules/mediation/intel_mediator.py
Depends on: `modules/lazy_intel.py`, `modules/lazy_loop.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `IntelMediator.__init__` (method) `modules/mediation/intel_mediator.py:18` `def __init__(self)` -- Start with no registered activity-log factory.
- `IntelMediator.register_activity_log_factory` (method) `modules/mediation/intel_mediator.py:22` `def register_activity_log_factory(self, factory)` -- Register the loop-side activity log factory.
- `IntelMediator.describe` (method) `modules/mediation/intel_mediator.py:32` `def describe(self)` -- Return mediator metadata for diagnostics.
- `IntelMediator.activity_records` (method) `modules/mediation/intel_mediator.py:39` `def activity_records(self, task_id, limit)` -- Return loop activity records for one task.
- `IntelMediator.record_routing_decision` (method) `modules/mediation/intel_mediator.py:64` `def record_routing_decision(self, task_id, intent_id, command, intent_text, target, stack)` -- Record which verb the loop chose for one intent.
- `IntelMediator.record_routing_outcome` (method) `modules/mediation/intel_mediator.py:97` `def record_routing_outcome(self, task_id, intent_id, command, state, facts, findings, stack)` -- Record the terminal outcome of one executed command.
- `IntelMediator.mask_configured` (method) `modules/mediation/intel_mediator.py:133` `def mask_configured(self, text)` -- Strip operator-configured secrets from LLM-bound context.
- `IntelMediator.stack_signature` (method) `modules/mediation/intel_mediator.py:149` `def stack_signature(self, assets)` -- Return the target stack fingerprint string.

## modules/mediation/telemetry_mediator.py
Depends on: `modules/loop_ai_bridge.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `TelemetryMediator.describe` (method) `modules/mediation/telemetry_mediator.py:19` `def describe(self)` -- Return mediator metadata for diagnostics.
- `TelemetryMediator.publish_event` (method) `modules/mediation/telemetry_mediator.py:23` `def publish_event(self, task_id, worker, kind, text, severity)` -- Publish one loop activity event to listeners.
- `TelemetryMediator.annotate_detection` (method) `modules/mediation/telemetry_mediator.py:43` `def annotate_detection(self, command)` -- Return the detection annotation for one command.
- `TelemetryMediator.assess_opsec` (method) `modules/mediation/telemetry_mediator.py:59` `def assess_opsec(self, command, rhost)` -- Return the pre-execution OPSEC gate assessment for one command.
- `TelemetryMediator.record_outcome_quality` (method) `modules/mediation/telemetry_mediator.py:77` `def record_outcome_quality(self, worker, intent_summary, facts, findings)` -- Record one intent's net yield as a decision-quality reward.
- `TelemetryMediator.tool_class_yields` (method) `modules/mediation/telemetry_mediator.py:93` `def tool_class_yields(self, summaries, phase)` -- Return learned decision-quality yields for candidate summaries.
- `TelemetryMediator.record_step` (method) `modules/mediation/telemetry_mediator.py:111` `def record_step(self, task_id, worker, command, output, detection_prob)` -- Record one executed step for learning stores.
- `TelemetryMediator.swan_available` (method) `modules/mediation/telemetry_mediator.py:128` `def swan_available(self)` -- Return True when the SWAN ensemble is ready.
- `TelemetryMediator.swan_consult` (method) `modules/mediation/telemetry_mediator.py:137` `def swan_consult(self, prompt, task_type, phase, timeout)` -- Consult the SWAN ensemble with one prompt.
- `TelemetryMediator.moe_route` (method) `modules/mediation/telemetry_mediator.py:162` `def moe_route(self, task_type)` -- Return the preferred MoE expert for a task type.
- `TelemetryMediator.rl_select` (method) `modules/mediation/telemetry_mediator.py:178` `def rl_select(self, task_type, phase, candidates, deterministic)` -- Return the RL-preferred candidate name.
- `TelemetryMediator.moe_record_outcome` (method) `modules/mediation/telemetry_mediator.py:203` `def moe_record_outcome(self, expert_id, task_type, reward, detection_prob)` -- Record one MoE outcome for learning.
- `TelemetryMediator.rl_update` (method) `modules/mediation/telemetry_mediator.py:219` `def rl_update(self, task_type, phase, action, reward, candidates, detection_prob)` -- Apply one Q-learning update for an executed action.

## modules/memory_cleaner.py
Imported by: `cli/commands/opsec_cleanup.py`
- `MemoryCleaner.__init__` (method) `modules/memory_cleaner.py:61` `def __init__(self, config)`
- `MemoryCleaner.windows_memory_cleanup` (method) `modules/memory_cleaner.py:64` `def windows_memory_cleanup(self)` -- Generate Windows memory artifact cleanup commands.
- `MemoryCleaner.linux_memory_cleanup` (method) `modules/memory_cleaner.py:151` `def linux_memory_cleanup(self)` -- Generate Linux memory artifact cleanup commands.
- `MemoryCleaner.macos_memory_cleanup` (method) `modules/memory_cleaner.py:206` `def macos_memory_cleanup(self)` -- Generate macOS memory artifact cleanup commands.
- `MemoryCleaner.generate_on_exit_script` (method) `modules/memory_cleaner.py:255` `def generate_on_exit_script(self)` -- Generate an on-exit cleanup script for beacons.

## modules/memory_embeddings.py
Imported by: `modules/memory_store.py`, `tests/test_memory_semantics.py`
- `embed` (function) `modules/memory_embeddings.py:50` `def embed(text)` -- Map text to a normalised 512-float histogram BLOB.
- `cosine` (function) `modules/memory_embeddings.py:75` `def cosine(a, b)` -- Cosine similarity of two embedding BLOBs; legacy/partial input -> 0.0.
- `semantic_top_k` (function) `modules/memory_embeddings.py:85` `def semantic_top_k(query, candidates, top_k)` -- Rank candidate (id, embedding) pairs against the query.
- `as_floats` (function) `modules/memory_embeddings.py:109` `def as_floats(blob)` -- Decode a BLOB into a mutable float array (diagnostics/tests).

## modules/memory_store.py
Depends on: `modules/memory_embeddings.py`
Imported by: `tests/test_memory_semantics.py`
- `StorageBackend.save` (method) `modules/memory_store.py:99` `def save(self, entry)`
- `StorageBackend.search` (method) `modules/memory_store.py:102` `def search(self, query, top_k)`
- `StorageBackend.by_host` (method) `modules/memory_store.py:105` `def by_host(self, host, top_k)`
- `StorageBackend.by_service` (method) `modules/memory_store.py:108` `def by_service(self, service, top_k)`
- `StorageBackend.all_entries` (method) `modules/memory_store.py:111` `def all_entries(self, limit)`
- `StorageBackend.close` (method) `modules/memory_store.py:114` `def close(self)`
- `SQLiteBackend.__init__` (method) `modules/memory_store.py:133` `def __init__(self, db_path)`
- `SQLiteBackend.save` (method) `modules/memory_store.py:148` `def save(self, entry)`
- `SQLiteBackend.search` (method) `modules/memory_store.py:180` `def search(self, query, top_k)`
- `SQLiteBackend.by_host` (method) `modules/memory_store.py:192` `def by_host(self, host, top_k)`
- `SQLiteBackend.by_service` (method) `modules/memory_store.py:203` `def by_service(self, service, top_k)`
- `SQLiteBackend.all_entries` (method) `modules/memory_store.py:215` `def all_entries(self, limit)`
- `SQLiteBackend.stats_raw` (method) `modules/memory_store.py:225` `def stats_raw(self)`
- `SQLiteBackend.close` (method) `modules/memory_store.py:232` `def close(self)`
- `MemoryStore.__init__` (method) `modules/memory_store.py:240` `def __init__(self, backend)`
- `MemoryStore.remember` (method) `modules/memory_store.py:243` `def remember(self, session_id, host, tool, command, output, findings, success)`
- `MemoryStore.recall` (method) `modules/memory_store.py:270` `def recall(self, query, top_k)`
- `MemoryStore.recall_by_host` (method) `modules/memory_store.py:273` `def recall_by_host(self, host, top_k)`
- `MemoryStore.recall_for_service` (method) `modules/memory_store.py:276` `def recall_for_service(self, service_name, top_k)`
- `MemoryStore.recall_hybrid` (method) `modules/memory_store.py:279` `def recall_hybrid(self, query, top_k)` -- FTS5 keyword hits first; semantic fallback when keywords miss.
- `MemoryStore.stats` (method) `modules/memory_store.py:292` `def stats(self)`
- `MemoryStore.export_finetuning_dataset` (method) `modules/memory_store.py:300` `def export_finetuning_dataset(self, path)`
- `VectorSQLiteBackend.save` (method) `modules/memory_store.py:320` `def save(self, entry)`
- `VectorSQLiteBackend.search_semantic` (method) `modules/memory_store.py:328` `def search_semantic(self, query, top_k)`
- `get_memory_store` (function) `modules/memory_store.py:339` `def get_memory_store()`
- `remember` (function) `modules/memory_store.py:348` `def remember(session_id, host, tool, command, output, findings, success)`
- `recall` (function) `modules/memory_store.py:360` `def recall(query, top_k)`
- `recall_hybrid` (function) `modules/memory_store.py:364` `def recall_hybrid(query, top_k)`

## modules/metasploitable_gym.py
Depends on: `core/logging.py`, `modules/atomic_exploit_bridge.py`, `modules/chain_registry.py`
Imported by: `cli/commands/redteam_gym.py`, `modules/ctf_capture.py`, `tests/test_metasploitable_gym.py`
- `load_index` (function) `modules/metasploitable_gym.py:42` `def load_index(path)` -- Load the gym index, returning an empty mapping on failure.
- `vulnerabilities` (function) `modules/metasploitable_gym.py:47` `def vulnerabilities(path)` -- Return every indexed vulnerability.
- `get` (function) `modules/metasploitable_gym.py:53` `def get(vuln_id, path)` -- Return one vulnerability by id, or None.
- `chain_for` (function) `modules/metasploitable_gym.py:62` `def chain_for(vuln_id, path)` -- Return the resolved chain for one vulnerability, or None.
- `exploit_for` (function) `modules/metasploitable_gym.py:72` `def exploit_for(vuln_id, path)` -- Return the exploit spec for one vulnerability, or None.
- `validate_matrix` (function) `modules/metasploitable_gym.py:82` `def validate_matrix(path)` -- Validate the index, exploit files and chains as one matrix.
- `summary` (function) `modules/metasploitable_gym.py:138` `def summary(path)` -- Return counts by severity and service for operators.
- `main` (function) `modules/metasploitable_gym.py:157` `def main()` -- CLI: list | validate | info | chain.

## modules/metasploitable_migrations.py
Depends on: `core/safe_exec.py`
Imported by: `modules/lab_runtime.py`, `tests/test_metasploitable_migrations.py`
- `build_migrations` (function) `modules/metasploitable_migrations.py:194` `def build_migrations(subnet)` -- Return the ordered migration list with the docker subnet applied.
- `apply_migrations` (function) `modules/metasploitable_migrations.py:354` `def apply_migrations(container, subnet)` -- Run every migration on the gym container, skipping applied ones.

## modules/metrics.py
Depends on: `core/logging.py`
Imported by: `lazyc2.py`, `lazyown.py`, `modules/c2_builder.py`, `skills/autonomous_daemon.py`, `skills/mcp_tools/metrics_summary.py`, `tests/test_metrics.py`
- `MetricsRegistry.__init__` (method) `modules/metrics.py:63` `def __init__(self)` -- Create an empty registry with its own lock.
- `MetricsRegistry.inc` (method) `modules/metrics.py:69` `def inc(self, name, labels, value)` -- Increment the named counter for the given labels.
- `MetricsRegistry.get` (method) `modules/metrics.py:87` `def get(self, name, labels)` -- Return the current value of a counter.
- `MetricsRegistry.prometheus_text` (method) `modules/metrics.py:107` `def prometheus_text(self)` -- Render every counter in Prometheus text exposition format.
- `MetricRecord.to_dict` (method) `modules/metrics.py:167` `def to_dict(self)` -- Return the record as a JSON-serialisable dictionary.
- `MetricsWriter.__init__` (method) `modules/metrics.py:189` `def __init__(self, path)` -- Initialise the writer.
- `MetricsWriter.path` (method) `modules/metrics.py:201` `def path(self)` -- Return the JSONL destination path.
- `MetricsWriter.append` (method) `modules/metrics.py:206` `def append(self, record)` -- Append a single record to disk.
- `MetricsAggregator.summarize` (method) `modules/metrics.py:254` `def summarize(cls, records, window_seconds, now_utc)` -- Compute aggregate statistics over the supplied records.
- `MetricsRecorder.__init__` (method) `modules/metrics.py:339` `def __init__(self, writer)` -- Initialise the recorder.
- `MetricsRecorder.path` (method) `modules/metrics.py:350` `def path(self)` -- Return the JSONL path used by the underlying writer.
- `MetricsRecorder.record` (method) `modules/metrics.py:355` `def record(self, command, args, duration_ms, success, exit_code, source)` -- Persist a single command-execution telemetry record.
- `MetricsRecorder.summarize` (method) `modules/metrics.py:416` `def summarize(self, window_seconds)` -- Return aggregate statistics over recorded events.
- `MetricsRecorder.tail` (method) `modules/metrics.py:430` `def tail(self, n)` -- Return the most recent *n* records, newest first.
- `get_recorder` (function) `modules/metrics.py:452` `def get_recorder()` -- Return the process-wide :class:`MetricsRecorder` singleton.
- `reset_recorder_for_tests` (function) `modules/metrics.py:466` `def reset_recorder_for_tests(writer)` -- Replace the module-level recorder with a fresh instance.

## modules/mfa_bypass.py
Imported by: `cli/commands/cicd.py`
- `MFABypassEngine.__init__` (method) `modules/mfa_bypass.py:128` `def __init__(self, sessions_dir)`
- `MFABypassEngine.enumerate_techniques` (method) `modules/mfa_bypass.py:133` `def enumerate_techniques(self, target)` -- Enumerate viable MFA bypass techniques for a given target.
- `MFABypassEngine.generate_phishing_templates` (method) `modules/mfa_bypass.py:153` `def generate_phishing_templates(self, target)` -- Generate phishing templates tailored for MFA bypass.
- `MFABypassEngine.mfa_conditional_access_scan` (method) `modules/mfa_bypass.py:223` `def mfa_conditional_access_scan(self, domain)` -- Scan for conditional access policy gaps.
- `MFABypassEngine.replay_oauth_token` (method) `modules/mfa_bypass.py:252` `def replay_oauth_token(self, access_token, refresh_token)` -- Test if an OAuth2 token is still valid and can be replayed.
- `MFABypassEngine.saml_golden_ticket_check` (method) `modules/mfa_bypass.py:278` `def saml_golden_ticket_check(self, adfs_server)` -- Check for ADFS token signing certificate exposure.
- `MFABypassEngine.export_report` (method) `modules/mfa_bypass.py:303` `def export_report(self)` -- Export MFA bypass results to a JSON report.

## modules/module_registry.py
Depends on: `core/logging.py`, `modules/__init__.py`
Imported by: `cli/commands/marketplace.py`, `cli/commands/misc_migrated.py`, `cli/commands/module_manager.py`, `cli/commands/session_ops.py`, `modules/lazy_loop.py`, `modules/selection/module.py`, `skills/mcp_tools/list_modules.py`, `tests/test_module_registry.py`, `tests/test_module_registry_bridge.py`, `tests/test_selection_module.py`
- `ModuleInfo.__init__` (method) `modules/module_registry.py:216` `def __init__(self, name, module_type, author, version, description, category, path, source, params, enabled...`
- `ModuleInfo.to_dict` (method) `modules/module_registry.py:246` `def to_dict(self)`
- `ModuleRegistry.__init__` (method) `modules/module_registry.py:279` `def __init__(self, base_dir)`
- `ModuleRegistry.get_instance` (method) `modules/module_registry.py:285` `def get_instance(cls, base_dir)` -- Return the singleton registry instance.
- `ModuleRegistry.scan` (method) `modules/module_registry.py:291` `def scan(self)` -- Scan all module directories and return the full list.
- `ModuleRegistry.rescan` (method) `modules/module_registry.py:304` `def rescan(self)` -- Force a full rescan and return modules.
- `ModuleRegistry.get` (method) `modules/module_registry.py:313` `def get(self, name)` -- Get a module by name.
- `ModuleRegistry.search` (method) `modules/module_registry.py:319` `def search(self, query, module_type, category, enabled_only, include_deprecated)` -- Search indexed modules.
- `ModuleRegistry.deprecated_modules` (method) `modules/module_registry.py:359` `def deprecated_modules(self)` -- Return all deprecated modules.
- `ModuleRegistry.by_type` (method) `modules/module_registry.py:365` `def by_type(self, module_type)` -- Shorthand for ``search(module_type=module_type)``.
- `ModuleRegistry.summary` (method) `modules/module_registry.py:369` `def summary(self)` -- Return counts by module type.
- `ModuleRegistry.proposal_intents` (method) `modules/module_registry.py:378` `def proposal_intents(self, texts, target, limit)` -- Loop bridge: map corpus mentions onto runnable module intents.
- `format_module_table` (function) `modules/module_registry.py:666` `def format_module_table(modules, cols)` -- Format a list of modules as an aligned text table.
- `format_module_detail` (function) `modules/module_registry.py:713` `def format_module_detail(m)` -- Format a single module's full metadata.

## modules/moe_router.py
Depends on: `core/logging.py`, `modules/toposwarm_bridge.py`
Imported by: `modules/lesson_ingestor.py`, `modules/loop_ai_bridge.py`, `skills/swan_agent.py`, `tests/integration_autonomous_flow.py`, `tests/test_moe_rl_swan.py`, `tests/test_moe_router_check_regression.py`
- `ExpertProfile.is_local` (method) `modules/moe_router.py:96` `def is_local(self)`
- `ExpertPerformance.update` (method) `modules/moe_router.py:115` `def update(self, reward, detection_prob)`
- `IExpertSelector.select` (method) `modules/moe_router.py:261` `def select(self, candidates, task_type, performance_store, deterministic)` -- Return the selected expert from candidates.
- `ExpertPerformanceStore.__init__` (method) `modules/moe_router.py:283` `def __init__(self, path)`
- `ExpertPerformanceStore.record` (method) `modules/moe_router.py:298` `def record(self, expert_id, task_type, reward, detection_prob)` -- Update performance for (expert, task_type) and persist.
- `ExpertPerformanceStore.get` (method) `modules/moe_router.py:316` `def get(self, expert_id, task_type)`
- `ExpertPerformanceStore.all_for_task` (method) `modules/moe_router.py:321` `def all_for_task(self, task_type)`
- `ExpertPerformanceStore.performance_bonus` (method) `modules/moe_router.py:325` `def performance_bonus(self, expert_id, task_type)` -- Return a bonus scalar in [-0.3, +0.5] based on EMA reward history.
- `SoftmaxSelector.__init__` (method) `modules/moe_router.py:377` `def __init__(self, temperature)`
- `SoftmaxSelector.temperature` (method) `modules/moe_router.py:381` `def temperature(self)`
- `SoftmaxSelector.temperature` (method) `modules/moe_router.py:385` `def temperature(self, value)`
- `SoftmaxSelector.select` (method) `modules/moe_router.py:388` `def select(self, candidates, task_type, performance_store, deterministic)`
- `ExpertAvailabilityChecker.__init__` (method) `modules/moe_router.py:443` `def __init__(self)`
- `ExpertAvailabilityChecker.is_available` (method) `modules/moe_router.py:447` `def is_available(self, expert, api_key)`
- `MoERouter.__init__` (method) `modules/moe_router.py:500` `def __init__(self, experts, selector, performance_store, api_key)`
- `MoERouter.route` (method) `modules/moe_router.py:515` `def route(self, task_type, goal, deterministic)` -- Return the single best expert for the given task_type.
- `MoERouter.ensemble` (method) `modules/moe_router.py:547` `def ensemble(self, task_type, goal, n)` -- Return up to *n* distinct experts for ensemble execution.
- `adjusted_weight` (function) `modules/moe_router.py:562` `def adjusted_weight(ep)`
- `MoERouter.record_outcome` (method) `modules/moe_router.py:575` `def record_outcome(self, expert_id, task_type, reward, detection_prob)` -- Record the outcome of an expert execution.
- `MoERouter.top_experts_for_task` (method) `modules/moe_router.py:589` `def top_experts_for_task(self, task_type, top_k)` -- Return (expert, adjusted_weight) sorted descending for diagnostics.
- `MoERouter.get_expert` (method) `modules/moe_router.py:605` `def get_expert(self, expert_id)` -- Return expert by ID, or None.
- `MoERouter.status_report` (method) `modules/moe_router.py:609` `def status_report(self)` -- Return a diagnostic snapshot of all experts and their weights.
- `get_router` (function) `modules/moe_router.py:684` `def get_router(api_key)` -- Return (or create) the module-level singleton MoERouter.


Next: [API_p18.md](API_p18.md)
