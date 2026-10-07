# Subsystem: modules (page 10 of 10)
Previous: [KB_modules_p9.md](KB_modules_p9.md)

## modules/tel.py
- Doc: to_numbers: Simula la función toNumbers de JavaScript
- Layer: utility
- Language: py
- Symbols:
  - `get_machine_id` (function, line 10) `def get_machine_id()`
  - `get_version` (function, line 22) `def get_version()`
  - `to_numbers` (function, line 33) `def to_numbers(hex_str)`
  - `to_hex` (function, line 37) `def to_hex(byte_list)`
  - `decrypt_cookie` (function, line 41) `def decrypt_cookie(encrypted, key, iv)`
  - `main` (function, line 47) `def main()`

## modules/test_lazyencoder_decoder.py
- Layer: testing
- Language: py
- Depends on: `modules/lazyencoder_decoder.py`

## modules/threat_model.py
- Doc: — Blue team threat model builder for LazyOwn.
- Layer: business_logic
- Language: py
- Symbols:
  - `_extract_iocs` (function, line 245) `def _extract_iocs(text, first_seen)`
  - `ThreatModelBuilder` (class, line 267) `class ThreatModelBuilder`
  - `get_builder` (method, line 577) `def get_builder()`
  - `build` (method, line 270) `def build(self)`
  - `load` (method, line 293) `def load(self)`
  - `_load_csv` (method, line 305) `def _load_csv(self)`
  - `_build_assets` (method, line 318) `def _build_assets(self, rows)`
  - `_risk_score` (method, line 352) `def _risk_score(self, commands, ports)`
  - `_compromise_indicators` (method, line 375) `def _compromise_indicators(self, commands)`
  - `_build_ttps` (method, line 391) `def _build_ttps(self, rows)`
  - `_build_iocs` (method, line 431) `def _build_iocs(self, rows)`
  - `_build_detection_rules` (method, line 462) `def _build_detection_rules(self, ttps)`
  - `_build_purple_team` (method, line 490) `def _build_purple_team(self, ttps, detection_rules)`
  - `_build_summary` (method, line 545) `def _build_summary(self, rows, assets, ttps)`
  - `_save` (method, line 563) `def _save(self, model)`
  - `_add` (method, line 435) `def _add(ioc)`
- Depends on: `core/logging.py`
- Imported by: `cli/commands/mcp_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`

## modules/timeline_narrator.py
- Doc: LazyOwn Timeline Narrator
- Layer: utility
- Language: py
- Symbols:
  - `_load_events` (function, line 56) `def _load_events(n)`
  - `_format_events_for_prompt` (function, line 75) `def _format_events_for_prompt(events)`
  - `_call_ai` (function, line 94) `def _call_ai(api_key, events_text, target)`
  - `_write_timeline` (function, line 115) `def _write_timeline(narrative, event_count, target)`
  - `narrate` (function, line 129) `def narrate(api_key, force)`
  - `load_timeline` (function, line 164) `def load_timeline()`
- Depends on: `modules/ai_fallback.py`
- Imported by: `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`

## modules/timestomper.py
- Doc: Filesystem timestomping — MACB timestamp manipulation for stealth.
- Layer: utility
- Language: py
- Symbols:
  - `TimestompConfig` (class, line 24) `class TimestompConfig`
  - `FileTimestamps` (class, line 51) `class FileTimestamps`
  - `Timestomper` (class, line 69) `class Timestomper`
  - `__init__` (method, line 106) `def __init__(self, config)`
  - `windows_timestomp_powershell` (method, line 110) `def windows_timestomp_powershell(self)`
  - `windows_timestomp_c` (method, line 152) `def windows_timestomp_c(self)`
  - `linux_timestomp_commands` (method, line 200) `def linux_timestomp_commands(self)`
  - `macos_timestomp_commands` (method, line 241) `def macos_timestomp_commands(self)`
  - `_pick_reference` (method, line 269) `def _pick_reference(self, path, platform)`
  - `generate_random_timestamps` (method, line 280) `def generate_random_timestamps(self, reference_ts, window_days)`
  - `verify_timestamps` (method, line 300) `def verify_timestamps(self, target_paths)`
  - `summary` (method, line 324) `def summary(self)`
- Imported by: `cli/commands/opsec_cleanup.py`

## modules/tmp.sh
- Layer: utility
- Language: sh

