# Symbols (page 40 of 44)
Previous: [SYMBOLS_p39.md](SYMBOLS_p39.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_auth` | function | `tests/test_orchestrator_api.py:43` | `def _auth(token)` |
| `_load` | function | `tests/test_orchestrator_api.py:126` | `def _load()` |
| `_write` | function | `tests/test_orchestrator_api.py:131` | `def _write(payload)` |
| `orchestrator_client` | function | `tests/test_orchestrator_api.py:22` | `def orchestrator_client(tmp_path, monkeypatch)` |
| `test_stage_toggle_round_trip` | function | `tests/test_orchestrator_api.py:116` | `def test_stage_toggle_round_trip(orchestrator_client, monkeypatch, tmp_path)` |
| `test_stage_unknown_rejected` | function | `tests/test_orchestrator_api.py:149` | `def test_stage_unknown_rejected(orchestrator_client)` |
| `test_status_reports_layers` | function | `tests/test_orchestrator_api.py:54` | `def test_status_reports_layers(orchestrator_client)` |
| `test_status_requires_auth` | function | `tests/test_orchestrator_api.py:47` | `def test_status_requires_auth(orchestrator_client)` |
| `test_trigger_crud_round_trip` | function | `tests/test_orchestrator_api.py:160` | `def test_trigger_crud_round_trip(orchestrator_client)` |
| `test_trigger_unknown_kind_rejected` | function | `tests/test_orchestrator_api.py:179` | `def test_trigger_unknown_kind_rejected(orchestrator_client)` |
| `test_verb_toggle_round_trip` | function | `tests/test_orchestrator_api.py:67` | `def test_verb_toggle_round_trip(orchestrator_client, tmp_path, monkeypatch)` |
| `test_verb_toggle_unknown_command_rejected` | function | `tests/test_orchestrator_api.py:97` | `def test_verb_toggle_unknown_command_rejected(orchestrator_client, tmp_path, monkeypatch)` |
| `_drive` | function | `tests/test_orchestrator_triggers.py:34` | `def _drive()` |
| `sandbox` | function | `tests/test_orchestrator_triggers.py:16` | `def sandbox(tmp_path, monkeypatch)` |
| `test_trigger_kind_options_cover_registry` | function | `tests/test_orchestrator_triggers.py:72` | `def test_trigger_kind_options_cover_registry(sandbox)` |
| `test_triggers_add_and_remove_via_app` | function | `tests/test_orchestrator_triggers.py:59` | `def test_triggers_add_and_remove_via_app(sandbox)` |
| `test_triggers_tab_lists_store_rows` | function | `tests/test_orchestrator_triggers.py:25` | `def test_triggers_tab_lists_store_rows(sandbox)` |
| `test_triggers_toggle_persists` | function | `tests/test_orchestrator_triggers.py:45` | `def test_triggers_toggle_persists(sandbox)` |
| `_load` | function | `tests/test_orchestrator_yaml.py:22` | `def _load(target)` |
| `_save` | function | `tests/test_orchestrator_yaml.py:25` | `def _save(data, target)` |
| `payload_store` | function | `tests/test_orchestrator_yaml.py:18` | `def payload_store(monkeypatch)` |
| `test_admin_console_switches_profile` | function | `tests/test_orchestrator_yaml.py:176` | `def test_admin_console_switches_profile(payload_store)` |
| `test_engine_uses_profile_limits` | function | `tests/test_orchestrator_yaml.py:141` | `def test_engine_uses_profile_limits(payload_store, monkeypatch, tmp_path)` |
| `test_payload_profile_overrides_yaml` | function | `tests/test_orchestrator_yaml.py:49` | `def test_payload_profile_overrides_yaml(payload_store)` |
| `test_payload_sink_toggles_override_profile` | function | `tests/test_orchestrator_yaml.py:188` | `def test_payload_sink_toggles_override_profile(payload_store)` |
| `test_profile_inheritance_merges_stages_and_limits` | function | `tests/test_orchestrator_yaml.py:72` | `def test_profile_inheritance_merges_stages_and_limits(payload_store, tmp_path, monkeypatch)` |
| `test_runner_parses_profile_and_resolves_defaults` | function | `tests/test_orchestrator_yaml.py:157` | `def test_runner_parses_profile_and_resolves_defaults(payload_store)` |
| `test_shipped_yaml_declares_required_profiles` | function | `tests/test_orchestrator_yaml.py:39` | `def test_shipped_yaml_declares_required_profiles(payload_store)` |
| `test_stage_params_resolve_and_payload_still_overrides` | function | `tests/test_orchestrator_yaml.py:60` | `def test_stage_params_resolve_and_payload_still_overrides(payload_store)` |
| `test_unknown_profile_is_rejected_and_payload_falls_back` | function | `tests/test_orchestrator_yaml.py:113` | `def test_unknown_profile_is_rejected_and_payload_falls_back(payload_store)` |
| `test_validate_config_rejects_unknown_version_and_bad_stage` | function | `tests/test_orchestrator_yaml.py:124` | `def test_validate_config_rejects_unknown_version_and_bad_stage()` |
| `boom` | function | `tests/test_outcome_bus.py:34` | `def boom(event)` |
| `fake_record` | function | `tests/test_outcome_bus.py:159` | `def fake_record(event, sinks)` |
| `flaky` | function | `tests/test_outcome_bus.py:257` | `def flaky(_event)` |
| `test_attack_graph_sink_writes_summary` | function | `tests/test_outcome_bus.py:141` | `def test_attack_graph_sink_writes_summary(tmp_path, monkeypatch)` |
| `test_bus_fans_out_dedupes_and_audits` | function | `tests/test_outcome_bus.py:15` | `def test_bus_fans_out_dedupes_and_audits(tmp_path)` |
| `test_bus_isolates_sink_failures` | function | `tests/test_outcome_bus.py:32` | `def test_bus_isolates_sink_failures(tmp_path)` |
| `test_bus_respects_sink_toggles` | function | `tests/test_outcome_bus.py:45` | `def test_bus_respects_sink_toggles(monkeypatch, tmp_path)` |
| `test_c2_surface_sink_writes_banner_cve_and_note` | function | `tests/test_outcome_bus.py:74` | `def test_c2_surface_sink_writes_banner_cve_and_note(tmp_path)` |
| `test_concurrent_duplicates_fan_out_once` | function | `tests/test_outcome_bus.py:271` | `def test_concurrent_duplicates_fan_out_once(tmp_path)` |
| `test_dedupe_key_includes_port_and_requested_sinks` | function | `tests/test_outcome_bus.py:237` | `def test_dedupe_key_includes_port_and_requested_sinks(tmp_path)` |
| `test_default_sinks_cover_required_surfaces` | function | `tests/test_outcome_bus.py:58` | `def test_default_sinks_cover_required_surfaces()` |
| `test_intel_graph_sink_writes_summary` | function | `tests/test_outcome_bus.py:132` | `def test_intel_graph_sink_writes_summary(tmp_path)` |
| `test_killchain_sink_only_advances_on_proven_outcomes` | function | `tests/test_outcome_bus.py:201` | `def test_killchain_sink_only_advances_on_proven_outcomes(monkeypatch)` |
| `test_objectives_sink_appends_actionable_finding` | function | `tests/test_outcome_bus.py:102` | `def test_objectives_sink_appends_actionable_finding(tmp_path)` |
| `test_objectives_sink_ignores_failed_and_dry_run` | function | `tests/test_outcome_bus.py:222` | `def test_objectives_sink_ignores_failed_and_dry_run(tmp_path)` |
| `test_record_outcome_builds_one_exploit_event` | function | `tests/test_outcome_bus.py:152` | `def test_record_outcome_builds_one_exploit_event(monkeypatch, tmp_path)` |
| `test_report_sink_only_refreshes_terminal_events` | function | `tests/test_outcome_bus.py:121` | `def test_report_sink_only_refreshes_terminal_events(monkeypatch)` |
| `test_transient_sink_failure_is_retried` | function | `tests/test_outcome_bus.py:252` | `def test_transient_sink_failure_is_retried(tmp_path)` |
| `TestCIWorkflows` | class | `tests/test_packaging.py:242` | `class TestCIWorkflows` |
| `TestConfigDeduplication` | class | `tests/test_packaging.py:39` | `class TestConfigDeduplication` |
| `TestGitIgnore` | class | `tests/test_packaging.py:284` | `class TestGitIgnore` |
| `TestInstallScript` | class | `tests/test_packaging.py:343` | `class TestInstallScript` |
| `TestPreCommitConfig` | class | `tests/test_packaging.py:213` | `class TestPreCommitConfig` |
| `TestPyProjectToml` | class | `tests/test_packaging.py:98` | `class TestPyProjectToml` |
| `TestRequirementsDev` | class | `tests/test_packaging.py:193` | `class TestRequirementsDev` |
| `TestRequirementsLock` | class | `tests/test_packaging.py:303` | `class TestRequirementsLock` |
| `TestSetupPy` | class | `tests/test_packaging.py:154` | `class TestSetupPy` |
| `TestSourceFilesParse` | class | `tests/test_packaging.py:370` | `class TestSourceFilesParse` |
| `_entries` | method | `tests/test_packaging.py:308` | `def _entries(name)` |
| `_load_toml` | function | `tests/test_packaging.py:29` | `def _load_toml(path)` |
| `_load_yaml` | function | `tests/test_packaging.py:34` | `def _load_yaml(path)` |
| `_names` | method | `tests/test_packaging.py:316` | `def _names(entries)` |
| `_read_text` | function | `tests/test_packaging.py:25` | `def _read_text(path)` |
| `_run_in_subprocess` | method | `tests/test_packaging.py:59` | `def _run_in_subprocess(snippet)` |
| `cfg` | method | `tests/test_packaging.py:217` | `def cfg(self)` |
| `deps` | method | `tests/test_packaging.py:197` | `def deps(self)` |
| `lint_wf` | method | `tests/test_packaging.py:246` | `def lint_wf(self)` |
| `patterns` | method | `tests/test_packaging.py:288` | `def patterns(self)` |
| `pyproject` | method | `tests/test_packaging.py:102` | `def pyproject(self)` |
| `security_wf` | method | `tests/test_packaging.py:254` | `def security_wf(self)` |
| `setup_text` | method | `tests/test_packaging.py:167` | `def setup_text(self)` |
| `setup_tree` | method | `tests/test_packaging.py:163` | `def setup_tree(self)` |
| `test_calls_setup` | method | `tests/test_packaging.py:173` | `def test_calls_setup(self, setup_tree)` |
| `test_config_attribute_access_works` | method | `tests/test_packaging.py:74` | `def test_config_attribute_access_works(self)` |
| `test_config_class_defined_exactly_once_in_core` | method | `tests/test_packaging.py:46` | `def test_config_class_defined_exactly_once_in_core(self)` |
| `test_config_class_not_redefined_in_utils` | method | `tests/test_packaging.py:52` | `def test_config_class_not_redefined_in_utils(self)` |
| `test_config_getitem_returns_none_for_missing_key` | method | `tests/test_packaging.py:89` | `def test_config_getitem_returns_none_for_missing_key(self)` |
| `test_config_getitem_returns_value` | method | `tests/test_packaging.py:83` | `def test_config_getitem_returns_value(self)` |
| `test_core_lock_exists_and_pinned` | method | `tests/test_packaging.py:319` | `def test_core_lock_exists_and_pinned(self)` |
| `test_core_lock_has_python_docx_not_broken_docx` | method | `tests/test_packaging.py:325` | `def test_core_lock_has_python_docx_not_broken_docx(self)` |
| `test_core_lock_is_cross_platform` | method | `tests/test_packaging.py:330` | `def test_core_lock_is_cross_platform(self)` |
| `test_does_not_duplicate_dependencies` | method | `tests/test_packaging.py:181` | `def test_does_not_duplicate_dependencies(self, setup_text)` |
| `test_does_not_install_broken_docx` | method | `tests/test_packaging.py:358` | `def test_does_not_install_broken_docx(self, text)` |
| `test_does_not_install_stdlib_ast` | method | `tests/test_packaging.py:353` | `def test_does_not_install_stdlib_ast(self, text)` |
| `test_does_not_list_broken_docx` | method | `tests/test_packaging.py:121` | `def test_does_not_list_broken_docx(self, pyproject)` |
| `test_does_not_list_stdlib_ast_as_dep` | method | `tests/test_packaging.py:113` | `def test_does_not_list_stdlib_ast_as_dep(self, pyproject)` |
| `test_has_bandit_section` | method | `tests/test_packaging.py:150` | `def test_has_bandit_section(self, pyproject)` |
| `test_has_core_hygiene_hooks` | method | `tests/test_packaging.py:233` | `def test_has_core_hygiene_hooks(self, cfg)` |
| `test_has_detect_secrets_repo` | method | `tests/test_packaging.py:229` | `def test_has_detect_secrets_repo(self, cfg)` |
| `test_has_dev_optional_dependencies` | method | `tests/test_packaging.py:132` | `def test_has_dev_optional_dependencies(self, pyproject)` |
| `test_has_ml_optional_dependencies` | method | `tests/test_packaging.py:126` | `def test_has_ml_optional_dependencies(self, pyproject)` |
| `test_has_mypy_section` | method | `tests/test_packaging.py:146` | `def test_has_mypy_section(self, pyproject)` |
| `test_has_no_typo_dependency` | method | `tests/test_packaging.py:108` | `def test_has_no_typo_dependency(self, pyproject)` |
| `test_has_pytest_section` | method | `tests/test_packaging.py:142` | `def test_has_pytest_section(self, pyproject)` |
| `test_has_ruff_repo` | method | `tests/test_packaging.py:225` | `def test_has_ruff_repo(self, cfg)` |
| `test_has_ruff_section` | method | `tests/test_packaging.py:138` | `def test_has_ruff_section(self, pyproject)` |
| `test_installs_from_pinned_lock` | method | `tests/test_packaging.py:363` | `def test_installs_from_pinned_lock(self, text)` |
| `test_lint_workflow_has_ruff_and_mypy_jobs` | method | `tests/test_packaging.py:257` | `def test_lint_workflow_has_ruff_and_mypy_jobs(self, lint_wf)` |
| `test_lists_flask_wtf_correctly` | method | `tests/test_packaging.py:117` | `def test_lists_flask_wtf_correctly(self, pyproject)` |
| `test_lists_tool` | method | `tests/test_packaging.py:208` | `def test_lists_tool(self, deps, tool)` |
| `test_ml_lock_exists_pinned_with_torch` | method | `tests/test_packaging.py:335` | `def test_ml_lock_exists_pinned_with_torch(self)` |
| `test_no_absolute_modules_ext_path` | method | `tests/test_packaging.py:366` | `def test_no_absolute_modules_ext_path(self, text)` |
| `test_no_stdlib_ast_dep` | method | `tests/test_packaging.py:189` | `def test_no_stdlib_ast_dep(self, setup_text)` |
| `test_no_typo_dep` | method | `tests/test_packaging.py:186` | `def test_no_typo_dep(self, setup_text)` |
| `test_parses` | method | `tests/test_packaging.py:105` | `def test_parses(self, pyproject)` |
| `test_parses` | method | `tests/test_packaging.py:170` | `def test_parses(self, setup_tree)` |
| `test_parses` | method | `tests/test_packaging.py:220` | `def test_parses(self, cfg)` |
| `test_parses` | method | `tests/test_packaging.py:374` | `def test_parses(self, filename)` |
| `test_pattern_present` | method | `tests/test_packaging.py:299` | `def test_pattern_present(self, patterns, pattern)` |
| `test_security_workflow_has_three_jobs` | method | `tests/test_packaging.py:267` | `def test_security_workflow_has_three_jobs(self, security_wf)` |
| `test_test_workflow_runs_pytest` | method | `tests/test_packaging.py:262` | `def test_test_workflow_runs_pytest(self, test_wf)` |
| `test_uses_strict_mode` | method | `tests/test_packaging.py:350` | `def test_uses_strict_mode(self, text)` |
| `test_wf` | method | `tests/test_packaging.py:250` | `def test_wf(self)` |
| `test_workflow_triggers_on_push_and_pr` | method | `tests/test_packaging.py:276` | `def test_workflow_triggers_on_push_and_pr(self, wf_path)` |
| `text` | method | `tests/test_packaging.py:347` | `def text(self)` |
| `_fake_index` | function | `tests/test_palette_overlay.py:24` | `def _fake_index()` |
| `runner` | function | `tests/test_palette_overlay.py:83` | `def runner(context)` |
| `test_build_state_returns_none_when_index_missing` | function | `tests/test_palette_overlay.py:73` | `def test_build_state_returns_none_when_index_missing(monkeypatch)` |
| `test_launch_overlay_uses_runner_for_tests` | function | `tests/test_palette_overlay.py:79` | `def test_launch_overlay_uses_runner_for_tests()` |
| `test_rows_filter_by_substring` | function | `tests/test_palette_overlay.py:44` | `def test_rows_filter_by_substring()` |
| `test_rows_rank_recents_above_substrings` | function | `tests/test_palette_overlay.py:52` | `def test_rows_rank_recents_above_substrings()` |
| `test_rows_respect_max_rows` | function | `tests/test_palette_overlay.py:65` | `def test_rows_respect_max_rows()` |
| `test_rows_returns_all_commands_when_query_empty` | function | `tests/test_palette_overlay.py:36` | `def test_rows_returns_all_commands_when_query_empty()` |
| `test_set_query_strips_whitespace` | function | `tests/test_palette_overlay.py:106` | `def test_set_query_strips_whitespace()` |
| `test_truncate_summary_uses_truncation_suffix` | function | `tests/test_palette_overlay.py:90` | `def test_truncate_summary_uses_truncation_suffix()` |
| `CustomPayload` | class | `tests/test_payload_factory.py:109` | `class CustomPayload(PayloadTemplate)` |
| `MinimalPayload` | class | `tests/test_payload_factory.py:30` | `class MinimalPayload(PayloadTemplate)` |
| `TestFormatPayloadTable` | class | `tests/test_payload_factory.py:168` | `class TestFormatPayloadTable` |
| `TestPayloadFactory` | class | `tests/test_payload_factory.py:74` | `class TestPayloadFactory` |
| `TestPayloadTemplate` | class | `tests/test_payload_factory.py:21` | `class TestPayloadTemplate` |
| `TestReverseShellPayload` | class | `tests/test_payload_factory.py:39` | `class TestReverseShellPayload` |
| `TestWindowsReverseShellPayload` | class | `tests/test_payload_factory.py:64` | `class TestWindowsReverseShellPayload` |
| `generate` | method | `tests/test_payload_factory.py:31` | `def generate(self)` |
| `generate` | method | `tests/test_payload_factory.py:110` | `def generate(self)` |
| `test_abstract_cannot_instantiate` | method | `tests/test_payload_factory.py:22` | `def test_abstract_cannot_instantiate(self)` |
| `test_bash_default` | method | `tests/test_payload_factory.py:40` | `def test_bash_default(self)` |
| `test_concrete_subclass` | method | `tests/test_payload_factory.py:27` | `def test_concrete_subclass(self)` |
| `test_empty_list` | method | `tests/test_payload_factory.py:169` | `def test_empty_list(self)` |
| `test_fallback_to_msfvenom_when_not_found` | method | `tests/test_payload_factory.py:161` | `def test_fallback_to_msfvenom_when_not_found(self)` |
| `test_format_base64` | method | `tests/test_payload_factory.py:130` | `def test_format_base64(self)` |
| `test_format_c` | method | `tests/test_payload_factory.py:138` | `def test_format_c(self)` |
| `test_format_hex` | method | `tests/test_payload_factory.py:124` | `def test_format_hex(self)` |
| `test_format_python` | method | `tests/test_payload_factory.py:144` | `def test_format_python(self)` |
| `test_format_raw` | method | `tests/test_payload_factory.py:118` | `def test_format_raw(self)` |
| `test_formats_list` | method | `tests/test_payload_factory.py:173` | `def test_formats_list(self)` |
| `test_generate_native_payload` | method | `tests/test_payload_factory.py:99` | `def test_generate_native_payload(self)` |
| `test_generates_powershell` | method | `tests/test_payload_factory.py:65` | `def test_generates_powershell(self)` |
| `test_get_existing_payload` | method | `tests/test_payload_factory.py:89` | `def test_get_existing_payload(self)` |
| `test_get_nonexistent_returns_none` | method | `tests/test_payload_factory.py:95` | `def test_get_nonexistent_returns_none(self)` |
| `test_list_all` | method | `tests/test_payload_factory.py:75` | `def test_list_all(self)` |
| `test_list_filter_by_platform` | method | `tests/test_payload_factory.py:82` | `def test_list_filter_by_platform(self)` |
| `test_list_formats` | method | `tests/test_payload_factory.py:150` | `def test_list_formats(self)` |
| `test_multiple_payloads_aligned` | method | `tests/test_payload_factory.py:182` | `def test_multiple_payloads_aligned(self)` |
| `test_nc_shell` | method | `tests/test_payload_factory.py:47` | `def test_nc_shell(self)` |
| `test_python_shell` | method | `tests/test_payload_factory.py:52` | `def test_python_shell(self)` |
| `test_register_custom` | method | `tests/test_payload_factory.py:106` | `def test_register_custom(self)` |
| `test_unknown_shell_type_falls_back_to_bash` | method | `tests/test_payload_factory.py:58` | `def test_unknown_shell_type_falls_back_to_bash(self)` |
| `TestAssignIntegration` | class | `tests/test_payload_schema.py:235` | `class TestAssignIntegration` |
| `TestCoerceValue` | class | `tests/test_payload_schema.py:133` | `class TestCoerceValue` |
| `TestFieldFor` | class | `tests/test_payload_schema.py:191` | `class TestFieldFor` |
| `TestFormatIssue` | class | `tests/test_payload_schema.py:201` | `class TestFormatIssue` |
| `TestLlmBackendSchema` | class | `tests/test_payload_schema.py:275` | `class TestLlmBackendSchema` |
| `TestSchemaShape` | class | `tests/test_payload_schema.py:41` | `class TestSchemaShape` |
| `TestValidatePayload` | class | `tests/test_payload_schema.py:162` | `class TestValidatePayload` |
| `TestValidateValue` | class | `tests/test_payload_schema.py:72` | `class TestValidateValue` |
| `test_allowed_values_enforced` | method | `tests/test_payload_schema.py:121` | `def test_allowed_values_enforced(self)` |
| `test_apply_assign_coerces_port_strings` | method | `tests/test_payload_schema.py:236` | `def test_apply_assign_coerces_port_strings(self)` |
| `test_apply_assign_keeps_unknown_key_behavior` | method | `tests/test_payload_schema.py:267` | `def test_apply_assign_keeps_unknown_key_behavior(self)` |
| `test_apply_assign_no_issue_for_valid_value` | method | `tests/test_payload_schema.py:259` | `def test_apply_assign_no_issue_for_valid_value(self)` |
| `test_apply_assign_surfaces_issue_for_bad_ip` | method | `tests/test_payload_schema.py:244` | `def test_apply_assign_surfaces_issue_for_bad_ip(self)` |
| `test_bool_falsy_strings` | method | `tests/test_payload_schema.py:147` | `def test_bool_falsy_strings(self)` |
| `test_bool_passthrough` | method | `tests/test_payload_schema.py:151` | `def test_bool_passthrough(self)` |
| `test_bool_truthy_strings` | method | `tests/test_payload_schema.py:143` | `def test_bool_truthy_strings(self)` |
| `test_categories_split_schema` | method | `tests/test_payload_schema.py:65` | `def test_categories_split_schema(self)` |
| `test_default_payload_passes` | method | `tests/test_payload_schema.py:163` | `def test_default_payload_passes(self)` |
| `test_every_spec_has_required_fields` | method | `tests/test_payload_schema.py:45` | `def test_every_spec_has_required_fields(self)` |
| `test_hex_validates` | method | `tests/test_payload_schema.py:117` | `def test_hex_validates(self)` |
| `test_hide_code_range` | method | `tests/test_payload_schema.py:127` | `def test_hide_code_range(self)` |
| `test_invalid_ip_returns_error` | method | `tests/test_payload_schema.py:89` | `def test_invalid_ip_returns_error(self)` |
| `test_ip_string_unchanged` | method | `tests/test_payload_schema.py:158` | `def test_ip_string_unchanged(self)` |
| `test_llm_backend_accepts_supported` | method | `tests/test_payload_schema.py:293` | `def test_llm_backend_accepts_supported(self)` |
| `test_llm_backend_enum_validated` | method | `tests/test_payload_schema.py:276` | `def test_llm_backend_enum_validated(self)` |
| `test_llm_backend_rejects_unknown` | method | `tests/test_payload_schema.py:290` | `def test_llm_backend_rejects_unknown(self)` |
| `test_long_values_truncated` | method | `tests/test_payload_schema.py:223` | `def test_long_values_truncated(self)` |
| `test_missing_required_field_reports_error` | method | `tests/test_payload_schema.py:168` | `def test_missing_required_field_reports_error(self)` |
| `test_model_slots_registered_with_factory_defaults` | method | `tests/test_payload_schema.py:300` | `def test_model_slots_registered_with_factory_defaults(self)` |
| `test_negative_port_warns` | method | `tests/test_payload_schema.py:102` | `def test_negative_port_warns(self)` |
| `test_non_sensitive_values_shown` | method | `tests/test_payload_schema.py:213` | `def test_non_sensitive_values_shown(self)` |
| `test_ollama_host_registered` | method | `tests/test_payload_schema.py:320` | `def test_ollama_host_registered(self)` |
| `test_optional_missing_returns_none` | method | `tests/test_payload_schema.py:82` | `def test_optional_missing_returns_none(self)` |
| `test_os_id_must_be_1_or_2` | method | `tests/test_payload_schema.py:106` | `def test_os_id_must_be_1_or_2(self)` |
| `test_port_int_passthrough` | method | `tests/test_payload_schema.py:137` | `def test_port_int_passthrough(self)` |
| `test_port_non_numeric_passthrough` | method | `tests/test_payload_schema.py:140` | `def test_port_non_numeric_passthrough(self)` |
| `test_port_out_of_range_is_warning` | method | `tests/test_payload_schema.py:98` | `def test_port_out_of_range_is_warning(self)` |
| `test_port_string_is_accepted` | method | `tests/test_payload_schema.py:95` | `def test_port_string_is_accepted(self)` |
| `test_port_string_to_int` | method | `tests/test_payload_schema.py:134` | `def test_port_string_to_int(self)` |
| `test_provider_key_slots_sensitive` | method | `tests/test_payload_schema.py:314` | `def test_provider_key_slots_sensitive(self)` |
| `test_required_fields_are_documented` | method | `tests/test_payload_schema.py:53` | `def test_required_fields_are_documented(self)` |
| `test_required_missing_returns_error` | method | `tests/test_payload_schema.py:78` | `def test_required_missing_returns_error(self)` |
| `test_returns_none_for_unknown_key` | method | `tests/test_payload_schema.py:197` | `def test_returns_none_for_unknown_key(self)` |
| `test_returns_spec_for_known_key` | method | `tests/test_payload_schema.py:192` | `def test_returns_spec_for_known_key(self)` |
| `test_schema_is_not_empty` | method | `tests/test_payload_schema.py:42` | `def test_schema_is_not_empty(self)` |
| `test_sensitive_values_redacted` | method | `tests/test_payload_schema.py:202` | `def test_sensitive_values_redacted(self)` |
| `test_shipped_payload_has_no_errors` | method | `tests/test_payload_schema.py:182` | `def test_shipped_payload_has_no_errors(self)` |
| `test_shipped_payload_keys_are_all_in_schema` | method | `tests/test_payload_schema.py:57` | `def test_shipped_payload_keys_are_all_in_schema(self)` |
| `test_unknown_key_in_payload_is_info` | method | `tests/test_payload_schema.py:175` | `def test_unknown_key_in_payload_is_info(self)` |
| `test_unknown_key_passthrough` | method | `tests/test_payload_schema.py:155` | `def test_unknown_key_passthrough(self)` |
| `test_unknown_key_returns_info` | method | `tests/test_payload_schema.py:73` | `def test_unknown_key_returns_info(self)` |
| `test_url_validates` | method | `tests/test_payload_schema.py:112` | `def test_url_validates(self)` |
| `test_valid_ip_passes` | method | `tests/test_payload_schema.py:86` | `def test_valid_ip_passes(self)` |
| `TestConsumePolicyFacts` | class | `tests/test_phase1_data_gaps.py:265` | `class TestConsumePolicyFacts` |
| `TestCredentialAwareRetry` | class | `tests/test_phase1_data_gaps.py:490` | `class TestCredentialAwareRetry` |
| `TestEmailAndDomainEntries` | class | `tests/test_phase1_data_gaps.py:158` | `class TestEmailAndDomainEntries` |
| `TestEmailExtractor` | class | `tests/test_phase1_data_gaps.py:103` | `class TestEmailExtractor` |
| `TestFindingMetadata` | class | `tests/test_phase1_data_gaps.py:56` | `class TestFindingMetadata` |
| `TestFullDataFlow` | class | `tests/test_phase1_data_gaps.py:562` | `class TestFullDataFlow` |
| `TestGraphTopologySignal` | class | `tests/test_phase1_data_gaps.py:376` | `class TestGraphTopologySignal` |
| `TestObsParserIncludesEmailExtractor` | class | `tests/test_phase1_data_gaps.py:130` | `class TestObsParserIncludesEmailExtractor` |
| `TestServiceVersionExtractor` | class | `tests/test_phase1_data_gaps.py:72` | `class TestServiceVersionExtractor` |
| `TestUpdateFromFindings` | class | `tests/test_phase1_data_gaps.py:198` | `class TestUpdateFromFindings` |
| `TestWorldModelEmailDomain` | class | `tests/test_phase1_data_gaps.py:174` | `class TestWorldModelEmailDomain` |
| `TestWorldModelPersistence` | class | `tests/test_phase1_data_gaps.py:332` | `class TestWorldModelPersistence` |
| `_make_finding` | function | `tests/test_phase1_data_gaps.py:49` | `def _make_finding(ftype, value, host, metadata)` |
| `parser` | function | `tests/test_phase1_data_gaps.py:36` | `def parser()` |
| `test_add_domain_stores_and_adds_note` | method | `tests/test_phase1_data_gaps.py:181` | `def test_add_domain_stores_and_adds_note(self, world_model)` |
| `test_add_domain_without_host` | method | `tests/test_phase1_data_gaps.py:189` | `def test_add_domain_without_host(self, world_model)` |
| `test_add_email_stores_and_deduplicates` | method | `tests/test_phase1_data_gaps.py:175` | `def test_add_email_stores_and_deduplicates(self, world_model)` |
| `test_computes_centrality_from_graph_when_no_candidates` | method | `tests/test_phase1_data_gaps.py:452` | `def test_computes_centrality_from_graph_when_no_candidates(self, tmp_path)` |
| `test_consume_empty_file_returns_zero` | method | `tests/test_phase1_data_gaps.py:266` | `def test_consume_empty_file_returns_zero(self, world_model, tmp_path)` |
| `test_consume_ingests_hosts_and_services` | method | `tests/test_phase1_data_gaps.py:272` | `def test_consume_ingests_hosts_and_services(self, world_model, tmp_path)` |
| `test_consume_malformed_json_returns_zero` | method | `tests/test_phase1_data_gaps.py:322` | `def test_consume_malformed_json_returns_zero(self, world_model, tmp_path)` |
| `test_consume_nonexistent_file_returns_zero` | method | `tests/test_phase1_data_gaps.py:318` | `def test_consume_nonexistent_file_returns_zero(self, world_model)` |
| `test_credential_aware_rank_boosts_brute_force` | method | `tests/test_phase1_data_gaps.py:501` | `def test_credential_aware_rank_boosts_brute_force(self)` |
| `test_credential_aware_rank_boosts_credential_reuse` | method | `tests/test_phase1_data_gaps.py:526` | `def test_credential_aware_rank_boosts_credential_reuse(self)` |
| `test_credential_aware_rank_handles_empty_creds` | method | `tests/test_phase1_data_gaps.py:543` | `def test_credential_aware_rank_handles_empty_creds(self)` |
| `test_deduplicates_emails` | method | `tests/test_phase1_data_gaps.py:119` | `def test_deduplicates_emails(self)` |
| `test_domain_entry_defaults` | method | `tests/test_phase1_data_gaps.py:165` | `def test_domain_entry_defaults(self)` |
| `test_domain_finding_calls_add_domain` | method | `tests/test_phase1_data_gaps.py:227` | `def test_domain_finding_calls_add_domain(self, world_model)` |
| `test_email_entry_defaults` | method | `tests/test_phase1_data_gaps.py:159` | `def test_email_entry_defaults(self)` |
| `test_email_finding_calls_add_email` | method | `tests/test_phase1_data_gaps.py:235` | `def test_email_finding_calls_add_email(self, world_model)` |
| `test_emails_and_domains_survive_roundtrip` | method | `tests/test_phase1_data_gaps.py:333` | `def test_emails_and_domains_survive_roundtrip(self, world_model)` |
| `test_error_finding_adds_note` | method | `tests/test_phase1_data_gaps.py:243` | `def test_error_finding_adds_note(self, world_model)` |
| `test_error_finding_no_host_uses_sentinel` | method | `tests/test_phase1_data_gaps.py:252` | `def test_error_finding_no_host_uses_sentinel(self, world_model)` |
| `test_extracts_multiple_emails` | method | `tests/test_phase1_data_gaps.py:111` | `def test_extracts_multiple_emails(self)` |
| `test_extracts_single_email` | method | `tests/test_phase1_data_gaps.py:104` | `def test_extracts_single_email(self)` |
| `test_finding_accepts_metadata` | method | `tests/test_phase1_data_gaps.py:61` | `def test_finding_accepts_metadata(self)` |
| `test_finding_has_metadata_default_empty` | method | `tests/test_phase1_data_gaps.py:57` | `def test_finding_has_metadata_default_empty(self)` |
| `test_ignores_non_email` | method | `tests/test_phase1_data_gaps.py:124` | `def test_ignores_non_email(self)` |
| `test_multiple_services_extracted` | method | `tests/test_phase1_data_gaps.py:81` | `def test_multiple_services_extracted(self)` |
| `test_parser_extracts_emails_from_output` | method | `tests/test_phase1_data_gaps.py:131` | `def test_parser_extracts_emails_from_output(self, parser)` |
| `test_parser_still_extracts_service_versions_with_metadata` | method | `tests/test_phase1_data_gaps.py:141` | `def test_parser_still_extracts_service_versions_with_metadata(self, parser)` |
| `test_port_and_protocol_in_metadata` | method | `tests/test_phase1_data_gaps.py:73` | `def test_port_and_protocol_in_metadata(self)` |
| `test_produces_credential_spray_proposals` | method | `tests/test_phase1_data_gaps.py:425` | `def test_produces_credential_spray_proposals(self, tmp_path)` |
| `test_produces_lateral_proposals_from_host_nodes` | method | `tests/test_phase1_data_gaps.py:388` | `def test_produces_lateral_proposals_from_host_nodes(self, tmp_path)` |
| `test_recon_to_world_model_to_recommendation` | method | `tests/test_phase1_data_gaps.py:563` | `def test_recon_to_world_model_to_recommendation(self, world_model, parser)` |
| `test_reset_clears_emails_and_domains` | method | `tests/test_phase1_data_gaps.py:349` | `def test_reset_clears_emails_and_domains(self, world_model)` |
| `test_retry_with_no_open_ports_returns_empty` | method | `tests/test_phase1_data_gaps.py:491` | `def test_retry_with_no_open_ports_returns_empty(self)` |
| `test_returns_empty_on_nonexistent_world_model` | method | `tests/test_phase1_data_gaps.py:377` | `def test_returns_empty_on_nonexistent_world_model(self)` |
| `test_service_version_calls_add_service` | method | `tests/test_phase1_data_gaps.py:199` | `def test_service_version_calls_add_service(self, world_model)` |
| `test_service_version_no_longer_adds_note` | method | `tests/test_phase1_data_gaps.py:213` | `def test_service_version_no_longer_adds_note(self, world_model)` |
| `test_signals_are_wired_in_build_default_engine` | method | `tests/test_phase1_data_gaps.py:477` | `def test_signals_are_wired_in_build_default_engine(self, tmp_path)` |
| `test_snapshot_includes_emails_and_domains` | method | `tests/test_phase1_data_gaps.py:356` | `def test_snapshot_includes_emails_and_domains(self, world_model)` |
| `test_to_context_string_has_email_domain_counts` | method | `tests/test_phase1_data_gaps.py:365` | `def test_to_context_string_has_email_domain_counts(self, world_model)` |
| `test_udp_service_captured` | method | `tests/test_phase1_data_gaps.py:91` | `def test_udp_service_captured(self)` |
| `world_model` | function | `tests/test_phase1_data_gaps.py:41` | `def world_model()` |
| `test_contextual_help_reuses_canonical_labels` | function | `tests/test_phase_labels.py:32` | `def test_contextual_help_reuses_canonical_labels()` |
| `test_known_phase_labels` | function | `tests/test_phase_labels.py:13` | `def test_known_phase_labels()` |
| `test_phase_label_falls_back_to_title_case` | function | `tests/test_phase_labels.py:19` | `def test_phase_label_falls_back_to_title_case()` |
| `test_phase_label_keys_cover_command_index_phases` | function | `tests/test_phase_labels.py:26` | `def test_phase_label_keys_cover_command_index_phases()` |
| `test_tips_engine_reuses_canonical_labels` | function | `tests/test_phase_labels.py:38` | `def test_tips_engine_reuses_canonical_labels()` |
| `_Proc` | class | `tests/test_pi_leg.py:20` | `class _Proc` |
| `__init__` | method | `tests/test_pi_leg.py:21` | `def __init__(self, returncode, stdout, stderr)` |
| `_fake_run` | function | `tests/test_pi_leg.py:32` | `def _fake_run(cmd)` |
| `_patch_run` | function | `tests/test_pi_leg.py:27` | `def _patch_run(monkeypatch, proc)` |
| `test_pi_default_model` | function | `tests/test_pi_leg.py:67` | `def test_pi_default_model(monkeypatch)` |
| `test_pi_empty_prompt_short_circuits` | function | `tests/test_pi_leg.py:106` | `def test_pi_empty_prompt_short_circuits(monkeypatch)` |
| `test_pi_empty_reply_raises` | function | `tests/test_pi_leg.py:88` | `def test_pi_empty_reply_raises(monkeypatch)` |
| `test_pi_missing_binary_raises` | function | `tests/test_pi_leg.py:44` | `def test_pi_missing_binary_raises(monkeypatch)` |
| `test_pi_model_passthrough` | function | `tests/test_pi_leg.py:60` | `def test_pi_model_passthrough(monkeypatch)` |
| `test_pi_nonzero_exit_raises` | function | `tests/test_pi_leg.py:81` | `def test_pi_nonzero_exit_raises(monkeypatch)` |
| `test_pi_pool_member_resolves` | function | `tests/test_pi_leg.py:121` | `def test_pi_pool_member_resolves(monkeypatch, tmp_path)` |
| `test_pi_prefix_case_insensitive` | function | `tests/test_pi_leg.py:74` | `def test_pi_prefix_case_insensitive(monkeypatch)` |
| `test_pi_stream_falls_back_to_complete` | function | `tests/test_pi_leg.py:114` | `def test_pi_stream_falls_back_to_complete(monkeypatch)` |
| `test_pi_success_returns_text` | function | `tests/test_pi_leg.py:51` | `def test_pi_success_returns_text(monkeypatch)` |
| `test_pi_timeout_raises` | function | `tests/test_pi_leg.py:95` | `def test_pi_timeout_raises(monkeypatch)` |
| `TestConditionEvaluator` | class | `tests/test_pipeline_engine.py:150` | `class TestConditionEvaluator` |
| `TestMcpEntryPoints` | class | `tests/test_pipeline_engine.py:684` | `class TestMcpEntryPoints` |
| `TestNestedPipelines` | class | `tests/test_pipeline_engine.py:577` | `class TestNestedPipelines` |
| `TestPipelineEngineExecution` | class | `tests/test_pipeline_engine.py:383` | `class TestPipelineEngineExecution` |
| `TestPipelineLoader` | class | `tests/test_pipeline_engine.py:254` | `class TestPipelineLoader` |
| `TestStepDerivers` | class | `tests/test_pipeline_engine.py:206` | `class TestStepDerivers` |
| `TestStepValidator` | class | `tests/test_pipeline_engine.py:175` | `class TestStepValidator` |
| `TestTemplateResolver` | class | `tests/test_pipeline_engine.py:98` | `class TestTemplateResolver` |
| `TestWiring` | class | `tests/test_pipeline_engine.py:738` | `class TestWiring` |
| `_ScriptedRunner` | class | `tests/test_pipeline_engine.py:67` | `class _ScriptedRunner` |
| `_SilentNarrator` | class | `tests/test_pipeline_engine.py:369` | `class _SilentNarrator(INarratorAdapter)` |
| `__init__` | method | `tests/test_pipeline_engine.py:70` | `def __init__(self, outputs, successes)` |
| `__init__` | method | `tests/test_pipeline_engine.py:370` | `def __init__(self)` |
| `_heuristic_success` | method | `tests/test_pipeline_engine.py:87` | `def _heuristic_success(output)` |
| `_write_pipeline` | function | `tests/test_pipeline_engine.py:248` | `def _write_pipeline(pipelines_dir, name, data)` |
| `narrate` | method | `tests/test_pipeline_engine.py:373` | `def narrate(self, kind, target, message, payload, severity)` |
| `run` | method | `tests/test_pipeline_engine.py:79` | `def run(self, command, args, target, timeout_s)` |
| `silent_engine_kwargs` | function | `tests/test_pipeline_engine.py:361` | `def silent_engine_kwargs(temp_lazyown)` |
| `temp_lazyown` | function | `tests/test_pipeline_engine.py:36` | `def temp_lazyown(tmp_path, monkeypatch)` |
| `test_bool_serialisation` | method | `tests/test_pipeline_engine.py:112` | `def test_bool_serialisation(self, temp_lazyown)` |
| `test_both_command_and_pipeline_rejected` | method | `tests/test_pipeline_engine.py:284` | `def test_both_command_and_pipeline_rejected(self, temp_lazyown)` |
| `test_condition_false_skips_step` | method | `tests/test_pipeline_engine.py:444` | `def test_condition_false_skips_step(self, temp_lazyown, silent_engine_kwargs)` |
| `test_condition_true_runs_step` | method | `tests/test_pipeline_engine.py:473` | `def test_condition_true_runs_step(self, temp_lazyown, silent_engine_kwargs)` |
| `test_cycle_is_detected` | method | `tests/test_pipeline_engine.py:613` | `def test_cycle_is_detected(self, temp_lazyown, silent_engine_kwargs)` |
| `test_daemon_has_pipeline_subcommand` | method | `tests/test_pipeline_engine.py:758` | `def test_daemon_has_pipeline_subcommand(self)` |
| `test_depth_limit_enforced` | method | `tests/test_pipeline_engine.py:639` | `def test_depth_limit_enforced(self, temp_lazyown, silent_engine_kwargs)` |
| `test_do_pipeline_exists_in_lazyown` | method | `tests/test_pipeline_engine.py:739` | `def test_do_pipeline_exists_in_lazyown(self)` |
| `test_dotted_path_lookup` | method | `tests/test_pipeline_engine.py:99` | `def test_dotted_path_lookup(self, temp_lazyown)` |
| `test_empty_and_non_empty` | method | `tests/test_pipeline_engine.py:188` | `def test_empty_and_non_empty(self, temp_lazyown)` |
| `test_empty_steps_rejected` | method | `tests/test_pipeline_engine.py:310` | `def test_empty_steps_rejected(self, temp_lazyown)` |
| `test_example_pipelines_validate` | method | `tests/test_pipeline_engine.py:769` | `def test_example_pipelines_validate(self)` |
| `test_input_from_replaces_args` | method | `tests/test_pipeline_engine.py:545` | `def test_input_from_replaces_args(self, temp_lazyown, silent_engine_kwargs)` |
| `test_invalid_name_rejected` | method | `tests/test_pipeline_engine.py:278` | `def test_invalid_name_rejected(self, temp_lazyown)` |
| `test_invalid_on_failure_rejected` | method | `tests/test_pipeline_engine.py:324` | `def test_invalid_on_failure_rejected(self, temp_lazyown)` |
| `test_invalid_yaml_raises_schema_error` | method | `tests/test_pipeline_engine.py:346` | `def test_invalid_yaml_raises_schema_error(self, temp_lazyown)` |
| `test_lazynmap_derives_services` | method | `tests/test_pipeline_engine.py:214` | `def test_lazynmap_derives_services(self, temp_lazyown)` |
| `test_list_index_lookup` | method | `tests/test_pipeline_engine.py:138` | `def test_list_index_lookup(self, temp_lazyown)` |
| `test_list_returns_json` | method | `tests/test_pipeline_engine.py:685` | `def test_list_returns_json(self, temp_lazyown)` |
| `test_list_returns_sorted_names` | method | `tests/test_pipeline_engine.py:337` | `def test_list_returns_sorted_names(self, temp_lazyown)` |
| `test_load_basic_pipeline` | method | `tests/test_pipeline_engine.py:255` | `def test_load_basic_pipeline(self, temp_lazyown)` |
| `test_mcp_exposes_four_pipeline_tools` | method | `tests/test_pipeline_engine.py:748` | `def test_mcp_exposes_four_pipeline_tools(self)` |
| `test_missing_path_renders_empty` | method | `tests/test_pipeline_engine.py:106` | `def test_missing_path_renders_empty(self, temp_lazyown)` |
| `test_missing_pipeline_raises` | method | `tests/test_pipeline_engine.py:272` | `def test_missing_pipeline_raises(self, temp_lazyown)` |
| `test_neither_command_nor_pipeline_rejected` | method | `tests/test_pipeline_engine.py:297` | `def test_neither_command_nor_pipeline_rejected(self, temp_lazyown)` |
| `test_nested_pipeline_runs_and_records_run_id` | method | `tests/test_pipeline_engine.py:578` | `def test_nested_pipeline_runs_and_records_run_id(self, temp_lazyown, silent_engine_kwargs)` |
| `test_no_code_execution` | method | `tests/test_pipeline_engine.py:130` | `def test_no_code_execution(self, temp_lazyown)` |
| `test_no_predicate_is_pass_through` | method | `tests/test_pipeline_engine.py:195` | `def test_no_predicate_is_pass_through(self, temp_lazyown)` |
| `test_no_template_passes_through` | method | `tests/test_pipeline_engine.py:124` | `def test_no_template_passes_through(self, temp_lazyown)` |
| `test_on_failure_continue_keeps_going` | method | `tests/test_pipeline_engine.py:520` | `def test_on_failure_continue_keeps_going(self, temp_lazyown, silent_engine_kwargs)` |
| `test_on_success_hook_runs` | method | `tests/test_pipeline_engine.py:498` | `def test_on_success_hook_runs(self, temp_lazyown, silent_engine_kwargs)` |
| `test_payload_lookup` | method | `tests/test_pipeline_engine.py:118` | `def test_payload_lookup(self, temp_lazyown)` |
| `test_ping_derives_ttl_and_alive` | method | `tests/test_pipeline_engine.py:207` | `def test_ping_derives_ttl_and_alive(self, temp_lazyown)` |
| `test_pipelines_dir_exists_and_has_readme` | method | `tests/test_pipeline_engine.py:763` | `def test_pipelines_dir_exists_and_has_readme(self)` |
| `test_regex_match` | method | `tests/test_pipeline_engine.py:182` | `def test_regex_match(self, temp_lazyown)` |
| `test_register_custom_deriver` | method | `tests/test_pipeline_engine.py:236` | `def test_register_custom_deriver(self, temp_lazyown)` |
| `test_run_rejects_invalid_name` | method | `tests/test_pipeline_engine.py:699` | `def test_run_rejects_invalid_name(self, temp_lazyown)` |
| `test_runs_steps_in_order_and_persists_artifacts` | method | `tests/test_pipeline_engine.py:384` | `def test_runs_steps_in_order_and_persists_artifacts(self, temp_lazyown, silent_engine_kwargs)` |
| `test_searchsploit_has_exploit` | method | `tests/test_pipeline_engine.py:223` | `def test_searchsploit_has_exploit(self, temp_lazyown)` |
| `test_status_returns_ok_with_no_runs` | method | `tests/test_pipeline_engine.py:725` | `def test_status_returns_ok_with_no_runs(self, temp_lazyown)` |
| `test_substring_match` | method | `tests/test_pipeline_engine.py:176` | `def test_substring_match(self, temp_lazyown)` |
| `test_truthy_table` | method | `tests/test_pipeline_engine.py:164` | `def test_truthy_table(self, temp_lazyown, value, expected)` |
| `test_unknown_command_returns_empty` | method | `tests/test_pipeline_engine.py:231` | `def test_unknown_command_returns_empty(self, temp_lazyown)` |
| `test_validate_failure_marks_step_failed` | method | `tests/test_pipeline_engine.py:417` | `def test_validate_failure_marks_step_failed(self, temp_lazyown, silent_engine_kwargs)` |
| `test_validate_missing_pipeline_errors` | method | `tests/test_pipeline_engine.py:719` | `def test_validate_missing_pipeline_errors(self, temp_lazyown)` |
| `test_validate_returns_step_list` | method | `tests/test_pipeline_engine.py:705` | `def test_validate_returns_step_list(self, temp_lazyown)` |
| `_live_keys` | function | `tests/test_placeholder_coverage.py:40` | `def _live_keys()` |
| `_skill_keys` | function | `tests/test_placeholder_coverage.py:49` | `def _skill_keys()` |
| `test_addon_tokens_resolve` | function | `tests/test_placeholder_coverage.py:74` | `def test_addon_tokens_resolve()` |
| `test_addon_tokens_resolve_at_runtime` | function | `tests/test_placeholder_coverage.py:94` | `def test_addon_tokens_resolve_at_runtime()` |
| `test_required_params_exist_live` | function | `tests/test_placeholder_coverage.py:118` | `def test_required_params_exist_live()` |
| `test_schema_covers_live_keys` | function | `tests/test_placeholder_coverage.py:63` | `def test_schema_covers_live_keys()` |
| `test_skill_documents_validator_keys` | function | `tests/test_placeholder_coverage.py:68` | `def test_skill_documents_validator_keys()` |
| `test_validator_covers_live_keys` | function | `tests/test_placeholder_coverage.py:57` | `def test_validator_covers_live_keys()` |
| `_write` | function | `tests/test_playbook_admin.py:21` | `def _write(directory, name, data)` |
| `test_create_refuses_overwrite_and_escape` | function | `tests/test_playbook_admin.py:91` | `def test_create_refuses_overwrite_and_escape(tmp_path)` |
| `test_create_update_and_delete_round_trip` | function | `tests/test_playbook_admin.py:70` | `def test_create_update_and_delete_round_trip(tmp_path)` |
| `test_scan_reports_apt_and_plan_shapes` | function | `tests/test_playbook_admin.py:27` | `def test_scan_reports_apt_and_plan_shapes(tmp_path)` |
| `test_slug_and_preview` | function | `tests/test_playbook_admin.py:110` | `def test_slug_and_preview(tmp_path)` |
| `test_validate_rejects_mixed_and_empty` | function | `tests/test_playbook_admin.py:60` | `def test_validate_rejects_mixed_and_empty(tmp_path)` |
| `TestPlaceholderQuoting` | class | `tests/test_plugin_loader_safety.py:38` | `class TestPlaceholderQuoting` |
| `_load_fn` | function | `tests/test_plugin_loader_safety.py:23` | `def _load_fn()` |
| `test_command_substitution_neutralized` | method | `tests/test_plugin_loader_safety.py:48` | `def test_command_substitution_neutralized(self)` |
| `test_injection_neutralized` | method | `tests/test_plugin_loader_safety.py:43` | `def test_injection_neutralized(self)` |
| `test_missing_key_left_verbatim` | method | `tests/test_plugin_loader_safety.py:53` | `def test_missing_key_left_verbatim(self)` |
| `test_plain_values_pass_through` | method | `tests/test_plugin_loader_safety.py:39` | `def test_plain_values_pass_through(self)` |
| `test_uses_shlex_quote` | method | `tests/test_plugin_loader_safety.py:57` | `def test_uses_shlex_quote(self)` |
| `test_corrupt_store_reads_empty` | function | `tests/test_plugin_tiers.py:79` | `def test_corrupt_store_reads_empty(tmp_path)` |
| `test_default_tier_is_community` | function | `tests/test_plugin_tiers.py:37` | `def test_default_tier_is_community()` |
| `test_format_rating` | function | `tests/test_plugin_tiers.py:85` | `def test_format_rating()` |
| `test_malformed_manifest_is_ignored` | function | `tests/test_plugin_tiers.py:56` | `def test_malformed_manifest_is_ignored(tmp_path)` |
| `test_manifest_overrides_metadata` | function | `tests/test_plugin_tiers.py:29` | `def test_manifest_overrides_metadata()` |
| `test_metadata_tier_used_without_manifest` | function | `tests/test_plugin_tiers.py:33` | `def test_metadata_tier_used_without_manifest()` |
| `test_missing_manifest_returns_empty` | function | `tests/test_plugin_tiers.py:52` | `def test_missing_manifest_returns_empty(tmp_path)` |
| `test_rate_and_average` | function | `tests/test_plugin_tiers.py:62` | `def test_rate_and_average(tmp_path)` |
| `test_rate_rejects_bad_input` | function | `tests/test_plugin_tiers.py:70` | `def test_rate_rejects_bad_input(tmp_path)` |
| `test_read_metadata_tier` | function | `tests/test_plugin_tiers.py:91` | `def test_read_metadata_tier(tmp_path)` |
| `test_repo_manifest_loads_with_valid_tiers` | function | `tests/test_plugin_tiers.py:42` | `def test_repo_manifest_loads_with_valid_tiers()` |
| `test_tier_constants` | function | `tests/test_plugin_tiers.py:25` | `def test_tier_constants()` |
| `_Spec` | class | `tests/test_profiles.py:26` | `class _Spec` |
| `__init__` | method | `tests/test_profiles.py:27` | `def __init__(self, import_name)` |
| `_pinned_names` | function | `tests/test_profiles.py:68` | `def _pinned_names(path)` |
| `test_default_profile_is_full` | function | `tests/test_profiles.py:31` | `def test_default_profile_is_full(monkeypatch)` |
| `test_full_profile_keeps_every_spec` | function | `tests/test_profiles.py:54` | `def test_full_profile_keeps_every_spec(monkeypatch)` |
| `test_light_lock_drops_analytics_and_ai` | function | `tests/test_profiles.py:88` | `def test_light_lock_drops_analytics_and_ai()` |
| `test_light_lock_is_a_subset_of_full_lock` | function | `tests/test_profiles.py:79` | `def test_light_lock_is_a_subset_of_full_lock()` |
| `test_light_profile_selected` | function | `tests/test_profiles.py:37` | `def test_light_profile_selected(monkeypatch)` |
| `test_light_profile_skips_analytics_and_ai` | function | `tests/test_profiles.py:60` | `def test_light_profile_skips_analytics_and_ai(monkeypatch)` |
| `test_profile_value_is_case_insensitive` | function | `tests/test_profiles.py:43` | `def test_profile_value_is_case_insensitive(monkeypatch)` |
| `test_unknown_profile_raises` | function | `tests/test_profiles.py:48` | `def test_unknown_profile_raises(monkeypatch)` |
| `test_ansi_escape_gets_fenced` | function | `tests/test_prompt_readline_markers.py:25` | `def test_ansi_escape_gets_fenced()` |
| `test_mixed_prompt_fences_only_ansi` | function | `tests/test_prompt_readline_markers.py:43` | `def test_mixed_prompt_fences_only_ansi()` |
| `test_newline_stays_bare` | function | `tests/test_prompt_readline_markers.py:35` | `def test_newline_stays_bare()` |
| `test_render_prompt_default_has_no_markers` | function | `tests/test_prompt_readline_markers.py:53` | `def test_render_prompt_default_has_no_markers()` |
| `test_render_prompt_raw_has_no_markers` | function | `tests/test_prompt_readline_markers.py:70` | `def test_render_prompt_raw_has_no_markers()` |
| `test_render_prompt_readline_mode_fences_ansi_only` | function | `tests/test_prompt_readline_markers.py:62` | `def test_render_prompt_readline_mode_fences_ansi_only()` |
| `test_strip_readline_markers_restores_raw` | function | `tests/test_prompt_readline_markers.py:79` | `def test_strip_readline_markers_restores_raw()` |
| `test_stripped_prompt_matches_box_shape` | function | `tests/test_prompt_readline_markers.py:87` | `def test_stripped_prompt_matches_box_shape()` |
| `_command_set_with_fake_shell` | function | `tests/test_prompt_refresh.py:22` | `def _command_set_with_fake_shell()` |
| `test_do_assign_calls_refresh_prompt` | function | `tests/test_prompt_refresh.py:52` | `def test_do_assign_calls_refresh_prompt()` |
| `test_no_bracket_replace_hack` | function | `tests/test_prompt_refresh.py:71` | `def test_no_bracket_replace_hack()` |
| `test_prompt_read_after_forward` | function | `tests/test_prompt_refresh.py:37` | `def test_prompt_read_after_forward()` |
| `test_prompt_write_forwards_to_shell` | function | `tests/test_prompt_refresh.py:29` | `def test_prompt_write_forwards_to_shell()` |
| `test_render_prompt_includes_rhost` | function | `tests/test_prompt_refresh.py:65` | `def test_render_prompt_includes_rhost()` |
| `test_rhost_commands_use_refresh_prompt` | function | `tests/test_prompt_refresh.py:78` | `def test_rhost_commands_use_refresh_prompt()` |
| `test_shell_defines_refresh_prompt` | function | `tests/test_prompt_refresh.py:59` | `def test_shell_defines_refresh_prompt()` |
| `test_unrelated_write_stays_local` | function | `tests/test_prompt_refresh.py:44` | `def test_unrelated_write_stays_local()` |
| `_load_tools` | function | `tests/test_pwntomate_tools.py:47` | `def _load_tools()` |
| `_render` | function | `tests/test_pwntomate_tools.py:57` | `def _render(template, domain, tunnel)` |
| `_would_run` | function | `tests/test_pwntomate_tools.py:83` | `def _would_run(template, domain)` |
| `test_gobuster_templates_use_valid_syntax` | function | `tests/test_pwntomate_tools.py:129` | `def test_gobuster_templates_use_valid_syntax()` |
| `test_no_hardcoded_always_ssl_flag` | function | `tests/test_pwntomate_tools.py:141` | `def test_no_hardcoded_always_ssl_flag()` |
| `test_placeholders_match_pwntomate_substitutions` | function | `tests/test_pwntomate_tools.py:103` | `def test_placeholders_match_pwntomate_substitutions()` |
| `test_rendered_commands_have_no_empty_host` | function | `tests/test_pwntomate_tools.py:115` | `def test_rendered_commands_have_no_empty_host()` |
| `test_templates_are_valid_json_with_required_keys` | function | `tests/test_pwntomate_tools.py:92` | `def test_templates_are_valid_json_with_required_keys()` |
| `Server` | class | `tests/test_rea_mcp.py:46` | `class Server` |
| `TextContent` | class | `tests/test_rea_mcp.py:39` | `class TextContent` |
| `Tool` | class | `tests/test_rea_mcp.py:35` | `class Tool` |
| `__init__` | method | `tests/test_rea_mcp.py:36` | `def __init__(self)` |
| `__init__` | method | `tests/test_rea_mcp.py:40` | `def __init__(self)` |
| `__init__` | method | `tests/test_rea_mcp.py:47` | `def __init__(self)` |
| `_call` | function | `tests/test_rea_mcp.py:73` | `def _call(arguments, monkeypatch)` |
| `_fake_run` | function | `tests/test_rea_mcp.py:78` | `def _fake_run(argv)` |
| `_fake_run` | function | `tests/test_rea_mcp.py:138` | `def _fake_run(argv)` |
| `_stub_mcp_sdk` | function | `tests/test_rea_mcp.py:21` | `def _stub_mcp_sdk()` |
| `call_tool` | method | `tests/test_rea_mcp.py:53` | `def call_tool(self)` |
| `list_tools` | method | `tests/test_rea_mcp.py:50` | `def list_tools(self)` |
| `test_analyze_missing_target` | function | `tests/test_rea_mcp.py:155` | `def test_analyze_missing_target(monkeypatch)` |
| `test_analyze_uses_explicit_target` | function | `tests/test_rea_mcp.py:148` | `def test_analyze_uses_explicit_target(tmp_path, monkeypatch)` |
| `test_decompile_needs_valid_address` | function | `tests/test_rea_mcp.py:174` | `def test_decompile_needs_valid_address(tmp_path, monkeypatch)` |
| `test_doctor_argv` | function | `tests/test_rea_mcp.py:113` | `def test_doctor_argv(monkeypatch)` |
| `test_inspect_artifact_argv` | function | `tests/test_rea_mcp.py:119` | `def test_inspect_artifact_argv(tmp_path, monkeypatch)` |
| `test_large_output_survives_compaction` | function | `tests/test_rea_mcp.py:132` | `def test_large_output_survives_compaction(tmp_path, monkeypatch)` |
| `test_list_tools_has_rea` | function | `tests/test_rea_mcp.py:90` | `def test_list_tools_has_rea()` |
| `test_missing_binary` | function | `tests/test_rea_mcp.py:105` | `def test_missing_binary(monkeypatch)` |
| `test_provider_flag_appended` | function | `tests/test_rea_mcp.py:201` | `def test_provider_flag_appended(tmp_path, monkeypatch)` |
| `test_search_needs_query` | function | `tests/test_rea_mcp.py:189` | `def test_search_needs_query(tmp_path, monkeypatch)` |
| `test_target_flag_injection_rejected` | function | `tests/test_rea_mcp.py:168` | `def test_target_flag_injection_rejected(monkeypatch)` |
| `test_unknown_action_rejected` | function | `tests/test_rea_mcp.py:99` | `def test_unknown_action_rejected(monkeypatch)` |
| `TestCredentialExtraction` | class | `tests/test_reaction_bridge.py:44` | `class TestCredentialExtraction` |
| `TestDecisionBuffer` | class | `tests/test_reaction_bridge.py:10` | `class TestDecisionBuffer` |
| `test_assign_rhost_becomes_probe` | method | `tests/test_reaction_bridge.py:23` | `def test_assign_rhost_becomes_probe(self, monkeypatch, tmp_path)` |
| `test_dedupe_and_cap` | method | `tests/test_reaction_bridge.py:31` | `def test_dedupe_and_cap(self, monkeypatch, tmp_path)` |
| `test_hash_detected` | method | `tests/test_reaction_bridge.py:59` | `def test_hash_detected(self)` |
| `test_pair_lines_extracted` | method | `tests/test_reaction_bridge.py:47` | `def test_pair_lines_extracted(self)` |
| `test_placeholders_dropped` | method | `tests/test_reaction_bridge.py:53` | `def test_placeholders_dropped(self)` |
| `test_save_and_drain_roundtrip` | method | `tests/test_reaction_bridge.py:13` | `def test_save_and_drain_roundtrip(self, monkeypatch, tmp_path)` |
| `_ExplodingRAG` | class | `tests/test_reactive_engine_semantic.py:189` | `class _ExplodingRAG` |
| `_FakeRAG` | class | `tests/test_reactive_engine_semantic.py:33` | `class _FakeRAG` |
| `__init__` | method | `tests/test_reactive_engine_semantic.py:36` | `def __init__(self, hits, ready)` |
| `query` | method | `tests/test_reactive_engine_semantic.py:41` | `def query(self, text, n)` |
| `query` | method | `tests/test_reactive_engine_semantic.py:192` | `def query(self, text, n)` |
| `test_advisor_swallows_rag_query_errors` | function | `tests/test_reactive_engine_semantic.py:186` | `def test_advisor_swallows_rag_query_errors()` |
| `test_emits_priority_five_suggestion` | function | `tests/test_reactive_engine_semantic.py:75` | `def test_emits_priority_five_suggestion()` |
| `test_engine_uses_semantic_advisor_when_supplied` | function | `tests/test_reactive_engine_semantic.py:158` | `def test_engine_uses_semantic_advisor_when_supplied()` |
| `test_returns_empty_when_disabled_via_payload` | function | `tests/test_reactive_engine_semantic.py:55` | `def test_returns_empty_when_disabled_via_payload()` |
| `test_returns_empty_when_rag_unavailable` | function | `tests/test_reactive_engine_semantic.py:46` | `def test_returns_empty_when_rag_unavailable(monkeypatch)` |
| `test_skips_hits_without_command_prefix` | function | `tests/test_reactive_engine_semantic.py:142` | `def test_skips_hits_without_command_prefix()` |
| `test_skips_low_score_hits` | function | `tests/test_reactive_engine_semantic.py:99` | `def test_skips_low_score_hits()` |
| `test_skips_same_command_and_dedupes` | function | `tests/test_reactive_engine_semantic.py:115` | `def test_skips_same_command_and_dedupes()` |
| `TestExtractLabels` | class | `tests/test_reactive_hints.py:88` | `class TestExtractLabels` |
| `TestFirstToken` | class | `tests/test_reactive_hints.py:57` | `class TestFirstToken` |
| `TestRenderInlineHints` | class | `tests/test_reactive_hints.py:111` | `class TestRenderInlineHints` |
| `TestTruncate` | class | `tests/test_reactive_hints.py:71` | `class TestTruncate` |
| `_FakeAdvisor` | class | `tests/test_reactive_hints.py:29` | `class _FakeAdvisor` |
| `__init__` | method | `tests/test_reactive_hints.py:32` | `def __init__(self, suggestions)` |
| `advisor_with_three_hints` | function | `tests/test_reactive_hints.py:42` | `def advisor_with_three_hints()` |
| `empty_advisor` | function | `tests/test_reactive_hints.py:53` | `def empty_advisor()` |
| `suggest_next` | method | `tests/test_reactive_hints.py:36` | `def suggest_next(self, recent_commands, limit)` |
| `test_advisor_called_with_correct_command` | method | `tests/test_reactive_hints.py:137` | `def test_advisor_called_with_correct_command(self, advisor_with_three_hints)` |
| `test_all_skip_commands_are_skipped` | method | `tests/test_reactive_hints.py:149` | `def test_all_skip_commands_are_skipped(self, advisor_with_three_hints)` |
| `test_disabled_flag_skips_render` | method | `tests/test_reactive_hints.py:112` | `def test_disabled_flag_skips_render(self, advisor_with_three_hints)` |
| `test_empty_command_skips_render` | method | `tests/test_reactive_hints.py:122` | `def test_empty_command_skips_render(self, advisor_with_three_hints)` |
| `test_empty_string` | method | `tests/test_reactive_hints.py:64` | `def test_empty_string(self)` |
| `test_empty_suggestions_skips_render` | method | `tests/test_reactive_hints.py:127` | `def test_empty_suggestions_skips_render(self, empty_advisor)` |
| `test_exact_length_unchanged` | method | `tests/test_reactive_hints.py:75` | `def test_exact_length_unchanged(self)` |
| `test_exception_in_advisor_does_not_propagate` | method | `tests/test_reactive_hints.py:142` | `def test_exception_in_advisor_does_not_propagate(self)` |
| `test_extracts_first_word` | method | `tests/test_reactive_hints.py:58` | `def test_extracts_first_word(self)` |
| `test_falls_back_to_id_when_no_label` | method | `tests/test_reactive_hints.py:93` | `def test_falls_back_to_id_when_no_label(self)` |
| `test_limit_is_passed_to_advisor` | method | `tests/test_reactive_hints.py:155` | `def test_limit_is_passed_to_advisor(self, advisor_with_three_hints)` |
| `test_long_string_truncated` | method | `tests/test_reactive_hints.py:78` | `def test_long_string_truncated(self)` |
| `test_normal_command_renders_hint` | method | `tests/test_reactive_hints.py:132` | `def test_normal_command_renders_hint(self, advisor_with_three_hints)` |
| `test_picks_label_over_id` | method | `tests/test_reactive_hints.py:89` | `def test_picks_label_over_id(self)` |
| `test_respects_limit` | method | `tests/test_reactive_hints.py:101` | `def test_respects_limit(self)` |
| `test_short_string_unchanged` | method | `tests/test_reactive_hints.py:72` | `def test_short_string_unchanged(self)` |
| `test_single_word` | method | `tests/test_reactive_hints.py:61` | `def test_single_word(self)` |
| `test_skip_command_skips_render` | method | `tests/test_reactive_hints.py:117` | `def test_skip_command_skips_render(self, advisor_with_three_hints)` |
| `test_skips_empty_entries` | method | `tests/test_reactive_hints.py:97` | `def test_skips_empty_entries(self)` |

Next: [SYMBOLS_p41.md](SYMBOLS_p41.md)
