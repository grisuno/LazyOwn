# Subsystem: modules (page 8 of 17)
Previous: [KB_modules_p7.md](KB_modules_p7.md)

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
- Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/lazy_cve_feed.py`, `modules/loop_triggers.py`

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


Next: [KB_modules_p9.md](KB_modules_p9.md)