## modules/tool_extractor.py
- Doc: extract_tools_from_source: Extrae AgentTool desde archivos Python (ideal para cmd2)
- Layer: utility
- Language: py
- Symbols:
  - `extract_tools_from_source` (function, line 6) `def extract_tools_from_source(file_path, class_name, prefix)`
- Depends on: `modules/agent_tool.py`

## modules/toposwarm_bridge.py
- Doc: modules/toposwarm_bridge.py
- Layer: utility
- Language: py
- Symbols:
  - `RoutedCall` (class, line 68) `class RoutedCall`
  - `_keyword_route` (method, line 198) `def _keyword_route(prompt)`
  - `_load_toposwarm_modules` (method, line 234) `def _load_toposwarm_modules()`
  - `OnlineFeedbackLoop` (class, line 266) `class OnlineFeedbackLoop`
  - `TopoSwarmBridge` (class, line 413) `class TopoSwarmBridge`
  - `get_bridge` (method, line 626) `def get_bridge()`
  - `lazyown_command` (method, line 77) `def lazyown_command(self)`
  - `__init__` (method, line 289) `def __init__(self, maxsize)`
  - `register` (method, line 296) `def register(self, result, hidden)`
  - `feedback` (method, line 311) `def feedback(self, result_id, good, comment, routing_head)`
  - `pending_count` (method, line 373) `def pending_count(self)`
  - `stats` (method, line 376) `def stats(self)`
  - `load_feedback_for_training` (method, line 383) `def load_feedback_for_training(self)`
  - `__init__` (method, line 421) `def __init__(self)`
  - `available` (method, line 433) `def available(self)`
  - `model_loaded` (method, line 438) `def model_loaded(self)`
  - `_try_load` (method, line 441) `def _try_load(self)`
  - `_neural_route` (method, line 481) `def _neural_route(self, prompt)`
  - `feedback` (method, line 544) `def feedback(self, result_id, good, comment)`
  - `route` (method, line 568) `def route(self, prompt)`
  - `execute_via_orchestrator` (method, line 595) `def execute_via_orchestrator(self, prompt, no_model)`
  - `_hook` (method, line 494) `def _hook(m, i, o)`
- Depends on: `core/logging.py`
- Imported by: `modules/ai_fallback.py`, `modules/hive_invoke.py`, `modules/moe_router.py`, `modules/unified_bridge.py`, `skills/toposwarm_autonomous.py`

## modules/traffic_morpher.py
- Doc: C2 traffic obfuscation: domain fronting, protocol mimicking, and traffic shaping.
- Layer: utility
- Language: py
- Symbols:
  - `TrafficMorpher` (class, line 18) `class TrafficMorpher`
  - `__init__` (method, line 77) `def __init__(self)`
  - `get_random_http_headers` (method, line 81) `def get_random_http_headers(self)`
  - `get_cdn_fronting_hosts` (method, line 91) `def get_cdn_fronting_hosts(self, provider, count)`
  - `generate_traffic_padding` (method, line 108) `def generate_traffic_padding(self, min_bytes, max_bytes)`
  - `generate_jitter` (method, line 125) `def generate_jitter(self, base_delay, jitter_pct)`
  - `generate_dns_tunnel_payload` (method, line 138) `def generate_dns_tunnel_payload(self, data, domain)`
  - `generate_icmp_exfil_payload` (method, line 164) `def generate_icmp_exfil_payload(self, data, chunk_size)`
  - `generate_websocket_masking` (method, line 190) `def generate_websocket_masking(self, data)`
  - `generate_cloudflare_worker_proxy_config` (method, line 205) `def generate_cloudflare_worker_proxy_config(self, c2_host, c2_port, auth_token)`
  - `generate_beacon_profile` (method, line 270) `def generate_beacon_profile(self, name, protocol, jitter_pct, user_agent)`
- Imported by: `cli/commands/persist_migrated.py`

## modules/ttp_coverage.py
- Doc: TTP coverage matrix — real-time MITRE ATT&CK technique tracking.
- Layer: utility
- Language: py
- Symbols:
  - `TTPRow` (class, line 55) `class TTPRow`
  - `TTPCoverage` (class, line 65) `class TTPCoverage`
  - `get_coverage` (method, line 260) `def get_coverage()`
  - `__init__` (method, line 68) `def __init__(self)`
  - `rebuild_from_operations` (method, line 76) `def rebuild_from_operations(self)`
  - `add` (method, line 125) `def add(self, technique_id, name, tactic, status, operation_id)`
  - `compute_ready` (method, line 146) `def compute_ready(self, available_facts)`
  - `_blocking_facts` (method, line 165) `def _blocking_facts(self, tactic)`
  - `matrix` (method, line 187) `def matrix(self)`
  - `status_by_id` (method, line 231) `def status_by_id(self, technique_id)`
  - `to_dict` (method, line 234) `def to_dict(self)`
  - `_save_state` (method, line 241) `def _save_state(self)`
  - `_load_state` (method, line 248) `def _load_state(self)`
