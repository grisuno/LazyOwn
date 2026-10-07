# API (page 12 of 20)
Previous: [API_p11.md](API_p11.md)

## modules/lazywps.sh
- `ctrl_c` (function) `modules/lazywps.sh:9`

## modules/lesson_ingestor.py
Depends on: `core/logging.py`, `modules/moe_router.py`, `modules/rl_trainer.py`
Imported by: `skills/lazyown_campaign.py`, `tests/test_lesson_ingestor.py`
- `LessonLearned.from_dict` (method) `modules/lesson_ingestor.py:65` `def from_dict(cls, d)`
- `LessonIngestor.__init__` (method) `modules/lesson_ingestor.py:85` `def __init__(self, lessons_file, router, trainer, boost_reward)`
- `LessonIngestor.ingest` (method) `modules/lesson_ingestor.py:122` `def ingest(self, lesson)` -- Apply a single lesson to the MoE performance store and RL Q-table.
- `LessonIngestor.ingest_all` (method) `modules/lesson_ingestor.py:180` `def ingest_all(self, lessons)` -- Ingest a batch of lessons.
- `LessonIngestor.ingest_campaign_lessons` (method) `modules/lesson_ingestor.py:217` `def ingest_campaign_lessons(lessons_file)` -- Module-level convenience function to ingest all campaign lessons.

## modules/lilsplunky.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `simple_parse_log_line` (function) `modules/lilsplunky.py:68` `def simple_parse_log_line(line, file_path)` -- Intenta extraer información básica de una línea de log.
- `store_event` (function) `modules/lilsplunky.py:106` `def store_event(event_data)` -- Almacena el evento procesado (diccionario Python) como una línea JSON en el archivo de salida.
- `analyze_with_deepseek` (function) `modules/lilsplunky.py:120` `def analyze_with_deepseek(log_entry_data)` -- Sends a single log entry to DeepSeek for analysis.
- `LogFileHandler.__init__` (method) `modules/lilsplunky.py:216` `def __init__(self, log_dir, mode)`
- `LogFileHandler.initialize_file_positions` (method) `modules/lilsplunky.py:222` `def initialize_file_positions(self)` -- Set initial position to the end of all currently monitored files.
- `LogFileHandler.is_monitored` (method) `modules/lilsplunky.py:238` `def is_monitored(self, file_path)` -- Check if the file path matches any of the monitored patterns.
- `LogFileHandler.process_file` (method) `modules/lilsplunky.py:250` `def process_file(self, file_path)` -- Reads new lines from a file since the last known position.
- `LogFileHandler.on_modified` (method) `modules/lilsplunky.py:324` `def on_modified(self, event)` -- Triggered when a file or directory is modified.
- `LogFileHandler.on_created` (method) `modules/lilsplunky.py:329` `def on_created(self, event)` -- Triggered when a file or directory is created.
- `LogFileHandler.display_record` (method) `modules/lilsplunky.py:338` `def display_record(record)` -- Muestra un registro procesado de forma atractiva en la consola.
- `LogFileHandler.search_logs` (method) `modules/lilsplunky.py:375` `def search_logs(query, file_path)` -- Busca en el archivo de eventos JSONL registros que coincidan (búsqueda simple de substring).
- `LogFileHandler.start_monitoring` (method) `modules/lilsplunky.py:406` `def start_monitoring(log_dir, mode)` -- Starts monitoring the specified log directory.
- `LogFileHandler.parse_args` (method) `modules/lilsplunky.py:438` `def parse_args()`

## modules/linux_advanced_payloads.py
Imported by: `cli/commands/payload_arsenal.py`
- `LinuxAdvancedPayloadFactory.__init__` (method) `modules/linux_advanced_payloads.py:107` `def __init__(self, config, output_dir)`
- `LinuxAdvancedPayloadFactory.generate_ld_preload_rootkit` (method) `modules/linux_advanced_payloads.py:112` `def generate_ld_preload_rootkit(self)` -- Generate a C source file for an LD_PRELOAD rootkit.
- `LinuxAdvancedPayloadFactory.generate_ebpf_payload` (method) `modules/linux_advanced_payloads.py:237` `def generate_ebpf_payload(self)` -- Generate an eBPF C program for network manipulation.
- `LinuxAdvancedPayloadFactory.generate_pam_backdoor` (method) `modules/linux_advanced_payloads.py:313` `def generate_pam_backdoor(self)` -- Generate a PAM (Pluggable Authentication Module) backdoor.
- `LinuxAdvancedPayloadFactory.generate_systemd_persistence` (method) `modules/linux_advanced_payloads.py:400` `def generate_systemd_persistence(self)` -- Generate systemd service and timer units for persistent callbacks.
- `LinuxAdvancedPayloadFactory.generate_ssh_persistence` (method) `modules/linux_advanced_payloads.py:462` `def generate_ssh_persistence(self)` -- Generate an SSH persistence script for authorized_keys injection.
- `LinuxAdvancedPayloadFactory.generate_kernel_module` (method) `modules/linux_advanced_payloads.py:523` `def generate_kernel_module(self)` -- Generate a Linux kernel module (LKM) rootkit.
- `LinuxAdvancedPayloadFactory.generate_process_masquerade` (method) `modules/linux_advanced_payloads.py:636` `def generate_process_masquerade(self)` -- Generate a process masquerading script.
- `LinuxAdvancedPayloadFactory.generate_udev_persistence` (method) `modules/linux_advanced_payloads.py:679` `def generate_udev_persistence(self)` -- Generate a udev rule for persistence on USB/device events.
- `LinuxAdvancedPayloadFactory.generate_motd_backdoor` (method) `modules/linux_advanced_payloads.py:694` `def generate_motd_backdoor(self)` -- Generate a Message of the Day (motd) hook for persistence.
- `LinuxAdvancedPayloadFactory.compile_c_source` (method) `modules/linux_advanced_payloads.py:714` `def compile_c_source(self, source, output_name, shared)` -- Compile C source code to a binary or shared library.
- `LinuxAdvancedPayloadFactory.generate_all` (method) `modules/linux_advanced_payloads.py:758` `def generate_all(self)` -- Generate all Linux advanced payload artifacts.
- `LinuxAdvancedPayloadFactory.list_hook_functions` (method) `modules/linux_advanced_payloads.py:802` `def list_hook_functions()`
- `LinuxAdvancedPayloadFactory.list_persistence_methods` (method) `modules/linux_advanced_payloads.py:806` `def list_persistence_methods()`

