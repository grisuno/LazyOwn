# Subsystem: tests (page 19 of 28)
Previous: [KB_tests_p18.md](KB_tests_p18.md)

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
  - `test_listing_noise_flags_recursive_session_dump` (function, line 152) `def test_listing_noise_flags_recursive_session_dump()`
  - `test_listing_noise_ignores_real_postexp_find_output` (function, line 161) `def test_listing_noise_ignores_real_postexp_find_output()`
  - `test_listing_noise_ignores_small_and_banner_outputs` (function, line 170) `def test_listing_noise_ignores_small_and_banner_outputs()`
  - `test_listing_policy_vetoes_ls_family` (function, line 181) `def test_listing_policy_vetoes_ls_family()`
  - `test_listing_policy_allows_find_with_filters_and_work` (function, line 190) `def test_listing_policy_allows_find_with_filters_and_work()`
  - `test_listing_policy_rejects_bare_find` (function, line 199) `def test_listing_policy_rejects_bare_find()`
  - `_work` (function, line 75) `def _work()`
  - `_work` (function, line 99) `def _work()`
- Depends on: `modules/loop_guardrails.py`

## tests/test_loop_idempotent_retest.py
- Doc: Idempotent retest + effect lock: exploitation verbs are verified, not replayed.
- Layer: testing
- Language: py
- Symbols:
  - `_sandbox` (function, line 17) `def _sandbox(tmp_path, monkeypatch)`
  - `test_is_exploit_command_recognizes_access_verbs` (function, line 24) `def test_is_exploit_command_recognizes_access_verbs()`
  - `test_exploit_target_prefers_command_then_text` (function, line 34) `def test_exploit_target_prefers_command_then_text()`
  - `test_session_verdict_passthrough_for_non_exploit` (function, line 44) `def test_session_verdict_passthrough_for_non_exploit(tmp_path, monkeypatch)`
  - `test_exploit_finding_not_replayed_without_session` (function, line 53) `def test_exploit_finding_not_replayed_without_session(tmp_path, monkeypatch)`
  - `test_exploit_finding_verified_via_live_session` (function, line 73) `def test_exploit_finding_verified_via_live_session(tmp_path, monkeypatch)`
  - `test_claim_effect_dedupes_by_target_vector` (function, line 98) `def test_claim_effect_dedupes_by_target_vector()`
  - `test_claim_effect_fail_open_on_empty` (function, line 111) `def test_claim_effect_fail_open_on_empty()`
  - `test_probe_live_shell_no_session_returns_none` (function, line 117) `def test_probe_live_shell_no_session_returns_none()`
  - `test_terminal_fallback_reuses_live_session` (function, line 123) `def test_terminal_fallback_reuses_live_session(tmp_path, monkeypatch)`
  - `test_terminal_fallback_skips_when_effect_locked` (function, line 145) `def test_terminal_fallback_skips_when_effect_locked(tmp_path, monkeypatch)`
  - `_Node` (class, line 37) `class _Node`
- Depends on: `modules/atomic_exploit_bridge.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/outcome_bus.py`

## tests/test_loop_intel_projection.py
- Doc: graph_state projects known assets, auto-findings carry class/CVE (bugs 2.4, 2.6).
- Layer: testing
- Language: py
- Symbols:
  - `_sandbox` (function, line 17) `def _sandbox(tmp_path, monkeypatch)`
  - `test_derive_finding_class_maps_marks_and_cve` (function, line 24) `def test_derive_finding_class_maps_marks_and_cve()`
  - `test_report_resolves_technique_from_vulnclass` (function, line 32) `def test_report_resolves_technique_from_vulnclass(tmp_path, monkeypatch)`
  - `test_graph_state_projects_known_assets` (function, line 43) `def test_graph_state_projects_known_assets(tmp_path, monkeypatch)`
  - `test_writeback_finding_has_concrete_class_and_name` (function, line 73) `def test_writeback_finding_has_concrete_class_and_name(tmp_path, monkeypatch)`
  - `_Graph` (class, line 47) `class _Graph`
  - `_FindingService` (class, line 78) `class _FindingService`
  - `_Evidence` (class, line 86) `class _Evidence`
  - `_Graph` (class, line 96) `class _Graph`
  - `_Assets` (class, line 114) `class _Assets`
  - `_Traffic` (class, line 118) `class _Traffic`
  - `overview` (method, line 50) `def overview(self)`
  - `__init__` (method, line 79) `def __init__(self)`
  - `report` (method, line 82) `def report(self)`
  - `__init__` (method, line 87) `def __init__(self)`
  - `add` (method, line 90) `def add(self)`
  - `add_node` (method, line 99) `def add_node(self, kind, text)`
  - `add_edge` (method, line 102) `def add_edge(self)`
  - `has_finding` (method, line 105) `def has_finding(self, text)`
  - `anchors_for` (method, line 108) `def anchors_for(self, node_id)`
  - `anchor` (method, line 111) `def anchor(self)`
  - `insert` (method, line 115) `def insert(self)`
  - `read` (method, line 119) `def read(self, _n)`
  - `bind` (method, line 122) `def bind(self)`