- Depends on: `core/logging.py`
- Imported by: `cli/commands/caldera.py`

## modules/unified_bridge.py
- Doc: UnifiedBridge — single API over all LazyOwn bridges and routing engines.
- Layer: utility
- Language: py
- Symbols:
  - `RouteResult` (class, line 39) `class RouteResult`
  - `DelegateResult` (class, line 52) `class DelegateResult`
  - `RouteBackend` (class, line 60) `class RouteBackend(ABC)`
  - `KeywordBackend` (class, line 68) `class KeywordBackend(RouteBackend)`
  - `LazyownBridgeBackend` (class, line 116) `class LazyownBridgeBackend(RouteBackend)`
  - `TopoSwarmBackend` (class, line 151) `class TopoSwarmBackend(RouteBackend)`
  - `UnifiedBridge` (class, line 182) `class UnifiedBridge`
  - `route_prompt` (method, line 355) `def route_prompt(prompt, context)`
  - `delegate_task` (method, line 360) `def delegate_task(goal, backend)`
  - `available` (method, line 62) `def available(self)`
  - `route` (method, line 65) `def route(self, prompt, context)`
  - `available` (method, line 95) `def available(self)`
  - `route` (method, line 98) `def route(self, prompt, context)`
  - `available` (method, line 119) `def available(self)`
  - `route` (method, line 126) `def route(self, prompt, context)`
  - `available` (method, line 154) `def available(self)`
  - `route` (method, line 162) `def route(self, prompt, context)`
  - `__init__` (method, line 201) `def __init__(self)`
  - `_init_backends` (method, line 206) `def _init_backends(self)`
  - `get` (method, line 212) `def get(cls)`
  - `set_publish_callback` (method, line 217) `def set_publish_callback(self, cb)`
  - `_publish` (method, line 220) `def _publish(self, category, event_type, payload)`
  - `route` (method, line 237) `def route(self, prompt, context)`
  - `delegate` (method, line 280) `def delegate(self, goal, backend, timeout)`
  - `list_backends` (method, line 332) `def list_backends(self)`
  - `_detect_phase` (method, line 338) `def _detect_phase(self)`
  - `_get_active_target` (method, line 346) `def _get_active_target(self)`
- Depends on: `core/logging.py`, `modules/event_bus.py`, `modules/lazyown_bridge.py`, `modules/mcp_agent_bridge.py`, `modules/state_manager.py`, `modules/toposwarm_bridge.py`
- Imported by: `lazyown.py`

## modules/unified_dashboard.py
- Doc: Unified campaign dashboard — combines all state sources into one view.
- Layer: utility
- Language: py
- Symbols:
  - `UnifiedDashboard` (class, line 36) `class UnifiedDashboard`
  - `get_unified_dashboard` (method, line 253) `def get_unified_dashboard(sessions_dir)`
  - `__init__` (method, line 43) `def __init__(self, sessions_dir)`
  - `_get_dashboard` (method, line 48) `def _get_dashboard(self)`
  - `_get_graph` (method, line 63) `def _get_graph(self)`
  - `build_unified_snapshot` (method, line 73) `def build_unified_snapshot(self)`
  - `_collect_world_model` (method, line 92) `def _collect_world_model(self)`
  - `_collect_hive_status` (method, line 101) `def _collect_hive_status(self)`
  - `_collect_policy_status` (method, line 110) `def _collect_policy_status(self)`
  - `_collect_daemon_status` (method, line 119) `def _collect_daemon_status(self)`
  - `_collect_live_graph` (method, line 128) `def _collect_live_graph(self)`
  - `_collect_graph_advice` (method, line 139) `def _collect_graph_advice(self)`
  - `_collect_dashboard` (method, line 157) `def _collect_dashboard(self)`
  - `render_unified` (method, line 167) `def render_unified(self)`
  - `export_json` (method, line 248) `def export_json(self)`
