# Subsystem: modules (page 6 of 10)
Previous: [KB_modules_p5.md](KB_modules_p5.md)

## modules/lazyk8s.py
- Doc: Container and Kubernetes attack module.
- Layer: utility
- Language: py
- Symbols:
  - `ContainerResource` (class, line 20) `class ContainerResource`
  - `ContainerFinding` (class, line 30) `class ContainerFinding`
  - `DockerEnumerator` (class, line 41) `class DockerEnumerator`
  - `K8sEnumerator` (class, line 234) `class K8sEnumerator`
  - `ContainerEscapeTechniques` (class, line 561) `class ContainerEscapeTechniques`
  - `ContainerRuntimeDetector` (class, line 693) `class ContainerRuntimeDetector`
  - `__init__` (method, line 44) `def __init__(self, socket_path)`
  - `is_socket_accessible` (method, line 47) `def is_socket_accessible(self)`
  - `_docker_api` (method, line 51) `def _docker_api(self, endpoint)`
  - `list_containers` (method, line 70) `def list_containers(self)`
  - `list_images` (method, line 92) `def list_images(self)`
  - `inspect_container` (method, line 114) `def inspect_container(self, container_id)`
  - `check_privileged_containers` (method, line 131) `def check_privileged_containers(self)`
  - `check_sensitive_mounts` (method, line 155) `def check_sensitive_mounts(self)`
  - `check_docker_socket_mount` (method, line 178) `def check_docker_socket_mount(self)`
  - `check_capabilities` (method, line 197) `def check_capabilities(self)`
  - `full_check` (method, line 220) `def full_check(self)`
  - `__init__` (method, line 237) `def __init__(self, kubeconfig, token, api_server)`
  - `_load_kubeconfig` (method, line 244) `def _load_kubeconfig(self)`
  - `_get_k8s_api` (method, line 254) `def _get_k8s_api(self, path)`
  - `list_pods` (method, line 332) `def list_pods(self, namespace)`
  - `list_namespaces` (method, line 354) `def list_namespaces(self)`
  - `list_secrets` (method, line 372) `def list_secrets(self, namespace)`
  - `list_service_accounts` (method, line 417) `def list_service_accounts(self, namespace)`
  - `check_rbac` (method, line 445) `def check_rbac(self)`
  - `check_pod_escape_vectors` (method, line 473) `def check_pod_escape_vectors(self)`
  - `full_check` (method, line 519) `def full_check(self, sessions_dir)`
  - `detect_current_environment` (method, line 621) `def detect_current_environment()`
  - `detect_runtime` (method, line 737) `def detect_runtime()`
  - `detect_mounts` (method, line 805) `def detect_mounts()`
  - `detect_dangerous_capabilities` (method, line 852) `def detect_dangerous_capabilities()`
  - `auto_detect_all` (method, line 912) `def auto_detect_all()`
- Imported by: `cli/commands/containers.py`

## modules/lazylynis.sh
- Doc: Verificar si se proporcionó un argumento para el host remoto
- Layer: utility
- Language: sh
- Symbols:
  - `check_sudo` (function, line 32)

## modules/lazymasscan.sh
- Doc: Nombre del script: lazymasscan.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh
- Symbols:
  - `extract_ports_info` (function, line 74)
  - `run_masscan_script` (function, line 94)
  - `print_row` (function, line 117)
  - `ctrl_c` (function, line 20)

## modules/lazymobilerevshell.sh
- Doc: Verificar si se pasaron los argumentos de IP y puerto
- Layer: utility
- Language: sh

## modules/lazynmap.sh
- Doc: Nombre del script: lazynmap.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh
- Symbols:
  - `cleanup` (function, line 29)
  - `nmaptest` (function, line 112)
  - `discover_network` (function, line 132)
  - `extract_ports_info` (function, line 802)
  - `run_nmap_script` (function, line 828)
  - `print_row` (function, line 861)
  - `ctrl_c` (function, line 38)

## modules/lazyown_bprfuzzer.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `_load_security_config` (function, line 44) `def _load_security_config()`
  - `load_headers_from_file` (function, line 90) `def load_headers_from_file(file_path)`
  - `load_data_from_file` (function, line 95) `def load_data_from_file(file_path)`
  - `signal_handler` (function, line 100) `def signal_handler(sig, frame)`
  - `ProxyHandler` (class, line 107) `class ProxyHandler(BaseHTTPRequestHandler)`
  - `run_proxy` (method, line 147) `def run_proxy(port)`
  - `edit_file_with_nano` (method, line 153) `def edit_file_with_nano(content)`
  - `send_request` (method, line 162) `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)`
  - `repeater` (method, line 183) `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)`
  - `lazyfuzz` (method, line 213) `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)`
  - `parse_arguments` (method, line 258) `def parse_arguments()`
  - `main` (method, line 279) `def main()`
  - `do_GET` (method, line 108) `def do_GET(self)`
  - `do_POST` (method, line 111) `def do_POST(self)`
  - `_handle_request` (method, line 114) `def _handle_request(self, method)`
