# Subsystem: tests (page 13 of 20)
Previous: [KB_tests_p12.md](KB_tests_p12.md)

## tests/test_loop_budget.py
- Doc: BDD tests for first-class budget flags on the loop runner.
- Layer: testing
- Language: py
- Symbols:
  - `TestBudgetParsing` (class, line 10) `class TestBudgetParsing`
  - `math_close` (function, line 38) `def math_close(budget)`
  - `TestBudgetGate` (class, line 42) `class TestBudgetGate`
  - `test_budget_pairs_parsed` (method, line 13) `def test_budget_pairs_parsed(self)`
  - `test_minimums_clamped` (method, line 19) `def test_minimums_clamped(self)`
  - `test_unknown_key_rejected` (method, line 25) `def test_unknown_key_rejected(self)`
  - `test_budget_confirm_toggle` (method, line 31) `def test_budget_confirm_toggle(self)`
  - `test_gate_blocks_when_declined` (method, line 45) `def test_gate_blocks_when_declined(self, monkeypatch)`
  - `test_gate_pass_when_approved` (method, line 55) `def test_gate_pass_when_approved(self, monkeypatch)`
  - `test_gate_skipped_autonomous` (method, line 65) `def test_gate_skipped_autonomous(self, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/lazy_runner.py`

## tests/test_loop_cli_catalog.py
- Doc: BDD tests for planner prompt visibility into routable CLI verbs.
- Layer: testing
- Language: py
- Symbols:
  - `sandbox` (function, line 17) `def sandbox(tmp_path, monkeypatch)`
  - `test_catalog_cli_for_phase_lists_enabled_only` (function, line 56) `def test_catalog_cli_for_phase_lists_enabled_only(sandbox)`
  - `test_prompt_context_carries_allowed_commands` (function, line 66) `def test_prompt_context_carries_allowed_commands(sandbox)`
  - `test_missing_catalog_view_adds_nothing` (function, line 79) `def test_missing_catalog_view_adds_nothing(tmp_path, monkeypatch)`
  - `_default` (function, line 47) `def _default(cfg)`
  - `_broken` (function, line 90) `def _broken()`
- Depends on: `modules/__init__.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_loop.py`, `modules/verb_catalog.py`, `modules/world_model.py`

