# Symbols (page 16 of 49)
Previous: [SYMBOLS_p15.md](SYMBOLS_p15.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_existing_chain_tokens` | function | `modules/lazy_autofire.py:215` | `def _existing_chain_tokens(chains_dir, slug)` |
| `_fire_matches` | function | `modules/lazy_autofire.py:166` | `def _fire_matches(report)` |
| `_load_state` | function | `modules/lazy_autofire.py:281` | `def _load_state(path)` |
| `_save_state` | function | `modules/lazy_autofire.py:291` | `def _save_state(path, state)` |
| `_slug` | function | `modules/lazy_autofire.py:312` | `def _slug(text)` |
| `_stamp_cooldown` | function | `modules/lazy_autofire.py:305` | `def _stamp_cooldown(state, target, cves, moment)` |
| `autofire_armed` | function | `modules/lazy_autofire.py:41` | `def autofire_armed(payload)` |
| `consider_report` | function | `modules/lazy_autofire.py:53` | `def consider_report(report, chains_dir, state_path, armed, now)` |
| `fire_from_file` | function | `modules/lazy_autofire.py:105` | `def fire_from_file(target, feed_path)` |
| `status` | function | `modules/lazy_autofire.py:147` | `def status(payload, state_path)` |
| `sweep_state` | function | `modules/lazy_autofire.py:127` | `def sweep_state(state_path, now)` |
| `_data_dir` | function | `modules/lazy_bridge.py:35` | `def _data_dir()` |
| `_extract_hosts_from_graph` | function | `modules/lazy_bridge.py:184` | `def _extract_hosts_from_graph(graph)` |
| `_notify` | function | `modules/lazy_bridge.py:398` | `def _notify(progress, text)` |
| `_read_json` | function | `modules/lazy_bridge.py:51` | `def _read_json(path, default)` |
| `_read_jsonl` | function | `modules/lazy_bridge.py:68` | `def _read_jsonl(path)` |
| `_read_new_traffic` | function | `modules/lazy_bridge.py:361` | `def _read_new_traffic(path, offset)` |
| `_record_sync` | function | `modules/lazy_bridge.py:592` | `def _record_sync(action, summary)` |
| `bridge_status` | function | `modules/lazy_bridge.py:163` | `def bridge_status()` |
| `lazy_activity` | function | `modules/lazy_bridge.py:127` | `def lazy_activity(task_id)` |
| `lazy_assets` | function | `modules/lazy_bridge.py:103` | `def lazy_assets()` |
| `lazy_graph` | function | `modules/lazy_bridge.py:114` | `def lazy_graph(task_id)` |
| `lazy_guard_audit` | function | `modules/lazy_bridge.py:151` | `def lazy_guard_audit(task_id)` |
| `lazy_tasks` | function | `modules/lazy_bridge.py:92` | `def lazy_tasks()` |
| `lazy_traffic` | function | `modules/lazy_bridge.py:139` | `def lazy_traffic(task_id)` |
| `pull_findings_to_lifecycle` | function | `modules/lazy_bridge.py:333` | `def pull_findings_to_lifecycle()` |
| `pull_to_objectives` | function | `modules/lazy_bridge.py:298` | `def pull_to_objectives()` |
| `pull_to_world_model` | function | `modules/lazy_bridge.py:221` | `def pull_to_world_model()` |
| `pull_traffic_to_recorder` | function | `modules/lazy_bridge.py:408` | `def pull_traffic_to_recorder(progress)` |
| `push_objective_to_lazy` | function | `modules/lazy_bridge.py:476` | `def push_objective_to_lazy(goal, scope)` |
| `push_tasks_to_c2` | function | `modules/lazy_bridge.py:501` | `def push_tasks_to_c2(only)` |
| `sync_all` | function | `modules/lazy_bridge.py:566` | `def sync_all(progress)` |
| `_range_says` | function | `modules/lazy_checks.py:105` | `def _range_says(version, ranges)` |
| `extract_cve` | function | `modules/lazy_checks.py:51` | `def extract_cve(text)` |
| `extract_version` | function | `modules/lazy_checks.py:30` | `def extract_version(text)` |
| `interpret_checks` | function | `modules/lazy_checks.py:57` | `def interpret_checks(checks, cve, stored_version, ranges)` |
| `_discover` | function | `modules/lazy_cli_bridge.py:93` | `def _discover()` |
| `_source_files` | function | `modules/lazy_cli_bridge.py:74` | `def _source_files()` |
| `_source_mtimes` | function | `modules/lazy_cli_bridge.py:82` | `def _source_mtimes()` |
| `build_cli_command` | function | `modules/lazy_cli_bridge.py:158` | `def build_cli_command(verb, target)` |
| `catalog_cli_for_phase` | function | `modules/lazy_cli_bridge.py:219` | `def catalog_cli_for_phase(limit)` |
| `cli_catalog_for_phase` | function | `modules/lazy_cli_bridge.py:211` | `def cli_catalog_for_phase(phase, limit)` |
| `cli_verbs` | function | `modules/lazy_cli_bridge.py:106` | `def cli_verbs()` |
| `full_cli_enabled` | function | `modules/lazy_cli_bridge.py:253` | `def full_cli_enabled()` |
| `is_cli_verb` | function | `modules/lazy_cli_bridge.py:125` | `def is_cli_verb(name)` |
| `needs_target_for` | function | `modules/lazy_cli_bridge.py:150` | `def needs_target_for(verb)` |
| `phase_for` | function | `modules/lazy_cli_bridge.py:131` | `def phase_for(verb)` |
| `risk_for` | function | `modules/lazy_cli_bridge.py:140` | `def risk_for(verb)` |
| `search_cli_verbs` | function | `modules/lazy_cli_bridge.py:185` | `def search_cli_verbs(query, phase, limit)` |
| `set_full_cli` | function | `modules/lazy_cli_bridge.py:276` | `def set_full_cli(enabled)` |
| `CredRow` | class | `modules/lazy_creds.py:30` | `class CredRow` |
| `as_lines` | function | `modules/lazy_creds.py:101` | `def as_lines(rows)` |
| `candidates` | function | `modules/lazy_creds.py:79` | `def candidates(limit)` |
| `count` | function | `modules/lazy_creds.py:96` | `def count()` |
| `export_pairs` | function | `modules/lazy_creds.py:106` | `def export_pairs(path, limit)` |
| `load` | function | `modules/lazy_creds.py:39` | `def load()` |
| `search` | function | `modules/lazy_creds.py:63` | `def search(query)` |
| `_advisory_cve_id` | function | `modules/lazy_cve_feed.py:398` | `def _advisory_cve_id(advisory)` |
| `_advisory_cvss` | function | `modules/lazy_cve_feed.py:407` | `def _advisory_cvss(advisory)` |
| `_advisory_matches_product` | function | `modules/lazy_cve_feed.py:421` | `def _advisory_matches_product(advisory, banner_words)` |
| `_cache_fresh` | function | `modules/lazy_cve_feed.py:104` | `def _cache_fresh(path, ttl_sec)` |
| `_cache_path` | function | `modules/lazy_cve_feed.py:95` | `def _cache_path(name)` |
| `_cached_advisories` | function | `modules/lazy_cve_feed.py:544` | `def _cached_advisories()` |
| `_env_flag` | function | `modules/lazy_cve_feed.py:90` | `def _env_flag(name, default)` |
| `_exploit_cves_from_text` | function | `modules/lazy_cve_feed.py:228` | `def _exploit_cves_from_text(text)` |
| `_fetch` | function | `modules/lazy_cve_feed.py:112` | `def _fetch(url)` |
| `_load_json` | function | `modules/lazy_cve_feed.py:150` | `def _load_json(name)` |
| `_osv_cache_path` | function | `modules/lazy_cve_feed.py:281` | `def _osv_cache_path(product)` |
| `_store_bytes` | function | `modules/lazy_cve_feed.py:134` | `def _store_bytes(name, payload)` |
| `_store_json` | function | `modules/lazy_cve_feed.py:142` | `def _store_json(name, data)` |
| `_worker` | function | `modules/lazy_cve_feed.py:696` | `def _worker()` |
| `convert_osv_ranges` | function | `modules/lazy_cve_feed.py:515` | `def convert_osv_ranges(affected)` |
| `correlate` | function | `modules/lazy_cve_feed.py:438` | `def correlate(product, version, allow_network)` |
| `cve_intel` | function | `modules/lazy_cve_feed.py:360` | `def cve_intel(cve_id, feeds, allow_network)` |
| `fetch_product_advisories` | function | `modules/lazy_cve_feed.py:291` | `def fetch_product_advisories(product, force)` |
| `hot_matches` | function | `modules/lazy_cve_feed.py:636` | `def hot_matches(services, allow_network)` |
| `load_epss` | function | `modules/lazy_cve_feed.py:192` | `def load_epss(force)` |
| `load_exploit_cves` | function | `modules/lazy_cve_feed.py:233` | `def load_exploit_cves(force)` |
| `load_kev` | function | `modules/lazy_cve_feed.py:158` | `def load_kev(force)` |
| `load_kev_matches` | function | `modules/lazy_cve_feed.py:594` | `def load_kev_matches(product, feeds)` |
| `load_msf_cves` | function | `modules/lazy_cve_feed.py:257` | `def load_msf_cves(force)` |
| `range_for_cve` | function | `modules/lazy_cve_feed.py:565` | `def range_for_cve(cve_id, allow_network)` |
| `refresh_feeds_async` | function | `modules/lazy_cve_feed.py:680` | `def refresh_feeds_async(products)` |
| `LazyEngine` | class | `modules/lazy_engine.py:56` | `class LazyEngine(LazyLoopEngine)` |
| `_int` | function | `modules/lazy_exposure.py:410` | `def _int(value, fallback)` |
| `_live_fingerprint` | function | `modules/lazy_exposure.py:210` | `def _live_fingerprint()` |
| `_match_hot_key` | function | `modules/lazy_exposure.py:400` | `def _match_hot_key(row)` |
| `_shape_sightings` | function | `modules/lazy_exposure.py:370` | `def _shape_sightings(rows)` |
| `_short_refs` | function | `modules/lazy_exposure.py:365` | `def _short_refs(row)` |
| `_slug` | function | `modules/lazy_exposure.py:405` | `def _slug(text)` |
| `ensure_report` | function | `modules/lazy_exposure.py:56` | `def ensure_report(target, entries, refresh)` |
| `generate_report` | function | `modules/lazy_exposure.py:129` | `def generate_report(target, entries, sightings)` |
| `probe_checks` | function | `modules/lazy_exposure.py:257` | `def probe_checks(matches, feed)` |
| `publish_report` | function | `modules/lazy_exposure.py:314` | `def publish_report(report)` |
| `read_sightings` | function | `modules/lazy_exposure.py:97` | `def read_sightings(target, state_path)` |
| `refresh_if_stale` | function | `modules/lazy_exposure.py:418` | `def refresh_if_stale(target, entries)` |
| `save_report` | function | `modules/lazy_exposure.py:291` | `def save_report(report, path)` |
| `score_report` | function | `modules/lazy_exposure.py:219` | `def score_report(entries, bounded_unknown, services)` |
| `ExploitSighting` | class | `modules/lazy_feedmatch.py:123` | `class ExploitSighting` |
| `FeedEntry` | class | `modules/lazy_feedmatch.py:73` | `class FeedEntry` |
| `Sighting` | class | `modules/lazy_feedmatch.py:98` | `class Sighting` |
| `_cvss` | function | `modules/lazy_feedmatch.py:470` | `def _cvss(value)` |
| `_fixed_key` | function | `modules/lazy_feedmatch.py:316` | `def _fixed_key(rng)` |
| `_float` | function | `modules/lazy_feedmatch.py:478` | `def _float(value)` |
| `_map_kev_row` | function | `modules/lazy_feedmatch.py:187` | `def _map_kev_row(item)` |
| `_references` | function | `modules/lazy_feedmatch.py:464` | `def _references(raw)` |
| `bind_sighting` | function | `modules/lazy_feedmatch.py:337` | `def bind_sighting(sighting, entries)` |
| `entry_matches_product` | function | `modules/lazy_feedmatch.py:262` | `def entry_matches_product(entry, product)` |
| `feed_fingerprint` | function | `modules/lazy_feedmatch.py:486` | `def feed_fingerprint(entries)` |
| `feed_tier` | function | `modules/lazy_feedmatch.py:325` | `def feed_tier(entry)` |
| `is_os_sighting` | function | `modules/lazy_feedmatch.py:248` | `def is_os_sighting(name)` |
| `live_bindings` | function | `modules/lazy_feedmatch.py:411` | `def live_bindings(sighting, allow_network)` |
| `load_feed` | function | `modules/lazy_feedmatch.py:151` | `def load_feed(path)` |
| `parse_feed` | function | `modules/lazy_feedmatch.py:210` | `def parse_feed(entries)` |
| `unversioned_leads` | function | `modules/lazy_feedmatch.py:388` | `def unversioned_leads(sightings)` |
| `version_in_ranges` | function | `modules/lazy_feedmatch.py:280` | `def version_in_ranges(version, ranges)` |
| `FindingValidationError` | class | `modules/lazy_findings.py:60` | `class FindingValidationError(ValueError)` |
| `FindingsLedger` | class | `modules/lazy_findings.py:539` | `class FindingsLedger` |
| `LedgerLimits` | class | `modules/lazy_findings.py:65` | `class LedgerLimits` |
| `__init__` | method | `modules/lazy_findings.py:542` | `def __init__(self, engagement_id, base_dir, limits, scrub)` |
| `_base_row` | function | `modules/lazy_findings.py:344` | `def _base_row(payload, bounds)` |
| `_now_iso` | function | `modules/lazy_findings.py:534` | `def _now_iso()` |
| `_row_from_verdict` | function | `modules/lazy_findings.py:294` | `def _row_from_verdict(payload, verdict, bounds)` |
| `append` | method | `modules/lazy_findings.py:606` | `def append(self, row)` |
| `build_handoff` | function | `modules/lazy_findings.py:481` | `def build_handoff(rows, status, rounds)` |
| `clamped` | method | `modules/lazy_findings.py:81` | `def clamped(self)` |
| `discard_row` | function | `modules/lazy_findings.py:382` | `def discard_row(reason, command, output, technique_id, engagement_id, target)` |
| `engagement_id_valid` | function | `modules/lazy_findings.py:91` | `def engagement_id_valid(value)` |
| `evidence_reject_reason` | function | `modules/lazy_findings.py:156` | `def evidence_reject_reason(state, evidence, min_output)` |
| `evidence_supported` | function | `modules/lazy_findings.py:281` | `def evidence_supported(evidence, min_output)` |
| `file_path` | method | `modules/lazy_findings.py:569` | `def file_path(self)` |
| `history` | method | `modules/lazy_findings.py:684` | `def history(self, finding_ref)` |
| `latest_state` | method | `modules/lazy_findings.py:696` | `def latest_state(self, finding_ref)` |
| `level_for_state_uplift` | function | `modules/lazy_findings.py:138` | `def level_for_state_uplift(level, state)` |
| `metadata_level` | function | `modules/lazy_findings.py:217` | `def metadata_level(payload)` |
| `normalize` | method | `modules/lazy_findings.py:573` | `def normalize(self, row)` |
| `normalize_finding` | function | `modules/lazy_findings.py:429` | `def normalize_finding(row, limits)` |
| `read` | method | `modules/lazy_findings.py:636` | `def read(self, cursor, limit)` |
| `row_from_event` | function | `modules/lazy_findings.py:230` | `def row_from_event(payload, limits)` |
| `rows` | method | `modules/lazy_findings.py:660` | `def rows(self)` |
| `severity_tier` | function | `modules/lazy_findings.py:116` | `def severity_tier(severity)` |
| `state_counts` | function | `modules/lazy_findings.py:191` | `def state_counts(rows)` |
| `technique_id_valid` | function | `modules/lazy_findings.py:103` | `def technique_id_valid(value)` |
| `backport_status` | function | `modules/lazy_heat.py:345` | `def backport_status(banner, fixed_revision)` |
| `classify_heat` | function | `modules/lazy_heat.py:71` | `def classify_heat(kev, epss, exploit, cvss)` |
| `compare_versions` | function | `modules/lazy_heat.py:157` | `def compare_versions(a, b)` |
| `cvss3_base_score` | function | `modules/lazy_heat.py:207` | `def cvss3_base_score(vector)` |
| `heat_of_severity` | function | `modules/lazy_heat.py:373` | `def heat_of_severity(severity)` |
| `heat_rank` | function | `modules/lazy_heat.py:392` | `def heat_rank(tier)` |
| `host_heat` | function | `modules/lazy_heat.py:404` | `def host_heat(tier_values, severity_levels, unscanned)` |
| `hottest` | function | `modules/lazy_heat.py:424` | `def hottest(tier_values)` |
| `label_for` | function | `modules/lazy_heat.py:438` | `def label_for(status, fixed_revision)` |
| `match_heat` | function | `modules/lazy_heat.py:94` | `def match_heat(tier, cvss, verdict, distro_status)` |
| `parse_distro_revision` | function | `modules/lazy_heat.py:306` | `def parse_distro_revision(banner)` |
| `parse_version` | function | `modules/lazy_heat.py:121` | `def parse_version(value, strict)` |
| `product_token` | function | `modules/lazy_heat.py:249` | `def product_token(value)` |
| `token_matches` | function | `modules/lazy_heat.py:272` | `def token_matches(haystack, needle)` |
| `version_in_range` | function | `modules/lazy_heat.py:165` | `def version_in_range(ver, rng)` |
| `_add` | function | `modules/lazy_hostscore.py:49` | `def _add(label, points)` |
| `_persist` | function | `modules/lazy_hostscore.py:182` | `def _persist(table, sessions_dir, now)` |
| `load_scores` | function | `modules/lazy_hostscore.py:193` | `def load_scores(sessions_dir)` |
| `rescore` | function | `modules/lazy_hostscore.py:96` | `def rescore(sessions_dir, allow_network, now)` |
| `score_host` | function | `modules/lazy_hostscore.py:34` | `def score_host(inputs)` |
| `install_command_for` | function | `modules/lazy_installer.py:70` | `def install_command_for(tool)` |
| `installer_enabled` | function | `modules/lazy_installer.py:41` | `def installer_enabled()` |
| `intent_for` | function | `modules/lazy_installer.py:75` | `def intent_for(tool)` |
| `set_installer_enabled` | function | `modules/lazy_installer.py:58` | `def set_installer_enabled(enabled)` |
| `steps_for_install` | function | `modules/lazy_installer.py:88` | `def steps_for_install(text)` |
| `tool_from_intent` | function | `modules/lazy_installer.py:80` | `def tool_from_intent(text)` |
| `_append` | function | `modules/lazy_intel.py:79` | `def _append(record)` |
| `_is_ip_literal` | function | `modules/lazy_intel.py:292` | `def _is_ip_literal(value)` |
| `_log_path` | function | `modules/lazy_intel.py:35` | `def _log_path()` |
| `_mask` | function | `modules/lazy_intel.py:41` | `def _mask(text)` |
| `_now` | function | `modules/lazy_intel.py:30` | `def _now()` |
| `describe_command` | function | `modules/lazy_intel.py:114` | `def describe_command(command)` |
| `export_spans` | function | `modules/lazy_intel.py:342` | `def export_spans(task_id, out)` |
| `fuse_routing_decisions` | function | `modules/lazy_intel.py:303` | `def fuse_routing_decisions(task_id)` |
| `infer_source` | function | `modules/lazy_intel.py:88` | `def infer_source(command, intent_text)` |
| `mask_configured` | function | `modules/lazy_intel.py:237` | `def mask_configured(text)` |
| `read_decisions` | function | `modules/lazy_intel.py:211` | `def read_decisions(task_id, limit)` |
| `record_routing_decision` | function | `modules/lazy_intel.py:129` | `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` |
| `record_routing_outcome` | function | `modules/lazy_intel.py:169` | `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` |
| `stack_signature` | function | `modules/lazy_intel.py:272` | `def stack_signature(assets)` |
| `_LINUX_LINE` | function | `modules/lazy_inventory.py:87` | `def _LINUX_LINE(line)` |
| `_WINDOWS_LINE` | function | `modules/lazy_inventory.py:104` | `def _WINDOWS_LINE(line)` |
| `_clean_entry` | function | `modules/lazy_inventory.py:114` | `def _clean_entry(product, version, os_hint)` |
| `inventory_blob` | function | `modules/lazy_inventory.py:49` | `def inventory_blob(platform)` |
| `os_platform_of` | function | `modules/lazy_inventory.py:157` | `def os_platform_of(entries)` |
| `parse_blob_output` | function | `modules/lazy_inventory.py:61` | `def parse_blob_output(text, platform)` |
| `to_sightings` | function | `modules/lazy_inventory.py:133` | `def to_sightings(entries, host)` |
| `_addon_run_pair` | function | `modules/lazy_ledger.py:89` | `def _addon_run_pair(rest)` |
| `_load` | function | `modules/lazy_ledger.py:121` | `def _load(sessions_dir)` |
| `_path` | function | `modules/lazy_ledger.py:114` | `def _path(sessions_dir)` |
| `_sort_key` | function | `modules/lazy_ledger.py:209` | `def _sort_key(pair)` |
| `fresh` | function | `modules/lazy_ledger.py:140` | `def fresh(verb, target, now, sessions_dir)` |
| `json_load` | function | `modules/lazy_ledger.py:133` | `def json_load(path)` |
| `key_from_command` | function | `modules/lazy_ledger.py:58` | `def key_from_command(command, target)` |
| `ledger_key` | function | `modules/lazy_ledger.py:53` | `def ledger_key(verb, target)` |
| `record` | function | `modules/lazy_ledger.py:164` | `def record(verb, target, ok, now, sessions_dir)` |
| `stale_first` | function | `modules/lazy_ledger.py:191` | `def stale_first(catalog, now, sessions_dir)` |
| `window_for` | function | `modules/lazy_ledger.py:32` | `def window_for(verb)` |
| `ActivityLog` | class | `modules/lazy_loop.py:1579` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2331` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:1066` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:1041` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2425` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:6308` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:8343` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:7442` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:1032` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1229` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:1018` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:7123` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1551` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:1990` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:2577` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:8667` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:1055` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:7732` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:7563` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3288` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:6121` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2509` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:8269` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:8373` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:8535` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:8562` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:2779` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:8492` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:2737` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:8225` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:1712` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:4006` | `class Worker` |
| `__init__` | method | `modules/lazy_loop.py:1069` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1232` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1554` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1582` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1735` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1993` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2340` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2428` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2512` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2606` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2740` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2782` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3291` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:4009` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:6124` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:6316` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:7126` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:7445` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:7566` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7749` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8228` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8346` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8495` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8538` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:8692` | `def __init__(self, shell)` |
| `_absorb_reaction` | method | `modules/lazy_loop.py:4639` | `def _absorb_reaction(self, intent, command, output)` |
| `_agent_checkpoint` | method | `modules/lazy_loop.py:4986` | `def _agent_checkpoint(self, intent)` |
| `_agent_preflight` | method | `modules/lazy_loop.py:5012` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/lazy_loop.py:5357` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/lazy_loop.py:5175` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agentic_try` | method | `modules/lazy_loop.py:5389` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:6451` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:10533` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2275` | `def _asset_candidates(target)` |
| `_auto_approve` | method | `modules/lazy_loop.py:5498` | `def _auto_approve(self, command)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5840` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:9960` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:9996` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:6519` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:6333` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:7845` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:11234` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:3601` | `def _candidates(self)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:535` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:10451` | `def _check_goals(self, task_id, graph, activity)` |
| `_close_shell_session` | method | `modules/lazy_loop.py:5148` | `def _close_shell_session(self)` |
| `_cold_path` | method | `modules/lazy_loop.py:6321` | `def _cold_path(self)` |
| `_command_in_scope` | method | `modules/lazy_loop.py:5831` | `def _command_in_scope(self, command)` |
| `_constraints` | method | `modules/lazy_loop.py:3302` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:6511` | `def _content_versions(self)` |
| `_current_phase` | method | `modules/lazy_loop.py:3503` | `def _current_phase(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:589` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:3899` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:5730` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3311` | `def _denied(self, text)` |
| `_denied` | method | `modules/lazy_loop.py:5487` | `def _denied(self, command)` |
| `_draft_report` | method | `modules/lazy_loop.py:7270` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:7266` | `def _drafts_ready_path(self)` |
| `_drain_steer` | method | `modules/lazy_loop.py:5001` | `def _drain_steer(self, intent)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:9909` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:2601` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:631` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:551` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:10464` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:10051` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:2584` | `def _event_for(cls, path, item_id)` |
| `_fact_memory_store` | method | `modules/lazy_loop.py:4617` | `def _fact_memory_store(self)` |
| `_failure_memory` | method | `modules/lazy_loop.py:4545` | `def _failure_memory(self)` |
| `_find` | function | `modules/lazy_loop.py:6540` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:11130` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:4453` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:6479` | `def _foldable(self, node)` |
| `_goals_met` | method | `modules/lazy_loop.py:10458` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:6528` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:4691` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_has_creds` | method | `modules/lazy_loop.py:3589` | `def _has_creds()` |
| `_host_from_token` | function | `modules/lazy_loop.py:419` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:6113` | `def _host_like_target(target)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:9335` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_host_like_target` | function | `modules/lazy_loop.py:220` | `def _is_host_like_target(value)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:312` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:6475` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:6104` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:498` | `def _kill()` |
| `_lab_scope_default` | method | `modules/lazy_loop.py:4121` | `def _lab_scope_default(self, target)` |
| `_lazy_policy` | function | `modules/lazy_loop.py:3126` | `def _lazy_policy()` |
| `_learn_os` | method | `modules/lazy_loop.py:4590` | `def _learn_os(self, intent, command, output)` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:3480` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:3913` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:909` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:917` | `def _llm_quota_reply(text)` |
| `_llm_steps` | method | `modules/lazy_loop.py:5594` | `def _llm_steps(self, intent, prior_text)` |
| `_load` | method | `modules/lazy_loop.py:2612` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7450` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8232` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8350` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8499` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:6337` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:6325` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2347` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:869` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2351` | `def _load_task(self)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:7081` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2296` | `def _match_gate_rule(rule, target)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:10834` | `def _maybe_import_inbox(self)` |
| `_maybe_proxy_gc` | method | `modules/lazy_loop.py:10808` | `def _maybe_proxy_gc(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:10854` | `def _maybe_selfupdate_check(self)` |
| `_missing_tool` | method | `modules/lazy_loop.py:5510` | `def _missing_tool(self, command)` |
| `_noa_archive` | method | `modules/lazy_loop.py:6394` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:739` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:1927` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:781` | `def _now()` |
| `_open_shell_session` | method | `modules/lazy_loop.py:5077` | `def _open_shell_session(self, intent)` |
| `_origin_fact` | method | `modules/lazy_loop.py:3471` | `def _origin_fact(self)` |
| `_os_gate` | method | `modules/lazy_loop.py:4564` | `def _os_gate(self, intent, command)` |
| `_os_hint` | method | `modules/lazy_loop.py:3532` | `def _os_hint()` |
| `_parts` | method | `modules/lazy_loop.py:8902` | `def _parts(self, task_id)` |
| `_persist` | method | `modules/lazy_loop.py:1083` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1254` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2012` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2747` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2787` | `def _persist(self)` |
| `_policy_proposals` | function | `modules/lazy_loop.py:3148` | `def _policy_proposals(policy, target)` |
| `_prior_steps` | method | `modules/lazy_loop.py:4153` | `def _prior_steps(self, intent)` |
| `_publish_shell_proof` | method | `modules/lazy_loop.py:4937` | `def _publish_shell_proof(self, intent, target, command, output)` |
| `_reader` | function | `modules/lazy_loop.py:5099` | `def _reader()` |
| `_recall_facts` | method | `modules/lazy_loop.py:4632` | `def _recall_facts(self, query, k)` |
| `_record` | method | `modules/lazy_loop.py:7825` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:7925` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_raw` | method | `modules/lazy_loop.py:8180` | `def _record_raw(self, member, prompt, reply, ok, task_id, model_spec)` |
| `_refresh` | method | `modules/lazy_loop.py:2875` | `def _refresh(self)` |
| `_register_guardrails` | method | `modules/lazy_loop.py:8783` | `def _register_guardrails(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:476` | `def _register_loop_executor(executor)` |
| `_register_mediators` | method | `modules/lazy_loop.py:8772` | `def _register_mediators(self)` |
| `_remember_fact` | method | `modules/lazy_loop.py:4623` | `def _remember_fact(self, intent, command, output)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:7883` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:7325` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:6345` | `def _request_bodies(self, blocks, cold)` |
| `_resolved_command` | method | `modules/lazy_loop.py:5754` | `def _resolved_command(self, command)` |
| `_restrict_file` | function | `modules/lazy_loop.py:527` | `def _restrict_file(path)` |
| `_rl_rank` | method | `modules/lazy_loop.py:3825` | `def _rl_rank(self, out)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:7854` | `def _rotated_chain(self, chain)` |
| `_run` | method | `modules/lazy_loop.py:5526` | `def _run(self, command, executor)` |
| `_run_one` | function | `modules/lazy_loop.py:9754` | `def _run_one(index_node)` |
| `_run_round_guarded` | method | `modules/lazy_loop.py:8801` | `def _run_round_guarded(self, task_id, round_index, workers, executor)` |
| `_run_worker_guarded` | method | `modules/lazy_loop.py:8831` | `def _run_worker_guarded(self, worker, node, executor)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:5818` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:2616` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:6341` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:6329` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2358` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:879` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2362` | `def _save_task(self, payload)` |
| `_scope_allows_target` | method | `modules/lazy_loop.py:4092` | `def _scope_allows_target(self, target)` |
| `_scope_covers` | function | `modules/lazy_loop.py:2208` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2198` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:7760` | `def _seed_defaults(self)` |
| `_selector_candidates` | method | `modules/lazy_loop.py:3544` | `def _selector_candidates(self)` |
| `_send_email` | method | `modules/lazy_loop.py:7638` | `def _send_email(channel, line, event)` |
| `_send_shell` | method | `modules/lazy_loop.py:5112` | `def _send_shell(self, command, intent, timeout_sec)` |
| `_settle_partial` | method | `modules/lazy_loop.py:5689` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:3412` | `def _signature(text)` |
| `_slug` | function | `modules/lazy_loop.py:894` | `def _slug(value)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:9350` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:10255` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:3980` | `def _stall_intent(self, existing)` |
| `_start_background_job` | method | `modules/lazy_loop.py:5045` | `def _start_background_job(self, command, intent, transcripts)` |
| `_steps_for` | method | `modules/lazy_loop.py:5892` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:786` | `def _store_path(name)` |
| `_structured_verdict` | method | `modules/lazy_loop.py:6241` | `def _structured_verdict(self, finding)` |
| `_sudo_guard` | method | `modules/lazy_loop.py:5768` | `def _sudo_guard(self, intent, command)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:306` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:10672` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:9557` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2258` | `def _target_as_asset(value)` |
| `_target_for` | method | `modules/lazy_loop.py:4537` | `def _target_for(self, intent)` |
| `_target_services` | method | `modules/lazy_loop.py:3512` | `def _target_services(self, target)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:5795` | `def _task_executed_commands(self)` |
| `_technique_for` | method | `modules/lazy_loop.py:7134` | `def _technique_for(vulnclass, text)` |
| `_traffic_template` | function | `modules/lazy_loop.py:899` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:6546` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:482` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:326` | `def _valid_nmap_port_spec(value)` |
| `_wake_event` | function | `modules/lazy_loop.py:621` | `def _wake_event(task_id)` |
| `_with_llm_steps` | method | `modules/lazy_loop.py:5576` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `_work` | function | `modules/lazy_loop.py:5057` | `def _work()` |
| `_work` | function | `modules/lazy_loop.py:7304` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:6366` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:10016` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_draft` | method | `modules/lazy_loop.py:7341` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:5962` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:2549` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:2844` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2367` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:2751` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:7454` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:8354` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:8507` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:7578` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:2978` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1351` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:9120` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:9138` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:7789` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1266` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:2019` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:2997` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:10681` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:2913` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1364` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1379` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1375` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:7359` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:8727` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:1974` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:488` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:2774` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:8279` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:2113` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:2534` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:1896` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:8250` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:8768` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:8245` | `def bindings(self, agent)` |
| `broadcast` | method | `modules/lazy_loop.py:11159` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:9087` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:7002` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:1891` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:7570` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:2061` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2496` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1392` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1564` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:1980` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:8637` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:3033` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:4081` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:6796` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:6645` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1453` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:2758` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:7940` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` |
| `constraint_block` | function | `modules/lazy_loop.py:6877` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:8116` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1142` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1176` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:6592` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:2791` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:8907` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:2694` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:3228` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:1087` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:2835` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:9192` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:9226` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:10567` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:2864` | `def dequeue_next(self)` |
| `digest_of` | method | `modules/lazy_loop.py:1718` | `def digest_of(command, output)` |
| `digest_overview` | method | `modules/lazy_loop.py:6830` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:10700` | `def drain_queue(self, max_tasks)` |

Next: [SYMBOLS_p17.md](SYMBOLS_p17.md)
