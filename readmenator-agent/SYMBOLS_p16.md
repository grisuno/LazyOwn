# Symbols (page 16 of 48)
Previous: [SYMBOLS_p15.md](SYMBOLS_p15.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `LazyEngine` | class | `modules/lazy_engine.py:55` | `class LazyEngine(LazyLoopEngine)` |
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
| `ActivityLog` | class | `modules/lazy_loop.py:1457` | `class ActivityLog` |
| `AssetGate` | class | `modules/lazy_loop.py:2189` | `class AssetGate` |
| `AssetGraph` | class | `modules/lazy_loop.py:944` | `class AssetGraph` |
| `AssetNode` | class | `modules/lazy_loop.py:919` | `class AssetNode` |
| `Budget` | class | `modules/lazy_loop.py:2283` | `class Budget` |
| `ColdCompactor` | class | `modules/lazy_loop.py:6004` | `class ColdCompactor` |
| `CompanyScope` | class | `modules/lazy_loop.py:7958` | `class CompanyScope` |
| `EvidenceStore` | class | `modules/lazy_loop.py:7075` | `class EvidenceStore` |
| `ExplorationEdge` | class | `modules/lazy_loop.py:910` | `class ExplorationEdge` |
| `ExplorationGraph` | class | `modules/lazy_loop.py:1107` | `class ExplorationGraph` |
| `ExplorationNode` | class | `modules/lazy_loop.py:896` | `class ExplorationNode` |
| `FindingService` | class | `modules/lazy_loop.py:6757` | `class FindingService` |
| `Frontier` | class | `modules/lazy_loop.py:1429` | `class Frontier` |
| `Guard` | class | `modules/lazy_loop.py:1848` | `class Guard` |
| `InterceptQueue` | class | `modules/lazy_loop.py:2435` | `class InterceptQueue` |
| `LazyLoopEngine` | class | `modules/lazy_loop.py:8282` | `class LazyLoopEngine` |
| `LazyTask` | class | `modules/lazy_loop.py:933` | `class LazyTask` |
| `LlmPool` | class | `modules/lazy_loop.py:7347` | `class LlmPool` |
| `Notifier` | class | `modules/lazy_loop.py:7178` | `class Notifier` |
| `Planner` | class | `modules/lazy_loop.py:3146` | `class Planner` |
| `Retester` | class | `modules/lazy_loop.py:5817` | `class Retester` |
| `RuntimeTracker` | class | `modules/lazy_loop.py:2367` | `class RuntimeTracker` |
| `SideQuestions` | class | `modules/lazy_loop.py:7884` | `class SideQuestions` |
| `TaskArchive` | class | `modules/lazy_loop.py:7988` | `class TaskArchive` |
| `TaskCategory` | class | `modules/lazy_loop.py:8150` | `class TaskCategory` |
| `TaskChat` | class | `modules/lazy_loop.py:8177` | `class TaskChat` |
| `TaskStore` | class | `modules/lazy_loop.py:2637` | `class TaskStore` |
| `TaskTemplate` | class | `modules/lazy_loop.py:8107` | `class TaskTemplate` |
| `TodoStore` | class | `modules/lazy_loop.py:2595` | `class TodoStore` |
| `ToolCatalog` | class | `modules/lazy_loop.py:7840` | `class ToolCatalog` |
| `TrafficLog` | class | `modules/lazy_loop.py:1590` | `class TrafficLog` |
| `Worker` | class | `modules/lazy_loop.py:3785` | `class Worker` |
| `__init__` | method | `modules/lazy_loop.py:947` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:1110` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1432` | `def __init__(self, graph)` |
| `__init__` | method | `modules/lazy_loop.py:1460` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1593` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:1851` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2198` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2286` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2370` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:2464` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2598` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:2640` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:3149` | `def __init__(self, task_id, assets, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:3788` | `def __init__(self, name, task_id, assets, graph, activity, traffic, guard, store, shell, ephemeral)` |
| `__init__` | method | `modules/lazy_loop.py:5820` | `def __init__(self, graph, activity, traffic)` |
| `__init__` | method | `modules/lazy_loop.py:6012` | `def __init__(self, graph, activity)` |
| `__init__` | method | `modules/lazy_loop.py:6760` | `def __init__(self, task_id, graph, activity, store)` |
| `__init__` | method | `modules/lazy_loop.py:7078` | `def __init__(self, task_id)` |
| `__init__` | method | `modules/lazy_loop.py:7181` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:7364` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7843` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:7961` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8110` | `def __init__(self)` |
| `__init__` | method | `modules/lazy_loop.py:8153` | `def __init__(self, store)` |
| `__init__` | method | `modules/lazy_loop.py:8307` | `def __init__(self, shell)` |
| `_absorb_reaction` | method | `modules/lazy_loop.py:4407` | `def _absorb_reaction(self, intent, command, output)` |
| `_agent_checkpoint` | method | `modules/lazy_loop.py:4696` | `def _agent_checkpoint(self, intent)` |
| `_agent_preflight` | method | `modules/lazy_loop.py:4722` | `def _agent_preflight(self, intent, command)` |
| `_agent_system_prompt` | method | `modules/lazy_loop.py:5067` | `def _agent_system_prompt(self, intent)` |
| `_agent_tools` | method | `modules/lazy_loop.py:4885` | `def _agent_tools(self, intent, executor, transcripts, budget, intercept, retry_state)` |
| `_agentic_try` | method | `modules/lazy_loop.py:5099` | `def _agentic_try(self, intent, outcome, transcripts, executor, budget, intercept, retry_state)` |
| `_apply_stored_bodies` | method | `modules/lazy_loop.py:6147` | `def _apply_stored_bodies(self, bodies)` |
| `_archive_discards` | method | `modules/lazy_loop.py:10123` | `def _archive_discards(self, task_id, last_results)` |
| `_asset_candidates` | function | `modules/lazy_loop.py:2133` | `def _asset_candidates(target)` |
| `_auto_approve` | method | `modules/lazy_loop.py:5208` | `def _auto_approve(self, command)` |
| `_auto_bind_body_hits` | method | `modules/lazy_loop.py:5545` | `def _auto_bind_body_hits(self, finding, seed)` |
| `_auto_enrich` | method | `modules/lazy_loop.py:9558` | `def _auto_enrich(self, task_id, graph, activity, limit)` |
| `_auto_retest` | method | `modules/lazy_loop.py:9594` | `def _auto_retest(self, task_id, graph, activity, traffic, executor, limit)` |
| `_block_signature` | method | `modules/lazy_loop.py:6215` | `def _block_signature(self, members, anchors, versions)` |
| `_bodies_path` | method | `modules/lazy_loop.py:6029` | `def _bodies_path(self)` |
| `_breaker_active` | method | `modules/lazy_loop.py:7460` | `def _breaker_active(self)` |
| `_broadcast_row` | method | `modules/lazy_loop.py:10824` | `def _broadcast_row(self, graph, node)` |
| `_candidates` | method | `modules/lazy_loop.py:3361` | `def _candidates(self)` |
| `_channel_encryption_key` | function | `modules/lazy_loop.py:483` | `def _channel_encryption_key()` |
| `_check_goals` | method | `modules/lazy_loop.py:10049` | `def _check_goals(self, task_id, graph, activity)` |
| `_close_shell_session` | method | `modules/lazy_loop.py:4858` | `def _close_shell_session(self)` |
| `_cold_path` | method | `modules/lazy_loop.py:6017` | `def _cold_path(self)` |
| `_command_in_scope` | method | `modules/lazy_loop.py:5536` | `def _command_in_scope(self, command)` |
| `_constraints` | method | `modules/lazy_loop.py:3160` | `def _constraints(self)` |
| `_content_versions` | method | `modules/lazy_loop.py:6207` | `def _content_versions(self)` |
| `_decrypt_channel_secret` | function | `modules/lazy_loop.py:537` | `def _decrypt_channel_secret(stored)` |
| `_delta_sink` | method | `modules/lazy_loop.py:3678` | `def _delta_sink(self)` |
| `_delta_sink` | method | `modules/lazy_loop.py:5435` | `def _delta_sink(self, intent_id)` |
| `_denied` | method | `modules/lazy_loop.py:3169` | `def _denied(self, text)` |
| `_denied` | method | `modules/lazy_loop.py:5197` | `def _denied(self, command)` |
| `_draft_report` | method | `modules/lazy_loop.py:6903` | `def _draft_report(self, node)` |
| `_drafts_ready_path` | method | `modules/lazy_loop.py:6899` | `def _drafts_ready_path(self)` |
| `_drain_steer` | method | `modules/lazy_loop.py:4711` | `def _drain_steer(self, intent)` |
| `_drain_triggers` | method | `modules/lazy_loop.py:9507` | `def _drain_triggers(self, task_id, graph)` |
| `_drop_event` | method | `modules/lazy_loop.py:2459` | `def _drop_event(cls, path, item_id)` |
| `_drop_wake_event` | function | `modules/lazy_loop.py:579` | `def _drop_wake_event(task_id)` |
| `_encrypt_channel_secret` | function | `modules/lazy_loop.py:499` | `def _encrypt_channel_secret(plaintext)` |
| `_engagement_decision` | method | `modules/lazy_loop.py:10062` | `def _engagement_decision(self, task_id, round_index, summary)` |
| `_evaluate_goal` | method | `modules/lazy_loop.py:9649` | `def _evaluate_goal(self, task_id)` |
| `_event_for` | method | `modules/lazy_loop.py:2442` | `def _event_for(cls, path, item_id)` |
| `_fact_memory_store` | method | `modules/lazy_loop.py:4385` | `def _fact_memory_store(self)` |
| `_failure_memory` | method | `modules/lazy_loop.py:4313` | `def _failure_memory(self)` |
| `_find` | function | `modules/lazy_loop.py:6236` | `def _find(value)` |
| `_finding_list` | method | `modules/lazy_loop.py:10720` | `def _finding_list(self, graph)` |
| `_finish` | method | `modules/lazy_loop.py:4228` | `def _finish(self, intent, outcome, transcripts, worker_tools, skipped_tools)` |
| `_foldable` | method | `modules/lazy_loop.py:6175` | `def _foldable(self, node)` |
| `_goals_met` | method | `modules/lazy_loop.py:10056` | `def _goals_met(self, task_id)` |
| `_group` | method | `modules/lazy_loop.py:6224` | `def _group(self, eligible)` |
| `_guard_step` | method | `modules/lazy_loop.py:4459` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_host_from_token` | function | `modules/lazy_loop.py:367` | `def _host_from_token(token)` |
| `_host_like_target` | function | `modules/lazy_loop.py:5809` | `def _host_like_target(target)` |
| `_intent_subtree` | method | `modules/lazy_loop.py:8950` | `def _intent_subtree(self, graph, intent_id)` |
| `_is_ip_literal` | function | `modules/lazy_loop.py:260` | `def _is_ip_literal(value)` |
| `_is_live_intent` | method | `modules/lazy_loop.py:6171` | `def _is_live_intent(self, node)` |
| `_is_scan_command` | function | `modules/lazy_loop.py:5800` | `def _is_scan_command(command)` |
| `_kill` | function | `modules/lazy_loop.py:446` | `def _kill()` |
| `_lab_scope_default` | method | `modules/lazy_loop.py:3900` | `def _lab_scope_default(self, target)` |
| `_lazy_policy` | function | `modules/lazy_loop.py:2984` | `def _lazy_policy()` |
| `_learn_os` | method | `modules/lazy_loop.py:4358` | `def _learn_os(self, intent, command, output)` |
| `_ledger_fresh_summary` | method | `modules/lazy_loop.py:3338` | `def _ledger_fresh_summary(self, summary)` |
| `_llm_candidates` | method | `modules/lazy_loop.py:3692` | `def _llm_candidates(self, existing)` |
| `_llm_error_reply` | function | `modules/lazy_loop.py:787` | `def _llm_error_reply(text)` |
| `_llm_quota_reply` | function | `modules/lazy_loop.py:795` | `def _llm_quota_reply(text)` |
| `_llm_steps` | method | `modules/lazy_loop.py:5304` | `def _llm_steps(self, intent, prior_text)` |
| `_load` | method | `modules/lazy_loop.py:2470` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7083` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7847` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:7965` | `def _load(self)` |
| `_load` | method | `modules/lazy_loop.py:8114` | `def _load(self)` |
| `_load_bodies` | method | `modules/lazy_loop.py:6033` | `def _load_bodies(self)` |
| `_load_cold` | method | `modules/lazy_loop.py:6021` | `def _load_cold(self)` |
| `_load_global` | method | `modules/lazy_loop.py:2205` | `def _load_global(self)` |
| `_load_json` | function | `modules/lazy_loop.py:747` | `def _load_json(path, default)` |
| `_load_task` | method | `modules/lazy_loop.py:2209` | `def _load_task(self)` |
| `_mask_prompt_context` | function | `modules/lazy_loop.py:6715` | `def _mask_prompt_context(text)` |
| `_match_gate_rule` | function | `modules/lazy_loop.py:2154` | `def _match_gate_rule(rule, target)` |
| `_maybe_import_inbox` | method | `modules/lazy_loop.py:10424` | `def _maybe_import_inbox(self)` |
| `_maybe_proxy_gc` | method | `modules/lazy_loop.py:10398` | `def _maybe_proxy_gc(self)` |
| `_maybe_selfupdate_check` | method | `modules/lazy_loop.py:10444` | `def _maybe_selfupdate_check(self)` |
| `_missing_tool` | method | `modules/lazy_loop.py:5220` | `def _missing_tool(self, command)` |
| `_noa_archive` | method | `modules/lazy_loop.py:6090` | `def _noa_archive(self, signature, members, anchors)` |
| `_noa_enabled` | function | `modules/lazy_loop.py:687` | `def _noa_enabled()` |
| `_normalize_refs` | method | `modules/lazy_loop.py:1785` | `def _normalize_refs(raw)` |
| `_now` | function | `modules/lazy_loop.py:729` | `def _now()` |
| `_open_shell_session` | method | `modules/lazy_loop.py:4787` | `def _open_shell_session(self, intent)` |
| `_origin_fact` | method | `modules/lazy_loop.py:3329` | `def _origin_fact(self)` |
| `_os_gate` | method | `modules/lazy_loop.py:4332` | `def _os_gate(self, intent, command)` |
| `_parts` | method | `modules/lazy_loop.py:8517` | `def _parts(self, task_id)` |
| `_persist` | method | `modules/lazy_loop.py:961` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1132` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:1870` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2605` | `def _persist(self)` |
| `_persist` | method | `modules/lazy_loop.py:2645` | `def _persist(self)` |
| `_policy_proposals` | function | `modules/lazy_loop.py:3006` | `def _policy_proposals(policy, target)` |
| `_prior_steps` | method | `modules/lazy_loop.py:3932` | `def _prior_steps(self, intent)` |
| `_reader` | function | `modules/lazy_loop.py:4809` | `def _reader()` |
| `_recall_facts` | method | `modules/lazy_loop.py:4400` | `def _recall_facts(self, query, k)` |
| `_record` | method | `modules/lazy_loop.py:7440` | `def _record(self, member, ok, text)` |
| `_record_ai_outcome` | method | `modules/lazy_loop.py:7540` | `def _record_ai_outcome(self, member, ok, live_log)` |
| `_record_raw` | method | `modules/lazy_loop.py:7795` | `def _record_raw(self, member, prompt, reply, ok, task_id, model_spec)` |
| `_refresh` | method | `modules/lazy_loop.py:2733` | `def _refresh(self)` |
| `_register_guardrails` | method | `modules/lazy_loop.py:8398` | `def _register_guardrails(self)` |
| `_register_loop_executor` | function | `modules/lazy_loop.py:424` | `def _register_loop_executor(executor)` |
| `_register_mediators` | method | `modules/lazy_loop.py:8387` | `def _register_mediators(self)` |
| `_remember_fact` | method | `modules/lazy_loop.py:4391` | `def _remember_fact(self, intent, command, output)` |
| `_reorder_with_ai` | method | `modules/lazy_loop.py:7498` | `def _reorder_with_ai(self, chain, live_log)` |
| `_reporter_reply` | method | `modules/lazy_loop.py:6958` | `def _reporter_reply(self, pool, chain, entry)` |
| `_request_bodies` | method | `modules/lazy_loop.py:6041` | `def _request_bodies(self, blocks, cold)` |
| `_resolved_command` | method | `modules/lazy_loop.py:5459` | `def _resolved_command(self, command)` |
| `_restrict_file` | function | `modules/lazy_loop.py:475` | `def _restrict_file(path)` |
| `_rl_rank` | method | `modules/lazy_loop.py:3604` | `def _rl_rank(self, out)` |
| `_rotated_chain` | method | `modules/lazy_loop.py:7469` | `def _rotated_chain(self, chain)` |
| `_run` | method | `modules/lazy_loop.py:5236` | `def _run(self, command, executor)` |
| `_run_one` | function | `modules/lazy_loop.py:9352` | `def _run_one(index_node)` |
| `_run_round_guarded` | method | `modules/lazy_loop.py:8416` | `def _run_round_guarded(self, task_id, round_index, workers, executor)` |
| `_run_worker_guarded` | method | `modules/lazy_loop.py:8446` | `def _run_worker_guarded(self, worker, node, executor)` |
| `_sanitize_step` | method | `modules/lazy_loop.py:5523` | `def _sanitize_step(self, intent, command)` |
| `_save` | method | `modules/lazy_loop.py:2474` | `def _save(self, payload)` |
| `_save_bodies` | method | `modules/lazy_loop.py:6037` | `def _save_bodies(self, payload)` |
| `_save_cold` | method | `modules/lazy_loop.py:6025` | `def _save_cold(self, payload)` |
| `_save_global` | method | `modules/lazy_loop.py:2216` | `def _save_global(self, block)` |
| `_save_json` | function | `modules/lazy_loop.py:757` | `def _save_json(path, payload)` |
| `_save_task` | method | `modules/lazy_loop.py:2220` | `def _save_task(self, payload)` |
| `_scope_allows_target` | method | `modules/lazy_loop.py:3871` | `def _scope_allows_target(self, target)` |
| `_scope_covers` | function | `modules/lazy_loop.py:2066` | `def _scope_covers(scope_kind, scope_value, asset)` |
| `_scope_host` | function | `modules/lazy_loop.py:2056` | `def _scope_host(value)` |
| `_seed_defaults` | method | `modules/lazy_loop.py:7375` | `def _seed_defaults(self)` |
| `_send_email` | method | `modules/lazy_loop.py:7253` | `def _send_email(channel, line, event)` |
| `_send_shell` | method | `modules/lazy_loop.py:4822` | `def _send_shell(self, command, intent, timeout_sec)` |
| `_settle_partial` | method | `modules/lazy_loop.py:5399` | `def _settle_partial(self, intent, transcripts, reason)` |
| `_signature` | function | `modules/lazy_loop.py:3270` | `def _signature(text)` |
| `_slug` | function | `modules/lazy_loop.py:772` | `def _slug(value)` |
| `_split_exclusive` | method | `modules/lazy_loop.py:8965` | `def _split_exclusive(self, graph, reachable)` |
| `_stage_enabled` | function | `modules/lazy_loop.py:9853` | `def _stage_enabled(_name)` |
| `_stall_intent` | method | `modules/lazy_loop.py:3759` | `def _stall_intent(self, existing)` |
| `_start_background_job` | method | `modules/lazy_loop.py:4755` | `def _start_background_job(self, command, intent, transcripts)` |
| `_steps_for` | method | `modules/lazy_loop.py:5597` | `def _steps_for(self, intent)` |
| `_store_path` | function | `modules/lazy_loop.py:734` | `def _store_path(name)` |
| `_structured_verdict` | method | `modules/lazy_loop.py:5937` | `def _structured_verdict(self, finding)` |
| `_sudo_guard` | method | `modules/lazy_loop.py:5473` | `def _sudo_guard(self, intent, command)` |
| `_sudo_unavailable` | function | `modules/lazy_loop.py:254` | `def _sudo_unavailable(output)` |
| `_sync_c2_board` | method | `modules/lazy_loop.py:10262` | `def _sync_c2_board(self, task_ids)` |
| `_sync_intel` | method | `modules/lazy_loop.py:9172` | `def _sync_intel(self, task_id, activity, force)` |
| `_target_as_asset` | function | `modules/lazy_loop.py:2116` | `def _target_as_asset(value)` |
| `_target_for` | method | `modules/lazy_loop.py:4305` | `def _target_for(self, intent)` |
| `_task_executed_commands` | method | `modules/lazy_loop.py:5500` | `def _task_executed_commands(self)` |
| `_technique_for` | method | `modules/lazy_loop.py:6768` | `def _technique_for(vulnclass, text)` |
| `_traffic_template` | function | `modules/lazy_loop.py:777` | `def _traffic_template(command)` |
| `_union` | function | `modules/lazy_loop.py:6242` | `def _union(left, right)` |
| `_unregister_loop_executor` | function | `modules/lazy_loop.py:430` | `def _unregister_loop_executor(executor)` |
| `_valid_nmap_port_spec` | function | `modules/lazy_loop.py:274` | `def _valid_nmap_port_spec(value)` |
| `_wake_event` | function | `modules/lazy_loop.py:569` | `def _wake_event(task_id)` |
| `_with_llm_steps` | method | `modules/lazy_loop.py:5286` | `def _with_llm_steps(self, intent, steps, prior_text)` |
| `_work` | function | `modules/lazy_loop.py:4767` | `def _work()` |
| `_work` | function | `modules/lazy_loop.py:6937` | `def _work()` |
| `_worker` | function | `modules/lazy_loop.py:6062` | `def _worker(work)` |
| `_wrapup_summary` | method | `modules/lazy_loop.py:9614` | `def _wrapup_summary(self, task_id, reason)` |
| `_write_draft` | method | `modules/lazy_loop.py:6974` | `def _write_draft(self, finding_id, report, evidence_version)` |
| `_writeback` | method | `modules/lazy_loop.py:5658` | `def _writeback(self, intent, transcripts, allow_finding)` |
| `abort` | method | `modules/lazy_loop.py:2407` | `def abort(self, task_id, cause, detail)` |
| `active_count` | method | `modules/lazy_loop.py:2702` | `def active_count(self, exclude)` |
| `add` | method | `modules/lazy_loop.py:2225` | `def add(self, kind, pattern, note, action)` |
| `add` | method | `modules/lazy_loop.py:2609` | `def add(self, text)` |
| `add` | method | `modules/lazy_loop.py:7087` | `def add(self, finding_id, kind, body)` |
| `add` | method | `modules/lazy_loop.py:7969` | `def add(self, name, scope)` |
| `add` | method | `modules/lazy_loop.py:8122` | `def add(self, name, goal)` |
| `add_channel` | method | `modules/lazy_loop.py:7193` | `def add_channel(self, kind, target, min_severity, extra)` |
| `add_constraint` | method | `modules/lazy_loop.py:2836` | `def add_constraint(self, task_id, ctype, text, scope)` |
| `add_edge` | method | `modules/lazy_loop.py:1229` | `def add_edge(self, src, dst, kind)` |
| `add_hint` | method | `modules/lazy_loop.py:8735` | `def add_hint(self, task_id, text)` |
| `add_intent` | method | `modules/lazy_loop.py:8753` | `def add_intent(self, task_id, summary, asset_ids, parent_ids, priority)` |
| `add_member` | method | `modules/lazy_loop.py:7404` | `def add_member(self, name, model, priority)` |
| `add_node` | method | `modules/lazy_loop.py:1144` | `def add_node(self, kind, text, state, priority, meta)` |
| `add_rule` | method | `modules/lazy_loop.py:1877` | `def add_rule(self, pattern, action, reason, priority)` |
| `add_scope` | method | `modules/lazy_loop.py:2855` | `def add_scope(self, task_id, kind, value, reason)` |
| `admission_check` | method | `modules/lazy_loop.py:10271` | `def admission_check(self, task_id)` |
| `advance_llm` | method | `modules/lazy_loop.py:2771` | `def advance_llm(self, task_id)` |
| `anchor` | method | `modules/lazy_loop.py:1242` | `def anchor(self, node_id, asset_id)` |
| `anchored_nodes` | method | `modules/lazy_loop.py:1257` | `def anchored_nodes(self, asset_id)` |
| `anchors_for` | method | `modules/lazy_loop.py:1253` | `def anchors_for(self, node_id)` |
| `apply_drafts` | method | `modules/lazy_loop.py:6992` | `def apply_drafts(self)` |
| `apply_profile` | method | `modules/lazy_loop.py:8342` | `def apply_profile(self, name)` |
| `archive` | method | `modules/lazy_loop.py:1832` | `def archive(self, label)` |
| `arm_exit_watchdog` | function | `modules/lazy_loop.py:436` | `def arm_exit_watchdog(seconds)` |
| `as_list` | method | `modules/lazy_loop.py:2632` | `def as_list(self)` |
| `ask` | method | `modules/lazy_loop.py:7894` | `def ask(self, task_id, question, pool, session)` |
| `audit` | method | `modules/lazy_loop.py:1971` | `def audit(self, limit, action, source, query)` |
| `beat` | method | `modules/lazy_loop.py:2392` | `def beat(self, task_id, workers)` |
| `bind` | method | `modules/lazy_loop.py:1754` | `def bind(self, finding_id, digest, graph, role, note)` |
| `bind` | method | `modules/lazy_loop.py:7865` | `def bind(self, agent, tool)` |
| `bind_shell` | method | `modules/lazy_loop.py:8383` | `def bind_shell(self, shell)` |
| `bindings` | method | `modules/lazy_loop.py:7860` | `def bindings(self, agent)` |
| `broadcast` | method | `modules/lazy_loop.py:10749` | `def broadcast(self, task_id, kinds, query, order, page, per_page, states)` |
| `broadcast_events` | method | `modules/lazy_loop.py:8702` | `def broadcast_events(self, task_id, cursor, batch)` |
| `build_prompt_context` | function | `modules/lazy_loop.py:6636` | `def build_prompt_context(task_id, graph, assets, store, budget, top)` |
| `by_template` | method | `modules/lazy_loop.py:1749` | `def by_template(self, template, limit)` |
| `channels` | method | `modules/lazy_loop.py:7185` | `def channels(self)` |
| `check` | method | `modules/lazy_loop.py:1919` | `def check(self, tool, command, tool_use_id, source, intent_id)` |
| `check` | method | `modules/lazy_loop.py:2354` | `def check(self, task_id)` |
| `children` | method | `modules/lazy_loop.py:1270` | `def children(self, node_id, kind)` |
| `claim_next` | method | `modules/lazy_loop.py:1442` | `def claim_next(self)` |
| `clear` | method | `modules/lazy_loop.py:1838` | `def clear(self)` |
| `clear` | method | `modules/lazy_loop.py:8252` | `def clear(self, task_id, session)` |
| `clear_steer` | method | `modules/lazy_loop.py:2891` | `def clear_steer(self, task_id, intent_id)` |
| `close` | method | `modules/lazy_loop.py:3860` | `def close(self)` |
| `cold_index` | method | `modules/lazy_loop.py:6492` | `def cold_index(self)` |
| `compact` | method | `modules/lazy_loop.py:6341` | `def compact(self, threshold, mode, debounce_sec)` |
| `compare_and_claim` | method | `modules/lazy_loop.py:1331` | `def compare_and_claim(self, node_id)` |
| `complete` | method | `modules/lazy_loop.py:2616` | `def complete(self, item_id)` |
| `complete` | method | `modules/lazy_loop.py:7555` | `def complete(self, prompt, max_tokens, empty_retries, members, task_id, on_delta)` |
| `constraint_block` | function | `modules/lazy_loop.py:6573` | `def constraint_block(constraints, scope)` |
| `context_budget` | method | `modules/lazy_loop.py:7731` | `def context_budget(self)` |
| `coverage` | method | `modules/lazy_loop.py:1020` | `def coverage(self, scope)` |
| `coverage_for` | method | `modules/lazy_loop.py:1054` | `def coverage_for(self, graph, scope)` |
| `covered_members` | method | `modules/lazy_loop.py:6288` | `def covered_members(self)` |
| `create` | method | `modules/lazy_loop.py:2649` | `def create(self, goal, description)` |
| `create_task` | method | `modules/lazy_loop.py:8522` | `def create_task(self, goal, description)` |
| `decide` | method | `modules/lazy_loop.py:2552` | `def decide(self, item_id, verdict)` |
| `decompose_goals` | function | `modules/lazy_loop.py:3086` | `def decompose_goals(goal_text, description)` |
| `dedupe_key` | method | `modules/lazy_loop.py:965` | `def dedupe_key(self, kind, value, parent_id)` |
| `delete` | method | `modules/lazy_loop.py:2693` | `def delete(self, task_id)` |
| `delete_goal` | method | `modules/lazy_loop.py:8807` | `def delete_goal(self, task_id, goal_id)` |
| `delete_intent` | method | `modules/lazy_loop.py:8841` | `def delete_intent(self, task_id, intent_id, mode, reason)` |
| `delete_task` | method | `modules/lazy_loop.py:10157` | `def delete_task(self, task_id)` |
| `dequeue_next` | method | `modules/lazy_loop.py:2722` | `def dequeue_next(self)` |
| `digest_overview` | method | `modules/lazy_loop.py:6526` | `def digest_overview(self)` |
| `drain_queue` | method | `modules/lazy_loop.py:10290` | `def drain_queue(self, max_tasks)` |
| `edit_goal` | method | `modules/lazy_loop.py:8795` | `def edit_goal(self, task_id, goal_id, text)` |
| `emit` | method | `modules/lazy_loop.py:1465` | `def emit(self, worker, kind, text, intent_id, tool_use_id)` |
| `emit` | method | `modules/lazy_loop.py:7291` | `def emit(self, task_id, event, data)` |
| `enqueue` | method | `modules/lazy_loop.py:2711` | `def enqueue(self, task_id)` |
| `enrich_asset` | function | `modules/lazy_loop.py:3123` | `def enrich_asset(value)` |
| `ensure_target` | method | `modules/lazy_loop.py:8467` | `def ensure_target(self, task_id, target, reason)` |
| `evaluate` | method | `modules/lazy_loop.py:2268` | `def evaluate(self, target)` |
| `evidence` | method | `modules/lazy_loop.py:1802` | `def evidence(self, finding_id, graph)` |
| `execute` | method | `modules/lazy_loop.py:3956` | `def execute(self, intent, executor, timeout_sec)` |
| `expand` | method | `modules/lazy_loop.py:6468` | `def expand(self, digest_id, role)` |
| `expired` | method | `modules/lazy_loop.py:2830` | `def expired(self, task_id)` |
| `export` | method | `modules/lazy_loop.py:1825` | `def export(self, path, limit)` |
| `export` | method | `modules/lazy_loop.py:7170` | `def export(self, path)` |
| `export_evidence` | method | `modules/lazy_loop.py:10493` | `def export_evidence(self, task_id, dest)` |
| `export_findings_report` | method | `modules/lazy_loop.py:10552` | `def export_findings_report(self, task_id, path, fmt)` |
| `export_task_traffic` | method | `modules/lazy_loop.py:10464` | `def export_task_traffic(self, task_id)` |
| `extract_constraint_items` | function | `modules/lazy_loop.py:2942` | `def extract_constraint_items(goal_text, description)` |
| `extract_scope_items` | function | `modules/lazy_loop.py:2910` | `def extract_scope_items(goal_text, description)` |
| `finalize` | method | `modules/lazy_loop.py:3662` | `def finalize(self, reason)` |
| `finding_severity` | function | `modules/lazy_loop.py:6725` | `def finding_severity(text, evidence)` |
| `finding_signature` | method | `modules/lazy_loop.py:1359` | `def finding_signature(self, text)` |
| `for_finding` | method | `modules/lazy_loop.py:7129` | `def for_finding(self, finding_id)` |
| `for_intent` | method | `modules/lazy_loop.py:1504` | `def for_intent(self, intent_id)` |
| `gc` | method | `modules/lazy_loop.py:7113` | `def gc(self, valid_findings)` |
| `get` | method | `modules/lazy_loop.py:999` | `def get(self, asset_id)` |
| `get` | method | `modules/lazy_loop.py:1172` | `def get(self, node_id)` |
| `get` | method | `modules/lazy_loop.py:1673` | `def get(self, digest)` |
| `get` | method | `modules/lazy_loop.py:2660` | `def get(self, task_id)` |
| `get` | method | `modules/lazy_loop.py:8142` | `def get(self, name)` |
| `get` | method | `modules/lazy_loop.py:8165` | `def get(self, task_id)` |
| `goal_met` | method | `modules/lazy_loop.py:9082` | `def goal_met(self, task_id, reason)` |
| `graph_context` | method | `modules/lazy_loop.py:10942` | `def graph_context(self, task_id, top)` |
| `graph_overview` | method | `modules/lazy_loop.py:10687` | `def graph_overview(self, task_id)` |
| `graph_state` | function | `modules/lazy_loop.py:4955` | `def graph_state()` |
| `has_finding` | method | `modules/lazy_loop.py:1365` | `def has_finding(self, text)` |
| `health` | method | `modules/lazy_loop.py:7720` | `def health(self)` |
| `heartbeat` | method | `modules/lazy_loop.py:2374` | `def heartbeat(self, task_id)` |
| `history` | method | `modules/lazy_loop.py:2500` | `def history(self, page, per_page, states, query)` |
| `history` | method | `modules/lazy_loop.py:7940` | `def history(self, task_id, session, limit)` |
| `hot_set` | method | `modules/lazy_loop.py:6181` | `def hot_set(self)` |
| `ingest_proxy_traffic` | method | `modules/lazy_loop.py:10318` | `def ingest_proxy_traffic(self, task_id, limit)` |
| `insert` | method | `modules/lazy_loop.py:969` | `def insert(self, kind, value, parent_id, meta, task_id)` |
| `job_output` | function | `modules/lazy_loop.py:4986` | `def job_output(job_id)` |
| `job_status` | function | `modules/lazy_loop.py:4978` | `def job_status(job_id)` |
| `judge_command` | function | `modules/lazy_loop.py:854` | `def judge_command(command, background, fail_action)` |
| `kill` | method | `modules/lazy_loop.py:2875` | `def kill(self, task_id, intent_id)` |
| `killed` | method | `modules/lazy_loop.py:2904` | `def killed(self, task_id, intent_id)` |
| `limits` | method | `modules/lazy_loop.py:2290` | `def limits(self, task_id)` |
| `list` | method | `modules/lazy_loop.py:1003` | `def list(self, kind)` |
| `list` | method | `modules/lazy_loop.py:1261` | `def list(self, kind, state)` |
| `list` | method | `modules/lazy_loop.py:2264` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:2664` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:7978` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8012` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8118` | `def list(self)` |
| `list` | method | `modules/lazy_loop.py:8169` | `def list(self, category)` |
| `list_facts` | method | `modules/lazy_loop.py:1391` | `def list_facts(self, query, limit, hot_full)` |
| `list_tasks` | method | `modules/lazy_loop.py:8601` | `def list_tasks(self)` |
| `llm_state` | method | `modules/lazy_loop.py:2765` | `def llm_state(self, task_id)` |
| `load_intel_scores` | function | `modules/lazy_loop.py:3034` | `def load_intel_scores()` |
| `log` | method | `modules/lazy_loop.py:8227` | `def log(self, task_id, limit, session)` |
| `lookup` | method | `modules/lazy_loop.py:1999` | `def lookup(self, tool_use_id)` |
| `loop_exiting` | function | `modules/lazy_loop.py:419` | `def loop_exiting()` |
| `loop_graph` | method | `modules/lazy_loop.py:10873` | `def loop_graph(self, task_id)` |
| `mark_tested` | method | `modules/lazy_loop.py:1010` | `def mark_tested(self, asset_id)` |
| `match` | method | `modules/lazy_loop.py:7982` | `def match(self, value)` |
| `members` | method | `modules/lazy_loop.py:7399` | `def members(self)` |
| `next_pending` | method | `modules/lazy_loop.py:2625` | `def next_pending(self)` |
| `noa_archives` | method | `modules/lazy_loop.py:6122` | `def noa_archives(self, limit)` |
| `node_detail` | method | `modules/lazy_loop.py:1375` | `def node_detail(self, node_id)` |
| `note_trigger` | method | `modules/lazy_loop.py:2423` | `def note_trigger(self, task_id, trigger_id)` |
| `on_planner_round` | method | `modules/lazy_loop.py:6300` | `def on_planner_round(self)` |
| `orchestrate` | method | `modules/lazy_loop.py:8494` | `def orchestrate(self, goal, task_id, target, max_rounds, workers, timeout_sec, executor)` |
| `overview` | method | `modules/lazy_loop.py:1284` | `def overview(self)` |
| `parents` | method | `modules/lazy_loop.py:1277` | `def parents(self, node_id, kind)` |
| `parse_judge_output` | function | `modules/lazy_loop.py:826` | `def parse_judge_output(raw)` |
| `pause` | method | `modules/lazy_loop.py:2680` | `def pause(self, task_id)` |
| `pause_intent` | method | `modules/lazy_loop.py:8986` | `def pause_intent(self, task_id, intent_id)` |
| `pause_task` | method | `modules/lazy_loop.py:8629` | `def pause_task(self, task_id, reason)` |
| `pending` | method | `modules/lazy_loop.py:1437` | `def pending(self)` |
| `pending` | method | `modules/lazy_loop.py:2496` | `def pending(self)` |
| `persist` | method | `modules/lazy_loop.py:1176` | `def persist(self)` |
| `plan` | method | `modules/lazy_loop.py:3177` | `def plan(self, triggers)` |
| `plausible_command` | function | `modules/lazy_loop.py:168` | `def plausible_command(command)` |
| `preview_delete_intent` | method | `modules/lazy_loop.py:8818` | `def preview_delete_intent(self, task_id, intent_id)` |
| `prove_goal` | method | `modules/lazy_loop.py:10016` | `def prove_goal(self, task_id, goal_id, evidence_id, reason)` |
| `proxy_env` | method | `modules/lazy_loop.py:10241` | `def proxy_env(self)` |
| `proxy_start` | method | `modules/lazy_loop.py:10191` | `def proxy_start(self, host, port, task_id, trust, upstream)` |
| `proxy_status` | method | `modules/lazy_loop.py:10235` | `def proxy_status(self)` |
| `proxy_stop` | method | `modules/lazy_loop.py:10227` | `def proxy_stop(self)` |
| `queue` | method | `modules/lazy_loop.py:2706` | `def queue(self)` |
| `ranked` | method | `modules/lazy_loop.py:7068` | `def ranked(self)` |
| `raw_entries` | method | `modules/lazy_loop.py:7748` | `def raw_entries(self, limit)` |
| `raw_entries_for_task` | method | `modules/lazy_loop.py:7762` | `def raw_entries_for_task(self, task_id, limit)` |
| `read` | method | `modules/lazy_loop.py:1490` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:1620` | `def read(self, limit)` |
| `read` | method | `modules/lazy_loop.py:7133` | `def read(self, evidence_id, offset, length)` |
| `rebind` | method | `modules/lazy_loop.py:3836` | `def rebind(self, assets, graph, activity, traffic, guard, store, shell)` |
| `record` | method | `modules/lazy_loop.py:1598` | `def record(self, kind, command, output, meta)` |
| `record_call` | method | `modules/lazy_loop.py:7446` | `def record_call(self, member, ok, text)` |
| `record_fact` | method | `modules/lazy_loop.py:1407` | `def record_fact(self, text, evidence, confidence, intent_id, asset_ids)` |
| `record_fact` | function | `modules/lazy_loop.py:4922` | `def record_fact(text)` |
| `record_fact` | method | `modules/lazy_loop.py:9092` | `def record_fact(self, task_id, text, evidence, intent_id)` |
| `record_raw` | method | `modules/lazy_loop.py:7736` | `def record_raw(self)` |
| `record_round` | method | `modules/lazy_loop.py:2336` | `def record_round(self, task_id)` |
| `record_toolcall` | method | `modules/lazy_loop.py:2324` | `def record_toolcall(self, task_id, intent_id)` |
| `record_verdict` | method | `modules/lazy_loop.py:9099` | `def record_verdict(self, task_id, finding_id, verdict, note)` |

Next: [SYMBOLS_p17.md](SYMBOLS_p17.md)