## tests/test_loop_cold_overview.py
- Doc: Cold debounce + planner overview parity (lazy 0.3.8 coldgraph).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `_old_facts` (function, line 15) `def _old_facts(graph, count, prefix)`
  - `test_compact_debounce_keeps_fresh_hot` (function, line 28) `def test_compact_debounce_keeps_fresh_hot(tmp_path, monkeypatch)`
  - `test_compact_folds_stale_facts` (function, line 41) `def test_compact_folds_stale_facts(tmp_path, monkeypatch)`
  - `test_planner_round_folds_minor_window` (function, line 56) `def test_planner_round_folds_minor_window(tmp_path, monkeypatch)`
  - `test_graph_overview_carries_findings_and_done_totals` (function, line 77) `def test_graph_overview_carries_findings_and_done_totals(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_force_graph.py
- Doc: Loop ForceGraph context regression tests (lazy 0.3.12 fidelity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_loop_graph_is_forcegraph_ready` (function, line 15) `def test_loop_graph_is_forcegraph_ready(tmp_path, monkeypatch)`
  - `test_graph_context_surfaces_hubs_and_next` (function, line 32) `def test_graph_context_surfaces_hubs_and_next(tmp_path, monkeypatch)`
  - `test_planner_force_ranks_connected_surface` (function, line 53) `def test_planner_force_ranks_connected_surface(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_guard_audit.py
- Doc: Guard audit filters + tool_use_id source jump (lazy 0.3.11/0.3.12 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_check_mints_tool_use_id` (function, line 15) `def test_check_mints_tool_use_id(tmp_path, monkeypatch)`
  - `test_audit_filters_action_source_query` (function, line 31) `def test_audit_filters_action_source_query(tmp_path, monkeypatch)`
  - `test_lookup_jumps_to_execution` (function, line 48) `def test_lookup_jumps_to_execution(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_guardrails.py
- Doc: Loop guardrails: repetition detection, EDR pacing, target caps, vector fact memory.
- Layer: testing
- Language: py
- Symbols:
  - `test_repeat_detector_flags_identical_window` (function, line 12) `def test_repeat_detector_flags_identical_window()`
  - `test_repeat_detector_recovery_on_variation` (function, line 21) `def test_repeat_detector_recovery_on_variation()`
  - `test_edr_pacer_slow_scan_raises_level` (function, line 35) `def test_edr_pacer_slow_scan_raises_level()`
  - `test_edr_pacer_connection_reset_raises_and_decays` (function, line 47) `def test_edr_pacer_connection_reset_raises_and_decays()`
  - `test_edr_pacer_calm_level_returns_command_unchanged` (function, line 59) `def test_edr_pacer_calm_level_returns_command_unchanged()`
  - `test_target_limiter_caps_concurrency` (function, line 67) `def test_target_limiter_caps_concurrency()`
  - `test_target_limiter_is_reentrant_per_thread` (function, line 93) `def test_target_limiter_is_reentrant_per_thread()`
  - `test_target_limiter_empty_target_bypasses` (function, line 112) `def test_target_limiter_empty_target_bypasses()`
  - `test_fact_vector_store_roundtrip_and_search` (function, line 121) `def test_fact_vector_store_roundtrip_and_search(tmp_path)`
  - `test_fact_vector_store_search_block_rendering` (function, line 141) `def test_fact_vector_store_search_block_rendering(tmp_path)`
  - `_work` (function, line 75) `def _work()`
  - `_work` (function, line 99) `def _work()`
- Depends on: `modules/loop_guardrails.py`

## tests/test_loop_intent_delete.py
- Doc: Intent delete modes regression tests (lazy 0.3.12 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 8) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_soft_delete_keeps_outputs_and_notifies` (function, line 17) `def test_soft_delete_keeps_outputs_and_notifies(tmp_path, monkeypatch)`
  - `test_soft_delete_requires_reason` (function, line 37) `def test_soft_delete_requires_reason(tmp_path, monkeypatch)`
  - `test_hard_delete_removes_exclusive_keeps_shared` (function, line 46) `def test_hard_delete_removes_exclusive_keeps_shared(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_llm_resilience.py
- Doc: LLM retry layers, wall-clock settle, stall-guard (lazy 0.3.8/0.3.9 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_empty_reply_replays_before_failover` (function, line 15) `def test_empty_reply_replays_before_failover(tmp_path, monkeypatch)`
  - `test_empty_budget_exhausted_moves_to_next_member` (function, line 34) `def test_empty_budget_exhausted_moves_to_next_member(tmp_path, monkeypatch)`
  - `test_error_reply_fails_over_instead_of_becoming_content` (function, line 54) `def test_error_reply_fails_over_instead_of_becoming_content(tmp_path, monkeypatch)`
  - `test_worker_llm_steps_filtered_by_scope_and_tooling` (function, line 71) `def test_worker_llm_steps_filtered_by_scope_and_tooling(tmp_path, monkeypatch)`
  - `test_wall_clock_settles_partial_not_hard_kill` (function, line 95) `def test_wall_clock_settles_partial_not_hard_kill(tmp_path, monkeypatch)`
  - `test_stall_guard_forces_intent_when_nothing_open` (function, line 114) `def test_stall_guard_forces_intent_when_nothing_open(tmp_path, monkeypatch)`
  - `test_task_llm_chain_quota_failover` (function, line 135) `def test_task_llm_chain_quota_failover(tmp_path, monkeypatch)`
  - `test_raw_llm_recording_toggle` (function, line 169) `def test_raw_llm_recording_toggle(tmp_path, monkeypatch)`
  - `test_llm_context_budget_roundtrip` (function, line 190) `def test_llm_context_budget_roundtrip(tmp_path, monkeypatch)`
  - `test_planner_uses_bound_task_chain` (function, line 202) `def test_planner_uses_bound_task_chain(tmp_path, monkeypatch)`
  - `scripted` (function, line 23) `def scripted(model, prompt, max_tokens)`
  - `first_empty_then_ok` (function, line 42) `def first_empty_then_ok(model, prompt, max_tokens)`
  - `error_then_ok` (function, line 61) `def error_then_ok(model, prompt, max_tokens)`
  - `scripted` (function, line 79) `def scripted(model, prompt, max_tokens)`
  - `scripted` (function, line 147) `def scripted(model, prompt, max_tokens)`
  - `scripted_next` (function, line 160) `def scripted_next(model, prompt, max_tokens)`
  - `scripted` (function, line 213) `def scripted(model, prompt, max_tokens)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`

## tests/test_loop_mentions.py
- Doc: Lazy mentions multi-type search and scroll pagination.
- Layer: testing
- Language: py
- Symbols:
  - `test_mentions_search_and_cursor` (function, line 6) `def test_mentions_search_and_cursor(tmp_path, monkeypatch)`
  - `test_mentions_parse_caps_and_trusts_ids` (function, line 16) `def test_mentions_parse_caps_and_trusts_ids()`
- Depends on: `modules/__init__.py`

## tests/test_loop_multi_target.py
- Doc: Multi-target loop entry: scope-file parsing, validation and caps.
- Layer: testing
- Language: py
- Symbols:
  - `test_parse_loop_line_accepts_targets_file` (function, line 10) `def test_parse_loop_line_accepts_targets_file(tmp_path)`
  - `test_parse_loop_line_defaults_without_file` (function, line 20) `def test_parse_loop_line_defaults_without_file()`
  - `test_load_targets_file_skips_comments_and_invalid` (function, line 27) `def test_load_targets_file_skips_comments_and_invalid(tmp_path)`
  - `test_load_targets_file_caps_batch` (function, line 38) `def test_load_targets_file_caps_batch(tmp_path)`
  - `test_load_targets_file_missing_raises` (function, line 46) `def test_load_targets_file_missing_raises(tmp_path)`
  - `test_load_targets_file_empty_raises` (function, line 52) `def test_load_targets_file_empty_raises(tmp_path)`
