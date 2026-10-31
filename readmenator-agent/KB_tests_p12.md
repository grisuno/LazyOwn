# Subsystem: tests (page 12 of 23)
Previous: [KB_tests_p11.md](KB_tests_p11.md)

## tests/test_intelligence_engine.py
- Doc: Tests for IntelligenceEngine — collection, analysis, intelligence, dissemination.
- Layer: testing
- Language: py
- Symbols:
  - `engine` (function, line 19) `def engine()`
  - `nmap_xml` (function, line 24) `def nmap_xml(tmp_path)`
  - `TestCollection` (class, line 45) `class TestCollection`
  - `TestAnalysis` (class, line 108) `class TestAnalysis`
  - `TestIntelligenceProduction` (class, line 159) `class TestIntelligenceProduction`
  - `TestCounterIntelligence` (class, line 178) `class TestCounterIntelligence`
  - `TestFullCycle` (class, line 198) `class TestFullCycle`
  - `TestPlaceholderFiltering` (class, line 215) `class TestPlaceholderFiltering`
  - `test_collect_from_scan_services` (method, line 46) `def test_collect_from_scan_services(self, engine, nmap_xml)`
  - `test_collect_from_scan_os` (method, line 56) `def test_collect_from_scan_os(self, engine, nmap_xml)`
  - `test_collect_from_scan_domain` (method, line 63) `def test_collect_from_scan_domain(self, engine, nmap_xml)`
  - `test_collect_from_scan_hosts` (method, line 70) `def test_collect_from_scan_hosts(self, engine, nmap_xml)`
  - `test_collect_from_scan_missing_xml` (method, line 76) `def test_collect_from_scan_missing_xml(self, engine)`
  - `test_collect_from_tool_parses_creds` (method, line 81) `def test_collect_from_tool_parses_creds(self, engine)`
  - `test_collect_from_tool_filters_placeholders` (method, line 86) `def test_collect_from_tool_filters_placeholders(self, engine)`
  - `test_collect_from_factstore` (method, line 91) `def test_collect_from_factstore(self, engine, tmp_path)`
  - `test_analyze_produces_assessments` (method, line 109) `def test_analyze_produces_assessments(self, engine, nmap_xml)`
  - `test_analyze_maps_apache_cve` (method, line 115) `def test_analyze_maps_apache_cve(self, engine)`
  - `test_analyze_correlates_creds_to_hosts` (method, line 131) `def test_analyze_correlates_creds_to_hosts(self, engine)`
  - `test_analyze_ranks_targets` (method, line 143) `def test_analyze_ranks_targets(self, engine)`
  - `test_produce_intelligence_grades_assessments` (method, line 160) `def test_produce_intelligence_grades_assessments(self, engine)`
  - `test_credential_exposure_detected` (method, line 179) `def test_credential_exposure_detected(self, engine)`
  - `test_high_scan_volume_detected` (method, line 188) `def test_high_scan_volume_detected(self, engine)`
  - `test_run_full_cycle_returns_summary` (method, line 199) `def test_run_full_cycle_returns_summary(self, engine, nmap_xml)`
  - `test_get_intel_report_structured` (method, line 205) `def test_get_intel_report_structured(self, engine, nmap_xml)`
  - `test_is_placeholder_detects_change_me` (method, line 216) `def test_is_placeholder_detects_change_me(self, engine)`
  - `test_is_placeholder_rejects_real_values` (method, line 220) `def test_is_placeholder_rejects_real_values(self, engine)`
- Depends on: `modules/intelligence_engine.py`

## tests/test_journal.py
- Doc: Tests for the GitHub Discussions engineering journal.
- Layer: testing
- Language: py
- Symbols:
  - `FakeRunner` (class, line 16) `class FakeRunner`
  - `_success_responses` (function, line 34) `def _success_responses()`
  - `test_config_from_remote_slug` (function, line 51) `def test_config_from_remote_slug()`
  - `test_config_rejects_bare_name` (function, line 58) `def test_config_rejects_bare_name()`
  - `test_post_entry_uses_resolved_ids` (function, line 64) `def test_post_entry_uses_resolved_ids()`
  - `test_entries_returns_nodes` (function, line 73) `def test_entries_returns_nodes()`
  - `test_missing_category_raises` (function, line 81) `def test_missing_category_raises()`
  - `test_graphql_errors_raise` (function, line 93) `def test_graphql_errors_raise()`
  - `__init__` (method, line 19) `def __init__(self, responses)`
  - `__call__` (method, line 24) `def __call__(self, args)`
- Depends on: `scripts/journal.py`

