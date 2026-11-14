# Symbols (page 46 of 52)
Previous: [SYMBOLS_p45.md](SYMBOLS_p45.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `_ExitShell` | class | `tests/test_loop_exit_gate.py:92` | `class _ExitShell` |
| `_Shell` | class | `tests/test_loop_exit_gate.py:113` | `class _Shell` |
| `__init__` | method | `tests/test_loop_exit_gate.py:93` | `def __init__(self, code)` |
| `__init__` | method | `tests/test_loop_exit_gate.py:114` | `def __init__(self)` |
| `onecmd` | method | `tests/test_loop_exit_gate.py:96` | `def onecmd(self, cmd)` |
| `onecmd` | method | `tests/test_loop_exit_gate.py:117` | `def onecmd(self, cmd)` |
| `test_autonomous_gate_raises_only_when_env_set` | function | `tests/test_loop_exit_gate.py:45` | `def test_autonomous_gate_raises_only_when_env_set(monkeypatch)` |
| `test_headless_catches_systemexit` | function | `tests/test_loop_exit_gate.py:100` | `def test_headless_catches_systemexit()` |
| `test_headless_chain_stops_on_failure` | function | `tests/test_loop_exit_gate.py:110` | `def test_headless_chain_stops_on_failure()` |
| `test_loop_exit_code_mapping` | function | `tests/test_loop_exit_gate.py:10` | `def test_loop_exit_code_mapping()` |
| `test_report_result_prints_verdict` | function | `tests/test_loop_exit_gate.py:131` | `def test_report_result_prints_verdict(capsys)` |
| `test_write_loop_result_sessions_fallback` | function | `tests/test_loop_exit_gate.py:80` | `def test_write_loop_result_sessions_fallback(tmp_path, monkeypatch)` |
| `test_write_loop_result_workspace` | function | `tests/test_loop_exit_gate.py:64` | `def test_write_loop_result_workspace(tmp_path, monkeypatch)` |
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
| `_FakePopen` | class | `tests/test_loop_manager_outcome.py:150` | `class _FakePopen` |
| `_FakeProcess` | class | `tests/test_loop_manager_outcome.py:48` | `class _FakeProcess` |
| `__init__` | method | `tests/test_loop_manager_outcome.py:49` | `def __init__(self, exit_code)` |
| `__init__` | method | `tests/test_loop_manager_outcome.py:151` | `def __init__(self, argv)` |
| `_fake_reap` | function | `tests/test_loop_manager_outcome.py:161` | `def _fake_reap(self, loop_id, process)` |
| `_register` | function | `tests/test_loop_manager_outcome.py:18` | `def _register(manager, loop_id, workspace)` |
| `manager` | function | `tests/test_loop_manager_outcome.py:12` | `def manager(tmp_path)` |
| `test_read_outcome_parses_result_json` | function | `tests/test_loop_manager_outcome.py:56` | `def test_read_outcome_parses_result_json(manager, tmp_path)` |
| `test_reap_cancelled_outcome_maps_stopped` | function | `tests/test_loop_manager_outcome.py:130` | `def test_reap_cancelled_outcome_maps_stopped(manager, tmp_path)` |
| `test_reap_falls_back_to_exit_code_without_outcome` | function | `tests/test_loop_manager_outcome.py:103` | `def test_reap_falls_back_to_exit_code_without_outcome(manager, tmp_path)` |
| `test_reap_marks_failed_on_honest_outcome` | function | `tests/test_loop_manager_outcome.py:68` | `def test_reap_marks_failed_on_honest_outcome(manager, tmp_path)` |
| `test_reap_marks_finished_on_success` | function | `tests/test_loop_manager_outcome.py:87` | `def test_reap_marks_finished_on_success(manager, tmp_path)` |
| `test_reap_stopped_overrides_outcome` | function | `tests/test_loop_manager_outcome.py:116` | `def test_reap_stopped_overrides_outcome(manager, tmp_path)` |
| `test_spawn_binds_workspace_env` | function | `tests/test_loop_manager_outcome.py:145` | `def test_spawn_binds_workspace_env(manager, tmp_path, monkeypatch)` |
| `wait` | method | `tests/test_loop_manager_outcome.py:52` | `def wait(self)` |
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
| `_patched_engine` | function | `tests/test_loop_objective_wiring.py:14` | `def _patched_engine(tmp_path, monkeypatch)` |
| `_point_objectives` | function | `tests/test_loop_objective_wiring.py:25` | `def _point_objectives(tmp_path, monkeypatch)` |
| `_statuses` | function | `tests/test_loop_objective_wiring.py:51` | `def _statuses(path)` |
| `_write_objective` | function | `tests/test_loop_objective_wiring.py:37` | `def _write_objective(path, objective_id, text, status, priority, target)` |
| `test_daemon_drain_drafts_helper_is_safe_without_engine` | function | `tests/test_loop_objective_wiring.py:172` | `def test_daemon_drain_drafts_helper_is_safe_without_engine()` |
| `test_daemon_drain_drafts_imports_pending_draft` | function | `tests/test_loop_objective_wiring.py:179` | `def test_daemon_drain_drafts_imports_pending_draft(tmp_path, monkeypatch)` |
| `test_drain_drafts_imports_pending_draft_as_task` | function | `tests/test_loop_objective_wiring.py:128` | `def test_drain_drafts_imports_pending_draft_as_task(tmp_path, monkeypatch)` |
| `test_drain_drafts_is_idempotent` | function | `tests/test_loop_objective_wiring.py:153` | `def test_drain_drafts_is_idempotent(tmp_path, monkeypatch)` |
| `test_pending_objectives_filters_by_target_and_priority` | function | `tests/test_loop_objective_wiring.py:61` | `def test_pending_objectives_filters_by_target_and_priority(tmp_path, monkeypatch)` |
| `test_planner_emits_and_claims_injected_objective` | function | `tests/test_loop_objective_wiring.py:77` | `def test_planner_emits_and_claims_injected_objective(tmp_path, monkeypatch)` |
| `test_settle_marks_done_when_intent_done` | function | `tests/test_loop_objective_wiring.py:95` | `def test_settle_marks_done_when_intent_done(tmp_path, monkeypatch)` |
| `test_settle_requeues_when_intent_unfinished` | function | `tests/test_loop_objective_wiring.py:112` | `def test_settle_requeues_when_intent_unfinished(tmp_path, monkeypatch)` |
| `_accept` | function | `tests/test_loop_preflight.py:110` | `def _accept()` |
| `test_check_target_fails_fast_on_stopped_lab` | function | `tests/test_loop_preflight.py:39` | `def test_check_target_fails_fast_on_stopped_lab()` |
| `test_check_target_passes_on_running_lab` | function | `tests/test_loop_preflight.py:52` | `def test_check_target_passes_on_running_lab()` |
| `test_check_target_probes_tcp` | function | `tests/test_loop_preflight.py:63` | `def test_check_target_probes_tcp(monkeypatch)` |
| `test_check_target_refused_means_alive` | function | `tests/test_loop_preflight.py:82` | `def test_check_target_refused_means_alive(monkeypatch)` |
| `test_check_target_without_target` | function | `tests/test_loop_preflight.py:94` | `def test_check_target_without_target()` |
| `test_lab_state_maps_running_and_stopped` | function | `tests/test_loop_preflight.py:8` | `def test_lab_state_maps_running_and_stopped()` |
| `test_no_preflight_hint_override` | function | `tests/test_loop_preflight.py:128` | `def test_no_preflight_hint_override()` |
| `test_preflight_flag_parses` | function | `tests/test_loop_preflight.py:136` | `def test_preflight_flag_parses()` |
| `test_probe_tcp_real_socket` | function | `tests/test_loop_preflight.py:102` | `def test_probe_tcp_real_socket()` |
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
| `_Bare` | class | `tests/test_loop_target_authority.py:83` | `class _Bare` |
| `_FakeShell` | class | `tests/test_loop_target_authority.py:16` | `class _FakeShell` |
| `__init__` | method | `tests/test_loop_target_authority.py:19` | `def __init__(self, params)` |
| `__init__` | method | `tests/test_loop_target_authority.py:84` | `def __init__(self)` |
| `_fake_save` | function | `tests/test_loop_target_authority.py:78` | `def _fake_save(params)` |
| `_scope_save` | method | `tests/test_loop_target_authority.py:23` | `def _scope_save(self, entries, mode)` |
| `test_dedupes_and_strips` | function | `tests/test_loop_target_authority.py:49` | `def test_dedupes_and_strips()` |
| `test_empty_targets_is_noop` | function | `tests/test_loop_target_authority.py:68` | `def test_empty_targets_is_noop()` |
| `test_enforcement_mode_untouched` | function | `tests/test_loop_target_authority.py:62` | `def test_enforcement_mode_untouched()` |
| `test_fallback_writer_without_scope_save` | function | `tests/test_loop_target_authority.py:75` | `def test_fallback_writer_without_scope_save(monkeypatch)` |
| `test_multi_target_scope_is_every_target` | function | `tests/test_loop_target_authority.py:42` | `def test_multi_target_scope_is_every_target()` |
| `test_noop_when_already_bound` | function | `tests/test_loop_target_authority.py:55` | `def test_noop_when_already_bound()` |
| `test_single_target_replaces_rhost_and_scope` | function | `tests/test_loop_target_authority.py:31` | `def test_single_target_replaces_rhost_and_scope()` |
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
| `_boom` | function | `tests/test_mcp_auto_loop_wrapper.py:34` | `def _boom(shell, params, line, verb)` |
| `_fake_run` | function | `tests/test_mcp_auto_loop_wrapper.py:47` | `def _fake_run(shell, params, line, verb)` |
| `_patched` | function | `tests/test_mcp_auto_loop_wrapper.py:15` | `def _patched(monkeypatch, tmp_path)` |
| `_refuse` | function | `tests/test_mcp_auto_loop_wrapper.py:41` | `def _refuse(shell, params, line, verb)` |
| `_text` | function | `tests/test_mcp_auto_loop_wrapper.py:148` | `def _text(response)` |
| `loop_join` | function | `tests/test_mcp_auto_loop_wrapper.py:163` | `def loop_join(coro)` |
| `test_fast_path_routes_through_the_shared_runner` | function | `tests/test_mcp_auto_loop_wrapper.py:60` | `def test_fast_path_routes_through_the_shared_runner(monkeypatch, tmp_path)` |
| `test_legacy_flag_annotates_but_routes_shared` | function | `tests/test_mcp_auto_loop_wrapper.py:75` | `def test_legacy_flag_annotates_but_routes_shared(monkeypatch, tmp_path)` |
| `test_loop_line_translation` | function | `tests/test_mcp_auto_loop_wrapper.py:131` | `def test_loop_line_translation()` |
| `test_preflight_failed_summary_still_renders_the_task` | function | `tests/test_mcp_auto_loop_wrapper.py:106` | `def test_preflight_failed_summary_still_renders_the_task(monkeypatch, tmp_path)` |
| `test_refused_run_reports_the_reason` | function | `tests/test_mcp_auto_loop_wrapper.py:95` | `def test_refused_run_reports_the_reason(monkeypatch, tmp_path)` |
| `test_runner_failure_surfaces` | function | `tests/test_mcp_auto_loop_wrapper.py:85` | `def test_runner_failure_surfaces(monkeypatch, tmp_path)` |
| `test_schema_matches_the_shared_flags` | function | `tests/test_mcp_auto_loop_wrapper.py:121` | `def test_schema_matches_the_shared_flags()` |
| `TestRegistryDispatch` | class | `tests/test_mcp_dispatch.py:61` | `class TestRegistryDispatch` |
| `_fallback_branches` | function | `tests/test_mcp_dispatch.py:50` | `def _fallback_branches()` |
| `_package_names` | function | `tests/test_mcp_dispatch.py:29` | `def _package_names()` |
| `_registered` | function | `tests/test_mcp_dispatch.py:33` | `def _registered()` |
| `test_mcp_never_offers_interactive_repl` | function | `tests/test_mcp_dispatch.py:121` | `def test_mcp_never_offers_interactive_repl()` |
| `test_migrated_handlers_absent_from_fallback` | method | `tests/test_mcp_dispatch.py:71` | `def test_migrated_handlers_absent_from_fallback(self)` |
| `test_migrated_handlers_registered` | method | `tests/test_mcp_dispatch.py:66` | `def test_migrated_handlers_registered(self)` |
| `test_new_chain_shell_tools_have_defs_and_handlers` | function | `tests/test_mcp_dispatch.py:99` | `def test_new_chain_shell_tools_have_defs_and_handlers()` |
| `test_no_dead_duplicate_branches` | method | `tests/test_mcp_dispatch.py:62` | `def test_no_dead_duplicate_branches(self)` |
| `test_opencode_bridge_curates_loop_and_chain` | function | `tests/test_mcp_dispatch.py:106` | `def test_opencode_bridge_curates_loop_and_chain()` |
| `test_set_config_refuses_null_values` | function | `tests/test_mcp_dispatch.py:79` | `def test_set_config_refuses_null_values()` |
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

Next: [SYMBOLS_p47.md](SYMBOLS_p47.md)
