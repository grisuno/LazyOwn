# API (page 16 of 26)
Previous: [API_p15.md](API_p15.md)

## modules/lazyreverse_shell.sh
- `mostrar_ayuda` (function) `modules/lazyreverse_shell.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyreverse_shell.sh:31` -- Validar dirección IP

## modules/lazyshortener.py
Depends on: `core/safe_exec.py`
Imported by: `modules/lazypoophish.py`
- `providers` (function) `modules/lazyshortener.py:30` `def providers()` -- Return every supported shortener provider key.
- `shorten` (function) `modules/lazyshortener.py:35` `def shorten(url, provider, timeout)` -- Shorten one URL through a keyless public provider.

## modules/lazyvpnshield.sh
- `ctrl_c` (function) `modules/lazyvpnshield.sh:11`
- `check_sudo` (function) `modules/lazyvpnshield.sh:16`
- `save_current_rules` (function) `modules/lazyvpnshield.sh:29`
- `show_current_rules` (function) `modules/lazyvpnshield.sh:37`
- `apply_vpn_rules` (function) `modules/lazyvpnshield.sh:45`
- `undo_and_restore_rules` (function) `modules/lazyvpnshield.sh:86`
- `main` (function) `modules/lazyvpnshield.sh:113`

## modules/lazywps.sh
- `ctrl_c` (function) `modules/lazywps.sh:9`

## modules/lesson_ingestor.py
Depends on: `core/logging.py`, `modules/moe_router.py`, `modules/rl_trainer.py`
Imported by: `skills/lazyown_campaign.py`, `tests/test_lesson_ingestor.py`
- `LessonLearned.from_dict` (method) `modules/lesson_ingestor.py:66` `def from_dict(cls, d)`
- `LessonIngestor.__init__` (method) `modules/lesson_ingestor.py:86` `def __init__(self, lessons_file, router, trainer, boost_reward)`
- `LessonIngestor.ingest` (method) `modules/lesson_ingestor.py:125` `def ingest(self, lesson)` -- Apply a single lesson to the MoE performance store and RL Q-table.
- `LessonIngestor.ingest_all` (method) `modules/lesson_ingestor.py:185` `def ingest_all(self, lessons)` -- Ingest a batch of lessons.
- `ingest_campaign_lessons` (function) `modules/lesson_ingestor.py:222` `def ingest_campaign_lessons(lessons_file)` -- Module-level convenience function to ingest all campaign lessons.

## modules/lilsplunky.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `simple_parse_log_line` (function) `modules/lilsplunky.py:69` `def simple_parse_log_line(line, file_path)` -- Intenta extraer información básica de una línea de log.
- `store_event` (function) `modules/lilsplunky.py:108` `def store_event(event_data)` -- Almacena el evento procesado (diccionario Python) como una línea JSON en el archivo de salida.
- `analyze_with_deepseek` (function) `modules/lilsplunky.py:123` `def analyze_with_deepseek(log_entry_data)` -- Sends a single log entry to DeepSeek for analysis.
- `LogFileHandler.__init__` (method) `modules/lilsplunky.py:223` `def __init__(self, log_dir, mode)`
- `LogFileHandler.initialize_file_positions` (method) `modules/lilsplunky.py:229` `def initialize_file_positions(self)` -- Set initial position to the end of all currently monitored files.
- `LogFileHandler.is_monitored` (method) `modules/lilsplunky.py:245` `def is_monitored(self, file_path)` -- Check if the file path matches any of the monitored patterns.
- `LogFileHandler.process_file` (method) `modules/lilsplunky.py:257` `def process_file(self, file_path)` -- Reads new lines from a file since the last known position.
- `LogFileHandler.on_modified` (method) `modules/lilsplunky.py:331` `def on_modified(self, event)` -- Triggered when a file or directory is modified.
- `LogFileHandler.on_created` (method) `modules/lilsplunky.py:336` `def on_created(self, event)` -- Triggered when a file or directory is created.
- `display_record` (function) `modules/lilsplunky.py:346` `def display_record(record)` -- Muestra un registro procesado de forma atractiva en la consola.
- `search_logs` (function) `modules/lilsplunky.py:382` `def search_logs(query, file_path)` -- Busca en el archivo de eventos JSONL registros que coincidan (búsqueda simple de substring).
- `start_monitoring` (function) `modules/lilsplunky.py:413` `def start_monitoring(log_dir, mode)` -- Starts monitoring the specified log directory.
- `parse_args` (function) `modules/lilsplunky.py:446` `def parse_args()`

