# Symbols (page 5 of 53)
Previous: [SYMBOLS_p4.md](SYMBOLS_p4.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_score` | method | `cli/graph_advisor.py:335` | `def _score(self, value, terms, query)` |
| `_seed_nodes` | method | `cli/graph_advisor.py:624` | `def _seed_nodes(self, recent_commands)` |
| `_tokens` | method | `cli/graph_advisor.py:350` | `def _tokens(self, query)` |
| `clear_cache` | method | `cli/graph_advisor.py:207` | `def clear_cache(cls)` |
| `community_members` | method | `cli/graph_advisor.py:289` | `def community_members(self, community_id)` |
| `degree` | method | `cli/graph_advisor.py:292` | `def degree(self, node_id)` |
| `degree_ranked` | method | `cli/graph_advisor.py:295` | `def degree_ranked(self)` |
| `did_you_mean` | method | `cli/graph_advisor.py:591` | `def did_you_mean(self, query, limit)` |
| `edges_between` | method | `cli/graph_advisor.py:286` | `def edges_between(self, source, target)` |
| `format_god_nodes` | function | `cli/graph_advisor.py:724` | `def format_god_nodes(results)` |
| `format_neighbors` | function | `cli/graph_advisor.py:706` | `def format_neighbors(result)` |
| `format_search_table` | function | `cli/graph_advisor.py:691` | `def format_search_table(results)` |
| `format_suggestions` | function | `cli/graph_advisor.py:734` | `def format_suggestions(results)` |
| `from_path` | method | `cli/graph_advisor.py:375` | `def from_path(cls, path, config)` |
| `get` | method | `cli/graph_advisor.py:280` | `def get(self, node_id)` |
| `god_nodes` | method | `cli/graph_advisor.py:505` | `def god_nodes(self, limit)` |
| `is_available` | method | `cli/graph_advisor.py:384` | `def is_available(self)` |
| `load` | method | `cli/graph_advisor.py:184` | `def load(self, override)` |
| `neighbors` | method | `cli/graph_advisor.py:283` | `def neighbors(self, node_id)` |
| `neighbors` | method | `cli/graph_advisor.py:456` | `def neighbors(self, node_query, depth, limit)` |
| `nodes` | method | `cli/graph_advisor.py:277` | `def nodes(self)` |
| `rank` | method | `cli/graph_advisor.py:307` | `def rank(self, nodes, query)` |
| `read_recent_commands` | method | `cli/graph_advisor.py:566` | `def read_recent_commands(self, window)` |
| `reload` | method | `cli/graph_advisor.py:387` | `def reload(self, path)` |
| `resolve_path` | method | `cli/graph_advisor.py:160` | `def resolve_path(self, override)` |
| `search` | method | `cli/graph_advisor.py:445` | `def search(self, query, limit)` |
| `suggest_next` | method | `cli/graph_advisor.py:520` | `def suggest_next(self, recent_commands, limit)` |
| `summary` | method | `cli/graph_advisor.py:396` | `def summary(self)` |
| `to_summary` | method | `cli/graph_advisor.py:109` | `def to_summary(self)` |
| `to_summary` | method | `cli/graph_advisor.py:132` | `def to_summary(self)` |
| `truncate_to_budget` | method | `cli/graph_advisor.py:605` | `def truncate_to_budget(self, payload, budget_tokens)` |
| `GraphOverlayConfig` | class | `cli/graph_overlay.py:41` | `class GraphOverlayConfig` |
| `GraphOverlayItem` | class | `cli/graph_overlay.py:59` | `class GraphOverlayItem` |
| `GraphOverlayState` | class | `cli/graph_overlay.py:69` | `class GraphOverlayState` |
| `GraphOverlayView` | class | `cli/graph_overlay.py:33` | `class GraphOverlayView(StrEnum)` |
| `_GraphOverlayApp` | class | `cli/graph_overlay.py:246` | `class _GraphOverlayApp(App)` |
| `__init__` | method | `cli/graph_overlay.py:260` | `def __init__(self)` |
| `_advisor` | method | `cli/graph_overlay.py:174` | `def _advisor(self)` |
| `_build_app` | function | `cli/graph_overlay.py:235` | `def _build_app(state, theme)` |
| `_default_advisor_factory` | function | `cli/graph_overlay.py:181` | `def _default_advisor_factory()` |
| `_edge_badge` | method | `cli/graph_overlay.py:159` | `def _edge_badge(self, edges)` |
| `_god_nodes` | method | `cli/graph_overlay.py:111` | `def _god_nodes(self, advisor)` |
| `_neighbors` | method | `cli/graph_overlay.py:119` | `def _neighbors(self, advisor)` |
| `_refresh` | method | `cli/graph_overlay.py:287` | `def _refresh(self)` |
| `_row` | method | `cli/graph_overlay.py:147` | `def _row(self, payload, badge)` |
| `_truncate` | method | `cli/graph_overlay.py:169` | `def _truncate(self, value)` |
| `action_close` | method | `cli/graph_overlay.py:284` | `def action_close(self)` |
| `action_toggle_view` | method | `cli/graph_overlay.py:280` | `def action_toggle_view(self)` |
| `build_state` | function | `cli/graph_overlay.py:192` | `def build_state(config, advisor_factory)` |
| `compose` | method | `cli/graph_overlay.py:265` | `def compose(self)` |
| `is_available` | method | `cli/graph_overlay.py:77` | `def is_available(self)` |
| `launch_overlay` | function | `cli/graph_overlay.py:203` | `def launch_overlay(payload, state, runner)` |
| `on_input_changed` | method | `cli/graph_overlay.py:276` | `def on_input_changed(self, event)` |
| `on_mount` | method | `cli/graph_overlay.py:273` | `def on_mount(self)` |
| `set_focus` | method | `cli/graph_overlay.py:87` | `def set_focus(self, value)` |
| `snapshot` | method | `cli/graph_overlay.py:102` | `def snapshot(self)` |
| `toggle_view` | method | `cli/graph_overlay.py:95` | `def toggle_view(self)` |
| `HeadlessRunner` | class | `cli/headless.py:62` | `class HeadlessRunner` |
| `__init__` | method | `cli/headless.py:72` | `def __init__(self, shell, json_output, profile_path)` |
| `apply_profile` | function | `cli/headless.py:48` | `def apply_profile(config, profile)` |
| `load_profile` | function | `cli/headless.py:31` | `def load_profile(path)` |
| `run_chain` | method | `cli/headless.py:136` | `def run_chain(self, commands)` |
| `run_command` | method | `cli/headless.py:87` | `def run_command(self, cmd, timeout)` |
| `PhaseProgress` | class | `cli/killchain.py:29` | `class PhaseProgress` |
| `_detect_current_phase` | function | `cli/killchain.py:58` | `def _detect_current_phase(events, world, phase_keys)` |
| `_phase_from_event` | function | `cli/killchain.py:48` | `def _phase_from_event(event)` |
| `compute_killchain` | function | `cli/killchain.py:83` | `def compute_killchain(events, world, phases)` |
| `LazyMonitorApp` | class | `cli/lazy_monitor.py:89` | `class LazyMonitorApp` |
| `PromptModal` | class | `cli/lazy_monitor.py:61` | `class PromptModal` |
| `__init__` | method | `cli/lazy_monitor.py:66` | `def __init__(self, title, placeholder)` |
| `__init__` | method | `cli/lazy_monitor.py:124` | `def __init__(self, task_id, engine, config, params)` |
| `_append_activity` | method | `cli/lazy_monitor.py:387` | `def _append_activity(self, text, style)` |
| `_append_activity_text` | method | `cli/lazy_monitor.py:392` | `def _append_activity_text(self, line)` |
| `_decide` | method | `cli/lazy_monitor.py:433` | `def _decide(self, verdict)` |
| `_done` | function | `cli/lazy_monitor.py:448` | `def _done(text)` |
| `_done` | function | `cli/lazy_monitor.py:467` | `def _done(text)` |
| `_drain_activity` | method | `cli/lazy_monitor.py:270` | `def _drain_activity(self)` |
| `_drain_guard` | method | `cli/lazy_monitor.py:290` | `def _drain_guard(self)` |
| `_drain_traffic` | method | `cli/lazy_monitor.py:304` | `def _drain_traffic(self)` |
| `_finish` | method | `cli/lazy_monitor.py:246` | `def _finish(self, result)` |
| `_focus_tab` | method | `cli/lazy_monitor.py:501` | `def _focus_tab(self, tab_id)` |
| `_hint_via_graph` | function | `cli/lazy_monitor.py:566` | `def _hint_via_graph(task_id, text)` |
| `_init_tails` | method | `cli/lazy_monitor.py:203` | `def _init_tails(self)` |
| `_overview` | method | `cli/lazy_monitor.py:263` | `def _overview(self)` |
| `_poll` | method | `cli/lazy_monitor.py:252` | `def _poll(self)` |
| `_render_approvals` | method | `cli/lazy_monitor.py:313` | `def _render_approvals(self)` |
| `_render_findings` | method | `cli/lazy_monitor.py:332` | `def _render_findings(self)` |
| `_render_stages` | method | `cli/lazy_monitor.py:351` | `def _render_stages(self, overview)` |
| `_reset_view` | method | `cli/lazy_monitor.py:537` | `def _reset_view(self)` |
| `_resolve_task` | method | `cli/lazy_monitor.py:192` | `def _resolve_task(self)` |
| `_run` | function | `cli/lazy_monitor.py:225` | `def _run()` |
| `_running_intent` | method | `cli/lazy_monitor.py:399` | `def _running_intent(self)` |
| `_start_engine` | method | `cli/lazy_monitor.py:213` | `def _start_engine(self)` |
| `_stream` | function | `cli/lazy_monitor.py:217` | `def _stream(line)` |
| `action_approve` | method | `cli/lazy_monitor.py:425` | `def action_approve(self)` |
| `action_deny` | method | `cli/lazy_monitor.py:429` | `def action_deny(self)` |
| `action_dismiss` | method | `cli/lazy_monitor.py:84` | `def action_dismiss(self, value)` |
| `action_focus_worker` | method | `cli/lazy_monitor.py:508` | `def action_focus_worker(self, index)` |
| `action_hint` | method | `cli/lazy_monitor.py:445` | `def action_hint(self)` |
| `action_kill` | method | `cli/lazy_monitor.py:477` | `def action_kill(self)` |
| `action_next_task` | method | `cli/lazy_monitor.py:518` | `def action_next_task(self)` |
| `action_pause` | method | `cli/lazy_monitor.py:409` | `def action_pause(self)` |
| `action_resume` | method | `cli/lazy_monitor.py:417` | `def action_resume(self)` |
| `action_steer` | method | `cli/lazy_monitor.py:460` | `def action_steer(self)` |
| `action_tab_findings` | method | `cli/lazy_monitor.py:489` | `def action_tab_findings(self)` |
| `action_tab_guard` | method | `cli/lazy_monitor.py:493` | `def action_tab_guard(self)` |
| `action_tab_traffic` | method | `cli/lazy_monitor.py:497` | `def action_tab_traffic(self)` |
| `compose` | method | `cli/lazy_monitor.py:72` | `def compose(self)` |
| `compose` | method | `cli/lazy_monitor.py:140` | `def compose(self)` |
| `on_input_submitted` | method | `cli/lazy_monitor.py:80` | `def on_input_submitted(self, event)` |
| `on_mount` | method | `cli/lazy_monitor.py:168` | `def on_mount(self)` |
| `run_monitor_command` | function | `cli/lazy_monitor.py:575` | `def run_monitor_command(task_id)` |
| `run_monitor_session` | function | `cli/lazy_monitor.py:589` | `def run_monitor_session(engine, config, params)` |
| `LazyOrchestratorApp` | class | `cli/lazy_orchestrator.py:147` | `class LazyOrchestratorApp(OrchestratorAssetsMixin)` |
| `__init__` | method | `cli/lazy_orchestrator.py:180` | `def __init__(self, payload_path, task_id, shell, param_root)` |
| `_active_tab` | method | `cli/lazy_orchestrator.py:779` | `def _active_tab(self)` |
| `_confirmed` | function | `cli/lazy_orchestrator.py:1158` | `def _confirmed(answer)` |
| `_confirmed_bof` | function | `cli/lazy_orchestrator.py:1171` | `def _confirmed_bof(answer)` |
| `_confirmed_gym` | function | `cli/lazy_orchestrator.py:1184` | `def _confirmed_gym(answer)` |
| `_confirmed_param` | function | `cli/lazy_orchestrator.py:1208` | `def _confirmed_param(answer)` |
| `_confirmed_trigger` | function | `cli/lazy_orchestrator.py:1225` | `def _confirmed_trigger(answer)` |
| `_done` | function | `cli/lazy_orchestrator.py:820` | `def _done(values)` |
| `_done` | function | `cli/lazy_orchestrator.py:1109` | `def _done(values)` |
| `_done_bof` | function | `cli/lazy_orchestrator.py:1019` | `def _done_bof(values)` |
| `_done_chain` | function | `cli/lazy_orchestrator.py:1005` | `def _done_chain(playbook)` |
| `_done_new` | function | `cli/lazy_orchestrator.py:930` | `def _done_new(values)` |
| `_done_new_gym` | function | `cli/lazy_orchestrator.py:958` | `def _done_new_gym(values)` |
| `_done_param` | function | `cli/lazy_orchestrator.py:837` | `def _done_param(values)` |
| `_done_param` | function | `cli/lazy_orchestrator.py:1082` | `def _done_param(values)` |
| `_done_rule` | function | `cli/lazy_orchestrator.py:867` | `def _done_rule(values)` |
| `_done_trigger` | function | `cli/lazy_orchestrator.py:795` | `def _done_trigger(values)` |
| `_done_verb` | function | `cli/lazy_orchestrator.py:888` | `def _done_verb(values)` |
| `_param_root` | method | `cli/lazy_orchestrator.py:211` | `def _param_root(self)` |
| `_picked` | function | `cli/lazy_orchestrator.py:884` | `def _picked(value)` |
| `_picked_kind` | function | `cli/lazy_orchestrator.py:791` | `def _picked_kind(value)` |
| `_poll_now` | method | `cli/lazy_orchestrator.py:394` | `def _poll_now(self)` |
| `_refresh_params` | method | `cli/lazy_orchestrator.py:608` | `def _refresh_params(self)` |
| `_resolve_task` | method | `cli/lazy_orchestrator.py:376` | `def _resolve_task(self)` |
| `_selected_row` | method | `cli/lazy_orchestrator.py:726` | `def _selected_row(self, table_id)` |
| `_submit_config_save` | method | `cli/lazy_orchestrator.py:518` | `def _submit_config_save(self)` |
| `_submit_harness_save` | method | `cli/lazy_orchestrator.py:554` | `def _submit_harness_save(self)` |
| `_submit_pacing_save` | method | `cli/lazy_orchestrator.py:534` | `def _submit_pacing_save(self)` |
| `action_add_item` | method | `cli/lazy_orchestrator.py:786` | `def action_add_item(self)` |
| `action_delete_item` | method | `cli/lazy_orchestrator.py:1130` | `def action_delete_item(self)` |
| `action_edit_item` | method | `cli/lazy_orchestrator.py:1046` | `def action_edit_item(self)` |
| `action_refresh` | method | `cli/lazy_orchestrator.py:577` | `def action_refresh(self)` |
| `action_save_config` | method | `cli/lazy_orchestrator.py:769` | `def action_save_config(self)` |
| `action_seed_triggers` | method | `cli/lazy_orchestrator.py:592` | `def action_seed_triggers(self)` |
| `action_toggle_item` | method | `cli/lazy_orchestrator.py:735` | `def action_toggle_item(self)` |
| `add_auto_verb` | method | `cli/lazy_orchestrator.py:345` | `def add_auto_verb(self, name, keywords, needs_target, description, phases)` |
| `command_descriptions` | function | `cli/lazy_orchestrator.py:102` | `def command_descriptions()` |
| `compose` | method | `cli/lazy_orchestrator.py:215` | `def compose(self)` |
| `create_param` | method | `cli/lazy_orchestrator.py:631` | `def create_param(self, name, kind, default, description, category)` |
| `delete_param` | method | `cli/lazy_orchestrator.py:703` | `def delete_param(self, name)` |
| `discover_shell_commands` | function | `cli/lazy_orchestrator.py:69` | `def discover_shell_commands()` |
| `on_button_pressed` | method | `cli/lazy_orchestrator.py:501` | `def on_button_pressed(self, event)` |
| `on_mount` | method | `cli/lazy_orchestrator.py:301` | `def on_mount(self)` |
| `remove_auto_verb` | method | `cli/lazy_orchestrator.py:368` | `def remove_auto_verb(self, name)` |
| `run_orchestrator_console` | function | `cli/lazy_orchestrator.py:1235` | `def run_orchestrator_console(task_id, shell)` |
| `toggle_stage` | method | `cli/lazy_orchestrator.py:320` | `def toggle_stage(self, name)` |
| `toggle_verb` | method | `cli/lazy_orchestrator.py:329` | `def toggle_verb(self, name)` |
| `update_param` | method | `cli/lazy_orchestrator.py:671` | `def update_param(self, name, default, description)` |
| `verb_candidates` | function | `cli/lazy_orchestrator.py:116` | `def verb_candidates()` |
| `PostScanConfig` | class | `cli/lazynmap_post.py:57` | `class PostScanConfig` |
| `PostScanResult` | class | `cli/lazynmap_post.py:76` | `class PostScanResult` |
| `_default_engine_factory` | function | `cli/lazynmap_post.py:180` | `def _default_engine_factory(payload, cfg)` |
| `_emit_event` | function | `cli/lazynmap_post.py:212` | `def _emit_event(cfg, target, plan, plan_path, clock_fn)` |
| `_enabled` | function | `cli/lazynmap_post.py:164` | `def _enabled(payload, cfg)` |
| `_safe_log` | function | `cli/lazynmap_post.py:262` | `def _safe_log(console, message)` |
| `_update_world_model_phase` | function | `cli/lazynmap_post.py:188` | `def _update_world_model_phase(cfg, target, clock_fn)` |
| `run_post_scan` | function | `cli/lazynmap_post.py:94` | `def run_post_scan(target, payload, console, config, engine_factory, plan_config, clock)` |
| `AddonInfo` | class | `cli/marketplace_config.py:134` | `class AddonInfo` |
| `AddonRegistry` | class | `cli/marketplace_config.py:314` | `class AddonRegistry` |
| `MarketplaceConfig` | class | `cli/marketplace_config.py:78` | `class MarketplaceConfig` |
| `MarketplaceConfigApp` | class | `cli/marketplace_config.py:546` | `class MarketplaceConfigApp` |
| `MarketplaceSettings` | class | `cli/marketplace_config.py:508` | `class MarketplaceSettings` |
| `__init__` | method | `cli/marketplace_config.py:331` | `def __init__(self)` |
| `__init__` | method | `cli/marketplace_config.py:578` | `def __init__(self, config, registry, initial, start_tab)` |
| `_active_tab` | method | `cli/marketplace_config.py:614` | `def _active_tab(self)` |
| `_build_initial_settings` | function | `cli/marketplace_config.py:896` | `def _build_initial_settings(registry)` |
| `_confirmed` | function | `cli/marketplace_config.py:849` | `def _confirmed(answer)` |
| `_created` | function | `cli/marketplace_config.py:793` | `def _created(values)` |
| `_from_json` | method | `cli/marketplace_config.py:184` | `def _from_json(cls, path, kind)` |
| `_from_read_only` | method | `cli/marketplace_config.py:206` | `def _from_read_only(cls, path, kind)` |
| `_from_yaml` | method | `cli/marketplace_config.py:160` | `def _from_yaml(cls, path, kind)` |
| `_nuclei_dir` | method | `cli/marketplace_config.py:335` | `def _nuclei_dir(self)` |
| `_parse_nuclei_severity` | method | `cli/marketplace_config.py:415` | `def _parse_nuclei_severity(path)` |
| `_parse_yara_meta` | method | `cli/marketplace_config.py:403` | `def _parse_yara_meta(path)` |
| `_refresh_all` | method | `cli/marketplace_config.py:637` | `def _refresh_all(self)` |
| `_refresh_tab_labels` | method | `cli/marketplace_config.py:643` | `def _refresh_tab_labels(self, tab)` |
| `_refresh_table` | method | `cli/marketplace_config.py:651` | `def _refresh_table(self, tab)` |
| `_rows` | method | `cli/marketplace_config.py:622` | `def _rows(self, tab)` |
| `_saved` | function | `cli/marketplace_config.py:825` | `def _saved(raw)` |
| `_scan_files` | method | `cli/marketplace_config.py:357` | `def _scan_files(self, tab)` |
| `_scan_nuclei` | method | `cli/marketplace_config.py:382` | `def _scan_nuclei(self)` |
| `_scan_yara` | method | `cli/marketplace_config.py:370` | `def _scan_yara(self)` |
| `_selected_addon` | method | `cli/marketplace_config.py:674` | `def _selected_addon(self, tab)` |
| `_selected_row` | method | `cli/marketplace_config.py:681` | `def _selected_row(self, tab)` |
| `_update_detail` | method | `cli/marketplace_config.py:690` | `def _update_detail(self, row_key, tab)` |
| `action_cancel` | method | `cli/marketplace_config.py:867` | `def action_cancel(self)` |
| `action_create` | method | `cli/marketplace_config.py:786` | `def action_create(self)` |
| `action_delete` | method | `cli/marketplace_config.py:839` | `def action_delete(self)` |
| `action_disable_all` | method | `cli/marketplace_config.py:779` | `def action_disable_all(self)` |
| `action_edit` | method | `cli/marketplace_config.py:811` | `def action_edit(self)` |
| `action_enable_all` | method | `cli/marketplace_config.py:772` | `def action_enable_all(self)` |
| `action_focus_filter` | method | `cli/marketplace_config.py:747` | `def action_focus_filter(self)` |
| `action_rescan` | method | `cli/marketplace_config.py:754` | `def action_rescan(self)` |
| `action_save` | method | `cli/marketplace_config.py:863` | `def action_save(self)` |
| `action_toggle` | method | `cli/marketplace_config.py:761` | `def action_toggle(self)` |
| `compose` | method | `cli/marketplace_config.py:593` | `def compose(self)` |
| `configure_marketplace_interactive` | function | `cli/marketplace_config.py:872` | `def configure_marketplace_interactive(config, start_tab)` |
| `create_addon` | method | `cli/marketplace_config.py:447` | `def create_addon(self, tab, name)` |
| `delete_addon` | method | `cli/marketplace_config.py:491` | `def delete_addon(self, addon)` |
| `disable_all` | method | `cli/marketplace_config.py:537` | `def disable_all(self, addons)` |
| `enable_all` | method | `cli/marketplace_config.py:529` | `def enable_all(self, addons)` |
| `from_path` | method | `cli/marketplace_config.py:151` | `def from_path(cls, path, kind)` |
| `is_enabled` | method | `cli/marketplace_config.py:513` | `def is_enabled(self, kind, name)` |
| `marketplace_summary` | function | `cli/marketplace_config.py:907` | `def marketplace_summary(registry)` |
| `on_data_table_row_highlighted` | method | `cli/marketplace_config.py:722` | `def on_data_table_row_highlighted(self, event)` |
| `on_input_changed` | method | `cli/marketplace_config.py:732` | `def on_input_changed(self, event)` |
| `on_mount` | method | `cli/marketplace_config.py:604` | `def on_mount(self)` |
| `on_tabbed_content_tab_activated` | method | `cli/marketplace_config.py:738` | `def on_tabbed_content_tab_activated(self, event)` |
| `read_data` | method | `cli/marketplace_config.py:229` | `def read_data(self)` |
| `read_text` | method | `cli/marketplace_config.py:225` | `def read_text(self)` |
| `rescan` | method | `cli/marketplace_config.py:426` | `def rescan(self, tab)` |
| `save_text` | method | `cli/marketplace_config.py:260` | `def save_text(self, text)` |
| `save_yaml` | method | `cli/marketplace_config.py:303` | `def save_yaml(self, data)` |
| `scan` | method | `cli/marketplace_config.py:342` | `def scan(self, tab)` |
| `set_enabled` | method | `cli/marketplace_config.py:278` | `def set_enabled(self, enabled)` |
| `tab_count` | method | `cli/marketplace_config.py:439` | `def tab_count(self, tab)` |
| `tab_is_read_only` | method | `cli/marketplace_config.py:443` | `def tab_is_read_only(self, tab)` |
| `tab_label` | method | `cli/marketplace_config.py:435` | `def tab_label(self, tab)` |
| `tab_order` | method | `cli/marketplace_config.py:431` | `def tab_order(self)` |
| `toggle` | method | `cli/marketplace_config.py:517` | `def toggle(self, addon)` |
| `toggle_enabled` | method | `cli/marketplace_config.py:299` | `def toggle_enabled(self)` |
| `toggleable` | method | `cli/marketplace_config.py:221` | `def toggleable(self)` |
| `validate_text` | method | `cli/marketplace_config.py:238` | `def validate_text(self, text)` |
| `LootEntry` | class | `cli/ops_commands.py:552` | `class LootEntry` |
| `_bucket` | function | `cli/ops_commands.py:868` | `def _bucket(node)` |
| `_cli_phase_to_host_state` | function | `cli/ops_commands.py:297` | `def _cli_phase_to_host_state(phase)` |
| `_count_glob` | function | `cli/ops_commands.py:457` | `def _count_glob(pattern)` |
| `_count_pivots` | function | `cli/ops_commands.py:385` | `def _count_pivots(sessions_dir)` |
| `_cred_node` | function | `cli/ops_commands.py:765` | `def _cred_node(value)` |
| `_cred_outcomes_for_host` | function | `cli/ops_commands.py:738` | `def _cred_outcomes_for_host(world, host)` |
| `_engagement_phase_to_cli` | function | `cli/ops_commands.py:292` | `def _engagement_phase_to_cli(phase_value)` |
| `_glob_count` | function | `cli/ops_commands.py:375` | `def _glob_count(sessions_dir, pattern)` |
| `_highlight_match` | function | `cli/ops_commands.py:265` | `def _highlight_match(line, rx)` |
| `_host_label` | function | `cli/ops_commands.py:871` | `def _host_label(node)` |
| `_human_age` | function | `cli/ops_commands.py:1481` | `def _human_age(seconds)` |
| `_human_size` | function | `cli/ops_commands.py:1491` | `def _human_size(n)` |
| `_join` | function | `cli/ops_commands.py:908` | `def _join(items)` |
| `_load_tasks` | function | `cli/ops_commands.py:1066` | `def _load_tasks()` |
| `_loot_provenance` | function | `cli/ops_commands.py:664` | `def _loot_provenance(query, sessions_dir)` |
| `_os_identified` | function | `cli/ops_commands.py:367` | `def _os_identified(sessions_dir)` |
| `_phase_rank` | function | `cli/ops_commands.py:287` | `def _phase_rank(phase)` |
| `_print_next_steps` | function | `cli/ops_commands.py:1393` | `def _print_next_steps(rhost, phase, has_scan, cred_count, n_tasks_new, n_hosts)` |
| `_read_json` | function | `cli/ops_commands.py:425` | `def _read_json(path)` |
| `_read_plan` | function | `cli/ops_commands.py:1460` | `def _read_plan()` |
| `_read_world_model` | function | `cli/ops_commands.py:433` | `def _read_world_model(path)` |
| `_render_progress_bar` | function | `cli/ops_commands.py:359` | `def _render_progress_bar(ratio)` |
| `_render_steps` | function | `cli/ops_commands.py:1455` | `def _render_steps(steps)` |
| `_report_artifact_exists` | function | `cli/ops_commands.py:380` | `def _report_artifact_exists(sessions_dir)` |
| `_save_tasks` | function | `cli/ops_commands.py:1073` | `def _save_tasks(tasks)` |
| `_search_csv` | function | `cli/ops_commands.py:211` | `def _search_csv(rx, hits, limit)` |
| `_search_logs` | function | `cli/ops_commands.py:236` | `def _search_logs(rx, hits, limit, sessions_dir)` |
| `_search_transcript_jsonl` | function | `cli/ops_commands.py:177` | `def _search_transcript_jsonl(rx, hits, limit)` |
| `_write_json_atomic` | function | `cli/ops_commands.py:440` | `def _write_json_atomic(path, data)` |
| `gather_loot` | function | `cli/ops_commands.py:578` | `def gather_loot(sessions_dir)` |
| `loot_graph` | function | `cli/ops_commands.py:854` | `def loot_graph(sessions_dir)` |
| `loot_mark` | function | `cli/ops_commands.py:952` | `def loot_mark(selector, outcome, host, sessions_dir)` |
| `loot_reuse` | function | `cli/ops_commands.py:770` | `def loot_reuse(rhost, sessions_dir)` |
| `loot_search` | function | `cli/ops_commands.py:693` | `def loot_search(query, sessions_dir)` |
| `loot_show` | function | `cli/ops_commands.py:621` | `def loot_show(sessions_dir)` |
| `note_add` | function | `cli/ops_commands.py:475` | `def note_add(text, rhost, phase)` |
| `note_list` | function | `cli/ops_commands.py:500` | `def note_list(rhost, limit)` |
| `phase_progress` | function | `cli/ops_commands.py:393` | `def phase_progress(world, sessions_dir)` |
| `pivot_add` | function | `cli/ops_commands.py:994` | `def pivot_add(new_ip, via_ip, note)` |
| `pivot_list` | function | `cli/ops_commands.py:1020` | `def pivot_list()` |
| `print_ctx` | function | `cli/ops_commands.py:74` | `def print_ctx(payload, sessions_dir)` |
| `print_phase` | function | `cli/ops_commands.py:317` | `def print_phase()` |
| `read_phase` | function | `cli/ops_commands.py:279` | `def read_phase()` |
| `resolve_cred_value` | function | `cli/ops_commands.py:924` | `def resolve_cred_value(selector, entries)` |
| `scans_list` | function | `cli/ops_commands.py:1196` | `def scans_list(rhost, sessions_dir)` |
| `sitrep` | function | `cli/ops_commands.py:1249` | `def sitrep(payload, sessions_dir)` |
| `tasks_add` | function | `cli/ops_commands.py:1132` | `def tasks_add(title, operator)` |
| `tasks_done` | function | `cli/ops_commands.py:1153` | `def tasks_done(task_id)` |
| `tasks_list` | function | `cli/ops_commands.py:1077` | `def tasks_list(status_filter, limit)` |
| `tasks_start` | function | `cli/ops_commands.py:1173` | `def tasks_start(task_id)` |
| `tgrep` | function | `cli/ops_commands.py:115` | `def tgrep(pattern)` |
| `value` | method | `cli/ops_commands.py:568` | `def value(self)` |
| `write_phase` | function | `cli/ops_commands.py:302` | `def write_phase(phase)` |
| `ConfigField` | class | `cli/orchestrator_assets_tabs.py:21` | `class ConfigField` |
| `OrchestratorAssetsMixin` | class | `cli/orchestrator_assets_tabs.py:206` | `class OrchestratorAssetsMixin` |
| `_bofs_dir` | method | `cli/orchestrator_assets_tabs.py:622` | `def _bofs_dir(self)` |
| `_chains_dir` | method | `cli/orchestrator_assets_tabs.py:614` | `def _chains_dir(self)` |
| `_coerce` | function | `cli/orchestrator_assets_tabs.py:75` | `def _coerce(raw)` |
| `_edit_bof` | method | `cli/orchestrator_assets_tabs.py:759` | `def _edit_bof(self, filename)` |
| `_edit_gym` | method | `cli/orchestrator_assets_tabs.py:503` | `def _edit_gym(self, gym_id)` |
| `_edit_playbook` | method | `cli/orchestrator_assets_tabs.py:344` | `def _edit_playbook(self, filename)` |
| `_load_guardrails_into_form` | method | `cli/orchestrator_assets_tabs.py:1337` | `def _load_guardrails_into_form(self)` |
| `_load_pacing_into_form` | method | `cli/orchestrator_assets_tabs.py:1067` | `def _load_pacing_into_form(self)` |
| `_load_payload` | method | `cli/orchestrator_assets_tabs.py:1045` | `def _load_payload(self)` |
| `_load_payload_into_form` | method | `cli/orchestrator_assets_tabs.py:1055` | `def _load_payload_into_form(self)` |
| `_payload_assign` | function | `cli/orchestrator_assets_tabs.py:188` | `def _payload_assign(payload, key, value)` |
| `_payload_value` | function | `cli/orchestrator_assets_tabs.py:178` | `def _payload_value(payload, key)` |
| `_playbooks_dir` | method | `cli/orchestrator_assets_tabs.py:209` | `def _playbooks_dir(self)` |
| `_refresh_bofs` | method | `cli/orchestrator_assets_tabs.py:720` | `def _refresh_bofs(self)` |
| `_refresh_chains` | method | `cli/orchestrator_assets_tabs.py:866` | `def _refresh_chains(self)` |
| `_refresh_guard` | method | `cli/orchestrator_assets_tabs.py:1246` | `def _refresh_guard(self)` |
| `_refresh_gyms` | method | `cli/orchestrator_assets_tabs.py:425` | `def _refresh_gyms(self)` |
| `_refresh_harness` | method | `cli/orchestrator_assets_tabs.py:1357` | `def _refresh_harness(self)` |
| `_refresh_models` | method | `cli/orchestrator_assets_tabs.py:1225` | `def _refresh_models(self)` |
| `_refresh_playbooks` | method | `cli/orchestrator_assets_tabs.py:309` | `def _refresh_playbooks(self)` |
| `_refresh_profiles` | method | `cli/orchestrator_assets_tabs.py:573` | `def _refresh_profiles(self)` |
| `_refresh_stages` | method | `cli/orchestrator_assets_tabs.py:1005` | `def _refresh_stages(self)` |
| `_refresh_triggers` | method | `cli/orchestrator_assets_tabs.py:918` | `def _refresh_triggers(self)` |
| `_refresh_verbs` | method | `cli/orchestrator_assets_tabs.py:1021` | `def _refresh_verbs(self)` |
| `_saved` | function | `cli/orchestrator_assets_tabs.py:368` | `def _saved(raw)` |
| `_saved` | function | `cli/orchestrator_assets_tabs.py:524` | `def _saved(raw)` |
| `_saved` | function | `cli/orchestrator_assets_tabs.py:783` | `def _saved(raw)` |
| `_update_bofs_detail` | method | `cli/orchestrator_assets_tabs.py:742` | `def _update_bofs_detail(self, filename)` |
| `_update_chains_detail` | method | `cli/orchestrator_assets_tabs.py:889` | `def _update_chains_detail(self, name)` |
| `_update_gyms_detail` | method | `cli/orchestrator_assets_tabs.py:447` | `def _update_gyms_detail(self, gym_id)` |
| `_update_playbooks_detail` | method | `cli/orchestrator_assets_tabs.py:331` | `def _update_playbooks_detail(self, filename)` |
| `_update_profile_detail` | method | `cli/orchestrator_assets_tabs.py:594` | `def _update_profile_detail(self, name)` |
| `_update_trigger_detail` | method | `cli/orchestrator_assets_tabs.py:950` | `def _update_trigger_detail(self)` |
| `_validate` | function | `cli/orchestrator_assets_tabs.py:357` | `def _validate(raw)` |
| `_validate` | function | `cli/orchestrator_assets_tabs.py:513` | `def _validate(raw)` |
| `_validate` | function | `cli/orchestrator_assets_tabs.py:772` | `def _validate(raw)` |
| `_widget_id` | function | `cli/orchestrator_assets_tabs.py:201` | `def _widget_id(key)` |
| `activate_profile` | method | `cli/orchestrator_assets_tabs.py:562` | `def activate_profile(self, name)` |
| `add_guard_rule` | method | `cli/orchestrator_assets_tabs.py:1209` | `def add_guard_rule(self, pattern, action, reason)` |
| `add_model_member` | method | `cli/orchestrator_assets_tabs.py:1156` | `def add_model_member(self, name, model, priority)` |
| `add_trigger` | method | `cli/orchestrator_assets_tabs.py:987` | `def add_trigger(self, kind, every_sec, arg)` |
| `bof_preview` | method | `cli/orchestrator_assets_tabs.py:654` | `def bof_preview(self, filename, limit)` |
| `bof_rows` | method | `cli/orchestrator_assets_tabs.py:630` | `def bof_rows(self)` |
| `chain_rows` | method | `cli/orchestrator_assets_tabs.py:789` | `def chain_rows(self)` |
| `chain_steps_preview` | method | `cli/orchestrator_assets_tabs.py:798` | `def chain_steps_preview(self, name, limit)` |
| `create_bof_file` | method | `cli/orchestrator_assets_tabs.py:663` | `def create_bof_file(self, filename, name, description, client)` |
| `create_playbook_file` | method | `cli/orchestrator_assets_tabs.py:250` | `def create_playbook_file(self, filename, name, description, platforms)` |
| `delete_bof_file` | method | `cli/orchestrator_assets_tabs.py:695` | `def delete_bof_file(self, filename)` |
| `delete_playbook_file` | method | `cli/orchestrator_assets_tabs.py:283` | `def delete_playbook_file(self, filename)` |
| `format_edr_pause_ranges` | function | `cli/orchestrator_assets_tabs.py:161` | `def format_edr_pause_ranges(value)` |
| `format_sleeper_windows` | function | `cli/orchestrator_assets_tabs.py:121` | `def format_sleeper_windows(value)` |
| `generate_chain` | method | `cli/orchestrator_assets_tabs.py:826` | `def generate_chain(self, playbook_key)` |
| `gym_preview` | method | `cli/orchestrator_assets_tabs.py:411` | `def gym_preview(self, gym_id, limit)` |
| `gym_rows` | method | `cli/orchestrator_assets_tabs.py:374` | `def gym_rows(self)` |
| `on_data_table_row_highlighted` | method | `cli/orchestrator_assets_tabs.py:896` | `def on_data_table_row_highlighted(self, event)` |
| `parse_edr_pause_ranges` | function | `cli/orchestrator_assets_tabs.py:128` | `def parse_edr_pause_ranges(raw)` |
| `parse_sleeper_windows` | function | `cli/orchestrator_assets_tabs.py:92` | `def parse_sleeper_windows(raw)` |
| `playbook_candidates` | method | `cli/orchestrator_assets_tabs.py:291` | `def playbook_candidates(self)` |
| `playbook_preview` | method | `cli/orchestrator_assets_tabs.py:241` | `def playbook_preview(self, filename, limit)` |
| `playbook_rows` | method | `cli/orchestrator_assets_tabs.py:217` | `def playbook_rows(self)` |
| `profile_rows` | method | `cli/orchestrator_assets_tabs.py:537` | `def profile_rows(self)` |
| `rearm_harness` | method | `cli/orchestrator_assets_tabs.py:1326` | `def rearm_harness(self)` |
| `remove_chain` | method | `cli/orchestrator_assets_tabs.py:840` | `def remove_chain(self, name)` |
| `remove_guard_rule` | method | `cli/orchestrator_assets_tabs.py:1217` | `def remove_guard_rule(self, pattern)` |
| `remove_model_member` | method | `cli/orchestrator_assets_tabs.py:1164` | `def remove_model_member(self, name)` |
| `remove_trigger` | method | `cli/orchestrator_assets_tabs.py:979` | `def remove_trigger(self, trigger_id)` |
| `save_bof_text` | method | `cli/orchestrator_assets_tabs.py:683` | `def save_bof_text(self, filename, text)` |
| `save_config` | method | `cli/orchestrator_assets_tabs.py:1134` | `def save_config(self, values)` |
| `save_guardrails` | method | `cli/orchestrator_assets_tabs.py:1268` | `def save_guardrails(self, values)` |
| `save_pacing` | method | `cli/orchestrator_assets_tabs.py:1089` | `def save_pacing(self, values)` |
| `save_playbook_text` | method | `cli/orchestrator_assets_tabs.py:271` | `def save_playbook_text(self, filename, text)` |
| `seed_triggers_from_yaml` | method | `cli/orchestrator_assets_tabs.py:939` | `def seed_triggers_from_yaml(self)` |
| `set_harness` | method | `cli/orchestrator_assets_tabs.py:1184` | `def set_harness(self, enabled)` |
| `set_model_priority` | method | `cli/orchestrator_assets_tabs.py:1172` | `def set_model_priority(self, name, priority)` |
| `stage_bof_file` | method | `cli/orchestrator_assets_tabs.py:703` | `def stage_bof_file(self, filename)` |
| `start_gym` | method | `cli/orchestrator_assets_tabs.py:479` | `def start_gym(self, gym_id, target)` |
| `stop_gym` | method | `cli/orchestrator_assets_tabs.py:487` | `def stop_gym(self, selector)` |
| `toggle_chain` | method | `cli/orchestrator_assets_tabs.py:815` | `def toggle_chain(self, name)` |
| `toggle_gym` | method | `cli/orchestrator_assets_tabs.py:495` | `def toggle_gym(self, gym_id)` |
| `toggle_trigger` | method | `cli/orchestrator_assets_tabs.py:969` | `def toggle_trigger(self, trigger_id)` |
| `trigger_kind_options` | method | `cli/orchestrator_assets_tabs.py:999` | `def trigger_kind_options(self)` |
| `warm_restart_harness` | method | `cli/orchestrator_assets_tabs.py:1314` | `def warm_restart_harness(self)` |
| `OutputMode` | class | `cli/output_mode.py:33` | `class OutputMode` |
| `OutputModeConfig` | class | `cli/output_mode.py:20` | `class OutputModeConfig` |
| `dry_run_line` | function | `cli/output_mode.py:98` | `def dry_run_line(command)` |
| `format_output` | function | `cli/output_mode.py:77` | `def format_output(data, mode)` |
| `parse_output_flags` | function | `cli/output_mode.py:43` | `def parse_output_flags(args, config)` |
| `strip_ansi` | function | `cli/output_mode.py:65` | `def strip_ansi(text)` |
| `CommandIndexError` | class | `cli/palette.py:25` | `class CommandIndexError(RuntimeError)` |
| `all_categories` | function | `cli/palette.py:77` | `def all_categories()` |
| `all_commands` | function | `cli/palette.py:55` | `def all_commands()` |
| `all_phases` | function | `cli/palette.py:72` | `def all_phases()` |
| `duplicates` | function | `cli/palette.py:125` | `def duplicates()` |
| `filter_by_category` | function | `cli/palette.py:92` | `def filter_by_category(category)` |
| `filter_by_phase` | function | `cli/palette.py:82` | `def filter_by_phase(phase)` |
| `get` | function | `cli/palette.py:114` | `def get(name)` |
| `load_index` | function | `cli/palette.py:30` | `def load_index(path)` |
| `search` | function | `cli/palette.py:97` | `def search(query)` |
| `totals` | function | `cli/palette.py:130` | `def totals()` |
| `CompletionPosition` | class | `cli/palette_command.py:737` | `class CompletionPosition` |
| `PaletteArgs` | class | `cli/palette_command.py:123` | `class PaletteArgs` |
| `PaletteArgumentParser` | class | `cli/palette_command.py:132` | `class PaletteArgumentParser` |
| `PaletteCompleter` | class | `cli/palette_command.py:744` | `class PaletteCompleter` |
| `PaletteIndexQuery` | class | `cli/palette_command.py:184` | `class PaletteIndexQuery` |
| `PaletteJsonRenderer` | class | `cli/palette_command.py:514` | `class PaletteJsonRenderer` |
| `PaletteJsonResult` | class | `cli/palette_command.py:487` | `class PaletteJsonResult` |
| `PaletteMode` | class | `cli/palette_command.py:33` | `class PaletteMode(Enum)` |
| `PaletteRenderConfig` | class | `cli/palette_command.py:44` | `class PaletteRenderConfig` |
| `PaletteRenderer` | class | `cli/palette_command.py:277` | `class PaletteRenderer` |
| `PaletteViewConfig` | class | `cli/palette_command.py:605` | `class PaletteViewConfig` |
| `__init__` | method | `cli/palette_command.py:149` | `def __init__(self, config)` |
| `__init__` | method | `cli/palette_command.py:193` | `def __init__(self, index)` |
| `__init__` | method | `cli/palette_command.py:285` | `def __init__(self, config)` |
| `__init__` | method | `cli/palette_command.py:522` | `def __init__(self, config)` |
| `__init__` | method | `cli/palette_command.py:755` | `def __init__(self, config)` |
| `_enrich_commands_for_view` | function | `cli/palette_command.py:665` | `def _enrich_commands_for_view(rows)` |
| `_enrich_detail_entry` | function | `cli/palette_command.py:409` | `def _enrich_detail_entry(entry)` |
| `_ensure_neighbour_keys` | function | `cli/palette_command.py:689` | `def _ensure_neighbour_keys(rows)` |
| `_filter_phase_rows` | function | `cli/palette_command.py:395` | `def _filter_phase_rows(rows, query)` |
| `_filter_prefix` | method | `cli/palette_command.py:797` | `def _filter_prefix(candidates, text)` |
| `_format_name_summary_table` | method | `cli/palette_command.py:383` | `def _format_name_summary_table(self, header, rows)` |
| `_format_neighbours` | method | `cli/palette_command.py:370` | `def _format_neighbours(self, values)` |
| `_load_recent_commands` | function | `cli/palette_command.py:712` | `def _load_recent_commands()` |
| `_ordered_phase_ids` | function | `cli/palette_command.py:728` | `def _ordered_phase_ids(config, phase_counts)` |
| `_ordered_phases` | method | `cli/palette_command.py:376` | `def _ordered_phases(self, phase_counts)` |
| `_tokenise` | method | `cli/palette_command.py:784` | `def _tokenise(self, line, endidx)` |
| `build_palette_view` | function | `cli/palette_command.py:619` | `def build_palette_view(index)` |
| `commands` | method | `cli/palette_command.py:197` | `def commands(self)` |
| `complete` | method | `cli/palette_command.py:758` | `def complete(self, text, line, endidx, index)` |
| `detail` | method | `cli/palette_command.py:234` | `def detail(self, target)` |
| `in_phase` | method | `cli/palette_command.py:213` | `def in_phase(self, phase)` |
| `next_phase` | method | `cli/palette_command.py:249` | `def next_phase(self, current)` |
| `parse` | method | `cli/palette_command.py:152` | `def parse(self, line)` |
| `phase_counts` | method | `cli/palette_command.py:208` | `def phase_counts(self)` |
| `phases` | method | `cli/palette_command.py:203` | `def phases(self)` |
| `render` | function | `cli/palette_command.py:447` | `def render(index, line)` |
| `render_detail` | method | `cli/palette_command.py:320` | `def render_detail(self, entry)` |
| `render_detail` | method | `cli/palette_command.py:549` | `def render_detail(self, target, entry)` |
| `render_json` | function | `cli/palette_command.py:566` | `def render_json(index, line)` |
| `render_next` | method | `cli/palette_command.py:360` | `def render_next(self, phase, rows)` |
| `render_next` | method | `cli/palette_command.py:557` | `def render_next(self, phase, rows)` |
| `render_overview` | method | `cli/palette_command.py:288` | `def render_overview(self, phase_counts)` |
| `render_overview` | method | `cli/palette_command.py:525` | `def render_overview(self, phase_counts)` |
| `render_phase` | method | `cli/palette_command.py:304` | `def render_phase(self, phase, rows)` |
| `render_phase` | method | `cli/palette_command.py:532` | `def render_phase(self, phase, query, rows)` |
| `render_search` | method | `cli/palette_command.py:312` | `def render_search(self, query, rows)` |
| `render_search` | method | `cli/palette_command.py:541` | `def render_search(self, query, rows)` |
| `search` | method | `cli/palette_command.py:218` | `def search(self, query)` |
| `to_dict` | method | `cli/palette_command.py:502` | `def to_dict(self)` |
| `truncate_summary` | method | `cli/palette_command.py:107` | `def truncate_summary(self, summary)` |
| `GraphIndex` | class | `cli/palette_graph.py:74` | `class GraphIndex` |
| `GraphIndexError` | class | `cli/palette_graph.py:39` | `class GraphIndexError(RuntimeError)` |
| `GraphLookupConfig` | class | `cli/palette_graph.py:44` | `class GraphLookupConfig` |
| `_build_adjacency` | function | `cli/palette_graph.py:90` | `def _build_adjacency(document)` |
| `_command_name_from_label` | function | `cli/palette_graph.py:68` | `def _command_name_from_label(label)` |
| `_filter_neighbours` | function | `cli/palette_graph.py:161` | `def _filter_neighbours(neighbours)` |
| `_looks_like_command_label` | function | `cli/palette_graph.py:63` | `def _looks_like_command_label(label)` |
| `callees` | function | `cli/palette_graph.py:179` | `def callees(graph, command_name)` |
| `enrich_commands` | function | `cli/palette_graph.py:309` | `def enrich_commands(graph, rows)` |
| `enrich_detail` | function | `cli/palette_graph.py:287` | `def enrich_detail(graph, entry)` |
| `load_graph` | function | `cli/palette_graph.py:127` | `def load_graph(path)` |
| `related_commands` | function | `cli/palette_graph.py:226` | `def related_commands(graph, command_name)` |
| `safe_load_graph` | function | `cli/palette_graph.py:149` | `def safe_load_graph(path)` |
| `PaletteOverlayConfig` | class | `cli/palette_overlay.py:38` | `class PaletteOverlayConfig` |
| `PaletteOverlayState` | class | `cli/palette_overlay.py:70` | `class PaletteOverlayState` |
| `PaletteRow` | class | `cli/palette_overlay.py:59` | `class PaletteRow` |
| `_PaletteOverlayApp` | class | `cli/palette_overlay.py:240` | `class _PaletteOverlayApp(App)` |
| `__init__` | method | `cli/palette_overlay.py:255` | `def __init__(self)` |
| `_build_app` | function | `cli/palette_overlay.py:228` | `def _build_app(state, theme)` |
| `_commit_from_item` | method | `cli/palette_overlay.py:292` | `def _commit_from_item(self, item)` |
| `_format_row` | method | `cli/palette_overlay.py:314` | `def _format_row(self, row)` |
| `_load_index` | function | `cli/palette_overlay.py:151` | `def _load_index()` |
| `_load_recents` | function | `cli/palette_overlay.py:136` | `def _load_recents()` |
| `_refresh_rows` | method | `cli/palette_overlay.py:300` | `def _refresh_rows(self)` |
| `_score` | method | `cli/palette_overlay.py:113` | `def _score(self, name, summary, needle, is_recent)` |
| `_truncate` | method | `cli/palette_overlay.py:130` | `def _truncate(self, value, max_chars)` |
| `action_cancel` | method | `cli/palette_overlay.py:282` | `def action_cancel(self)` |
| `action_select_current` | method | `cli/palette_overlay.py:285` | `def action_select_current(self)` |
| `build_state` | function | `cli/palette_overlay.py:162` | `def build_state(payload, index, recents, config)` |
| `compose` | method | `cli/palette_overlay.py:261` | `def compose(self)` |
| `launch_overlay` | function | `cli/palette_overlay.py:188` | `def launch_overlay(payload, state, runner)` |
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
| `_build_index` | function | `cli/palette_telemetry.py:123` | `def _build_index(rows)` |
| `_normalise_command` | function | `cli/palette_telemetry.py:97` | `def _normalise_command(value)` |
| `_read_csv_rows` | function | `cli/palette_telemetry.py:107` | `def _read_csv_rows(path)` |
| `command_stats` | function | `cli/palette_telemetry.py:216` | `def command_stats(telemetry, command_name)` |
| `enrich_commands` | function | `cli/palette_telemetry.py:300` | `def enrich_commands(telemetry, rows)` |
| `enrich_detail` | function | `cli/palette_telemetry.py:275` | `def enrich_detail(telemetry, entry)` |
| `load_telemetry` | function | `cli/palette_telemetry.py:186` | `def load_telemetry(path)` |
| `recents` | function | `cli/palette_telemetry.py:259` | `def recents(telemetry)` |
| `runs_after` | function | `cli/palette_telemetry.py:239` | `def runs_after(telemetry, command_name)` |

Next: [SYMBOLS_p6.md](SYMBOLS_p6.md)
