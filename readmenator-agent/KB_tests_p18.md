# Subsystem: tests (page 18 of 27)
Previous: [KB_tests_p17.md](KB_tests_p17.md)

## tests/test_loop_auto_orchestrator.py
- Doc: Loop orchestrates every auto verb plus addon/tool triggers.
- Layer: testing
- Language: py
- Symbols:
  - `test_exfil_auto_registered_as_verb` (function, line 6) `def test_exfil_auto_registered_as_verb()`
  - `test_service_tokens_split_and_alias` (function, line 15) `def test_service_tokens_split_and_alias()`
  - `test_addon_hits_rank_specific_before_generic` (function, line 22) `def test_addon_hits_rank_specific_before_generic()`
  - `test_propose_addon_intents_shape_and_tool_collapse` (function, line 31) `def test_propose_addon_intents_shape_and_tool_collapse()`
  - `test_steps_for_lazy_addon_routes_to_command` (function, line 40) `def test_steps_for_lazy_addon_routes_to_command()`
  - `test_worker_routes_verbs_via_bound_shell` (function, line 49) `def test_worker_routes_verbs_via_bound_shell(tmp_path, monkeypatch)`
  - `test_worker_without_shell_reports_honestly` (function, line 85) `def test_worker_without_shell_reports_honestly(tmp_path, monkeypatch)`
  - `test_execute_streaming_streams_and_captures` (function, line 109) `def test_execute_streaming_streams_and_captures()`
  - `test_execute_streaming_timeout_reports` (function, line 119) `def test_execute_streaming_timeout_reports()`
  - `test_execute_shell_verb_forwards_output` (function, line 127) `def test_execute_shell_verb_forwards_output()`
  - `test_autonomous_mode_suppresses_and_restores_input` (function, line 141) `def test_autonomous_mode_suppresses_and_restores_input(monkeypatch)`
  - `test_lazy_addon_command_registered` (function, line 153) `def test_lazy_addon_command_registered()`
  - `test_worker_skips_missing_binary_and_records_gap` (function, line 163) `def test_worker_skips_missing_binary_and_records_gap(tmp_path, monkeypatch)`
  - `test_service_trigger_fires_with_addon_hits` (function, line 194) `def test_service_trigger_fires_with_addon_hits(tmp_path, monkeypatch)`
  - `_Shell` (class, line 59) `class _Shell`
  - `_Shell` (class, line 131) `class _Shell`
  - `onecmd` (method, line 60) `def onecmd(self, command)`
  - `onecmd_plus_hooks` (method, line 132) `def onecmd_plus_hooks(self, command)`
