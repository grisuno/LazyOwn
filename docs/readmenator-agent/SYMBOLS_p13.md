# Symbols (page 13 of 35)
Previous: [SYMBOLS_p12.md](SYMBOLS_p12.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `SilverTicketConfig` | class | `modules/kerberos_tickets.py:36` | `class SilverTicketConfig` |
| `SilverTicketForger` | class | `modules/kerberos_tickets.py:124` | `class SilverTicketForger` |
| `SkeletonKeyInjector` | class | `modules/kerberos_tickets.py:565` | `class SkeletonKeyInjector` |
| `__init__` | method | `modules/kerberos_tickets.py:131` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:272` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:405` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:469` | `def __init__(self, kerberos_core)` |
| `_assemble_tgt` | method | `modules/kerberos_tickets.py:368` | `def _assemble_tgt(self, config, flags, enc_part)` |
| `_build_diamond_pac` | method | `modules/kerberos_tickets.py:446` | `def _build_diamond_pac(self, config)` |
| `_build_enc_ticket_part` | method | `modules/kerberos_tickets.py:206` | `def _build_enc_ticket_part(self, config, start, end, flags, key, etype)` |
| `_build_golden_enc_part` | method | `modules/kerberos_tickets.py:346` | `def _build_golden_enc_part(self, config, start, end, flags, key)` |
| `_build_golden_pac` | method | `modules/kerberos_tickets.py:339` | `def _build_golden_pac(self, config)` |
| `_build_kirbi` | method | `modules/kerberos_tickets.py:235` | `def _build_kirbi(self, ticket, enc_part, etype)` |
| `_build_silver_pac` | method | `modules/kerberos_tickets.py:200` | `def _build_silver_pac(self, config, start, end)` |
| `_build_ticket_structure` | method | `modules/kerberos_tickets.py:225` | `def _build_ticket_structure(self, config, flags, enc_part)` |
| `_impacket_command` | method | `modules/kerberos_tickets.py:254` | `def _impacket_command(self, config)` |
| `_impacket_command` | method | `modules/kerberos_tickets.py:388` | `def _impacket_command(self, config)` |
| `_mimikatz_command` | method | `modules/kerberos_tickets.py:379` | `def _mimikatz_command(self, config)` |
| `_mimikatz_inject_command` | method | `modules/kerberos_tickets.py:244` | `def _mimikatz_inject_command(self, config)` |
| `_resolve_key` | method | `modules/kerberos_tickets.py:190` | `def _resolve_key(self, config)` |
| `_resolve_krbtgt_key` | method | `modules/kerberos_tickets.py:324` | `def _resolve_krbtgt_key(self, config)` |
| `cleanup_command` | method | `modules/kerberos_tickets.py:610` | `def cleanup_command()` |
| `detect_skeleton_key` | method | `modules/kerberos_tickets.py:576` | `def detect_skeleton_key(target_host, domain, dc_ip)` |
| `forge` | method | `modules/kerberos_tickets.py:134` | `def forge(self, config)` |
| `forge` | method | `modules/kerberos_tickets.py:275` | `def forge(self, config)` |
| `forge` | method | `modules/kerberos_tickets.py:408` | `def forge(self, config)` |
| `forge_rbcd` | method | `modules/kerberos_tickets.py:530` | `def forge_rbcd(self, machine_account_hash, target_service, domain, username)` |
| `forge_s4u2self` | method | `modules/kerberos_tickets.py:472` | `def forge_s4u2self(self, tgt, session_key, target_user, target_service, domain)` |
| `inject_command` | method | `modules/kerberos_tickets.py:598` | `def inject_command(target_host)` |
| `_build_svg` | function | `modules/kill_chain_viz.py:38` | `def _build_svg(phases)` |
| `_load_phases` | function | `modules/kill_chain_viz.py:21` | `def _load_phases(sessions)` |
| `_read_target` | function | `modules/kill_chain_viz.py:31` | `def _read_target()` |
| `generate_html` | function | `modules/kill_chain_viz.py:67` | `def generate_html(target, sessions)` |
| `generate_svg` | function | `modules/kill_chain_viz.py:98` | `def generate_svg(target, sessions)` |
| `KillChain` | class | `modules/killchain.py:136` | `class KillChain` |
| `KillChainConfig` | class | `modules/killchain.py:39` | `class KillChainConfig` |
| `PhaseStatus` | class | `modules/killchain.py:127` | `class PhaseStatus` |
| `advance_phase` | method | `modules/killchain.py:242` | `def advance_phase(new_phase, world_model_path)` |
| `cli_phase_to_host_state` | method | `modules/killchain.py:182` | `def cli_phase_to_host_state(phase)` |
| `compact_progress` | method | `modules/killchain.py:348` | `def compact_progress(current_phase, phases_entered)` |
| `config` | method | `modules/killchain.py:145` | `def config()` |
| `current_phase` | method | `modules/killchain.py:195` | `def current_phase(world_model_path)` |
| `engagement_phase_to_cli` | method | `modules/killchain.py:170` | `def engagement_phase_to_cli(engagement_value)` |
| `get_killchain` | method | `modules/killchain.py:427` | `def get_killchain()` |
| `get_progress` | method | `modules/killchain.py:305` | `def get_progress(world_model_path)` |
| `is_valid_phase` | method | `modules/killchain.py:118` | `def is_valid_phase(self, phase)` |
| `phase_colors` | method | `modules/killchain.py:160` | `def phase_colors()` |
| `phase_index` | method | `modules/killchain.py:111` | `def phase_index(self, phase)` |
| `phase_index` | method | `modules/killchain.py:379` | `def phase_index(phase)` |
| `phase_labels` | method | `modules/killchain.py:155` | `def phase_labels()` |
| `phase_rich_colors` | method | `modules/killchain.py:165` | `def phase_rich_colors()` |
| `phases` | method | `modules/killchain.py:150` | `def phases()` |
| `phases_for_display` | method | `modules/killchain.py:368` | `def phases_for_display()` |
| `snapshot` | method | `modules/killchain.py:384` | `def snapshot(world_model_path)` |
| `world_model_path` | method | `modules/killchain.py:107` | `def world_model_path(self)` |
| `ReverseShellApp` | class | `modules/kivi.py:11` | `class ReverseShellApp(App)` |
| `build` | method | `modules/kivi.py:12` | `def build(self)` |
| `connect_to_server` | method | `modules/kivi.py:27` | `def connect_to_server(self, instance)` |
| `Permission` | class | `modules/lazy_rbac.py:66` | `class Permission(Enum)` |
| `RBACStore` | class | `modules/lazy_rbac.py:211` | `class RBACStore` |
| `RBACUser` | class | `modules/lazy_rbac.py:124` | `class RBACUser` |
| `Role` | class | `modules/lazy_rbac.py:55` | `class Role(Enum)` |
| `TenantConfig` | class | `modules/lazy_rbac.py:373` | `class TenantConfig` |
| `TenantManager` | class | `modules/lazy_rbac.py:399` | `class TenantManager` |
| `_UsersFileUnreadable` | class | `modules/lazy_rbac.py:115` | `class _UsersFileUnreadable(Exception)` |
| `__init__` | method | `modules/lazy_rbac.py:214` | `def __init__(self, users_path)` |
| `__init__` | method | `modules/lazy_rbac.py:402` | `def __init__(self, payloads_dir, config_path, default_payload)` |
| `_bits_to_bytes` | method | `modules/lazy_rbac.py:905` | `def _bits_to_bytes(bits, data_bits)` |
| `_generate_recovery_codes` | method | `modules/lazy_rbac.py:358` | `def _generate_recovery_codes(count)` |
| `_get_rbac_store` | method | `modules/lazy_rbac.py:636` | `def _get_rbac_store()` |
| `_get_rbac_user` | method | `modules/lazy_rbac.py:623` | `def _get_rbac_user(flask_user)` |
| `_load_config` | method | `modules/lazy_rbac.py:415` | `def _load_config(self)` |
| `_qr_add_format_info` | method | `modules/lazy_rbac.py:837` | `def _qr_add_format_info(modules, size, ecl_bits, mask)` |
| `_qr_apply_mask` | method | `modules/lazy_rbac.py:965` | `def _qr_apply_mask(modules, size, mask)` |
| `_qr_best_mask` | method | `modules/lazy_rbac.py:952` | `def _qr_best_mask(modules, size)` |
| `_qr_blank_matrix` | method | `modules/lazy_rbac.py:824` | `def _qr_blank_matrix(version)` |
| `_qr_choose_version` | method | `modules/lazy_rbac.py:745` | `def _qr_choose_version(data)` |
| `_qr_data_bits_for_version` | method | `modules/lazy_rbac.py:813` | `def _qr_data_bits_for_version(version)` |
| `_qr_data_bits_positions` | method | `modules/lazy_rbac.py:886` | `def _qr_data_bits_positions(matrix, size)` |
| `_qr_ec_codewords` | method | `modules/lazy_rbac.py:753` | `def _qr_ec_codewords(version)` |
| `_qr_encode_alphanumeric` | method | `modules/lazy_rbac.py:758` | `def _qr_encode_alphanumeric(data, version)` |
| `_qr_penalty` | method | `modules/lazy_rbac.py:998` | `def _qr_penalty(modules, size)` |
| `_qr_place_dark_module` | method | `modules/lazy_rbac.py:833` | `def _qr_place_dark_module(matrix, size, version)` |
| `_qr_place_finders` | method | `modules/lazy_rbac.py:870` | `def _qr_place_finders(matrix, size)` |
| `_qr_place_timing` | method | `modules/lazy_rbac.py:880` | `def _qr_place_timing(matrix, size)` |
| `_qr_render_svg` | method | `modules/lazy_rbac.py:1060` | `def _qr_render_svg(modules, size, modules_per_pixel)` |
| `_qr_svg_error` | method | `modules/lazy_rbac.py:861` | `def _qr_svg_error(msg)` |
| `_read_users` | method | `modules/lazy_rbac.py:218` | `def _read_users(self)` |
| `_reed_solomon_encode` | method | `modules/lazy_rbac.py:916` | `def _reed_solomon_encode(data, ec_words)` |
| `_save_config` | method | `modules/lazy_rbac.py:426` | `def _save_config(self)` |
| `_slugify` | method | `modules/lazy_rbac.py:519` | `def _slugify(name)` |
| `_write_users` | method | `modules/lazy_rbac.py:234` | `def _write_users(self, users)` |
| `can_manage_role` | method | `modules/lazy_rbac.py:173` | `def can_manage_role(self, target_role)` |
| `check_cli_permission` | method | `modules/lazy_rbac.py:664` | `def check_cli_permission(username, permission)` |
| `consume_recovery_code` | method | `modules/lazy_rbac.py:201` | `def consume_recovery_code(self, code)` |
| `consume_recovery_code` | method | `modules/lazy_rbac.py:336` | `def consume_recovery_code(self, user_id, code)` |
| `create_tenant` | method | `modules/lazy_rbac.py:462` | `def create_tenant(self, name, base_payload)` |
| `create_user` | method | `modules/lazy_rbac.py:276` | `def create_user(self, username, password_hash, role, tenant_id)` |
| `decorated` | method | `modules/lazy_rbac.py:548` | `def decorated()` |
| `decorated` | method | `modules/lazy_rbac.py:574` | `def decorated()` |
| `decorated` | method | `modules/lazy_rbac.py:604` | `def decorated()` |
| `decorator` | method | `modules/lazy_rbac.py:546` | `def decorator(f)` |
| `decorator` | method | `modules/lazy_rbac.py:572` | `def decorator(f)` |
| `delete_tenant` | method | `modules/lazy_rbac.py:500` | `def delete_tenant(self, tenant_id)` |
| `delete_user` | method | `modules/lazy_rbac.py:297` | `def delete_user(self, user_id)` |
| `disable_mfa` | method | `modules/lazy_rbac.py:326` | `def disable_mfa(self, user_id)` |
| `enable_mfa` | method | `modules/lazy_rbac.py:316` | `def enable_mfa(self, user_id)` |
| `ensure_admin` | method | `modules/lazy_rbac.py:345` | `def ensure_admin(self, username, password_hash)` |
| `ensure_default_tenant` | method | `modules/lazy_rbac.py:509` | `def ensure_default_tenant(self)` |
| `find_by_id` | method | `modules/lazy_rbac.py:251` | `def find_by_id(self, user_id)` |
| `find_by_username` | method | `modules/lazy_rbac.py:257` | `def find_by_username(self, username)` |
| `from_dict` | method | `modules/lazy_rbac.py:139` | `def from_dict(cls, data)` |
| `from_dict` | method | `modules/lazy_rbac.py:395` | `def from_dict(cls, data)` |
| `from_payload` | method | `modules/lazy_rbac.py:382` | `def from_payload(cls, tenant_id, name, payload_path)` |
| `generate_mfa_qr_url` | method | `modules/lazy_rbac.py:684` | `def generate_mfa_qr_url(secret, username)` |
| `generate_qr_svg` | method | `modules/lazy_rbac.py:693` | `def generate_qr_svg(data)` |
| `get_active` | method | `modules/lazy_rbac.py:439` | `def get_active(self)` |
| `get_active_payload_path` | method | `modules/lazy_rbac.py:444` | `def get_active_payload_path(self)` |
| `get_active_sessions_dir` | method | `modules/lazy_rbac.py:450` | `def get_active_sessions_dir(self)` |
| `get_mfa_provisioning_uri` | method | `modules/lazy_rbac.py:181` | `def get_mfa_provisioning_uri(self)` |
| `get_payload_for_tenant` | method | `modules/lazy_rbac.py:456` | `def get_payload_for_tenant(self, tenant_id)` |
| `get_rbac_store` | method | `modules/lazy_rbac.py:643` | `def get_rbac_store()` |
| `get_role` | method | `modules/lazy_rbac.py:163` | `def get_role(self)` |
| `get_tenant_manager` | method | `modules/lazy_rbac.py:652` | `def get_tenant_manager()` |
| `get_user_role` | method | `modules/lazy_rbac.py:676` | `def get_user_role(username)` |
| `gf_mul` | method | `modules/lazy_rbac.py:929` | `def gf_mul(a, b)` |
| `has_permission` | method | `modules/lazy_rbac.py:169` | `def has_permission(self, permission)` |
| `init_rbac_store` | method | `modules/lazy_rbac.py:527` | `def init_rbac_store(users_path)` |
| `init_tenant_manager` | method | `modules/lazy_rbac.py:531` | `def init_tenant_manager(payloads_dir, config_path, default_payload)` |
| `list_tenants` | method | `modules/lazy_rbac.py:436` | `def list_tenants(self)` |
| `load_all` | method | `modules/lazy_rbac.py:247` | `def load_all(self)` |
| `require_mfa` | method | `modules/lazy_rbac.py:600` | `def require_mfa(f)` |
| `require_permission` | method | `modules/lazy_rbac.py:569` | `def require_permission()` |
| `require_role` | method | `modules/lazy_rbac.py:543` | `def require_role()` |
| `save` | method | `modules/lazy_rbac.py:263` | `def save(self, user)` |
| `set_rbac_store` | method | `modules/lazy_rbac.py:647` | `def set_rbac_store(store)` |
| `set_tenant_manager` | method | `modules/lazy_rbac.py:659` | `def set_tenant_manager(tm)` |
| `switch_tenant` | method | `modules/lazy_rbac.py:491` | `def switch_tenant(self, tenant_id)` |
| `to_dict` | method | `modules/lazy_rbac.py:135` | `def to_dict(self)` |
| `to_dict` | method | `modules/lazy_rbac.py:391` | `def to_dict(self)` |
| `update_role` | method | `modules/lazy_rbac.py:306` | `def update_role(self, user_id, new_role)` |
| `valid_roles` | method | `modules/lazy_rbac.py:62` | `def valid_roles(cls)` |
| `verify_recovery_code` | method | `modules/lazy_rbac.py:193` | `def verify_recovery_code(self, code)` |
| `verify_totp` | method | `modules/lazy_rbac.py:188` | `def verify_totp(self, token)` |
| `abusar_tar` | function | `modules/lazyatack.sh:248` | `` |
| `comprobar_rutas` | function | `modules/lazyatack.sh:242` | `` |
| `comprobar_sudo` | function | `modules/lazyatack.sh:194` | `` |
| `configurar_netcat` | function | `modules/lazyatack.sh:139` | `` |
| `configurar_shell_reversa` | function | `modules/lazyatack.sh:165` | `` |
| `configurar_tty` | function | `modules/lazyatack.sh:206` | `` |
| `descargar_seclists` | function | `modules/lazyatack.sh:107` | `` |
| `ejecutar_wfuzz` | function | `modules/lazyatack.sh:188` | `` |
| `eliminar_archivos` | function | `modules/lazyatack.sh:217` | `` |
| `eliminar_contenedores_docker` | function | `modules/lazyatack.sh:260` | `` |
| `enumerar_http` | function | `modules/lazyatack.sh:127` | `` |
| `enumerar_puertos` | function | `modules/lazyatack.sh:254` | `` |
| `enumerar_suid` | function | `modules/lazyatack.sh:230` | `` |
| `enviar_archivo_netcat` | function | `modules/lazyatack.sh:145` | `` |
| `escanear_puertos` | function | `modules/lazyatack.sh:115` | `` |
| `escanear_puertos_especificos` | function | `modules/lazyatack.sh:121` | `` |
| `escanear_red` | function | `modules/lazyatack.sh:266` | `` |
| `escuchar_shell` | function | `modules/lazyatack.sh:171` | `` |
| `explotar_lfi` | function | `modules/lazyatack.sh:200` | `` |
| `iniciar_servidor_http` | function | `modules/lazyatack.sh:133` | `` |
| `listar_timers` | function | `modules/lazyatack.sh:236` | `` |
| `menu_cliente` | function | `modules/lazyatack.sh:307` | `` |
| `menu_servidor` | function | `modules/lazyatack.sh:272` | `` |
| `monitorear_procesos` | function | `modules/lazyatack.sh:177` | `` |
| `mostrar_ayuda` | function | `modules/lazyatack.sh:21` | `` |
| `obtener_root_shell` | function | `modules/lazyatack.sh:223` | `` |
| `validar_ip` | function | `modules/lazyatack.sh:33` | `` |
| `validar_url` | function | `modules/lazyatack.sh:49` | `` |
| `verificar_conectividad` | function | `modules/lazyatack.sh:151` | `` |
| `verificar_curl` | function | `modules/lazyatack.sh:158` | `` |
| `CloudBucketEnumerator` | class | `modules/lazycloud.py:216` | `class CloudBucketEnumerator` |
| `CloudFinding` | class | `modules/lazycloud.py:70` | `class CloudFinding` |
| `CloudIAMEnumerator` | class | `modules/lazycloud.py:315` | `class CloudIAMEnumerator` |
| `CloudMetadataHarvester` | class | `modules/lazycloud.py:80` | `class CloudMetadataHarvester` |
| `CloudResource` | class | `modules/lazycloud.py:59` | `class CloudResource` |
| `CloudScanner` | class | `modules/lazycloud.py:359` | `class CloudScanner` |
| `__init__` | method | `modules/lazycloud.py:83` | `def __init__(self, timeout)` |
| `__init__` | method | `modules/lazycloud.py:219` | `def __init__(self, timeout)` |
| `__init__` | method | `modules/lazycloud.py:362` | `def __init__(self, target_domain, timeout)` |
| `_aws_sig` | method | `modules/lazycloud.py:332` | `def _aws_sig(key, msg)` |
| `_check_url` | method | `modules/lazycloud.py:230` | `def _check_url(self, url)` |
| `_get` | method | `modules/lazycloud.py:94` | `def _get(self, url, headers)` |
| `_sign` | method | `modules/lazycloud.py:335` | `def _sign(key, msg)` |
| `enumerate_aws_iam` | method | `modules/lazycloud.py:318` | `def enumerate_aws_iam(self, access_key, secret_key, session_token)` |
| `enumerate_azure_storage` | method | `modules/lazycloud.py:272` | `def enumerate_azure_storage(self, prefix, accounts)` |
| `enumerate_gcp_storage` | method | `modules/lazycloud.py:292` | `def enumerate_gcp_storage(self, prefix, buckets)` |
| `enumerate_s3` | method | `modules/lazycloud.py:245` | `def enumerate_s3(self, prefix, buckets)` |
| `full_scan` | method | `modules/lazycloud.py:369` | `def full_scan(self, target_prefix, sessions_dir)` |
| `harvest_all` | method | `modules/lazycloud.py:199` | `def harvest_all(self)` |
| `harvest_aws` | method | `modules/lazycloud.py:110` | `def harvest_aws(self)` |
| `harvest_azure` | method | `modules/lazycloud.py:155` | `def harvest_azure(self)` |
| `harvest_gcp` | method | `modules/lazycloud.py:176` | `def harvest_gcp(self)` |
| `quick_buckets` | method | `modules/lazycloud.py:429` | `def quick_buckets(self, prefix)` |
| `quick_metadata` | method | `modules/lazycloud.py:425` | `def quick_metadata(self)` |
| `session` | method | `modules/lazycloud.py:88` | `def session(self)` |
| `session` | method | `modules/lazycloud.py:224` | `def session(self)` |
| `ctrl_c` | function | `modules/lazycurl.sh:23` | `` |
| `execute_curl` | function | `modules/lazycurl.sh:52` | `` |
| `show_help` | function | `modules/lazycurl.sh:29` | `` |
| `base64_decode` | function | `modules/lazyencoder_decoder.py:8` | `def base64_decode(data)` |
| `base64_encode` | function | `modules/lazyencoder_decoder.py:4` | `def base64_encode(data)` |
| `caesar_cipher` | function | `modules/lazyencoder_decoder.py:13` | `def caesar_cipher(text, shift)` |
| `caesar_decipher` | function | `modules/lazyencoder_decoder.py:27` | `def caesar_decipher(text, shift)` |
| `decode` | function | `modules/lazyencoder_decoder.py:82` | `def decode(data, shift, key)` |
| `decode_string` | function | `modules/lazyencoder_decoder.py:94` | `def decode_string(data, shift, key)` |
| `encode` | function | `modules/lazyencoder_decoder.py:63` | `def encode(data, shift, key)` |
| `encode_string` | function | `modules/lazyencoder_decoder.py:75` | `def encode_string(data, shift, key)` |
| `key_substitution` | function | `modules/lazyencoder_decoder.py:31` | `def key_substitution(text, key)` |
| `key_substitution_reverse` | function | `modules/lazyencoder_decoder.py:47` | `def key_substitution_reverse(text, key)` |
| `execute_evil_winrm` | function | `modules/lazyevilwimrm.sh:14` | `` |
| `ContainerEscapeTechniques` | class | `modules/lazyk8s.py:561` | `class ContainerEscapeTechniques` |
| `ContainerFinding` | class | `modules/lazyk8s.py:30` | `class ContainerFinding` |
| `ContainerResource` | class | `modules/lazyk8s.py:20` | `class ContainerResource` |
| `ContainerRuntimeDetector` | class | `modules/lazyk8s.py:693` | `class ContainerRuntimeDetector` |
| `DockerEnumerator` | class | `modules/lazyk8s.py:41` | `class DockerEnumerator` |
| `K8sEnumerator` | class | `modules/lazyk8s.py:234` | `class K8sEnumerator` |
| `__init__` | method | `modules/lazyk8s.py:44` | `def __init__(self, socket_path)` |
| `__init__` | method | `modules/lazyk8s.py:237` | `def __init__(self, kubeconfig, token, api_server)` |
| `_docker_api` | method | `modules/lazyk8s.py:51` | `def _docker_api(self, endpoint)` |
| `_get_k8s_api` | method | `modules/lazyk8s.py:254` | `def _get_k8s_api(self, path)` |
| `_load_kubeconfig` | method | `modules/lazyk8s.py:244` | `def _load_kubeconfig(self)` |
| `auto_detect_all` | method | `modules/lazyk8s.py:912` | `def auto_detect_all()` |
| `check_capabilities` | method | `modules/lazyk8s.py:197` | `def check_capabilities(self)` |
| `check_docker_socket_mount` | method | `modules/lazyk8s.py:178` | `def check_docker_socket_mount(self)` |
| `check_pod_escape_vectors` | method | `modules/lazyk8s.py:473` | `def check_pod_escape_vectors(self)` |
| `check_privileged_containers` | method | `modules/lazyk8s.py:131` | `def check_privileged_containers(self)` |
| `check_rbac` | method | `modules/lazyk8s.py:445` | `def check_rbac(self)` |
| `check_sensitive_mounts` | method | `modules/lazyk8s.py:155` | `def check_sensitive_mounts(self)` |
| `detect_current_environment` | method | `modules/lazyk8s.py:621` | `def detect_current_environment()` |
| `detect_dangerous_capabilities` | method | `modules/lazyk8s.py:852` | `def detect_dangerous_capabilities()` |
| `detect_mounts` | method | `modules/lazyk8s.py:805` | `def detect_mounts()` |
| `detect_runtime` | method | `modules/lazyk8s.py:737` | `def detect_runtime()` |
| `full_check` | method | `modules/lazyk8s.py:220` | `def full_check(self)` |
| `full_check` | method | `modules/lazyk8s.py:519` | `def full_check(self, sessions_dir)` |
| `inspect_container` | method | `modules/lazyk8s.py:114` | `def inspect_container(self, container_id)` |
| `is_socket_accessible` | method | `modules/lazyk8s.py:47` | `def is_socket_accessible(self)` |
| `list_containers` | method | `modules/lazyk8s.py:70` | `def list_containers(self)` |
| `list_images` | method | `modules/lazyk8s.py:92` | `def list_images(self)` |
| `list_namespaces` | method | `modules/lazyk8s.py:354` | `def list_namespaces(self)` |
| `list_pods` | method | `modules/lazyk8s.py:332` | `def list_pods(self, namespace)` |
| `list_secrets` | method | `modules/lazyk8s.py:372` | `def list_secrets(self, namespace)` |
| `list_service_accounts` | method | `modules/lazyk8s.py:417` | `def list_service_accounts(self, namespace)` |
| `check_sudo` | function | `modules/lazylynis.sh:32` | `` |
| `ctrl_c` | function | `modules/lazymasscan.sh:20` | `` |
| `extract_ports_info` | function | `modules/lazymasscan.sh:74` | `` |
| `print_row` | function | `modules/lazymasscan.sh:117` | `` |
| `run_masscan_script` | function | `modules/lazymasscan.sh:94` | `` |
| `cleanup` | function | `modules/lazynmap.sh:29` | `` |
| `ctrl_c` | function | `modules/lazynmap.sh:38` | `` |
| `discover_network` | function | `modules/lazynmap.sh:142` | `` |
| `extract_ports_info` | function | `modules/lazynmap.sh:811` | `` |
| `fix_sessions_owner` | function | `modules/lazynmap.sh:67` | `` |
| `nmaptest` | function | `modules/lazynmap.sh:122` | `` |
| `print_row` | function | `modules/lazynmap.sh:870` | `` |
| `run_nmap_script` | function | `modules/lazynmap.sh:837` | `` |
| `ProxyHandler` | class | `modules/lazyown_bprfuzzer.py:107` | `class ProxyHandler(BaseHTTPRequestHandler)` |
| `_handle_request` | method | `modules/lazyown_bprfuzzer.py:114` | `def _handle_request(self, method)` |
| `_load_security_config` | function | `modules/lazyown_bprfuzzer.py:44` | `def _load_security_config()` |
| `do_GET` | method | `modules/lazyown_bprfuzzer.py:108` | `def do_GET(self)` |
| `do_POST` | method | `modules/lazyown_bprfuzzer.py:111` | `def do_POST(self)` |
| `edit_file_with_nano` | method | `modules/lazyown_bprfuzzer.py:153` | `def edit_file_with_nano(content)` |
| `lazyfuzz` | method | `modules/lazyown_bprfuzzer.py:213` | `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)` |
| `load_data_from_file` | function | `modules/lazyown_bprfuzzer.py:95` | `def load_data_from_file(file_path)` |
| `load_headers_from_file` | function | `modules/lazyown_bprfuzzer.py:90` | `def load_headers_from_file(file_path)` |
| `main` | method | `modules/lazyown_bprfuzzer.py:279` | `def main()` |
| `parse_arguments` | method | `modules/lazyown_bprfuzzer.py:258` | `def parse_arguments()` |
| `repeater` | method | `modules/lazyown_bprfuzzer.py:183` | `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)` |
| `run_proxy` | method | `modules/lazyown_bprfuzzer.py:147` | `def run_proxy(port)` |
| `send_request` | method | `modules/lazyown_bprfuzzer.py:162` | `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)` |
| `signal_handler` | function | `modules/lazyown_bprfuzzer.py:100` | `def signal_handler(sig, frame)` |
| `AbstractSelector` | class | `modules/lazyown_bridge.py:1490` | `class AbstractSelector(ABC)` |
| `BridgeDispatcher` | class | `modules/lazyown_bridge.py:1726` | `class BridgeDispatcher` |
| `CatalogEntry` | class | `modules/lazyown_bridge.py:46` | `class CatalogEntry` |
| `CommandCatalog` | class | `modules/lazyown_bridge.py:111` | `class CommandCatalog` |
| `ContextEnricher` | class | `modules/lazyown_bridge.py:1610` | `class ContextEnricher` |
| `MitreAlignedSelector` | class | `modules/lazyown_bridge.py:1549` | `class MitreAlignedSelector(AbstractSelector)` |
| `PhaseMapper` | class | `modules/lazyown_bridge.py:1659` | `class PhaseMapper` |
| `ServiceAwareSelector` | class | `modules/lazyown_bridge.py:1509` | `class ServiceAwareSelector(AbstractSelector)` |
| `TagSelector` | class | `modules/lazyown_bridge.py:1578` | `class TagSelector(AbstractSelector)` |
| `__init__` | method | `modules/lazyown_bridge.py:114` | `def __init__(self)` |
| `__init__` | method | `modules/lazyown_bridge.py:1552` | `def __init__(self, technique_id)` |
| `__init__` | method | `modules/lazyown_bridge.py:1581` | `def __init__(self, tag)` |
| `__init__` | method | `modules/lazyown_bridge.py:1732` | `def __init__(self, catalog, selector, enricher, phase_mapper)` |
| `_populate` | method | `modules/lazyown_bridge.py:118` | `def _populate(self)` |
| `all_phases` | method | `modules/lazyown_bridge.py:1473` | `def all_phases(self)` |
| `all_phases` | method | `modules/lazyown_bridge.py:1841` | `def all_phases(self)` |
| `build_command` | method | `modules/lazyown_bridge.py:60` | `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)` |
| `by_mitre` | method | `modules/lazyown_bridge.py:1457` | `def by_mitre(self, technique_id)` |
| `by_os` | method | `modules/lazyown_bridge.py:1470` | `def by_os(self, os_hint)` |
| `by_phase` | method | `modules/lazyown_bridge.py:1451` | `def by_phase(self, phase)` |
| `by_service` | method | `modules/lazyown_bridge.py:1461` | `def by_service(self, service_name)` |
| `by_tag` | method | `modules/lazyown_bridge.py:1467` | `def by_tag(self, tag)` |
| `canonical_kill_chain_order` | method | `modules/lazyown_bridge.py:1699` | `def canonical_kill_chain_order()` |
| `catalog_count` | method | `modules/lazyown_bridge.py:1889` | `def catalog_count(self)` |
| `catalog_summary` | method | `modules/lazyown_bridge.py:1844` | `def catalog_summary(self)` |
| `catalog_summary_filtered` | method | `modules/lazyown_bridge.py:1852` | `def catalog_summary_filtered(self, phase, os_hint)` |
| `count` | method | `modules/lazyown_bridge.py:1482` | `def count(self)` |
| `enrich` | method | `modules/lazyown_bridge.py:1613` | `def enrich(self, entry, target, world_snapshot)` |
| `get` | method | `modules/lazyown_bridge.py:1476` | `def get(self, command)` |
| `get_dispatcher` | method | `modules/lazyown_bridge.py:1903` | `def get_dispatcher()` |
| `kill_chain_order` | method | `modules/lazyown_bridge.py:1716` | `def kill_chain_order(self)` |
| `list_phase` | method | `modules/lazyown_bridge.py:1837` | `def list_phase(self, phase)` |
| `matches_os` | method | `modules/lazyown_bridge.py:101` | `def matches_os(self, os_hint)` |
| `matches_service` | method | `modules/lazyown_bridge.py:91` | `def matches_service(self, services)` |
| `phase_kill_chain` | method | `modules/lazyown_bridge.py:1892` | `def phase_kill_chain(self)` |
| `select` | method | `modules/lazyown_bridge.py:1493` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:1512` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:1556` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:1585` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `suggest` | method | `modules/lazyown_bridge.py:1744` | `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)` |
| `suggest_for_wm_phase` | method | `modules/lazyown_bridge.py:1819` | `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)` |
| `suggest_sequence` | method | `modules/lazyown_bridge.py:1790` | `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)` |
| `to_bridge_phase` | method | `modules/lazyown_bridge.py:1704` | `def to_bridge_phase(self, wm_phase)` |
| `extract_docx_metadata` | function | `modules/lazyown_metaextract0r.py:57` | `def extract_docx_metadata(file_path)` |
| `extract_image_metadata` | function | `modules/lazyown_metaextract0r.py:78` | `def extract_image_metadata(file_path)` |
| `extract_metadata` | function | `modules/lazyown_metaextract0r.py:88` | `def extract_metadata(file_path)` |
| `extract_ole_metadata` | function | `modules/lazyown_metaextract0r.py:67` | `def extract_ole_metadata(file_path)` |
| `extract_pdf_metadata` | function | `modules/lazyown_metaextract0r.py:47` | `def extract_pdf_metadata(file_path)` |
| `find_and_extract_metadata` | function | `modules/lazyown_metaextract0r.py:100` | `def find_and_extract_metadata(directory, output_file)` |
| `main` | function | `modules/lazyown_metaextract0r.py:129` | `def main()` |
| `parse_arguments` | function | `modules/lazyown_metaextract0r.py:120` | `def parse_arguments()` |
| `signal_handler` | function | `modules/lazyown_metaextract0r.py:40` | `def signal_handler(sig, frame)` |
| `buscar_binarios` | function | `modules/lazyown_parquet_tool.py:49` | `def buscar_binarios(args)` |
| `ejecutar_opciones` | function | `modules/lazyown_parquet_tool.py:131` | `def ejecutar_opciones()` |
| `highlight_term` | function | `modules/lazyown_parquet_tool.py:32` | `def highlight_term(text, term)` |
| `search_in_parquet` | function | `modules/lazyown_parquet_tool.py:36` | `def search_in_parquet(term, parquet_files)` |
| `decrypt` | function | `modules/lazyownclient.py:56` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `modules/lazyownclient.py:50` | `def encrypt(plaintext, key)` |
| `handle_command` | function | `modules/lazyownclient.py:62` | `def handle_command(cmd, key)` |
| `main` | function | `modules/lazyownclient.py:190` | `def main()` |
| `pad` | function | `modules/lazyownclient.py:47` | `def pad(s)` |
| `signal_handler` | function | `modules/lazyownclient.py:33` | `def signal_handler(sig, frame)` |
| `main` | function | `modules/lazyownerweb.py:58` | `def main()` |
| `send_request` | function | `modules/lazyownerweb.py:37` | `def send_request(url, params, method)` |
| `test_injection` | function | `modules/lazyownerweb.py:49` | `def test_injection(url, payloads, param_name, detection_strings, method)` |
| `decrypt` | function | `modules/lazyownserver.py:48` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `modules/lazyownserver.py:42` | `def encrypt(plaintext, key)` |
| `handle_client` | function | `modules/lazyownserver.py:54` | `def handle_client(conn, addr, key)` |
| `main` | function | `modules/lazyownserver.py:90` | `def main()` |
| `pad` | function | `modules/lazyownserver.py:39` | `def pad(s)` |
| `signal_handler` | function | `modules/lazyownserver.py:33` | `def signal_handler(sig, frame)` |
| `execute_psexec` | function | `modules/lazypsexec.sh:15` | `` |
| `mostrar_ayuda` | function | `modules/lazyreverse_shell.sh:21` | `` |
| `validar_ip` | function | `modules/lazyreverse_shell.sh:31` | `` |
| `apply_vpn_rules` | function | `modules/lazyvpnshield.sh:45` | `` |
| `check_sudo` | function | `modules/lazyvpnshield.sh:16` | `` |
| `ctrl_c` | function | `modules/lazyvpnshield.sh:11` | `` |
| `main` | function | `modules/lazyvpnshield.sh:113` | `` |
| `save_current_rules` | function | `modules/lazyvpnshield.sh:29` | `` |
| `show_current_rules` | function | `modules/lazyvpnshield.sh:37` | `` |
| `undo_and_restore_rules` | function | `modules/lazyvpnshield.sh:86` | `` |
| `ctrl_c` | function | `modules/lazywps.sh:9` | `` |
| `LessonIngestor` | class | `modules/lesson_ingestor.py:76` | `class LessonIngestor` |
| `LessonLearned` | class | `modules/lesson_ingestor.py:54` | `class LessonLearned` |
| `__init__` | method | `modules/lesson_ingestor.py:85` | `def __init__(self, lessons_file, router, trainer, boost_reward)` |
| `_expert_for_topic` | method | `modules/lesson_ingestor.py:119` | `def _expert_for_topic(self, topic)` |
| `_get_router` | method | `modules/lesson_ingestor.py:97` | `def _get_router(self)` |
| `_get_trainer` | method | `modules/lesson_ingestor.py:108` | `def _get_trainer(self)` |
| `_load_from_file` | method | `modules/lesson_ingestor.py:197` | `def _load_from_file(self)` |
| `from_dict` | method | `modules/lesson_ingestor.py:65` | `def from_dict(cls, d)` |
| `ingest` | method | `modules/lesson_ingestor.py:122` | `def ingest(self, lesson)` |
| `ingest_all` | method | `modules/lesson_ingestor.py:180` | `def ingest_all(self, lessons)` |
| `ingest_campaign_lessons` | method | `modules/lesson_ingestor.py:217` | `def ingest_campaign_lessons(lessons_file)` |
| `LogFileHandler` | class | `modules/lilsplunky.py:211` | `class LogFileHandler(FileSystemEventHandler)` |
| `__init__` | method | `modules/lilsplunky.py:216` | `def __init__(self, log_dir, mode)` |
| `analyze_with_deepseek` | function | `modules/lilsplunky.py:120` | `def analyze_with_deepseek(log_entry_data)` |
| `display_record` | method | `modules/lilsplunky.py:338` | `def display_record(record)` |
| `initialize_file_positions` | method | `modules/lilsplunky.py:222` | `def initialize_file_positions(self)` |
| `is_monitored` | method | `modules/lilsplunky.py:238` | `def is_monitored(self, file_path)` |
| `on_created` | method | `modules/lilsplunky.py:329` | `def on_created(self, event)` |
| `on_modified` | method | `modules/lilsplunky.py:324` | `def on_modified(self, event)` |
| `parse_args` | method | `modules/lilsplunky.py:438` | `def parse_args()` |
| `process_file` | method | `modules/lilsplunky.py:250` | `def process_file(self, file_path)` |
| `search_logs` | method | `modules/lilsplunky.py:375` | `def search_logs(query, file_path)` |
| `simple_parse_log_line` | function | `modules/lilsplunky.py:68` | `def simple_parse_log_line(line, file_path)` |
| `start_monitoring` | method | `modules/lilsplunky.py:406` | `def start_monitoring(log_dir, mode)` |
| `store_event` | function | `modules/lilsplunky.py:106` | `def store_event(event_data)` |
| `LinuxAdvancedConfig` | class | `modules/linux_advanced_payloads.py:64` | `class LinuxAdvancedConfig` |
| `LinuxAdvancedPayloadFactory` | class | `modules/linux_advanced_payloads.py:92` | `class LinuxAdvancedPayloadFactory` |
| `__init__` | method | `modules/linux_advanced_payloads.py:107` | `def __init__(self, config, output_dir)` |
| `_ip_to_hex` | method | `modules/linux_advanced_payloads.py:307` | `def _ip_to_hex(ip_str)` |
| `compile_c_source` | method | `modules/linux_advanced_payloads.py:714` | `def compile_c_source(self, source, output_name, shared)` |
| `generate_all` | method | `modules/linux_advanced_payloads.py:758` | `def generate_all(self)` |
| `generate_ebpf_payload` | method | `modules/linux_advanced_payloads.py:237` | `def generate_ebpf_payload(self)` |
| `generate_kernel_module` | method | `modules/linux_advanced_payloads.py:523` | `def generate_kernel_module(self)` |
| `generate_ld_preload_rootkit` | method | `modules/linux_advanced_payloads.py:112` | `def generate_ld_preload_rootkit(self)` |
| `generate_motd_backdoor` | method | `modules/linux_advanced_payloads.py:694` | `def generate_motd_backdoor(self)` |
| `generate_pam_backdoor` | method | `modules/linux_advanced_payloads.py:313` | `def generate_pam_backdoor(self)` |
| `generate_process_masquerade` | method | `modules/linux_advanced_payloads.py:636` | `def generate_process_masquerade(self)` |
| `generate_ssh_persistence` | method | `modules/linux_advanced_payloads.py:462` | `def generate_ssh_persistence(self)` |
| `generate_systemd_persistence` | method | `modules/linux_advanced_payloads.py:400` | `def generate_systemd_persistence(self)` |
| `generate_udev_persistence` | method | `modules/linux_advanced_payloads.py:679` | `def generate_udev_persistence(self)` |
| `list_hook_functions` | method | `modules/linux_advanced_payloads.py:802` | `def list_hook_functions()` |
| `list_persistence_methods` | method | `modules/linux_advanced_payloads.py:806` | `def list_persistence_methods()` |
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
| `_stop` | method | `modules/listener_manager.py:335` | `def _stop(self, listener)` |
| `add` | method | `modules/listener_manager.py:229` | `def add(self, port, ssl, listener_id)` |
| `from_dict` | method | `modules/listener_manager.py:162` | `def from_dict(cls, data)` |
| `get_default_port` | method | `modules/listener_manager.py:369` | `def get_default_port(self, fallback)` |
| `remove` | method | `modules/listener_manager.py:242` | `def remove(self, listener_id)` |
| `set_payload` | method | `modules/listener_manager.py:187` | `def set_payload(self, payload)` |
| `start` | method | `modules/listener_manager.py:255` | `def start(self, listener_id)` |
| `start_all` | method | `modules/listener_manager.py:348` | `def start_all(self)` |
| `status` | method | `modules/listener_manager.py:359` | `def status(self)` |
| `stop` | method | `modules/listener_manager.py:327` | `def stop(self, listener_id)` |
| `stop_all` | method | `modules/listener_manager.py:354` | `def stop_all(self)` |
| `to_dict` | method | `modules/listener_manager.py:152` | `def to_dict(self)` |
| `_emit_edge` | function | `modules/live_surface.py:126` | `def _emit_edge(source, target, relation, weight)` |
| `_emit_node` | function | `modules/live_surface.py:106` | `def _emit_node(node_id, state, title)` |
| `_group_for` | function | `modules/live_surface.py:55` | `def _group_for(node_id)` |
| `_is_compromised` | function | `modules/live_surface.py:45` | `def _is_compromised(state)` |
| `_label_for` | function | `modules/live_surface.py:64` | `def _label_for(node_id)` |
| `_node_value` | function | `modules/live_surface.py:50` | `def _node_value(centrality)` |
| `build_live_graph` | function | `modules/live_surface.py:72` | `def build_live_graph(world)` |
| `_complete` | function | `modules/llm_adapter.py:82` | `def _complete(client, full_prompt, model)` |
| `_configure_logging` | function | `modules/llm_adapter.py:65` | `def _configure_logging(debug)` |
| `_process` | function | `modules/llm_adapter.py:96` | `def _process(client, prompt, debug, template, config)` |
| `_read_error` | function | `modules/llm_adapter.py:78` | `def _read_error(prompt)` |
| `_read_prompt_file` | function | `modules/llm_adapter.py:70` | `def _read_prompt_file(prompt)` |
| `ask_general` | function | `modules/llm_adapter.py:256` | `def ask_general(prompt, debug)` |
| `process_prompt` | function | `modules/llm_adapter.py:121` | `def process_prompt(client, prompt, debug)` |
| `process_prompt_adversary` | function | `modules/llm_adapter.py:149` | `def process_prompt_adversary(client, prompt, debug)` |
| `process_prompt_general` | function | `modules/llm_adapter.py:163` | `def process_prompt_general(client, prompt, debug)` |
| `process_prompt_redop` | function | `modules/llm_adapter.py:239` | `def process_prompt_redop(client, prompt, debug)` |
| `process_prompt_script` | function | `modules/llm_adapter.py:135` | `def process_prompt_script(client, prompt, debug)` |
| `process_prompt_search` | function | `modules/llm_adapter.py:177` | `def process_prompt_search(client, prompt, debug)` |
| `process_prompt_task` | function | `modules/llm_adapter.py:191` | `def process_prompt_task(client, prompt, debug)` |
| `process_prompt_vuln` | function | `modules/llm_adapter.py:208` | `def process_prompt_vuln(client, prompt, debug, event)` |
| `safe_groq_client` | function | `modules/llm_adapter.py:48` | `def safe_groq_client(api_key)` |
| `LLMClient` | class | `modules/llm_client.py:45` | `class LLMClient` |
| `__init__` | method | `modules/llm_client.py:63` | `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)` |
| `_ask_groq` | method | `modules/llm_client.py:174` | `def _ask_groq(self, prompt, model, system, temperature)` |
| `_ask_ollama` | method | `modules/llm_client.py:213` | `def _ask_ollama(self, prompt, model)` |
| `ask` | method | `modules/llm_client.py:79` | `def ask(self, prompt)` |
| `ask` | method | `modules/llm_client.py:247` | `def ask(prompt)` |
| `classify` | method | `modules/llm_client.py:125` | `def classify(self, output)` |
| `classify` | method | `modules/llm_client.py:259` | `def classify(output)` |
| `get_client` | method | `modules/llm_client.py:239` | `def get_client(api_key)` |
| `summarize` | method | `modules/llm_client.py:154` | `def summarize(self, text)` |
| `summarize` | method | `modules/llm_client.py:264` | `def summarize(text)` |
| `DecisionRecord` | class | `modules/llm_evaluator.py:21` | `class DecisionRecord` |
| `JSONLRecorder` | class | `modules/llm_evaluator.py:75` | `class JSONLRecorder(OutcomeRecorder)` |
| `LLMEvaluator` | class | `modules/llm_evaluator.py:161` | `class LLMEvaluator` |
| `OutcomeRecorder` | class | `modules/llm_evaluator.py:55` | `class OutcomeRecorder(ABC)` |
| `QualityMetrics` | class | `modules/llm_evaluator.py:140` | `class QualityMetrics` |
| `__init__` | method | `modules/llm_evaluator.py:76` | `def __init__(self, path)` |
| `__init__` | method | `modules/llm_evaluator.py:162` | `def __init__(self, recorder)` |
| `_cli` | method | `modules/llm_evaluator.py:324` | `def _cli()` |
| `_new_id` | method | `modules/llm_evaluator.py:35` | `def _new_id()` |
| `_record_from_dict` | method | `modules/llm_evaluator.py:39` | `def _record_from_dict(d)` |
| `_safe_mean` | method | `modules/llm_evaluator.py:150` | `def _safe_mean(values)` |
| `_tactic_success_rates` | method | `modules/llm_evaluator.py:154` | `def _tactic_success_rates(records)` |
| `compute_metrics` | method | `modules/llm_evaluator.py:200` | `def compute_metrics(self, session_id)` |
| `export_finetuning_dataset` | method | `modules/llm_evaluator.py:256` | `def export_finetuning_dataset(self, path)` |
| `get_evaluator` | method | `modules/llm_evaluator.py:293` | `def get_evaluator()` |
| `load_all` | method | `modules/llm_evaluator.py:69` | `def load_all(self)` |
| `load_all` | method | `modules/llm_evaluator.py:120` | `def load_all(self)` |
| `load_by_session` | method | `modules/llm_evaluator.py:72` | `def load_by_session(self, session_id)` |
| `load_by_session` | method | `modules/llm_evaluator.py:135` | `def load_by_session(self, session_id)` |
| `quality_report` | method | `modules/llm_evaluator.py:241` | `def quality_report(self, session_id)` |
| `record` | method | `modules/llm_evaluator.py:57` | `def record(self, decision)` |
| `record` | method | `modules/llm_evaluator.py:81` | `def record(self, decision)` |
| `record_decision` | method | `modules/llm_evaluator.py:165` | `def record_decision(self, session_id, thought, action, mitre_tactic, expected_outcome, confidence)` |
| `record_decision` | method | `modules/llm_evaluator.py:302` | `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)` |
| `record_outcome` | method | `modules/llm_evaluator.py:191` | `def record_outcome(self, decision_id, actual_outcome, findings_count, success)` |
| `record_outcome` | method | `modules/llm_evaluator.py:315` | `def record_outcome(decision_id, actual_outcome, findings_count, success)` |
| `update_outcome` | method | `modules/llm_evaluator.py:60` | `def update_outcome(self, decision_id, actual, findings_count, success)` |
| `update_outcome` | method | `modules/llm_evaluator.py:86` | `def update_outcome(self, decision_id, actual, findings_count, success)` |
| `LLMBackendNotSupportedError` | class | `modules/llm_factory.py:119` | `class LLMBackendNotSupportedError(ValueError)` |
| `LLMBackendUnavailableError` | class | `modules/llm_factory.py:115` | `class LLMBackendUnavailableError(RuntimeError)` |
| `_build_anthropic` | method | `modules/llm_factory.py:390` | `def _build_anthropic(config)` |
| `_build_backend` | method | `modules/llm_factory.py:551` | `def _build_backend(normalized, resolved_config)` |
| `_build_deepseek` | method | `modules/llm_factory.py:412` | `def _build_deepseek(config)` |
| `_build_groq` | method | `modules/llm_factory.py:332` | `def _build_groq(config)` |
| `_build_ollama` | method | `modules/llm_factory.py:354` | `def _build_ollama(config)` |
| `_build_openai` | method | `modules/llm_factory.py:368` | `def _build_openai(config)` |
| `_normalize_backend` | method | `modules/llm_factory.py:308` | `def _normalize_backend(backend)` |
| `_resolve_api_key` | method | `modules/llm_factory.py:254` | `def _resolve_api_key(config)` |
| `_resolve_api_key_for_backend` | method | `modules/llm_factory.py:277` | `def _resolve_api_key_for_backend(backend, config)` |
| `_resolve_model_identifier` | method | `modules/llm_factory.py:434` | `def _resolve_model_identifier(backend_identifier, config)` |

Next: [SYMBOLS_p14.md](SYMBOLS_p14.md)