- Depends on: `modules/backdoor/server.c`, `modules/security_sanitizers.py`

## modules/lazyown_bridge.py
- Doc: modules/lazyown_bridge.py
- Layer: utility
- Language: py
- Symbols:
  - `CatalogEntry` (class, line 46) `class CatalogEntry`
  - `CommandCatalog` (class, line 111) `class CommandCatalog`
  - `AbstractSelector` (class, line 1490) `class AbstractSelector(ABC)`
  - `ServiceAwareSelector` (class, line 1509) `class ServiceAwareSelector(AbstractSelector)`
  - `MitreAlignedSelector` (class, line 1549) `class MitreAlignedSelector(AbstractSelector)`
  - `TagSelector` (class, line 1578) `class TagSelector(AbstractSelector)`
  - `ContextEnricher` (class, line 1610) `class ContextEnricher`
  - `PhaseMapper` (class, line 1659) `class PhaseMapper`
  - `BridgeDispatcher` (class, line 1726) `class BridgeDispatcher`
  - `get_dispatcher` (method, line 1903) `def get_dispatcher()`
  - `build_command` (method, line 60) `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)`
  - `matches_service` (method, line 91) `def matches_service(self, services)`
  - `matches_os` (method, line 101) `def matches_os(self, os_hint)`
  - `__init__` (method, line 114) `def __init__(self)`
  - `_populate` (method, line 118) `def _populate(self)`
  - `by_phase` (method, line 1451) `def by_phase(self, phase)`
  - `by_mitre` (method, line 1457) `def by_mitre(self, technique_id)`
  - `by_service` (method, line 1461) `def by_service(self, service_name)`
  - `by_tag` (method, line 1467) `def by_tag(self, tag)`
  - `by_os` (method, line 1470) `def by_os(self, os_hint)`
  - `all_phases` (method, line 1473) `def all_phases(self)`
  - `get` (method, line 1476) `def get(self, command)`
  - `count` (method, line 1482) `def count(self)`
  - `select` (method, line 1493) `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
  - `select` (method, line 1512) `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
  - `__init__` (method, line 1552) `def __init__(self, technique_id)`
  - `select` (method, line 1556) `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
  - `__init__` (method, line 1581) `def __init__(self, tag)`
  - `select` (method, line 1585) `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
  - `enrich` (method, line 1613) `def enrich(self, entry, target, world_snapshot)`
  - `canonical_kill_chain_order` (method, line 1699) `def canonical_kill_chain_order()`
  - `to_bridge_phase` (method, line 1704) `def to_bridge_phase(self, wm_phase)`
  - `kill_chain_order` (method, line 1716) `def kill_chain_order(self)`
  - `__init__` (method, line 1732) `def __init__(self, catalog, selector, enricher, phase_mapper)`
  - `suggest` (method, line 1744) `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)`
  - `suggest_sequence` (method, line 1790) `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)`
  - `suggest_for_wm_phase` (method, line 1819) `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)`
  - `list_phase` (method, line 1837) `def list_phase(self, phase)`
  - `all_phases` (method, line 1841) `def all_phases(self)`
  - `catalog_summary` (method, line 1844) `def catalog_summary(self)`
  - `catalog_summary_filtered` (method, line 1852) `def catalog_summary_filtered(self, phase, os_hint)`
  - `catalog_count` (method, line 1889) `def catalog_count(self)`
  - `phase_kill_chain` (method, line 1892) `def phase_kill_chain(self)`
- Depends on: `modules/killchain.py`
- Imported by: `modules/unified_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_bridge_catalog_filtered.py`, `tests/test_core_modules.py`, `tests/test_exploitgym_gym.py`

## modules/lazyown_metaextract0r.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 40) `def signal_handler(sig, frame)`
  - `extract_pdf_metadata` (function, line 47) `def extract_pdf_metadata(file_path)`
  - `extract_docx_metadata` (function, line 57) `def extract_docx_metadata(file_path)`
  - `extract_ole_metadata` (function, line 67) `def extract_ole_metadata(file_path)`
  - `extract_image_metadata` (function, line 78) `def extract_image_metadata(file_path)`
  - `extract_metadata` (function, line 88) `def extract_metadata(file_path)`
  - `find_and_extract_metadata` (function, line 100) `def find_and_extract_metadata(directory, output_file)`
  - `parse_arguments` (function, line 120) `def parse_arguments()`
  - `main` (function, line 129) `def main()`

