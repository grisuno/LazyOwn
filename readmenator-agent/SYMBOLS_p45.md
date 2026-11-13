# Symbols (page 45 of 53)
Previous: [SYMBOLS_p44.md](SYMBOLS_p44.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_unreadable_inputs` | method | `tests/test_lazy_timeline.py:85` | `def test_unreadable_inputs(self, tmp_path)` |
| `test_version_changed_kind` | method | `tests/test_lazy_timeline.py:57` | `def test_version_changed_kind(self, tmp_path)` |
| `test_zombie_requires_services` | method | `tests/test_lazy_timeline.py:77` | `def test_zombie_requires_services(self, tmp_path)` |
| `test_zombie_via_lost_dns` | method | `tests/test_lazy_timeline.py:70` | `def test_zombie_via_lost_dns(self, tmp_path)` |
| `test_apply_rules_never_drops_below_floor` | function | `tests/test_lazy_triage.py:41` | `def test_apply_rules_never_drops_below_floor()` |
| `test_backed_confirmed_stays` | function | `tests/test_lazy_triage.py:53` | `def test_backed_confirmed_stays()` |
| `test_cve_match_without_version_is_unknown` | function | `tests/test_lazy_triage.py:35` | `def test_cve_match_without_version_is_unknown()` |
| `test_floor_confirms_shell_and_exploit_success` | function | `tests/test_lazy_triage.py:27` | `def test_floor_confirms_shell_and_exploit_success()` |
| `test_replay_within_ttl` | function | `tests/test_lazy_triage.py:96` | `def test_replay_within_ttl(tmp_path)` |
| `test_signature_excludes_asset_fields` | function | `tests/test_lazy_triage.py:65` | `def test_signature_excludes_asset_fields()` |
| `test_signature_keeps_evidence_terms` | function | `tests/test_lazy_triage.py:72` | `def test_signature_keeps_evidence_terms()` |
| `test_signature_respects_ttl` | function | `tests/test_lazy_triage.py:79` | `def test_signature_respects_ttl(tmp_path, monkeypatch)` |
| `test_signature_store_persists` | function | `tests/test_lazy_triage.py:88` | `def test_signature_store_persists(tmp_path)` |
| `test_unbacked_confirmed_demotes_to_likely` | function | `tests/test_lazy_triage.py:47` | `def test_unbacked_confirmed_demotes_to_likely()` |
| `test_version_unknown_is_immovable` | function | `tests/test_lazy_triage.py:58` | `def test_version_unknown_is_immovable()` |
| `_ToyPool` | class | `tests/test_lazy_worker_safety.py:263` | `class _ToyPool` |
| `__init__` | method | `tests/test_lazy_worker_safety.py:264` | `def __init__(self)` |
| `_engine` | function | `tests/test_lazy_worker_safety.py:28` | `def _engine(tmp_path, monkeypatch)` |
| `_fake_execute` | function | `tests/test_lazy_worker_safety.py:122` | `def _fake_execute(self, node, executor, timeout_sec)` |
| `_worker` | function | `tests/test_lazy_worker_safety.py:37` | `def _worker(loop, engine, task_id, name)` |
| `complete` | method | `tests/test_lazy_worker_safety.py:270` | `def complete(self)` |
| `executor` | function | `tests/test_lazy_worker_safety.py:95` | `def executor(command)` |
| `members` | method | `tests/test_lazy_worker_safety.py:267` | `def members(self)` |
| `payload_store` | function | `tests/test_lazy_worker_safety.py:15` | `def payload_store(tmp_path, monkeypatch)` |
| `test_capable_member_chain_filters_toy_models` | function | `tests/test_lazy_worker_safety.py:195` | `def test_capable_member_chain_filters_toy_models()` |
| `test_destructive_or_malformed_steps_rejected` | function | `tests/test_lazy_worker_safety.py:211` | `def test_destructive_or_malformed_steps_rejected()` |
| `test_enumeration_intent_does_not_escalate` | function | `tests/test_lazy_worker_safety.py:242` | `def test_enumeration_intent_does_not_escalate(tmp_path, monkeypatch)` |
| `test_initial_access_intent_escalates_to_auto_pwn` | function | `tests/test_lazy_worker_safety.py:229` | `def test_initial_access_intent_escalates_to_auto_pwn(tmp_path, monkeypatch)` |
| `test_needs_sudo_detects_wrappers_and_segments` | function | `tests/test_lazy_worker_safety.py:140` | `def test_needs_sudo_detects_wrappers_and_segments(tmp_path, monkeypatch)` |
| `test_run_round_reuses_worker_pool` | function | `tests/test_lazy_worker_safety.py:105` | `def test_run_round_reuses_worker_pool(payload_store, monkeypatch)` |
| `test_sanitizer_retargets_and_repairs_commands` | function | `tests/test_lazy_worker_safety.py:53` | `def test_sanitizer_retargets_and_repairs_commands(tmp_path, monkeypatch)` |
| `test_worker_dedupes_commands_already_executed_for_task` | function | `tests/test_lazy_worker_safety.py:70` | `def test_worker_dedupes_commands_already_executed_for_task(tmp_path, monkeypatch)` |
| `test_worker_llm_steps_require_capable_member` | function | `tests/test_lazy_worker_safety.py:255` | `def test_worker_llm_steps_require_capable_member(tmp_path, monkeypatch)` |
| `test_worker_runs_sudo_alias_when_passwordless_available` | function | `tests/test_lazy_worker_safety.py:175` | `def test_worker_runs_sudo_alias_when_passwordless_available(tmp_path, monkeypatch)` |
| `test_worker_skips_sudo_alias_before_execution` | function | `tests/test_lazy_worker_safety.py:153` | `def test_worker_skips_sudo_alias_before_execution(tmp_path, monkeypatch)` |
| `test_worker_skips_sudo_when_unavailable` | function | `tests/test_lazy_worker_safety.py:88` | `def test_worker_skips_sudo_when_unavailable(tmp_path, monkeypatch)` |
| `_svc` | function | `tests/test_lazy_world_diff.py:41` | `def _svc(name, product, version)` |
| `_world` | function | `tests/test_lazy_world_diff.py:37` | `def _world(hosts)` |
| `test_diff_os_change_and_empty_states` | function | `tests/test_lazy_world_diff.py:140` | `def test_diff_os_change_and_empty_states()` |
| `test_diff_reports_port_lifecycle` | function | `tests/test_lazy_world_diff.py:108` | `def test_diff_reports_port_lifecycle()` |
| `test_diff_service_change_requires_prior_identity` | function | `tests/test_lazy_world_diff.py:128` | `def test_diff_service_change_requires_prior_identity()` |
| `test_ghost_endpoints_prefers_web_ports` | function | `tests/test_lazy_world_diff.py:209` | `def test_ghost_endpoints_prefers_web_ports()` |
| `test_ghost_state_apply_ignores_empty_host` | function | `tests/test_lazy_world_diff.py:238` | `def test_ghost_state_apply_ignores_empty_host(tmp_path)` |
| `test_ghost_state_apply_roundtrip` | function | `tests/test_lazy_world_diff.py:225` | `def test_ghost_state_apply_roundtrip(tmp_path)` |
| `test_host_snapshot_missing_host_is_empty` | function | `tests/test_lazy_world_diff.py:69` | `def test_host_snapshot_missing_host_is_empty()` |
| `test_host_snapshot_reads_open_services_only` | function | `tests/test_lazy_world_diff.py:48` | `def test_host_snapshot_reads_open_services_only()` |
| `test_prune_changes` | function | `tests/test_lazy_world_diff.py:196` | `def test_prune_changes(tmp_path)` |
| `test_record_and_recent_changes` | function | `tests/test_lazy_world_diff.py:152` | `def test_record_and_recent_changes(tmp_path)` |
| `test_record_changes_caps_each_host` | function | `tests/test_lazy_world_diff.py:184` | `def test_record_changes_caps_each_host(tmp_path)` |
| `test_record_changes_dedupes_repeat` | function | `tests/test_lazy_world_diff.py:176` | `def test_record_changes_dedupes_repeat(tmp_path)` |
| `test_snapshot_engagement_cooldown` | function | `tests/test_lazy_world_diff.py:268` | `def test_snapshot_engagement_cooldown(tmp_path)` |
| `test_snapshot_engagement_counts_campaign` | function | `tests/test_lazy_world_diff.py:247` | `def test_snapshot_engagement_counts_campaign(tmp_path)` |
| `test_snapshot_fingerprint_ignores_key_order` | function | `tests/test_lazy_world_diff.py:84` | `def test_snapshot_fingerprint_ignores_key_order()` |
| `test_snapshot_fingerprint_stable_and_sensitive` | function | `tests/test_lazy_world_diff.py:74` | `def test_snapshot_fingerprint_stable_and_sensitive()` |
| `TestLazyDorks` | class | `tests/test_lazydorks.py:23` | `class TestLazyDorks` |
| `dorks` | function | `tests/test_lazydorks.py:17` | `def dorks()` |
| `test_all_queries_only_populated` | method | `tests/test_lazydorks.py:52` | `def test_all_queries_only_populated(self, dorks)` |
| `test_categories_populated` | method | `tests/test_lazydorks.py:24` | `def test_categories_populated(self, dorks)` |
| `test_empty_domain_empty` | method | `tests/test_lazydorks.py:48` | `def test_empty_domain_empty(self, dorks)` |
| `test_github_needs_org_or_domain` | method | `tests/test_lazydorks.py:40` | `def test_github_needs_org_or_domain(self, dorks)` |
| `test_github_org_fallback_to_domain` | method | `tests/test_lazydorks.py:44` | `def test_github_org_fallback_to_domain(self, dorks)` |
| `test_queries_cap` | method | `tests/test_lazydorks.py:33` | `def test_queries_cap(self, dorks)` |
| `test_queries_scoped_to_domain` | method | `tests/test_lazydorks.py:29` | `def test_queries_scoped_to_domain(self, dorks)` |
| `test_unknown_category_empty` | method | `tests/test_lazydorks.py:37` | `def test_unknown_category_empty(self, dorks)` |
| `test_write_report` | method | `tests/test_lazydorks.py:56` | `def test_write_report(self, dorks, tmp_path)` |
| `test_write_report_invalid_target` | method | `tests/test_lazydorks.py:65` | `def test_write_report_invalid_target(self, dorks, tmp_path)` |
| `ConcreteBackend` | class | `tests/test_lazygui_backend.py:151` | `class ConcreteBackend(Backend)` |
| `TestBackendDescriptor` | class | `tests/test_lazygui_backend.py:26` | `class TestBackendDescriptor` |
| `TestBackendSignals` | class | `tests/test_lazygui_backend.py:77` | `class TestBackendSignals` |
| `TestBackendStatus` | class | `tests/test_lazygui_backend.py:41` | `class TestBackendStatus` |
| `TestTeamserverBackendConstruction` | class | `tests/test_lazygui_backend.py:173` | `class TestTeamserverBackendConstruction` |
| `TestTeamserverBackendLifecycle` | class | `tests/test_lazygui_backend.py:302` | `class TestTeamserverBackendLifecycle` |
| `TestTeamserverCredentials` | class | `tests/test_lazygui_backend.py:52` | `class TestTeamserverCredentials` |
| `TestTeamserverPayloadParsing` | class | `tests/test_lazygui_backend.py:206` | `class TestTeamserverPayloadParsing` |
| `TestTopologyBuilderFromPayload` | class | `tests/test_lazygui_backend.py:344` | `class TestTopologyBuilderFromPayload` |
| `TestTopologyDataContract` | class | `tests/test_lazygui_backend.py:328` | `class TestTopologyDataContract` |
| `_make_backend` | method | `tests/test_lazygui_backend.py:146` | `def _make_backend()` |
| `feed_terminal_input` | method | `tests/test_lazygui_backend.py:169` | `def feed_terminal_input(self, data)` |
| `make_backend` | method | `tests/test_lazygui_backend.py:347` | `def make_backend(self)` |
| `refresh` | method | `tests/test_lazygui_backend.py:163` | `def refresh(self)` |
| `resize_terminal` | method | `tests/test_lazygui_backend.py:166` | `def resize_terminal(self, columns, rows)` |
| `send_command` | method | `tests/test_lazygui_backend.py:160` | `def send_command(self, command, target_session)` |
| `start` | method | `tests/test_lazygui_backend.py:154` | `def start(self)` |
| `stop` | method | `tests/test_lazygui_backend.py:157` | `def stop(self)` |
| `test_build_url` | method | `tests/test_lazygui_backend.py:191` | `def test_build_url(self)` |
| `test_build_url_no_trailing_slash` | method | `tests/test_lazygui_backend.py:198` | `def test_build_url_no_trailing_slash(self)` |
| `test_builds_beacon_nodes` | method | `tests/test_lazygui_backend.py:362` | `def test_builds_beacon_nodes(self)` |
| `test_builds_c2_node` | method | `tests/test_lazygui_backend.py:354` | `def test_builds_c2_node(self)` |
| `test_builds_connected_hosts` | method | `tests/test_lazygui_backend.py:428` | `def test_builds_connected_hosts(self)` |
| `test_builds_edges_c2_to_beacon` | method | `tests/test_lazygui_backend.py:379` | `def test_builds_edges_c2_to_beacon(self)` |
| `test_builds_host_nodes_from_discovered` | method | `tests/test_lazygui_backend.py:396` | `def test_builds_host_nodes_from_discovered(self)` |
| `test_builds_port_nodes` | method | `tests/test_lazygui_backend.py:412` | `def test_builds_port_nodes(self)` |
| `test_construct_and_compare` | method | `tests/test_lazygui_backend.py:331` | `def test_construct_and_compare(self)` |
| `test_construction` | method | `tests/test_lazygui_backend.py:29` | `def test_construction(self)` |
| `test_construction` | method | `tests/test_lazygui_backend.py:55` | `def test_construction(self)` |
| `test_construction` | method | `tests/test_lazygui_backend.py:176` | `def test_construction(self)` |
| `test_construction_with_parent` | method | `tests/test_lazygui_backend.py:184` | `def test_construction_with_parent(self)` |
| `test_default_tls` | method | `tests/test_lazygui_backend.py:67` | `def test_default_tls(self)` |
| `test_descriptor_read_only` | method | `tests/test_lazygui_backend.py:113` | `def test_descriptor_read_only(self)` |
| `test_immutable` | method | `tests/test_lazygui_backend.py:35` | `def test_immutable(self)` |
| `test_immutable` | method | `tests/test_lazygui_backend.py:71` | `def test_immutable(self)` |
| `test_initial_status_is_disconnected` | method | `tests/test_lazygui_backend.py:93` | `def test_initial_status_is_disconnected(self)` |
| `test_known_campaigns_default` | method | `tests/test_lazygui_backend.py:129` | `def test_known_campaigns_default(self)` |
| `test_known_sessions_defaults` | method | `tests/test_lazygui_backend.py:118` | `def test_known_sessions_defaults(self)` |
| `test_known_topology_default` | method | `tests/test_lazygui_backend.py:123` | `def test_known_topology_default(self)` |
| `test_non_mapping_payload` | method | `tests/test_lazygui_backend.py:216` | `def test_non_mapping_payload(self)` |
| `test_none_converted` | method | `tests/test_lazygui_backend.py:338` | `def test_none_converted(self)` |
| `test_parse_empty_graph_payload` | method | `tests/test_lazygui_backend.py:259` | `def test_parse_empty_graph_payload(self)` |
| `test_parse_graph_edges_from_valid_payload` | method | `tests/test_lazygui_backend.py:242` | `def test_parse_graph_edges_from_valid_payload(self)` |
| `test_parse_graph_nodes_from_valid_payload` | method | `tests/test_lazygui_backend.py:223` | `def test_parse_graph_nodes_from_valid_payload(self)` |
| `test_send_command_does_not_raise` | method | `tests/test_lazygui_backend.py:321` | `def test_send_command_does_not_raise(self)` |
| `test_session_state_default` | method | `tests/test_lazygui_backend.py:138` | `def test_session_state_default(self)` |
| `test_signals_exist` | method | `tests/test_lazygui_backend.py:80` | `def test_signals_exist(self)` |
| `test_status_no_duplicate_emit` | method | `tests/test_lazygui_backend.py:104` | `def test_status_no_duplicate_emit(self)` |
| `test_status_transition` | method | `tests/test_lazygui_backend.py:97` | `def test_status_transition(self)` |
| `test_stop_sets_disconnected` | method | `tests/test_lazygui_backend.py:312` | `def test_stop_sets_disconnected(self)` |
| `test_stop_without_start` | method | `tests/test_lazygui_backend.py:305` | `def test_stop_without_start(self)` |
| `test_topology_emitted_on_change` | method | `tests/test_lazygui_backend.py:439` | `def test_topology_emitted_on_change(self)` |
| `test_topology_not_emitted_on_no_change` | method | `tests/test_lazygui_backend.py:455` | `def test_topology_not_emitted_on_no_change(self)` |
| `test_update_from_empty_payload` | method | `tests/test_lazygui_backend.py:209` | `def test_update_from_empty_payload(self)` |
| `test_update_operator` | method | `tests/test_lazygui_backend.py:267` | `def test_update_operator(self)` |
| `test_update_operator_no_username` | method | `tests/test_lazygui_backend.py:285` | `def test_update_operator_no_username(self)` |
| `test_update_sessions_empty` | method | `tests/test_lazygui_backend.py:294` | `def test_update_sessions_empty(self)` |
| `test_values` | method | `tests/test_lazygui_backend.py:44` | `def test_values(self)` |
| `test_world_model_default` | method | `tests/test_lazygui_backend.py:133` | `def test_world_model_default(self)` |
| `TestColorMap` | class | `tests/test_lazygui_graph_widget.py:106` | `class TestColorMap` |
| `TestColorResolution` | class | `tests/test_lazygui_graph_widget.py:43` | `class TestColorResolution` |
| `TestGraphEdgeItem` | class | `tests/test_lazygui_graph_widget.py:181` | `class TestGraphEdgeItem` |
| `TestGraphNodeItem` | class | `tests/test_lazygui_graph_widget.py:114` | `class TestGraphNodeItem` |
| `TestGraphNodeItemWithIcon` | class | `tests/test_lazygui_graph_widget.py:360` | `class TestGraphNodeItemWithIcon` |
| `TestGraphScene` | class | `tests/test_lazygui_graph_widget.py:212` | `class TestGraphScene` |
| `TestGraphView` | class | `tests/test_lazygui_graph_widget.py:307` | `class TestGraphView` |
| `TestGraphViewWithDatabaseFixture` | class | `tests/test_lazygui_graph_widget.py:333` | `class TestGraphViewWithDatabaseFixture` |
| `TestRadiusResolution` | class | `tests/test_lazygui_graph_widget.py:79` | `class TestRadiusResolution` |
| `_capture` | function | `tests/test_lazygui_graph_widget.py:296` | `def _capture(nid, pos)` |
| `_cb` | function | `tests/test_lazygui_graph_widget.py:149` | `def _cb(nid)` |
| `_cb` | function | `tests/test_lazygui_graph_widget.py:163` | `def _cb(nid, pos)` |
| `_get_qapp` | function | `tests/test_lazygui_graph_widget.py:36` | `def _get_qapp()` |
| `test_all_keys_present` | method | `tests/test_lazygui_graph_widget.py:109` | `def test_all_keys_present(self)` |
| `test_beacon_color` | method | `tests/test_lazygui_graph_widget.py:50` | `def test_beacon_color(self)` |
| `test_beacon_radius` | method | `tests/test_lazygui_graph_widget.py:86` | `def test_beacon_radius(self)` |
| `test_c2_color` | method | `tests/test_lazygui_graph_widget.py:46` | `def test_c2_color(self)` |
| `test_c2_radius` | method | `tests/test_lazygui_graph_widget.py:82` | `def test_c2_radius(self)` |
| `test_callback_on_context_menu` | method | `tests/test_lazygui_graph_widget.py:157` | `def test_callback_on_context_menu(self)` |
| `test_callback_on_selected` | method | `tests/test_lazygui_graph_widget.py:144` | `def test_callback_on_selected(self)` |
| `test_construction` | method | `tests/test_lazygui_graph_widget.py:117` | `def test_construction(self)` |
| `test_construction` | method | `tests/test_lazygui_graph_widget.py:215` | `def test_construction(self)` |
| `test_construction` | method | `tests/test_lazygui_graph_widget.py:310` | `def test_construction(self)` |
| `test_construction_with_nodes` | method | `tests/test_lazygui_graph_widget.py:184` | `def test_construction_with_nodes(self)` |
| `test_default_radius` | method | `tests/test_lazygui_graph_widget.py:101` | `def test_default_radius(self)` |
| `test_fit_to_content` | method | `tests/test_lazygui_graph_widget.py:325` | `def test_fit_to_content(self)` |
| `test_force_layout_single_node` | method | `tests/test_lazygui_graph_widget.py:243` | `def test_force_layout_single_node(self)` |
| `test_full_pipeline` | method | `tests/test_lazygui_graph_widget.py:336` | `def test_full_pipeline(self)` |
| `test_host_color` | method | `tests/test_lazygui_graph_widget.py:54` | `def test_host_color(self)` |
| `test_host_radius` | method | `tests/test_lazygui_graph_widget.py:91` | `def test_host_radius(self)` |
| `test_hover_behavior` | method | `tests/test_lazygui_graph_widget.py:369` | `def test_hover_behavior(self)` |
| `test_identifiers` | method | `tests/test_lazygui_graph_widget.py:127` | `def test_identifiers(self)` |
| `test_linux_os_hint` | method | `tests/test_lazygui_graph_widget.py:66` | `def test_linux_os_hint(self)` |
| `test_macos_os_hint` | method | `tests/test_lazygui_graph_widget.py:70` | `def test_macos_os_hint(self)` |
| `test_movable_flag` | method | `tests/test_lazygui_graph_widget.py:375` | `def test_movable_flag(self)` |
| `test_node_context_menu_signal` | method | `tests/test_lazygui_graph_widget.py:289` | `def test_node_context_menu_signal(self)` |
| `test_node_selected_signal` | method | `tests/test_lazygui_graph_widget.py:280` | `def test_node_selected_signal(self)` |
| `test_node_with_icon` | method | `tests/test_lazygui_graph_widget.py:363` | `def test_node_with_icon(self)` |
| `test_node_without_callbacks_does_not_raise` | method | `tests/test_lazygui_graph_widget.py:173` | `def test_node_without_callbacks_does_not_raise(self)` |
| `test_physics_completion` | method | `tests/test_lazygui_graph_widget.py:258` | `def test_physics_completion(self)` |
| `test_physics_stops_without_nodes` | method | `tests/test_lazygui_graph_widget.py:273` | `def test_physics_stops_without_nodes(self)` |
| `test_port_color` | method | `tests/test_lazygui_graph_widget.py:58` | `def test_port_color(self)` |
| `test_port_radius` | method | `tests/test_lazygui_graph_widget.py:96` | `def test_port_radius(self)` |
| `test_selected_node_id_none_when_empty` | method | `tests/test_lazygui_graph_widget.py:252` | `def test_selected_node_id_none_when_empty(self)` |
| `test_selection_behaviour` | method | `tests/test_lazygui_graph_widget.py:134` | `def test_selection_behaviour(self)` |
| `test_set_empty_topology` | method | `tests/test_lazygui_graph_widget.py:235` | `def test_set_empty_topology(self)` |
| `test_set_topology` | method | `tests/test_lazygui_graph_widget.py:316` | `def test_set_topology(self)` |
| `test_set_topology_with_data` | method | `tests/test_lazygui_graph_widget.py:221` | `def test_set_topology_with_data(self)` |
| `test_unknown_default` | method | `tests/test_lazygui_graph_widget.py:74` | `def test_unknown_default(self)` |
| `test_update_position` | method | `tests/test_lazygui_graph_widget.py:198` | `def test_update_position(self)` |
| `test_windows_os_hint` | method | `tests/test_lazygui_graph_widget.py:62` | `def test_windows_os_hint(self)` |
| `TestBackendKind` | class | `tests/test_lazygui_models.py:303` | `class TestBackendKind` |
| `TestBeaconResult` | class | `tests/test_lazygui_models.py:143` | `class TestBeaconResult` |
| `TestCampaignSummary` | class | `tests/test_lazygui_models.py:221` | `class TestCampaignSummary` |
| `TestDashboardPayload` | class | `tests/test_lazygui_models.py:196` | `class TestDashboardPayload` |
| `TestEventLevel` | class | `tests/test_lazygui_models.py:314` | `class TestEventLevel` |
| `TestEventRecord` | class | `tests/test_lazygui_models.py:256` | `class TestEventRecord` |
| `TestGraphEdge` | class | `tests/test_lazygui_models.py:74` | `class TestGraphEdge` |
| `TestGraphNode` | class | `tests/test_lazygui_models.py:30` | `class TestGraphNode` |
| `TestSessionModel` | class | `tests/test_lazygui_models.py:280` | `class TestSessionModel` |
| `TestTopology` | class | `tests/test_lazygui_models.py:105` | `class TestTopology` |
| `test_compare` | method | `tests/test_lazygui_models.py:322` | `def test_compare(self)` |
| `test_construction` | method | `tests/test_lazygui_models.py:77` | `def test_construction(self)` |
| `test_construction` | method | `tests/test_lazygui_models.py:283` | `def test_construction(self)` |
| `test_default_metadata` | method | `tests/test_lazygui_models.py:56` | `def test_default_metadata(self)` |
| `test_defaults` | method | `tests/test_lazygui_models.py:91` | `def test_defaults(self)` |
| `test_defaults` | method | `tests/test_lazygui_models.py:199` | `def test_defaults(self)` |
| `test_defaults` | method | `tests/test_lazygui_models.py:224` | `def test_defaults(self)` |
| `test_empty_classmethod` | method | `tests/test_lazygui_models.py:115` | `def test_empty_classmethod(self)` |
| `test_empty_fields_default_to_empty_string` | method | `tests/test_lazygui_models.py:181` | `def test_empty_fields_default_to_empty_string(self)` |
| `test_empty_list_keywords` | method | `tests/test_lazygui_models.py:137` | `def test_empty_list_keywords(self)` |
| `test_empty_topology` | method | `tests/test_lazygui_models.py:108` | `def test_empty_topology(self)` |
| `test_equality` | method | `tests/test_lazygui_models.py:61` | `def test_equality(self)` |
| `test_equality` | method | `tests/test_lazygui_models.py:97` | `def test_equality(self)` |
| `test_equality` | method | `tests/test_lazygui_models.py:130` | `def test_equality(self)` |
| `test_equality` | method | `tests/test_lazygui_models.py:174` | `def test_equality(self)` |
| `test_equality` | method | `tests/test_lazygui_models.py:213` | `def test_equality(self)` |
| `test_equality` | method | `tests/test_lazygui_models.py:248` | `def test_equality(self)` |
| `test_fields` | method | `tests/test_lazygui_models.py:263` | `def test_fields(self)` |
| `test_full_construction` | method | `tests/test_lazygui_models.py:41` | `def test_full_construction(self)` |
| `test_full_construction` | method | `tests/test_lazygui_models.py:154` | `def test_full_construction(self)` |
| `test_immutable` | method | `tests/test_lazygui_models.py:68` | `def test_immutable(self)` |
| `test_metadata_default` | method | `tests/test_lazygui_models.py:298` | `def test_metadata_default(self)` |
| `test_minimal_construction` | method | `tests/test_lazygui_models.py:33` | `def test_minimal_construction(self)` |
| `test_minimal_construction` | method | `tests/test_lazygui_models.py:146` | `def test_minimal_construction(self)` |
| `test_now_uses_utc` | method | `tests/test_lazygui_models.py:259` | `def test_now_uses_utc(self)` |
| `test_numeric_levels` | method | `tests/test_lazygui_models.py:271` | `def test_numeric_levels(self)` |
| `test_order` | method | `tests/test_lazygui_models.py:317` | `def test_order(self)` |
| `test_populated` | method | `tests/test_lazygui_models.py:206` | `def test_populated(self)` |
| `test_populated_topology` | method | `tests/test_lazygui_models.py:120` | `def test_populated_topology(self)` |
| `test_str_compat` | method | `tests/test_lazygui_models.py:310` | `def test_str_compat(self)` |
| `test_values` | method | `tests/test_lazygui_models.py:306` | `def test_values(self)` |
| `test_with_counts` | method | `tests/test_lazygui_models.py:234` | `def test_with_counts(self)` |
| `PostScanOutputSpec` | class | `tests/test_lazynmap_post.py:88` | `class PostScanOutputSpec(TestCase)` |
| `PostScanResilienceSpec` | class | `tests/test_lazynmap_post.py:230` | `class PostScanResilienceSpec(TestCase)` |
| `PostScanToggleSpec` | class | `tests/test_lazynmap_post.py:188` | `class PostScanToggleSpec(TestCase)` |
| `_ConsoleRecorder` | class | `tests/test_lazynmap_post.py:81` | `class _ConsoleRecorder` |
| `_broken_factory` | function | `tests/test_lazynmap_post.py:237` | `def _broken_factory()` |
| `_make_engine` | function | `tests/test_lazynmap_post.py:71` | `def _make_engine(sessions, addons, tools)` |
| `_seed_addon` | function | `tests/test_lazynmap_post.py:37` | `def _seed_addon(addons)` |
| `_seed_environment` | function | `tests/test_lazynmap_post.py:59` | `def _seed_environment(tmp)` |
| `print` | method | `tests/test_lazynmap_post.py:84` | `def print(self, line)` |
| `test_console_receives_plan_preview_lines` | method | `tests/test_lazynmap_post.py:168` | `def test_console_receives_plan_preview_lines(self)` |
| `test_disabled_payload_skips_all_writes` | method | `tests/test_lazynmap_post.py:191` | `def test_disabled_payload_skips_all_writes(self)` |
| `test_engine_failure_still_emits_event_and_updates_world_model` | method | `tests/test_lazynmap_post.py:233` | `def test_engine_failure_still_emits_event_and_updates_world_model(self)` |
| `test_event_record_carries_target_and_counts` | method | `tests/test_lazynmap_post.py:144` | `def test_event_record_carries_target_and_counts(self)` |
| `test_string_falsy_toggle_is_respected` | method | `tests/test_lazynmap_post.py:212` | `def test_string_falsy_toggle_is_respected(self)` |
| `test_world_model_is_merged_not_overwritten` | method | `tests/test_lazynmap_post.py:117` | `def test_world_model_is_merged_not_overwritten(self)` |
| `test_writes_plan_world_model_and_event` | method | `tests/test_lazynmap_post.py:91` | `def test_writes_plan_world_model_and_event(self)` |
| `_fake_bin` | function | `tests/test_lazynmap_sudo_branches.py:18` | `def _fake_bin(tmp_path)` |
| `_run_script` | function | `tests/test_lazynmap_sudo_branches.py:31` | `def _run_script(tmp_path, extra_env)` |
| `test_autonomous_mode_aborts_without_passwordless_sudo` | function | `tests/test_lazynmap_sudo_branches.py:48` | `def test_autonomous_mode_aborts_without_passwordless_sudo(tmp_path)` |
| `test_interactive_mode_keeps_the_sudo_prompt_path` | function | `tests/test_lazynmap_sudo_branches.py:55` | `def test_interactive_mode_keeps_the_sudo_prompt_path(tmp_path)` |
| `TestLazyPassGen` | class | `tests/test_lazypassgen.py:23` | `class TestLazyPassGen` |
| `passgen` | function | `tests/test_lazypassgen.py:17` | `def passgen()` |
| `test_export` | method | `tests/test_lazypassgen.py:58` | `def test_export(self, passgen, tmp_path)` |
| `test_export_empty` | method | `tests/test_lazypassgen.py:65` | `def test_export_empty(self, passgen, tmp_path)` |
| `test_generate_cap` | method | `tests/test_lazypassgen.py:50` | `def test_generate_cap(self, passgen)` |
| `test_generate_empty_target` | method | `tests/test_lazypassgen.py:45` | `def test_generate_empty_target(self, passgen)` |
| `test_generate_leet` | method | `tests/test_lazypassgen.py:37` | `def test_generate_leet(self, passgen)` |
| `test_generate_seasons` | method | `tests/test_lazypassgen.py:41` | `def test_generate_seasons(self, passgen)` |
| `test_generate_target_words` | method | `tests/test_lazypassgen.py:32` | `def test_generate_target_words(self, passgen)` |
| `test_seeds_use_lazy_creds` | method | `tests/test_lazypassgen.py:54` | `def test_seeds_use_lazy_creds(self, passgen)` |
| `test_split_entities` | method | `tests/test_lazypassgen.py:24` | `def test_split_entities(self, passgen)` |
| `test_split_skip_short_words` | method | `tests/test_lazypassgen.py:28` | `def test_split_skip_short_words(self, passgen)` |
| `TestFallbackReady` | class | `tests/test_lazypoophish.py:53` | `class TestFallbackReady` |
| `TestRunFallback` | class | `tests/test_lazypoophish.py:70` | `class TestRunFallback` |
| `_fake_orchestrator` | function | `tests/test_lazypoophish.py:32` | `def _fake_orchestrator(monkeypatch, campaign_dir, campaign_id)` |
| `cleared_sessions` | function | `tests/test_lazypoophish.py:27` | `def cleared_sessions(tmp_path, monkeypatch)` |
| `fake_launch` | function | `tests/test_lazypoophish.py:33` | `def fake_launch(target_domain, template, mode, targets_file)` |
| `fake_shorten` | function | `tests/test_lazypoophish.py:89` | `def fake_shorten(url, provider)` |
| `forbidden` | function | `tests/test_lazypoophish.py:113` | `def forbidden()` |
| `poophish` | function | `tests/test_lazypoophish.py:20` | `def poophish()` |
| `raising` | function | `tests/test_lazypoophish.py:63` | `def raising()` |
| `test_invalid_mode` | method | `tests/test_lazypoophish.py:71` | `def test_invalid_mode(self, poophish, cleared_sessions)` |
| `test_launch_failure` | method | `tests/test_lazypoophish.py:76` | `def test_launch_failure(self, poophish, cleared_sessions, monkeypatch)` |
| `test_no_shorten_keeps_raw_url` | method | `tests/test_lazypoophish.py:108` | `def test_no_shorten_keeps_raw_url(self, poophish, cleared_sessions, monkeypatch)` |
| `test_not_ready_with_access` | method | `tests/test_lazypoophish.py:58` | `def test_not_ready_with_access(self, poophish, monkeypatch)` |
| `test_ready_when_access_none` | method | `tests/test_lazypoophish.py:54` | `def test_ready_when_access_none(self, poophish, monkeypatch)` |
| `test_ready_when_tokens_fail` | method | `tests/test_lazypoophish.py:62` | `def test_ready_when_tokens_fail(self, poophish, monkeypatch)` |
| `test_short_url_and_artifact` | method | `tests/test_lazypoophish.py:85` | `def test_short_url_and_artifact(self, poophish, cleared_sessions, monkeypatch)` |
| `TestLazyShortener` | class | `tests/test_lazyshortener.py:33` | `class TestLazyShortener` |
| `_FakeResponse` | class | `tests/test_lazyshortener.py:23` | `class _FakeResponse` |
| `__init__` | method | `tests/test_lazyshortener.py:24` | `def __init__(self, text, status)` |
| `fake_get` | function | `tests/test_lazyshortener.py:56` | `def fake_get(endpoint, params)` |
| `raise_for_status` | method | `tests/test_lazyshortener.py:28` | `def raise_for_status(self)` |
| `raising` | function | `tests/test_lazyshortener.py:75` | `def raising()` |
| `shortener` | function | `tests/test_lazyshortener.py:17` | `def shortener()` |
| `test_provider_error_message` | method | `tests/test_lazyshortener.py:68` | `def test_provider_error_message(self, shortener, monkeypatch)` |
| `test_providers` | method | `tests/test_lazyshortener.py:34` | `def test_providers(self, shortener)` |
| `test_rejects_invalid_url` | method | `tests/test_lazyshortener.py:43` | `def test_rejects_invalid_url(self, shortener)` |
| `test_rejects_metacharacters` | method | `tests/test_lazyshortener.py:48` | `def test_rejects_metacharacters(self, shortener)` |
| `test_shorten_success` | method | `tests/test_lazyshortener.py:53` | `def test_shorten_success(self, shortener, monkeypatch)` |
| `test_transport_failure` | method | `tests/test_lazyshortener.py:74` | `def test_transport_failure(self, shortener, monkeypatch)` |
| `test_unknown_provider` | method | `tests/test_lazyshortener.py:38` | `def test_unknown_provider(self, shortener)` |
| `TestLegacyShims` | class | `tests/test_legacy_shims.py:23` | `class TestLegacyShims` |
| `TestReferencedScriptsExist` | class | `tests/test_legacy_shims.py:43` | `class TestReferencedScriptsExist` |
| `test_exploit_migrated_script_paths` | method | `tests/test_legacy_shims.py:44` | `def test_exploit_migrated_script_paths(self)` |
| `test_no_regular_file_clones` | method | `tests/test_legacy_shims.py:24` | `def test_no_regular_file_clones(self)` |
| `test_symlinks_resolve_into_contrib` | method | `tests/test_legacy_shims.py:32` | `def test_symlinks_resolve_into_contrib(self)` |
| `TestLessonIngestor` | class | `tests/test_lesson_ingestor.py:35` | `class TestLessonIngestor` |
| `TestLessonLearned` | class | `tests/test_lesson_ingestor.py:15` | `class TestLessonLearned` |
| `test_expert_mapping` | method | `tests/test_lesson_ingestor.py:36` | `def test_expert_mapping(self)` |
| `test_from_dict` | method | `tests/test_lesson_ingestor.py:16` | `def test_from_dict(self)` |
| `test_from_dict_minimal` | method | `tests/test_lesson_ingestor.py:29` | `def test_from_dict_minimal(self)` |
| `test_ingest_all` | method | `tests/test_lesson_ingestor.py:124` | `def test_ingest_all(self, tmp_path)` |
| `test_ingest_no_backends` | method | `tests/test_lesson_ingestor.py:79` | `def test_ingest_no_backends(self, monkeypatch)` |
| `test_ingest_unmapped_topic` | method | `tests/test_lesson_ingestor.py:62` | `def test_ingest_unmapped_topic(self, tmp_path)` |
| `test_ingest_with_mock_backends` | method | `tests/test_lesson_ingestor.py:43` | `def test_ingest_with_mock_backends(self, tmp_path)` |
| `test_load_from_file` | method | `tests/test_lesson_ingestor.py:99` | `def test_load_from_file(self, tmp_path)` |
| `test_load_from_file_missing` | method | `tests/test_lesson_ingestor.py:119` | `def test_load_from_file_missing(self, tmp_path)` |
| `_run_ruff` | function | `tests/test_lint_quality.py:63` | `def _run_ruff(args)` |
| `test_format_targets_exist` | function | `tests/test_lint_quality.py:100` | `def test_format_targets_exist()` |
| `test_lint_targets_exist` | function | `tests/test_lint_quality.py:94` | `def test_lint_targets_exist()` |
| `test_ruff_check_clean` | function | `tests/test_lint_quality.py:75` | `def test_ruff_check_clean(target)` |
| `test_ruff_format_clean` | function | `tests/test_lint_quality.py:84` | `def test_ruff_format_clean(target)` |
| `_world` | function | `tests/test_live_surface.py:25` | `def _world()` |
| `test_compromised_states_constant_matches_world_model` | function | `tests/test_live_surface.py:116` | `def test_compromised_states_constant_matches_world_model()` |
| `test_empty_world_is_well_formed` | function | `tests/test_live_surface.py:55` | `def test_empty_world_is_well_formed()` |
| `test_host_with_credential_pulses_even_if_not_owned` | function | `tests/test_live_surface.py:87` | `def test_host_with_credential_pulses_even_if_not_owned()` |
| `test_hosts_and_services_become_nodes` | function | `tests/test_live_surface.py:68` | `def test_hosts_and_services_become_nodes()` |
| `test_malformed_host_entry_is_skipped` | function | `tests/test_live_surface.py:109` | `def test_malformed_host_entry_is_skipped()` |
| `test_none_world_is_tolerated` | function | `tests/test_live_surface.py:63` | `def test_none_world_is_tolerated()` |
| `test_owned_host_pulses_and_counts_as_compromised` | function | `tests/test_live_surface.py:79` | `def test_owned_host_pulses_and_counts_as_compromised()` |
| `test_runs_service_edge_is_emitted_once` | function | `tests/test_live_surface.py:95` | `def test_runs_service_edge_is_emitted_once()` |
| `test_stats_block_counts` | function | `tests/test_live_surface.py:102` | `def test_stats_block_counts()` |
| `TestAskGeneral` | class | `tests/test_llm_adapter_parity.py:222` | `class TestAskGeneral` |
| `TestDirectPromptFlow` | class | `tests/test_llm_adapter_parity.py:111` | `class TestDirectPromptFlow` |
| `TestExports` | class | `tests/test_llm_adapter_parity.py:188` | `class TestExports` |
| `TestFileReadingVariants` | class | `tests/test_llm_adapter_parity.py:146` | `class TestFileReadingVariants` |
| `TestKnowledgePersistence` | class | `tests/test_llm_adapter_parity.py:130` | `class TestKnowledgePersistence` |
| `TestMissingClient` | class | `tests/test_llm_adapter_parity.py:82` | `class TestMissingClient` |
| `TestUninitializedClient` | class | `tests/test_llm_adapter_parity.py:105` | `class TestUninitializedClient` |
| `TestVulnAugmentation` | class | `tests/test_llm_adapter_parity.py:164` | `class TestVulnAugmentation` |
| `_FakeBackend` | class | `tests/test_llm_adapter_parity.py:208` | `class _FakeBackend` |
| `_FakeClient` | class | `tests/test_llm_adapter_parity.py:42` | `class _FakeClient` |
| `_FakeCompletions` | class | `tests/test_llm_adapter_parity.py:28` | `class _FakeCompletions` |
| `__init__` | method | `tests/test_llm_adapter_parity.py:29` | `def __init__(self, content)` |
| `__init__` | method | `tests/test_llm_adapter_parity.py:43` | `def __init__(self, content)` |
| `__init__` | method | `tests/test_llm_adapter_parity.py:209` | `def __init__(self, result)` |
| `_write` | function | `tests/test_llm_adapter_parity.py:77` | `def _write(path, text)` |
| `cfg` | function | `tests/test_llm_adapter_parity.py:61` | `def cfg(tmp_path)` |
| `complete` | method | `tests/test_llm_adapter_parity.py:214` | `def complete(self, system, user)` |
| `create` | method | `tests/test_llm_adapter_parity.py:35` | `def create(self, model, messages, max_tokens)` |
| `exhausted_chain` | function | `tests/test_llm_adapter_parity.py:49` | `def exhausted_chain(monkeypatch)` |
| `patched` | function | `tests/test_llm_adapter_parity.py:72` | `def patched(monkeypatch, cfg)` |
| `test_appends_event_tool_output` | method | `tests/test_llm_adapter_parity.py:165` | `def test_appends_event_tool_output(self, patched, cfg, tmp_path)` |
| `test_appends_plan_history` | method | `tests/test_llm_adapter_parity.py:178` | `def test_appends_plan_history(self, patched, cfg, tmp_path)` |
| `test_backend_error_string_not_remembered` | method | `tests/test_llm_adapter_parity.py:254` | `def test_backend_error_string_not_remembered(self, patched, cfg, monkeypatch)` |
| `test_backend_exception_reports_error` | method | `tests/test_llm_adapter_parity.py:247` | `def test_backend_exception_reports_error(self, patched, monkeypatch)` |
| `test_complete_error_handled` | method | `tests/test_llm_adapter_parity.py:106` | `def test_complete_error_handled(self, patched)` |
| `test_completion_received_single_user_message` | method | `tests/test_llm_adapter_parity.py:117` | `def test_completion_received_single_user_message(self, patched)` |
| `test_default_max_tokens_applied` | method | `tests/test_llm_adapter_parity.py:124` | `def test_default_max_tokens_applied(self, patched)` |
| `test_direct_variants_report_missing_key` | method | `tests/test_llm_adapter_parity.py:93` | `def test_direct_variants_report_missing_key(self, patched, name)` |
| `test_error_response_not_remembered` | method | `tests/test_llm_adapter_parity.py:139` | `def test_error_response_not_remembered(self, patched, cfg)` |
| `test_exported` | method | `tests/test_llm_adapter_parity.py:274` | `def test_exported(self)` |
| `test_file_variants_report_missing_key` | method | `tests/test_llm_adapter_parity.py:98` | `def test_file_variants_report_missing_key(self, patched, name, tmp_path)` |
| `test_groq_family_exports_present` | method | `tests/test_llm_adapter_parity.py:189` | `def test_groq_family_exports_present(self)` |
| `test_missing_backend_reports_error` | method | `tests/test_llm_adapter_parity.py:240` | `def test_missing_backend_reports_error(self, patched, monkeypatch)` |
| `test_receives_system_and_rendered_user` | method | `tests/test_llm_adapter_parity.py:230` | `def test_receives_system_and_rendered_user(self, patched, monkeypatch)` |
| `test_redop_reads_file_content` | method | `tests/test_llm_adapter_parity.py:158` | `def test_redop_reads_file_content(self, patched, tmp_path)` |
| `test_safe_groq_client_none_without_key` | method | `tests/test_llm_adapter_parity.py:203` | `def test_safe_groq_client_none_without_key(self)` |
| `test_sends_user_message_and_returns_content` | method | `tests/test_llm_adapter_parity.py:112` | `def test_sends_user_message_and_returns_content(self, patched)` |
| `test_successful_answer_remembered` | method | `tests/test_llm_adapter_parity.py:263` | `def test_successful_answer_remembered(self, patched, cfg, monkeypatch)` |
| `test_successful_response_is_remembered` | method | `tests/test_llm_adapter_parity.py:131` | `def test_successful_response_is_remembered(self, patched, cfg)` |
| `test_task_missing_file_returns_error` | method | `tests/test_llm_adapter_parity.py:154` | `def test_task_missing_file_returns_error(self, patched, tmp_path)` |
| `test_task_reads_file_content` | method | `tests/test_llm_adapter_parity.py:147` | `def test_task_reads_file_content(self, patched, tmp_path)` |
| `test_uses_configured_backend` | method | `tests/test_llm_adapter_parity.py:223` | `def test_uses_configured_backend(self, patched, monkeypatch)` |
| `_StubBackend` | class | `tests/test_llm_budget.py:316` | `class _StubBackend` |
| `_StubBackend` | class | `tests/test_llm_budget.py:356` | `class _StubBackend` |
| `complete` | method | `tests/test_llm_budget.py:323` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `tests/test_llm_budget.py:363` | `def complete(self, system, user, max_tokens, temperature)` |
| `generate` | method | `tests/test_llm_budget.py:317` | `def generate(self, prompt)` |
| `generate` | method | `tests/test_llm_budget.py:357` | `def generate(self, prompt)` |
| `stream_generate` | method | `tests/test_llm_budget.py:320` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `tests/test_llm_budget.py:360` | `def stream_generate(self, prompt)` |
| `test_budget_config_dataclass_carries_expected_fields` | function | `tests/test_llm_budget.py:51` | `def test_budget_config_dataclass_carries_expected_fields()` |
| `test_budget_guard_charges_a_successful_call` | function | `tests/test_llm_budget.py:218` | `def test_budget_guard_charges_a_successful_call(tmp_sessions)` |
| `test_budget_guard_disabled_passes_through` | function | `tests/test_llm_budget.py:242` | `def test_budget_guard_disabled_passes_through(tmp_sessions)` |
| `test_budget_guard_refuses_call_when_daily_budget_exhausted` | function | `tests/test_llm_budget.py:162` | `def test_budget_guard_refuses_call_when_daily_budget_exhausted(tmp_sessions)` |
| `test_budget_guard_refuses_call_when_token_cap_exceeded` | function | `tests/test_llm_budget.py:195` | `def test_budget_guard_refuses_call_when_token_cap_exceeded(tmp_sessions)` |
| `test_budget_ledger_persists_to_disk` | function | `tests/test_llm_budget.py:116` | `def test_budget_ledger_persists_to_disk(tmp_sessions)` |
| `test_budget_ledger_records_a_charge` | function | `tests/test_llm_budget.py:99` | `def test_budget_ledger_records_a_charge(tmp_path)` |
| `test_budget_ledger_rolls_over_at_midnight` | function | `tests/test_llm_budget.py:136` | `def test_budget_ledger_rolls_over_at_midnight(tmp_sessions)` |
| `test_budget_module_is_importable` | function | `tests/test_llm_budget.py:35` | `def test_budget_module_is_importable()` |
| `test_format_budget_status_includes_spent_and_remaining` | function | `tests/test_llm_budget.py:265` | `def test_format_budget_status_includes_spent_and_remaining(tmp_sessions)` |
| `test_load_budget_config_reads_payload` | function | `tests/test_llm_budget.py:395` | `def test_load_budget_config_reads_payload(tmp_sessions)` |
| `test_payload_schema_recognises_budget_keys` | function | `tests/test_llm_budget.py:384` | `def test_payload_schema_recognises_budget_keys()` |
| `test_read_budget_status_returns_dict` | function | `tests/test_llm_budget.py:287` | `def test_read_budget_status_returns_dict(tmp_sessions)` |
| `test_token_estimator_counts_text_tokens` | function | `tests/test_llm_budget.py:71` | `def test_token_estimator_counts_text_tokens()` |
| `test_token_estimator_handles_empty_string` | function | `tests/test_llm_budget.py:81` | `def test_token_estimator_handles_empty_string()` |
| `test_token_estimator_is_deterministic` | function | `tests/test_llm_budget.py:89` | `def test_token_estimator_is_deterministic()` |
| `test_wrap_backend_with_budget_charges_call` | function | `tests/test_llm_budget.py:347` | `def test_wrap_backend_with_budget_charges_call(tmp_sessions)` |
| `test_wrap_backend_with_budget_returns_same_shape` | function | `tests/test_llm_budget.py:307` | `def test_wrap_backend_with_budget_returns_same_shape(tmp_sessions)` |
| `tmp_sessions` | function | `tests/test_llm_budget.py:27` | `def tmp_sessions(tmp_path, monkeypatch)` |
| `TestBackendMetadataContract` | class | `tests/test_llm_contract.py:114` | `class TestBackendMetadataContract` |
| `TestDeadModuleRemoved` | class | `tests/test_llm_contract.py:50` | `class TestDeadModuleRemoved` |
| `TestLlmFactoryContract` | class | `tests/test_llm_contract.py:56` | `class TestLlmFactoryContract` |
| `TestSupportModulesContract` | class | `tests/test_llm_contract.py:86` | `class TestSupportModulesContract` |
| `_import` | function | `tests/test_llm_contract.py:46` | `def _import(name)` |
| `test_ai_fallback_exposes_public_api` | method | `tests/test_llm_contract.py:97` | `def test_ai_fallback_exposes_public_api(self)` |
| `test_ai_fallback_reads_factory_constants` | method | `tests/test_llm_contract.py:107` | `def test_ai_fallback_reads_factory_constants(self)` |
| `test_ai_model_exposes_all_backends` | method | `tests/test_llm_contract.py:102` | `def test_ai_model_exposes_all_backends(self)` |
| `test_api_key_slots` | method | `tests/test_llm_contract.py:144` | `def test_api_key_slots(self)` |
| `test_backend_constants_exposed` | method | `tests/test_llm_contract.py:69` | `def test_backend_constants_exposed(self)` |
| `test_default_models_match_constants` | method | `tests/test_llm_contract.py:125` | `def test_default_models_match_constants(self)` |
| `test_factory_exposes_public_api` | method | `tests/test_llm_contract.py:60` | `def test_factory_exposes_public_api(self)` |
| `test_factory_importable` | method | `tests/test_llm_contract.py:57` | `def test_factory_importable(self)` |
| `test_llm_client_class_methods_present` | method | `tests/test_llm_contract.py:92` | `def test_llm_client_class_methods_present(self)` |
| `test_llm_client_exposes_public_api` | method | `tests/test_llm_contract.py:87` | `def test_llm_client_exposes_public_api(self)` |
| `test_metadata_helpers_exposed` | method | `tests/test_llm_contract.py:115` | `def test_metadata_helpers_exposed(self)` |
| `test_model_config_keys_match_constants` | method | `tests/test_llm_contract.py:135` | `def test_model_config_keys_match_constants(self)` |
| `test_normalize_falls_back_to_auto_on_empty` | method | `tests/test_llm_contract.py:80` | `def test_normalize_falls_back_to_auto_on_empty(self)` |
| `test_normalize_rejects_unknown_backend` | method | `tests/test_llm_contract.py:75` | `def test_normalize_rejects_unknown_backend(self)` |
| `test_requires_api_key_only_for_cloud` | method | `tests/test_llm_contract.py:153` | `def test_requires_api_key_only_for_cloud(self)` |
| `test_supported_backends_are_canonical` | method | `tests/test_llm_contract.py:65` | `def test_supported_backends_are_canonical(self)` |
| `test_unified_llm_client_does_not_exist` | method | `tests/test_llm_contract.py:51` | `def test_unified_llm_client_does_not_exist(self)` |
| `test_unknown_backend_rejected` | method | `tests/test_llm_contract.py:159` | `def test_unknown_backend_rejected(self)` |
| `test_all_cooling_returns_soonest_so_progress_continues` | function | `tests/test_llm_key_pool.py:47` | `def test_all_cooling_returns_soonest_so_progress_continues()` |
| `test_build_from_config_seeds_primary_first` | function | `tests/test_llm_key_pool.py:56` | `def test_build_from_config_seeds_primary_first()` |
| `test_build_from_config_supports_per_backend_mapping` | function | `tests/test_llm_key_pool.py:63` | `def test_build_from_config_supports_per_backend_mapping()` |
| `test_exhausted_key_is_skipped_during_cooldown` | function | `tests/test_llm_key_pool.py:35` | `def test_exhausted_key_is_skipped_during_cooldown()` |
| `test_note_quota_error_parks_global_key` | function | `tests/test_llm_key_pool.py:91` | `def test_note_quota_error_parks_global_key()` |
| `test_placeholders_and_duplicates_are_dropped` | function | `tests/test_llm_key_pool.py:27` | `def test_placeholders_and_duplicates_are_dropped()` |
| `test_resolve_pooled_key_is_noop_without_a_pool` | function | `tests/test_llm_key_pool.py:76` | `def test_resolve_pooled_key_is_noop_without_a_pool()` |
| `test_resolve_pooled_key_rotates_with_a_pool` | function | `tests/test_llm_key_pool.py:82` | `def test_resolve_pooled_key_rotates_with_a_pool()` |
| `test_round_robin_cycles_keys_in_order` | function | `tests/test_llm_key_pool.py:19` | `def test_round_robin_cycles_keys_in_order()` |
| `TestNoLegacyGroqImportInCore` | class | `tests/test_llm_legacy_isolation.py:61` | `class TestNoLegacyGroqImportInCore` |
| `_core_source_files` | function | `tests/test_llm_legacy_isolation.py:33` | `def _core_source_files()` |
| `_imported_targets` | function | `tests/test_llm_legacy_isolation.py:47` | `def _imported_targets(node)` |
| `test_no_core_file_imports_legacy_groq` | method | `tests/test_llm_legacy_isolation.py:62` | `def test_no_core_file_imports_legacy_groq(self)` |
| `TestAdapterWiring` | class | `tests/test_llm_orchestrator.py:498` | `class TestAdapterWiring` |
| `TestAiFallbackIntegration` | class | `tests/test_llm_orchestrator.py:925` | `class TestAiFallbackIntegration` |
| `TestBackendKind` | class | `tests/test_llm_orchestrator.py:480` | `class TestBackendKind` |
| `TestC2Wiring` | class | `tests/test_llm_orchestrator.py:679` | `class TestC2Wiring` |
| `TestChainOrder` | class | `tests/test_llm_orchestrator.py:101` | `class TestChainOrder` |
| `TestErrorDetection` | class | `tests/test_llm_orchestrator.py:700` | `class TestErrorDetection` |
| `TestFailover` | class | `tests/test_llm_orchestrator.py:152` | `class TestFailover` |
| `TestGroqEnvKey` | class | `tests/test_llm_orchestrator.py:886` | `class TestGroqEnvKey` |
| `TestHealth` | class | `tests/test_llm_orchestrator.py:353` | `class TestHealth` |
| `TestLedger` | class | `tests/test_llm_orchestrator.py:448` | `class TestLedger` |
| `TestPlaceholderKeys` | class | `tests/test_llm_orchestrator.py:821` | `class TestPlaceholderKeys` |
| `_RecordingRegistry` | class | `tests/test_llm_orchestrator.py:432` | `class _RecordingRegistry` |
| `_StubHealth` | class | `tests/test_llm_orchestrator.py:59` | `class _StubHealth` |
| `__init__` | method | `tests/test_llm_orchestrator.py:62` | `def __init__(self, parked)` |
| `__init__` | method | `tests/test_llm_orchestrator.py:435` | `def __init__(self, seen)` |
| `_execute` | function | `tests/test_llm_orchestrator.py:78` | `def _execute(model_spec, prompt, max_tokens)` |
| `_explode` | function | `tests/test_llm_orchestrator.py:145` | `def _explode()` |
| `_member` | function | `tests/test_llm_orchestrator.py:89` | `def _member(name, model, priority)` |
| `_restore_groq_env` | function | `tests/test_llm_orchestrator.py:41` | `def _restore_groq_env()` |
| `_scripted_executor` | function | `tests/test_llm_orchestrator.py:77` | `def _scripted_executor(script, calls)` |
| `_spy` | function | `tests/test_llm_orchestrator.py:786` | `def _spy(model_spec, prompt, max_tokens)` |
| `cfg` | method | `tests/test_llm_orchestrator.py:500` | `def cfg(self, tmp_path)` |
| `executor` | function | `tests/test_llm_orchestrator.py:282` | `def executor(model_spec, prompt, max_tokens)` |
| `executor` | function | `tests/test_llm_orchestrator.py:302` | `def executor(model_spec, prompt, max_tokens)` |
| `healthy` | method | `tests/test_llm_orchestrator.py:67` | `def healthy(self, name)` |
| `healthy` | method | `tests/test_llm_orchestrator.py:438` | `def healthy(self, name)` |
| `isolated_pool` | function | `tests/test_llm_orchestrator.py:94` | `def isolated_pool(tmp_path, monkeypatch)` |
| `lazyc2_source` | function | `tests/test_llm_orchestrator.py:996` | `def lazyc2_source()` |
| `patched` | method | `tests/test_llm_orchestrator.py:512` | `def patched(self, cfg, monkeypatch)` |
| `report_failure` | method | `tests/test_llm_orchestrator.py:70` | `def report_failure(self, name, error)` |
| `report_failure` | method | `tests/test_llm_orchestrator.py:441` | `def report_failure(self, name, error)` |
| `report_success` | method | `tests/test_llm_orchestrator.py:73` | `def report_success(self, name)` |
| `report_success` | method | `tests/test_llm_orchestrator.py:444` | `def report_success(self, name)` |
| `test_ai_fallback_call_routes_through_the_chain` | method | `tests/test_llm_orchestrator.py:690` | `def test_ai_fallback_call_routes_through_the_chain(self)` |
| `test_all_members_fail_returns_error_result_without_raising` | method | `tests/test_llm_orchestrator.py:200` | `def test_all_members_fail_returns_error_result_without_raising(self)` |
| `test_all_unhealthy_members_still_get_attempted` | method | `tests/test_llm_orchestrator.py:371` | `def test_all_unhealthy_members_still_get_attempted(self)` |
| `test_analyze_functions_route_through_the_orchestrator` | method | `tests/test_llm_orchestrator.py:680` | `def test_analyze_functions_route_through_the_orchestrator(self)` |
| `test_ask_general_keeps_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:668` | `def test_ask_general_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_ask_general_serves_from_the_chain_when_backend_missing` | method | `tests/test_llm_orchestrator.py:650` | `def test_ask_general_serves_from_the_chain_when_backend_missing(self, patched, monkeypatch)` |
| `test_backend_kind_parses_spec_prefix` | method | `tests/test_llm_orchestrator.py:492` | `def test_backend_kind_parses_spec_prefix(self, spec, kind)` |
| `test_blank_reply_is_a_failure` | method | `tests/test_llm_orchestrator.py:236` | `def test_blank_reply_is_a_failure(self)` |
| `test_chain_uses_orchestrator_pool_when_no_override` | method | `tests/test_llm_orchestrator.py:316` | `def test_chain_uses_orchestrator_pool_when_no_override(self, isolated_pool)` |
| `test_client_401_error_string_falls_back_to_the_chain` | method | `tests/test_llm_orchestrator.py:589` | `def test_client_401_error_string_falls_back_to_the_chain(self, patched, monkeypatch)` |
| `test_client_401_keeps_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:616` | `def test_client_401_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_client_error_falls_back_to_the_chain` | method | `tests/test_llm_orchestrator.py:541` | `def test_client_error_falls_back_to_the_chain(self, patched, monkeypatch)` |
| `test_client_success_stays_primary_without_chain_call` | method | `tests/test_llm_orchestrator.py:567` | `def test_client_success_stays_primary_without_chain_call(self, patched, monkeypatch)` |
| `test_dedupes_members_by_name` | method | `tests/test_llm_orchestrator.py:337` | `def test_dedupes_members_by_name(self)` |
| `test_default_health_comes_from_shared_registry` | method | `tests/test_llm_orchestrator.py:414` | `def test_default_health_comes_from_shared_registry(self, isolated_pool, monkeypatch)` |
| `test_empty_prompt_short_circuits` | method | `tests/test_llm_orchestrator.py:262` | `def test_empty_prompt_short_circuits(self)` |
| `test_error_banner_text_is_a_failure_not_content` | method | `tests/test_llm_orchestrator.py:217` | `def test_error_banner_text_is_a_failure_not_content(self)` |
| `test_error_replies_detected` | method | `tests/test_llm_orchestrator.py:713` | `def test_error_replies_detected(self, reply)` |
| `test_exhausted_chain_degrades_to_local_ollama` | method | `tests/test_llm_orchestrator.py:969` | `def test_exhausted_chain_degrades_to_local_ollama(self, monkeypatch)` |
| `test_explicit_api_key_published_to_environment` | method | `tests/test_llm_orchestrator.py:887` | `def test_explicit_api_key_published_to_environment(self, monkeypatch)` |
| `test_factory_rejects_placeholder_env_key` | method | `tests/test_llm_orchestrator.py:841` | `def test_factory_rejects_placeholder_env_key(self, monkeypatch)` |
| `test_factory_rejects_placeholder_payload_key` | method | `tests/test_llm_orchestrator.py:832` | `def test_factory_rejects_placeholder_payload_key(self)` |
| `test_failure_is_recorded_in_the_pool_ledger` | method | `tests/test_llm_orchestrator.py:464` | `def test_failure_is_recorded_in_the_pool_ledger(self, isolated_pool)` |
| `test_failure_reports_health` | method | `tests/test_llm_orchestrator.py:400` | `def test_failure_reports_health(self)` |
| `test_fallback_answer_is_memorized_clean` | method | `tests/test_llm_orchestrator.py:634` | `def test_fallback_answer_is_memorized_clean(self, patched, monkeypatch, tmp_path)` |
| `test_invalid_api_key_reply_is_a_failure` | method | `tests/test_llm_orchestrator.py:756` | `def test_invalid_api_key_reply_is_a_failure(self)` |
| `test_long_pentest_plan_is_served_not_failed_over` | method | `tests/test_llm_orchestrator.py:735` | `def test_long_pentest_plan_is_served_not_failed_over(self)` |
| `test_max_tokens_is_forwarded` | method | `tests/test_llm_orchestrator.py:297` | `def test_max_tokens_is_forwarded(self)` |
| `test_missing_client_returns_legacy_error_when_chain_exhausted` | method | `tests/test_llm_orchestrator.py:534` | `def test_missing_client_returns_legacy_error_when_chain_exhausted(self, patched, monkeypatch)` |
| `test_missing_client_serves_from_the_chain` | method | `tests/test_llm_orchestrator.py:518` | `def test_missing_client_serves_from_the_chain(self, patched, monkeypatch)` |
| `test_orchestrator_module_exports_public_api` | function | `tests/test_llm_orchestrator.py:1004` | `def test_orchestrator_module_exports_public_api()` |
| `test_orchestrator_success_after_failure_carries_notice` | method | `tests/test_llm_orchestrator.py:947` | `def test_orchestrator_success_after_failure_carries_notice(self, monkeypatch)` |
| `test_orchestrator_success_maps_to_ai_result` | method | `tests/test_llm_orchestrator.py:926` | `def test_orchestrator_success_maps_to_ai_result(self, monkeypatch)` |
| `test_pentest_prose_with_unauthorized_word_is_content` | method | `tests/test_llm_orchestrator.py:723` | `def test_pentest_prose_with_unauthorized_word_is_content(self)` |
| `test_phishing_prose_with_credit_word_is_content` | method | `tests/test_llm_orchestrator.py:729` | `def test_phishing_prose_with_credit_word_is_content(self)` |
| `test_placeholder_env_replaced_by_payload_key` | method | `tests/test_llm_orchestrator.py:849` | `def test_placeholder_env_replaced_by_payload_key(self, monkeypatch)` |
| `test_placeholder_env_survives_without_payload_key` | method | `tests/test_llm_orchestrator.py:867` | `def test_placeholder_env_survives_without_payload_key(self, monkeypatch)` |
| `test_placeholder_fragments_recognized` | method | `tests/test_llm_orchestrator.py:822` | `def test_placeholder_fragments_recognized(self)` |
| `test_placeholder_groq_leg_refused_even_with_payload_key` | method | `tests/test_llm_orchestrator.py:802` | `def test_placeholder_groq_leg_refused_even_with_payload_key(self, monkeypatch)` |
| `test_placeholder_groq_leg_refused_without_doomed_call` | method | `tests/test_llm_orchestrator.py:776` | `def test_placeholder_groq_leg_refused_without_doomed_call(self, monkeypatch)` |
| `test_placeholder_payload_key_not_published` | method | `tests/test_llm_orchestrator.py:906` | `def test_placeholder_payload_key_not_published(self, monkeypatch)` |
| `test_pool_chain_reads_lazy_orchestrator_store` | method | `tests/test_llm_orchestrator.py:119` | `def test_pool_chain_reads_lazy_orchestrator_store(self, isolated_pool)` |
| `test_pool_chain_returns_empty_when_pool_unreadable` | method | `tests/test_llm_orchestrator.py:140` | `def test_pool_chain_returns_empty_when_pool_unreadable(self, monkeypatch)` |
| `test_pool_chain_self_heals_corrupt_store` | method | `tests/test_llm_orchestrator.py:132` | `def test_pool_chain_self_heals_corrupt_store(self, isolated_pool)` |

Next: [SYMBOLS_p46.md](SYMBOLS_p46.md)
