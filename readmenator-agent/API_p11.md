# API (page 11 of 23)
Previous: [API_p10.md](API_p10.md)

## modules/estorides_importer.py
Depends on: `core/logging.py`, `modules/db.py`
Imported by: `cli/commands/estorides.py`, `modules/intelligence_engine.py`
- `ImportResult.success` (method) `modules/estorides_importer.py:110` `def success(self)`
- `ImportResult.to_dict` (method) `modules/estorides_importer.py:113` `def to_dict(self)`
- `SeedResult.new_assets` (method) `modules/estorides_importer.py:139` `def new_assets(self)`
- `extract_seeds_from_world_model` (function) `modules/estorides_importer.py:143` `def extract_seeds_from_world_model(world_model_path)` -- Extract IPs and domains from world_model.json as estorides seeds.
- `extract_seeds_from_hosts_file` (function) `modules/estorides_importer.py:175` `def extract_seeds_from_hosts_file(path)` -- Extract IPs/domains from hostsdiscovery.txt or similar.
- `extract_seeds_from_db` (function) `modules/estorides_importer.py:203` `def extract_seeds_from_db(db_path)` -- Extract hosts from LazyOwn database.
- `extract_seeds_from_scope` (function) `modules/estorides_importer.py:242` `def extract_seeds_from_scope(scope_entries)` -- Extract scoped IPs/domains from payload.json scope list.
- `run_estorides_discover` (function) `modules/estorides_importer.py:272` `def run_estorides_discover(seed_type, seed_value, max_depth, max_steps, out_json, timeout)` -- Run estorides discover on a single seed.
- `run_estorides_run` (function) `modules/estorides_importer.py:332` `def run_estorides_run(query, out_json, timeout)` -- Run estorides run (single fan-out) on a query.
- `EstoridesCaseReader.__init__` (method) `modules/estorides_importer.py:388` `def __init__(self, db_path)`
- `EstoridesCaseReader.available` (method) `modules/estorides_importer.py:393` `def available(self)`
- `EstoridesCaseReader.list_cases` (method) `modules/estorides_importer.py:402` `def list_cases(self, limit)`
- `EstoridesCaseReader.get_entities` (method) `modules/estorides_importer.py:414` `def get_entities(self, case_id, entity_types, limit)` -- Fetch entities from the case store.
- `EstoridesCaseReader.get_host_entities` (method) `modules/estorides_importer.py:469` `def get_host_entities(self, case_id)` -- Get entities of host-related types (ipv4, ipv6, domain, url, asn).
- `EstoridesCaseReader.get_all_entities` (method) `modules/estorides_importer.py:473` `def get_all_entities(self, case_id)`
- `EstoridesCaseReader.stats` (method) `modules/estorides_importer.py:476` `def stats(self)`
- `EstoridesCaseReader.close` (method) `modules/estorides_importer.py:489` `def close(self)`
- `EstoridesStixParser.__init__` (method) `modules/estorides_importer.py:511` `def __init__(self, stix_path)`
- `EstoridesStixParser.available` (method) `modules/estorides_importer.py:515` `def available(self)`
- `EstoridesStixParser.parse` (method) `modules/estorides_importer.py:518` `def parse(self)` -- Parse a STIX 2.1 bundle into EstoridesEntity objects.
- `EstoridesStixParser.parse_by_type` (method) `modules/estorides_importer.py:552` `def parse_by_type(self, entity_types)` -- Parse STIX and group values by entity type.
- `find_lan_bundle_files` (function) `modules/estorides_importer.py:586` `def find_lan_bundle_files(lan_dir, sessions_dir)` -- Locate LAN bundle deliverables.
- `LanBundleReader.__init__` (method) `modules/estorides_importer.py:632` `def __init__(self, lan_dir)`
- `LanBundleReader.available` (method) `modules/estorides_importer.py:636` `def available(self)`
- `LanBundleReader.read_devices` (method) `modules/estorides_importer.py:639` `def read_devices(self)` -- Return raw device dicts from the inventory file.
- `LanBundleReader.parse` (method) `modules/estorides_importer.py:652` `def parse(self)` -- Parse LAN devices into entities (host, mac, domain).
- `LanBundleReader.attack_targets` (method) `modules/estorides_importer.py:683` `def attack_targets(self)` -- IPs actionable for the attack graph and auto_loop queue.
- `ensure_directories` (function) `modules/estorides_importer.py:694` `def ensure_directories()` -- Ensure sessions/ directories exist.
- `EstoridesToLazyOwnBridge.__init__` (method) `modules/estorides_importer.py:703` `def __init__(self, db_path, config_path)`
- `EstoridesToLazyOwnBridge.import_entities` (method) `modules/estorides_importer.py:711` `def import_entities(self, entities, add_to_scope, add_to_db)` -- Import entities into LazyOwn DB and optionally scope.
- `EstoridesToLazyOwnBridge.get_combined_surface` (method) `modules/estorides_importer.py:834` `def get_combined_surface(self)` -- Get the combined attack surface from LazyOwn DB + scope.
- `FeedbackLoop.__init__` (method) `modules/estorides_importer.py:892` `def __init__(self, max_iterations, max_depth, max_steps, timeout)`
- `FeedbackLoop.run` (method) `modules/estorides_importer.py:908` `def run(self, seed_methods)` -- Run the feedback loop.
- `export_combined_graph` (function) `modules/estorides_importer.py:1027` `def export_combined_graph(output_path)` -- Export the combined (Estorides + LazyOwn) graph as GraphML.

## modules/evasion_engine.py
Imported by: `cli/commands/evasive_payload.py`, `skills/lazyown_mcp.py`
- `EvasionEngine.__init__` (method) `modules/evasion_engine.py:130` `def __init__(self, config)`
- `EvasionEngine.set_config` (method) `modules/evasion_engine.py:136` `def set_config(self, config)`
- `EvasionEngine.generate_profile` (method) `modules/evasion_engine.py:244` `def generate_profile(self, os_family)`
- `EvasionEngine.rotate_profile` (method) `modules/evasion_engine.py:264` `def rotate_profile(self, os_family)`
- `EvasionEngine.get_active_profile` (method) `modules/evasion_engine.py:269` `def get_active_profile(self)`
- `EvasionEngine.get_beacon_config` (method) `modules/evasion_engine.py:272` `def get_beacon_config(self)`
- `EvasionEngine.morph_traffic` (method) `modules/evasion_engine.py:287` `def morph_traffic(self, config)`
- `EvasionEngine.get_history` (method) `modules/evasion_engine.py:328` `def get_history(self)`
- `EvasionEngine.profile_to_json` (method) `modules/evasion_engine.py:343` `def profile_to_json(self, profile)`

