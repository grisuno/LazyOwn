# Subsystem: modules (page 4 of 16)
Previous: [KB_modules_p3.md](KB_modules_p3.md)

## modules/ctf_capture.py
- Doc: CTF capture verification for gym attack paths.
- Layer: utility
- Language: py
- Symbols:
  - `output_dir` (function, line 32) `def output_dir(sessions_dir)`
  - `_check_root_shell` (function, line 45) `def _check_root_shell(output)`
  - `_check_shadow_dump` (function, line 58) `def _check_shadow_dump(output)`
  - `_check_credentials` (function, line 78) `def _check_credentials(output)`
  - `_check_windows_os_enum` (function, line 96) `def _check_windows_os_enum(output)`
  - `_check_defense_report` (function, line 115) `def _check_defense_report(output)`
  - `_check_eventlog_rows` (function, line 128) `def _check_eventlog_rows(output)`
  - `capture` (function, line 151) `def capture(vuln_id, target, output, sessions_dir, catalogue)`
  - `_publish_capture_outcome` (function, line 209) `def _publish_capture_outcome(record)`
  - `record_path` (function, line 232) `def record_path(vuln_id, sessions_dir)`
  - `_safe_dir` (function, line 245) `def _safe_dir(vuln_id)`
  - `store_record` (function, line 258) `def store_record(record, sessions_dir)`
  - `list_records` (function, line 276) `def list_records(sessions_dir)`
  - `summary` (function, line 299) `def summary(sessions_dir)`
  - `_gather_evidence` (function, line 326) `def _gather_evidence(candidates)`
  - `_cli_capture` (function, line 350) `def _cli_capture(argv)`
- Depends on: `core/logging.py`, `modules/metasploitable_gym.py`, `modules/outcome_bus.py`

## modules/custom_tools.py
- Doc: Operator-defined custom tools exposed to the autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `_store_file` (function, line 30) `def _store_file()`
  - `_load` (function, line 37) `def _load()`
  - `_save` (function, line 45) `def _save(payload)`
  - `add_tool` (function, line 52) `def add_tool(name, kind, target, description, method, body, timeout, trigger)`
  - `remove_tool` (function, line 97) `def remove_tool(name)`
  - `list_tools` (function, line 109) `def list_tools()`
  - `get_tool` (function, line 114) `def get_tool(name)`
  - `_trigger_tokens` (function, line 122) `def _trigger_tokens(raw)`
  - `match_tools` (function, line 128) `def match_tools(text, limit)`
  - `run_tool` (function, line 151) `def run_tool(name, arg, on_output)`
  - `_run_http` (function, line 179) `def _run_http(tool, arg, on_output)`
- Depends on: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/notify.py`
- Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `tests/test_lazy_loop.py`

## modules/cve_matcher.py
- Doc: modules/cve_matcher.py
- Layer: utility
- Language: py
- Symbols:
  - `CVEResult` (class, line 51) `class CVEResult`
  - `CVEMatcher` (class, line 60) `class CVEMatcher`
  - `get_matcher` (function, line 198) `def get_matcher()`
  - `search` (function, line 206) `def search(product, version, max_results)`
  - `__init__` (method, line 70) `def __init__(self, api_key, cache_dir)`
  - `search` (method, line 82) `def search(self)`
  - `search_by_cpe` (method, line 89) `def search_by_cpe(self, cpe_name, max_results)`
  - `_cache_path` (method, line 95) `def _cache_path(self, params)`
  - `_load_cache` (method, line 100) `def _load_cache(self, params)`
  - `_save_cache` (method, line 112) `def _save_cache(self, params, results)`
  - `_rate_limit` (method, line 121) `def _rate_limit(self)`
  - `_query` (method, line 128) `def _query(self)`
- Depends on: `core/logging.py`
- Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`

