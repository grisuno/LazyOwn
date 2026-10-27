# Subsystem: tests (page 10 of 21)
Previous: [KB_tests_p9.md](KB_tests_p9.md)

## tests/test_graph_advisor.py
- Doc: Tests for cli/graph_advisor.py.
- Layer: testing
- Language: py
- Symbols:
  - `small_graph_data` (function, line 34) `def small_graph_data()`
  - `small_graph_path` (function, line 126) `def small_graph_path(tmp_path, small_graph_data)`
  - `advisor` (function, line 133) `def advisor(small_graph_path)`
  - `test_loader_resolves_explicit_path` (function, line 138) `def test_loader_resolves_explicit_path(tmp_path, small_graph_data)`
  - `test_loader_returns_none_when_missing` (function, line 147) `def test_loader_returns_none_when_missing(tmp_path)`
  - `test_index_builds_adjacency_and_degree` (function, line 153) `def test_index_builds_adjacency_and_degree(small_graph_data)`
  - `test_scorer_prefers_prefix_match` (function, line 174) `def test_scorer_prefers_prefix_match(small_graph_data)`
  - `test_scorer_returns_empty_for_unrelated_query` (function, line 182) `def test_scorer_returns_empty_for_unrelated_query(small_graph_data)`
  - `test_advisor_summary_reports_topology` (function, line 188) `def test_advisor_summary_reports_topology(advisor)`
  - `test_advisor_summary_flags_empty_graph` (function, line 199) `def test_advisor_summary_flags_empty_graph(tmp_path)`
  - `test_advisor_summary_flags_stale_graph` (function, line 212) `def test_advisor_summary_flags_stale_graph(tmp_path)`
  - `test_advisor_search_returns_ranked_nodes` (function, line 231) `def test_advisor_search_returns_ranked_nodes(advisor)`
  - `test_advisor_neighbors_returns_layered_walk` (function, line 239) `def test_advisor_neighbors_returns_layered_walk(advisor)`
  - `test_advisor_neighbors_respects_depth` (function, line 248) `def test_advisor_neighbors_respects_depth(advisor)`
  - `test_advisor_god_nodes_ranks_by_degree` (function, line 254) `def test_advisor_god_nodes_ranks_by_degree(advisor)`
  - `test_advisor_suggest_next_walks_from_recent` (function, line 260) `def test_advisor_suggest_next_walks_from_recent(advisor)`
  - `test_advisor_did_you_mean_returns_close_labels` (function, line 268) `def test_advisor_did_you_mean_returns_close_labels(advisor)`
  - `test_advisor_truncate_respects_token_budget` (function, line 274) `def test_advisor_truncate_respects_token_budget(advisor)`
  - `test_advisor_handles_missing_graph_gracefully` (function, line 280) `def test_advisor_handles_missing_graph_gracefully(tmp_path)`
  - `test_advisor_reads_recent_commands_from_csv` (function, line 292) `def test_advisor_reads_recent_commands_from_csv(tmp_path, advisor)`
  - `test_format_search_table_renders_rows` (function, line 309) `def test_format_search_table_renders_rows(advisor)`
  - `test_format_neighbors_renders_when_match_found` (function, line 316) `def test_format_neighbors_renders_when_match_found(advisor)`
  - `test_format_god_nodes_handles_empty` (function, line 322) `def test_format_god_nodes_handles_empty()`
  - `test_format_suggestions_handles_empty` (function, line 326) `def test_format_suggestions_handles_empty()`
  - `test_real_graph_summary_when_available` (function, line 333) `def test_real_graph_summary_when_available()`
- Depends on: `cli/graph_advisor.py`