## modules/evasive_payloads.py
Imported by: `cli/commands/evasive_payload.py`
- `EvasivePayloadGenerator.__init__` (method) `modules/evasive_payloads.py:84` `def __init__(self)`
- `EvasivePayloadGenerator.generate_powershell_obfuscated` (method) `modules/evasive_payloads.py:138` `def generate_powershell_obfuscated(self, payload, obfuscation_level)` -- Generate an obfuscated PowerShell payload.
- `EvasivePayloadGenerator.generate_javascript_obfuscated` (method) `modules/evasive_payloads.py:178` `def generate_javascript_obfuscated(self, payload)` -- Generate an obfuscated JavaScript payload.
- `EvasivePayloadGenerator.generate_vba_obfuscated` (method) `modules/evasive_payloads.py:197` `def generate_vba_obfuscated(self, payload)` -- Generate an obfuscated VBA macro payload.
- `EvasivePayloadGenerator.generate_linux_evasive` (method) `modules/evasive_payloads.py:214` `def generate_linux_evasive(self, rhost, rport, technique)` -- Generate an evasive Linux reverse shell payload.
- `EvasivePayloadGenerator.generate_shellcode_loader_powershell` (method) `modules/evasive_payloads.py:239` `def generate_shellcode_loader_powershell(self, shellcode_b64, injection_technique)` -- Generate a PowerShell shellcode loader with AMSI bypass.
- `EvasivePayloadGenerator.generate_lolbas_execution` (method) `modules/evasive_payloads.py:284` `def generate_lolbas_execution(self, payload_url, technique)` -- Generate a LOLBAS-based payload execution command.
- `EvasivePayloadGenerator.generate_polymorphic_command` (method) `modules/evasive_payloads.py:334` `def generate_polymorphic_command(self, base_cmd, iterations)` -- Generate a polymorphic command that mutates at each execution.
- `EvasivePayloadGenerator.list_techniques` (method) `modules/evasive_payloads.py:374` `def list_techniques(self)` -- Return all available evasion techniques.

## modules/event_bus.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/collab_bp.py`, `modules/engagement_hooks.py`
Imported by: `lazyc2.py`, `lazyown.py`, `modules/command_executor.py`, `modules/event_consumers.py`, `modules/loop_ai_bridge.py`, `modules/state_manager.py`, `modules/unified_bridge.py`, `skills/lazyown_mcp.py`, `tests/test_loop_ai_bridge.py`
- `LazyEvent.to_dict` (method) `modules/event_bus.py:96` `def to_dict(self)`
- `LazyEvent.to_json` (method) `modules/event_bus.py:111` `def to_json(self)`
- `LazyEvent.from_dict` (method) `modules/event_bus.py:115` `def from_dict(cls, d)`
- `Sink.write` (method) `modules/event_bus.py:137` `def write(self, event)`
- `Sink.close` (method) `modules/event_bus.py:140` `def close(self)`
- `JsonlSink.__init__` (method) `modules/event_bus.py:146` `def __init__(self, filepath)`
- `JsonlSink.write` (method) `modules/event_bus.py:151` `def write(self, event)`
- `JsonlSink.close` (method) `modules/event_bus.py:159` `def close(self)`
- `CollabBusSink.__init__` (method) `modules/event_bus.py:166` `def __init__(self)`
- `CollabBusSink.write` (method) `modules/event_bus.py:181` `def write(self, event)`
- `CollabBusSink.close` (method) `modules/event_bus.py:198` `def close(self)`
- `EngagementSink.write` (method) `modules/event_bus.py:205` `def write(self, event)`
- `EngagementSink.close` (method) `modules/event_bus.py:226` `def close(self)`
- `UnifiedEventBus.__init__` (method) `modules/event_bus.py:255` `def __init__(self)`
- `UnifiedEventBus.instance` (method) `modules/event_bus.py:287` `def instance(cls)`
- `UnifiedEventBus.subscriber_count` (method) `modules/event_bus.py:295` `def subscriber_count(self)` -- Return the number of active subscribers across all registration types.
- `UnifiedEventBus.subscribe` (method) `modules/event_bus.py:300` `def subscribe(self, subscriber_id, callback)` -- Register a callback for all events.
- `UnifiedEventBus.subscribe_topic` (method) `modules/event_bus.py:305` `def subscribe_topic(self, subscriber_id, topic, callback)` -- Register a callback for events matching a topic.
- `UnifiedEventBus.subscribe_async` (method) `modules/event_bus.py:315` `def subscribe_async(self, subscriber_id)` -- Get a Queue for async event consumption (for SSE, WebSocket, etc.).
- `UnifiedEventBus.unsubscribe` (method) `modules/event_bus.py:327` `def unsubscribe(self, subscriber_id)` -- Remove all subscriptions for a subscriber.
- `UnifiedEventBus.publish` (method) `modules/event_bus.py:336` `def publish(self, event)` -- Publish an event via the bounded dispatch queue.
- `UnifiedEventBus.drain` (method) `modules/event_bus.py:354` `def drain(self)` -- Consume and drop all pending events from the dispatch queue.
- `UnifiedEventBus.shutdown` (method) `modules/event_bus.py:372` `def shutdown(self)` -- Shut down the event bus cleanly.
- `UnifiedEventBus.history` (method) `modules/event_bus.py:556` `def history(self, n, category)` -- Return recent events, optionally filtered by category.
- `UnifiedEventBus.history_since` (method) `modules/event_bus.py:564` `def history_since(self, since_ts)` -- Return all events since a given timestamp.
- `get_event_bus` (function) `modules/event_bus.py:570` `def get_event_bus()` -- Return the singleton UnifiedEventBus instance.
- `publish_event` (function) `modules/event_bus.py:575` `def publish_event(category, event_type, source, payload, severity, target, operator)` -- Convenience function to build and publish an event in one call.

## modules/event_consumers.py
Depends on: `core/logging.py`, `modules/event_bus.py`, `modules/state_manager.py`
Imported by: `lazyc2.py`, `lazyown.py`, `skills/autonomous_daemon.py`
- `PhaseTracker.__init__` (method) `modules/event_consumers.py:156` `def __init__(self)`
- `PhaseTracker.__call__` (method) `modules/event_consumers.py:159` `def __call__(self, event)`
- `AutoRecommender.__init__` (method) `modules/event_consumers.py:204` `def __init__(self)`
- `AutoRecommender.__call__` (method) `modules/event_consumers.py:207` `def __call__(self, event)`
- `CredentialReactor.__call__` (method) `modules/event_consumers.py:282` `def __call__(self, event)`
- `SoulSync.__call__` (method) `modules/event_consumers.py:323` `def __call__(self, event)`
- `DashboardPusher.__call__` (method) `modules/event_consumers.py:361` `def __call__(self, event)`
- `wire_all_consumers` (function) `modules/event_consumers.py:380` `def wire_all_consumers(bus)` -- Register all event consumers on the UnifiedEventBus.
- `unwire_all_consumers` (function) `modules/event_consumers.py:409` `def unwire_all_consumers(bus)` -- Remove all event consumers from the bus.

## modules/event_engine.py
Imported by: `lazyc2.py`, `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`, `skills/sessions_watcher.py`
- `load_rules` (function) `modules/event_engine.py:99` `def load_rules()` -- Load rules from event_rules.json, creating it with defaults if missing.
- `save_rules` (function) `modules/event_engine.py:110` `def save_rules(rules)`
- `add_rule` (function) `modules/event_engine.py:114` `def add_rule(rule)` -- Add or replace a rule by id.
- `process_new_rows` (function) `modules/event_engine.py:181` `def process_new_rows()` -- Read new rows from the session CSV since last watermark.
- `read_events` (function) `modules/event_engine.py:250` `def read_events(limit, status)` -- Return up to `limit` events matching `status` (pending/processed/all).
- `ack_event` (function) `modules/event_engine.py:270` `def ack_event(event_id)` -- Mark an event as processed.

