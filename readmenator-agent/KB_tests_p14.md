# Subsystem: tests (page 14 of 21)
Previous: [KB_tests_p13.md](KB_tests_p13.md)

## tests/test_llm_orchestrator.py
- Doc: SDD spec and BDD scenarios for the orchestrator-governed LLM failover chain.
- Layer: testing
- Language: py
- Symbols:
  - `_StubHealth` (class, line 40) `class _StubHealth`
  - `_scripted_executor` (function, line 58) `def _scripted_executor(script, calls)`
  - `_member` (function, line 70) `def _member(name, model, priority)`
  - `isolated_pool` (function, line 75) `def isolated_pool(tmp_path, monkeypatch)`
  - `TestChainOrder` (class, line 82) `class TestChainOrder`
  - `TestFailover` (class, line 133) `class TestFailover`
  - `TestHealth` (class, line 334) `class TestHealth`
  - `_RecordingRegistry` (class, line 413) `class _RecordingRegistry`
  - `TestLedger` (class, line 429) `class TestLedger`
  - `TestBackendKind` (class, line 461) `class TestBackendKind`
  - `TestAdapterWiring` (class, line 479) `class TestAdapterWiring`
  - `TestC2Wiring` (class, line 656) `class TestC2Wiring`
  - `TestErrorDetection` (class, line 677) `class TestErrorDetection`
  - `TestPlaceholderKeys` (class, line 799) `class TestPlaceholderKeys`
  - `TestGroqEnvKey` (class, line 864) `class TestGroqEnvKey`
  - `TestAiFallbackIntegration` (class, line 903) `class TestAiFallbackIntegration`
  - `lazyc2_source` (function, line 974) `def lazyc2_source()`
  - `test_orchestrator_module_exports_public_api` (function, line 982) `def test_orchestrator_module_exports_public_api()`
  - `__init__` (method, line 43) `def __init__(self, parked)`
  - `healthy` (method, line 48) `def healthy(self, name)`
  - `report_failure` (method, line 51) `def report_failure(self, name, error)`
  - `report_success` (method, line 54) `def report_success(self, name)`
  - `_execute` (function, line 59) `def _execute(model_spec, prompt, max_tokens)`
  - `test_weights_sort_members_by_descending_priority` (method, line 83) `def test_weights_sort_members_by_descending_priority(self)`
  - `test_sort_members_never_mutates_input` (method, line 94) `def test_sort_members_never_mutates_input(self)`
  - `test_pool_chain_reads_lazy_orchestrator_store` (method, line 100) `def test_pool_chain_reads_lazy_orchestrator_store(self, isolated_pool)`
  - `test_pool_chain_self_heals_corrupt_store` (method, line 113) `def test_pool_chain_self_heals_corrupt_store(self, isolated_pool)`
  - `test_pool_chain_returns_empty_when_pool_unreadable` (method, line 121) `def test_pool_chain_returns_empty_when_pool_unreadable(self, monkeypatch)`
  - `test_primary_success_needs_no_fallback` (method, line 134) `def test_primary_success_needs_no_fallback(self)`
  - `test_primary_failure_serves_fallback_with_notice` (method, line 155) `def test_primary_failure_serves_fallback_with_notice(self)`
  - `test_all_members_fail_returns_error_result_without_raising` (method, line 181) `def test_all_members_fail_returns_error_result_without_raising(self)`
  - `test_error_banner_text_is_a_failure_not_content` (method, line 198) `def test_error_banner_text_is_a_failure_not_content(self)`
  - `test_blank_reply_is_a_failure` (method, line 217) `def test_blank_reply_is_a_failure(self)`
  - `test_quota_wording_reply_is_a_failure` (method, line 230) `def test_quota_wording_reply_is_a_failure(self)`
  - `test_empty_prompt_short_circuits` (method, line 243) `def test_empty_prompt_short_circuits(self)`
  - `test_system_prompt_is_prepended_for_the_executor` (method, line 258) `def test_system_prompt_is_prepended_for_the_executor(self)`
  - `test_max_tokens_is_forwarded` (method, line 278) `def test_max_tokens_is_forwarded(self)`
  - `test_chain_uses_orchestrator_pool_when_no_override` (method, line 297) `def test_chain_uses_orchestrator_pool_when_no_override(self, isolated_pool)`
  - `test_dedupes_members_by_name` (method, line 318) `def test_dedupes_members_by_name(self)`
  - `test_unhealthy_member_is_skipped_while_others_remain` (method, line 335) `def test_unhealthy_member_is_skipped_while_others_remain(self)`
  - `test_all_unhealthy_members_still_get_attempted` (method, line 352) `def test_all_unhealthy_members_still_get_attempted(self)`
  - `test_success_reports_health` (method, line 367) `def test_success_reports_health(self)`
  - `test_failure_reports_health` (method, line 381) `def test_failure_reports_health(self)`
  - `test_default_health_comes_from_shared_registry` (method, line 395) `def test_default_health_comes_from_shared_registry(self, isolated_pool, monkeypatch)`
  - `__init__` (method, line 416) `def __init__(self, seen)`
  - `healthy` (method, line 419) `def healthy(self, name)`
  - `report_failure` (method, line 422) `def report_failure(self, name, error)`
  - `report_success` (method, line 425) `def report_success(self, name)`
  - `test_success_is_recorded_in_the_pool_ledger` (method, line 430) `def test_success_is_recorded_in_the_pool_ledger(self, isolated_pool)`
  - `test_failure_is_recorded_in_the_pool_ledger` (method, line 445) `def test_failure_is_recorded_in_the_pool_ledger(self, isolated_pool)`
  - `test_backend_kind_parses_spec_prefix` (method, line 473) `def test_backend_kind_parses_spec_prefix(self, spec, kind)`
  - `cfg` (method, line 481) `def cfg(self, tmp_path)`
  - `patched` (method, line 493) `def patched(self, cfg, monkeypatch)`
  - `test_missing_client_serves_from_the_chain` (method, line 499) `def test_missing_client_serves_from_the_chain(self, patched, monkeypatch)`
  - `test_missing_client_returns_legacy_error_when_chain_exhausted` (method, line 515) `def test_missing_client_returns_legacy_error_when_chain_exhausted(self, patched, monkeypatch)`
  - `test_client_error_falls_back_to_the_chain` (method, line 522) `def test_client_error_falls_back_to_the_chain(self, patched, monkeypatch)`
  - `test_client_success_stays_primary_without_chain_call` (method, line 548) `def test_client_success_stays_primary_without_chain_call(self, patched, monkeypatch)`
  - `test_client_401_error_string_falls_back_to_the_chain` (method, line 570) `def test_client_401_error_string_falls_back_to_the_chain(self, patched, monkeypatch)`
  - `test_client_401_keeps_legacy_error_when_chain_exhausted` (method, line 595) `def test_client_401_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch)`
  - `test_fallback_answer_is_memorized_clean` (method, line 611) `def test_fallback_answer_is_memorized_clean(self, patched, monkeypatch, tmp_path)`
  - `test_ask_general_serves_from_the_chain_when_backend_missing` (method, line 627) `def test_ask_general_serves_from_the_chain_when_backend_missing(self, patched, monkeypatch)`
  - `test_ask_general_keeps_legacy_error_when_chain_exhausted` (method, line 645) `def test_ask_general_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch)`
  - `test_analyze_functions_route_through_the_orchestrator` (method, line 657) `def test_analyze_functions_route_through_the_orchestrator(self)`
  - `test_ai_fallback_call_routes_through_the_chain` (method, line 667) `def test_ai_fallback_call_routes_through_the_chain(self)`
  - `test_error_replies_detected` (method, line 690) `def test_error_replies_detected(self, reply)`
  - `test_real_answer_not_treated_as_error` (method, line 695) `def test_real_answer_not_treated_as_error(self)`
  - `test_pentest_prose_with_unauthorized_word_is_content` (method, line 700) `def test_pentest_prose_with_unauthorized_word_is_content(self)`
  - `test_phishing_prose_with_credit_word_is_content` (method, line 706) `def test_phishing_prose_with_credit_word_is_content(self)`
  - `test_long_pentest_plan_is_served_not_failed_over` (method, line 712) `def test_long_pentest_plan_is_served_not_failed_over(self)`
  - `test_invalid_api_key_reply_is_a_failure` (method, line 733) `def test_invalid_api_key_reply_is_a_failure(self)`
  - `test_placeholder_groq_leg_refused_without_doomed_call` (method, line 754) `def test_placeholder_groq_leg_refused_without_doomed_call(self, monkeypatch)`
  - `test_placeholder_groq_leg_refused_even_with_payload_key` (method, line 780) `def test_placeholder_groq_leg_refused_even_with_payload_key(self, monkeypatch)`
  - `test_placeholder_fragments_recognized` (method, line 800) `def test_placeholder_fragments_recognized(self)`
  - `test_real_key_not_a_placeholder` (method, line 806) `def test_real_key_not_a_placeholder(self)`
  - `test_factory_rejects_placeholder_payload_key` (method, line 810) `def test_factory_rejects_placeholder_payload_key(self)`
  - `test_factory_rejects_placeholder_env_key` (method, line 819) `def test_factory_rejects_placeholder_env_key(self, monkeypatch)`
  - `test_placeholder_env_replaced_by_payload_key` (method, line 827) `def test_placeholder_env_replaced_by_payload_key(self, monkeypatch)`
  - `test_placeholder_env_survives_without_payload_key` (method, line 845) `def test_placeholder_env_survives_without_payload_key(self, monkeypatch)`
  - `test_explicit_api_key_published_to_environment` (method, line 865) `def test_explicit_api_key_published_to_environment(self, monkeypatch)`
  - `test_placeholder_payload_key_not_published` (method, line 884) `def test_placeholder_payload_key_not_published(self, monkeypatch)`
  - `test_orchestrator_success_maps_to_ai_result` (method, line 904) `def test_orchestrator_success_maps_to_ai_result(self, monkeypatch)`
  - `test_orchestrator_success_after_failure_carries_notice` (method, line 925) `def test_orchestrator_success_after_failure_carries_notice(self, monkeypatch)`
  - `test_exhausted_chain_degrades_to_local_ollama` (method, line 947) `def test_exhausted_chain_degrades_to_local_ollama(self, monkeypatch)`
  - `test_total_failure_returns_help_message` (method, line 961) `def test_total_failure_returns_help_message(self, monkeypatch)`
  - `_explode` (function, line 126) `def _explode()`
  - `executor` (function, line 263) `def executor(model_spec, prompt, max_tokens)`
  - `executor` (function, line 283) `def executor(model_spec, prompt, max_tokens)`
  - `_spy` (function, line 764) `def _spy(model_spec, prompt, max_tokens)`
