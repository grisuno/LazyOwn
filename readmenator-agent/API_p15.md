# API (page 15 of 24)
Previous: [API_p14.md](API_p14.md)

## modules/llm_factory.py
Depends on: `core/llm_budget.py`, `modules/ai_model.py`, `modules/harness.py`, `modules/llm_client.py`, `modules/toposwarm_bridge.py`
Imported by: `cli/commands/ai.py`, `cli/wizard.py`, `contrib/legacy/lazyllmchat.py`, `core/payload_schema.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ai_fallback.py`, `modules/ai_model.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/llm_adapter.py`, `modules/mcp_agent_bridge.py`, `modules/privesc_predictor.py`, `modules/professional_report.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `tests/conftest.py`, `tests/test_ai_commands_llm.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_streaming.py`, `tests/test_llm_adapter_parity.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_llm_resilience.py`, `tests/test_payload_schema.py`, `tests/test_wizard_llm.py`
- `is_model_missing_error` (function) `modules/llm_factory.py:121` `def is_model_missing_error(message)` -- Return True when an error text means the model id is unavailable.
- `groq_model_chain` (function) `modules/llm_factory.py:141` `def groq_model_chain(config)` -- Return the ordered Groq model ids to try, configured model first.
- `default_model_for` (function) `modules/llm_factory.py:224` `def default_model_for(backend)` -- Return the default model identifier for a backend.
- `model_config_key` (function) `modules/llm_factory.py:245` `def model_config_key(backend)` -- Return the ``payload.json`` key holding a backend's model override.
- `api_key_config_key` (function) `modules/llm_factory.py:266` `def api_key_config_key(backend)` -- Return the ``payload.json`` key holding a backend's API key slot.
- `backend_requires_api_key` (function) `modules/llm_factory.py:291` `def backend_requires_api_key(backend)` -- Report whether a backend needs an API key to operate.
- `load_payload` (function) `modules/llm_factory.py:309` `def load_payload(payload_path)` -- Read ``payload.json`` from disk and return it as a dictionary.
- `get_llm_backend` (function) `modules/llm_factory.py:633` `def get_llm_backend(config, backend)` -- Return a concrete :class:`AIModel` selected by configuration.
- `get_llm_backend_raw` (function) `modules/llm_factory.py:729` `def get_llm_backend_raw(config, backend)` -- Return a raw :class:`AIModel` without the budget wrapper.
- `try_get_llm_backend` (function) `modules/llm_factory.py:751` `def try_get_llm_backend(config, backend)` -- Return a backend or ``None`` if construction fails for any reason.
- `stream_complete` (function) `modules/llm_factory.py:828` `def stream_complete(model, prompt, max_tokens, on_delta)` -- Completion that reports incremental deltas while it arrives.
- `complete` (function) `modules/llm_factory.py:899` `def complete(model, prompt, max_tokens)` -- Complete a prompt through one model spec; raise when unanswered.

## modules/llm_pool.py
Imported by: `cli/commands/ai.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_autonomous_ops.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_runner.py`
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
Imported by: `cli/commands/ai.py`, `modules/llm_adapter.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_prompts.py`
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
Imported by: `lazy_sentinel4.py`, `lazyc2.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/icmp_server.py`, `modules/lazyownerweb.py`, `modules/lilsplunky.py`, `modules/vulnbot.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`
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

## modules/loop_ai_bridge.py
Depends on: `modules/detection_oracle.py`, `modules/event_bus.py`, `modules/moe_router.py`, `modules/orchestrator_config.py`, `modules/rl_trainer.py`, `skills/hive_mind.py`, `skills/swan_agent.py`
Imported by: `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/mediation/telemetry_mediator.py`, `tests/conftest.py`, `tests/test_lazy_streaming.py`, `tests/test_loop_ai_bridge.py`, `tests/test_mediation.py`
- `publish_loop_event` (function) `modules/loop_ai_bridge.py:74` `def publish_loop_event(task_id, worker, kind, text, severity)` -- Publish one loop activity to the unified bus and Hive memory.
- `annotate_detection` (function) `modules/loop_ai_bridge.py:125` `def annotate_detection(command, action_category)` -- Return oracle details for one command, or None when unavailable.
- `moe_route` (function) `modules/loop_ai_bridge.py:149` `def moe_route(task_type, goal)` -- Return the MoE router's preferred expert for a task type, or None.
- `moe_record_outcome` (function) `modules/loop_ai_bridge.py:166` `def moe_record_outcome(expert_id, task_type, reward, detection_prob)` -- Feed one execution outcome back to the MoE performance store.
- `rl_select` (function) `modules/loop_ai_bridge.py:185` `def rl_select(task_type, phase, candidates, deterministic)` -- Pick an expert with the RL policy; first candidate when unavailable.
- `rl_update` (function) `modules/loop_ai_bridge.py:207` `def rl_update(task_type, phase, action, reward, candidates, detection_prob)` -- Apply one Q-learning update for an executed action.
- `rl_save` (function) `modules/loop_ai_bridge.py:230` `def rl_save()` -- Persist the RL tables after a run.
- `record_step` (function) `modules/loop_ai_bridge.py:249` `def record_step(task_id, worker, command, output, detection_prob)` -- Feed one executed command outcome to MoE and the RL trainer.
- `swan_available` (function) `modules/loop_ai_bridge.py:264` `def swan_available()` -- Return True when the SWAN orchestrator can be constructed.
- `swan_consult` (function) `modules/loop_ai_bridge.py:277` `def swan_consult(prompt, task_type, phase, timeout)` -- Ask SWAN for an ensemble answer; empty string when unavailable.
- `stream_enabled` (function) `modules/loop_ai_bridge.py:304` `def stream_enabled()` -- Return whether token streaming into the activity log is enabled.
- `ai_snapshot` (function) `modules/loop_ai_bridge.py:314` `def ai_snapshot()` -- Compact status of the wired AI stack for the operator log.

## modules/loop_guardrails.py
Imported by: `modules/lazy_loop.py`, `modules/lazy_runner.py`, `tests/test_loop_guardrails.py`
- `RepeatDetector.__init__` (method) `modules/loop_guardrails.py:89` `def __init__(self, window)`
- `RepeatDetector.record` (method) `modules/loop_guardrails.py:93` `def record(self, command)` -- Add one executed command; returns True when the window fills.
- `RepeatDetector.stuck` (method) `modules/loop_guardrails.py:110` `def stuck(self)` -- True when the window is full of one identical command.
- `RepeatDetector.last_commands` (method) `modules/loop_guardrails.py:117` `def last_commands(self)` -- Snapshot of the recent command window (oldest first).
- `RepeatDetector.reset` (method) `modules/loop_guardrails.py:121` `def reset(self)` -- Clear the window (operator intervention acknowledged).
- `EdrPacer.__init__` (method) `modules/loop_guardrails.py:135` `def __init__(self, duration_threshold)`
- `EdrPacer.observe` (method) `modules/loop_guardrails.py:141` `def observe(self, command, duration_sec, output)` -- Feed one executed step and update the telemetry estimate.
- `EdrPacer.decay` (method) `modules/loop_guardrails.py:163` `def decay(self, factor)` -- Cool the estimate down (call once per completed step).
- `EdrPacer.level` (method) `modules/loop_guardrails.py:169` `def level(self)` -- Current pacing level: 0 calm, 1 cautious, 2 stealth.
- `EdrPacer.signal` (method) `modules/loop_guardrails.py:179` `def signal(self)` -- Human-readable reason for the current level (may be empty).
- `EdrPacer.inter_step_delay` (method) `modules/loop_guardrails.py:184` `def inter_step_delay(self)` -- Recommended sleep before the next step at the current level.
- `EdrPacer.quieten` (method) `modules/loop_guardrails.py:192` `def quieten(self, command)` -- Return a quieter variant of the command at the current level.
- `TargetLimiter.__init__` (method) `modules/loop_guardrails.py:216` `def __init__(self, max_concurrent)`
- `TargetLimiter.max_concurrent` (method) `modules/loop_guardrails.py:223` `def max_concurrent(self)` -- Configured upper bound of simultaneous targets.
- `TargetLimiter.active_targets` (method) `modules/loop_guardrails.py:228` `def active_targets(self)` -- How many distinct targets currently hold a slot.
- `TargetLimiter.slot` (method) `modules/loop_guardrails.py:234` `def slot(self, target)` -- Hold one of at most ``max_concurrent`` target slots.
- `FactVectorStore.__init__` (method) `modules/loop_guardrails.py:286` `def __init__(self, path, max_facts)`
- `FactVectorStore.path` (method) `modules/loop_guardrails.py:294` `def path(self)` -- Backing file path.
- `FactVectorStore.add` (method) `modules/loop_guardrails.py:315` `def add(self, text, meta)` -- Embed and store one fact; returns False for duplicates.
- `FactVectorStore.search` (method) `modules/loop_guardrails.py:349` `def search(self, query, k)` -- Return the ``k`` facts most similar to the query.
- `FactVectorStore.search_block` (method) `modules/loop_guardrails.py:379` `def search_block(self, query, k, max_chars)` -- Render retrieved facts as a prompt-ready block (may be empty).
- `FactVectorStore.clear` (method) `modules/loop_guardrails.py:388` `def clear(self)` -- Drop every fact (manual reset path).
- `FactVectorStore.save` (method) `modules/loop_guardrails.py:394` `def save(self)` -- Persist atomically; I/O errors never surface to the loop.

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
Depends on: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`
Imported by: `cli/orchestrator_assets_tabs.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`, `tests/test_orchestrator_triggers.py`, `tests/test_trigger_policy.py`
- `TriggerStore.__init__` (method) `modules/loop_triggers.py:26` `def __init__(self, task_id)` -- Bind trigger table (global when task_id empty).
- `TriggerStore.add` (method) `modules/loop_triggers.py:36` `def add(self, kind, arg, every_sec)` -- Register a trigger; interval needs every_sec, events fire on new rows.
- `TriggerStore.upsert_defaults` (method) `modules/loop_triggers.py:58` `def upsert_defaults(self, seeds)` -- Merge declarative seeds without duplicating or re-enabling.
- `TriggerStore.remove` (method) `modules/loop_triggers.py:100` `def remove(self, trigger_id)` -- Delete a trigger.
- `TriggerStore.set_enabled` (method) `modules/loop_triggers.py:111` `def set_enabled(self, trigger_id, enabled)` -- Flip one trigger's enabled flag in place.
- `TriggerStore.list` (method) `modules/loop_triggers.py:125` `def list(self)` -- Return all triggers.
- `TriggerStore.ensure_service_trigger` (method) `modules/loop_triggers.py:129` `def ensure_service_trigger(self)` -- Register the catalog trigger once so services fire the loop.
- `TriggerStore.due` (method) `modules/loop_triggers.py:142` `def due(self, task_id, graph, activity, assets, store)` -- Evaluate triggers like the scheduler tick; fires at most once each.

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
Imported by: `modules/unified_bridge.py`, `skills/lazyown_mcp.py`
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
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `MediationDomains.is_known` (method) `modules/mediation/contracts.py:23` `def is_known(cls, domain)` -- Check whether a domain key is registered in the default set.
- `ActivityLogPort.read` (method) `modules/mediation/contracts.py:44` `def read(self, limit)` -- Return the latest activity records oldest-first.
- `LlmCompletionPort.complete` (method) `modules/mediation/contracts.py:60` `def complete(self, prompt, max_tokens, task_id)` -- Complete one prompt with the configured LLM pool.
- `LlmCompletionPort.has_members` (method) `modules/mediation/contracts.py:78` `def has_members(self)` -- Report whether any LLM member is configured.
- `MediatorContract.describe` (method) `modules/mediation/contracts.py:89` `def describe(self)` -- Return introspection metadata for diagnostics.
- `MediationHubContract.mediator_for` (method) `modules/mediation/contracts.py:98` `def mediator_for(self, domain)` -- Return the mediator registered for a domain key, or None.
- `resolve` (function) `modules/mediation/contracts.py:103` `def resolve(domain)` -- Return the default-hub mediator for a domain key.

