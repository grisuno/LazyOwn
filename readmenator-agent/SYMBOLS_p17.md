# Symbols (page 17 of 54)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `record_path` | function | `modules/lazy_continuation.py:77` | `def record_path(target)` |
| `save` | function | `modules/lazy_continuation.py:89` | `def save(target, task_id, goal, status, settlement, findings, next_steps, credentials, deviations)` |
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
| `DeviationLedger` | class | `modules/lazy_deviations.py:72` | `class DeviationLedger` |
| `DeviationRecord` | class | `modules/lazy_deviations.py:35` | `class DeviationRecord` |
| `__init__` | method | `modules/lazy_deviations.py:80` | `def __init__(self, path)` |
| `_append` | method | `modules/lazy_deviations.py:201` | `def _append(self, record)` |
| `_clean` | function | `modules/lazy_deviations.py:67` | `def _clean(text)` |
| `_last_matches` | method | `modules/lazy_deviations.py:160` | `def _last_matches(self, scope, planned, actual, reason)` |
| `_read` | method | `modules/lazy_deviations.py:172` | `def _read(self)` |
| `_trim` | method | `modules/lazy_deviations.py:216` | `def _trim(self)` |
| `as_dict` | method | `modules/lazy_deviations.py:55` | `def as_dict(self)` |
| `list` | method | `modules/lazy_deviations.py:124` | `def list(self, scope, limit)` |
| `record` | method | `modules/lazy_deviations.py:84` | `def record(self, scope, planned, actual, reason, source)` |
| `render_markdown` | method | `modules/lazy_deviations.py:140` | `def render_markdown(self, records, title)` |
| `_drafts_dir` | function | `modules/lazy_drafts.py:27` | `def _drafts_dir()` |
| `drain` | function | `modules/lazy_drafts.py:34` | `def drain(engine)` |
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
| `AdaptiveFallbackArbiter` | class | `modules/lazy_fallback.py:185` | `class AdaptiveFallbackArbiter` |
| `Alternative` | class | `modules/lazy_fallback.py:29` | `class Alternative` |
| `TechniqueFallback` | class | `modules/lazy_fallback.py:47` | `class TechniqueFallback` |
| `__init__` | method | `modules/lazy_fallback.py:193` | `def __init__(self, graph)` |
| `_bind_family` | method | `modules/lazy_fallback.py:246` | `def _bind_family(self, command)` |
| `_service_satisfied` | function | `modules/lazy_fallback.py:172` | `def _service_satisfied(required, services)` |
| `catalogue_ids` | function | `modules/lazy_fallback.py:256` | `def catalogue_ids()` |
| `matches` | method | `modules/lazy_fallback.py:61` | `def matches(self, command)` |
| `suggest` | method | `modules/lazy_fallback.py:203` | `def suggest(self, command, verdict, services, has_credentials, catalogue)` |
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
| `FinalizerDecision` | class | `modules/lazy_finalizer.py:35` | `class FinalizerDecision` |
| `decide` | function | `modules/lazy_finalizer.py:72` | `def decide(status, candidate_verdict, facts, findings, confirmed, tested, pending_approvals, pending_plan_steps)` |
| `to_dict` | method | `modules/lazy_finalizer.py:58` | `def to_dict(self)` |
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
| `_append_run_separator` | function | `modules/lazy_handoff.py:211` | `def _append_run_separator(log_path, host, source, task_id)` |
| `_beacon_is_live` | function | `modules/lazy_handoff.py:128` | `def _beacon_is_live(target, sessions_dir)` |
| `_handoff_worker` | function | `modules/lazy_handoff.py:371` | `def _handoff_worker(target, source, log, sessions_dir, wait_s, rounds, task_id)` |
| `_log_skip_reason` | function | `modules/lazy_handoff.py:235` | `def _log_skip_reason(host, sessions_dir, log)` |
| `_main` | function | `modules/lazy_handoff.py:486` | `def _main()` |
| `_mark_status` | function | `modules/lazy_handoff.py:454` | `def _mark_status(target, sessions_dir, status, client_id)` |
| `_marker_path` | function | `modules/lazy_handoff.py:76` | `def _marker_path(target, sessions_dir)` |
| `_resolve_task_id` | function | `modules/lazy_handoff.py:90` | `def _resolve_task_id(task_id)` |
| `_seq` | function | `modules/lazy_handoff.py:118` | `def _seq(record)` |
| `activity` | function | `modules/lazy_handoff.py:400` | `def activity(kind, text)` |
| `already_handed_off` | function | `modules/lazy_handoff.py:167` | `def already_handed_off(target, sessions_dir)` |
| `handoff_enabled` | function | `modules/lazy_handoff.py:52` | `def handoff_enabled(payload)` |
| `maybe_beacon_handoff` | function | `modules/lazy_handoff.py:263` | `def maybe_beacon_handoff(target, source, log, sessions_dir, wait_s, rounds, task_id)` |
| `tlog` | function | `modules/lazy_handoff.py:392` | `def tlog(line)` |
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
| `ActivityLog` | class | `modules/lazy_loop.py:2089` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2950` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:1471` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:1446` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:3079` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:6837` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:8897` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:8011` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:1437` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1629` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:1423` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:7691` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:2061` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:2618` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:3240` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:9239` | `class LazyLoopEngine(EngineProxyMixin)` |
| `LazyTask` | class | `modules/lazy_loop.py:1460` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:8301` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:8132` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:4207` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:6547` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:3172` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:8823` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:8927` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:9089` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:9116` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:3442` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:9046` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:3400` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:8779` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:2211` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:5168` | `class Worker(WorkerLazymodeMixin, WorkerAgenticMixin, WorkerExecutionMixin, WorkerGatingMixin, WorkerMemoryMixin)` |
| `__init__` | method | `modules/lazy_loop.py:1474` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1632` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2064` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:2092` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2234` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2621` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2959` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3082` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3175` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3269` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3403` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3445` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:4210` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:5171` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:6550` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:6845` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:7694` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:8014` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:8135` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:8318` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8782` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8900` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:9049` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:9092` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:9264` | `def __init__(self, shell)` |
| `_absorb_campaign_lessons` | method | `modules/lazy_loop.py:10781` | `def _absorb_campaign_lessons(self)` |
| `_append_jsonl` | function | `modules/lazy_loop.py:1199` | `def _append_jsonl(path, rows)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:6980` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:11756` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2894` | `def _asset_candidates(target)` |
| `_audit_blocked` | method | `modules/lazy_loop.py:5950` | `def _audit_blocked(self, source, reason, command, intent)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:6186` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:10685` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_pwn_cover_all` | function | `modules/lazy_loop.py:194` | `def _auto_pwn_cover_all()` |
| `_auto_retest` | method | `modules/lazy_loop.py:10721` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:7048` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:6862` | `def _bodies_path(self)` |
| `_boundary_enabled` | function | `modules/lazy_loop.py:7613` | `def _boundary_enabled()` |
| `_breaker_active` | method | `modules/lazy_loop.py:8414` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:12309` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:4730` | `def _candidates(self)` |
| `_capture_wire` | method | `modules/lazy_loop.py:2291` | `def _capture_wire(self, digest, body)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:767` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:11465` | `def _check_goals(self, task_id, graph, activity)` |
| `_citation_verdict` | method | `modules/lazy_loop.py:6735` | `def _citation_verdict(self, finding)` |
| `_cold_path` | method | `modules/lazy_loop.py:6850` | `def _cold_path(self)` |
| `_commit` | method | `modules/lazy_loop.py:1703` | `def _commit(self, mutator)` |
| `_complete` | function | `modules/lazy_loop.py:9822` | `def _complete(prompt, max_tokens)` |
| `_constraints` | method | `modules/lazy_loop.py:4221` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:7040` | `def _content_versions(self)` |
| `_continuation_candidates` | method | `modules/lazy_loop.py:4606` | `def _continuation_candidates(self)` |
| `_current_phase` | method | `modules/lazy_loop.py:4478` | `def _current_phase(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:821` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:5063` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:6119` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:4230` | `def _denied(self, text)` |
| `_derive_finding_class` | function | `modules/lazy_loop.py:7666` | `def _derive_finding_class(blob)` |
| `_do` | function | `modules/lazy_loop.py:1755` | `def _do()` |
| `_do` | function | `modules/lazy_loop.py:1789` | `def _do()` |
| `_draft_report` | method | `modules/lazy_loop.py:7839` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:7835` | `def _drafts_ready_path(self)` |
| `_drain_drafts` | method | `modules/lazy_loop.py:10800` | `def _drain_drafts(self)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:10634` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:3264` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:863` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:783` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:11687` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_enrich_finding` | method | `modules/lazy_loop.py:2514` | `def _enrich_finding(self, finding_id, graph)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:10985` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:3247` | `def _event_for(cls, path, item_id)` |
| `_evidence_store` | method | `modules/lazy_loop.py:2240` | `def _evidence_store(self)` |
| `_exploit_target` | function | `modules/lazy_loop.py:6525` | `def _exploit_target(command, finding)` |
| `_fact_gate_candidates` | method | `modules/lazy_loop.py:4238` | `def _fact_gate_candidates(self, candidates)` |
| `_find` | function | `modules/lazy_loop.py:7069` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:12205` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:5578` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:7008` | `def _foldable(self, node)` |
| `_foothold_dependent_intent` | function | `modules/lazy_loop.py:3879` | `def _foothold_dependent_intent(text)` |
| `_foothold_evidence_id` | method | `modules/lazy_loop.py:11433` | `def _foothold_evidence_id(self, graph)` |
| `_foothold_proven` | method | `modules/lazy_loop.py:11524` | `def _foothold_proven(self, target, task_id)` |
| `_fresh_scan_path` | function | `modules/lazy_loop.py:1021` | `def _fresh_scan_path(target, max_age_sec)` |
| `_goals_met` | method | `modules/lazy_loop.py:11518` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:7057` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:5668` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_handover_credentials` | method | `modules/lazy_loop.py:10919` | `def _handover_credentials(settlement, findings)` |
| `_handover_deviations` | method | `modules/lazy_loop.py:10895` | `def _handover_deviations(task_id)` |
| `_has_creds` | method | `modules/lazy_loop.py:4682` | `def _has_creds()` |
| `_host_from_token` | function | `modules/lazy_loop.py:588` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:6482` | `def _host_like_target(target)` |
| `_initial_access_candidate` | method | `modules/lazy_loop.py:4694` | `def _initial_access_candidate(self, existing)` |
| `_initial_access_intent` | function | `modules/lazy_loop.py:3851` | `def _initial_access_intent(text)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:10042` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_exploit_command` | function | `modules/lazy_loop.py:6510` | `def _is_exploit_command(command)` |
| `_is_foothold` | function | `modules/lazy_loop.py:4016` | `def _is_foothold(text, meta)` |
| `_is_host_like_target` | function | `modules/lazy_loop.py:393` | `def _is_host_like_target(value)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:481` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:7004` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:6473` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:667` | `def _kill()` |
| `_lazy_policy` | function | `modules/lazy_loop.py:4045` | `def _lazy_policy()` |
| `_lease_store` | function | `modules/lazy_loop.py:1111` | `def _lease_store()` |
| `_ledger_confirmed_count` | function | `modules/lazy_loop.py:9212` | `def _ledger_confirmed_count(task_id)` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:4455` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:5077` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:1301` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:1309` | `def _llm_quota_reply(text)` |
| `_load` | method | `modules/lazy_loop.py:3275` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8019` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8786` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8904` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:9053` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:6866` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:6854` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2966` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:1255` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2970` | `def _load_task(self)` |
| `_loop_exploit_first` | function | `modules/lazy_loop.py:210` | `def _loop_exploit_first()` |
| `_loop_fact_gate` | function | `modules/lazy_loop.py:3890` | `def _loop_fact_gate()` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:7623` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2915` | `def _match_gate_rule(rule, target)` |
| `_maybe_blindspot` | method | `modules/lazy_loop.py:10593` | `def _maybe_blindspot(self, task_id, activity, stage_enabled, new_intents)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:11909` | `def _maybe_import_inbox(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:11929` | `def _maybe_selfupdate_check(self)` |
| `_merge_from_disk` | method | `modules/lazy_loop.py:1664` | `def _merge_from_disk(self, raw)` |
| `_noa_archive` | method | `modules/lazy_loop.py:6923` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:974` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:2555` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:1089` | `def _now()` |
| `_objective_candidates` | method | `modules/lazy_loop.py:4636` | `def _objective_candidates(self)` |
| `_origin_fact` | method | `modules/lazy_loop.py:4446` | `def _origin_fact(self)` |
| `_os_hint` | method | `modules/lazy_loop.py:4507` | `def _os_hint()` |
| `_parts` | method | `modules/lazy_loop.py:9543` | `def _parts(self, task_id)` |
| `_payload_scope_items` | function | `modules/lazy_loop.py:3731` | `def _payload_scope_items()` |
| `_persist` | method | `modules/lazy_loop.py:1488` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1735` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2640` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3410` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3450` | `def _persist(self)` |
| `_policy_proposals` | function | `modules/lazy_loop.py:4067` | `def _policy_proposals(policy, target)` |
| `_pre_round_gate` | method | `modules/lazy_loop.py:10285` | `def _pre_round_gate(self, task_id)` |
| `_preserve_evidence` | method | `modules/lazy_loop.py:2532` | `def _preserve_evidence(self, digest)` |
| `_prior_steps` | method | `modules/lazy_loop.py:5255` | `def _prior_steps(self, intent)` |
| `_publish_fallback_shell` | method | `modules/lazy_loop.py:11634` | `def _publish_fallback_shell(self, task_id, target, command, output, activity, reused)` |
| `_publish_shell_proof` | method | `modules/lazy_loop.py:6006` | `def _publish_shell_proof(self, intent, target, command, output)` |
| `_read_jsonl` | function | `modules/lazy_loop.py:1225` | `def _read_jsonl(path, limit)` |
| `_record` | method | `modules/lazy_loop.py:8394` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:8491` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_deviation` | function | `modules/lazy_loop.py:64` | `def _record_deviation(scope, planned, actual, reason, source)` |
| `_record_raw` | method | `modules/lazy_loop.py:8738` | `def _record_raw(self, member, prompt, reply, ok, task_id, model_spec)` |
| `_record_selector_decision` | method | `modules/lazy_loop.py:4564` | `def _record_selector_decision(self, ctx, decision, command)` |
| `_refresh` | method | `modules/lazy_loop.py:3554` | `def _refresh(self)` |
| `_register_guardrails` | method | `modules/lazy_loop.py:9424` | `def _register_guardrails(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:645` | `def _register_loop_executor(executor)` |
| `_register_mediators` | method | `modules/lazy_loop.py:9413` | `def _register_mediators(self)` |
| `_release_lease` | method | `modules/lazy_loop.py:1983` | `def _release_lease(self, node_id)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:8452` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:7894` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:6874` | `def _request_bodies(self, blocks, cold)` |
| `_restrict_file` | function | `modules/lazy_loop.py:759` | `def _restrict_file(path)` |
| `_rl_rank` | method | `modules/lazy_loop.py:4990` | `def _rl_rank(self, out)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:8423` | `def _rotated_chain(self, chain)` |
| `_run_chained` | method | `modules/lazy_loop.py:5974` | `def _run_chained(self, intent, command, executor, budget, intercept, retry_state)` |
| `_run_one` | function | `modules/lazy_loop.py:10412` | `def _run_one(index_node)` |
| `_run_round_guarded` | method | `modules/lazy_loop.py:9442` | `def _run_round_guarded(self, task_id, round_index, workers, executor)` |
| `_run_worker_guarded` | method | `modules/lazy_loop.py:9472` | `def _run_worker_guarded(self, worker, node, executor)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:6166` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:3279` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:6870` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:6858` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2977` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:1270` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2981` | `def _save_task(self, payload)` |
| `_save_tokens_mode` | method | `modules/lazy_loop.py:10245` | `def _save_tokens_mode(self, task_id)` |
| `_scan_aggressive` | function | `modules/lazy_loop.py:1003` | `def _scan_aggressive()` |
| `_scan_reuse_sec` | function | `modules/lazy_loop.py:984` | `def _scan_reuse_sec()` |
| `_scope_covers` | function | `modules/lazy_loop.py:2827` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2817` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:8329` | `def _seed_defaults(self)` |
| `_selector_candidates` | method | `modules/lazy_loop.py:4519` | `def _selector_candidates(self)` |
| `_send_email` | method | `modules/lazy_loop.py:8207` | `def _send_email(channel, line, event)` |
| `_session_verdict` | method | `modules/lazy_loop.py:6671` | `def _session_verdict(self, finding, command)` |
| `_settle_objectives` | method | `modules/lazy_loop.py:10818` | `def _settle_objectives(self, task_id)` |
| `_settle_partial` | method | `modules/lazy_loop.py:6078` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:4387` | `def _signature(text)` |
| `_sleeper_round` | method | `modules/lazy_loop.py:9384` | `def _sleeper_round(self, activity)` |
| `_slug` | function | `modules/lazy_loop.py:1286` | `def _slug(value)` |
| `_snapshot` | method | `modules/lazy_loop.py:1655` | `def _snapshot(self)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:10057` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:11233` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:5142` | `def _stall_intent(self, existing)` |
| `_steps_for` | method | `modules/lazy_loop.py:6238` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:1094` | `def _store_path(name)` |
| `_structured_verdict` | method | `modules/lazy_loop.py:6770` | `def _structured_verdict(self, finding)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:475` | `def _sudo_unavailable(output)` |
| `_sweep_leases` | method | `modules/lazy_loop.py:10253` | `def _sweep_leases(self, task_id)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:11836` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:10168` | `def _sync_intel(self, task_id, activity, force)` |
| `_sync_lease` | method | `modules/lazy_loop.py:1818` | `def _sync_lease(self, node, state)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2877` | `def _target_as_asset(value)` |
| `_target_foothold_proven` | function | `modules/lazy_loop.py:3986` | `def _target_foothold_proven(target, task_id)` |
| `_target_for` | method | `modules/lazy_loop.py:5660` | `def _target_for(self, intent)` |
| `_target_services` | method | `modules/lazy_loop.py:4487` | `def _target_services(self, target)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:6143` | `def _task_executed_commands(self)` |
| `_technique_deterministic_enabled` | function | `modules/lazy_loop.py:3951` | `def _technique_deterministic_enabled()` |
| `_technique_for` | method | `modules/lazy_loop.py:7702` | `def _technique_for(vulnclass, text)` |
| `_technique_intent` | function | `modules/lazy_loop.py:3909` | `def _technique_intent(text)` |
| `_technique_steps` | function | `modules/lazy_loop.py:3931` | `def _technique_steps(text)` |
| `_terminal_autopwn_fallback` | method | `modules/lazy_loop.py:11541` | `def _terminal_autopwn_fallback(self, task_id, executor, activity)` |
| `_traffic_template` | function | `modules/lazy_loop.py:1291` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:7075` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:651` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:495` | `def _valid_nmap_port_spec(value)` |
| `_veto_blocked_from_audit` | method | `modules/lazy_loop.py:10741` | `def _veto_blocked_from_audit(self, task_id)` |
| `_wake_event` | function | `modules/lazy_loop.py:853` | `def _wake_event(task_id)` |
| `_wire_store` | method | `modules/lazy_loop.py:2277` | `def _wire_store(self)` |
| `_work` | function | `modules/lazy_loop.py:7873` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:6895` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:10950` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_continuation` | method | `modules/lazy_loop.py:10849` | `def _write_continuation(self, task_id, status)` |
| `_write_draft` | method | `modules/lazy_loop.py:7910` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:6324` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:3212` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:3507` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2986` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:3414` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:8023` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:8908` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:9061` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:8147` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:3657` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1830` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:9771` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:9849` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:8358` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1739` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:2647` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:3676` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:11845` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:3592` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1843` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1858` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1854` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:7928` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:9325` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:2602` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:657` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:3437` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:8833` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:2741` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:3197` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:2482` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:8804` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:9409` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:8799` | `def bindings(self, agent)` |
| `blindspot_review` | method | `modules/lazy_loop.py:9789` | `def blindspot_review(self, task_id)` |
| `broadcast` | method | `modules/lazy_loop.py:12234` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:9738` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:7531` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:2477` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:8139` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:2690` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:3156` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1871` | `def children(self, node_id, kind)` |
| `citation_service_bound` | function | `modules/lazy_loop.py:3065` | `def citation_service_bound()` |
| `claim_next` | method | `modules/lazy_loop.py:2074` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:2608` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:9182` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:3712` | `def clear_steer(self, task_id, intent_id)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
