# Subsystem: modules (page 8 of 18)
Previous: [KB_modules_p7.md](KB_modules_p7.md)

## modules/kivi.py
- Layer: utility
- Language: py
- Symbols:
  - `ReverseShellApp` (class, line 11) `class ReverseShellApp(App)`
  - `build` (method, line 12) `def build(self)`
  - `connect_to_server` (method, line 27) `def connect_to_server(self, instance)`

## modules/lab_runtime.py
- Doc: Lab runtime: Docker lifecycle for practice targets and cyber ranges.
- Layer: utility
- Language: py
- Symbols:
  - `docker_available` (function, line 93) `def docker_available()`
  - `_docker` (function, line 107) `def _docker()`
  - `running_containers` (function, line 115) `def running_containers()`
  - `existing_containers` (function, line 131) `def existing_containers()`
  - `running_range_containers` (function, line 148) `def running_range_containers()`
  - `container_name` (function, line 164) `def container_name(scenario)`
  - `container_ip` (function, line 169) `def container_ip(container_name)`
  - `ensure_web` (function, line 183) `def ensure_web(scenario, name)`
  - `_ensure_ad_lab` (function, line 197) `def _ensure_ad_lab(scenario, name)`
  - `apply_gym_migrations` (function, line 242) `def apply_gym_migrations(name)`
  - `start` (function, line 250) `def start(scenario)`
  - `stop` (function, line 304) `def stop(scenario)`
  - `stop_all` (function, line 322) `def stop_all()`
  - `range_compose` (function, line 340) `def range_compose(profile)`
  - `start_range` (function, line 349) `def start_range(profile)`
  - `stop_range` (function, line 368) `def stop_range(profile)`
  - `stop_ranges` (function, line 379) `def stop_ranges()`
  - `_docker_compose` (function, line 412) `def _docker_compose(args)`
  - `ensure_range_secret` (function, line 420) `def ensure_range_secret(profile_dir)`
- Depends on: `modules/metasploitable_migrations.py`
- Imported by: `tests/test_bdd_infra_range_report.py`, `tests/test_infra_disposable.py`

## modules/lazy_agent.py
- Doc: Agentic tool-calling bridge for the loop and the main agent.
- Layer: utility
- Language: py
- Symbols:
  - `model_timeout_sec` (function, line 41) `def model_timeout_sec()`
  - `tool_calling_enabled` (function, line 57) `def tool_calling_enabled()`
  - `max_iterations` (function, line 72) `def max_iterations()`
  - `resolve_agentic_model` (function, line 83) `def resolve_agentic_model(exclude)`
  - `_enable_streaming` (function, line 123) `def _enable_streaming(runner, on_event)`
  - `ObservableAgentRunner` (class, line 145) `class ObservableAgentRunner(AgentRunner)`
  - `_json_default` (function, line 221) `def _json_default(value)`
  - `_deep_clean` (function, line 237) `def _deep_clean(value, _depth)`
  - `_json_safe` (function, line 253) `def _json_safe(messages)`
  - `ConversationStore` (class, line 261) `class ConversationStore`
  - `register_tools` (function, line 322) `def register_tools(runner, specs)`
  - `run_worker_session` (function, line 335) `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)`
  - `run_main_session` (function, line 374) `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)`
  - `run_external_opencode` (function, line 396) `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)`
  - `run_external_hermes` (function, line 472) `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)`
  - `_session_from_line` (function, line 556) `def _session_from_line(line)`
  - `_process_watchdog` (function, line 578) `def _process_watchdog(timeout_sec, process)`
  - `__init__` (method, line 148) `def __init__(self, model, system_prompt, max_iterations, on_event)`
  - `_process_tool_call` (method, line 159) `def _process_tool_call(self, tool_call)`
  - `run` (method, line 168) `def run(self, user_input)`
  - `_call_model` (method, line 174) `def _call_model(self)`
  - `__init__` (method, line 264) `def __init__(self, task_id)`
  - `_load` (method, line 269) `def _load(self)`
  - `intent_messages` (method, line 273) `def intent_messages(self, intent_id)`
  - `save_intent` (method, line 278) `def save_intent(self, intent_id, messages)`
  - `session` (method, line 287) `def session(self, session_id)`
  - `sessions` (method, line 291) `def sessions(self)`
  - `save_session` (method, line 305) `def save_session(self, session_id, messages, title)`
  - `reset_intents` (method, line 315) `def reset_intents(self)`
  - `_kill` (function, line 583) `def _kill()`
  - `_invoke` (function, line 190) `def _invoke()`
  - `_tick` (function, line 196) `def _tick()`
