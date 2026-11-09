# Symbols (page 12 of 50)
Previous: [SYMBOLS_p11.md](SYMBOLS_p11.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_match_privesc_techniques` | method | `modules/autonomous_exploit_engine.py:2188` | `def _match_privesc_techniques(self, findings, os_type)` |
| `_match_service_banners` | method | `modules/autonomous_exploit_engine.py:1842` | `def _match_service_banners(self, profile)` |
| `_parse_nse_output` | method | `modules/autonomous_exploit_engine.py:1759` | `def _parse_nse_output(self, target_ip)` |
| `_register_session` | method | `modules/autonomous_exploit_engine.py:1471` | `def _register_session(self, ip, output)` |
| `_resolve_port` | method | `modules/autonomous_exploit_engine.py:1159` | `def _resolve_port(self, candidate, profile)` |
| `_run_exploit` | method | `modules/autonomous_exploit_engine.py:1113` | `def _run_exploit(self, candidate, profile)` |
| `_run_linux_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2076` | `def _run_linux_privesc_checks(self, profile, session_id)` |
| `_run_windows_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2145` | `def _run_windows_privesc_checks(self, profile, session_id)` |
| `_scorer` | method | `modules/autonomous_exploit_engine.py:1073` | `def _scorer(self, exploit, service, product, version)` |
| `chain_privesc` | method | `modules/autonomous_exploit_engine.py:2048` | `def chain_privesc(self, profile, session_id)` |
| `enable_stealth` | method | `modules/autonomous_exploit_engine.py:2604` | `def enable_stealth(self, stealth_level)` |
| `execute_candidate` | method | `modules/autonomous_exploit_engine.py:412` | `def execute_candidate(self, candidate, profile)` |
| `full_auto_pwn` | method | `modules/autonomous_exploit_engine.py:2668` | `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth)` |
| `get_instance` | method | `modules/autonomous_exploit_engine.py:134` | `def get_instance(cls)` |
| `hunt` | method | `modules/autonomous_exploit_engine.py:145` | `def hunt(self, target, max_exploits, profile)` |
| `profile` | method | `modules/autonomous_exploit_engine.py:328` | `def profile(self, target)` |
| `rank_exploits` | method | `modules/autonomous_exploit_engine.py:389` | `def rank_exploits(self, profile)` |
| `retry_with_credentials` | method | `modules/autonomous_exploit_engine.py:184` | `def retry_with_credentials(self, target, credentials)` |
| `scan_vulnerabilities` | method | `modules/autonomous_exploit_engine.py:1733` | `def scan_vulnerabilities(self, profile)` |
| `trigger_pivot` | method | `modules/autonomous_exploit_engine.py:2478` | `def trigger_pivot(self, profile, session_id)` |
| `AWSAttackEngine` | class | `modules/aws_attacks.py:80` | `class AWSAttackEngine` |
| `AWSConfig` | class | `modules/aws_attacks.py:58` | `class AWSConfig` |
| `__init__` | method | `modules/aws_attacks.py:91` | `def __init__(self, config)` |
| `cloudformation_drift` | method | `modules/aws_attacks.py:242` | `def cloudformation_drift(self)` |
| `ec2_ssm_session_abuse` | method | `modules/aws_attacks.py:274` | `def ec2_ssm_session_abuse(self)` |
| `ec2_user_data_exfil` | method | `modules/aws_attacks.py:181` | `def ec2_user_data_exfil(self)` |
| `enumerate_iam_permissions` | method | `modules/aws_attacks.py:95` | `def enumerate_iam_permissions(self)` |
| `lambda_backdoor` | method | `modules/aws_attacks.py:127` | `def lambda_backdoor(self, function_name)` |
| `s3_enumeration` | method | `modules/aws_attacks.py:206` | `def s3_enumeration(self)` |
| `sts_role_chain` | method | `modules/aws_attacks.py:155` | `def sts_role_chain(self, target_role_arn)` |
| `summary` | method | `modules/aws_attacks.py:293` | `def summary(self)` |
| `RUNKEY_NAME` | macro | `modules/backdoor/backdoor.c:17` | `#define RUNKEY_NAME` |
| `Shell` | function | `modules/backdoor/backdoor.c:88` | `void Shell()` |
| `WinMain` | function | `modules/backdoor/backdoor.c:129` | `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)` |
| `bootRun` | function | `modules/backdoor/backdoor.c:22` | `int bootRun()` |
| `bzero` | macro | `modules/backdoor/backdoor.c:14` | `#define bzero(p, size)` |
| `str_cut` | function | `modules/backdoor/backdoor.c:53` | `char * str_cut(char str[], int slice_from, int slice_to)` |
| `logg` | function | `modules/backdoor/keylogger.h:1` | `DWORD WINAPI logg(LPVOID lpParam)` |
| `main` | function | `modules/backdoor/server.c:10` | `int main()` |
| `BeaconConfig` | class | `modules/beacon_config_builder.py:44` | `class BeaconConfig` |
| `BeaconConfigBuilder` | class | `modules/beacon_config_builder.py:237` | `class BeaconConfigBuilder` |
| `__init__` | method | `modules/beacon_config_builder.py:245` | `def __init__(self, payload)` |
| `_inject_profile_engine` | method | `modules/beacon_config_builder.py:318` | `def _inject_profile_engine(self, config)` |
| `_inject_sleep_engine` | method | `modules/beacon_config_builder.py:366` | `def _inject_sleep_engine(self, config)` |
| `_inject_socks_engine` | method | `modules/beacon_config_builder.py:385` | `def _inject_socks_engine(self, config)` |
| `build` | method | `modules/beacon_config_builder.py:248` | `def build(self, name)` |
| `from_payload` | method | `modules/beacon_config_builder.py:403` | `def from_payload(cls, payload)` |
| `from_payload_file` | method | `modules/beacon_config_builder.py:408` | `def from_payload_file(cls, path)` |
| `generate_bof_execution_command` | function | `modules/beacon_config_builder.py:416` | `def generate_bof_execution_command(bof_name, c2_url, client_id, args, bofs_dir)` |
| `to_config_json` | method | `modules/beacon_config_builder.py:160` | `def to_config_json(self)` |
| `to_dict` | method | `modules/beacon_config_builder.py:185` | `def to_dict(self)` |
| `to_gen_beacon_args` | method | `modules/beacon_config_builder.py:117` | `def to_gen_beacon_args(self)` |
| `to_go_implant_vars` | method | `modules/beacon_config_builder.py:137` | `def to_go_implant_vars(self)` |
| `BeaconHistoryConfig` | class | `modules/beacon_history.py:28` | `class BeaconHistoryConfig` |
| `append_record` | function | `modules/beacon_history.py:82` | `def append_record(record, config)` |
| `read_records` | function | `modules/beacon_history.py:116` | `def read_records(client_id, config)` |
| `records_path` | method | `modules/beacon_history.py:43` | `def records_path(self, client_id)` |
| `records_path` | function | `modules/beacon_history.py:145` | `def records_path(client_id, config)` |
| `sanitize_client_id` | function | `modules/beacon_history.py:70` | `def sanitize_client_id(client_id)` |
| `sessions_dir` | method | `modules/beacon_history.py:39` | `def sessions_dir(self)` |
| `_append_discovery_ledger` | function | `modules/beacon_recon.py:264` | `def _append_discovery_ledger(primary_ip, discovered, sessions_dir)` |
| `_looks_like_ip` | function | `modules/beacon_recon.py:42` | `def _looks_like_ip(value)` |
| `_ports_from` | function | `modules/beacon_recon.py:111` | `def _ports_from(value)` |
| `ingest_beacon_recon` | function | `modules/beacon_recon.py:169` | `def ingest_beacon_recon(primary_ip, discovered_ips, portscan, hostname, user, client_id, sessions_dir)` |
| `parse_beacon_portscan` | function | `modules/beacon_recon.py:94` | `def parse_beacon_portscan(raw, default_host)` |
| `parse_discovered_ips` | function | `modules/beacon_recon.py:50` | `def parse_discovered_ips(raw)` |
| `binario_a_imagen` | function | `modules/bin2img.py:7` | `def binario_a_imagen(binario, imagen_input, imagen_output, block_size)` |
| `main` | function | `modules/bin2img.py:54` | `def main()` |
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
| `ChainStepBlocked` | class | `modules/chain_loop.py:138` | `class ChainStepBlocked(RuntimeError)` |
| `__init__` | method | `modules/chain_loop.py:141` | `def __init__(self, status, detail)` |
| `_build_runner` | function | `modules/chain_loop.py:270` | `def _build_runner(chain, guarded, tokens, total_timeout, run_id, worker, intent)` |
| `_render_summary` | function | `modules/chain_loop.py:313` | `def _render_summary(result, chain_name)` |
| `_spool` | function | `modules/chain_loop.py:303` | `def _spool(result)` |
| `chain_mode` | function | `modules/chain_loop.py:34` | `def chain_mode()` |
| `guarded` | function | `modules/chain_loop.py:225` | `def guarded(step_command)` |
| `is_chain_command` | function | `modules/chain_loop.py:52` | `def is_chain_command(command)` |
| `on_step` | function | `modules/chain_loop.py:282` | `def on_step(outcome)` |
| `parse_chain_invocation` | function | `modules/chain_loop.py:57` | `def parse_chain_invocation(command)` |
| `run_chain_stepwise` | function | `modules/chain_loop.py:153` | `def run_chain_stepwise(worker, intent, command, executor, budget, intercept, retry_state)` |
| `stepwise_eligible` | function | `modules/chain_loop.py:108` | `def stepwise_eligible(chain, routable)` |
| `best_chain` | function | `modules/chain_match.py:139` | `def best_chain(phase, os_hint, services, exclude, allow_lab, rows, ttl)` |
| `load_rows` | function | `modules/chain_match.py:109` | `def load_rows(allow_lab, ttl)` |
| `normalize_tags` | function | `modules/chain_match.py:49` | `def normalize_tags(tags)` |
| `platform_ok` | function | `modules/chain_match.py:75` | `def platform_ok(platforms, os_hint)` |
| `reset_cache` | function | `modules/chain_match.py:101` | `def reset_cache()` |
| `score` | function | `modules/chain_match.py:86` | `def score(tags, phase, svc_tokens)` |
| `service_tokens` | function | `modules/chain_match.py:65` | `def service_tokens(services)` |
| `Chain` | class | `modules/chain_registry.py:158` | `class Chain` |
| `ChainStep` | class | `modules/chain_registry.py:104` | `class ChainStep` |
| `_eval` | function | `modules/chain_registry.py:319` | `def _eval(node)` |
| `_materialize` | function | `modules/chain_registry.py:625` | `def _materialize(name, raw, stack)` |
| `_nonneg_float` | function | `modules/chain_registry.py:681` | `def _nonneg_float(raw, ceiling)` |
| `_nonneg_int` | function | `modules/chain_registry.py:672` | `def _nonneg_int(raw)` |
| `_render` | function | `modules/chain_registry.py:241` | `def _render(template, variables)` |
| `_step_from_raw` | function | `modules/chain_registry.py:692` | `def _step_from_raw(item)` |
| `_when_tree` | function | `modules/chain_registry.py:270` | `def _when_tree(expression)` |
| `evaluate_when` | function | `modules/chain_registry.py:297` | `def evaluate_when(expression, variables)` |
| `generate_for_playbook` | function | `modules/chain_registry.py:837` | `def generate_for_playbook(engine_key, apt_display, description, chains_dir, overwrite)` |
| `get` | function | `modules/chain_registry.py:749` | `def get(name, chains_dir)` |
| `identifier` | method | `modules/chain_registry.py:152` | `def identifier(self)` |
| `load_all` | function | `modules/chain_registry.py:591` | `def load_all(chains_dir)` |
| `render_text_token_braces` | function | `modules/chain_registry.py:586` | `def render_text_token_braces(text)` |
| `resolve` | method | `modules/chain_registry.py:176` | `def resolve(self, tokens)` |
| `scan_all` | function | `modules/chain_registry.py:754` | `def scan_all(chains_dir)` |
| `set_enabled` | function | `modules/chain_registry.py:814` | `def set_enabled(name, enabled, chains_dir)` |
| `skip_pending` | function | `modules/chain_registry.py:69` | `def skip_pending(path, max_age, now)` |
| `validate_chain` | function | `modules/chain_registry.py:362` | `def validate_chain(data, filename, chains_dir)` |
| `ChainRunResult` | class | `modules/chain_runner.py:112` | `class ChainRunResult` |
| `ChainRunner` | class | `modules/chain_runner.py:220` | `class ChainRunner` |
| `ReplanContext` | class | `modules/chain_runner.py:165` | `class ReplanContext` |
| `StepOutcome` | class | `modules/chain_runner.py:56` | `class StepOutcome` |
| `__init__` | method | `modules/chain_runner.py:223` | `def __init__(self, chain, tokens, shell, executor, default_timeout, dry_run, on_step, retry_backoff, total_timeout...` |
| `_all_json_objects` | function | `modules/chain_runner.py:1431` | `def _all_json_objects(text)` |
| `_apply_replanner` | method | `modules/chain_runner.py:884` | `def _apply_replanner(self, result, index, outcome, steps, step_index, variables, captured_keys)` |
| `_ask_approval` | method | `modules/chain_runner.py:1183` | `def _ask_approval(self, step_id, command)` |
| `_call` | method | `modules/chain_runner.py:1411` | `def _call(callback, timeout)` |
| `_deliver` | method | `modules/chain_runner.py:745` | `def _deliver(self, outcome)` |
| `_dependency_block` | method | `modules/chain_runner.py:1116` | `def _dependency_block(step, prior_verdicts)` |
| `_execute` | method | `modules/chain_runner.py:1293` | `def _execute(self, command, timeout, expect_exits)` |
| `_finalize_verdict` | method | `modules/chain_runner.py:528` | `def _finalize_verdict(self, result)` |
| `_first_json` | method | `modules/chain_runner.py:1254` | `def _first_json(output)` |
| `_is_verb` | method | `modules/chain_runner.py:1328` | `def _is_verb(self, command)` |
| `_load_json_events` | function | `modules/chain_runner.py:1452` | `def _load_json_events(path)` |
| `_notify` | method | `modules/chain_runner.py:875` | `def _notify(self, outcome)` |
| `_pace_after` | method | `modules/chain_runner.py:309` | `def _pace_after(self, outcome, started, step)` |
| `_pre_check_timeout` | method | `modules/chain_runner.py:1198` | `def _pre_check_timeout(self, step)` |
| `_promoted_sinks` | method | `modules/chain_runner.py:750` | `def _promoted_sinks(self, outcome)` |
| `_publish_step` | method | `modules/chain_runner.py:775` | `def _publish_step(self, outcome)` |
| `_raise_timeout` | function | `modules/chain_runner.py:1374` | `def _raise_timeout(_signum, _frame)` |
| `_record_verdict` | method | `modules/chain_runner.py:971` | `def _record_verdict(verdicts, outcome)` |
| `_render_command` | method | `modules/chain_runner.py:1268` | `def _render_command(self, template, variables, captured_keys)` |
| `_run_fallback_chain` | method | `modules/chain_runner.py:674` | `def _run_fallback_chain(self, result, variables, captured_keys, started)` |
| `_run_parallel_group` | method | `modules/chain_runner.py:580` | `def _run_parallel_group(self, group, executions, resumed_ok, variables, captured_keys, prior_verdicts)` |
| `_run_raw` | method | `modules/chain_runner.py:1394` | `def _run_raw(self, command, timeout, allowed)` |
| `_run_shell_verb` | method | `modules/chain_runner.py:1339` | `def _run_shell_verb(self, command, timeout)` |
| `_run_step` | method | `modules/chain_runner.py:978` | `def _run_step(self, step, variables, captured_keys, prior_verdicts)` |
| `_save_checkpoint` | method | `modules/chain_runner.py:933` | `def _save_checkpoint(self, result, variables, captured_keys, next_index, state_name, verdicts)` |
| `_skip_remaining` | method | `modules/chain_runner.py:565` | `def _skip_remaining(self, steps, start, reason)` |
| `_store_capture` | method | `modules/chain_runner.py:1202` | `def _store_capture(self, step, output, outcome, variables, captured_keys)` |
| `_verify_evidence` | method | `modules/chain_runner.py:1138` | `def _verify_evidence(self, step, outcome, variables)` |
| `_verify_timeout` | method | `modules/chain_runner.py:1192` | `def _verify_timeout(self, step)` |
| `applied_vars` | method | `modules/chain_runner.py:197` | `def applied_vars(self)` |
| `chain_proven` | method | `modules/chain_runner.py:159` | `def chain_proven(self)` |
| `insert_step` | method | `modules/chain_runner.py:187` | `def insert_step(self, step)` |
| `inserted` | method | `modules/chain_runner.py:202` | `def inserted(self)` |
| `ok` | method | `modules/chain_runner.py:84` | `def ok(self)` |
| `render_text` | function | `modules/chain_runner.py:212` | `def render_text(template, variables)` |
| `run` | method | `modules/chain_runner.py:348` | `def run(self)` |
| `set_var` | method | `modules/chain_runner.py:182` | `def set_var(self, name, value)` |
| `skip_rest` | method | `modules/chain_runner.py:192` | `def skip_rest(self)` |
| `skip_rest_flag` | method | `modules/chain_runner.py:207` | `def skip_rest_flag(self)` |
| `to_dict` | method | `modules/chain_runner.py:88` | `def to_dict(self)` |
| `to_dict` | method | `modules/chain_runner.py:134` | `def to_dict(self)` |
| `checkpoint_dir` | function | `modules/chain_state.py:26` | `def checkpoint_dir(base_dir)` |
| `list_checkpoints` | function | `modules/chain_state.py:80` | `def list_checkpoints(directory, limit, chain)` |
| `load_checkpoint` | function | `modules/chain_state.py:65` | `def load_checkpoint(directory, run_id)` |
| `new_run_id` | function | `modules/chain_state.py:33` | `def new_run_id(chain_name)` |
| `write_checkpoint` | function | `modules/chain_state.py:39` | `def write_checkpoint(directory, state)` |
| `_service_steps` | function | `modules/chain_synth.py:44` | `def _service_steps(host, services)` |
| `_slug` | function | `modules/chain_synth.py:31` | `def _slug(name)` |
| `_wordlist` | function | `modules/chain_synth.py:35` | `def _wordlist(param, fallback)` |
| `facts_for_target` | function | `modules/chain_synth.py:243` | `def facts_for_target(target)` |
| `synth_chain_data` | function | `modules/chain_synth.py:91` | `def synth_chain_data(playbook, target, services, has_creds, os_hint, include_c2, techniques)` |
| `synth_technique_chain_data` | function | `modules/chain_synth.py:272` | `def synth_technique_chain_data(target, techniques, os_hint)` |
| `write_generated_chain` | function | `modules/chain_synth.py:339` | `def write_generated_chain(data, chains_dir)` |
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

Next: [SYMBOLS_p13.md](SYMBOLS_p13.md)
