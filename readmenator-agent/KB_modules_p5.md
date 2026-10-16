# Subsystem: modules (page 5 of 14)
Previous: [KB_modules_p4.md](KB_modules_p4.md)

## modules/exp.c
- Doc: gcc exp.c -o exp -l mnl -l nftnl -w
- Layer: utility
- Language: c
- Symbols:
  - `keyring_payload` (struct, line 120)
  - `leak` (struct, line 126)
  - `fd_uring` (struct, line 131)
  - `msg` (struct, line 84)
  - `msg_header` (struct, line 90)
  - `Msg` (struct, line 100)
  - `user_rule_t` (struct, line 105)
  - `nft_trans_phase` (enum, line 77)
  - `key_serial_t` (type_alias, line 135) `typedef int32_t key_serial_t;`
  - `add_key` (function, line 147) `static inline key_serial_t add_key(const char *type, const char *description, const void *payload...`
  - `keyctl` (function, line 151) `static inline long keyctl(int operation, unsigned long arg2, unsigned long arg3, unsigned long ar...`
  - `bye` (function, line 155) `void bye(char *info)`
  - `do_error_exit` (function, line 161) `void do_error_exit(char *info)`
  - `bye2` (function, line 167) `void bye2(char *info, char *arg)`
  - `spray_keyring` (function, line 172) `key_serial_t *spray_keyring(uint32_t start, uint32_t spray_size)`
  - `spray_keyring_list_del_purpose` (function, line 190) `key_serial_t *spray_keyring_list_del_purpose(uint32_t spray_size, uint64_t next, uint64_t prev, u...`
  - `spray_keyring_list_overwrite_purpose` (function, line 214) `key_serial_t *spray_keyring_list_overwrite_purpose(uint32_t spray_size, uint64_t len, uint64_t of...`
  - `get_keyring_leak` (function, line 248) `int get_keyring_leak(key_serial_t *id_buffer, uint32_t id_buffer_size)`
  - `awake_partial_keys` (function, line 271) `void awake_partial_keys(key_serial_t *id_buffer, uint32_t idx)`
  - `release_keys` (function, line 279) `void release_keys(key_serial_t *id_buffer, uint32_t id_buffer_size)`
  - `release_partial_keys` (function, line 290) `void release_partial_keys(key_serial_t *id_buffer, int i)`
  - `unshare_setup` (function, line 297) `void unshare_setup(uid_t uid, gid_t gid)`
  - `set_stable_table_and_set` (function, line 322) `void set_stable_table_and_set(struct mnl_socket* nl, const char *name)`
  - `set_trigger_set_and_overwrite` (function, line 385) `void set_trigger_set_and_overwrite(struct mnl_socket* nl, const char *name, const char *set_name)`
  - `set_cpu_affinity` (function, line 438) `void set_cpu_affinity(int cpu_n, pid_t pid)`
  - `spray_mqueue` (function, line 448) `void spray_mqueue(mqd_t mqdes, char *msgptr, int spray_size)`
  - `gather_mqueue` (function, line 463) `int gather_mqueue(mqd_t mqdes, int gather_size)`
  - `gather_mqueue_nosave` (function, line 485) `int gather_mqueue_nosave(mqd_t mqdes, int gather_size)`
  - `spray_msg_msg` (function, line 496) `void spray_msg_msg(unsigned int size, unsigned int amount, int qid)`
  - `io_uring_setup` (function, line 520) `static inline int io_uring_setup(uint32_t entries, struct io_uring_params *p)`
  - `io_uring_register` (function, line 524) `static inline int io_uring_register(int fd, unsigned int opcode, void *arg, unsigned int nr_args)`
  - `spray_uring` (function, line 529) `struct fd_uring *spray_uring(uint32_t spray_size, struct fd_uring *fd_buffer)`
  - `release_uring` (function, line 546) `void release_uring(struct fd_uring *fd_buffer, uint32_t buffer_size)`
  - `release_partial_uring` (function, line 554) `void release_partial_uring(struct fd_uring *fd_buffer, uint32_t buffer_idx)`
  - `prepare_root_shell` (function, line 559) `void prepare_root_shell(void)`
  - `create_dummy_file` (function, line 564) `void create_dummy_file(void)`
  - `create_priv_file` (function, line 572) `void create_priv_file(void)`
  - `write_new_modprobe` (function, line 582) `void write_new_modprobe()`
  - `setup_modprobe_payload` (function, line 601) `void setup_modprobe_payload()`
  - `userland_T` (function, line 605) `void userland_T(int *sema)`
  - `sema_up` (function, line 610) `void sema_up(int *sema)`
  - `sema_down` (function, line 615) `void sema_down(int *sema)`
  - `main` (function, line 620) `int main(int argc, char ** argv)`
  - `_GNU_SOURCE` (macro, line 2) `#define _GNU_SOURCE`
  - `MQUEUE_NUM` (macro, line 49) `#define MQUEUE_NUM`
  - `INBOUND` (macro, line 52) `#define INBOUND`
  - `OUTBOUND` (macro, line 53) `#define OUTBOUND`
  - `DESC_MAX` (macro, line 54) `#define DESC_MAX`
  - `BUFFER` (macro, line 56) `#define BUFFER`
  - `NAMELEN` (macro, line 57) `#define NAMELEN`
  - `ERROR_PREFIX` (macro, line 58) `#define ERROR_PREFIX`
  - `KEY_DESC_MAX_SIZE` (macro, line 60) `#define KEY_DESC_MAX_SIZE`
  - `PREFIX_BUF_LEN` (macro, line 62) `#define PREFIX_BUF_LEN`
  - `RCU_HEAD_LEN` (macro, line 63) `#define RCU_HEAD_LEN`
  - `SPRAY_KEY_SIZE` (macro, line 65) `#define SPRAY_KEY_SIZE`
  - `PHYSMAP_MASK` (macro, line 67) `#define PHYSMAP_MASK`
  - `SPRAY_SIZE` (macro, line 69) `#define SPRAY_SIZE`
  - `SPRAY_NB_ENTRIES` (macro, line 71) `#define SPRAY_NB_ENTRIES`
