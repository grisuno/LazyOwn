# Subsystem: tests (page 1 of 14)
Pages: [KB_tests.md](KB_tests.md), [KB_tests_p2.md](KB_tests_p2.md), [KB_tests_p3.md](KB_tests_p3.md), [KB_tests_p4.md](KB_tests_p4.md), [KB_tests_p5.md](KB_tests_p5.md), [KB_tests_p6.md](KB_tests_p6.md), [KB_tests_p7.md](KB_tests_p7.md), [KB_tests_p8.md](KB_tests_p8.md), [KB_tests_p9.md](KB_tests_p9.md), [KB_tests_p10.md](KB_tests_p10.md), [KB_tests_p11.md](KB_tests_p11.md), [KB_tests_p12.md](KB_tests_p12.md), [KB_tests_p13.md](KB_tests_p13.md), [KB_tests_p14.md](KB_tests_p14.md)

## tests/__init__.py
- Layer: testing
- Language: py

## tests/conftest.py
- Doc: Global pytest isolation hooks.
- Layer: testing
- Language: py
- Symbols:
  - `_reset_world_model_singleton` (function, line 16) `def _reset_world_model_singleton()`
- Depends on: `modules/world_model.py`

## tests/integration_autonomous_flow.py
- Doc: test_autonomous_flow_integration: Simulates a simplified autonomous flow to verify module...
- Layer: testing
- Language: py
- Symbols:
  - `test_autonomous_flow_integration` (function, line 15) `def test_autonomous_flow_integration()`
- Depends on: `modules/moe_router.py`, `modules/obs_parser.py`, `modules/session_rag.py`, `modules/world_model.py`

## tests/run_mutation_addon_creator.py
- Doc: Manual mutation testing runner for the LazyAddon creator contract.
- Layer: testing
- Language: py
- Symbols:
  - `backup_files` (function, line 94) `def backup_files(mutations, base_dir)`
  - `restore_files` (function, line 112) `def restore_files(backups, base_dir, mutations)`
  - `run_tests` (function, line 125) `def run_tests()`
  - `main` (function, line 140) `def main()`

## tests/run_mutation_api_authz.py
- Doc: Mutation testing runner for core.api_authz and core.logging.
- Layer: presentation
- Language: py
- Symbols:
  - `_apply_mutation` (function, line 64) `def _apply_mutation(source, data)`
  - `_run_mutation_subprocess` (function, line 71) `def _run_mutation_subprocess(test)`
  - `run` (function, line 83) `def run()`

## tests/run_mutation_c2_route_auth.py
- Doc: Mutation gate for C2 route-level auth boundaries.
- Layer: presentation
- Language: py
- Symbols:
  - `_run_tests` (function, line 29) `def _run_tests()`
  - `main` (function, line 40) `def main()`