- Depends on: `core/config.py`, `modules/__init__.py`, `modules/agent_runner.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop_ai_bridge.py`
- Imported by: `cli/commands/lazyops.py`, `tests/conftest.py`, `tests/test_lazy_agent.py`

## modules/lazy_autofire.py
- Doc: Lazy autofire: exploit intelligence closing the loop into chains.
- Layer: utility
- Language: py
- Symbols:
  - `autofire_armed` (function, line 41) `def autofire_armed(payload)`
  - `consider_report` (function, line 53) `def consider_report(report, chains_dir, state_path, armed, now)`
  - `fire_from_file` (function, line 105) `def fire_from_file(target, feed_path)`
  - `sweep_state` (function, line 127) `def sweep_state(state_path, now)`
  - `status` (function, line 147) `def status(payload, state_path)`
  - `_fire_matches` (function, line 166) `def _fire_matches(report)`
  - `_cooldown_filter` (function, line 180) `def _cooldown_filter(fires, state, target, moment, chains_dir)`
  - `_existing_chain_tokens` (function, line 215) `def _existing_chain_tokens(chains_dir, slug)`
  - `_chain_data` (function, line 225) `def _chain_data(target, fires)`
  - `_load_state` (function, line 281) `def _load_state(path)`
  - `_save_state` (function, line 291) `def _save_state(path, state)`
  - `_stamp_cooldown` (function, line 305) `def _stamp_cooldown(state, target, cves, moment)`
  - `_slug` (function, line 312) `def _slug(text)`
- Depends on: `modules/__init__.py`, `modules/chain_synth.py`, `modules/lazy_probes.py`
- Imported by: `tests/test_loop_fire_pending.py`

## modules/lazy_blindspot.py
- Doc: Blindspot review contract for the lazy autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `BlindspotFinding` (class, line 55) `class BlindspotFinding`
  - `parse_blindspots` (function, line 82) `def parse_blindspots(raw)`
  - `_fence` (function, line 130) `def _fence(text, limit)`
  - `build_blindspot_prompt` (function, line 145) `def build_blindspot_prompt(goal, context)`
  - `BlindspotReview` (class, line 159) `class BlindspotReview`
  - `as_hint` (method, line 70) `def as_hint(self)`
  - `__init__` (method, line 171) `def __init__(self, complete, add_hint)`
  - `run` (method, line 176) `def run(self, goal, context)`
  - `_review` (method, line 190) `def _review(self, goal, context)`
  - `apply` (method, line 200) `def apply(self, findings)`
- Imported by: `modules/lazy_loop.py`, `tests/test_lazy_blindspot.py`

## modules/lazy_bridge.py
- Doc: Bidirectional LAZY <-> LazyOwn bridge.
- Layer: utility
- Language: py
- Symbols:
  - `_data_dir` (function, line 35) `def _data_dir()`
  - `_read_json` (function, line 51) `def _read_json(path, default)`
  - `_read_jsonl` (function, line 68) `def _read_jsonl(path)`
  - `lazy_tasks` (function, line 92) `def lazy_tasks()`
  - `lazy_assets` (function, line 103) `def lazy_assets()`
  - `lazy_graph` (function, line 114) `def lazy_graph(task_id)`
  - `lazy_activity` (function, line 127) `def lazy_activity(task_id)`
  - `lazy_traffic` (function, line 139) `def lazy_traffic(task_id)`
  - `lazy_guard_audit` (function, line 151) `def lazy_guard_audit(task_id)`
  - `bridge_status` (function, line 163) `def bridge_status()`
  - `_extract_hosts_from_graph` (function, line 184) `def _extract_hosts_from_graph(graph)`
  - `pull_to_world_model` (function, line 221) `def pull_to_world_model()`
  - `pull_to_objectives` (function, line 298) `def pull_to_objectives()`
  - `pull_findings_to_lifecycle` (function, line 333) `def pull_findings_to_lifecycle()`
  - `_read_new_traffic` (function, line 361) `def _read_new_traffic(path, offset)`
  - `_notify` (function, line 398) `def _notify(progress, text)`
  - `pull_traffic_to_recorder` (function, line 408) `def pull_traffic_to_recorder(progress)`
  - `push_objective_to_lazy` (function, line 476) `def push_objective_to_lazy(goal, scope)`
  - `push_tasks_to_c2` (function, line 501) `def push_tasks_to_c2(only)`
  - `sync_all` (function, line 566) `def sync_all(progress)`
  - `_record_sync` (function, line 592) `def _record_sync(action, summary)`