## modules/lazyown_parquet_tool.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `highlight_term` (function, line 32) `def highlight_term(text, term)`
  - `search_in_parquet` (function, line 36) `def search_in_parquet(term, parquet_files)`
  - `buscar_binarios` (function, line 49) `def buscar_binarios(args)`
  - `ejecutar_opciones` (function, line 131) `def ejecutar_opciones()`

## modules/lazyownclient.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 33) `def signal_handler(sig, frame)`
  - `pad` (function, line 47) `def pad(s)`
  - `encrypt` (function, line 50) `def encrypt(plaintext, key)`
  - `decrypt` (function, line 56) `def decrypt(ciphertext, key)`
  - `handle_command` (function, line 62) `def handle_command(cmd, key)`
  - `main` (function, line 190) `def main()`

## modules/lazyownerweb.py
- Layer: utility
- Language: py
- Symbols:
  - `send_request` (function, line 37) `def send_request(url, params, method)`
  - `test_injection` (function, line 49) `def test_injection(url, payloads, param_name, detection_strings, method)`
  - `main` (function, line 58) `def main()`
- Depends on: `core/logging.py`, `modules/logging_config.py`

## modules/lazyownserver.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 33) `def signal_handler(sig, frame)`
  - `pad` (function, line 39) `def pad(s)`
  - `encrypt` (function, line 42) `def encrypt(plaintext, key)`
  - `decrypt` (function, line 48) `def decrypt(ciphertext, key)`
  - `handle_client` (function, line 54) `def handle_client(conn, addr, key)`
  - `main` (function, line 90) `def main()`

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
  - `LessonLearned` (class, line 54) `class LessonLearned`
  - `LessonIngestor` (class, line 76) `class LessonIngestor`
  - `ingest_campaign_lessons` (method, line 217) `def ingest_campaign_lessons(lessons_file)`
  - `from_dict` (method, line 65) `def from_dict(cls, d)`
  - `__init__` (method, line 85) `def __init__(self, lessons_file, router, trainer, boost_reward)`
  - `_get_router` (method, line 97) `def _get_router(self)`
  - `_get_trainer` (method, line 108) `def _get_trainer(self)`
  - `_expert_for_topic` (method, line 119) `def _expert_for_topic(self, topic)`
  - `ingest` (method, line 122) `def ingest(self, lesson)`
  - `ingest_all` (method, line 180) `def ingest_all(self, lessons)`
  - `_load_from_file` (method, line 197) `def _load_from_file(self)`
- Depends on: `core/logging.py`, `modules/moe_router.py`, `modules/rl_trainer.py`
- Imported by: `skills/lazyown_campaign.py`, `tests/test_lesson_ingestor.py`

