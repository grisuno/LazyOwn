# Symbols (page 14 of 45)
Previous: [SYMBOLS_p13.md](SYMBOLS_p13.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `garbage_collect` | method | `modules/evidence.py:105` | `def garbage_collect(self, referenced)` |
| `get` | method | `modules/evidence.py:90` | `def get(self, content_hash)` |
| `hash_bytes` | function | `modules/evidence.py:37` | `def hash_bytes(data)` |
| `put` | method | `modules/evidence.py:70` | `def put(self, data)` |
| `BUFFER` | macro | `modules/exp.c:56` | `#define BUFFER` |
| `DESC_MAX` | macro | `modules/exp.c:54` | `#define DESC_MAX` |
| `ERROR_PREFIX` | macro | `modules/exp.c:58` | `#define ERROR_PREFIX` |
| `INBOUND` | macro | `modules/exp.c:52` | `#define INBOUND` |
| `KEY_DESC_MAX_SIZE` | macro | `modules/exp.c:60` | `#define KEY_DESC_MAX_SIZE` |
| `MQUEUE_NUM` | macro | `modules/exp.c:49` | `#define MQUEUE_NUM` |
| `Msg` | struct | `modules/exp.c:100` | `` |
| `NAMELEN` | macro | `modules/exp.c:57` | `#define NAMELEN` |
| `OUTBOUND` | macro | `modules/exp.c:53` | `#define OUTBOUND` |
| `PHYSMAP_MASK` | macro | `modules/exp.c:67` | `#define PHYSMAP_MASK` |
| `PREFIX_BUF_LEN` | macro | `modules/exp.c:62` | `#define PREFIX_BUF_LEN` |
| `RCU_HEAD_LEN` | macro | `modules/exp.c:63` | `#define RCU_HEAD_LEN` |
| `SPRAY_KEY_SIZE` | macro | `modules/exp.c:65` | `#define SPRAY_KEY_SIZE` |
| `SPRAY_NB_ENTRIES` | macro | `modules/exp.c:71` | `#define SPRAY_NB_ENTRIES` |
| `SPRAY_SIZE` | macro | `modules/exp.c:69` | `#define SPRAY_SIZE` |
| `_GNU_SOURCE` | macro | `modules/exp.c:2` | `#define _GNU_SOURCE` |
| `add_key` | function | `modules/exp.c:147` | `static inline key_serial_t add_key(const char *type, const char *description, const void *payload...` |
| `awake_partial_keys` | function | `modules/exp.c:271` | `void awake_partial_keys(key_serial_t *id_buffer, uint32_t idx)` |
| `bye` | function | `modules/exp.c:155` | `void bye(char *info)` |
| `bye2` | function | `modules/exp.c:167` | `void bye2(char *info, char *arg)` |
| `create_dummy_file` | function | `modules/exp.c:564` | `void create_dummy_file(void)` |
| `create_priv_file` | function | `modules/exp.c:572` | `void create_priv_file(void)` |
| `do_error_exit` | function | `modules/exp.c:161` | `void do_error_exit(char *info)` |
| `fd_uring` | struct | `modules/exp.c:131` | `` |
| `gather_mqueue` | function | `modules/exp.c:463` | `int gather_mqueue(mqd_t mqdes, int gather_size)` |
| `gather_mqueue_nosave` | function | `modules/exp.c:485` | `int gather_mqueue_nosave(mqd_t mqdes, int gather_size)` |
| `get_keyring_leak` | function | `modules/exp.c:248` | `int get_keyring_leak(key_serial_t *id_buffer, uint32_t id_buffer_size)` |
| `io_uring_register` | function | `modules/exp.c:524` | `static inline int io_uring_register(int fd, unsigned int opcode, void *arg, unsigned int nr_args)` |
| `io_uring_setup` | function | `modules/exp.c:520` | `static inline int io_uring_setup(uint32_t entries, struct io_uring_params *p)` |
| `key_serial_t` | type_alias | `modules/exp.c:135` | `typedef int32_t key_serial_t;` |
| `keyctl` | function | `modules/exp.c:151` | `static inline long keyctl(int operation, unsigned long arg2, unsigned long arg3, unsigned long ar...` |
| `keyring_payload` | struct | `modules/exp.c:120` | `` |
| `leak` | struct | `modules/exp.c:126` | `` |
| `main` | function | `modules/exp.c:620` | `int main(int argc, char ** argv)` |
| `msg` | struct | `modules/exp.c:84` | `` |
| `msg_header` | struct | `modules/exp.c:90` | `` |
| `nft_trans_phase` | enum | `modules/exp.c:77` | `` |
| `prepare_root_shell` | function | `modules/exp.c:559` | `void prepare_root_shell(void)` |
| `release_keys` | function | `modules/exp.c:279` | `void release_keys(key_serial_t *id_buffer, uint32_t id_buffer_size)` |
| `release_partial_keys` | function | `modules/exp.c:290` | `void release_partial_keys(key_serial_t *id_buffer, int i)` |
| `release_partial_uring` | function | `modules/exp.c:554` | `void release_partial_uring(struct fd_uring *fd_buffer, uint32_t buffer_idx)` |
| `release_uring` | function | `modules/exp.c:546` | `void release_uring(struct fd_uring *fd_buffer, uint32_t buffer_size)` |
| `sema_down` | function | `modules/exp.c:615` | `void sema_down(int *sema)` |
| `sema_up` | function | `modules/exp.c:610` | `void sema_up(int *sema)` |
| `set_cpu_affinity` | function | `modules/exp.c:438` | `void set_cpu_affinity(int cpu_n, pid_t pid)` |
| `set_stable_table_and_set` | function | `modules/exp.c:322` | `void set_stable_table_and_set(struct mnl_socket* nl, const char *name)` |
| `set_trigger_set_and_overwrite` | function | `modules/exp.c:385` | `void set_trigger_set_and_overwrite(struct mnl_socket* nl, const char *name, const char *set_name)` |
| `setup_modprobe_payload` | function | `modules/exp.c:601` | `void setup_modprobe_payload()` |
| `spray_keyring` | function | `modules/exp.c:172` | `key_serial_t *spray_keyring(uint32_t start, uint32_t spray_size)` |
| `spray_keyring_list_del_purpose` | function | `modules/exp.c:190` | `key_serial_t *spray_keyring_list_del_purpose(uint32_t spray_size, uint64_t next, uint64_t prev, u...` |
| `spray_keyring_list_overwrite_purpose` | function | `modules/exp.c:214` | `key_serial_t *spray_keyring_list_overwrite_purpose(uint32_t spray_size, uint64_t len, uint64_t of...` |
| `spray_mqueue` | function | `modules/exp.c:448` | `void spray_mqueue(mqd_t mqdes, char *msgptr, int spray_size)` |
| `spray_msg_msg` | function | `modules/exp.c:496` | `void spray_msg_msg(unsigned int size, unsigned int amount, int qid)` |
| `spray_uring` | function | `modules/exp.c:529` | `struct fd_uring *spray_uring(uint32_t spray_size, struct fd_uring *fd_buffer)` |
| `unshare_setup` | function | `modules/exp.c:297` | `void unshare_setup(uid_t uid, gid_t gid)` |
| `user_rule_t` | struct | `modules/exp.c:105` | `` |
| `userland_T` | function | `modules/exp.c:605` | `void userland_T(int *sema)` |
| `write_new_modprobe` | function | `modules/exp.c:582` | `void write_new_modprobe()` |
| `ChainResult` | class | `modules/exploit_chain.py:65` | `class ChainResult` |
| `ExploitChain` | class | `modules/exploit_chain.py:289` | `class ExploitChain` |
| `ExploitResult` | class | `modules/exploit_chain.py:54` | `class ExploitResult` |
| `ServiceInfo` | class | `modules/exploit_chain.py:29` | `class ServiceInfo` |
| `VulnerabilityMatch` | class | `modules/exploit_chain.py:41` | `class VulnerabilityMatch` |
| `__init__` | method | `modules/exploit_chain.py:292` | `def __init__(self, rhost, rport, lhost, lport, sessions_dir, nmap_xml_path)` |
| `_add_vuln` | method | `modules/exploit_chain.py:485` | `def _add_vuln(self, service, sig, version)` |
| `_compare_versions` | function | `modules/exploit_chain.py:266` | `def _compare_versions(version_a, version_b)` |
| `_discover_xml_files` | method | `modules/exploit_chain.py:331` | `def _discover_xml_files(self)` |
| `_is_richer` | method | `modules/exploit_chain.py:361` | `def _is_richer(new_svc, existing)` |
| `_parse_all_nmap_xml` | method | `modules/exploit_chain.py:346` | `def _parse_all_nmap_xml(self)` |
| `_parse_nmap_text` | method | `modules/exploit_chain.py:404` | `def _parse_nmap_text(self, output)` |
| `_parse_single_xml` | method | `modules/exploit_chain.py:367` | `def _parse_single_xml(self, xml_path)` |
| `fingerprint_services` | method | `modules/exploit_chain.py:311` | `def fingerprint_services(self, nmap_output)` |
| `generate_exploit_plan` | method | `modules/exploit_chain.py:499` | `def generate_exploit_plan(self)` |
| `generate_report` | method | `modules/exploit_chain.py:531` | `def generate_report(self)` |
| `get_post_exploit_commands` | method | `modules/exploit_chain.py:519` | `def get_post_exploit_commands(self, platform)` |
| `map_vulnerabilities` | method | `modules/exploit_chain.py:446` | `def map_vulnerabilities(self)` |
| `save_report` | method | `modules/exploit_chain.py:566` | `def save_report(self, path)` |
| `ExploitMatch` | class | `modules/exploit_recommender.py:37` | `class ExploitMatch` |
| `ExploitRecommender` | class | `modules/exploit_recommender.py:50` | `class ExploitRecommender` |
| `__init__` | method | `modules/exploit_recommender.py:120` | `def __init__(self, world_model)` |
| `_compare_versions` | method | `modules/exploit_recommender.py:165` | `def _compare_versions(version, max_vulnerable)` |
| `_extract_cve_ids` | method | `modules/exploit_recommender.py:161` | `def _extract_cve_ids(text)` |
| `_generate_lazyown_commands` | method | `modules/exploit_recommender.py:214` | `def _generate_lazyown_commands(self, cve_id, service, host_ip)` |
| `_load_exploitdb` | method | `modules/exploit_recommender.py:135` | `def _load_exploitdb(self)` |
| `_query_nvd` | method | `modules/exploit_recommender.py:175` | `def _query_nvd(self, cve_id)` |
| `_try_nvd` | method | `modules/exploit_recommender.py:211` | `def _try_nvd(self, cve_id)` |
| `format_for_llm` | method | `modules/exploit_recommender.py:390` | `def format_for_llm(self, matches, max_items)` |
| `match_services` | method | `modules/exploit_recommender.py:244` | `def match_services(self, hosts)` |
| `parse_version` | function | `modules/exploit_recommender.py:25` | `def parse_version(v)` |
| `persist_recommendations` | method | `modules/exploit_recommender.py:370` | `def persist_recommendations(self, matches)` |
| `recommend` | method | `modules/exploit_recommender.py:337` | `def recommend(self, hosts, top_n)` |
| `set_nvd_api_key` | method | `modules/exploit_recommender.py:132` | `def set_nvd_api_key(self, key)` |
| `set_world_model` | method | `modules/exploit_recommender.py:129` | `def set_world_model(self, world_model)` |
| `_detect_domain` | function | `modules/exploitgym_gym.py:96` | `def _detect_domain(task_id)` |
| `_ensure_clone` | function | `modules/exploitgym_gym.py:232` | `def _ensure_clone(root, timeout)` |
| `_ensure_dir` | function | `modules/exploitgym_gym.py:56` | `def _ensure_dir()` |
| `_env_for_run` | function | `modules/exploitgym_gym.py:315` | `def _env_for_run(params)` |
| `_extract_flag` | function | `modules/exploitgym_gym.py:487` | `def _extract_flag(output)` |
| `_load_records` | function | `modules/exploitgym_gym.py:500` | `def _load_records()` |
| `_read_task_ids` | function | `modules/exploitgym_gym.py:75` | `def _read_task_ids(root)` |
| `_record` | function | `modules/exploitgym_gym.py:523` | `def _record(task_id, success, elapsed, flag)` |
| `_resolve_root` | function | `modules/exploitgym_gym.py:61` | `def _resolve_root(params)` |
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
| `_as_list` | function | `modules/factsio.py:131` | `def _as_list(value)` |
| `_iter_kind` | function | `modules/factsio.py:116` | `def _iter_kind(record, key, fact_type, host)` |
| `_observable` | function | `modules/factsio.py:137` | `def _observable(record, fact_type)` |
| `canonical_policy_facts` | function | `modules/factsio.py:61` | `def canonical_policy_facts(data)` |
| `iter_flat_facts` | function | `modules/factsio.py:93` | `def iter_flat_facts(host_keyed)` |
| `iter_host_records` | function | `modules/factsio.py:81` | `def iter_host_records(host_keyed)` |
| `load_policy_facts` | function | `modules/factsio.py:39` | `def load_policy_facts(path)` |
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
| `_action_for` | function | `modules/golden_path.py:113` | `def _action_for(relation)` |
| `_add` | function | `modules/golden_path.py:167` | `def _add(src, dst, relation, weight, evidence, cost)` |
| `_bare` | function | `modules/golden_path.py:78` | `def _bare(node)` |
| `_cost_for_relation` | function | `modules/golden_path.py:135` | `def _cost_for_relation(relation, weight)` |
| `_diijkstra` | function | `modules/golden_path.py:244` | `def _diijkstra(adjacency, source)` |
| `_host_node` | function | `modules/golden_path.py:66` | `def _host_node(ip)` |
| `_label` | function | `modules/golden_path.py:97` | `def _label(node)` |
| `_persist` | function | `modules/golden_path.py:381` | `def _persist(result, sessions_dir)` |
| `_source_hosts` | function | `modules/golden_path.py:227` | `def _source_hosts(snapshot)` |
| `build` | function | `modules/golden_path.py:350` | `def build(world_model_path, top_k, sessions_dir)` |
| `build_edges` | function | `modules/golden_path.py:155` | `def build_edges(snapshot)` |
| `load_artifact` | function | `modules/golden_path.py:401` | `def load_artifact(sessions_dir)` |
| `priority_for` | function | `modules/golden_path.py:418` | `def priority_for(cost)` |
| `push_objectives` | function | `modules/golden_path.py:433` | `def push_objectives(paths, store_path)` |
| `resolve_paths` | function | `modules/golden_path.py:274` | `def resolve_paths(snapshot, top_k, source)` |
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
| `AdvisoryLedger` | class | `modules/guardrails/advisories.py:17` | `class AdvisoryLedger` |
| `FeatureGate` | class | `modules/guardrails/advisories.py:71` | `class FeatureGate` |
| `__init__` | method | `modules/guardrails/advisories.py:20` | `def __init__(self, limit)` |
| `__init__` | method | `modules/guardrails/advisories.py:74` | `def __init__(self, features)` |
| `clear` | method | `modules/guardrails/advisories.py:54` | `def clear(self)` |
| `describe` | method | `modules/guardrails/advisories.py:61` | `def describe(self)` |
| `describe` | method | `modules/guardrails/advisories.py:125` | `def describe(self)` |
| `is_suspended` | method | `modules/guardrails/advisories.py:115` | `def is_suspended(self, feature)` |
| `notice` | method | `modules/guardrails/advisories.py:31` | `def notice(self, code, message)` |
| `resume` | method | `modules/guardrails/advisories.py:102` | `def resume(self, feature)` |
| `resume_all` | method | `modules/guardrails/advisories.py:108` | `def resume_all(self)` |
| `suspend` | method | `modules/guardrails/advisories.py:84` | `def suspend(self, feature, reason)` |
| `suspended` | method | `modules/guardrails/advisories.py:120` | `def suspended(self)` |
| `tail` | method | `modules/guardrails/advisories.py:49` | `def tail(self, limit)` |
| `tail_locked` | method | `modules/guardrails/advisories.py:66` | `def tail_locked(self, limit)` |
| `CapacityEnvelope` | class | `modules/guardrails/budget.py:25` | `class CapacityEnvelope` |
| `__init__` | method | `modules/guardrails/budget.py:28` | `def __init__(self, capacities, threshold)` |
| `_default_capacities` | method | `modules/guardrails/budget.py:42` | `def _default_capacities()` |
| `_snapshot_locked` | method | `modules/guardrails/budget.py:176` | `def _snapshot_locked(self)` |
| `_usage_ratio` | method | `modules/guardrails/budget.py:171` | `def _usage_ratio(self, tier)` |
| `account` | method | `modules/guardrails/budget.py:109` | `def account(self, task_class, units)` |
| `admit` | method | `modules/guardrails/budget.py:78` | `def admit(self, task_class, units)` |
| `capacity` | method | `modules/guardrails/budget.py:147` | `def capacity(self, task_class)` |
| `configure` | method | `modules/guardrails/budget.py:50` | `def configure(self, capacities, threshold)` |
| `describe` | method | `modules/guardrails/budget.py:166` | `def describe(self)` |
| `purge` | method | `modules/guardrails/budget.py:126` | `def purge(self, task_class)` |
| `reclaim` | method | `modules/guardrails/budget.py:136` | `def reclaim(self)` |
| `release` | method | `modules/guardrails/budget.py:118` | `def release(self, task_class, units)` |
| `saturated` | method | `modules/guardrails/budget.py:154` | `def saturated(self, task_class)` |
| `threshold` | method | `modules/guardrails/budget.py:161` | `def threshold(self)` |
| `usage` | method | `modules/guardrails/budget.py:140` | `def usage(self, task_class)` |
| `CheckpointLedger` | class | `modules/guardrails/checkpoints.py:18` | `class CheckpointLedger` |
| `__init__` | method | `modules/guardrails/checkpoints.py:21` | `def __init__(self, history)` |
| `capture` | method | `modules/guardrails/checkpoints.py:33` | `def capture(self, key, state)` |
| `describe` | method | `modules/guardrails/checkpoints.py:92` | `def describe(self)` |
| `keys` | method | `modules/guardrails/checkpoints.py:59` | `def keys(self)` |
| `restore` | method | `modules/guardrails/checkpoints.py:51` | `def restore(self, key)` |
| `warm_restart` | method | `modules/guardrails/checkpoints.py:64` | `def warm_restart(self, core_key)` |
| `GuardrailContract` | class | `modules/guardrails/contracts.py:49` | `class GuardrailContract(Protocol)` |
| `HarnessAdminPort` | class | `modules/guardrails/contracts.py:73` | `class HarnessAdminPort(Protocol)` |
| `RunTicket` | class | `modules/guardrails/contracts.py:40` | `class RunTicket` |
| `TaskClass` | class | `modules/guardrails/contracts.py:19` | `class TaskClass(IntEnum)` |
| `configure` | method | `modules/guardrails/contracts.py:76` | `def configure(self, settings)` |
| `describe` | method | `modules/guardrails/contracts.py:52` | `def describe(self)` |
| `is_known` | method | `modules/guardrails/contracts.py:31` | `def is_known(cls, value)` |
| `rearm` | method | `modules/guardrails/contracts.py:80` | `def rearm(self)` |
| `run_guarded` | method | `modules/guardrails/contracts.py:56` | `def run_guarded(self, task_class, fn)` |
| `warm_restart` | method | `modules/guardrails/contracts.py:68` | `def warm_restart(self)` |
| `GuardHarness` | class | `modules/guardrails/harness.py:25` | `class GuardHarness` |
| `__init__` | method | `modules/guardrails/harness.py:28` | `def __init__(self, threshold, capacities)` |
| `_on_failure` | method | `modules/guardrails/harness.py:174` | `def _on_failure(self, tier, ticket, key, fn, args, kwargs, exc)` |
| `configure` | method | `modules/guardrails/harness.py:48` | `def configure(self, settings)` |
| `describe` | method | `modules/guardrails/harness.py:165` | `def describe(self)` |
| `global_harness` | function | `modules/guardrails/harness.py:232` | `def global_harness()` |
| `rearm` | method | `modules/guardrails/harness.py:153` | `def rearm(self)` |
| `reset_global_harness` | function | `modules/guardrails/harness.py:241` | `def reset_global_harness()` |
| `run_guarded` | method | `modules/guardrails/harness.py:63` | `def run_guarded(self, task_class, fn)` |
| `suspend` | method | `modules/guardrails/harness.py:138` | `def suspend(self, feature, reason)` |
| `warm_restart` | method | `modules/guardrails/harness.py:124` | `def warm_restart(self, core_key)` |
| `has` | function | `modules/gui_askpass.sh:22` | `` |
| `try_kdialog` | function | `modules/gui_askpass.sh:40` | `` |
| `try_ssh_askpass` | function | `modules/gui_askpass.sh:33` | `` |
| `try_yad` | function | `modules/gui_askpass.sh:28` | `` |
| `try_zenity` | function | `modules/gui_askpass.sh:24` | `` |
| `cleanup_enabled` | function | `modules/gym_cleanup.py:21` | `def cleanup_enabled()` |
| `cleanup_gym_machines` | function | `modules/gym_cleanup.py:35` | `def cleanup_gym_machines(verbose)` |
| `_persist` | function | `modules/gym_matrix_runner.py:217` | `def _persist(summary_result, sessions_dir)` |
| `_stats` | function | `modules/gym_matrix_runner.py:201` | `def _stats(runs)` |
| `load_matrix` | function | `modules/gym_matrix_runner.py:233` | `def load_matrix(sessions_dir)` |
| `plan_matrix` | function | `modules/gym_matrix_runner.py:36` | `def plan_matrix(target, sessions_dir, only, top_k)` |
| `run_matrix` | function | `modules/gym_matrix_runner.py:89` | `def run_matrix(target)` |
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
| `gate` | function | `modules/harness.py:65` | `def gate(name)` |
| `harness_enabled` | function | `modules/harness.py:30` | `def harness_enabled()` |
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
| `EventRecord` | class | `modules/hunt_verify.py:48` | `class EventRecord` |
| `Observation` | class | `modules/hunt_verify.py:73` | `class Observation` |
| `StageAssessment` | class | `modules/hunt_verify.py:85` | `class StageAssessment` |
| `StageSpec` | class | `modules/hunt_verify.py:60` | `class StageSpec` |
| `Verification` | class | `modules/hunt_verify.py:116` | `class Verification` |
| `_assess_stage` | function | `modules/hunt_verify.py:310` | `def _assess_stage(spec, observations, events, complete, warnings)` |
| `_field_present` | function | `modules/hunt_verify.py:172` | `def _field_present(event, field_name)` |
| `_scalar_present` | function | `modules/hunt_verify.py:177` | `def _scalar_present(value)` |
| `_stage_matches` | function | `modules/hunt_verify.py:188` | `def _stage_matches(spec, event)` |
| `_unique` | function | `modules/hunt_verify.py:140` | `def _unique(values)` |
| `chain_proven` | method | `modules/hunt_verify.py:124` | `def chain_proven(self)` |
| `field_present` | function | `modules/hunt_verify.py:152` | `def field_present(fields, field_name)` |
| `to_dict` | method | `modules/hunt_verify.py:99` | `def to_dict(self)` |
| `to_dict` | method | `modules/hunt_verify.py:130` | `def to_dict(self)` |
| `validate_specs` | function | `modules/hunt_verify.py:197` | `def validate_specs(specs)` |
| `verify_stages` | function | `modules/hunt_verify.py:232` | `def verify_stages(specs, observations, events, scope_covered)` |
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
| `_DictFinding` | class | `modules/integrations/misp_export.py:498` | `class _DictFinding` |
| `__init__` | method | `modules/integrations/misp_export.py:263` | `def __init__(self, mappers)` |
| `__init__` | method | `modules/integrations/misp_export.py:501` | `def __init__(self, data)` |
| `_detect_type` | method | `modules/integrations/misp_export.py:211` | `def _detect_type(value)` |
| `_dict_to_fact_records` | method | `modules/integrations/misp_export.py:457` | `def _dict_to_fact_records(data)` |
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
| `_main` | function | `modules/integrations/misp_export.py:529` | `def _main()` |
| `_map_finding` | method | `modules/integrations/misp_export.py:490` | `def _map_finding(self, finding)` |
| `export_session` | method | `modules/integrations/misp_export.py:268` | `def export_session(self, sessions_dir, target)` |
| `get_exporter` | function | `modules/integrations/misp_export.py:516` | `def get_exporter()` |
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

Next: [SYMBOLS_p15.md](SYMBOLS_p15.md)