## tests/run_mutation_contract_manifest.py
- Doc: Mutation gate for the contract manifest drift checker.
- Layer: testing
- Language: py
- Symbols:
  - `_run_tests` (function, line 35) `def _run_tests()`
  - `main` (function, line 47) `def main()`

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
  - `main` (function, line 100) `def main()`

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
  - `_make_goal` (function, line 32) `def _make_goal()`
  - `_patched_paths` (function, line 40) `def _patched_paths(tmp_path)`
  - `_start_patches` (function, line 53) `def _start_patches(tmp_path)`
  - `_stop_patches` (function, line 69) `def _stop_patches(patchers)`
  - `_make_planner` (function, line 74) `def _make_planner(tmp_path, api_key)`
  - `_make_engine` (function, line 85) `def _make_engine(tmp_path, api_key)`
  - `TestACIGoal` (class, line 100) `class TestACIGoal`
  - `TestAttackPhase` (class, line 121) `class TestAttackPhase`
  - `TestACIPlan` (class, line 162) `class TestACIPlan`
  - `TestACIPlannerStatic` (class, line 226) `class TestACIPlannerStatic`
  - `TestACIPlannerLLM` (class, line 325) `class TestACIPlannerLLM`
  - `TestACIEngineStatus` (class, line 400) `class TestACIEngineStatus`
  - `TestACIEngineShouldReplan` (class, line 440) `class TestACIEngineShouldReplan`
  - `TestACIEngineReplan` (class, line 488) `class TestACIEngineReplan`
  - `TestACIEngineComplete` (class, line 561) `class TestACIEngineComplete`
  - `TestACIReflector` (class, line 589) `class TestACIReflector`
  - `TestMCPBridges` (class, line 670) `class TestMCPBridges`
  - `TestPersistenceHelpers` (class, line 764) `class TestPersistenceHelpers`
  - `TestCLI` (class, line 831) `class TestCLI`
  - `test_fields` (method, line 101) `def test_fields(self)`
  - `test_defaults` (method, line 111) `def test_defaults(self)`
  - `test_to_dict_round_trip` (method, line 122) `def test_to_dict_round_trip(self)`
  - `test_from_dict_ignores_extra_keys` (method, line 140) `def test_from_dict_ignores_extra_keys(self)`
  - `_make_plan` (method, line 163) `def _make_plan(self, phase_statuses)`
  - `test_completion_pct_all_done` (method, line 188) `def test_completion_pct_all_done(self)`
  - `test_completion_pct_none_done` (method, line 192) `def test_completion_pct_none_done(self)`
  - `test_completion_pct_partial` (method, line 196) `def test_completion_pct_partial(self)`
  - `test_active_phase_returns_first_pending_or_active` (method, line 200) `def test_active_phase_returns_first_pending_or_active(self)`
  - `test_active_phase_none_when_all_done` (method, line 205) `def test_active_phase_none_when_all_done(self)`
  - `test_to_dict_has_completion_pct` (method, line 209) `def test_to_dict_has_completion_pct(self)`
  - `test_round_trip` (method, line 215) `def test_round_trip(self)`
  - `test_plan_creates_file` (method, line 227) `def test_plan_creates_file(self, tmp_path)`
  - `test_plan_has_phases` (method, line 234) `def test_plan_has_phases(self, tmp_path)`
  - `test_first_phase_is_active` (method, line 239) `def test_first_phase_is_active(self, tmp_path)`
  - `test_subsequent_phases_are_pending` (method, line 244) `def test_subsequent_phases_are_pending(self, tmp_path)`
  - `test_objectives_injected_into_file` (method, line 250) `def test_objectives_injected_into_file(self, tmp_path)`
  - `test_objectives_ids_match_phase_objectives` (method, line 258) `def test_objectives_ids_match_phase_objectives(self, tmp_path)`
  - `test_phase_filter_restricts_phases` (method, line 269) `def test_phase_filter_restricts_phases(self, tmp_path)`
  - `test_objective_source_is_aci_planner` (method, line 275) `def test_objective_source_is_aci_planner(self, tmp_path)`
  - `test_plan_status_is_active` (method, line 284) `def test_plan_status_is_active(self, tmp_path)`
  - `test_plan_id_is_unique` (method, line 289) `def test_plan_id_is_unique(self, tmp_path)`
  - `test_plan_target_stored` (method, line 295) `def test_plan_target_stored(self, tmp_path)`
  - `test_plan_domain_stored` (method, line 300) `def test_plan_domain_stored(self, tmp_path)`
  - `test_objectives_contain_target_in_text` (method, line 305) `def test_objectives_contain_target_in_text(self, tmp_path)`
  - `test_plan_roundtrip_from_disk` (method, line 312) `def test_plan_roundtrip_from_disk(self, tmp_path)`
  - `_llm_response` (method, line 326) `def _llm_response(self, phases)`
  - `test_llm_phases_used_when_api_key_set` (method, line 335) `def test_llm_phases_used_when_api_key_set(self, tmp_path)`
  - `test_llm_objectives_injected` (method, line 360) `def test_llm_objectives_injected(self, tmp_path)`
  - `test_llm_failure_falls_back_to_static` (method, line 379) `def test_llm_failure_falls_back_to_static(self, tmp_path)`
  - `test_llm_bad_json_falls_back_to_static` (method, line 387) `def test_llm_bad_json_falls_back_to_static(self, tmp_path)`
  - `test_status_no_plan` (method, line 401) `def test_status_no_plan(self, tmp_path)`
  - `test_status_with_plan` (method, line 406) `def test_status_with_plan(self, tmp_path)`
  - `test_status_has_active_phase` (method, line 416) `def test_status_has_active_phase(self, tmp_path)`
  - `test_status_completion_zero_at_start` (method, line 423) `def test_status_completion_zero_at_start(self, tmp_path)`
  - `test_status_blocked_count_zero_at_start` (method, line 430) `def test_status_blocked_count_zero_at_start(self, tmp_path)`
  - `_write_objectives_blocked` (method, line 441) `def _write_objectives_blocked(self, obj_file, obj_ids)`
  - `test_should_replan_false_when_no_plan` (method, line 451) `def test_should_replan_false_when_no_plan(self, tmp_path)`
  - `test_should_replan_false_below_threshold` (method, line 455) `def test_should_replan_false_below_threshold(self, tmp_path)`
  - `test_should_replan_true_at_threshold` (method, line 464) `def test_should_replan_true_at_threshold(self, tmp_path)`
  - `test_should_replan_false_for_completed_plan` (method, line 475) `def test_should_replan_false_for_completed_plan(self, tmp_path)`
  - `test_replan_no_plan` (method, line 489) `def test_replan_no_plan(self, tmp_path)`
  - `test_replan_increments_count` (method, line 495) `def test_replan_increments_count(self, tmp_path)`
  - `test_replan_records_reason` (method, line 502) `def test_replan_records_reason(self, tmp_path)`
  - `test_replan_injects_new_objectives` (method, line 509) `def test_replan_injects_new_objectives(self, tmp_path)`
  - `test_replan_status_returns_to_active` (method, line 519) `def test_replan_status_returns_to_active(self, tmp_path)`
  - `test_replan_twice_counts_two` (method, line 526) `def test_replan_twice_counts_two(self, tmp_path)`
  - `test_replan_with_llm` (method, line 534) `def test_replan_with_llm(self, tmp_path)`
  - `test_complete_archives_plan` (method, line 562) `def test_complete_archives_plan(self, tmp_path)`
  - `test_complete_marks_plan_as_completed` (method, line 572) `def test_complete_marks_plan_as_completed(self, tmp_path)`
  - `test_complete_no_plan` (method, line 581) `def test_complete_no_plan(self, tmp_path)`
  - `_make_plan_with_statuses` (method, line 590) `def _make_plan_with_statuses(self, phase_statuses, replan_count)`
  - `test_reflect_blocked_phase_generates_lesson` (method, line 617) `def test_reflect_blocked_phase_generates_lesson(self, tmp_path)`
  - `test_reflect_done_after_replan_generates_lesson` (method, line 626) `def test_reflect_done_after_replan_generates_lesson(self, tmp_path)`
  - `test_reflect_no_lessons_clean_plan` (method, line 634) `def test_reflect_no_lessons_clean_plan(self, tmp_path)`
  - `test_reflect_persists_to_file` (method, line 642) `def test_reflect_persists_to_file(self, tmp_path)`
  - `test_reflect_lesson_has_required_fields` (method, line 656) `def test_reflect_lesson_has_required_fields(self, tmp_path)`
  - `test_mcp_aci_status_no_plan` (method, line 671) `def test_mcp_aci_status_no_plan(self, tmp_path)`
  - `test_mcp_aci_plan_returns_json` (method, line 680) `def test_mcp_aci_plan_returns_json(self, tmp_path)`
  - `test_mcp_aci_plan_uses_rhost_from_payload` (method, line 692) `def test_mcp_aci_plan_uses_rhost_from_payload(self, tmp_path)`
  - `test_mcp_aci_plan_static_backend` (method, line 702) `def test_mcp_aci_plan_static_backend(self, tmp_path)`
  - `test_mcp_aci_replan_no_plan` (method, line 712) `def test_mcp_aci_replan_no_plan(self, tmp_path)`
  - `test_mcp_aci_replan_with_plan` (method, line 722) `def test_mcp_aci_replan_with_plan(self, tmp_path)`
  - `test_mcp_aci_status_after_plan` (method, line 734) `def test_mcp_aci_status_after_plan(self, tmp_path)`
  - `test_mcp_aci_plan_phase_filter` (method, line 746) `def test_mcp_aci_plan_phase_filter(self, tmp_path)`
  - `test_save_load_plan_roundtrip` (method, line 765) `def test_save_load_plan_roundtrip(self, tmp_path)`
  - `test_load_plan_returns_none_for_missing` (method, line 779) `def test_load_plan_returns_none_for_missing(self, tmp_path)`
  - `test_load_plan_returns_none_for_corrupt` (method, line 784) `def test_load_plan_returns_none_for_corrupt(self, tmp_path)`
  - `test_archive_plan_appends` (method, line 791) `def test_archive_plan_appends(self, tmp_path)`
  - `test_count_objectives_by_status` (method, line 807) `def test_count_objectives_by_status(self, tmp_path)`
  - `test_count_objectives_returns_empty_for_missing_file` (method, line 823) `def test_count_objectives_returns_empty_for_missing_file(self, tmp_path)`
  - `test_plan_command` (method, line 832) `def test_plan_command(self, tmp_path)`
  - `test_status_command_no_plan` (method, line 842) `def test_status_command_no_plan(self, tmp_path, capsys)`
  - `test_replan_command_no_plan` (method, line 855) `def test_replan_command_no_plan(self, tmp_path, capsys)`
  - `test_no_subcommand_returns_nonzero` (method, line 868) `def test_no_subcommand_returns_nonzero(self, tmp_path)`
  - `test_reflect_command_no_plan` (method, line 873) `def test_reflect_command_no_plan(self, tmp_path, capsys)`
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
  - `_build_test_app` (method, line 521) `def _build_test_app(tmp_path)`
  - `_login` (method, line 581) `def _login(client)`
  - `TestBlueprint` (class, line 587) `class TestBlueprint`
  - `TestTemplateSanity` (class, line 801) `class TestTemplateSanity`
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
  - `_FakeOperator` (class, line 566) `class _FakeOperator(UserMixin)`
  - `_load_user` (method, line 573) `def _load_user(user_id)`
  - `test_unauthenticated_access_redirects_to_login` (method, line 590) `def test_unauthenticated_access_redirects_to_login(self, tmp_path)`
  - `test_create_form_issues_csrf_cookie` (method, line 598) `def test_create_form_issues_csrf_cookie(self, tmp_path)`
  - `test_post_without_csrf_is_rejected` (method, line 608) `def test_post_without_csrf_is_rejected(self, tmp_path)`
  - `test_delete_without_csrf_is_rejected` (method, line 615) `def test_delete_without_csrf_is_rejected(self, tmp_path)`
  - `_form_data` (method, line 622) `def _form_data(self)`
  - `_csrf_token` (method, line 646) `def _csrf_token(self, client)`
  - `test_valid_post_creates_addon_and_redirects` (method, line 656) `def test_valid_post_creates_addon_and_redirects(self, tmp_path)`
  - `test_invalid_post_rerenders_with_field_errors` (method, line 669) `def test_invalid_post_rerenders_with_field_errors(self, tmp_path)`
  - `test_duplicate_name_rerenders_with_error` (method, line 681) `def test_duplicate_name_rerenders_with_error(self, tmp_path)`
  - `test_view_page_renders_yaml` (method, line 694) `def test_view_page_renders_yaml(self, tmp_path)`
  - `test_list_page_shows_created_addon` (method, line 706) `def test_list_page_shows_created_addon(self, tmp_path)`
  - `test_delete_removes_addon` (method, line 718) `def test_delete_removes_addon(self, tmp_path)`
  - `test_delete_unknown_addon_flashes_and_redirects` (method, line 730) `def test_delete_unknown_addon_flashes_and_redirects(self, tmp_path)`
  - `test_view_unknown_addon_redirects_to_list` (method, line 740) `def test_view_unknown_addon_redirects_to_list(self, tmp_path)`
  - `test_view_legacy_uppercase_addon_renders` (method, line 747) `def test_view_legacy_uppercase_addon_renders(self, tmp_path)`
  - `test_list_page_links_by_filename_for_legacy_names` (method, line 760) `def test_list_page_links_by_filename_for_legacy_names(self, tmp_path)`
  - `test_delete_legacy_uppercase_addon` (method, line 770) `def test_delete_legacy_uppercase_addon(self, tmp_path)`
  - `test_rendered_addon_passes_cli_schema_contract` (method, line 782) `def test_rendered_addon_passes_cli_schema_contract(self, tmp_path)`
  - `test_creator_template_has_help_affordances` (method, line 804) `def test_creator_template_has_help_affordances(self)`
  - `test_creator_template_forbids_emojis_and_console_spam` (method, line 812) `def test_creator_template_forbids_emojis_and_console_spam(self)`
  - `test_tools_creator_template_has_no_broken_js` (method, line 817) `def test_tools_creator_template_has_no_broken_js(self)`
