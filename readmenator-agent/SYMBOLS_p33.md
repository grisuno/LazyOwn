# Symbols (page 33 of 35)
Previous: [SYMBOLS_p32.md](SYMBOLS_p32.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_advisor_swallows_rag_query_errors` | method | `tests/test_reactive_engine_semantic.py:163` | `def test_advisor_swallows_rag_query_errors()` |
| `test_emits_priority_five_suggestion` | method | `tests/test_reactive_engine_semantic.py:70` | `def test_emits_priority_five_suggestion()` |
| `test_engine_uses_semantic_advisor_when_supplied` | method | `tests/test_reactive_engine_semantic.py:139` | `def test_engine_uses_semantic_advisor_when_supplied()` |
| `test_returns_empty_when_disabled_via_payload` | method | `tests/test_reactive_engine_semantic.py:54` | `def test_returns_empty_when_disabled_via_payload()` |
| `test_returns_empty_when_rag_unavailable` | method | `tests/test_reactive_engine_semantic.py:46` | `def test_returns_empty_when_rag_unavailable()` |
| `test_skips_hits_without_command_prefix` | method | `tests/test_reactive_engine_semantic.py:127` | `def test_skips_hits_without_command_prefix()` |
| `test_skips_low_score_hits` | method | `tests/test_reactive_engine_semantic.py:90` | `def test_skips_low_score_hits()` |
| `test_skips_same_command_and_dedupes` | method | `tests/test_reactive_engine_semantic.py:102` | `def test_skips_same_command_and_dedupes()` |
| `TestExtractLabels` | class | `tests/test_reactive_hints.py:88` | `class TestExtractLabels` |
| `TestFirstToken` | class | `tests/test_reactive_hints.py:57` | `class TestFirstToken` |
| `TestRenderInlineHints` | class | `tests/test_reactive_hints.py:111` | `class TestRenderInlineHints` |
| `TestTruncate` | class | `tests/test_reactive_hints.py:71` | `class TestTruncate` |
| `_FakeAdvisor` | class | `tests/test_reactive_hints.py:29` | `class _FakeAdvisor` |
| `__init__` | method | `tests/test_reactive_hints.py:32` | `def __init__(self, suggestions)` |
| `advisor_with_three_hints` | method | `tests/test_reactive_hints.py:42` | `def advisor_with_three_hints()` |
| `empty_advisor` | method | `tests/test_reactive_hints.py:53` | `def empty_advisor()` |
| `suggest_next` | method | `tests/test_reactive_hints.py:36` | `def suggest_next(self, recent_commands, limit)` |
| `test_advisor_called_with_correct_command` | method | `tests/test_reactive_hints.py:137` | `def test_advisor_called_with_correct_command(self, advisor_with_three_hints)` |
| `test_all_skip_commands_are_skipped` | method | `tests/test_reactive_hints.py:149` | `def test_all_skip_commands_are_skipped(self, advisor_with_three_hints)` |
| `test_disabled_flag_skips_render` | method | `tests/test_reactive_hints.py:112` | `def test_disabled_flag_skips_render(self, advisor_with_three_hints)` |
| `test_empty_command_skips_render` | method | `tests/test_reactive_hints.py:122` | `def test_empty_command_skips_render(self, advisor_with_three_hints)` |
| `test_empty_string` | method | `tests/test_reactive_hints.py:64` | `def test_empty_string(self)` |
| `test_empty_suggestions_skips_render` | method | `tests/test_reactive_hints.py:127` | `def test_empty_suggestions_skips_render(self, empty_advisor)` |
| `test_exact_length_unchanged` | method | `tests/test_reactive_hints.py:75` | `def test_exact_length_unchanged(self)` |
| `test_exception_in_advisor_does_not_propagate` | method | `tests/test_reactive_hints.py:142` | `def test_exception_in_advisor_does_not_propagate(self)` |
| `test_extracts_first_word` | method | `tests/test_reactive_hints.py:58` | `def test_extracts_first_word(self)` |
| `test_falls_back_to_id_when_no_label` | method | `tests/test_reactive_hints.py:93` | `def test_falls_back_to_id_when_no_label(self)` |
| `test_limit_is_passed_to_advisor` | method | `tests/test_reactive_hints.py:155` | `def test_limit_is_passed_to_advisor(self, advisor_with_three_hints)` |
| `test_long_string_truncated` | method | `tests/test_reactive_hints.py:78` | `def test_long_string_truncated(self)` |
| `test_normal_command_renders_hint` | method | `tests/test_reactive_hints.py:132` | `def test_normal_command_renders_hint(self, advisor_with_three_hints)` |
| `test_picks_label_over_id` | method | `tests/test_reactive_hints.py:89` | `def test_picks_label_over_id(self)` |
| `test_respects_limit` | method | `tests/test_reactive_hints.py:101` | `def test_respects_limit(self)` |
| `test_short_string_unchanged` | method | `tests/test_reactive_hints.py:72` | `def test_short_string_unchanged(self)` |
| `test_single_word` | method | `tests/test_reactive_hints.py:61` | `def test_single_word(self)` |
| `test_skip_command_skips_render` | method | `tests/test_reactive_hints.py:117` | `def test_skip_command_skips_render(self, advisor_with_three_hints)` |
| `test_skips_empty_entries` | method | `tests/test_reactive_hints.py:97` | `def test_skips_empty_entries(self)` |
| `test_truncates_long_labels` | method | `tests/test_reactive_hints.py:105` | `def test_truncates_long_labels(self)` |
| `test_truncation_preserves_start` | method | `tests/test_reactive_hints.py:83` | `def test_truncation_preserves_start(self)` |
| `test_whitespace_only` | method | `tests/test_reactive_hints.py:67` | `def test_whitespace_only(self)` |
| `TestKillChainNextExpanded` | class | `tests/test_reactive_hints_expanded.py:13` | `class TestKillChainNextExpanded` |
| `TestPhasePriorityExpanded` | class | `tests/test_reactive_hints_expanded.py:62` | `class TestPhasePriorityExpanded` |
| `TestProtipTriggers` | class | `tests/test_reactive_hints_expanded.py:142` | `class TestProtipTriggers` |
| `TestProtipsExpanded` | class | `tests/test_reactive_hints_expanded.py:93` | `class TestProtipsExpanded` |
| `test_after_trigger` | method | `tests/test_reactive_hints_expanded.py:154` | `def test_after_trigger(self)` |
| `test_auto_pwn_has_followups` | method | `tests/test_reactive_hints_expanded.py:20` | `def test_auto_pwn_has_followups(self)` |
| `test_auto_pwn_in_lazynmap_followups` | method | `tests/test_reactive_hints_expanded.py:14` | `def test_auto_pwn_in_lazynmap_followups(self)` |
| `test_campaign_has_followups` | method | `tests/test_reactive_hints_expanded.py:51` | `def test_campaign_has_followups(self)` |
| `test_chain_has_followups` | method | `tests/test_reactive_hints_expanded.py:26` | `def test_chain_has_followups(self)` |
| `test_collab_has_followups` | method | `tests/test_reactive_hints_expanded.py:56` | `def test_collab_has_followups(self)` |
| `test_enum_includes_nuclei` | method | `tests/test_reactive_hints_expanded.py:70` | `def test_enum_includes_nuclei(self)` |
| `test_exploit_includes_automation` | method | `tests/test_reactive_hints_expanded.py:63` | `def test_exploit_includes_automation(self)` |
| `test_hunt_has_followups` | method | `tests/test_reactive_hints_expanded.py:31` | `def test_hunt_has_followups(self)` |
| `test_lateral_includes_collab` | method | `tests/test_reactive_hints_expanded.py:81` | `def test_lateral_includes_collab(self)` |
| `test_lazynmap_suggests_nuclei` | method | `tests/test_reactive_hints_expanded.py:46` | `def test_lazynmap_suggests_nuclei(self)` |
| `test_nuclei_has_followups` | method | `tests/test_reactive_hints_expanded.py:36` | `def test_nuclei_has_followups(self)` |
| `test_os_linux_detection` | method | `tests/test_reactive_hints_expanded.py:143` | `def test_os_linux_detection(self)` |
| `test_os_windows_detection` | method | `tests/test_reactive_hints_expanded.py:149` | `def test_os_windows_detection(self)` |
| `test_persist_phase_exists` | method | `tests/test_reactive_hints_expanded.py:86` | `def test_persist_phase_exists(self)` |
| `test_phase_in_trigger` | method | `tests/test_reactive_hints_expanded.py:159` | `def test_phase_in_trigger(self)` |
| `test_postexp_includes_security` | method | `tests/test_reactive_hints_expanded.py:75` | `def test_postexp_includes_security(self)` |
| `test_session_tips_expanded` | method | `tests/test_reactive_hints_expanded.py:131` | `def test_session_tips_expanded(self)` |
| `test_tips_include_automation` | method | `tests/test_reactive_hints_expanded.py:94` | `def test_tips_include_automation(self)` |
| `test_tips_include_collab` | method | `tests/test_reactive_hints_expanded.py:114` | `def test_tips_include_collab(self)` |
| `test_tips_include_discovery` | method | `tests/test_reactive_hints_expanded.py:124` | `def test_tips_include_discovery(self)` |
| `test_tips_include_security` | method | `tests/test_reactive_hints_expanded.py:105` | `def test_tips_include_security(self)` |
| `test_yara_scan_has_followups` | method | `tests/test_reactive_hints_expanded.py:41` | `def test_yara_scan_has_followups(self)` |
| `TestDataOfInterestMatcher` | class | `tests/test_reactive_lateral_data.py:60` | `class TestDataOfInterestMatcher` |
| `TestLateralOpportunityMatcher` | class | `tests/test_reactive_lateral_data.py:11` | `class TestLateralOpportunityMatcher` |
| `TestReactiveEngineIntegration` | class | `tests/test_reactive_lateral_data.py:118` | `class TestReactiveEngineIntegration` |
| `_make_engine` | method | `tests/test_reactive_lateral_data.py:119` | `def _make_engine(self, matchers)` |
| `test_confidence` | method | `tests/test_reactive_lateral_data.py:53` | `def test_confidence(self)` |
| `test_confidence_levels` | method | `tests/test_reactive_lateral_data.py:106` | `def test_confidence_levels(self)` |
| `test_data_signals_produce_decisions` | method | `tests/test_reactive_lateral_data.py:147` | `def test_data_signals_produce_decisions(self)` |
| `test_decisions_sorted_by_priority` | method | `tests/test_reactive_lateral_data.py:165` | `def test_decisions_sorted_by_priority(self)` |
| `test_domain_admin` | method | `tests/test_reactive_lateral_data.py:43` | `def test_domain_admin(self)` |
| `test_file_pattern_config` | method | `tests/test_reactive_lateral_data.py:96` | `def test_file_pattern_config(self)` |
| `test_file_pattern_env` | method | `tests/test_reactive_lateral_data.py:91` | `def test_file_pattern_env(self)` |
| `test_kerberos_ticket` | method | `tests/test_reactive_lateral_data.py:12` | `def test_kerberos_ticket(self)` |
| `test_lateral_signals_produce_decisions` | method | `tests/test_reactive_lateral_data.py:130` | `def test_lateral_signals_produce_decisions(self)` |
| `test_no_match` | method | `tests/test_reactive_lateral_data.py:48` | `def test_no_match(self)` |
| `test_no_match` | method | `tests/test_reactive_lateral_data.py:101` | `def test_no_match(self)` |
| `test_pii_credit_card` | method | `tests/test_reactive_lateral_data.py:71` | `def test_pii_credit_card(self)` |
| `test_pii_email` | method | `tests/test_reactive_lateral_data.py:61` | `def test_pii_email(self)` |
| `test_pii_ssn` | method | `tests/test_reactive_lateral_data.py:66` | `def test_pii_ssn(self)` |
| `test_rdp_session` | method | `tests/test_reactive_lateral_data.py:18` | `def test_rdp_session(self)` |
| `test_secret_api_key` | method | `tests/test_reactive_lateral_data.py:76` | `def test_secret_api_key(self)` |
| `test_secret_aws_key` | method | `tests/test_reactive_lateral_data.py:81` | `def test_secret_aws_key(self)` |
| `test_secret_private_key` | method | `tests/test_reactive_lateral_data.py:86` | `def test_secret_private_key(self)` |
| `test_smb_admin_share` | method | `tests/test_reactive_lateral_data.py:23` | `def test_smb_admin_share(self)` |
| `test_ssh_key` | method | `tests/test_reactive_lateral_data.py:33` | `def test_ssh_key(self)` |
| `test_winrm_access` | method | `tests/test_reactive_lateral_data.py:28` | `def test_winrm_access(self)` |
| `test_wmi_access` | method | `tests/test_reactive_lateral_data.py:38` | `def test_wmi_access(self)` |
| `_write_events` | function | `tests/test_reasoning_stream.py:28` | `def _write_events(path, events)` |
| `test_event_to_entry_extracts_reward` | function | `tests/test_reasoning_stream.py:85` | `def test_event_to_entry_extracts_reward()` |
| `test_event_to_entry_handles_non_dict_payload` | function | `tests/test_reasoning_stream.py:111` | `def test_event_to_entry_handles_non_dict_payload()` |
| `test_event_to_entry_metrics_skip_renders_success_rate` | function | `tests/test_reasoning_stream.py:95` | `def test_event_to_entry_metrics_skip_renders_success_rate()` |
| `test_event_to_entry_step_done_failure_flips_icon_and_style` | function | `tests/test_reasoning_stream.py:75` | `def test_event_to_entry_step_done_failure_flips_icon_and_style()` |
| `test_event_to_entry_step_start_uses_reason_and_source` | function | `tests/test_reasoning_stream.py:53` | `def test_event_to_entry_step_start_uses_reason_and_source()` |
| `test_event_to_entry_unknown_type_falls_back` | function | `tests/test_reasoning_stream.py:105` | `def test_event_to_entry_unknown_type_falls_back()` |
| `test_format_size_threshold` | function | `tests/test_reasoning_stream.py:117` | `def test_format_size_threshold()` |
| `test_latest_reasoning_end_to_end` | function | `tests/test_reasoning_stream.py:127` | `def test_latest_reasoning_end_to_end(tmp_path)` |
| `test_read_raw_events_honours_limit_tail` | function | `tests/test_reasoning_stream.py:46` | `def test_read_raw_events_honours_limit_tail(tmp_path)` |
| `test_read_raw_events_missing_file_returns_empty` | function | `tests/test_reasoning_stream.py:32` | `def test_read_raw_events_missing_file_returns_empty(tmp_path)` |
| `test_read_raw_events_skips_malformed_lines` | function | `tests/test_reasoning_stream.py:36` | `def test_read_raw_events_skips_malformed_lines(tmp_path)` |
| `test_truncate_adds_ellipsis` | function | `tests/test_reasoning_stream.py:122` | `def test_truncate_adds_ellipsis()` |
| `TestAdapters` | class | `tests/test_recommendation.py:158` | `class TestAdapters` |
| `TestContextAndFactory` | class | `tests/test_recommendation.py:216` | `class TestContextAndFactory` |
| `TestFusionCore` | class | `tests/test_recommendation.py:70` | `class TestFusionCore` |
| `_Advisor` | class | `tests/test_recommendation.py:160` | `class _Advisor` |
| `_BoomSignal` | class | `tests/test_recommendation.py:55` | `class _BoomSignal` |
| `_Item` | class | `tests/test_recommendation.py:178` | `class _Item` |
| `_Plan` | class | `tests/test_recommendation.py:185` | `class _Plan` |
| `_Policy` | class | `tests/test_recommendation.py:168` | `class _Policy` |
| `_StubSignal` | class | `tests/test_recommendation.py:46` | `class _StubSignal` |
| `__init__` | method | `tests/test_recommendation.py:47` | `def __init__(self, name, proposals)` |
| `__init__` | method | `tests/test_recommendation.py:179` | `def __init__(self, kind, name, reason)` |
| `_builder` | method | `tests/test_recommendation.py:188` | `def _builder(target, engine, payload)` |
| `_ctx` | function | `tests/test_recommendation.py:36` | `def _ctx(limit, recent, phase)` |
| `_engine` | method | `tests/test_recommendation.py:62` | `def _engine(signals, resolver, weights)` |
| `get_recommendations` | method | `tests/test_recommendation.py:169` | `def get_recommendations(self, target)` |
| `propose` | method | `tests/test_recommendation.py:51` | `def propose(self, ctx)` |
| `propose` | method | `tests/test_recommendation.py:58` | `def propose(self, ctx)` |
| `suggest_next` | method | `tests/test_recommendation.py:161` | `def suggest_next(self, recent_commands, limit)` |
| `test_build_context_resolves_target_and_phase` | method | `tests/test_recommendation.py:229` | `def test_build_context_resolves_target_and_phase(self, tmp_path)` |
| `test_build_default_engine_always_returns_engine` | method | `tests/test_recommendation.py:234` | `def test_build_default_engine_always_returns_engine(self, tmp_path)` |
| `test_category_prior_boosts_matching_action` | method | `tests/test_recommendation.py:98` | `def test_category_prior_boosts_matching_action(self)` |
| `test_covered_category_not_duplicated_as_standalone` | method | `tests/test_recommendation.py:123` | `def test_covered_category_not_duplicated_as_standalone(self)` |
| `test_cross_signal_merge_sums_and_records_provenance` | method | `tests/test_recommendation.py:85` | `def test_cross_signal_merge_sums_and_records_provenance(self)` |
| `test_deterministic_ordering_on_score_tie` | method | `tests/test_recommendation.py:131` | `def test_deterministic_ordering_on_score_tie(self)` |
| `test_failing_signal_is_isolated` | method | `tests/test_recommendation.py:147` | `def test_failing_signal_is_isolated(self)` |
| `test_graph_signal_extracts_label_and_score` | method | `tests/test_recommendation.py:159` | `def test_graph_signal_extracts_label_and_score(self)` |
| `test_killchain_signal_filters_already_run` | method | `tests/test_recommendation.py:206` | `def test_killchain_signal_filters_already_run(self)` |
| `test_killchain_signal_uses_adjacency_then_phase` | method | `tests/test_recommendation.py:196` | `def test_killchain_signal_uses_adjacency_then_phase(self)` |
| `test_limit_is_honoured` | method | `tests/test_recommendation.py:139` | `def test_limit_is_honoured(self)` |
| `test_policy_signal_emits_categories` | method | `tests/test_recommendation.py:167` | `def test_policy_signal_emits_categories(self)` |
| `test_read_recent_commands_missing_file` | method | `tests/test_recommendation.py:226` | `def test_read_recent_commands_missing_file(self, tmp_path)` |
| `test_read_recent_commands_orders_and_windows` | method | `tests/test_recommendation.py:217` | `def test_read_recent_commands_orders_and_windows(self, tmp_path)` |
| `test_recon_signal_maps_items_with_descending_weight` | method | `tests/test_recommendation.py:177` | `def test_recon_signal_maps_items_with_descending_weight(self)` |
| `test_single_signal_normalises_to_peak` | method | `tests/test_recommendation.py:71` | `def test_single_signal_normalises_to_peak(self)` |
| `test_uncovered_category_surfaces_as_recommendation` | method | `tests/test_recommendation.py:115` | `def test_uncovered_category_surfaces_as_recommendation(self)` |
| `test_zero_weight_signal_contributes_nothing` | method | `tests/test_recommendation.py:152` | `def test_zero_weight_signal_contributes_nothing(self)` |
| `BuildReconPlanContractSpec` | class | `tests/test_recon_plan.py:149` | `class BuildReconPlanContractSpec(TestCase)` |
| `RenderMarkdownSpec` | class | `tests/test_recon_plan.py:289` | `class RenderMarkdownSpec(TestCase)` |
| `RenderRichSpec` | class | `tests/test_recon_plan.py:379` | `class RenderRichSpec(TestCase)` |
| `WritePlanSpec` | class | `tests/test_recon_plan.py:338` | `class WritePlanSpec(TestCase)` |
| `_Recorder` | class | `tests/test_recon_plan.py:383` | `class _Recorder` |
| `_build` | method | `tests/test_recon_plan.py:179` | `def _build(self, current_os, payload)` |
| `_plan` | method | `tests/test_recon_plan.py:341` | `def _plan(self, target)` |
| `_plan_with_items` | method | `tests/test_recon_plan.py:292` | `def _plan_with_items(self)` |
| `_seed_addon` | function | `tests/test_recon_plan.py:68` | `def _seed_addon(addons_dir, name, os_value, triggers)` |
| `_seed_command_index` | function | `tests/test_recon_plan.py:110` | `def _seed_command_index(path)` |
| `_seed_engine` | function | `tests/test_recon_plan.py:130` | `def _seed_engine(sessions, addons, tools, nmap_xml, history_rows, current_os)` |
| `_seed_tool` | function | `tests/test_recon_plan.py:90` | `def _seed_tool(tools_dir, name, triggers, command, os_value)` |
| `print` | method | `tests/test_recon_plan.py:386` | `def print(self, line)` |
| `setUp` | method | `tests/test_recon_plan.py:152` | `def setUp(self)` |
| `tearDown` | method | `tests/test_recon_plan.py:176` | `def tearDown(self)` |
| `test_empty_scan_returns_empty_plan` | method | `tests/test_recon_plan.py:273` | `def test_empty_scan_returns_empty_plan(self)` |
| `test_markdown_handles_empty_plan` | method | `tests/test_recon_plan.py:325` | `def test_markdown_handles_empty_plan(self)` |
| `test_markdown_renders_command_preview_block` | method | `tests/test_recon_plan.py:320` | `def test_markdown_renders_command_preview_block(self)` |
| `test_markdown_renders_services_table` | method | `tests/test_recon_plan.py:315` | `def test_markdown_renders_services_table(self)` |
| `test_markdown_starts_with_target_header` | method | `tests/test_recon_plan.py:311` | `def test_markdown_starts_with_target_header(self)` |
| `test_plan_excludes_already_executed_addons` | method | `tests/test_recon_plan.py:216` | `def test_plan_excludes_already_executed_addons(self)` |
| `test_plan_filters_os_incompatible_addons_on_linux` | method | `tests/test_recon_plan.py:199` | `def test_plan_filters_os_incompatible_addons_on_linux(self)` |
| `test_plan_includes_addons_matching_open_service` | method | `tests/test_recon_plan.py:193` | `def test_plan_includes_addons_matching_open_service(self)` |
| `test_plan_includes_phase_priority_command_suggestions` | method | `tests/test_recon_plan.py:237` | `def test_plan_includes_phase_priority_command_suggestions(self)` |
| `test_plan_includes_tools_matching_open_service` | method | `tests/test_recon_plan.py:204` | `def test_plan_includes_tools_matching_open_service(self)` |
| `test_plan_skips_command_layer_when_index_missing` | method | `tests/test_recon_plan.py:243` | `def test_plan_skips_command_layer_when_index_missing(self)` |
| `test_plan_uses_payload_target_when_argument_missing` | method | `tests/test_recon_plan.py:259` | `def test_plan_uses_payload_target_when_argument_missing(self)` |
| `test_renders_friendly_message_when_empty` | method | `tests/test_recon_plan.py:406` | `def test_renders_friendly_message_when_empty(self)` |
| `test_renders_one_line_per_item` | method | `tests/test_recon_plan.py:389` | `def test_renders_one_line_per_item(self)` |
| `test_tool_preview_substitutes_payload_placeholders` | method | `tests/test_recon_plan.py:210` | `def test_tool_preview_substitutes_payload_placeholders(self)` |
| `test_write_creates_expected_filename` | method | `tests/test_recon_plan.py:351` | `def test_write_creates_expected_filename(self)` |
| `test_write_overwrites_existing_plan` | method | `tests/test_recon_plan.py:370` | `def test_write_overwrites_existing_plan(self)` |
| `test_write_sanitises_target_for_filename` | method | `tests/test_recon_plan.py:358` | `def test_write_sanitises_target_for_filename(self)` |
| `test_write_sets_restrictive_permissions` | method | `tests/test_recon_plan.py:364` | `def test_write_sets_restrictive_permissions(self)` |
| `TestBannersHTML` | class | `tests/test_report_banners_endpoints.py:176` | `class TestBannersHTML` |
| `TestLoadBanners` | class | `tests/test_report_banners_endpoints.py:125` | `class TestLoadBanners` |
| `TestLoadJSONFileSafe` | class | `tests/test_report_banners_endpoints.py:333` | `class TestLoadJSONFileSafe` |
| `TestReportContext` | class | `tests/test_report_banners_endpoints.py:209` | `class TestReportContext` |
| `build_banners_html` | function | `tests/test_report_banners_endpoints.py:95` | `def build_banners_html(banners)` |
| `build_report_context` | function | `tests/test_report_banners_endpoints.py:55` | `def build_report_context(report_file, session_file, tools_dir)` |
| `load_banners` | function | `tests/test_report_banners_endpoints.py:18` | `def load_banners(path)` |
| `load_json_file_safe` | function | `tests/test_report_banners_endpoints.py:38` | `def load_json_file_safe(path)` |
| `test_dict_format` | method | `tests/test_report_banners_endpoints.py:128` | `def test_dict_format(self, tmp_path)` |
| `test_empty_banners` | method | `tests/test_report_banners_endpoints.py:179` | `def test_empty_banners(self)` |
| `test_empty_dict` | method | `tests/test_report_banners_endpoints.py:142` | `def test_empty_dict(self, tmp_path)` |
| `test_empty_file` | method | `tests/test_report_banners_endpoints.py:159` | `def test_empty_file(self, tmp_path)` |
| `test_empty_file` | method | `tests/test_report_banners_endpoints.py:341` | `def test_empty_file(self, tmp_path)` |
| `test_empty_session_file` | method | `tests/test_report_banners_endpoints.py:228` | `def test_empty_session_file(self, tmp_path)` |
| `test_empty_session_list` | method | `tests/test_report_banners_endpoints.py:296` | `def test_empty_session_list(self, tmp_path)` |
| `test_file_not_found` | method | `tests/test_report_banners_endpoints.py:149` | `def test_file_not_found(self, tmp_path)` |
| `test_file_not_found` | method | `tests/test_report_banners_endpoints.py:346` | `def test_file_not_found(self, tmp_path)` |
| `test_flat_list_format` | method | `tests/test_report_banners_endpoints.py:165` | `def test_flat_list_format(self, tmp_path)` |
| `test_invalid_body_report_json` | method | `tests/test_report_banners_endpoints.py:273` | `def test_invalid_body_report_json(self, tmp_path)` |
| `test_invalid_json` | method | `tests/test_report_banners_endpoints.py:153` | `def test_invalid_json(self, tmp_path)` |
| `test_invalid_json` | method | `tests/test_report_banners_endpoints.py:349` | `def test_invalid_json(self, tmp_path)` |
| `test_invalid_json_session` | method | `tests/test_report_banners_endpoints.py:241` | `def test_invalid_json_session(self, tmp_path)` |
| `test_invalid_tool_file_does_not_crash` | method | `tests/test_report_banners_endpoints.py:318` | `def test_invalid_tool_file_does_not_crash(self, tmp_path)` |
| `test_list_json` | method | `tests/test_report_banners_endpoints.py:354` | `def test_list_json(self, tmp_path)` |
| `test_missing_body_report` | method | `tests/test_report_banners_endpoints.py:263` | `def test_missing_body_report(self, tmp_path)` |
| `test_missing_keys_does_not_crash` | method | `tests/test_report_banners_endpoints.py:183` | `def test_missing_keys_does_not_crash(self)` |
| `test_missing_session_file` | method | `tests/test_report_banners_endpoints.py:253` | `def test_missing_session_file(self, tmp_path)` |
| `test_missing_tools_dir` | method | `tests/test_report_banners_endpoints.py:308` | `def test_missing_tools_dir(self, tmp_path)` |
| `test_session_data_as_list` | method | `tests/test_report_banners_endpoints.py:285` | `def test_session_data_as_list(self, tmp_path)` |
| `test_valid_data` | method | `tests/test_report_banners_endpoints.py:196` | `def test_valid_data(self)` |
| `test_valid_files` | method | `tests/test_report_banners_endpoints.py:212` | `def test_valid_files(self, tmp_path)` |
| `test_valid_json` | method | `tests/test_report_banners_endpoints.py:336` | `def test_valid_json(self, tmp_path)` |
| `TestResourceScript` | class | `tests/test_resource_script.py:10` | `class TestResourceScript` |
| `_execute` | method | `tests/test_resource_script.py:14` | `def _execute(script)` |
| `test_break` | method | `tests/test_resource_script.py:197` | `def test_break(self)` |
| `test_builtin_timestamp` | method | `tests/test_resource_script.py:53` | `def test_builtin_timestamp(self)` |
| `test_comment` | method | `tests/test_resource_script.py:219` | `def test_comment(self)` |
| `test_continue` | method | `tests/test_resource_script.py:208` | `def test_continue(self)` |
| `test_dry_run_mode` | method | `tests/test_resource_script.py:116` | `def test_dry_run_mode(self)` |
| `test_eval_condition_contains` | method | `tests/test_resource_script.py:91` | `def test_eval_condition_contains(self)` |
| `test_eval_condition_defined` | method | `tests/test_resource_script.py:97` | `def test_eval_condition_defined(self)` |
| `test_eval_condition_equals` | method | `tests/test_resource_script.py:66` | `def test_eval_condition_equals(self)` |
| `test_eval_condition_fallback_falsy` | method | `tests/test_resource_script.py:104` | `def test_eval_condition_fallback_falsy(self)` |
| `test_eval_condition_fallback_truthy` | method | `tests/test_resource_script.py:110` | `def test_eval_condition_fallback_truthy(self)` |
| `test_eval_condition_not_equals` | method | `tests/test_resource_script.py:72` | `def test_eval_condition_not_equals(self)` |
| `test_eval_condition_numeric` | method | `tests/test_resource_script.py:83` | `def test_eval_condition_numeric(self)` |
| `test_eval_condition_regex` | method | `tests/test_resource_script.py:77` | `def test_eval_condition_regex(self)` |
| `test_for_loop` | method | `tests/test_resource_script.py:170` | `def test_for_loop(self)` |
| `test_for_loop_empty` | method | `tests/test_resource_script.py:178` | `def test_for_loop_empty(self)` |
| `test_if_else_endif_false` | method | `tests/test_resource_script.py:153` | `def test_if_else_endif_false(self)` |
| `test_if_else_endif_true` | method | `tests/test_resource_script.py:143` | `def test_if_else_endif_true(self)` |
| `test_macro_and_call` | method | `tests/test_resource_script.py:228` | `def test_macro_and_call(self)` |
| `test_nested_if` | method | `tests/test_resource_script.py:267` | `def test_nested_if(self)` |
| `test_resolve_unresolved` | method | `tests/test_resource_script.py:60` | `def test_resolve_unresolved(self)` |
| `test_set_and_echo` | method | `tests/test_resource_script.py:163` | `def test_set_and_echo(self)` |
| `test_set_and_get` | method | `tests/test_resource_script.py:25` | `def test_set_and_get(self)` |
| `test_setg_and_get` | method | `tests/test_resource_script.py:31` | `def test_setg_and_get(self)` |
| `test_skip_depth` | method | `tests/test_resource_script.py:125` | `def test_skip_depth(self)` |
| `test_spool` | method | `tests/test_resource_script.py:238` | `def test_spool(self, tmp_path)` |
| `test_undefined_macro_raises` | method | `tests/test_resource_script.py:253` | `def test_undefined_macro_raises(self)` |
| `test_unset_removes_var` | method | `tests/test_resource_script.py:37` | `def test_unset_removes_var(self)` |
| `test_unset_variable` | method | `tests/test_resource_script.py:258` | `def test_unset_variable(self)` |
| `test_var_substitution` | method | `tests/test_resource_script.py:46` | `def test_var_substitution(self)` |
| `test_while_loop` | method | `tests/test_resource_script.py:187` | `def test_while_loop(self)` |
| `TestRunArgv` | class | `tests/test_safe_subprocess.py:35` | `class TestRunArgv` |
| `TestRunShellAllowed` | class | `tests/test_safe_subprocess.py:71` | `class TestRunShellAllowed` |
| `TestRunShellDefaultDeny` | class | `tests/test_safe_subprocess.py:53` | `class TestRunShellDefaultDeny` |
| `test_allowed_executes` | method | `tests/test_safe_subprocess.py:74` | `def test_allowed_executes(self)` |
| `test_allowed_is_audited` | method | `tests/test_safe_subprocess.py:84` | `def test_allowed_is_audited(self, tmp_path)` |
| `test_default_deny_raises` | method | `tests/test_safe_subprocess.py:56` | `def test_default_deny_raises(self)` |
| `test_deny_audit_logged` | method | `tests/test_safe_subprocess.py:61` | `def test_deny_audit_logged(self, tmp_path)` |
| `test_empty_reason_rejected` | method | `tests/test_safe_subprocess.py:94` | `def test_empty_reason_rejected(self)` |
| `test_failed_command_returns_nonzero` | method | `tests/test_safe_subprocess.py:99` | `def test_failed_command_returns_nonzero(self)` |
| `test_run_does_not_audit` | method | `tests/test_safe_subprocess.py:46` | `def test_run_does_not_audit(self, tmp_path)` |
| `test_run_returns_completed_result` | method | `tests/test_safe_subprocess.py:38` | `def test_run_returns_completed_result(self)` |
| `test_given_argv_when_run_then_executes_without_audit` | function | `tests/test_safe_subprocess_behavior.py:12` | `def test_given_argv_when_run_then_executes_without_audit(tmp_path)` |
| `test_given_shell_with_allow_and_reason_when_called_then_executes` | function | `tests/test_safe_subprocess_behavior.py:36` | `def test_given_shell_with_allow_and_reason_when_called_then_executes(tmp_path)` |
| `test_given_shell_without_allow_when_called_then_denied` | function | `tests/test_safe_subprocess_behavior.py:22` | `def test_given_shell_without_allow_when_called_then_denied(tmp_path)` |
| `TestAutoEngageWiring` | class | `tests/test_scope_bound_auto_gate.py:191` | `class TestAutoEngageWiring` |
| `TestDefaultScopePredicate` | class | `tests/test_scope_bound_auto_gate.py:152` | `class TestDefaultScopePredicate` |
| `TestFailClosedAutonomy` | class | `tests/test_scope_bound_auto_gate.py:262` | `class TestFailClosedAutonomy` |
| `TestScopeBoundAutoGate` | class | `tests/test_scope_bound_auto_gate.py:49` | `class TestScopeBoundAutoGate` |
| `_CountingRunner` | class | `tests/test_scope_bound_auto_gate.py:247` | `class _CountingRunner` |
| `_SpyOrchestrator` | class | `tests/test_scope_bound_auto_gate.py:200` | `class _SpyOrchestrator` |
| `_SpyOrchestrator` | class | `tests/test_scope_bound_auto_gate.py:221` | `class _SpyOrchestrator` |
| `__init__` | method | `tests/test_scope_bound_auto_gate.py:201` | `def __init__(self, target, max_switches_per_step, approval_gate)` |
| `__init__` | method | `tests/test_scope_bound_auto_gate.py:222` | `def __init__(self, target, max_switches_per_step, approval_gate)` |
| `__init__` | method | `tests/test_scope_bound_auto_gate.py:250` | `def __init__(self)` |
| `_boom` | method | `tests/test_scope_bound_auto_gate.py:178` | `def _boom(target, entries)` |
| `_explode` | method | `tests/test_scope_bound_auto_gate.py:237` | `def _explode()` |
| `_gate` | function | `tests/test_scope_bound_auto_gate.py:39` | `def _gate(tmp_path, data, in_scope_fn)` |
| `_write_payload` | function | `tests/test_scope_bound_auto_gate.py:32` | `def _write_payload(tmp_path, data)` |
| `name` | method | `tests/test_scope_bound_auto_gate.py:258` | `def name(self)` |
| `run` | method | `tests/test_scope_bound_auto_gate.py:205` | `def run(self)` |
| `run` | method | `tests/test_scope_bound_auto_gate.py:226` | `def run(self)` |
| `run` | method | `tests/test_scope_bound_auto_gate.py:253` | `def run(self, command, timeout)` |
| `temp_engagement` | method | `tests/test_scope_bound_auto_gate.py:266` | `def temp_engagement(self, tmp_path)` |
| `test_approves_in_scope_under_enforce` | method | `tests/test_scope_bound_auto_gate.py:69` | `def test_approves_in_scope_under_enforce(self, tmp_path)` |
| `test_auto_wires_scope_bound_gate_and_chains_report` | method | `tests/test_scope_bound_auto_gate.py:194` | `def test_auto_wires_scope_bound_gate_and_chains_report(self, monkeypatch)` |
| `test_default_enforcement_is_warn` | method | `tests/test_scope_bound_auto_gate.py:103` | `def test_default_enforcement_is_warn(self, tmp_path)` |
| `test_default_predicate_matches_cidr` | method | `tests/test_scope_bound_auto_gate.py:155` | `def test_default_predicate_matches_cidr(self, tmp_path)` |
| `test_denies_out_of_scope_under_enforce` | method | `tests/test_scope_bound_auto_gate.py:79` | `def test_denies_out_of_scope_under_enforce(self, tmp_path)` |
| `test_dormant_when_enforcement_off` | method | `tests/test_scope_bound_auto_gate.py:61` | `def test_dormant_when_enforcement_off(self, tmp_path)` |
| `test_dormant_when_scope_empty` | method | `tests/test_scope_bound_auto_gate.py:52` | `def test_dormant_when_scope_empty(self, tmp_path)` |
| `test_honours_approval_gate_interface` | method | `tests/test_scope_bound_auto_gate.py:142` | `def test_honours_approval_gate_interface(self, tmp_path)` |
| `test_in_scope_fails_closed_on_predicate_error` | method | `tests/test_scope_bound_auto_gate.py:175` | `def test_in_scope_fails_closed_on_predicate_error(self, tmp_path)` |
| `test_in_scope_target_executes_steps` | method | `tests/test_scope_bound_auto_gate.py:302` | `def test_in_scope_target_executes_steps(self, temp_engagement)` |
| `test_maybe_generate_report_is_best_effort` | method | `tests/test_scope_bound_auto_gate.py:234` | `def test_maybe_generate_report_is_best_effort(self, monkeypatch)` |
| `test_missing_payload_is_dormant` | method | `tests/test_scope_bound_auto_gate.py:125` | `def test_missing_payload_is_dormant(self, tmp_path)` |
| `test_never_blocks_returns_synchronously` | method | `tests/test_scope_bound_auto_gate.py:131` | `def test_never_blocks_returns_synchronously(self, tmp_path)` |
| `test_non_auto_uses_default_gate_and_no_report` | method | `tests/test_scope_bound_auto_gate.py:216` | `def test_non_auto_uses_default_gate_and_no_report(self, monkeypatch)` |
| `test_normalize_scope_drops_blanks` | method | `tests/test_scope_bound_auto_gate.py:166` | `def test_normalize_scope_drops_blanks(self)` |
| `test_out_of_scope_denies_all_steps_runner_never_called` | method | `tests/test_scope_bound_auto_gate.py:285` | `def test_out_of_scope_denies_all_steps_runner_never_called(self, temp_engagement)` |
| `test_reads_payload_at_request_time` | method | `tests/test_scope_bound_auto_gate.py:111` | `def test_reads_payload_at_request_time(self, tmp_path)` |
| `test_warns_but_approves_out_of_scope` | method | `tests/test_scope_bound_auto_gate.py:92` | `def test_warns_but_approves_out_of_scope(self, tmp_path)` |
| `TestBuildOffensiveCommands` | class | `tests/test_scope_guard.py:116` | `class TestBuildOffensiveCommands` |
| `TestNormalizeScope` | class | `tests/test_scope_guard.py:50` | `class TestNormalizeScope` |
| `TestOffensiveCategoryDrift` | class | `tests/test_scope_guard.py:191` | `class TestOffensiveCategoryDrift` |
| `TestScopeGuardEvaluate` | class | `tests/test_scope_guard.py:137` | `class TestScopeGuardEvaluate` |
| `TestScopeMode` | class | `tests/test_scope_guard.py:33` | `class TestScopeMode` |
| `TestTargetInScope` | class | `tests/test_scope_guard.py:77` | `class TestTargetInScope` |
| `_guard` | method | `tests/test_scope_guard.py:132` | `def _guard(scope, mode, offensive_names)` |
| `boom` | method | `tests/test_scope_guard.py:177` | `def boom(_name)` |
| `test_bare_ip_match` | method | `tests/test_scope_guard.py:87` | `def test_bare_ip_match(self)` |
| `test_bare_ip_mismatch` | method | `tests/test_scope_guard.py:90` | `def test_bare_ip_mismatch(self)` |
| `test_benign_command_allowed` | method | `tests/test_scope_guard.py:148` | `def test_benign_command_allowed(self)` |
| `test_blank_entries_ignored` | method | `tests/test_scope_guard.py:112` | `def test_blank_entries_ignored(self)` |
| `test_categories_exist_in_utils` | method | `tests/test_scope_guard.py:194` | `def test_categories_exist_in_utils(self)` |
| `test_classifier_exception_fails_open` | method | `tests/test_scope_guard.py:176` | `def test_classifier_exception_fails_open(self)` |
| `test_comma_separated_string` | method | `tests/test_scope_guard.py:64` | `def test_comma_separated_string(self)` |
| `test_decision_is_value_object` | method | `tests/test_scope_guard.py:184` | `def test_decision_is_value_object(self)` |
| `test_empty` | method | `tests/test_scope_guard.py:128` | `def test_empty(self)` |
| `test_empty_string` | method | `tests/test_scope_guard.py:70` | `def test_empty_string(self)` |
| `test_empty_target` | method | `tests/test_scope_guard.py:78` | `def test_empty_target(self)` |
| `test_empty_target_allowed` | method | `tests/test_scope_guard.py:153` | `def test_empty_target_allowed(self)` |
| `test_exact_hostname` | method | `tests/test_scope_guard.py:93` | `def test_exact_hostname(self)` |
| `test_from_value_passthrough` | method | `tests/test_scope_guard.py:34` | `def test_from_value_passthrough(self)` |
| `test_from_value_strings` | method | `tests/test_scope_guard.py:42` | `def test_from_value_strings(self, raw, expected)` |
| `test_hostname_not_in_cidr` | method | `tests/test_scope_guard.py:103` | `def test_hostname_not_in_cidr(self)` |
| `test_in_scope_allowed` | method | `tests/test_scope_guard.py:157` | `def test_in_scope_allowed(self)` |
| `test_ip_in_cidr` | method | `tests/test_scope_guard.py:81` | `def test_ip_in_cidr(self)` |
| `test_ip_not_matched_by_hostname_entry` | method | `tests/test_scope_guard.py:106` | `def test_ip_not_matched_by_hostname_entry(self)` |
| `test_ip_outside_cidr` | method | `tests/test_scope_guard.py:84` | `def test_ip_outside_cidr(self)` |
| `test_ipv6_in_cidr` | method | `tests/test_scope_guard.py:109` | `def test_ipv6_in_cidr(self)` |
| `test_json_array_string` | method | `tests/test_scope_guard.py:61` | `def test_json_array_string(self)` |
| `test_list` | method | `tests/test_scope_guard.py:54` | `def test_list(self)` |
| `test_mode_off_is_noop` | method | `tests/test_scope_guard.py:138` | `def test_mode_off_is_noop(self)` |
| `test_no_scope_allows` | method | `tests/test_scope_guard.py:143` | `def test_no_scope_allows(self)` |
| `test_none` | method | `tests/test_scope_guard.py:51` | `def test_none(self)` |
| `test_out_of_scope_enforce_blocks` | method | `tests/test_scope_guard.py:169` | `def test_out_of_scope_enforce_blocks(self)` |
| `test_out_of_scope_warn_allows_with_reason` | method | `tests/test_scope_guard.py:162` | `def test_out_of_scope_warn_allows_with_reason(self)` |
| `test_selects_offensive_only` | method | `tests/test_scope_guard.py:117` | `def test_selects_offensive_only(self)` |
| `test_space_separated_string` | method | `tests/test_scope_guard.py:67` | `def test_space_separated_string(self)` |
| `test_subdomain_match` | method | `tests/test_scope_guard.py:96` | `def test_subdomain_match(self)` |
| `test_tuple_and_set` | method | `tests/test_scope_guard.py:57` | `def test_tuple_and_set(self)` |
| `test_unknown_defaults_to_warn` | method | `tests/test_scope_guard.py:46` | `def test_unknown_defaults_to_warn(self, raw)` |
| `test_unsupported_type` | method | `tests/test_scope_guard.py:73` | `def test_unsupported_type(self)` |
| `test_wildcard_match` | method | `tests/test_scope_guard.py:99` | `def test_wildcard_match(self)` |
| `TestOffensiveClassificationIsBuilt` | class | `tests/test_scope_guard_integration.py:137` | `class TestOffensiveClassificationIsBuilt` |
| `TestResolveOffensive` | class | `tests/test_scope_guard_integration.py:40` | `class TestResolveOffensive` |
| `TestScopeCheck` | class | `tests/test_scope_guard_integration.py:58` | `class TestScopeCheck` |
| `TestScopeConfirmNonInteractive` | class | `tests/test_scope_guard_integration.py:119` | `class TestScopeConfirmNonInteractive` |
| `TestScopeEntries` | class | `tests/test_scope_guard_integration.py:127` | `class TestScopeEntries` |
| `_do_benign` | method | `tests/test_scope_guard_integration.py:146` | `def _do_benign()` |
| `_do_offensive` | method | `tests/test_scope_guard_integration.py:143` | `def _do_offensive()` |
| `_make_stub` | function | `tests/test_scope_guard_integration.py:28` | `def _make_stub(params, offensive, aliases, confirm)` |
| `test_alias_to_benign` | method | `tests/test_scope_guard_integration.py:53` | `def test_alias_to_benign(self)` |
| `test_alias_to_offensive` | method | `tests/test_scope_guard_integration.py:49` | `def test_alias_to_offensive(self)` |
| `test_benign` | method | `tests/test_scope_guard_integration.py:45` | `def test_benign(self)` |
| `test_benign_command_allows` | method | `tests/test_scope_guard_integration.py:73` | `def test_benign_command_allows(self)` |
| `test_build_offensive_from_categories` | method | `tests/test_scope_guard_integration.py:138` | `def test_build_offensive_from_categories(self)` |
| `test_direct_offensive` | method | `tests/test_scope_guard_integration.py:41` | `def test_direct_offensive(self)` |
| `test_enforce_mode_blocks_out_of_scope` | method | `tests/test_scope_guard_integration.py:87` | `def test_enforce_mode_blocks_out_of_scope(self)` |
| `test_enforce_mode_confirmation_allows` | method | `tests/test_scope_guard_integration.py:95` | `def test_enforce_mode_confirmation_allows(self)` |
| `test_in_scope_allows` | method | `tests/test_scope_guard_integration.py:66` | `def test_in_scope_allows(self)` |
| `test_malformed_params_fail_open` | method | `tests/test_scope_guard_integration.py:110` | `def test_malformed_params_fail_open(self)` |
| `test_no_scope_allows` | method | `tests/test_scope_guard_integration.py:59` | `def test_no_scope_allows(self)` |
| `test_non_tty_refuses` | method | `tests/test_scope_guard_integration.py:120` | `def test_non_tty_refuses(self, monkeypatch)` |
| `test_normalizes_list` | method | `tests/test_scope_guard_integration.py:128` | `def test_normalizes_list(self)` |
| `test_normalizes_string` | method | `tests/test_scope_guard_integration.py:132` | `def test_normalizes_string(self)` |
| `test_off_mode_allows` | method | `tests/test_scope_guard_integration.py:103` | `def test_off_mode_allows(self)` |
| `test_warn_mode_allows_out_of_scope` | method | `tests/test_scope_guard_integration.py:80` | `def test_warn_mode_allows_out_of_scope(self, capsys)` |
| `TestAuthTimingIntegration` | class | `tests/test_security_hardening.py:377` | `class TestAuthTimingIntegration` |
| `TestCalderaConfigSecrets` | class | `tests/test_security_hardening.py:250` | `class TestCalderaConfigSecrets` |
| `TestConfigConstantsConsolidation` | class | `tests/test_security_hardening.py:279` | `class TestConfigConstantsConsolidation` |
| `TestCredentialEncryptionWarning` | class | `tests/test_security_hardening.py:325` | `class TestCredentialEncryptionWarning` |
| `TestLIKEEscapePrevention` | class | `tests/test_security_hardening.py:84` | `class TestLIKEEscapePrevention` |
| `TestOpenSSLConf` | class | `tests/test_security_hardening.py:357` | `class TestOpenSSLConf` |
| `TestPickleRemoved` | class | `tests/test_security_hardening.py:229` | `class TestPickleRemoved` |
| `TestSQLInjectionPrevention` | class | `tests/test_security_hardening.py:34` | `class TestSQLInjectionPrevention` |
| `TestSafeRunnerShellFalse` | class | `tests/test_security_hardening.py:176` | `class TestSafeRunnerShellFalse` |
| `TestTimingAttackPrevention` | class | `tests/test_security_hardening.py:132` | `class TestTimingAttackPrevention` |
| `db_with_hosts` | method | `tests/test_security_hardening.py:89` | `def db_with_hosts(self)` |
| `fresh_db` | method | `tests/test_security_hardening.py:72` | `def fresh_db(self)` |
| `test_ai_fallback_imports_from_llm_factory` | method | `tests/test_security_hardening.py:291` | `def test_ai_fallback_imports_from_llm_factory(self)` |
| `test_caldera_config_uses_secrets_module` | method | `tests/test_security_hardening.py:263` | `def test_caldera_config_uses_secrets_module(self)` |
| `test_check_auth_returns_false_for_wrong_credentials` | method | `tests/test_security_hardening.py:380` | `def test_check_auth_returns_false_for_wrong_credentials(self)` |
| `test_check_auth_uses_hmac_compare_digest` | method | `tests/test_security_hardening.py:136` | `def test_check_auth_uses_hmac_compare_digest(self)` |
| `test_cli_ai_imports_from_llm_factory` | method | `tests/test_security_hardening.py:306` | `def test_cli_ai_imports_from_llm_factory(self)` |
| `test_db_maybe_decrypt_logs_failure` | method | `tests/test_security_hardening.py:344` | `def test_db_maybe_decrypt_logs_failure(self)` |
| `test_db_maybe_encrypt_has_warning_log` | method | `tests/test_security_hardening.py:336` | `def test_db_maybe_encrypt_has_warning_log(self)` |
| `test_db_module_has_logging_import` | method | `tests/test_security_hardening.py:329` | `def test_db_module_has_logging_import(self)` |
| `test_export_csv_accepts_all_valid_tables` | method | `tests/test_security_hardening.py:57` | `def test_export_csv_accepts_all_valid_tables(self, fresh_db)` |
| `test_export_csv_rejects_malicious_table_name` | method | `tests/test_security_hardening.py:45` | `def test_export_csv_rejects_malicious_table_name(self, fresh_db)` |
| `test_export_csv_rejects_union_select` | method | `tests/test_security_hardening.py:51` | `def test_export_csv_rejects_union_select(self, fresh_db)` |
| `test_hmac_compare_digest_rejects_timing_difference` | method | `tests/test_security_hardening.py:161` | `def test_hmac_compare_digest_rejects_timing_difference(self)` |
| `test_hmac_module_imported_in_lazyc2` | method | `tests/test_security_hardening.py:390` | `def test_hmac_module_imported_in_lazyc2(self)` |
| `test_llm_factory_defines_constants` | method | `tests/test_security_hardening.py:283` | `def test_llm_factory_defines_constants(self)` |
| `test_no_hardcoded_api_keys_in_caldera_config` | method | `tests/test_security_hardening.py:254` | `def test_no_hardcoded_api_keys_in_caldera_config(self)` |
| `test_normal_query_still_works` | method | `tests/test_security_hardening.py:116` | `def test_normal_query_still_works(self, db_with_hosts)` |
| `test_openssl_conf_uses_setdefault` | method | `tests/test_security_hardening.py:361` | `def test_openssl_conf_uses_setdefault(self)` |
| `test_percent_literal_not_wildcard` | method | `tests/test_security_hardening.py:98` | `def test_percent_literal_not_wildcard(self, db_with_hosts)` |
| `test_pickle_not_imported_in_utils` | method | `tests/test_security_hardening.py:233` | `def test_pickle_not_imported_in_utils(self)` |
| `test_run_shell_does_not_use_shell_true` | method | `tests/test_security_hardening.py:181` | `def test_run_shell_does_not_use_shell_true(self)` |
| `test_run_shell_with_pipe_character` | method | `tests/test_security_hardening.py:200` | `def test_run_shell_with_pipe_character(self)` |
| `test_run_shell_with_semicolon_is_treated_as_argument` | method | `tests/test_security_hardening.py:212` | `def test_run_shell_with_semicolon_is_treated_as_argument(self)` |
| `test_underscore_literal_not_wildcard` | method | `tests/test_security_hardening.py:107` | `def test_underscore_literal_not_wildcard(self, db_with_hosts)` |
| `test_valid_tables_constant_is_complete` | method | `tests/test_security_hardening.py:39` | `def test_valid_tables_constant_is_complete(self)` |
| `TestAICommandInjectionPrevention` | class | `tests/test_security_hardening_v2.py:33` | `class TestAICommandInjectionPrevention` |
| `TestCredentialEncryptionAtRest` | class | `tests/test_security_hardening_v2.py:284` | `class TestCredentialEncryptionAtRest` |
| `TestDNSCommandAllowlist` | class | `tests/test_security_hardening_v2.py:157` | `class TestDNSCommandAllowlist` |
| `TestNoOsSystemInCriticalPaths` | class | `tests/test_security_hardening_v2.py:344` | `class TestNoOsSystemInCriticalPaths` |
| `TestSSHCredentialInjectionPrevention` | class | `tests/test_security_hardening_v2.py:93` | `class TestSSHCredentialInjectionPrevention` |
| `TestSafeShellExecution` | class | `tests/test_security_hardening_v2.py:217` | `class TestSafeShellExecution` |
| `_read` | function | `tests/test_security_hardening_v2.py:25` | `def _read(relpath)` |
| `test_ai_module_no_os_system` | method | `tests/test_security_hardening_v2.py:349` | `def test_ai_module_no_os_system(self)` |
| `test_allowlist_exists_as_frozenset` | method | `tests/test_security_hardening_v2.py:163` | `def test_allowlist_exists_as_frozenset(self)` |
| `test_allowlist_is_finite_and_reasonable` | method | `tests/test_security_hardening_v2.py:175` | `def test_allowlist_is_finite_and_reasonable(self)` |
| `test_answers_through_canonical_backend` | method | `tests/test_security_hardening_v2.py:69` | `def test_answers_through_canonical_backend(self)` |
| `test_api_key_never_leaves_factory_path` | method | `tests/test_security_hardening_v2.py:62` | `def test_api_key_never_leaves_factory_path(self)` |
| `test_credential_key_derivation` | method | `tests/test_security_hardening_v2.py:333` | `def test_credential_key_derivation(self)` |
| `test_dangerous_command_not_in_allowlist` | method | `tests/test_security_hardening_v2.py:199` | `def test_dangerous_command_not_in_allowlist(self)` |
| `test_decrypt_function_exists` | method | `tests/test_security_hardening_v2.py:297` | `def test_decrypt_function_exists(self)` |
| `test_dns_handler_checks_allowlist` | method | `tests/test_security_hardening_v2.py:187` | `def test_dns_handler_checks_allowlist(self)` |
| `test_dns_handler_checks_length` | method | `tests/test_security_hardening_v2.py:193` | `def test_dns_handler_checks_length(self)` |
| `test_dns_resolver_has_allowlist_guard` | method | `tests/test_security_hardening_v2.py:374` | `def test_dns_resolver_has_allowlist_guard(self)` |
| `test_do_sys_captures_output` | method | `tests/test_security_hardening_v2.py:243` | `def test_do_sys_captures_output(self)` |
| `test_do_sys_uses_safe_runner` | method | `tests/test_security_hardening_v2.py:224` | `def test_do_sys_uses_safe_runner(self)` |
| `test_encrypt_function_exists` | method | `tests/test_security_hardening_v2.py:291` | `def test_encrypt_function_exists(self)` |
| `test_hash_function_exists` | method | `tests/test_security_hardening_v2.py:303` | `def test_hash_function_exists(self)` |
| `test_imports_base64_for_encoding` | method | `tests/test_security_hardening_v2.py:327` | `def test_imports_base64_for_encoding(self)` |
| `test_log_uses_hash_not_plaintext` | method | `tests/test_security_hardening_v2.py:315` | `def test_log_uses_hash_not_plaintext(self)` |
| `test_max_length_constant_exists` | method | `tests/test_security_hardening_v2.py:169` | `def test_max_length_constant_exists(self)` |
| `test_misc_sys_no_os_system` | method | `tests/test_security_hardening_v2.py:381` | `def test_misc_sys_no_os_system(self)` |
| `test_no_fstring_with_api_key_in_command` | method | `tests/test_security_hardening_v2.py:76` | `def test_no_fstring_with_api_key_in_command(self)` |
| `test_no_os_system_in_ai_module` | method | `tests/test_security_hardening_v2.py:42` | `def test_no_os_system_in_ai_module(self)` |
| `test_no_os_system_in_misc_module_code` | method | `tests/test_security_hardening_v2.py:261` | `def test_no_os_system_in_misc_module_code(self)` |
| `test_no_shell_true_in_ai_module` | method | `tests/test_security_hardening_v2.py:56` | `def test_no_shell_true_in_ai_module(self)` |
| `test_no_sshpass_minus_p_in_code` | method | `tests/test_security_hardening_v2.py:100` | `def test_no_sshpass_minus_p_in_code(self)` |
| `test_no_subprocess_in_ai_module` | method | `tests/test_security_hardening_v2.py:48` | `def test_no_subprocess_in_ai_module(self)` |
| `test_password_not_in_fstring_command` | method | `tests/test_security_hardening_v2.py:135` | `def test_password_not_in_fstring_command(self)` |
| `test_postexp_no_sshpass_in_fstring_code` | method | `tests/test_security_hardening_v2.py:356` | `def test_postexp_no_sshpass_in_fstring_code(self)` |
| `test_record_credentials_encrypts_password` | method | `tests/test_security_hardening_v2.py:309` | `def test_record_credentials_encrypts_password(self)` |
| `test_sshpass_in_list_form` | method | `tests/test_security_hardening_v2.py:129` | `def test_sshpass_in_list_form(self)` |
| `test_sshpass_uses_e_flag` | method | `tests/test_security_hardening_v2.py:117` | `def test_sshpass_uses_e_flag(self)` |
| `test_ssppass_env_var_used` | method | `tests/test_security_hardening_v2.py:123` | `def test_ssppass_env_var_used(self)` |
| `test_uses_aes_encryption` | method | `tests/test_security_hardening_v2.py:321` | `def test_uses_aes_encryption(self)` |
| `TestAntiForensicsCommands` | class | `tests/test_security_hardening_v3.py:439` | `class TestAntiForensicsCommands` |
| `TestBuildSshpassCommand` | class | `tests/test_security_hardening_v3.py:134` | `class TestBuildSshpassCommand` |
| `TestEscapeHtmlContent` | class | `tests/test_security_hardening_v3.py:182` | `class TestEscapeHtmlContent` |
| `TestIcmpServerCommandExecution` | class | `tests/test_security_hardening_v3.py:379` | `class TestIcmpServerCommandExecution` |
| `TestPhishingOrchestratorKey` | class | `tests/test_security_hardening_v3.py:356` | `class TestPhishingOrchestratorKey` |
| `TestPivotingCommands` | class | `tests/test_security_hardening_v3.py:420` | `class TestPivotingCommands` |
| `TestRequireEncryptionKey` | class | `tests/test_security_hardening_v3.py:305` | `class TestRequireEncryptionKey` |
| `TestResourceScriptEngine` | class | `tests/test_security_hardening_v3.py:405` | `class TestResourceScriptEngine` |
| `TestSafeClipboardCopy` | class | `tests/test_security_hardening_v3.py:116` | `class TestSafeClipboardCopy` |
| `TestSafePathJoin` | class | `tests/test_security_hardening_v3.py:213` | `class TestSafePathJoin` |
| `TestSafeSubprocessRun` | class | `tests/test_security_hardening_v3.py:21` | `class TestSafeSubprocessRun` |
| `TestSanitizeFilename` | class | `tests/test_security_hardening_v3.py:332` | `class TestSanitizeFilename` |
| `TestSetSshpassEnv` | class | `tests/test_security_hardening_v3.py:159` | `class TestSetSshpassEnv` |
| `TestValidateHost` | class | `tests/test_security_hardening_v3.py:284` | `class TestValidateHost` |
| `TestValidateNetworkCidr` | class | `tests/test_security_hardening_v3.py:244` | `class TestValidateNetworkCidr` |
| `TestValidatePortSpec` | class | `tests/test_security_hardening_v3.py:266` | `class TestValidatePortSpec` |
| `test_accepts_valid_cidr` | method | `tests/test_security_hardening_v3.py:248` | `def test_accepts_valid_cidr(self)` |
| `test_accepts_valid_hostname` | method | `tests/test_security_hardening_v3.py:293` | `def test_accepts_valid_hostname(self)` |
| `test_accepts_valid_ip` | method | `tests/test_security_hardening_v3.py:288` | `def test_accepts_valid_ip(self)` |
| `test_accepts_valid_ports` | method | `tests/test_security_hardening_v3.py:270` | `def test_accepts_valid_ports(self)` |
| `test_allows_safe_paths` | method | `tests/test_security_hardening_v3.py:217` | `def test_allows_safe_paths(self, tmp_path)` |
| `test_anti_forensics_has_no_shell_true` | method | `tests/test_security_hardening_v3.py:443` | `def test_anti_forensics_has_no_shell_true(self)` |
| `test_blocks_symlink_escape` | method | `tests/test_security_hardening_v3.py:229` | `def test_blocks_symlink_escape(self, tmp_path)` |
| `test_blocks_traversal` | method | `tests/test_security_hardening_v3.py:223` | `def test_blocks_traversal(self, tmp_path)` |
| `test_capture_output_default_true` | method | `tests/test_security_hardening_v3.py:82` | `def test_capture_output_default_true(self)` |
| `test_captures_stderr` | method | `tests/test_security_hardening_v3.py:44` | `def test_captures_stderr(self)` |
| `test_check_false` | method | `tests/test_security_hardening_v3.py:93` | `def test_check_false(self)` |
| `test_escapes_quotes` | method | `tests/test_security_hardening_v3.py:193` | `def test_escapes_quotes(self)` |
| `test_escapes_script_tags` | method | `tests/test_security_hardening_v3.py:186` | `def test_escapes_script_tags(self)` |
| `test_execute_command_uses_list_form` | method | `tests/test_security_hardening_v3.py:383` | `def test_execute_command_uses_list_form(self)` |
| `test_handles_empty` | method | `tests/test_security_hardening_v3.py:343` | `def test_handles_empty(self)` |
| `test_handles_empty_command` | method | `tests/test_security_hardening_v3.py:392` | `def test_handles_empty_command(self)` |
| `test_handles_empty_string` | method | `tests/test_security_hardening_v3.py:206` | `def test_handles_empty_string(self)` |
| `test_handles_invalid_command` | method | `tests/test_security_hardening_v3.py:398` | `def test_handles_invalid_command(self)` |
| `test_pivoting_module_has_no_shell_true` | method | `tests/test_security_hardening_v3.py:424` | `def test_pivoting_module_has_no_shell_true(self)` |
| `test_preserves_existing_env` | method | `tests/test_security_hardening_v3.py:169` | `def test_preserves_existing_env(self)` |
| `test_preserves_safe_content` | method | `tests/test_security_hardening_v3.py:200` | `def test_preserves_safe_content(self)` |
| `test_raises_without_key` | method | `tests/test_security_hardening_v3.py:309` | `def test_raises_without_key(self)` |
| `test_raises_without_key` | method | `tests/test_security_hardening_v3.py:360` | `def test_raises_without_key(self)` |
| `test_reads_from_env` | method | `tests/test_security_hardening_v3.py:316` | `def test_reads_from_env(self)` |
| `test_reads_from_file` | method | `tests/test_security_hardening_v3.py:323` | `def test_reads_from_file(self, tmp_path)` |
| `test_rejects_empty` | method | `tests/test_security_hardening_v3.py:260` | `def test_rejects_empty(self)` |
| `test_rejects_empty_argv` | method | `tests/test_security_hardening_v3.py:25` | `def test_rejects_empty_argv(self)` |
| `test_rejects_empty_path` | method | `tests/test_security_hardening_v3.py:237` | `def test_rejects_empty_path(self, tmp_path)` |
| `test_rejects_invalid` | method | `tests/test_security_hardening_v3.py:298` | `def test_rejects_invalid(self)` |
| `test_rejects_invalid_cidr` | method | `tests/test_security_hardening_v3.py:254` | `def test_rejects_invalid_cidr(self)` |
| `test_rejects_invalid_ports` | method | `tests/test_security_hardening_v3.py:277` | `def test_rejects_invalid_ports(self)` |
| `test_rejects_null_bytes` | method | `tests/test_security_hardening_v3.py:31` | `def test_rejects_null_bytes(self)` |
| `test_rejects_null_bytes` | method | `tests/test_security_hardening_v3.py:175` | `def test_rejects_null_bytes(self)` |
| `test_rejects_null_bytes_in_password` | method | `tests/test_security_hardening_v3.py:152` | `def test_rejects_null_bytes_in_password(self)` |
| `test_rejects_oversized_content` | method | `tests/test_security_hardening_v3.py:120` | `def test_rejects_oversized_content(self)` |
| `test_rejects_oversized_password` | method | `tests/test_security_hardening_v3.py:146` | `def test_rejects_oversized_password(self)` |
| `test_removes_dangerous_chars` | method | `tests/test_security_hardening_v3.py:336` | `def test_removes_dangerous_chars(self)` |
| `test_returns_completed_process_fields` | method | `tests/test_security_hardening_v3.py:62` | `def test_returns_completed_process_fields(self)` |
| `test_returns_false_without_clipboard_tool` | method | `tests/test_security_hardening_v3.py:126` | `def test_returns_false_without_clipboard_tool(self)` |
| `test_run_command_uses_list_form` | method | `tests/test_security_hardening_v3.py:409` | `def test_run_command_uses_list_form(self)` |
| `test_runs_command_without_shell` | method | `tests/test_security_hardening_v3.py:37` | `def test_runs_command_without_shell(self)` |
| `test_sets_ssplash_env` | method | `tests/test_security_hardening_v3.py:163` | `def test_sets_ssplash_env(self)` |
| `test_shell_false_enforced` | method | `tests/test_security_hardening_v3.py:51` | `def test_shell_false_enforced(self)` |
| `test_text_mode_enabled` | method | `tests/test_security_hardening_v3.py:104` | `def test_text_mode_enabled(self)` |
| `test_timeout_passed_through` | method | `tests/test_security_hardening_v3.py:71` | `def test_timeout_passed_through(self)` |

Next: [SYMBOLS_p34.md](SYMBOLS_p34.md)