## modules/evidence.py
Imported by: `modules/engage_summary.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_summary.py`, `tests/test_lazy_parity.py`, `tests/test_safety_gates.py`
- `hash_bytes` (function) `modules/evidence.py:37` `def hash_bytes(data)` -- Return the lowercase hex SHA-256 of data.
- `EvidenceStore.__init__` (method) `modules/evidence.py:57` `def __init__(self, base_dir)` -- Create vault directories.
- `EvidenceStore.blob_path` (method) `modules/evidence.py:65` `def blob_path(self, content_hash)` -- Resolve the canonical path for a validated hash.
- `EvidenceStore.put` (method) `modules/evidence.py:70` `def put(self, data)` -- Atomically store bytes and return their SHA-256 hash.
- `EvidenceStore.get` (method) `modules/evidence.py:90` `def get(self, content_hash)` -- Read and verify blob bytes for a hash.
- `EvidenceStore.exists` (method) `modules/evidence.py:98` `def exists(self, content_hash)` -- Return True when the blob exists on disk.
- `EvidenceStore.garbage_collect` (method) `modules/evidence.py:105` `def garbage_collect(self, referenced)` -- Remove unreferenced blobs older than the grace period.

## modules/exp.c
Imported by: `static/js/3d-force-graph-1.73.4.min.js`, `static/js/force-graph-1.43.5.min.js`
- `add_key` (function) `modules/exp.c:147` `static inline key_serial_t add_key(const char *type, const char *description, const void *payload...`
- `keyctl` (function) `modules/exp.c:151` `static inline long keyctl(int operation, unsigned long arg2, unsigned long arg3, unsigned long ar...`
- `bye` (function) `modules/exp.c:155` `void bye(char *info)`
- `do_error_exit` (function) `modules/exp.c:161` `void do_error_exit(char *info)`
- `bye2` (function) `modules/exp.c:167` `void bye2(char *info, char *arg)`
- `spray_keyring` (function) `modules/exp.c:172` `key_serial_t *spray_keyring(uint32_t start, uint32_t spray_size)`
- `spray_keyring_list_del_purpose` (function) `modules/exp.c:190` `key_serial_t *spray_keyring_list_del_purpose(uint32_t spray_size, uint64_t next, uint64_t prev, u...`
- `spray_keyring_list_overwrite_purpose` (function) `modules/exp.c:214` `key_serial_t *spray_keyring_list_overwrite_purpose(uint32_t spray_size, uint64_t len, uint64_t of...`
- `get_keyring_leak` (function) `modules/exp.c:248` `int get_keyring_leak(key_serial_t *id_buffer, uint32_t id_buffer_size)`
- `awake_partial_keys` (function) `modules/exp.c:271` `void awake_partial_keys(key_serial_t *id_buffer, uint32_t idx)`
- `release_keys` (function) `modules/exp.c:279` `void release_keys(key_serial_t *id_buffer, uint32_t id_buffer_size)`
- `release_partial_keys` (function) `modules/exp.c:290` `void release_partial_keys(key_serial_t *id_buffer, int i)`
- `unshare_setup` (function) `modules/exp.c:297` `void unshare_setup(uid_t uid, gid_t gid)`
- `set_stable_table_and_set` (function) `modules/exp.c:322` `void set_stable_table_and_set(struct mnl_socket* nl, const char *name)`
- `set_trigger_set_and_overwrite` (function) `modules/exp.c:385` `void set_trigger_set_and_overwrite(struct mnl_socket* nl, const char *name, const char *set_name)`
- `set_cpu_affinity` (function) `modules/exp.c:438` `void set_cpu_affinity(int cpu_n, pid_t pid)`
- `spray_mqueue` (function) `modules/exp.c:448` `void spray_mqueue(mqd_t mqdes, char *msgptr, int spray_size)`
- `gather_mqueue` (function) `modules/exp.c:463` `int gather_mqueue(mqd_t mqdes, int gather_size)`
- `gather_mqueue_nosave` (function) `modules/exp.c:485` `int gather_mqueue_nosave(mqd_t mqdes, int gather_size)`
- `spray_msg_msg` (function) `modules/exp.c:496` `void spray_msg_msg(unsigned int size, unsigned int amount, int qid)`
- `io_uring_setup` (function) `modules/exp.c:520` `static inline int io_uring_setup(uint32_t entries, struct io_uring_params *p)`
- `io_uring_register` (function) `modules/exp.c:524` `static inline int io_uring_register(int fd, unsigned int opcode, void *arg, unsigned int nr_args)`
- `spray_uring` (function) `modules/exp.c:529` `struct fd_uring *spray_uring(uint32_t spray_size, struct fd_uring *fd_buffer)`
- `release_uring` (function) `modules/exp.c:546` `void release_uring(struct fd_uring *fd_buffer, uint32_t buffer_size)`
- `release_partial_uring` (function) `modules/exp.c:554` `void release_partial_uring(struct fd_uring *fd_buffer, uint32_t buffer_idx)`
- `prepare_root_shell` (function) `modules/exp.c:559` `void prepare_root_shell(void)`
- `create_dummy_file` (function) `modules/exp.c:564` `void create_dummy_file(void)`
- `create_priv_file` (function) `modules/exp.c:572` `void create_priv_file(void)`
- `write_new_modprobe` (function) `modules/exp.c:582` `void write_new_modprobe()`
- `setup_modprobe_payload` (function) `modules/exp.c:601` `void setup_modprobe_payload()`
- `userland_T` (function) `modules/exp.c:605` `void userland_T(int *sema)`
- `sema_up` (function) `modules/exp.c:610` `void sema_up(int *sema)`
- `sema_down` (function) `modules/exp.c:615` `void sema_down(int *sema)`
- `main` (function) `modules/exp.c:620` `int main(int argc, char ** argv)`

## modules/exploit_chain.py
Imported by: `cli/commands/exploit_migrated.py`
- `ExploitChain.__init__` (method) `modules/exploit_chain.py:292` `def __init__(self, rhost, rport, lhost, lport, sessions_dir, nmap_xml_path)`
- `ExploitChain.fingerprint_services` (method) `modules/exploit_chain.py:311` `def fingerprint_services(self, nmap_output)` -- Parse service information from all available nmap XML files.
- `ExploitChain.map_vulnerabilities` (method) `modules/exploit_chain.py:446` `def map_vulnerabilities(self)` -- Map discovered services to known vulnerabilities.
- `ExploitChain.generate_exploit_plan` (method) `modules/exploit_chain.py:499` `def generate_exploit_plan(self)` -- Generate a prioritized exploitation plan.
- `ExploitChain.get_post_exploit_commands` (method) `modules/exploit_chain.py:519` `def get_post_exploit_commands(self, platform)` -- Return recommended post-exploitation commands for the platform.
- `ExploitChain.generate_report` (method) `modules/exploit_chain.py:531` `def generate_report(self)` -- Generate a structured exploitation chain report.
- `ExploitChain.save_report` (method) `modules/exploit_chain.py:566` `def save_report(self, path)` -- Save the exploitation chain report to a file.