- Imported by: `static/js/3d-force-graph-1.73.4.min.js`, `static/js/force-graph-1.43.5.min.js`

## modules/exploit_chain.py
- Doc: Autonomous exploitation chain engine.
- Layer: utility
- Language: py
- Symbols:
  - `ServiceInfo` (class, line 29) `class ServiceInfo`
  - `VulnerabilityMatch` (class, line 41) `class VulnerabilityMatch`
  - `ExploitResult` (class, line 54) `class ExploitResult`
  - `ChainResult` (class, line 65) `class ChainResult`
  - `_compare_versions` (function, line 266) `def _compare_versions(version_a, version_b)`
  - `ExploitChain` (class, line 289) `class ExploitChain`
  - `__init__` (method, line 292) `def __init__(self, rhost, rport, lhost, lport, sessions_dir, nmap_xml_path)`
  - `fingerprint_services` (method, line 311) `def fingerprint_services(self, nmap_output)`
  - `_discover_xml_files` (method, line 331) `def _discover_xml_files(self)`
  - `_parse_all_nmap_xml` (method, line 346) `def _parse_all_nmap_xml(self)`
  - `_is_richer` (method, line 361) `def _is_richer(new_svc, existing)`
  - `_parse_single_xml` (method, line 367) `def _parse_single_xml(self, xml_path)`
  - `_parse_nmap_text` (method, line 404) `def _parse_nmap_text(self, output)`
  - `map_vulnerabilities` (method, line 446) `def map_vulnerabilities(self)`
  - `_add_vuln` (method, line 485) `def _add_vuln(self, service, sig, version)`
  - `generate_exploit_plan` (method, line 499) `def generate_exploit_plan(self)`
  - `get_post_exploit_commands` (method, line 519) `def get_post_exploit_commands(self, platform)`
  - `generate_report` (method, line 531) `def generate_report(self)`
  - `save_report` (method, line 566) `def save_report(self, path)`
