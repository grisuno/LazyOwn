# Symbols (page 38 of 54)
Previous: [SYMBOLS_p37.md](SYMBOLS_p37.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_deploy_never_uses_predictable_tmp_path` | method | `tests/test_c2_agent_dual.py:136` | `def test_deploy_never_uses_predictable_tmp_path(self)` |
| `test_ids_validate` | method | `tests/test_c2_agent_dual.py:57` | `def test_ids_validate(self)` |
| `test_invalid_privilege` | method | `tests/test_c2_agent_dual.py:73` | `def test_invalid_privilege(self)` |
| `test_invalid_privilege_rejected` | method | `tests/test_c2_agent_dual.py:53` | `def test_invalid_privilege_rejected(self)` |
| `test_lowpriv_accepts_best_ranked` | method | `tests/test_c2_agent_dual.py:86` | `def test_lowpriv_accepts_best_ranked(self)` |
| `test_lowpriv_default` | method | `tests/test_c2_agent_dual.py:64` | `def test_lowpriv_default(self)` |
| `test_root_id_suffix` | method | `tests/test_c2_agent_dual.py:50` | `def test_root_id_suffix(self)` |
| `test_root_profile` | method | `tests/test_c2_agent_dual.py:69` | `def test_root_profile(self)` |
| `test_root_request_excludes_lowpriv_specs` | method | `tests/test_c2_agent_dual.py:79` | `def test_root_request_excludes_lowpriv_specs(self)` |
| `test_root_without_root_primitive` | method | `tests/test_c2_agent_dual.py:103` | `def test_root_without_root_primitive(self)` |
| `test_unknown_privilege` | method | `tests/test_c2_agent_dual.py:93` | `def test_unknown_privilege(self)` |
| `test_unknown_privilege` | method | `tests/test_c2_agent_dual.py:99` | `def test_unknown_privilege(self)` |
| `TestEndpoint` | class | `tests/test_c2_autostart.py:37` | `class TestEndpoint` |
| `TestMaybeStartC2` | class | `tests/test_c2_autostart.py:56` | `class TestMaybeStartC2` |
| `_allow_pytest_call` | function | `tests/test_c2_autostart.py:25` | `def _allow_pytest_call(monkeypatch)` |
| `fake_alive` | function | `tests/test_c2_autostart.py:80` | `def fake_alive(host, port)` |
| `raising` | function | `tests/test_c2_autostart.py:129` | `def raising()` |
| `runner` | function | `tests/test_c2_autostart.py:19` | `def runner()` |
| `test_already_listening_skips_spawn` | method | `tests/test_c2_autostart.py:65` | `def test_already_listening_skips_spawn(self, runner, monkeypatch)` |
| `test_bad_port_falls_back` | method | `tests/test_c2_autostart.py:51` | `def test_bad_port_falls_back(self, runner)` |
| `test_bind_address_wins` | method | `tests/test_c2_autostart.py:38` | `def test_bind_address_wins(self, runner)` |
| `test_flag_off_is_noop` | method | `tests/test_c2_autostart.py:57` | `def test_flag_off_is_noop(self, runner, monkeypatch)` |
| `test_never_raises_on_spawn_failure` | method | `tests/test_c2_autostart.py:126` | `def test_never_raises_on_spawn_failure(self, runner, monkeypatch)` |
| `test_no_tip_when_handoff_on` | method | `tests/test_c2_autostart.py:146` | `def test_no_tip_when_handoff_on(self, runner, monkeypatch)` |
| `test_port_fallback` | method | `tests/test_c2_autostart.py:46` | `def test_port_fallback(self, runner)` |
| `test_pytest_guard_blocks_spawn` | method | `tests/test_c2_autostart.py:119` | `def test_pytest_guard_blocks_spawn(self, runner, monkeypatch)` |
| `test_spawn_and_wait_success` | method | `tests/test_c2_autostart.py:74` | `def test_spawn_and_wait_success(self, runner, monkeypatch)` |
| `test_spawn_never_listening_warns` | method | `tests/test_c2_autostart.py:101` | `def test_spawn_never_listening_warns(self, runner, monkeypatch)` |
| `test_tip_when_handoff_off` | method | `tests/test_c2_autostart.py:136` | `def test_tip_when_handoff_off(self, runner, monkeypatch)` |
| `test_wildcard_maps_to_loopback` | method | `tests/test_c2_autostart.py:42` | `def test_wildcard_maps_to_loopback(self, runner)` |
| `_FakeStore` | class | `tests/test_c2_credential_bootstrap.py:27` | `class _FakeStore` |
| `_FakeUser` | class | `tests/test_c2_credential_bootstrap.py:20` | `class _FakeUser` |
| `__init__` | method | `tests/test_c2_credential_bootstrap.py:21` | `def __init__(self, username, password_hash, role)` |
| `__init__` | method | `tests/test_c2_credential_bootstrap.py:28` | `def __init__(self, users, unreadable)` |
| `_resolve` | function | `tests/test_c2_credential_bootstrap.py:94` | `def _resolve(user, password, rotate)` |
| `create_user` | method | `tests/test_c2_credential_bootstrap.py:45` | `def create_user(self, username, password_hash, role)` |
| `find_by_username` | method | `tests/test_c2_credential_bootstrap.py:34` | `def find_by_username(self, username)` |
| `save` | method | `tests/test_c2_credential_bootstrap.py:42` | `def save(self, user)` |
| `test_boot_block_applies_rotation_flag` | function | `tests/test_c2_credential_bootstrap.py:123` | `def test_boot_block_applies_rotation_flag()` |
| `test_boot_block_writes_file_and_registers_cli_user` | function | `tests/test_c2_credential_bootstrap.py:136` | `def test_boot_block_writes_file_and_registers_cli_user()` |
| `test_boot_starts_revshell_listener_thread` | function | `tests/test_c2_credential_bootstrap.py:145` | `def test_boot_starts_revshell_listener_thread()` |
| `test_credentials_file_written_owner_only` | function | `tests/test_c2_credential_bootstrap.py:52` | `def test_credentials_file_written_owner_only(tmp_path)` |
| `test_register_cli_user_creates_when_new` | function | `tests/test_c2_credential_bootstrap.py:68` | `def test_register_cli_user_creates_when_new(tmp_path)` |
| `test_register_cli_user_never_touches_other_accounts` | function | `tests/test_c2_credential_bootstrap.py:82` | `def test_register_cli_user_never_touches_other_accounts(tmp_path)` |
| `test_register_cli_user_skips_unreadable_store` | function | `tests/test_c2_credential_bootstrap.py:75` | `def test_register_cli_user_skips_unreadable_store()` |
| `test_register_cli_user_updates_existing` | function | `tests/test_c2_credential_bootstrap.py:60` | `def test_register_cli_user_updates_existing(tmp_path)` |
| `test_resolve_keeps_strong_credentials` | function | `tests/test_c2_credential_bootstrap.py:111` | `def test_resolve_keeps_strong_credentials()` |
| `test_resolve_on_boot_flag_wins_over_strong_creds` | function | `tests/test_c2_credential_bootstrap.py:117` | `def test_resolve_on_boot_flag_wins_over_strong_creds()` |
| `test_resolve_rotates_insecure_credentials` | function | `tests/test_c2_credential_bootstrap.py:105` | `def test_resolve_rotates_insecure_credentials()` |
| `test_revshell_listener_accepts_multiple_sessions` | function | `tests/test_c2_credential_bootstrap.py:152` | `def test_revshell_listener_accepts_multiple_sessions()` |
| `test_revshell_listener_is_not_login_gated` | function | `tests/test_c2_credential_bootstrap.py:131` | `def test_revshell_listener_is_not_login_gated()` |
| `TestRealC2Process` | class | `tests/test_c2_process_smoke.py:127` | `class TestRealC2Process` |
| `_free_port` | function | `tests/test_c2_process_smoke.py:35` | `def _free_port()` |
| `_wait_port` | function | `tests/test_c2_process_smoke.py:41` | `def _wait_port(port, proc, timeout)` |
| `c2_server` | function | `tests/test_c2_process_smoke.py:55` | `def c2_server(tmp_path)` |
| `test_cli_basic_channel_without_token` | method | `tests/test_c2_process_smoke.py:173` | `def test_cli_basic_channel_without_token(self, c2_server)` |
| `test_health_remote_shape` | method | `tests/test_c2_process_smoke.py:128` | `def test_health_remote_shape(self, c2_server)` |
| `test_login_then_csrf_command_flow` | method | `tests/test_c2_process_smoke.py:137` | `def test_login_then_csrf_command_flow(self, c2_server)` |
| `TestDnsProfile` | class | `tests/test_c2_profile_engine.py:99` | `class TestDnsProfile` |
| `TestProfileEngine` | class | `tests/test_c2_profile_engine.py:397` | `class TestProfileEngine` |
| `TestProfileRotator` | class | `tests/test_c2_profile_engine.py:214` | `class TestProfileRotator` |
| `TestProfileValidator` | class | `tests/test_c2_profile_engine.py:291` | `class TestProfileValidator` |
| `TestSmbProfile` | class | `tests/test_c2_profile_engine.py:154` | `class TestSmbProfile` |
| `TestTlsProfile` | class | `tests/test_c2_profile_engine.py:34` | `class TestTlsProfile` |
| `TestWebSocketProfile` | class | `tests/test_c2_profile_engine.py:183` | `class TestWebSocketProfile` |
| `test_build_query_subdomain_base32` | method | `tests/test_c2_profile_engine.py:113` | `def test_build_query_subdomain_base32(self)` |
| `test_build_query_subdomain_base64` | method | `tests/test_c2_profile_engine.py:107` | `def test_build_query_subdomain_base64(self)` |
| `test_build_query_subdomain_hex` | method | `tests/test_c2_profile_engine.py:119` | `def test_build_query_subdomain_hex(self)` |
| `test_build_query_subdomain_truncates_to_max_length` | method | `tests/test_c2_profile_engine.py:124` | `def test_build_query_subdomain_truncates_to_max_length(self)` |
| `test_build_query_subdomain_ttl_cache_bypass_disabled` | method | `tests/test_c2_profile_engine.py:130` | `def test_build_query_subdomain_ttl_cache_bypass_disabled(self)` |
| `test_current_slot_identity` | method | `tests/test_c2_profile_engine.py:283` | `def test_current_slot_identity(self)` |
| `test_default_construction` | method | `tests/test_c2_profile_engine.py:35` | `def test_default_construction(self)` |
| `test_default_construction` | method | `tests/test_c2_profile_engine.py:100` | `def test_default_construction(self)` |
| `test_default_construction` | method | `tests/test_c2_profile_engine.py:155` | `def test_default_construction(self)` |
| `test_default_construction` | method | `tests/test_c2_profile_engine.py:184` | `def test_default_construction(self)` |
| `test_default_engine_has_http_slot` | method | `tests/test_c2_profile_engine.py:398` | `def test_default_engine_has_http_slot(self)` |
| `test_disabled_profile` | method | `tests/test_c2_profile_engine.py:94` | `def test_disabled_profile(self)` |
| `test_engine_empty_payload_falls_back_to_defaults` | method | `tests/test_c2_profile_engine.py:465` | `def test_engine_empty_payload_falls_back_to_defaults(self)` |
| `test_engine_from_dict` | method | `tests/test_c2_profile_engine.py:442` | `def test_engine_from_dict(self)` |
| `test_engine_from_payload` | method | `tests/test_c2_profile_engine.py:455` | `def test_engine_from_payload(self)` |
| `test_engine_get_active_profile_dict` | method | `tests/test_c2_profile_engine.py:427` | `def test_engine_get_active_profile_dict(self)` |
| `test_engine_get_all_profiles_dict` | method | `tests/test_c2_profile_engine.py:433` | `def test_engine_get_all_profiles_dict(self)` |
| `test_engine_rotate_through_transports` | method | `tests/test_c2_profile_engine.py:420` | `def test_engine_rotate_through_transports(self)` |
| `test_engine_validate_returns_errors_for_invalid_dns` | method | `tests/test_c2_profile_engine.py:412` | `def test_engine_validate_returns_errors_for_invalid_dns(self)` |
| `test_engine_with_all_transports` | method | `tests/test_c2_profile_engine.py:402` | `def test_engine_with_all_transports(self)` |
| `test_from_dict_empty` | method | `tests/test_c2_profile_engine.py:90` | `def test_from_dict_empty(self)` |
| `test_from_dict_empty` | method | `tests/test_c2_profile_engine.py:148` | `def test_from_dict_empty(self)` |
| `test_from_dict_empty` | method | `tests/test_c2_profile_engine.py:178` | `def test_from_dict_empty(self)` |
| `test_from_dict_empty` | method | `tests/test_c2_profile_engine.py:208` | `def test_from_dict_empty(self)` |
| `test_get_cipher_suites_returns_custom_when_set` | method | `tests/test_c2_profile_engine.py:50` | `def test_get_cipher_suites_returns_custom_when_set(self)` |
| `test_get_cipher_suites_returns_library_defaults` | method | `tests/test_c2_profile_engine.py:44` | `def test_get_cipher_suites_returns_library_defaults(self)` |
| `test_get_cipher_suites_unknown_library_falls_back_to_generic` | method | `tests/test_c2_profile_engine.py:55` | `def test_get_cipher_suites_unknown_library_falls_back_to_generic(self)` |
| `test_get_ja3_hash_produces_stable_output` | method | `tests/test_c2_profile_engine.py:61` | `def test_get_ja3_hash_produces_stable_output(self)` |
| `test_get_ja3_hash_with_grease_produces_variable_output` | method | `tests/test_c2_profile_engine.py:72` | `def test_get_ja3_hash_with_grease_produces_variable_output(self)` |
| `test_is_available_after_touch` | method | `tests/test_c2_profile_engine.py:278` | `def test_is_available_after_touch(self)` |
| `test_is_available_fresh_slot` | method | `tests/test_c2_profile_engine.py:274` | `def test_is_available_fresh_slot(self)` |
| `test_list_slots` | method | `tests/test_c2_profile_engine.py:263` | `def test_list_slots(self)` |
| `test_requires_at_least_one_slot` | method | `tests/test_c2_profile_engine.py:215` | `def test_requires_at_least_one_slot(self)` |
| `test_rotation_cycles_through_slots` | method | `tests/test_c2_profile_engine.py:226` | `def test_rotation_cycles_through_slots(self)` |
| `test_rotation_resets_all_cooldowns_when_all_busy` | method | `tests/test_c2_profile_engine.py:252` | `def test_rotation_resets_all_cooldowns_when_all_busy(self)` |
| `test_rotation_skips_cooldown_slots` | method | `tests/test_c2_profile_engine.py:238` | `def test_rotation_skips_cooldown_slots(self)` |
| `test_serialization_roundtrip` | method | `tests/test_c2_profile_engine.py:77` | `def test_serialization_roundtrip(self)` |
| `test_serialization_roundtrip` | method | `tests/test_c2_profile_engine.py:135` | `def test_serialization_roundtrip(self)` |
| `test_serialization_roundtrip` | method | `tests/test_c2_profile_engine.py:161` | `def test_serialization_roundtrip(self)` |
| `test_serialization_roundtrip` | method | `tests/test_c2_profile_engine.py:191` | `def test_serialization_roundtrip(self)` |
| `test_single_slot_always_active` | method | `tests/test_c2_profile_engine.py:219` | `def test_single_slot_always_active(self)` |
| `test_validate_all_returns_dict` | method | `tests/test_c2_profile_engine.py:383` | `def test_validate_all_returns_dict(self)` |
| `test_validate_dns_disabled_skips` | method | `tests/test_c2_profile_engine.py:339` | `def test_validate_dns_disabled_skips(self)` |
| `test_validate_dns_enabled_missing_domain` | method | `tests/test_c2_profile_engine.py:327` | `def test_validate_dns_enabled_missing_domain(self)` |
| `test_validate_dns_invalid_domain_format` | method | `tests/test_c2_profile_engine.py:344` | `def test_validate_dns_invalid_domain_format(self)` |
| `test_validate_dns_invalid_encoding` | method | `tests/test_c2_profile_engine.py:333` | `def test_validate_dns_invalid_encoding(self)` |
| `test_validate_smb_disabled_skips` | method | `tests/test_c2_profile_engine.py:356` | `def test_validate_smb_disabled_skips(self)` |
| `test_validate_smb_missing_pipe_name` | method | `tests/test_c2_profile_engine.py:350` | `def test_validate_smb_missing_pipe_name(self)` |
| `test_validate_smb_username_without_domain` | method | `tests/test_c2_profile_engine.py:361` | `def test_validate_smb_username_without_domain(self)` |
| `test_validate_tls_disabled_skips` | method | `tests/test_c2_profile_engine.py:297` | `def test_validate_tls_disabled_skips(self)` |
| `test_validate_tls_invalid_version` | method | `tests/test_c2_profile_engine.py:302` | `def test_validate_tls_invalid_version(self)` |
| `test_validate_tls_missing_key_with_cert` | method | `tests/test_c2_profile_engine.py:308` | `def test_validate_tls_missing_key_with_cert(self)` |
| `test_validate_tls_unknown_library` | method | `tests/test_c2_profile_engine.py:318` | `def test_validate_tls_unknown_library(self)` |
| `test_validate_tls_valid` | method | `tests/test_c2_profile_engine.py:292` | `def test_validate_tls_valid(self)` |
| `test_validate_websocket_disabled_skips` | method | `tests/test_c2_profile_engine.py:378` | `def test_validate_websocket_disabled_skips(self)` |
| `test_validate_websocket_invalid_protocol` | method | `tests/test_c2_profile_engine.py:372` | `def test_validate_websocket_invalid_protocol(self)` |
| `_route_decorators` | function | `tests/test_c2_route_auth.py:75` | `def _route_decorators()` |
| `routes` | function | `tests/test_c2_route_auth.py:106` | `def routes()` |
| `test_all_protected_endpoints_exist` | function | `tests/test_c2_route_auth.py:120` | `def test_all_protected_endpoints_exist(routes)` |
| `test_protected_endpoints_require_auth` | function | `tests/test_c2_route_auth.py:110` | `def test_protected_endpoints_require_auth(routes)` |
| `test_public_endpoints_stay_open` | function | `tests/test_c2_route_auth.py:115` | `def test_public_endpoints_stay_open(routes)` |
| `TestLazyShellProxy` | class | `tests/test_c2_shell_lazy.py:103` | `class TestLazyShellProxy` |
| `TestNoEagerCliBuild` | class | `tests/test_c2_shell_lazy.py:62` | `class TestNoEagerCliBuild` |
| `_FakeShell` | class | `tests/test_c2_shell_lazy.py:40` | `class _FakeShell` |
| `__init__` | method | `tests/test_c2_shell_lazy.py:41` | `def __init__(self)` |
| `_init_shell` | function | `tests/test_c2_shell_lazy.py:51` | `def _init_shell()` |
| `_load_proxy_class` | function | `tests/test_c2_shell_lazy.py:25` | `def _load_proxy_class()` |
| `_module_tree` | function | `tests/test_c2_shell_lazy.py:21` | `def _module_tree()` |
| `one_cmd` | method | `tests/test_c2_shell_lazy.py:45` | `def one_cmd(self, command)` |
| `test_lazy_accessor_with_boot_sequence` | method | `tests/test_c2_shell_lazy.py:88` | `def test_lazy_accessor_with_boot_sequence(self)` |
| `test_no_eager_shell_build` | method | `tests/test_c2_shell_lazy.py:76` | `def test_no_eager_shell_build(self)` |
| `test_no_lazyown_import_at_top_level` | method | `tests/test_c2_shell_lazy.py:63` | `def test_no_lazyown_import_at_top_level(self)` |
| `test_reads_forward_and_share_target` | method | `tests/test_c2_shell_lazy.py:104` | `def test_reads_forward_and_share_target(self)` |
| `test_shell_output_attribute` | method | `tests/test_c2_shell_lazy.py:118` | `def test_shell_output_attribute(self)` |
| `test_writes_forward` | method | `tests/test_c2_shell_lazy.py:111` | `def test_writes_forward(self)` |
| `_StubWM` | class | `tests/test_c2_surfaces.py:103` | `class _StubWM` |
| `_refused` | function | `tests/test_c2_surfaces.py:132` | `def _refused()` |
| `_sandbox` | function | `tests/test_c2_surfaces.py:23` | `def _sandbox(tmp_path)` |
| `_slow` | function | `tests/test_c2_surfaces.py:141` | `def _slow()` |
| `test_append_note_never_clobbers` | function | `tests/test_c2_surfaces.py:56` | `def test_append_note_never_clobbers(tmp_path)` |
| `test_group_tasks_unique_hits` | function | `tests/test_c2_surfaces.py:77` | `def test_group_tasks_unique_hits(tmp_path)` |
| `test_lazyreport_errors_are_actionable` | function | `tests/test_c2_surfaces.py:122` | `def test_lazyreport_errors_are_actionable(monkeypatch)` |
| `test_publish_banner_dedupes` | function | `tests/test_c2_surfaces.py:30` | `def test_publish_banner_dedupes(tmp_path)` |
| `test_publish_cve_validates_and_dedupes` | function | `tests/test_c2_surfaces.py:42` | `def test_publish_cve_validates_and_dedupes(tmp_path)` |
| `test_record_outcome_feeds_c2_surfaces` | function | `tests/test_c2_surfaces.py:95` | `def test_record_outcome_feeds_c2_surfaces(tmp_path, monkeypatch)` |
| `test_register_loot_event_dedupes_and_rejects_traversal` | function | `tests/test_c2_surfaces.py:66` | `def test_register_loot_event_dedupes_and_rejects_traversal(tmp_path)` |
| `update_from_findings` | method | `tests/test_c2_surfaces.py:104` | `def update_from_findings(self, findings)` |
| `TestCampaignRoutesThroughHelpers` | class | `tests/test_campaign_import_safety.py:96` | `class TestCampaignRoutesThroughHelpers` |
| `TestColumnFiltering` | class | `tests/test_campaign_import_safety.py:55` | `class TestColumnFiltering` |
| `TestCopyTree` | class | `tests/test_campaign_import_safety.py:80` | `class TestCopyTree` |
| `TestZipSlip` | class | `tests/test_campaign_import_safety.py:35` | `class TestZipSlip` |
| `_make_evil_zip` | function | `tests/test_campaign_import_safety.py:27` | `def _make_evil_zip(path)` |
| `test_evil_members_skipped` | method | `tests/test_campaign_import_safety.py:36` | `def test_evil_members_skipped(self, tmp_path)` |
| `test_filtered_insert_roundtrip` | method | `tests/test_campaign_import_safety.py:70` | `def test_filtered_insert_roundtrip(self, tmp_path)` |
| `test_identifier_policy` | method | `tests/test_campaign_import_safety.py:56` | `def test_identifier_policy(self)` |
| `test_legit_tree_extracted` | method | `tests/test_campaign_import_safety.py:46` | `def test_legit_tree_extracted(self, tmp_path)` |
| `test_no_raw_extractall_on_import` | method | `tests/test_campaign_import_safety.py:97` | `def test_no_raw_extractall_on_import(self)` |
| `test_order_preserved` | method | `tests/test_campaign_import_safety.py:67` | `def test_order_preserved(self)` |
| `test_symlinks_not_followed` | method | `tests/test_campaign_import_safety.py:81` | `def test_symlinks_not_followed(self, tmp_path)` |
| `test_unknown_and_hostile_dropped` | method | `tests/test_campaign_import_safety.py:62` | `def test_unknown_and_hostile_dropped(self)` |
| `test_uses_safe_helpers` | method | `tests/test_campaign_import_safety.py:108` | `def test_uses_safe_helpers(self)` |
| `TestAllCategories` | class | `tests/test_categories.py:154` | `class TestAllCategories` |
| `TestBijectionInvariant` | class | `tests/test_categories.py:172` | `class TestBijectionInvariant` |
| `TestCategoryConstants` | class | `tests/test_categories.py:28` | `class TestCategoryConstants` |
| `TestCategoryToShort` | class | `tests/test_categories.py:128` | `class TestCategoryToShort` |
| `TestShortToCategory` | class | `tests/test_categories.py:78` | `class TestShortToCategory` |
| `test_ai_to_category` | method | `tests/test_categories.py:118` | `def test_ai_to_category(self)` |
| `test_all_ai_values` | method | `tests/test_categories.py:68` | `def test_all_ai_values(self)` |
| `test_all_c2_values` | method | `tests/test_categories.py:56` | `def test_all_c2_values(self)` |
| `test_all_categories_count` | method | `tests/test_categories.py:168` | `def test_all_categories_count(self)` |
| `test_all_categories_non_empty` | method | `tests/test_categories.py:161` | `def test_all_categories_non_empty(self)` |
| `test_all_cloud_values` | method | `tests/test_categories.py:71` | `def test_all_cloud_values(self)` |
| `test_all_container_values` | method | `tests/test_categories.py:74` | `def test_all_container_values(self)` |
| `test_all_cred_access_values` | method | `tests/test_categories.py:47` | `def test_all_cred_access_values(self)` |
| `test_all_exfil_values` | method | `tests/test_categories.py:53` | `def test_all_exfil_values(self)` |
| `test_all_exploitation_values` | method | `tests/test_categories.py:35` | `def test_all_exploitation_values(self)` |
| `test_all_lateral_values` | method | `tests/test_categories.py:50` | `def test_all_lateral_values(self)` |
| `test_all_lua_values` | method | `tests/test_categories.py:65` | `def test_all_lua_values(self)` |
| `test_all_misc_values` | method | `tests/test_categories.py:62` | `def test_all_misc_values(self)` |
| `test_all_persistence_values` | method | `tests/test_categories.py:41` | `def test_all_persistence_values(self)` |
| `test_all_post_exploitation_values` | method | `tests/test_categories.py:38` | `def test_all_post_exploitation_values(self)` |
| `test_all_privesc_values` | method | `tests/test_categories.py:44` | `def test_all_privesc_values(self)` |
| `test_all_recon_values` | method | `tests/test_categories.py:29` | `def test_all_recon_values(self)` |
| `test_all_reporting_values` | method | `tests/test_categories.py:59` | `def test_all_reporting_values(self)` |
| `test_all_scanning_values` | method | `tests/test_categories.py:32` | `def test_all_scanning_values(self)` |
| `test_c2_reverse_lookup` | method | `tests/test_categories.py:138` | `def test_c2_reverse_lookup(self)` |
| `test_c2_to_category` | method | `tests/test_categories.py:109` | `def test_c2_to_category(self)` |
| `test_credential_to_category` | method | `tests/test_categories.py:100` | `def test_credential_to_category(self)` |
| `test_enum_to_scanning_category` | method | `tests/test_categories.py:85` | `def test_enum_to_scanning_category(self)` |
| `test_every_short_key_in_all_categories` | method | `tests/test_categories.py:155` | `def test_every_short_key_in_all_categories(self)` |
| `test_exfil_to_category` | method | `tests/test_categories.py:106` | `def test_exfil_to_category(self)` |
| `test_exploit_to_category` | method | `tests/test_categories.py:88` | `def test_exploit_to_category(self)` |
| `test_exploitation_reverse_lookup` | method | `tests/test_categories.py:132` | `def test_exploitation_reverse_lookup(self)` |
| `test_forward_and_reverse_match` | method | `tests/test_categories.py:173` | `def test_forward_and_reverse_match(self)` |
| `test_lateral_to_category` | method | `tests/test_categories.py:103` | `def test_lateral_to_category(self)` |
| `test_misc_to_category` | method | `tests/test_categories.py:115` | `def test_misc_to_category(self)` |
| `test_no_duplicate_all_categories` | method | `tests/test_categories.py:165` | `def test_no_duplicate_all_categories(self)` |
| `test_persistence_to_category` | method | `tests/test_categories.py:94` | `def test_persistence_to_category(self)` |
| `test_post_to_category` | method | `tests/test_categories.py:91` | `def test_post_to_category(self)` |
| `test_privesc_reverse_lookup` | method | `tests/test_categories.py:135` | `def test_privesc_reverse_lookup(self)` |
| `test_privesc_to_category` | method | `tests/test_categories.py:97` | `def test_privesc_to_category(self)` |
| `test_recon_reverse_lookup` | method | `tests/test_categories.py:129` | `def test_recon_reverse_lookup(self)` |
| `test_recon_to_category` | method | `tests/test_categories.py:79` | `def test_recon_to_category(self)` |
| `test_reporting_to_category` | method | `tests/test_categories.py:112` | `def test_reporting_to_category(self)` |
| `test_reverse_lookup_less_than_or_equal_forward` | method | `tests/test_categories.py:150` | `def test_reverse_lookup_less_than_or_equal_forward(self)` |
| `test_reverse_lookup_roundtrip` | method | `tests/test_categories.py:141` | `def test_reverse_lookup_roundtrip(self)` |
| `test_scanning_to_category` | method | `tests/test_categories.py:82` | `def test_scanning_to_category(self)` |
| `test_unknown_short_name_raises_key_error` | method | `tests/test_categories.py:121` | `def test_unknown_short_name_raises_key_error(self)` |
| `BackendSelection` | class | `tests/test_chain_approval_c2.py:128` | `class BackendSelection(TestCase)` |
| `C2Approver` | class | `tests/test_chain_approval_c2.py:73` | `class C2Approver(TestCase)` |
| `C2ChainApprovalEndpoints` | class | `tests/test_chain_approval_c2.py:155` | `class C2ChainApprovalEndpoints(TestCase)` |
| `Directive` | class | `tests/test_chain_approval_c2.py:147` | `class Directive(TestCase)` |
| `StoreLifecycle` | class | `tests/test_chain_approval_c2.py:25` | `class StoreLifecycle(TestCase)` |
| `_server` | method | `tests/test_chain_approval_c2.py:161` | `def _server(cls)` |
| `decide_later` | function | `tests/test_chain_approval_c2.py:82` | `def decide_later()` |
| `deny_later` | function | `tests/test_chain_approval_c2.py:97` | `def deny_later()` |
| `fast_clock` | function | `tests/test_chain_approval_c2.py:111` | `def fast_clock()` |
| `setUp` | method | `tests/test_chain_approval_c2.py:28` | `def setUp(self)` |
| `setUp` | method | `tests/test_chain_approval_c2.py:76` | `def setUp(self)` |
| `setUp` | method | `tests/test_chain_approval_c2.py:178` | `def setUp(self)` |
| `test_approve_after_c2_decision` | method | `tests/test_chain_approval_c2.py:79` | `def test_approve_after_c2_decision(self)` |
| `test_audit_trail_written` | method | `tests/test_chain_approval_c2.py:63` | `def test_audit_trail_written(self)` |
| `test_c2_selected` | method | `tests/test_chain_approval_c2.py:136` | `def test_c2_selected(self)` |
| `test_create_and_list_roundtrip` | method | `tests/test_chain_approval_c2.py:31` | `def test_create_and_list_roundtrip(self)` |
| `test_deadline_expiry_denies` | method | `tests/test_chain_approval_c2.py:108` | `def test_deadline_expiry_denies(self)` |
| `test_decision_records_and_dedupes` | method | `tests/test_chain_approval_c2.py:42` | `def test_decision_records_and_dedupes(self)` |
| `test_default_cli` | method | `tests/test_chain_approval_c2.py:131` | `def test_default_cli(self)` |
| `test_deny_votes_false` | method | `tests/test_chain_approval_c2.py:94` | `def test_deny_votes_false(self)` |
| `test_expire_stale_sweeps_only_past_deadline` | method | `tests/test_chain_approval_c2.py:55` | `def test_expire_stale_sweeps_only_past_deadline(self)` |
| `test_filenames` | method | `tests/test_chain_approval_c2.py:150` | `def test_filenames(self)` |
| `test_list_filter_and_decide_roundtrip` | method | `tests/test_chain_approval_c2.py:197` | `def test_list_filter_and_decide_roundtrip(self)` |
| `test_list_shape` | method | `tests/test_chain_approval_c2.py:190` | `def test_list_shape(self)` |
| `test_store_failure_denies` | method | `tests/test_chain_approval_c2.py:122` | `def test_store_failure_denies(self)` |
| `test_timeout_clamped` | method | `tests/test_chain_approval_c2.py:140` | `def test_timeout_clamped(self)` |
| `test_unknown_and_already_decided_failures` | method | `tests/test_chain_approval_c2.py:50` | `def test_unknown_and_already_decided_failures(self)` |
| `TestCliApprovalBackendWiring` | class | `tests/test_chain_approval_cli_wiring.py:14` | `class TestCliApprovalBackendWiring` |
| `test_c2_approver_importable_from_support` | method | `tests/test_chain_approval_cli_wiring.py:15` | `def test_c2_approver_importable_from_support(self)` |
| `TestBuild` | class | `tests/test_chain_distill.py:167` | `class TestBuild` |
| `TestInferTarget` | class | `tests/test_chain_distill.py:150` | `class TestInferTarget` |
| `TestLocate` | class | `tests/test_chain_distill.py:133` | `class TestLocate` |
| `TestWrite` | class | `tests/test_chain_distill.py:232` | `class TestWrite` |
| `report_checks` | method | `tests/test_chain_distill.py:213` | `def report_checks(self, trace_dir)` |
| `test_empty_trace_yields_validateable_chain` | method | `tests/test_chain_distill.py:220` | `def test_empty_trace_yields_validateable_chain(self, tmp_path)` |
| `test_exploit_steps_strict` | method | `tests/test_chain_distill.py:204` | `def test_exploit_steps_strict(self, trace_dir)` |
| `test_frequency_fallback_hosts_win_over_loopback` | method | `tests/test_chain_distill.py:161` | `def test_frequency_fallback_hosts_win_over_loopback(self, tmp_path)` |
| `test_goal_beats_frequency` | method | `tests/test_chain_distill.py:153` | `def test_goal_beats_frequency(self, trace_dir)` |
| `test_keep_drop_dedupe` | method | `tests/test_chain_distill.py:170` | `def test_keep_drop_dedupe(self, trace_dir)` |
| `test_pair_found` | method | `tests/test_chain_distill.py:136` | `def test_pair_found(self, trace_dir)` |
| `test_target_tokenised_and_lineage_kept` | method | `tests/test_chain_distill.py:186` | `def test_target_tokenised_and_lineage_kept(self, trace_dir)` |
| `test_unknown_task_is_none` | method | `tests/test_chain_distill.py:142` | `def test_unknown_task_is_none(self, trace_dir)` |
| `test_written_chain_validates_lifetime` | method | `tests/test_chain_distill.py:235` | `def test_written_chain_validates_lifetime(self, trace_dir)` |
| `trace_dir` | function | `tests/test_chain_distill.py:22` | `def trace_dir(tmp_path)` |
| `_pinned_step` | function | `tests/test_chain_distill_custody.py:28` | `def _pinned_step(digest)` |
| `_write_artifact` | function | `tests/test_chain_distill_custody.py:20` | `def _write_artifact(sessions_dir, name, payload)` |
| `test_build_chain_data_attaches_evidence_pins` | function | `tests/test_chain_distill_custody.py:71` | `def test_build_chain_data_attaches_evidence_pins(tmp_path, monkeypatch)` |
| `test_missing_and_oversized_artifacts_are_skipped` | function | `tests/test_chain_distill_custody.py:62` | `def test_missing_and_oversized_artifacts_are_skipped(tmp_path, monkeypatch)` |
| `test_pins_hash_referenced_session_artifacts` | function | `tests/test_chain_distill_custody.py:38` | `def test_pins_hash_referenced_session_artifacts(tmp_path, monkeypatch)` |
| `test_pins_tokenized_paths_resolve_target` | function | `tests/test_chain_distill_custody.py:50` | `def test_pins_tokenized_paths_resolve_target(tmp_path, monkeypatch)` |
| `test_verify_rejects_tampered_evidence_at_replay` | function | `tests/test_chain_distill_custody.py:95` | `def test_verify_rejects_tampered_evidence_at_replay(tmp_path, monkeypatch)` |
| `test_infer_target_defers_denylist_load` | function | `tests/test_chain_distill_scope.py:55` | `def test_infer_target_defers_denylist_load(tmp_path, monkeypatch)` |
| `test_infer_target_respects_operator_deny` | function | `tests/test_chain_distill_scope.py:40` | `def test_infer_target_respects_operator_deny(tmp_path)` |
| `test_lookalikes_still_candidates` | function | `tests/test_chain_distill_scope.py:22` | `def test_lookalikes_still_candidates()` |
| `test_operator_denylist_excludes_label_tree` | function | `tests/test_chain_distill_scope.py:28` | `def test_operator_denylist_excludes_label_tree(tmp_path)` |
| `test_reserved_documentation_domains_excluded` | function | `tests/test_chain_distill_scope.py:15` | `def test_reserved_documentation_domains_excluded()` |
| `_Runner` | class | `tests/test_chain_evidence.py:63` | `class _Runner(ChainRunner)` |
| `_Runner` | class | `tests/test_chain_evidence.py:90` | `class _Runner(ChainRunner)` |
| `_Runner` | class | `tests/test_chain_evidence.py:108` | `class _Runner(ChainRunner)` |
| `_Runner` | class | `tests/test_chain_evidence.py:127` | `class _Runner(ChainRunner)` |
| `_Runner` | class | `tests/test_chain_evidence.py:146` | `class _Runner(ChainRunner)` |
| `_Runner` | class | `tests/test_chain_evidence.py:170` | `class _Runner(ChainRunner)` |
| `_Runner` | class | `tests/test_chain_evidence.py:185` | `class _Runner(ChainRunner)` |
| `_Runner` | class | `tests/test_chain_evidence.py:203` | `class _Runner(ChainRunner)` |
| `_chain` | function | `tests/test_chain_evidence.py:19` | `def _chain(tmp_path, steps, name)` |
| `_execute` | method | `tests/test_chain_evidence.py:64` | `def _execute(self, command, timeout, expect_exits)` |
| `_execute` | method | `tests/test_chain_evidence.py:91` | `def _execute(self, command, timeout, expect_exits)` |
| `_execute` | method | `tests/test_chain_evidence.py:109` | `def _execute(self, command, timeout, expect_exits)` |
| `_execute` | method | `tests/test_chain_evidence.py:128` | `def _execute(self, command, timeout, expect_exits)` |
| `_execute` | method | `tests/test_chain_evidence.py:147` | `def _execute(self, command, timeout, expect_exits)` |
| `_execute` | method | `tests/test_chain_evidence.py:171` | `def _execute(self, command, timeout, expect_exits)` |
| `_execute` | method | `tests/test_chain_evidence.py:186` | `def _execute(self, command, timeout, expect_exits)` |
| `_execute` | method | `tests/test_chain_evidence.py:204` | `def _execute(self, command, timeout, expect_exits)` |
| `_load` | function | `tests/test_chain_evidence.py:25` | `def _load(document, tmp_path)` |
| `test_budget_caps_attempts` | function | `tests/test_chain_evidence.py:162` | `def test_budget_caps_attempts(tmp_path)` |
| `test_budget_seconds_caps_timeout` | function | `tests/test_chain_evidence.py:181` | `def test_budget_seconds_caps_timeout(tmp_path)` |
| `test_dependency_gate_passes_when_observed` | function | `tests/test_chain_evidence.py:78` | `def test_dependency_gate_passes_when_observed(tmp_path)` |
| `test_dependency_gate_skips_unproven_chain` | function | `tests/test_chain_evidence.py:53` | `def test_dependency_gate_skips_unproven_chain(tmp_path)` |
| `test_evidence_sha256_pin` | function | `tests/test_chain_evidence.py:135` | `def test_evidence_sha256_pin(tmp_path)` |
| `test_legacy_chains_unchanged` | function | `tests/test_chain_evidence.py:196` | `def test_legacy_chains_unchanged(tmp_path)` |
| `test_missing_required_field_is_insufficient` | function | `tests/test_chain_evidence.py:118` | `def test_missing_required_field_is_insufficient(tmp_path)` |
| `test_observed_verdict_on_success_with_fields` | function | `tests/test_chain_evidence.py:99` | `def test_observed_verdict_on_success_with_fields(tmp_path)` |
| `test_validate_hunting_fields` | function | `tests/test_chain_evidence.py:29` | `def test_validate_hunting_fields()` |
| `test_default_registry_uses_store_path` | function | `tests/test_chain_family.py:72` | `def test_default_registry_uses_store_path(tmp_path, monkeypatch)` |
| `test_empty_services_is_the_empty_family` | function | `tests/test_chain_family.py:35` | `def test_empty_services_is_the_empty_family()` |
| `test_registry_empty_family_is_never_recorded` | function | `tests/test_chain_family.py:54` | `def test_registry_empty_family_is_never_recorded(tmp_path)` |
| `test_registry_ranks_proven_chain_over_associated` | function | `tests/test_chain_family.py:40` | `def test_registry_ranks_proven_chain_over_associated(tmp_path)` |
| `test_signature_collapses_known_service_aliases` | function | `tests/test_chain_family.py:21` | `def test_signature_collapses_known_service_aliases()` |
| `test_signature_distinguishes_os_and_creds` | function | `tests/test_chain_family.py:28` | `def test_signature_distinguishes_os_and_creds()` |
| `test_signature_ignores_service_order_and_duplicates` | function | `tests/test_chain_family.py:14` | `def test_signature_ignores_service_order_and_duplicates()` |
| `test_transfer_note_surfaces_known_chain` | function | `tests/test_chain_family.py:61` | `def test_transfer_note_surfaces_known_chain(tmp_path)` |
| `_chain` | function | `tests/test_chain_finalizer.py:21` | `def _chain(steps)` |
| `executor` | function | `tests/test_chain_finalizer.py:53` | `def executor(command)` |
| `executor` | function | `tests/test_chain_finalizer.py:86` | `def executor(command)` |
| `test_chain_ok_without_evidence_is_downgraded` | function | `tests/test_chain_finalizer.py:39` | `def test_chain_ok_without_evidence_is_downgraded()` |
| `test_chain_with_captured_evidence_is_verified` | function | `tests/test_chain_finalizer.py:26` | `def test_chain_with_captured_evidence_is_verified()` |
| `test_chain_with_open_steps_reports_pending_reason` | function | `tests/test_chain_finalizer.py:49` | `def test_chain_with_open_steps_reports_pending_reason()` |
| `test_dry_run_has_no_finalization` | function | `tests/test_chain_finalizer.py:71` | `def test_dry_run_has_no_finalization()` |
| `test_hunting_verdicts_count_as_confirmed` | function | `tests/test_chain_finalizer.py:80` | `def test_hunting_verdicts_count_as_confirmed(tmp_path)` |
| `_file` | function | `tests/test_chain_freshness_guard.py:18` | `def _file(path, payload, mtime)` |
| `executor` | function | `tests/test_chain_freshness_guard.py:73` | `def executor(command)` |
| `executor` | function | `tests/test_chain_freshness_guard.py:94` | `def executor(command)` |
| `test_missing_artifact_runs` | function | `tests/test_chain_freshness_guard.py:40` | `def test_missing_artifact_runs(tmp_path)` |
| `test_runner_reexecutes_stale_step` | function | `tests/test_chain_freshness_guard.py:68` | `def test_runner_reexecutes_stale_step(tmp_path)` |
| `test_runner_skips_fresh_step` | function | `tests/test_chain_freshness_guard.py:89` | `def test_runner_skips_fresh_step(tmp_path)` |
| `test_schema_validates_skip_max_age` | function | `tests/test_chain_freshness_guard.py:45` | `def test_schema_validates_skip_max_age()` |
| `test_skip_pending_fresh_and_forever` | function | `tests/test_chain_freshness_guard.py:26` | `def test_skip_pending_fresh_and_forever(tmp_path)` |
| `test_skip_pending_stale_artifact_runs` | function | `tests/test_chain_freshness_guard.py:33` | `def test_skip_pending_stale_artifact_runs(tmp_path)` |
| `test_chain_list_filters` | function | `tests/test_chain_list_command.py:22` | `def test_chain_list_filters(capsys)` |
| `test_chain_list_lists_registry` | function | `tests/test_chain_list_command.py:12` | `def test_chain_list_lists_registry(capsys)` |
| `FakeActivity` | class | `tests/test_chain_loop.py:21` | `class FakeActivity` |
| `FakeWorker` | class | `tests/test_chain_loop.py:29` | `class FakeWorker` |
| `__init__` | method | `tests/test_chain_loop.py:22` | `def __init__(self)` |
| `__init__` | method | `tests/test_chain_loop.py:33` | `def __init__(self, statuses)` |
| `_chain` | function | `tests/test_chain_loop.py:53` | `def _chain()` |
| `_guard_step` | method | `tests/test_chain_loop.py:41` | `def _guard_step(self, intent, command, executor, budget, intercept, retry_state)` |
| `_intent` | function | `tests/test_chain_loop.py:49` | `def _intent()` |
| `_patch_chain` | function | `tests/test_chain_loop.py:64` | `def _patch_chain(monkeypatch, chain, name)` |
| `_routable_true` | function | `tests/test_chain_loop.py:68` | `def _routable_true(monkeypatch)` |
| `_target_for` | method | `tests/test_chain_loop.py:38` | `def _target_for(self, intent)` |
| `emit` | method | `tests/test_chain_loop.py:25` | `def emit(self, name, kind, message)` |
| `spy_runner` | function | `tests/test_chain_loop.py:188` | `def spy_runner(chain, guarded, tokens, total_timeout, run_id, worker, intent)` |
| `test_chain_step_blocked_carries_status_and_detail` | function | `tests/test_chain_loop.py:173` | `def test_chain_step_blocked_carries_status_and_detail()` |
| `test_parse_chain_invocation_splits_name_target_vars` | function | `tests/test_chain_loop.py:72` | `def test_parse_chain_invocation_splits_name_target_vars()` |
| `test_run_chain_stepwise_auto_mode_skips_ineligible` | function | `tests/test_chain_loop.py:121` | `def test_run_chain_stepwise_auto_mode_skips_ineligible(monkeypatch)` |
| `test_run_chain_stepwise_forced_blocks_ineligible` | function | `tests/test_chain_loop.py:129` | `def test_run_chain_stepwise_forced_blocks_ineligible(monkeypatch)` |
| `test_run_chain_stepwise_guard_block_aborts_chain` | function | `tests/test_chain_loop.py:140` | `def test_run_chain_stepwise_guard_block_aborts_chain(monkeypatch)` |
| `test_run_chain_stepwise_nesting_limit_blocks` | function | `tests/test_chain_loop.py:162` | `def test_run_chain_stepwise_nesting_limit_blocks(monkeypatch)` |
| `test_run_chain_stepwise_routes_every_step_through_guard` | function | `tests/test_chain_loop.py:93` | `def test_run_chain_stepwise_routes_every_step_through_guard(monkeypatch)` |
| `test_run_chain_stepwise_subprocess_mode_falls_through` | function | `tests/test_chain_loop.py:112` | `def test_run_chain_stepwise_subprocess_mode_falls_through(monkeypatch)` |
| `test_run_chain_stepwise_unknown_chain_falls_through` | function | `tests/test_chain_loop.py:155` | `def test_run_chain_stepwise_unknown_chain_falls_through(monkeypatch)` |
| `test_run_chain_stepwise_worker_target_used_when_unset` | function | `tests/test_chain_loop.py:180` | `def test_run_chain_stepwise_worker_target_used_when_unset(monkeypatch)` |
| `test_stepwise_eligible_reports_unroutable_steps` | function | `tests/test_chain_loop.py:81` | `def test_stepwise_eligible_reports_unroutable_steps()` |
| `_Boom` | class | `tests/test_chain_match_determinism.py:50` | `class _Boom` |
| `_Pick` | class | `tests/test_chain_match_determinism.py:68` | `class _Pick` |
| `_Quiet` | class | `tests/test_chain_match_determinism.py:59` | `class _Quiet` |
| `_rows` | function | `tests/test_chain_match_determinism.py:19` | `def _rows(names)` |
| `propose` | method | `tests/test_chain_match_determinism.py:55` | `def propose(self, ctx)` |
| `propose` | method | `tests/test_chain_match_determinism.py:64` | `def propose(self, ctx)` |
| `propose` | method | `tests/test_chain_match_determinism.py:73` | `def propose(self, ctx)` |
| `test_clean_abstention_emits_no_warning` | function | `tests/test_chain_match_determinism.py:85` | `def test_clean_abstention_emits_no_warning(caplog)` |
| `test_crashing_selector_is_abstention_but_logged` | function | `tests/test_chain_match_determinism.py:77` | `def test_crashing_selector_is_abstention_but_logged(caplog)` |
| `test_excluded_chain_is_skipped_deterministically` | function | `tests/test_chain_match_determinism.py:41` | `def test_excluded_chain_is_skipped_deterministically()` |
| `test_higher_score_still_wins_over_name_order` | function | `tests/test_chain_match_determinism.py:32` | `def test_higher_score_still_wins_over_name_order()` |
| `test_no_service_match_returns_none` | function | `tests/test_chain_match_determinism.py:46` | `def test_no_service_match_returns_none()` |
| `test_tie_break_is_name_ascending_regardless_of_order` | function | `tests/test_chain_match_determinism.py:24` | `def test_tie_break_is_name_ascending_regardless_of_order()` |
| `_Step` | class | `tests/test_chain_mode.py:36` | `class _Step` |
| `__init__` | method | `tests/test_chain_mode.py:39` | `def __init__(self, name, source, reason)` |
| `_engine` | function | `tests/test_chain_mode.py:52` | `def _engine(resolver)` |
| `_resolver` | function | `tests/test_chain_mode.py:45` | `def _resolver()` |
| `broken` | function | `tests/test_chain_mode.py:212` | `def broken(cmd, phase)` |
| `fake_input` | function | `tests/test_chain_mode.py:63` | `def fake_input(prompt)` |
| `raise_ki` | function | `tests/test_chain_mode.py:179` | `def raise_ki(prompt)` |
| `resolve` | function | `tests/test_chain_mode.py:46` | `def resolve(cmd, phase)` |
| `test_auto_pause_after_max_steps` | function | `tests/test_chain_mode.py:195` | `def test_auto_pause_after_max_steps(tmp_path)` |
| `test_engine_reads_persisted_state` | function | `tests/test_chain_mode.py:239` | `def test_engine_reads_persisted_state(tmp_path)` |
| `test_enter_runs_top_suggestion` | function | `tests/test_chain_mode.py:106` | `def test_enter_runs_top_suggestion()` |
| `test_exit_words_disable_chain_mode` | function | `tests/test_chain_mode.py:144` | `def test_exit_words_disable_chain_mode(word)` |
| `test_invalid_number_re_prompts_then_accepts_valid_pick` | function | `tests/test_chain_mode.py:168` | `def test_invalid_number_re_prompts_then_accepts_valid_pick()` |
| `test_invalid_number_re_prompts_then_skips` | function | `tests/test_chain_mode.py:160` | `def test_invalid_number_re_prompts_then_skips()` |
| `test_keyboard_interrupt_disables` | function | `tests/test_chain_mode.py:178` | `def test_keyboard_interrupt_disables(tmp_path)` |
| `test_no_suggestions_enter_skips_custom_command_runs` | function | `tests/test_chain_mode.py:151` | `def test_no_suggestions_enter_skips_custom_command_runs()` |
| `test_number_selects_ranked_alternative` | function | `tests/test_chain_mode.py:116` | `def test_number_selects_ranked_alternative()` |
| `test_override_runs_operator_command` | function | `tests/test_chain_mode.py:126` | `def test_override_runs_operator_command()` |
| `test_persist_toggle_writes_state_file` | function | `tests/test_chain_mode.py:252` | `def test_persist_toggle_writes_state_file(tmp_path)` |
| `test_prompt_exit_words_persist_off` | function | `tests/test_chain_mode.py:267` | `def test_prompt_exit_words_persist_off(tmp_path)` |
| `test_resolver_failure_degrades_to_no_suggestions` | function | `tests/test_chain_mode.py:211` | `def test_resolver_failure_degrades_to_no_suggestions()` |
| `test_skip_keeps_chain_mode_enabled` | function | `tests/test_chain_mode.py:136` | `def test_skip_keeps_chain_mode_enabled()` |
| `test_step_none_for_skip_verbs` | function | `tests/test_chain_mode.py:101` | `def test_step_none_for_skip_verbs(verb)` |
| `test_step_none_when_disabled` | function | `tests/test_chain_mode.py:90` | `def test_step_none_when_disabled()` |
| `test_step_none_when_not_interactive` | function | `tests/test_chain_mode.py:95` | `def test_step_none_when_not_interactive()` |
| `test_store_roundtrip_and_missing` | function | `tests/test_chain_mode.py:221` | `def test_store_roundtrip_and_missing(tmp_path)` |
| `test_store_survives_malformed_file` | function | `tests/test_chain_mode.py:230` | `def test_store_survives_malformed_file(tmp_path)` |
| `test_suggestion_from_step_and_string` | function | `tests/test_chain_mode.py:85` | `def test_suggestion_from_step_and_string()` |
| `_SlowFirst` | class | `tests/test_chain_parallel_fallback.py:48` | `class _SlowFirst` |
| `__call__` | method | `tests/test_chain_parallel_fallback.py:51` | `def __call__(self, command)` |
| `_chain` | function | `tests/test_chain_parallel_fallback.py:16` | `def _chain(steps)` |
| `_run` | function | `tests/test_chain_parallel_fallback.py:60` | `def _run()` |
| `executor` | function | `tests/test_chain_parallel_fallback.py:29` | `def executor(command)` |
| `executor` | function | `tests/test_chain_parallel_fallback.py:84` | `def executor(command)` |
| `executor` | function | `tests/test_chain_parallel_fallback.py:108` | `def executor(command)` |
| `executor` | function | `tests/test_chain_parallel_fallback.py:131` | `def executor(command)` |
| `executor` | function | `tests/test_chain_parallel_fallback.py:154` | `def executor(command)` |
| `executor` | function | `tests/test_chain_parallel_fallback.py:169` | `def executor(command)` |
| `executor` | function | `tests/test_chain_parallel_fallback.py:212` | `def executor(command)` |
| `loader` | function | `tests/test_chain_parallel_fallback.py:180` | `def loader(name)` |
| `loader` | function | `tests/test_chain_parallel_fallback.py:197` | `def loader(name)` |
| `loader` | function | `tests/test_chain_parallel_fallback.py:220` | `def loader(name)` |
| `test_dry_run_treats_parallel_steps_sequentially` | function | `tests/test_chain_parallel_fallback.py:274` | `def test_dry_run_treats_parallel_steps_sequentially()` |
| `test_fallback_chain_runs_on_failure` | function | `tests/test_chain_parallel_fallback.py:165` | `def test_fallback_chain_runs_on_failure()` |
| `test_fallback_depth_is_capped` | function | `tests/test_chain_parallel_fallback.py:208` | `def test_fallback_depth_is_capped()` |
| `test_fallback_skipped_when_primary_succeeds` | function | `tests/test_chain_parallel_fallback.py:192` | `def test_fallback_skipped_when_primary_succeeds()` |
| `test_parallel_failure_with_continue_keeps_going` | function | `tests/test_chain_parallel_fallback.py:103` | `def test_parallel_failure_with_continue_keeps_going()` |
| `test_parallel_failure_without_continue_aborts` | function | `tests/test_chain_parallel_fallback.py:79` | `def test_parallel_failure_without_continue_aborts()` |
| `test_parallel_steps_execute_concurrently` | function | `tests/test_chain_parallel_fallback.py:21` | `def test_parallel_steps_execute_concurrently()` |
| `test_pre_check_failure_skips_step` | function | `tests/test_chain_parallel_fallback.py:126` | `def test_pre_check_failure_skips_step()` |
| `test_pre_check_success_executes_step` | function | `tests/test_chain_parallel_fallback.py:150` | `def test_pre_check_success_executes_step()` |
| `test_registry_parses_parallel_and_pre_check` | function | `tests/test_chain_parallel_fallback.py:257` | `def test_registry_parses_parallel_and_pre_check()` |
| `test_registry_validation_rejects_parallel_with_capture` | function | `tests/test_chain_parallel_fallback.py:230` | `def test_registry_validation_rejects_parallel_with_capture()` |
| `test_registry_validation_rejects_unknown_fallback` | function | `tests/test_chain_parallel_fallback.py:241` | `def test_registry_validation_rejects_unknown_fallback()` |
| `test_chain_yaml_matches_skill_contract` | function | `tests/test_chain_registry.py:73` | `def test_chain_yaml_matches_skill_contract()` |
| `test_disabled_chains_skip_but_stay_visible` | function | `tests/test_chain_registry.py:124` | `def test_disabled_chains_skip_but_stay_visible(tmp_path)` |
| `test_extends_cycle_and_unknown_parent_rejected` | function | `tests/test_chain_registry.py:110` | `def test_extends_cycle_and_unknown_parent_rejected(tmp_path)` |
| `test_extends_inherits_steps_and_merges_defaults` | function | `tests/test_chain_registry.py:80` | `def test_extends_inherits_steps_and_merges_defaults(tmp_path)` |
| `test_generate_for_playbook_roundtrip` | function | `tests/test_chain_registry.py:143` | `def test_generate_for_playbook_roundtrip(tmp_path)` |
| `test_resolve_flags_unresolved_tokens` | function | `tests/test_chain_registry.py:65` | `def test_resolve_flags_unresolved_tokens()` |
| `test_resolve_substitutes_and_skips` | function | `tests/test_chain_registry.py:43` | `def test_resolve_substitutes_and_skips(tmp_path, monkeypatch)` |
| `test_shipped_chain_loads` | function | `tests/test_chain_registry.py:18` | `def test_shipped_chain_loads()` |
| `test_validate_rejects_bad_chains` | function | `tests/test_chain_registry.py:33` | `def test_validate_rejects_bad_chains()` |
| `FakeShell` | class | `tests/test_chain_runner.py:373` | `class FakeShell` |
| `HangingShell` | class | `tests/test_chain_runner.py:274` | `class HangingShell` |
| `Shell` | class | `tests/test_chain_runner.py:224` | `class Shell` |
| `Shell` | class | `tests/test_chain_runner.py:238` | `class Shell` |
| `Shell` | class | `tests/test_chain_runner.py:251` | `class Shell` |
| `Shell` | class | `tests/test_chain_runner.py:301` | `class Shell` |
| `Shell` | class | `tests/test_chain_runner.py:314` | `class Shell` |
| `_chain` | function | `tests/test_chain_runner.py:16` | `def _chain(steps)` |
| `_drive` | function | `tests/test_chain_runner.py:288` | `def _drive()` |
| `do_assign` | method | `tests/test_chain_runner.py:254` | `def do_assign(self, line)` |
| `do_assign` | method | `tests/test_chain_runner.py:317` | `def do_assign(self, line)` |
| `do_echo` | method | `tests/test_chain_runner.py:227` | `def do_echo(self, line)` |
| `do_hang` | method | `tests/test_chain_runner.py:277` | `def do_hang(self, line)` |
| `do_lazy_note` | method | `tests/test_chain_runner.py:376` | `def do_lazy_note(self, line)` |
| `executor` | function | `tests/test_chain_runner.py:39` | `def executor(command)` |
| `executor` | function | `tests/test_chain_runner.py:62` | `def executor(command)` |
| `executor` | function | `tests/test_chain_runner.py:79` | `def executor(command)` |
| `executor` | function | `tests/test_chain_runner.py:101` | `def executor(command)` |
| `executor` | function | `tests/test_chain_runner.py:135` | `def executor(command)` |
| `executor` | function | `tests/test_chain_runner.py:357` | `def executor(command)` |
| `executor` | function | `tests/test_chain_runner.py:401` | `def executor(command)` |
| `executor` | function | `tests/test_chain_runner.py:415` | `def executor(command)` |
| `onecmd` | method | `tests/test_chain_runner.py:257` | `def onecmd(self, command)` |
| `onecmd` | method | `tests/test_chain_runner.py:281` | `def onecmd(self, command)` |
| `onecmd` | method | `tests/test_chain_runner.py:320` | `def onecmd(self, command)` |
| `onecmd` | method | `tests/test_chain_runner.py:379` | `def onecmd(self, command)` |
| `test_runner_aborts_unless_continue_on_error` | function | `tests/test_chain_runner.py:75` | `def test_runner_aborts_unless_continue_on_error()` |
| `test_runner_captures_output_for_later_steps` | function | `tests/test_chain_runner.py:35` | `def test_runner_captures_output_for_later_steps()` |
| `test_runner_captures_verb_stdout` | function | `tests/test_chain_runner.py:371` | `def test_runner_captures_verb_stdout()` |
| `test_runner_continues_when_policy_allows` | function | `tests/test_chain_runner.py:97` | `def test_runner_continues_when_policy_allows()` |
| `test_runner_dry_run_never_executes` | function | `tests/test_chain_runner.py:120` | `def test_runner_dry_run_never_executes()` |
| `test_runner_executes_python_module_commands` | function | `tests/test_chain_runner.py:236` | `def test_runner_executes_python_module_commands()` |
| `test_runner_fails_on_nonzero_exit` | function | `tests/test_chain_runner.py:299` | `def test_runner_fails_on_nonzero_exit()` |
| `test_runner_falls_back_to_os_commands` | function | `tests/test_chain_runner.py:222` | `def test_runner_falls_back_to_os_commands()` |
| `test_runner_keeps_verbs_on_calling_thread` | function | `tests/test_chain_runner.py:247` | `def test_runner_keeps_verbs_on_calling_thread()` |
| `test_runner_quotes_captured_values_in_raw_shell_steps` | function | `tests/test_chain_runner.py:353` | `def test_runner_quotes_captured_values_in_raw_shell_steps()` |
| `test_runner_resolves_newest_and_skip_if_exists` | function | `tests/test_chain_runner.py:153` | `def test_runner_resolves_newest_and_skip_if_exists(tmp_path, monkeypatch)` |
| `test_runner_retries_then_succeeds` | function | `tests/test_chain_runner.py:58` | `def test_runner_retries_then_succeeds()` |
| `test_runner_routes_known_verb_through_shell` | function | `tests/test_chain_runner.py:310` | `def test_runner_routes_known_verb_through_shell()` |
| `test_runner_skips_when_and_unresolved_and_checks_expect` | function | `tests/test_chain_runner.py:131` | `def test_runner_skips_when_and_unresolved_and_checks_expect()` |
| `test_runner_step_sleep_jitter_applies` | function | `tests/test_chain_runner.py:388` | `def test_runner_step_sleep_jitter_applies()` |
| `test_runner_step_sleep_skipped_on_failure` | function | `tests/test_chain_runner.py:410` | `def test_runner_step_sleep_skipped_on_failure()` |
| `test_runner_timeout_marks_step_timeout` | function | `tests/test_chain_runner.py:330` | `def test_runner_timeout_marks_step_timeout()` |
| `test_runner_validate_rejects_parallel_sleep` | function | `tests/test_chain_runner.py:423` | `def test_runner_validate_rejects_parallel_sleep()` |
| `test_runner_verb_timeout_releases_chain_off_main_thread` | function | `tests/test_chain_runner.py:269` | `def test_runner_verb_timeout_releases_chain_off_main_thread()` |
| `test_v2_schema_accepts_policy_and_rejects_bad_values` | function | `tests/test_chain_runner.py:180` | `def test_v2_schema_accepts_policy_and_rejects_bad_values(tmp_path)` |
| `test_validate_rejects_malformed_when` | function | `tests/test_chain_runner.py:345` | `def test_validate_rejects_malformed_when()` |
| `test_when_evaluator_accepts_list_literals` | function | `tests/test_chain_runner.py:338` | `def test_when_evaluator_accepts_list_literals()` |
| `test_when_evaluator_is_safe_and_expressive` | function | `tests/test_chain_runner.py:21` | `def test_when_evaluator_is_safe_and_expressive()` |
| `_bind_registry` | function | `tests/test_chain_selector.py:49` | `def _bind_registry(monkeypatch, rows)` |
| `_ctx` | function | `tests/test_chain_selector.py:55` | `def _ctx(target, phase, services, os_hint, exclude)` |
| `_rows` | function | `tests/test_chain_selector.py:37` | `def _rows()` |
| `test_disabled_and_invalid_chains_ignored` | function | `tests/test_chain_selector.py:128` | `def test_disabled_and_invalid_chains_ignored(monkeypatch)` |
| `test_each_pair_proposed_once` | function | `tests/test_chain_selector.py:118` | `def test_each_pair_proposed_once(monkeypatch)` |
| `test_lab_chains_allowed_when_flag_set` | function | `tests/test_chain_selector.py:104` | `def test_lab_chains_allowed_when_flag_set(monkeypatch)` |
| `test_lab_chains_excluded_when_flag_off` | function | `tests/test_chain_selector.py:97` | `def test_lab_chains_excluded_when_flag_off(monkeypatch)` |
| `test_master_switch_off_drops_chain_selector` | function | `tests/test_chain_selector.py:138` | `def test_master_switch_off_drops_chain_selector(monkeypatch)` |
| `test_master_switch_on_includes_chain_selector` | function | `tests/test_chain_selector.py:144` | `def test_master_switch_on_includes_chain_selector(monkeypatch)` |
| `test_no_match_returns_none` | function | `tests/test_chain_selector.py:112` | `def test_no_match_returns_none(monkeypatch)` |
| `test_non_strategic_phase_returns_none` | function | `tests/test_chain_selector.py:66` | `def test_non_strategic_phase_returns_none(monkeypatch)` |
| `test_platform_match_for_windows_ad` | function | `tests/test_chain_selector.py:89` | `def test_platform_match_for_windows_ad(monkeypatch)` |
| `test_platform_mismatch_excludes_chain` | function | `tests/test_chain_selector.py:82` | `def test_platform_mismatch_excludes_chain(monkeypatch)` |
| `test_service_match_proposes_apt_chain` | function | `tests/test_chain_selector.py:73` | `def test_service_match_proposes_apt_chain(monkeypatch)` |
| `_capture_events` | function | `tests/test_chain_step_streaming.py:21` | `def _capture_events(monkeypatch)` |
| `_capture_with_sinks` | function | `tests/test_chain_step_streaming.py:202` | `def _capture_with_sinks(monkeypatch)` |
| `_chain` | function | `tests/test_chain_step_streaming.py:16` | `def _chain(steps)` |
| `_chain_steps_for` | function | `tests/test_chain_step_streaming.py:35` | `def _chain_steps_for(captured)` |
| `_failing_executor` | function | `tests/test_chain_step_streaming.py:80` | `def _failing_executor(prefixes)` |
| `boom` | function | `tests/test_chain_step_streaming.py:145` | `def boom(event, sinks)` |
| `execute` | function | `tests/test_chain_step_streaming.py:83` | `def execute(command)` |
| `executor` | function | `tests/test_chain_step_streaming.py:53` | `def executor(command)` |

Next: [SYMBOLS_p39.md](SYMBOLS_p39.md)
