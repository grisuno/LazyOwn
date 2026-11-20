# Symbols (page 48 of 54)
Previous: [SYMBOLS_p47.md](SYMBOLS_p47.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `_FakePopen` | class | `tests/test_loop_manager_outcome.py:150` | `class _FakePopen` |
| `_FakeProcess` | class | `tests/test_loop_manager_outcome.py:48` | `class _FakeProcess` |
| `__init__` | method | `tests/test_loop_manager_outcome.py:49` | `def __init__(self, exit_code)` |
| `__init__` | method | `tests/test_loop_manager_outcome.py:151` | `def __init__(self, argv)` |
| `_fake_reap` | function | `tests/test_loop_manager_outcome.py:161` | `def _fake_reap(self, loop_id, process)` |
| `_register` | function | `tests/test_loop_manager_outcome.py:18` | `def _register(manager, loop_id, workspace)` |
| `manager` | function | `tests/test_loop_manager_outcome.py:12` | `def manager(tmp_path)` |
| `test_read_outcome_parses_result_json` | function | `tests/test_loop_manager_outcome.py:56` | `def test_read_outcome_parses_result_json(manager, tmp_path)` |
| `test_reap_cancelled_outcome_maps_stopped` | function | `tests/test_loop_manager_outcome.py:130` | `def test_reap_cancelled_outcome_maps_stopped(manager, tmp_path)` |
| `test_reap_falls_back_to_exit_code_without_outcome` | function | `tests/test_loop_manager_outcome.py:103` | `def test_reap_falls_back_to_exit_code_without_outcome(manager, tmp_path)` |
| `test_reap_marks_failed_on_honest_outcome` | function | `tests/test_loop_manager_outcome.py:68` | `def test_reap_marks_failed_on_honest_outcome(manager, tmp_path)` |
| `test_reap_marks_finished_on_success` | function | `tests/test_loop_manager_outcome.py:87` | `def test_reap_marks_finished_on_success(manager, tmp_path)` |
| `test_reap_stopped_overrides_outcome` | function | `tests/test_loop_manager_outcome.py:116` | `def test_reap_stopped_overrides_outcome(manager, tmp_path)` |
| `test_spawn_binds_workspace_env` | function | `tests/test_loop_manager_outcome.py:145` | `def test_spawn_binds_workspace_env(manager, tmp_path, monkeypatch)` |
| `wait` | method | `tests/test_loop_manager_outcome.py:52` | `def wait(self)` |
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
| `FakePlanner` | class | `tests/test_loop_planner_bridge.py:28` | `class FakePlanner` |
| `boom` | function | `tests/test_loop_planner_bridge.py:39` | `def boom()` |
| `plan` | method | `tests/test_loop_planner_bridge.py:29` | `def plan(self, target, max_candidates)` |
| `test_bridge_dedupes_existing` | function | `tests/test_loop_planner_bridge.py:46` | `def test_bridge_dedupes_existing(monkeypatch)` |
| `test_bridge_disabled` | function | `tests/test_loop_planner_bridge.py:61` | `def test_bridge_disabled(monkeypatch)` |
| `test_technique_candidate_summary_with_command` | function | `tests/test_loop_planner_bridge.py:10` | `def test_technique_candidate_summary_with_command()` |
| `test_technique_candidate_summary_without_command` | function | `tests/test_loop_planner_bridge.py:15` | `def test_technique_candidate_summary_without_command()` |
| `test_technique_intents_converts_candidates` | function | `tests/test_loop_planner_bridge.py:20` | `def test_technique_intents_converts_candidates(monkeypatch)` |
| `test_technique_intents_never_raises` | function | `tests/test_loop_planner_bridge.py:38` | `def test_technique_intents_never_raises(monkeypatch)` |
| `test_classify_ignores_benign_timeout_echo` | function | `tests/test_loop_post_signal.py:19` | `def test_classify_ignores_benign_timeout_echo()` |
| `test_classify_still_flags_real_block_and_error` | function | `tests/test_loop_post_signal.py:30` | `def test_classify_still_flags_real_block_and_error()` |
| `test_guard_step_uses_calibrated_classifier_and_post_signal` | function | `tests/test_loop_post_signal.py:37` | `def test_guard_step_uses_calibrated_classifier_and_post_signal()` |
| `test_post_signal_block_does_not_short_circuit_return` | function | `tests/test_loop_post_signal.py:46` | `def test_post_signal_block_does_not_short_circuit_return()` |
| `_accept` | function | `tests/test_loop_preflight.py:110` | `def _accept()` |
| `test_check_target_fails_fast_on_stopped_lab` | function | `tests/test_loop_preflight.py:39` | `def test_check_target_fails_fast_on_stopped_lab()` |
| `test_check_target_passes_on_running_lab` | function | `tests/test_loop_preflight.py:52` | `def test_check_target_passes_on_running_lab()` |
| `test_check_target_probes_tcp` | function | `tests/test_loop_preflight.py:63` | `def test_check_target_probes_tcp(monkeypatch)` |
| `test_check_target_refused_means_alive` | function | `tests/test_loop_preflight.py:82` | `def test_check_target_refused_means_alive(monkeypatch)` |
| `test_check_target_without_target` | function | `tests/test_loop_preflight.py:94` | `def test_check_target_without_target()` |
| `test_lab_state_maps_running_and_stopped` | function | `tests/test_loop_preflight.py:8` | `def test_lab_state_maps_running_and_stopped()` |
| `test_no_preflight_hint_override` | function | `tests/test_loop_preflight.py:128` | `def test_no_preflight_hint_override()` |
| `test_preflight_flag_parses` | function | `tests/test_loop_preflight.py:136` | `def test_preflight_flag_parses()` |
| `test_probe_tcp_real_socket` | function | `tests/test_loop_preflight.py:102` | `def test_probe_tcp_real_socket()` |
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
| `TestScanBannerGuard` | class | `tests/test_loop_scan_banner_guard.py:98` | `class TestScanBannerGuard` |
| `TestScanOnlyVerb` | class | `tests/test_loop_scan_banner_guard.py:65` | `class TestScanOnlyVerb` |
| `_intent` | function | `tests/test_loop_scan_banner_guard.py:30` | `def _intent(node_id)` |
| `_worker` | function | `tests/test_loop_scan_banner_guard.py:35` | `def _worker(task_id)` |
| `fake_record` | function | `tests/test_loop_scan_banner_guard.py:50` | `def fake_record()` |
| `sink_log` | function | `tests/test_loop_scan_banner_guard.py:43` | `def sink_log()` |
| `test_detector_fires_on_the_nmap_banner` | method | `tests/test_loop_scan_banner_guard.py:99` | `def test_detector_fires_on_the_nmap_banner(self)` |
| `test_interactive_shell_verbs_are_not_scan_only` | method | `tests/test_loop_scan_banner_guard.py:81` | `def test_interactive_shell_verbs_are_not_scan_only(self)` |
| `test_real_nc_shell_still_publishes` | method | `tests/test_loop_scan_banner_guard.py:117` | `def test_real_nc_shell_still_publishes(self, sink_log)` |
| `test_scan_banner_never_publishes_a_shell` | method | `tests/test_loop_scan_banner_guard.py:107` | `def test_scan_banner_never_publishes_a_shell(self, sink_log)` |
| `test_scanners_are_scan_only` | method | `tests/test_loop_scan_banner_guard.py:66` | `def test_scanners_are_scan_only(self)` |
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
| `_Bare` | class | `tests/test_loop_target_authority.py:83` | `class _Bare` |
| `_FakeShell` | class | `tests/test_loop_target_authority.py:16` | `class _FakeShell` |
| `__init__` | method | `tests/test_loop_target_authority.py:19` | `def __init__(self, params)` |
| `__init__` | method | `tests/test_loop_target_authority.py:84` | `def __init__(self)` |
| `_fake_save` | function | `tests/test_loop_target_authority.py:78` | `def _fake_save(params)` |
| `_scope_save` | method | `tests/test_loop_target_authority.py:23` | `def _scope_save(self, entries, mode)` |
| `test_dedupes_and_strips` | function | `tests/test_loop_target_authority.py:49` | `def test_dedupes_and_strips()` |
| `test_empty_targets_is_noop` | function | `tests/test_loop_target_authority.py:68` | `def test_empty_targets_is_noop()` |
| `test_enforcement_mode_untouched` | function | `tests/test_loop_target_authority.py:62` | `def test_enforcement_mode_untouched()` |
| `test_fallback_writer_without_scope_save` | function | `tests/test_loop_target_authority.py:75` | `def test_fallback_writer_without_scope_save(monkeypatch)` |
| `test_multi_target_scope_is_every_target` | function | `tests/test_loop_target_authority.py:42` | `def test_multi_target_scope_is_every_target()` |
| `test_noop_when_already_bound` | function | `tests/test_loop_target_authority.py:55` | `def test_noop_when_already_bound()` |
| `test_single_target_replaces_rhost_and_scope` | function | `tests/test_loop_target_authority.py:31` | `def test_single_target_replaces_rhost_and_scope()` |
| `_agentic` | function | `tests/test_loop_technique_deterministic.py:102` | `def _agentic()` |
| `_executor` | function | `tests/test_loop_technique_deterministic.py:86` | `def _executor(command)` |
| `test_execute_uses_model_for_nontechnique` | function | `tests/test_loop_technique_deterministic.py:95` | `def test_execute_uses_model_for_nontechnique(worker_env, monkeypatch)` |
| `test_steps_for_resolves_technique` | function | `tests/test_loop_technique_deterministic.py:65` | `def test_steps_for_resolves_technique(worker_env)` |
| `test_technique_deterministic_step_when_steps_run` | function | `tests/test_loop_technique_deterministic.py:73` | `def test_technique_deterministic_step_when_steps_run(worker_env, monkeypatch)` |
| `test_technique_intent_classification` | function | `tests/test_loop_technique_deterministic.py:14` | `def test_technique_intent_classification()` |
| `test_technique_steps_are_headless` | function | `tests/test_loop_technique_deterministic.py:25` | `def test_technique_steps_are_headless()` |
| `worker_env` | function | `tests/test_loop_technique_deterministic.py:39` | `def worker_env(tmp_path, monkeypatch)` |
| `_guard` | function | `tests/test_loop_termination.py:24` | `def _guard(task_id, intent_id)` |
| `_guard` | function | `tests/test_loop_termination.py:58` | `def _guard(task_id, intent_id)` |
| `engine` | function | `tests/test_loop_termination.py:11` | `def engine(tmp_path, monkeypatch)` |
| `test_save_tokens_run_wraps_up_without_autopwn` | function | `tests/test_loop_termination.py:42` | `def test_save_tokens_run_wraps_up_without_autopwn(engine, monkeypatch)` |
| `test_save_tokens_skips_terminal_autopwn` | function | `tests/test_loop_termination.py:35` | `def test_save_tokens_skips_terminal_autopwn(engine)` |
| `test_try_hard_continues_running` | function | `tests/test_loop_termination.py:54` | `def test_try_hard_continues_running(engine, monkeypatch)` |
| `_Member` | class | `tests/test_loop_tokens.py:102` | `class _Member` |
| `complete` | method | `tests/test_loop_tokens.py:104` | `def complete(self, prompt, session_key)` |
| `ledger` | function | `tests/test_loop_tokens.py:12` | `def ledger(tmp_path)` |
| `test_charge_and_usage` | function | `tests/test_loop_tokens.py:22` | `def test_charge_and_usage(ledger)` |
| `test_charge_chars_capped` | function | `tests/test_loop_tokens.py:33` | `def test_charge_chars_capped(ledger)` |
| `test_estimate_tokens_floor` | function | `tests/test_loop_tokens.py:17` | `def test_estimate_tokens_floor()` |
| `test_invalid_mode_falls_back` | function | `tests/test_loop_tokens.py:92` | `def test_invalid_mode_falls_back()` |
| `test_policy_defaults_are_try_hard` | function | `tests/test_loop_tokens.py:46` | `def test_policy_defaults_are_try_hard()` |
| `test_policy_intent_cap_degrades_to_deterministic` | function | `tests/test_loop_tokens.py:76` | `def test_policy_intent_cap_degrades_to_deterministic(ledger)` |
| `test_policy_save_tokens_wraps_up` | function | `tests/test_loop_tokens.py:52` | `def test_policy_save_tokens_wraps_up(ledger)` |
| `test_policy_try_hard_degrades_only` | function | `tests/test_loop_tokens.py:60` | `def test_policy_try_hard_degrades_only(ledger)` |
| `test_policy_under_budget_continues` | function | `tests/test_loop_tokens.py:68` | `def test_policy_under_budget_continues(ledger)` |
| `test_reset` | function | `tests/test_loop_tokens.py:40` | `def test_reset(ledger)` |
| `test_usage_sink_publishes` | function | `tests/test_loop_tokens.py:97` | `def test_usage_sink_publishes(monkeypatch, tmp_path)` |
| `test_wrapup_reserve_bounds` | function | `tests/test_loop_tokens.py:85` | `def test_wrapup_reserve_bounds()` |
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
| `test_capability_of_returns_record_or_empty` | function | `tests/test_loop_verb_capabilities.py:27` | `def test_capability_of_returns_record_or_empty()` |
| `test_downgrade_leaves_non_privileged_commands_untouched` | function | `tests/test_loop_verb_capabilities.py:46` | `def test_downgrade_leaves_non_privileged_commands_untouched()` |
| `test_downgrade_rewrites_lazynmap_to_unprivileged_scan` | function | `tests/test_loop_verb_capabilities.py:36` | `def test_downgrade_rewrites_lazynmap_to_unprivileged_scan()` |
| `test_guard_step_wires_the_capability_downgrade` | function | `tests/test_loop_verb_capabilities.py:66` | `def test_guard_step_wires_the_capability_downgrade()` |
| `test_prompts_no_longer_hard_prefer_lazynmap` | function | `tests/test_loop_verb_capabilities.py:72` | `def test_prompts_no_longer_hard_prefer_lazynmap()` |
| `test_requires_privilege_flags_only_privileged_verbs` | function | `tests/test_loop_verb_capabilities.py:18` | `def test_requires_privilege_flags_only_privileged_verbs()` |
| `test_worker_downgrade_depends_on_sudo_availability` | function | `tests/test_loop_verb_capabilities.py:51` | `def test_worker_downgrade_depends_on_sudo_availability(monkeypatch)` |
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
| `_boom` | function | `tests/test_mcp_auto_loop_wrapper.py:34` | `def _boom(shell, params, line, verb)` |
| `_fake_run` | function | `tests/test_mcp_auto_loop_wrapper.py:47` | `def _fake_run(shell, params, line, verb)` |
| `_patched` | function | `tests/test_mcp_auto_loop_wrapper.py:15` | `def _patched(monkeypatch, tmp_path)` |
| `_refuse` | function | `tests/test_mcp_auto_loop_wrapper.py:41` | `def _refuse(shell, params, line, verb)` |
| `_text` | function | `tests/test_mcp_auto_loop_wrapper.py:148` | `def _text(response)` |
| `loop_join` | function | `tests/test_mcp_auto_loop_wrapper.py:163` | `def loop_join(coro)` |
| `test_fast_path_routes_through_the_shared_runner` | function | `tests/test_mcp_auto_loop_wrapper.py:60` | `def test_fast_path_routes_through_the_shared_runner(monkeypatch, tmp_path)` |
| `test_legacy_flag_annotates_but_routes_shared` | function | `tests/test_mcp_auto_loop_wrapper.py:75` | `def test_legacy_flag_annotates_but_routes_shared(monkeypatch, tmp_path)` |
| `test_loop_line_translation` | function | `tests/test_mcp_auto_loop_wrapper.py:131` | `def test_loop_line_translation()` |
| `test_preflight_failed_summary_still_renders_the_task` | function | `tests/test_mcp_auto_loop_wrapper.py:106` | `def test_preflight_failed_summary_still_renders_the_task(monkeypatch, tmp_path)` |
| `test_refused_run_reports_the_reason` | function | `tests/test_mcp_auto_loop_wrapper.py:95` | `def test_refused_run_reports_the_reason(monkeypatch, tmp_path)` |
| `test_runner_failure_surfaces` | function | `tests/test_mcp_auto_loop_wrapper.py:85` | `def test_runner_failure_surfaces(monkeypatch, tmp_path)` |
| `test_schema_matches_the_shared_flags` | function | `tests/test_mcp_auto_loop_wrapper.py:121` | `def test_schema_matches_the_shared_flags()` |
| `TestRegistryDispatch` | class | `tests/test_mcp_dispatch.py:61` | `class TestRegistryDispatch` |
| `_fallback_branches` | function | `tests/test_mcp_dispatch.py:50` | `def _fallback_branches()` |
| `_package_names` | function | `tests/test_mcp_dispatch.py:29` | `def _package_names()` |
| `_registered` | function | `tests/test_mcp_dispatch.py:33` | `def _registered()` |
| `test_mcp_never_offers_interactive_repl` | function | `tests/test_mcp_dispatch.py:121` | `def test_mcp_never_offers_interactive_repl()` |
| `test_migrated_handlers_absent_from_fallback` | method | `tests/test_mcp_dispatch.py:71` | `def test_migrated_handlers_absent_from_fallback(self)` |
| `test_migrated_handlers_registered` | method | `tests/test_mcp_dispatch.py:66` | `def test_migrated_handlers_registered(self)` |
| `test_new_chain_shell_tools_have_defs_and_handlers` | function | `tests/test_mcp_dispatch.py:99` | `def test_new_chain_shell_tools_have_defs_and_handlers()` |
| `test_no_dead_duplicate_branches` | method | `tests/test_mcp_dispatch.py:62` | `def test_no_dead_duplicate_branches(self)` |
| `test_opencode_bridge_curates_loop_and_chain` | function | `tests/test_mcp_dispatch.py:106` | `def test_opencode_bridge_curates_loop_and_chain()` |
| `test_set_config_refuses_null_values` | function | `tests/test_mcp_dispatch.py:79` | `def test_set_config_refuses_null_values()` |
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
| `TestImportPurity` | class | `tests/test_mcp_tools_registry.py:103` | `class TestImportPurity` |
| `TestRegistryDiscovery` | class | `tests/test_mcp_tools_registry.py:62` | `class TestRegistryDiscovery` |
| `TestSingleOwnership` | class | `tests/test_mcp_tools_registry.py:93` | `class TestSingleOwnership` |
| `_legacy_handler_names` | function | `tests/test_mcp_tools_registry.py:45` | `def _legacy_handler_names()` |
| `_legacy_schema_names` | function | `tests/test_mcp_tools_registry.py:30` | `def _legacy_schema_names()` |
| `_registry_names` | function | `tests/test_mcp_tools_registry.py:26` | `def _registry_names()` |
| `test_no_duplicate_handler` | method | `tests/test_mcp_tools_registry.py:98` | `def test_no_duplicate_handler(self)` |
| `test_no_duplicate_schema` | method | `tests/test_mcp_tools_registry.py:94` | `def test_no_duplicate_schema(self)` |
| `test_reference_tool_discovered` | method | `tests/test_mcp_tools_registry.py:63` | `def test_reference_tool_discovered(self)` |
| `test_register_handlers_populates_table` | method | `tests/test_mcp_tools_registry.py:66` | `def test_register_handlers_populates_table(self)` |
| `test_tool_modules_do_not_import_runtime` | method | `tests/test_mcp_tools_registry.py:104` | `def test_tool_modules_do_not_import_runtime(self)` |
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
| `_BrokenSource` | class | `tests/test_metrics_aware_selector.py:216` | `class _BrokenSource` |
| `_StubMetrics` | class | `tests/test_metrics_aware_selector.py:53` | `class _StubMetrics` |
| `_StubSelector` | class | `tests/test_metrics_aware_selector.py:36` | `class _StubSelector(ICommandSelector)` |
| `__init__` | method | `tests/test_metrics_aware_selector.py:39` | `def __init__(self, decision)` |
| `__init__` | method | `tests/test_metrics_aware_selector.py:56` | `def __init__(self, by_command)` |
| `_decision` | function | `tests/test_metrics_aware_selector.py:70` | `def _decision(command)` |
| `fake_clock` | function | `tests/test_metrics_aware_selector.py:168` | `def fake_clock()` |
| `select` | method | `tests/test_metrics_aware_selector.py:43` | `def select(self, target, phase, context)` |
| `summarize` | method | `tests/test_metrics_aware_selector.py:61` | `def summarize(self, window_seconds)` |
| `summarize` | method | `tests/test_metrics_aware_selector.py:217` | `def summarize(self, window_seconds)` |
| `test_accepts_when_success_rate_at_threshold` | function | `tests/test_metrics_aware_selector.py:121` | `def test_accepts_when_success_rate_at_threshold()` |
| `test_chain_falls_through_to_fallback_when_all_filtered` | function | `tests/test_metrics_aware_selector.py:297` | `def test_chain_falls_through_to_fallback_when_all_filtered()` |
| `test_decorator_degrades_when_metrics_source_unavailable` | function | `tests/test_metrics_aware_selector.py:213` | `def test_decorator_degrades_when_metrics_source_unavailable()` |
| `test_filtering_emits_skip_event` | function | `tests/test_metrics_aware_selector.py:264` | `def test_filtering_emits_skip_event(tmp_path, monkeypatch)` |
| `test_filters_when_success_rate_below_threshold` | function | `tests/test_metrics_aware_selector.py:104` | `def test_filters_when_success_rate_below_threshold()` |
| `test_only_filters_named_command_not_whole_decision_object` | function | `tests/test_metrics_aware_selector.py:140` | `def test_only_filters_named_command_not_whole_decision_object()` |
| `test_passthrough_when_insufficient_attempts` | function | `tests/test_metrics_aware_selector.py:86` | `def test_passthrough_when_insufficient_attempts()` |
| `test_passthrough_when_wrapped_returns_none` | function | `tests/test_metrics_aware_selector.py:74` | `def test_passthrough_when_wrapped_returns_none()` |
| `test_summary_forwards_window_seconds` | function | `tests/test_metrics_aware_selector.py:187` | `def test_summary_forwards_window_seconds()` |
| `test_summary_is_cached_within_ttl` | function | `tests/test_metrics_aware_selector.py:157` | `def test_summary_is_cached_within_ttl()` |
| `test_wrap_chain_is_idempotent` | function | `tests/test_metrics_aware_selector.py:252` | `def test_wrap_chain_is_idempotent()` |
| `test_wrap_chain_leaves_fallback_unwrapped` | function | `tests/test_metrics_aware_selector.py:229` | `def test_wrap_chain_leaves_fallback_unwrapped()` |
| `test_wrap_chain_master_switch_off` | function | `tests/test_metrics_aware_selector.py:240` | `def test_wrap_chain_master_switch_off()` |
| `test_zero_window_is_treated_as_unbounded` | function | `tests/test_metrics_aware_selector.py:200` | `def test_zero_window_is_treated_as_unbounded()` |
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

Next: [SYMBOLS_p49.md](SYMBOLS_p49.md)