## modules/exploit_recommender.py
Depends on: `lazygui/version.py`, `modules/world_model.py`
Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/pwn.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`
- `parse_version` (function) `modules/exploit_recommender.py:25` `def parse_version(v)`
- `ExploitRecommender.__init__` (method) `modules/exploit_recommender.py:120` `def __init__(self, world_model)`
- `ExploitRecommender.set_world_model` (method) `modules/exploit_recommender.py:129` `def set_world_model(self, world_model)`
- `ExploitRecommender.set_nvd_api_key` (method) `modules/exploit_recommender.py:132` `def set_nvd_api_key(self, key)`
- `ExploitRecommender.match_services` (method) `modules/exploit_recommender.py:244` `def match_services(self, hosts)` -- Match discovered services against known CVEs with confidence scoring.
- `ExploitRecommender.recommend` (method) `modules/exploit_recommender.py:337` `def recommend(self, hosts, top_n)` -- Return top-N recommended exploits as structured dicts for MCP/CLI.
- `ExploitRecommender.persist_recommendations` (method) `modules/exploit_recommender.py:370` `def persist_recommendations(self, matches)` -- Save recommendations to sessions/ for audit and replay.
- `ExploitRecommender.format_for_llm` (method) `modules/exploit_recommender.py:390` `def format_for_llm(self, matches, max_items)` -- Format recommendations as compact text for LLM context injection.

## modules/exploitgym_gym.py
Depends on: `modules/redteam_gym.py`
Imported by: `cli/commands/exploitgym.py`, `skills/lazyown_mcp.py`, `tests/test_exploitgym_gym.py`
- `check_readiness` (function) `modules/exploitgym_gym.py:112` `def check_readiness(params)` -- Report whether the ExploitGym harness can run.
- `list_tasks` (function) `modules/exploitgym_gym.py:178` `def list_tasks(params, domain, limit)` -- List available ExploitGym tasks, optionally filtered by domain.
- `setup_harness` (function) `modules/exploitgym_gym.py:249` `def setup_harness(params, steps)` -- Automate ExploitGym installation (clone, deps, data, firewall, images).
- `pull_task` (function) `modules/exploitgym_gym.py:344` `def pull_task(task_id, params, timeout)` -- Pull the Docker image required by a task.
- `run_task` (function) `modules/exploitgym_gym.py:423` `def run_task(task_id, params, model, mitigations, timeout)` -- Run the agent against an ExploitGym task and capture the outcome.
- `verify_flag` (function) `modules/exploitgym_gym.py:548` `def verify_flag(task_id, params)` -- Verify whether a task flag was captured from a previous run.
- `score_task` (function) `modules/exploitgym_gym.py:565` `def score_task(task_id, success, techniques, params)` -- Award Red Team Gym ELO and leaderboard points for a task outcome.

## modules/fast_run_service.sh
- `log_timestamp` (function) `modules/fast_run_service.sh:69` -- # # Logging primitives.
- `log_info` (function) `modules/fast_run_service.sh:73`
- `log_warn` (function) `modules/fast_run_service.sh:77`
- `log_error` (function) `modules/fast_run_service.sh:81`
- `require_root` (function) `modules/fast_run_service.sh:89` -- # # Pre-flight checks.
- `require_deps` (function) `modules/fast_run_service.sh:97`
- `require_paths` (function) `modules/fast_run_service.sh:113`
- `prepare_runtime_dirs` (function) `modules/fast_run_service.sh:126`
- `load_config` (function) `modules/fast_run_service.sh:139`
- `config_truthy` (function) `modules/fast_run_service.sh:155`
- `pid_file_for` (function) `modules/fast_run_service.sh:166` -- # # PID-file primitives.
- `log_file_for` (function) `modules/fast_run_service.sh:171`
- `read_pid_value` (function) `modules/fast_run_service.sh:176`
- `is_pid_alive` (function) `modules/fast_run_service.sh:189`
- `is_service_running` (function) `modules/fast_run_service.sh:194`
- `write_pid_file` (function) `modules/fast_run_service.sh:201`
- `ensure_log_file` (function) `modules/fast_run_service.sh:211`
- `spawn_as_target_user` (function) `modules/fast_run_service.sh:228` -- # # Process spawn primitives.
- `spawn_as_root` (function) `modules/fast_run_service.sh:247`
- `terminate_pid_tree` (function) `modules/fast_run_service.sh:264`
- `stop_named_service` (function) `modules/fast_run_service.sh:292`
- `chown_project_tree` (function) `modules/fast_run_service.sh:310` -- # # Ownership maintenance.
- `start_chown_watcher` (function) `modules/fast_run_service.sh:315`
- `start_lazyc2_service` (function) `modules/fast_run_service.sh:342` -- # # Concrete service launchers.
- `start_www_service` (function) `modules/fast_run_service.sh:356`
- `start_vpn_service` (function) `modules/fast_run_service.sh:363`
- `start_discord_service` (function) `modules/fast_run_service.sh:380`
- `start_telegram_service` (function) `modules/fast_run_service.sh:390`
- `start_cloudflare_service` (function) `modules/fast_run_service.sh:400`
- `start_ollama_service` (function) `modules/fast_run_service.sh:410`
- `managed_services_in_order` (function) `modules/fast_run_service.sh:429` -- # # Service registry.
- `cmd_start` (function) `modules/fast_run_service.sh:445` -- # # Lifecycle commands.
- `cmd_stop` (function) `modules/fast_run_service.sh:465`
- `cmd_restart` (function) `modules/fast_run_service.sh:480`
- `cmd_status` (function) `modules/fast_run_service.sh:486`
- `cmd_logs` (function) `modules/fast_run_service.sh:505`
- `cmd_chown_now` (function) `modules/fast_run_service.sh:521`
- `usage` (function) `modules/fast_run_service.sh:528`
- `main` (function) `modules/fast_run_service.sh:557` -- # # Entry point. require_root re-executes under sudo and never returns there; # the case-arm dispatch is reached...

## modules/finding_lifecycle.py
Depends on: `modules/osint_enrich.py`
Imported by: `cli/commands/database.py`, `modules/attack_surface3d.py`, `modules/intel_fusion.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `tests/test_autonomous_ops.py`, `tests/test_finding_lifecycle.py`
- `confirm` (function) `modules/finding_lifecycle.py:61` `def confirm(finding_id, evidence, sessions_dir, by)` -- Mark a finding confirmed with linked evidence (CAIRN seed-add).
- `reject` (function) `modules/finding_lifecycle.py:90` `def reject(finding_id, reason, sessions_dir, by)` -- Mark a finding rejected (disproven lead, CAIRN dead-end discipline).
- `add_dead_end` (function) `modules/finding_lifecycle.py:104` `def add_dead_end(kind, value, reason, sessions_dir)` -- Suppress a value campaign-wide with a labeled reason (dead_end_hashes).
- `is_dead_end` (function) `modules/finding_lifecycle.py:116` `def is_dead_end(kind, value, sessions_dir)` -- Return True when a kind/value pair sits on the suppression list.
- `suppressed_values` (function) `modules/finding_lifecycle.py:123` `def suppressed_values(sessions_dir)` -- Return every suppressed value for text-level filtering by the loop.
- `resolve` (function) `modules/finding_lifecycle.py:129` `def resolve(node, sessions_dir)` -- Resolve a finding node's confirmation state.
- `apply_confirmation` (function) `modules/finding_lifecycle.py:154` `def apply_confirmation(nodes, sessions_dir)` -- Stamp ``confirmation``/``status`` on every finding node in place.
- `record` (function) `modules/finding_lifecycle.py:234` `def record(db, workspace, host, title, severity, summary, poc)` -- Record a campaign finding on the DB for one host.
- `findings_for` (function) `modules/finding_lifecycle.py:259` `def findings_for(db, workspace)` -- List campaign findings with parsed status markers.
- `set_status` (function) `modules/finding_lifecycle.py:264` `def set_status(db, finding_id, status)` -- Set the lifecycle status marker on one finding.
- `has_running_retest` (function) `modules/finding_lifecycle.py:310` `def has_running_retest(finding_id, sessions_dir)` -- Return True while a retest for the finding is still running.
- `request_retest` (function) `modules/finding_lifecycle.py:318` `def request_retest(db, finding_id, sessions_dir)` -- Queue a retest; an already-running one is returned unchanged.
- `resolve_retest` (function) `modules/finding_lifecycle.py:338` `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)` -- Close a retest, bump the evidence version and apply the verdict.
- `classify_retest` (function) `modules/finding_lifecycle.py:384` `def classify_retest(needle, output)` -- Map retest output onto reproducible / fixed / inconclusive.
- `render_markdown` (function) `modules/finding_lifecycle.py:403` `def render_markdown(db, workspace, title)` -- Render campaign findings as a markdown report.

