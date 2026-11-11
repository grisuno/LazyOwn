# Subsystem: tests (page 17 of 25)
Previous: [KB_tests_p16.md](KB_tests_p16.md)

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
  - `test_raw_llm_recording_carries_task_and_model` (function, line 190) `def test_raw_llm_recording_carries_task_and_model(tmp_path, monkeypatch)`
  - `test_llm_context_budget_roundtrip` (function, line 213) `def test_llm_context_budget_roundtrip(tmp_path, monkeypatch)`
  - `test_planner_uses_bound_task_chain` (function, line 225) `def test_planner_uses_bound_task_chain(tmp_path, monkeypatch)`
  - `scripted` (function, line 23) `def scripted(model, prompt, max_tokens)`
  - `first_empty_then_ok` (function, line 42) `def first_empty_then_ok(model, prompt, max_tokens)`
  - `error_then_ok` (function, line 61) `def error_then_ok(model, prompt, max_tokens)`
  - `scripted` (function, line 79) `def scripted(model, prompt, max_tokens)`
  - `scripted` (function, line 147) `def scripted(model, prompt, max_tokens)`
  - `scripted_next` (function, line 160) `def scripted_next(model, prompt, max_tokens)`
  - `scripted` (function, line 236) `def scripted(model, prompt, max_tokens)`
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

## tests/test_loop_objective_wiring.py
- Doc: Loop wiring fidelity: objective queue and Hermes draft consumption.
- Layer: testing
- Language: py
- Symbols:
  - `_patched_engine` (function, line 14) `def _patched_engine(tmp_path, monkeypatch)`
  - `_point_objectives` (function, line 25) `def _point_objectives(tmp_path, monkeypatch)`
  - `_write_objective` (function, line 37) `def _write_objective(path, objective_id, text, status, priority, target)`
  - `_statuses` (function, line 51) `def _statuses(path)`
  - `test_pending_objectives_filters_by_target_and_priority` (function, line 61) `def test_pending_objectives_filters_by_target_and_priority(tmp_path, monkeypatch)`
  - `test_planner_emits_and_claims_injected_objective` (function, line 77) `def test_planner_emits_and_claims_injected_objective(tmp_path, monkeypatch)`
  - `test_settle_marks_done_when_intent_done` (function, line 95) `def test_settle_marks_done_when_intent_done(tmp_path, monkeypatch)`
  - `test_settle_requeues_when_intent_unfinished` (function, line 112) `def test_settle_requeues_when_intent_unfinished(tmp_path, monkeypatch)`
  - `test_drain_drafts_imports_pending_draft_as_task` (function, line 128) `def test_drain_drafts_imports_pending_draft_as_task(tmp_path, monkeypatch)`
  - `test_drain_drafts_is_idempotent` (function, line 153) `def test_drain_drafts_is_idempotent(tmp_path, monkeypatch)`
  - `test_daemon_drain_drafts_helper_is_safe_without_engine` (function, line 172) `def test_daemon_drain_drafts_helper_is_safe_without_engine()`
  - `test_daemon_drain_drafts_imports_pending_draft` (function, line 179) `def test_daemon_drain_drafts_imports_pending_draft(tmp_path, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/lazy_drafts.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`

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

## tests/test_loop_target_authority.py
- Doc: Target authority: --target rebinds payload rhost and scope.
- Layer: testing
- Language: py
- Symbols:
  - `_FakeShell` (class, line 16) `class _FakeShell`
  - `test_single_target_replaces_rhost_and_scope` (function, line 31) `def test_single_target_replaces_rhost_and_scope()`
  - `test_multi_target_scope_is_every_target` (function, line 42) `def test_multi_target_scope_is_every_target()`
  - `test_dedupes_and_strips` (function, line 49) `def test_dedupes_and_strips()`
  - `test_noop_when_already_bound` (function, line 55) `def test_noop_when_already_bound()`
  - `test_enforcement_mode_untouched` (function, line 62) `def test_enforcement_mode_untouched()`
  - `test_empty_targets_is_noop` (function, line 68) `def test_empty_targets_is_noop()`
  - `test_fallback_writer_without_scope_save` (function, line 75) `def test_fallback_writer_without_scope_save(monkeypatch)`
  - `__init__` (method, line 19) `def __init__(self, params)`
  - `_scope_save` (method, line 23) `def _scope_save(self, entries, mode)`
  - `_fake_save` (function, line 78) `def _fake_save(params)`
  - `_Bare` (class, line 83) `class _Bare`
  - `__init__` (method, line 84) `def __init__(self)`
