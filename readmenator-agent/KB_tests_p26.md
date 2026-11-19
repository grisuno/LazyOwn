# Subsystem: tests (page 26 of 27)
Previous: [KB_tests_p25.md](KB_tests_p25.md)

## tests/test_sync_doc_stats.py
- Doc: Tests for the documentation-stats single source of truth.
- Layer: testing
- Language: py
- Symbols:
  - `_load_module` (function, line 20) `def _load_module()`
  - `mod` (function, line 28) `def mod()`
  - `test_canonical_command_count_reads_index` (function, line 32) `def test_canonical_command_count_reads_index(mod, tmp_path)`
  - `test_measure_stats_command_count_matches_index` (function, line 39) `def test_measure_stats_command_count_matches_index(mod, tmp_path)`
  - `test_sync_check_does_not_write` (function, line 67) `def test_sync_check_does_not_write(mod, tmp_path)`
  - `test_sync_apply_rewrites_when_stale` (function, line 80) `def test_sync_apply_rewrites_when_stale(mod, tmp_path)`
  - `test_render_formats_template` (function, line 92) `def test_render_formats_template(mod)`

## tests/test_target_os.py
- Doc: Contract tests for modules/loop/target_os.py.
- Language: py
- Symbols:
  - `_FakeCompleted` (class, line 17) `class _FakeCompleted`
  - `_FakeWorldModel` (class, line 25) `class _FakeWorldModel`
  - `_run_detect` (function, line 39) `def _run_detect(monkeypatch, ping_output)`
  - `test_detect_linux_ttl` (function, line 53) `def test_detect_linux_ttl(monkeypatch)`
  - `test_detect_windows_ttl` (function, line 57) `def test_detect_windows_ttl(monkeypatch)`
  - `test_detect_unknown_high_ttl` (function, line 61) `def test_detect_unknown_high_ttl(monkeypatch)`
  - `test_detect_unknown_without_ttl` (function, line 65) `def test_detect_unknown_without_ttl(monkeypatch)`
  - `test_detect_unknown_on_exception` (function, line 69) `def test_detect_unknown_on_exception(monkeypatch)`
  - `test_os_id_for` (function, line 85) `def test_os_id_for(label, expected)`
  - `_collect_emit` (function, line 89) `def _collect_emit()`
  - `test_persist_unknown_only_emits` (function, line 98) `def test_persist_unknown_only_emits(tmp_path)`
  - `test_persist_known_writes_all` (function, line 120) `def test_persist_known_writes_all(tmp_path)`
  - `test_persist_known_skips_payload_when_unchanged` (function, line 158) `def test_persist_known_skips_payload_when_unchanged(tmp_path)`
  - `test_persist_known_respects_existing_os_hint` (function, line 185) `def test_persist_known_respects_existing_os_hint(tmp_path)`
  - `__init__` (method, line 20) `def __init__(self, stdout, stderr)`
  - `__init__` (method, line 28) `def __init__(self, snapshot)`
  - `snapshot` (method, line 32) `def snapshot(self)`
  - `update_host` (method, line 35) `def update_host(self, target)`
  - `_fake_run` (function, line 42) `def _fake_run()`
  - `_boom` (function, line 70) `def _boom()`
  - `_emit` (function, line 92) `def _emit(name, payload)`
  - `_fake_save` (function, line 128) `def _fake_save(payload, path)`
- Depends on: `core/config.py`, `modules/loop/__init__.py`

## tests/test_themes.py
- Doc: Tests for cli/themes.py.
- Layer: testing
- Language: py
- Symbols:
  - `test_themes_registry_contains_required_entries` (function, line 24) `def test_themes_registry_contains_required_entries()`
  - `test_get_theme_returns_default_for_unknown_name` (function, line 30) `def test_get_theme_returns_default_for_unknown_name()`
  - `test_get_theme_is_case_insensitive` (function, line 35) `def test_get_theme_is_case_insensitive()`
  - `test_theme_from_payload_none_yields_default` (function, line 40) `def test_theme_from_payload_none_yields_default()`
  - `test_theme_from_payload_picks_named_theme` (function, line 45) `def test_theme_from_payload_picks_named_theme()`
  - `test_theme_dataclass_is_immutable` (function, line 51) `def test_theme_dataclass_is_immutable()`
- Depends on: `cli/themes.py`

## tests/test_timeline_browser.py
- Doc: Tests for cli/timeline_browser.py.
- Layer: testing
- Language: py
- Symbols:
  - `_write_report` (function, line 24) `def _write_report(path, rows)`
  - `test_reader_returns_empty_when_csv_missing` (function, line 34) `def test_reader_returns_empty_when_csv_missing(tmp_path)`
  - `test_reader_parses_rows` (function, line 40) `def test_reader_parses_rows(tmp_path)`
  - `test_state_filters_across_columns` (function, line 67) `def test_state_filters_across_columns(tmp_path)`
  - `test_state_filter_empty_returns_all` (function, line 84) `def test_state_filter_empty_returns_all(tmp_path)`
  - `test_column_value_falls_back_through_source_keys` (function, line 92) `def test_column_value_falls_back_through_source_keys(tmp_path)`
  - `test_state_reload_drops_cache` (function, line 102) `def test_state_reload_drops_cache(tmp_path)`
  - `test_reader_truncates_long_field_values` (function, line 113) `def test_reader_truncates_long_field_values(tmp_path)`