## modules/dacl_abuse.py
- Doc: DACL/SACL abuse module — ACL manipulation for AD privilege escalation.
- Layer: utility
- Language: py
- Symbols:
  - `ACEntry` (class, line 67) `class ACEntry`
  - `ACLTarget` (class, line 91) `class ACLTarget`
  - `DACLAbuseEngine` (class, line 113) `class DACLAbuseEngine`
  - `__init__` (method, line 136) `def __init__(self, domain, domain_sid, acl_data)`
  - `parse_bloodhound_acls` (method, line 143) `def parse_bloodhound_acls(self, edges)`
  - `parse_raw_aces` (method, line 182) `def parse_raw_aces(self, raw_nthashes)`
  - `compute_attack_chains` (method, line 224) `def compute_attack_chains(self)`
  - `adminsdholder_abuse_plan` (method, line 291) `def adminsdholder_abuse_plan(self, target_sid)`
  - `dcsync_rights_assignment_plan` (method, line 318) `def dcsync_rights_assignment_plan(self, target_sid, domain_dn)`
  - `owner_takeover_plan` (method, line 348) `def owner_takeover_plan(self, target_dn, attacker_sid)`
  - `_is_dangerous_ace` (method, line 379) `def _is_dangerous_ace(ace)`
  - `_calculate_severity` (method, line 384) `def _calculate_severity(target)`
  - `_guess_object_type` (method, line 397) `def _guess_object_type(dn)`
  - `_extract_cn` (method, line 414) `def _extract_cn(dn)`
  - `summary` (method, line 418) `def summary(self)`
- Imported by: `cli/commands/active_directory.py`

## modules/dashboard_bp.py
- Doc: modules/dashboard_bp.py
- Layer: presentation
- Language: py
- Symbols:
  - `_require_login` (function, line 30) `def _require_login()`
  - `_read_jsonl` (function, line 71) `def _read_jsonl(path, last_n)`
  - `_read_json` (function, line 93) `def _read_json(path)`
  - `_count_lines` (function, line 103) `def _count_lines(path)`
  - `_aggregate_data` (function, line 113) `def _aggregate_data()`
  - `dashboard_index` (function, line 778) `def dashboard_index()`
  - `dashboard_api_data` (function, line 784) `def dashboard_api_data()`
  - `_read_loot_lines` (function, line 800) `def _read_loot_lines(pattern)`
  - `_read_loot` (function, line 817) `def _read_loot()`
  - `dashboard_loot` (function, line 902) `def dashboard_loot()`
  - `_normalize_ts` (function, line 913) `def _normalize_ts(raw)`
  - `_read_timeline` (function, line 934) `def _read_timeline()`
  - `dashboard_timeline` (function, line 1017) `def dashboard_timeline()`
- Imported by: `lazyc2.py`, `tests/test_core_modules.py`, `tests/test_dashboard_routes.py`

## modules/dashboard_engine.py
- Doc: Live Network Map Dashboard for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `_parse_nmap_xml_services` (function, line 39) `def _parse_nmap_xml_services(sessions_dir)`
  - `DashboardNode` (class, line 99) `class DashboardNode`
  - `DashboardEdge` (class, line 111) `class DashboardEdge`
  - `DashboardEngine` (class, line 118) `class DashboardEngine`
  - `__init__` (method, line 139) `def __init__(self, world_model)`
  - `set_world_model` (method, line 148) `def set_world_model(self, model)`
  - `set_exploit_recommender` (method, line 151) `def set_exploit_recommender(self, recommender)`
  - `set_auto_pivot` (method, line 154) `def set_auto_pivot(self, pivot)`
  - `set_evasion_engine` (method, line 157) `def set_evasion_engine(self, evasion)`
  - `build_snapshot` (method, line 160) `def build_snapshot(self)`
  - `render_text_map` (method, line 276) `def render_text_map(self, snapshot)`
  - `render_ascii_topology` (method, line 358) `def render_ascii_topology(self, snapshot)`
  - `_phase_icon` (method, line 398) `def _phase_icon(phase)`
  - `export_json` (method, line 408) `def export_json(self, snapshot)`
  - `persist_snapshot` (method, line 421) `def persist_snapshot(self, snapshot)`
  - `format_for_cli` (method, line 438) `def format_for_cli(self, snapshot)`
- Imported by: `cli/commands/pwn.py`, `modules/rich_tui.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`

