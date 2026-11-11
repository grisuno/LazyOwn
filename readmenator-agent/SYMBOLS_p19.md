# Symbols (page 19 of 51)
Previous: [SYMBOLS_p18.md](SYMBOLS_p18.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `load_headers_from_file` | function | `modules/lazyown_bprfuzzer.py:93` | `def load_headers_from_file(file_path)` |
| `main` | function | `modules/lazyown_bprfuzzer.py:302` | `def main()` |
| `parse_arguments` | function | `modules/lazyown_bprfuzzer.py:278` | `def parse_arguments()` |
| `repeater` | function | `modules/lazyown_bprfuzzer.py:203` | `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)` |
| `run_proxy` | function | `modules/lazyown_bprfuzzer.py:162` | `def run_proxy(port)` |
| `send_request` | function | `modules/lazyown_bprfuzzer.py:179` | `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)` |
| `signal_handler` | function | `modules/lazyown_bprfuzzer.py:105` | `def signal_handler(sig, frame)` |
| `AbstractSelector` | class | `modules/lazyown_bridge.py:3984` | `class AbstractSelector(ABC)` |
| `BridgeDispatcher` | class | `modules/lazyown_bridge.py:4233` | `class BridgeDispatcher` |
| `CatalogEntry` | class | `modules/lazyown_bridge.py:48` | `class CatalogEntry` |
| `CommandCatalog` | class | `modules/lazyown_bridge.py:115` | `class CommandCatalog` |
| `ContextEnricher` | class | `modules/lazyown_bridge.py:4103` | `class ContextEnricher` |
| `MitreAlignedSelector` | class | `modules/lazyown_bridge.py:4042` | `class MitreAlignedSelector(AbstractSelector)` |
| `PhaseMapper` | class | `modules/lazyown_bridge.py:4153` | `class PhaseMapper` |
| `ServiceAwareSelector` | class | `modules/lazyown_bridge.py:4002` | `class ServiceAwareSelector(AbstractSelector)` |
| `TagSelector` | class | `modules/lazyown_bridge.py:4071` | `class TagSelector(AbstractSelector)` |
| `__init__` | method | `modules/lazyown_bridge.py:118` | `def __init__(self)` |
| `__init__` | method | `modules/lazyown_bridge.py:4045` | `def __init__(self, technique_id)` |
| `__init__` | method | `modules/lazyown_bridge.py:4074` | `def __init__(self, tag)` |
| `__init__` | method | `modules/lazyown_bridge.py:4239` | `def __init__(self, catalog, selector, enricher, phase_mapper)` |
| `_populate` | method | `modules/lazyown_bridge.py:122` | `def _populate(self)` |
| `all_phases` | method | `modules/lazyown_bridge.py:3966` | `def all_phases(self)` |
| `all_phases` | method | `modules/lazyown_bridge.py:4347` | `def all_phases(self)` |
| `build_command` | method | `modules/lazyown_bridge.py:63` | `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)` |
| `by_mitre` | method | `modules/lazyown_bridge.py:3952` | `def by_mitre(self, technique_id)` |
| `by_os` | method | `modules/lazyown_bridge.py:3963` | `def by_os(self, os_hint)` |
| `by_phase` | method | `modules/lazyown_bridge.py:3946` | `def by_phase(self, phase)` |
| `by_service` | method | `modules/lazyown_bridge.py:3956` | `def by_service(self, service_name)` |
| `by_tag` | method | `modules/lazyown_bridge.py:3960` | `def by_tag(self, tag)` |
| `canonical_kill_chain_order` | method | `modules/lazyown_bridge.py:4204` | `def canonical_kill_chain_order()` |
| `catalog_count` | method | `modules/lazyown_bridge.py:4395` | `def catalog_count(self)` |
| `catalog_summary` | method | `modules/lazyown_bridge.py:4350` | `def catalog_summary(self)` |
| `catalog_summary_filtered` | method | `modules/lazyown_bridge.py:4358` | `def catalog_summary_filtered(self, phase, os_hint)` |
| `count` | method | `modules/lazyown_bridge.py:3975` | `def count(self)` |
| `enrich` | method | `modules/lazyown_bridge.py:4106` | `def enrich(self, entry, target, world_snapshot)` |
| `get` | method | `modules/lazyown_bridge.py:3969` | `def get(self, command)` |
| `get_dispatcher` | function | `modules/lazyown_bridge.py:4409` | `def get_dispatcher()` |
| `kill_chain_order` | method | `modules/lazyown_bridge.py:4223` | `def kill_chain_order(self)` |
| `list_phase` | method | `modules/lazyown_bridge.py:4343` | `def list_phase(self, phase)` |
| `matches_os` | method | `modules/lazyown_bridge.py:104` | `def matches_os(self, os_hint)` |
| `matches_service` | method | `modules/lazyown_bridge.py:94` | `def matches_service(self, services)` |
| `phase_kill_chain` | method | `modules/lazyown_bridge.py:4398` | `def phase_kill_chain(self)` |
| `select` | method | `modules/lazyown_bridge.py:3986` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:4005` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:4049` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:4078` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `suggest` | method | `modules/lazyown_bridge.py:4251` | `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)` |
| `suggest_for_wm_phase` | method | `modules/lazyown_bridge.py:4325` | `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)` |
| `suggest_sequence` | method | `modules/lazyown_bridge.py:4296` | `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)` |
| `to_bridge_phase` | method | `modules/lazyown_bridge.py:4210` | `def to_bridge_phase(self, wm_phase)` |
| `extract_docx_metadata` | function | `modules/lazyown_metaextract0r.py:62` | `def extract_docx_metadata(file_path)` |
| `extract_image_metadata` | function | `modules/lazyown_metaextract0r.py:85` | `def extract_image_metadata(file_path)` |
| `extract_metadata` | function | `modules/lazyown_metaextract0r.py:96` | `def extract_metadata(file_path)` |
| `extract_ole_metadata` | function | `modules/lazyown_metaextract0r.py:73` | `def extract_ole_metadata(file_path)` |
| `extract_pdf_metadata` | function | `modules/lazyown_metaextract0r.py:51` | `def extract_pdf_metadata(file_path)` |
| `find_and_extract_metadata` | function | `modules/lazyown_metaextract0r.py:109` | `def find_and_extract_metadata(directory, output_file)` |
| `main` | function | `modules/lazyown_metaextract0r.py:140` | `def main()` |
| `parse_arguments` | function | `modules/lazyown_metaextract0r.py:130` | `def parse_arguments()` |
| `signal_handler` | function | `modules/lazyown_metaextract0r.py:42` | `def signal_handler(sig, frame)` |
| `buscar_binarios` | function | `modules/lazyown_parquet_tool.py:53` | `def buscar_binarios(args)` |
| `ejecutar_opciones` | function | `modules/lazyown_parquet_tool.py:136` | `def ejecutar_opciones()` |
| `highlight_term` | function | `modules/lazyown_parquet_tool.py:34` | `def highlight_term(text, term)` |
| `search_in_parquet` | function | `modules/lazyown_parquet_tool.py:39` | `def search_in_parquet(term, parquet_files)` |
| `main` | function | `modules/lazyownerweb.py:59` | `def main()` |
| `send_request` | function | `modules/lazyownerweb.py:36` | `def send_request(url, params, method)` |
| `test_injection` | function | `modules/lazyownerweb.py:49` | `def test_injection(url, payloads, param_name, detection_strings, method)` |
| `_leetspeak` | function | `modules/lazypassgen.py:62` | `def _leetspeak(word)` |
| `_mutations` | function | `modules/lazypassgen.py:77` | `def _mutations(words)` |
| `_split_entities` | function | `modules/lazypassgen.py:45` | `def _split_entities(target)` |
| `export` | function | `modules/lazypassgen.py:135` | `def export(target, path)` |
| `generate` | function | `modules/lazypassgen.py:115` | `def generate(target)` |
| `fallback_ready` | function | `modules/lazypoophish.py:52` | `def fallback_ready(target)` |
| `fresh_access_token` | function | `modules/lazypoophish.py:34` | `def fresh_access_token(target)` |
| `run_fallback` | function | `modules/lazypoophish.py:71` | `def run_fallback(target, params, template, mode, targets_file, provider, shorten)` |
| `execute_psexec` | function | `modules/lazypsexec.sh:15` | `` |
| `mostrar_ayuda` | function | `modules/lazyreverse_shell.sh:21` | `` |
| `validar_ip` | function | `modules/lazyreverse_shell.sh:31` | `` |
| `providers` | function | `modules/lazyshortener.py:30` | `def providers()` |
| `shorten` | function | `modules/lazyshortener.py:35` | `def shorten(url, provider, timeout)` |
| `apply_vpn_rules` | function | `modules/lazyvpnshield.sh:45` | `` |
| `check_sudo` | function | `modules/lazyvpnshield.sh:16` | `` |
| `ctrl_c` | function | `modules/lazyvpnshield.sh:11` | `` |
| `main` | function | `modules/lazyvpnshield.sh:113` | `` |
| `save_current_rules` | function | `modules/lazyvpnshield.sh:29` | `` |
| `show_current_rules` | function | `modules/lazyvpnshield.sh:37` | `` |
| `undo_and_restore_rules` | function | `modules/lazyvpnshield.sh:86` | `` |
| `ctrl_c` | function | `modules/lazywps.sh:9` | `` |
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
| `_build_anthropic` | function | `modules/llm_factory.py:567` | `def _build_anthropic(config)` |
| `_build_backend` | function | `modules/llm_factory.py:728` | `def _build_backend(normalized, resolved_config)` |
| `_build_deepseek` | function | `modules/llm_factory.py:589` | `def _build_deepseek(config)` |
| `_build_groq` | function | `modules/llm_factory.py:495` | `def _build_groq(config)` |
| `_build_llamacpp` | function | `modules/llm_factory.py:531` | `def _build_llamacpp(config)` |
| `_build_ollama` | function | `modules/llm_factory.py:517` | `def _build_ollama(config)` |
| `_build_openai` | function | `modules/llm_factory.py:545` | `def _build_openai(config)` |
| `_is_placeholder_key` | function | `modules/llm_factory.py:333` | `def _is_placeholder_key(value)` |
| `_normalize_backend` | function | `modules/llm_factory.py:430` | `def _normalize_backend(backend)` |
| `_pi_complete` | function | `modules/llm_factory.py:830` | `def _pi_complete(model, prompt, max_tokens)` |
| `_pi_timeout` | function | `modules/llm_factory.py:818` | `def _pi_timeout()` |
| `_pooled_key` | function | `modules/llm_factory.py:376` | `def _pooled_key(backend, config, fallback)` |
| `_require_cloud_allowed` | function | `modules/llm_factory.py:463` | `def _require_cloud_allowed(normalized)` |
| `_resolve_api_key` | function | `modules/llm_factory.py:353` | `def _resolve_api_key(config)` |
| `_resolve_api_key_for_backend` | function | `modules/llm_factory.py:399` | `def _resolve_api_key_for_backend(backend, config)` |
| `_resolve_model_identifier` | function | `modules/llm_factory.py:611` | `def _resolve_model_identifier(backend_identifier, config)` |
| `_wrap_with_budget` | function | `modules/llm_factory.py:638` | `def _wrap_with_budget(backend, config, backend_identifier)` |
| `api_key_config_key` | function | `modules/llm_factory.py:266` | `def api_key_config_key(backend)` |
| `backend_requires_api_key` | function | `modules/llm_factory.py:291` | `def backend_requires_api_key(backend)` |
| `complete` | function | `modules/llm_factory.py:942` | `def complete(model, prompt, max_tokens)` |
| `default_model_for` | function | `modules/llm_factory.py:224` | `def default_model_for(backend)` |
| `get_llm_backend` | function | `modules/llm_factory.py:676` | `def get_llm_backend(config, backend)` |
| `get_llm_backend_raw` | function | `modules/llm_factory.py:772` | `def get_llm_backend_raw(config, backend)` |
| `groq_model_chain` | function | `modules/llm_factory.py:141` | `def groq_model_chain(config)` |
| `is_model_missing_error` | function | `modules/llm_factory.py:121` | `def is_model_missing_error(message)` |
| `load_payload` | function | `modules/llm_factory.py:309` | `def load_payload(payload_path)` |
| `model_config_key` | function | `modules/llm_factory.py:245` | `def model_config_key(backend)` |
| `stream_complete` | function | `modules/llm_factory.py:871` | `def stream_complete(model, prompt, max_tokens, on_delta)` |
| `try_get_llm_backend` | function | `modules/llm_factory.py:794` | `def try_get_llm_backend(config, backend)` |
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
| `EngineProxyMixin` | class | `modules/loop/engine_proxy.py:4` | `class EngineProxyMixin` |
| `_maybe_proxy_gc` | method | `modules/loop/engine_proxy.py:157` | `def _maybe_proxy_gc(self)` |
| `ingest_proxy_traffic` | method | `modules/loop/engine_proxy.py:75` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `proxy_env` | method | `modules/loop/engine_proxy.py:66` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/loop/engine_proxy.py:16` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/loop/engine_proxy.py:60` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/loop/engine_proxy.py:52` | `def proxy_stop(self)` |
| `search_proxy_body` | method | `modules/loop/engine_proxy.py:130` | `def search_proxy_body(self, task_id, query, limit)` |
| `TriageScheduler` | class | `modules/loop/triage_scheduler.py:73` | `class TriageScheduler` |
| `__init__` | method | `modules/loop/triage_scheduler.py:80` | `def __init__(self, stop_loss_attempts, salvage_progress, hard_threshold)` |
| `_clamp01` | function | `modules/loop/triage_scheduler.py:30` | `def _clamp01(value)` |
| `_item` | function | `modules/loop/triage_scheduler.py:61` | `def _item(record)` |
| `estimate_difficulty` | function | `modules/loop/triage_scheduler.py:35` | `def estimate_difficulty(facts)` |
| `normal_key` | function | `modules/loop/triage_scheduler.py:144` | `def normal_key(record)` |
| `order` | method | `modules/loop/triage_scheduler.py:121` | `def order(self, records)` |
| `pick_next` | method | `modules/loop/triage_scheduler.py:160` | `def pick_next(self, records)` |
| `route` | method | `modules/loop/triage_scheduler.py:110` | `def route(self, record)` |
| `salvage_key` | function | `modules/loop/triage_scheduler.py:151` | `def salvage_key(record)` |
| `should_stop` | method | `modules/loop/triage_scheduler.py:98` | `def should_stop(self, record)` |
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

Next: [SYMBOLS_p20.md](SYMBOLS_p20.md)
