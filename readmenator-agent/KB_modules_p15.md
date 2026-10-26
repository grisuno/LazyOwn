# Subsystem: modules (page 15 of 16)
Previous: [KB_modules_p14.md](KB_modules_p14.md)

## modules/stego_video.py
- Doc: Video steganography addon for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `load_payload_file` (function, line 26) `def load_payload_file()`
  - `is_zip` (function, line 36) `def is_zip(path)`
  - `is_video` (function, line 40) `def is_video(path)`
  - `prompt_path` (function, line 44) `def prompt_path(message)`
  - `resolve_path` (function, line 52) `def resolve_path(arg_path, payload_file, validator, kind)`
  - `generate_carrier` (function, line 61) `def generate_carrier(output)`
  - `encode` (function, line 75) `def encode(zip_path, output_video)`
  - `decode` (function, line 93) `def decode(stego_video, output_zip)`
  - `default_output` (function, line 113) `def default_output(zip_path)`
  - `main` (function, line 118) `def main(argv)`

## modules/sudo_tiocsti.py
- Doc: – Production‑grade TIOCSTI injection with multiple attack modes.
- Layer: utility
- Language: py
- Symbols:
  - `get_controlling_tty` (function, line 52) `def get_controlling_tty()`
  - `inject_byte` (function, line 64) `def inject_byte(fd, byte_char)`
  - `inject_payload` (function, line 79) `def inject_payload(fd, payload, char_delay)`
  - `get_sudo_pids_on_tty` (function, line 102) `def get_sudo_pids_on_tty(tty_path)`
  - `sudo_cache_valid` (function, line 139) `def sudo_cache_valid()`
  - `mode_poll` (function, line 149) `def mode_poll(fd, tty_path)`
  - `mode_prefill` (function, line 175) `def mode_prefill(fd)`
  - `mode_cache` (function, line 185) `def mode_cache(fd)`
  - `main` (function, line 198) `def main()`
- Depends on: `core/logging.py`

## modules/surface_ops.py
- Doc: Pure attack-surface helpers (no cmd2): discovery targets, confirm parsing.
- Layer: utility
- Language: py
- Symbols:
  - `is_ipv4` (function, line 18) `def is_ipv4(value)`
  - `parse_confirm` (function, line 26) `def parse_confirm(answer)`
  - `discovery_targets` (function, line 31) `def discovery_targets(sessions_dir)`
  - `write_world_model_hosts` (function, line 50) `def write_world_model_hosts(document, sessions)`
- Depends on: `modules/world_model.py`
- Imported by: `cli/commands/surface.py`, `tests/test_estorides_fusion.py`

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
  - `get_builder` (function, line 592) `def get_builder()`
  - `build` (method, line 270) `def build(self)`
  - `load` (method, line 293) `def load(self)`
  - `_load_csv` (method, line 305) `def _load_csv(self)`
  - `_build_assets` (method, line 318) `def _build_assets(self, rows)`
  - `_risk_score` (method, line 352) `def _risk_score(self, commands, ports)`
  - `_compromise_indicators` (method, line 388) `def _compromise_indicators(self, commands)`
  - `_build_ttps` (method, line 404) `def _build_ttps(self, rows)`
  - `_build_iocs` (method, line 444) `def _build_iocs(self, rows)`
  - `_build_detection_rules` (method, line 475) `def _build_detection_rules(self, ttps)`
  - `_build_purple_team` (method, line 505) `def _build_purple_team(self, ttps, detection_rules)`
  - `_build_summary` (method, line 560) `def _build_summary(self, rows, assets, ttps)`
  - `_save` (method, line 578) `def _save(self, model)`
  - `_add` (function, line 448) `def _add(ioc)`
- Depends on: `core/logging.py`
- Imported by: `cli/commands/mcp_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`

