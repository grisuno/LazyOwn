# Symbols (page 36 of 40)
Previous: [SYMBOLS_p35.md](SYMBOLS_p35.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `TestDirectPromptFlow` | class | `tests/test_llm_adapter_parity.py:94` | `class TestDirectPromptFlow` |
| `TestExports` | class | `tests/test_llm_adapter_parity.py:171` | `class TestExports` |
| `TestFileReadingVariants` | class | `tests/test_llm_adapter_parity.py:129` | `class TestFileReadingVariants` |
| `TestKnowledgePersistence` | class | `tests/test_llm_adapter_parity.py:113` | `class TestKnowledgePersistence` |
| `TestMissingClient` | class | `tests/test_llm_adapter_parity.py:65` | `class TestMissingClient` |
| `TestUninitializedClient` | class | `tests/test_llm_adapter_parity.py:88` | `class TestUninitializedClient` |
| `TestVulnAugmentation` | class | `tests/test_llm_adapter_parity.py:147` | `class TestVulnAugmentation` |
| `_FakeBackend` | class | `tests/test_llm_adapter_parity.py:191` | `class _FakeBackend` |
| `_FakeClient` | class | `tests/test_llm_adapter_parity.py:37` | `class _FakeClient` |
| `_FakeCompletions` | class | `tests/test_llm_adapter_parity.py:23` | `class _FakeCompletions` |
| `__init__` | method | `tests/test_llm_adapter_parity.py:24` | `def __init__(self, content)` |
| `__init__` | method | `tests/test_llm_adapter_parity.py:38` | `def __init__(self, content)` |
| `__init__` | method | `tests/test_llm_adapter_parity.py:192` | `def __init__(self, result)` |
| `_write` | function | `tests/test_llm_adapter_parity.py:60` | `def _write(path, text)` |
| `cfg` | function | `tests/test_llm_adapter_parity.py:44` | `def cfg(tmp_path)` |
| `complete` | method | `tests/test_llm_adapter_parity.py:197` | `def complete(self, system, user)` |
| `create` | method | `tests/test_llm_adapter_parity.py:30` | `def create(self, model, messages, max_tokens)` |
| `patched` | function | `tests/test_llm_adapter_parity.py:55` | `def patched(monkeypatch, cfg)` |
| `test_appends_event_tool_output` | method | `tests/test_llm_adapter_parity.py:148` | `def test_appends_event_tool_output(self, patched, cfg, tmp_path)` |
| `test_appends_plan_history` | method | `tests/test_llm_adapter_parity.py:161` | `def test_appends_plan_history(self, patched, cfg, tmp_path)` |
| `test_backend_error_string_not_remembered` | method | `tests/test_llm_adapter_parity.py:237` | `def test_backend_error_string_not_remembered(self, patched, cfg, monkeypatch)` |
| `test_backend_exception_reports_error` | method | `tests/test_llm_adapter_parity.py:230` | `def test_backend_exception_reports_error(self, patched, monkeypatch)` |
| `test_complete_error_handled` | method | `tests/test_llm_adapter_parity.py:89` | `def test_complete_error_handled(self, patched)` |
| `test_completion_received_single_user_message` | method | `tests/test_llm_adapter_parity.py:100` | `def test_completion_received_single_user_message(self, patched)` |
| `test_default_max_tokens_applied` | method | `tests/test_llm_adapter_parity.py:107` | `def test_default_max_tokens_applied(self, patched)` |
| `test_direct_variants_report_missing_key` | method | `tests/test_llm_adapter_parity.py:76` | `def test_direct_variants_report_missing_key(self, patched, name)` |
| `test_error_response_not_remembered` | method | `tests/test_llm_adapter_parity.py:122` | `def test_error_response_not_remembered(self, patched, cfg)` |
| `test_exported` | method | `tests/test_llm_adapter_parity.py:257` | `def test_exported(self)` |
| `test_file_variants_report_missing_key` | method | `tests/test_llm_adapter_parity.py:81` | `def test_file_variants_report_missing_key(self, patched, name, tmp_path)` |
| `test_groq_family_exports_present` | method | `tests/test_llm_adapter_parity.py:172` | `def test_groq_family_exports_present(self)` |
| `test_missing_backend_reports_error` | method | `tests/test_llm_adapter_parity.py:223` | `def test_missing_backend_reports_error(self, patched, monkeypatch)` |
| `test_receives_system_and_rendered_user` | method | `tests/test_llm_adapter_parity.py:213` | `def test_receives_system_and_rendered_user(self, patched, monkeypatch)` |
| `test_redop_reads_file_content` | method | `tests/test_llm_adapter_parity.py:141` | `def test_redop_reads_file_content(self, patched, tmp_path)` |
| `test_safe_groq_client_none_without_key` | method | `tests/test_llm_adapter_parity.py:186` | `def test_safe_groq_client_none_without_key(self)` |
| `test_sends_user_message_and_returns_content` | method | `tests/test_llm_adapter_parity.py:95` | `def test_sends_user_message_and_returns_content(self, patched)` |
| `test_successful_answer_remembered` | method | `tests/test_llm_adapter_parity.py:246` | `def test_successful_answer_remembered(self, patched, cfg, monkeypatch)` |
| `test_successful_response_is_remembered` | method | `tests/test_llm_adapter_parity.py:114` | `def test_successful_response_is_remembered(self, patched, cfg)` |
| `test_task_missing_file_returns_error` | method | `tests/test_llm_adapter_parity.py:137` | `def test_task_missing_file_returns_error(self, patched, tmp_path)` |
| `test_task_reads_file_content` | method | `tests/test_llm_adapter_parity.py:130` | `def test_task_reads_file_content(self, patched, tmp_path)` |
| `test_uses_configured_backend` | method | `tests/test_llm_adapter_parity.py:206` | `def test_uses_configured_backend(self, patched, monkeypatch)` |
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
| `test_mentions_parse_caps_and_trusts_ids` | function | `tests/test_loop_mentions.py:16` | `def test_mentions_parse_caps_and_trusts_ids()` |
| `test_mentions_search_and_cursor` | function | `tests/test_loop_mentions.py:6` | `def test_mentions_search_and_cursor(tmp_path, monkeypatch)` |
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
| `_patched_engine` | function | `tests/test_loop_worker_traces.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `_seed_two_works` | function | `tests/test_loop_worker_traces.py:15` | `def _seed_two_works(engine, task_id)` |
| `test_add_hint_emits_explicit_planner_trigger` | function | `tests/test_loop_worker_traces.py:65` | `def test_add_hint_emits_explicit_planner_trigger(tmp_path, monkeypatch)` |
| `test_planner_intent_unbound_emits_nothing` | function | `tests/test_loop_worker_traces.py:100` | `def test_planner_intent_unbound_emits_nothing(tmp_path, monkeypatch)` |
| `test_search_all_spans_works_without_intent` | function | `tests/test_loop_worker_traces.py:27` | `def test_search_all_spans_works_without_intent(tmp_path, monkeypatch)` |
| `test_trace_steps_and_single_step` | function | `tests/test_loop_worker_traces.py:40` | `def test_trace_steps_and_single_step(tmp_path, monkeypatch)` |
| `test_worker_bash_unbound_blocks_without_execution` | function | `tests/test_loop_worker_traces.py:81` | `def test_worker_bash_unbound_blocks_without_execution(tmp_path, monkeypatch)` |
| `test_worker_lane_binds_node_detail` | function | `tests/test_loop_worker_traces.py:57` | `def test_worker_lane_binds_node_detail(tmp_path, monkeypatch)` |
| `TestRegistryDispatch` | class | `tests/test_mcp_dispatch.py:51` | `class TestRegistryDispatch` |
| `_fallback_branches` | function | `tests/test_mcp_dispatch.py:40` | `def _fallback_branches()` |
| `_registered` | function | `tests/test_mcp_dispatch.py:23` | `def _registered()` |
| `test_migrated_handlers_absent_from_fallback` | method | `tests/test_mcp_dispatch.py:61` | `def test_migrated_handlers_absent_from_fallback(self)` |
| `test_migrated_handlers_registered` | method | `tests/test_mcp_dispatch.py:56` | `def test_migrated_handlers_registered(self)` |
| `test_no_dead_duplicate_branches` | method | `tests/test_mcp_dispatch.py:52` | `def test_no_dead_duplicate_branches(self)` |
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
| `_build_recorder` | function | `tests/test_metrics.py:35` | `def _build_recorder(tmp_path)` |
| `test_aggregator_handles_empty_iterable` | function | `tests/test_metrics.py:211` | `def test_aggregator_handles_empty_iterable()` |
| `test_aggregator_skips_malformed_records` | function | `tests/test_metrics.py:220` | `def test_aggregator_skips_malformed_records()` |
| `test_concurrent_writes_do_not_corrupt` | function | `tests/test_metrics.py:173` | `def test_concurrent_writes_do_not_corrupt(tmp_path)` |
| `test_get_recorder_is_singleton` | function | `tests/test_metrics.py:202` | `def test_get_recorder_is_singleton(tmp_path)` |
| `test_legacy_registry_inc_and_render` | function | `tests/test_metrics.py:42` | `def test_legacy_registry_inc_and_render()` |
| `test_metric_record_to_dict_roundtrip` | function | `tests/test_metrics.py:234` | `def test_metric_record_to_dict_roundtrip()` |
| `test_p95_uses_nearest_rank` | function | `tests/test_metrics.py:227` | `def test_p95_uses_nearest_rank()` |
| `test_recorder_appends_record_line` | function | `tests/test_metrics.py:57` | `def test_recorder_appends_record_line(tmp_path)` |
| `test_recorder_clamps_negative_duration` | function | `tests/test_metrics.py:83` | `def test_recorder_clamps_negative_duration(tmp_path)` |
| `test_summarize_aggregates_by_command` | function | `tests/test_metrics.py:92` | `def test_summarize_aggregates_by_command(tmp_path)` |
| `test_summarize_window_filters_old_records` | function | `tests/test_metrics.py:124` | `def test_summarize_window_filters_old_records(tmp_path)` |
| `test_tail_returns_newest_first` | function | `tests/test_metrics.py:163` | `def test_tail_returns_newest_first(tmp_path)` |
| `worker` | function | `tests/test_metrics.py:180` | `def worker(tag)` |
| `_BrokenSource` | class | `tests/test_metrics_aware_selector.py:217` | `class _BrokenSource` |
| `_StubMetrics` | class | `tests/test_metrics_aware_selector.py:54` | `class _StubMetrics` |
| `_StubSelector` | class | `tests/test_metrics_aware_selector.py:37` | `class _StubSelector(ICommandSelector)` |
| `__init__` | method | `tests/test_metrics_aware_selector.py:40` | `def __init__(self, decision)` |
| `__init__` | method | `tests/test_metrics_aware_selector.py:57` | `def __init__(self, by_command)` |
| `_decision` | function | `tests/test_metrics_aware_selector.py:71` | `def _decision(command)` |
| `fake_clock` | function | `tests/test_metrics_aware_selector.py:169` | `def fake_clock()` |
| `select` | method | `tests/test_metrics_aware_selector.py:44` | `def select(self, target, phase, context)` |
| `summarize` | method | `tests/test_metrics_aware_selector.py:62` | `def summarize(self, window_seconds)` |
| `summarize` | method | `tests/test_metrics_aware_selector.py:218` | `def summarize(self, window_seconds)` |
| `test_accepts_when_success_rate_at_threshold` | function | `tests/test_metrics_aware_selector.py:122` | `def test_accepts_when_success_rate_at_threshold()` |
| `test_chain_falls_through_to_fallback_when_all_filtered` | function | `tests/test_metrics_aware_selector.py:298` | `def test_chain_falls_through_to_fallback_when_all_filtered()` |
| `test_decorator_degrades_when_metrics_source_unavailable` | function | `tests/test_metrics_aware_selector.py:214` | `def test_decorator_degrades_when_metrics_source_unavailable()` |
| `test_filtering_emits_skip_event` | function | `tests/test_metrics_aware_selector.py:265` | `def test_filtering_emits_skip_event(tmp_path, monkeypatch)` |
| `test_filters_when_success_rate_below_threshold` | function | `tests/test_metrics_aware_selector.py:105` | `def test_filters_when_success_rate_below_threshold()` |
| `test_only_filters_named_command_not_whole_decision_object` | function | `tests/test_metrics_aware_selector.py:141` | `def test_only_filters_named_command_not_whole_decision_object()` |
| `test_passthrough_when_insufficient_attempts` | function | `tests/test_metrics_aware_selector.py:87` | `def test_passthrough_when_insufficient_attempts()` |
| `test_passthrough_when_wrapped_returns_none` | function | `tests/test_metrics_aware_selector.py:75` | `def test_passthrough_when_wrapped_returns_none()` |
| `test_summary_forwards_window_seconds` | function | `tests/test_metrics_aware_selector.py:188` | `def test_summary_forwards_window_seconds()` |
| `test_summary_is_cached_within_ttl` | function | `tests/test_metrics_aware_selector.py:158` | `def test_summary_is_cached_within_ttl()` |
| `test_wrap_chain_is_idempotent` | function | `tests/test_metrics_aware_selector.py:253` | `def test_wrap_chain_is_idempotent()` |
| `test_wrap_chain_leaves_fallback_unwrapped` | function | `tests/test_metrics_aware_selector.py:230` | `def test_wrap_chain_leaves_fallback_unwrapped()` |
| `test_wrap_chain_master_switch_off` | function | `tests/test_metrics_aware_selector.py:241` | `def test_wrap_chain_master_switch_off()` |
| `test_zero_window_is_treated_as_unbounded` | function | `tests/test_metrics_aware_selector.py:201` | `def test_zero_window_is_treated_as_unbounded()` |
| `_module_all` | function | `tests/test_migrate_lazyown_generator.py:27` | `def _module_all(source)` |
| `test_all_is_static_and_matches_class_name` | function | `tests/test_migrate_lazyown_generator.py:62` | `def test_all_is_static_and_matches_class_name()` |
| `test_compound_phase_title_casing` | function | `tests/test_migrate_lazyown_generator.py:68` | `def test_compound_phase_title_casing()` |
| `test_generated_module_parses` | function | `tests/test_migrate_lazyown_generator.py:57` | `def test_generated_module_parses()` |
| `test_method_bodies_are_embedded_in_order` | function | `tests/test_migrate_lazyown_generator.py:81` | `def test_method_bodies_are_embedded_in_order()` |
| `test_no_unevaluated_fstring_all_literal` | function | `tests/test_migrate_lazyown_generator.py:74` | `def test_no_unevaluated_fstring_all_literal()` |
| `TestClassify` | class | `tests/test_module_registry.py:20` | `class TestClassify` |
| `TestFormatFunctions` | class | `tests/test_module_registry.py:185` | `class TestFormatFunctions` |
| `TestModuleInfo` | class | `tests/test_module_registry.py:36` | `class TestModuleInfo` |
| `TestModuleRegistry` | class | `tests/test_module_registry.py:75` | `class TestModuleRegistry` |
| `test_by_type_shorthand` | method | `tests/test_module_registry.py:159` | `def test_by_type_shorthand(self)` |
| `test_empty_string` | method | `tests/test_module_registry.py:31` | `def test_empty_string(self)` |
| `test_format_module_detail` | method | `tests/test_module_registry.py:201` | `def test_format_module_detail(self)` |
| `test_format_module_detail_minimal` | method | `tests/test_module_registry.py:217` | `def test_format_module_detail_minimal(self)` |
| `test_format_module_table_empty` | method | `tests/test_module_registry.py:186` | `def test_format_module_table_empty(self)` |
| `test_format_module_table_with_data` | method | `tests/test_module_registry.py:190` | `def test_format_module_table_with_data(self)` |
| `test_full_construction` | method | `tests/test_module_registry.py:44` | `def test_full_construction(self)` |
| `test_get_known_module` | method | `tests/test_module_registry.py:133` | `def test_get_known_module(self)` |
| `test_get_unknown_returns_none` | method | `tests/test_module_registry.py:145` | `def test_get_unknown_returns_none(self)` |
| `test_initial_state_not_scanned` | method | `tests/test_module_registry.py:87` | `def test_initial_state_not_scanned(self)` |
| `test_known_categories` | method | `tests/test_module_registry.py:21` | `def test_known_categories(self)` |
| `test_minimal_construction` | method | `tests/test_module_registry.py:37` | `def test_minimal_construction(self)` |
| `test_repr` | method | `tests/test_module_registry.py:70` | `def test_repr(self)` |
| `test_rescan_forces_refresh` | method | `tests/test_module_registry.py:106` | `def test_rescan_forces_refresh(self)` |
| `test_scan_is_idempotent` | method | `tests/test_module_registry.py:99` | `def test_scan_is_idempotent(self)` |
| `test_scan_returns_list` | method | `tests/test_module_registry.py:92` | `def test_scan_returns_list(self)` |
| `test_search_by_category` | method | `tests/test_module_registry.py:127` | `def test_search_by_category(self)` |
| `test_search_by_module_type` | method | `tests/test_module_registry.py:121` | `def test_search_by_module_type(self)` |
| `test_search_enabled_only_filters_disabled` | method | `tests/test_module_registry.py:164` | `def test_search_enabled_only_filters_disabled(self)` |
| `test_search_returns_list` | method | `tests/test_module_registry.py:115` | `def test_search_returns_list(self)` |
| `test_singleton` | method | `tests/test_module_registry.py:76` | `def test_singleton(self)` |
| `test_singleton_with_base_dir` | method | `tests/test_module_registry.py:82` | `def test_singleton_with_base_dir(self)` |
| `test_summary_returns_counts` | method | `tests/test_module_registry.py:149` | `def test_summary_returns_counts(self)` |
| `test_to_dict` | method | `tests/test_module_registry.py:62` | `def test_to_dict(self)` |
| `test_unknown_category_defaults_to_auxiliary` | method | `tests/test_module_registry.py:27` | `def test_unknown_category_defaults_to_auxiliary(self)` |
| `TestAutonomousDaemonSWAN` | class | `tests/test_moe_rl_swan.py:493` | `class TestAutonomousDaemonSWAN` |
| `TestDetectionOracle` | class | `tests/test_moe_rl_swan.py:37` | `class TestDetectionOracle` |
| `TestMCPRegistration` | class | `tests/test_moe_rl_swan.py:675` | `class TestMCPRegistration` |
| `TestMoERouter` | class | `tests/test_moe_rl_swan.py:121` | `class TestMoERouter` |
| `TestPolicyDetectionAware` | class | `tests/test_moe_rl_swan.py:571` | `class TestPolicyDetectionAware` |
| `TestRLTrainer` | class | `tests/test_moe_rl_swan.py:223` | `class TestRLTrainer` |
| `TestSwanAgent` | class | `tests/test_moe_rl_swan.py:340` | `class TestSwanAgent` |
| `TestWorldModelGraph` | class | `tests/test_moe_rl_swan.py:616` | `class TestWorldModelGraph` |
| `_ep` | function | `tests/test_moe_rl_swan.py:199` | `def _ep(eid, w)` |
| `_make_trainer` | function | `tests/test_moe_rl_swan.py:285` | `def _make_trainer(suffix)` |
| `_result` | function | `tests/test_moe_rl_swan.py:421` | `def _result(task_type)` |
| `test_add_relation_and_pivot_candidates` | method | `tests/test_moe_rl_swan.py:617` | `def test_add_relation_and_pivot_candidates(self, tmp_path)` |
| `test_assessment_has_required_fields` | method | `tests/test_moe_rl_swan.py:62` | `def test_assessment_has_required_fields(self)` |
| `test_auto_relation_on_service_add` | method | `tests/test_moe_rl_swan.py:645` | `def test_auto_relation_on_service_add(self, tmp_path)` |
| `test_cascade_strategy_contains_swan_selector` | method | `tests/test_moe_rl_swan.py:511` | `def test_cascade_strategy_contains_swan_selector(self)` |
| `test_cascade_strategy_order` | method | `tests/test_moe_rl_swan.py:525` | `def test_cascade_strategy_order(self)` |
| `test_command_decision_source_label` | method | `tests/test_moe_rl_swan.py:548` | `def test_command_decision_source_label(self)` |
| `test_critical_risk_combined_credential_tools` | method | `tests/test_moe_rl_swan.py:54` | `def test_critical_risk_combined_credential_tools(self)` |
| `test_detection_above_threshold_zeroes_reward` | method | `tests/test_moe_rl_swan.py:572` | `def test_detection_above_threshold_zeroes_reward(self)` |
| `test_detection_penalty_lowers_effective_reward` | method | `tests/test_moe_rl_swan.py:281` | `def test_detection_penalty_lowers_effective_reward(self, tmp_path)` |
| `test_encode_state_format` | method | `tests/test_moe_rl_swan.py:224` | `def test_encode_state_format(self)` |
| `test_ensemble_result_dataclass_fields` | method | `tests/test_moe_rl_swan.py:460` | `def test_ensemble_result_dataclass_fields(self)` |
| `test_ensemble_returns_available_candidates` | method | `tests/test_moe_rl_swan.py:143` | `def test_ensemble_returns_available_candidates(self)` |
| `test_epsilon_decays_after_update` | method | `tests/test_moe_rl_swan.py:269` | `def test_epsilon_decays_after_update(self, tmp_path)` |
| `test_evil_winrm_is_high_risk` | method | `tests/test_moe_rl_swan.py:99` | `def test_evil_winrm_is_high_risk(self)` |
| `test_failed_outcome_gives_negative_reward` | method | `tests/test_moe_rl_swan.py:602` | `def test_failed_outcome_gives_negative_reward(self)` |
| `test_fallback_selector_never_returns_none` | method | `tests/test_moe_rl_swan.py:539` | `def test_fallback_selector_never_returns_none(self)` |
| `test_graph_snapshot_is_serialisable` | method | `tests/test_moe_rl_swan.py:634` | `def test_graph_snapshot_is_serialisable(self, tmp_path)` |
| `test_high_risk_mimikatz` | method | `tests/test_moe_rl_swan.py:46` | `def test_high_risk_mimikatz(self)` |
| `test_hive_tools_registered_in_mcp` | method | `tests/test_moe_rl_swan.py:685` | `def test_hive_tools_registered_in_mcp(self)` |
| `test_is_critical_risk_property` | method | `tests/test_moe_rl_swan.py:107` | `def test_is_critical_risk_property(self)` |
| `test_is_high_risk_property_consistent_with_probability` | method | `tests/test_moe_rl_swan.py:75` | `def test_is_high_risk_property_consistent_with_probability(self)` |
| `test_llm_selector_disabled_without_env` | method | `tests/test_moe_rl_swan.py:556` | `def test_llm_selector_disabled_without_env(self)` |
| `test_low_detection_preserves_positive_reward` | method | `tests/test_moe_rl_swan.py:587` | `def test_low_detection_preserves_positive_reward(self)` |
| `test_low_risk_dns_query` | method | `tests/test_moe_rl_swan.py:38` | `def test_low_risk_dns_query(self)` |
| `test_mcp_swan_route_returns_valid_json` | method | `tests/test_moe_rl_swan.py:438` | `def test_mcp_swan_route_returns_valid_json(self)` |
| `test_mcp_swan_status_returns_valid_json` | method | `tests/test_moe_rl_swan.py:452` | `def test_mcp_swan_status_returns_valid_json(self)` |
| `test_nmap_is_not_high_risk` | method | `tests/test_moe_rl_swan.py:91` | `def test_nmap_is_not_high_risk(self)` |
| `test_optimistic_init_for_unseen_actions` | method | `tests/test_moe_rl_swan.py:310` | `def test_optimistic_init_for_unseen_actions(self, tmp_path)` |
| `test_outcome_evaluator_failed_gives_negative_reward` | method | `tests/test_moe_rl_swan.py:399` | `def test_outcome_evaluator_failed_gives_negative_reward(self)` |
| `test_outcome_evaluator_high_value_category_bonus` | method | `tests/test_moe_rl_swan.py:417` | `def test_outcome_evaluator_high_value_category_bonus(self)` |
| `test_outcome_evaluator_success_reward` | method | `tests/test_moe_rl_swan.py:380` | `def test_outcome_evaluator_success_reward(self)` |
| `test_performance_bonus_penalises_high_detection` | method | `tests/test_moe_rl_swan.py:173` | `def test_performance_bonus_penalises_high_detection(self, tmp_path)` |
| `test_performance_bonus_positive_after_success` | method | `tests/test_moe_rl_swan.py:164` | `def test_performance_bonus_positive_after_success(self, tmp_path)` |
| `test_pivot_candidates_sorted_by_centrality` | method | `tests/test_moe_rl_swan.py:656` | `def test_pivot_candidates_sorted_by_centrality(self, tmp_path)` |
| `test_record_outcome_updates_ema` | method | `tests/test_moe_rl_swan.py:154` | `def test_record_outcome_updates_ema(self, tmp_path)` |
| `test_route_returns_expert_or_raises_gracefully` | method | `tests/test_moe_rl_swan.py:130` | `def test_route_returns_expert_or_raises_gracefully(self)` |
| `test_save_and_reload_persistence` | method | `tests/test_moe_rl_swan.py:318` | `def test_save_and_reload_persistence(self, tmp_path)` |
| `test_select_action_returns_valid_candidate` | method | `tests/test_moe_rl_swan.py:236` | `def test_select_action_returns_valid_candidate(self)` |
| `test_singleton_returns_same_instance` | method | `tests/test_moe_rl_swan.py:83` | `def test_singleton_returns_same_instance(self)` |
| `test_singleton_returns_same_instance` | method | `tests/test_moe_rl_swan.py:122` | `def test_singleton_returns_same_instance(self)` |
| `test_softmax_deterministic_picks_highest_weight` | method | `tests/test_moe_rl_swan.py:193` | `def test_softmax_deterministic_picks_highest_weight(self)` |
| `test_status_report_contains_experts` | method | `tests/test_moe_rl_swan.py:184` | `def test_status_report_contains_experts(self)` |
| `test_swan_result_dataclass_fields` | method | `tests/test_moe_rl_swan.py:341` | `def test_swan_result_dataclass_fields(self)` |
| `test_swan_result_failed_is_not_success` | method | `tests/test_moe_rl_swan.py:364` | `def test_swan_result_failed_is_not_success(self)` |
| `test_swan_selector_disabled_by_default` | method | `tests/test_moe_rl_swan.py:494` | `def test_swan_selector_disabled_by_default(self)` |
| `test_swan_selector_phase_mapping_coverage` | method | `tests/test_moe_rl_swan.py:503` | `def test_swan_selector_phase_mapping_coverage(self)` |
| `test_swan_tools_registered_in_mcp` | method | `tests/test_moe_rl_swan.py:676` | `def test_swan_tools_registered_in_mcp(self)` |
| `test_update_changes_qvalue` | method | `tests/test_moe_rl_swan.py:246` | `def test_update_changes_qvalue(self, tmp_path)` |
| `test_check_groq_reads_env_when_arg_empty` | function | `tests/test_moe_router_check_regression.py:65` | `def test_check_groq_reads_env_when_arg_empty(monkeypatch)` |
| `test_check_groq_returns_false_without_api_key` | function | `tests/test_moe_router_check_regression.py:27` | `def test_check_groq_returns_false_without_api_key(monkeypatch)` |
| `test_check_groq_returns_true_with_explicit_key` | function | `tests/test_moe_router_check_regression.py:47` | `def test_check_groq_returns_true_with_explicit_key()` |
| `test_check_toposwarm_returns_false_when_dir_absent` | function | `tests/test_moe_router_check_regression.py:110` | `def test_check_toposwarm_returns_false_when_dir_absent(tmp_path, monkeypatch)` |
| `test_check_toposwarm_uses_module_level_os_and_path` | function | `tests/test_moe_router_check_regression.py:85` | `def test_check_toposwarm_uses_module_level_os_and_path(tmp_path, monkeypatch)` |
| `test_check_unknown_backend_is_unavailable` | function | `tests/test_moe_router_check_regression.py:131` | `def test_check_unknown_backend_is_unavailable()` |
| `test_hmac_compare_digest_used` | function | `tests/test_mutation_verification.py:27` | `def test_hmac_compare_digest_used()` |
| `test_no_hardcoded_secrets` | function | `tests/test_mutation_verification.py:63` | `def test_no_hardcoded_secrets()` |
| `test_pickle_removed` | function | `tests/test_mutation_verification.py:56` | `def test_pickle_removed()` |
| `test_shell_false_in_safe_runner` | function | `tests/test_mutation_verification.py:41` | `def test_shell_false_in_safe_runner()` |
| `test_sql_injection_blocked` | function | `tests/test_mutation_verification.py:19` | `def test_sql_injection_blocked()` |
| `NethelpersSuiteConfig` | class | `tests/test_nethelpers_command_set.py:38` | `class NethelpersSuiteConfig` |
| `_add_repo_root_to_syspath` | function | `tests/test_nethelpers_command_set.py:32` | `def _add_repo_root_to_syspath()` |
| `_methods_of` | function | `tests/test_nethelpers_command_set.py:61` | `def _methods_of(path, class_name)` |
| `test_no_command_collisions_with_source` | function | `tests/test_nethelpers_command_set.py:108` | `def test_no_command_collisions_with_source()` |
| `test_registry_registers_target` | function | `tests/test_nethelpers_command_set.py:101` | `def test_registry_registers_target()` |
| `test_source_no_longer_defines_cluster` | function | `tests/test_nethelpers_command_set.py:95` | `def test_source_no_longer_defines_cluster()` |
| `test_target_exposes_full_nethelpers_cluster` | function | `tests/test_nethelpers_command_set.py:82` | `def test_target_exposes_full_nethelpers_cluster()` |
| `test_target_is_active_command_set` | function | `tests/test_nethelpers_command_set.py:73` | `def test_target_is_active_command_set()` |
| `test_target_phase_metadata` | function | `tests/test_nethelpers_command_set.py:89` | `def test_target_phase_metadata()` |
| `ScanConfig` | class | `tests/test_no_shell_execution.py:20` | `class ScanConfig` |
| `_parse` | function | `tests/test_no_shell_execution.py:64` | `def _parse(path)` |
| `find_os_system_calls` | function | `tests/test_no_shell_execution.py:72` | `def find_os_system_calls(config)` |
| `find_stdout_assignments` | function | `tests/test_no_shell_execution.py:96` | `def find_stdout_assignments(config)` |
| `iter_files` | method | `tests/test_no_shell_execution.py:44` | `def iter_files(self)` |
| `test_no_manual_stdout_reassignment` | function | `tests/test_no_shell_execution.py:130` | `def test_no_manual_stdout_reassignment()` |
| `test_no_os_system_in_production` | function | `tests/test_no_shell_execution.py:124` | `def test_no_os_system_in_production()` |
| `test_scanner_detects_a_synthetic_os_system` | function | `tests/test_no_shell_execution.py:136` | `def test_scanner_detects_a_synthetic_os_system(tmp_path)` |
| `TestMitreTactics` | class | `tests/test_nuclei_parser.py:128` | `class TestMitreTactics` |
| `TestNucleiFinding` | class | `tests/test_nuclei_parser.py:13` | `class TestNucleiFinding` |
| `TestNucleiParserJson` | class | `tests/test_nuclei_parser.py:73` | `class TestNucleiParserJson` |
| `TestNucleiParserText` | class | `tests/test_nuclei_parser.py:58` | `class TestNucleiParserText` |
| `TestRecommendations` | class | `tests/test_nuclei_parser.py:134` | `class TestRecommendations` |
| `TestSeverityMap` | class | `tests/test_nuclei_parser.py:120` | `class TestSeverityMap` |
| `test_all_tactics_have_ta_prefix` | method | `tests/test_nuclei_parser.py:129` | `def test_all_tactics_have_ta_prefix(self)` |
| `test_critical_is_10` | method | `tests/test_nuclei_parser.py:121` | `def test_critical_is_10(self)` |
| `test_exploit_probability_map` | method | `tests/test_nuclei_parser.py:28` | `def test_exploit_probability_map(self)` |
| `test_fields` | method | `tests/test_nuclei_parser.py:14` | `def test_fields(self)` |
| `test_generate_for_critical` | method | `tests/test_nuclei_parser.py:135` | `def test_generate_for_critical(self)` |
| `test_info_is_1` | method | `tests/test_nuclei_parser.py:124` | `def test_info_is_1(self)` |
| `test_mitre_tactic` | method | `tests/test_nuclei_parser.py:46` | `def test_mitre_tactic(self)` |
| `test_parse_empty` | method | `tests/test_nuclei_parser.py:59` | `def test_parse_empty(self)` |
| `test_parse_empty` | method | `tests/test_nuclei_parser.py:74` | `def test_parse_empty(self)` |
| `test_parse_json_array` | method | `tests/test_nuclei_parser.py:99` | `def test_parse_json_array(self)` |
| `test_parse_json_multiple_findings` | method | `tests/test_nuclei_parser.py:90` | `def test_parse_json_multiple_findings(self)` |
| `test_parse_json_single_finding` | method | `tests/test_nuclei_parser.py:78` | `def test_parse_json_single_finding(self)` |
| `test_parse_nuclei_line` | method | `tests/test_nuclei_parser.py:64` | `def test_parse_nuclei_line(self)` |
| `test_parse_with_cve_classification` | method | `tests/test_nuclei_parser.py:108` | `def test_parse_with_cve_classification(self)` |
| `test_skip_low_severity` | method | `tests/test_nuclei_parser.py:151` | `def test_skip_low_severity(self)` |
| `_seed_loot` | function | `tests/test_ops_loot_phase.py:34` | `def _seed_loot(sessions_dir)` |
| `_write_world` | function | `tests/test_ops_loot_phase.py:46` | `def _write_world(sessions_dir, world)` |
| `test_gather_loot_parses_kinds_and_skips_noise` | function | `tests/test_ops_loot_phase.py:53` | `def test_gather_loot_parses_kinds_and_skips_noise(tmp_path)` |
| `test_link_credential_to_failure_edge_and_roundtrip` | function | `tests/test_ops_loot_phase.py:310` | `def test_link_credential_to_failure_edge_and_roundtrip(tmp_path)` |
| `test_loot_entry_value` | function | `tests/test_ops_loot_phase.py:65` | `def test_loot_entry_value()` |
| `test_loot_graph_empty` | function | `tests/test_ops_loot_phase.py:196` | `def test_loot_graph_empty(tmp_path, capsys)` |
| `test_loot_graph_renders_edges` | function | `tests/test_ops_loot_phase.py:174` | `def test_loot_graph_renders_edges(tmp_path, capsys)` |
| `test_loot_mark_rejects_bad_outcome` | function | `tests/test_ops_loot_phase.py:222` | `def test_loot_mark_rejects_bad_outcome(tmp_path, capsys)` |
| `test_loot_mark_unknown_credential` | function | `tests/test_ops_loot_phase.py:230` | `def test_loot_mark_unknown_credential(tmp_path, capsys)` |
| `test_loot_mark_writes_rejected_edge` | function | `tests/test_ops_loot_phase.py:206` | `def test_loot_mark_writes_rejected_edge(tmp_path)` |
| `test_loot_reuse_excludes_rejected_and_flags_confirmed` | function | `tests/test_ops_loot_phase.py:148` | `def test_loot_reuse_excludes_rejected_and_flags_confirmed(tmp_path, capsys)` |
| `test_loot_reuse_no_loot` | function | `tests/test_ops_loot_phase.py:141` | `def test_loot_reuse_no_loot(tmp_path, capsys)` |
| `test_loot_reuse_no_target` | function | `tests/test_ops_loot_phase.py:133` | `def test_loot_reuse_no_target(tmp_path, capsys)` |

Next: [SYMBOLS_p37.md](SYMBOLS_p37.md)