- Depends on: `modules/lazy_runner.py`

## tests/test_loop_trigger_hints.py
- Doc: BDD for the cve_hot trigger hint fingerprints.
- Layer: testing
- Language: py
- Symbols:
  - `_Graph` (class, line 29) `class _Graph`
  - `_Assets` (class, line 42) `class _Assets`
  - `trigger_env` (function, line 56) `def trigger_env(tmp_path, monkeypatch)`
  - `test_cve_hot_hint_proposed_once_per_signature` (function, line 78) `def test_cve_hot_hint_proposed_once_per_signature(trigger_env)`
  - `test_changed_banner_refires_the_hint` (function, line 90) `def test_changed_banner_refires_the_hint(tmp_path, monkeypatch)`
  - `test_hint_fingerprint_normalizes_product_and_version` (function, line 118) `def test_hint_fingerprint_normalizes_product_and_version()`
  - `test_prune_drops_expired_fingerprints` (function, line 128) `def test_prune_drops_expired_fingerprints()`
  - `test_hint_ttl_expires_and_refires` (function, line 137) `def test_hint_ttl_expires_and_refires(tmp_path, monkeypatch)`
  - `test_hint_store_written_under_loop_stores` (function, line 158) `def test_hint_store_written_under_loop_stores(tmp_path, monkeypatch)`
  - `__init__` (method, line 32) `def __init__(self)`
  - `add_node` (method, line 35) `def add_node(self, kind, text, state, priority, meta)`
  - `list` (method, line 38) `def list(self)`
  - `__init__` (method, line 45) `def __init__(self, value)`
  - `list` (method, line 49) `def list(self, kind)`
  - `fake_hot_matches` (function, line 65) `def fake_hot_matches(services, allow_network)`
  - `fake_hot_matches` (function, line 100) `def fake_hot_matches(services, allow_network)`
- Depends on: `modules/lazy_loop.py`, `modules/loop_triggers.py`, `modules/world_model.py`

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

## tests/test_marketplace_config.py
- Doc: Marketplace registry and settings: formats, toggles, CRUD.
- Layer: testing
- Language: py
- Symbols:
  - `_registry` (function, line 12) `def _registry(tmp_path, monkeypatch)`
  - `test_tool_rows_use_json_and_active_key` (function, line 33) `def test_tool_rows_use_json_and_active_key(tmp_path, monkeypatch)`
  - `test_plugin_rows_skip_lua_and_templates` (function, line 61) `def test_plugin_rows_skip_lua_and_templates(tmp_path, monkeypatch)`
  - `test_read_only_tabs_never_toggle_or_delete` (function, line 76) `def test_read_only_tabs_never_toggle_or_delete(tmp_path, monkeypatch)`
  - `test_create_and_delete_across_tabs` (function, line 89) `def test_create_and_delete_across_tabs(tmp_path, monkeypatch)`
  - `test_settings_toggle_tracks_only_success` (function, line 105) `def test_settings_toggle_tracks_only_success(tmp_path, monkeypatch)`
  - `test_marketplace_app_filters_rows` (function, line 118) `def test_marketplace_app_filters_rows(tmp_path, monkeypatch)`
  - `test_filter_input_keeps_printable_keys` (function, line 145) `def test_filter_input_keeps_printable_keys(tmp_path, monkeypatch)`
  - `_drive` (function, line 128) `def _drive()`
  - `_drive` (function, line 151) `def _drive()`
- Depends on: `cli/__init__.py`

## tests/test_mcp_auto_loop_wrapper.py
- Doc: MCP auto_loop wrapper contract: one orchestrator, no dual engines.
- Layer: testing
- Language: py
- Symbols:
  - `_patched` (function, line 16) `def _patched(monkeypatch, tmp_path)`
  - `test_fast_path_runs_the_engine` (function, line 76) `def test_fast_path_runs_the_engine(monkeypatch, tmp_path)`
  - `test_legacy_flag_annotates_but_routes_fast` (function, line 90) `def test_legacy_flag_annotates_but_routes_fast(monkeypatch, tmp_path)`
  - `test_engine_failure_surfaces` (function, line 100) `def test_engine_failure_surfaces(monkeypatch, tmp_path)`
  - `_text` (function, line 110) `def _text(response)`
  - `loop_join` (function, line 125) `def loop_join(coro)`
  - `_FakeEngine` (class, line 44) `class _FakeEngine`
  - `_Boom` (class, line 31) `class _Boom`
  - `__init__` (method, line 45) `def __init__(self)`
  - `create_task` (method, line 50) `def create_task(self, goal)`
  - `ensure_target` (method, line 54) `def ensure_target(self, task_id, target, reason)`
  - `run` (method, line 58) `def run(self, task_id, max_rounds, workers, timeout_sec)`
  - `__init__` (method, line 32) `def __init__(self)`
