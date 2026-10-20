# Symbols (page 31 of 43)
Previous: [SYMBOLS_p30.md](SYMBOLS_p30.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `FakeStore` | class | `tests/test_apt_chain_admin.py:253` | `class FakeStore` |
| `_Set` | class | `tests/test_apt_chain_admin.py:27` | `class _Set(CommandAndControlMigratedCommandSet)` |
| `_Shell` | class | `tests/test_apt_chain_admin.py:30` | `class _Shell(Cmd)` |
| `__init__` | method | `tests/test_apt_chain_admin.py:33` | `def __init__(self)` |
| `__init__` | method | `tests/test_apt_chain_admin.py:256` | `def __init__(self)` |
| `_make_shell` | function | `tests/test_apt_chain_admin.py:23` | `def _make_shell()` |
| `_patch_chain_loading` | function | `tests/test_apt_chain_admin.py:49` | `def _patch_chain_loading(monkeypatch, tmp_path, enabled_name, chain)` |
| `_write_chain` | function | `tests/test_apt_chain_admin.py:41` | `def _write_chain(tmp_path, name, steps, enabled)` |
| `get_host` | method | `tests/test_apt_chain_admin.py:265` | `def get_host(host)` |
| `parse_all` | method | `tests/test_apt_chain_admin.py:260` | `def parse_all()` |
| `test_admin_list_validate_and_enable_disable` | function | `tests/test_apt_chain_admin.py:101` | `def test_admin_list_validate_and_enable_disable(tmp_path, monkeypatch, capsys)` |
| `test_admin_missing_chain_and_bad_input_fail` | function | `tests/test_apt_chain_admin.py:127` | `def test_admin_missing_chain_and_bad_input_fail(tmp_path, monkeypatch, capsys)` |
| `test_confirm_gate_auto_approves_in_autonomous_mode` | function | `tests/test_apt_chain_admin.py:200` | `def test_confirm_gate_auto_approves_in_autonomous_mode(tmp_path, monkeypatch, capsys)` |
| `test_confirm_gate_denies_when_operator_refuses` | function | `tests/test_apt_chain_admin.py:217` | `def test_confirm_gate_denies_when_operator_refuses(tmp_path, monkeypatch, capsys)` |
| `test_engagement_tokens_resolved_from_fact_store` | function | `tests/test_apt_chain_admin.py:233` | `def test_engagement_tokens_resolved_from_fact_store(monkeypatch, tmp_path)` |
| `test_parse_flags_and_unknown_flag_fails_loudly` | function | `tests/test_apt_chain_admin.py:59` | `def test_parse_flags_and_unknown_flag_fails_loudly()` |
| `test_playbook_overrides_base_chain` | function | `tests/test_apt_chain_admin.py:282` | `def test_playbook_overrides_base_chain(tmp_path, monkeypatch, capsys)` |
| `test_run_checkpoints_and_resume` | function | `tests/test_apt_chain_admin.py:157` | `def test_run_checkpoints_and_resume(tmp_path, monkeypatch, capsys)` |
| `test_run_dry_run_json_output` | function | `tests/test_apt_chain_admin.py:138` | `def test_run_dry_run_json_output(tmp_path, monkeypatch, capsys)` |
| `test_select_step_ids_supports_step_from_and_to` | function | `tests/test_apt_chain_admin.py:74` | `def test_select_step_ids_supports_step_from_and_to()` |
| `test_step_filtering_drops_out_of_scope_steps` | function | `tests/test_apt_chain_admin.py:295` | `def test_step_filtering_drops_out_of_scope_steps(tmp_path, monkeypatch, capsys)` |
| `test_unknown_run_flags_fail_loudly` | function | `tests/test_apt_chain_admin.py:318` | `def test_unknown_run_flags_fail_loudly(tmp_path, monkeypatch, capsys)` |
| `_Set` | class | `tests/test_apt_chain_integration.py:19` | `class _Set(CommandAndControlMigratedCommandSet)` |
| `_Shell` | class | `tests/test_apt_chain_integration.py:28` | `class _Shell(Cmd)` |
| `__init__` | method | `tests/test_apt_chain_integration.py:31` | `def __init__(self)` |
| `do_assign` | method | `tests/test_apt_chain_integration.py:37` | `def do_assign(self, line)` |
| `do_atomic_shell` | method | `tests/test_apt_chain_integration.py:22` | `def do_atomic_shell(self, line)` |
| `test_apt_chain_prints_raw_output_and_opens_shell_on_main_thread` | function | `tests/test_apt_chain_integration.py:42` | `def test_apt_chain_prints_raw_output_and_opens_shell_on_main_thread(tmp_path, monkeypatch, capsys)` |
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
| `_Done` | class | `tests/test_atomic_exploit_bridge.py:418` | `class _Done` |
| `_FakeCleanupSession` | class | `tests/test_atomic_exploit_bridge.py:356` | `class _FakeCleanupSession` |
| `__init__` | method | `tests/test_atomic_exploit_bridge.py:359` | `def __init__(self)` |
| `_counting_trigger` | function | `tests/test_atomic_exploit_bridge.py:342` | `def _counting_trigger()` |
| `_demo_spec` | function | `tests/test_atomic_exploit_bridge.py:258` | `def _demo_spec()` |
| `_fake` | function | `tests/test_atomic_exploit_bridge.py:284` | `def _fake(target_port, timeout)` |
| `_fake_input` | function | `tests/test_atomic_exploit_bridge.py:450` | `def _fake_input(prompt)` |
| `_fake_shell_peer` | function | `tests/test_atomic_exploit_bridge.py:211` | `def _fake_shell_peer(sock, reply)` |
| `_flaky_trigger` | function | `tests/test_atomic_exploit_bridge.py:306` | `def _flaky_trigger()` |
| `_missing` | function | `tests/test_atomic_exploit_bridge.py:412` | `def _missing()` |
| `_patch_connect` | function | `tests/test_atomic_exploit_bridge.py:276` | `def _patch_connect(monkeypatch, failures_before_success)` |
| `_serve` | function | `tests/test_atomic_exploit_bridge.py:216` | `def _serve()` |
| `_valid_doc` | function | `tests/test_atomic_exploit_bridge.py:32` | `def _valid_doc()` |
| `_write` | function | `tests/test_atomic_exploit_bridge.py:27` | `def _write(path, data)` |
| `run` | method | `tests/test_atomic_exploit_bridge.py:362` | `def run(self, command, timeout)` |
| `test_addon_paths_match_cwd` | function | `tests/test_atomic_exploit_bridge.py:192` | `def test_addon_paths_match_cwd()` |
| `test_addon_schema` | function | `tests/test_atomic_exploit_bridge.py:182` | `def test_addon_schema()` |
| `test_auto_sweep_from_scan_xml` | function | `tests/test_atomic_exploit_bridge.py:140` | `def test_auto_sweep_from_scan_xml(tmp_path, monkeypatch)` |
| `test_build_commands_tokens` | function | `tests/test_atomic_exploit_bridge.py:101` | `def test_build_commands_tokens(tmp_path)` |
| `test_cleanup_no_session_reports_honestly` | function | `tests/test_atomic_exploit_bridge.py:394` | `def test_cleanup_no_session_reports_honestly(monkeypatch)` |
| `test_cleanup_soft_removes_but_keeps_loot` | function | `tests/test_atomic_exploit_bridge.py:367` | `def test_cleanup_soft_removes_but_keeps_loot(tmp_path, monkeypatch)` |
| `test_destroy_gym_validates_and_handles_missing_docker` | function | `tests/test_atomic_exploit_bridge.py:403` | `def test_destroy_gym_validates_and_handles_missing_docker(monkeypatch)` |
| `test_engine_prefers_yaml_over_hardcode` | function | `tests/test_atomic_exploit_bridge.py:166` | `def test_engine_prefers_yaml_over_hardcode(tmp_path, monkeypatch)` |
| `test_ensure_session_adopts_orphan` | function | `tests/test_atomic_exploit_bridge.py:334` | `def test_ensure_session_adopts_orphan(monkeypatch)` |
| `test_interactive_shell_no_spec_reports_error` | function | `tests/test_atomic_exploit_bridge.py:465` | `def test_interactive_shell_no_spec_reports_error(monkeypatch)` |
| `test_interactive_shell_repl_until_exit` | function | `tests/test_atomic_exploit_bridge.py:437` | `def test_interactive_shell_repl_until_exit(monkeypatch, capsys)` |
| `test_interactive_shell_verify_only_without_tty` | function | `tests/test_atomic_exploit_bridge.py:427` | `def test_interactive_shell_verify_only_without_tty(monkeypatch, capsys)` |
| `test_load_all_skips_invalid_and_disabled` | function | `tests/test_atomic_exploit_bridge.py:81` | `def test_load_all_skips_invalid_and_disabled(tmp_path)` |
| `test_match_is_exact_or_all` | function | `tests/test_atomic_exploit_bridge.py:90` | `def test_match_is_exact_or_all()` |
| `test_open_shell_gives_up` | function | `tests/test_atomic_exploit_bridge.py:322` | `def test_open_shell_gives_up(monkeypatch)` |
| `test_open_shell_retries_racy_trigger` | function | `tests/test_atomic_exploit_bridge.py:297` | `def test_open_shell_retries_racy_trigger(monkeypatch)` |
| `test_rank_orders_severity_then_confidence` | function | `tests/test_atomic_exploit_bridge.py:110` | `def test_rank_orders_severity_then_confidence(tmp_path)` |
| `test_run_spec_detects_shell_without_network` | function | `tests/test_atomic_exploit_bridge.py:121` | `def test_run_spec_detects_shell_without_network()` |
| `test_session_multiplexes_commands` | function | `tests/test_atomic_exploit_bridge.py:239` | `def test_session_multiplexes_commands()` |
| `test_validate_accepts_good_document` | function | `tests/test_atomic_exploit_bridge.py:54` | `def test_validate_accepts_good_document()` |
| `test_validate_rejects_bad_documents` | function | `tests/test_atomic_exploit_bridge.py:59` | `def test_validate_rejects_bad_documents()` |
| `_fixture_atomics` | function | `tests/test_atomic_loop.py:20` | `def _fixture_atomics(root)` |
| `test_apt_chain_binds_playbook_and_target` | function | `tests/test_atomic_loop.py:135` | `def test_apt_chain_binds_playbook_and_target()` |
| `test_apt_chain_keyword_never_invents_playbook` | function | `tests/test_atomic_loop.py:145` | `def test_apt_chain_keyword_never_invents_playbook()` |
| `test_apt_chain_line_routes_via_shell` | function | `tests/test_atomic_loop.py:156` | `def test_apt_chain_line_routes_via_shell()` |
| `test_atomic_clean_routes_and_never_autofires` | function | `tests/test_atomic_loop.py:212` | `def test_atomic_clean_routes_and_never_autofires()` |
| `test_atomic_lines_are_always_non_interactive` | function | `tests/test_atomic_loop.py:62` | `def test_atomic_lines_are_always_non_interactive()` |
| `test_atomic_shell_never_interactive_from_loop` | function | `tests/test_atomic_loop.py:202` | `def test_atomic_shell_never_interactive_from_loop()` |
| `test_loop_reaches_apt_chain_end_to_end` | function | `tests/test_atomic_loop.py:112` | `def test_loop_reaches_apt_chain_end_to_end()` |
| `test_planner_discovers_apt_chain_verb` | function | `tests/test_atomic_loop.py:168` | `def test_planner_discovers_apt_chain_verb()` |
| `test_planner_discovers_atomic_verbs` | function | `tests/test_atomic_loop.py:73` | `def test_planner_discovers_atomic_verbs()` |
| `test_planner_discovers_playbook_verb` | function | `tests/test_atomic_loop.py:106` | `def test_planner_discovers_playbook_verb()` |
| `test_rocke_playbook_resolves_linux_chain` | function | `tests/test_atomic_loop.py:94` | `def test_rocke_playbook_resolves_linux_chain()` |
| `test_steps_for_explicit_atomic_intent` | function | `tests/test_atomic_loop.py:44` | `def test_steps_for_explicit_atomic_intent()` |
| `test_steps_for_explicit_playbook_intent` | function | `tests/test_atomic_loop.py:79` | `def test_steps_for_explicit_playbook_intent()` |
| `test_steps_for_keyword_atomic_intent` | function | `tests/test_atomic_loop.py:54` | `def test_steps_for_keyword_atomic_intent()` |
| `test_steps_for_keyword_playbook_intent` | function | `tests/test_atomic_loop.py:85` | `def test_steps_for_keyword_playbook_intent()` |
| `test_validate_resolves_technique_ids` | function | `tests/test_atomic_loop.py:174` | `def test_validate_resolves_technique_ids(tmp_path, monkeypatch)` |
| `_write_fixture_atomics` | function | `tests/test_atomic_resolver.py:30` | `def _write_fixture_atomics(root)` |
| `test_chain_skips_invalid` | function | `tests/test_atomic_resolver.py:114` | `def test_chain_skips_invalid(tmp_path)` |
| `test_guid_validation_roundtrip` | function | `tests/test_atomic_resolver.py:79` | `def test_guid_validation_roundtrip()` |
| `test_normalize_mitre_accepts_variants` | function | `tests/test_atomic_resolver.py:64` | `def test_normalize_mitre_accepts_variants()` |
| `test_normalize_mitre_rejects_injection` | function | `tests/test_atomic_resolver.py:71` | `def test_normalize_mitre_rejects_injection()` |
| `test_platform_allowlist` | function | `tests/test_atomic_resolver.py:87` | `def test_platform_allowlist()` |
| `test_resolver_lists_and_filters` | function | `tests/test_atomic_resolver.py:94` | `def test_resolver_lists_and_filters(tmp_path)` |
| `test_resolver_prefix_and_unknown` | function | `tests/test_atomic_resolver.py:105` | `def test_resolver_prefix_and_unknown(tmp_path)` |
| `test_variables_and_render` | function | `tests/test_atomic_resolver.py:121` | `def test_variables_and_render()` |
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
| `test_eof_encrypts_before_returning` | method | `tests/test_auto_crypto.py:213` | `def test_eof_encrypts_before_returning(self, monkeypatch)` |
| `test_exit_encrypts_after_confirmation` | method | `tests/test_auto_crypto.py:195` | `def test_exit_encrypts_after_confirmation(self, monkeypatch)` |
| `test_false_when_provider_returns_empty` | method | `tests/test_auto_crypto.py:163` | `def test_false_when_provider_returns_empty(self, crypto_module, tmp_sessions)` |
| `test_false_without_provider` | method | `tests/test_auto_crypto.py:153` | `def test_false_without_provider(self, crypto_module, tmp_sessions)` |
| `test_no_password_provider_returns_false` | method | `tests/test_auto_crypto.py:66` | `def test_no_password_provider_returns_false(self, crypto_module, tmp_sessions)` |
| `test_qa_encrypts_before_exit` | method | `tests/test_auto_crypto.py:180` | `def test_qa_encrypts_before_exit(self, monkeypatch)` |
| `test_salt_is_persisted` | method | `tests/test_auto_crypto.py:122` | `def test_salt_is_persisted(self, crypto_module, tmp_sessions)` |
| `test_true_with_provider` | method | `tests/test_auto_crypto.py:158` | `def test_true_with_provider(self, crypto_module, tmp_sessions)` |
| `tmp_sessions` | function | `tests/test_auto_crypto.py:28` | `def tmp_sessions()` |
| `TestDecisionPersistence` | class | `tests/test_auto_loop_memory.py:86` | `class TestDecisionPersistence` |
| `TestFailureMemory` | class | `tests/test_auto_loop_memory.py:13` | `class TestFailureMemory` |
| `TestFailureMemorySanctioned` | class | `tests/test_auto_loop_memory.py:71` | `class TestFailureMemorySanctioned` |
| `TestSelectorManager` | class | `tests/test_auto_loop_memory.py:121` | `class TestSelectorManager` |
| `test_all_blocked_returns_none` | method | `tests/test_auto_loop_memory.py:144` | `def test_all_blocked_returns_none(self)` |
| `test_blocked_after_threshold_by_base` | method | `tests/test_auto_loop_memory.py:25` | `def test_blocked_after_threshold_by_base(self, tmp_path)` |
| `test_blocked_proposal_skipped_with_trace` | method | `tests/test_auto_loop_memory.py:130` | `def test_blocked_proposal_skipped_with_trace(self)` |
| `test_clear_target_forgets_records` | method | `tests/test_auto_loop_memory.py:53` | `def test_clear_target_forgets_records(self, tmp_path)` |
| `test_counts_persist_across_reload` | method | `tests/test_auto_loop_memory.py:16` | `def test_counts_persist_across_reload(self, tmp_path)` |
| `test_duplicates_deduped` | method | `tests/test_auto_loop_memory.py:149` | `def test_duplicates_deduped(self)` |
| `test_empty_command_rejected` | method | `tests/test_auto_loop_memory.py:155` | `def test_empty_command_rejected(self)` |
| `test_invalid_key_raises` | method | `tests/test_auto_loop_memory.py:63` | `def test_invalid_key_raises(self, tmp_path)` |
| `test_newest_First_and_persisted` | method | `tests/test_auto_loop_memory.py:99` | `def test_newest_First_and_persisted(self, tmp_path)` |
| `test_priority_order_wins` | method | `tests/test_auto_loop_memory.py:124` | `def test_priority_order_wins(self)` |
| `test_push_ignores_empty_and_caps` | method | `tests/test_auto_loop_memory.py:110` | `def test_push_ignores_empty_and_caps(self, tmp_path)` |
| `test_push_pop_round_trip` | method | `tests/test_auto_loop_memory.py:89` | `def test_push_pop_round_trip(self, tmp_path)` |
| `test_sanctioned_lists_sorted_rows` | method | `tests/test_auto_loop_memory.py:74` | `def test_sanctioned_lists_sorted_rows(self, tmp_path)` |
| `test_trims_to_capacity` | method | `tests/test_auto_loop_memory.py:43` | `def test_trims_to_capacity(self, tmp_path)` |
| `test_veto_blocks_immediately_and_persists` | method | `tests/test_auto_loop_memory.py:35` | `def test_veto_blocks_immediately_and_persists(self, tmp_path)` |
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
| `test_graph_provider_returns_none_when_advisor_empty` | function | `tests/test_autosuggest.py:232` | `def test_graph_provider_returns_none_when_advisor_empty()` |
| `test_graph_provider_returns_top_result` | function | `tests/test_autosuggest.py:215` | `def test_graph_provider_returns_top_result()` |
| `test_graph_provider_skips_when_last_command_blank` | function | `tests/test_autosuggest.py:239` | `def test_graph_provider_skips_when_last_command_blank()` |
| `test_killchain_provider_falls_back_to_phase_priority` | function | `tests/test_autosuggest.py:184` | `def test_killchain_provider_falls_back_to_phase_priority()` |
| `test_killchain_provider_returns_none_with_nothing_to_offer` | function | `tests/test_autosuggest.py:197` | `def test_killchain_provider_returns_none_with_nothing_to_offer()` |
| `test_killchain_provider_skips_already_executed` | function | `tests/test_autosuggest.py:169` | `def test_killchain_provider_skips_already_executed()` |
| `test_killchain_provider_uses_adjacency` | function | `tests/test_autosuggest.py:158` | `def test_killchain_provider_uses_adjacency()` |
| `test_render_hint_line_emits_to_console` | function | `tests/test_autosuggest.py:303` | `def test_render_hint_line_emits_to_console()` |
| `test_render_hint_line_is_noop_when_disabled` | function | `tests/test_autosuggest.py:325` | `def test_render_hint_line_is_noop_when_disabled()` |
| `test_render_hint_line_is_noop_without_suggestion` | function | `tests/test_autosuggest.py:315` | `def test_render_hint_line_is_noop_without_suggestion()` |
| `test_ensure_persists_once_then_reuses` | function | `tests/test_backdoor_random.py:50` | `def test_ensure_persists_once_then_reuses(monkeypatch)` |
| `test_password_assign_and_shell_safe` | function | `tests/test_backdoor_random.py:25` | `def test_password_assign_and_shell_safe()` |
| `test_resolve_generates_on_placeholders` | function | `tests/test_backdoor_random.py:39` | `def test_resolve_generates_on_placeholders()` |
| `test_resolve_keeps_configured` | function | `tests/test_backdoor_random.py:33` | `def test_resolve_keeps_configured()` |
| `test_username_shape_and_uniqueness` | function | `tests/test_backdoor_random.py:17` | `def test_username_shape_and_uniqueness()` |
| `_FakeResp` | class | `tests/test_banner_config.py:281` | `class _FakeResp` |
| `__enter__` | method | `tests/test_banner_config.py:282` | `def __enter__(self)` |
| `__exit__` | method | `tests/test_banner_config.py:285` | `def __exit__(self)` |
| `_make_ctx` | function | `tests/test_banner_config.py:150` | `def _make_ctx(palette)` |
| `color_registry` | function | `tests/test_banner_config.py:42` | `def color_registry()` |
| `glyph_registry` | function | `tests/test_banner_config.py:47` | `def glyph_registry()` |
| `neutral_palette` | function | `tests/test_banner_config.py:52` | `def neutral_palette()` |
| `read` | method | `tests/test_banner_config.py:288` | `def read(self)` |
| `registry` | function | `tests/test_banner_config.py:37` | `def registry()` |
| `test_banner_summary_handles_empty` | function | `tests/test_banner_config.py:254` | `def test_banner_summary_handles_empty()` |
| `test_banner_summary_lists_enabled_ids_sorted` | function | `tests/test_banner_config.py:248` | `def test_banner_summary_lists_enabled_ids_sorted()` |
| `test_color_registry_cycle_wraps_around` | function | `tests/test_banner_config.py:327` | `def test_color_registry_cycle_wraps_around(color_registry)` |
| `test_color_registry_exposes_named_palette` | function | `tests/test_banner_config.py:320` | `def test_color_registry_exposes_named_palette(color_registry)` |
| `test_color_registry_resolve_unknown_falls_back` | function | `tests/test_banner_config.py:335` | `def test_color_registry_resolve_unknown_falls_back(color_registry)` |
| `test_configurator_returns_none_in_non_tty_environment` | function | `tests/test_banner_config.py:303` | `def test_configurator_returns_none_in_non_tty_environment(monkeypatch, registry, neutral_palette, color_registry...` |
| `test_context_resolver_public_ip_caches_within_ttl` | function | `tests/test_banner_config.py:275` | `def test_context_resolver_public_ip_caches_within_ttl(neutral_palette)` |
| `test_context_resolver_uses_payload_rhost_and_lhost` | function | `tests/test_banner_config.py:261` | `def test_context_resolver_uses_payload_rhost_and_lhost(neutral_palette)` |
| `test_glyph_registry_cycle_preserves_unknown_value` | function | `tests/test_banner_config.py:357` | `def test_glyph_registry_cycle_preserves_unknown_value(glyph_registry)` |
| `test_glyph_registry_cycle_returns_known_choice` | function | `tests/test_banner_config.py:350` | `def test_glyph_registry_cycle_returns_known_choice(glyph_registry)` |
| `test_glyph_registry_exposes_canonical_slots` | function | `tests/test_banner_config.py:344` | `def test_glyph_registry_exposes_canonical_slots(glyph_registry)` |
| `test_registry_group_partition` | function | `tests/test_banner_config.py:88` | `def test_registry_group_partition(registry)` |
| `test_registry_lists_every_canonical_segment` | function | `tests/test_banner_config.py:68` | `def test_registry_lists_every_canonical_segment(registry)` |
| `test_registry_lookup_returns_none_for_unknown` | function | `tests/test_banner_config.py:96` | `def test_registry_lookup_returns_none_for_unknown(registry)` |
| `test_render_prompt_honours_payload_colors_and_glyphs` | function | `tests/test_banner_config.py:458` | `def test_render_prompt_honours_payload_colors_and_glyphs()` |
| `test_render_prompt_uses_payload_banner_block` | function | `tests/test_banner_config.py:228` | `def test_render_prompt_uses_payload_banner_block()` |
| `test_render_prompt_with_no_payload_uses_defaults` | function | `tests/test_banner_config.py:239` | `def test_render_prompt_with_no_payload_uses_defaults()` |
| `test_renderer_drops_empty_value_segments` | function | `tests/test_banner_config.py:206` | `def test_renderer_drops_empty_value_segments(registry, neutral_palette)` |
| `test_renderer_emits_chosen_color_for_each_segment` | function | `tests/test_banner_config.py:418` | `def test_renderer_emits_chosen_color_for_each_segment(registry, color_registry, glyph_registry, neutral_palette)` |
| `test_renderer_emits_three_lines_with_box_corners` | function | `tests/test_banner_config.py:176` | `def test_renderer_emits_three_lines_with_box_corners(registry, neutral_palette)` |
| `test_renderer_includes_kernel_and_version_when_enabled` | function | `tests/test_banner_config.py:198` | `def test_renderer_includes_kernel_and_version_when_enabled(registry, neutral_palette)` |
| `test_renderer_marks_dirty_git_with_dirty_glyph` | function | `tests/test_banner_config.py:214` | `def test_renderer_marks_dirty_git_with_dirty_glyph(registry, neutral_palette)` |
| `test_renderer_omits_disabled_segments` | function | `tests/test_banner_config.py:187` | `def test_renderer_omits_disabled_segments(registry, neutral_palette)` |
| `test_renderer_uses_glyph_overrides_in_box` | function | `tests/test_banner_config.py:438` | `def test_renderer_uses_glyph_overrides_in_box(registry, color_registry, glyph_registry, neutral_palette)` |
| `test_settings_cycle_color_uses_registry_order` | function | `tests/test_banner_config.py:391` | `def test_settings_cycle_color_uses_registry_order(registry, color_registry)` |
| `test_settings_cycle_glyph_uses_registry_order` | function | `tests/test_banner_config.py:398` | `def test_settings_cycle_glyph_uses_registry_order(registry, color_registry, glyph_registry)` |
| `test_settings_defaults_match_registry_defaults` | function | `tests/test_banner_config.py:103` | `def test_settings_defaults_match_registry_defaults(registry)` |
| `test_settings_enable_all_then_disable_all` | function | `tests/test_banner_config.py:139` | `def test_settings_enable_all_then_disable_all(registry)` |
| `test_settings_from_payload_falls_back_to_defaults_when_missing` | function | `tests/test_banner_config.py:120` | `def test_settings_from_payload_falls_back_to_defaults_when_missing(registry)` |
| `test_settings_from_payload_ignores_unknown_color_names` | function | `tests/test_banner_config.py:379` | `def test_settings_from_payload_ignores_unknown_color_names(registry, color_registry, glyph_registry)` |
| `test_settings_from_payload_ignores_unknown_glyph_chars` | function | `tests/test_banner_config.py:385` | `def test_settings_from_payload_ignores_unknown_glyph_chars(registry, color_registry, glyph_registry)` |
| `test_settings_from_payload_ignores_unknown_ids` | function | `tests/test_banner_config.py:125` | `def test_settings_from_payload_ignores_unknown_ids(registry)` |
| `test_settings_reset_color_and_glyph_for_specific_id` | function | `tests/test_banner_config.py:405` | `def test_settings_reset_color_and_glyph_for_specific_id(registry, color_registry, glyph_registry)` |
| `test_settings_round_trip_carries_colors_and_glyphs` | function | `tests/test_banner_config.py:364` | `def test_settings_round_trip_carries_colors_and_glyphs(registry, color_registry, glyph_registry)` |
| `test_settings_round_trip_through_payload_block` | function | `tests/test_banner_config.py:113` | `def test_settings_round_trip_through_payload_block(registry)` |
| `test_settings_toggle_adds_then_removes` | function | `tests/test_banner_config.py:131` | `def test_settings_toggle_adds_then_removes()` |
| `Completed` | class | `tests/test_bdd_infra_range_report.py:28` | `class Completed` |
| `test_bdd_beacon_build_injects_fallback_urls` | function | `tests/test_bdd_infra_range_report.py:51` | `def test_bdd_beacon_build_injects_fallback_urls()` |
| `test_bdd_range_compose_topology` | function | `tests/test_bdd_infra_range_report.py:65` | `def test_bdd_range_compose_topology()` |
| `test_bdd_redirector_spawn_registers_urls` | function | `tests/test_bdd_infra_range_report.py:15` | `def test_bdd_redirector_spawn_registers_urls()` |
| `test_bdd_report_executive_summary_without_ai` | function | `tests/test_bdd_infra_range_report.py:83` | `def test_bdd_report_executive_summary_without_ai()` |
| `TestBeaconConfig` | class | `tests/test_beacon_config_builder.py:22` | `class TestBeaconConfig` |
| `TestBeaconConfigBuilder` | class | `tests/test_beacon_config_builder.py:141` | `class TestBeaconConfigBuilder` |
| `TestGenerateBofExecutionCommand` | class | `tests/test_beacon_config_builder.py:205` | `class TestGenerateBofExecutionCommand` |
| `test_basic_bof_command` | method | `tests/test_beacon_config_builder.py:206` | `def test_basic_bof_command(self)` |
| `test_bof_with_args` | method | `tests/test_beacon_config_builder.py:214` | `def test_bof_with_args(self)` |
| `test_build_falls_back_on_missing_engines` | method | `tests/test_beacon_config_builder.py:197` | `def test_build_falls_back_on_missing_engines(self)` |
| `test_build_injects_dns_from_payload` | method | `tests/test_beacon_config_builder.py:183` | `def test_build_injects_dns_from_payload(self)` |
| `test_build_injects_tls_from_payload` | method | `tests/test_beacon_config_builder.py:170` | `def test_build_injects_tls_from_payload(self)` |
| `test_build_minimal` | method | `tests/test_beacon_config_builder.py:142` | `def test_build_minimal(self)` |
| `test_build_with_malleable_route` | method | `tests/test_beacon_config_builder.py:157` | `def test_build_with_malleable_route(self)` |
| `test_custom_bofs_dir` | method | `tests/test_beacon_config_builder.py:224` | `def test_custom_bofs_dir(self)` |
| `test_default_construction` | method | `tests/test_beacon_config_builder.py:23` | `def test_default_construction(self)` |
| `test_to_config_json` | method | `tests/test_beacon_config_builder.py:85` | `def test_to_config_json(self)` |
| `test_to_dict_serialization` | method | `tests/test_beacon_config_builder.py:113` | `def test_to_dict_serialization(self)` |
| `test_to_gen_beacon_args` | method | `tests/test_beacon_config_builder.py:36` | `def test_to_gen_beacon_args(self)` |
| `test_to_go_implant_vars` | method | `tests/test_beacon_config_builder.py:59` | `def test_to_go_implant_vars(self)` |
| `TestAppendRead` | class | `tests/test_beacon_history.py:38` | `class TestAppendRead` |
| `TestSanitization` | class | `tests/test_beacon_history.py:23` | `class TestSanitization` |
| `_config` | function | `tests/test_beacon_history.py:19` | `def _config(tmp_path)` |
| `test_append_then_read_round_trips` | method | `tests/test_beacon_history.py:39` | `def test_append_then_read_round_trips(self, tmp_path)` |
| `test_missing_history_reads_empty` | method | `tests/test_beacon_history.py:72` | `def test_missing_history_reads_empty(self, tmp_path)` |
| `test_multiple_beacons_do_not_interleave` | method | `tests/test_beacon_history.py:50` | `def test_multiple_beacons_do_not_interleave(self, tmp_path)` |
| `test_record_without_client_id_is_rejected` | method | `tests/test_beacon_history.py:75` | `def test_record_without_client_id_is_rejected(self, tmp_path)` |
| `test_records_path_is_bounded_inside_sessions` | method | `tests/test_beacon_history.py:29` | `def test_records_path_is_bounded_inside_sessions(self, tmp_path)` |
| `test_sanitize_client_id_strips_unsafe_chars` | method | `tests/test_beacon_history.py:24` | `def test_sanitize_client_id_strips_unsafe_chars(self)` |
| `test_skips_malformed_lines` | method | `tests/test_beacon_history.py:59` | `def test_skips_malformed_lines(self, tmp_path)` |
| `TestBeaconCategory` | class | `tests/test_blacksandbeacon_addon.py:111` | `class TestBeaconCategory` |

Next: [SYMBOLS_p32.md](SYMBOLS_p32.md)
