# Symbols (page 12 of 48)
Previous: [SYMBOLS_p11.md](SYMBOLS_p11.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `BitMState` | class | `modules/bitm_engine.py:85` | `class BitMState` |
| `_build_js_payload` | function | `modules/bitm_engine.py:151` | `def _build_js_payload(payload_name, lhost, lport)` |
| `_check_tool` | function | `modules/bitm_engine.py:168` | `def _check_tool(tool)` |
| `_ensure_bitm_dir` | function | `modules/bitm_engine.py:103` | `def _ensure_bitm_dir()` |
| `_get_default_interface` | function | `modules/bitm_engine.py:195` | `def _get_default_interface()` |
| `_get_gateway_ip` | function | `modules/bitm_engine.py:234` | `def _get_gateway_ip()` |
| `_load_state` | function | `modules/bitm_engine.py:134` | `def _load_state()` |
| `_recommend_method` | function | `modules/bitm_engine.py:180` | `def _recommend_method()` |
| `_save_state` | function | `modules/bitm_engine.py:108` | `def _save_state(state)` |
| `_start_arpspoof` | function | `modules/bitm_engine.py:413` | `def _start_arpspoof(target_ip, gateway_ip, interface, lhost, lport, js_payload, harvest_path)` |
| `_start_bettercap` | function | `modules/bitm_engine.py:354` | `def _start_bettercap(target_ip, gateway_ip, interface, lhost, lport, js_payload, harvest_path)` |
| `bitm_cleanup` | function | `modules/bitm_engine.py:642` | `def bitm_cleanup()` |
| `bitm_harvest_stats` | function | `modules/bitm_engine.py:607` | `def bitm_harvest_stats()` |
| `bitm_inject` | function | `modules/bitm_engine.py:572` | `def bitm_inject(payload_name)` |
| `bitm_start` | function | `modules/bitm_engine.py:257` | `def bitm_start(target_ip, gateway_ip, interface, lhost, lport, method, payloads)` |
| `bitm_status` | function | `modules/bitm_engine.py:539` | `def bitm_status()` |
| `bitm_stop` | function | `modules/bitm_engine.py:481` | `def bitm_stop()` |
| `main` | function | `modules/bitm_engine.py:661` | `def main()` |
| `BofCatalog` | class | `modules/bof_registry.py:157` | `class BofCatalog` |
| `BofCategory` | class | `modules/bof_registry.py:68` | `class BofCategory(str, Enum)` |
| `BofEntry` | class | `modules/bof_registry.py:85` | `class BofEntry` |
| `BofMarketplace` | class | `modules/bof_registry.py:639` | `class BofMarketplace` |
| `BofPlatform` | class | `modules/bof_registry.py:61` | `class BofPlatform(str, Enum)` |
| `BofRegistry` | class | `modules/bof_registry.py:552` | `class BofRegistry` |
| `BofValidator` | class | `modules/bof_registry.py:506` | `class BofValidator` |
| `__init__` | method | `modules/bof_registry.py:559` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/bof_registry.py:651` | `def __init__(self, sessions_dir, catalog)` |
| `_build_default_catalog` | function | `modules/bof_registry.py:265` | `def _build_default_catalog()` |
| `_load_manifest` | method | `modules/bof_registry.py:569` | `def _load_manifest(self)` |
| `_save_manifest` | method | `modules/bof_registry.py:580` | `def _save_manifest(self, manifest)` |
| `bulk_install` | method | `modules/bof_registry.py:769` | `def bulk_install(self, names)` |
| `catalog` | method | `modules/bof_registry.py:662` | `def catalog(self)` |
| `compute_sha256` | method | `modules/bof_registry.py:515` | `def compute_sha256(filepath)` |
| `from_dict` | method | `modules/bof_registry.py:137` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/bof_registry.py:241` | `def from_dict(cls, raw)` |
| `get` | method | `modules/bof_registry.py:177` | `def get(self, name)` |
| `get_install_info` | method | `modules/bof_registry.py:633` | `def get_install_info(self, name)` |
| `info` | method | `modules/bof_registry.py:690` | `def info(self, name)` |
| `install` | method | `modules/bof_registry.py:590` | `def install(self, entry)` |
| `install` | method | `modules/bof_registry.py:707` | `def install(self, name)` |
| `install_dir` | method | `modules/bof_registry.py:565` | `def install_dir(self)` |
| `is_installed` | method | `modules/bof_registry.py:585` | `def is_installed(self, name)` |
| `list_all` | method | `modules/bof_registry.py:229` | `def list_all(self)` |
| `list_by_category` | method | `modules/bof_registry.py:221` | `def list_by_category(self, category)` |
| `list_by_platform` | method | `modules/bof_registry.py:225` | `def list_by_platform(self, platform)` |
| `list_installed` | method | `modules/bof_registry.py:628` | `def list_installed(self)` |
| `list_installed` | method | `modules/bof_registry.py:749` | `def list_installed(self)` |
| `list_missing_dependencies` | method | `modules/bof_registry.py:761` | `def list_missing_dependencies(self, name)` |
| `load` | method | `modules/bof_registry.py:249` | `def load(cls, path)` |
| `register` | method | `modules/bof_registry.py:167` | `def register(self, entry)` |
| `register_many` | method | `modules/bof_registry.py:172` | `def register_many(self, entries)` |
| `registry` | method | `modules/bof_registry.py:667` | `def registry(self)` |
| `save` | method | `modules/bof_registry.py:257` | `def save(self, path)` |
| `search` | method | `modules/bof_registry.py:188` | `def search(self, query)` |
| `search` | method | `modules/bof_registry.py:671` | `def search(self, query)` |
| `to_dict` | method | `modules/bof_registry.py:118` | `def to_dict(self)` |
| `to_dict` | method | `modules/bof_registry.py:233` | `def to_dict(self)` |
| `uninstall` | method | `modules/bof_registry.py:611` | `def uninstall(self, name, remove_files)` |
| `uninstall` | method | `modules/bof_registry.py:736` | `def uninstall(self, name)` |
| `validate_args` | method | `modules/bof_registry.py:540` | `def validate_args(entry, args)` |
| `verify_entry` | method | `modules/bof_registry.py:524` | `def verify_entry(entry, filepath)` |
| `C2Server` | class | `modules/c2_agent.py:711` | `class C2Server` |
| `__init__` | method | `modules/c2_agent.py:714` | `def __init__(self, port, user, password)` |
| `_api` | function | `modules/c2_agent.py:825` | `def _api(path, data)` |
| `_ensure_key` | function | `modules/c2_agent.py:462` | `def _ensure_key()` |
| `_pid` | method | `modules/c2_agent.py:719` | `def _pid(self)` |
| `_restore_key_from_snapshot` | function | `modules/c2_agent.py:493` | `def _restore_key_from_snapshot()` |
| `_snapshot_key` | function | `modules/c2_agent.py:516` | `def _snapshot_key(aes_hex)` |
| `_sync_credentials_file` | function | `modules/c2_agent.py:59` | `def _sync_credentials_file(user, password)` |
| `_unverified_context` | function | `modules/c2_agent.py:84` | `def _unverified_context()` |
| `build_agent` | function | `modules/c2_agent.py:398` | `def build_agent(c2_url, client_id, aes_hex, rat_key, route, sleep, privilege)` |
| `client_id_for` | function | `modules/c2_agent.py:94` | `def client_id_for(target, privilege)` |
| `deploy` | function | `modules/c2_agent.py:533` | `def deploy(target, c2_base, route, lhost, sleep, privilege)` |
| `ensure_http_listener` | method | `modules/c2_agent.py:817` | `def ensure_http_listener(self, http_port, auth)` |
| `read_aes_hex` | function | `modules/c2_agent.py:528` | `def read_aes_hex()` |
| `read_records` | function | `modules/c2_agent.py:680` | `def read_records(client_id, limit)` |
| `start` | method | `modules/c2_agent.py:763` | `def start(self)` |
| `status` | method | `modules/c2_agent.py:731` | `def status(self)` |
| `stop` | method | `modules/c2_agent.py:794` | `def stop(self)` |
| `validate_client_id` | function | `modules/c2_agent.py:119` | `def validate_client_id(raw)` |
| `wait_record` | function | `modules/c2_agent.py:697` | `def wait_record(client_id, command, since, timeout)` |
| `C2Builder` | class | `modules/c2_builder.py:449` | `class C2Builder` |
| `C2Profile` | class | `modules/c2_builder.py:77` | `class C2Profile` |
| `__init__` | method | `modules/c2_builder.py:452` | `def __init__(self, params, sessions_dir, cmd_fn, onecmd_fn, toastr_fn, c2_user, c2_pass)` |
| `_beacon_scan_ports_csv` | function | `modules/c2_builder.py:274` | `def _beacon_scan_ports_csv(params)` |
| `_build_compile_commands` | function | `modules/c2_builder.py:367` | `def _build_compile_commands(sessions_dir, profile, gocompiler, compile_flags, main_out, main_src, listener_out...` |
| `_build_context` | function | `modules/c2_builder.py:418` | `def _build_context(sessions_dir)` |
| `_command_output` | function | `modules/c2_builder.py:306` | `def _command_output(argv, timeout)` |
| `_ensure_garble_toolchain` | method | `modules/c2_builder.py:470` | `def _ensure_garble_toolchain(self, go_bin, garble_bin, gocompiler, profile)` |
| `_ensure_go` | function | `modules/c2_builder.py:60` | `def _ensure_go(cmd_fn)` |
| `_garble_matches_toolchain` | function | `modules/c2_builder.py:344` | `def _garble_matches_toolchain(go_bin, garble_bin)` |
| `_go_build_version` | function | `modules/c2_builder.py:325` | `def _go_build_version(go_bin, target)` |
| `_go_string_list` | function | `modules/c2_builder.py:221` | `def _go_string_list(urls)` |
| `_lkm_makefile_text` | function | `modules/c2_builder.py:238` | `def _lkm_makefile_text(listener_ip, listener_port)` |
| `_parse_go_version` | function | `modules/c2_builder.py:291` | `def _parse_go_version(text)` |
| `_preflight` | function | `modules/c2_builder.py:161` | `def _preflight(profile)` |
| `_read` | function | `modules/c2_builder.py:713` | `def _read(path_)` |
| `_read_required` | function | `modules/c2_builder.py:720` | `def _read_required(path_)` |
| `_render_template` | function | `modules/c2_builder.py:170` | `def _render_template(content, context)` |
| `_replacer` | function | `modules/c2_builder.py:174` | `def _replacer(match)` |
| `_resolve_fallback_urls` | function | `modules/c2_builder.py:181` | `def _resolve_fallback_urls(params)` |
| `_resolve_go_bin` | function | `modules/c2_builder.py:45` | `def _resolve_go_bin()` |
| `_write` | function | `modules/c2_builder.py:724` | `def _write(path_, content)` |
| `run` | method | `modules/c2_builder.py:510` | `def run(self, line, choice, use_tunnel)` |
| `PayloadConfigAdapter` | class | `modules/c2_messaging_base.py:117` | `class PayloadConfigAdapter` |
| `SecureSessionManager` | class | `modules/c2_messaging_base.py:9` | `class SecureSessionManager` |
| `__getitem__` | method | `modules/c2_messaging_base.py:129` | `def __getitem__(self, key)` |
| `__init__` | method | `modules/c2_messaging_base.py:22` | `def __init__(self, max_failed_attempts, lockout_duration, rate_limit, session_timeout)` |
| `__init__` | method | `modules/c2_messaging_base.py:124` | `def __init__(self, config_dict)` |
| `check_lockout` | method | `modules/c2_messaging_base.py:46` | `def check_lockout(self, user_id)` |
| `check_rate_limit` | method | `modules/c2_messaging_base.py:61` | `def check_rate_limit(self, user_id)` |
| `create_session` | method | `modules/c2_messaging_base.py:79` | `def create_session(self, user_id, client_id)` |
| `get` | method | `modules/c2_messaging_base.py:132` | `def get(self, key, default)` |
| `get_client` | method | `modules/c2_messaging_base.py:111` | `def get_client(self, user_id)` |
| `register_failed_attempt` | method | `modules/c2_messaging_base.py:37` | `def register_failed_attempt(self, user_id)` |
| `set_client` | method | `modules/c2_messaging_base.py:106` | `def set_client(self, user_id, client_id)` |
| `validate_session` | method | `modules/c2_messaging_base.py:89` | `def validate_session(self, user_id)` |
| `C2Profile` | class | `modules/c2_profile.py:81` | `class C2Profile` |
| `HttpConfig` | class | `modules/c2_profile.py:62` | `class HttpConfig` |
| `ProfileApplier` | class | `modules/c2_profile.py:520` | `class ProfileApplier` |
| `ProfileLoader` | class | `modules/c2_profile.py:187` | `class ProfileLoader` |
| `ProfileRegistry` | class | `modules/c2_profile.py:449` | `class ProfileRegistry` |
| `ProfileValidator` | class | `modules/c2_profile.py:155` | `class ProfileValidator` |
| `SleepConfig` | class | `modules/c2_profile.py:54` | `class SleepConfig` |
| `StagerConfig` | class | `modules/c2_profile.py:72` | `class StagerConfig` |
| `__init__` | method | `modules/c2_profile.py:457` | `def __init__(self)` |
| `_config_for` | method | `modules/c2_profile.py:144` | `def _config_for(self, method)` |
| `_make_aggressive_profile` | function | `modules/c2_profile.py:385` | `def _make_aggressive_profile()` |
| `_make_debug_profile` | function | `modules/c2_profile.py:410` | `def _make_debug_profile()` |
| `_make_default_profile` | function | `modules/c2_profile.py:308` | `def _make_default_profile()` |
| `_make_stealth_profile` | function | `modules/c2_profile.py:339` | `def _make_stealth_profile()` |
| `apply_to_response` | method | `modules/c2_profile.py:529` | `def apply_to_response(profile, response)` |
| `apply_to_session` | method | `modules/c2_profile.py:554` | `def apply_to_session(profile, session)` |
| `build_headers` | method | `modules/c2_profile.py:128` | `def build_headers(self, method)` |
| `from_dict` | method | `modules/c2_profile.py:215` | `def from_dict(d)` |
| `from_yaml` | method | `modules/c2_profile.py:200` | `def from_yaml(path)` |
| `get` | method | `modules/c2_profile.py:473` | `def get(self, name)` |
| `get_beacon_config` | method | `modules/c2_profile.py:567` | `def get_beacon_config(profile)` |
| `get_profile` | function | `modules/c2_profile.py:620` | `def get_profile(name)` |
| `get_registry` | function | `modules/c2_profile.py:595` | `def get_registry()` |
| `get_uri` | method | `modules/c2_profile.py:117` | `def get_uri(self, method)` |
| `jitter_delay` | method | `modules/c2_profile.py:101` | `def jitter_delay(self)` |
| `list_names` | method | `modules/c2_profile.py:485` | `def list_names(self)` |
| `list_profiles` | function | `modules/c2_profile.py:625` | `def list_profiles()` |
| `load_from_directory` | method | `modules/c2_profile.py:493` | `def load_from_directory(self, path)` |
| `register` | method | `modules/c2_profile.py:464` | `def register(self, name, profile)` |
| `save` | method | `modules/c2_profile.py:282` | `def save(profile, path)` |
| `to_dict` | method | `modules/c2_profile.py:254` | `def to_dict(profile)` |
| `validate` | method | `modules/c2_profile.py:162` | `def validate(self, profile)` |
| `DnsProfile` | class | `modules/c2_profile_engine.py:205` | `class DnsProfile` |
| `ProfileEngine` | class | `modules/c2_profile_engine.py:611` | `class ProfileEngine` |
| `ProfileRotator` | class | `modules/c2_profile_engine.py:441` | `class ProfileRotator` |
| `ProfileValidator` | class | `modules/c2_profile_engine.py:503` | `class ProfileValidator` |
| `RotationSlot` | class | `modules/c2_profile_engine.py:414` | `class RotationSlot` |
| `SmbProfile` | class | `modules/c2_profile_engine.py:289` | `class SmbProfile` |
| `TlsProfile` | class | `modules/c2_profile_engine.py:117` | `class TlsProfile` |
| `TransportType` | class | `modules/c2_profile_engine.py:404` | `class TransportType(Enum)` |
| `WebSocketProfile` | class | `modules/c2_profile_engine.py:349` | `class WebSocketProfile` |
| `__init__` | method | `modules/c2_profile_engine.py:453` | `def __init__(self, slots)` |
| `__init__` | method | `modules/c2_profile_engine.py:627` | `def __init__(self, tls_profile, dns_profile, smb_profile, websocket_profile, rotation_slots)` |
| `_default_slots` | method | `modules/c2_profile_engine.py:709` | `def _default_slots(self)` |
| `active_transport` | method | `modules/c2_profile_engine.py:668` | `def active_transport(self)` |
| `build_query_subdomain` | method | `modules/c2_profile_engine.py:231` | `def build_query_subdomain(self, data, packet_id)` |
| `current_slot` | method | `modules/c2_profile_engine.py:460` | `def current_slot(self)` |
| `dns_profile` | method | `modules/c2_profile_engine.py:648` | `def dns_profile(self)` |
| `from_config` | method | `modules/c2_profile_engine.py:771` | `def from_config(cls, config)` |
| `from_dict` | method | `modules/c2_profile_engine.py:173` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:261` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:319` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:375` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:747` | `def from_dict(cls, raw)` |
| `from_payload` | method | `modules/c2_profile_engine.py:766` | `def from_payload(cls, payload)` |
| `get_active_profile_dict` | method | `modules/c2_profile_engine.py:685` | `def get_active_profile_dict(self)` |
| `get_all_profiles_dict` | method | `modules/c2_profile_engine.py:699` | `def get_all_profiles_dict(self)` |
| `get_cipher_suites` | method | `modules/c2_profile_engine.py:144` | `def get_cipher_suites(self)` |
| `get_ja3_hash` | method | `modules/c2_profile_engine.py:155` | `def get_ja3_hash(self)` |
| `is_available` | method | `modules/c2_profile_engine.py:429` | `def is_available(self)` |
| `list_slots` | method | `modules/c2_profile_engine.py:487` | `def list_slots(self)` |
| `rotate` | method | `modules/c2_profile_engine.py:469` | `def rotate(self)` |
| `rotate` | method | `modules/c2_profile_engine.py:672` | `def rotate(self)` |
| `rotator` | method | `modules/c2_profile_engine.py:663` | `def rotator(self)` |
| `smb_profile` | method | `modules/c2_profile_engine.py:653` | `def smb_profile(self)` |
| `tls_profile` | method | `modules/c2_profile_engine.py:643` | `def tls_profile(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:188` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:274` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:333` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:389` | `def to_dict(self)` |
| `touch` | method | `modules/c2_profile_engine.py:436` | `def touch(self)` |
| `transport` | method | `modules/c2_profile_engine.py:465` | `def transport(self)` |
| `validate` | method | `modules/c2_profile_engine.py:676` | `def validate(self)` |
| `validate_all` | method | `modules/c2_profile_engine.py:591` | `def validate_all(self, tls, dns, smb, websocket)` |
| `validate_dns` | method | `modules/c2_profile_engine.py:536` | `def validate_dns(profile)` |
| `validate_smb` | method | `modules/c2_profile_engine.py:556` | `def validate_smb(profile)` |
| `validate_tls` | method | `modules/c2_profile_engine.py:511` | `def validate_tls(profile)` |
| `validate_websocket` | method | `modules/c2_profile_engine.py:576` | `def validate_websocket(profile)` |
| `websocket_profile` | method | `modules/c2_profile_engine.py:658` | `def websocket_profile(self)` |
| `_normalize_task_title` | function | `modules/c2_surfaces.py:256` | `def _normalize_task_title(title)` |
| `_read_json` | function | `modules/c2_surfaces.py:42` | `def _read_json(path, default)` |
| `_stamp` | function | `modules/c2_surfaces.py:68` | `def _stamp()` |
| `_write_json` | function | `modules/c2_surfaces.py:54` | `def _write_json(path, data)` |
| `append_note` | function | `modules/c2_surfaces.py:155` | `def append_note(line, sessions_dir)` |
| `group_tasks_for_display` | function | `modules/c2_surfaces.py:261` | `def group_tasks_for_display(tasks)` |
| `publish_banner` | function | `modules/c2_surfaces.py:73` | `def publish_banner(hostname, port, protocol, service, extra, sessions_dir)` |
| `publish_cve` | function | `modules/c2_surfaces.py:115` | `def publish_cve(title, description, operator, risk, sessions_dir)` |
| `refresh_session_report` | function | `modules/c2_surfaces.py:229` | `def refresh_session_report(timeout)` |
| `register_loot_event` | function | `modules/c2_surfaces.py:184` | `def register_loot_event(name, path_glob, description, event_config)` |
| `severity_to_risk` | function | `modules/c2_surfaces.py:251` | `def severity_to_risk(severity)` |
| `days_in_month` | function | `modules/cal.sh:14` | `` |
| `first_day_of_month` | function | `modules/cal.sh:31` | `` |
| `is_leap_year` | function | `modules/cal.sh:4` | `` |
| `PendingStore` | class | `modules/chain_approval.py:114` | `class PendingStore` |
| `__init__` | method | `modules/chain_approval.py:117` | `def __init__(self, sessions_dir)` |
| `_audit` | function | `modules/chain_approval.py:91` | `def _audit(sessions_dir, event)` |
| `_audit_path` | function | `modules/chain_approval.py:73` | `def _audit_path(sessions_dir)` |
| `_clamp_timeout` | function | `modules/chain_approval.py:52` | `def _clamp_timeout(value)` |
| `_load` | method | `modules/chain_approval.py:125` | `def _load(self)` |
| `_now` | function | `modules/chain_approval.py:47` | `def _now()` |
| `_save` | method | `modules/chain_approval.py:141` | `def _save(self, payload)` |
| `_store_path` | function | `modules/chain_approval.py:68` | `def _store_path(sessions_dir)` |
| `approval_backend` | function | `modules/chain_approval.py:318` | `def approval_backend()` |
| `approve` | function | `modules/chain_approval.py:358` | `def approve(step_id, command)` |
| `build_c2_approver` | function | `modules/chain_approval.py:328` | `def build_c2_approver(printer, chain_name, run_id, timeout, poll_interval, sessions_dir, clock)` |
| `command_fingerprint` | function | `modules/chain_approval.py:78` | `def command_fingerprint(command)` |
| `create` | method | `modules/chain_approval.py:153` | `def create(self, chain, step_id, command, timeout, run_id, now_override)` |
| `decide` | method | `modules/chain_approval.py:229` | `def decide(self, request_id, allowed, decided_by, note, expired)` |
| `expire_stale` | method | `modules/chain_approval.py:282` | `def expire_stale(self, now)` |
| `get` | method | `modules/chain_approval.py:204` | `def get(self, request_id)` |
| `list` | method | `modules/chain_approval.py:215` | `def list(self, status)` |
| `DistillReport` | class | `modules/chain_distill.py:479` | `class DistillReport` |
| `StepDecision` | class | `modules/chain_distill.py:458` | `class StepDecision` |
| `_artifact_pins` | function | `modules/chain_distill.py:338` | `def _artifact_pins(command, output, target)` |
| `_command_index_phases` | function | `modules/chain_distill.py:249` | `def _command_index_phases()` |
| `_command_verb` | function | `modules/chain_distill.py:229` | `def _command_verb(command)` |
| `_excluded_host` | function | `modules/chain_distill.py:374` | `def _excluded_host(host, operator_deny)` |
| `_infer_target` | function | `modules/chain_distill.py:418` | `def _infer_target(rows, graph, operator_deny)` |
| `_is_doc_example` | function | `modules/chain_distill.py:310` | `def _is_doc_example(host)` |
| `_is_failed` | function | `modules/chain_distill.py:213` | `def _is_failed(row)` |
| `_is_prose` | function | `modules/chain_distill.py:198` | `def _is_prose(command)` |
| `_load_graph` | function | `modules/chain_distill.py:172` | `def _load_graph(path)` |
| `_load_traffic` | function | `modules/chain_distill.py:136` | `def _load_traffic(path)` |
| `_operator_deny` | function | `modules/chain_distill.py:400` | `def _operator_deny(sessions_dir)` |
| `_phase_for` | function | `modules/chain_distill.py:278` | `def _phase_for(command, manifest_phase)` |
| `_slug` | function | `modules/chain_distill.py:80` | `def _slug(text)` |
| `build_chain_data` | function | `modules/chain_distill.py:574` | `def build_chain_data(task, rows, graph, manifests)` |
| `distill` | function | `modules/chain_distill.py:687` | `def distill(task, sessions_dir, write, chains_dir)` |
| `dropped` | method | `modules/chain_distill.py:512` | `def dropped(self)` |
| `kept` | method | `modules/chain_distill.py:507` | `def kept(self)` |
| `locate_traces` | function | `modules/chain_distill.py:93` | `def locate_traces(task, sessions_dir)` |
| `note` | function | `modules/chain_distill.py:598` | `def note(row, kept, reason)` |
| `render` | method | `modules/chain_distill.py:543` | `def render(self, verbose)` |
| `to_dict` | method | `modules/chain_distill.py:516` | `def to_dict(self)` |
| `_default_store` | function | `modules/chain_facts.py:73` | `def _default_store()` |
| `_host_hint` | function | `modules/chain_facts.py:84` | `def _host_hint(output, phase, target_hint)` |
| `spool_chain_outputs` | function | `modules/chain_facts.py:24` | `def spool_chain_outputs(result, sessions_dir, fact_store_factory)` |
| `best_chain` | function | `modules/chain_match.py:135` | `def best_chain(phase, os_hint, services, exclude, allow_lab, rows, ttl)` |
| `load_rows` | function | `modules/chain_match.py:105` | `def load_rows(allow_lab, ttl)` |
| `normalize_tags` | function | `modules/chain_match.py:48` | `def normalize_tags(tags)` |
| `platform_ok` | function | `modules/chain_match.py:74` | `def platform_ok(platforms, os_hint)` |
| `reset_cache` | function | `modules/chain_match.py:97` | `def reset_cache()` |
| `score` | function | `modules/chain_match.py:85` | `def score(tags, phase, svc_tokens)` |
| `service_tokens` | function | `modules/chain_match.py:64` | `def service_tokens(services)` |
| `Chain` | class | `modules/chain_registry.py:152` | `class Chain` |
| `ChainStep` | class | `modules/chain_registry.py:102` | `class ChainStep` |
| `_eval` | function | `modules/chain_registry.py:313` | `def _eval(node)` |
| `_materialize` | function | `modules/chain_registry.py:610` | `def _materialize(name, raw, stack)` |
| `_nonneg_int` | function | `modules/chain_registry.py:657` | `def _nonneg_int(raw)` |
| `_render` | function | `modules/chain_registry.py:235` | `def _render(template, variables)` |
| `_step_from_raw` | function | `modules/chain_registry.py:666` | `def _step_from_raw(item)` |
| `_when_tree` | function | `modules/chain_registry.py:264` | `def _when_tree(expression)` |
| `evaluate_when` | function | `modules/chain_registry.py:291` | `def evaluate_when(expression, variables)` |
| `generate_for_playbook` | function | `modules/chain_registry.py:809` | `def generate_for_playbook(engine_key, apt_display, description, chains_dir, overwrite)` |
| `get` | function | `modules/chain_registry.py:721` | `def get(name, chains_dir)` |
| `identifier` | method | `modules/chain_registry.py:146` | `def identifier(self)` |
| `load_all` | function | `modules/chain_registry.py:576` | `def load_all(chains_dir)` |
| `render_text_token_braces` | function | `modules/chain_registry.py:571` | `def render_text_token_braces(text)` |
| `resolve` | method | `modules/chain_registry.py:170` | `def resolve(self, tokens)` |
| `scan_all` | function | `modules/chain_registry.py:726` | `def scan_all(chains_dir)` |
| `set_enabled` | function | `modules/chain_registry.py:786` | `def set_enabled(name, enabled, chains_dir)` |
| `skip_pending` | function | `modules/chain_registry.py:67` | `def skip_pending(path, max_age, now)` |
| `validate_chain` | function | `modules/chain_registry.py:356` | `def validate_chain(data, filename, chains_dir)` |
| `ChainRunResult` | class | `modules/chain_runner.py:110` | `class ChainRunResult` |
| `ChainRunner` | class | `modules/chain_runner.py:216` | `class ChainRunner` |
| `ReplanContext` | class | `modules/chain_runner.py:161` | `class ReplanContext` |
| `StepOutcome` | class | `modules/chain_runner.py:54` | `class StepOutcome` |
| `__init__` | method | `modules/chain_runner.py:219` | `def __init__(self, chain, tokens, shell, executor, default_timeout, dry_run, on_step, retry_backoff, total_timeout...` |
| `_all_json_objects` | function | `modules/chain_runner.py:1377` | `def _all_json_objects(text)` |
| `_apply_replanner` | method | `modules/chain_runner.py:830` | `def _apply_replanner(self, result, index, outcome, steps, step_index, variables, captured_keys)` |
| `_ask_approval` | method | `modules/chain_runner.py:1129` | `def _ask_approval(self, step_id, command)` |
| `_call` | method | `modules/chain_runner.py:1357` | `def _call(callback, timeout)` |
| `_deliver` | method | `modules/chain_runner.py:691` | `def _deliver(self, outcome)` |
| `_dependency_block` | method | `modules/chain_runner.py:1062` | `def _dependency_block(step, prior_verdicts)` |
| `_execute` | method | `modules/chain_runner.py:1239` | `def _execute(self, command, timeout, expect_exits)` |
| `_first_json` | method | `modules/chain_runner.py:1200` | `def _first_json(output)` |
| `_is_verb` | method | `modules/chain_runner.py:1274` | `def _is_verb(self, command)` |
| `_load_json_events` | function | `modules/chain_runner.py:1398` | `def _load_json_events(path)` |
| `_notify` | method | `modules/chain_runner.py:821` | `def _notify(self, outcome)` |
| `_pace_after` | method | `modules/chain_runner.py:305` | `def _pace_after(self, outcome, started)` |
| `_pre_check_timeout` | method | `modules/chain_runner.py:1144` | `def _pre_check_timeout(self, step)` |
| `_promoted_sinks` | method | `modules/chain_runner.py:696` | `def _promoted_sinks(self, outcome)` |
| `_publish_step` | method | `modules/chain_runner.py:721` | `def _publish_step(self, outcome)` |
| `_raise_timeout` | function | `modules/chain_runner.py:1320` | `def _raise_timeout(_signum, _frame)` |
| `_record_verdict` | method | `modules/chain_runner.py:917` | `def _record_verdict(verdicts, outcome)` |
| `_render_command` | method | `modules/chain_runner.py:1214` | `def _render_command(self, template, variables, captured_keys)` |
| `_run_fallback_chain` | method | `modules/chain_runner.py:620` | `def _run_fallback_chain(self, result, variables, captured_keys, started)` |
| `_run_parallel_group` | method | `modules/chain_runner.py:526` | `def _run_parallel_group(self, group, executions, resumed_ok, variables, captured_keys, prior_verdicts)` |
| `_run_raw` | method | `modules/chain_runner.py:1340` | `def _run_raw(self, command, timeout, allowed)` |
| `_run_shell_verb` | method | `modules/chain_runner.py:1285` | `def _run_shell_verb(self, command, timeout)` |
| `_run_step` | method | `modules/chain_runner.py:924` | `def _run_step(self, step, variables, captured_keys, prior_verdicts)` |
| `_save_checkpoint` | method | `modules/chain_runner.py:879` | `def _save_checkpoint(self, result, variables, captured_keys, next_index, state_name, verdicts)` |
| `_skip_remaining` | method | `modules/chain_runner.py:511` | `def _skip_remaining(self, steps, start, reason)` |
| `_store_capture` | method | `modules/chain_runner.py:1148` | `def _store_capture(self, step, output, outcome, variables, captured_keys)` |
| `_verify_evidence` | method | `modules/chain_runner.py:1084` | `def _verify_evidence(self, step, outcome, variables)` |
| `_verify_timeout` | method | `modules/chain_runner.py:1138` | `def _verify_timeout(self, step)` |
| `applied_vars` | method | `modules/chain_runner.py:193` | `def applied_vars(self)` |
| `chain_proven` | method | `modules/chain_runner.py:155` | `def chain_proven(self)` |
| `insert_step` | method | `modules/chain_runner.py:183` | `def insert_step(self, step)` |
| `inserted` | method | `modules/chain_runner.py:198` | `def inserted(self)` |
| `ok` | method | `modules/chain_runner.py:82` | `def ok(self)` |
| `render_text` | function | `modules/chain_runner.py:208` | `def render_text(template, variables)` |
| `run` | method | `modules/chain_runner.py:332` | `def run(self)` |
| `set_var` | method | `modules/chain_runner.py:178` | `def set_var(self, name, value)` |
| `skip_rest` | method | `modules/chain_runner.py:188` | `def skip_rest(self)` |
| `skip_rest_flag` | method | `modules/chain_runner.py:203` | `def skip_rest_flag(self)` |
| `to_dict` | method | `modules/chain_runner.py:86` | `def to_dict(self)` |
| `to_dict` | method | `modules/chain_runner.py:131` | `def to_dict(self)` |
| `checkpoint_dir` | function | `modules/chain_state.py:26` | `def checkpoint_dir(base_dir)` |
| `list_checkpoints` | function | `modules/chain_state.py:80` | `def list_checkpoints(directory, limit, chain)` |
| `load_checkpoint` | function | `modules/chain_state.py:65` | `def load_checkpoint(directory, run_id)` |
| `new_run_id` | function | `modules/chain_state.py:33` | `def new_run_id(chain_name)` |
| `write_checkpoint` | function | `modules/chain_state.py:39` | `def write_checkpoint(directory, state)` |
| `_service_steps` | function | `modules/chain_synth.py:42` | `def _service_steps(host, services)` |
| `_slug` | function | `modules/chain_synth.py:29` | `def _slug(name)` |
| `_wordlist` | function | `modules/chain_synth.py:33` | `def _wordlist(param, fallback)` |
| `facts_for_target` | function | `modules/chain_synth.py:224` | `def facts_for_target(target)` |
| `synth_chain_data` | function | `modules/chain_synth.py:89` | `def synth_chain_data(playbook, target, services, has_creds, os_hint, include_c2)` |
| `write_generated_chain` | function | `modules/chain_synth.py:253` | `def write_generated_chain(data, chains_dir)` |
| `_candidate_files` | function | `modules/chain_tokens.py:120` | `def _candidate_files()` |
| `_load_host_facts` | function | `modules/chain_tokens.py:77` | `def _load_host_facts(host)` |
| `_mentions` | function | `modules/chain_tokens.py:130` | `def _mentions(path, needle)` |
| `_newest_creds_file` | function | `modules/chain_tokens.py:93` | `def _newest_creds_file(host)` |
| `build_tokens` | function | `modules/chain_tokens.py:29` | `def build_tokens(target, params)` |
| `token_keys` | function | `modules/chain_tokens.py:24` | `def token_keys()` |
| `CICDEnumerator` | class | `modules/cicd_enumerator.py:43` | `class CICDEnumerator` |
| `CICDFinding` | class | `modules/cicd_enumerator.py:33` | `class CICDFinding` |
| `__init__` | method | `modules/cicd_enumerator.py:54` | `def __init__(self, target_url, sessions_dir)` |
| `_check_azure_devops` | method | `modules/cicd_enumerator.py:230` | `def _check_azure_devops(self)` |
| `_check_bitbucket` | method | `modules/cicd_enumerator.py:266` | `def _check_bitbucket(self)` |
| `_check_github_actions` | method | `modules/cicd_enumerator.py:189` | `def _check_github_actions(self)` |
| `_check_gitlab` | method | `modules/cicd_enumerator.py:120` | `def _check_gitlab(self)` |
| `_check_jenkins` | method | `modules/cicd_enumerator.py:73` | `def _check_jenkins(self)` |
| `export_findings` | method | `modules/cicd_enumerator.py:387` | `def export_findings(self)` |
| `generate_ci_attack_matrix` | method | `modules/cicd_enumerator.py:322` | `def generate_ci_attack_matrix(self)` |
| `scan` | method | `modules/cicd_enumerator.py:60` | `def scan(self)` |
| `scan_build_log` | method | `modules/cicd_enumerator.py:297` | `def scan_build_log(self, log_content, source)` |
| `_clear_cli_session` | function | `modules/cli_auth.py:478` | `def _clear_cli_session()` |
| `_load_payload` | function | `modules/cli_auth.py:85` | `def _load_payload()` |
| `_load_users` | function | `modules/cli_auth.py:34` | `def _load_users()` |
| `_read_cli_session` | function | `modules/cli_auth.py:429` | `def _read_cli_session()` |
| `_save_payload` | function | `modules/cli_auth.py:100` | `def _save_payload(payload)` |
| `_save_users` | function | `modules/cli_auth.py:52` | `def _save_users(users)` |
| `_write_cli_session` | function | `modules/cli_auth.py:444` | `def _write_cli_session(username, elo, role)` |
| `_write_cli_session_raw` | function | `modules/cli_auth.py:462` | `def _write_cli_session_raw(data)` |
| `get_current_operator` | function | `modules/cli_auth.py:396` | `def get_current_operator()` |
| `login` | function | `modules/cli_auth.py:240` | `def login(username, password, remember)` |
| `logout` | function | `modules/cli_auth.py:293` | `def logout()` |
| `needs_login` | function | `modules/cli_auth.py:487` | `def needs_login()` |
| `register` | function | `modules/cli_auth.py:145` | `def register(username, password)` |
| `sync_elo_from_session` | function | `modules/cli_auth.py:408` | `def sync_elo_from_session(elo)` |
| `try_auto_login` | function | `modules/cli_auth.py:328` | `def try_auto_login()` |
| `user_exists` | function | `modules/cli_auth.py:122` | `def user_exists(username)` |
| `verify_password` | function | `modules/cli_auth.py:214` | `def verify_password(username, password)` |
| `whoami` | function | `modules/cli_auth.py:366` | `def whoami()` |
| `Comparison` | class | `modules/closedloop.py:55` | `class Comparison` |
| `RuleMetrics` | class | `modules/closedloop.py:32` | `class RuleMetrics` |
| `_metrics_for` | function | `modules/closedloop.py:77` | `def _metrics_for(result)` |
| `compare_rules` | function | `modules/closedloop.py:90` | `def compare_rules(baseline_rule, candidate_rule, target_logs, control_logs)` |
| `suggest_tuning` | function | `modules/closedloop.py:136` | `def suggest_tuning(candidate, baseline)` |
| `to_dict` | method | `modules/closedloop.py:42` | `def to_dict(self)` |
| `to_dict` | method | `modules/closedloop.py:66` | `def to_dict(self)` |
| `CloudEnumerator` | class | `modules/cloud_enum.py:23` | `class CloudEnumerator` |
| `__init__` | method | `modules/cloud_enum.py:34` | `def __init__(self, provider, session, timeout)` |
| `_check_aws_privesc` | method | `modules/cloud_enum.py:526` | `def _check_aws_privesc(data)` |
| `_enumerate_aws_iam` | method | `modules/cloud_enum.py:390` | `def _enumerate_aws_iam(self)` |
| `_enumerate_aws_metadata` | method | `modules/cloud_enum.py:96` | `def _enumerate_aws_metadata(self)` |
| `_enumerate_azure_iam` | method | `modules/cloud_enum.py:421` | `def _enumerate_azure_iam(self)` |
| `_enumerate_azure_metadata` | method | `modules/cloud_enum.py:146` | `def _enumerate_azure_metadata(self)` |
| `_enumerate_azure_storage` | method | `modules/cloud_enum.py:316` | `def _enumerate_azure_storage(self, target_bucket)` |
| `_enumerate_gcp_iam` | method | `modules/cloud_enum.py:477` | `def _enumerate_gcp_iam(self)` |
| `_enumerate_gcp_metadata` | method | `modules/cloud_enum.py:193` | `def _enumerate_gcp_metadata(self)` |
| `_enumerate_gcs` | method | `modules/cloud_enum.py:350` | `def _enumerate_gcs(self, target_bucket)` |
| `_enumerate_s3` | method | `modules/cloud_enum.py:274` | `def _enumerate_s3(self, target_bucket)` |
| `detect_provider` | method | `modules/cloud_enum.py:47` | `def detect_provider(self)` |
| `enumerate_iam` | method | `modules/cloud_enum.py:372` | `def enumerate_iam(self)` |
| `enumerate_metadata` | method | `modules/cloud_enum.py:75` | `def enumerate_metadata(self)` |
| `enumerate_storage` | method | `modules/cloud_enum.py:251` | `def enumerate_storage(self, target_bucket)` |
| `full_enumeration` | method | `modules/cloud_enum.py:576` | `def full_enumeration(self)` |
| `ColabEvent` | class | `modules/collab_bp.py:163` | `class ColabEvent` |
| `EventBus` | class | `modules/collab_bp.py:188` | `class EventBus` |
| `LockManager` | class | `modules/collab_bp.py:257` | `class LockManager` |
| `OperatorInfo` | class | `modules/collab_bp.py:176` | `class OperatorInfo` |
| `OperatorRegistry` | class | `modules/collab_bp.py:314` | `class OperatorRegistry` |
| `TargetLock` | class | `modules/collab_bp.py:250` | `class TargetLock` |
| `__init__` | method | `modules/collab_bp.py:198` | `def __init__(self)` |
| `__init__` | method | `modules/collab_bp.py:263` | `def __init__(self)` |
| `__init__` | method | `modules/collab_bp.py:319` | `def __init__(self)` |
| `_authenticated_operator` | function | `modules/collab_bp.py:90` | `def _authenticated_operator()` |
| `_check_collab_permission` | function | `modules/collab_bp.py:100` | `def _check_collab_permission(perm_name)` |
| `_collab_login_required` | function | `modules/collab_bp.py:120` | `def _collab_login_required(f)` |
| `_collab_permission_required` | function | `modules/collab_bp.py:136` | `def _collab_permission_required(perm_name)` |
| `_expire` | method | `modules/collab_bp.py:297` | `def _expire(self)` |
| `_expire` | method | `modules/collab_bp.py:350` | `def _expire(self)` |
| `acquire` | method | `modules/collab_bp.py:267` | `def acquire(self, target, operator, ttl_secs)` |
| `active_operators` | method | `modules/collab_bp.py:345` | `def active_operators(self)` |
| `all_locks` | method | `modules/collab_bp.py:292` | `def all_locks(self)` |
| `collab_ui` | function | `modules/collab_bp.py:396` | `def collab_ui()` |
| `decorated` | function | `modules/collab_bp.py:84` | `def decorated()` |
| `decorated` | function | `modules/collab_bp.py:124` | `def decorated()` |
| `decorated` | function | `modules/collab_bp.py:141` | `def decorated()` |
| `decorator` | function | `modules/collab_bp.py:139` | `def decorator(f)` |
| `generate` | function | `modules/collab_bp.py:424` | `def generate()` |
| `get_event_bus` | function | `modules/collab_bp.py:370` | `def get_event_bus()` |
| `get_lock_manager` | function | `modules/collab_bp.py:374` | `def get_lock_manager()` |
| `get_operator_registry` | function | `modules/collab_bp.py:378` | `def get_operator_registry()` |
| `heartbeat` | method | `modules/collab_bp.py:334` | `def heartbeat(self, name)` |
| `history` | function | `modules/collab_bp.py:537` | `def history()` |
| `join` | method | `modules/collab_bp.py:323` | `def join(self, name)` |
| `leave` | method | `modules/collab_bp.py:340` | `def leave(self, name)` |
| `lock` | function | `modules/collab_bp.py:483` | `def lock()` |
| `locks` | function | `modules/collab_bp.py:522` | `def locks()` |
| `login_required` | function | `modules/collab_bp.py:80` | `def login_required(f)` |
| `operators` | function | `modules/collab_bp.py:458` | `def operators()` |
| `publish` | method | `modules/collab_bp.py:219` | `def publish(self, event)` |
| `publish` | function | `modules/collab_bp.py:470` | `def publish()` |
| `publish_event` | function | `modules/collab_bp.py:382` | `def publish_event(type, payload, operator)` |
| `recent` | method | `modules/collab_bp.py:234` | `def recent(self, n)` |
| `release` | method | `modules/collab_bp.py:279` | `def release(self, target, operator)` |
| `reset` | method | `modules/collab_bp.py:238` | `def reset(self)` |
| `reset` | method | `modules/collab_bp.py:304` | `def reset(self)` |
| `reset` | method | `modules/collab_bp.py:356` | `def reset(self)` |
| `status` | method | `modules/collab_bp.py:287` | `def status(self, target)` |
| `stream` | function | `modules/collab_bp.py:411` | `def stream()` |
| `subscribe` | method | `modules/collab_bp.py:203` | `def subscribe(self, subscriber_id)` |
| `to_sse` | method | `modules/collab_bp.py:170` | `def to_sse(self)` |
| `unlock` | function | `modules/collab_bp.py:504` | `def unlock()` |
| `unsubscribe` | method | `modules/collab_bp.py:215` | `def unsubscribe(self, subscriber_id)` |
| `delete_lines` | function | `modules/colors.py:68` | `def delete_lines(content, to_delete)` |
| `no_html` | function | `modules/colors.py:74` | `def no_html(content)` |
| `retModel` | function | `modules/colors.py:40` | `def retModel()` |
| `CommandExecutor` | class | `modules/command_executor.py:106` | `class CommandExecutor` |
| `ExecutionResult` | class | `modules/command_executor.py:97` | `class ExecutionResult` |
| `__init__` | method | `modules/command_executor.py:118` | `def __init__(self)` |
| `_argv` | method | `modules/command_executor.py:173` | `def _argv(self, command)` |
| `_default_writer` | method | `modules/command_executor.py:291` | `def _default_writer(line)` |
| `_fire_hooks` | method | `modules/command_executor.py:394` | `def _fire_hooks(self, result)` |
| `_kill_process_group` | function | `modules/command_executor.py:77` | `def _kill_process_group(proc)` |
| `_needs_shell` | method | `modules/command_executor.py:165` | `def _needs_shell(self, command)` |
| `_publish_event` | method | `modules/command_executor.py:401` | `def _publish_event(self, result)` |
| `_run_capture` | method | `modules/command_executor.py:296` | `def _run_capture(self, command, timeout)` |
| `_run_stream` | method | `modules/command_executor.py:321` | `def _run_stream(self, command, timeout)` |
| `add_hook` | method | `modules/command_executor.py:127` | `def add_hook(self, hook)` |
| `clear_thread_stdin_devnull` | function | `modules/command_executor.py:64` | `def clear_thread_stdin_devnull()` |
| `clear_thread_timeout` | function | `modules/command_executor.py:46` | `def clear_thread_timeout()` |
| `get_executor` | function | `modules/command_executor.py:426` | `def get_executor()` |
| `instance` | method | `modules/command_executor.py:122` | `def instance(cls)` |
| `run` | method | `modules/command_executor.py:131` | `def run(self, command, timeout, stream)` |
| `run_passthrough` | method | `modules/command_executor.py:179` | `def run_passthrough(self, command, env)` |
| `run_tee` | method | `modules/command_executor.py:194` | `def run_tee(self, command)` |
| `run_with_tee` | method | `modules/command_executor.py:358` | `def run_with_tee(self, command, output_path, timeout)` |
| `set_thread_stdin_devnull` | function | `modules/command_executor.py:59` | `def set_thread_stdin_devnull(enabled)` |
| `set_thread_timeout` | function | `modules/command_executor.py:41` | `def set_thread_timeout(seconds)` |
| `thread_stdin_devnull` | function | `modules/command_executor.py:72` | `def thread_stdin_devnull()` |
| `thread_timeout` | function | `modules/command_executor.py:54` | `def thread_timeout()` |
| `ComplianceEngine` | class | `modules/compliance.py:632` | `class ComplianceEngine` |
| `ComplianceFinding` | class | `modules/compliance.py:620` | `class ComplianceFinding` |
| `EvidenceChain` | class | `modules/compliance.py:349` | `class EvidenceChain` |
| `EvidenceEntry` | class | `modules/compliance.py:340` | `class EvidenceEntry` |
| `__init__` | method | `modules/compliance.py:357` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/compliance.py:635` | `def __init__(self, sessions_dir)` |
| `_append_to_file` | method | `modules/compliance.py:403` | `def _append_to_file(self, entry)` |
| `_compliance_finding` | method | `modules/compliance.py:780` | `def _compliance_finding(fact)` |
| `_count_by_category` | method | `modules/compliance.py:772` | `def _count_by_category(self, findings)` |
| `_count_by_severity` | method | `modules/compliance.py:765` | `def _count_by_severity(self, findings)` |
| `_format_compliance_report_md` | method | `modules/compliance.py:861` | `def _format_compliance_report_md(self, report)` |
| `_hash_entry` | method | `modules/compliance.py:379` | `def _hash_entry(self, entry)` |
| `_load` | method | `modules/compliance.py:364` | `def _load(self)` |
| `_load_findings` | method | `modules/compliance.py:808` | `def _load_findings(self)` |
| `add_evidence` | method | `modules/compliance.py:927` | `def add_evidence(self, filepath, operator, description)` |
| `add_file` | method | `modules/compliance.py:383` | `def add_file(self, filepath, operator, description)` |
| `export_pdf` | function | `modules/compliance.py:449` | `def export_pdf(report_md, output_path, title, classification)` |
| `export_pdf` | method | `modules/compliance.py:857` | `def export_pdf(self, report, output_path)` |
| `export_to_cef` | function | `modules/compliance.py:572` | `def export_to_cef(findings, output_path, vendor, product, version)` |
| `export_to_elastic_ndjson` | function | `modules/compliance.py:533` | `def export_to_elastic_ndjson(findings, output_path, index_prefix)` |
| `generate_compliance_report` | method | `modules/compliance.py:710` | `def generate_compliance_report(self, findings, include_evidence_chain, include_siem_formats)` |

Next: [SYMBOLS_p13.md](SYMBOLS_p13.md)