## modules/forensic_cleaner.py
Imported by: `cli/commands/opsec_cleanup.py`
- `ForensicCleaner.__init__` (method) `modules/forensic_cleaner.py:67` `def __init__(self, config)`
- `ForensicCleaner.windows_cleanup` (method) `modules/forensic_cleaner.py:70` `def windows_cleanup(self)` -- Generate Windows forensic artifact cleanup commands.
- `ForensicCleaner.linux_cleanup` (method) `modules/forensic_cleaner.py:165` `def linux_cleanup(self)` -- Generate Linux forensic artifact cleanup commands.
- `ForensicCleaner.macos_cleanup` (method) `modules/forensic_cleaner.py:193` `def macos_cleanup(self)` -- Generate macOS forensic artifact cleanup commands.
- `ForensicCleaner.windows_prefetch_parse` (method) `modules/forensic_cleaner.py:221` `def windows_prefetch_parse(self, prefetch_path)` -- Parse Prefetch files to identify what the attacker should clean.
- `ForensicCleaner.amcache_parse` (method) `modules/forensic_cleaner.py:259` `def amcache_parse(self)` -- Parse Amcache registry entries for evidence of execution.

## modules/gcp_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `GCPAttackEngine.__init__` (method) `modules/gcp_attacks.py:90` `def __init__(self, config)`
- `GCPAttackEngine.enumerate_iam_policy` (method) `modules/gcp_attacks.py:93` `def enumerate_iam_policy(self, resource)` -- Enumerate IAM policies for projects, folders, or organizations.
- `GCPAttackEngine.service_account_impersonation` (method) `modules/gcp_attacks.py:119` `def service_account_impersonation(self)` -- Exploit service account impersonation for privilege escalation.
- `GCPAttackEngine.cloud_functions_backdoor` (method) `modules/gcp_attacks.py:144` `def cloud_functions_backdoor(self)` -- Backdoor Cloud Functions for privilege escalation.
- `GCPAttackEngine.compute_engine_metadata_exfil` (method) `modules/gcp_attacks.py:173` `def compute_engine_metadata_exfil(self)` -- Exfiltrate GCE instance metadata and service account tokens.
- `GCPAttackEngine.gcs_enumeration` (method) `modules/gcp_attacks.py:194` `def gcs_enumeration(self)` -- Enumerate Cloud Storage buckets for sensitive data.
- `GCPAttackEngine.cloudbuild_abuse` (method) `modules/gcp_attacks.py:230` `def cloudbuild_abuse(self)` -- Abuse Cloud Build for privilege escalation.
- `GCPAttackEngine.organization_escalation` (method) `modules/gcp_attacks.py:261` `def organization_escalation(self)` -- Escalate from project-level to organization-level access.
- `GCPAttackEngine.summary` (method) `modules/gcp_attacks.py:297` `def summary(self)`

## modules/generate_tools.py
- `extract_cmd2_tools` (function) `modules/generate_tools.py:6` `def extract_cmd2_tools(script_path)`

## modules/goals.py
Imported by: `cli/commands/daemon_ctl.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_parity.py`
- `TaskConstraints.blocked` (method) `modules/goals.py:35` `def blocked(self, command)` -- Return the blocking constraint or empty string.
- `decompose_rule_based` (function) `modules/goals.py:63` `def decompose_rule_based(objective_text, max_goals)` -- Split objective text into goal specs without an LLM (deterministic).
- `load_constraints` (function) `modules/goals.py:83` `def load_constraints(payload)` -- Build constraints from payload config (deny wins, LAZY parity).
- `constraint_block_text` (function) `modules/goals.py:103` `def constraint_block_text(constraints)` -- Render the constraint block injected at max priority (LAZY parity).
- `GoalTracker.__init__` (method) `modules/goals.py:120` `def __init__(self, goals)` -- Bind to an initial goal list.
- `GoalTracker.goals` (method) `modules/goals.py:125` `def goals(self)` -- Return a copy of tracked goals.
- `GoalTracker.prove_goal` (method) `modules/goals.py:129` `def prove_goal(self, goal_text, evidence)` -- Mark one goal achieved from evidence; return True when found.
- `GoalTracker.goal_met` (method) `modules/goals.py:140` `def goal_met(self, opt_in)` -- End the whole task; requires explicit opt-in (default unbound).
- `GoalTracker.all_achieved` (method) `modules/goals.py:148` `def all_achieved(self)` -- Return True when every goal is achieved.
- `GoalTracker.open_goals` (method) `modules/goals.py:152` `def open_goals(self)` -- Return goals still open.

## modules/gpo_abuse.py
Imported by: `cli/commands/active_directory.py`
- `GPOAbuseEngine.__init__` (method) `modules/gpo_abuse.py:118` `def __init__(self, domain, dc_ip)`
- `GPOAbuseEngine.parse_gpo_list` (method) `modules/gpo_abuse.py:124` `def parse_gpo_list(self, raw_gpo_output)` -- Parse Get-GPO or ldapsearch output for GPO information.
- `GPOAbuseEngine.parse_bloodhound_gpos` (method) `modules/gpo_abuse.py:160` `def parse_bloodhound_gpos(self, bloodhound_nodes)` -- Parse BloodHound GPO nodes for abusable policies.
- `GPOAbuseEngine.plan_scheduled_task` (method) `modules/gpo_abuse.py:182` `def plan_scheduled_task(self, gpo, command, task_name)` -- Plan a GPO-backed scheduled task for immediate code execution.
- `GPOAbuseEngine.plan_startup_script` (method) `modules/gpo_abuse.py:208` `def plan_startup_script(self, gpo, script_content, script_name)` -- Plan a GPO startup script for persistence via SYSVOL.
- `GPOAbuseEngine.plan_logon_script` (method) `modules/gpo_abuse.py:238` `def plan_logon_script(self, gpo, command)` -- Plan a GPO user logon script for user-triggered code execution.
- `GPOAbuseEngine.plan_local_admin_addition` (method) `modules/gpo_abuse.py:266` `def plan_local_admin_addition(self, gpo, username, group)` -- Plan adding a user to the local Administrators group via GPO preferences.
- `GPOAbuseEngine.plan_wmi_filter_abuse` (method) `modules/gpo_abuse.py:293` `def plan_wmi_filter_abuse(self, gpo, wmi_query)` -- Plan WMI filter abuse for targeted GPO scope control.
- `GPOAbuseEngine.plan_registry_preference` (method) `modules/gpo_abuse.py:322` `def plan_registry_preference(self, gpo, registry_path, value_name, value_data, value_type)` -- Plan a registry modification via GPO preferences.
- `GPOAbuseEngine.plan_service_installation` (method) `modules/gpo_abuse.py:356` `def plan_service_installation(self, gpo, service_name, binary_path)` -- Plan a service installation via GPO for SYSTEM-level persistence.
- `GPOAbuseEngine.generate_all_plans` (method) `modules/gpo_abuse.py:382` `def generate_all_plans(self, command, username)` -- Generate all abuse plans for the discovered GPOs.
- `GPOAbuseEngine.detect_risky_gpos` (method) `modules/gpo_abuse.py:406` `def detect_risky_gpos(self)` -- Identify GPOs with risky configurations for post-compromise cleanup.
- `GPOAbuseEngine.summary` (method) `modules/gpo_abuse.py:434` `def summary(self)` -- Return a summary of GPO abuse capabilities.

