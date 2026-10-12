# Subsystem: modules (page 9 of 14)
Previous: [KB_modules_p8.md](KB_modules_p8.md)

## modules/lazyownclient.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 34) `def signal_handler(sig, frame)`
  - `pad` (function, line 51) `def pad(s)`
  - `encrypt` (function, line 55) `def encrypt(plaintext, key)`
  - `decrypt` (function, line 62) `def decrypt(ciphertext, key)`
  - `handle_command` (function, line 69) `def handle_command(cmd, key)`
  - `main` (function, line 198) `def main()`

## modules/lazyownerweb.py
- Layer: utility
- Language: py
- Symbols:
  - `send_request` (function, line 36) `def send_request(url, params, method)`
  - `test_injection` (function, line 49) `def test_injection(url, payloads, param_name, detection_strings, method)`
  - `main` (function, line 59) `def main()`
- Depends on: `core/logging.py`, `modules/logging_config.py`

## modules/lazyownserver.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 34) `def signal_handler(sig, frame)`
  - `pad` (function, line 42) `def pad(s)`
  - `encrypt` (function, line 46) `def encrypt(plaintext, key)`
  - `decrypt` (function, line 53) `def decrypt(ciphertext, key)`
  - `handle_client` (function, line 60) `def handle_client(conn, addr, key)`
  - `main` (function, line 97) `def main()`

## modules/lazypsexec.sh
- Doc: execute_psexec: Función para ejecutar psexec y verificar la salida
- Layer: utility
- Language: sh
- Symbols:
  - `execute_psexec` (function, line 15)

## modules/lazyreverse_shell.sh
- Doc: Nombre del script: lazyreverse_shell.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh
- Symbols:
  - `mostrar_ayuda` (function, line 21)
  - `validar_ip` (function, line 31)

## modules/lazyrtpflood.sh
- Layer: utility
- Language: sh

## modules/lazyvpnshield.sh
- Doc: Author: Nisrin Ahmed aka Wh1teDrvg0n Modify: grisun0
- Layer: utility
- Language: sh
- Symbols:
  - `save_current_rules` (function, line 29)
  - `show_current_rules` (function, line 37)
  - `apply_vpn_rules` (function, line 45)
  - `undo_and_restore_rules` (function, line 86)
  - `main` (function, line 113)
  - `ctrl_c` (function, line 11)
  - `check_sudo` (function, line 16)

## modules/lazywps.sh
- Layer: utility
- Language: sh
- Symbols:
  - `ctrl_c` (function, line 9)

## modules/lesson_ingestor.py
- Doc: Lesson ingestion bridge between EpisodeReflectionEngine and MoERouter.
- Layer: utility
- Language: py
- Symbols:
  - `LessonLearned` (class, line 55) `class LessonLearned`
  - `LessonIngestor` (class, line 77) `class LessonIngestor`
  - `ingest_campaign_lessons` (function, line 222) `def ingest_campaign_lessons(lessons_file)`
  - `from_dict` (method, line 66) `def from_dict(cls, d)`
  - `__init__` (method, line 86) `def __init__(self, lessons_file, router, trainer, boost_reward)`
  - `_get_router` (method, line 98) `def _get_router(self)`
  - `_get_trainer` (method, line 110) `def _get_trainer(self)`
  - `_expert_for_topic` (method, line 122) `def _expert_for_topic(self, topic)`
  - `ingest` (method, line 125) `def ingest(self, lesson)`
  - `ingest_all` (method, line 185) `def ingest_all(self, lessons)`
  - `_load_from_file` (method, line 202) `def _load_from_file(self)`
- Depends on: `core/logging.py`, `modules/moe_router.py`, `modules/rl_trainer.py`
- Imported by: `skills/lazyown_campaign.py`, `tests/test_lesson_ingestor.py`

