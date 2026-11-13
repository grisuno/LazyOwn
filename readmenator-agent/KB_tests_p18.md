# Subsystem: tests (page 18 of 26)
Previous: [KB_tests_p17.md](KB_tests_p17.md)

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
  - `test_loop_exit_code_mapping` (function, line 10) `def test_loop_exit_code_mapping()`
  - `test_autonomous_gate_raises_only_when_env_set` (function, line 28) `def test_autonomous_gate_raises_only_when_env_set(monkeypatch)`
  - `test_write_loop_result_workspace` (function, line 47) `def test_write_loop_result_workspace(tmp_path, monkeypatch)`
  - `test_write_loop_result_sessions_fallback` (function, line 63) `def test_write_loop_result_sessions_fallback(tmp_path, monkeypatch)`
  - `_ExitShell` (class, line 75) `class _ExitShell`
  - `test_headless_catches_systemexit` (function, line 83) `def test_headless_catches_systemexit()`
  - `test_headless_chain_stops_on_failure` (function, line 93) `def test_headless_chain_stops_on_failure()`
  - `test_report_result_prints_verdict` (function, line 114) `def test_report_result_prints_verdict(capsys)`
  - `__init__` (method, line 76) `def __init__(self, code)`
  - `onecmd` (method, line 79) `def onecmd(self, cmd)`
  - `_Shell` (class, line 96) `class _Shell`
  - `__init__` (method, line 97) `def __init__(self)`
  - `onecmd` (method, line 100) `def onecmd(self, cmd)`
- Depends on: `cli/headless.py`, `modules/__init__.py`, `modules/lazy_runner.py`

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
  - `test_lab_state_maps_running_and_stopped` (function, line 10) `def test_lab_state_maps_running_and_stopped()`
  - `test_check_target_fails_fast_on_stopped_lab` (function, line 41) `def test_check_target_fails_fast_on_stopped_lab()`
  - `test_check_target_passes_on_running_lab` (function, line 54) `def test_check_target_passes_on_running_lab()`
  - `test_check_target_probes_tcp` (function, line 65) `def test_check_target_probes_tcp(monkeypatch)`
  - `test_check_target_refused_means_alive` (function, line 84) `def test_check_target_refused_means_alive(monkeypatch)`
  - `test_check_target_without_target` (function, line 96) `def test_check_target_without_target()`
  - `test_probe_tcp_real_socket` (function, line 104) `def test_probe_tcp_real_socket()`
  - `test_no_preflight_hint_override` (function, line 130) `def test_no_preflight_hint_override()`
  - `test_preflight_flag_parses` (function, line 138) `def test_preflight_flag_parses()`
  - `_accept` (function, line 112) `def _accept()`
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

## tests/test_loop_target_authority.py
- Doc: Target authority: --target rebinds payload rhost and scope.
- Layer: testing
- Language: py
- Symbols:
  - `_FakeShell` (class, line 16) `class _FakeShell`
  - `test_single_target_replaces_rhost_and_scope` (function, line 31) `def test_single_target_replaces_rhost_and_scope()`
  - `test_multi_target_scope_is_every_target` (function, line 42) `def test_multi_target_scope_is_every_target()`
  - `test_dedupes_and_strips` (function, line 49) `def test_dedupes_and_strips()`
  - `test_noop_when_already_bound` (function, line 55) `def test_noop_when_already_bound()`
  - `test_enforcement_mode_untouched` (function, line 62) `def test_enforcement_mode_untouched()`
  - `test_empty_targets_is_noop` (function, line 68) `def test_empty_targets_is_noop()`
  - `test_fallback_writer_without_scope_save` (function, line 75) `def test_fallback_writer_without_scope_save(monkeypatch)`
  - `__init__` (method, line 19) `def __init__(self, params)`
  - `_scope_save` (method, line 23) `def _scope_save(self, entries, mode)`
  - `_fake_save` (function, line 78) `def _fake_save(params)`
  - `_Bare` (class, line 83) `class _Bare`
  - `__init__` (method, line 84) `def __init__(self)`
- Depends on: `modules/lazy_runner.py`

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
  - `_package_names` (function, line 29) `def _package_names()`
  - `_registered` (function, line 33) `def _registered()`
  - `_fallback_branches` (function, line 50) `def _fallback_branches()`
  - `TestRegistryDispatch` (class, line 61) `class TestRegistryDispatch`
  - `test_set_config_refuses_null_values` (function, line 79) `def test_set_config_refuses_null_values()`
  - `test_new_chain_shell_tools_have_defs_and_handlers` (function, line 99) `def test_new_chain_shell_tools_have_defs_and_handlers()`
  - `test_opencode_bridge_curates_loop_and_chain` (function, line 106) `def test_opencode_bridge_curates_loop_and_chain()`
  - `test_mcp_never_offers_interactive_repl` (function, line 121) `def test_mcp_never_offers_interactive_repl()`
  - `test_no_dead_duplicate_branches` (method, line 62) `def test_no_dead_duplicate_branches(self)`
  - `test_migrated_handlers_registered` (method, line 66) `def test_migrated_handlers_registered(self)`
  - `test_migrated_handlers_absent_from_fallback` (method, line 71) `def test_migrated_handlers_absent_from_fallback(self)`


Next: [KB_tests_p19.md](KB_tests_p19.md)
