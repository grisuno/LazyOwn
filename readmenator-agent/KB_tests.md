# Subsystem: tests (page 1 of 17)
Pages: [KB_tests.md](KB_tests.md), [KB_tests_p2.md](KB_tests_p2.md), [KB_tests_p3.md](KB_tests_p3.md), [KB_tests_p4.md](KB_tests_p4.md), [KB_tests_p5.md](KB_tests_p5.md), [KB_tests_p6.md](KB_tests_p6.md), [KB_tests_p7.md](KB_tests_p7.md), [KB_tests_p8.md](KB_tests_p8.md), [KB_tests_p9.md](KB_tests_p9.md), [KB_tests_p10.md](KB_tests_p10.md), [KB_tests_p11.md](KB_tests_p11.md), [KB_tests_p12.md](KB_tests_p12.md), [KB_tests_p13.md](KB_tests_p13.md), [KB_tests_p14.md](KB_tests_p14.md), [KB_tests_p15.md](KB_tests_p15.md), [KB_tests_p16.md](KB_tests_p16.md), [KB_tests_p17.md](KB_tests_p17.md)

## tests/__init__.py
- Layer: testing
- Language: py

## tests/conftest.py
- Doc: Global pytest isolation hooks.
- Layer: testing
- Language: py
- Symbols:
  - `_isolated_llm_health` (function, line 16) `def _isolated_llm_health(tmp_path, monkeypatch)`
  - `_fast_llm_connect_backoff` (function, line 46) `def _fast_llm_connect_backoff(monkeypatch)`
  - `_reset_world_model_singleton` (function, line 62) `def _reset_world_model_singleton()`
  - `_offline_llm_for_loop_tests` (function, line 72) `def _offline_llm_for_loop_tests(request, monkeypatch)`
  - `_isolated_path` (function, line 32) `def _isolated_path()`
  - `_offline` (function, line 89) `def _offline(model, prompt, max_tokens)`
  - `_HealthyRegistry` (class, line 94) `class _HealthyRegistry`
  - `healthy` (method, line 97) `def healthy(self, name)`
  - `report_failure` (method, line 100) `def report_failure(self, name, reason)`
  - `report_success` (method, line 103) `def report_success(self, name)`
- Depends on: `modules/lazy_agent.py`, `modules/lazy_bridge.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/llm_pool.py`, `modules/loop_ai_bridge.py`, `modules/world_model.py`

## tests/integration_autonomous_flow.py
- Doc: test_autonomous_flow_integration: Simulates a simplified autonomous flow to verify module...
- Layer: testing
- Language: py
- Symbols:
  - `test_autonomous_flow_integration` (function, line 15) `def test_autonomous_flow_integration()`
- Depends on: `modules/moe_router.py`, `modules/obs_parser.py`, `modules/session_rag.py`

## tests/run_mutation_addon_creator.py
- Doc: Manual mutation testing runner for the LazyAddon creator contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 94) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 112) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 125) `def run_tests()`
  - `main` (function, line 140) `def main()`

## tests/run_mutation_addon_updater.py
- Doc: Mutation runner for the lazyaddon update contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 47) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 57) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 64) `def run_tests()`
  - `main` (function, line 76) `def main()`

## tests/run_mutation_api_authz.py
- Doc: Mutation testing runner for core.api_authz and core.logging.
- Layer: presentation
- Language: py
- Symbols:
  - `_apply_mutation` (function, line 64) `def _apply_mutation(source, data)`
  - `_run_mutation_subprocess` (function, line 71) `def _run_mutation_subprocess(test)`
  - `run` (function, line 83) `def run()`

## tests/run_mutation_autonomous_ops.py
- Doc: Manual mutation runner for the LAZY port contracts.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 59) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 69) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 76) `def run_tests()`
  - `main` (function, line 87) `def main()`

## tests/run_mutation_c2_route_auth.py
- Doc: Mutation gate for C2 route-level auth boundaries.
- Layer: presentation
- Language: py
- Symbols:
  - `_run_tests` (function, line 29) `def _run_tests()`
  - `main` (function, line 40) `def main()`

## tests/run_mutation_chain_v2.py
- Doc: Mutation runner for the chain v2 contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 82) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 92) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 99) `def run_tests()`
  - `main` (function, line 111) `def main()`

