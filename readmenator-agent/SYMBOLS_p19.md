# Symbols (page 19 of 50)
Previous: [SYMBOLS_p18.md](SYMBOLS_p18.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `_stop` | method | `modules/listener_manager.py:343` | `def _stop(self, listener)` |
| `add` | method | `modules/listener_manager.py:229` | `def add(self, port, ssl, listener_id)` |
| `from_dict` | method | `modules/listener_manager.py:162` | `def from_dict(cls, data)` |
| `get_default_port` | method | `modules/listener_manager.py:379` | `def get_default_port(self, fallback)` |
| `remove` | method | `modules/listener_manager.py:242` | `def remove(self, listener_id)` |
| `set_payload` | method | `modules/listener_manager.py:187` | `def set_payload(self, payload)` |
| `start` | method | `modules/listener_manager.py:255` | `def start(self, listener_id)` |
| `start_all` | method | `modules/listener_manager.py:356` | `def start_all(self)` |
| `status` | method | `modules/listener_manager.py:367` | `def status(self)` |
| `stop` | method | `modules/listener_manager.py:335` | `def stop(self, listener_id)` |
| `stop_all` | method | `modules/listener_manager.py:362` | `def stop_all(self)` |
| `to_dict` | method | `modules/listener_manager.py:152` | `def to_dict(self)` |
| `_emit_edge` | function | `modules/live_surface.py:126` | `def _emit_edge(source, target, relation, weight)` |
| `_emit_node` | function | `modules/live_surface.py:106` | `def _emit_node(node_id, state, title)` |
| `_group_for` | function | `modules/live_surface.py:55` | `def _group_for(node_id)` |
| `_is_compromised` | function | `modules/live_surface.py:45` | `def _is_compromised(state)` |
| `_label_for` | function | `modules/live_surface.py:64` | `def _label_for(node_id)` |
| `_node_value` | function | `modules/live_surface.py:50` | `def _node_value(centrality)` |
| `build_live_graph` | function | `modules/live_surface.py:72` | `def build_live_graph(world)` |
| `_complete` | function | `modules/llm_adapter.py:89` | `def _complete(client, full_prompt, model)` |
| `_configure_logging` | function | `modules/llm_adapter.py:72` | `def _configure_logging(debug)` |
| `_orchestrated` | function | `modules/llm_adapter.py:124` | `def _orchestrated(full_prompt, prompt, store, primary_error)` |
| `_process` | function | `modules/llm_adapter.py:103` | `def _process(client, prompt, debug, template, config)` |
| `_read_error` | function | `modules/llm_adapter.py:85` | `def _read_error(prompt)` |
| `_read_prompt_file` | function | `modules/llm_adapter.py:77` | `def _read_prompt_file(prompt)` |
| `ask_general` | function | `modules/llm_adapter.py:290` | `def ask_general(prompt, debug)` |
| `process_prompt` | function | `modules/llm_adapter.py:155` | `def process_prompt(client, prompt, debug)` |
| `process_prompt_adversary` | function | `modules/llm_adapter.py:183` | `def process_prompt_adversary(client, prompt, debug)` |
| `process_prompt_general` | function | `modules/llm_adapter.py:197` | `def process_prompt_general(client, prompt, debug)` |
| `process_prompt_redop` | function | `modules/llm_adapter.py:273` | `def process_prompt_redop(client, prompt, debug)` |
| `process_prompt_script` | function | `modules/llm_adapter.py:169` | `def process_prompt_script(client, prompt, debug)` |
| `process_prompt_search` | function | `modules/llm_adapter.py:211` | `def process_prompt_search(client, prompt, debug)` |
| `process_prompt_task` | function | `modules/llm_adapter.py:225` | `def process_prompt_task(client, prompt, debug)` |
| `process_prompt_vuln` | function | `modules/llm_adapter.py:242` | `def process_prompt_vuln(client, prompt, debug, event)` |
| `safe_groq_client` | function | `modules/llm_adapter.py:55` | `def safe_groq_client(api_key)` |
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
| `LLMBackendNotSupportedError` | class | `modules/llm_factory.py:194` | `class LLMBackendNotSupportedError(ValueError)` |
| `LLMBackendUnavailableError` | class | `modules/llm_factory.py:190` | `class LLMBackendUnavailableError(RuntimeError)` |
| `_build_anthropic` | function | `modules/llm_factory.py:544` | `def _build_anthropic(config)` |
| `_build_backend` | function | `modules/llm_factory.py:705` | `def _build_backend(normalized, resolved_config)` |
| `_build_deepseek` | function | `modules/llm_factory.py:566` | `def _build_deepseek(config)` |
| `_build_groq` | function | `modules/llm_factory.py:472` | `def _build_groq(config)` |
| `_build_llamacpp` | function | `modules/llm_factory.py:508` | `def _build_llamacpp(config)` |
| `_build_ollama` | function | `modules/llm_factory.py:494` | `def _build_ollama(config)` |
| `_build_openai` | function | `modules/llm_factory.py:522` | `def _build_openai(config)` |
| `_is_placeholder_key` | function | `modules/llm_factory.py:333` | `def _is_placeholder_key(value)` |
| `_normalize_backend` | function | `modules/llm_factory.py:407` | `def _normalize_backend(backend)` |
| `_pi_complete` | function | `modules/llm_factory.py:807` | `def _pi_complete(model, prompt, max_tokens)` |
| `_pi_timeout` | function | `modules/llm_factory.py:795` | `def _pi_timeout()` |
| `_require_cloud_allowed` | function | `modules/llm_factory.py:440` | `def _require_cloud_allowed(normalized)` |
| `_resolve_api_key` | function | `modules/llm_factory.py:353` | `def _resolve_api_key(config)` |
| `_resolve_api_key_for_backend` | function | `modules/llm_factory.py:376` | `def _resolve_api_key_for_backend(backend, config)` |
| `_resolve_model_identifier` | function | `modules/llm_factory.py:588` | `def _resolve_model_identifier(backend_identifier, config)` |
| `_wrap_with_budget` | function | `modules/llm_factory.py:615` | `def _wrap_with_budget(backend, config, backend_identifier)` |
| `api_key_config_key` | function | `modules/llm_factory.py:266` | `def api_key_config_key(backend)` |
| `backend_requires_api_key` | function | `modules/llm_factory.py:291` | `def backend_requires_api_key(backend)` |
| `complete` | function | `modules/llm_factory.py:919` | `def complete(model, prompt, max_tokens)` |
| `default_model_for` | function | `modules/llm_factory.py:224` | `def default_model_for(backend)` |
| `get_llm_backend` | function | `modules/llm_factory.py:653` | `def get_llm_backend(config, backend)` |
| `get_llm_backend_raw` | function | `modules/llm_factory.py:749` | `def get_llm_backend_raw(config, backend)` |
| `groq_model_chain` | function | `modules/llm_factory.py:141` | `def groq_model_chain(config)` |
| `is_model_missing_error` | function | `modules/llm_factory.py:121` | `def is_model_missing_error(message)` |
| `load_payload` | function | `modules/llm_factory.py:309` | `def load_payload(payload_path)` |
| `model_config_key` | function | `modules/llm_factory.py:245` | `def model_config_key(backend)` |
| `stream_complete` | function | `modules/llm_factory.py:848` | `def stream_complete(model, prompt, max_tokens, on_delta)` |
| `try_get_llm_backend` | function | `modules/llm_factory.py:771` | `def try_get_llm_backend(config, backend)` |
| `OrchestratorResult` | class | `modules/llm_orchestrator.py:92` | `class OrchestratorResult` |
| `_bare_model_name` | function | `modules/llm_orchestrator.py:423` | `def _bare_model_name(model_spec)` |
| `_blank_error` | function | `modules/llm_orchestrator.py:87` | `def _blank_error(message)` |
| `_breaker_active` | function | `modules/llm_orchestrator.py:288` | `def _breaker_active()` |
| `_dedupe` | function | `modules/llm_orchestrator.py:229` | `def _dedupe(chain)` |
| `_default_health` | function | `modules/llm_orchestrator.py:278` | `def _default_health()` |
| `_ensure_groq_env_key` | function | `modules/llm_orchestrator.py:242` | `def _ensure_groq_env_key(api_key)` |
| `_exhausted_result` | function | `modules/llm_orchestrator.py:512` | `def _exhausted_result(attempts, specs, record)` |
| `_factory_executor` | function | `modules/llm_orchestrator.py:308` | `def _factory_executor(model_spec, prompt, max_tokens)` |
| `_ledger_record` | function | `modules/llm_orchestrator.py:298` | `def _ledger_record(name, ok, text)` |
| `_notice_fallback` | function | `modules/llm_orchestrator.py:330` | `def _notice_fallback(primary, attempts, served)` |
| `_walk_chain` | function | `modules/llm_orchestrator.py:431` | `def _walk_chain(chain, walk, health, attempts, specs, max_tokens, system, prompt, record, healthy_only, skipped)` |
| `_weight` | function | `modules/llm_orchestrator.py:139` | `def _weight(member)` |
| `backend_kind` | function | `modules/llm_orchestrator.py:175` | `def backend_kind(model_spec)` |
| `complete_with_fallback` | function | `modules/llm_orchestrator.py:349` | `def complete_with_fallback(prompt, system, max_tokens, api_key, members, executor, health, record)` |
| `display_text` | method | `modules/llm_orchestrator.py:123` | `def display_text(self)` |
| `is_error_reply` | function | `modules/llm_orchestrator.py:192` | `def is_error_reply(text)` |
| `is_placeholder_key` | function | `modules/llm_orchestrator.py:211` | `def is_placeholder_key(value)` |
| `ok` | method | `modules/llm_orchestrator.py:118` | `def ok(self)` |
| `pool_chain` | function | `modules/llm_orchestrator.py:148` | `def pool_chain()` |
| `sort_members` | function | `modules/llm_orchestrator.py:130` | `def sort_members(members)` |
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
| `WorkerAgenticMixin` | class | `modules/loop/worker_agentic.py:11` | `class WorkerAgenticMixin` |
| `_agent_checkpoint` | method | `modules/loop/worker_agentic.py:21` | `def _agent_checkpoint(self, intent)` |
| `_agent_preflight` | method | `modules/loop/worker_agentic.py:49` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/loop/worker_agentic.py:265` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/loop/worker_agentic.py:82` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agentic_try` | method | `modules/loop/worker_agentic.py:299` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_drain_steer` | method | `modules/loop/worker_agentic.py:38` | `def _drain_steer(self, intent)` |
| `_llm_steps` | method | `modules/loop/worker_agentic.py:419` | `def _llm_steps(self, intent, prior_text)` |
| `_with_llm_steps` | method | `modules/loop/worker_agentic.py:399` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `graph_state` | function | `modules/loop/worker_agentic.py:153` | `def graph_state()` |
| `job_output` | function | `modules/loop/worker_agentic.py:184` | `def job_output(job_id)` |
| `job_status` | function | `modules/loop/worker_agentic.py:176` | `def job_status(job_id)` |
| `record_fact` | function | `modules/loop/worker_agentic.py:120` | `def record_fact(text)` |
| `report_finding` | function | `modules/loop/worker_agentic.py:129` | `def report_finding(name, evidence, severity)` |
| `run_command` | function | `modules/loop/worker_agentic.py:94` | `def run_command(command, background)` |
| `shell_open` | function | `modules/loop/worker_agentic.py:168` | `def shell_open()` |
| `shell_send` | function | `modules/loop/worker_agentic.py:172` | `def shell_send(command)` |
| `traffic_search` | function | `modules/loop/worker_agentic.py:140` | `def traffic_search(query)` |
| `WorkerExecutionMixin` | class | `modules/loop/worker_execution.py:10` | `class WorkerExecutionMixin` |
| `_auto_approve` | method | `modules/loop/worker_execution.py:164` | `def _auto_approve(self, command)` |
| `_close_shell_session` | method | `modules/loop/worker_execution.py:126` | `def _close_shell_session(self)` |
| `_denied` | method | `modules/loop/worker_execution.py:153` | `def _denied(self, command)` |
| `_missing_tool` | method | `modules/loop/worker_execution.py:176` | `def _missing_tool(self, command)` |
| `_open_shell_session` | method | `modules/loop/worker_execution.py:55` | `def _open_shell_session(self, intent)` |
| `_reader` | function | `modules/loop/worker_execution.py:77` | `def _reader()` |
| `_resolved_command` | method | `modules/loop/worker_execution.py:242` | `def _resolved_command(self, command)` |
| `_run` | method | `modules/loop/worker_execution.py:192` | `def _run(self, command, executor)` |
| `_send_shell` | method | `modules/loop/worker_execution.py:90` | `def _send_shell(self, command, intent, timeout_sec)` |
| `_start_background_job` | method | `modules/loop/worker_execution.py:22` | `def _start_background_job(self, command, intent, transcripts)` |
| `_work` | function | `modules/loop/worker_execution.py:35` | `def _work()` |
| `WorkerGatingMixin` | class | `modules/loop/worker_gating.py:6` | `class WorkerGatingMixin` |
| `_command_in_scope` | method | `modules/loop/worker_gating.py:157` | `def _command_in_scope(self, command)` |
| `_lab_scope_default` | method | `modules/loop/worker_gating.py:48` | `def _lab_scope_default(self, target)` |
| `_learn_os` | method | `modules/loop/worker_gating.py:106` | `def _learn_os(self, intent, command, output)` |
| `_os_gate` | method | `modules/loop/worker_gating.py:80` | `def _os_gate(self, intent, command)` |
| `_scope_allows_target` | method | `modules/loop/worker_gating.py:17` | `def _scope_allows_target(self, target)` |
| `_sudo_guard` | method | `modules/loop/worker_gating.py:130` | `def _sudo_guard(self, intent, command)` |
| `WorkerMemoryMixin` | class | `modules/loop/worker_memory.py:6` | `class WorkerMemoryMixin` |
| `_absorb_reaction` | method | `modules/loop/worker_memory.py:62` | `def _absorb_reaction(self, intent, command, output)` |
| `_fact_memory_store` | method | `modules/loop/worker_memory.py:38` | `def _fact_memory_store(self)` |
| `_failure_memory` | method | `modules/loop/worker_memory.py:18` | `def _failure_memory(self)` |
| `_recall_facts` | method | `modules/loop/worker_memory.py:55` | `def _recall_facts(self, query, k)` |
| `_remember_fact` | method | `modules/loop/worker_memory.py:46` | `def _remember_fact(self, intent, command, output)` |
| `_hive_store` | function | `modules/loop_ai_bridge.py:101` | `def _hive_store(task_id, worker, kind, text)` |
| `_open` | function | `modules/loop_ai_bridge.py:104` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:260` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:285` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:307` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:326` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:347` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:369` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:390` | `def _open()` |
| `_open` | function | `modules/loop_ai_bridge.py:424` | `def _open()` |
| `_singleton` | function | `modules/loop_ai_bridge.py:50` | `def _singleton(key, factory)` |
| `_stage` | function | `modules/loop_ai_bridge.py:64` | `def _stage(name, default)` |
| `ai_snapshot` | function | `modules/loop_ai_bridge.py:469` | `def ai_snapshot()` |
| `annotate_detection` | function | `modules/loop_ai_bridge.py:280` | `def annotate_detection(command, action_category)` |
| `assess_opsec` | function | `modules/loop_ai_bridge.py:125` | `def assess_opsec(command, rhost)` |
| `intent_tool_class` | function | `modules/loop_ai_bridge.py:169` | `def intent_tool_class(summary)` |
| `moe_record_outcome` | function | `modules/loop_ai_bridge.py:321` | `def moe_record_outcome(expert_id, task_type, reward, detection_prob)` |
| `moe_route` | function | `modules/loop_ai_bridge.py:304` | `def moe_route(task_type, goal)` |
| `publish_loop_event` | function | `modules/loop_ai_bridge.py:74` | `def publish_loop_event(task_id, worker, kind, text, severity)` |
| `record_outcome_quality` | function | `modules/loop_ai_bridge.py:213` | `def record_outcome_quality(worker, intent_summary, facts, findings)` |
| `record_step` | function | `modules/loop_ai_bridge.py:404` | `def record_step(task_id, worker, command, output, detection_prob)` |
| `rl_save` | function | `modules/loop_ai_bridge.py:385` | `def rl_save()` |
| `rl_select` | function | `modules/loop_ai_bridge.py:340` | `def rl_select(task_type, phase, candidates, deterministic)` |
| `rl_update` | function | `modules/loop_ai_bridge.py:362` | `def rl_update(task_type, phase, action, reward, candidates, detection_prob)` |
| `stream_enabled` | function | `modules/loop_ai_bridge.py:459` | `def stream_enabled()` |
| `swan_available` | function | `modules/loop_ai_bridge.py:419` | `def swan_available()` |
| `swan_consult` | function | `modules/loop_ai_bridge.py:432` | `def swan_consult(prompt, task_type, phase, timeout)` |
| `tool_class_yields` | function | `modules/loop_ai_bridge.py:240` | `def tool_class_yields(summaries, phase)` |
| `EdrPacer` | class | `modules/loop_guardrails.py:190` | `class EdrPacer` |
| `Fact` | class | `modules/loop_guardrails.py:85` | `class Fact` |
| `FactVectorStore` | class | `modules/loop_guardrails.py:537` | `class FactVectorStore` |
| `RepeatDetector` | class | `modules/loop_guardrails.py:94` | `class RepeatDetector` |
| `TargetLimiter` | class | `modules/loop_guardrails.py:467` | `class TargetLimiter` |
| `__init__` | method | `modules/loop_guardrails.py:110` | `def __init__(self, window)` |
| `__init__` | method | `modules/loop_guardrails.py:206` | `def __init__(self, duration_threshold)` |
| `__init__` | method | `modules/loop_guardrails.py:475` | `def __init__(self, max_concurrent)` |
| `__init__` | method | `modules/loop_guardrails.py:545` | `def __init__(self, path, max_facts)` |
| `__len__` | method | `modules/loop_guardrails.py:557` | `def __len__(self)` |
| `_alternating` | method | `modules/loop_guardrails.py:167` | `def _alternating(self)` |
| `_load` | method | `modules/loop_guardrails.py:674` | `def _load(self)` |
| `_strict_alternating` | method | `modules/loop_guardrails.py:146` | `def _strict_alternating(entries)` |
| `_tokenize` | method | `modules/loop_guardrails.py:561` | `def _tokenize(text)` |
| `_update_oscillation` | method | `modules/loop_guardrails.py:132` | `def _update_oscillation(self)` |
| `_vectorize` | method | `modules/loop_guardrails.py:566` | `def _vectorize(tokens)` |
| `_window_seconds_until_end` | method | `modules/loop_guardrails.py:349` | `def _window_seconds_until_end(windows, now)` |
| `active_targets` | method | `modules/loop_guardrails.py:487` | `def active_targets(self)` |
| `add` | method | `modules/loop_guardrails.py:574` | `def add(self, text, meta)` |
| `clear` | method | `modules/loop_guardrails.py:647` | `def clear(self)` |
| `decay` | method | `modules/loop_guardrails.py:327` | `def decay(self, factor)` |
| `describe` | method | `modules/loop_guardrails.py:452` | `def describe(self)` |
| `from_config` | method | `modules/loop_guardrails.py:274` | `def from_config(cls)` |
| `in_sleeper_window` | method | `modules/loop_guardrails.py:374` | `def in_sleeper_window(self, now)` |
| `inter_step_delay` | method | `modules/loop_guardrails.py:420` | `def inter_step_delay(self)` |
| `last_commands` | method | `modules/loop_guardrails.py:179` | `def last_commands(self)` |
| `level` | method | `modules/loop_guardrails.py:333` | `def level(self)` |
| `max_concurrent` | method | `modules/loop_guardrails.py:482` | `def max_concurrent(self)` |
| `observe` | method | `modules/loop_guardrails.py:305` | `def observe(self, command, duration_sec, output)` |
| `oscillation_pair` | method | `modules/loop_guardrails.py:175` | `def oscillation_pair(self)` |
| `parse_windows` | method | `modules/loop_guardrails.py:252` | `def parse_windows(raw)` |
| `path` | method | `modules/loop_guardrails.py:553` | `def path(self)` |
| `quieten` | method | `modules/loop_guardrails.py:437` | `def quieten(self, command)` |
| `record` | method | `modules/loop_guardrails.py:116` | `def record(self, command)` |
| `reset` | method | `modules/loop_guardrails.py:183` | `def reset(self)` |
| `save` | method | `modules/loop_guardrails.py:653` | `def save(self)` |
| `search` | method | `modules/loop_guardrails.py:608` | `def search(self, query, k)` |
| `search_block` | method | `modules/loop_guardrails.py:638` | `def search_block(self, query, k, max_chars)` |
| `signal` | method | `modules/loop_guardrails.py:343` | `def signal(self)` |
| `sleeper_delay` | method | `modules/loop_guardrails.py:407` | `def sleeper_delay(self, now)` |
| `slot` | method | `modules/loop_guardrails.py:493` | `def slot(self, target)` |
| `stuck` | method | `modules/loop_guardrails.py:151` | `def stuck(self)` |
| `windows_delay` | method | `modules/loop_guardrails.py:380` | `def windows_delay(windows, now)` |
| `LoopManager` | class | `modules/loop_manager.py:316` | `class LoopManager` |
| `LoopNotFoundError` | class | `modules/loop_manager.py:96` | `class LoopNotFoundError(KeyError)` |
| `LoopSpec` | class | `modules/loop_manager.py:264` | `class LoopSpec` |
| `LoopValidationError` | class | `modules/loop_manager.py:87` | `class LoopValidationError(ValueError)` |
| `__init__` | method | `modules/loop_manager.py:90` | `def __init__(self, field, message)` |
| `__init__` | method | `modules/loop_manager.py:327` | `def __init__(self, loops_dir, python_executable, max_concurrent, repo_root, lazyown_script)` |
| `_load_registry_locked` | method | `modules/loop_manager.py:764` | `def _load_registry_locked(self)` |
| `_loop_command` | function | `modules/loop_manager.py:284` | `def _loop_command(spec)` |
| `_now_iso` | function | `modules/loop_manager.py:217` | `def _now_iso()` |
| `_pid_alive` | function | `modules/loop_manager.py:246` | `def _pid_alive(pid, start_ticks)` |
| `_process_start_ticks` | function | `modules/loop_manager.py:222` | `def _process_start_ticks(pid)` |
| `_prune_locked` | method | `modules/loop_manager.py:715` | `def _prune_locked(self)` |
| `_reap` | method | `modules/loop_manager.py:470` | `def _reap(self, loop_id, process)` |
| `_refresh_log_bytes` | method | `modules/loop_manager.py:517` | `def _refresh_log_bytes(self, record)` |
| `_remove_workspace` | method | `modules/loop_manager.py:740` | `def _remove_workspace(self, loop_id)` |
| `_resolve_log_path` | method | `modules/loop_manager.py:588` | `def _resolve_log_path(self, record)` |
| `_save_registry_locked` | method | `modules/loop_manager.py:779` | `def _save_registry_locked(self, records)` |
| `_spawn_locked` | method | `modules/loop_manager.py:394` | `def _spawn_locked(self, spec, operator)` |
| `_update_status_locked` | method | `modules/loop_manager.py:662` | `def _update_status_locked(self, loop_id, status)` |
| `clamp_float` | function | `modules/loop_manager.py:175` | `def clamp_float(raw, field, default, minimum, maximum)` |
| `clamp_int` | function | `modules/loop_manager.py:150` | `def clamp_int(raw, field, default, minimum, maximum)` |
| `get_loop` | method | `modules/loop_manager.py:528` | `def get_loop(self, loop_id)` |
| `list_loops` | method | `modules/loop_manager.py:493` | `def list_loops(self)` |
| `loops_dir` | method | `modules/loop_manager.py:349` | `def loops_dir(self)` |
| `read_log` | method | `modules/loop_manager.py:547` | `def read_log(self, loop_id, offset)` |
| `sanitize_goal` | function | `modules/loop_manager.py:123` | `def sanitize_goal(raw)` |
| `start` | method | `modules/loop_manager.py:353` | `def start(self, spec, operator)` |
| `stop` | method | `modules/loop_manager.py:614` | `def stop(self, loop_id)` |
| `summary` | method | `modules/loop_manager.py:679` | `def summary(self)` |
| `validate_loop_id` | function | `modules/loop_manager.py:200` | `def validate_loop_id(loop_id)` |
| `validate_target` | function | `modules/loop_manager.py:100` | `def validate_target(raw)` |
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
| `TriggerStore` | class | `modules/loop_triggers.py:88` | `class TriggerStore` |
| `__init__` | method | `modules/loop_triggers.py:91` | `def __init__(self, task_id)` |
| `_core` | function | `modules/loop_triggers.py:81` | `def _core()` |
| `_load` | method | `modules/loop_triggers.py:97` | `def _load(self)` |
| `add` | method | `modules/loop_triggers.py:101` | `def add(self, kind, arg, every_sec)` |
| `due` | method | `modules/loop_triggers.py:233` | `def due(self, task_id, graph, activity, assets, store)` |
| `ensure_ad_surface_trigger` | method | `modules/loop_triggers.py:220` | `def ensure_ad_surface_trigger(self)` |
| `ensure_cve_hot_trigger` | method | `modules/loop_triggers.py:207` | `def ensure_cve_hot_trigger(self)` |
| `ensure_service_trigger` | method | `modules/loop_triggers.py:194` | `def ensure_service_trigger(self)` |
| `hint_fingerprint` | function | `modules/loop_triggers.py:28` | `def hint_fingerprint(row)` |
| `list` | method | `modules/loop_triggers.py:190` | `def list(self)` |
| `prune_hint_fingerprints` | function | `modules/loop_triggers.py:60` | `def prune_hint_fingerprints(store, now, ttl)` |
| `read_signing_evidence` | function | `modules/loop_triggers.py:499` | `def read_signing_evidence(store_dir)` |
| `remove` | method | `modules/loop_triggers.py:165` | `def remove(self, trigger_id)` |
| `set_enabled` | method | `modules/loop_triggers.py:176` | `def set_enabled(self, trigger_id, enabled)` |
| `upsert_defaults` | method | `modules/loop_triggers.py:123` | `def upsert_defaults(self, seeds)` |
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
| `ChainMediator` | class | `modules/mediation/chain_mediator.py:48` | `class ChainMediator` |
| `LlmPoolPort` | class | `modules/mediation/chain_mediator.py:13` | `class LlmPoolPort` |
| `__init__` | method | `modules/mediation/chain_mediator.py:53` | `def __init__(self)` |
| `complete` | method | `modules/mediation/chain_mediator.py:16` | `def complete(self, prompt, max_tokens, task_id)` |
| `describe` | method | `modules/mediation/chain_mediator.py:73` | `def describe(self)` |
| `has_members` | method | `modules/mediation/chain_mediator.py:34` | `def has_members(self)` |
| `llm` | method | `modules/mediation/chain_mediator.py:65` | `def llm(self)` |
| `register_llm_port` | method | `modules/mediation/chain_mediator.py:57` | `def register_llm_port(self, port)` |
| `ActivityLogPort` | class | `modules/mediation/contracts.py:36` | `class ActivityLogPort(Protocol)` |
| `LlmCompletionPort` | class | `modules/mediation/contracts.py:58` | `class LlmCompletionPort(Protocol)` |
| `MediationDomains` | class | `modules/mediation/contracts.py:12` | `class MediationDomains` |
| `MediationHubContract` | class | `modules/mediation/contracts.py:96` | `class MediationHubContract(Protocol)` |
| `MediatorContract` | class | `modules/mediation/contracts.py:85` | `class MediatorContract(Protocol)` |
| `complete` | method | `modules/mediation/contracts.py:61` | `def complete(self, prompt, max_tokens, task_id)` |
| `describe` | method | `modules/mediation/contracts.py:90` | `def describe(self)` |
| `has_members` | method | `modules/mediation/contracts.py:79` | `def has_members(self)` |
| `is_known` | method | `modules/mediation/contracts.py:24` | `def is_known(cls, domain)` |
| `mediator_for` | method | `modules/mediation/contracts.py:99` | `def mediator_for(self, domain)` |
| `read` | method | `modules/mediation/contracts.py:45` | `def read(self, limit)` |
| `resolve` | function | `modules/mediation/contracts.py:104` | `def resolve(domain)` |
| `EngineMediator` | class | `modules/mediation/engine_mediator.py:84` | `class EngineMediator` |
| `ExploitRetryPort` | class | `modules/mediation/engine_mediator.py:34` | `class ExploitRetryPort(Protocol)` |
| `ReactionPort` | class | `modules/mediation/engine_mediator.py:51` | `class ReactionPort(Protocol)` |
| `ReasoningPort` | class | `modules/mediation/engine_mediator.py:69` | `class ReasoningPort(Protocol)` |
| `analyse` | method | `modules/mediation/engine_mediator.py:54` | `def analyse(self, output, command, platform)` |
| `analyse` | method | `modules/mediation/engine_mediator.py:118` | `def analyse(self, output, command, platform)` |
| `describe` | method | `modules/mediation/engine_mediator.py:89` | `def describe(self)` |
| `reason` | method | `modules/mediation/engine_mediator.py:72` | `def reason(self, target)` |
| `reason` | method | `modules/mediation/engine_mediator.py:136` | `def reason(self, target)` |
| `retry_with_credentials` | method | `modules/mediation/engine_mediator.py:37` | `def retry_with_credentials(self, target, credentials)` |
| `retry_with_credentials` | method | `modules/mediation/engine_mediator.py:97` | `def retry_with_credentials(self, target, credentials)` |
| `FeedbackMediator` | class | `modules/mediation/feedback_mediator.py:13` | `class FeedbackMediator` |
| `describe` | method | `modules/mediation/feedback_mediator.py:18` | `def describe(self)` |
| `order_steps` | method | `modules/mediation/feedback_mediator.py:22` | `def order_steps(self, steps, stack)` |
| `MediationHub` | class | `modules/mediation/hub.py:19` | `class MediationHub` |
| `__init__` | method | `modules/mediation/hub.py:22` | `def __init__(self)` |
| `_build_default` | function | `modules/mediation/hub.py:55` | `def _build_default()` |
| `default_hub` | function | `modules/mediation/hub.py:75` | `def default_hub()` |
| `get_hub` | function | `modules/mediation/hub.py:80` | `def get_hub()` |
| `mediator_for` | method | `modules/mediation/hub.py:35` | `def mediator_for(self, domain)` |
| `register` | method | `modules/mediation/hub.py:26` | `def register(self, mediator)` |
| `snapshot` | method | `modules/mediation/hub.py:46` | `def snapshot(self)` |

Next: [SYMBOLS_p20.md](SYMBOLS_p20.md)