## modules/listener_manager.py
Depends on: `utils.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `lazyc2.py`
- `Listener.to_dict` (method) `modules/listener_manager.py:152` `def to_dict(self)`
- `Listener.from_dict` (method) `modules/listener_manager.py:162` `def from_dict(cls, data)`
- `ListenerManager.__init__` (method) `modules/listener_manager.py:179` `def __init__(self, app, sessions_dir, payload)`
- `ListenerManager.set_payload` (method) `modules/listener_manager.py:187` `def set_payload(self, payload)` -- Update the payload mapping used to resolve the bind address.
- `ListenerManager.add` (method) `modules/listener_manager.py:229` `def add(self, port, ssl, listener_id)` -- Register a new listener configuration (does not start it).
- `ListenerManager.remove` (method) `modules/listener_manager.py:242` `def remove(self, listener_id)` -- Remove a listener configuration.
- `ListenerManager.start` (method) `modules/listener_manager.py:255` `def start(self, listener_id)` -- Start a single listener.
- `ListenerManager.stop` (method) `modules/listener_manager.py:327` `def stop(self, listener_id)` -- Stop a single listener.
- `ListenerManager.start_all` (method) `modules/listener_manager.py:348` `def start_all(self)` -- Start every listener marked as active.
- `ListenerManager.stop_all` (method) `modules/listener_manager.py:354` `def stop_all(self)` -- Stop every running listener.
- `ListenerManager.status` (method) `modules/listener_manager.py:359` `def status(self)` -- Return status of all listeners.
- `ListenerManager.get_default_port` (method) `modules/listener_manager.py:369` `def get_default_port(self, fallback)` -- Return the port of the first active listener, or fallback.

## modules/live_surface.py
Depends on: `modules/world_model.py`
Imported by: `lazyc2.py`, `modules/unified_dashboard.py`, `tests/test_live_surface.py`
- `build_live_graph` (function) `modules/live_surface.py:72` `def build_live_graph(world)` -- Build a live vis-network payload from a world-model snapshot.

## modules/llm_adapter.py
Depends on: `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazyphishingai.py`, `core/logging.py`, `modules/llm_factory.py`, `modules/llm_prompts.py`
Imported by: `cli/commands/ai.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_llm_adapter_parity.py`
- `safe_groq_client` (function) `modules/llm_adapter.py:48` `def safe_groq_client(api_key)` -- Create a Groq client, returning None when no key is provided.
- `process_prompt` (function) `modules/llm_adapter.py:121` `def process_prompt(client, prompt, debug)` -- Generate a single-line shell command from a user prompt.
- `process_prompt_script` (function) `modules/llm_adapter.py:135` `def process_prompt_script(client, prompt, debug)` -- Generate a full script from a user prompt.
- `process_prompt_adversary` (function) `modules/llm_adapter.py:149` `def process_prompt_adversary(client, prompt, debug)` -- Answer questions about MITRE ATT&CK techniques and Atomic Red Team.
- `process_prompt_general` (function) `modules/llm_adapter.py:163` `def process_prompt_general(client, prompt, debug)` -- Answer as a general red-team assistant with payload.json context.
- `process_prompt_search` (function) `modules/llm_adapter.py:177` `def process_prompt_search(client, prompt, debug)` -- Perform research and threat-intelligence analysis.
- `process_prompt_task` (function) `modules/llm_adapter.py:191` `def process_prompt_task(client, prompt, debug)` -- Analyze a task-assessment JSON file for completion status.
- `process_prompt_vuln` (function) `modules/llm_adapter.py:208` `def process_prompt_vuln(client, prompt, debug, event)` -- Analyze Nmap output for vulnerabilities and propose an action plan.
- `process_prompt_redop` (function) `modules/llm_adapter.py:239` `def process_prompt_redop(client, prompt, debug)` -- Evaluate a red-team operation status from a JSON database file.
- `ask_general` (function) `modules/llm_adapter.py:256` `def ask_general(prompt, debug)` -- Answer through the configured LLM backend, regardless of provider.

## modules/llm_client.py
Depends on: `core/logging.py`
Imported by: `contrib/legacy/lazyaddon_creator.py`, `modules/planner.py`, `modules/playbook_engine.py`, `skills/lazyown_mcp.py`
- `LLMClient.__init__` (method) `modules/llm_client.py:63` `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)`
- `LLMClient.ask` (method) `modules/llm_client.py:79` `def ask(self, prompt)` -- Send a prompt and return the text response.
- `LLMClient.classify` (method) `modules/llm_client.py:125` `def classify(self, output)` -- Short classification prompt.
- `LLMClient.summarize` (method) `modules/llm_client.py:154` `def summarize(self, text)` -- Summarize a block of text (e.g. nmap output, tool output).
- `LLMClient.get_client` (method) `modules/llm_client.py:239` `def get_client(api_key)` -- Return (or create) the module-level singleton LLMClient.
- `LLMClient.ask` (method) `modules/llm_client.py:247` `def ask(prompt)` -- Module-level convenience wrapper.
- `LLMClient.classify` (method) `modules/llm_client.py:259` `def classify(output)` -- Module-level convenience wrapper.
- `LLMClient.summarize` (method) `modules/llm_client.py:264` `def summarize(text)` -- Module-level convenience wrapper.

## modules/llm_evaluator.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `OutcomeRecorder.record` (method) `modules/llm_evaluator.py:57` `def record(self, decision)`
- `OutcomeRecorder.update_outcome` (method) `modules/llm_evaluator.py:60` `def update_outcome(self, decision_id, actual, findings_count, success)`
- `OutcomeRecorder.load_all` (method) `modules/llm_evaluator.py:69` `def load_all(self)`
- `OutcomeRecorder.load_by_session` (method) `modules/llm_evaluator.py:72` `def load_by_session(self, session_id)`
- `JSONLRecorder.__init__` (method) `modules/llm_evaluator.py:76` `def __init__(self, path)`
- `JSONLRecorder.record` (method) `modules/llm_evaluator.py:81` `def record(self, decision)`
- `JSONLRecorder.update_outcome` (method) `modules/llm_evaluator.py:86` `def update_outcome(self, decision_id, actual, findings_count, success)`
- `JSONLRecorder.load_all` (method) `modules/llm_evaluator.py:120` `def load_all(self)`
- `JSONLRecorder.load_by_session` (method) `modules/llm_evaluator.py:135` `def load_by_session(self, session_id)`
- `LLMEvaluator.__init__` (method) `modules/llm_evaluator.py:162` `def __init__(self, recorder)`
- `LLMEvaluator.record_decision` (method) `modules/llm_evaluator.py:165` `def record_decision(self, session_id, thought, action, mitre_tactic, expected_outcome, confidence)`
- `LLMEvaluator.record_outcome` (method) `modules/llm_evaluator.py:191` `def record_outcome(self, decision_id, actual_outcome, findings_count, success)`
- `LLMEvaluator.compute_metrics` (method) `modules/llm_evaluator.py:200` `def compute_metrics(self, session_id)`
- `LLMEvaluator.quality_report` (method) `modules/llm_evaluator.py:241` `def quality_report(self, session_id)`
- `LLMEvaluator.export_finetuning_dataset` (method) `modules/llm_evaluator.py:256` `def export_finetuning_dataset(self, path)`
- `LLMEvaluator.get_evaluator` (method) `modules/llm_evaluator.py:293` `def get_evaluator()`
- `LLMEvaluator.record_decision` (method) `modules/llm_evaluator.py:302` `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)`
- `LLMEvaluator.record_outcome` (method) `modules/llm_evaluator.py:315` `def record_outcome(decision_id, actual_outcome, findings_count, success)`

## modules/llm_factory.py
Depends on: `core/llm_budget.py`, `modules/ai_model.py`
Imported by: `cli/commands/ai.py`, `cli/wizard.py`, `contrib/legacy/lazyllmchat.py`, `core/payload_schema.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ai_fallback.py`, `modules/llm_adapter.py`, `modules/privesc_predictor.py`, `modules/professional_report.py`, `modules/vuln_agent.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `tests/test_ai_commands_llm.py`, `tests/test_llm_adapter_parity.py`, `tests/test_payload_schema.py`, `tests/test_wizard_llm.py`
- `LLMBackendNotSupportedError.default_model_for` (method) `modules/llm_factory.py:147` `def default_model_for(backend)` -- Return the default model identifier for a backend.
- `LLMBackendNotSupportedError.model_config_key` (method) `modules/llm_factory.py:168` `def model_config_key(backend)` -- Return the ``payload.json`` key holding a backend's model override.
- `LLMBackendNotSupportedError.api_key_config_key` (method) `modules/llm_factory.py:189` `def api_key_config_key(backend)` -- Return the ``payload.json`` key holding a backend's API key slot.
- `LLMBackendNotSupportedError.backend_requires_api_key` (method) `modules/llm_factory.py:212` `def backend_requires_api_key(backend)` -- Report whether a backend needs an API key to operate.
- `LLMBackendNotSupportedError.load_payload` (method) `modules/llm_factory.py:230` `def load_payload(payload_path)` -- Read ``payload.json`` from disk and return it as a dictionary.
- `LLMBackendNotSupportedError.get_llm_backend` (method) `modules/llm_factory.py:499` `def get_llm_backend(config, backend)` -- Return a concrete :class:`AIModel` selected by configuration.
- `LLMBackendNotSupportedError.get_llm_backend_raw` (method) `modules/llm_factory.py:585` `def get_llm_backend_raw(config, backend)` -- Return a raw :class:`AIModel` without the budget wrapper.
- `LLMBackendNotSupportedError.try_get_llm_backend` (method) `modules/llm_factory.py:607` `def try_get_llm_backend(config, backend)` -- Return a backend or ``None`` if construction fails for any reason.

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
- `LlmPromptConfig.render_kb_tail` (method) `modules/llm_prompts.py:271` `def render_kb_tail(lines)` -- Join the most recent knowledge lines for embedding into a prompt.
- `KnowledgeStore.__init__` (method) `modules/llm_prompts.py:289` `def __init__(self, path)` -- Initialize a store bound to a single JSON file.
- `KnowledgeStore.load` (method) `modules/llm_prompts.py:297` `def load(self)` -- Load the knowledge-base records from disk.
- `KnowledgeStore.save` (method) `modules/llm_prompts.py:312` `def save(self, records)` -- Persist a full record list to disk, creating parent directories.
- `KnowledgeStore.add` (method) `modules/llm_prompts.py:324` `def add(self, prompt, response)` -- Append a prompt/response record to the knowledge base.
- `KnowledgeStore.relevant` (method) `modules/llm_prompts.py:335` `def relevant(self, prompt, limit)` -- Return knowledge responses whose text shares keywords with the prompt.