## modules/mediation/feedback_mediator.py
Depends on: `modules/lazy_orchestrator_feedback.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
- `FeedbackMediator.describe` (method) `modules/mediation/feedback_mediator.py:18` `def describe(self)` -- Return mediator metadata for diagnostics.
- `FeedbackMediator.order_steps` (method) `modules/mediation/feedback_mediator.py:22` `def order_steps(self, steps, stack)` -- Reorder worker steps with cross-task priors.

## modules/mediation/hub.py
Depends on: `modules/mediation/chain_mediator.py`, `modules/mediation/contracts.py`, `modules/mediation/feedback_mediator.py`, `modules/mediation/intel_mediator.py`, `modules/mediation/telemetry_mediator.py`
Imported by: `modules/mediation/__init__.py`, `modules/mediation/contracts.py`, `tests/test_mediation.py`
- `MediationHub.__init__` (method) `modules/mediation/hub.py:22` `def __init__(self)` -- Start with an empty registry.
- `MediationHub.register` (method) `modules/mediation/hub.py:26` `def register(self, mediator)` -- Register a mediator under its declared domain.
- `MediationHub.mediator_for` (method) `modules/mediation/hub.py:35` `def mediator_for(self, domain)` -- Return the mediator registered for a domain key, or None.
- `MediationHub.snapshot` (method) `modules/mediation/hub.py:46` `def snapshot(self)` -- Return high-level metadata for every registered mediator.
- `default_hub` (function) `modules/mediation/hub.py:73` `def default_hub()` -- Return a fresh default-configured hub (test-safe, no singleton).
- `get_hub` (function) `modules/mediation/hub.py:78` `def get_hub()` -- Return the process-wide hub, building it on first use.

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
- `TelemetryMediator.record_step` (method) `modules/mediation/telemetry_mediator.py:59` `def record_step(self, task_id, worker, command, output, detection_prob)` -- Record one executed step for learning stores.
- `TelemetryMediator.swan_available` (method) `modules/mediation/telemetry_mediator.py:76` `def swan_available(self)` -- Return True when the SWAN ensemble is ready.
- `TelemetryMediator.swan_consult` (method) `modules/mediation/telemetry_mediator.py:85` `def swan_consult(self, prompt, task_type, phase, timeout)` -- Consult the SWAN ensemble with one prompt.
- `TelemetryMediator.moe_route` (method) `modules/mediation/telemetry_mediator.py:110` `def moe_route(self, task_type)` -- Return the preferred MoE expert for a task type.
- `TelemetryMediator.rl_select` (method) `modules/mediation/telemetry_mediator.py:126` `def rl_select(self, task_type, phase, candidates, deterministic)` -- Return the RL-preferred candidate name.
- `TelemetryMediator.moe_record_outcome` (method) `modules/mediation/telemetry_mediator.py:151` `def moe_record_outcome(self, expert_id, task_type, reward, detection_prob)` -- Record one MoE outcome for learning.
- `TelemetryMediator.rl_update` (method) `modules/mediation/telemetry_mediator.py:167` `def rl_update(self, task_type, phase, action, reward, candidates, detection_prob)` -- Apply one Q-learning update for an executed action.

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
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`, `tests/test_memory_semantics.py`
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
Imported by: `lazyc2.py`, `lazyown.py`, `modules/c2_builder.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_metrics.py`
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
Depends on: `core/logging.py`
Imported by: `cli/commands/marketplace.py`, `cli/commands/misc_migrated.py`, `cli/commands/module_manager.py`, `cli/commands/session_ops.py`, `skills/lazyown_mcp.py`, `tests/test_module_registry.py`
- `ModuleInfo.__init__` (method) `modules/module_registry.py:172` `def __init__(self, name, module_type, author, version, description, category, path, source, params, enabled...`
- `ModuleInfo.to_dict` (method) `modules/module_registry.py:202` `def to_dict(self)`
- `ModuleRegistry.__init__` (method) `modules/module_registry.py:235` `def __init__(self, base_dir)`
- `ModuleRegistry.get_instance` (method) `modules/module_registry.py:241` `def get_instance(cls, base_dir)` -- Return the singleton registry instance.
- `ModuleRegistry.scan` (method) `modules/module_registry.py:247` `def scan(self)` -- Scan all module directories and return the full list.
- `ModuleRegistry.rescan` (method) `modules/module_registry.py:260` `def rescan(self)` -- Force a full rescan and return modules.
- `ModuleRegistry.get` (method) `modules/module_registry.py:269` `def get(self, name)` -- Get a module by name.
- `ModuleRegistry.search` (method) `modules/module_registry.py:275` `def search(self, query, module_type, category, enabled_only, include_deprecated)` -- Search indexed modules.
- `ModuleRegistry.deprecated_modules` (method) `modules/module_registry.py:315` `def deprecated_modules(self)` -- Return all deprecated modules.
- `ModuleRegistry.by_type` (method) `modules/module_registry.py:321` `def by_type(self, module_type)` -- Shorthand for ``search(module_type=module_type)``.
- `ModuleRegistry.summary` (method) `modules/module_registry.py:325` `def summary(self)` -- Return counts by module type.
- `format_module_table` (function) `modules/module_registry.py:542` `def format_module_table(modules, cols)` -- Format a list of modules as an aligned text table.
- `format_module_detail` (function) `modules/module_registry.py:589` `def format_module_detail(m)` -- Format a single module's full metadata.

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