## modules/db.py
- Doc: SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes.
- Layer: utility
- Language: py
- Symbols:
  - `LazyOwnDB` (class, line 147) `class LazyOwnDB`
  - `get_db` (function, line 821) `def get_db(db_path)`
  - `__init__` (method, line 159) `def __init__(self, db_path)`
  - `_get_conn` (method, line 171) `def _get_conn(self)`
  - `db_path` (method, line 182) `def db_path(self)`
  - `_init_schema` (method, line 186) `def _init_schema(self)`
  - `_current_version` (method, line 192) `def _current_version(self)`
  - `_run_migrations` (method, line 197) `def _run_migrations(self)`
  - `migration_status` (method, line 222) `def migration_status(self)`
  - `_cursor` (method, line 235) `def _cursor(self)`
  - `_maybe_encrypt` (method, line 251) `def _maybe_encrypt(self, value)`
  - `_maybe_decrypt` (method, line 273) `def _maybe_decrypt(self, value)`
  - `workspace_create` (method, line 292) `def workspace_create(self, name, description)`
  - `workspace_list` (method, line 307) `def workspace_list(self)`
  - `workspace_get` (method, line 313) `def workspace_get(self, name)`
  - `default_workspace` (method, line 320) `def default_workspace(self, name)`
  - `workspace_delete` (method, line 333) `def workspace_delete(self, name)`
  - `host_add` (method, line 357) `def host_add(self, workspace_id, address, mac, hostname, os, state)`
  - `host_delete` (method, line 390) `def host_delete(self, host_id)`
  - `host_list` (method, line 401) `def host_list(self, workspace_id)`
  - `host_find` (method, line 410) `def host_find(self, workspace_id, query)`
  - `service_add` (method, line 427) `def service_add(self, host_id, port, protocol, state, name, product, version)`
  - `service_list` (method, line 447) `def service_list(self, host_id)`
  - `vuln_add` (method, line 460) `def vuln_add(self, host_id, name, severity, description, refs)`
  - `vuln_get` (method, line 478) `def vuln_get(self, vuln_id)`
  - `vuln_update` (method, line 490) `def vuln_update(self, vuln_id, refs, severity, description)`
  - `vuln_list` (method, line 528) `def vuln_list(self, workspace_id, severity)`
  - `cred_add` (method, line 557) `def cred_add(self, host_id, username, password, realm, cred_type, origin)`
  - `cred_list` (method, line 577) `def cred_list(self, workspace_id)`
  - `loot_add` (method, line 596) `def loot_add(self, workspace_id, name, loot_type, path, notes, host_id)`
  - `loot_list` (method, line 615) `def loot_list(self, workspace_id)`
  - `note_add` (method, line 631) `def note_add(self, workspace_id, data, note_type, host_id)`
  - `note_list` (method, line 648) `def note_list(self, workspace_id)`
  - `import_nmap_xml` (method, line 664) `def import_nmap_xml(self, workspace_id, xml_path)`
  - `export_csv` (method, line 740) `def export_csv(self, table, workspace_id)`
  - `status` (method, line 775) `def status(self, workspace_id)`
  - `close` (method, line 804) `def close(self)`
- Depends on: `core/config.py`, `core/crypto.py`, `core/logging.py`
- Imported by: `cli/commands/campaign.py`, `cli/commands/collaboration.py`, `cli/commands/database.py`, `lazyc2/blueprints/api_v1.py`, `modules/autonomous_exploit_engine.py`, `modules/estorides_importer.py`, `modules/hash_cracker.py`, `modules/integrations/nuclei_parser.py`, `modules/opsec_scorer.py`, `modules/sinks/campaign_db.py`, `modules/state_manager.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_api_v1.py`, `tests/test_autonomous_ops.py`, `tests/test_daemon_loop.py`, `tests/test_db.py`, `tests/test_mutation_verification.py`, `tests/test_security_hardening.py`