## modules/log_tamper.py
Imported by: `cli/commands/opsec_cleanup.py`
- `LogTamper.__init__` (method) `modules/log_tamper.py:105` `def __init__(self, config)`
- `LogTamper.windows_clear_commands` (method) `modules/log_tamper.py:108` `def windows_clear_commands(self)` -- Generate Windows Event Log clearing commands.
- `LogTamper.linux_clear_commands` (method) `modules/log_tamper.py:164` `def linux_clear_commands(self)` -- Generate Linux log clearing commands.
- `LogTamper.macos_clear_commands` (method) `modules/log_tamper.py:221` `def macos_clear_commands(self)` -- Generate macOS log clearing commands.
- `LogTamper.generate_all` (method) `modules/log_tamper.py:267` `def generate_all(self)` -- Generate log tampering commands for all platforms.
- `LogTamper.auditd_disable_commands` (method) `modules/log_tamper.py:279` `def auditd_disable_commands(self)` -- Commands to temporarily disable or reconfigure auditd on Linux.
- `LogTamper.sysmon_disable_commands` (method) `modules/log_tamper.py:313` `def sysmon_disable_commands(self)` -- Commands to disable or degrade Sysmon on Windows.

## modules/logging_config.py
Depends on: `core/logging.py`
Imported by: `lazy_sentinel4.py`, `lazyc2.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/icmp_server.py`, `modules/lazyownerweb.py`, `modules/lilsplunky.py`, `modules/vuln_agent.py`, `modules/vulnbot.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`
- `ColoredFormatter.format` (method) `modules/logging_config.py:39` `def format(self, record)`
- `JsonFormatter.format` (method) `modules/logging_config.py:72` `def format(self, record)`
- `CorrelationFilter.filter` (method) `modules/logging_config.py:96` `def filter(self, record)`
- `ResilientRotatingFileHandler.emit` (method) `modules/logging_config.py:118` `def emit(self, record)` -- Write one record, no-op after the file has become unwritable.
- `ResilientRotatingFileHandler.handleError` (method) `modules/logging_config.py:124` `def handleError(self, record)` -- Suppress the default per-record traceback; notify once via stderr.
- `ResilientRotatingFileHandler.set_correlation_id` (method) `modules/logging_config.py:138` `def set_correlation_id(cid)` -- Set the correlation ID for the current async/task context.
- `ResilientRotatingFileHandler.get_correlation_id` (method) `modules/logging_config.py:143` `def get_correlation_id()` -- Return the current correlation ID, or None.
- `ResilientRotatingFileHandler.clear_correlation_id` (method) `modules/logging_config.py:148` `def clear_correlation_id()` -- Reset the correlation ID for the current context.
- `ResilientRotatingFileHandler.configure` (method) `modules/logging_config.py:248` `def configure(level, log_dir, console, file, format_console, format_file, max_bytes, backup_count, module_levels)` -- Configure LazyOwn's centralized logging system.
- `ResilientRotatingFileHandler.get_logger` (method) `modules/logging_config.py:329` `def get_logger(name, level)` -- Get a logger with the given name.
- `ResilientRotatingFileHandler.set_level` (method) `modules/logging_config.py:358` `def set_level(name, level)` -- Set the log level for a specific logger.
- `ResilientRotatingFileHandler.set_quiet` (method) `modules/logging_config.py:368` `def set_quiet()` -- Silence all logging below WARNING level.
- `ResilientRotatingFileHandler.set_verbose` (method) `modules/logging_config.py:374` `def set_verbose()` -- Enable DEBUG level logging.
- `ResilientRotatingFileHandler.silence_module` (method) `modules/logging_config.py:380` `def silence_module(name)` -- Completely silence a noisy module.
- `ResilientRotatingFileHandler.reset` (method) `modules/logging_config.py:389` `def reset()` -- Reset the logging system to defaults.

