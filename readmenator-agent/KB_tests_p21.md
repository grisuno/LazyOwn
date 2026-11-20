# Subsystem: tests (page 21 of 28)
Previous: [KB_tests_p20.md](KB_tests_p20.md)

## tests/test_moe_rl_swan.py
- Doc: tests/test_moe_rl_swan.py
- Layer: testing
- Language: py
- Symbols:
  - `TestDetectionOracle` (class, line 37) `class TestDetectionOracle`
  - `TestMoERouter` (class, line 121) `class TestMoERouter`
  - `TestRLTrainer` (class, line 223) `class TestRLTrainer`
  - `TestSwanAgent` (class, line 340) `class TestSwanAgent`
  - `TestAutonomousDaemonSWAN` (class, line 493) `class TestAutonomousDaemonSWAN`
  - `TestPolicyDetectionAware` (class, line 571) `class TestPolicyDetectionAware`
  - `TestWorldModelGraph` (class, line 616) `class TestWorldModelGraph`
  - `TestMCPRegistration` (class, line 675) `class TestMCPRegistration`
  - `test_low_risk_dns_query` (method, line 38) `def test_low_risk_dns_query(self)`
  - `test_high_risk_mimikatz` (method, line 46) `def test_high_risk_mimikatz(self)`
  - `test_critical_risk_combined_credential_tools` (method, line 54) `def test_critical_risk_combined_credential_tools(self)`
  - `test_assessment_has_required_fields` (method, line 62) `def test_assessment_has_required_fields(self)`
  - `test_is_high_risk_property_consistent_with_probability` (method, line 75) `def test_is_high_risk_property_consistent_with_probability(self)`
  - `test_singleton_returns_same_instance` (method, line 83) `def test_singleton_returns_same_instance(self)`
  - `test_nmap_is_not_high_risk` (method, line 91) `def test_nmap_is_not_high_risk(self)`
  - `test_evil_winrm_is_high_risk` (method, line 99) `def test_evil_winrm_is_high_risk(self)`
  - `test_is_critical_risk_property` (method, line 107) `def test_is_critical_risk_property(self)`
  - `test_singleton_returns_same_instance` (method, line 122) `def test_singleton_returns_same_instance(self)`
  - `test_route_returns_expert_or_raises_gracefully` (method, line 130) `def test_route_returns_expert_or_raises_gracefully(self)`
  - `test_ensemble_returns_available_candidates` (method, line 143) `def test_ensemble_returns_available_candidates(self)`
  - `test_record_outcome_updates_ema` (method, line 154) `def test_record_outcome_updates_ema(self, tmp_path)`
  - `test_performance_bonus_positive_after_success` (method, line 164) `def test_performance_bonus_positive_after_success(self, tmp_path)`
  - `test_performance_bonus_penalises_high_detection` (method, line 173) `def test_performance_bonus_penalises_high_detection(self, tmp_path)`
  - `test_status_report_contains_experts` (method, line 184) `def test_status_report_contains_experts(self)`
  - `test_softmax_deterministic_picks_highest_weight` (method, line 193) `def test_softmax_deterministic_picks_highest_weight(self)`
  - `test_encode_state_format` (method, line 224) `def test_encode_state_format(self)`
  - `test_select_action_returns_valid_candidate` (method, line 236) `def test_select_action_returns_valid_candidate(self)`
  - `test_update_changes_qvalue` (method, line 246) `def test_update_changes_qvalue(self, tmp_path)`
  - `test_epsilon_decays_after_update` (method, line 269) `def test_epsilon_decays_after_update(self, tmp_path)`
  - `test_detection_penalty_lowers_effective_reward` (method, line 281) `def test_detection_penalty_lowers_effective_reward(self, tmp_path)`
  - `test_optimistic_init_for_unseen_actions` (method, line 310) `def test_optimistic_init_for_unseen_actions(self, tmp_path)`
  - `test_save_and_reload_persistence` (method, line 318) `def test_save_and_reload_persistence(self, tmp_path)`
  - `test_swan_result_dataclass_fields` (method, line 341) `def test_swan_result_dataclass_fields(self)`
  - `test_swan_result_failed_is_not_success` (method, line 364) `def test_swan_result_failed_is_not_success(self)`
  - `test_outcome_evaluator_success_reward` (method, line 380) `def test_outcome_evaluator_success_reward(self)`
  - `test_outcome_evaluator_failed_gives_negative_reward` (method, line 399) `def test_outcome_evaluator_failed_gives_negative_reward(self)`
  - `test_outcome_evaluator_high_value_category_bonus` (method, line 417) `def test_outcome_evaluator_high_value_category_bonus(self)`
  - `test_mcp_swan_route_returns_valid_json` (method, line 438) `def test_mcp_swan_route_returns_valid_json(self)`
  - `test_mcp_swan_status_returns_valid_json` (method, line 452) `def test_mcp_swan_status_returns_valid_json(self)`
  - `test_ensemble_result_dataclass_fields` (method, line 460) `def test_ensemble_result_dataclass_fields(self)`
  - `test_swan_selector_disabled_by_default` (method, line 494) `def test_swan_selector_disabled_by_default(self)`
  - `test_swan_selector_phase_mapping_coverage` (method, line 503) `def test_swan_selector_phase_mapping_coverage(self)`
  - `test_cascade_strategy_contains_swan_selector` (method, line 511) `def test_cascade_strategy_contains_swan_selector(self)`
  - `test_cascade_strategy_order` (method, line 525) `def test_cascade_strategy_order(self)`
  - `test_fallback_selector_never_returns_none` (method, line 539) `def test_fallback_selector_never_returns_none(self)`
  - `test_command_decision_source_label` (method, line 548) `def test_command_decision_source_label(self)`
  - `test_llm_selector_disabled_without_env` (method, line 556) `def test_llm_selector_disabled_without_env(self)`
  - `test_detection_above_threshold_zeroes_reward` (method, line 572) `def test_detection_above_threshold_zeroes_reward(self)`
  - `test_low_detection_preserves_positive_reward` (method, line 587) `def test_low_detection_preserves_positive_reward(self)`
  - `test_failed_outcome_gives_negative_reward` (method, line 602) `def test_failed_outcome_gives_negative_reward(self)`
  - `test_add_relation_and_pivot_candidates` (method, line 617) `def test_add_relation_and_pivot_candidates(self, tmp_path)`
  - `test_graph_snapshot_is_serialisable` (method, line 634) `def test_graph_snapshot_is_serialisable(self, tmp_path)`
  - `test_auto_relation_on_service_add` (method, line 645) `def test_auto_relation_on_service_add(self, tmp_path)`
  - `test_pivot_candidates_sorted_by_centrality` (method, line 656) `def test_pivot_candidates_sorted_by_centrality(self, tmp_path)`
  - `test_swan_tools_registered_in_mcp` (method, line 676) `def test_swan_tools_registered_in_mcp(self)`
  - `test_hive_tools_registered_in_mcp` (method, line 688) `def test_hive_tools_registered_in_mcp(self)`
  - `_ep` (function, line 199) `def _ep(eid, w)`
  - `_make_trainer` (function, line 285) `def _make_trainer(suffix)`
  - `_result` (function, line 421) `def _result(task_type)`