## modules/defense_eval.py
- Doc: Detection rule replay over recorded attack and control logs.
- Layer: utility
- Language: py
- Symbols:
  - `RuleEvaluationError` (class, line 39) `class RuleEvaluationError(ValueError)`
  - `Condition` (class, line 44) `class Condition`
  - `Evaluation` (class, line 53) `class Evaluation`
  - `DatasetSummary` (class, line 74) `class DatasetSummary`
  - `RuleResult` (class, line 93) `class RuleResult`
  - `parse_rule` (function, line 115) `def parse_rule(rule_text)`
  - `_lookup` (function, line 167) `def _lookup(fields, field_name)`
  - `_canonical_number` (function, line 179) `def _canonical_number(value)`
  - `_compare` (function, line 194) `def _compare(actual, expected, op)`
  - `_scalar_present` (function, line 223) `def _scalar_present(value)`
  - `evaluate_event` (function, line 234) `def evaluate_event(conditions, fields)`
  - `_parse_logs` (function, line 269) `def _parse_logs(text, dataset, max_events)`
  - `evaluate_rule` (function, line 322) `def evaluate_rule(rule_text, target_logs, control_logs)`
  - `metrics` (function, line 380) `def metrics(result)`
  - `to_dict` (method, line 62) `def to_dict(self)`
  - `to_dict` (method, line 82) `def to_dict(self)`
  - `to_dict` (method, line 103) `def to_dict(self)`
- Imported by: `modules/closedloop.py`, `modules/defense_stages.py`, `tests/test_defense_eval.py`, `tests/test_defense_stages.py`

## modules/defense_stages.py
- Doc: Orchestrator stage runners for defense validation and hunt verification.
- Layer: utility
- Language: py
- Symbols:
  - `_activity` (function, line 28) `def _activity(task_id)`
  - `_params` (function, line 42) `def _params(stage)`
  - `_render` (function, line 52) `def _render(value, task_id)`
  - `_read_text` (function, line 57) `def _read_text(path)`
  - `_load_dataset` (function, line 67) `def _load_dataset(stage, key, task_id)`
  - `run_defense_validate` (function, line 82) `def run_defense_validate(task_id)`
  - `run_closedloop_tune` (function, line 117) `def run_closedloop_tune(task_id)`
  - `run_hunt_verify` (function, line 151) `def run_hunt_verify(task_id)`
  - `_write_json` (function, line 230) `def _write_json(path, data)`
  - `_Stub` (class, line 35) `class _Stub`
  - `emit` (method, line 36) `def emit(self)`
- Depends on: `core/logging.py`, `modules/closedloop.py`, `modules/defense_eval.py`, `modules/hunt_verify.py`, `modules/orchestrator_config.py`
- Imported by: `modules/lazy_loop.py`, `tests/test_defense_stages.py`

## modules/delegation_attacks.py
- Doc: Active Directory delegation enumeration and abuse.
- Layer: utility
- Language: py
- Symbols:
  - `DelegationTarget` (class, line 32) `class DelegationTarget`
  - `DelegationAttackPath` (class, line 63) `class DelegationAttackPath`
  - `DelegationEnumerator` (class, line 85) `class DelegationEnumerator`
  - `__init__` (method, line 98) `def __init__(self, domain, raw_ldap_output)`
  - `enumerate_from_uac_flags` (method, line 104) `def enumerate_from_uac_flags(self, accounts)`
  - `parse_bloodhound_output` (method, line 151) `def parse_bloodhound_output(self, bloodhound_json)`
  - `find_unconstrained_targets` (method, line 181) `def find_unconstrained_targets(self)`
  - `find_constrained_targets` (method, line 189) `def find_constrained_targets(self)`
  - `find_rbcd_targets` (method, line 197) `def find_rbcd_targets(self)`
  - `find_dc_targets` (method, line 205) `def find_dc_targets(self)`
  - `compute_attack_paths` (method, line 215) `def compute_attack_paths(self)`
  - `summary` (method, line 296) `def summary(self)`
- Imported by: `cli/commands/active_directory.py`

## modules/detailed_search.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `obtener_informacion` (function, line 40) `def obtener_informacion(url)`

