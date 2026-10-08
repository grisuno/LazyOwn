# Symbols (page 11 of 35)
Previous: [SYMBOLS_p10.md](SYMBOLS_p10.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `get_executor` | method | `modules/command_executor.py:264` | `def get_executor()` |
| `instance` | method | `modules/command_executor.py:63` | `def instance(cls)` |
| `run` | method | `modules/command_executor.py:72` | `def run(self, command, timeout, stream)` |
| `run_with_tee` | method | `modules/command_executor.py:172` | `def run_with_tee(self, command, output_path, timeout)` |
| `ComplianceEngine` | class | `modules/compliance.py:468` | `class ComplianceEngine` |
| `ComplianceFinding` | class | `modules/compliance.py:456` | `class ComplianceFinding` |
| `EvidenceChain` | class | `modules/compliance.py:192` | `class EvidenceChain` |
| `EvidenceEntry` | class | `modules/compliance.py:183` | `class EvidenceEntry` |
| `__init__` | method | `modules/compliance.py:200` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/compliance.py:471` | `def __init__(self, sessions_dir)` |
| `_append_to_file` | method | `modules/compliance.py:246` | `def _append_to_file(self, entry)` |
| `_count_by_category` | method | `modules/compliance.py:613` | `def _count_by_category(self, findings)` |
| `_count_by_severity` | method | `modules/compliance.py:606` | `def _count_by_severity(self, findings)` |
| `_format_compliance_report_md` | method | `modules/compliance.py:672` | `def _format_compliance_report_md(self, report)` |
| `_hash_entry` | method | `modules/compliance.py:222` | `def _hash_entry(self, entry)` |
| `_load` | method | `modules/compliance.py:207` | `def _load(self)` |
| `_load_findings` | method | `modules/compliance.py:620` | `def _load_findings(self)` |
| `add_evidence` | method | `modules/compliance.py:736` | `def add_evidence(self, filepath, operator, description)` |
| `add_file` | method | `modules/compliance.py:226` | `def add_file(self, filepath, operator, description)` |
| `export_pdf` | method | `modules/compliance.py:291` | `def export_pdf(report_md, output_path, title, classification)` |
| `export_pdf` | method | `modules/compliance.py:668` | `def export_pdf(self, report, output_path)` |
| `export_to_cef` | method | `modules/compliance.py:413` | `def export_to_cef(findings, output_path, vendor, product, version)` |
| `export_to_elastic_ndjson` | method | `modules/compliance.py:373` | `def export_to_elastic_ndjson(findings, output_path, index_prefix)` |
| `generate_compliance_report` | method | `modules/compliance.py:551` | `def generate_compliance_report(self, findings, include_evidence_chain, include_siem_formats)` |
| `get_chain_digest` | method | `modules/compliance.py:272` | `def get_chain_digest(self)` |
| `map_findings_to_compliance` | method | `modules/compliance.py:475` | `def map_findings_to_compliance(self, findings, frameworks)` |
| `to_report` | method | `modules/compliance.py:275` | `def to_report(self)` |
| `verify` | method | `modules/compliance.py:253` | `def verify(self)` |
| `verify_evidence_chain` | method | `modules/compliance.py:739` | `def verify_evidence_chain(self)` |
| `HookEngine` | class | `modules/conditional_hooks.py:250` | `class HookEngine` |
| `HookRule` | class | `modules/conditional_hooks.py:45` | `class HookRule` |
| `__init__` | method | `modules/conditional_hooks.py:262` | `def __init__(self)` |
| `_execute_action` | method | `modules/conditional_hooks.py:422` | `def _execute_action(self, action, context)` |
| `_execute_cred_reuse` | method | `modules/conditional_hooks.py:498` | `def _execute_cred_reuse(self, context)` |
| `_execute_local_command` | method | `modules/conditional_hooks.py:472` | `def _execute_local_command(command)` |
| `_execute_shell_command` | method | `modules/conditional_hooks.py:461` | `def _execute_shell_command(self, command, context)` |
| `_match_trigger` | method | `modules/conditional_hooks.py:361` | `def _match_trigger(self, rule_trigger, event, context)` |
| `_resolve_placeholders` | method | `modules/conditional_hooks.py:408` | `def _resolve_placeholders(self, text, context)` |
| `add_rule` | method | `modules/conditional_hooks.py:322` | `def add_rule(self, rule_dict)` |
| `can_fire` | method | `modules/conditional_hooks.py:56` | `def can_fire(self, now)` |
| `enable_rule` | method | `modules/conditional_hooks.py:351` | `def enable_rule(self, name, enabled)` |
| `fire` | method | `modules/conditional_hooks.py:514` | `def fire(self, event, context)` |
| `get_hook_engine` | method | `modules/conditional_hooks.py:580` | `def get_hook_engine()` |
| `get_rule` | method | `modules/conditional_hooks.py:569` | `def get_rule(self, name)` |
| `list_rules` | method | `modules/conditional_hooks.py:565` | `def list_rules(self)` |
| `load_rules` | method | `modules/conditional_hooks.py:282` | `def load_rules(self, path)` |
| `mark_fired` | method | `modules/conditional_hooks.py:65` | `def mark_fired(self)` |
| `register_action_handler` | method | `modules/conditional_hooks.py:269` | `def register_action_handler(self, action_type, handler)` |
| `remove_rule` | method | `modules/conditional_hooks.py:337` | `def remove_rule(self, name)` |
| `save_rules` | method | `modules/conditional_hooks.py:314` | `def save_rules(self, path)` |
| `set_placeholders` | method | `modules/conditional_hooks.py:278` | `def set_placeholders(self, placeholders)` |
| `to_dict` | method | `modules/conditional_hooks.py:69` | `def to_dict(self)` |
| `_ensure_loaded` | function | `modules/config_store.py:104` | `def _ensure_loaded()` |
| `_load` | function | `modules/config_store.py:111` | `def _load()` |
| `_persist` | function | `modules/config_store.py:129` | `def _persist()` |
| `_start_watcher` | function | `modules/config_store.py:141` | `def _start_watcher(interval)` |
| `_watch_loop` | function | `modules/config_store.py:146` | `def _watch_loop()` |
| `get_config` | function | `modules/config_store.py:52` | `def get_config(key, default)` |
| `init` | function | `modules/config_store.py:35` | `def init(path, watch)` |
| `reload_config` | function | `modules/config_store.py:89` | `def reload_config()` |
| `set_config` | function | `modules/config_store.py:65` | `def set_config()` |
| `set_config_dict` | function | `modules/config_store.py:79` | `def set_config_dict(updates)` |
| `stop_watcher` | function | `modules/config_store.py:95` | `def stop_watcher()` |
| `CredentialReuseEngine` | class | `modules/credential_reuse.py:55` | `class CredentialReuseEngine` |
| `ReuseCandidate` | class | `modules/credential_reuse.py:32` | `class ReuseCandidate` |
| `__init__` | method | `modules/credential_reuse.py:80` | `def __init__(self)` |
| `_build_command` | method | `modules/credential_reuse.py:196` | `def _build_command(self, username, password, host, target_services)` |
| `_load_cache` | method | `modules/credential_reuse.py:85` | `def _load_cache(self)` |
| `_save_cache` | method | `modules/credential_reuse.py:95` | `def _save_cache(self)` |
| `_score_candidate` | method | `modules/credential_reuse.py:144` | `def _score_candidate(self, username, password, source_host, target_host, target_services)` |
| `_subnet_distance` | method | `modules/credential_reuse.py:118` | `def _subnet_distance(self, ip_a, ip_b)` |
| `get_credential_reuse_engine` | method | `modules/credential_reuse.py:365` | `def get_credential_reuse_engine()` |
| `get_summary` | method | `modules/credential_reuse.py:343` | `def get_summary(self, candidates)` |
| `mark_confirmed` | method | `modules/credential_reuse.py:112` | `def mark_confirmed(self, username, password, host)` |
| `mark_failed` | method | `modules/credential_reuse.py:107` | `def mark_failed(self, username, password, host)` |
| `rank` | method | `modules/credential_reuse.py:226` | `def rank(self, hosts, creds, host_services, limit)` |
| `suggest_from_state_manager` | method | `modules/credential_reuse.py:280` | `def suggest_from_state_manager(self, state_manager, limit)` |
| `suggest_from_world_model` | method | `modules/credential_reuse.py:310` | `def suggest_from_world_model(self, world_model, limit)` |
| `to_dict` | method | `modules/credential_reuse.py:43` | `def to_dict(self)` |
| `CrossCloudAttackEngine` | class | `modules/cross_cloud.py:54` | `class CrossCloudAttackEngine` |
| `CrossCloudConfig` | class | `modules/cross_cloud.py:30` | `class CrossCloudConfig` |
| `__init__` | method | `modules/cross_cloud.py:64` | `def __init__(self, config)` |
| `aws_oidc_to_gcp` | method | `modules/cross_cloud.py:133` | `def aws_oidc_to_gcp(self)` |
| `azure_saml_to_aws` | method | `modules/cross_cloud.py:67` | `def azure_saml_to_aws(self)` |
| `detect_cross_cloud_federation` | method | `modules/cross_cloud.py:234` | `def detect_cross_cloud_federation(self)` |
| `entra_id_to_gcp_workforce_federation` | method | `modules/cross_cloud.py:204` | `def entra_id_to_gcp_workforce_federation(self)` |
| `gcp_oidc_to_azure` | method | `modules/cross_cloud.py:104` | `def gcp_oidc_to_azure(self)` |
| `multi_cloud_imds_harvesting` | method | `modules/cross_cloud.py:167` | `def multi_cloud_imds_harvesting(self)` |
| `summary` | method | `modules/cross_cloud.py:258` | `def summary(self)` |
| `CVEMatcher` | class | `modules/cve_matcher.py:59` | `class CVEMatcher` |
| `CVEResult` | class | `modules/cve_matcher.py:50` | `class CVEResult` |
| `__init__` | method | `modules/cve_matcher.py:69` | `def __init__(self, api_key, cache_dir)` |
| `_cache_path` | method | `modules/cve_matcher.py:94` | `def _cache_path(self, params)` |
| `_load_cache` | method | `modules/cve_matcher.py:99` | `def _load_cache(self, params)` |
| `_query` | method | `modules/cve_matcher.py:127` | `def _query(self)` |
| `_rate_limit` | method | `modules/cve_matcher.py:120` | `def _rate_limit(self)` |
| `_save_cache` | method | `modules/cve_matcher.py:111` | `def _save_cache(self, params, results)` |
| `get_matcher` | method | `modules/cve_matcher.py:195` | `def get_matcher()` |
| `search` | method | `modules/cve_matcher.py:81` | `def search(self)` |
| `search` | method | `modules/cve_matcher.py:203` | `def search(product, version, max_results)` |
| `search_by_cpe` | method | `modules/cve_matcher.py:88` | `def search_by_cpe(self, cpe_name, max_results)` |
| `ACEntry` | class | `modules/dacl_abuse.py:67` | `class ACEntry` |
| `ACLTarget` | class | `modules/dacl_abuse.py:91` | `class ACLTarget` |
| `DACLAbuseEngine` | class | `modules/dacl_abuse.py:113` | `class DACLAbuseEngine` |
| `__init__` | method | `modules/dacl_abuse.py:136` | `def __init__(self, domain, domain_sid, acl_data)` |
| `_calculate_severity` | method | `modules/dacl_abuse.py:382` | `def _calculate_severity(target)` |
| `_extract_cn` | method | `modules/dacl_abuse.py:412` | `def _extract_cn(dn)` |
| `_guess_object_type` | method | `modules/dacl_abuse.py:395` | `def _guess_object_type(dn)` |
| `_is_dangerous_ace` | method | `modules/dacl_abuse.py:377` | `def _is_dangerous_ace(ace)` |
| `adminsdholder_abuse_plan` | method | `modules/dacl_abuse.py:289` | `def adminsdholder_abuse_plan(self, target_sid)` |
| `compute_attack_chains` | method | `modules/dacl_abuse.py:224` | `def compute_attack_chains(self)` |
| `dcsync_rights_assignment_plan` | method | `modules/dacl_abuse.py:316` | `def dcsync_rights_assignment_plan(self, target_sid, domain_dn)` |
| `owner_takeover_plan` | method | `modules/dacl_abuse.py:346` | `def owner_takeover_plan(self, target_dn, attacker_sid)` |
| `parse_bloodhound_acls` | method | `modules/dacl_abuse.py:143` | `def parse_bloodhound_acls(self, edges)` |
| `parse_raw_aces` | method | `modules/dacl_abuse.py:182` | `def parse_raw_aces(self, raw_nthashes)` |
| `summary` | method | `modules/dacl_abuse.py:416` | `def summary(self)` |
| `_aggregate_data` | function | `modules/dashboard_bp.py:110` | `def _aggregate_data()` |
| `_count_lines` | function | `modules/dashboard_bp.py:100` | `def _count_lines(path)` |
| `_normalize_ts` | function | `modules/dashboard_bp.py:901` | `def _normalize_ts(raw)` |
| `_read_json` | function | `modules/dashboard_bp.py:90` | `def _read_json(path)` |
| `_read_jsonl` | function | `modules/dashboard_bp.py:68` | `def _read_jsonl(path, last_n)` |
| `_read_loot` | function | `modules/dashboard_bp.py:805` | `def _read_loot()` |
| `_read_loot_lines` | function | `modules/dashboard_bp.py:788` | `def _read_loot_lines(pattern)` |
| `_read_timeline` | function | `modules/dashboard_bp.py:922` | `def _read_timeline()` |
| `_require_login` | function | `modules/dashboard_bp.py:29` | `def _require_login()` |
| `dashboard_api_data` | function | `modules/dashboard_bp.py:772` | `def dashboard_api_data()` |
| `dashboard_index` | function | `modules/dashboard_bp.py:766` | `def dashboard_index()` |
| `dashboard_loot` | function | `modules/dashboard_bp.py:890` | `def dashboard_loot()` |
| `dashboard_timeline` | function | `modules/dashboard_bp.py:1001` | `def dashboard_timeline()` |
| `DashboardEdge` | class | `modules/dashboard_engine.py:102` | `class DashboardEdge` |
| `DashboardEngine` | class | `modules/dashboard_engine.py:109` | `class DashboardEngine` |
| `DashboardNode` | class | `modules/dashboard_engine.py:90` | `class DashboardNode` |
| `__init__` | method | `modules/dashboard_engine.py:130` | `def __init__(self, world_model)` |
| `_parse_nmap_xml_services` | function | `modules/dashboard_engine.py:31` | `def _parse_nmap_xml_services(sessions_dir)` |
| `_phase_icon` | method | `modules/dashboard_engine.py:384` | `def _phase_icon(phase)` |
| `build_snapshot` | method | `modules/dashboard_engine.py:151` | `def build_snapshot(self)` |
| `export_json` | method | `modules/dashboard_engine.py:394` | `def export_json(self, snapshot)` |
| `format_for_cli` | method | `modules/dashboard_engine.py:424` | `def format_for_cli(self, snapshot)` |
| `persist_snapshot` | method | `modules/dashboard_engine.py:407` | `def persist_snapshot(self, snapshot)` |
| `render_ascii_topology` | method | `modules/dashboard_engine.py:343` | `def render_ascii_topology(self, snapshot)` |
| `render_text_map` | method | `modules/dashboard_engine.py:261` | `def render_text_map(self, snapshot)` |
| `set_auto_pivot` | method | `modules/dashboard_engine.py:145` | `def set_auto_pivot(self, pivot)` |
| `set_evasion_engine` | method | `modules/dashboard_engine.py:148` | `def set_evasion_engine(self, evasion)` |
| `set_exploit_recommender` | method | `modules/dashboard_engine.py:142` | `def set_exploit_recommender(self, recommender)` |
| `set_world_model` | method | `modules/dashboard_engine.py:139` | `def set_world_model(self, model)` |
| `LazyOwnDB` | class | `modules/db.py:147` | `class LazyOwnDB` |
| `__init__` | method | `modules/db.py:159` | `def __init__(self, db_path)` |
| `_current_version` | method | `modules/db.py:192` | `def _current_version(self)` |
| `_cursor` | method | `modules/db.py:237` | `def _cursor(self)` |
| `_get_conn` | method | `modules/db.py:171` | `def _get_conn(self)` |
| `_init_schema` | method | `modules/db.py:186` | `def _init_schema(self)` |
| `_maybe_decrypt` | method | `modules/db.py:275` | `def _maybe_decrypt(self, value)` |
| `_maybe_encrypt` | method | `modules/db.py:253` | `def _maybe_encrypt(self, value)` |
| `_run_migrations` | method | `modules/db.py:199` | `def _run_migrations(self)` |
| `close` | method | `modules/db.py:762` | `def close(self)` |
| `cred_add` | method | `modules/db.py:513` | `def cred_add(self, host_id, username, password, realm, cred_type, origin)` |
| `cred_list` | method | `modules/db.py:533` | `def cred_list(self, workspace_id)` |
| `db_path` | method | `modules/db.py:182` | `def db_path(self)` |
| `default_workspace` | method | `modules/db.py:321` | `def default_workspace(self, name)` |
| `export_csv` | method | `modules/db.py:698` | `def export_csv(self, table, workspace_id)` |
| `get_db` | method | `modules/db.py:779` | `def get_db(db_path)` |
| `host_add` | method | `modules/db.py:363` | `def host_add(self, workspace_id, address, mac, hostname, os, state)` |
| `host_delete` | method | `modules/db.py:396` | `def host_delete(self, host_id)` |
| `host_find` | method | `modules/db.py:416` | `def host_find(self, workspace_id, query)` |
| `host_list` | method | `modules/db.py:407` | `def host_list(self, workspace_id)` |
| `import_nmap_xml` | method | `modules/db.py:620` | `def import_nmap_xml(self, workspace_id, xml_path)` |
| `loot_add` | method | `modules/db.py:552` | `def loot_add(self, workspace_id, name, loot_type, path, notes, host_id)` |
| `loot_list` | method | `modules/db.py:571` | `def loot_list(self, workspace_id)` |
| `migration_status` | method | `modules/db.py:224` | `def migration_status(self)` |
| `note_add` | method | `modules/db.py:587` | `def note_add(self, workspace_id, data, note_type, host_id)` |
| `note_list` | method | `modules/db.py:604` | `def note_list(self, workspace_id)` |
| `service_add` | method | `modules/db.py:433` | `def service_add(self, host_id, port, protocol, state, name, product, version)` |
| `service_list` | method | `modules/db.py:453` | `def service_list(self, host_id)` |
| `status` | method | `modules/db.py:733` | `def status(self, workspace_id)` |
| `vuln_add` | method | `modules/db.py:466` | `def vuln_add(self, host_id, name, severity, description, refs)` |
| `vuln_list` | method | `modules/db.py:484` | `def vuln_list(self, workspace_id, severity)` |
| `workspace_create` | method | `modules/db.py:293` | `def workspace_create(self, name, description)` |
| `workspace_delete` | method | `modules/db.py:334` | `def workspace_delete(self, name)` |
| `workspace_get` | method | `modules/db.py:314` | `def workspace_get(self, name)` |
| `workspace_list` | method | `modules/db.py:308` | `def workspace_list(self)` |
| `DelegationAttackPath` | class | `modules/delegation_attacks.py:63` | `class DelegationAttackPath` |
| `DelegationEnumerator` | class | `modules/delegation_attacks.py:85` | `class DelegationEnumerator` |
| `DelegationTarget` | class | `modules/delegation_attacks.py:32` | `class DelegationTarget` |
| `__init__` | method | `modules/delegation_attacks.py:98` | `def __init__(self, domain, raw_ldap_output)` |
| `compute_attack_paths` | method | `modules/delegation_attacks.py:215` | `def compute_attack_paths(self)` |
| `enumerate_from_uac_flags` | method | `modules/delegation_attacks.py:104` | `def enumerate_from_uac_flags(self, accounts)` |
| `find_constrained_targets` | method | `modules/delegation_attacks.py:187` | `def find_constrained_targets(self)` |
| `find_dc_targets` | method | `modules/delegation_attacks.py:203` | `def find_dc_targets(self)` |
| `find_rbcd_targets` | method | `modules/delegation_attacks.py:195` | `def find_rbcd_targets(self)` |
| `find_unconstrained_targets` | method | `modules/delegation_attacks.py:179` | `def find_unconstrained_targets(self)` |
| `parse_bloodhound_output` | method | `modules/delegation_attacks.py:149` | `def parse_bloodhound_output(self, bloodhound_json)` |
| `summary` | method | `modules/delegation_attacks.py:296` | `def summary(self)` |
| `obtener_informacion` | function | `modules/detailed_search.py:38` | `def obtener_informacion(url)` |
| `DetectionFeed` | class | `modules/detection_feed.py:72` | `class DetectionFeed` |
| `FeedResult` | class | `modules/detection_feed.py:63` | `class FeedResult` |
| `__init__` | method | `modules/detection_feed.py:82` | `def __init__(self, cache_dir, sources)` |
| `_cache_rules` | method | `modules/detection_feed.py:216` | `def _cache_rules(self, rules, source)` |
| `_extract_categories` | method | `modules/detection_feed.py:203` | `def _extract_categories(self, doc)` |
| `_extract_keywords` | method | `modules/detection_feed.py:186` | `def _extract_keywords(self, doc)` |
| `_extract_log_source` | method | `modules/detection_feed.py:169` | `def _extract_log_source(self, doc)` |
| `_extract_mitre` | method | `modules/detection_feed.py:177` | `def _extract_mitre(self, doc)` |
| `_parse_sigma_feed` | method | `modules/detection_feed.py:124` | `def _parse_sigma_feed(self, text)` |
| `adjust_from_feedback` | method | `modules/detection_feed.py:263` | `def adjust_from_feedback(self, feedback_file)` |
| `get_feed` | method | `modules/detection_feed.py:317` | `def get_feed()` |
| `load_cached_rules` | method | `modules/detection_feed.py:241` | `def load_cached_rules(self, source)` |
| `update_rules` | method | `modules/detection_feed.py:91` | `def update_rules(self, source)` |
| `DetectionAssessment` | class | `modules/detection_oracle.py:62` | `class DetectionAssessment` |
| `DetectionOracle` | class | `modules/detection_oracle.py:323` | `class DetectionOracle(IDetectionOracle)` |
| `IDetectionOracle` | class | `modules/detection_oracle.py:89` | `class IDetectionOracle(ABC)` |
| `SigmaRule` | class | `modules/detection_oracle.py:49` | `class SigmaRule` |
| `__init__` | method | `modules/detection_oracle.py:338` | `def __init__(self, rules, feed)` |
| `_aggregate_probability` | method | `modules/detection_oracle.py:432` | `def _aggregate_probability(self, matched, action_category)` |
| `_build_recommendation` | method | `modules/detection_oracle.py:449` | `def _build_recommendation(probability, matched, action_category)` |
| `_effective_probability` | method | `modules/detection_oracle.py:422` | `def _effective_probability(rule, action_category)` |
| `_match_rules` | method | `modules/detection_oracle.py:402` | `def _match_rules(self, text, action_category)` |
| `assess` | method | `modules/detection_oracle.py:93` | `def assess(self, command, args, action_category)` |
| `assess` | method | `modules/detection_oracle.py:376` | `def assess(self, command, args, action_category)` |
| `get_oracle` | method | `modules/detection_oracle.py:486` | `def get_oracle()` |
| `is_critical_risk` | method | `modules/detection_oracle.py:79` | `def is_critical_risk(self)` |
| `is_high_risk` | method | `modules/detection_oracle.py:74` | `def is_high_risk(self)` |
| `probability` | method | `modules/detection_oracle.py:102` | `def probability(self, command, args, action_category)` |
| `probability` | method | `modules/detection_oracle.py:397` | `def probability(self, command, args, action_category)` |
| `refresh` | method | `modules/detection_oracle.py:342` | `def refresh(self)` |
| `DNSBeacon` | class | `modules/dns_beacon.py:23` | `class DNSBeacon` |
| `DNSC2Server` | class | `modules/dns_beacon.py:193` | `class DNSC2Server` |
| `__init__` | method | `modules/dns_beacon.py:38` | `def __init__(self, domain, dns_server, sleep_seconds, jitter_percent, dns_type, encode_method)` |
| `__init__` | method | `modules/dns_beacon.py:205` | `def __init__(self, domain, log_source, interface)` |
| `_build_query` | method | `modules/dns_beacon.py:94` | `def _build_query(self, msg_type, payload)` |
| `_decode` | method | `modules/dns_beacon.py:70` | `def _decode(self, data)` |
| `_dns_query` | method | `modules/dns_beacon.py:83` | `def _dns_query(self, name, qtype)` |
| `_encode` | method | `modules/dns_beacon.py:63` | `def _encode(self, data)` |
| `_ensure_dnspython` | method | `modules/dns_beacon.py:57` | `def _ensure_dnspython(self)` |
| `_handle_result` | method | `modules/dns_beacon.py:288` | `def _handle_result(self, labels, query)` |
| `_jittered_sleep` | method | `modules/dns_beacon.py:78` | `def _jittered_sleep(self)` |
| `check_in` | method | `modules/dns_beacon.py:103` | `def check_in(self)` |
| `get_results` | method | `modules/dns_beacon.py:321` | `def get_results(self, beacon_id)` |
| `list_beacons` | method | `modules/dns_beacon.py:229` | `def list_beacons(self)` |
| `process_query_log` | method | `modules/dns_beacon.py:242` | `def process_query_log(self, line)` |
| `register_beacon` | method | `modules/dns_beacon.py:219` | `def register_beacon(self, beacon_id, hostname)` |
| `run` | method | `modules/dns_beacon.py:165` | `def run(self)` |
| `send_result` | method | `modules/dns_beacon.py:132` | `def send_result(self, command, output, exit_code)` |
| `send_task` | method | `modules/dns_beacon.py:233` | `def send_task(self, beacon_id, command)` |
| `CredentialStash` | class | `modules/domain_dominance.py:65` | `class CredentialStash` |
| `DomainDominance` | class | `modules/domain_dominance.py:89` | `class DomainDominance` |
| `DomainInfo` | class | `modules/domain_dominance.py:49` | `class DomainInfo` |
| `DominanceResult` | class | `modules/domain_dominance.py:75` | `class DominanceResult` |
| `__init__` | method | `modules/domain_dominance.py:103` | `def __init__(self)` |
| `_asrep_roast` | method | `modules/domain_dominance.py:556` | `def _asrep_roast(self, domain_info)` |
| `_attempt_dcsync` | method | `modules/domain_dominance.py:730` | `def _attempt_dcsync(self, dc_ip)` |
| `_discover_dc` | method | `modules/domain_dominance.py:344` | `def _discover_dc(self, domain, dns_servers)` |
| `_domain_to_dn` | method | `modules/domain_dominance.py:796` | `def _domain_to_dn(self, domain)` |
| `_enumerate_computers` | method | `modules/domain_dominance.py:459` | `def _enumerate_computers(self, dc_ip)` |
| `_enumerate_groups` | method | `modules/domain_dominance.py:483` | `def _enumerate_groups(self, dc_ip)` |
| `_enumerate_spns` | method | `modules/domain_dominance.py:502` | `def _enumerate_spns(self, dc_ip)` |
| `_enumerate_trusts` | method | `modules/domain_dominance.py:529` | `def _enumerate_trusts(self, domain, dc_ip)` |
| `_enumerate_users` | method | `modules/domain_dominance.py:420` | `def _enumerate_users(self, dc_ip)` |
| `_find_dcs` | method | `modules/domain_dominance.py:368` | `def _find_dcs(self, domain, dc_ip)` |
| `_find_domain_admins` | method | `modules/domain_dominance.py:392` | `def _find_domain_admins(self, domain, dc_ip)` |
| `_kerberoast` | method | `modules/domain_dominance.py:592` | `def _kerberoast(self, domain_info)` |
| `_load_config` | method | `modules/domain_dominance.py:785` | `def _load_config(self)` |
| `_psexec_session` | method | `modules/domain_dominance.py:629` | `def _psexec_session(self, target, domain, user, password)` |
| `_pth_session` | method | `modules/domain_dominance.py:691` | `def _pth_session(self, target, domain, user, ntlm_hash)` |
| `_save_credential` | method | `modules/domain_dominance.py:807` | `def _save_credential(self, username, secret, secret_type, source)` |
| `_save_dominance_report` | method | `modules/domain_dominance.py:847` | `def _save_dominance_report(self)` |
| `_save_session` | method | `modules/domain_dominance.py:825` | `def _save_session(self, session_id, target, method, user)` |
| `_wmiexec_session` | method | `modules/domain_dominance.py:660` | `def _wmiexec_session(self, target, domain, user, password)` |
| `dominate` | method | `modules/domain_dominance.py:121` | `def dominate(self, domain, dc_ip, username, password, ntlm_hash)` |
| `enumerate_domain` | method | `modules/domain_dominance.py:194` | `def enumerate_domain(self, domain, dc_ip)` |
| `escalate` | method | `modules/domain_dominance.py:262` | `def escalate(self, domain_info, stash)` |
| `extract_credentials` | method | `modules/domain_dominance.py:229` | `def extract_credentials(self, domain_info, known_creds)` |
| `get_instance` | method | `modules/domain_dominance.py:110` | `def get_instance(cls)` |
| `persist` | method | `modules/domain_dominance.py:318` | `def persist(self, domain_info)` |
| `DotNetPayloadConfig` | class | `modules/dotnet_payload.py:298` | `class DotNetPayloadConfig` |
| `DotNetPayloadFactory` | class | `modules/dotnet_payload.py:320` | `class DotNetPayloadFactory` |
| `__init__` | method | `modules/dotnet_payload.py:332` | `def __init__(self, output_dir)` |
| `_detect_compiler` | method | `modules/dotnet_payload.py:338` | `def _detect_compiler()` |
| `_resolve_template` | method | `modules/dotnet_payload.py:373` | `def _resolve_template(self, config)` |
| `compile` | method | `modules/dotnet_payload.py:408` | `def compile(self, config, source_code)` |
| `generate` | method | `modules/dotnet_payload.py:459` | `def generate(self, config)` |
| `generate_inline_assembly` | method | `modules/dotnet_payload.py:505` | `def generate_inline_assembly(self, config)` |
| `generate_powershell_reflective` | method | `modules/dotnet_payload.py:486` | `def generate_powershell_reflective(self, config)` |
| `generate_source` | method | `modules/dotnet_payload.py:394` | `def generate_source(self, config)` |
| `list_templates` | method | `modules/dotnet_payload.py:369` | `def list_templates()` |
| `to_format` | method | `modules/dotnet_payload.py:525` | `def to_format(self, data, fmt)` |
| `DATA_BLOB` | class | `modules/dpapi_harvester.py:155` | `class DATA_BLOB(Structure)` |
| `DPAPICredential` | class | `modules/dpapi_harvester.py:44` | `class DPAPICredential` |
| `DPAPIHarvester` | class | `modules/dpapi_harvester.py:63` | `class DPAPIHarvester` |
| `DPAPIMasterKey` | class | `modules/dpapi_harvester.py:54` | `class DPAPIMasterKey` |
| `__init__` | method | `modules/dpapi_harvester.py:79` | `def __init__(self, sessions_dir, masterkey_path)` |
| `_crack_cookies` | method | `modules/dpapi_harvester.py:286` | `def _crack_cookies(self, cookies_path, key, source)` |
| `_crack_login_data` | method | `modules/dpapi_harvester.py:259` | `def _crack_login_data(self, login_db_path, key, source)` |
| `_extract_sid_from_file` | method | `modules/dpapi_harvester.py:317` | `def _extract_sid_from_file(filepath)` |
| `_harvest_chrome` | method | `modules/dpapi_harvester.py:137` | `def _harvest_chrome(self)` |
| `_harvest_chrome_offline` | method | `modules/dpapi_harvester.py:177` | `def _harvest_chrome_offline(self)` |
| `_harvest_credential_manager` | method | `modules/dpapi_harvester.py:118` | `def _harvest_credential_manager(self)` |
| `_harvest_edge` | method | `modules/dpapi_harvester.py:185` | `def _harvest_edge(self)` |
| `_harvest_master_keys` | method | `modules/dpapi_harvester.py:105` | `def _harvest_master_keys(self)` |
| `_harvest_rdp` | method | `modules/dpapi_harvester.py:229` | `def _harvest_rdp(self)` |
| `_harvest_wifi` | method | `modules/dpapi_harvester.py:195` | `def _harvest_wifi(self)` |
| `_harvest_windows_vault` | method | `modules/dpapi_harvester.py:239` | `def _harvest_windows_vault(self)` |
| `export_credentials` | method | `modules/dpapi_harvester.py:329` | `def export_credentials(self)` |
| `harvest_all` | method | `modules/dpapi_harvester.py:90` | `def harvest_all(self)` |
| `masterkey_report` | method | `modules/dpapi_harvester.py:348` | `def masterkey_report(self)` |
| `EDRDetector` | class | `modules/edr_detector.py:191` | `class EDRDetector` |
| `EDRFinding` | class | `modules/edr_detector.py:174` | `class EDRFinding` |
| `EDRProfile` | class | `modules/edr_detector.py:182` | `class EDRProfile` |
| `_generate_recommendations` | method | `modules/edr_detector.py:344` | `def _generate_recommendations(profile)` |
| `_local_drivers` | method | `modules/edr_detector.py:300` | `def _local_drivers()` |
| `_local_processes` | method | `modules/edr_detector.py:274` | `def _local_processes()` |
| `_local_services` | method | `modules/edr_detector.py:285` | `def _local_services()` |
| `_match_signatures` | method | `modules/edr_detector.py:311` | `def _match_signatures(profile)` |
| `_severity` | method | `modules/edr_detector.py:398` | `def _severity(profile)` |
| `detect_local` | method | `modules/edr_detector.py:202` | `def detect_local()` |
| `detect_remote_commands` | method | `modules/edr_detector.py:221` | `def detect_remote_commands(remote_type)` |
| `generate_edr_check_script` | method | `modules/edr_detector.py:410` | `def generate_edr_check_script(remote_type)` |
| `init_board` | function | `modules/eegg.sh:26` | `` |
| `move_black_pawns` | function | `modules/eegg.sh:78` | `` |
| `move_white_pawns` | function | `modules/eegg.sh:61` | `` |
| `show_board` | function | `modules/eegg.sh:40` | `` |
| `CollabNotificationSink` | class | `modules/engagement_hooks.py:202` | `class CollabNotificationSink(INotificationSink)` |
| `DiscordNotificationSink` | class | `modules/engagement_hooks.py:307` | `class DiscordNotificationSink(_OutboundHTTPSink)` |
| `EngagementEvent` | class | `modules/engagement_hooks.py:99` | `class EngagementEvent` |
| `EngagementNarrator` | class | `modules/engagement_hooks.py:376` | `class EngagementNarrator` |
| `INotificationSink` | class | `modules/engagement_hooks.py:148` | `class INotificationSink(ABC)` |
| `NotificationBroadcaster` | class | `modules/engagement_hooks.py:332` | `class NotificationBroadcaster` |
| `StreamEventSink` | class | `modules/engagement_hooks.py:165` | `class StreamEventSink(INotificationSink)` |
| `TelegramNotificationSink` | class | `modules/engagement_hooks.py:276` | `class TelegramNotificationSink(_OutboundHTTPSink)` |
| `_OutboundHTTPSink` | class | `modules/engagement_hooks.py:240` | `class _OutboundHTTPSink(INotificationSink)` |
| `__init__` | method | `modules/engagement_hooks.py:345` | `def __init__(self, sinks)` |
| `__init__` | method | `modules/engagement_hooks.py:387` | `def __init__(self, broadcaster)` |
| `_build_request` | method | `modules/engagement_hooks.py:253` | `def _build_request(self, event)` |
| `_build_request` | method | `modules/engagement_hooks.py:289` | `def _build_request(self, event)` |
| `_build_request` | method | `modules/engagement_hooks.py:319` | `def _build_request(self, event)` |
| `_load_payload` | function | `modules/engagement_hooks.py:86` | `def _load_payload()` |
| `_load_seen_beacons` | method | `modules/engagement_hooks.py:438` | `def _load_seen_beacons()` |
| `_persist` | method | `modules/engagement_hooks.py:411` | `def _persist(self, event)` |
| `_safe_str` | function | `modules/engagement_hooks.py:76` | `def _safe_str(value, maxlen)` |
| `_sanitize_client_id` | method | `modules/engagement_hooks.py:460` | `def _sanitize_client_id(client_id)` |
| `_save_seen_beacons` | method | `modules/engagement_hooks.py:449` | `def _save_seen_beacons(seen)` |
| `add` | method | `modules/engagement_hooks.py:359` | `def add(self, sink)` |
| `append_approval_record` | method | `modules/engagement_hooks.py:558` | `def append_approval_record(record)` |
| `default` | method | `modules/engagement_hooks.py:350` | `def default(cls)` |
| `deliver` | method | `modules/engagement_hooks.py:157` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:179` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:214` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:256` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:364` | `def deliver(self, event)` |
| `get_default_narrator` | method | `modules/engagement_hooks.py:476` | `def get_default_narrator()` |
| `is_valid_target` | method | `modules/engagement_hooks.py:620` | `def is_valid_target(value)` |
| `list_pending_approvals` | method | `modules/engagement_hooks.py:569` | `def list_pending_approvals()` |
| `name` | method | `modules/engagement_hooks.py:153` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:176` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:211` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:250` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:286` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:316` | `def name(self)` |
| `narrate` | method | `modules/engagement_hooks.py:394` | `def narrate(self, kind, target, message, payload, severity)` |
| `now` | method | `modules/engagement_hooks.py:122` | `def now(cls, kind, target, message, payload, severity)` |
| `publish_shell_obtained` | method | `modules/engagement_hooks.py:485` | `def publish_shell_obtained(client_id, primary_ip, hostname, user, platform, narrator)` |
| `render_line` | method | `modules/engagement_hooks.py:141` | `def render_line(self)` |
| `resolve_approval` | method | `modules/engagement_hooks.py:595` | `def resolve_approval(approval_id, decision, operator)` |
| `EntraIDAttackEngine` | class | `modules/entra_id_attacks.py:80` | `class EntraIDAttackEngine` |
| `EntraIDConfig` | class | `modules/entra_id_attacks.py:56` | `class EntraIDConfig` |
| `__init__` | method | `modules/entra_id_attacks.py:91` | `def __init__(self, config)` |
| `conditional_access_bypass` | method | `modules/entra_id_attacks.py:306` | `def conditional_access_bypass(self)` |
| `device_code_phish` | method | `modules/entra_id_attacks.py:95` | `def device_code_phish(self, scope)` |
| `entra_connect_sync_abuse` | method | `modules/entra_id_attacks.py:265` | `def entra_connect_sync_abuse(self)` |
| `enumerate_tenant` | method | `modules/entra_id_attacks.py:344` | `def enumerate_tenant(self)` |
| `managed_identity_abuse` | method | `modules/entra_id_attacks.py:234` | `def managed_identity_abuse(self, resource)` |
| `oauth_consent_grant` | method | `modules/entra_id_attacks.py:165` | `def oauth_consent_grant(self, redirect_uri)` |
| `poll_device_code` | method | `modules/entra_id_attacks.py:128` | `def poll_device_code(self, device_code, interval, timeout)` |
| `service_principal_credential_theft` | method | `modules/entra_id_attacks.py:202` | `def service_principal_credential_theft(self)` |
| `summary` | method | `modules/entra_id_attacks.py:367` | `def summary(self)` |
| `EstoridesCaseReader` | class | `modules/estorides_importer.py:377` | `class EstoridesCaseReader` |
| `EstoridesEntity` | class | `modules/estorides_importer.py:84` | `class EstoridesEntity` |
| `EstoridesStixParser` | class | `modules/estorides_importer.py:487` | `class EstoridesStixParser` |
| `EstoridesToLazyOwnBridge` | class | `modules/estorides_importer.py:577` | `class EstoridesToLazyOwnBridge` |
| `FeedbackLoop` | class | `modules/estorides_importer.py:753` | `class FeedbackLoop` |
| `ImportResult` | class | `modules/estorides_importer.py:96` | `class ImportResult` |
| `SeedResult` | class | `modules/estorides_importer.py:128` | `class SeedResult` |
| `__init__` | method | `modules/estorides_importer.py:380` | `def __init__(self, db_path)` |
| `__init__` | method | `modules/estorides_importer.py:503` | `def __init__(self, stix_path)` |
| `__init__` | method | `modules/estorides_importer.py:580` | `def __init__(self, db_path, config_path)` |
| `__init__` | method | `modules/estorides_importer.py:764` | `def __init__(self, max_iterations, max_depth, max_steps, timeout)` |
| `_ensure_conn` | method | `modules/estorides_importer.py:388` | `def _ensure_conn(self)` |
| `_extract_value` | method | `modules/estorides_importer.py:555` | `def _extract_value(obj, stix_type)` |
| `_gather_seeds` | method | `modules/estorides_importer.py:871` | `def _gather_seeds(self, methods, seen)` |
| `_import_to_db` | method | `modules/estorides_importer.py:632` | `def _import_to_db(self, imports, result)` |
| `_import_to_scope` | method | `modules/estorides_importer.py:676` | `def _import_to_scope(self, imports, result)` |
| `available` | method | `modules/estorides_importer.py:385` | `def available(self)` |
| `available` | method | `modules/estorides_importer.py:507` | `def available(self)` |
| `close` | method | `modules/estorides_importer.py:481` | `def close(self)` |
| `ensure_directories` | method | `modules/estorides_importer.py:571` | `def ensure_directories()` |
| `export_combined_graph` | method | `modules/estorides_importer.py:897` | `def export_combined_graph(output_path)` |
| `extract_seeds_from_db` | method | `modules/estorides_importer.py:203` | `def extract_seeds_from_db(db_path)` |
| `extract_seeds_from_hosts_file` | method | `modules/estorides_importer.py:175` | `def extract_seeds_from_hosts_file(path)` |
| `extract_seeds_from_scope` | method | `modules/estorides_importer.py:241` | `def extract_seeds_from_scope(scope_entries)` |
| `extract_seeds_from_world_model` | method | `modules/estorides_importer.py:143` | `def extract_seeds_from_world_model(world_model_path)` |
| `get_all_entities` | method | `modules/estorides_importer.py:465` | `def get_all_entities(self, case_id)` |
| `get_combined_surface` | method | `modules/estorides_importer.py:707` | `def get_combined_surface(self)` |
| `get_entities` | method | `modules/estorides_importer.py:406` | `def get_entities(self, case_id, entity_types, limit)` |
| `get_host_entities` | method | `modules/estorides_importer.py:461` | `def get_host_entities(self, case_id)` |
| `import_entities` | method | `modules/estorides_importer.py:588` | `def import_entities(self, entities, add_to_scope, add_to_db)` |
| `list_cases` | method | `modules/estorides_importer.py:394` | `def list_cases(self, limit)` |
| `new_assets` | method | `modules/estorides_importer.py:139` | `def new_assets(self)` |
| `parse` | method | `modules/estorides_importer.py:510` | `def parse(self)` |
| `parse_by_type` | method | `modules/estorides_importer.py:544` | `def parse_by_type(self, entity_types)` |
| `run` | method | `modules/estorides_importer.py:780` | `def run(self, seed_methods)` |
| `run_estorides_discover` | method | `modules/estorides_importer.py:271` | `def run_estorides_discover(seed_type, seed_value, max_depth, max_steps, out_json, timeout)` |
| `run_estorides_run` | method | `modules/estorides_importer.py:327` | `def run_estorides_run(query, out_json, timeout)` |
| `stats` | method | `modules/estorides_importer.py:468` | `def stats(self)` |
| `success` | method | `modules/estorides_importer.py:110` | `def success(self)` |
| `to_dict` | method | `modules/estorides_importer.py:113` | `def to_dict(self)` |
| `EvasionEngine` | class | `modules/evasion_engine.py:52` | `class EvasionEngine` |
| `MalleableProfile` | class | `modules/evasion_engine.py:37` | `class MalleableProfile` |
| `TrafficMorphConfig` | class | `modules/evasion_engine.py:25` | `class TrafficMorphConfig` |
| `__init__` | method | `modules/evasion_engine.py:130` | `def __init__(self, config)` |
| `_compute_jitter` | method | `modules/evasion_engine.py:214` | `def _compute_jitter(self)` |
| `_compute_sleep` | method | `modules/evasion_engine.py:218` | `def _compute_sleep(self)` |
| `_generate_cert_fingerprint` | method | `modules/evasion_engine.py:211` | `def _generate_cert_fingerprint(self)` |
| `_generate_headers` | method | `modules/evasion_engine.py:180` | `def _generate_headers(self, user_agent)` |
| `_generate_ja4_hash` | method | `modules/evasion_engine.py:148` | `def _generate_ja4_hash(self)` |
| `_generate_user_agent` | method | `modules/evasion_engine.py:162` | `def _generate_user_agent(self, os_family)` |
| `_get_domain_front` | method | `modules/evasion_engine.py:226` | `def _get_domain_front(self)` |
| `_persist_profile` | method | `modules/evasion_engine.py:305` | `def _persist_profile(self, profile)` |
| `_pick_uri_pool` | method | `modules/evasion_engine.py:203` | `def _pick_uri_pool(self)` |
| `_random_chrome_version` | method | `modules/evasion_engine.py:139` | `def _random_chrome_version(self)` |
| `_random_firefox_version` | method | `modules/evasion_engine.py:142` | `def _random_firefox_version(self)` |
| `_random_safari_version` | method | `modules/evasion_engine.py:145` | `def _random_safari_version(self)` |
| `generate_profile` | method | `modules/evasion_engine.py:238` | `def generate_profile(self, os_family)` |
| `get_active_profile` | method | `modules/evasion_engine.py:263` | `def get_active_profile(self)` |
| `get_beacon_config` | method | `modules/evasion_engine.py:266` | `def get_beacon_config(self)` |
| `get_history` | method | `modules/evasion_engine.py:322` | `def get_history(self)` |
| `morph_traffic` | method | `modules/evasion_engine.py:281` | `def morph_traffic(self, config)` |
| `profile_to_json` | method | `modules/evasion_engine.py:337` | `def profile_to_json(self, profile)` |
| `rotate_profile` | method | `modules/evasion_engine.py:258` | `def rotate_profile(self, os_family)` |
| `set_config` | method | `modules/evasion_engine.py:136` | `def set_config(self, config)` |
| `EvasivePayloadGenerator` | class | `modules/evasive_payloads.py:18` | `class EvasivePayloadGenerator` |
| `__init__` | method | `modules/evasive_payloads.py:86` | `def __init__(self)` |
| `_apply_encoding_chain` | method | `modules/evasive_payloads.py:120` | `def _apply_encoding_chain(self, data, chain)` |
| `_gzip_compress` | method | `modules/evasive_payloads.py:116` | `def _gzip_compress(self, data)` |
| `_random_string` | method | `modules/evasive_payloads.py:95` | `def _random_string(self, length)` |
| `_random_var` | method | `modules/evasive_payloads.py:89` | `def _random_var(self, length)` |
| `_rot13` | method | `modules/evasive_payloads.py:104` | `def _rot13(self, data)` |
| `_xor_encode` | method | `modules/evasive_payloads.py:99` | `def _xor_encode(self, data, key)` |
| `generate_javascript_obfuscated` | method | `modules/evasive_payloads.py:182` | `def generate_javascript_obfuscated(self, payload)` |
| `generate_linux_evasive` | method | `modules/evasive_payloads.py:218` | `def generate_linux_evasive(self, rhost, rport, technique)` |
| `generate_lolbas_execution` | method | `modules/evasive_payloads.py:288` | `def generate_lolbas_execution(self, payload_url, technique)` |
| `generate_polymorphic_command` | method | `modules/evasive_payloads.py:338` | `def generate_polymorphic_command(self, base_cmd, iterations)` |
| `generate_powershell_obfuscated` | method | `modules/evasive_payloads.py:140` | `def generate_powershell_obfuscated(self, payload, obfuscation_level)` |
| `generate_shellcode_loader_powershell` | method | `modules/evasive_payloads.py:243` | `def generate_shellcode_loader_powershell(self, shellcode_b64, injection_technique)` |
| `generate_vba_obfuscated` | method | `modules/evasive_payloads.py:201` | `def generate_vba_obfuscated(self, payload)` |
| `list_techniques` | method | `modules/evasive_payloads.py:378` | `def list_techniques(self)` |
| `CollabBusSink` | class | `modules/event_bus.py:162` | `class CollabBusSink(Sink)` |
| `EngagementSink` | class | `modules/event_bus.py:198` | `class EngagementSink(Sink)` |
| `EventCategory` | class | `modules/event_bus.py:47` | `class EventCategory(str, Enum)` |
| `EventSeverity` | class | `modules/event_bus.py:73` | `class EventSeverity(str, Enum)` |
| `JsonlSink` | class | `modules/event_bus.py:142` | `class JsonlSink(Sink)` |
| `LazyEvent` | class | `modules/event_bus.py:82` | `class LazyEvent` |
| `Sink` | class | `modules/event_bus.py:132` | `class Sink(ABC)` |
| `UnifiedEventBus` | class | `modules/event_bus.py:221` | `class UnifiedEventBus` |
| `__init__` | method | `modules/event_bus.py:145` | `def __init__(self, filepath)` |
| `__init__` | method | `modules/event_bus.py:165` | `def __init__(self)` |
| `__init__` | method | `modules/event_bus.py:246` | `def __init__(self)` |
| `_bus` | method | `modules/event_bus.py:169` | `def _bus(self)` |
| `_dispatch_event` | method | `modules/event_bus.py:440` | `def _dispatch_event(self, event)` |
| `_dispatch_loop` | method | `modules/event_bus.py:412` | `def _dispatch_loop(self)` |
| `_init_sinks` | method | `modules/event_bus.py:264` | `def _init_sinks(self)` |
| `_match_topic` | method | `modules/event_bus.py:516` | `def _match_topic(self, topic, event)` |
| `_notify_shutdown` | method | `modules/event_bus.py:478` | `def _notify_shutdown(self)` |
| `close` | method | `modules/event_bus.py:139` | `def close(self)` |
| `close` | method | `modules/event_bus.py:158` | `def close(self)` |
| `close` | method | `modules/event_bus.py:194` | `def close(self)` |
| `close` | method | `modules/event_bus.py:217` | `def close(self)` |
| `drain` | method | `modules/event_bus.py:350` | `def drain(self)` |
| `from_dict` | method | `modules/event_bus.py:114` | `def from_dict(cls, d)` |
| `get_event_bus` | method | `modules/event_bus.py:569` | `def get_event_bus()` |
| `history` | method | `modules/event_bus.py:555` | `def history(self, n, category)` |
| `history_since` | method | `modules/event_bus.py:563` | `def history_since(self, since_ts)` |
| `instance` | method | `modules/event_bus.py:278` | `def instance(cls)` |
| `publish` | method | `modules/event_bus.py:332` | `def publish(self, event)` |
| `publish_event` | method | `modules/event_bus.py:574` | `def publish_event(category, event_type, source, payload, severity, target, operator)` |
| `shutdown` | method | `modules/event_bus.py:368` | `def shutdown(self)` |
| `subscribe` | method | `modules/event_bus.py:295` | `def subscribe(self, subscriber_id, callback)` |
| `subscribe_async` | method | `modules/event_bus.py:310` | `def subscribe_async(self, subscriber_id)` |
| `subscribe_topic` | method | `modules/event_bus.py:300` | `def subscribe_topic(self, subscriber_id, topic, callback)` |
| `subscriber_count` | method | `modules/event_bus.py:286` | `def subscriber_count(self)` |
| `to_dict` | method | `modules/event_bus.py:95` | `def to_dict(self)` |
| `to_json` | method | `modules/event_bus.py:110` | `def to_json(self)` |
| `unsubscribe` | method | `modules/event_bus.py:322` | `def unsubscribe(self, subscriber_id)` |
| `write` | method | `modules/event_bus.py:136` | `def write(self, event)` |
| `write` | method | `modules/event_bus.py:150` | `def write(self, event)` |
| `write` | method | `modules/event_bus.py:179` | `def write(self, event)` |

Next: [SYMBOLS_p12.md](SYMBOLS_p12.md)