- Depends on: `modules/detection_oracle.py`, `modules/moe_router.py`, `modules/rl_trainer.py`, `skills/autonomous_daemon.py`, `skills/lazyown_policy.py`, `skills/swan_agent.py`

## tests/test_moe_router_check_regression.py
- Doc: Regression coverage for ``modules.moe_router.ExpertAvailabilityChecker._check``.
- Layer: testing
- Language: py
- Symbols:
  - `test_check_groq_returns_false_without_api_key` (function, line 27) `def test_check_groq_returns_false_without_api_key(monkeypatch)`
  - `test_check_groq_returns_true_with_explicit_key` (function, line 47) `def test_check_groq_returns_true_with_explicit_key()`
  - `test_check_groq_reads_env_when_arg_empty` (function, line 65) `def test_check_groq_reads_env_when_arg_empty(monkeypatch)`
  - `test_check_toposwarm_uses_module_level_os_and_path` (function, line 85) `def test_check_toposwarm_uses_module_level_os_and_path(tmp_path, monkeypatch)`
  - `test_check_toposwarm_returns_false_when_dir_absent` (function, line 110) `def test_check_toposwarm_returns_false_when_dir_absent(tmp_path, monkeypatch)`
  - `test_check_unknown_backend_is_unavailable` (function, line 131) `def test_check_unknown_backend_is_unavailable()`
- Depends on: `modules/moe_router.py`

## tests/test_mutation_verification.py
- Doc: Mutation verification contracts.
- Layer: testing
- Language: py
- Symbols:
  - `test_sql_injection_blocked` (function, line 19) `def test_sql_injection_blocked()`
  - `test_hmac_compare_digest_used` (function, line 27) `def test_hmac_compare_digest_used()`
  - `test_shell_false_in_safe_runner` (function, line 41) `def test_shell_false_in_safe_runner()`
  - `test_pickle_removed` (function, line 56) `def test_pickle_removed()`
  - `test_no_hardcoded_secrets` (function, line 63) `def test_no_hardcoded_secrets()`
- Depends on: `modules/db.py`

## tests/test_nethelpers_command_set.py
- Doc: Network helpers command set extraction tests.
- Layer: testing
- Language: py
- Symbols:
  - `_add_repo_root_to_syspath` (function, line 32) `def _add_repo_root_to_syspath()`
  - `NethelpersSuiteConfig` (class, line 38) `class NethelpersSuiteConfig`
  - `_methods_of` (function, line 61) `def _methods_of(path, class_name)`
  - `test_target_is_active_command_set` (function, line 73) `def test_target_is_active_command_set()`
  - `test_target_exposes_full_nethelpers_cluster` (function, line 82) `def test_target_exposes_full_nethelpers_cluster()`
  - `test_target_phase_metadata` (function, line 89) `def test_target_phase_metadata()`
  - `test_source_no_longer_defines_cluster` (function, line 95) `def test_source_no_longer_defines_cluster()`
  - `test_registry_registers_target` (function, line 101) `def test_registry_registers_target()`
  - `test_no_command_collisions_with_source` (function, line 108) `def test_no_command_collisions_with_source()`