- Depends on: `cli/timeline_browser.py`

## tests/test_tips_engine.py
- Doc: Tests for cli.tips_engine — unified post-command suggestion engine.
- Layer: testing
- Language: py
- Symbols:
  - `tmp_sessions` (function, line 39) `def tmp_sessions()`
  - `config` (function, line 48) `def config()`
  - `engine` (function, line 70) `def engine(config, tmp_sessions)`
  - `TestTipsConfig` (class, line 77) `class TestTipsConfig`
  - `TestEngagementState` (class, line 104) `class TestEngagementState`
  - `TestTipsEngineConstruction` (class, line 119) `class TestTipsEngineConstruction`
  - `TestKillChainHints` (class, line 138) `class TestKillChainHints`
  - `TestChainActiveSuppression` (class, line 152) `class TestChainActiveSuppression`
  - `TestHintsLevelGating` (class, line 200) `class TestHintsLevelGating`
  - `TestELOScoring` (class, line 280) `class TestELOScoring`
  - `TestVRIThresholds` (class, line 305) `class TestVRIThresholds`
  - `TestCommandsSeenSanitisation` (class, line 318) `class TestCommandsSeenSanitisation`
  - `TestSkipCommands` (class, line 342) `class TestSkipCommands`
  - `TestCommandNameRegex` (class, line 357) `class TestCommandNameRegex`
  - `TestTruncate` (class, line 373) `class TestTruncate`
  - `TestKarmaNames` (class, line 385) `class TestKarmaNames`
  - `TestBuildDefaultConfig` (class, line 396) `class TestBuildDefaultConfig`
  - `test_default_config_has_sensible_values` (method, line 78) `def test_default_config_has_sensible_values(self)`
  - `test_build_default_tips_config_populates_tables` (method, line 86) `def test_build_default_tips_config_populates_tables(self)`
  - `test_default_state` (method, line 105) `def test_default_state(self)`
  - `test_badges_field_defaults_to_list` (method, line 113) `def test_badges_field_defaults_to_list(self)`
  - `test_engine_initialises_with_config` (method, line 120) `def test_engine_initialises_with_config(self, config)`
  - `test_engine_can_disable` (method, line 125) `def test_engine_can_disable(self, config)`
  - `test_render_skips_disabled_engine` (method, line 130) `def test_render_skips_disabled_engine(self, config, capsys)`
  - `test_ping_suggests_lazynmap` (method, line 139) `def test_ping_suggests_lazynmap(self, engine)`
  - `test_lazynmap_suggests_auto_pwn` (method, line 143) `def test_lazynmap_suggests_auto_pwn(self, engine)`
  - `test_auto_pwn_suggests_hunt` (method, line 147) `def test_auto_pwn_suggests_hunt(self, engine)`
  - `_render_with_surfaces_stubbed` (method, line 153) `def _render_with_surfaces_stubbed(self, engine)`
  - `test_chain_active_suppresses_competing_suggestion_surfaces` (method, line 179) `def test_chain_active_suppresses_competing_suggestion_surfaces(self, engine)`
  - `test_chain_inactive_keeps_all_surfaces` (method, line 190) `def test_chain_inactive_keeps_all_surfaces(self, engine)`
  - `_stub_surfaces` (method, line 201) `def _stub_surfaces(self, engine)`
  - `test_hints_level_constants` (method, line 225) `def test_hints_level_constants(self)`
  - `test_default_config_is_on` (method, line 232) `def test_default_config_is_on(self)`
  - `test_off_suppresses_all_surfaces` (method, line 235) `def test_off_suppresses_all_surfaces(self, engine)`
  - `test_minimal_runs_autosuggest_only` (method, line 245) `def test_minimal_runs_autosuggest_only(self, engine)`
  - `test_on_runs_every_surface` (method, line 255) `def test_on_runs_every_surface(self, engine)`
  - `test_invalid_level_falls_back_to_on` (method, line 264) `def test_invalid_level_falls_back_to_on(self, engine)`
  - `test_get_hints_level_reads_config` (method, line 271) `def test_get_hints_level_reads_config(self, engine)`
  - `test_get_hints_level_defaults_for_invalid` (method, line 275) `def test_get_hints_level_defaults_for_invalid(self, engine)`
  - `test_base_elo_awarded` (method, line 281) `def test_base_elo_awarded(self, engine)`
  - `test_high_value_command_bonus` (method, line 285) `def test_high_value_command_bonus(self, engine)`
  - `test_first_time_bonus` (method, line 289) `def test_first_time_bonus(self, config)`
  - `test_new_phase_bonus` (method, line 294) `def test_new_phase_bonus(self, config)`
  - `test_no_double_count_first_time_plus_new_phase` (method, line 299) `def test_no_double_count_first_time_plus_new_phase(self, config)`
  - `test_next_threshold_increases` (method, line 306) `def test_next_threshold_increases(self, engine)`
  - `test_next_threshold_never_less_than_two` (method, line 312) `def test_next_threshold_never_less_than_two(self, engine)`
  - `test_valid_commands_kept` (method, line 319) `def test_valid_commands_kept(self)`
  - `test_invalid_entries_dropped` (method, line 325) `def test_invalid_entries_dropped(self)`
  - `test_known_filter_drops_unknown` (method, line 332) `def test_known_filter_drops_unknown(self)`
  - `test_skip_set_contains_common_noise` (method, line 343) `def test_skip_set_contains_common_noise(self)`
  - `test_ping_not_skipped` (method, line 350) `def test_ping_not_skipped(self)`
  - `test_auto_pwn_not_skipped` (method, line 353) `def test_auto_pwn_not_skipped(self)`
  - `test_valid_command_names` (method, line 358) `def test_valid_command_names(self)`
  - `test_invalid_command_names` (method, line 365) `def test_invalid_command_names(self)`
  - `test_short_value_untouched` (method, line 374) `def test_short_value_untouched(self)`
  - `test_long_value_truncated` (method, line 377) `def test_long_value_truncated(self)`
  - `test_empty_value` (method, line 381) `def test_empty_value(self)`
  - `test_noob_at_zero` (method, line 386) `def test_noob_at_zero(self)`
  - `test_rookie_at_thousand` (method, line 389) `def test_rookie_at_thousand(self)`
  - `test_godlike_above_6000` (method, line 392) `def test_godlike_above_6000(self)`
  - `test_config_includes_automation_commands` (method, line 397) `def test_config_includes_automation_commands(self)`
  - `test_config_has_high_value_for_new_commands` (method, line 410) `def test_config_has_high_value_for_new_commands(self)`
  - `test_config_has_session_tips` (method, line 417) `def test_config_has_session_tips(self)`
  - `stub` (function, line 164) `def stub(name)`
  - `stub` (function, line 211) `def stub(name)`
  - `record` (function, line 165) `def record()`
  - `record` (function, line 212) `def record()`