- Imported by: `cli/commands/exploit_migrated.py`

## modules/exploit_recommender.py
- Doc: AI-Powered Exploit Recommendation Engine for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `ExploitMatch` (class, line 37) `class ExploitMatch`
  - `ExploitRecommender` (class, line 50) `class ExploitRecommender`
  - `__init__` (method, line 120) `def __init__(self, world_model)`
  - `set_world_model` (method, line 129) `def set_world_model(self, world_model)`
  - `set_nvd_api_key` (method, line 132) `def set_nvd_api_key(self, key)`
  - `_load_exploitdb` (method, line 135) `def _load_exploitdb(self)`
  - `_extract_cve_ids` (method, line 161) `def _extract_cve_ids(text)`
  - `_compare_versions` (method, line 165) `def _compare_versions(version, max_vulnerable)`
  - `_query_nvd` (method, line 175) `def _query_nvd(self, cve_id)`
  - `_try_nvd` (method, line 211) `def _try_nvd(self, cve_id)`
  - `_generate_lazyown_commands` (method, line 214) `def _generate_lazyown_commands(self, cve_id, service, host_ip)`
  - `match_services` (method, line 244) `def match_services(self, hosts)`
  - `recommend` (method, line 337) `def recommend(self, hosts, top_n)`
  - `persist_recommendations` (method, line 370) `def persist_recommendations(self, matches)`
  - `format_for_llm` (method, line 390) `def format_for_llm(self, matches, max_items)`
  - `parse_version` (function, line 25) `def parse_version(v)`