## modules/lilsplunky.py
- Doc: Author: Your Name Email: youremail@example.com Creation Date: 14/04/2025 License: GPL v3...
- Layer: utility
- Language: py
- Symbols:
  - `simple_parse_log_line` (function, line 69) `def simple_parse_log_line(line, file_path)`
  - `store_event` (function, line 108) `def store_event(event_data)`
  - `analyze_with_deepseek` (function, line 123) `def analyze_with_deepseek(log_entry_data)`
  - `LogFileHandler` (class, line 217) `class LogFileHandler(FileSystemEventHandler)`
  - `display_record` (function, line 346) `def display_record(record)`
  - `search_logs` (function, line 382) `def search_logs(query, file_path)`
  - `start_monitoring` (function, line 413) `def start_monitoring(log_dir, mode)`
  - `parse_args` (function, line 446) `def parse_args()`
  - `__init__` (method, line 223) `def __init__(self, log_dir, mode)`
  - `initialize_file_positions` (method, line 229) `def initialize_file_positions(self)`
  - `is_monitored` (method, line 245) `def is_monitored(self, file_path)`
  - `process_file` (method, line 257) `def process_file(self, file_path)`
  - `on_modified` (method, line 331) `def on_modified(self, event)`
  - `on_created` (method, line 336) `def on_created(self, event)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/linux_advanced_payloads.py
- Doc: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- Layer: utility
- Language: py
- Symbols:
  - `LinuxAdvancedConfig` (class, line 64) `class LinuxAdvancedConfig`
  - `LinuxAdvancedPayloadFactory` (class, line 92) `class LinuxAdvancedPayloadFactory`
  - `__init__` (method, line 105) `def __init__(self, config, output_dir)`
  - `generate_ld_preload_rootkit` (method, line 110) `def generate_ld_preload_rootkit(self)`
  - `generate_ebpf_payload` (method, line 235) `def generate_ebpf_payload(self)`
  - `_ip_to_hex` (method, line 305) `def _ip_to_hex(ip_str)`
  - `generate_pam_backdoor` (method, line 311) `def generate_pam_backdoor(self)`
  - `generate_systemd_persistence` (method, line 398) `def generate_systemd_persistence(self)`
  - `generate_ssh_persistence` (method, line 458) `def generate_ssh_persistence(self)`
  - `generate_kernel_module` (method, line 519) `def generate_kernel_module(self)`
  - `generate_process_masquerade` (method, line 632) `def generate_process_masquerade(self)`
  - `generate_udev_persistence` (method, line 676) `def generate_udev_persistence(self)`
  - `generate_motd_backdoor` (method, line 689) `def generate_motd_backdoor(self)`
  - `compile_c_source` (method, line 707) `def compile_c_source(self, source, output_name, shared)`
  - `generate_all` (method, line 749) `def generate_all(self)`
  - `list_hook_functions` (method, line 793) `def list_hook_functions()`
  - `list_persistence_methods` (method, line 797) `def list_persistence_methods()`
- Imported by: `cli/commands/payload_arsenal.py`

## modules/listener_manager.py
- Doc: Multi-listener manager for LazyOwn C2.
- Layer: utility
- Language: py
- Symbols:
  - `_collect_listener_bind_candidates` (function, line 35) `def _collect_listener_bind_candidates(payload)`
  - `_probe_listener_bind` (function, line 72) `def _probe_listener_bind(address, port)`
  - `_resolve_listener_bind_address` (function, line 110) `def _resolve_listener_bind_address(payload, port)`
  - `Listener` (class, line 141) `class Listener`
  - `ListenerManager` (class, line 172) `class ListenerManager`
  - `to_dict` (method, line 152) `def to_dict(self)`
  - `from_dict` (method, line 162) `def from_dict(cls, data)`
  - `__init__` (method, line 179) `def __init__(self, app, sessions_dir, payload)`
  - `set_payload` (method, line 187) `def set_payload(self, payload)`
  - `_bind_address` (method, line 191) `def _bind_address(self, port)`
  - `_listeners_path` (method, line 201) `def _listeners_path(self)`
  - `_load` (method, line 204) `def _load(self)`
  - `_save` (method, line 217) `def _save(self)`
  - `add` (method, line 229) `def add(self, port, ssl, listener_id)`
  - `remove` (method, line 242) `def remove(self, listener_id)`
  - `start` (method, line 255) `def start(self, listener_id)`
  - `stop` (method, line 323) `def stop(self, listener_id)`
  - `_stop` (method, line 331) `def _stop(self, listener)`
  - `start_all` (method, line 344) `def start_all(self)`
  - `stop_all` (method, line 350) `def stop_all(self)`
  - `status` (method, line 355) `def status(self)`
  - `get_default_port` (method, line 367) `def get_default_port(self, fallback)`
- Depends on: `utils.py`
- Imported by: `cli/commands/command_and_control_migrated.py`, `lazyc2.py`

## modules/live_surface.py
- Doc: Live attack-surface graph derived from the world model.
- Layer: utility
- Language: py
- Symbols:
  - `_is_compromised` (function, line 45) `def _is_compromised(state)`
  - `_node_value` (function, line 50) `def _node_value(centrality)`
  - `_group_for` (function, line 55) `def _group_for(node_id)`
  - `_label_for` (function, line 64) `def _label_for(node_id)`
  - `build_live_graph` (function, line 72) `def build_live_graph(world)`
  - `_emit_node` (function, line 106) `def _emit_node(node_id, state, title)`
  - `_emit_edge` (function, line 126) `def _emit_edge(source, target, relation, weight)`
- Depends on: `modules/world_model.py`
- Imported by: `lazyc2.py`, `modules/unified_dashboard.py`, `tests/test_live_surface.py`

## modules/llm_adapter.py
- Doc: LLM adapter facade — single import point for all LLM backends used by lazyc2.
- Layer: infrastructure
- Language: py
- Symbols:
  - `safe_groq_client` (function, line 48) `def safe_groq_client(api_key)`
  - `_configure_logging` (function, line 65) `def _configure_logging(debug)`
  - `_read_prompt_file` (function, line 70) `def _read_prompt_file(prompt)`
  - `_read_error` (function, line 78) `def _read_error(prompt)`
  - `_complete` (function, line 82) `def _complete(client, full_prompt, model)`
  - `_process` (function, line 96) `def _process(client, prompt, debug, template, config)`
  - `process_prompt` (function, line 119) `def process_prompt(client, prompt, debug)`
  - `process_prompt_script` (function, line 133) `def process_prompt_script(client, prompt, debug)`
  - `process_prompt_adversary` (function, line 147) `def process_prompt_adversary(client, prompt, debug)`
  - `process_prompt_general` (function, line 161) `def process_prompt_general(client, prompt, debug)`
  - `process_prompt_search` (function, line 175) `def process_prompt_search(client, prompt, debug)`
  - `process_prompt_task` (function, line 189) `def process_prompt_task(client, prompt, debug)`
  - `process_prompt_vuln` (function, line 206) `def process_prompt_vuln(client, prompt, debug, event)`
  - `process_prompt_redop` (function, line 237) `def process_prompt_redop(client, prompt, debug)`
  - `ask_general` (function, line 254) `def ask_general(prompt, debug)`
- Depends on: `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazyphishingai.py`, `core/logging.py`, `modules/llm_factory.py`, `modules/llm_prompts.py`
- Imported by: `cli/commands/ai.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_llm_adapter_parity.py`

## modules/llm_client.py
- Doc: LazyOwn Unified LLM Client
- Layer: infrastructure
- Language: py
- Symbols:
  - `LLMClient` (class, line 45) `class LLMClient`
  - `get_client` (function, line 243) `def get_client(api_key)`
  - `ask` (function, line 251) `def ask(prompt)`
  - `classify` (function, line 263) `def classify(output)`
  - `summarize` (function, line 268) `def summarize(text)`
  - `__init__` (method, line 63) `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)`
  - `ask` (method, line 79) `def ask(self, prompt)`
  - `classify` (method, line 125) `def classify(self, output)`
  - `summarize` (method, line 154) `def summarize(self, text)`
  - `_ask_groq` (method, line 174) `def _ask_groq(self, prompt, model, system, temperature)`
  - `_ask_ollama` (method, line 215) `def _ask_ollama(self, prompt, model)`
- Depends on: `core/logging.py`
- Imported by: `contrib/legacy/lazyaddon_creator.py`, `modules/llm_factory.py`, `modules/planner.py`, `modules/playbook_engine.py`, `skills/lazyown_mcp.py`

## modules/llm_evaluator.py
- Doc: — Records LLM decisions and their outcomes, computes quality metrics, and exports fine-tuning...
- Layer: utility
- Language: py
- Symbols:
  - `DecisionRecord` (class, line 21) `class DecisionRecord`
  - `_new_id` (function, line 35) `def _new_id()`
  - `_record_from_dict` (function, line 39) `def _record_from_dict(d)`
  - `OutcomeRecorder` (class, line 55) `class OutcomeRecorder(ABC)`
  - `JSONLRecorder` (class, line 75) `class JSONLRecorder(OutcomeRecorder)`
  - `QualityMetrics` (class, line 140) `class QualityMetrics`
  - `_safe_mean` (function, line 150) `def _safe_mean(values)`
  - `_tactic_success_rates` (function, line 154) `def _tactic_success_rates(records)`
  - `LLMEvaluator` (class, line 161) `class LLMEvaluator`
  - `get_evaluator` (function, line 293) `def get_evaluator()`
  - `record_decision` (function, line 302) `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)`
  - `record_outcome` (function, line 313) `def record_outcome(decision_id, actual_outcome, findings_count, success)`
  - `_cli` (function, line 322) `def _cli()`
  - `record` (method, line 57) `def record(self, decision)`
  - `update_outcome` (method, line 60) `def update_outcome(self, decision_id, actual, findings_count, success)`
  - `load_all` (method, line 69) `def load_all(self)`
  - `load_by_session` (method, line 72) `def load_by_session(self, session_id)`
  - `__init__` (method, line 76) `def __init__(self, path)`
  - `record` (method, line 81) `def record(self, decision)`
  - `update_outcome` (method, line 86) `def update_outcome(self, decision_id, actual, findings_count, success)`
  - `load_all` (method, line 120) `def load_all(self)`
  - `load_by_session` (method, line 135) `def load_by_session(self, session_id)`
  - `__init__` (method, line 162) `def __init__(self, recorder)`
  - `record_decision` (method, line 165) `def record_decision(self, session_id, thought, action, mitre_tactic, expected_outcome, confidence)`
  - `record_outcome` (method, line 191) `def record_outcome(self, decision_id, actual_outcome, findings_count, success)`
  - `compute_metrics` (method, line 200) `def compute_metrics(self, session_id)`
  - `quality_report` (method, line 241) `def quality_report(self, session_id)`
  - `export_finetuning_dataset` (method, line 256) `def export_finetuning_dataset(self, path)`
- Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`