## tests/run_mutation_contract_manifest.py
- Doc: Mutation gate for the contract manifest drift checker.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 35) `def _run_tests()`
  - `main` (function, line 47) `def main()`

## tests/run_mutation_emulation_runner.py
- Doc: Mutation runner for the emulation-runner contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 54) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 64) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 71) `def run_tests()`
  - `main` (function, line 83) `def main()`

## tests/run_mutation_infra_report.py
- Doc: Mutation runner for the disposable infra and reporting contracts.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 92) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 110) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 122) `def run_tests()`
  - `main` (function, line 137) `def main()`

## tests/run_mutation_killchain.py
- Doc: Manual mutation testing runner for the unified kill-chain contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 56) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 65) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 71) `def run_tests()`
  - `main` (function, line 81) `def main()`

## tests/run_mutation_llm.py
- Doc: Mutation runner for the LLM subsystem contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 60) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 69) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 74) `def run_tests()`
  - `main` (function, line 84) `def main()`

## tests/run_mutation_no_shell.py
- Doc: Mutation gate for the no-shell execution contract.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 25) `def _run_tests()`
  - `main` (function, line 37) `def main()`

## tests/run_mutation_opsec.py
- Doc: Mutation runner for the consolidated OPSEC scorer contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 59) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 68) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 73) `def run_tests()`
  - `main` (function, line 83) `def main()`

## tests/run_mutation_orchestrator_yaml.py
- Doc: Mutation runner for the orchestrator YAML contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 54) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 64) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 71) `def run_tests()`
  - `main` (function, line 83) `def main()`

## tests/run_mutation_outcome_bus.py
- Doc: Mutation runner for the outcome-bus contract.
- Layer: infrastructure
- Language: py
- Symbols:
  - `backup_files` (function, line 47) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 57) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 64) `def run_tests()`
  - `main` (function, line 76) `def main()`

## tests/run_mutation_phase1.py
- Doc: Mutation testing runner for Phase 1 data-gap closure.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 138) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 147) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 153) `def run_tests()`
  - `main` (function, line 164) `def main()`

## tests/run_mutation_shell_semantics.py
- Doc: Mutation gate for shell semantics and colored output.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 41) `def _run_tests()`
  - `main` (function, line 53) `def main()`

## tests/run_mutation_tests.py
- Doc: Manual mutation testing runner for LazyOwn connectivity improvements.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 69) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 78) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 84) `def run_tests()`
  - `main` (function, line 103) `def main()`

## tests/run_mutation_ux_usability.py
- Doc: Mutation testing runner for the UX usability contracts.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 60) `def _run_tests()`
  - `_backups` (function, line 71) `def _backups(mutations)`
  - `_restore` (function, line 79) `def _restore(backups, mutations)`
  - `main` (function, line 84) `def main()`