- Depends on: `modules/lazy_runner.py`

## tests/test_loop_nmap_guard.py
- Doc: Loop guardrails: command repair and bounded scanning retests.
- Layer: testing
- Language: py
- Symbols:
  - `_sandbox` (function, line 8) `def _sandbox(tmp_path, monkeypatch)`
  - `test_repair_rejects_target_in_port_slot` (function, line 13) `def test_repair_rejects_target_in_port_slot()`
  - `test_repair_strips_binary_path_for_shell_verb` (function, line 20) `def test_repair_strips_binary_path_for_shell_verb()`
  - `test_repair_keeps_valid_port_specs` (function, line 27) `def test_repair_keeps_valid_port_specs()`
  - `test_repair_appends_missing_target` (function, line 35) `def test_repair_appends_missing_target()`
  - `test_repair_drops_port_flag_without_value` (function, line 41) `def test_repair_drops_port_flag_without_value()`
  - `test_stall_thresholds_follow_command_timeout` (function, line 48) `def test_stall_thresholds_follow_command_timeout()`
  - `test_scan_commands_are_not_replayed` (function, line 58) `def test_scan_commands_are_not_replayed(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_loop.py`, `modules/lazy_runner.py`

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
  - `TestHubRouting` (class, line 18) `class TestHubRouting`
  - `TestIntelMediatorActivityPort` (class, line 38) `class TestIntelMediatorActivityPort`
  - `TestFeedbackMediator` (class, line 61) `class TestFeedbackMediator`
  - `TestTelemetryMediator` (class, line 81) `class TestTelemetryMediator`
  - `TestChainMediatorLlmPort` (class, line 110) `class TestChainMediatorLlmPort`
  - `test_all_default_domains_registered` (method, line 21) `def test_all_default_domains_registered(self)`
  - `test_unknown_domain_returns_none` (method, line 26) `def test_unknown_domain_returns_none(self)`
  - `test_singleton_hub_shared` (method, line 29) `def test_singleton_hub_shared(self)`
  - `test_mediation_contract_shape` (method, line 32) `def test_mediation_contract_shape(self)`
  - `test_activity_records_via_injected_port` (method, line 41) `def test_activity_records_via_injected_port(self)`
  - `test_activity_records_fallback_graceful` (method, line 47) `def test_activity_records_fallback_graceful(self)`
  - `test_mask_and_stack_survive_missing_peers` (method, line 51) `def test_mask_and_stack_survive_missing_peers(self, monkeypatch)`
  - `test_order_steps_passthrough_on_error` (method, line 64) `def test_order_steps_passthrough_on_error(self, monkeypatch)`
  - `test_order_steps_forwarded` (method, line 74) `def test_order_steps_forwarded(self, monkeypatch)`
  - `test_publish_event_default_severity_positional` (method, line 84) `def test_publish_event_default_severity_positional(self, monkeypatch)`
  - `test_publish_event_forwarding_calls_default_path` (method, line 94) `def test_publish_event_forwarding_calls_default_path(self, monkeypatch)`
  - `test_rl_select_graceful_off` (method, line 100) `def test_rl_select_graceful_off(self, monkeypatch)`
  - `test_port_contract` (method, line 113) `def test_port_contract(self)`
  - `test_register_llm_port_replaces` (method, line 121) `def test_register_llm_port_replaces(self)`
  - `_patch_hub` (method, line 134) `def _patch_hub(self, monkeypatch, port)`
  - `test_recovery_pool_absent_returns_empty` (method, line 154) `def test_recovery_pool_absent_returns_empty(self, monkeypatch)`
  - `test_recovery_pool_builds_steps` (method, line 176) `def test_recovery_pool_builds_steps(self, monkeypatch)`
  - `boom` (function, line 67) `def boom(steps, stack)`
  - `boom` (function, line 103) `def boom()`
  - `Fake` (class, line 122) `class Fake`
  - `_FakeHub` (class, line 137) `class _FakeHub`
  - `_NoLock` (class, line 144) `class _NoLock`
  - `Empty` (class, line 157) `class Empty`
  - `FakePort` (class, line 179) `class FakePort`
  - `complete` (method, line 123) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 126) `def has_members(self)`
  - `__init__` (method, line 138) `def __init__(self, port)`
  - `mediator_for` (method, line 141) `def mediator_for(self, domain)`
  - `__enter__` (method, line 145) `def __enter__(self)`
  - `__exit__` (method, line 148) `def __exit__(self)`
  - `complete` (method, line 158) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 161) `def has_members(self)`
  - `complete` (method, line 180) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 183) `def has_members(self)`
- Depends on: `cli/__init__.py`, `modules/chain_runner.py`, `modules/lazy_intel.py`, `modules/lazy_orchestrator_feedback.py`, `modules/loop_ai_bridge.py`, `modules/mediation/__init__.py`, `modules/mediation/hub.py`

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


Next: [KB_tests_p14.md](KB_tests_p14.md)
