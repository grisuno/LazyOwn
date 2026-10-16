# Symbols (page 6 of 41)
Previous: [SYMBOLS_p5.md](SYMBOLS_p5.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_read_hostsdiscovery` | method | `cli/surface_graph.py:414` | `def _read_hostsdiscovery(self, local_ips)` |
| `_read_implants` | method | `cli/surface_graph.py:525` | `def _read_implants(self)` |
| `_read_last_implant_row` | method | `cli/surface_graph.py:542` | `def _read_last_implant_row(self, path)` |
| `_read_os_hint` | method | `cli/surface_graph.py:399` | `def _read_os_hint(self)` |
| `_read_scan_csv` | method | `cli/surface_graph.py:442` | `def _read_scan_csv(self, local_ips)` |
| `_read_scan_discovery` | method | `cli/surface_graph.py:436` | `def _read_scan_discovery(self, local_ips)` |
| `_read_scan_nmap` | method | `cli/surface_graph.py:467` | `def _read_scan_nmap(self, local_ips)` |
| `_slug_host` | function | `cli/surface_graph.py:75` | `def _slug_host(ip)` |
| `_slug_port` | function | `cli/surface_graph.py:80` | `def _slug_port(host_id, port, protocol)` |
| `build` | method | `cli/surface_graph.py:202` | `def build(self)` |
| `build_surface_graph` | function | `cli/surface_graph.py:633` | `def build_surface_graph(sessions_dir, payload_path)` |
| `children_of` | method | `cli/surface_graph.py:153` | `def children_of(self, node_id)` |
| `get` | method | `cli/surface_graph.py:165` | `def get(self, node_id)` |
| `iter_descendants` | function | `cli/surface_graph.py:650` | `def iter_descendants(graph, root_id)` |
| `stats` | method | `cli/surface_graph.py:146` | `def stats(self)` |
| `to_dict` | method | `cli/surface_graph.py:102` | `def to_dict(self)` |
| `to_dict` | method | `cli/surface_graph.py:120` | `def to_dict(self)` |
| `to_dict` | method | `cli/surface_graph.py:135` | `def to_dict(self)` |
| `SurfaceExplorer` | class | `cli/surface_tui.py:130` | `class SurfaceExplorer(App)` |
| `TextualNotInstalled` | class | `cli/surface_tui.py:61` | `class TextualNotInstalled(RuntimeError)` |
| `__init__` | method | `cli/surface_tui.py:148` | `def __init__(self, sessions_dir, payload_path)` |
| `_add_children` | method | `cli/surface_tui.py:205` | `def _add_children(self, parent_node, graph, parent_id)` |
| `_attach_children` | function | `cli/surface_tui.py:223` | `def _attach_children(parent, graph, parent_id, seen)` |
| `_build_rich_tree` | function | `cli/surface_tui.py:214` | `def _build_rich_tree(graph)` |
| `_reload_graph` | method | `cli/surface_tui.py:185` | `def _reload_graph(self)` |
| `_render_node_detail` | function | `cli/surface_tui.py:260` | `def _render_node_detail(data)` |
| `_stats_table` | function | `cli/surface_tui.py:241` | `def _stats_table(graph)` |
| `_styled_label` | function | `cli/surface_tui.py:232` | `def _styled_label(node)` |
| `action_collapse_all` | method | `cli/surface_tui.py:172` | `def action_collapse_all(self)` |
| `action_expand_all` | method | `cli/surface_tui.py:168` | `def action_expand_all(self)` |
| `action_refresh` | method | `cli/surface_tui.py:164` | `def action_refresh(self)` |
| `compose` | method | `cli/surface_tui.py:154` | `def compose(self)` |
| `launch_tui` | function | `cli/surface_tui.py:112` | `def launch_tui(sessions_dir, payload_path)` |
| `on_mount` | method | `cli/surface_tui.py:161` | `def on_mount(self)` |
| `on_tree_node_selected` | method | `cli/surface_tui.py:176` | `def on_tree_node_selected(self, event)` |
| `render_json` | function | `cli/surface_tui.py:92` | `def render_json(graph, sessions_dir, payload_path)` |
| `render_static` | function | `cli/surface_tui.py:65` | `def render_static(graph, sessions_dir, payload_path, console)` |
| `Theme` | class | `cli/themes.py:31` | `class Theme` |
| `get_theme` | function | `cli/themes.py:222` | `def get_theme(name)` |
| `theme_from_payload` | function | `cli/themes.py:238` | `def theme_from_payload(payload)` |
| `TimelineColumn` | class | `cli/timeline_browser.py:33` | `class TimelineColumn` |
| `TimelineConfig` | class | `cli/timeline_browser.py:43` | `class TimelineConfig` |
| `TimelineEntry` | class | `cli/timeline_browser.py:65` | `class TimelineEntry` |
| `TimelineReader` | class | `cli/timeline_browser.py:72` | `class TimelineReader` |
| `TimelineState` | class | `cli/timeline_browser.py:122` | `class TimelineState` |
| `_TimelineBrowserApp` | class | `cli/timeline_browser.py:213` | `class _TimelineBrowserApp(App)` |
| `__init__` | method | `cli/timeline_browser.py:75` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/timeline_browser.py:228` | `def __init__(self)` |
| `_build_app` | function | `cli/timeline_browser.py:202` | `def _build_app(state, theme)` |
| `_coerce_row` | method | `cli/timeline_browser.py:103` | `def _coerce_row(self, row)` |
| `_rebuild_rows` | method | `cli/timeline_browser.py:266` | `def _rebuild_rows(self)` |
| `_refresh_detail` | method | `cli/timeline_browser.py:278` | `def _refresh_detail(self, row_index)` |
| `action_close` | method | `cli/timeline_browser.py:263` | `def action_close(self)` |
| `action_refresh` | method | `cli/timeline_browser.py:259` | `def action_refresh(self)` |
| `build_state` | function | `cli/timeline_browser.py:157` | `def build_state(payload, sessions_dir, config)` |
| `column_value` | method | `cli/timeline_browser.py:148` | `def column_value(self, entry, column)` |
| `compose` | method | `cli/timeline_browser.py:234` | `def compose(self)` |
| `entries` | method | `cli/timeline_browser.py:134` | `def entries(self)` |
| `launch_scrubber` | function | `cli/timeline_browser.py:169` | `def launch_scrubber(payload, state, runner)` |
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
| `_render_arsenal_tip` | function | `cli/tips_engine.py:1180` | `def _render_arsenal_tip(ctx, state, config)` |
| `_render_autosuggest_hint` | method | `cli/tips_engine.py:750` | `def _render_autosuggest_hint(self, engine)` |
| `_render_contextual_tip` | method | `cli/tips_engine.py:633` | `def _render_contextual_tip(self, cmd, phase)` |
| `_render_exploration` | function | `cli/tips_engine.py:1124` | `def _render_exploration(ctx, state, config)` |
| `_render_hidden_feature` | function | `cli/tips_engine.py:1160` | `def _render_hidden_feature(ctx, state, config)` |
| `_render_kill_chain_hints` | method | `cli/tips_engine.py:475` | `def _render_kill_chain_hints(self, cmd, phase)` |
| `_render_phase_badge` | function | `cli/tips_engine.py:1142` | `def _render_phase_badge(ctx, state, config)` |
| `_render_streak` | function | `cli/tips_engine.py:1103` | `def _render_streak(ctx, state, config)` |
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
| `build_default_tips_config` | function | `cli/tips_engine.py:1240` | `def build_default_tips_config()` |
| `enabled` | method | `cli/tips_engine.py:221` | `def enabled(self)` |
| `get_state_snapshot` | method | `cli/tips_engine.py:440` | `def get_state_snapshot(self)` |
| `heal_commands_seen` | method | `cli/tips_engine.py:460` | `def heal_commands_seen(self, known)` |
| `render` | method | `cli/tips_engine.py:229` | `def render(self, cmd, phase)` |
| `render_session_start` | method | `cli/tips_engine.py:408` | `def render_session_start(self, phase, os_id)` |
| `reset_session` | method | `cli/tips_engine.py:455` | `def reset_session(self)` |
| `set_enabled` | method | `cli/tips_engine.py:225` | `def set_enabled(self, value)` |
| `ToastBus` | class | `cli/toast_bus.py:511` | `class ToastBus` |
| `ToastConfig` | class | `cli/toast_bus.py:43` | `class ToastConfig` |
| `ToastEvent` | class | `cli/toast_bus.py:110` | `class ToastEvent` |
| `ToastFormatter` | class | `cli/toast_bus.py:330` | `class ToastFormatter` |
| `ToastReader` | class | `cli/toast_bus.py:203` | `class ToastReader` |
| `ToastState` | class | `cli/toast_bus.py:121` | `class ToastState` |
| `__init__` | method | `cli/toast_bus.py:129` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/toast_bus.py:206` | `def __init__(self, config, root)` |
| `__init__` | method | `cli/toast_bus.py:333` | `def __init__(self, config, theme)` |
| `__init__` | method | `cli/toast_bus.py:518` | `def __init__(self, config, state, reader, formatter, console)` |
| `_budget` | function | `cli/toast_bus.py:687` | `def _budget(payload, config)` |
| `_build_event` | method | `cli/toast_bus.py:267` | `def _build_event(self, line, source, offset)` |
| `_coerce_str` | method | `cli/toast_bus.py:290` | `def _coerce_str(value)` |
| `_console_width` | method | `cli/toast_bus.py:492` | `def _console_width(self)` |
| `_ensure_loaded` | method | `cli/toast_bus.py:182` | `def _ensure_loaded(self)` |
| `_erase_lines` | method | `cli/toast_bus.py:630` | `def _erase_lines(stream, rows)` |
| `_is_dumb_stream` | function | `cli/toast_bus.py:659` | `def _is_dumb_stream(stream)` |
| `_is_truthy` | function | `cli/toast_bus.py:645` | `def _is_truthy(value, config, default)` |
| `_parse` | method | `cli/toast_bus.py:252` | `def _parse(self, text, source, base_offset)` |
| `_role_for` | method | `cli/toast_bus.py:499` | `def _role_for(self, severity)` |
| `_schedule_erase` | method | `cli/toast_bus.py:614` | `def _schedule_erase(self, delay)` |
| `_summary` | method | `cli/toast_bus.py:298` | `def _summary(record)` |
| `_truncate` | method | `cli/toast_bus.py:505` | `def _truncate(self, value)` |
| `build_default_bus` | function | `cli/toast_bus.py:702` | `def build_default_bus(payload, sessions_dir, console)` |
| `build_toast_renderable` | function | `cli/toast_bus.py:890` | `def build_toast_renderable(events, payload, width, config)` |
| `collect` | method | `cli/toast_bus.py:533` | `def collect(self)` |
| `digest_line` | method | `cli/toast_bus.py:430` | `def digest_line(dropped)` |
| `duration_for` | method | `cli/toast_bus.py:405` | `def duration_for(self, event)` |
| `emit_toast` | function | `cli/toast_bus.py:801` | `def emit_toast(message, severity, event_type, sessions_dir, config)` |
| `ephemeral_enabled` | function | `cli/toast_bus.py:755` | `def ephemeral_enabled(payload, config)` |
| `flush` | method | `cli/toast_bus.py:164` | `def flush(self)` |
| `format` | method | `cli/toast_bus.py:338` | `def format(self, event)` |
| `format_ephemeral` | method | `cli/toast_bus.py:377` | `def format_ephemeral(self, event)` |
| `format_many` | method | `cli/toast_bus.py:438` | `def format_many(self, events, width)` |
| `format_prominent` | method | `cli/toast_bus.py:360` | `def format_prominent(self, event)` |
| `get` | method | `cli/toast_bus.py:148` | `def get(self, name)` |
| `is_prominent` | method | `cli/toast_bus.py:350` | `def is_prominent(self, event)` |
| `mark_all_seen` | method | `cli/toast_bus.py:574` | `def mark_all_seen(self)` |
| `path` | method | `cli/toast_bus.py:144` | `def path(self)` |
| `read_recent_toasts` | function | `cli/toast_bus.py:846` | `def read_recent_toasts(sessions_dir, limit, config)` |
| `read_unseen` | method | `cli/toast_bus.py:221` | `def read_unseen(self, name, start_offset)` |
| `render` | method | `cli/toast_bus.py:545` | `def render(self, enabled)` |
| `render_ephemeral` | method | `cli/toast_bus.py:581` | `def render_ephemeral(self, enabled, duration)` |
| `render_ephemeral_toasts` | function | `cli/toast_bus.py:771` | `def render_ephemeral_toasts(payload, sessions_dir, console, duration, bus_factory)` |
| `render_toasts` | function | `cli/toast_bus.py:731` | `def render_toasts(payload, sessions_dir, console, bus_factory)` |
| `reset` | method | `cli/toast_bus.py:159` | `def reset(self)` |
| `root` | method | `cli/toast_bus.py:217` | `def root(self)` |
| `set` | method | `cli/toast_bus.py:153` | `def set(self, name, offset)` |
| `toasts_enabled` | function | `cli/toast_bus.py:679` | `def toasts_enabled(payload, config)` |
| `_cycle` | function | `cli/tui_theme.py:65` | `def _cycle(payload, direction)` |
| `_format_listing` | function | `cli/tui_theme.py:45` | `def _format_listing(current)` |
| `_set_theme` | function | `cli/tui_theme.py:30` | `def _set_theme(payload, name)` |
| `run` | function | `cli/tui_theme.py:87` | `def run(args, payload, save)` |
| `TutorialConfig` | class | `cli/tutorial.py:76` | `class TutorialConfig` |
| `is_done` | function | `cli/tutorial.py:83` | `def is_done(config)` |
| `mark_done` | function | `cli/tutorial.py:89` | `def mark_done(config)` |
| `render_header` | function | `cli/tutorial.py:96` | `def render_header()` |
| `render_phase_table` | function | `cli/tutorial.py:113` | `def render_phase_table()` |
| `run` | function | `cli/tutorial.py:185` | `def run(params, command_runner)` |
| `run_step` | function | `cli/tutorial.py:128` | `def run_step(index, command, description, why, params, command_runner)` |
| `BinarySpec` | class | `cli/wizard.py:90` | `class BinarySpec` |
| `BinaryStatus` | class | `cli/wizard.py:141` | `class BinaryStatus` |
| `ReadinessItem` | class | `cli/wizard.py:150` | `class ReadinessItem` |
| `WizardResult` | class | `cli/wizard.py:160` | `class WizardResult` |
| `_ask_device` | function | `cli/wizard.py:537` | `def _ask_device(current)` |
| `_ask_domain` | function | `cli/wizard.py:515` | `def _ask_domain(current)` |
| `_ask_lhost` | function | `cli/wizard.py:484` | `def _ask_lhost(current)` |
| `_ask_llm` | function | `cli/wizard.py:621` | `def _ask_llm(params)` |
| `_ask_marketplace_config` | function | `cli/wizard.py:852` | `def _ask_marketplace_config()` |
| `_ask_operator_login` | function | `cli/wizard.py:724` | `def _ask_operator_login(params)` |
| `_ask_os_id` | function | `cli/wizard.py:563` | `def _ask_os_id(current)` |
| `_ask_rhost` | function | `cli/wizard.py:457` | `def _ask_rhost(current)` |
| `_ask_wordlists` | function | `cli/wizard.py:692` | `def _ask_wordlists(params)` |
| `_build_readiness` | function | `cli/wizard.py:875` | `def _build_readiness(params)` |
| `_check` | function | `cli/wizard.py:878` | `def _check(key, label, hint)` |
| `_check_llm` | function | `cli/wizard.py:887` | `def _check_llm()` |
| `_collect_values` | function | `cli/wizard.py:419` | `def _collect_values(params)` |
| `_detect_device` | function | `cli/wizard.py:1120` | `def _detect_device()` |
| `_detect_lhost` | function | `cli/wizard.py:1098` | `def _detect_lhost()` |
| `_find_seclists_root` | function | `cli/wizard.py:1133` | `def _find_seclists_root()` |
| `_group_by_category` | function | `cli/wizard.py:988` | `def _group_by_category(statuses)` |
| `_info` | function | `cli/wizard.py:1169` | `def _info(msg)` |
| `_is_default` | function | `cli/wizard.py:322` | `def _is_default(value)` |
| `_is_weak` | function | `cli/wizard.py:325` | `def _is_weak(value)` |
| `_mask_secret` | function | `cli/wizard.py:606` | `def _mask_secret(value)` |
| `_normalize_provider_answer` | function | `cli/wizard.py:585` | `def _normalize_provider_answer(raw)` |
| `_ok` | function | `cli/wizard.py:1161` | `def _ok(msg)` |
| `_ping` | function | `cli/wizard.py:1141` | `def _ping(ip)` |
| `_print_binary_report` | function | `cli/wizard.py:997` | `def _print_binary_report(statuses)` |
| `_print_glossary_panel` | function | `cli/wizard.py:379` | `def _print_glossary_panel()` |
| `_print_header` | function | `cli/wizard.py:364` | `def _print_header()` |
| `_print_long_help` | function | `cli/wizard.py:412` | `def _print_long_help(key)` |
| `_print_next_steps` | function | `cli/wizard.py:1035` | `def _print_next_steps(params)` |
| `_print_readiness` | function | `cli/wizard.py:927` | `def _print_readiness(items)` |
| `_print_secret_rotation` | function | `cli/wizard.py:348` | `def _print_secret_rotation(rotated)` |
| `_print_validation_summary` | function | `cli/wizard.py:1059` | `def _print_validation_summary(params)` |
| `_prompt` | function | `cli/wizard.py:1154` | `def _prompt(message)` |
| `_rotate_default_secrets` | function | `cli/wizard.py:300` | `def _rotate_default_secrets(params, save)` |
| `_spec_long_help` | function | `cli/wizard.py:404` | `def _spec_long_help(key)` |
| `_warn` | function | `cli/wizard.py:1165` | `def _warn(msg)` |
| `_wizard_login_flow` | function | `cli/wizard.py:786` | `def _wizard_login_flow()` |
| `_wizard_register_flow` | function | `cli/wizard.py:809` | `def _wizard_register_flow()` |
| `check_binaries` | function | `cli/wizard.py:947` | `def check_binaries(specs, which)` |
| `run` | function | `cli/wizard.py:169` | `def run(params, save)` |
| `run_non_interactive` | function | `cli/wizard.py:234` | `def run_non_interactive(params, save, values)` |
| `WizardScope` | class | `cli/wizard_scope.py:31` | `class WizardScope` |
| `WizardScopeConfig` | class | `cli/wizard_scope.py:17` | `class WizardScopeConfig` |
| `parse_scope` | function | `cli/wizard_scope.py:38` | `def parse_scope(tokens, config)` |
| `status_rows` | function | `cli/wizard_scope.py:64` | `def status_rows(params)` |
| `exploit` | function | `contrib/legacy/lazy_http_bof.py:29` | `def exploit(target, port, payload)` |
| `genHeader` | function | `contrib/legacy/lazy_http_bof.py:6` | `def genHeader(raw)` |
| `check_sudo` | function | `contrib/legacy/lazy_packet_image_sniffer.py:23` | `def check_sudo()` |
| `choose_interface` | function | `contrib/legacy/lazy_packet_image_sniffer.py:49` | `def choose_interface(interfaces)` |
| `daemonize` | function | `contrib/legacy/lazy_packet_image_sniffer.py:192` | `def daemonize()` |
| `get_ip_addresses` | function | `contrib/legacy/lazy_packet_image_sniffer.py:65` | `def get_ip_addresses(interface)` |
| `get_subnet_from_interface` | function | `contrib/legacy/lazy_packet_image_sniffer.py:61` | `def get_subnet_from_interface(interface)` |
| `handle_packet` | function | `contrib/legacy/lazy_packet_image_sniffer.py:111` | `def handle_packet(packet)` |
| `list_interfaces` | function | `contrib/legacy/lazy_packet_image_sniffer.py:31` | `def list_interfaces()` |
| `run` | function | `contrib/legacy/lazy_packet_image_sniffer.py:187` | `def run()` |
| `save_image` | function | `contrib/legacy/lazy_packet_image_sniffer.py:161` | `def save_image(src_ip, end_idx)` |
| `build_llm_prompt` | function | `contrib/legacy/lazyaddon_creator.py:98` | `def build_llm_prompt(meta, readme, root_files)` |
| `build_yaml` | function | `contrib/legacy/lazyaddon_creator.py:300` | `def build_yaml(data, repo_url)` |
| `extract_json_from_response` | function | `contrib/legacy/lazyaddon_creator.py:164` | `def extract_json_from_response(text)` |
| `fallback_yaml_data` | function | `contrib/legacy/lazyaddon_creator.py:276` | `def fallback_yaml_data(meta, readme, root_files)` |
| `fetch_readme` | function | `contrib/legacy/lazyaddon_creator.py:73` | `def fetch_readme(owner, repo)` |
| `fetch_repo_metadata` | function | `contrib/legacy/lazyaddon_creator.py:68` | `def fetch_repo_metadata(owner, repo)` |
| `fetch_root_files` | function | `contrib/legacy/lazyaddon_creator.py:85` | `def fetch_root_files(owner, repo)` |
| `github_api_get` | function | `contrib/legacy/lazyaddon_creator.py:58` | `def github_api_get(owner, repo, endpoint)` |
| `heuristic_execute_command` | function | `contrib/legacy/lazyaddon_creator.py:211` | `def heuristic_execute_command(name, root_files, language)` |
| `heuristic_install_command` | function | `contrib/legacy/lazyaddon_creator.py:192` | `def heuristic_install_command(root_files, language)` |
| `heuristic_params` | function | `contrib/legacy/lazyaddon_creator.py:245` | `def heuristic_params(name, readme, root_files)` |
| `main` | function | `contrib/legacy/lazyaddon_creator.py:357` | `def main()` |
| `parse_github_url` | function | `contrib/legacy/lazyaddon_creator.py:49` | `def parse_github_url(url)` |
| `save_yaml` | function | `contrib/legacy/lazyaddon_creator.py:336` | `def save_yaml(addon, output_dir)` |
| `check_sudo` | function | `contrib/legacy/lazyarpspoofing.py:27` | `def check_sudo()` |
| `disable_ip_forward` | function | `contrib/legacy/lazyarpspoofing.py:38` | `def disable_ip_forward()` |
| `enable_ip_forward` | function | `contrib/legacy/lazyarpspoofing.py:35` | `def enable_ip_forward()` |
| `get_local_ip` | function | `contrib/legacy/lazyarpspoofing.py:41` | `def get_local_ip(ifname)` |
| `get_mac` | function | `contrib/legacy/lazyarpspoofing.py:49` | `def get_mac(ip, device, retries, timeout)` |
| `main` | function | `contrib/legacy/lazyarpspoofing.py:80` | `def main()` |
| `spoofer` | function | `contrib/legacy/lazyarpspoofing.py:69` | `def spoofer(target, spoofed, device)` |
| `generate_key_iv` | function | `contrib/legacy/lazybinenc.py:12` | `def generate_key_iv(sessions_path)` |
| `main` | function | `contrib/legacy/lazybinenc.py:54` | `def main()` |
| `decrypt` | function | `contrib/legacy/lazybotcli.py:36` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `contrib/legacy/lazybotcli.py:30` | `def encrypt(plaintext, key)` |
| `main` | function | `contrib/legacy/lazybotcli.py:42` | `def main()` |
| `Keylogger` | class | `contrib/legacy/lazybotnet.py:89` | `class Keylogger` |
| `__init__` | method | `contrib/legacy/lazybotnet.py:90` | `def __init__(self, key, log_file)` |
| `add_to_botnet` | function | `contrib/legacy/lazybotnet.py:58` | `def add_to_botnet(ip, port, botnet_file)` |
| `clean_botnet` | function | `contrib/legacy/lazybotnet.py:62` | `def clean_botnet(ip, port, botnet_file)` |
| `create_shortcut` | method | `contrib/legacy/lazybotnet.py:136` | `def create_shortcut(self, script_path, shortcut_path)` |
| `decrypt` | function | `contrib/legacy/lazybotnet.py:52` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `contrib/legacy/lazybotnet.py:46` | `def encrypt(plaintext, key)` |
| `get_log` | method | `contrib/legacy/lazybotnet.py:110` | `def get_log(self)` |
| `handle_client` | function | `contrib/legacy/lazybotnet.py:144` | `def handle_client(conn, key, botnet_file, log_file)` |
| `on_press` | method | `contrib/legacy/lazybotnet.py:95` | `def on_press(self, key)` |
| `run` | method | `contrib/legacy/lazybotnet.py:120` | `def run(self)` |
| `save_log` | method | `contrib/legacy/lazybotnet.py:113` | `def save_log(self)` |
| `send_to_botnet` | function | `contrib/legacy/lazybotnet.py:71` | `def send_to_botnet(cmd, key, botnet_file)` |
| `setup_persistence` | method | `contrib/legacy/lazybotnet.py:125` | `def setup_persistence(self)` |
| `start` | method | `contrib/legacy/lazybotnet.py:106` | `def start(self)` |
| `start_server` | function | `contrib/legacy/lazybotnet.py:182` | `def start_server(host, port, key, botnet_file, log_file)` |
| `RTSPScanner` | class | `contrib/legacy/lazycam.py:32` | `class RTSPScanner` |
| `__init__` | method | `contrib/legacy/lazycam.py:33` | `def __init__(self, verbose, wspace)` |
| `addCameras` | method | `contrib/legacy/lazycam.py:149` | `def addCameras(self)` |
| `cla` | function | `contrib/legacy/lazycam.py:212` | `def cla()` |
| `delCameras` | method | `contrib/legacy/lazycam.py:136` | `def delCameras(self)` |
| `main` | function | `contrib/legacy/lazycam.py:257` | `def main()` |
| `resizeImg` | method | `contrib/legacy/lazycam.py:68` | `def resizeImg(self, img, output, height, ratio, fmt)` |
| `run` | method | `contrib/legacy/lazycam.py:49` | `def run(self)` |
| `scanner` | method | `contrib/legacy/lazycam.py:83` | `def scanner(self)` |
| `splitCSV` | method | `contrib/legacy/lazycam.py:77` | `def splitCSV(self, csv)` |
| `_load_payload_kv` | function | `contrib/legacy/lazydeepseekcli.py:50` | `def _load_payload_kv()` |
| `_load_report_context` | function | `contrib/legacy/lazydeepseekcli.py:68` | `def _load_report_context()` |
| `_ollama_stream` | function | `contrib/legacy/lazydeepseekcli.py:223` | `def _ollama_stream(prompt_text, mode, timeout)` |
| `_prompt_redteam` | function | `contrib/legacy/lazydeepseekcli.py:79` | `def _prompt_redteam(base_prompt, history, knowledge_base)` |
| `_prompt_report` | function | `contrib/legacy/lazydeepseekcli.py:118` | `def _prompt_report(base_prompt, history, knowledge_base)` |
| `add_to_knowledge_base` | function | `contrib/legacy/lazydeepseekcli.py:179` | `def add_to_knowledge_base(prompt, command, file_path)` |
| `configure_logging` | function | `contrib/legacy/lazydeepseekcli.py:45` | `def configure_logging(debug)` |
| `generate` | function | `contrib/legacy/lazydeepseekcli.py:232` | `def generate()` |
| `get_relevant_knowledge` | function | `contrib/legacy/lazydeepseekcli.py:185` | `def get_relevant_knowledge(prompt)` |
| `load_knowledge_base` | function | `contrib/legacy/lazydeepseekcli.py:167` | `def load_knowledge_base(file_path)` |
| `parse_args` | function | `contrib/legacy/lazydeepseekcli.py:277` | `def parse_args()` |
| `process_prompt_local` | function | `contrib/legacy/lazydeepseekcli.py:261` | `def process_prompt_local(prompt, debug, mode)` |
| `process_prompt_localreport` | function | `contrib/legacy/lazydeepseekcli.py:269` | `def process_prompt_localreport(prompt, debug, mode)` |
| `save_knowledge_base` | function | `contrib/legacy/lazydeepseekcli.py:174` | `def save_knowledge_base(knowledge_base, file_path)` |
| `transform_knowledge_base` | function | `contrib/legacy/lazydeepseekcli.py:193` | `def transform_knowledge_base(prompt_builder)` |
| `truncate_message` | function | `contrib/legacy/lazydeepseekcli.py:41` | `def truncate_message(message, max_chars)` |
| `X64Disassembler` | class | `contrib/legacy/lazydisassebler.py:24` | `class X64Disassembler` |
| `__init__` | method | `contrib/legacy/lazydisassebler.py:34` | `def __init__(self)` |
| `disassemble` | method | `contrib/legacy/lazydisassebler.py:305` | `def disassemble(self, bytes_data, file_offset, vaddr, size, entry_point)` |
| `get_operand_str` | method | `contrib/legacy/lazydisassebler.py:212` | `def get_operand_str(self, mod, rm, rex, bytes_data, offset)` |
| `main` | function | `contrib/legacy/lazydisassebler.py:489` | `def main()` |
| `parse_modrm` | method | `contrib/legacy/lazydisassebler.py:135` | `def parse_modrm(self, modrm, rex)` |
| `parse_sib` | method | `contrib/legacy/lazydisassebler.py:173` | `def parse_sib(self, sib, rex)` |
| `read_elf_header` | method | `contrib/legacy/lazydisassebler.py:79` | `def read_elf_header(self, data)` |
| `check_sudo` | function | `contrib/legacy/lazyftpsniff.py:21` | `def check_sudo()` |
| `main` | function | `contrib/legacy/lazyftpsniff.py:69` | `def main()` |
| `parse_arguments` | function | `contrib/legacy/lazyftpsniff.py:42` | `def parse_arguments()` |
| `signal_handler` | function | `contrib/legacy/lazyftpsniff.py:34` | `def signal_handler(sig, frame)` |
| `sniffer_ftp` | function | `contrib/legacy/lazyftpsniff.py:56` | `def sniffer_ftp(pkt)` |
| `SamsungKnoxExploitServer` | class | `contrib/legacy/lazygalazy.py:8` | `class SamsungKnoxExploitServer(BaseHTTPRequestHandler)` |
| `apk_bytes` | method | `contrib/legacy/lazygalazy.py:33` | `def apk_bytes(self)` |
| `do_GET` | method | `contrib/legacy/lazygalazy.py:11` | `def do_GET(self)` |
| `exploit_js` | method | `contrib/legacy/lazygalazy.py:49` | `def exploit_js(self)` |
| `launch_html` | method | `contrib/legacy/lazygalazy.py:36` | `def launch_html(self)` |
| `main` | function | `contrib/legacy/lazygalazy.py:97` | `def main()` |
| `rand_word` | method | `contrib/legacy/lazygalazy.py:93` | `def rand_word(self)` |
| `add_to_knowledge_base` | function | `contrib/legacy/lazygptcli.py:128` | `def add_to_knowledge_base(prompt, command, file_path)` |
| `check_api_key` | function | `contrib/legacy/lazygptcli.py:77` | `def check_api_key()` |
| `cleanup_temp_files` | function | `contrib/legacy/lazygptcli.py:164` | `def cleanup_temp_files()` |
| `configure_logging` | function | `contrib/legacy/lazygptcli.py:83` | `def configure_logging(debug)` |
| `create_complex_prompt` | function | `contrib/legacy/lazygptcli.py:94` | `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)` |
| `execute_command` | function | `contrib/legacy/lazygptcli.py:108` | `def execute_command(command)` |
| `get_relevant_knowledge` | function | `contrib/legacy/lazygptcli.py:133` | `def get_relevant_knowledge(prompt)` |
| `load_knowledge_base` | function | `contrib/legacy/lazygptcli.py:118` | `def load_knowledge_base(file_path)` |
| `main` | function | `contrib/legacy/lazygptcli.py:177` | `def main()` |
| `parse_args` | function | `contrib/legacy/lazygptcli.py:87` | `def parse_args()` |
| `save_knowledge_base` | function | `contrib/legacy/lazygptcli.py:124` | `def save_knowledge_base(knowledge_base, file_path)` |
| `show_help` | function | `contrib/legacy/lazygptcli.py:73` | `def show_help(message)` |
| `signal_handler` | function | `contrib/legacy/lazygptcli.py:66` | `def signal_handler(sig, frame)` |
| `transform_knowledge_base` | function | `contrib/legacy/lazygptcli.py:141` | `def transform_knowledge_base(client)` |
| `_add_to_knowledge_base` | function | `contrib/legacy/lazygptcli_unified.py:76` | `def _add_to_knowledge_base(prompt, response, file_path)` |
| `_configure_logging` | function | `contrib/legacy/lazygptcli_unified.py:57` | `def _configure_logging(debug)` |
| `_deepseek_fallback` | function | `contrib/legacy/lazygptcli_unified.py:392` | `def _deepseek_fallback(prompt)` |
| `_get_relevant_knowledge` | function | `contrib/legacy/lazygptcli_unified.py:82` | `def _get_relevant_knowledge(prompt, file_path)` |
| `_groq_chat` | function | `contrib/legacy/lazygptcli_unified.py:115` | `def _groq_chat(client, messages, model, max_tokens)` |
| `_load_event_config` | function | `contrib/legacy/lazygptcli_unified.py:147` | `def _load_event_config()` |
| `_load_knowledge_base` | function | `contrib/legacy/lazygptcli_unified.py:62` | `def _load_knowledge_base(file_path)` |
| `_load_payload_kv` | function | `contrib/legacy/lazygptcli_unified.py:129` | `def _load_payload_kv()` |
| `_process_groq` | function | `contrib/legacy/lazygptcli_unified.py:287` | `def _process_groq(client, prompt, debug, prompt_template, kb_file, model)` |
| `_prompt_adversary` | function | `contrib/legacy/lazygptcli_unified.py:190` | `def _prompt_adversary(base_prompt, history, knowledge_base)` |
| `_prompt_general` | function | `contrib/legacy/lazygptcli_unified.py:206` | `def _prompt_general(base_prompt, history, knowledge_base)` |
| `_prompt_oneliner` | function | `contrib/legacy/lazygptcli_unified.py:159` | `def _prompt_oneliner(base_prompt, history, knowledge_base)` |
| `_prompt_redop` | function | `contrib/legacy/lazygptcli_unified.py:267` | `def _prompt_redop(base_prompt, history, knowledge_base)` |
| `_prompt_script` | function | `contrib/legacy/lazygptcli_unified.py:175` | `def _prompt_script(base_prompt, history, knowledge_base)` |
| `_prompt_search` | function | `contrib/legacy/lazygptcli_unified.py:225` | `def _prompt_search(base_prompt, history, knowledge_base)` |
| `_prompt_task` | function | `contrib/legacy/lazygptcli_unified.py:254` | `def _prompt_task(base_prompt, history, knowledge_base)` |
| `_prompt_vuln` | function | `contrib/legacy/lazygptcli_unified.py:239` | `def _prompt_vuln(base_prompt, history, knowledge_base)` |
| `_ret_model` | function | `contrib/legacy/lazygptcli_unified.py:45` | `def _ret_model()` |
| `_save_knowledge_base` | function | `contrib/legacy/lazygptcli_unified.py:70` | `def _save_knowledge_base(knowledge_base, file_path)` |
| `_transform_knowledge_base` | function | `contrib/legacy/lazygptcli_unified.py:95` | `def _transform_knowledge_base(client, kb_file, improved_file)` |
| `process_prompt` | function | `contrib/legacy/lazygptcli_unified.py:318` | `def process_prompt(client, prompt, debug)` |
| `process_prompt_adversary` | function | `contrib/legacy/lazygptcli_unified.py:328` | `def process_prompt_adversary(client, prompt, debug)` |
| `process_prompt_general` | function | `contrib/legacy/lazygptcli_unified.py:333` | `def process_prompt_general(client, prompt, debug)` |
| `process_prompt_redop` | function | `contrib/legacy/lazygptcli_unified.py:382` | `def process_prompt_redop(client, prompt, debug)` |
| `process_prompt_script` | function | `contrib/legacy/lazygptcli_unified.py:323` | `def process_prompt_script(client, prompt, debug)` |
| `process_prompt_search` | function | `contrib/legacy/lazygptcli_unified.py:341` | `def process_prompt_search(client, prompt, debug)` |
| `process_prompt_task` | function | `contrib/legacy/lazygptcli_unified.py:346` | `def process_prompt_task(client, prompt, debug)` |
| `process_prompt_vuln` | function | `contrib/legacy/lazygptcli_unified.py:356` | `def process_prompt_vuln(client, prompt, debug, event)` |
| `truncate_message` | function | `contrib/legacy/lazygptcli_unified.py:53` | `def truncate_message(message, max_chars)` |
| `Server` | class | `contrib/legacy/lazyhoneypot.py:60` | `class Server(ServerInterface)` |
| `__init__` | method | `contrib/legacy/lazyhoneypot.py:61` | `def __init__(self)` |
| `alert_admin` | function | `contrib/legacy/lazyhoneypot.py:147` | `def alert_admin(message)` |
| `analyze_traffic` | function | `contrib/legacy/lazyhoneypot.py:136` | `def analyze_traffic()` |
| `check_auth_password` | method | `contrib/legacy/lazyhoneypot.py:69` | `def check_auth_password(self, username, password)` |
| `check_channel_request` | method | `contrib/legacy/lazyhoneypot.py:64` | `def check_channel_request(self, kind, chanid)` |
| `generate_rsa_key` | function | `contrib/legacy/lazyhoneypot.py:56` | `def generate_rsa_key(key_filename)` |
| `handle_connection` | function | `contrib/legacy/lazyhoneypot.py:74` | `def handle_connection(client_socket, host_key, commands_log, downloads_log, downloads_dir)` |
| `handle_file_download` | function | `contrib/legacy/lazyhoneypot.py:110` | `def handle_file_download(command, downloads_dir, downloads_log)` |
| `log_command` | function | `contrib/legacy/lazyhoneypot.py:128` | `def log_command(command, commands_log)` |
| `log_downloaded_file` | function | `contrib/legacy/lazyhoneypot.py:132` | `def log_downloaded_file(filename, url, downloads_log)` |
| `main` | function | `contrib/legacy/lazyhoneypot.py:165` | `def main()` |
| `parse_args` | function | `contrib/legacy/lazyhoneypot.py:34` | `def parse_args()` |
| `process_packet` | function | `contrib/legacy/lazyhoneypot.py:137` | `def process_packet(packet)` |
| `setup_logging` | function | `contrib/legacy/lazyhoneypot.py:52` | `def setup_logging(log_file)` |
| `RequestHandler` | class | `contrib/legacy/lazyhttpreverseshell.py:51` | `class RequestHandler(BaseHTTPRequestHandler)` |
| `compress` | function | `contrib/legacy/lazyhttpreverseshell.py:20` | `def compress(data)` |
| `decompress` | function | `contrib/legacy/lazyhttpreverseshell.py:23` | `def decompress(data)` |
| `decrypt` | function | `contrib/legacy/lazyhttpreverseshell.py:17` | `def decrypt(data)` |
| `do_GET` | method | `contrib/legacy/lazyhttpreverseshell.py:52` | `def do_GET(self)` |
| `do_POST` | method | `contrib/legacy/lazyhttpreverseshell.py:65` | `def do_POST(self)` |
| `encrypt` | function | `contrib/legacy/lazyhttpreverseshell.py:14` | `def encrypt(data)` |
| `parse_arguments` | function | `contrib/legacy/lazyhttpreverseshell.py:88` | `def parse_arguments(args)` |
| `reverse_http_shell_client` | function | `contrib/legacy/lazyhttpreverseshell.py:26` | `def reverse_http_shell_client(lhost, rhost, rport)` |
| `reverse_http_shell_server` | function | `contrib/legacy/lazyhttpreverseshell.py:50` | `def reverse_http_shell_server(lhost, lport)` |
| `decrypt` | function | `contrib/legacy/lazykeygen.py:17` | `def decrypt(ciphertext, key)` |
| `encrypt` | function | `contrib/legacy/lazykeygen.py:11` | `def encrypt(plaintext, key)` |
| `generate_key` | function | `contrib/legacy/lazykeygen.py:23` | `def generate_key(length)` |
| `main` | function | `contrib/legacy/lazykeygen.py:26` | `def main()` |
| `pad` | function | `contrib/legacy/lazykeygen.py:8` | `def pad(s)` |
| `check_lfi_success` | function | `contrib/legacy/lazylfi2rce.py:35` | `def check_lfi_success(response_text)` |
| `check_rfi_success` | function | `contrib/legacy/lazylfi2rce.py:39` | `def check_rfi_success(response_text)` |
| `main` | function | `contrib/legacy/lazylfi2rce.py:43` | `def main()` |
| `signal_handler` | function | `contrib/legacy/lazylfi2rce.py:29` | `def signal_handler(sig, frame)` |
| `LLMEngine` | class | `contrib/legacy/lazyllmchat.py:163` | `class LLMEngine` |
| `LazyOwnLLMChat` | class | `contrib/legacy/lazyllmchat.py:234` | `class LazyOwnLLMChat` |
| `LazyOwnPromptRenderer` | class | `contrib/legacy/lazyllmchat.py:198` | `class LazyOwnPromptRenderer` |
| `LazyOwnShellBridge` | class | `contrib/legacy/lazyllmchat.py:22` | `class LazyOwnShellBridge` |
| `PromptBuilder` | class | `contrib/legacy/lazyllmchat.py:123` | `class PromptBuilder` |
| `SessionContextProvider` | class | `contrib/legacy/lazyllmchat.py:104` | `class SessionContextProvider` |
| `__init__` | method | `contrib/legacy/lazyllmchat.py:25` | `def __init__(self, script_path)` |
| `__init__` | method | `contrib/legacy/lazyllmchat.py:105` | `def __init__(self, session_path)` |
| `__init__` | method | `contrib/legacy/lazyllmchat.py:164` | `def __init__(self)` |
| `__init__` | method | `contrib/legacy/lazyllmchat.py:235` | `def __init__(self)` |
| `_analyze` | method | `contrib/legacy/lazyllmchat.py:263` | `def _analyze(self, command, output)` |
| `_direct_query` | method | `contrib/legacy/lazyllmchat.py:273` | `def _direct_query(self, query)` |
| `_get_context` | method | `contrib/legacy/lazyllmchat.py:242` | `def _get_context(self)` |
| `_load_model` | method | `contrib/legacy/lazyllmchat.py:170` | `def _load_model(self)` |
| `_load_shell` | method | `contrib/legacy/lazyllmchat.py:31` | `def _load_shell(self)` |
| `_run_shell_command` | method | `contrib/legacy/lazyllmchat.py:245` | `def _run_shell_command(self, command)` |
| `_run_system_command` | method | `contrib/legacy/lazyllmchat.py:251` | `def _run_system_command(self, command)` |
| `ask` | method | `contrib/legacy/lazyllmchat.py:182` | `def ask(self, prompt)` |
| `banner` | method | `contrib/legacy/lazyllmchat.py:223` | `def banner(self)` |
| `execute` | method | `contrib/legacy/lazyllmchat.py:65` | `def execute(self, command)` |
| `for_command_analysis` | method | `contrib/legacy/lazyllmchat.py:133` | `def for_command_analysis(command, output, context, history)` |
| `for_direct_query` | method | `contrib/legacy/lazyllmchat.py:149` | `def for_direct_query(query, context, history)` |
| `get_history_text` | method | `contrib/legacy/lazyllmchat.py:194` | `def get_history_text(self)` |
| `get_last_lines` | method | `contrib/legacy/lazyllmchat.py:108` | `def get_last_lines(self, count)` |
| `is_ready` | method | `contrib/legacy/lazyllmchat.py:179` | `def is_ready(self)` |
| `main` | function | `contrib/legacy/lazyllmchat.py:309` | `def main()` |
| `no_history_init` | function | `contrib/legacy/lazyllmchat.py:38` | `def no_history_init(self_)` |
| `render` | method | `contrib/legacy/lazyllmchat.py:208` | `def render(self)` |
| `run` | method | `contrib/legacy/lazyllmchat.py:280` | `def run(self, initial_query)` |
| `target` | function | `contrib/legacy/lazyllmchat.py:70` | `def target()` |
| `ensure_http_prefix` | function | `contrib/legacy/lazylogpoisoning.py:39` | `def ensure_http_prefix(url)` |
| `main` | function | `contrib/legacy/lazylogpoisoning.py:53` | `def main()` |
| `signal_handler` | function | `contrib/legacy/lazylogpoisoning.py:45` | `def signal_handler(sig, frame)` |
| `errmsg` | function | `contrib/legacy/lazymariadb_rce_cve_2016-662.py:63` | `def errmsg(str)` |
| `info` | function | `contrib/legacy/lazymariadb_rce_cve_2016-662.py:59` | `def info(str)` |
| `shutdown` | function | `contrib/legacy/lazymariadb_rce_cve_2016-662.py:67` | `def shutdown(code)` |
| `get_mac` | function | `contrib/legacy/lazymidm.py:12` | `def get_mac(ip)` |
| `main` | function | `contrib/legacy/lazymidm.py:68` | `def main()` |
| `mitm` | function | `contrib/legacy/lazymidm.py:37` | `def mitm(target_ip, gateway_ip)` |
| `restore` | function | `contrib/legacy/lazymidm.py:27` | `def restore(target_ip, spoof_ip)` |
| `setup_monitor_mode` | function | `contrib/legacy/lazymidm.py:58` | `def setup_monitor_mode(interface)` |
| `spoof` | function | `contrib/legacy/lazymidm.py:18` | `def spoof(target_ip, spoof_ip)` |
| `start_sslstrip` | function | `contrib/legacy/lazymidm.py:50` | `def start_sslstrip(port)` |
| `start_tcpdump` | function | `contrib/legacy/lazymidm.py:54` | `def start_tcpdump(interface, output_file)` |
| `_sudo_run` | function | `contrib/legacy/lazymitmap.py:14` | `def _sudo_run()` |
| `_validate_iface` | function | `contrib/legacy/lazymitmap.py:19` | `def _validate_iface(value, name)` |
| `append_file` | function | `contrib/legacy/lazymitmap.py:67` | `def append_file(path, s)` |
| `backup_file` | function | `contrib/legacy/lazymitmap.py:121` | `def backup_file(filepath)` |
| `cleanup` | function | `contrib/legacy/lazymitmap.py:315` | `def cleanup()` |
| `configure_dnsmasq` | function | `contrib/legacy/lazymitmap.py:163` | `def configure_dnsmasq(ap_iface, ap_ip_range_start, ap_ip_range_end, ap_ip_gateway, dns_ip_1, dns_ip_2, sslstrip)` |
| `configure_hostapd` | function | `contrib/legacy/lazymitmap.py:195` | `def configure_hostapd(ap_iface, ssid, channel, wpa_passphrase)` |
| `create_dir` | function | `contrib/legacy/lazymitmap.py:72` | `def create_dir(directory)` |
| `flush_iptables` | function | `contrib/legacy/lazymitmap.py:145` | `def flush_iptables()` |
| `install_dependencies` | function | `contrib/legacy/lazymitmap.py:84` | `def install_dependencies()` |
| `print_header` | function | `contrib/legacy/lazymitmap.py:45` | `def print_header()` |
| `restart_service` | function | `contrib/legacy/lazymitmap.py:138` | `def restart_service(service)` |
| `restore_file` | function | `contrib/legacy/lazymitmap.py:128` | `def restore_file(filepath)` |
| `run_cmd_write` | function | `contrib/legacy/lazymitmap.py:49` | `def run_cmd_write(cmd_args, s)` |
| `set_permissions` | function | `contrib/legacy/lazymitmap.py:77` | `def set_permissions(directory, permissions)` |
| `set_speed_limit` | function | `contrib/legacy/lazymitmap.py:248` | `def set_speed_limit(ap_iface, speed_up, speed_down)` |
| `setup_iptables` | function | `contrib/legacy/lazymitmap.py:228` | `def setup_iptables(ap_iface, ap_ip, net_iface)` |
| `setup_network_manager` | function | `contrib/legacy/lazymitmap.py:153` | `def setup_network_manager(ap_iface)` |
| `signal_handler` | function | `contrib/legacy/lazymitmap.py:324` | `def signal_handler(sig, frame)` |
| `start_services` | function | `contrib/legacy/lazymitmap.py:254` | `def start_services(ap_iface, script_path, sslstrip, wireshark, driftnet, tshark)` |
| `write_file` | function | `contrib/legacy/lazymitmap.py:63` | `def write_file(path, s)` |
| `check_arp` | function | `contrib/legacy/lazynetbios.py:58` | `def check_arp(ip)` |
| `check_netbios` | function | `contrib/legacy/lazynetbios.py:71` | `def check_netbios(ip)` |
| `check_sudo` | function | `contrib/legacy/lazynetbios.py:30` | `def check_sudo()` |
| `generate_ip_range` | function | `contrib/legacy/lazynetbios.py:115` | `def generate_ip_range(start_ip, end_ip)` |
| `scan_netbios` | function | `contrib/legacy/lazynetbios.py:45` | `def scan_netbios(ip_range)` |
| `send_nbns_spoof` | function | `contrib/legacy/lazynetbios.py:90` | `def send_nbns_spoof(target_ip, target_name, spoof_ip, trans_id)` |
| `signal_handler` | function | `contrib/legacy/lazynetbios.py:38` | `def signal_handler(sig, frame)` |
| `ntlm_relay` | function | `contrib/legacy/lazyntlrelayx.py:52` | `def ntlm_relay(target_ip, credentials)` |
| `parse_hash_file` | function | `contrib/legacy/lazyntlrelayx.py:5` | `def parse_hash_file(file_path)` |
| `InvalidUsername` | class | `contrib/legacy/lazyopenssh77enum2.py:14` | `class InvalidUsername(Exception)` |
| `add_boolean` | function | `contrib/legacy/lazyopenssh77enum2.py:19` | `def add_boolean()` |
| `check_user` | function | `contrib/legacy/lazyopenssh77enum2.py:50` | `def check_user(username)` |
| `invalid_username` | function | `contrib/legacy/lazyopenssh77enum2.py:36` | `def invalid_username()` |
| `service_accept` | function | `contrib/legacy/lazyopenssh77enum2.py:30` | `def service_accept()` |
| `add_to_knowledge_base` | function | `contrib/legacy/lazyphishingai.py:117` | `def add_to_knowledge_base(prompt, command, file_path)` |
| `clean_think` | function | `contrib/legacy/lazyphishingai.py:28` | `def clean_think(texto)` |
| `clean_yaml` | function | `contrib/legacy/lazyphishingai.py:31` | `def clean_yaml(texto)` |
| `configure_logging` | function | `contrib/legacy/lazyphishingai.py:42` | `def configure_logging(debug)` |
| `create_complex_prompt` | function | `contrib/legacy/lazyphishingai.py:46` | `def create_complex_prompt(base_prompt, history, knowledge_base)` |

Next: [SYMBOLS_p7.md](SYMBOLS_p7.md)
