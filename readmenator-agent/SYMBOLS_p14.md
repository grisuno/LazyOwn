# Symbols (page 14 of 48)
Previous: [SYMBOLS_p13.md](SYMBOLS_p13.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `extract_seeds_from_scope` | function | `modules/estorides_importer.py:244` | `def extract_seeds_from_scope(scope_entries)` |
| `extract_seeds_from_world_model` | function | `modules/estorides_importer.py:143` | `def extract_seeds_from_world_model(world_model_path)` |
| `find_lan_bundle_files` | function | `modules/estorides_importer.py:588` | `def find_lan_bundle_files(lan_dir, sessions_dir)` |
| `get_all_entities` | method | `modules/estorides_importer.py:475` | `def get_all_entities(self, case_id)` |
| `get_combined_surface` | method | `modules/estorides_importer.py:836` | `def get_combined_surface(self)` |
| `get_entities` | method | `modules/estorides_importer.py:416` | `def get_entities(self, case_id, entity_types, limit)` |
| `get_host_entities` | method | `modules/estorides_importer.py:471` | `def get_host_entities(self, case_id)` |
| `import_entities` | method | `modules/estorides_importer.py:713` | `def import_entities(self, entities, add_to_scope, add_to_db)` |
| `list_cases` | method | `modules/estorides_importer.py:404` | `def list_cases(self, limit)` |
| `new_assets` | method | `modules/estorides_importer.py:139` | `def new_assets(self)` |
| `parse` | method | `modules/estorides_importer.py:520` | `def parse(self)` |
| `parse` | method | `modules/estorides_importer.py:654` | `def parse(self)` |
| `parse_by_type` | method | `modules/estorides_importer.py:554` | `def parse_by_type(self, entity_types)` |
| `read_devices` | method | `modules/estorides_importer.py:641` | `def read_devices(self)` |
| `run` | method | `modules/estorides_importer.py:912` | `def run(self, seed_methods)` |
| `run_estorides_discover` | function | `modules/estorides_importer.py:274` | `def run_estorides_discover(seed_type, seed_value, max_depth, max_steps, out_json, timeout)` |
| `run_estorides_run` | function | `modules/estorides_importer.py:334` | `def run_estorides_run(query, out_json, timeout)` |
| `stats` | method | `modules/estorides_importer.py:478` | `def stats(self)` |
| `success` | method | `modules/estorides_importer.py:110` | `def success(self)` |
| `to_dict` | method | `modules/estorides_importer.py:113` | `def to_dict(self)` |
| `EvasionEngine` | class | `modules/evasion_engine.py:52` | `class EvasionEngine` |
| `MalleableProfile` | class | `modules/evasion_engine.py:37` | `class MalleableProfile` |
| `TrafficMorphConfig` | class | `modules/evasion_engine.py:25` | `class TrafficMorphConfig` |
| `__init__` | method | `modules/evasion_engine.py:130` | `def __init__(self, config)` |
| `_compute_jitter` | method | `modules/evasion_engine.py:220` | `def _compute_jitter(self)` |
| `_compute_sleep` | method | `modules/evasion_engine.py:224` | `def _compute_sleep(self)` |
| `_generate_cert_fingerprint` | method | `modules/evasion_engine.py:217` | `def _generate_cert_fingerprint(self)` |
| `_generate_headers` | method | `modules/evasion_engine.py:180` | `def _generate_headers(self, user_agent)` |
| `_generate_ja4_hash` | method | `modules/evasion_engine.py:148` | `def _generate_ja4_hash(self)` |
| `_generate_user_agent` | method | `modules/evasion_engine.py:162` | `def _generate_user_agent(self, os_family)` |
| `_get_domain_front` | method | `modules/evasion_engine.py:232` | `def _get_domain_front(self)` |
| `_persist_profile` | method | `modules/evasion_engine.py:311` | `def _persist_profile(self, profile)` |
| `_pick_uri_pool` | method | `modules/evasion_engine.py:209` | `def _pick_uri_pool(self)` |
| `_random_chrome_version` | method | `modules/evasion_engine.py:139` | `def _random_chrome_version(self)` |
| `_random_firefox_version` | method | `modules/evasion_engine.py:142` | `def _random_firefox_version(self)` |
| `_random_safari_version` | method | `modules/evasion_engine.py:145` | `def _random_safari_version(self)` |
| `generate_profile` | method | `modules/evasion_engine.py:244` | `def generate_profile(self, os_family)` |
| `get_active_profile` | method | `modules/evasion_engine.py:269` | `def get_active_profile(self)` |
| `get_beacon_config` | method | `modules/evasion_engine.py:272` | `def get_beacon_config(self)` |
| `get_history` | method | `modules/evasion_engine.py:328` | `def get_history(self)` |
| `morph_traffic` | method | `modules/evasion_engine.py:287` | `def morph_traffic(self, config)` |
| `profile_to_json` | method | `modules/evasion_engine.py:343` | `def profile_to_json(self, profile)` |
| `rotate_profile` | method | `modules/evasion_engine.py:264` | `def rotate_profile(self, os_family)` |
| `set_config` | method | `modules/evasion_engine.py:136` | `def set_config(self, config)` |
| `EvasivePayloadGenerator` | class | `modules/evasive_payloads.py:18` | `class EvasivePayloadGenerator` |
| `__init__` | method | `modules/evasive_payloads.py:84` | `def __init__(self)` |
| `_apply_encoding_chain` | method | `modules/evasive_payloads.py:118` | `def _apply_encoding_chain(self, data, chain)` |
| `_gzip_compress` | method | `modules/evasive_payloads.py:114` | `def _gzip_compress(self, data)` |
| `_random_string` | method | `modules/evasive_payloads.py:93` | `def _random_string(self, length)` |
| `_random_var` | method | `modules/evasive_payloads.py:87` | `def _random_var(self, length)` |
| `_rot13` | method | `modules/evasive_payloads.py:102` | `def _rot13(self, data)` |
| `_xor_encode` | method | `modules/evasive_payloads.py:97` | `def _xor_encode(self, data, key)` |
| `generate_javascript_obfuscated` | method | `modules/evasive_payloads.py:178` | `def generate_javascript_obfuscated(self, payload)` |
| `generate_linux_evasive` | method | `modules/evasive_payloads.py:214` | `def generate_linux_evasive(self, rhost, rport, technique)` |
| `generate_lolbas_execution` | method | `modules/evasive_payloads.py:284` | `def generate_lolbas_execution(self, payload_url, technique)` |
| `generate_polymorphic_command` | method | `modules/evasive_payloads.py:334` | `def generate_polymorphic_command(self, base_cmd, iterations)` |
| `generate_powershell_obfuscated` | method | `modules/evasive_payloads.py:138` | `def generate_powershell_obfuscated(self, payload, obfuscation_level)` |
| `generate_shellcode_loader_powershell` | method | `modules/evasive_payloads.py:239` | `def generate_shellcode_loader_powershell(self, shellcode_b64, injection_technique)` |
| `generate_vba_obfuscated` | method | `modules/evasive_payloads.py:197` | `def generate_vba_obfuscated(self, payload)` |
| `list_techniques` | method | `modules/evasive_payloads.py:374` | `def list_techniques(self)` |
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
| `AutoRecommender` | class | `modules/event_consumers.py:191` | `class AutoRecommender` |
| `CredentialReactor` | class | `modules/event_consumers.py:262` | `class CredentialReactor` |
| `DashboardPusher` | class | `modules/event_consumers.py:348` | `class DashboardPusher` |
| `PhaseTracker` | class | `modules/event_consumers.py:136` | `class PhaseTracker` |
| `SoulSync` | class | `modules/event_consumers.py:310` | `class SoulSync` |
| `__call__` | method | `modules/event_consumers.py:149` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:197` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:272` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:313` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:351` | `def __call__(self, event)` |
| `__init__` | method | `modules/event_consumers.py:146` | `def __init__(self)` |
| `__init__` | method | `modules/event_consumers.py:194` | `def __init__(self)` |
| `_inject_objective` | function | `modules/event_consumers.py:54` | `def _inject_objective(text, priority, source)` |
| `_load_payload` | function | `modules/event_consumers.py:43` | `def _load_payload()` |
| `_update_soul` | function | `modules/event_consumers.py:100` | `def _update_soul(phase, credentials, access)` |
| `_update_world_model_host` | function | `modules/event_consumers.py:72` | `def _update_world_model_host(address, state, services)` |
| `unwire_all_consumers` | function | `modules/event_consumers.py:399` | `def unwire_all_consumers(bus)` |
| `wire_all_consumers` | function | `modules/event_consumers.py:370` | `def wire_all_consumers(bus)` |
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
| `FindingRecord` | class | `modules/finding_lifecycle.py:218` | `class FindingRecord` |
| `RetestRecord` | class | `modules/finding_lifecycle.py:231` | `class RetestRecord` |
| `_finding_from_row` | function | `modules/finding_lifecycle.py:256` | `def _finding_from_row(row)` |
| `_load` | function | `modules/finding_lifecycle.py:73` | `def _load(sessions_dir)` |
| `_load_retests` | function | `modules/finding_lifecycle.py:328` | `def _load_retests(sessions_dir)` |
| `_retests_path` | function | `modules/finding_lifecycle.py:323` | `def _retests_path(sessions_dir)` |
| `_save` | function | `modules/finding_lifecycle.py:86` | `def _save(sessions_dir, data)` |
| `_save_retests` | function | `modules/finding_lifecycle.py:339` | `def _save_retests(sessions_dir, payload)` |
| `_store_path` | function | `modules/finding_lifecycle.py:68` | `def _store_path(sessions_dir)` |
| `_token_value` | function | `modules/finding_lifecycle.py:241` | `def _token_value(refs, prefix, default)` |
| `_with_token` | function | `modules/finding_lifecycle.py:249` | `def _with_token(refs, prefix, value)` |
| `add_dead_end` | function | `modules/finding_lifecycle.py:137` | `def add_dead_end(kind, value, reason, sessions_dir)` |
| `apply_confirmation` | function | `modules/finding_lifecycle.py:190` | `def apply_confirmation(nodes, sessions_dir)` |
| `classify_retest` | function | `modules/finding_lifecycle.py:420` | `def classify_retest(needle, output)` |
| `confirm` | function | `modules/finding_lifecycle.py:94` | `def confirm(finding_id, evidence, sessions_dir, by)` |
| `evidence_floor` | function | `modules/finding_lifecycle.py:52` | `def evidence_floor(items)` |
| `findings_for` | function | `modules/finding_lifecycle.py:295` | `def findings_for(db, workspace)` |
| `has_running_retest` | function | `modules/finding_lifecycle.py:346` | `def has_running_retest(finding_id, sessions_dir)` |
| `is_dead_end` | function | `modules/finding_lifecycle.py:149` | `def is_dead_end(kind, value, sessions_dir)` |
| `record` | function | `modules/finding_lifecycle.py:270` | `def record(db, workspace, host, title, severity, summary, poc)` |
| `reject` | function | `modules/finding_lifecycle.py:123` | `def reject(finding_id, reason, sessions_dir, by)` |
| `render_markdown` | function | `modules/finding_lifecycle.py:439` | `def render_markdown(db, workspace, title)` |
| `request_retest` | function | `modules/finding_lifecycle.py:354` | `def request_retest(db, finding_id, sessions_dir)` |
| `resolve` | function | `modules/finding_lifecycle.py:162` | `def resolve(node, sessions_dir)` |
| `resolve_retest` | function | `modules/finding_lifecycle.py:374` | `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)` |
| `set_status` | function | `modules/finding_lifecycle.py:300` | `def set_status(db, finding_id, status)` |
| `suppressed_values` | function | `modules/finding_lifecycle.py:156` | `def suppressed_values(sessions_dir)` |
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
| `_catalogue` | function | `modules/gym_matrix_runner.py:36` | `def _catalogue(catalogue)` |
| `_persist` | function | `modules/gym_matrix_runner.py:236` | `def _persist(summary_result, sessions_dir)` |
| `_stats` | function | `modules/gym_matrix_runner.py:220` | `def _stats(runs)` |
| `load_matrix` | function | `modules/gym_matrix_runner.py:252` | `def load_matrix(sessions_dir)` |
| `plan_matrix` | function | `modules/gym_matrix_runner.py:49` | `def plan_matrix(target, sessions_dir, only, top_k, catalogue)` |
| `run_matrix` | function | `modules/gym_matrix_runner.py:104` | `def run_matrix(target)` |
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
| `chain_available` | function | `modules/gym_winbox_runner.py:130` | `def chain_available(vuln_id)` |
| `plan_matrix` | function | `modules/gym_winbox_runner.py:21` | `def plan_matrix(target, sessions_dir, only, top_k)` |
| `report` | function | `modules/gym_winbox_runner.py:118` | `def report(sessions_dir)` |
| `run_matrix` | function | `modules/gym_winbox_runner.py:51` | `def run_matrix(target)` |

Next: [SYMBOLS_p15.md](SYMBOLS_p15.md)