## modules/macos_payloads.py
Imported by: `cli/commands/payload_arsenal.py`
- `MacOSPayloadFactory.__init__` (method) `modules/macos_payloads.py:115` `def __init__(self, config, output_dir)`
- `MacOSPayloadFactory.generate_app_bundle` (method) `modules/macos_payloads.py:144` `def generate_app_bundle(self)` -- Generate a macOS .app bundle with embedded reverse shell.
- `MacOSPayloadFactory.generate_launchd_persistence` (method) `modules/macos_payloads.py:219` `def generate_launchd_persistence(self)` -- Generate a LaunchDaemon or LaunchAgent plist for persistence.
- `MacOSPayloadFactory.generate_tcc_bypass` (method) `modules/macos_payloads.py:275` `def generate_tcc_bypass(self)` -- Generate a TCC bypass script targeting common permissions.
- `MacOSPayloadFactory.generate_osascript_dropper` (method) `modules/macos_payloads.py:321` `def generate_osascript_dropper(self)` -- Generate an AppleScript-based dropper that downloads and executes a stage.
- `MacOSPayloadFactory.generate_swift_stager` (method) `modules/macos_payloads.py:342` `def generate_swift_stager(self)` -- Generate a Swift reverse shell stager.
- `MacOSPayloadFactory.generate_persistence_scripts` (method) `modules/macos_payloads.py:405` `def generate_persistence_scripts(self)` -- Generate all available macOS persistence scripts.
- `MacOSPayloadFactory.generate_phishing_dialog` (method) `modules/macos_payloads.py:454` `def generate_phishing_dialog(self)` -- Generate an AppleScript credential phishing dialog.
- `MacOSPayloadFactory.generate_all` (method) `modules/macos_payloads.py:477` `def generate_all(self)` -- Generate all macOS payload artifacts.
- `MacOSPayloadFactory.list_tcc_services` (method) `modules/macos_payloads.py:524` `def list_tcc_services()` -- Return the list of known TCC service identifiers.
- `MacOSPayloadFactory.list_persistence_methods` (method) `modules/macos_payloads.py:529` `def list_persistence_methods()` -- Return the list of available persistence methods for macOS.

## modules/mario.py
- `check_collision` (function) `modules/mario.py:102` `def check_collision(x, y, layer)`

## modules/mcp_agent_bridge.py
Depends on: `core/logging.py`
Imported by: `modules/unified_bridge.py`, `skills/lazyown_mcp.py`
- `get_agent_status` (function) `modules/mcp_agent_bridge.py:154` `def get_agent_status(agent_id)` -- Public: returns current status dict for an agent.
- `get_agent_result` (function) `modules/mcp_agent_bridge.py:179` `def get_agent_result(agent_id)` -- Public: returns final result + full action log.
- `list_agents` (function) `modules/mcp_agent_bridge.py:202` `def list_agents(limit)` -- List recent agents sorted by start time.
- `GroqAgentWorker.__init__` (method) `modules/mcp_agent_bridge.py:225` `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)`
- `GroqAgentWorker.run` (method) `modules/mcp_agent_bridge.py:247` `def run(self)`
- `OllamaReActWorker.__init__` (method) `modules/mcp_agent_bridge.py:317` `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)`
- `OllamaReActWorker.run` (method) `modules/mcp_agent_bridge.py:338` `def run(self)`
- `AgentBridgeWorker.__init__` (method) `modules/mcp_agent_bridge.py:388` `def __init__(self, agent_id, goal, backend, run_cmd, max_iterations)`
- `AgentBridgeWorker.run` (method) `modules/mcp_agent_bridge.py:395` `def run(self)`
- `AgentBridgeWorker.start_agent` (method) `modules/mcp_agent_bridge.py:417` `def start_agent(goal, backend, lazyown_runner_fn, max_iterations)` -- Start an agent in a background thread.
- `AgentBridgeWorker.dummy_runner` (method) `modules/mcp_agent_bridge.py:441` `def dummy_runner(cmd)`

## modules/memory_cleaner.py
Imported by: `cli/commands/opsec_cleanup.py`
- `MemoryCleaner.__init__` (method) `modules/memory_cleaner.py:61` `def __init__(self, config)`
- `MemoryCleaner.windows_memory_cleanup` (method) `modules/memory_cleaner.py:64` `def windows_memory_cleanup(self)` -- Generate Windows memory artifact cleanup commands.
- `MemoryCleaner.linux_memory_cleanup` (method) `modules/memory_cleaner.py:137` `def linux_memory_cleanup(self)` -- Generate Linux memory artifact cleanup commands.
- `MemoryCleaner.macos_memory_cleanup` (method) `modules/memory_cleaner.py:184` `def macos_memory_cleanup(self)` -- Generate macOS memory artifact cleanup commands.
- `MemoryCleaner.generate_on_exit_script` (method) `modules/memory_cleaner.py:225` `def generate_on_exit_script(self)` -- Generate an on-exit cleanup script for beacons.

## modules/memory_store.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `StorageBackend.save` (method) `modules/memory_store.py:95` `def save(self, entry)`
- `StorageBackend.search` (method) `modules/memory_store.py:98` `def search(self, query, top_k)`
- `StorageBackend.by_host` (method) `modules/memory_store.py:101` `def by_host(self, host, top_k)`
- `StorageBackend.by_service` (method) `modules/memory_store.py:104` `def by_service(self, service, top_k)`
- `StorageBackend.all_entries` (method) `modules/memory_store.py:107` `def all_entries(self, limit)`
- `StorageBackend.close` (method) `modules/memory_store.py:110` `def close(self)`
- `SQLiteBackend.__init__` (method) `modules/memory_store.py:129` `def __init__(self, db_path)`
- `SQLiteBackend.save` (method) `modules/memory_store.py:145` `def save(self, entry)`
- `SQLiteBackend.search` (method) `modules/memory_store.py:177` `def search(self, query, top_k)`
- `SQLiteBackend.by_host` (method) `modules/memory_store.py:189` `def by_host(self, host, top_k)`
- `SQLiteBackend.by_service` (method) `modules/memory_store.py:200` `def by_service(self, service, top_k)`
- `SQLiteBackend.all_entries` (method) `modules/memory_store.py:212` `def all_entries(self, limit)`
- `SQLiteBackend.stats_raw` (method) `modules/memory_store.py:222` `def stats_raw(self)`
- `SQLiteBackend.close` (method) `modules/memory_store.py:233` `def close(self)`
- `MemoryStore.__init__` (method) `modules/memory_store.py:241` `def __init__(self, backend)`
- `MemoryStore.remember` (method) `modules/memory_store.py:244` `def remember(self, session_id, host, tool, command, output, findings, success)`
- `MemoryStore.recall` (method) `modules/memory_store.py:271` `def recall(self, query, top_k)`
- `MemoryStore.recall_by_host` (method) `modules/memory_store.py:274` `def recall_by_host(self, host, top_k)`
- `MemoryStore.recall_for_service` (method) `modules/memory_store.py:277` `def recall_for_service(self, service_name, top_k)`
- `MemoryStore.stats` (method) `modules/memory_store.py:280` `def stats(self)`
- `MemoryStore.export_finetuning_dataset` (method) `modules/memory_store.py:288` `def export_finetuning_dataset(self, path)`
- `MemoryStore.get_memory_store` (method) `modules/memory_store.py:311` `def get_memory_store()`
- `MemoryStore.remember` (method) `modules/memory_store.py:320` `def remember(session_id, host, tool, command, output, findings, success)`
- `MemoryStore.recall` (method) `modules/memory_store.py:332` `def recall(query, top_k)`