- Depends on: `modules/lazy_loop.py`

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

## tests/test_loop_lazymode_first.py
- Doc: Code-mode (lazymode) is the worker's first option.
- Layer: testing
- Language: py
- Symbols:
  - `_result` (function, line 18) `def _result(ok, result, stdout, error, duration)`
  - `worker_env` (function, line 24) `def worker_env(tmp_path, monkeypatch)`
  - `_patch_model` (function, line 53) `def _patch_model(monkeypatch, loop, reply, run_result)`
  - `test_codemode_shell_wins_and_skips_agent` (function, line 61) `def test_codemode_shell_wins_and_skips_agent(worker_env, monkeypatch)`
  - `test_codemode_exploit_without_shell_falls_through` (function, line 82) `def test_codemode_exploit_without_shell_falls_through(worker_env, monkeypatch)`
  - `test_codemode_no_script_falls_through` (function, line 97) `def test_codemode_no_script_falls_through(worker_env, monkeypatch)`
  - `test_codemode_disabled_is_noop` (function, line 114) `def test_codemode_disabled_is_noop(worker_env, monkeypatch)`
  - `test_codemode_recon_owns_on_content` (function, line 129) `def test_codemode_recon_owns_on_content(worker_env, monkeypatch)`
  - `test_execute_tries_codemode_before_agentic` (function, line 149) `def test_execute_tries_codemode_before_agentic(worker_env, monkeypatch)`