- Depends on: `cli/tips_engine.py`

## tests/test_toast_bus.py
- Doc: Tests for cli/toast_bus.py.
- Layer: testing
- Language: py
- Symbols:
  - `_write_jsonl` (function, line 34) `def _write_jsonl(path, records)`
  - `_append_jsonl` (function, line 42) `def _append_jsonl(path, records)`
  - `test_state_round_trip` (function, line 49) `def test_state_round_trip(tmp_path)`
  - `test_state_clamps_negative_offsets` (function, line 59) `def test_state_clamps_negative_offsets(tmp_path)`
  - `test_reader_returns_unseen_events_only` (function, line 67) `def test_reader_returns_unseen_events_only(tmp_path)`
  - `test_reader_handles_malformed_lines` (function, line 80) `def test_reader_handles_malformed_lines(tmp_path)`
  - `test_formatter_uses_theme_role_for_severity` (function, line 91) `def test_formatter_uses_theme_role_for_severity()`
  - `test_bus_render_respects_per_tick_budget` (function, line 109) `def test_bus_render_respects_per_tick_budget(tmp_path)`
  - `test_bus_render_disabled_returns_zero` (function, line 127) `def test_bus_render_disabled_returns_zero(tmp_path)`
  - `test_bus_mark_all_seen_consumes_pending` (function, line 140) `def test_bus_mark_all_seen_consumes_pending(tmp_path)`
  - `test_toasts_enabled_default_true` (function, line 157) `def test_toasts_enabled_default_true()`
  - `test_render_toasts_returns_count` (function, line 165) `def test_render_toasts_returns_count(tmp_path)`
  - `test_build_default_bus_honours_budget` (function, line 175) `def test_build_default_bus_honours_budget(tmp_path)`
  - `test_reader_picks_up_new_events_after_offset` (function, line 187) `def test_reader_picks_up_new_events_after_offset(tmp_path)`
  - `_toast_event` (function, line 199) `def _toast_event(kind, severity, summary)`
  - `test_prominent_completion_renders_full_text` (function, line 211) `def test_prominent_completion_renders_full_text()`
  - `test_prominent_severity_renders_panel` (function, line 229) `def test_prominent_severity_renders_panel()`
  - `test_over_budget_events_collapse_into_digest` (function, line 242) `def test_over_budget_events_collapse_into_digest()`
  - `_cli_record` (function, line 255) `def _cli_record(event_type, payload, target)`
  - `test_summary_prefers_title_then_description` (function, line 269) `def test_summary_prefers_title_then_description()`
  - `test_summary_falls_back_to_capture_metadata` (function, line 279) `def test_summary_falls_back_to_capture_metadata()`
  - `test_summary_deduplicates_command_args_tail` (function, line 296) `def test_summary_deduplicates_command_args_tail()`
  - `test_activity_trigger_sources_expand_and_render` (function, line 306) `def test_activity_trigger_sources_expand_and_render()`
  - `test_collect_includes_activity_sources` (function, line 328) `def test_collect_includes_activity_sources()`