## tests/test_graph_overlay.py
- Doc: Tests for cli/graph_overlay.py.
- Layer: testing
- Language: py
- Symbols:
  - `_FakeAdvisor` (class, line 25) `class _FakeAdvisor`
  - `test_is_available_returns_false_when_advisor_missing` (function, line 55) `def test_is_available_returns_false_when_advisor_missing()`
  - `test_god_nodes_view_returns_hubs` (function, line 61) `def test_god_nodes_view_returns_hubs()`
  - `test_focus_switches_to_neighbors_view` (function, line 72) `def test_focus_switches_to_neighbors_view()`
  - `test_focus_unknown_returns_no_match_message` (function, line 85) `def test_focus_unknown_returns_no_match_message()`
  - `test_unavailable_advisor_returns_no_graph_message` (function, line 97) `def test_unavailable_advisor_returns_no_graph_message()`
  - `test_toggle_view_round_trip` (function, line 108) `def test_toggle_view_round_trip()`
  - `test_launch_overlay_uses_runner` (function, line 122) `def test_launch_overlay_uses_runner()`
  - `test_build_state_uses_default_factory_signature` (function, line 135) `def test_build_state_uses_default_factory_signature()`
  - `__init__` (method, line 26) `def __init__(self, available)`
  - `is_available` (method, line 29) `def is_available(self)`
  - `god_nodes` (method, line 32) `def god_nodes(self, limit)`
  - `neighbors` (method, line 39) `def neighbors(self, query, depth, limit)`
  - `runner` (function, line 129) `def runner(context)`
- Depends on: `cli/graph_overlay.py`