## tests/test_killchain.py
- Doc: Tests for cli/killchain.py.
- Layer: testing
- Language: py
- Symbols:
  - `_states` (function, line 28) `def _states(progress)`
  - `test_empty_events_all_pending_without_world` (function, line 32) `def test_empty_events_all_pending_without_world()`
  - `test_current_phase_from_step_events` (function, line 38) `def test_current_phase_from_step_events()`
  - `test_phase_advance_event_sets_current` (function, line 49) `def test_phase_advance_event_sets_current()`
  - `test_activity_and_reward_accumulate` (function, line 62) `def test_activity_and_reward_accumulate()`
  - `test_world_phase_fallback_when_no_events` (function, line 75) `def test_world_phase_fallback_when_no_events()`
  - `test_explicit_completed_phases_respected` (function, line 81) `def test_explicit_completed_phases_respected()`
  - `test_unknown_phase_in_event_is_ignored` (function, line 86) `def test_unknown_phase_in_event_is_ignored()`
  - `test_non_dict_payload_is_tolerated` (function, line 92) `def test_non_dict_payload_is_tolerated()`
- Depends on: `cli/killchain.py`

## tests/test_killchain_auto_refresh.py
- Doc: BDD-style tests for the periodic kill-chain auto-refresh in the tips engine.
- Layer: testing
- Language: py
- Symbols:
  - `_engine` (function, line 12) `def _engine()`
  - `TestPeriodicAutoRefresh` (class, line 22) `class TestPeriodicAutoRefresh`
  - `test_shows_immediately_on_phase_change` (method, line 23) `def test_shows_immediately_on_phase_change(self)`
  - `test_shows_on_cadence_without_phase_change` (method, line 31) `def test_shows_on_cadence_without_phase_change(self)`
  - `test_cadence_below_every_surpresses` (method, line 41) `def test_cadence_below_every_surpresses(self)`
  - `test_phase_change_beats_periodic_cadence` (method, line 50) `def test_phase_change_beats_periodic_cadence(self)`
  - `test_disabled_engine_never_shows` (method, line 59) `def test_disabled_engine_never_shows(self)`
  - `test_zero_every_and_no_phase_change_never_shows` (method, line 67) `def test_zero_every_and_no_phase_change_never_shows(self)`
- Depends on: `cli/tips_engine.py`

## tests/test_killchain_gap_signal.py
- Doc: Tests for :class:`cli.recommendation_signals.KillchainGapSignal`.
- Layer: testing
- Language: py
- Symbols:
  - `sessions_dir` (function, line 23) `def sessions_dir()`
  - `_write_world_model` (function, line 28) `def _write_world_model(sessions_dir, data)`
  - `TestKillchainGapSignalConstruction` (class, line 32) `class TestKillchainGapSignalConstruction`
  - `TestGapExploitedNoPrivesc` (class, line 38) `class TestGapExploitedNoPrivesc`
  - `TestGapOwnedNoCreds` (class, line 82) `class TestGapOwnedNoCreds`
  - `TestGapScanNoEnum` (class, line 110) `class TestGapScanNoEnum`
  - `TestGapCredsNoLateral` (class, line 141) `class TestGapCredsNoLateral`
  - `TestKillchainGapSignalIntegration` (class, line 169) `class TestKillchainGapSignalIntegration`
  - `test_name_is_gap_source` (method, line 33) `def test_name_is_gap_source(self)`
  - `test_exploited_linux_recommends_linpeas` (method, line 39) `def test_exploited_linux_recommends_linpeas(self, sessions_dir)`
  - `test_exploited_windows_recommends_winpeas` (method, line 51) `def test_exploited_windows_recommends_winpeas(self, sessions_dir)`
  - `test_unscanned_host_no_proposals` (method, line 63) `def test_unscanned_host_no_proposals(self, sessions_dir)`
  - `test_no_world_model_returns_empty` (method, line 75) `def test_no_world_model_returns_empty(self, sessions_dir)`
  - `test_owned_no_credentials_recommends_lazydump` (method, line 83) `def test_owned_no_credentials_recommends_lazydump(self, sessions_dir)`
  - `test_owned_with_credentials_no_proposals` (method, line 96) `def test_owned_with_credentials_no_proposals(self, sessions_dir)`
  - `test_scanned_no_enum_recommends_gobuster` (method, line 111) `def test_scanned_no_enum_recommends_gobuster(self, sessions_dir)`
  - `test_scanned_with_enum_recent_no_proposals` (method, line 123) `def test_scanned_with_enum_recent_no_proposals(self, sessions_dir)`
  - `test_credentials_no_lateral_recommends_crackmapexec` (method, line 142) `def test_credentials_no_lateral_recommends_crackmapexec(self, sessions_dir)`
  - `test_no_credentials_no_lateral_proposals` (method, line 155) `def test_no_credentials_no_lateral_proposals(self, sessions_dir)`
  - `test_multiple_gaps_detected_simultaneously` (method, line 170) `def test_multiple_gaps_detected_simultaneously(self, sessions_dir)`