- Depends on: `cli/themes.py`, `cli/toast_bus.py`, `core/console.py`

## tests/test_toastr_unify.py
- Doc: BDD tests for the unified toastr presentation layer.
- Layer: testing
- Language: py
- Symbols:
  - `test_severity_table_covers_every_surface_level` (function, line 22) `def test_severity_table_covers_every_surface_level()`
  - `test_unknown_severity_falls_back_to_info` (function, line 30) `def test_unknown_severity_falls_back_to_info()`
  - `test_plain_text_message_wraps_and_adapts` (function, line 35) `def test_plain_text_message_wraps_and_adapts()`
  - `test_empty_message_falls_back_like_legacy` (function, line 45) `def test_empty_message_falls_back_like_legacy()`
  - `test_markup_is_escaped_for_plain_text` (function, line 51) `def test_markup_is_escaped_for_plain_text()`
  - `test_sentinel_panel_keeps_field_layout` (function, line 57) `def test_sentinel_panel_keeps_field_layout()`
  - `test_sentinel_severity_selects_border` (function, line 67) `def test_sentinel_severity_selects_border()`
  - `_SpyConsole` (class, line 73) `class _SpyConsole`
  - `test_shell_hint_bypass_prints_flat_line` (function, line 84) `def test_shell_hint_bypass_prints_flat_line()`
  - `test_shell_hint_bypass_keeps_empty_fallback` (function, line 91) `def test_shell_hint_bypass_keeps_empty_fallback()`
  - `__init__` (method, line 76) `def __init__(self)`
  - `print` (method, line 79) `def print(self, message, style)`
- Depends on: `cli/toast_bus.py`

## tests/test_toolchain_pins.py
- Doc: Contract: one ruff/mypy version across every tooling surface.
- Layer: testing
- Language: py
- Symbols:
  - `_dev_pin` (function, line 18) `def _dev_pin(package)`
  - `test_ci_yml_does_not_hardcode_ruff` (function, line 25) `def test_ci_yml_does_not_hardcode_ruff()`
  - `test_pre_commit_ruff_rev_matches_dev_pin` (function, line 32) `def test_pre_commit_ruff_rev_matches_dev_pin()`
  - `test_pre_commit_mypy_rev_matches_dev_pin` (function, line 43) `def test_pre_commit_mypy_rev_matches_dev_pin()`
  - `test_lint_workflow_installs_dev_requirements` (function, line 54) `def test_lint_workflow_installs_dev_requirements()`

## tests/test_triage_scheduler.py
- Doc: Difficulty-triage scheduler BDD contract.
- Layer: testing
- Language: py
- Symbols:
  - `test_estimate_difficulty_wide_surface_is_easier` (function, line 13) `def test_estimate_difficulty_wide_surface_is_easier()`
  - `test_estimate_difficulty_unknown_target_is_neutral` (function, line 20) `def test_estimate_difficulty_unknown_target_is_neutral()`
  - `test_estimate_difficulty_rich_target_drains_before_unknown` (function, line 26) `def test_estimate_difficulty_rich_target_drains_before_unknown()`
  - `test_estimate_difficulty_accepts_counts_or_collections` (function, line 33) `def test_estimate_difficulty_accepts_counts_or_collections()`
  - `test_order_is_easy_first` (function, line 40) `def test_order_is_easy_first()`
  - `test_order_breaks_ties_by_progress_then_arrival` (function, line 51) `def test_order_breaks_ties_by_progress_then_arrival()`
  - `test_deadline_salvages_partials_first` (function, line 62) `def test_deadline_salvages_partials_first()`
  - `test_deadline_ignores_partials_below_salvage_threshold` (function, line 72) `def test_deadline_ignores_partials_below_salvage_threshold()`
  - `test_stop_loss_triggers_on_attempts_without_progress` (function, line 83) `def test_stop_loss_triggers_on_attempts_without_progress()`
  - `test_route_splits_hard_and_easy` (function, line 91) `def test_route_splits_hard_and_easy()`
  - `test_pick_next_returns_none_when_empty` (function, line 98) `def test_pick_next_returns_none_when_empty()`
- Depends on: `modules/loop/triage_scheduler.py`

## tests/test_trigger_policy.py
- Doc: BDD contract tests for the declarative trigger policy.
- Layer: testing
- Language: py
- Symbols:
  - `test_validate_policy_rejects_bad_documents` (function, line 18) `def test_validate_policy_rejects_bad_documents()`
  - `test_seeds_coerce_and_skip_unknown_kinds` (function, line 26) `def test_seeds_coerce_and_skip_unknown_kinds()`
  - `test_yaml_seeds_read_from_orchestrator_document` (function, line 40) `def test_yaml_seeds_read_from_orchestrator_document()`
  - `test_seed_store_is_idempotent` (function, line 48) `def test_seed_store_is_idempotent(tmp_path, monkeypatch)`
  - `test_seed_store_keeps_runtime_triggers` (function, line 66) `def test_seed_store_keeps_runtime_triggers(tmp_path, monkeypatch)`
  - `test_orchestrator_yaml_declares_trigger_seeds` (function, line 82) `def test_orchestrator_yaml_declares_trigger_seeds()`
  - `test_seed_store_drops_unknown_kinds` (function, line 89) `def test_seed_store_drops_unknown_kinds(tmp_path, monkeypatch)`
