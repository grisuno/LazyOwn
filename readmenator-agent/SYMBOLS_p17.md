# Symbols (page 17 of 52)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `ActivityLog` | class | `modules/lazy_loop.py:1958` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2819` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:1385` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:1360` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2913` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:6218` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:8239` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:7353` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:1351` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1543` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:1337` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:7034` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1930` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:2487` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:3065` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:8581` | `class LazyLoopEngine(EngineProxyMixin)` |
| `LazyTask` | class | `modules/lazy_loop.py:1374` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:7643` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:7474` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3854` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:6031` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2997` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:8165` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:8269` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:8431` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:8458` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:3267` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:8388` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:3225` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:8121` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:2080` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:4755` | `class Worker(WorkerAgenticMixin, WorkerExecutionMixin, WorkerGatingMixin, WorkerMemoryMixin)` |
| `__init__` | method | `modules/lazy_loop.py:1388` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1546` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1933` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1961` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2103` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2490` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2828` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2916` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3000` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:3094` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3228` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:3270` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3857` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:4758` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:6034` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:6226` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:7037` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:7356` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:7477` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7660` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8124` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8242` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8391` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8434` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:8606` | `def __init__(self, shell)` |
| `_append_jsonl` | function | `modules/lazy_loop.py:1115` | `def _append_jsonl(path, rows)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:6361` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:10705` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2763` | `def _asset_candidates(target)` |
| `_audit_blocked` | method | `modules/lazy_loop.py:5517` | `def _audit_blocked(self, source, reason, command, intent)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5730` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:9956` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:9992` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:6429` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:6243` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:7756` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:11258` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:4327` | `def _candidates(self)` |
| `_capture_wire` | method | `modules/lazy_loop.py:2160` | `def _capture_wire(self, digest, body)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:708` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:10623` | `def _check_goals(self, task_id, graph, activity)` |
| `_cold_path` | method | `modules/lazy_loop.py:6231` | `def _cold_path(self)` |
| `_commit` | method | `modules/lazy_loop.py:1616` | `def _commit(self, mutator)` |
| `_complete` | function | `modules/lazy_loop.py:9157` | `def _complete(prompt, max_tokens)` |
| `_constraints` | method | `modules/lazy_loop.py:3868` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:6421` | `def _content_versions(self)` |
| `_continuation_candidates` | method | `modules/lazy_loop.py:4200` | `def _continuation_candidates(self)` |
| `_current_phase` | method | `modules/lazy_loop.py:4072` | `def _current_phase(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:762` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:4650` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:5663` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3877` | `def _denied(self, text)` |
| `_do` | function | `modules/lazy_loop.py:1668` | `def _do()` |
| `_do` | function | `modules/lazy_loop.py:1702` | `def _do()` |
| `_draft_report` | method | `modules/lazy_loop.py:7181` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:7177` | `def _drafts_ready_path(self)` |
| `_drain_drafts` | method | `modules/lazy_loop.py:10012` | `def _drain_drafts(self)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:9905` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:3089` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:804` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:724` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:10636` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_enrich_finding` | method | `modules/lazy_loop.py:2383` | `def _enrich_finding(self, finding_id, graph)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:10197` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:3072` | `def _event_for(cls, path, item_id)` |
| `_evidence_store` | method | `modules/lazy_loop.py:2109` | `def _evidence_store(self)` |
| `_find` | function | `modules/lazy_loop.py:6450` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:11154` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:5153` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:6389` | `def _foldable(self, node)` |
| `_fresh_scan_path` | function | `modules/lazy_loop.py:962` | `def _fresh_scan_path(target, max_age_sec)` |
| `_goals_met` | method | `modules/lazy_loop.py:10630` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:6438` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:5243` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_handover_credentials` | method | `modules/lazy_loop.py:10131` | `def _handover_credentials(settlement, findings)` |
| `_handover_deviations` | method | `modules/lazy_loop.py:10107` | `def _handover_deviations(task_id)` |
| `_has_creds` | method | `modules/lazy_loop.py:4276` | `def _has_creds()` |
| `_host_from_token` | function | `modules/lazy_loop.py:529` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:6017` | `def _host_like_target(target)` |
| `_initial_access_candidate` | method | `modules/lazy_loop.py:4288` | `def _initial_access_candidate(self, existing)` |
| `_initial_access_intent` | function | `modules/lazy_loop.py:3676` | `def _initial_access_intent(text)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:9377` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_host_like_target` | function | `modules/lazy_loop.py:334` | `def _is_host_like_target(value)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:422` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:6385` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:6008` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:608` | `def _kill()` |
| `_lazy_policy` | function | `modules/lazy_loop.py:3692` | `def _lazy_policy()` |
| `_ledger_confirmed_count` | function | `modules/lazy_loop.py:8554` | `def _ledger_confirmed_count(task_id)` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:4049` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:4664` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:1217` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:1225` | `def _llm_quota_reply(text)` |
| `_load` | method | `modules/lazy_loop.py:3100` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7361` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8128` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8246` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8395` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:6247` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:6235` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2835` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:1171` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2839` | `def _load_task(self)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:6991` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2784` | `def _match_gate_rule(rule, target)` |
| `_maybe_blindspot` | method | `modules/lazy_loop.py:9864` | `def _maybe_blindspot(self, task_id, activity, stage_enabled, new_intents)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:10858` | `def _maybe_import_inbox(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:10878` | `def _maybe_selfupdate_check(self)` |
| `_merge_from_disk` | method | `modules/lazy_loop.py:1577` | `def _merge_from_disk(self, raw)` |
| `_noa_archive` | method | `modules/lazy_loop.py:6304` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:915` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:2424` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:1030` | `def _now()` |
| `_objective_candidates` | method | `modules/lazy_loop.py:4230` | `def _objective_candidates(self)` |
| `_origin_fact` | method | `modules/lazy_loop.py:4040` | `def _origin_fact(self)` |
| `_os_hint` | method | `modules/lazy_loop.py:4101` | `def _os_hint()` |
| `_parts` | method | `modules/lazy_loop.py:8878` | `def _parts(self, task_id)` |
| `_payload_scope_items` | function | `modules/lazy_loop.py:3556` | `def _payload_scope_items()` |
| `_persist` | method | `modules/lazy_loop.py:1402` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1648` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2509` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3235` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:3275` | `def _persist(self)` |
| `_policy_proposals` | function | `modules/lazy_loop.py:3714` | `def _policy_proposals(policy, target)` |
| `_pre_round_gate` | method | `modules/lazy_loop.py:9580` | `def _pre_round_gate(self, task_id)` |
| `_preserve_evidence` | method | `modules/lazy_loop.py:2401` | `def _preserve_evidence(self, digest)` |
| `_prior_steps` | method | `modules/lazy_loop.py:4842` | `def _prior_steps(self, intent)` |
| `_publish_shell_proof` | method | `modules/lazy_loop.py:5573` | `def _publish_shell_proof(self, intent, target, command, output)` |
| `_read_jsonl` | function | `modules/lazy_loop.py:1141` | `def _read_jsonl(path, limit)` |
| `_record` | method | `modules/lazy_loop.py:7736` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:7833` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_deviation` | function | `modules/lazy_loop.py:59` | `def _record_deviation(scope, planned, actual, reason, source)` |
| `_record_raw` | method | `modules/lazy_loop.py:8080` | `def _record_raw(self, member, prompt, reply, ok, task_id, model_spec)` |
| `_record_selector_decision` | method | `modules/lazy_loop.py:4158` | `def _record_selector_decision(self, ctx, decision, command)` |
| `_refresh` | method | `modules/lazy_loop.py:3379` | `def _refresh(self)` |
| `_register_guardrails` | method | `modules/lazy_loop.py:8759` | `def _register_guardrails(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:586` | `def _register_loop_executor(executor)` |
| `_register_mediators` | method | `modules/lazy_loop.py:8748` | `def _register_mediators(self)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:7794` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:7236` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:6255` | `def _request_bodies(self, blocks, cold)` |
| `_restrict_file` | function | `modules/lazy_loop.py:700` | `def _restrict_file(path)` |
| `_rl_rank` | method | `modules/lazy_loop.py:4577` | `def _rl_rank(self, out)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:7765` | `def _rotated_chain(self, chain)` |
| `_run_chained` | method | `modules/lazy_loop.py:5541` | `def _run_chained(self, intent, command, executor, budget, intercept, retry_state)` |
| `_run_one` | function | `modules/lazy_loop.py:9707` | `def _run_one(index_node)` |
| `_run_round_guarded` | method | `modules/lazy_loop.py:8777` | `def _run_round_guarded(self, task_id, round_index, workers, executor)` |
| `_run_worker_guarded` | method | `modules/lazy_loop.py:8807` | `def _run_worker_guarded(self, worker, node, executor)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:5710` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:3104` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:6251` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:6239` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2846` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:1186` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2850` | `def _save_task(self, payload)` |
| `_scan_aggressive` | function | `modules/lazy_loop.py:944` | `def _scan_aggressive()` |
| `_scan_reuse_sec` | function | `modules/lazy_loop.py:925` | `def _scan_reuse_sec()` |
| `_scope_covers` | function | `modules/lazy_loop.py:2696` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2686` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:7671` | `def _seed_defaults(self)` |
| `_selector_candidates` | method | `modules/lazy_loop.py:4113` | `def _selector_candidates(self)` |
| `_send_email` | method | `modules/lazy_loop.py:7549` | `def _send_email(channel, line, event)` |
| `_settle_objectives` | method | `modules/lazy_loop.py:10030` | `def _settle_objectives(self, task_id)` |
| `_settle_partial` | method | `modules/lazy_loop.py:5622` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:3981` | `def _signature(text)` |
| `_sleeper_round` | method | `modules/lazy_loop.py:8719` | `def _sleeper_round(self, activity)` |
| `_slug` | function | `modules/lazy_loop.py:1202` | `def _slug(value)` |
| `_snapshot` | method | `modules/lazy_loop.py:1568` | `def _snapshot(self)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:9392` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:10424` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:4729` | `def _stall_intent(self, existing)` |
| `_steps_for` | method | `modules/lazy_loop.py:5782` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:1035` | `def _store_path(name)` |
| `_structured_verdict` | method | `modules/lazy_loop.py:6151` | `def _structured_verdict(self, finding)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:416` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:10785` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:9503` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2746` | `def _target_as_asset(value)` |
| `_target_for` | method | `modules/lazy_loop.py:5235` | `def _target_for(self, intent)` |
| `_target_services` | method | `modules/lazy_loop.py:4081` | `def _target_services(self, target)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:5687` | `def _task_executed_commands(self)` |
| `_technique_for` | method | `modules/lazy_loop.py:7045` | `def _technique_for(vulnclass, text)` |
| `_traffic_template` | function | `modules/lazy_loop.py:1207` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:6456` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:592` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:436` | `def _valid_nmap_port_spec(value)` |
| `_wake_event` | function | `modules/lazy_loop.py:794` | `def _wake_event(task_id)` |
| `_wire_store` | method | `modules/lazy_loop.py:2146` | `def _wire_store(self)` |
| `_work` | function | `modules/lazy_loop.py:7215` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:6276` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:10162` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_continuation` | method | `modules/lazy_loop.py:10061` | `def _write_continuation(self, task_id, status)` |
| `_write_draft` | method | `modules/lazy_loop.py:7252` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:5863` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:3037` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:3332` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2855` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:3239` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:7365` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:8250` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:8403` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:7489` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:3482` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1730` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:9106` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:9184` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:7700` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1652` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:2516` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:3501` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:10794` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:3417` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1743` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1758` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1754` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:7270` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:8667` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:2471` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:598` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:3262` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:8175` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:2610` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:3022` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:2351` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:8146` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:8744` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:8141` | `def bindings(self, agent)` |
| `blindspot_review` | method | `modules/lazy_loop.py:9124` | `def blindspot_review(self, task_id)` |
| `broadcast` | method | `modules/lazy_loop.py:11183` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:9073` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:6912` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:2346` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:7481` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:2559` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2984` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1771` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1943` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:2477` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:8524` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:3537` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:4831` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:6706` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:6555` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1832` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:3246` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:7847` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta, temperature)` |
| `constraint_block` | function | `modules/lazy_loop.py:6787` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:8034` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1461` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1490` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:6502` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:3279` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:8883` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:3182` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:3794` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:1406` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:3323` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:9238` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:9272` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:10739` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:3352` | `def dequeue_next(self, order)` |
| `digest_of` | method | `modules/lazy_loop.py:2086` | `def digest_of(command, output)` |
| `digest_overview` | method | `modules/lazy_loop.py:6740` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:10813` | `def drain_queue(self, max_tasks, deadline_near)` |
| `edit_goal` | method | `modules/lazy_loop.py:9226` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1966` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:7587` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:3341` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3831` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:8828` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2898` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:2441` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:4866` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:6682` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:3476` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:2464` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:7466` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:10927` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:10986` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:10898` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:3622` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:3590` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:4634` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:7002` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1860` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:7425` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1994` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:7409` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:1440` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1711` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:2256` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:3290` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:8423` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:8446` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:9413` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:11376` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:11121` | `def graph_overview(self, task_id)` |
| `has_finding` | method | `modules/lazy_loop.py:1866` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:8023` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:3004` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:3130` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:8221` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:6395` | `def hot_set(self)` |
| `insert` | method | `modules/lazy_loop.py:1410` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `judge_command` | function | `modules/lazy_loop.py:1294` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:3521` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:3550` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2920` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:1444` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1762` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2894` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:3294` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8259` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8293` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8399` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8450` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1892` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:8972` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:3411` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:3742` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:8508` | `def log(self, task_id, limit, session)` |
| `looks_like_prose` | function | `modules/lazy_loop.py:307` | `def looks_like_prose(command)` |
| `lookup` | method | `modules/lazy_loop.py:2629` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:581` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:11307` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:1451` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:8263` | `def match(self, value)` |
| `mediation_feedback` | function | `modules/lazy_loop.py:682` | `def mediation_feedback()` |
| `mediation_intel` | function | `modules/lazy_loop.py:654` | `def mediation_intel()` |
| `mediation_resolve` | function | `modules/lazy_loop.py:633` | `def mediation_resolve(domain)` |
| `mediation_telemetry` | function | `modules/lazy_loop.py:668` | `def mediation_telemetry()` |
| `members` | method | `modules/lazy_loop.py:7695` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:3255` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:6336` | `def noa_archives(self, limit)` |
| `node_detail` | method | `modules/lazy_loop.py:1876` | `def node_detail(self, node_id)` |
| `note_trigger` | method | `modules/lazy_loop.py:3053` | `def note_trigger(self, task_id, trigger_id)` |
| `on_planner_round` | method | `modules/lazy_loop.py:6514` | `def on_planner_round(self)` |
| `orchestrate` | method | `modules/lazy_loop.py:8855` | `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` |
| `order` | function | `modules/lazy_loop.py:10834` | `def order(items)` |
| `overview` | method | `modules/lazy_loop.py:1785` | `def overview(self)` |
| `parents` | method | `modules/lazy_loop.py:1778` | `def parents(self, node_id, kind)` |
| `parse_judge_output` | function | `modules/lazy_loop.py:1256` | `def parse_judge_output(raw)` |
| `pause` | method | `modules/lazy_loop.py:3310` | `def pause(self, task_id)` |
| `pause_task` | method | `modules/lazy_loop.py:9000` | `def pause_task(self, task_id, reason)` |
| `pending` | method | `modules/lazy_loop.py:1938` | `def pending(self)` |
| `pending` | method | `modules/lazy_loop.py:3126` | `def pending(self)` |
| `persist` | method | `modules/lazy_loop.py:1715` | `def persist(self)` |
| `plan` | method | `modules/lazy_loop.py:3885` | `def plan(self, triggers)` |
| `planner_temperature` | function | `modules/lazy_loop.py:132` | `def planner_temperature()` |
| `plausible_command` | function | `modules/lazy_loop.py:275` | `def plausible_command(command)` |
| `preview_delete_intent` | method | `modules/lazy_loop.py:9249` | `def preview_delete_intent(self, task_id, intent_id)` |
| `prove_goal` | method | `modules/lazy_loop.py:10590` | `def prove_goal(self, task_id, goal_id, evidence_id, reason)` |
| `queue` | method | `modules/lazy_loop.py:3336` | `def queue(self)` |
| `ranked` | method | `modules/lazy_loop.py:7346` | `def ranked(self)` |
| `raw_entries` | method | `modules/lazy_loop.py:8051` | `def raw_entries(self, limit)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
