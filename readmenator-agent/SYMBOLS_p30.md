# Symbols (page 30 of 35)
Previous: [SYMBOLS_p29.md](SYMBOLS_p29.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `TestNormalisers` | class | `tests/test_exploration_and_addons.py:148` | `class TestNormalisers` |
| `TestRenderer` | class | `tests/test_exploration_and_addons.py:337` | `class TestRenderer` |
| `TestResolveCurrentOs` | class | `tests/test_exploration_and_addons.py:316` | `class TestResolveCurrentOs` |
| `TestShippedAddonsRespectSchema` | class | `tests/test_exploration_and_addons.py:362` | `class TestShippedAddonsRespectSchema` |
| `TestTriggerMatcher` | class | `tests/test_exploration_and_addons.py:262` | `class TestTriggerMatcher` |
| `_addon` | method | `tests/test_exploration_and_addons.py:395` | `def _addon(name, addon_os, trigger, enabled)` |
| `_svc` | method | `tests/test_exploration_and_addons.py:410` | `def _svc(service, port)` |
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
| `_FakeView` | class | `tests/test_fuzzy_picker.py:35` | `class _FakeView(PickerView)` |
| `__init__` | method | `tests/test_fuzzy_picker.py:38` | `def __init__(self, selection_index)` |
| `_collect_runtime_strings` | method | `tests/test_fuzzy_picker.py:198` | `def _collect_runtime_strings()` |
| `_collect_string_constants` | method | `tests/test_fuzzy_picker.py:174` | `def _collect_string_constants(source)` |
| `run` | method | `tests/test_fuzzy_picker.py:43` | `def run(self, items, initial_query)` |
| `sample_items` | method | `tests/test_fuzzy_picker.py:59` | `def sample_items()` |
| `scorer` | method | `tests/test_fuzzy_picker.py:54` | `def scorer()` |
| `test_config_from_payload_ignores_unknown_keys` | method | `tests/test_fuzzy_picker.py:119` | `def test_config_from_payload_ignores_unknown_keys()` |
| `test_config_from_payload_respects_known_overrides` | method | `tests/test_fuzzy_picker.py:112` | `def test_config_from_payload_respects_known_overrides()` |
| `test_config_from_payload_returns_defaults_when_no_block` | method | `tests/test_fuzzy_picker.py:124` | `def test_config_from_payload_returns_defaults_when_no_block()` |
| `test_empty_query_returns_all_items_in_order` | method | `tests/test_fuzzy_picker.py:72` | `def test_empty_query_returns_all_items_in_order(scorer, sample_items)` |
| `test_exact_match_scores_highest` | method | `tests/test_fuzzy_picker.py:78` | `def test_exact_match_scores_highest(scorer, sample_items)` |
| `test_getprompt_renders_three_lines_and_includes_payload_segments` | method | `tests/test_fuzzy_picker.py:283` | `def test_getprompt_renders_three_lines_and_includes_payload_segments()` |
| `test_lazyown_runtime_strings_preserve_shell_payload` | method | `tests/test_fuzzy_picker.py:260` | `def test_lazyown_runtime_strings_preserve_shell_payload(expected_substring)` |
| `test_lazyown_source_has_no_invalid_escape_warning` | method | `tests/test_fuzzy_picker.py:268` | `def test_lazyown_source_has_no_invalid_escape_warning()` |
| `test_picker_cancel_returns_none` | method | `tests/test_fuzzy_picker.py:146` | `def test_picker_cancel_returns_none(sample_items)` |
| `test_picker_empty_input_returns_none` | method | `tests/test_fuzzy_picker.py:152` | `def test_picker_empty_input_returns_none()` |
| `test_picker_routes_through_view_for_multiple_items` | method | `tests/test_fuzzy_picker.py:138` | `def test_picker_routes_through_view_for_multiple_items(sample_items)` |
| `test_picker_short_circuits_single_item` | method | `tests/test_fuzzy_picker.py:132` | `def test_picker_short_circuits_single_item()` |
| `test_prefix_match_outranks_substring` | method | `tests/test_fuzzy_picker.py:84` | `def test_prefix_match_outranks_substring(scorer)` |
| `test_similarity_floor_excludes_unrelated_text` | method | `tests/test_fuzzy_picker.py:98` | `def test_similarity_floor_excludes_unrelated_text(scorer)` |
| `test_strip_ansi_passes_through_plain_text` | method | `tests/test_fuzzy_picker.py:165` | `def test_strip_ansi_passes_through_plain_text()` |
| `test_strip_ansi_removes_csi_sequences` | method | `tests/test_fuzzy_picker.py:160` | `def test_strip_ansi_removes_csi_sequences()` |
| `test_subsequence_match_emits_positions` | method | `tests/test_fuzzy_picker.py:90` | `def test_subsequence_match_emits_positions(scorer, sample_items)` |
| `test_subsequence_positions_helper_returns_empty_when_no_match` | method | `tests/test_fuzzy_picker.py:104` | `def test_subsequence_positions_helper_returns_empty_when_no_match()` |
| `advisor` | function | `tests/test_graph_advisor.py:63` | `def advisor(small_graph_path)` |
| `small_graph_data` | function | `tests/test_graph_advisor.py:34` | `def small_graph_data()` |
| `small_graph_path` | function | `tests/test_graph_advisor.py:56` | `def small_graph_path(tmp_path, small_graph_data)` |
| `test_advisor_did_you_mean_returns_close_labels` | function | `tests/test_graph_advisor.py:192` | `def test_advisor_did_you_mean_returns_close_labels(advisor)` |
| `test_advisor_god_nodes_ranks_by_degree` | function | `tests/test_graph_advisor.py:178` | `def test_advisor_god_nodes_ranks_by_degree(advisor)` |
| `test_advisor_handles_missing_graph_gracefully` | function | `tests/test_graph_advisor.py:204` | `def test_advisor_handles_missing_graph_gracefully(tmp_path)` |
| `test_advisor_neighbors_respects_depth` | function | `tests/test_graph_advisor.py:172` | `def test_advisor_neighbors_respects_depth(advisor)` |
| `test_advisor_neighbors_returns_layered_walk` | function | `tests/test_graph_advisor.py:163` | `def test_advisor_neighbors_returns_layered_walk(advisor)` |
| `test_advisor_reads_recent_commands_from_csv` | function | `tests/test_graph_advisor.py:216` | `def test_advisor_reads_recent_commands_from_csv(tmp_path, advisor)` |
| `test_advisor_search_returns_ranked_nodes` | function | `tests/test_graph_advisor.py:155` | `def test_advisor_search_returns_ranked_nodes(advisor)` |
| `test_advisor_suggest_next_walks_from_recent` | function | `tests/test_graph_advisor.py:184` | `def test_advisor_suggest_next_walks_from_recent(advisor)` |
| `test_advisor_summary_flags_empty_graph` | function | `tests/test_graph_advisor.py:123` | `def test_advisor_summary_flags_empty_graph(tmp_path)` |
| `test_advisor_summary_flags_stale_graph` | function | `tests/test_graph_advisor.py:136` | `def test_advisor_summary_flags_stale_graph(tmp_path)` |
| `test_advisor_summary_reports_topology` | function | `tests/test_graph_advisor.py:112` | `def test_advisor_summary_reports_topology(advisor)` |
| `test_advisor_truncate_respects_token_budget` | function | `tests/test_graph_advisor.py:198` | `def test_advisor_truncate_respects_token_budget(advisor)` |
| `test_format_god_nodes_handles_empty` | function | `tests/test_graph_advisor.py:248` | `def test_format_god_nodes_handles_empty()` |
| `test_format_neighbors_renders_when_match_found` | function | `tests/test_graph_advisor.py:242` | `def test_format_neighbors_renders_when_match_found(advisor)` |
| `test_format_search_table_renders_rows` | function | `tests/test_graph_advisor.py:235` | `def test_format_search_table_renders_rows(advisor)` |
| `test_format_suggestions_handles_empty` | function | `tests/test_graph_advisor.py:252` | `def test_format_suggestions_handles_empty()` |
| `test_index_builds_adjacency_and_degree` | function | `tests/test_graph_advisor.py:83` | `def test_index_builds_adjacency_and_degree(small_graph_data)` |
| `test_loader_resolves_explicit_path` | function | `tests/test_graph_advisor.py:68` | `def test_loader_resolves_explicit_path(tmp_path, small_graph_data)` |
| `test_loader_returns_none_when_missing` | function | `tests/test_graph_advisor.py:77` | `def test_loader_returns_none_when_missing(tmp_path)` |
| `test_real_graph_summary_when_available` | function | `tests/test_graph_advisor.py:259` | `def test_real_graph_summary_when_available()` |
| `test_scorer_prefers_prefix_match` | function | `tests/test_graph_advisor.py:98` | `def test_scorer_prefers_prefix_match(small_graph_data)` |
| `test_scorer_returns_empty_for_unrelated_query` | function | `tests/test_graph_advisor.py:106` | `def test_scorer_returns_empty_for_unrelated_query(small_graph_data)` |
| `_FakeAdvisor` | class | `tests/test_graph_overlay.py:25` | `class _FakeAdvisor` |
| `__init__` | method | `tests/test_graph_overlay.py:26` | `def __init__(self, available)` |
| `god_nodes` | method | `tests/test_graph_overlay.py:32` | `def god_nodes(self, limit)` |
| `is_available` | method | `tests/test_graph_overlay.py:29` | `def is_available(self)` |
| `neighbors` | method | `tests/test_graph_overlay.py:39` | `def neighbors(self, query, depth, limit)` |
| `runner` | method | `tests/test_graph_overlay.py:129` | `def runner(context)` |
| `test_build_state_uses_default_factory_signature` | method | `tests/test_graph_overlay.py:135` | `def test_build_state_uses_default_factory_signature()` |
| `test_focus_switches_to_neighbors_view` | method | `tests/test_graph_overlay.py:72` | `def test_focus_switches_to_neighbors_view()` |
| `test_focus_unknown_returns_no_match_message` | method | `tests/test_graph_overlay.py:85` | `def test_focus_unknown_returns_no_match_message()` |
| `test_god_nodes_view_returns_hubs` | method | `tests/test_graph_overlay.py:61` | `def test_god_nodes_view_returns_hubs()` |
| `test_is_available_returns_false_when_advisor_missing` | method | `tests/test_graph_overlay.py:55` | `def test_is_available_returns_false_when_advisor_missing()` |
| `test_launch_overlay_uses_runner` | method | `tests/test_graph_overlay.py:122` | `def test_launch_overlay_uses_runner()` |
| `test_toggle_view_round_trip` | method | `tests/test_graph_overlay.py:108` | `def test_toggle_view_round_trip()` |
| `test_unavailable_advisor_returns_no_graph_message` | method | `tests/test_graph_overlay.py:97` | `def test_unavailable_advisor_returns_no_graph_message()` |
| `SafeHtmlHelperTests` | class | `tests/test_gui_xss_sinks.py:26` | `class SafeHtmlHelperTests(TestCase)` |
| `SinkSanitizationTests` | class | `tests/test_gui_xss_sinks.py:37` | `class SinkSanitizationTests(TestCase)` |
| `_read_template` | function | `tests/test_gui_xss_sinks.py:21` | `def _read_template()` |
| `test_helper_is_defined_exactly_once` | method | `tests/test_gui_xss_sinks.py:27` | `def test_helper_is_defined_exactly_once(self)` |
| `test_helper_prefers_dompurify_with_text_fallback` | method | `tests/test_gui_xss_sinks.py:31` | `def test_helper_prefers_dompurify_with_text_fallback(self)` |
| `test_no_raw_error_interpolation` | method | `tests/test_gui_xss_sinks.py:50` | `def test_no_raw_error_interpolation(self)` |
| `test_no_raw_html_interpolation` | method | `tests/test_gui_xss_sinks.py:43` | `def test_no_raw_html_interpolation(self)` |
| `test_no_raw_output_interpolation` | method | `tests/test_gui_xss_sinks.py:61` | `def test_no_raw_output_interpolation(self)` |
| `test_no_raw_response_interpolation` | method | `tests/test_gui_xss_sinks.py:38` | `def test_no_raw_response_interpolation(self)` |
| `TestCrackResult` | class | `tests/test_hash_cracker.py:91` | `class TestCrackResult` |
| `TestFileIdentification` | class | `tests/test_hash_cracker.py:66` | `class TestFileIdentification` |
| `TestHashIdentification` | class | `tests/test_hash_cracker.py:14` | `class TestHashIdentification` |
| `TestHashIdentifier` | class | `tests/test_hash_cracker.py:129` | `class TestHashIdentifier` |
| `TestHashPatterns` | class | `tests/test_hash_cracker.py:114` | `class TestHashPatterns` |
| `TestWordlists` | class | `tests/test_hash_cracker.py:122` | `class TestWordlists` |
| `test_all_patterns_exist` | method | `tests/test_hash_cracker.py:115` | `def test_all_patterns_exist(self)` |
| `test_crack_result_cracked` | method | `tests/test_hash_cracker.py:102` | `def test_crack_result_cracked(self)` |
| `test_crack_result_defaults` | method | `tests/test_hash_cracker.py:92` | `def test_crack_result_defaults(self)` |
| `test_hash_identifier_fields` | method | `tests/test_hash_cracker.py:130` | `def test_hash_identifier_fields(self)` |
| `test_identify_empty` | method | `tests/test_hash_cracker.py:41` | `def test_identify_empty(self)` |
| `test_identify_file_empty` | method | `tests/test_hash_cracker.py:67` | `def test_identify_file_empty(self, tmp_path)` |
| `test_identify_file_not_exists` | method | `tests/test_hash_cracker.py:85` | `def test_identify_file_not_exists(self)` |
| `test_identify_file_with_hashes` | method | `tests/test_hash_cracker.py:74` | `def test_identify_file_with_hashes(self, tmp_path)` |
| `test_identify_kerberos_tgs` | method | `tests/test_hash_cracker.py:46` | `def test_identify_kerberos_tgs(self)` |
| `test_identify_md5` | method | `tests/test_hash_cracker.py:53` | `def test_identify_md5(self)` |
| `test_identify_ntlm` | method | `tests/test_hash_cracker.py:15` | `def test_identify_ntlm(self)` |
| `test_identify_ntlm_from_secretsdump` | method | `tests/test_hash_cracker.py:22` | `def test_identify_ntlm_from_secretsdump(self)` |
| `test_identify_sha1` | method | `tests/test_hash_cracker.py:59` | `def test_identify_sha1(self)` |
| `test_identify_sha512crypt` | method | `tests/test_hash_cracker.py:29` | `def test_identify_sha512crypt(self)` |
| `test_identify_unknown` | method | `tests/test_hash_cracker.py:36` | `def test_identify_unknown(self)` |
| `test_wordlist_paths_are_strings` | method | `tests/test_hash_cracker.py:123` | `def test_wordlist_paths_are_strings(self)` |
| `HelpUiSuiteConfig` | class | `tests/test_help_ui_command_set.py:38` | `class HelpUiSuiteConfig` |
| `_add_repo_root_to_syspath` | function | `tests/test_help_ui_command_set.py:32` | `def _add_repo_root_to_syspath()` |
| `_methods_of` | method | `tests/test_help_ui_command_set.py:65` | `def _methods_of(path, class_name)` |
| `test_no_command_collisions_with_source` | method | `tests/test_help_ui_command_set.py:112` | `def test_no_command_collisions_with_source()` |
| `test_registry_registers_target` | method | `tests/test_help_ui_command_set.py:105` | `def test_registry_registers_target()` |
| `test_source_no_longer_defines_cluster` | method | `tests/test_help_ui_command_set.py:99` | `def test_source_no_longer_defines_cluster()` |
| `test_target_exposes_full_help_cluster` | method | `tests/test_help_ui_command_set.py:86` | `def test_target_exposes_full_help_cluster()` |
| `test_target_is_active_command_set` | method | `tests/test_help_ui_command_set.py:77` | `def test_target_is_active_command_set()` |
| `test_target_phase_metadata` | method | `tests/test_help_ui_command_set.py:93` | `def test_target_phase_metadata()` |
| `TestBenignTagsPreserved` | class | `tests/test_html_sanitizer.py:71` | `class TestBenignTagsPreserved` |
| `TestCustomAllowlist` | class | `tests/test_html_sanitizer.py:93` | `class TestCustomAllowlist` |
| `TestEventHandlerStripping` | class | `tests/test_html_sanitizer.py:49` | `class TestEventHandlerStripping` |
| `TestJavascriptUriStripping` | class | `tests/test_html_sanitizer.py:63` | `class TestJavascriptUriStripping` |
| `TestScriptStripping` | class | `tests/test_html_sanitizer.py:25` | `class TestScriptStripping` |
| `test_basic_formatting_preserved` | method | `tests/test_html_sanitizer.py:74` | `def test_basic_formatting_preserved(self)` |
| `test_headings_preserved` | method | `tests/test_html_sanitizer.py:86` | `def test_headings_preserved(self)` |
| `test_iframe_removed` | method | `tests/test_html_sanitizer.py:33` | `def test_iframe_removed(self)` |
| `test_javascript_href_stripped` | method | `tests/test_html_sanitizer.py:66` | `def test_javascript_href_stripped(self)` |
| `test_lists_preserved` | method | `tests/test_html_sanitizer.py:81` | `def test_lists_preserved(self)` |
| `test_object_and_embed_removed` | method | `tests/test_html_sanitizer.py:38` | `def test_object_and_embed_removed(self)` |
| `test_onclick_removed` | method | `tests/test_html_sanitizer.py:52` | `def test_onclick_removed(self)` |
| `test_onerror_removed` | method | `tests/test_html_sanitizer.py:57` | `def test_onerror_removed(self)` |
| `test_script_block_removed` | method | `tests/test_html_sanitizer.py:28` | `def test_script_block_removed(self)` |
| `test_strict_allowlist_strips_more` | method | `tests/test_html_sanitizer.py:96` | `def test_strict_allowlist_strips_more(self)` |
| `test_style_removed` | method | `tests/test_html_sanitizer.py:43` | `def test_style_removed(self)` |
| `TestHTTPSRedirect` | class | `tests/test_https_redirect.py:34` | `class TestHTTPSRedirect` |
| `TestRedirectResponseShape` | class | `tests/test_https_redirect.py:74` | `class TestRedirectResponseShape` |
| `_FakeRequest` | class | `tests/test_https_redirect.py:23` | `class _FakeRequest` |
| `__init__` | method | `tests/test_https_redirect.py:24` | `def __init__(self, is_secure, host, path, query_string)` |
| `test_insecure_in_dev_passes_through` | method | `tests/test_https_redirect.py:50` | `def test_insecure_in_dev_passes_through(self)` |
| `test_insecure_in_prod_redirects_to_https` | method | `tests/test_https_redirect.py:42` | `def test_insecure_in_prod_redirects_to_https(self)` |
| `test_insecure_when_disabled_passes_through` | method | `tests/test_https_redirect.py:55` | `def test_insecure_when_disabled_passes_through(self)` |
| `test_query_string_preserved` | method | `tests/test_https_redirect.py:60` | `def test_query_string_preserved(self)` |
| `test_response_is_named_tuple_like` | method | `tests/test_https_redirect.py:77` | `def test_response_is_named_tuple_like(self)` |
| `test_root_path_preserved` | method | `tests/test_https_redirect.py:67` | `def test_root_path_preserved(self)` |
| `test_secure_request_passes_through` | method | `tests/test_https_redirect.py:37` | `def test_secure_request_passes_through(self)` |
| `BackendAdapterSpec` | class | `tests/test_improvements_spec.py:550` | `class BackendAdapterSpec(TestCase)` |
| `BackendRegistrySpec` | class | `tests/test_improvements_spec.py:444` | `class BackendRegistrySpec(TestCase)` |
| `CmdIntegrationRegressionSpec` | class | `tests/test_improvements_spec.py:767` | `class CmdIntegrationRegressionSpec(TestCase)` |
| `CommandSetActivationSpec` | class | `tests/test_improvements_spec.py:673` | `class CommandSetActivationSpec(TestCase)` |
| `ConfigDedupeSpec` | class | `tests/test_improvements_spec.py:649` | `class ConfigDedupeSpec(TestCase)` |
| `DocstringDisciplineSpec` | class | `tests/test_improvements_spec.py:706` | `class DocstringDisciplineSpec(TestCase)` |
| `EventBusSpec` | class | `tests/test_improvements_spec.py:518` | `class EventBusSpec(TestCase)` |
| `FactoryWiringSpec` | class | `tests/test_improvements_spec.py:996` | `class FactoryWiringSpec(TestCase)` |
| `GraphifyAvailabilitySpec` | class | `tests/test_improvements_spec.py:745` | `class GraphifyAvailabilitySpec(TestCase)` |
| `LiveShellBehaviourSpec` | class | `tests/test_improvements_spec.py:844` | `class LiveShellBehaviourSpec(TestCase)` |
| `OrchestratorGoalValidationSpec` | class | `tests/test_improvements_spec.py:404` | `class OrchestratorGoalValidationSpec(TestCase)` |
| `RouterPolicySpec` | class | `tests/test_improvements_spec.py:477` | `class RouterPolicySpec(TestCase)` |
| `StatusBarConfigSpec` | class | `tests/test_improvements_spec.py:183` | `class StatusBarConfigSpec(TestCase)` |
| `StatusBarFactorySpec` | class | `tests/test_improvements_spec.py:395` | `class StatusBarFactorySpec(TestCase)` |
| `StatusBarManagerSpec` | class | `tests/test_improvements_spec.py:278` | `class StatusBarManagerSpec(TestCase)` |
| `StatusBarRendererSpec` | class | `tests/test_improvements_spec.py:239` | `class StatusBarRendererSpec(TestCase)` |
| `StatusBarSecuritySpec` | class | `tests/test_improvements_spec.py:205` | `class StatusBarSecuritySpec(TestCase)` |
| `StatusBarSourceSpec` | class | `tests/test_improvements_spec.py:350` | `class StatusBarSourceSpec(TestCase)` |
| `UnifiedOrchestratorSpec` | class | `tests/test_improvements_spec.py:601` | `class UnifiedOrchestratorSpec(TestCase)` |
| `_Boom` | class | `tests/test_improvements_spec.py:591` | `class _Boom` |
| `_Broken` | class | `tests/test_improvements_spec.py:289` | `class _Broken` |
| `_Broken` | class | `tests/test_improvements_spec.py:387` | `class _Broken` |
| `_Engine` | class | `tests/test_improvements_spec.py:934` | `class _Engine` |
| `_FakeAdvisor` | class | `tests/test_improvements_spec.py:134` | `class _FakeAdvisor` |
| `_FakeEngagement` | class | `tests/test_improvements_spec.py:90` | `class _FakeEngagement` |
| `_FakeQueen` | class | `tests/test_improvements_spec.py:98` | `class _FakeQueen` |
| `_FakeShell` | class | `tests/test_improvements_spec.py:77` | `class _FakeShell` |
| `_FakeSwanOrchestrator` | class | `tests/test_improvements_spec.py:126` | `class _FakeSwanOrchestrator` |
| `_FakeSwanResult` | class | `tests/test_improvements_spec.py:117` | `class _FakeSwanResult` |
| `_Shell` | class | `tests/test_improvements_spec.py:786` | `class _Shell(Cmd)` |
| `_Shell` | class | `tests/test_improvements_spec.py:798` | `class _Shell(Cmd)` |
| `_Shell` | class | `tests/test_improvements_spec.py:823` | `class _Shell(Cmd)` |
| `_Static` | class | `tests/test_improvements_spec.py:308` | `class _Static` |
| `_Static` | class | `tests/test_improvements_spec.py:329` | `class _Static` |
| `_UnavailableBackend` | class | `tests/test_improvements_spec.py:172` | `class _UnavailableBackend` |
| `_Unnamed` | class | `tests/test_improvements_spec.py:453` | `class _Unnamed` |
| `__init__` | method | `tests/test_improvements_spec.py:80` | `def __init__(self, custom_prompt)` |
| `__init__` | method | `tests/test_improvements_spec.py:91` | `def __init__(self, payload)` |
| `__init__` | method | `tests/test_improvements_spec.py:99` | `def __init__(self, drones, summary)` |
| `__init__` | method | `tests/test_improvements_spec.py:118` | `def __init__(self, text, expert_id)` |
| `__init__` | method | `tests/test_improvements_spec.py:127` | `def __init__(self, result)` |
| `__init__` | method | `tests/test_improvements_spec.py:135` | `def __init__(self, suggestions)` |
| `__init__` | method | `tests/test_improvements_spec.py:173` | `def __init__(self, name)` |
| `__init__` | method | `tests/test_improvements_spec.py:309` | `def __init__(self, value)` |
| `__init__` | method | `tests/test_improvements_spec.py:330` | `def __init__(self, value)` |
| `_build_test_orchestrator` | method | `tests/test_improvements_spec.py:142` | `def _build_test_orchestrator(tmp_root, daemon_available, hive_available, swan_available, daemon_payload)` |
| `_discover` | method | `tests/test_improvements_spec.py:683` | `def _discover(self)` |
| `_events` | method | `tests/test_improvements_spec.py:611` | `def _events(self)` |
| `_goal` | method | `tests/test_improvements_spec.py:561` | `def _goal(self)` |
| `_make_engine` | method | `tests/test_improvements_spec.py:154` | `def _make_engine(goal)` |
| `_reader` | method | `tests/test_improvements_spec.py:216` | `def _reader(self)` |
| `available` | method | `tests/test_improvements_spec.py:176` | `def available(self)` |
| `available` | method | `tests/test_improvements_spec.py:456` | `def available(self)` |
| `broken` | method | `tests/test_improvements_spec.py:899` | `def broken()` |
| `collect` | method | `tests/test_improvements_spec.py:110` | `def collect(self, ids)` |
| `collect` | method | `tests/test_improvements_spec.py:290` | `def collect(self)` |
| `collect` | method | `tests/test_improvements_spec.py:312` | `def collect(self)` |
| `collect` | method | `tests/test_improvements_spec.py:333` | `def collect(self)` |
| `contains_emoji` | method | `tests/test_improvements_spec.py:730` | `def contains_emoji(text)` |
| `dispatch` | method | `tests/test_improvements_spec.py:107` | `def dispatch(self, tasks)` |
| `factory` | method | `tests/test_improvements_spec.py:931` | `def factory(goal)` |
| `fake_hints` | method | `tests/test_improvements_spec.py:878` | `def fake_hints(last_cmd, phase, sessions_dir, limit)` |
| `plan` | method | `tests/test_improvements_spec.py:103` | `def plan(self, goal, n_drones)` |
| `register_precmd_hook` | method | `tests/test_improvements_spec.py:86` | `def register_precmd_hook(self, hook)` |
| `run` | method | `tests/test_improvements_spec.py:94` | `def run(self)` |
| `run` | method | `tests/test_improvements_spec.py:130` | `def run(self, task_type, goal, engagement_phase, timeout)` |
| `run` | method | `tests/test_improvements_spec.py:179` | `def run(self, goal)` |
| `run` | method | `tests/test_improvements_spec.py:459` | `def run(self, goal)` |
| `run` | method | `tests/test_improvements_spec.py:592` | `def run(self)` |
| `run` | method | `tests/test_improvements_spec.py:935` | `def run(self_inner)` |
| `setUp` | method | `tests/test_improvements_spec.py:208` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:242` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:353` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:407` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:480` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:521` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:553` | `def setUp(self)` |
| `setUp` | method | `tests/test_improvements_spec.py:604` | `def setUp(self)` |
| `suggest_next` | method | `tests/test_improvements_spec.py:138` | `def suggest_next(self, recent_commands, limit)` |
| `suggest_next` | method | `tests/test_improvements_spec.py:388` | `def suggest_next(self)` |
| `synthesize` | method | `tests/test_improvements_spec.py:113` | `def synthesize(self, results)` |
| `tearDown` | method | `tests/test_improvements_spec.py:213` | `def tearDown(self)` |
| `tearDown` | method | `tests/test_improvements_spec.py:359` | `def tearDown(self)` |
| `tearDown` | method | `tests/test_improvements_spec.py:527` | `def tearDown(self)` |
| `tearDown` | method | `tests/test_improvements_spec.py:558` | `def tearDown(self)` |
| `tearDown` | method | `tests/test_improvements_spec.py:608` | `def tearDown(self)` |
| `test_auto_picks_daemon_when_target_present` | method | `tests/test_improvements_spec.py:496` | `def test_auto_picks_daemon_when_target_present(self)` |
| `test_auto_picks_hive_on_swarm_keyword` | method | `tests/test_improvements_spec.py:500` | `def test_auto_picks_hive_on_swarm_keyword(self)` |
| `test_auto_picks_swan_on_exploit_keyword` | method | `tests/test_improvements_spec.py:504` | `def test_auto_picks_swan_on_exploit_keyword(self)` |
| `test_auto_routes_with_target_to_daemon` | method | `tests/test_improvements_spec.py:628` | `def test_auto_routes_with_target_to_daemon(self)` |
| `test_backend_returns_error_when_engine_raises` | method | `tests/test_improvements_spec.py:590` | `def test_backend_returns_error_when_engine_raises(self)` |
| `test_build_default_manager_does_not_touch_filesystem` | method | `tests/test_improvements_spec.py:1003` | `def test_build_default_manager_does_not_touch_filesystem(self)` |
| `test_build_default_orchestrator_registers_three_backends` | method | `tests/test_improvements_spec.py:999` | `def test_build_default_orchestrator_registers_three_backends(self)` |
| `test_collect_context_uses_fallbacks_on_failure` | method | `tests/test_improvements_spec.py:286` | `def test_collect_context_uses_fallbacks_on_failure(self)` |
| `test_command_hint_source_falls_back_when_provider_raises` | method | `tests/test_improvements_spec.py:892` | `def test_command_hint_source_falls_back_when_provider_raises(self)` |
| `test_command_hint_source_returns_kill_chain_verb` | method | `tests/test_improvements_spec.py:866` | `def test_command_hint_source_returns_kill_chain_verb(self)` |
| `test_command_hints_helper_returns_phase_priority_verbs` | method | `tests/test_improvements_spec.py:913` | `def test_command_hints_helper_returns_phase_priority_verbs(self)` |
| `test_command_set_resolves_shell_via_cmd_property` | method | `tests/test_improvements_spec.py:781` | `def test_command_set_resolves_shell_via_cmd_property(self)` |
| `test_config_ignores_invalid_overrides` | method | `tests/test_improvements_spec.py:200` | `def test_config_ignores_invalid_overrides(self)` |
| `test_config_is_immutable_dataclass` | method | `tests/test_improvements_spec.py:190` | `def test_config_is_immutable_dataclass(self)` |
| `test_config_overrides_from_payload` | method | `tests/test_improvements_spec.py:196` | `def test_config_overrides_from_payload(self)` |
| `test_core_config_is_canonical` | method | `tests/test_improvements_spec.py:664` | `def test_core_config_is_canonical(self)` |
| `test_daemon_falls_back_to_payload_rhost` | method | `tests/test_improvements_spec.py:921` | `def test_daemon_falls_back_to_payload_rhost(self)` |
| `test_daemon_normalises_dict_result` | method | `tests/test_improvements_spec.py:570` | `def test_daemon_normalises_dict_result(self)` |
| `test_daemon_requires_target` | method | `tests/test_improvements_spec.py:565` | `def test_daemon_requires_target(self)` |
| `test_default_prompt_join_is_newline` | method | `tests/test_improvements_spec.py:861` | `def test_default_prompt_join_is_newline(self)` |
| `test_defaults_are_applied` | method | `tests/test_improvements_spec.py:424` | `def test_defaults_are_applied(self)` |
| `test_duplicate_name_raises` | method | `tests/test_improvements_spec.py:447` | `def test_duplicate_name_raises(self)` |
| `test_emit_appends_jsonline` | method | `tests/test_improvements_spec.py:530` | `def test_emit_appends_jsonline(self)` |
| `test_emit_rejects_non_serialisable` | method | `tests/test_improvements_spec.py:541` | `def test_emit_rejects_non_serialisable(self)` |
| `test_emit_rejects_oversize_event` | method | `tests/test_improvements_spec.py:537` | `def test_emit_rejects_oversize_event(self)` |
| `test_empty_goal_is_rejected` | method | `tests/test_improvements_spec.py:411` | `def test_empty_goal_is_rejected(self)` |
| `test_empty_name_raises` | method | `tests/test_improvements_spec.py:452` | `def test_empty_name_raises(self)` |
| `test_enabled_flag_accepts_strings_and_bools` | method | `tests/test_improvements_spec.py:304` | `def test_enabled_flag_accepts_strings_and_bools(self)` |
| `test_event_is_emitted_per_execution` | method | `tests/test_improvements_spec.py:634` | `def test_event_is_emitted_per_execution(self)` |
| `test_every_class_in_new_modules_has_docstring` | method | `tests/test_improvements_spec.py:709` | `def test_every_class_in_new_modules_has_docstring(self)` |
| `test_explicit_mode_overrides_router` | method | `tests/test_improvements_spec.py:492` | `def test_explicit_mode_overrides_router(self)` |
| `test_factory_returns_manager_with_four_sources` | method | `tests/test_improvements_spec.py:398` | `def test_factory_returns_manager_with_four_sources(self)` |
| `test_file_permissions_are_restrictive` | method | `tests/test_improvements_spec.py:544` | `def test_file_permissions_are_restrictive(self)` |
| `test_finding_prefers_credentials_over_notes` | method | `tests/test_improvements_spec.py:375` | `def test_finding_prefers_credentials_over_notes(self)` |
| `test_graph_file_is_valid_json_when_present` | method | `tests/test_improvements_spec.py:758` | `def test_graph_file_is_valid_json_when_present(self)` |
| `test_hive_runs_full_lifecycle` | method | `tests/test_improvements_spec.py:577` | `def test_hive_runs_full_lifecycle(self)` |
| `test_install_registers_precmd_hook` | method | `tests/test_improvements_spec.py:325` | `def test_install_registers_precmd_hook(self)` |
| `test_long_goal_is_bounded` | method | `tests/test_improvements_spec.py:419` | `def test_long_goal_is_bounded(self)` |
| `test_metadata_carries_request_id` | method | `tests/test_improvements_spec.py:438` | `def test_metadata_carries_request_id(self)` |
| `test_missing_source_key_raises` | method | `tests/test_improvements_spec.py:281` | `def test_missing_source_key_raises(self)` |
| `test_modules_avoid_emoji_in_source` | method | `tests/test_improvements_spec.py:724` | `def test_modules_avoid_emoji_in_source(self)` |
| `test_numeric_fields_stay_zero_when_unset` | method | `tests/test_improvements_spec.py:433` | `def test_numeric_fields_stay_zero_when_unset(self)` |
| `test_orchestration_commandset_finds_managers_on_bound_shell` | method | `tests/test_improvements_spec.py:818` | `def test_orchestration_commandset_finds_managers_on_bound_shell(self)` |
| `test_orchestration_set_exposes_required_verbs` | method | `tests/test_improvements_spec.py:697` | `def test_orchestration_set_exposes_required_verbs(self)` |
| `test_orchestration_set_is_active` | method | `tests/test_improvements_spec.py:691` | `def test_orchestration_set_is_active(self)` |
| `test_orchestration_set_phase_and_category_set` | method | `tests/test_improvements_spec.py:701` | `def test_orchestration_set_phase_and_category_set(self)` |
| `test_order_is_preserved` | method | `tests/test_improvements_spec.py:465` | `def test_order_is_preserved(self)` |
| `test_payload_target_falls_back_to_default` | method | `tests/test_improvements_spec.py:366` | `def test_payload_target_falls_back_to_default(self)` |
| `test_payload_target_picks_first_non_empty_key` | method | `tests/test_improvements_spec.py:362` | `def test_payload_target_picks_first_non_empty_key(self)` |
| `test_phase_prefers_world_model_over_payload` | method | `tests/test_improvements_spec.py:370` | `def test_phase_prefers_world_model_over_payload(self)` |
| `test_reader_bounds_file_size` | method | `tests/test_improvements_spec.py:225` | `def test_reader_bounds_file_size(self)` |
| `test_reader_invalid_json_returns_none` | method | `tests/test_improvements_spec.py:234` | `def test_reader_invalid_json_returns_none(self)` |
| `test_reader_rejects_absolute_paths` | method | `tests/test_improvements_spec.py:222` | `def test_reader_rejects_absolute_paths(self)` |
| `test_reader_rejects_parent_traversal` | method | `tests/test_improvements_spec.py:219` | `def test_reader_rejects_parent_traversal(self)` |
| `test_reader_returns_empty_on_missing_file` | method | `tests/test_improvements_spec.py:231` | `def test_reader_returns_empty_on_missing_file(self)` |
| `test_render_plain_contains_all_fields` | method | `tests/test_improvements_spec.py:246` | `def test_render_plain_contains_all_fields(self)` |
| `test_render_prompt_defaults_to_raw_ansi_for_prompt_toolkit` | method | `tests/test_improvements_spec.py:263` | `def test_render_prompt_defaults_to_raw_ansi_for_prompt_toolkit(self)` |
| `test_render_prompt_opt_in_readline_mode_wraps_ansi_with_markers` | method | `tests/test_improvements_spec.py:270` | `def test_render_prompt_opt_in_readline_mode_wraps_ansi_with_markers(self)` |
| `test_render_strips_dangerous_substrings` | method | `tests/test_improvements_spec.py:258` | `def test_render_strips_dangerous_substrings(self)` |
| `test_render_truncates_to_max_chars` | method | `tests/test_improvements_spec.py:252` | `def test_render_truncates_to_max_chars(self)` |
| `test_result_to_dict_is_json_serialisable` | method | `tests/test_improvements_spec.py:642` | `def test_result_to_dict_is_json_serialisable(self)` |
| `test_router_ignores_unset_task_type_for_keyword_scoring` | method | `tests/test_improvements_spec.py:970` | `def test_router_ignores_unset_task_type_for_keyword_scoring(self)` |
| `test_router_picks_daemon_when_only_payload_supplies_target` | method | `tests/test_improvements_spec.py:946` | `def test_router_picks_daemon_when_only_payload_supplies_target(self)` |
| `test_status_bar_install_registers_precmd_hook_on_real_cmd2` | method | `tests/test_improvements_spec.py:795` | `def test_status_bar_install_registers_precmd_hook_on_real_cmd2(self)` |
| `test_suggestion_fallback_when_factory_none` | method | `tests/test_improvements_spec.py:752` | `def test_suggestion_fallback_when_factory_none(self)` |
| `test_suggestion_falls_back_when_advisor_raises` | method | `tests/test_improvements_spec.py:386` | `def test_suggestion_falls_back_when_advisor_raises(self)` |
| `test_suggestion_uses_advisor_when_available` | method | `tests/test_improvements_spec.py:381` | `def test_suggestion_uses_advisor_when_available(self)` |
| `test_swan_normalises_result_object` | method | `tests/test_improvements_spec.py:584` | `def test_swan_normalises_result_object(self)` |
| `test_task_type_stays_empty_when_unset` | method | `tests/test_improvements_spec.py:429` | `def test_task_type_stays_empty_when_unset(self)` |
| `test_unavailable_backend_returns_unavailable_result` | method | `tests/test_improvements_spec.py:623` | `def test_unavailable_backend_returns_unavailable_result(self)` |
| `test_unavailable_explicit_mode_returns_none` | method | `tests/test_improvements_spec.py:508` | `def test_unavailable_explicit_mode_returns_none(self)` |
| `test_unknown_mode_is_rejected` | method | `tests/test_improvements_spec.py:415` | `def test_unknown_mode_is_rejected(self)` |
| `test_utils_has_no_class_config` | method | `tests/test_improvements_spec.py:658` | `def test_utils_has_no_class_config(self)` |
| `test_validation_error_returns_invalid_result` | method | `tests/test_improvements_spec.py:617` | `def test_validation_error_returns_invalid_result(self)` |
| `test_c2_compose_terminates_tls` | function | `tests/test_infra_disposable.py:111` | `def test_c2_compose_terminates_tls()` |
| `test_compile_commands_route_through_shell` | function | `tests/test_infra_disposable.py:228` | `def test_compile_commands_route_through_shell()` |
| `test_compose_down_missing_file` | function | `tests/test_infra_disposable.py:373` | `def test_compose_down_missing_file()` |
| `test_find_cloudflared_pids` | function | `tests/test_infra_disposable.py:357` | `def test_find_cloudflared_pids()` |
| `test_format_timeline_event_summarizes_payload` | function | `tests/test_infra_disposable.py:279` | `def test_format_timeline_event_summarizes_payload()` |
| `test_garble_mismatch_detected` | function | `tests/test_infra_disposable.py:258` | `def test_garble_mismatch_detected()` |
| `test_go_string_list_formats_slice` | function | `tests/test_infra_disposable.py:60` | `def test_go_string_list_formats_slice()` |
| `test_gym_range_challenges_registered` | function | `tests/test_infra_disposable.py:161` | `def test_gym_range_challenges_registered()` |
| `test_gym_range_next_steps` | function | `tests/test_infra_disposable.py:342` | `def test_gym_range_next_steps()` |
| `test_implant_template_has_fallback_helpers` | function | `tests/test_infra_disposable.py:86` | `def test_implant_template_has_fallback_helpers()` |
| `test_infra_phases_as_c2` | function | `tests/test_infra_disposable.py:52` | `def test_infra_phases_as_c2()` |
| `test_lab_range_profiles_registered` | function | `tests/test_infra_disposable.py:170` | `def test_lab_range_profiles_registered()` |
| `test_mitre_matrix_keeps_unknown_tactics` | function | `tests/test_infra_disposable.py:298` | `def test_mitre_matrix_keeps_unknown_tactics()` |
| `test_parse_go_version_triples` | function | `tests/test_infra_disposable.py:217` | `def test_parse_go_version_triples()` |
| `test_parse_tunnel_urls_dedupes` | function | `tests/test_infra_disposable.py:16` | `def test_parse_tunnel_urls_dedupes()` |
| `test_parse_tunnel_urls_empty` | function | `tests/test_infra_disposable.py:31` | `def test_parse_tunnel_urls_empty()` |
| `test_parse_tunnel_urls_rejects_non_cloudflare` | function | `tests/test_infra_disposable.py:38` | `def test_parse_tunnel_urls_rejects_non_cloudflare()` |
| `test_payload_schema_has_fallback_slot` | function | `tests/test_infra_disposable.py:380` | `def test_payload_schema_has_fallback_slot()` |
| `test_range_backdoor_shell_published` | function | `tests/test_infra_disposable.py:307` | `def test_range_backdoor_shell_published()` |
| `test_range_compose_uses_valid_images` | function | `tests/test_infra_disposable.py:179` | `def test_range_compose_uses_valid_images()` |
| `test_range_dc_secret_wired` | function | `tests/test_infra_disposable.py:198` | `def test_range_dc_secret_wired()` |
| `test_range_secret_generator_roundtrip` | function | `tests/test_infra_disposable.py:207` | `def test_range_secret_generator_roundtrip(tmp_path)` |
| `test_range_verify_confirms_root` | function | `tests/test_infra_disposable.py:316` | `def test_range_verify_confirms_root(capsys)` |
| `test_range_verify_unknown_profile` | function | `tests/test_infra_disposable.py:334` | `def test_range_verify_unknown_profile(capsys)` |
| `test_range_workstation_stays_alive` | function | `tests/test_infra_disposable.py:189` | `def test_range_workstation_stays_alive()` |
| `test_redirector_caddy_filters_paths` | function | `tests/test_infra_disposable.py:95` | `def test_redirector_caddy_filters_paths()` |
| `test_redirector_compose_routes_to_caddy` | function | `tests/test_infra_disposable.py:103` | `def test_redirector_compose_routes_to_caddy()` |
| `test_redirector_stale_threshold` | function | `tests/test_infra_disposable.py:272` | `def test_redirector_stale_threshold()` |
| `test_report_ai_failure_falls_back_to_template` | function | `tests/test_infra_disposable.py:150` | `def test_report_ai_failure_falls_back_to_template()` |
| `test_report_collects_history_and_loot` | function | `tests/test_infra_disposable.py:125` | `def test_report_collects_history_and_loot()` |
| `test_report_template_summary_mentions_remediation_windows` | function | `tests/test_infra_disposable.py:137` | `def test_report_template_summary_mentions_remediation_windows()` |
| `test_resolve_fallback_urls_param_list` | function | `tests/test_infra_disposable.py:78` | `def test_resolve_fallback_urls_param_list()` |
| `test_resolve_fallback_urls_param_string` | function | `tests/test_infra_disposable.py:70` | `def test_resolve_fallback_urls_param_string()` |
| `test_terraform_firewall_restricts_c2_port` | function | `tests/test_infra_disposable.py:118` | `def test_terraform_firewall_restricts_c2_port()` |
| `test_valid_providers_exact_allowlist` | function | `tests/test_infra_disposable.py:45` | `def test_valid_providers_exact_allowlist()` |
| `_host_inputs` | function | `tests/test_input_fuzz.py:85` | `def _host_inputs()` |
| `_port_inputs` | function | `tests/test_input_fuzz.py:93` | `def _port_inputs()` |
| `_random_host` | function | `tests/test_input_fuzz.py:80` | `def _random_host(rng)` |
| `test_accepted_hosts_have_no_shell_metacharacters` | function | `tests/test_input_fuzz.py:110` | `def test_accepted_hosts_have_no_shell_metacharacters(value, capsys)` |
| `test_host_validators_never_raise` | function | `tests/test_input_fuzz.py:103` | `def test_host_validators_never_raise(value, capsys)` |
| `test_known_good_values_accepted` | function | `tests/test_input_fuzz.py:126` | `def test_known_good_values_accepted(capsys)` |
| `test_port_validator_never_raise_and_bounded` | function | `tests/test_input_fuzz.py:118` | `def test_port_validator_never_raise_and_bounded(value, capsys)` |
| `test_rate_plugin_rejects_non_integer_stars` | function | `tests/test_input_fuzz.py:139` | `def test_rate_plugin_rejects_non_integer_stars(tmp_path, stars)` |
| `TestAnalysis` | class | `tests/test_intelligence_engine.py:108` | `class TestAnalysis` |
| `TestCollection` | class | `tests/test_intelligence_engine.py:45` | `class TestCollection` |
| `TestCounterIntelligence` | class | `tests/test_intelligence_engine.py:170` | `class TestCounterIntelligence` |
| `TestFullCycle` | class | `tests/test_intelligence_engine.py:191` | `class TestFullCycle` |
| `TestIntelligenceProduction` | class | `tests/test_intelligence_engine.py:155` | `class TestIntelligenceProduction` |
| `TestPlaceholderFiltering` | class | `tests/test_intelligence_engine.py:208` | `class TestPlaceholderFiltering` |
| `engine` | function | `tests/test_intelligence_engine.py:19` | `def engine()` |
| `nmap_xml` | function | `tests/test_intelligence_engine.py:24` | `def nmap_xml(tmp_path)` |
| `test_analyze_correlates_creds_to_hosts` | method | `tests/test_intelligence_engine.py:126` | `def test_analyze_correlates_creds_to_hosts(self, engine)` |
| `test_analyze_maps_apache_cve` | method | `tests/test_intelligence_engine.py:115` | `def test_analyze_maps_apache_cve(self, engine)` |
| `test_analyze_produces_assessments` | method | `tests/test_intelligence_engine.py:109` | `def test_analyze_produces_assessments(self, engine, nmap_xml)` |
| `test_analyze_ranks_targets` | method | `tests/test_intelligence_engine.py:139` | `def test_analyze_ranks_targets(self, engine)` |
| `test_collect_from_factstore` | method | `tests/test_intelligence_engine.py:95` | `def test_collect_from_factstore(self, engine, tmp_path)` |
| `test_collect_from_scan_domain` | method | `tests/test_intelligence_engine.py:63` | `def test_collect_from_scan_domain(self, engine, nmap_xml)` |
| `test_collect_from_scan_hosts` | method | `tests/test_intelligence_engine.py:70` | `def test_collect_from_scan_hosts(self, engine, nmap_xml)` |
| `test_collect_from_scan_missing_xml` | method | `tests/test_intelligence_engine.py:76` | `def test_collect_from_scan_missing_xml(self, engine)` |
| `test_collect_from_scan_os` | method | `tests/test_intelligence_engine.py:56` | `def test_collect_from_scan_os(self, engine, nmap_xml)` |
| `test_collect_from_scan_services` | method | `tests/test_intelligence_engine.py:46` | `def test_collect_from_scan_services(self, engine, nmap_xml)` |
| `test_collect_from_tool_filters_placeholders` | method | `tests/test_intelligence_engine.py:88` | `def test_collect_from_tool_filters_placeholders(self, engine)` |
| `test_collect_from_tool_parses_creds` | method | `tests/test_intelligence_engine.py:81` | `def test_collect_from_tool_parses_creds(self, engine)` |
| `test_credential_exposure_detected` | method | `tests/test_intelligence_engine.py:171` | `def test_credential_exposure_detected(self, engine)` |
| `test_get_intel_report_structured` | method | `tests/test_intelligence_engine.py:198` | `def test_get_intel_report_structured(self, engine, nmap_xml)` |
| `test_high_scan_volume_detected` | method | `tests/test_intelligence_engine.py:181` | `def test_high_scan_volume_detected(self, engine)` |
| `test_is_placeholder_detects_change_me` | method | `tests/test_intelligence_engine.py:209` | `def test_is_placeholder_detects_change_me(self, engine)` |
| `test_is_placeholder_rejects_real_values` | method | `tests/test_intelligence_engine.py:213` | `def test_is_placeholder_rejects_real_values(self, engine)` |
| `test_produce_intelligence_grades_assessments` | method | `tests/test_intelligence_engine.py:156` | `def test_produce_intelligence_grades_assessments(self, engine)` |
| `test_run_full_cycle_returns_summary` | method | `tests/test_intelligence_engine.py:192` | `def test_run_full_cycle_returns_summary(self, engine, nmap_xml)` |
| `FakeRunner` | class | `tests/test_journal.py:16` | `class FakeRunner` |
| `__call__` | method | `tests/test_journal.py:24` | `def __call__(self, args)` |
| `__init__` | method | `tests/test_journal.py:19` | `def __init__(self, responses)` |
| `_success_responses` | method | `tests/test_journal.py:34` | `def _success_responses()` |
| `test_config_from_remote_slug` | method | `tests/test_journal.py:49` | `def test_config_from_remote_slug()` |
| `test_config_rejects_bare_name` | method | `tests/test_journal.py:56` | `def test_config_rejects_bare_name()` |
| `test_entries_returns_nodes` | method | `tests/test_journal.py:71` | `def test_entries_returns_nodes()` |
| `test_graphql_errors_raise` | method | `tests/test_journal.py:91` | `def test_graphql_errors_raise()` |
| `test_missing_category_raises` | method | `tests/test_journal.py:79` | `def test_missing_category_raises()` |
| `test_post_entry_uses_resolved_ids` | method | `tests/test_journal.py:62` | `def test_post_entry_uses_resolved_ids()` |
| `_states` | function | `tests/test_killchain.py:28` | `def _states(progress)` |
| `test_activity_and_reward_accumulate` | function | `tests/test_killchain.py:62` | `def test_activity_and_reward_accumulate()` |
| `test_current_phase_from_step_events` | function | `tests/test_killchain.py:38` | `def test_current_phase_from_step_events()` |
| `test_empty_events_all_pending_without_world` | function | `tests/test_killchain.py:32` | `def test_empty_events_all_pending_without_world()` |
| `test_explicit_completed_phases_respected` | function | `tests/test_killchain.py:81` | `def test_explicit_completed_phases_respected()` |
| `test_non_dict_payload_is_tolerated` | function | `tests/test_killchain.py:92` | `def test_non_dict_payload_is_tolerated()` |
| `test_phase_advance_event_sets_current` | function | `tests/test_killchain.py:49` | `def test_phase_advance_event_sets_current()` |
| `test_unknown_phase_in_event_is_ignored` | function | `tests/test_killchain.py:86` | `def test_unknown_phase_in_event_is_ignored()` |
| `test_world_phase_fallback_when_no_events` | function | `tests/test_killchain.py:75` | `def test_world_phase_fallback_when_no_events()` |
| `TestPeriodicAutoRefresh` | class | `tests/test_killchain_auto_refresh.py:22` | `class TestPeriodicAutoRefresh` |
| `_engine` | function | `tests/test_killchain_auto_refresh.py:12` | `def _engine()` |
| `test_cadence_below_every_surpresses` | method | `tests/test_killchain_auto_refresh.py:41` | `def test_cadence_below_every_surpresses(self)` |
| `test_disabled_engine_never_shows` | method | `tests/test_killchain_auto_refresh.py:59` | `def test_disabled_engine_never_shows(self)` |
| `test_phase_change_beats_periodic_cadence` | method | `tests/test_killchain_auto_refresh.py:50` | `def test_phase_change_beats_periodic_cadence(self)` |
| `test_shows_immediately_on_phase_change` | method | `tests/test_killchain_auto_refresh.py:23` | `def test_shows_immediately_on_phase_change(self)` |
| `test_shows_on_cadence_without_phase_change` | method | `tests/test_killchain_auto_refresh.py:31` | `def test_shows_on_cadence_without_phase_change(self)` |
| `test_zero_every_and_no_phase_change_never_shows` | method | `tests/test_killchain_auto_refresh.py:67` | `def test_zero_every_and_no_phase_change_never_shows(self)` |
| `TestGapCredsNoLateral` | class | `tests/test_killchain_gap_signal.py:122` | `class TestGapCredsNoLateral` |
| `TestGapExploitedNoPrivesc` | class | `tests/test_killchain_gap_signal.py:39` | `class TestGapExploitedNoPrivesc` |
| `TestGapOwnedNoCreds` | class | `tests/test_killchain_gap_signal.py:75` | `class TestGapOwnedNoCreds` |
| `TestGapScanNoEnum` | class | `tests/test_killchain_gap_signal.py:98` | `class TestGapScanNoEnum` |
| `TestKillchainGapSignalConstruction` | class | `tests/test_killchain_gap_signal.py:32` | `class TestKillchainGapSignalConstruction` |
| `TestKillchainGapSignalIntegration` | class | `tests/test_killchain_gap_signal.py:145` | `class TestKillchainGapSignalIntegration` |
| `_write_world_model` | function | `tests/test_killchain_gap_signal.py:28` | `def _write_world_model(sessions_dir, data)` |
| `sessions_dir` | function | `tests/test_killchain_gap_signal.py:23` | `def sessions_dir()` |
| `test_credentials_no_lateral_recommends_crackmapexec` | method | `tests/test_killchain_gap_signal.py:124` | `def test_credentials_no_lateral_recommends_crackmapexec(self, sessions_dir)` |
| `test_exploited_linux_recommends_linpeas` | method | `tests/test_killchain_gap_signal.py:41` | `def test_exploited_linux_recommends_linpeas(self, sessions_dir)` |
| `test_exploited_windows_recommends_winpeas` | method | `tests/test_killchain_gap_signal.py:50` | `def test_exploited_windows_recommends_winpeas(self, sessions_dir)` |
| `test_multiple_gaps_detected_simultaneously` | method | `tests/test_killchain_gap_signal.py:147` | `def test_multiple_gaps_detected_simultaneously(self, sessions_dir)` |
| `test_name_is_gap_source` | method | `tests/test_killchain_gap_signal.py:34` | `def test_name_is_gap_source(self)` |
| `test_no_credentials_no_lateral_proposals` | method | `tests/test_killchain_gap_signal.py:134` | `def test_no_credentials_no_lateral_proposals(self, sessions_dir)` |
| `test_no_world_model_returns_empty` | method | `tests/test_killchain_gap_signal.py:68` | `def test_no_world_model_returns_empty(self, sessions_dir)` |
| `test_owned_no_credentials_recommends_lazydump` | method | `tests/test_killchain_gap_signal.py:77` | `def test_owned_no_credentials_recommends_lazydump(self, sessions_dir)` |
| `test_owned_with_credentials_no_proposals` | method | `tests/test_killchain_gap_signal.py:87` | `def test_owned_with_credentials_no_proposals(self, sessions_dir)` |
| `test_scanned_no_enum_recommends_gobuster` | method | `tests/test_killchain_gap_signal.py:100` | `def test_scanned_no_enum_recommends_gobuster(self, sessions_dir)` |
| `test_scanned_with_enum_recent_no_proposals` | method | `tests/test_killchain_gap_signal.py:109` | `def test_scanned_with_enum_recent_no_proposals(self, sessions_dir)` |
| `test_unscanned_host_no_proposals` | method | `tests/test_killchain_gap_signal.py:59` | `def test_unscanned_host_no_proposals(self, sessions_dir)` |
| `TestEncryptedStateTransparency` | class | `tests/test_killchain_snapshot.py:102` | `class TestEncryptedStateTransparency` |
| `TestKillChainSnapshot` | class | `tests/test_killchain_snapshot.py:52` | `class TestKillChainSnapshot` |
| `_encrypt_at` | function | `tests/test_killchain_snapshot.py:41` | `def _encrypt_at(path, password, salt)` |
| `_seed_snapshot` | function | `tests/test_killchain_snapshot.py:17` | `def _seed_snapshot(path, phase, completed, current)` |
| `_states` | function | `tests/test_killchain_snapshot.py:37` | `def _states(snapshot)` |
| `test_advance_then_snapshot_is_consistent` | method | `tests/test_killchain_snapshot.py:90` | `def test_advance_then_snapshot_is_consistent(self, tmp_path)` |
| `test_empty_snapshot_defaults_to_recon` | method | `tests/test_killchain_snapshot.py:53` | `def test_empty_snapshot_defaults_to_recon(self, tmp_path)` |
| `test_encrypted_without_password_reads_empty` | method | `tests/test_killchain_snapshot.py:131` | `def test_encrypted_without_password_reads_empty(self, tmp_path, monkeypatch)` |
| `test_missing_file_reads_empty` | method | `tests/test_killchain_snapshot.py:123` | `def test_missing_file_reads_empty(self, tmp_path)` |
| `test_read_state_dict_decrypts_at_rest` | method | `tests/test_killchain_snapshot.py:103` | `def test_read_state_dict_decrypts_at_rest(self, tmp_path, monkeypatch)` |
| `test_snapshot_is_json_serialisable` | method | `tests/test_killchain_snapshot.py:80` | `def test_snapshot_is_json_serialisable(self, tmp_path)` |
| `test_snapshot_reflects_explicit_phase_and_completed` | method | `tests/test_killchain_snapshot.py:64` | `def test_snapshot_reflects_explicit_phase_and_completed(self, tmp_path)` |
| `TestPhaseMapping` | class | `tests/test_killchain_unified.py:19` | `class TestPhaseMapping` |
| `TestWritePhaseWithWorldModel` | class | `tests/test_killchain_unified.py:48` | `class TestWritePhaseWithWorldModel` |
| `sessions_dir` | method | `tests/test_killchain_unified.py:52` | `def sessions_dir(self)` |
| `test_cli_phase_to_host_state_maps_correctly` | method | `tests/test_killchain_unified.py:30` | `def test_cli_phase_to_host_state_maps_correctly(self)` |
| `test_engagement_phase_to_cli_maps_all` | method | `tests/test_killchain_unified.py:21` | `def test_engagement_phase_to_cli_maps_all(self)` |
| `test_phase_rank_returns_correct_index` | method | `tests/test_killchain_unified.py:41` | `def test_phase_rank_returns_correct_index(self)` |
| `test_write_phase_advances_hosts` | method | `tests/test_killchain_unified.py:78` | `def test_write_phase_advances_hosts(self, sessions_dir)` |
| `test_write_phase_completed_phases_tracks_progress` | method | `tests/test_killchain_unified.py:97` | `def test_write_phase_completed_phases_tracks_progress(self, sessions_dir)` |
| `test_write_phase_invalid_returns_false` | method | `tests/test_killchain_unified.py:93` | `def test_write_phase_invalid_returns_false(self, sessions_dir)` |
| `TestKillChainAdvancePhase` | class | `tests/test_killchain_unified_v2.py:184` | `class TestKillChainAdvancePhase` |
| `TestKillChainConfig` | class | `tests/test_killchain_unified_v2.py:31` | `class TestKillChainConfig` |
| `TestKillChainCurrentPhase` | class | `tests/test_killchain_unified_v2.py:103` | `class TestKillChainCurrentPhase` |
| `TestKillChainGetProgress` | class | `tests/test_killchain_unified_v2.py:279` | `class TestKillChainGetProgress` |
| `TestKillChainHelpers` | class | `tests/test_killchain_unified_v2.py:347` | `class TestKillChainHelpers` |
| `TestPhaseStatusDataclass` | class | `tests/test_killchain_unified_v2.py:394` | `class TestPhaseStatusDataclass` |
| `_reset_wm_singleton` | method | `tests/test_killchain_unified_v2.py:107` | `def _reset_wm_singleton(self)` |
| `_reset_wm_singleton` | method | `tests/test_killchain_unified_v2.py:188` | `def _reset_wm_singleton(self)` |
| `_reset_wm_singleton` | method | `tests/test_killchain_unified_v2.py:283` | `def _reset_wm_singleton(self)` |
| `test_advance_advances_world_model_hosts` | method | `tests/test_killchain_unified_v2.py:243` | `def test_advance_advances_world_model_hosts(self)` |
| `test_advance_does_not_downgrade_cached_world_model_state` | method | `tests/test_killchain_unified_v2.py:260` | `def test_advance_does_not_downgrade_cached_world_model_state(self)` |
| `test_advance_invalid_phase_returns_false` | method | `tests/test_killchain_unified_v2.py:233` | `def test_advance_invalid_phase_returns_false(self)` |
| `test_advance_tracks_completed_phases` | method | `tests/test_killchain_unified_v2.py:215` | `def test_advance_tracks_completed_phases(self)` |
| `test_advance_writes_current_phase_and_phase_keys` | method | `tests/test_killchain_unified_v2.py:199` | `def test_advance_writes_current_phase_and_phase_keys(self)` |
| `test_all_pending_when_nothing_done` | method | `tests/test_killchain_unified_v2.py:294` | `def test_all_pending_when_nothing_done(self)` |
| `test_all_phases_have_colors` | method | `tests/test_killchain_unified_v2.py:53` | `def test_all_phases_have_colors(self)` |
| `test_all_phases_have_labels` | method | `tests/test_killchain_unified_v2.py:48` | `def test_all_phases_have_labels(self)` |
| `test_all_phases_have_rich_colors` | method | `tests/test_killchain_unified_v2.py:58` | `def test_all_phases_have_rich_colors(self)` |
| `test_cli_phase_to_host_state_maps_all` | method | `tests/test_killchain_unified_v2.py:375` | `def test_cli_phase_to_host_state_maps_all(self)` |
| `test_cli_to_host_state_returns_expected` | method | `tests/test_killchain_unified_v2.py:70` | `def test_cli_to_host_state_returns_expected(self)` |
| `test_compact_phases_and_labels` | method | `tests/test_killchain_unified_v2.py:91` | `def test_compact_phases_and_labels(self)` |
| `test_compact_phases_are_in_correct_order` | method | `tests/test_killchain_unified_v2.py:44` | `def test_compact_phases_are_in_correct_order(self)` |
| `test_compact_progress_returns_string` | method | `tests/test_killchain_unified_v2.py:360` | `def test_compact_progress_returns_string(self)` |
| `test_engagement_phase_to_cli_maps_all` | method | `tests/test_killchain_unified_v2.py:366` | `def test_engagement_phase_to_cli_maps_all(self)` |
| `test_engagement_to_cli_covers_all_engagement_phases` | method | `tests/test_killchain_unified_v2.py:62` | `def test_engagement_to_cli_covers_all_engagement_phases(self)` |
| `test_falls_back_to_legacy_phase_key` | method | `tests/test_killchain_unified_v2.py:172` | `def test_falls_back_to_legacy_phase_key(self)` |
| `test_get_killchain_returns_class` | method | `tests/test_killchain_unified_v2.py:383` | `def test_get_killchain_returns_class(self)` |
| `test_is_valid_phase` | method | `tests/test_killchain_unified_v2.py:86` | `def test_is_valid_phase(self)` |
| `test_phase_index_returns_correct` | method | `tests/test_killchain_unified_v2.py:387` | `def test_phase_index_returns_correct(self)` |
| `test_phase_index_valid_and_invalid` | method | `tests/test_killchain_unified_v2.py:80` | `def test_phase_index_valid_and_invalid(self)` |
| `test_phase_status_fields_match_config` | method | `tests/test_killchain_unified_v2.py:402` | `def test_phase_status_fields_match_config(self)` |

Next: [SYMBOLS_p31.md](SYMBOLS_p31.md)