- Depends on: `cli/graph_advisor.py`, `core/logging.py`, `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/live_surface.py`, `modules/world_model.py`, `skills/hive_mind.py`, `skills/lazyown_policy.py`
- Imported by: `skills/lazyown_mcp.py`, `tests/test_unified_dashboard.py`

## modules/update_db.sh
- Doc: Nombre del script: update_db.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh

## modules/venator.py
- Layer: utility
- Language: py
- Symbols:
  - `getUUID` (function, line 37) `def getUUID()`
  - `getSystemInfo` (function, line 55) `def getSystemInfo(output_file)`
  - `getVTResult` (function, line 71) `def getVTResult(fileHash)`
  - `getHash` (function, line 100) `def getHash(file, ignoreVFlag)`
  - `checkSignature` (function, line 119) `def checkSignature(file, bundle)`
  - `datetime_handler` (function, line 186) `def datetime_handler(x)`
  - `parseAgentsDaemons` (function, line 190) `def parseAgentsDaemons(item, path)`
  - `getLaunchAgents` (function, line 261) `def getLaunchAgents(path, output_file, ignoreVFlag)`
  - `getLaunchDaemons` (function, line 275) `def getLaunchDaemons(path, output_file, ignoreVFlag)`
  - `getUsers` (function, line 289) `def getUsers(output_file)`
  - `getSafariExtensions` (function, line 309) `def getSafariExtensions(path, output_file)`
  - `getChromeExtensions` (function, line 327) `def getChromeExtensions(path, output_file)`
  - `getChromeDownloads` (function, line 357) `def getChromeDownloads(chromeHistoryDbPath, output_file)`
  - `getFirefoxExtensions` (function, line 398) `def getFirefoxExtensions(path, output_file)`
  - `getInstallHistory` (function, line 432) `def getInstallHistory(output_file)`
  - `getCronJobs` (function, line 449) `def getCronJobs(users, output_file)`
  - `getEmond` (function, line 465) `def getEmond(output_file)`
  - `getKext` (function, line 481) `def getKext(sipStatus, kextPath, output_file, ignoreVFlag)`
  - `getEnv` (function, line 527) `def getEnv(output_file)`
  - `getPeriodicScripts` (function, line 541) `def getPeriodicScripts(output_file)`
  - `getConnections` (function, line 557) `def getConnections(output_file)`
  - `SIPStatus` (function, line 584) `def SIPStatus(output_file)`
  - `GatekeeperStatus` (function, line 598) `def GatekeeperStatus(output_file)`
  - `parseApp` (function, line 609) `def parseApp(app, ignoreVFlag)`
  - `getLoginItems` (function, line 651) `def getLoginItems(path, output_file, ignoreVFlag)`
  - `getApps` (function, line 681) `def getApps(path, output_file, ignoreVFlag)`
  - `getEventTaps` (function, line 704) `def getEventTaps(output_file)`
  - `getBashHistory` (function, line 724) `def getBashHistory(output_file, users)`
  - `getShellStartupScripts` (function, line 741) `def getShellStartupScripts(users, output_file)`
  - `hmac_sha256` (function, line 781) `def hmac_sha256(key, data)`
  - `amzn_sig` (function, line 785) `def amzn_sig(secret_access_key, data, aws_region, aws_service)`
  - `amzn_canonical_req` (function, line 795) `def amzn_canonical_req(filename_path, headers_list)`
  - `s3_upload` (function, line 807) `def s3_upload(data, content_type, filename_path, access_key_id, secret_access_key, s3_bucket, aws_region)`
  - `io_key` (function, line 45) `def io_key(keyname)`

