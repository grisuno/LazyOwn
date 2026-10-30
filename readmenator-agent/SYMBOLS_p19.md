# Symbols (page 19 of 48)
Previous: [SYMBOLS_p18.md](SYMBOLS_p18.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `level` | method | `modules/loop_guardrails.py:221` | `def level(self)` |
| `max_concurrent` | method | `modules/loop_guardrails.py:275` | `def max_concurrent(self)` |
| `observe` | method | `modules/loop_guardrails.py:193` | `def observe(self, command, duration_sec, output)` |
| `oscillation_pair` | method | `modules/loop_guardrails.py:163` | `def oscillation_pair(self)` |
| `path` | method | `modules/loop_guardrails.py:346` | `def path(self)` |
| `quieten` | method | `modules/loop_guardrails.py:244` | `def quieten(self, command)` |
| `record` | method | `modules/loop_guardrails.py:104` | `def record(self, command)` |
| `reset` | method | `modules/loop_guardrails.py:171` | `def reset(self)` |
| `save` | method | `modules/loop_guardrails.py:446` | `def save(self)` |
| `search` | method | `modules/loop_guardrails.py:401` | `def search(self, query, k)` |
| `search_block` | method | `modules/loop_guardrails.py:431` | `def search_block(self, query, k, max_chars)` |
| `signal` | method | `modules/loop_guardrails.py:231` | `def signal(self)` |
| `slot` | method | `modules/loop_guardrails.py:286` | `def slot(self, target)` |
| `stuck` | method | `modules/loop_guardrails.py:139` | `def stuck(self)` |
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
| `assess_opsec` | method | `modules/mediation/telemetry_mediator.py:59` | `def assess_opsec(self, command, rhost)` |
| `describe` | method | `modules/mediation/telemetry_mediator.py:19` | `def describe(self)` |
| `moe_record_outcome` | method | `modules/mediation/telemetry_mediator.py:203` | `def moe_record_outcome(self, expert_id, task_type, reward, detection_prob)` |
| `moe_route` | method | `modules/mediation/telemetry_mediator.py:162` | `def moe_route(self, task_type)` |
| `publish_event` | method | `modules/mediation/telemetry_mediator.py:23` | `def publish_event(self, task_id, worker, kind, text, severity)` |
| `record_outcome_quality` | method | `modules/mediation/telemetry_mediator.py:77` | `def record_outcome_quality(self, worker, intent_summary, facts, findings)` |
| `record_step` | method | `modules/mediation/telemetry_mediator.py:111` | `def record_step(self, task_id, worker, command, output, detection_prob)` |
| `rl_select` | method | `modules/mediation/telemetry_mediator.py:178` | `def rl_select(self, task_type, phase, candidates, deterministic)` |
| `rl_update` | method | `modules/mediation/telemetry_mediator.py:219` | `def rl_update(self, task_type, phase, action, reward, candidates, detection_prob)` |
| `swan_available` | method | `modules/mediation/telemetry_mediator.py:128` | `def swan_available(self)` |
| `swan_consult` | method | `modules/mediation/telemetry_mediator.py:137` | `def swan_consult(self, prompt, task_type, phase, timeout)` |
| `tool_class_yields` | method | `modules/mediation/telemetry_mediator.py:93` | `def tool_class_yields(self, summaries, phase)` |
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
| `ModuleInfo` | class | `modules/module_registry.py:194` | `class ModuleInfo` |
| `ModuleRegistry` | class | `modules/module_registry.py:267` | `class ModuleRegistry` |
| `__contains__` | method | `modules/module_registry.py:660` | `def __contains__(self, name)` |
| `__init__` | method | `modules/module_registry.py:216` | `def __init__(self, name, module_type, author, version, description, category, path, source, params, enabled...` |
| `__init__` | method | `modules/module_registry.py:279` | `def __init__(self, base_dir)` |
| `__iter__` | method | `modules/module_registry.py:655` | `def __iter__(self)` |
| `__len__` | method | `modules/module_registry.py:650` | `def __len__(self)` |
| `__repr__` | method | `modules/module_registry.py:263` | `def __repr__(self)` |
| `_classify` | function | `modules/module_registry.py:91` | `def _classify(category)` |
| `_classify_module_source` | function | `modules/module_registry.py:162` | `def _classify_module_source(name, source)` |
| `_extract_docstring_summary` | function | `modules/module_registry.py:180` | `def _extract_docstring_summary(source)` |
| `_load_yaml` | method | `modules/module_registry.py:641` | `def _load_yaml(path)` |
| `_looks_discoverable` | method | `modules/module_registry.py:627` | `def _looks_discoverable(source)` |
| `_scan_playbooks` | method | `modules/module_registry.py:577` | `def _scan_playbooks(self)` |
| `_scan_plugins` | method | `modules/module_registry.py:503` | `def _scan_plugins(self)` |
| `_scan_python_modules` | method | `modules/module_registry.py:597` | `def _scan_python_modules(self)` |
| `_scan_tools` | method | `modules/module_registry.py:543` | `def _scan_tools(self)` |
| `_scan_yaml_addons` | method | `modules/module_registry.py:462` | `def _scan_yaml_addons(self)` |
| `by_type` | method | `modules/module_registry.py:365` | `def by_type(self, module_type)` |
| `deprecated_modules` | method | `modules/module_registry.py:359` | `def deprecated_modules(self)` |
| `format_module_detail` | function | `modules/module_registry.py:713` | `def format_module_detail(m)` |
| `format_module_table` | function | `modules/module_registry.py:666` | `def format_module_table(modules, cols)` |
| `get` | method | `modules/module_registry.py:313` | `def get(self, name)` |
| `get_instance` | method | `modules/module_registry.py:285` | `def get_instance(cls, base_dir)` |
| `proposal_intents` | method | `modules/module_registry.py:378` | `def proposal_intents(self, texts, target, limit)` |
| `rescan` | method | `modules/module_registry.py:304` | `def rescan(self)` |
| `scan` | method | `modules/module_registry.py:291` | `def scan(self)` |
| `search` | method | `modules/module_registry.py:319` | `def search(self, query, module_type, category, enabled_only, include_deprecated)` |
| `summary` | method | `modules/module_registry.py:369` | `def summary(self)` |
| `to_dict` | method | `modules/module_registry.py:246` | `def to_dict(self)` |
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
| `get_port_script_list` | method | `modules/nmap2csv.py:243` | `def get_port_script_list(self)` |
| `get_port_service_list` | method | `modules/nmap2csv.py:225` | `def get_port_service_list(self)` |
| `get_port_version_list` | method | `modules/nmap2csv.py:234` | `def get_port_version_list(self)` |
| `get_protocol` | method | `modules/nmap2csv.py:293` | `def get_protocol(self)` |
| `get_rdns_record` | method | `modules/nmap2csv.py:201` | `def get_rdns_record(self)` |
| `get_script` | method | `modules/nmap2csv.py:302` | `def get_script(self)` |
| `get_service` | method | `modules/nmap2csv.py:296` | `def get_service(self)` |
| `get_version` | method | `modules/nmap2csv.py:299` | `def get_version(self)` |
| `is_format_valid` | function | `modules/nmap2csv.py:572` | `def is_format_valid(fmt)` |
| `main` | function | `modules/nmap2csv.py:688` | `def main()` |
| `num_to_dottedquad` | function | `modules/nmap2csv.py:133` | `def num_to_dottedquad(n)` |
| `parse` | function | `modules/nmap2csv.py:362` | `def parse(fd)` |
| `parse_xml` | function | `modules/nmap2csv.py:492` | `def parse_xml(xml_file)` |
| `repeat_attributes` | function | `modules/nmap2csv.py:639` | `def repeat_attributes(attribute_list)` |
| `set_fqdn` | method | `modules/nmap2csv.py:265` | `def set_fqdn(self, fqdn)` |
| `set_mac` | method | `modules/nmap2csv.py:274` | `def set_mac(self, mac_address, mac_address_vendor)` |
| `set_network_distance` | method | `modules/nmap2csv.py:278` | `def set_network_distance(self, network_distance)` |
| `set_os` | method | `modules/nmap2csv.py:271` | `def set_os(self, os)` |
| `set_rdns_record` | method | `modules/nmap2csv.py:268` | `def set_rdns_record(self, rdns_record)` |
| `set_script` | method | `modules/nmap2csv.py:311` | `def set_script(self, script)` |
| `set_service` | method | `modules/nmap2csv.py:305` | `def set_service(self, service)` |
| `set_version` | method | `modules/nmap2csv.py:308` | `def set_version(self, version)` |
| `split_grepable_match` | function | `modules/nmap2csv.py:315` | `def split_grepable_match(raw_string)` |
| `unique_match_from_list` | function | `modules/nmap2csv.py:140` | `def unique_match_from_list(list)` |
| `Channel` | class | `modules/notify.py:186` | `class Channel` |
| `Notifier` | class | `modules/notify.py:204` | `class Notifier` |
| `NotifyConfig` | class | `modules/notify.py:15` | `class NotifyConfig` |
| `NotifyMessage` | class | `modules/notify.py:173` | `class NotifyMessage` |
| `_GuardRedirect` | class | `modules/notify.py:158` | `class _GuardRedirect(HTTPRedirectHandler)` |
| `__init__` | method | `modules/notify.py:207` | `def __init__(self, config)` |
| `__post_init__` | method | `modules/notify.py:198` | `def __post_init__(self)` |
| `_addr_denied` | function | `modules/notify.py:105` | `def _addr_denied(addr)` |
| `dispatch` | method | `modules/notify.py:244` | `def dispatch(self, message, channels)` |
| `flush_digest` | method | `modules/notify.py:260` | `def flush_digest(self, max_age_sec)` |
| `mask_secrets` | function | `modules/notify.py:39` | `def mask_secrets(text, config)` |
| `post_url_validated` | function | `modules/notify.py:145` | `def post_url_validated(url, data, timeout)` |
| `redirect_request` | method | `modules/notify.py:159` | `def redirect_request(self, req, fp, code, msg, headers, newurl)` |
| `render` | method | `modules/notify.py:238` | `def render(self, message)` |
| `severity_rank` | function | `modules/notify.py:31` | `def severity_rank(severity, config)` |
| `should_send` | method | `modules/notify.py:215` | `def should_send(self, message, channel)` |
| `url_allowed` | function | `modules/notify.py:57` | `def url_allowed(url)` |
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
| `Extractor` | class | `modules/obs_parser.py:126` | `class Extractor(ABC)` |
| `Finding` | class | `modules/obs_parser.py:79` | `class Finding` |
| `FindingType` | class | `modules/obs_parser.py:63` | `class FindingType(StrEnum)` |
| `ObsParser` | class | `modules/obs_parser.py:454` | `class ObsParser` |
| `Observation` | class | `modules/obs_parser.py:107` | `class Observation` |
| `_CVEExtractor` | class | `modules/obs_parser.py:314` | `class _CVEExtractor(Extractor)` |
| `_CloudIdentityExtractor` | class | `modules/obs_parser.py:386` | `class _CloudIdentityExtractor(Extractor)` |
| `_CredentialExtractor` | class | `modules/obs_parser.py:176` | `class _CredentialExtractor(Extractor)` |
| `_DomainExtractor` | class | `modules/obs_parser.py:330` | `class _DomainExtractor(Extractor)` |
| `_EmailExtractor` | class | `modules/obs_parser.py:349` | `class _EmailExtractor(Extractor)` |
| `_ErrorExtractor` | class | `modules/obs_parser.py:365` | `class _ErrorExtractor(Extractor)` |
| `_ExtractorRegistry` | class | `modules/obs_parser.py:134` | `class _ExtractorRegistry` |
| `_HashExtractor` | class | `modules/obs_parser.py:288` | `class _HashExtractor(Extractor)` |
| `_IPExtractor` | class | `modules/obs_parser.py:158` | `class _IPExtractor(Extractor)` |
| `_PathExtractor` | class | `modules/obs_parser.py:250` | `class _PathExtractor(Extractor)` |
| `_ServiceVersionExtractor` | class | `modules/obs_parser.py:224` | `class _ServiceVersionExtractor(Extractor)` |
| `_SuccessDetector` | class | `modules/obs_parser.py:421` | `class _SuccessDetector` |
| `_UsernameExtractor` | class | `modules/obs_parser.py:266` | `class _UsernameExtractor(Extractor)` |
| `__init__` | method | `modules/obs_parser.py:137` | `def __init__(self)` |
| `__init__` | method | `modules/obs_parser.py:462` | `def __init__(self)` |
| `by_type` | method | `modules/obs_parser.py:114` | `def by_type(self, ftype)` |
| `extract` | method | `modules/obs_parser.py:130` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:165` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:206` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:229` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:255` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:276` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:302` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:319` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:336` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:354` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:376` | `def extract(self, text, host)` |
| `extract` | method | `modules/obs_parser.py:398` | `def extract(self, text, host)` |
| `get_parser` | function | `modules/obs_parser.py:531` | `def get_parser()` |
| `has` | method | `modules/obs_parser.py:117` | `def has(self, ftype)` |
| `is_success` | method | `modules/obs_parser.py:438` | `def is_success(self, text)` |
| `parse` | method | `modules/obs_parser.py:485` | `def parse(self, output, host, tool)` |
| `parse` | function | `modules/obs_parser.py:539` | `def parse(output, host, tool)` |
| `register` | method | `modules/obs_parser.py:140` | `def register(self, extractor)` |
| `register` | method | `modules/obs_parser.py:481` | `def register(self, extractor)` |
| `run_all` | method | `modules/obs_parser.py:143` | `def run_all(self, text, host)` |
| `with_technique` | method | `modules/obs_parser.py:88` | `def with_technique(self, mapping)` |
| `OpEvent` | class | `modules/operation.py:52` | `class OpEvent` |
| `Operation` | class | `modules/operation.py:79` | `class Operation` |
| `OperationManager` | class | `modules/operation.py:180` | `class OperationManager` |
| `OperationStatus` | class | `modules/operation.py:42` | `class OperationStatus(StrEnum)` |
| `OperationStep` | class | `modules/operation.py:63` | `class OperationStep` |
| `__init__` | method | `modules/operation.py:183` | `def __init__(self)` |
| `create` | method | `modules/operation.py:206` | `def create(self, name, target, apt_name, description)` |
| `from_dict` | method | `modules/operation.py:116` | `def from_dict(cls, d)` |
| `get` | method | `modules/operation.py:199` | `def get(self, op_id)` |
| `get_manager` | function | `modules/operation.py:471` | `def get_manager()` |
| `list` | method | `modules/operation.py:187` | `def list(self)` |
| `log_event` | method | `modules/operation.py:143` | `def log_event(self, step_index, step_name, status, summary, findings_count, error)` |

Next: [SYMBOLS_p20.md](SYMBOLS_p20.md)
