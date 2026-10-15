# API (page 14 of 22)
Previous: [API_p13.md](API_p13.md)

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
Imported by: `modules/lazy_agent.py`, `modules/lazy_loop.py`, `tests/conftest.py`, `tests/test_lazy_streaming.py`, `tests/test_loop_ai_bridge.py`
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

## modules/memory_cleaner.py
Imported by: `cli/commands/opsec_cleanup.py`
- `MemoryCleaner.__init__` (method) `modules/memory_cleaner.py:61` `def __init__(self, config)`
- `MemoryCleaner.windows_memory_cleanup` (method) `modules/memory_cleaner.py:64` `def windows_memory_cleanup(self)` -- Generate Windows memory artifact cleanup commands.
- `MemoryCleaner.linux_memory_cleanup` (method) `modules/memory_cleaner.py:151` `def linux_memory_cleanup(self)` -- Generate Linux memory artifact cleanup commands.
- `MemoryCleaner.macos_memory_cleanup` (method) `modules/memory_cleaner.py:206` `def macos_memory_cleanup(self)` -- Generate macOS memory artifact cleanup commands.
- `MemoryCleaner.generate_on_exit_script` (method) `modules/memory_cleaner.py:255` `def generate_on_exit_script(self)` -- Generate an on-exit cleanup script for beacons.

## modules/memory_store.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `StorageBackend.save` (method) `modules/memory_store.py:96` `def save(self, entry)`
- `StorageBackend.search` (method) `modules/memory_store.py:99` `def search(self, query, top_k)`
- `StorageBackend.by_host` (method) `modules/memory_store.py:102` `def by_host(self, host, top_k)`
- `StorageBackend.by_service` (method) `modules/memory_store.py:105` `def by_service(self, service, top_k)`
- `StorageBackend.all_entries` (method) `modules/memory_store.py:108` `def all_entries(self, limit)`
- `StorageBackend.close` (method) `modules/memory_store.py:111` `def close(self)`
- `SQLiteBackend.__init__` (method) `modules/memory_store.py:130` `def __init__(self, db_path)`
- `SQLiteBackend.save` (method) `modules/memory_store.py:145` `def save(self, entry)`
- `SQLiteBackend.search` (method) `modules/memory_store.py:177` `def search(self, query, top_k)`
- `SQLiteBackend.by_host` (method) `modules/memory_store.py:189` `def by_host(self, host, top_k)`
- `SQLiteBackend.by_service` (method) `modules/memory_store.py:200` `def by_service(self, service, top_k)`
- `SQLiteBackend.all_entries` (method) `modules/memory_store.py:212` `def all_entries(self, limit)`
- `SQLiteBackend.stats_raw` (method) `modules/memory_store.py:222` `def stats_raw(self)`
- `SQLiteBackend.close` (method) `modules/memory_store.py:229` `def close(self)`
- `MemoryStore.__init__` (method) `modules/memory_store.py:237` `def __init__(self, backend)`
- `MemoryStore.remember` (method) `modules/memory_store.py:240` `def remember(self, session_id, host, tool, command, output, findings, success)`
- `MemoryStore.recall` (method) `modules/memory_store.py:267` `def recall(self, query, top_k)`
- `MemoryStore.recall_by_host` (method) `modules/memory_store.py:270` `def recall_by_host(self, host, top_k)`
- `MemoryStore.recall_for_service` (method) `modules/memory_store.py:273` `def recall_for_service(self, service_name, top_k)`
- `MemoryStore.stats` (method) `modules/memory_store.py:276` `def stats(self)`
- `MemoryStore.export_finetuning_dataset` (method) `modules/memory_store.py:284` `def export_finetuning_dataset(self, path)`
- `get_memory_store` (function) `modules/memory_store.py:303` `def get_memory_store()`
- `remember` (function) `modules/memory_store.py:312` `def remember(session_id, host, tool, command, output, findings, success)`
- `recall` (function) `modules/memory_store.py:324` `def recall(query, top_k)`

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

