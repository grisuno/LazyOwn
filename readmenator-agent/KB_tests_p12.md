# Subsystem: tests (page 12 of 19)
Previous: [KB_tests_p11.md](KB_tests_p11.md)

## tests/test_lazygui_models.py
- Doc: Tests for lazygui domain models.
- Layer: testing
- Language: py
- Symbols:
  - `TestGraphNode` (class, line 30) `class TestGraphNode`
  - `TestGraphEdge` (class, line 74) `class TestGraphEdge`
  - `TestTopology` (class, line 105) `class TestTopology`
  - `TestBeaconResult` (class, line 143) `class TestBeaconResult`
  - `TestDashboardPayload` (class, line 196) `class TestDashboardPayload`
  - `TestCampaignSummary` (class, line 221) `class TestCampaignSummary`
  - `TestEventRecord` (class, line 256) `class TestEventRecord`
  - `TestSessionModel` (class, line 280) `class TestSessionModel`
  - `TestBackendKind` (class, line 303) `class TestBackendKind`
  - `TestEventLevel` (class, line 314) `class TestEventLevel`
  - `test_minimal_construction` (method, line 33) `def test_minimal_construction(self)`
  - `test_full_construction` (method, line 41) `def test_full_construction(self)`
  - `test_default_metadata` (method, line 56) `def test_default_metadata(self)`
  - `test_equality` (method, line 61) `def test_equality(self)`
  - `test_immutable` (method, line 68) `def test_immutable(self)`
  - `test_construction` (method, line 77) `def test_construction(self)`
  - `test_defaults` (method, line 91) `def test_defaults(self)`
  - `test_equality` (method, line 97) `def test_equality(self)`
  - `test_empty_topology` (method, line 108) `def test_empty_topology(self)`
  - `test_empty_classmethod` (method, line 115) `def test_empty_classmethod(self)`
  - `test_populated_topology` (method, line 120) `def test_populated_topology(self)`
  - `test_equality` (method, line 130) `def test_equality(self)`
  - `test_empty_list_keywords` (method, line 137) `def test_empty_list_keywords(self)`
  - `test_minimal_construction` (method, line 146) `def test_minimal_construction(self)`
  - `test_full_construction` (method, line 154) `def test_full_construction(self)`
  - `test_equality` (method, line 174) `def test_equality(self)`
  - `test_empty_fields_default_to_empty_string` (method, line 181) `def test_empty_fields_default_to_empty_string(self)`
  - `test_defaults` (method, line 199) `def test_defaults(self)`
  - `test_populated` (method, line 206) `def test_populated(self)`
  - `test_equality` (method, line 213) `def test_equality(self)`
  - `test_defaults` (method, line 224) `def test_defaults(self)`
  - `test_with_counts` (method, line 234) `def test_with_counts(self)`
  - `test_equality` (method, line 248) `def test_equality(self)`
  - `test_now_uses_utc` (method, line 259) `def test_now_uses_utc(self)`
  - `test_fields` (method, line 263) `def test_fields(self)`
  - `test_numeric_levels` (method, line 271) `def test_numeric_levels(self)`
  - `test_construction` (method, line 283) `def test_construction(self)`
  - `test_metadata_default` (method, line 298) `def test_metadata_default(self)`
  - `test_values` (method, line 306) `def test_values(self)`
  - `test_str_compat` (method, line 310) `def test_str_compat(self)`
  - `test_order` (method, line 317) `def test_order(self)`
  - `test_compare` (method, line 322) `def test_compare(self)`
- Depends on: `lazygui/services/models.py`

## tests/test_lazynmap_post.py
- Doc: Spec coverage for :mod:`cli.lazynmap_post`.
- Layer: testing
- Language: py
- Symbols:
  - `_seed_addon` (function, line 37) `def _seed_addon(addons)`
  - `_seed_environment` (function, line 59) `def _seed_environment(tmp)`
  - `_make_engine` (function, line 71) `def _make_engine(sessions, addons, tools)`
  - `_ConsoleRecorder` (class, line 81) `class _ConsoleRecorder`
  - `PostScanOutputSpec` (class, line 88) `class PostScanOutputSpec(TestCase)`
  - `PostScanToggleSpec` (class, line 186) `class PostScanToggleSpec(TestCase)`
  - `PostScanResilienceSpec` (class, line 228) `class PostScanResilienceSpec(TestCase)`
  - `print` (method, line 84) `def print(self, line)`
  - `test_writes_plan_world_model_and_event` (method, line 91) `def test_writes_plan_world_model_and_event(self)`
  - `test_world_model_is_merged_not_overwritten` (method, line 117) `def test_world_model_is_merged_not_overwritten(self)`
  - `test_event_record_carries_target_and_counts` (method, line 142) `def test_event_record_carries_target_and_counts(self)`
  - `test_console_receives_plan_preview_lines` (method, line 166) `def test_console_receives_plan_preview_lines(self)`
  - `test_disabled_payload_skips_all_writes` (method, line 189) `def test_disabled_payload_skips_all_writes(self)`
  - `test_string_falsy_toggle_is_respected` (method, line 210) `def test_string_falsy_toggle_is_respected(self)`
  - `test_engine_failure_still_emits_event_and_updates_world_model` (method, line 231) `def test_engine_failure_still_emits_event_and_updates_world_model(self)`
  - `_broken_factory` (function, line 235) `def _broken_factory()`