## tests/test_guardrails.py
- Doc: Guardrail harness tests: tiers, capacity, warm restart, wiring.
- Layer: testing
- Language: py
- Symbols:
  - `TestTaskClass` (class, line 26) `class TestTaskClass`
  - `TestCapacityEnvelope` (class, line 36) `class TestCapacityEnvelope`
  - `TestCheckpointLedger` (class, line 83) `class TestCheckpointLedger`
  - `TestAdvisoriesAndFeatures` (class, line 116) `class TestAdvisoriesAndFeatures`
  - `TestGuardHarness` (class, line 144) `class TestGuardHarness`
  - `TestGlobalHarness` (class, line 229) `class TestGlobalHarness`
  - `TestLazyLoopWiring` (class, line 243) `class TestLazyLoopWiring`
  - `TestAptChainWiring` (class, line 298) `class TestAptChainWiring`
  - `TestOrchestratorHarnessTab` (class, line 344) `class TestOrchestratorHarnessTab`
  - `test_tier_ordering_is_strict` (method, line 27) `def test_tier_ordering_is_strict(self)`
  - `test_is_known_accepts_values_and_rejects_strays` (method, line 30) `def test_is_known_accepts_values_and_rejects_strays(self)`
  - `test_defaults_snapshot` (method, line 37) `def test_defaults_snapshot(self)`
  - `test_admit_and_account_roundtrip` (method, line 43) `def test_admit_and_account_roundtrip(self)`
  - `test_saturated_tier_refuses_admission` (method, line 51) `def test_saturated_tier_refuses_admission(self)`
  - `test_higher_tier_saturation_refuses_lower_tiers` (method, line 58) `def test_higher_tier_saturation_refuses_lower_tiers(self)`
  - `test_reclaim_purges_support_only` (method, line 66) `def test_reclaim_purges_support_only(self)`
  - `test_configure_clamps_and_accepts_names` (method, line 75) `def test_configure_clamps_and_accepts_names(self)`
  - `test_capture_restore_roundtrip` (method, line 84) `def test_capture_restore_roundtrip(self)`
  - `test_history_is_bounded` (method, line 89) `def test_history_is_bounded(self)`
  - `test_restore_missing_is_none` (method, line 96) `def test_restore_missing_is_none(self)`
  - `test_warm_restart_restores_and_counts` (method, line 99) `def test_warm_restart_restores_and_counts(self)`
  - `test_warm_restart_without_key_reports_unrestored` (method, line 107) `def test_warm_restart_without_key_reports_unrestored(self)`
  - `test_capture_rejects_blank_keys` (method, line 112) `def test_capture_rejects_blank_keys(self)`
  - `test_notice_is_bounded_newest_first` (method, line 117) `def test_notice_is_bounded_newest_first(self)`
  - `test_clear_returns_count` (method, line 125) `def test_clear_returns_count(self)`
  - `test_feature_gate_unknown_feature_never_suspends` (method, line 132) `def test_feature_gate_unknown_feature_never_suspends(self)`
  - `test_feature_gate_known_set` (method, line 139) `def test_feature_gate_known_set(self)`
  - `harness` (method, line 146) `def harness(self)`
  - `test_mission_success_accounts_usage` (method, line 149) `def test_mission_success_accounts_usage(self, harness)`
  - `test_mission_failure_degrades_with_advisory` (method, line 153) `def test_mission_failure_degrades_with_advisory(self, harness)`
  - `test_support_refused_while_render_suspended` (method, line 161) `def test_support_refused_while_render_suspended(self, harness)`
  - `test_core_retries_once_after_warm_restart` (method, line 168) `def test_core_retries_once_after_warm_restart(self, harness)`
  - `test_core_gives_up_after_second_failure` (method, line 181) `def test_core_gives_up_after_second_failure(self, harness)`
  - `test_core_without_checkpoint_never_retries` (method, line 189) `def test_core_without_checkpoint_never_retries(self, harness)`
  - `test_keyboard_interrupt_propagates` (method, line 197) `def test_keyboard_interrupt_propagates(self, harness)`
  - `test_priority_reservation_refuses_lower_tiers` (method, line 204) `def test_priority_reservation_refuses_lower_tiers(self, harness)`
  - `test_configure_from_payload_section` (method, line 215) `def test_configure_from_payload_section(self, harness)`
  - `test_warm_restart_purges_support_and_notifies` (method, line 220) `def test_warm_restart_purges_support_and_notifies(self, harness)`
  - `_fresh_global_harness` (method, line 231) `def _fresh_global_harness(self)`
  - `test_singleton_shared` (method, line 236) `def test_singleton_shared(self)`
  - `test_config_section_constant_shape` (method, line 239) `def test_config_section_constant_shape(self)`
  - `_fresh_global_harness` (method, line 245) `def _fresh_global_harness(self)`
  - `test_apply_profile_configures_harness` (method, line 250) `def test_apply_profile_configures_harness(self, tmp_path, monkeypatch)`
  - `test_worker_guard_maps_refusal_to_degraded_outcome` (method, line 266) `def test_worker_guard_maps_refusal_to_degraded_outcome(self, tmp_path, monkeypatch)`
  - `test_round_guard_halt_maps_to_degraded_abort` (method, line 285) `def test_round_guard_halt_maps_to_degraded_abort(self, tmp_path, monkeypatch)`
  - `_fresh_global_harness` (method, line 300) `def _fresh_global_harness(self)`
  - `test_recovery_guard_returns_none_when_refused` (method, line 305) `def test_recovery_guard_returns_none_when_refused(self, monkeypatch)`
  - `sandbox` (method, line 346) `def sandbox(self, tmp_path, monkeypatch)`
  - `test_command_registered` (method, line 353) `def test_command_registered(self)`
  - `test_guardrails_persist_via_payload` (method, line 358) `def test_guardrails_persist_via_payload(self, monkeypatch, sandbox)`
  - `test_harness_tab_composes_headless` (method, line 380) `def test_harness_tab_composes_headless(self, sandbox, monkeypatch)`
  - `boom` (function, line 154) `def boom()`
  - `flaky` (function, line 171) `def flaky()`
  - `always_fails` (function, line 182) `def always_fails()`
  - `boom` (function, line 190) `def boom()`
  - `interrupted` (function, line 198) `def interrupted()`
  - `_load` (function, line 361) `def _load(target)`
  - `_save` (function, line 364) `def _save(data, target)`
  - `_drive` (function, line 385) `def _drive()`
- Depends on: `cli/apt_chain_support.py`, `cli/commands/lazyloop.py`, `cli/lazy_orchestrator.py`, `core/config.py`, `modules/guardrails/__init__.py`, `modules/lazy_loop.py`, `modules/mediation/chain_mediator.py`