- Depends on: `modules/__init__.py`, `modules/lazy_loop.py`, `modules/loop_triggers.py`

## tests/test_trusted_proxy.py
- Doc: TDD tests for the trusted proxy resolver contract.
- Layer: testing
- Language: py
- Symbols:
  - `TestNoProxy` (class, line 22) `class TestNoProxy`
  - `TestTrustedProxy` (class, line 43) `class TestTrustedProxy`
  - `TestIsOperator` (class, line 99) `class TestIsOperator`
  - `test_remote_addr_returned` (method, line 25) `def test_remote_addr_returned(self)`
  - `test_no_header_falls_back_to_remote` (method, line 38) `def test_no_header_falls_back_to_remote(self)`
  - `test_single_proxy_returns_leftmost` (method, line 46) `def test_single_proxy_returns_leftmost(self)`
  - `test_two_proxies_returns_leftmost` (method, line 59) `def test_two_proxies_returns_leftmost(self)`
  - `test_insufficient_chain_falls_back` (method, line 72) `def test_insufficient_chain_falls_back(self)`
  - `test_empty_header_falls_back` (method, line 85) `def test_empty_header_falls_back(self)`
  - `test_match` (method, line 102) `def test_match(self)`
  - `test_no_match` (method, line 109) `def test_no_match(self)`
- Depends on: `lazyc2/security/trusted_proxy.py`

## tests/test_ttpscope_bridge.py
- Doc: TTPScope bridge contract: validators, fallbacks, addon schema.
- Layer: testing
- Language: py
- Symbols:
  - `test_object_id_validation` (function, line 18) `def test_object_id_validation()`
  - `test_query_and_platform_validation` (function, line 27) `def test_query_and_platform_validation()`
  - `test_unknown_action_rejected` (function, line 40) `def test_unknown_action_rejected()`
  - `test_search_fallback_needs_no_binary` (function, line 48) `def test_search_fallback_needs_no_binary(monkeypatch)`
  - `test_show_fallback_technique` (function, line 56) `def test_show_fallback_technique(monkeypatch)`
  - `test_matrix_fallback_groups` (function, line 65) `def test_matrix_fallback_groups(monkeypatch)`
  - `test_notes_roundtrip_without_binary` (function, line 73) `def test_notes_roundtrip_without_binary(monkeypatch, tmp_path)`
  - `test_chain_needs_no_binary` (function, line 85) `def test_chain_needs_no_binary(monkeypatch)`
  - `test_addon_schema_agent_friendly` (function, line 95) `def test_addon_schema_agent_friendly()`
- Depends on: `modules/__init__.py`

## tests/test_tui_splash.py
- Doc: Tests for cli.splash — the animated first-run overlay.
- Layer: testing
- Language: py
- Symbols:
  - `_console` (function, line 19) `def _console()`
  - `SplashInstantEffectTests` (class, line 30) `class SplashInstantEffectTests(TestCase)`
  - `SplashTypewriterEffectTests` (class, line 67) `class SplashTypewriterEffectTests(TestCase)`
  - `SplashDispatchTests` (class, line 81) `class SplashDispatchTests(TestCase)`
  - `SplashEdgeCaseTests` (class, line 145) `class SplashEdgeCaseTests(TestCase)`
  - `test_instant_renders_every_line` (method, line 31) `def test_instant_renders_every_line(self)`
  - `test_instant_does_not_block` (method, line 44) `def test_instant_does_not_block(self)`
  - `test_instant_emits_ansi_for_known_tokens` (method, line 56) `def test_instant_emits_ansi_for_known_tokens(self)`
  - `test_typewriter_renders_all_lines_when_total_seconds_high` (method, line 68) `def test_typewriter_renders_all_lines_when_total_seconds_high(self)`
  - `test_render_splash_dispatches_instant_for_zero_seconds` (method, line 82) `def test_render_splash_dispatches_instant_for_zero_seconds(self)`
  - `test_render_splash_dispatches_instant_when_explicit` (method, line 92) `def test_render_splash_dispatches_instant_when_explicit(self)`
  - `test_render_splash_unknown_effect_falls_back_to_instant` (method, line 103) `def test_render_splash_unknown_effect_falls_back_to_instant(self)`
  - `test_render_splash_uses_payload_theme_when_provided` (method, line 114) `def test_render_splash_uses_payload_theme_when_provided(self)`
  - `test_render_splash_clear_after_emits_clear_escape` (method, line 124) `def test_render_splash_clear_after_emits_clear_escape(self)`
  - `test_render_splash_no_clear_when_disabled` (method, line 134) `def test_render_splash_no_clear_when_disabled(self)`
  - `test_empty_lines_is_noop` (method, line 146) `def test_empty_lines_is_noop(self)`
  - `test_lines_with_brackets_render_verbatim` (method, line 156) `def test_lines_with_brackets_render_verbatim(self)`
