# Subsystem: modules (page 8 of 17)
Previous: [KB_modules_p7.md](KB_modules_p7.md)

## modules/lazy_checks.py
- Doc: Validation plans as data: re-read observed checks through version math.
- Layer: utility
- Language: py
- Symbols:
  - `extract_version` (function, line 30) `def extract_version(text)`
  - `extract_cve` (function, line 51) `def extract_cve(text)`
  - `interpret_checks` (function, line 57) `def interpret_checks(checks, cve, stored_version, ranges)`
  - `_range_says` (function, line 105) `def _range_says(version, ranges)`
- Depends on: `modules/lazy_heat.py`
- Imported by: `tests/test_lazy_checks.py`

## modules/lazy_cli_bridge.py
- Doc: Full CLI catalog for the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `_source_files` (function, line 74) `def _source_files()`
  - `_source_mtimes` (function, line 82) `def _source_mtimes()`
  - `_discover` (function, line 93) `def _discover()`
  - `cli_verbs` (function, line 106) `def cli_verbs()`
  - `is_cli_verb` (function, line 125) `def is_cli_verb(name)`
  - `phase_for` (function, line 131) `def phase_for(verb)`
  - `risk_for` (function, line 140) `def risk_for(verb)`
  - `needs_target_for` (function, line 150) `def needs_target_for(verb)`
  - `build_cli_command` (function, line 158) `def build_cli_command(verb, target)`
  - `search_cli_verbs` (function, line 185) `def search_cli_verbs(query, phase, limit)`
  - `cli_catalog_for_phase` (function, line 211) `def cli_catalog_for_phase(phase, limit)`
  - `catalog_cli_for_phase` (function, line 219) `def catalog_cli_for_phase(limit)`
  - `full_cli_enabled` (function, line 253) `def full_cli_enabled()`
  - `set_full_cli` (function, line 276) `def set_full_cli(enabled)`
- Depends on: `core/config.py`, `modules/killchain.py`, `modules/verb_catalog.py`
- Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/chain_distill.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/verb_catalog.py`, `tests/test_loop_cli_catalog.py`

## modules/lazy_creds.py
- Doc: Default-credential knowledge base for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `CredRow` (class, line 30) `class CredRow`
  - `load` (function, line 39) `def load()`
  - `search` (function, line 63) `def search(query)`
  - `candidates` (function, line 79) `def candidates(limit)`
  - `count` (function, line 96) `def count()`
  - `as_lines` (function, line 101) `def as_lines(rows)`
  - `export_pairs` (function, line 106) `def export_pairs(path, limit)`

## modules/lazy_cve_feed.py
- Doc: Keyless CVE intelligence feeds and version-aware service correlation.
- Layer: utility
- Language: py
- Symbols:
  - `_env_flag` (function, line 90) `def _env_flag(name, default)`
  - `_cache_path` (function, line 95) `def _cache_path(name)`
  - `_cache_fresh` (function, line 104) `def _cache_fresh(path, ttl_sec)`
  - `_fetch` (function, line 112) `def _fetch(url)`
  - `_store_bytes` (function, line 134) `def _store_bytes(name, payload)`
  - `_store_json` (function, line 142) `def _store_json(name, data)`
  - `_load_json` (function, line 150) `def _load_json(name)`
  - `load_kev` (function, line 158) `def load_kev(force)`
  - `load_epss` (function, line 192) `def load_epss(force)`
  - `_exploit_cves_from_text` (function, line 228) `def _exploit_cves_from_text(text)`
  - `load_exploit_cves` (function, line 233) `def load_exploit_cves(force)`
  - `load_msf_cves` (function, line 257) `def load_msf_cves(force)`
  - `_osv_cache_path` (function, line 281) `def _osv_cache_path(product)`
  - `fetch_product_advisories` (function, line 291) `def fetch_product_advisories(product, force)`
  - `cve_intel` (function, line 360) `def cve_intel(cve_id, feeds, allow_network)`
  - `_advisory_cve_id` (function, line 398) `def _advisory_cve_id(advisory)`
  - `_advisory_cvss` (function, line 407) `def _advisory_cvss(advisory)`
  - `_advisory_matches_product` (function, line 421) `def _advisory_matches_product(advisory, banner_words)`
  - `correlate` (function, line 438) `def correlate(product, version, allow_network)`
  - `convert_osv_ranges` (function, line 515) `def convert_osv_ranges(affected)`
  - `_cached_advisories` (function, line 544) `def _cached_advisories()`
  - `range_for_cve` (function, line 565) `def range_for_cve(cve_id, allow_network)`
  - `load_kev_matches` (function, line 594) `def load_kev_matches(product, feeds)`
  - `hot_matches` (function, line 636) `def hot_matches(services, allow_network)`
  - `refresh_feeds_async` (function, line 680) `def refresh_feeds_async(products)`
  - `_worker` (function, line 696) `def _worker()`
- Depends on: `modules/lazy_heat.py`
- Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/lazy_hostscore.py`, `tests/test_lazy_checks.py`