- Depends on: `cli/recommendation.py`, `cli/recommendation_signals.py`

## tests/test_killchain_snapshot.py
- Doc: BDD-style tests for the unified kill-chain snapshot contract.
- Layer: testing
- Language: py
- Symbols:
  - `_seed_snapshot` (function, line 17) `def _seed_snapshot(path, phase, completed, current)`
  - `_states` (function, line 37) `def _states(snapshot)`
  - `_encrypt_at` (function, line 41) `def _encrypt_at(path, password, salt)`
  - `TestKillChainSnapshot` (class, line 52) `class TestKillChainSnapshot`
  - `TestEncryptedStateTransparency` (class, line 102) `class TestEncryptedStateTransparency`
  - `test_empty_snapshot_defaults_to_recon` (method, line 53) `def test_empty_snapshot_defaults_to_recon(self, tmp_path)`
  - `test_snapshot_reflects_explicit_phase_and_completed` (method, line 64) `def test_snapshot_reflects_explicit_phase_and_completed(self, tmp_path)`
  - `test_snapshot_is_json_serialisable` (method, line 80) `def test_snapshot_is_json_serialisable(self, tmp_path)`
  - `test_advance_then_snapshot_is_consistent` (method, line 90) `def test_advance_then_snapshot_is_consistent(self, tmp_path)`
  - `test_read_state_dict_decrypts_at_rest` (method, line 103) `def test_read_state_dict_decrypts_at_rest(self, tmp_path, monkeypatch)`
  - `test_write_state_dict_persists_fernet_token` (method, line 122) `def test_write_state_dict_persists_fernet_token(self, tmp_path, monkeypatch)`
  - `test_write_state_dict_then_engine_encrypt_unwraps_nested` (method, line 138) `def test_write_state_dict_then_engine_encrypt_unwraps_nested(self, tmp_path, monkeypatch)`
  - `test_missing_file_reads_empty` (method, line 157) `def test_missing_file_reads_empty(self, tmp_path)`
  - `test_encrypted_without_password_reads_empty` (method, line 165) `def test_encrypted_without_password_reads_empty(self, tmp_path, monkeypatch)`
- Depends on: `modules/killchain.py`, `modules/world_model.py`

## tests/test_killchain_unified.py
- Doc: Tests for unified killchain phase: read_phase, write_phase, phase mapping helpers.
- Layer: testing
- Language: py
- Symbols:
  - `TestPhaseMapping` (class, line 20) `class TestPhaseMapping`
  - `TestWritePhaseWithWorldModel` (class, line 48) `class TestWritePhaseWithWorldModel`
  - `test_engagement_phase_to_cli_maps_all` (method, line 21) `def test_engagement_phase_to_cli_maps_all(self)`
  - `test_cli_phase_to_host_state_maps_correctly` (method, line 30) `def test_cli_phase_to_host_state_maps_correctly(self)`
  - `test_phase_rank_returns_correct_index` (method, line 41) `def test_phase_rank_returns_correct_index(self)`
  - `sessions_dir` (method, line 52) `def sessions_dir(self)`
  - `test_write_phase_advances_hosts` (method, line 80) `def test_write_phase_advances_hosts(self, sessions_dir)`
  - `test_write_phase_invalid_returns_false` (method, line 96) `def test_write_phase_invalid_returns_false(self, sessions_dir)`
  - `test_write_phase_completed_phases_tracks_progress` (method, line 100) `def test_write_phase_completed_phases_tracks_progress(self, sessions_dir)`
- Depends on: `cli/ops_commands.py`, `modules/world_model.py`

