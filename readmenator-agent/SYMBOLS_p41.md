# Symbols (page 41 of 47)
Previous: [SYMBOLS_p40.md](SYMBOLS_p40.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_receives_system_and_rendered_user` | method | `tests/test_llm_adapter_parity.py:230` | `def test_receives_system_and_rendered_user(self, patched, monkeypatch)` |
| `test_redop_reads_file_content` | method | `tests/test_llm_adapter_parity.py:158` | `def test_redop_reads_file_content(self, patched, tmp_path)` |
| `test_safe_groq_client_none_without_key` | method | `tests/test_llm_adapter_parity.py:203` | `def test_safe_groq_client_none_without_key(self)` |
| `test_sends_user_message_and_returns_content` | method | `tests/test_llm_adapter_parity.py:112` | `def test_sends_user_message_and_returns_content(self, patched)` |
| `test_successful_answer_remembered` | method | `tests/test_llm_adapter_parity.py:263` | `def test_successful_answer_remembered(self, patched, cfg, monkeypatch)` |
| `test_successful_response_is_remembered` | method | `tests/test_llm_adapter_parity.py:131` | `def test_successful_response_is_remembered(self, patched, cfg)` |
| `test_task_missing_file_returns_error` | method | `tests/test_llm_adapter_parity.py:154` | `def test_task_missing_file_returns_error(self, patched, tmp_path)` |
| `test_task_reads_file_content` | method | `tests/test_llm_adapter_parity.py:147` | `def test_task_reads_file_content(self, patched, tmp_path)` |
| `test_uses_configured_backend` | method | `tests/test_llm_adapter_parity.py:223` | `def test_uses_configured_backend(self, patched, monkeypatch)` |
| `_StubBackend` | class | `tests/test_llm_budget.py:316` | `class _StubBackend` |
| `_StubBackend` | class | `tests/test_llm_budget.py:356` | `class _StubBackend` |
| `complete` | method | `tests/test_llm_budget.py:323` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `tests/test_llm_budget.py:363` | `def complete(self, system, user, max_tokens, temperature)` |
| `generate` | method | `tests/test_llm_budget.py:317` | `def generate(self, prompt)` |
| `generate` | method | `tests/test_llm_budget.py:357` | `def generate(self, prompt)` |
| `stream_generate` | method | `tests/test_llm_budget.py:320` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `tests/test_llm_budget.py:360` | `def stream_generate(self, prompt)` |
| `test_budget_config_dataclass_carries_expected_fields` | function | `tests/test_llm_budget.py:51` | `def test_budget_config_dataclass_carries_expected_fields()` |
| `test_budget_guard_charges_a_successful_call` | function | `tests/test_llm_budget.py:218` | `def test_budget_guard_charges_a_successful_call(tmp_sessions)` |
| `test_budget_guard_disabled_passes_through` | function | `tests/test_llm_budget.py:242` | `def test_budget_guard_disabled_passes_through(tmp_sessions)` |
| `test_budget_guard_refuses_call_when_daily_budget_exhausted` | function | `tests/test_llm_budget.py:162` | `def test_budget_guard_refuses_call_when_daily_budget_exhausted(tmp_sessions)` |
| `test_budget_guard_refuses_call_when_token_cap_exceeded` | function | `tests/test_llm_budget.py:195` | `def test_budget_guard_refuses_call_when_token_cap_exceeded(tmp_sessions)` |
| `test_budget_ledger_persists_to_disk` | function | `tests/test_llm_budget.py:116` | `def test_budget_ledger_persists_to_disk(tmp_sessions)` |
| `test_budget_ledger_records_a_charge` | function | `tests/test_llm_budget.py:99` | `def test_budget_ledger_records_a_charge(tmp_path)` |
| `test_budget_ledger_rolls_over_at_midnight` | function | `tests/test_llm_budget.py:136` | `def test_budget_ledger_rolls_over_at_midnight(tmp_sessions)` |
| `test_budget_module_is_importable` | function | `tests/test_llm_budget.py:35` | `def test_budget_module_is_importable()` |
| `test_format_budget_status_includes_spent_and_remaining` | function | `tests/test_llm_budget.py:265` | `def test_format_budget_status_includes_spent_and_remaining(tmp_sessions)` |
| `test_load_budget_config_reads_payload` | function | `tests/test_llm_budget.py:395` | `def test_load_budget_config_reads_payload(tmp_sessions)` |
| `test_payload_schema_recognises_budget_keys` | function | `tests/test_llm_budget.py:384` | `def test_payload_schema_recognises_budget_keys()` |
| `test_read_budget_status_returns_dict` | function | `tests/test_llm_budget.py:287` | `def test_read_budget_status_returns_dict(tmp_sessions)` |
| `test_token_estimator_counts_text_tokens` | function | `tests/test_llm_budget.py:71` | `def test_token_estimator_counts_text_tokens()` |
| `test_token_estimator_handles_empty_string` | function | `tests/test_llm_budget.py:81` | `def test_token_estimator_handles_empty_string()` |
| `test_token_estimator_is_deterministic` | function | `tests/test_llm_budget.py:89` | `def test_token_estimator_is_deterministic()` |
| `test_wrap_backend_with_budget_charges_call` | function | `tests/test_llm_budget.py:347` | `def test_wrap_backend_with_budget_charges_call(tmp_sessions)` |
| `test_wrap_backend_with_budget_returns_same_shape` | function | `tests/test_llm_budget.py:307` | `def test_wrap_backend_with_budget_returns_same_shape(tmp_sessions)` |
| `tmp_sessions` | function | `tests/test_llm_budget.py:27` | `def tmp_sessions(tmp_path, monkeypatch)` |
| `TestBackendMetadataContract` | class | `tests/test_llm_contract.py:114` | `class TestBackendMetadataContract` |
| `TestDeadModuleRemoved` | class | `tests/test_llm_contract.py:50` | `class TestDeadModuleRemoved` |
| `TestLlmFactoryContract` | class | `tests/test_llm_contract.py:56` | `class TestLlmFactoryContract` |
| `TestSupportModulesContract` | class | `tests/test_llm_contract.py:86` | `class TestSupportModulesContract` |
| `_import` | function | `tests/test_llm_contract.py:46` | `def _import(name)` |
| `test_ai_fallback_exposes_public_api` | method | `tests/test_llm_contract.py:97` | `def test_ai_fallback_exposes_public_api(self)` |
| `test_ai_fallback_reads_factory_constants` | method | `tests/test_llm_contract.py:107` | `def test_ai_fallback_reads_factory_constants(self)` |
| `test_ai_model_exposes_all_backends` | method | `tests/test_llm_contract.py:102` | `def test_ai_model_exposes_all_backends(self)` |
| `test_api_key_slots` | method | `tests/test_llm_contract.py:144` | `def test_api_key_slots(self)` |
| `test_backend_constants_exposed` | method | `tests/test_llm_contract.py:69` | `def test_backend_constants_exposed(self)` |
| `test_default_models_match_constants` | method | `tests/test_llm_contract.py:125` | `def test_default_models_match_constants(self)` |
| `test_factory_exposes_public_api` | method | `tests/test_llm_contract.py:60` | `def test_factory_exposes_public_api(self)` |
| `test_factory_importable` | method | `tests/test_llm_contract.py:57` | `def test_factory_importable(self)` |
| `test_llm_client_class_methods_present` | method | `tests/test_llm_contract.py:92` | `def test_llm_client_class_methods_present(self)` |
| `test_llm_client_exposes_public_api` | method | `tests/test_llm_contract.py:87` | `def test_llm_client_exposes_public_api(self)` |
| `test_metadata_helpers_exposed` | method | `tests/test_llm_contract.py:115` | `def test_metadata_helpers_exposed(self)` |
| `test_model_config_keys_match_constants` | method | `tests/test_llm_contract.py:135` | `def test_model_config_keys_match_constants(self)` |
| `test_normalize_falls_back_to_auto_on_empty` | method | `tests/test_llm_contract.py:80` | `def test_normalize_falls_back_to_auto_on_empty(self)` |
| `test_normalize_rejects_unknown_backend` | method | `tests/test_llm_contract.py:75` | `def test_normalize_rejects_unknown_backend(self)` |
| `test_requires_api_key_only_for_cloud` | method | `tests/test_llm_contract.py:153` | `def test_requires_api_key_only_for_cloud(self)` |
| `test_supported_backends_are_canonical` | method | `tests/test_llm_contract.py:65` | `def test_supported_backends_are_canonical(self)` |
| `test_unified_llm_client_does_not_exist` | method | `tests/test_llm_contract.py:51` | `def test_unified_llm_client_does_not_exist(self)` |
| `test_unknown_backend_rejected` | method | `tests/test_llm_contract.py:159` | `def test_unknown_backend_rejected(self)` |
| `TestNoLegacyGroqImportInCore` | class | `tests/test_llm_legacy_isolation.py:61` | `class TestNoLegacyGroqImportInCore` |
| `_core_source_files` | function | `tests/test_llm_legacy_isolation.py:33` | `def _core_source_files()` |
| `_imported_targets` | function | `tests/test_llm_legacy_isolation.py:47` | `def _imported_targets(node)` |
| `test_no_core_file_imports_legacy_groq` | method | `tests/test_llm_legacy_isolation.py:62` | `def test_no_core_file_imports_legacy_groq(self)` |
| `TestAdapterWiring` | class | `tests/test_llm_orchestrator.py:479` | `class TestAdapterWiring` |
| `TestAiFallbackIntegration` | class | `tests/test_llm_orchestrator.py:903` | `class TestAiFallbackIntegration` |
| `TestBackendKind` | class | `tests/test_llm_orchestrator.py:461` | `class TestBackendKind` |
| `TestC2Wiring` | class | `tests/test_llm_orchestrator.py:656` | `class TestC2Wiring` |
| `TestChainOrder` | class | `tests/test_llm_orchestrator.py:82` | `class TestChainOrder` |
| `TestErrorDetection` | class | `tests/test_llm_orchestrator.py:677` | `class TestErrorDetection` |
| `TestFailover` | class | `tests/test_llm_orchestrator.py:133` | `class TestFailover` |
| `TestGroqEnvKey` | class | `tests/test_llm_orchestrator.py:864` | `class TestGroqEnvKey` |
| `TestHealth` | class | `tests/test_llm_orchestrator.py:334` | `class TestHealth` |
| `TestLedger` | class | `tests/test_llm_orchestrator.py:429` | `class TestLedger` |
| `TestPlaceholderKeys` | class | `tests/test_llm_orchestrator.py:799` | `class TestPlaceholderKeys` |
| `_RecordingRegistry` | class | `tests/test_llm_orchestrator.py:413` | `class _RecordingRegistry` |
| `_StubHealth` | class | `tests/test_llm_orchestrator.py:40` | `class _StubHealth` |
| `__init__` | method | `tests/test_llm_orchestrator.py:43` | `def __init__(self, parked)` |
| `__init__` | method | `tests/test_llm_orchestrator.py:416` | `def __init__(self, seen)` |
| `_execute` | function | `tests/test_llm_orchestrator.py:59` | `def _execute(model_spec, prompt, max_tokens)` |
| `_explode` | function | `tests/test_llm_orchestrator.py:126` | `def _explode()` |
| `_member` | function | `tests/test_llm_orchestrator.py:70` | `def _member(name, model, priority)` |
| `_scripted_executor` | function | `tests/test_llm_orchestrator.py:58` | `def _scripted_executor(script, calls)` |
| `_spy` | function | `tests/test_llm_orchestrator.py:764` | `def _spy(model_spec, prompt, max_tokens)` |
| `cfg` | method | `tests/test_llm_orchestrator.py:481` | `def cfg(self, tmp_path)` |
| `executor` | function | `tests/test_llm_orchestrator.py:263` | `def executor(model_spec, prompt, max_tokens)` |
| `executor` | function | `tests/test_llm_orchestrator.py:283` | `def executor(model_spec, prompt, max_tokens)` |
| `healthy` | method | `tests/test_llm_orchestrator.py:48` | `def healthy(self, name)` |
| `healthy` | method | `tests/test_llm_orchestrator.py:419` | `def healthy(self, name)` |
| `isolated_pool` | function | `tests/test_llm_orchestrator.py:75` | `def isolated_pool(tmp_path, monkeypatch)` |
| `lazyc2_source` | function | `tests/test_llm_orchestrator.py:974` | `def lazyc2_source()` |
| `patched` | method | `tests/test_llm_orchestrator.py:493` | `def patched(self, cfg, monkeypatch)` |
| `report_failure` | method | `tests/test_llm_orchestrator.py:51` | `def report_failure(self, name, error)` |
| `report_failure` | method | `tests/test_llm_orchestrator.py:422` | `def report_failure(self, name, error)` |
| `report_success` | method | `tests/test_llm_orchestrator.py:54` | `def report_success(self, name)` |
| `report_success` | method | `tests/test_llm_orchestrator.py:425` | `def report_success(self, name)` |
| `test_ai_fallback_call_routes_through_the_chain` | method | `tests/test_llm_orchestrator.py:667` | `def test_ai_fallback_call_routes_through_the_chain(self)` |
| `test_all_members_fail_returns_error_result_without_raising` | method | `tests/test_llm_orchestrator.py:181` | `def test_all_members_fail_returns_error_result_without_raising(self)` |
| `test_all_unhealthy_members_still_get_attempted` | method | `tests/test_llm_orchestrator.py:352` | `def test_all_unhealthy_members_still_get_attempted(self)` |
| `test_analyze_functions_route_through_the_orchestrator` | method | `tests/test_llm_orchestrator.py:657` | `def test_analyze_functions_route_through_the_orchestrator(self)` |
| `test_ask_general_keeps_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:645` | `def test_ask_general_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_ask_general_serves_from_the_chain_when_backend_missing` | method | `tests/test_llm_orchestrator.py:627` | `def test_ask_general_serves_from_the_chain_when_backend_missing(self, patched, monkeypatch)` |
| `test_backend_kind_parses_spec_prefix` | method | `tests/test_llm_orchestrator.py:473` | `def test_backend_kind_parses_spec_prefix(self, spec, kind)` |
| `test_blank_reply_is_a_failure` | method | `tests/test_llm_orchestrator.py:217` | `def test_blank_reply_is_a_failure(self)` |
| `test_chain_uses_orchestrator_pool_when_no_override` | method | `tests/test_llm_orchestrator.py:297` | `def test_chain_uses_orchestrator_pool_when_no_override(self, isolated_pool)` |
| `test_client_401_error_string_falls_back_to_the_chain` | method | `tests/test_llm_orchestrator.py:570` | `def test_client_401_error_string_falls_back_to_the_chain(self, patched, monkeypatch)` |
| `test_client_401_keeps_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:595` | `def test_client_401_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_client_error_falls_back_to_the_chain` | method | `tests/test_llm_orchestrator.py:522` | `def test_client_error_falls_back_to_the_chain(self, patched, monkeypatch)` |
| `test_client_success_stays_primary_without_chain_call` | method | `tests/test_llm_orchestrator.py:548` | `def test_client_success_stays_primary_without_chain_call(self, patched, monkeypatch)` |
| `test_dedupes_members_by_name` | method | `tests/test_llm_orchestrator.py:318` | `def test_dedupes_members_by_name(self)` |
| `test_default_health_comes_from_shared_registry` | method | `tests/test_llm_orchestrator.py:395` | `def test_default_health_comes_from_shared_registry(self, isolated_pool, monkeypatch)` |
| `test_empty_prompt_short_circuits` | method | `tests/test_llm_orchestrator.py:243` | `def test_empty_prompt_short_circuits(self)` |
| `test_error_banner_text_is_a_failure_not_content` | method | `tests/test_llm_orchestrator.py:198` | `def test_error_banner_text_is_a_failure_not_content(self)` |
| `test_error_replies_detected` | method | `tests/test_llm_orchestrator.py:690` | `def test_error_replies_detected(self, reply)` |
| `test_exhausted_chain_degrades_to_local_ollama` | method | `tests/test_llm_orchestrator.py:947` | `def test_exhausted_chain_degrades_to_local_ollama(self, monkeypatch)` |
| `test_explicit_api_key_published_to_environment` | method | `tests/test_llm_orchestrator.py:865` | `def test_explicit_api_key_published_to_environment(self, monkeypatch)` |
| `test_factory_rejects_placeholder_env_key` | method | `tests/test_llm_orchestrator.py:819` | `def test_factory_rejects_placeholder_env_key(self, monkeypatch)` |
| `test_factory_rejects_placeholder_payload_key` | method | `tests/test_llm_orchestrator.py:810` | `def test_factory_rejects_placeholder_payload_key(self)` |
| `test_failure_is_recorded_in_the_pool_ledger` | method | `tests/test_llm_orchestrator.py:445` | `def test_failure_is_recorded_in_the_pool_ledger(self, isolated_pool)` |
| `test_failure_reports_health` | method | `tests/test_llm_orchestrator.py:381` | `def test_failure_reports_health(self)` |
| `test_fallback_answer_is_memorized_clean` | method | `tests/test_llm_orchestrator.py:611` | `def test_fallback_answer_is_memorized_clean(self, patched, monkeypatch, tmp_path)` |
| `test_invalid_api_key_reply_is_a_failure` | method | `tests/test_llm_orchestrator.py:733` | `def test_invalid_api_key_reply_is_a_failure(self)` |
| `test_long_pentest_plan_is_served_not_failed_over` | method | `tests/test_llm_orchestrator.py:712` | `def test_long_pentest_plan_is_served_not_failed_over(self)` |
| `test_max_tokens_is_forwarded` | method | `tests/test_llm_orchestrator.py:278` | `def test_max_tokens_is_forwarded(self)` |
| `test_missing_client_returns_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:515` | `def test_missing_client_returns_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_missing_client_serves_from_the_chain` | method | `tests/test_llm_orchestrator.py:499` | `def test_missing_client_serves_from_the_chain(self, patched, monkeypatch)` |
| `test_orchestrator_module_exports_public_api` | function | `tests/test_llm_orchestrator.py:982` | `def test_orchestrator_module_exports_public_api()` |
| `test_orchestrator_success_after_failure_carries_notice` | method | `tests/test_llm_orchestrator.py:925` | `def test_orchestrator_success_after_failure_carries_notice(self, monkeypatch)` |
| `test_orchestrator_success_maps_to_ai_result` | method | `tests/test_llm_orchestrator.py:904` | `def test_orchestrator_success_maps_to_ai_result(self, monkeypatch)` |
| `test_pentest_prose_with_unauthorized_word_is_content` | method | `tests/test_llm_orchestrator.py:700` | `def test_pentest_prose_with_unauthorized_word_is_content(self)` |
| `test_phishing_prose_with_credit_word_is_content` | method | `tests/test_llm_orchestrator.py:706` | `def test_phishing_prose_with_credit_word_is_content(self)` |
| `test_placeholder_env_replaced_by_payload_key` | method | `tests/test_llm_orchestrator.py:827` | `def test_placeholder_env_replaced_by_payload_key(self, monkeypatch)` |
| `test_placeholder_env_survives_without_payload_key` | method | `tests/test_llm_orchestrator.py:845` | `def test_placeholder_env_survives_without_payload_key(self, monkeypatch)` |
| `test_placeholder_fragments_recognized` | method | `tests/test_llm_orchestrator.py:800` | `def test_placeholder_fragments_recognized(self)` |
| `test_placeholder_groq_leg_refused_even_with_payload_key` | method | `tests/test_llm_orchestrator.py:780` | `def test_placeholder_groq_leg_refused_even_with_payload_key(self, monkeypatch)` |
| `test_placeholder_groq_leg_refused_without_doomed_call` | method | `tests/test_llm_orchestrator.py:754` | `def test_placeholder_groq_leg_refused_without_doomed_call(self, monkeypatch)` |
| `test_placeholder_payload_key_not_published` | method | `tests/test_llm_orchestrator.py:884` | `def test_placeholder_payload_key_not_published(self, monkeypatch)` |
| `test_pool_chain_reads_lazy_orchestrator_store` | method | `tests/test_llm_orchestrator.py:100` | `def test_pool_chain_reads_lazy_orchestrator_store(self, isolated_pool)` |
| `test_pool_chain_returns_empty_when_pool_unreadable` | method | `tests/test_llm_orchestrator.py:121` | `def test_pool_chain_returns_empty_when_pool_unreadable(self, monkeypatch)` |
| `test_pool_chain_self_heals_corrupt_store` | method | `tests/test_llm_orchestrator.py:113` | `def test_pool_chain_self_heals_corrupt_store(self, isolated_pool)` |
| `test_primary_failure_serves_fallback_with_notice` | method | `tests/test_llm_orchestrator.py:155` | `def test_primary_failure_serves_fallback_with_notice(self)` |
| `test_primary_success_needs_no_fallback` | method | `tests/test_llm_orchestrator.py:134` | `def test_primary_success_needs_no_fallback(self)` |
| `test_quota_wording_reply_is_a_failure` | method | `tests/test_llm_orchestrator.py:230` | `def test_quota_wording_reply_is_a_failure(self)` |
| `test_real_answer_not_treated_as_error` | method | `tests/test_llm_orchestrator.py:695` | `def test_real_answer_not_treated_as_error(self)` |
| `test_real_key_not_a_placeholder` | method | `tests/test_llm_orchestrator.py:806` | `def test_real_key_not_a_placeholder(self)` |
| `test_sort_members_never_mutates_input` | method | `tests/test_llm_orchestrator.py:94` | `def test_sort_members_never_mutates_input(self)` |
| `test_success_is_recorded_in_the_pool_ledger` | method | `tests/test_llm_orchestrator.py:430` | `def test_success_is_recorded_in_the_pool_ledger(self, isolated_pool)` |
| `test_success_reports_health` | method | `tests/test_llm_orchestrator.py:367` | `def test_success_reports_health(self)` |
| `test_system_prompt_is_prepended_for_the_executor` | method | `tests/test_llm_orchestrator.py:258` | `def test_system_prompt_is_prepended_for_the_executor(self)` |
| `test_total_failure_returns_help_message` | method | `tests/test_llm_orchestrator.py:961` | `def test_total_failure_returns_help_message(self, monkeypatch)` |
| `test_unhealthy_member_is_skipped_while_others_remain` | method | `tests/test_llm_orchestrator.py:335` | `def test_unhealthy_member_is_skipped_while_others_remain(self)` |
| `test_weights_sort_members_by_descending_priority` | method | `tests/test_llm_orchestrator.py:83` | `def test_weights_sort_members_by_descending_priority(self)` |
| `TestConfig` | class | `tests/test_llm_prompts.py:83` | `class TestConfig` |
| `TestKnowledgeStore` | class | `tests/test_llm_prompts.py:53` | `class TestKnowledgeStore` |
| `TestRegistryIntegrity` | class | `tests/test_llm_prompts.py:157` | `class TestRegistryIntegrity` |
| `TestTemplates` | class | `tests/test_llm_prompts.py:129` | `class TestTemplates` |
| `TestTruncateMessage` | class | `tests/test_llm_prompts.py:39` | `class TestTruncateMessage` |
| `_config` | function | `tests/test_llm_prompts.py:29` | `def _config(tmp_path)` |
| `_write_json` | function | `tests/test_llm_prompts.py:23` | `def _write_json(path, payload)` |
| `test_add_and_load_roundtrip` | method | `tests/test_llm_prompts.py:63` | `def test_add_and_load_roundtrip(self, tmp_path)` |
| `test_all_templates_have_registered_kb_domain` | method | `tests/test_llm_prompts.py:164` | `def test_all_templates_have_registered_kb_domain(self)` |
| `test_boundary_length_kept` | method | `tests/test_llm_prompts.py:48` | `def test_boundary_length_kept(self)` |
| `test_event_tool_output_empty_when_no_match` | method | `tests/test_llm_prompts.py:116` | `def test_event_tool_output_empty_when_no_match(self, tmp_path)` |
| `test_event_tool_output_reads_file` | method | `tests/test_llm_prompts.py:121` | `def test_event_tool_output_reads_file(self, tmp_path)` |
| `test_from_defaults_points_under_module_parent` | method | `tests/test_llm_prompts.py:84` | `def test_from_defaults_points_under_module_parent(self, tmp_path, monkeypatch)` |
| `test_general_embeds_payload_rhost` | method | `tests/test_llm_prompts.py:144` | `def test_general_embeds_payload_rhost(self, tmp_path)` |
| `test_kb_domains_are_valid_file_names` | method | `tests/test_llm_prompts.py:158` | `def test_kb_domains_are_valid_file_names(self)` |
| `test_knowledge_base_path_resolves_names` | method | `tests/test_llm_prompts.py:90` | `def test_knowledge_base_path_resolves_names(self, tmp_path)` |
| `test_load_malformed_file_returns_empty` | method | `tests/test_llm_prompts.py:58` | `def test_load_malformed_file_returns_empty(self, tmp_path)` |
| `test_load_missing_file_returns_empty` | method | `tests/test_llm_prompts.py:54` | `def test_load_missing_file_returns_empty(self, tmp_path)` |
| `test_long_message_truncated_with_ellipsis` | method | `tests/test_llm_prompts.py:43` | `def test_long_message_truncated_with_ellipsis(self)` |
| `test_payload_context_defaults_to_empty` | method | `tests/test_llm_prompts.py:94` | `def test_payload_context_defaults_to_empty(self, tmp_path)` |
| `test_payload_context_reads_values` | method | `tests/test_llm_prompts.py:109` | `def test_payload_context_reads_values(self, tmp_path)` |
| `test_relevant_filters_on_keyword` | method | `tests/test_llm_prompts.py:69` | `def test_relevant_filters_on_keyword(self, tmp_path)` |
| `test_relevant_limits_results` | method | `tests/test_llm_prompts.py:76` | `def test_relevant_limits_results(self, tmp_path)` |
| `test_render_embeds_knowledge_tail` | method | `tests/test_llm_prompts.py:137` | `def test_render_embeds_knowledge_tail(self, tmp_path, name)` |
| `test_render_includes_operator_prompt` | method | `tests/test_llm_prompts.py:131` | `def test_render_includes_operator_prompt(self, tmp_path, name)` |
| `test_short_message_returned_unchanged` | method | `tests/test_llm_prompts.py:40` | `def test_short_message_returned_unchanged(self)` |
| `test_vuln_embeds_payload_rhost` | method | `tests/test_llm_prompts.py:150` | `def test_vuln_embeds_payload_rhost(self, tmp_path)` |
| `TestResilientRotatingFileHandler` | class | `tests/test_logging_config.py:21` | `class TestResilientRotatingFileHandler` |
| `_make_logger` | function | `tests/test_logging_config.py:13` | `def _make_logger(handler)` |
| `test_detaches_silently_when_file_unwritable` | method | `tests/test_logging_config.py:32` | `def test_detaches_silently_when_file_unwritable(self, tmp_path, capsys)` |
| `test_rotating_file_is_exposed` | method | `tests/test_logging_config.py:47` | `def test_rotating_file_is_exposed(self)` |
| `test_writes_normally_when_dir_writable` | method | `tests/test_logging_config.py:22` | `def test_writes_normally_when_dir_writable(self, tmp_path)` |
| `_Bus` | class | `tests/test_loop_ai_bridge.py:38` | `class _Bus` |
| `_Oracle` | class | `tests/test_loop_ai_bridge.py:63` | `class _Oracle` |
| `_complete` | function | `tests/test_loop_ai_bridge.py:120` | `def _complete(model, prompt, max_tokens)` |
| `_swan` | function | `tests/test_loop_ai_bridge.py:140` | `def _swan(prompt, task_type, phase, timeout)` |
| `assess` | method | `tests/test_loop_ai_bridge.py:64` | `def assess(self, tool, command, category)` |
| `bridge` | function | `tests/test_loop_ai_bridge.py:25` | `def bridge(monkeypatch)` |
| `publish` | method | `tests/test_loop_ai_bridge.py:39` | `def publish(self, event)` |
| `store` | function | `tests/test_loop_ai_bridge.py:15` | `def store(tmp_path, monkeypatch)` |
| `test_activity_log_publishes_to_bridge` | function | `tests/test_loop_ai_bridge.py:52` | `def test_activity_log_publishes_to_bridge(store, bridge, monkeypatch)` |
| `test_annotate_detection_uses_oracle` | function | `tests/test_loop_ai_bridge.py:62` | `def test_annotate_detection_uses_oracle(bridge, monkeypatch)` |
| `test_llm_pool_prefers_moe_expert_and_records_outcome` | function | `tests/test_loop_ai_bridge.py:108` | `def test_llm_pool_prefers_moe_expert_and_records_outcome(store, bridge, monkeypatch)` |
| `test_planner_uses_swan_when_available` | function | `tests/test_loop_ai_bridge.py:133` | `def test_planner_uses_swan_when_available(store, bridge, monkeypatch)` |
| `test_publish_loop_event_skips_stream_kinds` | function | `tests/test_loop_ai_bridge.py:34` | `def test_publish_loop_event_skips_stream_kinds(bridge, monkeypatch)` |
| `test_worker_annotates_detection_and_records_outcome` | function | `tests/test_loop_ai_bridge.py:74` | `def test_worker_annotates_detection_and_records_outcome(store, bridge, monkeypatch)` |
| `_Shell` | class | `tests/test_loop_auto_orchestrator.py:59` | `class _Shell` |
| `_Shell` | class | `tests/test_loop_auto_orchestrator.py:131` | `class _Shell` |
| `onecmd` | method | `tests/test_loop_auto_orchestrator.py:60` | `def onecmd(self, command)` |
| `onecmd_plus_hooks` | method | `tests/test_loop_auto_orchestrator.py:132` | `def onecmd_plus_hooks(self, command)` |
| `test_addon_hits_rank_specific_before_generic` | function | `tests/test_loop_auto_orchestrator.py:22` | `def test_addon_hits_rank_specific_before_generic()` |
| `test_autonomous_mode_suppresses_and_restores_input` | function | `tests/test_loop_auto_orchestrator.py:141` | `def test_autonomous_mode_suppresses_and_restores_input(monkeypatch)` |
| `test_execute_shell_verb_forwards_output` | function | `tests/test_loop_auto_orchestrator.py:127` | `def test_execute_shell_verb_forwards_output()` |
| `test_execute_streaming_streams_and_captures` | function | `tests/test_loop_auto_orchestrator.py:109` | `def test_execute_streaming_streams_and_captures()` |
| `test_execute_streaming_timeout_reports` | function | `tests/test_loop_auto_orchestrator.py:119` | `def test_execute_streaming_timeout_reports()` |
| `test_exfil_auto_registered_as_verb` | function | `tests/test_loop_auto_orchestrator.py:6` | `def test_exfil_auto_registered_as_verb()` |
| `test_lazy_addon_command_registered` | function | `tests/test_loop_auto_orchestrator.py:153` | `def test_lazy_addon_command_registered()` |
| `test_propose_addon_intents_shape_and_tool_collapse` | function | `tests/test_loop_auto_orchestrator.py:31` | `def test_propose_addon_intents_shape_and_tool_collapse()` |
| `test_service_tokens_split_and_alias` | function | `tests/test_loop_auto_orchestrator.py:15` | `def test_service_tokens_split_and_alias()` |
| `test_service_trigger_fires_with_addon_hits` | function | `tests/test_loop_auto_orchestrator.py:194` | `def test_service_trigger_fires_with_addon_hits(tmp_path, monkeypatch)` |
| `test_steps_for_lazy_addon_routes_to_command` | function | `tests/test_loop_auto_orchestrator.py:40` | `def test_steps_for_lazy_addon_routes_to_command()` |
| `test_worker_routes_verbs_via_bound_shell` | function | `tests/test_loop_auto_orchestrator.py:49` | `def test_worker_routes_verbs_via_bound_shell(tmp_path, monkeypatch)` |
| `test_worker_skips_missing_binary_and_records_gap` | function | `tests/test_loop_auto_orchestrator.py:163` | `def test_worker_skips_missing_binary_and_records_gap(tmp_path, monkeypatch)` |
| `test_worker_without_shell_reports_honestly` | function | `tests/test_loop_auto_orchestrator.py:85` | `def test_worker_without_shell_reports_honestly(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_broadcast.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_broadcast_rows_carry_neighbours_and_assets` | function | `tests/test_loop_broadcast.py:15` | `def test_broadcast_rows_carry_neighbours_and_assets(tmp_path, monkeypatch)` |
| `test_broadcast_search_id_and_kind_filter` | function | `tests/test_loop_broadcast.py:36` | `def test_broadcast_search_id_and_kind_filter(tmp_path, monkeypatch)` |
| `TestBudgetGate` | class | `tests/test_loop_budget.py:42` | `class TestBudgetGate` |
| `TestBudgetParsing` | class | `tests/test_loop_budget.py:10` | `class TestBudgetParsing` |
| `math_close` | function | `tests/test_loop_budget.py:38` | `def math_close(budget)` |
| `test_budget_confirm_toggle` | method | `tests/test_loop_budget.py:31` | `def test_budget_confirm_toggle(self)` |
| `test_budget_pairs_parsed` | method | `tests/test_loop_budget.py:13` | `def test_budget_pairs_parsed(self)` |
| `test_gate_blocks_when_declined` | method | `tests/test_loop_budget.py:45` | `def test_gate_blocks_when_declined(self, monkeypatch)` |
| `test_gate_pass_when_approved` | method | `tests/test_loop_budget.py:55` | `def test_gate_pass_when_approved(self, monkeypatch)` |
| `test_gate_skipped_autonomous` | method | `tests/test_loop_budget.py:65` | `def test_gate_skipped_autonomous(self, monkeypatch)` |
| `test_minimums_clamped` | method | `tests/test_loop_budget.py:19` | `def test_minimums_clamped(self)` |
| `test_unknown_key_rejected` | method | `tests/test_loop_budget.py:25` | `def test_unknown_key_rejected(self)` |
| `_broken` | function | `tests/test_loop_cli_catalog.py:90` | `def _broken()` |
| `_default` | function | `tests/test_loop_cli_catalog.py:47` | `def _default(cfg)` |
| `sandbox` | function | `tests/test_loop_cli_catalog.py:17` | `def sandbox(tmp_path, monkeypatch)` |
| `test_catalog_cli_for_phase_lists_enabled_only` | function | `tests/test_loop_cli_catalog.py:56` | `def test_catalog_cli_for_phase_lists_enabled_only(sandbox)` |
| `test_missing_catalog_view_adds_nothing` | function | `tests/test_loop_cli_catalog.py:79` | `def test_missing_catalog_view_adds_nothing(tmp_path, monkeypatch)` |
| `test_prompt_context_carries_allowed_commands` | function | `tests/test_loop_cli_catalog.py:66` | `def test_prompt_context_carries_allowed_commands(sandbox)` |
| `_old_facts` | function | `tests/test_loop_cold_overview.py:15` | `def _old_facts(graph, count, prefix)` |
| `_patched_engine` | function | `tests/test_loop_cold_overview.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_compact_debounce_keeps_fresh_hot` | function | `tests/test_loop_cold_overview.py:28` | `def test_compact_debounce_keeps_fresh_hot(tmp_path, monkeypatch)` |
| `test_compact_folds_stale_facts` | function | `tests/test_loop_cold_overview.py:41` | `def test_compact_folds_stale_facts(tmp_path, monkeypatch)` |
| `test_graph_overview_carries_findings_and_done_totals` | function | `tests/test_loop_cold_overview.py:77` | `def test_graph_overview_carries_findings_and_done_totals(tmp_path, monkeypatch)` |
| `test_planner_round_folds_minor_window` | function | `tests/test_loop_cold_overview.py:56` | `def test_planner_round_folds_minor_window(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_force_graph.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_graph_context_surfaces_hubs_and_next` | function | `tests/test_loop_force_graph.py:32` | `def test_graph_context_surfaces_hubs_and_next(tmp_path, monkeypatch)` |
| `test_loop_graph_is_forcegraph_ready` | function | `tests/test_loop_force_graph.py:15` | `def test_loop_graph_is_forcegraph_ready(tmp_path, monkeypatch)` |
| `test_planner_force_ranks_connected_surface` | function | `tests/test_loop_force_graph.py:53` | `def test_planner_force_ranks_connected_surface(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_guard_audit.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_audit_filters_action_source_query` | function | `tests/test_loop_guard_audit.py:31` | `def test_audit_filters_action_source_query(tmp_path, monkeypatch)` |
| `test_check_mints_tool_use_id` | function | `tests/test_loop_guard_audit.py:15` | `def test_check_mints_tool_use_id(tmp_path, monkeypatch)` |
| `test_lookup_jumps_to_execution` | function | `tests/test_loop_guard_audit.py:48` | `def test_lookup_jumps_to_execution(tmp_path, monkeypatch)` |
| `_work` | function | `tests/test_loop_guardrails.py:75` | `def _work()` |
| `_work` | function | `tests/test_loop_guardrails.py:99` | `def _work()` |
| `test_edr_pacer_calm_level_returns_command_unchanged` | function | `tests/test_loop_guardrails.py:59` | `def test_edr_pacer_calm_level_returns_command_unchanged()` |
| `test_edr_pacer_connection_reset_raises_and_decays` | function | `tests/test_loop_guardrails.py:47` | `def test_edr_pacer_connection_reset_raises_and_decays()` |
| `test_edr_pacer_slow_scan_raises_level` | function | `tests/test_loop_guardrails.py:35` | `def test_edr_pacer_slow_scan_raises_level()` |
| `test_fact_vector_store_roundtrip_and_search` | function | `tests/test_loop_guardrails.py:121` | `def test_fact_vector_store_roundtrip_and_search(tmp_path)` |
| `test_fact_vector_store_search_block_rendering` | function | `tests/test_loop_guardrails.py:141` | `def test_fact_vector_store_search_block_rendering(tmp_path)` |
| `test_repeat_detector_flags_identical_window` | function | `tests/test_loop_guardrails.py:12` | `def test_repeat_detector_flags_identical_window()` |
| `test_repeat_detector_recovery_on_variation` | function | `tests/test_loop_guardrails.py:21` | `def test_repeat_detector_recovery_on_variation()` |
| `test_target_limiter_caps_concurrency` | function | `tests/test_loop_guardrails.py:67` | `def test_target_limiter_caps_concurrency()` |
| `test_target_limiter_empty_target_bypasses` | function | `tests/test_loop_guardrails.py:112` | `def test_target_limiter_empty_target_bypasses()` |
| `test_target_limiter_is_reentrant_per_thread` | function | `tests/test_loop_guardrails.py:93` | `def test_target_limiter_is_reentrant_per_thread()` |
| `_patched_engine` | function | `tests/test_loop_intent_delete.py:8` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_hard_delete_removes_exclusive_keeps_shared` | function | `tests/test_loop_intent_delete.py:46` | `def test_hard_delete_removes_exclusive_keeps_shared(tmp_path, monkeypatch)` |
| `test_soft_delete_keeps_outputs_and_notifies` | function | `tests/test_loop_intent_delete.py:17` | `def test_soft_delete_keeps_outputs_and_notifies(tmp_path, monkeypatch)` |
| `test_soft_delete_requires_reason` | function | `tests/test_loop_intent_delete.py:37` | `def test_soft_delete_requires_reason(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_llm_resilience.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `error_then_ok` | function | `tests/test_loop_llm_resilience.py:61` | `def error_then_ok(model, prompt, max_tokens)` |
| `first_empty_then_ok` | function | `tests/test_loop_llm_resilience.py:42` | `def first_empty_then_ok(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:23` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:79` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:147` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:213` | `def scripted(model, prompt, max_tokens)` |
| `scripted_next` | function | `tests/test_loop_llm_resilience.py:160` | `def scripted_next(model, prompt, max_tokens)` |
| `test_empty_budget_exhausted_moves_to_next_member` | function | `tests/test_loop_llm_resilience.py:34` | `def test_empty_budget_exhausted_moves_to_next_member(tmp_path, monkeypatch)` |
| `test_empty_reply_replays_before_failover` | function | `tests/test_loop_llm_resilience.py:15` | `def test_empty_reply_replays_before_failover(tmp_path, monkeypatch)` |
| `test_error_reply_fails_over_instead_of_becoming_content` | function | `tests/test_loop_llm_resilience.py:54` | `def test_error_reply_fails_over_instead_of_becoming_content(tmp_path, monkeypatch)` |
| `test_llm_context_budget_roundtrip` | function | `tests/test_loop_llm_resilience.py:190` | `def test_llm_context_budget_roundtrip(tmp_path, monkeypatch)` |
| `test_planner_uses_bound_task_chain` | function | `tests/test_loop_llm_resilience.py:202` | `def test_planner_uses_bound_task_chain(tmp_path, monkeypatch)` |
| `test_raw_llm_recording_toggle` | function | `tests/test_loop_llm_resilience.py:169` | `def test_raw_llm_recording_toggle(tmp_path, monkeypatch)` |
| `test_stall_guard_forces_intent_when_nothing_open` | function | `tests/test_loop_llm_resilience.py:114` | `def test_stall_guard_forces_intent_when_nothing_open(tmp_path, monkeypatch)` |
| `test_task_llm_chain_quota_failover` | function | `tests/test_loop_llm_resilience.py:135` | `def test_task_llm_chain_quota_failover(tmp_path, monkeypatch)` |
| `test_wall_clock_settles_partial_not_hard_kill` | function | `tests/test_loop_llm_resilience.py:95` | `def test_wall_clock_settles_partial_not_hard_kill(tmp_path, monkeypatch)` |
| `test_worker_llm_steps_filtered_by_scope_and_tooling` | function | `tests/test_loop_llm_resilience.py:71` | `def test_worker_llm_steps_filtered_by_scope_and_tooling(tmp_path, monkeypatch)` |
| `TestClampInt` | class | `tests/test_loop_manager.py:123` | `class TestClampInt` |
| `TestLifecycle` | class | `tests/test_loop_manager.py:281` | `class TestLifecycle` |
| `TestLogReading` | class | `tests/test_loop_manager.py:222` | `class TestLogReading` |
| `TestSanitizeGoal` | class | `tests/test_loop_manager.py:95` | `class TestSanitizeGoal` |
| `TestSpawnAndRegistry` | class | `tests/test_loop_manager.py:151` | `class TestSpawnAndRegistry` |
| `TestStop` | class | `tests/test_loop_manager.py:251` | `class TestStop` |
| `TestValidateLoopId` | class | `tests/test_loop_manager.py:138` | `class TestValidateLoopId` |
| `TestValidateTarget` | class | `tests/test_loop_manager.py:64` | `class TestValidateTarget` |
| `loops_dir` | function | `tests/test_loop_manager.py:37` | `def loops_dir()` |
| `manager` | function | `tests/test_loop_manager.py:56` | `def manager(loops_dir, stub_script)` |
| `stub_script` | function | `tests/test_loop_manager.py:43` | `def stub_script(tmp_path)` |
| `test_accepts_hex32` | method | `tests/test_loop_manager.py:139` | `def test_accepts_hex32(self)` |
| `test_accepts_ipv4` | method | `tests/test_loop_manager.py:65` | `def test_accepts_ipv4(self)` |
| `test_accepts_ipv6` | method | `tests/test_loop_manager.py:68` | `def test_accepts_ipv6(self)` |
| `test_accepts_plain_words` | method | `tests/test_loop_manager.py:119` | `def test_accepts_plain_words(self)` |
| `test_argv_has_no_shell` | method | `tests/test_loop_manager.py:164` | `def test_argv_has_no_shell(self, manager)` |
| `test_clamps_high` | method | `tests/test_loop_manager.py:130` | `def test_clamps_high(self)` |
| `test_clamps_low` | method | `tests/test_loop_manager.py:127` | `def test_clamps_low(self)` |
| `test_collapses_whitespace` | method | `tests/test_loop_manager.py:100` | `def test_collapses_whitespace(self)` |
| `test_concurrency_cap` | method | `tests/test_loop_manager.py:187` | `def test_concurrency_cap(self, manager)` |
| `test_default_on_none` | method | `tests/test_loop_manager.py:124` | `def test_default_on_none(self)` |
| `test_defaults_on_empty` | method | `tests/test_loop_manager.py:96` | `def test_defaults_on_empty(self)` |
| `test_invalid_kind_rejected` | method | `tests/test_loop_manager.py:179` | `def test_invalid_kind_rejected(self, manager)` |
| `test_invalid_target_rejected` | method | `tests/test_loop_manager.py:183` | `def test_invalid_target_rejected(self, manager)` |
| `test_list_loops_sorted_newest_first` | method | `tests/test_loop_manager.py:195` | `def test_list_loops_sorted_newest_first(self, manager)` |
| `test_metadata_written` | method | `tests/test_loop_manager.py:212` | `def test_metadata_written(self, manager, loops_dir)` |
| `test_quick_exit_marks_finished` | method | `tests/test_loop_manager.py:282` | `def test_quick_exit_marks_finished(self, loops_dir, tmp_path)` |
| `test_read_log_chunk` | method | `tests/test_loop_manager.py:223` | `def test_read_log_chunk(self, manager, loops_dir)` |
| `test_read_log_confinement` | method | `tests/test_loop_manager.py:235` | `def test_read_log_confinement(self, manager, loops_dir)` |
| `test_read_log_offset_beyond_size` | method | `tests/test_loop_manager.py:243` | `def test_read_log_offset_beyond_size(self, manager)` |
| `test_read_log_unknown_loop` | method | `tests/test_loop_manager.py:231` | `def test_read_log_unknown_loop(self, manager)` |
| `test_registry_survives_restart` | method | `tests/test_loop_manager.py:205` | `def test_registry_survives_restart(self, manager, loops_dir)` |
| `test_rejects_command_injection` | method | `tests/test_loop_manager.py:78` | `def test_rejects_command_injection(self)` |
| `test_rejects_empty` | method | `tests/test_loop_manager.py:90` | `def test_rejects_empty(self)` |
| `test_rejects_hostname` | method | `tests/test_loop_manager.py:74` | `def test_rejects_hostname(self)` |
| `test_rejects_metacharacters` | method | `tests/test_loop_manager.py:82` | `def test_rejects_metacharacters(self)` |
| `test_rejects_newlines` | method | `tests/test_loop_manager.py:103` | `def test_rejects_newlines(self)` |
| `test_rejects_non_hex` | method | `tests/test_loop_manager.py:146` | `def test_rejects_non_hex(self)` |
| `test_rejects_non_numeric` | method | `tests/test_loop_manager.py:133` | `def test_rejects_non_numeric(self)` |
| `test_rejects_non_string` | method | `tests/test_loop_manager.py:86` | `def test_rejects_non_string(self)` |
| `test_rejects_quotes` | method | `tests/test_loop_manager.py:107` | `def test_rejects_quotes(self)` |
| `test_rejects_semicolons` | method | `tests/test_loop_manager.py:111` | `def test_rejects_semicolons(self)` |
| `test_rejects_too_long` | method | `tests/test_loop_manager.py:115` | `def test_rejects_too_long(self)` |
| `test_rejects_traversal` | method | `tests/test_loop_manager.py:142` | `def test_rejects_traversal(self)` |
| `test_sigterm_resistant_process_is_killed` | method | `tests/test_loop_manager.py:297` | `def test_sigterm_resistant_process_is_killed(self, loops_dir, tmp_path)` |
| `test_start_spawns_and_records` | method | `tests/test_loop_manager.py:152` | `def test_start_spawns_and_records(self, manager, loops_dir)` |
| `test_stop_finished_loop_rejected` | method | `tests/test_loop_manager.py:268` | `def test_stop_finished_loop_rejected(self, manager)` |
| `test_stop_terminates_process` | method | `tests/test_loop_manager.py:252` | `def test_stop_terminates_process(self, manager)` |
| `test_stop_unknown_loop` | method | `tests/test_loop_manager.py:264` | `def test_stop_unknown_loop(self, manager)` |
| `test_strips_whitespace` | method | `tests/test_loop_manager.py:71` | `def test_strips_whitespace(self)` |
| `test_summary_shape` | method | `tests/test_loop_manager.py:314` | `def test_summary_shape(self, manager)` |
| `test_mentions_parse_caps_and_trusts_ids` | function | `tests/test_loop_mentions.py:16` | `def test_mentions_parse_caps_and_trusts_ids()` |
| `test_mentions_search_and_cursor` | function | `tests/test_loop_mentions.py:6` | `def test_mentions_search_and_cursor(tmp_path, monkeypatch)` |
| `test_load_targets_file_caps_batch` | function | `tests/test_loop_multi_target.py:38` | `def test_load_targets_file_caps_batch(tmp_path)` |
| `test_load_targets_file_empty_raises` | function | `tests/test_loop_multi_target.py:52` | `def test_load_targets_file_empty_raises(tmp_path)` |
| `test_load_targets_file_missing_raises` | function | `tests/test_loop_multi_target.py:46` | `def test_load_targets_file_missing_raises(tmp_path)` |
| `test_load_targets_file_skips_comments_and_invalid` | function | `tests/test_loop_multi_target.py:27` | `def test_load_targets_file_skips_comments_and_invalid(tmp_path)` |
| `test_parse_loop_line_accepts_targets_file` | function | `tests/test_loop_multi_target.py:10` | `def test_parse_loop_line_accepts_targets_file(tmp_path)` |
| `test_parse_loop_line_defaults_without_file` | function | `tests/test_loop_multi_target.py:20` | `def test_parse_loop_line_defaults_without_file()` |
| `_sandbox` | function | `tests/test_loop_nmap_guard.py:8` | `def _sandbox(tmp_path, monkeypatch)` |
| `test_repair_appends_missing_target` | function | `tests/test_loop_nmap_guard.py:35` | `def test_repair_appends_missing_target()` |
| `test_repair_drops_port_flag_without_value` | function | `tests/test_loop_nmap_guard.py:41` | `def test_repair_drops_port_flag_without_value()` |
| `test_repair_keeps_valid_port_specs` | function | `tests/test_loop_nmap_guard.py:27` | `def test_repair_keeps_valid_port_specs()` |
| `test_repair_rejects_target_in_port_slot` | function | `tests/test_loop_nmap_guard.py:13` | `def test_repair_rejects_target_in_port_slot()` |
| `test_repair_strips_binary_path_for_shell_verb` | function | `tests/test_loop_nmap_guard.py:20` | `def test_repair_strips_binary_path_for_shell_verb()` |
| `test_scan_commands_are_not_replayed` | function | `tests/test_loop_nmap_guard.py:58` | `def test_scan_commands_are_not_replayed(tmp_path, monkeypatch)` |
| `test_stall_thresholds_follow_command_timeout` | function | `tests/test_loop_nmap_guard.py:48` | `def test_stall_thresholds_follow_command_timeout()` |
| `_overview` | function | `tests/test_loop_progress.py:20` | `def _overview()` |
| `test_chain_has_fourteen_stages` | function | `tests/test_loop_progress.py:28` | `def test_chain_has_fourteen_stages()` |
| `test_finished_task_all_green` | function | `tests/test_loop_progress.py:58` | `def test_finished_task_all_green()` |
| `test_fresh_task_shows_first_stage_current` | function | `tests/test_loop_progress.py:34` | `def test_fresh_task_shows_first_stage_current()` |
| `test_line_mode_prints_only_on_stage_change` | function | `tests/test_loop_progress.py:104` | `def test_line_mode_prints_only_on_stage_change(capsys)` |
| `test_panel_renders_without_live` | function | `tests/test_loop_progress.py:79` | `def test_panel_renders_without_live()` |
| `test_progress_advances_with_evidence` | function | `tests/test_loop_progress.py:44` | `def test_progress_advances_with_evidence()` |
| `test_render_contains_no_markup_strings` | function | `tests/test_loop_progress.py:88` | `def test_render_contains_no_markup_strings()` |
| `test_sanitize_line_keeps_ansi_when_asked` | function | `tests/test_loop_progress.py:134` | `def test_sanitize_line_keeps_ansi_when_asked()` |
| `test_sanitize_line_strips_ansi_and_cr` | function | `tests/test_loop_progress.py:126` | `def test_sanitize_line_strips_ansi_and_cr()` |
| `test_snapshot_counts_intent_states` | function | `tests/test_loop_progress.py:69` | `def test_snapshot_counts_intent_states()` |
| `_patched_engine` | function | `tests/test_loop_scope_traffic_evidence.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_finding_evidence_roles_notes_order` | function | `tests/test_loop_scope_traffic_evidence.py:88` | `def test_finding_evidence_roles_notes_order(tmp_path, monkeypatch)` |
| `test_scope_cidr_covers_url_embedded_ip` | function | `tests/test_loop_scope_traffic_evidence.py:29` | `def test_scope_cidr_covers_url_embedded_ip(tmp_path, monkeypatch)` |
| `test_scope_covers_by_ownership_not_substring` | function | `tests/test_loop_scope_traffic_evidence.py:15` | `def test_scope_covers_by_ownership_not_substring(tmp_path, monkeypatch)` |
| `test_scope_ip_covers_any_port_url` | function | `tests/test_loop_scope_traffic_evidence.py:41` | `def test_scope_ip_covers_any_port_url(tmp_path, monkeypatch)` |
| `test_traffic_search_host_port_aware` | function | `tests/test_loop_scope_traffic_evidence.py:71` | `def test_traffic_search_host_port_aware(tmp_path, monkeypatch)` |
| `test_worker_scope_enforcement_cidr` | function | `tests/test_loop_scope_traffic_evidence.py:54` | `def test_worker_scope_enforcement_cidr(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_spawn_side.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_chat_sessions_stay_independent` | function | `tests/test_loop_spawn_side.py:15` | `def test_chat_sessions_stay_independent(tmp_path, monkeypatch)` |
| `test_side_questions_persist_and_recall` | function | `tests/test_loop_spawn_side.py:36` | `def test_side_questions_persist_and_recall(tmp_path, monkeypatch)` |
| `test_spawn_inherits_scope_and_findings_read_only` | function | `tests/test_loop_spawn_side.py:53` | `def test_spawn_inherits_scope_and_findings_read_only(tmp_path, monkeypatch)` |
| `test_save_json_survives_parallel_writers` | function | `tests/test_loop_store_race.py:8` | `def test_save_json_survives_parallel_writers(tmp_path, monkeypatch)` |
| `writer` | function | `tests/test_loop_store_race.py:16` | `def writer(worker)` |
| `_DeadPool` | class | `tests/test_loop_supervision.py:25` | `class _DeadPool` |
| `_isolate_intel` | function | `tests/test_loop_supervision.py:16` | `def _isolate_intel(tmp_path, monkeypatch)` |
| `_kill_llm` | function | `tests/test_loop_supervision.py:37` | `def _kill_llm(monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_supervision.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `complete` | method | `tests/test_loop_supervision.py:32` | `def complete(self)` |
| `members` | method | `tests/test_loop_supervision.py:28` | `def members(self)` |
| `test_prompt_context_masks_configured_only` | function | `tests/test_loop_supervision.py:99` | `def test_prompt_context_masks_configured_only(tmp_path, monkeypatch)` |
| `test_repetition_watchdog_settles` | function | `tests/test_loop_supervision.py:46` | `def test_repetition_watchdog_settles(tmp_path, monkeypatch)` |
| `test_stack_priors_prefer_same_stack` | function | `tests/test_loop_supervision.py:75` | `def test_stack_priors_prefer_same_stack(tmp_path, monkeypatch)` |
| `_Assets` | class | `tests/test_loop_trigger_hints.py:42` | `class _Assets` |
| `_Graph` | class | `tests/test_loop_trigger_hints.py:29` | `class _Graph` |
| `__init__` | method | `tests/test_loop_trigger_hints.py:32` | `def __init__(self)` |
| `__init__` | method | `tests/test_loop_trigger_hints.py:45` | `def __init__(self, value)` |
| `add_node` | method | `tests/test_loop_trigger_hints.py:35` | `def add_node(self, kind, text, state, priority, meta)` |
| `fake_hot_matches` | function | `tests/test_loop_trigger_hints.py:65` | `def fake_hot_matches(services, allow_network)` |
| `fake_hot_matches` | function | `tests/test_loop_trigger_hints.py:100` | `def fake_hot_matches(services, allow_network)` |
| `list` | method | `tests/test_loop_trigger_hints.py:38` | `def list(self)` |
| `list` | method | `tests/test_loop_trigger_hints.py:49` | `def list(self, kind)` |
| `test_changed_banner_refires_the_hint` | function | `tests/test_loop_trigger_hints.py:90` | `def test_changed_banner_refires_the_hint(tmp_path, monkeypatch)` |
| `test_cve_hot_hint_proposed_once_per_signature` | function | `tests/test_loop_trigger_hints.py:78` | `def test_cve_hot_hint_proposed_once_per_signature(trigger_env)` |
| `test_hint_fingerprint_normalizes_product_and_version` | function | `tests/test_loop_trigger_hints.py:118` | `def test_hint_fingerprint_normalizes_product_and_version()` |
| `test_hint_store_written_under_loop_stores` | function | `tests/test_loop_trigger_hints.py:158` | `def test_hint_store_written_under_loop_stores(tmp_path, monkeypatch)` |
| `test_hint_ttl_expires_and_refires` | function | `tests/test_loop_trigger_hints.py:137` | `def test_hint_ttl_expires_and_refires(tmp_path, monkeypatch)` |
| `test_prune_drops_expired_fingerprints` | function | `tests/test_loop_trigger_hints.py:128` | `def test_prune_drops_expired_fingerprints()` |
| `trigger_env` | function | `tests/test_loop_trigger_hints.py:56` | `def trigger_env(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_worker_traces.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `_seed_two_works` | function | `tests/test_loop_worker_traces.py:15` | `def _seed_two_works(engine, task_id)` |
| `test_add_hint_emits_explicit_planner_trigger` | function | `tests/test_loop_worker_traces.py:65` | `def test_add_hint_emits_explicit_planner_trigger(tmp_path, monkeypatch)` |
| `test_planner_intent_unbound_emits_nothing` | function | `tests/test_loop_worker_traces.py:100` | `def test_planner_intent_unbound_emits_nothing(tmp_path, monkeypatch)` |
| `test_search_all_spans_works_without_intent` | function | `tests/test_loop_worker_traces.py:27` | `def test_search_all_spans_works_without_intent(tmp_path, monkeypatch)` |
| `test_trace_steps_and_single_step` | function | `tests/test_loop_worker_traces.py:40` | `def test_trace_steps_and_single_step(tmp_path, monkeypatch)` |
| `test_worker_bash_unbound_blocks_without_execution` | function | `tests/test_loop_worker_traces.py:81` | `def test_worker_bash_unbound_blocks_without_execution(tmp_path, monkeypatch)` |
| `test_worker_lane_binds_node_detail` | function | `tests/test_loop_worker_traces.py:57` | `def test_worker_lane_binds_node_detail(tmp_path, monkeypatch)` |
| `_drive` | function | `tests/test_marketplace_config.py:128` | `def _drive()` |
| `_drive` | function | `tests/test_marketplace_config.py:151` | `def _drive()` |
| `_registry` | function | `tests/test_marketplace_config.py:12` | `def _registry(tmp_path, monkeypatch)` |
| `test_create_and_delete_across_tabs` | function | `tests/test_marketplace_config.py:89` | `def test_create_and_delete_across_tabs(tmp_path, monkeypatch)` |
| `test_filter_input_keeps_printable_keys` | function | `tests/test_marketplace_config.py:145` | `def test_filter_input_keeps_printable_keys(tmp_path, monkeypatch)` |
| `test_marketplace_app_filters_rows` | function | `tests/test_marketplace_config.py:118` | `def test_marketplace_app_filters_rows(tmp_path, monkeypatch)` |
| `test_plugin_rows_skip_lua_and_templates` | function | `tests/test_marketplace_config.py:61` | `def test_plugin_rows_skip_lua_and_templates(tmp_path, monkeypatch)` |
| `test_read_only_tabs_never_toggle_or_delete` | function | `tests/test_marketplace_config.py:76` | `def test_read_only_tabs_never_toggle_or_delete(tmp_path, monkeypatch)` |
| `test_settings_toggle_tracks_only_success` | function | `tests/test_marketplace_config.py:105` | `def test_settings_toggle_tracks_only_success(tmp_path, monkeypatch)` |
| `test_tool_rows_use_json_and_active_key` | function | `tests/test_marketplace_config.py:33` | `def test_tool_rows_use_json_and_active_key(tmp_path, monkeypatch)` |
| `TestRegistryDispatch` | class | `tests/test_mcp_dispatch.py:51` | `class TestRegistryDispatch` |
| `_fallback_branches` | function | `tests/test_mcp_dispatch.py:40` | `def _fallback_branches()` |
| `_registered` | function | `tests/test_mcp_dispatch.py:23` | `def _registered()` |
| `test_mcp_never_offers_interactive_repl` | function | `tests/test_mcp_dispatch.py:107` | `def test_mcp_never_offers_interactive_repl()` |
| `test_migrated_handlers_absent_from_fallback` | method | `tests/test_mcp_dispatch.py:61` | `def test_migrated_handlers_absent_from_fallback(self)` |
| `test_migrated_handlers_registered` | method | `tests/test_mcp_dispatch.py:56` | `def test_migrated_handlers_registered(self)` |
| `test_new_chain_shell_tools_have_defs_and_handlers` | function | `tests/test_mcp_dispatch.py:82` | `def test_new_chain_shell_tools_have_defs_and_handlers()` |
| `test_no_dead_duplicate_branches` | method | `tests/test_mcp_dispatch.py:52` | `def test_no_dead_duplicate_branches(self)` |
| `test_opencode_bridge_curates_loop_and_chain` | function | `tests/test_mcp_dispatch.py:92` | `def test_opencode_bridge_curates_loop_and_chain()` |
| `test_set_config_refuses_null_values` | function | `tests/test_mcp_dispatch.py:67` | `def test_set_config_refuses_null_values()` |
| `_fresh_mcp_module` | function | `tests/test_mcp_improvements.py:397` | `def _fresh_mcp_module(tmp_path)` |
| `_seed_sessions` | function | `tests/test_mcp_improvements.py:182` | `def _seed_sessions(tmp_path)` |
| `runner` | function | `tests/test_mcp_improvements.py:300` | `def runner(cmd, timeout)` |
| `runner` | function | `tests/test_mcp_improvements.py:320` | `def runner(cmd, timeout)` |
| `test_audit_tasks_drops_timestamps_and_urls` | function | `tests/test_mcp_improvements.py:117` | `def test_audit_tasks_drops_timestamps_and_urls()` |
| `test_audit_tasks_respects_min_confidence` | function | `tests/test_mcp_improvements.py:141` | `def test_audit_tasks_respects_min_confidence()` |
| `test_build_target_context_filters_by_port` | function | `tests/test_mcp_improvements.py:195` | `def test_build_target_context_filters_by_port(tmp_path)` |
| `test_build_target_context_no_port_returns_all` | function | `tests/test_mcp_improvements.py:218` | `def test_build_target_context_no_port_returns_all(tmp_path)` |
| `test_confirmation_required_for_destructive_command` | function | `tests/test_mcp_improvements.py:380` | `def test_confirmation_required_for_destructive_command()` |
| `test_confirmation_required_for_destructive_tools` | function | `tests/test_mcp_improvements.py:389` | `def test_confirmation_required_for_destructive_tools()` |
| `test_confirmation_skipped_for_benign` | function | `tests/test_mcp_improvements.py:385` | `def test_confirmation_skipped_for_benign()` |
| `test_diff_first_run_reports_first_run` | function | `tests/test_mcp_improvements.py:353` | `def test_diff_first_run_reports_first_run(tmp_path)` |
| `test_diff_picks_up_changes` | function | `tests/test_mcp_improvements.py:360` | `def test_diff_picks_up_changes(tmp_path)` |
| `test_evidence_freshness_fresh` | function | `tests/test_mcp_improvements.py:160` | `def test_evidence_freshness_fresh(tmp_path)` |
| `test_evidence_freshness_missing` | function | `tests/test_mcp_improvements.py:154` | `def test_evidence_freshness_missing(tmp_path)` |
| `test_evidence_freshness_stale` | function | `tests/test_mcp_improvements.py:170` | `def test_evidence_freshness_stale(tmp_path)` |
| `test_evidence_grep_finds_in_loot_scope` | function | `tests/test_mcp_improvements.py:227` | `def test_evidence_grep_finds_in_loot_scope(tmp_path)` |
| `test_evidence_grep_handler_ignores_binaries` | function | `tests/test_mcp_improvements.py:436` | `def test_evidence_grep_handler_ignores_binaries(tmp_path)` |
| `test_evidence_grep_invalid_regex` | function | `tests/test_mcp_improvements.py:237` | `def test_evidence_grep_invalid_regex(tmp_path)` |
| `test_evidence_grep_truncates` | function | `tests/test_mcp_improvements.py:244` | `def test_evidence_grep_truncates(tmp_path)` |
| `test_handler_target_context_via_helper` | function | `tests/test_mcp_improvements.py:414` | `def test_handler_target_context_via_helper(tmp_path)` |
| `test_handler_tasks_cleanup_dry_run` | function | `tests/test_mcp_improvements.py:421` | `def test_handler_tasks_cleanup_dry_run(tmp_path)` |
| `test_is_likely_credential_classifies` | function | `tests/test_mcp_improvements.py:74` | `def test_is_likely_credential_classifies(value, expect_real, expect_reason)` |
| `test_is_likely_credential_handles_non_string` | function | `tests/test_mcp_improvements.py:84` | `def test_is_likely_credential_handles_non_string()` |
| `test_jobstore_captures_failure` | function | `tests/test_mcp_improvements.py:317` | `def test_jobstore_captures_failure()` |
| `test_jobstore_list_orders_newest_first` | function | `tests/test_mcp_improvements.py:340` | `def test_jobstore_list_orders_newest_first()` |
| `test_jobstore_runs_command_and_reports_done` | function | `tests/test_mcp_improvements.py:297` | `def test_jobstore_runs_command_and_reports_done()` |
| `test_jobstore_unknown_id` | function | `tests/test_mcp_improvements.py:335` | `def test_jobstore_unknown_id()` |
| `test_parse_task_value_complete` | function | `tests/test_mcp_improvements.py:92` | `def test_parse_task_value_complete()` |
| `test_parse_task_value_no_payload` | function | `tests/test_mcp_improvements.py:110` | `def test_parse_task_value_no_payload()` |
| `test_parse_task_value_truncated` | function | `tests/test_mcp_improvements.py:103` | `def test_parse_task_value_truncated()` |
| `test_preflight_detects_duplicate` | function | `tests/test_mcp_improvements.py:256` | `def test_preflight_detects_duplicate(tmp_path)` |
| `test_preflight_flags_missing_payload_keys` | function | `tests/test_mcp_improvements.py:270` | `def test_preflight_flags_missing_payload_keys(tmp_path)` |
| `test_preflight_os_mismatch` | function | `tests/test_mcp_improvements.py:281` | `def test_preflight_os_mismatch(tmp_path)` |
| `TestEnsureOptional` | class | `tests/test_mcp_lazy.py:42` | `class TestEnsureOptional` |
| `TestWrappersDelegate` | class | `tests/test_mcp_lazy.py:86` | `class TestWrappersDelegate` |
| `loader` | function | `tests/test_mcp_lazy.py:47` | `def loader(ns)` |
| `loader` | function | `tests/test_mcp_lazy.py:61` | `def loader(ns)` |
| `loader` | function | `tests/test_mcp_lazy.py:69` | `def loader(ns)` |
| `loader` | function | `tests/test_mcp_lazy.py:78` | `def loader(ns)` |
| `test_all_wrappers_delegate_to_helper` | method | `tests/test_mcp_lazy.py:87` | `def test_all_wrappers_delegate_to_helper(self)` |
| `test_cached_value_returned_untouched` | method | `tests/test_mcp_lazy.py:58` | `def test_cached_value_returned_untouched(self)` |
| `test_exception_fails_closed` | method | `tests/test_mcp_lazy.py:66` | `def test_exception_fails_closed(self)` |
| `test_false_loader_with_fallback` | method | `tests/test_mcp_lazy.py:75` | `def test_false_loader_with_fallback(self)` |
| `test_success_binds_and_caches` | method | `tests/test_mcp_lazy.py:43` | `def test_success_binds_and_caches(self)` |
| `_load_mcp_module` | function | `tests/test_mcp_recommender_embed.py:15` | `def _load_mcp_module()` |
| `explode` | function | `tests/test_mcp_recommender_embed.py:62` | `def explode()` |
| `fake_recommend` | function | `tests/test_mcp_recommender_embed.py:48` | `def fake_recommend()` |
| `test_limits_suggestions` | function | `tests/test_mcp_recommender_embed.py:81` | `def test_limits_suggestions(monkeypatch)` |
| `test_maps_recommender_fields` | function | `tests/test_mcp_recommender_embed.py:25` | `def test_maps_recommender_fields(monkeypatch)` |
| `test_never_forwards_positional_arguments` | function | `tests/test_mcp_recommender_embed.py:44` | `def test_never_forwards_positional_arguments(monkeypatch)` |
| `test_reports_unavailable_recommender` | function | `tests/test_mcp_recommender_embed.py:71` | `def test_reports_unavailable_recommender(monkeypatch)` |
| `test_returns_error_entry_on_failure` | function | `tests/test_mcp_recommender_embed.py:59` | `def test_returns_error_entry_on_failure(monkeypatch)` |
| `Empty` | class | `tests/test_mediation.py:158` | `class Empty` |
| `Fake` | class | `tests/test_mediation.py:123` | `class Fake` |
| `FakePort` | class | `tests/test_mediation.py:180` | `class FakePort` |
| `FakePort` | class | `tests/test_mediation.py:221` | `class FakePort` |
| `TestChainMediatorLlmPort` | class | `tests/test_mediation.py:111` | `class TestChainMediatorLlmPort` |
| `TestFeedbackMediator` | class | `tests/test_mediation.py:62` | `class TestFeedbackMediator` |
| `TestHubRouting` | class | `tests/test_mediation.py:19` | `class TestHubRouting` |
| `TestIntelMediatorActivityPort` | class | `tests/test_mediation.py:39` | `class TestIntelMediatorActivityPort` |
| `TestTelemetryMediator` | class | `tests/test_mediation.py:82` | `class TestTelemetryMediator` |
| `_FakeHub` | class | `tests/test_mediation.py:138` | `class _FakeHub` |
| `_NoLock` | class | `tests/test_mediation.py:145` | `class _NoLock` |
| `__enter__` | method | `tests/test_mediation.py:146` | `def __enter__(self)` |
| `__exit__` | method | `tests/test_mediation.py:149` | `def __exit__(self)` |
| `__init__` | method | `tests/test_mediation.py:139` | `def __init__(self, port)` |

Next: [SYMBOLS_p42.md](SYMBOLS_p42.md)
