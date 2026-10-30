# Subsystem: modules (page 11 of 17)
Previous: [KB_modules_p10.md](KB_modules_p10.md)

## modules/lazy_verify.py
- Doc: Structured read-only verification of loop findings.
- Layer: utility
- Language: py
- Symbols:
  - `_cap` (function, line 52) `def _cap(text, cap)`
  - `_host_port` (function, line 57) `def _host_port(finding_text, poc)`
  - `plan_checks` (function, line 84) `def plan_checks(finding_text, poc)`
  - `_nmap_available` (function, line 133) `def _nmap_available()`
  - `run_check` (function, line 143) `def run_check(check, executor)`
  - `verdict_from_checks` (function, line 214) `def verdict_from_checks(checks_results)`
  - `verify_finding` (function, line 232) `def verify_finding(finding_text, poc, executor)`
  - `_add` (function, line 104) `def _add(kind, command, check_port)`
- Depends on: `core/process.py`

## modules/lazy_world_diff.py
- Doc: World-surface diff: host snapshots, change detection, ghost liveness.
- Layer: utility
- Language: py
- Symbols:
  - `SurfaceChange` (class, line 65) `class SurfaceChange`
  - `host_snapshot` (function, line 78) `def host_snapshot(world, ip)`
  - `snapshot_fingerprint` (function, line 119) `def snapshot_fingerprint(state)`
  - `_port_number` (function, line 124) `def _port_number(key)`
  - `diff_snapshots` (function, line 131) `def diff_snapshots(before, after)`
  - `_changes_path` (function, line 172) `def _changes_path(sessions_dir)`
  - `_load_changes` (function, line 176) `def _load_changes(sessions_dir)`
  - `_as_change` (function, line 192) `def _as_change(change)`
  - `record_changes` (function, line 200) `def record_changes(changes, sessions_dir, now)`
  - `recent_changes` (function, line 260) `def recent_changes(sessions_dir, days, host)`
  - `prune_changes` (function, line 270) `def prune_changes(sessions_dir, keep_days)`
  - `load_host_snapshots` (function, line 290) `def load_host_snapshots(sessions_dir)`
  - `save_host_snapshots` (function, line 301) `def save_host_snapshots(snapshots, sessions_dir)`
  - `campaign_snapshots` (function, line 312) `def campaign_snapshots(sessions_dir)`
  - `ghost_endpoints` (function, line 366) `def ghost_endpoints(snapshot, limit)`
  - `name_resolves` (function, line 395) `def name_resolves(host, resolver)`
  - `_default_resolve` (function, line 406) `def _default_resolve(host)`
  - `_default_probe` (function, line 415) `def _default_probe(ip, port, scheme, host)`
  - `load_ghosts` (function, line 435) `def load_ghosts(sessions_dir)`
  - `ghost_state_apply` (function, line 447) `def ghost_state_apply(host, answers, sessions_dir, now)`
  - `find_ghost_hosts` (function, line 489) `def find_ghost_hosts(candidates, snapshots, checker, resolver, cap)`
  - `snapshot_engagement` (function, line 528) `def snapshot_engagement(sessions_dir, now, world)`
- Depends on: `modules/world_model.py`
- Imported by: `modules/intel_fusion.py`, `modules/lazy_hostscore.py`, `modules/lazy_loop.py`, `modules/sinks/world_diff.py`, `tests/test_lazy_world_diff.py`, `tests/test_mediation.py`, `tests/test_world_diff_retest.py`

## modules/lazyatack.sh
- Doc: Nombre del script: lazyatack.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh
- Symbols:
  - `mostrar_ayuda` (function, line 21)
  - `validar_ip` (function, line 33)
  - `validar_url` (function, line 49)
  - `descargar_seclists` (function, line 107)
  - `escanear_puertos` (function, line 115)
  - `escanear_puertos_especificos` (function, line 121)
  - `enumerar_http` (function, line 127)
  - `iniciar_servidor_http` (function, line 133)
  - `configurar_netcat` (function, line 139)
  - `enviar_archivo_netcat` (function, line 145)
  - `verificar_conectividad` (function, line 151)
  - `verificar_curl` (function, line 158)
  - `configurar_shell_reversa` (function, line 165)
  - `escuchar_shell` (function, line 171)
  - `monitorear_procesos` (function, line 177)
  - `ejecutar_wfuzz` (function, line 188)
  - `comprobar_sudo` (function, line 194)
  - `explotar_lfi` (function, line 200)
  - `configurar_tty` (function, line 206)
  - `eliminar_archivos` (function, line 217)
  - `obtener_root_shell` (function, line 223)
  - `enumerar_suid` (function, line 230)
  - `listar_timers` (function, line 236)
  - `comprobar_rutas` (function, line 242)
  - `abusar_tar` (function, line 248)
  - `enumerar_puertos` (function, line 254)
  - `eliminar_contenedores_docker` (function, line 260)
  - `escanear_red` (function, line 266)
  - `menu_servidor` (function, line 272)
  - `menu_cliente` (function, line 307)

## modules/lazybrutesshuserenum.sh
- Doc: Función para manejar el interruptor de señal Ctrl+C
- Layer: utility
- Language: sh

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

## modules/lazydorks.py
- Doc: LazyDorks: target-aware Google and GitHub dork generator for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `categories` (function, line 96) `def categories()`
  - `queries` (function, line 101) `def queries(category, domain, org)`
  - `all_queries` (function, line 123) `def all_queries(domain, org)`
  - `write_report` (function, line 137) `def write_report(path, domain, org)`

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

## modules/lazypassgen.py
- Doc: LazyPassGen: target-aware weak-password generator for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `_split_entities` (function, line 45) `def _split_entities(target)`
  - `_leetspeak` (function, line 62) `def _leetspeak(word)`
  - `_mutations` (function, line 77) `def _mutations(words)`
  - `generate` (function, line 115) `def generate(target)`
  - `export` (function, line 135) `def export(target, path)`
- Depends on: `modules/__init__.py`

## modules/lazypoophish.py
- Doc: LazyPoophish: phishing fallback delivery for the LazyOwn autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `fresh_access_token` (function, line 34) `def fresh_access_token(target)`
  - `fallback_ready` (function, line 52) `def fallback_ready(target)`
  - `run_fallback` (function, line 71) `def run_fallback(target, params, template, mode, targets_file, provider, shorten)`
- Depends on: `modules/chain_tokens.py`, `modules/lazyshortener.py`, `modules/phishing_orchestrator.py`

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

## modules/lazyshortener.py
- Doc: LazyShortener: URL shortener bridge for LazyOwn phishing delivery.
- Layer: utility
- Language: py
- Symbols:
  - `providers` (function, line 30) `def providers()`
  - `shorten` (function, line 35) `def shorten(url, provider, timeout)`
- Depends on: `core/safe_exec.py`
- Imported by: `modules/lazypoophish.py`

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


Next: [KB_modules_p12.md](KB_modules_p12.md)