## modules/detection_feed.py
- Doc: Dynamic detection feed for the Detection Oracle.
- Layer: utility
- Language: py
- Symbols:
  - `FeedResult` (class, line 64) `class FeedResult`
  - `DetectionFeed` (class, line 73) `class DetectionFeed`
  - `get_feed` (function, line 326) `def get_feed()`
  - `__init__` (method, line 83) `def __init__(self, cache_dir, sources)`
  - `update_rules` (method, line 92) `def update_rules(self, source)`
  - `_parse_sigma_feed` (method, line 125) `def _parse_sigma_feed(self, text)`
  - `_extract_log_source` (method, line 172) `def _extract_log_source(self, doc)`
  - `_extract_mitre` (method, line 180) `def _extract_mitre(self, doc)`
  - `_extract_keywords` (method, line 189) `def _extract_keywords(self, doc)`
  - `_extract_categories` (method, line 206) `def _extract_categories(self, doc)`
  - `_cache_rules` (method, line 219) `def _cache_rules(self, rules, source)`
  - `load_cached_rules` (method, line 246) `def load_cached_rules(self, source)`
  - `adjust_from_feedback` (method, line 270) `def adjust_from_feedback(self, feedback_file)`
- Depends on: `core/logging.py`, `modules/detection_oracle.py`
- Imported by: `modules/detection_oracle.py`, `tests/test_detection_feed.py`

## modules/detection_oracle.py
- Doc: modules/detection_oracle.py
- Layer: utility
- Language: py
- Symbols:
  - `SigmaRule` (class, line 50) `class SigmaRule`
  - `DetectionAssessment` (class, line 63) `class DetectionAssessment`
  - `IDetectionOracle` (class, line 90) `class IDetectionOracle(ABC)`
  - `DetectionOracle` (class, line 317) `class DetectionOracle(IDetectionOracle)`
  - `get_oracle` (function, line 478) `def get_oracle()`
  - `is_high_risk` (method, line 75) `def is_high_risk(self)`
  - `is_critical_risk` (method, line 80) `def is_critical_risk(self)`
  - `assess` (method, line 94) `def assess(self, command, args, action_category)`
  - `probability` (method, line 103) `def probability(self, command, args, action_category)`
  - `__init__` (method, line 332) `def __init__(self, rules, feed)`
  - `refresh` (method, line 336) `def refresh(self)`
  - `assess` (method, line 371) `def assess(self, command, args, action_category)`
  - `probability` (method, line 392) `def probability(self, command, args, action_category)`
  - `_match_rules` (method, line 397) `def _match_rules(self, text, action_category)`
  - `_effective_probability` (method, line 417) `def _effective_probability(rule, action_category)`
  - `_aggregate_probability` (method, line 427) `def _aggregate_probability(self, matched, action_category)`
  - `_build_recommendation` (method, line 444) `def _build_recommendation(probability, matched, action_category)`
- Depends on: `core/logging.py`, `modules/detection_feed.py`
- Imported by: `modules/auto_purple.py`, `modules/detection_feed.py`, `modules/loop_ai_bridge.py`, `skills/autonomous_daemon.py`, `skills/lazyown_policy.py`, `skills/swan_agent.py`, `tests/test_detection_feed.py`, `tests/test_loop_ai_bridge.py`, `tests/test_moe_rl_swan.py`

## modules/digest.py
- Doc: Operator digest generation for loop runs.
- Layer: utility
- Language: py
- Symbols:
  - `build_engine_digest` (function, line 20) `def build_engine_digest(task_id, status, rounds, findings, facts, blocks, reaction_backlog)`
  - `write_digest` (function, line 71) `def write_digest(task_id, body, root)`
  - `worker_results_digest` (function, line 82) `def worker_results_digest(rows)`
- Imported by: `modules/lazy_loop.py`, `skills/lazyown_mcp.py`