- Depends on: `cli/exploration.py`, `cli/lazynmap_post.py`, `cli/recon_plan.py`

## tests/test_lazynmap_sudo_branches.py
- Doc: LazyNmap sudo branches: unattended abort vs interactive prompt.
- Layer: testing
- Language: py
- Symbols:
  - `_fake_bin` (function, line 18) `def _fake_bin(tmp_path)`
  - `_run_script` (function, line 31) `def _run_script(tmp_path, extra_env)`
  - `test_autonomous_mode_aborts_without_passwordless_sudo` (function, line 48) `def test_autonomous_mode_aborts_without_passwordless_sudo(tmp_path)`
  - `test_interactive_mode_keeps_the_sudo_prompt_path` (function, line 55) `def test_interactive_mode_keeps_the_sudo_prompt_path(tmp_path)`

## tests/test_legacy_shims.py
- Doc: Legacy shim contract plus referenced-script existence.
- Layer: testing
- Language: py
- Symbols:
  - `TestLegacyShims` (class, line 23) `class TestLegacyShims`
  - `TestReferencedScriptsExist` (class, line 43) `class TestReferencedScriptsExist`
  - `test_no_regular_file_clones` (method, line 24) `def test_no_regular_file_clones(self)`
  - `test_symlinks_resolve_into_contrib` (method, line 32) `def test_symlinks_resolve_into_contrib(self)`
  - `test_exploit_migrated_script_paths` (method, line 44) `def test_exploit_migrated_script_paths(self)`

## tests/test_lesson_ingestor.py
- Doc: Tests for modules/lesson_ingestor.py.
- Layer: testing
- Language: py
- Symbols:
  - `TestLessonLearned` (class, line 15) `class TestLessonLearned`
  - `TestLessonIngestor` (class, line 35) `class TestLessonIngestor`
  - `test_from_dict` (method, line 16) `def test_from_dict(self)`
  - `test_from_dict_minimal` (method, line 29) `def test_from_dict_minimal(self)`
  - `test_expert_mapping` (method, line 36) `def test_expert_mapping(self)`
  - `test_ingest_with_mock_backends` (method, line 43) `def test_ingest_with_mock_backends(self, tmp_path)`
  - `test_ingest_unmapped_topic` (method, line 62) `def test_ingest_unmapped_topic(self, tmp_path)`
  - `test_ingest_no_backends` (method, line 79) `def test_ingest_no_backends(self, monkeypatch)`
  - `test_load_from_file` (method, line 99) `def test_load_from_file(self, tmp_path)`
  - `test_load_from_file_missing` (method, line 119) `def test_load_from_file_missing(self, tmp_path)`
  - `test_ingest_all` (method, line 124) `def test_ingest_all(self, tmp_path)`
- Depends on: `modules/lesson_ingestor.py`

## tests/test_lint_quality.py
- Doc: Lint quality gate.
- Layer: testing
- Language: py
- Symbols:
  - `_run_ruff` (function, line 63) `def _run_ruff(args)`
  - `test_ruff_check_clean` (function, line 75) `def test_ruff_check_clean(target)`
  - `test_ruff_format_clean` (function, line 84) `def test_ruff_format_clean(target)`
  - `test_lint_targets_exist` (function, line 94) `def test_lint_targets_exist()`
  - `test_format_targets_exist` (function, line 100) `def test_format_targets_exist()`

## tests/test_live_surface.py
- Doc: Tests for modules/live_surface.py.
- Layer: testing
- Language: py
- Symbols:
  - `_world` (function, line 25) `def _world()`
  - `test_empty_world_is_well_formed` (function, line 55) `def test_empty_world_is_well_formed()`
  - `test_none_world_is_tolerated` (function, line 63) `def test_none_world_is_tolerated()`
  - `test_hosts_and_services_become_nodes` (function, line 68) `def test_hosts_and_services_become_nodes()`
  - `test_owned_host_pulses_and_counts_as_compromised` (function, line 79) `def test_owned_host_pulses_and_counts_as_compromised()`
  - `test_host_with_credential_pulses_even_if_not_owned` (function, line 87) `def test_host_with_credential_pulses_even_if_not_owned()`
  - `test_runs_service_edge_is_emitted_once` (function, line 95) `def test_runs_service_edge_is_emitted_once()`
  - `test_stats_block_counts` (function, line 102) `def test_stats_block_counts()`
  - `test_malformed_host_entry_is_skipped` (function, line 109) `def test_malformed_host_entry_is_skipped()`
  - `test_compromised_states_constant_matches_world_model` (function, line 116) `def test_compromised_states_constant_matches_world_model()`