## modules/obs_parser.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `modules/intelligence_engine.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`, `tests/test_daemon_loop.py`, `tests/test_phase1_data_gaps.py`
- `Observation.by_type` (method) `modules/obs_parser.py:83` `def by_type(self, ftype)`
- `Observation.has` (method) `modules/obs_parser.py:86` `def has(self, ftype)`
- `Extractor.extract` (method) `modules/obs_parser.py:99` `def extract(self, text, host)` -- Return all findings of this type found in *text*.
- `_ExtractorRegistry.__init__` (method) `modules/obs_parser.py:106` `def __init__(self)`
- `_ExtractorRegistry.register` (method) `modules/obs_parser.py:109` `def register(self, extractor)`
- `_ExtractorRegistry.run_all` (method) `modules/obs_parser.py:112` `def run_all(self, text, host)`
- `_IPExtractor.extract` (method) `modules/obs_parser.py:134` `def extract(self, text, host)`
- `_CredentialExtractor.extract` (method) `modules/obs_parser.py:175` `def extract(self, text, host)`
- `_ServiceVersionExtractor.extract` (method) `modules/obs_parser.py:198` `def extract(self, text, host)`
- `_PathExtractor.extract` (method) `modules/obs_parser.py:224` `def extract(self, text, host)`
- `_UsernameExtractor.extract` (method) `modules/obs_parser.py:245` `def extract(self, text, host)`
- `_HashExtractor.extract` (method) `modules/obs_parser.py:271` `def extract(self, text, host)`
- `_CVEExtractor.extract` (method) `modules/obs_parser.py:288` `def extract(self, text, host)`
- `_DomainExtractor.extract` (method) `modules/obs_parser.py:305` `def extract(self, text, host)`
- `_EmailExtractor.extract` (method) `modules/obs_parser.py:323` `def extract(self, text, host)`
- `_ErrorExtractor.extract` (method) `modules/obs_parser.py:345` `def extract(self, text, host)`
- `_CloudIdentityExtractor.extract` (method) `modules/obs_parser.py:367` `def extract(self, text, host)`
- `_SuccessDetector.is_success` (method) `modules/obs_parser.py:407` `def is_success(self, text)`
- `ObsParser.__init__` (method) `modules/obs_parser.py:431` `def __init__(self)`
- `ObsParser.register` (method) `modules/obs_parser.py:450` `def register(self, extractor)` -- Register an additional Extractor (Open/Closed extension point).
- `ObsParser.parse` (method) `modules/obs_parser.py:454` `def parse(self, output, host, tool)` -- Parse *output* and return an Observation.
- `get_parser` (function) `modules/obs_parser.py:500` `def get_parser()` -- Return (or create) the module-level singleton ObsParser.
- `parse` (function) `modules/obs_parser.py:508` `def parse(output, host, tool)` -- Module-level convenience wrapper.

## modules/operation.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/apt_playbooks.py`, `modules/obs_parser.py`, `modules/playbook_engine.py`, `modules/world_model.py`
Imported by: `cli/commands/caldera.py`
- `Operation.to_dict` (method) `modules/operation.py:98` `def to_dict(self)`
- `Operation.from_dict` (method) `modules/operation.py:116` `def from_dict(cls, d)`
- `Operation.save` (method) `modules/operation.py:134` `def save(self)`
- `Operation.log_event` (method) `modules/operation.py:143` `def log_event(self, step_index, step_name, status, summary, findings_count, error)`
- `Operation.record_facts` (method) `modules/operation.py:164` `def record_facts(self, findings)`
- `OperationManager.__init__` (method) `modules/operation.py:183` `def __init__(self)`
- `OperationManager.list` (method) `modules/operation.py:187` `def list(self)` -- List all persisted operations.
- `OperationManager.get` (method) `modules/operation.py:199` `def get(self, op_id)`
- `OperationManager.create` (method) `modules/operation.py:206` `def create(self, name, target, apt_name, description)` -- Create a new planned operation.
- `OperationManager.plan_from_apt` (method) `modules/operation.py:225` `def plan_from_apt(self, op, playbook_yaml_path)` -- Populate steps from an APT playbook YAML (or fall back to a derived MITRE playbook).
- `OperationManager.start` (method) `modules/operation.py:287` `def start(self, op_id, executor)` -- Start or resume a planned operation.
- `OperationManager.pause` (method) `modules/operation.py:369` `def pause(self, op_id)`
- `OperationManager.resume` (method) `modules/operation.py:378` `def resume(self, op_id, executor)`
- `OperationManager.stop` (method) `modules/operation.py:386` `def stop(self, op_id)`
- `OperationManager.status` (method) `modules/operation.py:396` `def status(self, op_id)` -- Return a structured status dict for an operation.
- `OperationManager.timeline` (method) `modules/operation.py:425` `def timeline(self, op_id)`
- `OperationManager.report` (method) `modules/operation.py:431` `def report(self, op_id)`
- `get_manager` (function) `modules/operation.py:471` `def get_manager()` -- Return a fresh :class:`OperationManager`.