- Depends on: `lazygui/version.py`, `modules/world_model.py`
- Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/pwn.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`

## modules/exploitgym_gym.py
- Doc: ExploitGym integration — real-world vulnerability-to-exploit benchmark.
- Layer: utility
- Language: py
- Symbols:
  - `_ensure_dir` (function, line 56) `def _ensure_dir()`
  - `_resolve_root` (function, line 61) `def _resolve_root(params)`
  - `_read_task_ids` (function, line 75) `def _read_task_ids(root)`
  - `_detect_domain` (function, line 96) `def _detect_domain(task_id)`
  - `check_readiness` (function, line 112) `def check_readiness(params)`
  - `list_tasks` (function, line 178) `def list_tasks(params, domain, limit)`
  - `_run_streaming` (function, line 206) `def _run_streaming(cmd, cwd, timeout)`
  - `_ensure_clone` (function, line 232) `def _ensure_clone(root, timeout)`
  - `setup_harness` (function, line 249) `def setup_harness(params, steps)`
  - `_env_for_run` (function, line 315) `def _env_for_run(params)`
  - `pull_task` (function, line 344) `def pull_task(task_id, params, timeout)`
  - `_run_agent` (function, line 378) `def _run_agent(task_id, model, mitigations, root, params, timeout)`
  - `run_task` (function, line 423) `def run_task(task_id, params, model, mitigations, timeout)`
  - `_extract_flag` (function, line 487) `def _extract_flag(output)`
  - `_load_records` (function, line 500) `def _load_records()`
  - `_save_records` (function, line 514) `def _save_records(records)`
  - `_record` (function, line 523) `def _record(task_id, success, elapsed, flag)`
  - `verify_flag` (function, line 548) `def verify_flag(task_id, params)`
  - `score_task` (function, line 565) `def score_task(task_id, success, techniques, params)`
  - `_run` (function, line 274) `def _run(name, cmd, cwd, timeout)`
- Depends on: `modules/redteam_gym.py`
- Imported by: `cli/commands/exploitgym.py`, `skills/lazyown_mcp.py`, `tests/test_exploitgym_gym.py`

## modules/fast_run_service.sh
- Doc: LazyOwn service-mode orchestrator.
- Layer: business_logic
- Language: sh
- Symbols:
  - `log_timestamp` (function, line 69)
  - `log_info` (function, line 73)
  - `log_warn` (function, line 77)
  - `log_error` (function, line 81)
  - `require_root` (function, line 89)
  - `require_deps` (function, line 97)
  - `require_paths` (function, line 113)
  - `prepare_runtime_dirs` (function, line 126)
  - `load_config` (function, line 139)
  - `config_truthy` (function, line 155)
  - `pid_file_for` (function, line 166)
  - `log_file_for` (function, line 171)
  - `read_pid_value` (function, line 176)
  - `is_pid_alive` (function, line 189)
  - `is_service_running` (function, line 194)
  - `write_pid_file` (function, line 201)
  - `ensure_log_file` (function, line 211)
  - `spawn_as_target_user` (function, line 228)
  - `spawn_as_root` (function, line 247)
  - `terminate_pid_tree` (function, line 264)
  - `stop_named_service` (function, line 292)
  - `chown_project_tree` (function, line 310)
  - `start_chown_watcher` (function, line 315)
  - `start_lazyc2_service` (function, line 342)
  - `start_www_service` (function, line 356)
  - `start_vpn_service` (function, line 363)
  - `start_discord_service` (function, line 380)
  - `start_telegram_service` (function, line 390)
  - `start_cloudflare_service` (function, line 400)
  - `start_ollama_service` (function, line 410)
  - `managed_services_in_order` (function, line 429)
  - `cmd_start` (function, line 445)
  - `cmd_stop` (function, line 465)
  - `cmd_restart` (function, line 480)
  - `cmd_status` (function, line 486)
  - `cmd_logs` (function, line 505)
  - `cmd_chown_now` (function, line 521)
  - `usage` (function, line 528)
  - `main` (function, line 557)

## modules/finding_lifecycle.py
- Doc: Finding confirmation lifecycle: pending -> confirmed / rejected.
- Layer: utility
- Language: py
- Symbols:
  - `_store_path` (function, line 35) `def _store_path(sessions_dir)`
  - `_load` (function, line 40) `def _load(sessions_dir)`
  - `_save` (function, line 53) `def _save(sessions_dir, data)`
  - `confirm` (function, line 61) `def confirm(finding_id, evidence, sessions_dir, by)`
  - `reject` (function, line 90) `def reject(finding_id, reason, sessions_dir, by)`
  - `add_dead_end` (function, line 104) `def add_dead_end(kind, value, reason, sessions_dir)`
  - `is_dead_end` (function, line 116) `def is_dead_end(kind, value, sessions_dir)`
  - `suppressed_values` (function, line 123) `def suppressed_values(sessions_dir)`
  - `resolve` (function, line 129) `def resolve(node, sessions_dir)`
  - `apply_confirmation` (function, line 154) `def apply_confirmation(nodes, sessions_dir)`
  - `FindingRecord` (class, line 182) `class FindingRecord`
  - `RetestRecord` (class, line 195) `class RetestRecord`
  - `_token_value` (function, line 205) `def _token_value(refs, prefix, default)`
  - `_with_token` (function, line 213) `def _with_token(refs, prefix, value)`
  - `_finding_from_row` (function, line 220) `def _finding_from_row(row)`
  - `record` (function, line 234) `def record(db, workspace, host, title, severity, summary, poc)`
  - `findings_for` (function, line 259) `def findings_for(db, workspace)`
  - `set_status` (function, line 264) `def set_status(db, finding_id, status)`
  - `_retests_path` (function, line 287) `def _retests_path(sessions_dir)`
  - `_load_retests` (function, line 292) `def _load_retests(sessions_dir)`
  - `_save_retests` (function, line 303) `def _save_retests(sessions_dir, payload)`
  - `has_running_retest` (function, line 310) `def has_running_retest(finding_id, sessions_dir)`
  - `request_retest` (function, line 318) `def request_retest(db, finding_id, sessions_dir)`
  - `resolve_retest` (function, line 338) `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)`
  - `classify_retest` (function, line 384) `def classify_retest(needle, output)`
  - `render_markdown` (function, line 403) `def render_markdown(db, workspace, title)`
- Depends on: `modules/osint_enrich.py`
- Imported by: `cli/commands/database.py`, `modules/attack_surface3d.py`, `modules/intel_fusion.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `tests/test_autonomous_ops.py`, `tests/test_finding_lifecycle.py`

