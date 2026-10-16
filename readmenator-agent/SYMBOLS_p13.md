# Symbols (page 13 of 41)
Previous: [SYMBOLS_p12.md](SYMBOLS_p12.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `CollabBusSink` | class | `modules/event_bus.py:163` | `class CollabBusSink(Sink)` |
| `EngagementSink` | class | `modules/event_bus.py:202` | `class EngagementSink(Sink)` |
| `EventCategory` | class | `modules/event_bus.py:47` | `class EventCategory(str, Enum)` |
| `EventSeverity` | class | `modules/event_bus.py:73` | `class EventSeverity(str, Enum)` |
| `JsonlSink` | class | `modules/event_bus.py:143` | `class JsonlSink(Sink)` |
| `LazyEvent` | class | `modules/event_bus.py:82` | `class LazyEvent` |
| `Sink` | class | `modules/event_bus.py:133` | `class Sink(ABC)` |
| `UnifiedEventBus` | class | `modules/event_bus.py:230` | `class UnifiedEventBus` |
| `__init__` | method | `modules/event_bus.py:146` | `def __init__(self, filepath)` |
| `__init__` | method | `modules/event_bus.py:166` | `def __init__(self)` |
| `__init__` | method | `modules/event_bus.py:255` | `def __init__(self)` |
| `_bus` | method | `modules/event_bus.py:170` | `def _bus(self)` |
| `_dispatch_event` | method | `modules/event_bus.py:441` | `def _dispatch_event(self, event)` |
| `_dispatch_loop` | method | `modules/event_bus.py:416` | `def _dispatch_loop(self)` |
| `_init_sinks` | method | `modules/event_bus.py:273` | `def _init_sinks(self)` |
| `_match_topic` | method | `modules/event_bus.py:517` | `def _match_topic(self, topic, event)` |
| `_notify_shutdown` | method | `modules/event_bus.py:479` | `def _notify_shutdown(self)` |
| `close` | method | `modules/event_bus.py:140` | `def close(self)` |
| `close` | method | `modules/event_bus.py:159` | `def close(self)` |
| `close` | method | `modules/event_bus.py:198` | `def close(self)` |
| `close` | method | `modules/event_bus.py:226` | `def close(self)` |
| `drain` | method | `modules/event_bus.py:354` | `def drain(self)` |
| `from_dict` | method | `modules/event_bus.py:115` | `def from_dict(cls, d)` |
| `get_event_bus` | function | `modules/event_bus.py:570` | `def get_event_bus()` |
| `history` | method | `modules/event_bus.py:556` | `def history(self, n, category)` |
| `history_since` | method | `modules/event_bus.py:564` | `def history_since(self, since_ts)` |
| `instance` | method | `modules/event_bus.py:287` | `def instance(cls)` |
| `publish` | method | `modules/event_bus.py:336` | `def publish(self, event)` |
| `publish_event` | function | `modules/event_bus.py:575` | `def publish_event(category, event_type, source, payload, severity, target, operator)` |
| `shutdown` | method | `modules/event_bus.py:372` | `def shutdown(self)` |
| `subscribe` | method | `modules/event_bus.py:300` | `def subscribe(self, subscriber_id, callback)` |
| `subscribe_async` | method | `modules/event_bus.py:315` | `def subscribe_async(self, subscriber_id)` |
| `subscribe_topic` | method | `modules/event_bus.py:305` | `def subscribe_topic(self, subscriber_id, topic, callback)` |
| `subscriber_count` | method | `modules/event_bus.py:295` | `def subscriber_count(self)` |
| `to_dict` | method | `modules/event_bus.py:96` | `def to_dict(self)` |
| `to_json` | method | `modules/event_bus.py:111` | `def to_json(self)` |
| `unsubscribe` | method | `modules/event_bus.py:327` | `def unsubscribe(self, subscriber_id)` |
| `write` | method | `modules/event_bus.py:137` | `def write(self, event)` |
| `write` | method | `modules/event_bus.py:151` | `def write(self, event)` |
| `write` | method | `modules/event_bus.py:181` | `def write(self, event)` |
| `write` | method | `modules/event_bus.py:205` | `def write(self, event)` |
| `AutoRecommender` | class | `modules/event_consumers.py:201` | `class AutoRecommender` |
| `CredentialReactor` | class | `modules/event_consumers.py:272` | `class CredentialReactor` |
| `DashboardPusher` | class | `modules/event_consumers.py:358` | `class DashboardPusher` |
| `PhaseTracker` | class | `modules/event_consumers.py:146` | `class PhaseTracker` |
| `SoulSync` | class | `modules/event_consumers.py:320` | `class SoulSync` |
| `__call__` | method | `modules/event_consumers.py:159` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:207` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:282` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:323` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:361` | `def __call__(self, event)` |
| `__init__` | method | `modules/event_consumers.py:156` | `def __init__(self)` |
| `__init__` | method | `modules/event_consumers.py:204` | `def __init__(self)` |
| `_inject_objective` | function | `modules/event_consumers.py:54` | `def _inject_objective(text, priority, source)` |
| `_load_payload` | function | `modules/event_consumers.py:43` | `def _load_payload()` |
| `_update_soul` | function | `modules/event_consumers.py:110` | `def _update_soul(phase, credentials, access)` |
| `_update_world_model_host` | function | `modules/event_consumers.py:72` | `def _update_world_model_host(address, state, services)` |
| `unwire_all_consumers` | function | `modules/event_consumers.py:409` | `def unwire_all_consumers(bus)` |
| `wire_all_consumers` | function | `modules/event_consumers.py:380` | `def wire_all_consumers(bus)` |
| `_append_event` | function | `modules/event_engine.py:173` | `def _append_event(event)` |
| `_read_watermark` | function | `modules/event_engine.py:130` | `def _read_watermark()` |
| `_row_matches` | function | `modules/event_engine.py:144` | `def _row_matches(row, trigger)` |
| `_write_watermark` | function | `modules/event_engine.py:137` | `def _write_watermark(offset)` |
| `ack_event` | function | `modules/event_engine.py:270` | `def ack_event(event_id)` |
| `add_rule` | function | `modules/event_engine.py:114` | `def add_rule(rule)` |
| `load_rules` | function | `modules/event_engine.py:99` | `def load_rules()` |
| `process_new_rows` | function | `modules/event_engine.py:181` | `def process_new_rows()` |
| `read_events` | function | `modules/event_engine.py:250` | `def read_events(limit, status)` |
| `save_rules` | function | `modules/event_engine.py:110` | `def save_rules(rules)` |
| `EvidenceConfig` | class | `modules/evidence.py:20` | `class EvidenceConfig` |
| `EvidenceStore` | class | `modules/evidence.py:54` | `class EvidenceStore` |
| `__init__` | method | `modules/evidence.py:57` | `def __init__(self, base_dir)` |
| `_validate_hash` | function | `modules/evidence.py:42` | `def _validate_hash(value)` |
| `blob_path` | method | `modules/evidence.py:65` | `def blob_path(self, content_hash)` |
| `exists` | method | `modules/evidence.py:98` | `def exists(self, content_hash)` |
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

Next: [SYMBOLS_p14.md](SYMBOLS_p14.md)