## modules/morse.py
- `reverse_morse_code` (function) `modules/morse.py:98` `def reverse_morse_code()` -- Build the reverse lookup table from Morse code to characters.
- `text_to_morse` (function) `modules/morse.py:109` `def text_to_morse(text, config)` -- Convert plain text to Morse code.
- `morse_to_text` (function) `modules/morse.py:130` `def morse_to_text(morse_code, config)` -- Convert Morse code back to plain text.
- `clear_screen` (function) `modules/morse.py:157` `def clear_screen(config)` -- Reset the terminal screen using a bounded subprocess call.
- `read_choice` (function) `modules/morse.py:171` `def read_choice(config)` -- Read and validate the menu choice from standard input.
- `run_driver` (function) `modules/morse.py:186` `def run_driver(config)` -- Run the interactive Morse code conversion loop.

## modules/mysql_hookandroot_lib.c
- `reverse_shell` (function) `modules/mysql_hookandroot_lib.c:74` `void reverse_shell(void)` -- fork & send a bash shell to the attacker before starting mysqld
- `execvp` (function) `modules/mysql_hookandroot_lib.c:128` `int execvp(const char* filename, char* const argv[])` -- execvp() hook

## modules/network_opsec.py
Imported by: `cli/commands/opsec_cleanup.py`
- `NetworkOpsecEngine.__init__` (method) `modules/network_opsec.py:83` `def __init__(self, config)`
- `NetworkOpsecEngine.configure_proxy_chain` (method) `modules/network_opsec.py:87` `def configure_proxy_chain(self, chain_type)` -- Configure a proxy chain for C2 communication.
- `NetworkOpsecEngine.check_canary_tokens` (method) `modules/network_opsec.py:131` `def check_canary_tokens(self)` -- Check if the target has canary token / deception technology.
- `NetworkOpsecEngine.analyze_traffic_with_canary_check` (method) `modules/network_opsec.py:179` `def analyze_traffic_with_canary_check(self, target_host, target_port)` -- Analyze whether target traffic is being intercepted or analyzed.
- `NetworkOpsecEngine.dns_over_https_config` (method) `modules/network_opsec.py:246` `def dns_over_https_config(self)` -- Generate DNS-over-HTTPS configuration for proxy and system.
- `NetworkOpsecEngine.source_port_randomize` (method) `modules/network_opsec.py:269` `def source_port_randomize(self)` -- Randomize source port for outbound connections.
- `NetworkOpsecEngine.connection_jitter_schedule` (method) `modules/network_opsec.py:294` `def connection_jitter_schedule(self, beacon_interval)` -- Generate a jitter schedule for beacon connections.
- `NetworkOpsecEngine.canary_detection_setup` (method) `modules/network_opsec.py:317` `def canary_detection_setup(self)` -- Set up canary detection for the engagement.
- `NetworkOpsecEngine.summary` (method) `modules/network_opsec.py:349` `def summary(self)`