## modules/timeline_narrator.py
- Doc: LazyOwn Timeline Narrator
- Layer: utility
- Language: py
- Symbols:
  - `_load_events` (function, line 57) `def _load_events(n)`
  - `_format_events_for_prompt` (function, line 77) `def _format_events_for_prompt(events)`
  - `_call_ai` (function, line 97) `def _call_ai(api_key, events_text, target)`
  - `_write_timeline` (function, line 115) `def _write_timeline(narrative, event_count, target)`
  - `narrate` (function, line 130) `def narrate(api_key, force)`
  - `load_timeline` (function, line 165) `def load_timeline()`
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
  - `summary` (method, line 326) `def summary(self)`
- Imported by: `cli/commands/opsec_cleanup.py`

## modules/tmp.sh
- Layer: utility
- Language: sh

## modules/toolset.py
- Doc: Typed tool sets per agent role with shell allowlists.
- Layer: utility
- Language: py
- Symbols:
  - `ToolSeed` (class, line 27) `class ToolSeed`
  - `builtin_seeds` (function, line 35) `def builtin_seeds()`
  - `resolve` (function, line 72) `def resolve(agent, tool_key)`
  - `extract_tool` (function, line 105) `def extract_tool(command)`
  - `validate_shell` (function, line 128) `def validate_shell(role, command)`
- Imported by: `skills/autonomous_daemon.py`

## modules/toposwarm_bridge.py
- Doc: modules/toposwarm_bridge.py
- Layer: utility
- Language: py
- Symbols:
  - `RoutedCall` (class, line 71) `class RoutedCall`
  - `_keyword_route` (function, line 202) `def _keyword_route(prompt)`
  - `_load_toposwarm_modules` (function, line 241) `def _load_toposwarm_modules()`
  - `OnlineFeedbackLoop` (class, line 273) `class OnlineFeedbackLoop`
  - `TopoSwarmBridge` (class, line 424) `class TopoSwarmBridge`
  - `get_bridge` (function, line 645) `def get_bridge()`
  - `lazyown_command` (method, line 81) `def lazyown_command(self)`
  - `__init__` (method, line 296) `def __init__(self, maxsize)`
  - `register` (method, line 303) `def register(self, result, hidden)`
  - `feedback` (method, line 318) `def feedback(self, result_id, good, comment, routing_head)`
  - `pending_count` (method, line 379) `def pending_count(self)`
  - `stats` (method, line 382) `def stats(self)`
  - `load_feedback_for_training` (method, line 389) `def load_feedback_for_training(self)`
  - `__init__` (method, line 432) `def __init__(self)`
  - `available` (method, line 444) `def available(self)`
  - `model_loaded` (method, line 449) `def model_loaded(self)`
  - `_try_load` (method, line 452) `def _try_load(self)`
  - `_neural_route` (method, line 493) `def _neural_route(self, prompt)`
  - `feedback` (method, line 562) `def feedback(self, result_id, good, comment)`
  - `route` (method, line 586) `def route(self, prompt)`
  - `execute_via_orchestrator` (method, line 613) `def execute_via_orchestrator(self, prompt, no_model)`
  - `_hook` (function, line 508) `def _hook(m, i, o)`
- Depends on: `core/logging.py`
- Imported by: `modules/ai_fallback.py`, `modules/hive_invoke.py`, `modules/llm_factory.py`, `modules/moe_router.py`, `modules/unified_bridge.py`, `skills/toposwarm_autonomous.py`

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