## tests/test_aci_planner.py
- Doc: tests/test_aci_planner.py
- Layer: testing
- Language: py
- Symbols:
  - `_make_goal` (function, line 33) `def _make_goal()`
  - `_patched_paths` (function, line 47) `def _patched_paths(tmp_path)`
  - `_start_patches` (function, line 60) `def _start_patches(tmp_path)`
  - `_stop_patches` (function, line 77) `def _stop_patches(patchers)`
  - `_make_planner` (function, line 82) `def _make_planner(tmp_path, api_key)`
  - `_make_engine` (function, line 94) `def _make_engine(tmp_path, api_key)`
  - `TestACIGoal` (class, line 111) `class TestACIGoal`
  - `TestAttackPhase` (class, line 134) `class TestAttackPhase`
  - `TestACIPlan` (class, line 177) `class TestACIPlan`
  - `TestACIPlannerStatic` (class, line 244) `class TestACIPlannerStatic`
  - `TestACIPlannerLLM` (class, line 345) `class TestACIPlannerLLM`
  - `TestACIEngineStatus` (class, line 421) `class TestACIEngineStatus`
  - `TestACIEngineShouldReplan` (class, line 462) `class TestACIEngineShouldReplan`
  - `TestACIEngineReplan` (class, line 522) `class TestACIEngineReplan`
  - `TestACIEngineComplete` (class, line 596) `class TestACIEngineComplete`
  - `TestACIReflector` (class, line 626) `class TestACIReflector`
  - `TestMCPBridges` (class, line 723) `class TestMCPBridges`
  - `TestPersistenceHelpers` (class, line 829) `class TestPersistenceHelpers`
  - `TestCLI` (class, line 914) `class TestCLI`
  - `test_fields` (method, line 112) `def test_fields(self)`
  - `test_defaults` (method, line 122) `def test_defaults(self)`
  - `test_to_dict_round_trip` (method, line 135) `def test_to_dict_round_trip(self)`
  - `test_from_dict_ignores_extra_keys` (method, line 154) `def test_from_dict_ignores_extra_keys(self)`
  - `_make_plan` (method, line 178) `def _make_plan(self, phase_statuses)`
  - `test_completion_pct_all_done` (method, line 204) `def test_completion_pct_all_done(self)`
  - `test_completion_pct_none_done` (method, line 208) `def test_completion_pct_none_done(self)`
  - `test_completion_pct_partial` (method, line 212) `def test_completion_pct_partial(self)`
  - `test_active_phase_returns_first_pending_or_active` (method, line 216) `def test_active_phase_returns_first_pending_or_active(self)`
  - `test_active_phase_none_when_all_done` (method, line 221) `def test_active_phase_none_when_all_done(self)`
  - `test_to_dict_has_completion_pct` (method, line 225) `def test_to_dict_has_completion_pct(self)`
  - `test_round_trip` (method, line 231) `def test_round_trip(self)`
  - `test_plan_creates_file` (method, line 245) `def test_plan_creates_file(self, tmp_path)`
  - `test_plan_has_phases` (method, line 252) `def test_plan_has_phases(self, tmp_path)`
  - `test_first_phase_is_active` (method, line 257) `def test_first_phase_is_active(self, tmp_path)`
  - `test_subsequent_phases_are_pending` (method, line 262) `def test_subsequent_phases_are_pending(self, tmp_path)`
  - `test_objectives_injected_into_file` (method, line 268) `def test_objectives_injected_into_file(self, tmp_path)`
  - `test_objectives_ids_match_phase_objectives` (method, line 276) `def test_objectives_ids_match_phase_objectives(self, tmp_path)`
  - `test_phase_filter_restricts_phases` (method, line 287) `def test_phase_filter_restricts_phases(self, tmp_path)`
  - `test_objective_source_is_aci_planner` (method, line 293) `def test_objective_source_is_aci_planner(self, tmp_path)`
  - `test_plan_status_is_active` (method, line 302) `def test_plan_status_is_active(self, tmp_path)`
  - `test_plan_id_is_unique` (method, line 307) `def test_plan_id_is_unique(self, tmp_path)`
  - `test_plan_target_stored` (method, line 313) `def test_plan_target_stored(self, tmp_path)`
  - `test_plan_domain_stored` (method, line 318) `def test_plan_domain_stored(self, tmp_path)`
  - `test_objectives_contain_target_in_text` (method, line 323) `def test_objectives_contain_target_in_text(self, tmp_path)`
  - `test_plan_roundtrip_from_disk` (method, line 330) `def test_plan_roundtrip_from_disk(self, tmp_path)`
  - `_llm_response` (method, line 346) `def _llm_response(self, phases)`
  - `test_llm_phases_used_when_api_key_set` (method, line 355) `def test_llm_phases_used_when_api_key_set(self, tmp_path)`
  - `test_llm_objectives_injected` (method, line 380) `def test_llm_objectives_injected(self, tmp_path)`
  - `test_llm_failure_falls_back_to_static` (method, line 399) `def test_llm_failure_falls_back_to_static(self, tmp_path)`
  - `test_llm_bad_json_falls_back_to_static` (method, line 407) `def test_llm_bad_json_falls_back_to_static(self, tmp_path)`
  - `test_status_no_plan` (method, line 422) `def test_status_no_plan(self, tmp_path)`
  - `test_status_with_plan` (method, line 427) `def test_status_with_plan(self, tmp_path)`
  - `test_status_has_active_phase` (method, line 437) `def test_status_has_active_phase(self, tmp_path)`
  - `test_status_completion_zero_at_start` (method, line 444) `def test_status_completion_zero_at_start(self, tmp_path)`
  - `test_status_blocked_count_zero_at_start` (method, line 451) `def test_status_blocked_count_zero_at_start(self, tmp_path)`
  - `_write_objectives_blocked` (method, line 463) `def _write_objectives_blocked(self, obj_file, obj_ids)`
  - `test_should_replan_false_when_no_plan` (method, line 483) `def test_should_replan_false_when_no_plan(self, tmp_path)`
  - `test_should_replan_false_below_threshold` (method, line 487) `def test_should_replan_false_below_threshold(self, tmp_path)`
  - `test_should_replan_true_at_threshold` (method, line 496) `def test_should_replan_true_at_threshold(self, tmp_path)`
  - `test_should_replan_false_for_completed_plan` (method, line 507) `def test_should_replan_false_for_completed_plan(self, tmp_path)`
  - `test_replan_no_plan` (method, line 523) `def test_replan_no_plan(self, tmp_path)`
  - `test_replan_increments_count` (method, line 529) `def test_replan_increments_count(self, tmp_path)`
  - `test_replan_records_reason` (method, line 536) `def test_replan_records_reason(self, tmp_path)`
  - `test_replan_injects_new_objectives` (method, line 543) `def test_replan_injects_new_objectives(self, tmp_path)`
  - `test_replan_status_returns_to_active` (method, line 553) `def test_replan_status_returns_to_active(self, tmp_path)`
  - `test_replan_twice_counts_two` (method, line 560) `def test_replan_twice_counts_two(self, tmp_path)`
  - `test_replan_with_llm` (method, line 568) `def test_replan_with_llm(self, tmp_path)`
  - `test_complete_archives_plan` (method, line 597) `def test_complete_archives_plan(self, tmp_path)`
  - `test_complete_marks_plan_as_completed` (method, line 607) `def test_complete_marks_plan_as_completed(self, tmp_path)`
  - `test_complete_no_plan` (method, line 617) `def test_complete_no_plan(self, tmp_path)`
  - `_make_plan_with_statuses` (method, line 627) `def _make_plan_with_statuses(self, phase_statuses, replan_count)`
  - `test_reflect_blocked_phase_generates_lesson` (method, line 655) `def test_reflect_blocked_phase_generates_lesson(self, tmp_path)`
  - `test_reflect_done_after_replan_generates_lesson` (method, line 665) `def test_reflect_done_after_replan_generates_lesson(self, tmp_path)`
  - `test_reflect_no_lessons_clean_plan` (method, line 674) `def test_reflect_no_lessons_clean_plan(self, tmp_path)`
  - `test_reflect_persists_to_file` (method, line 683) `def test_reflect_persists_to_file(self, tmp_path)`
  - `test_reflect_lesson_has_required_fields` (method, line 698) `def test_reflect_lesson_has_required_fields(self, tmp_path)`
  - `test_mcp_aci_status_no_plan` (method, line 724) `def test_mcp_aci_status_no_plan(self, tmp_path)`
  - `test_mcp_aci_plan_returns_json` (method, line 734) `def test_mcp_aci_plan_returns_json(self, tmp_path)`
  - `test_mcp_aci_plan_uses_rhost_from_payload` (method, line 747) `def test_mcp_aci_plan_uses_rhost_from_payload(self, tmp_path)`
  - `test_mcp_aci_plan_static_backend` (method, line 758) `def test_mcp_aci_plan_static_backend(self, tmp_path)`
  - `test_mcp_aci_replan_no_plan` (method, line 769) `def test_mcp_aci_replan_no_plan(self, tmp_path)`
  - `test_mcp_aci_replan_with_plan` (method, line 780) `def test_mcp_aci_replan_with_plan(self, tmp_path)`
  - `test_mcp_aci_status_after_plan` (method, line 793) `def test_mcp_aci_status_after_plan(self, tmp_path)`
  - `test_mcp_aci_plan_phase_filter` (method, line 806) `def test_mcp_aci_plan_phase_filter(self, tmp_path)`
  - `test_save_load_plan_roundtrip` (method, line 830) `def test_save_load_plan_roundtrip(self, tmp_path)`
  - `test_load_plan_returns_none_for_missing` (method, line 845) `def test_load_plan_returns_none_for_missing(self, tmp_path)`
  - `test_load_plan_returns_none_for_corrupt` (method, line 851) `def test_load_plan_returns_none_for_corrupt(self, tmp_path)`
  - `test_archive_plan_appends` (method, line 859) `def test_archive_plan_appends(self, tmp_path)`
  - `test_count_objectives_by_status` (method, line 876) `def test_count_objectives_by_status(self, tmp_path)`
  - `test_count_objectives_returns_empty_for_missing_file` (method, line 904) `def test_count_objectives_returns_empty_for_missing_file(self, tmp_path)`
  - `test_plan_command` (method, line 915) `def test_plan_command(self, tmp_path)`
  - `test_status_command_no_plan` (method, line 926) `def test_status_command_no_plan(self, tmp_path, capsys)`
  - `test_replan_command_no_plan` (method, line 940) `def test_replan_command_no_plan(self, tmp_path, capsys)`
  - `test_no_subcommand_returns_nonzero` (method, line 954) `def test_no_subcommand_returns_nonzero(self, tmp_path)`
  - `test_reflect_command_no_plan` (method, line 960) `def test_reflect_command_no_plan(self, tmp_path, capsys)`