## tests/test_gui_xss_sinks.py
- Doc: Regression gate for XSS sinks in the C2 dashboard template.
- Layer: testing
- Language: py
- Symbols:
  - `_read_template` (function, line 21) `def _read_template()`
  - `SafeHtmlHelperTests` (class, line 26) `class SafeHtmlHelperTests(TestCase)`
  - `SinkSanitizationTests` (class, line 37) `class SinkSanitizationTests(TestCase)`
  - `test_helper_is_defined_exactly_once` (method, line 27) `def test_helper_is_defined_exactly_once(self)`
  - `test_helper_prefers_dompurify_with_text_fallback` (method, line 31) `def test_helper_prefers_dompurify_with_text_fallback(self)`
  - `test_no_raw_response_interpolation` (method, line 38) `def test_no_raw_response_interpolation(self)`
  - `test_no_raw_html_interpolation` (method, line 43) `def test_no_raw_html_interpolation(self)`
  - `test_no_raw_error_interpolation` (method, line 50) `def test_no_raw_error_interpolation(self)`
  - `test_no_raw_output_interpolation` (method, line 61) `def test_no_raw_output_interpolation(self)`

## tests/test_gym_cli.py
- Doc: Gym CLI lifecycle: start, status, stop by selector and stop-all.
- Layer: testing
- Language: py
- Symbols:
  - `sandbox` (function, line 11) `def sandbox(tmp_path, monkeypatch)`
  - `test_gym_stop_without_active_is_clean` (function, line 32) `def test_gym_stop_without_active_is_clean(sandbox, capsys)`
  - `test_gym_start_status_stop_lifecycle` (function, line 39) `def test_gym_start_status_stop_lifecycle(sandbox, capsys)`
  - `test_gym_stop_all_and_by_name` (function, line 65) `def test_gym_stop_all_and_by_name(sandbox, capsys)`
  - `test_gym_status_explains_live_shell_without_gym` (function, line 82) `def test_gym_status_explains_live_shell_without_gym(sandbox, monkeypatch, capsys)`
  - `test_gym_top_aliases_leaderboard` (function, line 97) `def test_gym_top_aliases_leaderboard(sandbox, capsys)`
  - `test_gym_status_filters_hosts_by_current_target` (function, line 103) `def test_gym_status_filters_hosts_by_current_target(sandbox, monkeypatch, capsys)`
  - `test_atomic_shell_marks_target_compromised` (function, line 123) `def test_atomic_shell_marks_target_compromised(sandbox, monkeypatch, capsys)`
- Depends on: `cli/commands/command_and_control_migrated.py`, `cli/commands/redteam_gym.py`, `modules/__init__.py`, `modules/atomic_exploit_bridge.py`, `modules/gym_registry.py`, `modules/outcome_bus.py`, `modules/redteam_gym.py`, `modules/world_model.py`

## tests/test_gym_lifecycle.py
- Doc: Gym lifecycle: lab spin-up on start, teardown on stop and exit cleanup.
- Layer: testing
- Language: py
- Symbols:
  - `sandbox` (function, line 20) `def sandbox(tmp_path, monkeypatch)`
  - `_FakeDocker` (class, line 38) `class _FakeDocker`
  - `_result` (class, line 53) `class _result`
  - `test_start_spins_scenario_and_resolves_ip` (function, line 60) `def test_start_spins_scenario_and_resolves_ip(sandbox, monkeypatch)`
  - `test_start_without_lab_flag_still_registers` (function, line 89) `def test_start_without_lab_flag_still_registers(sandbox, monkeypatch)`
  - `test_start_without_docker_degrades_gracefully` (function, line 99) `def test_start_without_docker_degrades_gracefully(sandbox, monkeypatch)`
  - `test_start_removes_stale_container_first` (function, line 107) `def test_start_removes_stale_container_first(sandbox, monkeypatch)`
  - `test_stop_teardowns_scenario_container` (function, line 122) `def test_stop_teardowns_scenario_container(sandbox, monkeypatch)`
  - `test_stop_keeps_scenario_with_active_runs` (function, line 142) `def test_stop_keeps_scenario_with_active_runs(sandbox, monkeypatch)`
  - `test_cleanup_gym_machines_stops_all` (function, line 162) `def test_cleanup_gym_machines_stops_all(tmp_path, monkeypatch, capsys)`
  - `__init__` (method, line 41) `def __init__(self, responses)`
  - `__call__` (method, line 45) `def __call__(self)`
  - `__init__` (method, line 54) `def __init__(self, returncode, stdout, stderr)`
- Depends on: `core/config.py`, `modules/__init__.py`, `modules/gym_cleanup.py`, `modules/outcome_bus.py`, `modules/world_model.py`