## modules/linux_advanced_payloads.py
Imported by: `cli/commands/payload_arsenal.py`
- `LinuxAdvancedPayloadFactory.__init__` (method) `modules/linux_advanced_payloads.py:105` `def __init__(self, config, output_dir)`
- `LinuxAdvancedPayloadFactory.generate_ld_preload_rootkit` (method) `modules/linux_advanced_payloads.py:110` `def generate_ld_preload_rootkit(self)` -- Generate a C source file for an LD_PRELOAD rootkit.
- `LinuxAdvancedPayloadFactory.generate_ebpf_payload` (method) `modules/linux_advanced_payloads.py:235` `def generate_ebpf_payload(self)` -- Generate an eBPF C program for network manipulation.
- `LinuxAdvancedPayloadFactory.generate_pam_backdoor` (method) `modules/linux_advanced_payloads.py:311` `def generate_pam_backdoor(self)` -- Generate a PAM (Pluggable Authentication Module) backdoor.
- `LinuxAdvancedPayloadFactory.generate_systemd_persistence` (method) `modules/linux_advanced_payloads.py:398` `def generate_systemd_persistence(self)` -- Generate systemd service and timer units for persistent callbacks.
- `LinuxAdvancedPayloadFactory.generate_ssh_persistence` (method) `modules/linux_advanced_payloads.py:458` `def generate_ssh_persistence(self)` -- Generate an SSH persistence script for authorized_keys injection.
- `LinuxAdvancedPayloadFactory.generate_kernel_module` (method) `modules/linux_advanced_payloads.py:519` `def generate_kernel_module(self)` -- Generate a Linux kernel module (LKM) rootkit.
- `LinuxAdvancedPayloadFactory.generate_process_masquerade` (method) `modules/linux_advanced_payloads.py:632` `def generate_process_masquerade(self)` -- Generate a process masquerading script.
- `LinuxAdvancedPayloadFactory.generate_udev_persistence` (method) `modules/linux_advanced_payloads.py:676` `def generate_udev_persistence(self)` -- Generate a udev rule for persistence on USB/device events.
- `LinuxAdvancedPayloadFactory.generate_motd_backdoor` (method) `modules/linux_advanced_payloads.py:689` `def generate_motd_backdoor(self)` -- Generate a Message of the Day (motd) hook for persistence.
- `LinuxAdvancedPayloadFactory.compile_c_source` (method) `modules/linux_advanced_payloads.py:707` `def compile_c_source(self, source, output_name, shared)` -- Compile C source code to a binary or shared library.
- `LinuxAdvancedPayloadFactory.generate_all` (method) `modules/linux_advanced_payloads.py:749` `def generate_all(self)` -- Generate all Linux advanced payload artifacts.
- `LinuxAdvancedPayloadFactory.list_hook_functions` (method) `modules/linux_advanced_payloads.py:793` `def list_hook_functions()`
- `LinuxAdvancedPayloadFactory.list_persistence_methods` (method) `modules/linux_advanced_payloads.py:797` `def list_persistence_methods()`

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
- `ListenerManager.stop` (method) `modules/listener_manager.py:335` `def stop(self, listener_id)` -- Stop a single listener.
- `ListenerManager.start_all` (method) `modules/listener_manager.py:356` `def start_all(self)` -- Start every listener marked as active.
- `ListenerManager.stop_all` (method) `modules/listener_manager.py:362` `def stop_all(self)` -- Stop every running listener.
- `ListenerManager.status` (method) `modules/listener_manager.py:367` `def status(self)` -- Return status of all listeners.
- `ListenerManager.get_default_port` (method) `modules/listener_manager.py:379` `def get_default_port(self, fallback)` -- Return the port of the first active listener, or fallback.

## modules/live_surface.py
Depends on: `modules/world_model.py`
Imported by: `lazyc2.py`, `modules/unified_dashboard.py`, `tests/test_live_surface.py`
- `build_live_graph` (function) `modules/live_surface.py:72` `def build_live_graph(world)` -- Build a live vis-network payload from a world-model snapshot.