## modules/gui_askpass.sh
- `has` (function) `modules/gui_askpass.sh:22` -- ── helpers ───────────────────────────────────────────────────────────────────
- `try_zenity` (function) `modules/gui_askpass.sh:24`
- `try_yad` (function) `modules/gui_askpass.sh:28`
- `try_ssh_askpass` (function) `modules/gui_askpass.sh:33`
- `try_kdialog` (function) `modules/gui_askpass.sh:40`

## modules/hash_cracker.py
Depends on: `core/defaults.py`, `core/logging.py`, `modules/db.py`
Imported by: `cli/commands/security.py`, `tests/test_hash_cracker.py`
- `HashCracker.__init__` (method) `modules/hash_cracker.py:164` `def __init__(self, wordlist, rules, use_hashcat, timeout)`
- `HashCracker.identify` (method) `modules/hash_cracker.py:186` `def identify(self, line)` -- Identify the hash type of a single line.
- `HashCracker.identify_file` (method) `modules/hash_cracker.py:273` `def identify_file(self, filepath)` -- Parse a hash file and group hashes by type.
- `HashCracker.crack_hash` (method) `modules/hash_cracker.py:295` `def crack_hash(self, hash_value, hash_type, wordlist)` -- Attempt to crack a single hash.
- `HashCracker.crack_file` (method) `modules/hash_cracker.py:349` `def crack_file(self, filepath, wordlist, hash_types)` -- Crack all hashes in a file.
- `HashCracker.import_to_db` (method) `modules/hash_cracker.py:405` `def import_to_db(self, results, rhost, workspace_name)` -- Import cracked results into the LazyOwnDB credentials table.
- `crack_secretsdump_output` (function) `modules/hash_cracker.py:695` `def crack_secretsdump_output(filepath, wordlist, rhost)` -- Convenience function: crack a secretsdump output file and import results.

## modules/hive_invoke.py
Depends on: `modules/toposwarm_bridge.py`
- `main` (function) `modules/hive_invoke.py:255` `def main(argv)`

## modules/hostdiscover.sh
- `extract_ips_from_arp` (function) `modules/hostdiscover.sh:21`
- `extract_listening_ips_from_netstat` (function) `modules/hostdiscover.sh:26`

## modules/ia_code_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `CodeAnalyzer.__init__` (method) `modules/ia_code_analysis.py:33` `def __init__(self, mode)`
- `CodeAnalyzer.analyze_directory` (method) `modules/ia_code_analysis.py:37` `def analyze_directory(self, directory)` -- Recursively analyzes all source code files in the specified directory.
- `CodeAnalyzer.analyze_code_file` (method) `modules/ia_code_analysis.py:49` `def analyze_code_file(self, file_path)` -- Analyzes the content of the source code file.
- `analyze_with_deepseek` (function) `modules/ia_code_analysis.py:66` `def analyze_with_deepseek(code_content, file_path, mode)` -- Sends the code content to DeepSeek for analysis.
- `save_results_to_json` (function) `modules/ia_code_analysis.py:123` `def save_results_to_json(results, file_path)` -- Saves the analysis results to JSON files.
- `start_analysis` (function) `modules/ia_code_analysis.py:169` `def start_analysis(code_dir, mode)` -- Starts the analysis of the specified code directory.
- `parse_args` (function) `modules/ia_code_analysis.py:178` `def parse_args()`

## modules/ia_logs_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `LogFileHandler.__init__` (method) `modules/ia_logs_analysis.py:59` `def __init__(self, mode)`
- `LogFileHandler.on_modified` (method) `modules/ia_logs_analysis.py:64` `def on_modified(self, event)` -- Triggered when a log file is modified.
- `LogFileHandler.analyze_log_file` (method) `modules/ia_logs_analysis.py:75` `def analyze_log_file(self, file_path)` -- Analyzes the content of the modified log file.
- `analyze_with_deepseek` (function) `modules/ia_logs_analysis.py:94` `def analyze_with_deepseek(log_content, mode)` -- Sends log content to DeepSeek for advanced analysis.
- `start_monitoring` (function) `modules/ia_logs_analysis.py:147` `def start_monitoring(log_dir, mode)` -- Starts monitoring the specified log directory.
- `parse_args` (function) `modules/ia_logs_analysis.py:168` `def parse_args()`

## modules/ia_network_analysis.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `analyze_with_deepseek` (function) `modules/ia_network_analysis.py:39` `def analyze_with_deepseek(packet_info, mode)` -- Envía la información del paquete a DeepSeek para análisis avanzado.
- `packet_callback` (function) `modules/ia_network_analysis.py:91` `def packet_callback(packet, mode)` -- Callback para procesar cada paquete capturado.
- `start_monitoring` (function) `modules/ia_network_analysis.py:130` `def start_monitoring(interface, timeout, mode)` -- Inicia el monitoreo del tráfico de red.
- `parse_args` (function) `modules/ia_network_analysis.py:154` `def parse_args()`

## modules/icmp_client.py
- `encrypt_data` (function) `modules/icmp_client.py:18` `def encrypt_data(data, key)` -- Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- `decrypt_data` (function) `modules/icmp_client.py:34` `def decrypt_data(data, key)` -- Decrypt bytes produced by ``encrypt_data`` after authenticating them.
- `check_sudo` (function) `modules/icmp_client.py:57` `def check_sudo()`
- `checksum` (function) `modules/icmp_client.py:64` `def checksum(source_string)`
- `send_icmp_packet` (function) `modules/icmp_client.py:82` `def send_icmp_packet(dest_addr, data, key)`
- `receive_icmp_reply` (function) `modules/icmp_client.py:117` `def receive_icmp_reply(sock)`
- `main` (function) `modules/icmp_client.py:130` `def main()`

