# Symbols (page 13 of 46)
Previous: [SYMBOLS_p12.md](SYMBOLS_p12.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_extract_cn` | method | `modules/dacl_abuse.py:414` | `def _extract_cn(dn)` |
| `_guess_object_type` | method | `modules/dacl_abuse.py:397` | `def _guess_object_type(dn)` |
| `_is_dangerous_ace` | method | `modules/dacl_abuse.py:379` | `def _is_dangerous_ace(ace)` |
| `adminsdholder_abuse_plan` | method | `modules/dacl_abuse.py:291` | `def adminsdholder_abuse_plan(self, target_sid)` |
| `compute_attack_chains` | method | `modules/dacl_abuse.py:224` | `def compute_attack_chains(self)` |
| `dcsync_rights_assignment_plan` | method | `modules/dacl_abuse.py:318` | `def dcsync_rights_assignment_plan(self, target_sid, domain_dn)` |
| `owner_takeover_plan` | method | `modules/dacl_abuse.py:348` | `def owner_takeover_plan(self, target_dn, attacker_sid)` |
| `parse_bloodhound_acls` | method | `modules/dacl_abuse.py:143` | `def parse_bloodhound_acls(self, edges)` |
| `parse_raw_aces` | method | `modules/dacl_abuse.py:182` | `def parse_raw_aces(self, raw_nthashes)` |
| `summary` | method | `modules/dacl_abuse.py:418` | `def summary(self)` |
| `_aggregate_data` | function | `modules/dashboard_bp.py:113` | `def _aggregate_data()` |
| `_count_lines` | function | `modules/dashboard_bp.py:103` | `def _count_lines(path)` |
| `_normalize_ts` | function | `modules/dashboard_bp.py:913` | `def _normalize_ts(raw)` |
| `_read_json` | function | `modules/dashboard_bp.py:93` | `def _read_json(path)` |
| `_read_jsonl` | function | `modules/dashboard_bp.py:71` | `def _read_jsonl(path, last_n)` |
| `_read_loot` | function | `modules/dashboard_bp.py:817` | `def _read_loot()` |
| `_read_loot_lines` | function | `modules/dashboard_bp.py:800` | `def _read_loot_lines(pattern)` |
| `_read_timeline` | function | `modules/dashboard_bp.py:934` | `def _read_timeline()` |
| `_require_login` | function | `modules/dashboard_bp.py:30` | `def _require_login()` |
| `dashboard_api_data` | function | `modules/dashboard_bp.py:784` | `def dashboard_api_data()` |
| `dashboard_index` | function | `modules/dashboard_bp.py:778` | `def dashboard_index()` |
| `dashboard_loot` | function | `modules/dashboard_bp.py:902` | `def dashboard_loot()` |
| `dashboard_timeline` | function | `modules/dashboard_bp.py:1017` | `def dashboard_timeline()` |
| `DashboardEdge` | class | `modules/dashboard_engine.py:111` | `class DashboardEdge` |
| `DashboardEngine` | class | `modules/dashboard_engine.py:118` | `class DashboardEngine` |
| `DashboardNode` | class | `modules/dashboard_engine.py:99` | `class DashboardNode` |
| `__init__` | method | `modules/dashboard_engine.py:139` | `def __init__(self, world_model)` |
| `_parse_nmap_xml_services` | function | `modules/dashboard_engine.py:39` | `def _parse_nmap_xml_services(sessions_dir)` |
| `_phase_icon` | method | `modules/dashboard_engine.py:398` | `def _phase_icon(phase)` |
| `build_snapshot` | method | `modules/dashboard_engine.py:160` | `def build_snapshot(self)` |
| `export_json` | method | `modules/dashboard_engine.py:408` | `def export_json(self, snapshot)` |
| `format_for_cli` | method | `modules/dashboard_engine.py:438` | `def format_for_cli(self, snapshot)` |
| `persist_snapshot` | method | `modules/dashboard_engine.py:421` | `def persist_snapshot(self, snapshot)` |
| `render_ascii_topology` | method | `modules/dashboard_engine.py:358` | `def render_ascii_topology(self, snapshot)` |
| `render_text_map` | method | `modules/dashboard_engine.py:276` | `def render_text_map(self, snapshot)` |
| `set_auto_pivot` | method | `modules/dashboard_engine.py:154` | `def set_auto_pivot(self, pivot)` |
| `set_evasion_engine` | method | `modules/dashboard_engine.py:157` | `def set_evasion_engine(self, evasion)` |
| `set_exploit_recommender` | method | `modules/dashboard_engine.py:151` | `def set_exploit_recommender(self, recommender)` |
| `set_world_model` | method | `modules/dashboard_engine.py:148` | `def set_world_model(self, model)` |
| `LazyOwnDB` | class | `modules/db.py:147` | `class LazyOwnDB` |
| `__init__` | method | `modules/db.py:159` | `def __init__(self, db_path)` |
| `_current_version` | method | `modules/db.py:192` | `def _current_version(self)` |
| `_cursor` | method | `modules/db.py:235` | `def _cursor(self)` |
| `_get_conn` | method | `modules/db.py:171` | `def _get_conn(self)` |
| `_init_schema` | method | `modules/db.py:186` | `def _init_schema(self)` |
| `_maybe_decrypt` | method | `modules/db.py:273` | `def _maybe_decrypt(self, value)` |
| `_maybe_encrypt` | method | `modules/db.py:251` | `def _maybe_encrypt(self, value)` |
| `_run_migrations` | method | `modules/db.py:197` | `def _run_migrations(self)` |
| `close` | method | `modules/db.py:804` | `def close(self)` |
| `cred_add` | method | `modules/db.py:557` | `def cred_add(self, host_id, username, password, realm, cred_type, origin)` |
| `cred_list` | method | `modules/db.py:577` | `def cred_list(self, workspace_id)` |
| `db_path` | method | `modules/db.py:182` | `def db_path(self)` |
| `default_workspace` | method | `modules/db.py:320` | `def default_workspace(self, name)` |
| `export_csv` | method | `modules/db.py:740` | `def export_csv(self, table, workspace_id)` |
| `get_db` | function | `modules/db.py:821` | `def get_db(db_path)` |
| `host_add` | method | `modules/db.py:357` | `def host_add(self, workspace_id, address, mac, hostname, os, state)` |
| `host_delete` | method | `modules/db.py:390` | `def host_delete(self, host_id)` |
| `host_find` | method | `modules/db.py:410` | `def host_find(self, workspace_id, query)` |
| `host_list` | method | `modules/db.py:401` | `def host_list(self, workspace_id)` |
| `import_nmap_xml` | method | `modules/db.py:664` | `def import_nmap_xml(self, workspace_id, xml_path)` |
| `loot_add` | method | `modules/db.py:596` | `def loot_add(self, workspace_id, name, loot_type, path, notes, host_id)` |
| `loot_list` | method | `modules/db.py:615` | `def loot_list(self, workspace_id)` |
| `migration_status` | method | `modules/db.py:222` | `def migration_status(self)` |
| `note_add` | method | `modules/db.py:631` | `def note_add(self, workspace_id, data, note_type, host_id)` |
| `note_list` | method | `modules/db.py:648` | `def note_list(self, workspace_id)` |
| `service_add` | method | `modules/db.py:427` | `def service_add(self, host_id, port, protocol, state, name, product, version)` |
| `service_list` | method | `modules/db.py:447` | `def service_list(self, host_id)` |
| `status` | method | `modules/db.py:775` | `def status(self, workspace_id)` |
| `vuln_add` | method | `modules/db.py:460` | `def vuln_add(self, host_id, name, severity, description, refs)` |
| `vuln_get` | method | `modules/db.py:478` | `def vuln_get(self, vuln_id)` |
| `vuln_list` | method | `modules/db.py:528` | `def vuln_list(self, workspace_id, severity)` |
| `vuln_update` | method | `modules/db.py:490` | `def vuln_update(self, vuln_id, refs, severity, description)` |
| `workspace_create` | method | `modules/db.py:292` | `def workspace_create(self, name, description)` |
| `workspace_delete` | method | `modules/db.py:333` | `def workspace_delete(self, name)` |
| `workspace_get` | method | `modules/db.py:313` | `def workspace_get(self, name)` |
| `workspace_list` | method | `modules/db.py:307` | `def workspace_list(self)` |
| `Condition` | class | `modules/defense_eval.py:44` | `class Condition` |
| `DatasetSummary` | class | `modules/defense_eval.py:74` | `class DatasetSummary` |
| `Evaluation` | class | `modules/defense_eval.py:53` | `class Evaluation` |
| `RuleEvaluationError` | class | `modules/defense_eval.py:39` | `class RuleEvaluationError(ValueError)` |
| `RuleResult` | class | `modules/defense_eval.py:93` | `class RuleResult` |
| `_canonical_number` | function | `modules/defense_eval.py:179` | `def _canonical_number(value)` |
| `_compare` | function | `modules/defense_eval.py:194` | `def _compare(actual, expected, op)` |
| `_lookup` | function | `modules/defense_eval.py:167` | `def _lookup(fields, field_name)` |
| `_parse_logs` | function | `modules/defense_eval.py:269` | `def _parse_logs(text, dataset, max_events)` |
| `_scalar_present` | function | `modules/defense_eval.py:223` | `def _scalar_present(value)` |
| `evaluate_event` | function | `modules/defense_eval.py:234` | `def evaluate_event(conditions, fields)` |
| `evaluate_rule` | function | `modules/defense_eval.py:322` | `def evaluate_rule(rule_text, target_logs, control_logs)` |
| `metrics` | function | `modules/defense_eval.py:380` | `def metrics(result)` |
| `parse_rule` | function | `modules/defense_eval.py:115` | `def parse_rule(rule_text)` |
| `to_dict` | method | `modules/defense_eval.py:62` | `def to_dict(self)` |
| `to_dict` | method | `modules/defense_eval.py:82` | `def to_dict(self)` |
| `to_dict` | method | `modules/defense_eval.py:103` | `def to_dict(self)` |
| `_Stub` | class | `modules/defense_stages.py:35` | `class _Stub` |
| `_activity` | function | `modules/defense_stages.py:28` | `def _activity(task_id)` |
| `_load_dataset` | function | `modules/defense_stages.py:67` | `def _load_dataset(stage, key, task_id)` |
| `_params` | function | `modules/defense_stages.py:42` | `def _params(stage)` |
| `_read_text` | function | `modules/defense_stages.py:57` | `def _read_text(path)` |
| `_render` | function | `modules/defense_stages.py:52` | `def _render(value, task_id)` |
| `_write_json` | function | `modules/defense_stages.py:230` | `def _write_json(path, data)` |
| `emit` | method | `modules/defense_stages.py:36` | `def emit(self)` |
| `run_closedloop_tune` | function | `modules/defense_stages.py:117` | `def run_closedloop_tune(task_id)` |
| `run_defense_validate` | function | `modules/defense_stages.py:82` | `def run_defense_validate(task_id)` |
| `run_hunt_verify` | function | `modules/defense_stages.py:151` | `def run_hunt_verify(task_id)` |
| `DelegationAttackPath` | class | `modules/delegation_attacks.py:63` | `class DelegationAttackPath` |
| `DelegationEnumerator` | class | `modules/delegation_attacks.py:85` | `class DelegationEnumerator` |
| `DelegationTarget` | class | `modules/delegation_attacks.py:32` | `class DelegationTarget` |
| `__init__` | method | `modules/delegation_attacks.py:98` | `def __init__(self, domain, raw_ldap_output)` |
| `compute_attack_paths` | method | `modules/delegation_attacks.py:215` | `def compute_attack_paths(self)` |
| `enumerate_from_uac_flags` | method | `modules/delegation_attacks.py:104` | `def enumerate_from_uac_flags(self, accounts)` |
| `find_constrained_targets` | method | `modules/delegation_attacks.py:189` | `def find_constrained_targets(self)` |
| `find_dc_targets` | method | `modules/delegation_attacks.py:205` | `def find_dc_targets(self)` |
| `find_rbcd_targets` | method | `modules/delegation_attacks.py:197` | `def find_rbcd_targets(self)` |
| `find_unconstrained_targets` | method | `modules/delegation_attacks.py:181` | `def find_unconstrained_targets(self)` |
| `parse_bloodhound_output` | method | `modules/delegation_attacks.py:151` | `def parse_bloodhound_output(self, bloodhound_json)` |
| `summary` | method | `modules/delegation_attacks.py:296` | `def summary(self)` |
| `obtener_informacion` | function | `modules/detailed_search.py:40` | `def obtener_informacion(url)` |
| `DetectionFeed` | class | `modules/detection_feed.py:73` | `class DetectionFeed` |
| `FeedResult` | class | `modules/detection_feed.py:64` | `class FeedResult` |
| `__init__` | method | `modules/detection_feed.py:83` | `def __init__(self, cache_dir, sources)` |
| `_cache_rules` | method | `modules/detection_feed.py:219` | `def _cache_rules(self, rules, source)` |
| `_extract_categories` | method | `modules/detection_feed.py:206` | `def _extract_categories(self, doc)` |
| `_extract_keywords` | method | `modules/detection_feed.py:189` | `def _extract_keywords(self, doc)` |
| `_extract_log_source` | method | `modules/detection_feed.py:172` | `def _extract_log_source(self, doc)` |
| `_extract_mitre` | method | `modules/detection_feed.py:180` | `def _extract_mitre(self, doc)` |
| `_parse_sigma_feed` | method | `modules/detection_feed.py:125` | `def _parse_sigma_feed(self, text)` |
| `adjust_from_feedback` | method | `modules/detection_feed.py:270` | `def adjust_from_feedback(self, feedback_file)` |
| `get_feed` | function | `modules/detection_feed.py:326` | `def get_feed()` |
| `load_cached_rules` | method | `modules/detection_feed.py:246` | `def load_cached_rules(self, source)` |
| `update_rules` | method | `modules/detection_feed.py:92` | `def update_rules(self, source)` |
| `DetectionAssessment` | class | `modules/detection_oracle.py:63` | `class DetectionAssessment` |
| `DetectionOracle` | class | `modules/detection_oracle.py:317` | `class DetectionOracle(IDetectionOracle)` |
| `IDetectionOracle` | class | `modules/detection_oracle.py:90` | `class IDetectionOracle(ABC)` |
| `SigmaRule` | class | `modules/detection_oracle.py:50` | `class SigmaRule` |
| `__init__` | method | `modules/detection_oracle.py:332` | `def __init__(self, rules, feed)` |
| `_aggregate_probability` | method | `modules/detection_oracle.py:427` | `def _aggregate_probability(self, matched, action_category)` |
| `_build_recommendation` | method | `modules/detection_oracle.py:444` | `def _build_recommendation(probability, matched, action_category)` |
| `_effective_probability` | method | `modules/detection_oracle.py:417` | `def _effective_probability(rule, action_category)` |
| `_match_rules` | method | `modules/detection_oracle.py:397` | `def _match_rules(self, text, action_category)` |
| `assess` | method | `modules/detection_oracle.py:94` | `def assess(self, command, args, action_category)` |
| `assess` | method | `modules/detection_oracle.py:371` | `def assess(self, command, args, action_category)` |
| `get_oracle` | function | `modules/detection_oracle.py:478` | `def get_oracle()` |
| `is_critical_risk` | method | `modules/detection_oracle.py:80` | `def is_critical_risk(self)` |
| `is_high_risk` | method | `modules/detection_oracle.py:75` | `def is_high_risk(self)` |
| `probability` | method | `modules/detection_oracle.py:103` | `def probability(self, command, args, action_category)` |
| `probability` | method | `modules/detection_oracle.py:392` | `def probability(self, command, args, action_category)` |
| `refresh` | method | `modules/detection_oracle.py:336` | `def refresh(self)` |
| `build_engine_digest` | function | `modules/digest.py:20` | `def build_engine_digest(task_id, status, rounds, findings, facts, blocks, reaction_backlog)` |
| `worker_results_digest` | function | `modules/digest.py:82` | `def worker_results_digest(rows)` |
| `write_digest` | function | `modules/digest.py:71` | `def write_digest(task_id, body, root)` |
| `DNSBeacon` | class | `modules/dns_beacon.py:23` | `class DNSBeacon` |
| `DNSC2Server` | class | `modules/dns_beacon.py:199` | `class DNSC2Server` |
| `__init__` | method | `modules/dns_beacon.py:38` | `def __init__(self, domain, dns_server, sleep_seconds, jitter_percent, dns_type, encode_method)` |
| `__init__` | method | `modules/dns_beacon.py:211` | `def __init__(self, domain, log_source, interface)` |
| `_build_query` | method | `modules/dns_beacon.py:96` | `def _build_query(self, msg_type, payload)` |
| `_decode` | method | `modules/dns_beacon.py:70` | `def _decode(self, data)` |
| `_dns_query` | method | `modules/dns_beacon.py:84` | `def _dns_query(self, name, qtype)` |
| `_encode` | method | `modules/dns_beacon.py:63` | `def _encode(self, data)` |
| `_ensure_dnspython` | method | `modules/dns_beacon.py:57` | `def _ensure_dnspython(self)` |
| `_handle_result` | method | `modules/dns_beacon.py:294` | `def _handle_result(self, labels, query)` |
| `_jittered_sleep` | method | `modules/dns_beacon.py:78` | `def _jittered_sleep(self)` |
| `check_in` | method | `modules/dns_beacon.py:105` | `def check_in(self)` |
| `get_results` | method | `modules/dns_beacon.py:327` | `def get_results(self, beacon_id)` |
| `list_beacons` | method | `modules/dns_beacon.py:235` | `def list_beacons(self)` |
| `process_query_log` | method | `modules/dns_beacon.py:248` | `def process_query_log(self, line)` |
| `register_beacon` | method | `modules/dns_beacon.py:225` | `def register_beacon(self, beacon_id, hostname)` |
| `run` | method | `modules/dns_beacon.py:171` | `def run(self)` |
| `send_result` | method | `modules/dns_beacon.py:135` | `def send_result(self, command, output, exit_code)` |
| `send_task` | method | `modules/dns_beacon.py:239` | `def send_task(self, beacon_id, command)` |
| `CredentialStash` | class | `modules/domain_dominance.py:65` | `class CredentialStash` |
| `DomainDominance` | class | `modules/domain_dominance.py:89` | `class DomainDominance` |
| `DomainInfo` | class | `modules/domain_dominance.py:49` | `class DomainInfo` |
| `DominanceResult` | class | `modules/domain_dominance.py:75` | `class DominanceResult` |
| `__init__` | method | `modules/domain_dominance.py:103` | `def __init__(self)` |
| `_asrep_roast` | method | `modules/domain_dominance.py:575` | `def _asrep_roast(self, domain_info)` |
| `_attempt_dcsync` | method | `modules/domain_dominance.py:768` | `def _attempt_dcsync(self, dc_ip)` |
| `_discover_dc` | method | `modules/domain_dominance.py:340` | `def _discover_dc(self, domain, dns_servers)` |
| `_domain_to_dn` | method | `modules/domain_dominance.py:838` | `def _domain_to_dn(self, domain)` |
| `_enumerate_computers` | method | `modules/domain_dominance.py:469` | `def _enumerate_computers(self, dc_ip)` |
| `_enumerate_groups` | method | `modules/domain_dominance.py:495` | `def _enumerate_groups(self, dc_ip)` |
| `_enumerate_spns` | method | `modules/domain_dominance.py:516` | `def _enumerate_spns(self, dc_ip)` |
| `_enumerate_trusts` | method | `modules/domain_dominance.py:546` | `def _enumerate_trusts(self, domain, dc_ip)` |
| `_enumerate_users` | method | `modules/domain_dominance.py:426` | `def _enumerate_users(self, dc_ip)` |
| `_find_dcs` | method | `modules/domain_dominance.py:366` | `def _find_dcs(self, domain, dc_ip)` |
| `_find_domain_admins` | method | `modules/domain_dominance.py:392` | `def _find_domain_admins(self, domain, dc_ip)` |
| `_kerberoast` | method | `modules/domain_dominance.py:625` | `def _kerberoast(self, domain_info)` |
| `_load_config` | method | `modules/domain_dominance.py:827` | `def _load_config(self)` |
| `_psexec_session` | method | `modules/domain_dominance.py:666` | `def _psexec_session(self, target, domain, user, password)` |
| `_pth_session` | method | `modules/domain_dominance.py:728` | `def _pth_session(self, target, domain, user, ntlm_hash)` |
| `_save_credential` | method | `modules/domain_dominance.py:890` | `def _save_credential(self, username, secret, secret_type, source)` |
| `_save_dominance_report` | method | `modules/domain_dominance.py:944` | `def _save_dominance_report(self)` |
| `_save_session` | method | `modules/domain_dominance.py:924` | `def _save_session(self, session_id, target, method, user)` |
| `_seal_loot_secret` | method | `modules/domain_dominance.py:850` | `def _seal_loot_secret(secret)` |
| `_unseal_loot_secret` | method | `modules/domain_dominance.py:871` | `def _unseal_loot_secret(stored)` |
| `_wmiexec_session` | method | `modules/domain_dominance.py:697` | `def _wmiexec_session(self, target, domain, user, password)` |
| `dominate` | method | `modules/domain_dominance.py:121` | `def dominate(self, domain, dc_ip, username, password, ntlm_hash)` |
| `enumerate_domain` | method | `modules/domain_dominance.py:194` | `def enumerate_domain(self, domain, dc_ip)` |
| `escalate` | method | `modules/domain_dominance.py:260` | `def escalate(self, domain_info, stash)` |
| `extract_credentials` | method | `modules/domain_dominance.py:227` | `def extract_credentials(self, domain_info, known_creds)` |
| `get_instance` | method | `modules/domain_dominance.py:110` | `def get_instance(cls)` |
| `persist` | method | `modules/domain_dominance.py:314` | `def persist(self, domain_info)` |
| `DotNetPayloadConfig` | class | `modules/dotnet_payload.py:293` | `class DotNetPayloadConfig` |
| `DotNetPayloadFactory` | class | `modules/dotnet_payload.py:315` | `class DotNetPayloadFactory` |
| `__init__` | method | `modules/dotnet_payload.py:327` | `def __init__(self, output_dir)` |
| `_detect_compiler` | method | `modules/dotnet_payload.py:333` | `def _detect_compiler()` |
| `_resolve_template` | method | `modules/dotnet_payload.py:368` | `def _resolve_template(self, config)` |
| `compile` | method | `modules/dotnet_payload.py:403` | `def compile(self, config, source_code)` |
| `generate` | method | `modules/dotnet_payload.py:454` | `def generate(self, config)` |
| `generate_inline_assembly` | method | `modules/dotnet_payload.py:500` | `def generate_inline_assembly(self, config)` |
| `generate_powershell_reflective` | method | `modules/dotnet_payload.py:481` | `def generate_powershell_reflective(self, config)` |
| `generate_source` | method | `modules/dotnet_payload.py:389` | `def generate_source(self, config)` |
| `list_templates` | method | `modules/dotnet_payload.py:364` | `def list_templates()` |
| `to_format` | method | `modules/dotnet_payload.py:520` | `def to_format(self, data, fmt)` |
| `DATA_BLOB` | class | `modules/dpapi_harvester.py:160` | `class DATA_BLOB(Structure)` |
| `DPAPICredential` | class | `modules/dpapi_harvester.py:44` | `class DPAPICredential` |
| `DPAPIHarvester` | class | `modules/dpapi_harvester.py:63` | `class DPAPIHarvester` |
| `DPAPIMasterKey` | class | `modules/dpapi_harvester.py:54` | `class DPAPIMasterKey` |
| `__init__` | method | `modules/dpapi_harvester.py:79` | `def __init__(self, sessions_dir, masterkey_path)` |
| `_crack_cookies` | method | `modules/dpapi_harvester.py:320` | `def _crack_cookies(self, cookies_path, key, source)` |
| `_crack_login_data` | method | `modules/dpapi_harvester.py:286` | `def _crack_login_data(self, login_db_path, key, source)` |
| `_extract_sid_from_file` | method | `modules/dpapi_harvester.py:355` | `def _extract_sid_from_file(filepath)` |
| `_harvest_chrome` | method | `modules/dpapi_harvester.py:143` | `def _harvest_chrome(self)` |
| `_harvest_chrome_offline` | method | `modules/dpapi_harvester.py:188` | `def _harvest_chrome_offline(self)` |
| `_harvest_credential_manager` | method | `modules/dpapi_harvester.py:120` | `def _harvest_credential_manager(self)` |
| `_harvest_edge` | method | `modules/dpapi_harvester.py:198` | `def _harvest_edge(self)` |
| `_harvest_master_keys` | method | `modules/dpapi_harvester.py:105` | `def _harvest_master_keys(self)` |
| `_harvest_rdp` | method | `modules/dpapi_harvester.py:250` | `def _harvest_rdp(self)` |
| `_harvest_wifi` | method | `modules/dpapi_harvester.py:210` | `def _harvest_wifi(self)` |
| `_harvest_windows_vault` | method | `modules/dpapi_harvester.py:262` | `def _harvest_windows_vault(self)` |
| `export_credentials` | method | `modules/dpapi_harvester.py:367` | `def export_credentials(self)` |
| `harvest_all` | method | `modules/dpapi_harvester.py:90` | `def harvest_all(self)` |
| `masterkey_report` | method | `modules/dpapi_harvester.py:386` | `def masterkey_report(self)` |
| `EDRDetector` | class | `modules/edr_detector.py:191` | `class EDRDetector` |
| `EDRFinding` | class | `modules/edr_detector.py:174` | `class EDRFinding` |
| `EDRProfile` | class | `modules/edr_detector.py:182` | `class EDRProfile` |
| `_generate_recommendations` | method | `modules/edr_detector.py:370` | `def _generate_recommendations(profile)` |
| `_local_drivers` | method | `modules/edr_detector.py:322` | `def _local_drivers()` |
| `_local_processes` | method | `modules/edr_detector.py:292` | `def _local_processes()` |
| `_local_services` | method | `modules/edr_detector.py:305` | `def _local_services()` |
| `_match_signatures` | method | `modules/edr_detector.py:335` | `def _match_signatures(profile)` |
| `_severity` | method | `modules/edr_detector.py:428` | `def _severity(profile)` |
| `detect_local` | method | `modules/edr_detector.py:202` | `def detect_local()` |
| `detect_remote_commands` | method | `modules/edr_detector.py:221` | `def detect_remote_commands(remote_type)` |
| `generate_edr_check_script` | method | `modules/edr_detector.py:440` | `def generate_edr_check_script(remote_type)` |
| `init_board` | function | `modules/eegg.sh:26` | `` |
| `move_black_pawns` | function | `modules/eegg.sh:78` | `` |
| `move_white_pawns` | function | `modules/eegg.sh:61` | `` |
| `show_board` | function | `modules/eegg.sh:40` | `` |
| `EmulationReport` | class | `modules/emulation_runner.py:69` | `class EmulationReport` |
| `EmulationResult` | class | `modules/emulation_runner.py:40` | `class EmulationResult` |
| `EmulationRunner` | class | `modules/emulation_runner.py:105` | `class EmulationRunner` |
| `EmulationStep` | class | `modules/emulation_runner.py:28` | `class EmulationStep` |
| `__init__` | method | `modules/emulation_runner.py:108` | `def __init__(self, resolver, sessions_dir, shell_opener, remote_exec_fn, playbook_loader, outcome_recorder...` |
| `_detect` | method | `modules/emulation_runner.py:159` | `def _detect(self, spec, output)` |
| `_exec` | method | `modules/emulation_runner.py:151` | `def _exec(self, spec, target, command, lhost)` |
| `_open_shell` | method | `modules/emulation_runner.py:143` | `def _open_shell(self, target, services, lhost, exploits_dir)` |
| `_playbook` | method | `modules/emulation_runner.py:135` | `def _playbook(self, name)` |
| `_publish` | method | `modules/emulation_runner.py:450` | `def _publish(self, result, target, source, dry_run, sessions)` |
| `_record` | method | `modules/emulation_runner.py:170` | `def _record(self)` |
| `_resolver_obj` | method | `modules/emulation_runner.py:127` | `def _resolver_obj(self)` |
| `_run_test` | method | `modules/emulation_runner.py:399` | `def _run_test(self, test, technique, target, spec, lhost, executor, dry_run, include_manual, report, sessions)` |
| `_stage` | method | `modules/emulation_runner.py:482` | `def _stage(self, report, sessions)` |
| `executed` | method | `modules/emulation_runner.py:81` | `def executed(self)` |
| `run` | method | `modules/emulation_runner.py:202` | `def run(self, target, techniques, playbook, platform, lhost, per_technique, include_manual, dry_run, executor...` |
| `run_steps` | method | `modules/emulation_runner.py:321` | `def run_steps(self, steps, target, executor, platform, dry_run, source)` |
| `shell` | method | `modules/emulation_runner.py:86` | `def shell(self)` |
| `techniques_for_playbook` | method | `modules/emulation_runner.py:182` | `def techniques_for_playbook(self, playbook, platform)` |
| `to_dict` | method | `modules/emulation_runner.py:53` | `def to_dict(self)` |
| `to_dict` | method | `modules/emulation_runner.py:90` | `def to_dict(self)` |
| `detail_for` | function | `modules/engage_summary.py:98` | `def detail_for(tool, text, target, sessions_dir)` |
| `full_output` | function | `modules/engage_summary.py:51` | `def full_output(step, sessions_dir)` |
| `held_scan_ports` | function | `modules/engage_summary.py:64` | `def held_scan_ports(target, sessions_dir)` |
| `marker_lines` | function | `modules/engage_summary.py:35` | `def marker_lines(text, limit)` |
| `next_actions` | function | `modules/engage_summary.py:150` | `def next_actions(target, sessions_dir, limit)` |
| `render_markdown` | function | `modules/engage_summary.py:210` | `def render_markdown(engagement_id, target, shell, steps, next_list, sessions_dir)` |
| `render_text` | function | `modules/engage_summary.py:175` | `def render_text(engagement_id, target, shell, steps, sessions_dir)` |
| `write_report` | function | `modules/engage_summary.py:247` | `def write_report(engagement_id, target, shell, steps, sessions_dir)` |
| `CollabNotificationSink` | class | `modules/engagement_hooks.py:204` | `class CollabNotificationSink(INotificationSink)` |
| `DiscordNotificationSink` | class | `modules/engagement_hooks.py:311` | `class DiscordNotificationSink(_OutboundHTTPSink)` |
| `EngagementEvent` | class | `modules/engagement_hooks.py:101` | `class EngagementEvent` |
| `EngagementNarrator` | class | `modules/engagement_hooks.py:382` | `class EngagementNarrator` |
| `INotificationSink` | class | `modules/engagement_hooks.py:150` | `class INotificationSink(ABC)` |
| `NotificationBroadcaster` | class | `modules/engagement_hooks.py:336` | `class NotificationBroadcaster` |
| `StreamEventSink` | class | `modules/engagement_hooks.py:167` | `class StreamEventSink(INotificationSink)` |
| `TelegramNotificationSink` | class | `modules/engagement_hooks.py:278` | `class TelegramNotificationSink(_OutboundHTTPSink)` |
| `_OutboundHTTPSink` | class | `modules/engagement_hooks.py:242` | `class _OutboundHTTPSink(INotificationSink)` |
| `__init__` | method | `modules/engagement_hooks.py:349` | `def __init__(self, sinks)` |
| `__init__` | method | `modules/engagement_hooks.py:393` | `def __init__(self, broadcaster)` |
| `_build_request` | method | `modules/engagement_hooks.py:255` | `def _build_request(self, event)` |
| `_build_request` | method | `modules/engagement_hooks.py:291` | `def _build_request(self, event)` |
| `_build_request` | method | `modules/engagement_hooks.py:323` | `def _build_request(self, event)` |
| `_load_payload` | function | `modules/engagement_hooks.py:88` | `def _load_payload()` |
| `_load_seen_beacons` | function | `modules/engagement_hooks.py:444` | `def _load_seen_beacons()` |
| `_persist` | method | `modules/engagement_hooks.py:417` | `def _persist(self, event)` |
| `_safe_str` | function | `modules/engagement_hooks.py:78` | `def _safe_str(value, maxlen)` |
| `_sanitize_client_id` | function | `modules/engagement_hooks.py:466` | `def _sanitize_client_id(client_id)` |
| `_save_seen_beacons` | function | `modules/engagement_hooks.py:455` | `def _save_seen_beacons(seen)` |
| `add` | method | `modules/engagement_hooks.py:365` | `def add(self, sink)` |
| `append_approval_record` | function | `modules/engagement_hooks.py:564` | `def append_approval_record(record)` |
| `default` | method | `modules/engagement_hooks.py:354` | `def default(cls)` |
| `deliver` | method | `modules/engagement_hooks.py:159` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:181` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:216` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:258` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:370` | `def deliver(self, event)` |
| `get_default_narrator` | function | `modules/engagement_hooks.py:482` | `def get_default_narrator()` |
| `is_valid_target` | function | `modules/engagement_hooks.py:626` | `def is_valid_target(value)` |
| `list_pending_approvals` | function | `modules/engagement_hooks.py:575` | `def list_pending_approvals()` |
| `name` | method | `modules/engagement_hooks.py:155` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:178` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:213` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:252` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:288` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:320` | `def name(self)` |
| `narrate` | method | `modules/engagement_hooks.py:400` | `def narrate(self, kind, target, message, payload, severity)` |
| `now` | method | `modules/engagement_hooks.py:124` | `def now(cls, kind, target, message, payload, severity)` |
| `publish_shell_obtained` | function | `modules/engagement_hooks.py:491` | `def publish_shell_obtained(client_id, primary_ip, hostname, user, platform, narrator)` |
| `render_line` | method | `modules/engagement_hooks.py:143` | `def render_line(self)` |
| `resolve_approval` | function | `modules/engagement_hooks.py:601` | `def resolve_approval(approval_id, decision, operator)` |
| `EnrichEngine` | class | `modules/enrich.py:100` | `class EnrichEngine` |
| `EnrichResult` | class | `modules/enrich.py:30` | `class EnrichResult` |
| `__init__` | method | `modules/enrich.py:103` | `def __init__(self, max_workers)` |
| `_run` | method | `modules/enrich.py:121` | `def _run(self, target)` |
| `fetch_http` | function | `modules/enrich.py:86` | `def fetch_http(target, timeout)` |
| `resolve_dns` | function | `modules/enrich.py:73` | `def resolve_dns(target, timeout)` |
| `scan_files_for` | function | `modules/enrich.py:40` | `def scan_files_for(sessions_dir, target)` |
| `shared_engine` | function | `modules/enrich.py:137` | `def shared_engine()` |
| `should_rescan` | function | `modules/enrich.py:57` | `def should_rescan(sessions_dir, target, fresh_sec)` |
| `shutdown` | method | `modules/enrich.py:128` | `def shutdown(self, wait)` |
| `submit` | method | `modules/enrich.py:108` | `def submit(self, target)` |
| `EntraIDAttackEngine` | class | `modules/entra_id_attacks.py:81` | `class EntraIDAttackEngine` |
| `EntraIDConfig` | class | `modules/entra_id_attacks.py:57` | `class EntraIDConfig` |
| `__init__` | method | `modules/entra_id_attacks.py:92` | `def __init__(self, config)` |
| `conditional_access_bypass` | method | `modules/entra_id_attacks.py:307` | `def conditional_access_bypass(self)` |
| `device_code_phish` | method | `modules/entra_id_attacks.py:96` | `def device_code_phish(self, scope)` |
| `entra_connect_sync_abuse` | method | `modules/entra_id_attacks.py:266` | `def entra_connect_sync_abuse(self)` |
| `enumerate_tenant` | method | `modules/entra_id_attacks.py:345` | `def enumerate_tenant(self)` |
| `managed_identity_abuse` | method | `modules/entra_id_attacks.py:235` | `def managed_identity_abuse(self, resource)` |
| `oauth_consent_grant` | method | `modules/entra_id_attacks.py:166` | `def oauth_consent_grant(self, redirect_uri)` |
| `poll_device_code` | method | `modules/entra_id_attacks.py:129` | `def poll_device_code(self, device_code, interval, timeout)` |
| `service_principal_credential_theft` | method | `modules/entra_id_attacks.py:203` | `def service_principal_credential_theft(self)` |
| `summary` | method | `modules/entra_id_attacks.py:368` | `def summary(self)` |
| `_from_raw` | function | `modules/estorides_fusion.py:142` | `def _from_raw(document)` |
| `_norm` | function | `modules/estorides_fusion.py:123` | `def _norm(value)` |
| `community_for` | function | `modules/estorides_fusion.py:180` | `def community_for(kind, value)` |
| `estorides_checkout` | function | `modules/estorides_fusion.py:48` | `def estorides_checkout()` |
| `find_export` | function | `modules/estorides_fusion.py:68` | `def find_export(sessions_dir)` |
| `find_lan_bundle` | function | `modules/estorides_fusion.py:268` | `def find_lan_bundle(sessions_dir)` |
| `load_export` | function | `modules/estorides_fusion.py:128` | `def load_export(path)` |
| `load_lan_bundle` | function | `modules/estorides_fusion.py:288` | `def load_lan_bundle(path)` |
| `merge_estorides` | function | `modules/estorides_fusion.py:187` | `def merge_estorides(nodes, edges, est, cap)` |
| `run_export` | function | `modules/estorides_fusion.py:84` | `def run_export(sessions_dir, cli_path, timeout_sec)` |
| `split_lan_targets` | function | `modules/estorides_fusion.py:323` | `def split_lan_targets(est)` |
| `EstoridesCaseReader` | class | `modules/estorides_importer.py:387` | `class EstoridesCaseReader` |
| `EstoridesEntity` | class | `modules/estorides_importer.py:84` | `class EstoridesEntity` |
| `EstoridesStixParser` | class | `modules/estorides_importer.py:497` | `class EstoridesStixParser` |
| `EstoridesToLazyOwnBridge` | class | `modules/estorides_importer.py:702` | `class EstoridesToLazyOwnBridge` |
| `FeedbackLoop` | class | `modules/estorides_importer.py:885` | `class FeedbackLoop` |
| `ImportResult` | class | `modules/estorides_importer.py:96` | `class ImportResult` |
| `LanBundleReader` | class | `modules/estorides_importer.py:624` | `class LanBundleReader` |
| `SeedResult` | class | `modules/estorides_importer.py:128` | `class SeedResult` |
| `__init__` | method | `modules/estorides_importer.py:390` | `def __init__(self, db_path)` |
| `__init__` | method | `modules/estorides_importer.py:513` | `def __init__(self, stix_path)` |
| `__init__` | method | `modules/estorides_importer.py:634` | `def __init__(self, lan_dir)` |
| `__init__` | method | `modules/estorides_importer.py:705` | `def __init__(self, db_path, config_path)` |
| `__init__` | method | `modules/estorides_importer.py:896` | `def __init__(self, max_iterations, max_depth, max_steps, timeout)` |
| `_ensure_conn` | method | `modules/estorides_importer.py:398` | `def _ensure_conn(self)` |
| `_extract_value` | method | `modules/estorides_importer.py:565` | `def _extract_value(obj, stix_type)` |
| `_gather_seeds` | method | `modules/estorides_importer.py:1005` | `def _gather_seeds(self, methods, seen)` |
| `_import_to_db` | method | `modules/estorides_importer.py:757` | `def _import_to_db(self, imports, result)` |
| `_import_to_scope` | method | `modules/estorides_importer.py:803` | `def _import_to_scope(self, imports, result)` |
| `attack_targets` | method | `modules/estorides_importer.py:685` | `def attack_targets(self)` |
| `available` | method | `modules/estorides_importer.py:395` | `def available(self)` |
| `available` | method | `modules/estorides_importer.py:517` | `def available(self)` |
| `available` | method | `modules/estorides_importer.py:638` | `def available(self)` |
| `close` | method | `modules/estorides_importer.py:491` | `def close(self)` |
| `ensure_directories` | function | `modules/estorides_importer.py:696` | `def ensure_directories()` |
| `export_combined_graph` | function | `modules/estorides_importer.py:1031` | `def export_combined_graph(output_path)` |
| `extract_seeds_from_db` | function | `modules/estorides_importer.py:205` | `def extract_seeds_from_db(db_path)` |
| `extract_seeds_from_hosts_file` | function | `modules/estorides_importer.py:177` | `def extract_seeds_from_hosts_file(path)` |
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

Next: [SYMBOLS_p14.md](SYMBOLS_p14.md)