## modules/dns_beacon.py
- Doc: DNS Beacon — covert C2 channel via DNS tunneling.
- Layer: utility
- Language: py
- Symbols:
  - `DNSBeacon` (class, line 23) `class DNSBeacon`
  - `DNSC2Server` (class, line 199) `class DNSC2Server`
  - `__init__` (method, line 38) `def __init__(self, domain, dns_server, sleep_seconds, jitter_percent, dns_type, encode_method)`
  - `_ensure_dnspython` (method, line 57) `def _ensure_dnspython(self)`
  - `_encode` (method, line 63) `def _encode(self, data)`
  - `_decode` (method, line 70) `def _decode(self, data)`
  - `_jittered_sleep` (method, line 78) `def _jittered_sleep(self)`
  - `_dns_query` (method, line 84) `def _dns_query(self, name, qtype)`
  - `_build_query` (method, line 96) `def _build_query(self, msg_type, payload)`
  - `check_in` (method, line 105) `def check_in(self)`
  - `send_result` (method, line 135) `def send_result(self, command, output, exit_code)`
  - `run` (method, line 171) `def run(self)`
  - `__init__` (method, line 211) `def __init__(self, domain, log_source, interface)`
  - `register_beacon` (method, line 225) `def register_beacon(self, beacon_id, hostname)`
  - `list_beacons` (method, line 235) `def list_beacons(self)`
  - `send_task` (method, line 239) `def send_task(self, beacon_id, command)`
  - `process_query_log` (method, line 248) `def process_query_log(self, line)`
  - `_handle_result` (method, line 294) `def _handle_result(self, labels, query)`
  - `get_results` (method, line 327) `def get_results(self, beacon_id)`
- Depends on: `core/safe_exec.py`
- Imported by: `cli/commands/dns_exfil.py`

## modules/domain_dominance.py
- Doc: Domain Dominance Engine — automated Active Directory takeover.
- Layer: business_logic
- Language: py
- Symbols:
  - `DomainInfo` (class, line 49) `class DomainInfo`
  - `CredentialStash` (class, line 65) `class CredentialStash`
  - `DominanceResult` (class, line 75) `class DominanceResult`
  - `DomainDominance` (class, line 89) `class DomainDominance`
  - `__init__` (method, line 103) `def __init__(self)`
  - `get_instance` (method, line 110) `def get_instance(cls)`
  - `dominate` (method, line 121) `def dominate(self, domain, dc_ip, username, password, ntlm_hash)`
  - `enumerate_domain` (method, line 194) `def enumerate_domain(self, domain, dc_ip)`
  - `extract_credentials` (method, line 227) `def extract_credentials(self, domain_info, known_creds)`
  - `escalate` (method, line 260) `def escalate(self, domain_info, stash)`
  - `persist` (method, line 314) `def persist(self, domain_info)`
  - `_discover_dc` (method, line 340) `def _discover_dc(self, domain, dns_servers)`
  - `_find_dcs` (method, line 366) `def _find_dcs(self, domain, dc_ip)`
  - `_find_domain_admins` (method, line 392) `def _find_domain_admins(self, domain, dc_ip)`
  - `_enumerate_users` (method, line 426) `def _enumerate_users(self, dc_ip)`
  - `_enumerate_computers` (method, line 469) `def _enumerate_computers(self, dc_ip)`
  - `_enumerate_groups` (method, line 495) `def _enumerate_groups(self, dc_ip)`
  - `_enumerate_spns` (method, line 516) `def _enumerate_spns(self, dc_ip)`
  - `_enumerate_trusts` (method, line 546) `def _enumerate_trusts(self, domain, dc_ip)`
  - `_asrep_roast` (method, line 575) `def _asrep_roast(self, domain_info)`
  - `_kerberoast` (method, line 625) `def _kerberoast(self, domain_info)`
  - `_psexec_session` (method, line 666) `def _psexec_session(self, target, domain, user, password)`
  - `_wmiexec_session` (method, line 697) `def _wmiexec_session(self, target, domain, user, password)`
  - `_pth_session` (method, line 728) `def _pth_session(self, target, domain, user, ntlm_hash)`
  - `_attempt_dcsync` (method, line 768) `def _attempt_dcsync(self, dc_ip)`
  - `_load_config` (method, line 827) `def _load_config(self)`
  - `_domain_to_dn` (method, line 838) `def _domain_to_dn(self, domain)`
  - `_seal_loot_secret` (method, line 850) `def _seal_loot_secret(secret)`
  - `_unseal_loot_secret` (method, line 871) `def _unseal_loot_secret(stored)`
  - `_save_credential` (method, line 890) `def _save_credential(self, username, secret, secret_type, source)`
  - `_save_session` (method, line 924) `def _save_session(self, session_id, target, method, user)`
  - `_save_dominance_report` (method, line 944) `def _save_dominance_report(self)`
