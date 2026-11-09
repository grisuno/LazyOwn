# Symbols (page 44 of 50)
Previous: [SYMBOLS_p43.md](SYMBOLS_p43.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_intent` | function | `tests/test_loop_evidence_wiring.py:56` | `def _intent(node_id)` |
| `_worker` | function | `tests/test_loop_evidence_wiring.py:49` | `def _worker(task_id)` |
| `fake_record` | function | `tests/test_loop_evidence_wiring.py:34` | `def fake_record()` |
| `sink_log` | function | `tests/test_loop_evidence_wiring.py:27` | `def sink_log()` |
| `test_empty_transcripts_write_nothing` | method | `tests/test_loop_evidence_wiring.py:120` | `def test_empty_transcripts_write_nothing(self, tmp_path)` |
| `test_full_body_hash_and_stored_hash` | method | `tests/test_loop_evidence_wiring.py:143` | `def test_full_body_hash_and_stored_hash(self, tmp_path)` |
| `test_junk_output_never_publishes` | method | `tests/test_loop_evidence_wiring.py:71` | `def test_junk_output_never_publishes(self, sink_log)` |
| `test_no_target_no_event` | method | `tests/test_loop_evidence_wiring.py:77` | `def test_no_target_no_event(self, sink_log)` |
| `test_publishes_exploit_event_with_shell_flag` | method | `tests/test_loop_evidence_wiring.py:62` | `def test_publishes_exploit_event_with_shell_flag(self, sink_log)` |
| `test_rotation_keeps_tail` | method | `tests/test_loop_evidence_wiring.py:103` | `def test_rotation_keeps_tail(self, tmp_path)` |
| `test_rows_written_reader_schema` | method | `tests/test_loop_evidence_wiring.py:84` | `def test_rows_written_reader_schema(self, tmp_path)` |
| `test_same_output_same_digest_other_output_differs` | method | `tests/test_loop_evidence_wiring.py:132` | `def test_same_output_same_digest_other_output_differs(self)` |
| `test_tamper_detected` | method | `tests/test_loop_evidence_wiring.py:156` | `def test_tamper_detected(self, tmp_path)` |
| `test_wiring_sources` | method | `tests/test_loop_evidence_wiring.py:171` | `def test_wiring_sources(self)` |
| `TestCascadeFirePending` | class | `tests/test_loop_fire_pending.py:63` | `class TestCascadeFirePending` |
| `TestPlannerFireIntent` | class | `tests/test_loop_fire_pending.py:75` | `class TestPlannerFireIntent` |
| `TestRegistry` | class | `tests/test_loop_fire_pending.py:157` | `class TestRegistry` |
| `TestWorkerExecutesFireAction` | class | `tests/test_loop_fire_pending.py:105` | `class TestWorkerExecutesFireAction` |
| `_RecordingShell` | class | `tests/test_loop_fire_pending.py:33` | `class _RecordingShell` |
| `__init__` | method | `tests/test_loop_fire_pending.py:36` | `def __init__(self)` |
| `fire_report` | function | `tests/test_loop_fire_pending.py:45` | `def fire_report(tmp_path, monkeypatch)` |
| `onecmd_plus_hooks` | method | `tests/test_loop_fire_pending.py:39` | `def onecmd_plus_hooks(self, line)` |
| `test_cascade_answers_fire_first` | method | `tests/test_loop_fire_pending.py:64` | `def test_cascade_answers_fire_first(self, fire_report)` |
| `test_lazy_intel_verbs_routable` | method | `tests/test_loop_fire_pending.py:158` | `def test_lazy_intel_verbs_routable(self)` |
| `test_planner_dedupes_after_first_proposal` | method | `tests/test_loop_fire_pending.py:91` | `def test_planner_dedupes_after_first_proposal(self, fire_report, monkeypatch)` |
| `test_planner_queues_fire_action` | method | `tests/test_loop_fire_pending.py:76` | `def test_planner_queues_fire_action(self, fire_report, monkeypatch)` |
| `test_registry_routes_and_shell_receives` | method | `tests/test_loop_fire_pending.py:128` | `def test_registry_routes_and_shell_receives(self)` |
| `test_steps_expand_verbatim` | method | `tests/test_loop_fire_pending.py:106` | `def test_steps_expand_verbatim(self)` |
| `_patched_engine` | function | `tests/test_loop_force_graph.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_graph_context_surfaces_hubs_and_next` | function | `tests/test_loop_force_graph.py:32` | `def test_graph_context_surfaces_hubs_and_next(tmp_path, monkeypatch)` |
| `test_loop_graph_is_forcegraph_ready` | function | `tests/test_loop_force_graph.py:15` | `def test_loop_graph_is_forcegraph_ready(tmp_path, monkeypatch)` |
| `test_planner_force_ranks_connected_surface` | function | `tests/test_loop_force_graph.py:53` | `def test_planner_force_ranks_connected_surface(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_guard_audit.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_audit_filters_action_source_query` | function | `tests/test_loop_guard_audit.py:31` | `def test_audit_filters_action_source_query(tmp_path, monkeypatch)` |
| `test_check_mints_tool_use_id` | function | `tests/test_loop_guard_audit.py:15` | `def test_check_mints_tool_use_id(tmp_path, monkeypatch)` |
| `test_lookup_jumps_to_execution` | function | `tests/test_loop_guard_audit.py:48` | `def test_lookup_jumps_to_execution(tmp_path, monkeypatch)` |
| `_work` | function | `tests/test_loop_guardrails.py:75` | `def _work()` |
| `_work` | function | `tests/test_loop_guardrails.py:99` | `def _work()` |
| `test_edr_pacer_calm_level_returns_command_unchanged` | function | `tests/test_loop_guardrails.py:59` | `def test_edr_pacer_calm_level_returns_command_unchanged()` |
| `test_edr_pacer_connection_reset_raises_and_decays` | function | `tests/test_loop_guardrails.py:47` | `def test_edr_pacer_connection_reset_raises_and_decays()` |
| `test_edr_pacer_slow_scan_raises_level` | function | `tests/test_loop_guardrails.py:35` | `def test_edr_pacer_slow_scan_raises_level()` |
| `test_fact_vector_store_roundtrip_and_search` | function | `tests/test_loop_guardrails.py:121` | `def test_fact_vector_store_roundtrip_and_search(tmp_path)` |
| `test_fact_vector_store_search_block_rendering` | function | `tests/test_loop_guardrails.py:141` | `def test_fact_vector_store_search_block_rendering(tmp_path)` |
| `test_repeat_detector_flags_identical_window` | function | `tests/test_loop_guardrails.py:12` | `def test_repeat_detector_flags_identical_window()` |
| `test_repeat_detector_recovery_on_variation` | function | `tests/test_loop_guardrails.py:21` | `def test_repeat_detector_recovery_on_variation()` |
| `test_target_limiter_caps_concurrency` | function | `tests/test_loop_guardrails.py:67` | `def test_target_limiter_caps_concurrency()` |
| `test_target_limiter_empty_target_bypasses` | function | `tests/test_loop_guardrails.py:112` | `def test_target_limiter_empty_target_bypasses()` |
| `test_target_limiter_is_reentrant_per_thread` | function | `tests/test_loop_guardrails.py:93` | `def test_target_limiter_is_reentrant_per_thread()` |
| `_patched_engine` | function | `tests/test_loop_intent_delete.py:8` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_hard_delete_removes_exclusive_keeps_shared` | function | `tests/test_loop_intent_delete.py:46` | `def test_hard_delete_removes_exclusive_keeps_shared(tmp_path, monkeypatch)` |
| `test_soft_delete_keeps_outputs_and_notifies` | function | `tests/test_loop_intent_delete.py:17` | `def test_soft_delete_keeps_outputs_and_notifies(tmp_path, monkeypatch)` |
| `test_soft_delete_requires_reason` | function | `tests/test_loop_intent_delete.py:37` | `def test_soft_delete_requires_reason(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_llm_resilience.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `error_then_ok` | function | `tests/test_loop_llm_resilience.py:61` | `def error_then_ok(model, prompt, max_tokens)` |
| `first_empty_then_ok` | function | `tests/test_loop_llm_resilience.py:42` | `def first_empty_then_ok(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:23` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:79` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:147` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:236` | `def scripted(model, prompt, max_tokens)` |
| `scripted_next` | function | `tests/test_loop_llm_resilience.py:160` | `def scripted_next(model, prompt, max_tokens)` |
| `test_empty_budget_exhausted_moves_to_next_member` | function | `tests/test_loop_llm_resilience.py:34` | `def test_empty_budget_exhausted_moves_to_next_member(tmp_path, monkeypatch)` |
| `test_empty_reply_replays_before_failover` | function | `tests/test_loop_llm_resilience.py:15` | `def test_empty_reply_replays_before_failover(tmp_path, monkeypatch)` |
| `test_error_reply_fails_over_instead_of_becoming_content` | function | `tests/test_loop_llm_resilience.py:54` | `def test_error_reply_fails_over_instead_of_becoming_content(tmp_path, monkeypatch)` |
| `test_llm_context_budget_roundtrip` | function | `tests/test_loop_llm_resilience.py:213` | `def test_llm_context_budget_roundtrip(tmp_path, monkeypatch)` |
| `test_planner_uses_bound_task_chain` | function | `tests/test_loop_llm_resilience.py:225` | `def test_planner_uses_bound_task_chain(tmp_path, monkeypatch)` |
| `test_raw_llm_recording_carries_task_and_model` | function | `tests/test_loop_llm_resilience.py:190` | `def test_raw_llm_recording_carries_task_and_model(tmp_path, monkeypatch)` |
| `test_raw_llm_recording_toggle` | function | `tests/test_loop_llm_resilience.py:169` | `def test_raw_llm_recording_toggle(tmp_path, monkeypatch)` |
| `test_stall_guard_forces_intent_when_nothing_open` | function | `tests/test_loop_llm_resilience.py:114` | `def test_stall_guard_forces_intent_when_nothing_open(tmp_path, monkeypatch)` |
| `test_task_llm_chain_quota_failover` | function | `tests/test_loop_llm_resilience.py:135` | `def test_task_llm_chain_quota_failover(tmp_path, monkeypatch)` |
| `test_wall_clock_settles_partial_not_hard_kill` | function | `tests/test_loop_llm_resilience.py:95` | `def test_wall_clock_settles_partial_not_hard_kill(tmp_path, monkeypatch)` |
| `test_worker_llm_steps_filtered_by_scope_and_tooling` | function | `tests/test_loop_llm_resilience.py:71` | `def test_worker_llm_steps_filtered_by_scope_and_tooling(tmp_path, monkeypatch)` |
| `TestClampInt` | class | `tests/test_loop_manager.py:123` | `class TestClampInt` |
| `TestLifecycle` | class | `tests/test_loop_manager.py:281` | `class TestLifecycle` |
| `TestLogReading` | class | `tests/test_loop_manager.py:222` | `class TestLogReading` |
| `TestSanitizeGoal` | class | `tests/test_loop_manager.py:95` | `class TestSanitizeGoal` |
| `TestSpawnAndRegistry` | class | `tests/test_loop_manager.py:151` | `class TestSpawnAndRegistry` |
| `TestStop` | class | `tests/test_loop_manager.py:251` | `class TestStop` |
| `TestValidateLoopId` | class | `tests/test_loop_manager.py:138` | `class TestValidateLoopId` |
| `TestValidateTarget` | class | `tests/test_loop_manager.py:64` | `class TestValidateTarget` |
| `loops_dir` | function | `tests/test_loop_manager.py:37` | `def loops_dir()` |
| `manager` | function | `tests/test_loop_manager.py:56` | `def manager(loops_dir, stub_script)` |
| `stub_script` | function | `tests/test_loop_manager.py:43` | `def stub_script(tmp_path)` |
| `test_accepts_hex32` | method | `tests/test_loop_manager.py:139` | `def test_accepts_hex32(self)` |
| `test_accepts_ipv4` | method | `tests/test_loop_manager.py:65` | `def test_accepts_ipv4(self)` |
| `test_accepts_ipv6` | method | `tests/test_loop_manager.py:68` | `def test_accepts_ipv6(self)` |
| `test_accepts_plain_words` | method | `tests/test_loop_manager.py:119` | `def test_accepts_plain_words(self)` |
| `test_argv_has_no_shell` | method | `tests/test_loop_manager.py:164` | `def test_argv_has_no_shell(self, manager)` |
| `test_clamps_high` | method | `tests/test_loop_manager.py:130` | `def test_clamps_high(self)` |
| `test_clamps_low` | method | `tests/test_loop_manager.py:127` | `def test_clamps_low(self)` |
| `test_collapses_whitespace` | method | `tests/test_loop_manager.py:100` | `def test_collapses_whitespace(self)` |
| `test_concurrency_cap` | method | `tests/test_loop_manager.py:187` | `def test_concurrency_cap(self, manager)` |
| `test_default_on_none` | method | `tests/test_loop_manager.py:124` | `def test_default_on_none(self)` |
| `test_defaults_on_empty` | method | `tests/test_loop_manager.py:96` | `def test_defaults_on_empty(self)` |
| `test_invalid_kind_rejected` | method | `tests/test_loop_manager.py:179` | `def test_invalid_kind_rejected(self, manager)` |
| `test_invalid_target_rejected` | method | `tests/test_loop_manager.py:183` | `def test_invalid_target_rejected(self, manager)` |
| `test_list_loops_sorted_newest_first` | method | `tests/test_loop_manager.py:195` | `def test_list_loops_sorted_newest_first(self, manager)` |
| `test_metadata_written` | method | `tests/test_loop_manager.py:212` | `def test_metadata_written(self, manager, loops_dir)` |
| `test_quick_exit_marks_finished` | method | `tests/test_loop_manager.py:282` | `def test_quick_exit_marks_finished(self, loops_dir, tmp_path)` |
| `test_read_log_chunk` | method | `tests/test_loop_manager.py:223` | `def test_read_log_chunk(self, manager, loops_dir)` |
| `test_read_log_confinement` | method | `tests/test_loop_manager.py:235` | `def test_read_log_confinement(self, manager, loops_dir)` |
| `test_read_log_offset_beyond_size` | method | `tests/test_loop_manager.py:243` | `def test_read_log_offset_beyond_size(self, manager)` |
| `test_read_log_unknown_loop` | method | `tests/test_loop_manager.py:231` | `def test_read_log_unknown_loop(self, manager)` |
| `test_registry_survives_restart` | method | `tests/test_loop_manager.py:205` | `def test_registry_survives_restart(self, manager, loops_dir)` |
| `test_rejects_command_injection` | method | `tests/test_loop_manager.py:78` | `def test_rejects_command_injection(self)` |
| `test_rejects_empty` | method | `tests/test_loop_manager.py:90` | `def test_rejects_empty(self)` |
| `test_rejects_hostname` | method | `tests/test_loop_manager.py:74` | `def test_rejects_hostname(self)` |
| `test_rejects_metacharacters` | method | `tests/test_loop_manager.py:82` | `def test_rejects_metacharacters(self)` |
| `test_rejects_newlines` | method | `tests/test_loop_manager.py:103` | `def test_rejects_newlines(self)` |
| `test_rejects_non_hex` | method | `tests/test_loop_manager.py:146` | `def test_rejects_non_hex(self)` |
| `test_rejects_non_numeric` | method | `tests/test_loop_manager.py:133` | `def test_rejects_non_numeric(self)` |
| `test_rejects_non_string` | method | `tests/test_loop_manager.py:86` | `def test_rejects_non_string(self)` |
| `test_rejects_quotes` | method | `tests/test_loop_manager.py:107` | `def test_rejects_quotes(self)` |
| `test_rejects_semicolons` | method | `tests/test_loop_manager.py:111` | `def test_rejects_semicolons(self)` |
| `test_rejects_too_long` | method | `tests/test_loop_manager.py:115` | `def test_rejects_too_long(self)` |
| `test_rejects_traversal` | method | `tests/test_loop_manager.py:142` | `def test_rejects_traversal(self)` |
| `test_sigterm_resistant_process_is_killed` | method | `tests/test_loop_manager.py:297` | `def test_sigterm_resistant_process_is_killed(self, loops_dir, tmp_path)` |
| `test_start_spawns_and_records` | method | `tests/test_loop_manager.py:152` | `def test_start_spawns_and_records(self, manager, loops_dir)` |
| `test_stop_finished_loop_rejected` | method | `tests/test_loop_manager.py:268` | `def test_stop_finished_loop_rejected(self, manager)` |
| `test_stop_terminates_process` | method | `tests/test_loop_manager.py:252` | `def test_stop_terminates_process(self, manager)` |
| `test_stop_unknown_loop` | method | `tests/test_loop_manager.py:264` | `def test_stop_unknown_loop(self, manager)` |
| `test_strips_whitespace` | method | `tests/test_loop_manager.py:71` | `def test_strips_whitespace(self)` |
| `test_summary_shape` | method | `tests/test_loop_manager.py:314` | `def test_summary_shape(self, manager)` |
| `test_mentions_parse_caps_and_trusts_ids` | function | `tests/test_loop_mentions.py:16` | `def test_mentions_parse_caps_and_trusts_ids()` |
| `test_mentions_search_and_cursor` | function | `tests/test_loop_mentions.py:6` | `def test_mentions_search_and_cursor(tmp_path, monkeypatch)` |
| `test_load_targets_file_caps_batch` | function | `tests/test_loop_multi_target.py:38` | `def test_load_targets_file_caps_batch(tmp_path)` |
| `test_load_targets_file_empty_raises` | function | `tests/test_loop_multi_target.py:52` | `def test_load_targets_file_empty_raises(tmp_path)` |
| `test_load_targets_file_missing_raises` | function | `tests/test_loop_multi_target.py:46` | `def test_load_targets_file_missing_raises(tmp_path)` |
| `test_load_targets_file_skips_comments_and_invalid` | function | `tests/test_loop_multi_target.py:27` | `def test_load_targets_file_skips_comments_and_invalid(tmp_path)` |
| `test_parse_loop_line_accepts_targets_file` | function | `tests/test_loop_multi_target.py:10` | `def test_parse_loop_line_accepts_targets_file(tmp_path)` |
| `test_parse_loop_line_defaults_without_file` | function | `tests/test_loop_multi_target.py:20` | `def test_parse_loop_line_defaults_without_file()` |
| `_sandbox` | function | `tests/test_loop_nmap_guard.py:8` | `def _sandbox(tmp_path, monkeypatch)` |
| `test_repair_appends_missing_target` | function | `tests/test_loop_nmap_guard.py:35` | `def test_repair_appends_missing_target()` |
| `test_repair_drops_port_flag_without_value` | function | `tests/test_loop_nmap_guard.py:41` | `def test_repair_drops_port_flag_without_value()` |
| `test_repair_keeps_valid_port_specs` | function | `tests/test_loop_nmap_guard.py:27` | `def test_repair_keeps_valid_port_specs()` |
| `test_repair_rejects_target_in_port_slot` | function | `tests/test_loop_nmap_guard.py:13` | `def test_repair_rejects_target_in_port_slot()` |
| `test_repair_strips_binary_path_for_shell_verb` | function | `tests/test_loop_nmap_guard.py:20` | `def test_repair_strips_binary_path_for_shell_verb()` |
| `test_scan_commands_are_not_replayed` | function | `tests/test_loop_nmap_guard.py:58` | `def test_scan_commands_are_not_replayed(tmp_path, monkeypatch)` |
| `test_stall_thresholds_follow_command_timeout` | function | `tests/test_loop_nmap_guard.py:48` | `def test_stall_thresholds_follow_command_timeout()` |
| `_patched_engine` | function | `tests/test_loop_objective_wiring.py:14` | `def _patched_engine(tmp_path, monkeypatch)` |
| `_point_objectives` | function | `tests/test_loop_objective_wiring.py:25` | `def _point_objectives(tmp_path, monkeypatch)` |
| `_statuses` | function | `tests/test_loop_objective_wiring.py:51` | `def _statuses(path)` |
| `_write_objective` | function | `tests/test_loop_objective_wiring.py:37` | `def _write_objective(path, objective_id, text, status, priority, target)` |
| `test_daemon_drain_drafts_helper_is_safe_without_engine` | function | `tests/test_loop_objective_wiring.py:172` | `def test_daemon_drain_drafts_helper_is_safe_without_engine()` |
| `test_daemon_drain_drafts_imports_pending_draft` | function | `tests/test_loop_objective_wiring.py:179` | `def test_daemon_drain_drafts_imports_pending_draft(tmp_path, monkeypatch)` |
| `test_drain_drafts_imports_pending_draft_as_task` | function | `tests/test_loop_objective_wiring.py:128` | `def test_drain_drafts_imports_pending_draft_as_task(tmp_path, monkeypatch)` |
| `test_drain_drafts_is_idempotent` | function | `tests/test_loop_objective_wiring.py:153` | `def test_drain_drafts_is_idempotent(tmp_path, monkeypatch)` |
| `test_pending_objectives_filters_by_target_and_priority` | function | `tests/test_loop_objective_wiring.py:61` | `def test_pending_objectives_filters_by_target_and_priority(tmp_path, monkeypatch)` |
| `test_planner_emits_and_claims_injected_objective` | function | `tests/test_loop_objective_wiring.py:77` | `def test_planner_emits_and_claims_injected_objective(tmp_path, monkeypatch)` |
| `test_settle_marks_done_when_intent_done` | function | `tests/test_loop_objective_wiring.py:95` | `def test_settle_marks_done_when_intent_done(tmp_path, monkeypatch)` |
| `test_settle_requeues_when_intent_unfinished` | function | `tests/test_loop_objective_wiring.py:112` | `def test_settle_requeues_when_intent_unfinished(tmp_path, monkeypatch)` |
| `_overview` | function | `tests/test_loop_progress.py:20` | `def _overview()` |
| `test_chain_has_fourteen_stages` | function | `tests/test_loop_progress.py:28` | `def test_chain_has_fourteen_stages()` |
| `test_finished_task_all_green` | function | `tests/test_loop_progress.py:58` | `def test_finished_task_all_green()` |
| `test_fresh_task_shows_first_stage_current` | function | `tests/test_loop_progress.py:34` | `def test_fresh_task_shows_first_stage_current()` |
| `test_line_mode_prints_only_on_stage_change` | function | `tests/test_loop_progress.py:104` | `def test_line_mode_prints_only_on_stage_change(capsys)` |
| `test_panel_renders_without_live` | function | `tests/test_loop_progress.py:79` | `def test_panel_renders_without_live()` |
| `test_progress_advances_with_evidence` | function | `tests/test_loop_progress.py:44` | `def test_progress_advances_with_evidence()` |
| `test_render_contains_no_markup_strings` | function | `tests/test_loop_progress.py:88` | `def test_render_contains_no_markup_strings()` |
| `test_sanitize_line_keeps_ansi_when_asked` | function | `tests/test_loop_progress.py:134` | `def test_sanitize_line_keeps_ansi_when_asked()` |
| `test_sanitize_line_strips_ansi_and_cr` | function | `tests/test_loop_progress.py:126` | `def test_sanitize_line_strips_ansi_and_cr()` |
| `test_snapshot_counts_intent_states` | function | `tests/test_loop_progress.py:69` | `def test_snapshot_counts_intent_states()` |
| `_patched_engine` | function | `tests/test_loop_scope_traffic_evidence.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_finding_evidence_roles_notes_order` | function | `tests/test_loop_scope_traffic_evidence.py:88` | `def test_finding_evidence_roles_notes_order(tmp_path, monkeypatch)` |
| `test_scope_cidr_covers_url_embedded_ip` | function | `tests/test_loop_scope_traffic_evidence.py:29` | `def test_scope_cidr_covers_url_embedded_ip(tmp_path, monkeypatch)` |
| `test_scope_covers_by_ownership_not_substring` | function | `tests/test_loop_scope_traffic_evidence.py:15` | `def test_scope_covers_by_ownership_not_substring(tmp_path, monkeypatch)` |
| `test_scope_ip_covers_any_port_url` | function | `tests/test_loop_scope_traffic_evidence.py:41` | `def test_scope_ip_covers_any_port_url(tmp_path, monkeypatch)` |
| `test_traffic_search_host_port_aware` | function | `tests/test_loop_scope_traffic_evidence.py:71` | `def test_traffic_search_host_port_aware(tmp_path, monkeypatch)` |
| `test_worker_scope_enforcement_cidr` | function | `tests/test_loop_scope_traffic_evidence.py:54` | `def test_worker_scope_enforcement_cidr(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_spawn_side.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_chat_sessions_stay_independent` | function | `tests/test_loop_spawn_side.py:15` | `def test_chat_sessions_stay_independent(tmp_path, monkeypatch)` |
| `test_side_questions_persist_and_recall` | function | `tests/test_loop_spawn_side.py:36` | `def test_side_questions_persist_and_recall(tmp_path, monkeypatch)` |
| `test_spawn_inherits_scope_and_findings_read_only` | function | `tests/test_loop_spawn_side.py:53` | `def test_spawn_inherits_scope_and_findings_read_only(tmp_path, monkeypatch)` |
| `test_save_json_survives_parallel_writers` | function | `tests/test_loop_store_race.py:8` | `def test_save_json_survives_parallel_writers(tmp_path, monkeypatch)` |
| `writer` | function | `tests/test_loop_store_race.py:16` | `def writer(worker)` |
| `_DeadPool` | class | `tests/test_loop_supervision.py:25` | `class _DeadPool` |
| `_isolate_intel` | function | `tests/test_loop_supervision.py:16` | `def _isolate_intel(tmp_path, monkeypatch)` |
| `_kill_llm` | function | `tests/test_loop_supervision.py:37` | `def _kill_llm(monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_supervision.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `complete` | method | `tests/test_loop_supervision.py:32` | `def complete(self)` |
| `members` | method | `tests/test_loop_supervision.py:28` | `def members(self)` |
| `test_prompt_context_masks_configured_only` | function | `tests/test_loop_supervision.py:99` | `def test_prompt_context_masks_configured_only(tmp_path, monkeypatch)` |
| `test_repetition_watchdog_settles` | function | `tests/test_loop_supervision.py:46` | `def test_repetition_watchdog_settles(tmp_path, monkeypatch)` |
| `test_stack_priors_prefer_same_stack` | function | `tests/test_loop_supervision.py:75` | `def test_stack_priors_prefer_same_stack(tmp_path, monkeypatch)` |
| `_Assets` | class | `tests/test_loop_trigger_hints.py:42` | `class _Assets` |
| `_Graph` | class | `tests/test_loop_trigger_hints.py:29` | `class _Graph` |
| `__init__` | method | `tests/test_loop_trigger_hints.py:32` | `def __init__(self)` |
| `__init__` | method | `tests/test_loop_trigger_hints.py:45` | `def __init__(self, value)` |
| `add_node` | method | `tests/test_loop_trigger_hints.py:35` | `def add_node(self, kind, text, state, priority, meta)` |
| `fake_hot_matches` | function | `tests/test_loop_trigger_hints.py:65` | `def fake_hot_matches(services, allow_network)` |
| `fake_hot_matches` | function | `tests/test_loop_trigger_hints.py:100` | `def fake_hot_matches(services, allow_network)` |
| `list` | method | `tests/test_loop_trigger_hints.py:38` | `def list(self)` |
| `list` | method | `tests/test_loop_trigger_hints.py:49` | `def list(self, kind)` |
| `test_changed_banner_refires_the_hint` | function | `tests/test_loop_trigger_hints.py:90` | `def test_changed_banner_refires_the_hint(tmp_path, monkeypatch)` |
| `test_cve_hot_hint_proposed_once_per_signature` | function | `tests/test_loop_trigger_hints.py:78` | `def test_cve_hot_hint_proposed_once_per_signature(trigger_env)` |
| `test_hint_fingerprint_normalizes_product_and_version` | function | `tests/test_loop_trigger_hints.py:118` | `def test_hint_fingerprint_normalizes_product_and_version()` |
| `test_hint_store_written_under_loop_stores` | function | `tests/test_loop_trigger_hints.py:158` | `def test_hint_store_written_under_loop_stores(tmp_path, monkeypatch)` |
| `test_hint_ttl_expires_and_refires` | function | `tests/test_loop_trigger_hints.py:137` | `def test_hint_ttl_expires_and_refires(tmp_path, monkeypatch)` |
| `test_prune_drops_expired_fingerprints` | function | `tests/test_loop_trigger_hints.py:128` | `def test_prune_drops_expired_fingerprints()` |
| `trigger_env` | function | `tests/test_loop_trigger_hints.py:56` | `def trigger_env(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_worker_traces.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `_seed_two_works` | function | `tests/test_loop_worker_traces.py:15` | `def _seed_two_works(engine, task_id)` |
| `test_add_hint_emits_explicit_planner_trigger` | function | `tests/test_loop_worker_traces.py:65` | `def test_add_hint_emits_explicit_planner_trigger(tmp_path, monkeypatch)` |
| `test_planner_intent_unbound_emits_nothing` | function | `tests/test_loop_worker_traces.py:100` | `def test_planner_intent_unbound_emits_nothing(tmp_path, monkeypatch)` |
| `test_search_all_spans_works_without_intent` | function | `tests/test_loop_worker_traces.py:27` | `def test_search_all_spans_works_without_intent(tmp_path, monkeypatch)` |
| `test_trace_steps_and_single_step` | function | `tests/test_loop_worker_traces.py:40` | `def test_trace_steps_and_single_step(tmp_path, monkeypatch)` |
| `test_worker_bash_unbound_blocks_without_execution` | function | `tests/test_loop_worker_traces.py:81` | `def test_worker_bash_unbound_blocks_without_execution(tmp_path, monkeypatch)` |
| `test_worker_lane_binds_node_detail` | function | `tests/test_loop_worker_traces.py:57` | `def test_worker_lane_binds_node_detail(tmp_path, monkeypatch)` |
| `_drive` | function | `tests/test_marketplace_config.py:128` | `def _drive()` |
| `_drive` | function | `tests/test_marketplace_config.py:151` | `def _drive()` |
| `_registry` | function | `tests/test_marketplace_config.py:12` | `def _registry(tmp_path, monkeypatch)` |
| `test_create_and_delete_across_tabs` | function | `tests/test_marketplace_config.py:89` | `def test_create_and_delete_across_tabs(tmp_path, monkeypatch)` |
| `test_filter_input_keeps_printable_keys` | function | `tests/test_marketplace_config.py:145` | `def test_filter_input_keeps_printable_keys(tmp_path, monkeypatch)` |
| `test_marketplace_app_filters_rows` | function | `tests/test_marketplace_config.py:118` | `def test_marketplace_app_filters_rows(tmp_path, monkeypatch)` |
| `test_plugin_rows_skip_lua_and_templates` | function | `tests/test_marketplace_config.py:61` | `def test_plugin_rows_skip_lua_and_templates(tmp_path, monkeypatch)` |
| `test_read_only_tabs_never_toggle_or_delete` | function | `tests/test_marketplace_config.py:76` | `def test_read_only_tabs_never_toggle_or_delete(tmp_path, monkeypatch)` |
| `test_settings_toggle_tracks_only_success` | function | `tests/test_marketplace_config.py:105` | `def test_settings_toggle_tracks_only_success(tmp_path, monkeypatch)` |
| `test_tool_rows_use_json_and_active_key` | function | `tests/test_marketplace_config.py:33` | `def test_tool_rows_use_json_and_active_key(tmp_path, monkeypatch)` |
| `_Boom` | class | `tests/test_mcp_auto_loop_wrapper.py:31` | `class _Boom` |
| `_FakeEngine` | class | `tests/test_mcp_auto_loop_wrapper.py:44` | `class _FakeEngine` |
| `__init__` | method | `tests/test_mcp_auto_loop_wrapper.py:32` | `def __init__(self)` |
| `__init__` | method | `tests/test_mcp_auto_loop_wrapper.py:45` | `def __init__(self)` |
| `_patched` | function | `tests/test_mcp_auto_loop_wrapper.py:16` | `def _patched(monkeypatch, tmp_path)` |
| `_text` | function | `tests/test_mcp_auto_loop_wrapper.py:110` | `def _text(response)` |
| `create_task` | method | `tests/test_mcp_auto_loop_wrapper.py:50` | `def create_task(self, goal)` |
| `ensure_target` | method | `tests/test_mcp_auto_loop_wrapper.py:54` | `def ensure_target(self, task_id, target, reason)` |
| `loop_join` | function | `tests/test_mcp_auto_loop_wrapper.py:125` | `def loop_join(coro)` |
| `run` | method | `tests/test_mcp_auto_loop_wrapper.py:58` | `def run(self, task_id, max_rounds, workers, timeout_sec)` |
| `test_engine_failure_surfaces` | function | `tests/test_mcp_auto_loop_wrapper.py:100` | `def test_engine_failure_surfaces(monkeypatch, tmp_path)` |
| `test_fast_path_runs_the_engine` | function | `tests/test_mcp_auto_loop_wrapper.py:76` | `def test_fast_path_runs_the_engine(monkeypatch, tmp_path)` |
| `test_legacy_flag_annotates_but_routes_fast` | function | `tests/test_mcp_auto_loop_wrapper.py:90` | `def test_legacy_flag_annotates_but_routes_fast(monkeypatch, tmp_path)` |
| `TestRegistryDispatch` | class | `tests/test_mcp_dispatch.py:51` | `class TestRegistryDispatch` |
| `_fallback_branches` | function | `tests/test_mcp_dispatch.py:40` | `def _fallback_branches()` |
| `_registered` | function | `tests/test_mcp_dispatch.py:23` | `def _registered()` |
| `test_mcp_never_offers_interactive_repl` | function | `tests/test_mcp_dispatch.py:107` | `def test_mcp_never_offers_interactive_repl()` |
| `test_migrated_handlers_absent_from_fallback` | method | `tests/test_mcp_dispatch.py:61` | `def test_migrated_handlers_absent_from_fallback(self)` |
| `test_migrated_handlers_registered` | method | `tests/test_mcp_dispatch.py:56` | `def test_migrated_handlers_registered(self)` |
| `test_new_chain_shell_tools_have_defs_and_handlers` | function | `tests/test_mcp_dispatch.py:82` | `def test_new_chain_shell_tools_have_defs_and_handlers()` |
| `test_no_dead_duplicate_branches` | method | `tests/test_mcp_dispatch.py:52` | `def test_no_dead_duplicate_branches(self)` |
| `test_opencode_bridge_curates_loop_and_chain` | function | `tests/test_mcp_dispatch.py:92` | `def test_opencode_bridge_curates_loop_and_chain()` |
| `test_set_config_refuses_null_values` | function | `tests/test_mcp_dispatch.py:67` | `def test_set_config_refuses_null_values()` |
| `_fresh_mcp_module` | function | `tests/test_mcp_improvements.py:397` | `def _fresh_mcp_module(tmp_path)` |
| `_seed_sessions` | function | `tests/test_mcp_improvements.py:182` | `def _seed_sessions(tmp_path)` |
| `runner` | function | `tests/test_mcp_improvements.py:300` | `def runner(cmd, timeout)` |
| `runner` | function | `tests/test_mcp_improvements.py:320` | `def runner(cmd, timeout)` |
| `test_audit_tasks_drops_timestamps_and_urls` | function | `tests/test_mcp_improvements.py:117` | `def test_audit_tasks_drops_timestamps_and_urls()` |
| `test_audit_tasks_respects_min_confidence` | function | `tests/test_mcp_improvements.py:141` | `def test_audit_tasks_respects_min_confidence()` |
| `test_build_target_context_filters_by_port` | function | `tests/test_mcp_improvements.py:195` | `def test_build_target_context_filters_by_port(tmp_path)` |
| `test_build_target_context_no_port_returns_all` | function | `tests/test_mcp_improvements.py:218` | `def test_build_target_context_no_port_returns_all(tmp_path)` |
| `test_confirmation_required_for_destructive_command` | function | `tests/test_mcp_improvements.py:380` | `def test_confirmation_required_for_destructive_command()` |
| `test_confirmation_required_for_destructive_tools` | function | `tests/test_mcp_improvements.py:389` | `def test_confirmation_required_for_destructive_tools()` |
| `test_confirmation_skipped_for_benign` | function | `tests/test_mcp_improvements.py:385` | `def test_confirmation_skipped_for_benign()` |
| `test_diff_first_run_reports_first_run` | function | `tests/test_mcp_improvements.py:353` | `def test_diff_first_run_reports_first_run(tmp_path)` |
| `test_diff_picks_up_changes` | function | `tests/test_mcp_improvements.py:360` | `def test_diff_picks_up_changes(tmp_path)` |
| `test_evidence_freshness_fresh` | function | `tests/test_mcp_improvements.py:160` | `def test_evidence_freshness_fresh(tmp_path)` |
| `test_evidence_freshness_missing` | function | `tests/test_mcp_improvements.py:154` | `def test_evidence_freshness_missing(tmp_path)` |
| `test_evidence_freshness_stale` | function | `tests/test_mcp_improvements.py:170` | `def test_evidence_freshness_stale(tmp_path)` |
| `test_evidence_grep_finds_in_loot_scope` | function | `tests/test_mcp_improvements.py:227` | `def test_evidence_grep_finds_in_loot_scope(tmp_path)` |
| `test_evidence_grep_handler_ignores_binaries` | function | `tests/test_mcp_improvements.py:436` | `def test_evidence_grep_handler_ignores_binaries(tmp_path)` |
| `test_evidence_grep_invalid_regex` | function | `tests/test_mcp_improvements.py:237` | `def test_evidence_grep_invalid_regex(tmp_path)` |
| `test_evidence_grep_truncates` | function | `tests/test_mcp_improvements.py:244` | `def test_evidence_grep_truncates(tmp_path)` |
| `test_handler_target_context_via_helper` | function | `tests/test_mcp_improvements.py:414` | `def test_handler_target_context_via_helper(tmp_path)` |
| `test_handler_tasks_cleanup_dry_run` | function | `tests/test_mcp_improvements.py:421` | `def test_handler_tasks_cleanup_dry_run(tmp_path)` |
| `test_is_likely_credential_classifies` | function | `tests/test_mcp_improvements.py:74` | `def test_is_likely_credential_classifies(value, expect_real, expect_reason)` |
| `test_is_likely_credential_handles_non_string` | function | `tests/test_mcp_improvements.py:84` | `def test_is_likely_credential_handles_non_string()` |
| `test_jobstore_captures_failure` | function | `tests/test_mcp_improvements.py:317` | `def test_jobstore_captures_failure()` |
| `test_jobstore_list_orders_newest_first` | function | `tests/test_mcp_improvements.py:340` | `def test_jobstore_list_orders_newest_first()` |
| `test_jobstore_runs_command_and_reports_done` | function | `tests/test_mcp_improvements.py:297` | `def test_jobstore_runs_command_and_reports_done()` |
| `test_jobstore_unknown_id` | function | `tests/test_mcp_improvements.py:335` | `def test_jobstore_unknown_id()` |
| `test_parse_task_value_complete` | function | `tests/test_mcp_improvements.py:92` | `def test_parse_task_value_complete()` |
| `test_parse_task_value_no_payload` | function | `tests/test_mcp_improvements.py:110` | `def test_parse_task_value_no_payload()` |
| `test_parse_task_value_truncated` | function | `tests/test_mcp_improvements.py:103` | `def test_parse_task_value_truncated()` |
| `test_preflight_detects_duplicate` | function | `tests/test_mcp_improvements.py:256` | `def test_preflight_detects_duplicate(tmp_path)` |
| `test_preflight_flags_missing_payload_keys` | function | `tests/test_mcp_improvements.py:270` | `def test_preflight_flags_missing_payload_keys(tmp_path)` |
| `test_preflight_os_mismatch` | function | `tests/test_mcp_improvements.py:281` | `def test_preflight_os_mismatch(tmp_path)` |
| `TestEnsureOptional` | class | `tests/test_mcp_lazy.py:42` | `class TestEnsureOptional` |
| `TestWrappersDelegate` | class | `tests/test_mcp_lazy.py:86` | `class TestWrappersDelegate` |
| `loader` | function | `tests/test_mcp_lazy.py:47` | `def loader(ns)` |
| `loader` | function | `tests/test_mcp_lazy.py:61` | `def loader(ns)` |
| `loader` | function | `tests/test_mcp_lazy.py:69` | `def loader(ns)` |
| `loader` | function | `tests/test_mcp_lazy.py:78` | `def loader(ns)` |
| `test_all_wrappers_delegate_to_helper` | method | `tests/test_mcp_lazy.py:87` | `def test_all_wrappers_delegate_to_helper(self)` |
| `test_cached_value_returned_untouched` | method | `tests/test_mcp_lazy.py:58` | `def test_cached_value_returned_untouched(self)` |
| `test_exception_fails_closed` | method | `tests/test_mcp_lazy.py:66` | `def test_exception_fails_closed(self)` |
| `test_false_loader_with_fallback` | method | `tests/test_mcp_lazy.py:75` | `def test_false_loader_with_fallback(self)` |
| `test_success_binds_and_caches` | method | `tests/test_mcp_lazy.py:43` | `def test_success_binds_and_caches(self)` |
| `_load_mcp_module` | function | `tests/test_mcp_recommender_embed.py:15` | `def _load_mcp_module()` |
| `explode` | function | `tests/test_mcp_recommender_embed.py:62` | `def explode()` |
| `fake_recommend` | function | `tests/test_mcp_recommender_embed.py:48` | `def fake_recommend()` |
| `test_limits_suggestions` | function | `tests/test_mcp_recommender_embed.py:81` | `def test_limits_suggestions(monkeypatch)` |
| `test_maps_recommender_fields` | function | `tests/test_mcp_recommender_embed.py:25` | `def test_maps_recommender_fields(monkeypatch)` |
| `test_never_forwards_positional_arguments` | function | `tests/test_mcp_recommender_embed.py:44` | `def test_never_forwards_positional_arguments(monkeypatch)` |
| `test_reports_unavailable_recommender` | function | `tests/test_mcp_recommender_embed.py:71` | `def test_reports_unavailable_recommender(monkeypatch)` |
| `test_returns_error_entry_on_failure` | function | `tests/test_mcp_recommender_embed.py:59` | `def test_returns_error_entry_on_failure(monkeypatch)` |
| `Empty` | class | `tests/test_mediation.py:217` | `class Empty` |
| `Fake` | class | `tests/test_mediation.py:182` | `class Fake` |
| `FakePort` | class | `tests/test_mediation.py:239` | `class FakePort` |
| `FakePort` | class | `tests/test_mediation.py:280` | `class FakePort` |
| `TestChainMediatorLlmPort` | class | `tests/test_mediation.py:170` | `class TestChainMediatorLlmPort` |
| `TestFeedbackMediator` | class | `tests/test_mediation.py:62` | `class TestFeedbackMediator` |
| `TestHubRouting` | class | `tests/test_mediation.py:19` | `class TestHubRouting` |
| `TestIntelMediatorActivityPort` | class | `tests/test_mediation.py:39` | `class TestIntelMediatorActivityPort` |
| `TestTelemetryMediator` | class | `tests/test_mediation.py:82` | `class TestTelemetryMediator` |
| `_FakeHub` | class | `tests/test_mediation.py:197` | `class _FakeHub` |
| `_NoLock` | class | `tests/test_mediation.py:204` | `class _NoLock` |
| `__enter__` | method | `tests/test_mediation.py:205` | `def __enter__(self)` |
| `__exit__` | method | `tests/test_mediation.py:208` | `def __exit__(self)` |
| `__init__` | method | `tests/test_mediation.py:198` | `def __init__(self, port)` |
| `_patch_hub` | method | `tests/test_mediation.py:194` | `def _patch_hub(self, monkeypatch, port)` |
| `boom` | function | `tests/test_mediation.py:68` | `def boom(steps, stack)` |
| `boom` | function | `tests/test_mediation.py:108` | `def boom()` |
| `boom` | function | `tests/test_mediation.py:124` | `def boom()` |
| `boom` | function | `tests/test_mediation.py:147` | `def boom()` |
| `boom` | function | `tests/test_mediation.py:163` | `def boom()` |
| `complete` | method | `tests/test_mediation.py:183` | `def complete(self, prompt, max_tokens, task_id)` |
| `complete` | method | `tests/test_mediation.py:218` | `def complete(self, prompt, max_tokens, task_id)` |
| `complete` | method | `tests/test_mediation.py:240` | `def complete(self, prompt, max_tokens, task_id)` |
| `complete` | method | `tests/test_mediation.py:281` | `def complete(self, prompt, max_tokens, task_id)` |
| `has_members` | method | `tests/test_mediation.py:186` | `def has_members(self)` |
| `has_members` | method | `tests/test_mediation.py:221` | `def has_members(self)` |
| `has_members` | method | `tests/test_mediation.py:243` | `def has_members(self)` |
| `has_members` | method | `tests/test_mediation.py:285` | `def has_members(self)` |
| `mediator_for` | method | `tests/test_mediation.py:201` | `def mediator_for(self, domain)` |
| `test_activity_records_fallback_graceful` | method | `tests/test_mediation.py:48` | `def test_activity_records_fallback_graceful(self)` |
| `test_activity_records_via_injected_port` | method | `tests/test_mediation.py:42` | `def test_activity_records_via_injected_port(self)` |
| `test_all_default_domains_registered` | method | `tests/test_mediation.py:22` | `def test_all_default_domains_registered(self)` |
| `test_assess_opsec_forwards_to_bridge` | method | `tests/test_mediation.py:114` | `def test_assess_opsec_forwards_to_bridge(self, monkeypatch)` |
| `test_assess_opsec_graceful_on_bridge_failure` | method | `tests/test_mediation.py:121` | `def test_assess_opsec_graceful_on_bridge_failure(self, monkeypatch)` |
| `test_mask_and_stack_survive_missing_peers` | method | `tests/test_mediation.py:52` | `def test_mask_and_stack_survive_missing_peers(self, monkeypatch)` |
| `test_mediation_contract_shape` | method | `tests/test_mediation.py:33` | `def test_mediation_contract_shape(self)` |
| `test_order_steps_forwarded` | method | `tests/test_mediation.py:75` | `def test_order_steps_forwarded(self, monkeypatch)` |
| `test_order_steps_passthrough_on_error` | method | `tests/test_mediation.py:65` | `def test_order_steps_passthrough_on_error(self, monkeypatch)` |
| `test_port_contract` | method | `tests/test_mediation.py:173` | `def test_port_contract(self)` |
| `test_publish_event_default_severity_positional` | method | `tests/test_mediation.py:85` | `def test_publish_event_default_severity_positional(self, monkeypatch)` |
| `test_publish_event_forwarding_calls_default_path` | method | `tests/test_mediation.py:95` | `def test_publish_event_forwarding_calls_default_path(self, monkeypatch)` |
| `test_record_outcome_quality_forwards_to_bridge` | method | `tests/test_mediation.py:130` | `def test_record_outcome_quality_forwards_to_bridge(self, monkeypatch)` |
| `test_record_outcome_quality_graceful_on_bridge_failure` | method | `tests/test_mediation.py:144` | `def test_record_outcome_quality_graceful_on_bridge_failure(self, monkeypatch)` |
| `test_recovery_pool_absent_returns_empty` | method | `tests/test_mediation.py:214` | `def test_recovery_pool_absent_returns_empty(self, monkeypatch)` |
| `test_recovery_pool_builds_steps` | method | `tests/test_mediation.py:236` | `def test_recovery_pool_builds_steps(self, monkeypatch)` |
| `test_recovery_prompt_carries_recent_changes` | method | `tests/test_mediation.py:262` | `def test_recovery_prompt_carries_recent_changes(self, monkeypatch, tmp_path)` |
| `test_register_llm_port_replaces` | method | `tests/test_mediation.py:181` | `def test_register_llm_port_replaces(self)` |
| `test_rl_select_graceful_off` | method | `tests/test_mediation.py:105` | `def test_rl_select_graceful_off(self, monkeypatch)` |
| `test_singleton_hub_shared` | method | `tests/test_mediation.py:30` | `def test_singleton_hub_shared(self)` |
| `test_tool_class_yields_forwards_to_bridge` | method | `tests/test_mediation.py:153` | `def test_tool_class_yields_forwards_to_bridge(self, monkeypatch)` |
| `test_tool_class_yields_graceful_on_bridge_failure` | method | `tests/test_mediation.py:160` | `def test_tool_class_yields_graceful_on_bridge_failure(self, monkeypatch)` |
| `test_unknown_domain_returns_none` | method | `tests/test_mediation.py:27` | `def test_unknown_domain_returns_none(self)` |
| `TestHashingEmbedder` | class | `tests/test_memory_semantics.py:27` | `class TestHashingEmbedder` |
| `TestMemoryStoreHybrid` | class | `tests/test_memory_semantics.py:90` | `class TestMemoryStoreHybrid` |
| `TestVectorSQLiteBackend` | class | `tests/test_memory_semantics.py:62` | `class TestVectorSQLiteBackend` |
| `_entry` | function | `tests/test_memory_semantics.py:14` | `def _entry(tool, command, snippet)` |
| `test_determinism_across_runs` | method | `tests/test_memory_semantics.py:44` | `def test_determinism_across_runs(self)` |
| `test_empty_text_raises` | method | `tests/test_memory_semantics.py:49` | `def test_empty_text_raises(self)` |
| `test_fts_wins_when_present` | method | `tests/test_memory_semantics.py:93` | `def test_fts_wins_when_present(self, tmp_path)` |
| `test_hybrid_fallback_after_miss` | method | `tests/test_memory_semantics.py:101` | `def test_hybrid_fallback_after_miss(self, tmp_path)` |
| `test_identical_text_full_similarity` | method | `tests/test_memory_semantics.py:30` | `def test_identical_text_full_similarity(self)` |
| `test_keyword_query_still_works` | method | `tests/test_memory_semantics.py:82` | `def test_keyword_query_still_works(self, tmp_path)` |
| `test_save_gets_embedding` | method | `tests/test_memory_semantics.py:65` | `def test_save_gets_embedding(self, tmp_path)` |
| `test_semantic_ranks_relevant_first` | method | `tests/test_memory_semantics.py:73` | `def test_semantic_ranks_relevant_first(self, tmp_path)` |
| `test_similar_text_scores_higher_than_unrelated` | method | `tests/test_memory_semantics.py:36` | `def test_similar_text_scores_higher_than_unrelated(self)` |
| `test_unit_length` | method | `tests/test_memory_semantics.py:55` | `def test_unit_length(self)` |
| `test_every_chain_resolves_without_unresolved_tokens` | function | `tests/test_metasploitable_gym.py:74` | `def test_every_chain_resolves_without_unresolved_tokens()` |
| `test_every_exploit_and_chain_is_loadable` | function | `tests/test_metasploitable_gym.py:50` | `def test_every_exploit_and_chain_is_loadable()` |
| `test_gym_base_ends_with_interactive_shell` | function | `tests/test_metasploitable_gym.py:63` | `def test_gym_base_ends_with_interactive_shell()` |
| `test_index_covers_the_ms2_vectors` | function | `tests/test_metasploitable_gym.py:23` | `def test_index_covers_the_ms2_vectors()` |
| `test_invalid_matrix_is_reported` | function | `tests/test_metasploitable_gym.py:96` | `def test_invalid_matrix_is_reported(tmp_path)` |
| `test_unknown_vulnerability_returns_none` | function | `tests/test_metasploitable_gym.py:89` | `def test_unknown_vulnerability_returns_none()` |
| `_fake_exec` | function | `tests/test_metasploitable_migrations.py:69` | `def _fake_exec(container, script, payload, timeout)` |
| `test_apply_migrations_applies_when_check_fails` | function | `tests/test_metasploitable_migrations.py:68` | `def test_apply_migrations_applies_when_check_fails(monkeypatch)` |
| `test_apply_migrations_skips_when_check_passes` | function | `tests/test_metasploitable_migrations.py:57` | `def test_apply_migrations_skips_when_check_passes(monkeypatch)` |
| `test_build_migrations_ordered_and_unique` | function | `tests/test_metasploitable_migrations.py:8` | `def test_build_migrations_ordered_and_unique()` |
| `test_database_mirror_uses_dump_and_restore` | function | `tests/test_metasploitable_migrations.py:90` | `def test_database_mirror_uses_dump_and_restore()` |
| `test_dns_fallback_payload_targets_port_53` | function | `tests/test_metasploitable_migrations.py:17` | `def test_dns_fallback_payload_targets_port_53()` |
| `test_dvwa_dom_page_payload_contains_sink` | function | `tests/test_metasploitable_migrations.py:82` | `def test_dvwa_dom_page_payload_contains_sink()` |
| `test_hosts_allow_uses_subnet_prefix` | function | `tests/test_metasploitable_migrations.py:47` | `def test_hosts_allow_uses_subnet_prefix()` |
| `test_nfs_fallback_starts_mountd_without_kernel_nfsd` | function | `tests/test_metasploitable_migrations.py:28` | `def test_nfs_fallback_starts_mountd_without_kernel_nfsd()` |
| `test_rlogin_trust_sets_rhosts_and_local_allow` | function | `tests/test_metasploitable_migrations.py:37` | `def test_rlogin_trust_sets_rhosts_and_local_allow()` |
| `_build_recorder` | function | `tests/test_metrics.py:35` | `def _build_recorder(tmp_path)` |
| `test_aggregator_handles_empty_iterable` | function | `tests/test_metrics.py:211` | `def test_aggregator_handles_empty_iterable()` |
| `test_aggregator_skips_malformed_records` | function | `tests/test_metrics.py:220` | `def test_aggregator_skips_malformed_records()` |
| `test_concurrent_writes_do_not_corrupt` | function | `tests/test_metrics.py:173` | `def test_concurrent_writes_do_not_corrupt(tmp_path)` |
| `test_get_recorder_is_singleton` | function | `tests/test_metrics.py:202` | `def test_get_recorder_is_singleton(tmp_path)` |
| `test_legacy_registry_inc_and_render` | function | `tests/test_metrics.py:42` | `def test_legacy_registry_inc_and_render()` |
| `test_metric_record_to_dict_roundtrip` | function | `tests/test_metrics.py:234` | `def test_metric_record_to_dict_roundtrip()` |
| `test_p95_uses_nearest_rank` | function | `tests/test_metrics.py:227` | `def test_p95_uses_nearest_rank()` |
| `test_recorder_appends_record_line` | function | `tests/test_metrics.py:57` | `def test_recorder_appends_record_line(tmp_path)` |
| `test_recorder_clamps_negative_duration` | function | `tests/test_metrics.py:83` | `def test_recorder_clamps_negative_duration(tmp_path)` |
| `test_summarize_aggregates_by_command` | function | `tests/test_metrics.py:92` | `def test_summarize_aggregates_by_command(tmp_path)` |
| `test_summarize_window_filters_old_records` | function | `tests/test_metrics.py:124` | `def test_summarize_window_filters_old_records(tmp_path)` |
| `test_tail_returns_newest_first` | function | `tests/test_metrics.py:163` | `def test_tail_returns_newest_first(tmp_path)` |
| `worker` | function | `tests/test_metrics.py:180` | `def worker(tag)` |
| `_BrokenSource` | class | `tests/test_metrics_aware_selector.py:217` | `class _BrokenSource` |
| `_StubMetrics` | class | `tests/test_metrics_aware_selector.py:54` | `class _StubMetrics` |
| `_StubSelector` | class | `tests/test_metrics_aware_selector.py:37` | `class _StubSelector(ICommandSelector)` |
| `__init__` | method | `tests/test_metrics_aware_selector.py:40` | `def __init__(self, decision)` |
| `__init__` | method | `tests/test_metrics_aware_selector.py:57` | `def __init__(self, by_command)` |
| `_decision` | function | `tests/test_metrics_aware_selector.py:71` | `def _decision(command)` |
| `fake_clock` | function | `tests/test_metrics_aware_selector.py:169` | `def fake_clock()` |
| `select` | method | `tests/test_metrics_aware_selector.py:44` | `def select(self, target, phase, context)` |
| `summarize` | method | `tests/test_metrics_aware_selector.py:62` | `def summarize(self, window_seconds)` |
| `summarize` | method | `tests/test_metrics_aware_selector.py:218` | `def summarize(self, window_seconds)` |
| `test_accepts_when_success_rate_at_threshold` | function | `tests/test_metrics_aware_selector.py:122` | `def test_accepts_when_success_rate_at_threshold()` |
| `test_chain_falls_through_to_fallback_when_all_filtered` | function | `tests/test_metrics_aware_selector.py:298` | `def test_chain_falls_through_to_fallback_when_all_filtered()` |
| `test_decorator_degrades_when_metrics_source_unavailable` | function | `tests/test_metrics_aware_selector.py:214` | `def test_decorator_degrades_when_metrics_source_unavailable()` |
| `test_filtering_emits_skip_event` | function | `tests/test_metrics_aware_selector.py:265` | `def test_filtering_emits_skip_event(tmp_path, monkeypatch)` |
| `test_filters_when_success_rate_below_threshold` | function | `tests/test_metrics_aware_selector.py:105` | `def test_filters_when_success_rate_below_threshold()` |
| `test_only_filters_named_command_not_whole_decision_object` | function | `tests/test_metrics_aware_selector.py:141` | `def test_only_filters_named_command_not_whole_decision_object()` |
| `test_passthrough_when_insufficient_attempts` | function | `tests/test_metrics_aware_selector.py:87` | `def test_passthrough_when_insufficient_attempts()` |
| `test_passthrough_when_wrapped_returns_none` | function | `tests/test_metrics_aware_selector.py:75` | `def test_passthrough_when_wrapped_returns_none()` |
| `test_summary_forwards_window_seconds` | function | `tests/test_metrics_aware_selector.py:188` | `def test_summary_forwards_window_seconds()` |
| `test_summary_is_cached_within_ttl` | function | `tests/test_metrics_aware_selector.py:158` | `def test_summary_is_cached_within_ttl()` |
| `test_wrap_chain_is_idempotent` | function | `tests/test_metrics_aware_selector.py:253` | `def test_wrap_chain_is_idempotent()` |
| `test_wrap_chain_leaves_fallback_unwrapped` | function | `tests/test_metrics_aware_selector.py:230` | `def test_wrap_chain_leaves_fallback_unwrapped()` |
| `test_wrap_chain_master_switch_off` | function | `tests/test_metrics_aware_selector.py:241` | `def test_wrap_chain_master_switch_off()` |
| `test_zero_window_is_treated_as_unbounded` | function | `tests/test_metrics_aware_selector.py:201` | `def test_zero_window_is_treated_as_unbounded()` |
| `_module_all` | function | `tests/test_migrate_lazyown_generator.py:27` | `def _module_all(source)` |
| `test_all_is_static_and_matches_class_name` | function | `tests/test_migrate_lazyown_generator.py:62` | `def test_all_is_static_and_matches_class_name()` |
| `test_compound_phase_title_casing` | function | `tests/test_migrate_lazyown_generator.py:68` | `def test_compound_phase_title_casing()` |
| `test_generated_module_parses` | function | `tests/test_migrate_lazyown_generator.py:57` | `def test_generated_module_parses()` |
| `test_method_bodies_are_embedded_in_order` | function | `tests/test_migrate_lazyown_generator.py:81` | `def test_method_bodies_are_embedded_in_order()` |
| `test_no_unevaluated_fstring_all_literal` | function | `tests/test_migrate_lazyown_generator.py:74` | `def test_no_unevaluated_fstring_all_literal()` |
| `TestClassify` | class | `tests/test_module_registry.py:20` | `class TestClassify` |
| `TestFormatFunctions` | class | `tests/test_module_registry.py:185` | `class TestFormatFunctions` |
| `TestModuleInfo` | class | `tests/test_module_registry.py:36` | `class TestModuleInfo` |
| `TestModuleRegistry` | class | `tests/test_module_registry.py:75` | `class TestModuleRegistry` |
| `test_by_type_shorthand` | method | `tests/test_module_registry.py:159` | `def test_by_type_shorthand(self)` |
| `test_empty_string` | method | `tests/test_module_registry.py:31` | `def test_empty_string(self)` |
| `test_format_module_detail` | method | `tests/test_module_registry.py:201` | `def test_format_module_detail(self)` |
| `test_format_module_detail_minimal` | method | `tests/test_module_registry.py:217` | `def test_format_module_detail_minimal(self)` |
| `test_format_module_table_empty` | method | `tests/test_module_registry.py:186` | `def test_format_module_table_empty(self)` |
| `test_format_module_table_with_data` | method | `tests/test_module_registry.py:190` | `def test_format_module_table_with_data(self)` |
| `test_full_construction` | method | `tests/test_module_registry.py:44` | `def test_full_construction(self)` |
| `test_get_known_module` | method | `tests/test_module_registry.py:133` | `def test_get_known_module(self)` |
| `test_get_unknown_returns_none` | method | `tests/test_module_registry.py:145` | `def test_get_unknown_returns_none(self)` |
| `test_initial_state_not_scanned` | method | `tests/test_module_registry.py:87` | `def test_initial_state_not_scanned(self)` |
| `test_known_categories` | method | `tests/test_module_registry.py:21` | `def test_known_categories(self)` |
| `test_minimal_construction` | method | `tests/test_module_registry.py:37` | `def test_minimal_construction(self)` |
| `test_repr` | method | `tests/test_module_registry.py:70` | `def test_repr(self)` |
| `test_rescan_forces_refresh` | method | `tests/test_module_registry.py:106` | `def test_rescan_forces_refresh(self)` |
| `test_scan_is_idempotent` | method | `tests/test_module_registry.py:99` | `def test_scan_is_idempotent(self)` |
| `test_scan_returns_list` | method | `tests/test_module_registry.py:92` | `def test_scan_returns_list(self)` |
| `test_search_by_category` | method | `tests/test_module_registry.py:127` | `def test_search_by_category(self)` |
| `test_search_by_module_type` | method | `tests/test_module_registry.py:121` | `def test_search_by_module_type(self)` |
| `test_search_enabled_only_filters_disabled` | method | `tests/test_module_registry.py:164` | `def test_search_enabled_only_filters_disabled(self)` |
| `test_search_returns_list` | method | `tests/test_module_registry.py:115` | `def test_search_returns_list(self)` |
| `test_singleton` | method | `tests/test_module_registry.py:76` | `def test_singleton(self)` |
| `test_singleton_with_base_dir` | method | `tests/test_module_registry.py:82` | `def test_singleton_with_base_dir(self)` |
| `test_summary_returns_counts` | method | `tests/test_module_registry.py:149` | `def test_summary_returns_counts(self)` |
| `test_to_dict` | method | `tests/test_module_registry.py:62` | `def test_to_dict(self)` |
| `test_unknown_category_defaults_to_auxiliary` | method | `tests/test_module_registry.py:27` | `def test_unknown_category_defaults_to_auxiliary(self)` |
| `_empty_osinfer` | function | `tests/test_module_registry_bridge.py:51` | `def _empty_osinfer(monkeypatch)` |
| `_registry` | function | `tests/test_module_registry_bridge.py:15` | `def _registry(tmp_path)` |
| `_registry_with_extras` | function | `tests/test_module_registry_bridge.py:43` | `def _registry_with_extras(tmp_path)` |
| `test_fillers_and_nonrunnable_sources_propose_nothing` | function | `tests/test_module_registry_bridge.py:85` | `def test_fillers_and_nonrunnable_sources_propose_nothing(tmp_path, monkeypatch)` |
| `test_incompatible_os_is_gated` | function | `tests/test_module_registry_bridge.py:74` | `def test_incompatible_os_is_gated(tmp_path, monkeypatch)` |
| `test_limit_caps_results` | function | `tests/test_module_registry_bridge.py:93` | `def test_limit_caps_results(tmp_path, monkeypatch)` |
| `test_name_mentions_propose_runnable_intents` | function | `tests/test_module_registry_bridge.py:58` | `def test_name_mentions_propose_runnable_intents(tmp_path, monkeypatch)` |
| `test_planner_appends_registry_candidates_last` | function | `tests/test_module_registry_bridge.py:107` | `def test_planner_appends_registry_candidates_last(tmp_path, monkeypatch)` |
| `test_playbook_mentions_map_to_apt_playbook` | function | `tests/test_module_registry_bridge.py:66` | `def test_playbook_mentions_map_to_apt_playbook(tmp_path, monkeypatch)` |
| `TestAutonomousDaemonSWAN` | class | `tests/test_moe_rl_swan.py:493` | `class TestAutonomousDaemonSWAN` |
| `TestDetectionOracle` | class | `tests/test_moe_rl_swan.py:37` | `class TestDetectionOracle` |
| `TestMCPRegistration` | class | `tests/test_moe_rl_swan.py:675` | `class TestMCPRegistration` |
| `TestMoERouter` | class | `tests/test_moe_rl_swan.py:121` | `class TestMoERouter` |
| `TestPolicyDetectionAware` | class | `tests/test_moe_rl_swan.py:571` | `class TestPolicyDetectionAware` |
| `TestRLTrainer` | class | `tests/test_moe_rl_swan.py:223` | `class TestRLTrainer` |
| `TestSwanAgent` | class | `tests/test_moe_rl_swan.py:340` | `class TestSwanAgent` |
| `TestWorldModelGraph` | class | `tests/test_moe_rl_swan.py:616` | `class TestWorldModelGraph` |
| `_ep` | function | `tests/test_moe_rl_swan.py:199` | `def _ep(eid, w)` |
| `_make_trainer` | function | `tests/test_moe_rl_swan.py:285` | `def _make_trainer(suffix)` |
| `_result` | function | `tests/test_moe_rl_swan.py:421` | `def _result(task_type)` |
| `test_add_relation_and_pivot_candidates` | method | `tests/test_moe_rl_swan.py:617` | `def test_add_relation_and_pivot_candidates(self, tmp_path)` |
| `test_assessment_has_required_fields` | method | `tests/test_moe_rl_swan.py:62` | `def test_assessment_has_required_fields(self)` |
| `test_auto_relation_on_service_add` | method | `tests/test_moe_rl_swan.py:645` | `def test_auto_relation_on_service_add(self, tmp_path)` |
| `test_cascade_strategy_contains_swan_selector` | method | `tests/test_moe_rl_swan.py:511` | `def test_cascade_strategy_contains_swan_selector(self)` |
| `test_cascade_strategy_order` | method | `tests/test_moe_rl_swan.py:525` | `def test_cascade_strategy_order(self)` |
| `test_command_decision_source_label` | method | `tests/test_moe_rl_swan.py:548` | `def test_command_decision_source_label(self)` |
| `test_critical_risk_combined_credential_tools` | method | `tests/test_moe_rl_swan.py:54` | `def test_critical_risk_combined_credential_tools(self)` |
| `test_detection_above_threshold_zeroes_reward` | method | `tests/test_moe_rl_swan.py:572` | `def test_detection_above_threshold_zeroes_reward(self)` |
| `test_detection_penalty_lowers_effective_reward` | method | `tests/test_moe_rl_swan.py:281` | `def test_detection_penalty_lowers_effective_reward(self, tmp_path)` |
| `test_encode_state_format` | method | `tests/test_moe_rl_swan.py:224` | `def test_encode_state_format(self)` |
| `test_ensemble_result_dataclass_fields` | method | `tests/test_moe_rl_swan.py:460` | `def test_ensemble_result_dataclass_fields(self)` |
| `test_ensemble_returns_available_candidates` | method | `tests/test_moe_rl_swan.py:143` | `def test_ensemble_returns_available_candidates(self)` |
| `test_epsilon_decays_after_update` | method | `tests/test_moe_rl_swan.py:269` | `def test_epsilon_decays_after_update(self, tmp_path)` |
| `test_evil_winrm_is_high_risk` | method | `tests/test_moe_rl_swan.py:99` | `def test_evil_winrm_is_high_risk(self)` |
| `test_failed_outcome_gives_negative_reward` | method | `tests/test_moe_rl_swan.py:602` | `def test_failed_outcome_gives_negative_reward(self)` |
| `test_fallback_selector_never_returns_none` | method | `tests/test_moe_rl_swan.py:539` | `def test_fallback_selector_never_returns_none(self)` |
| `test_graph_snapshot_is_serialisable` | method | `tests/test_moe_rl_swan.py:634` | `def test_graph_snapshot_is_serialisable(self, tmp_path)` |
| `test_high_risk_mimikatz` | method | `tests/test_moe_rl_swan.py:46` | `def test_high_risk_mimikatz(self)` |
| `test_hive_tools_registered_in_mcp` | method | `tests/test_moe_rl_swan.py:685` | `def test_hive_tools_registered_in_mcp(self)` |
| `test_is_critical_risk_property` | method | `tests/test_moe_rl_swan.py:107` | `def test_is_critical_risk_property(self)` |
| `test_is_high_risk_property_consistent_with_probability` | method | `tests/test_moe_rl_swan.py:75` | `def test_is_high_risk_property_consistent_with_probability(self)` |
| `test_llm_selector_disabled_without_env` | method | `tests/test_moe_rl_swan.py:556` | `def test_llm_selector_disabled_without_env(self)` |
| `test_low_detection_preserves_positive_reward` | method | `tests/test_moe_rl_swan.py:587` | `def test_low_detection_preserves_positive_reward(self)` |
| `test_low_risk_dns_query` | method | `tests/test_moe_rl_swan.py:38` | `def test_low_risk_dns_query(self)` |
| `test_mcp_swan_route_returns_valid_json` | method | `tests/test_moe_rl_swan.py:438` | `def test_mcp_swan_route_returns_valid_json(self)` |

Next: [SYMBOLS_p45.md](SYMBOLS_p45.md)