- Depends on: `cli/commands/_base.py`, `cli/commands/_dormancy.py`, `cli/commands/misc_migrated.py`, `cli/commands/nethelpers.py`, `cli/registry.py`

## tests/test_no_shell_execution.py
- Doc: Contract tests: no os.system and no manual sys.stdout reassignment.
- Layer: testing
- Language: py
- Symbols:
  - `ScanConfig` (class, line 20) `class ScanConfig`
  - `_parse` (function, line 64) `def _parse(path)`
  - `find_os_system_calls` (function, line 72) `def find_os_system_calls(config)`
  - `find_stdout_assignments` (function, line 96) `def find_stdout_assignments(config)`
  - `test_no_os_system_in_production` (function, line 124) `def test_no_os_system_in_production()`
  - `test_no_manual_stdout_reassignment` (function, line 130) `def test_no_manual_stdout_reassignment()`
  - `test_scanner_detects_a_synthetic_os_system` (function, line 136) `def test_scanner_detects_a_synthetic_os_system(tmp_path)`
  - `iter_files` (method, line 44) `def iter_files(self)`

## tests/test_nuclei_parser.py
- Doc: Tests for modules/integrations/nuclei_parser.py
- Layer: testing
- Language: py
- Symbols:
  - `TestNucleiFinding` (class, line 13) `class TestNucleiFinding`
  - `TestNucleiParserText` (class, line 58) `class TestNucleiParserText`
  - `TestNucleiParserJson` (class, line 73) `class TestNucleiParserJson`
  - `TestSeverityMap` (class, line 120) `class TestSeverityMap`
  - `TestMitreTactics` (class, line 128) `class TestMitreTactics`
  - `TestRecommendations` (class, line 134) `class TestRecommendations`
  - `test_fields` (method, line 14) `def test_fields(self)`
  - `test_exploit_probability_map` (method, line 28) `def test_exploit_probability_map(self)`
  - `test_mitre_tactic` (method, line 46) `def test_mitre_tactic(self)`
  - `test_parse_empty` (method, line 59) `def test_parse_empty(self)`
  - `test_parse_nuclei_line` (method, line 64) `def test_parse_nuclei_line(self)`
  - `test_parse_empty` (method, line 74) `def test_parse_empty(self)`
  - `test_parse_json_single_finding` (method, line 78) `def test_parse_json_single_finding(self)`
  - `test_parse_json_multiple_findings` (method, line 90) `def test_parse_json_multiple_findings(self)`
  - `test_parse_json_array` (method, line 99) `def test_parse_json_array(self)`
  - `test_parse_with_cve_classification` (method, line 108) `def test_parse_with_cve_classification(self)`
  - `test_critical_is_10` (method, line 121) `def test_critical_is_10(self)`
  - `test_info_is_1` (method, line 124) `def test_info_is_1(self)`
  - `test_all_tactics_have_ta_prefix` (method, line 129) `def test_all_tactics_have_ta_prefix(self)`
  - `test_generate_for_critical` (method, line 135) `def test_generate_for_critical(self)`
  - `test_skip_low_severity` (method, line 151) `def test_skip_low_severity(self)`
- Depends on: `modules/integrations/nuclei_parser.py`

## tests/test_objective_bootstrap.py
- Doc: Contract tests for modules/loop/objective_bootstrap.py.
- Layer: testing
- Language: py
- Symbols:
  - `_collect_emit` (function, line 11) `def _collect_emit()`
  - `test_scope_denied_aborts_before_enrich_and_frontier` (function, line 20) `def test_scope_denied_aborts_before_enrich_and_frontier(monkeypatch)`
  - `test_in_scope_builds_frontier_guard_and_enriches` (function, line 53) `def test_in_scope_builds_frontier_guard_and_enriches(monkeypatch)`
  - `test_goals_decomposed_emitted` (function, line 82) `def test_goals_decomposed_emitted(monkeypatch)`
  - `test_goal_failure_degrades_without_raising` (function, line 107) `def test_goal_failure_degrades_without_raising(monkeypatch)`
  - `_emit` (function, line 14) `def _emit(name, payload)`
  - `_FakeEngine` (class, line 57) `class _FakeEngine`
  - `_boom` (function, line 115) `def _boom()`
  - `submit` (method, line 58) `def submit(self, target)`
- Depends on: `modules/loop/objective_bootstrap.py`