## modules/lilsplunky.py
- Doc: Author: Your Name Email: youremail@example.com Creation Date: 14/04/2025 License: GPL v3...
- Layer: utility
- Language: py
- Symbols:
  - `simple_parse_log_line` (function, line 68) `def simple_parse_log_line(line, file_path)`
  - `store_event` (function, line 106) `def store_event(event_data)`
  - `analyze_with_deepseek` (function, line 120) `def analyze_with_deepseek(log_entry_data)`
  - `LogFileHandler` (class, line 211) `class LogFileHandler(FileSystemEventHandler)`
  - `display_record` (method, line 338) `def display_record(record)`
  - `search_logs` (method, line 375) `def search_logs(query, file_path)`
  - `start_monitoring` (method, line 406) `def start_monitoring(log_dir, mode)`
  - `parse_args` (method, line 438) `def parse_args()`
  - `__init__` (method, line 216) `def __init__(self, log_dir, mode)`
  - `initialize_file_positions` (method, line 222) `def initialize_file_positions(self)`
  - `is_monitored` (method, line 238) `def is_monitored(self, file_path)`
  - `process_file` (method, line 250) `def process_file(self, file_path)`
  - `on_modified` (method, line 324) `def on_modified(self, event)`
  - `on_created` (method, line 329) `def on_created(self, event)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/linux_advanced_payloads.py
- Doc: Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.
- Layer: utility
- Language: py
- Symbols:
  - `LinuxAdvancedConfig` (class, line 64) `class LinuxAdvancedConfig`
  - `LinuxAdvancedPayloadFactory` (class, line 92) `class LinuxAdvancedPayloadFactory`
  - `__init__` (method, line 107) `def __init__(self, config, output_dir)`
  - `generate_ld_preload_rootkit` (method, line 112) `def generate_ld_preload_rootkit(self)`
  - `generate_ebpf_payload` (method, line 237) `def generate_ebpf_payload(self)`
  - `_ip_to_hex` (method, line 307) `def _ip_to_hex(ip_str)`
  - `generate_pam_backdoor` (method, line 313) `def generate_pam_backdoor(self)`
  - `generate_systemd_persistence` (method, line 400) `def generate_systemd_persistence(self)`
  - `generate_ssh_persistence` (method, line 462) `def generate_ssh_persistence(self)`
  - `generate_kernel_module` (method, line 523) `def generate_kernel_module(self)`
  - `generate_process_masquerade` (method, line 636) `def generate_process_masquerade(self)`
  - `generate_udev_persistence` (method, line 679) `def generate_udev_persistence(self)`
  - `generate_motd_backdoor` (method, line 694) `def generate_motd_backdoor(self)`
  - `compile_c_source` (method, line 714) `def compile_c_source(self, source, output_name, shared)`
  - `generate_all` (method, line 758) `def generate_all(self)`
  - `list_hook_functions` (method, line 802) `def list_hook_functions()`
  - `list_persistence_methods` (method, line 806) `def list_persistence_methods()`
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
  - `stop` (method, line 327) `def stop(self, listener_id)`
  - `_stop` (method, line 335) `def _stop(self, listener)`
  - `start_all` (method, line 348) `def start_all(self)`
  - `stop_all` (method, line 354) `def stop_all(self)`
  - `status` (method, line 359) `def status(self)`
  - `get_default_port` (method, line 369) `def get_default_port(self, fallback)`
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
  - `process_prompt` (function, line 121) `def process_prompt(client, prompt, debug)`
  - `process_prompt_script` (function, line 135) `def process_prompt_script(client, prompt, debug)`
  - `process_prompt_adversary` (function, line 149) `def process_prompt_adversary(client, prompt, debug)`
  - `process_prompt_general` (function, line 163) `def process_prompt_general(client, prompt, debug)`
  - `process_prompt_search` (function, line 177) `def process_prompt_search(client, prompt, debug)`
  - `process_prompt_task` (function, line 191) `def process_prompt_task(client, prompt, debug)`
  - `process_prompt_vuln` (function, line 208) `def process_prompt_vuln(client, prompt, debug, event)`
  - `process_prompt_redop` (function, line 239) `def process_prompt_redop(client, prompt, debug)`
  - `ask_general` (function, line 256) `def ask_general(prompt, debug)`
- Depends on: `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazyphishingai.py`, `core/logging.py`, `modules/llm_factory.py`, `modules/llm_prompts.py`
- Imported by: `cli/commands/ai.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_llm_adapter_parity.py`

## modules/llm_client.py
- Doc: LazyOwn Unified LLM Client
- Layer: infrastructure
- Language: py
- Symbols:
  - `LLMClient` (class, line 45) `class LLMClient`
  - `get_client` (method, line 239) `def get_client(api_key)`
  - `ask` (method, line 247) `def ask(prompt)`
  - `classify` (method, line 259) `def classify(output)`
  - `summarize` (method, line 264) `def summarize(text)`
  - `__init__` (method, line 63) `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)`
  - `ask` (method, line 79) `def ask(self, prompt)`
  - `classify` (method, line 125) `def classify(self, output)`
  - `summarize` (method, line 154) `def summarize(self, text)`
  - `_ask_groq` (method, line 174) `def _ask_groq(self, prompt, model, system, temperature)`
  - `_ask_ollama` (method, line 213) `def _ask_ollama(self, prompt, model)`
- Depends on: `core/logging.py`
- Imported by: `contrib/legacy/lazyaddon_creator.py`, `modules/planner.py`, `modules/playbook_engine.py`, `skills/lazyown_mcp.py`

## modules/llm_evaluator.py
- Doc: — Records LLM decisions and their outcomes, computes quality metrics, and exports fine-tuning...
- Layer: utility
- Language: py
- Symbols:
  - `DecisionRecord` (class, line 21) `class DecisionRecord`
  - `_new_id` (method, line 35) `def _new_id()`
  - `_record_from_dict` (method, line 39) `def _record_from_dict(d)`
  - `OutcomeRecorder` (class, line 55) `class OutcomeRecorder(ABC)`
  - `JSONLRecorder` (class, line 75) `class JSONLRecorder(OutcomeRecorder)`
  - `QualityMetrics` (class, line 140) `class QualityMetrics`
  - `_safe_mean` (method, line 150) `def _safe_mean(values)`
  - `_tactic_success_rates` (method, line 154) `def _tactic_success_rates(records)`
  - `LLMEvaluator` (class, line 161) `class LLMEvaluator`
  - `get_evaluator` (method, line 293) `def get_evaluator()`
  - `record_decision` (method, line 302) `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)`
  - `record_outcome` (method, line 315) `def record_outcome(decision_id, actual_outcome, findings_count, success)`
  - `_cli` (method, line 324) `def _cli()`
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
  - `LLMBackendUnavailableError` (class, line 115) `class LLMBackendUnavailableError(RuntimeError)`
  - `LLMBackendNotSupportedError` (class, line 119) `class LLMBackendNotSupportedError(ValueError)`
  - `default_model_for` (method, line 147) `def default_model_for(backend)`
  - `model_config_key` (method, line 168) `def model_config_key(backend)`
  - `api_key_config_key` (method, line 189) `def api_key_config_key(backend)`
  - `backend_requires_api_key` (method, line 212) `def backend_requires_api_key(backend)`
  - `load_payload` (method, line 230) `def load_payload(payload_path)`
  - `_resolve_api_key` (method, line 254) `def _resolve_api_key(config)`
  - `_resolve_api_key_for_backend` (method, line 277) `def _resolve_api_key_for_backend(backend, config)`
  - `_normalize_backend` (method, line 308) `def _normalize_backend(backend)`
  - `_build_groq` (method, line 332) `def _build_groq(config)`
  - `_build_ollama` (method, line 354) `def _build_ollama(config)`
  - `_build_openai` (method, line 368) `def _build_openai(config)`
  - `_build_anthropic` (method, line 390) `def _build_anthropic(config)`
  - `_build_deepseek` (method, line 412) `def _build_deepseek(config)`
  - `_resolve_model_identifier` (method, line 434) `def _resolve_model_identifier(backend_identifier, config)`
  - `_wrap_with_budget` (method, line 461) `def _wrap_with_budget(backend, config, backend_identifier)`
  - `get_llm_backend` (method, line 499) `def get_llm_backend(config, backend)`
  - `_build_backend` (method, line 551) `def _build_backend(normalized, resolved_config)`
  - `get_llm_backend_raw` (method, line 585) `def get_llm_backend_raw(config, backend)`
  - `try_get_llm_backend` (method, line 607) `def try_get_llm_backend(config, backend)`
- Depends on: `core/llm_budget.py`, `modules/ai_model.py`
- Imported by: `cli/commands/ai.py`, `cli/wizard.py`, `contrib/legacy/lazyllmchat.py`, `core/payload_schema.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ai_fallback.py`, `modules/llm_adapter.py`, `modules/privesc_predictor.py`, `modules/professional_report.py`, `modules/vuln_agent.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `tests/test_ai_commands_llm.py`, `tests/test_llm_adapter_parity.py`, `tests/test_payload_schema.py`, `tests/test_wizard_llm.py`

