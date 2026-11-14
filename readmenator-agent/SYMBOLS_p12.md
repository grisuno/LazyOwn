# Symbols (page 12 of 52)
Previous: [SYMBOLS_p11.md](SYMBOLS_p11.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `PurpleTeamLoop` | class | `modules/auto_purple.py:407` | `class PurpleTeamLoop(IPurpleLoop, IPurpleEvaluator)` |
| `__init__` | method | `modules/auto_purple.py:414` | `def __init__(self, bt_path, detection_delay, methods, auto_feedback, session_id)` |
| `_append_dataset` | method | `modules/auto_purple.py:698` | `def _append_dataset(self, result)` |
| `_compute_oracle_accuracy` | method | `modules/auto_purple.py:739` | `def _compute_oracle_accuracy(self)` |
| `_execute_red` | method | `modules/auto_purple.py:614` | `def _execute_red(self, command, args)` |
| `_get_detection_methods` | method | `modules/auto_purple.py:759` | `def _get_detection_methods(self)` |
| `_hash_output` | method | `modules/auto_purple.py:687` | `def _hash_output(self, output)` |
| `_init_dataset` | method | `modules/auto_purple.py:433` | `def _init_dataset(self)` |
| `_load_audit` | method | `modules/auto_purple.py:724` | `def _load_audit(self)` |
| `_parse_ai_test` | function | `modules/auto_purple.py:329` | `def _parse_ai_test(output, command, args)` |
| `_parse_alert_check` | function | `modules/auto_purple.py:374` | `def _parse_alert_check(output, command, args)` |
| `_parse_fim_check` | function | `modules/auto_purple.py:388` | `def _parse_fim_check(output, command, args)` |
| `_parse_keyword_match` | function | `modules/auto_purple.py:342` | `def _parse_keyword_match(output, command, args)` |
| `_query_blue` | method | `modules/auto_purple.py:635` | `def _query_blue(self, command, args)` |
| `_run_bt_command` | function | `modules/auto_purple.py:225` | `def _run_bt_command(bt_path, command, timeout)` |
| `_write_audit` | method | `modules/auto_purple.py:693` | `def _write_audit(self, result)` |
| `_write_feedback` | method | `modules/auto_purple.py:704` | `def _write_feedback(self, result)` |
| `category_accuracy` | method | `modules/auto_purple.py:217` | `def category_accuracy(self, category)` |
| `category_accuracy` | method | `modules/auto_purple.py:599` | `def category_accuracy(self, category)` |
| `engagement_score` | method | `modules/auto_purple.py:201` | `def engagement_score(self)` |
| `engagement_score` | method | `modules/auto_purple.py:529` | `def engagement_score(self)` |
| `execute_and_measure` | method | `modules/auto_purple.py:185` | `def execute_and_measure(self, command, args, category)` |
| `execute_and_measure` | method | `modules/auto_purple.py:443` | `def execute_and_measure(self, command, args, category)` |
| `export_dataset` | method | `modules/auto_purple.py:204` | `def export_dataset(self)` |
| `export_dataset` | method | `modules/auto_purple.py:567` | `def export_dataset(self)` |
| `export_report` | method | `modules/auto_purple.py:207` | `def export_report(self)` |
| `export_report` | method | `modules/auto_purple.py:571` | `def export_report(self)` |
| `get_loop` | function | `modules/auto_purple.py:772` | `def get_loop(bt_path, detection_delay, methods, auto_feedback)` |
| `last_results` | method | `modules/auto_purple.py:214` | `def last_results(self, n)` |
| `last_results` | method | `modules/auto_purple.py:596` | `def last_results(self, n)` |
| `load_config_from_payload` | function | `modules/auto_purple.py:790` | `def load_config_from_payload(params)` |
| `measure_only` | method | `modules/auto_purple.py:193` | `def measure_only(self, command, args, category)` |
| `measure_only` | method | `modules/auto_purple.py:493` | `def measure_only(self, command, args, category)` |
| `to_csv_row` | method | `modules/auto_purple.py:146` | `def to_csv_row(self)` |
| `to_dict` | method | `modules/auto_purple.py:160` | `def to_dict(self)` |
| `AutoVerb` | class | `modules/auto_registry.py:95` | `class AutoVerb` |
| `ShellResult` | class | `modules/auto_registry.py:1017` | `class ShellResult` |
| `_TeeCapture` | class | `modules/auto_registry.py:1024` | `class _TeeCapture(StringIO)` |
| `__init__` | method | `modules/auto_registry.py:1034` | `def __init__(self, observer)` |
| `_apt_chain_steps` | function | `modules/auto_registry.py:797` | `def _apt_chain_steps(embedded, target, strict)` |
| `_atomic_steps` | function | `modules/auto_registry.py:763` | `def _atomic_steps(verb, text)` |
| `_chain_name_for_playbook` | function | `modules/auto_registry.py:826` | `def _chain_name_for_playbook(playbook)` |
| `_cli_verb_allowed` | function | `modules/auto_registry.py:427` | `def _cli_verb_allowed(name)` |
| `_exploitdb_steps` | function | `modules/auto_registry.py:1303` | `def _exploitdb_steps(embedded, target)` |
| `_invoke` | function | `modules/auto_registry.py:1075` | `def _invoke()` |
| `_kill` | function | `modules/auto_registry.py:1227` | `def _kill()` |
| `_looks_like_target` | function | `modules/auto_registry.py:38` | `def _looks_like_target(value)` |
| `_os_default_for_verb` | function | `modules/auto_registry.py:278` | `def _os_default_for_verb(verb)` |
| `_parse_trigger_lines` | function | `modules/auto_registry.py:514` | `def _parse_trigger_lines(lines, start)` |
| `_playbook_steps` | function | `modules/auto_registry.py:782` | `def _playbook_steps(text)` |
| `_register_process` | function | `modules/auto_registry.py:1150` | `def _register_process(process)` |
| `_repo_base` | function | `modules/auto_registry.py:451` | `def _repo_base()` |
| `_target` | function | `modules/auto_registry.py:1086` | `def _target()` |
| `_unregister_process` | function | `modules/auto_registry.py:1156` | `def _unregister_process(process)` |
| `_verb_row` | function | `modules/auto_registry.py:331` | `def _verb_row(name)` |
| `_verb_rows` | function | `modules/auto_registry.py:286` | `def _verb_rows()` |
| `addon_hits_for` | function | `modules/auto_registry.py:604` | `def addon_hits_for(service_text, limit)` |
| `auto_verb_target` | function | `modules/auto_registry.py:55` | `def auto_verb_target(command)` |
| `binary_available` | function | `modules/auto_registry.py:458` | `def binary_available(name)` |
| `build_command` | function | `modules/auto_registry.py:721` | `def build_command(verb, target)` |
| `cancel_running_commands` | function | `modules/auto_registry.py:1172` | `def cancel_running_commands()` |
| `execute_shell_verb` | function | `modules/auto_registry.py:1052` | `def execute_shell_verb(shell, command, timeout_sec, on_output)` |
| `execute_streaming` | function | `modules/auto_registry.py:1195` | `def execute_streaming(command, on_output, timeout_sec)` |
| `is_routable_command` | function | `modules/auto_registry.py:674` | `def is_routable_command(line)` |
| `is_shell_verb` | function | `modules/auto_registry.py:697` | `def is_shell_verb(token)` |
| `iter_addon_triggers` | function | `modules/auto_registry.py:545` | `def iter_addon_triggers()` |
| `iter_tool_triggers` | function | `modules/auto_registry.py:581` | `def iter_tool_triggers()` |
| `missing_binary` | function | `modules/auto_registry.py:474` | `def missing_binary(command)` |
| `propose_addon_intents` | function | `modules/auto_registry.py:630` | `def propose_addon_intents(service_texts, target, limit)` |
| `propose_intents` | function | `modules/auto_registry.py:738` | `def propose_intents(goal, target, finding_texts)` |
| `service_tokens` | function | `modules/auto_registry.py:503` | `def service_tokens(service_text)` |
| `steps_for` | function | `modules/auto_registry.py:859` | `def steps_for(text, target)` |
| `track_process` | function | `modules/auto_registry.py:1162` | `def track_process(process)` |
| `untrack_process` | function | `modules/auto_registry.py:1167` | `def untrack_process(process)` |
| `verb_available` | function | `modules/auto_registry.py:498` | `def verb_available(verb)` |
| `verb_enabled` | function | `modules/auto_registry.py:340` | `def verb_enabled(name)` |
| `verb_gap` | function | `modules/auto_registry.py:486` | `def verb_gap(verb)` |
| `verbs` | function | `modules/auto_registry.py:692` | `def verbs()` |
| `verbs_for` | function | `modules/auto_registry.py:732` | `def verbs_for(text)` |
| `write` | method | `modules/auto_registry.py:1039` | `def write(self, data)` |
| `AutonomousExploitEngine` | class | `modules/autonomous_exploit_engine.py:101` | `class AutonomousExploitEngine` |
| `ExploitCandidate` | class | `modules/autonomous_exploit_engine.py:74` | `class ExploitCandidate` |
| `ExploitResult` | class | `modules/autonomous_exploit_engine.py:89` | `class ExploitResult` |
| `TargetProfile` | class | `modules/autonomous_exploit_engine.py:59` | `class TargetProfile` |
| `__init__` | method | `modules/autonomous_exploit_engine.py:114` | `def __init__(self)` |
| `_apply_stealth_delay` | method | `modules/autonomous_exploit_engine.py:1679` | `def _apply_stealth_delay(self)` |
| `_build_command_chain` | method | `modules/autonomous_exploit_engine.py:1191` | `def _build_command_chain(self, candidate, profile)` |
| `_check_known_cves` | method | `modules/autonomous_exploit_engine.py:1979` | `def _check_known_cves(self, profile)` |
| `_check_success` | method | `modules/autonomous_exploit_engine.py:1343` | `def _check_success(self, output, candidate)` |
| `_credential_aware_rank` | method | `modules/autonomous_exploit_engine.py:241` | `def _credential_aware_rank(self, profile, credentials)` |
| `_detect_os_from_payload` | method | `modules/autonomous_exploit_engine.py:1566` | `def _detect_os_from_payload(self)` |
| `_detect_shell` | method | `modules/autonomous_exploit_engine.py:1378` | `def _detect_shell(self, output)` |
| `_determine_access_level` | method | `modules/autonomous_exploit_engine.py:1398` | `def _determine_access_level(self, ip, credentials)` |
| `_discover_internal_interfaces` | method | `modules/autonomous_exploit_engine.py:2500` | `def _discover_internal_interfaces(self, profile)` |
| `_execute_privesc` | method | `modules/autonomous_exploit_engine.py:2335` | `def _execute_privesc(self, technique, profile, session_id)` |
| `_extract_cves_from_text` | method | `modules/autonomous_exploit_engine.py:1751` | `def _extract_cves_from_text(self, text)` |
| `_filter_placeholder_creds` | method | `modules/autonomous_exploit_engine.py:284` | `def _filter_placeholder_creds(credentials)` |
| `_get_os_type` | method | `modules/autonomous_exploit_engine.py:1663` | `def _get_os_type(self, profile)` |
| `_get_stealth_scan_flags` | method | `modules/autonomous_exploit_engine.py:2606` | `def _get_stealth_scan_flags(self)` |
| `_heuristic_match` | method | `modules/autonomous_exploit_engine.py:520` | `def _heuristic_match(self, service, product, version)` |
| `_is_placeholder` | function | `modules/autonomous_exploit_engine.py:299` | `def _is_placeholder(value)` |
| `_load_from_nmap_xml` | method | `modules/autonomous_exploit_engine.py:1584` | `def _load_from_nmap_xml(self, target)` |
| `_load_payload_config` | method | `modules/autonomous_exploit_engine.py:1456` | `def _load_payload_config(self)` |
| `_load_world_model` | method | `modules/autonomous_exploit_engine.py:1467` | `def _load_world_model(self, target)` |
| `_match_by_port` | method | `modules/autonomous_exploit_engine.py:1031` | `def _match_by_port(self, port, os_type)` |
| `_match_exploit_db` | method | `modules/autonomous_exploit_engine.py:482` | `def _match_exploit_db(self, service, product, version)` |
| `_match_privesc_techniques` | method | `modules/autonomous_exploit_engine.py:2145` | `def _match_privesc_techniques(self, findings, os_type)` |
| `_match_service_banners` | method | `modules/autonomous_exploit_engine.py:1799` | `def _match_service_banners(self, profile)` |
| `_parse_nse_output` | method | `modules/autonomous_exploit_engine.py:1716` | `def _parse_nse_output(self, target_ip)` |
| `_register_session` | method | `modules/autonomous_exploit_engine.py:1428` | `def _register_session(self, ip, output)` |
| `_resolve_port` | method | `modules/autonomous_exploit_engine.py:1174` | `def _resolve_port(self, candidate, profile)` |
| `_run_exploit` | method | `modules/autonomous_exploit_engine.py:1128` | `def _run_exploit(self, candidate, profile)` |
| `_run_linux_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2033` | `def _run_linux_privesc_checks(self, profile, session_id)` |
| `_run_windows_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2102` | `def _run_windows_privesc_checks(self, profile, session_id)` |
| `_scorer` | method | `modules/autonomous_exploit_engine.py:1088` | `def _scorer(self, exploit, service, product, version)` |
| `chain_privesc` | method | `modules/autonomous_exploit_engine.py:2005` | `def chain_privesc(self, profile, session_id)` |
| `enable_stealth` | method | `modules/autonomous_exploit_engine.py:2561` | `def enable_stealth(self, stealth_level)` |
| `execute_candidate` | method | `modules/autonomous_exploit_engine.py:420` | `def execute_candidate(self, candidate, profile)` |
| `full_auto_pwn` | method | `modules/autonomous_exploit_engine.py:2625` | `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth)` |
| `get_instance` | method | `modules/autonomous_exploit_engine.py:134` | `def get_instance(cls)` |
| `hunt` | method | `modules/autonomous_exploit_engine.py:145` | `def hunt(self, target, max_exploits, profile)` |
| `profile` | method | `modules/autonomous_exploit_engine.py:328` | `def profile(self, target)` |
| `rank_exploits` | method | `modules/autonomous_exploit_engine.py:389` | `def rank_exploits(self, profile)` |
| `retry_with_credentials` | method | `modules/autonomous_exploit_engine.py:184` | `def retry_with_credentials(self, target, credentials)` |
| `scan_vulnerabilities` | method | `modules/autonomous_exploit_engine.py:1690` | `def scan_vulnerabilities(self, profile)` |
| `trigger_pivot` | method | `modules/autonomous_exploit_engine.py:2435` | `def trigger_pivot(self, profile, session_id)` |
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
| `BeaconConfig` | class | `modules/beacon_config_builder.py:46` | `class BeaconConfig` |
| `BeaconConfigBuilder` | class | `modules/beacon_config_builder.py:239` | `class BeaconConfigBuilder` |
| `__init__` | method | `modules/beacon_config_builder.py:247` | `def __init__(self, payload)` |
| `_inject_profile_engine` | method | `modules/beacon_config_builder.py:320` | `def _inject_profile_engine(self, config)` |
| `_inject_sleep_engine` | method | `modules/beacon_config_builder.py:368` | `def _inject_sleep_engine(self, config)` |
| `_inject_socks_engine` | method | `modules/beacon_config_builder.py:387` | `def _inject_socks_engine(self, config)` |
| `_validate_bof_token` | function | `modules/beacon_config_builder.py:493` | `def _validate_bof_token(token, label)` |
| `build` | method | `modules/beacon_config_builder.py:250` | `def build(self, name)` |
| `from_payload` | method | `modules/beacon_config_builder.py:405` | `def from_payload(cls, payload)` |
| `from_payload_file` | method | `modules/beacon_config_builder.py:410` | `def from_payload_file(cls, path)` |
| `generate_bof_execution_command` | function | `modules/beacon_config_builder.py:449` | `def generate_bof_execution_command(bof_name, c2_url, args, bofs_dir)` |
| `sanitize_client_id` | function | `modules/beacon_config_builder.py:425` | `def sanitize_client_id(client_id)` |
| `to_config_json` | method | `modules/beacon_config_builder.py:162` | `def to_config_json(self)` |
| `to_dict` | method | `modules/beacon_config_builder.py:187` | `def to_dict(self)` |
| `to_gen_beacon_args` | method | `modules/beacon_config_builder.py:119` | `def to_gen_beacon_args(self)` |
| `to_go_implant_vars` | method | `modules/beacon_config_builder.py:139` | `def to_go_implant_vars(self)` |
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
| `BofEntryRow` | class | `modules/bof_admin.py:50` | `class BofEntryRow` |
| `_write_atomic` | function | `modules/bof_admin.py:243` | `def _write_atomic(target, data)` |
| `_yaml_module` | function | `modules/bof_admin.py:65` | `def _yaml_module()` |
| `bof_path` | function | `modules/bof_admin.py:85` | `def bof_path(filename, directory)` |
| `bof_template` | function | `modules/bof_admin.py:224` | `def bof_template(name, description, client)` |
| `create_bof` | function | `modules/bof_admin.py:257` | `def create_bof(filename)` |
| `delete_bof` | function | `modules/bof_admin.py:391` | `def delete_bof(path, directory)` |
| `load_bof` | function | `modules/bof_admin.py:110` | `def load_bof(path)` |
| `preview_bof` | function | `modules/bof_admin.py:370` | `def preview_bof(path, limit)` |
| `save_bof_yaml` | function | `modules/bof_admin.py:332` | `def save_bof_yaml(path, text, directory)` |
| `scan_bofs` | function | `modules/bof_admin.py:179` | `def scan_bofs(directory, sessions_dir)` |
| `slugify` | function | `modules/bof_admin.py:72` | `def slugify(value)` |
| `update_bof` | function | `modules/bof_admin.py:300` | `def update_bof(path, data, directory)` |
| `validate_bof` | function | `modules/bof_admin.py:132` | `def validate_bof(data)` |
| `BofDeliveryConfig` | class | `modules/bof_delivery.py:141` | `class BofDeliveryConfig` |
| `ClientAddon` | class | `modules/bof_delivery.py:162` | `class ClientAddon` |
| `_DockerSession` | class | `modules/bof_delivery.py:1152` | `class _DockerSession` |
| `__init__` | method | `modules/bof_delivery.py:1160` | `def __init__(self, container)` |
| `_apply_upstream_report_patch` | function | `modules/bof_delivery.py:493` | `def _apply_upstream_report_patch(addon, config)` |
| `_atomic_session` | function | `modules/bof_delivery.py:1253` | `def _atomic_session(target)` |
| `_beacons_from_history` | function | `modules/bof_delivery.py:791` | `def _beacons_from_history(config)` |
| `_c2_channel_base` | function | `modules/bof_delivery.py:666` | `def _c2_channel_base(cfg, payload)` |
| `_deploy_paths` | function | `modules/bof_delivery.py:1006` | `def _deploy_paths(addon)` |
| `_docker_session_for` | function | `modules/bof_delivery.py:1206` | `def _docker_session_for(target)` |
| `_history_config` | function | `modules/bof_delivery.py:1340` | `def _history_config(config)` |
| `_raw_stage_for_implant_serving` | function | `modules/bof_delivery.py:441` | `def _raw_stage_for_implant_serving(addon_name, binary_path, config)` |
| `_record_after` | function | `modules/bof_delivery.py:871` | `def _record_after(row, since)` |
| `_shell_bearing_specs` | function | `modules/bof_delivery.py:1303` | `def _shell_bearing_specs(target)` |
| `_stage_payload_b64` | function | `modules/bof_delivery.py:95` | `def _stage_payload_b64(external_root)` |
| `alive` | method | `modules/bof_delivery.py:1164` | `def alive(self, timeout)` |
| `beacon_runtime_config` | function | `modules/bof_delivery.py:255` | `def beacon_runtime_config(client, client_id, config, payload)` |
| `bof_results` | function | `modules/bof_delivery.py:1356` | `def bof_results(client_id, limit, config)` |
| `c2_reachable` | function | `modules/bof_delivery.py:895` | `def c2_reachable(config, payload)` |
| `config_sessions_dir` | function | `modules/bof_delivery.py:1335` | `def config_sessions_dir()` |
| `delivery_command` | function | `modules/bof_delivery.py:640` | `def delivery_command(bof_name, c2_url, args, bofs_dir)` |
| `deploy_client` | function | `modules/bof_delivery.py:1035` | `def deploy_client(client, target)` |
| `key_missing_from_error` | function | `modules/bof_delivery.py:626` | `def key_missing_from_error(exc)` |
| `load_client_addon` | function | `modules/bof_delivery.py:180` | `def load_client_addon(client, config)` |
| `queue_to_beacon` | function | `modules/bof_delivery.py:688` | `def queue_to_beacon(client_id, command, config, payload)` |
| `recent_beacons` | function | `modules/bof_delivery.py:751` | `def recent_beacons(config, payload)` |
| `run` | method | `modules/bof_delivery.py:1184` | `def run(self, command, timeout)` |
| `run_bof` | function | `modules/bof_delivery.py:930` | `def run_bof(bof_name, client_id, args)` |
| `run_bof_train` | function | `modules/bof_delivery.py:969` | `def run_bof_train(client_id, names, args)` |
| `stage_bof` | function | `modules/bof_delivery.py:236` | `def stage_bof(name, config)` |
| `stage_client` | function | `modules/bof_delivery.py:374` | `def stage_client(client, config, payload)` |
| `staging_dir` | function | `modules/bof_delivery.py:221` | `def staging_dir(config)` |
| `wait_for_beacon` | function | `modules/bof_delivery.py:817` | `def wait_for_beacon(client_id, since, timeout, config, payload)` |
| `write_client_config` | function | `modules/bof_delivery.py:332` | `def write_client_config(client, client_id, config, payload)` |
| `BofCatalog` | class | `modules/bof_registry.py:173` | `class BofCatalog` |
| `BofCategory` | class | `modules/bof_registry.py:78` | `class BofCategory(str, Enum)` |
| `BofEntry` | class | `modules/bof_registry.py:95` | `class BofEntry` |
| `BofMarketplace` | class | `modules/bof_registry.py:607` | `class BofMarketplace` |
| `BofPlatform` | class | `modules/bof_registry.py:71` | `class BofPlatform(str, Enum)` |
| `BofRegistry` | class | `modules/bof_registry.py:520` | `class BofRegistry` |
| `BofValidator` | class | `modules/bof_registry.py:474` | `class BofValidator` |
| `BofYamlStore` | class | `modules/bof_registry.py:281` | `class BofYamlStore` |
| `__init__` | method | `modules/bof_registry.py:290` | `def __init__(self, directory)` |
| `__init__` | method | `modules/bof_registry.py:527` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/bof_registry.py:619` | `def __init__(self, sessions_dir, catalog)` |
| `_build_default_catalog` | function | `modules/bof_registry.py:349` | `def _build_default_catalog()` |
| `_load_manifest` | method | `modules/bof_registry.py:537` | `def _load_manifest(self)` |
| `_save_manifest` | method | `modules/bof_registry.py:548` | `def _save_manifest(self, manifest)` |
| `bulk_install` | method | `modules/bof_registry.py:737` | `def bulk_install(self, names)` |
| `catalog` | method | `modules/bof_registry.py:630` | `def catalog(self)` |
| `client_addon_install_path` | function | `modules/bof_registry.py:415` | `def client_addon_install_path(client, addons_dir)` |
| `compute_sha256` | method | `modules/bof_registry.py:483` | `def compute_sha256(filepath)` |
| `directory` | method | `modules/bof_registry.py:299` | `def directory(self)` |
| `find_client_artifact` | function | `modules/bof_registry.py:362` | `def find_client_artifact(entry)` |
| `from_dict` | method | `modules/bof_registry.py:151` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/bof_registry.py:257` | `def from_dict(cls, raw)` |
| `get` | method | `modules/bof_registry.py:193` | `def get(self, name)` |
| `get_install_info` | method | `modules/bof_registry.py:601` | `def get_install_info(self, name)` |
| `info` | method | `modules/bof_registry.py:658` | `def info(self, name)` |
| `install` | method | `modules/bof_registry.py:558` | `def install(self, entry)` |
| `install` | method | `modules/bof_registry.py:675` | `def install(self, name)` |
| `install_dir` | method | `modules/bof_registry.py:533` | `def install_dir(self)` |
| `is_installed` | method | `modules/bof_registry.py:553` | `def is_installed(self, name)` |
| `list_all` | method | `modules/bof_registry.py:245` | `def list_all(self)` |
| `list_by_category` | method | `modules/bof_registry.py:237` | `def list_by_category(self, category)` |
| `list_by_platform` | method | `modules/bof_registry.py:241` | `def list_by_platform(self, platform)` |
| `list_installed` | method | `modules/bof_registry.py:596` | `def list_installed(self)` |
| `list_installed` | method | `modules/bof_registry.py:717` | `def list_installed(self)` |
| `list_missing_dependencies` | method | `modules/bof_registry.py:729` | `def list_missing_dependencies(self, name)` |
| `load` | method | `modules/bof_registry.py:265` | `def load(cls, path)` |
| `load_catalog` | method | `modules/bof_registry.py:342` | `def load_catalog(self)` |
| `load_entries` | method | `modules/bof_registry.py:303` | `def load_entries(self)` |
| `register` | method | `modules/bof_registry.py:183` | `def register(self, entry)` |
| `register_many` | method | `modules/bof_registry.py:188` | `def register_many(self, entries)` |
| `registry` | method | `modules/bof_registry.py:635` | `def registry(self)` |
| `save` | method | `modules/bof_registry.py:273` | `def save(self, path)` |
| `search` | method | `modules/bof_registry.py:204` | `def search(self, query)` |
| `search` | method | `modules/bof_registry.py:639` | `def search(self, query)` |
| `stage_entry_bof` | function | `modules/bof_registry.py:441` | `def stage_entry_bof(entry, sessions_dir)` |
| `to_dict` | method | `modules/bof_registry.py:130` | `def to_dict(self)` |
| `to_dict` | method | `modules/bof_registry.py:249` | `def to_dict(self)` |
| `uninstall` | method | `modules/bof_registry.py:579` | `def uninstall(self, name, remove_files)` |
| `uninstall` | method | `modules/bof_registry.py:704` | `def uninstall(self, name)` |
| `validate_args` | method | `modules/bof_registry.py:508` | `def validate_args(entry, args)` |
| `verify_entry` | method | `modules/bof_registry.py:492` | `def verify_entry(entry, filepath)` |
| `SyncReceiver` | class | `modules/browser_sync.py:592` | `class SyncReceiver` |
| `_Handler` | class | `modules/browser_sync.py:632` | `class _Handler(BaseHTTPRequestHandler)` |
| `__init__` | method | `modules/browser_sync.py:595` | `def __init__(self, host, port)` |
| `_clean_cookie` | function | `modules/browser_sync.py:562` | `def _clean_cookie(raw)` |
| `_drain` | method | `modules/browser_sync.py:686` | `def _drain(self, length)` |
| `_jar_path` | function | `modules/browser_sync.py:82` | `def _jar_path()` |
| `_load_rules_cached` | function | `modules/browser_sync.py:367` | `def _load_rules_cached()` |
| `_netscape_line` | function | `modules/browser_sync.py:317` | `def _netscape_line(cookie)` |
| `_payload_inject_enabled` | function | `modules/browser_sync.py:413` | `def _payload_inject_enabled()` |
| `_profile_cache_get` | function | `modules/browser_sync.py:543` | `def _profile_cache_get()` |
| `_profile_path` | function | `modules/browser_sync.py:77` | `def _profile_path()` |
| `_read_payload_cached` | function | `modules/browser_sync.py:393` | `def _read_payload_cached()` |
| `_reply` | method | `modules/browser_sync.py:698` | `def _reply(self, code, payload)` |
| `_rules_path` | function | `modules/browser_sync.py:87` | `def _rules_path()` |
| `_sanitize_header_value` | function | `modules/browser_sync.py:97` | `def _sanitize_header_value(value)` |
| `_sessions_dir` | function | `modules/browser_sync.py:71` | `def _sessions_dir()` |
| `_store` | method | `modules/browser_sync.py:716` | `def _store(self, data)` |
| `_token_path` | function | `modules/browser_sync.py:92` | `def _token_path()` |
| `apply_identity_headers` | function | `modules/browser_sync.py:475` | `def apply_identity_headers(host, headers, body, path, scheme)` |
| `apply_identity_to_url` | function | `modules/browser_sync.py:839` | `def apply_identity_to_url(url, headers, body)` |
| `apply_rules` | function | `modules/browser_sync.py:418` | `def apply_rules(headers, body)` |
| `build_cookie_header` | function | `modules/browser_sync.py:285` | `def build_cookie_header(existing, cookies)` |
| `clear_profile` | function | `modules/browser_sync.py:822` | `def clear_profile()` |
| `cookie_expired` | function | `modules/browser_sync.py:226` | `def cookie_expired(cookie, now)` |
| `cookie_matches_host` | function | `modules/browser_sync.py:183` | `def cookie_matches_host(cookie, host)` |
| `cookie_matches_path` | function | `modules/browser_sync.py:202` | `def cookie_matches_path(cookie, request_path)` |
| `cookies_for_host` | function | `modules/browser_sync.py:248` | `def cookies_for_host(profile, host, path, scheme)` |
| `do_GET` | method | `modules/browser_sync.py:642` | `def do_GET(self)` |
| `do_POST` | method | `modules/browser_sync.py:654` | `def do_POST(self)` |
| `ensure_wiring` | function | `modules/browser_sync.py:864` | `def ensure_wiring()` |
| `get_receiver` | function | `modules/browser_sync.py:791` | `def get_receiver()` |
| `jar_path` | function | `modules/browser_sync.py:362` | `def jar_path()` |
| `load_profile` | function | `modules/browser_sync.py:151` | `def load_profile()` |
| `log_message` | method | `modules/browser_sync.py:638` | `def log_message(self, fmt)` |
| `masked_rows` | function | `modules/browser_sync.py:906` | `def masked_rows(profile, domain_filter, full)` |
| `profile_stats` | function | `modules/browser_sync.py:164` | `def profile_stats()` |
| `reset_token` | function | `modules/browser_sync.py:138` | `def reset_token()` |
| `start` | method | `modules/browser_sync.py:610` | `def start(self, host, port)` |
| `start_receiver` | function | `modules/browser_sync.py:800` | `def start_receiver(port, host)` |
| `status` | method | `modules/browser_sync.py:771` | `def status(self)` |
| `stop` | method | `modules/browser_sync.py:755` | `def stop(self)` |
| `stop_receiver` | function | `modules/browser_sync.py:813` | `def stop_receiver()` |
| `token` | function | `modules/browser_sync.py:112` | `def token(create)` |
| `write_netscape_jar` | function | `modules/browser_sync.py:340` | `def write_netscape_jar(profile, path)` |
| `decrypt_bsb_report` | function | `modules/bsb_compat.py:90` | `def decrypt_bsb_report(encrypted_data, master_key, replay_window_seconds)` |
| `decrypt_bsb_stage_blob` | function | `modules/bsb_compat.py:232` | `def decrypt_bsb_stage_blob(encrypted_data, token)` |
| `derive_bsb_keys` | function | `modules/bsb_compat.py:52` | `def derive_bsb_keys(master_key)` |
| `derive_bsb_stage_keys` | function | `modules/bsb_compat.py:162` | `def derive_bsb_stage_keys(token)` |
| `encrypt_bsb_command` | function | `modules/bsb_compat.py:139` | `def encrypt_bsb_command(data, master_key)` |
| `encrypt_bsb_stage_blob` | function | `modules/bsb_compat.py:208` | `def encrypt_bsb_stage_blob(data, token)` |
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
| `_lessons_path` | function | `modules/campaign_blacklist.py:22` | `def _lessons_path()` |

Next: [SYMBOLS_p13.md](SYMBOLS_p13.md)
