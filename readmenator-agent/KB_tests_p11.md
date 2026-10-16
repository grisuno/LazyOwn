# Subsystem: tests (page 11 of 17)
Previous: [KB_tests_p10.md](KB_tests_p10.md)

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

## tests/test_loop_progress.py
- Doc: Loop milestone panel: inferred stage states stay honest.
- Layer: testing
- Language: py
- Symbols:
  - `_overview` (function, line 20) `def _overview()`
  - `test_chain_has_fourteen_stages` (function, line 28) `def test_chain_has_fourteen_stages()`
  - `test_fresh_task_shows_first_stage_current` (function, line 34) `def test_fresh_task_shows_first_stage_current()`
  - `test_progress_advances_with_evidence` (function, line 44) `def test_progress_advances_with_evidence()`
  - `test_finished_task_all_green` (function, line 58) `def test_finished_task_all_green()`
  - `test_snapshot_counts_intent_states` (function, line 69) `def test_snapshot_counts_intent_states()`
  - `test_panel_renders_without_live` (function, line 79) `def test_panel_renders_without_live()`
  - `test_render_contains_no_markup_strings` (function, line 88) `def test_render_contains_no_markup_strings()`
  - `test_line_mode_prints_only_on_stage_change` (function, line 104) `def test_line_mode_prints_only_on_stage_change(capsys)`
  - `test_sanitize_line_strips_ansi_and_cr` (function, line 126) `def test_sanitize_line_strips_ansi_and_cr()`
  - `test_sanitize_line_keeps_ansi_when_asked` (function, line 134) `def test_sanitize_line_keeps_ansi_when_asked()`
- Depends on: `core/console.py`, `modules/loop_progress.py`