## tests/test_gym_matrix_ctf.py
- Doc: Contract tests for gym matrix runner and CTF capture.
- Layer: testing
- Language: py
- Symbols:
  - `CtfCaptureSpec` (class, line 13) `class CtfCaptureSpec(TestCase)`
  - `GymMatrixRunnerSpec` (class, line 62) `class GymMatrixRunnerSpec(TestCase)`
  - `ReportIntegrationSpec` (class, line 120) `class ReportIntegrationSpec(TestCase)`
  - `test_root_shell_capture` (method, line 16) `def test_root_shell_capture(self)`
  - `test_failed_capture_without_evidence` (method, line 29) `def test_failed_capture_without_evidence(self)`
  - `test_unknown_vuln_rejected` (method, line 39) `def test_unknown_vuln_rejected(self)`
  - `test_shadow_evidence_masked` (method, line 44) `def test_shadow_evidence_masked(self)`
  - `test_load_artifact` (method, line 57) `def test_load_artifact(self)`
  - `test_plan_ordered_by_severity` (method, line 65) `def test_plan_ordered_by_severity(self)`
  - `test_plan_isolates_only_filter` (method, line 72) `def test_plan_isolates_only_filter(self)`
  - `test_plan_rejects_empty_target` (method, line 76) `def test_plan_rejects_empty_target(self)`
  - `test_run_matrix_dry_run_writes_no_capture` (method, line 80) `def test_run_matrix_dry_run_writes_no_capture(self)`
  - `test_run_matrix_executes_and_captures` (method, line 91) `def test_run_matrix_executes_and_captures(self)`
  - `test_run_matrix_flags_missing_chain` (method, line 110) `def test_run_matrix_flags_missing_chain(self)`
  - `test_captured_findings_enter_report` (method, line 123) `def test_captured_findings_enter_report(self)`
  - `executor` (function, line 92) `def executor(cmd)`
- Depends on: `modules/__init__.py`, `modules/professional_report.py`

## tests/test_gym_ms2_cli.py
- Layer: testing
- Language: py
- Symbols:
  - `test_gym_ms2_chains_lists_index` (function, line 4) `def test_gym_ms2_chains_lists_index(capsys)`
- Depends on: `cli/commands/redteam_gym.py`

## tests/test_gym_registry.py
- Doc: Gym YAML catalogue and persistent world-model run state.
- Layer: testing
- Language: py
- Symbols:
  - `sandbox` (function, line 14) `def sandbox(tmp_path, monkeypatch)`
  - `_write_definition` (function, line 35) `def _write_definition(directory, gym_id)`
  - `test_shipped_catalogue_loads` (function, line 63) `def test_shipped_catalogue_loads()`
  - `test_definition_crud_is_confined` (function, line 71) `def test_definition_crud_is_confined(sandbox, tmp_path)`
  - `test_start_status_stop_all_persists` (function, line 93) `def test_start_status_stop_all_persists(sandbox)`
  - `test_stop_by_id_and_name` (function, line 116) `def test_stop_by_id_and_name(sandbox)`
  - `test_submit_requires_disambiguation` (function, line 129) `def test_submit_requires_disambiguation(sandbox)`
  - `test_delete_refuses_active_definition` (function, line 145) `def test_delete_refuses_active_definition(sandbox)`
  - `test_legacy_active_files_are_imported_once` (function, line 156) `def test_legacy_active_files_are_imported_once(sandbox, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/outcome_bus.py`, `modules/redteam_gym.py`, `modules/world_model.py`