- Depends on: `skills/aci_planner.py`

## tests/test_addon_creator.py
- Doc: Tests for the LazyAddon creator contract and C2 blueprint.
- Layer: testing
- Language: py
- Symbols:
  - `_valid_draft` (function, line 45) `def _valid_draft()`
  - `TestConfig` (class, line 86) `class TestConfig`
  - `TestValidator` (class, line 117) `class TestValidator`
  - `TestYamlRenderer` (class, line 263) `class TestYamlRenderer`
  - `TestAddonStore` (class, line 328) `class TestAddonStore`
  - `TestParseAddonForm` (class, line 460) `class TestParseAddonForm`
  - `_build_test_app` (function, line 521) `def _build_test_app(tmp_path)`
  - `_login` (function, line 585) `def _login(client)`
  - `TestBlueprint` (class, line 591) `class TestBlueprint`
  - `TestTemplateSanity` (class, line 805) `class TestTemplateSanity`
  - `test_name_pattern_rejects_traversal` (method, line 89) `def test_name_pattern_rejects_traversal(self)`
  - `test_patterns_accept_canonical_values` (method, line 96) `def test_patterns_accept_canonical_values(self)`
  - `test_os_options_cover_mitre_platforms` (method, line 105) `def test_os_options_cover_mitre_platforms(self)`
  - `test_payload_placeholders_cover_core_keys` (method, line 111) `def test_payload_placeholders_cover_core_keys(self)`
  - `test_valid_draft_has_no_issues` (method, line 120) `def test_valid_draft_has_no_issues(self)`
  - `test_missing_name_reports_issue` (method, line 125) `def test_missing_name_reports_issue(self)`
  - `test_invalid_name_reports_issue` (method, line 131) `def test_invalid_name_reports_issue(self)`
  - `test_missing_description_reports_issue` (method, line 138) `def test_missing_description_reports_issue(self)`
  - `test_unknown_os_reports_issue` (method, line 144) `def test_unknown_os_reports_issue(self)`
  - `test_unknown_module_type_reports_issue` (method, line 150) `def test_unknown_module_type_reports_issue(self)`
  - `test_malformed_category_reports_issue` (method, line 156) `def test_malformed_category_reports_issue(self)`
  - `test_uppercase_trigger_reports_issue` (method, line 162) `def test_uppercase_trigger_reports_issue(self)`
  - `test_missing_execute_command_reports_issue` (method, line 168) `def test_missing_execute_command_reports_issue(self)`
  - `test_unknown_placeholder_reports_issue` (method, line 174) `def test_unknown_placeholder_reports_issue(self)`
  - `test_nested_brace_placeholder_reports_issue` (method, line 180) `def test_nested_brace_placeholder_reports_issue(self)`
  - `test_declared_param_placeholder_is_allowed` (method, line 186) `def test_declared_param_placeholder_is_allowed(self)`
  - `test_install_path_without_repo_url_reports_issue` (method, line 192) `def test_install_path_without_repo_url_reports_issue(self)`
  - `test_traversal_install_path_reports_issue` (method, line 198) `def test_traversal_install_path_reports_issue(self)`
  - `test_bad_repo_url_reports_issue` (method, line 205) `def test_bad_repo_url_reports_issue(self)`
  - `test_duplicate_param_reports_issue` (method, line 212) `def test_duplicate_param_reports_issue(self)`
  - `test_param_without_description_reports_issue` (method, line 218) `def test_param_without_description_reports_issue(self)`
  - `test_integer_default_must_parse` (method, line 224) `def test_integer_default_must_parse(self)`
  - `test_boolean_default_whitelist` (method, line 232) `def test_boolean_default_whitelist(self)`
  - `test_too_many_params_reports_issue` (method, line 240) `def test_too_many_params_reports_issue(self)`
  - `test_malformed_env_entry_reports_issue` (method, line 249) `def test_malformed_env_entry_reports_issue(self)`
  - `test_validation_error_carries_issues` (method, line 255) `def test_validation_error_carries_issues(self)`
  - `test_rendered_document_is_canonical` (method, line 266) `def test_rendered_document_is_canonical(self)`
  - `test_yaml_round_trips_through_loader` (method, line 286) `def test_yaml_round_trips_through_loader(self)`
  - `test_optional_fields_are_dropped` (method, line 295) `def test_optional_fields_are_dropped(self)`
  - `test_rendered_yaml_has_no_none_values` (method, line 310) `def test_rendered_yaml_has_no_none_values(self)`
  - `test_default_author_and_version_applied` (method, line 315) `def test_default_author_and_version_applied(self)`
  - `test_save_load_delete_round_trip` (method, line 331) `def test_save_load_delete_round_trip(self, tmp_path)`
  - `test_traversal_name_rejected_on_save` (method, line 342) `def test_traversal_name_rejected_on_save(self, tmp_path)`
  - `test_traversal_name_rejected_on_load` (method, line 347) `def test_traversal_name_rejected_on_load(self, tmp_path)`
  - `test_traversal_name_rejected_on_delete` (method, line 352) `def test_traversal_name_rejected_on_delete(self, tmp_path)`
  - `test_save_is_atomic_and_leaves_no_temp_files` (method, line 357) `def test_save_is_atomic_and_leaves_no_temp_files(self, tmp_path)`
  - `test_save_overwrites_cleanly` (method, line 363) `def test_save_overwrites_cleanly(self, tmp_path)`
  - `test_load_missing_raises_file_not_found` (method, line 369) `def test_load_missing_raises_file_not_found(self, tmp_path)`
  - `test_list_all_skips_broken_files` (method, line 374) `def test_list_all_skips_broken_files(self, tmp_path)`
  - `test_list_all_is_sorted_and_has_expected_keys` (method, line 383) `def test_list_all_is_sorted_and_has_expected_keys(self, tmp_path)`
  - `test_list_all_reports_file_stem_as_filename` (method, line 400) `def test_list_all_reports_file_stem_as_filename(self, tmp_path)`
  - `test_load_accepts_pre_existing_uppercase_names` (method, line 407) `def test_load_accepts_pre_existing_uppercase_names(self, tmp_path)`
  - `test_load_accepts_pre_existing_dots_and_hyphens` (method, line 413) `def test_load_accepts_pre_existing_dots_and_hyphens(self, tmp_path)`
  - `test_load_still_rejects_traversal_through_existing_path` (method, line 419) `def test_load_still_rejects_traversal_through_existing_path(self, tmp_path)`
  - `test_delete_rejects_unsafe_existing_names` (method, line 425) `def test_delete_rejects_unsafe_existing_names(self, tmp_path)`
  - `test_missing_directory_lists_empty` (method, line 430) `def test_missing_directory_lists_empty(self, tmp_path)`
  - `test_exists_swallows_invalid_names` (method, line 434) `def test_exists_swallows_invalid_names(self, tmp_path)`
  - `test_symlink_escape_rejected_on_load` (method, line 438) `def test_symlink_escape_rejected_on_load(self, tmp_path)`
  - `test_symlink_escape_rejected_on_delete` (method, line 448) `def test_symlink_escape_rejected_on_delete(self, tmp_path)`
  - `test_parse_complete_form` (method, line 463) `def test_parse_complete_form(self)`
  - `test_unchecked_enabled_becomes_false` (method, line 505) `def test_unchecked_enabled_becomes_false(self)`
  - `test_missing_optional_fields_become_empty` (method, line 509) `def test_missing_optional_fields_become_empty(self)`
  - `test_single_trigger_string_becomes_list` (method, line 516) `def test_single_trigger_string_becomes_list(self)`
  - `_FakeOperator` (class, line 570) `class _FakeOperator(UserMixin)`
  - `_load_user` (function, line 577) `def _load_user(user_id)`
  - `test_unauthenticated_access_redirects_to_login` (method, line 594) `def test_unauthenticated_access_redirects_to_login(self, tmp_path)`
  - `test_create_form_issues_csrf_cookie` (method, line 602) `def test_create_form_issues_csrf_cookie(self, tmp_path)`
  - `test_post_without_csrf_is_rejected` (method, line 612) `def test_post_without_csrf_is_rejected(self, tmp_path)`
  - `test_delete_without_csrf_is_rejected` (method, line 619) `def test_delete_without_csrf_is_rejected(self, tmp_path)`
  - `_form_data` (method, line 626) `def _form_data(self)`
  - `_csrf_token` (method, line 650) `def _csrf_token(self, client)`
  - `test_valid_post_creates_addon_and_redirects` (method, line 660) `def test_valid_post_creates_addon_and_redirects(self, tmp_path)`
  - `test_invalid_post_rerenders_with_field_errors` (method, line 673) `def test_invalid_post_rerenders_with_field_errors(self, tmp_path)`
  - `test_duplicate_name_rerenders_with_error` (method, line 685) `def test_duplicate_name_rerenders_with_error(self, tmp_path)`
  - `test_view_page_renders_yaml` (method, line 698) `def test_view_page_renders_yaml(self, tmp_path)`
  - `test_list_page_shows_created_addon` (method, line 710) `def test_list_page_shows_created_addon(self, tmp_path)`
  - `test_delete_removes_addon` (method, line 722) `def test_delete_removes_addon(self, tmp_path)`
  - `test_delete_unknown_addon_flashes_and_redirects` (method, line 734) `def test_delete_unknown_addon_flashes_and_redirects(self, tmp_path)`
  - `test_view_unknown_addon_redirects_to_list` (method, line 744) `def test_view_unknown_addon_redirects_to_list(self, tmp_path)`
  - `test_view_legacy_uppercase_addon_renders` (method, line 751) `def test_view_legacy_uppercase_addon_renders(self, tmp_path)`
  - `test_list_page_links_by_filename_for_legacy_names` (method, line 764) `def test_list_page_links_by_filename_for_legacy_names(self, tmp_path)`
  - `test_delete_legacy_uppercase_addon` (method, line 774) `def test_delete_legacy_uppercase_addon(self, tmp_path)`
  - `test_rendered_addon_passes_cli_schema_contract` (method, line 786) `def test_rendered_addon_passes_cli_schema_contract(self, tmp_path)`
  - `test_creator_template_has_help_affordances` (method, line 808) `def test_creator_template_has_help_affordances(self)`
  - `test_creator_template_forbids_emojis_and_console_spam` (method, line 816) `def test_creator_template_forbids_emojis_and_console_spam(self)`
  - `test_tools_creator_template_has_no_broken_js` (method, line 821) `def test_tools_creator_template_has_no_broken_js(self)`