## tests/test_opencode_backend.py
- Doc: Contract tests for the OpenCode Zen LLM backend.
- Layer: testing
- Language: py
- Symbols:
  - `_FakeOpenAIClient` (class, line 17) `class _FakeOpenAIClient`
  - `fake_openai` (function, line 30) `def fake_openai(monkeypatch)`
  - `TestOpenCodeRegistration` (class, line 38) `class TestOpenCodeRegistration`
  - `TestOpenCodeBuild` (class, line 56) `class TestOpenCodeBuild`
  - `__init__` (method, line 24) `def __init__(self, api_key, base_url)`
  - `test_backend_is_supported` (method, line 39) `def test_backend_is_supported(self)`
  - `test_backend_is_cloud_gated` (method, line 43) `def test_backend_is_cloud_gated(self)`
  - `test_default_model_and_keys` (method, line 46) `def test_default_model_and_keys(self)`
  - `test_model_class_exported` (method, line 52) `def test_model_class_exported(self)`
  - `test_builds_from_config_key` (method, line 57) `def test_builds_from_config_key(self, fake_openai)`
  - `test_base_url_override` (method, line 69) `def test_base_url_override(self, fake_openai)`
  - `test_default_model_when_unset` (method, line 78) `def test_default_model_when_unset(self, fake_openai)`
  - `test_env_var_fallback` (method, line 83) `def test_env_var_fallback(self, fake_openai, monkeypatch)`
  - `test_missing_key_raises` (method, line 88) `def test_missing_key_raises(self, monkeypatch)`
  - `test_placeholder_key_rejected` (method, line 93) `def test_placeholder_key_rejected(self, monkeypatch)`
  - `test_model_identifier_for_budget` (method, line 100) `def test_model_identifier_for_budget(self)`

## tests/test_opencode_mcp_harness.py
- Doc: Opencode shim harness tool tests.
- Layer: testing
- Language: py
- Symbols:
  - `OpencodeShimHarnessSpec` (class, line 16) `class OpencodeShimHarnessSpec(TestCase)`
  - `test_harness_tools_listed` (method, line 19) `def test_harness_tools_listed(self)`
  - `test_harness_status_shape` (method, line 25) `def test_harness_status_shape(self)`
  - `test_golden_paths_and_ctf` (method, line 32) `def test_golden_paths_and_ctf(self)`
  - `test_unknown_tool_rejected` (method, line 47) `def test_unknown_tool_rejected(self)`
- Depends on: `modules/__init__.py`, `skills/lazyown_mcp_opencode.py`

## tests/test_ops_loot_phase.py
- Doc: Tests for unified loot, cred-graph view, and quantitative phase progress.
- Layer: testing
- Language: py
- Symbols:
  - `_seed_loot` (function, line 34) `def _seed_loot(sessions_dir)`
  - `_write_world` (function, line 46) `def _write_world(sessions_dir, world)`
  - `test_gather_loot_parses_kinds_and_skips_noise` (function, line 53) `def test_gather_loot_parses_kinds_and_skips_noise(tmp_path)`
  - `test_loot_entry_value` (function, line 65) `def test_loot_entry_value()`
  - `test_resolve_cred_value_precedence` (function, line 70) `def test_resolve_cred_value_precedence()`
  - `test_loot_show_renders_table` (function, line 85) `def test_loot_show_renders_table(tmp_path, capsys)`
  - `test_loot_show_empty` (function, line 94) `def test_loot_show_empty(tmp_path, capsys)`
  - `test_loot_search_hits_and_provenance` (function, line 101) `def test_loot_search_hits_and_provenance(tmp_path, capsys)`
  - `test_loot_search_no_match` (function, line 115) `def test_loot_search_no_match(tmp_path, capsys)`
  - `test_loot_search_requires_query` (function, line 123) `def test_loot_search_requires_query(tmp_path, capsys)`
  - `test_loot_reuse_no_target` (function, line 133) `def test_loot_reuse_no_target(tmp_path, capsys)`
  - `test_loot_reuse_no_loot` (function, line 141) `def test_loot_reuse_no_loot(tmp_path, capsys)`
  - `test_loot_reuse_excludes_rejected_and_flags_confirmed` (function, line 148) `def test_loot_reuse_excludes_rejected_and_flags_confirmed(tmp_path, capsys)`
  - `test_loot_graph_renders_edges` (function, line 174) `def test_loot_graph_renders_edges(tmp_path, capsys)`
  - `test_loot_graph_empty` (function, line 196) `def test_loot_graph_empty(tmp_path, capsys)`
  - `test_loot_mark_writes_rejected_edge` (function, line 206) `def test_loot_mark_writes_rejected_edge(tmp_path)`
  - `test_loot_mark_rejects_bad_outcome` (function, line 224) `def test_loot_mark_rejects_bad_outcome(tmp_path, capsys)`
  - `test_loot_mark_unknown_credential` (function, line 232) `def test_loot_mark_unknown_credential(tmp_path, capsys)`
  - `test_phase_progress_ranks` (function, line 243) `def test_phase_progress_ranks(tmp_path)`
  - `test_phase_progress_completed_override` (function, line 264) `def test_phase_progress_completed_override(tmp_path)`
  - `test_phase_progress_os_owned_report_and_loot` (function, line 285) `def test_phase_progress_os_owned_report_and_loot(tmp_path)`
  - `test_link_credential_to_failure_edge_and_roundtrip` (function, line 312) `def test_link_credential_to_failure_edge_and_roundtrip(tmp_path)`
- Depends on: `cli/ops_commands.py`, `modules/world_model.py`

