# Symbols (page 16 of 48)
Previous: [SYMBOLS_p15.md](SYMBOLS_p15.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `backport_status` | function | `modules/lazy_heat.py:342` | `def backport_status(banner, fixed_revision)` |
| `classify_heat` | function | `modules/lazy_heat.py:68` | `def classify_heat(kev, epss, exploit, cvss)` |
| `compare_versions` | function | `modules/lazy_heat.py:154` | `def compare_versions(a, b)` |
| `cvss3_base_score` | function | `modules/lazy_heat.py:204` | `def cvss3_base_score(vector)` |
| `label_for` | function | `modules/lazy_heat.py:370` | `def label_for(status, fixed_revision)` |
| `match_heat` | function | `modules/lazy_heat.py:91` | `def match_heat(tier, cvss, verdict, distro_status)` |
| `parse_distro_revision` | function | `modules/lazy_heat.py:303` | `def parse_distro_revision(banner)` |
| `parse_version` | function | `modules/lazy_heat.py:118` | `def parse_version(value, strict)` |
| `product_token` | function | `modules/lazy_heat.py:246` | `def product_token(value)` |
| `token_matches` | function | `modules/lazy_heat.py:269` | `def token_matches(haystack, needle)` |
| `version_in_range` | function | `modules/lazy_heat.py:162` | `def version_in_range(ver, rng)` |
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
| `ActivityLog` | class | `modules/lazy_loop.py:1508` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2240` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:995` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:970` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2334` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:6180` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:8196` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:7313` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:961` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1158` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:947` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:6995` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1480` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:1899` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:2486` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:8520` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:984` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:7585` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:7416` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3197` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:5993` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2418` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:8122` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:8226` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:8388` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:8415` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:2688` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:8345` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:2646` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:8078` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:1641` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:3935` | `class Worker` |
| `__init__` | method | `modules/lazy_loop.py:998` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1161` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1483` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1511` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1644` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1902` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2249` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2337` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2421` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2515` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2649` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2691` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3200` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:3938` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:5996` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:6188` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:6998` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:7316` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:7419` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7602` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8081` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8199` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8348` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8391` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:8545` | `def __init__(self, shell)` |
| `_absorb_reaction` | method | `modules/lazy_loop.py:4561` | `def _absorb_reaction(self, intent, command, output)` |
| `_agent_checkpoint` | method | `modules/lazy_loop.py:4858` | `def _agent_checkpoint(self, intent)` |
| `_agent_preflight` | method | `modules/lazy_loop.py:4884` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/lazy_loop.py:5229` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/lazy_loop.py:5047` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agentic_try` | method | `modules/lazy_loop.py:5261` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:6323` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:10361` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2184` | `def _asset_candidates(target)` |
| `_auto_approve` | method | `modules/lazy_loop.py:5370` | `def _auto_approve(self, command)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5712` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:9796` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:9832` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:6391` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:6205` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:7698` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:11062` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:3510` | `def _candidates(self)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:534` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:10287` | `def _check_goals(self, task_id, graph, activity)` |
| `_close_shell_session` | method | `modules/lazy_loop.py:5020` | `def _close_shell_session(self)` |
| `_cold_path` | method | `modules/lazy_loop.py:6193` | `def _cold_path(self)` |
| `_command_in_scope` | method | `modules/lazy_loop.py:5703` | `def _command_in_scope(self, command)` |
| `_constraints` | method | `modules/lazy_loop.py:3211` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:6383` | `def _content_versions(self)` |
| `_current_phase` | method | `modules/lazy_loop.py:3412` | `def _current_phase(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:588` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:3828` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:5602` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3220` | `def _denied(self, text)` |
| `_denied` | method | `modules/lazy_loop.py:5359` | `def _denied(self, command)` |
| `_draft_report` | method | `modules/lazy_loop.py:7141` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:7137` | `def _drafts_ready_path(self)` |
| `_drain_steer` | method | `modules/lazy_loop.py:4873` | `def _drain_steer(self, intent)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:9745` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:2510` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:630` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:550` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:10300` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:9887` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:2493` | `def _event_for(cls, path, item_id)` |
| `_fact_memory_store` | method | `modules/lazy_loop.py:4539` | `def _fact_memory_store(self)` |
| `_failure_memory` | method | `modules/lazy_loop.py:4467` | `def _failure_memory(self)` |
| `_find` | function | `modules/lazy_loop.py:6412` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:10958` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:4382` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:6351` | `def _foldable(self, node)` |
| `_goals_met` | method | `modules/lazy_loop.py:10294` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:6400` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:4613` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_has_creds` | method | `modules/lazy_loop.py:3498` | `def _has_creds()` |
| `_host_from_token` | function | `modules/lazy_loop.py:418` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:5985` | `def _host_like_target(target)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:9188` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_host_like_target` | function | `modules/lazy_loop.py:219` | `def _is_host_like_target(value)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:311` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:6347` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:5976` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:497` | `def _kill()` |
| `_lab_scope_default` | method | `modules/lazy_loop.py:4050` | `def _lab_scope_default(self, target)` |
| `_lazy_policy` | function | `modules/lazy_loop.py:3035` | `def _lazy_policy()` |
| `_learn_os` | method | `modules/lazy_loop.py:4512` | `def _learn_os(self, intent, command, output)` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:3389` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:3842` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:838` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:846` | `def _llm_quota_reply(text)` |
| `_llm_steps` | method | `modules/lazy_loop.py:5466` | `def _llm_steps(self, intent, prior_text)` |
| `_load` | method | `modules/lazy_loop.py:2521` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7321` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8085` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8203` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8352` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:6209` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:6197` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2256` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:798` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2260` | `def _load_task(self)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:6953` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2205` | `def _match_gate_rule(rule, target)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:10662` | `def _maybe_import_inbox(self)` |
| `_maybe_proxy_gc` | method | `modules/lazy_loop.py:10636` | `def _maybe_proxy_gc(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:10682` | `def _maybe_selfupdate_check(self)` |
| `_missing_tool` | method | `modules/lazy_loop.py:5382` | `def _missing_tool(self, command)` |
| `_noa_archive` | method | `modules/lazy_loop.py:6266` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:738` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:1836` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:780` | `def _now()` |
| `_open_shell_session` | method | `modules/lazy_loop.py:4949` | `def _open_shell_session(self, intent)` |
| `_origin_fact` | method | `modules/lazy_loop.py:3380` | `def _origin_fact(self)` |
| `_os_gate` | method | `modules/lazy_loop.py:4486` | `def _os_gate(self, intent, command)` |
| `_os_hint` | method | `modules/lazy_loop.py:3441` | `def _os_hint()` |
| `_parts` | method | `modules/lazy_loop.py:8755` | `def _parts(self, task_id)` |
| `_persist` | method | `modules/lazy_loop.py:1012` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1183` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1921` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2656` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2696` | `def _persist(self)` |
| `_policy_proposals` | function | `modules/lazy_loop.py:3057` | `def _policy_proposals(policy, target)` |
| `_prior_steps` | method | `modules/lazy_loop.py:4082` | `def _prior_steps(self, intent)` |
| `_reader` | function | `modules/lazy_loop.py:4971` | `def _reader()` |
| `_recall_facts` | method | `modules/lazy_loop.py:4554` | `def _recall_facts(self, query, k)` |
| `_record` | method | `modules/lazy_loop.py:7678` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:7778` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_raw` | method | `modules/lazy_loop.py:8033` | `def _record_raw(self, member, prompt, reply, ok, task_id, model_spec)` |
| `_refresh` | method | `modules/lazy_loop.py:2784` | `def _refresh(self)` |
| `_register_guardrails` | method | `modules/lazy_loop.py:8636` | `def _register_guardrails(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:475` | `def _register_loop_executor(executor)` |
| `_register_mediators` | method | `modules/lazy_loop.py:8625` | `def _register_mediators(self)` |
| `_remember_fact` | method | `modules/lazy_loop.py:4545` | `def _remember_fact(self, intent, command, output)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:7736` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:7196` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:6217` | `def _request_bodies(self, blocks, cold)` |
| `_resolved_command` | method | `modules/lazy_loop.py:5626` | `def _resolved_command(self, command)` |
| `_restrict_file` | function | `modules/lazy_loop.py:526` | `def _restrict_file(path)` |
| `_rl_rank` | method | `modules/lazy_loop.py:3754` | `def _rl_rank(self, out)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:7707` | `def _rotated_chain(self, chain)` |
| `_run` | method | `modules/lazy_loop.py:5398` | `def _run(self, command, executor)` |
| `_run_one` | function | `modules/lazy_loop.py:9590` | `def _run_one(index_node)` |
| `_run_round_guarded` | method | `modules/lazy_loop.py:8654` | `def _run_round_guarded(self, task_id, round_index, workers, executor)` |
| `_run_worker_guarded` | method | `modules/lazy_loop.py:8684` | `def _run_worker_guarded(self, worker, node, executor)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:5690` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:2525` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:6213` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:6201` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2267` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:808` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2271` | `def _save_task(self, payload)` |
| `_scope_allows_target` | method | `modules/lazy_loop.py:4021` | `def _scope_allows_target(self, target)` |
| `_scope_covers` | function | `modules/lazy_loop.py:2117` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2107` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:7613` | `def _seed_defaults(self)` |
| `_selector_candidates` | method | `modules/lazy_loop.py:3453` | `def _selector_candidates(self)` |
| `_send_email` | method | `modules/lazy_loop.py:7491` | `def _send_email(channel, line, event)` |
| `_send_shell` | method | `modules/lazy_loop.py:4984` | `def _send_shell(self, command, intent, timeout_sec)` |
| `_settle_partial` | method | `modules/lazy_loop.py:5561` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:3321` | `def _signature(text)` |
| `_slug` | function | `modules/lazy_loop.py:823` | `def _slug(value)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:9203` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:10091` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:3909` | `def _stall_intent(self, existing)` |
| `_start_background_job` | method | `modules/lazy_loop.py:4917` | `def _start_background_job(self, command, intent, transcripts)` |
| `_steps_for` | method | `modules/lazy_loop.py:5764` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:785` | `def _store_path(name)` |
| `_structured_verdict` | method | `modules/lazy_loop.py:6113` | `def _structured_verdict(self, finding)` |
| `_sudo_guard` | method | `modules/lazy_loop.py:5640` | `def _sudo_guard(self, intent, command)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:305` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:10500` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:9410` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2167` | `def _target_as_asset(value)` |
| `_target_for` | method | `modules/lazy_loop.py:4459` | `def _target_for(self, intent)` |
| `_target_services` | method | `modules/lazy_loop.py:3421` | `def _target_services(self, target)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:5667` | `def _task_executed_commands(self)` |
| `_technique_for` | method | `modules/lazy_loop.py:7006` | `def _technique_for(vulnclass, text)` |
| `_traffic_template` | function | `modules/lazy_loop.py:828` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:6418` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:481` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:325` | `def _valid_nmap_port_spec(value)` |
| `_wake_event` | function | `modules/lazy_loop.py:620` | `def _wake_event(task_id)` |
| `_with_llm_steps` | method | `modules/lazy_loop.py:5448` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `_work` | function | `modules/lazy_loop.py:4929` | `def _work()` |
| `_work` | function | `modules/lazy_loop.py:7175` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:6238` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:9852` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_draft` | method | `modules/lazy_loop.py:7212` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:5834` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:2458` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:2753` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2276` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:2660` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:7325` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:8207` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:8360` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:7431` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:2887` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1280` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:8973` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:8991` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:7642` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1195` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:1928` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:2906` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:10509` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:2822` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1293` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1308` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1304` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:7230` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:8580` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:1883` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:487` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:2683` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:8132` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:2022` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:2443` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:1805` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:8103` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:8621` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:8098` | `def bindings(self, agent)` |
| `broadcast` | method | `modules/lazy_loop.py:10987` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:8940` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:6874` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:1800` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:7423` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:1970` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2405` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1321` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1493` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:1889` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:8490` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:2942` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:4010` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:6668` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:6517` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1382` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:2667` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:7793` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` |
| `constraint_block` | function | `modules/lazy_loop.py:6749` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:7969` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1071` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1105` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:6464` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:2700` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:8760` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:2603` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:3137` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:1016` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:2744` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:9045` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:9079` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:10395` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:2773` | `def dequeue_next(self)` |
| `digest_overview` | method | `modules/lazy_loop.py:6702` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:10528` | `def drain_queue(self, max_tasks)` |
| `edit_goal` | method | `modules/lazy_loop.py:9033` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1516` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:7529` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:2762` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3174` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:8705` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2319` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:1853` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:4106` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:6644` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:2881` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:1876` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:7408` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:10731` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:10790` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:10702` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:2993` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:2961` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:3812` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:6963` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1410` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:7367` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1555` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:7351` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:1050` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1223` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:1724` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:2711` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:8380` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:8403` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:9320` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:11180` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:10925` | `def graph_overview(self, task_id)` |
| `graph_state` | function | `modules/lazy_loop.py:5117` | `def graph_state()` |
| `has_finding` | method | `modules/lazy_loop.py:1416` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:7958` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:2425` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:2551` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:8178` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:6357` | `def hot_set(self)` |
| `ingest_proxy_traffic` | method | `modules/lazy_loop.py:10556` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `insert` | method | `modules/lazy_loop.py:1020` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `job_output` | function | `modules/lazy_loop.py:5148` | `def job_output(job_id)` |
| `job_status` | function | `modules/lazy_loop.py:5140` | `def job_status(job_id)` |
| `judge_command` | function | `modules/lazy_loop.py:905` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:2926` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:2955` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2341` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:1054` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1312` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2315` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:2715` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8216` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8250` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8356` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8407` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1442` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:8839` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:2816` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:3085` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:8465` | `def log(self, task_id, limit, session)` |
| `looks_like_prose` | function | `modules/lazy_loop.py:192` | `def looks_like_prose(command)` |
| `lookup` | method | `modules/lazy_loop.py:2050` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:470` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:11111` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:1061` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:8220` | `def match(self, value)` |
| `members` | method | `modules/lazy_loop.py:7637` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:2676` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:6298` | `def noa_archives(self, limit)` |
| `node_detail` | method | `modules/lazy_loop.py:1426` | `def node_detail(self, node_id)` |
| `note_trigger` | method | `modules/lazy_loop.py:2474` | `def note_trigger(self, task_id, trigger_id)` |
| `on_planner_round` | method | `modules/lazy_loop.py:6476` | `def on_planner_round(self)` |
| `orchestrate` | method | `modules/lazy_loop.py:8732` | `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` |
| `overview` | method | `modules/lazy_loop.py:1335` | `def overview(self)` |
| `parents` | method | `modules/lazy_loop.py:1328` | `def parents(self, node_id, kind)` |
| `parse_judge_output` | function | `modules/lazy_loop.py:877` | `def parse_judge_output(raw)` |
| `pause` | method | `modules/lazy_loop.py:2731` | `def pause(self, task_id)` |
| `pause_intent` | method | `modules/lazy_loop.py:9224` | `def pause_intent(self, task_id, intent_id)` |
| `pause_task` | method | `modules/lazy_loop.py:8867` | `def pause_task(self, task_id, reason)` |
| `pending` | method | `modules/lazy_loop.py:1488` | `def pending(self)` |
| `pending` | method | `modules/lazy_loop.py:2547` | `def pending(self)` |
| `persist` | method | `modules/lazy_loop.py:1227` | `def persist(self)` |
| `plan` | method | `modules/lazy_loop.py:3228` | `def plan(self, triggers)` |
| `plausible_command` | function | `modules/lazy_loop.py:168` | `def plausible_command(command)` |
| `preview_delete_intent` | method | `modules/lazy_loop.py:9056` | `def preview_delete_intent(self, task_id, intent_id)` |
| `prove_goal` | method | `modules/lazy_loop.py:10254` | `def prove_goal(self, task_id, goal_id, evidence_id, reason)` |
| `proxy_env` | method | `modules/lazy_loop.py:10479` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/lazy_loop.py:10429` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/lazy_loop.py:10473` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/lazy_loop.py:10465` | `def proxy_stop(self)` |

Next: [SYMBOLS_p17.md](SYMBOLS_p17.md)