- Depends on: `modules/__init__.py`, `modules/ai_fallback.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/llm_adapter.py`, `modules/llm_factory.py`, `modules/llm_orchestrator.py`, `modules/llm_pool.py`, `modules/llm_prompts.py`

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

## tests/test_loop_guardrails.py
- Doc: Loop guardrails: repetition detection, EDR pacing, target caps, vector fact memory.
- Layer: testing
- Language: py
- Symbols:
  - `test_repeat_detector_flags_identical_window` (function, line 12) `def test_repeat_detector_flags_identical_window()`
  - `test_repeat_detector_recovery_on_variation` (function, line 21) `def test_repeat_detector_recovery_on_variation()`
  - `test_edr_pacer_slow_scan_raises_level` (function, line 35) `def test_edr_pacer_slow_scan_raises_level()`
  - `test_edr_pacer_connection_reset_raises_and_decays` (function, line 47) `def test_edr_pacer_connection_reset_raises_and_decays()`
  - `test_edr_pacer_calm_level_returns_command_unchanged` (function, line 59) `def test_edr_pacer_calm_level_returns_command_unchanged()`
  - `test_target_limiter_caps_concurrency` (function, line 67) `def test_target_limiter_caps_concurrency()`
  - `test_target_limiter_is_reentrant_per_thread` (function, line 93) `def test_target_limiter_is_reentrant_per_thread()`
  - `test_target_limiter_empty_target_bypasses` (function, line 112) `def test_target_limiter_empty_target_bypasses()`
  - `test_fact_vector_store_roundtrip_and_search` (function, line 121) `def test_fact_vector_store_roundtrip_and_search(tmp_path)`
  - `test_fact_vector_store_search_block_rendering` (function, line 141) `def test_fact_vector_store_search_block_rendering(tmp_path)`
  - `_work` (function, line 75) `def _work()`
  - `_work` (function, line 99) `def _work()`
