# Symbols (page 29 of 35)
Previous: [SYMBOLS_p28.md](SYMBOLS_p28.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_wildcard_in_csv_is_dropped` | method | `tests/test_cors_policy.py:31` | `def test_wildcard_in_csv_is_dropped(self)` |
| `test_wildcard_is_rejected` | method | `tests/test_cors_policy.py:27` | `def test_wildcard_is_rejected(self)` |
| `TestOriginsForSocketIO` | class | `tests/test_cors_socketio_regression.py:20` | `class TestOriginsForSocketIO` |
| `test_dev_empty_includes_http_and_https` | method | `tests/test_cors_socketio_regression.py:29` | `def test_dev_empty_includes_http_and_https(self)` |
| `test_dev_empty_includes_lhost_with_common_ports` | method | `tests/test_cors_socketio_regression.py:23` | `def test_dev_empty_includes_lhost_with_common_ports(self)` |
| `test_dev_empty_includes_localhost_alias` | method | `tests/test_cors_socketio_regression.py:35` | `def test_dev_empty_includes_localhost_alias(self)` |
| `test_explicit_origins_deduped` | method | `tests/test_cors_socketio_regression.py:51` | `def test_explicit_origins_deduped(self)` |
| `test_explicit_origins_kept_with_port_appended` | method | `tests/test_cors_socketio_regression.py:40` | `def test_explicit_origins_kept_with_port_appended(self)` |
| `test_prod_raises_when_empty` | method | `tests/test_cors_socketio_regression.py:61` | `def test_prod_raises_when_empty(self)` |
| `test_wildcard_rejected` | method | `tests/test_cors_socketio_regression.py:65` | `def test_wildcard_rejected(self)` |
| `TestCheckDefaults` | class | `tests/test_credential_vault.py:18` | `class TestCheckDefaults` |
| `TestSealUnseal` | class | `tests/test_credential_vault.py:56` | `class TestSealUnseal` |
| `TestSecureDefaults` | class | `tests/test_credential_vault.py:116` | `class TestSecureDefaults` |
| `test_api_key_is_longer` | method | `tests/test_credential_vault.py:124` | `def test_api_key_is_longer(self)` |
| `test_changeme_variants` | method | `tests/test_credential_vault.py:44` | `def test_changeme_variants(self)` |
| `test_clean_payload_no_warnings` | method | `tests/test_credential_vault.py:24` | `def test_clean_payload_no_warnings(self)` |
| `test_default_values_detected` | method | `tests/test_credential_vault.py:19` | `def test_default_values_detected(self)` |
| `test_different_key_fails` | method | `tests/test_credential_vault.py:72` | `def test_different_key_fails(self)` |
| `test_empty_keys_flagged` | method | `tests/test_credential_vault.py:39` | `def test_empty_keys_flagged(self)` |
| `test_empty_string_passthrough` | method | `tests/test_credential_vault.py:64` | `def test_empty_string_passthrough(self)` |
| `test_generates_random_values` | method | `tests/test_credential_vault.py:117` | `def test_generates_random_values(self)` |
| `test_non_sensitive_keys_untouched` | method | `tests/test_credential_vault.py:107` | `def test_non_sensitive_keys_untouched(self)` |
| `test_payload_roundtrip` | method | `tests/test_credential_vault.py:80` | `def test_payload_roundtrip(self)` |
| `test_plaintext_passthrough` | method | `tests/test_credential_vault.py:68` | `def test_plaintext_passthrough(self)` |
| `test_roundtrip` | method | `tests/test_credential_vault.py:57` | `def test_roundtrip(self)` |
| `test_sensitive_keys_encrypted` | method | `tests/test_credential_vault.py:98` | `def test_sensitive_keys_encrypted(self)` |
| `_boom` | function | `tests/test_credentials_rotation.py:69` | `def _boom()` |
| `_boom` | function | `tests/test_credentials_rotation.py:80` | `def _boom()` |
| `in_tmp_sessions` | function | `tests/test_credentials_rotation.py:32` | `def in_tmp_sessions(tmp_path, monkeypatch)` |
| `test_empty_file_uses_fallback_username` | function | `tests/test_credentials_rotation.py:51` | `def test_empty_file_uses_fallback_username(in_tmp_sessions)` |
| `test_existing_file_is_backed_up_by_username` | function | `tests/test_credentials_rotation.py:42` | `def test_existing_file_is_backed_up_by_username(in_tmp_sessions)` |
| `test_line_without_colon_uses_whole_token` | function | `tests/test_credentials_rotation.py:58` | `def test_line_without_colon_uses_whole_token(in_tmp_sessions)` |
| `test_missing_file_returns_none` | function | `tests/test_credentials_rotation.py:38` | `def test_missing_file_returns_none(in_tmp_sessions)` |
| `test_oserror_on_rename_is_swallowed` | function | `tests/test_credentials_rotation.py:76` | `def test_oserror_on_rename_is_swallowed(in_tmp_sessions, monkeypatch)` |
| `test_race_on_rename_is_swallowed` | function | `tests/test_credentials_rotation.py:65` | `def test_race_on_rename_is_swallowed(in_tmp_sessions, monkeypatch)` |
| `_Request` | class | `tests/test_csrf_behavior.py:8` | `class _Request` |
| `__init__` | method | `tests/test_csrf_behavior.py:9` | `def __init__(self, method, path, headers, form)` |
| `test_given_authenticated_post_with_valid_token_then_allowed` | method | `tests/test_csrf_behavior.py:23` | `def test_given_authenticated_post_with_valid_token_then_allowed()` |
| `test_given_authenticated_post_without_token_then_rejected` | method | `tests/test_csrf_behavior.py:16` | `def test_given_authenticated_post_without_token_then_rejected()` |
| `test_given_get_request_then_always_allowed` | method | `tests/test_csrf_behavior.py:42` | `def test_given_get_request_then_always_allowed()` |
| `test_given_login_path_without_token_then_allowed` | method | `tests/test_csrf_behavior.py:35` | `def test_given_login_path_without_token_then_allowed()` |
| `TestCheckRequest` | class | `tests/test_csrf_policy.py:123` | `class TestCheckRequest` |
| `TestExemptions` | class | `tests/test_csrf_policy.py:81` | `class TestExemptions` |
| `TestRequestExtraction` | class | `tests/test_csrf_policy.py:96` | `class TestRequestExtraction` |
| `TestTokenIssuance` | class | `tests/test_csrf_policy.py:34` | `class TestTokenIssuance` |
| `TestTokenValidation` | class | `tests/test_csrf_policy.py:56` | `class TestTokenValidation` |
| `_FakeRequest` | class | `tests/test_csrf_policy.py:26` | `class _FakeRequest` |
| `__init__` | method | `tests/test_csrf_policy.py:27` | `def __init__(self, headers, form, path, method)` |
| `test_exempt_path_passes_without_token` | method | `tests/test_csrf_policy.py:84` | `def test_exempt_path_passes_without_token(self)` |
| `test_exempt_path_with_no_token_still_passes` | method | `tests/test_csrf_policy.py:146` | `def test_exempt_path_with_no_token_still_passes(self)` |
| `test_extract_form` | method | `tests/test_csrf_policy.py:104` | `def test_extract_form(self)` |
| `test_extract_header` | method | `tests/test_csrf_policy.py:99` | `def test_extract_header(self)` |
| `test_extract_header_takes_precedence` | method | `tests/test_csrf_policy.py:109` | `def test_extract_header_takes_precedence(self)` |
| `test_extract_returns_none_when_missing` | method | `tests/test_csrf_policy.py:117` | `def test_extract_returns_none_when_missing(self)` |
| `test_issue_is_deterministic_for_same_session` | method | `tests/test_csrf_policy.py:43` | `def test_issue_is_deterministic_for_same_session(self)` |
| `test_issue_is_unique_across_sessions` | method | `tests/test_csrf_policy.py:49` | `def test_issue_is_unique_across_sessions(self)` |
| `test_issue_returns_string` | method | `tests/test_csrf_policy.py:37` | `def test_issue_returns_string(self)` |
| `test_missing_token_fails` | method | `tests/test_csrf_policy.py:64` | `def test_missing_token_fails(self)` |
| `test_mutating_with_valid_token_passes` | method | `tests/test_csrf_policy.py:136` | `def test_mutating_with_valid_token_passes(self)` |
| `test_mutating_without_token_fails` | method | `tests/test_csrf_policy.py:131` | `def test_mutating_without_token_fails(self)` |
| `test_non_exempt_path_fails_check` | method | `tests/test_csrf_policy.py:90` | `def test_non_exempt_path_fails_check(self)` |
| `test_safe_methods_bypass` | method | `tests/test_csrf_policy.py:126` | `def test_safe_methods_bypass(self)` |
| `test_unknown_session_fails` | method | `tests/test_csrf_policy.py:70` | `def test_unknown_session_fails(self)` |
| `test_valid_token_passes` | method | `tests/test_csrf_policy.py:59` | `def test_valid_token_passes(self)` |
| `test_wrong_token_fails` | method | `tests/test_csrf_policy.py:75` | `def test_wrong_token_fails(self)` |
| `_now` | function | `tests/test_daemon_control.py:287` | `def _now()` |
| `_sleep` | function | `tests/test_daemon_control.py:252` | `def _sleep(_seconds)` |
| `_sleep` | function | `tests/test_daemon_control.py:290` | `def _sleep(_seconds)` |
| `_sleep` | function | `tests/test_daemon_control.py:309` | `def _sleep(_seconds)` |
| `sessions_dir` | function | `tests/test_daemon_control.py:46` | `def sessions_dir(tmp_path)` |
| `test_add_remove_clear_veto` | function | `tests/test_daemon_control.py:112` | `def test_add_remove_clear_veto(sessions_dir)` |
| `test_add_veto_rejects_empty_token` | function | `tests/test_daemon_control.py:128` | `def test_add_veto_rejects_empty_token(sessions_dir)` |
| `test_concurrent_save_serialised_by_lock` | function | `tests/test_daemon_control.py:346` | `def test_concurrent_save_serialised_by_lock(sessions_dir)` |
| `test_consume_expires_overdue_pending` | function | `tests/test_daemon_control.py:198` | `def test_consume_expires_overdue_pending(sessions_dir)` |
| `test_decide_rejects_invalid_decision` | function | `tests/test_daemon_control.py:183` | `def test_decide_rejects_invalid_decision(sessions_dir)` |
| `test_decide_with_unknown_id_returns_none` | function | `tests/test_daemon_control.py:191` | `def test_decide_with_unknown_id_returns_none(sessions_dir)` |
| `test_default_state_roundtrip` | function | `tests/test_daemon_control.py:52` | `def test_default_state_roundtrip(sessions_dir)` |
| `test_is_vetoed_uses_first_token` | function | `tests/test_daemon_control.py:135` | `def test_is_vetoed_uses_first_token(sessions_dir)` |
| `test_load_returns_defaults_on_invalid_json` | function | `tests/test_daemon_control.py:336` | `def test_load_returns_defaults_on_invalid_json(sessions_dir)` |
| `test_pause_resume_round_trip` | function | `tests/test_daemon_control.py:102` | `def test_pause_resume_round_trip(sessions_dir)` |
| `test_pending_action_is_expired_only_when_still_pending` | function | `tests/test_daemon_control.py:209` | `def test_pending_action_is_expired_only_when_still_pending()` |
| `test_propose_decide_consume_cycle` | function | `tests/test_daemon_control.py:163` | `def test_propose_decide_consume_cycle(sessions_dir)` |
| `test_save_writes_atomic_file_with_restricted_mode` | function | `tests/test_daemon_control.py:325` | `def test_save_writes_atomic_file_with_restricted_mode(sessions_dir)` |
| `test_set_focus_replaces_list` | function | `tests/test_daemon_control.py:143` | `def test_set_focus_replaces_list(sessions_dir)` |
| `test_set_mode_persists_and_normalises_invalid` | function | `tests/test_daemon_control.py:63` | `def test_set_mode_persists_and_normalises_invalid(sessions_dir)` |
| `test_state_from_dict_preserves_pending` | function | `tests/test_daemon_control.py:80` | `def test_state_from_dict_preserves_pending()` |
| `test_state_from_dict_sanitises_unknown_mode` | function | `tests/test_daemon_control.py:74` | `def test_state_from_dict_sanitises_unknown_mode()` |
| `test_target_in_focus_defaults_to_true_when_no_focus` | function | `tests/test_daemon_control.py:153` | `def test_target_in_focus_defaults_to_true_when_no_focus(sessions_dir)` |
| `test_wait_for_decision_expires_after_ttl` | function | `tests/test_daemon_control.py:233` | `def test_wait_for_decision_expires_after_ttl(sessions_dir)` |
| `test_wait_for_decision_polls_until_decided` | function | `tests/test_daemon_control.py:247` | `def test_wait_for_decision_polls_until_decided(sessions_dir)` |
| `test_wait_for_decision_returns_approved` | function | `tests/test_daemon_control.py:218` | `def test_wait_for_decision_returns_approved(sessions_dir)` |
| `test_wait_until_unpaused_returns_false_after_max_wait` | function | `tests/test_daemon_control.py:282` | `def test_wait_until_unpaused_returns_false_after_max_wait(sessions_dir)` |
| `test_wait_until_unpaused_returns_true_after_resume` | function | `tests/test_daemon_control.py:304` | `def test_wait_until_unpaused_returns_true_after_resume(sessions_dir)` |
| `test_wait_until_unpaused_returns_true_when_already_running` | function | `tests/test_daemon_control.py:268` | `def test_wait_until_unpaused_returns_true_when_already_running(sessions_dir)` |
| `DaemonSuiteConfig` | class | `tests/test_daemon_ctl_command_set.py:34` | `class DaemonSuiteConfig` |
| `_add_repo_root_to_syspath` | function | `tests/test_daemon_ctl_command_set.py:28` | `def _add_repo_root_to_syspath()` |
| `_methods_of` | method | `tests/test_daemon_ctl_command_set.py:53` | `def _methods_of(path, class_name)` |
| `test_no_command_collisions_with_source` | method | `tests/test_daemon_ctl_command_set.py:100` | `def test_no_command_collisions_with_source()` |
| `test_registry_registers_target` | method | `tests/test_daemon_ctl_command_set.py:93` | `def test_registry_registers_target()` |
| `test_source_no_longer_defines_cluster` | method | `tests/test_daemon_ctl_command_set.py:87` | `def test_source_no_longer_defines_cluster()` |
| `test_target_exposes_full_daemon_cluster` | method | `tests/test_daemon_ctl_command_set.py:74` | `def test_target_exposes_full_daemon_cluster()` |
| `test_target_is_active_command_set` | method | `tests/test_daemon_ctl_command_set.py:65` | `def test_target_is_active_command_set()` |
| `test_target_phase_metadata` | method | `tests/test_daemon_ctl_command_set.py:81` | `def test_target_phase_metadata()` |
| `TestDashboardIndexRoute` | class | `tests/test_dashboard_routes.py:308` | `class TestDashboardIndexRoute` |
| `TestLootRoute` | class | `tests/test_dashboard_routes.py:74` | `class TestLootRoute` |
| `TestTimelineRoute` | class | `tests/test_dashboard_routes.py:163` | `class TestTimelineRoute` |
| `_TestUser` | class | `tests/test_dashboard_routes.py:15` | `class _TestUser(UserMixin)` |
| `__init__` | method | `tests/test_dashboard_routes.py:16` | `def __init__(self, user_id)` |
| `_write_credentials_file` | method | `tests/test_dashboard_routes.py:44` | `def _write_credentials_file(sessions_dir, filename, lines)` |
| `_write_csv_report` | method | `tests/test_dashboard_routes.py:59` | `def _write_csv_report(sessions_dir, rows)` |
| `_write_events_jsonl` | method | `tests/test_dashboard_routes.py:68` | `def _write_events_jsonl(sessions_dir, events)` |
| `_write_hashes_file` | method | `tests/test_dashboard_routes.py:48` | `def _write_hashes_file(sessions_dir, filename, lines)` |
| `_write_loot_file` | method | `tests/test_dashboard_routes.py:52` | `def _write_loot_file(sessions_dir, rel_path, content)` |
| `client` | method | `tests/test_dashboard_routes.py:21` | `def client(tmp_path)` |
| `load_user` | method | `tests/test_dashboard_routes.py:33` | `def load_user(user_id)` |
| `test_dashboard_api_data_returns_json` | method | `tests/test_dashboard_routes.py:318` | `def test_dashboard_api_data_returns_json(self, client)` |
| `test_dashboard_index_returns_200` | method | `tests/test_dashboard_routes.py:311` | `def test_dashboard_index_returns_200(self, client)` |
| `test_loot_empty_returns_200` | method | `tests/test_dashboard_routes.py:98` | `def test_loot_empty_returns_200(self, client)` |
| `test_loot_multiple_credential_files` | method | `tests/test_dashboard_routes.py:148` | `def test_loot_multiple_credential_files(self, client)` |
| `test_loot_respects_max_entries` | method | `tests/test_dashboard_routes.py:131` | `def test_loot_respects_max_entries(self, client)` |
| `test_loot_route_returns_200_with_data` | method | `tests/test_dashboard_routes.py:77` | `def test_loot_route_returns_200_with_data(self, client)` |
| `test_loot_skips_comment_lines` | method | `tests/test_dashboard_routes.py:108` | `def test_loot_skips_comment_lines(self, client)` |
| `test_timeline_csv_without_timestamp` | method | `tests/test_dashboard_routes.py:221` | `def test_timeline_csv_without_timestamp(self, client)` |
| `test_timeline_empty_returns_200` | method | `tests/test_dashboard_routes.py:187` | `def test_timeline_empty_returns_200(self, client)` |
| `test_timeline_handles_csv_tool_column` | method | `tests/test_dashboard_routes.py:212` | `def test_timeline_handles_csv_tool_column(self, client)` |
| `test_timeline_handles_malformed_jsonl` | method | `tests/test_dashboard_routes.py:292` | `def test_timeline_handles_malformed_jsonl(self, client)` |
| `test_timeline_normalizes_iso_timestamps` | method | `tests/test_dashboard_routes.py:254` | `def test_timeline_normalizes_iso_timestamps(self, client)` |
| `test_timeline_only_csv_no_events` | method | `tests/test_dashboard_routes.py:280` | `def test_timeline_only_csv_no_events(self, client)` |
| `test_timeline_only_events_no_csv` | method | `tests/test_dashboard_routes.py:267` | `def test_timeline_only_events_no_csv(self, client)` |
| `test_timeline_respects_max_rows` | method | `tests/test_dashboard_routes.py:235` | `def test_timeline_respects_max_rows(self, client)` |
| `test_timeline_route_returns_200_with_data` | method | `tests/test_dashboard_routes.py:166` | `def test_timeline_route_returns_200_with_data(self, client)` |
| `test_timeline_sorted_newest_first` | method | `tests/test_dashboard_routes.py:195` | `def test_timeline_sorted_newest_first(self, client)` |
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
| `TestCaching` | class | `tests/test_detection_feed.py:67` | `class TestCaching` |
| `TestCategoryMap` | class | `tests/test_detection_feed.py:112` | `class TestCategoryMap` |
| `TestDetectionFeedInit` | class | `tests/test_detection_feed.py:13` | `class TestDetectionFeedInit` |
| `TestFeedbackAdjustment` | class | `tests/test_detection_feed.py:94` | `class TestFeedbackAdjustment` |
| `TestSigmaParsing` | class | `tests/test_detection_feed.py:26` | `class TestSigmaParsing` |
| `test_adjust_from_feedback` | method | `tests/test_detection_feed.py:100` | `def test_adjust_from_feedback(self, tmp_path)` |
| `test_adjust_from_feedback_no_file` | method | `tests/test_detection_feed.py:95` | `def test_adjust_from_feedback_no_file(self, tmp_path)` |
| `test_cache_and_load` | method | `tests/test_detection_feed.py:68` | `def test_cache_and_load(self, tmp_path)` |
| `test_category_mappings` | method | `tests/test_detection_feed.py:113` | `def test_category_mappings(self)` |
| `test_custom_sources` | method | `tests/test_detection_feed.py:19` | `def test_custom_sources(self, tmp_path)` |
| `test_default_init` | method | `tests/test_detection_feed.py:14` | `def test_default_init(self, tmp_path)` |
| `test_default_probability` | method | `tests/test_detection_feed.py:120` | `def test_default_probability(self)` |
| `test_extract_categories` | method | `tests/test_detection_feed.py:60` | `def test_extract_categories(self, tmp_path)` |
| `test_extract_keywords` | method | `tests/test_detection_feed.py:47` | `def test_extract_keywords(self, tmp_path)` |
| `test_extract_log_source` | method | `tests/test_detection_feed.py:27` | `def test_extract_log_source(self, tmp_path)` |
| `test_extract_log_source_minimal` | method | `tests/test_detection_feed.py:32` | `def test_extract_log_source_minimal(self, tmp_path)` |
| `test_extract_mitre` | method | `tests/test_detection_feed.py:37` | `def test_extract_mitre(self, tmp_path)` |
| `test_extract_mitre_none` | method | `tests/test_detection_feed.py:42` | `def test_extract_mitre_none(self, tmp_path)` |
| `test_load_cached_missing` | method | `tests/test_detection_feed.py:88` | `def test_load_cached_missing(self, tmp_path)` |
| `_runs_command` | function | `tests/test_docs_drift_contract.py:38` | `def _runs_command(step, command)` |
| `test_diffs_command_index` | function | `tests/test_docs_drift_contract.py:68` | `def test_diffs_command_index(workflow_steps)` |
| `test_diffs_commands_reference` | function | `tests/test_docs_drift_contract.py:75` | `def test_diffs_commands_reference(workflow_steps)` |
| `test_diffs_utils_reference` | function | `tests/test_docs_drift_contract.py:81` | `def test_diffs_utils_reference(workflow_steps)` |
| `test_regenerates_command_index` | function | `tests/test_docs_drift_contract.py:47` | `def test_regenerates_command_index(workflow_steps)` |
| `test_regenerates_commands_reference` | function | `tests/test_docs_drift_contract.py:54` | `def test_regenerates_commands_reference(workflow_steps)` |
| `test_regenerates_utils_reference` | function | `tests/test_docs_drift_contract.py:61` | `def test_regenerates_utils_reference(workflow_steps)` |
| `test_trigger_watches_generator_inputs` | function | `tests/test_docs_drift_contract.py:87` | `def test_trigger_watches_generator_inputs(workflow_text)` |
| `test_workflow_exists` | function | `tests/test_docs_drift_contract.py:43` | `def test_workflow_exists()` |
| `workflow_steps` | function | `tests/test_docs_drift_contract.py:27` | `def workflow_steps(workflow_text)` |
| `workflow_text` | function | `tests/test_docs_drift_contract.py:22` | `def workflow_text()` |
| `TestFileChecks` | class | `tests/test_doctor.py:115` | `class TestFileChecks` |
| `TestGatherAndRun` | class | `tests/test_doctor.py:194` | `class TestGatherAndRun` |
| `TestPackages` | class | `tests/test_doctor.py:80` | `class TestPackages` |
| `TestPythonVersion` | class | `tests/test_doctor.py:32` | `class TestPythonVersion` |
| `TestReportAggregation` | class | `tests/test_doctor.py:163` | `class TestReportAggregation` |
| `TestSecListsAndTools` | class | `tests/test_doctor.py:137` | `class TestSecListsAndTools` |
| `TestVirtualEnv` | class | `tests/test_doctor.py:51` | `class TestVirtualEnv` |
| `boom` | method | `tests/test_doctor.py:98` | `def boom(name)` |
| `test_active_venv_is_ok` | method | `tests/test_doctor.py:52` | `def test_active_venv_is_ok(self, tmp_path)` |
| `test_certificates_partial_warns` | method | `tests/test_doctor.py:130` | `def test_certificates_partial_warns(self, tmp_path)` |
| `test_certificates_present_is_ok` | method | `tests/test_doctor.py:125` | `def test_certificates_present_is_ok(self, tmp_path)` |
| `test_default_registry_has_core_packages` | method | `tests/test_doctor.py:105` | `def test_default_registry_has_core_packages(self)` |
| `test_exact_minimum_is_ok` | method | `tests/test_doctor.py:37` | `def test_exact_minimum_is_ok(self)` |
| `test_external_tools_present_and_missing` | method | `tests/test_doctor.py:147` | `def test_external_tools_present_and_missing(self)` |
| `test_finder_exception_treated_as_missing` | method | `tests/test_doctor.py:97` | `def test_finder_exception_treated_as_missing(self)` |
| `test_gather_report_populates_all_sections` | method | `tests/test_doctor.py:195` | `def test_gather_report_populates_all_sections(self, tmp_path)` |
| `test_import_name_differs_from_pip_name_where_expected` | method | `tests/test_doctor.py:109` | `def test_import_name_differs_from_pip_name_where_expected(self)` |
| `test_inactive_with_env_dir_warns_to_activate` | method | `tests/test_doctor.py:58` | `def test_inactive_with_env_dir_warns_to_activate(self, tmp_path)` |
| `test_missing_optional_package_warns` | method | `tests/test_doctor.py:92` | `def test_missing_optional_package_warns(self)` |
| `test_missing_required_package_fails` | method | `tests/test_doctor.py:86` | `def test_missing_required_package_fails(self)` |
| `test_no_venv_anywhere_warns_to_install` | method | `tests/test_doctor.py:66` | `def test_no_venv_anywhere_warns_to_install(self, tmp_path)` |
| `test_none_base_prefix_collapses_to_prefix` | method | `tests/test_doctor.py:73` | `def test_none_base_prefix_collapses_to_prefix(self, tmp_path)` |
| `test_old_version_fails` | method | `tests/test_doctor.py:41` | `def test_old_version_fails(self)` |
| `test_overall_status_fail_trips_healthy` | method | `tests/test_doctor.py:181` | `def test_overall_status_fail_trips_healthy(self)` |
| `test_overall_status_ok_when_all_ok` | method | `tests/test_doctor.py:164` | `def test_overall_status_ok_when_all_ok(self)` |
| `test_overall_status_warn_with_warnings_only` | method | `tests/test_doctor.py:171` | `def test_overall_status_warn_with_warnings_only(self)` |
| `test_payload_missing_fails` | method | `tests/test_doctor.py:120` | `def test_payload_missing_fails(self, tmp_path)` |
| `test_payload_present_is_ok` | method | `tests/test_doctor.py:116` | `def test_payload_present_is_ok(self, tmp_path)` |
| `test_present_required_package_is_ok` | method | `tests/test_doctor.py:81` | `def test_present_required_package_is_ok(self)` |
| `test_run_returns_report_without_raising` | method | `tests/test_doctor.py:204` | `def test_run_returns_report_without_raising(self, tmp_path)` |
| `test_seclists_found_is_ok` | method | `tests/test_doctor.py:138` | `def test_seclists_found_is_ok(self)` |
| `test_seclists_missing_warns` | method | `tests/test_doctor.py:143` | `def test_seclists_missing_warns(self)` |
| `test_supported_version_is_ok` | method | `tests/test_doctor.py:33` | `def test_supported_version_is_ok(self)` |
| `test_uses_live_interpreter_by_default` | method | `tests/test_doctor.py:46` | `def test_uses_live_interpreter_by_default(self)` |
| `EncodingSuiteConfig` | class | `tests/test_encoding_command_set.py:34` | `class EncodingSuiteConfig` |
| `_add_repo_root_to_syspath` | function | `tests/test_encoding_command_set.py:28` | `def _add_repo_root_to_syspath()` |
| `_methods_of` | method | `tests/test_encoding_command_set.py:59` | `def _methods_of(path, class_name)` |
| `test_no_command_collisions_with_source` | method | `tests/test_encoding_command_set.py:106` | `def test_no_command_collisions_with_source()` |
| `test_registry_registers_target` | method | `tests/test_encoding_command_set.py:99` | `def test_registry_registers_target()` |
| `test_source_no_longer_defines_cluster` | method | `tests/test_encoding_command_set.py:93` | `def test_source_no_longer_defines_cluster()` |
| `test_target_exposes_full_encoding_cluster` | method | `tests/test_encoding_command_set.py:80` | `def test_target_exposes_full_encoding_cluster()` |
| `test_target_is_active_command_set` | method | `tests/test_encoding_command_set.py:71` | `def test_target_is_active_command_set()` |
| `test_target_phase_metadata` | method | `tests/test_encoding_command_set.py:87` | `def test_target_phase_metadata()` |
| `TestApprovalGate` | class | `tests/test_engage_orchestrator.py:294` | `class TestApprovalGate` |
| `TestEngageOrchestrator` | class | `tests/test_engage_orchestrator.py:527` | `class TestEngageOrchestrator` |
| `TestEngagementNarrator` | class | `tests/test_engage_orchestrator.py:85` | `class TestEngagementNarrator` |
| `TestFileApprovalSink` | class | `tests/test_engage_orchestrator.py:395` | `class TestFileApprovalSink` |
| `TestIsValidTarget` | class | `tests/test_engage_orchestrator.py:242` | `class TestIsValidTarget` |
| `TestMcpEntryPoints` | class | `tests/test_engage_orchestrator.py:623` | `class TestMcpEntryPoints` |
| `TestNotificationBroadcaster` | class | `tests/test_engage_orchestrator.py:140` | `class TestNotificationBroadcaster` |
| `TestShellObtainedPublisher` | class | `tests/test_engage_orchestrator.py:192` | `class TestShellObtainedPublisher` |
| `TestStaticFallbackResolver` | class | `tests/test_engage_orchestrator.py:452` | `class TestStaticFallbackResolver` |
| `TestStdinApprovalSink` | class | `tests/test_engage_orchestrator.py:436` | `class TestStdinApprovalSink` |
| `TestWiring` | class | `tests/test_engage_orchestrator.py:671` | `class TestWiring` |
| `_BoomSink` | class | `tests/test_engage_orchestrator.py:166` | `class _BoomSink(INotificationSink)` |
| `_CountingSink` | class | `tests/test_engage_orchestrator.py:146` | `class _CountingSink(INotificationSink)` |
| `_GoodSink` | class | `tests/test_engage_orchestrator.py:174` | `class _GoodSink(INotificationSink)` |
| `_NoOpGate` | class | `tests/test_engage_orchestrator.py:498` | `class _NoOpGate` |
| `_RecordingSink` | class | `tests/test_engage_orchestrator.py:280` | `class _RecordingSink` |
| `_RejectingGate` | class | `tests/test_engage_orchestrator.py:508` | `class _RejectingGate` |
| `_ScriptedRunner` | class | `tests/test_engage_orchestrator.py:474` | `class _ScriptedRunner` |
| `__init__` | method | `tests/test_engage_orchestrator.py:147` | `def __init__(self, name)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:283` | `def __init__(self)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:482` | `def __init__(self, scripted)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:509` | `def __init__(self, rejected_phase)` |
| `_injected_sleep` | method | `tests/test_engage_orchestrator.py:334` | `def _injected_sleep(_seconds)` |
| `announce` | method | `tests/test_engage_orchestrator.py:287` | `def announce(self, request)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:154` | `def deliver(self, event)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:171` | `def deliver(self, event)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:179` | `def deliver(self, event)` |
| `name` | method | `tests/test_engage_orchestrator.py:151` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:168` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:176` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:494` | `def name(self)` |
| `policy_module` | method | `tests/test_engage_orchestrator.py:271` | `def policy_module(temp_sessions, monkeypatch)` |
| `request` | method | `tests/test_engage_orchestrator.py:499` | `def request(self, target, phase, command, reason)` |
| `request` | method | `tests/test_engage_orchestrator.py:512` | `def request(self, target, phase, command, reason)` |
| `resolution_for` | method | `tests/test_engage_orchestrator.py:290` | `def resolution_for(self, approval_id)` |
| `run` | method | `tests/test_engage_orchestrator.py:486` | `def run(self, command, timeout)` |
| `temp_sessions` | function | `tests/test_engage_orchestrator.py:47` | `def temp_sessions(tmp_path, monkeypatch)` |
| `test_accepts_hostname` | method | `tests/test_engage_orchestrator.py:249` | `def test_accepts_hostname(self)` |
| `test_accepts_ipv4` | method | `tests/test_engage_orchestrator.py:243` | `def test_accepts_ipv4(self)` |
| `test_announce_writes_pending_record` | method | `tests/test_engage_orchestrator.py:396` | `def test_announce_writes_pending_record(self, policy_module, temp_sessions)` |
| `test_approval_gate_defaults_to_true_when_key_missing` | method | `tests/test_engage_orchestrator.py:710` | `def test_approval_gate_defaults_to_true_when_key_missing(self, tmp_path)` |
| `test_auto_approve_true_returns_approved_for_gated_phase` | method | `tests/test_engage_orchestrator.py:295` | `def test_auto_approve_true_returns_approved_for_gated_phase(self, policy_module, temp_sessions)` |
| `test_client_id_is_sanitised` | method | `tests/test_engage_orchestrator.py:224` | `def test_client_id_is_sanitised(self, temp_sessions)` |
| `test_daemon_has_engage_subcommand` | method | `tests/test_engage_orchestrator.py:698` | `def test_daemon_has_engage_subcommand(self)` |
| `test_denied_step_is_skipped` | method | `tests/test_engage_orchestrator.py:580` | `def test_denied_step_is_skipped(self, temp_sessions, policy_module)` |
| `test_do_engage_method_exists_in_lazyown` | method | `tests/test_engage_orchestrator.py:672` | `def test_do_engage_method_exists_in_lazyown(self)` |
| `test_engage_approve_accepts_valid_decision` | method | `tests/test_engage_orchestrator.py:655` | `def test_engage_approve_accepts_valid_decision(self, temp_sessions, policy_module)` |
| `test_engage_approve_rejects_bad_decision` | method | `tests/test_engage_orchestrator.py:649` | `def test_engage_approve_rejects_bad_decision(self, temp_sessions, policy_module)` |
| `test_engage_status_returns_pending_approvals_structure` | method | `tests/test_engage_orchestrator.py:639` | `def test_engage_status_returns_pending_approvals_structure(self, temp_sessions, policy_module)` |
| `test_engage_target_rejects_invalid` | method | `tests/test_engage_orchestrator.py:624` | `def test_engage_target_rejects_invalid(self, temp_sessions, policy_module)` |
| `test_engage_target_returns_engagement_id` | method | `tests/test_engage_orchestrator.py:630` | `def test_engage_target_returns_engagement_id(self, temp_sessions, policy_module)` |
| `test_engagement_hooks_module_exposes_public_surface` | method | `tests/test_engage_orchestrator.py:726` | `def test_engagement_hooks_module_exposes_public_surface(self)` |
| `test_failing_sink_does_not_break_broadcaster` | method | `tests/test_engage_orchestrator.py:163` | `def test_failing_sink_does_not_break_broadcaster(self, temp_sessions)` |
| `test_fans_out_to_every_sink` | method | `tests/test_engage_orchestrator.py:141` | `def test_fans_out_to_every_sink(self, temp_sessions)` |
| `test_first_call_emits_event` | method | `tests/test_engage_orchestrator.py:193` | `def test_first_call_emits_event(self, temp_sessions)` |
| `test_gated_phase_times_out_to_denied` | method | `tests/test_engage_orchestrator.py:360` | `def test_gated_phase_times_out_to_denied(self, policy_module, temp_sessions)` |
| `test_gated_phase_with_auto_approve_false_polls_sink` | method | `tests/test_engage_orchestrator.py:328` | `def test_gated_phase_with_auto_approve_false_polls_sink(self, policy_module, temp_sessions)` |
| `test_invalid_client_id_returns_none` | method | `tests/test_engage_orchestrator.py:218` | `def test_invalid_client_id_returns_none(self, temp_sessions)` |
| `test_invalid_payload_defaults_to_auto_approve_true` | method | `tests/test_engage_orchestrator.py:381` | `def test_invalid_payload_defaults_to_auto_approve_true(self, policy_module, temp_sessions)` |
| `test_lazyc2_has_engagement_hook_call` | method | `tests/test_engage_orchestrator.py:682` | `def test_lazyc2_has_engagement_hook_call(self)` |
| `test_mcp_exposes_four_engage_tools` | method | `tests/test_engage_orchestrator.py:688` | `def test_mcp_exposes_four_engage_tools(self)` |
| `test_narrate_writes_log_and_audit` | method | `tests/test_engage_orchestrator.py:86` | `def test_narrate_writes_log_and_audit(self, temp_sessions)` |
| `test_no_tty_returns_none` | method | `tests/test_engage_orchestrator.py:437` | `def test_no_tty_returns_none(self, policy_module)` |
| `test_non_gated_phase_bypasses_sink` | method | `tests/test_engage_orchestrator.py:312` | `def test_non_gated_phase_bypasses_sink(self, policy_module, temp_sessions)` |
| `test_payload_json_auto_approve_key_is_bool_when_present` | method | `tests/test_engage_orchestrator.py:703` | `def test_payload_json_auto_approve_key_is_bool_when_present(self)` |
| `test_policy_module_exposes_approval_surface` | method | `tests/test_engage_orchestrator.py:739` | `def test_policy_module_exposes_approval_surface(self)` |
| `test_rejects_garbage` | method | `tests/test_engage_orchestrator.py:255` | `def test_rejects_garbage(self)` |
| `test_rejects_invalid_target` | method | `tests/test_engage_orchestrator.py:528` | `def test_rejects_invalid_target(self, temp_sessions, policy_module)` |
| `test_render_line_format_is_stable` | method | `tests/test_engage_orchestrator.py:124` | `def test_render_line_format_is_stable(self)` |
| `test_repeat_call_is_idempotent` | method | `tests/test_engage_orchestrator.py:210` | `def test_repeat_call_is_idempotent(self, temp_sessions)` |
| `test_resolution_returns_latest_non_pending` | method | `tests/test_engage_orchestrator.py:412` | `def test_resolution_returns_latest_non_pending(self, policy_module, temp_sessions)` |
| `test_returns_alternatives_in_order` | method | `tests/test_engage_orchestrator.py:453` | `def test_returns_alternatives_in_order(self)` |
| `test_runs_full_plan_on_success` | method | `tests/test_engage_orchestrator.py:534` | `def test_runs_full_plan_on_success(self, temp_sessions, policy_module)` |
| `test_shell_indicator_stops_loop` | method | `tests/test_engage_orchestrator.py:602` | `def test_shell_indicator_stops_loop(self, temp_sessions, policy_module)` |
| `test_stream_sink_appends_to_autonomous_events` | method | `tests/test_engage_orchestrator.py:111` | `def test_stream_sink_appends_to_autonomous_events(self, temp_sessions)` |
| `test_switches_tool_on_failure` | method | `tests/test_engage_orchestrator.py:556` | `def test_switches_tool_on_failure(self, temp_sessions, policy_module)` |
| `test_unknown_primary_returns_none` | method | `tests/test_engage_orchestrator.py:463` | `def test_unknown_primary_returns_none(self)` |
| `TestCuriosityEngine` | class | `tests/test_engagement_and_ping.py:168` | `class TestCuriosityEngine` |
| `TestEngagementState` | class | `tests/test_engagement_and_ping.py:57` | `class TestEngagementState` |
| `TestPingOsId` | class | `tests/test_engagement_and_ping.py:268` | `class TestPingOsId` |
| `TestRecommendNextCommandIndex` | class | `tests/test_engagement_and_ping.py:336` | `class TestRecommendNextCommandIndex` |
| `TestVRIScheduler` | class | `tests/test_engagement_and_ping.py:101` | `class TestVRIScheduler` |
| `_build_csv` | method | `tests/test_engagement_and_ping.py:351` | `def _build_csv(self, tmp_path, run_cmds)` |
| `_build_index` | method | `tests/test_engagement_and_ping.py:339` | `def _build_index(self, tmp_path, phase, n_cmds)` |
| `_command_location` | function | `tests/test_engagement_and_ping.py:30` | `def _command_location(name)` |
| `_extract_os_id_from_json` | method | `tests/test_engagement_and_ping.py:277` | `def _extract_os_id_from_json(self, data)` |
| `_make_params` | method | `tests/test_engagement_and_ping.py:274` | `def _make_params(self)` |
| `_make_state` | method | `tests/test_engagement_and_ping.py:169` | `def _make_state(self, seen)` |
| `_minimal_index` | method | `tests/test_engagement_and_ping.py:176` | `def _minimal_index(self, phase_cmds)` |
| `_ping_stdout` | method | `tests/test_engagement_and_ping.py:271` | `def _ping_stdout(self, ttl)` |
| `test_atomic_write_leaves_no_tmp_file` | method | `tests/test_engagement_and_ping.py:87` | `def test_atomic_write_leaves_no_tmp_file(self, tmp_path)` |
| `test_commands_seen_accumulates_across_calls` | method | `tests/test_engagement_and_ping.py:241` | `def test_commands_seen_accumulates_across_calls(self, tmp_path)` |
| `test_curiosity_does_not_repeat_in_session` | method | `tests/test_engagement_and_ping.py:194` | `def test_curiosity_does_not_repeat_in_session(self, capsys)` |
| `test_curiosity_shows_undiscovered_command` | method | `tests/test_engagement_and_ping.py:185` | `def test_curiosity_shows_undiscovered_command(self, capsys)` |
| `test_curiosity_silent_for_unknown_phase` | method | `tests/test_engagement_and_ping.py:233` | `def test_curiosity_silent_for_unknown_phase(self, capsys)` |
| `test_curiosity_silent_when_all_discovered` | method | `tests/test_engagement_and_ping.py:210` | `def test_curiosity_silent_when_all_discovered(self, capsys)` |
| `test_curiosity_silent_when_disabled` | method | `tests/test_engagement_and_ping.py:219` | `def test_curiosity_silent_when_disabled(self, capsys)` |
| `test_fallback_message_present` | method | `tests/test_engagement_and_ping.py:467` | `def test_fallback_message_present(self)` |
| `test_load_fresh_state_has_zero_commands` | method | `tests/test_engagement_and_ping.py:58` | `def test_load_fresh_state_has_zero_commands(self, tmp_path)` |
| `test_next_threshold_always_positive` | method | `tests/test_engagement_and_ping.py:102` | `def test_next_threshold_always_positive(self)` |
| `test_next_threshold_mean_near_target` | method | `tests/test_engagement_and_ping.py:108` | `def test_next_threshold_mean_near_target(self)` |
| `test_no_advisor_reference_before_definition` | method | `tests/test_engagement_and_ping.py:420` | `def test_no_advisor_reference_before_definition(self)` |
| `test_no_graph_nodes_in_output` | method | `tests/test_engagement_and_ping.py:407` | `def test_no_graph_nodes_in_output(self, tmp_path, capsys)` |
| `test_ping_os_json_contract` | method | `tests/test_engagement_and_ping.py:315` | `def test_ping_os_json_contract(self)` |
| `test_ping_persists_via_apply_assign` | method | `tests/test_engagement_and_ping.py:323` | `def test_ping_persists_via_apply_assign(self)` |
| `test_rule_not_used_without_import` | method | `tests/test_engagement_and_ping.py:460` | `def test_rule_not_used_without_import(self)` |
| `test_save_and_reload_state` | method | `tests/test_engagement_and_ping.py:72` | `def test_save_and_reload_state(self, tmp_path)` |
| `test_shows_nothing_when_all_run` | method | `tests/test_engagement_and_ping.py:388` | `def test_shows_nothing_when_all_run(self, tmp_path)` |
| `test_shows_unrun_commands` | method | `tests/test_engagement_and_ping.py:364` | `def test_shows_unrun_commands(self, tmp_path, capsys)` |
| `test_threshold_is_variable_not_constant` | method | `tests/test_engagement_and_ping.py:114` | `def test_threshold_is_variable_not_constant(self)` |
| `test_ttl_127_maps_to_os_id_2_windows` | method | `tests/test_engagement_and_ping.py:294` | `def test_ttl_127_maps_to_os_id_2_windows(self)` |
| `test_ttl_128_maps_to_os_id_2_windows` | method | `tests/test_engagement_and_ping.py:287` | `def test_ttl_128_maps_to_os_id_2_windows(self)` |
| `test_ttl_255_maps_to_unknown` | method | `tests/test_engagement_and_ping.py:308` | `def test_ttl_255_maps_to_unknown(self)` |
| `test_ttl_63_maps_to_os_id_1_linux` | method | `tests/test_engagement_and_ping.py:301` | `def test_ttl_63_maps_to_os_id_1_linux(self)` |
| `test_ttl_64_maps_to_os_id_1_linux` | method | `tests/test_engagement_and_ping.py:280` | `def test_ttl_64_maps_to_os_id_1_linux(self)` |
| `test_vri_does_not_fire_before_threshold` | method | `tests/test_engagement_and_ping.py:144` | `def test_vri_does_not_fire_before_threshold(self, tmp_path, capsys)` |
| `test_vri_fires_when_threshold_reached` | method | `tests/test_engagement_and_ping.py:119` | `def test_vri_fires_when_threshold_reached(self, tmp_path, capsys)` |
| `TestHealCommandsSeen` | class | `tests/test_engagement_command_gate.py:177` | `class TestHealCommandsSeen` |
| `TestHookRejectsNoise` | class | `tests/test_engagement_command_gate.py:105` | `class TestHookRejectsNoise` |
| `TestIsRecordableCommand` | class | `tests/test_engagement_command_gate.py:67` | `class TestIsRecordableCommand` |
| `TestSanitizeSeen` | class | `tests/test_engagement_command_gate.py:139` | `class TestSanitizeSeen` |
| `_redirect_paths` | function | `tests/test_engagement_command_gate.py:34` | `def _redirect_paths(tmp_path)` |
| `_restore_paths` | function | `tests/test_engagement_command_gate.py:56` | `def _restore_paths(saved)` |
| `test_accepts_command_shaped_tokens` | method | `tests/test_engagement_command_gate.py:71` | `def test_accepts_command_shaped_tokens(self, cmd)` |
| `test_do_prefixed_input_is_accepted` | method | `tests/test_engagement_command_gate.py:91` | `def test_do_prefixed_input_is_accepted(self)` |
| `test_garbage_does_not_enter_commands_seen` | method | `tests/test_engagement_command_gate.py:108` | `def test_garbage_does_not_enter_commands_seen(self, tmp_path)` |
| `test_idempotent_on_clean_state` | method | `tests/test_engagement_command_gate.py:197` | `def test_idempotent_on_clean_state(self, tmp_path)` |
| `test_load_state_heals_polluted_file` | method | `tests/test_engagement_command_gate.py:156` | `def test_load_state_heals_polluted_file(self, tmp_path)` |
| `test_normalize_is_idempotent` | method | `tests/test_engagement_command_gate.py:96` | `def test_normalize_is_idempotent(self)` |
| `test_purges_and_persists` | method | `tests/test_engagement_command_gate.py:180` | `def test_purges_and_persists(self, tmp_path)` |
| `test_quoted_path_rejected` | method | `tests/test_engagement_command_gate.py:86` | `def test_quoted_path_rejected(self)` |
| `test_real_command_recorded_between_garbage` | method | `tests/test_engagement_command_gate.py:122` | `def test_real_command_recorded_between_garbage(self, tmp_path)` |
| `test_rejects_syntactic_garbage` | method | `tests/test_engagement_command_gate.py:81` | `def test_rejects_syntactic_garbage(self, cmd)` |
| `test_roster_drops_valid_but_unknown_tokens` | method | `tests/test_engagement_command_gate.py:149` | `def test_roster_drops_valid_but_unknown_tokens(self)` |
| `test_syntactic_only_drops_ugly_garbage` | method | `tests/test_engagement_command_gate.py:142` | `def test_syntactic_only_drops_ugly_garbage(self)` |
| `TestAwardElo` | class | `tests/test_engagement_elo_and_methodology.py:113` | `class TestAwardElo` |
| `TestGetKarmaName` | class | `tests/test_engagement_elo_and_methodology.py:84` | `class TestGetKarmaName` |
| `TestKarmaUp` | class | `tests/test_engagement_elo_and_methodology.py:381` | `class TestKarmaUp` |
| `TestMethodologyRewards` | class | `tests/test_engagement_elo_and_methodology.py:288` | `class TestMethodologyRewards` |
| `TestPersistNotification` | class | `tests/test_engagement_elo_and_methodology.py:232` | `class TestPersistNotification` |
| `TestRenderEngagementHookIntegration` | class | `tests/test_engagement_elo_and_methodology.py:416` | `class TestRenderEngagementHookIntegration` |
| `TestStateSnapshot` | class | `tests/test_engagement_elo_and_methodology.py:474` | `class TestStateSnapshot` |
| `TestSyncUserElo` | class | `tests/test_engagement_elo_and_methodology.py:165` | `class TestSyncUserElo` |
| `_no_cli_operator` | function | `tests/test_engagement_elo_and_methodology.py:31` | `def _no_cli_operator(monkeypatch)` |
| `_redirect_paths` | function | `tests/test_engagement_elo_and_methodology.py:47` | `def _redirect_paths(tmp_path)` |
| `_restore_paths` | function | `tests/test_engagement_elo_and_methodology.py:74` | `def _restore_paths(saved)` |
| `test_all_bonuses_stack` | method | `tests/test_engagement_elo_and_methodology.py:138` | `def test_all_bonuses_stack(self)` |
| `test_appends_to_existing_file` | method | `tests/test_engagement_elo_and_methodology.py:243` | `def test_appends_to_existing_file(self, tmp_path)` |
| `test_atomic_rename_leaves_no_tmp` | method | `tests/test_engagement_elo_and_methodology.py:216` | `def test_atomic_rename_leaves_no_tmp(self, tmp_path)` |
| `test_base_only_for_unknown_command_and_phase` | method | `tests/test_engagement_elo_and_methodology.py:114` | `def test_base_only_for_unknown_command_and_phase(self)` |
| `test_creates_file_on_first_call` | method | `tests/test_engagement_elo_and_methodology.py:233` | `def test_creates_file_on_first_call(self, tmp_path)` |
| `test_disabled_flag_is_noop` | method | `tests/test_engagement_elo_and_methodology.py:460` | `def test_disabled_flag_is_noop(self, tmp_path, capsys)` |
| `test_do_prefix_is_stripped` | method | `tests/test_engagement_elo_and_methodology.py:157` | `def test_do_prefix_is_stripped(self)` |
| `test_elo_accumulates_across_commands` | method | `tests/test_engagement_elo_and_methodology.py:417` | `def test_elo_accumulates_across_commands(self, tmp_path)` |
| `test_fires_on_threshold_crossing` | method | `tests/test_engagement_elo_and_methodology.py:382` | `def test_fires_on_threshold_crossing(self, tmp_path, capsys)` |
| `test_first_time_bonus` | method | `tests/test_engagement_elo_and_methodology.py:128` | `def test_first_time_bonus(self)` |
| `test_first_time_bonus_only_once_per_command` | method | `tests/test_engagement_elo_and_methodology.py:431` | `def test_first_time_bonus_only_once_per_command(self, tmp_path)` |
| `test_high_value_bonus_applied` | method | `tests/test_engagement_elo_and_methodology.py:118` | `def test_high_value_bonus_applied(self)` |
| `test_idempotent_when_no_threshold_cross` | method | `tests/test_engagement_elo_and_methodology.py:395` | `def test_idempotent_when_no_threshold_cross(self, capsys)` |
| `test_ignores_non_positive_delta` | method | `tests/test_engagement_elo_and_methodology.py:207` | `def test_ignores_non_positive_delta(self, tmp_path)` |
| `test_new_phase_bonus` | method | `tests/test_engagement_elo_and_methodology.py:133` | `def test_new_phase_bonus(self)` |
| `test_note_reward_renders_latest` | method | `tests/test_engagement_elo_and_methodology.py:354` | `def test_note_reward_renders_latest(self, tmp_path, capsys)` |
| `test_note_reward_silent_when_empty` | method | `tests/test_engagement_elo_and_methodology.py:370` | `def test_note_reward_silent_when_empty(self, tmp_path, capsys)` |
| `test_objective_reward_silent_when_no_pending` | method | `tests/test_engagement_elo_and_methodology.py:343` | `def test_objective_reward_silent_when_no_pending(self, tmp_path, capsys)` |
| `test_objective_reward_uses_phase_to_next_cmd` | method | `tests/test_engagement_elo_and_methodology.py:325` | `def test_objective_reward_uses_phase_to_next_cmd(self, tmp_path, capsys)` |
| `test_patches_matching_username` | method | `tests/test_engagement_elo_and_methodology.py:166` | `def test_patches_matching_username(self, tmp_path)` |
| `test_persists_notification` | method | `tests/test_engagement_elo_and_methodology.py:401` | `def test_persists_notification(self, tmp_path)` |
| `test_phase_bonus_applied` | method | `tests/test_engagement_elo_and_methodology.py:123` | `def test_phase_bonus_applied(self)` |
| `test_recovers_from_corrupt_file` | method | `tests/test_engagement_elo_and_methodology.py:274` | `def test_recovers_from_corrupt_file(self, tmp_path)` |
| `test_returns_required_keys` | method | `tests/test_engagement_elo_and_methodology.py:475` | `def test_returns_required_keys(self, tmp_path)` |
| `test_ring_cap_drops_oldest` | method | `tests/test_engagement_elo_and_methodology.py:257` | `def test_ring_cap_drops_oldest(self, tmp_path)` |
| `test_silent_when_payload_missing` | method | `tests/test_engagement_elo_and_methodology.py:184` | `def test_silent_when_payload_missing(self, tmp_path)` |
| `test_silent_when_username_not_found` | method | `tests/test_engagement_elo_and_methodology.py:195` | `def test_silent_when_username_not_found(self, tmp_path)` |
| `test_task_reward_renders_pending_match` | method | `tests/test_engagement_elo_and_methodology.py:298` | `def test_task_reward_renders_pending_match(self, tmp_path, capsys)` |
| `test_task_reward_silent_when_all_done` | method | `tests/test_engagement_elo_and_methodology.py:313` | `def test_task_reward_silent_when_all_done(self, tmp_path, capsys)` |
| `test_task_reward_silent_when_no_file` | method | `tests/test_engagement_elo_and_methodology.py:289` | `def test_task_reward_silent_when_no_file(self, tmp_path, capsys)` |
| `test_thresholds` | method | `tests/test_engagement_elo_and_methodology.py:106` | `def test_thresholds(self, elo, expected)` |
| `test_users_json_syncd_when_payload_present` | method | `tests/test_engagement_elo_and_methodology.py:446` | `def test_users_json_syncd_when_payload_present(self, tmp_path)` |
| `TestBuildEvidenceHints` | class | `tests/test_evidence_hints.py:86` | `class TestBuildEvidenceHints` |
| `TestConfidenceFromScore` | class | `tests/test_evidence_hints.py:62` | `class TestConfidenceFromScore` |
| `TestRecommendWithEvidence` | class | `tests/test_evidence_hints.py:148` | `class TestRecommendWithEvidence` |
| `TestRenderEvidenceHints` | class | `tests/test_evidence_hints.py:133` | `class TestRenderEvidenceHints` |
| `TestTipsEngineEvidenceWiring` | class | `tests/test_evidence_hints.py:184` | `class TestTipsEngineEvidenceWiring` |
| `_FakeEngine` | class | `tests/test_evidence_hints.py:50` | `class _FakeEngine` |
| `__init__` | method | `tests/test_evidence_hints.py:53` | `def __init__(self, recs)` |
| `_engine_with_stub` | method | `tests/test_evidence_hints.py:176` | `def _engine_with_stub(sessions, recs, evidence)` |
| `_rec` | function | `tests/test_evidence_hints.py:33` | `def _rec(action, score, reasons, sources, command_preview)` |
| `recommend` | method | `tests/test_evidence_hints.py:57` | `def recommend(self, ctx)` |
| `test_bounded_in_unit_range_scaled` | method | `tests/test_evidence_hints.py:80` | `def test_bounded_in_unit_range_scaled(self)` |
| `test_disabled_flag_returns_empty` | method | `tests/test_evidence_hints.py:185` | `def test_disabled_flag_returns_empty(self, tmp_sessions_with_csv)` |
| `test_empty_list_prints_nothing` | method | `tests/test_evidence_hints.py:143` | `def test_empty_list_prints_nothing(self, capsys)` |
| `test_filters_already_run_commands` | method | `tests/test_evidence_hints.py:204` | `def test_filters_already_run_commands(self, tmp_sessions_with_csv)` |
| `test_half_score_constant_yields_fifty` | method | `tests/test_evidence_hints.py:69` | `def test_half_score_constant_yields_fifty(self)` |
| `test_maps_core_fields` | method | `tests/test_evidence_hints.py:87` | `def test_maps_core_fields(self)` |
| `test_missing_engine_returns_empty` | method | `tests/test_evidence_hints.py:189` | `def test_missing_engine_returns_empty(self, tmp_sessions_with_csv)` |
| `test_monotonic_non_decreasing` | method | `tests/test_evidence_hints.py:72` | `def test_monotonic_non_decreasing(self)` |
| `test_negative_score_floored_to_zero` | method | `tests/test_evidence_hints.py:66` | `def test_negative_score_floored_to_zero(self)` |
| `test_never_reaches_or_exceeds_hundred` | method | `tests/test_evidence_hints.py:76` | `def test_never_reaches_or_exceeds_hundred(self)` |
| `test_phase_override_reaches_engine_context` | method | `tests/test_evidence_hints.py:154` | `def test_phase_override_reaches_engine_context(self)` |
| `test_prefers_command_preview_over_action` | method | `tests/test_evidence_hints.py:106` | `def test_prefers_command_preview_over_action(self)` |
| `test_prints_verb_confidence_and_reason` | method | `tests/test_evidence_hints.py:134` | `def test_prints_verb_confidence_and_reason(self, capsys)` |
| `test_render_falls_back_to_bare_names` | method | `tests/test_evidence_hints.py:224` | `def test_render_falls_back_to_bare_names(self, tmp_sessions_with_csv)` |
| `test_render_prefers_evidence_over_bare_names` | method | `tests/test_evidence_hints.py:216` | `def test_render_prefers_evidence_over_bare_names(self, tmp_sessions_with_csv)` |
| `test_respects_limit` | method | `tests/test_evidence_hints.py:121` | `def test_respects_limit(self)` |
| `test_returns_engine_output` | method | `tests/test_evidence_hints.py:149` | `def test_returns_engine_output(self)` |
| `test_returns_evidence_hints` | method | `tests/test_evidence_hints.py:196` | `def test_returns_evidence_hints(self, tmp_sessions_with_csv)` |
| `test_skips_recommendation_without_reason` | method | `tests/test_evidence_hints.py:117` | `def test_skips_recommendation_without_reason(self)` |
| `test_skips_recommendation_without_verb` | method | `tests/test_evidence_hints.py:113` | `def test_skips_recommendation_without_verb(self)` |
| `test_strips_source_tag_from_reason` | method | `tests/test_evidence_hints.py:100` | `def test_strips_source_tag_from_reason(self)` |
| `test_target_falls_back_to_rhost` | method | `tests/test_evidence_hints.py:159` | `def test_target_falls_back_to_rhost(self)` |
| `test_truncates_long_reason` | method | `tests/test_evidence_hints.py:127` | `def test_truncates_long_reason(self)` |
| `test_zero_score_is_zero_confidence` | method | `tests/test_evidence_hints.py:63` | `def test_zero_score_is_zero_confidence(self)` |
| `tmp_sessions_with_csv` | method | `tests/test_evidence_hints.py:166` | `def tmp_sessions_with_csv()` |
| `FakeProc` | class | `tests/test_exploitgym_gym.py:145` | `class FakeProc` |
| `FakeProc` | class | `tests/test_exploitgym_gym.py:179` | `class FakeProc` |
| `_add_repo_root_to_syspath` | function | `tests/test_exploitgym_gym.py:18` | `def _add_repo_root_to_syspath()` |
| `_params` | function | `tests/test_exploitgym_gym.py:39` | `def _params(root)` |

Next: [SYMBOLS_p30.md](SYMBOLS_p30.md)
