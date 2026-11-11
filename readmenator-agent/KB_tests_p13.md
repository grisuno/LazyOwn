# Subsystem: tests (page 13 of 25)
Previous: [KB_tests_p12.md](KB_tests_p12.md)

## tests/test_lab_target_visibility.py
- Doc: Lab target visibility: start/status always show the container IP.
- Layer: testing
- Language: py
- Symbols:
  - `test_start_on_running_lab_reports_ip` (function, line 14) `def test_start_on_running_lab_reports_ip(capsys, monkeypatch)`
  - `test_status_reports_ip` (function, line 27) `def test_status_reports_ip(capsys, monkeypatch)`
- Depends on: `cli/commands/lab.py`

## tests/test_lazy_adaptive_replan.py
- Doc: Adaptive replanner wiring through the ChainRunner (apt_chain --adaptive).
- Layer: testing
- Language: py
- Symbols:
  - `_chain` (function, line 14) `def _chain(steps)`
  - `_fail_locked_out` (function, line 19) `def _fail_locked_out(command)`
  - `_facts` (function, line 25) `def _facts(monkeypatch, services, credentials)`
  - `test_parse_accepts_adaptive_flag` (function, line 30) `def test_parse_accepts_adaptive_flag()`
  - `test_adaptive_replanner_inserts_alternative_after_permission_wall` (function, line 38) `def test_adaptive_replanner_inserts_alternative_after_permission_wall(monkeypatch)`
  - `test_lockout_walls_insert_nothing` (function, line 76) `def test_lockout_walls_insert_nothing(monkeypatch)`
  - `test_composed_replanners_run_in_order` (function, line 110) `def test_composed_replanners_run_in_order(monkeypatch)`
  - `test_replanner_ignores_ok_outcomes` (function, line 135) `def test_replanner_ignores_ok_outcomes()`
  - `executor` (function, line 44) `def executor(command)`
  - `executor` (function, line 81) `def executor(command)`
  - `first` (function, line 116) `def first(context)`
  - `second` (function, line 119) `def second(context)`
  - `FakeOutcome` (class, line 124) `class FakeOutcome`
  - `Ctx` (class, line 141) `class Ctx`
  - `Outcome` (class, line 145) `class Outcome`
  - `insert_step` (method, line 156) `def insert_step(self, step)`
- Depends on: `cli/apt_chain_support.py`, `modules/chain_registry.py`, `modules/chain_runner.py`

## tests/test_lazy_agent.py
- Doc: Agentic tool-calling: worker agent path, resume and main sessions.
- Layer: testing
- Language: py
- Symbols:
  - `_tool_call` (function, line 13) `def _tool_call(tool_id, name, arguments)`
  - `_message` (function, line 19) `def _message(content, tool_calls)`
  - `_Completions` (class, line 23) `class _Completions`
  - `fake_model` (function, line 37) `def fake_model(script)`
  - `_sandbox` (function, line 43) `def _sandbox(tmp_path, monkeypatch)`
  - `_worker` (function, line 50) `def _worker(loop, engine, task_id, graph)`
  - `test_worker_agentic_tool_calling` (function, line 63) `def test_worker_agentic_tool_calling(tmp_path, monkeypatch)`
  - `test_worker_agentic_resume_seeds_prior_turns` (function, line 104) `def test_worker_agentic_resume_seeds_prior_turns(tmp_path, monkeypatch)`
  - `test_main_session_persists_and_resumes` (function, line 138) `def test_main_session_persists_and_resumes(tmp_path, monkeypatch)`
  - `test_model_keepalive_tick_while_waiting` (function, line 152) `def test_model_keepalive_tick_while_waiting(tmp_path, monkeypatch)`
  - `test_tool_calling_flag_honors_payload` (function, line 175) `def test_tool_calling_flag_honors_payload(tmp_path, monkeypatch)`
  - `test_external_opencode_degrades_without_binary` (function, line 184) `def test_external_opencode_degrades_without_binary(monkeypatch)`
  - `test_lazy_agent_command_session_lifecycle` (function, line 194) `def test_lazy_agent_command_session_lifecycle(tmp_path, monkeypatch)`
  - `__init__` (method, line 26) `def __init__(self, script)`
  - `create` (method, line 30) `def create(self)`
  - `_executor` (function, line 85) `def _executor(command)`
  - `_Completions` (class, line 162) `class _Completions`
  - `create` (method, line 163) `def create(self)`