## tests/test_opsec_scorer.py
- Doc: Tests for modules/opsec_scorer.py
- Layer: testing
- Language: py
- Symbols:
  - `TestOpsecScorer` (class, line 13) `class TestOpsecScorer`
  - `test_score_high_noise_command` (method, line 14) `def test_score_high_noise_command(self)`
  - `test_score_low_noise_command` (method, line 21) `def test_score_low_noise_command(self)`
  - `test_score_unknown_command` (method, line 27) `def test_score_unknown_command(self)`
  - `test_score_with_evasion` (method, line 33) `def test_score_with_evasion(self)`
  - `test_score_batch` (method, line 39) `def test_score_batch(self)`
  - `test_score_to_dict` (method, line 45) `def test_score_to_dict(self)`
  - `test_confidence_is_float` (method, line 61) `def test_confidence_is_float(self)`
  - `test_mitigations_returned` (method, line 67) `def test_mitigations_returned(self)`
  - `test_convenience_function` (method, line 72) `def test_convenience_function(self)`
  - `test_all_known_commands_have_mitigations` (method, line 77) `def test_all_known_commands_have_mitigations(self)`
  - `test_suggest_mitigations` (method, line 85) `def test_suggest_mitigations(self)`
  - `test_target_sensitivity_dc` (method, line 90) `def test_target_sensitivity_dc(self)`
- Depends on: `modules/opsec_scorer.py`

## tests/test_opsec_scorer_consolidated.py
- Doc: Consolidated OPSEC scorer contract tests (SDD/TDD/BDD).
- Layer: testing
- Language: py
- Symbols:
  - `TestSharedRiskMapping` (class, line 29) `class TestSharedRiskMapping`
  - `TestRiskLevelAndGate` (class, line 59) `class TestRiskLevelAndGate`
  - `TestOpsecScorerV2` (class, line 78) `class TestOpsecScorerV2`
  - `TestBackwardCompatibility` (class, line 140) `class TestBackwardCompatibility`
  - `test_risk_buckets_respect_thresholds` (method, line 30) `def test_risk_buckets_respect_thresholds(self)`
  - `test_risk_label_matches_bucket` (method, line 40) `def test_risk_label_matches_bucket(self)`
  - `test_risk_level_matches_bucket` (method, line 46) `def test_risk_level_matches_bucket(self)`
  - `test_string_and_enum_labels_are_consistent` (method, line 52) `def test_string_and_enum_labels_are_consistent(self)`
  - `test_enum_values` (method, line 60) `def test_enum_values(self)`
  - `test_gate_mapping` (method, line 70) `def test_gate_mapping(self)`
  - `test_assess_returns_gated_score` (method, line 79) `def test_assess_returns_gated_score(self)`
  - `test_mimikatz_is_high_critical` (method, line 87) `def test_mimikatz_is_high_critical(self)`
  - `test_ping_is_allow` (method, line 99) `def test_ping_is_allow(self)`
  - `test_should_allow_returns_tuple` (method, line 105) `def test_should_allow_returns_tuple(self)`
  - `test_trend_insufficient_data` (method, line 111) `def test_trend_insufficient_data(self)`
  - `test_trend_after_scoring` (method, line 115) `def test_trend_after_scoring(self)`
  - `test_mitigations_generated` (method, line 123) `def test_mitigations_generated(self)`
  - `test_alternatives_for_mimikatz` (method, line 128) `def test_alternatives_for_mimikatz(self)`
  - `test_unknown_command_uses_default_profile` (method, line 133) `def test_unknown_command_uses_default_profile(self)`
  - `test_v1_score_returns_string_risk` (method, line 141) `def test_v1_score_returns_string_risk(self)`
  - `test_opsec_context_defaults` (method, line 147) `def test_opsec_context_defaults(self)`
  - `test_risk_profiles_shared_table_intact` (method, line 154) `def test_risk_profiles_shared_table_intact(self)`
- Depends on: `modules/opsec_scorer.py`

## tests/test_orchestrator_api.py
- Doc: Integration tests for the orchestrator REST API (``/api/v1/orchestrator``).
- Layer: testing
- Language: py
- Symbols:
  - `orchestrator_client` (function, line 22) `def orchestrator_client(tmp_path, monkeypatch)`
  - `_auth` (function, line 43) `def _auth(token)`
  - `test_status_requires_auth` (function, line 47) `def test_status_requires_auth(orchestrator_client)`
  - `test_status_reports_layers` (function, line 54) `def test_status_reports_layers(orchestrator_client)`
  - `test_verb_toggle_round_trip` (function, line 67) `def test_verb_toggle_round_trip(orchestrator_client, tmp_path, monkeypatch)`
  - `test_verb_toggle_unknown_command_rejected` (function, line 97) `def test_verb_toggle_unknown_command_rejected(orchestrator_client, tmp_path, monkeypatch)`
  - `test_stage_toggle_round_trip` (function, line 116) `def test_stage_toggle_round_trip(orchestrator_client, monkeypatch, tmp_path)`
  - `test_stage_unknown_rejected` (function, line 149) `def test_stage_unknown_rejected(orchestrator_client)`
  - `test_trigger_crud_round_trip` (function, line 160) `def test_trigger_crud_round_trip(orchestrator_client)`
  - `test_trigger_unknown_kind_rejected` (function, line 179) `def test_trigger_unknown_kind_rejected(orchestrator_client)`
  - `_load` (function, line 126) `def _load()`
  - `_write` (function, line 131) `def _write(payload)`
