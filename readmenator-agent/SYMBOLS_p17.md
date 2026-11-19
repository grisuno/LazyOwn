# Symbols (page 17 of 54)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `_beacon_is_live` | function | `modules/lazy_handoff.py:90` | `def _beacon_is_live(target, sessions_dir)` |
| `_handoff_worker` | function | `modules/lazy_handoff.py:260` | `def _handoff_worker(target, source, log, sessions_dir, wait_s, rounds, task_id)` |
| `_main` | function | `modules/lazy_handoff.py:365` | `def _main()` |
| `_mark_status` | function | `modules/lazy_handoff.py:333` | `def _mark_status(target, sessions_dir, status, client_id)` |
| `_marker_path` | function | `modules/lazy_handoff.py:76` | `def _marker_path(target, sessions_dir)` |
| `activity` | function | `modules/lazy_handoff.py:281` | `def activity(kind, text)` |
| `already_handed_off` | function | `modules/lazy_handoff.py:120` | `def already_handed_off(target, sessions_dir)` |
| `handoff_enabled` | function | `modules/lazy_handoff.py:52` | `def handoff_enabled(payload)` |
| `maybe_beacon_handoff` | function | `modules/lazy_handoff.py:164` | `def maybe_beacon_handoff(target, source, log, sessions_dir, wait_s, rounds, task_id)` |
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
| `ActivityLog` | class | `modules/lazy_loop.py:1990` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2851` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:1417` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:1392` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2945` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:6400` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:8421` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:7535` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:1383` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1575` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:1369` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:7216` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1962` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:2519` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:3097` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:8763` | `class LazyLoopEngine(EngineProxyMixin)` |
| `LazyTask` | class | `modules/lazy_loop.py:1406` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:7825` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:7656` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:4025` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:6213` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:3029` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:8347` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:8451` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:8613` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:8640` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:3299` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:8570` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:3257` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:8303` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:2112` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:4923` | `class Worker(WorkerLazymodeMixin, WorkerAgenticMixin, WorkerExecutionMixin, WorkerGatingMixin, WorkerMemoryMixin)` |
| `__init__` | method | `modules/lazy_loop.py:1420` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1578` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1965` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1993` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2135` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2522` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2860` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2948` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3032` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3126` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3260` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3302` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:4028` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:4926` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:6216` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:6408` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:7219` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:7538` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:7659` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7842` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8306` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8424` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8573` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8616` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:8788` | `def __init__(self, shell)` |
| `_absorb_campaign_lessons` | method | `modules/lazy_loop.py:10265` | `def _absorb_campaign_lessons(self)` |
| `_append_jsonl` | function | `modules/lazy_loop.py:1147` | `def _append_jsonl(path, rows)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:6543` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:11151` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2795` | `def _asset_candidates(target)` |
| `_audit_blocked` | method | `modules/lazy_loop.py:5688` | `def _audit_blocked(self, source, reason, command, intent)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5907` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:10169` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_pwn_cover_all` | function | `modules/lazy_loop.py:189` | `def _auto_pwn_cover_all()` |
| `_auto_retest` | method | `modules/lazy_loop.py:10205` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:6611` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:6425` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:7938` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:11704` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:4495` | `def _candidates(self)` |
| `_capture_wire` | method | `modules/lazy_loop.py:2192` | `def _capture_wire(self, digest, body)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:740` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:10933` | `def _check_goals(self, task_id, graph, activity)` |
| `_cold_path` | method | `modules/lazy_loop.py:6413` | `def _cold_path(self)` |
| `_commit` | method | `modules/lazy_loop.py:1648` | `def _commit(self, mutator)` |
| `_complete` | function | `modules/lazy_loop.py:9346` | `def _complete(prompt, max_tokens)` |
| `_constraints` | method | `modules/lazy_loop.py:4039` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:6603` | `def _content_versions(self)` |
| `_continuation_candidates` | method | `modules/lazy_loop.py:4371` | `def _continuation_candidates(self)` |
| `_current_phase` | method | `modules/lazy_loop.py:4243` | `def _current_phase(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:794` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4818` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:5840` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:4048` | `def _denied(self, text)` |
| `_do` | function | `modules/lazy_loop.py:1700` | `def _do()` |
| `_do` | function | `modules/lazy_loop.py:1734` | `def _do()` |
| `_draft_report` | method | `modules/lazy_loop.py:7363` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:7359` | `def _drafts_ready_path(self)` |
| `_drain_drafts` | method | `modules/lazy_loop.py:10284` | `def _drain_drafts(self)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:10118` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:3121` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:836` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:756` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:11082` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_enrich_finding` | method | `modules/lazy_loop.py:2415` | `def _enrich_finding(self, finding_id, graph)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:10469` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:3104` | `def _event_for(cls, path, item_id)` |
| `_evidence_store` | method | `modules/lazy_loop.py:2141` | `def _evidence_store(self)` |
| `_find` | function | `modules/lazy_loop.py:6632` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:11600` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:5324` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:6571` | `def _foldable(self, node)` |
| `_foothold_evidence_id` | method | `modules/lazy_loop.py:10901` | `def _foothold_evidence_id(self, graph)` |
| `_foothold_proven` | method | `modules/lazy_loop.py:10992` | `def _foothold_proven(self, target, task_id)` |
| `_fresh_scan_path` | function | `modules/lazy_loop.py:994` | `def _fresh_scan_path(target, max_age_sec)` |
| `_goals_met` | method | `modules/lazy_loop.py:10986` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:6620` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:5414` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_handover_credentials` | method | `modules/lazy_loop.py:10403` | `def _handover_credentials(settlement, findings)` |
| `_handover_deviations` | method | `modules/lazy_loop.py:10379` | `def _handover_deviations(task_id)` |
| `_has_creds` | method | `modules/lazy_loop.py:4447` | `def _has_creds()` |
| `_host_from_token` | function | `modules/lazy_loop.py:561` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:6199` | `def _host_like_target(target)` |
| `_initial_access_candidate` | method | `modules/lazy_loop.py:4459` | `def _initial_access_candidate(self, existing)` |
| `_initial_access_intent` | function | `modules/lazy_loop.py:3708` | `def _initial_access_intent(text)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:9566` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_foothold` | function | `modules/lazy_loop.py:3834` | `def _is_foothold(text, meta)` |
| `_is_host_like_target` | function | `modules/lazy_loop.py:366` | `def _is_host_like_target(value)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:454` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:6567` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:6190` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:640` | `def _kill()` |
| `_lazy_policy` | function | `modules/lazy_loop.py:3863` | `def _lazy_policy()` |
| `_ledger_confirmed_count` | function | `modules/lazy_loop.py:8736` | `def _ledger_confirmed_count(task_id)` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:4220` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:4832` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:1249` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:1257` | `def _llm_quota_reply(text)` |
| `_load` | method | `modules/lazy_loop.py:3132` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7543` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8310` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8428` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8577` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:6429` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:6417` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2867` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:1203` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2871` | `def _load_task(self)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:7173` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2816` | `def _match_gate_rule(rule, target)` |
| `_maybe_blindspot` | method | `modules/lazy_loop.py:10077` | `def _maybe_blindspot(self, task_id, activity, stage_enabled, new_intents)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:11304` | `def _maybe_import_inbox(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:11324` | `def _maybe_selfupdate_check(self)` |
| `_merge_from_disk` | method | `modules/lazy_loop.py:1609` | `def _merge_from_disk(self, raw)` |
| `_noa_archive` | method | `modules/lazy_loop.py:6486` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:947` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:2456` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:1062` | `def _now()` |
| `_objective_candidates` | method | `modules/lazy_loop.py:4401` | `def _objective_candidates(self)` |
| `_origin_fact` | method | `modules/lazy_loop.py:4211` | `def _origin_fact(self)` |
| `_os_hint` | method | `modules/lazy_loop.py:4272` | `def _os_hint()` |
| `_parts` | method | `modules/lazy_loop.py:9067` | `def _parts(self, task_id)` |
| `_payload_scope_items` | function | `modules/lazy_loop.py:3588` | `def _payload_scope_items()` |
| `_persist` | method | `modules/lazy_loop.py:1434` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1680` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2541` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3267` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3307` | `def _persist(self)` |
| `_policy_proposals` | function | `modules/lazy_loop.py:3885` | `def _policy_proposals(policy, target)` |
| `_pre_round_gate` | method | `modules/lazy_loop.py:9769` | `def _pre_round_gate(self, task_id)` |
| `_preserve_evidence` | method | `modules/lazy_loop.py:2433` | `def _preserve_evidence(self, digest)` |
| `_prior_steps` | method | `modules/lazy_loop.py:5010` | `def _prior_steps(self, intent)` |
| `_publish_shell_proof` | method | `modules/lazy_loop.py:5744` | `def _publish_shell_proof(self, intent, target, command, output)` |
| `_read_jsonl` | function | `modules/lazy_loop.py:1173` | `def _read_jsonl(path, limit)` |
| `_record` | method | `modules/lazy_loop.py:7918` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:8015` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_deviation` | function | `modules/lazy_loop.py:60` | `def _record_deviation(scope, planned, actual, reason, source)` |
| `_record_raw` | method | `modules/lazy_loop.py:8262` | `def _record_raw(self, member, prompt, reply, ok, task_id, model_spec)` |
| `_record_selector_decision` | method | `modules/lazy_loop.py:4329` | `def _record_selector_decision(self, ctx, decision, command)` |
| `_refresh` | method | `modules/lazy_loop.py:3411` | `def _refresh(self)` |
| `_register_guardrails` | method | `modules/lazy_loop.py:8948` | `def _register_guardrails(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:618` | `def _register_loop_executor(executor)` |
| `_register_mediators` | method | `modules/lazy_loop.py:8937` | `def _register_mediators(self)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:7976` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:7418` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:6437` | `def _request_bodies(self, blocks, cold)` |
| `_restrict_file` | function | `modules/lazy_loop.py:732` | `def _restrict_file(path)` |
| `_rl_rank` | method | `modules/lazy_loop.py:4745` | `def _rl_rank(self, out)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:7947` | `def _rotated_chain(self, chain)` |
| `_run_chained` | method | `modules/lazy_loop.py:5712` | `def _run_chained(self, intent, command, executor, budget, intercept, retry_state)` |
| `_run_one` | function | `modules/lazy_loop.py:9896` | `def _run_one(index_node)` |
| `_run_round_guarded` | method | `modules/lazy_loop.py:8966` | `def _run_round_guarded(self, task_id, round_index, workers, executor)` |
| `_run_worker_guarded` | method | `modules/lazy_loop.py:8996` | `def _run_worker_guarded(self, worker, node, executor)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:5887` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:3136` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:6433` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:6421` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2878` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:1218` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2882` | `def _save_task(self, payload)` |
| `_scan_aggressive` | function | `modules/lazy_loop.py:976` | `def _scan_aggressive()` |
| `_scan_reuse_sec` | function | `modules/lazy_loop.py:957` | `def _scan_reuse_sec()` |
| `_scope_covers` | function | `modules/lazy_loop.py:2728` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2718` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:7853` | `def _seed_defaults(self)` |
| `_selector_candidates` | method | `modules/lazy_loop.py:4284` | `def _selector_candidates(self)` |
| `_send_email` | method | `modules/lazy_loop.py:7731` | `def _send_email(channel, line, event)` |
| `_settle_objectives` | method | `modules/lazy_loop.py:10302` | `def _settle_objectives(self, task_id)` |
| `_settle_partial` | method | `modules/lazy_loop.py:5799` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:4152` | `def _signature(text)` |
| `_sleeper_round` | method | `modules/lazy_loop.py:8908` | `def _sleeper_round(self, activity)` |
| `_slug` | function | `modules/lazy_loop.py:1234` | `def _slug(value)` |
| `_snapshot` | method | `modules/lazy_loop.py:1600` | `def _snapshot(self)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:9581` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:10701` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:4897` | `def _stall_intent(self, existing)` |
| `_steps_for` | method | `modules/lazy_loop.py:5959` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:1067` | `def _store_path(name)` |
| `_structured_verdict` | method | `modules/lazy_loop.py:6333` | `def _structured_verdict(self, finding)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:448` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:11231` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:9692` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2778` | `def _target_as_asset(value)` |
| `_target_foothold_proven` | function | `modules/lazy_loop.py:3804` | `def _target_foothold_proven(target, task_id)` |
| `_target_for` | method | `modules/lazy_loop.py:5406` | `def _target_for(self, intent)` |
| `_target_services` | method | `modules/lazy_loop.py:4252` | `def _target_services(self, target)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:5864` | `def _task_executed_commands(self)` |
| `_technique_deterministic_enabled` | function | `modules/lazy_loop.py:3769` | `def _technique_deterministic_enabled()` |
| `_technique_for` | method | `modules/lazy_loop.py:7227` | `def _technique_for(vulnclass, text)` |
| `_technique_intent` | function | `modules/lazy_loop.py:3727` | `def _technique_intent(text)` |
| `_technique_steps` | function | `modules/lazy_loop.py:3749` | `def _technique_steps(text)` |
| `_terminal_autopwn_fallback` | method | `modules/lazy_loop.py:11009` | `def _terminal_autopwn_fallback(self, task_id, executor, activity)` |
| `_traffic_template` | function | `modules/lazy_loop.py:1239` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:6638` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:624` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:468` | `def _valid_nmap_port_spec(value)` |
| `_veto_blocked_from_audit` | method | `modules/lazy_loop.py:10225` | `def _veto_blocked_from_audit(self, task_id)` |
| `_wake_event` | function | `modules/lazy_loop.py:826` | `def _wake_event(task_id)` |
| `_wire_store` | method | `modules/lazy_loop.py:2178` | `def _wire_store(self)` |
| `_work` | function | `modules/lazy_loop.py:7397` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:6458` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:10434` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_continuation` | method | `modules/lazy_loop.py:10333` | `def _write_continuation(self, task_id, status)` |
| `_write_draft` | method | `modules/lazy_loop.py:7434` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:6045` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:3069` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:3364` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2887` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:3271` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:7547` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:8432` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:8585` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:7671` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:3514` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1762` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:9295` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:9373` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:7882` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1684` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:2548` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:3533` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:11240` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:3449` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1775` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1790` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1786` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:7452` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:8849` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:2503` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:630` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:3294` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:8357` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:2642` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:3054` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:2383` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:8328` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:8933` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:8323` | `def bindings(self, agent)` |
| `blindspot_review` | method | `modules/lazy_loop.py:9313` | `def blindspot_review(self, task_id)` |
| `broadcast` | method | `modules/lazy_loop.py:11629` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:9262` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:7094` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:2378` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:7663` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:2591` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:3016` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1803` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1975` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:2509` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:8706` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:3569` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:4999` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:6888` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:6737` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1864` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:3278` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:8029` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta, temperature)` |
| `constraint_block` | function | `modules/lazy_loop.py:6969` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:8216` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1493` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1522` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:6684` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:3311` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:9072` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:3214` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:3965` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:1438` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:3355` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:9427` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:9461` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:11185` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:3384` | `def dequeue_next(self, order)` |
| `digest_of` | method | `modules/lazy_loop.py:2118` | `def digest_of(command, output)` |
| `digest_overview` | method | `modules/lazy_loop.py:6922` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:11259` | `def drain_queue(self, max_tasks, deadline_near)` |
| `edit_goal` | method | `modules/lazy_loop.py:9415` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1998` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:7769` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:3373` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:4002` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:9017` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2930` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:2473` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:5034` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:6864` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:3508` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:2496` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:7648` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:11373` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:11432` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:11344` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:3654` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:3622` | `def extract_scope_items(goal_text, description)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