## modules/operator_profiles.py
Depends on: `core/config.py`, `core/logging.py`
Imported by: `cli/commands/automation.py`
- `OperatorProfile.to_dict` (method) `modules/operator_profiles.py:57` `def to_dict(self)`
- `OperatorProfileManager.__init__` (method) `modules/operator_profiles.py:88` `def __init__(self)`
- `OperatorProfileManager.create_profile` (method) `modules/operator_profiles.py:192` `def create_profile(self, username, display_name, role, lhost, lport, listener_port, c2_port, c2_malleable_route...` -- Create a new operator profile.
- `OperatorProfileManager.load_profile` (method) `modules/operator_profiles.py:260` `def load_profile(self, username)` -- Load an operator profile.
- `OperatorProfileManager.update_profile` (method) `modules/operator_profiles.py:276` `def update_profile(self, username)` -- Update fields on an existing profile.
- `OperatorProfileManager.delete_profile` (method) `modules/operator_profiles.py:289` `def delete_profile(self, username)` -- Delete an operator profile and its directory.
- `OperatorProfileManager.list_profiles` (method) `modules/operator_profiles.py:300` `def list_profiles(self)` -- Return all operator profiles.
- `OperatorProfileManager.touch_activity` (method) `modules/operator_profiles.py:312` `def touch_activity(self, username)` -- Update last_active timestamp.
- `OperatorProfileManager.set_attribute` (method) `modules/operator_profiles.py:319` `def set_attribute(self, username, key, value)` -- Set a custom attribute on an operator profile.
- `OperatorProfileManager.get_attribute` (method) `modules/operator_profiles.py:328` `def get_attribute(self, username, key, default)` -- Get a custom attribute from an operator profile.
- `OperatorProfileManager.log_action` (method) `modules/operator_profiles.py:335` `def log_action(self, username, action, details)` -- Append an audited action to the operator's audit log.
- `OperatorProfileManager.effective_config` (method) `modules/operator_profiles.py:360` `def effective_config(self, username)` -- Merge team baseline (payload.json) with per-operator overrides.
- `get_operator_profile_manager` (function) `modules/operator_profiles.py:398` `def get_operator_profile_manager()` -- Return the singleton :class:`OperatorProfileManager`.

## modules/opsec_scorer.py
Depends on: `cli/commands/enum.py`, `core/config.py`, `core/logging.py`, `modules/db.py`, `modules/killchain.py`
Imported by: `cli/commands/opsec_cleanup.py`, `cli/commands/security.py`, `tests/test_opsec_scorer.py`, `tests/test_opsec_scorer_consolidated.py`
- `OpsecScore.to_dict` (method) `modules/opsec_scorer.py:288` `def to_dict(self)` -- Return the score serialized as a plain dictionary.
- `OpsecScorer.__init__` (method) `modules/opsec_scorer.py:343` `def __init__(self, payload, world_model)`
- `OpsecScorer.evasion_active` (method) `modules/opsec_scorer.py:352` `def evasion_active(self)`
- `OpsecScorer.traffic_morphing_active` (method) `modules/opsec_scorer.py:357` `def traffic_morphing_active(self)`
- `OpsecScorer.score` (method) `modules/opsec_scorer.py:365` `def score(self, command, rhost, phase_override)` -- Score an OPSEC risk for ``command`` against ``rhost``.
- `OpsecScorer.score_batch` (method) `modules/opsec_scorer.py:413` `def score_batch(self, commands, rhost)` -- Score multiple commands and return {command: OpsecScore}.
- `OpsecScorer.suggest_mitigations` (method) `modules/opsec_scorer.py:417` `def suggest_mitigations(self, command, detectable_by)` -- Return mitigation suggestions for a given command.
- `OpsecScorerV2.__init__` (method) `modules/opsec_scorer.py:617` `def __init__(self, context)`
- `OpsecScorerV2.assess` (method) `modules/opsec_scorer.py:622` `def assess(self, command, extra_context)` -- Assess OPSEC risk for a command in the current context.
- `OpsecScorerV2.should_allow` (method) `modules/opsec_scorer.py:696` `def should_allow(self, command)` -- Quick gating check - returns (allowed, score).
- `OpsecScorerV2.get_trend` (method) `modules/opsec_scorer.py:709` `def get_trend(self)` -- Analyze OPSEC risk trend over the session.
- `score_command` (function) `modules/opsec_scorer.py:811` `def score_command(command, payload, rhost)` -- Convenience function: score a single command without creating a scorer instance.

