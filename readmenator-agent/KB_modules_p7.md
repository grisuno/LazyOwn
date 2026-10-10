# Subsystem: modules (page 7 of 12)
Previous: [KB_modules_p6.md](KB_modules_p6.md)

## modules/lazy_rbac.py
- Doc: modules/lazy_rbac.py
- Layer: presentation
- Language: py
- Symbols:
  - `Role` (class, line 55) `class Role(Enum)`
  - `Permission` (class, line 66) `class Permission(Enum)`
  - `_UsersFileUnreadable` (class, line 115) `class _UsersFileUnreadable(Exception)`
  - `RBACUser` (class, line 124) `class RBACUser`
  - `RBACStore` (class, line 210) `class RBACStore`
  - `_generate_recovery_codes` (method, line 356) `def _generate_recovery_codes(count)`
  - `TenantConfig` (class, line 368) `class TenantConfig`
  - `TenantManager` (class, line 394) `class TenantManager`
  - `_slugify` (method, line 514) `def _slugify(name)`
  - `init_rbac_store` (method, line 523) `def init_rbac_store(users_path)`
  - `init_tenant_manager` (method, line 527) `def init_tenant_manager(payloads_dir, config_path, default_payload)`
  - `require_role` (method, line 539) `def require_role()`
  - `require_permission` (method, line 565) `def require_permission()`
  - `require_mfa` (method, line 596) `def require_mfa(f)`
  - `_get_rbac_user` (method, line 619) `def _get_rbac_user(flask_user)`
  - `_get_rbac_store` (method, line 632) `def _get_rbac_store()`
  - `get_rbac_store` (method, line 639) `def get_rbac_store()`
  - `set_rbac_store` (method, line 643) `def set_rbac_store(store)`
  - `get_tenant_manager` (method, line 648) `def get_tenant_manager()`
  - `set_tenant_manager` (method, line 655) `def set_tenant_manager(tm)`
  - `check_cli_permission` (method, line 660) `def check_cli_permission(username, permission)`
  - `get_user_role` (method, line 672) `def get_user_role(username)`
  - `generate_mfa_qr_url` (method, line 680) `def generate_mfa_qr_url(secret, username)`
  - `generate_qr_svg` (method, line 689) `def generate_qr_svg(data)`
  - `_qr_choose_version` (method, line 744) `def _qr_choose_version(data)`
  - `_qr_ec_codewords` (method, line 752) `def _qr_ec_codewords(version)`
  - `_qr_encode_alphanumeric` (method, line 757) `def _qr_encode_alphanumeric(data, version)`
  - `_qr_data_bits_for_version` (method, line 812) `def _qr_data_bits_for_version(version)`
  - `_qr_blank_matrix` (method, line 823) `def _qr_blank_matrix(version)`
  - `_qr_place_dark_module` (method, line 832) `def _qr_place_dark_module(matrix, size, version)`
  - `_qr_add_format_info` (method, line 836) `def _qr_add_format_info(modules, size, ecl_bits, mask)`
  - `_qr_svg_error` (method, line 860) `def _qr_svg_error(msg)`
  - `_qr_place_finders` (method, line 869) `def _qr_place_finders(matrix, size)`
  - `_qr_place_timing` (method, line 878) `def _qr_place_timing(matrix, size)`
  - `_qr_data_bits_positions` (method, line 884) `def _qr_data_bits_positions(matrix, size)`
  - `_bits_to_bytes` (method, line 903) `def _bits_to_bytes(bits, data_bits)`
  - `_reed_solomon_encode` (method, line 914) `def _reed_solomon_encode(data, ec_words)`
  - `_qr_best_mask` (method, line 950) `def _qr_best_mask(modules, size)`
  - `_qr_apply_mask` (method, line 963) `def _qr_apply_mask(modules, size, mask)`
  - `_qr_penalty` (method, line 996) `def _qr_penalty(modules, size)`
  - `_qr_render_svg` (method, line 1058) `def _qr_render_svg(modules, size, modules_per_pixel)`
  - `valid_roles` (method, line 62) `def valid_roles(cls)`
  - `to_dict` (method, line 136) `def to_dict(self)`
  - `from_dict` (method, line 140) `def from_dict(cls, data)`
  - `get_role` (method, line 164) `def get_role(self)`
  - `has_permission` (method, line 170) `def has_permission(self, permission)`
  - `can_manage_role` (method, line 174) `def can_manage_role(self, target_role)`
  - `get_mfa_provisioning_uri` (method, line 182) `def get_mfa_provisioning_uri(self)`
  - `verify_totp` (method, line 187) `def verify_totp(self, token)`
  - `verify_recovery_code` (method, line 192) `def verify_recovery_code(self, code)`
  - `consume_recovery_code` (method, line 200) `def consume_recovery_code(self, code)`
  - `__init__` (method, line 213) `def __init__(self, users_path)`
  - `_read_users` (method, line 217) `def _read_users(self)`
  - `_write_users` (method, line 232) `def _write_users(self, users)`
  - `load_all` (method, line 245) `def load_all(self)`
  - `find_by_id` (method, line 249) `def find_by_id(self, user_id)`
  - `find_by_username` (method, line 255) `def find_by_username(self, username)`
  - `save` (method, line 261) `def save(self, user)`
  - `create_user` (method, line 274) `def create_user(self, username, password_hash, role, tenant_id)`
  - `delete_user` (method, line 295) `def delete_user(self, user_id)`
  - `update_role` (method, line 304) `def update_role(self, user_id, new_role)`
  - `enable_mfa` (method, line 314) `def enable_mfa(self, user_id)`
  - `disable_mfa` (method, line 324) `def disable_mfa(self, user_id)`
  - `consume_recovery_code` (method, line 334) `def consume_recovery_code(self, user_id, code)`
  - `ensure_admin` (method, line 343) `def ensure_admin(self, username, password_hash)`
  - `from_payload` (method, line 377) `def from_payload(cls, tenant_id, name, payload_path)`
  - `to_dict` (method, line 386) `def to_dict(self)`
  - `from_dict` (method, line 390) `def from_dict(cls, data)`
  - `__init__` (method, line 397) `def __init__(self, payloads_dir, config_path, default_payload)`
  - `_load_config` (method, line 410) `def _load_config(self)`
  - `_save_config` (method, line 421) `def _save_config(self)`
  - `list_tenants` (method, line 431) `def list_tenants(self)`
  - `get_active` (method, line 434) `def get_active(self)`
  - `get_active_payload_path` (method, line 439) `def get_active_payload_path(self)`
  - `get_active_sessions_dir` (method, line 445) `def get_active_sessions_dir(self)`
  - `get_payload_for_tenant` (method, line 451) `def get_payload_for_tenant(self, tenant_id)`
  - `create_tenant` (method, line 457) `def create_tenant(self, name, base_payload)`
  - `switch_tenant` (method, line 486) `def switch_tenant(self, tenant_id)`
  - `delete_tenant` (method, line 495) `def delete_tenant(self, tenant_id)`
  - `ensure_default_tenant` (method, line 504) `def ensure_default_tenant(self)`
  - `decorator` (method, line 542) `def decorator(f)`
  - `decorator` (method, line 568) `def decorator(f)`
  - `decorated` (method, line 600) `def decorated()`
  - `gf_mul` (method, line 927) `def gf_mul(a, b)`
  - `decorated` (method, line 544) `def decorated()`
  - `decorated` (method, line 570) `def decorated()`
