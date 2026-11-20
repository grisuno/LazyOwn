# Symbols (page 47 of 54)
Previous: [SYMBOLS_p46.md](SYMBOLS_p46.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_exhausted_key_is_skipped_during_cooldown` | function | `tests/test_llm_key_pool.py:35` | `def test_exhausted_key_is_skipped_during_cooldown()` |
| `test_note_quota_error_parks_global_key` | function | `tests/test_llm_key_pool.py:91` | `def test_note_quota_error_parks_global_key()` |
| `test_placeholders_and_duplicates_are_dropped` | function | `tests/test_llm_key_pool.py:27` | `def test_placeholders_and_duplicates_are_dropped()` |
| `test_resolve_pooled_key_is_noop_without_a_pool` | function | `tests/test_llm_key_pool.py:76` | `def test_resolve_pooled_key_is_noop_without_a_pool()` |
| `test_resolve_pooled_key_rotates_with_a_pool` | function | `tests/test_llm_key_pool.py:82` | `def test_resolve_pooled_key_rotates_with_a_pool()` |
| `test_round_robin_cycles_keys_in_order` | function | `tests/test_llm_key_pool.py:19` | `def test_round_robin_cycles_keys_in_order()` |
| `TestNoLegacyGroqImportInCore` | class | `tests/test_llm_legacy_isolation.py:61` | `class TestNoLegacyGroqImportInCore` |
| `_core_source_files` | function | `tests/test_llm_legacy_isolation.py:33` | `def _core_source_files()` |
| `_imported_targets` | function | `tests/test_llm_legacy_isolation.py:47` | `def _imported_targets(node)` |
| `test_no_core_file_imports_legacy_groq` | method | `tests/test_llm_legacy_isolation.py:62` | `def test_no_core_file_imports_legacy_groq(self)` |
| `TestAdapterWiring` | class | `tests/test_llm_orchestrator.py:498` | `class TestAdapterWiring` |
| `TestAiFallbackIntegration` | class | `tests/test_llm_orchestrator.py:925` | `class TestAiFallbackIntegration` |
| `TestBackendKind` | class | `tests/test_llm_orchestrator.py:480` | `class TestBackendKind` |
| `TestC2Wiring` | class | `tests/test_llm_orchestrator.py:679` | `class TestC2Wiring` |
| `TestChainOrder` | class | `tests/test_llm_orchestrator.py:101` | `class TestChainOrder` |
| `TestErrorDetection` | class | `tests/test_llm_orchestrator.py:700` | `class TestErrorDetection` |
| `TestFailover` | class | `tests/test_llm_orchestrator.py:152` | `class TestFailover` |
| `TestGroqEnvKey` | class | `tests/test_llm_orchestrator.py:886` | `class TestGroqEnvKey` |
| `TestHealth` | class | `tests/test_llm_orchestrator.py:353` | `class TestHealth` |
| `TestLedger` | class | `tests/test_llm_orchestrator.py:448` | `class TestLedger` |
| `TestPlaceholderKeys` | class | `tests/test_llm_orchestrator.py:821` | `class TestPlaceholderKeys` |
| `_RecordingRegistry` | class | `tests/test_llm_orchestrator.py:432` | `class _RecordingRegistry` |
| `_StubHealth` | class | `tests/test_llm_orchestrator.py:59` | `class _StubHealth` |
| `__init__` | method | `tests/test_llm_orchestrator.py:62` | `def __init__(self, parked)` |
| `__init__` | method | `tests/test_llm_orchestrator.py:435` | `def __init__(self, seen)` |
| `_execute` | function | `tests/test_llm_orchestrator.py:78` | `def _execute(model_spec, prompt, max_tokens)` |
| `_explode` | function | `tests/test_llm_orchestrator.py:145` | `def _explode()` |
| `_member` | function | `tests/test_llm_orchestrator.py:89` | `def _member(name, model, priority)` |
| `_restore_groq_env` | function | `tests/test_llm_orchestrator.py:41` | `def _restore_groq_env()` |
| `_scripted_executor` | function | `tests/test_llm_orchestrator.py:77` | `def _scripted_executor(script, calls)` |
| `_spy` | function | `tests/test_llm_orchestrator.py:786` | `def _spy(model_spec, prompt, max_tokens)` |
| `cfg` | method | `tests/test_llm_orchestrator.py:500` | `def cfg(self, tmp_path)` |
| `executor` | function | `tests/test_llm_orchestrator.py:282` | `def executor(model_spec, prompt, max_tokens)` |
| `executor` | function | `tests/test_llm_orchestrator.py:302` | `def executor(model_spec, prompt, max_tokens)` |
| `healthy` | method | `tests/test_llm_orchestrator.py:67` | `def healthy(self, name)` |
| `healthy` | method | `tests/test_llm_orchestrator.py:438` | `def healthy(self, name)` |
| `isolated_pool` | function | `tests/test_llm_orchestrator.py:94` | `def isolated_pool(tmp_path, monkeypatch)` |
| `lazyc2_source` | function | `tests/test_llm_orchestrator.py:996` | `def lazyc2_source()` |
| `patched` | method | `tests/test_llm_orchestrator.py:512` | `def patched(self, cfg, monkeypatch)` |
| `report_failure` | method | `tests/test_llm_orchestrator.py:70` | `def report_failure(self, name, error)` |
| `report_failure` | method | `tests/test_llm_orchestrator.py:441` | `def report_failure(self, name, error)` |
| `report_success` | method | `tests/test_llm_orchestrator.py:73` | `def report_success(self, name)` |
| `report_success` | method | `tests/test_llm_orchestrator.py:444` | `def report_success(self, name)` |
| `test_ai_fallback_call_routes_through_the_chain` | method | `tests/test_llm_orchestrator.py:690` | `def test_ai_fallback_call_routes_through_the_chain(self)` |
| `test_all_members_fail_returns_error_result_without_raising` | method | `tests/test_llm_orchestrator.py:200` | `def test_all_members_fail_returns_error_result_without_raising(self)` |
| `test_all_unhealthy_members_still_get_attempted` | method | `tests/test_llm_orchestrator.py:371` | `def test_all_unhealthy_members_still_get_attempted(self)` |
| `test_analyze_functions_route_through_the_orchestrator` | method | `tests/test_llm_orchestrator.py:680` | `def test_analyze_functions_route_through_the_orchestrator(self)` |
| `test_ask_general_keeps_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:668` | `def test_ask_general_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_ask_general_serves_from_the_chain_when_backend_missing` | method | `tests/test_llm_orchestrator.py:650` | `def test_ask_general_serves_from_the_chain_when_backend_missing(self, patched, monkeypatch)` |
| `test_backend_kind_parses_spec_prefix` | method | `tests/test_llm_orchestrator.py:492` | `def test_backend_kind_parses_spec_prefix(self, spec, kind)` |
| `test_blank_reply_is_a_failure` | method | `tests/test_llm_orchestrator.py:236` | `def test_blank_reply_is_a_failure(self)` |
| `test_chain_uses_orchestrator_pool_when_no_override` | method | `tests/test_llm_orchestrator.py:316` | `def test_chain_uses_orchestrator_pool_when_no_override(self, isolated_pool)` |
| `test_client_401_error_string_falls_back_to_the_chain` | method | `tests/test_llm_orchestrator.py:589` | `def test_client_401_error_string_falls_back_to_the_chain(self, patched, monkeypatch)` |
| `test_client_401_keeps_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:616` | `def test_client_401_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_client_error_falls_back_to_the_chain` | method | `tests/test_llm_orchestrator.py:541` | `def test_client_error_falls_back_to_the_chain(self, patched, monkeypatch)` |
| `test_client_success_stays_primary_without_chain_call` | method | `tests/test_llm_orchestrator.py:567` | `def test_client_success_stays_primary_without_chain_call(self, patched, monkeypatch)` |
| `test_dedupes_members_by_name` | method | `tests/test_llm_orchestrator.py:337` | `def test_dedupes_members_by_name(self)` |
| `test_default_health_comes_from_shared_registry` | method | `tests/test_llm_orchestrator.py:414` | `def test_default_health_comes_from_shared_registry(self, isolated_pool, monkeypatch)` |
| `test_empty_prompt_short_circuits` | method | `tests/test_llm_orchestrator.py:262` | `def test_empty_prompt_short_circuits(self)` |
| `test_error_banner_text_is_a_failure_not_content` | method | `tests/test_llm_orchestrator.py:217` | `def test_error_banner_text_is_a_failure_not_content(self)` |
| `test_error_replies_detected` | method | `tests/test_llm_orchestrator.py:713` | `def test_error_replies_detected(self, reply)` |
| `test_exhausted_chain_degrades_to_local_ollama` | method | `tests/test_llm_orchestrator.py:969` | `def test_exhausted_chain_degrades_to_local_ollama(self, monkeypatch)` |
| `test_explicit_api_key_published_to_environment` | method | `tests/test_llm_orchestrator.py:887` | `def test_explicit_api_key_published_to_environment(self, monkeypatch)` |
| `test_factory_rejects_placeholder_env_key` | method | `tests/test_llm_orchestrator.py:841` | `def test_factory_rejects_placeholder_env_key(self, monkeypatch)` |
| `test_factory_rejects_placeholder_payload_key` | method | `tests/test_llm_orchestrator.py:832` | `def test_factory_rejects_placeholder_payload_key(self)` |
| `test_failure_is_recorded_in_the_pool_ledger` | method | `tests/test_llm_orchestrator.py:464` | `def test_failure_is_recorded_in_the_pool_ledger(self, isolated_pool)` |
| `test_failure_reports_health` | method | `tests/test_llm_orchestrator.py:400` | `def test_failure_reports_health(self)` |
| `test_fallback_answer_is_memorized_clean` | method | `tests/test_llm_orchestrator.py:634` | `def test_fallback_answer_is_memorized_clean(self, patched, monkeypatch, tmp_path)` |
| `test_invalid_api_key_reply_is_a_failure` | method | `tests/test_llm_orchestrator.py:756` | `def test_invalid_api_key_reply_is_a_failure(self)` |
| `test_long_pentest_plan_is_served_not_failed_over` | method | `tests/test_llm_orchestrator.py:735` | `def test_long_pentest_plan_is_served_not_failed_over(self)` |
| `test_max_tokens_is_forwarded` | method | `tests/test_llm_orchestrator.py:297` | `def test_max_tokens_is_forwarded(self)` |
| `test_missing_client_returns_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:534` | `def test_missing_client_returns_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_missing_client_serves_from_the_chain` | method | `tests/test_llm_orchestrator.py:518` | `def test_missing_client_serves_from_the_chain(self, patched, monkeypatch)` |
| `test_orchestrator_module_exports_public_api` | function | `tests/test_llm_orchestrator.py:1004` | `def test_orchestrator_module_exports_public_api()` |
| `test_orchestrator_success_after_failure_carries_notice` | method | `tests/test_llm_orchestrator.py:947` | `def test_orchestrator_success_after_failure_carries_notice(self, monkeypatch)` |
| `test_orchestrator_success_maps_to_ai_result` | method | `tests/test_llm_orchestrator.py:926` | `def test_orchestrator_success_maps_to_ai_result(self, monkeypatch)` |
| `test_pentest_prose_with_unauthorized_word_is_content` | method | `tests/test_llm_orchestrator.py:723` | `def test_pentest_prose_with_unauthorized_word_is_content(self)` |
| `test_phishing_prose_with_credit_word_is_content` | method | `tests/test_llm_orchestrator.py:729` | `def test_phishing_prose_with_credit_word_is_content(self)` |
| `test_placeholder_env_replaced_by_payload_key` | method | `tests/test_llm_orchestrator.py:849` | `def test_placeholder_env_replaced_by_payload_key(self, monkeypatch)` |
| `test_placeholder_env_survives_without_payload_key` | method | `tests/test_llm_orchestrator.py:867` | `def test_placeholder_env_survives_without_payload_key(self, monkeypatch)` |
| `test_placeholder_fragments_recognized` | method | `tests/test_llm_orchestrator.py:822` | `def test_placeholder_fragments_recognized(self)` |
| `test_placeholder_groq_leg_refused_even_with_payload_key` | method | `tests/test_llm_orchestrator.py:802` | `def test_placeholder_groq_leg_refused_even_with_payload_key(self, monkeypatch)` |
| `test_placeholder_groq_leg_refused_without_doomed_call` | method | `tests/test_llm_orchestrator.py:776` | `def test_placeholder_groq_leg_refused_without_doomed_call(self, monkeypatch)` |
| `test_placeholder_payload_key_not_published` | method | `tests/test_llm_orchestrator.py:906` | `def test_placeholder_payload_key_not_published(self, monkeypatch)` |
| `test_pool_chain_reads_lazy_orchestrator_store` | method | `tests/test_llm_orchestrator.py:119` | `def test_pool_chain_reads_lazy_orchestrator_store(self, isolated_pool)` |
| `test_pool_chain_returns_empty_when_pool_unreadable` | method | `tests/test_llm_orchestrator.py:140` | `def test_pool_chain_returns_empty_when_pool_unreadable(self, monkeypatch)` |
| `test_pool_chain_self_heals_corrupt_store` | method | `tests/test_llm_orchestrator.py:132` | `def test_pool_chain_self_heals_corrupt_store(self, isolated_pool)` |
| `test_primary_failure_serves_fallback_with_notice` | method | `tests/test_llm_orchestrator.py:174` | `def test_primary_failure_serves_fallback_with_notice(self)` |
| `test_primary_success_needs_no_fallback` | method | `tests/test_llm_orchestrator.py:153` | `def test_primary_success_needs_no_fallback(self)` |
| `test_quota_wording_reply_is_a_failure` | method | `tests/test_llm_orchestrator.py:249` | `def test_quota_wording_reply_is_a_failure(self)` |
| `test_real_answer_not_treated_as_error` | method | `tests/test_llm_orchestrator.py:718` | `def test_real_answer_not_treated_as_error(self)` |
| `test_real_key_not_a_placeholder` | method | `tests/test_llm_orchestrator.py:828` | `def test_real_key_not_a_placeholder(self)` |
| `test_sort_members_never_mutates_input` | method | `tests/test_llm_orchestrator.py:113` | `def test_sort_members_never_mutates_input(self)` |
| `test_success_is_recorded_in_the_pool_ledger` | method | `tests/test_llm_orchestrator.py:449` | `def test_success_is_recorded_in_the_pool_ledger(self, isolated_pool)` |
| `test_success_reports_health` | method | `tests/test_llm_orchestrator.py:386` | `def test_success_reports_health(self)` |
| `test_system_prompt_is_prepended_for_the_executor` | method | `tests/test_llm_orchestrator.py:277` | `def test_system_prompt_is_prepended_for_the_executor(self)` |
| `test_total_failure_returns_help_message` | method | `tests/test_llm_orchestrator.py:983` | `def test_total_failure_returns_help_message(self, monkeypatch)` |
| `test_unhealthy_member_is_skipped_while_others_remain` | method | `tests/test_llm_orchestrator.py:354` | `def test_unhealthy_member_is_skipped_while_others_remain(self)` |
| `test_weights_sort_members_by_descending_priority` | method | `tests/test_llm_orchestrator.py:102` | `def test_weights_sort_members_by_descending_priority(self)` |
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
| `_FakeTrainer` | class | `tests/test_loop_ai_bridge.py:179` | `class _FakeTrainer` |
| `_Oracle` | class | `tests/test_loop_ai_bridge.py:63` | `class _Oracle` |
| `__init__` | method | `tests/test_loop_ai_bridge.py:180` | `def __init__(self)` |
| `_complete` | function | `tests/test_loop_ai_bridge.py:372` | `def _complete(model, prompt, max_tokens)` |
| `_swan` | function | `tests/test_loop_ai_bridge.py:392` | `def _swan(prompt, task_type, phase, timeout)` |
| `_yields` | function | `tests/test_loop_ai_bridge.py:322` | `def _yields(summaries, phase)` |
| `assess` | method | `tests/test_loop_ai_bridge.py:64` | `def assess(self, tool, command, category)` |
| `boom` | function | `tests/test_loop_ai_bridge.py:125` | `def boom()` |
| `bridge` | function | `tests/test_loop_ai_bridge.py:25` | `def bridge(monkeypatch)` |
| `encode_state` | method | `tests/test_loop_ai_bridge.py:183` | `def encode_state(self, task_type, phase, ema)` |
| `publish` | method | `tests/test_loop_ai_bridge.py:39` | `def publish(self, event)` |
| `q_values_for_state` | method | `tests/test_loop_ai_bridge.py:192` | `def q_values_for_state(self, state, candidates)` |
| `store` | function | `tests/test_loop_ai_bridge.py:15` | `def store(tmp_path, monkeypatch)` |
| `test_activity_log_publishes_to_bridge` | function | `tests/test_loop_ai_bridge.py:52` | `def test_activity_log_publishes_to_bridge(store, bridge, monkeypatch)` |
| `test_annotate_detection_uses_oracle` | function | `tests/test_loop_ai_bridge.py:62` | `def test_annotate_detection_uses_oracle(bridge, monkeypatch)` |
| `test_assess_opsec_graceful_on_scorer_failure` | function | `tests/test_loop_ai_bridge.py:124` | `def test_assess_opsec_graceful_on_scorer_failure(bridge, monkeypatch)` |
| `test_assess_opsec_off_when_stage_disabled` | function | `tests/test_loop_ai_bridge.py:117` | `def test_assess_opsec_off_when_stage_disabled(monkeypatch)` |
| `test_assess_opsec_wraps_scorer_v2` | function | `tests/test_loop_ai_bridge.py:108` | `def test_assess_opsec_wraps_scorer_v2(bridge)` |
| `test_decision_quality_reward_is_closed_loop` | function | `tests/test_loop_ai_bridge.py:170` | `def test_decision_quality_reward_is_closed_loop(bridge)` |
| `test_finish_records_decision_quality_outcome` | function | `tests/test_loop_ai_bridge.py:283` | `def test_finish_records_decision_quality_outcome(store, bridge, monkeypatch)` |
| `test_intent_tool_class_mapping` | function | `tests/test_loop_ai_bridge.py:132` | `def test_intent_tool_class_mapping(bridge)` |
| `test_llm_pool_prefers_moe_expert_and_records_outcome` | function | `tests/test_loop_ai_bridge.py:360` | `def test_llm_pool_prefers_moe_expert_and_records_outcome(store, bridge, monkeypatch)` |
| `test_planner_rl_rank_demotes_low_yield_and_boosts_high` | function | `tests/test_loop_ai_bridge.py:312` | `def test_planner_rl_rank_demotes_low_yield_and_boosts_high(store, bridge, monkeypatch)` |
| `test_planner_rl_rank_noop_without_learned_yield` | function | `tests/test_loop_ai_bridge.py:343` | `def test_planner_rl_rank_noop_without_learned_yield(store, monkeypatch)` |
| `test_planner_uses_swan_when_available` | function | `tests/test_loop_ai_bridge.py:385` | `def test_planner_uses_swan_when_available(store, bridge, monkeypatch)` |
| `test_publish_loop_event_skips_stream_kinds` | function | `tests/test_loop_ai_bridge.py:34` | `def test_publish_loop_event_skips_stream_kinds(bridge, monkeypatch)` |
| `test_record_outcome_quality_noop_without_class` | function | `tests/test_loop_ai_bridge.py:163` | `def test_record_outcome_quality_noop_without_class(bridge, monkeypatch)` |
| `test_record_outcome_quality_rewards_findings_over_facts` | function | `tests/test_loop_ai_bridge.py:144` | `def test_record_outcome_quality_rewards_findings_over_facts(bridge, monkeypatch)` |
| `test_record_step_rewards_shell_above_plain_success` | function | `tests/test_loop_ai_bridge.py:405` | `def test_record_step_rewards_shell_above_plain_success(bridge, monkeypatch)` |
| `test_record_step_shell_reward_ignores_benign_banner` | function | `tests/test_loop_ai_bridge.py:429` | `def test_record_step_shell_reward_ignores_benign_banner(bridge, monkeypatch)` |
| `test_worker_annotates_detection_and_records_outcome` | function | `tests/test_loop_ai_bridge.py:74` | `def test_worker_annotates_detection_and_records_outcome(store, bridge, monkeypatch)` |
| `test_worker_blocks_on_opsec_gate` | function | `tests/test_loop_ai_bridge.py:207` | `def test_worker_blocks_on_opsec_gate(store, bridge, monkeypatch)` |
| `test_worker_confirms_via_intercept_on_opsec_confirm` | function | `tests/test_loop_ai_bridge.py:239` | `def test_worker_confirms_via_intercept_on_opsec_confirm(store, bridge, monkeypatch)` |
| `update` | method | `tests/test_loop_ai_bridge.py:186` | `def update(self, state, action, reward, next_state, candidates, detection_prob)` |
| `audit_dir` | function | `tests/test_loop_audit.py:11` | `def audit_dir(tmp_path, monkeypatch)` |
| `test_blocked_events` | function | `tests/test_loop_audit.py:86` | `def test_blocked_events(audit_dir)` |
| `test_cap_trims_oldest` | function | `tests/test_loop_audit.py:172` | `def test_cap_trims_oldest(audit_dir, monkeypatch)` |
| `test_list_runs_summarizes` | function | `tests/test_loop_audit.py:145` | `def test_list_runs_summarizes(audit_dir)` |
| `test_output_tail_bounded_and_ansi_stripped` | function | `tests/test_loop_audit.py:74` | `def test_output_tail_bounded_and_ansi_stripped(audit_dir)` |
| `test_record_appends_events` | function | `tests/test_loop_audit.py:20` | `def test_record_appends_events(audit_dir)` |
| `test_record_command_carries_step_context` | function | `tests/test_loop_audit.py:35` | `def test_record_command_carries_step_context(audit_dir)` |
| `test_record_command_detects_failure` | function | `tests/test_loop_audit.py:65` | `def test_record_command_detects_failure(audit_dir)` |
| `test_registry_start_and_stop` | function | `tests/test_loop_audit.py:96` | `def test_registry_start_and_stop(audit_dir)` |
| `test_render_shows_verdict_and_run_end` | function | `tests/test_loop_audit.py:132` | `def test_render_shows_verdict_and_run_end(audit_dir)` |
| `test_render_summary_empty` | function | `tests/test_loop_audit.py:166` | `def test_render_summary_empty(audit_dir)` |
| `test_timeline_merges_guard_and_activity` | function | `tests/test_loop_audit.py:106` | `def test_timeline_merges_guard_and_activity(audit_dir, monkeypatch)` |
| `_write_run` | function | `tests/test_loop_audit_feedback.py:29` | `def _write_run(task_id)` |
| `audit` | function | `tests/test_loop_audit_feedback.py:24` | `def audit(tmp_path, monkeypatch)` |
| `test_blocked_verbs_empty_for_unknown_task` | function | `tests/test_loop_audit_feedback.py:51` | `def test_blocked_verbs_empty_for_unknown_task(audit)` |
| `test_blocked_verbs_ignores_executed_commands` | function | `tests/test_loop_audit_feedback.py:55` | `def test_blocked_verbs_ignores_executed_commands(audit)` |
| `test_blocked_verbs_returns_repeat_offenders` | function | `tests/test_loop_audit_feedback.py:39` | `def test_blocked_verbs_returns_repeat_offenders(audit)` |
| `test_blocked_verbs_threshold_respected` | function | `tests/test_loop_audit_feedback.py:45` | `def test_blocked_verbs_threshold_respected(audit)` |
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
| `test_check_leakage_detects_broken_fence` | function | `tests/test_loop_boundary.py:38` | `def test_check_leakage_detects_broken_fence()` |
| `test_check_leakage_ignores_normal_text` | function | `tests/test_loop_boundary.py:45` | `def test_check_leakage_ignores_normal_text()` |
| `test_code_tail_is_stable` | function | `tests/test_loop_boundary.py:49` | `def test_code_tail_is_stable()` |
| `test_fence_empty_content_is_empty` | function | `tests/test_loop_boundary.py:29` | `def test_fence_empty_content_is_empty()` |
| `test_fence_nonce_differs_every_call` | function | `tests/test_loop_boundary.py:23` | `def test_fence_nonce_differs_every_call()` |
| `test_fence_truncates_huge_content` | function | `tests/test_loop_boundary.py:33` | `def test_fence_truncates_huge_content()` |
| `test_fence_wraps_content_with_markers` | function | `tests/test_loop_boundary.py:15` | `def test_fence_wraps_content_with_markers()` |
| `test_tail_sections_appends_tail_once` | function | `tests/test_loop_boundary.py:54` | `def test_tail_sections_appends_tail_once()` |
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
| `FakePool` | class | `tests/test_loop_citation_judge.py:98` | `class FakePool` |
| `FakeTraffic` | class | `tests/test_loop_citation_judge.py:22` | `class FakeTraffic` |
| `__init__` | method | `tests/test_loop_citation_judge.py:23` | `def __init__(self, rows)` |
| `complete` | method | `tests/test_loop_citation_judge.py:102` | `def complete(self, prompt, max_tokens)` |
| `members` | method | `tests/test_loop_citation_judge.py:99` | `def members(self)` |
| `read` | method | `tests/test_loop_citation_judge.py:27` | `def read(self, limit)` |
| `record` | method | `tests/test_loop_citation_judge.py:30` | `def record(self, kind, command, output, meta)` |
| `sandbox` | function | `tests/test_loop_citation_judge.py:14` | `def sandbox(tmp_path, monkeypatch)` |
| `test_citation_verdict_none_when_output_stale` | function | `tests/test_loop_citation_judge.py:68` | `def test_citation_verdict_none_when_output_stale(sandbox, monkeypatch)` |
| `test_citation_verdict_none_without_quote` | function | `tests/test_loop_citation_judge.py:61` | `def test_citation_verdict_none_without_quote(sandbox)` |
| `test_citation_verdict_reproduces_without_execution` | function | `tests/test_loop_citation_judge.py:35` | `def test_citation_verdict_reproduces_without_execution(sandbox)` |
| `test_judge_prompt_fenced_when_enabled` | function | `tests/test_loop_citation_judge.py:92` | `def test_judge_prompt_fenced_when_enabled(sandbox, monkeypatch)` |
| `test_report_binds_quote_meta` | function | `tests/test_loop_citation_judge.py:84` | `def test_report_binds_quote_meta(sandbox)` |
| `_broken` | function | `tests/test_loop_cli_catalog.py:90` | `def _broken()` |
| `_default` | function | `tests/test_loop_cli_catalog.py:47` | `def _default(cfg)` |
| `sandbox` | function | `tests/test_loop_cli_catalog.py:17` | `def sandbox(tmp_path, monkeypatch)` |
| `test_catalog_cli_for_phase_lists_enabled_only` | function | `tests/test_loop_cli_catalog.py:56` | `def test_catalog_cli_for_phase_lists_enabled_only(sandbox)` |
| `test_missing_catalog_view_adds_nothing` | function | `tests/test_loop_cli_catalog.py:79` | `def test_missing_catalog_view_adds_nothing(tmp_path, monkeypatch)` |
| `test_multi_phase_verb_visible_in_each_declared_phase` | function | `tests/test_loop_cli_catalog.py:101` | `def test_multi_phase_verb_visible_in_each_declared_phase(sandbox, monkeypatch)` |
| `test_prompt_context_carries_allowed_commands` | function | `tests/test_loop_cli_catalog.py:66` | `def test_prompt_context_carries_allowed_commands(sandbox)` |
| `_old_facts` | function | `tests/test_loop_cold_overview.py:15` | `def _old_facts(graph, count, prefix)` |
| `_patched_engine` | function | `tests/test_loop_cold_overview.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_compact_debounce_keeps_fresh_hot` | function | `tests/test_loop_cold_overview.py:28` | `def test_compact_debounce_keeps_fresh_hot(tmp_path, monkeypatch)` |
| `test_compact_folds_stale_facts` | function | `tests/test_loop_cold_overview.py:41` | `def test_compact_folds_stale_facts(tmp_path, monkeypatch)` |
| `test_graph_overview_carries_findings_and_done_totals` | function | `tests/test_loop_cold_overview.py:77` | `def test_graph_overview_carries_findings_and_done_totals(tmp_path, monkeypatch)` |
| `test_planner_round_folds_minor_window` | function | `tests/test_loop_cold_overview.py:56` | `def test_planner_round_folds_minor_window(tmp_path, monkeypatch)` |
| `_Ctx` | class | `tests/test_loop_decision_log.py:20` | `class _Ctx` |
| `__init__` | method | `tests/test_loop_decision_log.py:23` | `def __init__(self, extra, services)` |
| `test_config_digest_empty_inputs` | function | `tests/test_loop_decision_log.py:67` | `def test_config_digest_empty_inputs()` |
| `test_config_digest_only_tracks_relevant_keys` | function | `tests/test_loop_decision_log.py:59` | `def test_config_digest_only_tracks_relevant_keys()` |
| `test_config_digest_tracks_determinism_flags` | function | `tests/test_loop_decision_log.py:73` | `def test_config_digest_tracks_determinism_flags()` |
| `test_context_digest_changes_with_state` | function | `tests/test_loop_decision_log.py:52` | `def test_context_digest_changes_with_state()` |
| `test_context_digest_ignores_mapping_order` | function | `tests/test_loop_decision_log.py:40` | `def test_context_digest_ignores_mapping_order()` |
| `test_context_digest_ignores_service_order` | function | `tests/test_loop_decision_log.py:46` | `def test_context_digest_ignores_service_order()` |
| `test_digest_is_stable_and_bounded` | function | `tests/test_loop_decision_log.py:33` | `def test_digest_is_stable_and_bounded()` |
| `test_extract_dedupes_preserving_order` | function | `tests/test_loop_decision_log.py:162` | `def test_extract_dedupes_preserving_order()` |
| `test_extract_empty_reply` | function | `tests/test_loop_decision_log.py:166` | `def test_extract_empty_reply()` |
| `test_extract_json_contract` | function | `tests/test_loop_decision_log.py:140` | `def test_extract_json_contract()` |
| `test_extract_json_fenced_block` | function | `tests/test_loop_decision_log.py:145` | `def test_extract_json_fenced_block()` |
| `test_extract_json_string_array` | function | `tests/test_loop_decision_log.py:150` | `def test_extract_json_string_array()` |
| `test_extract_line_fallback_on_non_json` | function | `tests/test_loop_decision_log.py:154` | `def test_extract_line_fallback_on_non_json()` |
| `test_filtered_rows_bounds_and_shape` | function | `tests/test_loop_decision_log.py:134` | `def test_filtered_rows_bounds_and_shape()` |
| `test_planner_temperature_clamps_negative` | function | `tests/test_loop_decision_log.py:188` | `def test_planner_temperature_clamps_negative(monkeypatch)` |
| `test_planner_temperature_default_is_greedy` | function | `tests/test_loop_decision_log.py:171` | `def test_planner_temperature_default_is_greedy(monkeypatch)` |
| `test_planner_temperature_reads_payload` | function | `tests/test_loop_decision_log.py:179` | `def test_planner_temperature_reads_payload(monkeypatch)` |
| `test_planner_temperature_survives_malformed` | function | `tests/test_loop_decision_log.py:197` | `def test_planner_temperature_survives_malformed(monkeypatch)` |
| `test_read_records_skips_corrupt_lines` | function | `tests/test_loop_decision_log.py:101` | `def test_read_records_skips_corrupt_lines(tmp_path)` |
| `test_record_and_read_round_trip` | function | `tests/test_loop_decision_log.py:80` | `def test_record_and_read_round_trip(tmp_path)` |
| `test_record_marks_model_fallback_for_llm` | function | `tests/test_loop_decision_log.py:108` | `def test_record_marks_model_fallback_for_llm(tmp_path)` |
| `test_record_never_raises_on_bad_path` | function | `tests/test_loop_decision_log.py:127` | `def test_record_never_raises_on_bad_path(tmp_path)` |
| `_spy_llm_tiers` | function | `tests/test_loop_deterministic_first.py:45` | `def _spy_llm_tiers(worker, monkeypatch, calls)` |
| `test_default_off_keeps_llm_first_for_exploit` | function | `tests/test_loop_deterministic_first.py:88` | `def test_default_off_keeps_llm_first_for_exploit(worker_env, monkeypatch)` |
| `test_exploit_intent_skips_llm_tiers_when_enabled` | function | `tests/test_loop_deterministic_first.py:63` | `def test_exploit_intent_skips_llm_tiers_when_enabled(worker_env, monkeypatch)` |
| `test_loop_exploit_first_opt_in_default_off` | function | `tests/test_loop_deterministic_first.py:56` | `def test_loop_exploit_first_opt_in_default_off()` |
| `test_recon_intent_still_uses_llm_tiers_when_enabled` | function | `tests/test_loop_deterministic_first.py:77` | `def test_recon_intent_still_uses_llm_tiers_when_enabled(worker_env, monkeypatch)` |
| `worker_env` | function | `tests/test_loop_deterministic_first.py:17` | `def worker_env(tmp_path, monkeypatch)` |
| `_Activity` | class | `tests/test_loop_deterministic_mode.py:17` | `class _Activity` |
| `_PlaceholderThenReal` | class | `tests/test_loop_deterministic_mode.py:75` | `class _PlaceholderThenReal(_Worker)` |
| `_Worker` | class | `tests/test_loop_deterministic_mode.py:27` | `class _Worker(WorkerAgenticMixin)` |
| `__init__` | method | `tests/test_loop_deterministic_mode.py:20` | `def __init__(self)` |
| `__init__` | method | `tests/test_loop_deterministic_mode.py:30` | `def __init__(self, suggested)` |
| `_boom` | function | `tests/test_loop_deterministic_mode.py:123` | `def _boom()` |
| `_intent` | function | `tests/test_loop_deterministic_mode.py:39` | `def _intent()` |
| `_llm_steps` | method | `tests/test_loop_deterministic_mode.py:35` | `def _llm_steps(self, intent, prior_text)` |
| `_llm_steps` | method | `tests/test_loop_deterministic_mode.py:76` | `def _llm_steps(self, intent, prior_text)` |
| `emit` | method | `tests/test_loop_deterministic_mode.py:23` | `def emit(self)` |
| `test_default_mode_prefixes_llm` | function | `tests/test_loop_deterministic_mode.py:49` | `def test_default_mode_prefixes_llm(monkeypatch)` |
| `test_deterministic_fallback_orders_heuristic_first` | function | `tests/test_loop_deterministic_mode.py:72` | `def test_deterministic_fallback_orders_heuristic_first(monkeypatch)` |
| `test_deterministic_mode_enforces_guard_and_records_decision` | function | `tests/test_loop_deterministic_mode.py:84` | `def test_deterministic_mode_enforces_guard_and_records_decision(monkeypatch, tmp_path)` |
| `test_deterministic_mode_falls_back_to_model_on_placeholder` | function | `tests/test_loop_deterministic_mode.py:65` | `def test_deterministic_mode_falls_back_to_model_on_placeholder(monkeypatch)` |
| `test_deterministic_mode_heuristic_wins_and_skips_model` | function | `tests/test_loop_deterministic_mode.py:57` | `def test_deterministic_mode_heuristic_wins_and_skips_model(monkeypatch)` |
| `test_is_placeholder_detects_no_target` | function | `tests/test_loop_deterministic_mode.py:43` | `def test_is_placeholder_detects_no_target()` |
| `test_loop_deterministic_reads_payload` | function | `tests/test_loop_deterministic_mode.py:111` | `def test_loop_deterministic_reads_payload(monkeypatch)` |
| `test_loop_deterministic_survives_error` | function | `tests/test_loop_deterministic_mode.py:120` | `def test_loop_deterministic_survives_error(monkeypatch)` |
| `FakeTraffic` | class | `tests/test_loop_evidence.py:15` | `class FakeTraffic` |
| `__init__` | method | `tests/test_loop_evidence.py:16` | `def __init__(self, rows)` |
| `boom` | function | `tests/test_loop_evidence.py:87` | `def boom(command)` |
| `read` | method | `tests/test_loop_evidence.py:19` | `def read(self, limit)` |
| `record` | method | `tests/test_loop_evidence.py:22` | `def record(self, kind, command, output, meta)` |
| `test_annotate_writes_meta` | function | `tests/test_loop_evidence.py:99` | `def test_annotate_writes_meta()` |
| `test_extract_quote_backtick` | function | `tests/test_loop_evidence.py:42` | `def test_extract_quote_backtick()` |
| `test_extract_quote_double` | function | `tests/test_loop_evidence.py:38` | `def test_extract_quote_double()` |
| `test_extract_quote_label` | function | `tests/test_loop_evidence.py:46` | `def test_extract_quote_label()` |
| `test_extract_quote_no_quote` | function | `tests/test_loop_evidence.py:50` | `def test_extract_quote_no_quote()` |
| `test_normalize_ws` | function | `tests/test_loop_evidence.py:26` | `def test_normalize_ws()` |
| `test_replay_empty_command` | function | `tests/test_loop_evidence.py:95` | `def test_replay_empty_command()` |
| `test_replay_executes_and_records` | function | `tests/test_loop_evidence.py:76` | `def test_replay_executes_and_records()` |
| `test_replay_failure_is_reported` | function | `tests/test_loop_evidence.py:84` | `def test_replay_failure_is_reported()` |
| `test_verbatim_contains` | function | `tests/test_loop_evidence.py:31` | `def test_verbatim_contains()` |
| `test_verify_hits_fresh_record` | function | `tests/test_loop_evidence.py:54` | `def test_verify_hits_fresh_record()` |
| `test_verify_no_traffic` | function | `tests/test_loop_evidence.py:72` | `def test_verify_no_traffic()` |
| `test_verify_rejects_stale_record` | function | `tests/test_loop_evidence.py:64` | `def test_verify_rejects_stale_record()` |
| `TestContracts` | class | `tests/test_loop_evidence_wiring.py:170` | `class TestContracts` |
| `TestEvidenceDualHash` | class | `tests/test_loop_evidence_wiring.py:142` | `class TestEvidenceDualHash` |
| `TestShellProofPublication` | class | `tests/test_loop_evidence_wiring.py:61` | `class TestShellProofPublication` |
| `TestTrafficDigest` | class | `tests/test_loop_evidence_wiring.py:131` | `class TestTrafficDigest` |
| `TestWorkerTraces` | class | `tests/test_loop_evidence_wiring.py:83` | `class TestWorkerTraces` |
| `_intent` | function | `tests/test_loop_evidence_wiring.py:56` | `def _intent(node_id)` |
| `_worker` | function | `tests/test_loop_evidence_wiring.py:49` | `def _worker(task_id)` |
| `fake_record` | function | `tests/test_loop_evidence_wiring.py:34` | `def fake_record()` |
| `sink_log` | function | `tests/test_loop_evidence_wiring.py:27` | `def sink_log()` |
| `test_empty_transcripts_write_nothing` | method | `tests/test_loop_evidence_wiring.py:120` | `def test_empty_transcripts_write_nothing(self, tmp_path)` |
| `test_full_body_hash_and_stored_hash` | method | `tests/test_loop_evidence_wiring.py:143` | `def test_full_body_hash_and_stored_hash(self, tmp_path)` |
| `test_junk_output_never_publishes` | method | `tests/test_loop_evidence_wiring.py:71` | `def test_junk_output_never_publishes(self, sink_log)` |
| `test_no_target_no_event` | method | `tests/test_loop_evidence_wiring.py:77` | `def test_no_target_no_event(self, sink_log)` |
| `test_publishes_exploit_event_with_shell_flag` | method | `tests/test_loop_evidence_wiring.py:62` | `def test_publishes_exploit_event_with_shell_flag(self, sink_log)` |
| `test_rotation_keeps_tail` | method | `tests/test_loop_evidence_wiring.py:103` | `def test_rotation_keeps_tail(self, tmp_path)` |
| `test_rows_written_reader_schema` | method | `tests/test_loop_evidence_wiring.py:84` | `def test_rows_written_reader_schema(self, tmp_path)` |
| `test_same_output_same_digest_other_output_differs` | method | `tests/test_loop_evidence_wiring.py:132` | `def test_same_output_same_digest_other_output_differs(self)` |
| `test_tamper_detected` | method | `tests/test_loop_evidence_wiring.py:156` | `def test_tamper_detected(self, tmp_path)` |
| `test_wiring_sources` | method | `tests/test_loop_evidence_wiring.py:171` | `def test_wiring_sources(self)` |
| `_ExitShell` | class | `tests/test_loop_exit_gate.py:137` | `class _ExitShell` |
| `_Shell` | class | `tests/test_loop_exit_gate.py:158` | `class _Shell` |
| `__init__` | method | `tests/test_loop_exit_gate.py:138` | `def __init__(self, code)` |
| `__init__` | method | `tests/test_loop_exit_gate.py:159` | `def __init__(self)` |
| `_abort_cause_literals` | function | `tests/test_loop_exit_gate.py:14` | `def _abort_cause_literals(source)` |
| `onecmd` | method | `tests/test_loop_exit_gate.py:141` | `def onecmd(self, cmd)` |
| `onecmd` | method | `tests/test_loop_exit_gate.py:162` | `def onecmd(self, cmd)` |
| `test_autonomous_gate_raises_only_when_env_set` | function | `tests/test_loop_exit_gate.py:90` | `def test_autonomous_gate_raises_only_when_env_set(monkeypatch)` |
| `test_every_abort_call_site_uses_a_registered_cause` | function | `tests/test_loop_exit_gate.py:42` | `def test_every_abort_call_site_uses_a_registered_cause()` |
| `test_headless_catches_systemexit` | function | `tests/test_loop_exit_gate.py:145` | `def test_headless_catches_systemexit()` |
| `test_headless_chain_stops_on_failure` | function | `tests/test_loop_exit_gate.py:155` | `def test_headless_chain_stops_on_failure()` |
| `test_loop_exit_code_mapping` | function | `tests/test_loop_exit_gate.py:55` | `def test_loop_exit_code_mapping()` |
| `test_report_result_prints_verdict` | function | `tests/test_loop_exit_gate.py:176` | `def test_report_result_prints_verdict(capsys)` |
| `test_terminal_autopwn_fallback_cause_is_valid` | function | `tests/test_loop_exit_gate.py:36` | `def test_terminal_autopwn_fallback_cause_is_valid()` |
| `test_write_loop_result_sessions_fallback` | function | `tests/test_loop_exit_gate.py:125` | `def test_write_loop_result_sessions_fallback(tmp_path, monkeypatch)` |
| `test_write_loop_result_workspace` | function | `tests/test_loop_exit_gate.py:109` | `def test_write_loop_result_workspace(tmp_path, monkeypatch)` |
| `TestCascadeFirePending` | class | `tests/test_loop_fire_pending.py:63` | `class TestCascadeFirePending` |
| `TestPlannerFireIntent` | class | `tests/test_loop_fire_pending.py:75` | `class TestPlannerFireIntent` |
| `TestRegistry` | class | `tests/test_loop_fire_pending.py:157` | `class TestRegistry` |
| `TestWorkerExecutesFireAction` | class | `tests/test_loop_fire_pending.py:105` | `class TestWorkerExecutesFireAction` |
| `_RecordingShell` | class | `tests/test_loop_fire_pending.py:33` | `class _RecordingShell` |
| `__init__` | method | `tests/test_loop_fire_pending.py:36` | `def __init__(self)` |
| `fire_report` | function | `tests/test_loop_fire_pending.py:45` | `def fire_report(tmp_path, monkeypatch)` |
| `onecmd_plus_hooks` | method | `tests/test_loop_fire_pending.py:39` | `def onecmd_plus_hooks(self, line)` |
| `test_cascade_answers_fire_first` | method | `tests/test_loop_fire_pending.py:64` | `def test_cascade_answers_fire_first(self, fire_report)` |
| `test_lazy_intel_verbs_routable` | method | `tests/test_loop_fire_pending.py:158` | `def test_lazy_intel_verbs_routable(self)` |
| `test_planner_dedupes_after_first_proposal` | method | `tests/test_loop_fire_pending.py:91` | `def test_planner_dedupes_after_first_proposal(self, fire_report, monkeypatch)` |
| `test_planner_queues_fire_action` | method | `tests/test_loop_fire_pending.py:76` | `def test_planner_queues_fire_action(self, fire_report, monkeypatch)` |
| `test_registry_routes_and_shell_receives` | method | `tests/test_loop_fire_pending.py:128` | `def test_registry_routes_and_shell_receives(self)` |
| `test_steps_expand_verbatim` | method | `tests/test_loop_fire_pending.py:106` | `def test_steps_expand_verbatim(self)` |
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
| `test_listing_noise_flags_recursive_session_dump` | function | `tests/test_loop_guardrails.py:152` | `def test_listing_noise_flags_recursive_session_dump()` |
| `test_listing_noise_ignores_real_postexp_find_output` | function | `tests/test_loop_guardrails.py:161` | `def test_listing_noise_ignores_real_postexp_find_output()` |
| `test_listing_noise_ignores_small_and_banner_outputs` | function | `tests/test_loop_guardrails.py:170` | `def test_listing_noise_ignores_small_and_banner_outputs()` |
| `test_listing_policy_allows_find_with_filters_and_work` | function | `tests/test_loop_guardrails.py:190` | `def test_listing_policy_allows_find_with_filters_and_work()` |
| `test_listing_policy_rejects_bare_find` | function | `tests/test_loop_guardrails.py:199` | `def test_listing_policy_rejects_bare_find()` |
| `test_listing_policy_vetoes_ls_family` | function | `tests/test_loop_guardrails.py:181` | `def test_listing_policy_vetoes_ls_family()` |
| `test_repeat_detector_flags_identical_window` | function | `tests/test_loop_guardrails.py:12` | `def test_repeat_detector_flags_identical_window()` |
| `test_repeat_detector_recovery_on_variation` | function | `tests/test_loop_guardrails.py:21` | `def test_repeat_detector_recovery_on_variation()` |
| `test_target_limiter_caps_concurrency` | function | `tests/test_loop_guardrails.py:67` | `def test_target_limiter_caps_concurrency()` |
| `test_target_limiter_empty_target_bypasses` | function | `tests/test_loop_guardrails.py:112` | `def test_target_limiter_empty_target_bypasses()` |
| `test_target_limiter_is_reentrant_per_thread` | function | `tests/test_loop_guardrails.py:93` | `def test_target_limiter_is_reentrant_per_thread()` |
| `_Node` | class | `tests/test_loop_idempotent_retest.py:37` | `class _Node` |
| `_sandbox` | function | `tests/test_loop_idempotent_retest.py:17` | `def _sandbox(tmp_path, monkeypatch)` |
| `test_claim_effect_dedupes_by_target_vector` | function | `tests/test_loop_idempotent_retest.py:98` | `def test_claim_effect_dedupes_by_target_vector()` |
| `test_claim_effect_fail_open_on_empty` | function | `tests/test_loop_idempotent_retest.py:111` | `def test_claim_effect_fail_open_on_empty()` |
| `test_exploit_finding_not_replayed_without_session` | function | `tests/test_loop_idempotent_retest.py:53` | `def test_exploit_finding_not_replayed_without_session(tmp_path, monkeypatch)` |
| `test_exploit_finding_verified_via_live_session` | function | `tests/test_loop_idempotent_retest.py:73` | `def test_exploit_finding_verified_via_live_session(tmp_path, monkeypatch)` |
| `test_exploit_target_prefers_command_then_text` | function | `tests/test_loop_idempotent_retest.py:34` | `def test_exploit_target_prefers_command_then_text()` |
| `test_is_exploit_command_recognizes_access_verbs` | function | `tests/test_loop_idempotent_retest.py:24` | `def test_is_exploit_command_recognizes_access_verbs()` |
| `test_probe_live_shell_no_session_returns_none` | function | `tests/test_loop_idempotent_retest.py:117` | `def test_probe_live_shell_no_session_returns_none()` |
| `test_session_verdict_passthrough_for_non_exploit` | function | `tests/test_loop_idempotent_retest.py:44` | `def test_session_verdict_passthrough_for_non_exploit(tmp_path, monkeypatch)` |
| `test_terminal_fallback_reuses_live_session` | function | `tests/test_loop_idempotent_retest.py:123` | `def test_terminal_fallback_reuses_live_session(tmp_path, monkeypatch)` |
| `test_terminal_fallback_skips_when_effect_locked` | function | `tests/test_loop_idempotent_retest.py:145` | `def test_terminal_fallback_skips_when_effect_locked(tmp_path, monkeypatch)` |
| `_Assets` | class | `tests/test_loop_intel_projection.py:114` | `class _Assets` |
| `_Evidence` | class | `tests/test_loop_intel_projection.py:86` | `class _Evidence` |
| `_FindingService` | class | `tests/test_loop_intel_projection.py:78` | `class _FindingService` |
| `_Graph` | class | `tests/test_loop_intel_projection.py:47` | `class _Graph` |
| `_Graph` | class | `tests/test_loop_intel_projection.py:96` | `class _Graph` |
| `_Traffic` | class | `tests/test_loop_intel_projection.py:118` | `class _Traffic` |
| `__init__` | method | `tests/test_loop_intel_projection.py:79` | `def __init__(self)` |
| `__init__` | method | `tests/test_loop_intel_projection.py:87` | `def __init__(self)` |
| `_sandbox` | function | `tests/test_loop_intel_projection.py:17` | `def _sandbox(tmp_path, monkeypatch)` |
| `add` | method | `tests/test_loop_intel_projection.py:90` | `def add(self)` |
| `add_edge` | method | `tests/test_loop_intel_projection.py:102` | `def add_edge(self)` |
| `add_node` | method | `tests/test_loop_intel_projection.py:99` | `def add_node(self, kind, text)` |
| `anchor` | method | `tests/test_loop_intel_projection.py:111` | `def anchor(self)` |
| `anchors_for` | method | `tests/test_loop_intel_projection.py:108` | `def anchors_for(self, node_id)` |
| `bind` | method | `tests/test_loop_intel_projection.py:122` | `def bind(self)` |
| `has_finding` | method | `tests/test_loop_intel_projection.py:105` | `def has_finding(self, text)` |
| `insert` | method | `tests/test_loop_intel_projection.py:115` | `def insert(self)` |
| `overview` | method | `tests/test_loop_intel_projection.py:50` | `def overview(self)` |
| `read` | method | `tests/test_loop_intel_projection.py:119` | `def read(self, _n)` |
| `report` | method | `tests/test_loop_intel_projection.py:82` | `def report(self)` |
| `test_derive_finding_class_maps_marks_and_cve` | function | `tests/test_loop_intel_projection.py:24` | `def test_derive_finding_class_maps_marks_and_cve()` |
| `test_graph_state_projects_known_assets` | function | `tests/test_loop_intel_projection.py:43` | `def test_graph_state_projects_known_assets(tmp_path, monkeypatch)` |
| `test_report_resolves_technique_from_vulnclass` | function | `tests/test_loop_intel_projection.py:32` | `def test_report_resolves_technique_from_vulnclass(tmp_path, monkeypatch)` |
| `test_writeback_finding_has_concrete_class_and_name` | function | `tests/test_loop_intel_projection.py:73` | `def test_writeback_finding_has_concrete_class_and_name(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_intent_delete.py:8` | `def _patched_engine(tmp_path, monkeypatch)` |
| `test_hard_delete_removes_exclusive_keeps_shared` | function | `tests/test_loop_intent_delete.py:46` | `def test_hard_delete_removes_exclusive_keeps_shared(tmp_path, monkeypatch)` |
| `test_soft_delete_keeps_outputs_and_notifies` | function | `tests/test_loop_intent_delete.py:17` | `def test_soft_delete_keeps_outputs_and_notifies(tmp_path, monkeypatch)` |
| `test_soft_delete_requires_reason` | function | `tests/test_loop_intent_delete.py:37` | `def test_soft_delete_requires_reason(tmp_path, monkeypatch)` |
| `_patch_model` | function | `tests/test_loop_lazymode_first.py:53` | `def _patch_model(monkeypatch, loop, reply, run_result)` |
| `_result` | function | `tests/test_loop_lazymode_first.py:18` | `def _result(ok, result, stdout, error, duration)` |
| `test_codemode_disabled_is_noop` | function | `tests/test_loop_lazymode_first.py:114` | `def test_codemode_disabled_is_noop(worker_env, monkeypatch)` |
| `test_codemode_exploit_without_shell_falls_through` | function | `tests/test_loop_lazymode_first.py:82` | `def test_codemode_exploit_without_shell_falls_through(worker_env, monkeypatch)` |
| `test_codemode_no_script_falls_through` | function | `tests/test_loop_lazymode_first.py:97` | `def test_codemode_no_script_falls_through(worker_env, monkeypatch)` |
| `test_codemode_recon_owns_on_content` | function | `tests/test_loop_lazymode_first.py:129` | `def test_codemode_recon_owns_on_content(worker_env, monkeypatch)` |
| `test_codemode_shell_wins_and_skips_agent` | function | `tests/test_loop_lazymode_first.py:61` | `def test_codemode_shell_wins_and_skips_agent(worker_env, monkeypatch)` |
| `test_execute_tries_codemode_before_agentic` | function | `tests/test_loop_lazymode_first.py:149` | `def test_execute_tries_codemode_before_agentic(worker_env, monkeypatch)` |
| `worker_env` | function | `tests/test_loop_lazymode_first.py:24` | `def worker_env(tmp_path, monkeypatch)` |
| `claim` | function | `tests/test_loop_leases.py:98` | `def claim(target)` |
| `store` | function | `tests/test_loop_leases.py:13` | `def store(tmp_path)` |
| `test_active_and_counts` | function | `tests/test_loop_leases.py:69` | `def test_active_and_counts(store)` |
| `test_cross_process_claim_via_second_connection` | function | `tests/test_loop_leases.py:86` | `def test_cross_process_claim_via_second_connection(tmp_path)` |
| `test_expired_claim_freed_by_sweep` | function | `tests/test_loop_leases.py:45` | `def test_expired_claim_freed_by_sweep(store)` |
| `test_expired_lease_reclaimable` | function | `tests/test_loop_leases.py:37` | `def test_expired_lease_reclaimable(store)` |
| `test_first_claim_wins` | function | `tests/test_loop_leases.py:18` | `def test_first_claim_wins(store)` |
| `test_heartbeat_extends_live_lease_only` | function | `tests/test_loop_leases.py:53` | `def test_heartbeat_extends_live_lease_only(store)` |
| `test_independent_tasks_do_not_collide` | function | `tests/test_loop_leases.py:81` | `def test_independent_tasks_do_not_collide(store)` |
| `test_release_makes_intent_claimable` | function | `tests/test_loop_leases.py:61` | `def test_release_makes_intent_claimable(store)` |
| `test_second_claim_while_held_fails` | function | `tests/test_loop_leases.py:25` | `def test_second_claim_while_held_fails(store)` |
| `test_settled_intent_never_reclaims` | function | `tests/test_loop_leases.py:30` | `def test_settled_intent_never_reclaims(store)` |
| `test_threads_do_not_share_connection_state` | function | `tests/test_loop_leases.py:95` | `def test_threads_do_not_share_connection_state(store)` |
| `graph` | function | `tests/test_loop_leases_integration.py:11` | `def graph(tmp_path, monkeypatch)` |
| `test_budget_check_includes_token_verdict` | function | `tests/test_loop_leases_integration.py:58` | `def test_budget_check_includes_token_verdict(tmp_path, monkeypatch)` |
| `test_claim_acquires_lease` | function | `tests/test_loop_leases_integration.py:25` | `def test_claim_acquires_lease(graph)` |
| `test_lease_store_disabled` | function | `tests/test_loop_leases_integration.py:74` | `def test_lease_store_disabled(monkeypatch)` |
| `test_requeue_releases_lease` | function | `tests/test_loop_leases_integration.py:49` | `def test_requeue_releases_lease(graph)` |
| `test_second_claim_blocked_by_lease` | function | `tests/test_loop_leases_integration.py:33` | `def test_second_claim_blocked_by_lease(graph)` |
| `test_settle_on_exhausted_blocks_reclaim` | function | `tests/test_loop_leases_integration.py:40` | `def test_settle_on_exhausted_blocks_reclaim(graph)` |
| `test_token_guard_fail_soft` | function | `tests/test_loop_leases_integration.py:67` | `def test_token_guard_fail_soft(tmp_path, monkeypatch)` |
| `_patched_engine` | function | `tests/test_loop_llm_resilience.py:6` | `def _patched_engine(tmp_path, monkeypatch)` |
| `error_then_ok` | function | `tests/test_loop_llm_resilience.py:61` | `def error_then_ok(model, prompt, max_tokens)` |
| `first_empty_then_ok` | function | `tests/test_loop_llm_resilience.py:42` | `def first_empty_then_ok(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:23` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:79` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:147` | `def scripted(model, prompt, max_tokens)` |
| `scripted` | function | `tests/test_loop_llm_resilience.py:236` | `def scripted(model, prompt, max_tokens)` |
| `scripted_next` | function | `tests/test_loop_llm_resilience.py:160` | `def scripted_next(model, prompt, max_tokens)` |
| `test_empty_budget_exhausted_moves_to_next_member` | function | `tests/test_loop_llm_resilience.py:34` | `def test_empty_budget_exhausted_moves_to_next_member(tmp_path, monkeypatch)` |
| `test_empty_reply_replays_before_failover` | function | `tests/test_loop_llm_resilience.py:15` | `def test_empty_reply_replays_before_failover(tmp_path, monkeypatch)` |
| `test_error_reply_fails_over_instead_of_becoming_content` | function | `tests/test_loop_llm_resilience.py:54` | `def test_error_reply_fails_over_instead_of_becoming_content(tmp_path, monkeypatch)` |
| `test_llm_context_budget_roundtrip` | function | `tests/test_loop_llm_resilience.py:213` | `def test_llm_context_budget_roundtrip(tmp_path, monkeypatch)` |
| `test_planner_uses_bound_task_chain` | function | `tests/test_loop_llm_resilience.py:225` | `def test_planner_uses_bound_task_chain(tmp_path, monkeypatch)` |
| `test_raw_llm_recording_carries_task_and_model` | function | `tests/test_loop_llm_resilience.py:190` | `def test_raw_llm_recording_carries_task_and_model(tmp_path, monkeypatch)` |
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

Next: [SYMBOLS_p48.md](SYMBOLS_p48.md)
