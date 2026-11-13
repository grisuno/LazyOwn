# Symbols (page 17 of 53)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `_bind_family` | method | `modules/lazy_fallback.py:251` | `def _bind_family(self, command)` |
| `_service_satisfied` | function | `modules/lazy_fallback.py:172` | `def _service_satisfied(required, services)` |
| `catalogue_ids` | function | `modules/lazy_fallback.py:261` | `def catalogue_ids()` |
| `matches` | method | `modules/lazy_fallback.py:61` | `def matches(self, command)` |
| `suggest` | method | `modules/lazy_fallback.py:203` | `def suggest(self, command, verdict, services, has_credentials, catalogue)` |
| `tried_count` | method | `modules/lazy_fallback.py:246` | `def tried_count(self)` |
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
| `ActivityLog` | class | `modules/lazy_loop.py:1885` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2778` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:1269` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:1244` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2872` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:6144` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:8190` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:7278` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:1235` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1432` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:1221` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:6959` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1857` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:2436` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:3024` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:8514` | `class LazyLoopEngine(EngineProxyMixin)` |
| `LazyTask` | class | `modules/lazy_loop.py:1258` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:7568` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:7399` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3813` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:5957` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2956` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:8116` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:8220` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:8382` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:8409` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:3226` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:8339` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:3184` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:8072` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:2018` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:4675` | `class Worker(WorkerAgenticMixin, WorkerExecutionMixin, WorkerGatingMixin, WorkerMemoryMixin)` |
| `__init__` | method | `modules/lazy_loop.py:1272` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1435` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1860` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1888` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2041` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2439` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2787` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2875` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2959` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3053` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3187` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3229` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3816` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:4678` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:5960` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:6152` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:6962` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:7281` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:7402` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7585` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8075` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8193` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8342` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8385` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:8539` | `def __init__(self, shell)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:6287` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:10731` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2722` | `def _asset_candidates(target)` |
| `_audit_blocked` | method | `modules/lazy_loop.py:5443` | `def _audit_blocked(self, source, reason, command, intent)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5656` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:9979` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:10015` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:6355` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:6169` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:7681` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:11284` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:4244` | `def _candidates(self)` |
| `_capture_wire` | method | `modules/lazy_loop.py:2099` | `def _capture_wire(self, digest, body)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:645` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:10649` | `def _check_goals(self, task_id, graph, activity)` |
| `_cold_path` | method | `modules/lazy_loop.py:6157` | `def _cold_path(self)` |
| `_commit` | method | `modules/lazy_loop.py:1505` | `def _commit(self, mutator)` |
| `_complete` | function | `modules/lazy_loop.py:9090` | `def _complete(prompt, max_tokens)` |
| `_constraints` | method | `modules/lazy_loop.py:3827` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:6347` | `def _content_versions(self)` |
| `_continuation_candidates` | method | `modules/lazy_loop.py:4156` | `def _continuation_candidates(self)` |
| `_current_phase` | method | `modules/lazy_loop.py:4028` | `def _current_phase(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:699` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4568` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:5589` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3836` | `def _denied(self, text)` |
| `_do` | function | `modules/lazy_loop.py:1557` | `def _do()` |
| `_do` | function | `modules/lazy_loop.py:1591` | `def _do()` |
| `_draft_report` | method | `modules/lazy_loop.py:7106` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:7102` | `def _drafts_ready_path(self)` |
| `_drain_drafts` | method | `modules/lazy_loop.py:10035` | `def _drain_drafts(self)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:9928` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:3048` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:741` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:661` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:10662` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_enrich_finding` | method | `modules/lazy_loop.py:2332` | `def _enrich_finding(self, finding_id, graph)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:10220` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:3031` | `def _event_for(cls, path, item_id)` |
| `_evidence_store` | method | `modules/lazy_loop.py:2047` | `def _evidence_store(self)` |
| `_find` | function | `modules/lazy_loop.py:6376` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:11180` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:5075` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:6315` | `def _foldable(self, node)` |
| `_fresh_scan_path` | function | `modules/lazy_loop.py:899` | `def _fresh_scan_path(target, max_age_sec)` |
| `_goals_met` | method | `modules/lazy_loop.py:10656` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:6364` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:5167` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_handover_credentials` | method | `modules/lazy_loop.py:10154` | `def _handover_credentials(settlement, findings)` |
| `_handover_deviations` | method | `modules/lazy_loop.py:10130` | `def _handover_deviations(task_id)` |
| `_has_creds` | method | `modules/lazy_loop.py:4232` | `def _has_creds()` |
| `_host_from_token` | function | `modules/lazy_loop.py:529` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:5943` | `def _host_like_target(target)` |
| `_initial_access_intent` | function | `modules/lazy_loop.py:3635` | `def _initial_access_intent(text)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:9310` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_host_like_target` | function | `modules/lazy_loop.py:334` | `def _is_host_like_target(value)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:422` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:6311` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:5934` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:608` | `def _kill()` |
| `_lazy_policy` | function | `modules/lazy_loop.py:3651` | `def _lazy_policy()` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:4005` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:4582` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:1101` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:1109` | `def _llm_quota_reply(text)` |
| `_load` | method | `modules/lazy_loop.py:3059` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7286` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8079` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8197` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8346` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:6173` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:6161` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2794` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:1055` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2798` | `def _load_task(self)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:6917` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2743` | `def _match_gate_rule(rule, target)` |
| `_maybe_blindspot` | method | `modules/lazy_loop.py:9887` | `def _maybe_blindspot(self, task_id, activity, stage_enabled, new_intents)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:10884` | `def _maybe_import_inbox(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:10904` | `def _maybe_selfupdate_check(self)` |
| `_merge_from_disk` | method | `modules/lazy_loop.py:1466` | `def _merge_from_disk(self, raw)` |
| `_noa_archive` | method | `modules/lazy_loop.py:6230` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:852` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:2373` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:967` | `def _now()` |
| `_objective_candidates` | method | `modules/lazy_loop.py:4186` | `def _objective_candidates(self)` |
| `_origin_fact` | method | `modules/lazy_loop.py:3996` | `def _origin_fact(self)` |
| `_os_hint` | method | `modules/lazy_loop.py:4057` | `def _os_hint()` |
| `_parts` | method | `modules/lazy_loop.py:8811` | `def _parts(self, task_id)` |
| `_payload_scope_items` | function | `modules/lazy_loop.py:3515` | `def _payload_scope_items()` |
| `_persist` | method | `modules/lazy_loop.py:1286` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1537` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2458` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3194` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3234` | `def _persist(self)` |
| `_policy_proposals` | function | `modules/lazy_loop.py:3673` | `def _policy_proposals(policy, target)` |
| `_preserve_evidence` | method | `modules/lazy_loop.py:2350` | `def _preserve_evidence(self, digest)` |
| `_prior_steps` | method | `modules/lazy_loop.py:4762` | `def _prior_steps(self, intent)` |
| `_publish_shell_proof` | method | `modules/lazy_loop.py:5499` | `def _publish_shell_proof(self, intent, target, command, output)` |
| `_record` | method | `modules/lazy_loop.py:7661` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:7761` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_deviation` | function | `modules/lazy_loop.py:59` | `def _record_deviation(scope, planned, actual, reason, source)` |
| `_record_raw` | method | `modules/lazy_loop.py:8027` | `def _record_raw(self, member, prompt, reply, ok, task_id, model_spec)` |
| `_record_selector_decision` | method | `modules/lazy_loop.py:4114` | `def _record_selector_decision(self, ctx, decision, command)` |
| `_refresh` | method | `modules/lazy_loop.py:3338` | `def _refresh(self)` |
| `_register_guardrails` | method | `modules/lazy_loop.py:8692` | `def _register_guardrails(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:586` | `def _register_loop_executor(executor)` |
| `_register_mediators` | method | `modules/lazy_loop.py:8681` | `def _register_mediators(self)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:7719` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:7161` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:6181` | `def _request_bodies(self, blocks, cold)` |
| `_restrict_file` | function | `modules/lazy_loop.py:637` | `def _restrict_file(path)` |
| `_rl_rank` | method | `modules/lazy_loop.py:4494` | `def _rl_rank(self, out)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:7690` | `def _rotated_chain(self, chain)` |
| `_run_chained` | method | `modules/lazy_loop.py:5467` | `def _run_chained(self, intent, command, executor, budget, intercept, retry_state)` |
| `_run_one` | function | `modules/lazy_loop.py:9730` | `def _run_one(index_node)` |
| `_run_round_guarded` | method | `modules/lazy_loop.py:8710` | `def _run_round_guarded(self, task_id, round_index, workers, executor)` |
| `_run_worker_guarded` | method | `modules/lazy_loop.py:8740` | `def _run_worker_guarded(self, worker, node, executor)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:5636` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:3063` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:6177` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:6165` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2805` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:1070` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2809` | `def _save_task(self, payload)` |
| `_scan_aggressive` | function | `modules/lazy_loop.py:881` | `def _scan_aggressive()` |
| `_scan_reuse_sec` | function | `modules/lazy_loop.py:862` | `def _scan_reuse_sec()` |
| `_scope_covers` | function | `modules/lazy_loop.py:2655` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2645` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:7596` | `def _seed_defaults(self)` |
| `_selector_candidates` | method | `modules/lazy_loop.py:4069` | `def _selector_candidates(self)` |
| `_send_email` | method | `modules/lazy_loop.py:7474` | `def _send_email(channel, line, event)` |
| `_settle_objectives` | method | `modules/lazy_loop.py:10053` | `def _settle_objectives(self, task_id)` |
| `_settle_partial` | method | `modules/lazy_loop.py:5548` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:3937` | `def _signature(text)` |
| `_sleeper_round` | method | `modules/lazy_loop.py:8652` | `def _sleeper_round(self, activity)` |
| `_slug` | function | `modules/lazy_loop.py:1086` | `def _slug(value)` |
| `_snapshot` | method | `modules/lazy_loop.py:1457` | `def _snapshot(self)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:9325` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:10450` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:4649` | `def _stall_intent(self, existing)` |
| `_steps_for` | method | `modules/lazy_loop.py:5708` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:972` | `def _store_path(name)` |
| `_structured_verdict` | method | `modules/lazy_loop.py:6077` | `def _structured_verdict(self, finding)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:416` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:10811` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:9532` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2705` | `def _target_as_asset(value)` |
| `_target_for` | method | `modules/lazy_loop.py:5159` | `def _target_for(self, intent)` |
| `_target_services` | method | `modules/lazy_loop.py:4037` | `def _target_services(self, target)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:5613` | `def _task_executed_commands(self)` |
| `_technique_for` | method | `modules/lazy_loop.py:6970` | `def _technique_for(vulnclass, text)` |
| `_traffic_template` | function | `modules/lazy_loop.py:1091` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:6382` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:592` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:436` | `def _valid_nmap_port_spec(value)` |
| `_wake_event` | function | `modules/lazy_loop.py:731` | `def _wake_event(task_id)` |
| `_wire_store` | method | `modules/lazy_loop.py:2085` | `def _wire_store(self)` |
| `_work` | function | `modules/lazy_loop.py:7140` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:6202` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:10185` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_continuation` | method | `modules/lazy_loop.py:10084` | `def _write_continuation(self, task_id, status)` |
| `_write_draft` | method | `modules/lazy_loop.py:7177` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:5789` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:2996` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:3291` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2814` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:3198` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:7290` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:8201` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:8354` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:7414` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:3441` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1657` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:9039` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:9117` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:7625` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1541` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:2465` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:3460` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:10820` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:3376` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1670` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1685` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1681` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:7195` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:8600` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:2420` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:598` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:3221` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:8126` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:2560` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:2981` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:2300` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:8097` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:8677` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:8092` | `def bindings(self, agent)` |
| `blindspot_review` | method | `modules/lazy_loop.py:9057` | `def blindspot_review(self, task_id)` |
| `broadcast` | method | `modules/lazy_loop.py:11209` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:9006` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:6838` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:2295` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:7406` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:2508` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2943` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1698` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1870` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:2426` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:8484` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:3496` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:4751` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:6632` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:6481` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1759` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:3205` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:7776` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta, temperature)` |
| `constraint_block` | function | `modules/lazy_loop.py:6713` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:7963` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1345` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1379` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:6428` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:3238` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:8816` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:3141` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:3753` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:1290` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:3282` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:9171` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:9205` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:10765` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:3311` | `def dequeue_next(self, order)` |
| `digest_of` | method | `modules/lazy_loop.py:2024` | `def digest_of(command, output)` |
| `digest_overview` | method | `modules/lazy_loop.py:6666` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:10839` | `def drain_queue(self, max_tasks, deadline_near)` |
| `edit_goal` | method | `modules/lazy_loop.py:9159` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1893` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:7512` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:3300` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3790` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:8761` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2857` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:2390` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:4786` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:6608` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:3435` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:2413` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:7391` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:10953` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:11012` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:10924` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:3581` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:3549` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:4552` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:6927` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1787` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:7350` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1932` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:7334` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:1324` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1600` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:2205` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:3249` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:8374` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:8397` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:9442` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:11402` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:11147` | `def graph_overview(self, task_id)` |
| `has_finding` | method | `modules/lazy_loop.py:1793` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:7952` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:2963` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:3089` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:8172` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:6321` | `def hot_set(self)` |
| `insert` | method | `modules/lazy_loop.py:1294` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `judge_command` | function | `modules/lazy_loop.py:1178` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:3480` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:3509` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2879` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:1328` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1689` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2853` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:3253` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8210` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8244` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8350` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8401` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1819` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:8905` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:3370` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:3701` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:8459` | `def log(self, task_id, limit, session)` |
| `looks_like_prose` | function | `modules/lazy_loop.py:307` | `def looks_like_prose(command)` |
| `lookup` | method | `modules/lazy_loop.py:2588` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:581` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:11333` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:1335` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:8214` | `def match(self, value)` |
| `members` | method | `modules/lazy_loop.py:7620` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:3214` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:6262` | `def noa_archives(self, limit)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