- Depends on: `cli/splash.py`, `core/console.py`

## tests/test_tui_style.py
- Doc: Tests for the cli/style semantic token layer.
- Layer: testing
- Language: py
- Symbols:
  - `StyleTokenTests` (class, line 14) `class StyleTokenTests(TestCase)`
  - `test_known_token_returns_theme_attribute` (method, line 15) `def test_known_token_returns_theme_attribute(self)`
  - `test_unknown_token_falls_back_to_white` (method, line 21) `def test_unknown_token_falls_back_to_white(self)`
  - `test_active_tokens_covers_every_key` (method, line 25) `def test_active_tokens_covers_every_key(self)`
  - `test_active_tokens_honours_payload` (method, line 32) `def test_active_tokens_honours_payload(self)`
  - `test_paint_returns_rich_text_with_style` (method, line 39) `def test_paint_returns_rich_text_with_style(self)`
  - `test_render_prompt_emits_segments_separated_by_bar` (method, line 44) `def test_render_prompt_emits_segments_separated_by_bar(self)`
  - `test_render_prompt_empty_is_noop` (method, line 59) `def test_render_prompt_empty_is_noop(self)`
- Depends on: `cli/__init__.py`, `cli/themes.py`, `core/console.py`

## tests/test_tui_theme_command.py
- Doc: Tests for the cli.tui_theme command logic.
- Layer: testing
- Language: py
- Symbols:
  - `RecordingSave` (class, line 11) `class RecordingSave`
  - `_payload` (function, line 21) `def _payload()`
  - `TuiThemeListingTests` (class, line 28) `class TuiThemeListingTests(TestCase)`
  - `TuiThemeSwitchTests` (class, line 46) `class TuiThemeSwitchTests(TestCase)`
  - `TuiThemeCycleTests` (class, line 78) `class TuiThemeCycleTests(TestCase)`
  - `TuiThemeRegistrationConsistencyTests` (class, line 105) `class TuiThemeRegistrationConsistencyTests(TestCase)`
  - `__init__` (method, line 14) `def __init__(self)`
  - `__call__` (method, line 17) `def __call__(self, payload)`
  - `test_empty_args_lists_every_registered_theme` (method, line 29) `def test_empty_args_lists_every_registered_theme(self)`
  - `test_listing_marks_current_theme` (method, line 38) `def test_listing_marks_current_theme(self)`
  - `test_known_name_switches_and_persists` (method, line 47) `def test_known_name_switches_and_persists(self)`
  - `test_unknown_name_does_not_mutate` (method, line 55) `def test_unknown_name_does_not_mutate(self)`
  - `test_case_insensitive_lookup` (method, line 63) `def test_case_insensitive_lookup(self)`
  - `test_reset_returns_to_default` (method, line 70) `def test_reset_returns_to_default(self)`
  - `test_cycle_advances_in_theme_order` (method, line 79) `def test_cycle_advances_in_theme_order(self)`
  - `test_cycle_wraps_around` (method, line 87) `def test_cycle_wraps_around(self)`
  - `test_prev_walks_backwards_and_wraps` (method, line 94) `def test_prev_walks_backwards_and_wraps(self)`
  - `test_theme_order_covers_every_registered_theme` (method, line 106) `def test_theme_order_covers_every_registered_theme(self)`
  - `test_theme_order_has_no_duplicates` (method, line 109) `def test_theme_order_has_no_duplicates(self)`
- Depends on: `cli/__init__.py`, `cli/themes.py`

## tests/test_tui_themes.py
- Doc: Tests for the four new themes added on top of the original four.
- Layer: testing
- Language: py
- Symbols:
  - `NewThemeRegistrationTests` (class, line 39) `class NewThemeRegistrationTests(TestCase)`
  - `NewThemeRenderTests` (class, line 86) `class NewThemeRenderTests(TestCase)`
  - `ThemeOrderTests` (class, line 130) `class ThemeOrderTests(TestCase)`
  - `test_every_new_theme_is_registered` (method, line 40) `def test_every_new_theme_is_registered(self)`
  - `test_original_themes_remain_registered` (method, line 45) `def test_original_themes_remain_registered(self)`
  - `test_get_theme_resolves_every_new_name` (method, line 50) `def test_get_theme_resolves_every_new_name(self)`
  - `test_get_theme_uses_case_insensitive_lookup` (method, line 55) `def test_get_theme_uses_case_insensitive_lookup(self)`
  - `test_unknown_name_falls_back_to_default` (method, line 59) `def test_unknown_name_falls_back_to_default(self)`
  - `test_theme_from_payload_picks_each_new_theme` (method, line 64) `def test_theme_from_payload_picks_each_new_theme(self)`
  - `test_new_themes_have_unique_color_palettes` (method, line 72) `def test_new_themes_have_unique_color_palettes(self)`
  - `test_new_themes_have_non_empty_token_values` (method, line 76) `def test_new_themes_have_non_empty_token_values(self)`
  - `test_every_token_renders_with_ansi_escapes` (method, line 95) `def test_every_token_renders_with_ansi_escapes(self)`
  - `test_every_token_renders_with_ansi_escapes_in_256color` (method, line 112) `def test_every_token_renders_with_ansi_escapes_in_256color(self)`
  - `test_order_covers_every_registered_theme_exactly_once` (method, line 131) `def test_order_covers_every_registered_theme_exactly_once(self)`
  - `test_order_is_reexported_by_tui_theme_command` (method, line 135) `def test_order_is_reexported_by_tui_theme_command(self)`
