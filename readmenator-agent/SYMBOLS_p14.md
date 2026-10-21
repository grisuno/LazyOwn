# Symbols (page 14 of 44)
Previous: [SYMBOLS_p13.md](SYMBOLS_p13.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_run` | function | `modules/exploitgym_gym.py:274` | `def _run(name, cmd, cwd, timeout)` |
| `_run_agent` | function | `modules/exploitgym_gym.py:378` | `def _run_agent(task_id, model, mitigations, root, params, timeout)` |
| `_run_streaming` | function | `modules/exploitgym_gym.py:206` | `def _run_streaming(cmd, cwd, timeout)` |
| `_save_records` | function | `modules/exploitgym_gym.py:514` | `def _save_records(records)` |
| `check_readiness` | function | `modules/exploitgym_gym.py:112` | `def check_readiness(params)` |
| `list_tasks` | function | `modules/exploitgym_gym.py:178` | `def list_tasks(params, domain, limit)` |
| `pull_task` | function | `modules/exploitgym_gym.py:344` | `def pull_task(task_id, params, timeout)` |
| `run_task` | function | `modules/exploitgym_gym.py:423` | `def run_task(task_id, params, model, mitigations, timeout)` |
| `score_task` | function | `modules/exploitgym_gym.py:565` | `def score_task(task_id, success, techniques, params)` |
| `setup_harness` | function | `modules/exploitgym_gym.py:249` | `def setup_harness(params, steps)` |
| `verify_flag` | function | `modules/exploitgym_gym.py:548` | `def verify_flag(task_id, params)` |
| `chown_project_tree` | function | `modules/fast_run_service.sh:310` | `` |
| `cmd_chown_now` | function | `modules/fast_run_service.sh:521` | `` |
| `cmd_logs` | function | `modules/fast_run_service.sh:505` | `` |
| `cmd_restart` | function | `modules/fast_run_service.sh:480` | `` |
| `cmd_start` | function | `modules/fast_run_service.sh:445` | `` |
| `cmd_status` | function | `modules/fast_run_service.sh:486` | `` |
| `cmd_stop` | function | `modules/fast_run_service.sh:465` | `` |
| `config_truthy` | function | `modules/fast_run_service.sh:155` | `` |
| `ensure_log_file` | function | `modules/fast_run_service.sh:211` | `` |
| `is_pid_alive` | function | `modules/fast_run_service.sh:189` | `` |
| `is_service_running` | function | `modules/fast_run_service.sh:194` | `` |
| `load_config` | function | `modules/fast_run_service.sh:139` | `` |
| `log_error` | function | `modules/fast_run_service.sh:81` | `` |
| `log_file_for` | function | `modules/fast_run_service.sh:171` | `` |
| `log_info` | function | `modules/fast_run_service.sh:73` | `` |
| `log_timestamp` | function | `modules/fast_run_service.sh:69` | `` |
| `log_warn` | function | `modules/fast_run_service.sh:77` | `` |
| `main` | function | `modules/fast_run_service.sh:557` | `` |
| `managed_services_in_order` | function | `modules/fast_run_service.sh:429` | `` |
| `pid_file_for` | function | `modules/fast_run_service.sh:166` | `` |
| `prepare_runtime_dirs` | function | `modules/fast_run_service.sh:126` | `` |
| `read_pid_value` | function | `modules/fast_run_service.sh:176` | `` |
| `require_deps` | function | `modules/fast_run_service.sh:97` | `` |
| `require_paths` | function | `modules/fast_run_service.sh:113` | `` |
| `require_root` | function | `modules/fast_run_service.sh:89` | `` |
| `spawn_as_root` | function | `modules/fast_run_service.sh:247` | `` |
| `spawn_as_target_user` | function | `modules/fast_run_service.sh:228` | `` |
| `start_chown_watcher` | function | `modules/fast_run_service.sh:315` | `` |
| `start_cloudflare_service` | function | `modules/fast_run_service.sh:400` | `` |
| `start_discord_service` | function | `modules/fast_run_service.sh:380` | `` |
| `start_lazyc2_service` | function | `modules/fast_run_service.sh:342` | `` |
| `start_ollama_service` | function | `modules/fast_run_service.sh:410` | `` |
| `start_telegram_service` | function | `modules/fast_run_service.sh:390` | `` |
| `start_vpn_service` | function | `modules/fast_run_service.sh:363` | `` |
| `start_www_service` | function | `modules/fast_run_service.sh:356` | `` |
| `stop_named_service` | function | `modules/fast_run_service.sh:292` | `` |
| `terminate_pid_tree` | function | `modules/fast_run_service.sh:264` | `` |
| `usage` | function | `modules/fast_run_service.sh:528` | `` |
| `write_pid_file` | function | `modules/fast_run_service.sh:201` | `` |
| `FindingRecord` | class | `modules/finding_lifecycle.py:182` | `class FindingRecord` |
| `RetestRecord` | class | `modules/finding_lifecycle.py:195` | `class RetestRecord` |
| `_finding_from_row` | function | `modules/finding_lifecycle.py:220` | `def _finding_from_row(row)` |
| `_load` | function | `modules/finding_lifecycle.py:40` | `def _load(sessions_dir)` |
| `_load_retests` | function | `modules/finding_lifecycle.py:292` | `def _load_retests(sessions_dir)` |
| `_retests_path` | function | `modules/finding_lifecycle.py:287` | `def _retests_path(sessions_dir)` |
| `_save` | function | `modules/finding_lifecycle.py:53` | `def _save(sessions_dir, data)` |
| `_save_retests` | function | `modules/finding_lifecycle.py:303` | `def _save_retests(sessions_dir, payload)` |
| `_store_path` | function | `modules/finding_lifecycle.py:35` | `def _store_path(sessions_dir)` |
| `_token_value` | function | `modules/finding_lifecycle.py:205` | `def _token_value(refs, prefix, default)` |
| `_with_token` | function | `modules/finding_lifecycle.py:213` | `def _with_token(refs, prefix, value)` |
| `add_dead_end` | function | `modules/finding_lifecycle.py:104` | `def add_dead_end(kind, value, reason, sessions_dir)` |
| `apply_confirmation` | function | `modules/finding_lifecycle.py:154` | `def apply_confirmation(nodes, sessions_dir)` |
| `classify_retest` | function | `modules/finding_lifecycle.py:384` | `def classify_retest(needle, output)` |
| `confirm` | function | `modules/finding_lifecycle.py:61` | `def confirm(finding_id, evidence, sessions_dir, by)` |
| `findings_for` | function | `modules/finding_lifecycle.py:259` | `def findings_for(db, workspace)` |
| `has_running_retest` | function | `modules/finding_lifecycle.py:310` | `def has_running_retest(finding_id, sessions_dir)` |
| `is_dead_end` | function | `modules/finding_lifecycle.py:116` | `def is_dead_end(kind, value, sessions_dir)` |
| `record` | function | `modules/finding_lifecycle.py:234` | `def record(db, workspace, host, title, severity, summary, poc)` |
| `reject` | function | `modules/finding_lifecycle.py:90` | `def reject(finding_id, reason, sessions_dir, by)` |
| `render_markdown` | function | `modules/finding_lifecycle.py:403` | `def render_markdown(db, workspace, title)` |
| `request_retest` | function | `modules/finding_lifecycle.py:318` | `def request_retest(db, finding_id, sessions_dir)` |
| `resolve` | function | `modules/finding_lifecycle.py:129` | `def resolve(node, sessions_dir)` |
| `resolve_retest` | function | `modules/finding_lifecycle.py:338` | `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)` |
| `set_status` | function | `modules/finding_lifecycle.py:264` | `def set_status(db, finding_id, status)` |
| `suppressed_values` | function | `modules/finding_lifecycle.py:123` | `def suppressed_values(sessions_dir)` |
| `ForensicCleaner` | class | `modules/forensic_cleaner.py:57` | `class ForensicCleaner` |
| `ForensicCleanerConfig` | class | `modules/forensic_cleaner.py:23` | `class ForensicCleanerConfig` |
| `__init__` | method | `modules/forensic_cleaner.py:67` | `def __init__(self, config)` |
| `amcache_parse` | method | `modules/forensic_cleaner.py:259` | `def amcache_parse(self)` |
| `linux_cleanup` | method | `modules/forensic_cleaner.py:165` | `def linux_cleanup(self)` |
| `macos_cleanup` | method | `modules/forensic_cleaner.py:193` | `def macos_cleanup(self)` |
| `windows_cleanup` | method | `modules/forensic_cleaner.py:70` | `def windows_cleanup(self)` |
| `windows_prefetch_parse` | method | `modules/forensic_cleaner.py:221` | `def windows_prefetch_parse(self, prefetch_path)` |
| `GCPAttackEngine` | class | `modules/gcp_attacks.py:77` | `class GCPAttackEngine` |
| `GCPConfig` | class | `modules/gcp_attacks.py:57` | `class GCPConfig` |
| `__init__` | method | `modules/gcp_attacks.py:90` | `def __init__(self, config)` |
| `cloud_functions_backdoor` | method | `modules/gcp_attacks.py:144` | `def cloud_functions_backdoor(self)` |
| `cloudbuild_abuse` | method | `modules/gcp_attacks.py:230` | `def cloudbuild_abuse(self)` |
| `compute_engine_metadata_exfil` | method | `modules/gcp_attacks.py:173` | `def compute_engine_metadata_exfil(self)` |
| `enumerate_iam_policy` | method | `modules/gcp_attacks.py:93` | `def enumerate_iam_policy(self, resource)` |
| `gcs_enumeration` | method | `modules/gcp_attacks.py:194` | `def gcs_enumeration(self)` |
| `organization_escalation` | method | `modules/gcp_attacks.py:261` | `def organization_escalation(self)` |
| `service_account_impersonation` | method | `modules/gcp_attacks.py:119` | `def service_account_impersonation(self)` |
| `summary` | method | `modules/gcp_attacks.py:297` | `def summary(self)` |
| `extract_cmd2_tools` | function | `modules/generate_tools.py:6` | `def extract_cmd2_tools(script_path)` |
| `GoalSpec` | class | `modules/goals.py:20` | `class GoalSpec` |
| `GoalTracker` | class | `modules/goals.py:117` | `class GoalTracker` |
| `TaskConstraints` | class | `modules/goals.py:29` | `class TaskConstraints` |
| `__init__` | method | `modules/goals.py:120` | `def __init__(self, goals)` |
| `all_achieved` | method | `modules/goals.py:148` | `def all_achieved(self)` |
| `blocked` | method | `modules/goals.py:35` | `def blocked(self, command)` |
| `constraint_block_text` | function | `modules/goals.py:103` | `def constraint_block_text(constraints)` |
| `decompose_rule_based` | function | `modules/goals.py:63` | `def decompose_rule_based(objective_text, max_goals)` |
| `goal_met` | method | `modules/goals.py:140` | `def goal_met(self, opt_in)` |
| `goals` | method | `modules/goals.py:125` | `def goals(self)` |
| `load_constraints` | function | `modules/goals.py:83` | `def load_constraints(payload)` |
| `open_goals` | method | `modules/goals.py:152` | `def open_goals(self)` |
| `prove_goal` | method | `modules/goals.py:129` | `def prove_goal(self, goal_text, evidence)` |
| `GPOAbuseEngine` | class | `modules/gpo_abuse.py:105` | `class GPOAbuseEngine` |
| `GPOAbusePlan` | class | `modules/gpo_abuse.py:83` | `class GPOAbusePlan` |
| `GPOInfo` | class | `modules/gpo_abuse.py:54` | `class GPOInfo` |
| `__init__` | method | `modules/gpo_abuse.py:118` | `def __init__(self, domain, dc_ip)` |
| `detect_risky_gpos` | method | `modules/gpo_abuse.py:406` | `def detect_risky_gpos(self)` |
| `generate_all_plans` | method | `modules/gpo_abuse.py:382` | `def generate_all_plans(self, command, username)` |
| `parse_bloodhound_gpos` | method | `modules/gpo_abuse.py:160` | `def parse_bloodhound_gpos(self, bloodhound_nodes)` |
| `parse_gpo_list` | method | `modules/gpo_abuse.py:124` | `def parse_gpo_list(self, raw_gpo_output)` |
| `plan_local_admin_addition` | method | `modules/gpo_abuse.py:266` | `def plan_local_admin_addition(self, gpo, username, group)` |
| `plan_logon_script` | method | `modules/gpo_abuse.py:238` | `def plan_logon_script(self, gpo, command)` |
| `plan_registry_preference` | method | `modules/gpo_abuse.py:322` | `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)` |
| `plan_scheduled_task` | method | `modules/gpo_abuse.py:182` | `def plan_scheduled_task(self, gpo, command, task_name)` |
| `plan_service_installation` | method | `modules/gpo_abuse.py:356` | `def plan_service_installation(self, gpo, service_name, binary_path)` |
| `plan_startup_script` | method | `modules/gpo_abuse.py:208` | `def plan_startup_script(self, gpo, script_content, script_name)` |
| `plan_wmi_filter_abuse` | method | `modules/gpo_abuse.py:293` | `def plan_wmi_filter_abuse(self, gpo, wmi_query)` |
| `summary` | method | `modules/gpo_abuse.py:434` | `def summary(self)` |
| `has` | function | `modules/gui_askpass.sh:22` | `` |
| `try_kdialog` | function | `modules/gui_askpass.sh:40` | `` |
| `try_ssh_askpass` | function | `modules/gui_askpass.sh:33` | `` |
| `try_yad` | function | `modules/gui_askpass.sh:28` | `` |
| `try_zenity` | function | `modules/gui_askpass.sh:24` | `` |
| `_empty_state` | function | `modules/gym_registry.py:442` | `def _empty_state()` |
| `_matches` | function | `modules/gym_registry.py:625` | `def _matches(run, selector)` |
| `_merge_legacy` | function | `modules/gym_registry.py:532` | `def _merge_legacy(state)` |
| `_next_run_id` | function | `modules/gym_registry.py:569` | `def _next_run_id(state)` |
| `_normalize_definition` | function | `modules/gym_registry.py:188` | `def _normalize_definition(data)` |
| `_read_yaml` | function | `modules/gym_registry.py:178` | `def _read_yaml(path)` |
| `_sanitize_state` | function | `modules/gym_registry.py:454` | `def _sanitize_state(raw)` |
| `_world_model` | function | `modules/gym_registry.py:447` | `def _world_model()` |
| `_write_yaml` | function | `modules/gym_registry.py:282` | `def _write_yaml(path, data)` |
| `_yaml_module` | function | `modules/gym_registry.py:85` | `def _yaml_module()` |
| `create_definition` | function | `modules/gym_registry.py:300` | `def create_definition(gym_id)` |
| `definition_path` | function | `modules/gym_registry.py:155` | `def definition_path(gym_id, directory)` |
| `delete_definition` | function | `modules/gym_registry.py:402` | `def delete_definition(gym_id, directory)` |
| `get_active_runs` | function | `modules/gym_registry.py:637` | `def get_active_runs(selector, operator)` |
| `load_definitions` | function | `modules/gym_registry.py:207` | `def load_definitions(directory)` |
| `new_run_token` | function | `modules/gym_registry.py:761` | `def new_run_token()` |
| `normalize_operator` | function | `modules/gym_registry.py:495` | `def normalize_operator(value)` |
| `pop_run` | function | `modules/gym_registry.py:724` | `def pop_run(selector)` |
| `read_state` | function | `modules/gym_registry.py:501` | `def read_state()` |
| `scan_definitions` | function | `modules/gym_registry.py:239` | `def scan_definitions(directory)` |
| `select_run` | function | `modules/gym_registry.py:663` | `def select_run(selector)` |
| `slugify` | function | `modules/gym_registry.py:92` | `def slugify(value)` |
| `start_run` | function | `modules/gym_registry.py:579` | `def start_run(challenge_id, definitions)` |
| `state_summary` | function | `modules/gym_registry.py:751` | `def state_summary()` |
| `stop_runs` | function | `modules/gym_registry.py:695` | `def stop_runs(selector)` |
| `update_definition_yaml` | function | `modules/gym_registry.py:369` | `def update_definition_yaml(gym_id, text, directory)` |
| `validate_definition` | function | `modules/gym_registry.py:110` | `def validate_definition(data, filename)` |
| `write_state` | function | `modules/gym_registry.py:520` | `def write_state(state)` |
| `CrackResult` | class | `modules/hash_cracker.py:127` | `class CrackResult` |
| `HashCracker` | class | `modules/hash_cracker.py:151` | `class HashCracker` |
| `HashIdentifier` | class | `modules/hash_cracker.py:140` | `class HashIdentifier` |
| `__init__` | method | `modules/hash_cracker.py:164` | `def __init__(self, wordlist, rules, use_hashcat, timeout)` |
| `_crack_batch_hashcat` | method | `modules/hash_cracker.py:500` | `def _crack_batch_hashcat(self, idents, hash_type, fmt_info, wordlist)` |
| `_crack_batch_john` | method | `modules/hash_cracker.py:610` | `def _crack_batch_john(self, idents, hash_type, fmt_info, wordlist)` |
| `_crack_hashcat` | method | `modules/hash_cracker.py:454` | `def _crack_hashcat(self, hash_value, hash_type, fmt_info, wordlist)` |
| `_crack_john` | method | `modules/hash_cracker.py:560` | `def _crack_john(self, hash_value, hash_type, fmt_info, wordlist)` |
| `_parse_hashcat_output` | method | `modules/hash_cracker.py:671` | `def _parse_hashcat_output(stdout, stderr, original)` |
| `_parse_john_show` | method | `modules/hash_cracker.py:686` | `def _parse_john_show(show_output, original)` |
| `_resolve_wordlist` | method | `modules/hash_cracker.py:178` | `def _resolve_wordlist(self)` |
| `crack_file` | method | `modules/hash_cracker.py:349` | `def crack_file(self, filepath, wordlist, hash_types)` |
| `crack_hash` | method | `modules/hash_cracker.py:295` | `def crack_hash(self, hash_value, hash_type, wordlist)` |
| `crack_secretsdump_output` | function | `modules/hash_cracker.py:695` | `def crack_secretsdump_output(filepath, wordlist, rhost)` |
| `identify` | method | `modules/hash_cracker.py:186` | `def identify(self, line)` |
| `identify_file` | method | `modules/hash_cracker.py:273` | `def identify_file(self, filepath)` |
| `import_to_db` | method | `modules/hash_cracker.py:405` | `def import_to_db(self, results, rhost, workspace_name)` |
| `_find_claude` | function | `modules/hive_invoke.py:115` | `def _find_claude()` |
| `_get_toposwarm` | function | `modules/hive_invoke.py:50` | `def _get_toposwarm()` |
| `_parse_argv` | function | `modules/hive_invoke.py:120` | `def _parse_argv(argv)` |
| `_run_interactive_mode` | function | `modules/hive_invoke.py:172` | `def _run_interactive_mode(prompt, effort, claude_bin)` |
| `_run_print_mode` | function | `modules/hive_invoke.py:150` | `def _run_print_mode(prompt, effort, claude_bin)` |
| `_run_toposwarm_mode` | function | `modules/hive_invoke.py:205` | `def _run_toposwarm_mode(prompt, effort, bridge)` |
| `main` | function | `modules/hive_invoke.py:255` | `def main(argv)` |
| `extract_ips_from_arp` | function | `modules/hostdiscover.sh:21` | `` |
| `extract_listening_ips_from_netstat` | function | `modules/hostdiscover.sh:26` | `` |
| `CodeAnalyzer` | class | `modules/ia_code_analysis.py:28` | `class CodeAnalyzer` |
| `__init__` | method | `modules/ia_code_analysis.py:33` | `def __init__(self, mode)` |
| `analyze_code_file` | method | `modules/ia_code_analysis.py:49` | `def analyze_code_file(self, file_path)` |
| `analyze_directory` | method | `modules/ia_code_analysis.py:37` | `def analyze_directory(self, directory)` |
| `analyze_with_deepseek` | function | `modules/ia_code_analysis.py:66` | `def analyze_with_deepseek(code_content, file_path, mode)` |
| `parse_args` | function | `modules/ia_code_analysis.py:178` | `def parse_args()` |
| `save_results_to_json` | function | `modules/ia_code_analysis.py:123` | `def save_results_to_json(results, file_path)` |
| `start_analysis` | function | `modules/ia_code_analysis.py:169` | `def start_analysis(code_dir, mode)` |
| `LogFileHandler` | class | `modules/ia_logs_analysis.py:54` | `class LogFileHandler(FileSystemEventHandler)` |
| `__init__` | method | `modules/ia_logs_analysis.py:59` | `def __init__(self, mode)` |
| `analyze_log_file` | method | `modules/ia_logs_analysis.py:75` | `def analyze_log_file(self, file_path)` |
| `analyze_with_deepseek` | function | `modules/ia_logs_analysis.py:94` | `def analyze_with_deepseek(log_content, mode)` |
| `on_modified` | method | `modules/ia_logs_analysis.py:64` | `def on_modified(self, event)` |
| `parse_args` | function | `modules/ia_logs_analysis.py:168` | `def parse_args()` |
| `start_monitoring` | function | `modules/ia_logs_analysis.py:147` | `def start_monitoring(log_dir, mode)` |
| `analyze_with_deepseek` | function | `modules/ia_network_analysis.py:39` | `def analyze_with_deepseek(packet_info, mode)` |
| `packet_callback` | function | `modules/ia_network_analysis.py:91` | `def packet_callback(packet, mode)` |
| `parse_args` | function | `modules/ia_network_analysis.py:154` | `def parse_args()` |
| `start_monitoring` | function | `modules/ia_network_analysis.py:130` | `def start_monitoring(interface, timeout, mode)` |
| `check_sudo` | function | `modules/icmp_client.py:57` | `def check_sudo()` |
| `checksum` | function | `modules/icmp_client.py:64` | `def checksum(source_string)` |
| `decrypt_data` | function | `modules/icmp_client.py:34` | `def decrypt_data(data, key)` |
| `encrypt_data` | function | `modules/icmp_client.py:18` | `def encrypt_data(data, key)` |
| `main` | function | `modules/icmp_client.py:130` | `def main()` |
| `receive_icmp_reply` | function | `modules/icmp_client.py:117` | `def receive_icmp_reply(sock)` |
| `send_icmp_packet` | function | `modules/icmp_client.py:82` | `def send_icmp_packet(dest_addr, data, key)` |
| `check_sudo` | function | `modules/icmp_server.py:44` | `def check_sudo()` |
| `checksum` | function | `modules/icmp_server.py:132` | `def checksum(source_string)` |
| `decrypt_data` | function | `modules/icmp_server.py:71` | `def decrypt_data(data, key)` |
| `encrypt_data` | function | `modules/icmp_server.py:55` | `def encrypt_data(data, key)` |
| `execute_command` | function | `modules/icmp_server.py:93` | `def execute_command(command)` |
| `handle_packet` | function | `modules/icmp_server.py:150` | `def handle_packet(packet, addr, key, sock)` |
| `listen_for_icmp` | function | `modules/icmp_server.py:175` | `def listen_for_icmp(interface, key)` |
| `main` | function | `modules/icmp_server.py:202` | `def main()` |
| `send_icmp_reply` | function | `modules/icmp_server.py:112` | `def send_icmp_reply(sock, addr, data, key)` |
| `imagen_a_binario` | function | `modules/img2bin.py:7` | `def imagen_a_binario(imagen_input, binario_output, block_size)` |
| `main` | function | `modules/img2bin.py:43` | `def main()` |
| `CVEMapper` | class | `modules/integrations/misp_export.py:143` | `class CVEMapper(FindingMapper)` |
| `CredentialMapper` | class | `modules/integrations/misp_export.py:123` | `class CredentialMapper(FindingMapper)` |
| `DomainMapper` | class | `modules/integrations/misp_export.py:163` | `class DomainMapper(FindingMapper)` |
| `FindingMapper` | class | `modules/integrations/misp_export.py:86` | `class FindingMapper(ABC)` |
| `HashMapper` | class | `modules/integrations/misp_export.py:183` | `class HashMapper(FindingMapper)` |
| `IPMapper` | class | `modules/integrations/misp_export.py:103` | `class IPMapper(FindingMapper)` |
| `MISPAttribute` | class | `modules/integrations/misp_export.py:59` | `class MISPAttribute` |
| `MISPEvent` | class | `modules/integrations/misp_export.py:70` | `class MISPEvent` |
| `MISPExporter` | class | `modules/integrations/misp_export.py:254` | `class MISPExporter` |
| `ServiceMapper` | class | `modules/integrations/misp_export.py:218` | `class ServiceMapper(FindingMapper)` |
| `_DictFinding` | class | `modules/integrations/misp_export.py:451` | `class _DictFinding` |
| `__init__` | method | `modules/integrations/misp_export.py:263` | `def __init__(self, mappers)` |
| `__init__` | method | `modules/integrations/misp_export.py:454` | `def __init__(self, data)` |
| `_detect_type` | method | `modules/integrations/misp_export.py:211` | `def _detect_type(value)` |
| `_dict_to_findings` | method | `modules/integrations/misp_export.py:403` | `def _dict_to_findings(data)` |
| `_is_credential` | method | `modules/integrations/misp_export.py:138` | `def _is_credential(finding)` |
| `_is_cve` | method | `modules/integrations/misp_export.py:158` | `def _is_cve(finding)` |
| `_is_domain` | method | `modules/integrations/misp_export.py:178` | `def _is_domain(finding)` |
| `_is_hash` | method | `modules/integrations/misp_export.py:206` | `def _is_hash(finding)` |
| `_is_ip` | method | `modules/integrations/misp_export.py:118` | `def _is_ip(finding)` |
| `_is_service` | method | `modules/integrations/misp_export.py:233` | `def _is_service(finding)` |
| `_load_events` | method | `modules/integrations/misp_export.py:383` | `def _load_events(self, sdir)` |
| `_load_findings` | method | `modules/integrations/misp_export.py:365` | `def _load_findings(self, sdir)` |
| `_load_policy_facts` | method | `modules/integrations/misp_export.py:372` | `def _load_policy_facts(self, sdir)` |
| `_main` | function | `modules/integrations/misp_export.py:482` | `def _main()` |
| `_map_finding` | method | `modules/integrations/misp_export.py:443` | `def _map_finding(self, finding)` |
| `export_session` | method | `modules/integrations/misp_export.py:268` | `def export_session(self, sessions_dir, target)` |
| `get_exporter` | function | `modules/integrations/misp_export.py:469` | `def get_exporter()` |
| `map` | method | `modules/integrations/misp_export.py:90` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:106` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:126` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:146` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:166` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:192` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:221` | `def map(self, finding)` |
| `push_to_misp` | method | `modules/integrations/misp_export.py:330` | `def push_to_misp(self, event, url, api_key)` |
| `save` | method | `modules/integrations/misp_export.py:322` | `def save(self, event, path)` |
| `to_json` | method | `modules/integrations/misp_export.py:299` | `def to_json(self, event)` |
| `LocalTemplateIndex` | class | `modules/integrations/nuclei_bridge.py:104` | `class LocalTemplateIndex(TemplateSelector)` |
| `NucleiBridge` | class | `modules/integrations/nuclei_bridge.py:389` | `class NucleiBridge` |
| `NucleiRunner` | class | `modules/integrations/nuclei_bridge.py:279` | `class NucleiRunner` |
| `NucleiTemplate` | class | `modules/integrations/nuclei_bridge.py:71` | `class NucleiTemplate` |
| `TemplateSelector` | class | `modules/integrations/nuclei_bridge.py:87` | `class TemplateSelector(ABC)` |
| `_F` | class | `modules/integrations/nuclei_bridge.py:483` | `class _F` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:114` | `def __init__(self, templates_dir)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:288` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:396` | `def __init__(self, selector, runner)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:484` | `def __init__(self, ftype, value)` |
| `_build_command` | method | `modules/integrations/nuclei_bridge.py:343` | `def _build_command(self, target, templates, output_dir)` |
| `_ensure_built` | method | `modules/integrations/nuclei_bridge.py:158` | `def _ensure_built(self)` |
| `_extract_context` | method | `modules/integrations/nuclei_bridge.py:370` | `def _extract_context(findings)` |
| `_extract_cve_from_tags` | method | `modules/integrations/nuclei_bridge.py:246` | `def _extract_cve_from_tags(tags)` |
| `_extract_cve_from_text` | method | `modules/integrations/nuclei_bridge.py:253` | `def _extract_cve_from_text(text)` |
| `_main` | function | `modules/integrations/nuclei_bridge.py:456` | `def _main()` |
| `_matches` | method | `modules/integrations/nuclei_bridge.py:258` | `def _matches(tmpl, service_lower, cve_upper)` |
| `_normalise_tags` | method | `modules/integrations/nuclei_bridge.py:238` | `def _normalise_tags(raw)` |
| `_parse_regex` | method | `modules/integrations/nuclei_bridge.py:201` | `def _parse_regex(self, text, path)` |
| `_parse_template` | method | `modules/integrations/nuclei_bridge.py:162` | `def _parse_template(self, path)` |
| `_parse_yaml` | method | `modules/integrations/nuclei_bridge.py:172` | `def _parse_yaml(self, text, path)` |
| `build` | method | `modules/integrations/nuclei_bridge.py:141` | `def build(self)` |
| `get_bridge` | function | `modules/integrations/nuclei_bridge.py:443` | `def get_bridge()` |
| `list_templates` | method | `modules/integrations/nuclei_bridge.py:427` | `def list_templates(self, services, cves)` |
| `run` | method | `modules/integrations/nuclei_bridge.py:293` | `def run(self, target, templates, output_dir)` |
| `run_for_findings` | method | `modules/integrations/nuclei_bridge.py:326` | `def run_for_findings(self, target, findings, output_dir, selector)` |
| `scan` | method | `modules/integrations/nuclei_bridge.py:404` | `def scan(self, target, findings, dry_run)` |
| `select` | method | `modules/integrations/nuclei_bridge.py:91` | `def select(self, services, cves)` |
| `select` | method | `modules/integrations/nuclei_bridge.py:121` | `def select(self, services, cves)` |
| `NucleiFinding` | class | `modules/integrations/nuclei_parser.py:71` | `class NucleiFinding` |
| `NucleiParser` | class | `modules/integrations/nuclei_parser.py:99` | `class NucleiParser` |
| `__init__` | method | `modules/integrations/nuclei_parser.py:109` | `def __init__(self, sessions_dir)` |
| `_finding_to_dict` | method | `modules/integrations/nuclei_parser.py:504` | `def _finding_to_dict(finding)` |
| `_parse_json_obj` | method | `modules/integrations/nuclei_parser.py:412` | `def _parse_json_obj(self, obj)` |
| `_parse_line` | method | `modules/integrations/nuclei_parser.py:393` | `def _parse_line(self, line)` |
| `_recommend_for_finding` | method | `modules/integrations/nuclei_parser.py:468` | `def _recommend_for_finding(self, finding, rhost)` |
| `_summarize` | method | `modules/integrations/nuclei_parser.py:517` | `def _summarize(findings)` |
| `enrich_world_model` | method | `modules/integrations/nuclei_parser.py:262` | `def enrich_world_model(self, findings, rhost)` |
| `exploit_probability` | method | `modules/integrations/nuclei_parser.py:95` | `def exploit_probability(self)` |
| `generate_recommendations` | method | `modules/integrations/nuclei_parser.py:300` | `def generate_recommendations(self, findings, rhost)` |
| `import_to_db` | method | `modules/integrations/nuclei_parser.py:196` | `def import_to_db(self, findings, rhost, workspace_name)` |
| `mitre_tactic` | method | `modules/integrations/nuclei_parser.py:87` | `def mitre_tactic(self)` |
| `parse_file` | method | `modules/integrations/nuclei_parser.py:177` | `def parse_file(self, filepath)` |
| `parse_json` | method | `modules/integrations/nuclei_parser.py:134` | `def parse_json(self, json_text)` |
| `parse_text` | method | `modules/integrations/nuclei_parser.py:115` | `def parse_text(self, text)` |
| `scan_and_import` | method | `modules/integrations/nuclei_parser.py:328` | `def scan_and_import(self, target, templates, services, cves, workspace_name)` |
| `ExploitDBAPI` | class | `modules/integrations/searchsploit.py:193` | `class ExploitDBAPI(ExploitSource)` |
| `ExploitEntry` | class | `modules/integrations/searchsploit.py:60` | `class ExploitEntry` |
| `ExploitSource` | class | `modules/integrations/searchsploit.py:76` | `class ExploitSource(ABC)` |
| `SearchsploitCLI` | class | `modules/integrations/searchsploit.py:93` | `class SearchsploitCLI(ExploitSource)` |
| `SearchsploitClient` | class | `modules/integrations/searchsploit.py:271` | `class SearchsploitClient` |
| `__init__` | method | `modules/integrations/searchsploit.py:102` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/searchsploit.py:201` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/searchsploit.py:278` | `def __init__(self, primary, fallback)` |
| `_extract_cve` | method | `modules/integrations/searchsploit.py:183` | `def _extract_cve(text)` |
| `_main` | function | `modules/integrations/searchsploit.py:356` | `def _main()` |
| `_parse` | method | `modules/integrations/searchsploit.py:133` | `def _parse(self, raw)` |
| `_query` | method | `modules/integrations/searchsploit.py:218` | `def _query(self, cve_id)` |
| `_rate_limit` | method | `modules/integrations/searchsploit.py:258` | `def _rate_limit()` |
| `_row_to_entry` | method | `modules/integrations/searchsploit.py:162` | `def _row_to_entry(self, row)` |
| `_run` | method | `modules/integrations/searchsploit.py:118` | `def _run(self, query)` |
| `enrich_findings` | method | `modules/integrations/searchsploit.py:300` | `def enrich_findings(self, findings)` |
| `get_client` | function | `modules/integrations/searchsploit.py:333` | `def get_client()` |
| `search_cve` | method | `modules/integrations/searchsploit.py:80` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:109` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:207` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:286` | `def search_cve(self, cve_id)` |
| `search_cve` | function | `modules/integrations/searchsploit.py:341` | `def search_cve(cve_id)` |
| `search_service` | method | `modules/integrations/searchsploit.py:84` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:112` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:210` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:293` | `def search_service(self, name, version)` |
| `search_service` | function | `modules/integrations/searchsploit.py:346` | `def search_service(name, version)` |
| `_enrich_readmenator_fields` | function | `modules/intel_fusion.py:428` | `def _enrich_readmenator_fields(nodes, edges)` |
| `_family_color` | function | `modules/intel_fusion.py:95` | `def _family_color(name)` |
| `_fibonacci_sphere` | function | `modules/intel_fusion.py:610` | `def _fibonacci_sphere(count)` |
| `_file_pagerank` | function | `modules/intel_fusion.py:146` | `def _file_pagerank(ids, pairs, alpha, max_iter, tol)` |
| `_host_mentions` | function | `modules/intel_fusion.py:139` | `def _host_mentions(text)` |
| `_load_json` | function | `modules/intel_fusion.py:112` | `def _load_json(path, default)` |
| `_node_doc` | function | `modules/intel_fusion.py:390` | `def _node_doc(node)` |
| `_read_lines` | function | `modules/intel_fusion.py:122` | `def _read_lines(path, limit)` |
| `_split_caps` | function | `modules/intel_fusion.py:626` | `def _split_caps(labels, sizes, points, lattice, out)` |
| `_symbol_list` | function | `modules/intel_fusion.py:413` | `def _symbol_list(node)` |
| `_unit` | function | `modules/intel_fusion.py:651` | `def _unit(vec)` |
| `add_edge` | function | `modules/intel_fusion.py:197` | `def add_edge(src, dst, kind, evidence, weight)` |
| `add_node` | function | `modules/intel_fusion.py:183` | `def add_node(kind, value, label)` |
| `assign_layout` | function | `modules/intel_fusion.py:800` | `def assign_layout(graph, mode)` |
| `build_analytics` | function | `modules/intel_fusion.py:585` | `def build_analytics(graph, summary)` |
| `build_bundle_payload` | function | `modules/intel_fusion.py:659` | `def build_bundle_payload(graph)` |
| `build_intel_graph` | function | `modules/intel_fusion.py:176` | `def build_intel_graph(sessions_dir, est_cap)` |
| `bundle_settings` | function | `modules/intel_fusion.py:769` | `def bundle_settings(graph)` |
| `group_colors` | function | `modules/intel_fusion.py:512` | `def group_colors(graph)` |
| `node_id` | function | `modules/intel_fusion.py:106` | `def node_id(kind, value)` |
| `page_settings` | function | `modules/intel_fusion.py:528` | `def page_settings(graph)` |
| `tag_source` | function | `modules/intel_fusion.py:205` | `def tag_source(nid, source)` |
| `write_summary` | function | `modules/intel_fusion.py:865` | `def write_summary(graph, sessions_dir)` |
| `CollectedFact` | class | `modules/intelligence_engine.py:78` | `class CollectedFact` |
| `CounterIntelFinding` | class | `modules/intelligence_engine.py:108` | `class CounterIntelFinding` |
| `IntelligenceAssessment` | class | `modules/intelligence_engine.py:93` | `class IntelligenceAssessment` |
| `IntelligenceConfig` | class | `modules/intelligence_engine.py:57` | `class IntelligenceConfig` |
| `IntelligenceEngine` | class | `modules/intelligence_engine.py:119` | `class IntelligenceEngine` |
| `__init__` | method | `modules/intelligence_engine.py:142` | `def __init__(self, config)` |
| `_correlate_creds_to_hosts` | method | `modules/intelligence_engine.py:565` | `def _correlate_creds_to_hosts(self)` |
| `_correlate_domains_to_infrastructure` | method | `modules/intelligence_engine.py:588` | `def _correlate_domains_to_infrastructure(self)` |
| `_correlate_services_to_vulns` | method | `modules/intelligence_engine.py:494` | `def _correlate_services_to_vulns(self)` |
| `_detect_killchain_gaps` | method | `modules/intelligence_engine.py:644` | `def _detect_killchain_gaps(self)` |
| `_is_placeholder` | method | `modules/intelligence_engine.py:925` | `def _is_placeholder(value)` |
| `_map_category_to_mitre` | method | `modules/intelligence_engine.py:700` | `def _map_category_to_mitre(category)` |
| `_match_known_vulns` | method | `modules/intelligence_engine.py:537` | `def _match_known_vulns(fact)` |
| `_rank_targets` | method | `modules/intelligence_engine.py:604` | `def _rank_targets(self)` |
| `analyze` | method | `modules/intelligence_engine.py:477` | `def analyze(self)` |
| `collect_from_estorides` | method | `modules/intelligence_engine.py:292` | `def collect_from_estorides(self, target)` |
| `collect_from_factstore` | method | `modules/intelligence_engine.py:415` | `def collect_from_factstore(self)` |
| `collect_from_nuclei` | method | `modules/intelligence_engine.py:334` | `def collect_from_nuclei(self, target)` |
| `collect_from_scan` | method | `modules/intelligence_engine.py:153` | `def collect_from_scan(self, target)` |
| `collect_from_tool` | method | `modules/intelligence_engine.py:255` | `def collect_from_tool(self, output, tool, host)` |
| `collect_from_yara` | method | `modules/intelligence_engine.py:376` | `def collect_from_yara(self, target_path)` |
| `disseminate` | method | `modules/intelligence_engine.py:765` | `def disseminate(self)` |
| `get_intel_report` | method | `modules/intelligence_engine.py:874` | `def get_intel_report(self)` |
| `get_intelligence_engine` | function | `modules/intelligence_engine.py:931` | `def get_intelligence_engine(config)` |
| `produce_counter_intelligence` | method | `modules/intelligence_engine.py:715` | `def produce_counter_intelligence(self)` |
| `produce_intelligence` | method | `modules/intelligence_engine.py:685` | `def produce_intelligence(self)` |
| `run_full_cycle` | method | `modules/intelligence_engine.py:845` | `def run_full_cycle(self, target)` |
| `Guard` | class | `modules/intercept.py:255` | `class Guard` |
| `InterceptAction` | class | `modules/intercept.py:21` | `class InterceptAction(str, Enum)` |
| `InterceptConfig` | class | `modules/intercept.py:33` | `class InterceptConfig` |
| `InterceptRule` | class | `modules/intercept.py:50` | `class InterceptRule` |
| `InterceptVerdict` | class | `modules/intercept.py:92` | `class InterceptVerdict` |
| `Interceptor` | class | `modules/intercept.py:154` | `class Interceptor` |
| `PendingApproval` | class | `modules/intercept.py:77` | `class PendingApproval` |
| `__init__` | method | `modules/intercept.py:157` | `def __init__(self, rules, ask_timeout_sec, timeout_action)` |
| `__init__` | method | `modules/intercept.py:258` | `def __init__(self, interceptor)` |
| `__post_init__` | method | `modules/intercept.py:61` | `def __post_init__(self)` |
| `add_rule` | method | `modules/intercept.py:177` | `def add_rule(self, rule)` |
| `approval_status` | method | `modules/intercept.py:249` | `def approval_status(self, approval_id)` |
| `attribution` | method | `modules/intercept.py:301` | `def attribution(self)` |
| `audit_log` | method | `modules/intercept.py:296` | `def audit_log(self, limit)` |
| `builtin_rules` | function | `modules/intercept.py:101` | `def builtin_rules()` |
| `check` | method | `modules/intercept.py:270` | `def check(self, tool, command)` |
| `decide` | method | `modules/intercept.py:220` | `def decide(self, approval_id, decision)` |
| `evaluate` | method | `modules/intercept.py:192` | `def evaluate(self, tool, command)` |
| `interceptor` | method | `modules/intercept.py:266` | `def interceptor(self)` |
| `matches` | method | `modules/intercept.py:68` | `def matches(self, tool, command)` |
| `observe` | method | `modules/intercept.py:282` | `def observe(self, output, source)` |
| `observe_post_tool` | function | `modules/intercept.py:144` | `def observe_post_tool(output)` |
| `pending_approvals` | method | `modules/intercept.py:234` | `def pending_approvals(self)` |
| `record_failure` | method | `modules/intercept.py:291` | `def record_failure(self, source)` |
| `remove_rule` | method | `modules/intercept.py:183` | `def remove_rule(self, pattern)` |
| `rules` | method | `modules/intercept.py:172` | `def rules(self)` |
| `scope_blocked` | function | `modules/intercept.py:131` | `def scope_blocked(target)` |
| `display_usage` | function | `modules/iptables_portforward.sh:29` | `` |
| `JsonlTail` | class | `modules/jsonl_tail.py:14` | `class JsonlTail` |
| `__init__` | method | `modules/jsonl_tail.py:17` | `def __init__(self, path)` |
| `read_new` | method | `modules/jsonl_tail.py:22` | `def read_new(self, limit)` |
| `K8SAttackEngine` | class | `modules/k8s_attacks.py:77` | `class K8SAttackEngine` |
| `K8sConfig` | class | `modules/k8s_attacks.py:57` | `class K8sConfig` |
| `__init__` | method | `modules/k8s_attacks.py:87` | `def __init__(self, config)` |
| `enumerate_rbac` | method | `modules/k8s_attacks.py:90` | `def enumerate_rbac(self)` |
| `etcd_access_exploitation` | method | `modules/k8s_attacks.py:222` | `def etcd_access_exploitation(self)` |
| `helm_tiller_abuse` | method | `modules/k8s_attacks.py:250` | `def helm_tiller_abuse(self)` |
| `kubelet_anonymous_auth_abuse` | method | `modules/k8s_attacks.py:198` | `def kubelet_anonymous_auth_abuse(self)` |
| `persistence_techniques` | method | `modules/k8s_attacks.py:278` | `def persistence_techniques(self)` |
| `privileged_pod_escape` | method | `modules/k8s_attacks.py:118` | `def privileged_pod_escape(self)` |
| `service_account_token_theft` | method | `modules/k8s_attacks.py:173` | `def service_account_token_theft(self)` |
| `summary` | method | `modules/k8s_attacks.py:318` | `def summary(self)` |
| `KerberoastHash` | class | `modules/kerberoasting.py:59` | `class KerberoastHash` |
| `KerberoastTarget` | class | `modules/kerberoasting.py:38` | `class KerberoastTarget` |
| `KerberoastingEngine` | class | `modules/kerberoasting.py:79` | `class KerberoastingEngine` |
| `__init__` | method | `modules/kerberoasting.py:95` | `def __init__(self, domain, dc_ip, username, password, hash)` |
| `_build_hash_string` | method | `modules/kerberoasting.py:248` | `def _build_hash_string(self, spn, etype)` |
| `_hashcat_command` | method | `modules/kerberoasting.py:268` | `def _hashcat_command(hash_str, mode)` |
| `_prioritize_targets` | method | `modules/kerberoasting.py:169` | `def _prioritize_targets(self)` |
| `asreproast_check` | method | `modules/kerberoasting.py:306` | `def asreproast_check(self, usernames)` |
| `build_hashcat_batch` | method | `modules/kerberoasting.py:379` | `def build_hashcat_batch(self, output_path)` |
| `detect_kerberoasting_activity` | method | `modules/kerberoasting.py:336` | `def detect_kerberoasting_activity(self, event_log)` |
| `enumerate_spns` | method | `modules/kerberoasting.py:112` | `def enumerate_spns(self, ldap_output, bloodhound_data)` |
| `extract_hashes_from_pcap` | method | `modules/kerberoasting.py:321` | `def extract_hashes_from_pcap(self, pcap_path)` |
| `priority` | function | `modules/kerberoasting.py:172` | `def priority(target)` |
| `request_tgs` | method | `modules/kerberoasting.py:219` | `def request_tgs(self, user_spn, etype)` |
| `request_tgs_aes_only` | method | `modules/kerberoasting.py:187` | `def request_tgs_aes_only(self, user_spn)` |
| `request_tgs_rc4` | method | `modules/kerberoasting.py:208` | `def request_tgs_rc4(self, user_spn)` |
| `summary` | method | `modules/kerberoasting.py:401` | `def summary(self)` |
| `targeted_kerberoast` | method | `modules/kerberoasting.py:271` | `def targeted_kerberoast(self, high_value_only)` |
| `EncryptedData` | class | `modules/kerberos_core.py:157` | `class EncryptedData` |
| `KerberosCore` | class | `modules/kerberos_core.py:407` | `class KerberosCore` |
| `KerberosCrypto` | class | `modules/kerberos_core.py:271` | `class KerberosCrypto` |
| `KerberosErrorParser` | class | `modules/kerberos_core.py:683` | `class KerberosErrorParser` |
| `KerberosPrincipal` | class | `modules/kerberos_core.py:139` | `class KerberosPrincipal` |
| `KerberosTicket` | class | `modules/kerberos_core.py:172` | `class KerberosTicket` |
| `PACInfo` | class | `modules/kerberos_core.py:228` | `class PACInfo` |
| `PACSignature` | class | `modules/kerberos_core.py:213` | `class PACSignature` |
| `TGSRequest` | class | `modules/kerberos_core.py:249` | `class TGSRequest` |
| `TicketValidator` | class | `modules/kerberos_core.py:702` | `class TicketValidator` |
| `__init__` | method | `modules/kerberos_core.py:277` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_core.py:421` | `def __init__(self, domain, dc_host, dc_ip)` |
| `_build_pa_enc_timestamp` | method | `modules/kerberos_core.py:640` | `def _build_pa_enc_timestamp(self, key, etype, timestamp)` |
| `_parse_kdc_rep` | method | `modules/kerberos_core.py:653` | `def _parse_kdc_rep(self, data, key, etype, rep_type)` |
| `_parse_pac_buffer` | method | `modules/kerberos_core.py:622` | `def _parse_pac_buffer(pac, buf_type, buf_data)` |
| `_rc4_decrypt` | method | `modules/kerberos_core.py:676` | `def _rc4_decrypt(key, data, usage)` |
| `_rc4_encrypt` | method | `modules/kerberos_core.py:667` | `def _rc4_encrypt(key, data, usage)` |
| `aes_decrypt` | method | `modules/kerberos_core.py:361` | `def aes_decrypt(self, key, ciphertext, usage)` |
| `aes_encrypt` | method | `modules/kerberos_core.py:329` | `def aes_encrypt(self, key, plaintext, usage)` |
| `build_as_req` | method | `modules/kerberos_core.py:435` | `def build_as_req(self, username, domain, password, etype)` |
| `build_tgs_req` | method | `modules/kerberos_core.py:489` | `def build_tgs_req(self, params)` |
| `compute_checksum` | method | `modules/kerberos_core.py:389` | `def compute_checksum(key, data, etype)` |
| `decrypt_ticket` | method | `modules/kerberos_core.py:563` | `def decrypt_ticket(self, ticket_data, key, etype)` |
| `derive_aes_key` | method | `modules/kerberos_core.py:282` | `def derive_aes_key(password, salt, etype)` |
| `derive_rc4_key` | method | `modules/kerberos_core.py:318` | `def derive_rc4_key(password)` |
| `get_supported_etypes` | method | `modules/kerberos_core.py:427` | `def get_supported_etypes(self)` |
| `has_flag` | method | `modules/kerberos_core.py:207` | `def has_flag(self, flag_name)` |
| `is_expired` | method | `modules/kerberos_core.py:706` | `def is_expired(endtime, grace_period)` |
| `parse_as_rep` | method | `modules/kerberos_core.py:534` | `def parse_as_rep(self, as_rep_data, key, etype)` |
| `parse_error` | method | `modules/kerberos_core.py:687` | `def parse_error(error_data)` |
| `parse_pac` | method | `modules/kerberos_core.py:588` | `def parse_pac(self, pac_data)` |
| `parse_tgs_rep` | method | `modules/kerberos_core.py:550` | `def parse_tgs_rep(self, tgs_rep_data, session_key, etype)` |
| `to_string` | method | `modules/kerberos_core.py:152` | `def to_string(self)` |
| `validate_flags` | method | `modules/kerberos_core.py:719` | `def validate_flags(ticket, required_flags)` |
| `validate_pac_checksums` | method | `modules/kerberos_core.py:735` | `def validate_pac_checksums(pac)` |
| `DiamondTicketConfig` | class | `modules/kerberos_tickets.py:94` | `class DiamondTicketConfig` |
| `DiamondTicketForger` | class | `modules/kerberos_tickets.py:397` | `class DiamondTicketForger` |
| `GoldenTicketConfig` | class | `modules/kerberos_tickets.py:65` | `class GoldenTicketConfig` |
| `GoldenTicketForger` | class | `modules/kerberos_tickets.py:265` | `class GoldenTicketForger` |
| `SapphireTicketForger` | class | `modules/kerberos_tickets.py:462` | `class SapphireTicketForger` |
| `SilverTicketConfig` | class | `modules/kerberos_tickets.py:36` | `class SilverTicketConfig` |
| `SilverTicketForger` | class | `modules/kerberos_tickets.py:124` | `class SilverTicketForger` |
| `SkeletonKeyInjector` | class | `modules/kerberos_tickets.py:567` | `class SkeletonKeyInjector` |
| `__init__` | method | `modules/kerberos_tickets.py:131` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:272` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:405` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_tickets.py:469` | `def __init__(self, kerberos_core)` |
| `_assemble_tgt` | method | `modules/kerberos_tickets.py:368` | `def _assemble_tgt(self, config, flags, enc_part)` |
| `_build_diamond_pac` | method | `modules/kerberos_tickets.py:446` | `def _build_diamond_pac(self, config)` |
| `_build_enc_ticket_part` | method | `modules/kerberos_tickets.py:206` | `def _build_enc_ticket_part(self, config, start, end, flags, key, etype)` |
| `_build_golden_enc_part` | method | `modules/kerberos_tickets.py:346` | `def _build_golden_enc_part(self, config, start, end, flags, key)` |

Next: [SYMBOLS_p15.md](SYMBOLS_p15.md)