- Depends on: `core/hardening.py`
- Imported by: `cli/commands/lateral_migrated.py`, `tests/test_security_alerts_fix.py`

## modules/dotnet_payload.py
- Doc: .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.
- Layer: utility
- Language: py
- Symbols:
  - `DotNetPayloadConfig` (class, line 293) `class DotNetPayloadConfig`
  - `DotNetPayloadFactory` (class, line 315) `class DotNetPayloadFactory`
  - `__init__` (method, line 327) `def __init__(self, output_dir)`
  - `_detect_compiler` (method, line 333) `def _detect_compiler()`
  - `list_templates` (method, line 364) `def list_templates()`
  - `_resolve_template` (method, line 368) `def _resolve_template(self, config)`
  - `generate_source` (method, line 389) `def generate_source(self, config)`
  - `compile` (method, line 403) `def compile(self, config, source_code)`
  - `generate` (method, line 454) `def generate(self, config)`
  - `generate_powershell_reflective` (method, line 481) `def generate_powershell_reflective(self, config)`
  - `generate_inline_assembly` (method, line 500) `def generate_inline_assembly(self, config)`
  - `to_format` (method, line 520) `def to_format(self, data, fmt)`
- Imported by: `cli/commands/payload_arsenal.py`

## modules/dpapi_harvester.py
- Doc: DPAPI credential decryption and harvesting engine.
- Layer: utility
- Language: py
- Symbols:
  - `DPAPICredential` (class, line 44) `class DPAPICredential`
  - `DPAPIMasterKey` (class, line 54) `class DPAPIMasterKey`
  - `DPAPIHarvester` (class, line 63) `class DPAPIHarvester`
  - `__init__` (method, line 79) `def __init__(self, sessions_dir, masterkey_path)`
  - `harvest_all` (method, line 90) `def harvest_all(self)`
  - `_harvest_master_keys` (method, line 105) `def _harvest_master_keys(self)`
  - `_harvest_credential_manager` (method, line 120) `def _harvest_credential_manager(self)`
  - `_harvest_chrome` (method, line 143) `def _harvest_chrome(self)`
  - `_harvest_chrome_offline` (method, line 188) `def _harvest_chrome_offline(self)`
  - `_harvest_edge` (method, line 198) `def _harvest_edge(self)`
  - `_harvest_wifi` (method, line 210) `def _harvest_wifi(self)`
  - `_harvest_rdp` (method, line 250) `def _harvest_rdp(self)`
  - `_harvest_windows_vault` (method, line 262) `def _harvest_windows_vault(self)`
  - `_crack_login_data` (method, line 286) `def _crack_login_data(self, login_db_path, key, source)`
  - `_crack_cookies` (method, line 320) `def _crack_cookies(self, cookies_path, key, source)`
  - `_extract_sid_from_file` (method, line 355) `def _extract_sid_from_file(filepath)`
  - `export_credentials` (method, line 367) `def export_credentials(self)`
  - `masterkey_report` (method, line 386) `def masterkey_report(self)`
  - `DATA_BLOB` (class, line 160) `class DATA_BLOB(Structure)`
- Imported by: `cli/commands/dpapi.py`

## modules/duckdns.sh
- Doc: Solicita el TOKEN y el DOMAIN al usuario
- Layer: utility
- Language: sh

## modules/edr_detector.py
- Doc: EDR/AV Detection and Evasion Profiling Engine.
- Layer: utility
- Language: py
- Symbols:
  - `EDRFinding` (class, line 174) `class EDRFinding`
  - `EDRProfile` (class, line 182) `class EDRProfile`
  - `EDRDetector` (class, line 191) `class EDRDetector`
  - `detect_local` (method, line 202) `def detect_local()`
  - `detect_remote_commands` (method, line 221) `def detect_remote_commands(remote_type)`
  - `_local_processes` (method, line 292) `def _local_processes()`
  - `_local_services` (method, line 305) `def _local_services()`
  - `_local_drivers` (method, line 322) `def _local_drivers()`
  - `_match_signatures` (method, line 335) `def _match_signatures(profile)`
  - `_generate_recommendations` (method, line 370) `def _generate_recommendations(profile)`
  - `_severity` (method, line 428) `def _severity(profile)`
  - `generate_edr_check_script` (method, line 440) `def generate_edr_check_script(remote_type)`