- Depends on: `modules/loop_guardrails.py`

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

## tests/test_loop_manager.py
- Doc: Tests for modules.loop_manager — safe autonomous loop orchestration.
- Layer: testing
- Language: py
- Symbols:
  - `loops_dir` (function, line 37) `def loops_dir()`
  - `stub_script` (function, line 43) `def stub_script(tmp_path)`
  - `manager` (function, line 56) `def manager(loops_dir, stub_script)`
  - `TestValidateTarget` (class, line 64) `class TestValidateTarget`
  - `TestSanitizeGoal` (class, line 95) `class TestSanitizeGoal`
  - `TestClampInt` (class, line 123) `class TestClampInt`
  - `TestValidateLoopId` (class, line 138) `class TestValidateLoopId`
  - `TestSpawnAndRegistry` (class, line 151) `class TestSpawnAndRegistry`
  - `TestLogReading` (class, line 222) `class TestLogReading`
  - `TestStop` (class, line 251) `class TestStop`
  - `TestLifecycle` (class, line 281) `class TestLifecycle`
  - `test_accepts_ipv4` (method, line 65) `def test_accepts_ipv4(self)`
  - `test_accepts_ipv6` (method, line 68) `def test_accepts_ipv6(self)`
  - `test_strips_whitespace` (method, line 71) `def test_strips_whitespace(self)`
  - `test_rejects_hostname` (method, line 74) `def test_rejects_hostname(self)`
  - `test_rejects_command_injection` (method, line 78) `def test_rejects_command_injection(self)`
  - `test_rejects_metacharacters` (method, line 82) `def test_rejects_metacharacters(self)`
  - `test_rejects_non_string` (method, line 86) `def test_rejects_non_string(self)`
  - `test_rejects_empty` (method, line 90) `def test_rejects_empty(self)`
  - `test_defaults_on_empty` (method, line 96) `def test_defaults_on_empty(self)`
  - `test_collapses_whitespace` (method, line 100) `def test_collapses_whitespace(self)`
  - `test_rejects_newlines` (method, line 103) `def test_rejects_newlines(self)`
  - `test_rejects_quotes` (method, line 107) `def test_rejects_quotes(self)`
  - `test_rejects_semicolons` (method, line 111) `def test_rejects_semicolons(self)`
  - `test_rejects_too_long` (method, line 115) `def test_rejects_too_long(self)`
  - `test_accepts_plain_words` (method, line 119) `def test_accepts_plain_words(self)`
  - `test_default_on_none` (method, line 124) `def test_default_on_none(self)`
  - `test_clamps_low` (method, line 127) `def test_clamps_low(self)`
  - `test_clamps_high` (method, line 130) `def test_clamps_high(self)`
  - `test_rejects_non_numeric` (method, line 133) `def test_rejects_non_numeric(self)`
  - `test_accepts_hex32` (method, line 139) `def test_accepts_hex32(self)`
  - `test_rejects_traversal` (method, line 142) `def test_rejects_traversal(self)`
  - `test_rejects_non_hex` (method, line 146) `def test_rejects_non_hex(self)`
  - `test_start_spawns_and_records` (method, line 152) `def test_start_spawns_and_records(self, manager, loops_dir)`
  - `test_argv_has_no_shell` (method, line 164) `def test_argv_has_no_shell(self, manager)`
  - `test_invalid_kind_rejected` (method, line 179) `def test_invalid_kind_rejected(self, manager)`
  - `test_invalid_target_rejected` (method, line 183) `def test_invalid_target_rejected(self, manager)`
  - `test_concurrency_cap` (method, line 187) `def test_concurrency_cap(self, manager)`
  - `test_list_loops_sorted_newest_first` (method, line 195) `def test_list_loops_sorted_newest_first(self, manager)`
  - `test_registry_survives_restart` (method, line 205) `def test_registry_survives_restart(self, manager, loops_dir)`
  - `test_metadata_written` (method, line 212) `def test_metadata_written(self, manager, loops_dir)`
  - `test_read_log_chunk` (method, line 223) `def test_read_log_chunk(self, manager, loops_dir)`
  - `test_read_log_unknown_loop` (method, line 231) `def test_read_log_unknown_loop(self, manager)`
  - `test_read_log_confinement` (method, line 235) `def test_read_log_confinement(self, manager, loops_dir)`
  - `test_read_log_offset_beyond_size` (method, line 243) `def test_read_log_offset_beyond_size(self, manager)`
  - `test_stop_terminates_process` (method, line 252) `def test_stop_terminates_process(self, manager)`
  - `test_stop_unknown_loop` (method, line 264) `def test_stop_unknown_loop(self, manager)`
  - `test_stop_finished_loop_rejected` (method, line 268) `def test_stop_finished_loop_rejected(self, manager)`
  - `test_quick_exit_marks_finished` (method, line 282) `def test_quick_exit_marks_finished(self, loops_dir, tmp_path)`
  - `test_sigterm_resistant_process_is_killed` (method, line 297) `def test_sigterm_resistant_process_is_killed(self, loops_dir, tmp_path)`
  - `test_summary_shape` (method, line 314) `def test_summary_shape(self, manager)`
