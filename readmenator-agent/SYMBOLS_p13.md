# Symbols (page 13 of 43)
Previous: [SYMBOLS_p12.md](SYMBOLS_p12.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `EstoridesCaseReader` | class | `modules/estorides_importer.py:385` | `class EstoridesCaseReader` |
| `EstoridesEntity` | class | `modules/estorides_importer.py:84` | `class EstoridesEntity` |
| `EstoridesStixParser` | class | `modules/estorides_importer.py:495` | `class EstoridesStixParser` |
| `EstoridesToLazyOwnBridge` | class | `modules/estorides_importer.py:700` | `class EstoridesToLazyOwnBridge` |
| `FeedbackLoop` | class | `modules/estorides_importer.py:881` | `class FeedbackLoop` |
| `ImportResult` | class | `modules/estorides_importer.py:96` | `class ImportResult` |
| `LanBundleReader` | class | `modules/estorides_importer.py:622` | `class LanBundleReader` |
| `SeedResult` | class | `modules/estorides_importer.py:128` | `class SeedResult` |
| `__init__` | method | `modules/estorides_importer.py:388` | `def __init__(self, db_path)` |
| `__init__` | method | `modules/estorides_importer.py:511` | `def __init__(self, stix_path)` |
| `__init__` | method | `modules/estorides_importer.py:632` | `def __init__(self, lan_dir)` |
| `__init__` | method | `modules/estorides_importer.py:703` | `def __init__(self, db_path, config_path)` |
| `__init__` | method | `modules/estorides_importer.py:892` | `def __init__(self, max_iterations, max_depth, max_steps, timeout)` |
| `_ensure_conn` | method | `modules/estorides_importer.py:396` | `def _ensure_conn(self)` |
| `_extract_value` | method | `modules/estorides_importer.py:563` | `def _extract_value(obj, stix_type)` |
| `_gather_seeds` | method | `modules/estorides_importer.py:1001` | `def _gather_seeds(self, methods, seen)` |
| `_import_to_db` | method | `modules/estorides_importer.py:755` | `def _import_to_db(self, imports, result)` |
| `_import_to_scope` | method | `modules/estorides_importer.py:801` | `def _import_to_scope(self, imports, result)` |
| `attack_targets` | method | `modules/estorides_importer.py:683` | `def attack_targets(self)` |
| `available` | method | `modules/estorides_importer.py:393` | `def available(self)` |
| `available` | method | `modules/estorides_importer.py:515` | `def available(self)` |
| `available` | method | `modules/estorides_importer.py:636` | `def available(self)` |
| `close` | method | `modules/estorides_importer.py:489` | `def close(self)` |
| `ensure_directories` | function | `modules/estorides_importer.py:694` | `def ensure_directories()` |
| `export_combined_graph` | function | `modules/estorides_importer.py:1027` | `def export_combined_graph(output_path)` |
| `extract_seeds_from_db` | function | `modules/estorides_importer.py:203` | `def extract_seeds_from_db(db_path)` |
| `extract_seeds_from_hosts_file` | function | `modules/estorides_importer.py:175` | `def extract_seeds_from_hosts_file(path)` |
| `extract_seeds_from_scope` | function | `modules/estorides_importer.py:242` | `def extract_seeds_from_scope(scope_entries)` |
| `extract_seeds_from_world_model` | function | `modules/estorides_importer.py:143` | `def extract_seeds_from_world_model(world_model_path)` |
| `find_lan_bundle_files` | function | `modules/estorides_importer.py:586` | `def find_lan_bundle_files(lan_dir, sessions_dir)` |
| `get_all_entities` | method | `modules/estorides_importer.py:473` | `def get_all_entities(self, case_id)` |
| `get_combined_surface` | method | `modules/estorides_importer.py:834` | `def get_combined_surface(self)` |
| `get_entities` | method | `modules/estorides_importer.py:414` | `def get_entities(self, case_id, entity_types, limit)` |
| `get_host_entities` | method | `modules/estorides_importer.py:469` | `def get_host_entities(self, case_id)` |
| `import_entities` | method | `modules/estorides_importer.py:711` | `def import_entities(self, entities, add_to_scope, add_to_db)` |
| `list_cases` | method | `modules/estorides_importer.py:402` | `def list_cases(self, limit)` |
| `new_assets` | method | `modules/estorides_importer.py:139` | `def new_assets(self)` |
| `parse` | method | `modules/estorides_importer.py:518` | `def parse(self)` |
| `parse` | method | `modules/estorides_importer.py:652` | `def parse(self)` |
| `parse_by_type` | method | `modules/estorides_importer.py:552` | `def parse_by_type(self, entity_types)` |
| `read_devices` | method | `modules/estorides_importer.py:639` | `def read_devices(self)` |
| `run` | method | `modules/estorides_importer.py:908` | `def run(self, seed_methods)` |
| `run_estorides_discover` | function | `modules/estorides_importer.py:272` | `def run_estorides_discover(seed_type, seed_value, max_depth, max_steps, out_json, timeout)` |
| `run_estorides_run` | function | `modules/estorides_importer.py:332` | `def run_estorides_run(query, out_json, timeout)` |
| `stats` | method | `modules/estorides_importer.py:476` | `def stats(self)` |
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
| `AutoRecommender` | class | `modules/event_consumers.py:201` | `class AutoRecommender` |
| `CredentialReactor` | class | `modules/event_consumers.py:272` | `class CredentialReactor` |
| `DashboardPusher` | class | `modules/event_consumers.py:358` | `class DashboardPusher` |
| `PhaseTracker` | class | `modules/event_consumers.py:146` | `class PhaseTracker` |
| `SoulSync` | class | `modules/event_consumers.py:320` | `class SoulSync` |
| `__call__` | method | `modules/event_consumers.py:159` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:207` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:282` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:323` | `def __call__(self, event)` |
| `__call__` | method | `modules/event_consumers.py:361` | `def __call__(self, event)` |
| `__init__` | method | `modules/event_consumers.py:156` | `def __init__(self)` |
| `__init__` | method | `modules/event_consumers.py:204` | `def __init__(self)` |
| `_inject_objective` | function | `modules/event_consumers.py:54` | `def _inject_objective(text, priority, source)` |
| `_load_payload` | function | `modules/event_consumers.py:43` | `def _load_payload()` |
| `_update_soul` | function | `modules/event_consumers.py:110` | `def _update_soul(phase, credentials, access)` |
| `_update_world_model_host` | function | `modules/event_consumers.py:72` | `def _update_world_model_host(address, state, services)` |
| `unwire_all_consumers` | function | `modules/event_consumers.py:409` | `def unwire_all_consumers(bus)` |
| `wire_all_consumers` | function | `modules/event_consumers.py:380` | `def wire_all_consumers(bus)` |
| `_append_event` | function | `modules/event_engine.py:173` | `def _append_event(event)` |
| `_read_watermark` | function | `modules/event_engine.py:130` | `def _read_watermark()` |
| `_row_matches` | function | `modules/event_engine.py:144` | `def _row_matches(row, trigger)` |
| `_write_watermark` | function | `modules/event_engine.py:137` | `def _write_watermark(offset)` |
| `ack_event` | function | `modules/event_engine.py:270` | `def ack_event(event_id)` |
| `add_rule` | function | `modules/event_engine.py:114` | `def add_rule(rule)` |
| `load_rules` | function | `modules/event_engine.py:99` | `def load_rules()` |
| `process_new_rows` | function | `modules/event_engine.py:181` | `def process_new_rows()` |
| `read_events` | function | `modules/event_engine.py:250` | `def read_events(limit, status)` |
| `save_rules` | function | `modules/event_engine.py:110` | `def save_rules(rules)` |
| `EvidenceConfig` | class | `modules/evidence.py:20` | `class EvidenceConfig` |
| `EvidenceStore` | class | `modules/evidence.py:54` | `class EvidenceStore` |
| `__init__` | method | `modules/evidence.py:57` | `def __init__(self, base_dir)` |
| `_validate_hash` | function | `modules/evidence.py:42` | `def _validate_hash(value)` |
| `blob_path` | method | `modules/evidence.py:65` | `def blob_path(self, content_hash)` |
| `exists` | method | `modules/evidence.py:98` | `def exists(self, content_hash)` |
| `garbage_collect` | method | `modules/evidence.py:105` | `def garbage_collect(self, referenced)` |
| `get` | method | `modules/evidence.py:90` | `def get(self, content_hash)` |
| `hash_bytes` | function | `modules/evidence.py:37` | `def hash_bytes(data)` |
| `put` | method | `modules/evidence.py:70` | `def put(self, data)` |
| `BUFFER` | macro | `modules/exp.c:56` | `#define BUFFER` |
| `DESC_MAX` | macro | `modules/exp.c:54` | `#define DESC_MAX` |
| `ERROR_PREFIX` | macro | `modules/exp.c:58` | `#define ERROR_PREFIX` |
| `INBOUND` | macro | `modules/exp.c:52` | `#define INBOUND` |
| `KEY_DESC_MAX_SIZE` | macro | `modules/exp.c:60` | `#define KEY_DESC_MAX_SIZE` |
| `MQUEUE_NUM` | macro | `modules/exp.c:49` | `#define MQUEUE_NUM` |
| `Msg` | struct | `modules/exp.c:100` | `` |
| `NAMELEN` | macro | `modules/exp.c:57` | `#define NAMELEN` |
| `OUTBOUND` | macro | `modules/exp.c:53` | `#define OUTBOUND` |
| `PHYSMAP_MASK` | macro | `modules/exp.c:67` | `#define PHYSMAP_MASK` |
| `PREFIX_BUF_LEN` | macro | `modules/exp.c:62` | `#define PREFIX_BUF_LEN` |
| `RCU_HEAD_LEN` | macro | `modules/exp.c:63` | `#define RCU_HEAD_LEN` |
| `SPRAY_KEY_SIZE` | macro | `modules/exp.c:65` | `#define SPRAY_KEY_SIZE` |
| `SPRAY_NB_ENTRIES` | macro | `modules/exp.c:71` | `#define SPRAY_NB_ENTRIES` |
| `SPRAY_SIZE` | macro | `modules/exp.c:69` | `#define SPRAY_SIZE` |
| `_GNU_SOURCE` | macro | `modules/exp.c:2` | `#define _GNU_SOURCE` |
| `add_key` | function | `modules/exp.c:147` | `static inline key_serial_t add_key(const char *type, const char *description, const void *payload...` |
| `awake_partial_keys` | function | `modules/exp.c:271` | `void awake_partial_keys(key_serial_t *id_buffer, uint32_t idx)` |
| `bye` | function | `modules/exp.c:155` | `void bye(char *info)` |
| `bye2` | function | `modules/exp.c:167` | `void bye2(char *info, char *arg)` |
| `create_dummy_file` | function | `modules/exp.c:564` | `void create_dummy_file(void)` |
| `create_priv_file` | function | `modules/exp.c:572` | `void create_priv_file(void)` |
| `do_error_exit` | function | `modules/exp.c:161` | `void do_error_exit(char *info)` |
| `fd_uring` | struct | `modules/exp.c:131` | `` |
| `gather_mqueue` | function | `modules/exp.c:463` | `int gather_mqueue(mqd_t mqdes, int gather_size)` |
| `gather_mqueue_nosave` | function | `modules/exp.c:485` | `int gather_mqueue_nosave(mqd_t mqdes, int gather_size)` |
| `get_keyring_leak` | function | `modules/exp.c:248` | `int get_keyring_leak(key_serial_t *id_buffer, uint32_t id_buffer_size)` |
| `io_uring_register` | function | `modules/exp.c:524` | `static inline int io_uring_register(int fd, unsigned int opcode, void *arg, unsigned int nr_args)` |
| `io_uring_setup` | function | `modules/exp.c:520` | `static inline int io_uring_setup(uint32_t entries, struct io_uring_params *p)` |
| `key_serial_t` | type_alias | `modules/exp.c:135` | `typedef int32_t key_serial_t;` |
| `keyctl` | function | `modules/exp.c:151` | `static inline long keyctl(int operation, unsigned long arg2, unsigned long arg3, unsigned long ar...` |
| `keyring_payload` | struct | `modules/exp.c:120` | `` |
| `leak` | struct | `modules/exp.c:126` | `` |
| `main` | function | `modules/exp.c:620` | `int main(int argc, char ** argv)` |
| `msg` | struct | `modules/exp.c:84` | `` |
| `msg_header` | struct | `modules/exp.c:90` | `` |
| `nft_trans_phase` | enum | `modules/exp.c:77` | `` |
| `prepare_root_shell` | function | `modules/exp.c:559` | `void prepare_root_shell(void)` |
| `release_keys` | function | `modules/exp.c:279` | `void release_keys(key_serial_t *id_buffer, uint32_t id_buffer_size)` |
| `release_partial_keys` | function | `modules/exp.c:290` | `void release_partial_keys(key_serial_t *id_buffer, int i)` |
| `release_partial_uring` | function | `modules/exp.c:554` | `void release_partial_uring(struct fd_uring *fd_buffer, uint32_t buffer_idx)` |
| `release_uring` | function | `modules/exp.c:546` | `void release_uring(struct fd_uring *fd_buffer, uint32_t buffer_size)` |
| `sema_down` | function | `modules/exp.c:615` | `void sema_down(int *sema)` |
| `sema_up` | function | `modules/exp.c:610` | `void sema_up(int *sema)` |
| `set_cpu_affinity` | function | `modules/exp.c:438` | `void set_cpu_affinity(int cpu_n, pid_t pid)` |
| `set_stable_table_and_set` | function | `modules/exp.c:322` | `void set_stable_table_and_set(struct mnl_socket* nl, const char *name)` |
| `set_trigger_set_and_overwrite` | function | `modules/exp.c:385` | `void set_trigger_set_and_overwrite(struct mnl_socket* nl, const char *name, const char *set_name)` |
| `setup_modprobe_payload` | function | `modules/exp.c:601` | `void setup_modprobe_payload()` |
| `spray_keyring` | function | `modules/exp.c:172` | `key_serial_t *spray_keyring(uint32_t start, uint32_t spray_size)` |
| `spray_keyring_list_del_purpose` | function | `modules/exp.c:190` | `key_serial_t *spray_keyring_list_del_purpose(uint32_t spray_size, uint64_t next, uint64_t prev, u...` |
| `spray_keyring_list_overwrite_purpose` | function | `modules/exp.c:214` | `key_serial_t *spray_keyring_list_overwrite_purpose(uint32_t spray_size, uint64_t len, uint64_t of...` |
| `spray_mqueue` | function | `modules/exp.c:448` | `void spray_mqueue(mqd_t mqdes, char *msgptr, int spray_size)` |
| `spray_msg_msg` | function | `modules/exp.c:496` | `void spray_msg_msg(unsigned int size, unsigned int amount, int qid)` |
| `spray_uring` | function | `modules/exp.c:529` | `struct fd_uring *spray_uring(uint32_t spray_size, struct fd_uring *fd_buffer)` |
| `unshare_setup` | function | `modules/exp.c:297` | `void unshare_setup(uid_t uid, gid_t gid)` |
| `user_rule_t` | struct | `modules/exp.c:105` | `` |
| `userland_T` | function | `modules/exp.c:605` | `void userland_T(int *sema)` |
| `write_new_modprobe` | function | `modules/exp.c:582` | `void write_new_modprobe()` |
| `ChainResult` | class | `modules/exploit_chain.py:65` | `class ChainResult` |
| `ExploitChain` | class | `modules/exploit_chain.py:289` | `class ExploitChain` |
| `ExploitResult` | class | `modules/exploit_chain.py:54` | `class ExploitResult` |
| `ServiceInfo` | class | `modules/exploit_chain.py:29` | `class ServiceInfo` |
| `VulnerabilityMatch` | class | `modules/exploit_chain.py:41` | `class VulnerabilityMatch` |
| `__init__` | method | `modules/exploit_chain.py:292` | `def __init__(self, rhost, rport, lhost, lport, sessions_dir, nmap_xml_path)` |
| `_add_vuln` | method | `modules/exploit_chain.py:485` | `def _add_vuln(self, service, sig, version)` |
| `_compare_versions` | function | `modules/exploit_chain.py:266` | `def _compare_versions(version_a, version_b)` |
| `_discover_xml_files` | method | `modules/exploit_chain.py:331` | `def _discover_xml_files(self)` |
| `_is_richer` | method | `modules/exploit_chain.py:361` | `def _is_richer(new_svc, existing)` |
| `_parse_all_nmap_xml` | method | `modules/exploit_chain.py:346` | `def _parse_all_nmap_xml(self)` |
| `_parse_nmap_text` | method | `modules/exploit_chain.py:404` | `def _parse_nmap_text(self, output)` |
| `_parse_single_xml` | method | `modules/exploit_chain.py:367` | `def _parse_single_xml(self, xml_path)` |
| `fingerprint_services` | method | `modules/exploit_chain.py:311` | `def fingerprint_services(self, nmap_output)` |
| `generate_exploit_plan` | method | `modules/exploit_chain.py:499` | `def generate_exploit_plan(self)` |
| `generate_report` | method | `modules/exploit_chain.py:531` | `def generate_report(self)` |
| `get_post_exploit_commands` | method | `modules/exploit_chain.py:519` | `def get_post_exploit_commands(self, platform)` |
| `map_vulnerabilities` | method | `modules/exploit_chain.py:446` | `def map_vulnerabilities(self)` |
| `save_report` | method | `modules/exploit_chain.py:566` | `def save_report(self, path)` |
| `ExploitMatch` | class | `modules/exploit_recommender.py:37` | `class ExploitMatch` |
| `ExploitRecommender` | class | `modules/exploit_recommender.py:50` | `class ExploitRecommender` |
| `__init__` | method | `modules/exploit_recommender.py:120` | `def __init__(self, world_model)` |
| `_compare_versions` | method | `modules/exploit_recommender.py:165` | `def _compare_versions(version, max_vulnerable)` |
| `_extract_cve_ids` | method | `modules/exploit_recommender.py:161` | `def _extract_cve_ids(text)` |
| `_generate_lazyown_commands` | method | `modules/exploit_recommender.py:214` | `def _generate_lazyown_commands(self, cve_id, service, host_ip)` |
| `_load_exploitdb` | method | `modules/exploit_recommender.py:135` | `def _load_exploitdb(self)` |
| `_query_nvd` | method | `modules/exploit_recommender.py:175` | `def _query_nvd(self, cve_id)` |
| `_try_nvd` | method | `modules/exploit_recommender.py:211` | `def _try_nvd(self, cve_id)` |
| `format_for_llm` | method | `modules/exploit_recommender.py:390` | `def format_for_llm(self, matches, max_items)` |
| `match_services` | method | `modules/exploit_recommender.py:244` | `def match_services(self, hosts)` |
| `parse_version` | function | `modules/exploit_recommender.py:25` | `def parse_version(v)` |
| `persist_recommendations` | method | `modules/exploit_recommender.py:370` | `def persist_recommendations(self, matches)` |
| `recommend` | method | `modules/exploit_recommender.py:337` | `def recommend(self, hosts, top_n)` |
| `set_nvd_api_key` | method | `modules/exploit_recommender.py:132` | `def set_nvd_api_key(self, key)` |
| `set_world_model` | method | `modules/exploit_recommender.py:129` | `def set_world_model(self, world_model)` |
| `_detect_domain` | function | `modules/exploitgym_gym.py:96` | `def _detect_domain(task_id)` |
| `_ensure_clone` | function | `modules/exploitgym_gym.py:232` | `def _ensure_clone(root, timeout)` |
| `_ensure_dir` | function | `modules/exploitgym_gym.py:56` | `def _ensure_dir()` |
| `_env_for_run` | function | `modules/exploitgym_gym.py:315` | `def _env_for_run(params)` |
| `_extract_flag` | function | `modules/exploitgym_gym.py:487` | `def _extract_flag(output)` |
| `_load_records` | function | `modules/exploitgym_gym.py:500` | `def _load_records()` |
| `_read_task_ids` | function | `modules/exploitgym_gym.py:75` | `def _read_task_ids(root)` |
| `_record` | function | `modules/exploitgym_gym.py:523` | `def _record(task_id, success, elapsed, flag)` |
| `_resolve_root` | function | `modules/exploitgym_gym.py:61` | `def _resolve_root(params)` |
| `_run` | function | `modules/exploitgym_gym.py:274` | `def _run(name, cmd, cwd, timeout)` |
| `_run_agent` | function | `modules/exploitgym_gym.py:378` | `def _run_agent(task_id, model, mitigations, root, params, timeout)` |
| `_run_streaming` | function | `modules/exploitgym_gym.py:206` | `def _run_streaming(cmd, cwd, timeout)` |
| `_save_records` | function | `modules/exploitgym_gym.py:514` | `def _save_records(records)` |
| `check_readiness` | function | `modules/exploitgym_gym.py:112` | `def check_readiness(params)` |
| `list_tasks` | function | `modules/exploitgym_gym.py:178` | `def list_tasks(params, domain, limit)` |
| `pull_task` | function | `modules/exploitgym_gym.py:344` | `def pull_task(task_id, params, timeout)` |
| `run_task` | function | `modules/exploitgym_gym.py:423` | `def run_task(task_id, params, model, mitigations, timeout)` |
| `score_task` | function | `modules/exploitgym_gym.py:565` | `def score_task(task_id, success, techniques, params)` |
| `setup_harness` | function | `modules/exploitgym_gym.py:249` | `def setup_harness(params, steps)` |
| `verify_flag` | function | `modules/exploitgym_gym.py:548` | `def verify_flag(task_id, params)` |
| `chown_project_tree` | function | `modules/fast_run_service.sh:310` | `` |
| `cmd_chown_now` | function | `modules/fast_run_service.sh:521` | `` |
| `cmd_logs` | function | `modules/fast_run_service.sh:505` | `` |
| `cmd_restart` | function | `modules/fast_run_service.sh:480` | `` |
| `cmd_start` | function | `modules/fast_run_service.sh:445` | `` |
| `cmd_status` | function | `modules/fast_run_service.sh:486` | `` |
| `cmd_stop` | function | `modules/fast_run_service.sh:465` | `` |
| `config_truthy` | function | `modules/fast_run_service.sh:155` | `` |
| `ensure_log_file` | function | `modules/fast_run_service.sh:211` | `` |
| `is_pid_alive` | function | `modules/fast_run_service.sh:189` | `` |
| `is_service_running` | function | `modules/fast_run_service.sh:194` | `` |
| `load_config` | function | `modules/fast_run_service.sh:139` | `` |
| `log_error` | function | `modules/fast_run_service.sh:81` | `` |
| `log_file_for` | function | `modules/fast_run_service.sh:171` | `` |
| `log_info` | function | `modules/fast_run_service.sh:73` | `` |
| `log_timestamp` | function | `modules/fast_run_service.sh:69` | `` |
| `log_warn` | function | `modules/fast_run_service.sh:77` | `` |
| `main` | function | `modules/fast_run_service.sh:557` | `` |
| `managed_services_in_order` | function | `modules/fast_run_service.sh:429` | `` |
| `pid_file_for` | function | `modules/fast_run_service.sh:166` | `` |
| `prepare_runtime_dirs` | function | `modules/fast_run_service.sh:126` | `` |
| `read_pid_value` | function | `modules/fast_run_service.sh:176` | `` |
| `require_deps` | function | `modules/fast_run_service.sh:97` | `` |
| `require_paths` | function | `modules/fast_run_service.sh:113` | `` |
| `require_root` | function | `modules/fast_run_service.sh:89` | `` |
| `spawn_as_root` | function | `modules/fast_run_service.sh:247` | `` |
| `spawn_as_target_user` | function | `modules/fast_run_service.sh:228` | `` |
| `start_chown_watcher` | function | `modules/fast_run_service.sh:315` | `` |
| `start_cloudflare_service` | function | `modules/fast_run_service.sh:400` | `` |
| `start_discord_service` | function | `modules/fast_run_service.sh:380` | `` |
| `start_lazyc2_service` | function | `modules/fast_run_service.sh:342` | `` |
| `start_ollama_service` | function | `modules/fast_run_service.sh:410` | `` |
| `start_telegram_service` | function | `modules/fast_run_service.sh:390` | `` |
| `start_vpn_service` | function | `modules/fast_run_service.sh:363` | `` |
| `start_www_service` | function | `modules/fast_run_service.sh:356` | `` |
| `stop_named_service` | function | `modules/fast_run_service.sh:292` | `` |
| `terminate_pid_tree` | function | `modules/fast_run_service.sh:264` | `` |
| `usage` | function | `modules/fast_run_service.sh:528` | `` |
| `write_pid_file` | function | `modules/fast_run_service.sh:201` | `` |
| `FindingRecord` | class | `modules/finding_lifecycle.py:182` | `class FindingRecord` |
| `RetestRecord` | class | `modules/finding_lifecycle.py:195` | `class RetestRecord` |
| `_finding_from_row` | function | `modules/finding_lifecycle.py:220` | `def _finding_from_row(row)` |
| `_load` | function | `modules/finding_lifecycle.py:40` | `def _load(sessions_dir)` |
| `_load_retests` | function | `modules/finding_lifecycle.py:292` | `def _load_retests(sessions_dir)` |
| `_retests_path` | function | `modules/finding_lifecycle.py:287` | `def _retests_path(sessions_dir)` |
| `_save` | function | `modules/finding_lifecycle.py:53` | `def _save(sessions_dir, data)` |
| `_save_retests` | function | `modules/finding_lifecycle.py:303` | `def _save_retests(sessions_dir, payload)` |
| `_store_path` | function | `modules/finding_lifecycle.py:35` | `def _store_path(sessions_dir)` |
| `_token_value` | function | `modules/finding_lifecycle.py:205` | `def _token_value(refs, prefix, default)` |
| `_with_token` | function | `modules/finding_lifecycle.py:213` | `def _with_token(refs, prefix, value)` |
| `add_dead_end` | function | `modules/finding_lifecycle.py:104` | `def add_dead_end(kind, value, reason, sessions_dir)` |
| `apply_confirmation` | function | `modules/finding_lifecycle.py:154` | `def apply_confirmation(nodes, sessions_dir)` |
| `classify_retest` | function | `modules/finding_lifecycle.py:384` | `def classify_retest(needle, output)` |
| `confirm` | function | `modules/finding_lifecycle.py:61` | `def confirm(finding_id, evidence, sessions_dir, by)` |
| `findings_for` | function | `modules/finding_lifecycle.py:259` | `def findings_for(db, workspace)` |
| `has_running_retest` | function | `modules/finding_lifecycle.py:310` | `def has_running_retest(finding_id, sessions_dir)` |
| `is_dead_end` | function | `modules/finding_lifecycle.py:116` | `def is_dead_end(kind, value, sessions_dir)` |
| `record` | function | `modules/finding_lifecycle.py:234` | `def record(db, workspace, host, title, severity, summary, poc)` |
| `reject` | function | `modules/finding_lifecycle.py:90` | `def reject(finding_id, reason, sessions_dir, by)` |
| `render_markdown` | function | `modules/finding_lifecycle.py:403` | `def render_markdown(db, workspace, title)` |
| `request_retest` | function | `modules/finding_lifecycle.py:318` | `def request_retest(db, finding_id, sessions_dir)` |
| `resolve` | function | `modules/finding_lifecycle.py:129` | `def resolve(node, sessions_dir)` |
| `resolve_retest` | function | `modules/finding_lifecycle.py:338` | `def resolve_retest(db, retest_id, conclusion, evidence, sessions_dir)` |
| `set_status` | function | `modules/finding_lifecycle.py:264` | `def set_status(db, finding_id, status)` |
| `suppressed_values` | function | `modules/finding_lifecycle.py:123` | `def suppressed_values(sessions_dir)` |
| `ForensicCleaner` | class | `modules/forensic_cleaner.py:57` | `class ForensicCleaner` |
| `ForensicCleanerConfig` | class | `modules/forensic_cleaner.py:23` | `class ForensicCleanerConfig` |
| `__init__` | method | `modules/forensic_cleaner.py:67` | `def __init__(self, config)` |
| `amcache_parse` | method | `modules/forensic_cleaner.py:259` | `def amcache_parse(self)` |
| `linux_cleanup` | method | `modules/forensic_cleaner.py:165` | `def linux_cleanup(self)` |
| `macos_cleanup` | method | `modules/forensic_cleaner.py:193` | `def macos_cleanup(self)` |
| `windows_cleanup` | method | `modules/forensic_cleaner.py:70` | `def windows_cleanup(self)` |
| `windows_prefetch_parse` | method | `modules/forensic_cleaner.py:221` | `def windows_prefetch_parse(self, prefetch_path)` |
| `GCPAttackEngine` | class | `modules/gcp_attacks.py:77` | `class GCPAttackEngine` |
| `GCPConfig` | class | `modules/gcp_attacks.py:57` | `class GCPConfig` |
| `__init__` | method | `modules/gcp_attacks.py:90` | `def __init__(self, config)` |

Next: [SYMBOLS_p14.md](SYMBOLS_p14.md)