- Depends on: `cli/commands/lazyops.py`, `core/config.py`, `modules/__init__.py`, `modules/lazy_agent.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_lazy_autofire.py
- Doc: BDD tests for the lazy_autofire intelligence-to-chain closure.
- Layer: testing
- Language: py
- Symbols:
  - `_clean_report` (function, line 13) `def _clean_report()`
  - `TestConsiderReport` (class, line 36) `class TestConsiderReport`
  - `TestHelpers` (class, line 98) `class TestHelpers`
  - `test_unarmed_proposes` (method, line 37) `def test_unarmed_proposes(self, tmp_path)`
  - `test_armed_writes_validated_chain` (method, line 48) `def test_armed_writes_validated_chain(self, tmp_path)`
  - `test_step_cap` (method, line 62) `def test_step_cap(self, tmp_path)`
  - `test_smoke_tier_never_fires` (method, line 72) `def test_smoke_tier_never_fires(self, tmp_path)`
  - `test_cooldown_blocks_regeneration` (method, line 81) `def test_cooldown_blocks_regeneration(self, tmp_path)`
  - `test_state_persisted` (method, line 90) `def test_state_persisted(self, tmp_path)`
  - `test_autofire_armed_contract` (method, line 99) `def test_autofire_armed_contract(self)`
  - `test_status_surface` (method, line 105) `def test_status_surface(self, tmp_path)`
  - `test_sweep_prunes_expired` (method, line 112) `def test_sweep_prunes_expired(self, tmp_path)`
  - `test_fire_from_missing_report` (method, line 119) `def test_fire_from_missing_report(self, tmp_path)`
- Depends on: `modules/__init__.py`

## tests/test_lazy_blindspot.py
- Doc: Blindspot review contract tests: parse, fence, apply and loop gating.
- Layer: testing
- Language: py
- Symbols:
  - `_payload` (function, line 16) `def _payload(spots)`
  - `test_parse_fenced_json` (function, line 20) `def test_parse_fenced_json()`
  - `test_parse_bare_json_and_defaults` (function, line 28) `def test_parse_bare_json_and_defaults()`
  - `test_parse_drops_invalid_entries` (function, line 36) `def test_parse_drops_invalid_entries()`
  - `test_parse_accepted_false_yields_none` (function, line 42) `def test_parse_accepted_false_yields_none()`
  - `test_parse_garbage_yields_empty` (function, line 46) `def test_parse_garbage_yields_empty()`
  - `test_parse_risk_normalized_and_capped` (function, line 51) `def test_parse_risk_normalized_and_capped()`
  - `test_hint_rendering_with_and_without_suggestion` (function, line 58) `def test_hint_rendering_with_and_without_suggestion()`
  - `test_prompt_fences_untrusted_blocks` (function, line 65) `def test_prompt_fences_untrusted_blocks()`
  - `test_review_applies_findings_as_hints` (function, line 73) `def test_review_applies_findings_as_hints()`
  - `test_review_unavailable_or_garbage_is_silent` (function, line 82) `def test_review_unavailable_or_garbage_is_silent()`
  - `test_review_pool_exception_is_silent` (function, line 91) `def test_review_pool_exception_is_silent()`
  - `test_apply_raising_sink_keeps_finding_out` (function, line 99) `def test_apply_raising_sink_keeps_finding_out()`
  - `test_apply_none_sink_stops_cleanly` (function, line 109) `def test_apply_none_sink_stops_cleanly()`
  - `test_engine_blindspot_review_disabled_by_default` (function, line 115) `def test_engine_blindspot_review_disabled_by_default(tmp_path, monkeypatch)`
  - `test_engine_blindspot_enabled_reads_payload` (function, line 125) `def test_engine_blindspot_enabled_reads_payload(tmp_path, monkeypatch)`
  - `test_maybe_blindspot_requires_flag_and_quiet_planner` (function, line 133) `def test_maybe_blindspot_requires_flag_and_quiet_planner()`
  - `test_maybe_blindspot_respects_stage_toggle` (function, line 160) `def test_maybe_blindspot_respects_stage_toggle()`
  - `boom` (function, line 92) `def boom(prompt, max_tokens)`
  - `raising_sink` (function, line 102) `def raising_sink(text)`
  - `fake_review` (function, line 140) `def fake_review(task_id)`
- Depends on: `modules/lazy_blindspot.py`, `modules/lazy_loop.py`

## tests/test_lazy_bridge_traffic.py
- Doc: Incremental LAZY traffic mirroring (stall regression).
- Layer: testing
- Language: py
- Symbols:
  - `_sandbox` (function, line 16) `def _sandbox(tmp_path, monkeypatch)`
  - `_append` (function, line 29) `def _append(path, rows)`
  - `_exchanges` (function, line 35) `def _exchanges(sessions_dir)`
  - `test_traffic_mirror_is_incremental` (function, line 39) `def test_traffic_mirror_is_incremental(tmp_path, monkeypatch)`
  - `test_partial_line_is_retried` (function, line 61) `def test_partial_line_is_retried(tmp_path, monkeypatch)`
  - `test_progress_callback_survives_failures` (function, line 78) `def test_progress_callback_survives_failures(tmp_path, monkeypatch)`
  - `_boom` (function, line 83) `def _boom(_text)`
- Depends on: `modules/__init__.py`, `modules/traffic_recorder.py`

## tests/test_lazy_checks.py
- Doc: Lazy checks doctrine: version-aware interpretation of read-only retests.
- Layer: testing
- Language: py
- Symbols:
  - `test_extract_version_tolerates_patch_tails_and_rejects_ips` (function, line 27) `def test_extract_version_tolerates_patch_tails_and_rejects_ips()`
  - `test_extract_cve_uppercases` (function, line 36) `def test_extract_cve_uppercases()`
  - `test_interpret_reaffirms_when_observed_version_in_range` (function, line 42) `def test_interpret_reaffirms_when_observed_version_in_range()`
  - `test_interpret_flags_version_changed` (function, line 54) `def test_interpret_flags_version_changed()`
  - `test_interpret_without_version_or_range_stays_inconclusive_on_miss` (function, line 65) `def test_interpret_without_version_or_range_stays_inconclusive_on_miss()`
  - `test_convert_osv_ranges_and_range_for_cve` (function, line 76) `def test_convert_osv_ranges_and_range_for_cve(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_checks.py`, `modules/lazy_cve_feed.py`

## tests/test_lazy_commander.py
- Doc: Fleet commander contract tests: parse, prompt, fairness and the loop.
- Layer: testing
- Language: py
- Symbols:
  - `_reply` (function, line 20) `def _reply(action, target, note, accepted)`
  - `_rows` (function, line 27) `def _rows()`
  - `test_actions_vocabulary` (function, line 35) `def test_actions_vocabulary()`
  - `test_parse_valid_actions` (function, line 39) `def test_parse_valid_actions()`
  - `test_parse_fenced_and_case` (function, line 46) `def test_parse_fenced_and_case()`
  - `test_parse_rejects_unusable` (function, line 52) `def test_parse_rejects_unusable()`
  - `test_parse_accepted_false_is_reject` (function, line 60) `def test_parse_accepted_false_is_reject()`
  - `test_parse_bare_object_without_envelope` (function, line 65) `def test_parse_bare_object_without_envelope()`
  - `test_board_renders_rows_and_slices` (function, line 70) `def test_board_renders_rows_and_slices()`
  - `test_prompt_fences_board_and_strips_backticks` (function, line 78) `def test_prompt_fences_board_and_strips_backticks()`
  - `test_budget_line` (function, line 86) `def test_budget_line()`
  - `test_least_worked_first_fallback` (function, line 91) `def test_least_worked_first_fallback()`
  - `test_fallback_tiebreak_stale_first` (function, line 107) `def test_fallback_tiebreak_stale_first()`
  - `test_model_decision_drives_slices` (function, line 118) `def test_model_decision_drives_slices()`
  - `test_fire_pauses_and_keeps_task_out` (function, line 135) `def test_fire_pauses_and_keeps_task_out()`
  - `test_fire_only_target_ends_cleanly` (function, line 152) `def test_fire_only_target_ends_cleanly()`
  - `test_unknown_target_counts_toward_noop_limit` (function, line 167) `def test_unknown_target_counts_toward_noop_limit()`
  - `test_garbage_reply_falls_back_to_fairness` (function, line 183) `def test_garbage_reply_falls_back_to_fairness()`
  - `test_reject_replies_hit_noop_limit` (function, line 198) `def test_reject_replies_hit_noop_limit()`
  - `test_deadline_stops_before_slices` (function, line 213) `def test_deadline_stops_before_slices()`
  - `test_empty_board_ends_cleanly` (function, line 238) `def test_empty_board_ends_cleanly()`
  - `test_board_fn_failure_ends_cleanly` (function, line 252) `def test_board_fn_failure_ends_cleanly()`
  - `test_model_exception_falls_back_to_fairness` (function, line 265) `def test_model_exception_falls_back_to_fairness()`
  - `work` (function, line 216) `def work(task_id, workers)`
  - `wrapped` (function, line 221) `def wrapped(task_id, workers)`
- Depends on: `modules/lazy_commander.py`

## tests/test_lazy_continuation.py
- Doc: Continuation record contract tests.
- Layer: testing
- Language: py
- Symbols:
  - `_install_sessions_dir` (function, line 13) `def _install_sessions_dir(monkeypatch, tmp_path)`
  - `TestSaveLoad` (class, line 17) `class TestSaveLoad`
  - `TestRecall` (class, line 87) `class TestRecall`
  - `TestPlannerWiring` (class, line 112) `class TestPlannerWiring`
  - `test_save_then_load_round_trip` (method, line 20) `def test_save_then_load_round_trip(self, monkeypatch, tmp_path)`
  - `test_credentials_round_trip_for_successor` (method, line 38) `def test_credentials_round_trip_for_successor(self, monkeypatch, tmp_path)`
  - `test_handover_brief_renders_playbook` (method, line 50) `def test_handover_brief_renders_playbook(self, monkeypatch, tmp_path)`
  - `test_handover_brief_missing_target_is_empty` (method, line 68) `def test_handover_brief_missing_target_is_empty(self, monkeypatch, tmp_path)`
  - `test_load_missing_target_is_none` (method, line 72) `def test_load_missing_target_is_none(self, monkeypatch, tmp_path)`
  - `test_save_without_target_is_false` (method, line 76) `def test_save_without_target_is_false(self, monkeypatch, tmp_path)`
  - `test_target_is_slug_sanitised` (method, line 80) `def test_target_is_slug_sanitised(self, monkeypatch, tmp_path)`
  - `test_recall_returns_intent_with_reason` (method, line 90) `def test_recall_returns_intent_with_reason(self, monkeypatch, tmp_path)`
  - `test_recall_without_record_is_empty` (method, line 100) `def test_recall_without_record_is_empty(self, monkeypatch, tmp_path)`
  - `test_recall_respects_limit` (method, line 104) `def test_recall_respects_limit(self, monkeypatch, tmp_path)`
  - `test_continuation_marker_constant_exists` (method, line 115) `def test_continuation_marker_constant_exists(self)`
  - `test_lazy_loop_writes_continuation_on_terminal_status` (method, line 120) `def test_lazy_loop_writes_continuation_on_terminal_status(self)`
- Depends on: `modules/__init__.py`, `modules/lazy_loop.py`

## tests/test_lazy_creds.py
- Doc: Contract tests for the lazycreds default-credential knowledge base.
- Layer: testing
- Language: py
- Symbols:
  - `LazyCredsKbSpec` (class, line 12) `class LazyCredsKbSpec(TestCase)`
  - `test_kb_loads_rows` (method, line 15) `def test_kb_loads_rows(self)`
  - `test_search_matches_vendor_and_username` (method, line 23) `def test_search_matches_vendor_and_username(self)`
  - `test_search_is_case_insensitive` (method, line 29) `def test_search_is_case_insensitive(self)`
  - `test_search_capped` (method, line 34) `def test_search_capped(self)`
  - `test_candidates_distinct_and_ranked` (method, line 38) `def test_candidates_distinct_and_ranked(self)`
  - `test_as_lines_rendered` (method, line 44) `def test_as_lines_rendered(self)`
  - `test_export_pairs_writes_file` (method, line 48) `def test_export_pairs_writes_file(self)`
  - `test_export_rejects_bad_path` (method, line 58) `def test_export_rejects_bad_path(self)`
- Depends on: `modules/__init__.py`

## tests/test_lazy_deviations.py
- Doc: Deviation ledger contract tests: record, dedupe, cap, render.
- Layer: testing
- Language: py
- Symbols:
  - `ledger` (function, line 17) `def ledger(tmp_path)`
  - `test_default_path_points_into_sessions_lazy` (function, line 21) `def test_default_path_points_into_sessions_lazy()`
  - `test_record_requires_reason_and_change` (function, line 26) `def test_record_requires_reason_and_change(ledger)`
  - `test_record_collapses_repeats` (function, line 35) `def test_record_collapses_repeats(ledger)`
  - `test_list_scopes_and_order` (function, line 42) `def test_list_scopes_and_order(ledger)`
  - `test_texts_cleaned_and_bounded` (function, line 52) `def test_texts_cleaned_and_bounded(ledger)`
  - `test_survives_broken_lines` (function, line 61) `def test_survives_broken_lines(ledger, tmp_path)`
  - `test_trim_caps_file` (function, line 72) `def test_trim_caps_file(tmp_path)`
  - `test_render_markdown_block` (function, line 84) `def test_render_markdown_block(ledger)`
  - `test_render_markdown_empty` (function, line 92) `def test_render_markdown_empty(ledger)`
  - `test_read_missing_file_is_empty` (function, line 96) `def test_read_missing_file_is_empty(tmp_path)`
  - `test_worker_sanitize_records_deviation` (function, line 100) `def test_worker_sanitize_records_deviation(tmp_path, monkeypatch)`
  - `test_chain_replanner_deviations_recorded` (function, line 134) `def test_chain_replanner_deviations_recorded(tmp_path, monkeypatch)`
  - `test_handover_brief_includes_deviations` (function, line 157) `def test_handover_brief_includes_deviations(tmp_path, monkeypatch)`
  - `FakeActivity` (class, line 105) `class FakeActivity`
  - `FakeIntent` (class, line 112) `class FakeIntent`
  - `FakeWorker` (class, line 115) `class FakeWorker`
  - `FakeReplanner` (class, line 142) `class FakeReplanner`
  - `__init__` (method, line 106) `def __init__(self)`
  - `emit` (method, line 109) `def emit(self)`
  - `_target_for` (method, line 121) `def _target_for(intent)`
  - `__call__` (method, line 143) `def __call__(self, context)`
- Depends on: `modules/__init__.py`, `modules/chain_registry.py`, `modules/chain_runner.py`, `modules/lazy_deviations.py`, `modules/lazy_loop.py`

## tests/test_lazy_engine.py
- Doc: Lazy engine (LAZY-faithful) regression tests with stub executor.
- Layer: testing
- Language: py
- Symbols:
  - `_stub_executor` (function, line 11) `def _stub_executor(command)`
  - `_no_llm` (function, line 23) `def _no_llm(monkeypatch)`
  - `engine` (function, line 33) `def engine(tmp_path, monkeypatch)`
  - `test_create_auto_scope_and_asset` (function, line 45) `def test_create_auto_scope_and_asset(engine)`
  - `test_scope_strict_no_external_intents` (function, line 52) `def test_scope_strict_no_external_intents(engine)`
  - `test_no_premature_done_goals_pending` (function, line 62) `def test_no_premature_done_goals_pending(engine)`
  - `test_worker_aggregates_single_fact` (function, line 71) `def test_worker_aggregates_single_fact(engine)`
  - `test_new_run_clears_previous_shutdown` (function, line 77) `def test_new_run_clears_previous_shutdown(engine)`
  - `test_pause_resume` (function, line 87) `def test_pause_resume(engine)`
  - `test_prove_goal_needs_reason_and_evidence` (function, line 97) `def test_prove_goal_needs_reason_and_evidence(engine)`
  - `test_lazy_alias_surface` (function, line 107) `def test_lazy_alias_surface()`
  - `test_delete_task_sweeps_only_its_store_files` (function, line 117) `def test_delete_task_sweeps_only_its_store_files(engine, tmp_path)`
  - `test_delete_task_unknown_returns_empty` (function, line 131) `def test_delete_task_unknown_returns_empty(engine)`
- Depends on: `cli/commands/lazyops.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`

## tests/test_lazy_evidence.py
- Doc: Traffic recorder trigram search and frozen evidence package export.
- Layer: testing
- Language: py
- Symbols:
  - `test_trigram_search_finds_mid_token` (function, line 16) `def test_trigram_search_finds_mid_token(tmp_path)`
  - `test_legacy_fts_is_migrated_in_place` (function, line 34) `def test_legacy_fts_is_migrated_in_place(tmp_path)`
  - `test_export_evidence_freezes_files_with_hashes` (function, line 53) `def test_export_evidence_freezes_files_with_hashes(tmp_path, monkeypatch)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/traffic_recorder.py`

## tests/test_lazy_exposure.py
- Doc: BDD tests for the lazy exposure report engine.
- Layer: testing
- Language: py
- Symbols:
  - `TestGenerateReport` (class, line 42) `class TestGenerateReport`
  - `TestPublish` (class, line 101) `class TestPublish`
  - `test_in_range_matches_ranked` (method, line 43) `def test_in_range_matches_ranked(self)`
  - `test_unbounded_kev_is_review_not_match` (method, line 51) `def test_unbounded_kev_is_review_not_match(self)`
  - `test_leads_for_unversioned` (method, line 57) `def test_leads_for_unversioned(self)`
  - `test_score_breakdown` (method, line 66) `def test_score_breakdown(self)`
  - `test_checks_render_for_bounded` (method, line 73) `def test_checks_render_for_bounded(self)`
  - `test_feed_fingerprint_recorded` (method, line 81) `def test_feed_fingerprint_recorded(self)`
  - `test_save_report_atomic` (method, line 86) `def test_save_report_atomic(self, tmp_path)`
  - `test_save_report_survives_bad_path` (method, line 95) `def test_save_report_survives_bad_path(self, tmp_path)`
  - `test_publish_event` (method, line 102) `def test_publish_event(self)`
  - `test_score_report_caps` (method, line 110) `def test_score_report_caps(self)`
  - `test_probe_checks_sorted_and_capped` (method, line 125) `def test_probe_checks_sorted_and_capped(self)`
- Depends on: `modules/__init__.py`, `modules/lazy_exposure.py`, `modules/lazy_feedmatch.py`

## tests/test_lazy_fallback.py
- Doc: Adaptive fallback arbiter: prerequisites, one-shot memory, no lockouts.
- Layer: testing
- Language: py
- Symbols:
  - `_verdict` (function, line 12) `def _verdict(failure_class)`
  - `test_kerberoast_failure_gets_ordered_alternatives` (function, line 19) `def test_kerberoast_failure_gets_ordered_alternatives()`
  - `test_lockout_never_gets_an_alternative` (function, line 43) `def test_lockout_never_gets_an_alternative()`
  - `test_service_gates_fail_closed_on_unknown_evidence` (function, line 56) `def test_service_gates_fail_closed_on_unknown_evidence()`
  - `test_service_gates_skip_unserved_candidates` (function, line 68) `def test_service_gates_skip_unserved_candidates()`
  - `test_credential_gates_fail_closed_when_unknown` (function, line 80) `def test_credential_gates_fail_closed_when_unknown()`
  - `test_unknown_catalogue_ids_never_propose` (function, line 94) `def test_unknown_catalogue_ids_never_propose()`
  - `test_tool_missing_or_scope_verdicts_get_no_alternatives` (function, line 107) `def test_tool_missing_or_scope_verdicts_get_no_alternatives()`
  - `test_unmatched_command_gets_no_alternatives` (function, line 115) `def test_unmatched_command_gets_no_alternatives()`
  - `test_graph_is_well_formed` (function, line 127) `def test_graph_is_well_formed()`
- Depends on: `modules/failure_verdict.py`, `modules/lazy_fallback.py`

## tests/test_lazy_feedmatch.py
- Doc: BDD tests for the lazy feed schema and hard-evidence version matching.
- Layer: testing
- Language: py
- Symbols:
  - `TestParseVersion` (class, line 49) `class TestParseVersion`
  - `TestProductTokens` (class, line 68) `class TestProductTokens`
  - `TestRanges` (class, line 91) `class TestRanges`
  - `TestBindSighting` (class, line 107) `class TestBindSighting`
  - `TestLoadFeed` (class, line 152) `class TestLoadFeed`
  - `TestLiveBindings` (class, line 181) `class TestLiveBindings`
  - `test_plain_numbers` (method, line 50) `def test_plain_numbers(self)`
  - `test_ignored_epoch` (method, line 54) `def test_ignored_epoch(self)`
  - `test_pre_release_ordering` (method, line 58) `def test_pre_release_ordering(self)`
  - `test_garbage_returns_none` (method, line 62) `def test_garbage_returns_none(self)`
  - `test_os_sightings_never_match` (method, line 69) `def test_os_sightings_never_match(self)`
  - `test_generic_filler_never_binds` (method, line 76) `def test_generic_filler_never_binds(self)`
  - `test_version_suffix_split` (method, line 82) `def test_version_suffix_split(self)`
  - `test_http_daemon_words_stripped` (method, line 86) `def test_http_daemon_words_stripped(self)`
  - `test_in_range` (method, line 92) `def test_in_range(self)`
  - `test_fixed_bound_excludes` (method, line 97) `def test_fixed_bound_excludes(self)`
  - `test_unbounded_is_none` (method, line 102) `def test_unbounded_is_none(self)`
  - `feed` (method, line 109) `def feed(self)`
  - `test_hard_evidence_in_range` (method, line 112) `def test_hard_evidence_in_range(self, feed)`
  - `test_fixed_version_not_affected` (method, line 119) `def test_fixed_version_not_affected(self, feed)`
  - `test_unbounded_kev_review` (method, line 124) `def test_unbounded_kev_review(self, feed)`
  - `test_name_only_never_binds` (method, line 131) `def test_name_only_never_binds(self, feed)`
  - `test_out_of_range_version_binds_nothing` (method, line 136) `def test_out_of_range_version_binds_nothing(self, feed)`
  - `test_unversioned_leads` (method, line 141) `def test_unversioned_leads(self, feed)`
  - `test_lazy_schema` (method, line 153) `def test_lazy_schema(self, tmp_path)`
  - `test_kev_dump_mapping` (method, line 160) `def test_kev_dump_mapping(self, tmp_path)`
  - `test_missing_file_is_silent` (method, line 170) `def test_missing_file_is_silent(self, tmp_path)`
  - `test_parse_feed_drops_malformed` (method, line 174) `def test_parse_feed_drops_malformed(self)`
  - `test_live_bindings_offline_contract` (method, line 182) `def test_live_bindings_offline_contract(self)`
  - `test_live_bindings_source_passthrough` (method, line 201) `def test_live_bindings_source_passthrough(self)`
- Depends on: `modules/__init__.py`, `modules/lazy_feedmatch.py`, `modules/lazy_heat.py`

## tests/test_lazy_finalizer.py
- Doc: Evidence-gated finalization contract.
- Layer: testing
- Language: py
- Symbols:
  - `test_done_with_confirmed_findings_is_achieved_and_verified` (function, line 14) `def test_done_with_confirmed_findings_is_achieved_and_verified()`
  - `test_done_without_any_evidence_is_downgraded_to_failed` (function, line 23) `def test_done_without_any_evidence_is_downgraded_to_failed()`
  - `test_done_with_weak_evidence_downgrades_to_partial` (function, line 33) `def test_done_with_weak_evidence_downgrades_to_partial()`
  - `test_facts_plus_tested_is_strong_evidence` (function, line 42) `def test_facts_plus_tested_is_strong_evidence()`
  - `test_non_done_status_is_not_finalizable_without_evidence` (function, line 49) `def test_non_done_status_is_not_finalizable_without_evidence()`
  - `test_decision_to_dict_round_trips_fields` (function, line 56) `def test_decision_to_dict_round_trips_fields()`
  - `test_pending_approvals_block_achieved` (function, line 73) `def test_pending_approvals_block_achieved()`
  - `test_pending_plan_steps_block_achieved` (function, line 89) `def test_pending_plan_steps_block_achieved()`
  - `test_pending_blocks_beat_evidence` (function, line 105) `def test_pending_blocks_beat_evidence()`
  - `test_pending_state_survives_into_non_done_reasons` (function, line 121) `def test_pending_state_survives_into_non_done_reasons()`
- Depends on: `modules/__init__.py`

## tests/test_lazy_findings.py
- Doc: Tests for modules.lazy_findings — engagement findings ledger.
- Layer: testing
- Language: py
- Symbols:
  - `ledger_module` (function, line 23) `def ledger_module()`
  - `tmp_base` (function, line 30) `def tmp_base()`
  - `TestNormalize` (class, line 35) `class TestNormalize`
  - `TestEvents` (class, line 117) `class TestEvents`
  - `TestLedger` (class, line 178) `class TestLedger`
  - `TestCountsHandoff` (class, line 239) `class TestCountsHandoff`
  - `TestDiscardRow` (class, line 260) `class TestDiscardRow`
  - `test_valid_row_passes` (method, line 36) `def test_valid_row_passes(self, ledger_module, tmp_base)`
  - `test_empty_title_rejected` (method, line 55) `def test_empty_title_rejected(self, ledger_module)`
  - `test_unknown_state_rejected` (method, line 60) `def test_unknown_state_rejected(self, ledger_module)`
  - `test_unknown_level_rejected` (method, line 65) `def test_unknown_level_rejected(self, ledger_module)`
  - `test_invented_technique_rejected` (method, line 70) `def test_invented_technique_rejected(self, ledger_module)`
  - `test_tac_id_accepted` (method, line 75) `def test_tac_id_accepted(self, ledger_module)`
  - `test_confirmed_requires_evidence` (method, line 82) `def test_confirmed_requires_evidence(self, ledger_module)`
  - `test_confirmed_with_reproducible_ok` (method, line 91) `def test_confirmed_with_reproducible_ok(self, ledger_module)`
  - `test_confirmed_with_artifact_ref_ok` (method, line 104) `def test_confirmed_with_artifact_ref_ok(self, ledger_module)`
  - `test_verdict_reproduced_promotes` (method, line 118) `def test_verdict_reproduced_promotes(self, ledger_module)`
  - `test_verdict_fixed_discards` (method, line 137) `def test_verdict_fixed_discards(self, ledger_module)`
  - `test_verdict_inconclusive_partial` (method, line 144) `def test_verdict_inconclusive_partial(self, ledger_module)`
  - `test_unmapped_verdict_ignores` (method, line 151) `def test_unmapped_verdict_ignores(self, ledger_module)`
  - `test_out_of_scope_kind_ignores` (method, line 157) `def test_out_of_scope_kind_ignores(self, ledger_module)`
  - `test_exploit_success_confirmed` (method, line 161) `def test_exploit_success_confirmed(self, ledger_module)`
  - `test_traversal_rejected` (method, line 179) `def test_traversal_rejected(self, ledger_module, tmp_base)`
  - `test_append_and_read_pg` (method, line 184) `def test_append_and_read_pg(self, ledger_module, tmp_base)`
  - `test_corrupt_lines_skipped` (method, line 199) `def test_corrupt_lines_skipped(self, ledger_module, tmp_base)`
  - `test_redaction_masks_secrets` (method, line 208) `def test_redaction_masks_secrets(self, ledger_module, tmp_base)`
  - `test_redaction_off_shows_verbatim` (method, line 224) `def test_redaction_off_shows_verbatim(self, ledger_module, tmp_base)`
  - `test_state_counts_latest_wins` (method, line 240) `def test_state_counts_latest_wins(self, ledger_module)`
  - `test_handoff_decision` (method, line 250) `def test_handoff_decision(self, ledger_module)`
  - `test_discard_row_normalized` (method, line 261) `def test_discard_row_normalized(self, ledger_module)`
- Depends on: `modules/lazy_findings.py`

## tests/test_lazy_hostscore.py
- Doc: Host heat score contract: deterministic, capped, auditable priorities.
- Layer: testing
- Language: py
- Symbols:
  - `test_hot_cve_and_findings_and_shell_stay_capped` (function, line 21) `def test_hot_cve_and_findings_and_shell_stay_capped()`
  - `test_findings_cap_bounds_the_subtotal` (function, line 39) `def test_findings_cap_bounds_the_subtotal()`
  - `test_discarded_findings_and_cold_no_points` (function, line 58) `def test_discarded_findings_and_cold_no_points()`
  - `test_empty_inputs_score_zero` (function, line 78) `def test_empty_inputs_score_zero()`
  - `test_persistence_roundtrip` (function, line 83) `def test_persistence_roundtrip(tmp_path)`
  - `test_rescore_offline_survives_errors` (function, line 93) `def test_rescore_offline_survives_errors(tmp_path, monkeypatch)`
  - `_StubWorld` (class, line 97) `class _StubWorld`
  - `broken_correlate` (function, line 116) `def broken_correlate()`
  - `snapshot` (method, line 100) `def snapshot(self)`
- Depends on: `modules/lazy_hostscore.py`

## tests/test_lazy_intel_wiring.py
- Doc: Wiring contract tests: loop timeline snapshot + MCP lazy intel tools.
- Layer: testing
- Language: py
- Symbols:
  - `TestExposureRefreshWiring` (class, line 13) `class TestExposureRefreshWiring`
  - `TestLoopTimelineWiring` (class, line 45) `class TestLoopTimelineWiring`
  - `TestMcpTools` (class, line 65) `class TestMcpTools`
  - `test_loop_refreshes_stale_intel_report` (method, line 14) `def test_loop_refreshes_stale_intel_report(self)`
  - `test_refresh_stale_contract` (method, line 20) `def test_refresh_stale_contract(self, tmp_path, monkeypatch)`
  - `test_sync_intel_records_timeline_snapshot` (method, line 46) `def test_sync_intel_records_timeline_snapshot(self)`
  - `test_shell_exit_snapshot_registered` (method, line 52) `def test_shell_exit_snapshot_registered(self)`
  - `test_record_quiet_never_raises` (method, line 57) `def test_record_quiet_never_raises(self, tmp_path)`
  - `test_lazy_tools_declared` (method, line 66) `def test_lazy_tools_declared(self)`
  - `test_lazy_tools_dispatched` (method, line 75) `def test_lazy_tools_dispatched(self)`
  - `test_hermes_bridge_exposes_lazy_tools` (method, line 83) `def test_hermes_bridge_exposes_lazy_tools(self)`
- Depends on: `modules/__init__.py`, `modules/lazy_timeline.py`

## tests/test_lazy_inventory.py
- Doc: BDD tests for the host-reported inventory contract.
- Layer: testing
- Language: py
- Symbols:
  - `TestBlobs` (class, line 25) `class TestBlobs`
  - `TestParse` (class, line 42) `class TestParse`
  - `TestPromotion` (class, line 63) `class TestPromotion`
  - `test_linux_blob_read_only` (method, line 26) `def test_linux_blob_read_only(self)`
  - `test_windows_blob_read_only` (method, line 31) `def test_windows_blob_read_only(self)`
  - `test_unknown_platform_empty` (method, line 37) `def test_unknown_platform_empty(self)`
  - `test_linux_parse` (method, line 43) `def test_linux_parse(self)`
  - `test_windows_parse` (method, line 51) `def test_windows_parse(self)`
  - `test_source_is_host` (method, line 57) `def test_source_is_host(self)`
  - `test_to_sightings` (method, line 64) `def test_to_sightings(self)`
  - `test_host_source_fills_missing_lead` (method, line 70) `def test_host_source_fills_missing_lead(self)`
  - `test_platform_of` (method, line 83) `def test_platform_of(self)`
- Depends on: `modules/__init__.py`

## tests/test_lazy_ledger.py
- Doc: Freshness ledger contract: recurring windows are ledger windows.
- Layer: testing
- Language: py
- Symbols:
  - `_dir` (function, line 16) `def _dir(tmp_path)`
  - `test_key_from_command_normalises_addon_surfaces` (function, line 23) `def test_key_from_command_normalises_addon_surfaces()`
  - `test_plain_verbs_key_by_first_token` (function, line 32) `def test_plain_verbs_key_by_first_token()`
  - `test_record_and_fresh_within_window` (function, line 38) `def test_record_and_fresh_within_window(tmp_path)`
  - `test_ttl_windows_are_verb_specific` (function, line 45) `def test_ttl_windows_are_verb_specific(tmp_path)`
  - `test_stale_first_orders_unknown_then_oldest` (function, line 55) `def test_stale_first_orders_unknown_then_oldest(tmp_path)`
  - `test_corrupt_store_fails_open` (function, line 64) `def test_corrupt_store_fails_open(tmp_path)`
  - `test_routing_sink_records_terminal_outcomes` (function, line 74) `def test_routing_sink_records_terminal_outcomes(tmp_path, monkeypatch)`
  - `test_planner_skips_fresh_addon_proposals` (function, line 103) `def test_planner_skips_fresh_addon_proposals(tmp_path, monkeypatch)`
  - `_PlannerStub` (class, line 117) `class _PlannerStub(Planner)`
  - `__init__` (method, line 120) `def __init__(self)`
- Depends on: `modules/__init__.py`, `modules/lazy_ledger.py`, `modules/lazy_loop.py`, `modules/outcome_bus.py`, `modules/sinks/__init__.py`


Next: [KB_tests_p14.md](KB_tests_p14.md)
