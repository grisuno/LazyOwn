# Subsystem: modules (page 9 of 19)
Previous: [KB_modules_p8.md](KB_modules_p8.md)

## modules/lazy_feedmatch.py
- Doc: Exploit feed matching for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `FeedEntry` (class, line 73) `class FeedEntry`
  - `Sighting` (class, line 98) `class Sighting`
  - `ExploitSighting` (class, line 123) `class ExploitSighting`
  - `load_feed` (function, line 151) `def load_feed(path)`
  - `_map_kev_row` (function, line 187) `def _map_kev_row(item)`
  - `parse_feed` (function, line 210) `def parse_feed(entries)`
  - `is_os_sighting` (function, line 248) `def is_os_sighting(name)`
  - `entry_matches_product` (function, line 262) `def entry_matches_product(entry, product)`
  - `version_in_ranges` (function, line 280) `def version_in_ranges(version, ranges)`
  - `_fixed_key` (function, line 316) `def _fixed_key(rng)`
  - `feed_tier` (function, line 325) `def feed_tier(entry)`
  - `bind_sighting` (function, line 337) `def bind_sighting(sighting, entries)`
  - `unversioned_leads` (function, line 388) `def unversioned_leads(sightings)`
  - `live_bindings` (function, line 411) `def live_bindings(sighting, allow_network)`
  - `_references` (function, line 464) `def _references(raw)`
  - `_cvss` (function, line 470) `def _cvss(value)`
  - `_float` (function, line 478) `def _float(value)`
  - `feed_fingerprint` (function, line 486) `def feed_fingerprint(entries)`
- Depends on: `modules/lazy_cve_feed.py`, `modules/lazy_heat.py`
- Imported by: `modules/lazy_exposure.py`, `modules/lazy_inventory.py`, `modules/lazy_sentinel.py`, `tests/test_lazy_exposure.py`, `tests/test_lazy_feedmatch.py`, `tests/test_lazy_sentinel.py`

## modules/lazy_finalizer.py
- Doc: Evidence-gated finalization for the autonomous loop and apt_chain.
- Layer: utility
- Language: py
- Symbols:
  - `FinalizerDecision` (class, line 35) `class FinalizerDecision`
  - `decide` (function, line 72) `def decide(status, candidate_verdict, facts, findings, confirmed, tested, pending_approvals, pending_plan_steps)`
  - `to_dict` (method, line 58) `def to_dict(self)`
- Imported by: `tests/test_chain_finalizer.py`

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
  - `classify_heat` (function, line 71) `def classify_heat(kev, epss, exploit, cvss)`
  - `match_heat` (function, line 94) `def match_heat(tier, cvss, verdict, distro_status)`
  - `parse_version` (function, line 121) `def parse_version(value, strict)`
  - `compare_versions` (function, line 157) `def compare_versions(a, b)`
  - `version_in_range` (function, line 165) `def version_in_range(ver, rng)`
  - `cvss3_base_score` (function, line 207) `def cvss3_base_score(vector)`
  - `product_token` (function, line 249) `def product_token(value)`
  - `token_matches` (function, line 272) `def token_matches(haystack, needle)`
  - `parse_distro_revision` (function, line 306) `def parse_distro_revision(banner)`
  - `backport_status` (function, line 345) `def backport_status(banner, fixed_revision)`
  - `heat_of_severity` (function, line 373) `def heat_of_severity(severity)`
  - `heat_rank` (function, line 392) `def heat_rank(tier)`
  - `host_heat` (function, line 404) `def host_heat(tier_values, severity_levels, unscanned)`
  - `hottest` (function, line 424) `def hottest(tier_values)`
  - `label_for` (function, line 438) `def label_for(status, fixed_revision)`
- Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/lazy_checks.py`, `modules/lazy_cve_feed.py`, `modules/lazy_exposure.py`, `modules/lazy_feedmatch.py`, `modules/lazy_match_policy.py`, `modules/loop_triggers.py`, `modules/sinks/lazy_intel.py`, `tests/test_lazy_feedmatch.py`

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

## modules/lazy_inventory.py
- Doc: Host-reported inventory for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `inventory_blob` (function, line 49) `def inventory_blob(platform)`
  - `parse_blob_output` (function, line 61) `def parse_blob_output(text, platform)`
  - `_LINUX_LINE` (function, line 87) `def _LINUX_LINE(line)`
  - `_WINDOWS_LINE` (function, line 104) `def _WINDOWS_LINE(line)`
  - `_clean_entry` (function, line 114) `def _clean_entry(product, version, os_hint)`
  - `to_sightings` (function, line 133) `def to_sightings(entries, host)`
  - `os_platform_of` (function, line 157) `def os_platform_of(entries)`
- Depends on: `modules/lazy_feedmatch.py`

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


Next: [KB_modules_p10.md](KB_modules_p10.md)