## modules/icmp_server.py
Depends on: `core/logging.py`, `modules/logging_config.py`
Imported by: `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v5.py`
- `check_sudo` (function) `modules/icmp_server.py:44` `def check_sudo()`
- `encrypt_data` (function) `modules/icmp_server.py:55` `def encrypt_data(data, key)` -- Encrypt bytes with AES-256-GCM returning ``nonce || ciphertext || tag``.
- `decrypt_data` (function) `modules/icmp_server.py:71` `def decrypt_data(data, key)` -- Decrypt bytes produced by ``encrypt_data`` after authenticating them.
- `execute_command` (function) `modules/icmp_server.py:93` `def execute_command(command)`
- `send_icmp_reply` (function) `modules/icmp_server.py:112` `def send_icmp_reply(sock, addr, data, key)`
- `checksum` (function) `modules/icmp_server.py:132` `def checksum(source_string)`
- `handle_packet` (function) `modules/icmp_server.py:150` `def handle_packet(packet, addr, key, sock)`
- `listen_for_icmp` (function) `modules/icmp_server.py:175` `def listen_for_icmp(interface, key)`
- `main` (function) `modules/icmp_server.py:202` `def main()`

## modules/img2bin.py
- `imagen_a_binario` (function) `modules/img2bin.py:7` `def imagen_a_binario(imagen_input, binario_output, block_size)`
- `main` (function) `modules/img2bin.py:43` `def main()`

## modules/integrations/misp_export.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `FindingMapper.map` (method) `modules/integrations/misp_export.py:90` `def map(self, finding)` -- Convert *finding* to a MISPAttribute.
- `IPMapper.map` (method) `modules/integrations/misp_export.py:106` `def map(self, finding)`
- `CredentialMapper.map` (method) `modules/integrations/misp_export.py:126` `def map(self, finding)`
- `CVEMapper.map` (method) `modules/integrations/misp_export.py:146` `def map(self, finding)`
- `DomainMapper.map` (method) `modules/integrations/misp_export.py:166` `def map(self, finding)`
- `HashMapper.map` (method) `modules/integrations/misp_export.py:192` `def map(self, finding)`
- `ServiceMapper.map` (method) `modules/integrations/misp_export.py:221` `def map(self, finding)`
- `MISPExporter.__init__` (method) `modules/integrations/misp_export.py:263` `def __init__(self, mappers)`
- `MISPExporter.export_session` (method) `modules/integrations/misp_export.py:268` `def export_session(self, sessions_dir, target)` -- Read policy_facts.json and events.jsonl from *sessions_dir*, map all findings, and return a populated MISPEvent.
- `MISPExporter.to_json` (method) `modules/integrations/misp_export.py:299` `def to_json(self, event)` -- Serialise *event* to a MISP-compatible JSON string.
- `MISPExporter.save` (method) `modules/integrations/misp_export.py:322` `def save(self, event, path)` -- Write the MISP event JSON to *path* and return the resolved path.
- `MISPExporter.push_to_misp` (method) `modules/integrations/misp_export.py:330` `def push_to_misp(self, event, url, api_key)` -- HTTP-push the event to a live MISP instance.
- `_DictFinding.__init__` (method) `modules/integrations/misp_export.py:454` `def __init__(self, data)`
- `get_exporter` (function) `modules/integrations/misp_export.py:469` `def get_exporter()` -- Return the module-level MISPExporter singleton.

## modules/integrations/nuclei_bridge.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `modules/integrations/nuclei_parser.py`, `modules/intelligence_engine.py`
- `TemplateSelector.select` (method) `modules/integrations/nuclei_bridge.py:91` `def select(self, services, cves)` -- Return templates relevant to the provided *services* and *cves*.
- `LocalTemplateIndex.__init__` (method) `modules/integrations/nuclei_bridge.py:114` `def __init__(self, templates_dir)`
- `LocalTemplateIndex.select` (method) `modules/integrations/nuclei_bridge.py:121` `def select(self, services, cves)`
- `LocalTemplateIndex.build` (method) `modules/integrations/nuclei_bridge.py:141` `def build(self)` -- Force a (re)build of the template index.
- `NucleiRunner.__init__` (method) `modules/integrations/nuclei_bridge.py:288` `def __init__(self)`
- `NucleiRunner.run` (method) `modules/integrations/nuclei_bridge.py:293` `def run(self, target, templates, output_dir)` -- Execute nuclei against *target* using the provided *templates*.
- `NucleiRunner.run_for_findings` (method) `modules/integrations/nuclei_bridge.py:326` `def run_for_findings(self, target, findings, output_dir, selector)` -- Convenience: extract services/CVEs from *findings*, select templates, run.
- `NucleiBridge.__init__` (method) `modules/integrations/nuclei_bridge.py:396` `def __init__(self, selector, runner)`
- `NucleiBridge.scan` (method) `modules/integrations/nuclei_bridge.py:404` `def scan(self, target, findings, dry_run)` -- Select templates from *findings* and run nuclei against *target*.
- `NucleiBridge.list_templates` (method) `modules/integrations/nuclei_bridge.py:427` `def list_templates(self, services, cves)` -- Return matching templates without running nuclei.
- `get_bridge` (function) `modules/integrations/nuclei_bridge.py:443` `def get_bridge()` -- Return the module-level NucleiBridge singleton.
- `_F.__init__` (method) `modules/integrations/nuclei_bridge.py:484` `def __init__(self, ftype, value)`

## modules/integrations/nuclei_parser.py
Depends on: `core/logging.py`, `modules/db.py`, `modules/integrations/nuclei_bridge.py`, `modules/world_model.py`
Imported by: `modules/intelligence_engine.py`, `tests/test_nuclei_parser.py`
- `NucleiFinding.mitre_tactic` (method) `modules/integrations/nuclei_parser.py:87` `def mitre_tactic(self)`
- `NucleiFinding.exploit_probability` (method) `modules/integrations/nuclei_parser.py:95` `def exploit_probability(self)`
- `NucleiParser.__init__` (method) `modules/integrations/nuclei_parser.py:109` `def __init__(self, sessions_dir)`
- `NucleiParser.parse_text` (method) `modules/integrations/nuclei_parser.py:115` `def parse_text(self, text)` -- Parse raw nuclei text output (table format).
- `NucleiParser.parse_json` (method) `modules/integrations/nuclei_parser.py:134` `def parse_json(self, json_text)` -- Parse nuclei JSON output (``-jsonl`` or ``-json`` format).
- `NucleiParser.parse_file` (method) `modules/integrations/nuclei_parser.py:177` `def parse_file(self, filepath)` -- Parse nuclei output from a file (auto-detects format).
- `NucleiParser.import_to_db` (method) `modules/integrations/nuclei_parser.py:196` `def import_to_db(self, findings, rhost, workspace_name)` -- Import parsed findings into the LazyOwnDB vulnerabilities table.
- `NucleiParser.enrich_world_model` (method) `modules/integrations/nuclei_parser.py:262` `def enrich_world_model(self, findings, rhost)` -- Feed parsed findings into the WorldModel for autonomous decision-making.
- `NucleiParser.generate_recommendations` (method) `modules/integrations/nuclei_parser.py:300` `def generate_recommendations(self, findings, rhost)` -- Generate actionable LazyOwn command recommendations from findings.
- `NucleiParser.scan_and_import` (method) `modules/integrations/nuclei_parser.py:328` `def scan_and_import(self, target, templates, services, cves, workspace_name)` -- Run nuclei scan against target, parse output, and import to DB/WorldModel.

