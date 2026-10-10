# Symbols (page 11 of 38)
Previous: [SYMBOLS_p10.md](SYMBOLS_p10.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `get_ja3_hash` | method | `modules/c2_profile_engine.py:155` | `def get_ja3_hash(self)` |
| `is_available` | method | `modules/c2_profile_engine.py:429` | `def is_available(self)` |
| `list_slots` | method | `modules/c2_profile_engine.py:487` | `def list_slots(self)` |
| `rotate` | method | `modules/c2_profile_engine.py:469` | `def rotate(self)` |
| `rotate` | method | `modules/c2_profile_engine.py:672` | `def rotate(self)` |
| `rotator` | method | `modules/c2_profile_engine.py:663` | `def rotator(self)` |
| `smb_profile` | method | `modules/c2_profile_engine.py:653` | `def smb_profile(self)` |
| `tls_profile` | method | `modules/c2_profile_engine.py:643` | `def tls_profile(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:188` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:274` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:333` | `def to_dict(self)` |
| `to_dict` | method | `modules/c2_profile_engine.py:389` | `def to_dict(self)` |
| `touch` | method | `modules/c2_profile_engine.py:436` | `def touch(self)` |
| `transport` | method | `modules/c2_profile_engine.py:465` | `def transport(self)` |
| `validate` | method | `modules/c2_profile_engine.py:676` | `def validate(self)` |
| `validate_all` | method | `modules/c2_profile_engine.py:591` | `def validate_all(self, tls, dns, smb, websocket)` |
| `validate_dns` | method | `modules/c2_profile_engine.py:536` | `def validate_dns(profile)` |
| `validate_smb` | method | `modules/c2_profile_engine.py:556` | `def validate_smb(profile)` |
| `validate_tls` | method | `modules/c2_profile_engine.py:511` | `def validate_tls(profile)` |
| `validate_websocket` | method | `modules/c2_profile_engine.py:576` | `def validate_websocket(profile)` |
| `websocket_profile` | method | `modules/c2_profile_engine.py:658` | `def websocket_profile(self)` |
| `days_in_month` | function | `modules/cal.sh:14` | `` |
| `first_day_of_month` | function | `modules/cal.sh:31` | `` |
| `is_leap_year` | function | `modules/cal.sh:4` | `` |
| `CICDEnumerator` | class | `modules/cicd_enumerator.py:43` | `class CICDEnumerator` |
| `CICDFinding` | class | `modules/cicd_enumerator.py:33` | `class CICDFinding` |
| `__init__` | method | `modules/cicd_enumerator.py:54` | `def __init__(self, target_url, sessions_dir)` |
| `_check_azure_devops` | method | `modules/cicd_enumerator.py:230` | `def _check_azure_devops(self)` |
| `_check_bitbucket` | method | `modules/cicd_enumerator.py:266` | `def _check_bitbucket(self)` |
| `_check_github_actions` | method | `modules/cicd_enumerator.py:189` | `def _check_github_actions(self)` |
| `_check_gitlab` | method | `modules/cicd_enumerator.py:120` | `def _check_gitlab(self)` |
| `_check_jenkins` | method | `modules/cicd_enumerator.py:73` | `def _check_jenkins(self)` |
| `export_findings` | method | `modules/cicd_enumerator.py:387` | `def export_findings(self)` |
| `generate_ci_attack_matrix` | method | `modules/cicd_enumerator.py:322` | `def generate_ci_attack_matrix(self)` |
| `scan` | method | `modules/cicd_enumerator.py:60` | `def scan(self)` |
| `scan_build_log` | method | `modules/cicd_enumerator.py:297` | `def scan_build_log(self, log_content, source)` |
| `_clear_cli_session` | function | `modules/cli_auth.py:474` | `def _clear_cli_session()` |
| `_load_payload` | function | `modules/cli_auth.py:84` | `def _load_payload()` |
| `_load_users` | function | `modules/cli_auth.py:33` | `def _load_users()` |
| `_read_cli_session` | function | `modules/cli_auth.py:425` | `def _read_cli_session()` |
| `_save_payload` | function | `modules/cli_auth.py:99` | `def _save_payload(payload)` |
| `_save_users` | function | `modules/cli_auth.py:51` | `def _save_users(users)` |
| `_write_cli_session` | function | `modules/cli_auth.py:440` | `def _write_cli_session(username, elo, role)` |
| `_write_cli_session_raw` | function | `modules/cli_auth.py:458` | `def _write_cli_session_raw(data)` |
| `get_current_operator` | function | `modules/cli_auth.py:392` | `def get_current_operator()` |
| `login` | function | `modules/cli_auth.py:236` | `def login(username, password, remember)` |
| `logout` | function | `modules/cli_auth.py:289` | `def logout()` |
| `needs_login` | function | `modules/cli_auth.py:483` | `def needs_login()` |
| `register` | function | `modules/cli_auth.py:141` | `def register(username, password)` |
| `sync_elo_from_session` | function | `modules/cli_auth.py:404` | `def sync_elo_from_session(elo)` |
| `try_auto_login` | function | `modules/cli_auth.py:324` | `def try_auto_login()` |
| `user_exists` | function | `modules/cli_auth.py:118` | `def user_exists(username)` |
| `verify_password` | function | `modules/cli_auth.py:210` | `def verify_password(username, password)` |
| `whoami` | function | `modules/cli_auth.py:362` | `def whoami()` |
| `CloudEnumerator` | class | `modules/cloud_enum.py:23` | `class CloudEnumerator` |
| `__init__` | method | `modules/cloud_enum.py:34` | `def __init__(self, provider, session, timeout)` |
| `_check_aws_privesc` | method | `modules/cloud_enum.py:526` | `def _check_aws_privesc(data)` |
| `_enumerate_aws_iam` | method | `modules/cloud_enum.py:390` | `def _enumerate_aws_iam(self)` |
| `_enumerate_aws_metadata` | method | `modules/cloud_enum.py:96` | `def _enumerate_aws_metadata(self)` |
| `_enumerate_azure_iam` | method | `modules/cloud_enum.py:421` | `def _enumerate_azure_iam(self)` |
| `_enumerate_azure_metadata` | method | `modules/cloud_enum.py:146` | `def _enumerate_azure_metadata(self)` |
| `_enumerate_azure_storage` | method | `modules/cloud_enum.py:316` | `def _enumerate_azure_storage(self, target_bucket)` |
| `_enumerate_gcp_iam` | method | `modules/cloud_enum.py:477` | `def _enumerate_gcp_iam(self)` |
| `_enumerate_gcp_metadata` | method | `modules/cloud_enum.py:193` | `def _enumerate_gcp_metadata(self)` |
| `_enumerate_gcs` | method | `modules/cloud_enum.py:350` | `def _enumerate_gcs(self, target_bucket)` |
| `_enumerate_s3` | method | `modules/cloud_enum.py:274` | `def _enumerate_s3(self, target_bucket)` |
| `detect_provider` | method | `modules/cloud_enum.py:47` | `def detect_provider(self)` |
| `enumerate_iam` | method | `modules/cloud_enum.py:372` | `def enumerate_iam(self)` |
| `enumerate_metadata` | method | `modules/cloud_enum.py:75` | `def enumerate_metadata(self)` |
| `enumerate_storage` | method | `modules/cloud_enum.py:251` | `def enumerate_storage(self, target_bucket)` |
| `full_enumeration` | method | `modules/cloud_enum.py:576` | `def full_enumeration(self)` |
| `ColabEvent` | class | `modules/collab_bp.py:163` | `class ColabEvent` |
| `EventBus` | class | `modules/collab_bp.py:188` | `class EventBus` |
| `LockManager` | class | `modules/collab_bp.py:257` | `class LockManager` |
| `OperatorInfo` | class | `modules/collab_bp.py:176` | `class OperatorInfo` |
| `OperatorRegistry` | class | `modules/collab_bp.py:314` | `class OperatorRegistry` |
| `TargetLock` | class | `modules/collab_bp.py:250` | `class TargetLock` |
| `__init__` | method | `modules/collab_bp.py:198` | `def __init__(self)` |
| `__init__` | method | `modules/collab_bp.py:263` | `def __init__(self)` |
| `__init__` | method | `modules/collab_bp.py:319` | `def __init__(self)` |
| `_authenticated_operator` | function | `modules/collab_bp.py:90` | `def _authenticated_operator()` |
| `_check_collab_permission` | function | `modules/collab_bp.py:100` | `def _check_collab_permission(perm_name)` |
| `_collab_login_required` | function | `modules/collab_bp.py:120` | `def _collab_login_required(f)` |
| `_collab_permission_required` | function | `modules/collab_bp.py:136` | `def _collab_permission_required(perm_name)` |
| `_expire` | method | `modules/collab_bp.py:297` | `def _expire(self)` |
| `_expire` | method | `modules/collab_bp.py:350` | `def _expire(self)` |
| `acquire` | method | `modules/collab_bp.py:267` | `def acquire(self, target, operator, ttl_secs)` |
| `active_operators` | method | `modules/collab_bp.py:345` | `def active_operators(self)` |
| `all_locks` | method | `modules/collab_bp.py:292` | `def all_locks(self)` |
| `collab_ui` | method | `modules/collab_bp.py:396` | `def collab_ui()` |
| `decorated` | method | `modules/collab_bp.py:84` | `def decorated()` |
| `decorated` | method | `modules/collab_bp.py:124` | `def decorated()` |
| `decorated` | method | `modules/collab_bp.py:141` | `def decorated()` |
| `decorator` | method | `modules/collab_bp.py:139` | `def decorator(f)` |
| `generate` | method | `modules/collab_bp.py:424` | `def generate()` |
| `get_event_bus` | method | `modules/collab_bp.py:370` | `def get_event_bus()` |
| `get_lock_manager` | method | `modules/collab_bp.py:374` | `def get_lock_manager()` |
| `get_operator_registry` | method | `modules/collab_bp.py:378` | `def get_operator_registry()` |
| `heartbeat` | method | `modules/collab_bp.py:334` | `def heartbeat(self, name)` |
| `history` | method | `modules/collab_bp.py:537` | `def history()` |
| `join` | method | `modules/collab_bp.py:323` | `def join(self, name)` |
| `leave` | method | `modules/collab_bp.py:340` | `def leave(self, name)` |
| `lock` | method | `modules/collab_bp.py:483` | `def lock()` |
| `locks` | method | `modules/collab_bp.py:522` | `def locks()` |
| `login_required` | method | `modules/collab_bp.py:80` | `def login_required(f)` |
| `operators` | method | `modules/collab_bp.py:458` | `def operators()` |
| `publish` | method | `modules/collab_bp.py:219` | `def publish(self, event)` |
| `publish` | method | `modules/collab_bp.py:470` | `def publish()` |
| `publish_event` | method | `modules/collab_bp.py:382` | `def publish_event(type, payload, operator)` |
| `recent` | method | `modules/collab_bp.py:234` | `def recent(self, n)` |
| `release` | method | `modules/collab_bp.py:279` | `def release(self, target, operator)` |
| `reset` | method | `modules/collab_bp.py:238` | `def reset(self)` |
| `reset` | method | `modules/collab_bp.py:304` | `def reset(self)` |
| `reset` | method | `modules/collab_bp.py:356` | `def reset(self)` |
| `status` | method | `modules/collab_bp.py:287` | `def status(self, target)` |
| `stream` | method | `modules/collab_bp.py:411` | `def stream()` |
| `subscribe` | method | `modules/collab_bp.py:203` | `def subscribe(self, subscriber_id)` |
| `to_sse` | method | `modules/collab_bp.py:170` | `def to_sse(self)` |
| `unlock` | method | `modules/collab_bp.py:504` | `def unlock()` |
| `unsubscribe` | method | `modules/collab_bp.py:215` | `def unsubscribe(self, subscriber_id)` |
| `delete_lines` | function | `modules/colors.py:68` | `def delete_lines(content, to_delete)` |
| `no_html` | function | `modules/colors.py:74` | `def no_html(content)` |
| `retModel` | function | `modules/colors.py:40` | `def retModel()` |
| `CommandExecutor` | class | `modules/command_executor.py:47` | `class CommandExecutor` |
| `ExecutionResult` | class | `modules/command_executor.py:38` | `class ExecutionResult` |
| `__init__` | method | `modules/command_executor.py:59` | `def __init__(self)` |
| `_fire_hooks` | method | `modules/command_executor.py:232` | `def _fire_hooks(self, result)` |
| `_needs_shell` | method | `modules/command_executor.py:106` | `def _needs_shell(self, command)` |
| `_publish_event` | method | `modules/command_executor.py:239` | `def _publish_event(self, result)` |
| `_run_capture` | method | `modules/command_executor.py:110` | `def _run_capture(self, command, timeout)` |
| `_run_stream` | method | `modules/command_executor.py:135` | `def _run_stream(self, command, timeout)` |
| `add_hook` | method | `modules/command_executor.py:68` | `def add_hook(self, hook)` |
| `get_executor` | method | `modules/command_executor.py:264` | `def get_executor()` |
| `instance` | method | `modules/command_executor.py:63` | `def instance(cls)` |
| `run` | method | `modules/command_executor.py:72` | `def run(self, command, timeout, stream)` |
| `run_with_tee` | method | `modules/command_executor.py:172` | `def run_with_tee(self, command, output_path, timeout)` |
| `ComplianceEngine` | class | `modules/compliance.py:632` | `class ComplianceEngine` |
| `ComplianceFinding` | class | `modules/compliance.py:620` | `class ComplianceFinding` |
| `EvidenceChain` | class | `modules/compliance.py:349` | `class EvidenceChain` |
| `EvidenceEntry` | class | `modules/compliance.py:340` | `class EvidenceEntry` |
| `__init__` | method | `modules/compliance.py:357` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/compliance.py:635` | `def __init__(self, sessions_dir)` |
| `_append_to_file` | method | `modules/compliance.py:403` | `def _append_to_file(self, entry)` |
| `_count_by_category` | method | `modules/compliance.py:772` | `def _count_by_category(self, findings)` |
| `_count_by_severity` | method | `modules/compliance.py:765` | `def _count_by_severity(self, findings)` |
| `_format_compliance_report_md` | method | `modules/compliance.py:835` | `def _format_compliance_report_md(self, report)` |
| `_hash_entry` | method | `modules/compliance.py:379` | `def _hash_entry(self, entry)` |
| `_load` | method | `modules/compliance.py:364` | `def _load(self)` |
| `_load_findings` | method | `modules/compliance.py:779` | `def _load_findings(self)` |
| `add_evidence` | method | `modules/compliance.py:901` | `def add_evidence(self, filepath, operator, description)` |
| `add_file` | method | `modules/compliance.py:383` | `def add_file(self, filepath, operator, description)` |
| `export_pdf` | method | `modules/compliance.py:449` | `def export_pdf(report_md, output_path, title, classification)` |
| `export_pdf` | method | `modules/compliance.py:831` | `def export_pdf(self, report, output_path)` |
| `export_to_cef` | method | `modules/compliance.py:572` | `def export_to_cef(findings, output_path, vendor, product, version)` |
| `export_to_elastic_ndjson` | method | `modules/compliance.py:533` | `def export_to_elastic_ndjson(findings, output_path, index_prefix)` |
| `generate_compliance_report` | method | `modules/compliance.py:710` | `def generate_compliance_report(self, findings, include_evidence_chain, include_siem_formats)` |
| `get_chain_digest` | method | `modules/compliance.py:429` | `def get_chain_digest(self)` |
| `map_findings_to_compliance` | method | `modules/compliance.py:639` | `def map_findings_to_compliance(self, findings, frameworks)` |
| `to_report` | method | `modules/compliance.py:432` | `def to_report(self)` |
| `verify` | method | `modules/compliance.py:410` | `def verify(self)` |
| `verify_evidence_chain` | method | `modules/compliance.py:904` | `def verify_evidence_chain(self)` |
| `HookEngine` | class | `modules/conditional_hooks.py:258` | `class HookEngine` |
| `HookRule` | class | `modules/conditional_hooks.py:45` | `class HookRule` |
| `__init__` | method | `modules/conditional_hooks.py:270` | `def __init__(self)` |
| `_execute_action` | method | `modules/conditional_hooks.py:428` | `def _execute_action(self, action, context)` |
| `_execute_cred_reuse` | method | `modules/conditional_hooks.py:500` | `def _execute_cred_reuse(self, context)` |
| `_execute_local_command` | method | `modules/conditional_hooks.py:476` | `def _execute_local_command(command)` |
| `_execute_shell_command` | method | `modules/conditional_hooks.py:467` | `def _execute_shell_command(self, command, context)` |
| `_match_trigger` | method | `modules/conditional_hooks.py:369` | `def _match_trigger(self, rule_trigger, event, context)` |
| `_resolve_placeholders` | method | `modules/conditional_hooks.py:414` | `def _resolve_placeholders(self, text, context)` |
| `add_rule` | method | `modules/conditional_hooks.py:330` | `def add_rule(self, rule_dict)` |
| `can_fire` | method | `modules/conditional_hooks.py:56` | `def can_fire(self, now)` |
| `enable_rule` | method | `modules/conditional_hooks.py:359` | `def enable_rule(self, name, enabled)` |
| `fire` | method | `modules/conditional_hooks.py:516` | `def fire(self, event, context)` |
| `get_hook_engine` | method | `modules/conditional_hooks.py:586` | `def get_hook_engine()` |
| `get_rule` | method | `modules/conditional_hooks.py:575` | `def get_rule(self, name)` |
| `list_rules` | method | `modules/conditional_hooks.py:571` | `def list_rules(self)` |
| `load_rules` | method | `modules/conditional_hooks.py:290` | `def load_rules(self, path)` |
| `mark_fired` | method | `modules/conditional_hooks.py:65` | `def mark_fired(self)` |
| `register_action_handler` | method | `modules/conditional_hooks.py:277` | `def register_action_handler(self, action_type, handler)` |
| `remove_rule` | method | `modules/conditional_hooks.py:345` | `def remove_rule(self, name)` |
| `save_rules` | method | `modules/conditional_hooks.py:322` | `def save_rules(self, path)` |
| `set_placeholders` | method | `modules/conditional_hooks.py:286` | `def set_placeholders(self, placeholders)` |
| `to_dict` | method | `modules/conditional_hooks.py:69` | `def to_dict(self)` |
| `_ensure_loaded` | function | `modules/config_store.py:106` | `def _ensure_loaded()` |
| `_load` | function | `modules/config_store.py:113` | `def _load()` |
| `_persist` | function | `modules/config_store.py:131` | `def _persist()` |
| `_start_watcher` | function | `modules/config_store.py:143` | `def _start_watcher(interval)` |
| `_watch_loop` | function | `modules/config_store.py:148` | `def _watch_loop()` |
| `get_config` | function | `modules/config_store.py:53` | `def get_config(key, default)` |
| `init` | function | `modules/config_store.py:36` | `def init(path, watch)` |
| `reload_config` | function | `modules/config_store.py:90` | `def reload_config()` |
| `set_config` | function | `modules/config_store.py:66` | `def set_config()` |
| `set_config_dict` | function | `modules/config_store.py:80` | `def set_config_dict(updates)` |
| `stop_watcher` | function | `modules/config_store.py:96` | `def stop_watcher()` |
| `CredentialReuseEngine` | class | `modules/credential_reuse.py:55` | `class CredentialReuseEngine` |
| `ReuseCandidate` | class | `modules/credential_reuse.py:32` | `class ReuseCandidate` |
| `__init__` | method | `modules/credential_reuse.py:80` | `def __init__(self)` |
| `_build_command` | method | `modules/credential_reuse.py:196` | `def _build_command(self, username, password, host, target_services)` |
| `_load_cache` | method | `modules/credential_reuse.py:85` | `def _load_cache(self)` |
| `_save_cache` | method | `modules/credential_reuse.py:95` | `def _save_cache(self)` |
| `_score_candidate` | method | `modules/credential_reuse.py:144` | `def _score_candidate(self, username, password, source_host, target_host, target_services)` |
| `_subnet_distance` | method | `modules/credential_reuse.py:118` | `def _subnet_distance(self, ip_a, ip_b)` |
| `get_credential_reuse_engine` | method | `modules/credential_reuse.py:358` | `def get_credential_reuse_engine()` |
| `get_summary` | method | `modules/credential_reuse.py:338` | `def get_summary(self, candidates)` |
| `mark_confirmed` | method | `modules/credential_reuse.py:112` | `def mark_confirmed(self, username, password, host)` |
| `mark_failed` | method | `modules/credential_reuse.py:107` | `def mark_failed(self, username, password, host)` |
| `rank` | method | `modules/credential_reuse.py:226` | `def rank(self, hosts, creds, host_services, limit)` |
| `suggest_from_state_manager` | method | `modules/credential_reuse.py:278` | `def suggest_from_state_manager(self, state_manager, limit)` |
| `suggest_from_world_model` | method | `modules/credential_reuse.py:308` | `def suggest_from_world_model(self, world_model, limit)` |
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
| `CVEMatcher` | class | `modules/cve_matcher.py:60` | `class CVEMatcher` |
| `CVEResult` | class | `modules/cve_matcher.py:51` | `class CVEResult` |
| `__init__` | method | `modules/cve_matcher.py:70` | `def __init__(self, api_key, cache_dir)` |
| `_cache_path` | method | `modules/cve_matcher.py:95` | `def _cache_path(self, params)` |
| `_load_cache` | method | `modules/cve_matcher.py:100` | `def _load_cache(self, params)` |
| `_query` | method | `modules/cve_matcher.py:128` | `def _query(self)` |
| `_rate_limit` | method | `modules/cve_matcher.py:121` | `def _rate_limit(self)` |
| `_save_cache` | method | `modules/cve_matcher.py:112` | `def _save_cache(self, params, results)` |
| `get_matcher` | method | `modules/cve_matcher.py:198` | `def get_matcher()` |
| `search` | method | `modules/cve_matcher.py:82` | `def search(self)` |
| `search` | method | `modules/cve_matcher.py:206` | `def search(product, version, max_results)` |
| `search_by_cpe` | method | `modules/cve_matcher.py:89` | `def search_by_cpe(self, cpe_name, max_results)` |
| `ACEntry` | class | `modules/dacl_abuse.py:67` | `class ACEntry` |
| `ACLTarget` | class | `modules/dacl_abuse.py:91` | `class ACLTarget` |
| `DACLAbuseEngine` | class | `modules/dacl_abuse.py:113` | `class DACLAbuseEngine` |
| `__init__` | method | `modules/dacl_abuse.py:136` | `def __init__(self, domain, domain_sid, acl_data)` |
| `_calculate_severity` | method | `modules/dacl_abuse.py:384` | `def _calculate_severity(target)` |
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
| `close` | method | `modules/db.py:754` | `def close(self)` |
| `cred_add` | method | `modules/db.py:507` | `def cred_add(self, host_id, username, password, realm, cred_type, origin)` |
| `cred_list` | method | `modules/db.py:527` | `def cred_list(self, workspace_id)` |
| `db_path` | method | `modules/db.py:182` | `def db_path(self)` |
| `default_workspace` | method | `modules/db.py:320` | `def default_workspace(self, name)` |
| `export_csv` | method | `modules/db.py:690` | `def export_csv(self, table, workspace_id)` |
| `get_db` | method | `modules/db.py:771` | `def get_db(db_path)` |
| `host_add` | method | `modules/db.py:357` | `def host_add(self, workspace_id, address, mac, hostname, os, state)` |
| `host_delete` | method | `modules/db.py:390` | `def host_delete(self, host_id)` |
| `host_find` | method | `modules/db.py:410` | `def host_find(self, workspace_id, query)` |
| `host_list` | method | `modules/db.py:401` | `def host_list(self, workspace_id)` |
| `import_nmap_xml` | method | `modules/db.py:614` | `def import_nmap_xml(self, workspace_id, xml_path)` |
| `loot_add` | method | `modules/db.py:546` | `def loot_add(self, workspace_id, name, loot_type, path, notes, host_id)` |
| `loot_list` | method | `modules/db.py:565` | `def loot_list(self, workspace_id)` |
| `migration_status` | method | `modules/db.py:222` | `def migration_status(self)` |
| `note_add` | method | `modules/db.py:581` | `def note_add(self, workspace_id, data, note_type, host_id)` |
| `note_list` | method | `modules/db.py:598` | `def note_list(self, workspace_id)` |
| `service_add` | method | `modules/db.py:427` | `def service_add(self, host_id, port, protocol, state, name, product, version)` |
| `service_list` | method | `modules/db.py:447` | `def service_list(self, host_id)` |
| `status` | method | `modules/db.py:725` | `def status(self, workspace_id)` |
| `vuln_add` | method | `modules/db.py:460` | `def vuln_add(self, host_id, name, severity, description, refs)` |
| `vuln_list` | method | `modules/db.py:478` | `def vuln_list(self, workspace_id, severity)` |
| `workspace_create` | method | `modules/db.py:292` | `def workspace_create(self, name, description)` |
| `workspace_delete` | method | `modules/db.py:333` | `def workspace_delete(self, name)` |
| `workspace_get` | method | `modules/db.py:313` | `def workspace_get(self, name)` |
| `workspace_list` | method | `modules/db.py:307` | `def workspace_list(self)` |
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
| `get_feed` | method | `modules/detection_feed.py:326` | `def get_feed()` |
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
| `get_oracle` | method | `modules/detection_oracle.py:478` | `def get_oracle()` |
| `is_critical_risk` | method | `modules/detection_oracle.py:80` | `def is_critical_risk(self)` |
| `is_high_risk` | method | `modules/detection_oracle.py:75` | `def is_high_risk(self)` |
| `probability` | method | `modules/detection_oracle.py:103` | `def probability(self, command, args, action_category)` |
| `probability` | method | `modules/detection_oracle.py:392` | `def probability(self, command, args, action_category)` |
| `refresh` | method | `modules/detection_oracle.py:336` | `def refresh(self)` |
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
| `_save_credential` | method | `modules/domain_dominance.py:849` | `def _save_credential(self, username, secret, secret_type, source)` |
| `_save_dominance_report` | method | `modules/domain_dominance.py:885` | `def _save_dominance_report(self)` |
| `_save_session` | method | `modules/domain_dominance.py:865` | `def _save_session(self, session_id, target, method, user)` |
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
| `_load_seen_beacons` | method | `modules/engagement_hooks.py:444` | `def _load_seen_beacons()` |
| `_persist` | method | `modules/engagement_hooks.py:417` | `def _persist(self, event)` |
| `_safe_str` | function | `modules/engagement_hooks.py:78` | `def _safe_str(value, maxlen)` |
| `_sanitize_client_id` | method | `modules/engagement_hooks.py:466` | `def _sanitize_client_id(client_id)` |
| `_save_seen_beacons` | method | `modules/engagement_hooks.py:455` | `def _save_seen_beacons(seen)` |
| `add` | method | `modules/engagement_hooks.py:365` | `def add(self, sink)` |
| `append_approval_record` | method | `modules/engagement_hooks.py:564` | `def append_approval_record(record)` |
| `default` | method | `modules/engagement_hooks.py:354` | `def default(cls)` |
| `deliver` | method | `modules/engagement_hooks.py:159` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:181` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:216` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:258` | `def deliver(self, event)` |
| `deliver` | method | `modules/engagement_hooks.py:370` | `def deliver(self, event)` |
| `get_default_narrator` | method | `modules/engagement_hooks.py:482` | `def get_default_narrator()` |
| `is_valid_target` | method | `modules/engagement_hooks.py:626` | `def is_valid_target(value)` |
| `list_pending_approvals` | method | `modules/engagement_hooks.py:575` | `def list_pending_approvals()` |
| `name` | method | `modules/engagement_hooks.py:155` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:178` | `def name(self)` |
| `name` | method | `modules/engagement_hooks.py:213` | `def name(self)` |

Next: [SYMBOLS_p12.md](SYMBOLS_p12.md)
