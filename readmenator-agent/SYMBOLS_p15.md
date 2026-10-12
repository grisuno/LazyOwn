# Symbols (page 15 of 40)
Previous: [SYMBOLS_p14.md](SYMBOLS_p14.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `verify` | method | `modules/lazy_loop.py:5798` | `def verify(self)` |
| `wait` | method | `modules/lazy_loop.py:2245` | `def wait(self, item_id, timeout_sec)` |
| `wake_task` | function | `modules/lazy_loop.py:300` | `def wake_task(task_id)` |
| `InvalidCursor` | class | `modules/lazy_mentions.py:52` | `class InvalidCursor(ValueError)` |
| `LazyMention` | class | `modules/lazy_mentions.py:35` | `class LazyMention` |
| `LazyMentionPage` | class | `modules/lazy_mentions.py:45` | `class LazyMentionPage` |
| `_asset_hits` | function | `modules/lazy_mentions.py:167` | `def _asset_hits(kind, query)` |
| `_collect_candidates` | function | `modules/lazy_mentions.py:91` | `def _collect_candidates(kind, query)` |
| `_company_hits` | function | `modules/lazy_mentions.py:142` | `def _company_hits(query)` |
| `_decode_cursor` | function | `modules/lazy_mentions.py:64` | `def _decode_cursor(cursor, scope, query)` |
| `_encode_cursor` | function | `modules/lazy_mentions.py:56` | `def _encode_cursor(last_id, last_kind, exact, scope, query)` |
| `_finding_hits` | function | `modules/lazy_mentions.py:108` | `def _finding_hits(query)` |
| `_literal_match` | function | `modules/lazy_mentions.py:84` | `def _literal_match(haystack, query)` |
| `_load_snapshot` | function | `modules/lazy_mentions.py:296` | `def _load_snapshot(kind, ref_id)` |
| `_store_glob` | function | `modules/lazy_mentions.py:186` | `def _store_glob(pattern)` |
| `compose_message` | function | `modules/lazy_mentions.py:268` | `def compose_message(message)` |
| `parse_mentions` | function | `modules/lazy_mentions.py:237` | `def parse_mentions(message)` |
| `search_mentions_page` | function | `modules/lazy_mentions.py:193` | `def search_mentions_page(kind, query, cursor)` |
| `CertificateAuthority` | class | `modules/lazy_proxy.py:245` | `class CertificateAuthority` |
| `ProxyController` | class | `modules/lazy_proxy.py:421` | `class ProxyController` |
| `ProxyHandler` | class | `modules/lazy_proxy.py:533` | `class ProxyHandler(BaseHTTPRequestHandler)` |
| `RecorderServer` | class | `modules/lazy_proxy.py:393` | `class RecorderServer(ThreadingHTTPServer)` |
| `__init__` | method | `modules/lazy_proxy.py:248` | `def __init__(self, pki_dir)` |
| `__init__` | method | `modules/lazy_proxy.py:397` | `def __init__(self, address, handler)` |
| `__init__` | method | `modules/lazy_proxy.py:424` | `def __init__(self)` |
| `_cert_stem` | function | `modules/lazy_proxy.py:107` | `def _cert_stem(host)` |
| `_default_traffic_dir` | function | `modules/lazy_proxy.py:74` | `def _default_traffic_dir()` |
| `_ensure_ca` | method | `modules/lazy_proxy.py:260` | `def _ensure_ca(self)` |
| `_forward_plain` | method | `modules/lazy_proxy.py:601` | `def _forward_plain(self)` |
| `_handle_websocket` | method | `modules/lazy_proxy.py:744` | `def _handle_websocket(self, scheme, host, port, path, url, req_headers)` |
| `_make_handler` | function | `modules/lazy_proxy.py:529` | `def _make_handler()` |
| `_maybe_tls` | method | `modules/lazy_proxy.py:724` | `def _maybe_tls(sock, scheme, host)` |
| `_open_target` | method | `modules/lazy_proxy.py:704` | `def _open_target(self, scheme, host, port)` |
| `_parse_upstream` | function | `modules/lazy_proxy.py:79` | `def _parse_upstream(spec)` |
| `_read_headers_from` | method | `modules/lazy_proxy.py:734` | `def _read_headers_from(sock, limit)` |
| `_record` | method | `modules/lazy_proxy.py:829` | `def _record(self, scheme, host, port, url, status, req_headers, resp_headers, req_body, resp_body, content_type, error)` |
| `_relay` | method | `modules/lazy_proxy.py:663` | `def _relay(self, scheme, host, port, path, url, headers, body)` |
| `_run_root` | function | `modules/lazy_proxy.py:132` | `def _run_root(argv)` |
| `_safe_send_error` | method | `modules/lazy_proxy.py:583` | `def _safe_send_error(self, code, message)` |
| `_server_class` | function | `modules/lazy_proxy.py:389` | `def _server_class()` |
| `_sha256` | function | `modules/lazy_proxy.py:382` | `def _sha256()` |
| `_upstream_auth_header` | function | `modules/lazy_proxy.py:97` | `def _upstream_auth_header(auth)` |
| `_utc` | function | `modules/lazy_proxy.py:375` | `def _utc(timestamp)` |
| `_write_leaf` | method | `modules/lazy_proxy.py:315` | `def _write_leaf(self, host, cert_path, key_path)` |
| `apply_env` | function | `modules/lazy_proxy.py:896` | `def apply_env(ca_path, host, port)` |
| `ca_path` | method | `modules/lazy_proxy.py:524` | `def ca_path(self)` |
| `ca_trusted` | function | `modules/lazy_proxy.py:120` | `def ca_trusted(ca_path)` |
| `context_for` | method | `modules/lazy_proxy.py:358` | `def context_for(self, host)` |
| `detect_nss_profiles` | function | `modules/lazy_proxy.py:139` | `def detect_nss_profiles()` |
| `detect_trust_target` | function | `modules/lazy_proxy.py:112` | `def detect_trust_target()` |
| `do_CONNECT` | method | `modules/lazy_proxy.py:543` | `def do_CONNECT(self)` |
| `do_GET` | method | `modules/lazy_proxy.py:590` | `def do_GET(self)` |
| `env_for_ca` | function | `modules/lazy_proxy.py:880` | `def env_for_ca(ca_path, host, port)` |
| `get_proxy` | function | `modules/lazy_proxy.py:871` | `def get_proxy()` |
| `handle_error` | method | `modules/lazy_proxy.py:404` | `def handle_error(self, request, client_address)` |
| `install_ca_nss` | function | `modules/lazy_proxy.py:154` | `def install_ca_nss(ca_path, runner, profiles)` |
| `install_ca_trust` | function | `modules/lazy_proxy.py:194` | `def install_ca_trust(ca_path, runner)` |
| `log_message` | method | `modules/lazy_proxy.py:539` | `def log_message(self, fmt)` |
| `recorder` | method | `modules/lazy_proxy.py:520` | `def recorder(self)` |
| `restore_env` | function | `modules/lazy_proxy.py:903` | `def restore_env(previous)` |
| `start` | method | `modules/lazy_proxy.py:437` | `def start(self, host, port, task_id, traffic_dir, upstream)` |
| `status` | method | `modules/lazy_proxy.py:498` | `def status(self)` |
| `stop` | method | `modules/lazy_proxy.py:482` | `def stop(self)` |
| `Permission` | class | `modules/lazy_rbac.py:66` | `class Permission(Enum)` |
| `RBACStore` | class | `modules/lazy_rbac.py:210` | `class RBACStore` |
| `RBACUser` | class | `modules/lazy_rbac.py:124` | `class RBACUser` |
| `Role` | class | `modules/lazy_rbac.py:55` | `class Role(Enum)` |
| `TenantConfig` | class | `modules/lazy_rbac.py:368` | `class TenantConfig` |
| `TenantManager` | class | `modules/lazy_rbac.py:394` | `class TenantManager` |
| `_UsersFileUnreadable` | class | `modules/lazy_rbac.py:115` | `class _UsersFileUnreadable(Exception)` |
| `__init__` | method | `modules/lazy_rbac.py:213` | `def __init__(self, users_path)` |
| `__init__` | method | `modules/lazy_rbac.py:397` | `def __init__(self, payloads_dir, config_path, default_payload)` |
| `_bits_to_bytes` | function | `modules/lazy_rbac.py:903` | `def _bits_to_bytes(bits, data_bits)` |
| `_generate_recovery_codes` | function | `modules/lazy_rbac.py:356` | `def _generate_recovery_codes(count)` |
| `_get_rbac_store` | function | `modules/lazy_rbac.py:632` | `def _get_rbac_store()` |
| `_get_rbac_user` | function | `modules/lazy_rbac.py:619` | `def _get_rbac_user(flask_user)` |
| `_load_config` | method | `modules/lazy_rbac.py:410` | `def _load_config(self)` |
| `_qr_add_format_info` | function | `modules/lazy_rbac.py:836` | `def _qr_add_format_info(modules, size, ecl_bits, mask)` |
| `_qr_apply_mask` | function | `modules/lazy_rbac.py:963` | `def _qr_apply_mask(modules, size, mask)` |
| `_qr_best_mask` | function | `modules/lazy_rbac.py:950` | `def _qr_best_mask(modules, size)` |
| `_qr_blank_matrix` | function | `modules/lazy_rbac.py:823` | `def _qr_blank_matrix(version)` |
| `_qr_choose_version` | function | `modules/lazy_rbac.py:744` | `def _qr_choose_version(data)` |
| `_qr_data_bits_for_version` | function | `modules/lazy_rbac.py:812` | `def _qr_data_bits_for_version(version)` |
| `_qr_data_bits_positions` | function | `modules/lazy_rbac.py:884` | `def _qr_data_bits_positions(matrix, size)` |
| `_qr_ec_codewords` | function | `modules/lazy_rbac.py:752` | `def _qr_ec_codewords(version)` |
| `_qr_encode_alphanumeric` | function | `modules/lazy_rbac.py:757` | `def _qr_encode_alphanumeric(data, version)` |
| `_qr_penalty` | function | `modules/lazy_rbac.py:996` | `def _qr_penalty(modules, size)` |
| `_qr_place_dark_module` | function | `modules/lazy_rbac.py:832` | `def _qr_place_dark_module(matrix, size, version)` |
| `_qr_place_finders` | function | `modules/lazy_rbac.py:869` | `def _qr_place_finders(matrix, size)` |
| `_qr_place_timing` | function | `modules/lazy_rbac.py:878` | `def _qr_place_timing(matrix, size)` |
| `_qr_render_svg` | function | `modules/lazy_rbac.py:1058` | `def _qr_render_svg(modules, size, modules_per_pixel)` |
| `_qr_svg_error` | function | `modules/lazy_rbac.py:860` | `def _qr_svg_error(msg)` |
| `_read_users` | method | `modules/lazy_rbac.py:217` | `def _read_users(self)` |
| `_reed_solomon_encode` | function | `modules/lazy_rbac.py:914` | `def _reed_solomon_encode(data, ec_words)` |
| `_save_config` | method | `modules/lazy_rbac.py:421` | `def _save_config(self)` |
| `_slugify` | function | `modules/lazy_rbac.py:514` | `def _slugify(name)` |
| `_write_users` | method | `modules/lazy_rbac.py:232` | `def _write_users(self, users)` |
| `can_manage_role` | method | `modules/lazy_rbac.py:174` | `def can_manage_role(self, target_role)` |
| `check_cli_permission` | function | `modules/lazy_rbac.py:660` | `def check_cli_permission(username, permission)` |
| `consume_recovery_code` | method | `modules/lazy_rbac.py:200` | `def consume_recovery_code(self, code)` |
| `consume_recovery_code` | method | `modules/lazy_rbac.py:334` | `def consume_recovery_code(self, user_id, code)` |
| `create_tenant` | method | `modules/lazy_rbac.py:457` | `def create_tenant(self, name, base_payload)` |
| `create_user` | method | `modules/lazy_rbac.py:274` | `def create_user(self, username, password_hash, role, tenant_id)` |
| `decorated` | function | `modules/lazy_rbac.py:544` | `def decorated()` |
| `decorated` | function | `modules/lazy_rbac.py:570` | `def decorated()` |
| `decorated` | function | `modules/lazy_rbac.py:600` | `def decorated()` |
| `decorator` | function | `modules/lazy_rbac.py:542` | `def decorator(f)` |
| `decorator` | function | `modules/lazy_rbac.py:568` | `def decorator(f)` |
| `delete_tenant` | method | `modules/lazy_rbac.py:495` | `def delete_tenant(self, tenant_id)` |
| `delete_user` | method | `modules/lazy_rbac.py:295` | `def delete_user(self, user_id)` |
| `disable_mfa` | method | `modules/lazy_rbac.py:324` | `def disable_mfa(self, user_id)` |
| `enable_mfa` | method | `modules/lazy_rbac.py:314` | `def enable_mfa(self, user_id)` |
| `ensure_admin` | method | `modules/lazy_rbac.py:343` | `def ensure_admin(self, username, password_hash)` |
| `ensure_default_tenant` | method | `modules/lazy_rbac.py:504` | `def ensure_default_tenant(self)` |
| `find_by_id` | method | `modules/lazy_rbac.py:249` | `def find_by_id(self, user_id)` |
| `find_by_username` | method | `modules/lazy_rbac.py:255` | `def find_by_username(self, username)` |
| `from_dict` | method | `modules/lazy_rbac.py:140` | `def from_dict(cls, data)` |
| `from_dict` | method | `modules/lazy_rbac.py:390` | `def from_dict(cls, data)` |
| `from_payload` | method | `modules/lazy_rbac.py:377` | `def from_payload(cls, tenant_id, name, payload_path)` |
| `generate_mfa_qr_url` | function | `modules/lazy_rbac.py:680` | `def generate_mfa_qr_url(secret, username)` |
| `generate_qr_svg` | function | `modules/lazy_rbac.py:689` | `def generate_qr_svg(data)` |
| `get_active` | method | `modules/lazy_rbac.py:434` | `def get_active(self)` |
| `get_active_payload_path` | method | `modules/lazy_rbac.py:439` | `def get_active_payload_path(self)` |
| `get_active_sessions_dir` | method | `modules/lazy_rbac.py:445` | `def get_active_sessions_dir(self)` |
| `get_mfa_provisioning_uri` | method | `modules/lazy_rbac.py:182` | `def get_mfa_provisioning_uri(self)` |
| `get_payload_for_tenant` | method | `modules/lazy_rbac.py:451` | `def get_payload_for_tenant(self, tenant_id)` |
| `get_rbac_store` | function | `modules/lazy_rbac.py:639` | `def get_rbac_store()` |
| `get_role` | method | `modules/lazy_rbac.py:164` | `def get_role(self)` |
| `get_tenant_manager` | function | `modules/lazy_rbac.py:648` | `def get_tenant_manager()` |
| `get_user_role` | function | `modules/lazy_rbac.py:672` | `def get_user_role(username)` |
| `gf_mul` | function | `modules/lazy_rbac.py:927` | `def gf_mul(a, b)` |
| `has_permission` | method | `modules/lazy_rbac.py:170` | `def has_permission(self, permission)` |
| `init_rbac_store` | function | `modules/lazy_rbac.py:523` | `def init_rbac_store(users_path)` |
| `init_tenant_manager` | function | `modules/lazy_rbac.py:527` | `def init_tenant_manager(payloads_dir, config_path, default_payload)` |
| `list_tenants` | method | `modules/lazy_rbac.py:431` | `def list_tenants(self)` |
| `load_all` | method | `modules/lazy_rbac.py:245` | `def load_all(self)` |
| `require_mfa` | function | `modules/lazy_rbac.py:596` | `def require_mfa(f)` |
| `require_permission` | function | `modules/lazy_rbac.py:565` | `def require_permission()` |
| `require_role` | function | `modules/lazy_rbac.py:539` | `def require_role()` |
| `save` | method | `modules/lazy_rbac.py:261` | `def save(self, user)` |
| `set_rbac_store` | function | `modules/lazy_rbac.py:643` | `def set_rbac_store(store)` |
| `set_tenant_manager` | function | `modules/lazy_rbac.py:655` | `def set_tenant_manager(tm)` |
| `switch_tenant` | method | `modules/lazy_rbac.py:486` | `def switch_tenant(self, tenant_id)` |
| `to_dict` | method | `modules/lazy_rbac.py:136` | `def to_dict(self)` |
| `to_dict` | method | `modules/lazy_rbac.py:386` | `def to_dict(self)` |
| `update_role` | method | `modules/lazy_rbac.py:304` | `def update_role(self, user_id, new_role)` |
| `valid_roles` | method | `modules/lazy_rbac.py:62` | `def valid_roles(cls)` |
| `verify_recovery_code` | method | `modules/lazy_rbac.py:192` | `def verify_recovery_code(self, code)` |
| `verify_totp` | method | `modules/lazy_rbac.py:187` | `def verify_totp(self, token)` |
| `LoopRunConfig` | class | `modules/lazy_runner.py:90` | `class LoopRunConfig` |
| `ThreadStdoutRouter` | class | `modules/lazy_runner.py:41` | `class ThreadStdoutRouter(TextIOBase)` |
| `__init__` | method | `modules/lazy_runner.py:51` | `def __init__(self, main_stream, spool)` |
| `_abort_run` | function | `modules/lazy_runner.py:271` | `def _abort_run(engine, task_id, reason)` |
| `_bootstrap` | function | `modules/lazy_runner.py:353` | `def _bootstrap(scan_target, executor)` |
| `_dump_thread_stacks` | function | `modules/lazy_runner.py:484` | `def _dump_thread_stacks()` |
| `_executor` | function | `modules/lazy_runner.py:233` | `def _executor(command)` |
| `_format_activity` | function | `modules/lazy_runner.py:470` | `def _format_activity(record)` |
| `_overview` | function | `modules/lazy_runner.py:460` | `def _overview(task_id)` |
| `_poll_progress` | function | `modules/lazy_runner.py:499` | `def _poll_progress(engine, config, progress, transcript, worker)` |
| `_prepare_engine` | function | `modules/lazy_runner.py:290` | `def _prepare_engine(engine, shell, config, params)` |
| `_resolve_alias` | function | `modules/lazy_runner.py:225` | `def _resolve_alias(command)` |
| `_run` | function | `modules/lazy_runner.py:406` | `def _run()` |
| `_run_plain` | function | `modules/lazy_runner.py:616` | `def _run_plain(engine, config)` |
| `_run_with_progress` | function | `modules/lazy_runner.py:367` | `def _run_with_progress(engine, config)` |
| `_start_proxy` | function | `modules/lazy_runner.py:304` | `def _start_proxy(engine, params)` |
| `_terminal_stream` | function | `modules/lazy_runner.py:594` | `def _terminal_stream()` |
| `_to_float` | function | `modules/lazy_runner.py:128` | `def _to_float(raw, default)` |
| `_to_int` | function | `modules/lazy_runner.py:120` | `def _to_int(raw, default)` |
| `_tty_available` | function | `modules/lazy_runner.py:722` | `def _tty_available()` |
| `_write` | function | `modules/lazy_runner.py:606` | `def _write(text)` |
| `build_executor` | function | `modules/lazy_runner.py:213` | `def build_executor(shell, config, stream, cancelled)` |
| `clamped` | method | `modules/lazy_runner.py:106` | `def clamped(self)` |
| `encoding` | method | `modules/lazy_runner.py:76` | `def encoding(self)` |
| `flush` | method | `modules/lazy_runner.py:68` | `def flush(self)` |
| `isatty` | method | `modules/lazy_runner.py:80` | `def isatty(self)` |
| `parse_loop_line` | function | `modules/lazy_runner.py:136` | `def parse_loop_line(line)` |
| `report_result` | function | `modules/lazy_runner.py:329` | `def report_result(result)` |
| `run_loop` | function | `modules/lazy_runner.py:640` | `def run_loop(shell, params, config)` |
| `stream` | function | `modules/lazy_runner.py:382` | `def stream(text)` |
| `write` | method | `modules/lazy_runner.py:57` | `def write(self, data)` |
| `_frontmatter` | function | `modules/lazy_skills.py:28` | `def _frontmatter(text)` |
| `_load` | function | `modules/lazy_skills.py:53` | `def _load(path)` |
| `_skill_files` | function | `modules/lazy_skills.py:42` | `def _skill_files()` |
| `get_skill` | function | `modules/lazy_skills.py:91` | `def get_skill(name)` |
| `list_skills` | function | `modules/lazy_skills.py:85` | `def list_skills()` |
| `match_skills` | function | `modules/lazy_skills.py:102` | `def match_skills(text, limit)` |
| `skills_context` | function | `modules/lazy_skills.py:118` | `def skills_context(text, explicit, auto, budget)` |
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
| `CloudBucketEnumerator` | class | `modules/lazycloud.py:248` | `class CloudBucketEnumerator` |
| `CloudFinding` | class | `modules/lazycloud.py:98` | `class CloudFinding` |
| `CloudIAMEnumerator` | class | `modules/lazycloud.py:342` | `class CloudIAMEnumerator` |
| `CloudMetadataHarvester` | class | `modules/lazycloud.py:108` | `class CloudMetadataHarvester` |
| `CloudResource` | class | `modules/lazycloud.py:87` | `class CloudResource` |
| `CloudScanner` | class | `modules/lazycloud.py:390` | `class CloudScanner` |
| `__init__` | method | `modules/lazycloud.py:111` | `def __init__(self, timeout)` |
| `__init__` | method | `modules/lazycloud.py:251` | `def __init__(self, timeout)` |
| `__init__` | method | `modules/lazycloud.py:393` | `def __init__(self, target_domain, timeout)` |
| `_aws_sig` | function | `modules/lazycloud.py:361` | `def _aws_sig(key, msg)` |
| `_check_url` | method | `modules/lazycloud.py:262` | `def _check_url(self, url)` |
| `_get` | method | `modules/lazycloud.py:122` | `def _get(self, url, headers)` |
| `_sign` | function | `modules/lazycloud.py:364` | `def _sign(key, msg)` |
| `enumerate_aws_iam` | method | `modules/lazycloud.py:345` | `def enumerate_aws_iam(self, access_key, secret_key, session_token)` |
| `enumerate_azure_storage` | method | `modules/lazycloud.py:303` | `def enumerate_azure_storage(self, prefix, accounts)` |
| `enumerate_gcp_storage` | method | `modules/lazycloud.py:321` | `def enumerate_gcp_storage(self, prefix, buckets)` |
| `enumerate_s3` | method | `modules/lazycloud.py:278` | `def enumerate_s3(self, prefix, buckets)` |
| `full_scan` | method | `modules/lazycloud.py:400` | `def full_scan(self, target_prefix, sessions_dir)` |
| `harvest_all` | method | `modules/lazycloud.py:231` | `def harvest_all(self)` |
| `harvest_aws` | method | `modules/lazycloud.py:139` | `def harvest_aws(self)` |
| `harvest_azure` | method | `modules/lazycloud.py:184` | `def harvest_azure(self)` |
| `harvest_gcp` | method | `modules/lazycloud.py:208` | `def harvest_gcp(self)` |
| `quick_buckets` | method | `modules/lazycloud.py:460` | `def quick_buckets(self, prefix)` |
| `quick_metadata` | method | `modules/lazycloud.py:456` | `def quick_metadata(self)` |
| `session` | method | `modules/lazycloud.py:116` | `def session(self)` |
| `session` | method | `modules/lazycloud.py:256` | `def session(self)` |
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
| `ContainerEscapeTechniques` | class | `modules/lazyk8s.py:624` | `class ContainerEscapeTechniques` |
| `ContainerFinding` | class | `modules/lazyk8s.py:30` | `class ContainerFinding` |
| `ContainerResource` | class | `modules/lazyk8s.py:20` | `class ContainerResource` |
| `ContainerRuntimeDetector` | class | `modules/lazyk8s.py:759` | `class ContainerRuntimeDetector` |
| `DockerEnumerator` | class | `modules/lazyk8s.py:41` | `class DockerEnumerator` |
| `K8sEnumerator` | class | `modules/lazyk8s.py:264` | `class K8sEnumerator` |
| `__init__` | method | `modules/lazyk8s.py:44` | `def __init__(self, socket_path)` |
| `__init__` | method | `modules/lazyk8s.py:267` | `def __init__(self, kubeconfig, token, api_server)` |
| `_docker_api` | method | `modules/lazyk8s.py:51` | `def _docker_api(self, endpoint)` |
| `_get_k8s_api` | method | `modules/lazyk8s.py:285` | `def _get_k8s_api(self, path)` |
| `_load_kubeconfig` | method | `modules/lazyk8s.py:274` | `def _load_kubeconfig(self)` |
| `auto_detect_all` | method | `modules/lazyk8s.py:992` | `def auto_detect_all()` |
| `check_capabilities` | method | `modules/lazyk8s.py:217` | `def check_capabilities(self)` |
| `check_docker_socket_mount` | method | `modules/lazyk8s.py:196` | `def check_docker_socket_mount(self)` |
| `check_pod_escape_vectors` | method | `modules/lazyk8s.py:530` | `def check_pod_escape_vectors(self)` |
| `check_privileged_containers` | method | `modules/lazyk8s.py:137` | `def check_privileged_containers(self)` |
| `check_rbac` | method | `modules/lazyk8s.py:498` | `def check_rbac(self)` |
| `check_sensitive_mounts` | method | `modules/lazyk8s.py:162` | `def check_sensitive_mounts(self)` |
| `detect_current_environment` | method | `modules/lazyk8s.py:684` | `def detect_current_environment()` |
| `detect_dangerous_capabilities` | method | `modules/lazyk8s.py:921` | `def detect_dangerous_capabilities()` |
| `detect_mounts` | method | `modules/lazyk8s.py:874` | `def detect_mounts()` |
| `detect_runtime` | method | `modules/lazyk8s.py:803` | `def detect_runtime()` |
| `full_check` | method | `modules/lazyk8s.py:250` | `def full_check(self)` |
| `full_check` | method | `modules/lazyk8s.py:582` | `def full_check(self, sessions_dir)` |
| `inspect_container` | method | `modules/lazyk8s.py:118` | `def inspect_container(self, container_id)` |
| `is_socket_accessible` | method | `modules/lazyk8s.py:47` | `def is_socket_accessible(self)` |
| `list_containers` | method | `modules/lazyk8s.py:70` | `def list_containers(self)` |
| `list_images` | method | `modules/lazyk8s.py:94` | `def list_images(self)` |
| `list_namespaces` | method | `modules/lazyk8s.py:390` | `def list_namespaces(self)` |
| `list_pods` | method | `modules/lazyk8s.py:366` | `def list_pods(self, namespace)` |
| `list_secrets` | method | `modules/lazyk8s.py:410` | `def list_secrets(self, namespace)` |
| `list_service_accounts` | method | `modules/lazyk8s.py:462` | `def list_service_accounts(self, namespace)` |
| `check_sudo` | function | `modules/lazylynis.sh:32` | `` |
| `ctrl_c` | function | `modules/lazymasscan.sh:20` | `` |
| `extract_ports_info` | function | `modules/lazymasscan.sh:74` | `` |
| `print_row` | function | `modules/lazymasscan.sh:117` | `` |
| `run_masscan_script` | function | `modules/lazymasscan.sh:94` | `` |
| `cleanup` | function | `modules/lazynmap.sh:29` | `` |
| `ctrl_c` | function | `modules/lazynmap.sh:38` | `` |
| `discover_network` | function | `modules/lazynmap.sh:149` | `` |
| `extract_ports_info` | function | `modules/lazynmap.sh:818` | `` |
| `fix_sessions_owner` | function | `modules/lazynmap.sh:74` | `` |
| `nmaptest` | function | `modules/lazynmap.sh:129` | `` |
| `print_row` | function | `modules/lazynmap.sh:877` | `` |
| `run_nmap_script` | function | `modules/lazynmap.sh:844` | `` |
| `ProxyHandler` | class | `modules/lazyown_bprfuzzer.py:114` | `class ProxyHandler(BaseHTTPRequestHandler)` |
| `_handle_request` | method | `modules/lazyown_bprfuzzer.py:121` | `def _handle_request(self, method)` |
| `_load_security_config` | function | `modules/lazyown_bprfuzzer.py:45` | `def _load_security_config()` |
| `do_GET` | method | `modules/lazyown_bprfuzzer.py:115` | `def do_GET(self)` |
| `do_POST` | method | `modules/lazyown_bprfuzzer.py:118` | `def do_POST(self)` |
| `edit_file_with_nano` | function | `modules/lazyown_bprfuzzer.py:169` | `def edit_file_with_nano(content)` |
| `lazyfuzz` | function | `modules/lazyown_bprfuzzer.py:233` | `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)` |
| `load_data_from_file` | function | `modules/lazyown_bprfuzzer.py:99` | `def load_data_from_file(file_path)` |
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
| `decrypt` | function | `modules/lazyownclient.py:62` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `modules/lazyownclient.py:55` | `def encrypt(plaintext, key)` |
| `handle_command` | function | `modules/lazyownclient.py:69` | `def handle_command(cmd, key)` |
| `main` | function | `modules/lazyownclient.py:198` | `def main()` |
| `pad` | function | `modules/lazyownclient.py:51` | `def pad(s)` |
| `signal_handler` | function | `modules/lazyownclient.py:34` | `def signal_handler(sig, frame)` |
| `main` | function | `modules/lazyownerweb.py:59` | `def main()` |
| `send_request` | function | `modules/lazyownerweb.py:36` | `def send_request(url, params, method)` |
| `test_injection` | function | `modules/lazyownerweb.py:49` | `def test_injection(url, payloads, param_name, detection_strings, method)` |
| `decrypt` | function | `modules/lazyownserver.py:53` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `modules/lazyownserver.py:46` | `def encrypt(plaintext, key)` |
| `handle_client` | function | `modules/lazyownserver.py:60` | `def handle_client(conn, addr, key)` |
| `main` | function | `modules/lazyownserver.py:97` | `def main()` |
| `pad` | function | `modules/lazyownserver.py:42` | `def pad(s)` |
| `signal_handler` | function | `modules/lazyownserver.py:34` | `def signal_handler(sig, frame)` |
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
| `_stop` | method | `modules/listener_manager.py:331` | `def _stop(self, listener)` |
| `add` | method | `modules/listener_manager.py:229` | `def add(self, port, ssl, listener_id)` |
| `from_dict` | method | `modules/listener_manager.py:162` | `def from_dict(cls, data)` |
| `get_default_port` | method | `modules/listener_manager.py:367` | `def get_default_port(self, fallback)` |
| `remove` | method | `modules/listener_manager.py:242` | `def remove(self, listener_id)` |
| `set_payload` | method | `modules/listener_manager.py:187` | `def set_payload(self, payload)` |
| `start` | method | `modules/listener_manager.py:255` | `def start(self, listener_id)` |
| `start_all` | method | `modules/listener_manager.py:344` | `def start_all(self)` |
| `status` | method | `modules/listener_manager.py:355` | `def status(self)` |
| `stop` | method | `modules/listener_manager.py:323` | `def stop(self, listener_id)` |
| `stop_all` | method | `modules/listener_manager.py:350` | `def stop_all(self)` |
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
| `ask_general` | function | `modules/llm_adapter.py:254` | `def ask_general(prompt, debug)` |
| `process_prompt` | function | `modules/llm_adapter.py:119` | `def process_prompt(client, prompt, debug)` |
| `process_prompt_adversary` | function | `modules/llm_adapter.py:147` | `def process_prompt_adversary(client, prompt, debug)` |
| `process_prompt_general` | function | `modules/llm_adapter.py:161` | `def process_prompt_general(client, prompt, debug)` |
| `process_prompt_redop` | function | `modules/llm_adapter.py:237` | `def process_prompt_redop(client, prompt, debug)` |
| `process_prompt_script` | function | `modules/llm_adapter.py:133` | `def process_prompt_script(client, prompt, debug)` |
| `process_prompt_search` | function | `modules/llm_adapter.py:175` | `def process_prompt_search(client, prompt, debug)` |
| `process_prompt_task` | function | `modules/llm_adapter.py:189` | `def process_prompt_task(client, prompt, debug)` |
| `process_prompt_vuln` | function | `modules/llm_adapter.py:206` | `def process_prompt_vuln(client, prompt, debug, event)` |
| `safe_groq_client` | function | `modules/llm_adapter.py:48` | `def safe_groq_client(api_key)` |
| `LLMClient` | class | `modules/llm_client.py:45` | `class LLMClient` |
| `__init__` | method | `modules/llm_client.py:63` | `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)` |
| `_ask_groq` | method | `modules/llm_client.py:174` | `def _ask_groq(self, prompt, model, system, temperature)` |
| `_ask_ollama` | method | `modules/llm_client.py:215` | `def _ask_ollama(self, prompt, model)` |
| `ask` | method | `modules/llm_client.py:79` | `def ask(self, prompt)` |
| `ask` | function | `modules/llm_client.py:251` | `def ask(prompt)` |
| `classify` | method | `modules/llm_client.py:125` | `def classify(self, output)` |
| `classify` | function | `modules/llm_client.py:263` | `def classify(output)` |

Next: [SYMBOLS_p16.md](SYMBOLS_p16.md)