## modules/llm_factory.py
- Doc: LLM backend factory and selection utilities.
- Layer: infrastructure
- Language: py
- Symbols:
  - `is_model_missing_error` (function, line 112) `def is_model_missing_error(message)`
  - `groq_model_chain` (function, line 132) `def groq_model_chain(config)`
  - `LLMBackendUnavailableError` (class, line 175) `class LLMBackendUnavailableError(RuntimeError)`
  - `LLMBackendNotSupportedError` (class, line 179) `class LLMBackendNotSupportedError(ValueError)`
  - `default_model_for` (function, line 207) `def default_model_for(backend)`
  - `model_config_key` (function, line 228) `def model_config_key(backend)`
  - `api_key_config_key` (function, line 249) `def api_key_config_key(backend)`
  - `backend_requires_api_key` (function, line 272) `def backend_requires_api_key(backend)`
  - `load_payload` (function, line 290) `def load_payload(payload_path)`
  - `_resolve_api_key` (function, line 314) `def _resolve_api_key(config)`
  - `_resolve_api_key_for_backend` (function, line 337) `def _resolve_api_key_for_backend(backend, config)`
  - `_normalize_backend` (function, line 368) `def _normalize_backend(backend)`
  - `_build_groq` (function, line 391) `def _build_groq(config)`
  - `_build_ollama` (function, line 413) `def _build_ollama(config)`
  - `_build_openai` (function, line 427) `def _build_openai(config)`
  - `_build_anthropic` (function, line 449) `def _build_anthropic(config)`
  - `_build_deepseek` (function, line 471) `def _build_deepseek(config)`
  - `_resolve_model_identifier` (function, line 493) `def _resolve_model_identifier(backend_identifier, config)`
  - `_wrap_with_budget` (function, line 520) `def _wrap_with_budget(backend, config, backend_identifier)`
  - `get_llm_backend` (function, line 558) `def get_llm_backend(config, backend)`
  - `_build_backend` (function, line 610) `def _build_backend(normalized, resolved_config)`
  - `get_llm_backend_raw` (function, line 644) `def get_llm_backend_raw(config, backend)`
  - `try_get_llm_backend` (function, line 666) `def try_get_llm_backend(config, backend)`
  - `stream_complete` (function, line 690) `def stream_complete(model, prompt, max_tokens, on_delta)`
  - `complete` (function, line 759) `def complete(model, prompt, max_tokens)`