## tests/test_loop_scope_traffic_evidence.py
- Doc: Scope ownership, port-aware traffic search, role-based evidences (lazy parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_scope_covers_by_ownership_not_substring` (function, line 15) `def test_scope_covers_by_ownership_not_substring(tmp_path, monkeypatch)`
  - `test_scope_cidr_covers_url_embedded_ip` (function, line 29) `def test_scope_cidr_covers_url_embedded_ip(tmp_path, monkeypatch)`
  - `test_scope_ip_covers_any_port_url` (function, line 41) `def test_scope_ip_covers_any_port_url(tmp_path, monkeypatch)`
  - `test_worker_scope_enforcement_cidr` (function, line 54) `def test_worker_scope_enforcement_cidr(tmp_path, monkeypatch)`
  - `test_traffic_search_host_port_aware` (function, line 71) `def test_traffic_search_host_port_aware(tmp_path, monkeypatch)`
  - `test_finding_evidence_roles_notes_order` (function, line 88) `def test_finding_evidence_roles_notes_order(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_spawn_side.py
- Doc: Multi-session chat, persistent side questions, spawn inheritance (lazy 0.3.9).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `test_chat_sessions_stay_independent` (function, line 15) `def test_chat_sessions_stay_independent(tmp_path, monkeypatch)`
  - `test_side_questions_persist_and_recall` (function, line 36) `def test_side_questions_persist_and_recall(tmp_path, monkeypatch)`
  - `test_spawn_inherits_scope_and_findings_read_only` (function, line 53) `def test_spawn_inherits_scope_and_findings_read_only(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_loop_store_race.py
- Doc: Store file writes stay atomic under parallel workers (race regression).
- Layer: testing
- Language: py
- Symbols:
  - `test_save_json_survives_parallel_writers` (function, line 8) `def test_save_json_survives_parallel_writers(tmp_path, monkeypatch)`
  - `writer` (function, line 16) `def writer(worker)`
- Depends on: `modules/lazy_loop.py`

## tests/test_loop_supervision.py
- Doc: Supervision upgrades: repetition watchdog, stack priors, prompt masking.
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `_isolate_intel` (function, line 16) `def _isolate_intel(tmp_path, monkeypatch)`
  - `_DeadPool` (class, line 25) `class _DeadPool`
  - `_kill_llm` (function, line 37) `def _kill_llm(monkeypatch)`
  - `test_repetition_watchdog_settles` (function, line 46) `def test_repetition_watchdog_settles(tmp_path, monkeypatch)`
  - `test_stack_priors_prefer_same_stack` (function, line 75) `def test_stack_priors_prefer_same_stack(tmp_path, monkeypatch)`
  - `test_prompt_context_masks_configured_only` (function, line 99) `def test_prompt_context_masks_configured_only(tmp_path, monkeypatch)`
  - `members` (method, line 28) `def members(self)`
  - `complete` (method, line 32) `def complete(self)`
- Depends on: `core/config.py`, `modules/lazy_engine.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`

## tests/test_loop_worker_traces.py
- Doc: Worker cross-work trace tools (lazy 0.3.10 parity).
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 6) `def _patched_engine(tmp_path, monkeypatch)`
  - `_seed_two_works` (function, line 15) `def _seed_two_works(engine, task_id)`
  - `test_search_all_spans_works_without_intent` (function, line 27) `def test_search_all_spans_works_without_intent(tmp_path, monkeypatch)`
  - `test_trace_steps_and_single_step` (function, line 40) `def test_trace_steps_and_single_step(tmp_path, monkeypatch)`
  - `test_worker_lane_binds_node_detail` (function, line 57) `def test_worker_lane_binds_node_detail(tmp_path, monkeypatch)`
  - `test_add_hint_emits_explicit_planner_trigger` (function, line 65) `def test_add_hint_emits_explicit_planner_trigger(tmp_path, monkeypatch)`
  - `test_worker_bash_unbound_blocks_without_execution` (function, line 81) `def test_worker_bash_unbound_blocks_without_execution(tmp_path, monkeypatch)`
  - `test_planner_intent_unbound_emits_nothing` (function, line 100) `def test_planner_intent_unbound_emits_nothing(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_mcp_dispatch.py
- Doc: call_tool dispatches through the handler registry.
- Layer: testing
- Language: py
- Symbols:
  - `_registered` (function, line 23) `def _registered()`
  - `_fallback_branches` (function, line 40) `def _fallback_branches()`
  - `TestRegistryDispatch` (class, line 51) `class TestRegistryDispatch`
  - `test_set_config_refuses_null_values` (function, line 67) `def test_set_config_refuses_null_values()`
  - `test_new_chain_shell_tools_have_defs_and_handlers` (function, line 82) `def test_new_chain_shell_tools_have_defs_and_handlers()`
  - `test_opencode_bridge_curates_loop_and_chain` (function, line 92) `def test_opencode_bridge_curates_loop_and_chain()`
  - `test_mcp_never_offers_interactive_repl` (function, line 107) `def test_mcp_never_offers_interactive_repl()`
  - `test_no_dead_duplicate_branches` (method, line 52) `def test_no_dead_duplicate_branches(self)`
  - `test_migrated_handlers_registered` (method, line 56) `def test_migrated_handlers_registered(self)`
  - `test_migrated_handlers_absent_from_fallback` (method, line 61) `def test_migrated_handlers_absent_from_fallback(self)`

## tests/test_mcp_improvements.py
- Doc: Tests for the high/medium/low impact MCP improvements.
- Layer: testing
- Language: py
- Symbols:
  - `test_is_likely_credential_classifies` (function, line 74) `def test_is_likely_credential_classifies(value, expect_real, expect_reason)`
  - `test_is_likely_credential_handles_non_string` (function, line 84) `def test_is_likely_credential_handles_non_string()`
  - `test_parse_task_value_complete` (function, line 92) `def test_parse_task_value_complete()`
  - `test_parse_task_value_truncated` (function, line 103) `def test_parse_task_value_truncated()`
  - `test_parse_task_value_no_payload` (function, line 110) `def test_parse_task_value_no_payload()`
  - `test_audit_tasks_drops_timestamps_and_urls` (function, line 117) `def test_audit_tasks_drops_timestamps_and_urls()`
  - `test_audit_tasks_respects_min_confidence` (function, line 141) `def test_audit_tasks_respects_min_confidence()`
  - `test_evidence_freshness_missing` (function, line 154) `def test_evidence_freshness_missing(tmp_path)`
  - `test_evidence_freshness_fresh` (function, line 160) `def test_evidence_freshness_fresh(tmp_path)`
  - `test_evidence_freshness_stale` (function, line 170) `def test_evidence_freshness_stale(tmp_path)`
  - `_seed_sessions` (function, line 182) `def _seed_sessions(tmp_path)`
  - `test_build_target_context_filters_by_port` (function, line 195) `def test_build_target_context_filters_by_port(tmp_path)`
  - `test_build_target_context_no_port_returns_all` (function, line 218) `def test_build_target_context_no_port_returns_all(tmp_path)`
  - `test_evidence_grep_finds_in_loot_scope` (function, line 227) `def test_evidence_grep_finds_in_loot_scope(tmp_path)`
  - `test_evidence_grep_invalid_regex` (function, line 237) `def test_evidence_grep_invalid_regex(tmp_path)`
  - `test_evidence_grep_truncates` (function, line 244) `def test_evidence_grep_truncates(tmp_path)`
  - `test_preflight_detects_duplicate` (function, line 256) `def test_preflight_detects_duplicate(tmp_path)`
  - `test_preflight_flags_missing_payload_keys` (function, line 270) `def test_preflight_flags_missing_payload_keys(tmp_path)`
  - `test_preflight_os_mismatch` (function, line 281) `def test_preflight_os_mismatch(tmp_path)`
  - `test_jobstore_runs_command_and_reports_done` (function, line 297) `def test_jobstore_runs_command_and_reports_done()`
  - `test_jobstore_captures_failure` (function, line 317) `def test_jobstore_captures_failure()`
  - `test_jobstore_unknown_id` (function, line 335) `def test_jobstore_unknown_id()`
  - `test_jobstore_list_orders_newest_first` (function, line 340) `def test_jobstore_list_orders_newest_first()`
  - `test_diff_first_run_reports_first_run` (function, line 353) `def test_diff_first_run_reports_first_run(tmp_path)`
  - `test_diff_picks_up_changes` (function, line 360) `def test_diff_picks_up_changes(tmp_path)`
  - `test_confirmation_required_for_destructive_command` (function, line 380) `def test_confirmation_required_for_destructive_command()`
  - `test_confirmation_skipped_for_benign` (function, line 385) `def test_confirmation_skipped_for_benign()`
  - `test_confirmation_required_for_destructive_tools` (function, line 389) `def test_confirmation_required_for_destructive_tools()`
  - `_fresh_mcp_module` (function, line 397) `def _fresh_mcp_module(tmp_path)`
  - `test_handler_target_context_via_helper` (function, line 414) `def test_handler_target_context_via_helper(tmp_path)`
  - `test_handler_tasks_cleanup_dry_run` (function, line 421) `def test_handler_tasks_cleanup_dry_run(tmp_path)`
  - `test_evidence_grep_handler_ignores_binaries` (function, line 436) `def test_evidence_grep_handler_ignores_binaries(tmp_path)`
  - `runner` (function, line 300) `def runner(cmd, timeout)`
  - `runner` (function, line 320) `def runner(cmd, timeout)`
- Depends on: `skills/lazyown_mcp.py`, `skills/lazyown_mcp_helpers.py`

## tests/test_mcp_lazy.py
- Doc: Contract for the unified MCP lazy-import helper.
- Layer: testing
- Language: py
- Symbols:
  - `TestEnsureOptional` (class, line 42) `class TestEnsureOptional`
  - `TestWrappersDelegate` (class, line 86) `class TestWrappersDelegate`
  - `test_success_binds_and_caches` (method, line 43) `def test_success_binds_and_caches(self)`
  - `test_cached_value_returned_untouched` (method, line 58) `def test_cached_value_returned_untouched(self)`
  - `test_exception_fails_closed` (method, line 66) `def test_exception_fails_closed(self)`
  - `test_false_loader_with_fallback` (method, line 75) `def test_false_loader_with_fallback(self)`
  - `test_all_wrappers_delegate_to_helper` (method, line 87) `def test_all_wrappers_delegate_to_helper(self)`
  - `loader` (function, line 47) `def loader(ns)`
  - `loader` (function, line 61) `def loader(ns)`
  - `loader` (function, line 69) `def loader(ns)`
  - `loader` (function, line 78) `def loader(ns)`
- Depends on: `skills/mcp_lazy.py`

## tests/test_mcp_recommender_embed.py
- Doc: Contract tests for the MCP sitrep recommender embedding.
- Layer: testing
- Language: py
- Symbols:
  - `_load_mcp_module` (function, line 15) `def _load_mcp_module()`
  - `test_maps_recommender_fields` (function, line 25) `def test_maps_recommender_fields(monkeypatch)`
  - `test_never_forwards_positional_arguments` (function, line 44) `def test_never_forwards_positional_arguments(monkeypatch)`
  - `test_returns_error_entry_on_failure` (function, line 59) `def test_returns_error_entry_on_failure(monkeypatch)`
  - `test_reports_unavailable_recommender` (function, line 71) `def test_reports_unavailable_recommender(monkeypatch)`
  - `test_limits_suggestions` (function, line 81) `def test_limits_suggestions(monkeypatch)`
  - `fake_recommend` (function, line 48) `def fake_recommend()`
  - `explode` (function, line 62) `def explode()`


Next: [KB_tests_p12.md](KB_tests_p12.md)
