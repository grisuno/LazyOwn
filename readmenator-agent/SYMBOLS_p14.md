# Symbols (page 14 of 35)
Previous: [SYMBOLS_p13.md](SYMBOLS_p13.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_wrap_with_budget` | method | `modules/llm_factory.py:459` | `def _wrap_with_budget(backend, config, backend_identifier)` |
| `api_key_config_key` | method | `modules/llm_factory.py:188` | `def api_key_config_key(backend)` |
| `backend_requires_api_key` | method | `modules/llm_factory.py:211` | `def backend_requires_api_key(backend)` |
| `default_model_for` | method | `modules/llm_factory.py:146` | `def default_model_for(backend)` |
| `get_llm_backend` | method | `modules/llm_factory.py:497` | `def get_llm_backend(config, backend)` |
| `get_llm_backend_raw` | method | `modules/llm_factory.py:583` | `def get_llm_backend_raw(config, backend)` |
| `load_payload` | method | `modules/llm_factory.py:229` | `def load_payload(payload_path)` |
| `model_config_key` | method | `modules/llm_factory.py:167` | `def model_config_key(backend)` |
| `try_get_llm_backend` | method | `modules/llm_factory.py:605` | `def try_get_llm_backend(config, backend)` |
| `KnowledgeStore` | class | `modules/llm_prompts.py:286` | `class KnowledgeStore` |
| `LlmPromptConfig` | class | `modules/llm_prompts.py:111` | `class LlmPromptConfig` |
| `__init__` | method | `modules/llm_prompts.py:289` | `def __init__(self, path)` |
| `_payload_block` | method | `modules/llm_prompts.py:354` | `def _payload_block(config)` |
| `_prompt_adversary` | method | `modules/llm_prompts.py:393` | `def _prompt_adversary(base_prompt, kb_text, config)` |
| `_prompt_general` | method | `modules/llm_prompts.py:409` | `def _prompt_general(base_prompt, kb_text, config)` |
| `_prompt_oneliner` | method | `modules/llm_prompts.py:362` | `def _prompt_oneliner(base_prompt, kb_text, config)` |
| `_prompt_redop` | method | `modules/llm_prompts.py:462` | `def _prompt_redop(base_prompt, kb_text, config)` |
| `_prompt_script` | method | `modules/llm_prompts.py:378` | `def _prompt_script(base_prompt, kb_text, config)` |
| `_prompt_search` | method | `modules/llm_prompts.py:422` | `def _prompt_search(base_prompt, kb_text, config)` |
| `_prompt_task` | method | `modules/llm_prompts.py:450` | `def _prompt_task(base_prompt, kb_text, config)` |
| `_prompt_vuln` | method | `modules/llm_prompts.py:436` | `def _prompt_vuln(base_prompt, kb_text, config)` |
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
| `render_kb_tail` | method | `modules/llm_prompts.py:271` | `def render_kb_tail(lines)` |
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
| `_ensure_log_dir_writable` | method | `modules/logging_config.py:156` | `def _ensure_log_dir_writable(log_dir)` |
| `_use_json_format` | method | `modules/logging_config.py:235` | `def _use_json_format()` |
| `clear_correlation_id` | method | `modules/logging_config.py:144` | `def clear_correlation_id()` |
| `configure` | method | `modules/logging_config.py:244` | `def configure(level, log_dir, console, file, format_console, format_file, max_bytes, backup_count, module_levels)` |
| `emit` | method | `modules/logging_config.py:116` | `def emit(self, record)` |
| `filter` | method | `modules/logging_config.py:94` | `def filter(self, record)` |
| `format` | method | `modules/logging_config.py:39` | `def format(self, record)` |
| `format` | method | `modules/logging_config.py:72` | `def format(self, record)` |
| `get_correlation_id` | method | `modules/logging_config.py:139` | `def get_correlation_id()` |
| `get_logger` | method | `modules/logging_config.py:328` | `def get_logger(name, level)` |
| `handleError` | method | `modules/logging_config.py:122` | `def handleError(self, record)` |
| `reset` | method | `modules/logging_config.py:388` | `def reset()` |
| `set_correlation_id` | method | `modules/logging_config.py:134` | `def set_correlation_id(cid)` |
| `set_level` | method | `modules/logging_config.py:357` | `def set_level(name, level)` |
| `set_quiet` | method | `modules/logging_config.py:367` | `def set_quiet()` |
| `set_verbose` | method | `modules/logging_config.py:373` | `def set_verbose()` |
| `silence_module` | method | `modules/logging_config.py:379` | `def silence_module(name)` |
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
| `AgentBridgeWorker` | class | `modules/mcp_agent_bridge.py:462` | `class AgentBridgeWorker` |
| `GroqAgentWorker` | class | `modules/mcp_agent_bridge.py:228` | `class GroqAgentWorker` |
| `OllamaReActWorker` | class | `modules/mcp_agent_bridge.py:361` | `class OllamaReActWorker` |
| `__init__` | method | `modules/mcp_agent_bridge.py:229` | `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)` |
| `__init__` | method | `modules/mcp_agent_bridge.py:362` | `def __init__(self, agent_id, goal, client, model, run_cmd, max_iter)` |
| `__init__` | method | `modules/mcp_agent_bridge.py:465` | `def __init__(self, agent_id, goal, backend, run_cmd, max_iterations)` |
| `_agent_file` | function | `modules/mcp_agent_bridge.py:135` | `def _agent_file(agent_id)` |
| `_make_client` | function | `modules/mcp_agent_bridge.py:39` | `def _make_client(backend)` |
| `_ollama_chat` | function | `modules/mcp_agent_bridge.py:86` | `def _ollama_chat(model, messages, max_tokens, timeout)` |
| `_parse` | method | `modules/mcp_agent_bridge.py:375` | `def _parse(self, text)` |
| `_read_log` | function | `modules/mcp_agent_bridge.py:144` | `def _read_log(agent_id)` |
| `_tools` | method | `modules/mcp_agent_bridge.py:242` | `def _tools(self)` |
| `_write_log` | function | `modules/mcp_agent_bridge.py:139` | `def _write_log(agent_id, entry)` |
| `dummy_runner` | method | `modules/mcp_agent_bridge.py:525` | `def dummy_runner(cmd)` |
| `get_agent_result` | function | `modules/mcp_agent_bridge.py:182` | `def get_agent_result(agent_id)` |
| `get_agent_status` | function | `modules/mcp_agent_bridge.py:157` | `def get_agent_status(agent_id)` |
| `list_agents` | function | `modules/mcp_agent_bridge.py:205` | `def list_agents(limit)` |
| `run` | method | `modules/mcp_agent_bridge.py:258` | `def run(self)` |
| `run` | method | `modules/mcp_agent_bridge.py:383` | `def run(self)` |
| `run` | method | `modules/mcp_agent_bridge.py:472` | `def run(self)` |
| `start_agent` | method | `modules/mcp_agent_bridge.py:502` | `def start_agent(goal, backend, lazyown_runner_fn, max_iterations)` |
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
| `_cli` | method | `modules/memory_store.py:341` | `def _cli()` |
| `_connect` | method | `modules/memory_store.py:136` | `def _connect(self)` |
| `_fetch` | method | `modules/memory_store.py:172` | `def _fetch(self, sql, params)` |
| `_print_entries` | method | `modules/memory_store.py:328` | `def _print_entries(entries)` |
| `_row_to_entry` | method | `modules/memory_store.py:114` | `def _row_to_entry(row)` |
| `all_entries` | method | `modules/memory_store.py:108` | `def all_entries(self, limit)` |
| `all_entries` | method | `modules/memory_store.py:212` | `def all_entries(self, limit)` |
| `by_host` | method | `modules/memory_store.py:102` | `def by_host(self, host, top_k)` |
| `by_host` | method | `modules/memory_store.py:189` | `def by_host(self, host, top_k)` |
| `by_service` | method | `modules/memory_store.py:105` | `def by_service(self, service, top_k)` |
| `by_service` | method | `modules/memory_store.py:200` | `def by_service(self, service, top_k)` |
| `close` | method | `modules/memory_store.py:111` | `def close(self)` |
| `close` | method | `modules/memory_store.py:229` | `def close(self)` |
| `export_finetuning_dataset` | method | `modules/memory_store.py:284` | `def export_finetuning_dataset(self, path)` |
| `get_memory_store` | method | `modules/memory_store.py:303` | `def get_memory_store()` |
| `recall` | method | `modules/memory_store.py:267` | `def recall(self, query, top_k)` |
| `recall` | method | `modules/memory_store.py:324` | `def recall(query, top_k)` |
| `recall_by_host` | method | `modules/memory_store.py:270` | `def recall_by_host(self, host, top_k)` |
| `recall_for_service` | method | `modules/memory_store.py:273` | `def recall_for_service(self, service_name, top_k)` |
| `remember` | method | `modules/memory_store.py:240` | `def remember(self, session_id, host, tool, command, output, findings, success)` |
| `remember` | method | `modules/memory_store.py:312` | `def remember(session_id, host, tool, command, output, findings, success)` |
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
| `_labels_key` | method | `modules/metrics.py:126` | `def _labels_key(labels)` |
| `_percentile` | method | `modules/metrics.py:234` | `def _percentile(values, percentile)` |
| `_read_all` | method | `modules/metrics.py:388` | `def _read_all(self)` |
| `append` | method | `modules/metrics.py:206` | `def append(self, record)` |
| `get` | method | `modules/metrics.py:87` | `def get(self, name, labels)` |
| `get_recorder` | method | `modules/metrics.py:452` | `def get_recorder()` |
| `inc` | method | `modules/metrics.py:69` | `def inc(self, name, labels, value)` |
| `path` | method | `modules/metrics.py:201` | `def path(self)` |
| `path` | method | `modules/metrics.py:350` | `def path(self)` |
| `prometheus_text` | method | `modules/metrics.py:107` | `def prometheus_text(self)` |
| `record` | method | `modules/metrics.py:355` | `def record(self, command, args, duration_ms, success, exit_code, source)` |
| `reset_recorder_for_tests` | method | `modules/metrics.py:466` | `def reset_recorder_for_tests(writer)` |
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
| `format_module_detail` | method | `modules/module_registry.py:589` | `def format_module_detail(m)` |
| `format_module_table` | method | `modules/module_registry.py:542` | `def format_module_table(modules, cols)` |
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
| `_load_groq_key` | method | `modules/moe_router.py:665` | `def _load_groq_key()` |
| `_save` | method | `modules/moe_router.py:341` | `def _save(self)` |
| `_softmax` | method | `modules/moe_router.py:423` | `def _softmax(values, temperature)` |
| `adjusted_weight` | method | `modules/moe_router.py:562` | `def adjusted_weight(ep)` |
| `all_for_task` | method | `modules/moe_router.py:321` | `def all_for_task(self, task_type)` |
| `ensemble` | method | `modules/moe_router.py:547` | `def ensemble(self, task_type, goal, n)` |
| `get` | method | `modules/moe_router.py:316` | `def get(self, expert_id, task_type)` |
| `get_expert` | method | `modules/moe_router.py:605` | `def get_expert(self, expert_id)` |
| `get_router` | method | `modules/moe_router.py:684` | `def get_router(api_key)` |
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
| `clear_screen` | method | `modules/morse.py:157` | `def clear_screen(config)` |
| `morse_to_text` | method | `modules/morse.py:130` | `def morse_to_text(morse_code, config)` |
| `read_choice` | method | `modules/morse.py:171` | `def read_choice(config)` |
| `reverse_morse_code` | method | `modules/morse.py:98` | `def reverse_morse_code()` |
| `run_driver` | method | `modules/morse.py:186` | `def run_driver(config)` |
| `text_to_morse` | method | `modules/morse.py:109` | `def text_to_morse(text, config)` |
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
| `formatted_item` | method | `modules/nmap2csv.py:606` | `def formatted_item(host, format_item)` |
| `generate_csv` | method | `modules/nmap2csv.py:653` | `def generate_csv(fd, results, options)` |
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
| `get_port_script_list` | method | `modules/nmap2csv.py:243` | `def get_port_script_list(self)` |
| `get_port_service_list` | method | `modules/nmap2csv.py:225` | `def get_port_service_list(self)` |
| `get_port_version_list` | method | `modules/nmap2csv.py:234` | `def get_port_version_list(self)` |
| `get_protocol` | method | `modules/nmap2csv.py:293` | `def get_protocol(self)` |
| `get_rdns_record` | method | `modules/nmap2csv.py:201` | `def get_rdns_record(self)` |
| `get_script` | method | `modules/nmap2csv.py:302` | `def get_script(self)` |
| `get_service` | method | `modules/nmap2csv.py:296` | `def get_service(self)` |
| `get_version` | method | `modules/nmap2csv.py:299` | `def get_version(self)` |
| `is_format_valid` | method | `modules/nmap2csv.py:572` | `def is_format_valid(fmt)` |
| `main` | method | `modules/nmap2csv.py:688` | `def main()` |
| `num_to_dottedquad` | function | `modules/nmap2csv.py:133` | `def num_to_dottedquad(n)` |
| `parse` | method | `modules/nmap2csv.py:362` | `def parse(fd)` |
| `parse_xml` | method | `modules/nmap2csv.py:492` | `def parse_xml(xml_file)` |
| `repeat_attributes` | method | `modules/nmap2csv.py:639` | `def repeat_attributes(attribute_list)` |
| `set_fqdn` | method | `modules/nmap2csv.py:265` | `def set_fqdn(self, fqdn)` |
| `set_mac` | method | `modules/nmap2csv.py:274` | `def set_mac(self, mac_address, mac_address_vendor)` |
| `set_network_distance` | method | `modules/nmap2csv.py:278` | `def set_network_distance(self, network_distance)` |
| `set_os` | method | `modules/nmap2csv.py:271` | `def set_os(self, os)` |
| `set_rdns_record` | method | `modules/nmap2csv.py:268` | `def set_rdns_record(self, rdns_record)` |
| `set_script` | method | `modules/nmap2csv.py:311` | `def set_script(self, script)` |
| `set_service` | method | `modules/nmap2csv.py:305` | `def set_service(self, service)` |
| `set_version` | method | `modules/nmap2csv.py:308` | `def set_version(self, version)` |
| `split_grepable_match` | method | `modules/nmap2csv.py:315` | `def split_grepable_match(raw_string)` |
| `unique_match_from_list` | function | `modules/nmap2csv.py:140` | `def unique_match_from_list(list)` |
| `build_parser` | function | `modules/nuclei_templates_sync.py:238` | `def build_parser()` |
| `canonical_dest` | function | `modules/nuclei_templates_sync.py:48` | `def canonical_dest(subdir)` |
| `clone_templates` | function | `modules/nuclei_templates_sync.py:84` | `def clone_templates(repo, staging)` |
| `count_templates` | function | `modules/nuclei_templates_sync.py:132` | `def count_templates(tree)` |
| `ensure_git_available` | function | `modules/nuclei_templates_sync.py:73` | `def ensure_git_available()` |
| `main` | function | `modules/nuclei_templates_sync.py:337` | `def main(argv)` |
| `normalize` | function | `modules/nuclei_templates_sync.py:179` | `def normalize(url)` |
| `refresh_existing_clone` | function | `modules/nuclei_templates_sync.py:188` | `def refresh_existing_clone(path, repo)` |
| `replace_dest` | function | `modules/nuclei_templates_sync.py:144` | `def replace_dest(src, dest, expected)` |
| `repo_root` | function | `modules/nuclei_templates_sync.py:39` | `def repo_root()` |
| `resolve_plan` | function | `modules/nuclei_templates_sync.py:308` | `def resolve_plan(args)` |
| `run` | function | `modules/nuclei_templates_sync.py:60` | `def run(argv, cwd)` |
| `same_remote` | function | `modules/nuclei_templates_sync.py:168` | `def same_remote(path, repo)` |
| `strip_git_traces` | function | `modules/nuclei_templates_sync.py:113` | `def strip_git_traces(tree)` |
| `sync` | function | `modules/nuclei_templates_sync.py:263` | `def sync(name, repo, dest, refresh_existing, skip_validate)` |
| `validate_subset` | function | `modules/nuclei_templates_sync.py:209` | `def validate_subset(dest, subset)` |
| `Extractor` | class | `modules/obs_parser.py:95` | `class Extractor(ABC)` |
| `Finding` | class | `modules/obs_parser.py:66` | `class Finding` |
| `FindingType` | class | `modules/obs_parser.py:50` | `class FindingType(StrEnum)` |
| `ObsParser` | class | `modules/obs_parser.py:423` | `class ObsParser` |
| `Observation` | class | `modules/obs_parser.py:76` | `class Observation` |
| `_CVEExtractor` | class | `modules/obs_parser.py:283` | `class _CVEExtractor(Extractor)` |
| `_CloudIdentityExtractor` | class | `modules/obs_parser.py:355` | `class _CloudIdentityExtractor(Extractor)` |
| `_CredentialExtractor` | class | `modules/obs_parser.py:145` | `class _CredentialExtractor(Extractor)` |
| `_DomainExtractor` | class | `modules/obs_parser.py:299` | `class _DomainExtractor(Extractor)` |
| `_EmailExtractor` | class | `modules/obs_parser.py:318` | `class _EmailExtractor(Extractor)` |
| `_ErrorExtractor` | class | `modules/obs_parser.py:334` | `class _ErrorExtractor(Extractor)` |
| `_ExtractorRegistry` | class | `modules/obs_parser.py:103` | `class _ExtractorRegistry` |
| `_HashExtractor` | class | `modules/obs_parser.py:257` | `class _HashExtractor(Extractor)` |
| `_IPExtractor` | class | `modules/obs_parser.py:127` | `class _IPExtractor(Extractor)` |
| `_PathExtractor` | class | `modules/obs_parser.py:219` | `class _PathExtractor(Extractor)` |
| `_ServiceVersionExtractor` | class | `modules/obs_parser.py:193` | `class _ServiceVersionExtractor(Extractor)` |
| `_SuccessDetector` | class | `modules/obs_parser.py:390` | `class _SuccessDetector` |
| `_UsernameExtractor` | class | `modules/obs_parser.py:235` | `class _UsernameExtractor(Extractor)` |
| `__init__` | method | `modules/obs_parser.py:106` | `def __init__(self)` |
| `__init__` | method | `modules/obs_parser.py:431` | `def __init__(self)` |
| `by_type` | method | `modules/obs_parser.py:83` | `def by_type(self, ftype)` |
| `extract` | method | `modules/obs_parser.py:99` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:134` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:175` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:198` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:224` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:245` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:271` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:288` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:305` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:323` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:345` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:367` | `def extract(self, text, host)` |
| `get_parser` | method | `modules/obs_parser.py:500` | `def get_parser()` |
| `has` | method | `modules/obs_parser.py:86` | `def has(self, ftype)` |
| `is_success` | method | `modules/obs_parser.py:407` | `def is_success(self, text)` |
| `parse` | method | `modules/obs_parser.py:454` | `def parse(self, output, host, tool)` |
| `parse` | method | `modules/obs_parser.py:508` | `def parse(output, host, tool)` |
| `register` | method | `modules/obs_parser.py:109` | `def register(self, extractor)` |
| `register` | method | `modules/obs_parser.py:450` | `def register(self, extractor)` |
| `run_all` | method | `modules/obs_parser.py:112` | `def run_all(self, text, host)` |
| `OpEvent` | class | `modules/operation.py:52` | `class OpEvent` |
| `Operation` | class | `modules/operation.py:79` | `class Operation` |
| `OperationManager` | class | `modules/operation.py:180` | `class OperationManager` |
| `OperationStatus` | class | `modules/operation.py:42` | `class OperationStatus(StrEnum)` |
| `OperationStep` | class | `modules/operation.py:63` | `class OperationStep` |
| `__init__` | method | `modules/operation.py:183` | `def __init__(self)` |
| `create` | method | `modules/operation.py:206` | `def create(self, name, target, apt_name, description)` |
| `from_dict` | method | `modules/operation.py:116` | `def from_dict(cls, d)` |
| `get` | method | `modules/operation.py:199` | `def get(self, op_id)` |
| `get_manager` | method | `modules/operation.py:471` | `def get_manager()` |
| `list` | method | `modules/operation.py:187` | `def list(self)` |
| `log_event` | method | `modules/operation.py:143` | `def log_event(self, step_index, step_name, status, summary, findings_count, error)` |
| `pause` | method | `modules/operation.py:369` | `def pause(self, op_id)` |
| `plan_from_apt` | method | `modules/operation.py:225` | `def plan_from_apt(self, op, playbook_yaml_path)` |
| `record_facts` | method | `modules/operation.py:164` | `def record_facts(self, findings)` |
| `report` | method | `modules/operation.py:431` | `def report(self, op_id)` |
| `resume` | method | `modules/operation.py:378` | `def resume(self, op_id, executor)` |
| `save` | method | `modules/operation.py:134` | `def save(self)` |
| `start` | method | `modules/operation.py:287` | `def start(self, op_id, executor)` |
| `status` | method | `modules/operation.py:396` | `def status(self, op_id)` |
| `stop` | method | `modules/operation.py:386` | `def stop(self, op_id)` |
| `timeline` | method | `modules/operation.py:425` | `def timeline(self, op_id)` |
| `to_dict` | method | `modules/operation.py:98` | `def to_dict(self)` |
| `OperatorProfile` | class | `modules/operator_profiles.py:38` | `class OperatorProfile` |
| `OperatorProfileManager` | class | `modules/operator_profiles.py:77` | `class OperatorProfileManager` |
| `__init__` | method | `modules/operator_profiles.py:88` | `def __init__(self)` |
| `_ensure_team_ca` | method | `modules/operator_profiles.py:93` | `def _ensure_team_ca(self)` |
| `_generate_operator_cert` | method | `modules/operator_profiles.py:130` | `def _generate_operator_cert(self, username)` |
| `_profile_dir` | method | `modules/operator_profiles.py:124` | `def _profile_dir(self, username)` |
| `_profile_path` | method | `modules/operator_profiles.py:127` | `def _profile_path(self, username)` |
| `_save_profile` | method | `modules/operator_profiles.py:255` | `def _save_profile(self, profile)` |
| `create_profile` | method | `modules/operator_profiles.py:192` | `def create_profile(self, username, display_name, role, lhost, lport, listener_port, c2_port, c2_malleable_route...` |
| `delete_profile` | method | `modules/operator_profiles.py:289` | `def delete_profile(self, username)` |
| `effective_config` | method | `modules/operator_profiles.py:360` | `def effective_config(self, username)` |
| `get_attribute` | method | `modules/operator_profiles.py:328` | `def get_attribute(self, username, key, default)` |
| `get_operator_profile_manager` | method | `modules/operator_profiles.py:398` | `def get_operator_profile_manager()` |
| `list_profiles` | method | `modules/operator_profiles.py:300` | `def list_profiles(self)` |
| `load_profile` | method | `modules/operator_profiles.py:260` | `def load_profile(self, username)` |
| `log_action` | method | `modules/operator_profiles.py:335` | `def log_action(self, username, action, details)` |
| `set_attribute` | method | `modules/operator_profiles.py:319` | `def set_attribute(self, username, key, value)` |
| `to_dict` | method | `modules/operator_profiles.py:57` | `def to_dict(self)` |
| `touch_activity` | method | `modules/operator_profiles.py:312` | `def touch_activity(self, username)` |
| `update_profile` | method | `modules/operator_profiles.py:276` | `def update_profile(self, username)` |
| `GateAction` | class | `modules/opsec_scorer.py:180` | `class GateAction(IntEnum)` |
| `GatedOpsecScore` | class | `modules/opsec_scorer.py:303` | `class GatedOpsecScore` |
| `OpsecContext` | class | `modules/opsec_scorer.py:232` | `class OpsecContext` |
| `OpsecScore` | class | `modules/opsec_scorer.py:265` | `class OpsecScore` |
| `OpsecScorer` | class | `modules/opsec_scorer.py:331` | `class OpsecScorer` |
| `OpsecScorerV2` | class | `modules/opsec_scorer.py:559` | `class OpsecScorerV2` |
| `RiskLevel` | class | `modules/opsec_scorer.py:170` | `class RiskLevel(IntEnum)` |
| `__init__` | method | `modules/opsec_scorer.py:343` | `def __init__(self, payload, world_model)` |
| `__init__` | method | `modules/opsec_scorer.py:617` | `def __init__(self, context)` |
| `_build_explanation` | method | `modules/opsec_scorer.py:796` | `def _build_explanation(cmd, noise, detects, gate)` |
| `_build_recommendation` | method | `modules/opsec_scorer.py:544` | `def _build_recommendation(risk_level, mitigations)` |
| `_detection_risk_label` | method | `modules/opsec_scorer.py:532` | `def _detection_risk_label(detectable, noise)` |
| `_estimate_noise` | method | `modules/opsec_scorer.py:426` | `def _estimate_noise(self, command)` |
| `_evasion_reduction` | method | `modules/opsec_scorer.py:498` | `def _evasion_reduction(self, detectable)` |
| `_find_alternatives` | method | `modules/opsec_scorer.py:777` | `def _find_alternatives(cmd)` |
| `_gather_mitigations` | method | `modules/opsec_scorer.py:510` | `def _gather_mitigations(self, detectable, noise)` |
| `_generate_mitigations` | method | `modules/opsec_scorer.py:753` | `def _generate_mitigations(noise, detects)` |
| `_get_host_purpose` | method | `modules/opsec_scorer.py:479` | `def _get_host_purpose(self, rhost)` |
| `_noise_to_risk` | method | `modules/opsec_scorer.py:527` | `def _noise_to_risk(noise)` |
| `_noise_to_risk` | method | `modules/opsec_scorer.py:739` | `def _noise_to_risk(noise)` |
| `_phase_mismatch_penalty` | method | `modules/opsec_scorer.py:448` | `def _phase_mismatch_penalty(self, tool_phase, override)` |
| `_risk_bucket` | method | `modules/opsec_scorer.py:189` | `def _risk_bucket(noise)` |
| `_risk_label` | method | `modules/opsec_scorer.py:207` | `def _risk_label(noise)` |
| `_risk_level` | method | `modules/opsec_scorer.py:219` | `def _risk_level(noise)` |
| `_risk_to_gate` | method | `modules/opsec_scorer.py:743` | `def _risk_to_gate(self, risk)` |
| `_target_sensitivity_bonus` | method | `modules/opsec_scorer.py:470` | `def _target_sensitivity_bonus(self, rhost)` |
| `assess` | method | `modules/opsec_scorer.py:622` | `def assess(self, command, extra_context)` |
| `evasion_active` | method | `modules/opsec_scorer.py:352` | `def evasion_active(self)` |
| `get_trend` | method | `modules/opsec_scorer.py:709` | `def get_trend(self)` |
| `score` | method | `modules/opsec_scorer.py:365` | `def score(self, command, rhost, phase_override)` |
| `score_batch` | method | `modules/opsec_scorer.py:413` | `def score_batch(self, commands, rhost)` |
| `score_command` | method | `modules/opsec_scorer.py:811` | `def score_command(command, payload, rhost)` |
| `should_allow` | method | `modules/opsec_scorer.py:696` | `def should_allow(self, command)` |
| `suggest_mitigations` | method | `modules/opsec_scorer.py:417` | `def suggest_mitigations(self, command, detectable_by)` |
| `to_dict` | method | `modules/opsec_scorer.py:288` | `def to_dict(self)` |
| `traffic_morphing_active` | method | `modules/opsec_scorer.py:357` | `def traffic_morphing_active(self)` |
| `DynamicShellcodePayload` | class | `modules/payload_factory.py:409` | `class DynamicShellcodePayload(PayloadTemplate)` |
| `MsfvenomPayload` | class | `modules/payload_factory.py:322` | `class MsfvenomPayload(PayloadTemplate)` |
| `PayloadFactory` | class | `modules/payload_factory.py:457` | `class PayloadFactory` |
| `PayloadTemplate` | class | `modules/payload_factory.py:216` | `class PayloadTemplate(ABC)` |
| `ReverseShellPayload` | class | `modules/payload_factory.py:251` | `class ReverseShellPayload(PayloadTemplate)` |
| `ShellcodePayload` | class | `modules/payload_factory.py:363` | `class ShellcodePayload(PayloadTemplate)` |
| `WindowsReverseShellPayload` | class | `modules/payload_factory.py:290` | `class WindowsReverseShellPayload(PayloadTemplate)` |
| `__init__` | method | `modules/payload_factory.py:222` | `def __init__(self, name, platform, arch, description, options)` |
| `__init__` | method | `modules/payload_factory.py:254` | `def __init__(self)` |
| `__init__` | method | `modules/payload_factory.py:293` | `def __init__(self)` |
| `__init__` | method | `modules/payload_factory.py:325` | `def __init__(self, name, platform, arch)` |
| `__init__` | method | `modules/payload_factory.py:374` | `def __init__(self, name, platform, arch, description, escaped_hex, patcher)` |
| `__init__` | method | `modules/payload_factory.py:416` | `def __init__(self, name, platform, arch, description, builder)` |
| `__init__` | method | `modules/payload_factory.py:464` | `def __init__(self)` |
| `_apply_format` | method | `modules/payload_factory.py:575` | `def _apply_format(data, fmt)` |
| `_build_linux_x64_reverse_tcp` | function | `modules/payload_factory.py:118` | `def _build_linux_x64_reverse_tcp(lhost, lport)` |
| `_parse_escaped_hex` | method | `modules/payload_factory.py:442` | `def _parse_escaped_hex(escaped)` |
| `_patch_shellcode_x64` | function | `modules/payload_factory.py:190` | `def _patch_shellcode_x64(raw, lhost, lport)` |
| `_register_builtins` | method | `modules/payload_factory.py:468` | `def _register_builtins(self)` |
| `format_payload_table` | method | `modules/payload_factory.py:672` | `def format_payload_table(payloads)` |
| `generate` | method | `modules/payload_factory.py:237` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:272` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:305` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:337` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:397` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:436` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:529` | `def generate(self, name, format, output)` |
| `get` | method | `modules/payload_factory.py:525` | `def get(self, name)` |
| `list` | method | `modules/payload_factory.py:516` | `def list(self, platform)` |
| `list_formats` | method | `modules/payload_factory.py:664` | `def list_formats()` |
| `register` | method | `modules/payload_factory.py:512` | `def register(self, template)` |
| `to_dict` | method | `modules/payload_factory.py:241` | `def to_dict(self)` |
| `CampaignResult` | class | `modules/phishing_orchestrator.py:167` | `class CampaignResult` |
| `CampaignTarget` | class | `modules/phishing_orchestrator.py:139` | `class CampaignTarget` |
| `PhishingOrchestrator` | class | `modules/phishing_orchestrator.py:180` | `class PhishingOrchestrator` |
| `PhishingTemplate` | class | `modules/phishing_orchestrator.py:154` | `class PhishingTemplate` |
| `__init__` | method | `modules/phishing_orchestrator.py:316` | `def __init__(self)` |
| `_decrypt_credential` | function | `modules/phishing_orchestrator.py:100` | `def _decrypt_credential(encrypted_b64)` |
| `_derive_credential_key` | function | `modules/phishing_orchestrator.py:57` | `def _derive_credential_key()` |
| `_encrypt_credential` | function | `modules/phishing_orchestrator.py:84` | `def _encrypt_credential(plaintext)` |
| `_generate_landing_page` | method | `modules/phishing_orchestrator.py:683` | `def _generate_landing_page(self, template, target_domain, campaign_id)` |

Next: [SYMBOLS_p15.md](SYMBOLS_p15.md)