- Depends on: `cli/__init__.py`, `cli/themes.py`, `core/console.py`

## tests/test_unified_bridge_delegate.py
- Doc: Contract tests for UnifiedBridge.delegate agent polling.
- Layer: testing
- Language: py
- Symbols:
  - `unified_bridge` (function, line 16) `def unified_bridge(monkeypatch)`
  - `_patch_bridge_api` (function, line 25) `def _patch_bridge_api(monkeypatch, statuses, result)`
  - `test_delegate_polls_until_completion` (function, line 40) `def test_delegate_polls_until_completion(monkeypatch, unified_bridge)`
  - `test_delegate_times_out_when_agent_never_finishes` (function, line 55) `def test_delegate_times_out_when_agent_never_finishes(monkeypatch, unified_bridge)`
  - `test_delegate_reports_agent_failure` (function, line 66) `def test_delegate_reports_agent_failure(monkeypatch, unified_bridge)`
  - `test_delegate_surfaces_missing_agent` (function, line 77) `def test_delegate_surfaces_missing_agent(monkeypatch, unified_bridge)`
  - `test_delegate_wraps_start_errors` (function, line 87) `def test_delegate_wraps_start_errors(monkeypatch, unified_bridge)`
  - `fake_start` (function, line 30) `def fake_start(goal, backend, runner, max_iterations)`
  - `boom` (function, line 90) `def boom()`
- Depends on: `modules/__init__.py`

## tests/test_unified_dashboard.py
- Doc: Tests for modules/unified_dashboard.py.
- Layer: testing
- Language: py
- Symbols:
  - `TestUnifiedDashboardInit` (class, line 10) `class TestUnifiedDashboardInit`
  - `TestWorldModelCollection` (class, line 21) `class TestWorldModelCollection`
  - `TestDaemonStatus` (class, line 36) `class TestDaemonStatus`
  - `TestUnifiedSnapshot` (class, line 51) `class TestUnifiedSnapshot`
  - `TestRenderUnified` (class, line 74) `class TestRenderUnified`
  - `TestExportJson` (class, line 95) `class TestExportJson`
  - `test_default_init` (method, line 11) `def test_default_init(self, tmp_path)`
  - `test_get_unified_dashboard_singleton` (method, line 15) `def test_get_unified_dashboard_singleton(self, tmp_path)`
  - `test_collect_world_model_exists` (method, line 22) `def test_collect_world_model_exists(self, tmp_path)`
  - `test_collect_world_model_missing` (method, line 30) `def test_collect_world_model_missing(self, tmp_path)`
  - `test_collect_daemon_status_exists` (method, line 37) `def test_collect_daemon_status_exists(self, tmp_path)`
  - `test_collect_daemon_status_missing` (method, line 45) `def test_collect_daemon_status_missing(self, tmp_path)`
  - `test_snapshot_keys` (method, line 52) `def test_snapshot_keys(self, tmp_path)`
  - `test_snapshot_timestamp` (method, line 67) `def test_snapshot_timestamp(self, tmp_path)`
  - `test_render_contains_header` (method, line 75) `def test_render_contains_header(self, tmp_path)`
  - `test_render_contains_sections` (method, line 80) `def test_render_contains_sections(self, tmp_path)`
  - `test_render_contains_timestamp` (method, line 89) `def test_render_contains_timestamp(self, tmp_path)`
  - `test_export_json` (method, line 96) `def test_export_json(self, tmp_path)`
- Depends on: `modules/unified_dashboard.py`

## tests/test_utils_import_silent.py
- Doc: utils as a library: importing it must never parse the importer's argv.
- Layer: testing
- Language: py
- Symbols:
  - `test_import_with_foreign_argv_is_silent` (function, line 12) `def test_import_with_foreign_argv_is_silent()`
  - `test_lazy_import_chains_stay_silent` (function, line 34) `def test_lazy_import_chains_stay_silent()`