## modules/forensic_cleaner.py
- Doc: Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup.
- Layer: utility
- Language: py
- Symbols:
  - `ForensicCleanerConfig` (class, line 23) `class ForensicCleanerConfig`
  - `ForensicCleaner` (class, line 57) `class ForensicCleaner`
  - `__init__` (method, line 67) `def __init__(self, config)`
  - `windows_cleanup` (method, line 70) `def windows_cleanup(self)`
  - `linux_cleanup` (method, line 165) `def linux_cleanup(self)`
  - `macos_cleanup` (method, line 193) `def macos_cleanup(self)`
  - `windows_prefetch_parse` (method, line 221) `def windows_prefetch_parse(self, prefetch_path)`
  - `amcache_parse` (method, line 259) `def amcache_parse(self)`
- Imported by: `cli/commands/opsec_cleanup.py`

## modules/gcp_attacks.py
- Doc: GCP privilege escalation — service account impersonation, Cloud Functions, GCS enumeration.
- Layer: utility
- Language: py
- Symbols:
  - `GCPConfig` (class, line 57) `class GCPConfig`
  - `GCPAttackEngine` (class, line 77) `class GCPAttackEngine`
  - `__init__` (method, line 90) `def __init__(self, config)`
  - `enumerate_iam_policy` (method, line 93) `def enumerate_iam_policy(self, resource)`
  - `service_account_impersonation` (method, line 119) `def service_account_impersonation(self)`
  - `cloud_functions_backdoor` (method, line 144) `def cloud_functions_backdoor(self)`
  - `compute_engine_metadata_exfil` (method, line 173) `def compute_engine_metadata_exfil(self)`
  - `gcs_enumeration` (method, line 194) `def gcs_enumeration(self)`
  - `cloudbuild_abuse` (method, line 230) `def cloudbuild_abuse(self)`
  - `organization_escalation` (method, line 261) `def organization_escalation(self)`
  - `summary` (method, line 297) `def summary(self)`
- Imported by: `cli/commands/cloud_attacks.py`

## modules/generate_tools.py
- Layer: utility
- Language: py
- Symbols:
  - `extract_cmd2_tools` (function, line 6) `def extract_cmd2_tools(script_path)`

## modules/goals.py
- Doc: Goal decomposition round-0 with constraints and proof.
- Layer: utility
- Language: py
- Symbols:
  - `GoalSpec` (class, line 20) `class GoalSpec`
  - `TaskConstraints` (class, line 29) `class TaskConstraints`
  - `decompose_rule_based` (function, line 63) `def decompose_rule_based(objective_text, max_goals)`
  - `load_constraints` (function, line 83) `def load_constraints(payload)`
  - `constraint_block_text` (function, line 103) `def constraint_block_text(constraints)`
  - `GoalTracker` (class, line 117) `class GoalTracker`
  - `blocked` (method, line 35) `def blocked(self, command)`
  - `__init__` (method, line 120) `def __init__(self, goals)`
  - `goals` (method, line 125) `def goals(self)`
  - `prove_goal` (method, line 129) `def prove_goal(self, goal_text, evidence)`
  - `goal_met` (method, line 140) `def goal_met(self, opt_in)`
  - `all_achieved` (method, line 148) `def all_achieved(self)`
  - `open_goals` (method, line 152) `def open_goals(self)`
- Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_parity.py`

## modules/gpo_abuse.py
- Doc: GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.
- Layer: utility
- Language: py
- Symbols:
  - `GPOInfo` (class, line 54) `class GPOInfo`
  - `GPOAbusePlan` (class, line 83) `class GPOAbusePlan`
  - `GPOAbuseEngine` (class, line 105) `class GPOAbuseEngine`
  - `__init__` (method, line 118) `def __init__(self, domain, dc_ip)`
  - `parse_gpo_list` (method, line 124) `def parse_gpo_list(self, raw_gpo_output)`
  - `parse_bloodhound_gpos` (method, line 160) `def parse_bloodhound_gpos(self, bloodhound_nodes)`
  - `plan_scheduled_task` (method, line 182) `def plan_scheduled_task(self, gpo, command, task_name)`
  - `plan_startup_script` (method, line 208) `def plan_startup_script(self, gpo, script_content, script_name)`
  - `plan_logon_script` (method, line 238) `def plan_logon_script(self, gpo, command)`
  - `plan_local_admin_addition` (method, line 266) `def plan_local_admin_addition(self, gpo, username, group)`
  - `plan_wmi_filter_abuse` (method, line 293) `def plan_wmi_filter_abuse(self, gpo, wmi_query)`
  - `plan_registry_preference` (method, line 322) `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)`
  - `plan_service_installation` (method, line 356) `def plan_service_installation(self, gpo, service_name, binary_path)`
  - `generate_all_plans` (method, line 382) `def generate_all_plans(self, command, username)`
  - `detect_risky_gpos` (method, line 406) `def detect_risky_gpos(self)`
  - `summary` (method, line 434) `def summary(self)`
- Imported by: `cli/commands/active_directory.py`

## modules/gui_askpass.sh
- Doc: — SUDO_ASKPASS helper for LazyOwn MCP  Used by: sudo -A <script>  (set SUDO_ASKPASS to this...
- Layer: utility
- Language: sh
- Symbols:
  - `has` (function, line 22)
  - `try_zenity` (function, line 24)
  - `try_yad` (function, line 28)
  - `try_ssh_askpass` (function, line 33)
  - `try_kdialog` (function, line 40)

## modules/hash_cracker.py
- Doc: Hash cracking pipeline — John the Ripper and Hashcat integration.
- Layer: utility
- Language: py
- Symbols:
  - `CrackResult` (class, line 127) `class CrackResult`
  - `HashIdentifier` (class, line 140) `class HashIdentifier`
  - `HashCracker` (class, line 151) `class HashCracker`
  - `crack_secretsdump_output` (function, line 695) `def crack_secretsdump_output(filepath, wordlist, rhost)`
  - `__init__` (method, line 164) `def __init__(self, wordlist, rules, use_hashcat, timeout)`
  - `_resolve_wordlist` (method, line 178) `def _resolve_wordlist(self)`
  - `identify` (method, line 186) `def identify(self, line)`
  - `identify_file` (method, line 273) `def identify_file(self, filepath)`
  - `crack_hash` (method, line 295) `def crack_hash(self, hash_value, hash_type, wordlist)`
  - `crack_file` (method, line 349) `def crack_file(self, filepath, wordlist, hash_types)`
  - `import_to_db` (method, line 405) `def import_to_db(self, results, rhost, workspace_name)`
  - `_crack_hashcat` (method, line 454) `def _crack_hashcat(self, hash_value, hash_type, fmt_info, wordlist)`
  - `_crack_batch_hashcat` (method, line 500) `def _crack_batch_hashcat(self, idents, hash_type, fmt_info, wordlist)`
  - `_crack_john` (method, line 560) `def _crack_john(self, hash_value, hash_type, fmt_info, wordlist)`
  - `_crack_batch_john` (method, line 610) `def _crack_batch_john(self, idents, hash_type, fmt_info, wordlist)`
  - `_parse_hashcat_output` (method, line 671) `def _parse_hashcat_output(stdout, stderr, original)`
  - `_parse_john_show` (method, line 686) `def _parse_john_show(show_output, original)`
- Depends on: `core/defaults.py`, `core/logging.py`, `modules/db.py`
- Imported by: `cli/commands/security.py`, `tests/test_hash_cracker.py`

## modules/hive_invoke.py
- Doc: modules/hive_invoke.py
- Layer: utility
- Language: py
- Symbols:
  - `_get_toposwarm` (function, line 50) `def _get_toposwarm()`
  - `_find_claude` (function, line 115) `def _find_claude()`
  - `_parse_argv` (function, line 120) `def _parse_argv(argv)`
  - `_run_print_mode` (function, line 150) `def _run_print_mode(prompt, effort, claude_bin)`
  - `_run_interactive_mode` (function, line 172) `def _run_interactive_mode(prompt, effort, claude_bin)`
  - `_run_toposwarm_mode` (function, line 205) `def _run_toposwarm_mode(prompt, effort, bridge)`
  - `main` (function, line 255) `def main(argv)`
- Depends on: `modules/toposwarm_bridge.py`

## modules/hostdiscover.sh
- Layer: utility
- Language: sh
- Symbols:
  - `extract_ips_from_arp` (function, line 21)
  - `extract_listening_ips_from_netstat` (function, line 26)

## modules/ia_code_analysis.py
- Doc: CodeAnalyzer: Analyzes source code in a directory and its subdirectories.
- Layer: utility
- Language: py
- Symbols:
  - `CodeAnalyzer` (class, line 28) `class CodeAnalyzer`
  - `analyze_with_deepseek` (function, line 66) `def analyze_with_deepseek(code_content, file_path, mode)`
  - `save_results_to_json` (function, line 123) `def save_results_to_json(results, file_path)`
  - `start_analysis` (function, line 169) `def start_analysis(code_dir, mode)`
  - `parse_args` (function, line 178) `def parse_args()`
  - `__init__` (method, line 33) `def __init__(self, mode)`
  - `analyze_directory` (method, line 37) `def analyze_directory(self, directory)`
  - `analyze_code_file` (method, line 49) `def analyze_code_file(self, file_path)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/ia_logs_analysis.py
