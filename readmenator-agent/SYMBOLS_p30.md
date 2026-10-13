# Symbols (page 30 of 40)
Previous: [SYMBOLS_p29.md](SYMBOLS_p29.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_graph_provider_returns_none_when_advisor_empty` | function | `tests/test_autosuggest.py:232` | `def test_graph_provider_returns_none_when_advisor_empty()` |
| `test_graph_provider_returns_top_result` | function | `tests/test_autosuggest.py:215` | `def test_graph_provider_returns_top_result()` |
| `test_graph_provider_skips_when_last_command_blank` | function | `tests/test_autosuggest.py:239` | `def test_graph_provider_skips_when_last_command_blank()` |
| `test_killchain_provider_falls_back_to_phase_priority` | function | `tests/test_autosuggest.py:184` | `def test_killchain_provider_falls_back_to_phase_priority()` |
| `test_killchain_provider_returns_none_with_nothing_to_offer` | function | `tests/test_autosuggest.py:197` | `def test_killchain_provider_returns_none_with_nothing_to_offer()` |
| `test_killchain_provider_skips_already_executed` | function | `tests/test_autosuggest.py:169` | `def test_killchain_provider_skips_already_executed()` |
| `test_killchain_provider_uses_adjacency` | function | `tests/test_autosuggest.py:158` | `def test_killchain_provider_uses_adjacency()` |
| `test_render_hint_line_emits_to_console` | function | `tests/test_autosuggest.py:303` | `def test_render_hint_line_emits_to_console()` |
| `test_render_hint_line_is_noop_when_disabled` | function | `tests/test_autosuggest.py:325` | `def test_render_hint_line_is_noop_when_disabled()` |
| `test_render_hint_line_is_noop_without_suggestion` | function | `tests/test_autosuggest.py:315` | `def test_render_hint_line_is_noop_without_suggestion()` |
| `_FakeResp` | class | `tests/test_banner_config.py:281` | `class _FakeResp` |
| `__enter__` | method | `tests/test_banner_config.py:282` | `def __enter__(self)` |
| `__exit__` | method | `tests/test_banner_config.py:285` | `def __exit__(self)` |
| `_make_ctx` | function | `tests/test_banner_config.py:150` | `def _make_ctx(palette)` |
| `color_registry` | function | `tests/test_banner_config.py:42` | `def color_registry()` |
| `glyph_registry` | function | `tests/test_banner_config.py:47` | `def glyph_registry()` |
| `neutral_palette` | function | `tests/test_banner_config.py:52` | `def neutral_palette()` |
| `read` | method | `tests/test_banner_config.py:288` | `def read(self)` |
| `registry` | function | `tests/test_banner_config.py:37` | `def registry()` |
| `test_banner_summary_handles_empty` | function | `tests/test_banner_config.py:254` | `def test_banner_summary_handles_empty()` |
| `test_banner_summary_lists_enabled_ids_sorted` | function | `tests/test_banner_config.py:248` | `def test_banner_summary_lists_enabled_ids_sorted()` |
| `test_color_registry_cycle_wraps_around` | function | `tests/test_banner_config.py:327` | `def test_color_registry_cycle_wraps_around(color_registry)` |
| `test_color_registry_exposes_named_palette` | function | `tests/test_banner_config.py:320` | `def test_color_registry_exposes_named_palette(color_registry)` |
| `test_color_registry_resolve_unknown_falls_back` | function | `tests/test_banner_config.py:335` | `def test_color_registry_resolve_unknown_falls_back(color_registry)` |
| `test_configurator_returns_none_in_non_tty_environment` | function | `tests/test_banner_config.py:303` | `def test_configurator_returns_none_in_non_tty_environment(monkeypatch, registry, neutral_palette, color_registry...` |
| `test_context_resolver_public_ip_caches_within_ttl` | function | `tests/test_banner_config.py:275` | `def test_context_resolver_public_ip_caches_within_ttl(neutral_palette)` |
| `test_context_resolver_uses_payload_rhost_and_lhost` | function | `tests/test_banner_config.py:261` | `def test_context_resolver_uses_payload_rhost_and_lhost(neutral_palette)` |
| `test_glyph_registry_cycle_preserves_unknown_value` | function | `tests/test_banner_config.py:357` | `def test_glyph_registry_cycle_preserves_unknown_value(glyph_registry)` |
| `test_glyph_registry_cycle_returns_known_choice` | function | `tests/test_banner_config.py:350` | `def test_glyph_registry_cycle_returns_known_choice(glyph_registry)` |
| `test_glyph_registry_exposes_canonical_slots` | function | `tests/test_banner_config.py:344` | `def test_glyph_registry_exposes_canonical_slots(glyph_registry)` |
| `test_registry_group_partition` | function | `tests/test_banner_config.py:88` | `def test_registry_group_partition(registry)` |
| `test_registry_lists_every_canonical_segment` | function | `tests/test_banner_config.py:68` | `def test_registry_lists_every_canonical_segment(registry)` |
| `test_registry_lookup_returns_none_for_unknown` | function | `tests/test_banner_config.py:96` | `def test_registry_lookup_returns_none_for_unknown(registry)` |
| `test_render_prompt_honours_payload_colors_and_glyphs` | function | `tests/test_banner_config.py:458` | `def test_render_prompt_honours_payload_colors_and_glyphs()` |
| `test_render_prompt_uses_payload_banner_block` | function | `tests/test_banner_config.py:228` | `def test_render_prompt_uses_payload_banner_block()` |
| `test_render_prompt_with_no_payload_uses_defaults` | function | `tests/test_banner_config.py:239` | `def test_render_prompt_with_no_payload_uses_defaults()` |
| `test_renderer_drops_empty_value_segments` | function | `tests/test_banner_config.py:206` | `def test_renderer_drops_empty_value_segments(registry, neutral_palette)` |
| `test_renderer_emits_chosen_color_for_each_segment` | function | `tests/test_banner_config.py:418` | `def test_renderer_emits_chosen_color_for_each_segment(registry, color_registry, glyph_registry, neutral_palette)` |
| `test_renderer_emits_three_lines_with_box_corners` | function | `tests/test_banner_config.py:176` | `def test_renderer_emits_three_lines_with_box_corners(registry, neutral_palette)` |
| `test_renderer_includes_kernel_and_version_when_enabled` | function | `tests/test_banner_config.py:198` | `def test_renderer_includes_kernel_and_version_when_enabled(registry, neutral_palette)` |
| `test_renderer_marks_dirty_git_with_dirty_glyph` | function | `tests/test_banner_config.py:214` | `def test_renderer_marks_dirty_git_with_dirty_glyph(registry, neutral_palette)` |
| `test_renderer_omits_disabled_segments` | function | `tests/test_banner_config.py:187` | `def test_renderer_omits_disabled_segments(registry, neutral_palette)` |
| `test_renderer_uses_glyph_overrides_in_box` | function | `tests/test_banner_config.py:438` | `def test_renderer_uses_glyph_overrides_in_box(registry, color_registry, glyph_registry, neutral_palette)` |
| `test_settings_cycle_color_uses_registry_order` | function | `tests/test_banner_config.py:391` | `def test_settings_cycle_color_uses_registry_order(registry, color_registry)` |
| `test_settings_cycle_glyph_uses_registry_order` | function | `tests/test_banner_config.py:398` | `def test_settings_cycle_glyph_uses_registry_order(registry, color_registry, glyph_registry)` |
| `test_settings_defaults_match_registry_defaults` | function | `tests/test_banner_config.py:103` | `def test_settings_defaults_match_registry_defaults(registry)` |
| `test_settings_enable_all_then_disable_all` | function | `tests/test_banner_config.py:139` | `def test_settings_enable_all_then_disable_all(registry)` |
| `test_settings_from_payload_falls_back_to_defaults_when_missing` | function | `tests/test_banner_config.py:120` | `def test_settings_from_payload_falls_back_to_defaults_when_missing(registry)` |
| `test_settings_from_payload_ignores_unknown_color_names` | function | `tests/test_banner_config.py:379` | `def test_settings_from_payload_ignores_unknown_color_names(registry, color_registry, glyph_registry)` |
| `test_settings_from_payload_ignores_unknown_glyph_chars` | function | `tests/test_banner_config.py:385` | `def test_settings_from_payload_ignores_unknown_glyph_chars(registry, color_registry, glyph_registry)` |
| `test_settings_from_payload_ignores_unknown_ids` | function | `tests/test_banner_config.py:125` | `def test_settings_from_payload_ignores_unknown_ids(registry)` |
| `test_settings_reset_color_and_glyph_for_specific_id` | function | `tests/test_banner_config.py:405` | `def test_settings_reset_color_and_glyph_for_specific_id(registry, color_registry, glyph_registry)` |
| `test_settings_round_trip_carries_colors_and_glyphs` | function | `tests/test_banner_config.py:364` | `def test_settings_round_trip_carries_colors_and_glyphs(registry, color_registry, glyph_registry)` |
| `test_settings_round_trip_through_payload_block` | function | `tests/test_banner_config.py:113` | `def test_settings_round_trip_through_payload_block(registry)` |
| `test_settings_toggle_adds_then_removes` | function | `tests/test_banner_config.py:131` | `def test_settings_toggle_adds_then_removes()` |
| `Completed` | class | `tests/test_bdd_infra_range_report.py:28` | `class Completed` |
| `test_bdd_beacon_build_injects_fallback_urls` | function | `tests/test_bdd_infra_range_report.py:51` | `def test_bdd_beacon_build_injects_fallback_urls()` |
| `test_bdd_range_compose_topology` | function | `tests/test_bdd_infra_range_report.py:65` | `def test_bdd_range_compose_topology()` |
| `test_bdd_redirector_spawn_registers_urls` | function | `tests/test_bdd_infra_range_report.py:15` | `def test_bdd_redirector_spawn_registers_urls()` |
| `test_bdd_report_executive_summary_without_ai` | function | `tests/test_bdd_infra_range_report.py:83` | `def test_bdd_report_executive_summary_without_ai()` |
| `TestBeaconConfig` | class | `tests/test_beacon_config_builder.py:22` | `class TestBeaconConfig` |
| `TestBeaconConfigBuilder` | class | `tests/test_beacon_config_builder.py:141` | `class TestBeaconConfigBuilder` |
| `TestGenerateBofExecutionCommand` | class | `tests/test_beacon_config_builder.py:205` | `class TestGenerateBofExecutionCommand` |
| `test_basic_bof_command` | method | `tests/test_beacon_config_builder.py:206` | `def test_basic_bof_command(self)` |
| `test_bof_with_args` | method | `tests/test_beacon_config_builder.py:214` | `def test_bof_with_args(self)` |
| `test_build_falls_back_on_missing_engines` | method | `tests/test_beacon_config_builder.py:197` | `def test_build_falls_back_on_missing_engines(self)` |
| `test_build_injects_dns_from_payload` | method | `tests/test_beacon_config_builder.py:183` | `def test_build_injects_dns_from_payload(self)` |
| `test_build_injects_tls_from_payload` | method | `tests/test_beacon_config_builder.py:170` | `def test_build_injects_tls_from_payload(self)` |
| `test_build_minimal` | method | `tests/test_beacon_config_builder.py:142` | `def test_build_minimal(self)` |
| `test_build_with_malleable_route` | method | `tests/test_beacon_config_builder.py:157` | `def test_build_with_malleable_route(self)` |
| `test_custom_bofs_dir` | method | `tests/test_beacon_config_builder.py:224` | `def test_custom_bofs_dir(self)` |
| `test_default_construction` | method | `tests/test_beacon_config_builder.py:23` | `def test_default_construction(self)` |
| `test_to_config_json` | method | `tests/test_beacon_config_builder.py:85` | `def test_to_config_json(self)` |
| `test_to_dict_serialization` | method | `tests/test_beacon_config_builder.py:113` | `def test_to_dict_serialization(self)` |
| `test_to_gen_beacon_args` | method | `tests/test_beacon_config_builder.py:36` | `def test_to_gen_beacon_args(self)` |
| `test_to_go_implant_vars` | method | `tests/test_beacon_config_builder.py:59` | `def test_to_go_implant_vars(self)` |
| `TestAppendRead` | class | `tests/test_beacon_history.py:38` | `class TestAppendRead` |
| `TestSanitization` | class | `tests/test_beacon_history.py:23` | `class TestSanitization` |
| `_config` | function | `tests/test_beacon_history.py:19` | `def _config(tmp_path)` |
| `test_append_then_read_round_trips` | method | `tests/test_beacon_history.py:39` | `def test_append_then_read_round_trips(self, tmp_path)` |
| `test_missing_history_reads_empty` | method | `tests/test_beacon_history.py:72` | `def test_missing_history_reads_empty(self, tmp_path)` |
| `test_multiple_beacons_do_not_interleave` | method | `tests/test_beacon_history.py:50` | `def test_multiple_beacons_do_not_interleave(self, tmp_path)` |
| `test_record_without_client_id_is_rejected` | method | `tests/test_beacon_history.py:75` | `def test_record_without_client_id_is_rejected(self, tmp_path)` |
| `test_records_path_is_bounded_inside_sessions` | method | `tests/test_beacon_history.py:29` | `def test_records_path_is_bounded_inside_sessions(self, tmp_path)` |
| `test_sanitize_client_id_strips_unsafe_chars` | method | `tests/test_beacon_history.py:24` | `def test_sanitize_client_id_strips_unsafe_chars(self)` |
| `test_skips_malformed_lines` | method | `tests/test_beacon_history.py:59` | `def test_skips_malformed_lines(self, tmp_path)` |
| `TestBeaconCategory` | class | `tests/test_blacksandbeacon_addon.py:111` | `class TestBeaconCategory` |
| `TestBeaconCommandTemplates` | class | `tests/test_blacksandbeacon_addon.py:157` | `class TestBeaconCommandTemplates` |
| `TestBeaconDescriptionQuality` | class | `tests/test_blacksandbeacon_addon.py:192` | `class TestBeaconDescriptionQuality` |
| `TestBeaconEnabled` | class | `tests/test_blacksandbeacon_addon.py:119` | `class TestBeaconEnabled` |
| `TestBeaconNoHardcodedSecrets` | class | `tests/test_blacksandbeacon_addon.py:217` | `class TestBeaconNoHardcodedSecrets` |
| `TestBeaconParams` | class | `tests/test_blacksandbeacon_addon.py:127` | `class TestBeaconParams` |
| `TestBeaconPathSafety` | class | `tests/test_blacksandbeacon_addon.py:97` | `class TestBeaconPathSafety` |
| `TestBeaconRequiredFields` | class | `tests/test_blacksandbeacon_addon.py:55` | `class TestBeaconRequiredFields` |
| `TestBeaconToolSection` | class | `tests/test_blacksandbeacon_addon.py:67` | `class TestBeaconToolSection` |
| `TestBeaconYamlExists` | class | `tests/test_blacksandbeacon_addon.py:41` | `class TestBeaconYamlExists` |
| `_load` | function | `tests/test_blacksandbeacon_addon.py:26` | `def _load(path)` |
| `_param_names` | method | `tests/test_blacksandbeacon_addon.py:130` | `def _param_names(self, addon)` |
| `_yaml_text` | method | `tests/test_blacksandbeacon_addon.py:220` | `def _yaml_text(self, path)` |
| `beacon` | function | `tests/test_blacksandbeacon_addon.py:32` | `def beacon()` |
| `bof` | function | `tests/test_blacksandbeacon_addon.py:37` | `def bof()` |
| `test_beacon_category` | method | `tests/test_blacksandbeacon_addon.py:112` | `def test_beacon_category(self, beacon)` |
| `test_beacon_description_mentions_bof` | method | `tests/test_blacksandbeacon_addon.py:195` | `def test_beacon_description_mentions_bof(self, beacon)` |
| `test_beacon_description_mentions_linux` | method | `tests/test_blacksandbeacon_addon.py:199` | `def test_beacon_description_mentions_linux(self, beacon)` |
| `test_beacon_enabled` | method | `tests/test_blacksandbeacon_addon.py:120` | `def test_beacon_enabled(self, beacon)` |
| `test_beacon_execute_resets_before_pull` | method | `tests/test_blacksandbeacon_addon.py:183` | `def test_beacon_execute_resets_before_pull(self, beacon)` |
| `test_beacon_execute_stages_to_sessions` | method | `tests/test_blacksandbeacon_addon.py:176` | `def test_beacon_execute_stages_to_sessions(self, beacon)` |
| `test_beacon_has_c2_port_param` | method | `tests/test_blacksandbeacon_addon.py:139` | `def test_beacon_has_c2_port_param(self, beacon)` |
| `test_beacon_has_field` | method | `tests/test_blacksandbeacon_addon.py:59` | `def test_beacon_has_field(self, beacon, field)` |
| `test_beacon_has_lhost_param` | method | `tests/test_blacksandbeacon_addon.py:133` | `def test_beacon_has_lhost_param(self, beacon)` |
| `test_beacon_has_lport_param` | method | `tests/test_blacksandbeacon_addon.py:136` | `def test_beacon_has_lport_param(self, beacon)` |
| `test_beacon_install_command_is_make` | method | `tests/test_blacksandbeacon_addon.py:90` | `def test_beacon_install_command_is_make(self, beacon)` |
| `test_beacon_install_path` | method | `tests/test_blacksandbeacon_addon.py:84` | `def test_beacon_install_path(self, beacon)` |
| `test_beacon_install_path_no_traversal` | method | `tests/test_blacksandbeacon_addon.py:100` | `def test_beacon_install_path_no_traversal(self, beacon)` |
| `test_beacon_lazycommand_has_c2_port` | method | `tests/test_blacksandbeacon_addon.py:164` | `def test_beacon_lazycommand_has_c2_port(self, beacon)` |
| `test_beacon_lazycommand_has_lhost` | method | `tests/test_blacksandbeacon_addon.py:160` | `def test_beacon_lazycommand_has_lhost(self, beacon)` |
| `test_beacon_lhost_required` | method | `tests/test_blacksandbeacon_addon.py:148` | `def test_beacon_lhost_required(self, beacon)` |
| `test_beacon_name_is_correct` | method | `tests/test_blacksandbeacon_addon.py:210` | `def test_beacon_name_is_correct(self, beacon)` |
| `test_beacon_no_hardcoded_ip` | method | `tests/test_blacksandbeacon_addon.py:223` | `def test_beacon_no_hardcoded_ip(self)` |
| `test_beacon_no_hardcoded_port_numbers` | method | `tests/test_blacksandbeacon_addon.py:237` | `def test_beacon_no_hardcoded_port_numbers(self)` |
| `test_beacon_repo_url` | method | `tests/test_blacksandbeacon_addon.py:78` | `def test_beacon_repo_url(self, beacon)` |
| `test_beacon_tool_has_key` | method | `tests/test_blacksandbeacon_addon.py:71` | `def test_beacon_tool_has_key(self, beacon, key)` |
| `test_beacon_yaml_parses` | method | `tests/test_blacksandbeacon_addon.py:48` | `def test_beacon_yaml_parses(self, beacon)` |
| `test_beacon_yaml_present` | method | `tests/test_blacksandbeacon_addon.py:42` | `def test_beacon_yaml_present(self)` |
| `test_bof_category` | method | `tests/test_blacksandbeacon_addon.py:115` | `def test_bof_category(self, bof)` |
| `test_bof_description_mentions_elf` | method | `tests/test_blacksandbeacon_addon.py:206` | `def test_bof_description_mentions_elf(self, bof)` |
| `test_bof_description_mentions_linux_bof` | method | `tests/test_blacksandbeacon_addon.py:202` | `def test_bof_description_mentions_linux_bof(self, bof)` |
| `test_bof_enabled` | method | `tests/test_blacksandbeacon_addon.py:123` | `def test_bof_enabled(self, bof)` |
| `test_bof_execute_resets_before_pull` | method | `tests/test_blacksandbeacon_addon.py:187` | `def test_bof_execute_resets_before_pull(self, bof)` |
| `test_bof_execute_stages_to_sessions` | method | `tests/test_blacksandbeacon_addon.py:180` | `def test_bof_execute_stages_to_sessions(self, bof)` |
| `test_bof_has_field` | method | `tests/test_blacksandbeacon_addon.py:63` | `def test_bof_has_field(self, bof, field)` |
| `test_bof_has_lhost_param` | method | `tests/test_blacksandbeacon_addon.py:142` | `def test_bof_has_lhost_param(self, bof)` |
| `test_bof_has_lport_param` | method | `tests/test_blacksandbeacon_addon.py:145` | `def test_bof_has_lport_param(self, bof)` |
| `test_bof_install_command_is_make` | method | `tests/test_blacksandbeacon_addon.py:93` | `def test_bof_install_command_is_make(self, bof)` |
| `test_bof_install_path` | method | `tests/test_blacksandbeacon_addon.py:87` | `def test_bof_install_path(self, bof)` |
| `test_bof_install_path_no_traversal` | method | `tests/test_blacksandbeacon_addon.py:105` | `def test_bof_install_path_no_traversal(self, bof)` |
| `test_bof_lazycommand_has_lhost` | method | `tests/test_blacksandbeacon_addon.py:168` | `def test_bof_lazycommand_has_lhost(self, bof)` |
| `test_bof_lazycommand_has_lport` | method | `tests/test_blacksandbeacon_addon.py:172` | `def test_bof_lazycommand_has_lport(self, bof)` |
| `test_bof_lhost_required` | method | `tests/test_blacksandbeacon_addon.py:152` | `def test_bof_lhost_required(self, bof)` |
| `test_bof_name_is_correct` | method | `tests/test_blacksandbeacon_addon.py:213` | `def test_bof_name_is_correct(self, bof)` |
| `test_bof_no_hardcoded_ip` | method | `tests/test_blacksandbeacon_addon.py:230` | `def test_bof_no_hardcoded_ip(self)` |
| `test_bof_no_hardcoded_port_numbers` | method | `tests/test_blacksandbeacon_addon.py:241` | `def test_bof_no_hardcoded_port_numbers(self)` |
| `test_bof_repo_url` | method | `tests/test_blacksandbeacon_addon.py:81` | `def test_bof_repo_url(self, bof)` |
| `test_bof_tool_has_key` | method | `tests/test_blacksandbeacon_addon.py:75` | `def test_bof_tool_has_key(self, bof, key)` |
| `test_bof_yaml_parses` | method | `tests/test_blacksandbeacon_addon.py:51` | `def test_bof_yaml_parses(self, bof)` |
| `test_bof_yaml_present` | method | `tests/test_blacksandbeacon_addon.py:45` | `def test_bof_yaml_present(self)` |
| `TestBofCatalog` | class | `tests/test_bof_registry.py:101` | `class TestBofCatalog` |
| `TestBofEntry` | class | `tests/test_bof_registry.py:47` | `class TestBofEntry` |
| `TestBofEnums` | class | `tests/test_bof_registry.py:359` | `class TestBofEnums` |
| `TestBofMarketplace` | class | `tests/test_bof_registry.py:291` | `class TestBofMarketplace` |
| `TestBofRegistry` | class | `tests/test_bof_registry.py:174` | `class TestBofRegistry` |
| `TestBofValidator` | class | `tests/test_bof_registry.py:221` | `class TestBofValidator` |
| `catalog` | function | `tests/test_bof_registry.py:37` | `def catalog()` |
| `test_bulk_install` | method | `tests/test_bof_registry.py:352` | `def test_bulk_install(self, tmp_sessions)` |
| `test_category_values` | method | `tests/test_bof_registry.py:364` | `def test_category_values(self)` |
| `test_compute_sha256_deterministic` | method | `tests/test_bof_registry.py:230` | `def test_compute_sha256_deterministic(self, tmp_sessions)` |
| `test_construction_and_properties` | method | `tests/test_bof_registry.py:48` | `def test_construction_and_properties(self)` |
| `test_empty_catalog` | method | `tests/test_bof_registry.py:158` | `def test_empty_catalog(self)` |
| `test_from_dict_minimal` | method | `tests/test_bof_registry.py:91` | `def test_from_dict_minimal(self)` |
| `test_get_install_info` | method | `tests/test_bof_registry.py:201` | `def test_get_install_info(self, tmp_sessions)` |
| `test_get_install_info_nonexistent` | method | `tests/test_bof_registry.py:209` | `def test_get_install_info_nonexistent(self, tmp_sessions)` |
| `test_get_missing_raises_keyerror` | method | `tests/test_bof_registry.py:107` | `def test_get_missing_raises_keyerror(self, catalog)` |
| `test_immutability` | method | `tests/test_bof_registry.py:65` | `def test_immutability(self)` |
| `test_info_missing_bof` | method | `tests/test_bof_registry.py:306` | `def test_info_missing_bof(self)` |
| `test_info_returns_catalog_and_install_state` | method | `tests/test_bof_registry.py:299` | `def test_info_returns_catalog_and_install_state(self, tmp_sessions)` |
| `test_install_already_installed` | method | `tests/test_bof_registry.py:321` | `def test_install_already_installed(self, tmp_sessions)` |
| `test_install_and_check` | method | `tests/test_bof_registry.py:175` | `def test_install_and_check(self, tmp_sessions)` |
| `test_install_and_uninstall` | method | `tests/test_bof_registry.py:311` | `def test_install_and_uninstall(self, tmp_sessions)` |
| `test_install_missing_bof` | method | `tests/test_bof_registry.py:327` | `def test_install_missing_bof(self)` |
| `test_list_all_sorted` | method | `tests/test_bof_registry.py:131` | `def test_list_all_sorted(self, catalog)` |
| `test_list_by_category` | method | `tests/test_bof_registry.py:141` | `def test_list_by_category(self, catalog)` |
| `test_list_by_platform` | method | `tests/test_bof_registry.py:136` | `def test_list_by_platform(self, catalog)` |
| `test_list_installed` | method | `tests/test_bof_registry.py:193` | `def test_list_installed(self, tmp_sessions)` |
| `test_list_installed_empty_initially` | method | `tests/test_bof_registry.py:337` | `def test_list_installed_empty_initially(self, tmp_sessions)` |
| `test_list_missing_dependencies` | method | `tests/test_bof_registry.py:342` | `def test_list_missing_dependencies(self, tmp_sessions)` |
| `test_list_missing_dependencies_unknown_bof` | method | `tests/test_bof_registry.py:347` | `def test_list_missing_dependencies_unknown_bof(self)` |
| `test_load_missing_file_returns_empty` | method | `tests/test_bof_registry.py:153` | `def test_load_missing_file_returns_empty(self, tmp_sessions)` |
| `test_manifest_persistence` | method | `tests/test_bof_registry.py:213` | `def test_manifest_persistence(self, tmp_sessions)` |
| `test_platform_values` | method | `tests/test_bof_registry.py:360` | `def test_platform_values(self)` |
| `test_register_and_get` | method | `tests/test_bof_registry.py:102` | `def test_register_and_get(self, catalog)` |
| `test_register_overwrites` | method | `tests/test_bof_registry.py:165` | `def test_register_overwrites(self)` |
| `test_save_load_roundtrip` | method | `tests/test_bof_registry.py:147` | `def test_save_load_roundtrip(self, catalog, tmp_sessions)` |
| `test_search_by_category` | method | `tests/test_bof_registry.py:116` | `def test_search_by_category(self, catalog)` |
| `test_search_by_technique` | method | `tests/test_bof_registry.py:121` | `def test_search_by_technique(self, catalog)` |
| `test_search_empty_query_returns_all` | method | `tests/test_bof_registry.py:127` | `def test_search_empty_query_returns_all(self, catalog)` |
| `test_search_enriches_with_install_status` | method | `tests/test_bof_registry.py:292` | `def test_search_enriches_with_install_status(self, tmp_sessions)` |
| `test_search_exact_match` | method | `tests/test_bof_registry.py:111` | `def test_search_exact_match(self, catalog)` |
| `test_to_dict_roundtrip` | method | `tests/test_bof_registry.py:70` | `def test_to_dict_roundtrip(self)` |
| `test_uninstall` | method | `tests/test_bof_registry.py:182` | `def test_uninstall(self, tmp_sessions)` |
| `test_uninstall_missing_bof` | method | `tests/test_bof_registry.py:332` | `def test_uninstall_missing_bof(self, tmp_sessions)` |
| `test_uninstall_nonexistent` | method | `tests/test_bof_registry.py:189` | `def test_uninstall_nonexistent(self, tmp_sessions)` |
| `test_validate_args_all_present` | method | `tests/test_bof_registry.py:266` | `def test_validate_args_all_present(self)` |
| `test_validate_args_missing_required` | method | `tests/test_bof_registry.py:253` | `def test_validate_args_missing_required(self)` |
| `test_validate_args_no_required` | method | `tests/test_bof_registry.py:278` | `def test_validate_args_no_required(self)` |
| `test_verify_mismatched_hash` | method | `tests/test_bof_registry.py:238` | `def test_verify_mismatched_hash(self, tmp_sessions)` |
| `test_verify_with_empty_hash_skips` | method | `tests/test_bof_registry.py:222` | `def test_verify_with_empty_hash_skips(self, tmp_sessions)` |
| `tmp_sessions` | function | `tests/test_bof_registry.py:42` | `def tmp_sessions()` |
| `_git` | function | `tests/test_bootstrap_installer.py:44` | `def _git(args, cwd)` |
| `_make_stub_repo` | function | `tests/test_bootstrap_installer.py:105` | `def _make_stub_repo(path)` |
| `_run_bootstrap` | function | `tests/test_bootstrap_installer.py:29` | `def _run_bootstrap(args, env, cwd)` |
| `test_bootstrap_help_lists_options` | function | `tests/test_bootstrap_installer.py:55` | `def test_bootstrap_help_lists_options()` |
| `test_bootstrap_rejects_bad_modes` | function | `tests/test_bootstrap_installer.py:75` | `def test_bootstrap_rejects_bad_modes()` |
| `test_bootstrap_rejects_unknown_flag` | function | `tests/test_bootstrap_installer.py:63` | `def test_bootstrap_rejects_unknown_flag()` |
| `test_debug_flag_traces_execution` | function | `tests/test_bootstrap_installer.py:138` | `def test_debug_flag_traces_execution(tmp_path)` |
| `test_existing_checkout_abort_changes_nothing` | function | `tests/test_bootstrap_installer.py:118` | `def test_existing_checkout_abort_changes_nothing(tmp_path)` |
| `test_existing_checkout_clean_backs_up_payload` | function | `tests/test_bootstrap_installer.py:170` | `def test_existing_checkout_clean_backs_up_payload(tmp_path)` |
| `test_existing_checkout_update_reinstalls` | function | `tests/test_bootstrap_installer.py:153` | `def test_existing_checkout_update_reinstalls(tmp_path)` |
| `test_install_pipe_guard` | function | `tests/test_bootstrap_installer.py:88` | `def test_install_pipe_guard(tmp_path)` |
| `test_install_uses_supported_pip_flags` | function | `tests/test_bootstrap_installer.py:208` | `def test_install_uses_supported_pip_flags()` |
| `test_non_checkout_path_fails_without_tty` | function | `tests/test_bootstrap_installer.py:195` | `def test_non_checkout_path_fails_without_tty(tmp_path)` |
| `test_scripts_are_executable_and_clean` | function | `tests/test_bootstrap_installer.py:220` | `def test_scripts_are_executable_and_clean()` |
| `Server` | class | `tests/test_boyscout_contracts.py:83` | `class Server` |
| `TextContent` | class | `tests/test_boyscout_contracts.py:73` | `class TextContent` |
| `Tool` | class | `tests/test_boyscout_contracts.py:66` | `class Tool` |
| `__init__` | method | `tests/test_boyscout_contracts.py:69` | `def __init__(self)` |
| `__init__` | method | `tests/test_boyscout_contracts.py:76` | `def __init__(self)` |
| `__init__` | method | `tests/test_boyscout_contracts.py:86` | `def __init__(self)` |
| `_bound_import_names` | function | `tests/test_boyscout_contracts.py:27` | `def _bound_import_names(tree)` |
| `_load_mcp_module` | function | `tests/test_boyscout_contracts.py:52` | `def _load_mcp_module()` |
| `call_tool` | method | `tests/test_boyscout_contracts.py:93` | `def call_tool(self)` |
| `list_tools` | method | `tests/test_boyscout_contracts.py:89` | `def list_tools(self)` |
| `test_deploy_has_no_todo_markers` | function | `tests/test_boyscout_contracts.py:141` | `def test_deploy_has_no_todo_markers()` |
| `test_lazyown_has_no_unused_imports` | function | `tests/test_boyscout_contracts.py:42` | `def test_lazyown_has_no_unused_imports()` |
| `test_playbook_target_is_shell_quoted` | function | `tests/test_boyscout_contracts.py:110` | `def test_playbook_target_is_shell_quoted()` |
| `test_replace_placeholders_keeps_brace_values_literal` | function | `tests/test_boyscout_contracts.py:133` | `def test_replace_placeholders_keeps_brace_values_literal()` |
| `test_replace_placeholders_matches_single_pass_engine` | function | `tests/test_boyscout_contracts.py:119` | `def test_replace_placeholders_matches_single_pass_engine()` |
| `TestBridgeCatalogToolFunction` | class | `tests/test_bridge_catalog_filtered.py:111` | `class TestBridgeCatalogToolFunction` |
| `TestCatalogSummaryFiltered` | class | `tests/test_bridge_catalog_filtered.py:32` | `class TestCatalogSummaryFiltered` |
| `_entries_for` | method | `tests/test_bridge_catalog_filtered.py:48` | `def _entries_for(self, dispatcher, phase, command_name)` |
| `dispatcher` | function | `tests/test_bridge_catalog_filtered.py:26` | `def dispatcher()` |
| `test_empty_phase_keeps_all_phases` | method | `tests/test_bridge_catalog_filtered.py:89` | `def test_empty_phase_keeps_all_phases(self, dispatcher)` |
| `test_no_args_matches_unfiltered_summary` | method | `tests/test_bridge_catalog_filtered.py:33` | `def test_no_args_matches_unfiltered_summary(self, dispatcher)` |
| `test_no_args_returns_full_catalog_header` | method | `tests/test_bridge_catalog_filtered.py:112` | `def test_no_args_returns_full_catalog_header(self)` |
| `test_os_filter_shrinks_or_preserves_each_phase` | method | `tests/test_bridge_catalog_filtered.py:71` | `def test_os_filter_shrinks_or_preserves_each_phase(self, dispatcher)` |
| `test_os_hint_any_is_passthrough` | method | `tests/test_bridge_catalog_filtered.py:100` | `def test_os_hint_any_is_passthrough(self, dispatcher)` |
| `test_os_hint_linux_excludes_windows_only_entries` | method | `tests/test_bridge_catalog_filtered.py:51` | `def test_os_hint_linux_excludes_windows_only_entries(self, dispatcher)` |
| `test_os_hint_only_appears_in_header` | method | `tests/test_bridge_catalog_filtered.py:127` | `def test_os_hint_only_appears_in_header(self)` |
| `test_os_hint_uppercase_normalized` | method | `tests/test_bridge_catalog_filtered.py:105` | `def test_os_hint_uppercase_normalized(self, dispatcher)` |
| `test_os_hint_windows_excludes_linux_only_entries` | method | `tests/test_bridge_catalog_filtered.py:61` | `def test_os_hint_windows_excludes_linux_only_entries(self, dispatcher)` |
| `test_phase_arg_accepts_world_model_alias` | method | `tests/test_bridge_catalog_filtered.py:43` | `def test_phase_arg_accepts_world_model_alias(self, dispatcher)` |
| `test_phase_arg_appears_in_header` | method | `tests/test_bridge_catalog_filtered.py:120` | `def test_phase_arg_appears_in_header(self)` |
| `test_phase_arg_restricts_to_one_phase` | method | `tests/test_bridge_catalog_filtered.py:38` | `def test_phase_arg_restricts_to_one_phase(self, dispatcher)` |
| `test_phase_drops_smaller_than_unfiltered_total` | method | `tests/test_bridge_catalog_filtered.py:94` | `def test_phase_drops_smaller_than_unfiltered_total(self, dispatcher)` |
| `test_phase_plus_os_combines_both_filters` | method | `tests/test_bridge_catalog_filtered.py:81` | `def test_phase_plus_os_combines_both_filters(self, dispatcher)` |
| `test_registry_exposes_optional_phase_and_os` | method | `tests/test_bridge_catalog_filtered.py:140` | `def test_registry_exposes_optional_phase_and_os(self)` |
| `test_unknown_phase_returns_friendly_no_match` | method | `tests/test_bridge_catalog_filtered.py:134` | `def test_unknown_phase_returns_friendly_no_match(self)` |
| `TestDnsProfile` | class | `tests/test_c2_profile_engine.py:99` | `class TestDnsProfile` |
| `TestProfileEngine` | class | `tests/test_c2_profile_engine.py:397` | `class TestProfileEngine` |
| `TestProfileRotator` | class | `tests/test_c2_profile_engine.py:214` | `class TestProfileRotator` |
| `TestProfileValidator` | class | `tests/test_c2_profile_engine.py:291` | `class TestProfileValidator` |
| `TestSmbProfile` | class | `tests/test_c2_profile_engine.py:154` | `class TestSmbProfile` |
| `TestTlsProfile` | class | `tests/test_c2_profile_engine.py:34` | `class TestTlsProfile` |
| `TestWebSocketProfile` | class | `tests/test_c2_profile_engine.py:183` | `class TestWebSocketProfile` |
| `test_build_query_subdomain_base32` | method | `tests/test_c2_profile_engine.py:113` | `def test_build_query_subdomain_base32(self)` |
| `test_build_query_subdomain_base64` | method | `tests/test_c2_profile_engine.py:107` | `def test_build_query_subdomain_base64(self)` |
| `test_build_query_subdomain_hex` | method | `tests/test_c2_profile_engine.py:119` | `def test_build_query_subdomain_hex(self)` |
| `test_build_query_subdomain_truncates_to_max_length` | method | `tests/test_c2_profile_engine.py:124` | `def test_build_query_subdomain_truncates_to_max_length(self)` |
| `test_build_query_subdomain_ttl_cache_bypass_disabled` | method | `tests/test_c2_profile_engine.py:130` | `def test_build_query_subdomain_ttl_cache_bypass_disabled(self)` |
| `test_current_slot_identity` | method | `tests/test_c2_profile_engine.py:283` | `def test_current_slot_identity(self)` |
| `test_default_construction` | method | `tests/test_c2_profile_engine.py:35` | `def test_default_construction(self)` |
| `test_default_construction` | method | `tests/test_c2_profile_engine.py:100` | `def test_default_construction(self)` |
| `test_default_construction` | method | `tests/test_c2_profile_engine.py:155` | `def test_default_construction(self)` |
| `test_default_construction` | method | `tests/test_c2_profile_engine.py:184` | `def test_default_construction(self)` |
| `test_default_engine_has_http_slot` | method | `tests/test_c2_profile_engine.py:398` | `def test_default_engine_has_http_slot(self)` |
| `test_disabled_profile` | method | `tests/test_c2_profile_engine.py:94` | `def test_disabled_profile(self)` |
| `test_engine_empty_payload_falls_back_to_defaults` | method | `tests/test_c2_profile_engine.py:465` | `def test_engine_empty_payload_falls_back_to_defaults(self)` |
| `test_engine_from_dict` | method | `tests/test_c2_profile_engine.py:442` | `def test_engine_from_dict(self)` |
| `test_engine_from_payload` | method | `tests/test_c2_profile_engine.py:455` | `def test_engine_from_payload(self)` |
| `test_engine_get_active_profile_dict` | method | `tests/test_c2_profile_engine.py:427` | `def test_engine_get_active_profile_dict(self)` |
| `test_engine_get_all_profiles_dict` | method | `tests/test_c2_profile_engine.py:433` | `def test_engine_get_all_profiles_dict(self)` |
| `test_engine_rotate_through_transports` | method | `tests/test_c2_profile_engine.py:420` | `def test_engine_rotate_through_transports(self)` |
| `test_engine_validate_returns_errors_for_invalid_dns` | method | `tests/test_c2_profile_engine.py:412` | `def test_engine_validate_returns_errors_for_invalid_dns(self)` |
| `test_engine_with_all_transports` | method | `tests/test_c2_profile_engine.py:402` | `def test_engine_with_all_transports(self)` |
| `test_from_dict_empty` | method | `tests/test_c2_profile_engine.py:90` | `def test_from_dict_empty(self)` |
| `test_from_dict_empty` | method | `tests/test_c2_profile_engine.py:148` | `def test_from_dict_empty(self)` |
| `test_from_dict_empty` | method | `tests/test_c2_profile_engine.py:178` | `def test_from_dict_empty(self)` |
| `test_from_dict_empty` | method | `tests/test_c2_profile_engine.py:208` | `def test_from_dict_empty(self)` |
| `test_get_cipher_suites_returns_custom_when_set` | method | `tests/test_c2_profile_engine.py:50` | `def test_get_cipher_suites_returns_custom_when_set(self)` |
| `test_get_cipher_suites_returns_library_defaults` | method | `tests/test_c2_profile_engine.py:44` | `def test_get_cipher_suites_returns_library_defaults(self)` |
| `test_get_cipher_suites_unknown_library_falls_back_to_generic` | method | `tests/test_c2_profile_engine.py:55` | `def test_get_cipher_suites_unknown_library_falls_back_to_generic(self)` |
| `test_get_ja3_hash_produces_stable_output` | method | `tests/test_c2_profile_engine.py:61` | `def test_get_ja3_hash_produces_stable_output(self)` |
| `test_get_ja3_hash_with_grease_produces_variable_output` | method | `tests/test_c2_profile_engine.py:72` | `def test_get_ja3_hash_with_grease_produces_variable_output(self)` |
| `test_is_available_after_touch` | method | `tests/test_c2_profile_engine.py:278` | `def test_is_available_after_touch(self)` |
| `test_is_available_fresh_slot` | method | `tests/test_c2_profile_engine.py:274` | `def test_is_available_fresh_slot(self)` |
| `test_list_slots` | method | `tests/test_c2_profile_engine.py:263` | `def test_list_slots(self)` |
| `test_requires_at_least_one_slot` | method | `tests/test_c2_profile_engine.py:215` | `def test_requires_at_least_one_slot(self)` |
| `test_rotation_cycles_through_slots` | method | `tests/test_c2_profile_engine.py:226` | `def test_rotation_cycles_through_slots(self)` |
| `test_rotation_resets_all_cooldowns_when_all_busy` | method | `tests/test_c2_profile_engine.py:252` | `def test_rotation_resets_all_cooldowns_when_all_busy(self)` |
| `test_rotation_skips_cooldown_slots` | method | `tests/test_c2_profile_engine.py:238` | `def test_rotation_skips_cooldown_slots(self)` |
| `test_serialization_roundtrip` | method | `tests/test_c2_profile_engine.py:77` | `def test_serialization_roundtrip(self)` |
| `test_serialization_roundtrip` | method | `tests/test_c2_profile_engine.py:135` | `def test_serialization_roundtrip(self)` |
| `test_serialization_roundtrip` | method | `tests/test_c2_profile_engine.py:161` | `def test_serialization_roundtrip(self)` |
| `test_serialization_roundtrip` | method | `tests/test_c2_profile_engine.py:191` | `def test_serialization_roundtrip(self)` |
| `test_single_slot_always_active` | method | `tests/test_c2_profile_engine.py:219` | `def test_single_slot_always_active(self)` |
| `test_validate_all_returns_dict` | method | `tests/test_c2_profile_engine.py:383` | `def test_validate_all_returns_dict(self)` |
| `test_validate_dns_disabled_skips` | method | `tests/test_c2_profile_engine.py:339` | `def test_validate_dns_disabled_skips(self)` |
| `test_validate_dns_enabled_missing_domain` | method | `tests/test_c2_profile_engine.py:327` | `def test_validate_dns_enabled_missing_domain(self)` |
| `test_validate_dns_invalid_domain_format` | method | `tests/test_c2_profile_engine.py:344` | `def test_validate_dns_invalid_domain_format(self)` |
| `test_validate_dns_invalid_encoding` | method | `tests/test_c2_profile_engine.py:333` | `def test_validate_dns_invalid_encoding(self)` |
| `test_validate_smb_disabled_skips` | method | `tests/test_c2_profile_engine.py:356` | `def test_validate_smb_disabled_skips(self)` |
| `test_validate_smb_missing_pipe_name` | method | `tests/test_c2_profile_engine.py:350` | `def test_validate_smb_missing_pipe_name(self)` |
| `test_validate_smb_username_without_domain` | method | `tests/test_c2_profile_engine.py:361` | `def test_validate_smb_username_without_domain(self)` |
| `test_validate_tls_disabled_skips` | method | `tests/test_c2_profile_engine.py:297` | `def test_validate_tls_disabled_skips(self)` |
| `test_validate_tls_invalid_version` | method | `tests/test_c2_profile_engine.py:302` | `def test_validate_tls_invalid_version(self)` |
| `test_validate_tls_missing_key_with_cert` | method | `tests/test_c2_profile_engine.py:308` | `def test_validate_tls_missing_key_with_cert(self)` |
| `test_validate_tls_unknown_library` | method | `tests/test_c2_profile_engine.py:318` | `def test_validate_tls_unknown_library(self)` |
| `test_validate_tls_valid` | method | `tests/test_c2_profile_engine.py:292` | `def test_validate_tls_valid(self)` |
| `test_validate_websocket_disabled_skips` | method | `tests/test_c2_profile_engine.py:378` | `def test_validate_websocket_disabled_skips(self)` |
| `test_validate_websocket_invalid_protocol` | method | `tests/test_c2_profile_engine.py:372` | `def test_validate_websocket_invalid_protocol(self)` |
| `_route_decorators` | function | `tests/test_c2_route_auth.py:75` | `def _route_decorators()` |
| `routes` | function | `tests/test_c2_route_auth.py:106` | `def routes()` |
| `test_all_protected_endpoints_exist` | function | `tests/test_c2_route_auth.py:120` | `def test_all_protected_endpoints_exist(routes)` |
| `test_protected_endpoints_require_auth` | function | `tests/test_c2_route_auth.py:110` | `def test_protected_endpoints_require_auth(routes)` |
| `test_public_endpoints_stay_open` | function | `tests/test_c2_route_auth.py:115` | `def test_public_endpoints_stay_open(routes)` |
| `TestLazyShellProxy` | class | `tests/test_c2_shell_lazy.py:103` | `class TestLazyShellProxy` |
| `TestNoEagerCliBuild` | class | `tests/test_c2_shell_lazy.py:62` | `class TestNoEagerCliBuild` |
| `_FakeShell` | class | `tests/test_c2_shell_lazy.py:40` | `class _FakeShell` |
| `__init__` | method | `tests/test_c2_shell_lazy.py:41` | `def __init__(self)` |
| `_init_shell` | function | `tests/test_c2_shell_lazy.py:51` | `def _init_shell()` |
| `_load_proxy_class` | function | `tests/test_c2_shell_lazy.py:25` | `def _load_proxy_class()` |
| `_module_tree` | function | `tests/test_c2_shell_lazy.py:21` | `def _module_tree()` |
| `one_cmd` | method | `tests/test_c2_shell_lazy.py:45` | `def one_cmd(self, command)` |
| `test_lazy_accessor_with_boot_sequence` | method | `tests/test_c2_shell_lazy.py:88` | `def test_lazy_accessor_with_boot_sequence(self)` |
| `test_no_eager_shell_build` | method | `tests/test_c2_shell_lazy.py:76` | `def test_no_eager_shell_build(self)` |
| `test_no_lazyown_import_at_top_level` | method | `tests/test_c2_shell_lazy.py:63` | `def test_no_lazyown_import_at_top_level(self)` |
| `test_reads_forward_and_share_target` | method | `tests/test_c2_shell_lazy.py:104` | `def test_reads_forward_and_share_target(self)` |
| `test_shell_output_attribute` | method | `tests/test_c2_shell_lazy.py:118` | `def test_shell_output_attribute(self)` |
| `test_writes_forward` | method | `tests/test_c2_shell_lazy.py:111` | `def test_writes_forward(self)` |
| `TestCampaignRoutesThroughHelpers` | class | `tests/test_campaign_import_safety.py:96` | `class TestCampaignRoutesThroughHelpers` |
| `TestColumnFiltering` | class | `tests/test_campaign_import_safety.py:55` | `class TestColumnFiltering` |
| `TestCopyTree` | class | `tests/test_campaign_import_safety.py:80` | `class TestCopyTree` |
| `TestZipSlip` | class | `tests/test_campaign_import_safety.py:35` | `class TestZipSlip` |
| `_make_evil_zip` | function | `tests/test_campaign_import_safety.py:27` | `def _make_evil_zip(path)` |
| `test_evil_members_skipped` | method | `tests/test_campaign_import_safety.py:36` | `def test_evil_members_skipped(self, tmp_path)` |
| `test_filtered_insert_roundtrip` | method | `tests/test_campaign_import_safety.py:70` | `def test_filtered_insert_roundtrip(self, tmp_path)` |
| `test_identifier_policy` | method | `tests/test_campaign_import_safety.py:56` | `def test_identifier_policy(self)` |
| `test_legit_tree_extracted` | method | `tests/test_campaign_import_safety.py:46` | `def test_legit_tree_extracted(self, tmp_path)` |
| `test_no_raw_extractall_on_import` | method | `tests/test_campaign_import_safety.py:97` | `def test_no_raw_extractall_on_import(self)` |
| `test_order_preserved` | method | `tests/test_campaign_import_safety.py:67` | `def test_order_preserved(self)` |
| `test_symlinks_not_followed` | method | `tests/test_campaign_import_safety.py:81` | `def test_symlinks_not_followed(self, tmp_path)` |
| `test_unknown_and_hostile_dropped` | method | `tests/test_campaign_import_safety.py:62` | `def test_unknown_and_hostile_dropped(self)` |
| `test_uses_safe_helpers` | method | `tests/test_campaign_import_safety.py:108` | `def test_uses_safe_helpers(self)` |
| `TestAllCategories` | class | `tests/test_categories.py:154` | `class TestAllCategories` |
| `TestBijectionInvariant` | class | `tests/test_categories.py:172` | `class TestBijectionInvariant` |
| `TestCategoryConstants` | class | `tests/test_categories.py:28` | `class TestCategoryConstants` |
| `TestCategoryToShort` | class | `tests/test_categories.py:128` | `class TestCategoryToShort` |
| `TestShortToCategory` | class | `tests/test_categories.py:78` | `class TestShortToCategory` |
| `test_ai_to_category` | method | `tests/test_categories.py:118` | `def test_ai_to_category(self)` |
| `test_all_ai_values` | method | `tests/test_categories.py:68` | `def test_all_ai_values(self)` |
| `test_all_c2_values` | method | `tests/test_categories.py:56` | `def test_all_c2_values(self)` |
| `test_all_categories_count` | method | `tests/test_categories.py:168` | `def test_all_categories_count(self)` |
| `test_all_categories_non_empty` | method | `tests/test_categories.py:161` | `def test_all_categories_non_empty(self)` |
| `test_all_cloud_values` | method | `tests/test_categories.py:71` | `def test_all_cloud_values(self)` |
| `test_all_container_values` | method | `tests/test_categories.py:74` | `def test_all_container_values(self)` |
| `test_all_cred_access_values` | method | `tests/test_categories.py:47` | `def test_all_cred_access_values(self)` |
| `test_all_exfil_values` | method | `tests/test_categories.py:53` | `def test_all_exfil_values(self)` |
| `test_all_exploitation_values` | method | `tests/test_categories.py:35` | `def test_all_exploitation_values(self)` |
| `test_all_lateral_values` | method | `tests/test_categories.py:50` | `def test_all_lateral_values(self)` |
| `test_all_lua_values` | method | `tests/test_categories.py:65` | `def test_all_lua_values(self)` |
| `test_all_misc_values` | method | `tests/test_categories.py:62` | `def test_all_misc_values(self)` |
| `test_all_persistence_values` | method | `tests/test_categories.py:41` | `def test_all_persistence_values(self)` |
| `test_all_post_exploitation_values` | method | `tests/test_categories.py:38` | `def test_all_post_exploitation_values(self)` |
| `test_all_privesc_values` | method | `tests/test_categories.py:44` | `def test_all_privesc_values(self)` |
| `test_all_recon_values` | method | `tests/test_categories.py:29` | `def test_all_recon_values(self)` |
| `test_all_reporting_values` | method | `tests/test_categories.py:59` | `def test_all_reporting_values(self)` |
| `test_all_scanning_values` | method | `tests/test_categories.py:32` | `def test_all_scanning_values(self)` |
| `test_c2_reverse_lookup` | method | `tests/test_categories.py:138` | `def test_c2_reverse_lookup(self)` |
| `test_c2_to_category` | method | `tests/test_categories.py:109` | `def test_c2_to_category(self)` |
| `test_credential_to_category` | method | `tests/test_categories.py:100` | `def test_credential_to_category(self)` |
| `test_enum_to_scanning_category` | method | `tests/test_categories.py:85` | `def test_enum_to_scanning_category(self)` |
| `test_every_short_key_in_all_categories` | method | `tests/test_categories.py:155` | `def test_every_short_key_in_all_categories(self)` |
| `test_exfil_to_category` | method | `tests/test_categories.py:106` | `def test_exfil_to_category(self)` |
| `test_exploit_to_category` | method | `tests/test_categories.py:88` | `def test_exploit_to_category(self)` |
| `test_exploitation_reverse_lookup` | method | `tests/test_categories.py:132` | `def test_exploitation_reverse_lookup(self)` |
| `test_forward_and_reverse_match` | method | `tests/test_categories.py:173` | `def test_forward_and_reverse_match(self)` |
| `test_lateral_to_category` | method | `tests/test_categories.py:103` | `def test_lateral_to_category(self)` |
| `test_misc_to_category` | method | `tests/test_categories.py:115` | `def test_misc_to_category(self)` |
| `test_no_duplicate_all_categories` | method | `tests/test_categories.py:165` | `def test_no_duplicate_all_categories(self)` |
| `test_persistence_to_category` | method | `tests/test_categories.py:94` | `def test_persistence_to_category(self)` |
| `test_post_to_category` | method | `tests/test_categories.py:91` | `def test_post_to_category(self)` |
| `test_privesc_reverse_lookup` | method | `tests/test_categories.py:135` | `def test_privesc_reverse_lookup(self)` |
| `test_privesc_to_category` | method | `tests/test_categories.py:97` | `def test_privesc_to_category(self)` |
| `test_recon_reverse_lookup` | method | `tests/test_categories.py:129` | `def test_recon_reverse_lookup(self)` |
| `test_recon_to_category` | method | `tests/test_categories.py:79` | `def test_recon_to_category(self)` |
| `test_reporting_to_category` | method | `tests/test_categories.py:112` | `def test_reporting_to_category(self)` |
| `test_reverse_lookup_less_than_or_equal_forward` | method | `tests/test_categories.py:150` | `def test_reverse_lookup_less_than_or_equal_forward(self)` |
| `test_reverse_lookup_roundtrip` | method | `tests/test_categories.py:141` | `def test_reverse_lookup_roundtrip(self)` |
| `test_scanning_to_category` | method | `tests/test_categories.py:82` | `def test_scanning_to_category(self)` |
| `test_unknown_short_name_raises_key_error` | method | `tests/test_categories.py:121` | `def test_unknown_short_name_raises_key_error(self)` |
| `_Step` | class | `tests/test_chain_mode.py:36` | `class _Step` |
| `__init__` | method | `tests/test_chain_mode.py:39` | `def __init__(self, name, source, reason)` |
| `_engine` | function | `tests/test_chain_mode.py:52` | `def _engine(resolver)` |
| `_resolver` | function | `tests/test_chain_mode.py:45` | `def _resolver()` |
| `broken` | function | `tests/test_chain_mode.py:212` | `def broken(cmd, phase)` |
| `fake_input` | function | `tests/test_chain_mode.py:63` | `def fake_input(prompt)` |
| `raise_ki` | function | `tests/test_chain_mode.py:179` | `def raise_ki(prompt)` |
| `resolve` | function | `tests/test_chain_mode.py:46` | `def resolve(cmd, phase)` |
| `test_auto_pause_after_max_steps` | function | `tests/test_chain_mode.py:195` | `def test_auto_pause_after_max_steps(tmp_path)` |
| `test_engine_reads_persisted_state` | function | `tests/test_chain_mode.py:239` | `def test_engine_reads_persisted_state(tmp_path)` |
| `test_enter_runs_top_suggestion` | function | `tests/test_chain_mode.py:106` | `def test_enter_runs_top_suggestion()` |
| `test_exit_words_disable_chain_mode` | function | `tests/test_chain_mode.py:144` | `def test_exit_words_disable_chain_mode(word)` |
| `test_invalid_number_re_prompts_then_accepts_valid_pick` | function | `tests/test_chain_mode.py:168` | `def test_invalid_number_re_prompts_then_accepts_valid_pick()` |
| `test_invalid_number_re_prompts_then_skips` | function | `tests/test_chain_mode.py:160` | `def test_invalid_number_re_prompts_then_skips()` |
| `test_keyboard_interrupt_disables` | function | `tests/test_chain_mode.py:178` | `def test_keyboard_interrupt_disables(tmp_path)` |
| `test_no_suggestions_enter_skips_custom_command_runs` | function | `tests/test_chain_mode.py:151` | `def test_no_suggestions_enter_skips_custom_command_runs()` |
| `test_number_selects_ranked_alternative` | function | `tests/test_chain_mode.py:116` | `def test_number_selects_ranked_alternative()` |
| `test_override_runs_operator_command` | function | `tests/test_chain_mode.py:126` | `def test_override_runs_operator_command()` |
| `test_persist_toggle_writes_state_file` | function | `tests/test_chain_mode.py:252` | `def test_persist_toggle_writes_state_file(tmp_path)` |
| `test_prompt_exit_words_persist_off` | function | `tests/test_chain_mode.py:267` | `def test_prompt_exit_words_persist_off(tmp_path)` |
| `test_resolver_failure_degrades_to_no_suggestions` | function | `tests/test_chain_mode.py:211` | `def test_resolver_failure_degrades_to_no_suggestions()` |
| `test_skip_keeps_chain_mode_enabled` | function | `tests/test_chain_mode.py:136` | `def test_skip_keeps_chain_mode_enabled()` |
| `test_step_none_for_skip_verbs` | function | `tests/test_chain_mode.py:101` | `def test_step_none_for_skip_verbs(verb)` |
| `test_step_none_when_disabled` | function | `tests/test_chain_mode.py:90` | `def test_step_none_when_disabled()` |
| `test_step_none_when_not_interactive` | function | `tests/test_chain_mode.py:95` | `def test_step_none_when_not_interactive()` |
| `test_store_roundtrip_and_missing` | function | `tests/test_chain_mode.py:221` | `def test_store_roundtrip_and_missing(tmp_path)` |
| `test_store_survives_malformed_file` | function | `tests/test_chain_mode.py:230` | `def test_store_survives_malformed_file(tmp_path)` |
| `test_suggestion_from_step_and_string` | function | `tests/test_chain_mode.py:85` | `def test_suggestion_from_step_and_string()` |
| `test_ci_workflow_gates_severity_and_types` | function | `tests/test_ci_strict.py:91` | `def test_ci_workflow_gates_severity_and_types()` |
| `test_ci_workflow_has_no_swallowed_quality_gate` | function | `tests/test_ci_strict.py:83` | `def test_ci_workflow_has_no_swallowed_quality_gate()` |
| `test_old_swallow_workflow_is_removed` | function | `tests/test_ci_strict.py:68` | `def test_old_swallow_workflow_is_removed()` |
| `test_strict_workflow_contains_no_swallow_flags` | function | `tests/test_ci_strict.py:26` | `def test_strict_workflow_contains_no_swallow_flags()` |
| `test_strict_workflow_exists` | function | `tests/test_ci_strict.py:21` | `def test_strict_workflow_exists()` |
| `test_strict_workflow_runs_lint` | function | `tests/test_ci_strict.py:38` | `def test_strict_workflow_runs_lint()` |
| `test_strict_workflow_runs_pytest` | function | `tests/test_ci_strict.py:56` | `def test_strict_workflow_runs_pytest()` |
| `test_strict_workflow_runs_security_scan` | function | `tests/test_ci_strict.py:50` | `def test_strict_workflow_runs_security_scan()` |
| `test_strict_workflow_runs_type_check` | function | `tests/test_ci_strict.py:44` | `def test_strict_workflow_runs_type_check()` |
| `test_strict_workflow_targets_main_branch` | function | `tests/test_ci_strict.py:62` | `def test_strict_workflow_targets_main_branch()` |
| `claude_md_text` | function | `tests/test_claudemd_consistency.py:22` | `def claude_md_text()` |
| `test_claude_md_does_not_reference_deduplicated_config` | function | `tests/test_claudemd_consistency.py:41` | `def test_claude_md_does_not_reference_deduplicated_config(claude_md_text)` |
| `test_claude_md_reports_actual_test_file_count` | function | `tests/test_claudemd_consistency.py:28` | `def test_claude_md_reports_actual_test_file_count(claude_md_text)` |
| `test_claude_md_under_size_budget` | function | `tests/test_claudemd_size.py:22` | `def test_claude_md_under_size_budget()` |
| `TestApplyAssign` | class | `tests/test_cli_assign.py:34` | `class TestApplyAssign` |
| `TestCompleteAssignBehaviour` | class | `tests/test_cli_assign.py:230` | `class TestCompleteAssignBehaviour` |
| `TestFormatPayload` | class | `tests/test_cli_assign.py:105` | `class TestFormatPayload` |
| `TestLazyOwnAssignWiring` | class | `tests/test_cli_assign.py:163` | `class TestLazyOwnAssignWiring` |
| `_add_repo_root_to_syspath` | function | `tests/test_cli_assign.py:29` | `def _add_repo_root_to_syspath()` |
| `_extract_method_body` | method | `tests/test_cli_assign.py:219` | `def _extract_method_body(src, name)` |
| `migrated_src` | method | `tests/test_cli_assign.py:169` | `def migrated_src(self)` |
| `saver` | function | `tests/test_cli_assign.py:72` | `def saver(p)` |
| `src` | method | `tests/test_cli_assign.py:165` | `def src(self)` |
| `test_aligns_column_to_widest_key` | method | `tests/test_cli_assign.py:120` | `def test_aligns_column_to_widest_key(self)` |
| `test_complete_assign_defined` | method | `tests/test_cli_assign.py:202` | `def test_complete_assign_defined(self, src)` |
| `test_complete_assign_reads_self_params` | method | `tests/test_cli_assign.py:205` | `def test_complete_assign_reads_self_params(self, src)` |
| `test_do_assign_calls_apply_assign` | method | `tests/test_cli_assign.py:186` | `def test_do_assign_calls_apply_assign(self, migrated_src)` |
| `test_do_assign_no_longer_directly_mutates_params` | method | `tests/test_cli_assign.py:196` | `def test_do_assign_no_longer_directly_mutates_params(self, migrated_src)` |
| `test_do_assign_refreshes_aliases` | method | `tests/test_cli_assign.py:191` | `def test_do_assign_refreshes_aliases(self, migrated_src)` |
| `test_do_payload_refreshes_aliases` | method | `tests/test_cli_assign.py:213` | `def test_do_payload_refreshes_aliases(self, migrated_src)` |
| `test_do_show_uses_format_payload` | method | `tests/test_cli_assign.py:209` | `def test_do_show_uses_format_payload(self, migrated_src)` |
| `test_does_not_invoke_save_on_failure` | method | `tests/test_cli_assign.py:49` | `def test_does_not_invoke_save_on_failure(self)` |
| `test_empty_payload_returns_empty_string` | method | `tests/test_cli_assign.py:106` | `def test_empty_payload_returns_empty_string(self)` |
| `test_imports_apply_assign` | method | `tests/test_cli_assign.py:177` | `def test_imports_apply_assign(self, migrated_src)` |
| `test_imports_format_payload` | method | `tests/test_cli_assign.py:183` | `def test_imports_format_payload(self, migrated_src)` |
| `test_imports_save_payload_from_core` | method | `tests/test_cli_assign.py:180` | `def test_imports_save_payload_from_core(self, migrated_src)` |
| `test_int_value_rendered_as_string` | method | `tests/test_cli_assign.py:150` | `def test_int_value_rendered_as_string(self)` |
| `test_invokes_save_on_success` | method | `tests/test_cli_assign.py:57` | `def test_invokes_save_on_success(self)` |
| `test_keys_whitelist_filters_output` | method | `tests/test_cli_assign.py:136` | `def test_keys_whitelist_filters_output(self)` |
| `test_missing_whitelist_keys_render_as_empty` | method | `tests/test_cli_assign.py:143` | `def test_missing_whitelist_keys_render_as_empty(self)` |
| `test_no_ansi_codes` | method | `tests/test_cli_assign.py:156` | `def test_no_ansi_codes(self)` |
| `test_no_completion_for_value_position` | method | `tests/test_cli_assign.py:250` | `def test_no_completion_for_value_position(self)` |
| `test_none_values_render_as_empty` | method | `tests/test_cli_assign.py:130` | `def test_none_values_render_as_empty(self)` |
| `test_persists_to_disk_via_save_payload` | method | `tests/test_cli_assign.py:85` | `def test_persists_to_disk_via_save_payload(self, tmp_path)` |
| `test_renders_keys_sorted` | method | `tests/test_cli_assign.py:111` | `def test_renders_keys_sorted(self)` |
| `test_returns_false_when_key_missing` | method | `tests/test_cli_assign.py:42` | `def test_returns_false_when_key_missing(self)` |
| `test_returns_keys_starting_with_text` | method | `tests/test_cli_assign.py:233` | `def test_returns_keys_starting_with_text(self)` |
| `test_returns_true_when_key_exists` | method | `tests/test_cli_assign.py:35` | `def test_returns_true_when_key_exists(self)` |
| `test_save_optional` | method | `tests/test_cli_assign.py:78` | `def test_save_optional(self)` |
| `test_save_receives_mutated_dict` | method | `tests/test_cli_assign.py:66` | `def test_save_receives_mutated_dict(self)` |
| `TestRememberMeComparison` | class | `tests/test_cli_auth_remember.py:48` | `class TestRememberMeComparison` |
| `isolated_auth` | function | `tests/test_cli_auth_remember.py:24` | `def isolated_auth(tmp_path, monkeypatch)` |
| `test_comparison_is_timing_safe` | method | `tests/test_cli_auth_remember.py:76` | `def test_comparison_is_timing_safe(self)` |
| `test_save_delegates_to_canonical_writer` | method | `tests/test_cli_auth_remember.py:92` | `def test_save_delegates_to_canonical_writer(self)` |
| `test_save_writes_valid_json_and_audits` | method | `tests/test_cli_auth_remember.py:109` | `def test_save_writes_valid_json_and_audits(self, isolated_auth)` |
| `test_valid_token_logs_in` | method | `tests/test_cli_auth_remember.py:49` | `def test_valid_token_logs_in(self, isolated_auth)` |
| `test_wrong_token_rejected` | method | `tests/test_cli_auth_remember.py:63` | `def test_wrong_token_rejected(self, isolated_auth)` |
| `TestAliasLoaderSubstitution` | class | `tests/test_cli_command_sets.py:208` | `class TestAliasLoaderSubstitution` |
| `TestAliasYamlIntegrity` | class | `tests/test_cli_command_sets.py:177` | `class TestAliasYamlIntegrity` |
| `TestCommandSetDiscovery` | class | `tests/test_cli_command_sets.py:324` | `class TestCommandSetDiscovery` |
| `TestLazyOwnRefactor` | class | `tests/test_cli_command_sets.py:297` | `class TestLazyOwnRefactor` |
| `TestLazyOwnStillParses` | class | `tests/test_cli_command_sets.py:394` | `class TestLazyOwnStillParses` |
| `TestPrivateHelperForwarding` | class | `tests/test_cli_command_sets.py:399` | `class TestPrivateHelperForwarding` |
| `TestRegisterCommandSets` | class | `tests/test_cli_command_sets.py:356` | `class TestRegisterCommandSets` |
| `_Bare` | class | `tests/test_cli_command_sets.py:362` | `class _Bare(Cmd)` |
| `_Bare` | class | `tests/test_cli_command_sets.py:386` | `class _Bare(Cmd)` |
| `_ExplosiveCommandSet` | class | `tests/test_cli_command_sets.py:374` | `class _ExplosiveCommandSet(CommandSet)` |
| `_Probe` | class | `tests/test_cli_command_sets.py:414` | `class _Probe(LazyOwnCommandSet)` |
| `_Shell` | class | `tests/test_cli_command_sets.py:427` | `class _Shell(Cmd)` |
| `__init__` | method | `tests/test_cli_command_sets.py:375` | `def __init__(self)` |
| `__init__` | method | `tests/test_cli_command_sets.py:428` | `def __init__(self)` |
| `_add_repo_root_to_syspath` | function | `tests/test_cli_command_sets.py:24` | `def _add_repo_root_to_syspath()` |
| `_legacy_alias_keys_from_lazyown` | function | `tests/test_cli_command_sets.py:34` | `def _legacy_alias_keys_from_lazyown()` |
| `_load_yaml` | function | `tests/test_cli_command_sets.py:29` | `def _load_yaml()` |
| `_probe_class` | method | `tests/test_cli_command_sets.py:409` | `def _probe_class(self)` |
| `_scope_helper` | method | `tests/test_cli_command_sets.py:432` | `def _scope_helper(self)` |

Next: [SYMBOLS_p31.md](SYMBOLS_p31.md)