## modules/nmap2csv.py
- `dottedquad_to_num` (function) `modules/nmap2csv.py:126` `def dottedquad_to_num(ip)` -- Convert decimal dotted quad string IP to long integer
- `num_to_dottedquad` (function) `modules/nmap2csv.py:133` `def num_to_dottedquad(n)` -- Convert long int IP to dotted quad string
- `unique_match_from_list` (function) `modules/nmap2csv.py:140` `def unique_match_from_list(list)` -- Check the list for a potential pattern match
- `extract_matching_pattern` (function) `modules/nmap2csv.py:156` `def extract_matching_pattern(regex, group_name, unfiltered_list)` -- Return the desired group_name from a list of matching patterns
- `Host.__init__` (method) `modules/nmap2csv.py:177` `def __init__(self, ip, fqdn)`
- `Host.add_port` (method) `modules/nmap2csv.py:188` `def add_port(self, port)`
- `Host.get_ip_num_format` (method) `modules/nmap2csv.py:192` `def get_ip_num_format(self)`
- `Host.get_ip_dotted_format` (method) `modules/nmap2csv.py:195` `def get_ip_dotted_format(self)`
- `Host.get_fqdn` (method) `modules/nmap2csv.py:198` `def get_fqdn(self)`
- `Host.get_rdns_record` (method) `modules/nmap2csv.py:201` `def get_rdns_record(self)`
- `Host.get_port_list` (method) `modules/nmap2csv.py:204` `def get_port_list(self)`
- `Host.get_port_number_list` (method) `modules/nmap2csv.py:207` `def get_port_number_list(self)`
- `Host.get_port_protocol_list` (method) `modules/nmap2csv.py:216` `def get_port_protocol_list(self)`
- `Host.get_port_service_list` (method) `modules/nmap2csv.py:225` `def get_port_service_list(self)`
- `Host.get_port_version_list` (method) `modules/nmap2csv.py:234` `def get_port_version_list(self)`
- `Host.get_port_script_list` (method) `modules/nmap2csv.py:243` `def get_port_script_list(self)`
- `Host.get_os` (method) `modules/nmap2csv.py:252` `def get_os(self)`
- `Host.get_mac_address` (method) `modules/nmap2csv.py:255` `def get_mac_address(self)`
- `Host.get_mac_address_vendor` (method) `modules/nmap2csv.py:258` `def get_mac_address_vendor(self)`
- `Host.get_network_distance` (method) `modules/nmap2csv.py:261` `def get_network_distance(self)`
- `Host.set_fqdn` (method) `modules/nmap2csv.py:265` `def set_fqdn(self, fqdn)`
- `Host.set_rdns_record` (method) `modules/nmap2csv.py:268` `def set_rdns_record(self, rdns_record)`
- `Host.set_os` (method) `modules/nmap2csv.py:271` `def set_os(self, os)`
- `Host.set_mac` (method) `modules/nmap2csv.py:274` `def set_mac(self, mac_address, mac_address_vendor)`
- `Host.set_network_distance` (method) `modules/nmap2csv.py:278` `def set_network_distance(self, network_distance)`
- `Port.__init__` (method) `modules/nmap2csv.py:283` `def __init__(self, number, protocol, service, version, script)`
- `Port.get_number` (method) `modules/nmap2csv.py:290` `def get_number(self)`
- `Port.get_protocol` (method) `modules/nmap2csv.py:293` `def get_protocol(self)`
- `Port.get_service` (method) `modules/nmap2csv.py:296` `def get_service(self)`
- `Port.get_version` (method) `modules/nmap2csv.py:299` `def get_version(self)`
- `Port.get_script` (method) `modules/nmap2csv.py:302` `def get_script(self)`
- `Port.set_service` (method) `modules/nmap2csv.py:305` `def set_service(self, service)`
- `Port.set_version` (method) `modules/nmap2csv.py:308` `def set_version(self, version)`
- `Port.set_script` (method) `modules/nmap2csv.py:311` `def set_script(self, script)`
- `split_grepable_match` (function) `modules/nmap2csv.py:315` `def split_grepable_match(raw_string)` -- Split the raw line to a neat Host object
- `parse` (function) `modules/nmap2csv.py:362` `def parse(fd)` -- Parse the data according to several regexes
- `parse_xml` (function) `modules/nmap2csv.py:492` `def parse_xml(xml_file)` -- Parse the XML file
- `is_format_valid` (function) `modules/nmap2csv.py:572` `def is_format_valid(fmt)` -- Check for the supplied custom output format
- `formatted_item` (function) `modules/nmap2csv.py:606` `def formatted_item(host, format_item)` -- return the attribute value related to the host
- `repeat_attributes` (function) `modules/nmap2csv.py:639` `def repeat_attributes(attribute_list)` -- repeat attribute lists to the maximum for the
- `generate_csv` (function) `modules/nmap2csv.py:653` `def generate_csv(fd, results, options)` -- Generate a plain ';' separated csv file with the desired or default attribute format
- `main` (function) `modules/nmap2csv.py:688` `def main()`