## modules/metrics.py
Depends on: `core/logging.py`
Imported by: `lazyc2.py`, `lazyown.py`, `modules/c2_builder.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_metrics.py`
- `MetricsRegistry.__init__` (method) `modules/metrics.py:65` `def __init__(self)` -- Create an empty registry with its own lock.
- `MetricsRegistry.inc` (method) `modules/metrics.py:73` `def inc(self, name, labels, value)` -- Increment the named counter for the given labels.
- `MetricsRegistry.get` (method) `modules/metrics.py:91` `def get(self, name, labels)` -- Return the current value of a counter.
- `MetricsRegistry.prometheus_text` (method) `modules/metrics.py:111` `def prometheus_text(self)` -- Render every counter in Prometheus text exposition format.
- `MetricRecord.to_dict` (method) `modules/metrics.py:171` `def to_dict(self)` -- Return the record as a JSON-serialisable dictionary.
- `MetricsWriter.__init__` (method) `modules/metrics.py:193` `def __init__(self, path)` -- Initialise the writer.
- `MetricsWriter.path` (method) `modules/metrics.py:205` `def path(self)` -- Return the JSONL destination path.
- `MetricsWriter.append` (method) `modules/metrics.py:210` `def append(self, record)` -- Append a single record to disk.
- `MetricsAggregator.summarize` (method) `modules/metrics.py:258` `def summarize(cls, records, window_seconds, now_utc)` -- Compute aggregate statistics over the supplied records.
- `MetricsRecorder.__init__` (method) `modules/metrics.py:352` `def __init__(self, writer)` -- Initialise the recorder.
- `MetricsRecorder.path` (method) `modules/metrics.py:363` `def path(self)` -- Return the JSONL path used by the underlying writer.
- `MetricsRecorder.record` (method) `modules/metrics.py:368` `def record(self, command, args, duration_ms, success, exit_code, source)` -- Persist a single command-execution telemetry record.
- `MetricsRecorder.summarize` (method) `modules/metrics.py:429` `def summarize(self, window_seconds)` -- Return aggregate statistics over recorded events.
- `MetricsRecorder.tail` (method) `modules/metrics.py:445` `def tail(self, n)` -- Return the most recent *n* records, newest first.
- `MetricsRecorder.get_recorder` (method) `modules/metrics.py:467` `def get_recorder()` -- Return the process-wide :class:`MetricsRecorder` singleton.
- `MetricsRecorder.reset_recorder_for_tests` (method) `modules/metrics.py:481` `def reset_recorder_for_tests(writer)` -- Replace the module-level recorder with a fresh instance.

## modules/mfa_bypass.py
Imported by: `cli/commands/cicd.py`
- `MFABypassEngine.__init__` (method) `modules/mfa_bypass.py:128` `def __init__(self, sessions_dir)`
- `MFABypassEngine.enumerate_techniques` (method) `modules/mfa_bypass.py:133` `def enumerate_techniques(self, target)` -- Enumerate viable MFA bypass techniques for a given target.
- `MFABypassEngine.generate_phishing_templates` (method) `modules/mfa_bypass.py:153` `def generate_phishing_templates(self, target)` -- Generate phishing templates tailored for MFA bypass.
- `MFABypassEngine.mfa_conditional_access_scan` (method) `modules/mfa_bypass.py:209` `def mfa_conditional_access_scan(self, domain)` -- Scan for conditional access policy gaps.
- `MFABypassEngine.replay_oauth_token` (method) `modules/mfa_bypass.py:238` `def replay_oauth_token(self, access_token, refresh_token)` -- Test if an OAuth2 token is still valid and can be replayed.
- `MFABypassEngine.saml_golden_ticket_check` (method) `modules/mfa_bypass.py:263` `def saml_golden_ticket_check(self, adfs_server)` -- Check for ADFS token signing certificate exposure.
- `MFABypassEngine.export_report` (method) `modules/mfa_bypass.py:288` `def export_report(self)` -- Export MFA bypass results to a JSON report.

## modules/module_registry.py
Depends on: `core/logging.py`
Imported by: `cli/commands/marketplace.py`, `cli/commands/misc_migrated.py`, `cli/commands/module_manager.py`, `cli/commands/session_ops.py`, `skills/lazyown_mcp.py`, `tests/test_module_registry.py`
- `ModuleInfo.__init__` (method) `modules/module_registry.py:134` `def __init__(self, name, module_type, author, version, description, category, path, source, params, enabled...`
- `ModuleInfo.to_dict` (method) `modules/module_registry.py:164` `def to_dict(self)`
- `ModuleRegistry.__init__` (method) `modules/module_registry.py:197` `def __init__(self, base_dir)`
- `ModuleRegistry.get_instance` (method) `modules/module_registry.py:203` `def get_instance(cls, base_dir)` -- Return the singleton registry instance.
- `ModuleRegistry.scan` (method) `modules/module_registry.py:209` `def scan(self)` -- Scan all module directories and return the full list.
- `ModuleRegistry.rescan` (method) `modules/module_registry.py:222` `def rescan(self)` -- Force a full rescan and return modules.
- `ModuleRegistry.get` (method) `modules/module_registry.py:231` `def get(self, name)` -- Get a module by name.
- `ModuleRegistry.search` (method) `modules/module_registry.py:237` `def search(self, query, module_type, category, enabled_only, include_deprecated)` -- Search indexed modules.
- `ModuleRegistry.deprecated_modules` (method) `modules/module_registry.py:281` `def deprecated_modules(self)` -- Return all deprecated modules.
- `ModuleRegistry.by_type` (method) `modules/module_registry.py:287` `def by_type(self, module_type)` -- Shorthand for ``search(module_type=module_type)``.
- `ModuleRegistry.summary` (method) `modules/module_registry.py:291` `def summary(self)` -- Return counts by module type.
- `ModuleRegistry.format_module_table` (method) `modules/module_registry.py:507` `def format_module_table(modules, cols)` -- Format a list of modules as an aligned text table.
- `ModuleRegistry.format_module_detail` (method) `modules/module_registry.py:554` `def format_module_detail(m)` -- Format a single module's full metadata.

## modules/moe_router.py
Depends on: `core/logging.py`, `modules/toposwarm_bridge.py`
Imported by: `modules/lesson_ingestor.py`, `skills/swan_agent.py`, `tests/integration_autonomous_flow.py`, `tests/test_moe_rl_swan.py`, `tests/test_moe_router_check_regression.py`
- `ExpertProfile.is_local` (method) `modules/moe_router.py:95` `def is_local(self)`
- `ExpertPerformance.update` (method) `modules/moe_router.py:114` `def update(self, reward, detection_prob)`
- `IExpertSelector.select` (method) `modules/moe_router.py:252` `def select(self, candidates, task_type, performance_store, deterministic)` -- Return the selected expert from candidates.
- `ExpertPerformanceStore.__init__` (method) `modules/moe_router.py:274` `def __init__(self, path)`
- `ExpertPerformanceStore.record` (method) `modules/moe_router.py:289` `def record(self, expert_id, task_type, reward, detection_prob)` -- Update performance for (expert, task_type) and persist.
- `ExpertPerformanceStore.get` (method) `modules/moe_router.py:309` `def get(self, expert_id, task_type)`
- `ExpertPerformanceStore.all_for_task` (method) `modules/moe_router.py:314` `def all_for_task(self, task_type)`
- `ExpertPerformanceStore.performance_bonus` (method) `modules/moe_router.py:318` `def performance_bonus(self, expert_id, task_type)` -- Return a bonus scalar in [-0.3, +0.5] based on EMA reward history.
- `SoftmaxSelector.__init__` (method) `modules/moe_router.py:373` `def __init__(self, temperature)`
- `SoftmaxSelector.temperature` (method) `modules/moe_router.py:377` `def temperature(self)`
- `SoftmaxSelector.temperature` (method) `modules/moe_router.py:381` `def temperature(self, value)`
- `SoftmaxSelector.select` (method) `modules/moe_router.py:384` `def select(self, candidates, task_type, performance_store, deterministic)`
- `ExpertAvailabilityChecker.__init__` (method) `modules/moe_router.py:439` `def __init__(self)`
- `ExpertAvailabilityChecker.is_available` (method) `modules/moe_router.py:443` `def is_available(self, expert, api_key)`
- `MoERouter.__init__` (method) `modules/moe_router.py:500` `def __init__(self, experts, selector, performance_store, api_key)`
- `MoERouter.route` (method) `modules/moe_router.py:515` `def route(self, task_type, goal, deterministic)` -- Return the single best expert for the given task_type.
- `MoERouter.ensemble` (method) `modules/moe_router.py:548` `def ensemble(self, task_type, goal, n)` -- Return up to *n* distinct experts for ensemble execution.
- `MoERouter.adjusted_weight` (method) `modules/moe_router.py:563` `def adjusted_weight(ep)`
- `MoERouter.record_outcome` (method) `modules/moe_router.py:576` `def record_outcome(self, expert_id, task_type, reward, detection_prob)` -- Record the outcome of an expert execution.
- `MoERouter.top_experts_for_task` (method) `modules/moe_router.py:590` `def top_experts_for_task(self, task_type, top_k)` -- Return (expert, adjusted_weight) sorted descending for diagnostics.
- `MoERouter.get_expert` (method) `modules/moe_router.py:606` `def get_expert(self, expert_id)` -- Return expert by ID, or None.
- `MoERouter.status_report` (method) `modules/moe_router.py:610` `def status_report(self)` -- Return a diagnostic snapshot of all experts and their weights.
- `MoERouter.get_router` (method) `modules/moe_router.py:689` `def get_router(api_key)` -- Return (or create) the module-level singleton MoERouter.