- Depends on: `modules/finding_lifecycle.py`, `modules/traffic_recorder.py`, `modules/world_model.py`
- Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/mcp_tools/lazy_status.py`, `skills/mcp_tools/lazy_sync.py`, `tests/conftest.py`, `tests/test_cve_pipeline.py`, `tests/test_lazy_loop.py`

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
  - `_verb_in_phase` (function, line 219) `def _verb_in_phase(row, phase)`
  - `catalog_cli_for_phase` (function, line 240) `def catalog_cli_for_phase(limit)`
  - `full_cli_enabled` (function, line 274) `def full_cli_enabled()`
  - `set_full_cli` (function, line 297) `def set_full_cli(enabled)`
- Depends on: `core/config.py`, `modules/killchain.py`, `modules/verb_catalog.py`
- Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/chain_distill.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/verb_catalog.py`, `tests/test_loop_cli_catalog.py`

## modules/lazy_commander.py
- Doc: Fleet commander: allocate the next work slice across loop tasks.
- Layer: utility
- Language: py
- Symbols:
  - `CommanderDecision` (class, line 63) `class CommanderDecision`
  - `parse_commander_decision` (function, line 77) `def parse_commander_decision(raw)`
  - `render_board` (function, line 119) `def render_board(rows, worked)`
  - `build_commander_prompt` (function, line 145) `def build_commander_prompt(board_rows, time_budget, worked)`
  - `format_commander_budget` (function, line 161) `def format_commander_budget(deadline, now)`
  - `LazyCommander` (class, line 177) `class LazyCommander`
  - `__init__` (method, line 190) `def __init__(self, board_fn, complete_fn, work_fn, pause_fn, clock, sleep)`
  - `run` (method, line 207) `def run(self, minutes, max_slices, base_workers)`
  - `_rows` (method, line 292) `def _rows(self)`
  - `_decide` (method, line 300) `def _decide(self, rows, worked, deadline)`
  - `_least_worked` (method, line 325) `def _least_worked(rows, worked)`
- Imported by: `cli/commands/lazyops.py`, `tests/test_lazy_commander.py`

## modules/lazy_continuation.py
- Doc: Task continuation records: campaign memory that survives loop restarts.
- Layer: utility
- Language: py
- Symbols:
  - `ContinuationRecord` (class, line 36) `class ContinuationRecord`
  - `_dir` (function, line 64) `def _dir()`
  - `_slug` (function, line 71) `def _slug(target)`
  - `record_path` (function, line 77) `def record_path(target)`
  - `save` (function, line 89) `def save(target, task_id, goal, status, settlement, findings, next_steps, credentials, deviations)`
  - `load` (function, line 144) `def load(target)`
  - `handover_brief` (function, line 173) `def handover_brief(target)`
  - `recall_candidates` (function, line 214) `def recall_candidates(target, limit)`

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
- Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/lazy_feedmatch.py`, `modules/lazy_hostscore.py`, `tests/test_lazy_checks.py`

## modules/lazy_deviations.py
- Doc: Planned-versus-actual deviation ledger for loop and chain runs.
- Layer: utility
- Language: py
- Symbols:
  - `DeviationRecord` (class, line 35) `class DeviationRecord`
  - `_clean` (function, line 67) `def _clean(text)`
  - `DeviationLedger` (class, line 72) `class DeviationLedger`
  - `as_dict` (method, line 55) `def as_dict(self)`
  - `__init__` (method, line 80) `def __init__(self, path)`
  - `record` (method, line 84) `def record(self, scope, planned, actual, reason, source)`
  - `list` (method, line 124) `def list(self, scope, limit)`
  - `render_markdown` (method, line 140) `def render_markdown(self, records, title)`
  - `_last_matches` (method, line 160) `def _last_matches(self, scope, planned, actual, reason)`
  - `_read` (method, line 172) `def _read(self)`
  - `_append` (method, line 201) `def _append(self, record)`
  - `_trim` (method, line 216) `def _trim(self)`
- Imported by: `cli/commands/lazyops.py`, `modules/chain_runner.py`, `modules/lazy_loop.py`, `tests/test_lazy_deviations.py`

## modules/lazy_drafts.py
- Doc: Injected objective drafts: close the lazy_drafts handoff loop.
- Layer: utility
- Language: py
- Symbols:
  - `_drafts_dir` (function, line 27) `def _drafts_dir()`
  - `drain` (function, line 34) `def drain(engine)`
- Depends on: `modules/lazy_loop.py`
- Imported by: `tests/test_loop_objective_wiring.py`

## modules/lazy_engine.py
- Doc: Lazy autonomous loop engine: single orchestrator for lazy_* commands.
- Layer: utility
- Language: py
- Symbols:
  - `LazyEngine` (class, line 56) `class LazyEngine(LazyLoopEngine)`
- Depends on: `modules/lazy_loop.py`
- Imported by: `cli/commands/lazyloop.py`, `cli/commands/lazyops.py`, `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `cli/orchestrator_assets_tabs.py`, `cli/session_brief.py`, `modules/lazy_loop.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/llm_orchestrator.py`, `modules/tools/loop_smoke.py`, `modules/tools/monitor_smoke.py`, `skills/autonomous_daemon.py`, `skills/mcp_tools/auto_loop.py`, `skills/mcp_tools/lazy_board.py`, `skills/mcp_tools/lazy_finding.py`, `skills/mcp_tools/lazy_hint.py`, `skills/mcp_tools/lazy_proxy.py`, `skills/mcp_tools/lazy_trace.py`, `skills/mcp_tools/loop_smoke.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_evidence.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_worker_safety.py`, `tests/test_llm_orchestrator.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_broadcast.py`, `tests/test_loop_cold_overview.py`, `tests/test_loop_fire_pending.py`, `tests/test_loop_force_graph.py`, `tests/test_loop_guard_audit.py`, `tests/test_loop_intent_delete.py`, `tests/test_loop_llm_resilience.py`, `tests/test_loop_objective_wiring.py`, `tests/test_loop_scope_traffic_evidence.py`, `tests/test_loop_spawn_side.py`, `tests/test_loop_supervision.py`, `tests/test_loop_worker_traces.py`, `tests/test_module_registry_bridge.py`, `tests/test_session_brief.py`, `tests/test_sink_chain_feed.py`, `tests/test_world_diff_retest.py`

