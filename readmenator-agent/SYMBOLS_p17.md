# Symbols (page 17 of 54)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `ActivityLog` | class | `modules/lazy_loop.py:1989` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2850` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:1416` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:1391` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2944` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:6325` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:8346` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:7460` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:1382` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1574` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:1368` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:7141` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1961` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:2518` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:3096` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:8688` | `class LazyLoopEngine(EngineProxyMixin)` |
| `LazyTask` | class | `modules/lazy_loop.py:1405` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:7750` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:7581` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3956` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:6138` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:3028` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:8272` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:8376` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:8538` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:8565` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:3298` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:8495` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:3256` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:8228` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:2111` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:4854` | `class Worker(WorkerAgenticMixin, WorkerExecutionMixin, WorkerGatingMixin, WorkerMemoryMixin)` |
| `__init__` | method | `modules/lazy_loop.py:1419` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1577` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1964` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1992` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2134` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2521` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2859` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2947` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3031` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3125` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3259` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3301` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3959` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:4857` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:6141` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:6333` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:7144` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:7463` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:7584` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7767` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8231` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8349` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8498` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8541` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:8713` | `def __init__(self, shell)` |
| `_absorb_campaign_lessons` | method | `modules/lazy_loop.py:10190` | `def _absorb_campaign_lessons(self)` |
| `_append_jsonl` | function | `modules/lazy_loop.py:1146` | `def _append_jsonl(path, rows)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:6468` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:11076` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2794` | `def _asset_candidates(target)` |
| `_audit_blocked` | method | `modules/lazy_loop.py:5617` | `def _audit_blocked(self, source, reason, command, intent)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5836` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:10094` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_pwn_cover_all` | function | `modules/lazy_loop.py:188` | `def _auto_pwn_cover_all()` |
| `_auto_retest` | method | `modules/lazy_loop.py:10130` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:6536` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:6350` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:7863` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:11629` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:4426` | `def _candidates(self)` |
| `_capture_wire` | method | `modules/lazy_loop.py:2191` | `def _capture_wire(self, digest, body)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:739` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:10858` | `def _check_goals(self, task_id, graph, activity)` |
| `_cold_path` | method | `modules/lazy_loop.py:6338` | `def _cold_path(self)` |
| `_commit` | method | `modules/lazy_loop.py:1647` | `def _commit(self, mutator)` |
| `_complete` | function | `modules/lazy_loop.py:9271` | `def _complete(prompt, max_tokens)` |
| `_constraints` | method | `modules/lazy_loop.py:3970` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:6528` | `def _content_versions(self)` |
| `_continuation_candidates` | method | `modules/lazy_loop.py:4302` | `def _continuation_candidates(self)` |
| `_current_phase` | method | `modules/lazy_loop.py:4174` | `def _current_phase(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:793` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4749` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:5769` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3979` | `def _denied(self, text)` |
| `_do` | function | `modules/lazy_loop.py:1699` | `def _do()` |
| `_do` | function | `modules/lazy_loop.py:1733` | `def _do()` |
| `_draft_report` | method | `modules/lazy_loop.py:7288` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:7284` | `def _drafts_ready_path(self)` |
| `_drain_drafts` | method | `modules/lazy_loop.py:10209` | `def _drain_drafts(self)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:10043` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:3120` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:835` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:755` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:11007` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_enrich_finding` | method | `modules/lazy_loop.py:2414` | `def _enrich_finding(self, finding_id, graph)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:10394` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:3103` | `def _event_for(cls, path, item_id)` |
| `_evidence_store` | method | `modules/lazy_loop.py:2140` | `def _evidence_store(self)` |
| `_find` | function | `modules/lazy_loop.py:6557` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:11525` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:5253` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:6496` | `def _foldable(self, node)` |
| `_foothold_evidence_id` | method | `modules/lazy_loop.py:10826` | `def _foothold_evidence_id(self, graph)` |
| `_foothold_proven` | method | `modules/lazy_loop.py:10917` | `def _foothold_proven(self, target, task_id)` |
| `_fresh_scan_path` | function | `modules/lazy_loop.py:993` | `def _fresh_scan_path(target, max_age_sec)` |
| `_goals_met` | method | `modules/lazy_loop.py:10911` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:6545` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:5343` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_handover_credentials` | method | `modules/lazy_loop.py:10328` | `def _handover_credentials(settlement, findings)` |
| `_handover_deviations` | method | `modules/lazy_loop.py:10304` | `def _handover_deviations(task_id)` |
| `_has_creds` | method | `modules/lazy_loop.py:4378` | `def _has_creds()` |
| `_host_from_token` | function | `modules/lazy_loop.py:560` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:6124` | `def _host_like_target(target)` |
| `_initial_access_candidate` | method | `modules/lazy_loop.py:4390` | `def _initial_access_candidate(self, existing)` |
| `_initial_access_intent` | function | `modules/lazy_loop.py:3707` | `def _initial_access_intent(text)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:9491` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_foothold` | function | `modules/lazy_loop.py:3765` | `def _is_foothold(text, meta)` |
| `_is_host_like_target` | function | `modules/lazy_loop.py:365` | `def _is_host_like_target(value)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:453` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:6492` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:6115` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:639` | `def _kill()` |
| `_lazy_policy` | function | `modules/lazy_loop.py:3794` | `def _lazy_policy()` |
| `_ledger_confirmed_count` | function | `modules/lazy_loop.py:8661` | `def _ledger_confirmed_count(task_id)` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:4151` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:4763` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:1248` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:1256` | `def _llm_quota_reply(text)` |
| `_load` | method | `modules/lazy_loop.py:3131` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7468` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8235` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8353` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8502` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:6354` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:6342` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2866` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:1202` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2870` | `def _load_task(self)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:7098` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2815` | `def _match_gate_rule(rule, target)` |
| `_maybe_blindspot` | method | `modules/lazy_loop.py:10002` | `def _maybe_blindspot(self, task_id, activity, stage_enabled, new_intents)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:11229` | `def _maybe_import_inbox(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:11249` | `def _maybe_selfupdate_check(self)` |
| `_merge_from_disk` | method | `modules/lazy_loop.py:1608` | `def _merge_from_disk(self, raw)` |
| `_noa_archive` | method | `modules/lazy_loop.py:6411` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:946` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:2455` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:1061` | `def _now()` |
| `_objective_candidates` | method | `modules/lazy_loop.py:4332` | `def _objective_candidates(self)` |
| `_origin_fact` | method | `modules/lazy_loop.py:4142` | `def _origin_fact(self)` |
| `_os_hint` | method | `modules/lazy_loop.py:4203` | `def _os_hint()` |
| `_parts` | method | `modules/lazy_loop.py:8992` | `def _parts(self, task_id)` |
| `_payload_scope_items` | function | `modules/lazy_loop.py:3587` | `def _payload_scope_items()` |
| `_persist` | method | `modules/lazy_loop.py:1433` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1679` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2540` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3266` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3306` | `def _persist(self)` |
| `_policy_proposals` | function | `modules/lazy_loop.py:3816` | `def _policy_proposals(policy, target)` |
| `_pre_round_gate` | method | `modules/lazy_loop.py:9694` | `def _pre_round_gate(self, task_id)` |
| `_preserve_evidence` | method | `modules/lazy_loop.py:2432` | `def _preserve_evidence(self, digest)` |
| `_prior_steps` | method | `modules/lazy_loop.py:4941` | `def _prior_steps(self, intent)` |
| `_publish_shell_proof` | method | `modules/lazy_loop.py:5673` | `def _publish_shell_proof(self, intent, target, command, output)` |
| `_read_jsonl` | function | `modules/lazy_loop.py:1172` | `def _read_jsonl(path, limit)` |
| `_record` | method | `modules/lazy_loop.py:7843` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:7940` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_deviation` | function | `modules/lazy_loop.py:59` | `def _record_deviation(scope, planned, actual, reason, source)` |
| `_record_raw` | method | `modules/lazy_loop.py:8187` | `def _record_raw(self, member, prompt, reply, ok, task_id, model_spec)` |
| `_record_selector_decision` | method | `modules/lazy_loop.py:4260` | `def _record_selector_decision(self, ctx, decision, command)` |
| `_refresh` | method | `modules/lazy_loop.py:3410` | `def _refresh(self)` |
| `_register_guardrails` | method | `modules/lazy_loop.py:8873` | `def _register_guardrails(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:617` | `def _register_loop_executor(executor)` |
| `_register_mediators` | method | `modules/lazy_loop.py:8862` | `def _register_mediators(self)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:7901` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:7343` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:6362` | `def _request_bodies(self, blocks, cold)` |
| `_restrict_file` | function | `modules/lazy_loop.py:731` | `def _restrict_file(path)` |
| `_rl_rank` | method | `modules/lazy_loop.py:4676` | `def _rl_rank(self, out)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:7872` | `def _rotated_chain(self, chain)` |
| `_run_chained` | method | `modules/lazy_loop.py:5641` | `def _run_chained(self, intent, command, executor, budget, intercept, retry_state)` |
| `_run_one` | function | `modules/lazy_loop.py:9821` | `def _run_one(index_node)` |
| `_run_round_guarded` | method | `modules/lazy_loop.py:8891` | `def _run_round_guarded(self, task_id, round_index, workers, executor)` |
| `_run_worker_guarded` | method | `modules/lazy_loop.py:8921` | `def _run_worker_guarded(self, worker, node, executor)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:5816` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:3135` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:6358` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:6346` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2877` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:1217` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2881` | `def _save_task(self, payload)` |
| `_scan_aggressive` | function | `modules/lazy_loop.py:975` | `def _scan_aggressive()` |
| `_scan_reuse_sec` | function | `modules/lazy_loop.py:956` | `def _scan_reuse_sec()` |
| `_scope_covers` | function | `modules/lazy_loop.py:2727` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2717` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:7778` | `def _seed_defaults(self)` |
| `_selector_candidates` | method | `modules/lazy_loop.py:4215` | `def _selector_candidates(self)` |
| `_send_email` | method | `modules/lazy_loop.py:7656` | `def _send_email(channel, line, event)` |
| `_settle_objectives` | method | `modules/lazy_loop.py:10227` | `def _settle_objectives(self, task_id)` |
| `_settle_partial` | method | `modules/lazy_loop.py:5728` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:4083` | `def _signature(text)` |
| `_sleeper_round` | method | `modules/lazy_loop.py:8833` | `def _sleeper_round(self, activity)` |
| `_slug` | function | `modules/lazy_loop.py:1233` | `def _slug(value)` |
| `_snapshot` | method | `modules/lazy_loop.py:1599` | `def _snapshot(self)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:9506` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:10626` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:4828` | `def _stall_intent(self, existing)` |
| `_steps_for` | method | `modules/lazy_loop.py:5888` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:1066` | `def _store_path(name)` |
| `_structured_verdict` | method | `modules/lazy_loop.py:6258` | `def _structured_verdict(self, finding)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:447` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:11156` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:9617` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2777` | `def _target_as_asset(value)` |
| `_target_foothold_proven` | function | `modules/lazy_loop.py:3735` | `def _target_foothold_proven(target, task_id)` |
| `_target_for` | method | `modules/lazy_loop.py:5335` | `def _target_for(self, intent)` |
| `_target_services` | method | `modules/lazy_loop.py:4183` | `def _target_services(self, target)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:5793` | `def _task_executed_commands(self)` |
| `_technique_for` | method | `modules/lazy_loop.py:7152` | `def _technique_for(vulnclass, text)` |
| `_terminal_autopwn_fallback` | method | `modules/lazy_loop.py:10934` | `def _terminal_autopwn_fallback(self, task_id, executor, activity)` |
| `_traffic_template` | function | `modules/lazy_loop.py:1238` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:6563` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:623` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:467` | `def _valid_nmap_port_spec(value)` |
| `_veto_blocked_from_audit` | method | `modules/lazy_loop.py:10150` | `def _veto_blocked_from_audit(self, task_id)` |
| `_wake_event` | function | `modules/lazy_loop.py:825` | `def _wake_event(task_id)` |
| `_wire_store` | method | `modules/lazy_loop.py:2177` | `def _wire_store(self)` |
| `_work` | function | `modules/lazy_loop.py:7322` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:6383` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:10359` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_continuation` | method | `modules/lazy_loop.py:10258` | `def _write_continuation(self, task_id, status)` |
| `_write_draft` | method | `modules/lazy_loop.py:7359` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:5970` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:3068` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:3363` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2886` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:3270` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:7472` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:8357` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:8510` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:7596` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:3513` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1761` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:9220` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:9298` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:7807` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1683` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:2547` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:3532` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:11165` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:3448` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1774` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1789` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1785` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:7377` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:8774` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:2502` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:629` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:3293` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:8282` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:2641` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:3053` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:2382` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:8253` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:8858` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:8248` | `def bindings(self, agent)` |
| `blindspot_review` | method | `modules/lazy_loop.py:9238` | `def blindspot_review(self, task_id)` |
| `broadcast` | method | `modules/lazy_loop.py:11554` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:9187` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:7019` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:2377` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:7588` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:2590` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:3015` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1802` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1974` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:2508` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:8631` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:3568` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:4930` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:6813` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:6662` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1863` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:3277` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:7954` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta, temperature)` |
| `constraint_block` | function | `modules/lazy_loop.py:6894` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:8141` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1492` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1521` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:6609` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:3310` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:8997` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:3213` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:3896` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:1437` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:3354` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:9352` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:9386` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:11110` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:3383` | `def dequeue_next(self, order)` |
| `digest_of` | method | `modules/lazy_loop.py:2117` | `def digest_of(command, output)` |
| `digest_overview` | method | `modules/lazy_loop.py:6847` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:11184` | `def drain_queue(self, max_tasks, deadline_near)` |
| `edit_goal` | method | `modules/lazy_loop.py:9340` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1997` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:7694` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:3372` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3933` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:8942` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2929` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:2472` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:4965` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:6789` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:3507` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:2495` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:7573` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:11298` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:11357` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:11269` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:3653` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:3621` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:4733` | `def finalize(self, reason)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
