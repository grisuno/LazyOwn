# Subsystem: tests (page 17 of 24)
Previous: [KB_tests_p16.md](KB_tests_p16.md)

## tests/test_loop_objective_wiring.py
- Doc: Loop wiring fidelity: objective queue and Hermes draft consumption.
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 14) `def _patched_engine(tmp_path, monkeypatch)`
  - `_point_objectives` (function, line 25) `def _point_objectives(tmp_path, monkeypatch)`
  - `_write_objective` (function, line 37) `def _write_objective(path, objective_id, text, status, priority, target)`
  - `_statuses` (function, line 51) `def _statuses(path)`
  - `test_pending_objectives_filters_by_target_and_priority` (function, line 61) `def test_pending_objectives_filters_by_target_and_priority(tmp_path, monkeypatch)`
  - `test_planner_emits_and_claims_injected_objective` (function, line 77) `def test_planner_emits_and_claims_injected_objective(tmp_path, monkeypatch)`
  - `test_settle_marks_done_when_intent_done` (function, line 95) `def test_settle_marks_done_when_intent_done(tmp_path, monkeypatch)`
  - `test_settle_requeues_when_intent_unfinished` (function, line 112) `def test_settle_requeues_when_intent_unfinished(tmp_path, monkeypatch)`
  - `test_drain_drafts_imports_pending_draft_as_task` (function, line 128) `def test_drain_drafts_imports_pending_draft_as_task(tmp_path, monkeypatch)`
  - `test_drain_drafts_is_idempotent` (function, line 153) `def test_drain_drafts_is_idempotent(tmp_path, monkeypatch)`
  - `test_daemon_drain_drafts_helper_is_safe_without_engine` (function, line 172) `def test_daemon_drain_drafts_helper_is_safe_without_engine()`
  - `test_daemon_drain_drafts_imports_pending_draft` (function, line 179) `def test_daemon_drain_drafts_imports_pending_draft(tmp_path, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/lazy_drafts.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`

## tests/test_loop_progress.py
- Doc: Loop milestone panel: inferred stage states stay honest.
- Layer: testing
- Language: py
- Symbols:
  - `_overview` (function, line 20) `def _overview()`
  - `test_chain_has_fourteen_stages` (function, line 28) `def test_chain_has_fourteen_stages()`
  - `test_fresh_task_shows_first_stage_current` (function, line 34) `def test_fresh_task_shows_first_stage_current()`
  - `test_progress_advances_with_evidence` (function, line 44) `def test_progress_advances_with_evidence()`
  - `test_finished_task_all_green` (function, line 58) `def test_finished_task_all_green()`
  - `test_snapshot_counts_intent_states` (function, line 69) `def test_snapshot_counts_intent_states()`
  - `test_panel_renders_without_live` (function, line 79) `def test_panel_renders_without_live()`
  - `test_render_contains_no_markup_strings` (function, line 88) `def test_render_contains_no_markup_strings()`
  - `test_line_mode_prints_only_on_stage_change` (function, line 104) `def test_line_mode_prints_only_on_stage_change(capsys)`
  - `test_sanitize_line_strips_ansi_and_cr` (function, line 126) `def test_sanitize_line_strips_ansi_and_cr()`
  - `test_sanitize_line_keeps_ansi_when_asked` (function, line 134) `def test_sanitize_line_keeps_ansi_when_asked()`
- Depends on: `core/console.py`, `modules/loop_progress.py`

