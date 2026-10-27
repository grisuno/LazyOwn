# Symbols (page 18 of 46)
Previous: [SYMBOLS_p17.md](SYMBOLS_p17.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `EdrPacer` | class | `modules/loop_guardrails.py:126` | `class EdrPacer` |
| `Fact` | class | `modules/loop_guardrails.py:73` | `class Fact` |
| `FactVectorStore` | class | `modules/loop_guardrails.py:278` | `class FactVectorStore` |
| `RepeatDetector` | class | `modules/loop_guardrails.py:82` | `class RepeatDetector` |
| `TargetLimiter` | class | `modules/loop_guardrails.py:208` | `class TargetLimiter` |
| `__init__` | method | `modules/loop_guardrails.py:89` | `def __init__(self, window)` |
| `__init__` | method | `modules/loop_guardrails.py:135` | `def __init__(self, duration_threshold)` |
| `__init__` | method | `modules/loop_guardrails.py:216` | `def __init__(self, max_concurrent)` |
| `__init__` | method | `modules/loop_guardrails.py:286` | `def __init__(self, path, max_facts)` |
| `__len__` | method | `modules/loop_guardrails.py:298` | `def __len__(self)` |
| `_load` | method | `modules/loop_guardrails.py:415` | `def _load(self)` |
| `_tokenize` | method | `modules/loop_guardrails.py:302` | `def _tokenize(text)` |
| `_vectorize` | method | `modules/loop_guardrails.py:307` | `def _vectorize(tokens)` |
| `active_targets` | method | `modules/loop_guardrails.py:228` | `def active_targets(self)` |
| `add` | method | `modules/loop_guardrails.py:315` | `def add(self, text, meta)` |
| `clear` | method | `modules/loop_guardrails.py:388` | `def clear(self)` |
| `decay` | method | `modules/loop_guardrails.py:163` | `def decay(self, factor)` |
| `inter_step_delay` | method | `modules/loop_guardrails.py:184` | `def inter_step_delay(self)` |
| `last_commands` | method | `modules/loop_guardrails.py:117` | `def last_commands(self)` |
| `level` | method | `modules/loop_guardrails.py:169` | `def level(self)` |
| `max_concurrent` | method | `modules/loop_guardrails.py:223` | `def max_concurrent(self)` |
| `observe` | method | `modules/loop_guardrails.py:141` | `def observe(self, command, duration_sec, output)` |
| `path` | method | `modules/loop_guardrails.py:294` | `def path(self)` |
| `quieten` | method | `modules/loop_guardrails.py:192` | `def quieten(self, command)` |
| `record` | method | `modules/loop_guardrails.py:93` | `def record(self, command)` |
| `reset` | method | `modules/loop_guardrails.py:121` | `def reset(self)` |
| `save` | method | `modules/loop_guardrails.py:394` | `def save(self)` |
| `search` | method | `modules/loop_guardrails.py:349` | `def search(self, query, k)` |
| `search_block` | method | `modules/loop_guardrails.py:379` | `def search_block(self, query, k, max_chars)` |
| `signal` | method | `modules/loop_guardrails.py:179` | `def signal(self)` |
| `slot` | method | `modules/loop_guardrails.py:234` | `def slot(self, target)` |
| `stuck` | method | `modules/loop_guardrails.py:110` | `def stuck(self)` |
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
| `TriggerStore` | class | `modules/loop_triggers.py:23` | `class TriggerStore` |
| `__init__` | method | `modules/loop_triggers.py:26` | `def __init__(self, task_id)` |
| `_core` | function | `modules/loop_triggers.py:16` | `def _core()` |
| `_load` | method | `modules/loop_triggers.py:32` | `def _load(self)` |
| `add` | method | `modules/loop_triggers.py:36` | `def add(self, kind, arg, every_sec)` |
| `due` | method | `modules/loop_triggers.py:155` | `def due(self, task_id, graph, activity, assets, store)` |
| `ensure_cve_hot_trigger` | method | `modules/loop_triggers.py:142` | `def ensure_cve_hot_trigger(self)` |
| `ensure_service_trigger` | method | `modules/loop_triggers.py:129` | `def ensure_service_trigger(self)` |
| `list` | method | `modules/loop_triggers.py:125` | `def list(self)` |
| `remove` | method | `modules/loop_triggers.py:100` | `def remove(self, trigger_id)` |
| `set_enabled` | method | `modules/loop_triggers.py:111` | `def set_enabled(self, trigger_id, enabled)` |
| `upsert_defaults` | method | `modules/loop_triggers.py:58` | `def upsert_defaults(self, seeds)` |
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
| `ActivityLogPort` | class | `modules/mediation/contracts.py:35` | `class ActivityLogPort(Protocol)` |
| `LlmCompletionPort` | class | `modules/mediation/contracts.py:57` | `class LlmCompletionPort(Protocol)` |
| `MediationDomains` | class | `modules/mediation/contracts.py:12` | `class MediationDomains` |
| `MediationHubContract` | class | `modules/mediation/contracts.py:95` | `class MediationHubContract(Protocol)` |
| `MediatorContract` | class | `modules/mediation/contracts.py:84` | `class MediatorContract(Protocol)` |
| `complete` | method | `modules/mediation/contracts.py:60` | `def complete(self, prompt, max_tokens, task_id)` |
| `describe` | method | `modules/mediation/contracts.py:89` | `def describe(self)` |
| `has_members` | method | `modules/mediation/contracts.py:78` | `def has_members(self)` |
| `is_known` | method | `modules/mediation/contracts.py:23` | `def is_known(cls, domain)` |
| `mediator_for` | method | `modules/mediation/contracts.py:98` | `def mediator_for(self, domain)` |
| `read` | method | `modules/mediation/contracts.py:44` | `def read(self, limit)` |
| `resolve` | function | `modules/mediation/contracts.py:103` | `def resolve(domain)` |
| `FeedbackMediator` | class | `modules/mediation/feedback_mediator.py:13` | `class FeedbackMediator` |
| `describe` | method | `modules/mediation/feedback_mediator.py:18` | `def describe(self)` |
| `order_steps` | method | `modules/mediation/feedback_mediator.py:22` | `def order_steps(self, steps, stack)` |
| `MediationHub` | class | `modules/mediation/hub.py:19` | `class MediationHub` |
| `__init__` | method | `modules/mediation/hub.py:22` | `def __init__(self)` |
| `_build_default` | function | `modules/mediation/hub.py:55` | `def _build_default()` |
| `default_hub` | function | `modules/mediation/hub.py:73` | `def default_hub()` |
| `get_hub` | function | `modules/mediation/hub.py:78` | `def get_hub()` |
| `mediator_for` | method | `modules/mediation/hub.py:35` | `def mediator_for(self, domain)` |
| `register` | method | `modules/mediation/hub.py:26` | `def register(self, mediator)` |
| `snapshot` | method | `modules/mediation/hub.py:46` | `def snapshot(self)` |
| `IntelMediator` | class | `modules/mediation/intel_mediator.py:13` | `class IntelMediator` |
| `__init__` | method | `modules/mediation/intel_mediator.py:18` | `def __init__(self)` |
| `activity_records` | method | `modules/mediation/intel_mediator.py:39` | `def activity_records(self, task_id, limit)` |
| `describe` | method | `modules/mediation/intel_mediator.py:32` | `def describe(self)` |
| `mask_configured` | method | `modules/mediation/intel_mediator.py:133` | `def mask_configured(self, text)` |
| `record_routing_decision` | method | `modules/mediation/intel_mediator.py:64` | `def record_routing_decision(self, task_id, intent_id, command, intent_text, target, stack)` |
| `record_routing_outcome` | method | `modules/mediation/intel_mediator.py:97` | `def record_routing_outcome(self, task_id, intent_id, command, state, facts, findings, stack)` |
| `register_activity_log_factory` | method | `modules/mediation/intel_mediator.py:22` | `def register_activity_log_factory(self, factory)` |
| `stack_signature` | method | `modules/mediation/intel_mediator.py:149` | `def stack_signature(self, assets)` |
| `TelemetryMediator` | class | `modules/mediation/telemetry_mediator.py:14` | `class TelemetryMediator` |
| `annotate_detection` | method | `modules/mediation/telemetry_mediator.py:43` | `def annotate_detection(self, command)` |
| `describe` | method | `modules/mediation/telemetry_mediator.py:19` | `def describe(self)` |
| `moe_record_outcome` | method | `modules/mediation/telemetry_mediator.py:151` | `def moe_record_outcome(self, expert_id, task_type, reward, detection_prob)` |
| `moe_route` | method | `modules/mediation/telemetry_mediator.py:110` | `def moe_route(self, task_type)` |
| `publish_event` | method | `modules/mediation/telemetry_mediator.py:23` | `def publish_event(self, task_id, worker, kind, text, severity)` |
| `record_step` | method | `modules/mediation/telemetry_mediator.py:59` | `def record_step(self, task_id, worker, command, output, detection_prob)` |
| `rl_select` | method | `modules/mediation/telemetry_mediator.py:126` | `def rl_select(self, task_type, phase, candidates, deterministic)` |
| `rl_update` | method | `modules/mediation/telemetry_mediator.py:167` | `def rl_update(self, task_type, phase, action, reward, candidates, detection_prob)` |
| `swan_available` | method | `modules/mediation/telemetry_mediator.py:76` | `def swan_available(self)` |
| `swan_consult` | method | `modules/mediation/telemetry_mediator.py:85` | `def swan_consult(self, prompt, task_type, phase, timeout)` |
| `MemoryCleaner` | class | `modules/memory_cleaner.py:50` | `class MemoryCleaner` |
| `MemoryCleanerConfig` | class | `modules/memory_cleaner.py:22` | `class MemoryCleanerConfig` |
| `__init__` | method | `modules/memory_cleaner.py:61` | `def __init__(self, config)` |
| `generate_on_exit_script` | method | `modules/memory_cleaner.py:255` | `def generate_on_exit_script(self)` |
| `linux_memory_cleanup` | method | `modules/memory_cleaner.py:151` | `def linux_memory_cleanup(self)` |
| `macos_memory_cleanup` | method | `modules/memory_cleaner.py:206` | `def macos_memory_cleanup(self)` |
| `windows_memory_cleanup` | method | `modules/memory_cleaner.py:64` | `def windows_memory_cleanup(self)` |
| `EmbeddingError` | class | `modules/memory_embeddings.py:30` | `class EmbeddingError(ValueError)` |
| `_fnv1a` | function | `modules/memory_embeddings.py:34` | `def _fnv1a(data)` |
| `_tokens` | function | `modules/memory_embeddings.py:41` | `def _tokens(text)` |
| `as_floats` | function | `modules/memory_embeddings.py:109` | `def as_floats(blob)` |
| `cosine` | function | `modules/memory_embeddings.py:75` | `def cosine(a, b)` |
| `embed` | function | `modules/memory_embeddings.py:50` | `def embed(text)` |
| `semantic_top_k` | function | `modules/memory_embeddings.py:85` | `def semantic_top_k(query, candidates, top_k)` |
| `MemoryEntry` | class | `modules/memory_store.py:84` | `class MemoryEntry` |
| `MemoryStore` | class | `modules/memory_store.py:237` | `class MemoryStore` |
| `SQLiteBackend` | class | `modules/memory_store.py:132` | `class SQLiteBackend(StorageBackend)` |
| `StorageBackend` | class | `modules/memory_store.py:97` | `class StorageBackend(ABC)` |
| `VectorSQLiteBackend` | class | `modules/memory_store.py:315` | `class VectorSQLiteBackend(SQLiteBackend)` |
| `__init__` | method | `modules/memory_store.py:133` | `def __init__(self, db_path)` |
| `__init__` | method | `modules/memory_store.py:240` | `def __init__(self, backend)` |
| `_cli` | function | `modules/memory_store.py:381` | `def _cli()` |
| `_connect` | method | `modules/memory_store.py:139` | `def _connect(self)` |
| `_fetch` | method | `modules/memory_store.py:175` | `def _fetch(self, sql, params)` |
| `_print_entries` | function | `modules/memory_store.py:368` | `def _print_entries(entries)` |
| `_row_to_entry` | function | `modules/memory_store.py:117` | `def _row_to_entry(row)` |
| `all_entries` | method | `modules/memory_store.py:111` | `def all_entries(self, limit)` |
| `all_entries` | method | `modules/memory_store.py:215` | `def all_entries(self, limit)` |
| `by_host` | method | `modules/memory_store.py:105` | `def by_host(self, host, top_k)` |
| `by_host` | method | `modules/memory_store.py:192` | `def by_host(self, host, top_k)` |
| `by_service` | method | `modules/memory_store.py:108` | `def by_service(self, service, top_k)` |
| `by_service` | method | `modules/memory_store.py:203` | `def by_service(self, service, top_k)` |
| `close` | method | `modules/memory_store.py:114` | `def close(self)` |
| `close` | method | `modules/memory_store.py:232` | `def close(self)` |
| `export_finetuning_dataset` | method | `modules/memory_store.py:300` | `def export_finetuning_dataset(self, path)` |
| `get_memory_store` | function | `modules/memory_store.py:339` | `def get_memory_store()` |
| `recall` | method | `modules/memory_store.py:270` | `def recall(self, query, top_k)` |
| `recall` | function | `modules/memory_store.py:360` | `def recall(query, top_k)` |
| `recall_by_host` | method | `modules/memory_store.py:273` | `def recall_by_host(self, host, top_k)` |
| `recall_for_service` | method | `modules/memory_store.py:276` | `def recall_for_service(self, service_name, top_k)` |
| `recall_hybrid` | method | `modules/memory_store.py:279` | `def recall_hybrid(self, query, top_k)` |
| `recall_hybrid` | function | `modules/memory_store.py:364` | `def recall_hybrid(query, top_k)` |
| `remember` | method | `modules/memory_store.py:243` | `def remember(self, session_id, host, tool, command, output, findings, success)` |
| `remember` | function | `modules/memory_store.py:348` | `def remember(session_id, host, tool, command, output, findings, success)` |
| `save` | method | `modules/memory_store.py:99` | `def save(self, entry)` |
| `save` | method | `modules/memory_store.py:148` | `def save(self, entry)` |
| `save` | method | `modules/memory_store.py:320` | `def save(self, entry)` |
| `search` | method | `modules/memory_store.py:102` | `def search(self, query, top_k)` |
| `search` | method | `modules/memory_store.py:180` | `def search(self, query, top_k)` |
| `search_semantic` | method | `modules/memory_store.py:328` | `def search_semantic(self, query, top_k)` |
| `stats` | method | `modules/memory_store.py:292` | `def stats(self)` |
| `stats_raw` | method | `modules/memory_store.py:225` | `def stats_raw(self)` |
| `_load_yaml` | function | `modules/metasploitable_gym.py:30` | `def _load_yaml(path)` |
| `chain_for` | function | `modules/metasploitable_gym.py:62` | `def chain_for(vuln_id, path)` |
| `exploit_for` | function | `modules/metasploitable_gym.py:72` | `def exploit_for(vuln_id, path)` |
| `get` | function | `modules/metasploitable_gym.py:53` | `def get(vuln_id, path)` |
| `load_index` | function | `modules/metasploitable_gym.py:42` | `def load_index(path)` |
| `main` | function | `modules/metasploitable_gym.py:157` | `def main()` |
| `summary` | function | `modules/metasploitable_gym.py:138` | `def summary(path)` |
| `validate_matrix` | function | `modules/metasploitable_gym.py:82` | `def validate_matrix(path)` |
| `vulnerabilities` | function | `modules/metasploitable_gym.py:47` | `def vulnerabilities(path)` |
| `Migration` | class | `modules/metasploitable_migrations.py:129` | `class Migration` |
| `_core_services_apply` | function | `modules/metasploitable_migrations.py:180` | `def _core_services_apply()` |
| `_docker_exec` | function | `modules/metasploitable_migrations.py:150` | `def _docker_exec(container, script, payload, timeout)` |
| `apply_migrations` | function | `modules/metasploitable_migrations.py:354` | `def apply_migrations(container, subnet)` |
| `build_migrations` | function | `modules/metasploitable_migrations.py:194` | `def build_migrations(subnet)` |
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

Next: [SYMBOLS_p19.md](SYMBOLS_p19.md)
