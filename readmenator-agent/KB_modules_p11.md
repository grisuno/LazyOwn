# Subsystem: modules (page 11 of 17)
Previous: [KB_modules_p10.md](KB_modules_p10.md)

## modules/lazyclonewars.sh
- Doc: Lista de repositorios (nombre y URL)
- Layer: utility
- Language: sh

## modules/lazycloud.py
- Doc: Cloud-native attack module for AWS, Azure, and GCP.
- Layer: utility
- Language: py
- Symbols:
  - `CloudResource` (class, line 87) `class CloudResource`
  - `CloudFinding` (class, line 98) `class CloudFinding`
  - `CloudMetadataHarvester` (class, line 108) `class CloudMetadataHarvester`
  - `CloudBucketEnumerator` (class, line 248) `class CloudBucketEnumerator`
  - `CloudIAMEnumerator` (class, line 342) `class CloudIAMEnumerator`
  - `CloudScanner` (class, line 390) `class CloudScanner`
  - `__init__` (method, line 111) `def __init__(self, timeout)`
  - `session` (method, line 116) `def session(self)`
  - `_get` (method, line 122) `def _get(self, url, headers)`
  - `harvest_aws` (method, line 139) `def harvest_aws(self)`
  - `harvest_azure` (method, line 184) `def harvest_azure(self)`
  - `harvest_gcp` (method, line 208) `def harvest_gcp(self)`
  - `harvest_all` (method, line 231) `def harvest_all(self)`
  - `__init__` (method, line 251) `def __init__(self, timeout)`
  - `session` (method, line 256) `def session(self)`
  - `_check_url` (method, line 262) `def _check_url(self, url)`
  - `enumerate_s3` (method, line 278) `def enumerate_s3(self, prefix, buckets)`
  - `enumerate_azure_storage` (method, line 303) `def enumerate_azure_storage(self, prefix, accounts)`
  - `enumerate_gcp_storage` (method, line 321) `def enumerate_gcp_storage(self, prefix, buckets)`
  - `enumerate_aws_iam` (method, line 345) `def enumerate_aws_iam(self, access_key, secret_key, session_token)`
  - `__init__` (method, line 393) `def __init__(self, target_domain, timeout)`
  - `full_scan` (method, line 400) `def full_scan(self, target_prefix, sessions_dir)`
  - `quick_metadata` (method, line 456) `def quick_metadata(self)`
  - `quick_buckets` (method, line 460) `def quick_buckets(self, prefix)`
  - `_aws_sig` (function, line 361) `def _aws_sig(key, msg)`
  - `_sign` (function, line 364) `def _sign(key, msg)`
- Imported by: `cli/commands/cloud.py`

## modules/lazycurl.sh
- Doc: Nombre del script: lazycurl.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh
- Symbols:
  - `ctrl_c` (function, line 23)
  - `show_help` (function, line 29)
  - `execute_curl` (function, line 52)

## modules/lazyencoder_decoder.py
- Layer: utility
- Language: py
- Symbols:
  - `base64_encode` (function, line 4) `def base64_encode(data)`
  - `base64_decode` (function, line 8) `def base64_decode(data)`
  - `caesar_cipher` (function, line 13) `def caesar_cipher(text, shift)`
  - `caesar_decipher` (function, line 27) `def caesar_decipher(text, shift)`
  - `key_substitution` (function, line 31) `def key_substitution(text, key)`
  - `key_substitution_reverse` (function, line 47) `def key_substitution_reverse(text, key)`
  - `encode` (function, line 63) `def encode(data, shift, key)`
  - `encode_string` (function, line 75) `def encode_string(data, shift, key)`
  - `decode` (function, line 82) `def decode(data, shift, key)`
  - `decode_string` (function, line 94) `def decode_string(data, shift, key)`
- Imported by: `contrib/legacy/lazycreate_webshell.py`, `contrib/legacy/lazylogpoisoning.py`, `contrib/legacy/lazyreversentlmv2.py`, `modules/test_lazyencoder_decoder.py`, `utils.py`

## modules/lazyevilwimrm.sh
- Doc: execute_evil_winrm: Función para ejecutar evil-winrm y verificar la salida
- Layer: utility
- Language: sh
- Symbols:
  - `execute_evil_winrm` (function, line 14)