- Depends on: `core/config.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `sdk/lazymode/__init__.py`

## tests/test_loop_leases.py
- Doc: Tests for modules.loop.leases.
- Layer: testing
- Language: py
- Symbols:
  - `store` (function, line 13) `def store(tmp_path)`
  - `test_first_claim_wins` (function, line 18) `def test_first_claim_wins(store)`
  - `test_second_claim_while_held_fails` (function, line 25) `def test_second_claim_while_held_fails(store)`
  - `test_settled_intent_never_reclaims` (function, line 30) `def test_settled_intent_never_reclaims(store)`
  - `test_expired_lease_reclaimable` (function, line 37) `def test_expired_lease_reclaimable(store)`
  - `test_expired_claim_freed_by_sweep` (function, line 45) `def test_expired_claim_freed_by_sweep(store)`
  - `test_heartbeat_extends_live_lease_only` (function, line 53) `def test_heartbeat_extends_live_lease_only(store)`
  - `test_release_makes_intent_claimable` (function, line 61) `def test_release_makes_intent_claimable(store)`
  - `test_active_and_counts` (function, line 69) `def test_active_and_counts(store)`
  - `test_independent_tasks_do_not_collide` (function, line 81) `def test_independent_tasks_do_not_collide(store)`
  - `test_cross_process_claim_via_second_connection` (function, line 86) `def test_cross_process_claim_via_second_connection(tmp_path)`
  - `test_threads_do_not_share_connection_state` (function, line 95) `def test_threads_do_not_share_connection_state(store)`
  - `claim` (function, line 98) `def claim(target)`
- Depends on: `modules/loop/leases.py`

## tests/test_loop_leases_integration.py
- Doc: Integration tests: exploration graph claims ride on SQLite leases.
- Layer: testing
- Language: py
- Symbols:
  - `graph` (function, line 11) `def graph(tmp_path, monkeypatch)`
  - `test_claim_acquires_lease` (function, line 25) `def test_claim_acquires_lease(graph)`
  - `test_second_claim_blocked_by_lease` (function, line 33) `def test_second_claim_blocked_by_lease(graph)`
  - `test_settle_on_exhausted_blocks_reclaim` (function, line 40) `def test_settle_on_exhausted_blocks_reclaim(graph)`
  - `test_requeue_releases_lease` (function, line 49) `def test_requeue_releases_lease(graph)`
  - `test_budget_check_includes_token_verdict` (function, line 58) `def test_budget_check_includes_token_verdict(tmp_path, monkeypatch)`
  - `test_token_guard_fail_soft` (function, line 67) `def test_token_guard_fail_soft(tmp_path, monkeypatch)`
  - `test_lease_store_disabled` (function, line 74) `def test_lease_store_disabled(monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/lazy_loop.py`, `modules/loop/__init__.py`

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

## tests/test_loop_manager_outcome.py
- Doc: Loop manager outcome propagation: workspace result.json drives status.
- Layer: testing
- Language: py
- Symbols:
  - `manager` (function, line 12) `def manager(tmp_path)`
  - `_register` (function, line 18) `def _register(manager, loop_id, workspace)`
  - `_FakeProcess` (class, line 48) `class _FakeProcess`
  - `test_read_outcome_parses_result_json` (function, line 56) `def test_read_outcome_parses_result_json(manager, tmp_path)`
  - `test_reap_marks_failed_on_honest_outcome` (function, line 68) `def test_reap_marks_failed_on_honest_outcome(manager, tmp_path)`
  - `test_reap_marks_finished_on_success` (function, line 87) `def test_reap_marks_finished_on_success(manager, tmp_path)`
  - `test_reap_falls_back_to_exit_code_without_outcome` (function, line 103) `def test_reap_falls_back_to_exit_code_without_outcome(manager, tmp_path)`
  - `test_reap_stopped_overrides_outcome` (function, line 116) `def test_reap_stopped_overrides_outcome(manager, tmp_path)`
  - `test_reap_cancelled_outcome_maps_stopped` (function, line 130) `def test_reap_cancelled_outcome_maps_stopped(manager, tmp_path)`
  - `test_spawn_binds_workspace_env` (function, line 145) `def test_spawn_binds_workspace_env(manager, tmp_path, monkeypatch)`
  - `__init__` (method, line 49) `def __init__(self, exit_code)`
  - `wait` (method, line 52) `def wait(self)`
  - `_FakePopen` (class, line 150) `class _FakePopen`
  - `_fake_reap` (function, line 161) `def _fake_reap(self, loop_id, process)`
  - `__init__` (method, line 151) `def __init__(self, argv)`
- Depends on: `modules/__init__.py`

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

## tests/test_loop_planner_bridge.py
- Doc: Tests for the technique-planner to intent-frontier bridge.
- Layer: testing
- Language: py
- Symbols:
  - `test_technique_candidate_summary_with_command` (function, line 10) `def test_technique_candidate_summary_with_command()`
  - `test_technique_candidate_summary_without_command` (function, line 15) `def test_technique_candidate_summary_without_command()`
  - `test_technique_intents_converts_candidates` (function, line 20) `def test_technique_intents_converts_candidates(monkeypatch)`
  - `test_technique_intents_never_raises` (function, line 38) `def test_technique_intents_never_raises(monkeypatch)`
  - `test_bridge_dedupes_existing` (function, line 46) `def test_bridge_dedupes_existing(monkeypatch)`
  - `test_bridge_disabled` (function, line 61) `def test_bridge_disabled(monkeypatch)`
  - `FakePlanner` (class, line 28) `class FakePlanner`
  - `boom` (function, line 39) `def boom()`
  - `plan` (method, line 29) `def plan(self, target, max_candidates)`
- Depends on: `modules/loop/planner_bridge.py`

## tests/test_loop_post_signal.py
- Doc: Post-tool signal is observational, not enforcement (bug 2.3).
- Layer: testing
- Language: py
- Symbols:
  - `test_classify_ignores_benign_timeout_echo` (function, line 19) `def test_classify_ignores_benign_timeout_echo()`
  - `test_classify_still_flags_real_block_and_error` (function, line 30) `def test_classify_still_flags_real_block_and_error()`
  - `test_guard_step_uses_calibrated_classifier_and_post_signal` (function, line 37) `def test_guard_step_uses_calibrated_classifier_and_post_signal()`
  - `test_post_signal_block_does_not_short_circuit_return` (function, line 46) `def test_post_signal_block_does_not_short_circuit_return()`
- Depends on: `modules/intercept.py`, `modules/lazy_loop.py`, `modules/outcome_attribution.py`

## tests/test_loop_preflight.py
- Doc: Target preflight for loops and auto_pwn: lab state and TCP reachability.
- Layer: testing
- Language: py
- Symbols:
  - `test_lab_state_maps_running_and_stopped` (function, line 8) `def test_lab_state_maps_running_and_stopped()`
  - `test_check_target_fails_fast_on_stopped_lab` (function, line 39) `def test_check_target_fails_fast_on_stopped_lab()`
  - `test_check_target_passes_on_running_lab` (function, line 52) `def test_check_target_passes_on_running_lab()`
  - `test_check_target_probes_tcp` (function, line 63) `def test_check_target_probes_tcp(monkeypatch)`
  - `test_check_target_refused_means_alive` (function, line 82) `def test_check_target_refused_means_alive(monkeypatch)`
  - `test_check_target_without_target` (function, line 94) `def test_check_target_without_target()`
  - `test_probe_tcp_real_socket` (function, line 102) `def test_probe_tcp_real_socket()`
  - `test_no_preflight_hint_override` (function, line 128) `def test_no_preflight_hint_override()`
  - `test_preflight_flag_parses` (function, line 136) `def test_preflight_flag_parses()`
  - `_accept` (function, line 110) `def _accept()`
- Depends on: `modules/__init__.py`, `modules/lazy_runner.py`

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

## tests/test_loop_scan_banner_guard.py
- Doc: The scanner-banner guard: a scan that echoes a backdoor's shell prompt in its fingerprint must...
- Layer: testing
- Language: py
- Symbols:
  - `_intent` (function, line 30) `def _intent(node_id)`
  - `_worker` (function, line 35) `def _worker(task_id)`
  - `sink_log` (function, line 43) `def sink_log()`
  - `TestScanOnlyVerb` (class, line 65) `class TestScanOnlyVerb`
  - `TestScanBannerGuard` (class, line 98) `class TestScanBannerGuard`
  - `fake_record` (function, line 50) `def fake_record()`
  - `test_scanners_are_scan_only` (method, line 66) `def test_scanners_are_scan_only(self)`
  - `test_interactive_shell_verbs_are_not_scan_only` (method, line 81) `def test_interactive_shell_verbs_are_not_scan_only(self)`
  - `test_detector_fires_on_the_nmap_banner` (method, line 99) `def test_detector_fires_on_the_nmap_banner(self)`
  - `test_scan_banner_never_publishes_a_shell` (method, line 107) `def test_scan_banner_never_publishes_a_shell(self, sink_log)`
  - `test_real_nc_shell_still_publishes` (method, line 117) `def test_real_nc_shell_still_publishes(self, sink_log)`
- Depends on: `modules/__init__.py`, `modules/atomic_exploit_bridge.py`, `modules/lazy_loop.py`, `modules/outcome_bus.py`

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

## tests/test_loop_technique_deterministic.py
- Doc: Technique intents resolve deterministically, not via the model.
- Layer: testing
- Language: py
- Symbols:
  - `test_technique_intent_classification` (function, line 14) `def test_technique_intent_classification()`
  - `test_technique_steps_are_headless` (function, line 25) `def test_technique_steps_are_headless()`
  - `worker_env` (function, line 39) `def worker_env(tmp_path, monkeypatch)`
  - `test_steps_for_resolves_technique` (function, line 65) `def test_steps_for_resolves_technique(worker_env)`
  - `test_technique_deterministic_step_when_steps_run` (function, line 73) `def test_technique_deterministic_step_when_steps_run(worker_env, monkeypatch)`
  - `test_execute_uses_model_for_nontechnique` (function, line 95) `def test_execute_uses_model_for_nontechnique(worker_env, monkeypatch)`
  - `_executor` (function, line 86) `def _executor(command)`
  - `_agentic` (function, line 102) `def _agentic()`
- Depends on: `core/config.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`


Next: [KB_tests_p20.md](KB_tests_p20.md)