- Doc: Author: Your Name Email: youremail@example.com Creation Date: 10/06/2024 License: GPL v3...
- Layer: utility
- Language: py
- Symbols:
  - `LogFileHandler` (class, line 54) `class LogFileHandler(FileSystemEventHandler)`
  - `analyze_with_deepseek` (function, line 94) `def analyze_with_deepseek(log_content, mode)`
  - `start_monitoring` (function, line 147) `def start_monitoring(log_dir, mode)`
  - `parse_args` (function, line 168) `def parse_args()`
  - `__init__` (method, line 59) `def __init__(self, mode)`
  - `on_modified` (method, line 64) `def on_modified(self, event)`
  - `analyze_log_file` (method, line 75) `def analyze_log_file(self, file_path)`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/ia_network_analysis.py
- Doc: Autor: grisun0 Fecha de creación: 30/01/2025 Licencia: GPL v3  Descripción: Bot de monitoreo de...
- Layer: utility
- Language: py
- Symbols:
  - `analyze_with_deepseek` (function, line 39) `def analyze_with_deepseek(packet_info, mode)`
  - `packet_callback` (function, line 91) `def packet_callback(packet, mode)`
  - `start_monitoring` (function, line 130) `def start_monitoring(interface, timeout, mode)`
  - `parse_args` (function, line 154) `def parse_args()`
- Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`

## modules/icmp_client.py
- Doc: encrypt_data: Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- Layer: infrastructure
- Language: py
- Symbols:
  - `encrypt_data` (function, line 18) `def encrypt_data(data, key)`
  - `decrypt_data` (function, line 34) `def decrypt_data(data, key)`
  - `check_sudo` (function, line 57) `def check_sudo()`
  - `checksum` (function, line 64) `def checksum(source_string)`
  - `send_icmp_packet` (function, line 82) `def send_icmp_packet(dest_addr, data, key)`
  - `receive_icmp_reply` (function, line 117) `def receive_icmp_reply(sock)`
  - `main` (function, line 130) `def main()`

## modules/icmp_server.py
- Doc: encrypt_data: Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 44) `def check_sudo()`
  - `encrypt_data` (function, line 55) `def encrypt_data(data, key)`
  - `decrypt_data` (function, line 71) `def decrypt_data(data, key)`
  - `execute_command` (function, line 93) `def execute_command(command)`
  - `send_icmp_reply` (function, line 112) `def send_icmp_reply(sock, addr, data, key)`
  - `checksum` (function, line 132) `def checksum(source_string)`
  - `handle_packet` (function, line 150) `def handle_packet(packet, addr, key, sock)`
  - `listen_for_icmp` (function, line 175) `def listen_for_icmp(interface, key)`
  - `main` (function, line 202) `def main()`
- Depends on: `core/logging.py`, `modules/logging_config.py`
- Imported by: `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`

## modules/img2bin.py
- Layer: utility
- Language: py
- Symbols:
  - `imagen_a_binario` (function, line 7) `def imagen_a_binario(imagen_input, binario_output, block_size)`
  - `main` (function, line 43) `def main()`

## modules/intel_fusion.py
- Doc: Sessions attack-intel fusion: data -> information -> intelligence.
- Layer: utility
- Language: py
- Symbols:
  - `_family_color` (function, line 95) `def _family_color(name)`
  - `node_id` (function, line 106) `def node_id(kind, value)`
  - `_load_json` (function, line 112) `def _load_json(path, default)`
  - `_read_lines` (function, line 122) `def _read_lines(path, limit)`
  - `_host_mentions` (function, line 139) `def _host_mentions(text)`
  - `_file_pagerank` (function, line 146) `def _file_pagerank(ids, pairs, alpha, max_iter, tol)`
  - `build_intel_graph` (function, line 176) `def build_intel_graph(sessions_dir, est_cap)`
  - `_node_doc` (function, line 390) `def _node_doc(node)`
  - `_symbol_list` (function, line 413) `def _symbol_list(node)`
  - `_enrich_readmenator_fields` (function, line 428) `def _enrich_readmenator_fields(nodes, edges)`
  - `group_colors` (function, line 512) `def group_colors(graph)`
  - `page_settings` (function, line 528) `def page_settings(graph)`
  - `build_analytics` (function, line 585) `def build_analytics(graph, summary)`
  - `_fibonacci_sphere` (function, line 610) `def _fibonacci_sphere(count)`
  - `_split_caps` (function, line 626) `def _split_caps(labels, sizes, points, lattice, out)`
  - `_unit` (function, line 651) `def _unit(vec)`
  - `build_bundle_payload` (function, line 659) `def build_bundle_payload(graph)`
  - `bundle_settings` (function, line 769) `def bundle_settings(graph)`
  - `assign_layout` (function, line 800) `def assign_layout(graph, mode)`
  - `write_summary` (function, line 865) `def write_summary(graph, sessions_dir)`
  - `add_node` (function, line 183) `def add_node(kind, value, label)`
  - `add_edge` (function, line 197) `def add_edge(src, dst, kind, evidence, weight)`
  - `tag_source` (function, line 205) `def tag_source(nid, source)`
- Depends on: `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`
- Imported by: `lazyc2.py`, `modules/atomic_exploit_bridge.py`, `modules/attack_surface3d.py`, `tests/test_asset_gate.py`, `tests/test_attack_surface3d.py`, `tests/test_intel_fusion.py`


Next: [KB_modules_p6.md](KB_modules_p6.md)