- Depends on: `modules/live_surface.py`

## tests/test_llm_adapter_parity.py
- Doc: Parity contract tests for the self-contained Groq adapter family.
- Layer: testing
- Language: py
- Symbols:
  - `_FakeCompletions` (class, line 23) `class _FakeCompletions`
  - `_FakeClient` (class, line 37) `class _FakeClient`
  - `cfg` (function, line 44) `def cfg(tmp_path)`
  - `patched` (function, line 55) `def patched(monkeypatch, cfg)`
  - `_write` (function, line 60) `def _write(path, text)`
  - `TestMissingClient` (class, line 65) `class TestMissingClient`
  - `TestUninitializedClient` (class, line 88) `class TestUninitializedClient`
  - `TestDirectPromptFlow` (class, line 94) `class TestDirectPromptFlow`
  - `TestKnowledgePersistence` (class, line 113) `class TestKnowledgePersistence`
  - `TestFileReadingVariants` (class, line 129) `class TestFileReadingVariants`
  - `TestVulnAugmentation` (class, line 147) `class TestVulnAugmentation`
  - `TestExports` (class, line 171) `class TestExports`
  - `_FakeBackend` (class, line 191) `class _FakeBackend`
  - `TestAskGeneral` (class, line 205) `class TestAskGeneral`
  - `__init__` (method, line 24) `def __init__(self, content)`
  - `create` (method, line 30) `def create(self, model, messages, max_tokens)`
  - `__init__` (method, line 38) `def __init__(self, content)`
  - `test_direct_variants_report_missing_key` (method, line 76) `def test_direct_variants_report_missing_key(self, patched, name)`
  - `test_file_variants_report_missing_key` (method, line 81) `def test_file_variants_report_missing_key(self, patched, name, tmp_path)`
  - `test_complete_error_handled` (method, line 89) `def test_complete_error_handled(self, patched)`
  - `test_sends_user_message_and_returns_content` (method, line 95) `def test_sends_user_message_and_returns_content(self, patched)`
  - `test_completion_received_single_user_message` (method, line 100) `def test_completion_received_single_user_message(self, patched)`
  - `test_default_max_tokens_applied` (method, line 107) `def test_default_max_tokens_applied(self, patched)`
  - `test_successful_response_is_remembered` (method, line 114) `def test_successful_response_is_remembered(self, patched, cfg)`
  - `test_error_response_not_remembered` (method, line 122) `def test_error_response_not_remembered(self, patched, cfg)`
  - `test_task_reads_file_content` (method, line 130) `def test_task_reads_file_content(self, patched, tmp_path)`
  - `test_task_missing_file_returns_error` (method, line 137) `def test_task_missing_file_returns_error(self, patched, tmp_path)`
  - `test_redop_reads_file_content` (method, line 141) `def test_redop_reads_file_content(self, patched, tmp_path)`
  - `test_appends_event_tool_output` (method, line 148) `def test_appends_event_tool_output(self, patched, cfg, tmp_path)`
  - `test_appends_plan_history` (method, line 161) `def test_appends_plan_history(self, patched, cfg, tmp_path)`
  - `test_groq_family_exports_present` (method, line 172) `def test_groq_family_exports_present(self)`
  - `test_safe_groq_client_none_without_key` (method, line 186) `def test_safe_groq_client_none_without_key(self)`
  - `__init__` (method, line 192) `def __init__(self, result)`
  - `complete` (method, line 197) `def complete(self, system, user)`
  - `test_uses_configured_backend` (method, line 206) `def test_uses_configured_backend(self, patched, monkeypatch)`
  - `test_receives_system_and_rendered_user` (method, line 213) `def test_receives_system_and_rendered_user(self, patched, monkeypatch)`
  - `test_missing_backend_reports_error` (method, line 223) `def test_missing_backend_reports_error(self, patched, monkeypatch)`
  - `test_backend_exception_reports_error` (method, line 230) `def test_backend_exception_reports_error(self, patched, monkeypatch)`
  - `test_backend_error_string_not_remembered` (method, line 237) `def test_backend_error_string_not_remembered(self, patched, cfg, monkeypatch)`
  - `test_successful_answer_remembered` (method, line 246) `def test_successful_answer_remembered(self, patched, cfg, monkeypatch)`
  - `test_exported` (method, line 257) `def test_exported(self)`
- Depends on: `modules/llm_adapter.py`, `modules/llm_factory.py`, `modules/llm_prompts.py`