## tests/test_loop_scope_traffic_evidence.py
- Doc: Scope ownership, port-aware traffic search, role-based evidences (lazy parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_scope_covers_by_ownership_not_substring` (function, line 15) `def test_scope_covers_by_ownership_not_substring(tmp_path, monkeypatch)`
  - `test_scope_cidr_covers_url_embedded_ip` (function, line 29) `def test_scope_cidr_covers_url_embedded_ip(tmp_path, monkeypatch)`
  - `test_scope_ip_covers_any_port_url` (function, line 41) `def test_scope_ip_covers_any_port_url(tmp_path, monkeypatch)`
  - `test_worker_scope_enforcement_cidr` (function, line 54) `def test_worker_scope_enforcement_cidr(tmp_path, monkeypatch)`
  - `test_traffic_search_host_port_aware` (function, line 71) `def test_traffic_search_host_port_aware(tmp_path, monkeypatch)`
  - `test_finding_evidence_roles_notes_order` (function, line 88) `def test_finding_evidence_roles_notes_order(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_spawn_side.py
- Doc: Multi-session chat, persistent side questions, spawn inheritance (lazy 0.3.9).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_chat_sessions_stay_independent` (function, line 15) `def test_chat_sessions_stay_independent(tmp_path, monkeypatch)`
  - `test_side_questions_persist_and_recall` (function, line 36) `def test_side_questions_persist_and_recall(tmp_path, monkeypatch)`
  - `test_spawn_inherits_scope_and_findings_read_only` (function, line 53) `def test_spawn_inherits_scope_and_findings_read_only(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_store_race.py
- Doc: Store file writes stay atomic under parallel workers (race regression).
- Layer: testing
- Language: py
- Symbols:
  - `test_save_json_survives_parallel_writers` (function, line 8) `def test_save_json_survives_parallel_writers(tmp_path, monkeypatch)`
  - `writer` (function, line 16) `def writer(worker)`
- Depends on: `modules/lazy_loop.py`

## tests/test_loop_supervision.py
- Doc: Supervision upgrades: repetition watchdog, stack priors, prompt masking.
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `_isolate_intel` (function, line 16) `def _isolate_intel(tmp_path, monkeypatch)`
  - `_DeadPool` (class, line 25) `class _DeadPool`
  - `_kill_llm` (function, line 37) `def _kill_llm(monkeypatch)`
  - `test_repetition_watchdog_settles` (function, line 46) `def test_repetition_watchdog_settles(tmp_path, monkeypatch)`
  - `test_stack_priors_prefer_same_stack` (function, line 75) `def test_stack_priors_prefer_same_stack(tmp_path, monkeypatch)`
  - `test_prompt_context_masks_configured_only` (function, line 99) `def test_prompt_context_masks_configured_only(tmp_path, monkeypatch)`
  - `members` (method, line 28) `def members(self)`
  - `complete` (method, line 32) `def complete(self)`
- Depends on: `core/config.py`, `modules/lazy_engine.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`

## tests/test_loop_trigger_hints.py
- Doc: BDD for the cve_hot trigger hint fingerprints.
- Layer: testing
- Language: py
- Symbols:
  - `_Graph` (class, line 29) `class _Graph`
  - `_Assets` (class, line 42) `class _Assets`
  - `trigger_env` (function, line 56) `def trigger_env(tmp_path, monkeypatch)`
  - `test_cve_hot_hint_proposed_once_per_signature` (function, line 78) `def test_cve_hot_hint_proposed_once_per_signature(trigger_env)`
  - `test_changed_banner_refires_the_hint` (function, line 90) `def test_changed_banner_refires_the_hint(tmp_path, monkeypatch)`
  - `test_hint_fingerprint_normalizes_product_and_version` (function, line 118) `def test_hint_fingerprint_normalizes_product_and_version()`
  - `test_prune_drops_expired_fingerprints` (function, line 128) `def test_prune_drops_expired_fingerprints()`
  - `test_hint_ttl_expires_and_refires` (function, line 137) `def test_hint_ttl_expires_and_refires(tmp_path, monkeypatch)`
  - `test_hint_store_written_under_loop_stores` (function, line 158) `def test_hint_store_written_under_loop_stores(tmp_path, monkeypatch)`
  - `__init__` (method, line 32) `def __init__(self)`
  - `add_node` (method, line 35) `def add_node(self, kind, text, state, priority, meta)`
  - `list` (method, line 38) `def list(self)`
  - `__init__` (method, line 45) `def __init__(self, value)`
  - `list` (method, line 49) `def list(self, kind)`
  - `fake_hot_matches` (function, line 65) `def fake_hot_matches(services, allow_network)`
  - `fake_hot_matches` (function, line 100) `def fake_hot_matches(services, allow_network)`
- Depends on: `modules/lazy_loop.py`, `modules/loop_triggers.py`, `modules/world_model.py`

## tests/test_loop_worker_traces.py
- Doc: Worker cross-work trace tools (lazy 0.3.10 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `_seed_two_works` (function, line 15) `def _seed_two_works(engine, task_id)`
  - `test_search_all_spans_works_without_intent` (function, line 27) `def test_search_all_spans_works_without_intent(tmp_path, monkeypatch)`
  - `test_trace_steps_and_single_step` (function, line 40) `def test_trace_steps_and_single_step(tmp_path, monkeypatch)`
  - `test_worker_lane_binds_node_detail` (function, line 57) `def test_worker_lane_binds_node_detail(tmp_path, monkeypatch)`
  - `test_add_hint_emits_explicit_planner_trigger` (function, line 65) `def test_add_hint_emits_explicit_planner_trigger(tmp_path, monkeypatch)`
  - `test_worker_bash_unbound_blocks_without_execution` (function, line 81) `def test_worker_bash_unbound_blocks_without_execution(tmp_path, monkeypatch)`
  - `test_planner_intent_unbound_emits_nothing` (function, line 100) `def test_planner_intent_unbound_emits_nothing(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_marketplace_config.py
- Doc: Marketplace registry and settings: formats, toggles, CRUD.
- Layer: testing
- Language: py
- Symbols:
  - `_registry` (function, line 12) `def _registry(tmp_path, monkeypatch)`
  - `test_tool_rows_use_json_and_active_key` (function, line 33) `def test_tool_rows_use_json_and_active_key(tmp_path, monkeypatch)`
  - `test_plugin_rows_skip_lua_and_templates` (function, line 61) `def test_plugin_rows_skip_lua_and_templates(tmp_path, monkeypatch)`
  - `test_read_only_tabs_never_toggle_or_delete` (function, line 76) `def test_read_only_tabs_never_toggle_or_delete(tmp_path, monkeypatch)`
  - `test_create_and_delete_across_tabs` (function, line 89) `def test_create_and_delete_across_tabs(tmp_path, monkeypatch)`
  - `test_settings_toggle_tracks_only_success` (function, line 105) `def test_settings_toggle_tracks_only_success(tmp_path, monkeypatch)`
  - `test_marketplace_app_filters_rows` (function, line 118) `def test_marketplace_app_filters_rows(tmp_path, monkeypatch)`
  - `test_filter_input_keeps_printable_keys` (function, line 145) `def test_filter_input_keeps_printable_keys(tmp_path, monkeypatch)`
  - `_drive` (function, line 128) `def _drive()`
  - `_drive` (function, line 151) `def _drive()`
- Depends on: `cli/__init__.py`

## tests/test_mcp_auto_loop_wrapper.py
- Doc: MCP auto_loop wrapper contract: one orchestrator, no dual engines.
- Layer: testing
- Language: py
- Symbols:
  - `_patched` (function, line 16) `def _patched(monkeypatch, tmp_path)`
  - `test_fast_path_runs_the_engine` (function, line 76) `def test_fast_path_runs_the_engine(monkeypatch, tmp_path)`
  - `test_legacy_flag_annotates_but_routes_fast` (function, line 90) `def test_legacy_flag_annotates_but_routes_fast(monkeypatch, tmp_path)`
  - `test_engine_failure_surfaces` (function, line 100) `def test_engine_failure_surfaces(monkeypatch, tmp_path)`
  - `_text` (function, line 110) `def _text(response)`
  - `loop_join` (function, line 125) `def loop_join(coro)`
  - `_FakeEngine` (class, line 44) `class _FakeEngine`
  - `_Boom` (class, line 31) `class _Boom`
  - `__init__` (method, line 45) `def __init__(self)`
  - `create_task` (method, line 50) `def create_task(self, goal)`
  - `ensure_target` (method, line 54) `def ensure_target(self, task_id, target, reason)`
  - `run` (method, line 58) `def run(self, task_id, max_rounds, workers, timeout_sec)`
  - `__init__` (method, line 32) `def __init__(self)`
- Depends on: `modules/lazy_loop.py`, `skills/lazyown_mcp.py`

## tests/test_mcp_dispatch.py
- Doc: call_tool dispatches through the handler registry.
- Layer: testing
- Language: py
- Symbols:
  - `_registered` (function, line 23) `def _registered()`
  - `_fallback_branches` (function, line 40) `def _fallback_branches()`
  - `TestRegistryDispatch` (class, line 51) `class TestRegistryDispatch`
  - `test_set_config_refuses_null_values` (function, line 67) `def test_set_config_refuses_null_values()`
  - `test_new_chain_shell_tools_have_defs_and_handlers` (function, line 82) `def test_new_chain_shell_tools_have_defs_and_handlers()`
  - `test_opencode_bridge_curates_loop_and_chain` (function, line 92) `def test_opencode_bridge_curates_loop_and_chain()`
  - `test_mcp_never_offers_interactive_repl` (function, line 107) `def test_mcp_never_offers_interactive_repl()`
  - `test_no_dead_duplicate_branches` (method, line 52) `def test_no_dead_duplicate_branches(self)`
  - `test_migrated_handlers_registered` (method, line 56) `def test_migrated_handlers_registered(self)`
  - `test_migrated_handlers_absent_from_fallback` (method, line 61) `def test_migrated_handlers_absent_from_fallback(self)`

## tests/test_mcp_improvements.py
- Doc: Tests for the high/medium/low impact MCP improvements.
- Layer: testing
- Language: py
- Symbols:
  - `test_is_likely_credential_classifies` (function, line 74) `def test_is_likely_credential_classifies(value, expect_real, expect_reason)`
  - `test_is_likely_credential_handles_non_string` (function, line 84) `def test_is_likely_credential_handles_non_string()`
  - `test_parse_task_value_complete` (function, line 92) `def test_parse_task_value_complete()`
  - `test_parse_task_value_truncated` (function, line 103) `def test_parse_task_value_truncated()`
  - `test_parse_task_value_no_payload` (function, line 110) `def test_parse_task_value_no_payload()`
  - `test_audit_tasks_drops_timestamps_and_urls` (function, line 117) `def test_audit_tasks_drops_timestamps_and_urls()`
  - `test_audit_tasks_respects_min_confidence` (function, line 141) `def test_audit_tasks_respects_min_confidence()`
  - `test_evidence_freshness_missing` (function, line 154) `def test_evidence_freshness_missing(tmp_path)`
  - `test_evidence_freshness_fresh` (function, line 160) `def test_evidence_freshness_fresh(tmp_path)`
  - `test_evidence_freshness_stale` (function, line 170) `def test_evidence_freshness_stale(tmp_path)`
  - `_seed_sessions` (function, line 182) `def _seed_sessions(tmp_path)`
  - `test_build_target_context_filters_by_port` (function, line 195) `def test_build_target_context_filters_by_port(tmp_path)`
  - `test_build_target_context_no_port_returns_all` (function, line 218) `def test_build_target_context_no_port_returns_all(tmp_path)`
  - `test_evidence_grep_finds_in_loot_scope` (function, line 227) `def test_evidence_grep_finds_in_loot_scope(tmp_path)`
  - `test_evidence_grep_invalid_regex` (function, line 237) `def test_evidence_grep_invalid_regex(tmp_path)`
  - `test_evidence_grep_truncates` (function, line 244) `def test_evidence_grep_truncates(tmp_path)`
  - `test_preflight_detects_duplicate` (function, line 256) `def test_preflight_detects_duplicate(tmp_path)`
  - `test_preflight_flags_missing_payload_keys` (function, line 270) `def test_preflight_flags_missing_payload_keys(tmp_path)`
  - `test_preflight_os_mismatch` (function, line 281) `def test_preflight_os_mismatch(tmp_path)`
  - `test_jobstore_runs_command_and_reports_done` (function, line 297) `def test_jobstore_runs_command_and_reports_done()`
  - `test_jobstore_captures_failure` (function, line 317) `def test_jobstore_captures_failure()`
  - `test_jobstore_unknown_id` (function, line 335) `def test_jobstore_unknown_id()`
  - `test_jobstore_list_orders_newest_first` (function, line 340) `def test_jobstore_list_orders_newest_first()`
  - `test_diff_first_run_reports_first_run` (function, line 353) `def test_diff_first_run_reports_first_run(tmp_path)`
  - `test_diff_picks_up_changes` (function, line 360) `def test_diff_picks_up_changes(tmp_path)`
  - `test_confirmation_required_for_destructive_command` (function, line 380) `def test_confirmation_required_for_destructive_command()`
  - `test_confirmation_skipped_for_benign` (function, line 385) `def test_confirmation_skipped_for_benign()`
  - `test_confirmation_required_for_destructive_tools` (function, line 389) `def test_confirmation_required_for_destructive_tools()`
  - `_fresh_mcp_module` (function, line 397) `def _fresh_mcp_module(tmp_path)`
  - `test_handler_target_context_via_helper` (function, line 414) `def test_handler_target_context_via_helper(tmp_path)`
  - `test_handler_tasks_cleanup_dry_run` (function, line 421) `def test_handler_tasks_cleanup_dry_run(tmp_path)`
  - `test_evidence_grep_handler_ignores_binaries` (function, line 436) `def test_evidence_grep_handler_ignores_binaries(tmp_path)`
  - `runner` (function, line 300) `def runner(cmd, timeout)`
  - `runner` (function, line 320) `def runner(cmd, timeout)`
- Depends on: `skills/lazyown_mcp.py`, `skills/lazyown_mcp_helpers.py`

## tests/test_mcp_lazy.py
- Doc: Contract for the unified MCP lazy-import helper.
- Layer: testing
- Language: py
- Symbols:
  - `TestEnsureOptional` (class, line 42) `class TestEnsureOptional`
  - `TestWrappersDelegate` (class, line 86) `class TestWrappersDelegate`
  - `test_success_binds_and_caches` (method, line 43) `def test_success_binds_and_caches(self)`
  - `test_cached_value_returned_untouched` (method, line 58) `def test_cached_value_returned_untouched(self)`
  - `test_exception_fails_closed` (method, line 66) `def test_exception_fails_closed(self)`
  - `test_false_loader_with_fallback` (method, line 75) `def test_false_loader_with_fallback(self)`
  - `test_all_wrappers_delegate_to_helper` (method, line 87) `def test_all_wrappers_delegate_to_helper(self)`
  - `loader` (function, line 47) `def loader(ns)`
  - `loader` (function, line 61) `def loader(ns)`
  - `loader` (function, line 69) `def loader(ns)`
  - `loader` (function, line 78) `def loader(ns)`
- Depends on: `skills/mcp_lazy.py`

## tests/test_mcp_recommender_embed.py
- Doc: Contract tests for the MCP sitrep recommender embedding.
- Layer: testing
- Language: py
- Symbols:
  - `_load_mcp_module` (function, line 15) `def _load_mcp_module()`
  - `test_maps_recommender_fields` (function, line 25) `def test_maps_recommender_fields(monkeypatch)`
  - `test_never_forwards_positional_arguments` (function, line 44) `def test_never_forwards_positional_arguments(monkeypatch)`
  - `test_returns_error_entry_on_failure` (function, line 59) `def test_returns_error_entry_on_failure(monkeypatch)`
  - `test_reports_unavailable_recommender` (function, line 71) `def test_reports_unavailable_recommender(monkeypatch)`
  - `test_limits_suggestions` (function, line 81) `def test_limits_suggestions(monkeypatch)`
  - `fake_recommend` (function, line 48) `def fake_recommend()`
  - `explode` (function, line 62) `def explode()`

## tests/test_mediation.py
- Doc: Mediator pattern contract tests for the mediation package.
- Layer: testing
- Language: py
- Symbols:
  - `TestHubRouting` (class, line 19) `class TestHubRouting`
  - `TestIntelMediatorActivityPort` (class, line 39) `class TestIntelMediatorActivityPort`
  - `TestFeedbackMediator` (class, line 62) `class TestFeedbackMediator`
  - `TestTelemetryMediator` (class, line 82) `class TestTelemetryMediator`
  - `TestChainMediatorLlmPort` (class, line 170) `class TestChainMediatorLlmPort`
  - `test_all_default_domains_registered` (method, line 22) `def test_all_default_domains_registered(self)`
  - `test_unknown_domain_returns_none` (method, line 27) `def test_unknown_domain_returns_none(self)`
  - `test_singleton_hub_shared` (method, line 30) `def test_singleton_hub_shared(self)`
  - `test_mediation_contract_shape` (method, line 33) `def test_mediation_contract_shape(self)`
  - `test_activity_records_via_injected_port` (method, line 42) `def test_activity_records_via_injected_port(self)`
  - `test_activity_records_fallback_graceful` (method, line 48) `def test_activity_records_fallback_graceful(self)`
  - `test_mask_and_stack_survive_missing_peers` (method, line 52) `def test_mask_and_stack_survive_missing_peers(self, monkeypatch)`
  - `test_order_steps_passthrough_on_error` (method, line 65) `def test_order_steps_passthrough_on_error(self, monkeypatch)`
  - `test_order_steps_forwarded` (method, line 75) `def test_order_steps_forwarded(self, monkeypatch)`
  - `test_publish_event_default_severity_positional` (method, line 85) `def test_publish_event_default_severity_positional(self, monkeypatch)`
  - `test_publish_event_forwarding_calls_default_path` (method, line 95) `def test_publish_event_forwarding_calls_default_path(self, monkeypatch)`
  - `test_rl_select_graceful_off` (method, line 105) `def test_rl_select_graceful_off(self, monkeypatch)`
  - `test_assess_opsec_forwards_to_bridge` (method, line 114) `def test_assess_opsec_forwards_to_bridge(self, monkeypatch)`
  - `test_assess_opsec_graceful_on_bridge_failure` (method, line 121) `def test_assess_opsec_graceful_on_bridge_failure(self, monkeypatch)`
  - `test_record_outcome_quality_forwards_to_bridge` (method, line 130) `def test_record_outcome_quality_forwards_to_bridge(self, monkeypatch)`
  - `test_record_outcome_quality_graceful_on_bridge_failure` (method, line 144) `def test_record_outcome_quality_graceful_on_bridge_failure(self, monkeypatch)`
  - `test_tool_class_yields_forwards_to_bridge` (method, line 153) `def test_tool_class_yields_forwards_to_bridge(self, monkeypatch)`
  - `test_tool_class_yields_graceful_on_bridge_failure` (method, line 160) `def test_tool_class_yields_graceful_on_bridge_failure(self, monkeypatch)`
  - `test_port_contract` (method, line 173) `def test_port_contract(self)`
  - `test_register_llm_port_replaces` (method, line 181) `def test_register_llm_port_replaces(self)`
  - `_patch_hub` (method, line 194) `def _patch_hub(self, monkeypatch, port)`
  - `test_recovery_pool_absent_returns_empty` (method, line 214) `def test_recovery_pool_absent_returns_empty(self, monkeypatch)`
  - `test_recovery_pool_builds_steps` (method, line 236) `def test_recovery_pool_builds_steps(self, monkeypatch)`
  - `test_recovery_prompt_carries_recent_changes` (method, line 262) `def test_recovery_prompt_carries_recent_changes(self, monkeypatch, tmp_path)`
  - `boom` (function, line 68) `def boom(steps, stack)`
  - `boom` (function, line 108) `def boom()`
  - `boom` (function, line 124) `def boom()`
  - `boom` (function, line 147) `def boom()`
  - `boom` (function, line 163) `def boom()`
  - `Fake` (class, line 182) `class Fake`
  - `_FakeHub` (class, line 197) `class _FakeHub`
  - `_NoLock` (class, line 204) `class _NoLock`
  - `Empty` (class, line 217) `class Empty`
  - `FakePort` (class, line 239) `class FakePort`
  - `FakePort` (class, line 280) `class FakePort`
  - `complete` (method, line 183) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 186) `def has_members(self)`
  - `__init__` (method, line 198) `def __init__(self, port)`
  - `mediator_for` (method, line 201) `def mediator_for(self, domain)`
  - `__enter__` (method, line 205) `def __enter__(self)`
  - `__exit__` (method, line 208) `def __exit__(self)`
  - `complete` (method, line 218) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 221) `def has_members(self)`
  - `complete` (method, line 240) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 243) `def has_members(self)`
  - `complete` (method, line 281) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 285) `def has_members(self)`
- Depends on: `cli/__init__.py`, `modules/chain_runner.py`, `modules/lazy_intel.py`, `modules/lazy_orchestrator_feedback.py`, `modules/lazy_world_diff.py`, `modules/loop_ai_bridge.py`, `modules/mediation/__init__.py`, `modules/mediation/hub.py`

## tests/test_memory_semantics.py
- Doc: BDD tests for hashing embeddings and hybrid episodic recall.
- Layer: testing
- Language: py
- Symbols:
  - `_entry` (function, line 14) `def _entry(tool, command, snippet)`
  - `TestHashingEmbedder` (class, line 27) `class TestHashingEmbedder`
  - `TestVectorSQLiteBackend` (class, line 62) `class TestVectorSQLiteBackend`
  - `TestMemoryStoreHybrid` (class, line 90) `class TestMemoryStoreHybrid`
  - `test_identical_text_full_similarity` (method, line 30) `def test_identical_text_full_similarity(self)`
  - `test_similar_text_scores_higher_than_unrelated` (method, line 36) `def test_similar_text_scores_higher_than_unrelated(self)`
  - `test_determinism_across_runs` (method, line 44) `def test_determinism_across_runs(self)`
  - `test_empty_text_raises` (method, line 49) `def test_empty_text_raises(self)`
  - `test_unit_length` (method, line 55) `def test_unit_length(self)`
  - `test_save_gets_embedding` (method, line 65) `def test_save_gets_embedding(self, tmp_path)`
  - `test_semantic_ranks_relevant_first` (method, line 73) `def test_semantic_ranks_relevant_first(self, tmp_path)`
  - `test_keyword_query_still_works` (method, line 82) `def test_keyword_query_still_works(self, tmp_path)`
  - `test_fts_wins_when_present` (method, line 93) `def test_fts_wins_when_present(self, tmp_path)`
  - `test_hybrid_fallback_after_miss` (method, line 101) `def test_hybrid_fallback_after_miss(self, tmp_path)`
- Depends on: `modules/memory_embeddings.py`, `modules/memory_store.py`

## tests/test_metasploitable_gym.py
- Doc: Metasploitable 2 gym BDD contract: one exploit, one chain, one index entry.
- Layer: testing
- Language: py
- Symbols:
  - `test_index_covers_the_ms2_vectors` (function, line 23) `def test_index_covers_the_ms2_vectors()`
  - `test_every_exploit_and_chain_is_loadable` (function, line 50) `def test_every_exploit_and_chain_is_loadable()`
  - `test_gym_base_ends_with_interactive_shell` (function, line 63) `def test_gym_base_ends_with_interactive_shell()`
  - `test_every_chain_resolves_without_unresolved_tokens` (function, line 74) `def test_every_chain_resolves_without_unresolved_tokens()`
  - `test_unknown_vulnerability_returns_none` (function, line 89) `def test_unknown_vulnerability_returns_none()`
  - `test_invalid_matrix_is_reported` (function, line 96) `def test_invalid_matrix_is_reported(tmp_path)`
- Depends on: `modules/atomic_exploit_bridge.py`, `modules/chain_registry.py`, `modules/metasploitable_gym.py`

## tests/test_metasploitable_migrations.py
- Doc: Unit tests for the Metasploitable 2 gym migrations module.
- Layer: testing
- Language: py
- Symbols:
  - `test_build_migrations_ordered_and_unique` (function, line 8) `def test_build_migrations_ordered_and_unique()`
  - `test_dns_fallback_payload_targets_port_53` (function, line 17) `def test_dns_fallback_payload_targets_port_53()`
  - `test_nfs_fallback_starts_mountd_without_kernel_nfsd` (function, line 28) `def test_nfs_fallback_starts_mountd_without_kernel_nfsd()`
  - `test_rlogin_trust_sets_rhosts_and_local_allow` (function, line 37) `def test_rlogin_trust_sets_rhosts_and_local_allow()`
  - `test_hosts_allow_uses_subnet_prefix` (function, line 47) `def test_hosts_allow_uses_subnet_prefix()`
  - `test_apply_migrations_skips_when_check_passes` (function, line 57) `def test_apply_migrations_skips_when_check_passes(monkeypatch)`
  - `test_apply_migrations_applies_when_check_fails` (function, line 68) `def test_apply_migrations_applies_when_check_fails(monkeypatch)`
  - `test_dvwa_dom_page_payload_contains_sink` (function, line 82) `def test_dvwa_dom_page_payload_contains_sink()`
  - `test_database_mirror_uses_dump_and_restore` (function, line 90) `def test_database_mirror_uses_dump_and_restore()`
  - `_fake_exec` (function, line 69) `def _fake_exec(container, script, payload, timeout)`
- Depends on: `modules/metasploitable_migrations.py`

## tests/test_metrics.py
- Doc: Tests for ``modules/metrics.py``.
- Layer: testing
- Language: py
- Symbols:
  - `_build_recorder` (function, line 35) `def _build_recorder(tmp_path)`
  - `test_legacy_registry_inc_and_render` (function, line 42) `def test_legacy_registry_inc_and_render()`
  - `test_recorder_appends_record_line` (function, line 57) `def test_recorder_appends_record_line(tmp_path)`
  - `test_recorder_clamps_negative_duration` (function, line 83) `def test_recorder_clamps_negative_duration(tmp_path)`
  - `test_summarize_aggregates_by_command` (function, line 92) `def test_summarize_aggregates_by_command(tmp_path)`
  - `test_summarize_window_filters_old_records` (function, line 124) `def test_summarize_window_filters_old_records(tmp_path)`
  - `test_tail_returns_newest_first` (function, line 163) `def test_tail_returns_newest_first(tmp_path)`
  - `test_concurrent_writes_do_not_corrupt` (function, line 173) `def test_concurrent_writes_do_not_corrupt(tmp_path)`
  - `test_get_recorder_is_singleton` (function, line 202) `def test_get_recorder_is_singleton(tmp_path)`
  - `test_aggregator_handles_empty_iterable` (function, line 211) `def test_aggregator_handles_empty_iterable()`
  - `test_aggregator_skips_malformed_records` (function, line 220) `def test_aggregator_skips_malformed_records()`
  - `test_p95_uses_nearest_rank` (function, line 227) `def test_p95_uses_nearest_rank()`
  - `test_metric_record_to_dict_roundtrip` (function, line 234) `def test_metric_record_to_dict_roundtrip()`
  - `worker` (function, line 180) `def worker(tag)`
- Depends on: `modules/metrics.py`

## tests/test_metrics_aware_selector.py
- Doc: Tests for ``MetricsAwareSelector`` in ``skills/autonomous_daemon.py``.
- Layer: testing
- Language: py
- Symbols:
  - `_StubSelector` (class, line 37) `class _StubSelector(ICommandSelector)`
  - `_StubMetrics` (class, line 54) `class _StubMetrics`
  - `_decision` (function, line 71) `def _decision(command)`
  - `test_passthrough_when_wrapped_returns_none` (function, line 75) `def test_passthrough_when_wrapped_returns_none()`
  - `test_passthrough_when_insufficient_attempts` (function, line 87) `def test_passthrough_when_insufficient_attempts()`
  - `test_filters_when_success_rate_below_threshold` (function, line 105) `def test_filters_when_success_rate_below_threshold()`
  - `test_accepts_when_success_rate_at_threshold` (function, line 122) `def test_accepts_when_success_rate_at_threshold()`
  - `test_only_filters_named_command_not_whole_decision_object` (function, line 141) `def test_only_filters_named_command_not_whole_decision_object()`
  - `test_summary_is_cached_within_ttl` (function, line 158) `def test_summary_is_cached_within_ttl()`
  - `test_summary_forwards_window_seconds` (function, line 188) `def test_summary_forwards_window_seconds()`
  - `test_zero_window_is_treated_as_unbounded` (function, line 201) `def test_zero_window_is_treated_as_unbounded()`
  - `test_decorator_degrades_when_metrics_source_unavailable` (function, line 214) `def test_decorator_degrades_when_metrics_source_unavailable()`
  - `test_wrap_chain_leaves_fallback_unwrapped` (function, line 230) `def test_wrap_chain_leaves_fallback_unwrapped()`
  - `test_wrap_chain_master_switch_off` (function, line 241) `def test_wrap_chain_master_switch_off()`
  - `test_wrap_chain_is_idempotent` (function, line 253) `def test_wrap_chain_is_idempotent()`
  - `test_filtering_emits_skip_event` (function, line 265) `def test_filtering_emits_skip_event(tmp_path, monkeypatch)`
  - `test_chain_falls_through_to_fallback_when_all_filtered` (function, line 298) `def test_chain_falls_through_to_fallback_when_all_filtered()`
  - `__init__` (method, line 40) `def __init__(self, decision)`
  - `select` (method, line 44) `def select(self, target, phase, context)`
  - `__init__` (method, line 57) `def __init__(self, by_command)`
  - `summarize` (method, line 62) `def summarize(self, window_seconds)`
  - `fake_clock` (function, line 169) `def fake_clock()`
  - `_BrokenSource` (class, line 217) `class _BrokenSource`
  - `summarize` (method, line 218) `def summarize(self, window_seconds)`
- Depends on: `skills/autonomous_daemon.py`

## tests/test_migrate_lazyown_generator.py
- Doc: Regression guard for the ``cli/commands`` migration generator.
- Layer: testing
- Language: py
- Symbols:
  - `_module_all` (function, line 27) `def _module_all(source)`
  - `test_generated_module_parses` (function, line 57) `def test_generated_module_parses()`
  - `test_all_is_static_and_matches_class_name` (function, line 62) `def test_all_is_static_and_matches_class_name()`
  - `test_compound_phase_title_casing` (function, line 68) `def test_compound_phase_title_casing()`
  - `test_no_unevaluated_fstring_all_literal` (function, line 74) `def test_no_unevaluated_fstring_all_literal()`
  - `test_method_bodies_are_embedded_in_order` (function, line 81) `def test_method_bodies_are_embedded_in_order()`
- Depends on: `scripts/migrate_lazyown.py`

## tests/test_module_registry.py
- Doc: Tests for modules.module_registry — ModuleInfo, ModuleRegistry, search, summary.
- Layer: testing
- Language: py
- Symbols:
  - `TestClassify` (class, line 20) `class TestClassify`
  - `TestModuleInfo` (class, line 36) `class TestModuleInfo`
  - `TestModuleRegistry` (class, line 75) `class TestModuleRegistry`
  - `TestFormatFunctions` (class, line 185) `class TestFormatFunctions`
  - `test_known_categories` (method, line 21) `def test_known_categories(self)`
  - `test_unknown_category_defaults_to_auxiliary` (method, line 27) `def test_unknown_category_defaults_to_auxiliary(self)`
  - `test_empty_string` (method, line 31) `def test_empty_string(self)`
  - `test_minimal_construction` (method, line 37) `def test_minimal_construction(self)`
  - `test_full_construction` (method, line 44) `def test_full_construction(self)`
  - `test_to_dict` (method, line 62) `def test_to_dict(self)`
  - `test_repr` (method, line 70) `def test_repr(self)`
  - `test_singleton` (method, line 76) `def test_singleton(self)`
  - `test_singleton_with_base_dir` (method, line 82) `def test_singleton_with_base_dir(self)`
  - `test_initial_state_not_scanned` (method, line 87) `def test_initial_state_not_scanned(self)`
  - `test_scan_returns_list` (method, line 92) `def test_scan_returns_list(self)`
  - `test_scan_is_idempotent` (method, line 99) `def test_scan_is_idempotent(self)`
  - `test_rescan_forces_refresh` (method, line 106) `def test_rescan_forces_refresh(self)`
  - `test_search_returns_list` (method, line 115) `def test_search_returns_list(self)`
  - `test_search_by_module_type` (method, line 121) `def test_search_by_module_type(self)`
  - `test_search_by_category` (method, line 127) `def test_search_by_category(self)`
  - `test_get_known_module` (method, line 133) `def test_get_known_module(self)`
  - `test_get_unknown_returns_none` (method, line 145) `def test_get_unknown_returns_none(self)`
  - `test_summary_returns_counts` (method, line 149) `def test_summary_returns_counts(self)`
  - `test_by_type_shorthand` (method, line 159) `def test_by_type_shorthand(self)`
  - `test_search_enabled_only_filters_disabled` (method, line 164) `def test_search_enabled_only_filters_disabled(self)`
  - `test_format_module_table_empty` (method, line 186) `def test_format_module_table_empty(self)`
  - `test_format_module_table_with_data` (method, line 190) `def test_format_module_table_with_data(self)`
  - `test_format_module_detail` (method, line 201) `def test_format_module_detail(self)`
  - `test_format_module_detail_minimal` (method, line 217) `def test_format_module_detail_minimal(self)`
- Depends on: `modules/module_registry.py`

## tests/test_module_registry_bridge.py
- Doc: Module-registry loop bridge: corpus mentions enter planning as intents.
- Layer: testing
- Language: py
- Symbols:
  - `_registry` (function, line 15) `def _registry(tmp_path)`
  - `_registry_with_extras` (function, line 43) `def _registry_with_extras(tmp_path)`
  - `_empty_osinfer` (function, line 51) `def _empty_osinfer(monkeypatch)`
  - `test_name_mentions_propose_runnable_intents` (function, line 58) `def test_name_mentions_propose_runnable_intents(tmp_path, monkeypatch)`
  - `test_playbook_mentions_map_to_apt_playbook` (function, line 66) `def test_playbook_mentions_map_to_apt_playbook(tmp_path, monkeypatch)`
  - `test_incompatible_os_is_gated` (function, line 74) `def test_incompatible_os_is_gated(tmp_path, monkeypatch)`
  - `test_fillers_and_nonrunnable_sources_propose_nothing` (function, line 85) `def test_fillers_and_nonrunnable_sources_propose_nothing(tmp_path, monkeypatch)`
  - `test_limit_caps_results` (function, line 93) `def test_limit_caps_results(tmp_path, monkeypatch)`
  - `test_planner_appends_registry_candidates_last` (function, line 107) `def test_planner_appends_registry_candidates_last(tmp_path, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/module_registry.py`


Next: [KB_tests_p18.md](KB_tests_p18.md)
