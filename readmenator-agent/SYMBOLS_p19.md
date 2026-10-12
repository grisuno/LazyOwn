# Symbols (page 19 of 40)
Previous: [SYMBOLS_p18.md](SYMBOLS_p18.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_build_assets` | method | `modules/threat_model.py:318` | `def _build_assets(self, rows)` |
| `_build_detection_rules` | method | `modules/threat_model.py:475` | `def _build_detection_rules(self, ttps)` |
| `_build_iocs` | method | `modules/threat_model.py:444` | `def _build_iocs(self, rows)` |
| `_build_purple_team` | method | `modules/threat_model.py:505` | `def _build_purple_team(self, ttps, detection_rules)` |
| `_build_summary` | method | `modules/threat_model.py:560` | `def _build_summary(self, rows, assets, ttps)` |
| `_build_ttps` | method | `modules/threat_model.py:404` | `def _build_ttps(self, rows)` |
| `_compromise_indicators` | method | `modules/threat_model.py:388` | `def _compromise_indicators(self, commands)` |
| `_extract_iocs` | function | `modules/threat_model.py:245` | `def _extract_iocs(text, first_seen)` |
| `_load_csv` | method | `modules/threat_model.py:305` | `def _load_csv(self)` |
| `_risk_score` | method | `modules/threat_model.py:352` | `def _risk_score(self, commands, ports)` |
| `_save` | method | `modules/threat_model.py:578` | `def _save(self, model)` |
| `build` | method | `modules/threat_model.py:270` | `def build(self)` |
| `get_builder` | function | `modules/threat_model.py:592` | `def get_builder()` |
| `load` | method | `modules/threat_model.py:293` | `def load(self)` |
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
| `main` | function | `modules/tools/loop_smoke.py:114` | `def main()` |
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
| `Exchange` | class | `modules/traffic_recorder.py:80` | `class Exchange` |
| `RecorderConfig` | class | `modules/traffic_recorder.py:24` | `class RecorderConfig` |
| `TrafficRecorder` | class | `modules/traffic_recorder.py:91` | `class TrafficRecorder` |
| `__init__` | method | `modules/traffic_recorder.py:94` | `def __init__(self, base_dir)` |
| `_connect` | method | `modules/traffic_recorder.py:132` | `def _connect(self)` |
| `_fts_query` | method | `modules/traffic_recorder.py:375` | `def _fts_query(query)` |
| `_index_fts` | method | `modules/traffic_recorder.py:323` | `def _index_fts(self, exchange_id, req, resp)` |
| `_migrate_fts` | method | `modules/traffic_recorder.py:115` | `def _migrate_fts(self, conn)` |
| `_scan_bodies` | method | `modules/traffic_recorder.py:422` | `def _scan_bodies(self, needle, limit)` |
| `backfill_fts` | method | `modules/traffic_recorder.py:343` | `def backfill_fts(self, batch)` |
| `count` | method | `modules/traffic_recorder.py:317` | `def count(self)` |
| `export_archive` | method | `modules/traffic_recorder.py:451` | `def export_archive(self, path, limit, task)` |
| `gc` | method | `modules/traffic_recorder.py:587` | `def gc(self, older_than_sec)` |
| `get_body` | method | `modules/traffic_recorder.py:275` | `def get_body(self, exchange_id)` |
| `import_archive` | method | `modules/traffic_recorder.py:493` | `def import_archive(self, path)` |
| `import_inbox` | method | `modules/traffic_recorder.py:554` | `def import_inbox(self, inbox_dir)` |
| `latest_rowid` | method | `modules/traffic_recorder.py:247` | `def latest_rowid(self)` |
| `query` | method | `modules/traffic_recorder.py:253` | `def query(self, host, status, limit, offset, task)` |
| `read_body` | method | `modules/traffic_recorder.py:284` | `def read_body(self, exchange_id, part, offset, length)` |
| `record` | method | `modules/traffic_recorder.py:138` | `def record(self, method, url, status, req_body, resp_body, content_type, req_headers, resp_headers, host, port...` |
| `search_body` | method | `modules/traffic_recorder.py:382` | `def search_body(self, query, limit)` |
| `since` | method | `modules/traffic_recorder.py:230` | `def since(self, rowid, limit)` |
| `url_template` | function | `modules/traffic_recorder.py:69` | `def url_template(url)` |
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
| `_collect_daemon_status` | method | `modules/unified_dashboard.py:124` | `def _collect_daemon_status(self)` |
| `_collect_dashboard` | method | `modules/unified_dashboard.py:163` | `def _collect_dashboard(self)` |
| `_collect_graph_advice` | method | `modules/unified_dashboard.py:145` | `def _collect_graph_advice(self)` |
| `_collect_hive_status` | method | `modules/unified_dashboard.py:104` | `def _collect_hive_status(self)` |
| `_collect_live_graph` | method | `modules/unified_dashboard.py:133` | `def _collect_live_graph(self)` |
| `_collect_policy_status` | method | `modules/unified_dashboard.py:114` | `def _collect_policy_status(self)` |
| `_collect_world_model` | method | `modules/unified_dashboard.py:95` | `def _collect_world_model(self)` |
| `_get_dashboard` | method | `modules/unified_dashboard.py:49` | `def _get_dashboard(self)` |
| `_get_graph` | method | `modules/unified_dashboard.py:65` | `def _get_graph(self)` |
| `build_unified_snapshot` | method | `modules/unified_dashboard.py:76` | `def build_unified_snapshot(self)` |
| `export_json` | method | `modules/unified_dashboard.py:254` | `def export_json(self)` |
| `get_unified_dashboard` | function | `modules/unified_dashboard.py:259` | `def get_unified_dashboard(sessions_dir)` |
| `render_unified` | method | `modules/unified_dashboard.py:173` | `def render_unified(self)` |
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
| `main` | function | `modules/vuln_bot_cli.py:22` | `def main()` |
| `parse_args` | function | `modules/vuln_bot_cli.py:10` | `def parse_args()` |
| `VulnBotCLI` | class | `modules/vulnbot.py:29` | `class VulnBotCLI` |
| `__init__` | method | `modules/vulnbot.py:30` | `def __init__(self, provider, mode, debug, script_path)` |
| `_load_external_tools` | method | `modules/vulnbot.py:109` | `def _load_external_tools(self, script_path)` |
| `_load_model` | method | `modules/vulnbot.py:46` | `def _load_model(self)` |
| `_register_file_tools` | method | `modules/vulnbot.py:83` | `def _register_file_tools(self)` |
| `_setup_agent` | method | `modules/vulnbot.py:61` | `def _setup_agent(self, script_path)` |
| `_stream_agent_response` | method | `modules/vulnbot.py:136` | `def _stream_agent_response(self, prompt)` |
| `add_to_knowledge_base` | method | `modules/vulnbot.py:212` | `def add_to_knowledge_base(self, prompt, response)` |
| `create_complex_prompt` | method | `modules/vulnbot.py:160` | `def create_complex_prompt(self, base_prompt, history, knowledge)` |
| `edit_file` | function | `modules/vulnbot.py:95` | `def edit_file(path, content, old_text)` |
| `generate` | function | `modules/vulnbot.py:139` | `def generate()` |
| `generate` | function | `modules/vulnbot.py:207` | `def generate()` |
| `get_relevant_knowledge` | method | `modules/vulnbot.py:155` | `def get_relevant_knowledge(self, prompt)` |
| `list_files` | function | `modules/vulnbot.py:86` | `def list_files(directory)` |
| `load_event_config` | method | `modules/vulnbot.py:182` | `def load_event_config(self)` |
| `load_knowledge_base` | method | `modules/vulnbot.py:145` | `def load_knowledge_base(self)` |
| `process_with_context` | method | `modules/vulnbot.py:190` | `def process_with_context(self, file_path, event)` |
| `read_file` | function | `modules/vulnbot.py:90` | `def read_file(path)` |
| `read_file_content` | method | `modules/vulnbot.py:176` | `def read_file_content(self, file_path)` |
| `save_knowledge_base` | method | `modules/vulnbot.py:151` | `def save_knowledge_base(self, kb)` |
| `stream_response` | method | `modules/vulnbot.py:206` | `def stream_response(self, prompt)` |
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
| `list_entries` | function | `modules/workspace.py:46` | `def list_entries(rel)` |
| `make_dir` | function | `modules/workspace.py:83` | `def make_dir(rel)` |
| `read_text` | function | `modules/workspace.py:63` | `def read_text(rel, limit)` |
| `remove` | function | `modules/workspace.py:90` | `def remove(rel)` |
| `resolve` | function | `modules/workspace.py:27` | `def resolve(rel)` |
| `root` | function | `modules/workspace.py:21` | `def root()` |
| `write_text` | function | `modules/workspace.py:72` | `def write_text(rel, content)` |
| `CredentialEntry` | class | `modules/world_model.py:188` | `class CredentialEntry` |
| `DomainEntry` | class | `modules/world_model.py:214` | `class DomainEntry` |
| `EmailEntry` | class | `modules/world_model.py:206` | `class EmailEntry` |
| `EngagementPhase` | class | `modules/world_model.py:167` | `class EngagementPhase(StrEnum)` |
| `HostEntry` | class | `modules/world_model.py:364` | `class HostEntry` |
| `HostState` | class | `modules/world_model.py:151` | `class HostState(StrEnum)` |
| `NetworkGraph` | class | `modules/world_model.py:244` | `class NetworkGraph` |
| `NetworkRelation` | class | `modules/world_model.py:222` | `class NetworkRelation` |
| `ServiceInfo` | class | `modules/world_model.py:179` | `class ServiceInfo` |
| `VulnerabilityEntry` | class | `modules/world_model.py:197` | `class VulnerabilityEntry` |
| `WorldModel` | class | `modules/world_model.py:541` | `class WorldModel` |
| `_PhaseDeriver` | class | `modules/world_model.py:416` | `class _PhaseDeriver` |
| `__init__` | method | `modules/world_model.py:267` | `def __init__(self)` |
| `__init__` | method | `modules/world_model.py:549` | `def __init__(self, path)` |
| `_derive_crypto_key` | function | `modules/world_model.py:58` | `def _derive_crypto_key(password, salt)` |
| `_load` | method | `modules/world_model.py:1048` | `def _load(self)` |
| `_master_password` | function | `modules/world_model.py:67` | `def _master_password()` |
| `_save` | method | `modules/world_model.py:1029` | `def _save(self)` |
| `add_credential` | method | `modules/world_model.py:653` | `def add_credential(self, value, host, service)` |
| `add_domain` | method | `modules/world_model.py:748` | `def add_domain(self, domain, host, context)` |
| `add_email` | method | `modules/world_model.py:742` | `def add_email(self, address, host, context)` |
| `add_host` | method | `modules/world_model.py:565` | `def add_host(self, ip)` |
| `add_note` | method | `modules/world_model.py:609` | `def add_note(self, ip, note)` |
| `add_relation` | method | `modules/world_model.py:274` | `def add_relation(self, relation)` |
| `add_relation` | method | `modules/world_model.py:927` | `def add_relation(self, source, target, relation, weight)` |
| `add_service` | method | `modules/world_model.py:373` | `def add_service(self, svc)` |
| `add_service` | method | `modules/world_model.py:592` | `def add_service(self, ip, port, name, version, protocol)` |
| `add_vulnerability` | method | `modules/world_model.py:736` | `def add_vulnerability(self, description, host, cve, severity)` |
| `advance` | method | `modules/world_model.py:377` | `def advance(self, new_state)` |
| `advance_host` | method | `modules/world_model.py:583` | `def advance_host(self, ip, new_state)` |
| `can_advance_to` | method | `modules/world_model.py:163` | `def can_advance_to(self, next_state)` |
| `consume_policy_facts` | method | `modules/world_model.py:835` | `def consume_policy_facts(self, facts_path)` |
| `degree_centrality` | method | `modules/world_model.py:294` | `def degree_centrality(self)` |
| `derive` | method | `modules/world_model.py:430` | `def derive(self, hosts)` |
| `from_dict` | method | `modules/world_model.py:348` | `def from_dict(cls, data)` |
| `from_dict` | method | `modules/world_model.py:397` | `def from_dict(cls, d)` |
| `get_host` | method | `modules/world_model.py:630` | `def get_host(self, ip)` |
| `get_hosts_summary` | method | `modules/world_model.py:642` | `def get_hosts_summary(self)` |
| `get_phase` | method | `modules/world_model.py:963` | `def get_phase(self)` |
| `get_suggested_tools` | method | `modules/world_model.py:967` | `def get_suggested_tools(self)` |
| `get_world_model` | function | `modules/world_model.py:1126` | `def get_world_model(path)` |
| `graph_snapshot` | method | `modules/world_model.py:956` | `def graph_snapshot(self)` |
| `in_degree` | method | `modules/world_model.py:286` | `def in_degree(self, node)` |
| `link_credential_to_failure` | method | `modules/world_model.py:706` | `def link_credential_to_failure(self, value, host)` |
| `link_credential_to_success` | method | `modules/world_model.py:685` | `def link_credential_to_success(self, value, host)` |
| `neighbors` | method | `modules/world_model.py:282` | `def neighbors(self, node)` |
| `out_degree` | method | `modules/world_model.py:290` | `def out_degree(self, node)` |
| `pivot_candidates` | method | `modules/world_model.py:309` | `def pivot_candidates(self, top_k)` |
| `pivot_candidates` | method | `modules/world_model.py:948` | `def pivot_candidates(self, top_k)` |
| `rank` | method | `modules/world_model.py:160` | `def rank(self)` |
| `read_state_dict` | function | `modules/world_model.py:72` | `def read_state_dict(path)` |
| `reload` | method | `modules/world_model.py:1078` | `def reload(self)` |
| `reset` | method | `modules/world_model.py:1094` | `def reset(self)` |
| `reset_host` | method | `modules/world_model.py:573` | `def reset_host(self, ip)` |
| `set_os_hint` | method | `modules/world_model.py:616` | `def set_os_hint(self, ip, os_hint)` |
| `snapshot` | method | `modules/world_model.py:1105` | `def snapshot(self)` |
| `to_context_string` | method | `modules/world_model.py:970` | `def to_context_string(self)` |
| `to_dict` | method | `modules/world_model.py:331` | `def to_dict(self)` |
| `to_dict` | method | `modules/world_model.py:385` | `def to_dict(self)` |
| `update_from_findings` | method | `modules/world_model.py:762` | `def update_from_findings(self, findings)` |
| `write_state_dict` | function | `modules/world_model.py:118` | `def write_state_dict(path, data)` |
| `YAMLPromptGenerator` | class | `modules/yaml_generator.py:17` | `class YAMLPromptGenerator` |
| `__init__` | method | `modules/yaml_generator.py:18` | `def __init__(self, provider, api_key)` |
| `_load_model` | method | `modules/yaml_generator.py:32` | `def _load_model(self)` |
| `create_yaml_addon` | method | `modules/yaml_generator.py:109` | `def create_yaml_addon(self, user_request, output_dir)` |
| `extract_yaml_from_markdown` | method | `modules/yaml_generator.py:100` | `def extract_yaml_from_markdown(self, text)` |
| `generate_prompt` | method | `modules/yaml_generator.py:54` | `def generate_prompt(self, user_request)` |
| `load_payload` | method | `modules/yaml_generator.py:25` | `def load_payload(self)` |
| `main` | function | `modules/yaml_generator.py:141` | `def main()` |
| `YaraScanner` | class | `modules/yara_scanner.py:23` | `class YaraScanner` |
| `__init__` | method | `modules/yara_scanner.py:31` | `def __init__(self, rules_dir, auto_compile)` |
| `_format_match` | method | `modules/yara_scanner.py:162` | `def _format_match(self, match)` |
| `_load_external_vars` | method | `modules/yara_scanner.py:45` | `def _load_external_vars(self)` |
| `_scan_with_timeout` | method | `modules/yara_scanner.py:129` | `def _scan_with_timeout(self, filepath, externals, timeout)` |
| `_sha256` | method | `modules/yara_scanner.py:250` | `def _sha256(filepath)` |
| `add_rule` | method | `modules/yara_scanner.py:258` | `def add_rule(self, name, content)` |
| `compile_all` | method | `modules/yara_scanner.py:54` | `def compile_all(self)` |
| `create_default_rules` | function | `modules/yara_scanner.py:371` | `def create_default_rules()` |
| `download_community_rules` | method | `modules/yara_scanner.py:300` | `def download_community_rules(self)` |
| `ensure_directory` | method | `modules/yara_scanner.py:41` | `def ensure_directory(self)` |
| `ioc_scan` | method | `modules/yara_scanner.py:328` | `def ioc_scan(self, target_path, iocs)` |
| `list_rules` | method | `modules/yara_scanner.py:277` | `def list_rules(self)` |
| `scan_directory` | method | `modules/yara_scanner.py:187` | `def scan_directory(self, directory, recursive, extensions, max_files)` |
| `scan_file` | method | `modules/yara_scanner.py:98` | `def scan_file(self, filepath, timeout)` |
| `target` | function | `modules/yara_scanner.py:137` | `def target()` |
| `all` | function | `plugins/generate_c_reverse_shell.lua:108` | `` |
| `generate_c_reverse_shell` | function | `plugins/generate_c_reverse_shell.lua:1` | `` |
| `generate_cleanup_commands` | function | `plugins/generate_cleanup_commands.lua:3` | `` |
| `generate_html_payload` | function | `plugins/generate_html_payload.lua:1` | `` |
| `generate_lateral_command` | function | `plugins/generate_lateral_command.lua:4` | `` |
| `all` | function | `plugins/generate_linux_asm_reverse_shell.lua:121` | `` |
| `generate_linux_asm_reverse_shell` | function | `plugins/generate_linux_asm_reverse_shell.lua:1` | `` |
| `generate_linux_raw_shellcode` | function | `plugins/generate_linux_raw_shellcode.lua:1` | `` |
| `Xor` | function | `plugins/generate_lolbird.lua:64` | `` |
| `generate_lolbird_ps1` | function | `plugins/generate_lolbird.lua:44` | `` |
| `read_file` | function | `plugins/generate_lolbird.lua:12` | `` |
| `write_file` | function | `plugins/generate_lolbird.lua:4` | `` |
| `xor_hex_string` | function | `plugins/generate_lolbird.lua:21` | `` |
| `xor_string` | function | `plugins/generate_lolbird.lua:31` | `` |
| `execute_command_to_file` | function | `plugins/generate_msfvenom_loader.lua:2` | `` |
| `generate_loader` | function | `plugins/generate_msfvenom_loader.lua:49` | `` |
| `generate_msfvenom_loader` | function | `plugins/generate_msfvenom_loader.lua:104` | `` |
| `hex_to_nasm` | function | `plugins/generate_msfvenom_loader.lua:18` | `` |
| `read_file` | function | `plugins/generate_msfvenom_loader.lua:7` | `` |
| `generate_msfvenom_loader_windows` | function | `plugins/generate_msfvenom_loader_windows.lua:2` | `` |
| `generate_reverse_shell` | function | `plugins/generate_reverse_shell.lua:1` | `` |
| `generate_stub_ps1` | function | `plugins/generate_stub.lua:43` | `` |
| `read_file` | function | `plugins/generate_stub.lua:12` | `` |
| `write_file` | function | `plugins/generate_stub.lua:4` | `` |
| `xor_data` | function | `plugins/generate_stub.lua:21` | `` |
| `xor_string` | function | `plugins/generate_stub.lua:30` | `` |
| `load_plugin` | function | `plugins/init_plugins.lua:6` | `` |
| `kerberos_harvest` | function | `plugins/kerberos_harvest.lua:1` | `` |
| `read_file` | function | `plugins/lolbas_certutil_download_exec.lua:13` | `` |
| `write_file` | function | `plugins/lolbas_certutil_download_exec.lua:5` | `` |
| `xor_data` | function | `plugins/lolbas_certutil_download_exec.lua:21` | `` |
| `run_msfvenom` | function | `plugins/lolbas_certutil_exe.lua:2` | `` |
| `write_file` | function | `plugins/lolbas_wmic_xsl_execution.lua:4` | `` |
| `parse_nmap_with_xmlstarlet` | function | `plugins/parse_nmap_with_xmlstarlet.lua:1` | `` |
| `run_nuclei_on_nmap_files` | function | `plugins/run_nuclei_on_nmap_files.lua:1` | `` |
| `run_python_rev_c2` | function | `plugins/run_python_rev_c2.lua:2` | `` |
| `base64_encode` | function | `plugins/rundll32_sct_from_url.lua:22` | `` |
| `generate_sct` | function | `plugins/rundll32_sct_from_url.lua:58` | `` |
| `read_file` | function | `plugins/rundll32_sct_from_url.lua:12` | `` |
| `write_file` | function | `plugins/rundll32_sct_from_url.lua:4` | `` |
| `esc_hex_to_bytes` | function | `plugins/validate_shellcode.lua:21` | `` |
| `hex_list_to_byte_values` | function | `plugins/validate_shellcode.lua:65` | `` |
| `hex_to_bytes` | function | `plugins/validate_shellcode.lua:2` | `` |
| `validate_shellcode` | function | `plugins/validate_shellcode.lua:81` | `` |
| `visualize_network` | function | `plugins/visualize_network.lua:1` | `` |
| `DashboardPanel` | class | `poc_tui/app.py:137` | `class DashboardPanel(Static)` |
| `LazyOwnTUI` | class | `poc_tui/app.py:297` | `class LazyOwnTUI(App)` |
| `OutputPanel` | class | `poc_tui/app.py:240` | `class OutputPanel(VerticalScroll)` |
| `PluginBrowser` | class | `poc_tui/app.py:195` | `class PluginBrowser(Static)` |
| `ShellBackend` | class | `poc_tui/app.py:44` | `class ShellBackend` |
| `__init__` | method | `poc_tui/app.py:47` | `def __init__(self, base_dir)` |
| `__init__` | method | `poc_tui/app.py:140` | `def __init__(self, base_dir)` |
| `__init__` | method | `poc_tui/app.py:198` | `def __init__(self)` |
| `__init__` | method | `poc_tui/app.py:248` | `def __init__(self)` |
| `__init__` | method | `poc_tui/app.py:394` | `def __init__(self, base_dir)` |
| `_auto_refresh_dashboard` | method | `poc_tui/app.py:464` | `def _auto_refresh_dashboard(self)` |
| `_drain_queue` | method | `poc_tui/app.py:495` | `def _drain_queue(self)` |
| `_guess_category` | method | `poc_tui/app.py:223` | `def _guess_category(name, help_text)` |
| `_init_backend` | function | `poc_tui/app.py:429` | `def _init_backend()` |
| `_log` | method | `poc_tui/app.py:255` | `def _log(self)` |
| `_on_backend_ready` | method | `poc_tui/app.py:444` | `def _on_backend_ready(self)` |
| `_show_result` | method | `poc_tui/app.py:525` | `def _show_result(self, result)` |
| `_tab_complete` | method | `poc_tui/app.py:605` | `def _tab_complete(self, inp)` |
| `_work` | function | `poc_tui/app.py:510` | `def _work()` |
| `action_clear_output` | method | `poc_tui/app.py:539` | `def action_clear_output(self)` |
| `action_quit` | method | `poc_tui/app.py:561` | `def action_quit(self)` |
| `action_refresh_dashboard` | method | `poc_tui/app.py:555` | `def action_refresh_dashboard(self)` |
| `action_tab_complete` | method | `poc_tui/app.py:544` | `def action_tab_complete(self)` |
| `action_toggle_sidebar` | method | `poc_tui/app.py:549` | `def action_toggle_sidebar(self)` |
| `append_command` | method | `poc_tui/app.py:268` | `def append_command(self, cmd)` |
| `append_error` | method | `poc_tui/app.py:283` | `def append_error(self, text)` |
| `append_result` | method | `poc_tui/app.py:273` | `def append_result(self, text, success)` |
| `append_system` | method | `poc_tui/app.py:287` | `def append_system(self, text)` |
| `compose` | method | `poc_tui/app.py:144` | `def compose(self)` |
| `compose` | method | `poc_tui/app.py:201` | `def compose(self)` |
| `compose` | method | `poc_tui/app.py:252` | `def compose(self)` |
| `compose` | method | `poc_tui/app.py:405` | `def compose(self)` |
| `execute_command` | method | `poc_tui/app.py:470` | `def execute_command(self, cmd_str)` |
| `get_aliases` | method | `poc_tui/app.py:119` | `def get_aliases(self)` |

Next: [SYMBOLS_p20.md](SYMBOLS_p20.md)