- Depends on: `core/api_authz.py`, `lazyc2/blueprints/orchestrator.py`, `modules/__init__.py`, `modules/lazy_loop.py`, `modules/orchestrator_config.py`, `modules/trigger_policy.py`, `modules/verb_catalog.py`, `modules/world_model.py`

## tests/test_orchestrator_loop_substrate.py
- Doc: Tests for orchestrator termination/leases/boundary/evidence sections.
- Layer: testing
- Language: py
- Symbols:
  - `payload_store` (function, line 11) `def payload_store(monkeypatch)`
  - `test_termination_defaults` (function, line 19) `def test_termination_defaults(payload_store)`
  - `test_termination_payload_override` (function, line 26) `def test_termination_payload_override(payload_store)`
  - `test_termination_bad_mode_falls_back` (function, line 33) `def test_termination_bad_mode_falls_back(payload_store)`
  - `test_leases_defaults_and_override` (function, line 38) `def test_leases_defaults_and_override(payload_store)`
  - `test_leases_bad_value_falls_back` (function, line 48) `def test_leases_bad_value_falls_back(payload_store)`
  - `test_boundary_default_on_and_disableable` (function, line 53) `def test_boundary_default_on_and_disableable(payload_store)`
  - `test_evidence_defaults_and_override` (function, line 59) `def test_evidence_defaults_and_override(payload_store)`
  - `test_validate_rejects_bad_termination_mode` (function, line 67) `def test_validate_rejects_bad_termination_mode()`
  - `test_validate_rejects_negative_lease_ttl` (function, line 74) `def test_validate_rejects_negative_lease_ttl()`
  - `test_validate_rejects_bad_boundary_type` (function, line 81) `def test_validate_rejects_bad_boundary_type()`
  - `test_validate_accepts_full_section` (function, line 88) `def test_validate_accepts_full_section()`
- Depends on: `modules/__init__.py`

## tests/test_orchestrator_pacing.py
- Doc: Pacing tab: jitter and sleeper controls round-trip through set_pacing.
- Layer: testing
- Language: py
- Symbols:
  - `pacing_store` (function, line 24) `def pacing_store(monkeypatch)`
  - `_saver` (function, line 41) `def _saver()`
  - `test_parse_sleeper_windows_splits_valid_and_invalid` (function, line 46) `def test_parse_sleeper_windows_splits_valid_and_invalid()`
  - `test_format_sleeper_windows_round_trips` (function, line 52) `def test_format_sleeper_windows_round_trips()`
  - `test_parse_edr_pause_ranges_accepts_level_low_high` (function, line 56) `def test_parse_edr_pause_ranges_accepts_level_low_high()`
  - `test_parse_edr_pause_ranges_rejects_inverted_and_garbage` (function, line 62) `def test_parse_edr_pause_ranges_rejects_inverted_and_garbage()`
  - `test_format_edr_pause_ranges_round_trips` (function, line 68) `def test_format_edr_pause_ranges_round_trips()`
  - `test_save_pacing_persists_valid_sleeper_windows` (function, line 72) `def test_save_pacing_persists_valid_sleeper_windows(pacing_store)`
  - `test_save_pacing_persists_edr_pause_ranges` (function, line 87) `def test_save_pacing_persists_edr_pause_ranges(pacing_store)`
  - `test_save_pacing_rejects_malformed_window` (function, line 96) `def test_save_pacing_rejects_malformed_window(pacing_store)`
  - `test_saved_windows_reach_edr_pacer` (function, line 104) `def test_saved_windows_reach_edr_pacer(pacing_store)`
  - `_save` (function, line 31) `def _save(payload)`
- Depends on: `cli/orchestrator_assets_tabs.py`, `modules/__init__.py`, `modules/loop_guardrails.py`

## tests/test_orchestrator_triggers.py
- Doc: BDD tests for the orchestrator Triggers tab.
- Layer: testing
- Language: py
- Symbols:
  - `sandbox` (function, line 16) `def sandbox(tmp_path, monkeypatch)`
  - `test_triggers_tab_lists_store_rows` (function, line 25) `def test_triggers_tab_lists_store_rows(sandbox)`
  - `test_triggers_toggle_persists` (function, line 45) `def test_triggers_toggle_persists(sandbox)`
  - `test_triggers_add_and_remove_via_app` (function, line 59) `def test_triggers_add_and_remove_via_app(sandbox)`
  - `test_trigger_kind_options_cover_registry` (function, line 72) `def test_trigger_kind_options_cover_registry(sandbox)`
  - `_drive` (function, line 34) `def _drive()`
- Depends on: `cli/lazy_orchestrator.py`, `modules/lazy_loop.py`, `modules/loop_triggers.py`, `modules/trigger_policy.py`