## tests/test_verb_catalog.py
- Doc: BDD contract tests for the operator verb catalog.
- Layer: testing
- Language: py
- Symbols:
  - `sandbox` (function, line 19) `def sandbox(tmp_path)`
  - `test_sync_generates_catalog_with_builtins_on_and_new_off` (function, line 32) `def test_sync_generates_catalog_with_builtins_on_and_new_off(sandbox)`
  - `test_sync_preserves_operator_choices` (function, line 41) `def test_sync_preserves_operator_choices(sandbox)`
  - `test_sync_prunes_stale_commands` (function, line 51) `def test_sync_prunes_stale_commands(sandbox)`
  - `test_load_returns_empty_on_missing_invalid_or_oversize` (function, line 64) `def test_load_returns_empty_on_missing_invalid_or_oversize(sandbox, tmp_path)`
  - `test_set_enabled_unknown_command_raises` (function, line 73) `def test_set_enabled_unknown_command_raises(sandbox)`
  - `test_set_enabled_persists_atomically` (function, line 79) `def test_set_enabled_persists_atomically(sandbox)`
  - `test_validate_catalog_rejects_bad_documents` (function, line 88) `def test_validate_catalog_rejects_bad_documents(sandbox)`
  - `test_effective_verbs_include_catalog_entries` (function, line 97) `def test_effective_verbs_include_catalog_entries(sandbox, monkeypatch)`
  - `test_loop_refuses_disabled_cli_verb_and_allows_enabled` (function, line 111) `def test_loop_refuses_disabled_cli_verb_and_allows_enabled(sandbox, monkeypatch)`
  - `test_stats_reports_on_off_counts` (function, line 133) `def test_stats_reports_on_off_counts(sandbox)`
  - `test_search_filters_catalog` (function, line 141) `def test_search_filters_catalog(sandbox)`
  - `_addon_sandbox` (function, line 150) `def _addon_sandbox(tmp_path, enabled)`
  - `test_sync_indexes_enabled_lazyaddons_disabled_by_default` (function, line 169) `def test_sync_indexes_enabled_lazyaddons_disabled_by_default(tmp_path)`
  - `test_sync_prunes_renamed_or_disabled_addons` (function, line 187) `def test_sync_prunes_renamed_or_disabled_addons(tmp_path)`
  - `test_operator_can_turn_addon_verb_on` (function, line 202) `def test_operator_can_turn_addon_verb_on(tmp_path)`
  - `test_steps_for_addon_verb_runs_lazy_addon` (function, line 215) `def test_steps_for_addon_verb_runs_lazy_addon(tmp_path, monkeypatch)`
  - `test_entries_default_phases_is_single_phase` (function, line 237) `def test_entries_default_phases_is_single_phase(sandbox)`
  - `test_entries_multi_phase_list_is_honoured` (function, line 249) `def test_entries_multi_phase_list_is_honoured(sandbox)`
  - `test_validate_catalog_rejects_non_string_phases` (function, line 262) `def test_validate_catalog_rejects_non_string_phases(sandbox)`
- Depends on: `modules/__init__.py`

## tests/test_verb_manifest.py
- Doc: BDD tests for the typed verb manifest store.
- Layer: testing
- Language: py
- Symbols:
  - `manifest_path` (function, line 14) `def manifest_path(tmp_path)`
  - `TestSchema` (class, line 50) `class TestSchema`
  - `TestPlanCheck` (class, line 81) `class TestPlanCheck`
  - `TestNoiseAndCost` (class, line 118) `class TestNoiseAndCost`
  - `test_valid_manifest_parses` (method, line 53) `def test_valid_manifest_parses(self, manifest_path)`
  - `test_unknown_fact_id_dropped` (method, line 65) `def test_unknown_fact_id_dropped(self, manifest_path)`
  - `test_parse_manifest_rejects_junk` (method, line 73) `def test_parse_manifest_rejects_junk(self)`
  - `test_unmet_precondition_reported` (method, line 84) `def test_unmet_precondition_reported(self, manifest_path)`
  - `test_effect_paid_forward` (method, line 91) `def test_effect_paid_forward(self, manifest_path)`
  - `test_world_model_facts_default` (method, line 104) `def test_world_model_facts_default(self)`
  - `test_fallback_when_store_empty` (method, line 112) `def test_fallback_when_store_empty(self, tmp_path)`
  - `test_noise_clamped` (method, line 121) `def test_noise_clamped(self)`
  - `test_cost_tolerates_junk` (method, line 129) `def test_cost_tolerates_junk(self)`
- Depends on: `modules/chain_registry.py`, `modules/verb_manifest.py`

## tests/test_viral_adoption.py
- Doc: Viral adoption assets: GIFs, smoke script, drift CI, launch kit.
- Layer: testing
- Language: py
- Symbols:
  - `test_demo_gifs_exist_and_nonempty` (function, line 8) `def test_demo_gifs_exist_and_nonempty()`
  - `test_demo_gif_commands_exist_in_source` (function, line 23) `def test_demo_gif_commands_exist_in_source()`
  - `test_readme_links_viral_assets` (function, line 75) `def test_readme_links_viral_assets()`
  - `test_smoke_script_covers_onboarding` (function, line 83) `def test_smoke_script_covers_onboarding()`
  - `test_docs_drift_workflow_exists` (function, line 89) `def test_docs_drift_workflow_exists()`
  - `test_marketplace_template_exists` (function, line 95) `def test_marketplace_template_exists()`
  - `test_launch_kit_exists` (function, line 101) `def test_launch_kit_exists()`


Next: [KB_tests_p27.md](KB_tests_p27.md)