## modules/lazy_engine.py
- Doc: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- Layer: utility
- Language: py
- Symbols:
  - `LazyEngine` (class, line 56) `class LazyEngine(LazyLoopEngine)`
- Depends on: `modules/lazy_loop.py`
- Imported by: `cli/commands/lazyloop.py`, `cli/commands/lazyops.py`, `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `cli/orchestrator_assets_tabs.py`, `cli/session_brief.py`, `modules/lazy_loop.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/llm_orchestrator.py`, `modules/tools/loop_smoke.py`, `modules/tools/monitor_smoke.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_worker_safety.py`, `tests/test_llm_orchestrator.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_broadcast.py`, `tests/test_loop_cold_overview.py`, `tests/test_loop_force_graph.py`, `tests/test_loop_guard_audit.py`, `tests/test_loop_intent_delete.py`, `tests/test_loop_llm_resilience.py`, `tests/test_loop_scope_traffic_evidence.py`, `tests/test_loop_spawn_side.py`, `tests/test_loop_supervision.py`, `tests/test_loop_worker_traces.py`, `tests/test_module_registry_bridge.py`, `tests/test_session_brief.py`, `tests/test_sink_chain_feed.py`, `tests/test_world_diff_retest.py`

## modules/lazy_findings.py
- Doc: Engagement findings ledger: state machine plus reproducible evidence.
- Layer: utility
- Language: py
- Symbols:
  - `FindingValidationError` (class, line 60) `class FindingValidationError(ValueError)`
  - `LedgerLimits` (class, line 65) `class LedgerLimits`
  - `engagement_id_valid` (function, line 91) `def engagement_id_valid(value)`
  - `technique_id_valid` (function, line 103) `def technique_id_valid(value)`
  - `severity_tier` (function, line 116) `def severity_tier(severity)`
  - `level_for_state_uplift` (function, line 138) `def level_for_state_uplift(level, state)`
  - `evidence_reject_reason` (function, line 156) `def evidence_reject_reason(state, evidence, min_output)`
  - `state_counts` (function, line 191) `def state_counts(rows)`
  - `metadata_level` (function, line 217) `def metadata_level(payload)`
  - `row_from_event` (function, line 230) `def row_from_event(payload, limits)`
  - `evidence_supported` (function, line 281) `def evidence_supported(evidence, min_output)`
  - `_row_from_verdict` (function, line 294) `def _row_from_verdict(payload, verdict, bounds)`
  - `_base_row` (function, line 344) `def _base_row(payload, bounds)`
  - `discard_row` (function, line 382) `def discard_row(reason, command, output, technique_id, engagement_id, target)`
  - `normalize_finding` (function, line 429) `def normalize_finding(row, limits)`
  - `build_handoff` (function, line 481) `def build_handoff(rows, status, rounds)`
  - `_now_iso` (function, line 534) `def _now_iso()`
  - `FindingsLedger` (class, line 539) `class FindingsLedger`
  - `clamped` (method, line 81) `def clamped(self)`
  - `__init__` (method, line 542) `def __init__(self, engagement_id, base_dir, limits, scrub)`
  - `file_path` (method, line 569) `def file_path(self)`
  - `normalize` (method, line 573) `def normalize(self, row)`
  - `append` (method, line 606) `def append(self, row)`
  - `read` (method, line 636) `def read(self, cursor, limit)`
  - `rows` (method, line 660) `def rows(self)`
  - `history` (method, line 684) `def history(self, finding_ref)`
  - `latest_state` (method, line 696) `def latest_state(self, finding_ref)`
- Depends on: `core/hardening.py`
- Imported by: `tests/test_findings_gate.py`, `tests/test_lazy_findings.py`

## modules/lazy_heat.py
- Doc: Heat tiers and version math for CVE correlation.
- Layer: utility
- Language: py
- Symbols:
  - `classify_heat` (function, line 68) `def classify_heat(kev, epss, exploit, cvss)`
  - `match_heat` (function, line 91) `def match_heat(tier, cvss, verdict, distro_status)`
  - `parse_version` (function, line 118) `def parse_version(value, strict)`
  - `compare_versions` (function, line 154) `def compare_versions(a, b)`
  - `version_in_range` (function, line 162) `def version_in_range(ver, rng)`
  - `cvss3_base_score` (function, line 204) `def cvss3_base_score(vector)`
  - `product_token` (function, line 246) `def product_token(value)`
  - `token_matches` (function, line 269) `def token_matches(haystack, needle)`
  - `parse_distro_revision` (function, line 303) `def parse_distro_revision(banner)`
  - `backport_status` (function, line 342) `def backport_status(banner, fixed_revision)`
  - `label_for` (function, line 370) `def label_for(status, fixed_revision)`
- Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/lazy_checks.py`, `modules/lazy_cve_feed.py`, `modules/lazy_match_policy.py`, `modules/loop_triggers.py`