- Depends on: `lazyc2/addon_creator.py`, `lazyc2/blueprints/addons.py`

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
  - `_raise` (method, line 57) `def _raise()`
  - `_Backend` (class, line 71) `class _Backend`
  - `_factory` (method, line 77) `def _factory()`
  - `_Backend` (class, line 93) `class _Backend`
  - `_Backend` (class, line 106) `class _Backend`
  - `complete` (method, line 72) `def complete(self, system, user)`
  - `complete` (method, line 94) `def complete(self, system, user)`
  - `complete` (method, line 107) `def complete(self, system, user)`
- Depends on: `cli/commands/ai.py`, `modules/llm_factory.py`

## tests/test_api_authz.py
- Doc: Tests for ``core.api_authz`` — tenant-bound API authorization.
- Layer: testing
- Language: py
- Symbols:
  - `TestApiAuthzConfig` (class, line 21) `class TestApiAuthzConfig`
  - `TestApiKey` (class, line 45) `class TestApiKey`
  - `TestApiKeyStore` (class, line 96) `class TestApiKeyStore`
  - `TestRequireApiAuth` (class, line 271) `class TestRequireApiAuth`
  - `TestCreateApiToken` (class, line 356) `class TestCreateApiToken`
  - `TestEdgeCases` (class, line 397) `class TestEdgeCases`
  - `test_defaults_are_secure_by_default` (method, line 24) `def test_defaults_are_secure_by_default(self)`
  - `test_custom_overrides_preserve_typed_semantics` (method, line 32) `def test_custom_overrides_preserve_typed_semantics(self)`
  - `test_serialization_roundtrip_preserves_all_fields` (method, line 48) `def test_serialization_roundtrip_preserves_all_fields(self)`
  - `test_detects_expiration_correctly` (method, line 65) `def test_detects_expiration_correctly(self)`
  - `test_checks_permissions_with_set_operations` (method, line 83) `def test_checks_permissions_with_set_operations(self)`
  - `_make_store` (method, line 99) `def _make_store(self, tmp_path)`
  - `test_creates_and_lists_keys_scoped_by_tenant` (method, line 105) `def test_creates_and_lists_keys_scoped_by_tenant(self, tmp_path)`
  - `test_validates_a_known_key_and_returns_record` (method, line 116) `def test_validates_a_known_key_and_returns_record(self, tmp_path)`
  - `test_rejects_unknown_key_returning_none` (method, line 124) `def test_rejects_unknown_key_returning_none(self, tmp_path)`
  - `test_rejects_empty_plaintext_key` (method, line 128) `def test_rejects_empty_plaintext_key(self, tmp_path)`
  - `test_rejects_expired_key` (method, line 132) `def test_rejects_expired_key(self, tmp_path)`
  - `test_updates_last_used_on_successful_validation` (method, line 151) `def test_updates_last_used_on_successful_validation(self, tmp_path)`
  - `test_revokes_key_preventing_future_validation` (method, line 162) `def test_revokes_key_preventing_future_validation(self, tmp_path)`
  - `test_revocation_is_idempotent` (method, line 168) `def test_revocation_is_idempotent(self, tmp_path)`
  - `test_enforces_max_keys_per_tenant_raises_value_error` (method, line 172) `def test_enforces_max_keys_per_tenant_raises_value_error(self, tmp_path)`
  - `test_rotates_key_preserving_tenant_label_and_permissions` (method, line 185) `def test_rotates_key_preserving_tenant_label_and_permissions(self, tmp_path)`
  - `test_rotation_copies_permissions_from_the_rotated_key` (method, line 195) `def test_rotation_copies_permissions_from_the_rotated_key(self, tmp_path)`
  - `test_old_key_stays_valid_during_rotation_grace` (method, line 206) `def test_old_key_stays_valid_during_rotation_grace(self, tmp_path)`
  - `test_old_key_rejected_after_rotation_grace_expires` (method, line 214) `def test_old_key_rejected_after_rotation_grace_expires(self, tmp_path)`
  - `test_retired_keys_are_pruned_after_grace_expires` (method, line 227) `def test_retired_keys_are_pruned_after_grace_expires(self, tmp_path)`
  - `test_rotation_does_not_grow_active_key_count` (method, line 243) `def test_rotation_does_not_grow_active_key_count(self, tmp_path)`
  - `test_never_stores_plaintext_token_on_disk` (method, line 258) `def test_never_stores_plaintext_token_on_disk(self, tmp_path)`
  - `_make_app` (method, line 274) `def _make_app(self, tmp_path)`
  - `_build_client` (method, line 282) `def _build_client(self, tmp_path, store)`
  - `test_allows_valid_key_in_bearer_header` (method, line 312) `def test_allows_valid_key_in_bearer_header(self, tmp_path)`
  - `test_allows_valid_key_in_x_api_key_header` (method, line 319) `def test_allows_valid_key_in_x_api_key_header(self, tmp_path)`
  - `test_allows_valid_key_in_query_param` (method, line 325) `def test_allows_valid_key_in_query_param(self, tmp_path)`
  - `test_rejects_missing_key_with_401` (method, line 331) `def test_rejects_missing_key_with_401(self, tmp_path)`
  - `test_rejects_invalid_key_with_401` (method, line 336) `def test_rejects_invalid_key_with_401(self, tmp_path)`
  - `test_rejects_key_with_insufficient_permissions_with_403` (method, line 341) `def test_rejects_key_with_insufficient_permissions_with_403(self, tmp_path)`
  - `test_sets_g_variables_with_api_key_context_on_success` (method, line 347) `def test_sets_g_variables_with_api_key_context_on_success(self, tmp_path)`
  - `_make_store` (method, line 359) `def _make_store(self, tmp_path)`
  - `test_returns_a_validatable_token` (method, line 365) `def test_returns_a_validatable_token(self, tmp_path)`
  - `test_stores_permissions_on_the_key_record` (method, line 373) `def test_stores_permissions_on_the_key_record(self, tmp_path)`
  - `test_sets_expiration_when_days_are_provided` (method, line 386) `def test_sets_expiration_when_days_are_provided(self, tmp_path)`
  - `_make_store` (method, line 400) `def _make_store(self, tmp_path)`
  - `test_constant_time_comparison_rejects_wrong_secrets` (method, line 406) `def test_constant_time_comparison_rejects_wrong_secrets(self)`
  - `test_generates_50_unique_tokens_without_collision` (method, line 414) `def test_generates_50_unique_tokens_without_collision(self)`
  - `test_atomic_write_leaves_no_tmp_files` (method, line 419) `def test_atomic_write_leaves_no_tmp_files(self, tmp_path)`
  - `secure` (method, line 294) `def secure()`
  - `g_check` (method, line 299) `def g_check()`
  - `admin_only` (method, line 307) `def admin_only()`