- Depends on: `cli/commands/mcp_bridge.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_broadcast.py
- Doc: Broadcast board timeline regression tests (lazy 0.3.12 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_broadcast_rows_carry_neighbours_and_assets` (function, line 15) `def test_broadcast_rows_carry_neighbours_and_assets(tmp_path, monkeypatch)`
  - `test_broadcast_search_id_and_kind_filter` (function, line 36) `def test_broadcast_search_id_and_kind_filter(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

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
  - `test_multi_phase_verb_visible_in_each_declared_phase` (function, line 101) `def test_multi_phase_verb_visible_in_each_declared_phase(sandbox, monkeypatch)`
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

## tests/test_loop_decision_log.py
- Doc: Tests for the reproducible loop decision ledger and planner determinism.
- Layer: testing
- Language: py
- Symbols:
  - `_Ctx` (class, line 20) `class _Ctx`
  - `test_digest_is_stable_and_bounded` (function, line 33) `def test_digest_is_stable_and_bounded()`
  - `test_context_digest_ignores_mapping_order` (function, line 40) `def test_context_digest_ignores_mapping_order()`
  - `test_context_digest_ignores_service_order` (function, line 46) `def test_context_digest_ignores_service_order()`
  - `test_context_digest_changes_with_state` (function, line 52) `def test_context_digest_changes_with_state()`
  - `test_config_digest_only_tracks_relevant_keys` (function, line 59) `def test_config_digest_only_tracks_relevant_keys()`
  - `test_config_digest_empty_inputs` (function, line 67) `def test_config_digest_empty_inputs()`
  - `test_config_digest_tracks_determinism_flags` (function, line 73) `def test_config_digest_tracks_determinism_flags()`
  - `test_record_and_read_round_trip` (function, line 80) `def test_record_and_read_round_trip(tmp_path)`
  - `test_read_records_skips_corrupt_lines` (function, line 101) `def test_read_records_skips_corrupt_lines(tmp_path)`
  - `test_record_marks_model_fallback_for_llm` (function, line 108) `def test_record_marks_model_fallback_for_llm(tmp_path)`
  - `test_record_never_raises_on_bad_path` (function, line 127) `def test_record_never_raises_on_bad_path(tmp_path)`
  - `test_filtered_rows_bounds_and_shape` (function, line 134) `def test_filtered_rows_bounds_and_shape()`
  - `test_extract_json_contract` (function, line 140) `def test_extract_json_contract()`
  - `test_extract_json_fenced_block` (function, line 145) `def test_extract_json_fenced_block()`
  - `test_extract_json_string_array` (function, line 150) `def test_extract_json_string_array()`
  - `test_extract_line_fallback_on_non_json` (function, line 154) `def test_extract_line_fallback_on_non_json()`
  - `test_extract_dedupes_preserving_order` (function, line 162) `def test_extract_dedupes_preserving_order()`
  - `test_extract_empty_reply` (function, line 166) `def test_extract_empty_reply()`
  - `test_planner_temperature_default_is_greedy` (function, line 171) `def test_planner_temperature_default_is_greedy(monkeypatch)`
  - `test_planner_temperature_reads_payload` (function, line 179) `def test_planner_temperature_reads_payload(monkeypatch)`
  - `test_planner_temperature_clamps_negative` (function, line 188) `def test_planner_temperature_clamps_negative(monkeypatch)`
  - `test_planner_temperature_survives_malformed` (function, line 197) `def test_planner_temperature_survives_malformed(monkeypatch)`
  - `__init__` (method, line 23) `def __init__(self, extra, services)`
- Depends on: `core/config.py`, `modules/lazy_loop.py`, `modules/loop/__init__.py`, `modules/loop/worker_agentic.py`

## tests/test_loop_deterministic_mode.py
- Doc: Tests for the reproducible loop mode that prefers heuristic steps.
- Layer: testing
- Language: py
- Symbols:
  - `_Activity` (class, line 17) `class _Activity`
  - `_Worker` (class, line 27) `class _Worker(WorkerAgenticMixin)`
  - `_intent` (function, line 39) `def _intent()`
  - `test_is_placeholder_detects_no_target` (function, line 43) `def test_is_placeholder_detects_no_target()`
  - `test_default_mode_prefixes_llm` (function, line 49) `def test_default_mode_prefixes_llm(monkeypatch)`
  - `test_deterministic_mode_heuristic_wins_and_skips_model` (function, line 57) `def test_deterministic_mode_heuristic_wins_and_skips_model(monkeypatch)`
  - `test_deterministic_mode_falls_back_to_model_on_placeholder` (function, line 65) `def test_deterministic_mode_falls_back_to_model_on_placeholder(monkeypatch)`
  - `test_deterministic_fallback_orders_heuristic_first` (function, line 72) `def test_deterministic_fallback_orders_heuristic_first(monkeypatch)`
  - `test_deterministic_mode_enforces_guard_and_records_decision` (function, line 84) `def test_deterministic_mode_enforces_guard_and_records_decision(monkeypatch, tmp_path)`
  - `test_loop_deterministic_reads_payload` (function, line 111) `def test_loop_deterministic_reads_payload(monkeypatch)`
  - `test_loop_deterministic_survives_error` (function, line 120) `def test_loop_deterministic_survives_error(monkeypatch)`
  - `__init__` (method, line 20) `def __init__(self)`
  - `emit` (method, line 23) `def emit(self)`
  - `__init__` (method, line 30) `def __init__(self, suggested)`
  - `_llm_steps` (method, line 35) `def _llm_steps(self, intent, prior_text)`
  - `_PlaceholderThenReal` (class, line 75) `class _PlaceholderThenReal(_Worker)`
  - `_boom` (function, line 123) `def _boom()`
  - `_llm_steps` (method, line 76) `def _llm_steps(self, intent, prior_text)`
- Depends on: `core/config.py`, `modules/guard_rules.py`, `modules/loop/__init__.py`, `modules/loop/worker_agentic.py`

## tests/test_loop_evidence_wiring.py
- Doc: BDD tests for the loop evidence loop-closure wiring.
- Layer: testing
- Language: py
- Symbols:
  - `sink_log` (function, line 27) `def sink_log()`
  - `_worker` (function, line 49) `def _worker(task_id)`
  - `_intent` (function, line 56) `def _intent(node_id)`
  - `TestShellProofPublication` (class, line 61) `class TestShellProofPublication`
  - `TestWorkerTraces` (class, line 83) `class TestWorkerTraces`
  - `TestTrafficDigest` (class, line 131) `class TestTrafficDigest`
  - `TestEvidenceDualHash` (class, line 142) `class TestEvidenceDualHash`
  - `TestContracts` (class, line 170) `class TestContracts`
  - `fake_record` (function, line 34) `def fake_record()`
  - `test_publishes_exploit_event_with_shell_flag` (method, line 62) `def test_publishes_exploit_event_with_shell_flag(self, sink_log)`
  - `test_junk_output_never_publishes` (method, line 71) `def test_junk_output_never_publishes(self, sink_log)`
  - `test_no_target_no_event` (method, line 77) `def test_no_target_no_event(self, sink_log)`
  - `test_rows_written_reader_schema` (method, line 84) `def test_rows_written_reader_schema(self, tmp_path)`
  - `test_rotation_keeps_tail` (method, line 103) `def test_rotation_keeps_tail(self, tmp_path)`
  - `test_empty_transcripts_write_nothing` (method, line 120) `def test_empty_transcripts_write_nothing(self, tmp_path)`
  - `test_same_output_same_digest_other_output_differs` (method, line 132) `def test_same_output_same_digest_other_output_differs(self)`
  - `test_full_body_hash_and_stored_hash` (method, line 143) `def test_full_body_hash_and_stored_hash(self, tmp_path)`
  - `test_tamper_detected` (method, line 156) `def test_tamper_detected(self, tmp_path)`
  - `test_wiring_sources` (method, line 171) `def test_wiring_sources(self)`
- Depends on: `modules/__init__.py`, `modules/lazy_loop.py`, `modules/outcome_bus.py`

## tests/test_loop_exit_gate.py
- Doc: Honest loop endings: exit-code mapping, autonomous gate and headless runner.
- Layer: testing
- Language: py
- Symbols:
  - `_abort_cause_literals` (function, line 14) `def _abort_cause_literals(source)`
  - `test_terminal_autopwn_fallback_cause_is_valid` (function, line 36) `def test_terminal_autopwn_fallback_cause_is_valid()`
  - `test_every_abort_call_site_uses_a_registered_cause` (function, line 42) `def test_every_abort_call_site_uses_a_registered_cause()`
  - `test_loop_exit_code_mapping` (function, line 55) `def test_loop_exit_code_mapping()`
  - `test_autonomous_gate_raises_only_when_env_set` (function, line 90) `def test_autonomous_gate_raises_only_when_env_set(monkeypatch)`
  - `test_write_loop_result_workspace` (function, line 109) `def test_write_loop_result_workspace(tmp_path, monkeypatch)`
  - `test_write_loop_result_sessions_fallback` (function, line 125) `def test_write_loop_result_sessions_fallback(tmp_path, monkeypatch)`
  - `_ExitShell` (class, line 137) `class _ExitShell`
  - `test_headless_catches_systemexit` (function, line 145) `def test_headless_catches_systemexit()`
  - `test_headless_chain_stops_on_failure` (function, line 155) `def test_headless_chain_stops_on_failure()`
  - `test_report_result_prints_verdict` (function, line 176) `def test_report_result_prints_verdict(capsys)`
  - `__init__` (method, line 138) `def __init__(self, code)`
  - `onecmd` (method, line 141) `def onecmd(self, cmd)`
  - `_Shell` (class, line 158) `class _Shell`
  - `__init__` (method, line 159) `def __init__(self)`
  - `onecmd` (method, line 162) `def onecmd(self, cmd)`
- Depends on: `cli/headless.py`, `modules/__init__.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`

## tests/test_loop_fire_pending.py
- Doc: Vertical test: fire-pending intelligence drives a real auto_loop round.
- Layer: testing
- Language: py
- Symbols:
  - `_RecordingShell` (class, line 33) `class _RecordingShell`
  - `fire_report` (function, line 45) `def fire_report(tmp_path, monkeypatch)`
  - `TestCascadeFirePending` (class, line 63) `class TestCascadeFirePending`
  - `TestPlannerFireIntent` (class, line 75) `class TestPlannerFireIntent`
  - `TestWorkerExecutesFireAction` (class, line 105) `class TestWorkerExecutesFireAction`
  - `TestRegistry` (class, line 157) `class TestRegistry`
  - `__init__` (method, line 36) `def __init__(self)`
  - `onecmd_plus_hooks` (method, line 39) `def onecmd_plus_hooks(self, line)`
  - `test_cascade_answers_fire_first` (method, line 64) `def test_cascade_answers_fire_first(self, fire_report)`
  - `test_planner_queues_fire_action` (method, line 76) `def test_planner_queues_fire_action(self, fire_report, monkeypatch)`
  - `test_planner_dedupes_after_first_proposal` (method, line 91) `def test_planner_dedupes_after_first_proposal(self, fire_report, monkeypatch)`
  - `test_steps_expand_verbatim` (method, line 106) `def test_steps_expand_verbatim(self)`
  - `test_registry_routes_and_shell_receives` (method, line 128) `def test_registry_routes_and_shell_receives(self)`
  - `test_lazy_intel_verbs_routable` (method, line 158) `def test_lazy_intel_verbs_routable(self)`
- Depends on: `modules/auto_registry.py`, `modules/lazy_autofire.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/selection/__init__.py`, `modules/selection/base.py`, `modules/selection/intel.py`

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
  - `test_listing_noise_flags_recursive_session_dump` (function, line 152) `def test_listing_noise_flags_recursive_session_dump()`
  - `test_listing_noise_ignores_real_postexp_find_output` (function, line 161) `def test_listing_noise_ignores_real_postexp_find_output()`
  - `test_listing_noise_ignores_small_and_banner_outputs` (function, line 170) `def test_listing_noise_ignores_small_and_banner_outputs()`
  - `test_listing_policy_vetoes_ls_family` (function, line 181) `def test_listing_policy_vetoes_ls_family()`
  - `test_listing_policy_allows_find_with_filters_and_work` (function, line 190) `def test_listing_policy_allows_find_with_filters_and_work()`
  - `test_listing_policy_rejects_bare_find` (function, line 199) `def test_listing_policy_rejects_bare_find()`
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
  - `test_raw_llm_recording_carries_task_and_model` (function, line 190) `def test_raw_llm_recording_carries_task_and_model(tmp_path, monkeypatch)`
  - `test_llm_context_budget_roundtrip` (function, line 213) `def test_llm_context_budget_roundtrip(tmp_path, monkeypatch)`
  - `test_planner_uses_bound_task_chain` (function, line 225) `def test_planner_uses_bound_task_chain(tmp_path, monkeypatch)`
  - `scripted` (function, line 23) `def scripted(model, prompt, max_tokens)`
  - `first_empty_then_ok` (function, line 42) `def first_empty_then_ok(model, prompt, max_tokens)`
  - `error_then_ok` (function, line 61) `def error_then_ok(model, prompt, max_tokens)`
  - `scripted` (function, line 79) `def scripted(model, prompt, max_tokens)`
  - `scripted` (function, line 147) `def scripted(model, prompt, max_tokens)`
  - `scripted_next` (function, line 160) `def scripted_next(model, prompt, max_tokens)`
  - `scripted` (function, line 236) `def scripted(model, prompt, max_tokens)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`

## tests/test_loop_manager.py
- Doc: Tests for modules.loop_manager — safe autonomous loop orchestration.
- Layer: testing
- Language: py
- Symbols:
  - `loops_dir` (function, line 37) `def loops_dir()`
  - `stub_script` (function, line 43) `def stub_script(tmp_path)`
  - `manager` (function, line 56) `def manager(loops_dir, stub_script)`
  - `TestValidateTarget` (class, line 64) `class TestValidateTarget`
  - `TestSanitizeGoal` (class, line 95) `class TestSanitizeGoal`
  - `TestClampInt` (class, line 123) `class TestClampInt`
  - `TestValidateLoopId` (class, line 138) `class TestValidateLoopId`
  - `TestSpawnAndRegistry` (class, line 151) `class TestSpawnAndRegistry`
  - `TestLogReading` (class, line 222) `class TestLogReading`
  - `TestStop` (class, line 251) `class TestStop`
  - `TestLifecycle` (class, line 281) `class TestLifecycle`
  - `test_accepts_ipv4` (method, line 65) `def test_accepts_ipv4(self)`
  - `test_accepts_ipv6` (method, line 68) `def test_accepts_ipv6(self)`
  - `test_strips_whitespace` (method, line 71) `def test_strips_whitespace(self)`
  - `test_rejects_hostname` (method, line 74) `def test_rejects_hostname(self)`
  - `test_rejects_command_injection` (method, line 78) `def test_rejects_command_injection(self)`
  - `test_rejects_metacharacters` (method, line 82) `def test_rejects_metacharacters(self)`
  - `test_rejects_non_string` (method, line 86) `def test_rejects_non_string(self)`
  - `test_rejects_empty` (method, line 90) `def test_rejects_empty(self)`
  - `test_defaults_on_empty` (method, line 96) `def test_defaults_on_empty(self)`
  - `test_collapses_whitespace` (method, line 100) `def test_collapses_whitespace(self)`
  - `test_rejects_newlines` (method, line 103) `def test_rejects_newlines(self)`
  - `test_rejects_quotes` (method, line 107) `def test_rejects_quotes(self)`
  - `test_rejects_semicolons` (method, line 111) `def test_rejects_semicolons(self)`
  - `test_rejects_too_long` (method, line 115) `def test_rejects_too_long(self)`
  - `test_accepts_plain_words` (method, line 119) `def test_accepts_plain_words(self)`
  - `test_default_on_none` (method, line 124) `def test_default_on_none(self)`
  - `test_clamps_low` (method, line 127) `def test_clamps_low(self)`
  - `test_clamps_high` (method, line 130) `def test_clamps_high(self)`
  - `test_rejects_non_numeric` (method, line 133) `def test_rejects_non_numeric(self)`
  - `test_accepts_hex32` (method, line 139) `def test_accepts_hex32(self)`
  - `test_rejects_traversal` (method, line 142) `def test_rejects_traversal(self)`
  - `test_rejects_non_hex` (method, line 146) `def test_rejects_non_hex(self)`
  - `test_start_spawns_and_records` (method, line 152) `def test_start_spawns_and_records(self, manager, loops_dir)`
  - `test_argv_has_no_shell` (method, line 164) `def test_argv_has_no_shell(self, manager)`
  - `test_invalid_kind_rejected` (method, line 179) `def test_invalid_kind_rejected(self, manager)`
  - `test_invalid_target_rejected` (method, line 183) `def test_invalid_target_rejected(self, manager)`
  - `test_concurrency_cap` (method, line 187) `def test_concurrency_cap(self, manager)`
  - `test_list_loops_sorted_newest_first` (method, line 195) `def test_list_loops_sorted_newest_first(self, manager)`
  - `test_registry_survives_restart` (method, line 205) `def test_registry_survives_restart(self, manager, loops_dir)`
  - `test_metadata_written` (method, line 212) `def test_metadata_written(self, manager, loops_dir)`
  - `test_read_log_chunk` (method, line 223) `def test_read_log_chunk(self, manager, loops_dir)`
  - `test_read_log_unknown_loop` (method, line 231) `def test_read_log_unknown_loop(self, manager)`
  - `test_read_log_confinement` (method, line 235) `def test_read_log_confinement(self, manager, loops_dir)`
  - `test_read_log_offset_beyond_size` (method, line 243) `def test_read_log_offset_beyond_size(self, manager)`
  - `test_stop_terminates_process` (method, line 252) `def test_stop_terminates_process(self, manager)`
  - `test_stop_unknown_loop` (method, line 264) `def test_stop_unknown_loop(self, manager)`
  - `test_stop_finished_loop_rejected` (method, line 268) `def test_stop_finished_loop_rejected(self, manager)`
  - `test_quick_exit_marks_finished` (method, line 282) `def test_quick_exit_marks_finished(self, loops_dir, tmp_path)`
  - `test_sigterm_resistant_process_is_killed` (method, line 297) `def test_sigterm_resistant_process_is_killed(self, loops_dir, tmp_path)`
  - `test_summary_shape` (method, line 314) `def test_summary_shape(self, manager)`
- Depends on: `modules/loop_manager.py`

## tests/test_loop_manager_outcome.py
- Doc: Loop manager outcome propagation: workspace result.json drives status.
- Layer: testing
- Language: py
- Symbols:
  - `manager` (function, line 12) `def manager(tmp_path)`
  - `_register` (function, line 18) `def _register(manager, loop_id, workspace)`
  - `_FakeProcess` (class, line 48) `class _FakeProcess`
  - `test_read_outcome_parses_result_json` (function, line 56) `def test_read_outcome_parses_result_json(manager, tmp_path)`
  - `test_reap_marks_failed_on_honest_outcome` (function, line 68) `def test_reap_marks_failed_on_honest_outcome(manager, tmp_path)`
  - `test_reap_marks_finished_on_success` (function, line 87) `def test_reap_marks_finished_on_success(manager, tmp_path)`
  - `test_reap_falls_back_to_exit_code_without_outcome` (function, line 103) `def test_reap_falls_back_to_exit_code_without_outcome(manager, tmp_path)`
  - `test_reap_stopped_overrides_outcome` (function, line 116) `def test_reap_stopped_overrides_outcome(manager, tmp_path)`
  - `test_reap_cancelled_outcome_maps_stopped` (function, line 130) `def test_reap_cancelled_outcome_maps_stopped(manager, tmp_path)`
  - `test_spawn_binds_workspace_env` (function, line 145) `def test_spawn_binds_workspace_env(manager, tmp_path, monkeypatch)`
  - `__init__` (method, line 49) `def __init__(self, exit_code)`
  - `wait` (method, line 52) `def wait(self)`
  - `_FakePopen` (class, line 150) `class _FakePopen`
  - `_fake_reap` (function, line 161) `def _fake_reap(self, loop_id, process)`
  - `__init__` (method, line 151) `def __init__(self, argv)`
- Depends on: `modules/__init__.py`

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

## tests/test_loop_preflight.py
- Doc: Target preflight for loops and auto_pwn: lab state and TCP reachability.
- Layer: testing
- Language: py
- Symbols:
  - `test_lab_state_maps_running_and_stopped` (function, line 8) `def test_lab_state_maps_running_and_stopped()`
  - `test_check_target_fails_fast_on_stopped_lab` (function, line 39) `def test_check_target_fails_fast_on_stopped_lab()`
  - `test_check_target_passes_on_running_lab` (function, line 52) `def test_check_target_passes_on_running_lab()`
  - `test_check_target_probes_tcp` (function, line 63) `def test_check_target_probes_tcp(monkeypatch)`
  - `test_check_target_refused_means_alive` (function, line 82) `def test_check_target_refused_means_alive(monkeypatch)`
  - `test_check_target_without_target` (function, line 94) `def test_check_target_without_target()`
  - `test_probe_tcp_real_socket` (function, line 102) `def test_probe_tcp_real_socket()`
  - `test_no_preflight_hint_override` (function, line 128) `def test_no_preflight_hint_override()`
  - `test_preflight_flag_parses` (function, line 136) `def test_preflight_flag_parses()`
  - `_accept` (function, line 110) `def _accept()`
- Depends on: `modules/__init__.py`, `modules/lazy_runner.py`

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


Next: [KB_tests_p19.md](KB_tests_p19.md)