## tests/test_orchestrator_yaml.py
- Doc: Orchestrator YAML BDD contract: profiles, stages, limits and CLI wiring.
- Layer: testing
- Language: py
- Symbols:
  - `payload_store` (function, line 18) `def payload_store(monkeypatch)`
  - `test_shipped_yaml_declares_required_profiles` (function, line 39) `def test_shipped_yaml_declares_required_profiles(payload_store)`
  - `test_payload_profile_overrides_yaml` (function, line 49) `def test_payload_profile_overrides_yaml(payload_store)`
  - `test_stage_params_resolve_and_payload_still_overrides` (function, line 60) `def test_stage_params_resolve_and_payload_still_overrides(payload_store)`
  - `test_profile_inheritance_merges_stages_and_limits` (function, line 72) `def test_profile_inheritance_merges_stages_and_limits(payload_store, tmp_path, monkeypatch)`
  - `test_unknown_profile_is_rejected_and_payload_falls_back` (function, line 113) `def test_unknown_profile_is_rejected_and_payload_falls_back(payload_store)`
  - `test_validate_config_rejects_unknown_version_and_bad_stage` (function, line 124) `def test_validate_config_rejects_unknown_version_and_bad_stage()`
  - `test_engine_uses_profile_limits` (function, line 141) `def test_engine_uses_profile_limits(payload_store, monkeypatch, tmp_path)`
  - `test_runner_parses_profile_and_resolves_defaults` (function, line 157) `def test_runner_parses_profile_and_resolves_defaults(payload_store)`
  - `test_admin_console_switches_profile` (function, line 176) `def test_admin_console_switches_profile(payload_store)`
  - `test_payload_sink_toggles_override_profile` (function, line 188) `def test_payload_sink_toggles_override_profile(payload_store)`
  - `_load` (function, line 22) `def _load(target)`
  - `_save` (function, line 25) `def _save(data, target)`