## modules/vuln_agent.py
- Doc: LazyOwnShellWrapper: Wrapper robusto para integrar lazyown.py
- Layer: presentation
- Language: py
- Symbols:
  - `configure_logging` (function, line 35) `def configure_logging(debug)`
  - `LazyOwnShellWrapper` (class, line 39) `class LazyOwnShellWrapper`
  - `VulnBotCLI` (class, line 121) `class VulnBotCLI`
  - `parse_args` (method, line 285) `def parse_args()`
  - `interactive_mode` (method, line 297) `def interactive_mode(bot)`
  - `main` (method, line 318) `def main()`
  - `__init__` (method, line 42) `def __init__(self, script_path)`
  - `_load_shell_with_deps` (method, line 48) `def _load_shell_with_deps(self)`
  - `execute_command` (method, line 84) `def execute_command(self, command)`
  - `get_available_commands` (method, line 110) `def get_available_commands(self)`
  - `__init__` (method, line 122) `def __init__(self, provider, mode, debug, script_path)`
  - `_load_model` (method, line 136) `def _load_model(self)`
  - `_setup_agent` (method, line 155) `def _setup_agent(self)`
  - `_register_pentesting_tools` (method, line 179) `def _register_pentesting_tools(self)`
  - `_register_fallback_tools` (method, line 207) `def _register_fallback_tools(self)`
  - `read_file_content` (method, line 213) `def read_file_content(self, file_path)`
  - `load_knowledge_base` (method, line 223) `def load_knowledge_base(self)`
  - `save_knowledge_base` (method, line 229) `def save_knowledge_base(self, kb)`
  - `get_relevant_knowledge` (method, line 233) `def get_relevant_knowledge(self, prompt)`
  - `add_to_knowledge_base` (method, line 238) `def add_to_knowledge_base(self, prompt, response)`
  - `process_with_context` (method, line 244) `def process_with_context(self, file_path, event)`
  - `_stream_response` (method, line 279) `def _stream_response(self, prompt)`
  - `run_cli_command` (method, line 188) `def run_cli_command(command)`
  - `read_file` (method, line 208) `def read_file(path)`
  - `generate` (method, line 280) `def generate()`
- Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/agent_tool.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`

## modules/vuln_bot_cli.py
- Layer: utility
- Language: py
- Symbols:
  - `parse_args` (function, line 8) `def parse_args()`
  - `main` (function, line 17) `def main()`
- Depends on: `modules/vulnbot.py`

## modules/vulnbot.py
- Doc: list_files: Lista archivos en un directorio
- Layer: presentation
- Language: py
- Symbols:
  - `VulnBotCLI` (class, line 28) `class VulnBotCLI`
  - `__init__` (method, line 29) `def __init__(self, provider, mode, debug, script_path)`
  - `_load_model` (method, line 44) `def _load_model(self)`
  - `_setup_agent` (method, line 59) `def _setup_agent(self, script_path)`
  - `_register_file_tools` (method, line 81) `def _register_file_tools(self)`
  - `_load_external_tools` (method, line 107) `def _load_external_tools(self, script_path)`
  - `_stream_agent_response` (method, line 133) `def _stream_agent_response(self, prompt)`
  - `load_knowledge_base` (method, line 140) `def load_knowledge_base(self)`
  - `save_knowledge_base` (method, line 146) `def save_knowledge_base(self, kb)`
  - `get_relevant_knowledge` (method, line 150) `def get_relevant_knowledge(self, prompt)`
  - `create_complex_prompt` (method, line 155) `def create_complex_prompt(self, base_prompt, history, knowledge)`
  - `read_file_content` (method, line 171) `def read_file_content(self, file_path)`
  - `load_event_config` (method, line 177) `def load_event_config(self)`
  - `process_with_context` (method, line 185) `def process_with_context(self, file_path, event)`
  - `stream_response` (method, line 201) `def stream_response(self, prompt)`
  - `add_to_knowledge_base` (method, line 207) `def add_to_knowledge_base(self, prompt, response)`
  - `list_files` (method, line 84) `def list_files(directory)`
  - `read_file` (method, line 88) `def read_file(path)`
  - `edit_file` (method, line 93) `def edit_file(path, content, old_text)`
  - `generate` (method, line 135) `def generate()`
  - `generate` (method, line 202) `def generate()`
- Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
- Imported by: `modules/vuln_bot_cli.py`

## modules/websocket_beacon.py
- Doc: WebSocket beacon transport for modern C2 channels.
- Layer: utility
- Language: py
- Symbols:
  - `WebSocketBeacon` (class, line 46) `class WebSocketBeacon`
  - `WebSocketC2Handler` (class, line 274) `class WebSocketC2Handler`
  - `__init__` (method, line 62) `def __init__(self, server_url, beacon_id, encryption_key, sleep_seconds, jitter_percent, ssl_verify, proxy)`
  - `_encrypt` (method, line 91) `def _encrypt(self, data)`
  - `_decrypt` (method, line 97) `def _decrypt(self, data)`
  - `_build_message` (method, line 103) `def _build_message(self, msg_type, payload)`
  - `_jittered_sleep` (method, line 114) `def _jittered_sleep(self)`
  - `connect` (method, line 122) `def connect(self)`
  - `check_in` (method, line 157) `def check_in(self)`
  - `send_result` (method, line 191) `def send_result(self, task_id, output, exit_code)`
  - `run` (method, line 214) `def run(self, command_handler)`
  - `shutdown` (method, line 263) `def shutdown(self)`
  - `__init__` (method, line 288) `def __init__(self, host, port, ssl_context, beacon_callback, task_callback, result_callback)`
  - `_handle_connection` (method, line 310) `def _handle_connection(self, websocket, path)`
  - `start` (method, line 382) `def start(self)`
  - `stop` (method, line 392) `def stop(self)`
  - `start_in_thread` (method, line 399) `def start_in_thread(self)`
  - `_run_loop` (method, line 410) `def _run_loop(self, loop)`
  - `send_task` (method, line 416) `def send_task(self, beacon_id, command)`
  - `list_beacons` (method, line 447) `def list_beacons(self)`
  - `remove_stale_beacons` (method, line 464) `def remove_stale_beacons(self, timeout)`
- Depends on: `core/hardening.py`

## modules/wineconfig.sh
- Layer: utility
- Language: sh

## modules/world_model.py
- Doc: modules/world_model.py
- Layer: business_logic
- Language: py
- Symbols:
  - `_derive_crypto_key` (function, line 58) `def _derive_crypto_key(password, salt)`
  - `_master_password` (function, line 69) `def _master_password()`
  - `read_state_dict` (function, line 74) `def read_state_dict(path)`
  - `write_state_dict` (function, line 119) `def write_state_dict(path, data)`
  - `HostState` (class, line 152) `class HostState(StrEnum)`
  - `EngagementPhase` (class, line 168) `class EngagementPhase(StrEnum)`
  - `ServiceInfo` (class, line 180) `class ServiceInfo`
  - `CredentialEntry` (class, line 189) `class CredentialEntry`
  - `VulnerabilityEntry` (class, line 198) `class VulnerabilityEntry`
  - `EmailEntry` (class, line 207) `class EmailEntry`
  - `DomainEntry` (class, line 215) `class DomainEntry`
  - `NetworkRelation` (class, line 223) `class NetworkRelation`
  - `NetworkGraph` (class, line 245) `class NetworkGraph`
  - `HostEntry` (class, line 365) `class HostEntry`
  - `_PhaseDeriver` (class, line 417) `class _PhaseDeriver`
  - `WorldModel` (class, line 509) `class WorldModel`
  - `get_world_model` (method, line 1090) `def get_world_model(path)`
  - `rank` (method, line 161) `def rank(self)`
  - `can_advance_to` (method, line 164) `def can_advance_to(self, next_state)`
  - `__init__` (method, line 268) `def __init__(self)`
  - `add_relation` (method, line 275) `def add_relation(self, relation)`
  - `neighbors` (method, line 283) `def neighbors(self, node)`
  - `in_degree` (method, line 287) `def in_degree(self, node)`
  - `out_degree` (method, line 291) `def out_degree(self, node)`
  - `degree_centrality` (method, line 295) `def degree_centrality(self)`
  - `pivot_candidates` (method, line 310) `def pivot_candidates(self, top_k)`
  - `to_dict` (method, line 332) `def to_dict(self)`
  - `from_dict` (method, line 349) `def from_dict(cls, data)`
  - `add_service` (method, line 374) `def add_service(self, svc)`
  - `advance` (method, line 378) `def advance(self, new_state)`
  - `to_dict` (method, line 386) `def to_dict(self)`
  - `from_dict` (method, line 398) `def from_dict(cls, d)`
  - `derive` (method, line 431) `def derive(self, hosts)`
  - `__init__` (method, line 517) `def __init__(self, path)`
  - `add_host` (method, line 533) `def add_host(self, ip)`
  - `reset_host` (method, line 541) `def reset_host(self, ip)`
  - `advance_host` (method, line 551) `def advance_host(self, ip, new_state)`
  - `add_service` (method, line 560) `def add_service(self, ip, port, name, version, protocol)`
  - `add_note` (method, line 577) `def add_note(self, ip, note)`
  - `set_os_hint` (method, line 584) `def set_os_hint(self, ip, os_hint)`
  - `get_host` (method, line 598) `def get_host(self, ip)`
  - `get_hosts_summary` (method, line 610) `def get_hosts_summary(self)`
  - `add_credential` (method, line 621) `def add_credential(self, value, host, service)`
  - `link_credential_to_success` (method, line 653) `def link_credential_to_success(self, value, host)`
  - `link_credential_to_failure` (method, line 674) `def link_credential_to_failure(self, value, host)`
  - `add_vulnerability` (method, line 704) `def add_vulnerability(self, description, host, cve, severity)`
  - `add_email` (method, line 710) `def add_email(self, address, host, context)`
  - `add_domain` (method, line 716) `def add_domain(self, domain, host, context)`
  - `update_from_findings` (method, line 730) `def update_from_findings(self, findings)`
  - `consume_policy_facts` (method, line 803) `def consume_policy_facts(self, facts_path)`
  - `add_relation` (method, line 895) `def add_relation(self, source, target, relation, weight)`
  - `pivot_candidates` (method, line 916) `def pivot_candidates(self, top_k)`
  - `graph_snapshot` (method, line 924) `def graph_snapshot(self)`
  - `get_phase` (method, line 931) `def get_phase(self)`
  - `get_suggested_tools` (method, line 935) `def get_suggested_tools(self)`
  - `to_context_string` (method, line 938) `def to_context_string(self)`
  - `_save` (method, line 998) `def _save(self)`
  - `_load` (method, line 1018) `def _load(self)`
  - `reload` (method, line 1042) `def reload(self)`
  - `reset` (method, line 1058) `def reset(self)`
  - `snapshot` (method, line 1069) `def snapshot(self)`
- Depends on: `cli/commands/enum.py`, `core/logging.py`
- Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/pwn.py`, `cli/ops_commands.py`, `lazyc2.py`, `modules/exploit_recommender.py`, `modules/integrations/nuclei_parser.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/live_surface.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/state_manager.py`, `modules/unified_dashboard.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified.py`, `tests/test_killchain_unified_v2.py`, `tests/test_moe_rl_swan.py`, `tests/test_ops_loot_phase.py`, `tests/test_phase1_data_gaps.py`, `tests/test_world_model_extended.py`