- Depends on: `modules/lazy_loop.py`, `skills/lazyown_mcp.py`

## tests/test_mcp_dispatch.py
- Doc: call_tool dispatches through the handler registry.
- Layer: testing
- Language: py
- Symbols:
  - `_package_names` (function, line 29) `def _package_names()`
  - `_registered` (function, line 33) `def _registered()`
  - `_fallback_branches` (function, line 50) `def _fallback_branches()`
  - `TestRegistryDispatch` (class, line 61) `class TestRegistryDispatch`
  - `test_set_config_refuses_null_values` (function, line 79) `def test_set_config_refuses_null_values()`
  - `test_new_chain_shell_tools_have_defs_and_handlers` (function, line 99) `def test_new_chain_shell_tools_have_defs_and_handlers()`
  - `test_opencode_bridge_curates_loop_and_chain` (function, line 106) `def test_opencode_bridge_curates_loop_and_chain()`
  - `test_mcp_never_offers_interactive_repl` (function, line 121) `def test_mcp_never_offers_interactive_repl()`
  - `test_no_dead_duplicate_branches` (method, line 62) `def test_no_dead_duplicate_branches(self)`
  - `test_migrated_handlers_registered` (method, line 66) `def test_migrated_handlers_registered(self)`
  - `test_migrated_handlers_absent_from_fallback` (method, line 71) `def test_migrated_handlers_absent_from_fallback(self)`

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

## tests/test_mcp_tools_registry.py
- Doc: Contract for the one-file-per-tool MCP registry (``skills/mcp_tools``).
- Layer: testing
- Language: py
- Symbols:
  - `_registry_names` (function, line 26) `def _registry_names()`
  - `_legacy_schema_names` (function, line 30) `def _legacy_schema_names()`
  - `_legacy_handler_names` (function, line 45) `def _legacy_handler_names()`
  - `TestRegistryDiscovery` (class, line 62) `class TestRegistryDiscovery`
  - `TestSingleOwnership` (class, line 93) `class TestSingleOwnership`
  - `TestImportPurity` (class, line 103) `class TestImportPurity`
  - `test_reference_tool_discovered` (method, line 63) `def test_reference_tool_discovered(self)`
  - `test_register_handlers_populates_table` (method, line 66) `def test_register_handlers_populates_table(self)`
  - `test_no_duplicate_schema` (method, line 94) `def test_no_duplicate_schema(self)`
  - `test_no_duplicate_handler` (method, line 98) `def test_no_duplicate_handler(self)`
  - `test_tool_modules_do_not_import_runtime` (method, line 104) `def test_tool_modules_do_not_import_runtime(self)`
- Depends on: `skills/mcp_tools/_context.py`

