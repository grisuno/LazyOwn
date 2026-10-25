# Symbols (page 37 of 45)
Previous: [SYMBOLS_p36.md](SYMBOLS_p36.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `TestNotificationBroadcaster` | class | `tests/test_engage_orchestrator.py:139` | `class TestNotificationBroadcaster` |
| `TestShellObtainedPublisher` | class | `tests/test_engage_orchestrator.py:191` | `class TestShellObtainedPublisher` |
| `TestStaticFallbackResolver` | class | `tests/test_engage_orchestrator.py:451` | `class TestStaticFallbackResolver` |
| `TestStdinApprovalSink` | class | `tests/test_engage_orchestrator.py:431` | `class TestStdinApprovalSink` |
| `TestWiring` | class | `tests/test_engage_orchestrator.py:676` | `class TestWiring` |
| `_BoomSink` | class | `tests/test_engage_orchestrator.py:165` | `class _BoomSink(INotificationSink)` |
| `_CountingSink` | class | `tests/test_engage_orchestrator.py:145` | `class _CountingSink(INotificationSink)` |
| `_GoodSink` | class | `tests/test_engage_orchestrator.py:173` | `class _GoodSink(INotificationSink)` |
| `_NoOpGate` | class | `tests/test_engage_orchestrator.py:497` | `class _NoOpGate` |
| `_RecordingSink` | class | `tests/test_engage_orchestrator.py:280` | `class _RecordingSink` |
| `_RejectingGate` | class | `tests/test_engage_orchestrator.py:508` | `class _RejectingGate` |
| `_ScriptedRunner` | class | `tests/test_engage_orchestrator.py:473` | `class _ScriptedRunner` |
| `__init__` | method | `tests/test_engage_orchestrator.py:146` | `def __init__(self, name)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:283` | `def __init__(self)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:481` | `def __init__(self, scripted)` |
| `__init__` | method | `tests/test_engage_orchestrator.py:509` | `def __init__(self, rejected_phase)` |
| `_injected_sleep` | function | `tests/test_engage_orchestrator.py:330` | `def _injected_sleep(_seconds)` |
| `announce` | method | `tests/test_engage_orchestrator.py:287` | `def announce(self, request)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:153` | `def deliver(self, event)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:170` | `def deliver(self, event)` |
| `deliver` | method | `tests/test_engage_orchestrator.py:178` | `def deliver(self, event)` |
| `name` | method | `tests/test_engage_orchestrator.py:150` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:167` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:175` | `def name(self)` |
| `name` | method | `tests/test_engage_orchestrator.py:493` | `def name(self)` |
| `policy_module` | function | `tests/test_engage_orchestrator.py:270` | `def policy_module(temp_sessions, monkeypatch)` |
| `request` | method | `tests/test_engage_orchestrator.py:498` | `def request(self, target, phase, command, reason)` |
| `request` | method | `tests/test_engage_orchestrator.py:512` | `def request(self, target, phase, command, reason)` |
| `resolution_for` | method | `tests/test_engage_orchestrator.py:290` | `def resolution_for(self, approval_id)` |
| `run` | method | `tests/test_engage_orchestrator.py:485` | `def run(self, command, timeout)` |
| `temp_sessions` | function | `tests/test_engage_orchestrator.py:47` | `def temp_sessions(tmp_path, monkeypatch)` |
| `test_accepts_hostname` | method | `tests/test_engage_orchestrator.py:248` | `def test_accepts_hostname(self)` |
| `test_accepts_ipv4` | method | `tests/test_engage_orchestrator.py:242` | `def test_accepts_ipv4(self)` |
| `test_announce_writes_pending_record` | method | `tests/test_engage_orchestrator.py:386` | `def test_announce_writes_pending_record(self, policy_module, temp_sessions)` |
| `test_approval_gate_defaults_to_true_when_key_missing` | method | `tests/test_engage_orchestrator.py:708` | `def test_approval_gate_defaults_to_true_when_key_missing(self, tmp_path)` |
| `test_auto_approve_true_returns_approved_for_gated_phase` | method | `tests/test_engage_orchestrator.py:295` | `def test_auto_approve_true_returns_approved_for_gated_phase(self, policy_module, temp_sessions)` |
| `test_client_id_is_sanitised` | method | `tests/test_engage_orchestrator.py:223` | `def test_client_id_is_sanitised(self, temp_sessions)` |
| `test_daemon_has_engage_subcommand` | method | `tests/test_engage_orchestrator.py:698` | `def test_daemon_has_engage_subcommand(self)` |
| `test_denied_step_is_skipped` | method | `tests/test_engage_orchestrator.py:585` | `def test_denied_step_is_skipped(self, temp_sessions, policy_module)` |
| `test_do_engage_method_exists_in_lazyown` | method | `tests/test_engage_orchestrator.py:677` | `def test_do_engage_method_exists_in_lazyown(self)` |
| `test_engage_approve_accepts_valid_decision` | method | `tests/test_engage_orchestrator.py:662` | `def test_engage_approve_accepts_valid_decision(self, temp_sessions, policy_module)` |
| `test_engage_approve_rejects_bad_decision` | method | `tests/test_engage_orchestrator.py:656` | `def test_engage_approve_rejects_bad_decision(self, temp_sessions, policy_module)` |
| `test_engage_status_returns_pending_approvals_structure` | method | `tests/test_engage_orchestrator.py:648` | `def test_engage_status_returns_pending_approvals_structure(self, temp_sessions, policy_module)` |
| `test_engage_target_rejects_invalid` | method | `tests/test_engage_orchestrator.py:633` | `def test_engage_target_rejects_invalid(self, temp_sessions, policy_module)` |
| `test_engage_target_returns_engagement_id` | method | `tests/test_engage_orchestrator.py:639` | `def test_engage_target_returns_engagement_id(self, temp_sessions, policy_module)` |
| `test_engagement_hooks_module_exposes_public_surface` | method | `tests/test_engage_orchestrator.py:726` | `def test_engagement_hooks_module_exposes_public_surface(self)` |
| `test_failing_sink_does_not_break_broadcaster` | method | `tests/test_engage_orchestrator.py:162` | `def test_failing_sink_does_not_break_broadcaster(self, temp_sessions)` |
| `test_fans_out_to_every_sink` | method | `tests/test_engage_orchestrator.py:140` | `def test_fans_out_to_every_sink(self, temp_sessions)` |
| `test_first_call_emits_event` | method | `tests/test_engage_orchestrator.py:192` | `def test_first_call_emits_event(self, temp_sessions)` |
| `test_gated_phase_times_out_to_denied` | method | `tests/test_engage_orchestrator.py:356` | `def test_gated_phase_times_out_to_denied(self, policy_module, temp_sessions)` |
| `test_gated_phase_with_auto_approve_false_polls_sink` | method | `tests/test_engage_orchestrator.py:326` | `def test_gated_phase_with_auto_approve_false_polls_sink(self, policy_module, temp_sessions)` |
| `test_invalid_client_id_returns_none` | method | `tests/test_engage_orchestrator.py:217` | `def test_invalid_client_id_returns_none(self, temp_sessions)` |
| `test_invalid_payload_defaults_to_auto_approve_true` | method | `tests/test_engage_orchestrator.py:375` | `def test_invalid_payload_defaults_to_auto_approve_true(self, policy_module, temp_sessions)` |
| `test_lazyc2_has_engagement_hook_call` | method | `tests/test_engage_orchestrator.py:684` | `def test_lazyc2_has_engagement_hook_call(self)` |
| `test_mcp_exposes_four_engage_tools` | method | `tests/test_engage_orchestrator.py:688` | `def test_mcp_exposes_four_engage_tools(self)` |
| `test_narrate_writes_log_and_audit` | method | `tests/test_engage_orchestrator.py:87` | `def test_narrate_writes_log_and_audit(self, temp_sessions)` |
| `test_no_tty_returns_none` | method | `tests/test_engage_orchestrator.py:432` | `def test_no_tty_returns_none(self, policy_module)` |
| `test_non_gated_phase_bypasses_sink` | method | `tests/test_engage_orchestrator.py:310` | `def test_non_gated_phase_bypasses_sink(self, policy_module, temp_sessions)` |
| `test_payload_json_auto_approve_key_is_bool_when_present` | method | `tests/test_engage_orchestrator.py:703` | `def test_payload_json_auto_approve_key_is_bool_when_present(self)` |
| `test_policy_module_exposes_approval_surface` | method | `tests/test_engage_orchestrator.py:740` | `def test_policy_module_exposes_approval_surface(self)` |
| `test_rejects_garbage` | method | `tests/test_engage_orchestrator.py:254` | `def test_rejects_garbage(self)` |
| `test_rejects_invalid_target` | method | `tests/test_engage_orchestrator.py:529` | `def test_rejects_invalid_target(self, temp_sessions, policy_module)` |
| `test_render_line_format_is_stable` | method | `tests/test_engage_orchestrator.py:123` | `def test_render_line_format_is_stable(self)` |
| `test_repeat_call_is_idempotent` | method | `tests/test_engage_orchestrator.py:209` | `def test_repeat_call_is_idempotent(self, temp_sessions)` |
| `test_resolution_returns_latest_non_pending` | method | `tests/test_engage_orchestrator.py:402` | `def test_resolution_returns_latest_non_pending(self, policy_module, temp_sessions)` |
| `test_returns_alternatives_in_order` | method | `tests/test_engage_orchestrator.py:452` | `def test_returns_alternatives_in_order(self)` |
| `test_runs_full_plan_on_success` | method | `tests/test_engage_orchestrator.py:535` | `def test_runs_full_plan_on_success(self, temp_sessions, policy_module)` |
| `test_shell_indicator_stops_loop` | method | `tests/test_engage_orchestrator.py:609` | `def test_shell_indicator_stops_loop(self, temp_sessions, policy_module)` |
| `test_stream_sink_appends_to_autonomous_events` | method | `tests/test_engage_orchestrator.py:112` | `def test_stream_sink_appends_to_autonomous_events(self, temp_sessions)` |
| `test_switches_tool_on_failure` | method | `tests/test_engage_orchestrator.py:559` | `def test_switches_tool_on_failure(self, temp_sessions, policy_module)` |
| `test_unknown_primary_returns_none` | method | `tests/test_engage_orchestrator.py:462` | `def test_unknown_primary_returns_none(self)` |
| `_step` | function | `tests/test_engage_summary.py:45` | `def _step(command)` |
| `test_detail_for_empty_search_is_honest` | function | `tests/test_engage_summary.py:76` | `def test_detail_for_empty_search_is_honest()` |
| `test_detail_for_ping_extracts_os` | function | `tests/test_engage_summary.py:62` | `def test_detail_for_ping_extracts_os()` |
| `test_detail_for_populate_extracts_services` | function | `tests/test_engage_summary.py:69` | `def test_detail_for_populate_extracts_services()` |
| `test_full_output_prefers_evidence` | function | `tests/test_engage_summary.py:104` | `def test_full_output_prefers_evidence(tmp_path)` |
| `test_held_scan_ports_reads_xml` | function | `tests/test_engage_summary.py:82` | `def test_held_scan_ports_reads_xml(tmp_path)` |
| `test_marker_lines_drop_panels_and_bars` | function | `tests/test_engage_summary.py:54` | `def test_marker_lines_drop_panels_and_bars()` |
| `test_render_markdown_lists_evidence_and_next` | function | `tests/test_engage_summary.py:125` | `def test_render_markdown_lists_evidence_and_next()` |
| `test_render_text_shows_skip_with_held_ports` | function | `tests/test_engage_summary.py:91` | `def test_render_text_shows_skip_with_held_ports(tmp_path)` |
| `test_write_report_persists_markdown` | function | `tests/test_engage_summary.py:114` | `def test_write_report_persists_markdown(tmp_path)` |
| `TestCuriosityEngine` | class | `tests/test_engagement_and_ping.py:177` | `class TestCuriosityEngine` |
| `TestEngagementState` | class | `tests/test_engagement_and_ping.py:58` | `class TestEngagementState` |
| `TestPingOsId` | class | `tests/test_engagement_and_ping.py:283` | `class TestPingOsId` |
| `TestRecommendNextCommandIndex` | class | `tests/test_engagement_and_ping.py:351` | `class TestRecommendNextCommandIndex` |
| `TestVRIScheduler` | class | `tests/test_engagement_and_ping.py:105` | `class TestVRIScheduler` |
| `_build_csv` | method | `tests/test_engagement_and_ping.py:366` | `def _build_csv(self, tmp_path, run_cmds)` |
| `_build_index` | method | `tests/test_engagement_and_ping.py:354` | `def _build_index(self, tmp_path, phase, n_cmds)` |
| `_command_location` | function | `tests/test_engagement_and_ping.py:30` | `def _command_location(name)` |
| `_extract_os_id_from_json` | method | `tests/test_engagement_and_ping.py:292` | `def _extract_os_id_from_json(self, data)` |
| `_make_params` | method | `tests/test_engagement_and_ping.py:289` | `def _make_params(self)` |
| `_make_state` | method | `tests/test_engagement_and_ping.py:178` | `def _make_state(self, seen)` |
| `_minimal_index` | method | `tests/test_engagement_and_ping.py:186` | `def _minimal_index(self, phase_cmds)` |
| `_ping_stdout` | method | `tests/test_engagement_and_ping.py:286` | `def _ping_stdout(self, ttl)` |
| `test_atomic_write_leaves_no_tmp_file` | method | `tests/test_engagement_and_ping.py:90` | `def test_atomic_write_leaves_no_tmp_file(self, tmp_path)` |
| `test_commands_seen_accumulates_across_calls` | method | `tests/test_engagement_and_ping.py:254` | `def test_commands_seen_accumulates_across_calls(self, tmp_path)` |
| `test_curiosity_does_not_repeat_in_session` | method | `tests/test_engagement_and_ping.py:202` | `def test_curiosity_does_not_repeat_in_session(self, capsys)` |
| `test_curiosity_shows_undiscovered_command` | method | `tests/test_engagement_and_ping.py:192` | `def test_curiosity_shows_undiscovered_command(self, capsys)` |
| `test_curiosity_silent_for_unknown_phase` | method | `tests/test_engagement_and_ping.py:245` | `def test_curiosity_silent_for_unknown_phase(self, capsys)` |
| `test_curiosity_silent_when_all_discovered` | method | `tests/test_engagement_and_ping.py:219` | `def test_curiosity_silent_when_all_discovered(self, capsys)` |
| `test_curiosity_silent_when_disabled` | method | `tests/test_engagement_and_ping.py:229` | `def test_curiosity_silent_when_disabled(self, capsys)` |
| `test_fallback_message_present` | method | `tests/test_engagement_and_ping.py:517` | `def test_fallback_message_present(self)` |
| `test_load_fresh_state_has_zero_commands` | method | `tests/test_engagement_and_ping.py:59` | `def test_load_fresh_state_has_zero_commands(self, tmp_path)` |
| `test_next_threshold_always_positive` | method | `tests/test_engagement_and_ping.py:106` | `def test_next_threshold_always_positive(self)` |
| `test_next_threshold_mean_near_target` | method | `tests/test_engagement_and_ping.py:113` | `def test_next_threshold_mean_near_target(self)` |
| `test_no_advisor_reference_before_definition` | method | `tests/test_engagement_and_ping.py:470` | `def test_no_advisor_reference_before_definition(self)` |
| `test_no_graph_nodes_in_output` | method | `tests/test_engagement_and_ping.py:456` | `def test_no_graph_nodes_in_output(self, tmp_path, capsys)` |
| `test_ping_os_json_contract` | method | `tests/test_engagement_and_ping.py:330` | `def test_ping_os_json_contract(self)` |
| `test_ping_persists_via_apply_assign` | method | `tests/test_engagement_and_ping.py:338` | `def test_ping_persists_via_apply_assign(self)` |
| `test_rule_not_used_without_import` | method | `tests/test_engagement_and_ping.py:509` | `def test_rule_not_used_without_import(self)` |
| `test_save_and_reload_state` | method | `tests/test_engagement_and_ping.py:74` | `def test_save_and_reload_state(self, tmp_path)` |
| `test_shows_nothing_when_all_run` | method | `tests/test_engagement_and_ping.py:436` | `def test_shows_nothing_when_all_run(self, tmp_path)` |
| `test_shows_unrun_commands` | method | `tests/test_engagement_and_ping.py:411` | `def test_shows_unrun_commands(self, tmp_path, capsys)` |
| `test_threshold_is_variable_not_constant` | method | `tests/test_engagement_and_ping.py:120` | `def test_threshold_is_variable_not_constant(self)` |
| `test_ttl_127_maps_to_os_id_2_windows` | method | `tests/test_engagement_and_ping.py:309` | `def test_ttl_127_maps_to_os_id_2_windows(self)` |
| `test_ttl_128_maps_to_os_id_2_windows` | method | `tests/test_engagement_and_ping.py:302` | `def test_ttl_128_maps_to_os_id_2_windows(self)` |
| `test_ttl_255_maps_to_unknown` | method | `tests/test_engagement_and_ping.py:323` | `def test_ttl_255_maps_to_unknown(self)` |
| `test_ttl_63_maps_to_os_id_1_linux` | method | `tests/test_engagement_and_ping.py:316` | `def test_ttl_63_maps_to_os_id_1_linux(self)` |
| `test_ttl_64_maps_to_os_id_1_linux` | method | `tests/test_engagement_and_ping.py:295` | `def test_ttl_64_maps_to_os_id_1_linux(self)` |
| `test_vri_does_not_fire_before_threshold` | method | `tests/test_engagement_and_ping.py:152` | `def test_vri_does_not_fire_before_threshold(self, tmp_path, capsys)` |
| `test_vri_fires_when_threshold_reached` | method | `tests/test_engagement_and_ping.py:126` | `def test_vri_fires_when_threshold_reached(self, tmp_path, capsys)` |
| `TestHealCommandsSeen` | class | `tests/test_engagement_command_gate.py:187` | `class TestHealCommandsSeen` |
| `TestHookRejectsNoise` | class | `tests/test_engagement_command_gate.py:106` | `class TestHookRejectsNoise` |
| `TestIsRecordableCommand` | class | `tests/test_engagement_command_gate.py:68` | `class TestIsRecordableCommand` |
| `TestSanitizeSeen` | class | `tests/test_engagement_command_gate.py:141` | `class TestSanitizeSeen` |
| `_redirect_paths` | function | `tests/test_engagement_command_gate.py:34` | `def _redirect_paths(tmp_path)` |
| `_restore_paths` | function | `tests/test_engagement_command_gate.py:56` | `def _restore_paths(saved)` |
| `test_accepts_command_shaped_tokens` | method | `tests/test_engagement_command_gate.py:72` | `def test_accepts_command_shaped_tokens(self, cmd)` |
| `test_do_prefixed_input_is_accepted` | method | `tests/test_engagement_command_gate.py:91` | `def test_do_prefixed_input_is_accepted(self)` |
| `test_garbage_does_not_enter_commands_seen` | method | `tests/test_engagement_command_gate.py:109` | `def test_garbage_does_not_enter_commands_seen(self, tmp_path)` |
| `test_idempotent_on_clean_state` | method | `tests/test_engagement_command_gate.py:207` | `def test_idempotent_on_clean_state(self, tmp_path)` |
| `test_load_state_heals_polluted_file` | method | `tests/test_engagement_command_gate.py:165` | `def test_load_state_heals_polluted_file(self, tmp_path)` |
| `test_normalize_is_idempotent` | method | `tests/test_engagement_command_gate.py:96` | `def test_normalize_is_idempotent(self)` |
| `test_purges_and_persists` | method | `tests/test_engagement_command_gate.py:190` | `def test_purges_and_persists(self, tmp_path)` |
| `test_quoted_path_rejected` | method | `tests/test_engagement_command_gate.py:86` | `def test_quoted_path_rejected(self)` |
| `test_real_command_recorded_between_garbage` | method | `tests/test_engagement_command_gate.py:123` | `def test_real_command_recorded_between_garbage(self, tmp_path)` |
| `test_rejects_syntactic_garbage` | method | `tests/test_engagement_command_gate.py:81` | `def test_rejects_syntactic_garbage(self, cmd)` |
| `test_roster_drops_valid_but_unknown_tokens` | method | `tests/test_engagement_command_gate.py:158` | `def test_roster_drops_valid_but_unknown_tokens(self)` |
| `test_syntactic_only_drops_ugly_garbage` | method | `tests/test_engagement_command_gate.py:144` | `def test_syntactic_only_drops_ugly_garbage(self)` |
| `TestAwardElo` | class | `tests/test_engagement_elo_and_methodology.py:119` | `class TestAwardElo` |
| `TestGetKarmaName` | class | `tests/test_engagement_elo_and_methodology.py:88` | `class TestGetKarmaName` |
| `TestKarmaUp` | class | `tests/test_engagement_elo_and_methodology.py:425` | `class TestKarmaUp` |
| `TestMethodologyRewards` | class | `tests/test_engagement_elo_and_methodology.py:313` | `class TestMethodologyRewards` |
| `TestPersistNotification` | class | `tests/test_engagement_elo_and_methodology.py:252` | `class TestPersistNotification` |
| `TestRenderEngagementHookIntegration` | class | `tests/test_engagement_elo_and_methodology.py:463` | `class TestRenderEngagementHookIntegration` |
| `TestStateSnapshot` | class | `tests/test_engagement_elo_and_methodology.py:524` | `class TestStateSnapshot` |
| `TestSyncUserElo` | class | `tests/test_engagement_elo_and_methodology.py:179` | `class TestSyncUserElo` |
| `_no_cli_operator` | function | `tests/test_engagement_elo_and_methodology.py:31` | `def _no_cli_operator(monkeypatch)` |
| `_redirect_paths` | function | `tests/test_engagement_elo_and_methodology.py:48` | `def _redirect_paths(tmp_path)` |
| `_restore_paths` | function | `tests/test_engagement_elo_and_methodology.py:76` | `def _restore_paths(saved)` |
| `test_all_bonuses_stack` | method | `tests/test_engagement_elo_and_methodology.py:149` | `def test_all_bonuses_stack(self)` |
| `test_appends_to_existing_file` | method | `tests/test_engagement_elo_and_methodology.py:264` | `def test_appends_to_existing_file(self, tmp_path)` |
| `test_atomic_rename_leaves_no_tmp` | method | `tests/test_engagement_elo_and_methodology.py:234` | `def test_atomic_rename_leaves_no_tmp(self, tmp_path)` |
| `test_base_only_for_unknown_command_and_phase` | method | `tests/test_engagement_elo_and_methodology.py:120` | `def test_base_only_for_unknown_command_and_phase(self)` |
| `test_creates_file_on_first_call` | method | `tests/test_engagement_elo_and_methodology.py:253` | `def test_creates_file_on_first_call(self, tmp_path)` |
| `test_disabled_flag_is_noop` | method | `tests/test_engagement_elo_and_methodology.py:508` | `def test_disabled_flag_is_noop(self, tmp_path, capsys)` |
| `test_do_prefix_is_stripped` | method | `tests/test_engagement_elo_and_methodology.py:169` | `def test_do_prefix_is_stripped(self)` |
| `test_elo_accumulates_across_commands` | method | `tests/test_engagement_elo_and_methodology.py:464` | `def test_elo_accumulates_across_commands(self, tmp_path)` |
| `test_fires_on_threshold_crossing` | method | `tests/test_engagement_elo_and_methodology.py:426` | `def test_fires_on_threshold_crossing(self, tmp_path, capsys)` |
| `test_first_time_bonus` | method | `tests/test_engagement_elo_and_methodology.py:137` | `def test_first_time_bonus(self)` |
| `test_first_time_bonus_only_once_per_command` | method | `tests/test_engagement_elo_and_methodology.py:479` | `def test_first_time_bonus_only_once_per_command(self, tmp_path)` |
| `test_high_value_bonus_applied` | method | `tests/test_engagement_elo_and_methodology.py:125` | `def test_high_value_bonus_applied(self)` |
| `test_idempotent_when_no_threshold_cross` | method | `tests/test_engagement_elo_and_methodology.py:440` | `def test_idempotent_when_no_threshold_cross(self, capsys)` |
| `test_ignores_non_positive_delta` | method | `tests/test_engagement_elo_and_methodology.py:224` | `def test_ignores_non_positive_delta(self, tmp_path)` |
| `test_new_phase_bonus` | method | `tests/test_engagement_elo_and_methodology.py:143` | `def test_new_phase_bonus(self)` |
| `test_note_reward_renders_latest` | method | `tests/test_engagement_elo_and_methodology.py:391` | `def test_note_reward_renders_latest(self, tmp_path, capsys)` |
| `test_note_reward_silent_when_empty` | method | `tests/test_engagement_elo_and_methodology.py:412` | `def test_note_reward_silent_when_empty(self, tmp_path, capsys)` |
| `test_objective_reward_silent_when_no_pending` | method | `tests/test_engagement_elo_and_methodology.py:379` | `def test_objective_reward_silent_when_no_pending(self, tmp_path, capsys)` |
| `test_objective_reward_uses_phase_to_next_cmd` | method | `tests/test_engagement_elo_and_methodology.py:361` | `def test_objective_reward_uses_phase_to_next_cmd(self, tmp_path, capsys)` |
| `test_patches_matching_username` | method | `tests/test_engagement_elo_and_methodology.py:180` | `def test_patches_matching_username(self, tmp_path)` |
| `test_persists_notification` | method | `tests/test_engagement_elo_and_methodology.py:447` | `def test_persists_notification(self, tmp_path)` |
| `test_phase_bonus_applied` | method | `tests/test_engagement_elo_and_methodology.py:131` | `def test_phase_bonus_applied(self)` |
| `test_recovers_from_corrupt_file` | method | `tests/test_engagement_elo_and_methodology.py:297` | `def test_recovers_from_corrupt_file(self, tmp_path)` |
| `test_returns_required_keys` | method | `tests/test_engagement_elo_and_methodology.py:525` | `def test_returns_required_keys(self, tmp_path)` |
| `test_ring_cap_drops_oldest` | method | `tests/test_engagement_elo_and_methodology.py:277` | `def test_ring_cap_drops_oldest(self, tmp_path)` |
| `test_silent_when_payload_missing` | method | `tests/test_engagement_elo_and_methodology.py:199` | `def test_silent_when_payload_missing(self, tmp_path)` |
| `test_silent_when_username_not_found` | method | `tests/test_engagement_elo_and_methodology.py:211` | `def test_silent_when_username_not_found(self, tmp_path)` |
| `test_task_reward_renders_pending_match` | method | `tests/test_engagement_elo_and_methodology.py:324` | `def test_task_reward_renders_pending_match(self, tmp_path, capsys)` |
| `test_task_reward_silent_when_all_done` | method | `tests/test_engagement_elo_and_methodology.py:344` | `def test_task_reward_silent_when_all_done(self, tmp_path, capsys)` |
| `test_task_reward_silent_when_no_file` | method | `tests/test_engagement_elo_and_methodology.py:314` | `def test_task_reward_silent_when_no_file(self, tmp_path, capsys)` |
| `test_thresholds` | method | `tests/test_engagement_elo_and_methodology.py:110` | `def test_thresholds(self, elo, expected)` |
| `test_users_json_syncd_when_payload_present` | method | `tests/test_engagement_elo_and_methodology.py:493` | `def test_users_json_syncd_when_payload_present(self, tmp_path)` |
| `_base_nodes` | function | `tests/test_estorides_fusion.py:36` | `def _base_nodes()` |
| `_load_surface_graph` | function | `tests/test_estorides_fusion.py:27` | `def _load_surface_graph()` |
| `test_discovery_targets_reads_all_files` | function | `tests/test_estorides_fusion.py:194` | `def test_discovery_targets_reads_all_files(tmp_path)` |
| `test_find_export_prefers_lazyown` | function | `tests/test_estorides_fusion.py:182` | `def test_find_export_prefers_lazyown(tmp_path)` |
| `test_load_lazyown_vocabulary` | function | `tests/test_estorides_fusion.py:50` | `def test_load_lazyown_vocabulary(tmp_path)` |
| `test_load_raw_export_translates_types` | function | `tests/test_estorides_fusion.py:73` | `def test_load_raw_export_translates_types(tmp_path)` |
| `test_merge_adds_new_entities_capped` | function | `tests/test_estorides_fusion.py:116` | `def test_merge_adds_new_entities_capped()` |
| `test_merge_edges_reanchor` | function | `tests/test_estorides_fusion.py:141` | `def test_merge_edges_reanchor(tmp_path)` |
| `test_merge_fuses_matching_ip` | function | `tests/test_estorides_fusion.py:91` | `def test_merge_fuses_matching_ip()` |
| `test_parse_confirm` | function | `tests/test_estorides_fusion.py:187` | `def test_parse_confirm()` |
| `test_surface_readers_cover_sessions_formats` | function | `tests/test_estorides_fusion.py:219` | `def test_surface_readers_cover_sessions_formats(tmp_path)` |
| `test_write_world_model_hosts` | function | `tests/test_estorides_fusion.py:201` | `def test_write_world_model_hosts(tmp_path)` |
| `TestBuildEvidenceHints` | class | `tests/test_evidence_hints.py:86` | `class TestBuildEvidenceHints` |
| `TestConfidenceFromScore` | class | `tests/test_evidence_hints.py:62` | `class TestConfidenceFromScore` |
| `TestRecommendWithEvidence` | class | `tests/test_evidence_hints.py:144` | `class TestRecommendWithEvidence` |
| `TestRenderEvidenceHints` | class | `tests/test_evidence_hints.py:131` | `class TestRenderEvidenceHints` |
| `TestTipsEngineEvidenceWiring` | class | `tests/test_evidence_hints.py:178` | `class TestTipsEngineEvidenceWiring` |
| `_FakeEngine` | class | `tests/test_evidence_hints.py:50` | `class _FakeEngine` |
| `__init__` | method | `tests/test_evidence_hints.py:53` | `def __init__(self, recs)` |
| `_engine_with_stub` | function | `tests/test_evidence_hints.py:170` | `def _engine_with_stub(sessions, recs, evidence)` |
| `_rec` | function | `tests/test_evidence_hints.py:33` | `def _rec(action, score, reasons, sources, command_preview)` |
| `recommend` | method | `tests/test_evidence_hints.py:57` | `def recommend(self, ctx)` |
| `test_bounded_in_unit_range_scaled` | method | `tests/test_evidence_hints.py:80` | `def test_bounded_in_unit_range_scaled(self)` |
| `test_disabled_flag_returns_empty` | method | `tests/test_evidence_hints.py:179` | `def test_disabled_flag_returns_empty(self, tmp_sessions_with_csv)` |
| `test_empty_list_prints_nothing` | method | `tests/test_evidence_hints.py:139` | `def test_empty_list_prints_nothing(self, capsys)` |
| `test_filters_already_run_commands` | method | `tests/test_evidence_hints.py:196` | `def test_filters_already_run_commands(self, tmp_sessions_with_csv)` |
| `test_half_score_constant_yields_fifty` | method | `tests/test_evidence_hints.py:69` | `def test_half_score_constant_yields_fifty(self)` |
| `test_maps_core_fields` | method | `tests/test_evidence_hints.py:87` | `def test_maps_core_fields(self)` |
| `test_missing_engine_returns_empty` | method | `tests/test_evidence_hints.py:183` | `def test_missing_engine_returns_empty(self, tmp_sessions_with_csv)` |
| `test_monotonic_non_decreasing` | method | `tests/test_evidence_hints.py:72` | `def test_monotonic_non_decreasing(self)` |
| `test_negative_score_floored_to_zero` | method | `tests/test_evidence_hints.py:66` | `def test_negative_score_floored_to_zero(self)` |
| `test_never_reaches_or_exceeds_hundred` | method | `tests/test_evidence_hints.py:76` | `def test_never_reaches_or_exceeds_hundred(self)` |
| `test_phase_override_reaches_engine_context` | method | `tests/test_evidence_hints.py:150` | `def test_phase_override_reaches_engine_context(self)` |
| `test_prefers_command_preview_over_action` | method | `tests/test_evidence_hints.py:104` | `def test_prefers_command_preview_over_action(self)` |
| `test_prints_verb_confidence_and_reason` | method | `tests/test_evidence_hints.py:132` | `def test_prints_verb_confidence_and_reason(self, capsys)` |
| `test_render_falls_back_to_bare_names` | method | `tests/test_evidence_hints.py:214` | `def test_render_falls_back_to_bare_names(self, tmp_sessions_with_csv)` |
| `test_render_prefers_evidence_over_bare_names` | method | `tests/test_evidence_hints.py:208` | `def test_render_prefers_evidence_over_bare_names(self, tmp_sessions_with_csv)` |
| `test_respects_limit` | method | `tests/test_evidence_hints.py:119` | `def test_respects_limit(self)` |
| `test_returns_engine_output` | method | `tests/test_evidence_hints.py:145` | `def test_returns_engine_output(self)` |
| `test_returns_evidence_hints` | method | `tests/test_evidence_hints.py:190` | `def test_returns_evidence_hints(self, tmp_sessions_with_csv)` |
| `test_skips_recommendation_without_reason` | method | `tests/test_evidence_hints.py:115` | `def test_skips_recommendation_without_reason(self)` |
| `test_skips_recommendation_without_verb` | method | `tests/test_evidence_hints.py:111` | `def test_skips_recommendation_without_verb(self)` |
| `test_strips_source_tag_from_reason` | method | `tests/test_evidence_hints.py:100` | `def test_strips_source_tag_from_reason(self)` |
| `test_target_falls_back_to_rhost` | method | `tests/test_evidence_hints.py:155` | `def test_target_falls_back_to_rhost(self)` |
| `test_truncates_long_reason` | method | `tests/test_evidence_hints.py:125` | `def test_truncates_long_reason(self)` |
| `test_zero_score_is_zero_confidence` | method | `tests/test_evidence_hints.py:63` | `def test_zero_score_is_zero_confidence(self)` |
| `tmp_sessions_with_csv` | function | `tests/test_evidence_hints.py:162` | `def tmp_sessions_with_csv()` |
| `TestColorsPreserved` | class | `tests/test_executor_kernel.py:33` | `class TestColorsPreserved` |
| `TestExitCodes` | class | `tests/test_executor_kernel.py:62` | `class TestExitCodes` |
| `TestShellPolicy` | class | `tests/test_executor_kernel.py:87` | `class TestShellPolicy` |
| `TestSingleSpawnPath` | class | `tests/test_executor_kernel.py:113` | `class TestSingleSpawnPath` |
| `_executor` | function | `tests/test_executor_kernel.py:29` | `def _executor()` |
| `test_argv_path_exit_code` | method | `tests/test_executor_kernel.py:70` | `def test_argv_path_exit_code(self)` |
| `test_cmd_delegates_spawning_to_kernel` | method | `tests/test_executor_kernel.py:114` | `def test_cmd_delegates_spawning_to_kernel(self)` |
| `test_cmd_keeps_telemetry` | method | `tests/test_executor_kernel.py:142` | `def test_cmd_keeps_telemetry(self)` |
| `test_log_file_is_byte_identical_to_writer` | method | `tests/test_executor_kernel.py:42` | `def test_log_file_is_byte_identical_to_writer(self, tmp_path)` |
| `test_matches_shared_policy` | method | `tests/test_executor_kernel.py:101` | `def test_matches_shared_policy(self)` |
| `test_passthrough_returns_exit_code` | method | `tests/test_executor_kernel.py:76` | `def test_passthrough_returns_exit_code(self)` |
| `test_shell_path_exit_code` | method | `tests/test_executor_kernel.py:63` | `def test_shell_path_exit_code(self)` |
| `test_stderr_merged_into_stream` | method | `tests/test_executor_kernel.py:52` | `def test_stderr_merged_into_stream(self)` |
| `test_timeout_kills_and_raises` | method | `tests/test_executor_kernel.py:106` | `def test_timeout_kills_and_raises(self)` |
| `test_writer_receives_raw_ansi_bytes` | method | `tests/test_executor_kernel.py:34` | `def test_writer_receives_raw_ansi_bytes(self)` |
| `FakeProc` | class | `tests/test_exploitgym_gym.py:143` | `class FakeProc` |
| `FakeProc` | class | `tests/test_exploitgym_gym.py:177` | `class FakeProc` |
| `_add_repo_root_to_syspath` | function | `tests/test_exploitgym_gym.py:18` | `def _add_repo_root_to_syspath()` |
| `_params` | function | `tests/test_exploitgym_gym.py:39` | `def _params(root)` |
| `fake_record` | function | `tests/test_exploitgym_gym.py:195` | `def fake_record(challenge_id, success, elo_bonus, techniques)` |
| `fake_repo` | function | `tests/test_exploitgym_gym.py:24` | `def fake_repo(tmp_path)` |
| `fake_run` | function | `tests/test_exploitgym_gym.py:148` | `def fake_run(cmd, cwd, capture_output, text, timeout, env)` |
| `fake_run` | function | `tests/test_exploitgym_gym.py:182` | `def fake_run(cmd, cwd, capture_output, text, timeout, env)` |
| `fake_run_streaming` | function | `tests/test_exploitgym_gym.py:226` | `def fake_run_streaming(cmd, cwd, timeout)` |
| `fake_which` | function | `tests/test_exploitgym_gym.py:87` | `def fake_which(name)` |
| `fake_which` | function | `tests/test_exploitgym_gym.py:102` | `def fake_which(name)` |
| `fake_which` | function | `tests/test_exploitgym_gym.py:118` | `def fake_which(name)` |
| `test_bridge_catalog_has_exploitgym` | function | `tests/test_exploitgym_gym.py:248` | `def test_bridge_catalog_has_exploitgym()` |
| `test_check_readiness_missing_docker` | function | `tests/test_exploitgym_gym.py:99` | `def test_check_readiness_missing_docker(fake_repo, monkeypatch)` |
| `test_check_readiness_missing_keys` | function | `tests/test_exploitgym_gym.py:115` | `def test_check_readiness_missing_keys(fake_repo, monkeypatch)` |
| `test_check_readiness_ready` | function | `tests/test_exploitgym_gym.py:84` | `def test_check_readiness_ready(fake_repo, monkeypatch)` |
| `test_command_set_declares_exploitgym` | function | `tests/test_exploitgym_gym.py:241` | `def test_command_set_declares_exploitgym()` |
| `test_detect_domain_userspace` | function | `tests/test_exploitgym_gym.py:51` | `def test_detect_domain_userspace(fake_repo)` |
| `test_extract_flag` | function | `tests/test_exploitgym_gym.py:129` | `def test_extract_flag()` |
| `test_list_tasks_empty_without_repo` | function | `tests/test_exploitgym_gym.py:77` | `def test_list_tasks_empty_without_repo(tmp_path)` |
| `test_list_tasks_filters_by_domain` | function | `tests/test_exploitgym_gym.py:60` | `def test_list_tasks_filters_by_domain(fake_repo)` |
| `test_pull_task_success` | function | `tests/test_exploitgym_gym.py:174` | `def test_pull_task_success(fake_repo, monkeypatch)` |
| `test_run_task_reports_missing_repo` | function | `tests/test_exploitgym_gym.py:166` | `def test_run_task_reports_missing_repo(tmp_path)` |
| `test_run_task_writes_log_and_records` | function | `tests/test_exploitgym_gym.py:137` | `def test_run_task_writes_log_and_records(fake_repo, tmp_path, monkeypatch)` |
| `test_score_task_reuses_redteam_pipeline` | function | `tests/test_exploitgym_gym.py:192` | `def test_score_task_reuses_redteam_pipeline(fake_repo, monkeypatch)` |
| `test_setup_harness_reports_missing_repo` | function | `tests/test_exploitgym_gym.py:212` | `def test_setup_harness_reports_missing_repo(tmp_path, monkeypatch)` |
| `test_setup_harness_runs_requested_steps` | function | `tests/test_exploitgym_gym.py:221` | `def test_setup_harness_runs_requested_steps(fake_repo, monkeypatch)` |
| `TestCatalogues` | class | `tests/test_exploration_and_addons.py:206` | `class TestCatalogues` |
| `TestEngineEndToEnd` | class | `tests/test_exploration_and_addons.py:290` | `class TestEngineEndToEnd` |
| `TestNmapXmlReader` | class | `tests/test_exploration_and_addons.py:182` | `class TestNmapXmlReader` |
| `TestNormalisers` | class | `tests/test_exploration_and_addons.py:148` | `class TestNormalisers` |
| `TestRenderer` | class | `tests/test_exploration_and_addons.py:337` | `class TestRenderer` |
| `TestResolveCurrentOs` | class | `tests/test_exploration_and_addons.py:316` | `class TestResolveCurrentOs` |
| `TestShippedAddonsRespectSchema` | class | `tests/test_exploration_and_addons.py:362` | `class TestShippedAddonsRespectSchema` |
| `TestTriggerMatcher` | class | `tests/test_exploration_and_addons.py:262` | `class TestTriggerMatcher` |
| `_addon` | function | `tests/test_exploration_and_addons.py:395` | `def _addon(name, addon_os, trigger, enabled)` |
| `_svc` | function | `tests/test_exploration_and_addons.py:410` | `def _svc(service, port)` |
| `addon_files` | method | `tests/test_exploration_and_addons.py:366` | `def addon_files(self)` |
| `fake_addons` | function | `tests/test_exploration_and_addons.py:84` | `def fake_addons(tmp_path)` |
| `fake_sessions` | function | `tests/test_exploration_and_addons.py:71` | `def fake_sessions(tmp_path)` |
| `fake_tools` | function | `tests/test_exploration_and_addons.py:127` | `def fake_tools(tmp_path)` |
| `test_addon_catalog_invalidates_cache_on_change` | method | `tests/test_exploration_and_addons.py:237` | `def test_addon_catalog_invalidates_cache_on_change(self, fake_addons, monkeypatch)` |
| `test_addon_catalog_loads_os_and_trigger` | method | `tests/test_exploration_and_addons.py:209` | `def test_addon_catalog_loads_os_and_trigger(self, fake_addons, monkeypatch)` |
| `test_addon_catalog_reuses_cache_when_mtime_unchanged` | method | `tests/test_exploration_and_addons.py:228` | `def test_addon_catalog_reuses_cache_when_mtime_unchanged(self, fake_addons, monkeypatch)` |
| `test_all_have_os_in_allowed_values` | method | `tests/test_exploration_and_addons.py:372` | `def test_all_have_os_in_allowed_values(self, addon_files)` |
| `test_all_have_trigger_list` | method | `tests/test_exploration_and_addons.py:381` | `def test_all_have_trigger_list(self, addon_files)` |
| `test_at_least_one_addon_exists` | method | `tests/test_exploration_and_addons.py:369` | `def test_at_least_one_addon_exists(self, addon_files)` |
| `test_disabled_addon_skipped` | method | `tests/test_exploration_and_addons.py:283` | `def test_disabled_addon_skipped(self)` |
| `test_normalise_os` | method | `tests/test_exploration_and_addons.py:163` | `def test_normalise_os(self, value, expected)` |
| `test_normalise_trigger` | method | `tests/test_exploration_and_addons.py:178` | `def test_normalise_trigger(self, value, expected)` |
| `test_os_compat_any_passes` | method | `tests/test_exploration_and_addons.py:265` | `def test_os_compat_any_passes(self)` |
| `test_os_mismatch_filters_out` | method | `tests/test_exploration_and_addons.py:271` | `def test_os_mismatch_filters_out(self)` |
| `test_reads_only_open_ports` | method | `tests/test_exploration_and_addons.py:185` | `def test_reads_only_open_ports(self, fake_sessions, monkeypatch)` |
| `test_records_product_version` | method | `tests/test_exploration_and_addons.py:197` | `def test_records_product_version(self, fake_sessions, monkeypatch)` |
| `test_renders_empty_scope` | method | `tests/test_exploration_and_addons.py:340` | `def test_renders_empty_scope(self, tmp_path, monkeypatch)` |
| `test_renders_populated_scope` | method | `tests/test_exploration_and_addons.py:350` | `def test_renders_populated_scope(self, fake_sessions, fake_addons, fake_tools, monkeypatch, tmp_path)` |
| `test_resolves` | method | `tests/test_exploration_and_addons.py:333` | `def test_resolves(self, payload, expected)` |
| `test_suggestions_and_coverage` | method | `tests/test_exploration_and_addons.py:293` | `def test_suggestions_and_coverage(self, fake_sessions, fake_addons, fake_tools, monkeypatch, tmp_path)` |
| `test_target_filter_excludes_other_hosts` | method | `tests/test_exploration_and_addons.py:192` | `def test_target_filter_excludes_other_hosts(self, fake_sessions, monkeypatch)` |
| `test_tool_catalog_loads_os_default` | method | `tests/test_exploration_and_addons.py:219` | `def test_tool_catalog_loads_os_default(self, fake_tools, monkeypatch)` |
| `test_tool_catalog_reuses_cache_when_mtime_unchanged` | method | `tests/test_exploration_and_addons.py:252` | `def test_tool_catalog_reuses_cache_when_mtime_unchanged(self, fake_tools, monkeypatch)` |
| `test_unexplored_excludes_history` | method | `tests/test_exploration_and_addons.py:308` | `def test_unexplored_excludes_history(self, fake_sessions, fake_addons, fake_tools, monkeypatch, tmp_path)` |
| `test_wildcard_matches_any_service` | method | `tests/test_exploration_and_addons.py:277` | `def test_wildcard_matches_any_service(self)` |
| `ChainFactsSpoolSpec` | class | `tests/test_f4_hardening.py:89` | `class ChainFactsSpoolSpec(TestCase)` |
| `CtfCliSpec` | class | `tests/test_f4_hardening.py:128` | `class CtfCliSpec(TestCase)` |
| `FakeStore` | class | `tests/test_f4_hardening.py:95` | `class FakeStore` |
| `FootholdChainSpec` | class | `tests/test_f4_hardening.py:166` | `class FootholdChainSpec(TestCase)` |
| `Shell` | class | `tests/test_f4_hardening.py:27` | `class Shell` |
| `Shell` | class | `tests/test_f4_hardening.py:46` | `class Shell` |
| `Shell` | class | `tests/test_f4_hardening.py:73` | `class Shell` |
| `VerbWatchdogSpec` | class | `tests/test_f4_hardening.py:23` | `class VerbWatchdogSpec(TestCase)` |
| `_chain` | function | `tests/test_f4_hardening.py:18` | `def _chain(steps)` |
| `do_hang` | method | `tests/test_f4_hardening.py:30` | `def do_hang(self, line)` |
| `do_hang` | method | `tests/test_f4_hardening.py:49` | `def do_hang(self, line)` |
| `do_ping` | method | `tests/test_f4_hardening.py:76` | `def do_ping(self, line)` |
| `ingest_text` | method | `tests/test_f4_hardening.py:96` | `def ingest_text(self, path, host_hint)` |
| `onecmd` | method | `tests/test_f4_hardening.py:33` | `def onecmd(self, command)` |
| `onecmd` | method | `tests/test_f4_hardening.py:52` | `def onecmd(self, command)` |
| `onecmd` | method | `tests/test_f4_hardening.py:79` | `def onecmd(self, command)` |
| `save` | method | `tests/test_f4_hardening.py:100` | `def save(self)` |
| `test_capture_cli_roundtrip` | method | `tests/test_f4_hardening.py:131` | `def test_capture_cli_roundtrip(self)` |
| `test_chain_loads_and_renders_tokens` | method | `tests/test_f4_hardening.py:169` | `def test_chain_loads_and_renders_tokens(self)` |
| `test_empty_chain_spools_nothing` | method | `tests/test_f4_hardening.py:122` | `def test_empty_chain_spools_nothing(self)` |
| `test_fast_verb_still_on_main_thread` | method | `tests/test_f4_hardening.py:70` | `def test_fast_verb_still_on_main_thread(self)` |
| `test_hung_verb_fails_whole_chain` | method | `tests/test_f4_hardening.py:45` | `def test_hung_verb_fails_whole_chain(self)` |
| `test_hung_verb_times_out` | method | `tests/test_f4_hardening.py:26` | `def test_hung_verb_times_out(self)` |
| `test_spool_writes_and_ingests` | method | `tests/test_f4_hardening.py:92` | `def test_spool_writes_and_ingests(self)` |
| `_boom` | function | `tests/test_finding_lifecycle.py:87` | `def _boom(cve, sessions)` |
| `_finding` | function | `tests/test_finding_lifecycle.py:24` | `def _finding(fid, sources)` |
| `test_apply_confirmation_stamps_nodes` | function | `tests/test_finding_lifecycle.py:65` | `def test_apply_confirmation_stamps_nodes(tmp_path)` |
| `test_dead_end_suppresses_value` | function | `tests/test_finding_lifecycle.py:57` | `def test_dead_end_suppresses_value(tmp_path)` |
| `test_enrich_evidence_appends_keyless_verdicts` | function | `tests/test_finding_lifecycle.py:75` | `def test_enrich_evidence_appends_keyless_verdicts(tmp_path, monkeypatch)` |
| `test_enrich_evidence_never_fails_offline` | function | `tests/test_finding_lifecycle.py:85` | `def test_enrich_evidence_never_fails_offline(tmp_path, monkeypatch)` |
| `test_explicit_confirm_with_evidence` | function | `tests/test_finding_lifecycle.py:41` | `def test_explicit_confirm_with_evidence(tmp_path)` |
| `test_multi_source_auto_confirms` | function | `tests/test_finding_lifecycle.py:35` | `def test_multi_source_auto_confirms(tmp_path)` |
| `test_pending_by_default` | function | `tests/test_finding_lifecycle.py:30` | `def test_pending_by_default(tmp_path)` |
| `test_reject_beats_auto_confirm` | function | `tests/test_finding_lifecycle.py:49` | `def test_reject_beats_auto_confirm(tmp_path)` |
| `_FakeView` | class | `tests/test_fuzzy_picker.py:35` | `class _FakeView(PickerView)` |
| `__init__` | method | `tests/test_fuzzy_picker.py:38` | `def __init__(self, selection_index)` |
| `_collect_runtime_strings` | function | `tests/test_fuzzy_picker.py:198` | `def _collect_runtime_strings()` |
| `_collect_string_constants` | function | `tests/test_fuzzy_picker.py:174` | `def _collect_string_constants(source)` |
| `run` | method | `tests/test_fuzzy_picker.py:43` | `def run(self, items, initial_query)` |
| `sample_items` | function | `tests/test_fuzzy_picker.py:59` | `def sample_items()` |
| `scorer` | function | `tests/test_fuzzy_picker.py:54` | `def scorer()` |
| `test_config_from_payload_ignores_unknown_keys` | function | `tests/test_fuzzy_picker.py:119` | `def test_config_from_payload_ignores_unknown_keys()` |
| `test_config_from_payload_respects_known_overrides` | function | `tests/test_fuzzy_picker.py:112` | `def test_config_from_payload_respects_known_overrides()` |
| `test_config_from_payload_returns_defaults_when_no_block` | function | `tests/test_fuzzy_picker.py:124` | `def test_config_from_payload_returns_defaults_when_no_block()` |
| `test_empty_query_returns_all_items_in_order` | function | `tests/test_fuzzy_picker.py:72` | `def test_empty_query_returns_all_items_in_order(scorer, sample_items)` |
| `test_exact_match_scores_highest` | function | `tests/test_fuzzy_picker.py:78` | `def test_exact_match_scores_highest(scorer, sample_items)` |
| `test_getprompt_renders_three_lines_and_includes_payload_segments` | function | `tests/test_fuzzy_picker.py:280` | `def test_getprompt_renders_three_lines_and_includes_payload_segments()` |
| `test_lazyown_runtime_strings_preserve_shell_payload` | function | `tests/test_fuzzy_picker.py:260` | `def test_lazyown_runtime_strings_preserve_shell_payload(expected_substring)` |
| `test_lazyown_source_has_no_invalid_escape_warning` | function | `tests/test_fuzzy_picker.py:265` | `def test_lazyown_source_has_no_invalid_escape_warning()` |
| `test_picker_cancel_returns_none` | function | `tests/test_fuzzy_picker.py:146` | `def test_picker_cancel_returns_none(sample_items)` |
| `test_picker_empty_input_returns_none` | function | `tests/test_fuzzy_picker.py:152` | `def test_picker_empty_input_returns_none()` |
| `test_picker_routes_through_view_for_multiple_items` | function | `tests/test_fuzzy_picker.py:138` | `def test_picker_routes_through_view_for_multiple_items(sample_items)` |
| `test_picker_short_circuits_single_item` | function | `tests/test_fuzzy_picker.py:132` | `def test_picker_short_circuits_single_item()` |
| `test_prefix_match_outranks_substring` | function | `tests/test_fuzzy_picker.py:84` | `def test_prefix_match_outranks_substring(scorer)` |
| `test_similarity_floor_excludes_unrelated_text` | function | `tests/test_fuzzy_picker.py:98` | `def test_similarity_floor_excludes_unrelated_text(scorer)` |
| `test_strip_ansi_passes_through_plain_text` | function | `tests/test_fuzzy_picker.py:165` | `def test_strip_ansi_passes_through_plain_text()` |
| `test_strip_ansi_removes_csi_sequences` | function | `tests/test_fuzzy_picker.py:160` | `def test_strip_ansi_removes_csi_sequences()` |
| `test_subsequence_match_emits_positions` | function | `tests/test_fuzzy_picker.py:90` | `def test_subsequence_match_emits_positions(scorer, sample_items)` |
| `test_subsequence_positions_helper_returns_empty_when_no_match` | function | `tests/test_fuzzy_picker.py:104` | `def test_subsequence_positions_helper_returns_empty_when_no_match()` |
| `ArtifactSpec` | class | `tests/test_golden_path.py:86` | `class ArtifactSpec(TestCase)` |
| `PushObjectivesSpec` | class | `tests/test_golden_path.py:114` | `class PushObjectivesSpec(TestCase)` |
| `ResolvePathsSpec` | class | `tests/test_golden_path.py:45` | `class ResolvePathsSpec(TestCase)` |
| `_snapshot` | function | `tests/test_golden_path.py:13` | `def _snapshot()` |
| `test_anchor_excluded_from_targets` | method | `tests/test_golden_path.py:48` | `def test_anchor_excluded_from_targets(self)` |
| `test_build_writes_artifact_from_world_model` | method | `tests/test_golden_path.py:89` | `def test_build_writes_artifact_from_world_model(self)` |
| `test_confirmed_credential_beats_unconfirmed` | method | `tests/test_golden_path.py:62` | `def test_confirmed_credential_beats_unconfirmed(self)` |
| `test_critical_exploit_ranked_first_with_severity_cost` | method | `tests/test_golden_path.py:54` | `def test_critical_exploit_ranked_first_with_severity_cost(self)` |
| `test_deterministic_and_stable` | method | `tests/test_golden_path.py:79` | `def test_deterministic_and_stable(self)` |
| `test_lateral_relation_via_anchor` | method | `tests/test_golden_path.py:67` | `def test_lateral_relation_via_anchor(self)` |
| `test_load_artifact_tolerant_when_missing` | method | `tests/test_golden_path.py:109` | `def test_load_artifact_tolerant_when_missing(self)` |
| `test_priority_bands` | method | `tests/test_golden_path.py:136` | `def test_priority_bands(self)` |
| `test_push_and_dedupe` | method | `tests/test_golden_path.py:117` | `def test_push_and_dedupe(self)` |
| `test_runs_service_edges_ignored` | method | `tests/test_golden_path.py:73` | `def test_runs_service_edges_ignored(self)` |
| `advisor` | function | `tests/test_graph_advisor.py:133` | `def advisor(small_graph_path)` |
| `small_graph_data` | function | `tests/test_graph_advisor.py:34` | `def small_graph_data()` |
| `small_graph_path` | function | `tests/test_graph_advisor.py:126` | `def small_graph_path(tmp_path, small_graph_data)` |
| `test_advisor_did_you_mean_returns_close_labels` | function | `tests/test_graph_advisor.py:268` | `def test_advisor_did_you_mean_returns_close_labels(advisor)` |
| `test_advisor_god_nodes_ranks_by_degree` | function | `tests/test_graph_advisor.py:254` | `def test_advisor_god_nodes_ranks_by_degree(advisor)` |
| `test_advisor_handles_missing_graph_gracefully` | function | `tests/test_graph_advisor.py:280` | `def test_advisor_handles_missing_graph_gracefully(tmp_path)` |
| `test_advisor_neighbors_respects_depth` | function | `tests/test_graph_advisor.py:248` | `def test_advisor_neighbors_respects_depth(advisor)` |
| `test_advisor_neighbors_returns_layered_walk` | function | `tests/test_graph_advisor.py:239` | `def test_advisor_neighbors_returns_layered_walk(advisor)` |
| `test_advisor_reads_recent_commands_from_csv` | function | `tests/test_graph_advisor.py:292` | `def test_advisor_reads_recent_commands_from_csv(tmp_path, advisor)` |
| `test_advisor_search_returns_ranked_nodes` | function | `tests/test_graph_advisor.py:231` | `def test_advisor_search_returns_ranked_nodes(advisor)` |
| `test_advisor_suggest_next_walks_from_recent` | function | `tests/test_graph_advisor.py:260` | `def test_advisor_suggest_next_walks_from_recent(advisor)` |
| `test_advisor_summary_flags_empty_graph` | function | `tests/test_graph_advisor.py:199` | `def test_advisor_summary_flags_empty_graph(tmp_path)` |
| `test_advisor_summary_flags_stale_graph` | function | `tests/test_graph_advisor.py:212` | `def test_advisor_summary_flags_stale_graph(tmp_path)` |
| `test_advisor_summary_reports_topology` | function | `tests/test_graph_advisor.py:188` | `def test_advisor_summary_reports_topology(advisor)` |
| `test_advisor_truncate_respects_token_budget` | function | `tests/test_graph_advisor.py:274` | `def test_advisor_truncate_respects_token_budget(advisor)` |
| `test_format_god_nodes_handles_empty` | function | `tests/test_graph_advisor.py:322` | `def test_format_god_nodes_handles_empty()` |
| `test_format_neighbors_renders_when_match_found` | function | `tests/test_graph_advisor.py:316` | `def test_format_neighbors_renders_when_match_found(advisor)` |
| `test_format_search_table_renders_rows` | function | `tests/test_graph_advisor.py:309` | `def test_format_search_table_renders_rows(advisor)` |
| `test_format_suggestions_handles_empty` | function | `tests/test_graph_advisor.py:326` | `def test_format_suggestions_handles_empty()` |
| `test_index_builds_adjacency_and_degree` | function | `tests/test_graph_advisor.py:153` | `def test_index_builds_adjacency_and_degree(small_graph_data)` |
| `test_loader_resolves_explicit_path` | function | `tests/test_graph_advisor.py:138` | `def test_loader_resolves_explicit_path(tmp_path, small_graph_data)` |
| `test_loader_returns_none_when_missing` | function | `tests/test_graph_advisor.py:147` | `def test_loader_returns_none_when_missing(tmp_path)` |
| `test_real_graph_summary_when_available` | function | `tests/test_graph_advisor.py:333` | `def test_real_graph_summary_when_available()` |
| `test_scorer_prefers_prefix_match` | function | `tests/test_graph_advisor.py:174` | `def test_scorer_prefers_prefix_match(small_graph_data)` |
| `test_scorer_returns_empty_for_unrelated_query` | function | `tests/test_graph_advisor.py:182` | `def test_scorer_returns_empty_for_unrelated_query(small_graph_data)` |
| `_FakeAdvisor` | class | `tests/test_graph_overlay.py:25` | `class _FakeAdvisor` |
| `__init__` | method | `tests/test_graph_overlay.py:26` | `def __init__(self, available)` |
| `god_nodes` | method | `tests/test_graph_overlay.py:32` | `def god_nodes(self, limit)` |
| `is_available` | method | `tests/test_graph_overlay.py:29` | `def is_available(self)` |
| `neighbors` | method | `tests/test_graph_overlay.py:39` | `def neighbors(self, query, depth, limit)` |
| `runner` | function | `tests/test_graph_overlay.py:129` | `def runner(context)` |
| `test_build_state_uses_default_factory_signature` | function | `tests/test_graph_overlay.py:135` | `def test_build_state_uses_default_factory_signature()` |
| `test_focus_switches_to_neighbors_view` | function | `tests/test_graph_overlay.py:72` | `def test_focus_switches_to_neighbors_view()` |
| `test_focus_unknown_returns_no_match_message` | function | `tests/test_graph_overlay.py:85` | `def test_focus_unknown_returns_no_match_message()` |
| `test_god_nodes_view_returns_hubs` | function | `tests/test_graph_overlay.py:61` | `def test_god_nodes_view_returns_hubs()` |
| `test_is_available_returns_false_when_advisor_missing` | function | `tests/test_graph_overlay.py:55` | `def test_is_available_returns_false_when_advisor_missing()` |
| `test_launch_overlay_uses_runner` | function | `tests/test_graph_overlay.py:122` | `def test_launch_overlay_uses_runner()` |
| `test_toggle_view_round_trip` | function | `tests/test_graph_overlay.py:108` | `def test_toggle_view_round_trip()` |
| `test_unavailable_advisor_returns_no_graph_message` | function | `tests/test_graph_overlay.py:97` | `def test_unavailable_advisor_returns_no_graph_message()` |
| `TestAdvisoriesAndFeatures` | class | `tests/test_guardrails.py:116` | `class TestAdvisoriesAndFeatures` |
| `TestAptChainWiring` | class | `tests/test_guardrails.py:298` | `class TestAptChainWiring` |
| `TestCapacityEnvelope` | class | `tests/test_guardrails.py:36` | `class TestCapacityEnvelope` |
| `TestCheckpointLedger` | class | `tests/test_guardrails.py:83` | `class TestCheckpointLedger` |
| `TestGlobalHarness` | class | `tests/test_guardrails.py:229` | `class TestGlobalHarness` |
| `TestGuardHarness` | class | `tests/test_guardrails.py:144` | `class TestGuardHarness` |
| `TestLazyLoopWiring` | class | `tests/test_guardrails.py:243` | `class TestLazyLoopWiring` |
| `TestOrchestratorHarnessTab` | class | `tests/test_guardrails.py:344` | `class TestOrchestratorHarnessTab` |
| `TestTaskClass` | class | `tests/test_guardrails.py:26` | `class TestTaskClass` |
| `_drive` | function | `tests/test_guardrails.py:385` | `def _drive()` |
| `_fresh_global_harness` | method | `tests/test_guardrails.py:231` | `def _fresh_global_harness(self)` |
| `_fresh_global_harness` | method | `tests/test_guardrails.py:245` | `def _fresh_global_harness(self)` |
| `_fresh_global_harness` | method | `tests/test_guardrails.py:300` | `def _fresh_global_harness(self)` |
| `_load` | function | `tests/test_guardrails.py:361` | `def _load(target)` |
| `_save` | function | `tests/test_guardrails.py:364` | `def _save(data, target)` |
| `always_fails` | function | `tests/test_guardrails.py:182` | `def always_fails()` |
| `boom` | function | `tests/test_guardrails.py:154` | `def boom()` |
| `boom` | function | `tests/test_guardrails.py:190` | `def boom()` |
| `flaky` | function | `tests/test_guardrails.py:171` | `def flaky()` |
| `harness` | method | `tests/test_guardrails.py:146` | `def harness(self)` |
| `interrupted` | function | `tests/test_guardrails.py:198` | `def interrupted()` |
| `sandbox` | method | `tests/test_guardrails.py:346` | `def sandbox(self, tmp_path, monkeypatch)` |
| `test_admit_and_account_roundtrip` | method | `tests/test_guardrails.py:43` | `def test_admit_and_account_roundtrip(self)` |
| `test_apply_profile_configures_harness` | method | `tests/test_guardrails.py:250` | `def test_apply_profile_configures_harness(self, tmp_path, monkeypatch)` |
| `test_capture_rejects_blank_keys` | method | `tests/test_guardrails.py:112` | `def test_capture_rejects_blank_keys(self)` |
| `test_capture_restore_roundtrip` | method | `tests/test_guardrails.py:84` | `def test_capture_restore_roundtrip(self)` |
| `test_clear_returns_count` | method | `tests/test_guardrails.py:125` | `def test_clear_returns_count(self)` |
| `test_command_registered` | method | `tests/test_guardrails.py:353` | `def test_command_registered(self)` |
| `test_config_section_constant_shape` | method | `tests/test_guardrails.py:239` | `def test_config_section_constant_shape(self)` |
| `test_configure_clamps_and_accepts_names` | method | `tests/test_guardrails.py:75` | `def test_configure_clamps_and_accepts_names(self)` |
| `test_configure_from_payload_section` | method | `tests/test_guardrails.py:215` | `def test_configure_from_payload_section(self, harness)` |
| `test_core_gives_up_after_second_failure` | method | `tests/test_guardrails.py:181` | `def test_core_gives_up_after_second_failure(self, harness)` |
| `test_core_retries_once_after_warm_restart` | method | `tests/test_guardrails.py:168` | `def test_core_retries_once_after_warm_restart(self, harness)` |
| `test_core_without_checkpoint_never_retries` | method | `tests/test_guardrails.py:189` | `def test_core_without_checkpoint_never_retries(self, harness)` |
| `test_defaults_snapshot` | method | `tests/test_guardrails.py:37` | `def test_defaults_snapshot(self)` |
| `test_feature_gate_known_set` | method | `tests/test_guardrails.py:139` | `def test_feature_gate_known_set(self)` |
| `test_feature_gate_unknown_feature_never_suspends` | method | `tests/test_guardrails.py:132` | `def test_feature_gate_unknown_feature_never_suspends(self)` |
| `test_guardrails_persist_via_payload` | method | `tests/test_guardrails.py:358` | `def test_guardrails_persist_via_payload(self, monkeypatch, sandbox)` |
| `test_harness_tab_composes_headless` | method | `tests/test_guardrails.py:380` | `def test_harness_tab_composes_headless(self, sandbox, monkeypatch)` |
| `test_higher_tier_saturation_refuses_lower_tiers` | method | `tests/test_guardrails.py:58` | `def test_higher_tier_saturation_refuses_lower_tiers(self)` |
| `test_history_is_bounded` | method | `tests/test_guardrails.py:89` | `def test_history_is_bounded(self)` |
| `test_is_known_accepts_values_and_rejects_strays` | method | `tests/test_guardrails.py:30` | `def test_is_known_accepts_values_and_rejects_strays(self)` |
| `test_keyboard_interrupt_propagates` | method | `tests/test_guardrails.py:197` | `def test_keyboard_interrupt_propagates(self, harness)` |
| `test_mission_failure_degrades_with_advisory` | method | `tests/test_guardrails.py:153` | `def test_mission_failure_degrades_with_advisory(self, harness)` |
| `test_mission_success_accounts_usage` | method | `tests/test_guardrails.py:149` | `def test_mission_success_accounts_usage(self, harness)` |
| `test_notice_is_bounded_newest_first` | method | `tests/test_guardrails.py:117` | `def test_notice_is_bounded_newest_first(self)` |
| `test_priority_reservation_refuses_lower_tiers` | method | `tests/test_guardrails.py:204` | `def test_priority_reservation_refuses_lower_tiers(self, harness)` |
| `test_reclaim_purges_support_only` | method | `tests/test_guardrails.py:66` | `def test_reclaim_purges_support_only(self)` |
| `test_recovery_guard_returns_none_when_refused` | method | `tests/test_guardrails.py:305` | `def test_recovery_guard_returns_none_when_refused(self, monkeypatch)` |
| `test_restore_missing_is_none` | method | `tests/test_guardrails.py:96` | `def test_restore_missing_is_none(self)` |
| `test_round_guard_halt_maps_to_degraded_abort` | method | `tests/test_guardrails.py:285` | `def test_round_guard_halt_maps_to_degraded_abort(self, tmp_path, monkeypatch)` |
| `test_saturated_tier_refuses_admission` | method | `tests/test_guardrails.py:51` | `def test_saturated_tier_refuses_admission(self)` |
| `test_singleton_shared` | method | `tests/test_guardrails.py:236` | `def test_singleton_shared(self)` |
| `test_support_refused_while_render_suspended` | method | `tests/test_guardrails.py:161` | `def test_support_refused_while_render_suspended(self, harness)` |
| `test_tier_ordering_is_strict` | method | `tests/test_guardrails.py:27` | `def test_tier_ordering_is_strict(self)` |
| `test_warm_restart_purges_support_and_notifies` | method | `tests/test_guardrails.py:220` | `def test_warm_restart_purges_support_and_notifies(self, harness)` |
| `test_warm_restart_restores_and_counts` | method | `tests/test_guardrails.py:99` | `def test_warm_restart_restores_and_counts(self)` |
| `test_warm_restart_without_key_reports_unrestored` | method | `tests/test_guardrails.py:107` | `def test_warm_restart_without_key_reports_unrestored(self)` |
| `test_worker_guard_maps_refusal_to_degraded_outcome` | method | `tests/test_guardrails.py:266` | `def test_worker_guard_maps_refusal_to_degraded_outcome(self, tmp_path, monkeypatch)` |
| `SafeHtmlHelperTests` | class | `tests/test_gui_xss_sinks.py:26` | `class SafeHtmlHelperTests(TestCase)` |
| `SinkSanitizationTests` | class | `tests/test_gui_xss_sinks.py:37` | `class SinkSanitizationTests(TestCase)` |
| `_read_template` | function | `tests/test_gui_xss_sinks.py:21` | `def _read_template()` |
| `test_helper_is_defined_exactly_once` | method | `tests/test_gui_xss_sinks.py:27` | `def test_helper_is_defined_exactly_once(self)` |
| `test_helper_prefers_dompurify_with_text_fallback` | method | `tests/test_gui_xss_sinks.py:31` | `def test_helper_prefers_dompurify_with_text_fallback(self)` |
| `test_no_raw_error_interpolation` | method | `tests/test_gui_xss_sinks.py:50` | `def test_no_raw_error_interpolation(self)` |
| `test_no_raw_html_interpolation` | method | `tests/test_gui_xss_sinks.py:43` | `def test_no_raw_html_interpolation(self)` |
| `test_no_raw_output_interpolation` | method | `tests/test_gui_xss_sinks.py:61` | `def test_no_raw_output_interpolation(self)` |
| `test_no_raw_response_interpolation` | method | `tests/test_gui_xss_sinks.py:38` | `def test_no_raw_response_interpolation(self)` |
| `sandbox` | function | `tests/test_gym_cli.py:11` | `def sandbox(tmp_path, monkeypatch)` |
| `test_atomic_shell_marks_target_compromised` | function | `tests/test_gym_cli.py:123` | `def test_atomic_shell_marks_target_compromised(sandbox, monkeypatch, capsys)` |
| `test_gym_start_status_stop_lifecycle` | function | `tests/test_gym_cli.py:39` | `def test_gym_start_status_stop_lifecycle(sandbox, capsys)` |
| `test_gym_status_explains_live_shell_without_gym` | function | `tests/test_gym_cli.py:82` | `def test_gym_status_explains_live_shell_without_gym(sandbox, monkeypatch, capsys)` |
| `test_gym_status_filters_hosts_by_current_target` | function | `tests/test_gym_cli.py:103` | `def test_gym_status_filters_hosts_by_current_target(sandbox, monkeypatch, capsys)` |
| `test_gym_stop_all_and_by_name` | function | `tests/test_gym_cli.py:65` | `def test_gym_stop_all_and_by_name(sandbox, capsys)` |

Next: [SYMBOLS_p38.md](SYMBOLS_p38.md)