## tests/test_llm_budget.py
- Doc: Contract tests for the LLM budget cap.
- Layer: testing
- Language: py
- Symbols:
  - `tmp_sessions` (function, line 27) `def tmp_sessions(tmp_path, monkeypatch)`
  - `test_budget_module_is_importable` (function, line 35) `def test_budget_module_is_importable()`
  - `test_budget_config_dataclass_carries_expected_fields` (function, line 51) `def test_budget_config_dataclass_carries_expected_fields()`
  - `test_token_estimator_counts_text_tokens` (function, line 71) `def test_token_estimator_counts_text_tokens()`
  - `test_token_estimator_handles_empty_string` (function, line 81) `def test_token_estimator_handles_empty_string()`
  - `test_token_estimator_is_deterministic` (function, line 89) `def test_token_estimator_is_deterministic()`
  - `test_budget_ledger_records_a_charge` (function, line 99) `def test_budget_ledger_records_a_charge(tmp_path)`
  - `test_budget_ledger_persists_to_disk` (function, line 116) `def test_budget_ledger_persists_to_disk(tmp_sessions)`
  - `test_budget_ledger_rolls_over_at_midnight` (function, line 136) `def test_budget_ledger_rolls_over_at_midnight(tmp_sessions)`
  - `test_budget_guard_refuses_call_when_daily_budget_exhausted` (function, line 162) `def test_budget_guard_refuses_call_when_daily_budget_exhausted(tmp_sessions)`
  - `test_budget_guard_refuses_call_when_token_cap_exceeded` (function, line 195) `def test_budget_guard_refuses_call_when_token_cap_exceeded(tmp_sessions)`
  - `test_budget_guard_charges_a_successful_call` (function, line 218) `def test_budget_guard_charges_a_successful_call(tmp_sessions)`
  - `test_budget_guard_disabled_passes_through` (function, line 242) `def test_budget_guard_disabled_passes_through(tmp_sessions)`
  - `test_format_budget_status_includes_spent_and_remaining` (function, line 265) `def test_format_budget_status_includes_spent_and_remaining(tmp_sessions)`
  - `test_read_budget_status_returns_dict` (function, line 287) `def test_read_budget_status_returns_dict(tmp_sessions)`
  - `test_wrap_backend_with_budget_returns_same_shape` (function, line 307) `def test_wrap_backend_with_budget_returns_same_shape(tmp_sessions)`
  - `test_wrap_backend_with_budget_charges_call` (function, line 347) `def test_wrap_backend_with_budget_charges_call(tmp_sessions)`
  - `test_payload_schema_recognises_budget_keys` (function, line 384) `def test_payload_schema_recognises_budget_keys()`
  - `test_load_budget_config_reads_payload` (function, line 395) `def test_load_budget_config_reads_payload(tmp_sessions)`
  - `_StubBackend` (class, line 316) `class _StubBackend`
  - `_StubBackend` (class, line 356) `class _StubBackend`
  - `generate` (method, line 317) `def generate(self, prompt)`
  - `stream_generate` (method, line 320) `def stream_generate(self, prompt)`
  - `complete` (method, line 323) `def complete(self, system, user, max_tokens, temperature)`
  - `generate` (method, line 357) `def generate(self, prompt)`
  - `stream_generate` (method, line 360) `def stream_generate(self, prompt)`
  - `complete` (method, line 363) `def complete(self, system, user, max_tokens, temperature)`
- Depends on: `core/__init__.py`, `core/llm_budget.py`

## tests/test_llm_contract.py
- Doc: LLM subsystem contract tests.
- Layer: testing
- Language: py
- Symbols:
  - `_import` (function, line 46) `def _import(name)`
  - `TestDeadModuleRemoved` (class, line 50) `class TestDeadModuleRemoved`
  - `TestLlmFactoryContract` (class, line 56) `class TestLlmFactoryContract`
  - `TestSupportModulesContract` (class, line 86) `class TestSupportModulesContract`
  - `TestBackendMetadataContract` (class, line 114) `class TestBackendMetadataContract`
  - `test_unified_llm_client_does_not_exist` (method, line 51) `def test_unified_llm_client_does_not_exist(self)`
  - `test_factory_importable` (method, line 57) `def test_factory_importable(self)`
  - `test_factory_exposes_public_api` (method, line 60) `def test_factory_exposes_public_api(self)`
  - `test_supported_backends_are_canonical` (method, line 65) `def test_supported_backends_are_canonical(self)`
  - `test_backend_constants_exposed` (method, line 69) `def test_backend_constants_exposed(self)`
  - `test_normalize_rejects_unknown_backend` (method, line 75) `def test_normalize_rejects_unknown_backend(self)`
  - `test_normalize_falls_back_to_auto_on_empty` (method, line 80) `def test_normalize_falls_back_to_auto_on_empty(self)`
  - `test_llm_client_exposes_public_api` (method, line 87) `def test_llm_client_exposes_public_api(self)`
  - `test_llm_client_class_methods_present` (method, line 92) `def test_llm_client_class_methods_present(self)`
  - `test_ai_fallback_exposes_public_api` (method, line 97) `def test_ai_fallback_exposes_public_api(self)`
  - `test_ai_model_exposes_all_backends` (method, line 102) `def test_ai_model_exposes_all_backends(self)`
  - `test_ai_fallback_reads_factory_constants` (method, line 107) `def test_ai_fallback_reads_factory_constants(self)`
  - `test_metadata_helpers_exposed` (method, line 115) `def test_metadata_helpers_exposed(self)`
  - `test_default_models_match_constants` (method, line 125) `def test_default_models_match_constants(self)`
  - `test_model_config_keys_match_constants` (method, line 135) `def test_model_config_keys_match_constants(self)`
  - `test_api_key_slots` (method, line 144) `def test_api_key_slots(self)`
  - `test_requires_api_key_only_for_cloud` (method, line 153) `def test_requires_api_key_only_for_cloud(self)`
  - `test_unknown_backend_rejected` (method, line 159) `def test_unknown_backend_rejected(self)`