## modules/llm_adapter.py
Depends on: `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazyphishingai.py`, `core/logging.py`, `modules/llm_factory.py`, `modules/llm_orchestrator.py`, `modules/llm_prompts.py`
Imported by: `cli/commands/ai.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_orchestrator.py`
- `safe_groq_client` (function) `modules/llm_adapter.py:55` `def safe_groq_client(api_key)` -- Create a Groq client, returning None when no key is provided.
- `process_prompt` (function) `modules/llm_adapter.py:155` `def process_prompt(client, prompt, debug)` -- Generate a single-line shell command from a user prompt.
- `process_prompt_script` (function) `modules/llm_adapter.py:169` `def process_prompt_script(client, prompt, debug)` -- Generate a full script from a user prompt.
- `process_prompt_adversary` (function) `modules/llm_adapter.py:183` `def process_prompt_adversary(client, prompt, debug)` -- Answer questions about MITRE ATT&CK techniques and Atomic Red Team.
- `process_prompt_general` (function) `modules/llm_adapter.py:197` `def process_prompt_general(client, prompt, debug)` -- Answer as a general red-team assistant with payload.json context.
- `process_prompt_search` (function) `modules/llm_adapter.py:211` `def process_prompt_search(client, prompt, debug)` -- Perform research and threat-intelligence analysis.
- `process_prompt_task` (function) `modules/llm_adapter.py:225` `def process_prompt_task(client, prompt, debug)` -- Analyze a task-assessment JSON file for completion status.
- `process_prompt_vuln` (function) `modules/llm_adapter.py:242` `def process_prompt_vuln(client, prompt, debug, event)` -- Analyze Nmap output for vulnerabilities and propose an action plan.
- `process_prompt_redop` (function) `modules/llm_adapter.py:273` `def process_prompt_redop(client, prompt, debug)` -- Evaluate a red-team operation status from a JSON database file.
- `ask_general` (function) `modules/llm_adapter.py:290` `def ask_general(prompt, debug)` -- Answer through the configured LLM backend with chain failover.

## modules/llm_client.py
Depends on: `core/logging.py`, `modules/ai_model.py`
Imported by: `contrib/legacy/lazyaddon_creator.py`, `modules/llm_factory.py`, `modules/planner.py`, `modules/playbook_engine.py`
- `LLMClient.__init__` (method) `modules/llm_client.py:63` `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)`
- `LLMClient.ask` (method) `modules/llm_client.py:79` `def ask(self, prompt)` -- Send a prompt and return the text response.
- `LLMClient.classify` (method) `modules/llm_client.py:130` `def classify(self, output)` -- Short classification prompt.
- `LLMClient.summarize` (method) `modules/llm_client.py:159` `def summarize(self, text)` -- Summarize a block of text (e.g. nmap output, tool output).
- `get_client` (function) `modules/llm_client.py:268` `def get_client(api_key)` -- Return (or create) the module-level singleton LLMClient.
- `ask` (function) `modules/llm_client.py:276` `def ask(prompt)` -- Module-level convenience wrapper.
- `classify` (function) `modules/llm_client.py:288` `def classify(output)` -- Module-level convenience wrapper.
- `summarize` (function) `modules/llm_client.py:293` `def summarize(text)` -- Module-level convenience wrapper.

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
- `get_evaluator` (function) `modules/llm_evaluator.py:293` `def get_evaluator()`
- `record_decision` (function) `modules/llm_evaluator.py:302` `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)`
- `record_outcome` (function) `modules/llm_evaluator.py:313` `def record_outcome(decision_id, actual_outcome, findings_count, success)`

