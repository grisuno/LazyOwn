# Subsystem: modules (page 13 of 14)
Previous: [KB_modules_p12.md](KB_modules_p12.md)

## modules/socks_proxy.py
- Doc: SOCKS5 proxy engine for tunneling traffic through LazyOwn beacons.
- Layer: utility
- Language: py
- Symbols:
  - `SocksAuthMethod` (class, line 65) `class SocksAuthMethod(IntEnum)`
  - `SocksCommand` (class, line 74) `class SocksCommand(IntEnum)`
  - `SocksAddressType` (class, line 82) `class SocksAddressType(IntEnum)`
  - `SocksReply` (class, line 90) `class SocksReply(IntEnum)`
  - `SocksSession` (class, line 120) `class SocksSession`
  - `SocksProxyConfig` (class, line 166) `class SocksProxyConfig`
  - `SocksValidator` (class, line 244) `class SocksValidator`
  - `SocksProxyEngine` (class, line 368) `class SocksProxyEngine`
  - `message` (method, line 103) `def message(self)`
  - `elapsed_seconds` (method, line 144) `def elapsed_seconds(self)`
  - `to_dict` (method, line 150) `def to_dict(self)`
  - `to_dict` (method, line 199) `def to_dict(self)`
  - `from_dict` (method, line 218) `def from_dict(cls, raw)`
  - `validate_config` (method, line 253) `def validate_config(config)`
  - `validate_request` (method, line 300) `def validate_request(command, address_type, host, port, config)`
  - `_check_access_control` (method, line 340) `def _check_access_control(host, port, config)`
  - `__init__` (method, line 381) `def __init__(self, config)`
  - `config` (method, line 387) `def config(self)`
  - `sessions` (method, line 392) `def sessions(self)`
  - `session_count` (method, line 397) `def session_count(self)`
  - `validate` (method, line 401) `def validate(self, config)`
  - `build_spec` (method, line 413) `def build_spec(self)`
  - `create_session` (method, line 436) `def create_session(self, session_id, target_host, target_port, beacon_client_id)`
  - `remove_session` (method, line 475) `def remove_session(self, session_id)`
  - `get_session` (method, line 482) `def get_session(self, session_id)`
  - `add_bytes` (method, line 486) `def add_bytes(self, session_id, sent, received)`
  - `cleanup_expired` (method, line 497) `def cleanup_expired(self)`
  - `list_sessions` (method, line 511) `def list_sessions(self)`
  - `_find_oldest_session` (method, line 515) `def _find_oldest_session(self)`
  - `from_dict` (method, line 522) `def from_dict(cls, raw)`
  - `from_payload` (method, line 528) `def from_payload(cls, payload)`
- Depends on: `cli/commands/enum.py`, `core/logging.py`
- Imported by: `cli/commands/socks_proxy.py`, `modules/beacon_config_builder.py`, `tests/test_socks_proxy.py`

## modules/staged_delivery.py
- Doc: Staged payload delivery — HTA, Office macros, LNK files, ISO/VHD packaging.
- Layer: utility
- Language: py
- Symbols:
  - `StageDeliveryConfig` (class, line 25) `class StageDeliveryConfig`
  - `StagedDeliveryFactory` (class, line 51) `class StagedDeliveryFactory`
  - `__init__` (method, line 83) `def __init__(self, config, output_dir)`
  - `_obfuscate_powershell` (method, line 88) `def _obfuscate_powershell(self, code)`
  - `_obfuscate_vbscript` (method, line 95) `def _obfuscate_vbscript(self, code)`
  - `_payload_command` (method, line 102) `def _payload_command(self)`
  - `generate_hta` (method, line 134) `def generate_hta(self)`
  - `generate_vba_macro` (method, line 171) `def generate_vba_macro(self)`
  - `generate_xlm_macro` (method, line 219) `def generate_xlm_macro(self)`
  - `generate_lnk` (method, line 237) `def generate_lnk(self)`
  - `generate_iso` (method, line 301) `def generate_iso(self, inner_files)`
  - `_build_primary_volume_descriptor` (method, line 336) `def _build_primary_volume_descriptor(self, files)`
  - `generate_vhd` (method, line 370) `def generate_vhd(self, inner_files)`
  - `generate_all` (method, line 420) `def generate_all(self)`
  - `generate_phishing_page` (method, line 460) `def generate_phishing_page(self, template)`
  - `_office365_phish` (method, line 476) `def _office365_phish(self)`
  - `_gmail_phish` (method, line 504) `def _gmail_phish(self)`
  - `_outlook_phish` (method, line 532) `def _outlook_phish(self)`
- Imported by: `cli/commands/payload_arsenal.py`