## tests/test_llm_legacy_isolation.py
- Doc: Watchdog: core must not depend on the retired legacy Groq LLM scripts.
- Layer: testing
- Language: py
- Symbols:
  - `_core_source_files` (function, line 33) `def _core_source_files()`
  - `_imported_targets` (function, line 47) `def _imported_targets(node)`
  - `TestNoLegacyGroqImportInCore` (class, line 61) `class TestNoLegacyGroqImportInCore`
  - `test_no_core_file_imports_legacy_groq` (method, line 62) `def test_no_core_file_imports_legacy_groq(self)`

## tests/test_llm_prompts.py
- Doc: Contract tests for :mod:`modules.llm_prompts`.
- Layer: testing
- Language: py
- Symbols:
  - `_write_json` (function, line 23) `def _write_json(path, payload)`
  - `_config` (function, line 29) `def _config(tmp_path)`
  - `TestTruncateMessage` (class, line 39) `class TestTruncateMessage`
  - `TestKnowledgeStore` (class, line 53) `class TestKnowledgeStore`
  - `TestConfig` (class, line 83) `class TestConfig`
  - `TestTemplates` (class, line 129) `class TestTemplates`
  - `TestRegistryIntegrity` (class, line 157) `class TestRegistryIntegrity`
  - `test_short_message_returned_unchanged` (method, line 40) `def test_short_message_returned_unchanged(self)`
  - `test_long_message_truncated_with_ellipsis` (method, line 43) `def test_long_message_truncated_with_ellipsis(self)`
  - `test_boundary_length_kept` (method, line 48) `def test_boundary_length_kept(self)`
  - `test_load_missing_file_returns_empty` (method, line 54) `def test_load_missing_file_returns_empty(self, tmp_path)`
  - `test_load_malformed_file_returns_empty` (method, line 58) `def test_load_malformed_file_returns_empty(self, tmp_path)`
  - `test_add_and_load_roundtrip` (method, line 63) `def test_add_and_load_roundtrip(self, tmp_path)`
  - `test_relevant_filters_on_keyword` (method, line 69) `def test_relevant_filters_on_keyword(self, tmp_path)`
  - `test_relevant_limits_results` (method, line 76) `def test_relevant_limits_results(self, tmp_path)`
  - `test_from_defaults_points_under_module_parent` (method, line 84) `def test_from_defaults_points_under_module_parent(self, tmp_path, monkeypatch)`
  - `test_knowledge_base_path_resolves_names` (method, line 90) `def test_knowledge_base_path_resolves_names(self, tmp_path)`
  - `test_payload_context_defaults_to_empty` (method, line 94) `def test_payload_context_defaults_to_empty(self, tmp_path)`
  - `test_payload_context_reads_values` (method, line 109) `def test_payload_context_reads_values(self, tmp_path)`
  - `test_event_tool_output_empty_when_no_match` (method, line 116) `def test_event_tool_output_empty_when_no_match(self, tmp_path)`
  - `test_event_tool_output_reads_file` (method, line 121) `def test_event_tool_output_reads_file(self, tmp_path)`
  - `test_render_includes_operator_prompt` (method, line 131) `def test_render_includes_operator_prompt(self, tmp_path, name)`
  - `test_render_embeds_knowledge_tail` (method, line 137) `def test_render_embeds_knowledge_tail(self, tmp_path, name)`
  - `test_general_embeds_payload_rhost` (method, line 144) `def test_general_embeds_payload_rhost(self, tmp_path)`
  - `test_vuln_embeds_payload_rhost` (method, line 150) `def test_vuln_embeds_payload_rhost(self, tmp_path)`
  - `test_kb_domains_are_valid_file_names` (method, line 158) `def test_kb_domains_are_valid_file_names(self)`
  - `test_all_templates_have_registered_kb_domain` (method, line 164) `def test_all_templates_have_registered_kb_domain(self)`