- Depends on: `lazyc2/addon_creator.py`, `lazyc2/blueprints/addons.py`

## tests/test_addon_updater.py
- Doc: Lazyaddon update BDD contract: opt-in, path-safe, dirty-tree aware.
- Layer: testing
- Language: py
- Symbols:
  - `_git` (function, line 17) `def _git(cwd)`
  - `_repo_with_remote` (function, line 29) `def _repo_with_remote(tmp_path)`
  - `_addon` (function, line 46) `def _addon(path)`
  - `test_every_shipped_addon_opts_in` (function, line 62) `def test_every_shipped_addon_opts_in()`
  - `test_update_disabled_is_skipped` (function, line 69) `def test_update_disabled_is_skipped(tmp_path)`
  - `test_missing_repo_url_is_skipped` (function, line 77) `def test_missing_repo_url_is_skipped(tmp_path)`
  - `test_path_traversal_is_rejected` (function, line 85) `def test_path_traversal_is_rejected(tmp_path)`
  - `test_repository_root_is_rejected` (function, line 93) `def test_repository_root_is_rejected(tmp_path)`
  - `test_not_installed_is_skipped` (function, line 101) `def test_not_installed_is_skipped(tmp_path)`
  - `test_fast_forward_update` (function, line 109) `def test_fast_forward_update(tmp_path)`
  - `test_dirty_worktree_is_skipped` (function, line 124) `def test_dirty_worktree_is_skipped(tmp_path)`
  - `test_update_all_audits_summary` (function, line 134) `def test_update_all_audits_summary(tmp_path)`
  - `test_unknown_addon_fails` (function, line 146) `def test_unknown_addon_fails(tmp_path)`