## tests/test_mediation.py
- Doc: Mediator pattern contract tests for the mediation package.
- Layer: testing
- Language: py
- Symbols:
  - `TestHubRouting` (class, line 19) `class TestHubRouting`
  - `TestIntelMediatorActivityPort` (class, line 39) `class TestIntelMediatorActivityPort`
  - `TestFeedbackMediator` (class, line 62) `class TestFeedbackMediator`
  - `TestTelemetryMediator` (class, line 82) `class TestTelemetryMediator`
  - `TestChainMediatorLlmPort` (class, line 170) `class TestChainMediatorLlmPort`
  - `test_all_default_domains_registered` (method, line 22) `def test_all_default_domains_registered(self)`
  - `test_unknown_domain_returns_none` (method, line 27) `def test_unknown_domain_returns_none(self)`
  - `test_singleton_hub_shared` (method, line 30) `def test_singleton_hub_shared(self)`
  - `test_mediation_contract_shape` (method, line 33) `def test_mediation_contract_shape(self)`
  - `test_activity_records_via_injected_port` (method, line 42) `def test_activity_records_via_injected_port(self)`
  - `test_activity_records_fallback_graceful` (method, line 48) `def test_activity_records_fallback_graceful(self)`
  - `test_mask_and_stack_survive_missing_peers` (method, line 52) `def test_mask_and_stack_survive_missing_peers(self, monkeypatch)`
  - `test_order_steps_passthrough_on_error` (method, line 65) `def test_order_steps_passthrough_on_error(self, monkeypatch)`
  - `test_order_steps_forwarded` (method, line 75) `def test_order_steps_forwarded(self, monkeypatch)`
  - `test_publish_event_default_severity_positional` (method, line 85) `def test_publish_event_default_severity_positional(self, monkeypatch)`
  - `test_publish_event_forwarding_calls_default_path` (method, line 95) `def test_publish_event_forwarding_calls_default_path(self, monkeypatch)`
  - `test_rl_select_graceful_off` (method, line 105) `def test_rl_select_graceful_off(self, monkeypatch)`
  - `test_assess_opsec_forwards_to_bridge` (method, line 114) `def test_assess_opsec_forwards_to_bridge(self, monkeypatch)`
  - `test_assess_opsec_graceful_on_bridge_failure` (method, line 121) `def test_assess_opsec_graceful_on_bridge_failure(self, monkeypatch)`
  - `test_record_outcome_quality_forwards_to_bridge` (method, line 130) `def test_record_outcome_quality_forwards_to_bridge(self, monkeypatch)`
  - `test_record_outcome_quality_graceful_on_bridge_failure` (method, line 144) `def test_record_outcome_quality_graceful_on_bridge_failure(self, monkeypatch)`
  - `test_tool_class_yields_forwards_to_bridge` (method, line 153) `def test_tool_class_yields_forwards_to_bridge(self, monkeypatch)`
  - `test_tool_class_yields_graceful_on_bridge_failure` (method, line 160) `def test_tool_class_yields_graceful_on_bridge_failure(self, monkeypatch)`
  - `test_port_contract` (method, line 173) `def test_port_contract(self)`
  - `test_register_llm_port_replaces` (method, line 181) `def test_register_llm_port_replaces(self)`
  - `_patch_hub` (method, line 194) `def _patch_hub(self, monkeypatch, port)`
  - `test_recovery_pool_absent_returns_empty` (method, line 214) `def test_recovery_pool_absent_returns_empty(self, monkeypatch)`
  - `test_recovery_pool_builds_steps` (method, line 236) `def test_recovery_pool_builds_steps(self, monkeypatch)`
  - `test_recovery_prompt_carries_recent_changes` (method, line 262) `def test_recovery_prompt_carries_recent_changes(self, monkeypatch, tmp_path)`
  - `boom` (function, line 68) `def boom(steps, stack)`
  - `boom` (function, line 108) `def boom()`
  - `boom` (function, line 124) `def boom()`
  - `boom` (function, line 147) `def boom()`
  - `boom` (function, line 163) `def boom()`
  - `Fake` (class, line 182) `class Fake`
  - `_FakeHub` (class, line 197) `class _FakeHub`
  - `_NoLock` (class, line 204) `class _NoLock`
  - `Empty` (class, line 217) `class Empty`
  - `FakePort` (class, line 239) `class FakePort`
  - `FakePort` (class, line 280) `class FakePort`
  - `complete` (method, line 183) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 186) `def has_members(self)`
  - `__init__` (method, line 198) `def __init__(self, port)`
  - `mediator_for` (method, line 201) `def mediator_for(self, domain)`
  - `__enter__` (method, line 205) `def __enter__(self)`
  - `__exit__` (method, line 208) `def __exit__(self)`
  - `complete` (method, line 218) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 221) `def has_members(self)`
  - `complete` (method, line 240) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 243) `def has_members(self)`
  - `complete` (method, line 281) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 285) `def has_members(self)`
- Depends on: `cli/__init__.py`, `modules/chain_runner.py`, `modules/lazy_intel.py`, `modules/lazy_orchestrator_feedback.py`, `modules/lazy_world_diff.py`, `modules/loop_ai_bridge.py`, `modules/mediation/__init__.py`, `modules/mediation/hub.py`


Next: [KB_tests_p18.md](KB_tests_p18.md)
