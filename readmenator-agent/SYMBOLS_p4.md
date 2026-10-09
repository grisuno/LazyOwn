# Symbols (page 4 of 35)
Previous: [SYMBOLS_p3.md](SYMBOLS_p3.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `CheckResult` | class | `cli/doctor.py:96` | `class CheckResult` |
| `DoctorReport` | class | `cli/doctor.py:113` | `class DoctorReport` |
| `PackageSpec` | class | `cli/doctor.py:56` | `class PackageSpec` |
| `_apply_fix` | method | `cli/doctor.py:525` | `def _apply_fix(check, root, venv_pip, console)` |
| `_status_cell` | method | `cli/doctor.py:398` | `def _status_cell(status)` |
| `check_certificates` | method | `cli/doctor.py:248` | `def check_certificates(root)` |
| `check_command_index` | method | `cli/doctor.py:313` | `def check_command_index(root)` |
| `check_external_tools` | method | `cli/doctor.py:343` | `def check_external_tools(checker)` |
| `check_packages` | method | `cli/doctor.py:209` | `def check_packages(specs, finder)` |
| `check_payload` | method | `cli/doctor.py:269` | `def check_payload(root)` |
| `check_python_version` | method | `cli/doctor.py:143` | `def check_python_version(version_info)` |
| `check_seclists` | method | `cli/doctor.py:289` | `def check_seclists(finder)` |
| `check_virtualenv` | method | `cli/doctor.py:172` | `def check_virtualenv()` |
| `failures` | method | `cli/doctor.py:119` | `def failures(self)` |
| `fix_report` | method | `cli/doctor.py:468` | `def fix_report(report)` |
| `gather_report` | method | `cli/doctor.py:368` | `def gather_report(root)` |
| `healthy` | method | `cli/doctor.py:129` | `def healthy(self)` |
| `overall_status` | method | `cli/doctor.py:134` | `def overall_status(self)` |
| `render_report` | method | `cli/doctor.py:406` | `def render_report(report, console)` |
| `run` | method | `cli/doctor.py:451` | `def run(root, console)` |
| `warnings` | method | `cli/doctor.py:124` | `def warnings(self)` |
| `EngagementState` | class | `cli/engagement_hooks.py:242` | `class EngagementState` |
| `_award_elo` | method | `cli/engagement_hooks.py:734` | `def _award_elo(cmd, first_time, new_phase, current_phase)` |
| `_check_badges` | method | `cli/engagement_hooks.py:1009` | `def _check_badges(cmd, first_time)` |
| `_check_karma_up` | method | `cli/engagement_hooks.py:864` | `def _check_karma_up(state)` |
| `_commands_in_phase` | method | `cli/engagement_hooks.py:409` | `def _commands_in_phase(phase, index)` |
| `_fire_vri_reward` | method | `cli/engagement_hooks.py:672` | `def _fire_vri_reward(state, ctx)` |
| `_is_recordable_command` | method | `cli/engagement_hooks.py:306` | `def _is_recordable_command(cmd)` |
| `_load_index` | method | `cli/engagement_hooks.py:290` | `def _load_index()` |
| `_load_state` | method | `cli/engagement_hooks.py:260` | `def _load_state()` |
| `_next_threshold` | method | `cli/engagement_hooks.py:394` | `def _next_threshold(current)` |
| `_normalize_command` | method | `cli/engagement_hooks.py:301` | `def _normalize_command(cmd)` |
| `_persist_notification` | method | `cli/engagement_hooks.py:828` | `def _persist_notification(html)` |
| `_phase_for_cmd` | method | `cli/engagement_hooks.py:400` | `def _phase_for_cmd(cmd, index)` |
| `_print_badge` | method | `cli/engagement_hooks.py:1056` | `def _print_badge(name, description)` |
| `_render_arsenal_tip` | method | `cli/engagement_hooks.py:536` | `def _render_arsenal_tip(ctx)` |
| `_render_exploration` | method | `cli/engagement_hooks.py:488` | `def _render_exploration(ctx)` |
| `_render_hidden_feature` | method | `cli/engagement_hooks.py:522` | `def _render_hidden_feature(ctx)` |
| `_render_methodology_note` | method | `cli/engagement_hooks.py:630` | `def _render_methodology_note(ctx)` |
| `_render_methodology_objective` | method | `cli/engagement_hooks.py:583` | `def _render_methodology_objective(ctx)` |
| `_render_methodology_task` | method | `cli/engagement_hooks.py:544` | `def _render_methodology_task(ctx)` |
| `_render_phase_badge` | method | `cli/engagement_hooks.py:506` | `def _render_phase_badge(ctx)` |
| `_render_streak` | method | `cli/engagement_hooks.py:459` | `def _render_streak(ctx)` |
| `_run_curiosity` | method | `cli/engagement_hooks.py:431` | `def _run_curiosity(cmd, state, index)` |
| `_sanitize_seen` | method | `cli/engagement_hooks.py:332` | `def _sanitize_seen(names, known)` |
| `_save_state` | method | `cli/engagement_hooks.py:280` | `def _save_state(state)` |
| `_summary_for_cmd` | method | `cli/engagement_hooks.py:414` | `def _summary_for_cmd(cmd, index)` |
| `_sync_user_elo` | method | `cli/engagement_hooks.py:760` | `def _sync_user_elo(delta)` |
| `get_karma_name` | method | `cli/engagement_hooks.py:716` | `def get_karma_name(elo)` |
| `get_state_snapshot` | method | `cli/engagement_hooks.py:978` | `def get_state_snapshot()` |
| `heal_commands_seen` | method | `cli/engagement_hooks.py:365` | `def heal_commands_seen(known)` |
| `render_engagement_hook` | method | `cli/engagement_hooks.py:898` | `def render_engagement_hook(cmd, phase, enabled)` |
| `reset_session` | method | `cli/engagement_hooks.py:1066` | `def reset_session()` |
| `ExploitHit` | class | `cli/exploit_advisor.py:144` | `class ExploitHit` |
| `ServiceInfo` | class | `cli/exploit_advisor.py:111` | `class ServiceInfo` |
| `ServiceResult` | class | `cli/exploit_advisor.py:153` | `class ServiceResult` |
| `display_name` | method | `cli/exploit_advisor.py:128` | `def display_name(self)` |
| `find_nmap_xml` | method | `cli/exploit_advisor.py:203` | `def find_nmap_xml(rhost, sessions_dir)` |
| `inject_exploit_tasks` | method | `cli/exploit_advisor.py:338` | `def inject_exploit_tasks(results, rhost, tasks_path)` |
| `next_commands` | method | `cli/exploit_advisor.py:132` | `def next_commands(self)` |
| `parse_nmap_xml` | method | `cli/exploit_advisor.py:164` | `def parse_nmap_xml(path)` |
| `print_exploit_summary` | method | `cli/exploit_advisor.py:222` | `def print_exploit_summary(results, rhost)` |
| `save_ss_results` | method | `cli/exploit_advisor.py:296` | `def save_ss_results(results, rhost, sessions_dir)` |
| `search_query` | method | `cli/exploit_advisor.py:122` | `def search_query(self)` |
| `AddonCatalog` | class | `cli/exploration.py:252` | `class AddonCatalog` |
| `AddonEntry` | class | `cli/exploration.py:105` | `class AddonEntry` |
| `CoverageReport` | class | `cli/exploration.py:132` | `class CoverageReport` |
| `DiscoveredService` | class | `cli/exploration.py:87` | `class DiscoveredService` |
| `ExplorationConfig` | class | `cli/exploration.py:68` | `class ExplorationConfig` |
| `ExplorationEngine` | class | `cli/exploration.py:502` | `class ExplorationEngine` |
| `HistoryReader` | class | `cli/exploration.py:470` | `class HistoryReader` |
| `NmapXmlReader` | class | `cli/exploration.py:169` | `class NmapXmlReader` |
| `ToolCatalog` | class | `cli/exploration.py:333` | `class ToolCatalog` |
| `ToolEntry` | class | `cli/exploration.py:119` | `class ToolEntry` |
| `TriggerMatcher` | class | `cli/exploration.py:410` | `class TriggerMatcher` |
| `__init__` | method | `cli/exploration.py:176` | `def __init__(self, config)` |
| `__init__` | method | `cli/exploration.py:264` | `def __init__(self, config)` |
| `__init__` | method | `cli/exploration.py:344` | `def __init__(self, config)` |
| `__init__` | method | `cli/exploration.py:413` | `def __init__(self, current_os)` |
| `__init__` | method | `cli/exploration.py:473` | `def __init__(self, config)` |
| `__init__` | method | `cli/exploration.py:510` | `def __init__(self, config, current_os)` |
| `_iter_xml_paths` | method | `cli/exploration.py:196` | `def _iter_xml_paths(self, target)` |
| `_load_with_cache` | method | `cli/exploration.py:282` | `def _load_with_cache(self, path)` |
| `_load_with_cache` | method | `cli/exploration.py:362` | `def _load_with_cache(self, path)` |
| `_os_compatible` | method | `cli/exploration.py:452` | `def _os_compatible(self, candidate_os)` |
| `_parse_one` | method | `cli/exploration.py:210` | `def _parse_one(xml_path)` |
| `_parse_one` | method | `cli/exploration.py:304` | `def _parse_one(self, path)` |
| `_parse_one` | method | `cli/exploration.py:384` | `def _parse_one(self, path)` |
| `_trigger_matches` | method | `cli/exploration.py:460` | `def _trigger_matches(trigger, service_name)` |
| `addon_coverage` | method | `cli/exploration.py:153` | `def addon_coverage(self)` |
| `addons` | method | `cli/exploration.py:530` | `def addons(self)` |
| `addons_for_service` | method | `cli/exploration.py:418` | `def addons_for_service(self, service, addons)` |
| `clear_cache` | method | `cli/exploration.py:299` | `def clear_cache(cls)` |
| `clear_cache` | method | `cli/exploration.py:379` | `def clear_cache(cls)` |
| `coverage` | method | `cli/exploration.py:610` | `def coverage(self, target)` |
| `discover` | method | `cli/exploration.py:181` | `def discover(self, target)` |
| `executed_commands` | method | `cli/exploration.py:478` | `def executed_commands(self)` |
| `history` | method | `cli/exploration.py:540` | `def history(self)` |
| `label` | method | `cli/exploration.py:98` | `def label(self)` |
| `load` | method | `cli/exploration.py:269` | `def load(self)` |
| `load` | method | `cli/exploration.py:349` | `def load(self)` |
| `normalise_os` | method | `cli/exploration.py:677` | `def normalise_os(value, default)` |
| `normalise_trigger` | method | `cli/exploration.py:690` | `def normalise_trigger(value)` |
| `resolve_current_os` | method | `cli/exploration.py:656` | `def resolve_current_os(payload)` |
| `service_coverage` | method | `cli/exploration.py:145` | `def service_coverage(self)` |
| `services` | method | `cli/exploration.py:525` | `def services(self, target)` |
| `suggestions_for_target` | method | `cli/exploration.py:545` | `def suggestions_for_target(self, target)` |
| `tool_coverage` | method | `cli/exploration.py:161` | `def tool_coverage(self)` |
| `tools` | method | `cli/exploration.py:535` | `def tools(self)` |
| `tools_for_service` | method | `cli/exploration.py:435` | `def tools_for_service(self, service, tools)` |
| `unexplored_addons` | method | `cli/exploration.py:568` | `def unexplored_addons(self, target)` |
| `unexplored_tools` | method | `cli/exploration.py:589` | `def unexplored_tools(self, target)` |
| `_render_coverage_table` | function | `cli/exploration_view.py:196` | `def _render_coverage_table(console, coverage)` |
| `_render_entries` | function | `cli/exploration_view.py:140` | `def _render_entries(parent, entries, history, style, kind)` |
| `_render_header` | function | `cli/exploration_view.py:71` | `def _render_header(console, target, coverage)` |
| `_render_service_tree` | function | `cli/exploration_view.py:93` | `def _render_service_tree(console, services, grouped, history)` |
| `_render_unexplored` | function | `cli/exploration_view.py:161` | `def _render_unexplored(console, unexplored_addons, unexplored_tools)` |
| `render_exploration` | function | `cli/exploration_view.py:39` | `def render_exploration(console, engine, target, history)` |
| `FuzzyMatchConfig` | class | `cli/fuzzy_match.py:18` | `class FuzzyMatchConfig` |
| `did_you_mean` | method | `cli/fuzzy_match.py:56` | `def did_you_mean(query, candidates)` |
| `suggest` | method | `cli/fuzzy_match.py:28` | `def suggest(query, candidates, limit, config)` |
| `CursesPickerView` | class | `cli/fuzzy_picker.py:234` | `class CursesPickerView(PickerView)` |
| `FuzzyPicker` | class | `cli/fuzzy_picker.py:548` | `class FuzzyPicker` |
| `MatchScorer` | class | `cli/fuzzy_picker.py:161` | `class MatchScorer` |
| `PickerConfig` | class | `cli/fuzzy_picker.py:50` | `class PickerConfig` |
| `PickerItem` | class | `cli/fuzzy_picker.py:140` | `class PickerItem` |
| `PickerView` | class | `cli/fuzzy_picker.py:221` | `class PickerView(ABC)` |
| `ReadlineBridge` | class | `cli/fuzzy_picker.py:580` | `class ReadlineBridge` |
| `ScoredItem` | class | `cli/fuzzy_picker.py:153` | `class ScoredItem` |
| `__init__` | method | `cli/fuzzy_picker.py:170` | `def __init__(self, config)` |
| `__init__` | method | `cli/fuzzy_picker.py:243` | `def __init__(self, config, scorer)` |
| `__init__` | method | `cli/fuzzy_picker.py:551` | `def __init__(self, config, view_factory)` |
| `__init__` | method | `cli/fuzzy_picker.py:592` | `def __init__(self, picker)` |
| `_clamp_scroll` | method | `cli/fuzzy_picker.py:364` | `def _clamp_scroll(self, offset, cursor, total)` |
| `_classify_key` | method | `cli/fuzzy_picker.py:337` | `def _classify_key(self, key)` |
| `_color` | method | `cli/fuzzy_picker.py:539` | `def _color(self, pair_id)` |
| `_draw_box` | method | `cli/fuzzy_picker.py:435` | `def _draw_box(self, stdscr, top, left, height, width)` |
| `_draw_footer` | method | `cli/fuzzy_picker.py:469` | `def _draw_footer(self, stdscr, row_y, left, width)` |
| `_draw_header` | method | `cli/fuzzy_picker.py:450` | `def _draw_header(self, stdscr, top, left, width, query, total, selected)` |
| `_draw_highlighted` | method | `cli/fuzzy_picker.py:516` | `def _draw_highlighted(self, stdscr, row_y, start_x, text, positions, base_attr, selected)` |
| `_draw_item` | method | `cli/fuzzy_picker.py:482` | `def _draw_item(self, stdscr, row_y, left, width, scored, selected)` |
| `_event_loop` | method | `cli/fuzzy_picker.py:287` | `def _event_loop(self, stdscr, items, initial_query)` |
| `_init_colors` | method | `cli/fuzzy_picker.py:263` | `def _init_colors(self)` |
| `_layout` | method | `cli/fuzzy_picker.py:374` | `def _layout(self, stdscr, row_count)` |
| `_on_display_matches` | method | `cli/fuzzy_picker.py:611` | `def _on_display_matches(self, substitution, matches, longest_match_length)` |
| `_redraw_prompt` | method | `cli/fuzzy_picker.py:636` | `def _redraw_prompt()` |
| `_render` | method | `cli/fuzzy_picker.py:405` | `def _render(self, stdscr, ranked, query, cursor_index, scroll_offset)` |
| `_render_empty` | method | `cli/fuzzy_picker.py:386` | `def _render_empty(self, stdscr, query)` |
| `_score` | method | `cli/fuzzy_picker.py:190` | `def _score(self, haystack, query)` |
| `_strip_ansi` | method | `cli/fuzzy_picker.py:632` | `def _strip_ansi(cls, value)` |
| `_subsequence_positions` | method | `cli/fuzzy_picker.py:209` | `def _subsequence_positions(haystack, query)` |
| `_tty_available` | method | `cli/fuzzy_picker.py:260` | `def _tty_available()` |
| `_visible_rows` | method | `cli/fuzzy_picker.py:361` | `def _visible_rows(self)` |
| `config` | method | `cli/fuzzy_picker.py:562` | `def config(self)` |
| `from_payload` | method | `cli/fuzzy_picker.py:117` | `def from_payload(cls, payload)` |
| `install` | method | `cli/fuzzy_picker.py:595` | `def install(self)` |
| `install_fuzzy_completion` | method | `cli/fuzzy_picker.py:645` | `def install_fuzzy_completion(shell, payload, config)` |
| `pick` | method | `cli/fuzzy_picker.py:565` | `def pick(self, items, initial_query)` |
| `rank` | method | `cli/fuzzy_picker.py:173` | `def rank(self, items, query)` |
| `run` | method | `cli/fuzzy_picker.py:231` | `def run(self, items, initial_query)` |
| `run` | method | `cli/fuzzy_picker.py:247` | `def run(self, items, initial_query)` |
| `uninstall` | method | `cli/fuzzy_picker.py:603` | `def uninstall(self)` |
| `GraphAdvisor` | class | `cli/graph_advisor.py:354` | `class GraphAdvisor` |
| `GraphAdvisorConfig` | class | `cli/graph_advisor.py:50` | `class GraphAdvisorConfig` |
| `GraphEdge` | class | `cli/graph_advisor.py:122` | `class GraphEdge` |
| `GraphIndex` | class | `cli/graph_advisor.py:211` | `class GraphIndex` |
| `GraphLoader` | class | `cli/graph_advisor.py:151` | `class GraphLoader` |
| `GraphNode` | class | `cli/graph_advisor.py:98` | `class GraphNode` |
| `GraphScorer` | class | `cli/graph_advisor.py:299` | `class GraphScorer` |
| `ScoredNode` | class | `cli/graph_advisor.py:143` | `class ScoredNode` |
| `__init__` | method | `cli/graph_advisor.py:156` | `def __init__(self, config)` |
| `__init__` | method | `cli/graph_advisor.py:214` | `def __init__(self, data)` |
| `__init__` | method | `cli/graph_advisor.py:304` | `def __init__(self, config)` |
| `__init__` | method | `cli/graph_advisor.py:362` | `def __init__(self, config, loader, index, scorer)` |
| `_best_score` | method | `cli/graph_advisor.py:319` | `def _best_score(self, node, terms, raw_query)` |
| `_bfs_distance` | method | `cli/graph_advisor.py:649` | `def _bfs_distance(index, start, max_hops)` |
| `_build` | method | `cli/graph_advisor.py:223` | `def _build(self)` |
| `_classify_health` | method | `cli/graph_advisor.py:432` | `def _classify_health(self, edges_count, age_days)` |
| `_ensure_index` | method | `cli/graph_advisor.py:675` | `def _ensure_index(self)` |
| `_graph_age_days` | method | `cli/graph_advisor.py:423` | `def _graph_age_days(self, path)` |
| `_iter_all_edges` | method | `cli/graph_advisor.py:665` | `def _iter_all_edges(index)` |
| `_missing_reason` | method | `cli/graph_advisor.py:684` | `def _missing_reason(self)` |
| `_resolve_query` | method | `cli/graph_advisor.py:638` | `def _resolve_query(self, query)` |
| `_score` | method | `cli/graph_advisor.py:335` | `def _score(self, value, terms, query)` |
| `_seed_nodes` | method | `cli/graph_advisor.py:624` | `def _seed_nodes(self, recent_commands)` |
| `_tokens` | method | `cli/graph_advisor.py:350` | `def _tokens(self, query)` |
| `clear_cache` | method | `cli/graph_advisor.py:207` | `def clear_cache(cls)` |
| `community_members` | method | `cli/graph_advisor.py:289` | `def community_members(self, community_id)` |
| `degree` | method | `cli/graph_advisor.py:292` | `def degree(self, node_id)` |
| `degree_ranked` | method | `cli/graph_advisor.py:295` | `def degree_ranked(self)` |
| `did_you_mean` | method | `cli/graph_advisor.py:591` | `def did_you_mean(self, query, limit)` |
| `edges_between` | method | `cli/graph_advisor.py:286` | `def edges_between(self, source, target)` |
| `format_god_nodes` | method | `cli/graph_advisor.py:724` | `def format_god_nodes(results)` |
| `format_neighbors` | method | `cli/graph_advisor.py:706` | `def format_neighbors(result)` |
| `format_search_table` | method | `cli/graph_advisor.py:691` | `def format_search_table(results)` |
| `format_suggestions` | method | `cli/graph_advisor.py:734` | `def format_suggestions(results)` |
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
| `_build_app` | method | `cli/graph_overlay.py:235` | `def _build_app(state, theme)` |
| `_default_advisor_factory` | method | `cli/graph_overlay.py:181` | `def _default_advisor_factory()` |
| `_edge_badge` | method | `cli/graph_overlay.py:159` | `def _edge_badge(self, edges)` |
| `_god_nodes` | method | `cli/graph_overlay.py:111` | `def _god_nodes(self, advisor)` |
| `_neighbors` | method | `cli/graph_overlay.py:119` | `def _neighbors(self, advisor)` |
| `_refresh` | method | `cli/graph_overlay.py:287` | `def _refresh(self)` |
| `_row` | method | `cli/graph_overlay.py:147` | `def _row(self, payload, badge)` |
| `_truncate` | method | `cli/graph_overlay.py:169` | `def _truncate(self, value)` |
| `action_close` | method | `cli/graph_overlay.py:284` | `def action_close(self)` |
| `action_toggle_view` | method | `cli/graph_overlay.py:280` | `def action_toggle_view(self)` |
| `build_state` | method | `cli/graph_overlay.py:192` | `def build_state(config, advisor_factory)` |
| `compose` | method | `cli/graph_overlay.py:265` | `def compose(self)` |
| `is_available` | method | `cli/graph_overlay.py:77` | `def is_available(self)` |
| `launch_overlay` | method | `cli/graph_overlay.py:203` | `def launch_overlay(payload, state, runner)` |
| `on_input_changed` | method | `cli/graph_overlay.py:276` | `def on_input_changed(self, event)` |
| `on_mount` | method | `cli/graph_overlay.py:273` | `def on_mount(self)` |
| `set_focus` | method | `cli/graph_overlay.py:87` | `def set_focus(self, value)` |
| `snapshot` | method | `cli/graph_overlay.py:102` | `def snapshot(self)` |
| `toggle_view` | method | `cli/graph_overlay.py:95` | `def toggle_view(self)` |
| `HeadlessRunner` | class | `cli/headless.py:62` | `class HeadlessRunner` |
| `__init__` | method | `cli/headless.py:72` | `def __init__(self, shell, json_output, profile_path)` |
| `apply_profile` | function | `cli/headless.py:48` | `def apply_profile(config, profile)` |
| `load_profile` | function | `cli/headless.py:31` | `def load_profile(path)` |
| `run_chain` | method | `cli/headless.py:132` | `def run_chain(self, commands)` |
| `run_command` | method | `cli/headless.py:87` | `def run_command(self, cmd, timeout)` |
| `PhaseProgress` | class | `cli/killchain.py:29` | `class PhaseProgress` |
| `_detect_current_phase` | method | `cli/killchain.py:58` | `def _detect_current_phase(events, world, phase_keys)` |
| `_phase_from_event` | method | `cli/killchain.py:48` | `def _phase_from_event(event)` |
| `compute_killchain` | method | `cli/killchain.py:83` | `def compute_killchain(events, world, phases)` |
| `PostScanConfig` | class | `cli/lazynmap_post.py:57` | `class PostScanConfig` |
| `PostScanResult` | class | `cli/lazynmap_post.py:76` | `class PostScanResult` |
| `_atomic_write_json` | method | `cli/lazynmap_post.py:263` | `def _atomic_write_json(path, data, mode)` |
| `_default_engine_factory` | method | `cli/lazynmap_post.py:180` | `def _default_engine_factory(payload, cfg)` |
| `_emit_event` | method | `cli/lazynmap_post.py:213` | `def _emit_event(cfg, target, plan, plan_path, clock_fn)` |
| `_enabled` | method | `cli/lazynmap_post.py:164` | `def _enabled(payload, cfg)` |
| `_safe_log` | method | `cli/lazynmap_post.py:291` | `def _safe_log(console, message)` |
| `_update_world_model_phase` | method | `cli/lazynmap_post.py:188` | `def _update_world_model_phase(cfg, target, clock_fn)` |
| `run_post_scan` | method | `cli/lazynmap_post.py:94` | `def run_post_scan(target, payload, console, config, engine_factory, plan_config, clock)` |
| `AddonInfo` | class | `cli/marketplace_config.py:131` | `class AddonInfo` |
| `AddonRegistry` | class | `cli/marketplace_config.py:197` | `class AddonRegistry` |
| `MarketplaceConfig` | class | `cli/marketplace_config.py:56` | `class MarketplaceConfig` |
| `MarketplaceConfigurator` | class | `cli/marketplace_config.py:378` | `class MarketplaceConfigurator` |
| `MarketplaceSettings` | class | `cli/marketplace_config.py:349` | `class MarketplaceSettings` |
| `__init__` | method | `cli/marketplace_config.py:220` | `def __init__(self)` |
| `__init__` | method | `cli/marketplace_config.py:381` | `def __init__(self, config, registry, initial)` |
| `_build_initial_settings` | method | `cli/marketplace_config.py:774` | `def _build_initial_settings(registry)` |
| `_color` | method | `cli/marketplace_config.py:742` | `def _color(self, pair)` |
| `_create_addon` | method | `cli/marketplace_config.py:480` | `def _create_addon(self, stdscr)` |
| `_cycle_tab` | method | `cli/marketplace_config.py:465` | `def _cycle_tab(self, direction)` |
| `_draw_column_headers` | method | `cli/marketplace_config.py:659` | `def _draw_column_headers(self, stdscr, row_y, left, width, rows)` |
| `_draw_footer` | method | `cli/marketplace_config.py:732` | `def _draw_footer(self, stdscr, row_y, left, width)` |
| `_draw_frame` | method | `cli/marketplace_config.py:604` | `def _draw_frame(self, stdscr, top, left, height, width)` |
| `_draw_header` | method | `cli/marketplace_config.py:618` | `def _draw_header(self, stdscr, top, left, width)` |
| `_draw_preview` | method | `cli/marketplace_config.py:692` | `def _draw_preview(self, stdscr, top, left, width, addon)` |
| `_draw_row` | method | `cli/marketplace_config.py:669` | `def _draw_row(self, stdscr, row_y, left, width, addon, selected)` |
| `_draw_summary` | method | `cli/marketplace_config.py:720` | `def _draw_summary(self, stdscr, row_y, left, width, rows)` |
| `_draw_tabs` | method | `cli/marketplace_config.py:641` | `def _draw_tabs(self, stdscr, row_y, left, width)` |
| `_edit_addon` | method | `cli/marketplace_config.py:470` | `def _edit_addon(self, addon)` |
| `_init_colors` | method | `cli/marketplace_config.py:537` | `def _init_colors(self)` |
| `_loop` | method | `cli/marketplace_config.py:414` | `def _loop(self, stdscr)` |
| `_nuclei_dir` | method | `cli/marketplace_config.py:223` | `def _nuclei_dir(self)` |
| `_parse_nuclei_info` | method | `cli/marketplace_config.py:319` | `def _parse_nuclei_info(path)` |
| `_parse_yara_meta` | method | `cli/marketplace_config.py:307` | `def _parse_yara_meta(path)` |
| `_render` | method | `cli/marketplace_config.py:564` | `def _render(self, stdscr, rows, cursor, offset)` |
| `_rows_for_tab` | method | `cli/marketplace_config.py:411` | `def _rows_for_tab(self, tab)` |
| `_scan_nuclei` | method | `cli/marketplace_config.py:278` | `def _scan_nuclei(self)` |
| `_scan_yara` | method | `cli/marketplace_config.py:259` | `def _scan_yara(self)` |
| `_tty_available` | method | `cli/marketplace_config.py:408` | `def _tty_available()` |
| `configure_marketplace_interactive` | method | `cli/marketplace_config.py:751` | `def configure_marketplace_interactive(config, start_tab)` |
| `disable_all` | method | `cli/marketplace_config.py:372` | `def disable_all(self, addons)` |
| `enable_all` | method | `cli/marketplace_config.py:367` | `def enable_all(self, addons)` |
| `from_yaml` | method | `cli/marketplace_config.py:144` | `def from_yaml(cls, path)` |
| `is_enabled` | method | `cli/marketplace_config.py:354` | `def is_enabled(self, kind, name)` |
| `marketplace_summary` | method | `cli/marketplace_config.py:784` | `def marketplace_summary(registry)` |
| `rescan` | method | `cli/marketplace_config.py:334` | `def rescan(self, tab)` |
| `run` | method | `cli/marketplace_config.py:395` | `def run(self, start_tab)` |
| `save_yaml` | method | `cli/marketplace_config.py:185` | `def save_yaml(self, data)` |
| `scan` | method | `cli/marketplace_config.py:235` | `def scan(self, tab)` |
| `set_enabled` | method | `cli/marketplace_config.py:168` | `def set_enabled(self, enabled)` |
| `tab_count` | method | `cli/marketplace_config.py:344` | `def tab_count(self, tab)` |
| `tab_label` | method | `cli/marketplace_config.py:341` | `def tab_label(self, tab)` |
| `tab_order` | method | `cli/marketplace_config.py:338` | `def tab_order(self)` |
| `toggle` | method | `cli/marketplace_config.py:357` | `def toggle(self, addon)` |
| `toggle_enabled` | method | `cli/marketplace_config.py:164` | `def toggle_enabled(self)` |
| `LootEntry` | class | `cli/ops_commands.py:544` | `class LootEntry` |
| `_bucket` | method | `cli/ops_commands.py:860` | `def _bucket(node)` |
| `_cli_phase_to_host_state` | function | `cli/ops_commands.py:297` | `def _cli_phase_to_host_state(phase)` |
| `_count_glob` | function | `cli/ops_commands.py:449` | `def _count_glob(pattern)` |
| `_count_pivots` | function | `cli/ops_commands.py:384` | `def _count_pivots(sessions_dir)` |
| `_cred_node` | method | `cli/ops_commands.py:757` | `def _cred_node(value)` |
| `_cred_outcomes_for_host` | method | `cli/ops_commands.py:730` | `def _cred_outcomes_for_host(world, host)` |
| `_engagement_phase_to_cli` | function | `cli/ops_commands.py:292` | `def _engagement_phase_to_cli(phase_value)` |
| `_glob_count` | function | `cli/ops_commands.py:374` | `def _glob_count(sessions_dir, pattern)` |
| `_highlight_match` | function | `cli/ops_commands.py:265` | `def _highlight_match(line, rx)` |
| `_host_label` | method | `cli/ops_commands.py:863` | `def _host_label(node)` |
| `_human_age` | method | `cli/ops_commands.py:1462` | `def _human_age(seconds)` |
| `_human_size` | method | `cli/ops_commands.py:1472` | `def _human_size(n)` |
| `_join` | method | `cli/ops_commands.py:900` | `def _join(items)` |
| `_load_tasks` | method | `cli/ops_commands.py:1058` | `def _load_tasks()` |
| `_loot_provenance` | method | `cli/ops_commands.py:656` | `def _loot_provenance(query, sessions_dir)` |
| `_os_identified` | function | `cli/ops_commands.py:366` | `def _os_identified(sessions_dir)` |
| `_phase_rank` | function | `cli/ops_commands.py:287` | `def _phase_rank(phase)` |
| `_print_next_steps` | method | `cli/ops_commands.py:1374` | `def _print_next_steps(rhost, phase, has_scan, cred_count, n_tasks_new, n_hosts)` |
| `_read_json` | function | `cli/ops_commands.py:424` | `def _read_json(path)` |
| `_read_plan` | method | `cli/ops_commands.py:1441` | `def _read_plan()` |
| `_render_progress_bar` | function | `cli/ops_commands.py:359` | `def _render_progress_bar(ratio)` |
| `_render_steps` | method | `cli/ops_commands.py:1436` | `def _render_steps(steps)` |
| `_report_artifact_exists` | function | `cli/ops_commands.py:379` | `def _report_artifact_exists(sessions_dir)` |
| `_save_tasks` | method | `cli/ops_commands.py:1065` | `def _save_tasks(tasks)` |
| `_search_csv` | function | `cli/ops_commands.py:211` | `def _search_csv(rx, hits, limit)` |
| `_search_logs` | function | `cli/ops_commands.py:236` | `def _search_logs(rx, hits, limit, sessions_dir)` |
| `_search_transcript_jsonl` | function | `cli/ops_commands.py:177` | `def _search_transcript_jsonl(rx, hits, limit)` |
| `_write_json_atomic` | function | `cli/ops_commands.py:432` | `def _write_json_atomic(path, data)` |
| `gather_loot` | method | `cli/ops_commands.py:570` | `def gather_loot(sessions_dir)` |
| `loot_graph` | method | `cli/ops_commands.py:846` | `def loot_graph(sessions_dir)` |
| `loot_mark` | method | `cli/ops_commands.py:944` | `def loot_mark(selector, outcome, host, sessions_dir)` |
| `loot_reuse` | method | `cli/ops_commands.py:762` | `def loot_reuse(rhost, sessions_dir)` |
| `loot_search` | method | `cli/ops_commands.py:685` | `def loot_search(query, sessions_dir)` |
| `loot_show` | method | `cli/ops_commands.py:613` | `def loot_show(sessions_dir)` |
| `note_add` | function | `cli/ops_commands.py:467` | `def note_add(text, rhost, phase)` |
| `note_list` | function | `cli/ops_commands.py:492` | `def note_list(rhost, limit)` |
| `phase_progress` | function | `cli/ops_commands.py:392` | `def phase_progress(world, sessions_dir)` |
| `pivot_add` | method | `cli/ops_commands.py:986` | `def pivot_add(new_ip, via_ip, note)` |
| `pivot_list` | method | `cli/ops_commands.py:1012` | `def pivot_list()` |
| `print_ctx` | function | `cli/ops_commands.py:74` | `def print_ctx(payload, sessions_dir)` |
| `print_phase` | function | `cli/ops_commands.py:317` | `def print_phase()` |
| `read_phase` | function | `cli/ops_commands.py:279` | `def read_phase()` |
| `resolve_cred_value` | method | `cli/ops_commands.py:916` | `def resolve_cred_value(selector, entries)` |
| `scans_list` | method | `cli/ops_commands.py:1188` | `def scans_list(rhost, sessions_dir)` |
| `sitrep` | method | `cli/ops_commands.py:1241` | `def sitrep(payload, sessions_dir)` |
| `tasks_add` | method | `cli/ops_commands.py:1124` | `def tasks_add(title, operator)` |
| `tasks_done` | method | `cli/ops_commands.py:1145` | `def tasks_done(task_id)` |
| `tasks_list` | method | `cli/ops_commands.py:1069` | `def tasks_list(status_filter, limit)` |
| `tasks_start` | method | `cli/ops_commands.py:1165` | `def tasks_start(task_id)` |
| `tgrep` | function | `cli/ops_commands.py:115` | `def tgrep(pattern)` |
| `value` | method | `cli/ops_commands.py:560` | `def value(self)` |
| `write_phase` | function | `cli/ops_commands.py:302` | `def write_phase(phase)` |
| `OutputMode` | class | `cli/output_mode.py:33` | `class OutputMode` |
| `OutputModeConfig` | class | `cli/output_mode.py:20` | `class OutputModeConfig` |
| `dry_run_line` | method | `cli/output_mode.py:98` | `def dry_run_line(command)` |
| `format_output` | method | `cli/output_mode.py:77` | `def format_output(data, mode)` |
| `parse_output_flags` | method | `cli/output_mode.py:43` | `def parse_output_flags(args, config)` |
| `strip_ansi` | method | `cli/output_mode.py:65` | `def strip_ansi(text)` |
| `CommandIndexError` | class | `cli/palette.py:25` | `class CommandIndexError(RuntimeError)` |
| `all_categories` | method | `cli/palette.py:77` | `def all_categories()` |
| `all_commands` | method | `cli/palette.py:55` | `def all_commands()` |
| `all_phases` | method | `cli/palette.py:72` | `def all_phases()` |
| `duplicates` | method | `cli/palette.py:125` | `def duplicates()` |
| `filter_by_category` | method | `cli/palette.py:92` | `def filter_by_category(category)` |
| `filter_by_phase` | method | `cli/palette.py:82` | `def filter_by_phase(phase)` |
| `get` | method | `cli/palette.py:114` | `def get(name)` |
| `load_index` | method | `cli/palette.py:30` | `def load_index(path)` |
| `search` | method | `cli/palette.py:97` | `def search(query)` |
| `totals` | method | `cli/palette.py:130` | `def totals()` |
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
| `_enrich_commands_for_view` | method | `cli/palette_command.py:665` | `def _enrich_commands_for_view(rows)` |
| `_enrich_detail_entry` | method | `cli/palette_command.py:409` | `def _enrich_detail_entry(entry)` |
| `_ensure_neighbour_keys` | method | `cli/palette_command.py:689` | `def _ensure_neighbour_keys(rows)` |
| `_filter_phase_rows` | method | `cli/palette_command.py:395` | `def _filter_phase_rows(rows, query)` |
| `_filter_prefix` | method | `cli/palette_command.py:797` | `def _filter_prefix(candidates, text)` |
| `_format_name_summary_table` | method | `cli/palette_command.py:383` | `def _format_name_summary_table(self, header, rows)` |
| `_format_neighbours` | method | `cli/palette_command.py:370` | `def _format_neighbours(self, values)` |
| `_load_recent_commands` | method | `cli/palette_command.py:712` | `def _load_recent_commands()` |
| `_ordered_phase_ids` | method | `cli/palette_command.py:728` | `def _ordered_phase_ids(config, phase_counts)` |
| `_ordered_phases` | method | `cli/palette_command.py:376` | `def _ordered_phases(self, phase_counts)` |
| `_tokenise` | method | `cli/palette_command.py:784` | `def _tokenise(self, line, endidx)` |
| `build_palette_view` | method | `cli/palette_command.py:619` | `def build_palette_view(index)` |
| `commands` | method | `cli/palette_command.py:197` | `def commands(self)` |
| `complete` | method | `cli/palette_command.py:758` | `def complete(self, text, line, endidx, index)` |
| `detail` | method | `cli/palette_command.py:234` | `def detail(self, target)` |
| `in_phase` | method | `cli/palette_command.py:213` | `def in_phase(self, phase)` |
| `next_phase` | method | `cli/palette_command.py:249` | `def next_phase(self, current)` |
| `parse` | method | `cli/palette_command.py:152` | `def parse(self, line)` |
| `phase_counts` | method | `cli/palette_command.py:208` | `def phase_counts(self)` |
| `phases` | method | `cli/palette_command.py:203` | `def phases(self)` |
| `render` | method | `cli/palette_command.py:447` | `def render(index, line)` |
| `render_detail` | method | `cli/palette_command.py:320` | `def render_detail(self, entry)` |
| `render_detail` | method | `cli/palette_command.py:549` | `def render_detail(self, target, entry)` |
| `render_json` | method | `cli/palette_command.py:566` | `def render_json(index, line)` |
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

Next: [SYMBOLS_p5.md](SYMBOLS_p5.md)