## modules/lazygat.sh
- Doc: Nombre del script: lazygath.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh

## modules/lazyk8s.py
- Doc: Container and Kubernetes attack module.
- Layer: utility
- Language: py
- Symbols:
  - `ContainerResource` (class, line 20) `class ContainerResource`
  - `ContainerFinding` (class, line 30) `class ContainerFinding`
  - `DockerEnumerator` (class, line 41) `class DockerEnumerator`
  - `K8sEnumerator` (class, line 264) `class K8sEnumerator`
  - `ContainerEscapeTechniques` (class, line 624) `class ContainerEscapeTechniques`
  - `ContainerRuntimeDetector` (class, line 759) `class ContainerRuntimeDetector`
  - `__init__` (method, line 44) `def __init__(self, socket_path)`
  - `is_socket_accessible` (method, line 47) `def is_socket_accessible(self)`
  - `_docker_api` (method, line 51) `def _docker_api(self, endpoint)`
  - `list_containers` (method, line 70) `def list_containers(self)`
  - `list_images` (method, line 94) `def list_images(self)`
  - `inspect_container` (method, line 118) `def inspect_container(self, container_id)`
  - `check_privileged_containers` (method, line 137) `def check_privileged_containers(self)`
  - `check_sensitive_mounts` (method, line 162) `def check_sensitive_mounts(self)`
  - `check_docker_socket_mount` (method, line 196) `def check_docker_socket_mount(self)`
  - `check_capabilities` (method, line 217) `def check_capabilities(self)`
  - `full_check` (method, line 250) `def full_check(self)`
  - `__init__` (method, line 267) `def __init__(self, kubeconfig, token, api_server)`
  - `_load_kubeconfig` (method, line 274) `def _load_kubeconfig(self)`
  - `_get_k8s_api` (method, line 285) `def _get_k8s_api(self, path)`
  - `list_pods` (method, line 366) `def list_pods(self, namespace)`
  - `list_namespaces` (method, line 390) `def list_namespaces(self)`
  - `list_secrets` (method, line 410) `def list_secrets(self, namespace)`
  - `list_service_accounts` (method, line 462) `def list_service_accounts(self, namespace)`
  - `check_rbac` (method, line 498) `def check_rbac(self)`
  - `check_pod_escape_vectors` (method, line 530) `def check_pod_escape_vectors(self)`
  - `full_check` (method, line 582) `def full_check(self, sessions_dir)`
  - `detect_current_environment` (method, line 684) `def detect_current_environment()`
  - `detect_runtime` (method, line 803) `def detect_runtime()`
  - `detect_mounts` (method, line 874) `def detect_mounts()`
  - `detect_dangerous_capabilities` (method, line 921) `def detect_dangerous_capabilities()`
  - `auto_detect_all` (method, line 992) `def auto_detect_all()`
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
  - `fix_sessions_owner` (function, line 74)
  - `nmaptest` (function, line 129)
  - `discover_network` (function, line 149)
  - `extract_ports_info` (function, line 818)
  - `run_nmap_script` (function, line 844)
  - `print_row` (function, line 877)
  - `ctrl_c` (function, line 38)

## modules/lazyown_bprfuzzer.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `_load_security_config` (function, line 45) `def _load_security_config()`
  - `load_headers_from_file` (function, line 93) `def load_headers_from_file(file_path)`
  - `load_data_from_file` (function, line 99) `def load_data_from_file(file_path)`
  - `signal_handler` (function, line 105) `def signal_handler(sig, frame)`
  - `ProxyHandler` (class, line 114) `class ProxyHandler(BaseHTTPRequestHandler)`
  - `run_proxy` (function, line 162) `def run_proxy(port)`
  - `edit_file_with_nano` (function, line 169) `def edit_file_with_nano(content)`
  - `send_request` (function, line 179) `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)`
  - `repeater` (function, line 203) `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)`
  - `lazyfuzz` (function, line 233) `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)`
  - `parse_arguments` (function, line 278) `def parse_arguments()`
  - `main` (function, line 302) `def main()`
  - `do_GET` (method, line 115) `def do_GET(self)`
  - `do_POST` (method, line 118) `def do_POST(self)`
  - `_handle_request` (method, line 121) `def _handle_request(self, method)`