- Depends on: `modules/addon_updater.py`

## tests/test_aes_key_propagation.py
- Doc: TDD tests for the AES key resolution contract.
- Layer: testing
- Language: py
- Symbols:
  - `TestHexSource` (class, line 32) `class TestHexSource`
  - `TestDiskSource` (class, line 57) `class TestDiskSource`
  - `TestGeneratedSource` (class, line 67) `class TestGeneratedSource`
  - `TestConfigExposesKey` (class, line 83) `class TestConfigExposesKey`
  - `test_valid_hex_decodes_to_32_bytes` (method, line 35) `def test_valid_hex_decodes_to_32_bytes(self)`
  - `test_wrong_length_raises` (method, line 42) `def test_wrong_length_raises(self)`
  - `test_non_hex_raises` (method, line 49) `def test_non_hex_raises(self)`
  - `test_existing_disk_key_is_loaded` (method, line 60) `def test_existing_disk_key_is_loaded(self, tmp_path)`
  - `test_generated_key_is_32_bytes` (method, line 70) `def test_generated_key_is_32_bytes(self, tmp_path)`
  - `test_generated_key_is_persisted` (method, line 75) `def test_generated_key_is_persisted(self, tmp_path)`
  - `test_config_has_aes_key_attribute` (method, line 86) `def test_config_has_aes_key_attribute(self)`
  - `test_config_exposes_params_dict` (method, line 91) `def test_config_exposes_params_dict(self)`
