# Symbols (page 29 of 40)
Previous: [SYMBOLS_p28.md](SYMBOLS_p28.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_backups` | function | `tests/run_mutation_ux_usability.py:71` | `def _backups(mutations)` |
| `_restore` | function | `tests/run_mutation_ux_usability.py:79` | `def _restore(backups, mutations)` |
| `_run_tests` | function | `tests/run_mutation_ux_usability.py:60` | `def _run_tests()` |
| `main` | function | `tests/run_mutation_ux_usability.py:84` | `def main()` |
| `TestACIEngineComplete` | class | `tests/test_aci_planner.py:596` | `class TestACIEngineComplete` |
| `TestACIEngineReplan` | class | `tests/test_aci_planner.py:522` | `class TestACIEngineReplan` |
| `TestACIEngineShouldReplan` | class | `tests/test_aci_planner.py:462` | `class TestACIEngineShouldReplan` |
| `TestACIEngineStatus` | class | `tests/test_aci_planner.py:421` | `class TestACIEngineStatus` |
| `TestACIGoal` | class | `tests/test_aci_planner.py:111` | `class TestACIGoal` |
| `TestACIPlan` | class | `tests/test_aci_planner.py:177` | `class TestACIPlan` |
| `TestACIPlannerLLM` | class | `tests/test_aci_planner.py:345` | `class TestACIPlannerLLM` |
| `TestACIPlannerStatic` | class | `tests/test_aci_planner.py:244` | `class TestACIPlannerStatic` |
| `TestACIReflector` | class | `tests/test_aci_planner.py:626` | `class TestACIReflector` |
| `TestAttackPhase` | class | `tests/test_aci_planner.py:134` | `class TestAttackPhase` |
| `TestCLI` | class | `tests/test_aci_planner.py:914` | `class TestCLI` |
| `TestMCPBridges` | class | `tests/test_aci_planner.py:723` | `class TestMCPBridges` |
| `TestPersistenceHelpers` | class | `tests/test_aci_planner.py:829` | `class TestPersistenceHelpers` |
| `_llm_response` | method | `tests/test_aci_planner.py:346` | `def _llm_response(self, phases)` |
| `_make_engine` | function | `tests/test_aci_planner.py:94` | `def _make_engine(tmp_path, api_key)` |
| `_make_goal` | function | `tests/test_aci_planner.py:33` | `def _make_goal()` |
| `_make_plan` | method | `tests/test_aci_planner.py:178` | `def _make_plan(self, phase_statuses)` |
| `_make_plan_with_statuses` | method | `tests/test_aci_planner.py:627` | `def _make_plan_with_statuses(self, phase_statuses, replan_count)` |
| `_make_planner` | function | `tests/test_aci_planner.py:82` | `def _make_planner(tmp_path, api_key)` |
| `_patched_paths` | function | `tests/test_aci_planner.py:47` | `def _patched_paths(tmp_path)` |
| `_start_patches` | function | `tests/test_aci_planner.py:60` | `def _start_patches(tmp_path)` |
| `_stop_patches` | function | `tests/test_aci_planner.py:77` | `def _stop_patches(patchers)` |
| `_write_objectives_blocked` | method | `tests/test_aci_planner.py:463` | `def _write_objectives_blocked(self, obj_file, obj_ids)` |
| `test_active_phase_none_when_all_done` | method | `tests/test_aci_planner.py:221` | `def test_active_phase_none_when_all_done(self)` |
| `test_active_phase_returns_first_pending_or_active` | method | `tests/test_aci_planner.py:216` | `def test_active_phase_returns_first_pending_or_active(self)` |
| `test_archive_plan_appends` | method | `tests/test_aci_planner.py:859` | `def test_archive_plan_appends(self, tmp_path)` |
| `test_complete_archives_plan` | method | `tests/test_aci_planner.py:597` | `def test_complete_archives_plan(self, tmp_path)` |
| `test_complete_marks_plan_as_completed` | method | `tests/test_aci_planner.py:607` | `def test_complete_marks_plan_as_completed(self, tmp_path)` |
| `test_complete_no_plan` | method | `tests/test_aci_planner.py:617` | `def test_complete_no_plan(self, tmp_path)` |
| `test_completion_pct_all_done` | method | `tests/test_aci_planner.py:204` | `def test_completion_pct_all_done(self)` |
| `test_completion_pct_none_done` | method | `tests/test_aci_planner.py:208` | `def test_completion_pct_none_done(self)` |
| `test_completion_pct_partial` | method | `tests/test_aci_planner.py:212` | `def test_completion_pct_partial(self)` |
| `test_count_objectives_by_status` | method | `tests/test_aci_planner.py:876` | `def test_count_objectives_by_status(self, tmp_path)` |
| `test_count_objectives_returns_empty_for_missing_file` | method | `tests/test_aci_planner.py:904` | `def test_count_objectives_returns_empty_for_missing_file(self, tmp_path)` |
| `test_defaults` | method | `tests/test_aci_planner.py:122` | `def test_defaults(self)` |
| `test_fields` | method | `tests/test_aci_planner.py:112` | `def test_fields(self)` |
| `test_first_phase_is_active` | method | `tests/test_aci_planner.py:257` | `def test_first_phase_is_active(self, tmp_path)` |
| `test_from_dict_ignores_extra_keys` | method | `tests/test_aci_planner.py:154` | `def test_from_dict_ignores_extra_keys(self)` |
| `test_llm_bad_json_falls_back_to_static` | method | `tests/test_aci_planner.py:407` | `def test_llm_bad_json_falls_back_to_static(self, tmp_path)` |
| `test_llm_failure_falls_back_to_static` | method | `tests/test_aci_planner.py:399` | `def test_llm_failure_falls_back_to_static(self, tmp_path)` |
| `test_llm_objectives_injected` | method | `tests/test_aci_planner.py:380` | `def test_llm_objectives_injected(self, tmp_path)` |
| `test_llm_phases_used_when_api_key_set` | method | `tests/test_aci_planner.py:355` | `def test_llm_phases_used_when_api_key_set(self, tmp_path)` |
| `test_load_plan_returns_none_for_corrupt` | method | `tests/test_aci_planner.py:851` | `def test_load_plan_returns_none_for_corrupt(self, tmp_path)` |
| `test_load_plan_returns_none_for_missing` | method | `tests/test_aci_planner.py:845` | `def test_load_plan_returns_none_for_missing(self, tmp_path)` |
| `test_mcp_aci_plan_phase_filter` | method | `tests/test_aci_planner.py:806` | `def test_mcp_aci_plan_phase_filter(self, tmp_path)` |
| `test_mcp_aci_plan_returns_json` | method | `tests/test_aci_planner.py:734` | `def test_mcp_aci_plan_returns_json(self, tmp_path)` |
| `test_mcp_aci_plan_static_backend` | method | `tests/test_aci_planner.py:758` | `def test_mcp_aci_plan_static_backend(self, tmp_path)` |
| `test_mcp_aci_plan_uses_rhost_from_payload` | method | `tests/test_aci_planner.py:747` | `def test_mcp_aci_plan_uses_rhost_from_payload(self, tmp_path)` |
| `test_mcp_aci_replan_no_plan` | method | `tests/test_aci_planner.py:769` | `def test_mcp_aci_replan_no_plan(self, tmp_path)` |
| `test_mcp_aci_replan_with_plan` | method | `tests/test_aci_planner.py:780` | `def test_mcp_aci_replan_with_plan(self, tmp_path)` |
| `test_mcp_aci_status_after_plan` | method | `tests/test_aci_planner.py:793` | `def test_mcp_aci_status_after_plan(self, tmp_path)` |
| `test_mcp_aci_status_no_plan` | method | `tests/test_aci_planner.py:724` | `def test_mcp_aci_status_no_plan(self, tmp_path)` |
| `test_no_subcommand_returns_nonzero` | method | `tests/test_aci_planner.py:954` | `def test_no_subcommand_returns_nonzero(self, tmp_path)` |
| `test_objective_source_is_aci_planner` | method | `tests/test_aci_planner.py:293` | `def test_objective_source_is_aci_planner(self, tmp_path)` |
| `test_objectives_contain_target_in_text` | method | `tests/test_aci_planner.py:323` | `def test_objectives_contain_target_in_text(self, tmp_path)` |
| `test_objectives_ids_match_phase_objectives` | method | `tests/test_aci_planner.py:276` | `def test_objectives_ids_match_phase_objectives(self, tmp_path)` |
| `test_objectives_injected_into_file` | method | `tests/test_aci_planner.py:268` | `def test_objectives_injected_into_file(self, tmp_path)` |
| `test_phase_filter_restricts_phases` | method | `tests/test_aci_planner.py:287` | `def test_phase_filter_restricts_phases(self, tmp_path)` |
| `test_plan_command` | method | `tests/test_aci_planner.py:915` | `def test_plan_command(self, tmp_path)` |
| `test_plan_creates_file` | method | `tests/test_aci_planner.py:245` | `def test_plan_creates_file(self, tmp_path)` |
| `test_plan_domain_stored` | method | `tests/test_aci_planner.py:318` | `def test_plan_domain_stored(self, tmp_path)` |
| `test_plan_has_phases` | method | `tests/test_aci_planner.py:252` | `def test_plan_has_phases(self, tmp_path)` |
| `test_plan_id_is_unique` | method | `tests/test_aci_planner.py:307` | `def test_plan_id_is_unique(self, tmp_path)` |
| `test_plan_roundtrip_from_disk` | method | `tests/test_aci_planner.py:330` | `def test_plan_roundtrip_from_disk(self, tmp_path)` |
| `test_plan_status_is_active` | method | `tests/test_aci_planner.py:302` | `def test_plan_status_is_active(self, tmp_path)` |
| `test_plan_target_stored` | method | `tests/test_aci_planner.py:313` | `def test_plan_target_stored(self, tmp_path)` |
| `test_reflect_blocked_phase_generates_lesson` | method | `tests/test_aci_planner.py:655` | `def test_reflect_blocked_phase_generates_lesson(self, tmp_path)` |
| `test_reflect_command_no_plan` | method | `tests/test_aci_planner.py:960` | `def test_reflect_command_no_plan(self, tmp_path, capsys)` |
| `test_reflect_done_after_replan_generates_lesson` | method | `tests/test_aci_planner.py:665` | `def test_reflect_done_after_replan_generates_lesson(self, tmp_path)` |
| `test_reflect_lesson_has_required_fields` | method | `tests/test_aci_planner.py:698` | `def test_reflect_lesson_has_required_fields(self, tmp_path)` |
| `test_reflect_no_lessons_clean_plan` | method | `tests/test_aci_planner.py:674` | `def test_reflect_no_lessons_clean_plan(self, tmp_path)` |
| `test_reflect_persists_to_file` | method | `tests/test_aci_planner.py:683` | `def test_reflect_persists_to_file(self, tmp_path)` |
| `test_replan_command_no_plan` | method | `tests/test_aci_planner.py:940` | `def test_replan_command_no_plan(self, tmp_path, capsys)` |
| `test_replan_increments_count` | method | `tests/test_aci_planner.py:529` | `def test_replan_increments_count(self, tmp_path)` |
| `test_replan_injects_new_objectives` | method | `tests/test_aci_planner.py:543` | `def test_replan_injects_new_objectives(self, tmp_path)` |
| `test_replan_no_plan` | method | `tests/test_aci_planner.py:523` | `def test_replan_no_plan(self, tmp_path)` |
| `test_replan_records_reason` | method | `tests/test_aci_planner.py:536` | `def test_replan_records_reason(self, tmp_path)` |
| `test_replan_status_returns_to_active` | method | `tests/test_aci_planner.py:553` | `def test_replan_status_returns_to_active(self, tmp_path)` |
| `test_replan_twice_counts_two` | method | `tests/test_aci_planner.py:560` | `def test_replan_twice_counts_two(self, tmp_path)` |
| `test_replan_with_llm` | method | `tests/test_aci_planner.py:568` | `def test_replan_with_llm(self, tmp_path)` |
| `test_round_trip` | method | `tests/test_aci_planner.py:231` | `def test_round_trip(self)` |
| `test_save_load_plan_roundtrip` | method | `tests/test_aci_planner.py:830` | `def test_save_load_plan_roundtrip(self, tmp_path)` |
| `test_should_replan_false_below_threshold` | method | `tests/test_aci_planner.py:487` | `def test_should_replan_false_below_threshold(self, tmp_path)` |
| `test_should_replan_false_for_completed_plan` | method | `tests/test_aci_planner.py:507` | `def test_should_replan_false_for_completed_plan(self, tmp_path)` |
| `test_should_replan_false_when_no_plan` | method | `tests/test_aci_planner.py:483` | `def test_should_replan_false_when_no_plan(self, tmp_path)` |
| `test_should_replan_true_at_threshold` | method | `tests/test_aci_planner.py:496` | `def test_should_replan_true_at_threshold(self, tmp_path)` |
| `test_status_blocked_count_zero_at_start` | method | `tests/test_aci_planner.py:451` | `def test_status_blocked_count_zero_at_start(self, tmp_path)` |
| `test_status_command_no_plan` | method | `tests/test_aci_planner.py:926` | `def test_status_command_no_plan(self, tmp_path, capsys)` |
| `test_status_completion_zero_at_start` | method | `tests/test_aci_planner.py:444` | `def test_status_completion_zero_at_start(self, tmp_path)` |
| `test_status_has_active_phase` | method | `tests/test_aci_planner.py:437` | `def test_status_has_active_phase(self, tmp_path)` |
| `test_status_no_plan` | method | `tests/test_aci_planner.py:422` | `def test_status_no_plan(self, tmp_path)` |
| `test_status_with_plan` | method | `tests/test_aci_planner.py:427` | `def test_status_with_plan(self, tmp_path)` |
| `test_subsequent_phases_are_pending` | method | `tests/test_aci_planner.py:262` | `def test_subsequent_phases_are_pending(self, tmp_path)` |
| `test_to_dict_has_completion_pct` | method | `tests/test_aci_planner.py:225` | `def test_to_dict_has_completion_pct(self)` |
| `test_to_dict_round_trip` | method | `tests/test_aci_planner.py:135` | `def test_to_dict_round_trip(self)` |
| `TestAddonStore` | class | `tests/test_addon_creator.py:328` | `class TestAddonStore` |
| `TestBlueprint` | class | `tests/test_addon_creator.py:591` | `class TestBlueprint` |
| `TestConfig` | class | `tests/test_addon_creator.py:86` | `class TestConfig` |
| `TestParseAddonForm` | class | `tests/test_addon_creator.py:460` | `class TestParseAddonForm` |
| `TestTemplateSanity` | class | `tests/test_addon_creator.py:805` | `class TestTemplateSanity` |
| `TestValidator` | class | `tests/test_addon_creator.py:117` | `class TestValidator` |
| `TestYamlRenderer` | class | `tests/test_addon_creator.py:263` | `class TestYamlRenderer` |
| `_FakeOperator` | class | `tests/test_addon_creator.py:570` | `class _FakeOperator(UserMixin)` |
| `_build_test_app` | function | `tests/test_addon_creator.py:521` | `def _build_test_app(tmp_path)` |
| `_csrf_token` | method | `tests/test_addon_creator.py:650` | `def _csrf_token(self, client)` |
| `_form_data` | method | `tests/test_addon_creator.py:626` | `def _form_data(self)` |
| `_load_user` | function | `tests/test_addon_creator.py:577` | `def _load_user(user_id)` |
| `_login` | function | `tests/test_addon_creator.py:585` | `def _login(client)` |
| `_valid_draft` | function | `tests/test_addon_creator.py:45` | `def _valid_draft()` |
| `test_bad_repo_url_reports_issue` | method | `tests/test_addon_creator.py:205` | `def test_bad_repo_url_reports_issue(self)` |
| `test_boolean_default_whitelist` | method | `tests/test_addon_creator.py:232` | `def test_boolean_default_whitelist(self)` |
| `test_create_form_issues_csrf_cookie` | method | `tests/test_addon_creator.py:602` | `def test_create_form_issues_csrf_cookie(self, tmp_path)` |
| `test_creator_template_forbids_emojis_and_console_spam` | method | `tests/test_addon_creator.py:816` | `def test_creator_template_forbids_emojis_and_console_spam(self)` |
| `test_creator_template_has_help_affordances` | method | `tests/test_addon_creator.py:808` | `def test_creator_template_has_help_affordances(self)` |
| `test_declared_param_placeholder_is_allowed` | method | `tests/test_addon_creator.py:186` | `def test_declared_param_placeholder_is_allowed(self)` |
| `test_default_author_and_version_applied` | method | `tests/test_addon_creator.py:315` | `def test_default_author_and_version_applied(self)` |
| `test_delete_legacy_uppercase_addon` | method | `tests/test_addon_creator.py:774` | `def test_delete_legacy_uppercase_addon(self, tmp_path)` |
| `test_delete_rejects_unsafe_existing_names` | method | `tests/test_addon_creator.py:425` | `def test_delete_rejects_unsafe_existing_names(self, tmp_path)` |
| `test_delete_removes_addon` | method | `tests/test_addon_creator.py:722` | `def test_delete_removes_addon(self, tmp_path)` |
| `test_delete_unknown_addon_flashes_and_redirects` | method | `tests/test_addon_creator.py:734` | `def test_delete_unknown_addon_flashes_and_redirects(self, tmp_path)` |
| `test_delete_without_csrf_is_rejected` | method | `tests/test_addon_creator.py:619` | `def test_delete_without_csrf_is_rejected(self, tmp_path)` |
| `test_duplicate_name_rerenders_with_error` | method | `tests/test_addon_creator.py:685` | `def test_duplicate_name_rerenders_with_error(self, tmp_path)` |
| `test_duplicate_param_reports_issue` | method | `tests/test_addon_creator.py:212` | `def test_duplicate_param_reports_issue(self)` |
| `test_exists_swallows_invalid_names` | method | `tests/test_addon_creator.py:434` | `def test_exists_swallows_invalid_names(self, tmp_path)` |
| `test_install_path_without_repo_url_reports_issue` | method | `tests/test_addon_creator.py:192` | `def test_install_path_without_repo_url_reports_issue(self)` |
| `test_integer_default_must_parse` | method | `tests/test_addon_creator.py:224` | `def test_integer_default_must_parse(self)` |
| `test_invalid_name_reports_issue` | method | `tests/test_addon_creator.py:131` | `def test_invalid_name_reports_issue(self)` |
| `test_invalid_post_rerenders_with_field_errors` | method | `tests/test_addon_creator.py:673` | `def test_invalid_post_rerenders_with_field_errors(self, tmp_path)` |
| `test_list_all_is_sorted_and_has_expected_keys` | method | `tests/test_addon_creator.py:383` | `def test_list_all_is_sorted_and_has_expected_keys(self, tmp_path)` |
| `test_list_all_reports_file_stem_as_filename` | method | `tests/test_addon_creator.py:400` | `def test_list_all_reports_file_stem_as_filename(self, tmp_path)` |
| `test_list_all_skips_broken_files` | method | `tests/test_addon_creator.py:374` | `def test_list_all_skips_broken_files(self, tmp_path)` |
| `test_list_page_links_by_filename_for_legacy_names` | method | `tests/test_addon_creator.py:764` | `def test_list_page_links_by_filename_for_legacy_names(self, tmp_path)` |
| `test_list_page_shows_created_addon` | method | `tests/test_addon_creator.py:710` | `def test_list_page_shows_created_addon(self, tmp_path)` |
| `test_load_accepts_pre_existing_dots_and_hyphens` | method | `tests/test_addon_creator.py:413` | `def test_load_accepts_pre_existing_dots_and_hyphens(self, tmp_path)` |
| `test_load_accepts_pre_existing_uppercase_names` | method | `tests/test_addon_creator.py:407` | `def test_load_accepts_pre_existing_uppercase_names(self, tmp_path)` |
| `test_load_missing_raises_file_not_found` | method | `tests/test_addon_creator.py:369` | `def test_load_missing_raises_file_not_found(self, tmp_path)` |
| `test_load_still_rejects_traversal_through_existing_path` | method | `tests/test_addon_creator.py:419` | `def test_load_still_rejects_traversal_through_existing_path(self, tmp_path)` |
| `test_malformed_category_reports_issue` | method | `tests/test_addon_creator.py:156` | `def test_malformed_category_reports_issue(self)` |
| `test_malformed_env_entry_reports_issue` | method | `tests/test_addon_creator.py:249` | `def test_malformed_env_entry_reports_issue(self)` |
| `test_missing_description_reports_issue` | method | `tests/test_addon_creator.py:138` | `def test_missing_description_reports_issue(self)` |
| `test_missing_directory_lists_empty` | method | `tests/test_addon_creator.py:430` | `def test_missing_directory_lists_empty(self, tmp_path)` |
| `test_missing_execute_command_reports_issue` | method | `tests/test_addon_creator.py:168` | `def test_missing_execute_command_reports_issue(self)` |
| `test_missing_name_reports_issue` | method | `tests/test_addon_creator.py:125` | `def test_missing_name_reports_issue(self)` |
| `test_missing_optional_fields_become_empty` | method | `tests/test_addon_creator.py:509` | `def test_missing_optional_fields_become_empty(self)` |
| `test_name_pattern_rejects_traversal` | method | `tests/test_addon_creator.py:89` | `def test_name_pattern_rejects_traversal(self)` |
| `test_nested_brace_placeholder_reports_issue` | method | `tests/test_addon_creator.py:180` | `def test_nested_brace_placeholder_reports_issue(self)` |
| `test_optional_fields_are_dropped` | method | `tests/test_addon_creator.py:295` | `def test_optional_fields_are_dropped(self)` |
| `test_os_options_cover_mitre_platforms` | method | `tests/test_addon_creator.py:105` | `def test_os_options_cover_mitre_platforms(self)` |
| `test_param_without_description_reports_issue` | method | `tests/test_addon_creator.py:218` | `def test_param_without_description_reports_issue(self)` |
| `test_parse_complete_form` | method | `tests/test_addon_creator.py:463` | `def test_parse_complete_form(self)` |
| `test_patterns_accept_canonical_values` | method | `tests/test_addon_creator.py:96` | `def test_patterns_accept_canonical_values(self)` |
| `test_payload_placeholders_cover_core_keys` | method | `tests/test_addon_creator.py:111` | `def test_payload_placeholders_cover_core_keys(self)` |
| `test_post_without_csrf_is_rejected` | method | `tests/test_addon_creator.py:612` | `def test_post_without_csrf_is_rejected(self, tmp_path)` |
| `test_rendered_addon_passes_cli_schema_contract` | method | `tests/test_addon_creator.py:786` | `def test_rendered_addon_passes_cli_schema_contract(self, tmp_path)` |
| `test_rendered_document_is_canonical` | method | `tests/test_addon_creator.py:266` | `def test_rendered_document_is_canonical(self)` |
| `test_rendered_yaml_has_no_none_values` | method | `tests/test_addon_creator.py:310` | `def test_rendered_yaml_has_no_none_values(self)` |
| `test_save_is_atomic_and_leaves_no_temp_files` | method | `tests/test_addon_creator.py:357` | `def test_save_is_atomic_and_leaves_no_temp_files(self, tmp_path)` |
| `test_save_load_delete_round_trip` | method | `tests/test_addon_creator.py:331` | `def test_save_load_delete_round_trip(self, tmp_path)` |
| `test_save_overwrites_cleanly` | method | `tests/test_addon_creator.py:363` | `def test_save_overwrites_cleanly(self, tmp_path)` |
| `test_single_trigger_string_becomes_list` | method | `tests/test_addon_creator.py:516` | `def test_single_trigger_string_becomes_list(self)` |
| `test_symlink_escape_rejected_on_delete` | method | `tests/test_addon_creator.py:448` | `def test_symlink_escape_rejected_on_delete(self, tmp_path)` |
| `test_symlink_escape_rejected_on_load` | method | `tests/test_addon_creator.py:438` | `def test_symlink_escape_rejected_on_load(self, tmp_path)` |
| `test_too_many_params_reports_issue` | method | `tests/test_addon_creator.py:240` | `def test_too_many_params_reports_issue(self)` |
| `test_tools_creator_template_has_no_broken_js` | method | `tests/test_addon_creator.py:821` | `def test_tools_creator_template_has_no_broken_js(self)` |
| `test_traversal_install_path_reports_issue` | method | `tests/test_addon_creator.py:198` | `def test_traversal_install_path_reports_issue(self)` |
| `test_traversal_name_rejected_on_delete` | method | `tests/test_addon_creator.py:352` | `def test_traversal_name_rejected_on_delete(self, tmp_path)` |
| `test_traversal_name_rejected_on_load` | method | `tests/test_addon_creator.py:347` | `def test_traversal_name_rejected_on_load(self, tmp_path)` |
| `test_traversal_name_rejected_on_save` | method | `tests/test_addon_creator.py:342` | `def test_traversal_name_rejected_on_save(self, tmp_path)` |
| `test_unauthenticated_access_redirects_to_login` | method | `tests/test_addon_creator.py:594` | `def test_unauthenticated_access_redirects_to_login(self, tmp_path)` |
| `test_unchecked_enabled_becomes_false` | method | `tests/test_addon_creator.py:505` | `def test_unchecked_enabled_becomes_false(self)` |
| `test_unknown_module_type_reports_issue` | method | `tests/test_addon_creator.py:150` | `def test_unknown_module_type_reports_issue(self)` |
| `test_unknown_os_reports_issue` | method | `tests/test_addon_creator.py:144` | `def test_unknown_os_reports_issue(self)` |
| `test_unknown_placeholder_reports_issue` | method | `tests/test_addon_creator.py:174` | `def test_unknown_placeholder_reports_issue(self)` |
| `test_uppercase_trigger_reports_issue` | method | `tests/test_addon_creator.py:162` | `def test_uppercase_trigger_reports_issue(self)` |
| `test_valid_draft_has_no_issues` | method | `tests/test_addon_creator.py:120` | `def test_valid_draft_has_no_issues(self)` |
| `test_valid_post_creates_addon_and_redirects` | method | `tests/test_addon_creator.py:660` | `def test_valid_post_creates_addon_and_redirects(self, tmp_path)` |
| `test_validation_error_carries_issues` | method | `tests/test_addon_creator.py:255` | `def test_validation_error_carries_issues(self)` |
| `test_view_legacy_uppercase_addon_renders` | method | `tests/test_addon_creator.py:751` | `def test_view_legacy_uppercase_addon_renders(self, tmp_path)` |
| `test_view_page_renders_yaml` | method | `tests/test_addon_creator.py:698` | `def test_view_page_renders_yaml(self, tmp_path)` |
| `test_view_unknown_addon_redirects_to_list` | method | `tests/test_addon_creator.py:744` | `def test_view_unknown_addon_redirects_to_list(self, tmp_path)` |
| `test_yaml_round_trips_through_loader` | method | `tests/test_addon_creator.py:286` | `def test_yaml_round_trips_through_loader(self)` |
| `TestConfigExposesKey` | class | `tests/test_aes_key_propagation.py:83` | `class TestConfigExposesKey` |
| `TestDiskSource` | class | `tests/test_aes_key_propagation.py:57` | `class TestDiskSource` |
| `TestGeneratedSource` | class | `tests/test_aes_key_propagation.py:67` | `class TestGeneratedSource` |
| `TestHexSource` | class | `tests/test_aes_key_propagation.py:32` | `class TestHexSource` |
| `test_config_exposes_params_dict` | method | `tests/test_aes_key_propagation.py:91` | `def test_config_exposes_params_dict(self)` |
| `test_config_has_aes_key_attribute` | method | `tests/test_aes_key_propagation.py:86` | `def test_config_has_aes_key_attribute(self)` |
| `test_existing_disk_key_is_loaded` | method | `tests/test_aes_key_propagation.py:60` | `def test_existing_disk_key_is_loaded(self, tmp_path)` |
| `test_generated_key_is_32_bytes` | method | `tests/test_aes_key_propagation.py:70` | `def test_generated_key_is_32_bytes(self, tmp_path)` |
| `test_generated_key_is_persisted` | method | `tests/test_aes_key_propagation.py:75` | `def test_generated_key_is_persisted(self, tmp_path)` |
| `test_non_hex_raises` | method | `tests/test_aes_key_propagation.py:49` | `def test_non_hex_raises(self)` |
| `test_valid_hex_decodes_to_32_bytes` | method | `tests/test_aes_key_propagation.py:35` | `def test_valid_hex_decodes_to_32_bytes(self)` |
| `test_wrong_length_raises` | method | `tests/test_aes_key_propagation.py:42` | `def test_wrong_length_raises(self)` |
| `TestDoAsk` | class | `tests/test_ai_commands_llm.py:26` | `class TestDoAsk` |
| `TestDoGroq` | class | `tests/test_ai_commands_llm.py:53` | `class TestDoGroq` |
| `_Backend` | class | `tests/test_ai_commands_llm.py:71` | `class _Backend` |
| `_Backend` | class | `tests/test_ai_commands_llm.py:93` | `class _Backend` |
| `_Backend` | class | `tests/test_ai_commands_llm.py:106` | `class _Backend` |
| `_command_set` | function | `tests/test_ai_commands_llm.py:17` | `def _command_set()` |
| `_factory` | function | `tests/test_ai_commands_llm.py:77` | `def _factory()` |
| `_raise` | function | `tests/test_ai_commands_llm.py:57` | `def _raise()` |
| `complete` | method | `tests/test_ai_commands_llm.py:72` | `def complete(self, system, user)` |
| `complete` | method | `tests/test_ai_commands_llm.py:94` | `def complete(self, system, user)` |
| `complete` | method | `tests/test_ai_commands_llm.py:107` | `def complete(self, system, user)` |
| `test_backend_error_surfaces_as_message` | method | `tests/test_ai_commands_llm.py:45` | `def test_backend_error_surfaces_as_message(self, monkeypatch)` |
| `test_completion_failure_prints_error` | method | `tests/test_ai_commands_llm.py:90` | `def test_completion_failure_prints_error(self, monkeypatch)` |
| `test_empty_line_falls_back_to_shell_prompt` | method | `tests/test_ai_commands_llm.py:103` | `def test_empty_line_falls_back_to_shell_prompt(self, monkeypatch)` |
| `test_empty_question_prints_usage` | method | `tests/test_ai_commands_llm.py:27` | `def test_empty_question_prints_usage(self, monkeypatch)` |
| `test_question_forwarded_with_session_context` | method | `tests/test_ai_commands_llm.py:33` | `def test_question_forwarded_with_session_context(self, monkeypatch)` |
| `test_success_completes_oneliner_and_prints` | method | `tests/test_ai_commands_llm.py:66` | `def test_success_completes_oneliner_and_prints(self, monkeypatch)` |
| `test_unavailable_backend_prints_actionable_error` | method | `tests/test_ai_commands_llm.py:54` | `def test_unavailable_backend_prints_actionable_error(self, monkeypatch)` |
| `TestApiAuthzConfig` | class | `tests/test_api_authz.py:21` | `class TestApiAuthzConfig` |
| `TestApiKey` | class | `tests/test_api_authz.py:45` | `class TestApiKey` |
| `TestApiKeyStore` | class | `tests/test_api_authz.py:102` | `class TestApiKeyStore` |
| `TestCreateApiToken` | class | `tests/test_api_authz.py:377` | `class TestCreateApiToken` |
| `TestEdgeCases` | class | `tests/test_api_authz.py:423` | `class TestEdgeCases` |
| `TestRequireApiAuth` | class | `tests/test_api_authz.py:288` | `class TestRequireApiAuth` |
| `_build_client` | method | `tests/test_api_authz.py:301` | `def _build_client(self, tmp_path, store)` |
| `_make_app` | method | `tests/test_api_authz.py:291` | `def _make_app(self, tmp_path)` |
| `_make_store` | method | `tests/test_api_authz.py:105` | `def _make_store(self, tmp_path)` |
| `_make_store` | method | `tests/test_api_authz.py:380` | `def _make_store(self, tmp_path)` |
| `_make_store` | method | `tests/test_api_authz.py:426` | `def _make_store(self, tmp_path)` |
| `admin_only` | function | `tests/test_api_authz.py:328` | `def admin_only()` |
| `g_check` | function | `tests/test_api_authz.py:318` | `def g_check()` |
| `secure` | function | `tests/test_api_authz.py:313` | `def secure()` |
| `test_allows_valid_key_in_bearer_header` | method | `tests/test_api_authz.py:333` | `def test_allows_valid_key_in_bearer_header(self, tmp_path)` |
| `test_allows_valid_key_in_query_param` | method | `tests/test_api_authz.py:346` | `def test_allows_valid_key_in_query_param(self, tmp_path)` |
| `test_allows_valid_key_in_x_api_key_header` | method | `tests/test_api_authz.py:340` | `def test_allows_valid_key_in_x_api_key_header(self, tmp_path)` |
| `test_atomic_write_leaves_no_tmp_files` | method | `tests/test_api_authz.py:450` | `def test_atomic_write_leaves_no_tmp_files(self, tmp_path)` |
| `test_checks_permissions_with_set_operations` | method | `tests/test_api_authz.py:87` | `def test_checks_permissions_with_set_operations(self)` |
| `test_constant_time_comparison_rejects_wrong_secrets` | method | `tests/test_api_authz.py:435` | `def test_constant_time_comparison_rejects_wrong_secrets(self)` |
| `test_creates_and_lists_keys_scoped_by_tenant` | method | `tests/test_api_authz.py:114` | `def test_creates_and_lists_keys_scoped_by_tenant(self, tmp_path)` |
| `test_custom_overrides_preserve_typed_semantics` | method | `tests/test_api_authz.py:32` | `def test_custom_overrides_preserve_typed_semantics(self)` |
| `test_defaults_are_secure_by_default` | method | `tests/test_api_authz.py:24` | `def test_defaults_are_secure_by_default(self)` |
| `test_detects_expiration_correctly` | method | `tests/test_api_authz.py:65` | `def test_detects_expiration_correctly(self)` |
| `test_enforces_max_keys_per_tenant_raises_value_error` | method | `tests/test_api_authz.py:183` | `def test_enforces_max_keys_per_tenant_raises_value_error(self, tmp_path)` |
| `test_generates_50_unique_tokens_without_collision` | method | `tests/test_api_authz.py:444` | `def test_generates_50_unique_tokens_without_collision(self)` |
| `test_never_stores_plaintext_token_on_disk` | method | `tests/test_api_authz.py:275` | `def test_never_stores_plaintext_token_on_disk(self, tmp_path)` |
| `test_old_key_rejected_after_rotation_grace_expires` | method | `tests/test_api_authz.py:225` | `def test_old_key_rejected_after_rotation_grace_expires(self, tmp_path)` |
| `test_old_key_stays_valid_during_rotation_grace` | method | `tests/test_api_authz.py:217` | `def test_old_key_stays_valid_during_rotation_grace(self, tmp_path)` |
| `test_rejects_empty_plaintext_key` | method | `tests/test_api_authz.py:137` | `def test_rejects_empty_plaintext_key(self, tmp_path)` |
| `test_rejects_expired_key` | method | `tests/test_api_authz.py:141` | `def test_rejects_expired_key(self, tmp_path)` |
| `test_rejects_invalid_key_with_401` | method | `tests/test_api_authz.py:357` | `def test_rejects_invalid_key_with_401(self, tmp_path)` |
| `test_rejects_key_with_insufficient_permissions_with_403` | method | `tests/test_api_authz.py:362` | `def test_rejects_key_with_insufficient_permissions_with_403(self, tmp_path)` |
| `test_rejects_missing_key_with_401` | method | `tests/test_api_authz.py:352` | `def test_rejects_missing_key_with_401(self, tmp_path)` |
| `test_rejects_unknown_key_returning_none` | method | `tests/test_api_authz.py:133` | `def test_rejects_unknown_key_returning_none(self, tmp_path)` |
| `test_retired_keys_are_pruned_after_grace_expires` | method | `tests/test_api_authz.py:240` | `def test_retired_keys_are_pruned_after_grace_expires(self, tmp_path)` |
| `test_returns_a_validatable_token` | method | `tests/test_api_authz.py:389` | `def test_returns_a_validatable_token(self, tmp_path)` |
| `test_revocation_is_idempotent` | method | `tests/test_api_authz.py:179` | `def test_revocation_is_idempotent(self, tmp_path)` |
| `test_revokes_key_preventing_future_validation` | method | `tests/test_api_authz.py:173` | `def test_revokes_key_preventing_future_validation(self, tmp_path)` |
| `test_rotates_key_preserving_tenant_label_and_permissions` | method | `tests/test_api_authz.py:196` | `def test_rotates_key_preserving_tenant_label_and_permissions(self, tmp_path)` |
| `test_rotation_copies_permissions_from_the_rotated_key` | method | `tests/test_api_authz.py:206` | `def test_rotation_copies_permissions_from_the_rotated_key(self, tmp_path)` |
| `test_rotation_does_not_grow_active_key_count` | method | `tests/test_api_authz.py:258` | `def test_rotation_does_not_grow_active_key_count(self, tmp_path)` |
| `test_serialization_roundtrip_preserves_all_fields` | method | `tests/test_api_authz.py:48` | `def test_serialization_roundtrip_preserves_all_fields(self)` |
| `test_sets_expiration_when_days_are_provided` | method | `tests/test_api_authz.py:412` | `def test_sets_expiration_when_days_are_provided(self, tmp_path)` |
| `test_sets_g_variables_with_api_key_context_on_success` | method | `tests/test_api_authz.py:368` | `def test_sets_g_variables_with_api_key_context_on_success(self, tmp_path)` |
| `test_stores_permissions_on_the_key_record` | method | `tests/test_api_authz.py:397` | `def test_stores_permissions_on_the_key_record(self, tmp_path)` |
| `test_updates_last_used_on_successful_validation` | method | `tests/test_api_authz.py:162` | `def test_updates_last_used_on_successful_validation(self, tmp_path)` |
| `test_validates_a_known_key_and_returns_record` | method | `tests/test_api_authz.py:125` | `def test_validates_a_known_key_and_returns_record(self, tmp_path)` |
| `TestApiKeyWiredIntoParams` | class | `tests/test_api_key_resolution.py:21` | `class TestApiKeyWiredIntoParams` |
| `TestReplaceCommandPlaceholders` | class | `tests/test_api_key_resolution.py:39` | `class TestReplaceCommandPlaceholders` |
| `test_class_attribute_api_key_reads_payload` | method | `tests/test_api_key_resolution.py:34` | `def test_class_attribute_api_key_reads_payload(self)` |
| `test_double_brace_substitution` | method | `tests/test_api_key_resolution.py:40` | `def test_double_brace_substitution(self)` |
| `test_missing_key_left_intact` | method | `tests/test_api_key_resolution.py:63` | `def test_missing_key_left_intact(self)` |
| `test_mixed_braces_in_one_command` | method | `tests/test_api_key_resolution.py:56` | `def test_mixed_braces_in_one_command(self)` |
| `test_params_api_key_binds_config_attr` | method | `tests/test_api_key_resolution.py:28` | `def test_params_api_key_binds_config_attr(self)` |
| `test_params_api_key_is_not_hardcoded_none` | method | `tests/test_api_key_resolution.py:22` | `def test_params_api_key_is_not_hardcoded_none(self)` |
| `test_single_brace_substitution` | method | `tests/test_api_key_resolution.py:47` | `def test_single_brace_substitution(self)` |
| `_auth` | function | `tests/test_api_v1.py:40` | `def _auth(token)` |
| `api_client` | function | `tests/test_api_v1.py:23` | `def api_client(tmp_path)` |
| `test_campaigns_empty_state` | function | `tests/test_api_v1.py:95` | `def test_campaigns_empty_state(api_client)` |
| `test_campaigns_reads_state_files` | function | `tests/test_api_v1.py:101` | `def test_campaigns_reads_state_files(api_client)` |
| `test_health_is_public` | function | `tests/test_api_v1.py:44` | `def test_health_is_public(api_client)` |
| `test_mutating_endpoints_require_auth` | function | `tests/test_api_v1.py:134` | `def test_mutating_endpoints_require_auth(api_client)` |
| `test_results_empty` | function | `tests/test_api_v1.py:76` | `def test_results_empty(api_client)` |
| `test_results_per_client` | function | `tests/test_api_v1.py:82` | `def test_results_per_client(api_client)` |
| `test_targets_empty_workspace` | function | `tests/test_api_v1.py:56` | `def test_targets_empty_workspace(api_client)` |
| `test_targets_lists_hosts_with_services` | function | `tests/test_api_v1.py:64` | `def test_targets_lists_hosts_with_services(api_client)` |
| `test_targets_requires_auth` | function | `tests/test_api_v1.py:51` | `def test_targets_requires_auth(api_client)` |
| `test_webhook_crud` | function | `tests/test_api_v1.py:109` | `def test_webhook_crud(api_client)` |
| `test_webhook_rejects_bad_url` | function | `tests/test_api_v1.py:126` | `def test_webhook_rejects_bad_url(api_client)` |
| `gate_env` | function | `tests/test_asset_gate.py:18` | `def gate_env(tmp_path, monkeypatch)` |
| `test_compact_unfolded_cap_and_flag` | function | `tests/test_asset_gate.py:157` | `def test_compact_unfolded_cap_and_flag(gate_env)` |
| `test_digest_overview_expandable` | function | `tests/test_asset_gate.py:174` | `def test_digest_overview_expandable(gate_env)` |
| `test_gate_blocks_asset_insert` | function | `tests/test_asset_gate.py:57` | `def test_gate_blocks_asset_insert(gate_env)` |
| `test_gate_cidr_match` | function | `tests/test_asset_gate.py:36` | `def test_gate_cidr_match(gate_env)` |
| `test_gate_exact_and_fuzzy_match` | function | `tests/test_asset_gate.py:25` | `def test_gate_exact_and_fuzzy_match(gate_env)` |
| `test_gate_task_allow_is_closed_whitelist` | function | `tests/test_asset_gate.py:43` | `def test_gate_task_allow_is_closed_whitelist(gate_env)` |
| `test_hot_facts_never_truncated` | function | `tests/test_asset_gate.py:194` | `def test_hot_facts_never_truncated(gate_env)` |
| `test_intel_nodes_carry_community` | function | `tests/test_asset_gate.py:126` | `def test_intel_nodes_carry_community()` |
| `test_intel_payload_readmenator_shape` | function | `tests/test_asset_gate.py:136` | `def test_intel_payload_readmenator_shape()` |
| `test_intel_template_embedded_in_lazyown_chrome` | function | `tests/test_asset_gate.py:94` | `def test_intel_template_embedded_in_lazyown_chrome()` |
| `test_intel_template_maps_edges_to_links` | function | `tests/test_asset_gate.py:106` | `def test_intel_template_maps_edges_to_links()` |
| `test_intel_template_readmenator_grade` | function | `tests/test_asset_gate.py:114` | `def test_intel_template_readmenator_grade()` |
| `test_intel_template_uses_vendored_libs` | function | `tests/test_asset_gate.py:83` | `def test_intel_template_uses_vendored_libs()` |
| `test_lazy_gate_surface` | function | `tests/test_asset_gate.py:66` | `def test_lazy_gate_surface()` |
| `test_traffic_clear` | function | `tests/test_asset_gate.py:75` | `def test_traffic_clear(gate_env)` |
| `_fixture_sessions` | function | `tests/test_attack_surface3d.py:24` | `def _fixture_sessions(tmp_path)` |
| `test_attack_bundle_payload` | function | `tests/test_attack_surface3d.py:72` | `def test_attack_bundle_payload(tmp_path)` |
| `test_attack_fuses_surface_and_intel` | function | `tests/test_attack_surface3d.py:47` | `def test_attack_fuses_surface_and_intel(tmp_path)` |
| `test_attack_menu_entry_and_routes` | function | `tests/test_attack_surface3d.py:129` | `def test_attack_menu_entry_and_routes()` |
| `test_attack_pages_embedded_and_wired` | function | `tests/test_attack_surface3d.py:109` | `def test_attack_pages_embedded_and_wired()` |
| `test_attack_payload_readmenator_shape` | function | `tests/test_attack_surface3d.py:59` | `def test_attack_payload_readmenator_shape(tmp_path)` |
| `test_attack_summary_feeds_loop` | function | `tests/test_attack_surface3d.py:93` | `def test_attack_summary_feeds_loop(tmp_path)` |
| `test_new_endpoints_require_login_and_decoy` | function | `tests/test_attack_surface3d.py:144` | `def test_new_endpoints_require_login_and_decoy()` |
| `TestAddonExists` | class | `tests/test_attack_surface_addons.py:68` | `class TestAddonExists` |
| `TestCloudSploitSpecific` | class | `tests/test_attack_surface_addons.py:294` | `class TestCloudSploitSpecific` |
| `TestCommandTemplates` | class | `tests/test_attack_surface_addons.py:234` | `class TestCommandTemplates` |
| `TestFuzzAddonStructure` | class | `tests/test_attack_surface_addons.py:384` | `class TestFuzzAddonStructure` |
| `TestGrypeSpecific` | class | `tests/test_attack_surface_addons.py:333` | `class TestGrypeSpecific` |
| `TestNoHardcodedSecrets` | class | `tests/test_attack_surface_addons.py:207` | `class TestNoHardcodedSecrets` |
| `TestParams` | class | `tests/test_attack_surface_addons.py:151` | `class TestParams` |
| `TestPathSafety` | class | `tests/test_attack_surface_addons.py:180` | `class TestPathSafety` |
| `TestProwlerSpecific` | class | `tests/test_attack_surface_addons.py:273` | `class TestProwlerSpecific` |
| `TestReportFullSpecific` | class | `tests/test_attack_surface_addons.py:353` | `class TestReportFullSpecific` |
| `TestRequiredFields` | class | `tests/test_attack_surface_addons.py:88` | `class TestRequiredFields` |
| `TestResultReview` | class | `tests/test_attack_surface_addons.py:418` | `class TestResultReview` |
| `TestScoutSuiteSpecific` | class | `tests/test_attack_surface_addons.py:251` | `class TestScoutSuiteSpecific` |
| `TestToolSection` | class | `tests/test_attack_surface_addons.py:118` | `class TestToolSection` |
| `TestTrivySpecific` | class | `tests/test_attack_surface_addons.py:309` | `class TestTrivySpecific` |
| `_all_addon_data` | function | `tests/test_attack_surface_addons.py:54` | `def _all_addon_data()` |
| `_load` | function | `tests/test_attack_surface_addons.py:36` | `def _load(path)` |
| `_loaded` | function | `tests/test_attack_surface_addons.py:59` | `def _loaded(name)` |
| `_param_names` | function | `tests/test_attack_surface_addons.py:41` | `def _param_names(addon)` |
| `_yaml_text` | function | `tests/test_attack_surface_addons.py:45` | `def _yaml_text(path)` |
| `addon` | method | `tests/test_attack_surface_addons.py:255` | `def addon(self)` |
| `addon` | method | `tests/test_attack_surface_addons.py:277` | `def addon(self)` |
| `addon` | method | `tests/test_attack_surface_addons.py:298` | `def addon(self)` |
| `addon` | method | `tests/test_attack_surface_addons.py:313` | `def addon(self)` |
| `addon` | method | `tests/test_attack_surface_addons.py:337` | `def addon(self)` |
| `addon` | method | `tests/test_attack_surface_addons.py:357` | `def addon(self)` |
| `no_duplicate_param_names` | method | `tests/test_attack_surface_addons.py:170` | `def no_duplicate_param_names(self, name, addon)` |
| `test_category_falls_in_known_range` | method | `tests/test_attack_surface_addons.py:396` | `def test_category_falls_in_known_range(self, name, addon)` |
| `test_category_is_recon_or_scan` | method | `tests/test_attack_surface_addons.py:290` | `def test_category_is_recon_or_scan(self, addon)` |
| `test_category_is_reporting` | method | `tests/test_attack_surface_addons.py:363` | `def test_category_is_reporting(self, addon)` |
| `test_description_is_string` | method | `tests/test_attack_surface_addons.py:101` | `def test_description_is_string(self, name, addon)` |
| `test_description_mentions_vulnerability` | method | `tests/test_attack_surface_addons.py:349` | `def test_description_mentions_vulnerability(self, addon)` |
| `test_each_param_has_description` | method | `tests/test_attack_surface_addons.py:165` | `def test_each_param_has_description(self, name, addon)` |
| `test_each_param_has_name` | method | `tests/test_attack_surface_addons.py:160` | `def test_each_param_has_name(self, name, addon)` |
| `test_enabled_is_true` | method | `tests/test_attack_surface_addons.py:107` | `def test_enabled_is_true(self, name, addon)` |
| `test_execute_calls_report_generator` | method | `tests/test_attack_surface_addons.py:371` | `def test_execute_calls_report_generator(self, addon)` |
| `test_execute_command_is_string` | method | `tests/test_attack_surface_addons.py:141` | `def test_execute_command_is_string(self, name, addon)` |
| `test_execute_has_at_least_one_placeholder` | method | `tests/test_attack_surface_addons.py:238` | `def test_execute_has_at_least_one_placeholder(self, name, addon)` |
| `test_file_present` | method | `tests/test_attack_surface_addons.py:72` | `def test_file_present(self, name, path)` |
| `test_has_cloud_param` | method | `tests/test_attack_surface_addons.py:304` | `def test_has_cloud_param(self, addon)` |
| `test_has_provider_param` | method | `tests/test_attack_surface_addons.py:267` | `def test_has_provider_param(self, addon)` |
| `test_has_provider_param` | method | `tests/test_attack_surface_addons.py:286` | `def test_has_provider_param(self, addon)` |
| `test_has_region_param` | method | `tests/test_attack_surface_addons.py:264` | `def test_has_region_param(self, addon)` |
| `test_has_required_fields` | method | `tests/test_attack_surface_addons.py:92` | `def test_has_required_fields(self, name, addon)` |
| `test_has_target_param` | method | `tests/test_attack_surface_addons.py:322` | `def test_has_target_param(self, addon)` |
| `test_has_target_param` | method | `tests/test_attack_surface_addons.py:343` | `def test_has_target_param(self, addon)` |
| `test_install_path_contained` | method | `tests/test_attack_surface_addons.py:184` | `def test_install_path_contained(self, name, addon)` |
| `test_install_path_is_dot` | method | `tests/test_attack_surface_addons.py:366` | `def test_install_path_is_dot(self, addon)` |
| `test_install_path_no_dot_dot_prefix` | method | `tests/test_attack_surface_addons.py:190` | `def test_install_path_no_dot_dot_prefix(self, name, addon)` |
| `test_name` | method | `tests/test_attack_surface_addons.py:258` | `def test_name(self, addon)` |
| `test_name` | method | `tests/test_attack_surface_addons.py:280` | `def test_name(self, addon)` |
| `test_name` | method | `tests/test_attack_surface_addons.py:301` | `def test_name(self, addon)` |
| `test_name` | method | `tests/test_attack_surface_addons.py:316` | `def test_name(self, addon)` |
| `test_name` | method | `tests/test_attack_surface_addons.py:340` | `def test_name(self, addon)` |
| `test_name` | method | `tests/test_attack_surface_addons.py:360` | `def test_name(self, addon)` |
| `test_name_is_string` | method | `tests/test_attack_surface_addons.py:97` | `def test_name_is_string(self, name, addon)` |
| `test_name_lowercase` | method | `tests/test_attack_surface_addons.py:392` | `def test_name_lowercase(self, name, addon)` |
| `test_name_no_spaces` | method | `tests/test_attack_surface_addons.py:388` | `def test_name_no_spaces(self, name, addon)` |
| `test_no_hardcoded_ip` | method | `tests/test_attack_surface_addons.py:211` | `def test_no_hardcoded_ip(self, name, addon)` |
| `test_no_password_literals` | method | `tests/test_attack_surface_addons.py:223` | `def test_no_password_literals(self, name, addon)` |
| `test_no_tilde_in_paths` | method | `tests/test_attack_surface_addons.py:197` | `def test_no_tilde_in_paths(self, name, addon)` |
| `test_no_well_known_ports` | method | `tests/test_attack_surface_addons.py:217` | `def test_no_well_known_ports(self, name, addon)` |
| `test_os_is_containers` | method | `tests/test_attack_surface_addons.py:319` | `def test_os_is_containers(self, addon)` |
| `test_os_is_iaas` | method | `tests/test_attack_surface_addons.py:261` | `def test_os_is_iaas(self, addon)` |
| `test_os_is_iaas` | method | `tests/test_attack_surface_addons.py:283` | `def test_os_is_iaas(self, addon)` |
| `test_os_is_known_value` | method | `tests/test_attack_surface_addons.py:407` | `def test_os_is_known_value(self, name, addon)` |
| `test_params_is_list_when_present` | method | `tests/test_attack_surface_addons.py:155` | `def test_params_is_list_when_present(self, name, addon)` |
| `test_repo_url_ends_with_git` | method | `tests/test_attack_surface_addons.py:131` | `def test_repo_url_ends_with_git(self, name, addon)` |
| `test_repo_url_is_https` | method | `tests/test_attack_surface_addons.py:136` | `def test_repo_url_is_https(self, name, addon)` |
| `test_repo_url_points_to_lazyown` | method | `tests/test_attack_surface_addons.py:375` | `def test_repo_url_points_to_lazyown(self, addon)` |
| `test_summary_table` | method | `tests/test_attack_surface_addons.py:421` | `def test_summary_table(self)` |
| `test_tool_is_dict` | method | `tests/test_attack_surface_addons.py:122` | `def test_tool_is_dict(self, name, addon)` |
| `test_tool_required_keys` | method | `tests/test_attack_surface_addons.py:126` | `def test_tool_required_keys(self, name, addon)` |
| `test_trigger_is_list_when_present` | method | `tests/test_attack_surface_addons.py:402` | `def test_trigger_is_list_when_present(self, name, addon)` |
| `test_triggers_docker` | method | `tests/test_attack_surface_addons.py:328` | `def test_triggers_docker(self, addon)` |
| `test_yaml_parses` | method | `tests/test_attack_surface_addons.py:76` | `def test_yaml_parses(self, name, path)` |
| `TestAutoCryptoConfig` | class | `tests/test_auto_crypto.py:33` | `class TestAutoCryptoConfig` |
| `TestAutoCryptoEngine` | class | `tests/test_auto_crypto.py:54` | `class TestAutoCryptoEngine` |
| `TestExitEncryptWiring` | class | `tests/test_auto_crypto.py:169` | `class TestExitEncryptWiring` |
| `TestHasPassword` | class | `tests/test_auto_crypto.py:152` | `class TestHasPassword` |
| `TestPasswordProvider` | class | `tests/test_auto_crypto.py:144` | `class TestPasswordProvider` |
| `_stub_shell` | method | `tests/test_auto_crypto.py:172` | `def _stub_shell(self, calls)` |
| `crypto_module` | function | `tests/test_auto_crypto.py:21` | `def crypto_module()` |
| `test_build_provider_returns_callable` | method | `tests/test_auto_crypto.py:145` | `def test_build_provider_returns_callable(self)` |
| `test_custom_config` | method | `tests/test_auto_crypto.py:42` | `def test_custom_config(self, crypto_module)` |
| `test_default_config` | method | `tests/test_auto_crypto.py:34` | `def test_default_config(self, crypto_module)` |
| `test_disabled_engine_is_noop` | method | `tests/test_auto_crypto.py:55` | `def test_disabled_engine_is_noop(self, crypto_module, tmp_sessions)` |
| `test_empty_directory_is_not_encrypted` | method | `tests/test_auto_crypto.py:77` | `def test_empty_directory_is_not_encrypted(self, crypto_module, tmp_sessions)` |
| `test_encrypt_decrypt_roundtrip` | method | `tests/test_auto_crypto.py:86` | `def test_encrypt_decrypt_roundtrip(self, crypto_module, tmp_sessions)` |
| `test_eof_encrypts_before_returning` | method | `tests/test_auto_crypto.py:211` | `def test_eof_encrypts_before_returning(self, monkeypatch)` |
| `test_exit_encrypts_after_confirmation` | method | `tests/test_auto_crypto.py:194` | `def test_exit_encrypts_after_confirmation(self, monkeypatch)` |
| `test_false_when_provider_returns_empty` | method | `tests/test_auto_crypto.py:163` | `def test_false_when_provider_returns_empty(self, crypto_module, tmp_sessions)` |
| `test_false_without_provider` | method | `tests/test_auto_crypto.py:153` | `def test_false_without_provider(self, crypto_module, tmp_sessions)` |
| `test_no_password_provider_returns_false` | method | `tests/test_auto_crypto.py:66` | `def test_no_password_provider_returns_false(self, crypto_module, tmp_sessions)` |
| `test_qa_encrypts_before_exit` | method | `tests/test_auto_crypto.py:180` | `def test_qa_encrypts_before_exit(self, monkeypatch)` |
| `test_salt_is_persisted` | method | `tests/test_auto_crypto.py:122` | `def test_salt_is_persisted(self, crypto_module, tmp_sessions)` |
| `test_true_with_provider` | method | `tests/test_auto_crypto.py:158` | `def test_true_with_provider(self, crypto_module, tmp_sessions)` |
| `tmp_sessions` | function | `tests/test_auto_crypto.py:28` | `def tmp_sessions()` |
| `_FakeShell` | class | `tests/test_auto_registry.py:73` | `class _FakeShell` |
| `_HangingShell` | class | `tests/test_auto_registry.py:86` | `class _HangingShell` |
| `__init__` | method | `tests/test_auto_registry.py:76` | `def __init__(self, output)` |
| `_run` | function | `tests/test_auto_registry.py:169` | `def _run()` |
| `onecmd` | method | `tests/test_auto_registry.py:89` | `def onecmd(self, command)` |
| `onecmd_plus_hooks` | method | `tests/test_auto_registry.py:80` | `def onecmd_plus_hooks(self, command)` |
| `test_build_command_binds_target` | function | `tests/test_auto_registry.py:38` | `def test_build_command_binds_target()` |
| `test_cancel_running_commands_kills_streaming` | function | `tests/test_auto_registry.py:160` | `def test_cancel_running_commands_kills_streaming()` |
| `test_execute_shell_verb_captures_output` | function | `tests/test_auto_registry.py:96` | `def test_execute_shell_verb_captures_output()` |
| `test_execute_shell_verb_rejects_non_verbs` | function | `tests/test_auto_registry.py:104` | `def test_execute_shell_verb_rejects_non_verbs()` |
| `test_execute_shell_verb_timeout_never_hangs` | function | `tests/test_auto_registry.py:112` | `def test_execute_shell_verb_timeout_never_hangs()` |
| `test_execute_shell_verb_without_shell` | function | `tests/test_auto_registry.py:118` | `def test_execute_shell_verb_without_shell()` |
| `test_is_shell_verb_matches_first_token` | function | `tests/test_auto_registry.py:47` | `def test_is_shell_verb_matches_first_token()` |
| `test_missing_binary_skips_builtins_paths_and_scripts` | function | `tests/test_auto_registry.py:134` | `def test_missing_binary_skips_builtins_paths_and_scripts(monkeypatch)` |
| `test_propose_and_steps_skip_unavailable_verbs` | function | `tests/test_auto_registry.py:144` | `def test_propose_and_steps_skip_unavailable_verbs(monkeypatch)` |
| `test_propose_and_translate_roundtrip` | function | `tests/test_auto_registry.py:63` | `def test_propose_and_translate_roundtrip()` |
| `test_registry_covers_auto_family` | function | `tests/test_auto_registry.py:28` | `def test_registry_covers_auto_family()` |
| `test_steps_for_uses_next_available_keyword_verb` | function | `tests/test_auto_registry.py:154` | `def test_steps_for_uses_next_available_keyword_verb(monkeypatch)` |
| `test_verb_gap_flags_missing_tooling` | function | `tests/test_auto_registry.py:124` | `def test_verb_gap_flags_missing_tooling(monkeypatch)` |
| `test_verbs_for_matches_keywords` | function | `tests/test_auto_registry.py:55` | `def test_verbs_for_matches_keywords()` |
| `boom` | function | `tests/test_autonomous_ops.py:101` | `def boom(_prompt)` |
| `test_c04_dedup_anchor_coverage` | function | `tests/test_autonomous_ops.py:11` | `def test_c04_dedup_anchor_coverage()` |
| `test_c04_mirror_to_campaign_db` | function | `tests/test_autonomous_ops.py:26` | `def test_c04_mirror_to_campaign_db(tmp_path)` |
| `test_c05_frontier_emits_once_then_empty` | function | `tests/test_autonomous_ops.py:43` | `def test_c05_frontier_emits_once_then_empty()` |
| `test_c05_todo_blocks_lateral_until_creds` | function | `tests/test_autonomous_ops.py:58` | `def test_c05_todo_blocks_lateral_until_creds()` |
| `test_c06_finding_lifecycle_on_campaign_db` | function | `tests/test_autonomous_ops.py:70` | `def test_c06_finding_lifecycle_on_campaign_db(tmp_path)` |
| `test_c07_pool_failover_and_exhaustion` | function | `tests/test_autonomous_ops.py:98` | `def test_c07_pool_failover_and_exhaustion()` |
| `test_c08_notify_filter_and_redact` | function | `tests/test_autonomous_ops.py:116` | `def test_c08_notify_filter_and_redact()` |
| `test_c09_side_question_isolated` | function | `tests/test_autonomous_ops.py:128` | `def test_c09_side_question_isolated()` |
| `test_c10_rollback_restores_previous` | function | `tests/test_autonomous_ops.py:159` | `def test_c10_rollback_restores_previous(tmp_path)` |
| `test_c10_verify_rejects_bad_checksum` | function | `tests/test_autonomous_ops.py:143` | `def test_c10_verify_rejects_bad_checksum(tmp_path)` |
| `test_i2_pool_hard_trips_on_auth_errors` | function | `tests/test_autonomous_ops.py:186` | `def test_i2_pool_hard_trips_on_auth_errors()` |
| `test_i2_shared_registry_survives_rebuilds` | function | `tests/test_autonomous_ops.py:171` | `def test_i2_shared_registry_survives_rebuilds()` |
| `test_i3_classify_retest_verdicts` | function | `tests/test_autonomous_ops.py:194` | `def test_i3_classify_retest_verdicts()` |
| `test_i3_retest_bumps_evidence_version` | function | `tests/test_autonomous_ops.py:203` | `def test_i3_retest_bumps_evidence_version(tmp_path)` |
| `test_i4_shared_engine_cooldown` | function | `tests/test_autonomous_ops.py:224` | `def test_i4_shared_engine_cooldown()` |
| `test_i4_should_rescan_honours_fresh_scans` | function | `tests/test_autonomous_ops.py:232` | `def test_i4_should_rescan_honours_fresh_scans(tmp_path)` |
| `_Runner` | class | `tests/test_autonomous_replay.py:161` | `class _Runner` |
| `_Runner` | class | `tests/test_autonomous_replay.py:185` | `class _Runner` |
| `__init__` | method | `tests/test_autonomous_replay.py:162` | `def __init__(self)` |
| `_event` | function | `tests/test_autonomous_replay.py:40` | `def _event(event_id, objective_id, step, command, source, seed_override)` |
| `_write_jsonl` | function | `tests/test_autonomous_replay.py:65` | `def _write_jsonl(path, events)` |
| `run` | method | `tests/test_autonomous_replay.py:165` | `def run(self, command, timeout)` |
| `run` | method | `tests/test_autonomous_replay.py:186` | `def run(self, command, timeout)` |
| `test_event_log_reader_returns_empty_when_missing` | function | `tests/test_autonomous_replay.py:71` | `def test_event_log_reader_returns_empty_when_missing(tmp_path)` |
| `test_event_log_reader_skips_malformed_lines` | function | `tests/test_autonomous_replay.py:78` | `def test_event_log_reader_skips_malformed_lines(tmp_path)` |
| `test_execute_marks_runner_errors_as_failure` | function | `tests/test_autonomous_replay.py:179` | `def test_execute_marks_runner_errors_as_failure(tmp_path)` |
| `test_execute_runs_commands_through_injected_runner` | function | `tests/test_autonomous_replay.py:149` | `def test_execute_runs_commands_through_injected_runner(tmp_path)` |
| `test_replay_convenience_returns_dict` | function | `tests/test_autonomous_replay.py:195` | `def test_replay_convenience_returns_dict(tmp_path)` |
| `test_replay_rejects_unknown_mode` | function | `tests/test_autonomous_replay.py:206` | `def test_replay_rejects_unknown_mode(tmp_path)` |
| `test_slice_is_inclusive_on_both_bounds` | function | `tests/test_autonomous_replay.py:96` | `def test_slice_is_inclusive_on_both_bounds(tmp_path)` |
| `test_step_skips_events_without_command` | function | `tests/test_autonomous_replay.py:221` | `def test_step_skips_events_without_command(tmp_path)` |
| `test_supported_modes_constant` | function | `tests/test_autonomous_replay.py:215` | `def test_supported_modes_constant()` |
| `test_trace_detects_decision_seed_divergence` | function | `tests/test_autonomous_replay.py:131` | `def test_trace_detects_decision_seed_divergence(tmp_path)` |
| `test_trace_returns_one_step_per_event` | function | `tests/test_autonomous_replay.py:112` | `def test_trace_returns_one_step_per_event(tmp_path)` |
| `_CapturingConsole` | class | `tests/test_autosuggest.py:295` | `class _CapturingConsole` |
| `_FakeAdvisor` | class | `tests/test_autosuggest.py:203` | `class _FakeAdvisor` |
| `_RaisingProvider` | class | `tests/test_autosuggest.py:52` | `class _RaisingProvider` |
| `_SequenceProvider` | class | `tests/test_autosuggest.py:339` | `class _SequenceProvider` |
| `_StaticProvider` | class | `tests/test_autosuggest.py:42` | `class _StaticProvider` |
| `__init__` | method | `tests/test_autosuggest.py:45` | `def __init__(self, suggestion)` |
| `__init__` | method | `tests/test_autosuggest.py:204` | `def __init__(self, results, available)` |
| `__init__` | method | `tests/test_autosuggest.py:296` | `def __init__(self)` |
| `__init__` | method | `tests/test_autosuggest.py:342` | `def __init__(self, suggestions)` |
| `is_available` | method | `tests/test_autosuggest.py:208` | `def is_available(self)` |
| `print` | method | `tests/test_autosuggest.py:299` | `def print(self, value)` |
| `suggest` | method | `tests/test_autosuggest.py:48` | `def suggest(self, context)` |
| `suggest` | method | `tests/test_autosuggest.py:55` | `def suggest(self, context)` |
| `suggest` | method | `tests/test_autosuggest.py:346` | `def suggest(self, context)` |
| `suggest_next` | method | `tests/test_autosuggest.py:211` | `def suggest_next(self, recent_commands, limit)` |
| `test_build_default_engine_includes_killchain_only_when_no_advisor` | function | `tests/test_autosuggest.py:246` | `def test_build_default_engine_includes_killchain_only_when_no_advisor()` |
| `test_build_default_engine_with_unavailable_advisor` | function | `tests/test_autosuggest.py:372` | `def test_build_default_engine_with_unavailable_advisor()` |
| `test_composite_picks_highest_score` | function | `tests/test_autosuggest.py:133` | `def test_composite_picks_highest_score()` |
| `test_composite_returns_none_when_no_provider_responds` | function | `tests/test_autosuggest.py:152` | `def test_composite_returns_none_when_no_provider_responds()` |
| `test_composite_skips_raising_provider` | function | `tests/test_autosuggest.py:143` | `def test_composite_skips_raising_provider()` |
| `test_engine_accept_returns_command_and_clears` | function | `tests/test_autosuggest.py:69` | `def test_engine_accept_returns_command_and_clears()` |
| `test_engine_advances_suggestion_after_accept_refresh` | function | `tests/test_autosuggest.py:354` | `def test_engine_advances_suggestion_after_accept_refresh()` |
| `test_engine_disabled_clears_state_and_returns_none` | function | `tests/test_autosuggest.py:81` | `def test_engine_disabled_clears_state_and_returns_none()` |
| `test_engine_display_text_empty_without_suggestion` | function | `tests/test_autosuggest.py:102` | `def test_engine_display_text_empty_without_suggestion()` |
| `test_engine_display_text_renders_active_suggestion` | function | `tests/test_autosuggest.py:108` | `def test_engine_display_text_renders_active_suggestion()` |
| `test_engine_display_text_truncates_long_command` | function | `tests/test_autosuggest.py:119` | `def test_engine_display_text_truncates_long_command()` |
| `test_engine_refresh_stores_suggestion` | function | `tests/test_autosuggest.py:59` | `def test_engine_refresh_stores_suggestion()` |
| `test_engine_skip_commands_do_not_refresh` | function | `tests/test_autosuggest.py:93` | `def test_engine_skip_commands_do_not_refresh()` |
| `test_format_hint_line_includes_accept_key_and_reason` | function | `tests/test_autosuggest.py:261` | `def test_format_hint_line_includes_accept_key_and_reason()` |
| `test_format_hint_line_omits_reason_when_blank` | function | `tests/test_autosuggest.py:287` | `def test_format_hint_line_omits_reason_when_blank()` |
| `test_format_hint_line_truncates_long_command` | function | `tests/test_autosuggest.py:275` | `def test_format_hint_line_truncates_long_command()` |

Next: [SYMBOLS_p30.md](SYMBOLS_p30.md)