## modules/notify.py
Imported by: `modules/custom_tools.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `static/js/chart.min.js`, `tests/test_autonomous_ops.py`, `tests/test_lazy_loop.py`, `tests/test_security_codeql_batch.py`
- `severity_rank` (function) `modules/notify.py:31` `def severity_rank(severity, config)` -- Return the comparable order for a severity label.
- `mask_secrets` (function) `modules/notify.py:39` `def mask_secrets(text, config)` -- Replace known secret prefixes with a redaction marker.
- `url_allowed` (function) `modules/notify.py:57` `def url_allowed(url)` -- SSRF dial-guard for webhook delivery (LAZY parity).
- `post_url_validated` (function) `modules/notify.py:145` `def post_url_validated(url, data, timeout)` -- POST data to a webhook URL after SSRF validation, guarding redirects.
- `_GuardRedirect.redirect_request` (method) `modules/notify.py:159` `def redirect_request(self, req, fp, code, msg, headers, newurl)`
- `Notifier.__init__` (method) `modules/notify.py:207` `def __init__(self, config)` -- Initialize with shared notification constants.
- `Notifier.should_send` (method) `modules/notify.py:215` `def should_send(self, message, channel)` -- Apply event, severity, keyword and scope gates (LAZY parity).
- `Notifier.render` (method) `modules/notify.py:238` `def render(self, message)` -- Render masked Markdown text for a message.
- `Notifier.dispatch` (method) `modules/notify.py:244` `def dispatch(self, message, channels)` -- Fan out to eligible channels and journal deliveries.
- `Notifier.flush_digest` (method) `modules/notify.py:260` `def flush_digest(self, max_age_sec)` -- Emit one digest per channel when due (default 30m, LAZY parity).

## modules/nuclei_templates_sync.py
- `repo_root` (function) `modules/nuclei_templates_sync.py:39` `def repo_root()` -- Return the LazyOwn repository root derived from this file location.
- `canonical_dest` (function) `modules/nuclei_templates_sync.py:48` `def canonical_dest(subdir)` -- Return the canonical marketplace destination for a source.
- `run` (function) `modules/nuclei_templates_sync.py:60` `def run(argv, cwd)` -- Run a subprocess capturing output as text without raising.
- `ensure_git_available` (function) `modules/nuclei_templates_sync.py:73` `def ensure_git_available()` -- Abort with a clear message when the git binary is missing.
- `clone_templates` (function) `modules/nuclei_templates_sync.py:84` `def clone_templates(repo, staging)` -- Shallow-clone the template repository into the staging directory.
- `strip_git_traces` (function) `modules/nuclei_templates_sync.py:113` `def strip_git_traces(tree)` -- Remove every .git file or directory under the staged tree.
- `count_templates` (function) `modules/nuclei_templates_sync.py:132` `def count_templates(tree)` -- Count Nuclei template files under a directory tree.
- `replace_dest` (function) `modules/nuclei_templates_sync.py:144` `def replace_dest(src, dest, expected)` -- Atomically replace the destination with the staged tree contents.
- `same_remote` (function) `modules/nuclei_templates_sync.py:168` `def same_remote(path, repo)` -- Check whether an existing clone points at the expected remote.
- `normalize` (function) `modules/nuclei_templates_sync.py:179` `def normalize(url)`
- `refresh_existing_clone` (function) `modules/nuclei_templates_sync.py:188` `def refresh_existing_clone(path, repo)` -- Fast-forward an existing clean clone of the same remote.
- `validate_subset` (function) `modules/nuclei_templates_sync.py:209` `def validate_subset(dest, subset)` -- Validate a template subset with the nuclei binary when available.
- `build_parser` (function) `modules/nuclei_templates_sync.py:238` `def build_parser()` -- Build the command line parser for the sync script.
- `sync` (function) `modules/nuclei_templates_sync.py:263` `def sync(name, repo, dest, refresh_existing, skip_validate)` -- Clone, clean, and install one template source.
- `resolve_plan` (function) `modules/nuclei_templates_sync.py:308` `def resolve_plan(args)` -- Resolve the requested sources into (name, repo, dest) work items.
- `main` (function) `modules/nuclei_templates_sync.py:337` `def main(argv)` -- Entry point for the template sync script.


Next: [API_p16.md](API_p16.md)
