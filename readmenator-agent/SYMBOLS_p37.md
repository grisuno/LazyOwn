# Symbols (page 37 of 46)
Previous: [SYMBOLS_p36.md](SYMBOLS_p36.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `plan` | method | `tests/test_daemon_loop.py:76` | `def plan(self, _target, max_candidates)` |
| `plan` | method | `tests/test_daemon_loop.py:173` | `def plan(self, target, max_candidates)` |
| `register_output` | method | `tests/test_daemon_loop.py:70` | `def register_output(self, _output, _command, platform, success)` |
| `snapshot` | method | `tests/test_daemon_loop.py:39` | `def snapshot(self)` |
| `test_decompose_goal_splits_compound` | function | `tests/test_daemon_loop.py:197` | `def test_decompose_goal_splits_compound(tmp_path)` |
| `test_loop_ends_when_no_new_direction` | function | `tests/test_daemon_loop.py:126` | `def test_loop_ends_when_no_new_direction(monkeypatch, tmp_path)` |
| `test_loop_skips_duplicate_success` | function | `tests/test_daemon_loop.py:164` | `def test_loop_skips_duplicate_success(monkeypatch, tmp_path)` |
| `test_loop_skips_unapproved_gated_command` | function | `tests/test_daemon_loop.py:134` | `def test_loop_skips_unapproved_gated_command(monkeypatch, tmp_path)` |
| `test_loop_stops_when_objective_proven` | function | `tests/test_daemon_loop.py:155` | `def test_loop_stops_when_objective_proven(monkeypatch, tmp_path)` |
| `test_marker_helpers_extract_real_output` | function | `tests/test_daemon_loop.py:216` | `def test_marker_helpers_extract_real_output()` |
| `update_from_findings` | method | `tests/test_daemon_loop.py:43` | `def update_from_findings(self, _findings)` |
| `update_host` | method | `tests/test_daemon_loop.py:46` | `def update_host(self, _target)` |
| `TestDashboardIndexRoute` | class | `tests/test_dashboard_routes.py:391` | `class TestDashboardIndexRoute` |
| `TestLootRoute` | class | `tests/test_dashboard_routes.py:75` | `class TestLootRoute` |
| `TestTimelineRoute` | class | `tests/test_dashboard_routes.py:180` | `class TestTimelineRoute` |
| `_TestUser` | class | `tests/test_dashboard_routes.py:16` | `class _TestUser(UserMixin)` |
| `__init__` | method | `tests/test_dashboard_routes.py:17` | `def __init__(self, user_id)` |
| `_write_credentials_file` | function | `tests/test_dashboard_routes.py:45` | `def _write_credentials_file(sessions_dir, filename, lines)` |
| `_write_csv_report` | function | `tests/test_dashboard_routes.py:60` | `def _write_csv_report(sessions_dir, rows)` |
| `_write_events_jsonl` | function | `tests/test_dashboard_routes.py:69` | `def _write_events_jsonl(sessions_dir, events)` |
| `_write_hashes_file` | function | `tests/test_dashboard_routes.py:49` | `def _write_hashes_file(sessions_dir, filename, lines)` |
| `_write_loot_file` | function | `tests/test_dashboard_routes.py:53` | `def _write_loot_file(sessions_dir, rel_path, content)` |
| `client` | function | `tests/test_dashboard_routes.py:22` | `def client(tmp_path)` |
| `load_user` | function | `tests/test_dashboard_routes.py:34` | `def load_user(user_id)` |
| `test_dashboard_api_data_returns_json` | method | `tests/test_dashboard_routes.py:401` | `def test_dashboard_api_data_returns_json(self, client)` |
| `test_dashboard_index_returns_200` | method | `tests/test_dashboard_routes.py:394` | `def test_dashboard_index_returns_200(self, client)` |
| `test_loot_empty_returns_200` | method | `tests/test_dashboard_routes.py:107` | `def test_loot_empty_returns_200(self, client)` |
| `test_loot_multiple_credential_files` | method | `tests/test_dashboard_routes.py:165` | `def test_loot_multiple_credential_files(self, client)` |
| `test_loot_respects_max_entries` | method | `tests/test_dashboard_routes.py:148` | `def test_loot_respects_max_entries(self, client)` |
| `test_loot_route_returns_200_with_data` | method | `tests/test_dashboard_routes.py:78` | `def test_loot_route_returns_200_with_data(self, client)` |
| `test_loot_skips_comment_lines` | method | `tests/test_dashboard_routes.py:117` | `def test_loot_skips_comment_lines(self, client)` |
| `test_timeline_csv_without_timestamp` | method | `tests/test_dashboard_routes.py:278` | `def test_timeline_csv_without_timestamp(self, client)` |
| `test_timeline_empty_returns_200` | method | `tests/test_dashboard_routes.py:230` | `def test_timeline_empty_returns_200(self, client)` |
| `test_timeline_handles_csv_tool_column` | method | `tests/test_dashboard_routes.py:266` | `def test_timeline_handles_csv_tool_column(self, client)` |
| `test_timeline_handles_malformed_jsonl` | method | `tests/test_dashboard_routes.py:375` | `def test_timeline_handles_malformed_jsonl(self, client)` |
| `test_timeline_normalizes_iso_timestamps` | method | `tests/test_dashboard_routes.py:318` | `def test_timeline_normalizes_iso_timestamps(self, client)` |
| `test_timeline_only_csv_no_events` | method | `tests/test_dashboard_routes.py:360` | `def test_timeline_only_csv_no_events(self, client)` |
| `test_timeline_only_events_no_csv` | method | `tests/test_dashboard_routes.py:339` | `def test_timeline_only_events_no_csv(self, client)` |
| `test_timeline_respects_max_rows` | method | `tests/test_dashboard_routes.py:296` | `def test_timeline_respects_max_rows(self, client)` |
| `test_timeline_route_returns_200_with_data` | method | `tests/test_dashboard_routes.py:183` | `def test_timeline_route_returns_200_with_data(self, client)` |
| `test_timeline_sorted_newest_first` | method | `tests/test_dashboard_routes.py:238` | `def test_timeline_sorted_newest_first(self, client)` |
| `TestCountLinesInGlob` | class | `tests/test_dashboard_tui.py:44` | `class TestCountLinesInGlob` |
| `TestGraphHints` | class | `tests/test_dashboard_tui.py:131` | `class TestGraphHints` |
| `TestKillChainPhases` | class | `tests/test_dashboard_tui.py:117` | `class TestKillChainPhases` |
| `TestReadJson` | class | `tests/test_dashboard_tui.py:29` | `class TestReadJson` |
| `TestReadRecentCommands` | class | `tests/test_dashboard_tui.py:65` | `class TestReadRecentCommands` |
| `_make_transcript` | method | `tests/test_dashboard_tui.py:66` | `def _make_transcript(self, tmp_path, rows)` |
| `test_all_phases_present` | method | `tests/test_dashboard_tui.py:118` | `def test_all_phases_present(self)` |
| `test_counts_non_empty_lines` | method | `tests/test_dashboard_tui.py:45` | `def test_counts_non_empty_lines(self, tmp_path)` |
| `test_empty_file_returns_empty` | method | `tests/test_dashboard_tui.py:93` | `def test_empty_file_returns_empty(self, tmp_path)` |
| `test_empty_file_returns_zero` | method | `tests/test_dashboard_tui.py:51` | `def test_empty_file_returns_zero(self, tmp_path)` |
| `test_invalid_json_returns_empty_dict` | method | `tests/test_dashboard_tui.py:38` | `def test_invalid_json_returns_empty_dict(self, tmp_path)` |
| `test_missing_file_returns_empty` | method | `tests/test_dashboard_tui.py:89` | `def test_missing_file_returns_empty(self, tmp_path)` |
| `test_missing_file_returns_empty_dict` | method | `tests/test_dashboard_tui.py:35` | `def test_missing_file_returns_empty_dict(self, tmp_path)` |
| `test_multiple_files_summed` | method | `tests/test_dashboard_tui.py:59` | `def test_multiple_files_summed(self, tmp_path)` |
| `test_no_matching_files_returns_zero` | method | `tests/test_dashboard_tui.py:56` | `def test_no_matching_files_returns_zero(self, tmp_path)` |
| `test_phases_ordered` | method | `tests/test_dashboard_tui.py:125` | `def test_phases_ordered(self)` |
| `test_reads_recent_commands` | method | `tests/test_dashboard_tui.py:77` | `def test_reads_recent_commands(self, tmp_path)` |
| `test_reads_valid_file` | method | `tests/test_dashboard_tui.py:30` | `def test_reads_valid_file(self, tmp_path)` |
| `test_respects_window_limit` | method | `tests/test_dashboard_tui.py:98` | `def test_respects_window_limit(self, tmp_path)` |
| `test_returns_labels_from_advisor` | method | `tests/test_dashboard_tui.py:142` | `def test_returns_labels_from_advisor(self)` |
| `test_returns_list_on_exception` | method | `tests/test_dashboard_tui.py:137` | `def test_returns_list_on_exception(self)` |
| `test_returns_list_when_advisor_unavailable` | method | `tests/test_dashboard_tui.py:132` | `def test_returns_list_when_advisor_unavailable(self)` |
| `test_skips_empty_tool_rows` | method | `tests/test_dashboard_tui.py:105` | `def test_skips_empty_tool_rows(self, tmp_path)` |
| `TestLazyOwnDB` | class | `tests/test_db.py:28` | `class TestLazyOwnDB` |
| `fresh_db` | function | `tests/test_db.py:20` | `def fresh_db()` |
| `test_credential_storage` | method | `tests/test_db.py:94` | `def test_credential_storage(self, fresh_db)` |
| `test_csv_export` | method | `tests/test_db.py:105` | `def test_csv_export(self, fresh_db)` |
| `test_duplicate_workspace_returns_negative_one` | method | `tests/test_db.py:54` | `def test_duplicate_workspace_returns_negative_one(self, fresh_db)` |
| `test_host_crud` | method | `tests/test_db.py:60` | `def test_host_crud(self, fresh_db)` |
| `test_host_upsert_updates_existing` | method | `tests/test_db.py:73` | `def test_host_upsert_updates_existing(self, fresh_db)` |
| `test_initial_schema` | method | `tests/test_db.py:29` | `def test_initial_schema(self, fresh_db)` |
| `test_loot_and_notes` | method | `tests/test_db.py:151` | `def test_loot_and_notes(self, fresh_db)` |
| `test_nmap_xml_import` | method | `tests/test_db.py:114` | `def test_nmap_xml_import(self, fresh_db, tmp_path)` |
| `test_service_crud` | method | `tests/test_db.py:82` | `def test_service_crud(self, fresh_db)` |
| `test_workspace_create_and_list` | method | `tests/test_db.py:46` | `def test_workspace_create_and_list(self, fresh_db)` |
| `test_workspace_delete` | method | `tests/test_db.py:144` | `def test_workspace_delete(self, fresh_db)` |
| `test_control_match_is_fail` | function | `tests/test_defense_eval.py:55` | `def test_control_match_is_fail()` |
| `test_empty_datasets_are_inconclusive` | function | `tests/test_defense_eval.py:71` | `def test_empty_datasets_are_inconclusive()` |
| `test_json_array_datasets` | function | `tests/test_defense_eval.py:99` | `def test_json_array_datasets()` |
| `test_malformed_logs_raise` | function | `tests/test_defense_eval.py:105` | `def test_malformed_logs_raise()` |
| `test_missing_field_is_inconclusive` | function | `tests/test_defense_eval.py:63` | `def test_missing_field_is_inconclusive()` |
| `test_neq_operator` | function | `tests/test_defense_eval.py:88` | `def test_neq_operator()` |
| `test_number_canonicalization` | function | `tests/test_defense_eval.py:79` | `def test_number_canonicalization()` |
| `test_oversized_rule_rejected` | function | `tests/test_defense_eval.py:111` | `def test_oversized_rule_rejected()` |
| `test_parse_rule_accepts_and_rejects` | function | `tests/test_defense_eval.py:28` | `def test_parse_rule_accepts_and_rejects()` |
| `test_rule_pass_requires_control_clean` | function | `tests/test_defense_eval.py:43` | `def test_rule_pass_requires_control_clean()` |
| `_set_stage_params` | function | `tests/test_defense_stages.py:43` | `def _set_stage_params(monkeypatch, stage, params)` |
| `test_closedloop_tune_writes_comparison` | function | `tests/test_defense_stages.py:83` | `def test_closedloop_tune_writes_comparison(tmp_path, monkeypatch)` |
| `test_defense_validate_skips_without_rule` | function | `tests/test_defense_stages.py:77` | `def test_defense_validate_skips_without_rule(monkeypatch)` |
| `test_defense_validate_writes_result` | function | `tests/test_defense_stages.py:51` | `def test_defense_validate_writes_result(tmp_path, monkeypatch)` |
| `test_hunt_verify_skips_without_files` | function | `tests/test_defense_stages.py:141` | `def test_hunt_verify_skips_without_files(monkeypatch)` |
| `test_hunt_verify_writes_verification` | function | `tests/test_defense_stages.py:111` | `def test_hunt_verify_writes_verification(tmp_path, monkeypatch)` |
| `test_new_stages_declared` | function | `tests/test_defense_stages.py:29` | `def test_new_stages_declared()` |
| `test_yaml_profiles_load` | function | `tests/test_defense_stages.py:36` | `def test_yaml_profiles_load(tmp_path)` |
| `TestMissingDependencyError` | class | `tests/test_dependencies.py:82` | `class TestMissingDependencyError` |
| `TestOptionalAttr` | class | `tests/test_dependencies.py:146` | `class TestOptionalAttr` |
| `TestOptionalImportAbsent` | class | `tests/test_dependencies.py:113` | `class TestOptionalImportAbsent` |
| `TestOptionalImportPresent` | class | `tests/test_dependencies.py:102` | `class TestOptionalImportPresent` |
| `TestProbe` | class | `tests/test_dependencies.py:204` | `class TestProbe` |
| `TestRegistry` | class | `tests/test_dependencies.py:170` | `class TestRegistry` |
| `TestReport` | class | `tests/test_dependencies.py:220` | `class TestReport` |
| `TestUtilsIntegration` | class | `tests/test_dependencies.py:255` | `class TestUtilsIntegration` |
| `_run_in_subprocess` | function | `tests/test_dependencies.py:59` | `def _run_in_subprocess(snippet)` |
| `test_absent_dependency` | method | `tests/test_dependencies.py:213` | `def test_absent_dependency(self)` |
| `test_attribute_access_raises` | method | `tests/test_dependencies.py:120` | `def test_attribute_access_raises(self)` |
| `test_attributes_are_exposed` | method | `tests/test_dependencies.py:92` | `def test_attributes_are_exposed(self)` |
| `test_call_raises` | method | `tests/test_dependencies.py:125` | `def test_call_raises(self)` |
| `test_collect_returns_report` | method | `tests/test_dependencies.py:223` | `def test_collect_returns_report(self)` |
| `test_every_spec_is_fully_populated` | method | `tests/test_dependencies.py:173` | `def test_every_spec_is_fully_populated(self)` |
| `test_format_report_renders_markers` | method | `tests/test_dependencies.py:241` | `def test_format_report_renders_markers(self)` |
| `test_is_binary_present_uses_path_lookup` | method | `tests/test_dependencies.py:265` | `def test_is_binary_present_uses_path_lookup(self)` |
| `test_is_import_error_subclass` | method | `tests/test_dependencies.py:98` | `def test_is_import_error_subclass(self)` |
| `test_iteration_raises` | method | `tests/test_dependencies.py:135` | `def test_iteration_raises(self)` |
| `test_lazily_bound_dependency_is_registered` | method | `tests/test_dependencies.py:200` | `def test_lazily_bound_dependency_is_registered(self, import_name)` |
| `test_len_raises` | method | `tests/test_dependencies.py:140` | `def test_len_raises(self)` |
| `test_main_returns_exit_code` | method | `tests/test_dependencies.py:250` | `def test_main_returns_exit_code(self)` |
| `test_message_contains_pip_command` | method | `tests/test_dependencies.py:85` | `def test_message_contains_pip_command(self)` |
| `test_missing_and_ok_consistency` | method | `tests/test_dependencies.py:228` | `def test_missing_and_ok_consistency(self)` |
| `test_missing_attribute_returns_proxy` | method | `tests/test_dependencies.py:163` | `def test_missing_attribute_returns_proxy(self)` |
| `test_missing_module_returns_proxy` | method | `tests/test_dependencies.py:157` | `def test_missing_module_returns_proxy(self)` |
| `test_ok_report_has_no_missing` | method | `tests/test_dependencies.py:235` | `def test_ok_report_has_no_missing(self)` |
| `test_present_dependency` | method | `tests/test_dependencies.py:207` | `def test_present_dependency(self)` |
| `test_returns_falsy_proxy` | method | `tests/test_dependencies.py:116` | `def test_returns_falsy_proxy(self)` |
| `test_returns_real_attribute` | method | `tests/test_dependencies.py:149` | `def test_returns_real_attribute(self)` |
| `test_returns_real_module` | method | `tests/test_dependencies.py:105` | `def test_returns_real_module(self)` |
| `test_submodule_fallback` | method | `tests/test_dependencies.py:153` | `def test_submodule_fallback(self)` |
| `test_subscription_raises` | method | `tests/test_dependencies.py:130` | `def test_subscription_raises(self)` |
| `test_symbol_is_exported` | method | `tests/test_dependencies.py:259` | `def test_symbol_is_exported(self, name)` |
| `test_truthy_when_present` | method | `tests/test_dependencies.py:109` | `def test_truthy_when_present(self)` |
| `TestCaching` | class | `tests/test_detection_feed.py:68` | `class TestCaching` |
| `TestCategoryMap` | class | `tests/test_detection_feed.py:119` | `class TestCategoryMap` |
| `TestDetectionFeedInit` | class | `tests/test_detection_feed.py:14` | `class TestDetectionFeedInit` |
| `TestFeedbackAdjustment` | class | `tests/test_detection_feed.py:96` | `class TestFeedbackAdjustment` |
| `TestSigmaParsing` | class | `tests/test_detection_feed.py:27` | `class TestSigmaParsing` |
| `test_adjust_from_feedback` | method | `tests/test_detection_feed.py:102` | `def test_adjust_from_feedback(self, tmp_path)` |
| `test_adjust_from_feedback_no_file` | method | `tests/test_detection_feed.py:97` | `def test_adjust_from_feedback_no_file(self, tmp_path)` |
| `test_cache_and_load` | method | `tests/test_detection_feed.py:69` | `def test_cache_and_load(self, tmp_path)` |
| `test_category_mappings` | method | `tests/test_detection_feed.py:120` | `def test_category_mappings(self)` |
| `test_custom_sources` | method | `tests/test_detection_feed.py:20` | `def test_custom_sources(self, tmp_path)` |
| `test_default_init` | method | `tests/test_detection_feed.py:15` | `def test_default_init(self, tmp_path)` |
| `test_default_probability` | method | `tests/test_detection_feed.py:127` | `def test_default_probability(self)` |
| `test_extract_categories` | method | `tests/test_detection_feed.py:61` | `def test_extract_categories(self, tmp_path)` |
| `test_extract_keywords` | method | `tests/test_detection_feed.py:48` | `def test_extract_keywords(self, tmp_path)` |
| `test_extract_log_source` | method | `tests/test_detection_feed.py:28` | `def test_extract_log_source(self, tmp_path)` |
| `test_extract_log_source_minimal` | method | `tests/test_detection_feed.py:33` | `def test_extract_log_source_minimal(self, tmp_path)` |
| `test_extract_mitre` | method | `tests/test_detection_feed.py:38` | `def test_extract_mitre(self, tmp_path)` |
| `test_extract_mitre_none` | method | `tests/test_detection_feed.py:43` | `def test_extract_mitre_none(self, tmp_path)` |
| `test_load_cached_missing` | method | `tests/test_detection_feed.py:90` | `def test_load_cached_missing(self, tmp_path)` |
| `TestDirtyInitAddonExists` | class | `tests/test_dirtyinit_addon.py:48` | `class TestDirtyInitAddonExists` |
| `TestDirtyInitDriverContract` | class | `tests/test_dirtyinit_addon.py:175` | `class TestDirtyInitDriverContract` |
| `TestDirtyInitPlaceholders` | class | `tests/test_dirtyinit_addon.py:135` | `class TestDirtyInitPlaceholders` |
| `TestDirtyInitRequiredFields` | class | `tests/test_dirtyinit_addon.py:64` | `class TestDirtyInitRequiredFields` |
| `TestDirtyInitToolSection` | class | `tests/test_dirtyinit_addon.py:103` | `class TestDirtyInitToolSection` |
| `_load` | function | `tests/test_dirtyinit_addon.py:33` | `def _load(path)` |
| `addon` | function | `tests/test_dirtyinit_addon.py:39` | `def addon()` |
| `driver_text` | function | `tests/test_dirtyinit_addon.py:44` | `def driver_text()` |
| `test_addon_has_field` | method | `tests/test_dirtyinit_addon.py:66` | `def test_addon_has_field(self, addon, field)` |
| `test_addon_parses` | method | `tests/test_dirtyinit_addon.py:55` | `def test_addon_parses(self, addon)` |
| `test_addon_present` | method | `tests/test_dirtyinit_addon.py:49` | `def test_addon_present(self)` |
| `test_category` | method | `tests/test_dirtyinit_addon.py:84` | `def test_category(self, addon)` |
| `test_category_pattern` | method | `tests/test_dirtyinit_addon.py:87` | `def test_category_pattern(self, addon)` |
| `test_declared_params` | method | `tests/test_dirtyinit_addon.py:140` | `def test_declared_params(self, addon)` |
| `test_description_length` | method | `tests/test_dirtyinit_addon.py:78` | `def test_description_length(self, addon)` |
| `test_driver_builds_apk` | method | `tests/test_dirtyinit_addon.py:198` | `def test_driver_builds_apk(self, driver_text)` |
| `test_driver_exposes_action` | method | `tests/test_dirtyinit_addon.py:192` | `def test_driver_exposes_action(self, driver_text, action)` |
| `test_driver_falls_back_to_payload` | method | `tests/test_dirtyinit_addon.py:205` | `def test_driver_falls_back_to_payload(self, driver_text)` |
| `test_driver_has_no_hardcoded_host_paths` | method | `tests/test_dirtyinit_addon.py:209` | `def test_driver_has_no_hardcoded_host_paths(self, driver_text)` |
| `test_driver_help_runs` | method | `tests/test_dirtyinit_addon.py:213` | `def test_driver_help_runs(self)` |
| `test_driver_is_executable` | method | `tests/test_dirtyinit_addon.py:58` | `def test_driver_is_executable(self)` |
| `test_driver_present` | method | `tests/test_dirtyinit_addon.py:52` | `def test_driver_present(self)` |
| `test_driver_rejects_unknown_action` | method | `tests/test_dirtyinit_addon.py:233` | `def test_driver_rejects_unknown_action(self)` |
| `test_driver_resolves_repo_root` | method | `tests/test_dirtyinit_addon.py:185` | `def test_driver_resolves_repo_root(self, driver_text)` |
| `test_driver_status_runs` | method | `tests/test_dirtyinit_addon.py:223` | `def test_driver_status_runs(self)` |
| `test_driver_syntax` | method | `tests/test_dirtyinit_addon.py:176` | `def test_driver_syntax(self)` |
| `test_driver_targets_expected_package` | method | `tests/test_dirtyinit_addon.py:202` | `def test_driver_targets_expected_package(self, driver_text)` |
| `test_driver_uses_adb` | method | `tests/test_dirtyinit_addon.py:195` | `def test_driver_uses_adb(self, driver_text)` |
| `test_enabled` | method | `tests/test_dirtyinit_addon.py:81` | `def test_enabled(self, addon)` |
| `test_execute_command_is_complete` | method | `tests/test_dirtyinit_addon.py:131` | `def test_execute_command_is_complete(self, addon)` |
| `test_execute_command_runs_driver` | method | `tests/test_dirtyinit_addon.py:124` | `def test_execute_command_runs_driver(self, addon)` |
| `test_execute_command_uses_env_prefix` | method | `tests/test_dirtyinit_addon.py:127` | `def test_execute_command_uses_env_prefix(self, addon)` |
| `test_install_command_runs_doctor` | method | `tests/test_dirtyinit_addon.py:121` | `def test_install_command_runs_doctor(self, addon)` |
| `test_install_path` | method | `tests/test_dirtyinit_addon.py:114` | `def test_install_path(self, addon)` |
| `test_install_path_no_traversal` | method | `tests/test_dirtyinit_addon.py:117` | `def test_install_path_no_traversal(self, addon)` |
| `test_name_matches_file` | method | `tests/test_dirtyinit_addon.py:69` | `def test_name_matches_file(self, addon)` |
| `test_name_pattern` | method | `tests/test_dirtyinit_addon.py:72` | `def test_name_pattern(self, addon)` |
| `test_no_double_braces` | method | `tests/test_dirtyinit_addon.py:136` | `def test_no_double_braces(self, addon)` |
| `test_no_required_params` | method | `tests/test_dirtyinit_addon.py:161` | `def test_no_required_params(self, addon)` |
| `test_no_secret_placeholders` | method | `tests/test_dirtyinit_addon.py:156` | `def test_no_secret_placeholders(self, addon)` |
| `test_os_is_known` | method | `tests/test_dirtyinit_addon.py:90` | `def test_os_is_known(self, addon)` |
| `test_param_names_are_valid` | method | `tests/test_dirtyinit_addon.py:144` | `def test_param_names_are_valid(self, addon)` |
| `test_params_are_live` | method | `tests/test_dirtyinit_addon.py:165` | `def test_params_are_live(self)` |
| `test_repo_url` | method | `tests/test_dirtyinit_addon.py:108` | `def test_repo_url(self, addon)` |
| `test_repo_url_ends_with_git` | method | `tests/test_dirtyinit_addon.py:111` | `def test_repo_url_ends_with_git(self, addon)` |
| `test_tokens_are_declared` | method | `tests/test_dirtyinit_addon.py:151` | `def test_tokens_are_declared(self, addon)` |
| `test_tool_has_key` | method | `tests/test_dirtyinit_addon.py:105` | `def test_tool_has_key(self, addon, key)` |
| `test_version_pattern` | method | `tests/test_dirtyinit_addon.py:75` | `def test_version_pattern(self, addon)` |
| `_runs_command` | function | `tests/test_docs_drift_contract.py:38` | `def _runs_command(step, command)` |
| `test_diffs_command_index` | function | `tests/test_docs_drift_contract.py:65` | `def test_diffs_command_index(workflow_steps)` |
| `test_diffs_commands_reference` | function | `tests/test_docs_drift_contract.py:71` | `def test_diffs_commands_reference(workflow_steps)` |
| `test_diffs_utils_reference` | function | `tests/test_docs_drift_contract.py:77` | `def test_diffs_utils_reference(workflow_steps)` |
| `test_regenerates_command_index` | function | `tests/test_docs_drift_contract.py:47` | `def test_regenerates_command_index(workflow_steps)` |
| `test_regenerates_commands_reference` | function | `tests/test_docs_drift_contract.py:53` | `def test_regenerates_commands_reference(workflow_steps)` |
| `test_regenerates_utils_reference` | function | `tests/test_docs_drift_contract.py:59` | `def test_regenerates_utils_reference(workflow_steps)` |
| `test_trigger_watches_generator_inputs` | function | `tests/test_docs_drift_contract.py:81` | `def test_trigger_watches_generator_inputs(workflow_text)` |
| `test_workflow_exists` | function | `tests/test_docs_drift_contract.py:43` | `def test_workflow_exists()` |
| `workflow_steps` | function | `tests/test_docs_drift_contract.py:27` | `def workflow_steps(workflow_text)` |
| `workflow_text` | function | `tests/test_docs_drift_contract.py:22` | `def workflow_text()` |
| `TestFileChecks` | class | `tests/test_doctor.py:107` | `class TestFileChecks` |
| `TestGatherAndRun` | class | `tests/test_doctor.py:184` | `class TestGatherAndRun` |
| `TestPackages` | class | `tests/test_doctor.py:72` | `class TestPackages` |
| `TestPythonVersion` | class | `tests/test_doctor.py:32` | `class TestPythonVersion` |
| `TestReportAggregation` | class | `tests/test_doctor.py:155` | `class TestReportAggregation` |
| `TestSecListsAndTools` | class | `tests/test_doctor.py:129` | `class TestSecListsAndTools` |
| `TestVirtualEnv` | class | `tests/test_doctor.py:51` | `class TestVirtualEnv` |
| `boom` | function | `tests/test_doctor.py:90` | `def boom(name)` |
| `test_active_venv_is_ok` | method | `tests/test_doctor.py:52` | `def test_active_venv_is_ok(self, tmp_path)` |
| `test_certificates_partial_warns` | method | `tests/test_doctor.py:122` | `def test_certificates_partial_warns(self, tmp_path)` |
| `test_certificates_present_is_ok` | method | `tests/test_doctor.py:117` | `def test_certificates_present_is_ok(self, tmp_path)` |
| `test_default_registry_has_core_packages` | method | `tests/test_doctor.py:97` | `def test_default_registry_has_core_packages(self)` |
| `test_exact_minimum_is_ok` | method | `tests/test_doctor.py:37` | `def test_exact_minimum_is_ok(self)` |
| `test_external_tools_present_and_missing` | method | `tests/test_doctor.py:139` | `def test_external_tools_present_and_missing(self)` |
| `test_finder_exception_treated_as_missing` | method | `tests/test_doctor.py:89` | `def test_finder_exception_treated_as_missing(self)` |
| `test_gather_report_populates_all_sections` | method | `tests/test_doctor.py:185` | `def test_gather_report_populates_all_sections(self, tmp_path)` |
| `test_import_name_differs_from_pip_name_where_expected` | method | `tests/test_doctor.py:101` | `def test_import_name_differs_from_pip_name_where_expected(self)` |
| `test_inactive_with_env_dir_warns_to_activate` | method | `tests/test_doctor.py:56` | `def test_inactive_with_env_dir_warns_to_activate(self, tmp_path)` |
| `test_missing_optional_package_warns` | method | `tests/test_doctor.py:84` | `def test_missing_optional_package_warns(self)` |
| `test_missing_required_package_fails` | method | `tests/test_doctor.py:78` | `def test_missing_required_package_fails(self)` |
| `test_no_venv_anywhere_warns_to_install` | method | `tests/test_doctor.py:62` | `def test_no_venv_anywhere_warns_to_install(self, tmp_path)` |
| `test_none_base_prefix_collapses_to_prefix` | method | `tests/test_doctor.py:67` | `def test_none_base_prefix_collapses_to_prefix(self, tmp_path)` |
| `test_old_version_fails` | method | `tests/test_doctor.py:41` | `def test_old_version_fails(self)` |
| `test_overall_status_fail_trips_healthy` | method | `tests/test_doctor.py:171` | `def test_overall_status_fail_trips_healthy(self)` |
| `test_overall_status_ok_when_all_ok` | method | `tests/test_doctor.py:156` | `def test_overall_status_ok_when_all_ok(self)` |
| `test_overall_status_warn_with_warnings_only` | method | `tests/test_doctor.py:161` | `def test_overall_status_warn_with_warnings_only(self)` |
| `test_payload_missing_fails` | method | `tests/test_doctor.py:112` | `def test_payload_missing_fails(self, tmp_path)` |
| `test_payload_present_is_ok` | method | `tests/test_doctor.py:108` | `def test_payload_present_is_ok(self, tmp_path)` |
| `test_present_required_package_is_ok` | method | `tests/test_doctor.py:73` | `def test_present_required_package_is_ok(self)` |
| `test_run_returns_report_without_raising` | method | `tests/test_doctor.py:194` | `def test_run_returns_report_without_raising(self, tmp_path)` |
| `test_seclists_found_is_ok` | method | `tests/test_doctor.py:130` | `def test_seclists_found_is_ok(self)` |
| `test_seclists_missing_warns` | method | `tests/test_doctor.py:135` | `def test_seclists_missing_warns(self)` |
| `test_supported_version_is_ok` | method | `tests/test_doctor.py:33` | `def test_supported_version_is_ok(self)` |
| `test_uses_live_interpreter_by_default` | method | `tests/test_doctor.py:46` | `def test_uses_live_interpreter_by_default(self)` |
| `Broken` | class | `tests/test_emulation_runner.py:210` | `class Broken(FakeResolver)` |
| `FakeResolver` | class | `tests/test_emulation_runner.py:30` | `class FakeResolver` |
| `FakeTest` | class | `tests/test_emulation_runner.py:19` | `class FakeTest` |
| `_Runner` | class | `tests/test_emulation_runner.py:144` | `class _Runner` |
| `__init__` | method | `tests/test_emulation_runner.py:33` | `def __init__(self, tests)` |
| `__init__` | method | `tests/test_emulation_runner.py:145` | `def __init__(self)` |
| `executor` | function | `tests/test_emulation_runner.py:45` | `def executor(command)` |
| `executor` | function | `tests/test_emulation_runner.py:128` | `def executor(command)` |
| `list_for_technique` | method | `tests/test_emulation_runner.py:36` | `def list_for_technique(self, technique, platform)` |
| `list_for_technique` | method | `tests/test_emulation_runner.py:211` | `def list_for_technique(self, technique, platform)` |
| `run` | method | `tests/test_emulation_runner.py:148` | `def run(self, target)` |
| `test_bridge_emulate_delegates_to_runner` | function | `tests/test_emulation_runner.py:138` | `def test_bridge_emulate_delegates_to_runner(monkeypatch, tmp_path)` |
| `test_engine_prefers_yaml_command_chain` | function | `tests/test_emulation_runner.py:160` | `def test_engine_prefers_yaml_command_chain(monkeypatch)` |
| `test_outcome_metadata_uses_scan_dir` | function | `tests/test_emulation_runner.py:195` | `def test_outcome_metadata_uses_scan_dir(tmp_path)` |
| `test_resolver_errors_are_reported_not_hidden` | function | `tests/test_emulation_runner.py:208` | `def test_resolver_errors_are_reported_not_hidden(tmp_path)` |
| `test_run_steps_dry_run_never_publishes` | function | `tests/test_emulation_runner.py:185` | `def test_run_steps_dry_run_never_publishes()` |
| `test_run_steps_handles_dry_run_and_failures` | function | `tests/test_emulation_runner.py:119` | `def test_run_steps_handles_dry_run_and_failures()` |
| `test_runner_dry_run_never_calls_executor` | function | `tests/test_emulation_runner.py:64` | `def test_runner_dry_run_never_calls_executor(tmp_path)` |
| `test_runner_executes_normalizes_and_publishes` | function | `tests/test_emulation_runner.py:40` | `def test_runner_executes_normalizes_and_publishes(tmp_path)` |
| `test_runner_requires_techniques` | function | `tests/test_emulation_runner.py:112` | `def test_runner_requires_techniques(tmp_path)` |
| `test_runner_resolves_playbook_techniques` | function | `tests/test_emulation_runner.py:94` | `def test_runner_resolves_playbook_techniques(tmp_path)` |
| `test_runner_skips_manual_tests_by_default` | function | `tests/test_emulation_runner.py:79` | `def test_runner_skips_manual_tests_by_default(tmp_path)` |
| `EncodingSuiteConfig` | class | `tests/test_encoding_command_set.py:34` | `class EncodingSuiteConfig` |
| `_add_repo_root_to_syspath` | function | `tests/test_encoding_command_set.py:28` | `def _add_repo_root_to_syspath()` |
| `_methods_of` | function | `tests/test_encoding_command_set.py:59` | `def _methods_of(path, class_name)` |
| `test_no_command_collisions_with_source` | function | `tests/test_encoding_command_set.py:106` | `def test_no_command_collisions_with_source()` |
| `test_registry_registers_target` | function | `tests/test_encoding_command_set.py:99` | `def test_registry_registers_target()` |
| `test_source_no_longer_defines_cluster` | function | `tests/test_encoding_command_set.py:93` | `def test_source_no_longer_defines_cluster()` |
| `test_target_exposes_full_encoding_cluster` | function | `tests/test_encoding_command_set.py:80` | `def test_target_exposes_full_encoding_cluster()` |
| `test_target_is_active_command_set` | function | `tests/test_encoding_command_set.py:71` | `def test_target_is_active_command_set()` |
| `test_target_phase_metadata` | function | `tests/test_encoding_command_set.py:87` | `def test_target_phase_metadata()` |
| `_Dispatcher` | class | `tests/test_engage_gates.py:182` | `class _Dispatcher` |
| `_Dispatcher` | class | `tests/test_engage_gates.py:209` | `class _Dispatcher` |
| `_EmptyPlanner` | class | `tests/test_engage_gates.py:203` | `class _EmptyPlanner` |
| `_Narrator` | class | `tests/test_engage_gates.py:248` | `class _Narrator(_RecorderNarrator)` |
| `_RecorderNarrator` | class | `tests/test_engage_gates.py:44` | `class _RecorderNarrator` |
| `_ScriptedRunner` | class | `tests/test_engage_gates.py:23` | `class _ScriptedRunner` |
| `__init__` | method | `tests/test_engage_gates.py:26` | `def __init__(self, scripted)` |
| `__init__` | method | `tests/test_engage_gates.py:47` | `def __init__(self)` |
| `_approved_gate` | function | `tests/test_engage_gates.py:56` | `def _approved_gate()` |
| `_orch` | function | `tests/test_engage_gates.py:74` | `def _orch(target, scripted, plan, guard)` |
| `name` | method | `tests/test_engage_gates.py:39` | `def name(self)` |
| `narrate` | method | `tests/test_engage_gates.py:51` | `def narrate(self, kind)` |
| `narrate` | method | `tests/test_engage_gates.py:249` | `def narrate(self, kind, message)` |
| `plan` | method | `tests/test_engage_gates.py:204` | `def plan(self, target, max_candidates)` |
| `run` | method | `tests/test_engage_gates.py:31` | `def run(self, command, timeout)` |
| `suggest` | method | `tests/test_engage_gates.py:183` | `def suggest(self)` |
| `suggest` | method | `tests/test_engage_gates.py:210` | `def suggest(self)` |
| `temp_sessions` | function | `tests/test_engage_gates.py:63` | `def temp_sessions(tmp_path, monkeypatch)` |
| `test_denied_command_never_executes` | function | `tests/test_engage_gates.py:89` | `def test_denied_command_never_executes(temp_sessions)` |
| `test_duplicate_success_is_skipped` | function | `tests/test_engage_gates.py:109` | `def test_duplicate_success_is_skipped(temp_sessions)` |
| `test_engage_summary_counts_ran_and_skipped` | function | `tests/test_engage_gates.py:241` | `def test_engage_summary_counts_ran_and_skipped(temp_sessions, monkeypatch)` |
| `test_executed_steps_leave_transcript_and_evidence` | function | `tests/test_engage_gates.py:138` | `def test_executed_steps_leave_transcript_and_evidence(temp_sessions)` |
| `test_latest_hint_renders_newest_event` | function | `tests/test_engage_gates.py:225` | `def test_latest_hint_renders_newest_event(tmp_path)` |
| `test_no_new_direction_when_world_unchanged` | function | `tests/test_engage_gates.py:164` | `def test_no_new_direction_when_world_unchanged(temp_sessions, monkeypatch)` |
| `test_notify_journal_written_for_findings` | function | `tests/test_engage_gates.py:153` | `def test_notify_journal_written_for_findings(temp_sessions)` |
| `test_planner_fallback_pushes_forward` | function | `tests/test_engage_gates.py:196` | `def test_planner_fallback_pushes_forward(temp_sessions, monkeypatch)` |
| `test_planner_intent_executes_mapped_verb` | function | `tests/test_engage_gates.py:175` | `def test_planner_intent_executes_mapped_verb(temp_sessions, monkeypatch)` |
| `test_scan_step_skipped_when_scan_held` | function | `tests/test_engage_gates.py:123` | `def test_scan_step_skipped_when_scan_held(temp_sessions)` |
| `TestApprovalGate` | class | `tests/test_engage_orchestrator.py:294` | `class TestApprovalGate` |
| `TestEngageOrchestrator` | class | `tests/test_engage_orchestrator.py:528` | `class TestEngageOrchestrator` |
| `TestEngagementNarrator` | class | `tests/test_engage_orchestrator.py:86` | `class TestEngagementNarrator` |
| `TestFileApprovalSink` | class | `tests/test_engage_orchestrator.py:385` | `class TestFileApprovalSink` |
| `TestIsValidTarget` | class | `tests/test_engage_orchestrator.py:241` | `class TestIsValidTarget` |
| `TestMcpEntryPoints` | class | `tests/test_engage_orchestrator.py:632` | `class TestMcpEntryPoints` |
| `TestNotificationBroadcaster` | class | `tests/test_engage_orchestrator.py:139` | `class TestNotificationBroadcaster` |
| `TestShellObtainedPublisher` | class | `tests/test_engage_orchestrator.py:191` | `class TestShellObtainedPublisher` |
| `TestStaticFallbackResolver` | class | `tests/test_engage_orchestrator.py:451` | `class TestStaticFallbackResolver` |
| `TestStdinApprovalSink` | class | `tests/test_engage_orchestrator.py:431` | `class TestStdinApprovalSink` |
| `TestWiring` | class | `tests/test_engage_orchestrator.py:676` | `class TestWiring` |
| `_BoomSink` | class | `tests/test_engage_orchestrator.py:165` | `class _BoomSink(INotificationSink)` |
| `_CountingSink` | class | `tests/test_engage_orchestrator.py:145` | `class _CountingSink(INotificationSink)` |
| `_GoodSink` | class | `tests/test_engage_orchestrator.py:173` | `class _GoodSink(INotificationSink)` |
| `_NoOpGate` | class | `tests/test_engage_orchestrator.py:497` | `class _NoOpGate` |
| `_RecordingSink` | class | `tests/test_engage_orchestrator.py:280` | `class _RecordingSink` |
| `_RejectingGate` | class | `tests/test_engage_orchestrator.py:508` | `class _RejectingGate` |
| `_ScriptedRunner` | class | `tests/test_engage_orchestrator.py:473` | `class _ScriptedRunner` |
| `__init__` | method | `tests/test_engage_orchestrator.py:146` | `def __init__(self, name)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:283` | `def __init__(self)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:481` | `def __init__(self, scripted)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:509` | `def __init__(self, rejected_phase)` |
| `_injected_sleep` | function | `tests/test_engage_orchestrator.py:330` | `def _injected_sleep(_seconds)` |
| `announce` | method | `tests/test_engage_orchestrator.py:287` | `def announce(self, request)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:153` | `def deliver(self, event)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:170` | `def deliver(self, event)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:178` | `def deliver(self, event)` |
| `name` | method | `tests/test_engage_orchestrator.py:150` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:167` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:175` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:493` | `def name(self)` |
| `policy_module` | function | `tests/test_engage_orchestrator.py:270` | `def policy_module(temp_sessions, monkeypatch)` |
| `request` | method | `tests/test_engage_orchestrator.py:498` | `def request(self, target, phase, command, reason)` |
| `request` | method | `tests/test_engage_orchestrator.py:512` | `def request(self, target, phase, command, reason)` |
| `resolution_for` | method | `tests/test_engage_orchestrator.py:290` | `def resolution_for(self, approval_id)` |
| `run` | method | `tests/test_engage_orchestrator.py:485` | `def run(self, command, timeout)` |
| `temp_sessions` | function | `tests/test_engage_orchestrator.py:47` | `def temp_sessions(tmp_path, monkeypatch)` |
| `test_accepts_hostname` | method | `tests/test_engage_orchestrator.py:248` | `def test_accepts_hostname(self)` |
| `test_accepts_ipv4` | method | `tests/test_engage_orchestrator.py:242` | `def test_accepts_ipv4(self)` |
| `test_announce_writes_pending_record` | method | `tests/test_engage_orchestrator.py:386` | `def test_announce_writes_pending_record(self, policy_module, temp_sessions)` |
| `test_approval_gate_defaults_to_true_when_key_missing` | method | `tests/test_engage_orchestrator.py:708` | `def test_approval_gate_defaults_to_true_when_key_missing(self, tmp_path)` |
| `test_auto_approve_true_returns_approved_for_gated_phase` | method | `tests/test_engage_orchestrator.py:295` | `def test_auto_approve_true_returns_approved_for_gated_phase(self, policy_module, temp_sessions)` |
| `test_client_id_is_sanitised` | method | `tests/test_engage_orchestrator.py:223` | `def test_client_id_is_sanitised(self, temp_sessions)` |
| `test_daemon_has_engage_subcommand` | method | `tests/test_engage_orchestrator.py:698` | `def test_daemon_has_engage_subcommand(self)` |
| `test_denied_step_is_skipped` | method | `tests/test_engage_orchestrator.py:585` | `def test_denied_step_is_skipped(self, temp_sessions, policy_module)` |
| `test_do_engage_method_exists_in_lazyown` | method | `tests/test_engage_orchestrator.py:677` | `def test_do_engage_method_exists_in_lazyown(self)` |
| `test_engage_approve_accepts_valid_decision` | method | `tests/test_engage_orchestrator.py:662` | `def test_engage_approve_accepts_valid_decision(self, temp_sessions, policy_module)` |
| `test_engage_approve_rejects_bad_decision` | method | `tests/test_engage_orchestrator.py:656` | `def test_engage_approve_rejects_bad_decision(self, temp_sessions, policy_module)` |
| `test_engage_status_returns_pending_approvals_structure` | method | `tests/test_engage_orchestrator.py:648` | `def test_engage_status_returns_pending_approvals_structure(self, temp_sessions, policy_module)` |
| `test_engage_target_rejects_invalid` | method | `tests/test_engage_orchestrator.py:633` | `def test_engage_target_rejects_invalid(self, temp_sessions, policy_module)` |
| `test_engage_target_returns_engagement_id` | method | `tests/test_engage_orchestrator.py:639` | `def test_engage_target_returns_engagement_id(self, temp_sessions, policy_module)` |
| `test_engagement_hooks_module_exposes_public_surface` | method | `tests/test_engage_orchestrator.py:726` | `def test_engagement_hooks_module_exposes_public_surface(self)` |
| `test_failing_sink_does_not_break_broadcaster` | method | `tests/test_engage_orchestrator.py:162` | `def test_failing_sink_does_not_break_broadcaster(self, temp_sessions)` |
| `test_fans_out_to_every_sink` | method | `tests/test_engage_orchestrator.py:140` | `def test_fans_out_to_every_sink(self, temp_sessions)` |
| `test_first_call_emits_event` | method | `tests/test_engage_orchestrator.py:192` | `def test_first_call_emits_event(self, temp_sessions)` |
| `test_gated_phase_times_out_to_denied` | method | `tests/test_engage_orchestrator.py:356` | `def test_gated_phase_times_out_to_denied(self, policy_module, temp_sessions)` |
| `test_gated_phase_with_auto_approve_false_polls_sink` | method | `tests/test_engage_orchestrator.py:326` | `def test_gated_phase_with_auto_approve_false_polls_sink(self, policy_module, temp_sessions)` |
| `test_invalid_client_id_returns_none` | method | `tests/test_engage_orchestrator.py:217` | `def test_invalid_client_id_returns_none(self, temp_sessions)` |
| `test_invalid_payload_defaults_to_auto_approve_true` | method | `tests/test_engage_orchestrator.py:375` | `def test_invalid_payload_defaults_to_auto_approve_true(self, policy_module, temp_sessions)` |
| `test_lazyc2_has_engagement_hook_call` | method | `tests/test_engage_orchestrator.py:684` | `def test_lazyc2_has_engagement_hook_call(self)` |
| `test_mcp_exposes_four_engage_tools` | method | `tests/test_engage_orchestrator.py:688` | `def test_mcp_exposes_four_engage_tools(self)` |
| `test_narrate_writes_log_and_audit` | method | `tests/test_engage_orchestrator.py:87` | `def test_narrate_writes_log_and_audit(self, temp_sessions)` |
| `test_no_tty_returns_none` | method | `tests/test_engage_orchestrator.py:432` | `def test_no_tty_returns_none(self, policy_module)` |
| `test_non_gated_phase_bypasses_sink` | method | `tests/test_engage_orchestrator.py:310` | `def test_non_gated_phase_bypasses_sink(self, policy_module, temp_sessions)` |
| `test_payload_json_auto_approve_key_is_bool_when_present` | method | `tests/test_engage_orchestrator.py:703` | `def test_payload_json_auto_approve_key_is_bool_when_present(self)` |
| `test_policy_module_exposes_approval_surface` | method | `tests/test_engage_orchestrator.py:740` | `def test_policy_module_exposes_approval_surface(self)` |
| `test_rejects_garbage` | method | `tests/test_engage_orchestrator.py:254` | `def test_rejects_garbage(self)` |
| `test_rejects_invalid_target` | method | `tests/test_engage_orchestrator.py:529` | `def test_rejects_invalid_target(self, temp_sessions, policy_module)` |
| `test_render_line_format_is_stable` | method | `tests/test_engage_orchestrator.py:123` | `def test_render_line_format_is_stable(self)` |
| `test_repeat_call_is_idempotent` | method | `tests/test_engage_orchestrator.py:209` | `def test_repeat_call_is_idempotent(self, temp_sessions)` |
| `test_resolution_returns_latest_non_pending` | method | `tests/test_engage_orchestrator.py:402` | `def test_resolution_returns_latest_non_pending(self, policy_module, temp_sessions)` |
| `test_returns_alternatives_in_order` | method | `tests/test_engage_orchestrator.py:452` | `def test_returns_alternatives_in_order(self)` |
| `test_runs_full_plan_on_success` | method | `tests/test_engage_orchestrator.py:535` | `def test_runs_full_plan_on_success(self, temp_sessions, policy_module)` |
| `test_shell_indicator_stops_loop` | method | `tests/test_engage_orchestrator.py:609` | `def test_shell_indicator_stops_loop(self, temp_sessions, policy_module)` |
| `test_stream_sink_appends_to_autonomous_events` | method | `tests/test_engage_orchestrator.py:112` | `def test_stream_sink_appends_to_autonomous_events(self, temp_sessions)` |
| `test_switches_tool_on_failure` | method | `tests/test_engage_orchestrator.py:559` | `def test_switches_tool_on_failure(self, temp_sessions, policy_module)` |
| `test_unknown_primary_returns_none` | method | `tests/test_engage_orchestrator.py:462` | `def test_unknown_primary_returns_none(self)` |
| `_step` | function | `tests/test_engage_summary.py:45` | `def _step(command)` |
| `test_detail_for_empty_search_is_honest` | function | `tests/test_engage_summary.py:76` | `def test_detail_for_empty_search_is_honest()` |
| `test_detail_for_ping_extracts_os` | function | `tests/test_engage_summary.py:62` | `def test_detail_for_ping_extracts_os()` |
| `test_detail_for_populate_extracts_services` | function | `tests/test_engage_summary.py:69` | `def test_detail_for_populate_extracts_services()` |
| `test_full_output_prefers_evidence` | function | `tests/test_engage_summary.py:104` | `def test_full_output_prefers_evidence(tmp_path)` |
| `test_held_scan_ports_reads_xml` | function | `tests/test_engage_summary.py:82` | `def test_held_scan_ports_reads_xml(tmp_path)` |
| `test_marker_lines_drop_panels_and_bars` | function | `tests/test_engage_summary.py:54` | `def test_marker_lines_drop_panels_and_bars()` |
| `test_render_markdown_lists_evidence_and_next` | function | `tests/test_engage_summary.py:125` | `def test_render_markdown_lists_evidence_and_next()` |
| `test_render_text_shows_skip_with_held_ports` | function | `tests/test_engage_summary.py:91` | `def test_render_text_shows_skip_with_held_ports(tmp_path)` |
| `test_write_report_persists_markdown` | function | `tests/test_engage_summary.py:114` | `def test_write_report_persists_markdown(tmp_path)` |
| `TestCuriosityEngine` | class | `tests/test_engagement_and_ping.py:177` | `class TestCuriosityEngine` |
| `TestEngagementState` | class | `tests/test_engagement_and_ping.py:58` | `class TestEngagementState` |
| `TestPingOsId` | class | `tests/test_engagement_and_ping.py:283` | `class TestPingOsId` |
| `TestRecommendNextCommandIndex` | class | `tests/test_engagement_and_ping.py:351` | `class TestRecommendNextCommandIndex` |
| `TestVRIScheduler` | class | `tests/test_engagement_and_ping.py:105` | `class TestVRIScheduler` |
| `_build_csv` | method | `tests/test_engagement_and_ping.py:366` | `def _build_csv(self, tmp_path, run_cmds)` |
| `_build_index` | method | `tests/test_engagement_and_ping.py:354` | `def _build_index(self, tmp_path, phase, n_cmds)` |
| `_command_location` | function | `tests/test_engagement_and_ping.py:30` | `def _command_location(name)` |
| `_extract_os_id_from_json` | method | `tests/test_engagement_and_ping.py:292` | `def _extract_os_id_from_json(self, data)` |
| `_make_params` | method | `tests/test_engagement_and_ping.py:289` | `def _make_params(self)` |
| `_make_state` | method | `tests/test_engagement_and_ping.py:178` | `def _make_state(self, seen)` |
| `_minimal_index` | method | `tests/test_engagement_and_ping.py:186` | `def _minimal_index(self, phase_cmds)` |
| `_ping_stdout` | method | `tests/test_engagement_and_ping.py:286` | `def _ping_stdout(self, ttl)` |
| `test_atomic_write_leaves_no_tmp_file` | method | `tests/test_engagement_and_ping.py:90` | `def test_atomic_write_leaves_no_tmp_file(self, tmp_path)` |
| `test_commands_seen_accumulates_across_calls` | method | `tests/test_engagement_and_ping.py:254` | `def test_commands_seen_accumulates_across_calls(self, tmp_path)` |
| `test_curiosity_does_not_repeat_in_session` | method | `tests/test_engagement_and_ping.py:202` | `def test_curiosity_does_not_repeat_in_session(self, capsys)` |
| `test_curiosity_shows_undiscovered_command` | method | `tests/test_engagement_and_ping.py:192` | `def test_curiosity_shows_undiscovered_command(self, capsys)` |
| `test_curiosity_silent_for_unknown_phase` | method | `tests/test_engagement_and_ping.py:245` | `def test_curiosity_silent_for_unknown_phase(self, capsys)` |
| `test_curiosity_silent_when_all_discovered` | method | `tests/test_engagement_and_ping.py:219` | `def test_curiosity_silent_when_all_discovered(self, capsys)` |
| `test_curiosity_silent_when_disabled` | method | `tests/test_engagement_and_ping.py:229` | `def test_curiosity_silent_when_disabled(self, capsys)` |
| `test_fallback_message_present` | method | `tests/test_engagement_and_ping.py:517` | `def test_fallback_message_present(self)` |
| `test_load_fresh_state_has_zero_commands` | method | `tests/test_engagement_and_ping.py:59` | `def test_load_fresh_state_has_zero_commands(self, tmp_path)` |
| `test_next_threshold_always_positive` | method | `tests/test_engagement_and_ping.py:106` | `def test_next_threshold_always_positive(self)` |
| `test_next_threshold_mean_near_target` | method | `tests/test_engagement_and_ping.py:113` | `def test_next_threshold_mean_near_target(self)` |
| `test_no_advisor_reference_before_definition` | method | `tests/test_engagement_and_ping.py:470` | `def test_no_advisor_reference_before_definition(self)` |
| `test_no_graph_nodes_in_output` | method | `tests/test_engagement_and_ping.py:456` | `def test_no_graph_nodes_in_output(self, tmp_path, capsys)` |
| `test_ping_os_json_contract` | method | `tests/test_engagement_and_ping.py:330` | `def test_ping_os_json_contract(self)` |
| `test_ping_persists_via_apply_assign` | method | `tests/test_engagement_and_ping.py:338` | `def test_ping_persists_via_apply_assign(self)` |
| `test_rule_not_used_without_import` | method | `tests/test_engagement_and_ping.py:509` | `def test_rule_not_used_without_import(self)` |
| `test_save_and_reload_state` | method | `tests/test_engagement_and_ping.py:74` | `def test_save_and_reload_state(self, tmp_path)` |
| `test_shows_nothing_when_all_run` | method | `tests/test_engagement_and_ping.py:436` | `def test_shows_nothing_when_all_run(self, tmp_path)` |
| `test_shows_unrun_commands` | method | `tests/test_engagement_and_ping.py:411` | `def test_shows_unrun_commands(self, tmp_path, capsys)` |
| `test_threshold_is_variable_not_constant` | method | `tests/test_engagement_and_ping.py:120` | `def test_threshold_is_variable_not_constant(self)` |
| `test_ttl_127_maps_to_os_id_2_windows` | method | `tests/test_engagement_and_ping.py:309` | `def test_ttl_127_maps_to_os_id_2_windows(self)` |
| `test_ttl_128_maps_to_os_id_2_windows` | method | `tests/test_engagement_and_ping.py:302` | `def test_ttl_128_maps_to_os_id_2_windows(self)` |
| `test_ttl_255_maps_to_unknown` | method | `tests/test_engagement_and_ping.py:323` | `def test_ttl_255_maps_to_unknown(self)` |
| `test_ttl_63_maps_to_os_id_1_linux` | method | `tests/test_engagement_and_ping.py:316` | `def test_ttl_63_maps_to_os_id_1_linux(self)` |
| `test_ttl_64_maps_to_os_id_1_linux` | method | `tests/test_engagement_and_ping.py:295` | `def test_ttl_64_maps_to_os_id_1_linux(self)` |
| `test_vri_does_not_fire_before_threshold` | method | `tests/test_engagement_and_ping.py:152` | `def test_vri_does_not_fire_before_threshold(self, tmp_path, capsys)` |
| `test_vri_fires_when_threshold_reached` | method | `tests/test_engagement_and_ping.py:126` | `def test_vri_fires_when_threshold_reached(self, tmp_path, capsys)` |
| `TestHealCommandsSeen` | class | `tests/test_engagement_command_gate.py:187` | `class TestHealCommandsSeen` |
| `TestHookRejectsNoise` | class | `tests/test_engagement_command_gate.py:106` | `class TestHookRejectsNoise` |
| `TestIsRecordableCommand` | class | `tests/test_engagement_command_gate.py:68` | `class TestIsRecordableCommand` |
| `TestSanitizeSeen` | class | `tests/test_engagement_command_gate.py:141` | `class TestSanitizeSeen` |
| `_redirect_paths` | function | `tests/test_engagement_command_gate.py:34` | `def _redirect_paths(tmp_path)` |
| `_restore_paths` | function | `tests/test_engagement_command_gate.py:56` | `def _restore_paths(saved)` |
| `test_accepts_command_shaped_tokens` | method | `tests/test_engagement_command_gate.py:72` | `def test_accepts_command_shaped_tokens(self, cmd)` |
| `test_do_prefixed_input_is_accepted` | method | `tests/test_engagement_command_gate.py:91` | `def test_do_prefixed_input_is_accepted(self)` |
| `test_garbage_does_not_enter_commands_seen` | method | `tests/test_engagement_command_gate.py:109` | `def test_garbage_does_not_enter_commands_seen(self, tmp_path)` |
| `test_idempotent_on_clean_state` | method | `tests/test_engagement_command_gate.py:207` | `def test_idempotent_on_clean_state(self, tmp_path)` |
| `test_load_state_heals_polluted_file` | method | `tests/test_engagement_command_gate.py:165` | `def test_load_state_heals_polluted_file(self, tmp_path)` |
| `test_normalize_is_idempotent` | method | `tests/test_engagement_command_gate.py:96` | `def test_normalize_is_idempotent(self)` |
| `test_purges_and_persists` | method | `tests/test_engagement_command_gate.py:190` | `def test_purges_and_persists(self, tmp_path)` |
| `test_quoted_path_rejected` | method | `tests/test_engagement_command_gate.py:86` | `def test_quoted_path_rejected(self)` |
| `test_real_command_recorded_between_garbage` | method | `tests/test_engagement_command_gate.py:123` | `def test_real_command_recorded_between_garbage(self, tmp_path)` |
| `test_rejects_syntactic_garbage` | method | `tests/test_engagement_command_gate.py:81` | `def test_rejects_syntactic_garbage(self, cmd)` |
| `test_roster_drops_valid_but_unknown_tokens` | method | `tests/test_engagement_command_gate.py:158` | `def test_roster_drops_valid_but_unknown_tokens(self)` |
| `test_syntactic_only_drops_ugly_garbage` | method | `tests/test_engagement_command_gate.py:144` | `def test_syntactic_only_drops_ugly_garbage(self)` |
| `TestAwardElo` | class | `tests/test_engagement_elo_and_methodology.py:119` | `class TestAwardElo` |
| `TestGetKarmaName` | class | `tests/test_engagement_elo_and_methodology.py:88` | `class TestGetKarmaName` |
| `TestKarmaUp` | class | `tests/test_engagement_elo_and_methodology.py:425` | `class TestKarmaUp` |
| `TestMethodologyRewards` | class | `tests/test_engagement_elo_and_methodology.py:313` | `class TestMethodologyRewards` |
| `TestPersistNotification` | class | `tests/test_engagement_elo_and_methodology.py:252` | `class TestPersistNotification` |
| `TestRenderEngagementHookIntegration` | class | `tests/test_engagement_elo_and_methodology.py:463` | `class TestRenderEngagementHookIntegration` |
| `TestStateSnapshot` | class | `tests/test_engagement_elo_and_methodology.py:524` | `class TestStateSnapshot` |
| `TestSyncUserElo` | class | `tests/test_engagement_elo_and_methodology.py:179` | `class TestSyncUserElo` |
| `_no_cli_operator` | function | `tests/test_engagement_elo_and_methodology.py:31` | `def _no_cli_operator(monkeypatch)` |
| `_redirect_paths` | function | `tests/test_engagement_elo_and_methodology.py:48` | `def _redirect_paths(tmp_path)` |
| `_restore_paths` | function | `tests/test_engagement_elo_and_methodology.py:76` | `def _restore_paths(saved)` |
| `test_all_bonuses_stack` | method | `tests/test_engagement_elo_and_methodology.py:149` | `def test_all_bonuses_stack(self)` |
| `test_appends_to_existing_file` | method | `tests/test_engagement_elo_and_methodology.py:264` | `def test_appends_to_existing_file(self, tmp_path)` |
| `test_atomic_rename_leaves_no_tmp` | method | `tests/test_engagement_elo_and_methodology.py:234` | `def test_atomic_rename_leaves_no_tmp(self, tmp_path)` |
| `test_base_only_for_unknown_command_and_phase` | method | `tests/test_engagement_elo_and_methodology.py:120` | `def test_base_only_for_unknown_command_and_phase(self)` |
| `test_creates_file_on_first_call` | method | `tests/test_engagement_elo_and_methodology.py:253` | `def test_creates_file_on_first_call(self, tmp_path)` |
| `test_disabled_flag_is_noop` | method | `tests/test_engagement_elo_and_methodology.py:508` | `def test_disabled_flag_is_noop(self, tmp_path, capsys)` |
| `test_do_prefix_is_stripped` | method | `tests/test_engagement_elo_and_methodology.py:169` | `def test_do_prefix_is_stripped(self)` |
| `test_elo_accumulates_across_commands` | method | `tests/test_engagement_elo_and_methodology.py:464` | `def test_elo_accumulates_across_commands(self, tmp_path)` |
| `test_fires_on_threshold_crossing` | method | `tests/test_engagement_elo_and_methodology.py:426` | `def test_fires_on_threshold_crossing(self, tmp_path, capsys)` |
| `test_first_time_bonus` | method | `tests/test_engagement_elo_and_methodology.py:137` | `def test_first_time_bonus(self)` |
| `test_first_time_bonus_only_once_per_command` | method | `tests/test_engagement_elo_and_methodology.py:479` | `def test_first_time_bonus_only_once_per_command(self, tmp_path)` |
| `test_high_value_bonus_applied` | method | `tests/test_engagement_elo_and_methodology.py:125` | `def test_high_value_bonus_applied(self)` |
| `test_idempotent_when_no_threshold_cross` | method | `tests/test_engagement_elo_and_methodology.py:440` | `def test_idempotent_when_no_threshold_cross(self, capsys)` |
| `test_ignores_non_positive_delta` | method | `tests/test_engagement_elo_and_methodology.py:224` | `def test_ignores_non_positive_delta(self, tmp_path)` |
| `test_new_phase_bonus` | method | `tests/test_engagement_elo_and_methodology.py:143` | `def test_new_phase_bonus(self)` |
| `test_note_reward_renders_latest` | method | `tests/test_engagement_elo_and_methodology.py:391` | `def test_note_reward_renders_latest(self, tmp_path, capsys)` |
| `test_note_reward_silent_when_empty` | method | `tests/test_engagement_elo_and_methodology.py:412` | `def test_note_reward_silent_when_empty(self, tmp_path, capsys)` |
| `test_objective_reward_silent_when_no_pending` | method | `tests/test_engagement_elo_and_methodology.py:379` | `def test_objective_reward_silent_when_no_pending(self, tmp_path, capsys)` |
| `test_objective_reward_uses_phase_to_next_cmd` | method | `tests/test_engagement_elo_and_methodology.py:361` | `def test_objective_reward_uses_phase_to_next_cmd(self, tmp_path, capsys)` |
| `test_patches_matching_username` | method | `tests/test_engagement_elo_and_methodology.py:180` | `def test_patches_matching_username(self, tmp_path)` |
| `test_persists_notification` | method | `tests/test_engagement_elo_and_methodology.py:447` | `def test_persists_notification(self, tmp_path)` |
| `test_phase_bonus_applied` | method | `tests/test_engagement_elo_and_methodology.py:131` | `def test_phase_bonus_applied(self)` |
| `test_recovers_from_corrupt_file` | method | `tests/test_engagement_elo_and_methodology.py:297` | `def test_recovers_from_corrupt_file(self, tmp_path)` |
| `test_returns_required_keys` | method | `tests/test_engagement_elo_and_methodology.py:525` | `def test_returns_required_keys(self, tmp_path)` |
| `test_ring_cap_drops_oldest` | method | `tests/test_engagement_elo_and_methodology.py:277` | `def test_ring_cap_drops_oldest(self, tmp_path)` |
| `test_silent_when_payload_missing` | method | `tests/test_engagement_elo_and_methodology.py:199` | `def test_silent_when_payload_missing(self, tmp_path)` |
| `test_silent_when_username_not_found` | method | `tests/test_engagement_elo_and_methodology.py:211` | `def test_silent_when_username_not_found(self, tmp_path)` |
| `test_task_reward_renders_pending_match` | method | `tests/test_engagement_elo_and_methodology.py:324` | `def test_task_reward_renders_pending_match(self, tmp_path, capsys)` |
| `test_task_reward_silent_when_all_done` | method | `tests/test_engagement_elo_and_methodology.py:344` | `def test_task_reward_silent_when_all_done(self, tmp_path, capsys)` |
| `test_task_reward_silent_when_no_file` | method | `tests/test_engagement_elo_and_methodology.py:314` | `def test_task_reward_silent_when_no_file(self, tmp_path, capsys)` |
| `test_thresholds` | method | `tests/test_engagement_elo_and_methodology.py:110` | `def test_thresholds(self, elo, expected)` |
| `test_users_json_syncd_when_payload_present` | method | `tests/test_engagement_elo_and_methodology.py:493` | `def test_users_json_syncd_when_payload_present(self, tmp_path)` |
| `_base_nodes` | function | `tests/test_estorides_fusion.py:36` | `def _base_nodes()` |
| `_load_surface_graph` | function | `tests/test_estorides_fusion.py:27` | `def _load_surface_graph()` |
| `test_discovery_targets_reads_all_files` | function | `tests/test_estorides_fusion.py:194` | `def test_discovery_targets_reads_all_files(tmp_path)` |
| `test_find_export_prefers_lazyown` | function | `tests/test_estorides_fusion.py:182` | `def test_find_export_prefers_lazyown(tmp_path)` |

Next: [SYMBOLS_p38.md](SYMBOLS_p38.md)