## tests/test_harness_mode.py
- Doc: Harness deterministic-mode contract tests.
- Layer: testing
- Language: py
- Symbols:
  - `HarnessFlagSpec` (class, line 14) `class HarnessFlagSpec(TestCase)`
  - `HarnessProfileSpec` (class, line 46) `class HarnessProfileSpec(TestCase)`
  - `GateSpec` (class, line 65) `class GateSpec(TestCase)`
  - `ChainDirectiveSpec` (class, line 123) `class ChainDirectiveSpec(TestCase)`
  - `ObjectiveDirectiveSpec` (class, line 144) `class ObjectiveDirectiveSpec(TestCase)`
  - `setUp` (method, line 17) `def setUp(self)`
  - `tearDown` (method, line 20) `def tearDown(self)`
  - `test_env_flag_enables` (method, line 26) `def test_env_flag_enables(self)`
  - `test_env_flag_off_overrides_profile` (method, line 32) `def test_env_flag_off_overrides_profile(self)`
  - `test_payload_section_enables` (method, line 37) `def test_payload_section_enables(self)`
  - `test_payload_section_disables` (method, line 41) `def test_payload_section_disables(self)`
  - `test_profile_present` (method, line 49) `def test_profile_present(self)`
  - `test_profile_flags` (method, line 54) `def test_profile_flags(self)`
  - `_planner_returns_none_without_llm` (method, line 68) `def _planner_returns_none_without_llm(self)`
  - `test_plan_llm_gate_blocked_under_harness` (method, line 79) `def test_plan_llm_gate_blocked_under_harness(self)`
  - `test_worker_agentic_gate_blocked_under_harness` (method, line 84) `def test_worker_agentic_gate_blocked_under_harness(self)`
  - `test_worker_llm_steps_gate_keeps_base_steps` (method, line 104) `def test_worker_llm_steps_gate_keeps_base_steps(self)`
  - `test_known_chain_resolves` (method, line 126) `def test_known_chain_resolves(self)`
  - `test_unknown_chain_rejected` (method, line 132) `def test_unknown_chain_rejected(self)`
  - `test_target_token_fallback` (method, line 137) `def test_target_token_fallback(self)`
  - `test_push_objective_text_carries_directive` (method, line 147) `def test_push_objective_text_carries_directive(self)`
  - `_explode` (function, line 93) `def _explode()`
  - `_llm_steps` (function, line 112) `def _llm_steps(_intent, _prior)`
- Depends on: `modules/__init__.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/orchestrator_config.py`

## tests/test_hash_cracker.py
- Doc: Tests for modules/hash_cracker.py
- Layer: testing
- Language: py
- Symbols:
  - `TestHashIdentification` (class, line 14) `class TestHashIdentification`
  - `TestFileIdentification` (class, line 66) `class TestFileIdentification`
  - `TestCrackResult` (class, line 91) `class TestCrackResult`
  - `TestHashPatterns` (class, line 114) `class TestHashPatterns`
  - `TestWordlists` (class, line 122) `class TestWordlists`
  - `TestHashIdentifier` (class, line 129) `class TestHashIdentifier`
  - `test_identify_ntlm` (method, line 15) `def test_identify_ntlm(self)`
  - `test_identify_ntlm_from_secretsdump` (method, line 22) `def test_identify_ntlm_from_secretsdump(self)`
  - `test_identify_sha512crypt` (method, line 29) `def test_identify_sha512crypt(self)`
  - `test_identify_unknown` (method, line 36) `def test_identify_unknown(self)`
  - `test_identify_empty` (method, line 41) `def test_identify_empty(self)`
  - `test_identify_kerberos_tgs` (method, line 46) `def test_identify_kerberos_tgs(self)`
  - `test_identify_md5` (method, line 53) `def test_identify_md5(self)`
  - `test_identify_sha1` (method, line 59) `def test_identify_sha1(self)`
  - `test_identify_file_empty` (method, line 67) `def test_identify_file_empty(self, tmp_path)`
  - `test_identify_file_with_hashes` (method, line 74) `def test_identify_file_with_hashes(self, tmp_path)`
  - `test_identify_file_not_exists` (method, line 85) `def test_identify_file_not_exists(self)`
  - `test_crack_result_defaults` (method, line 92) `def test_crack_result_defaults(self)`
  - `test_crack_result_cracked` (method, line 102) `def test_crack_result_cracked(self)`
  - `test_all_patterns_exist` (method, line 115) `def test_all_patterns_exist(self)`
  - `test_wordlist_paths_are_strings` (method, line 123) `def test_wordlist_paths_are_strings(self)`
  - `test_hash_identifier_fields` (method, line 130) `def test_hash_identifier_fields(self)`
- Depends on: `modules/hash_cracker.py`

