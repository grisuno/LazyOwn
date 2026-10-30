# Subsystem: modules (page 6 of 17)
Previous: [KB_modules_p5.md](KB_modules_p5.md)

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
- Depends on: `modules/outcome_bus.py`
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

## modules/factsio.py
- Doc: Canonical reader for the FactStore ``policy_facts.json`` document.
- Layer: utility
- Language: py
- Symbols:
  - `load_policy_facts` (function, line 39) `def load_policy_facts(path)`
  - `canonical_policy_facts` (function, line 61) `def canonical_policy_facts(data)`
  - `iter_host_records` (function, line 81) `def iter_host_records(host_keyed)`
  - `iter_flat_facts` (function, line 93) `def iter_flat_facts(host_keyed)`
  - `_iter_kind` (function, line 116) `def _iter_kind(record, key, fact_type, host)`
  - `_as_list` (function, line 131) `def _as_list(value)`
  - `_observable` (function, line 137) `def _observable(record, fact_type)`
- Depends on: `core/logging.py`
- Imported by: `modules/compliance.py`, `modules/intelligence_engine.py`, `modules/world_model.py`, `tests/test_single_source_of_truth.py`

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
  - `evidence_floor` (function, line 52) `def evidence_floor(items)`
  - `_store_path` (function, line 68) `def _store_path(sessions_dir)`
  - `_load` (function, line 73) `def _load(sessions_dir)`
  - `_save` (function, line 86) `def _save(sessions_dir, data)`
  - `confirm` (function, line 94) `def confirm(finding_id, evidence, sessions_dir, by)`
  - `reject` (function, line 123) `def reject(finding_id, reason, sessions_dir, by)`
  - `add_dead_end` (function, line 137) `def add_dead_end(kind, value, reason, sessions_dir)`
  - `is_dead_end` (function, line 149) `def is_dead_end(kind, value, sessions_dir)`
  - `suppressed_values` (function, line 156) `def suppressed_values(sessions_dir)`
  - `resolve` (function, line 162) `def resolve(node, sessions_dir)`
  - `apply_confirmation` (function, line 190) `def apply_confirmation(nodes, sessions_dir)`
  - `FindingRecord` (class, line 218) `class FindingRecord`
  - `RetestRecord` (class, line 231) `class RetestRecord`
  - `_token_value` (function, line 241) `def _token_value(refs, prefix, default)`
  - `_with_token` (function, line 249) `def _with_token(refs, prefix, value)`
  - `_finding_from_row` (function, line 256) `def _finding_from_row(row)`
  - `record` (function, line 270) `def record(db, workspace, host, title, severity, summary, poc)`
  - `findings_for` (function, line 295) `def findings_for(db, workspace)`
  - `set_status` (function, line 300) `def set_status(db, finding_id, status)`
  - `_retests_path` (function, line 323) `def _retests_path(sessions_dir)`
  - `_load_retests` (function, line 328) `def _load_retests(sessions_dir)`
  - `_save_retests` (function, line 339) `def _save_retests(sessions_dir, payload)`
  - `has_running_retest` (function, line 346) `def has_running_retest(finding_id, sessions_dir)`
  - `request_retest` (function, line 354) `def request_retest(db, finding_id, sessions_dir)`
  - `resolve_retest` (function, line 374) `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)`
  - `classify_retest` (function, line 420) `def classify_retest(needle, output)`
  - `render_markdown` (function, line 439) `def render_markdown(db, workspace, title)`
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
- Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `tests/test_lazy_parity.py`

## modules/golden_path.py
- Doc: Deterministic attack-path solver over the LazyOwn world model.
- Layer: utility
- Language: py
- Symbols:
  - `_host_node` (function, line 66) `def _host_node(ip)`
  - `_bare` (function, line 78) `def _bare(node)`
  - `_label` (function, line 97) `def _label(node)`
  - `_action_for` (function, line 113) `def _action_for(relation)`
  - `_cost_for_relation` (function, line 135) `def _cost_for_relation(relation, weight)`
  - `build_edges` (function, line 155) `def build_edges(snapshot)`
  - `_source_hosts` (function, line 227) `def _source_hosts(snapshot)`
  - `_diijkstra` (function, line 244) `def _diijkstra(adjacency, source)`
  - `resolve_paths` (function, line 274) `def resolve_paths(snapshot, top_k, source)`
  - `build` (function, line 350) `def build(world_model_path, top_k, sessions_dir)`
  - `_persist` (function, line 381) `def _persist(result, sessions_dir)`
  - `load_artifact` (function, line 401) `def load_artifact(sessions_dir)`
  - `priority_for` (function, line 418) `def priority_for(cost)`
  - `push_objectives` (function, line 433) `def push_objectives(paths, store_path)`
  - `_add` (function, line 167) `def _add(src, dst, relation, weight, evidence, cost)`
- Depends on: `core/logging.py`, `modules/world_model.py`, `skills/lazyown_objective.py`

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