## modules/lazy_exposure.py
- Doc: Target exposure report for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `ensure_report` (function, line 56) `def ensure_report(target, entries, refresh)`
  - `read_sightings` (function, line 97) `def read_sightings(target, state_path)`
  - `generate_report` (function, line 129) `def generate_report(target, entries, sightings)`
  - `_live_fingerprint` (function, line 210) `def _live_fingerprint()`
  - `score_report` (function, line 219) `def score_report(entries, bounded_unknown, services)`
  - `probe_checks` (function, line 257) `def probe_checks(matches, feed)`
  - `save_report` (function, line 291) `def save_report(report, path)`
  - `publish_report` (function, line 314) `def publish_report(report)`
  - `_short_refs` (function, line 365) `def _short_refs(row)`
  - `_shape_sightings` (function, line 370) `def _shape_sightings(rows)`
  - `_match_hot_key` (function, line 400) `def _match_hot_key(row)`
  - `_slug` (function, line 405) `def _slug(text)`
  - `_int` (function, line 410) `def _int(value, fallback)`
  - `refresh_if_stale` (function, line 418) `def refresh_if_stale(target, entries)`
- Depends on: `modules/__init__.py`, `modules/lazy_feedmatch.py`, `modules/lazy_heat.py`, `modules/lazy_probes.py`, `modules/outcome_bus.py`, `modules/world_model.py`
- Imported by: `cli/commands/exposure_intel.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `skills/mcp_tools/lazy_intel.py`, `tests/test_lazy_exposure.py`

## modules/lazy_fallback.py
- Doc: Adaptive fallback alternatives for failed chain techniques.
- Layer: utility
- Language: py
- Symbols:
  - `Alternative` (class, line 29) `class Alternative`
  - `TechniqueFallback` (class, line 47) `class TechniqueFallback`
  - `_service_satisfied` (function, line 172) `def _service_satisfied(required, services)`
  - `AdaptiveFallbackArbiter` (class, line 185) `class AdaptiveFallbackArbiter`
  - `catalogue_ids` (function, line 261) `def catalogue_ids()`
  - `matches` (method, line 61) `def matches(self, command)`
  - `__init__` (method, line 193) `def __init__(self, graph)`
  - `suggest` (method, line 203) `def suggest(self, command, verdict, services, has_credentials, catalogue)`
  - `tried_count` (method, line 246) `def tried_count(self)`
  - `_bind_family` (method, line 251) `def _bind_family(self, command)`
- Depends on: `modules/atomic_exploit_bridge.py`, `modules/failure_verdict.py`
- Imported by: `cli/apt_chain_support.py`, `cli/commands/lazy_adaptive.py`, `tests/test_lazy_fallback.py`

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


Next: [KB_modules_p9.md](KB_modules_p9.md)
