# Symbols (page 16 of 40)
Previous: [SYMBOLS_p15.md](SYMBOLS_p15.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `LessonIngestor` | class | `modules/lesson_ingestor.py:77` | `class LessonIngestor` |
| `LessonLearned` | class | `modules/lesson_ingestor.py:55` | `class LessonLearned` |
| `__init__` | method | `modules/lesson_ingestor.py:86` | `def __init__(self, lessons_file, router, trainer, boost_reward)` |
| `_expert_for_topic` | method | `modules/lesson_ingestor.py:122` | `def _expert_for_topic(self, topic)` |
| `_get_router` | method | `modules/lesson_ingestor.py:98` | `def _get_router(self)` |
| `_get_trainer` | method | `modules/lesson_ingestor.py:110` | `def _get_trainer(self)` |
| `_load_from_file` | method | `modules/lesson_ingestor.py:202` | `def _load_from_file(self)` |
| `from_dict` | method | `modules/lesson_ingestor.py:66` | `def from_dict(cls, d)` |
| `ingest` | method | `modules/lesson_ingestor.py:125` | `def ingest(self, lesson)` |
| `ingest_all` | method | `modules/lesson_ingestor.py:185` | `def ingest_all(self, lessons)` |
| `ingest_campaign_lessons` | function | `modules/lesson_ingestor.py:222` | `def ingest_campaign_lessons(lessons_file)` |
| `LogFileHandler` | class | `modules/lilsplunky.py:217` | `class LogFileHandler(FileSystemEventHandler)` |
| `__init__` | method | `modules/lilsplunky.py:223` | `def __init__(self, log_dir, mode)` |
| `analyze_with_deepseek` | function | `modules/lilsplunky.py:123` | `def analyze_with_deepseek(log_entry_data)` |
| `display_record` | function | `modules/lilsplunky.py:346` | `def display_record(record)` |
| `initialize_file_positions` | method | `modules/lilsplunky.py:229` | `def initialize_file_positions(self)` |
| `is_monitored` | method | `modules/lilsplunky.py:245` | `def is_monitored(self, file_path)` |
| `on_created` | method | `modules/lilsplunky.py:336` | `def on_created(self, event)` |
| `on_modified` | method | `modules/lilsplunky.py:331` | `def on_modified(self, event)` |
| `parse_args` | function | `modules/lilsplunky.py:446` | `def parse_args()` |
| `process_file` | method | `modules/lilsplunky.py:257` | `def process_file(self, file_path)` |
| `search_logs` | function | `modules/lilsplunky.py:382` | `def search_logs(query, file_path)` |
| `simple_parse_log_line` | function | `modules/lilsplunky.py:69` | `def simple_parse_log_line(line, file_path)` |
| `start_monitoring` | function | `modules/lilsplunky.py:413` | `def start_monitoring(log_dir, mode)` |
| `store_event` | function | `modules/lilsplunky.py:108` | `def store_event(event_data)` |
| `LinuxAdvancedConfig` | class | `modules/linux_advanced_payloads.py:64` | `class LinuxAdvancedConfig` |
| `LinuxAdvancedPayloadFactory` | class | `modules/linux_advanced_payloads.py:92` | `class LinuxAdvancedPayloadFactory` |
| `__init__` | method | `modules/linux_advanced_payloads.py:105` | `def __init__(self, config, output_dir)` |
| `_ip_to_hex` | method | `modules/linux_advanced_payloads.py:305` | `def _ip_to_hex(ip_str)` |
| `compile_c_source` | method | `modules/linux_advanced_payloads.py:707` | `def compile_c_source(self, source, output_name, shared)` |
| `generate_all` | method | `modules/linux_advanced_payloads.py:749` | `def generate_all(self)` |
| `generate_ebpf_payload` | method | `modules/linux_advanced_payloads.py:235` | `def generate_ebpf_payload(self)` |
| `generate_kernel_module` | method | `modules/linux_advanced_payloads.py:519` | `def generate_kernel_module(self)` |
| `generate_ld_preload_rootkit` | method | `modules/linux_advanced_payloads.py:110` | `def generate_ld_preload_rootkit(self)` |
| `generate_motd_backdoor` | method | `modules/linux_advanced_payloads.py:689` | `def generate_motd_backdoor(self)` |
| `generate_pam_backdoor` | method | `modules/linux_advanced_payloads.py:311` | `def generate_pam_backdoor(self)` |
| `generate_process_masquerade` | method | `modules/linux_advanced_payloads.py:632` | `def generate_process_masquerade(self)` |
| `generate_ssh_persistence` | method | `modules/linux_advanced_payloads.py:458` | `def generate_ssh_persistence(self)` |
| `generate_systemd_persistence` | method | `modules/linux_advanced_payloads.py:398` | `def generate_systemd_persistence(self)` |
| `generate_udev_persistence` | method | `modules/linux_advanced_payloads.py:676` | `def generate_udev_persistence(self)` |
| `list_hook_functions` | method | `modules/linux_advanced_payloads.py:793` | `def list_hook_functions()` |
| `list_persistence_methods` | method | `modules/linux_advanced_payloads.py:797` | `def list_persistence_methods()` |
| `Listener` | class | `modules/listener_manager.py:141` | `class Listener` |
| `ListenerManager` | class | `modules/listener_manager.py:172` | `class ListenerManager` |
| `__init__` | method | `modules/listener_manager.py:179` | `def __init__(self, app, sessions_dir, payload)` |
| `_bind_address` | method | `modules/listener_manager.py:191` | `def _bind_address(self, port)` |
| `_collect_listener_bind_candidates` | function | `modules/listener_manager.py:35` | `def _collect_listener_bind_candidates(payload)` |
| `_listeners_path` | method | `modules/listener_manager.py:201` | `def _listeners_path(self)` |
| `_load` | method | `modules/listener_manager.py:204` | `def _load(self)` |
| `_probe_listener_bind` | function | `modules/listener_manager.py:72` | `def _probe_listener_bind(address, port)` |
| `_resolve_listener_bind_address` | function | `modules/listener_manager.py:110` | `def _resolve_listener_bind_address(payload, port)` |
| `_save` | method | `modules/listener_manager.py:217` | `def _save(self)` |
| `_stop` | method | `modules/listener_manager.py:331` | `def _stop(self, listener)` |
| `add` | method | `modules/listener_manager.py:229` | `def add(self, port, ssl, listener_id)` |
| `from_dict` | method | `modules/listener_manager.py:162` | `def from_dict(cls, data)` |
| `get_default_port` | method | `modules/listener_manager.py:367` | `def get_default_port(self, fallback)` |
| `remove` | method | `modules/listener_manager.py:242` | `def remove(self, listener_id)` |
| `set_payload` | method | `modules/listener_manager.py:187` | `def set_payload(self, payload)` |
| `start` | method | `modules/listener_manager.py:255` | `def start(self, listener_id)` |
| `start_all` | method | `modules/listener_manager.py:344` | `def start_all(self)` |
| `status` | method | `modules/listener_manager.py:355` | `def status(self)` |
| `stop` | method | `modules/listener_manager.py:323` | `def stop(self, listener_id)` |
| `stop_all` | method | `modules/listener_manager.py:350` | `def stop_all(self)` |
| `to_dict` | method | `modules/listener_manager.py:152` | `def to_dict(self)` |
| `_emit_edge` | function | `modules/live_surface.py:126` | `def _emit_edge(source, target, relation, weight)` |
| `_emit_node` | function | `modules/live_surface.py:106` | `def _emit_node(node_id, state, title)` |
| `_group_for` | function | `modules/live_surface.py:55` | `def _group_for(node_id)` |
| `_is_compromised` | function | `modules/live_surface.py:45` | `def _is_compromised(state)` |
| `_label_for` | function | `modules/live_surface.py:64` | `def _label_for(node_id)` |
| `_node_value` | function | `modules/live_surface.py:50` | `def _node_value(centrality)` |
| `build_live_graph` | function | `modules/live_surface.py:72` | `def build_live_graph(world)` |
| `_complete` | function | `modules/llm_adapter.py:82` | `def _complete(client, full_prompt, model)` |
| `_configure_logging` | function | `modules/llm_adapter.py:65` | `def _configure_logging(debug)` |
| `_process` | function | `modules/llm_adapter.py:96` | `def _process(client, prompt, debug, template, config)` |
| `_read_error` | function | `modules/llm_adapter.py:78` | `def _read_error(prompt)` |
| `_read_prompt_file` | function | `modules/llm_adapter.py:70` | `def _read_prompt_file(prompt)` |
| `ask_general` | function | `modules/llm_adapter.py:254` | `def ask_general(prompt, debug)` |
| `process_prompt` | function | `modules/llm_adapter.py:119` | `def process_prompt(client, prompt, debug)` |
| `process_prompt_adversary` | function | `modules/llm_adapter.py:147` | `def process_prompt_adversary(client, prompt, debug)` |
| `process_prompt_general` | function | `modules/llm_adapter.py:161` | `def process_prompt_general(client, prompt, debug)` |
| `process_prompt_redop` | function | `modules/llm_adapter.py:237` | `def process_prompt_redop(client, prompt, debug)` |
| `process_prompt_script` | function | `modules/llm_adapter.py:133` | `def process_prompt_script(client, prompt, debug)` |
| `process_prompt_search` | function | `modules/llm_adapter.py:175` | `def process_prompt_search(client, prompt, debug)` |
| `process_prompt_task` | function | `modules/llm_adapter.py:189` | `def process_prompt_task(client, prompt, debug)` |
| `process_prompt_vuln` | function | `modules/llm_adapter.py:206` | `def process_prompt_vuln(client, prompt, debug, event)` |
| `safe_groq_client` | function | `modules/llm_adapter.py:48` | `def safe_groq_client(api_key)` |
| `LLMClient` | class | `modules/llm_client.py:45` | `class LLMClient` |
| `__init__` | method | `modules/llm_client.py:63` | `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)` |
| `_ask_groq` | method | `modules/llm_client.py:179` | `def _ask_groq(self, prompt, model, system, temperature)` |
| `_ask_llamacpp` | method | `modules/llm_client.py:242` | `def _ask_llamacpp(self, prompt, model, system)` |
| `_ask_ollama` | method | `modules/llm_client.py:220` | `def _ask_ollama(self, prompt, model)` |
| `ask` | method | `modules/llm_client.py:79` | `def ask(self, prompt)` |
| `ask` | function | `modules/llm_client.py:276` | `def ask(prompt)` |
| `classify` | method | `modules/llm_client.py:130` | `def classify(self, output)` |
| `classify` | function | `modules/llm_client.py:288` | `def classify(output)` |
| `get_client` | function | `modules/llm_client.py:268` | `def get_client(api_key)` |
| `summarize` | method | `modules/llm_client.py:159` | `def summarize(self, text)` |
| `summarize` | function | `modules/llm_client.py:293` | `def summarize(text)` |
| `DecisionRecord` | class | `modules/llm_evaluator.py:21` | `class DecisionRecord` |
| `JSONLRecorder` | class | `modules/llm_evaluator.py:75` | `class JSONLRecorder(OutcomeRecorder)` |
| `LLMEvaluator` | class | `modules/llm_evaluator.py:161` | `class LLMEvaluator` |
| `OutcomeRecorder` | class | `modules/llm_evaluator.py:55` | `class OutcomeRecorder(ABC)` |
| `QualityMetrics` | class | `modules/llm_evaluator.py:140` | `class QualityMetrics` |
| `__init__` | method | `modules/llm_evaluator.py:76` | `def __init__(self, path)` |
| `__init__` | method | `modules/llm_evaluator.py:162` | `def __init__(self, recorder)` |
| `_cli` | function | `modules/llm_evaluator.py:322` | `def _cli()` |
| `_new_id` | function | `modules/llm_evaluator.py:35` | `def _new_id()` |
| `_record_from_dict` | function | `modules/llm_evaluator.py:39` | `def _record_from_dict(d)` |
| `_safe_mean` | function | `modules/llm_evaluator.py:150` | `def _safe_mean(values)` |
| `_tactic_success_rates` | function | `modules/llm_evaluator.py:154` | `def _tactic_success_rates(records)` |
| `compute_metrics` | method | `modules/llm_evaluator.py:200` | `def compute_metrics(self, session_id)` |
| `export_finetuning_dataset` | method | `modules/llm_evaluator.py:256` | `def export_finetuning_dataset(self, path)` |
| `get_evaluator` | function | `modules/llm_evaluator.py:293` | `def get_evaluator()` |
| `load_all` | method | `modules/llm_evaluator.py:69` | `def load_all(self)` |
| `load_all` | method | `modules/llm_evaluator.py:120` | `def load_all(self)` |
| `load_by_session` | method | `modules/llm_evaluator.py:72` | `def load_by_session(self, session_id)` |
| `load_by_session` | method | `modules/llm_evaluator.py:135` | `def load_by_session(self, session_id)` |
| `quality_report` | method | `modules/llm_evaluator.py:241` | `def quality_report(self, session_id)` |
| `record` | method | `modules/llm_evaluator.py:57` | `def record(self, decision)` |
| `record` | method | `modules/llm_evaluator.py:81` | `def record(self, decision)` |
| `record_decision` | method | `modules/llm_evaluator.py:165` | `def record_decision(self, session_id, thought, action, mitre_tactic, expected_outcome, confidence)` |
| `record_decision` | function | `modules/llm_evaluator.py:302` | `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)` |
| `record_outcome` | method | `modules/llm_evaluator.py:191` | `def record_outcome(self, decision_id, actual_outcome, findings_count, success)` |
| `record_outcome` | function | `modules/llm_evaluator.py:313` | `def record_outcome(decision_id, actual_outcome, findings_count, success)` |
| `update_outcome` | method | `modules/llm_evaluator.py:60` | `def update_outcome(self, decision_id, actual, findings_count, success)` |
| `update_outcome` | method | `modules/llm_evaluator.py:86` | `def update_outcome(self, decision_id, actual, findings_count, success)` |
| `LLMBackendNotSupportedError` | class | `modules/llm_factory.py:188` | `class LLMBackendNotSupportedError(ValueError)` |
| `LLMBackendUnavailableError` | class | `modules/llm_factory.py:184` | `class LLMBackendUnavailableError(RuntimeError)` |
| `_build_anthropic` | function | `modules/llm_factory.py:476` | `def _build_anthropic(config)` |
| `_build_backend` | function | `modules/llm_factory.py:637` | `def _build_backend(normalized, resolved_config)` |
| `_build_deepseek` | function | `modules/llm_factory.py:498` | `def _build_deepseek(config)` |
| `_build_groq` | function | `modules/llm_factory.py:404` | `def _build_groq(config)` |
| `_build_llamacpp` | function | `modules/llm_factory.py:440` | `def _build_llamacpp(config)` |
| `_build_ollama` | function | `modules/llm_factory.py:426` | `def _build_ollama(config)` |
| `_build_openai` | function | `modules/llm_factory.py:454` | `def _build_openai(config)` |
| `_normalize_backend` | function | `modules/llm_factory.py:381` | `def _normalize_backend(backend)` |
| `_resolve_api_key` | function | `modules/llm_factory.py:327` | `def _resolve_api_key(config)` |
| `_resolve_api_key_for_backend` | function | `modules/llm_factory.py:350` | `def _resolve_api_key_for_backend(backend, config)` |
| `_resolve_model_identifier` | function | `modules/llm_factory.py:520` | `def _resolve_model_identifier(backend_identifier, config)` |
| `_wrap_with_budget` | function | `modules/llm_factory.py:547` | `def _wrap_with_budget(backend, config, backend_identifier)` |
| `api_key_config_key` | function | `modules/llm_factory.py:260` | `def api_key_config_key(backend)` |
| `backend_requires_api_key` | function | `modules/llm_factory.py:285` | `def backend_requires_api_key(backend)` |
| `complete` | function | `modules/llm_factory.py:788` | `def complete(model, prompt, max_tokens)` |
| `default_model_for` | function | `modules/llm_factory.py:218` | `def default_model_for(backend)` |
| `get_llm_backend` | function | `modules/llm_factory.py:585` | `def get_llm_backend(config, backend)` |
| `get_llm_backend_raw` | function | `modules/llm_factory.py:673` | `def get_llm_backend_raw(config, backend)` |
| `groq_model_chain` | function | `modules/llm_factory.py:139` | `def groq_model_chain(config)` |
| `is_model_missing_error` | function | `modules/llm_factory.py:119` | `def is_model_missing_error(message)` |
| `load_payload` | function | `modules/llm_factory.py:303` | `def load_payload(payload_path)` |
| `model_config_key` | function | `modules/llm_factory.py:239` | `def model_config_key(backend)` |
| `stream_complete` | function | `modules/llm_factory.py:719` | `def stream_complete(model, prompt, max_tokens, on_delta)` |
| `try_get_llm_backend` | function | `modules/llm_factory.py:695` | `def try_get_llm_backend(config, backend)` |
| `HealthRegistry` | class | `modules/llm_pool.py:75` | `class HealthRegistry` |
| `LLMPool` | class | `modules/llm_pool.py:176` | `class LLMPool` |
| `PoolConfig` | class | `modules/llm_pool.py:29` | `class PoolConfig` |
| `PoolExhausted` | class | `modules/llm_pool.py:42` | `class PoolExhausted(RuntimeError)` |
| `PoolMember` | class | `modules/llm_pool.py:64` | `class PoolMember` |
| `__init__` | method | `modules/llm_pool.py:83` | `def __init__(self, config)` |
| `__init__` | method | `modules/llm_pool.py:179` | `def __init__(self, members, health, config)` |
| `_backoff_for` | method | `modules/llm_pool.py:155` | `def _backoff_for(self, failures)` |
| `_health_path` | function | `modules/llm_pool.py:20` | `def _health_path()` |
| `_load` | method | `modules/llm_pool.py:92` | `def _load(self)` |
| `_ordered` | method | `modules/llm_pool.py:201` | `def _ordered(self)` |
| `_persist_locked` | method | `modules/llm_pool.py:116` | `def _persist_locked(self)` |
| `_truncate` | method | `modules/llm_pool.py:217` | `def _truncate(self, text, overflow_dir)` |
| `complete` | method | `modules/llm_pool.py:237` | `def complete(self, prompt, max_tokens, session_key, overflow_dir)` |
| `healthy` | method | `modules/llm_pool.py:163` | `def healthy(self, member_id)` |
| `members` | method | `modules/llm_pool.py:192` | `def members(self)` |
| `report_failure` | method | `modules/llm_pool.py:143` | `def report_failure(self, member_id, error)` |
| `report_success` | method | `modules/llm_pool.py:135` | `def report_success(self, member_id)` |
| `session_key` | method | `modules/llm_pool.py:196` | `def session_key(self, conversation_id, role, index)` |
| `shared_registry` | function | `modules/llm_pool.py:50` | `def shared_registry(config)` |
| `KnowledgeStore` | class | `modules/llm_prompts.py:286` | `class KnowledgeStore` |
| `LlmPromptConfig` | class | `modules/llm_prompts.py:111` | `class LlmPromptConfig` |
| `__init__` | method | `modules/llm_prompts.py:289` | `def __init__(self, path)` |
| `_payload_block` | function | `modules/llm_prompts.py:354` | `def _payload_block(config)` |
| `_prompt_adversary` | function | `modules/llm_prompts.py:393` | `def _prompt_adversary(base_prompt, kb_text, config)` |
| `_prompt_general` | function | `modules/llm_prompts.py:409` | `def _prompt_general(base_prompt, kb_text, config)` |
| `_prompt_oneliner` | function | `modules/llm_prompts.py:362` | `def _prompt_oneliner(base_prompt, kb_text, config)` |
| `_prompt_redop` | function | `modules/llm_prompts.py:462` | `def _prompt_redop(base_prompt, kb_text, config)` |
| `_prompt_script` | function | `modules/llm_prompts.py:378` | `def _prompt_script(base_prompt, kb_text, config)` |
| `_prompt_search` | function | `modules/llm_prompts.py:422` | `def _prompt_search(base_prompt, kb_text, config)` |
| `_prompt_task` | function | `modules/llm_prompts.py:450` | `def _prompt_task(base_prompt, kb_text, config)` |
| `_prompt_vuln` | function | `modules/llm_prompts.py:436` | `def _prompt_vuln(base_prompt, kb_text, config)` |
| `add` | method | `modules/llm_prompts.py:324` | `def add(self, prompt, response)` |
| `default_project_root` | function | `modules/llm_prompts.py:67` | `def default_project_root()` |
| `from_defaults` | method | `modules/llm_prompts.py:130` | `def from_defaults(cls, project_root)` |
| `knowledge_base_path` | method | `modules/llm_prompts.py:150` | `def knowledge_base_path(self, domain)` |
| `knowledge_store` | method | `modules/llm_prompts.py:238` | `def knowledge_store(self, domain)` |
| `load` | method | `modules/llm_prompts.py:297` | `def load(self)` |
| `load_event_tool_output` | method | `modules/llm_prompts.py:176` | `def load_event_tool_output(self, event_name)` |
| `load_payload_context` | method | `modules/llm_prompts.py:161` | `def load_payload_context(self)` |
| `load_plan_history` | method | `modules/llm_prompts.py:203` | `def load_plan_history(self)` |
| `load_report_context` | method | `modules/llm_prompts.py:218` | `def load_report_context(self)` |
| `relevant` | method | `modules/llm_prompts.py:335` | `def relevant(self, prompt, limit)` |
| `render` | method | `modules/llm_prompts.py:249` | `def render(self, template, base_prompt)` |
| `render_kb_tail` | function | `modules/llm_prompts.py:271` | `def render_kb_tail(lines)` |
| `resolve_model` | function | `modules/llm_prompts.py:76` | `def resolve_model(model)` |
| `save` | method | `modules/llm_prompts.py:312` | `def save(self, records)` |
| `truncate_message` | function | `modules/llm_prompts.py:95` | `def truncate_message(message, max_chars)` |
| `LogTamper` | class | `modules/log_tamper.py:95` | `class LogTamper` |
| `LogTamperConfig` | class | `modules/log_tamper.py:71` | `class LogTamperConfig` |
| `__init__` | method | `modules/log_tamper.py:105` | `def __init__(self, config)` |
| `auditd_disable_commands` | method | `modules/log_tamper.py:307` | `def auditd_disable_commands(self)` |
| `generate_all` | method | `modules/log_tamper.py:295` | `def generate_all(self)` |
| `linux_clear_commands` | method | `modules/log_tamper.py:176` | `def linux_clear_commands(self)` |
| `macos_clear_commands` | method | `modules/log_tamper.py:243` | `def macos_clear_commands(self)` |
| `sysmon_disable_commands` | method | `modules/log_tamper.py:341` | `def sysmon_disable_commands(self)` |
| `windows_clear_commands` | method | `modules/log_tamper.py:108` | `def windows_clear_commands(self)` |
| `ColoredFormatter` | class | `modules/logging_config.py:36` | `class ColoredFormatter(Formatter)` |
| `CorrelationFilter` | class | `modules/logging_config.py:91` | `class CorrelationFilter(Filter)` |
| `JsonFormatter` | class | `modules/logging_config.py:53` | `class JsonFormatter(Formatter)` |
| `ResilientRotatingFileHandler` | class | `modules/logging_config.py:103` | `class ResilientRotatingFileHandler(RotatingFileHandler)` |
| `_ensure_log_dir_writable` | function | `modules/logging_config.py:156` | `def _ensure_log_dir_writable(log_dir)` |
| `_use_json_format` | function | `modules/logging_config.py:235` | `def _use_json_format()` |
| `clear_correlation_id` | function | `modules/logging_config.py:144` | `def clear_correlation_id()` |
| `configure` | function | `modules/logging_config.py:244` | `def configure(level, log_dir, console, file, format_console, format_file, max_bytes, backup_count, module_levels)` |
| `emit` | method | `modules/logging_config.py:116` | `def emit(self, record)` |
| `filter` | method | `modules/logging_config.py:94` | `def filter(self, record)` |
| `format` | method | `modules/logging_config.py:39` | `def format(self, record)` |
| `format` | method | `modules/logging_config.py:72` | `def format(self, record)` |
| `get_correlation_id` | function | `modules/logging_config.py:139` | `def get_correlation_id()` |
| `get_logger` | function | `modules/logging_config.py:328` | `def get_logger(name, level)` |
| `handleError` | method | `modules/logging_config.py:122` | `def handleError(self, record)` |
| `reset` | function | `modules/logging_config.py:388` | `def reset()` |
| `set_correlation_id` | function | `modules/logging_config.py:134` | `def set_correlation_id(cid)` |
| `set_level` | function | `modules/logging_config.py:357` | `def set_level(name, level)` |
| `set_quiet` | function | `modules/logging_config.py:367` | `def set_quiet()` |
| `set_verbose` | function | `modules/logging_config.py:373` | `def set_verbose()` |
| `silence_module` | function | `modules/logging_config.py:379` | `def silence_module(name)` |
| `_hive_store` | function | `modules/loop_ai_bridge.py:101` | `def _hive_store(task_id, worker, kind, text)` |
| `_open` | function | `modules/loop_ai_bridge.py:104` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:130` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:152` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:171` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:192` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:214` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:235` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:269` | `def _open()` |
| `_singleton` | function | `modules/loop_ai_bridge.py:50` | `def _singleton(key, factory)` |
| `_stage` | function | `modules/loop_ai_bridge.py:64` | `def _stage(name, default)` |
| `ai_snapshot` | function | `modules/loop_ai_bridge.py:314` | `def ai_snapshot()` |
| `annotate_detection` | function | `modules/loop_ai_bridge.py:125` | `def annotate_detection(command, action_category)` |
| `moe_record_outcome` | function | `modules/loop_ai_bridge.py:166` | `def moe_record_outcome(expert_id, task_type, reward, detection_prob)` |
| `moe_route` | function | `modules/loop_ai_bridge.py:149` | `def moe_route(task_type, goal)` |
| `publish_loop_event` | function | `modules/loop_ai_bridge.py:74` | `def publish_loop_event(task_id, worker, kind, text, severity)` |
| `record_step` | function | `modules/loop_ai_bridge.py:249` | `def record_step(task_id, worker, command, output, detection_prob)` |
| `rl_save` | function | `modules/loop_ai_bridge.py:230` | `def rl_save()` |
| `rl_select` | function | `modules/loop_ai_bridge.py:185` | `def rl_select(task_type, phase, candidates, deterministic)` |
| `rl_update` | function | `modules/loop_ai_bridge.py:207` | `def rl_update(task_type, phase, action, reward, candidates, detection_prob)` |
| `stream_enabled` | function | `modules/loop_ai_bridge.py:304` | `def stream_enabled()` |
| `swan_available` | function | `modules/loop_ai_bridge.py:264` | `def swan_available()` |
| `swan_consult` | function | `modules/loop_ai_bridge.py:277` | `def swan_consult(prompt, task_type, phase, timeout)` |
| `LoopProgress` | class | `modules/loop_progress.py:169` | `class LoopProgress` |
| `LoopSnapshot` | class | `modules/loop_progress.py:80` | `class LoopSnapshot` |
| `__post_init__` | method | `modules/loop_progress.py:182` | `def __post_init__(self)` |
| `_footer` | method | `modules/loop_progress.py:306` | `def _footer(self, snapshot, elapsed)` |
| `_header` | method | `modules/loop_progress.py:282` | `def _header(self)` |
| `_milestone_line` | method | `modules/loop_progress.py:289` | `def _milestone_line(self, snapshot, states, current)` |
| `_render` | method | `modules/loop_progress.py:324` | `def _render(self, snapshot)` |
| `emit` | method | `modules/loop_progress.py:268` | `def emit(self, line)` |
| `live_mode` | method | `modules/loop_progress.py:195` | `def live_mode(self)` |
| `refresh` | method | `modules/loop_progress.py:246` | `def refresh(self, snapshot)` |
| `sanitize_line` | function | `modules/loop_progress.py:151` | `def sanitize_line(line, keep_ansi)` |
| `snap_to_states` | function | `modules/loop_progress.py:123` | `def snap_to_states(snapshot)` |
| `snapshot_from_overview` | function | `modules/loop_progress.py:99` | `def snapshot_from_overview(overview, record, activity_tail, elapsed_sec)` |
| `start` | method | `modules/loop_progress.py:202` | `def start(self)` |
| `stop` | method | `modules/loop_progress.py:229` | `def stop(self)` |
| `MacOSPayloadConfig` | class | `modules/macos_payloads.py:60` | `class MacOSPayloadConfig` |
| `MacOSPayloadFactory` | class | `modules/macos_payloads.py:88` | `class MacOSPayloadFactory` |
| `__init__` | method | `modules/macos_payloads.py:111` | `def __init__(self, config, output_dir)` |
| `_adho_codesign` | method | `modules/macos_payloads.py:192` | `def _adho_codesign(self, app_dir)` |
| `_obfuscate_shell` | method | `modules/macos_payloads.py:116` | `def _obfuscate_shell(self, code)` |
| `_reverse_shell_command` | method | `modules/macos_payloads.py:122` | `def _reverse_shell_command(self)` |
| `generate_all` | method | `modules/macos_payloads.py:470` | `def generate_all(self)` |
| `generate_app_bundle` | method | `modules/macos_payloads.py:137` | `def generate_app_bundle(self)` |
| `generate_launchd_persistence` | method | `modules/macos_payloads.py:212` | `def generate_launchd_persistence(self)` |
| `generate_osascript_dropper` | method | `modules/macos_payloads.py:314` | `def generate_osascript_dropper(self)` |
| `generate_persistence_scripts` | method | `modules/macos_payloads.py:398` | `def generate_persistence_scripts(self)` |
| `generate_phishing_dialog` | method | `modules/macos_payloads.py:447` | `def generate_phishing_dialog(self)` |
| `generate_swift_stager` | method | `modules/macos_payloads.py:335` | `def generate_swift_stager(self)` |
| `generate_tcc_bypass` | method | `modules/macos_payloads.py:268` | `def generate_tcc_bypass(self)` |
| `list_persistence_methods` | method | `modules/macos_payloads.py:522` | `def list_persistence_methods()` |
| `list_tcc_services` | method | `modules/macos_payloads.py:517` | `def list_tcc_services()` |
| `check_collision` | function | `modules/mario.py:105` | `def check_collision(x, y, layer)` |
| `AgentBridgeWorker` | class | `modules/mcp_agent_bridge.py:468` | `class AgentBridgeWorker` |
| `GroqAgentWorker` | class | `modules/mcp_agent_bridge.py:234` | `class GroqAgentWorker` |
| `OllamaReActWorker` | class | `modules/mcp_agent_bridge.py:367` | `class OllamaReActWorker` |
| `__init__` | method | `modules/mcp_agent_bridge.py:235` | `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)` |
| `__init__` | method | `modules/mcp_agent_bridge.py:368` | `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)` |
| `__init__` | method | `modules/mcp_agent_bridge.py:471` | `def __init__(self, agent_id, goal, backend, run_cmd, max_iterations)` |
| `_agent_file` | function | `modules/mcp_agent_bridge.py:141` | `def _agent_file(agent_id)` |
| `_make_client` | function | `modules/mcp_agent_bridge.py:39` | `def _make_client(backend)` |
| `_ollama_chat` | function | `modules/mcp_agent_bridge.py:92` | `def _ollama_chat(model, messages, max_tokens, timeout)` |
| `_parse` | method | `modules/mcp_agent_bridge.py:381` | `def _parse(self, text)` |
| `_read_log` | function | `modules/mcp_agent_bridge.py:150` | `def _read_log(agent_id)` |
| `_tools` | method | `modules/mcp_agent_bridge.py:248` | `def _tools(self)` |
| `_write_log` | function | `modules/mcp_agent_bridge.py:145` | `def _write_log(agent_id, entry)` |
| `dummy_runner` | function | `modules/mcp_agent_bridge.py:531` | `def dummy_runner(cmd)` |
| `get_agent_result` | function | `modules/mcp_agent_bridge.py:188` | `def get_agent_result(agent_id)` |
| `get_agent_status` | function | `modules/mcp_agent_bridge.py:163` | `def get_agent_status(agent_id)` |
| `list_agents` | function | `modules/mcp_agent_bridge.py:211` | `def list_agents(limit)` |
| `run` | method | `modules/mcp_agent_bridge.py:264` | `def run(self)` |
| `run` | method | `modules/mcp_agent_bridge.py:389` | `def run(self)` |
| `run` | method | `modules/mcp_agent_bridge.py:478` | `def run(self)` |
| `start_agent` | function | `modules/mcp_agent_bridge.py:508` | `def start_agent(goal, backend, lazyown_runner_fn, max_iterations)` |
| `MemoryCleaner` | class | `modules/memory_cleaner.py:50` | `class MemoryCleaner` |
| `MemoryCleanerConfig` | class | `modules/memory_cleaner.py:22` | `class MemoryCleanerConfig` |
| `__init__` | method | `modules/memory_cleaner.py:61` | `def __init__(self, config)` |
| `generate_on_exit_script` | method | `modules/memory_cleaner.py:255` | `def generate_on_exit_script(self)` |
| `linux_memory_cleanup` | method | `modules/memory_cleaner.py:151` | `def linux_memory_cleanup(self)` |
| `macos_memory_cleanup` | method | `modules/memory_cleaner.py:206` | `def macos_memory_cleanup(self)` |
| `windows_memory_cleanup` | method | `modules/memory_cleaner.py:64` | `def windows_memory_cleanup(self)` |
| `MemoryEntry` | class | `modules/memory_store.py:81` | `class MemoryEntry` |
| `MemoryStore` | class | `modules/memory_store.py:234` | `class MemoryStore` |
| `SQLiteBackend` | class | `modules/memory_store.py:129` | `class SQLiteBackend(StorageBackend)` |
| `StorageBackend` | class | `modules/memory_store.py:94` | `class StorageBackend(ABC)` |
| `__init__` | method | `modules/memory_store.py:130` | `def __init__(self, db_path)` |
| `__init__` | method | `modules/memory_store.py:237` | `def __init__(self, backend)` |
| `_cli` | function | `modules/memory_store.py:341` | `def _cli()` |
| `_connect` | method | `modules/memory_store.py:136` | `def _connect(self)` |
| `_fetch` | method | `modules/memory_store.py:172` | `def _fetch(self, sql, params)` |
| `_print_entries` | function | `modules/memory_store.py:328` | `def _print_entries(entries)` |
| `_row_to_entry` | function | `modules/memory_store.py:114` | `def _row_to_entry(row)` |
| `all_entries` | method | `modules/memory_store.py:108` | `def all_entries(self, limit)` |
| `all_entries` | method | `modules/memory_store.py:212` | `def all_entries(self, limit)` |
| `by_host` | method | `modules/memory_store.py:102` | `def by_host(self, host, top_k)` |
| `by_host` | method | `modules/memory_store.py:189` | `def by_host(self, host, top_k)` |
| `by_service` | method | `modules/memory_store.py:105` | `def by_service(self, service, top_k)` |
| `by_service` | method | `modules/memory_store.py:200` | `def by_service(self, service, top_k)` |
| `close` | method | `modules/memory_store.py:111` | `def close(self)` |
| `close` | method | `modules/memory_store.py:229` | `def close(self)` |
| `export_finetuning_dataset` | method | `modules/memory_store.py:284` | `def export_finetuning_dataset(self, path)` |
| `get_memory_store` | function | `modules/memory_store.py:303` | `def get_memory_store()` |
| `recall` | method | `modules/memory_store.py:267` | `def recall(self, query, top_k)` |
| `recall` | function | `modules/memory_store.py:324` | `def recall(query, top_k)` |
| `recall_by_host` | method | `modules/memory_store.py:270` | `def recall_by_host(self, host, top_k)` |
| `recall_for_service` | method | `modules/memory_store.py:273` | `def recall_for_service(self, service_name, top_k)` |
| `remember` | method | `modules/memory_store.py:240` | `def remember(self, session_id, host, tool, command, output, findings, success)` |
| `remember` | function | `modules/memory_store.py:312` | `def remember(session_id, host, tool, command, output, findings, success)` |
| `save` | method | `modules/memory_store.py:96` | `def save(self, entry)` |
| `save` | method | `modules/memory_store.py:145` | `def save(self, entry)` |
| `search` | method | `modules/memory_store.py:99` | `def search(self, query, top_k)` |
| `search` | method | `modules/memory_store.py:177` | `def search(self, query, top_k)` |
| `stats` | method | `modules/memory_store.py:276` | `def stats(self)` |
| `stats_raw` | method | `modules/memory_store.py:222` | `def stats_raw(self)` |
| `MetricRecord` | class | `modules/metrics.py:146` | `class MetricRecord` |
| `MetricsAggregator` | class | `modules/metrics.py:226` | `class MetricsAggregator` |
| `MetricsRecorder` | class | `modules/metrics.py:332` | `class MetricsRecorder` |
| `MetricsRegistry` | class | `modules/metrics.py:54` | `class MetricsRegistry` |
| `MetricsWriter` | class | `modules/metrics.py:181` | `class MetricsWriter` |
| `__init__` | method | `modules/metrics.py:63` | `def __init__(self)` |
| `__init__` | method | `modules/metrics.py:189` | `def __init__(self, path)` |
| `__init__` | method | `modules/metrics.py:339` | `def __init__(self, writer)` |
| `_labels_key` | function | `modules/metrics.py:126` | `def _labels_key(labels)` |
| `_percentile` | method | `modules/metrics.py:234` | `def _percentile(values, percentile)` |
| `_read_all` | method | `modules/metrics.py:388` | `def _read_all(self)` |
| `append` | method | `modules/metrics.py:206` | `def append(self, record)` |
| `get` | method | `modules/metrics.py:87` | `def get(self, name, labels)` |
| `get_recorder` | function | `modules/metrics.py:452` | `def get_recorder()` |
| `inc` | method | `modules/metrics.py:69` | `def inc(self, name, labels, value)` |
| `path` | method | `modules/metrics.py:201` | `def path(self)` |
| `path` | method | `modules/metrics.py:350` | `def path(self)` |
| `prometheus_text` | method | `modules/metrics.py:107` | `def prometheus_text(self)` |
| `record` | method | `modules/metrics.py:355` | `def record(self, command, args, duration_ms, success, exit_code, source)` |
| `reset_recorder_for_tests` | function | `modules/metrics.py:466` | `def reset_recorder_for_tests(writer)` |
| `summarize` | method | `modules/metrics.py:254` | `def summarize(cls, records, window_seconds, now_utc)` |
| `summarize` | method | `modules/metrics.py:416` | `def summarize(self, window_seconds)` |
| `tail` | method | `modules/metrics.py:430` | `def tail(self, n)` |
| `to_dict` | method | `modules/metrics.py:167` | `def to_dict(self)` |
| `MFABypassEngine` | class | `modules/mfa_bypass.py:121` | `class MFABypassEngine` |
| `MFABypassResult` | class | `modules/mfa_bypass.py:113` | `class MFABypassResult` |
| `MFATarget` | class | `modules/mfa_bypass.py:103` | `class MFATarget` |
| `__init__` | method | `modules/mfa_bypass.py:128` | `def __init__(self, sessions_dir)` |
| `enumerate_techniques` | method | `modules/mfa_bypass.py:133` | `def enumerate_techniques(self, target)` |
| `export_report` | method | `modules/mfa_bypass.py:303` | `def export_report(self)` |
| `generate_phishing_templates` | method | `modules/mfa_bypass.py:153` | `def generate_phishing_templates(self, target)` |
| `mfa_conditional_access_scan` | method | `modules/mfa_bypass.py:223` | `def mfa_conditional_access_scan(self, domain)` |
| `replay_oauth_token` | method | `modules/mfa_bypass.py:252` | `def replay_oauth_token(self, access_token, refresh_token)` |
| `saml_golden_ticket_check` | method | `modules/mfa_bypass.py:278` | `def saml_golden_ticket_check(self, adfs_server)` |
| `ModuleInfo` | class | `modules/module_registry.py:150` | `class ModuleInfo` |
| `ModuleRegistry` | class | `modules/module_registry.py:223` | `class ModuleRegistry` |
| `__contains__` | method | `modules/module_registry.py:536` | `def __contains__(self, name)` |
| `__init__` | method | `modules/module_registry.py:172` | `def __init__(self, name, module_type, author, version, description, category, path, source, params, enabled...` |
| `__init__` | method | `modules/module_registry.py:235` | `def __init__(self, base_dir)` |
| `__iter__` | method | `modules/module_registry.py:531` | `def __iter__(self)` |
| `__len__` | method | `modules/module_registry.py:526` | `def __len__(self)` |
| `__repr__` | method | `modules/module_registry.py:219` | `def __repr__(self)` |
| `_classify` | function | `modules/module_registry.py:47` | `def _classify(category)` |
| `_classify_module_source` | function | `modules/module_registry.py:118` | `def _classify_module_source(name, source)` |
| `_extract_docstring_summary` | function | `modules/module_registry.py:136` | `def _extract_docstring_summary(source)` |
| `_load_yaml` | method | `modules/module_registry.py:517` | `def _load_yaml(path)` |
| `_looks_discoverable` | method | `modules/module_registry.py:503` | `def _looks_discoverable(source)` |
| `_scan_playbooks` | method | `modules/module_registry.py:453` | `def _scan_playbooks(self)` |
| `_scan_plugins` | method | `modules/module_registry.py:379` | `def _scan_plugins(self)` |
| `_scan_python_modules` | method | `modules/module_registry.py:473` | `def _scan_python_modules(self)` |
| `_scan_tools` | method | `modules/module_registry.py:419` | `def _scan_tools(self)` |
| `_scan_yaml_addons` | method | `modules/module_registry.py:338` | `def _scan_yaml_addons(self)` |
| `by_type` | method | `modules/module_registry.py:321` | `def by_type(self, module_type)` |
| `deprecated_modules` | method | `modules/module_registry.py:315` | `def deprecated_modules(self)` |
| `format_module_detail` | function | `modules/module_registry.py:589` | `def format_module_detail(m)` |
| `format_module_table` | function | `modules/module_registry.py:542` | `def format_module_table(modules, cols)` |
| `get` | method | `modules/module_registry.py:269` | `def get(self, name)` |
| `get_instance` | method | `modules/module_registry.py:241` | `def get_instance(cls, base_dir)` |
| `rescan` | method | `modules/module_registry.py:260` | `def rescan(self)` |
| `scan` | method | `modules/module_registry.py:247` | `def scan(self)` |
| `search` | method | `modules/module_registry.py:275` | `def search(self, query, module_type, category, enabled_only, include_deprecated)` |
| `summary` | method | `modules/module_registry.py:325` | `def summary(self)` |
| `to_dict` | method | `modules/module_registry.py:202` | `def to_dict(self)` |
| `ExpertAvailabilityChecker` | class | `modules/moe_router.py:437` | `class ExpertAvailabilityChecker` |
| `ExpertPerformance` | class | `modules/moe_router.py:101` | `class ExpertPerformance` |
| `ExpertPerformanceStore` | class | `modules/moe_router.py:276` | `class ExpertPerformanceStore` |
| `ExpertProfile` | class | `modules/moe_router.py:83` | `class ExpertProfile` |
| `IExpertSelector` | class | `modules/moe_router.py:257` | `class IExpertSelector(ABC)` |
| `MoERouter` | class | `modules/moe_router.py:489` | `class MoERouter` |
| `SoftmaxSelector` | class | `modules/moe_router.py:368` | `class SoftmaxSelector(IExpertSelector)` |
| `__init__` | method | `modules/moe_router.py:283` | `def __init__(self, path)` |
| `__init__` | method | `modules/moe_router.py:377` | `def __init__(self, temperature)` |
| `__init__` | method | `modules/moe_router.py:443` | `def __init__(self)` |
| `__init__` | method | `modules/moe_router.py:500` | `def __init__(self, experts, selector, performance_store, api_key)` |
| `_anneal_temperature` | method | `modules/moe_router.py:645` | `def _anneal_temperature(self)` |
| `_available_for_task` | method | `modules/moe_router.py:640` | `def _available_for_task(self, task_type)` |
| `_check` | method | `modules/moe_router.py:458` | `def _check(expert, api_key)` |
| `_compute_weights` | method | `modules/moe_router.py:410` | `def _compute_weights(candidates, task_type, store)` |
| `_key` | method | `modules/moe_router.py:293` | `def _key(expert_id, task_type)` |
| `_load` | method | `modules/moe_router.py:350` | `def _load(self)` |
| `_load_groq_key` | function | `modules/moe_router.py:665` | `def _load_groq_key()` |
| `_save` | method | `modules/moe_router.py:341` | `def _save(self)` |
| `_softmax` | function | `modules/moe_router.py:423` | `def _softmax(values, temperature)` |
| `adjusted_weight` | function | `modules/moe_router.py:562` | `def adjusted_weight(ep)` |
| `all_for_task` | method | `modules/moe_router.py:321` | `def all_for_task(self, task_type)` |
| `ensemble` | method | `modules/moe_router.py:547` | `def ensemble(self, task_type, goal, n)` |
| `get` | method | `modules/moe_router.py:316` | `def get(self, expert_id, task_type)` |
| `get_expert` | method | `modules/moe_router.py:605` | `def get_expert(self, expert_id)` |
| `get_router` | function | `modules/moe_router.py:684` | `def get_router(api_key)` |
| `is_available` | method | `modules/moe_router.py:447` | `def is_available(self, expert, api_key)` |
| `is_local` | method | `modules/moe_router.py:96` | `def is_local(self)` |
| `performance_bonus` | method | `modules/moe_router.py:325` | `def performance_bonus(self, expert_id, task_type)` |
| `record` | method | `modules/moe_router.py:298` | `def record(self, expert_id, task_type, reward, detection_prob)` |
| `record_outcome` | method | `modules/moe_router.py:575` | `def record_outcome(self, expert_id, task_type, reward, detection_prob)` |
| `route` | method | `modules/moe_router.py:515` | `def route(self, task_type, goal, deterministic)` |
| `select` | method | `modules/moe_router.py:261` | `def select(self, candidates, task_type, performance_store, deterministic)` |
| `select` | method | `modules/moe_router.py:388` | `def select(self, candidates, task_type, performance_store, deterministic)` |
| `status_report` | method | `modules/moe_router.py:609` | `def status_report(self)` |
| `temperature` | method | `modules/moe_router.py:381` | `def temperature(self)` |
| `temperature` | method | `modules/moe_router.py:385` | `def temperature(self, value)` |
| `top_experts_for_task` | method | `modules/moe_router.py:589` | `def top_experts_for_task(self, task_type, top_k)` |
| `update` | method | `modules/moe_router.py:115` | `def update(self, reward, detection_prob)` |
| `MorseConfig` | class | `modules/morse.py:16` | `class MorseConfig` |
| `clear_screen` | function | `modules/morse.py:157` | `def clear_screen(config)` |
| `morse_to_text` | function | `modules/morse.py:130` | `def morse_to_text(morse_code, config)` |
| `read_choice` | function | `modules/morse.py:171` | `def read_choice(config)` |
| `reverse_morse_code` | function | `modules/morse.py:98` | `def reverse_morse_code()` |
| `run_driver` | function | `modules/morse.py:186` | `def run_driver(config)` |
| `text_to_morse` | function | `modules/morse.py:109` | `def text_to_morse(text, config)` |
| `ATTACKERS_IP` | macro | `modules/mysql_hookandroot_lib.c:64` | `#define ATTACKERS_IP` |
| `INJECTED_CONF` | macro | `modules/mysql_hookandroot_lib.c:66` | `#define INJECTED_CONF` |
| `SHELL_PORT` | macro | `modules/mysql_hookandroot_lib.c:65` | `#define SHELL_PORT` |
| `_GNU_SOURCE` | macro | `modules/mysql_hookandroot_lib.c:50` | `#define _GNU_SOURCE` |
| `execvp` | function | `modules/mysql_hookandroot_lib.c:128` | `int execvp(const char* filename, char* const argv[])` |
| `reverse_shell` | function | `modules/mysql_hookandroot_lib.c:74` | `void reverse_shell(void)` |
| `NetworkOpsecConfig` | class | `modules/network_opsec.py:23` | `class NetworkOpsecConfig` |
| `NetworkOpsecEngine` | class | `modules/network_opsec.py:53` | `class NetworkOpsecEngine` |
| `__init__` | method | `modules/network_opsec.py:83` | `def __init__(self, config)` |
| `_build_proxychains_config` | method | `modules/network_opsec.py:119` | `def _build_proxychains_config(proxies)` |
| `analyze_traffic_with_canary_check` | method | `modules/network_opsec.py:179` | `def analyze_traffic_with_canary_check(self, target_host, target_port)` |
| `canary_detection_setup` | method | `modules/network_opsec.py:317` | `def canary_detection_setup(self)` |
| `check_canary_tokens` | method | `modules/network_opsec.py:131` | `def check_canary_tokens(self)` |
| `configure_proxy_chain` | method | `modules/network_opsec.py:87` | `def configure_proxy_chain(self, chain_type)` |
| `connection_jitter_schedule` | method | `modules/network_opsec.py:294` | `def connection_jitter_schedule(self, beacon_interval)` |
| `dns_over_https_config` | method | `modules/network_opsec.py:246` | `def dns_over_https_config(self)` |
| `source_port_randomize` | method | `modules/network_opsec.py:269` | `def source_port_randomize(self)` |
| `summary` | method | `modules/network_opsec.py:349` | `def summary(self)` |
| `Host` | class | `modules/nmap2csv.py:176` | `class Host` |
| `Port` | class | `modules/nmap2csv.py:282` | `class Port` |
| `__init__` | method | `modules/nmap2csv.py:177` | `def __init__(self, ip, fqdn)` |
| `__init__` | method | `modules/nmap2csv.py:283` | `def __init__(self, number, protocol, service, version, script)` |
| `add_port` | method | `modules/nmap2csv.py:188` | `def add_port(self, port)` |
| `dottedquad_to_num` | function | `modules/nmap2csv.py:126` | `def dottedquad_to_num(ip)` |
| `extract_matching_pattern` | function | `modules/nmap2csv.py:156` | `def extract_matching_pattern(regex, group_name, unfiltered_list)` |
| `formatted_item` | function | `modules/nmap2csv.py:606` | `def formatted_item(host, format_item)` |
| `generate_csv` | function | `modules/nmap2csv.py:653` | `def generate_csv(fd, results, options)` |
| `get_fqdn` | method | `modules/nmap2csv.py:198` | `def get_fqdn(self)` |
| `get_ip_dotted_format` | method | `modules/nmap2csv.py:195` | `def get_ip_dotted_format(self)` |
| `get_ip_num_format` | method | `modules/nmap2csv.py:192` | `def get_ip_num_format(self)` |
| `get_mac_address` | method | `modules/nmap2csv.py:255` | `def get_mac_address(self)` |
| `get_mac_address_vendor` | method | `modules/nmap2csv.py:258` | `def get_mac_address_vendor(self)` |
| `get_network_distance` | method | `modules/nmap2csv.py:261` | `def get_network_distance(self)` |
| `get_number` | method | `modules/nmap2csv.py:290` | `def get_number(self)` |
| `get_os` | method | `modules/nmap2csv.py:252` | `def get_os(self)` |
| `get_port_list` | method | `modules/nmap2csv.py:204` | `def get_port_list(self)` |
| `get_port_number_list` | method | `modules/nmap2csv.py:207` | `def get_port_number_list(self)` |
| `get_port_protocol_list` | method | `modules/nmap2csv.py:216` | `def get_port_protocol_list(self)` |

Next: [SYMBOLS_p17.md](SYMBOLS_p17.md)