- Depends on: `cli/lazy_orchestrator.py`, `core/config.py`, `modules/__init__.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `modules/orchestrator_config.py`

## tests/test_outcome_attribution.py
- Doc: Tests for Observer-style failure attribution and verb demotion.
- Layer: testing
- Language: py
- Symbols:
  - `test_classify_blocked_markers` (function, line 22) `def test_classify_blocked_markers()`
  - `test_classify_blocked_wins_over_error_flag` (function, line 29) `def test_classify_blocked_wins_over_error_flag()`
  - `test_classify_error_markers` (function, line 33) `def test_classify_error_markers()`
  - `test_classify_ok` (function, line 39) `def test_classify_ok()`
  - `test_classify_vendor_on_success_is_ok` (function, line 44) `def test_classify_vendor_on_success_is_ok()`
  - `test_classify_vendor_with_rejection_is_blocked` (function, line 51) `def test_classify_vendor_with_rejection_is_blocked()`
  - `test_classify_short_waf_codes_still_blocked` (function, line 57) `def test_classify_short_waf_codes_still_blocked()`
  - `test_ledger_concurrent_records_do_not_lose_updates` (function, line 62) `def test_ledger_concurrent_records_do_not_lose_updates(tmp_path)`
  - `test_verb_of_basename` (function, line 80) `def test_verb_of_basename()`
  - `test_ledger_records_and_counts` (function, line 86) `def test_ledger_records_and_counts(tmp_path)`
  - `test_ledger_demotes_after_threshold` (function, line 94) `def test_ledger_demotes_after_threshold(tmp_path)`
  - `test_ledger_success_clears_demotion` (function, line 102) `def test_ledger_success_clears_demotion(tmp_path)`
  - `test_ledger_ignores_unparseable_verb` (function, line 111) `def test_ledger_ignores_unparseable_verb(tmp_path)`
  - `test_ledger_task_isolation` (function, line 117) `def test_ledger_task_isolation(tmp_path)`
  - `test_agentic_blocked_verbs_reads_ledger` (function, line 126) `def test_agentic_blocked_verbs_reads_ledger(tmp_path, monkeypatch)`
  - `_hit` (function, line 68) `def _hit()`
- Depends on: `modules/loop/worker_agentic.py`, `modules/outcome_attribution.py`

## tests/test_outcome_bus.py
- Doc: Outcome bus BDD contract: one event, every surface, failure isolation.
- Layer: testing
- Language: py
- Symbols:
  - `test_bus_fans_out_dedupes_and_audits` (function, line 15) `def test_bus_fans_out_dedupes_and_audits(tmp_path)`
  - `test_bus_isolates_sink_failures` (function, line 32) `def test_bus_isolates_sink_failures(tmp_path)`
  - `test_bus_respects_sink_toggles` (function, line 45) `def test_bus_respects_sink_toggles(monkeypatch, tmp_path)`
  - `test_default_sinks_cover_required_surfaces` (function, line 58) `def test_default_sinks_cover_required_surfaces()`
  - `test_c2_surface_sink_writes_banner_cve_and_note` (function, line 76) `def test_c2_surface_sink_writes_banner_cve_and_note(tmp_path)`
  - `test_objectives_sink_appends_actionable_finding` (function, line 104) `def test_objectives_sink_appends_actionable_finding(tmp_path)`
  - `test_report_sink_only_refreshes_terminal_events` (function, line 123) `def test_report_sink_only_refreshes_terminal_events(monkeypatch)`
  - `test_intel_graph_sink_writes_summary` (function, line 139) `def test_intel_graph_sink_writes_summary(tmp_path)`
  - `test_attack_graph_sink_writes_summary` (function, line 148) `def test_attack_graph_sink_writes_summary(tmp_path, monkeypatch)`
  - `test_record_outcome_builds_one_exploit_event` (function, line 159) `def test_record_outcome_builds_one_exploit_event(monkeypatch, tmp_path)`
  - `test_killchain_sink_only_advances_on_proven_outcomes` (function, line 208) `def test_killchain_sink_only_advances_on_proven_outcomes(monkeypatch)`
  - `test_objectives_sink_ignores_failed_and_dry_run` (function, line 229) `def test_objectives_sink_ignores_failed_and_dry_run(tmp_path)`
  - `test_dedupe_key_includes_port_and_requested_sinks` (function, line 244) `def test_dedupe_key_includes_port_and_requested_sinks(tmp_path)`
  - `test_world_diff_sink_records_host_changes` (function, line 259) `def test_world_diff_sink_records_host_changes(tmp_path)`
  - `test_world_diff_sink_detects_service_change` (function, line 280) `def test_world_diff_sink_detects_service_change(tmp_path)`
  - `test_world_diff_sink_ignores_hostless_events` (function, line 296) `def test_world_diff_sink_ignores_hostless_events(tmp_path)`
  - `test_beacon_dispatch_sink_stages_foothold_command` (function, line 305) `def test_beacon_dispatch_sink_stages_foothold_command(tmp_path, monkeypatch)`
  - `test_beacon_dispatch_sink_ignores_non_foothold` (function, line 321) `def test_beacon_dispatch_sink_ignores_non_foothold(tmp_path, monkeypatch)`
  - `test_beacon_dispatch_sink_requires_c2_target` (function, line 331) `def test_beacon_dispatch_sink_requires_c2_target(tmp_path, monkeypatch)`
  - `test_beacon_dispatch_sink_clips_when_enabled` (function, line 341) `def test_beacon_dispatch_sink_clips_when_enabled(tmp_path, monkeypatch)`
  - `test_transient_sink_failure_is_retried` (function, line 353) `def test_transient_sink_failure_is_retried(tmp_path)`
  - `test_concurrent_duplicates_fan_out_once` (function, line 372) `def test_concurrent_duplicates_fan_out_once(tmp_path)`
  - `boom` (function, line 34) `def boom(event)`
  - `fake_record` (function, line 166) `def fake_record(event, sinks)`
  - `flaky` (function, line 358) `def flaky(_event)`
- Depends on: `modules/atomic_exploit_bridge.py`, `modules/orchestrator_config.py`, `modules/outcome_bus.py`, `modules/sinks/attack_graph.py`, `modules/sinks/beacon_dispatch.py`, `modules/sinks/c2_surfaces.py`, `modules/sinks/intel_graph.py`, `modules/sinks/killchain.py`, `modules/sinks/objectives.py`, `modules/sinks/world_diff.py`

## tests/test_pacing.py
- Doc: Configurable pacing: EdrPacer ranges, jitter scaling, sleeper windows.
- Layer: testing
- Language: py
- Symbols:
  - `test_sleeper_window_regex_accepts_valid_windows` (function, line 14) `def test_sleeper_window_regex_accepts_valid_windows()`
  - `test_edr_pacer_configurable_pause_ranges` (function, line 22) `def test_edr_pacer_configurable_pause_ranges()`
  - `test_edr_pacer_empty_ranges_disables_level_pauses` (function, line 32) `def test_edr_pacer_empty_ranges_disables_level_pauses()`
  - `test_edr_pacer_jitter_scales_drawn_delay` (function, line 40) `def test_edr_pacer_jitter_scales_drawn_delay()`
  - `test_edr_pacer_max_delay_clamps` (function, line 48) `def test_edr_pacer_max_delay_clamps()`
  - `test_edr_pacer_sleeper_window_extends_delay` (function, line 55) `def test_edr_pacer_sleeper_window_extends_delay()`
  - `test_edr_pacer_sleeper_window_outside_is_zero` (function, line 73) `def test_edr_pacer_sleeper_window_outside_is_zero()`
  - `test_edr_pacer_sleeper_wraps_midnight` (function, line 82) `def test_edr_pacer_sleeper_wraps_midnight()`
  - `test_edr_pacer_parse_windows_skips_invalid` (function, line 89) `def test_edr_pacer_parse_windows_skips_invalid()`
  - `test_edr_pacer_from_config_reads_orchestrator` (function, line 94) `def test_edr_pacer_from_config_reads_orchestrator(monkeypatch)`
  - `test_edr_pacer_from_config_disabled_is_inert` (function, line 118) `def test_edr_pacer_from_config_disabled_is_inert(monkeypatch)`
  - `test_validate_config_accepts_pacing_block` (function, line 128) `def test_validate_config_accepts_pacing_block()`
  - `test_validate_config_rejects_bad_pacing` (function, line 149) `def test_validate_config_rejects_bad_pacing()`
  - `test_validate_config_rejects_pacing_not_mapping` (function, line 171) `def test_validate_config_rejects_pacing_not_mapping()`
- Depends on: `modules/loop_guardrails.py`, `modules/orchestrator_config.py`


Next: [KB_tests_p22.md](KB_tests_p22.md)