## modules/orchestrator_config.py
Depends on: `core/config.py`, `modules/auto_registry.py`
Imported by: `cli/commands/lazyops.py`, `cli/lazy_orchestrator.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/loop_ai_bridge.py`, `tests/test_lazy_orchestrator.py`
- `stages` (function) `modules/orchestrator_config.py:105` `def stages()` -- Merged stage view: enabled flag, label and firing condition.
- `stage_enabled` (function) `modules/orchestrator_config.py:130` `def stage_enabled(name)` -- Return whether one pipeline stage is enabled (unknown = enabled).
- `set_stage` (function) `modules/orchestrator_config.py:136` `def set_stage(name, enabled)` -- Persist the enabled flag of one stage.
- `effective_verbs` (function) `modules/orchestrator_config.py:161` `def effective_verbs()` -- Merged auto-verb view: built-ins plus operator overrides and additions.
- `verb_config` (function) `modules/orchestrator_config.py:218` `def verb_config(name)` -- Return the merged configuration of one auto verb, or None.
- `verb_enabled` (function) `modules/orchestrator_config.py:227` `def verb_enabled(name)` -- Return whether one auto verb may be proposed or executed.
- `upsert_verb` (function) `modules/orchestrator_config.py:233` `def upsert_verb(name)` -- Create or update one auto-verb override in the payload.
- `remove_verb` (function) `modules/orchestrator_config.py:290` `def remove_verb(name)` -- Remove a custom verb, or disable a built-in one.
- `reset` (function) `modules/orchestrator_config.py:315` `def reset()` -- Drop every orchestrator override (back to defaults).

## modules/osint_enrich.py
Imported by: `modules/finding_lifecycle.py`, `tests/test_finding_lifecycle.py`
- `cve_lookup` (function) `modules/osint_enrich.py:122` `def cve_lookup(cve_id, sessions_dir)` -- Assemble OSV advisory + KEV flag + EPSS score for one CVE id.
- `reverse_dns` (function) `modules/osint_enrich.py:161` `def reverse_dns(ip, sessions_dir)` -- Best-effort PTR hostname for an IP (HackerTarget, then DoH).
- `host_geo` (function) `modules/osint_enrich.py:183` `def host_geo(ip, sessions_dir)` -- Country/org/ISP for an IP via the keyless ip-api endpoint.
- `domain_exposure` (function) `modules/osint_enrich.py:198` `def domain_exposure(domain, sessions_dir)` -- Count public urlscan.io results for a domain (no key needed).
- `enrich_evidence` (function) `modules/osint_enrich.py:213` `def enrich_evidence(items, sessions_dir)` -- Append keyless OSINT verdicts to CVE mentions inside evidence items.