## modules/morse.py
- `MorseConfig.reverse_morse_code` (method) `modules/morse.py:98` `def reverse_morse_code()` -- Build the reverse lookup table from Morse code to characters.
- `MorseConfig.text_to_morse` (method) `modules/morse.py:109` `def text_to_morse(text, config)` -- Convert plain text to Morse code.
- `MorseConfig.morse_to_text` (method) `modules/morse.py:130` `def morse_to_text(morse_code, config)` -- Convert Morse code back to plain text.
- `MorseConfig.clear_screen` (method) `modules/morse.py:157` `def clear_screen(config)` -- Reset the terminal screen using a bounded subprocess call.
- `MorseConfig.read_choice` (method) `modules/morse.py:171` `def read_choice(config)` -- Read and validate the menu choice from standard input.
- `MorseConfig.run_driver` (method) `modules/morse.py:186` `def run_driver(config)` -- Run the interactive Morse code conversion loop.

## modules/mysql_hookandroot_lib.c
- `reverse_shell` (function) `modules/mysql_hookandroot_lib.c:74` `void reverse_shell(void)` -- fork & send a bash shell to the attacker before starting mysqld
- `execvp` (function) `modules/mysql_hookandroot_lib.c:128` `int execvp(const char* filename, char* const argv[])` -- execvp() hook

## modules/network_opsec.py
Imported by: `cli/commands/opsec_cleanup.py`
- `NetworkOpsecEngine.__init__` (method) `modules/network_opsec.py:83` `def __init__(self, config)`
- `NetworkOpsecEngine.configure_proxy_chain` (method) `modules/network_opsec.py:87` `def configure_proxy_chain(self, chain_type)` -- Configure a proxy chain for C2 communication.
- `NetworkOpsecEngine.check_canary_tokens` (method) `modules/network_opsec.py:133` `def check_canary_tokens(self)` -- Check if the target has canary token / deception technology.
- `NetworkOpsecEngine.analyze_traffic_with_canary_check` (method) `modules/network_opsec.py:176` `def analyze_traffic_with_canary_check(self, target_host, target_port)` -- Analyze whether target traffic is being intercepted or analyzed.
- `NetworkOpsecEngine.dns_over_https_config` (method) `modules/network_opsec.py:235` `def dns_over_https_config(self)` -- Generate DNS-over-HTTPS configuration for proxy and system.
- `NetworkOpsecEngine.source_port_randomize` (method) `modules/network_opsec.py:259` `def source_port_randomize(self)` -- Randomize source port for outbound connections.
- `NetworkOpsecEngine.connection_jitter_schedule` (method) `modules/network_opsec.py:284` `def connection_jitter_schedule(self, beacon_interval)` -- Generate a jitter schedule for beacon connections.
- `NetworkOpsecEngine.canary_detection_setup` (method) `modules/network_opsec.py:307` `def canary_detection_setup(self)` -- Set up canary detection for the engagement.
- `NetworkOpsecEngine.summary` (method) `modules/network_opsec.py:339` `def summary(self)`

## modules/nmap2csv.py
- `dottedquad_to_num` (function) `modules/nmap2csv.py:95` `def dottedquad_to_num(ip)` -- Convert decimal dotted quad string IP to long integer
- `num_to_dottedquad` (function) `modules/nmap2csv.py:101` `def num_to_dottedquad(n)` -- Convert long int IP to dotted quad string
- `unique_match_from_list` (function) `modules/nmap2csv.py:107` `def unique_match_from_list(list)` -- Check the list for a potential pattern match
- `extract_matching_pattern` (function) `modules/nmap2csv.py:122` `def extract_matching_pattern(regex, group_name, unfiltered_list)` -- Return the desired group_name from a list of matching patterns
- `Host.__init__` (method) `modules/nmap2csv.py:142` `def __init__(self, ip, fqdn)`
- `Host.add_port` (method) `modules/nmap2csv.py:153` `def add_port(self, port)`
- `Host.get_ip_num_format` (method) `modules/nmap2csv.py:157` `def get_ip_num_format(self)`
- `Host.get_ip_dotted_format` (method) `modules/nmap2csv.py:160` `def get_ip_dotted_format(self)`
- `Host.get_fqdn` (method) `modules/nmap2csv.py:163` `def get_fqdn(self)`
- `Host.get_rdns_record` (method) `modules/nmap2csv.py:166` `def get_rdns_record(self)`
- `Host.get_port_list` (method) `modules/nmap2csv.py:169` `def get_port_list(self)`
- `Host.get_port_number_list` (method) `modules/nmap2csv.py:172` `def get_port_number_list(self)`
- `Host.get_port_protocol_list` (method) `modules/nmap2csv.py:181` `def get_port_protocol_list(self)`
- `Host.get_port_service_list` (method) `modules/nmap2csv.py:190` `def get_port_service_list(self)`
- `Host.get_port_version_list` (method) `modules/nmap2csv.py:199` `def get_port_version_list(self)`
- `Host.get_port_script_list` (method) `modules/nmap2csv.py:208` `def get_port_script_list(self)`
- `Host.get_os` (method) `modules/nmap2csv.py:217` `def get_os(self)`
- `Host.get_mac_address` (method) `modules/nmap2csv.py:220` `def get_mac_address(self)`
- `Host.get_mac_address_vendor` (method) `modules/nmap2csv.py:223` `def get_mac_address_vendor(self)`
- `Host.get_network_distance` (method) `modules/nmap2csv.py:226` `def get_network_distance(self)`
- `Host.set_fqdn` (method) `modules/nmap2csv.py:230` `def set_fqdn(self, fqdn)`
- `Host.set_rdns_record` (method) `modules/nmap2csv.py:233` `def set_rdns_record(self, rdns_record)`
- `Host.set_os` (method) `modules/nmap2csv.py:236` `def set_os(self, os)`
- `Host.set_mac` (method) `modules/nmap2csv.py:239` `def set_mac(self, mac_address, mac_address_vendor)`
- `Host.set_network_distance` (method) `modules/nmap2csv.py:243` `def set_network_distance(self, network_distance)`
- `Port.__init__` (method) `modules/nmap2csv.py:247` `def __init__(self, number, protocol, service, version, script)`
- `Port.get_number` (method) `modules/nmap2csv.py:254` `def get_number(self)`
- `Port.get_protocol` (method) `modules/nmap2csv.py:257` `def get_protocol(self)`
- `Port.get_service` (method) `modules/nmap2csv.py:260` `def get_service(self)`
- `Port.get_version` (method) `modules/nmap2csv.py:263` `def get_version(self)`
- `Port.get_script` (method) `modules/nmap2csv.py:266` `def get_script(self)`
- `Port.set_service` (method) `modules/nmap2csv.py:269` `def set_service(self, service)`
- `Port.set_version` (method) `modules/nmap2csv.py:272` `def set_version(self, version)`
- `Port.set_script` (method) `modules/nmap2csv.py:275` `def set_script(self, script)`
- `Port.split_grepable_match` (method) `modules/nmap2csv.py:278` `def split_grepable_match(raw_string)` -- Split the raw line to a neat Host object
- `Port.parse` (method) `modules/nmap2csv.py:324` `def parse(fd)` -- Parse the data according to several regexes
- `Port.parse_xml` (method) `modules/nmap2csv.py:445` `def parse_xml(xml_file)` -- Parse the XML file
- `Port.is_format_valid` (method) `modules/nmap2csv.py:524` `def is_format_valid(fmt)` -- Check for the supplied custom output format
- `Port.formatted_item` (method) `modules/nmap2csv.py:544` `def formatted_item(host, format_item)` -- return the attribute value related to the host
- `Port.repeat_attributes` (method) `modules/nmap2csv.py:576` `def repeat_attributes(attribute_list)` -- repeat attribute lists to the maximum for the
- `Port.generate_csv` (method) `modules/nmap2csv.py:589` `def generate_csv(fd, results, options)` -- Generate a plain ';' separated csv file with the desired or default attribute format
- `Port.main` (method) `modules/nmap2csv.py:623` `def main()`

