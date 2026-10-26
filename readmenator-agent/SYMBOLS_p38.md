# Symbols (page 38 of 46)
Previous: [SYMBOLS_p37.md](SYMBOLS_p37.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_getprompt_renders_three_lines_and_includes_payload_segments` | function | `tests/test_fuzzy_picker.py:280` | `def test_getprompt_renders_three_lines_and_includes_payload_segments()` |
| `test_lazyown_runtime_strings_preserve_shell_payload` | function | `tests/test_fuzzy_picker.py:260` | `def test_lazyown_runtime_strings_preserve_shell_payload(expected_substring)` |
| `test_lazyown_source_has_no_invalid_escape_warning` | function | `tests/test_fuzzy_picker.py:265` | `def test_lazyown_source_has_no_invalid_escape_warning()` |
| `test_picker_cancel_returns_none` | function | `tests/test_fuzzy_picker.py:146` | `def test_picker_cancel_returns_none(sample_items)` |
| `test_picker_empty_input_returns_none` | function | `tests/test_fuzzy_picker.py:152` | `def test_picker_empty_input_returns_none()` |
| `test_picker_routes_through_view_for_multiple_items` | function | `tests/test_fuzzy_picker.py:138` | `def test_picker_routes_through_view_for_multiple_items(sample_items)` |
| `test_picker_short_circuits_single_item` | function | `tests/test_fuzzy_picker.py:132` | `def test_picker_short_circuits_single_item()` |
| `test_prefix_match_outranks_substring` | function | `tests/test_fuzzy_picker.py:84` | `def test_prefix_match_outranks_substring(scorer)` |
| `test_similarity_floor_excludes_unrelated_text` | function | `tests/test_fuzzy_picker.py:98` | `def test_similarity_floor_excludes_unrelated_text(scorer)` |
| `test_strip_ansi_passes_through_plain_text` | function | `tests/test_fuzzy_picker.py:165` | `def test_strip_ansi_passes_through_plain_text()` |
| `test_strip_ansi_removes_csi_sequences` | function | `tests/test_fuzzy_picker.py:160` | `def test_strip_ansi_removes_csi_sequences()` |
| `test_subsequence_match_emits_positions` | function | `tests/test_fuzzy_picker.py:90` | `def test_subsequence_match_emits_positions(scorer, sample_items)` |
| `test_subsequence_positions_helper_returns_empty_when_no_match` | function | `tests/test_fuzzy_picker.py:104` | `def test_subsequence_positions_helper_returns_empty_when_no_match()` |
| `ArtifactSpec` | class | `tests/test_golden_path.py:86` | `class ArtifactSpec(TestCase)` |
| `PushObjectivesSpec` | class | `tests/test_golden_path.py:114` | `class PushObjectivesSpec(TestCase)` |
| `ResolvePathsSpec` | class | `tests/test_golden_path.py:45` | `class ResolvePathsSpec(TestCase)` |
| `_snapshot` | function | `tests/test_golden_path.py:13` | `def _snapshot()` |
| `test_anchor_excluded_from_targets` | method | `tests/test_golden_path.py:48` | `def test_anchor_excluded_from_targets(self)` |
| `test_build_writes_artifact_from_world_model` | method | `tests/test_golden_path.py:89` | `def test_build_writes_artifact_from_world_model(self)` |
| `test_confirmed_credential_beats_unconfirmed` | method | `tests/test_golden_path.py:62` | `def test_confirmed_credential_beats_unconfirmed(self)` |
| `test_critical_exploit_ranked_first_with_severity_cost` | method | `tests/test_golden_path.py:54` | `def test_critical_exploit_ranked_first_with_severity_cost(self)` |
| `test_deterministic_and_stable` | method | `tests/test_golden_path.py:79` | `def test_deterministic_and_stable(self)` |
| `test_lateral_relation_via_anchor` | method | `tests/test_golden_path.py:67` | `def test_lateral_relation_via_anchor(self)` |
| `test_load_artifact_tolerant_when_missing` | method | `tests/test_golden_path.py:109` | `def test_load_artifact_tolerant_when_missing(self)` |
| `test_priority_bands` | method | `tests/test_golden_path.py:136` | `def test_priority_bands(self)` |
| `test_push_and_dedupe` | method | `tests/test_golden_path.py:117` | `def test_push_and_dedupe(self)` |
| `test_runs_service_edges_ignored` | method | `tests/test_golden_path.py:73` | `def test_runs_service_edges_ignored(self)` |
| `advisor` | function | `tests/test_graph_advisor.py:133` | `def advisor(small_graph_path)` |
| `small_graph_data` | function | `tests/test_graph_advisor.py:34` | `def small_graph_data()` |
| `small_graph_path` | function | `tests/test_graph_advisor.py:126` | `def small_graph_path(tmp_path, small_graph_data)` |
| `test_advisor_did_you_mean_returns_close_labels` | function | `tests/test_graph_advisor.py:268` | `def test_advisor_did_you_mean_returns_close_labels(advisor)` |
| `test_advisor_god_nodes_ranks_by_degree` | function | `tests/test_graph_advisor.py:254` | `def test_advisor_god_nodes_ranks_by_degree(advisor)` |
| `test_advisor_handles_missing_graph_gracefully` | function | `tests/test_graph_advisor.py:280` | `def test_advisor_handles_missing_graph_gracefully(tmp_path)` |
| `test_advisor_neighbors_respects_depth` | function | `tests/test_graph_advisor.py:248` | `def test_advisor_neighbors_respects_depth(advisor)` |
| `test_advisor_neighbors_returns_layered_walk` | function | `tests/test_graph_advisor.py:239` | `def test_advisor_neighbors_returns_layered_walk(advisor)` |
| `test_advisor_reads_recent_commands_from_csv` | function | `tests/test_graph_advisor.py:292` | `def test_advisor_reads_recent_commands_from_csv(tmp_path, advisor)` |
| `test_advisor_search_returns_ranked_nodes` | function | `tests/test_graph_advisor.py:231` | `def test_advisor_search_returns_ranked_nodes(advisor)` |
| `test_advisor_suggest_next_walks_from_recent` | function | `tests/test_graph_advisor.py:260` | `def test_advisor_suggest_next_walks_from_recent(advisor)` |
| `test_advisor_summary_flags_empty_graph` | function | `tests/test_graph_advisor.py:199` | `def test_advisor_summary_flags_empty_graph(tmp_path)` |
| `test_advisor_summary_flags_stale_graph` | function | `tests/test_graph_advisor.py:212` | `def test_advisor_summary_flags_stale_graph(tmp_path)` |
| `test_advisor_summary_reports_topology` | function | `tests/test_graph_advisor.py:188` | `def test_advisor_summary_reports_topology(advisor)` |
| `test_advisor_truncate_respects_token_budget` | function | `tests/test_graph_advisor.py:274` | `def test_advisor_truncate_respects_token_budget(advisor)` |
| `test_format_god_nodes_handles_empty` | function | `tests/test_graph_advisor.py:322` | `def test_format_god_nodes_handles_empty()` |
| `test_format_neighbors_renders_when_match_found` | function | `tests/test_graph_advisor.py:316` | `def test_format_neighbors_renders_when_match_found(advisor)` |
| `test_format_search_table_renders_rows` | function | `tests/test_graph_advisor.py:309` | `def test_format_search_table_renders_rows(advisor)` |
| `test_format_suggestions_handles_empty` | function | `tests/test_graph_advisor.py:326` | `def test_format_suggestions_handles_empty()` |
| `test_index_builds_adjacency_and_degree` | function | `tests/test_graph_advisor.py:153` | `def test_index_builds_adjacency_and_degree(small_graph_data)` |
| `test_loader_resolves_explicit_path` | function | `tests/test_graph_advisor.py:138` | `def test_loader_resolves_explicit_path(tmp_path, small_graph_data)` |
| `test_loader_returns_none_when_missing` | function | `tests/test_graph_advisor.py:147` | `def test_loader_returns_none_when_missing(tmp_path)` |
| `test_real_graph_summary_when_available` | function | `tests/test_graph_advisor.py:333` | `def test_real_graph_summary_when_available()` |
| `test_scorer_prefers_prefix_match` | function | `tests/test_graph_advisor.py:174` | `def test_scorer_prefers_prefix_match(small_graph_data)` |
| `test_scorer_returns_empty_for_unrelated_query` | function | `tests/test_graph_advisor.py:182` | `def test_scorer_returns_empty_for_unrelated_query(small_graph_data)` |
| `_FakeAdvisor` | class | `tests/test_graph_overlay.py:25` | `class _FakeAdvisor` |
| `__init__` | method | `tests/test_graph_overlay.py:26` | `def __init__(self, available)` |
| `god_nodes` | method | `tests/test_graph_overlay.py:32` | `def god_nodes(self, limit)` |
| `is_available` | method | `tests/test_graph_overlay.py:29` | `def is_available(self)` |
| `neighbors` | method | `tests/test_graph_overlay.py:39` | `def neighbors(self, query, depth, limit)` |
| `runner` | function | `tests/test_graph_overlay.py:129` | `def runner(context)` |
| `test_build_state_uses_default_factory_signature` | function | `tests/test_graph_overlay.py:135` | `def test_build_state_uses_default_factory_signature()` |
| `test_focus_switches_to_neighbors_view` | function | `tests/test_graph_overlay.py:72` | `def test_focus_switches_to_neighbors_view()` |
| `test_focus_unknown_returns_no_match_message` | function | `tests/test_graph_overlay.py:85` | `def test_focus_unknown_returns_no_match_message()` |
| `test_god_nodes_view_returns_hubs` | function | `tests/test_graph_overlay.py:61` | `def test_god_nodes_view_returns_hubs()` |
| `test_is_available_returns_false_when_advisor_missing` | function | `tests/test_graph_overlay.py:55` | `def test_is_available_returns_false_when_advisor_missing()` |
| `test_launch_overlay_uses_runner` | function | `tests/test_graph_overlay.py:122` | `def test_launch_overlay_uses_runner()` |
| `test_toggle_view_round_trip` | function | `tests/test_graph_overlay.py:108` | `def test_toggle_view_round_trip()` |
| `test_unavailable_advisor_returns_no_graph_message` | function | `tests/test_graph_overlay.py:97` | `def test_unavailable_advisor_returns_no_graph_message()` |
| `TestAdvisoriesAndFeatures` | class | `tests/test_guardrails.py:116` | `class TestAdvisoriesAndFeatures` |
| `TestAptChainWiring` | class | `tests/test_guardrails.py:298` | `class TestAptChainWiring` |
| `TestCapacityEnvelope` | class | `tests/test_guardrails.py:36` | `class TestCapacityEnvelope` |
| `TestCheckpointLedger` | class | `tests/test_guardrails.py:83` | `class TestCheckpointLedger` |
| `TestGlobalHarness` | class | `tests/test_guardrails.py:229` | `class TestGlobalHarness` |
| `TestGuardHarness` | class | `tests/test_guardrails.py:144` | `class TestGuardHarness` |
| `TestLazyLoopWiring` | class | `tests/test_guardrails.py:243` | `class TestLazyLoopWiring` |
| `TestOrchestratorHarnessTab` | class | `tests/test_guardrails.py:344` | `class TestOrchestratorHarnessTab` |
| `TestTaskClass` | class | `tests/test_guardrails.py:26` | `class TestTaskClass` |
| `_drive` | function | `tests/test_guardrails.py:385` | `def _drive()` |
| `_fresh_global_harness` | method | `tests/test_guardrails.py:231` | `def _fresh_global_harness(self)` |
| `_fresh_global_harness` | method | `tests/test_guardrails.py:245` | `def _fresh_global_harness(self)` |
| `_fresh_global_harness` | method | `tests/test_guardrails.py:300` | `def _fresh_global_harness(self)` |
| `_load` | function | `tests/test_guardrails.py:361` | `def _load(target)` |
| `_save` | function | `tests/test_guardrails.py:364` | `def _save(data, target)` |
| `always_fails` | function | `tests/test_guardrails.py:182` | `def always_fails()` |
| `boom` | function | `tests/test_guardrails.py:154` | `def boom()` |
| `boom` | function | `tests/test_guardrails.py:190` | `def boom()` |
| `flaky` | function | `tests/test_guardrails.py:171` | `def flaky()` |
| `harness` | method | `tests/test_guardrails.py:146` | `def harness(self)` |
| `interrupted` | function | `tests/test_guardrails.py:198` | `def interrupted()` |
| `sandbox` | method | `tests/test_guardrails.py:346` | `def sandbox(self, tmp_path, monkeypatch)` |
| `test_admit_and_account_roundtrip` | method | `tests/test_guardrails.py:43` | `def test_admit_and_account_roundtrip(self)` |
| `test_apply_profile_configures_harness` | method | `tests/test_guardrails.py:250` | `def test_apply_profile_configures_harness(self, tmp_path, monkeypatch)` |
| `test_capture_rejects_blank_keys` | method | `tests/test_guardrails.py:112` | `def test_capture_rejects_blank_keys(self)` |
| `test_capture_restore_roundtrip` | method | `tests/test_guardrails.py:84` | `def test_capture_restore_roundtrip(self)` |
| `test_clear_returns_count` | method | `tests/test_guardrails.py:125` | `def test_clear_returns_count(self)` |
| `test_command_registered` | method | `tests/test_guardrails.py:353` | `def test_command_registered(self)` |
| `test_config_section_constant_shape` | method | `tests/test_guardrails.py:239` | `def test_config_section_constant_shape(self)` |
| `test_configure_clamps_and_accepts_names` | method | `tests/test_guardrails.py:75` | `def test_configure_clamps_and_accepts_names(self)` |
| `test_configure_from_payload_section` | method | `tests/test_guardrails.py:215` | `def test_configure_from_payload_section(self, harness)` |
| `test_core_gives_up_after_second_failure` | method | `tests/test_guardrails.py:181` | `def test_core_gives_up_after_second_failure(self, harness)` |
| `test_core_retries_once_after_warm_restart` | method | `tests/test_guardrails.py:168` | `def test_core_retries_once_after_warm_restart(self, harness)` |
| `test_core_without_checkpoint_never_retries` | method | `tests/test_guardrails.py:189` | `def test_core_without_checkpoint_never_retries(self, harness)` |
| `test_defaults_snapshot` | method | `tests/test_guardrails.py:37` | `def test_defaults_snapshot(self)` |
| `test_feature_gate_known_set` | method | `tests/test_guardrails.py:139` | `def test_feature_gate_known_set(self)` |
| `test_feature_gate_unknown_feature_never_suspends` | method | `tests/test_guardrails.py:132` | `def test_feature_gate_unknown_feature_never_suspends(self)` |
| `test_guardrails_persist_via_payload` | method | `tests/test_guardrails.py:358` | `def test_guardrails_persist_via_payload(self, monkeypatch, sandbox)` |
| `test_harness_tab_composes_headless` | method | `tests/test_guardrails.py:380` | `def test_harness_tab_composes_headless(self, sandbox, monkeypatch)` |
| `test_higher_tier_saturation_refuses_lower_tiers` | method | `tests/test_guardrails.py:58` | `def test_higher_tier_saturation_refuses_lower_tiers(self)` |
| `test_history_is_bounded` | method | `tests/test_guardrails.py:89` | `def test_history_is_bounded(self)` |
| `test_is_known_accepts_values_and_rejects_strays` | method | `tests/test_guardrails.py:30` | `def test_is_known_accepts_values_and_rejects_strays(self)` |
| `test_keyboard_interrupt_propagates` | method | `tests/test_guardrails.py:197` | `def test_keyboard_interrupt_propagates(self, harness)` |
| `test_mission_failure_degrades_with_advisory` | method | `tests/test_guardrails.py:153` | `def test_mission_failure_degrades_with_advisory(self, harness)` |
| `test_mission_success_accounts_usage` | method | `tests/test_guardrails.py:149` | `def test_mission_success_accounts_usage(self, harness)` |
| `test_notice_is_bounded_newest_first` | method | `tests/test_guardrails.py:117` | `def test_notice_is_bounded_newest_first(self)` |
| `test_priority_reservation_refuses_lower_tiers` | method | `tests/test_guardrails.py:204` | `def test_priority_reservation_refuses_lower_tiers(self, harness)` |
| `test_reclaim_purges_support_only` | method | `tests/test_guardrails.py:66` | `def test_reclaim_purges_support_only(self)` |
| `test_recovery_guard_returns_none_when_refused` | method | `tests/test_guardrails.py:305` | `def test_recovery_guard_returns_none_when_refused(self, monkeypatch)` |
| `test_restore_missing_is_none` | method | `tests/test_guardrails.py:96` | `def test_restore_missing_is_none(self)` |
| `test_round_guard_halt_maps_to_degraded_abort` | method | `tests/test_guardrails.py:285` | `def test_round_guard_halt_maps_to_degraded_abort(self, tmp_path, monkeypatch)` |
| `test_saturated_tier_refuses_admission` | method | `tests/test_guardrails.py:51` | `def test_saturated_tier_refuses_admission(self)` |
| `test_singleton_shared` | method | `tests/test_guardrails.py:236` | `def test_singleton_shared(self)` |
| `test_support_refused_while_render_suspended` | method | `tests/test_guardrails.py:161` | `def test_support_refused_while_render_suspended(self, harness)` |
| `test_tier_ordering_is_strict` | method | `tests/test_guardrails.py:27` | `def test_tier_ordering_is_strict(self)` |
| `test_warm_restart_purges_support_and_notifies` | method | `tests/test_guardrails.py:220` | `def test_warm_restart_purges_support_and_notifies(self, harness)` |
| `test_warm_restart_restores_and_counts` | method | `tests/test_guardrails.py:99` | `def test_warm_restart_restores_and_counts(self)` |
| `test_warm_restart_without_key_reports_unrestored` | method | `tests/test_guardrails.py:107` | `def test_warm_restart_without_key_reports_unrestored(self)` |
| `test_worker_guard_maps_refusal_to_degraded_outcome` | method | `tests/test_guardrails.py:266` | `def test_worker_guard_maps_refusal_to_degraded_outcome(self, tmp_path, monkeypatch)` |
| `SafeHtmlHelperTests` | class | `tests/test_gui_xss_sinks.py:26` | `class SafeHtmlHelperTests(TestCase)` |
| `SinkSanitizationTests` | class | `tests/test_gui_xss_sinks.py:37` | `class SinkSanitizationTests(TestCase)` |
| `_read_template` | function | `tests/test_gui_xss_sinks.py:21` | `def _read_template()` |
| `test_helper_is_defined_exactly_once` | method | `tests/test_gui_xss_sinks.py:27` | `def test_helper_is_defined_exactly_once(self)` |
| `test_helper_prefers_dompurify_with_text_fallback` | method | `tests/test_gui_xss_sinks.py:31` | `def test_helper_prefers_dompurify_with_text_fallback(self)` |
| `test_no_raw_error_interpolation` | method | `tests/test_gui_xss_sinks.py:50` | `def test_no_raw_error_interpolation(self)` |
| `test_no_raw_html_interpolation` | method | `tests/test_gui_xss_sinks.py:43` | `def test_no_raw_html_interpolation(self)` |
| `test_no_raw_output_interpolation` | method | `tests/test_gui_xss_sinks.py:61` | `def test_no_raw_output_interpolation(self)` |
| `test_no_raw_response_interpolation` | method | `tests/test_gui_xss_sinks.py:38` | `def test_no_raw_response_interpolation(self)` |
| `sandbox` | function | `tests/test_gym_cli.py:11` | `def sandbox(tmp_path, monkeypatch)` |
| `test_atomic_shell_marks_target_compromised` | function | `tests/test_gym_cli.py:123` | `def test_atomic_shell_marks_target_compromised(sandbox, monkeypatch, capsys)` |
| `test_gym_start_status_stop_lifecycle` | function | `tests/test_gym_cli.py:39` | `def test_gym_start_status_stop_lifecycle(sandbox, capsys)` |
| `test_gym_status_explains_live_shell_without_gym` | function | `tests/test_gym_cli.py:82` | `def test_gym_status_explains_live_shell_without_gym(sandbox, monkeypatch, capsys)` |
| `test_gym_status_filters_hosts_by_current_target` | function | `tests/test_gym_cli.py:103` | `def test_gym_status_filters_hosts_by_current_target(sandbox, monkeypatch, capsys)` |
| `test_gym_stop_all_and_by_name` | function | `tests/test_gym_cli.py:65` | `def test_gym_stop_all_and_by_name(sandbox, capsys)` |
| `test_gym_stop_without_active_is_clean` | function | `tests/test_gym_cli.py:32` | `def test_gym_stop_without_active_is_clean(sandbox, capsys)` |
| `test_gym_top_aliases_leaderboard` | function | `tests/test_gym_cli.py:97` | `def test_gym_top_aliases_leaderboard(sandbox, capsys)` |
| `_FakeDocker` | class | `tests/test_gym_lifecycle.py:38` | `class _FakeDocker` |
| `__call__` | method | `tests/test_gym_lifecycle.py:45` | `def __call__(self)` |
| `__init__` | method | `tests/test_gym_lifecycle.py:41` | `def __init__(self, responses)` |
| `__init__` | method | `tests/test_gym_lifecycle.py:54` | `def __init__(self, returncode, stdout, stderr)` |
| `_result` | class | `tests/test_gym_lifecycle.py:53` | `class _result` |
| `sandbox` | function | `tests/test_gym_lifecycle.py:20` | `def sandbox(tmp_path, monkeypatch)` |
| `test_cleanup_gym_machines_stops_all` | function | `tests/test_gym_lifecycle.py:162` | `def test_cleanup_gym_machines_stops_all(tmp_path, monkeypatch, capsys)` |
| `test_start_removes_stale_container_first` | function | `tests/test_gym_lifecycle.py:107` | `def test_start_removes_stale_container_first(sandbox, monkeypatch)` |
| `test_start_spins_scenario_and_resolves_ip` | function | `tests/test_gym_lifecycle.py:60` | `def test_start_spins_scenario_and_resolves_ip(sandbox, monkeypatch)` |
| `test_start_without_docker_degrades_gracefully` | function | `tests/test_gym_lifecycle.py:99` | `def test_start_without_docker_degrades_gracefully(sandbox, monkeypatch)` |
| `test_start_without_lab_flag_still_registers` | function | `tests/test_gym_lifecycle.py:89` | `def test_start_without_lab_flag_still_registers(sandbox, monkeypatch)` |
| `test_stop_keeps_scenario_with_active_runs` | function | `tests/test_gym_lifecycle.py:142` | `def test_stop_keeps_scenario_with_active_runs(sandbox, monkeypatch)` |
| `test_stop_teardowns_scenario_container` | function | `tests/test_gym_lifecycle.py:122` | `def test_stop_teardowns_scenario_container(sandbox, monkeypatch)` |
| `CtfCaptureSpec` | class | `tests/test_gym_matrix_ctf.py:13` | `class CtfCaptureSpec(TestCase)` |
| `GymMatrixRunnerSpec` | class | `tests/test_gym_matrix_ctf.py:62` | `class GymMatrixRunnerSpec(TestCase)` |
| `ReportIntegrationSpec` | class | `tests/test_gym_matrix_ctf.py:120` | `class ReportIntegrationSpec(TestCase)` |
| `executor` | function | `tests/test_gym_matrix_ctf.py:92` | `def executor(cmd)` |
| `test_captured_findings_enter_report` | method | `tests/test_gym_matrix_ctf.py:123` | `def test_captured_findings_enter_report(self)` |
| `test_failed_capture_without_evidence` | method | `tests/test_gym_matrix_ctf.py:29` | `def test_failed_capture_without_evidence(self)` |
| `test_load_artifact` | method | `tests/test_gym_matrix_ctf.py:57` | `def test_load_artifact(self)` |
| `test_plan_isolates_only_filter` | method | `tests/test_gym_matrix_ctf.py:72` | `def test_plan_isolates_only_filter(self)` |
| `test_plan_ordered_by_severity` | method | `tests/test_gym_matrix_ctf.py:65` | `def test_plan_ordered_by_severity(self)` |
| `test_plan_rejects_empty_target` | method | `tests/test_gym_matrix_ctf.py:76` | `def test_plan_rejects_empty_target(self)` |
| `test_root_shell_capture` | method | `tests/test_gym_matrix_ctf.py:16` | `def test_root_shell_capture(self)` |
| `test_run_matrix_dry_run_writes_no_capture` | method | `tests/test_gym_matrix_ctf.py:80` | `def test_run_matrix_dry_run_writes_no_capture(self)` |
| `test_run_matrix_executes_and_captures` | method | `tests/test_gym_matrix_ctf.py:91` | `def test_run_matrix_executes_and_captures(self)` |
| `test_run_matrix_flags_missing_chain` | method | `tests/test_gym_matrix_ctf.py:110` | `def test_run_matrix_flags_missing_chain(self)` |
| `test_shadow_evidence_masked` | method | `tests/test_gym_matrix_ctf.py:44` | `def test_shadow_evidence_masked(self)` |
| `test_unknown_vuln_rejected` | method | `tests/test_gym_matrix_ctf.py:39` | `def test_unknown_vuln_rejected(self)` |
| `test_gym_ms2_chains_lists_index` | function | `tests/test_gym_ms2_cli.py:4` | `def test_gym_ms2_chains_lists_index(capsys)` |
| `_write_definition` | function | `tests/test_gym_registry.py:35` | `def _write_definition(directory, gym_id)` |
| `sandbox` | function | `tests/test_gym_registry.py:14` | `def sandbox(tmp_path, monkeypatch)` |
| `test_definition_crud_is_confined` | function | `tests/test_gym_registry.py:71` | `def test_definition_crud_is_confined(sandbox, tmp_path)` |
| `test_delete_refuses_active_definition` | function | `tests/test_gym_registry.py:145` | `def test_delete_refuses_active_definition(sandbox)` |
| `test_legacy_active_files_are_imported_once` | function | `tests/test_gym_registry.py:156` | `def test_legacy_active_files_are_imported_once(sandbox, monkeypatch)` |
| `test_shipped_catalogue_loads` | function | `tests/test_gym_registry.py:63` | `def test_shipped_catalogue_loads()` |
| `test_start_status_stop_all_persists` | function | `tests/test_gym_registry.py:93` | `def test_start_status_stop_all_persists(sandbox)` |
| `test_stop_by_id_and_name` | function | `tests/test_gym_registry.py:116` | `def test_stop_by_id_and_name(sandbox)` |
| `test_submit_requires_disambiguation` | function | `tests/test_gym_registry.py:129` | `def test_submit_requires_disambiguation(sandbox)` |
| `ChainDirectiveSpec` | class | `tests/test_harness_mode.py:123` | `class ChainDirectiveSpec(TestCase)` |
| `GateSpec` | class | `tests/test_harness_mode.py:65` | `class GateSpec(TestCase)` |
| `HarnessFlagSpec` | class | `tests/test_harness_mode.py:14` | `class HarnessFlagSpec(TestCase)` |
| `HarnessProfileSpec` | class | `tests/test_harness_mode.py:46` | `class HarnessProfileSpec(TestCase)` |
| `ObjectiveDirectiveSpec` | class | `tests/test_harness_mode.py:144` | `class ObjectiveDirectiveSpec(TestCase)` |
| `_explode` | function | `tests/test_harness_mode.py:93` | `def _explode()` |
| `_llm_steps` | function | `tests/test_harness_mode.py:112` | `def _llm_steps(_intent, _prior)` |
| `_planner_returns_none_without_llm` | method | `tests/test_harness_mode.py:68` | `def _planner_returns_none_without_llm(self)` |
| `setUp` | method | `tests/test_harness_mode.py:17` | `def setUp(self)` |
| `tearDown` | method | `tests/test_harness_mode.py:20` | `def tearDown(self)` |
| `test_env_flag_enables` | method | `tests/test_harness_mode.py:26` | `def test_env_flag_enables(self)` |
| `test_env_flag_off_overrides_profile` | method | `tests/test_harness_mode.py:32` | `def test_env_flag_off_overrides_profile(self)` |
| `test_known_chain_resolves` | method | `tests/test_harness_mode.py:126` | `def test_known_chain_resolves(self)` |
| `test_payload_section_disables` | method | `tests/test_harness_mode.py:41` | `def test_payload_section_disables(self)` |
| `test_payload_section_enables` | method | `tests/test_harness_mode.py:37` | `def test_payload_section_enables(self)` |
| `test_plan_llm_gate_blocked_under_harness` | method | `tests/test_harness_mode.py:79` | `def test_plan_llm_gate_blocked_under_harness(self)` |
| `test_profile_flags` | method | `tests/test_harness_mode.py:54` | `def test_profile_flags(self)` |
| `test_profile_present` | method | `tests/test_harness_mode.py:49` | `def test_profile_present(self)` |
| `test_push_objective_text_carries_directive` | method | `tests/test_harness_mode.py:147` | `def test_push_objective_text_carries_directive(self)` |
| `test_target_token_fallback` | method | `tests/test_harness_mode.py:137` | `def test_target_token_fallback(self)` |
| `test_unknown_chain_rejected` | method | `tests/test_harness_mode.py:132` | `def test_unknown_chain_rejected(self)` |
| `test_worker_agentic_gate_blocked_under_harness` | method | `tests/test_harness_mode.py:84` | `def test_worker_agentic_gate_blocked_under_harness(self)` |
| `test_worker_llm_steps_gate_keeps_base_steps` | method | `tests/test_harness_mode.py:104` | `def test_worker_llm_steps_gate_keeps_base_steps(self)` |
| `TestCrackResult` | class | `tests/test_hash_cracker.py:91` | `class TestCrackResult` |
| `TestFileIdentification` | class | `tests/test_hash_cracker.py:66` | `class TestFileIdentification` |
| `TestHashIdentification` | class | `tests/test_hash_cracker.py:14` | `class TestHashIdentification` |
| `TestHashIdentifier` | class | `tests/test_hash_cracker.py:129` | `class TestHashIdentifier` |
| `TestHashPatterns` | class | `tests/test_hash_cracker.py:114` | `class TestHashPatterns` |
| `TestWordlists` | class | `tests/test_hash_cracker.py:122` | `class TestWordlists` |
| `test_all_patterns_exist` | method | `tests/test_hash_cracker.py:115` | `def test_all_patterns_exist(self)` |
| `test_crack_result_cracked` | method | `tests/test_hash_cracker.py:102` | `def test_crack_result_cracked(self)` |
| `test_crack_result_defaults` | method | `tests/test_hash_cracker.py:92` | `def test_crack_result_defaults(self)` |
| `test_hash_identifier_fields` | method | `tests/test_hash_cracker.py:130` | `def test_hash_identifier_fields(self)` |
| `test_identify_empty` | method | `tests/test_hash_cracker.py:41` | `def test_identify_empty(self)` |
| `test_identify_file_empty` | method | `tests/test_hash_cracker.py:67` | `def test_identify_file_empty(self, tmp_path)` |
| `test_identify_file_not_exists` | method | `tests/test_hash_cracker.py:85` | `def test_identify_file_not_exists(self)` |
| `test_identify_file_with_hashes` | method | `tests/test_hash_cracker.py:74` | `def test_identify_file_with_hashes(self, tmp_path)` |
| `test_identify_kerberos_tgs` | method | `tests/test_hash_cracker.py:46` | `def test_identify_kerberos_tgs(self)` |
| `test_identify_md5` | method | `tests/test_hash_cracker.py:53` | `def test_identify_md5(self)` |
| `test_identify_ntlm` | method | `tests/test_hash_cracker.py:15` | `def test_identify_ntlm(self)` |
| `test_identify_ntlm_from_secretsdump` | method | `tests/test_hash_cracker.py:22` | `def test_identify_ntlm_from_secretsdump(self)` |
| `test_identify_sha1` | method | `tests/test_hash_cracker.py:59` | `def test_identify_sha1(self)` |
| `test_identify_sha512crypt` | method | `tests/test_hash_cracker.py:29` | `def test_identify_sha512crypt(self)` |
| `test_identify_unknown` | method | `tests/test_hash_cracker.py:36` | `def test_identify_unknown(self)` |
| `test_wordlist_paths_are_strings` | method | `tests/test_hash_cracker.py:123` | `def test_wordlist_paths_are_strings(self)` |
| `HelpUiSuiteConfig` | class | `tests/test_help_ui_command_set.py:38` | `class HelpUiSuiteConfig` |
| `_add_repo_root_to_syspath` | function | `tests/test_help_ui_command_set.py:32` | `def _add_repo_root_to_syspath()` |
| `_methods_of` | function | `tests/test_help_ui_command_set.py:65` | `def _methods_of(path, class_name)` |
| `test_no_command_collisions_with_source` | function | `tests/test_help_ui_command_set.py:112` | `def test_no_command_collisions_with_source()` |
| `test_registry_registers_target` | function | `tests/test_help_ui_command_set.py:105` | `def test_registry_registers_target()` |
| `test_source_no_longer_defines_cluster` | function | `tests/test_help_ui_command_set.py:99` | `def test_source_no_longer_defines_cluster()` |
| `test_target_exposes_full_help_cluster` | function | `tests/test_help_ui_command_set.py:86` | `def test_target_exposes_full_help_cluster()` |
| `test_target_is_active_command_set` | function | `tests/test_help_ui_command_set.py:77` | `def test_target_is_active_command_set()` |
| `test_target_phase_metadata` | function | `tests/test_help_ui_command_set.py:93` | `def test_target_phase_metadata()` |
| `TestCliGatesDelegate` | class | `tests/test_host_policy.py:73` | `class TestCliGatesDelegate` |
| `TestSharedPolicy` | class | `tests/test_host_policy.py:51` | `class TestSharedPolicy` |
| `test_check_lhost_matches_policy` | method | `tests/test_host_policy.py:81` | `def test_check_lhost_matches_policy(self, capsys)` |
| `test_check_lport_unchanged` | method | `tests/test_host_policy.py:88` | `def test_check_lport_unchanged(self, capsys)` |
| `test_check_rhost_matches_policy` | method | `tests/test_host_policy.py:74` | `def test_check_rhost_matches_policy(self, capsys)` |
| `test_invalid_hosts_rejected` | method | `tests/test_host_policy.py:57` | `def test_invalid_hosts_rejected(self)` |
| `test_pinned_quirks_unchanged` | method | `tests/test_host_policy.py:67` | `def test_pinned_quirks_unchanged(self)` |
| `test_shell_meta_rejected` | method | `tests/test_host_policy.py:62` | `def test_shell_meta_rejected(self)` |
| `test_valid_hosts_accepted` | method | `tests/test_host_policy.py:52` | `def test_valid_hosts_accepted(self)` |
| `TestBenignTagsPreserved` | class | `tests/test_html_sanitizer.py:71` | `class TestBenignTagsPreserved` |
| `TestCustomAllowlist` | class | `tests/test_html_sanitizer.py:93` | `class TestCustomAllowlist` |
| `TestEventHandlerStripping` | class | `tests/test_html_sanitizer.py:49` | `class TestEventHandlerStripping` |
| `TestJavascriptUriStripping` | class | `tests/test_html_sanitizer.py:63` | `class TestJavascriptUriStripping` |
| `TestScriptStripping` | class | `tests/test_html_sanitizer.py:25` | `class TestScriptStripping` |
| `test_basic_formatting_preserved` | method | `tests/test_html_sanitizer.py:74` | `def test_basic_formatting_preserved(self)` |
| `test_headings_preserved` | method | `tests/test_html_sanitizer.py:86` | `def test_headings_preserved(self)` |
| `test_iframe_removed` | method | `tests/test_html_sanitizer.py:33` | `def test_iframe_removed(self)` |
| `test_javascript_href_stripped` | method | `tests/test_html_sanitizer.py:66` | `def test_javascript_href_stripped(self)` |
| `test_lists_preserved` | method | `tests/test_html_sanitizer.py:81` | `def test_lists_preserved(self)` |
| `test_object_and_embed_removed` | method | `tests/test_html_sanitizer.py:38` | `def test_object_and_embed_removed(self)` |
| `test_onclick_removed` | method | `tests/test_html_sanitizer.py:52` | `def test_onclick_removed(self)` |
| `test_onerror_removed` | method | `tests/test_html_sanitizer.py:57` | `def test_onerror_removed(self)` |
| `test_script_block_removed` | method | `tests/test_html_sanitizer.py:28` | `def test_script_block_removed(self)` |
| `test_strict_allowlist_strips_more` | method | `tests/test_html_sanitizer.py:96` | `def test_strict_allowlist_strips_more(self)` |
| `test_style_removed` | method | `tests/test_html_sanitizer.py:43` | `def test_style_removed(self)` |
| `TestHTTPSRedirect` | class | `tests/test_https_redirect.py:34` | `class TestHTTPSRedirect` |
| `TestRedirectResponseShape` | class | `tests/test_https_redirect.py:74` | `class TestRedirectResponseShape` |
| `_FakeRequest` | class | `tests/test_https_redirect.py:23` | `class _FakeRequest` |
| `__init__` | method | `tests/test_https_redirect.py:24` | `def __init__(self, is_secure, host, path, query_string)` |
| `test_insecure_in_dev_passes_through` | method | `tests/test_https_redirect.py:50` | `def test_insecure_in_dev_passes_through(self)` |
| `test_insecure_in_prod_redirects_to_https` | method | `tests/test_https_redirect.py:42` | `def test_insecure_in_prod_redirects_to_https(self)` |
| `test_insecure_when_disabled_passes_through` | method | `tests/test_https_redirect.py:55` | `def test_insecure_when_disabled_passes_through(self)` |
| `test_query_string_preserved` | method | `tests/test_https_redirect.py:60` | `def test_query_string_preserved(self)` |
| `test_response_is_named_tuple_like` | method | `tests/test_https_redirect.py:77` | `def test_response_is_named_tuple_like(self)` |
| `test_root_path_preserved` | method | `tests/test_https_redirect.py:67` | `def test_root_path_preserved(self)` |
| `test_secure_request_passes_through` | method | `tests/test_https_redirect.py:37` | `def test_secure_request_passes_through(self)` |
| `_event` | function | `tests/test_hunt_verify.py:29` | `def _event(ref, fields, kind, path)` |
| `test_caps_enforced` | function | `tests/test_hunt_verify.py:118` | `def test_caps_enforced()` |
| `test_dependency_gating_notes_unproven_chain` | function | `tests/test_hunt_verify.py:91` | `def test_dependency_gating_notes_unproven_chain()` |
| `test_field_present_helper` | function | `tests/test_hunt_verify.py:126` | `def test_field_present_helper()` |
| `test_inferred_requires_alternatives` | function | `tests/test_hunt_verify.py:78` | `def test_inferred_requires_alternatives()` |
| `test_known_self_refs_separated` | function | `tests/test_hunt_verify.py:100` | `def test_known_self_refs_separated()` |
| `test_missing_fields_block_observed` | function | `tests/test_hunt_verify.py:43` | `def test_missing_fields_block_observed()` |
| `test_not_observed_requires_scope_covered` | function | `tests/test_hunt_verify.py:60` | `def test_not_observed_requires_scope_covered()` |
| `test_observed_verdict_requires_fields` | function | `tests/test_hunt_verify.py:33` | `def test_observed_verdict_requires_fields()` |
| `test_out_of_scope_ref_rejected` | function | `tests/test_hunt_verify.py:52` | `def test_out_of_scope_ref_rejected()` |
| `test_stage_filters_exclude_events` | function | `tests/test_hunt_verify.py:70` | `def test_stage_filters_exclude_events()` |
| `test_validate_specs_checks_dependencies` | function | `tests/test_hunt_verify.py:109` | `def test_validate_specs_checks_dependencies()` |
| `ImplantSessionSecretsSpec` | class | `tests/test_implant_session_secrets.py:22` | `class ImplantSessionSecretsSpec(TestCase)` |
| `test_implant_binds_sleep_and_persistence_placeholders` | method | `tests/test_implant_session_secrets.py:25` | `def test_implant_binds_sleep_and_persistence_placeholders(self)` |
| `test_implant_uses_obfuscated_sleep_and_jitter_bounds` | method | `tests/test_implant_session_secrets.py:30` | `def test_implant_uses_obfuscated_sleep_and_jitter_bounds(self)` |
| `test_implant_uses_utls_for_real_tls_fingerprint` | method | `tests/test_implant_session_secrets.py:38` | `def test_implant_uses_utls_for_real_tls_fingerprint(self)` |
| `test_listener_and_monrevlin_bind_session_magic` | method | `tests/test_implant_session_secrets.py:45` | `def test_listener_and_monrevlin_bind_session_magic(self)` |
| `test_lkm_makefile_carries_deployment_values` | method | `tests/test_implant_session_secrets.py:57` | `def test_lkm_makefile_carries_deployment_values(self)` |
| `test_rootkit_listener_default_is_neutral` | method | `tests/test_implant_session_secrets.py:53` | `def test_rootkit_listener_default_is_neutral(self)` |
| `test_url_traffic_template_keys_match_builder_context` | method | `tests/test_implant_session_secrets.py:64` | `def test_url_traffic_template_keys_match_builder_context(self)` |
| `BackendAdapterSpec` | class | `tests/test_improvements_spec.py:550` | `class BackendAdapterSpec(TestCase)` |
| `BackendRegistrySpec` | class | `tests/test_improvements_spec.py:444` | `class BackendRegistrySpec(TestCase)` |
| `CmdIntegrationRegressionSpec` | class | `tests/test_improvements_spec.py:767` | `class CmdIntegrationRegressionSpec(TestCase)` |
| `CommandSetActivationSpec` | class | `tests/test_improvements_spec.py:673` | `class CommandSetActivationSpec(TestCase)` |
| `ConfigDedupeSpec` | class | `tests/test_improvements_spec.py:649` | `class ConfigDedupeSpec(TestCase)` |
| `DocstringDisciplineSpec` | class | `tests/test_improvements_spec.py:706` | `class DocstringDisciplineSpec(TestCase)` |
| `EventBusSpec` | class | `tests/test_improvements_spec.py:518` | `class EventBusSpec(TestCase)` |
| `FactoryWiringSpec` | class | `tests/test_improvements_spec.py:996` | `class FactoryWiringSpec(TestCase)` |
| `GraphifyAvailabilitySpec` | class | `tests/test_improvements_spec.py:745` | `class GraphifyAvailabilitySpec(TestCase)` |
| `LiveShellBehaviourSpec` | class | `tests/test_improvements_spec.py:844` | `class LiveShellBehaviourSpec(TestCase)` |
| `OrchestratorGoalValidationSpec` | class | `tests/test_improvements_spec.py:404` | `class OrchestratorGoalValidationSpec(TestCase)` |
| `RouterPolicySpec` | class | `tests/test_improvements_spec.py:477` | `class RouterPolicySpec(TestCase)` |
| `StatusBarConfigSpec` | class | `tests/test_improvements_spec.py:183` | `class StatusBarConfigSpec(TestCase)` |
| `StatusBarFactorySpec` | class | `tests/test_improvements_spec.py:395` | `class StatusBarFactorySpec(TestCase)` |
| `StatusBarManagerSpec` | class | `tests/test_improvements_spec.py:278` | `class StatusBarManagerSpec(TestCase)` |
| `StatusBarRendererSpec` | class | `tests/test_improvements_spec.py:239` | `class StatusBarRendererSpec(TestCase)` |
| `StatusBarSecuritySpec` | class | `tests/test_improvements_spec.py:205` | `class StatusBarSecuritySpec(TestCase)` |
| `StatusBarSourceSpec` | class | `tests/test_improvements_spec.py:350` | `class StatusBarSourceSpec(TestCase)` |
| `UnifiedOrchestratorSpec` | class | `tests/test_improvements_spec.py:601` | `class UnifiedOrchestratorSpec(TestCase)` |
| `_Boom` | class | `tests/test_improvements_spec.py:591` | `class _Boom` |
| `_Broken` | class | `tests/test_improvements_spec.py:289` | `class _Broken` |
| `_Broken` | class | `tests/test_improvements_spec.py:387` | `class _Broken` |
| `_Engine` | class | `tests/test_improvements_spec.py:934` | `class _Engine` |
| `_FakeAdvisor` | class | `tests/test_improvements_spec.py:134` | `class _FakeAdvisor` |
| `_FakeEngagement` | class | `tests/test_improvements_spec.py:90` | `class _FakeEngagement` |
| `_FakeQueen` | class | `tests/test_improvements_spec.py:98` | `class _FakeQueen` |
| `_FakeShell` | class | `tests/test_improvements_spec.py:77` | `class _FakeShell` |
| `_FakeSwanOrchestrator` | class | `tests/test_improvements_spec.py:126` | `class _FakeSwanOrchestrator` |
| `_FakeSwanResult` | class | `tests/test_improvements_spec.py:117` | `class _FakeSwanResult` |
| `_Shell` | class | `tests/test_improvements_spec.py:786` | `class _Shell(Cmd)` |
| `_Shell` | class | `tests/test_improvements_spec.py:798` | `class _Shell(Cmd)` |
| `_Shell` | class | `tests/test_improvements_spec.py:823` | `class _Shell(Cmd)` |
| `_Static` | class | `tests/test_improvements_spec.py:308` | `class _Static` |
| `_Static` | class | `tests/test_improvements_spec.py:329` | `class _Static` |
| `_UnavailableBackend` | class | `tests/test_improvements_spec.py:172` | `class _UnavailableBackend` |
| `_Unnamed` | class | `tests/test_improvements_spec.py:453` | `class _Unnamed` |
| `__init__` | method | `tests/test_improvements_spec.py:80` | `def __init__(self, custom_prompt)` |
| `__init__` | method | `tests/test_improvements_spec.py:91` | `def __init__(self, payload)` |
| `__init__` | method | `tests/test_improvements_spec.py:99` | `def __init__(self, drones, summary)` |
| `__init__` | method | `tests/test_improvements_spec.py:118` | `def __init__(self, text, expert_id)` |
| `__init__` | method | `tests/test_improvements_spec.py:127` | `def __init__(self, result)` |
| `__init__` | method | `tests/test_improvements_spec.py:135` | `def __init__(self, suggestions)` |
| `__init__` | method | `tests/test_improvements_spec.py:173` | `def __init__(self, name)` |
| `__init__` | method | `tests/test_improvements_spec.py:309` | `def __init__(self, value)` |
| `__init__` | method | `tests/test_improvements_spec.py:330` | `def __init__(self, value)` |
| `_build_test_orchestrator` | function | `tests/test_improvements_spec.py:142` | `def _build_test_orchestrator(tmp_root, daemon_available, hive_available, swan_available, daemon_payload)` |
| `_discover` | method | `tests/test_improvements_spec.py:683` | `def _discover(self)` |
| `_events` | method | `tests/test_improvements_spec.py:611` | `def _events(self)` |
| `_goal` | method | `tests/test_improvements_spec.py:561` | `def _goal(self)` |
| `_make_engine` | function | `tests/test_improvements_spec.py:154` | `def _make_engine(goal)` |
| `_reader` | method | `tests/test_improvements_spec.py:216` | `def _reader(self)` |
| `available` | method | `tests/test_improvements_spec.py:176` | `def available(self)` |
| `available` | method | `tests/test_improvements_spec.py:456` | `def available(self)` |
| `broken` | function | `tests/test_improvements_spec.py:899` | `def broken()` |
| `collect` | method | `tests/test_improvements_spec.py:110` | `def collect(self, ids)` |
| `collect` | method | `tests/test_improvements_spec.py:290` | `def collect(self)` |
| `collect` | method | `tests/test_improvements_spec.py:312` | `def collect(self)` |
| `collect` | method | `tests/test_improvements_spec.py:333` | `def collect(self)` |
| `contains_emoji` | function | `tests/test_improvements_spec.py:730` | `def contains_emoji(text)` |
| `dispatch` | method | `tests/test_improvements_spec.py:107` | `def dispatch(self, tasks)` |
| `factory` | function | `tests/test_improvements_spec.py:931` | `def factory(goal)` |
| `fake_hints` | function | `tests/test_improvements_spec.py:878` | `def fake_hints(last_cmd, phase, sessions_dir, limit)` |
| `plan` | method | `tests/test_improvements_spec.py:103` | `def plan(self, goal, n_drones)` |
| `register_precmd_hook` | method | `tests/test_improvements_spec.py:86` | `def register_precmd_hook(self, hook)` |
| `run` | method | `tests/test_improvements_spec.py:94` | `def run(self)` |
| `run` | method | `tests/test_improvements_spec.py:130` | `def run(self, task_type, goal, engagement_phase, timeout)` |
| `run` | method | `tests/test_improvements_spec.py:179` | `def run(self, goal)` |
| `run` | method | `tests/test_improvements_spec.py:459` | `def run(self, goal)` |
| `run` | method | `tests/test_improvements_spec.py:592` | `def run(self)` |
| `run` | method | `tests/test_improvements_spec.py:935` | `def run(self_inner)` |
| `setUp` | method | `tests/test_improvements_spec.py:208` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:242` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:353` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:407` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:480` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:521` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:553` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:604` | `def setUp(self)` |
| `suggest_next` | method | `tests/test_improvements_spec.py:138` | `def suggest_next(self, recent_commands, limit)` |
| `suggest_next` | method | `tests/test_improvements_spec.py:388` | `def suggest_next(self)` |
| `synthesize` | method | `tests/test_improvements_spec.py:113` | `def synthesize(self, results)` |
| `tearDown` | method | `tests/test_improvements_spec.py:213` | `def tearDown(self)` |
| `tearDown` | method | `tests/test_improvements_spec.py:359` | `def tearDown(self)` |
| `tearDown` | method | `tests/test_improvements_spec.py:527` | `def tearDown(self)` |
| `tearDown` | method | `tests/test_improvements_spec.py:558` | `def tearDown(self)` |
| `tearDown` | method | `tests/test_improvements_spec.py:608` | `def tearDown(self)` |
| `test_auto_picks_daemon_when_target_present` | method | `tests/test_improvements_spec.py:496` | `def test_auto_picks_daemon_when_target_present(self)` |
| `test_auto_picks_hive_on_swarm_keyword` | method | `tests/test_improvements_spec.py:500` | `def test_auto_picks_hive_on_swarm_keyword(self)` |
| `test_auto_picks_swan_on_exploit_keyword` | method | `tests/test_improvements_spec.py:504` | `def test_auto_picks_swan_on_exploit_keyword(self)` |
| `test_auto_routes_with_target_to_daemon` | method | `tests/test_improvements_spec.py:628` | `def test_auto_routes_with_target_to_daemon(self)` |
| `test_backend_returns_error_when_engine_raises` | method | `tests/test_improvements_spec.py:590` | `def test_backend_returns_error_when_engine_raises(self)` |
| `test_build_default_manager_does_not_touch_filesystem` | method | `tests/test_improvements_spec.py:1003` | `def test_build_default_manager_does_not_touch_filesystem(self)` |
| `test_build_default_orchestrator_registers_three_backends` | method | `tests/test_improvements_spec.py:999` | `def test_build_default_orchestrator_registers_three_backends(self)` |
| `test_collect_context_uses_fallbacks_on_failure` | method | `tests/test_improvements_spec.py:286` | `def test_collect_context_uses_fallbacks_on_failure(self)` |
| `test_command_hint_source_falls_back_when_provider_raises` | method | `tests/test_improvements_spec.py:892` | `def test_command_hint_source_falls_back_when_provider_raises(self)` |
| `test_command_hint_source_returns_kill_chain_verb` | method | `tests/test_improvements_spec.py:866` | `def test_command_hint_source_returns_kill_chain_verb(self)` |
| `test_command_hints_helper_returns_phase_priority_verbs` | method | `tests/test_improvements_spec.py:913` | `def test_command_hints_helper_returns_phase_priority_verbs(self)` |
| `test_command_set_resolves_shell_via_cmd_property` | method | `tests/test_improvements_spec.py:781` | `def test_command_set_resolves_shell_via_cmd_property(self)` |
| `test_config_ignores_invalid_overrides` | method | `tests/test_improvements_spec.py:200` | `def test_config_ignores_invalid_overrides(self)` |
| `test_config_is_immutable_dataclass` | method | `tests/test_improvements_spec.py:190` | `def test_config_is_immutable_dataclass(self)` |
| `test_config_overrides_from_payload` | method | `tests/test_improvements_spec.py:196` | `def test_config_overrides_from_payload(self)` |
| `test_core_config_is_canonical` | method | `tests/test_improvements_spec.py:664` | `def test_core_config_is_canonical(self)` |
| `test_daemon_falls_back_to_payload_rhost` | method | `tests/test_improvements_spec.py:921` | `def test_daemon_falls_back_to_payload_rhost(self)` |
| `test_daemon_normalises_dict_result` | method | `tests/test_improvements_spec.py:570` | `def test_daemon_normalises_dict_result(self)` |
| `test_daemon_requires_target` | method | `tests/test_improvements_spec.py:565` | `def test_daemon_requires_target(self)` |
| `test_default_prompt_join_is_newline` | method | `tests/test_improvements_spec.py:861` | `def test_default_prompt_join_is_newline(self)` |
| `test_defaults_are_applied` | method | `tests/test_improvements_spec.py:424` | `def test_defaults_are_applied(self)` |
| `test_duplicate_name_raises` | method | `tests/test_improvements_spec.py:447` | `def test_duplicate_name_raises(self)` |
| `test_emit_appends_jsonline` | method | `tests/test_improvements_spec.py:530` | `def test_emit_appends_jsonline(self)` |
| `test_emit_rejects_non_serialisable` | method | `tests/test_improvements_spec.py:541` | `def test_emit_rejects_non_serialisable(self)` |
| `test_emit_rejects_oversize_event` | method | `tests/test_improvements_spec.py:537` | `def test_emit_rejects_oversize_event(self)` |
| `test_empty_goal_is_rejected` | method | `tests/test_improvements_spec.py:411` | `def test_empty_goal_is_rejected(self)` |
| `test_empty_name_raises` | method | `tests/test_improvements_spec.py:452` | `def test_empty_name_raises(self)` |
| `test_enabled_flag_accepts_strings_and_bools` | method | `tests/test_improvements_spec.py:304` | `def test_enabled_flag_accepts_strings_and_bools(self)` |
| `test_event_is_emitted_per_execution` | method | `tests/test_improvements_spec.py:634` | `def test_event_is_emitted_per_execution(self)` |
| `test_every_class_in_new_modules_has_docstring` | method | `tests/test_improvements_spec.py:709` | `def test_every_class_in_new_modules_has_docstring(self)` |
| `test_explicit_mode_overrides_router` | method | `tests/test_improvements_spec.py:492` | `def test_explicit_mode_overrides_router(self)` |
| `test_factory_returns_manager_with_four_sources` | method | `tests/test_improvements_spec.py:398` | `def test_factory_returns_manager_with_four_sources(self)` |
| `test_file_permissions_are_restrictive` | method | `tests/test_improvements_spec.py:544` | `def test_file_permissions_are_restrictive(self)` |
| `test_finding_prefers_credentials_over_notes` | method | `tests/test_improvements_spec.py:375` | `def test_finding_prefers_credentials_over_notes(self)` |
| `test_graph_file_is_valid_json_when_present` | method | `tests/test_improvements_spec.py:758` | `def test_graph_file_is_valid_json_when_present(self)` |
| `test_hive_runs_full_lifecycle` | method | `tests/test_improvements_spec.py:577` | `def test_hive_runs_full_lifecycle(self)` |
| `test_install_registers_precmd_hook` | method | `tests/test_improvements_spec.py:325` | `def test_install_registers_precmd_hook(self)` |
| `test_long_goal_is_bounded` | method | `tests/test_improvements_spec.py:419` | `def test_long_goal_is_bounded(self)` |
| `test_metadata_carries_request_id` | method | `tests/test_improvements_spec.py:438` | `def test_metadata_carries_request_id(self)` |
| `test_missing_source_key_raises` | method | `tests/test_improvements_spec.py:281` | `def test_missing_source_key_raises(self)` |
| `test_modules_avoid_emoji_in_source` | method | `tests/test_improvements_spec.py:724` | `def test_modules_avoid_emoji_in_source(self)` |
| `test_numeric_fields_stay_zero_when_unset` | method | `tests/test_improvements_spec.py:433` | `def test_numeric_fields_stay_zero_when_unset(self)` |
| `test_orchestration_commandset_finds_managers_on_bound_shell` | method | `tests/test_improvements_spec.py:818` | `def test_orchestration_commandset_finds_managers_on_bound_shell(self)` |
| `test_orchestration_set_exposes_required_verbs` | method | `tests/test_improvements_spec.py:697` | `def test_orchestration_set_exposes_required_verbs(self)` |
| `test_orchestration_set_is_active` | method | `tests/test_improvements_spec.py:691` | `def test_orchestration_set_is_active(self)` |
| `test_orchestration_set_phase_and_category_set` | method | `tests/test_improvements_spec.py:701` | `def test_orchestration_set_phase_and_category_set(self)` |
| `test_order_is_preserved` | method | `tests/test_improvements_spec.py:465` | `def test_order_is_preserved(self)` |
| `test_payload_target_falls_back_to_default` | method | `tests/test_improvements_spec.py:366` | `def test_payload_target_falls_back_to_default(self)` |
| `test_payload_target_picks_first_non_empty_key` | method | `tests/test_improvements_spec.py:362` | `def test_payload_target_picks_first_non_empty_key(self)` |
| `test_phase_prefers_world_model_over_payload` | method | `tests/test_improvements_spec.py:370` | `def test_phase_prefers_world_model_over_payload(self)` |
| `test_reader_bounds_file_size` | method | `tests/test_improvements_spec.py:225` | `def test_reader_bounds_file_size(self)` |
| `test_reader_invalid_json_returns_none` | method | `tests/test_improvements_spec.py:234` | `def test_reader_invalid_json_returns_none(self)` |
| `test_reader_rejects_absolute_paths` | method | `tests/test_improvements_spec.py:222` | `def test_reader_rejects_absolute_paths(self)` |
| `test_reader_rejects_parent_traversal` | method | `tests/test_improvements_spec.py:219` | `def test_reader_rejects_parent_traversal(self)` |
| `test_reader_returns_empty_on_missing_file` | method | `tests/test_improvements_spec.py:231` | `def test_reader_returns_empty_on_missing_file(self)` |
| `test_render_plain_contains_all_fields` | method | `tests/test_improvements_spec.py:246` | `def test_render_plain_contains_all_fields(self)` |
| `test_render_prompt_defaults_to_raw_ansi_for_prompt_toolkit` | method | `tests/test_improvements_spec.py:263` | `def test_render_prompt_defaults_to_raw_ansi_for_prompt_toolkit(self)` |
| `test_render_prompt_opt_in_readline_mode_wraps_ansi_with_markers` | method | `tests/test_improvements_spec.py:270` | `def test_render_prompt_opt_in_readline_mode_wraps_ansi_with_markers(self)` |
| `test_render_strips_dangerous_substrings` | method | `tests/test_improvements_spec.py:258` | `def test_render_strips_dangerous_substrings(self)` |
| `test_render_truncates_to_max_chars` | method | `tests/test_improvements_spec.py:252` | `def test_render_truncates_to_max_chars(self)` |
| `test_result_to_dict_is_json_serialisable` | method | `tests/test_improvements_spec.py:642` | `def test_result_to_dict_is_json_serialisable(self)` |
| `test_router_ignores_unset_task_type_for_keyword_scoring` | method | `tests/test_improvements_spec.py:970` | `def test_router_ignores_unset_task_type_for_keyword_scoring(self)` |
| `test_router_picks_daemon_when_only_payload_supplies_target` | method | `tests/test_improvements_spec.py:946` | `def test_router_picks_daemon_when_only_payload_supplies_target(self)` |
| `test_status_bar_install_registers_precmd_hook_on_real_cmd2` | method | `tests/test_improvements_spec.py:795` | `def test_status_bar_install_registers_precmd_hook_on_real_cmd2(self)` |
| `test_suggestion_fallback_when_factory_none` | method | `tests/test_improvements_spec.py:752` | `def test_suggestion_fallback_when_factory_none(self)` |
| `test_suggestion_falls_back_when_advisor_raises` | method | `tests/test_improvements_spec.py:386` | `def test_suggestion_falls_back_when_advisor_raises(self)` |
| `test_suggestion_uses_advisor_when_available` | method | `tests/test_improvements_spec.py:381` | `def test_suggestion_uses_advisor_when_available(self)` |
| `test_swan_normalises_result_object` | method | `tests/test_improvements_spec.py:584` | `def test_swan_normalises_result_object(self)` |
| `test_task_type_stays_empty_when_unset` | method | `tests/test_improvements_spec.py:429` | `def test_task_type_stays_empty_when_unset(self)` |
| `test_unavailable_backend_returns_unavailable_result` | method | `tests/test_improvements_spec.py:623` | `def test_unavailable_backend_returns_unavailable_result(self)` |
| `test_unavailable_explicit_mode_returns_none` | method | `tests/test_improvements_spec.py:508` | `def test_unavailable_explicit_mode_returns_none(self)` |
| `test_unknown_mode_is_rejected` | method | `tests/test_improvements_spec.py:415` | `def test_unknown_mode_is_rejected(self)` |
| `test_utils_has_no_class_config` | method | `tests/test_improvements_spec.py:658` | `def test_utils_has_no_class_config(self)` |
| `test_validation_error_returns_invalid_result` | method | `tests/test_improvements_spec.py:617` | `def test_validation_error_returns_invalid_result(self)` |
| `test_c2_compose_terminates_tls` | function | `tests/test_infra_disposable.py:111` | `def test_c2_compose_terminates_tls()` |
| `test_compile_commands_route_through_shell` | function | `tests/test_infra_disposable.py:228` | `def test_compile_commands_route_through_shell()` |
| `test_compose_down_missing_file` | function | `tests/test_infra_disposable.py:373` | `def test_compose_down_missing_file()` |
| `test_find_cloudflared_pids` | function | `tests/test_infra_disposable.py:357` | `def test_find_cloudflared_pids()` |
| `test_format_timeline_event_summarizes_payload` | function | `tests/test_infra_disposable.py:279` | `def test_format_timeline_event_summarizes_payload()` |
| `test_garble_mismatch_detected` | function | `tests/test_infra_disposable.py:258` | `def test_garble_mismatch_detected()` |
| `test_go_string_list_formats_slice` | function | `tests/test_infra_disposable.py:60` | `def test_go_string_list_formats_slice()` |
| `test_gym_range_challenges_registered` | function | `tests/test_infra_disposable.py:161` | `def test_gym_range_challenges_registered()` |
| `test_gym_range_next_steps` | function | `tests/test_infra_disposable.py:344` | `def test_gym_range_next_steps(tmp_path, monkeypatch)` |
| `test_implant_template_has_fallback_helpers` | function | `tests/test_infra_disposable.py:86` | `def test_implant_template_has_fallback_helpers()` |
| `test_infra_phases_as_c2` | function | `tests/test_infra_disposable.py:52` | `def test_infra_phases_as_c2()` |
| `test_lab_range_profiles_registered` | function | `tests/test_infra_disposable.py:170` | `def test_lab_range_profiles_registered()` |
| `test_mitre_matrix_keeps_unknown_tactics` | function | `tests/test_infra_disposable.py:298` | `def test_mitre_matrix_keeps_unknown_tactics()` |
| `test_parse_go_version_triples` | function | `tests/test_infra_disposable.py:217` | `def test_parse_go_version_triples()` |
| `test_parse_tunnel_urls_dedupes` | function | `tests/test_infra_disposable.py:16` | `def test_parse_tunnel_urls_dedupes()` |
| `test_parse_tunnel_urls_empty` | function | `tests/test_infra_disposable.py:31` | `def test_parse_tunnel_urls_empty()` |
| `test_parse_tunnel_urls_rejects_non_cloudflare` | function | `tests/test_infra_disposable.py:38` | `def test_parse_tunnel_urls_rejects_non_cloudflare()` |
| `test_payload_schema_has_fallback_slot` | function | `tests/test_infra_disposable.py:380` | `def test_payload_schema_has_fallback_slot()` |
| `test_range_backdoor_shell_published` | function | `tests/test_infra_disposable.py:309` | `def test_range_backdoor_shell_published()` |
| `test_range_compose_uses_valid_images` | function | `tests/test_infra_disposable.py:179` | `def test_range_compose_uses_valid_images()` |
| `test_range_dc_secret_wired` | function | `tests/test_infra_disposable.py:198` | `def test_range_dc_secret_wired()` |
| `test_range_secret_generator_roundtrip` | function | `tests/test_infra_disposable.py:207` | `def test_range_secret_generator_roundtrip(tmp_path)` |
| `test_range_verify_confirms_root` | function | `tests/test_infra_disposable.py:318` | `def test_range_verify_confirms_root(capsys)` |
| `test_range_verify_unknown_profile` | function | `tests/test_infra_disposable.py:336` | `def test_range_verify_unknown_profile(capsys)` |
| `test_range_workstation_stays_alive` | function | `tests/test_infra_disposable.py:189` | `def test_range_workstation_stays_alive()` |
| `test_redirector_caddy_filters_paths` | function | `tests/test_infra_disposable.py:95` | `def test_redirector_caddy_filters_paths()` |
| `test_redirector_compose_routes_to_caddy` | function | `tests/test_infra_disposable.py:103` | `def test_redirector_compose_routes_to_caddy()` |
| `test_redirector_stale_threshold` | function | `tests/test_infra_disposable.py:272` | `def test_redirector_stale_threshold()` |
| `test_report_ai_failure_falls_back_to_template` | function | `tests/test_infra_disposable.py:150` | `def test_report_ai_failure_falls_back_to_template()` |
| `test_report_collects_history_and_loot` | function | `tests/test_infra_disposable.py:125` | `def test_report_collects_history_and_loot()` |
| `test_report_template_summary_mentions_remediation_windows` | function | `tests/test_infra_disposable.py:137` | `def test_report_template_summary_mentions_remediation_windows()` |
| `test_resolve_fallback_urls_param_list` | function | `tests/test_infra_disposable.py:78` | `def test_resolve_fallback_urls_param_list()` |
| `test_resolve_fallback_urls_param_string` | function | `tests/test_infra_disposable.py:70` | `def test_resolve_fallback_urls_param_string()` |
| `test_terraform_firewall_restricts_c2_port` | function | `tests/test_infra_disposable.py:118` | `def test_terraform_firewall_restricts_c2_port()` |
| `test_valid_providers_exact_allowlist` | function | `tests/test_infra_disposable.py:45` | `def test_valid_providers_exact_allowlist()` |
| `_host_inputs` | function | `tests/test_input_fuzz.py:85` | `def _host_inputs()` |
| `_port_inputs` | function | `tests/test_input_fuzz.py:93` | `def _port_inputs()` |
| `_random_host` | function | `tests/test_input_fuzz.py:80` | `def _random_host(rng)` |
| `test_accepted_hosts_have_no_shell_metacharacters` | function | `tests/test_input_fuzz.py:110` | `def test_accepted_hosts_have_no_shell_metacharacters(value, capsys)` |
| `test_host_validators_never_raise` | function | `tests/test_input_fuzz.py:103` | `def test_host_validators_never_raise(value, capsys)` |
| `test_known_good_values_accepted` | function | `tests/test_input_fuzz.py:126` | `def test_known_good_values_accepted(capsys)` |
| `test_port_validator_never_raise_and_bounded` | function | `tests/test_input_fuzz.py:118` | `def test_port_validator_never_raise_and_bounded(value, capsys)` |

Next: [SYMBOLS_p39.md](SYMBOLS_p39.md)
