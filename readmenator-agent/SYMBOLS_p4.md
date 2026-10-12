# Symbols (page 4 of 40)
Previous: [SYMBOLS_p3.md](SYMBOLS_p3.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `ConfigHistory` | class | `cli/config_history.py:23` | `class ConfigHistory` |
| `ConfigHistoryConfig` | class | `cli/config_history.py:16` | `class ConfigHistoryConfig` |
| `capture_baseline` | method | `cli/config_history.py:30` | `def capture_baseline(self, state)` |
| `depth` | method | `cli/config_history.py:76` | `def depth(self)` |
| `diff` | method | `cli/config_history.py:58` | `def diff(self, current)` |
| `get_shell_history` | function | `cli/config_history.py:81` | `def get_shell_history(shell)` |
| `push` | method | `cli/config_history.py:38` | `def push(self, state)` |
| `track_before` | function | `cli/config_history.py:104` | `def track_before(history, state)` |
| `undo` | method | `cli/config_history.py:48` | `def undo(self)` |
| `ConfigStatus` | class | `cli/config_status.py:62` | `class ConfigStatus` |
| `ConfigStatusConfig` | class | `cli/config_status.py:55` | `class ConfigStatusConfig` |
| `__init__` | method | `cli/config_status.py:70` | `def __init__(self, params, config)` |
| `_field_status` | method | `cli/config_status.py:78` | `def _field_status(self, key, value)` |
| `render_quick_check` | method | `cli/config_status.py:129` | `def render_quick_check(self)` |
| `render_status` | method | `cli/config_status.py:89` | `def render_status(self)` |
| `_read_line` | function | `cli/confirm.py:20` | `def _read_line(prompt)` |
| `confirm` | function | `cli/confirm.py:27` | `def confirm(question, default, yes_values)` |
| `CommandInfo` | class | `cli/contextual_help.py:62` | `class CommandInfo` |
| `ContextualHelp` | class | `cli/contextual_help.py:167` | `class ContextualHelp` |
| `ContextualHelpConfig` | class | `cli/contextual_help.py:78` | `class ContextualHelpConfig` |
| `__init__` | method | `cli/contextual_help.py:176` | `def __init__(self, aliases, params, config)` |
| `_build_command_lookup` | function | `cli/contextual_help.py:97` | `def _build_command_lookup(index)` |
| `_load_command_index` | function | `cli/contextual_help.py:85` | `def _load_command_index(path)` |
| `get_command_info` | method | `cli/contextual_help.py:188` | `def get_command_info(self, name)` |
| `render_command_help` | method | `cli/contextual_help.py:208` | `def render_command_help(self, name)` |
| `render_phase_commands` | method | `cli/contextual_help.py:261` | `def render_phase_commands(self, phase)` |
| `render_requirements_status` | method | `cli/contextual_help.py:281` | `def render_requirements_status(self)` |
| `DashboardLayoutConfig` | class | `cli/dashboard_layout.py:14` | `class DashboardLayoutConfig` |
| `hidden_panels` | function | `cli/dashboard_layout.py:45` | `def hidden_panels(mode)` |
| `layout_mode` | function | `cli/dashboard_layout.py:28` | `def layout_mode(width, config)` |
| `CommandRequested` | class | `cli/dashboard_tui.py:97` | `class CommandRequested(Message)` |
| `CommandsPanel` | class | `cli/dashboard_tui.py:460` | `class CommandsPanel(Static)` |
| `ConfigPanel` | class | `cli/dashboard_tui.py:430` | `class ConfigPanel(Static)` |
| `HintBar` | class | `cli/dashboard_tui.py:587` | `class HintBar(Horizontal)` |
| `KillChainPanel` | class | `cli/dashboard_tui.py:378` | `class KillChainPanel(Static)` |
| `LazyOwnDashboard` | class | `cli/dashboard_tui.py:738` | `class LazyOwnDashboard(App)` |
| `NextStepsPanel` | class | `cli/dashboard_tui.py:706` | `class NextStepsPanel(Static)` |
| `OpsPanel` | class | `cli/dashboard_tui.py:532` | `class OpsPanel(Static)` |
| `OutputPanel` | class | `cli/dashboard_tui.py:693` | `class OutputPanel(Log)` |
| `PhaseSelected` | class | `cli/dashboard_tui.py:105` | `class PhaseSelected(Message)` |
| `ReasoningPanel` | class | `cli/dashboard_tui.py:495` | `class ReasoningPanel(Static)` |
| `TargetPanel` | class | `cli/dashboard_tui.py:322` | `class TargetPanel(Static)` |
| `ToastPanel` | class | `cli/dashboard_tui.py:653` | `class ToastPanel(Static)` |
| `__init__` | method | `cli/dashboard_tui.py:100` | `def __init__(self, command)` |
| `__init__` | method | `cli/dashboard_tui.py:108` | `def __init__(self, phase)` |
| `__init__` | method | `cli/dashboard_tui.py:393` | `def __init__(self)` |
| `__init__` | method | `cli/dashboard_tui.py:610` | `def __init__(self)` |
| `__init__` | method | `cli/dashboard_tui.py:807` | `def __init__(self, payload_path, sessions_dir)` |
| `_apply_command_result` | method | `cli/dashboard_tui.py:894` | `def _apply_command_result(self, command, success, output)` |
| `_apply_layout` | method | `cli/dashboard_tui.py:819` | `def _apply_layout(self, mode, hidden_fn)` |
| `_beacon_count` | function | `cli/dashboard_tui.py:265` | `def _beacon_count()` |
| `_count_lines_in_glob` | function | `cli/dashboard_tui.py:169` | `def _count_lines_in_glob(pattern)` |
| `_cycle_phase` | method | `cli/dashboard_tui.py:995` | `def _cycle_phase(self, direction)` |
| `_do_refresh` | method | `cli/dashboard_tui.py:1011` | `def _do_refresh(self)` |
| `_engagement_to_cli_phase` | function | `cli/dashboard_tui.py:159` | `def _engagement_to_cli_phase(engagement_phase)` |
| `_execute` | method | `cli/dashboard_tui.py:881` | `def _execute(self, command)` |
| `_fallback_hints` | function | `cli/dashboard_tui.py:223` | `def _fallback_hints(last_command, limit)` |
| `_filter_commands` | method | `cli/dashboard_tui.py:1048` | `def _filter_commands(self, commands)` |
| `_get_killchain_for_tui` | function | `cli/dashboard_tui.py:55` | `def _get_killchain_for_tui()` |
| `_get_recommendations` | function | `cli/dashboard_tui.py:297` | `def _get_recommendations()` |
| `_graph_hints` | function | `cli/dashboard_tui.py:209` | `def _graph_hints(limit)` |
| `_raise_toast` | method | `cli/dashboard_tui.py:938` | `def _raise_toast(self, message, severity, event_type)` |
| `_read_credential_lines` | function | `cli/dashboard_tui.py:280` | `def _read_credential_lines(pattern)` |
| `_read_json` | function | `cli/dashboard_tui.py:151` | `def _read_json(path)` |
| `_read_recent_commands` | function | `cli/dashboard_tui.py:182` | `def _read_recent_commands(limit)` |
| `_resolve_hints` | function | `cli/dashboard_tui.py:248` | `def _resolve_hints(recent, limit)` |
| `_write_phase` | function | `cli/dashboard_tui.py:43` | `def _write_phase(phase)` |
| `action_export_snapshot` | method | `cli/dashboard_tui.py:967` | `def action_export_snapshot(self)` |
| `action_next_phase` | method | `cli/dashboard_tui.py:987` | `def action_next_phase(self)` |
| `action_prev_phase` | method | `cli/dashboard_tui.py:991` | `def action_prev_phase(self)` |
| `action_refresh_data` | method | `cli/dashboard_tui.py:923` | `def action_refresh_data(self)` |
| `action_screenshot` | method | `cli/dashboard_tui.py:956` | `def action_screenshot(self)` |
| `action_toggle_compact` | method | `cli/dashboard_tui.py:926` | `def action_toggle_compact(self)` |
| `compose` | method | `cli/dashboard_tui.py:615` | `def compose(self)` |
| `compose` | method | `cli/dashboard_tui.py:836` | `def compose(self)` |
| `dispatch_command` | function | `cli/dashboard_tui.py:113` | `def dispatch_command(command, timeout)` |
| `get_selection` | method | `cli/dashboard_tui.py:335` | `def get_selection(self, selection)` |
| `launch` | function | `cli/dashboard_tui.py:1064` | `def launch(payload_path, sessions_dir)` |
| `on_button_pressed` | method | `cli/dashboard_tui.py:644` | `def on_button_pressed(self, event)` |
| `on_click` | method | `cli/dashboard_tui.py:418` | `def on_click(self, event)` |
| `on_command_requested` | method | `cli/dashboard_tui.py:872` | `def on_command_requested(self, event)` |
| `on_input_submitted` | method | `cli/dashboard_tui.py:860` | `def on_input_submitted(self, event)` |
| `on_mount` | method | `cli/dashboard_tui.py:855` | `def on_mount(self)` |
| `on_phase_selected` | method | `cli/dashboard_tui.py:912` | `def on_phase_selected(self, event)` |
| `render_content` | method | `cli/dashboard_tui.py:348` | `def render_content(self, payload, world)` |
| `update_data` | method | `cli/dashboard_tui.py:374` | `def update_data(self, payload, world)` |
| `update_data` | method | `cli/dashboard_tui.py:397` | `def update_data(self, progress)` |
| `update_data` | method | `cli/dashboard_tui.py:442` | `def update_data(self, payload)` |
| `update_data` | method | `cli/dashboard_tui.py:472` | `def update_data(self, commands)` |
| `update_data` | method | `cli/dashboard_tui.py:507` | `def update_data(self, entries)` |
| `update_data` | method | `cli/dashboard_tui.py:544` | `def update_data(self, world, tasks, creds, hashes, beacons, cred_lines)` |
| `update_data` | method | `cli/dashboard_tui.py:619` | `def update_data(self, hints)` |
| `update_data` | method | `cli/dashboard_tui.py:671` | `def update_data(self, payload, sessions_dir, width)` |
| `update_data` | method | `cli/dashboard_tui.py:718` | `def update_data(self, recommendations)` |
| `CheckResult` | class | `cli/doctor.py:96` | `class CheckResult` |
| `DoctorReport` | class | `cli/doctor.py:113` | `class DoctorReport` |
| `PackageSpec` | class | `cli/doctor.py:56` | `class PackageSpec` |
| `_apply_fix` | function | `cli/doctor.py:525` | `def _apply_fix(check, root, venv_pip, console)` |
| `_status_cell` | function | `cli/doctor.py:398` | `def _status_cell(status)` |
| `check_certificates` | function | `cli/doctor.py:248` | `def check_certificates(root)` |
| `check_command_index` | function | `cli/doctor.py:313` | `def check_command_index(root)` |
| `check_external_tools` | function | `cli/doctor.py:343` | `def check_external_tools(checker)` |
| `check_packages` | function | `cli/doctor.py:209` | `def check_packages(specs, finder)` |
| `check_payload` | function | `cli/doctor.py:269` | `def check_payload(root)` |
| `check_python_version` | function | `cli/doctor.py:143` | `def check_python_version(version_info)` |
| `check_seclists` | function | `cli/doctor.py:289` | `def check_seclists(finder)` |
| `check_virtualenv` | function | `cli/doctor.py:172` | `def check_virtualenv()` |
| `failures` | method | `cli/doctor.py:119` | `def failures(self)` |
| `fix_report` | function | `cli/doctor.py:468` | `def fix_report(report)` |
| `gather_report` | function | `cli/doctor.py:368` | `def gather_report(root)` |
| `healthy` | method | `cli/doctor.py:129` | `def healthy(self)` |
| `overall_status` | method | `cli/doctor.py:134` | `def overall_status(self)` |
| `render_report` | function | `cli/doctor.py:406` | `def render_report(report, console)` |
| `run` | function | `cli/doctor.py:451` | `def run(root, console)` |
| `warnings` | method | `cli/doctor.py:124` | `def warnings(self)` |
| `EngagementState` | class | `cli/engagement_hooks.py:242` | `class EngagementState` |
| `_award_elo` | function | `cli/engagement_hooks.py:734` | `def _award_elo(cmd, first_time, new_phase, current_phase)` |
| `_check_badges` | function | `cli/engagement_hooks.py:1009` | `def _check_badges(cmd, first_time)` |
| `_check_karma_up` | function | `cli/engagement_hooks.py:864` | `def _check_karma_up(state)` |
| `_commands_in_phase` | function | `cli/engagement_hooks.py:409` | `def _commands_in_phase(phase, index)` |
| `_fire_vri_reward` | function | `cli/engagement_hooks.py:672` | `def _fire_vri_reward(state, ctx)` |
| `_is_recordable_command` | function | `cli/engagement_hooks.py:306` | `def _is_recordable_command(cmd)` |
| `_load_index` | function | `cli/engagement_hooks.py:290` | `def _load_index()` |
| `_load_state` | function | `cli/engagement_hooks.py:260` | `def _load_state()` |
| `_next_threshold` | function | `cli/engagement_hooks.py:394` | `def _next_threshold(current)` |
| `_normalize_command` | function | `cli/engagement_hooks.py:301` | `def _normalize_command(cmd)` |
| `_persist_notification` | function | `cli/engagement_hooks.py:828` | `def _persist_notification(html)` |
| `_phase_for_cmd` | function | `cli/engagement_hooks.py:400` | `def _phase_for_cmd(cmd, index)` |
| `_print_badge` | function | `cli/engagement_hooks.py:1056` | `def _print_badge(name, description)` |
| `_render_arsenal_tip` | function | `cli/engagement_hooks.py:536` | `def _render_arsenal_tip(ctx)` |
| `_render_exploration` | function | `cli/engagement_hooks.py:488` | `def _render_exploration(ctx)` |
| `_render_hidden_feature` | function | `cli/engagement_hooks.py:522` | `def _render_hidden_feature(ctx)` |
| `_render_methodology_note` | function | `cli/engagement_hooks.py:630` | `def _render_methodology_note(ctx)` |
| `_render_methodology_objective` | function | `cli/engagement_hooks.py:583` | `def _render_methodology_objective(ctx)` |
| `_render_methodology_task` | function | `cli/engagement_hooks.py:544` | `def _render_methodology_task(ctx)` |
| `_render_phase_badge` | function | `cli/engagement_hooks.py:506` | `def _render_phase_badge(ctx)` |
| `_render_streak` | function | `cli/engagement_hooks.py:459` | `def _render_streak(ctx)` |
| `_run_curiosity` | function | `cli/engagement_hooks.py:431` | `def _run_curiosity(cmd, state, index)` |
| `_sanitize_seen` | function | `cli/engagement_hooks.py:332` | `def _sanitize_seen(names, known)` |
| `_save_state` | function | `cli/engagement_hooks.py:280` | `def _save_state(state)` |
| `_summary_for_cmd` | function | `cli/engagement_hooks.py:414` | `def _summary_for_cmd(cmd, index)` |
| `_sync_user_elo` | function | `cli/engagement_hooks.py:760` | `def _sync_user_elo(delta)` |
| `get_karma_name` | function | `cli/engagement_hooks.py:716` | `def get_karma_name(elo)` |
| `get_state_snapshot` | function | `cli/engagement_hooks.py:978` | `def get_state_snapshot()` |
| `heal_commands_seen` | function | `cli/engagement_hooks.py:365` | `def heal_commands_seen(known)` |
| `render_engagement_hook` | function | `cli/engagement_hooks.py:898` | `def render_engagement_hook(cmd, phase, enabled)` |
| `reset_session` | function | `cli/engagement_hooks.py:1066` | `def reset_session()` |
| `ExploitHit` | class | `cli/exploit_advisor.py:144` | `class ExploitHit` |
| `ServiceInfo` | class | `cli/exploit_advisor.py:111` | `class ServiceInfo` |
| `ServiceResult` | class | `cli/exploit_advisor.py:153` | `class ServiceResult` |
| `display_name` | method | `cli/exploit_advisor.py:128` | `def display_name(self)` |
| `find_nmap_xml` | function | `cli/exploit_advisor.py:203` | `def find_nmap_xml(rhost, sessions_dir)` |
| `inject_exploit_tasks` | function | `cli/exploit_advisor.py:338` | `def inject_exploit_tasks(results, rhost, tasks_path)` |
| `next_commands` | method | `cli/exploit_advisor.py:132` | `def next_commands(self)` |
| `parse_nmap_xml` | function | `cli/exploit_advisor.py:164` | `def parse_nmap_xml(path)` |
| `print_exploit_summary` | function | `cli/exploit_advisor.py:222` | `def print_exploit_summary(results, rhost)` |
| `save_ss_results` | function | `cli/exploit_advisor.py:296` | `def save_ss_results(results, rhost, sessions_dir)` |
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
| `normalise_os` | function | `cli/exploration.py:677` | `def normalise_os(value, default)` |
| `normalise_trigger` | function | `cli/exploration.py:690` | `def normalise_trigger(value)` |
| `resolve_current_os` | function | `cli/exploration.py:656` | `def resolve_current_os(payload)` |
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
| `did_you_mean` | function | `cli/fuzzy_match.py:56` | `def did_you_mean(query, candidates)` |
| `suggest` | function | `cli/fuzzy_match.py:28` | `def suggest(query, candidates, limit, config)` |
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
| `install_fuzzy_completion` | function | `cli/fuzzy_picker.py:645` | `def install_fuzzy_completion(shell, payload, config)` |
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
| `run_chain` | method | `cli/headless.py:132` | `def run_chain(self, commands)` |
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
| `ConfigField` | class | `cli/lazy_orchestrator.py:59` | `class ConfigField` |
| `FormModal` | class | `cli/lazy_orchestrator.py:81` | `class FormModal` |
| `LazyOrchestratorApp` | class | `cli/lazy_orchestrator.py:118` | `class LazyOrchestratorApp` |
| `__init__` | method | `cli/lazy_orchestrator.py:86` | `def __init__(self, title, fields)` |
| `__init__` | method | `cli/lazy_orchestrator.py:141` | `def __init__(self, payload_path, task_id)` |
| `_active_tab` | method | `cli/lazy_orchestrator.py:495` | `def _active_tab(self)` |
| `_coerce` | function | `cli/lazy_orchestrator.py:588` | `def _coerce(raw)` |
| `_done` | function | `cli/lazy_orchestrator.py:507` | `def _done(values)` |
| `_done_rule` | function | `cli/lazy_orchestrator.py:524` | `def _done_rule(values)` |
| `_done_verb` | function | `cli/lazy_orchestrator.py:541` | `def _done_verb(values)` |
| `_load_payload` | method | `cli/lazy_orchestrator.py:267` | `def _load_payload(self)` |
| `_load_payload_into_form` | method | `cli/lazy_orchestrator.py:277` | `def _load_payload_into_form(self)` |
| `_poll_now` | method | `cli/lazy_orchestrator.py:403` | `def _poll_now(self)` |
| `_refresh_guard` | method | `cli/lazy_orchestrator.py:363` | `def _refresh_guard(self)` |
| `_refresh_models` | method | `cli/lazy_orchestrator.py:342` | `def _refresh_models(self)` |
| `_refresh_stages` | method | `cli/lazy_orchestrator.py:227` | `def _refresh_stages(self)` |
| `_refresh_verbs` | method | `cli/lazy_orchestrator.py:243` | `def _refresh_verbs(self)` |
| `_resolve_task` | method | `cli/lazy_orchestrator.py:385` | `def _resolve_task(self)` |
| `_selected_row` | method | `cli/lazy_orchestrator.py:464` | `def _selected_row(self, table_id)` |
| `action_add_item` | method | `cli/lazy_orchestrator.py:502` | `def action_add_item(self)` |
| `action_delete_item` | method | `cli/lazy_orchestrator.py:563` | `def action_delete_item(self)` |
| `action_refresh` | method | `cli/lazy_orchestrator.py:456` | `def action_refresh(self)` |
| `action_save_config` | method | `cli/lazy_orchestrator.py:485` | `def action_save_config(self)` |
| `action_toggle_item` | method | `cli/lazy_orchestrator.py:473` | `def action_toggle_item(self)` |
| `add_auto_verb` | method | `cli/lazy_orchestrator.py:204` | `def add_auto_verb(self, name, keywords, needs_target, description)` |
| `add_guard_rule` | method | `cli/lazy_orchestrator.py:326` | `def add_guard_rule(self, pattern, action, reason)` |
| `add_model_member` | method | `cli/lazy_orchestrator.py:310` | `def add_model_member(self, name, model, priority)` |
| `compose` | method | `cli/lazy_orchestrator.py:92` | `def compose(self)` |
| `compose` | method | `cli/lazy_orchestrator.py:151` | `def compose(self)` |
| `on_button_pressed` | method | `cli/lazy_orchestrator.py:101` | `def on_button_pressed(self, event)` |
| `on_button_pressed` | method | `cli/lazy_orchestrator.py:438` | `def on_button_pressed(self, event)` |
| `on_input_submitted` | method | `cli/lazy_orchestrator.py:110` | `def on_input_submitted(self, event)` |
| `on_mount` | method | `cli/lazy_orchestrator.py:176` | `def on_mount(self)` |
| `remove_auto_verb` | method | `cli/lazy_orchestrator.py:219` | `def remove_auto_verb(self, name)` |
| `remove_guard_rule` | method | `cli/lazy_orchestrator.py:334` | `def remove_guard_rule(self, pattern)` |
| `remove_model_member` | method | `cli/lazy_orchestrator.py:318` | `def remove_model_member(self, name)` |
| `run_orchestrator_console` | function | `cli/lazy_orchestrator.py:605` | `def run_orchestrator_console(task_id)` |
| `save_config` | method | `cli/lazy_orchestrator.py:288` | `def save_config(self, values)` |
| `toggle_stage` | method | `cli/lazy_orchestrator.py:186` | `def toggle_stage(self, name)` |
| `toggle_verb` | method | `cli/lazy_orchestrator.py:195` | `def toggle_verb(self, name)` |
| `PostScanConfig` | class | `cli/lazynmap_post.py:57` | `class PostScanConfig` |
| `PostScanResult` | class | `cli/lazynmap_post.py:76` | `class PostScanResult` |
| `_atomic_write_json` | function | `cli/lazynmap_post.py:263` | `def _atomic_write_json(path, data, mode)` |
| `_default_engine_factory` | function | `cli/lazynmap_post.py:180` | `def _default_engine_factory(payload, cfg)` |
| `_emit_event` | function | `cli/lazynmap_post.py:213` | `def _emit_event(cfg, target, plan, plan_path, clock_fn)` |
| `_enabled` | function | `cli/lazynmap_post.py:164` | `def _enabled(payload, cfg)` |
| `_safe_log` | function | `cli/lazynmap_post.py:291` | `def _safe_log(console, message)` |
| `_update_world_model_phase` | function | `cli/lazynmap_post.py:188` | `def _update_world_model_phase(cfg, target, clock_fn)` |
| `run_post_scan` | function | `cli/lazynmap_post.py:94` | `def run_post_scan(target, payload, console, config, engine_factory, plan_config, clock)` |
| `AddonInfo` | class | `cli/marketplace_config.py:131` | `class AddonInfo` |
| `AddonRegistry` | class | `cli/marketplace_config.py:197` | `class AddonRegistry` |
| `MarketplaceConfig` | class | `cli/marketplace_config.py:56` | `class MarketplaceConfig` |
| `MarketplaceConfigurator` | class | `cli/marketplace_config.py:378` | `class MarketplaceConfigurator` |
| `MarketplaceSettings` | class | `cli/marketplace_config.py:349` | `class MarketplaceSettings` |
| `__init__` | method | `cli/marketplace_config.py:220` | `def __init__(self)` |
| `__init__` | method | `cli/marketplace_config.py:381` | `def __init__(self, config, registry, initial)` |
| `_build_initial_settings` | function | `cli/marketplace_config.py:774` | `def _build_initial_settings(registry)` |
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
| `configure_marketplace_interactive` | function | `cli/marketplace_config.py:751` | `def configure_marketplace_interactive(config, start_tab)` |
| `disable_all` | method | `cli/marketplace_config.py:372` | `def disable_all(self, addons)` |
| `enable_all` | method | `cli/marketplace_config.py:367` | `def enable_all(self, addons)` |
| `from_yaml` | method | `cli/marketplace_config.py:144` | `def from_yaml(cls, path)` |
| `is_enabled` | method | `cli/marketplace_config.py:354` | `def is_enabled(self, kind, name)` |
| `marketplace_summary` | function | `cli/marketplace_config.py:784` | `def marketplace_summary(registry)` |
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
| `LootEntry` | class | `cli/ops_commands.py:545` | `class LootEntry` |
| `_bucket` | function | `cli/ops_commands.py:861` | `def _bucket(node)` |
| `_cli_phase_to_host_state` | function | `cli/ops_commands.py:297` | `def _cli_phase_to_host_state(phase)` |
| `_count_glob` | function | `cli/ops_commands.py:450` | `def _count_glob(pattern)` |
| `_count_pivots` | function | `cli/ops_commands.py:385` | `def _count_pivots(sessions_dir)` |
| `_cred_node` | function | `cli/ops_commands.py:758` | `def _cred_node(value)` |
| `_cred_outcomes_for_host` | function | `cli/ops_commands.py:731` | `def _cred_outcomes_for_host(world, host)` |
| `_engagement_phase_to_cli` | function | `cli/ops_commands.py:292` | `def _engagement_phase_to_cli(phase_value)` |

Next: [SYMBOLS_p5.md](SYMBOLS_p5.md)