- Depends on: `modules/backdoor/server.c`, `modules/security_sanitizers.py`

## modules/lazyown_bridge.py
- Doc: modules/lazyown_bridge.py
- Layer: utility
- Language: py
- Symbols:
  - `CatalogEntry` (class, line 48) `class CatalogEntry`
  - `CommandCatalog` (class, line 115) `class CommandCatalog`
  - `AbstractSelector` (class, line 3984) `class AbstractSelector(ABC)`
  - `ServiceAwareSelector` (class, line 4002) `class ServiceAwareSelector(AbstractSelector)`
  - `MitreAlignedSelector` (class, line 4042) `class MitreAlignedSelector(AbstractSelector)`
  - `TagSelector` (class, line 4071) `class TagSelector(AbstractSelector)`
  - `ContextEnricher` (class, line 4103) `class ContextEnricher`
  - `PhaseMapper` (class, line 4153) `class PhaseMapper`
  - `BridgeDispatcher` (class, line 4233) `class BridgeDispatcher`
  - `get_dispatcher` (function, line 4409) `def get_dispatcher()`
  - `build_command` (method, line 63) `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)`
  - `matches_service` (method, line 94) `def matches_service(self, services)`
  - `matches_os` (method, line 104) `def matches_os(self, os_hint)`
  - `__init__` (method, line 118) `def __init__(self)`
  - `_populate` (method, line 122) `def _populate(self)`
  - `by_phase` (method, line 3946) `def by_phase(self, phase)`
  - `by_mitre` (method, line 3952) `def by_mitre(self, technique_id)`
  - `by_service` (method, line 3956) `def by_service(self, service_name)`
  - `by_tag` (method, line 3960) `def by_tag(self, tag)`
  - `by_os` (method, line 3963) `def by_os(self, os_hint)`
  - `all_phases` (method, line 3966) `def all_phases(self)`
  - `get` (method, line 3969) `def get(self, command)`
  - `count` (method, line 3975) `def count(self)`
  - `select` (method, line 3986) `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
  - `select` (method, line 4005) `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
  - `__init__` (method, line 4045) `def __init__(self, technique_id)`
  - `select` (method, line 4049) `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
  - `__init__` (method, line 4074) `def __init__(self, tag)`
  - `select` (method, line 4078) `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
  - `enrich` (method, line 4106) `def enrich(self, entry, target, world_snapshot)`
  - `canonical_kill_chain_order` (method, line 4204) `def canonical_kill_chain_order()`
  - `to_bridge_phase` (method, line 4210) `def to_bridge_phase(self, wm_phase)`
  - `kill_chain_order` (method, line 4223) `def kill_chain_order(self)`
  - `__init__` (method, line 4239) `def __init__(self, catalog, selector, enricher, phase_mapper)`
  - `suggest` (method, line 4251) `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)`
  - `suggest_sequence` (method, line 4296) `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)`
  - `suggest_for_wm_phase` (method, line 4325) `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)`
  - `list_phase` (method, line 4343) `def list_phase(self, phase)`
  - `all_phases` (method, line 4347) `def all_phases(self)`
  - `catalog_summary` (method, line 4350) `def catalog_summary(self)`
  - `catalog_summary_filtered` (method, line 4358) `def catalog_summary_filtered(self, phase, os_hint)`
  - `catalog_count` (method, line 4395) `def catalog_count(self)`
  - `phase_kill_chain` (method, line 4398) `def phase_kill_chain(self)`
- Depends on: `modules/killchain.py`
- Imported by: `modules/unified_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_bridge_catalog_filtered.py`, `tests/test_core_modules.py`, `tests/test_exploitgym_gym.py`

## modules/lazyown_metaextract0r.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 42) `def signal_handler(sig, frame)`
  - `extract_pdf_metadata` (function, line 51) `def extract_pdf_metadata(file_path)`
  - `extract_docx_metadata` (function, line 62) `def extract_docx_metadata(file_path)`
  - `extract_ole_metadata` (function, line 73) `def extract_ole_metadata(file_path)`
  - `extract_image_metadata` (function, line 85) `def extract_image_metadata(file_path)`
  - `extract_metadata` (function, line 96) `def extract_metadata(file_path)`
  - `find_and_extract_metadata` (function, line 109) `def find_and_extract_metadata(directory, output_file)`
  - `parse_arguments` (function, line 130) `def parse_arguments()`
  - `main` (function, line 140) `def main()`