- Depends on: `core/config.py`

## tests/test_ai_commands_llm.py
- Doc: Behavioural tests for the resurrected ``ask``/``groq`` commands.
- Layer: testing
- Language: py
- Symbols:
  - `_command_set` (function, line 17) `def _command_set()`
  - `TestDoAsk` (class, line 26) `class TestDoAsk`
  - `TestDoGroq` (class, line 53) `class TestDoGroq`
  - `test_empty_question_prints_usage` (method, line 27) `def test_empty_question_prints_usage(self, monkeypatch)`
  - `test_question_forwarded_with_session_context` (method, line 33) `def test_question_forwarded_with_session_context(self, monkeypatch)`
  - `test_backend_error_surfaces_as_message` (method, line 45) `def test_backend_error_surfaces_as_message(self, monkeypatch)`
  - `test_unavailable_backend_prints_actionable_error` (method, line 54) `def test_unavailable_backend_prints_actionable_error(self, monkeypatch)`
  - `test_success_completes_oneliner_and_prints` (method, line 66) `def test_success_completes_oneliner_and_prints(self, monkeypatch)`
  - `test_completion_failure_prints_error` (method, line 90) `def test_completion_failure_prints_error(self, monkeypatch)`
  - `test_empty_line_falls_back_to_shell_prompt` (method, line 103) `def test_empty_line_falls_back_to_shell_prompt(self, monkeypatch)`
  - `_raise` (function, line 57) `def _raise()`
  - `_Backend` (class, line 71) `class _Backend`
  - `_factory` (function, line 77) `def _factory()`
  - `_Backend` (class, line 93) `class _Backend`
  - `_Backend` (class, line 106) `class _Backend`
  - `complete` (method, line 72) `def complete(self, system, user)`
  - `complete` (method, line 94) `def complete(self, system, user)`
  - `complete` (method, line 107) `def complete(self, system, user)`
- Depends on: `cli/commands/ai.py`, `modules/llm_factory.py`


Next: [KB_tests_p2.md](KB_tests_p2.md)
