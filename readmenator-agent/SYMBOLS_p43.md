# Symbols (page 43 of 44)
Previous: [SYMBOLS_p42.md](SYMBOLS_p42.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_rejects_absolute` | method | `tests/test_security_sanitizers.py:125` | `def test_rejects_absolute(self, cfg, tmp_path)` |
| `test_rejects_control_characters` | method | `tests/test_security_sanitizers.py:85` | `def test_rejects_control_characters(self, cfg)` |
| `test_rejects_non_string_template` | method | `tests/test_security_sanitizers.py:242` | `def test_rejects_non_string_template(self, cfg)` |
| `test_rejects_null_byte` | method | `tests/test_security_sanitizers.py:131` | `def test_rejects_null_byte(self, cfg, tmp_path)` |
| `test_rejects_parent_traversal` | method | `tests/test_security_sanitizers.py:119` | `def test_rejects_parent_traversal(self, cfg, tmp_path)` |
| `test_rejects_too_many_segments` | method | `tests/test_security_sanitizers.py:136` | `def test_rejects_too_many_segments(self, cfg, tmp_path)` |
| `test_resolves_valid_path` | method | `tests/test_security_sanitizers.py:142` | `def test_resolves_valid_path(self, cfg, tmp_path)` |
| `test_strips_cr_lf_nul` | method | `tests/test_security_sanitizers.py:77` | `def test_strips_cr_lf_nul(self, cfg)` |
| `test_unknown_objects_become_sentinel` | method | `tests/test_security_sanitizers.py:300` | `def test_unknown_objects_become_sentinel(self, cfg)` |
| `test_unspecified_requires_opt_in` | method | `tests/test_security_sanitizers.py:187` | `def test_unspecified_requires_opt_in(self, cfg)` |
| `test_valid_name_accepts_rfc7230_tokens` | method | `tests/test_security_sanitizers.py:96` | `def test_valid_name_accepts_rfc7230_tokens(self, cfg)` |
| `_console_text` | function | `tests/test_session_brief.py:31` | `def _console_text(renderable)` |
| `sandbox` | function | `tests/test_session_brief.py:18` | `def sandbox(tmp_path, monkeypatch)` |
| `test_brief_covers_target_phase_and_layers` | function | `tests/test_session_brief.py:39` | `def test_brief_covers_target_phase_and_layers(sandbox)` |
| `test_brief_never_raises_on_empty_stores` | function | `tests/test_session_brief.py:58` | `def test_brief_never_raises_on_empty_stores(tmp_path, monkeypatch)` |
| `test_brief_shows_newest_task` | function | `tests/test_session_brief.py:70` | `def test_brief_shows_newest_task(sandbox)` |
| `test_console_brief_respects_hints_off` | function | `tests/test_session_brief.py:81` | `def test_console_brief_respects_hints_off(tmp_path, monkeypatch)` |
| `SessionOpsSuiteConfig` | class | `tests/test_session_ops_command_set.py:38` | `class SessionOpsSuiteConfig` |
| `_add_repo_root_to_syspath` | function | `tests/test_session_ops_command_set.py:32` | `def _add_repo_root_to_syspath()` |
| `_methods_of` | function | `tests/test_session_ops_command_set.py:82` | `def _methods_of(path, class_name)` |
| `test_no_command_collisions_with_source` | function | `tests/test_session_ops_command_set.py:129` | `def test_no_command_collisions_with_source()` |
| `test_registry_registers_target` | function | `tests/test_session_ops_command_set.py:122` | `def test_registry_registers_target()` |
| `test_source_no_longer_defines_cluster` | function | `tests/test_session_ops_command_set.py:116` | `def test_source_no_longer_defines_cluster()` |
| `test_target_exposes_full_session_cluster` | function | `tests/test_session_ops_command_set.py:103` | `def test_target_exposes_full_session_cluster()` |
| `test_target_is_active_command_set` | function | `tests/test_session_ops_command_set.py:94` | `def test_target_is_active_command_set()` |
| `test_target_phase_metadata` | function | `tests/test_session_ops_command_set.py:110` | `def test_target_phase_metadata()` |
| `_populate` | function | `tests/test_sessions_browser.py:24` | `def _populate(tmp_path)` |
| `test_category_label_for_known_identifier` | function | `tests/test_sessions_browser.py:89` | `def test_category_label_for_known_identifier(tmp_path)` |
| `test_index_groups_known_files` | function | `tests/test_sessions_browser.py:34` | `def test_index_groups_known_files(tmp_path)` |
| `test_index_other_bucket_contains_unmatched_files` | function | `tests/test_sessions_browser.py:47` | `def test_index_other_bucket_contains_unmatched_files(tmp_path)` |
| `test_preview_flags_binary_files` | function | `tests/test_sessions_browser.py:64` | `def test_preview_flags_binary_files(tmp_path)` |
| `test_preview_rejects_path_traversal` | function | `tests/test_sessions_browser.py:71` | `def test_preview_rejects_path_traversal(tmp_path)` |
| `test_preview_returns_text_for_text_files` | function | `tests/test_sessions_browser.py:56` | `def test_preview_returns_text_for_text_files(tmp_path)` |
| `test_state_filter_keeps_matching_entries` | function | `tests/test_sessions_browser.py:79` | `def test_state_filter_keeps_matching_entries(tmp_path)` |
| `_FakePopen` | class | `tests/test_shell_semantics.py:75` | `class _FakePopen` |
| `__init__` | method | `tests/test_shell_semantics.py:76` | `def __init__(self, argv)` |
| `test_linpeas_http_server_is_detached` | function | `tests/test_shell_semantics.py:69` | `def test_linpeas_http_server_is_detached(monkeypatch)` |
| `test_needs_shell_accepts_plain_argv` | function | `tests/test_shell_semantics.py:32` | `def test_needs_shell_accepts_plain_argv()` |
| `test_needs_shell_detects_control_and_expansion` | function | `tests/test_shell_semantics.py:17` | `def test_needs_shell_detects_control_and_expansion()` |
| `test_run_command_expands_tilde_and_glob` | function | `tests/test_shell_semantics.py:45` | `def test_run_command_expands_tilde_and_glob(tmp_path, monkeypatch)` |
| `test_run_command_interprets_semicolon` | function | `tests/test_shell_semantics.py:38` | `def test_run_command_interprets_semicolon()` |
| `test_safe_runner_interprets_shell_syntax` | function | `tests/test_shell_semantics.py:87` | `def test_safe_runner_interprets_shell_syntax()` |
| `test_terminal_env_forces_color` | function | `tests/test_shell_semantics.py:53` | `def test_terminal_env_forces_color(monkeypatch)` |
| `test_terminal_env_respects_no_color` | function | `tests/test_shell_semantics.py:61` | `def test_terminal_env_respects_no_color(monkeypatch)` |
| `ShellsysSuiteConfig` | class | `tests/test_shellsys_command_set.py:38` | `class ShellsysSuiteConfig` |
| `_add_repo_root_to_syspath` | function | `tests/test_shellsys_command_set.py:32` | `def _add_repo_root_to_syspath()` |
| `_methods_of` | function | `tests/test_shellsys_command_set.py:61` | `def _methods_of(path, class_name)` |
| `test_no_command_collisions_with_source` | function | `tests/test_shellsys_command_set.py:108` | `def test_no_command_collisions_with_source()` |
| `test_registry_registers_target` | function | `tests/test_shellsys_command_set.py:101` | `def test_registry_registers_target()` |
| `test_source_no_longer_defines_cluster` | function | `tests/test_shellsys_command_set.py:95` | `def test_source_no_longer_defines_cluster()` |
| `test_target_exposes_full_shellsys_cluster` | function | `tests/test_shellsys_command_set.py:82` | `def test_target_exposes_full_shellsys_cluster()` |
| `test_target_is_active_command_set` | function | `tests/test_shellsys_command_set.py:73` | `def test_target_is_active_command_set()` |
| `test_target_phase_metadata` | function | `tests/test_shellsys_command_set.py:89` | `def test_target_phase_metadata()` |
| `TestBlueprintRouteContainment` | class | `tests/test_short_url_file_containment.py:105` | `class TestBlueprintRouteContainment` |
| `TestContainedPaths` | class | `tests/test_short_url_file_containment.py:36` | `class TestContainedPaths` |
| `TestRejectedPaths` | class | `tests/test_short_url_file_containment.py:51` | `class TestRejectedPaths` |
| `TestRouteStatusContract` | class | `tests/test_short_url_file_containment.py:78` | `class TestRouteStatusContract` |
| `sessions_dir` | function | `tests/test_short_url_file_containment.py:26` | `def sessions_dir(tmp_path, monkeypatch)` |
| `test_abort_propagates` | method | `tests/test_short_url_file_containment.py:86` | `def test_abort_propagates(self)` |
| `test_absolute_inside_base` | method | `tests/test_short_url_file_containment.py:41` | `def test_absolute_inside_base(self, sessions_dir)` |
| `test_absolute_outside_rejected` | method | `tests/test_short_url_file_containment.py:55` | `def test_absolute_outside_rejected(self, sessions_dir)` |
| `test_bare_relative_inside_base` | method | `tests/test_short_url_file_containment.py:37` | `def test_bare_relative_inside_base(self, sessions_dir)` |
| `test_blueprint_redirect_uses_contained_resolver` | method | `tests/test_short_url_file_containment.py:112` | `def test_blueprint_redirect_uses_contained_resolver(self)` |
| `test_empty_rejected` | method | `tests/test_short_url_file_containment.py:74` | `def test_empty_rejected(self, sessions_dir)` |
| `test_file_scheme_inside_base` | method | `tests/test_short_url_file_containment.py:45` | `def test_file_scheme_inside_base(self, sessions_dir)` |
| `test_file_scheme_outside_rejected` | method | `tests/test_short_url_file_containment.py:58` | `def test_file_scheme_outside_rejected(self, sessions_dir)` |
| `test_remote_url_rejected` | method | `tests/test_short_url_file_containment.py:52` | `def test_remote_url_rejected(self, sessions_dir)` |
| `test_symlink_escape_rejected` | method | `tests/test_short_url_file_containment.py:64` | `def test_symlink_escape_rejected(self, sessions_dir, tmp_path)` |
| `test_traversal_rejected` | method | `tests/test_short_url_file_containment.py:61` | `def test_traversal_rejected(self, sessions_dir)` |
| `TestDeadForkRemoved` | class | `tests/test_single_implementation.py:54` | `class TestDeadForkRemoved` |
| `test_live_utils_implementations_intact` | method | `tests/test_single_implementation.py:68` | `def test_live_utils_implementations_intact(self)` |
| `test_no_divergent_copies_in_core_namespace` | method | `tests/test_single_implementation.py:59` | `def test_no_divergent_copies_in_core_namespace(self)` |
| `test_no_divergent_copies_in_core_parsers` | method | `tests/test_single_implementation.py:55` | `def test_no_divergent_copies_in_core_parsers(self)` |
| `test_shared_kernel_still_available` | method | `tests/test_single_implementation.py:63` | `def test_shared_kernel_still_available(self)` |
| `TestBedEnumValues` | class | `tests/test_sleep_obfuscation.py:307` | `class TestBedEnumValues` |
| `TestSleepObfuscationConfig` | class | `tests/test_sleep_obfuscation.py:71` | `class TestSleepObfuscationConfig` |
| `TestSleepObfuscationEngine` | class | `tests/test_sleep_obfuscation.py:212` | `class TestSleepObfuscationEngine` |
| `TestSleepTechnique` | class | `tests/test_sleep_obfuscation.py:33` | `class TestSleepTechnique` |
| `TestSleepTechniqueCatalog` | class | `tests/test_sleep_obfuscation.py:114` | `class TestSleepTechniqueCatalog` |
| `TestSleepTechniqueValidator` | class | `tests/test_sleep_obfuscation.py:164` | `class TestSleepTechniqueValidator` |
| `test_configure_updates_config` | method | `tests/test_sleep_obfuscation.py:230` | `def test_configure_updates_config(self)` |
| `test_configure_without_overrides` | method | `tests/test_sleep_obfuscation.py:239` | `def test_configure_without_overrides(self)` |
| `test_construction_and_properties` | method | `tests/test_sleep_obfuscation.py:34` | `def test_construction_and_properties(self)` |
| `test_custom_catalog` | method | `tests/test_sleep_obfuscation.py:293` | `def test_custom_catalog(self)` |
| `test_default_catalog_has_techniques` | method | `tests/test_sleep_obfuscation.py:115` | `def test_default_catalog_has_techniques(self)` |
| `test_default_construction` | method | `tests/test_sleep_obfuscation.py:72` | `def test_default_construction(self)` |
| `test_default_engine` | method | `tests/test_sleep_obfuscation.py:213` | `def test_default_engine(self)` |
| `test_defaults` | method | `tests/test_sleep_obfuscation.py:48` | `def test_defaults(self)` |
| `test_ekko_requires_rop_gadgets` | method | `tests/test_sleep_obfuscation.py:173` | `def test_ekko_requires_rop_gadgets(self)` |
| `test_excessive_rop_gadget_count` | method | `tests/test_sleep_obfuscation.py:181` | `def test_excessive_rop_gadget_count(self)` |
| `test_excessive_sleep_delay` | method | `tests/test_sleep_obfuscation.py:197` | `def test_excessive_sleep_delay(self)` |
| `test_from_dict_empty` | method | `tests/test_sleep_obfuscation.py:102` | `def test_from_dict_empty(self)` |
| `test_from_dict_empty` | method | `tests/test_sleep_obfuscation.py:288` | `def test_from_dict_empty(self)` |
| `test_from_dict_partial` | method | `tests/test_sleep_obfuscation.py:107` | `def test_from_dict_partial(self)` |
| `test_from_dict_roundtrip` | method | `tests/test_sleep_obfuscation.py:278` | `def test_from_dict_roundtrip(self)` |
| `test_get_missing_raises_keyerror` | method | `tests/test_sleep_obfuscation.py:131` | `def test_get_missing_raises_keyerror(self)` |
| `test_immutability` | method | `tests/test_sleep_obfuscation.py:60` | `def test_immutability(self)` |
| `test_list_all_sorted_by_resistance` | method | `tests/test_sleep_obfuscation.py:136` | `def test_list_all_sorted_by_resistance(self)` |
| `test_list_by_platform_linux` | method | `tests/test_sleep_obfuscation.py:149` | `def test_list_by_platform_linux(self)` |
| `test_list_by_platform_windows` | method | `tests/test_sleep_obfuscation.py:142` | `def test_list_by_platform_windows(self)` |
| `test_list_names` | method | `tests/test_sleep_obfuscation.py:156` | `def test_list_names(self)` |
| `test_negative_sleep_delay` | method | `tests/test_sleep_obfuscation.py:189` | `def test_negative_sleep_delay(self)` |
| `test_os_platform_values` | method | `tests/test_sleep_obfuscation.py:308` | `def test_os_platform_values(self)` |
| `test_recommend_linux` | method | `tests/test_sleep_obfuscation.py:263` | `def test_recommend_linux(self)` |
| `test_recommend_windows` | method | `tests/test_sleep_obfuscation.py:257` | `def test_recommend_windows(self)` |
| `test_register_and_get` | method | `tests/test_sleep_obfuscation.py:120` | `def test_register_and_get(self)` |
| `test_select_existing_technique` | method | `tests/test_sleep_obfuscation.py:219` | `def test_select_existing_technique(self)` |
| `test_select_missing_technique` | method | `tests/test_sleep_obfuscation.py:225` | `def test_select_missing_technique(self)` |
| `test_serialization_roundtrip` | method | `tests/test_sleep_obfuscation.py:79` | `def test_serialization_roundtrip(self)` |
| `test_technique_risk_values` | method | `tests/test_sleep_obfuscation.py:312` | `def test_technique_risk_values(self)` |
| `test_to_dict` | method | `tests/test_sleep_obfuscation.py:270` | `def test_to_dict(self)` |
| `test_valid_config_passes` | method | `tests/test_sleep_obfuscation.py:165` | `def test_valid_config_passes(self)` |
| `test_validate_config_enabled_without_name` | method | `tests/test_sleep_obfuscation.py:205` | `def test_validate_config_enabled_without_name(self)` |
| `test_validate_unknown_technique` | method | `tests/test_sleep_obfuscation.py:251` | `def test_validate_unknown_technique(self)` |
| `test_validate_valid_config` | method | `tests/test_sleep_obfuscation.py:246` | `def test_validate_valid_config(self)` |
| `TestSocksEnums` | class | `tests/test_socks_proxy.py:373` | `class TestSocksEnums` |
| `TestSocksProxyConfig` | class | `tests/test_socks_proxy.py:33` | `class TestSocksProxyConfig` |
| `TestSocksProxyEngine` | class | `tests/test_socks_proxy.py:247` | `class TestSocksProxyEngine` |
| `TestSocksReply` | class | `tests/test_socks_proxy.py:359` | `class TestSocksReply` |
| `TestSocksSession` | class | `tests/test_socks_proxy.py:84` | `class TestSocksSession` |
| `TestSocksValidator` | class | `tests/test_socks_proxy.py:119` | `class TestSocksValidator` |
| `test_add_bytes` | method | `tests/test_socks_proxy.py:288` | `def test_add_bytes(self)` |
| `test_add_bytes_to_nonexistent` | method | `tests/test_socks_proxy.py:296` | `def test_add_bytes_to_nonexistent(self)` |
| `test_address_type_values` | method | `tests/test_socks_proxy.py:384` | `def test_address_type_values(self)` |
| `test_auth_method_values` | method | `tests/test_socks_proxy.py:374` | `def test_auth_method_values(self)` |
| `test_build_spec` | method | `tests/test_socks_proxy.py:253` | `def test_build_spec(self)` |
| `test_byte_counters` | method | `tests/test_socks_proxy.py:97` | `def test_byte_counters(self)` |
| `test_cleanup_expired` | method | `tests/test_socks_proxy.py:309` | `def test_cleanup_expired(self)` |
| `test_command_values` | method | `tests/test_socks_proxy.py:379` | `def test_command_values(self)` |
| `test_construction_and_defaults` | method | `tests/test_socks_proxy.py:85` | `def test_construction_and_defaults(self)` |
| `test_create_session` | method | `tests/test_socks_proxy.py:260` | `def test_create_session(self)` |
| `test_default_construction` | method | `tests/test_socks_proxy.py:34` | `def test_default_construction(self)` |
| `test_default_engine` | method | `tests/test_socks_proxy.py:248` | `def test_default_engine(self)` |
| `test_elapsed_seconds_with_zero_timestamp` | method | `tests/test_socks_proxy.py:113` | `def test_elapsed_seconds_with_zero_timestamp(self)` |
| `test_from_dict` | method | `tests/test_socks_proxy.py:326` | `def test_from_dict(self)` |
| `test_from_dict_empty` | method | `tests/test_socks_proxy.py:73` | `def test_from_dict_empty(self)` |
| `test_from_dict_unknown_auth_method_handled` | method | `tests/test_socks_proxy.py:78` | `def test_from_dict_unknown_auth_method_handled(self)` |
| `test_from_payload` | method | `tests/test_socks_proxy.py:337` | `def test_from_payload(self)` |
| `test_from_payload_empty` | method | `tests/test_socks_proxy.py:348` | `def test_from_payload_empty(self)` |
| `test_general_failure_message` | method | `tests/test_socks_proxy.py:363` | `def test_general_failure_message(self)` |
| `test_get_nonexistent_session` | method | `tests/test_socks_proxy.py:284` | `def test_get_nonexistent_session(self)` |
| `test_get_session` | method | `tests/test_socks_proxy.py:277` | `def test_get_session(self)` |
| `test_invalid_allowed_ports` | method | `tests/test_socks_proxy.py:178` | `def test_invalid_allowed_ports(self)` |
| `test_invalid_bind_address` | method | `tests/test_socks_proxy.py:126` | `def test_invalid_bind_address(self)` |
| `test_invalid_bind_port` | method | `tests/test_socks_proxy.py:132` | `def test_invalid_bind_port(self)` |
| `test_list_sessions` | method | `tests/test_socks_proxy.py:317` | `def test_list_sessions(self)` |
| `test_max_connections_limit` | method | `tests/test_socks_proxy.py:300` | `def test_max_connections_limit(self)` |
| `test_max_connections_zero` | method | `tests/test_socks_proxy.py:138` | `def test_max_connections_zero(self)` |
| `test_negative_bandwidth` | method | `tests/test_socks_proxy.py:156` | `def test_negative_bandwidth(self)` |
| `test_no_auth_methods` | method | `tests/test_socks_proxy.py:172` | `def test_no_auth_methods(self)` |
| `test_port_in_both_lists` | method | `tests/test_socks_proxy.py:184` | `def test_port_in_both_lists(self)` |
| `test_remove_nonexistent_session` | method | `tests/test_socks_proxy.py:273` | `def test_remove_nonexistent_session(self)` |
| `test_remove_session` | method | `tests/test_socks_proxy.py:267` | `def test_remove_session(self)` |
| `test_serialization_roundtrip` | method | `tests/test_socks_proxy.py:42` | `def test_serialization_roundtrip(self)` |
| `test_session_timeout_too_high` | method | `tests/test_socks_proxy.py:150` | `def test_session_timeout_too_high(self)` |
| `test_session_timeout_too_low` | method | `tests/test_socks_proxy.py:144` | `def test_session_timeout_too_low(self)` |
| `test_succeeded_message` | method | `tests/test_socks_proxy.py:360` | `def test_succeeded_message(self)` |
| `test_to_dict` | method | `tests/test_socks_proxy.py:104` | `def test_to_dict(self)` |
| `test_unknown_code_message` | method | `tests/test_socks_proxy.py:366` | `def test_unknown_code_message(self)` |
| `test_username_password_without_credentials` | method | `tests/test_socks_proxy.py:162` | `def test_username_password_without_credentials(self)` |
| `test_valid_config_passes` | method | `tests/test_socks_proxy.py:120` | `def test_valid_config_passes(self)` |
| `test_validate_custom_config` | method | `tests/test_socks_proxy.py:352` | `def test_validate_custom_config(self)` |
| `test_validate_request_denied_port_ac` | method | `tests/test_socks_proxy.py:233` | `def test_validate_request_denied_port_ac(self, tmp_path)` |
| `test_validate_request_invalid_port` | method | `tests/test_socks_proxy.py:223` | `def test_validate_request_invalid_port(self)` |
| `test_validate_request_unsupported_address_type` | method | `tests/test_socks_proxy.py:212` | `def test_validate_request_unsupported_address_type(self)` |
| `test_validate_request_unsupported_command` | method | `tests/test_socks_proxy.py:201` | `def test_validate_request_unsupported_command(self)` |
| `test_validate_request_valid_connect` | method | `tests/test_socks_proxy.py:190` | `def test_validate_request_valid_connect(self)` |
| `_write_operators` | function | `tests/test_status_bar_operators.py:28` | `def _write_operators(tmp_path, records)` |
| `test_build_default_manager_skips_operators_by_default` | function | `tests/test_status_bar_operators.py:86` | `def test_build_default_manager_skips_operators_by_default(tmp_path)` |
| `test_build_default_manager_wires_operators_when_enabled` | function | `tests/test_status_bar_operators.py:92` | `def test_build_default_manager_wires_operators_when_enabled(tmp_path)` |
| `test_collab_presence_counts_active_operators` | function | `tests/test_status_bar_operators.py:41` | `def test_collab_presence_counts_active_operators(tmp_path)` |
| `test_collab_presence_zero_when_file_missing` | function | `tests/test_status_bar_operators.py:33` | `def test_collab_presence_zero_when_file_missing(tmp_path)` |
| `test_render_prompt_switches_colour_with_tui_theme` | function | `tests/test_status_bar_operators.py:107` | `def test_render_prompt_switches_colour_with_tui_theme(tmp_path)` |
| `test_render_prompt_uses_default_theme_when_unspecified` | function | `tests/test_status_bar_operators.py:99` | `def test_render_prompt_uses_default_theme_when_unspecified(tmp_path)` |
| `test_renderer_switches_to_ops_format_when_present` | function | `tests/test_status_bar_operators.py:70` | `def test_renderer_switches_to_ops_format_when_present()` |
| `test_renderer_uses_default_format_when_operators_empty` | function | `tests/test_status_bar_operators.py:59` | `def test_renderer_uses_default_format_when_operators_empty()` |
| `TestGetLogger` | class | `tests/test_structured_logging.py:144` | `class TestGetLogger` |
| `TestInstallJsonHandler` | class | `tests/test_structured_logging.py:220` | `class TestInstallJsonHandler` |
| `TestJsonLineFormatter` | class | `tests/test_structured_logging.py:47` | `class TestJsonLineFormatter` |
| `TestReconfigure` | class | `tests/test_structured_logging.py:193` | `class TestReconfigure` |
| `TestStructuredLogConfig` | class | `tests/test_structured_logging.py:13` | `class TestStructuredLogConfig` |
| `TestStructuredLogger` | class | `tests/test_structured_logging.py:122` | `class TestStructuredLogger` |
| `test_cold_logger_gets_console_and_file_wiring` | method | `tests/test_structured_logging.py:223` | `def test_cold_logger_gets_console_and_file_wiring(self, tmp_path)` |
| `test_custom_override_preserves_other_defaults` | method | `tests/test_structured_logging.py:29` | `def test_custom_override_preserves_other_defaults(self)` |
| `test_defaults_are_production_ready` | method | `tests/test_structured_logging.py:16` | `def test_defaults_are_production_ready(self)` |
| `test_first_call_creates_and_configures_logger` | method | `tests/test_structured_logging.py:147` | `def test_first_call_creates_and_configures_logger(self)` |
| `test_formats_record_as_valid_json_line` | method | `tests/test_structured_logging.py:50` | `def test_formats_record_as_valid_json_line(self)` |
| `test_includes_exception_traceback_when_present` | method | `tests/test_structured_logging.py:98` | `def test_includes_exception_traceback_when_present(self)` |
| `test_make_records_promote_extra_fields_onto_record` | method | `tests/test_structured_logging.py:125` | `def test_make_records_promote_extra_fields_onto_record(self)` |
| `test_reconfigure_resets_cache_and_applies_new_config` | method | `tests/test_structured_logging.py:196` | `def test_reconfigure_resets_cache_and_applies_new_config(self, tmp_path)` |
| `test_redacts_sensitive_extra_fields` | method | `tests/test_structured_logging.py:74` | `def test_redacts_sensitive_extra_fields(self)` |
| `test_same_name_returns_cached_instance` | method | `tests/test_structured_logging.py:156` | `def test_same_name_returns_cached_instance(self)` |
| `test_second_install_is_idempotent` | method | `tests/test_structured_logging.py:260` | `def test_second_install_is_idempotent(self, tmp_path)` |
| `test_warm_logger_keeps_custom_handler_and_appends_json_file` | method | `tests/test_structured_logging.py:241` | `def test_warm_logger_keeps_custom_handler_and_appends_json_file(self, tmp_path)` |
| `test_writes_json_lines_to_file` | method | `tests/test_structured_logging.py:166` | `def test_writes_json_lines_to_file(self, tmp_path)` |
| `_build` | function | `tests/test_surface_graph.py:74` | `def _build(tmp_path, sessions)` |
| `_write_implant_log` | function | `tests/test_surface_graph.py:53` | `def _write_implant_log(path)` |
| `_write_payload` | function | `tests/test_surface_graph.py:62` | `def _write_payload(tmp_path)` |
| `sessions_dir` | function | `tests/test_surface_graph.py:80` | `def sessions_dir(tmp_path)` |
| `test_build_surface_graph_factory_works_without_payload_file` | function | `tests/test_surface_graph.py:210` | `def test_build_surface_graph_factory_works_without_payload_file(tmp_path, sessions_dir)` |
| `test_empty_sessions_still_produce_c2_root` | function | `tests/test_surface_graph.py:86` | `def test_empty_sessions_still_produce_c2_root(tmp_path, sessions_dir)` |
| `test_hostsdiscovery_populates_host_nodes` | function | `tests/test_surface_graph.py:95` | `def test_hostsdiscovery_populates_host_nodes(tmp_path, sessions_dir)` |
| `test_implant_log_creates_client_and_links_hosts` | function | `tests/test_surface_graph.py:137` | `def test_implant_log_creates_client_and_links_hosts(tmp_path, sessions_dir)` |
| `test_invalid_portscan_blob_does_not_crash` | function | `tests/test_surface_graph.py:218` | `def test_invalid_portscan_blob_does_not_crash(tmp_path, sessions_dir)` |
| `test_iter_descendants_walks_only_outgoing_edges` | function | `tests/test_surface_graph.py:200` | `def test_iter_descendants_walks_only_outgoing_edges(tmp_path, sessions_dir)` |
| `test_non_implant_logs_are_ignored` | function | `tests/test_surface_graph.py:180` | `def test_non_implant_logs_are_ignored(tmp_path, sessions_dir)` |
| `test_scan_discovery_csv_adds_ports_and_services` | function | `tests/test_surface_graph.py:112` | `def test_scan_discovery_csv_adds_ports_and_services(tmp_path, sessions_dir)` |
| `test_to_dict_round_trips_through_json` | function | `tests/test_surface_graph.py:189` | `def test_to_dict_round_trips_through_json(tmp_path, sessions_dir)` |
| `_load_module` | function | `tests/test_sync_doc_stats.py:20` | `def _load_module()` |
| `mod` | function | `tests/test_sync_doc_stats.py:28` | `def mod()` |
| `test_canonical_command_count_reads_index` | function | `tests/test_sync_doc_stats.py:32` | `def test_canonical_command_count_reads_index(mod, tmp_path)` |
| `test_measure_stats_command_count_matches_index` | function | `tests/test_sync_doc_stats.py:39` | `def test_measure_stats_command_count_matches_index(mod, tmp_path)` |
| `test_render_formats_template` | function | `tests/test_sync_doc_stats.py:92` | `def test_render_formats_template(mod)` |
| `test_sync_apply_rewrites_when_stale` | function | `tests/test_sync_doc_stats.py:80` | `def test_sync_apply_rewrites_when_stale(mod, tmp_path)` |
| `test_sync_check_does_not_write` | function | `tests/test_sync_doc_stats.py:67` | `def test_sync_check_does_not_write(mod, tmp_path)` |
| `test_get_theme_is_case_insensitive` | function | `tests/test_themes.py:35` | `def test_get_theme_is_case_insensitive()` |
| `test_get_theme_returns_default_for_unknown_name` | function | `tests/test_themes.py:30` | `def test_get_theme_returns_default_for_unknown_name()` |
| `test_theme_dataclass_is_immutable` | function | `tests/test_themes.py:51` | `def test_theme_dataclass_is_immutable()` |
| `test_theme_from_payload_none_yields_default` | function | `tests/test_themes.py:40` | `def test_theme_from_payload_none_yields_default()` |
| `test_theme_from_payload_picks_named_theme` | function | `tests/test_themes.py:45` | `def test_theme_from_payload_picks_named_theme()` |
| `test_themes_registry_contains_required_entries` | function | `tests/test_themes.py:24` | `def test_themes_registry_contains_required_entries()` |
| `_write_report` | function | `tests/test_timeline_browser.py:24` | `def _write_report(path, rows)` |
| `test_column_value_falls_back_through_source_keys` | function | `tests/test_timeline_browser.py:92` | `def test_column_value_falls_back_through_source_keys(tmp_path)` |
| `test_reader_parses_rows` | function | `tests/test_timeline_browser.py:40` | `def test_reader_parses_rows(tmp_path)` |
| `test_reader_returns_empty_when_csv_missing` | function | `tests/test_timeline_browser.py:34` | `def test_reader_returns_empty_when_csv_missing(tmp_path)` |
| `test_reader_truncates_long_field_values` | function | `tests/test_timeline_browser.py:113` | `def test_reader_truncates_long_field_values(tmp_path)` |
| `test_state_filter_empty_returns_all` | function | `tests/test_timeline_browser.py:84` | `def test_state_filter_empty_returns_all(tmp_path)` |
| `test_state_filters_across_columns` | function | `tests/test_timeline_browser.py:67` | `def test_state_filters_across_columns(tmp_path)` |
| `test_state_reload_drops_cache` | function | `tests/test_timeline_browser.py:102` | `def test_state_reload_drops_cache(tmp_path)` |
| `TestBuildDefaultConfig` | class | `tests/test_tips_engine.py:396` | `class TestBuildDefaultConfig` |
| `TestChainActiveSuppression` | class | `tests/test_tips_engine.py:152` | `class TestChainActiveSuppression` |
| `TestCommandNameRegex` | class | `tests/test_tips_engine.py:357` | `class TestCommandNameRegex` |
| `TestCommandsSeenSanitisation` | class | `tests/test_tips_engine.py:318` | `class TestCommandsSeenSanitisation` |
| `TestELOScoring` | class | `tests/test_tips_engine.py:280` | `class TestELOScoring` |
| `TestEngagementState` | class | `tests/test_tips_engine.py:104` | `class TestEngagementState` |
| `TestHintsLevelGating` | class | `tests/test_tips_engine.py:200` | `class TestHintsLevelGating` |
| `TestKarmaNames` | class | `tests/test_tips_engine.py:385` | `class TestKarmaNames` |
| `TestKillChainHints` | class | `tests/test_tips_engine.py:138` | `class TestKillChainHints` |
| `TestSkipCommands` | class | `tests/test_tips_engine.py:342` | `class TestSkipCommands` |
| `TestTipsConfig` | class | `tests/test_tips_engine.py:77` | `class TestTipsConfig` |
| `TestTipsEngineConstruction` | class | `tests/test_tips_engine.py:119` | `class TestTipsEngineConstruction` |
| `TestTruncate` | class | `tests/test_tips_engine.py:373` | `class TestTruncate` |
| `TestVRIThresholds` | class | `tests/test_tips_engine.py:305` | `class TestVRIThresholds` |
| `_render_with_surfaces_stubbed` | method | `tests/test_tips_engine.py:153` | `def _render_with_surfaces_stubbed(self, engine)` |
| `_stub_surfaces` | method | `tests/test_tips_engine.py:201` | `def _stub_surfaces(self, engine)` |
| `config` | function | `tests/test_tips_engine.py:48` | `def config()` |
| `engine` | function | `tests/test_tips_engine.py:70` | `def engine(config, tmp_sessions)` |
| `record` | function | `tests/test_tips_engine.py:165` | `def record()` |
| `record` | function | `tests/test_tips_engine.py:212` | `def record()` |
| `stub` | function | `tests/test_tips_engine.py:164` | `def stub(name)` |
| `stub` | function | `tests/test_tips_engine.py:211` | `def stub(name)` |
| `test_auto_pwn_not_skipped` | method | `tests/test_tips_engine.py:353` | `def test_auto_pwn_not_skipped(self)` |
| `test_auto_pwn_suggests_hunt` | method | `tests/test_tips_engine.py:147` | `def test_auto_pwn_suggests_hunt(self, engine)` |
| `test_badges_field_defaults_to_list` | method | `tests/test_tips_engine.py:113` | `def test_badges_field_defaults_to_list(self)` |
| `test_base_elo_awarded` | method | `tests/test_tips_engine.py:281` | `def test_base_elo_awarded(self, engine)` |
| `test_build_default_tips_config_populates_tables` | method | `tests/test_tips_engine.py:86` | `def test_build_default_tips_config_populates_tables(self)` |
| `test_chain_active_suppresses_competing_suggestion_surfaces` | method | `tests/test_tips_engine.py:179` | `def test_chain_active_suppresses_competing_suggestion_surfaces(self, engine)` |
| `test_chain_inactive_keeps_all_surfaces` | method | `tests/test_tips_engine.py:190` | `def test_chain_inactive_keeps_all_surfaces(self, engine)` |
| `test_config_has_high_value_for_new_commands` | method | `tests/test_tips_engine.py:410` | `def test_config_has_high_value_for_new_commands(self)` |
| `test_config_has_session_tips` | method | `tests/test_tips_engine.py:417` | `def test_config_has_session_tips(self)` |
| `test_config_includes_automation_commands` | method | `tests/test_tips_engine.py:397` | `def test_config_includes_automation_commands(self)` |
| `test_default_config_has_sensible_values` | method | `tests/test_tips_engine.py:78` | `def test_default_config_has_sensible_values(self)` |
| `test_default_config_is_on` | method | `tests/test_tips_engine.py:232` | `def test_default_config_is_on(self)` |
| `test_default_state` | method | `tests/test_tips_engine.py:105` | `def test_default_state(self)` |
| `test_empty_value` | method | `tests/test_tips_engine.py:381` | `def test_empty_value(self)` |
| `test_engine_can_disable` | method | `tests/test_tips_engine.py:125` | `def test_engine_can_disable(self, config)` |
| `test_engine_initialises_with_config` | method | `tests/test_tips_engine.py:120` | `def test_engine_initialises_with_config(self, config)` |
| `test_first_time_bonus` | method | `tests/test_tips_engine.py:289` | `def test_first_time_bonus(self, config)` |
| `test_get_hints_level_defaults_for_invalid` | method | `tests/test_tips_engine.py:275` | `def test_get_hints_level_defaults_for_invalid(self, engine)` |
| `test_get_hints_level_reads_config` | method | `tests/test_tips_engine.py:271` | `def test_get_hints_level_reads_config(self, engine)` |
| `test_godlike_above_6000` | method | `tests/test_tips_engine.py:392` | `def test_godlike_above_6000(self)` |
| `test_high_value_command_bonus` | method | `tests/test_tips_engine.py:285` | `def test_high_value_command_bonus(self, engine)` |
| `test_hints_level_constants` | method | `tests/test_tips_engine.py:225` | `def test_hints_level_constants(self)` |
| `test_invalid_command_names` | method | `tests/test_tips_engine.py:365` | `def test_invalid_command_names(self)` |
| `test_invalid_entries_dropped` | method | `tests/test_tips_engine.py:325` | `def test_invalid_entries_dropped(self)` |
| `test_invalid_level_falls_back_to_on` | method | `tests/test_tips_engine.py:264` | `def test_invalid_level_falls_back_to_on(self, engine)` |
| `test_known_filter_drops_unknown` | method | `tests/test_tips_engine.py:332` | `def test_known_filter_drops_unknown(self)` |
| `test_lazynmap_suggests_auto_pwn` | method | `tests/test_tips_engine.py:143` | `def test_lazynmap_suggests_auto_pwn(self, engine)` |
| `test_long_value_truncated` | method | `tests/test_tips_engine.py:377` | `def test_long_value_truncated(self)` |
| `test_minimal_runs_autosuggest_only` | method | `tests/test_tips_engine.py:245` | `def test_minimal_runs_autosuggest_only(self, engine)` |
| `test_new_phase_bonus` | method | `tests/test_tips_engine.py:294` | `def test_new_phase_bonus(self, config)` |
| `test_next_threshold_increases` | method | `tests/test_tips_engine.py:306` | `def test_next_threshold_increases(self, engine)` |
| `test_next_threshold_never_less_than_two` | method | `tests/test_tips_engine.py:312` | `def test_next_threshold_never_less_than_two(self, engine)` |
| `test_no_double_count_first_time_plus_new_phase` | method | `tests/test_tips_engine.py:299` | `def test_no_double_count_first_time_plus_new_phase(self, config)` |
| `test_noob_at_zero` | method | `tests/test_tips_engine.py:386` | `def test_noob_at_zero(self)` |
| `test_off_suppresses_all_surfaces` | method | `tests/test_tips_engine.py:235` | `def test_off_suppresses_all_surfaces(self, engine)` |
| `test_on_runs_every_surface` | method | `tests/test_tips_engine.py:255` | `def test_on_runs_every_surface(self, engine)` |
| `test_ping_not_skipped` | method | `tests/test_tips_engine.py:350` | `def test_ping_not_skipped(self)` |
| `test_ping_suggests_lazynmap` | method | `tests/test_tips_engine.py:139` | `def test_ping_suggests_lazynmap(self, engine)` |
| `test_render_skips_disabled_engine` | method | `tests/test_tips_engine.py:130` | `def test_render_skips_disabled_engine(self, config, capsys)` |
| `test_rookie_at_thousand` | method | `tests/test_tips_engine.py:389` | `def test_rookie_at_thousand(self)` |
| `test_short_value_untouched` | method | `tests/test_tips_engine.py:374` | `def test_short_value_untouched(self)` |
| `test_skip_set_contains_common_noise` | method | `tests/test_tips_engine.py:343` | `def test_skip_set_contains_common_noise(self)` |
| `test_valid_command_names` | method | `tests/test_tips_engine.py:358` | `def test_valid_command_names(self)` |
| `test_valid_commands_kept` | method | `tests/test_tips_engine.py:319` | `def test_valid_commands_kept(self)` |
| `tmp_sessions` | function | `tests/test_tips_engine.py:39` | `def tmp_sessions()` |
| `_append_jsonl` | function | `tests/test_toast_bus.py:42` | `def _append_jsonl(path, records)` |
| `_toast_event` | function | `tests/test_toast_bus.py:199` | `def _toast_event(kind, severity, summary)` |
| `_write_jsonl` | function | `tests/test_toast_bus.py:34` | `def _write_jsonl(path, records)` |
| `test_build_default_bus_honours_budget` | function | `tests/test_toast_bus.py:175` | `def test_build_default_bus_honours_budget(tmp_path)` |
| `test_bus_mark_all_seen_consumes_pending` | function | `tests/test_toast_bus.py:140` | `def test_bus_mark_all_seen_consumes_pending(tmp_path)` |
| `test_bus_render_disabled_returns_zero` | function | `tests/test_toast_bus.py:127` | `def test_bus_render_disabled_returns_zero(tmp_path)` |
| `test_bus_render_respects_per_tick_budget` | function | `tests/test_toast_bus.py:109` | `def test_bus_render_respects_per_tick_budget(tmp_path)` |
| `test_formatter_uses_theme_role_for_severity` | function | `tests/test_toast_bus.py:91` | `def test_formatter_uses_theme_role_for_severity()` |
| `test_over_budget_events_collapse_into_digest` | function | `tests/test_toast_bus.py:242` | `def test_over_budget_events_collapse_into_digest()` |
| `test_prominent_completion_renders_full_text` | function | `tests/test_toast_bus.py:211` | `def test_prominent_completion_renders_full_text()` |
| `test_prominent_severity_renders_panel` | function | `tests/test_toast_bus.py:229` | `def test_prominent_severity_renders_panel()` |
| `test_reader_handles_malformed_lines` | function | `tests/test_toast_bus.py:80` | `def test_reader_handles_malformed_lines(tmp_path)` |
| `test_reader_picks_up_new_events_after_offset` | function | `tests/test_toast_bus.py:187` | `def test_reader_picks_up_new_events_after_offset(tmp_path)` |
| `test_reader_returns_unseen_events_only` | function | `tests/test_toast_bus.py:67` | `def test_reader_returns_unseen_events_only(tmp_path)` |
| `test_render_toasts_returns_count` | function | `tests/test_toast_bus.py:165` | `def test_render_toasts_returns_count(tmp_path)` |
| `test_state_clamps_negative_offsets` | function | `tests/test_toast_bus.py:59` | `def test_state_clamps_negative_offsets(tmp_path)` |
| `test_state_round_trip` | function | `tests/test_toast_bus.py:49` | `def test_state_round_trip(tmp_path)` |
| `test_toasts_enabled_default_true` | function | `tests/test_toast_bus.py:157` | `def test_toasts_enabled_default_true()` |
| `_SpyConsole` | class | `tests/test_toastr_unify.py:73` | `class _SpyConsole` |
| `__init__` | method | `tests/test_toastr_unify.py:76` | `def __init__(self)` |
| `print` | method | `tests/test_toastr_unify.py:79` | `def print(self, message, style)` |
| `test_empty_message_falls_back_like_legacy` | function | `tests/test_toastr_unify.py:45` | `def test_empty_message_falls_back_like_legacy()` |
| `test_markup_is_escaped_for_plain_text` | function | `tests/test_toastr_unify.py:51` | `def test_markup_is_escaped_for_plain_text()` |
| `test_plain_text_message_wraps_and_adapts` | function | `tests/test_toastr_unify.py:35` | `def test_plain_text_message_wraps_and_adapts()` |
| `test_sentinel_panel_keeps_field_layout` | function | `tests/test_toastr_unify.py:57` | `def test_sentinel_panel_keeps_field_layout()` |
| `test_sentinel_severity_selects_border` | function | `tests/test_toastr_unify.py:67` | `def test_sentinel_severity_selects_border()` |
| `test_severity_table_covers_every_surface_level` | function | `tests/test_toastr_unify.py:22` | `def test_severity_table_covers_every_surface_level()` |
| `test_shell_hint_bypass_keeps_empty_fallback` | function | `tests/test_toastr_unify.py:91` | `def test_shell_hint_bypass_keeps_empty_fallback()` |
| `test_shell_hint_bypass_prints_flat_line` | function | `tests/test_toastr_unify.py:84` | `def test_shell_hint_bypass_prints_flat_line()` |
| `test_unknown_severity_falls_back_to_info` | function | `tests/test_toastr_unify.py:30` | `def test_unknown_severity_falls_back_to_info()` |
| `test_orchestrator_yaml_declares_trigger_seeds` | function | `tests/test_trigger_policy.py:82` | `def test_orchestrator_yaml_declares_trigger_seeds()` |
| `test_seed_store_drops_unknown_kinds` | function | `tests/test_trigger_policy.py:89` | `def test_seed_store_drops_unknown_kinds(tmp_path, monkeypatch)` |
| `test_seed_store_is_idempotent` | function | `tests/test_trigger_policy.py:48` | `def test_seed_store_is_idempotent(tmp_path, monkeypatch)` |
| `test_seed_store_keeps_runtime_triggers` | function | `tests/test_trigger_policy.py:66` | `def test_seed_store_keeps_runtime_triggers(tmp_path, monkeypatch)` |
| `test_seeds_coerce_and_skip_unknown_kinds` | function | `tests/test_trigger_policy.py:26` | `def test_seeds_coerce_and_skip_unknown_kinds()` |
| `test_validate_policy_rejects_bad_documents` | function | `tests/test_trigger_policy.py:18` | `def test_validate_policy_rejects_bad_documents()` |
| `test_yaml_seeds_read_from_orchestrator_document` | function | `tests/test_trigger_policy.py:40` | `def test_yaml_seeds_read_from_orchestrator_document()` |
| `TestIsOperator` | class | `tests/test_trusted_proxy.py:99` | `class TestIsOperator` |
| `TestNoProxy` | class | `tests/test_trusted_proxy.py:22` | `class TestNoProxy` |
| `TestTrustedProxy` | class | `tests/test_trusted_proxy.py:43` | `class TestTrustedProxy` |
| `test_empty_header_falls_back` | method | `tests/test_trusted_proxy.py:85` | `def test_empty_header_falls_back(self)` |
| `test_insufficient_chain_falls_back` | method | `tests/test_trusted_proxy.py:72` | `def test_insufficient_chain_falls_back(self)` |
| `test_match` | method | `tests/test_trusted_proxy.py:102` | `def test_match(self)` |
| `test_no_header_falls_back_to_remote` | method | `tests/test_trusted_proxy.py:38` | `def test_no_header_falls_back_to_remote(self)` |
| `test_no_match` | method | `tests/test_trusted_proxy.py:109` | `def test_no_match(self)` |
| `test_remote_addr_returned` | method | `tests/test_trusted_proxy.py:25` | `def test_remote_addr_returned(self)` |
| `test_single_proxy_returns_leftmost` | method | `tests/test_trusted_proxy.py:46` | `def test_single_proxy_returns_leftmost(self)` |
| `test_two_proxies_returns_leftmost` | method | `tests/test_trusted_proxy.py:59` | `def test_two_proxies_returns_leftmost(self)` |
| `test_addon_schema_agent_friendly` | function | `tests/test_ttpscope_bridge.py:95` | `def test_addon_schema_agent_friendly()` |
| `test_chain_needs_no_binary` | function | `tests/test_ttpscope_bridge.py:85` | `def test_chain_needs_no_binary(monkeypatch)` |
| `test_matrix_fallback_groups` | function | `tests/test_ttpscope_bridge.py:65` | `def test_matrix_fallback_groups(monkeypatch)` |
| `test_notes_roundtrip_without_binary` | function | `tests/test_ttpscope_bridge.py:73` | `def test_notes_roundtrip_without_binary(monkeypatch, tmp_path)` |
| `test_object_id_validation` | function | `tests/test_ttpscope_bridge.py:18` | `def test_object_id_validation()` |
| `test_query_and_platform_validation` | function | `tests/test_ttpscope_bridge.py:27` | `def test_query_and_platform_validation()` |
| `test_search_fallback_needs_no_binary` | function | `tests/test_ttpscope_bridge.py:48` | `def test_search_fallback_needs_no_binary(monkeypatch)` |
| `test_show_fallback_technique` | function | `tests/test_ttpscope_bridge.py:56` | `def test_show_fallback_technique(monkeypatch)` |
| `test_unknown_action_rejected` | function | `tests/test_ttpscope_bridge.py:40` | `def test_unknown_action_rejected()` |
| `SplashDispatchTests` | class | `tests/test_tui_splash.py:81` | `class SplashDispatchTests(TestCase)` |
| `SplashEdgeCaseTests` | class | `tests/test_tui_splash.py:145` | `class SplashEdgeCaseTests(TestCase)` |
| `SplashInstantEffectTests` | class | `tests/test_tui_splash.py:30` | `class SplashInstantEffectTests(TestCase)` |
| `SplashTypewriterEffectTests` | class | `tests/test_tui_splash.py:67` | `class SplashTypewriterEffectTests(TestCase)` |
| `_console` | function | `tests/test_tui_splash.py:19` | `def _console()` |
| `test_empty_lines_is_noop` | method | `tests/test_tui_splash.py:146` | `def test_empty_lines_is_noop(self)` |
| `test_instant_does_not_block` | method | `tests/test_tui_splash.py:44` | `def test_instant_does_not_block(self)` |
| `test_instant_emits_ansi_for_known_tokens` | method | `tests/test_tui_splash.py:56` | `def test_instant_emits_ansi_for_known_tokens(self)` |
| `test_instant_renders_every_line` | method | `tests/test_tui_splash.py:31` | `def test_instant_renders_every_line(self)` |
| `test_lines_with_brackets_render_verbatim` | method | `tests/test_tui_splash.py:156` | `def test_lines_with_brackets_render_verbatim(self)` |
| `test_render_splash_clear_after_emits_clear_escape` | method | `tests/test_tui_splash.py:124` | `def test_render_splash_clear_after_emits_clear_escape(self)` |
| `test_render_splash_dispatches_instant_for_zero_seconds` | method | `tests/test_tui_splash.py:82` | `def test_render_splash_dispatches_instant_for_zero_seconds(self)` |
| `test_render_splash_dispatches_instant_when_explicit` | method | `tests/test_tui_splash.py:92` | `def test_render_splash_dispatches_instant_when_explicit(self)` |
| `test_render_splash_no_clear_when_disabled` | method | `tests/test_tui_splash.py:134` | `def test_render_splash_no_clear_when_disabled(self)` |
| `test_render_splash_unknown_effect_falls_back_to_instant` | method | `tests/test_tui_splash.py:103` | `def test_render_splash_unknown_effect_falls_back_to_instant(self)` |
| `test_render_splash_uses_payload_theme_when_provided` | method | `tests/test_tui_splash.py:114` | `def test_render_splash_uses_payload_theme_when_provided(self)` |
| `test_typewriter_renders_all_lines_when_total_seconds_high` | method | `tests/test_tui_splash.py:68` | `def test_typewriter_renders_all_lines_when_total_seconds_high(self)` |
| `StyleTokenTests` | class | `tests/test_tui_style.py:14` | `class StyleTokenTests(TestCase)` |
| `test_active_tokens_covers_every_key` | method | `tests/test_tui_style.py:25` | `def test_active_tokens_covers_every_key(self)` |
| `test_active_tokens_honours_payload` | method | `tests/test_tui_style.py:32` | `def test_active_tokens_honours_payload(self)` |
| `test_known_token_returns_theme_attribute` | method | `tests/test_tui_style.py:15` | `def test_known_token_returns_theme_attribute(self)` |
| `test_paint_returns_rich_text_with_style` | method | `tests/test_tui_style.py:39` | `def test_paint_returns_rich_text_with_style(self)` |
| `test_render_prompt_emits_segments_separated_by_bar` | method | `tests/test_tui_style.py:44` | `def test_render_prompt_emits_segments_separated_by_bar(self)` |
| `test_render_prompt_empty_is_noop` | method | `tests/test_tui_style.py:59` | `def test_render_prompt_empty_is_noop(self)` |
| `test_unknown_token_falls_back_to_white` | method | `tests/test_tui_style.py:21` | `def test_unknown_token_falls_back_to_white(self)` |
| `RecordingSave` | class | `tests/test_tui_theme_command.py:11` | `class RecordingSave` |
| `TuiThemeCycleTests` | class | `tests/test_tui_theme_command.py:78` | `class TuiThemeCycleTests(TestCase)` |
| `TuiThemeListingTests` | class | `tests/test_tui_theme_command.py:28` | `class TuiThemeListingTests(TestCase)` |
| `TuiThemeRegistrationConsistencyTests` | class | `tests/test_tui_theme_command.py:105` | `class TuiThemeRegistrationConsistencyTests(TestCase)` |
| `TuiThemeSwitchTests` | class | `tests/test_tui_theme_command.py:46` | `class TuiThemeSwitchTests(TestCase)` |
| `__call__` | method | `tests/test_tui_theme_command.py:17` | `def __call__(self, payload)` |
| `__init__` | method | `tests/test_tui_theme_command.py:14` | `def __init__(self)` |
| `_payload` | function | `tests/test_tui_theme_command.py:21` | `def _payload()` |
| `test_case_insensitive_lookup` | method | `tests/test_tui_theme_command.py:63` | `def test_case_insensitive_lookup(self)` |
| `test_cycle_advances_in_theme_order` | method | `tests/test_tui_theme_command.py:79` | `def test_cycle_advances_in_theme_order(self)` |
| `test_cycle_wraps_around` | method | `tests/test_tui_theme_command.py:87` | `def test_cycle_wraps_around(self)` |
| `test_empty_args_lists_every_registered_theme` | method | `tests/test_tui_theme_command.py:29` | `def test_empty_args_lists_every_registered_theme(self)` |
| `test_known_name_switches_and_persists` | method | `tests/test_tui_theme_command.py:47` | `def test_known_name_switches_and_persists(self)` |
| `test_listing_marks_current_theme` | method | `tests/test_tui_theme_command.py:38` | `def test_listing_marks_current_theme(self)` |
| `test_prev_walks_backwards_and_wraps` | method | `tests/test_tui_theme_command.py:94` | `def test_prev_walks_backwards_and_wraps(self)` |
| `test_reset_returns_to_default` | method | `tests/test_tui_theme_command.py:70` | `def test_reset_returns_to_default(self)` |
| `test_theme_order_covers_every_registered_theme` | method | `tests/test_tui_theme_command.py:106` | `def test_theme_order_covers_every_registered_theme(self)` |
| `test_theme_order_has_no_duplicates` | method | `tests/test_tui_theme_command.py:109` | `def test_theme_order_has_no_duplicates(self)` |
| `test_unknown_name_does_not_mutate` | method | `tests/test_tui_theme_command.py:55` | `def test_unknown_name_does_not_mutate(self)` |
| `NewThemeRegistrationTests` | class | `tests/test_tui_themes.py:39` | `class NewThemeRegistrationTests(TestCase)` |
| `NewThemeRenderTests` | class | `tests/test_tui_themes.py:86` | `class NewThemeRenderTests(TestCase)` |
| `ThemeOrderTests` | class | `tests/test_tui_themes.py:130` | `class ThemeOrderTests(TestCase)` |
| `test_every_new_theme_is_registered` | method | `tests/test_tui_themes.py:40` | `def test_every_new_theme_is_registered(self)` |
| `test_every_token_renders_with_ansi_escapes` | method | `tests/test_tui_themes.py:95` | `def test_every_token_renders_with_ansi_escapes(self)` |
| `test_every_token_renders_with_ansi_escapes_in_256color` | method | `tests/test_tui_themes.py:112` | `def test_every_token_renders_with_ansi_escapes_in_256color(self)` |
| `test_get_theme_resolves_every_new_name` | method | `tests/test_tui_themes.py:50` | `def test_get_theme_resolves_every_new_name(self)` |
| `test_get_theme_uses_case_insensitive_lookup` | method | `tests/test_tui_themes.py:55` | `def test_get_theme_uses_case_insensitive_lookup(self)` |
| `test_new_themes_have_non_empty_token_values` | method | `tests/test_tui_themes.py:76` | `def test_new_themes_have_non_empty_token_values(self)` |
| `test_new_themes_have_unique_color_palettes` | method | `tests/test_tui_themes.py:72` | `def test_new_themes_have_unique_color_palettes(self)` |
| `test_order_covers_every_registered_theme_exactly_once` | method | `tests/test_tui_themes.py:131` | `def test_order_covers_every_registered_theme_exactly_once(self)` |
| `test_order_is_reexported_by_tui_theme_command` | method | `tests/test_tui_themes.py:135` | `def test_order_is_reexported_by_tui_theme_command(self)` |
| `test_original_themes_remain_registered` | method | `tests/test_tui_themes.py:45` | `def test_original_themes_remain_registered(self)` |
| `test_theme_from_payload_picks_each_new_theme` | method | `tests/test_tui_themes.py:64` | `def test_theme_from_payload_picks_each_new_theme(self)` |
| `test_unknown_name_falls_back_to_default` | method | `tests/test_tui_themes.py:59` | `def test_unknown_name_falls_back_to_default(self)` |
| `_patch_bridge_api` | function | `tests/test_unified_bridge_delegate.py:25` | `def _patch_bridge_api(monkeypatch, statuses, result)` |
| `boom` | function | `tests/test_unified_bridge_delegate.py:90` | `def boom()` |
| `fake_start` | function | `tests/test_unified_bridge_delegate.py:30` | `def fake_start(goal, backend, runner, max_iterations)` |
| `test_delegate_polls_until_completion` | function | `tests/test_unified_bridge_delegate.py:40` | `def test_delegate_polls_until_completion(monkeypatch, unified_bridge)` |
| `test_delegate_reports_agent_failure` | function | `tests/test_unified_bridge_delegate.py:66` | `def test_delegate_reports_agent_failure(monkeypatch, unified_bridge)` |
| `test_delegate_surfaces_missing_agent` | function | `tests/test_unified_bridge_delegate.py:77` | `def test_delegate_surfaces_missing_agent(monkeypatch, unified_bridge)` |
| `test_delegate_times_out_when_agent_never_finishes` | function | `tests/test_unified_bridge_delegate.py:55` | `def test_delegate_times_out_when_agent_never_finishes(monkeypatch, unified_bridge)` |
| `test_delegate_wraps_start_errors` | function | `tests/test_unified_bridge_delegate.py:87` | `def test_delegate_wraps_start_errors(monkeypatch, unified_bridge)` |
| `unified_bridge` | function | `tests/test_unified_bridge_delegate.py:16` | `def unified_bridge(monkeypatch)` |
| `TestDaemonStatus` | class | `tests/test_unified_dashboard.py:36` | `class TestDaemonStatus` |
| `TestExportJson` | class | `tests/test_unified_dashboard.py:95` | `class TestExportJson` |
| `TestRenderUnified` | class | `tests/test_unified_dashboard.py:74` | `class TestRenderUnified` |
| `TestUnifiedDashboardInit` | class | `tests/test_unified_dashboard.py:10` | `class TestUnifiedDashboardInit` |
| `TestUnifiedSnapshot` | class | `tests/test_unified_dashboard.py:51` | `class TestUnifiedSnapshot` |
| `TestWorldModelCollection` | class | `tests/test_unified_dashboard.py:21` | `class TestWorldModelCollection` |
| `test_collect_daemon_status_exists` | method | `tests/test_unified_dashboard.py:37` | `def test_collect_daemon_status_exists(self, tmp_path)` |
| `test_collect_daemon_status_missing` | method | `tests/test_unified_dashboard.py:45` | `def test_collect_daemon_status_missing(self, tmp_path)` |
| `test_collect_world_model_exists` | method | `tests/test_unified_dashboard.py:22` | `def test_collect_world_model_exists(self, tmp_path)` |
| `test_collect_world_model_missing` | method | `tests/test_unified_dashboard.py:30` | `def test_collect_world_model_missing(self, tmp_path)` |
| `test_default_init` | method | `tests/test_unified_dashboard.py:11` | `def test_default_init(self, tmp_path)` |
| `test_export_json` | method | `tests/test_unified_dashboard.py:96` | `def test_export_json(self, tmp_path)` |
| `test_get_unified_dashboard_singleton` | method | `tests/test_unified_dashboard.py:15` | `def test_get_unified_dashboard_singleton(self, tmp_path)` |
| `test_render_contains_header` | method | `tests/test_unified_dashboard.py:75` | `def test_render_contains_header(self, tmp_path)` |
| `test_render_contains_sections` | method | `tests/test_unified_dashboard.py:80` | `def test_render_contains_sections(self, tmp_path)` |
| `test_render_contains_timestamp` | method | `tests/test_unified_dashboard.py:89` | `def test_render_contains_timestamp(self, tmp_path)` |
| `test_snapshot_keys` | method | `tests/test_unified_dashboard.py:52` | `def test_snapshot_keys(self, tmp_path)` |
| `test_snapshot_timestamp` | method | `tests/test_unified_dashboard.py:67` | `def test_snapshot_timestamp(self, tmp_path)` |
| `test_import_with_foreign_argv_is_silent` | function | `tests/test_utils_import_silent.py:12` | `def test_import_with_foreign_argv_is_silent()` |
| `test_lazy_import_chains_stay_silent` | function | `tests/test_utils_import_silent.py:34` | `def test_lazy_import_chains_stay_silent()` |
| `_addon_sandbox` | function | `tests/test_verb_catalog.py:150` | `def _addon_sandbox(tmp_path, enabled)` |
| `sandbox` | function | `tests/test_verb_catalog.py:19` | `def sandbox(tmp_path)` |
| `test_effective_verbs_include_catalog_entries` | function | `tests/test_verb_catalog.py:97` | `def test_effective_verbs_include_catalog_entries(sandbox, monkeypatch)` |
| `test_load_returns_empty_on_missing_invalid_or_oversize` | function | `tests/test_verb_catalog.py:64` | `def test_load_returns_empty_on_missing_invalid_or_oversize(sandbox, tmp_path)` |
| `test_loop_refuses_disabled_cli_verb_and_allows_enabled` | function | `tests/test_verb_catalog.py:111` | `def test_loop_refuses_disabled_cli_verb_and_allows_enabled(sandbox, monkeypatch)` |
| `test_operator_can_turn_addon_verb_on` | function | `tests/test_verb_catalog.py:202` | `def test_operator_can_turn_addon_verb_on(tmp_path)` |
| `test_search_filters_catalog` | function | `tests/test_verb_catalog.py:141` | `def test_search_filters_catalog(sandbox)` |
| `test_set_enabled_persists_atomically` | function | `tests/test_verb_catalog.py:79` | `def test_set_enabled_persists_atomically(sandbox)` |
| `test_set_enabled_unknown_command_raises` | function | `tests/test_verb_catalog.py:73` | `def test_set_enabled_unknown_command_raises(sandbox)` |
| `test_stats_reports_on_off_counts` | function | `tests/test_verb_catalog.py:133` | `def test_stats_reports_on_off_counts(sandbox)` |
| `test_steps_for_addon_verb_runs_lazy_addon` | function | `tests/test_verb_catalog.py:215` | `def test_steps_for_addon_verb_runs_lazy_addon(tmp_path, monkeypatch)` |
| `test_sync_generates_catalog_with_builtins_on_and_new_off` | function | `tests/test_verb_catalog.py:32` | `def test_sync_generates_catalog_with_builtins_on_and_new_off(sandbox)` |
| `test_sync_indexes_enabled_lazyaddons_disabled_by_default` | function | `tests/test_verb_catalog.py:169` | `def test_sync_indexes_enabled_lazyaddons_disabled_by_default(tmp_path)` |
| `test_sync_preserves_operator_choices` | function | `tests/test_verb_catalog.py:41` | `def test_sync_preserves_operator_choices(sandbox)` |
| `test_sync_prunes_renamed_or_disabled_addons` | function | `tests/test_verb_catalog.py:187` | `def test_sync_prunes_renamed_or_disabled_addons(tmp_path)` |
| `test_sync_prunes_stale_commands` | function | `tests/test_verb_catalog.py:51` | `def test_sync_prunes_stale_commands(sandbox)` |
| `test_validate_catalog_rejects_bad_documents` | function | `tests/test_verb_catalog.py:88` | `def test_validate_catalog_rejects_bad_documents(sandbox)` |
| `TestNoiseAndCost` | class | `tests/test_verb_manifest.py:118` | `class TestNoiseAndCost` |
| `TestPlanCheck` | class | `tests/test_verb_manifest.py:81` | `class TestPlanCheck` |
| `TestSchema` | class | `tests/test_verb_manifest.py:50` | `class TestSchema` |
| `manifest_path` | function | `tests/test_verb_manifest.py:14` | `def manifest_path(tmp_path)` |
| `test_cost_tolerates_junk` | method | `tests/test_verb_manifest.py:129` | `def test_cost_tolerates_junk(self)` |
| `test_effect_paid_forward` | method | `tests/test_verb_manifest.py:91` | `def test_effect_paid_forward(self, manifest_path)` |
| `test_fallback_when_store_empty` | method | `tests/test_verb_manifest.py:112` | `def test_fallback_when_store_empty(self, tmp_path)` |
| `test_noise_clamped` | method | `tests/test_verb_manifest.py:121` | `def test_noise_clamped(self)` |
| `test_parse_manifest_rejects_junk` | method | `tests/test_verb_manifest.py:73` | `def test_parse_manifest_rejects_junk(self)` |
| `test_unknown_fact_id_dropped` | method | `tests/test_verb_manifest.py:65` | `def test_unknown_fact_id_dropped(self, manifest_path)` |
| `test_unmet_precondition_reported` | method | `tests/test_verb_manifest.py:84` | `def test_unmet_precondition_reported(self, manifest_path)` |
| `test_valid_manifest_parses` | method | `tests/test_verb_manifest.py:53` | `def test_valid_manifest_parses(self, manifest_path)` |
| `test_world_model_facts_default` | method | `tests/test_verb_manifest.py:104` | `def test_world_model_facts_default(self)` |
| `test_demo_gif_commands_exist_in_source` | function | `tests/test_viral_adoption.py:23` | `def test_demo_gif_commands_exist_in_source()` |
| `test_demo_gifs_exist_and_nonempty` | function | `tests/test_viral_adoption.py:8` | `def test_demo_gifs_exist_and_nonempty()` |
| `test_docs_drift_workflow_exists` | function | `tests/test_viral_adoption.py:89` | `def test_docs_drift_workflow_exists()` |
| `test_launch_kit_exists` | function | `tests/test_viral_adoption.py:101` | `def test_launch_kit_exists()` |
| `test_marketplace_template_exists` | function | `tests/test_viral_adoption.py:95` | `def test_marketplace_template_exists()` |
| `test_readme_links_viral_assets` | function | `tests/test_viral_adoption.py:75` | `def test_readme_links_viral_assets()` |
| `test_smoke_script_covers_onboarding` | function | `tests/test_viral_adoption.py:83` | `def test_smoke_script_covers_onboarding()` |
| `MitigationSuiteConfig` | class | `tests/test_vuln_mitigations.py:29` | `class MitigationSuiteConfig` |
| `TestMitigationConfigInvariants` | class | `tests/test_vuln_mitigations.py:224` | `class TestMitigationConfigInvariants` |
| `TestSentinelRegexSafety` | class | `tests/test_vuln_mitigations.py:166` | `class TestSentinelRegexSafety` |
| `TestStackTraceSanitisation` | class | `tests/test_vuln_mitigations.py:89` | `class TestStackTraceSanitisation` |
| `_extract_sanitise_pattern` | method | `tests/test_vuln_mitigations.py:181` | `def _extract_sanitise_pattern(self, src)` |
| `_iter_function_bodies` | function | `tests/test_vuln_mitigations.py:77` | `def _iter_function_bodies(src)` |
| `_read_module` | function | `tests/test_vuln_mitigations.py:69` | `def _read_module(config, relative_path)` |
| `lazyc2_src` | method | `tests/test_vuln_mitigations.py:93` | `def lazyc2_src(self, mitigation_config)` |
| `mitigation_config` | function | `tests/test_vuln_mitigations.py:64` | `def mitigation_config()` |
| `phishingai_src` | method | `tests/test_vuln_mitigations.py:98` | `def phishingai_src(self, mitigation_config)` |
| `repo_root` | method | `tests/test_vuln_mitigations.py:58` | `def repo_root(self)` |
| `src` | method | `tests/test_vuln_mitigations.py:177` | `def src(self, mitigation_config)` |
| `test_dynamic_route_drops_raw_save_to_log_payload` | method | `tests/test_vuln_mitigations.py:140` | `def test_dynamic_route_drops_raw_save_to_log_payload(self, lazyc2_src)` |
| `test_handler_module_paths_exist` | method | `tests/test_vuln_mitigations.py:227` | `def test_handler_module_paths_exist(self, mitigation_config)` |
| `test_log_handler_keeps_server_side_logging` | method | `tests/test_vuln_mitigations.py:112` | `def test_log_handler_keeps_server_side_logging(self, lazyc2_src)` |

Next: [SYMBOLS_p44.md](SYMBOLS_p44.md)