## tests/test_help_ui_command_set.py
- Doc: Help/UI command set extraction tests.
- Layer: testing
- Language: py
- Symbols:
  - `_add_repo_root_to_syspath` (function, line 32) `def _add_repo_root_to_syspath()`
  - `HelpUiSuiteConfig` (class, line 38) `class HelpUiSuiteConfig`
  - `_methods_of` (function, line 65) `def _methods_of(path, class_name)`
  - `test_target_is_active_command_set` (function, line 77) `def test_target_is_active_command_set()`
  - `test_target_exposes_full_help_cluster` (function, line 86) `def test_target_exposes_full_help_cluster()`
  - `test_target_phase_metadata` (function, line 93) `def test_target_phase_metadata()`
  - `test_source_no_longer_defines_cluster` (function, line 99) `def test_source_no_longer_defines_cluster()`
  - `test_registry_registers_target` (function, line 105) `def test_registry_registers_target()`
  - `test_no_command_collisions_with_source` (function, line 112) `def test_no_command_collisions_with_source()`
- Depends on: `cli/commands/_base.py`, `cli/commands/_dormancy.py`, `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/registry.py`

## tests/test_host_policy.py
- Doc: Single host-validation policy shared by CLI gates and hardening.
- Layer: testing
- Language: py
- Symbols:
  - `TestSharedPolicy` (class, line 51) `class TestSharedPolicy`
  - `TestCliGatesDelegate` (class, line 73) `class TestCliGatesDelegate`
  - `test_valid_hosts_accepted` (method, line 52) `def test_valid_hosts_accepted(self)`
  - `test_invalid_hosts_rejected` (method, line 57) `def test_invalid_hosts_rejected(self)`
  - `test_shell_meta_rejected` (method, line 62) `def test_shell_meta_rejected(self)`
  - `test_pinned_quirks_unchanged` (method, line 67) `def test_pinned_quirks_unchanged(self)`
  - `test_check_rhost_matches_policy` (method, line 74) `def test_check_rhost_matches_policy(self, capsys)`
  - `test_check_lhost_matches_policy` (method, line 81) `def test_check_lhost_matches_policy(self, capsys)`
  - `test_check_lport_unchanged` (method, line 88) `def test_check_lport_unchanged(self, capsys)`
- Depends on: `core/hardening.py`, `core/host_policy.py`, `core/validators.py`

## tests/test_html_sanitizer.py
- Doc: TDD tests for the bleach-based HTML sanitizer contract.
- Layer: testing
- Language: py
- Symbols:
  - `TestScriptStripping` (class, line 25) `class TestScriptStripping`
  - `TestEventHandlerStripping` (class, line 49) `class TestEventHandlerStripping`
  - `TestJavascriptUriStripping` (class, line 63) `class TestJavascriptUriStripping`
  - `TestBenignTagsPreserved` (class, line 71) `class TestBenignTagsPreserved`
  - `TestCustomAllowlist` (class, line 93) `class TestCustomAllowlist`
  - `test_script_block_removed` (method, line 28) `def test_script_block_removed(self)`
  - `test_iframe_removed` (method, line 33) `def test_iframe_removed(self)`
  - `test_object_and_embed_removed` (method, line 38) `def test_object_and_embed_removed(self)`
  - `test_style_removed` (method, line 43) `def test_style_removed(self)`
  - `test_onclick_removed` (method, line 52) `def test_onclick_removed(self)`
  - `test_onerror_removed` (method, line 57) `def test_onerror_removed(self)`
  - `test_javascript_href_stripped` (method, line 66) `def test_javascript_href_stripped(self)`
  - `test_basic_formatting_preserved` (method, line 74) `def test_basic_formatting_preserved(self)`
  - `test_lists_preserved` (method, line 81) `def test_lists_preserved(self)`
  - `test_headings_preserved` (method, line 86) `def test_headings_preserved(self)`
  - `test_strict_allowlist_strips_more` (method, line 96) `def test_strict_allowlist_strips_more(self)`
- Depends on: `lazyc2/security/html_sanitizer.py`