- Depends on: `modules/llm_prompts.py`

## tests/test_logging_config.py
- Doc: Tests for ``modules.logging_config`` — resilient file logging.
- Layer: testing
- Language: py
- Symbols:
  - `_make_logger` (function, line 13) `def _make_logger(handler)`
  - `TestResilientRotatingFileHandler` (class, line 21) `class TestResilientRotatingFileHandler`
  - `test_writes_normally_when_dir_writable` (method, line 22) `def test_writes_normally_when_dir_writable(self, tmp_path)`
  - `test_detaches_silently_when_file_unwritable` (method, line 32) `def test_detaches_silently_when_file_unwritable(self, tmp_path, capsys)`
  - `test_rotating_file_is_exposed` (method, line 47) `def test_rotating_file_is_exposed(self)`
- Depends on: `core/logging.py`, `modules/logging_config.py`

## tests/test_loop_ai_bridge.py
- Doc: Loop AI-stack bridge: event bus, oracle, MoE/RL and SWAN wiring.
- Layer: testing
- Language: py
- Symbols:
  - `store` (function, line 15) `def store(tmp_path, monkeypatch)`
  - `bridge` (function, line 25) `def bridge(monkeypatch)`
  - `test_publish_loop_event_skips_stream_kinds` (function, line 34) `def test_publish_loop_event_skips_stream_kinds(bridge, monkeypatch)`
  - `test_activity_log_publishes_to_bridge` (function, line 52) `def test_activity_log_publishes_to_bridge(store, bridge, monkeypatch)`
  - `test_annotate_detection_uses_oracle` (function, line 62) `def test_annotate_detection_uses_oracle(bridge, monkeypatch)`
  - `test_worker_annotates_detection_and_records_outcome` (function, line 74) `def test_worker_annotates_detection_and_records_outcome(store, bridge, monkeypatch)`
  - `test_llm_pool_prefers_moe_expert_and_records_outcome` (function, line 108) `def test_llm_pool_prefers_moe_expert_and_records_outcome(store, bridge, monkeypatch)`
  - `test_planner_uses_swan_when_available` (function, line 133) `def test_planner_uses_swan_when_available(store, bridge, monkeypatch)`
  - `_Bus` (class, line 38) `class _Bus`
  - `_Oracle` (class, line 63) `class _Oracle`
  - `_complete` (function, line 120) `def _complete(model, prompt, max_tokens)`
  - `_swan` (function, line 140) `def _swan(prompt, task_type, phase, timeout)`
  - `publish` (method, line 39) `def publish(self, event)`
  - `assess` (method, line 64) `def assess(self, tool, command, category)`
- Depends on: `modules/detection_oracle.py`, `modules/event_bus.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop_ai_bridge.py`

## tests/test_loop_auto_orchestrator.py
- Doc: Loop orchestrates every auto verb plus addon/tool triggers.
- Layer: testing
- Language: py
- Symbols:
  - `test_exfil_auto_registered_as_verb` (function, line 6) `def test_exfil_auto_registered_as_verb()`
  - `test_service_tokens_split_and_alias` (function, line 15) `def test_service_tokens_split_and_alias()`
  - `test_addon_hits_rank_specific_before_generic` (function, line 22) `def test_addon_hits_rank_specific_before_generic()`
  - `test_propose_addon_intents_shape_and_tool_collapse` (function, line 31) `def test_propose_addon_intents_shape_and_tool_collapse()`
  - `test_steps_for_lazy_addon_routes_to_command` (function, line 40) `def test_steps_for_lazy_addon_routes_to_command()`
  - `test_worker_routes_verbs_via_bound_shell` (function, line 49) `def test_worker_routes_verbs_via_bound_shell(tmp_path, monkeypatch)`
  - `test_worker_without_shell_reports_honestly` (function, line 85) `def test_worker_without_shell_reports_honestly(tmp_path, monkeypatch)`
  - `test_execute_streaming_streams_and_captures` (function, line 109) `def test_execute_streaming_streams_and_captures()`
  - `test_execute_streaming_timeout_reports` (function, line 119) `def test_execute_streaming_timeout_reports()`
  - `test_execute_shell_verb_forwards_output` (function, line 127) `def test_execute_shell_verb_forwards_output()`
  - `test_autonomous_mode_suppresses_and_restores_input` (function, line 141) `def test_autonomous_mode_suppresses_and_restores_input(monkeypatch)`
  - `test_lazy_addon_command_registered` (function, line 153) `def test_lazy_addon_command_registered()`
  - `test_worker_skips_missing_binary_and_records_gap` (function, line 163) `def test_worker_skips_missing_binary_and_records_gap(tmp_path, monkeypatch)`
  - `test_service_trigger_fires_with_addon_hits` (function, line 194) `def test_service_trigger_fires_with_addon_hits(tmp_path, monkeypatch)`
  - `_Shell` (class, line 59) `class _Shell`
  - `_Shell` (class, line 131) `class _Shell`
  - `onecmd` (method, line 60) `def onecmd(self, command)`
  - `onecmd_plus_hooks` (method, line 132) `def onecmd_plus_hooks(self, command)`