## modules/payload_factory.py
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/payload_generation.py`, `cli/commands/session_ops.py`, `lazyown.py`, `scripts/devtools/core_smoke.py`, `tests/test_payload_factory.py`
- `PayloadTemplate.__init__` (method) `modules/payload_factory.py:222` `def __init__(self, name, platform, arch, description, options)`
- `PayloadTemplate.generate` (method) `modules/payload_factory.py:237` `def generate(self)` -- Generate the raw payload bytes.
- `PayloadTemplate.to_dict` (method) `modules/payload_factory.py:241` `def to_dict(self)`
- `ReverseShellPayload.__init__` (method) `modules/payload_factory.py:254` `def __init__(self)`
- `ReverseShellPayload.generate` (method) `modules/payload_factory.py:272` `def generate(self)`
- `WindowsReverseShellPayload.__init__` (method) `modules/payload_factory.py:293` `def __init__(self)`
- `WindowsReverseShellPayload.generate` (method) `modules/payload_factory.py:305` `def generate(self)`
- `MsfvenomPayload.__init__` (method) `modules/payload_factory.py:325` `def __init__(self, name, platform, arch)`
- `MsfvenomPayload.generate` (method) `modules/payload_factory.py:337` `def generate(self)`
- `ShellcodePayload.__init__` (method) `modules/payload_factory.py:374` `def __init__(self, name, platform, arch, description, escaped_hex, patcher)`
- `ShellcodePayload.generate` (method) `modules/payload_factory.py:397` `def generate(self)` -- Return the shellcode, optionally patching LHOST / LPORT.
- `DynamicShellcodePayload.__init__` (method) `modules/payload_factory.py:416` `def __init__(self, name, platform, arch, description, builder)`
- `DynamicShellcodePayload.generate` (method) `modules/payload_factory.py:436` `def generate(self)`
- `PayloadFactory.__init__` (method) `modules/payload_factory.py:464` `def __init__(self)`
- `PayloadFactory.register` (method) `modules/payload_factory.py:512` `def register(self, template)` -- Register a custom payload template.
- `PayloadFactory.list` (method) `modules/payload_factory.py:516` `def list(self, platform)` -- List all registered payloads, optionally filtered by platform.
- `PayloadFactory.get` (method) `modules/payload_factory.py:525` `def get(self, name)` -- Get a payload template by name.
- `PayloadFactory.generate` (method) `modules/payload_factory.py:529` `def generate(self, name, format, output)` -- Generate a payload by name.
- `PayloadFactory.list_formats` (method) `modules/payload_factory.py:664` `def list_formats()` -- List all available output formats.
- `format_payload_table` (function) `modules/payload_factory.py:672` `def format_payload_table(payloads)` -- Format a list of payload dicts as an aligned table.

## modules/phishing_orchestrator.py
Depends on: `core/crypto.py`, `core/hardening.py`
Imported by: `cli/commands/phishing_wizard.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`
- `PhishingOrchestrator.__init__` (method) `modules/phishing_orchestrator.py:316` `def __init__(self)`
- `PhishingOrchestrator.get_instance` (method) `modules/phishing_orchestrator.py:321` `def get_instance(cls)`
- `PhishingOrchestrator.launch` (method) `modules/phishing_orchestrator.py:332` `def launch(self, target_domain, template, mode, targets_file, sender_email, sender_password, smtp_host, smtp_port)` -- Launch a phishing campaign.
- `PhishingOrchestrator.profile_targets` (method) `modules/phishing_orchestrator.py:441` `def profile_targets(self, domain)` -- Profile targets for a domain using OSINT techniques.
- `PhishingOrchestrator.generate_template` (method) `modules/phishing_orchestrator.py:486` `def generate_template(self, name, target_domain, context)` -- Generate or retrieve a phishing template.
- `PhishingOrchestrator.clone_landing_page` (method) `modules/phishing_orchestrator.py:533` `def clone_landing_page(self, url)` -- Clone a target login page for credential harvesting.
- `PhishingOrchestrator.get_results` (method) `modules/phishing_orchestrator.py:560` `def get_results(self, campaign_id)` -- Get campaign results.
- `PhishingOrchestrator.record_click` (method) `modules/phishing_orchestrator.py:584` `def record_click(self, campaign_id, email)` -- Record a link click.
- `PhishingOrchestrator.record_credentials` (method) `modules/phishing_orchestrator.py:605` `def record_credentials(self, campaign_id, email, password)` -- Record harvested credentials.


Next: [API_p15.md](API_p15.md)