## modules/yaml_generator.py
- Doc: load_payload: Carga las variables desde payload.json
- Layer: utility
- Language: py
- Symbols:
  - `YAMLPromptGenerator` (class, line 17) `class YAMLPromptGenerator`
  - `main` (method, line 140) `def main()`
  - `__init__` (method, line 18) `def __init__(self, provider, api_key)`
  - `load_payload` (method, line 25) `def load_payload(self)`
  - `_load_model` (method, line 32) `def _load_model(self)`
  - `generate_prompt` (method, line 54) `def generate_prompt(self, user_request)`
  - `extract_yaml_from_markdown` (method, line 100) `def extract_yaml_from_markdown(self, text)`
  - `create_yaml_addon` (method, line 109) `def create_yaml_addon(self, user_request, output_dir)`
- Depends on: `modules/ai_model.py`, `modules/llm_factory.py`

## modules/yara_scanner.py
- Doc: YARA integration for malware classification and IOC scanning.
- Layer: utility
- Language: py
- Symbols:
  - `YaraScanner` (class, line 22) `class YaraScanner`
  - `create_default_rules` (method, line 366) `def create_default_rules()`
  - `__init__` (method, line 30) `def __init__(self, rules_dir, auto_compile)`
  - `ensure_directory` (method, line 40) `def ensure_directory(self)`
  - `_load_external_vars` (method, line 44) `def _load_external_vars(self)`
  - `compile_all` (method, line 53) `def compile_all(self)`
  - `scan_file` (method, line 97) `def scan_file(self, filepath, timeout)`
  - `_scan_with_timeout` (method, line 129) `def _scan_with_timeout(self, filepath, externals, timeout)`
  - `_format_match` (method, line 162) `def _format_match(self, match)`
  - `scan_directory` (method, line 186) `def scan_directory(self, directory, recursive, extensions, max_files)`
  - `_sha256` (method, line 247) `def _sha256(filepath)`
  - `add_rule` (method, line 255) `def add_rule(self, name, content)`
  - `list_rules` (method, line 274) `def list_rules(self)`
  - `download_community_rules` (method, line 295) `def download_community_rules(self)`
  - `ioc_scan` (method, line 327) `def ioc_scan(self, target_path, iocs)`
  - `target` (method, line 137) `def target()`
- Imported by: `cli/commands/postexp_migrated.py`, `modules/intelligence_engine.py`