- Depends on: `cli/commands/enum.py`, `core/logging.py`
- Imported by: `cli/commands/session_ops.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/auth.py`, `lazyc2/extensions/users.py`, `lazyc2/models.py`, `modules/cli_auth.py`, `modules/collab_bp.py`

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
  - `_aws_sig` (method, line 361) `def _aws_sig(key, msg)`
  - `_sign` (method, line 364) `def _sign(key, msg)`
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
  - `fix_sessions_owner` (function, line 67)
  - `nmaptest` (function, line 122)
  - `discover_network` (function, line 142)
  - `extract_ports_info` (function, line 811)
  - `run_nmap_script` (function, line 837)
  - `print_row` (function, line 870)
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
  - `run_proxy` (method, line 162) `def run_proxy(port)`
  - `edit_file_with_nano` (method, line 169) `def edit_file_with_nano(content)`
  - `send_request` (method, line 179) `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)`
  - `repeater` (method, line 203) `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)`
  - `lazyfuzz` (method, line 233) `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)`
  - `parse_arguments` (method, line 278) `def parse_arguments()`
  - `main` (method, line 302) `def main()`
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
  - `get_dispatcher` (method, line 4409) `def get_dispatcher()`
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
  - `ingest_campaign_lessons` (method, line 222) `def ingest_campaign_lessons(lessons_file)`
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
  - `display_record` (method, line 346) `def display_record(record)`
  - `search_logs` (method, line 382) `def search_logs(query, file_path)`
  - `start_monitoring` (method, line 413) `def start_monitoring(log_dir, mode)`
  - `parse_args` (method, line 446) `def parse_args()`
  - `__init__` (method, line 223) `def __init__(self, log_dir, mode)`
  - `initialize_file_positions` (method, line 229) `def initialize_file_positions(self)`
  - `is_monitored` (method, line 245) `def is_monitored(self, file_path)`
  - `process_file` (method, line 257) `def process_file(self, file_path)`
  - `on_modified` (method, line 331) `def on_modified(self, event)`
  - `on_created` (method, line 336) `def on_created(self, event)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`


Next: [KB_modules_p8.md](KB_modules_p8.md)
