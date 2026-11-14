# Symbols (page 24 of 52)
Previous: [SYMBOLS_p23.md](SYMBOLS_p23.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_call_ai` | function | `modules/timeline_narrator.py:97` | `def _call_ai(api_key, events_text, target)` |
| `_format_events_for_prompt` | function | `modules/timeline_narrator.py:77` | `def _format_events_for_prompt(events)` |
| `_load_events` | function | `modules/timeline_narrator.py:57` | `def _load_events(n)` |
| `_write_timeline` | function | `modules/timeline_narrator.py:115` | `def _write_timeline(narrative, event_count, target)` |
| `load_timeline` | function | `modules/timeline_narrator.py:165` | `def load_timeline()` |
| `narrate` | function | `modules/timeline_narrator.py:130` | `def narrate(api_key, force)` |
| `FileTimestamps` | class | `modules/timestomper.py:51` | `class FileTimestamps` |
| `TimestompConfig` | class | `modules/timestomper.py:24` | `class TimestompConfig` |
| `Timestomper` | class | `modules/timestomper.py:69` | `class Timestomper` |
| `__init__` | method | `modules/timestomper.py:106` | `def __init__(self, config)` |
| `_pick_reference` | method | `modules/timestomper.py:269` | `def _pick_reference(self, path, platform)` |
| `generate_random_timestamps` | method | `modules/timestomper.py:280` | `def generate_random_timestamps(self, reference_ts, window_days)` |
| `linux_timestomp_commands` | method | `modules/timestomper.py:200` | `def linux_timestomp_commands(self)` |
| `macos_timestomp_commands` | method | `modules/timestomper.py:241` | `def macos_timestomp_commands(self)` |
| `summary` | method | `modules/timestomper.py:326` | `def summary(self)` |
| `verify_timestamps` | method | `modules/timestomper.py:300` | `def verify_timestamps(self, target_paths)` |
| `windows_timestomp_c` | method | `modules/timestomper.py:152` | `def windows_timestomp_c(self)` |
| `windows_timestomp_powershell` | method | `modules/timestomper.py:110` | `def windows_timestomp_powershell(self)` |
| `FakeEngine` | class | `modules/tools/loop_smoke.py:31` | `class FakeEngine` |
| `FakeShell` | class | `modules/tools/loop_smoke.py:22` | `class FakeShell` |
| `__init__` | method | `modules/tools/loop_smoke.py:36` | `def __init__(self)` |
| `bind_shell` | method | `modules/tools/loop_smoke.py:44` | `def bind_shell(self, shell)` |
| `create_task` | method | `modules/tools/loop_smoke.py:52` | `def create_task(self, goal, description)` |
| `main` | function | `modules/tools/loop_smoke.py:116` | `def main()` |
| `onecmd_plus_hooks` | method | `modules/tools/loop_smoke.py:25` | `def onecmd_plus_hooks(self, command)` |
| `orchestrate` | method | `modules/tools/loop_smoke.py:56` | `def orchestrate(self)` |
| `run` | function | `modules/tools/loop_smoke.py:77` | `def run()` |
| `set_concurrency` | method | `modules/tools/loop_smoke.py:48` | `def set_concurrency(self, value)` |
| `_drive` | function | `modules/tools/monitor_smoke.py:40` | `def _drive()` |
| `main` | function | `modules/tools/monitor_smoke.py:59` | `def main()` |
| `run` | function | `modules/tools/monitor_smoke.py:20` | `def run()` |
| `ToolSeed` | class | `modules/toolset.py:27` | `class ToolSeed` |
| `builtin_seeds` | function | `modules/toolset.py:35` | `def builtin_seeds()` |
| `extract_tool` | function | `modules/toolset.py:105` | `def extract_tool(command)` |
| `resolve` | function | `modules/toolset.py:72` | `def resolve(agent, tool_key)` |
| `validate_shell` | function | `modules/toolset.py:128` | `def validate_shell(role, command)` |
| `OnlineFeedbackLoop` | class | `modules/toposwarm_bridge.py:273` | `class OnlineFeedbackLoop` |
| `RoutedCall` | class | `modules/toposwarm_bridge.py:71` | `class RoutedCall` |
| `TopoSwarmBridge` | class | `modules/toposwarm_bridge.py:424` | `class TopoSwarmBridge` |
| `__init__` | method | `modules/toposwarm_bridge.py:296` | `def __init__(self, maxsize)` |
| `__init__` | method | `modules/toposwarm_bridge.py:432` | `def __init__(self)` |
| `_hook` | function | `modules/toposwarm_bridge.py:508` | `def _hook(m, i, o)` |
| `_keyword_route` | function | `modules/toposwarm_bridge.py:202` | `def _keyword_route(prompt)` |
| `_load_toposwarm_modules` | function | `modules/toposwarm_bridge.py:241` | `def _load_toposwarm_modules()` |
| `_neural_route` | method | `modules/toposwarm_bridge.py:493` | `def _neural_route(self, prompt)` |
| `_try_load` | method | `modules/toposwarm_bridge.py:452` | `def _try_load(self)` |
| `available` | method | `modules/toposwarm_bridge.py:444` | `def available(self)` |
| `execute_via_orchestrator` | method | `modules/toposwarm_bridge.py:613` | `def execute_via_orchestrator(self, prompt, no_model)` |
| `feedback` | method | `modules/toposwarm_bridge.py:318` | `def feedback(self, result_id, good, comment, routing_head)` |
| `feedback` | method | `modules/toposwarm_bridge.py:562` | `def feedback(self, result_id, good, comment)` |
| `get_bridge` | function | `modules/toposwarm_bridge.py:645` | `def get_bridge()` |
| `lazyown_command` | method | `modules/toposwarm_bridge.py:81` | `def lazyown_command(self)` |
| `load_feedback_for_training` | method | `modules/toposwarm_bridge.py:389` | `def load_feedback_for_training(self)` |
| `model_loaded` | method | `modules/toposwarm_bridge.py:449` | `def model_loaded(self)` |
| `pending_count` | method | `modules/toposwarm_bridge.py:379` | `def pending_count(self)` |
| `register` | method | `modules/toposwarm_bridge.py:303` | `def register(self, result, hidden)` |
| `route` | method | `modules/toposwarm_bridge.py:586` | `def route(self, prompt)` |
| `stats` | method | `modules/toposwarm_bridge.py:382` | `def stats(self)` |
| `TrafficMorpher` | class | `modules/traffic_morpher.py:18` | `class TrafficMorpher` |
| `__init__` | method | `modules/traffic_morpher.py:77` | `def __init__(self)` |
| `generate_beacon_profile` | method | `modules/traffic_morpher.py:270` | `def generate_beacon_profile(self, name, protocol, jitter_pct, user_agent)` |
| `generate_cloudflare_worker_proxy_config` | method | `modules/traffic_morpher.py:205` | `def generate_cloudflare_worker_proxy_config(self, c2_host, c2_port, auth_token)` |
| `generate_dns_tunnel_payload` | method | `modules/traffic_morpher.py:138` | `def generate_dns_tunnel_payload(self, data, domain)` |
| `generate_icmp_exfil_payload` | method | `modules/traffic_morpher.py:164` | `def generate_icmp_exfil_payload(self, data, chunk_size)` |
| `generate_jitter` | method | `modules/traffic_morpher.py:125` | `def generate_jitter(self, base_delay, jitter_pct)` |
| `generate_traffic_padding` | method | `modules/traffic_morpher.py:108` | `def generate_traffic_padding(self, min_bytes, max_bytes)` |
| `generate_websocket_masking` | method | `modules/traffic_morpher.py:190` | `def generate_websocket_masking(self, data)` |
| `get_cdn_fronting_hosts` | method | `modules/traffic_morpher.py:91` | `def get_cdn_fronting_hosts(self, provider, count)` |
| `get_random_http_headers` | method | `modules/traffic_morpher.py:81` | `def get_random_http_headers(self)` |
| `Exchange` | class | `modules/traffic_recorder.py:83` | `class Exchange` |
| `RecorderConfig` | class | `modules/traffic_recorder.py:24` | `class RecorderConfig` |
| `TrafficRecorder` | class | `modules/traffic_recorder.py:94` | `class TrafficRecorder` |
| `__init__` | method | `modules/traffic_recorder.py:97` | `def __init__(self, base_dir)` |
| `_connect` | method | `modules/traffic_recorder.py:135` | `def _connect(self)` |
| `_fts_query` | method | `modules/traffic_recorder.py:384` | `def _fts_query(query)` |
| `_index_fts` | method | `modules/traffic_recorder.py:332` | `def _index_fts(self, exchange_id, req, resp)` |
| `_migrate_fts` | method | `modules/traffic_recorder.py:118` | `def _migrate_fts(self, conn)` |
| `_scan_bodies` | method | `modules/traffic_recorder.py:431` | `def _scan_bodies(self, needle, limit)` |
| `backfill_fts` | method | `modules/traffic_recorder.py:352` | `def backfill_fts(self, batch)` |
| `count` | method | `modules/traffic_recorder.py:326` | `def count(self)` |
| `export_archive` | method | `modules/traffic_recorder.py:460` | `def export_archive(self, path, limit, task)` |
| `gc` | method | `modules/traffic_recorder.py:596` | `def gc(self, older_than_sec, max_rows)` |
| `get_body` | method | `modules/traffic_recorder.py:284` | `def get_body(self, exchange_id)` |
| `import_archive` | method | `modules/traffic_recorder.py:502` | `def import_archive(self, path)` |
| `import_inbox` | method | `modules/traffic_recorder.py:563` | `def import_inbox(self, inbox_dir)` |
| `latest_rowid` | method | `modules/traffic_recorder.py:256` | `def latest_rowid(self)` |
| `query` | method | `modules/traffic_recorder.py:262` | `def query(self, host, status, limit, offset, task)` |
| `read_body` | method | `modules/traffic_recorder.py:293` | `def read_body(self, exchange_id, part, offset, length)` |
| `record` | method | `modules/traffic_recorder.py:147` | `def record(self, method, url, status, req_body, resp_body, content_type, req_headers, resp_headers, host, port...` |
| `search_body` | method | `modules/traffic_recorder.py:391` | `def search_body(self, query, limit)` |
| `since` | method | `modules/traffic_recorder.py:239` | `def since(self, rowid, limit)` |
| `url_template` | function | `modules/traffic_recorder.py:72` | `def url_template(url)` |
| `TriggerPolicyConfig` | class | `modules/trigger_policy.py:31` | `class TriggerPolicyConfig` |
| `_coerce_every_sec` | function | `modules/trigger_policy.py:79` | `def _coerce_every_sec(value)` |
| `export_store` | function | `modules/trigger_policy.py:171` | `def export_store(task_id)` |
| `read_policy` | function | `modules/trigger_policy.py:120` | `def read_policy(path)` |
| `remove_seed` | function | `modules/trigger_policy.py:185` | `def remove_seed(kind, arg, task_id)` |
| `seed_store` | function | `modules/trigger_policy.py:146` | `def seed_store(policy, store, task_id)` |
| `seeds` | function | `modules/trigger_policy.py:87` | `def seeds(raw)` |
| `validate_triggers` | function | `modules/trigger_policy.py:40` | `def validate_triggers(raw)` |
| `TTPCoverage` | class | `modules/ttp_coverage.py:65` | `class TTPCoverage` |
| `TTPRow` | class | `modules/ttp_coverage.py:55` | `class TTPRow` |
| `__init__` | method | `modules/ttp_coverage.py:68` | `def __init__(self)` |
| `_blocking_facts` | method | `modules/ttp_coverage.py:168` | `def _blocking_facts(self, tactic)` |
| `_load_state` | method | `modules/ttp_coverage.py:248` | `def _load_state(self)` |
| `_save_state` | method | `modules/ttp_coverage.py:241` | `def _save_state(self)` |
| `add` | method | `modules/ttp_coverage.py:125` | `def add(self, technique_id, name, tactic, status, operation_id)` |
| `compute_ready` | method | `modules/ttp_coverage.py:149` | `def compute_ready(self, available_facts)` |
| `get_coverage` | function | `modules/ttp_coverage.py:260` | `def get_coverage()` |
| `matrix` | method | `modules/ttp_coverage.py:190` | `def matrix(self)` |
| `rebuild_from_operations` | method | `modules/ttp_coverage.py:76` | `def rebuild_from_operations(self)` |
| `status_by_id` | method | `modules/ttp_coverage.py:231` | `def status_by_id(self, technique_id)` |
| `to_dict` | method | `modules/ttp_coverage.py:234` | `def to_dict(self)` |
| `_as_list` | function | `modules/ttpscope_bridge.py:460` | `def _as_list(value)` |
| `_cache_dataset_path` | function | `modules/ttpscope_bridge.py:146` | `def _cache_dataset_path()` |
| `_fallback_matrix_bundle` | function | `modules/ttpscope_bridge.py:384` | `def _fallback_matrix_bundle(platform)` |
| `_fallback_matrix_parquet` | function | `modules/ttpscope_bridge.py:453` | `def _fallback_matrix_parquet(platform)` |
| `_fallback_note` | function | `modules/ttpscope_bridge.py:422` | `def _fallback_note(object_id, text)` |
| `_fallback_notes` | function | `modules/ttpscope_bridge.py:442` | `def _fallback_notes(object_id)` |
| `_fallback_search_bundle` | function | `modules/ttpscope_bridge.py:235` | `def _fallback_search_bundle(query, limit)` |
| `_fallback_search_parquet` | function | `modules/ttpscope_bridge.py:282` | `def _fallback_search_parquet(query, limit)` |
| `_fallback_show_bundle` | function | `modules/ttpscope_bridge.py:303` | `def _fallback_show_bundle(object_id)` |
| `_fallback_show_parquet` | function | `modules/ttpscope_bridge.py:350` | `def _fallback_show_parquet(object_id)` |
| `_fallback_sync` | function | `modules/ttpscope_bridge.py:153` | `def _fallback_sync()` |
| `_load_atomic_parquet` | function | `modules/ttpscope_bridge.py:273` | `def _load_atomic_parquet()` |
| `_load_parquet` | function | `modules/ttpscope_bridge.py:259` | `def _load_parquet(name)` |
| `_load_stix_bundle` | function | `modules/ttpscope_bridge.py:193` | `def _load_stix_bundle()` |
| `_notes_dir` | function | `modules/ttpscope_bridge.py:415` | `def _notes_dir()` |
| `_run_ttpscope` | function | `modules/ttpscope_bridge.py:129` | `def _run_ttpscope(args)` |
| `_slug` | function | `modules/ttpscope_bridge.py:123` | `def _slug(text)` |
| `_stage` | function | `modules/ttpscope_bridge.py:485` | `def _stage(action, slug, stdout, extra)` |
| `_stix_external_id` | function | `modules/ttpscope_bridge.py:211` | `def _stix_external_id(obj)` |
| `_stix_index` | function | `modules/ttpscope_bridge.py:219` | `def _stix_index(bundle)` |
| `do_chain` | function | `modules/ttpscope_bridge.py:582` | `def do_chain(object_id, platform, limit)` |
| `do_matrix` | function | `modules/ttpscope_bridge.py:535` | `def do_matrix(platform)` |
| `do_note` | function | `modules/ttpscope_bridge.py:551` | `def do_note(object_id, text)` |
| `do_notes` | function | `modules/ttpscope_bridge.py:570` | `def do_notes(object_id)` |
| `do_search` | function | `modules/ttpscope_bridge.py:508` | `def do_search(query)` |
| `do_show` | function | `modules/ttpscope_bridge.py:520` | `def do_show(object_id)` |
| `do_sync` | function | `modules/ttpscope_bridge.py:497` | `def do_sync()` |
| `locate_binary` | function | `modules/ttpscope_bridge.py:82` | `def locate_binary()` |
| `main` | function | `modules/ttpscope_bridge.py:679` | `def main()` |
| `run_action` | function | `modules/ttpscope_bridge.py:652` | `def run_action(action)` |
| `validate_object_id` | function | `modules/ttpscope_bridge.py:92` | `def validate_object_id(raw)` |
| `validate_platform` | function | `modules/ttpscope_bridge.py:112` | `def validate_platform(raw)` |
| `validate_query` | function | `modules/ttpscope_bridge.py:100` | `def validate_query(raw)` |
| `DelegateResult` | class | `modules/unified_bridge.py:59` | `class DelegateResult` |
| `KeywordBackend` | class | `modules/unified_bridge.py:75` | `class KeywordBackend(RouteBackend)` |
| `LazyownBridgeBackend` | class | `modules/unified_bridge.py:123` | `class LazyownBridgeBackend(RouteBackend)` |
| `RouteBackend` | class | `modules/unified_bridge.py:67` | `class RouteBackend(ABC)` |
| `RouteResult` | class | `modules/unified_bridge.py:46` | `class RouteResult` |
| `TopoSwarmBackend` | class | `modules/unified_bridge.py:161` | `class TopoSwarmBackend(RouteBackend)` |
| `UnifiedBridge` | class | `modules/unified_bridge.py:195` | `class UnifiedBridge` |
| `__init__` | method | `modules/unified_bridge.py:214` | `def __init__(self)` |
| `_await_agent` | method | `modules/unified_bridge.py:355` | `def _await_agent(self, get_status, agent_id, timeout)` |
| `_detect_phase` | method | `modules/unified_bridge.py:464` | `def _detect_phase(self)` |
| `_get_active_target` | method | `modules/unified_bridge.py:473` | `def _get_active_target(self)` |
| `_init_backends` | method | `modules/unified_bridge.py:219` | `def _init_backends(self)` |
| `_publish` | method | `modules/unified_bridge.py:233` | `def _publish(self, category, event_type, payload)` |
| `_run_agent_command` | method | `modules/unified_bridge.py:384` | `def _run_agent_command(self, command)` |
| `available` | method | `modules/unified_bridge.py:69` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:102` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:126` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:164` | `def available(self)` |
| `delegate` | method | `modules/unified_bridge.py:300` | `def delegate(self, goal, backend, timeout, max_iterations)` |
| `delegate_task` | function | `modules/unified_bridge.py:488` | `def delegate_task(goal, backend)` |
| `get` | method | `modules/unified_bridge.py:225` | `def get(cls)` |
| `list_backends` | method | `modules/unified_bridge.py:461` | `def list_backends(self)` |
| `route` | method | `modules/unified_bridge.py:72` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:105` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:134` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:173` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:253` | `def route(self, prompt, context)` |
| `route_prompt` | function | `modules/unified_bridge.py:483` | `def route_prompt(prompt, context)` |
| `set_publish_callback` | method | `modules/unified_bridge.py:230` | `def set_publish_callback(self, cb)` |
| `UnifiedDashboard` | class | `modules/unified_dashboard.py:37` | `class UnifiedDashboard` |
| `__init__` | method | `modules/unified_dashboard.py:44` | `def __init__(self, sessions_dir)` |
| `_collect_daemon_status` | method | `modules/unified_dashboard.py:121` | `def _collect_daemon_status(self)` |
| `_collect_dashboard` | method | `modules/unified_dashboard.py:160` | `def _collect_dashboard(self)` |
| `_collect_graph_advice` | method | `modules/unified_dashboard.py:142` | `def _collect_graph_advice(self)` |
| `_collect_hive_status` | method | `modules/unified_dashboard.py:101` | `def _collect_hive_status(self)` |
| `_collect_live_graph` | method | `modules/unified_dashboard.py:130` | `def _collect_live_graph(self)` |
| `_collect_policy_status` | method | `modules/unified_dashboard.py:111` | `def _collect_policy_status(self)` |
| `_collect_world_model` | method | `modules/unified_dashboard.py:95` | `def _collect_world_model(self)` |
| `_get_dashboard` | method | `modules/unified_dashboard.py:49` | `def _get_dashboard(self)` |
| `_get_graph` | method | `modules/unified_dashboard.py:65` | `def _get_graph(self)` |
| `build_unified_snapshot` | method | `modules/unified_dashboard.py:76` | `def build_unified_snapshot(self)` |
| `export_json` | method | `modules/unified_dashboard.py:251` | `def export_json(self)` |
| `get_unified_dashboard` | function | `modules/unified_dashboard.py:256` | `def get_unified_dashboard(sessions_dir)` |
| `render_unified` | method | `modules/unified_dashboard.py:170` | `def render_unified(self)` |
| `GatekeeperStatus` | function | `modules/venator.py:651` | `def GatekeeperStatus(output_file)` |
| `SIPStatus` | function | `modules/venator.py:637` | `def SIPStatus(output_file)` |
| `amzn_canonical_req` | function | `modules/venator.py:856` | `def amzn_canonical_req(filename_path, headers_list)` |
| `amzn_sig` | function | `modules/venator.py:846` | `def amzn_sig(secret_access_key, data, aws_region, aws_service)` |
| `checkSignature` | function | `modules/venator.py:132` | `def checkSignature(file, bundle)` |
| `datetime_handler` | function | `modules/venator.py:210` | `def datetime_handler(x)` |
| `getApps` | function | `modules/venator.py:741` | `def getApps(path, output_file, ignoreVFlag)` |
| `getBashHistory` | function | `modules/venator.py:786` | `def getBashHistory(output_file, users)` |
| `getChromeDownloads` | function | `modules/venator.py:388` | `def getChromeDownloads(chromeHistoryDbPath, output_file)` |
| `getChromeExtensions` | function | `modules/venator.py:357` | `def getChromeExtensions(path, output_file)` |
| `getConnections` | function | `modules/venator.py:609` | `def getConnections(output_file)` |
| `getCronJobs` | function | `modules/venator.py:494` | `def getCronJobs(users, output_file)` |
| `getEmond` | function | `modules/venator.py:513` | `def getEmond(output_file)` |
| `getEnv` | function | `modules/venator.py:577` | `def getEnv(output_file)` |
| `getEventTaps` | function | `modules/venator.py:763` | `def getEventTaps(output_file)` |
| `getFirefoxExtensions` | function | `modules/venator.py:442` | `def getFirefoxExtensions(path, output_file)` |
| `getHash` | function | `modules/venator.py:112` | `def getHash(file, ignoreVFlag)` |
| `getInstallHistory` | function | `modules/venator.py:477` | `def getInstallHistory(output_file)` |
| `getKext` | function | `modules/venator.py:530` | `def getKext(sipStatus, kextPath, output_file, ignoreVFlag)` |
| `getLaunchAgents` | function | `modules/venator.py:287` | `def getLaunchAgents(path, output_file, ignoreVFlag)` |
| `getLaunchDaemons` | function | `modules/venator.py:302` | `def getLaunchDaemons(path, output_file, ignoreVFlag)` |
| `getLoginItems` | function | `modules/venator.py:706` | `def getLoginItems(path, output_file, ignoreVFlag)` |
| `getPeriodicScripts` | function | `modules/venator.py:592` | `def getPeriodicScripts(output_file)` |
| `getSafariExtensions` | function | `modules/venator.py:338` | `def getSafariExtensions(path, output_file)` |
| `getShellStartupScripts` | function | `modules/venator.py:804` | `def getShellStartupScripts(users, output_file)` |
| `getSystemInfo` | function | `modules/venator.py:66` | `def getSystemInfo(output_file)` |
| `getUUID` | function | `modules/venator.py:38` | `def getUUID()` |
| `getUsers` | function | `modules/venator.py:317` | `def getUsers(output_file)` |
| `getVTResult` | function | `modules/venator.py:83` | `def getVTResult(fileHash)` |
| `hmac_sha256` | function | `modules/venator.py:842` | `def hmac_sha256(key, data)` |
| `io_key` | function | `modules/venator.py:49` | `def io_key(keyname)` |
| `parseAgentsDaemons` | function | `modules/venator.py:215` | `def parseAgentsDaemons(item, path)` |
| `parseApp` | function | `modules/venator.py:663` | `def parseApp(app, ignoreVFlag)` |
| `s3_upload` | function | `modules/venator.py:866` | `def s3_upload(data, content_type, filename_path, access_key_id, secret_access_key, s3_bucket, aws_region)` |
| `VerbCatalogConfig` | class | `modules/verb_catalog.py:77` | `class VerbCatalogConfig` |
| `_addon_discoveries` | function | `modules/verb_catalog.py:171` | `def _addon_discoveries(config)` |
| `_all_discoveries` | function | `modules/verb_catalog.py:242` | `def _all_discoveries(config)` |
| `_builtin_names` | function | `modules/verb_catalog.py:111` | `def _builtin_names()` |
| `_default_config` | function | `modules/verb_catalog.py:101` | `def _default_config()` |
| `_drop_cache` | function | `modules/verb_catalog.py:571` | `def _drop_cache(path_key)` |
| `_phase_fallback` | function | `modules/verb_catalog.py:123` | `def _phase_fallback(verb)` |
| `_phases_for` | function | `modules/verb_catalog.py:133` | `def _phases_for(stored, phase)` |
| `_poc_discoveries` | function | `modules/verb_catalog.py:215` | `def _poc_discoveries(config)` |
| `_risk_fallback` | function | `modules/verb_catalog.py:161` | `def _risk_fallback(verb)` |
| `_write` | function | `modules/verb_catalog.py:547` | `def _write(cfg, verbs)` |
| `catalog_enabled` | function | `modules/verb_catalog.py:420` | `def catalog_enabled(name, config)` |
| `catalog_source` | function | `modules/verb_catalog.py:435` | `def catalog_source(name, config)` |
| `entries` | function | `modules/verb_catalog.py:364` | `def entries(config)` |
| `index_commands` | function | `modules/verb_catalog.py:254` | `def index_commands(config)` |
| `load` | function | `modules/verb_catalog.py:331` | `def load(config)` |
| `search` | function | `modules/verb_catalog.py:593` | `def search(query, config, phase, enabled, limit)` |
| `set_enabled` | function | `modules/verb_catalog.py:449` | `def set_enabled(name, enabled, config)` |
| `stats` | function | `modules/verb_catalog.py:579` | `def stats(config)` |
| `sync` | function | `modules/verb_catalog.py:487` | `def sync(config)` |
| `validate_catalog` | function | `modules/verb_catalog.py:294` | `def validate_catalog(data)` |
| `FactPredicate` | class | `modules/verb_manifest.py:123` | `class FactPredicate` |
| `ManifestCost` | class | `modules/verb_manifest.py:93` | `class ManifestCost` |
| `ManifestNoise` | class | `modules/verb_manifest.py:108` | `class ManifestNoise` |
| `VerbManifest` | class | `modules/verb_manifest.py:188` | `class VerbManifest` |
| `_load_document` | function | `modules/verb_manifest.py:338` | `def _load_document(path)` |
| `_parse_cost` | function | `modules/verb_manifest.py:254` | `def _parse_cost(data)` |
| `_parse_noise` | function | `modules/verb_manifest.py:276` | `def _parse_noise(data)` |
| `args` | method | `modules/verb_manifest.py:152` | `def args(self)` |
| `coverage` | function | `modules/verb_manifest.py:522` | `def coverage(total_verbs, path)` |
| `facts_for_target` | function | `modules/verb_manifest.py:411` | `def facts_for_target(host)` |
| `is_wild` | method | `modules/verb_manifest.py:156` | `def is_wild(self, key)` |
| `manifest_for` | function | `modules/verb_manifest.py:396` | `def manifest_for(verb, path)` |
| `manifests` | function | `modules/verb_manifest.py:371` | `def manifests(path)` |
| `matches` | method | `modules/verb_manifest.py:161` | `def matches(self, other)` |
| `parse_manifest` | function | `modules/verb_manifest.py:296` | `def parse_manifest(verb, data)` |
| `parse_predicate` | function | `modules/verb_manifest.py:222` | `def parse_predicate(data)` |
| `plan_check` | function | `modules/verb_manifest.py:467` | `def plan_check(steps, tokens, path, facts)` |
| `main` | function | `modules/vuln_bot_cli.py:22` | `def main()` |
| `parse_args` | function | `modules/vuln_bot_cli.py:10` | `def parse_args()` |
| `VulnBotCLI` | class | `modules/vulnbot.py:37` | `class VulnBotCLI` |
| `__init__` | method | `modules/vulnbot.py:38` | `def __init__(self, provider, mode, debug, script_path)` |
| `_complete_with_fallback` | method | `modules/vulnbot.py:69` | `def _complete_with_fallback(self, prompt)` |
| `_load_external_tools` | method | `modules/vulnbot.py:172` | `def _load_external_tools(self, script_path)` |
| `_load_model` | method | `modules/vulnbot.py:54` | `def _load_model(self)` |
| `_register_file_tools` | method | `modules/vulnbot.py:146` | `def _register_file_tools(self)` |
| `_setup_agent` | method | `modules/vulnbot.py:124` | `def _setup_agent(self, script_path)` |
| `_stream_agent_response` | method | `modules/vulnbot.py:199` | `def _stream_agent_response(self, prompt)` |
| `_stream_with_fallback` | method | `modules/vulnbot.py:92` | `def _stream_with_fallback(self, prompt)` |
| `add_to_knowledge_base` | method | `modules/vulnbot.py:303` | `def add_to_knowledge_base(self, prompt, response)` |
| `create_complex_prompt` | method | `modules/vulnbot.py:251` | `def create_complex_prompt(self, base_prompt, history, knowledge)` |
| `edit_file` | function | `modules/vulnbot.py:158` | `def edit_file(path, content, old_text)` |
| `generate` | function | `modules/vulnbot.py:202` | `def generate()` |
| `generate` | function | `modules/vulnbot.py:298` | `def generate()` |
| `get_relevant_knowledge` | method | `modules/vulnbot.py:228` | `def get_relevant_knowledge(self, prompt)` |
| `list_files` | function | `modules/vulnbot.py:149` | `def list_files(directory)` |
| `load_event_config` | method | `modules/vulnbot.py:273` | `def load_event_config(self)` |
| `load_knowledge_base` | method | `modules/vulnbot.py:208` | `def load_knowledge_base(self)` |
| `process_with_context` | method | `modules/vulnbot.py:281` | `def process_with_context(self, file_path, event)` |
| `read_file` | function | `modules/vulnbot.py:153` | `def read_file(path)` |
| `read_file_content` | method | `modules/vulnbot.py:267` | `def read_file_content(self, file_path)` |
| `save_knowledge_base` | method | `modules/vulnbot.py:224` | `def save_knowledge_base(self, kb)` |
| `stream_response` | method | `modules/vulnbot.py:297` | `def stream_response(self, prompt)` |
| `WebSocketBeacon` | class | `modules/websocket_beacon.py:46` | `class WebSocketBeacon` |
| `WebSocketC2Handler` | class | `modules/websocket_beacon.py:274` | `class WebSocketC2Handler` |
| `__init__` | method | `modules/websocket_beacon.py:62` | `def __init__(self, server_url, beacon_id, encryption_key, sleep_seconds, jitter_percent, ssl_verify, proxy)` |
| `__init__` | method | `modules/websocket_beacon.py:288` | `def __init__(self, host, port, ssl_context, beacon_callback, task_callback, result_callback)` |
| `_build_message` | method | `modules/websocket_beacon.py:103` | `def _build_message(self, msg_type, payload)` |
| `_decrypt` | method | `modules/websocket_beacon.py:97` | `def _decrypt(self, data)` |
| `_encrypt` | method | `modules/websocket_beacon.py:91` | `def _encrypt(self, data)` |
| `_handle_connection` | method | `modules/websocket_beacon.py:310` | `def _handle_connection(self, websocket, path)` |
| `_jittered_sleep` | method | `modules/websocket_beacon.py:114` | `def _jittered_sleep(self)` |
| `_run_loop` | method | `modules/websocket_beacon.py:410` | `def _run_loop(self, loop)` |
| `check_in` | method | `modules/websocket_beacon.py:157` | `def check_in(self)` |
| `connect` | method | `modules/websocket_beacon.py:122` | `def connect(self)` |
| `list_beacons` | method | `modules/websocket_beacon.py:447` | `def list_beacons(self)` |
| `remove_stale_beacons` | method | `modules/websocket_beacon.py:464` | `def remove_stale_beacons(self, timeout)` |
| `run` | method | `modules/websocket_beacon.py:214` | `def run(self, command_handler)` |
| `send_result` | method | `modules/websocket_beacon.py:191` | `def send_result(self, task_id, output, exit_code)` |
| `send_task` | method | `modules/websocket_beacon.py:416` | `def send_task(self, beacon_id, command)` |
| `shutdown` | method | `modules/websocket_beacon.py:263` | `def shutdown(self)` |
| `start` | method | `modules/websocket_beacon.py:382` | `def start(self)` |
| `start_in_thread` | method | `modules/websocket_beacon.py:399` | `def start_in_thread(self)` |
| `stop` | method | `modules/websocket_beacon.py:392` | `def stop(self)` |
| `BUFFER_SIZE` | macro | `modules/win_rootkit/backup.c:18` | `#define BUFFER_SIZE` |
| `Command` | struct | `modules/win_rootkit/backup.c:27` | `` |
| `HIDE_FILE` | macro | `modules/win_rootkit/backup.c:21` | `#define HIDE_FILE` |
| `KEY_FILE` | macro | `modules/win_rootkit/backup.c:22` | `#define KEY_FILE` |
| `MAX_COMMANDS` | macro | `modules/win_rootkit/backup.c:19` | `#define MAX_COMMANDS` |
| `PASSWORD` | macro | `modules/win_rootkit/backup.c:24` | `#define PASSWORD` |
| `PID_FILE` | macro | `modules/win_rootkit/backup.c:20` | `#define PID_FILE` |
| `PORT` | macro | `modules/win_rootkit/backup.c:17` | `#define PORT` |
| `VirtualFile` | struct | `modules/win_rootkit/backup.c:33` | `` |
| `elp` | function | `modules/win_rootkit/backup.c:66` | `void elp()` |
| `ensure_hide_file_exists` | function | `modules/win_rootkit/backup.c:150` | `void ensure_hide_file_exists()` |
| `ensure_key_file_exists` | function | `modules/win_rootkit/backup.c:123` | `void ensure_key_file_exists()` |
| `ensure_pid_file_exists` | function | `modules/win_rootkit/backup.c:86` | `void ensure_pid_file_exists()` |
| `handle_client` | function | `modules/win_rootkit/backup.c:204` | `DWORD WINAPI handle_client(LPVOID client_socket)` |
| `infect_command` | function | `modules/win_rootkit/backup.c:179` | `void infect_command()` |
| `main` | function | `modules/win_rootkit/backup.c:540` | `int main()` |
| `monitor_shell` | function | `modules/win_rootkit/backup.c:430` | `DWORD WINAPI monitor_shell(LPVOID data)` |
| `DllMain` | function | `modules/win_rootkit/mrhyde.c:272` | `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)` |
| `FILE_HIDE_PATH` | macro | `modules/win_rootkit/mrhyde.c:9` | `#define FILE_HIDE_PATH` |
| `FindProcessId` | function | `modules/win_rootkit/mrhyde.c:89` | `DWORD FindProcessId(const char* processName)` |
| `HideProcessByPID` | function | `modules/win_rootkit/mrhyde.c:115` | `void HideProcessByPID(DWORD pid)` |
| `HookFunctions` | function | `modules/win_rootkit/mrhyde.c:222` | `void HookFunctions()` |
| `HookedCreateToolhelp32Snapshot` | function | `modules/win_rootkit/mrhyde.c:189` | `HANDLE WINAPI HookedCreateToolhelp32Snapshot(DWORD dwFlags, DWORD th32ProcessID)` |
| `HookedFindFirstFile` | function | `modules/win_rootkit/mrhyde.c:171` | `HANDLE WINAPI HookedFindFirstFile(LPCSTR lpFileName, LPWIN32_FIND_DATA lpFindFileData)` |
| `HookedFindNextFile` | function | `modules/win_rootkit/mrhyde.c:180` | `BOOL WINAPI HookedFindNextFile(HANDLE hFindFile, LPWIN32_FIND_DATA lpFindFileData)` |
| `HookedProcess32First` | function | `modules/win_rootkit/mrhyde.c:198` | `BOOL WINAPI HookedProcess32First(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)` |
| `HookedProcess32Next` | function | `modules/win_rootkit/mrhyde.c:210` | `BOOL WINAPI HookedProcess32Next(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)` |
| `MAX_HIDE_PIDS` | macro | `modules/win_rootkit/mrhyde.c:7` | `#define MAX_HIDE_PIDS` |
| `PID_FILE_PATH` | macro | `modules/win_rootkit/mrhyde.c:8` | `#define PID_FILE_PATH` |
| `RunExperiment` | function | `modules/win_rootkit/mrhyde.c:19` | `void __cdecl RunExperiment()` |
| `load_hidden_files` | function | `modules/win_rootkit/mrhyde.c:47` | `void load_hidden_files()` |
| `load_hidden_pids` | function | `modules/win_rootkit/mrhyde.c:24` | `void load_hidden_pids()` |
| `search_pid` | function | `modules/win_rootkit/mrhyde.c:137` | `BOOL search_pid()` |
| `should_hide_file` | function | `modules/win_rootkit/mrhyde.c:161` | `BOOL should_hide_file(const char* filename)` |
| `should_hide_pid` | function | `modules/win_rootkit/mrhyde.c:147` | `BOOL should_hide_pid(DWORD pid)` |
| `GetUsernameFromPid` | method | `modules/win_rootkit/win_rin3_rootkit.cs:145` | `` |
| `HookCreateFile` | method | `modules/win_rootkit/win_rin3_rootkit.cs:226` | `` |
| `HookFindFirstFile` | method | `modules/win_rootkit/win_rin3_rootkit.cs:214` | `` |
| `SECURITY_ATTRIBUTES` | class | `modules/win_rootkit/win_rin3_rootkit.cs:64` | `` |
| `SID` | class | `modules/win_rootkit/win_rin3_rootkit.cs:136` | `` |
| `SID_AND_ATTRIBUTES` | class | `modules/win_rootkit/win_rin3_rootkit.cs:129` | `` |
| `ShouldHidePid` | method | `modules/win_rootkit/win_rin3_rootkit.cs:203` | `` |
| `TOKEN_USER` | class | `modules/win_rootkit/win_rin3_rootkit.cs:123` | `` |
| `WIN32_FIND_DATA` | class | `modules/win_rootkit/win_rin3_rootkit.cs:47` | `` |
| `WinRing3Rootkit` | class | `modules/win_rootkit/win_rin3_rootkit.cs:32` | `` |
| `AddDllToAppInitDLLs` | function | `modules/win_rootkit/win_ring3_rootkit.c:191` | `BOOL AddDllToAppInitDLLs(const char* dllPath)` |
| `BUFFER_SIZE` | macro | `modules/win_rootkit/win_ring3_rootkit.c:19` | `#define BUFFER_SIZE` |
| `Command` | struct | `modules/win_rootkit/win_ring3_rootkit.c:28` | `` |
| `DownloadDLL` | function | `modules/win_rootkit/win_ring3_rootkit.c:79` | `BOOL DownloadDLL(const char* url, PBYTE* buffer, DWORD* size)` |
| `GetProcessIdByName` | function | `modules/win_rootkit/win_ring3_rootkit.c:240` | `DWORD GetProcessIdByName(const char* processName)` |
| `Gifted` | function | `modules/win_rootkit/win_ring3_rootkit.c:270` | `BOOL Gifted(DWORD processId, const char* dllPath)` |
| `HIDE_FILE` | macro | `modules/win_rootkit/win_ring3_rootkit.c:22` | `#define HIDE_FILE` |
| `KEY_FILE` | macro | `modules/win_rootkit/win_ring3_rootkit.c:23` | `#define KEY_FILE` |
| `MAX_COMMANDS` | macro | `modules/win_rootkit/win_ring3_rootkit.c:20` | `#define MAX_COMMANDS` |
| `PASSWORD` | macro | `modules/win_rootkit/win_ring3_rootkit.c:25` | `#define PASSWORD` |
| `PIDArray` | struct | `modules/win_rootkit/win_ring3_rootkit.c:40` | `` |
| `PID_FILE` | macro | `modules/win_rootkit/win_ring3_rootkit.c:21` | `#define PID_FILE` |
| `PORT` | macro | `modules/win_rootkit/win_ring3_rootkit.c:18` | `#define PORT` |
| `ReflectiveLoadDLL` | function | `modules/win_rootkit/win_ring3_rootkit.c:99` | `BOOL ReflectiveLoadDLL(PBYTE dllBuffer, DWORD dllSize)` |
| `VirtualFile` | struct | `modules/win_rootkit/win_ring3_rootkit.c:34` | `` |
| `addPID` | function | `modules/win_rootkit/win_ring3_rootkit.c:153` | `void addPID(PIDArray *array, DWORD pid)` |
| `elp` | function | `modules/win_rootkit/win_ring3_rootkit.c:362` | `void elp()` |
| `ensure_hide_file_exists` | function | `modules/win_rootkit/win_ring3_rootkit.c:446` | `void ensure_hide_file_exists()` |
| `ensure_key_file_exists` | function | `modules/win_rootkit/win_ring3_rootkit.c:419` | `void ensure_key_file_exists()` |
| `ensure_pid_file_exists` | function | `modules/win_rootkit/win_ring3_rootkit.c:382` | `void ensure_pid_file_exists()` |
| `freePIDArray` | function | `modules/win_rootkit/win_ring3_rootkit.c:162` | `void freePIDArray(PIDArray *array)` |
| `getPIDsFromTasklist` | function | `modules/win_rootkit/win_ring3_rootkit.c:166` | `void getPIDsFromTasklist(PIDArray *pidArray)` |
| `giveGift` | function | `modules/win_rootkit/win_ring3_rootkit.c:475` | `BOOL giveGift()` |
| `handle_client` | function | `modules/win_rootkit/win_ring3_rootkit.c:526` | `DWORD WINAPI handle_client(LPVOID client_socket)` |
| `initPIDArray` | function | `modules/win_rootkit/win_ring3_rootkit.c:146` | `void initPIDArray(PIDArray *array)` |
| `main` | function | `modules/win_rootkit/win_ring3_rootkit.c:865` | `int main()` |
| `monitor_shell` | function | `modules/win_rootkit/win_ring3_rootkit.c:755` | `DWORD WINAPI monitor_shell(LPVOID data)` |
| `DllMain` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:94` | `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)` |
| `HIDDEN_DIR` | macro | `modules/win_rootkit/win_ring3_rootkit.cpp:32` | `#define HIDDEN_DIR` |
| `HIDDEN_FILE` | macro | `modules/win_rootkit/win_ring3_rootkit.cpp:33` | `#define HIDDEN_FILE` |
| `HIDE_USER` | macro | `modules/win_rootkit/win_ring3_rootkit.cpp:34` | `#define HIDE_USER` |
| `MAX_HIDE_PIDS` | macro | `modules/win_rootkit/win_ring3_rootkit.cpp:35` | `#define MAX_HIDE_PIDS` |
| `get_username_from_pid` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:42` | `char* get_username_from_pid(DWORD pid)` |
| `hook_CreateFile` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:85` | `HANDLE WINAPI hook_CreateFile(CONST char* path, DWORD access, DWORD share, LPSECURITY_ATTRIBUTES ...` |
| `hook_FindFirstFile` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:75` | `HANDLE WINAPI hook_FindFirstFile(CONST char* path, WIN32_FIND_DATA* find_data)` |
| `should_hide_pid` | function | `modules/win_rootkit/win_ring3_rootkit.cpp:65` | `int should_hide_pid(const char* pid)` |
| `_c_locale_process_env` | function | `modules/winbox_gym.py:190` | `def _c_locale_process_env()` |
| `_canonical_state` | function | `modules/winbox_gym.py:164` | `def _canonical_state(raw)` |
| `_clean_snapshot_present` | function | `modules/winbox_gym.py:508` | `def _clean_snapshot_present()` |
| `_complete_partial_build` | function | `modules/winbox_gym.py:645` | `def _complete_partial_build(notify)` |
| `_emit_notify` | function | `modules/winbox_gym.py:179` | `def _emit_notify(notifier, message)` |
| `_guest_probe_z_drive` | function | `modules/winbox_gym.py:767` | `def _guest_probe_z_drive()` |
| `_guest_probe_z_drive_retries` | function | `modules/winbox_gym.py:781` | `def _guest_probe_z_drive_retries()` |
| `_install_disk_is_substantial` | function | `modules/winbox_gym.py:537` | `def _install_disk_is_substantial()` |
| `_load_yaml` | function | `modules/winbox_gym.py:205` | `def _load_yaml(path)` |
| `_missing_prereqs` | function | `modules/winbox_gym.py:407` | `def _missing_prereqs()` |
| `_prereq_path` | function | `modules/winbox_gym.py:392` | `def _prereq_path(name)` |
| `_recover_partial_build` | function | `modules/winbox_gym.py:705` | `def _recover_partial_build(notify, build_timeout)` |
| `_repair_guest_ntfs` | function | `modules/winbox_gym.py:588` | `def _repair_guest_ntfs(notify)` |
| `_stream_command` | function | `modules/winbox_gym.py:1002` | `def _stream_command(argv)` |
| `_verify_provisioning` | function | `modules/winbox_gym.py:798` | `def _verify_provisioning(notify)` |
| `_vm_built_from` | function | `modules/winbox_gym.py:1164` | `def _vm_built_from(status)` |
| `_wait_for_shutdown` | function | `modules/winbox_gym.py:560` | `def _wait_for_shutdown(timeout, notify)` |
| `_winbox_disk_path` | function | `modules/winbox_gym.py:634` | `def _winbox_disk_path()` |
| `attack_readiness` | function | `modules/winbox_gym.py:1234` | `def attack_readiness(params)` |
| `binary_path` | function | `modules/winbox_gym.py:335` | `def binary_path()` |
| `chain_for` | function | `modules/winbox_gym.py:242` | `def chain_for(vuln_id, path)` |
| `check_readiness` | function | `modules/winbox_gym.py:412` | `def check_readiness(params)` |
| `ensure_installed` | function | `modules/winbox_gym.py:340` | `def ensure_installed(params, timeout)` |
| `ensure_lab_ready` | function | `modules/winbox_gym.py:822` | `def ensure_lab_ready(params)` |
| `ensure_prereqs` | function | `modules/winbox_gym.py:453` | `def ensure_prereqs(timeout)` |
| `ensure_vm_running` | function | `modules/winbox_gym.py:1184` | `def ensure_vm_running(timeout)` |
| `exploit_for` | function | `modules/winbox_gym.py:252` | `def exploit_for(vuln_id, path)` |
| `get` | function | `modules/winbox_gym.py:233` | `def get(vuln_id, path)` |
| `load_index` | function | `modules/winbox_gym.py:222` | `def load_index(path)` |
| `main` | function | `modules/winbox_gym.py:1262` | `def main()` |
| `record_artifact` | function | `modules/winbox_gym.py:1211` | `def record_artifact(name, output)` |
| `resolve_target` | function | `modules/winbox_gym.py:1170` | `def resolve_target()` |
| `run_cli` | function | `modules/winbox_gym.py:924` | `def run_cli(args, timeout)` |
| `summary` | function | `modules/winbox_gym.py:311` | `def summary(path)` |
| `validate_matrix` | function | `modules/winbox_gym.py:262` | `def validate_matrix(path)` |
| `vm_ip` | function | `modules/winbox_gym.py:1148` | `def vm_ip()` |
| `vm_status` | function | `modules/winbox_gym.py:1113` | `def vm_status(timeout)` |
| `vulnerabilities` | function | `modules/winbox_gym.py:227` | `def vulnerabilities(path)` |
| `WireStore` | class | `modules/wire_capture.py:47` | `class WireStore` |
| `__init__` | method | `modules/wire_capture.py:56` | `def __init__(self, task_id, base_dir)` |
| `_path_for` | method | `modules/wire_capture.py:71` | `def _path_for(self, digest)` |
| `_sanitize_digest` | function | `modules/wire_capture.py:28` | `def _sanitize_digest(digest)` |
| `capture` | method | `modules/wire_capture.py:87` | `def capture(self, digest, raw, max_bytes)` |
| `directory` | method | `modules/wire_capture.py:67` | `def directory(self)` |
| `fetch` | method | `modules/wire_capture.py:146` | `def fetch(self, digest)` |
| `has` | method | `modules/wire_capture.py:82` | `def has(self, digest)` |
| `truncated` | method | `modules/wire_capture.py:129` | `def truncated(self, digest)` |
| `list_entries` | function | `modules/workspace.py:46` | `def list_entries(rel)` |
| `make_dir` | function | `modules/workspace.py:83` | `def make_dir(rel)` |
| `read_text` | function | `modules/workspace.py:63` | `def read_text(rel, limit)` |
| `remove` | function | `modules/workspace.py:90` | `def remove(rel)` |
| `resolve` | function | `modules/workspace.py:27` | `def resolve(rel)` |
| `root` | function | `modules/workspace.py:21` | `def root()` |
| `write_text` | function | `modules/workspace.py:72` | `def write_text(rel, content)` |
| `CredentialEntry` | class | `modules/world_model.py:412` | `class CredentialEntry` |
| `DomainEntry` | class | `modules/world_model.py:438` | `class DomainEntry` |
| `EmailEntry` | class | `modules/world_model.py:430` | `class EmailEntry` |
| `EngagementPhase` | class | `modules/world_model.py:391` | `class EngagementPhase(StrEnum)` |
| `HostEntry` | class | `modules/world_model.py:588` | `class HostEntry` |
| `HostState` | class | `modules/world_model.py:375` | `class HostState(StrEnum)` |
| `NetworkGraph` | class | `modules/world_model.py:468` | `class NetworkGraph` |
| `NetworkRelation` | class | `modules/world_model.py:446` | `class NetworkRelation` |
| `ServiceInfo` | class | `modules/world_model.py:403` | `class ServiceInfo` |
| `VulnerabilityEntry` | class | `modules/world_model.py:421` | `class VulnerabilityEntry` |
| `WorldModel` | class | `modules/world_model.py:769` | `class WorldModel` |
| `_PhaseDeriver` | class | `modules/world_model.py:644` | `class _PhaseDeriver` |
| `__init__` | method | `modules/world_model.py:491` | `def __init__(self)` |
| `__init__` | method | `modules/world_model.py:777` | `def __init__(self, path)` |
| `_cred_value` | method | `modules/world_model.py:1206` | `def _cred_value(cred)` |
| `_decrypt_payload_text` | function | `modules/world_model.py:220` | `def _decrypt_payload_text(text, password, salt)` |
| `_derive_crypto_key` | function | `modules/world_model.py:78` | `def _derive_crypto_key(password, salt)` |
| `_encrypt_payload` | function | `modules/world_model.py:200` | `def _encrypt_payload(payload, password, salt)` |
| `_load` | method | `modules/world_model.py:1339` | `def _load(self)` |
| `_load_or_create_salt` | function | `modules/world_model.py:157` | `def _load_or_create_salt(salt_path)` |
| `_machine_password` | function | `modules/world_model.py:87` | `def _machine_password()` |
| `_master_password` | function | `modules/world_model.py:128` | `def _master_password()` |
| `_read_encrypted_dict` | function | `modules/world_model.py:259` | `def _read_encrypted_dict(path)` |
| `_save` | method | `modules/world_model.py:1320` | `def _save(self)` |
| `add_credential` | method | `modules/world_model.py:897` | `def add_credential(self, value, host, service)` |
| `add_domain` | method | `modules/world_model.py:992` | `def add_domain(self, domain, host, context)` |
| `add_email` | method | `modules/world_model.py:986` | `def add_email(self, address, host, context)` |
| `add_host` | method | `modules/world_model.py:793` | `def add_host(self, ip)` |
| `add_note` | method | `modules/world_model.py:853` | `def add_note(self, ip, note)` |
| `add_relation` | method | `modules/world_model.py:498` | `def add_relation(self, relation)` |
| `add_relation` | method | `modules/world_model.py:1218` | `def add_relation(self, source, target, relation, weight)` |
| `add_service` | method | `modules/world_model.py:597` | `def add_service(self, svc)` |
| `add_service` | method | `modules/world_model.py:836` | `def add_service(self, ip, port, name, version, protocol)` |
| `add_vulnerability` | method | `modules/world_model.py:980` | `def add_vulnerability(self, description, host, cve, severity)` |
| `advance` | method | `modules/world_model.py:601` | `def advance(self, new_state)` |
| `advance_host` | method | `modules/world_model.py:827` | `def advance_host(self, ip, new_state)` |
| `can_advance_to` | method | `modules/world_model.py:387` | `def can_advance_to(self, next_state)` |
| `consume_policy_facts` | method | `modules/world_model.py:1079` | `def consume_policy_facts(self, facts_path)` |
| `degree_centrality` | method | `modules/world_model.py:518` | `def degree_centrality(self)` |
| `derive` | method | `modules/world_model.py:658` | `def derive(self, hosts)` |
| `from_dict` | method | `modules/world_model.py:572` | `def from_dict(cls, data)` |
| `from_dict` | method | `modules/world_model.py:621` | `def from_dict(cls, d)` |
| `get_host` | method | `modules/world_model.py:874` | `def get_host(self, ip)` |
| `get_hosts_summary` | method | `modules/world_model.py:886` | `def get_hosts_summary(self)` |
| `get_phase` | method | `modules/world_model.py:1254` | `def get_phase(self)` |
| `get_suggested_tools` | method | `modules/world_model.py:1258` | `def get_suggested_tools(self)` |
| `get_world_model` | function | `modules/world_model.py:1457` | `def get_world_model(path)` |
| `graph_snapshot` | method | `modules/world_model.py:1247` | `def graph_snapshot(self)` |
| `in_degree` | method | `modules/world_model.py:510` | `def in_degree(self, node)` |
| `link_credential_to_failure` | method | `modules/world_model.py:950` | `def link_credential_to_failure(self, value, host)` |

Next: [SYMBOLS_p25.md](SYMBOLS_p25.md)