## modules/lazy_hostscore.py
- Doc: Host heat score: deterministic 0-100 priority for every known host.
- Layer: utility
- Language: py
- Symbols:
  - `score_host` (function, line 34) `def score_host(inputs)`
  - `rescore` (function, line 96) `def rescore(sessions_dir, allow_network, now)`
  - `_persist` (function, line 182) `def _persist(table, sessions_dir, now)`
  - `load_scores` (function, line 193) `def load_scores(sessions_dir)`
  - `_add` (function, line 49) `def _add(label, points)`
- Depends on: `modules/lazy_cve_feed.py`, `modules/lazy_world_diff.py`, `modules/world_model.py`
- Imported by: `modules/lazy_loop.py`, `tests/test_lazy_hostscore.py`

## modules/lazy_installer.py
- Doc: Capability installer for the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `installer_enabled` (function, line 41) `def installer_enabled()`
  - `set_installer_enabled` (function, line 58) `def set_installer_enabled(enabled)`
  - `install_command_for` (function, line 70) `def install_command_for(tool)`
  - `intent_for` (function, line 75) `def intent_for(tool)`
  - `tool_from_intent` (function, line 80) `def tool_from_intent(text)`
  - `steps_for_install` (function, line 88) `def steps_for_install(text)`
- Depends on: `core/config.py`, `modules/auto_registry.py`
- Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`

## modules/lazy_intel.py
- Doc: Intel feed from the Lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `_now` (function, line 30) `def _now()`
  - `_log_path` (function, line 35) `def _log_path()`
  - `_mask` (function, line 41) `def _mask(text)`
  - `_append` (function, line 79) `def _append(record)`
  - `infer_source` (function, line 88) `def infer_source(command, intent_text)`
  - `describe_command` (function, line 114) `def describe_command(command)`
  - `record_routing_decision` (function, line 129) `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)`
  - `record_routing_outcome` (function, line 169) `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)`
  - `read_decisions` (function, line 211) `def read_decisions(task_id, limit)`
  - `mask_configured` (function, line 237) `def mask_configured(text)`
  - `stack_signature` (function, line 272) `def stack_signature(assets)`
  - `_is_ip_literal` (function, line 292) `def _is_ip_literal(value)`
  - `fuse_routing_decisions` (function, line 303) `def fuse_routing_decisions(task_id)`
  - `export_spans` (function, line 342) `def export_spans(task_id, out)`
- Depends on: `core/config.py`, `modules/lazy_cli_bridge.py`, `modules/mediation/__init__.py`, `modules/world_model.py`, `utils.py`
- Imported by: `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/mediation/intel_mediator.py`, `modules/sinks/routing.py`, `tests/test_loop_supervision.py`, `tests/test_mediation.py`

## modules/lazy_ledger.py
- Doc: Freshness ledger: TTL windows per verb and target for the loop worker.
- Layer: utility
- Language: py
- Symbols:
  - `window_for` (function, line 32) `def window_for(verb)`
  - `ledger_key` (function, line 53) `def ledger_key(verb, target)`
  - `key_from_command` (function, line 58) `def key_from_command(command, target)`
  - `_addon_run_pair` (function, line 89) `def _addon_run_pair(rest)`
  - `_path` (function, line 114) `def _path(sessions_dir)`
  - `_load` (function, line 121) `def _load(sessions_dir)`
  - `json_load` (function, line 133) `def json_load(path)`
  - `fresh` (function, line 140) `def fresh(verb, target, now, sessions_dir)`
  - `record` (function, line 164) `def record(verb, target, ok, now, sessions_dir)`
  - `stale_first` (function, line 191) `def stale_first(catalog, now, sessions_dir)`
  - `_sort_key` (function, line 209) `def _sort_key(pair)`
- Depends on: `modules/lazy_loop.py`
- Imported by: `modules/lazy_loop.py`, `modules/sinks/routing.py`, `tests/test_lazy_ledger.py`


Next: [KB_modules_p9.md](KB_modules_p9.md)