## modules/state_manager.py
- Doc: UnifiedStateManager — single source of truth for all LazyOwn campaign state.
- Layer: utility
- Language: py
- Symbols:
  - `_load_json` (function, line 43) `def _load_json(path)`
  - `_save_json` (function, line 53) `def _save_json(path, data)`
  - `HostSummary` (class, line 65) `class HostSummary`
  - `SessionSnapshot` (class, line 76) `class SessionSnapshot`
  - `StateManager` (class, line 92) `class StateManager`
  - `get_state_manager` (function, line 776) `def get_state_manager()`
  - `__init__` (method, line 107) `def __init__(self, db_path, sessions_dir, world_model_path, facts_path)`
  - `instance` (method, line 129) `def instance(cls)`
  - `db` (method, line 137) `def db(self)`
  - `workspace_id` (method, line 146) `def workspace_id(self)`
  - `_ensure_workspace` (method, line 151) `def _ensure_workspace(self)`
  - `set_payload` (method, line 165) `def set_payload(self, payload)`
  - `_publish` (method, line 169) `def _publish(self, category, event_type, payload)`
  - `_find_host` (method, line 184) `def _find_host(self, address)`
  - `_cred_list_for_host` (method, line 192) `def _cred_list_for_host(self, host_id)`
  - `_vuln_list_for_host` (method, line 197) `def _vuln_list_for_host(self, host_id)`
  - `close` (method, line 202) `def close(self)`
  - `add_host` (method, line 213) `def add_host(self, address, mac, hostname, os, state)`
  - `get_host` (method, line 236) `def get_host(self, address)`
  - `list_hosts` (method, line 245) `def list_hosts(self)`
  - `advance_host` (method, line 249) `def advance_host(self, address, new_state)`
  - `delete_host` (method, line 275) `def delete_host(self, address)`
  - `add_service` (method, line 287) `def add_service(self, host_address, port, protocol, name, product, version, state)`
  - `list_services` (method, line 319) `def list_services(self, host_address)`
  - `add_credential` (method, line 328) `def add_credential(self, host_address, username, password, realm, cred_type, origin)`
  - `list_credentials` (method, line 362) `def list_credentials(self, host_address)`
  - `add_vulnerability` (method, line 373) `def add_vulnerability(self, host_address, name, severity, description, refs)`
  - `list_vulnerabilities` (method, line 398) `def list_vulnerabilities(self, host_address, severity)`
  - `add_loot` (method, line 411) `def add_loot(self, name, loot_type, path, notes, host_address)`
  - `list_loot` (method, line 444) `def list_loot(self)`
  - `add_note` (method, line 450) `def add_note(self, data, note_type, host_address)`
  - `list_notes` (method, line 473) `def list_notes(self)`
  - `import_nmap_xml` (method, line 479) `def import_nmap_xml(self, xml_path)`
  - `import_nmap_from_facts` (method, line 495) `def import_nmap_from_facts(self, facts)`
  - `status` (method, line 550) `def status(self)`
  - `_sync_world_model_cache` (method, line 556) `def _sync_world_model_cache(self)`
  - `get_world_model_cache` (method, line 606) `def get_world_model_cache(self)`
  - `load_world_model` (method, line 612) `def load_world_model(self)`
  - `session_snapshot` (method, line 653) `def session_snapshot(self)`
  - `export_csv` (method, line 757) `def export_csv(self, table)`
  - `export_summary` (method, line 761) `def export_summary(self)`
- Depends on: `core/logging.py`, `modules/db.py`, `modules/event_bus.py`, `modules/world_model.py`
- Imported by: `cli/commands/automation.py`, `lazyc2.py`, `lazyc2/blueprints/beacon.py`, `lazyown.py`, `modules/conditional_hooks.py`, `modules/event_consumers.py`, `modules/unified_bridge.py`

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
- Imported by: `cli/commands/surface.py`, `tests/test_estorides_fusion.py`

## modules/tel.py
- Doc: to_numbers: Simula la función toNumbers de JavaScript
- Layer: utility
- Language: py
- Symbols:
  - `get_machine_id` (function, line 10) `def get_machine_id()`
  - `get_version` (function, line 24) `def get_version()`
  - `to_numbers` (function, line 36) `def to_numbers(hex_str)`
  - `to_hex` (function, line 41) `def to_hex(byte_list)`
  - `decrypt_cookie` (function, line 46) `def decrypt_cookie(encrypted, key, iv)`
  - `main` (function, line 53) `def main()`

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
- Imported by: `cli/commands/lazyops.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_gates.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_proxy.py`, `tests/test_safety_gates.py`

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
  - `get_unified_dashboard` (function, line 259) `def get_unified_dashboard(sessions_dir)`
  - `__init__` (method, line 44) `def __init__(self, sessions_dir)`
  - `_get_dashboard` (method, line 49) `def _get_dashboard(self)`
  - `_get_graph` (method, line 65) `def _get_graph(self)`
  - `build_unified_snapshot` (method, line 76) `def build_unified_snapshot(self)`
  - `_collect_world_model` (method, line 95) `def _collect_world_model(self)`
  - `_collect_hive_status` (method, line 104) `def _collect_hive_status(self)`
  - `_collect_policy_status` (method, line 114) `def _collect_policy_status(self)`
  - `_collect_daemon_status` (method, line 124) `def _collect_daemon_status(self)`
  - `_collect_live_graph` (method, line 133) `def _collect_live_graph(self)`
  - `_collect_graph_advice` (method, line 145) `def _collect_graph_advice(self)`
  - `_collect_dashboard` (method, line 163) `def _collect_dashboard(self)`
  - `render_unified` (method, line 173) `def render_unified(self)`
  - `export_json` (method, line 254) `def export_json(self)`
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


Next: [KB_modules_p14.md](KB_modules_p14.md)