## modules/traffic_recorder.py
- Doc: HTTP traffic recorder with file-tree storage and SQLite index.
- Layer: utility
- Language: py
- Symbols:
  - `RecorderConfig` (class, line 24) `class RecorderConfig`
  - `url_template` (function, line 69) `def url_template(url)`
  - `Exchange` (class, line 80) `class Exchange`
  - `TrafficRecorder` (class, line 91) `class TrafficRecorder`
  - `__init__` (method, line 94) `def __init__(self, base_dir)`
  - `_migrate_fts` (method, line 115) `def _migrate_fts(self, conn)`
  - `_connect` (method, line 132) `def _connect(self)`
  - `record` (method, line 138) `def record(self, method, url, status, req_body, resp_body, content_type, req_headers, resp_headers, host, port...`
  - `since` (method, line 230) `def since(self, rowid, limit)`
  - `latest_rowid` (method, line 247) `def latest_rowid(self)`
  - `query` (method, line 253) `def query(self, host, status, limit, offset, task)`
  - `get_body` (method, line 275) `def get_body(self, exchange_id)`
  - `read_body` (method, line 284) `def read_body(self, exchange_id, part, offset, length)`
  - `count` (method, line 317) `def count(self)`
  - `_index_fts` (method, line 323) `def _index_fts(self, exchange_id, req, resp)`
  - `backfill_fts` (method, line 343) `def backfill_fts(self, batch)`
  - `_fts_query` (method, line 375) `def _fts_query(query)`
  - `search_body` (method, line 382) `def search_body(self, query, limit)`
  - `_scan_bodies` (method, line 422) `def _scan_bodies(self, needle, limit)`
  - `export_archive` (method, line 451) `def export_archive(self, path, limit, task)`
  - `import_archive` (method, line 493) `def import_archive(self, path)`
  - `import_inbox` (method, line 554) `def import_inbox(self, inbox_dir)`
  - `gc` (method, line 587) `def gc(self, older_than_sec)`
- Imported by: `cli/commands/lazyops.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_gates.py`, `tests/test_lazy_bridge_traffic.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_proxy.py`, `tests/test_safety_gates.py`

## modules/trigger_policy.py
- Doc: Declarative trigger policy: YAML seeds for the loop TriggerStore.
- Layer: business_logic
- Language: py
- Symbols:
  - `TriggerPolicyConfig` (class, line 31) `class TriggerPolicyConfig`
  - `validate_triggers` (function, line 40) `def validate_triggers(raw)`
  - `_coerce_every_sec` (function, line 79) `def _coerce_every_sec(value)`
  - `seeds` (function, line 87) `def seeds(raw)`
  - `read_policy` (function, line 120) `def read_policy(path)`
  - `seed_store` (function, line 146) `def seed_store(policy, store, task_id)`
  - `export_store` (function, line 171) `def export_store(task_id)`
  - `remove_seed` (function, line 185) `def remove_seed(kind, arg, task_id)`
- Depends on: `core/logging.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`
- Imported by: `cli/orchestrator_assets_tabs.py`, `cli/session_brief.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_loop.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`, `tests/test_orchestrator_api.py`, `tests/test_orchestrator_triggers.py`

## modules/ttp_coverage.py
- Doc: TTP coverage matrix — real-time MITRE ATT&CK technique tracking.
- Layer: utility
- Language: py
- Symbols:
  - `TTPRow` (class, line 55) `class TTPRow`
  - `TTPCoverage` (class, line 65) `class TTPCoverage`
  - `get_coverage` (function, line 260) `def get_coverage()`
  - `__init__` (method, line 68) `def __init__(self)`
  - `rebuild_from_operations` (method, line 76) `def rebuild_from_operations(self)`
  - `add` (method, line 125) `def add(self, technique_id, name, tactic, status, operation_id)`
  - `compute_ready` (method, line 149) `def compute_ready(self, available_facts)`
  - `_blocking_facts` (method, line 168) `def _blocking_facts(self, tactic)`
  - `matrix` (method, line 190) `def matrix(self)`
  - `status_by_id` (method, line 231) `def status_by_id(self, technique_id)`
  - `to_dict` (method, line 234) `def to_dict(self)`
  - `_save_state` (method, line 241) `def _save_state(self)`
  - `_load_state` (method, line 248) `def _load_state(self)`
- Depends on: `core/logging.py`
- Imported by: `cli/commands/caldera.py`