- Depends on: `cli/commands/mcp_bridge.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_broadcast.py
- Doc: Broadcast board timeline regression tests (lazy 0.3.12 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_broadcast_rows_carry_neighbours_and_assets` (function, line 15) `def test_broadcast_rows_carry_neighbours_and_assets(tmp_path, monkeypatch)`
  - `test_broadcast_search_id_and_kind_filter` (function, line 36) `def test_broadcast_search_id_and_kind_filter(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_budget.py
- Doc: BDD tests for first-class budget flags on the loop runner.
- Layer: testing
- Language: py
- Symbols:
  - `TestBudgetParsing` (class, line 10) `class TestBudgetParsing`
  - `math_close` (function, line 38) `def math_close(budget)`
  - `TestBudgetGate` (class, line 42) `class TestBudgetGate`
  - `test_budget_pairs_parsed` (method, line 13) `def test_budget_pairs_parsed(self)`
  - `test_minimums_clamped` (method, line 19) `def test_minimums_clamped(self)`
  - `test_unknown_key_rejected` (method, line 25) `def test_unknown_key_rejected(self)`
  - `test_budget_confirm_toggle` (method, line 31) `def test_budget_confirm_toggle(self)`
  - `test_gate_blocks_when_declined` (method, line 45) `def test_gate_blocks_when_declined(self, monkeypatch)`
  - `test_gate_pass_when_approved` (method, line 55) `def test_gate_pass_when_approved(self, monkeypatch)`
  - `test_gate_skipped_autonomous` (method, line 65) `def test_gate_skipped_autonomous(self, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/lazy_runner.py`

## tests/test_loop_cli_catalog.py
- Doc: BDD tests for planner prompt visibility into routable CLI verbs.
- Layer: testing
- Language: py
- Symbols:
  - `sandbox` (function, line 17) `def sandbox(tmp_path, monkeypatch)`
  - `test_catalog_cli_for_phase_lists_enabled_only` (function, line 56) `def test_catalog_cli_for_phase_lists_enabled_only(sandbox)`
  - `test_prompt_context_carries_allowed_commands` (function, line 66) `def test_prompt_context_carries_allowed_commands(sandbox)`
  - `test_missing_catalog_view_adds_nothing` (function, line 79) `def test_missing_catalog_view_adds_nothing(tmp_path, monkeypatch)`
  - `_default` (function, line 47) `def _default(cfg)`
  - `_broken` (function, line 90) `def _broken()`
- Depends on: `modules/__init__.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_loop.py`, `modules/verb_catalog.py`, `modules/world_model.py`

## tests/test_loop_cold_overview.py
- Doc: Cold debounce + planner overview parity (lazy 0.3.8 coldgraph).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `_old_facts` (function, line 15) `def _old_facts(graph, count, prefix)`
  - `test_compact_debounce_keeps_fresh_hot` (function, line 28) `def test_compact_debounce_keeps_fresh_hot(tmp_path, monkeypatch)`
  - `test_compact_folds_stale_facts` (function, line 41) `def test_compact_folds_stale_facts(tmp_path, monkeypatch)`
  - `test_planner_round_folds_minor_window` (function, line 56) `def test_planner_round_folds_minor_window(tmp_path, monkeypatch)`
  - `test_graph_overview_carries_findings_and_done_totals` (function, line 77) `def test_graph_overview_carries_findings_and_done_totals(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_force_graph.py
- Doc: Loop ForceGraph context regression tests (lazy 0.3.12 fidelity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_loop_graph_is_forcegraph_ready` (function, line 15) `def test_loop_graph_is_forcegraph_ready(tmp_path, monkeypatch)`
  - `test_graph_context_surfaces_hubs_and_next` (function, line 32) `def test_graph_context_surfaces_hubs_and_next(tmp_path, monkeypatch)`
  - `test_planner_force_ranks_connected_surface` (function, line 53) `def test_planner_force_ranks_connected_surface(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_guard_audit.py
- Doc: Guard audit filters + tool_use_id source jump (lazy 0.3.11/0.3.12 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_check_mints_tool_use_id` (function, line 15) `def test_check_mints_tool_use_id(tmp_path, monkeypatch)`
  - `test_audit_filters_action_source_query` (function, line 31) `def test_audit_filters_action_source_query(tmp_path, monkeypatch)`
  - `test_lookup_jumps_to_execution` (function, line 48) `def test_lookup_jumps_to_execution(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_intent_delete.py
- Doc: Intent delete modes regression tests (lazy 0.3.12 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 8) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_soft_delete_keeps_outputs_and_notifies` (function, line 17) `def test_soft_delete_keeps_outputs_and_notifies(tmp_path, monkeypatch)`
  - `test_soft_delete_requires_reason` (function, line 37) `def test_soft_delete_requires_reason(tmp_path, monkeypatch)`
  - `test_hard_delete_removes_exclusive_keeps_shared` (function, line 46) `def test_hard_delete_removes_exclusive_keeps_shared(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_llm_resilience.py
- Doc: LLM retry layers, wall-clock settle, stall-guard (lazy 0.3.8/0.3.9 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_empty_reply_replays_before_failover` (function, line 15) `def test_empty_reply_replays_before_failover(tmp_path, monkeypatch)`
  - `test_empty_budget_exhausted_moves_to_next_member` (function, line 34) `def test_empty_budget_exhausted_moves_to_next_member(tmp_path, monkeypatch)`
  - `test_error_reply_fails_over_instead_of_becoming_content` (function, line 54) `def test_error_reply_fails_over_instead_of_becoming_content(tmp_path, monkeypatch)`
  - `test_worker_llm_steps_filtered_by_scope_and_tooling` (function, line 71) `def test_worker_llm_steps_filtered_by_scope_and_tooling(tmp_path, monkeypatch)`
  - `test_wall_clock_settles_partial_not_hard_kill` (function, line 95) `def test_wall_clock_settles_partial_not_hard_kill(tmp_path, monkeypatch)`
  - `test_stall_guard_forces_intent_when_nothing_open` (function, line 114) `def test_stall_guard_forces_intent_when_nothing_open(tmp_path, monkeypatch)`
  - `test_task_llm_chain_quota_failover` (function, line 135) `def test_task_llm_chain_quota_failover(tmp_path, monkeypatch)`
  - `test_raw_llm_recording_toggle` (function, line 169) `def test_raw_llm_recording_toggle(tmp_path, monkeypatch)`
  - `test_llm_context_budget_roundtrip` (function, line 190) `def test_llm_context_budget_roundtrip(tmp_path, monkeypatch)`
  - `test_planner_uses_bound_task_chain` (function, line 202) `def test_planner_uses_bound_task_chain(tmp_path, monkeypatch)`
  - `scripted` (function, line 23) `def scripted(model, prompt, max_tokens)`
  - `first_empty_then_ok` (function, line 42) `def first_empty_then_ok(model, prompt, max_tokens)`
  - `error_then_ok` (function, line 61) `def error_then_ok(model, prompt, max_tokens)`
  - `scripted` (function, line 79) `def scripted(model, prompt, max_tokens)`
  - `scripted` (function, line 147) `def scripted(model, prompt, max_tokens)`
  - `scripted_next` (function, line 160) `def scripted_next(model, prompt, max_tokens)`
  - `scripted` (function, line 213) `def scripted(model, prompt, max_tokens)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`

## tests/test_loop_mentions.py
- Doc: Lazy mentions multi-type search and scroll pagination.
- Layer: testing
- Language: py
- Symbols:
  - `test_mentions_search_and_cursor` (function, line 6) `def test_mentions_search_and_cursor(tmp_path, monkeypatch)`
  - `test_mentions_parse_caps_and_trusts_ids` (function, line 16) `def test_mentions_parse_caps_and_trusts_ids()`
- Depends on: `modules/__init__.py`

## tests/test_loop_nmap_guard.py
- Doc: Loop guardrails: command repair and bounded scanning retests.
- Layer: testing
- Language: py
- Symbols:
  - `_sandbox` (function, line 8) `def _sandbox(tmp_path, monkeypatch)`
  - `test_repair_rejects_target_in_port_slot` (function, line 13) `def test_repair_rejects_target_in_port_slot()`
  - `test_repair_strips_binary_path_for_shell_verb` (function, line 20) `def test_repair_strips_binary_path_for_shell_verb()`
  - `test_repair_keeps_valid_port_specs` (function, line 27) `def test_repair_keeps_valid_port_specs()`
  - `test_repair_appends_missing_target` (function, line 35) `def test_repair_appends_missing_target()`
  - `test_repair_drops_port_flag_without_value` (function, line 41) `def test_repair_drops_port_flag_without_value()`
  - `test_stall_thresholds_follow_command_timeout` (function, line 48) `def test_stall_thresholds_follow_command_timeout()`
  - `test_scan_commands_are_not_replayed` (function, line 58) `def test_scan_commands_are_not_replayed(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_loop.py`, `modules/lazy_runner.py`


Next: [KB_tests_p13.md](KB_tests_p13.md)