## modules/llm_prompts.py
- Doc: Canonical prompt-template and knowledge-base contract for LLM consumers.
- Layer: utility
- Language: py
- Symbols:
  - `default_project_root` (function, line 67) `def default_project_root()`
  - `resolve_model` (function, line 76) `def resolve_model(model)`
  - `truncate_message` (function, line 95) `def truncate_message(message, max_chars)`
  - `LlmPromptConfig` (class, line 111) `class LlmPromptConfig`
  - `render_kb_tail` (method, line 271) `def render_kb_tail(lines)`
  - `KnowledgeStore` (class, line 286) `class KnowledgeStore`
  - `_payload_block` (method, line 354) `def _payload_block(config)`
  - `_prompt_oneliner` (method, line 362) `def _prompt_oneliner(base_prompt, kb_text, config)`
  - `_prompt_script` (method, line 378) `def _prompt_script(base_prompt, kb_text, config)`
  - `_prompt_adversary` (method, line 393) `def _prompt_adversary(base_prompt, kb_text, config)`
  - `_prompt_general` (method, line 409) `def _prompt_general(base_prompt, kb_text, config)`
  - `_prompt_search` (method, line 422) `def _prompt_search(base_prompt, kb_text, config)`
  - `_prompt_vuln` (method, line 436) `def _prompt_vuln(base_prompt, kb_text, config)`
  - `_prompt_task` (method, line 450) `def _prompt_task(base_prompt, kb_text, config)`
  - `_prompt_redop` (method, line 462) `def _prompt_redop(base_prompt, kb_text, config)`
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


Next: [KB_modules_p7.md](KB_modules_p7.md)