## modules/lazyown_parquet_tool.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `highlight_term` (function, line 34) `def highlight_term(text, term)`
  - `search_in_parquet` (function, line 39) `def search_in_parquet(term, parquet_files)`
  - `buscar_binarios` (function, line 53) `def buscar_binarios(args)`
  - `ejecutar_opciones` (function, line 136) `def ejecutar_opciones()`

## modules/lazyownerweb.py
- Layer: utility
- Language: py
- Symbols:
  - `send_request` (function, line 36) `def send_request(url, params, method)`
  - `test_injection` (function, line 49) `def test_injection(url, payloads, param_name, detection_strings, method)`
  - `main` (function, line 59) `def main()`
- Depends on: `core/logging.py`, `modules/logging_config.py`

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
- Doc: Author: Your Name Email: youremail@example.com Creation Date: 14/04/2025 License: AGPL v3...
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
  - `stop` (method, line 335) `def stop(self, listener_id)`
  - `_stop` (method, line 343) `def _stop(self, listener)`
  - `start_all` (method, line 356) `def start_all(self)`
  - `stop_all` (method, line 362) `def stop_all(self)`
  - `status` (method, line 367) `def status(self)`
  - `get_default_port` (method, line 379) `def get_default_port(self, fallback)`
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
  - `safe_groq_client` (function, line 55) `def safe_groq_client(api_key)`
  - `_configure_logging` (function, line 72) `def _configure_logging(debug)`
  - `_read_prompt_file` (function, line 77) `def _read_prompt_file(prompt)`
  - `_read_error` (function, line 85) `def _read_error(prompt)`
  - `_complete` (function, line 89) `def _complete(client, full_prompt, model)`
  - `_process` (function, line 103) `def _process(client, prompt, debug, template, config)`
  - `_orchestrated` (function, line 124) `def _orchestrated(full_prompt, prompt, store, primary_error)`
  - `process_prompt` (function, line 155) `def process_prompt(client, prompt, debug)`
  - `process_prompt_script` (function, line 169) `def process_prompt_script(client, prompt, debug)`
  - `process_prompt_adversary` (function, line 183) `def process_prompt_adversary(client, prompt, debug)`
  - `process_prompt_general` (function, line 197) `def process_prompt_general(client, prompt, debug)`
  - `process_prompt_search` (function, line 211) `def process_prompt_search(client, prompt, debug)`
  - `process_prompt_task` (function, line 225) `def process_prompt_task(client, prompt, debug)`
  - `process_prompt_vuln` (function, line 242) `def process_prompt_vuln(client, prompt, debug, event)`
  - `process_prompt_redop` (function, line 273) `def process_prompt_redop(client, prompt, debug)`
  - `ask_general` (function, line 290) `def ask_general(prompt, debug)`
- Depends on: `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazyphishingai.py`, `core/logging.py`, `modules/llm_factory.py`, `modules/llm_orchestrator.py`, `modules/llm_prompts.py`
- Imported by: `cli/commands/ai.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_orchestrator.py`

## modules/llm_client.py
- Doc: LazyOwn Unified LLM Client
- Layer: infrastructure
- Language: py
- Symbols:
  - `LLMClient` (class, line 45) `class LLMClient`
  - `get_client` (function, line 268) `def get_client(api_key)`
  - `ask` (function, line 276) `def ask(prompt)`
  - `classify` (function, line 288) `def classify(output)`
  - `summarize` (function, line 293) `def summarize(text)`
  - `__init__` (method, line 63) `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)`
  - `ask` (method, line 79) `def ask(self, prompt)`
  - `classify` (method, line 130) `def classify(self, output)`
  - `summarize` (method, line 159) `def summarize(self, text)`
  - `_ask_groq` (method, line 179) `def _ask_groq(self, prompt, model, system, temperature)`
  - `_ask_ollama` (method, line 220) `def _ask_ollama(self, prompt, model)`
  - `_ask_llamacpp` (method, line 242) `def _ask_llamacpp(self, prompt, model, system)`
- Depends on: `core/logging.py`, `modules/ai_model.py`
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


Next: [KB_modules_p12.md](KB_modules_p12.md)