## tests/test_killchain_unified_v2.py
- Doc: Comprehensive tests for modules.killchain — the unified single source of truth.
- Layer: testing
- Language: py
- Symbols:
  - `TestKillChainConfig` (class, line 32) `class TestKillChainConfig`
  - `TestKillChainCurrentPhase` (class, line 104) `class TestKillChainCurrentPhase`
  - `TestKillChainAdvancePhase` (class, line 185) `class TestKillChainAdvancePhase`
  - `TestKillChainGetProgress` (class, line 296) `class TestKillChainGetProgress`
  - `TestKillChainHelpers` (class, line 364) `class TestKillChainHelpers`
  - `TestPhaseStatusDataclass` (class, line 411) `class TestPhaseStatusDataclass`
  - `test_phases_is_8_tuple` (method, line 35) `def test_phases_is_8_tuple(self)`
  - `test_phases_are_in_correct_kill_chain_order` (method, line 41) `def test_phases_are_in_correct_kill_chain_order(self)`
  - `test_compact_phases_are_in_correct_order` (method, line 45) `def test_compact_phases_are_in_correct_order(self)`
  - `test_all_phases_have_labels` (method, line 49) `def test_all_phases_have_labels(self)`
  - `test_all_phases_have_colors` (method, line 54) `def test_all_phases_have_colors(self)`
  - `test_all_phases_have_rich_colors` (method, line 59) `def test_all_phases_have_rich_colors(self)`
  - `test_engagement_to_cli_covers_all_engagement_phases` (method, line 63) `def test_engagement_to_cli_covers_all_engagement_phases(self)`
  - `test_cli_to_host_state_returns_expected` (method, line 71) `def test_cli_to_host_state_returns_expected(self)`
  - `test_phase_index_valid_and_invalid` (method, line 81) `def test_phase_index_valid_and_invalid(self)`
  - `test_is_valid_phase` (method, line 87) `def test_is_valid_phase(self)`
  - `test_compact_phases_and_labels` (method, line 92) `def test_compact_phases_and_labels(self)`
  - `test_world_model_path` (method, line 97) `def test_world_model_path(self)`
  - `_reset_wm_singleton` (method, line 108) `def _reset_wm_singleton(self)`
  - `test_returns_recon_when_no_world_model_exists` (method, line 119) `def test_returns_recon_when_no_world_model_exists(self)`
  - `test_reads_from_world_model_host_state` (method, line 126) `def test_reads_from_world_model_host_state(self)`
  - `test_raw_json_override_wins_when_higher_rank` (method, line 141) `def test_raw_json_override_wins_when_higher_rank(self)`
  - `test_raw_json_override_ignored_when_lower_rank` (method, line 157) `def test_raw_json_override_ignored_when_lower_rank(self)`
  - `test_falls_back_to_legacy_phase_key` (method, line 173) `def test_falls_back_to_legacy_phase_key(self)`
  - `_reset_wm_singleton` (method, line 189) `def _reset_wm_singleton(self)`
  - `test_advance_writes_current_phase_and_phase_keys` (method, line 200) `def test_advance_writes_current_phase_and_phase_keys(self)`
  - `test_advance_tracks_completed_phases` (method, line 216) `def test_advance_tracks_completed_phases(self)`
  - `test_advance_invalid_phase_returns_false` (method, line 234) `def test_advance_invalid_phase_returns_false(self)`
  - `test_advance_advances_world_model_hosts` (method, line 244) `def test_advance_advances_world_model_hosts(self)`
  - `test_advance_with_host_does_not_touch_unrelated_hosts` (method, line 261) `def test_advance_with_host_does_not_touch_unrelated_hosts(self)`
  - `test_advance_does_not_downgrade_cached_world_model_state` (method, line 277) `def test_advance_does_not_downgrade_cached_world_model_state(self)`
  - `_reset_wm_singleton` (method, line 300) `def _reset_wm_singleton(self)`
  - `test_all_pending_when_nothing_done` (method, line 311) `def test_all_pending_when_nothing_done(self)`
  - `test_progress_reflects_completed_and_active` (method, line 324) `def test_progress_reflects_completed_and_active(self)`
  - `test_progress_has_colors_and_labels` (method, line 348) `def test_progress_has_colors_and_labels(self)`
  - `test_phases_for_display_returns_triples` (method, line 367) `def test_phases_for_display_returns_triples(self)`
  - `test_compact_progress_returns_string` (method, line 377) `def test_compact_progress_returns_string(self)`
  - `test_engagement_phase_to_cli_maps_all` (method, line 383) `def test_engagement_phase_to_cli_maps_all(self)`
  - `test_cli_phase_to_host_state_maps_all` (method, line 392) `def test_cli_phase_to_host_state_maps_all(self)`
  - `test_get_killchain_returns_class` (method, line 400) `def test_get_killchain_returns_class(self)`
  - `test_phase_index_returns_correct` (method, line 404) `def test_phase_index_returns_correct(self)`
  - `test_phase_status_is_immutable` (method, line 414) `def test_phase_status_is_immutable(self)`
  - `test_phase_status_fields_match_config` (method, line 419) `def test_phase_status_fields_match_config(self)`
- Depends on: `modules/killchain.py`, `modules/world_model.py`

## tests/test_lab_target_visibility.py
- Doc: Lab target visibility: start/status always show the container IP.
- Layer: testing
- Language: py
- Symbols:
  - `test_start_on_running_lab_reports_ip` (function, line 14) `def test_start_on_running_lab_reports_ip(capsys, monkeypatch)`
  - `test_status_reports_ip` (function, line 27) `def test_status_reports_ip(capsys, monkeypatch)`
- Depends on: `cli/commands/lab.py`

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
  - `test_lazy_tools_dispatched` (method, line 72) `def test_lazy_tools_dispatched(self)`
  - `test_hermes_bridge_exposes_lazy_tools` (method, line 78) `def test_hermes_bridge_exposes_lazy_tools(self)`
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


Next: [KB_tests_p13.md](KB_tests_p13.md)