## modules/llm_factory.py
Depends on: `core/llm_budget.py`, `modules/ai_model.py`, `modules/harness.py`, `modules/llm_client.py`, `modules/llm_orchestrator.py`, `modules/toposwarm_bridge.py`
Imported by: `cli/commands/ai.py`, `cli/wizard.py`, `contrib/legacy/lazyllmchat.py`, `core/payload_schema.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ai_fallback.py`, `modules/ai_model.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/llm_adapter.py`, `modules/llm_orchestrator.py`, `modules/mcp_agent_bridge.py`, `modules/privesc_predictor.py`, `modules/professional_report.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `tests/conftest.py`, `tests/test_ai_commands_llm.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_streaming.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_orchestrator.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_llm_resilience.py`, `tests/test_payload_schema.py`, `tests/test_vulnbot_fallback.py`, `tests/test_wizard_llm.py`
- `is_model_missing_error` (function) `modules/llm_factory.py:121` `def is_model_missing_error(message)` -- Return True when an error text means the model id is unavailable.
- `groq_model_chain` (function) `modules/llm_factory.py:141` `def groq_model_chain(config)` -- Return the ordered Groq model ids to try, configured model first.
- `default_model_for` (function) `modules/llm_factory.py:224` `def default_model_for(backend)` -- Return the default model identifier for a backend.
- `model_config_key` (function) `modules/llm_factory.py:245` `def model_config_key(backend)` -- Return the ``payload.json`` key holding a backend's model override.
- `api_key_config_key` (function) `modules/llm_factory.py:266` `def api_key_config_key(backend)` -- Return the ``payload.json`` key holding a backend's API key slot.
- `backend_requires_api_key` (function) `modules/llm_factory.py:291` `def backend_requires_api_key(backend)` -- Report whether a backend needs an API key to operate.
- `load_payload` (function) `modules/llm_factory.py:309` `def load_payload(payload_path)` -- Read ``payload.json`` from disk and return it as a dictionary.
- `get_llm_backend` (function) `modules/llm_factory.py:653` `def get_llm_backend(config, backend)` -- Return a concrete :class:`AIModel` selected by configuration.
- `get_llm_backend_raw` (function) `modules/llm_factory.py:749` `def get_llm_backend_raw(config, backend)` -- Return a raw :class:`AIModel` without the budget wrapper.
- `try_get_llm_backend` (function) `modules/llm_factory.py:771` `def try_get_llm_backend(config, backend)` -- Return a backend or ``None`` if construction fails for any reason.
- `stream_complete` (function) `modules/llm_factory.py:848` `def stream_complete(model, prompt, max_tokens, on_delta)` -- Completion that reports incremental deltas while it arrives.
- `complete` (function) `modules/llm_factory.py:919` `def complete(model, prompt, max_tokens)` -- Complete a prompt through one model spec; raise when unanswered.

## modules/llm_orchestrator.py
Depends on: `modules/lazy_engine.py`, `modules/llm_factory.py`, `modules/llm_pool.py`, `modules/orchestrator_config.py`
Imported by: `lazyc2.py`, `modules/ai_fallback.py`, `modules/llm_adapter.py`, `modules/llm_factory.py`, `modules/vulnbot.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_orchestrator.py`, `tests/test_vulnbot_fallback.py`
- `OrchestratorResult.ok` (method) `modules/llm_orchestrator.py:118` `def ok(self)` -- Return True when a chain member served the answer.
- `OrchestratorResult.display_text` (method) `modules/llm_orchestrator.py:123` `def display_text(self)` -- Return the notice-prefixed answer for operator-facing surfaces.
- `sort_members` (function) `modules/llm_orchestrator.py:130` `def sort_members(members)` -- Return a weight-sorted defensive copy of a member list.
- `pool_chain` (function) `modules/llm_orchestrator.py:148` `def pool_chain()` -- Return the failover chain governed by lazy_orchestrator.
- `backend_kind` (function) `modules/llm_orchestrator.py:175` `def backend_kind(model_spec)` -- Return the provider prefix of a model spec.
- `is_error_reply` (function) `modules/llm_orchestrator.py:192` `def is_error_reply(text)` -- Return True when a reply is a backend error banner, not content.
- `is_placeholder_key` (function) `modules/llm_orchestrator.py:211` `def is_placeholder_key(value)` -- Return True when a key value is a shipped placeholder, not a secret.
- `complete_with_fallback` (function) `modules/llm_orchestrator.py:349` `def complete_with_fallback(prompt, system, max_tokens, api_key, members, executor, health, record)` -- Complete a prompt through the lazy_orchestrator chain with failover.

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

## modules/loop/worker_agentic.py
Depends on: `modules/__init__.py`, `modules/harness.py`, `modules/lazy_loop.py`, `modules/lazy_skills.py`
Imported by: `modules/loop/__init__.py`
- `run_command` (function) `modules/loop/worker_agentic.py:94` `def run_command(command, background)` -- Run one shell probe/verb through scope, guard and audit.
- `record_fact` (function) `modules/loop/worker_agentic.py:120` `def record_fact(text)` -- Persist one observed or inferred fact on the exploration graph.
- `report_finding` (function) `modules/loop/worker_agentic.py:129` `def report_finding(name, evidence, severity)` -- Record a verified vulnerability with its evidence.
- `traffic_search` (function) `modules/loop/worker_agentic.py:140` `def traffic_search(query)` -- Search captured command/traffic records by keyword.
- `graph_state` (function) `modules/loop/worker_agentic.py:153` `def graph_state()` -- Compact exploration overview: intents, facts, findings.
- `shell_open` (function) `modules/loop/worker_agentic.py:168` `def shell_open()` -- Open a persistent bash session for multi-step shell work.
- `shell_send` (function) `modules/loop/worker_agentic.py:172` `def shell_send(command)` -- Run one guarded command in the persistent shell session.
- `job_status` (function) `modules/loop/worker_agentic.py:176` `def job_status(job_id)` -- Report whether one background job is still running.
- `job_output` (function) `modules/loop/worker_agentic.py:184` `def job_output(job_id)` -- Return the tail of one background job's output.

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

## modules/loop_guardrails.py
Depends on: `modules/__init__.py`
Imported by: `modules/chain_runner.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `modules/loop/worker_memory.py`, `tests/test_loop_guardrails.py`, `tests/test_pacing.py`, `tests/test_repeat_shapes.py`
- `RepeatDetector.__init__` (method) `modules/loop_guardrails.py:110` `def __init__(self, window)`
- `RepeatDetector.record` (method) `modules/loop_guardrails.py:116` `def record(self, command)` -- Add one executed command; returns True when the window fills.
- `RepeatDetector.stuck` (method) `modules/loop_guardrails.py:151` `def stuck(self)` -- True when the loop is visibly not progressing.
- `RepeatDetector.oscillation_pair` (method) `modules/loop_guardrails.py:175` `def oscillation_pair(self)` -- Return the detected alternating pair, ('', '') when none.
- `RepeatDetector.last_commands` (method) `modules/loop_guardrails.py:179` `def last_commands(self)` -- Snapshot of the recent command window (oldest first).
- `RepeatDetector.reset` (method) `modules/loop_guardrails.py:183` `def reset(self)` -- Clear the window (operator intervention acknowledged).
- `EdrPacer.__init__` (method) `modules/loop_guardrails.py:206` `def __init__(self, duration_threshold)` -- Configure the pacer.
- `EdrPacer.parse_windows` (method) `modules/loop_guardrails.py:252` `def parse_windows(raw)` -- Parse ``HH:MM-HH:MM`` window strings into minute tuples.
- `EdrPacer.from_config` (method) `modules/loop_guardrails.py:274` `def from_config(cls)` -- Build a pacer from the orchestrator pacing configuration.
- `EdrPacer.observe` (method) `modules/loop_guardrails.py:305` `def observe(self, command, duration_sec, output)` -- Feed one executed step and update the telemetry estimate.
- `EdrPacer.decay` (method) `modules/loop_guardrails.py:327` `def decay(self, factor)` -- Cool the estimate down (call once per completed step).
- `EdrPacer.level` (method) `modules/loop_guardrails.py:333` `def level(self)` -- Current pacing level: 0 calm, 1 cautious, 2 stealth.
- `EdrPacer.signal` (method) `modules/loop_guardrails.py:343` `def signal(self)` -- Human-readable reason for the current level (may be empty).
- `EdrPacer.in_sleeper_window` (method) `modules/loop_guardrails.py:374` `def in_sleeper_window(self, now)` -- True when local time falls inside a configured quiet window.
- `EdrPacer.windows_delay` (method) `modules/loop_guardrails.py:380` `def windows_delay(windows, now)` -- Static quiet-window delay for callers without a pacer instance.
- `EdrPacer.sleeper_delay` (method) `modules/loop_guardrails.py:407` `def sleeper_delay(self, now)` -- Recommended sleep because of a quiet window (0 when outside).
- `EdrPacer.inter_step_delay` (method) `modules/loop_guardrails.py:420` `def inter_step_delay(self)` -- Recommended sleep before the next step at the current level.
- `EdrPacer.quieten` (method) `modules/loop_guardrails.py:437` `def quieten(self, command)` -- Return a quieter variant of the command at the current level.
- `EdrPacer.describe` (method) `modules/loop_guardrails.py:452` `def describe(self)` -- Return a snapshot of the pacer state for admin surfaces.
- `TargetLimiter.__init__` (method) `modules/loop_guardrails.py:475` `def __init__(self, max_concurrent)`
- `TargetLimiter.max_concurrent` (method) `modules/loop_guardrails.py:482` `def max_concurrent(self)` -- Configured upper bound of simultaneous targets.
- `TargetLimiter.active_targets` (method) `modules/loop_guardrails.py:487` `def active_targets(self)` -- How many distinct targets currently hold a slot.
- `TargetLimiter.slot` (method) `modules/loop_guardrails.py:493` `def slot(self, target)` -- Hold one of at most ``max_concurrent`` target slots.
- `FactVectorStore.__init__` (method) `modules/loop_guardrails.py:545` `def __init__(self, path, max_facts)`
- `FactVectorStore.path` (method) `modules/loop_guardrails.py:553` `def path(self)` -- Backing file path.
- `FactVectorStore.add` (method) `modules/loop_guardrails.py:574` `def add(self, text, meta)` -- Embed and store one fact; returns False for duplicates.
- `FactVectorStore.search` (method) `modules/loop_guardrails.py:608` `def search(self, query, k)` -- Return the ``k`` facts most similar to the query.
- `FactVectorStore.search_block` (method) `modules/loop_guardrails.py:638` `def search_block(self, query, k, max_chars)` -- Render retrieved facts as a prompt-ready block (may be empty).
- `FactVectorStore.clear` (method) `modules/loop_guardrails.py:647` `def clear(self)` -- Drop every fact (manual reset path).
- `FactVectorStore.save` (method) `modules/loop_guardrails.py:653` `def save(self)` -- Persist atomically; I/O errors never surface to the loop.