## modules/gym_cleanup.py
- Doc: Gym machine cleanup on LazyOwn exit.
- Layer: utility
- Language: py
- Symbols:
  - `cleanup_enabled` (function, line 21) `def cleanup_enabled()`
  - `cleanup_gym_machines` (function, line 35) `def cleanup_gym_machines(verbose)`
- Depends on: `core/config.py`, `core/logging.py`, `modules/__init__.py`
- Imported by: `lazyown.py`, `tests/test_gym_lifecycle.py`

## modules/gym_matrix_runner.py
- Doc: Ordered Metasploitable 2 gym matrix runner.
- Layer: utility
- Language: py
- Symbols:
  - `_catalogue` (function, line 36) `def _catalogue(catalogue)`
  - `plan_matrix` (function, line 49) `def plan_matrix(target, sessions_dir, only, top_k, catalogue)`
  - `run_matrix` (function, line 104) `def run_matrix(target)`
  - `_stats` (function, line 220) `def _stats(runs)`
  - `_persist` (function, line 236) `def _persist(summary_result, sessions_dir)`
  - `load_matrix` (function, line 252) `def load_matrix(sessions_dir)`
- Depends on: `core/logging.py`, `modules/__init__.py`, `modules/chain_facts.py`, `modules/chain_registry.py`, `modules/chain_runner.py`

## modules/gym_registry.py
- Doc: Gym definitions and persistent run state.
- Layer: utility
- Language: py
- Symbols:
  - `_yaml_module` (function, line 85) `def _yaml_module()`
  - `slugify` (function, line 92) `def slugify(value)`
  - `validate_definition` (function, line 110) `def validate_definition(data, filename)`
  - `definition_path` (function, line 155) `def definition_path(gym_id, directory)`
  - `_read_yaml` (function, line 178) `def _read_yaml(path)`
  - `_normalize_definition` (function, line 188) `def _normalize_definition(data)`
  - `load_definitions` (function, line 207) `def load_definitions(directory)`
  - `scan_definitions` (function, line 239) `def scan_definitions(directory)`
  - `_write_yaml` (function, line 282) `def _write_yaml(path, data)`
  - `create_definition` (function, line 300) `def create_definition(gym_id)`
  - `update_definition_yaml` (function, line 369) `def update_definition_yaml(gym_id, text, directory)`
  - `delete_definition` (function, line 402) `def delete_definition(gym_id, directory)`
  - `_empty_state` (function, line 442) `def _empty_state()`
  - `_world_model` (function, line 447) `def _world_model()`
  - `_sanitize_state` (function, line 454) `def _sanitize_state(raw)`
  - `normalize_operator` (function, line 495) `def normalize_operator(value)`
  - `read_state` (function, line 501) `def read_state()`
  - `write_state` (function, line 520) `def write_state(state)`
  - `_merge_legacy` (function, line 532) `def _merge_legacy(state)`
  - `_next_run_id` (function, line 569) `def _next_run_id(state)`
  - `start_run` (function, line 579) `def start_run(challenge_id, definitions)`
  - `_matches` (function, line 625) `def _matches(run, selector)`
  - `get_active_runs` (function, line 637) `def get_active_runs(selector, operator)`
  - `select_run` (function, line 663) `def select_run(selector)`
  - `stop_runs` (function, line 695) `def stop_runs(selector)`
  - `pop_run` (function, line 724) `def pop_run(selector)`
  - `state_summary` (function, line 751) `def state_summary()`
  - `new_run_token` (function, line 761) `def new_run_token()`
- Depends on: `core/logging.py`, `modules/world_model.py`
- Imported by: `cli/orchestrator_assets_tabs.py`, `modules/redteam_gym.py`, `tests/test_gym_cli.py`, `tests/test_lazy_orchestrator.py`, `tests/test_winbox_gym.py`

## modules/gym_winbox_runner.py
- Doc: Ordered WinBox gym matrix runner.
- Layer: utility
- Language: py
- Symbols:
  - `plan_matrix` (function, line 21) `def plan_matrix(target, sessions_dir, only, top_k)`
  - `run_matrix` (function, line 51) `def run_matrix(target)`
  - `report` (function, line 118) `def report(sessions_dir)`
  - `chain_available` (function, line 130) `def chain_available(vuln_id)`
- Depends on: `core/logging.py`, `modules/__init__.py`, `modules/chain_registry.py`

## modules/harness.py
- Doc: Deterministic harness gate for the LazyOwn loop.
- Layer: utility
- Language: py
- Symbols:
  - `harness_enabled` (function, line 30) `def harness_enabled()`
  - `gate` (function, line 65) `def gate(name)`
- Depends on: `core/config.py`, `core/logging.py`, `modules/orchestrator_config.py`
- Imported by: `modules/lazy_loop.py`, `modules/llm_factory.py`, `skills/lazyown_mcp_opencode.py`

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


Next: [KB_modules_p7.md](KB_modules_p7.md)