- Depends on: `core/api_authz.py`

## tests/test_api_key_resolution.py
- Doc: API-key resolution contract tests.
- Layer: testing
- Language: py
- Symbols:
  - `TestApiKeyWiredIntoParams` (class, line 21) `class TestApiKeyWiredIntoParams`
  - `TestReplaceCommandPlaceholders` (class, line 41) `class TestReplaceCommandPlaceholders`
  - `test_params_api_key_is_not_hardcoded_none` (method, line 22) `def test_params_api_key_is_not_hardcoded_none(self)`
  - `test_params_api_key_binds_config_attr` (method, line 29) `def test_params_api_key_binds_config_attr(self)`
  - `test_class_attribute_api_key_reads_payload` (method, line 36) `def test_class_attribute_api_key_reads_payload(self)`
  - `test_double_brace_substitution` (method, line 42) `def test_double_brace_substitution(self)`
  - `test_single_brace_substitution` (method, line 49) `def test_single_brace_substitution(self)`
  - `test_mixed_braces_in_one_command` (method, line 58) `def test_mixed_braces_in_one_command(self)`
  - `test_missing_key_left_intact` (method, line 67) `def test_missing_key_left_intact(self)`
- Depends on: `utils.py`

## tests/test_api_v1.py
- Doc: Integration tests for the versioned C2 REST API (``/api/v1``).
- Layer: testing
- Language: py
- Symbols:
  - `api_client` (function, line 23) `def api_client(tmp_path)`
  - `_auth` (function, line 40) `def _auth(token)`
  - `test_health_is_public` (function, line 44) `def test_health_is_public(api_client)`
  - `test_targets_requires_auth` (function, line 51) `def test_targets_requires_auth(api_client)`
  - `test_targets_empty_workspace` (function, line 56) `def test_targets_empty_workspace(api_client)`
  - `test_targets_lists_hosts_with_services` (function, line 64) `def test_targets_lists_hosts_with_services(api_client)`
  - `test_results_empty` (function, line 76) `def test_results_empty(api_client)`
  - `test_results_per_client` (function, line 82) `def test_results_per_client(api_client)`
  - `test_campaigns_empty_state` (function, line 95) `def test_campaigns_empty_state(api_client)`
  - `test_campaigns_reads_state_files` (function, line 101) `def test_campaigns_reads_state_files(api_client)`
  - `test_webhook_crud` (function, line 109) `def test_webhook_crud(api_client)`
  - `test_webhook_rejects_bad_url` (function, line 126) `def test_webhook_rejects_bad_url(api_client)`
  - `test_mutating_endpoints_require_auth` (function, line 134) `def test_mutating_endpoints_require_auth(api_client)`
- Depends on: `core/api_authz.py`, `lazyc2/blueprints/api_v1.py`, `modules/beacon_history.py`, `modules/db.py`


Next: [KB_tests_p2.md](KB_tests_p2.md)