## modules/loop_manager.py
Imported by: `lazyc2.py`, `tests/test_loop_manager.py`
- `LoopValidationError.__init__` (method) `modules/loop_manager.py:90` `def __init__(self, field, message)` -- Store the offending field alongside the human message.
- `validate_target` (function) `modules/loop_manager.py:100` `def validate_target(raw)` -- Return the canonical string form of a validated IP address target.
- `sanitize_goal` (function) `modules/loop_manager.py:123` `def sanitize_goal(raw)` -- Return a safe goal string accepted by the loop parser.
- `clamp_int` (function) `modules/loop_manager.py:150` `def clamp_int(raw, field, default, minimum, maximum)` -- Parse and clamp an integer knob to the supported range.
- `clamp_float` (function) `modules/loop_manager.py:175` `def clamp_float(raw, field, default, minimum, maximum)` -- Parse and clamp a float knob to the supported range.
- `validate_loop_id` (function) `modules/loop_manager.py:200` `def validate_loop_id(loop_id)` -- Validate a loop id and return its normalized hex form.
- `LoopManager.__init__` (method) `modules/loop_manager.py:327` `def __init__(self, loops_dir, python_executable, max_concurrent, repo_root, lazyown_script)` -- Create the manager and its persistence lock.
- `LoopManager.loops_dir` (method) `modules/loop_manager.py:349` `def loops_dir(self)` -- Return the root directory for loop workspaces.
- `LoopManager.start` (method) `modules/loop_manager.py:353` `def start(self, spec, operator)` -- Validate, spawn and register one autonomous loop.
- `LoopManager.list_loops` (method) `modules/loop_manager.py:493` `def list_loops(self)` -- Return every registry record with refreshed live status.
- `LoopManager.get_loop` (method) `modules/loop_manager.py:528` `def get_loop(self, loop_id)` -- Return one registry record by id.
- `LoopManager.read_log` (method) `modules/loop_manager.py:547` `def read_log(self, loop_id, offset)` -- Read one chunk of a loop's output log.
- `LoopManager.stop` (method) `modules/loop_manager.py:614` `def stop(self, loop_id)` -- Stop one running loop by terminating its process group.
- `LoopManager.summary` (method) `modules/loop_manager.py:679` `def summary(self)` -- Return an aggregate view of loop activity for the report.

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


Next: [API_p17.md](API_p17.md)