- Imported by: `cli/commands/edr_detect.py`

## modules/eegg.sh
- Doc: Definición de colores
- Layer: utility
- Language: sh
- Symbols:
  - `init_board` (function, line 26)
  - `show_board` (function, line 40)
  - `move_white_pawns` (function, line 61)
  - `move_black_pawns` (function, line 78)

## modules/emulation_runner.py
- Doc: Single execution contract for Atomic emulation.
- Layer: utility
- Language: py
- Symbols:
  - `EmulationStep` (class, line 28) `class EmulationStep`
  - `EmulationResult` (class, line 40) `class EmulationResult`
  - `EmulationReport` (class, line 69) `class EmulationReport`
  - `EmulationRunner` (class, line 105) `class EmulationRunner`
  - `to_dict` (method, line 53) `def to_dict(self)`
  - `executed` (method, line 81) `def executed(self)`
  - `shell` (method, line 86) `def shell(self)`
  - `to_dict` (method, line 90) `def to_dict(self)`
  - `__init__` (method, line 108) `def __init__(self, resolver, sessions_dir, shell_opener, remote_exec_fn, playbook_loader, outcome_recorder...`
  - `_resolver_obj` (method, line 127) `def _resolver_obj(self)`
  - `_playbook` (method, line 135) `def _playbook(self, name)`
  - `_open_shell` (method, line 143) `def _open_shell(self, target, services, lhost, exploits_dir)`
  - `_exec` (method, line 151) `def _exec(self, spec, target, command, lhost)`
  - `_detect` (method, line 159) `def _detect(self, spec, output)`
  - `_record` (method, line 170) `def _record(self)`
  - `techniques_for_playbook` (method, line 182) `def techniques_for_playbook(self, playbook, platform)`
  - `run` (method, line 202) `def run(self, target, techniques, playbook, platform, lhost, per_technique, include_manual, dry_run, executor...`
  - `run_steps` (method, line 321) `def run_steps(self, steps, target, executor, platform, dry_run, source)`
  - `_run_test` (method, line 399) `def _run_test(self, test, technique, target, spec, lhost, executor, dry_run, include_manual, report, sessions)`
  - `_publish` (method, line 450) `def _publish(self, result, target, source, dry_run, sessions)`
  - `_stage` (method, line 482) `def _stage(self, report, sessions)`
- Depends on: `core/logging.py`, `modules/apt_playbooks.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/outcome_bus.py`
- Imported by: `modules/atomic_exploit_bridge.py`, `modules/playbook_engine.py`, `tests/test_emulation_runner.py`

## modules/engage_summary.py
- Doc: Rich per-step engagement summaries from evidence and sessions artefacts.
- Layer: utility
- Language: py
- Symbols:
  - `marker_lines` (function, line 35) `def marker_lines(text, limit)`
  - `full_output` (function, line 51) `def full_output(step, sessions_dir)`
  - `held_scan_ports` (function, line 64) `def held_scan_ports(target, sessions_dir)`
  - `detail_for` (function, line 98) `def detail_for(tool, text, target, sessions_dir)`
  - `next_actions` (function, line 150) `def next_actions(target, sessions_dir, limit)`
  - `render_text` (function, line 175) `def render_text(engagement_id, target, shell, steps, sessions_dir)`
  - `render_markdown` (function, line 210) `def render_markdown(engagement_id, target, shell, steps, next_list, sessions_dir)`
  - `write_report` (function, line 247) `def write_report(engagement_id, target, shell, steps, sessions_dir)`
- Depends on: `cli/recommendation_signals.py`, `modules/enrich.py`, `modules/evidence.py`
- Imported by: `skills/unified_orchestrator.py`, `tests/test_engage_summary.py`


Next: [KB_modules_p5.md](KB_modules_p5.md)