- Depends on: `core/llm_budget.py`, `modules/ai_model.py`, `modules/llm_client.py`, `modules/toposwarm_bridge.py`
- Imported by: `cli/commands/ai.py`, `cli/wizard.py`, `contrib/legacy/lazyllmchat.py`, `core/payload_schema.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ai_fallback.py`, `modules/ai_model.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/llm_adapter.py`, `modules/mcp_agent_bridge.py`, `modules/privesc_predictor.py`, `modules/professional_report.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `tests/conftest.py`, `tests/test_ai_commands_llm.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_streaming.py`, `tests/test_llm_adapter_parity.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_llm_resilience.py`, `tests/test_payload_schema.py`, `tests/test_wizard_llm.py`

## modules/llm_pool.py
- Doc: Ordered LLM failover pool with health-aware skipping.
- Layer: utility
- Language: py
- Symbols:
  - `_health_path` (function, line 20) `def _health_path()`
  - `PoolConfig` (class, line 29) `class PoolConfig`
  - `PoolExhausted` (class, line 42) `class PoolExhausted(RuntimeError)`
  - `shared_registry` (function, line 50) `def shared_registry(config)`
  - `PoolMember` (class, line 64) `class PoolMember`
  - `HealthRegistry` (class, line 75) `class HealthRegistry`
  - `LLMPool` (class, line 176) `class LLMPool`
  - `__init__` (method, line 83) `def __init__(self, config)`
  - `_load` (method, line 92) `def _load(self)`
  - `_persist_locked` (method, line 116) `def _persist_locked(self)`
  - `report_success` (method, line 135) `def report_success(self, member_id)`
  - `report_failure` (method, line 143) `def report_failure(self, member_id, error)`
  - `_backoff_for` (method, line 155) `def _backoff_for(self, failures)`
  - `healthy` (method, line 163) `def healthy(self, member_id)`
  - `__init__` (method, line 179) `def __init__(self, members, health, config)`
  - `members` (method, line 192) `def members(self)`
  - `session_key` (method, line 196) `def session_key(self, conversation_id, role, index)`
  - `_ordered` (method, line 201) `def _ordered(self)`
  - `_truncate` (method, line 217) `def _truncate(self, text, overflow_dir)`
  - `complete` (method, line 237) `def complete(self, prompt, max_tokens, session_key, overflow_dir)`
- Imported by: `cli/commands/ai.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_autonomous_ops.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_runner.py`

## modules/llm_prompts.py
- Doc: Canonical prompt-template and knowledge-base contract for LLM consumers.
- Layer: utility
- Language: py
- Symbols:
  - `default_project_root` (function, line 67) `def default_project_root()`
  - `resolve_model` (function, line 76) `def resolve_model(model)`
  - `truncate_message` (function, line 95) `def truncate_message(message, max_chars)`
  - `LlmPromptConfig` (class, line 111) `class LlmPromptConfig`
  - `render_kb_tail` (function, line 271) `def render_kb_tail(lines)`
  - `KnowledgeStore` (class, line 286) `class KnowledgeStore`
  - `_payload_block` (function, line 354) `def _payload_block(config)`
  - `_prompt_oneliner` (function, line 362) `def _prompt_oneliner(base_prompt, kb_text, config)`
  - `_prompt_script` (function, line 378) `def _prompt_script(base_prompt, kb_text, config)`
  - `_prompt_adversary` (function, line 393) `def _prompt_adversary(base_prompt, kb_text, config)`
  - `_prompt_general` (function, line 409) `def _prompt_general(base_prompt, kb_text, config)`
  - `_prompt_search` (function, line 422) `def _prompt_search(base_prompt, kb_text, config)`
  - `_prompt_vuln` (function, line 436) `def _prompt_vuln(base_prompt, kb_text, config)`
  - `_prompt_task` (function, line 450) `def _prompt_task(base_prompt, kb_text, config)`
  - `_prompt_redop` (function, line 462) `def _prompt_redop(base_prompt, kb_text, config)`
  - `from_defaults` (method, line 130) `def from_defaults(cls, project_root)`
  - `knowledge_base_path` (method, line 150) `def knowledge_base_path(self, domain)`
  - `load_payload_context` (method, line 161) `def load_payload_context(self)`
  - `load_event_tool_output` (method, line 176) `def load_event_tool_output(self, event_name)`
  - `load_plan_history` (method, line 203) `def load_plan_history(self)`
  - `load_report_context` (method, line 218) `def load_report_context(self)`
  - `knowledge_store` (method, line 238) `def knowledge_store(self, domain)`
  - `render` (method, line 249) `def render(self, template, base_prompt)`
  - `__init__` (method, line 289) `def __init__(self, path)`
  - `load` (method, line 297) `def load(self)`
  - `save` (method, line 312) `def save(self, records)`
  - `add` (method, line 324) `def add(self, prompt, response)`
  - `relevant` (method, line 335) `def relevant(self, prompt, limit)`
- Depends on: `modules/colors.py`
- Imported by: `cli/commands/ai.py`, `modules/llm_adapter.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_prompts.py`

## modules/log_tamper.py
- Doc: Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log.
- Layer: utility
- Language: py
- Symbols:
  - `LogTamperConfig` (class, line 71) `class LogTamperConfig`
  - `LogTamper` (class, line 95) `class LogTamper`
  - `__init__` (method, line 105) `def __init__(self, config)`
  - `windows_clear_commands` (method, line 108) `def windows_clear_commands(self)`
  - `linux_clear_commands` (method, line 176) `def linux_clear_commands(self)`
  - `macos_clear_commands` (method, line 243) `def macos_clear_commands(self)`
  - `generate_all` (method, line 295) `def generate_all(self)`
  - `auditd_disable_commands` (method, line 307) `def auditd_disable_commands(self)`
  - `sysmon_disable_commands` (method, line 341) `def sysmon_disable_commands(self)`
- Imported by: `cli/commands/opsec_cleanup.py`

## modules/logging_config.py
- Doc: Centralized logging configuration for the LazyOwn framework.
- Layer: infrastructure
- Language: py
- Symbols:
  - `ColoredFormatter` (class, line 36) `class ColoredFormatter(Formatter)`
  - `JsonFormatter` (class, line 53) `class JsonFormatter(Formatter)`
  - `CorrelationFilter` (class, line 91) `class CorrelationFilter(Filter)`
  - `ResilientRotatingFileHandler` (class, line 103) `class ResilientRotatingFileHandler(RotatingFileHandler)`
  - `set_correlation_id` (function, line 134) `def set_correlation_id(cid)`
  - `get_correlation_id` (function, line 139) `def get_correlation_id()`
  - `clear_correlation_id` (function, line 144) `def clear_correlation_id()`
  - `_ensure_log_dir_writable` (function, line 156) `def _ensure_log_dir_writable(log_dir)`
  - `_use_json_format` (function, line 235) `def _use_json_format()`
  - `configure` (function, line 244) `def configure(level, log_dir, console, file, format_console, format_file, max_bytes, backup_count, module_levels)`
  - `get_logger` (function, line 328) `def get_logger(name, level)`
  - `set_level` (function, line 357) `def set_level(name, level)`
  - `set_quiet` (function, line 367) `def set_quiet()`
  - `set_verbose` (function, line 373) `def set_verbose()`
  - `silence_module` (function, line 379) `def silence_module(name)`
  - `reset` (function, line 388) `def reset()`
  - `format` (method, line 39) `def format(self, record)`
  - `format` (method, line 72) `def format(self, record)`
  - `filter` (method, line 94) `def filter(self, record)`
  - `emit` (method, line 116) `def emit(self, record)`
  - `handleError` (method, line 122) `def handleError(self, record)`
- Depends on: `core/logging.py`
- Imported by: `lazy_sentinel4.py`, `lazyc2.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/icmp_server.py`, `modules/lazyownerweb.py`, `modules/lilsplunky.py`, `modules/vulnbot.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`

## modules/loop_ai_bridge.py
- Doc: Single edge between the autonomous loop and the LazyOwn AI stack.
- Layer: utility
- Language: py
- Symbols:
  - `_singleton` (function, line 50) `def _singleton(key, factory)`
  - `_stage` (function, line 64) `def _stage(name, default)`
  - `publish_loop_event` (function, line 74) `def publish_loop_event(task_id, worker, kind, text, severity)`
  - `_hive_store` (function, line 101) `def _hive_store(task_id, worker, kind, text)`
  - `annotate_detection` (function, line 125) `def annotate_detection(command, action_category)`
  - `moe_route` (function, line 149) `def moe_route(task_type, goal)`
  - `moe_record_outcome` (function, line 166) `def moe_record_outcome(expert_id, task_type, reward, detection_prob)`
  - `rl_select` (function, line 185) `def rl_select(task_type, phase, candidates, deterministic)`
  - `rl_update` (function, line 207) `def rl_update(task_type, phase, action, reward, candidates, detection_prob)`
  - `rl_save` (function, line 230) `def rl_save()`
  - `record_step` (function, line 249) `def record_step(task_id, worker, command, output, detection_prob)`
  - `swan_available` (function, line 264) `def swan_available()`
  - `swan_consult` (function, line 277) `def swan_consult(prompt, task_type, phase, timeout)`
  - `stream_enabled` (function, line 304) `def stream_enabled()`
  - `ai_snapshot` (function, line 314) `def ai_snapshot()`
  - `_open` (function, line 104) `def _open()`
  - `_open` (function, line 130) `def _open()`
  - `_open` (function, line 152) `def _open()`
  - `_open` (function, line 171) `def _open()`
  - `_open` (function, line 192) `def _open()`
  - `_open` (function, line 214) `def _open()`
  - `_open` (function, line 235) `def _open()`
  - `_open` (function, line 269) `def _open()`
- Depends on: `modules/detection_oracle.py`, `modules/event_bus.py`, `modules/moe_router.py`, `modules/orchestrator_config.py`, `modules/rl_trainer.py`, `skills/hive_mind.py`, `skills/swan_agent.py`
- Imported by: `modules/lazy_agent.py`, `modules/lazy_loop.py`, `tests/conftest.py`, `tests/test_lazy_streaming.py`, `tests/test_loop_ai_bridge.py`

## modules/loop_progress.py
- Doc: Rich Live milestone panel for the autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `LoopSnapshot` (class, line 80) `class LoopSnapshot`
  - `snapshot_from_overview` (function, line 99) `def snapshot_from_overview(overview, record, activity_tail, elapsed_sec)`
  - `snap_to_states` (function, line 123) `def snap_to_states(snapshot)`
  - `sanitize_line` (function, line 151) `def sanitize_line(line, keep_ansi)`
  - `LoopProgress` (class, line 169) `class LoopProgress`
  - `__post_init__` (method, line 182) `def __post_init__(self)`
  - `live_mode` (method, line 195) `def live_mode(self)`
  - `start` (method, line 202) `def start(self)`
  - `stop` (method, line 229) `def stop(self)`
  - `refresh` (method, line 246) `def refresh(self, snapshot)`
  - `emit` (method, line 268) `def emit(self, line)`
  - `_header` (method, line 282) `def _header(self)`
  - `_milestone_line` (method, line 289) `def _milestone_line(self, snapshot, states, current)`
  - `_footer` (method, line 306) `def _footer(self, snapshot, elapsed)`
  - `_render` (method, line 324) `def _render(self, snapshot)`
- Depends on: `core/safe_console.py`
- Imported by: `cli/lazy_monitor.py`, `modules/lazy_runner.py`, `tests/test_lazy_runner.py`, `tests/test_loop_progress.py`

## modules/macos_payloads.py
- Doc: macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.
- Layer: utility
- Language: py
- Symbols:
  - `MacOSPayloadConfig` (class, line 60) `class MacOSPayloadConfig`
  - `MacOSPayloadFactory` (class, line 88) `class MacOSPayloadFactory`
  - `__init__` (method, line 111) `def __init__(self, config, output_dir)`
  - `_obfuscate_shell` (method, line 116) `def _obfuscate_shell(self, code)`
  - `_reverse_shell_command` (method, line 122) `def _reverse_shell_command(self)`
  - `generate_app_bundle` (method, line 137) `def generate_app_bundle(self)`
  - `_adho_codesign` (method, line 192) `def _adho_codesign(self, app_dir)`
  - `generate_launchd_persistence` (method, line 212) `def generate_launchd_persistence(self)`
  - `generate_tcc_bypass` (method, line 268) `def generate_tcc_bypass(self)`
  - `generate_osascript_dropper` (method, line 314) `def generate_osascript_dropper(self)`
  - `generate_swift_stager` (method, line 335) `def generate_swift_stager(self)`
  - `generate_persistence_scripts` (method, line 398) `def generate_persistence_scripts(self)`
  - `generate_phishing_dialog` (method, line 447) `def generate_phishing_dialog(self)`
  - `generate_all` (method, line 470) `def generate_all(self)`
  - `list_tcc_services` (method, line 517) `def list_tcc_services()`
  - `list_persistence_methods` (method, line 522) `def list_persistence_methods()`
- Imported by: `cli/commands/payload_arsenal.py`

## modules/mario.py
- Layer: utility
- Language: py
- Symbols:
  - `check_collision` (function, line 105) `def check_collision(x, y, layer)`


Next: [KB_modules_p10.md](KB_modules_p10.md)