## modules/integrations/searchsploit.py
Depends on: `core/logging.py`
Imported by: `modules/integrations/__init__.py`, `tests/test_core_modules.py`
- `ExploitSource.search_cve` (method) `modules/integrations/searchsploit.py:80` `def search_cve(self, cve_id)` -- Return exploits matching *cve_id* (e.g. 'CVE-2021-41773').
- `ExploitSource.search_service` (method) `modules/integrations/searchsploit.py:84` `def search_service(self, name, version)` -- Return exploits matching the service *name* and optional *version*.
- `SearchsploitCLI.__init__` (method) `modules/integrations/searchsploit.py:102` `def __init__(self)`
- `SearchsploitCLI.search_cve` (method) `modules/integrations/searchsploit.py:109` `def search_cve(self, cve_id)`
- `SearchsploitCLI.search_service` (method) `modules/integrations/searchsploit.py:112` `def search_service(self, name, version)`
- `ExploitDBAPI.__init__` (method) `modules/integrations/searchsploit.py:201` `def __init__(self)`
- `ExploitDBAPI.search_cve` (method) `modules/integrations/searchsploit.py:207` `def search_cve(self, cve_id)`
- `ExploitDBAPI.search_service` (method) `modules/integrations/searchsploit.py:210` `def search_service(self, name, version)`
- `SearchsploitClient.__init__` (method) `modules/integrations/searchsploit.py:278` `def __init__(self, primary, fallback)`
- `SearchsploitClient.search_cve` (method) `modules/integrations/searchsploit.py:286` `def search_cve(self, cve_id)` -- Return exploits for *cve_id*, trying CLI then API.
- `SearchsploitClient.search_service` (method) `modules/integrations/searchsploit.py:293` `def search_service(self, name, version)` -- Return exploits for *name*/*version*, trying CLI then API.
- `SearchsploitClient.enrich_findings` (method) `modules/integrations/searchsploit.py:300` `def enrich_findings(self, findings)` -- Takes an ObsParser Finding list, extracts CVEs and service_versions, returns ``{cve_or_service: [ExploitEntry, ...]}``.
- `get_client` (function) `modules/integrations/searchsploit.py:333` `def get_client()` -- Return the module-level SearchsploitClient singleton.
- `search_cve` (function) `modules/integrations/searchsploit.py:341` `def search_cve(cve_id)` -- Module-level convenience: search by CVE id.
- `search_service` (function) `modules/integrations/searchsploit.py:346` `def search_service(name, version)` -- Module-level convenience: search by service name and version.

## modules/intel_fusion.py
Depends on: `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`
Imported by: `lazyc2.py`, `modules/atomic_exploit_bridge.py`, `modules/attack_surface3d.py`, `tests/test_asset_gate.py`, `tests/test_attack_surface3d.py`, `tests/test_intel_fusion.py`
- `node_id` (function) `modules/intel_fusion.py:106` `def node_id(kind, value)` -- Deterministic node id from kind + normalized value.
- `build_intel_graph` (function) `modules/intel_fusion.py:176` `def build_intel_graph(sessions_dir, est_cap)` -- Fuse all session artefacts into one C2-centred intel graph.
- `add_node` (function) `modules/intel_fusion.py:183` `def add_node(kind, value, label)` -- Insert node or merge extra fields into the existing one.
- `add_edge` (function) `modules/intel_fusion.py:197` `def add_edge(src, dst, kind, evidence, weight)` -- Append one provenance-tagged relation.
- `tag_source` (function) `modules/intel_fusion.py:205` `def tag_source(nid, source)` -- Record a corroborating artefact on a node, deduped.
- `group_colors` (function) `modules/intel_fusion.py:512` `def group_colors(graph)` -- Stable colors for layer/language groupings (ReadMenator contract).
- `page_settings` (function) `modules/intel_fusion.py:528` `def page_settings(graph)` -- Explorer page settings with ReadMenator physics sizes (exact values).
- `build_analytics` (function) `modules/intel_fusion.py:585` `def build_analytics(graph, summary)` -- Side-panel analytics (attribution funnel + intel summary).
- `build_bundle_payload` (function) `modules/intel_fusion.py:659` `def build_bundle_payload(graph)` -- Derive the circular/spherical bundle payload from a fused graph.
- `bundle_settings` (function) `modules/intel_fusion.py:769` `def bundle_settings(graph)` -- Bundle page settings with ReadMenator sizes (exact values).
- `assign_layout` (function) `modules/intel_fusion.py:800` `def assign_layout(graph, mode)` -- Attach x/y/z for radial/spherical modes; force modes stay free.
- `write_summary` (function) `modules/intel_fusion.py:865` `def write_summary(graph, sessions_dir)` -- Score host exposure and suggest intents for the autonomous planner.

## modules/intelligence_engine.py
Depends on: `core/logging.py`, `modules/estorides_importer.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/obs_parser.py`, `modules/world_model.py`, `modules/yara_scanner.py`
Imported by: `cli/commands/mcp_bridge.py`, `cli/commands/recon.py`, `skills/lazyown_mcp.py`, `tests/test_intelligence_engine.py`
- `IntelligenceEngine.__init__` (method) `modules/intelligence_engine.py:142` `def __init__(self, config)`
- `IntelligenceEngine.collect_from_scan` (method) `modules/intelligence_engine.py:153` `def collect_from_scan(self, target)` -- Parse nmap XML into structured facts.
- `IntelligenceEngine.collect_from_tool` (method) `modules/intelligence_engine.py:255` `def collect_from_tool(self, output, tool, host)` -- Parse tool output into structured facts using ObsParser.
- `IntelligenceEngine.collect_from_estorides` (method) `modules/intelligence_engine.py:292` `def collect_from_estorides(self, target)` -- Run estorides OSINT aggregator and collect findings.
- `IntelligenceEngine.collect_from_nuclei` (method) `modules/intelligence_engine.py:334` `def collect_from_nuclei(self, target)` -- Run nuclei vulnerability scanner and collect findings.
- `IntelligenceEngine.collect_from_yara` (method) `modules/intelligence_engine.py:376` `def collect_from_yara(self, target_path)` -- Scan with YARA rules and collect IOC matches.
- `IntelligenceEngine.collect_from_factstore` (method) `modules/intelligence_engine.py:415` `def collect_from_factstore(self)` -- Ingest structured facts from FactStore policy_facts.json.
- `IntelligenceEngine.analyze` (method) `modules/intelligence_engine.py:477` `def analyze(self)` -- Correlate collected facts into structured intelligence.
- `IntelligenceEngine.produce_intelligence` (method) `modules/intelligence_engine.py:685` `def produce_intelligence(self)` -- Grade and enrich intelligence assessments with MITRE mappings.
- `IntelligenceEngine.produce_counter_intelligence` (method) `modules/intelligence_engine.py:715` `def produce_counter_intelligence(self)` -- Assess what we exposed and what can detect us.
- `IntelligenceEngine.disseminate` (method) `modules/intelligence_engine.py:765` `def disseminate(self)` -- Write intelligence to WorldModel, killchain, and report file.
- `IntelligenceEngine.run_full_cycle` (method) `modules/intelligence_engine.py:845` `def run_full_cycle(self, target)` -- Execute the complete intelligence cycle for a target.
- `IntelligenceEngine.get_intel_report` (method) `modules/intelligence_engine.py:874` `def get_intel_report(self)` -- Produce a structured JSON intelligence report.
- `get_intelligence_engine` (function) `modules/intelligence_engine.py:931` `def get_intelligence_engine(config)` -- Return the module-level singleton IntelligenceEngine.


Next: [API_p12.md](API_p12.md)
