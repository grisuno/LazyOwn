# Symbols (page 15 of 40)
Previous: [SYMBOLS_p14.md](SYMBOLS_p14.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `request` | method | `modules/lazy_loop.py:2343` | `def request(self, tool, command, reason, tool_use_id)` |
| `resolve_target` | function | `modules/lazy_loop.py:2850` | `def resolve_target(task_id, store, graph)` |
| `restore` | method | `modules/lazy_loop.py:7163` | `def restore(self, path)` |
| `resume` | method | `modules/lazy_loop.py:2549` | `def resume(self, task_id)` |
| `resume_intent` | method | `modules/lazy_loop.py:8010` | `def resume_intent(self, task_id, intent_id)` |
| `resume_task` | method | `modules/lazy_loop.py:7639` | `def resume_task(self, task_id)` |
| `retest` | method | `modules/lazy_loop.py:5077` | `def retest(self, finding_id, executor, note)` |
| `retest_context` | method | `modules/lazy_loop.py:5147` | `def retest_context(self, finding_id)` |
| `run` | method | `modules/lazy_loop.py:8660` | `def run(self, task_id, max_rounds, workers, executor, timeout_sec)` |
| `run_command` | function | `modules/lazy_loop.py:4162` | `def run_command(command, background)` |
| `run_round` | method | `modules/lazy_loop.py:8183` | `def run_round(self, task_id, workers, executor, pool)` |
| `save` | method | `modules/lazy_loop.py:7120` | `def save(self, task_id)` |
| `say` | method | `modules/lazy_loop.py:7313` | `def say(self, task_id, text, pool, session)` |
| `scoped` | method | `modules/lazy_loop.py:948` | `def scoped(self, scope, kind)` |
| `scrub_secrets` | function | `modules/lazy_loop.py:363` | `def scrub_secrets(text)` |
| `search` | method | `modules/lazy_loop.py:1441` | `def search(self, query, exclude_intent)` |
| `search` | method | `modules/lazy_loop.py:1499` | `def search(self, query, limit)` |
| `search_all` | method | `modules/lazy_loop.py:1411` | `def search_all(self, query, limit)` |
| `search_host` | method | `modules/lazy_loop.py:1510` | `def search_host(self, host, port, limit)` |
| `search_proxy_body` | method | `modules/lazy_loop.py:9104` | `def search_proxy_body(self, task_id, query, limit)` |
| `send_worker_message` | method | `modules/lazy_loop.py:8033` | `def send_worker_message(self, task_id, intent_id, message, request_id)` |
| `sessions` | method | `modules/lazy_loop.py:7077` | `def sessions(self, task_id)` |
| `sessions` | method | `modules/lazy_loop.py:7372` | `def sessions(self, task_id)` |
| `set` | method | `modules/lazy_loop.py:7287` | `def set(self, task_id, category)` |
| `set_concurrency` | method | `modules/lazy_loop.py:8982` | `def set_concurrency(self, limit)` |
| `set_context_budget` | method | `modules/lazy_loop.py:6954` | `def set_context_budget(self, chars)` |
| `set_deadline` | method | `modules/lazy_loop.py:2685` | `def set_deadline(self, task_id, timeout_sec)` |
| `set_goals` | method | `modules/lazy_loop.py:7777` | `def set_goals(self, task_id, specs)` |
| `set_judge` | method | `modules/lazy_loop.py:1762` | `def set_judge(self, enabled, fail_action)` |
| `set_limits` | method | `modules/lazy_loop.py:2166` | `def set_limits(self, task_id)` |
| `set_llm_chain` | method | `modules/lazy_loop.py:2602` | `def set_llm_chain(self, task_id, members, active)` |
| `set_priority` | method | `modules/lazy_loop.py:6625` | `def set_priority(self, name, priority)` |
| `set_record_raw` | method | `modules/lazy_loop.py:6916` | `def set_record_raw(self, enabled)` |
| `set_skills` | method | `modules/lazy_loop.py:2660` | `def set_skills(self, task_id, names, auto)` |
| `set_state` | method | `modules/lazy_loop.py:1083` | `def set_state(self, node_id, state)` |
| `set_status` | method | `modules/lazy_loop.py:2533` | `def set_status(self, task_id, status)` |
| `set_status` | method | `modules/lazy_loop.py:6086` | `def set_status(self, finding_id, status)` |
| `settlement_prompt` | function | `modules/lazy_loop.py:5764` | `def settlement_prompt(agent, reason)` |
| `shell_open` | function | `modules/lazy_loop.py:4235` | `def shell_open()` |
| `shell_send` | function | `modules/lazy_loop.py:4239` | `def shell_send(command)` |
| `shutdown_loop_runtime` | function | `modules/lazy_loop.py:513` | `def shutdown_loop_runtime(reason)` |
| `sink` | function | `modules/lazy_loop.py:3279` | `def sink(text)` |
| `sink` | function | `modules/lazy_loop.py:4689` | `def sink(text)` |
| `spawn_task` | method | `modules/lazy_loop.py:7550` | `def spawn_task(self, goal, source_task_ids, description)` |
| `stage_enabled` | function | `modules/lazy_loop.py:8234` | `def stage_enabled(_name)` |
| `stats` | method | `modules/lazy_loop.py:1906` | `def stats(self)` |
| `stats` | method | `modules/lazy_loop.py:7230` | `def stats(self)` |
| `status` | method | `modules/lazy_loop.py:9380` | `def status(self, task_id)` |
| `steer` | method | `modules/lazy_loop.py:2731` | `def steer(self, task_id, intent_id, message)` |
| `steer_for` | method | `modules/lazy_loop.py:2751` | `def steer_for(self, task_id, intent_id)` |
| `structural_cold` | method | `modules/lazy_loop.py:5360` | `def structural_cold(self, hot)` |
| `task_findings` | method | `modules/lazy_loop.py:7655` | `def task_findings(self, task_id)` |
| `task_graph` | method | `modules/lazy_loop.py:7649` | `def task_graph(self, task_id)` |
| `task_llm_chain` | function | `modules/lazy_loop.py:728` | `def task_llm_chain(store, task_id)` |
| `task_node_detail` | method | `modules/lazy_loop.py:7683` | `def task_node_detail(self, task_id, node_id)` |
| `task_traces` | method | `modules/lazy_loop.py:7674` | `def task_traces(self, task_id, query, limit)` |
| `templates` | method | `modules/lazy_loop.py:1605` | `def templates(self, limit)` |
| `trace` | method | `modules/lazy_loop.py:1373` | `def trace(self, intent_id, query, step_id, limit)` |
| `traffic_search` | function | `modules/lazy_loop.py:4207` | `def traffic_search(query)` |
| `unbind` | method | `modules/lazy_loop.py:7003` | `def unbind(self, agent, tool)` |
| `unfolded` | method | `modules/lazy_loop.py:5667` | `def unfolded(self, limit)` |
| `unregister_worker` | function | `modules/lazy_loop.py:507` | `def unregister_worker(worker)` |
| `untested` | method | `modules/lazy_loop.py:961` | `def untested(self, limit)` |
| `untested_for` | method | `modules/lazy_loop.py:994` | `def untested_for(self, graph, scope, limit)` |
| `update_finding_report` | method | `modules/lazy_loop.py:7689` | `def update_finding_report(self, task_id, finding_id, report)` |
| `update_report` | method | `modules/lazy_loop.py:6103` | `def update_report(self, finding_id, report)` |
| `usage` | method | `modules/lazy_loop.py:2179` | `def usage(self, task_id)` |
| `usage` | method | `modules/lazy_loop.py:6638` | `def usage(self)` |
| `verify` | method | `modules/lazy_loop.py:6161` | `def verify(self)` |
| `wait` | method | `modules/lazy_loop.py:2431` | `def wait(self, item_id, timeout_sec)` |
| `wake_task` | function | `modules/lazy_loop.py:467` | `def wake_task(task_id)` |
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
| `_dataset_path` | function | `modules/lazy_orchestrator_feedback.py:47` | `def _dataset_path()` |
| `_key` | function | `modules/lazy_orchestrator_feedback.py:228` | `def _key(line)` |
| `_load_priors` | function | `modules/lazy_orchestrator_feedback.py:144` | `def _load_priors()` |
| `_normalize` | function | `modules/lazy_orchestrator_feedback.py:129` | `def _normalize(priors)` |
| `_priors_path` | function | `modules/lazy_orchestrator_feedback.py:41` | `def _priors_path()` |
| `_reward_of` | function | `modules/lazy_orchestrator_feedback.py:53` | `def _reward_of(outcome)` |
| `adjust_from_usage` | function | `modules/lazy_orchestrator_feedback.py:61` | `def adjust_from_usage(limit)` |
| `export_dataset` | function | `modules/lazy_orchestrator_feedback.py:238` | `def export_dataset(out, limit)` |
| `order_steps` | function | `modules/lazy_orchestrator_feedback.py:213` | `def order_steps(steps, stack)` |
| `rank_verbs` | function | `modules/lazy_orchestrator_feedback.py:189` | `def rank_verbs(phase, verbs, stack)` |
| `verb_prior` | function | `modules/lazy_orchestrator_feedback.py:162` | `def verb_prior(phase, verb, stack)` |
| `CertificateAuthority` | class | `modules/lazy_proxy.py:455` | `class CertificateAuthority` |
| `ProxyController` | class | `modules/lazy_proxy.py:635` | `class ProxyController` |
| `ProxyHandler` | class | `modules/lazy_proxy.py:747` | `class ProxyHandler(BaseHTTPRequestHandler)` |
| `RecorderServer` | class | `modules/lazy_proxy.py:607` | `class RecorderServer(ThreadingHTTPServer)` |
| `__init__` | method | `modules/lazy_proxy.py:458` | `def __init__(self, pki_dir)` |
| `__init__` | method | `modules/lazy_proxy.py:611` | `def __init__(self, address, handler)` |
| `__init__` | method | `modules/lazy_proxy.py:638` | `def __init__(self)` |
| `_cert_stem` | function | `modules/lazy_proxy.py:317` | `def _cert_stem(host)` |
| `_default_traffic_dir` | function | `modules/lazy_proxy.py:284` | `def _default_traffic_dir()` |
| `_ensure_ca` | method | `modules/lazy_proxy.py:470` | `def _ensure_ca(self)` |
| `_forward_plain` | method | `modules/lazy_proxy.py:820` | `def _forward_plain(self)` |
| `_handle_websocket` | method | `modules/lazy_proxy.py:1024` | `def _handle_websocket(self, scheme, host, port, path, url, req_headers)` |
| `_host_syntax_valid` | function | `modules/lazy_proxy.py:141` | `def _host_syntax_valid(host)` |
| `_https_connection` | function | `modules/lazy_proxy.py:273` | `def _https_connection(host, port)` |
| `_is_lab_host` | function | `modules/lazy_proxy.py:261` | `def _is_lab_host(host)` |
| `_is_metadata_hostname` | function | `modules/lazy_proxy.py:129` | `def _is_metadata_hostname(host)` |
| `_is_metadata_ip` | function | `modules/lazy_proxy.py:115` | `def _is_metadata_ip(value)` |
| `_make_handler` | function | `modules/lazy_proxy.py:743` | `def _make_handler()` |
| `_maybe_tls` | method | `modules/lazy_proxy.py:994` | `def _maybe_tls(sock, scheme, host)` |
| `_open_target` | method | `modules/lazy_proxy.py:973` | `def _open_target(self, scheme, host, port)` |
| `_parse_upstream` | function | `modules/lazy_proxy.py:289` | `def _parse_upstream(spec)` |
| `_proxy_allow_private` | function | `modules/lazy_proxy.py:93` | `def _proxy_allow_private()` |
| `_proxy_insecure_tls` | function | `modules/lazy_proxy.py:105` | `def _proxy_insecure_tls()` |
| `_proxy_trust_ca` | function | `modules/lazy_proxy.py:110` | `def _proxy_trust_ca()` |
| `_read_headers_from` | method | `modules/lazy_proxy.py:1014` | `def _read_headers_from(sock, limit)` |
| `_record` | method | `modules/lazy_proxy.py:1109` | `def _record(self, scheme, host, port, url, status, req_headers, resp_headers, req_body, resp_body, content_type, error)` |
| `_relay` | method | `modules/lazy_proxy.py:894` | `def _relay(self, scheme, host, port, path, url, headers, body)` |
| `_resolved_ips` | function | `modules/lazy_proxy.py:157` | `def _resolved_ips(host)` |
| `_run_root` | function | `modules/lazy_proxy.py:342` | `def _run_root(argv)` |
| `_safe_send_error` | method | `modules/lazy_proxy.py:802` | `def _safe_send_error(self, code, message)` |
| `_server_class` | function | `modules/lazy_proxy.py:603` | `def _server_class()` |
| `_sha256` | function | `modules/lazy_proxy.py:596` | `def _sha256()` |
| `_upstream_auth_header` | function | `modules/lazy_proxy.py:307` | `def _upstream_auth_header(auth)` |
| `_upstream_tls_context` | function | `modules/lazy_proxy.py:224` | `def _upstream_tls_context(server_hostname)` |
| `_utc` | function | `modules/lazy_proxy.py:589` | `def _utc(timestamp)` |
| `_validate_proxy_target` | function | `modules/lazy_proxy.py:171` | `def _validate_proxy_target(host, port, scheme)` |
| `_write_leaf` | method | `modules/lazy_proxy.py:525` | `def _write_leaf(self, host, cert_path, key_path)` |
| `apply_env` | function | `modules/lazy_proxy.py:1176` | `def apply_env(ca_path, host, port)` |
| `ca_path` | method | `modules/lazy_proxy.py:738` | `def ca_path(self)` |
| `ca_trusted` | function | `modules/lazy_proxy.py:330` | `def ca_trusted(ca_path)` |
| `context_for` | method | `modules/lazy_proxy.py:568` | `def context_for(self, host)` |
| `detect_nss_profiles` | function | `modules/lazy_proxy.py:349` | `def detect_nss_profiles()` |
| `detect_trust_target` | function | `modules/lazy_proxy.py:322` | `def detect_trust_target()` |
| `do_CONNECT` | method | `modules/lazy_proxy.py:757` | `def do_CONNECT(self)` |
| `do_GET` | method | `modules/lazy_proxy.py:809` | `def do_GET(self)` |
| `env_for_ca` | function | `modules/lazy_proxy.py:1160` | `def env_for_ca(ca_path, host, port)` |
| `get_proxy` | function | `modules/lazy_proxy.py:1151` | `def get_proxy()` |
| `handle_error` | method | `modules/lazy_proxy.py:618` | `def handle_error(self, request, client_address)` |
| `install_ca_nss` | function | `modules/lazy_proxy.py:364` | `def install_ca_nss(ca_path, runner, profiles)` |
| `install_ca_trust` | function | `modules/lazy_proxy.py:404` | `def install_ca_trust(ca_path, runner)` |
| `log_message` | method | `modules/lazy_proxy.py:753` | `def log_message(self, fmt)` |
| `recorder` | method | `modules/lazy_proxy.py:734` | `def recorder(self)` |
| `restore_env` | function | `modules/lazy_proxy.py:1183` | `def restore_env(previous)` |
| `start` | method | `modules/lazy_proxy.py:651` | `def start(self, host, port, task_id, traffic_dir, upstream)` |
| `status` | method | `modules/lazy_proxy.py:712` | `def status(self)` |
| `stop` | method | `modules/lazy_proxy.py:696` | `def stop(self)` |
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
| `conformance` | function | `modules/lazy_roles.py:154` | `def conformance(role)` |
| `list_roles` | function | `modules/lazy_roles.py:100` | `def list_roles()` |
| `role_prompt` | function | `modules/lazy_roles.py:109` | `def role_prompt(role, goal, context)` |
| `roles_for_phase` | function | `modules/lazy_roles.py:134` | `def roles_for_phase(phase)` |
| `LoopRunConfig` | class | `modules/lazy_runner.py:90` | `class LoopRunConfig` |
| `ThreadStdoutRouter` | class | `modules/lazy_runner.py:41` | `class ThreadStdoutRouter(TextIOBase)` |
| `__init__` | method | `modules/lazy_runner.py:51` | `def __init__(self, main_stream, spool)` |
| `_abort_run` | function | `modules/lazy_runner.py:298` | `def _abort_run(engine, task_id, reason)` |
| `_bootstrap` | function | `modules/lazy_runner.py:380` | `def _bootstrap(scan_target, executor)` |
| `_dump_thread_stacks` | function | `modules/lazy_runner.py:524` | `def _dump_thread_stacks()` |
| `_executor` | function | `modules/lazy_runner.py:250` | `def _executor(command)` |
| `_format_activity` | function | `modules/lazy_runner.py:510` | `def _format_activity(record)` |
| `_overview` | function | `modules/lazy_runner.py:500` | `def _overview(task_id)` |
| `_poll_progress` | function | `modules/lazy_runner.py:539` | `def _poll_progress(engine, config, progress, transcript, worker)` |
| `_prepare_engine` | function | `modules/lazy_runner.py:317` | `def _prepare_engine(engine, shell, config, params)` |
| `_resolve_alias` | function | `modules/lazy_runner.py:242` | `def _resolve_alias(command)` |
| `_run` | function | `modules/lazy_runner.py:446` | `def _run()` |
| `_run_plain` | function | `modules/lazy_runner.py:656` | `def _run_plain(engine, config)` |
| `_run_with_progress` | function | `modules/lazy_runner.py:394` | `def _run_with_progress(engine, config)` |
| `_start_proxy` | function | `modules/lazy_runner.py:331` | `def _start_proxy(engine, params)` |
| `_terminal_stream` | function | `modules/lazy_runner.py:634` | `def _terminal_stream()` |
| `_to_float` | function | `modules/lazy_runner.py:129` | `def _to_float(raw, default)` |
| `_to_int` | function | `modules/lazy_runner.py:121` | `def _to_int(raw, default)` |
| `_tty_available` | function | `modules/lazy_runner.py:773` | `def _tty_available()` |
| `_write` | function | `modules/lazy_runner.py:646` | `def _write(text)` |
| `build_executor` | function | `modules/lazy_runner.py:225` | `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` |
| `clamped` | method | `modules/lazy_runner.py:107` | `def clamped(self)` |
| `encoding` | method | `modules/lazy_runner.py:76` | `def encoding(self)` |
| `flush` | method | `modules/lazy_runner.py:68` | `def flush(self)` |
| `isatty` | method | `modules/lazy_runner.py:80` | `def isatty(self)` |
| `parse_loop_line` | function | `modules/lazy_runner.py:137` | `def parse_loop_line(line)` |
| `report_result` | function | `modules/lazy_runner.py:356` | `def report_result(result)` |
| `run_loop` | function | `modules/lazy_runner.py:691` | `def run_loop(shell, params, config)` |
| `stream` | function | `modules/lazy_runner.py:409` | `def stream(text)` |
| `write` | method | `modules/lazy_runner.py:57` | `def write(self, data)` |
| `_payload_value` | function | `modules/lazy_sandbox.py:41` | `def _payload_value(key, default)` |
| `_sandbox_executor` | function | `modules/lazy_sandbox.py:265` | `def _sandbox_executor(command)` |
| `container_name` | function | `modules/lazy_sandbox.py:67` | `def container_name(task_id)` |
| `container_running` | function | `modules/lazy_sandbox.py:94` | `def container_running(task_id)` |
| `docker_available` | function | `modules/lazy_sandbox.py:73` | `def docker_available()` |
| `ensure_container` | function | `modules/lazy_sandbox.py:112` | `def ensure_container(task_id, image)` |
| `exec_command` | function | `modules/lazy_sandbox.py:180` | `def exec_command(task_id, command, timeout_sec, image)` |
| `executor_for` | function | `modules/lazy_sandbox.py:251` | `def executor_for(task_id, image)` |
| `image_available` | function | `modules/lazy_sandbox.py:78` | `def image_available(image)` |
| `image_name` | function | `modules/lazy_sandbox.py:52` | `def image_name(configured)` |
| `remove_container` | function | `modules/lazy_sandbox.py:214` | `def remove_container(task_id)` |
| `status` | function | `modules/lazy_sandbox.py:223` | `def status(task_id)` |
| `_hermes_config_path` | function | `modules/lazy_skill_mirror.py:112` | `def _hermes_config_path()` |
| `_hermes_frontmatter` | function | `modules/lazy_skill_mirror.py:45` | `def _hermes_frontmatter(name, fields)` |
| `_split_frontmatter` | function | `modules/lazy_skill_mirror.py:30` | `def _split_frontmatter(text)` |
| `available_skills` | function | `modules/lazy_skill_mirror.py:67` | `def available_skills()` |
| `mirror_all` | function | `modules/lazy_skill_mirror.py:106` | `def mirror_all()` |
| `mirror_skill` | function | `modules/lazy_skill_mirror.py:78` | `def mirror_skill(name)` |
| `register_external_dirs` | function | `modules/lazy_skill_mirror.py:117` | `def register_external_dirs()` |
| `_frontmatter` | function | `modules/lazy_skills.py:28` | `def _frontmatter(text)` |
| `_load` | function | `modules/lazy_skills.py:53` | `def _load(path)` |
| `_skill_files` | function | `modules/lazy_skills.py:42` | `def _skill_files()` |
| `get_skill` | function | `modules/lazy_skills.py:91` | `def get_skill(name)` |
| `list_skills` | function | `modules/lazy_skills.py:85` | `def list_skills()` |
| `match_skills` | function | `modules/lazy_skills.py:102` | `def match_skills(text, limit)` |
| `skills_context` | function | `modules/lazy_skills.py:118` | `def skills_context(text, explicit, auto, budget)` |
| `_digest` | function | `modules/lazy_summarizer.py:100` | `def _digest(older, complete)` |
| `_text_of` | function | `modules/lazy_summarizer.py:26` | `def _text_of(record)` |
| `_truncate_records` | function | `modules/lazy_summarizer.py:126` | `def _truncate_records(records, budget)` |
| `should_compact` | function | `modules/lazy_summarizer.py:35` | `def should_compact(used_chars, budget_chars)` |
| `summarize_chain` | function | `modules/lazy_summarizer.py:50` | `def summarize_chain(records, budget_chars, complete)` |
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

Next: [SYMBOLS_p16.md](SYMBOLS_p16.md)