## tests/test_https_redirect.py
- Doc: TDD tests for the HTTPS redirect contract.
- Layer: testing
- Language: py
- Symbols:
  - `_FakeRequest` (class, line 23) `class _FakeRequest`
  - `TestHTTPSRedirect` (class, line 34) `class TestHTTPSRedirect`
  - `TestRedirectResponseShape` (class, line 74) `class TestRedirectResponseShape`
  - `__init__` (method, line 24) `def __init__(self, is_secure, host, path, query_string)`
  - `test_secure_request_passes_through` (method, line 37) `def test_secure_request_passes_through(self)`
  - `test_insecure_in_prod_redirects_to_https` (method, line 42) `def test_insecure_in_prod_redirects_to_https(self)`
  - `test_insecure_in_dev_passes_through` (method, line 50) `def test_insecure_in_dev_passes_through(self)`
  - `test_insecure_when_disabled_passes_through` (method, line 55) `def test_insecure_when_disabled_passes_through(self)`
  - `test_query_string_preserved` (method, line 60) `def test_query_string_preserved(self)`
  - `test_root_path_preserved` (method, line 67) `def test_root_path_preserved(self)`
  - `test_response_is_named_tuple_like` (method, line 77) `def test_response_is_named_tuple_like(self)`
- Depends on: `lazyc2/security/https_redirect.py`

## tests/test_hunt_verify.py
- Doc: Hunt verification: verdict taxonomy, scope gate and dependency gating.
- Layer: testing
- Language: py
- Symbols:
  - `_event` (function, line 29) `def _event(ref, fields, kind, path)`
  - `test_observed_verdict_requires_fields` (function, line 33) `def test_observed_verdict_requires_fields()`
  - `test_missing_fields_block_observed` (function, line 43) `def test_missing_fields_block_observed()`
  - `test_out_of_scope_ref_rejected` (function, line 52) `def test_out_of_scope_ref_rejected()`
  - `test_not_observed_requires_scope_covered` (function, line 60) `def test_not_observed_requires_scope_covered()`
  - `test_stage_filters_exclude_events` (function, line 70) `def test_stage_filters_exclude_events()`
  - `test_inferred_requires_alternatives` (function, line 78) `def test_inferred_requires_alternatives()`
  - `test_dependency_gating_notes_unproven_chain` (function, line 91) `def test_dependency_gating_notes_unproven_chain()`
  - `test_known_self_refs_separated` (function, line 100) `def test_known_self_refs_separated()`
  - `test_validate_specs_checks_dependencies` (function, line 109) `def test_validate_specs_checks_dependencies()`
  - `test_caps_enforced` (function, line 118) `def test_caps_enforced()`
  - `test_field_present_helper` (function, line 126) `def test_field_present_helper()`
- Depends on: `modules/hunt_verify.py`

## tests/test_implant_session_secrets.py
- Doc: ImplantSessionSecretsSpec: Contract: lab Go implant templates bind rotating session secrets.
- Layer: testing
- Language: py
- Symbols:
  - `ImplantSessionSecretsSpec` (class, line 22) `class ImplantSessionSecretsSpec(TestCase)`
  - `test_implant_binds_sleep_and_persistence_placeholders` (method, line 25) `def test_implant_binds_sleep_and_persistence_placeholders(self)`
  - `test_implant_uses_obfuscated_sleep_and_jitter_bounds` (method, line 30) `def test_implant_uses_obfuscated_sleep_and_jitter_bounds(self)`
  - `test_implant_uses_utls_for_real_tls_fingerprint` (method, line 38) `def test_implant_uses_utls_for_real_tls_fingerprint(self)`
  - `test_listener_and_monrevlin_bind_session_magic` (method, line 45) `def test_listener_and_monrevlin_bind_session_magic(self)`
  - `test_rootkit_listener_default_is_neutral` (method, line 53) `def test_rootkit_listener_default_is_neutral(self)`
  - `test_lkm_makefile_carries_deployment_values` (method, line 57) `def test_lkm_makefile_carries_deployment_values(self)`
  - `test_url_traffic_template_keys_match_builder_context` (method, line 64) `def test_url_traffic_template_keys_match_builder_context(self)`
- Depends on: `modules/c2_builder.py`


Next: [KB_tests_p11.md](KB_tests_p11.md)