- Depends on: `modules/loop_manager.py`

## tests/test_loop_mentions.py
- Doc: Lazy mentions multi-type search and scroll pagination.
- Layer: testing
- Language: py
- Symbols:
  - `test_mentions_search_and_cursor` (function, line 6) `def test_mentions_search_and_cursor(tmp_path, monkeypatch)`
  - `test_mentions_parse_caps_and_trusts_ids` (function, line 16) `def test_mentions_parse_caps_and_trusts_ids()`
- Depends on: `modules/__init__.py`

## tests/test_loop_multi_target.py
- Doc: Multi-target loop entry: scope-file parsing, validation and caps.
- Layer: testing
- Language: py
- Symbols:
  - `test_parse_loop_line_accepts_targets_file` (function, line 10) `def test_parse_loop_line_accepts_targets_file(tmp_path)`
  - `test_parse_loop_line_defaults_without_file` (function, line 20) `def test_parse_loop_line_defaults_without_file()`
  - `test_load_targets_file_skips_comments_and_invalid` (function, line 27) `def test_load_targets_file_skips_comments_and_invalid(tmp_path)`
  - `test_load_targets_file_caps_batch` (function, line 38) `def test_load_targets_file_caps_batch(tmp_path)`
  - `test_load_targets_file_missing_raises` (function, line 46) `def test_load_targets_file_missing_raises(tmp_path)`
  - `test_load_targets_file_empty_raises` (function, line 52) `def test_load_targets_file_empty_raises(tmp_path)`
- Depends on: `modules/lazy_runner.py`

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


Next: [KB_tests_p15.md](KB_tests_p15.md)
