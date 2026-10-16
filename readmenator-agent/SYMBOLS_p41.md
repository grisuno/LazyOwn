# Symbols (page 41 of 41)
Previous: [SYMBOLS_p40.md](SYMBOLS_p40.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `TestWorldModelCollection` | class | `tests/test_unified_dashboard.py:21` | `class TestWorldModelCollection` |
| `test_collect_daemon_status_exists` | method | `tests/test_unified_dashboard.py:37` | `def test_collect_daemon_status_exists(self, tmp_path)` |
| `test_collect_daemon_status_missing` | method | `tests/test_unified_dashboard.py:45` | `def test_collect_daemon_status_missing(self, tmp_path)` |
| `test_collect_world_model_exists` | method | `tests/test_unified_dashboard.py:22` | `def test_collect_world_model_exists(self, tmp_path)` |
| `test_collect_world_model_missing` | method | `tests/test_unified_dashboard.py:30` | `def test_collect_world_model_missing(self, tmp_path)` |
| `test_default_init` | method | `tests/test_unified_dashboard.py:11` | `def test_default_init(self, tmp_path)` |
| `test_export_json` | method | `tests/test_unified_dashboard.py:96` | `def test_export_json(self, tmp_path)` |
| `test_get_unified_dashboard_singleton` | method | `tests/test_unified_dashboard.py:15` | `def test_get_unified_dashboard_singleton(self, tmp_path)` |
| `test_render_contains_header` | method | `tests/test_unified_dashboard.py:75` | `def test_render_contains_header(self, tmp_path)` |
| `test_render_contains_sections` | method | `tests/test_unified_dashboard.py:80` | `def test_render_contains_sections(self, tmp_path)` |
| `test_render_contains_timestamp` | method | `tests/test_unified_dashboard.py:89` | `def test_render_contains_timestamp(self, tmp_path)` |
| `test_snapshot_keys` | method | `tests/test_unified_dashboard.py:52` | `def test_snapshot_keys(self, tmp_path)` |
| `test_snapshot_timestamp` | method | `tests/test_unified_dashboard.py:67` | `def test_snapshot_timestamp(self, tmp_path)` |
| `test_import_with_foreign_argv_is_silent` | function | `tests/test_utils_import_silent.py:12` | `def test_import_with_foreign_argv_is_silent()` |
| `test_lazy_import_chains_stay_silent` | function | `tests/test_utils_import_silent.py:34` | `def test_lazy_import_chains_stay_silent()` |
| `test_demo_gif_commands_exist_in_source` | function | `tests/test_viral_adoption.py:23` | `def test_demo_gif_commands_exist_in_source()` |
| `test_demo_gifs_exist_and_nonempty` | function | `tests/test_viral_adoption.py:8` | `def test_demo_gifs_exist_and_nonempty()` |
| `test_docs_drift_workflow_exists` | function | `tests/test_viral_adoption.py:89` | `def test_docs_drift_workflow_exists()` |
| `test_launch_kit_exists` | function | `tests/test_viral_adoption.py:101` | `def test_launch_kit_exists()` |
| `test_marketplace_template_exists` | function | `tests/test_viral_adoption.py:95` | `def test_marketplace_template_exists()` |
| `test_readme_links_viral_assets` | function | `tests/test_viral_adoption.py:75` | `def test_readme_links_viral_assets()` |
| `test_smoke_script_covers_onboarding` | function | `tests/test_viral_adoption.py:83` | `def test_smoke_script_covers_onboarding()` |
| `MitigationSuiteConfig` | class | `tests/test_vuln_mitigations.py:29` | `class MitigationSuiteConfig` |
| `TestMitigationConfigInvariants` | class | `tests/test_vuln_mitigations.py:224` | `class TestMitigationConfigInvariants` |
| `TestSentinelRegexSafety` | class | `tests/test_vuln_mitigations.py:166` | `class TestSentinelRegexSafety` |
| `TestStackTraceSanitisation` | class | `tests/test_vuln_mitigations.py:89` | `class TestStackTraceSanitisation` |
| `_extract_sanitise_pattern` | method | `tests/test_vuln_mitigations.py:181` | `def _extract_sanitise_pattern(self, src)` |
| `_iter_function_bodies` | function | `tests/test_vuln_mitigations.py:77` | `def _iter_function_bodies(src)` |
| `_read_module` | function | `tests/test_vuln_mitigations.py:69` | `def _read_module(config, relative_path)` |
| `lazyc2_src` | method | `tests/test_vuln_mitigations.py:93` | `def lazyc2_src(self, mitigation_config)` |
| `mitigation_config` | function | `tests/test_vuln_mitigations.py:64` | `def mitigation_config()` |
| `phishingai_src` | method | `tests/test_vuln_mitigations.py:98` | `def phishingai_src(self, mitigation_config)` |
| `repo_root` | method | `tests/test_vuln_mitigations.py:58` | `def repo_root(self)` |
| `src` | method | `tests/test_vuln_mitigations.py:177` | `def src(self, mitigation_config)` |
| `test_dynamic_route_drops_raw_save_to_log_payload` | method | `tests/test_vuln_mitigations.py:140` | `def test_dynamic_route_drops_raw_save_to_log_payload(self, lazyc2_src)` |
| `test_handler_module_paths_exist` | method | `tests/test_vuln_mitigations.py:227` | `def test_handler_module_paths_exist(self, mitigation_config)` |
| `test_log_handler_keeps_server_side_logging` | method | `tests/test_vuln_mitigations.py:112` | `def test_log_handler_keeps_server_side_logging(self, lazyc2_src)` |
| `test_log_handler_returns_generic_message` | method | `tests/test_vuln_mitigations.py:102` | `def test_log_handler_returns_generic_message(self, lazyc2_src)` |
| `test_no_forbidden_response_substrings_remain` | method | `tests/test_vuln_mitigations.py:154` | `def test_no_forbidden_response_substrings_remain(self, lazyc2_src, phishingai_src, mitigation_config)` |
| `test_no_redundant_character_range_in_sanitise` | method | `tests/test_vuln_mitigations.py:188` | `def test_no_redundant_character_range_in_sanitise(self, src)` |
| `test_palette_api_keeps_server_side_logging` | method | `tests/test_vuln_mitigations.py:131` | `def test_palette_api_keeps_server_side_logging(self, lazyc2_src)` |
| `test_palette_api_returns_generic_message` | method | `tests/test_vuln_mitigations.py:121` | `def test_palette_api_returns_generic_message(self, lazyc2_src)` |
| `test_pattern_does_not_strip_brackets` | method | `tests/test_vuln_mitigations.py:217` | `def test_pattern_does_not_strip_brackets(self, src)` |
| `test_pattern_keeps_printable_ascii` | method | `tests/test_vuln_mitigations.py:197` | `def test_pattern_keeps_printable_ascii(self, src)` |
| `test_pattern_keeps_tab_and_newline` | method | `tests/test_vuln_mitigations.py:203` | `def test_pattern_keeps_tab_and_newline(self, src)` |
| `test_pattern_matches_simplified_form` | method | `tests/test_vuln_mitigations.py:193` | `def test_pattern_matches_simplified_form(self, src)` |
| `test_pattern_strips_control_bytes` | method | `tests/test_vuln_mitigations.py:209` | `def test_pattern_strips_control_bytes(self, src)` |
| `test_phishing_ai_returns_generic_message` | method | `tests/test_vuln_mitigations.py:149` | `def test_phishing_ai_returns_generic_message(self, phishingai_src)` |
| `test_sentinel_function_exposed` | method | `tests/test_vuln_mitigations.py:236` | `def test_sentinel_function_exposed(self, mitigation_config)` |
| `test_sentinel_module_exists` | method | `tests/test_vuln_mitigations.py:232` | `def test_sentinel_module_exists(self, mitigation_config)` |
| `TestBinaryNameRegex` | class | `tests/test_wizard_binary_check.py:58` | `class TestBinaryNameRegex` |
| `TestBinarySpecRegistry` | class | `tests/test_wizard_binary_check.py:32` | `class TestBinarySpecRegistry` |
| `TestCheckBinariesContract` | class | `tests/test_wizard_binary_check.py:92` | `class TestCheckBinariesContract` |
| `TestGroupByCategory` | class | `tests/test_wizard_binary_check.py:143` | `class TestGroupByCategory` |
| `TestPublicSurface` | class | `tests/test_wizard_binary_check.py:199` | `class TestPublicSurface` |
| `TestRunIntegratesBinaryCheck` | class | `tests/test_wizard_binary_check.py:156` | `class TestRunIntegratesBinaryCheck` |
| `_fail` | function | `tests/test_wizard_binary_check.py:127` | `def _fail()` |
| `fake_check` | function | `tests/test_wizard_binary_check.py:160` | `def fake_check()` |
| `fake_check` | function | `tests/test_wizard_binary_check.py:179` | `def fake_check()` |
| `test_accepts_known_safe_names` | method | `tests/test_wizard_binary_check.py:72` | `def test_accepts_known_safe_names(self, name)` |
| `test_check_binaries_in_dunder_all` | method | `tests/test_wizard_binary_check.py:200` | `def test_check_binaries_in_dunder_all(self)` |
| `test_check_does_not_invoke_subprocess` | method | `tests/test_wizard_binary_check.py:122` | `def test_check_does_not_invoke_subprocess(self, monkeypatch)` |
| `test_default_registry_is_not_empty` | method | `tests/test_wizard_binary_check.py:33` | `def test_default_registry_is_not_empty(self)` |
| `test_default_specs_used_when_omitted` | method | `tests/test_wizard_binary_check.py:138` | `def test_default_specs_used_when_omitted(self)` |
| `test_every_name_matches_safety_regex` | method | `tests/test_wizard_binary_check.py:44` | `def test_every_name_matches_safety_regex(self)` |
| `test_every_spec_has_required_fields` | method | `tests/test_wizard_binary_check.py:36` | `def test_every_spec_has_required_fields(self)` |
| `test_groups_preserve_order` | method | `tests/test_wizard_binary_check.py:144` | `def test_groups_preserve_order(self)` |
| `test_kill_chain_categories_covered` | method | `tests/test_wizard_binary_check.py:52` | `def test_kill_chain_categories_covered(self)` |
| `test_marks_missing_when_which_returns_none` | method | `tests/test_wizard_binary_check.py:103` | `def test_marks_missing_when_which_returns_none(self)` |
| `test_marks_present_when_which_returns_path` | method | `tests/test_wizard_binary_check.py:109` | `def test_marks_present_when_which_returns_path(self)` |
| `test_no_duplicate_binary_names` | method | `tests/test_wizard_binary_check.py:48` | `def test_no_duplicate_binary_names(self)` |
| `test_rejects_unsafe_names` | method | `tests/test_wizard_binary_check.py:88` | `def test_rejects_unsafe_names(self, name)` |
| `test_returns_one_status_per_spec` | method | `tests/test_wizard_binary_check.py:93` | `def test_returns_one_status_per_spec(self)` |
| `test_run_populates_binaries_after_updates` | method | `tests/test_wizard_binary_check.py:176` | `def test_run_populates_binaries_after_updates(self, monkeypatch)` |
| `test_run_populates_binaries_when_nothing_changes` | method | `tests/test_wizard_binary_check.py:157` | `def test_run_populates_binaries_when_nothing_changes(self, monkeypatch)` |
| `test_skips_specs_with_unsafe_names` | method | `tests/test_wizard_binary_check.py:115` | `def test_skips_specs_with_unsafe_names(self)` |
| `TestAskLlm` | class | `tests/test_wizard_llm.py:59` | `class TestAskLlm` |
| `TestMaskSecret` | class | `tests/test_wizard_llm.py:45` | `class TestMaskSecret` |
| `TestNormalizeProviderAnswer` | class | `tests/test_wizard_llm.py:23` | `class TestNormalizeProviderAnswer` |
| `TestReadinessLlm` | class | `tests/test_wizard_llm.py:121` | `class TestReadinessLlm` |
| `_fake` | function | `tests/test_wizard_llm.py:17` | `def _fake(message)` |
| `_fake` | function | `tests/test_wizard_llm.py:92` | `def _fake(message)` |
| `_fake` | function | `tests/test_wizard_llm.py:109` | `def _fake(message)` |
| `_row` | method | `tests/test_wizard_llm.py:122` | `def _row(self, params, label)` |
| `_scripted_prompt` | function | `tests/test_wizard_llm.py:14` | `def _scripted_prompt(answers)` |
| `test_blank_answers_keep_everything` | method | `tests/test_wizard_llm.py:60` | `def test_blank_answers_keep_everything(self, monkeypatch)` |
| `test_blank_returns_none` | method | `tests/test_wizard_llm.py:24` | `def test_blank_returns_none(self)` |
| `test_cloud_with_key_ok` | method | `tests/test_wizard_llm.py:126` | `def test_cloud_with_key_ok(self)` |
| `test_cloud_without_key_missing` | method | `tests/test_wizard_llm.py:131` | `def test_cloud_without_key_missing(self)` |
| `test_empty_returns_not_set` | method | `tests/test_wizard_llm.py:46` | `def test_empty_returns_not_set(self)` |
| `test_existing_key_prompt_shows_mask` | method | `tests/test_wizard_llm.py:106` | `def test_existing_key_prompt_shows_mask(self, monkeypatch)` |
| `test_invalid_backend_missing_with_fix_hint` | method | `tests/test_wizard_llm.py:141` | `def test_invalid_backend_missing_with_fix_hint(self)` |
| `test_invalid_provider_keeps_current` | method | `tests/test_wizard_llm.py:76` | `def test_invalid_provider_keeps_current(self, monkeypatch)` |
| `test_key_kept_when_blank` | method | `tests/test_wizard_llm.py:102` | `def test_key_kept_when_blank(self, monkeypatch)` |
| `test_long_value_masked_with_tail` | method | `tests/test_wizard_llm.py:50` | `def test_long_value_masked_with_tail(self)` |
| `test_model_override_stored_in_provider_slot` | method | `tests/test_wizard_llm.py:80` | `def test_model_override_stored_in_provider_slot(self, monkeypatch)` |
| `test_model_shown_in_value` | method | `tests/test_wizard_llm.py:146` | `def test_model_shown_in_value(self)` |
| `test_name_case_insensitive` | method | `tests/test_wizard_llm.py:28` | `def test_name_case_insensitive(self)` |
| `test_number_selects_backend` | method | `tests/test_wizard_llm.py:32` | `def test_number_selects_backend(self)` |
| `test_ollama_keyless_ok` | method | `tests/test_wizard_llm.py:136` | `def test_ollama_keyless_ok(self)` |
| `test_ollama_skips_key_prompt` | method | `tests/test_wizard_llm.py:89` | `def test_ollama_skips_key_prompt(self, monkeypatch)` |
| `test_out_of_range_number_returns_none` | method | `tests/test_wizard_llm.py:37` | `def test_out_of_range_number_returns_none(self)` |
| `test_provider_change_by_name` | method | `tests/test_wizard_llm.py:65` | `def test_provider_change_by_name(self, monkeypatch)` |
| `test_provider_change_by_number` | method | `tests/test_wizard_llm.py:70` | `def test_provider_change_by_number(self, monkeypatch)` |
| `test_sensitive_values_masked` | method | `tests/test_wizard_llm.py:150` | `def test_sensitive_values_masked(self)` |
| `test_short_value_never_shown_clear` | method | `tests/test_wizard_llm.py:53` | `def test_short_value_never_shown_clear(self)` |
| `test_unknown_name_returns_none` | method | `tests/test_wizard_llm.py:41` | `def test_unknown_name_returns_none(self)` |
| `TestAdvanceHostEdgeCases` | class | `tests/test_world_model_extended.py:73` | `class TestAdvanceHostEdgeCases` |
| `TestGetHost` | class | `tests/test_world_model_extended.py:43` | `class TestGetHost` |
| `TestGetHostsSummary` | class | `tests/test_world_model_extended.py:61` | `class TestGetHostsSummary` |
| `TestGetPhaseAfterStateChanges` | class | `tests/test_world_model_extended.py:90` | `class TestGetPhaseAfterStateChanges` |
| `TestSetOsHint` | class | `tests/test_world_model_extended.py:22` | `class TestSetOsHint` |
| `test_advance_host_skips_on_lower_state` | method | `tests/test_world_model_extended.py:79` | `def test_advance_host_skips_on_lower_state(self, world_model)` |
| `test_advance_host_skips_on_same_state` | method | `tests/test_world_model_extended.py:74` | `def test_advance_host_skips_on_same_state(self, world_model)` |
| `test_advance_host_to_owned_is_allowed_from_exploited` | method | `tests/test_world_model_extended.py:84` | `def test_advance_host_to_owned_is_allowed_from_exploited(self, world_model)` |
| `test_empty_summary` | method | `tests/test_world_model_extended.py:62` | `def test_empty_summary(self, world_model)` |
| `test_get_host_is_thread_safe` | method | `tests/test_world_model_extended.py:53` | `def test_get_host_is_thread_safe(self, world_model)` |
| `test_get_host_returns_entry_for_known` | method | `tests/test_world_model_extended.py:47` | `def test_get_host_returns_entry_for_known(self, world_model)` |
| `test_get_host_returns_none_for_unknown` | method | `tests/test_world_model_extended.py:44` | `def test_get_host_returns_none_for_unknown(self, world_model)` |
| `test_phase_complete_when_all_owned` | method | `tests/test_world_model_extended.py:100` | `def test_phase_complete_when_all_owned(self, world_model)` |
| `test_phase_derived_from_host_state` | method | `tests/test_world_model_extended.py:91` | `def test_phase_derived_from_host_state(self, world_model)` |
| `test_phase_post_exploitation_on_owned` | method | `tests/test_world_model_extended.py:95` | `def test_phase_post_exploitation_on_owned(self, world_model)` |
| `test_phase_recon_when_no_hosts` | method | `tests/test_world_model_extended.py:105` | `def test_phase_recon_when_no_hosts(self, world_model)` |
| `test_populated_summary` | method | `tests/test_world_model_extended.py:65` | `def test_populated_summary(self, world_model)` |
| `test_set_os_hint_empty_string_is_stored` | method | `tests/test_world_model_extended.py:36` | `def test_set_os_hint_empty_string_is_stored(self, world_model)` |
| `test_set_os_hint_on_existing_host` | method | `tests/test_world_model_extended.py:29` | `def test_set_os_hint_on_existing_host(self, world_model)` |
| `test_set_os_hint_on_new_host` | method | `tests/test_world_model_extended.py:23` | `def test_set_os_hint_on_new_host(self, world_model)` |
| `world_model` | function | `tests/test_world_model_extended.py:14` | `def world_model()` |
| `TestXssSinks` | class | `tests/test_xss_sanitization.py:22` | `class TestXssSinks` |
| `_src` | function | `tests/test_xss_sanitization.py:18` | `def _src(name)` |
| `test_collab_events_escaped` | method | `tests/test_xss_sanitization.py:23` | `def test_collab_events_escaped(self)` |
| `test_index_lazyos_response_sanitized` | method | `tests/test_xss_sanitization.py:47` | `def test_index_lazyos_response_sanitized(self)` |
| `test_new_campaign_chunks_sanitized` | method | `tests/test_xss_sanitization.py:37` | `def test_new_campaign_chunks_sanitized(self)` |
| `test_surface_labels_escaped` | method | `tests/test_xss_sanitization.py:42` | `def test_surface_labels_escaped(self)` |
| `test_yaml_view_chatbot_sanitized` | method | `tests/test_xss_sanitization.py:32` | `def test_yaml_view_chatbot_sanitized(self)` |
| `test_yaml_view_loads_purify` | method | `tests/test_xss_sanitization.py:28` | `def test_yaml_view_loads_purify(self)` |
| `check_file` | function | `tools/contract_check.py:19` | `def check_file(path)` |
| `main` | function | `tools/contract_check.py:46` | `def main(argv)` |
| `build_module` | function | `tools/extract_cluster.py:66` | `def build_module(target_class, phase, category, title, methods, extra_imports)` |
| `collect_methods` | function | `tools/extract_cluster.py:41` | `def collect_methods(source_text, wanted)` |
| `fragment_name` | function | `tools/extract_cluster.py:29` | `def fragment_name(fragment)` |
| `main` | function | `tools/extract_cluster.py:141` | `def main()` |
| `font` | function | `tools/gen_demo_gifs.py:14` | `def font(size)` |
| `main` | function | `tools/gen_demo_gifs.py:70` | `def main()` |
| `render` | function | `tools/gen_demo_gifs.py:22` | `def render(lines, path, hold)` |
| `main` | function | `tools/gen_demo_gifs_extra.py:49` | `def main()` |
| `IP2ASN` | class | `utils.py:3137` | `class IP2ASN` |
| `MyServer` | class | `utils.py:3099` | `class MyServer(HTTPServer)` |
| `ProcessResults` | function | `utils.py:2317` | `def ProcessResults(results, outfile)` |
| `SimpleHTTPRequestHandler` | class | `utils.py:3107` | `class SimpleHTTPRequestHandler(BaseHTTPRequestHandler)` |
| `Spray` | function | `utils.py:2270` | `def Spray(domain, users, password, target_url, wait, verbose, more_verbose)` |
| `VulnerabilityScanner` | class | `utils.py:3226` | `class VulnerabilityScanner` |
| `__init__` | method | `utils.py:3138` | `def __init__(self)` |
| `__init__` | method | `utils.py:3244` | `def __init__(self, user_agent, max_workers, sessions_dir, description_language)` |
| `_build_startup_parser` | function | `utils.py:3403` | `def _build_startup_parser()` |
| `_cvss_sort_key` | function | `utils.py:3390` | `def _cvss_sort_key(record)` |
| `_enrich_cve` | method | `utils.py:3319` | `def _enrich_cve(self, cve_info)` |
| `_load_prompt_payload` | function | `utils.py:711` | `def _load_prompt_payload()` |
| `_parse_file` | method | `utils.py:3158` | `def _parse_file(self, reader)` |
| `_rec_index_has_ip` | method | `utils.py:3194` | `def _rec_index_has_ip(self, idx, ip)` |
| `_redact` | function | `utils.py:1142` | `def _redact(text)` |
| `activate_server` | function | `utils.py:2259` | `def activate_server(httpd, url, lhost)` |
| `activate_virtualenv` | function | `utils.py:540` | `def activate_virtualenv(venv_path)` |
| `add` | function | `utils.py:1748` | `def add(str_part, delimiter, i)` |
| `aggressive_yaml_fix` | function | `utils.py:3007` | `def aggressive_yaml_fix(yaml_content)` |
| `anti_debug` | function | `utils.py:3058` | `def anti_debug()` |
| `as_country` | method | `utils.py:3207` | `def as_country(self, asn)` |
| `as_name` | method | `utils.py:3203` | `def as_name(self, asn)` |
| `as_of_ip` | method | `utils.py:3188` | `def as_of_ip(self, ip)` |
| `clean_html` | function | `utils.py:1510` | `def clean_html(html_string)` |
| `clean_output` | function | `utils.py:763` | `def clean_output(output)` |
| `clean_url` | function | `utils.py:1375` | `def clean_url(host)` |
| `copy2clip` | function | `utils.py:743` | `def copy2clip(text)` |
| `crack_password` | function | `utils.py:1932` | `def crack_password(crypttext)` |
| `create_arp_packet` | function | `utils.py:418` | `def create_arp_packet(src_mac, src_ip, dst_ip, dst_mac)` |
| `create_caldera_config` | function | `utils.py:2403` | `def create_caldera_config(file_path)` |
| `create_msfshellcoder_parser` | function | `utils.py:3067` | `def create_msfshellcoder_parser()` |
| `create_synthetic_yaml` | function | `utils.py:2859` | `def create_synthetic_yaml(nmap_services)` |
| `de_htmlify` | function | `utils.py:2608` | `def de_htmlify(data)` |
| `decode` | function | `utils.py:2202` | `def decode(data)` |
| `detect_delimiter` | function | `utils.py:1765` | `def detect_delimiter(foo_bar)` |
| `display_news` | function | `utils.py:2583` | `def display_news(titles, links, scores)` |
| `do_GET` | method | `utils.py:3118` | `def do_GET(self)` |
| `ensure_tmux_session` | function | `utils.py:2036` | `def ensure_tmux_session(session_name)` |
| `exploitalert` | function | `utils.py:848` | `def exploitalert(content)` |
| `extract` | function | `utils.py:1486` | `def extract(string, extract_flag)` |
| `extract_banners` | function | `utils.py:2499` | `def extract_banners(xml_file)` |
| `find_ea` | function | `utils.py:1033` | `def find_ea(keyword)` |
| `find_ps` | function | `utils.py:1083` | `def find_ps(keyword)` |
| `find_ss` | function | `utils.py:971` | `def find_ss(keyword)` |
| `fix_common_yaml_issues` | function | `utils.py:2967` | `def fix_common_yaml_issues(yaml_content)` |
| `format_openssh_key` | function | `utils.py:1412` | `def format_openssh_key(raw_key)` |
| `format_rsa_key` | function | `utils.py:1444` | `def format_rsa_key(raw_key)` |
| `generate_certificates` | function | `utils.py:1232` | `def generate_certificates()` |
| `generate_emails` | function | `utils.py:1315` | `def generate_emails(full_name, domain)` |
| `generate_http_req` | function | `utils.py:1388` | `def generate_http_req(host, port, uri, custom_header, cmd)` |
| `generate_index` | function | `utils.py:2332` | `def generate_index(repo_dir)` |
| `generate_random_cve_id` | function | `utils.py:1220` | `def generate_random_cve_id()` |
| `get_banner` | function | `utils.py:2140` | `def get_banner(ip, port)` |
| `get_command` | function | `utils.py:2220` | `def get_command(url, lhost)` |
| `get_credentials` | function | `utils.py:1537` | `def get_credentials(file, ncred)` |
| `get_domain` | function | `utils.py:1203` | `def get_domain(url)` |
| `get_domain_from_xml` | function | `utils.py:2085` | `def get_domain_from_xml(xml_file)` |
| `get_git_info` | function | `utils.py:685` | `def get_git_info()` |
| `get_hash` | function | `utils.py:1879` | `def get_hash(dir)` |
| `get_network_info` | function | `utils.py:650` | `def get_network_info()` |
| `get_open_ports` | function | `utils.py:609` | `def get_open_ports()` |
| `get_org` | function | `utils.py:2662` | `def get_org(data)` |
| `get_terminal_size` | function | `utils.py:1972` | `def get_terminal_size()` |
| `get_users_dic` | function | `utils.py:1844` | `def get_users_dic(txt)` |
| `get_venv_info` | function | `utils.py:704` | `def get_venv_info()` |
| `get_xml` | function | `utils.py:2072` | `def get_xml(directory)` |
| `getprompt` | function | `utils.py:725` | `def getprompt()` |
| `halp` | function | `utils.py:1981` | `def halp()` |
| `handle` | function | `utils.py:1814` | `def handle(input_str)` |
| `handle_forms` | function | `utils.py:1702` | `def handle_forms(content, url)` |
| `htmlify` | function | `utils.py:2597` | `def htmlify(data)` |
| `inject_payloads` | function | `utils.py:1640` | `def inject_payloads(urls, payload_url, request_timeout)` |
| `is_digit` | function | `utils.py:1920` | `def is_digit(the_digit)` |
| `is_exist` | function | `utils.py:1174` | `def is_exist(file)` |
| `is_package_installed` | function | `utils.py:1475` | `def is_package_installed(package_name)` |
| `is_port_in_use` | function | `utils.py:2620` | `def is_port_in_use(port, host)` |
| `list_binaries` | function | `utils.py:2157` | `def list_binaries(directory)` |
| `load_adversary` | function | `utils.py:2679` | `def load_adversary()` |
| `load_knowledge_base` | function | `utils.py:3050` | `def load_knowledge_base(knowledge_file)` |
| `load_user_aliases` | function | `utils.py:3087` | `def load_user_aliases()` |
| `load_version` | function | `utils.py:471` | `def load_version()` |
| `log_message` | method | `utils.py:3115` | `def log_message(self)` |
| `log_request` | method | `utils.py:3112` | `def log_request(self)` |
| `manual_yaml_extraction` | function | `utils.py:2793` | `def manual_yaml_extraction(content)` |
| `needs_sudo` | function | `utils.py:323` | `def needs_sudo(command)` |
| `nvddb` | function | `utils.py:925` | `def nvddb(content)` |
| `obfuscate_payload` | function | `utils.py:1593` | `def obfuscate_payload(payload)` |
| `open_file` | method | `utils.py:3143` | `def open_file(self, filename)` |
| `open_reader` | method | `utils.py:3148` | `def open_reader(self, reader)` |
| `packetstormsecurity` | function | `utils.py:887` | `def packetstormsecurity(content)` |
| `parse_bool` | function | `utils.py:497` | `def parse_bool(value)` |
| `parse_ip_mac` | function | `utils.py:396` | `def parse_ip_mac(input_string)` |
| `parse_nmap_csv` | function | `utils.py:2729` | `def parse_nmap_csv(csv_path)` |
| `parse_proc_net_file` | function | `utils.py:565` | `def parse_proc_net_file(file_path)` |
| `parse_yaml_response` | function | `utils.py:2932` | `def parse_yaml_response(content)` |
| `persist` | method | `utils.py:3340` | `def persist(self, service, target, cves)` |
| `preprocess_llm_response` | function | `utils.py:2758` | `def preprocess_llm_response(response)` |
| `pretty_print` | method | `utils.py:3377` | `def pretty_print(self, cves_details)` |
| `prompt` | function | `utils.py:1740` | `def prompt(label, default)` |
| `query_arin_ip` | function | `utils.py:2643` | `def query_arin_ip(ip)` |
| `query_ollama` | function | `utils.py:2743` | `def query_ollama(prompt, model)` |
| `random_string` | function | `utils.py:1382` | `def random_string(length)` |
| `read_payloads` | function | `utils.py:1618` | `def read_payloads(file_path)` |
| `redact_secrets` | function | `utils.py:376` | `def redact_secrets(text)` |
| `replace_command_placeholders` | function | `utils.py:2703` | `def replace_command_placeholders(command, params)` |
| `replace_match` | function | `utils.py:2721` | `def replace_match(match)` |
| `replace_placeholders` | function | `utils.py:2685` | `def replace_placeholders(template, replacements)` |
| `replace_variables` | function | `utils.py:2382` | `def replace_variables(command, variables)` |
| `return_creds` | function | `utils.py:2629` | `def return_creds()` |
| `rotate_char` | function | `utils.py:628` | `def rotate_char(c, shift)` |
| `run` | function | `utils.py:1115` | `def run(command)` |
| `salida_strace` | function | `utils.py:812` | `def salida_strace(filename)` |
| `save_playbook` | function | `utils.py:3038` | `def save_playbook(playbook_data, playbook_name)` |
| `scrape_news` | function | `utils.py:2548` | `def scrape_news()` |
| `search_cves` | method | `utils.py:3270` | `def search_cves(self, service)` |
| `select_binary` | function | `utils.py:2177` | `def select_binary(binaries)` |
| `send_command` | function | `utils.py:2231` | `def send_command(cmd, url, lhost)` |
| `send_packet` | function | `utils.py:453` | `def send_packet(packet, iface)` |
| `send_request` | function | `utils.py:1665` | `def send_request(raw_url)` |
| `shellcode_to_sylk` | function | `utils.py:2115` | `def shellcode_to_sylk(shellcode_path)` |
| `signal_handler` | function | `utils.py:515` | `def signal_handler(sig, frame)` |
| `sudo_available` | function | `utils.py:347` | `def sudo_available()` |
| `teclado_usuario` | function | `utils.py:776` | `def teclado_usuario(filename)` |
| `transform` | function | `utils.py:1784` | `def transform(parts, delimiter, casing)` |