## modules/obs_parser.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `modules/intelligence_engine.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`, `tests/test_phase1_data_gaps.py`
- `Observation.by_type` (method) `modules/obs_parser.py:81` `def by_type(self, ftype)`
- `Observation.has` (method) `modules/obs_parser.py:84` `def has(self, ftype)`
- `Extractor.extract` (method) `modules/obs_parser.py:96` `def extract(self, text, host)` -- Return all findings of this type found in *text*.
- `_ExtractorRegistry.__init__` (method) `modules/obs_parser.py:103` `def __init__(self)`
- `_ExtractorRegistry.register` (method) `modules/obs_parser.py:106` `def register(self, extractor)`
- `_ExtractorRegistry.run_all` (method) `modules/obs_parser.py:109` `def run_all(self, text, host)`
- `_IPExtractor.extract` (method) `modules/obs_parser.py:130` `def extract(self, text, host)`
- `_CredentialExtractor.extract` (method) `modules/obs_parser.py:155` `def extract(self, text, host)`
- `_ServiceVersionExtractor.extract` (method) `modules/obs_parser.py:182` `def extract(self, text, host)`
- `_PathExtractor.extract` (method) `modules/obs_parser.py:202` `def extract(self, text, host)`
- `_UsernameExtractor.extract` (method) `modules/obs_parser.py:222` `def extract(self, text, host)`
- `_HashExtractor.extract` (method) `modules/obs_parser.py:250` `def extract(self, text, host)`
- `_CVEExtractor.extract` (method) `modules/obs_parser.py:269` `def extract(self, text, host)`
- `_DomainExtractor.extract` (method) `modules/obs_parser.py:287` `def extract(self, text, host)`
- `_EmailExtractor.extract` (method) `modules/obs_parser.py:309` `def extract(self, text, host)`
- `_ErrorExtractor.extract` (method) `modules/obs_parser.py:331` `def extract(self, text, host)`
- `_CloudIdentityExtractor.extract` (method) `modules/obs_parser.py:355` `def extract(self, text, host)`
- `_SuccessDetector.is_success` (method) `modules/obs_parser.py:396` `def is_success(self, text)`
- `ObsParser.__init__` (method) `modules/obs_parser.py:419` `def __init__(self)`
- `ObsParser.register` (method) `modules/obs_parser.py:438` `def register(self, extractor)` -- Register an additional Extractor (Open/Closed extension point).
- `ObsParser.parse` (method) `modules/obs_parser.py:442` `def parse(self, output, host, tool)` -- Parse *output* and return an Observation.
- `ObsParser.get_parser` (method) `modules/obs_parser.py:487` `def get_parser()` -- Return (or create) the module-level singleton ObsParser.
- `ObsParser.parse` (method) `modules/obs_parser.py:495` `def parse(output, host, tool)` -- Module-level convenience wrapper.

## modules/operation.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/apt_playbooks.py`, `modules/obs_parser.py`, `modules/playbook_engine.py`, `modules/world_model.py`
Imported by: `cli/commands/caldera.py`
- `Operation.to_dict` (method) `modules/operation.py:98` `def to_dict(self)`
- `Operation.from_dict` (method) `modules/operation.py:116` `def from_dict(cls, d)`
- `Operation.save` (method) `modules/operation.py:134` `def save(self)`
- `Operation.log_event` (method) `modules/operation.py:143` `def log_event(self, step_index, step_name, status, summary, findings_count, error)`
- `Operation.record_facts` (method) `modules/operation.py:164` `def record_facts(self, findings)`
- `OperationManager.__init__` (method) `modules/operation.py:180` `def __init__(self)`
- `OperationManager.list` (method) `modules/operation.py:184` `def list(self)` -- List all persisted operations.
- `OperationManager.get` (method) `modules/operation.py:196` `def get(self, op_id)`
- `OperationManager.create` (method) `modules/operation.py:203` `def create(self, name, target, apt_name, description)` -- Create a new planned operation.
- `OperationManager.plan_from_apt` (method) `modules/operation.py:222` `def plan_from_apt(self, op, playbook_yaml_path)` -- Populate steps from an APT playbook YAML (or fall back to a derived MITRE playbook).
- `OperationManager.start` (method) `modules/operation.py:281` `def start(self, op_id, executor)` -- Start or resume a planned operation.
- `OperationManager.pause` (method) `modules/operation.py:356` `def pause(self, op_id)`
- `OperationManager.resume` (method) `modules/operation.py:365` `def resume(self, op_id, executor)`
- `OperationManager.stop` (method) `modules/operation.py:373` `def stop(self, op_id)`
- `OperationManager.status` (method) `modules/operation.py:383` `def status(self, op_id)` -- Return a structured status dict for an operation.
- `OperationManager.timeline` (method) `modules/operation.py:412` `def timeline(self, op_id)`
- `OperationManager.report` (method) `modules/operation.py:418` `def report(self, op_id)`
- `OperationManager.get_manager` (method) `modules/operation.py:459` `def get_manager()` -- Return a fresh :class:`OperationManager`.

