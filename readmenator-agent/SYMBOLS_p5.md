# Symbols (page 5 of 38)
Previous: [SYMBOLS_p4.md](SYMBOLS_p4.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_build_adjacency` | method | `cli/palette_graph.py:90` | `def _build_adjacency(document)` |
| `_command_name_from_label` | method | `cli/palette_graph.py:68` | `def _command_name_from_label(label)` |
| `_filter_neighbours` | method | `cli/palette_graph.py:161` | `def _filter_neighbours(neighbours)` |
| `_looks_like_command_label` | method | `cli/palette_graph.py:63` | `def _looks_like_command_label(label)` |
| `callees` | method | `cli/palette_graph.py:179` | `def callees(graph, command_name)` |
| `enrich_commands` | method | `cli/palette_graph.py:309` | `def enrich_commands(graph, rows)` |
| `enrich_detail` | method | `cli/palette_graph.py:287` | `def enrich_detail(graph, entry)` |
| `load_graph` | method | `cli/palette_graph.py:127` | `def load_graph(path)` |
| `related_commands` | method | `cli/palette_graph.py:226` | `def related_commands(graph, command_name)` |
| `safe_load_graph` | method | `cli/palette_graph.py:149` | `def safe_load_graph(path)` |
| `PaletteOverlayConfig` | class | `cli/palette_overlay.py:38` | `class PaletteOverlayConfig` |
| `PaletteOverlayState` | class | `cli/palette_overlay.py:70` | `class PaletteOverlayState` |
| `PaletteRow` | class | `cli/palette_overlay.py:59` | `class PaletteRow` |
| `_PaletteOverlayApp` | class | `cli/palette_overlay.py:240` | `class _PaletteOverlayApp(App)` |
| `__init__` | method | `cli/palette_overlay.py:255` | `def __init__(self)` |
| `_build_app` | method | `cli/palette_overlay.py:228` | `def _build_app(state, theme)` |
| `_commit_from_item` | method | `cli/palette_overlay.py:292` | `def _commit_from_item(self, item)` |
| `_format_row` | method | `cli/palette_overlay.py:314` | `def _format_row(self, row)` |
| `_load_index` | method | `cli/palette_overlay.py:151` | `def _load_index()` |
| `_load_recents` | method | `cli/palette_overlay.py:136` | `def _load_recents()` |
| `_refresh_rows` | method | `cli/palette_overlay.py:300` | `def _refresh_rows(self)` |
| `_score` | method | `cli/palette_overlay.py:113` | `def _score(self, name, summary, needle, is_recent)` |
| `_truncate` | method | `cli/palette_overlay.py:130` | `def _truncate(self, value, max_chars)` |
| `action_cancel` | method | `cli/palette_overlay.py:282` | `def action_cancel(self)` |
| `action_select_current` | method | `cli/palette_overlay.py:285` | `def action_select_current(self)` |
| `build_state` | method | `cli/palette_overlay.py:162` | `def build_state(payload, index, recents, config)` |
| `compose` | method | `cli/palette_overlay.py:261` | `def compose(self)` |
| `launch_overlay` | method | `cli/palette_overlay.py:188` | `def launch_overlay(payload, state, runner)` |
| `on_input_changed` | method | `cli/palette_overlay.py:272` | `def on_input_changed(self, event)` |
| `on_input_submitted` | method | `cli/palette_overlay.py:276` | `def on_input_submitted(self, event)` |
| `on_list_view_selected` | method | `cli/palette_overlay.py:279` | `def on_list_view_selected(self, event)` |
| `on_mount` | method | `cli/palette_overlay.py:269` | `def on_mount(self)` |
| `rows` | method | `cli/palette_overlay.py:87` | `def rows(self)` |
| `set_query` | method | `cli/palette_overlay.py:83` | `def set_query(self, value)` |
| `CommandStat` | class | `cli/palette_telemetry.py:61` | `class CommandStat` |
| `TelemetryConfig` | class | `cli/palette_telemetry.py:42` | `class TelemetryConfig` |
| `TelemetryIndex` | class | `cli/palette_telemetry.py:78` | `class TelemetryIndex` |
| `TelemetryIndexError` | class | `cli/palette_telemetry.py:37` | `class TelemetryIndexError(RuntimeError)` |
| `_build_index` | method | `cli/palette_telemetry.py:123` | `def _build_index(rows)` |
| `_normalise_command` | method | `cli/palette_telemetry.py:97` | `def _normalise_command(value)` |
| `_read_csv_rows` | method | `cli/palette_telemetry.py:107` | `def _read_csv_rows(path)` |
| `command_stats` | method | `cli/palette_telemetry.py:216` | `def command_stats(telemetry, command_name)` |
| `enrich_commands` | method | `cli/palette_telemetry.py:300` | `def enrich_commands(telemetry, rows)` |
| `enrich_detail` | method | `cli/palette_telemetry.py:275` | `def enrich_detail(telemetry, entry)` |
| `load_telemetry` | method | `cli/palette_telemetry.py:186` | `def load_telemetry(path)` |
| `recents` | method | `cli/palette_telemetry.py:259` | `def recents(telemetry)` |
| `runs_after` | method | `cli/palette_telemetry.py:239` | `def runs_after(telemetry, command_name)` |
| `safe_load_telemetry` | method | `cli/palette_telemetry.py:204` | `def safe_load_telemetry(path)` |
| `phase_label` | function | `cli/phase_labels.py:29` | `def phase_label(phase)` |
| `_load_ratings` | function | `cli/plugin_tiers.py:79` | `def _load_ratings(store)` |
| `default_store` | function | `cli/plugin_tiers.py:144` | `def default_store(base_dir)` |
| `format_rating` | function | `cli/plugin_tiers.py:137` | `def format_rating(average, count)` |
| `load_tier_manifest` | function | `cli/plugin_tiers.py:35` | `def load_tier_manifest(manifest)` |
| `rate_plugin` | function | `cli/plugin_tiers.py:98` | `def rate_plugin(name, stars, store)` |
| `rating_summary` | function | `cli/plugin_tiers.py:121` | `def rating_summary(name, store)` |
| `read_metadata_tier` | function | `cli/plugin_tiers.py:149` | `def read_metadata_tier(path)` |
| `tier_of` | function | `cli/plugin_tiers.py:61` | `def tier_of(name, manifest_tiers, metadata_tier)` |
| `ProTip` | class | `cli/protips.py:34` | `class ProTip` |
| `_after` | method | `cli/protips.py:75` | `def _after(ctx)` |
| `_has_api_key` | method | `cli/protips.py:59` | `def _has_api_key(ctx)` |
| `_has_domain` | method | `cli/protips.py:55` | `def _has_domain(ctx)` |
| `_has_rhost` | method | `cli/protips.py:51` | `def _has_rhost(ctx)` |
| `_last_cmd_is` | method | `cli/protips.py:67` | `def _last_cmd_is(ctx)` |
| `_os_linux` | method | `cli/protips.py:43` | `def _os_linux(ctx)` |
| `_os_windows` | method | `cli/protips.py:47` | `def _os_windows(ctx)` |
| `_phase_in` | method | `cli/protips.py:63` | `def _phase_in(ctx)` |
| `_safe_trigger` | method | `cli/protips.py:369` | `def _safe_trigger(tip, ctx)` |
| `get_session_tip` | method | `cli/protips.py:301` | `def get_session_tip(ctx)` |
| `print_session_tip` | method | `cli/protips.py:357` | `def print_session_tip(ctx)` |
| `render_contextual_tip` | method | `cli/protips.py:327` | `def render_contextual_tip(last_cmd, ctx)` |
| `PurpleDashboard` | class | `cli/purple_tui.py:79` | `class PurpleDashboard(App)` |
| `_color_rate` | function | `cli/purple_tui.py:70` | `def _color_rate(rate)` |
| `_dataset_stats` | function | `cli/purple_tui.py:56` | `def _dataset_stats()` |
| `_load_recent_results` | function | `cli/purple_tui.py:42` | `def _load_recent_results(n)` |
| `_load_score` | function | `cli/purple_tui.py:33` | `def _load_score()` |
| `_make_bar` | function | `cli/purple_tui.py:65` | `def _make_bar(value, width)` |
| `_render_actions` | method | `cli/purple_tui.py:173` | `def _render_actions(self, results)` |
| `_render_methods` | method | `cli/purple_tui.py:157` | `def _render_methods(self, score)` |
| `_render_score` | method | `cli/purple_tui.py:125` | `def _render_score(self, score)` |
| `_render_stats` | method | `cli/purple_tui.py:205` | `def _render_stats(self, score, ds)` |
| `action_refresh` | method | `cli/purple_tui.py:112` | `def action_refresh(self)` |
| `compose` | method | `cli/purple_tui.py:98` | `def compose(self)` |
| `launch` | method | `cli/purple_tui.py:233` | `def launch()` |
| `on_mount` | method | `cli/purple_tui.py:108` | `def on_mount(self)` |
| `refresh_data` | method | `cli/purple_tui.py:115` | `def refresh_data(self)` |
| `EvidenceHint` | class | `cli/reactive_hints.py:299` | `class EvidenceHint` |
| `_clean_reason` | method | `cli/reactive_hints.py:343` | `def _clean_reason(reasons)` |
| `_collect_command_hints` | method | `cli/reactive_hints.py:476` | `def _collect_command_hints(cmd, phase, already_run, limit)` |
| `_extract_labels` | function | `cli/reactive_hints.py:267` | `def _extract_labels(suggestions, limit)` |
| `_first_token` | function | `cli/reactive_hints.py:262` | `def _first_token(raw)` |
| `_render` | function | `cli/reactive_hints.py:284` | `def _render(labels)` |
| `_truncate` | function | `cli/reactive_hints.py:278` | `def _truncate(value, max_len)` |
| `build_evidence_hint_lines` | method | `cli/reactive_hints.py:416` | `def build_evidence_hint_lines(hints)` |
| `build_evidence_hints` | method | `cli/reactive_hints.py:362` | `def build_evidence_hints(recommendations, limit)` |
| `command_hints` | method | `cli/reactive_hints.py:549` | `def command_hints(last_command, phase, sessions_dir, limit)` |
| `confidence_from_score` | method | `cli/reactive_hints.py:321` | `def confidence_from_score(score)` |
| `read_run_commands` | method | `cli/reactive_hints.py:443` | `def read_run_commands(sessions_dir)` |
| `render_command_hints` | method | `cli/reactive_hints.py:514` | `def render_command_hints(last_command, phase, sessions_dir, limit, enabled)` |
| `render_evidence_hints` | method | `cli/reactive_hints.py:400` | `def render_evidence_hints(hints)` |
| `render_inline_hints` | function | `cli/reactive_hints.py:220` | `def render_inline_hints(advisor, last_command, limit, enabled)` |
| `ReasoningEntry` | class | `cli/reasoning_stream.py:66` | `class ReasoningEntry` |
| `_extract_reward` | method | `cli/reasoning_stream.py:175` | `def _extract_reward(payload)` |
| `_format_size` | method | `cli/reasoning_stream.py:134` | `def _format_size(num_bytes)` |
| `_format_time` | method | `cli/reasoning_stream.py:127` | `def _format_time(ts)` |
| `_summarize` | method | `cli/reasoning_stream.py:148` | `def _summarize(kind, payload)` |
| `_truncate` | method | `cli/reasoning_stream.py:141` | `def _truncate(text, limit)` |
| `event_to_entry` | method | `cli/reasoning_stream.py:183` | `def event_to_entry(event)` |
| `latest_hint` | method | `cli/reasoning_stream.py:229` | `def latest_hint(events_path)` |
| `latest_reasoning` | method | `cli/reasoning_stream.py:216` | `def latest_reasoning(path, limit)` |
| `read_raw_events` | method | `cli/reasoning_stream.py:91` | `def read_raw_events(path, limit)` |
| `CategoryResolver` | class | `cli/recommendation.py:192` | `class CategoryResolver` |
| `EngineWeights` | class | `cli/recommendation.py:67` | `class EngineWeights` |
| `Proposal` | class | `cli/recommendation.py:123` | `class Proposal` |
| `Recommendation` | class | `cli/recommendation.py:150` | `class Recommendation` |
| `RecommendationContext` | class | `cli/recommendation.py:101` | `class RecommendationContext` |
| `RecommendationEngine` | class | `cli/recommendation.py:232` | `class RecommendationEngine` |
| `RecommendationSignal` | class | `cli/recommendation.py:177` | `class RecommendationSignal(Protocol)` |
| `_Accumulator` | class | `cli/recommendation.py:362` | `class _Accumulator` |
| `__init__` | method | `cli/recommendation.py:201` | `def __init__(self, index_path, loader)` |
| `__init__` | method | `cli/recommendation.py:240` | `def __init__(self, signals, resolver, weights)` |
| `_build_category_priors` | method | `cli/recommendation.py:287` | `def _build_category_priors(self, collected)` |
| `_category_recommendations` | method | `cli/recommendation.py:331` | `def _category_recommendations(self, collected, concrete)` |
| `_clamp01` | method | `cli/recommendation.py:400` | `def _clamp01(value)` |
| `_fuse_concrete_actions` | method | `cli/recommendation.py:302` | `def _fuse_concrete_actions(self, collected, priors)` |
| `_load_command_index` | method | `cli/recommendation.py:422` | `def _load_command_index(path)` |
| `_non_negative` | method | `cli/recommendation.py:412` | `def _non_negative(value)` |
| `_safe_propose` | method | `cli/recommendation.py:280` | `def _safe_propose(signal, ctx)` |
| `add` | method | `cli/recommendation.py:374` | `def add(self, source, contribution, proposal)` |
| `build` | method | `cli/recommendation.py:386` | `def build(self)` |
| `category_for` | method | `cli/recommendation.py:227` | `def category_for(self, action)` |
| `propose` | method | `cli/recommendation.py:187` | `def propose(self, ctx)` |
| `recommend` | method | `cli/recommendation.py:258` | `def recommend(self, ctx)` |
| `GraphSignal` | class | `cli/recommendation_signals.py:110` | `class GraphSignal` |
| `GraphTopologySignal` | class | `cli/recommendation_signals.py:531` | `class GraphTopologySignal` |
| `KillChainSignal` | class | `cli/recommendation_signals.py:224` | `class KillChainSignal` |
| `KillchainGapSignal` | class | `cli/recommendation_signals.py:386` | `class KillchainGapSignal` |
| `PlaybookSignal` | class | `cli/recommendation_signals.py:337` | `class PlaybookSignal` |
| `PolicySignal` | class | `cli/recommendation_signals.py:148` | `class PolicySignal` |
| `ReconPlanSignal` | class | `cli/recommendation_signals.py:185` | `class ReconPlanSignal` |
| `__init__` | method | `cli/recommendation_signals.py:115` | `def __init__(self, advisor)` |
| `__init__` | method | `cli/recommendation_signals.py:153` | `def __init__(self, policy)` |
| `__init__` | method | `cli/recommendation_signals.py:190` | `def __init__(self, engine, builder)` |
| `__init__` | method | `cli/recommendation_signals.py:229` | `def __init__(self, next_table, phase_table)` |
| `__init__` | method | `cli/recommendation_signals.py:346` | `def __init__(self, playbook_engine)` |
| `__init__` | method | `cli/recommendation_signals.py:406` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `cli/recommendation_signals.py:542` | `def __init__(self, sessions_dir)` |
| `_build_killchain_signal` | method | `cli/recommendation_signals.py:785` | `def _build_killchain_signal()` |
| `_compute_centrality` | method | `cli/recommendation_signals.py:603` | `def _compute_centrality(graph_data)` |
| `_gap_creds_no_lateral` | method | `cli/recommendation_signals.py:507` | `def _gap_creds_no_lateral(self, wm_data, hosts)` |
| `_gap_exploited_no_privesc` | method | `cli/recommendation_signals.py:425` | `def _gap_exploited_no_privesc(self, hosts)` |
| `_gap_owned_no_creds` | method | `cli/recommendation_signals.py:465` | `def _gap_owned_no_creds(self, hosts, wm_data)` |
| `_gap_scan_no_enum` | method | `cli/recommendation_signals.py:485` | `def _gap_scan_no_enum(self, hosts, recent)` |
| `_load_world_model` | function | `cli/recommendation_signals.py:67` | `def _load_world_model(sessions_dir)` |
| `_rank_weight` | function | `cli/recommendation_signals.py:90` | `def _rank_weight(index, total)` |
| `_try_build_graph_signal` | method | `cli/recommendation_signals.py:742` | `def _try_build_graph_signal(graph_path)` |
| `_try_build_playbook_signal` | method | `cli/recommendation_signals.py:638` | `def _try_build_playbook_signal()` |
| `_try_build_policy_signal` | method | `cli/recommendation_signals.py:756` | `def _try_build_policy_signal()` |
| `_try_build_recon_signal` | method | `cli/recommendation_signals.py:772` | `def _try_build_recon_signal(payload)` |
| `build_context` | method | `cli/recommendation_signals.py:308` | `def build_context(payload, sessions_dir, target, limit)` |
| `build_default_engine` | method | `cli/recommendation_signals.py:649` | `def build_default_engine(payload, sessions_dir, graph_path, command_index_path, weights)` |
| `propose` | method | `cli/recommendation_signals.py:125` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:162` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:200` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:243` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:355` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:409` | `def propose(self, ctx)` |
| `propose` | method | `cli/recommendation_signals.py:545` | `def propose(self, ctx)` |
| `read_recent_commands` | method | `cli/recommendation_signals.py:275` | `def read_recent_commands(sessions_dir, window)` |
| `recommend_with_evidence` | method | `cli/recommendation_signals.py:705` | `def recommend_with_evidence(payload, sessions_dir, target, phase, limit, engine)` |
| `ReconPlan` | class | `cli/recon_plan.py:119` | `class ReconPlan` |
| `ReconPlanConfig` | class | `cli/recon_plan.py:62` | `class ReconPlanConfig` |
| `ReconPlanItem` | class | `cli/recon_plan.py:94` | `class ReconPlanItem` |
| `_addon_items` | method | `cli/recon_plan.py:330` | `def _addon_items(addons, services, payload)` |
| `_command_items` | method | `cli/recon_plan.py:367` | `def _command_items(index, phase, history, limit)` |
| `_default_command_index_loader` | method | `cli/recon_plan.py:494` | `def _default_command_index_loader(path)` |
| `_payload_target` | method | `cli/recon_plan.py:466` | `def _payload_target(payload, config)` |
| `_read_tool_command` | method | `cli/recon_plan.py:449` | `def _read_tool_command(source_path)` |
| `_resolve_phase` | method | `cli/recon_plan.py:474` | `def _resolve_phase(payload, config)` |
| `_safe_filename_component` | method | `cli/recon_plan.py:486` | `def _safe_filename_component(value)` |
| `_service_for_trigger` | method | `cli/recon_plan.py:414` | `def _service_for_trigger(trigger, services)` |
| `_tool_command_preview` | method | `cli/recon_plan.py:428` | `def _tool_command_preview(tool, payload)` |
| `_tool_items` | method | `cli/recon_plan.py:347` | `def _tool_items(tools, services, payload)` |
| `build_recon_plan` | method | `cli/recon_plan.py:144` | `def build_recon_plan(target, engine, payload, config, command_index_loader, clock)` |
| `is_empty` | method | `cli/recon_plan.py:139` | `def is_empty(self)` |
| `render_markdown` | method | `cli/recon_plan.py:207` | `def render_markdown(plan)` |
| `render_rich` | method | `cli/recon_plan.py:299` | `def render_rich(plan, console)` |
| `write_plan` | method | `cli/recon_plan.py:257` | `def write_plan(plan, sessions_dir, config)` |
| `iter_command_sets` | function | `cli/registry.py:41` | `def iter_command_sets(include_pending)` |
| `register_command_sets` | function | `cli/registry.py:77` | `def register_command_sets(shell)` |
| `ScopeDecision` | class | `cli/scope_guard.py:104` | `class ScopeDecision` |
| `ScopeGuard` | class | `cli/scope_guard.py:233` | `class ScopeGuard` |
| `ScopeMode` | class | `cli/scope_guard.py:69` | `class ScopeMode(StrEnum)` |
| `__init__` | method | `cli/scope_guard.py:242` | `def __init__(self, scope_entries, mode, is_offensive)` |
| `_hostname_match` | method | `cli/scope_guard.py:188` | `def _hostname_match(target, entry)` |
| `_parse_ip` | method | `cli/scope_guard.py:174` | `def _parse_ip(value)` |
| `_parse_network` | method | `cli/scope_guard.py:181` | `def _parse_network(value)` |
| `build_offensive_commands` | method | `cli/scope_guard.py:126` | `def build_offensive_commands(command_categories)` |
| `evaluate` | method | `cli/scope_guard.py:262` | `def evaluate(self, command, target)` |
| `from_value` | method | `cli/scope_guard.py:84` | `def from_value(cls, value)` |
| `normalize_scope` | method | `cli/scope_guard.py:142` | `def normalize_scope(entries)` |
| `target_in_scope` | method | `cli/scope_guard.py:197` | `def target_in_scope(target, entries)` |
| `HudConfig` | class | `cli/session_hud.py:25` | `class HudConfig` |
| `HudSnapshot` | class | `cli/session_hud.py:50` | `class HudSnapshot` |
| `_engagement_facts` | method | `cli/session_hud.py:135` | `def _engagement_facts()` |
| `build_snapshot` | method | `cli/session_hud.py:155` | `def build_snapshot(params, config)` |
| `count_csv_rows` | method | `cli/session_hud.py:83` | `def count_csv_rows(path)` |
| `count_lines_in_globs` | method | `cli/session_hud.py:62` | `def count_lines_in_globs(root, patterns)` |
| `format_elapsed` | method | `cli/session_hud.py:100` | `def format_elapsed(seconds)` |
| `phase_bar` | method | `cli/session_hud.py:115` | `def phase_bar(phase, width)` |
| `render_snapshot` | method | `cli/session_hud.py:180` | `def render_snapshot(snapshot, config)` |
| `SessionResumer` | class | `cli/session_resumer.py:51` | `class SessionResumer` |
| `SessionResumerConfig` | class | `cli/session_resumer.py:41` | `class SessionResumerConfig` |
| `SessionSummary` | class | `cli/session_resumer.py:29` | `class SessionSummary` |
| `__init__` | method | `cli/session_resumer.py:58` | `def __init__(self, config)` |
| `_discover_targets` | method | `cli/session_resumer.py:62` | `def _discover_targets(self)` |
| `render_startup_panel` | method | `cli/session_resumer.py:129` | `def render_startup_panel(self)` |
| `CategorySpec` | class | `cli/sessions_browser.py:33` | `class CategorySpec` |
| `SessionEntry` | class | `cli/sessions_browser.py:76` | `class SessionEntry` |
| `SessionPreview` | class | `cli/sessions_browser.py:185` | `class SessionPreview` |
| `SessionsBrowserConfig` | class | `cli/sessions_browser.py:49` | `class SessionsBrowserConfig` |
| `SessionsBrowserState` | class | `cli/sessions_browser.py:225` | `class SessionsBrowserState` |
| `SessionsIndex` | class | `cli/sessions_browser.py:85` | `class SessionsIndex` |
| `_SessionsBrowserApp` | class | `cli/sessions_browser.py:325` | `class _SessionsBrowserApp(App)` |
| `__init__` | method | `cli/sessions_browser.py:88` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/sessions_browser.py:188` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/sessions_browser.py:340` | `def __init__(self)` |
| `_build_app` | method | `cli/sessions_browser.py:314` | `def _build_app(state, theme)` |
| `_build_entry` | method | `cli/sessions_browser.py:160` | `def _build_entry(self, path, relative, category)` |
| `_collect_other` | method | `cli/sessions_browser.py:142` | `def _collect_other(self, claimed)` |
| `_entries_for` | method | `cli/sessions_browser.py:119` | `def _entries_for(self, patterns, spec)` |
| `_label` | method | `cli/sessions_browser.py:172` | `def _label(self, relative)` |
| `_rebuild_tree` | method | `cli/sessions_browser.py:376` | `def _rebuild_tree(self)` |
| `_relative` | method | `cli/sessions_browser.py:178` | `def _relative(self, path)` |
| `_show_preview` | method | `cli/sessions_browser.py:399` | `def _show_preview(self, relative)` |
| `action_close` | method | `cli/sessions_browser.py:373` | `def action_close(self)` |
| `action_refresh` | method | `cli/sessions_browser.py:370` | `def action_refresh(self)` |
| `build_state` | method | `cli/sessions_browser.py:258` | `def build_state(payload, sessions_dir, config)` |
| `categories` | method | `cli/sessions_browser.py:104` | `def categories(self)` |
| `category_label` | method | `cli/sessions_browser.py:248` | `def category_label(self, identifier)` |
| `compose` | method | `cli/sessions_browser.py:346` | `def compose(self)` |
| `grouped_entries` | method | `cli/sessions_browser.py:233` | `def grouped_entries(self)` |
| `launch_browser` | method | `cli/sessions_browser.py:281` | `def launch_browser(payload, state, runner)` |
| `on_input_changed` | method | `cli/sessions_browser.py:359` | `def on_input_changed(self, event)` |
| `on_mount` | method | `cli/sessions_browser.py:356` | `def on_mount(self)` |
| `on_tree_node_selected` | method | `cli/sessions_browser.py:363` | `def on_tree_node_selected(self, event)` |
| `read` | method | `cli/sessions_browser.py:193` | `def read(self, relative)` |
| `root` | method | `cli/sessions_browser.py:100` | `def root(self)` |
| `format_payload` | function | `cli/show.py:14` | `def format_payload(params)` |
| `InstantEffect` | class | `cli/splash.py:141` | `class InstantEffect` |
| `SplashConfig` | class | `cli/splash.py:37` | `class SplashConfig` |
| `SplashEffect` | class | `cli/splash.py:62` | `class SplashEffect(Protocol)` |
| `TypewriterEffect` | class | `cli/splash.py:80` | `class TypewriterEffect` |
| `_redraw` | method | `cli/splash.py:119` | `def _redraw(console, accumulated, caret, tokens)` |
| `render` | method | `cli/splash.py:71` | `def render(self, console, lines, tokens, config)` |
| `render` | method | `cli/splash.py:90` | `def render(self, console, lines, tokens, config)` |
| `render` | method | `cli/splash.py:150` | `def render(self, console, lines, tokens, config)` |
| `render_splash` | method | `cli/splash.py:166` | `def render_splash(console, lines, payload, config, effect_name)` |
| `CollabPresenceSource` | class | `cli/status_bar.py:590` | `class CollabPresenceSource` |
| `CommandHintSuggestionSource` | class | `cli/status_bar.py:416` | `class CommandHintSuggestionSource` |
| `FileSystemReader` | class | `cli/status_bar.py:151` | `class FileSystemReader` |
| `GraphSuggestionSource` | class | `cli/status_bar.py:508` | `class GraphSuggestionSource` |
| `IStatusSource` | class | `cli/status_bar.py:143` | `class IStatusSource(Protocol)` |
| `PayloadTargetSource` | class | `cli/status_bar.py:268` | `class PayloadTargetSource` |
| `SessionFindingSource` | class | `cli/status_bar.py:319` | `class SessionFindingSource` |
| `StatusBarConfig` | class | `cli/status_bar.py:41` | `class StatusBarConfig` |
| `StatusBarManager` | class | `cli/status_bar.py:744` | `class StatusBarManager` |
| `StatusBarRenderer` | class | `cli/status_bar.py:656` | `class StatusBarRenderer` |
| `StatusContext` | class | `cli/status_bar.py:127` | `class StatusContext` |
| `WorldModelPhaseSource` | class | `cli/status_bar.py:292` | `class WorldModelPhaseSource` |
| `__init__` | method | `cli/status_bar.py:160` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/status_bar.py:271` | `def __init__(self, config, payload)` |
| `__init__` | method | `cli/status_bar.py:295` | `def __init__(self, config, reader, payload)` |
| `__init__` | method | `cli/status_bar.py:322` | `def __init__(self, config, reader)` |
| `__init__` | method | `cli/status_bar.py:426` | `def __init__(self, config, reader, phase_provider, hint_provider)` |
| `__init__` | method | `cli/status_bar.py:511` | `def __init__(self, config, reader, advisor_factory)` |
| `__init__` | method | `cli/status_bar.py:601` | `def __init__(self, config, reader, clock)` |
| `__init__` | method | `cli/status_bar.py:659` | `def __init__(self, config)` |
| `__init__` | method | `cli/status_bar.py:752` | `def __init__(self, config, sources, renderer, payload)` |
| `_build_precmd_hook` | method | `cli/status_bar.py:895` | `def _build_precmd_hook(self, shell, base_prompt, base_prompt_attribute, prompt_attribute)` |
| `_default_provider` | method | `cli/status_bar.py:500` | `def _default_provider()` |
| `_extract_entries` | method | `cli/status_bar.py:636` | `def _extract_entries(payload)` |
| `_extract_vuln_items` | method | `cli/status_bar.py:396` | `def _extract_vuln_items(self, payload)` |
| `_fallback_for` | method | `cli/status_bar.py:938` | `def _fallback_for(self, key)` |
| `_has_traversal` | method | `cli/status_bar.py:261` | `def _has_traversal(value)` |
| `_hook` | method | `cli/status_bar.py:915` | `def _hook(data)` |
| `_is_active` | method | `cli/status_bar.py:646` | `def _is_active(entry, threshold)` |
| `_is_within_root` | method | `cli/status_bar.py:253` | `def _is_within_root(self, candidate)` |
| `_last_line` | method | `cli/status_bar.py:376` | `def _last_line(self, path)` |
| `_latest_command` | method | `cli/status_bar.py:476` | `def _latest_command(self)` |
| `_latest_credential` | method | `cli/status_bar.py:335` | `def _latest_credential(self)` |
| `_latest_note` | method | `cli/status_bar.py:358` | `def _latest_note(self)` |
| `_latest_vuln` | method | `cli/status_bar.py:345` | `def _latest_vuln(self)` |
| `_operator_presence_enabled` | method | `cli/status_bar.py:948` | `def _operator_presence_enabled(payload, config)` |
| `_recent_commands` | method | `cli/status_bar.py:551` | `def _recent_commands(self)` |
| `_resolve_theme_colors` | method | `cli/status_bar.py:823` | `def _resolve_theme_colors(self)` |
| `_safe_collect` | method | `cli/status_bar.py:929` | `def _safe_collect(self, key)` |
| `_safe_path` | method | `cli/status_bar.py:247` | `def _safe_path(self, relative)` |
| `_sanitise` | method | `cli/status_bar.py:724` | `def _sanitise(self, value, max_chars)` |
| `_suggestion_label` | method | `cli/status_bar.py:579` | `def _suggestion_label(entry)` |
| `_summarise_credential` | method | `cli/status_bar.py:389` | `def _summarise_credential(self, filename, line)` |
| `build_default_manager` | method | `cli/status_bar.py:969` | `def build_default_manager(payload, sessions_dir, advisor_factory, config)` |
| `collect` | method | `cli/status_bar.py:146` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:283` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:306` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:327` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:451` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:530` | `def collect(self)` |
| `collect` | method | `cli/status_bar.py:622` | `def collect(self)` |
| `collect_context` | method | `cli/status_bar.py:798` | `def collect_context(self)` |
| `enabled` | method | `cli/status_bar.py:783` | `def enabled(self)` |
| `from_payload` | method | `cli/status_bar.py:99` | `def from_payload(cls, payload)` |
| `glob_latest` | method | `cli/status_bar.py:222` | `def glob_latest(self, pattern)` |
| `install` | method | `cli/status_bar.py:857` | `def install(self, shell, base_prompt_attribute, prompt_attribute)` |
| `read_json` | method | `cli/status_bar.py:204` | `def read_json(self, relative)` |
| `read_text` | method | `cli/status_bar.py:183` | `def read_text(self, relative)` |
| `render_plain` | method | `cli/status_bar.py:664` | `def render_plain(self, ctx)` |
| `render_plain_line` | method | `cli/status_bar.py:833` | `def render_plain_line(self, ctx)` |
| `render_prompt` | method | `cli/status_bar.py:687` | `def render_prompt(self, ctx, base_prompt, color_open, color_close, readline_safe)` |
| `render_prompt` | method | `cli/status_bar.py:811` | `def render_prompt(self, base_prompt, readline_safe)` |
| `root` | method | `cli/status_bar.py:179` | `def root(self)` |
| `set_enabled` | method | `cli/status_bar.py:847` | `def set_enabled(self, enabled)` |
| `active_tokens` | function | `cli/style.py:68` | `def active_tokens(payload)` |
| `paint` | function | `cli/style.py:84` | `def paint(text, token, payload)` |
| `render_prompt` | function | `cli/style.py:98` | `def render_prompt(console, segments, payload)` |
| `style` | function | `cli/style.py:49` | `def style(token, theme)` |
| `SurfaceEdge` | class | `cli/surface_graph.py:113` | `class SurfaceEdge` |
| `SurfaceGraph` | class | `cli/surface_graph.py:126` | `class SurfaceGraph` |
| `SurfaceGraphBuilder` | class | `cli/surface_graph.py:196` | `class SurfaceGraphBuilder` |
| `SurfaceGraphConfig` | class | `cli/surface_graph.py:174` | `class SurfaceGraphConfig` |
| `SurfaceNode` | class | `cli/surface_graph.py:87` | `class SurfaceNode` |
| `__init__` | method | `cli/surface_graph.py:199` | `def __init__(self, config)` |
| `_build_c2_node` | method | `cli/surface_graph.py:341` | `def _build_c2_node(self, local_ips, payload)` |
| `_client_label` | method | `cli/surface_graph.py:620` | `def _client_label(client_id, meta)` |
| `_discover_local_ips` | method | `cli/surface_graph.py:359` | `def _discover_local_ips(self)` |
| `_fallback_local_ips` | method | `cli/surface_graph.py:380` | `def _fallback_local_ips()` |
| `_is_ipv4` | method | `cli/surface_graph.py:614` | `def _is_ipv4(value)` |
| `_kind_order` | method | `cli/surface_graph.py:331` | `def _kind_order(kind)` |
| `_load_payload` | method | `cli/surface_graph.py:386` | `def _load_payload(self)` |
| `_parse_implant_row` | method | `cli/surface_graph.py:557` | `def _parse_implant_row(self, row)` |
| `_parse_port_scan` | method | `cli/surface_graph.py:578` | `def _parse_port_scan(self, raw)` |
| `_read_hostsdiscovery` | method | `cli/surface_graph.py:414` | `def _read_hostsdiscovery(self, local_ips)` |
| `_read_implants` | method | `cli/surface_graph.py:523` | `def _read_implants(self)` |
| `_read_last_implant_row` | method | `cli/surface_graph.py:540` | `def _read_last_implant_row(self, path)` |
| `_read_os_hint` | method | `cli/surface_graph.py:399` | `def _read_os_hint(self)` |
| `_read_scan_csv` | method | `cli/surface_graph.py:442` | `def _read_scan_csv(self, local_ips)` |
| `_read_scan_discovery` | method | `cli/surface_graph.py:436` | `def _read_scan_discovery(self, local_ips)` |
| `_read_scan_nmap` | method | `cli/surface_graph.py:467` | `def _read_scan_nmap(self, local_ips)` |
| `_slug_host` | function | `cli/surface_graph.py:75` | `def _slug_host(ip)` |
| `_slug_port` | function | `cli/surface_graph.py:80` | `def _slug_port(host_id, port, protocol)` |
| `build` | method | `cli/surface_graph.py:202` | `def build(self)` |
| `build_surface_graph` | method | `cli/surface_graph.py:631` | `def build_surface_graph(sessions_dir, payload_path)` |
| `children_of` | method | `cli/surface_graph.py:153` | `def children_of(self, node_id)` |
| `get` | method | `cli/surface_graph.py:165` | `def get(self, node_id)` |
| `iter_descendants` | method | `cli/surface_graph.py:648` | `def iter_descendants(graph, root_id)` |
| `stats` | method | `cli/surface_graph.py:146` | `def stats(self)` |
| `to_dict` | method | `cli/surface_graph.py:102` | `def to_dict(self)` |
| `to_dict` | method | `cli/surface_graph.py:120` | `def to_dict(self)` |
| `to_dict` | method | `cli/surface_graph.py:135` | `def to_dict(self)` |
| `SurfaceExplorer` | class | `cli/surface_tui.py:130` | `class SurfaceExplorer(App)` |
| `TextualNotInstalled` | class | `cli/surface_tui.py:61` | `class TextualNotInstalled(RuntimeError)` |
| `__init__` | method | `cli/surface_tui.py:148` | `def __init__(self, sessions_dir, payload_path)` |
| `_add_children` | method | `cli/surface_tui.py:205` | `def _add_children(self, parent_node, graph, parent_id)` |
| `_attach_children` | method | `cli/surface_tui.py:223` | `def _attach_children(parent, graph, parent_id, seen)` |
| `_build_rich_tree` | method | `cli/surface_tui.py:214` | `def _build_rich_tree(graph)` |
| `_reload_graph` | method | `cli/surface_tui.py:185` | `def _reload_graph(self)` |
| `_render_node_detail` | method | `cli/surface_tui.py:260` | `def _render_node_detail(data)` |
| `_stats_table` | method | `cli/surface_tui.py:241` | `def _stats_table(graph)` |
| `_styled_label` | method | `cli/surface_tui.py:232` | `def _styled_label(node)` |
| `action_collapse_all` | method | `cli/surface_tui.py:172` | `def action_collapse_all(self)` |
| `action_expand_all` | method | `cli/surface_tui.py:168` | `def action_expand_all(self)` |
| `action_refresh` | method | `cli/surface_tui.py:164` | `def action_refresh(self)` |
| `compose` | method | `cli/surface_tui.py:154` | `def compose(self)` |
| `launch_tui` | method | `cli/surface_tui.py:112` | `def launch_tui(sessions_dir, payload_path)` |
| `on_mount` | method | `cli/surface_tui.py:161` | `def on_mount(self)` |
| `on_tree_node_selected` | method | `cli/surface_tui.py:176` | `def on_tree_node_selected(self, event)` |
| `render_json` | method | `cli/surface_tui.py:92` | `def render_json(graph, sessions_dir, payload_path)` |
| `render_static` | method | `cli/surface_tui.py:65` | `def render_static(graph, sessions_dir, payload_path, console)` |
| `Theme` | class | `cli/themes.py:31` | `class Theme` |
| `get_theme` | method | `cli/themes.py:222` | `def get_theme(name)` |
| `theme_from_payload` | method | `cli/themes.py:238` | `def theme_from_payload(payload)` |
| `TimelineColumn` | class | `cli/timeline_browser.py:33` | `class TimelineColumn` |
| `TimelineConfig` | class | `cli/timeline_browser.py:43` | `class TimelineConfig` |
| `TimelineEntry` | class | `cli/timeline_browser.py:65` | `class TimelineEntry` |
| `TimelineReader` | class | `cli/timeline_browser.py:72` | `class TimelineReader` |
| `TimelineState` | class | `cli/timeline_browser.py:122` | `class TimelineState` |
| `_TimelineBrowserApp` | class | `cli/timeline_browser.py:213` | `class _TimelineBrowserApp(App)` |
| `__init__` | method | `cli/timeline_browser.py:75` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/timeline_browser.py:228` | `def __init__(self)` |
| `_build_app` | method | `cli/timeline_browser.py:202` | `def _build_app(state, theme)` |
| `_coerce_row` | method | `cli/timeline_browser.py:103` | `def _coerce_row(self, row)` |
| `_rebuild_rows` | method | `cli/timeline_browser.py:266` | `def _rebuild_rows(self)` |
| `_refresh_detail` | method | `cli/timeline_browser.py:278` | `def _refresh_detail(self, row_index)` |
| `action_close` | method | `cli/timeline_browser.py:263` | `def action_close(self)` |
| `action_refresh` | method | `cli/timeline_browser.py:259` | `def action_refresh(self)` |
| `build_state` | method | `cli/timeline_browser.py:157` | `def build_state(payload, sessions_dir, config)` |
| `column_value` | method | `cli/timeline_browser.py:148` | `def column_value(self, entry, column)` |
| `compose` | method | `cli/timeline_browser.py:234` | `def compose(self)` |
| `entries` | method | `cli/timeline_browser.py:134` | `def entries(self)` |
| `launch_scrubber` | method | `cli/timeline_browser.py:169` | `def launch_scrubber(payload, state, runner)` |
| `on_data_table_row_highlighted` | method | `cli/timeline_browser.py:253` | `def on_data_table_row_highlighted(self, event)` |
| `on_input_changed` | method | `cli/timeline_browser.py:249` | `def on_input_changed(self, event)` |
| `on_mount` | method | `cli/timeline_browser.py:242` | `def on_mount(self)` |
| `read` | method | `cli/timeline_browser.py:85` | `def read(self)` |
| `reload` | method | `cli/timeline_browser.py:130` | `def reload(self)` |
| `root` | method | `cli/timeline_browser.py:81` | `def root(self)` |
| `TipsConfig` | class | `cli/tips_engine.py:137` | `class TipsConfig` |
| `TipsEngine` | class | `cli/tips_engine.py:186` | `class TipsEngine` |
| `__init__` | method | `cli/tips_engine.py:194` | `def __init__(self, config, autosuggest_engine)` |
| `_award_elo` | method | `cli/tips_engine.py:808` | `def _award_elo(self, cmd, first_time, new_phase, phase)` |
| `_check_badges` | method | `cli/tips_engine.py:840` | `def _check_badges(self, cmd, first_time)` |
| `_check_karma_up` | method | `cli/tips_engine.py:819` | `def _check_karma_up(self)` |
| `_collect_killchain_progress` | method | `cli/tips_engine.py:575` | `def _collect_killchain_progress(self, current_phase)` |
| `_commands_in_exploration_phase` | method | `cli/tips_engine.py:707` | `def _commands_in_exploration_phase(self, phase)` |
| `_compute_command_hints` | method | `cli/tips_engine.py:616` | `def _compute_command_hints(self, cmd, phase)` |
| `_compute_evidence_hints` | method | `cli/tips_engine.py:529` | `def _compute_evidence_hints(self, cmd, phase)` |
| `_ensure_state_and_index` | method | `cli/tips_engine.py:926` | `def _ensure_state_and_index(self)` |
| `_fire_vri_reward` | method | `cli/tips_engine.py:877` | `def _fire_vri_reward(self, ctx)` |
| `_flush_suggestions_panel` | method | `cli/tips_engine.py:311` | `def _flush_suggestions_panel(self)` |
| `_get_hints_level` | method | `cli/tips_engine.py:344` | `def _get_hints_level(self)` |
| `_get_karma_name` | method | `cli/tips_engine.py:1045` | `def _get_karma_name(elo)` |
| `_get_rec_engine` | method | `cli/tips_engine.py:505` | `def _get_rec_engine(self)` |
| `_is_recordable_command` | method | `cli/tips_engine.py:987` | `def _is_recordable_command(self, cmd)` |
| `_load_command_index` | method | `cli/tips_engine.py:977` | `def _load_command_index(self)` |
| `_load_payload` | method | `cli/tips_engine.py:492` | `def _load_payload(self)` |
| `_load_state` | method | `cli/tips_engine.py:932` | `def _load_state(self)` |
| `_maybe_auto_show_killchain` | method | `cli/tips_engine.py:272` | `def _maybe_auto_show_killchain(self, phase)` |
| `_maybe_show_full_killchain` | method | `cli/tips_engine.py:605` | `def _maybe_show_full_killchain(self, cmd)` |
| `_next_threshold` | method | `cli/tips_engine.py:1051` | `def _next_threshold(self, current)` |
| `_noop` | function | `cli/tips_engine.py:132` | `def _noop()` |
| `_phase_for_cmd` | method | `cli/tips_engine.py:1028` | `def _phase_for_cmd(self, cmd)` |
| `_pick_weighted` | method | `cli/tips_engine.py:907` | `def _pick_weighted(rewards, weights)` |
| `_print_badge` | method | `cli/tips_engine.py:867` | `def _print_badge(self, name, description)` |
| `_print_separator` | method | `cli/tips_engine.py:836` | `def _print_separator(self, width)` |
| `_read_os_id_from_session` | method | `cli/tips_engine.py:388` | `def _read_os_id_from_session(self)` |
| `_read_recent_commands_for_autosuggest` | method | `cli/tips_engine.py:1010` | `def _read_recent_commands_for_autosuggest(self, limit)` |
| `_read_run_commands` | method | `cli/tips_engine.py:1005` | `def _read_run_commands(self)` |
| `_read_world_model_phase` | method | `cli/tips_engine.py:378` | `def _read_world_model_phase(self)` |
| `_refresh_autosuggest` | method | `cli/tips_engine.py:726` | `def _refresh_autosuggest(self, cmd, phase)` |
| `_render_arsenal_tip` | method | `cli/tips_engine.py:1180` | `def _render_arsenal_tip(ctx, state, config)` |
| `_render_autosuggest_hint` | method | `cli/tips_engine.py:750` | `def _render_autosuggest_hint(self, engine)` |
| `_render_contextual_tip` | method | `cli/tips_engine.py:633` | `def _render_contextual_tip(self, cmd, phase)` |
| `_render_exploration` | method | `cli/tips_engine.py:1124` | `def _render_exploration(ctx, state, config)` |
| `_render_hidden_feature` | method | `cli/tips_engine.py:1160` | `def _render_hidden_feature(ctx, state, config)` |
| `_render_kill_chain_hints` | method | `cli/tips_engine.py:475` | `def _render_kill_chain_hints(self, cmd, phase)` |
| `_render_phase_badge` | method | `cli/tips_engine.py:1142` | `def _render_phase_badge(ctx, state, config)` |
| `_render_streak` | method | `cli/tips_engine.py:1103` | `def _render_streak(ctx, state, config)` |
| `_resolve_phase` | method | `cli/tips_engine.py:355` | `def _resolve_phase(self, cmd, fallback)` |
| `_resolve_theme` | method | `cli/tips_engine.py:300` | `def _resolve_theme(self)` |
| `_run_curiosity_reveal` | method | `cli/tips_engine.py:683` | `def _run_curiosity_reveal(self, cmd, phase)` |
| `_safe_tip_trigger` | method | `cli/tips_engine.py:672` | `def _safe_tip_trigger(tip, ctx)` |
| `_sanitize_seen` | method | `cli/tips_engine.py:991` | `def _sanitize_seen(self, names, known)` |
| `_save_state` | method | `cli/tips_engine.py:952` | `def _save_state(self)` |
| `_summary_for_exploration_cmd` | method | `cli/tips_engine.py:713` | `def _summary_for_exploration_cmd(self, cmd)` |
| `_sync_user_elo` | method | `cli/tips_engine.py:1055` | `def _sync_user_elo(self, delta)` |
| `_truncate` | method | `cli/tips_engine.py:1039` | `def _truncate(value, max_len)` |
| `_update_engagement_state` | method | `cli/tips_engine.py:767` | `def _update_engagement_state(self, cmd, phase)` |
| `build_default_tips_config` | method | `cli/tips_engine.py:1240` | `def build_default_tips_config()` |
| `enabled` | method | `cli/tips_engine.py:221` | `def enabled(self)` |
| `get_state_snapshot` | method | `cli/tips_engine.py:440` | `def get_state_snapshot(self)` |
| `heal_commands_seen` | method | `cli/tips_engine.py:460` | `def heal_commands_seen(self, known)` |
| `render` | method | `cli/tips_engine.py:229` | `def render(self, cmd, phase)` |
| `render_session_start` | method | `cli/tips_engine.py:408` | `def render_session_start(self, phase, os_id)` |
| `reset_session` | method | `cli/tips_engine.py:455` | `def reset_session(self)` |
| `set_enabled` | method | `cli/tips_engine.py:225` | `def set_enabled(self, value)` |
| `ToastBus` | class | `cli/toast_bus.py:488` | `class ToastBus` |
| `ToastConfig` | class | `cli/toast_bus.py:43` | `class ToastConfig` |
| `ToastEvent` | class | `cli/toast_bus.py:110` | `class ToastEvent` |
| `ToastFormatter` | class | `cli/toast_bus.py:316` | `class ToastFormatter` |
| `ToastReader` | class | `cli/toast_bus.py:203` | `class ToastReader` |
| `ToastState` | class | `cli/toast_bus.py:121` | `class ToastState` |
| `__init__` | method | `cli/toast_bus.py:129` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/toast_bus.py:206` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/toast_bus.py:319` | `def __init__(self, config, theme)` |
| `__init__` | method | `cli/toast_bus.py:495` | `def __init__(self, config, state, reader, formatter, console)` |
| `_budget` | method | `cli/toast_bus.py:664` | `def _budget(payload, config)` |
| `_build_event` | method | `cli/toast_bus.py:267` | `def _build_event(self, line, source, offset)` |
| `_coerce_str` | method | `cli/toast_bus.py:288` | `def _coerce_str(value)` |
| `_console_width` | method | `cli/toast_bus.py:469` | `def _console_width(self)` |
| `_ensure_loaded` | method | `cli/toast_bus.py:182` | `def _ensure_loaded(self)` |
| `_erase_lines` | method | `cli/toast_bus.py:607` | `def _erase_lines(stream, rows)` |
| `_is_dumb_stream` | method | `cli/toast_bus.py:636` | `def _is_dumb_stream(stream)` |
| `_is_truthy` | method | `cli/toast_bus.py:622` | `def _is_truthy(value, config, default)` |
| `_parse` | method | `cli/toast_bus.py:252` | `def _parse(self, text, source, base_offset)` |
| `_role_for` | method | `cli/toast_bus.py:476` | `def _role_for(self, severity)` |
| `_schedule_erase` | method | `cli/toast_bus.py:591` | `def _schedule_erase(self, delay)` |
| `_summary` | method | `cli/toast_bus.py:296` | `def _summary(record)` |
| `_truncate` | method | `cli/toast_bus.py:482` | `def _truncate(self, value)` |
| `build_default_bus` | method | `cli/toast_bus.py:679` | `def build_default_bus(payload, sessions_dir, console)` |
| `build_toast_renderable` | method | `cli/toast_bus.py:867` | `def build_toast_renderable(events, payload, width, config)` |
| `collect` | method | `cli/toast_bus.py:510` | `def collect(self)` |
| `digest_line` | method | `cli/toast_bus.py:409` | `def digest_line(dropped)` |
| `duration_for` | method | `cli/toast_bus.py:391` | `def duration_for(self, event)` |
| `emit_toast` | method | `cli/toast_bus.py:778` | `def emit_toast(message, severity, event_type, sessions_dir, config)` |

Next: [SYMBOLS_p6.md](SYMBOLS_p6.md)