## modules/ttpscope_bridge.py
- Doc: Secure bridge for the TTPScope MITRE ATT&CK research client.
- Layer: utility
- Language: py
- Symbols:
  - `locate_binary` (function, line 82) `def locate_binary()`
  - `validate_object_id` (function, line 92) `def validate_object_id(raw)`
  - `validate_query` (function, line 100) `def validate_query(raw)`
  - `validate_platform` (function, line 112) `def validate_platform(raw)`
  - `_slug` (function, line 123) `def _slug(text)`
  - `_run_ttpscope` (function, line 129) `def _run_ttpscope(args)`
  - `_cache_dataset_path` (function, line 146) `def _cache_dataset_path()`
  - `_fallback_sync` (function, line 153) `def _fallback_sync()`
  - `_load_stix_bundle` (function, line 193) `def _load_stix_bundle()`
  - `_stix_external_id` (function, line 211) `def _stix_external_id(obj)`
  - `_stix_index` (function, line 219) `def _stix_index(bundle)`
  - `_fallback_search_bundle` (function, line 235) `def _fallback_search_bundle(query, limit)`
  - `_load_parquet` (function, line 259) `def _load_parquet(name)`
  - `_load_atomic_parquet` (function, line 273) `def _load_atomic_parquet()`
  - `_fallback_search_parquet` (function, line 282) `def _fallback_search_parquet(query, limit)`
  - `_fallback_show_bundle` (function, line 303) `def _fallback_show_bundle(object_id)`
  - `_fallback_show_parquet` (function, line 350) `def _fallback_show_parquet(object_id)`
  - `_fallback_matrix_bundle` (function, line 384) `def _fallback_matrix_bundle(platform)`
  - `_notes_dir` (function, line 415) `def _notes_dir()`
  - `_fallback_note` (function, line 422) `def _fallback_note(object_id, text)`
  - `_fallback_notes` (function, line 442) `def _fallback_notes(object_id)`
  - `_fallback_matrix_parquet` (function, line 453) `def _fallback_matrix_parquet(platform)`
  - `_stage` (function, line 485) `def _stage(action, slug, stdout, extra)`
  - `do_sync` (function, line 497) `def do_sync()`
  - `do_search` (function, line 508) `def do_search(query)`
  - `do_show` (function, line 520) `def do_show(object_id)`
  - `do_matrix` (function, line 535) `def do_matrix(platform)`
  - `do_note` (function, line 551) `def do_note(object_id, text)`
  - `do_notes` (function, line 570) `def do_notes(object_id)`
  - `do_chain` (function, line 582) `def do_chain(object_id, platform, limit)`
  - `run_action` (function, line 652) `def run_action(action)`
  - `main` (function, line 679) `def main()`
  - `_as_list` (function, line 460) `def _as_list(value)`
- Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/atomic_resolver.py`, `skills/lazyown_parquet_db.py`
- Imported by: `skills/lazyown_mcp.py`

## modules/unified_bridge.py
- Doc: UnifiedBridge — single API over all LazyOwn bridges and routing engines.
- Layer: utility
- Language: py
- Symbols:
  - `RouteResult` (class, line 46) `class RouteResult`
  - `DelegateResult` (class, line 59) `class DelegateResult`
  - `RouteBackend` (class, line 67) `class RouteBackend(ABC)`
  - `KeywordBackend` (class, line 75) `class KeywordBackend(RouteBackend)`
  - `LazyownBridgeBackend` (class, line 123) `class LazyownBridgeBackend(RouteBackend)`
  - `TopoSwarmBackend` (class, line 161) `class TopoSwarmBackend(RouteBackend)`
  - `UnifiedBridge` (class, line 195) `class UnifiedBridge`
  - `route_prompt` (function, line 483) `def route_prompt(prompt, context)`
  - `delegate_task` (function, line 488) `def delegate_task(goal, backend)`
  - `available` (method, line 69) `def available(self)`
  - `route` (method, line 72) `def route(self, prompt, context)`
  - `available` (method, line 102) `def available(self)`
  - `route` (method, line 105) `def route(self, prompt, context)`
  - `available` (method, line 126) `def available(self)`
  - `route` (method, line 134) `def route(self, prompt, context)`
  - `available` (method, line 164) `def available(self)`
  - `route` (method, line 173) `def route(self, prompt, context)`
  - `__init__` (method, line 214) `def __init__(self)`
  - `_init_backends` (method, line 219) `def _init_backends(self)`
  - `get` (method, line 225) `def get(cls)`
  - `set_publish_callback` (method, line 230) `def set_publish_callback(self, cb)`
  - `_publish` (method, line 233) `def _publish(self, category, event_type, payload)`
  - `route` (method, line 253) `def route(self, prompt, context)`
  - `delegate` (method, line 300) `def delegate(self, goal, backend, timeout, max_iterations)`
  - `_await_agent` (method, line 355) `def _await_agent(self, get_status, agent_id, timeout)`
  - `_run_agent_command` (method, line 384) `def _run_agent_command(self, command)`
  - `list_backends` (method, line 461) `def list_backends(self)`
  - `_detect_phase` (method, line 464) `def _detect_phase(self)`
  - `_get_active_target` (method, line 473) `def _get_active_target(self)`
- Depends on: `core/logging.py`, `modules/event_bus.py`, `modules/lazyown_bridge.py`, `modules/mcp_agent_bridge.py`, `modules/state_manager.py`, `modules/toposwarm_bridge.py`
- Imported by: `lazyown.py`

## modules/unified_dashboard.py
- Doc: Unified campaign dashboard — combines all state sources into one view.
- Layer: utility
- Language: py
- Symbols:
  - `UnifiedDashboard` (class, line 37) `class UnifiedDashboard`
  - `get_unified_dashboard` (function, line 256) `def get_unified_dashboard(sessions_dir)`
  - `__init__` (method, line 44) `def __init__(self, sessions_dir)`
  - `_get_dashboard` (method, line 49) `def _get_dashboard(self)`
  - `_get_graph` (method, line 65) `def _get_graph(self)`
  - `build_unified_snapshot` (method, line 76) `def build_unified_snapshot(self)`
  - `_collect_world_model` (method, line 95) `def _collect_world_model(self)`
  - `_collect_hive_status` (method, line 101) `def _collect_hive_status(self)`
  - `_collect_policy_status` (method, line 111) `def _collect_policy_status(self)`
  - `_collect_daemon_status` (method, line 121) `def _collect_daemon_status(self)`
  - `_collect_live_graph` (method, line 130) `def _collect_live_graph(self)`
  - `_collect_graph_advice` (method, line 142) `def _collect_graph_advice(self)`
  - `_collect_dashboard` (method, line 160) `def _collect_dashboard(self)`
  - `render_unified` (method, line 170) `def render_unified(self)`
  - `export_json` (method, line 251) `def export_json(self)`
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
  - `getUUID` (function, line 38) `def getUUID()`
  - `getSystemInfo` (function, line 66) `def getSystemInfo(output_file)`
  - `getVTResult` (function, line 83) `def getVTResult(fileHash)`
  - `getHash` (function, line 112) `def getHash(file, ignoreVFlag)`
  - `checkSignature` (function, line 132) `def checkSignature(file, bundle)`
  - `datetime_handler` (function, line 210) `def datetime_handler(x)`
  - `parseAgentsDaemons` (function, line 215) `def parseAgentsDaemons(item, path)`
  - `getLaunchAgents` (function, line 287) `def getLaunchAgents(path, output_file, ignoreVFlag)`
  - `getLaunchDaemons` (function, line 302) `def getLaunchDaemons(path, output_file, ignoreVFlag)`
  - `getUsers` (function, line 317) `def getUsers(output_file)`
  - `getSafariExtensions` (function, line 338) `def getSafariExtensions(path, output_file)`
  - `getChromeExtensions` (function, line 357) `def getChromeExtensions(path, output_file)`
  - `getChromeDownloads` (function, line 388) `def getChromeDownloads(chromeHistoryDbPath, output_file)`
  - `getFirefoxExtensions` (function, line 442) `def getFirefoxExtensions(path, output_file)`
  - `getInstallHistory` (function, line 477) `def getInstallHistory(output_file)`
  - `getCronJobs` (function, line 494) `def getCronJobs(users, output_file)`
  - `getEmond` (function, line 513) `def getEmond(output_file)`
  - `getKext` (function, line 530) `def getKext(sipStatus, kextPath, output_file, ignoreVFlag)`
  - `getEnv` (function, line 577) `def getEnv(output_file)`
  - `getPeriodicScripts` (function, line 592) `def getPeriodicScripts(output_file)`
  - `getConnections` (function, line 609) `def getConnections(output_file)`
  - `SIPStatus` (function, line 637) `def SIPStatus(output_file)`
  - `GatekeeperStatus` (function, line 651) `def GatekeeperStatus(output_file)`
  - `parseApp` (function, line 663) `def parseApp(app, ignoreVFlag)`
  - `getLoginItems` (function, line 706) `def getLoginItems(path, output_file, ignoreVFlag)`
  - `getApps` (function, line 741) `def getApps(path, output_file, ignoreVFlag)`
  - `getEventTaps` (function, line 763) `def getEventTaps(output_file)`
  - `getBashHistory` (function, line 786) `def getBashHistory(output_file, users)`
  - `getShellStartupScripts` (function, line 804) `def getShellStartupScripts(users, output_file)`
  - `hmac_sha256` (function, line 842) `def hmac_sha256(key, data)`
  - `amzn_sig` (function, line 846) `def amzn_sig(secret_access_key, data, aws_region, aws_service)`
  - `amzn_canonical_req` (function, line 856) `def amzn_canonical_req(filename_path, headers_list)`
  - `s3_upload` (function, line 866) `def s3_upload(data, content_type, filename_path, access_key_id, secret_access_key, s3_bucket, aws_region)`
  - `io_key` (function, line 49) `def io_key(keyname)`

## modules/verb_catalog.py
- Doc: Operator-owned YAML catalog of every routable shell verb.
- Layer: utility
- Language: py
- Symbols:
  - `VerbCatalogConfig` (class, line 76) `class VerbCatalogConfig`
  - `_default_config` (function, line 99) `def _default_config()`
  - `_builtin_names` (function, line 105) `def _builtin_names()`
  - `_phase_fallback` (function, line 117) `def _phase_fallback(verb)`
  - `_risk_fallback` (function, line 127) `def _risk_fallback(verb)`
  - `_addon_discoveries` (function, line 137) `def _addon_discoveries(config)`
  - `_all_discoveries` (function, line 181) `def _all_discoveries(config)`
  - `index_commands` (function, line 190) `def index_commands(config)`
  - `validate_catalog` (function, line 230) `def validate_catalog(data)`
  - `load` (function, line 263) `def load(config)`
  - `entries` (function, line 296) `def entries(config)`
  - `catalog_enabled` (function, line 349) `def catalog_enabled(name, config)`
  - `catalog_source` (function, line 364) `def catalog_source(name, config)`
  - `set_enabled` (function, line 378) `def set_enabled(name, enabled, config)`
  - `sync` (function, line 415) `def sync(config)`
  - `_write` (function, line 470) `def _write(cfg, verbs)`
  - `_drop_cache` (function, line 494) `def _drop_cache(path_key)`
  - `stats` (function, line 502) `def stats(config)`
  - `search` (function, line 516) `def search(query, config, phase, enabled, limit)`
- Depends on: `core/logging.py`, `modules/auto_registry.py`, `modules/lazy_cli_bridge.py`
- Imported by: `cli/commands/verb_admin.py`, `cli/lazy_orchestrator.py`, `cli/session_brief.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_cli_bridge.py`, `modules/orchestrator_config.py`, `tests/test_loop_cli_catalog.py`, `tests/test_orchestrator_api.py`, `tests/test_session_brief.py`

## modules/verb_manifest.py
- Doc: Typed verb manifests - semantics for routable shell verbs.
- Layer: utility
- Language: py
- Symbols:
  - `ManifestCost` (class, line 93) `class ManifestCost`
  - `ManifestNoise` (class, line 108) `class ManifestNoise`
  - `FactPredicate` (class, line 123) `class FactPredicate`
  - `VerbManifest` (class, line 188) `class VerbManifest`
  - `parse_predicate` (function, line 222) `def parse_predicate(data)`
  - `_parse_cost` (function, line 254) `def _parse_cost(data)`
  - `_parse_noise` (function, line 276) `def _parse_noise(data)`
  - `parse_manifest` (function, line 296) `def parse_manifest(verb, data)`
  - `_load_document` (function, line 338) `def _load_document(path)`
  - `manifests` (function, line 371) `def manifests(path)`
  - `manifest_for` (function, line 396) `def manifest_for(verb, path)`
  - `facts_for_target` (function, line 411) `def facts_for_target(host)`
  - `plan_check` (function, line 467) `def plan_check(steps, tokens, path, facts)`
  - `coverage` (function, line 522) `def coverage(total_verbs, path)`
  - `args` (method, line 152) `def args(self)`
  - `is_wild` (method, line 156) `def is_wild(self, key)`
  - `matches` (method, line 161) `def matches(self, other)`
- Depends on: `core/logging.py`, `modules/chain_registry.py`, `modules/world_model.py`
- Imported by: `modules/chain_distill.py`, `modules/chain_runner.py`, `tests/test_verb_manifest.py`

## modules/vuln_bot_cli.py
- Layer: utility
- Language: py
- Symbols:
  - `parse_args` (function, line 10) `def parse_args()`
  - `main` (function, line 22) `def main()`
- Depends on: `modules/vulnbot.py`

## modules/vulnbot.py
- Doc: list_files: Lista archivos en un directorio
- Layer: presentation
- Language: py
- Symbols:
  - `VulnBotCLI` (class, line 29) `class VulnBotCLI`
  - `__init__` (method, line 30) `def __init__(self, provider, mode, debug, script_path)`
  - `_load_model` (method, line 46) `def _load_model(self)`
  - `_setup_agent` (method, line 61) `def _setup_agent(self, script_path)`
  - `_register_file_tools` (method, line 83) `def _register_file_tools(self)`
  - `_load_external_tools` (method, line 109) `def _load_external_tools(self, script_path)`
  - `_stream_agent_response` (method, line 136) `def _stream_agent_response(self, prompt)`
  - `load_knowledge_base` (method, line 145) `def load_knowledge_base(self)`
  - `save_knowledge_base` (method, line 151) `def save_knowledge_base(self, kb)`
  - `get_relevant_knowledge` (method, line 155) `def get_relevant_knowledge(self, prompt)`
  - `create_complex_prompt` (method, line 160) `def create_complex_prompt(self, base_prompt, history, knowledge)`
  - `read_file_content` (method, line 176) `def read_file_content(self, file_path)`
  - `load_event_config` (method, line 182) `def load_event_config(self)`
  - `process_with_context` (method, line 190) `def process_with_context(self, file_path, event)`
  - `stream_response` (method, line 206) `def stream_response(self, prompt)`
  - `add_to_knowledge_base` (method, line 212) `def add_to_knowledge_base(self, prompt, response)`
  - `list_files` (function, line 86) `def list_files(directory)`
  - `read_file` (function, line 90) `def read_file(path)`
  - `edit_file` (function, line 95) `def edit_file(path, content, old_text)`
  - `generate` (function, line 139) `def generate()`
  - `generate` (function, line 207) `def generate()`
- Depends on: `core/logging.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
- Imported by: `modules/vuln_bot_cli.py`


Next: [KB_modules_p16.md](KB_modules_p16.md)
