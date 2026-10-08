# Symbols (page 12 of 35)
Previous: [SYMBOLS_p11.md](SYMBOLS_p11.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `write` | method | `modules/event_bus.py:201` | `def write(self, event)` |
| `AutoRecommender` | class | `modules/event_consumers.py:198` | `class AutoRecommender` |
| `CredentialReactor` | class | `modules/event_consumers.py:269` | `class CredentialReactor` |
| `DashboardPusher` | class | `modules/event_consumers.py:354` | `class DashboardPusher` |
| `PhaseTracker` | class | `modules/event_consumers.py:146` | `class PhaseTracker` |
| `SoulSync` | class | `modules/event_consumers.py:316` | `class SoulSync` |
| `__call__` | method | `modules/event_consumers.py:159` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:204` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:279` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:319` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:357` | `def __call__(self, event)` |
| `__init__` | method | `modules/event_consumers.py:156` | `def __init__(self)` |
| `__init__` | method | `modules/event_consumers.py:201` | `def __init__(self)` |
| `_inject_objective` | function | `modules/event_consumers.py:54` | `def _inject_objective(text, priority, source)` |
| `_load_payload` | function | `modules/event_consumers.py:43` | `def _load_payload()` |
| `_update_soul` | function | `modules/event_consumers.py:110` | `def _update_soul(phase, credentials, access)` |
| `_update_world_model_host` | function | `modules/event_consumers.py:72` | `def _update_world_model_host(address, state, services)` |
| `unwire_all_consumers` | method | `modules/event_consumers.py:403` | `def unwire_all_consumers(bus)` |
| `wire_all_consumers` | method | `modules/event_consumers.py:375` | `def wire_all_consumers(bus)` |
| `_append_event` | function | `modules/event_engine.py:169` | `def _append_event(event)` |
| `_read_watermark` | function | `modules/event_engine.py:128` | `def _read_watermark()` |
| `_row_matches` | function | `modules/event_engine.py:141` | `def _row_matches(row, trigger)` |
| `_write_watermark` | function | `modules/event_engine.py:135` | `def _write_watermark(offset)` |
| `ack_event` | function | `modules/event_engine.py:253` | `def ack_event(event_id)` |
| `add_rule` | function | `modules/event_engine.py:113` | `def add_rule(rule)` |
| `load_rules` | function | `modules/event_engine.py:98` | `def load_rules()` |
| `process_new_rows` | function | `modules/event_engine.py:176` | `def process_new_rows()` |
| `read_events` | function | `modules/event_engine.py:233` | `def read_events(limit, status)` |
| `save_rules` | function | `modules/event_engine.py:109` | `def save_rules(rules)` |
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
| `_add_vuln` | method | `modules/exploit_chain.py:484` | `def _add_vuln(self, service, sig, version)` |
| `_compare_versions` | method | `modules/exploit_chain.py:266` | `def _compare_versions(version_a, version_b)` |
| `_discover_xml_files` | method | `modules/exploit_chain.py:331` | `def _discover_xml_files(self)` |
| `_is_richer` | method | `modules/exploit_chain.py:361` | `def _is_richer(new_svc, existing)` |
| `_parse_all_nmap_xml` | method | `modules/exploit_chain.py:346` | `def _parse_all_nmap_xml(self)` |
| `_parse_nmap_text` | method | `modules/exploit_chain.py:402` | `def _parse_nmap_text(self, output)` |
| `_parse_single_xml` | method | `modules/exploit_chain.py:367` | `def _parse_single_xml(self, xml_path)` |
| `fingerprint_services` | method | `modules/exploit_chain.py:311` | `def fingerprint_services(self, nmap_output)` |
| `generate_exploit_plan` | method | `modules/exploit_chain.py:496` | `def generate_exploit_plan(self)` |
| `generate_report` | method | `modules/exploit_chain.py:526` | `def generate_report(self)` |
| `get_post_exploit_commands` | method | `modules/exploit_chain.py:514` | `def get_post_exploit_commands(self, platform)` |
| `map_vulnerabilities` | method | `modules/exploit_chain.py:442` | `def map_vulnerabilities(self)` |
| `save_report` | method | `modules/exploit_chain.py:561` | `def save_report(self, path)` |
| `ExploitMatch` | class | `modules/exploit_recommender.py:35` | `class ExploitMatch` |
| `ExploitRecommender` | class | `modules/exploit_recommender.py:48` | `class ExploitRecommender` |
| `__init__` | method | `modules/exploit_recommender.py:118` | `def __init__(self, world_model)` |
| `_compare_versions` | method | `modules/exploit_recommender.py:161` | `def _compare_versions(version, max_vulnerable)` |
| `_extract_cve_ids` | method | `modules/exploit_recommender.py:157` | `def _extract_cve_ids(text)` |
| `_generate_lazyown_commands` | method | `modules/exploit_recommender.py:217` | `def _generate_lazyown_commands(self, cve_id, service, host_ip)` |
| `_load_exploitdb` | method | `modules/exploit_recommender.py:133` | `def _load_exploitdb(self)` |
| `_query_nvd` | method | `modules/exploit_recommender.py:171` | `def _query_nvd(self, cve_id)` |
| `_try_nvd` | method | `modules/exploit_recommender.py:214` | `def _try_nvd(self, cve_id)` |
| `format_for_llm` | method | `modules/exploit_recommender.py:397` | `def format_for_llm(self, matches, max_items)` |
| `match_services` | method | `modules/exploit_recommender.py:253` | `def match_services(self, hosts)` |
| `parse_version` | method | `modules/exploit_recommender.py:24` | `def parse_version(v)` |
| `persist_recommendations` | method | `modules/exploit_recommender.py:377` | `def persist_recommendations(self, matches)` |
| `recommend` | method | `modules/exploit_recommender.py:346` | `def recommend(self, hosts, top_n)` |
| `set_nvd_api_key` | method | `modules/exploit_recommender.py:130` | `def set_nvd_api_key(self, key)` |
| `set_world_model` | method | `modules/exploit_recommender.py:127` | `def set_world_model(self, world_model)` |
| `_detect_domain` | function | `modules/exploitgym_gym.py:96` | `def _detect_domain(task_id)` |
| `_ensure_clone` | function | `modules/exploitgym_gym.py:230` | `def _ensure_clone(root, timeout)` |
| `_ensure_dir` | function | `modules/exploitgym_gym.py:56` | `def _ensure_dir()` |
| `_env_for_run` | function | `modules/exploitgym_gym.py:315` | `def _env_for_run(params)` |
| `_extract_flag` | function | `modules/exploitgym_gym.py:487` | `def _extract_flag(output)` |
| `_load_records` | function | `modules/exploitgym_gym.py:500` | `def _load_records()` |
| `_read_task_ids` | function | `modules/exploitgym_gym.py:75` | `def _read_task_ids(root)` |
| `_record` | function | `modules/exploitgym_gym.py:523` | `def _record(task_id, success, elapsed, flag)` |
| `_resolve_root` | function | `modules/exploitgym_gym.py:61` | `def _resolve_root(params)` |
| `_run` | function | `modules/exploitgym_gym.py:274` | `def _run(name, cmd, cwd, timeout)` |
| `_run_agent` | function | `modules/exploitgym_gym.py:378` | `def _run_agent(task_id, model, mitigations, root, params, timeout)` |
| `_run_streaming` | function | `modules/exploitgym_gym.py:204` | `def _run_streaming(cmd, cwd, timeout)` |
| `_save_records` | function | `modules/exploitgym_gym.py:514` | `def _save_records(records)` |
| `check_readiness` | function | `modules/exploitgym_gym.py:112` | `def check_readiness(params)` |
| `list_tasks` | function | `modules/exploitgym_gym.py:176` | `def list_tasks(params, domain, limit)` |
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
| `ForensicCleaner` | class | `modules/forensic_cleaner.py:57` | `class ForensicCleaner` |
| `ForensicCleanerConfig` | class | `modules/forensic_cleaner.py:23` | `class ForensicCleanerConfig` |
| `__init__` | method | `modules/forensic_cleaner.py:67` | `def __init__(self, config)` |
| `amcache_parse` | method | `modules/forensic_cleaner.py:244` | `def amcache_parse(self)` |
| `linux_cleanup` | method | `modules/forensic_cleaner.py:165` | `def linux_cleanup(self)` |
| `macos_cleanup` | method | `modules/forensic_cleaner.py:193` | `def macos_cleanup(self)` |
| `windows_cleanup` | method | `modules/forensic_cleaner.py:70` | `def windows_cleanup(self)` |
| `windows_prefetch_parse` | method | `modules/forensic_cleaner.py:221` | `def windows_prefetch_parse(self, prefetch_path)` |
| `GCPAttackEngine` | class | `modules/gcp_attacks.py:77` | `class GCPAttackEngine` |
| `GCPConfig` | class | `modules/gcp_attacks.py:57` | `class GCPConfig` |
| `__init__` | method | `modules/gcp_attacks.py:90` | `def __init__(self, config)` |
| `cloud_functions_backdoor` | method | `modules/gcp_attacks.py:144` | `def cloud_functions_backdoor(self)` |
| `cloudbuild_abuse` | method | `modules/gcp_attacks.py:223` | `def cloudbuild_abuse(self)` |
| `compute_engine_metadata_exfil` | method | `modules/gcp_attacks.py:173` | `def compute_engine_metadata_exfil(self)` |
| `enumerate_iam_policy` | method | `modules/gcp_attacks.py:93` | `def enumerate_iam_policy(self, resource)` |
| `gcs_enumeration` | method | `modules/gcp_attacks.py:194` | `def gcs_enumeration(self)` |
| `organization_escalation` | method | `modules/gcp_attacks.py:254` | `def organization_escalation(self)` |
| `service_account_impersonation` | method | `modules/gcp_attacks.py:119` | `def service_account_impersonation(self)` |
| `summary` | method | `modules/gcp_attacks.py:290` | `def summary(self)` |
| `extract_cmd2_tools` | function | `modules/generate_tools.py:6` | `def extract_cmd2_tools(script_path)` |
| `GPOAbuseEngine` | class | `modules/gpo_abuse.py:105` | `class GPOAbuseEngine` |
| `GPOAbusePlan` | class | `modules/gpo_abuse.py:83` | `class GPOAbusePlan` |
| `GPOInfo` | class | `modules/gpo_abuse.py:54` | `class GPOInfo` |
| `__init__` | method | `modules/gpo_abuse.py:118` | `def __init__(self, domain, dc_ip)` |
| `detect_risky_gpos` | method | `modules/gpo_abuse.py:402` | `def detect_risky_gpos(self)` |
| `generate_all_plans` | method | `modules/gpo_abuse.py:380` | `def generate_all_plans(self, command, username)` |
| `parse_bloodhound_gpos` | method | `modules/gpo_abuse.py:160` | `def parse_bloodhound_gpos(self, bloodhound_nodes)` |
| `parse_gpo_list` | method | `modules/gpo_abuse.py:124` | `def parse_gpo_list(self, raw_gpo_output)` |
| `plan_local_admin_addition` | method | `modules/gpo_abuse.py:266` | `def plan_local_admin_addition(self, gpo, username, group)` |
| `plan_logon_script` | method | `modules/gpo_abuse.py:238` | `def plan_logon_script(self, gpo, command)` |
| `plan_registry_preference` | method | `modules/gpo_abuse.py:322` | `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)` |
| `plan_scheduled_task` | method | `modules/gpo_abuse.py:182` | `def plan_scheduled_task(self, gpo, command, task_name)` |
| `plan_service_installation` | method | `modules/gpo_abuse.py:354` | `def plan_service_installation(self, gpo, service_name, binary_path)` |
| `plan_startup_script` | method | `modules/gpo_abuse.py:208` | `def plan_startup_script(self, gpo, script_content, script_name)` |
| `plan_wmi_filter_abuse` | method | `modules/gpo_abuse.py:293` | `def plan_wmi_filter_abuse(self, gpo, wmi_query)` |
| `summary` | method | `modules/gpo_abuse.py:428` | `def summary(self)` |
| `has` | function | `modules/gui_askpass.sh:22` | `` |
| `try_kdialog` | function | `modules/gui_askpass.sh:40` | `` |
| `try_ssh_askpass` | function | `modules/gui_askpass.sh:33` | `` |
| `try_yad` | function | `modules/gui_askpass.sh:28` | `` |
| `try_zenity` | function | `modules/gui_askpass.sh:24` | `` |
| `CrackResult` | class | `modules/hash_cracker.py:131` | `class CrackResult` |
| `HashCracker` | class | `modules/hash_cracker.py:155` | `class HashCracker` |
| `HashIdentifier` | class | `modules/hash_cracker.py:144` | `class HashIdentifier` |
| `__init__` | method | `modules/hash_cracker.py:168` | `def __init__(self, wordlist, rules, use_hashcat, timeout)` |
| `_crack_batch_hashcat` | method | `modules/hash_cracker.py:496` | `def _crack_batch_hashcat(self, idents, hash_type, fmt_info, wordlist)` |
| `_crack_batch_john` | method | `modules/hash_cracker.py:604` | `def _crack_batch_john(self, idents, hash_type, fmt_info, wordlist)` |
| `_crack_hashcat` | method | `modules/hash_cracker.py:453` | `def _crack_hashcat(self, hash_value, hash_type, fmt_info, wordlist)` |
| `_crack_john` | method | `modules/hash_cracker.py:556` | `def _crack_john(self, hash_value, hash_type, fmt_info, wordlist)` |
| `_parse_hashcat_output` | method | `modules/hash_cracker.py:667` | `def _parse_hashcat_output(stdout, stderr, original)` |
| `_parse_john_show` | method | `modules/hash_cracker.py:682` | `def _parse_john_show(show_output, original)` |
| `_resolve_wordlist` | method | `modules/hash_cracker.py:182` | `def _resolve_wordlist(self)` |
| `crack_file` | method | `modules/hash_cracker.py:353` | `def crack_file(self, filepath, wordlist, hash_types)` |
| `crack_hash` | method | `modules/hash_cracker.py:299` | `def crack_hash(self, hash_value, hash_type, wordlist)` |
| `crack_secretsdump_output` | method | `modules/hash_cracker.py:691` | `def crack_secretsdump_output(filepath, wordlist, rhost)` |
| `identify` | method | `modules/hash_cracker.py:190` | `def identify(self, line)` |
| `identify_file` | method | `modules/hash_cracker.py:277` | `def identify_file(self, filepath)` |
| `import_to_db` | method | `modules/hash_cracker.py:405` | `def import_to_db(self, results, rhost, workspace_name)` |
| `_find_claude` | function | `modules/hive_invoke.py:112` | `def _find_claude()` |
| `_get_toposwarm` | function | `modules/hive_invoke.py:49` | `def _get_toposwarm()` |
| `_parse_argv` | function | `modules/hive_invoke.py:117` | `def _parse_argv(argv)` |
| `_run_interactive_mode` | function | `modules/hive_invoke.py:167` | `def _run_interactive_mode(prompt, effort, claude_bin)` |
| `_run_print_mode` | function | `modules/hive_invoke.py:147` | `def _run_print_mode(prompt, effort, claude_bin)` |
| `_run_toposwarm_mode` | function | `modules/hive_invoke.py:195` | `def _run_toposwarm_mode(prompt, effort, bridge)` |
| `main` | function | `modules/hive_invoke.py:244` | `def main(argv)` |
| `extract_ips_from_arp` | function | `modules/hostdiscover.sh:21` | `` |
| `extract_listening_ips_from_netstat` | function | `modules/hostdiscover.sh:26` | `` |
| `CodeAnalyzer` | class | `modules/ia_code_analysis.py:27` | `class CodeAnalyzer` |
| `__init__` | method | `modules/ia_code_analysis.py:31` | `def __init__(self, mode)` |
| `analyze_code_file` | method | `modules/ia_code_analysis.py:47` | `def analyze_code_file(self, file_path)` |
| `analyze_directory` | method | `modules/ia_code_analysis.py:35` | `def analyze_directory(self, directory)` |
| `analyze_with_deepseek` | method | `modules/ia_code_analysis.py:63` | `def analyze_with_deepseek(code_content, file_path, mode)` |
| `parse_args` | method | `modules/ia_code_analysis.py:172` | `def parse_args()` |
| `save_results_to_json` | method | `modules/ia_code_analysis.py:119` | `def save_results_to_json(results, file_path)` |
| `start_analysis` | method | `modules/ia_code_analysis.py:164` | `def start_analysis(code_dir, mode)` |
| `LogFileHandler` | class | `modules/ia_logs_analysis.py:53` | `class LogFileHandler(FileSystemEventHandler)` |
| `__init__` | method | `modules/ia_logs_analysis.py:57` | `def __init__(self, mode)` |
| `analyze_log_file` | method | `modules/ia_logs_analysis.py:73` | `def analyze_log_file(self, file_path)` |
| `analyze_with_deepseek` | method | `modules/ia_logs_analysis.py:91` | `def analyze_with_deepseek(log_content, mode)` |
| `on_modified` | method | `modules/ia_logs_analysis.py:62` | `def on_modified(self, event)` |
| `parse_args` | method | `modules/ia_logs_analysis.py:163` | `def parse_args()` |
| `start_monitoring` | method | `modules/ia_logs_analysis.py:143` | `def start_monitoring(log_dir, mode)` |
| `analyze_with_deepseek` | function | `modules/ia_network_analysis.py:39` | `def analyze_with_deepseek(packet_info, mode)` |
| `packet_callback` | function | `modules/ia_network_analysis.py:91` | `def packet_callback(packet, mode)` |
| `parse_args` | function | `modules/ia_network_analysis.py:154` | `def parse_args()` |
| `start_monitoring` | function | `modules/ia_network_analysis.py:130` | `def start_monitoring(interface, timeout, mode)` |
| `check_sudo` | function | `modules/icmp_client.py:55` | `def check_sudo()` |
| `checksum` | function | `modules/icmp_client.py:61` | `def checksum(source_string)` |
| `decrypt_data` | function | `modules/icmp_client.py:32` | `def decrypt_data(data, key)` |
| `encrypt_data` | function | `modules/icmp_client.py:17` | `def encrypt_data(data, key)` |
| `main` | function | `modules/icmp_client.py:124` | `def main()` |
| `receive_icmp_reply` | function | `modules/icmp_client.py:112` | `def receive_icmp_reply(sock)` |
| `send_icmp_packet` | function | `modules/icmp_client.py:78` | `def send_icmp_packet(dest_addr, data, key)` |
| `check_sudo` | function | `modules/icmp_server.py:32` | `def check_sudo()` |
| `checksum` | function | `modules/icmp_server.py:114` | `def checksum(source_string)` |
| `decrypt_data` | function | `modules/icmp_server.py:56` | `def decrypt_data(data, key)` |
| `encrypt_data` | function | `modules/icmp_server.py:40` | `def encrypt_data(data, key)` |
| `execute_command` | function | `modules/icmp_server.py:77` | `def execute_command(command)` |
| `handle_packet` | function | `modules/icmp_server.py:131` | `def handle_packet(packet, addr, key, sock)` |
| `listen_for_icmp` | function | `modules/icmp_server.py:155` | `def listen_for_icmp(interface, key)` |
| `main` | function | `modules/icmp_server.py:181` | `def main()` |
| `send_icmp_reply` | function | `modules/icmp_server.py:95` | `def send_icmp_reply(sock, addr, data, key)` |
| `imagen_a_binario` | function | `modules/img2bin.py:7` | `def imagen_a_binario(imagen_input, binario_output, block_size)` |
| `main` | function | `modules/img2bin.py:42` | `def main()` |
| `CVEMapper` | class | `modules/integrations/misp_export.py:136` | `class CVEMapper(FindingMapper)` |
| `CredentialMapper` | class | `modules/integrations/misp_export.py:116` | `class CredentialMapper(FindingMapper)` |
| `DomainMapper` | class | `modules/integrations/misp_export.py:156` | `class DomainMapper(FindingMapper)` |
| `FindingMapper` | class | `modules/integrations/misp_export.py:80` | `class FindingMapper(ABC)` |
| `HashMapper` | class | `modules/integrations/misp_export.py:176` | `class HashMapper(FindingMapper)` |
| `IPMapper` | class | `modules/integrations/misp_export.py:96` | `class IPMapper(FindingMapper)` |
| `MISPAttribute` | class | `modules/integrations/misp_export.py:56` | `class MISPAttribute` |
| `MISPEvent` | class | `modules/integrations/misp_export.py:66` | `class MISPEvent` |
| `MISPExporter` | class | `modules/integrations/misp_export.py:246` | `class MISPExporter` |
| `ServiceMapper` | class | `modules/integrations/misp_export.py:211` | `class ServiceMapper(FindingMapper)` |
| `_DictFinding` | class | `modules/integrations/misp_export.py:445` | `class _DictFinding` |
| `__init__` | method | `modules/integrations/misp_export.py:255` | `def __init__(self, mappers)` |
| `__init__` | method | `modules/integrations/misp_export.py:448` | `def __init__(self, data)` |
| `_detect_type` | method | `modules/integrations/misp_export.py:204` | `def _detect_type(value)` |
| `_dict_to_findings` | method | `modules/integrations/misp_export.py:397` | `def _dict_to_findings(data)` |
| `_is_credential` | method | `modules/integrations/misp_export.py:131` | `def _is_credential(finding)` |
| `_is_cve` | method | `modules/integrations/misp_export.py:151` | `def _is_cve(finding)` |
| `_is_domain` | method | `modules/integrations/misp_export.py:171` | `def _is_domain(finding)` |
| `_is_hash` | method | `modules/integrations/misp_export.py:199` | `def _is_hash(finding)` |
| `_is_ip` | method | `modules/integrations/misp_export.py:111` | `def _is_ip(finding)` |
| `_is_service` | method | `modules/integrations/misp_export.py:226` | `def _is_service(finding)` |
| `_load_events` | method | `modules/integrations/misp_export.py:377` | `def _load_events(self, sdir)` |
| `_load_findings` | method | `modules/integrations/misp_export.py:359` | `def _load_findings(self, sdir)` |
| `_load_policy_facts` | method | `modules/integrations/misp_export.py:366` | `def _load_policy_facts(self, sdir)` |
| `_main` | method | `modules/integrations/misp_export.py:475` | `def _main()` |
| `_map_finding` | method | `modules/integrations/misp_export.py:437` | `def _map_finding(self, finding)` |
| `export_session` | method | `modules/integrations/misp_export.py:260` | `def export_session(self, sessions_dir, target)` |
| `get_exporter` | method | `modules/integrations/misp_export.py:463` | `def get_exporter()` |
| `map` | method | `modules/integrations/misp_export.py:84` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:99` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:119` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:139` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:159` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:185` | `def map(self, finding)` |
| `map` | method | `modules/integrations/misp_export.py:214` | `def map(self, finding)` |
| `push_to_misp` | method | `modules/integrations/misp_export.py:322` | `def push_to_misp(self, event, url, api_key)` |
| `save` | method | `modules/integrations/misp_export.py:314` | `def save(self, event, path)` |
| `to_json` | method | `modules/integrations/misp_export.py:291` | `def to_json(self, event)` |
| `LocalTemplateIndex` | class | `modules/integrations/nuclei_bridge.py:98` | `class LocalTemplateIndex(TemplateSelector)` |
| `NucleiBridge` | class | `modules/integrations/nuclei_bridge.py:381` | `class NucleiBridge` |
| `NucleiRunner` | class | `modules/integrations/nuclei_bridge.py:272` | `class NucleiRunner` |
| `NucleiTemplate` | class | `modules/integrations/nuclei_bridge.py:68` | `class NucleiTemplate` |
| `TemplateSelector` | class | `modules/integrations/nuclei_bridge.py:82` | `class TemplateSelector(ABC)` |
| `_F` | class | `modules/integrations/nuclei_bridge.py:475` | `class _F` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:108` | `def __init__(self, templates_dir)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:281` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:388` | `def __init__(self, selector, runner)` |
| `__init__` | method | `modules/integrations/nuclei_bridge.py:476` | `def __init__(self, ftype, value)` |
| `_build_command` | method | `modules/integrations/nuclei_bridge.py:336` | `def _build_command(self, target, templates, output_dir)` |
| `_ensure_built` | method | `modules/integrations/nuclei_bridge.py:152` | `def _ensure_built(self)` |
| `_extract_context` | method | `modules/integrations/nuclei_bridge.py:363` | `def _extract_context(findings)` |
| `_extract_cve_from_tags` | method | `modules/integrations/nuclei_bridge.py:240` | `def _extract_cve_from_tags(tags)` |
| `_extract_cve_from_text` | method | `modules/integrations/nuclei_bridge.py:247` | `def _extract_cve_from_text(text)` |
| `_main` | method | `modules/integrations/nuclei_bridge.py:447` | `def _main()` |
| `_matches` | method | `modules/integrations/nuclei_bridge.py:252` | `def _matches(tmpl, service_lower, cve_upper)` |
| `_normalise_tags` | method | `modules/integrations/nuclei_bridge.py:232` | `def _normalise_tags(raw)` |
| `_parse_regex` | method | `modules/integrations/nuclei_bridge.py:195` | `def _parse_regex(self, text, path)` |
| `_parse_template` | method | `modules/integrations/nuclei_bridge.py:156` | `def _parse_template(self, path)` |
| `_parse_yaml` | method | `modules/integrations/nuclei_bridge.py:166` | `def _parse_yaml(self, text, path)` |
| `build` | method | `modules/integrations/nuclei_bridge.py:135` | `def build(self)` |
| `get_bridge` | method | `modules/integrations/nuclei_bridge.py:435` | `def get_bridge()` |
| `list_templates` | method | `modules/integrations/nuclei_bridge.py:419` | `def list_templates(self, services, cves)` |
| `run` | method | `modules/integrations/nuclei_bridge.py:286` | `def run(self, target, templates, output_dir)` |
| `run_for_findings` | method | `modules/integrations/nuclei_bridge.py:319` | `def run_for_findings(self, target, findings, output_dir, selector)` |
| `scan` | method | `modules/integrations/nuclei_bridge.py:396` | `def scan(self, target, findings, dry_run)` |
| `select` | method | `modules/integrations/nuclei_bridge.py:86` | `def select(self, services, cves)` |
| `select` | method | `modules/integrations/nuclei_bridge.py:115` | `def select(self, services, cves)` |
| `NucleiFinding` | class | `modules/integrations/nuclei_parser.py:71` | `class NucleiFinding` |
| `NucleiParser` | class | `modules/integrations/nuclei_parser.py:99` | `class NucleiParser` |
| `__init__` | method | `modules/integrations/nuclei_parser.py:109` | `def __init__(self, sessions_dir)` |
| `_finding_to_dict` | method | `modules/integrations/nuclei_parser.py:501` | `def _finding_to_dict(finding)` |
| `_parse_json_obj` | method | `modules/integrations/nuclei_parser.py:409` | `def _parse_json_obj(self, obj)` |
| `_parse_line` | method | `modules/integrations/nuclei_parser.py:390` | `def _parse_line(self, line)` |
| `_recommend_for_finding` | method | `modules/integrations/nuclei_parser.py:465` | `def _recommend_for_finding(self, finding, rhost)` |
| `_summarize` | method | `modules/integrations/nuclei_parser.py:514` | `def _summarize(findings)` |
| `enrich_world_model` | method | `modules/integrations/nuclei_parser.py:261` | `def enrich_world_model(self, findings, rhost)` |
| `exploit_probability` | method | `modules/integrations/nuclei_parser.py:95` | `def exploit_probability(self)` |
| `generate_recommendations` | method | `modules/integrations/nuclei_parser.py:298` | `def generate_recommendations(self, findings, rhost)` |
| `import_to_db` | method | `modules/integrations/nuclei_parser.py:196` | `def import_to_db(self, findings, rhost, workspace_name)` |
| `mitre_tactic` | method | `modules/integrations/nuclei_parser.py:87` | `def mitre_tactic(self)` |
| `parse_file` | method | `modules/integrations/nuclei_parser.py:177` | `def parse_file(self, filepath)` |
| `parse_json` | method | `modules/integrations/nuclei_parser.py:134` | `def parse_json(self, json_text)` |
| `parse_text` | method | `modules/integrations/nuclei_parser.py:115` | `def parse_text(self, text)` |
| `scan_and_import` | method | `modules/integrations/nuclei_parser.py:326` | `def scan_and_import(self, target, templates, services, cves, workspace_name)` |
| `ExploitDBAPI` | class | `modules/integrations/searchsploit.py:191` | `class ExploitDBAPI(ExploitSource)` |
| `ExploitEntry` | class | `modules/integrations/searchsploit.py:60` | `class ExploitEntry` |
| `ExploitSource` | class | `modules/integrations/searchsploit.py:74` | `class ExploitSource(ABC)` |
| `SearchsploitCLI` | class | `modules/integrations/searchsploit.py:90` | `class SearchsploitCLI(ExploitSource)` |
| `SearchsploitClient` | class | `modules/integrations/searchsploit.py:262` | `class SearchsploitClient` |
| `__init__` | method | `modules/integrations/searchsploit.py:99` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/searchsploit.py:199` | `def __init__(self)` |
| `__init__` | method | `modules/integrations/searchsploit.py:269` | `def __init__(self, primary, fallback)` |
| `_extract_cve` | method | `modules/integrations/searchsploit.py:182` | `def _extract_cve(text)` |
| `_main` | method | `modules/integrations/searchsploit.py:346` | `def _main()` |
| `_parse` | method | `modules/integrations/searchsploit.py:132` | `def _parse(self, raw)` |
| `_query` | method | `modules/integrations/searchsploit.py:218` | `def _query(self, cve_id)` |
| `_rate_limit` | method | `modules/integrations/searchsploit.py:250` | `def _rate_limit()` |
| `_row_to_entry` | method | `modules/integrations/searchsploit.py:161` | `def _row_to_entry(self, row)` |
| `_run` | method | `modules/integrations/searchsploit.py:117` | `def _run(self, query)` |
| `enrich_findings` | method | `modules/integrations/searchsploit.py:291` | `def enrich_findings(self, findings)` |
| `get_client` | method | `modules/integrations/searchsploit.py:324` | `def get_client()` |
| `search_cve` | method | `modules/integrations/searchsploit.py:78` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:108` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:207` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:277` | `def search_cve(self, cve_id)` |
| `search_cve` | method | `modules/integrations/searchsploit.py:332` | `def search_cve(cve_id)` |
| `search_service` | method | `modules/integrations/searchsploit.py:82` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:111` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:210` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:284` | `def search_service(self, name, version)` |
| `search_service` | method | `modules/integrations/searchsploit.py:337` | `def search_service(name, version)` |
| `CollectedFact` | class | `modules/intelligence_engine.py:76` | `class CollectedFact` |
| `CounterIntelFinding` | class | `modules/intelligence_engine.py:106` | `class CounterIntelFinding` |
| `IntelligenceAssessment` | class | `modules/intelligence_engine.py:91` | `class IntelligenceAssessment` |
| `IntelligenceConfig` | class | `modules/intelligence_engine.py:57` | `class IntelligenceConfig` |
| `IntelligenceEngine` | class | `modules/intelligence_engine.py:117` | `class IntelligenceEngine` |
| `__init__` | method | `modules/intelligence_engine.py:140` | `def __init__(self, config)` |
| `_correlate_creds_to_hosts` | method | `modules/intelligence_engine.py:515` | `def _correlate_creds_to_hosts(self)` |
| `_correlate_domains_to_infrastructure` | method | `modules/intelligence_engine.py:536` | `def _correlate_domains_to_infrastructure(self)` |
| `_correlate_services_to_vulns` | method | `modules/intelligence_engine.py:445` | `def _correlate_services_to_vulns(self)` |
| `_detect_killchain_gaps` | method | `modules/intelligence_engine.py:588` | `def _detect_killchain_gaps(self)` |
| `_is_placeholder` | method | `modules/intelligence_engine.py:864` | `def _is_placeholder(value)` |
| `_map_category_to_mitre` | method | `modules/intelligence_engine.py:647` | `def _map_category_to_mitre(category)` |
| `_match_known_vulns` | method | `modules/intelligence_engine.py:487` | `def _match_known_vulns(fact)` |
| `_rank_targets` | method | `modules/intelligence_engine.py:550` | `def _rank_targets(self)` |
| `analyze` | method | `modules/intelligence_engine.py:428` | `def analyze(self)` |
| `collect_from_estorides` | method | `modules/intelligence_engine.py:266` | `def collect_from_estorides(self, target)` |
| `collect_from_factstore` | method | `modules/intelligence_engine.py:380` | `def collect_from_factstore(self)` |
| `collect_from_nuclei` | method | `modules/intelligence_engine.py:303` | `def collect_from_nuclei(self, target)` |
| `collect_from_scan` | method | `modules/intelligence_engine.py:151` | `def collect_from_scan(self, target)` |
| `collect_from_tool` | method | `modules/intelligence_engine.py:229` | `def collect_from_tool(self, output, tool, host)` |
| `collect_from_yara` | method | `modules/intelligence_engine.py:343` | `def collect_from_yara(self, target_path)` |
| `disseminate` | method | `modules/intelligence_engine.py:706` | `def disseminate(self)` |
| `get_intel_report` | method | `modules/intelligence_engine.py:818` | `def get_intel_report(self)` |
| `get_intelligence_engine` | method | `modules/intelligence_engine.py:870` | `def get_intelligence_engine(config)` |
| `produce_counter_intelligence` | method | `modules/intelligence_engine.py:662` | `def produce_counter_intelligence(self)` |
| `produce_intelligence` | method | `modules/intelligence_engine.py:628` | `def produce_intelligence(self)` |
| `run_full_cycle` | method | `modules/intelligence_engine.py:789` | `def run_full_cycle(self, target)` |
| `display_usage` | function | `modules/iptables_portforward.sh:29` | `` |
| `K8SAttackEngine` | class | `modules/k8s_attacks.py:77` | `class K8SAttackEngine` |
| `K8sConfig` | class | `modules/k8s_attacks.py:57` | `class K8sConfig` |
| `__init__` | method | `modules/k8s_attacks.py:87` | `def __init__(self, config)` |
| `enumerate_rbac` | method | `modules/k8s_attacks.py:90` | `def enumerate_rbac(self)` |
| `etcd_access_exploitation` | method | `modules/k8s_attacks.py:222` | `def etcd_access_exploitation(self)` |
| `helm_tiller_abuse` | method | `modules/k8s_attacks.py:251` | `def helm_tiller_abuse(self)` |
| `kubelet_anonymous_auth_abuse` | method | `modules/k8s_attacks.py:198` | `def kubelet_anonymous_auth_abuse(self)` |
| `persistence_techniques` | method | `modules/k8s_attacks.py:279` | `def persistence_techniques(self)` |
| `privileged_pod_escape` | method | `modules/k8s_attacks.py:118` | `def privileged_pod_escape(self)` |
| `service_account_token_theft` | method | `modules/k8s_attacks.py:173` | `def service_account_token_theft(self)` |
| `summary` | method | `modules/k8s_attacks.py:319` | `def summary(self)` |
| `KerberoastHash` | class | `modules/kerberoasting.py:59` | `class KerberoastHash` |
| `KerberoastTarget` | class | `modules/kerberoasting.py:38` | `class KerberoastTarget` |
| `KerberoastingEngine` | class | `modules/kerberoasting.py:79` | `class KerberoastingEngine` |
| `__init__` | method | `modules/kerberoasting.py:95` | `def __init__(self, domain, dc_ip, username, password, hash)` |
| `_build_hash_string` | method | `modules/kerberoasting.py:240` | `def _build_hash_string(self, spn, etype)` |
| `_hashcat_command` | method | `modules/kerberoasting.py:266` | `def _hashcat_command(hash_str, mode)` |
| `_prioritize_targets` | method | `modules/kerberoasting.py:161` | `def _prioritize_targets(self)` |
| `asreproast_check` | method | `modules/kerberoasting.py:307` | `def asreproast_check(self, usernames)` |
| `build_hashcat_batch` | method | `modules/kerberoasting.py:376` | `def build_hashcat_batch(self, output_path)` |
| `detect_kerberoasting_activity` | method | `modules/kerberoasting.py:337` | `def detect_kerberoasting_activity(self, event_log)` |
| `enumerate_spns` | method | `modules/kerberoasting.py:112` | `def enumerate_spns(self, ldap_output, bloodhound_data)` |
| `extract_hashes_from_pcap` | method | `modules/kerberoasting.py:322` | `def extract_hashes_from_pcap(self, pcap_path)` |
| `priority` | method | `modules/kerberoasting.py:164` | `def priority(target)` |
| `request_tgs` | method | `modules/kerberoasting.py:211` | `def request_tgs(self, user_spn, etype)` |
| `request_tgs_aes_only` | method | `modules/kerberoasting.py:179` | `def request_tgs_aes_only(self, user_spn)` |
| `request_tgs_rc4` | method | `modules/kerberoasting.py:200` | `def request_tgs_rc4(self, user_spn)` |
| `summary` | method | `modules/kerberoasting.py:398` | `def summary(self)` |
| `targeted_kerberoast` | method | `modules/kerberoasting.py:272` | `def targeted_kerberoast(self, high_value_only)` |
| `EncryptedData` | class | `modules/kerberos_core.py:155` | `class EncryptedData` |
| `KerberosCore` | class | `modules/kerberos_core.py:405` | `class KerberosCore` |
| `KerberosCrypto` | class | `modules/kerberos_core.py:269` | `class KerberosCrypto` |
| `KerberosErrorParser` | class | `modules/kerberos_core.py:681` | `class KerberosErrorParser` |
| `KerberosPrincipal` | class | `modules/kerberos_core.py:137` | `class KerberosPrincipal` |
| `KerberosTicket` | class | `modules/kerberos_core.py:170` | `class KerberosTicket` |
| `PACInfo` | class | `modules/kerberos_core.py:226` | `class PACInfo` |
| `PACSignature` | class | `modules/kerberos_core.py:211` | `class PACSignature` |
| `TGSRequest` | class | `modules/kerberos_core.py:247` | `class TGSRequest` |
| `TicketValidator` | class | `modules/kerberos_core.py:700` | `class TicketValidator` |
| `__init__` | method | `modules/kerberos_core.py:275` | `def __init__(self)` |
| `__init__` | method | `modules/kerberos_core.py:419` | `def __init__(self, domain, dc_host, dc_ip)` |
| `_build_pa_enc_timestamp` | method | `modules/kerberos_core.py:638` | `def _build_pa_enc_timestamp(self, key, etype, timestamp)` |
| `_parse_kdc_rep` | method | `modules/kerberos_core.py:651` | `def _parse_kdc_rep(self, data, key, etype, rep_type)` |
| `_parse_pac_buffer` | method | `modules/kerberos_core.py:620` | `def _parse_pac_buffer(pac, buf_type, buf_data)` |
| `_rc4_decrypt` | method | `modules/kerberos_core.py:674` | `def _rc4_decrypt(key, data, usage)` |
| `_rc4_encrypt` | method | `modules/kerberos_core.py:665` | `def _rc4_encrypt(key, data, usage)` |
| `aes_decrypt` | method | `modules/kerberos_core.py:359` | `def aes_decrypt(self, key, ciphertext, usage)` |
| `aes_encrypt` | method | `modules/kerberos_core.py:327` | `def aes_encrypt(self, key, plaintext, usage)` |
| `build_as_req` | method | `modules/kerberos_core.py:433` | `def build_as_req(self, username, domain, password, etype)` |
| `build_tgs_req` | method | `modules/kerberos_core.py:487` | `def build_tgs_req(self, params)` |
| `compute_checksum` | method | `modules/kerberos_core.py:387` | `def compute_checksum(key, data, etype)` |
| `decrypt_ticket` | method | `modules/kerberos_core.py:561` | `def decrypt_ticket(self, ticket_data, key, etype)` |
| `derive_aes_key` | method | `modules/kerberos_core.py:280` | `def derive_aes_key(password, salt, etype)` |
| `derive_rc4_key` | method | `modules/kerberos_core.py:316` | `def derive_rc4_key(password)` |
| `get_supported_etypes` | method | `modules/kerberos_core.py:425` | `def get_supported_etypes(self)` |
| `has_flag` | method | `modules/kerberos_core.py:205` | `def has_flag(self, flag_name)` |
| `is_expired` | method | `modules/kerberos_core.py:704` | `def is_expired(endtime, grace_period)` |
| `parse_as_rep` | method | `modules/kerberos_core.py:532` | `def parse_as_rep(self, as_rep_data, key, etype)` |
| `parse_error` | method | `modules/kerberos_core.py:685` | `def parse_error(error_data)` |
| `parse_pac` | method | `modules/kerberos_core.py:586` | `def parse_pac(self, pac_data)` |
| `parse_tgs_rep` | method | `modules/kerberos_core.py:548` | `def parse_tgs_rep(self, tgs_rep_data, session_key, etype)` |
| `to_string` | method | `modules/kerberos_core.py:150` | `def to_string(self)` |
| `validate_flags` | method | `modules/kerberos_core.py:717` | `def validate_flags(ticket, required_flags)` |
| `validate_pac_checksums` | method | `modules/kerberos_core.py:733` | `def validate_pac_checksums(pac)` |
| `DiamondTicketConfig` | class | `modules/kerberos_tickets.py:94` | `class DiamondTicketConfig` |
| `DiamondTicketForger` | class | `modules/kerberos_tickets.py:397` | `class DiamondTicketForger` |
| `GoldenTicketConfig` | class | `modules/kerberos_tickets.py:65` | `class GoldenTicketConfig` |
| `GoldenTicketForger` | class | `modules/kerberos_tickets.py:265` | `class GoldenTicketForger` |
| `SapphireTicketForger` | class | `modules/kerberos_tickets.py:462` | `class SapphireTicketForger` |

Next: [SYMBOLS_p13.md](SYMBOLS_p13.md)