## modules/operator_profiles.py
Depends on: `core/config.py`, `core/logging.py`
Imported by: `cli/commands/automation.py`
- `OperatorProfile.to_dict` (method) `modules/operator_profiles.py:57` `def to_dict(self)`
- `OperatorProfileManager.__init__` (method) `modules/operator_profiles.py:88` `def __init__(self)`
- `OperatorProfileManager.create_profile` (method) `modules/operator_profiles.py:169` `def create_profile(self, username, display_name, role, lhost, lport, listener_port, c2_port, c2_malleable_route...` -- Create a new operator profile.
- `OperatorProfileManager.load_profile` (method) `modules/operator_profiles.py:237` `def load_profile(self, username)` -- Load an operator profile.
- `OperatorProfileManager.update_profile` (method) `modules/operator_profiles.py:253` `def update_profile(self, username)` -- Update fields on an existing profile.
- `OperatorProfileManager.delete_profile` (method) `modules/operator_profiles.py:268` `def delete_profile(self, username)` -- Delete an operator profile and its directory.
- `OperatorProfileManager.list_profiles` (method) `modules/operator_profiles.py:278` `def list_profiles(self)` -- Return all operator profiles.
- `OperatorProfileManager.touch_activity` (method) `modules/operator_profiles.py:290` `def touch_activity(self, username)` -- Update last_active timestamp.
- `OperatorProfileManager.set_attribute` (method) `modules/operator_profiles.py:297` `def set_attribute(self, username, key, value)` -- Set a custom attribute on an operator profile.
- `OperatorProfileManager.get_attribute` (method) `modules/operator_profiles.py:306` `def get_attribute(self, username, key, default)` -- Get a custom attribute from an operator profile.
- `OperatorProfileManager.log_action` (method) `modules/operator_profiles.py:313` `def log_action(self, username, action, details)` -- Append an audited action to the operator's audit log.
- `OperatorProfileManager.effective_config` (method) `modules/operator_profiles.py:340` `def effective_config(self, username)` -- Merge team baseline (payload.json) with per-operator overrides.
- `OperatorProfileManager.get_operator_profile_manager` (method) `modules/operator_profiles.py:378` `def get_operator_profile_manager()` -- Return the singleton :class:`OperatorProfileManager`.

## modules/opsec_scorer.py
Depends on: `cli/commands/enum.py`, `core/config.py`, `core/logging.py`, `modules/db.py`, `modules/killchain.py`
Imported by: `cli/commands/opsec_cleanup.py`, `cli/commands/security.py`, `tests/test_opsec_scorer.py`, `tests/test_opsec_scorer_consolidated.py`
- `OpsecScore.to_dict` (method) `modules/opsec_scorer.py:280` `def to_dict(self)` -- Return the score serialized as a plain dictionary.
- `OpsecScorer.__init__` (method) `modules/opsec_scorer.py:335` `def __init__(self, payload, world_model)`
- `OpsecScorer.evasion_active` (method) `modules/opsec_scorer.py:344` `def evasion_active(self)`
- `OpsecScorer.traffic_morphing_active` (method) `modules/opsec_scorer.py:349` `def traffic_morphing_active(self)`
- `OpsecScorer.score` (method) `modules/opsec_scorer.py:357` `def score(self, command, rhost, phase_override)` -- Score an OPSEC risk for ``command`` against ``rhost``.
- `OpsecScorer.score_batch` (method) `modules/opsec_scorer.py:405` `def score_batch(self, commands, rhost)` -- Score multiple commands and return {command: OpsecScore}.
- `OpsecScorer.suggest_mitigations` (method) `modules/opsec_scorer.py:409` `def suggest_mitigations(self, command, detectable_by)` -- Return mitigation suggestions for a given command.
- `OpsecScorerV2.__init__` (method) `modules/opsec_scorer.py:607` `def __init__(self, context)`
- `OpsecScorerV2.assess` (method) `modules/opsec_scorer.py:612` `def assess(self, command, extra_context)` -- Assess OPSEC risk for a command in the current context.
- `OpsecScorerV2.should_allow` (method) `modules/opsec_scorer.py:673` `def should_allow(self, command)` -- Quick gating check - returns (allowed, score).
- `OpsecScorerV2.get_trend` (method) `modules/opsec_scorer.py:686` `def get_trend(self)` -- Analyze OPSEC risk trend over the session.
- `OpsecScorerV2.score_command` (method) `modules/opsec_scorer.py:780` `def score_command(command, payload, rhost)` -- Convenience function: score a single command without creating a scorer instance.

## modules/payload_factory.py
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/payload_generation.py`, `cli/commands/session_ops.py`, `lazyown.py`, `scripts/devtools/core_smoke.py`, `tests/test_payload_factory.py`
- `PayloadTemplate.__init__` (method) `modules/payload_factory.py:218` `def __init__(self, name, platform, arch, description, options)`
- `PayloadTemplate.generate` (method) `modules/payload_factory.py:233` `def generate(self)` -- Generate the raw payload bytes.
- `PayloadTemplate.to_dict` (method) `modules/payload_factory.py:237` `def to_dict(self)`
- `ReverseShellPayload.__init__` (method) `modules/payload_factory.py:250` `def __init__(self)`
- `ReverseShellPayload.generate` (method) `modules/payload_factory.py:268` `def generate(self)`
- `WindowsReverseShellPayload.__init__` (method) `modules/payload_factory.py:289` `def __init__(self)`
- `WindowsReverseShellPayload.generate` (method) `modules/payload_factory.py:301` `def generate(self)`
- `MsfvenomPayload.__init__` (method) `modules/payload_factory.py:321` `def __init__(self, name, platform, arch)`
- `MsfvenomPayload.generate` (method) `modules/payload_factory.py:333` `def generate(self)`
- `ShellcodePayload.__init__` (method) `modules/payload_factory.py:366` `def __init__(self, name, platform, arch, description, escaped_hex, patcher)`
- `ShellcodePayload.generate` (method) `modules/payload_factory.py:389` `def generate(self)` -- Return the shellcode, optionally patching LHOST / LPORT.
- `DynamicShellcodePayload.__init__` (method) `modules/payload_factory.py:408` `def __init__(self, name, platform, arch, description, builder)`
- `DynamicShellcodePayload.generate` (method) `modules/payload_factory.py:428` `def generate(self)`
- `PayloadFactory.__init__` (method) `modules/payload_factory.py:456` `def __init__(self)`
- `PayloadFactory.register` (method) `modules/payload_factory.py:504` `def register(self, template)` -- Register a custom payload template.
- `PayloadFactory.list` (method) `modules/payload_factory.py:508` `def list(self, platform)` -- List all registered payloads, optionally filtered by platform.
- `PayloadFactory.get` (method) `modules/payload_factory.py:517` `def get(self, name)` -- Get a payload template by name.
- `PayloadFactory.generate` (method) `modules/payload_factory.py:521` `def generate(self, name, format, output)` -- Generate a payload by name.
- `PayloadFactory.list_formats` (method) `modules/payload_factory.py:665` `def list_formats()` -- List all available output formats.
- `PayloadFactory.format_payload_table` (method) `modules/payload_factory.py:673` `def format_payload_table(payloads)` -- Format a list of payload dicts as an aligned table.


Next: [API_p13.md](API_p13.md)
