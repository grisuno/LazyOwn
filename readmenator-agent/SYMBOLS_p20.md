# Symbols (page 20 of 54)
Previous: [SYMBOLS_p19.md](SYMBOLS_p19.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `record` | method | `modules/llm_evaluator.py:81` | `def record(self, decision)` |
| `record_decision` | method | `modules/llm_evaluator.py:165` | `def record_decision(self, session_id, thought, action, mitre_tactic, expected_outcome, confidence)` |
| `record_decision` | function | `modules/llm_evaluator.py:302` | `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)` |
| `record_outcome` | method | `modules/llm_evaluator.py:191` | `def record_outcome(self, decision_id, actual_outcome, findings_count, success)` |
| `record_outcome` | function | `modules/llm_evaluator.py:313` | `def record_outcome(decision_id, actual_outcome, findings_count, success)` |
| `update_outcome` | method | `modules/llm_evaluator.py:60` | `def update_outcome(self, decision_id, actual, findings_count, success)` |
| `update_outcome` | method | `modules/llm_evaluator.py:86` | `def update_outcome(self, decision_id, actual, findings_count, success)` |
| `LLMBackendNotSupportedError` | class | `modules/llm_factory.py:213` | `class LLMBackendNotSupportedError(ValueError)` |
| `LLMBackendUnavailableError` | class | `modules/llm_factory.py:209` | `class LLMBackendUnavailableError(RuntimeError)` |
| `_build_anthropic` | function | `modules/llm_factory.py:591` | `def _build_anthropic(config)` |
| `_build_backend` | function | `modules/llm_factory.py:781` | `def _build_backend(normalized, resolved_config)` |
| `_build_deepseek` | function | `modules/llm_factory.py:613` | `def _build_deepseek(config)` |
| `_build_groq` | function | `modules/llm_factory.py:519` | `def _build_groq(config)` |
| `_build_llamacpp` | function | `modules/llm_factory.py:555` | `def _build_llamacpp(config)` |
| `_build_ollama` | function | `modules/llm_factory.py:541` | `def _build_ollama(config)` |
| `_build_openai` | function | `modules/llm_factory.py:569` | `def _build_openai(config)` |
| `_build_opencode` | function | `modules/llm_factory.py:635` | `def _build_opencode(config)` |
| `_is_placeholder_key` | function | `modules/llm_factory.py:355` | `def _is_placeholder_key(value)` |
| `_normalize_backend` | function | `modules/llm_factory.py:453` | `def _normalize_backend(backend)` |
| `_pi_complete` | function | `modules/llm_factory.py:886` | `def _pi_complete(model, prompt, max_tokens)` |
| `_pi_timeout` | function | `modules/llm_factory.py:874` | `def _pi_timeout()` |
| `_pooled_key` | function | `modules/llm_factory.py:398` | `def _pooled_key(backend, config, fallback)` |
| `_require_cloud_allowed` | function | `modules/llm_factory.py:487` | `def _require_cloud_allowed(normalized)` |
| `_resolve_api_key` | function | `modules/llm_factory.py:375` | `def _resolve_api_key(config)` |
| `_resolve_api_key_for_backend` | function | `modules/llm_factory.py:421` | `def _resolve_api_key_for_backend(backend, config)` |
| `_resolve_model_identifier` | function | `modules/llm_factory.py:662` | `def _resolve_model_identifier(backend_identifier, config)` |
| `_wrap_with_budget` | function | `modules/llm_factory.py:691` | `def _wrap_with_budget(backend, config, backend_identifier)` |
| `api_key_config_key` | function | `modules/llm_factory.py:288` | `def api_key_config_key(backend)` |
| `backend_requires_api_key` | function | `modules/llm_factory.py:313` | `def backend_requires_api_key(backend)` |
| `complete` | function | `modules/llm_factory.py:998` | `def complete(model, prompt, max_tokens, temperature)` |
| `default_model_for` | function | `modules/llm_factory.py:246` | `def default_model_for(backend)` |
| `get_llm_backend` | function | `modules/llm_factory.py:729` | `def get_llm_backend(config, backend)` |
| `get_llm_backend_raw` | function | `modules/llm_factory.py:828` | `def get_llm_backend_raw(config, backend)` |
| `groq_model_chain` | function | `modules/llm_factory.py:157` | `def groq_model_chain(config)` |
| `is_model_missing_error` | function | `modules/llm_factory.py:137` | `def is_model_missing_error(message)` |
| `load_payload` | function | `modules/llm_factory.py:331` | `def load_payload(payload_path)` |
| `model_config_key` | function | `modules/llm_factory.py:267` | `def model_config_key(backend)` |
| `stream_complete` | function | `modules/llm_factory.py:927` | `def stream_complete(model, prompt, max_tokens, on_delta)` |
| `try_get_llm_backend` | function | `modules/llm_factory.py:850` | `def try_get_llm_backend(config, backend)` |
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
| `precheck_control` | function | `modules/loop/control_plane.py:23` | `def precheck_control(control, target, objective_id, step_n, emit, loop, wait_until_unpaused, poll_interval, max_wait)` |
| `RLStepResult` | class | `modules/loop/daemon_reward.py:104` | `class RLStepResult` |
| `_Trainer` | class | `modules/loop/daemon_reward.py:85` | `class _Trainer(Protocol)` |
| `_shell_evidence` | function | `modules/loop/daemon_reward.py:116` | `def _shell_evidence(output)` |
| `compute_step_reward` | function | `modules/loop/daemon_reward.py:126` | `def compute_step_reward(output, command, phase, success, findings, prev_cmds)` |
| `encode_state` | method | `modules/loop/daemon_reward.py:88` | `def encode_state(self, task_type, engagement_phase, recent_reward_ema)` |
| `record_rl_feedback` | function | `modules/loop/daemon_reward.py:189` | `def record_rl_feedback(trainer, source, command, phase, output, success, findings, prev_cmds, prior_ema, detection_prob)` |
| `save` | method | `modules/loop/daemon_reward.py:100` | `def save(self)` |
| `update` | method | `modules/loop/daemon_reward.py:90` | `def update(self, state, action, reward, next_state, candidates, detection_prob)` |
| `DecisionRecord` | class | `modules/loop/decision_log.py:143` | `class DecisionRecord` |
| `_canonical` | function | `modules/loop/decision_log.py:68` | `def _canonical(value)` |
| `_rotate` | function | `modules/loop/decision_log.py:182` | `def _rotate(path)` |
| `config_digest` | function | `modules/loop/decision_log.py:115` | `def config_digest(config)` |
| `context_digest` | function | `modules/loop/decision_log.py:90` | `def context_digest(ctx)` |
| `digest` | function | `modules/loop/decision_log.py:51` | `def digest(text)` |
| `filtered_rows` | function | `modules/loop/decision_log.py:248` | `def filtered_rows(items)` |
| `new_run_id` | function | `modules/loop/decision_log.py:137` | `def new_run_id()` |
| `read_records` | function | `modules/loop/decision_log.py:221` | `def read_records(path)` |
| `record` | function | `modules/loop/decision_log.py:192` | `def record(rec, path)` |
| `EngineProxyMixin` | class | `modules/loop/engine_proxy.py:4` | `class EngineProxyMixin` |
| `_maybe_proxy_gc` | method | `modules/loop/engine_proxy.py:157` | `def _maybe_proxy_gc(self)` |
| `ingest_proxy_traffic` | method | `modules/loop/engine_proxy.py:75` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `proxy_env` | method | `modules/loop/engine_proxy.py:66` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/loop/engine_proxy.py:16` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/loop/engine_proxy.py:60` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/loop/engine_proxy.py:52` | `def proxy_stop(self)` |
| `search_proxy_body` | method | `modules/loop/engine_proxy.py:130` | `def search_proxy_body(self, task_id, query, limit)` |
| `ObjectiveBootstrap` | class | `modules/loop/objective_bootstrap.py:26` | `class ObjectiveBootstrap` |
| `bootstrap_objective` | function | `modules/loop/objective_bootstrap.py:46` | `def bootstrap_objective(objective_id, objective_text, target, world_model, obs_parser, planner, emit, load_payload)` |
| `detect_target_os` | function | `modules/loop/target_os.py:42` | `def detect_target_os(target, loop)` |
| `os_id_for` | function | `modules/loop/target_os.py:93` | `def os_id_for(detected_os)` |
| `persist_detected_os` | function | `modules/loop/target_os.py:105` | `def persist_detected_os(objective_id, target, detected_os, world_model, emit, load_payload, sessions_dir, payload_file)` |
| `TriageScheduler` | class | `modules/loop/triage_scheduler.py:85` | `class TriageScheduler` |
| `__init__` | method | `modules/loop/triage_scheduler.py:92` | `def __init__(self, stop_loss_attempts, salvage_progress, hard_threshold)` |
| `_clamp01` | function | `modules/loop/triage_scheduler.py:31` | `def _clamp01(value)` |
| `_item` | function | `modules/loop/triage_scheduler.py:73` | `def _item(record)` |
| `estimate_difficulty` | function | `modules/loop/triage_scheduler.py:36` | `def estimate_difficulty(facts)` |
| `normal_key` | function | `modules/loop/triage_scheduler.py:156` | `def normal_key(record)` |
| `order` | method | `modules/loop/triage_scheduler.py:133` | `def order(self, records)` |
| `pick_next` | method | `modules/loop/triage_scheduler.py:172` | `def pick_next(self, records)` |
| `route` | method | `modules/loop/triage_scheduler.py:122` | `def route(self, record)` |
| `salvage_key` | function | `modules/loop/triage_scheduler.py:163` | `def salvage_key(record)` |
| `should_stop` | method | `modules/loop/triage_scheduler.py:110` | `def should_stop(self, record)` |
| `WorkerAgenticMixin` | class | `modules/loop/worker_agentic.py:225` | `class WorkerAgenticMixin` |
| `_agent_checkpoint` | method | `modules/loop/worker_agentic.py:235` | `def _agent_checkpoint(self, intent)` |
| `_agent_os_hint` | method | `modules/loop/worker_agentic.py:508` | `def _agent_os_hint(self, intent)` |
| `_agent_preflight` | method | `modules/loop/worker_agentic.py:263` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/loop/worker_agentic.py:524` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/loop/worker_agentic.py:296` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agent_verb_catalog` | method | `modules/loop/worker_agentic.py:480` | `def _agent_verb_catalog(self)` |
| `_agentic_try` | method | `modules/loop/worker_agentic.py:568` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state, deadline)` |
| `_blocked_verbs` | method | `modules/loop/worker_agentic.py:916` | `def _blocked_verbs(self)` |
| `_capable_member_chain` | function | `modules/loop/worker_agentic.py:60` | `def _capable_member_chain(members)` |
| `_decision_context` | method | `modules/loop/worker_agentic.py:1008` | `def _decision_context(self, intent)` |
| `_drain_steer` | method | `modules/loop/worker_agentic.py:252` | `def _drain_steer(self, intent)` |
| `_extract_llm_commands` | function | `modules/loop/worker_agentic.py:148` | `def _extract_llm_commands(reply)` |
| `_guard_filter` | method | `modules/loop/worker_agentic.py:1054` | `def _guard_filter(self, intent, candidates)` |
| `_guard_rules` | method | `modules/loop/worker_agentic.py:934` | `def _guard_rules(self)` |
| `_is_destructive_or_malformed` | function | `modules/loop/worker_agentic.py:43` | `def _is_destructive_or_malformed(command)` |
| `_is_placeholder_steps` | function | `modules/loop/worker_agentic.py:129` | `def _is_placeholder_steps(steps)` |
| `_llm_steps` | method | `modules/loop/worker_agentic.py:758` | `def _llm_steps(self, intent, prior_text)` |
| `_loop_deterministic` | function | `modules/loop/worker_agentic.py:112` | `def _loop_deterministic()` |
| `_planner_temperature` | function | `modules/loop/worker_agentic.py:87` | `def _planner_temperature()` |
| `_push` | function | `modules/loop/worker_agentic.py:170` | `def _push(value)` |
| `_record_deterministic_decision` | method | `modules/loop/worker_agentic.py:1085` | `def _record_deterministic_decision(self, intent, candidates, chosen, filtered)` |
| `_record_llm_decision` | method | `modules/loop/worker_agentic.py:956` | `def _record_llm_decision(self, intent, prompt, reply, candidates, chosen, filtered)` |
| `_strip_command` | function | `modules/loop/worker_agentic.py:143` | `def _strip_command(raw)` |
| `_try_json_commands` | function | `modules/loop/worker_agentic.py:189` | `def _try_json_commands(text)` |
| `_verb_of` | function | `modules/loop/worker_agentic.py:102` | `def _verb_of(command)` |
| `_with_llm_steps` | method | `modules/loop/worker_agentic.py:706` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `graph_state` | function | `modules/loop/worker_agentic.py:368` | `def graph_state()` |
| `job_output` | function | `modules/loop/worker_agentic.py:399` | `def job_output(job_id)` |
| `job_status` | function | `modules/loop/worker_agentic.py:391` | `def job_status(job_id)` |
| `record_fact` | function | `modules/loop/worker_agentic.py:335` | `def record_fact(text)` |
| `report_finding` | function | `modules/loop/worker_agentic.py:344` | `def report_finding(name, evidence, severity)` |
| `run_command` | function | `modules/loop/worker_agentic.py:308` | `def run_command(command, background)` |
| `shell_open` | function | `modules/loop/worker_agentic.py:383` | `def shell_open()` |
| `shell_send` | function | `modules/loop/worker_agentic.py:387` | `def shell_send(command)` |
| `traffic_search` | function | `modules/loop/worker_agentic.py:355` | `def traffic_search(query)` |
| `WorkerExecutionMixin` | class | `modules/loop/worker_execution.py:10` | `class WorkerExecutionMixin` |
| `_auto_approve` | method | `modules/loop/worker_execution.py:164` | `def _auto_approve(self, command)` |
| `_close_shell_session` | method | `modules/loop/worker_execution.py:126` | `def _close_shell_session(self)` |
| `_denied` | method | `modules/loop/worker_execution.py:153` | `def _denied(self, command)` |
| `_missing_tool` | method | `modules/loop/worker_execution.py:176` | `def _missing_tool(self, command)` |
| `_open_shell_session` | method | `modules/loop/worker_execution.py:55` | `def _open_shell_session(self, intent)` |
| `_reader` | function | `modules/loop/worker_execution.py:77` | `def _reader()` |
| `_resolved_command` | method | `modules/loop/worker_execution.py:239` | `def _resolved_command(self, command)` |
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
| `_attribute_outcome` | method | `modules/loop/worker_memory.py:122` | `def _attribute_outcome(self, intent, command, output)` |
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
| `_open` | function | `modules/loop_ai_bridge.py:440` | `def _open()` |
| `_singleton` | function | `modules/loop_ai_bridge.py:50` | `def _singleton(key, factory)` |
| `_stage` | function | `modules/loop_ai_bridge.py:64` | `def _stage(name, default)` |
| `ai_snapshot` | function | `modules/loop_ai_bridge.py:485` | `def ai_snapshot()` |
| `annotate_detection` | function | `modules/loop_ai_bridge.py:280` | `def annotate_detection(command, action_category)` |
| `assess_opsec` | function | `modules/loop_ai_bridge.py:125` | `def assess_opsec(command, rhost)` |
| `intent_tool_class` | function | `modules/loop_ai_bridge.py:169` | `def intent_tool_class(summary)` |
| `moe_record_outcome` | function | `modules/loop_ai_bridge.py:321` | `def moe_record_outcome(expert_id, task_type, reward, detection_prob)` |
| `moe_route` | function | `modules/loop_ai_bridge.py:304` | `def moe_route(task_type, goal)` |
| `publish_loop_event` | function | `modules/loop_ai_bridge.py:74` | `def publish_loop_event(task_id, worker, kind, text, severity)` |
| `record_outcome_quality` | function | `modules/loop_ai_bridge.py:213` | `def record_outcome_quality(worker, intent_summary, facts, findings)` |
| `record_step` | function | `modules/loop_ai_bridge.py:407` | `def record_step(task_id, worker, command, output, detection_prob)` |
| `rl_save` | function | `modules/loop_ai_bridge.py:385` | `def rl_save()` |
| `rl_select` | function | `modules/loop_ai_bridge.py:340` | `def rl_select(task_type, phase, candidates, deterministic)` |
| `rl_update` | function | `modules/loop_ai_bridge.py:362` | `def rl_update(task_type, phase, action, reward, candidates, detection_prob)` |
| `stream_enabled` | function | `modules/loop_ai_bridge.py:475` | `def stream_enabled()` |
| `swan_available` | function | `modules/loop_ai_bridge.py:435` | `def swan_available()` |
| `swan_consult` | function | `modules/loop_ai_bridge.py:448` | `def swan_consult(prompt, task_type, phase, timeout)` |
| `tool_class_yields` | function | `modules/loop_ai_bridge.py:240` | `def tool_class_yields(summaries, phase)` |
| `LoopAudit` | class | `modules/loop_audit.py:114` | `class LoopAudit` |
| `__init__` | method | `modules/loop_audit.py:123` | `def __init__(self, task_id, path)` |
| `_activity_event` | function | `modules/loop_audit.py:433` | `def _activity_event(row, start_ts)` |
| `_append` | method | `modules/loop_audit.py:273` | `def _append(self, event)` |
| `_clean` | function | `modules/loop_audit.py:56` | `def _clean(text, limit)` |
| `_consume_context` | function | `modules/loop_audit.py:103` | `def _consume_context()` |
| `_first_token` | function | `modules/loop_audit.py:61` | `def _first_token(command)` |
| `_fmt_offset` | function | `modules/loop_audit.py:471` | `def _fmt_offset(offset)` |
| `_guard_event` | function | `modules/loop_audit.py:421` | `def _guard_event(row, start_ts)` |
| `_output_tail` | function | `modules/loop_audit.py:71` | `def _output_tail(output)` |
| `_read` | method | `modules/loop_audit.py:303` | `def _read(path)` |
| `_read_jsonl` | function | `modules/loop_audit.py:355` | `def _read_jsonl(path)` |
| `_render_event` | function | `modules/loop_audit.py:476` | `def _render_event(event)` |
| `_timeline_event` | function | `modules/loop_audit.py:410` | `def _timeline_event(audit_row, start_ts)` |
| `_trim` | method | `modules/loop_audit.py:288` | `def _trim(self)` |
| `_ts` | function | `modules/loop_audit.py:402` | `def _ts(row)` |
| `activity_rows` | function | `modules/loop_audit.py:397` | `def activity_rows(task_id)` |
| `audit_for` | function | `modules/loop_audit.py:338` | `def audit_for(task_id)` |
| `audit_path` | function | `modules/loop_audit.py:109` | `def audit_path(task_id)` |
| `blocked` | method | `modules/loop_audit.py:178` | `def blocked(self, source, reason, command, worker, intent)` |
| `blocked_verbs` | function | `modules/loop_audit.py:360` | `def blocked_verbs(task_id, min_count)` |
| `guard_rows` | function | `modules/loop_audit.py:392` | `def guard_rows(task_id)` |
| `list_runs` | function | `modules/loop_audit.py:558` | `def list_runs(limit)` |
| `path` | method | `modules/loop_audit.py:131` | `def path(self)` |
| `preflight` | method | `modules/loop_audit.py:168` | `def preflight(self, outcome)` |
| `record` | method | `modules/loop_audit.py:135` | `def record(self, kind)` |
| `record_command` | method | `modules/loop_audit.py:216` | `def record_command(self, command, output, duration, ok, task_id)` |
| `render` | function | `modules/loop_audit.py:537` | `def render(task_id, limit, audit)` |
| `render_summary` | function | `modules/loop_audit.py:595` | `def render_summary(summaries)` |
| `run_end` | method | `modules/loop_audit.py:203` | `def run_end(self, status, rounds, verdict, error)` |
| `run_start` | method | `modules/loop_audit.py:155` | `def run_start(self, goal, target, rounds, workers, mode, profile)` |
| `start` | function | `modules/loop_audit.py:320` | `def start(task_id)` |
| `step_context` | function | `modules/loop_audit.py:80` | `def step_context(task_id)` |
| `stop` | function | `modules/loop_audit.py:349` | `def stop(task_id)` |
| `timeline` | function | `modules/loop_audit.py:447` | `def timeline(task_id, audit)` |
| `verdict` | method | `modules/loop_audit.py:189` | `def verdict(self, verdict)` |
| `EdrPacer` | class | `modules/loop_guardrails.py:242` | `class EdrPacer` |
| `Fact` | class | `modules/loop_guardrails.py:86` | `class Fact` |
| `FactVectorStore` | class | `modules/loop_guardrails.py:589` | `class FactVectorStore` |
| `ListingNoiseDetector` | class | `modules/loop_guardrails.py:787` | `class ListingNoiseDetector` |
| `RepeatDetector` | class | `modules/loop_guardrails.py:95` | `class RepeatDetector` |
| `TargetLimiter` | class | `modules/loop_guardrails.py:519` | `class TargetLimiter` |
| `__init__` | method | `modules/loop_guardrails.py:117` | `def __init__(self, window)` |
| `__init__` | method | `modules/loop_guardrails.py:258` | `def __init__(self, duration_threshold)` |
| `__init__` | method | `modules/loop_guardrails.py:527` | `def __init__(self, max_concurrent)` |
| `__init__` | method | `modules/loop_guardrails.py:597` | `def __init__(self, path, max_facts)` |
| `__len__` | method | `modules/loop_guardrails.py:609` | `def __len__(self)` |
| `_alternating` | method | `modules/loop_guardrails.py:214` | `def _alternating(self)` |
| `_load` | method | `modules/loop_guardrails.py:726` | `def _load(self)` |
| `_periodic_cycle` | method | `modules/loop_guardrails.py:161` | `def _periodic_cycle(entries)` |
| `_strict_alternating` | method | `modules/loop_guardrails.py:156` | `def _strict_alternating(entries)` |
| `_tokenize` | method | `modules/loop_guardrails.py:613` | `def _tokenize(text)` |
| `_update_oscillation` | method | `modules/loop_guardrails.py:142` | `def _update_oscillation(self)` |
| `_vectorize` | method | `modules/loop_guardrails.py:618` | `def _vectorize(tokens)` |
| `_window_seconds_until_end` | method | `modules/loop_guardrails.py:401` | `def _window_seconds_until_end(windows, now)` |
| `active_targets` | method | `modules/loop_guardrails.py:539` | `def active_targets(self)` |
| `add` | method | `modules/loop_guardrails.py:626` | `def add(self, text, meta)` |
| `clear` | method | `modules/loop_guardrails.py:699` | `def clear(self)` |
| `cycle` | method | `modules/loop_guardrails.py:226` | `def cycle(self)` |
| `decay` | method | `modules/loop_guardrails.py:379` | `def decay(self, factor)` |
| `describe` | method | `modules/loop_guardrails.py:200` | `def describe(self)` |
| `describe` | method | `modules/loop_guardrails.py:504` | `def describe(self)` |
| `from_config` | method | `modules/loop_guardrails.py:326` | `def from_config(cls)` |
| `in_sleeper_window` | method | `modules/loop_guardrails.py:426` | `def in_sleeper_window(self, now)` |
| `inter_step_delay` | method | `modules/loop_guardrails.py:472` | `def inter_step_delay(self)` |
| `last_commands` | method | `modules/loop_guardrails.py:230` | `def last_commands(self)` |
| `level` | method | `modules/loop_guardrails.py:385` | `def level(self)` |
| `listing_forbidden` | function | `modules/loop_guardrails.py:759` | `def listing_forbidden(command)` |
| `max_concurrent` | method | `modules/loop_guardrails.py:534` | `def max_concurrent(self)` |
| `observe` | method | `modules/loop_guardrails.py:357` | `def observe(self, command, duration_sec, output)` |
| `observe` | method | `modules/loop_guardrails.py:798` | `def observe(self, command, output)` |
| `oscillation_pair` | method | `modules/loop_guardrails.py:222` | `def oscillation_pair(self)` |
| `parse_windows` | method | `modules/loop_guardrails.py:304` | `def parse_windows(raw)` |
| `path` | method | `modules/loop_guardrails.py:605` | `def path(self)` |
| `quieten` | method | `modules/loop_guardrails.py:489` | `def quieten(self, command)` |
| `record` | method | `modules/loop_guardrails.py:125` | `def record(self, command)` |
| `reset` | method | `modules/loop_guardrails.py:234` | `def reset(self)` |
| `save` | method | `modules/loop_guardrails.py:705` | `def save(self)` |
| `search` | method | `modules/loop_guardrails.py:660` | `def search(self, query, k)` |
| `search_block` | method | `modules/loop_guardrails.py:690` | `def search_block(self, query, k, max_chars)` |
| `signal` | method | `modules/loop_guardrails.py:395` | `def signal(self)` |
| `sleeper_delay` | method | `modules/loop_guardrails.py:459` | `def sleeper_delay(self, now)` |
| `slot` | method | `modules/loop_guardrails.py:545` | `def slot(self, target)` |
| `stuck` | method | `modules/loop_guardrails.py:182` | `def stuck(self)` |
| `windows_delay` | method | `modules/loop_guardrails.py:432` | `def windows_delay(windows, now)` |
| `LoopManager` | class | `modules/loop_manager.py:355` | `class LoopManager` |
| `LoopNotFoundError` | class | `modules/loop_manager.py:97` | `class LoopNotFoundError(KeyError)` |
| `LoopSpec` | class | `modules/loop_manager.py:287` | `class LoopSpec` |
| `LoopValidationError` | class | `modules/loop_manager.py:88` | `class LoopValidationError(ValueError)` |
| `__init__` | method | `modules/loop_manager.py:91` | `def __init__(self, field, message)` |
| `__init__` | method | `modules/loop_manager.py:366` | `def __init__(self, loops_dir, python_executable, max_concurrent, repo_root, lazyown_script)` |
| `_load_registry_locked` | method | `modules/loop_manager.py:865` | `def _load_registry_locked(self)` |
| `_loop_command` | function | `modules/loop_manager.py:308` | `def _loop_command(spec)` |
| `_now_iso` | function | `modules/loop_manager.py:240` | `def _now_iso()` |
| `_pid_alive` | function | `modules/loop_manager.py:269` | `def _pid_alive(pid, start_ticks)` |
| `_process_start_ticks` | function | `modules/loop_manager.py:245` | `def _process_start_ticks(pid)` |
| `_prune_locked` | method | `modules/loop_manager.py:816` | `def _prune_locked(self)` |
| `_read_outcome` | method | `modules/loop_manager.py:577` | `def _read_outcome(workspace)` |
| `_reap` | method | `modules/loop_manager.py:518` | `def _reap(self, loop_id, process)` |
| `_refresh_log_bytes` | method | `modules/loop_manager.py:618` | `def _refresh_log_bytes(self, record)` |
| `_remove_workspace` | method | `modules/loop_manager.py:841` | `def _remove_workspace(self, loop_id)` |
| `_resolve_log_path` | method | `modules/loop_manager.py:689` | `def _resolve_log_path(self, record)` |
| `_save_registry_locked` | method | `modules/loop_manager.py:880` | `def _save_registry_locked(self, records)` |
| `_spawn_locked` | method | `modules/loop_manager.py:437` | `def _spawn_locked(self, spec, operator)` |
| `_update_status_locked` | method | `modules/loop_manager.py:763` | `def _update_status_locked(self, loop_id, status)` |
| `_write_workspace_metadata` | method | `modules/loop_manager.py:560` | `def _write_workspace_metadata(record)` |
| `clamp_float` | function | `modules/loop_manager.py:198` | `def clamp_float(raw, field, default, minimum, maximum)` |
| `clamp_int` | function | `modules/loop_manager.py:173` | `def clamp_int(raw, field, default, minimum, maximum)` |
| `default_manager` | function | `modules/loop_manager.py:898` | `def default_manager()` |
| `get_loop` | method | `modules/loop_manager.py:629` | `def get_loop(self, loop_id)` |
| `list_loops` | method | `modules/loop_manager.py:594` | `def list_loops(self)` |
| `loops_dir` | method | `modules/loop_manager.py:388` | `def loops_dir(self)` |
| `read_log` | method | `modules/loop_manager.py:648` | `def read_log(self, loop_id, offset)` |
| `sanitize_goal` | function | `modules/loop_manager.py:146` | `def sanitize_goal(raw)` |
| `start` | method | `modules/loop_manager.py:392` | `def start(self, spec, operator)` |
| `stop` | method | `modules/loop_manager.py:715` | `def stop(self, loop_id)` |
| `summary` | method | `modules/loop_manager.py:780` | `def summary(self)` |
| `validate_beacon_target` | function | `modules/loop_manager.py:124` | `def validate_beacon_target(raw)` |
| `validate_loop_id` | function | `modules/loop_manager.py:223` | `def validate_loop_id(loop_id)` |
| `validate_target` | function | `modules/loop_manager.py:101` | `def validate_target(raw)` |
| `_probe` | function | `modules/loop_preflight.py:107` | `def _probe(port)` |
| `check_target` | function | `modules/loop_preflight.py:145` | `def check_target(target, ports, connect_timeout, lab)` |
| `lab_state_for` | function | `modules/loop_preflight.py:38` | `def lab_state_for(target, scenarios, running, existing, ip_lookup)` |
| `probe_tcp` | function | `modules/loop_preflight.py:125` | `def probe_tcp(target, ports, timeout)` |
| `probe_tcp_detailed` | function | `modules/loop_preflight.py:83` | `def probe_tcp_detailed(target, ports, timeout)` |
| `recovery_hint` | function | `modules/loop_preflight.py:211` | `def recovery_hint(outcome)` |
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
| `EngineMediator` | class | `modules/mediation/engine_mediator.py:66` | `class EngineMediator` |
| `ExploitRetryPort` | class | `modules/mediation/engine_mediator.py:32` | `class ExploitRetryPort(Protocol)` |
| `ReactionPort` | class | `modules/mediation/engine_mediator.py:49` | `class ReactionPort(Protocol)` |
| `analyse` | method | `modules/mediation/engine_mediator.py:52` | `def analyse(self, output, command, platform)` |
| `analyse` | method | `modules/mediation/engine_mediator.py:100` | `def analyse(self, output, command, platform)` |
| `describe` | method | `modules/mediation/engine_mediator.py:71` | `def describe(self)` |
| `retry_with_credentials` | method | `modules/mediation/engine_mediator.py:35` | `def retry_with_credentials(self, target, credentials)` |

Next: [SYMBOLS_p21.md](SYMBOLS_p21.md)
