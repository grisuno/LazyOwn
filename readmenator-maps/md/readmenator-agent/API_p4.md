# API (page 4 of 24)
Previous: [API_p3.md](API_p3.md)

## cli/dashboard_tui.py
Depends on: `cli/commands/containers.py`, `cli/dashboard_layout.py`, `cli/graph_advisor.py`, `cli/killchain.py`, `cli/ops_commands.py`, `cli/reactive_hints.py`, `cli/reasoning_stream.py`, `cli/recommendation_signals.py`, `cli/toast_bus.py`, `modules/killchain.py`, `modules/world_model.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_dashboard_tui.py`
- `CommandRequested.__init__` (method) `cli/dashboard_tui.py:100` `def __init__(self, command)`
- `PhaseSelected.__init__` (method) `cli/dashboard_tui.py:108` `def __init__(self, phase)`
- `dispatch_command` (function) `cli/dashboard_tui.py:113` `def dispatch_command(command, timeout)` -- Run one LazyOwn command headlessly and capture its output.
- `TargetPanel.get_selection` (method) `cli/dashboard_tui.py:337` `def get_selection(self, selection)` -- Override to prevent IndexError when selection offsets exceed text length.
- `TargetPanel.render_content` (method) `cli/dashboard_tui.py:350` `def render_content(self, payload, world)`
- `TargetPanel.update_data` (method) `cli/dashboard_tui.py:376` `def update_data(self, payload, world)`
- `KillChainPanel.__init__` (method) `cli/dashboard_tui.py:395` `def __init__(self)`
- `KillChainPanel.update_data` (method) `cli/dashboard_tui.py:399` `def update_data(self, progress)` -- Render kill-chain progress.
- `KillChainPanel.on_click` (method) `cli/dashboard_tui.py:420` `def on_click(self, event)` -- Select the phase whose row was clicked.
- `ConfigPanel.update_data` (method) `cli/dashboard_tui.py:444` `def update_data(self, payload)`
- `CommandsPanel.update_data` (method) `cli/dashboard_tui.py:474` `def update_data(self, commands)`
- `ReasoningPanel.update_data` (method) `cli/dashboard_tui.py:509` `def update_data(self, entries)` -- Render the most recent daemon decisions, newest first.
- `OpsPanel.update_data` (method) `cli/dashboard_tui.py:546` `def update_data(self, world, tasks, creds, hashes, beacons, cred_lines)`
- `HintBar.__init__` (method) `cli/dashboard_tui.py:612` `def __init__(self)`
- `HintBar.compose` (method) `cli/dashboard_tui.py:617` `def compose(self)`
- `HintBar.update_data` (method) `cli/dashboard_tui.py:621` `def update_data(self, hints)` -- Replace the hint buttons with one button per suggestion.
- `HintBar.on_button_pressed` (method) `cli/dashboard_tui.py:646` `def on_button_pressed(self, event)` -- Run the clicked suggestion as if it had been typed.
- `ToastPanel.update_data` (method) `cli/dashboard_tui.py:673` `def update_data(self, payload, sessions_dir, width)` -- Render the latest notifications for the active theme.
- `NextStepsPanel.update_data` (method) `cli/dashboard_tui.py:720` `def update_data(self, recommendations)`
- `LazyOwnDashboard.__init__` (method) `cli/dashboard_tui.py:809` `def __init__(self, payload_path, sessions_dir)`
- `LazyOwnDashboard.compose` (method) `cli/dashboard_tui.py:838` `def compose(self)`
- `LazyOwnDashboard.on_mount` (method) `cli/dashboard_tui.py:857` `def on_mount(self)`
- `LazyOwnDashboard.on_input_submitted` (method) `cli/dashboard_tui.py:862` `def on_input_submitted(self, event)` -- Run the typed command and clear the input.
- `LazyOwnDashboard.on_command_requested` (method) `cli/dashboard_tui.py:874` `def on_command_requested(self, event)` -- Dispatch a command in a worker so the UI never blocks.
- `LazyOwnDashboard.on_phase_selected` (method) `cli/dashboard_tui.py:914` `def on_phase_selected(self, event)` -- Filter the center panel to a phase chosen by clicking the kill chain.
- `LazyOwnDashboard.action_refresh_data` (method) `cli/dashboard_tui.py:925` `def action_refresh_data(self)`
- `LazyOwnDashboard.action_toggle_compact` (method) `cli/dashboard_tui.py:928` `def action_toggle_compact(self)` -- Toggle the compact single-column layout for narrow terminals.
- `LazyOwnDashboard.action_screenshot` (method) `cli/dashboard_tui.py:958` `def action_screenshot(self)` -- Save an SVG screenshot next to the sessions directory.
- `LazyOwnDashboard.action_export_snapshot` (method) `cli/dashboard_tui.py:969` `def action_export_snapshot(self)` -- Export the current dashboard data as JSON for automation.
- `LazyOwnDashboard.action_next_phase` (method) `cli/dashboard_tui.py:989` `def action_next_phase(self)` -- Advance to the next kill-chain phase and refresh the display.
- `LazyOwnDashboard.action_prev_phase` (method) `cli/dashboard_tui.py:993` `def action_prev_phase(self)` -- Step back to the previous kill-chain phase.
- `launch` (function) `cli/dashboard_tui.py:1066` `def launch(payload_path, sessions_dir)` -- Launch the dashboard and block until the user quits.

## cli/doctor.py
Depends on: `cli/wizard.py`, `core/console.py`, `core/profiles.py`
Imported by: `cli/commands/help_ui.py`
- `DoctorReport.failures` (method) `cli/doctor.py:119` `def failures(self)` -- Return the checks whose status is :data:`STATUS_FAIL`.
- `DoctorReport.warnings` (method) `cli/doctor.py:124` `def warnings(self)` -- Return the checks whose status is :data:`STATUS_WARN`.
- `DoctorReport.healthy` (method) `cli/doctor.py:129` `def healthy(self)` -- Return ``True`` when no check failed (warnings are tolerated).
- `DoctorReport.overall_status` (method) `cli/doctor.py:134` `def overall_status(self)` -- Return the worst status across every check.
- `check_python_version` (function) `cli/doctor.py:143` `def check_python_version(version_info)` -- Verify the interpreter satisfies :data:`MIN_PYTHON_VERSION`.
- `check_virtualenv` (function) `cli/doctor.py:172` `def check_virtualenv()` -- Report whether the framework is running inside its virtual environment.
- `check_packages` (function) `cli/doctor.py:209` `def check_packages(specs, finder)` -- Verify every dependency in ``specs`` is importable without importing it.
- `check_certificates` (function) `cli/doctor.py:248` `def check_certificates(root)` -- Verify the self-signed C2 certificate pair exists.
- `check_payload` (function) `cli/doctor.py:269` `def check_payload(root)` -- Verify ``payload.json`` exists in the repository root.
- `check_seclists` (function) `cli/doctor.py:289` `def check_seclists(finder)` -- Verify a SecLists installation is discoverable on disk.
- `check_command_index` (function) `cli/doctor.py:313` `def check_command_index(root)`
- `check_external_tools` (function) `cli/doctor.py:343` `def check_external_tools(checker)` -- Adapt :func:`cli.wizard.check_binaries` into preflight check results.
- `gather_report` (function) `cli/doctor.py:368` `def gather_report(root)` -- Run every preflight check and collect the results without printing.
- `render_report` (function) `cli/doctor.py:406` `def render_report(report, console)` -- Render a :class:`DoctorReport` as a rich table with a summary banner.
- `run` (function) `cli/doctor.py:451` `def run(root, console)` -- Gather and render the preflight report.
- `fix_report` (function) `cli/doctor.py:468` `def fix_report(report)` -- Interactively offer to fix every failure and warning in the report.

## cli/engagement_hooks.py
Depends on: `cli/palette.py`, `core/config.py`, `modules/cli_auth.py`, `modules/lazy_rbac.py`
Imported by: `cli/banner_config.py`, `cli/commands/help_ui.py`, `cli/session_hud.py`, `cli/tips_engine.py`, `lazyown.py`, `modules/cli_auth.py`, `modules/redteam_gym.py`, `tests/test_engagement_and_ping.py`, `tests/test_engagement_command_gate.py`, `tests/test_engagement_elo_and_methodology.py`
- `heal_commands_seen` (function) `cli/engagement_hooks.py:366` `def heal_commands_seen(known)` -- Purge non-command entries from persisted ``commands_seen`` in place.
- `get_karma_name` (function) `cli/engagement_hooks.py:717` `def get_karma_name(elo)` -- Return karma rank for an ELO score.
- `render_engagement_hook` (function) `cli/engagement_hooks.py:899` `def render_engagement_hook(cmd, phase, enabled)` -- Post-command hook: curiosity reveal + ELO + VRI reward when due.
- `get_state_snapshot` (function) `cli/engagement_hooks.py:979` `def get_state_snapshot()` -- Return a read-only snapshot of current engagement state for CLI display.
- `reset_session` (function) `cli/engagement_hooks.py:1067` `def reset_session()` -- Reset session counters without clearing cross-session progress.

## cli/exploit_advisor.py
Depends on: `core/console.py`
Imported by: `cli/commands/recon.py`
- `ServiceInfo.search_query` (method) `cli/exploit_advisor.py:122` `def search_query(self)` -- Best query string for searchsploit / NVD.
- `ServiceInfo.display_name` (method) `cli/exploit_advisor.py:128` `def display_name(self)`
- `ServiceInfo.next_commands` (method) `cli/exploit_advisor.py:132` `def next_commands(self)` -- Return (command, reason) pairs recommended for this service.
- `parse_nmap_xml` (function) `cli/exploit_advisor.py:164` `def parse_nmap_xml(path)` -- Extract open services from a nmap XML file.
- `find_nmap_xml` (function) `cli/exploit_advisor.py:203` `def find_nmap_xml(rhost, sessions_dir)` -- Return all nmap XML files for a given rhost, newest first.
- `print_exploit_summary` (function) `cli/exploit_advisor.py:222` `def print_exploit_summary(results, rhost)` -- Print a rich summary table of exploit search results with next-step commands.
- `save_ss_results` (function) `cli/exploit_advisor.py:296` `def save_ss_results(results, rhost, sessions_dir)` -- Save exploit search results to sessions/ss_results_<rhost>.json.
- `inject_exploit_tasks` (function) `cli/exploit_advisor.py:338` `def inject_exploit_tasks(results, rhost, tasks_path)` -- Append one task per service with significant exploit hits to tasks.json.

## cli/exploration.py
Imported by: `cli/command_chain.py`, `cli/commands/misc_migrated.py`, `cli/exploration_view.py`, `cli/lazynmap_post.py`, `cli/recommendation_signals.py`, `cli/recon_plan.py`, `lazyown.py`, `tests/test_command_chain.py`, `tests/test_exploration_and_addons.py`, `tests/test_lazynmap_post.py`, `tests/test_recon_plan.py`
- `DiscoveredService.label` (method) `cli/exploration.py:98` `def label(self)` -- Return a compact human-readable label such as ``smb:445/tcp``.
- `CoverageReport.service_coverage` (method) `cli/exploration.py:145` `def service_coverage(self)` -- Fraction of discovered services with at least one run command.
- `CoverageReport.addon_coverage` (method) `cli/exploration.py:153` `def addon_coverage(self)` -- Fraction of enabled addons that have been executed at least once.
- `CoverageReport.tool_coverage` (method) `cli/exploration.py:161` `def tool_coverage(self)` -- Fraction of active tools that have been executed at least once.
- `NmapXmlReader.__init__` (method) `cli/exploration.py:176` `def __init__(self, config)` -- Store the configuration used to locate the nmap XML directory.
- `NmapXmlReader.discover` (method) `cli/exploration.py:181` `def discover(self, target)` -- Return every open service across every nmap XML in sessions.
- `AddonCatalog.__init__` (method) `cli/exploration.py:264` `def __init__(self, config)` -- Store the configuration used to locate the addons directory.
- `AddonCatalog.load` (method) `cli/exploration.py:269` `def load(self)` -- Return every parseable addon as an :class:`AddonEntry`.
- `AddonCatalog.clear_cache` (method) `cli/exploration.py:299` `def clear_cache(cls)` -- Drop the per-process addon cache (mainly used by tests).
- `ToolCatalog.__init__` (method) `cli/exploration.py:344` `def __init__(self, config)` -- Store the configuration used to locate the tools directory.
- `ToolCatalog.load` (method) `cli/exploration.py:349` `def load(self)` -- Return every parseable ``.tool`` file as a :class:`ToolEntry`.
- `ToolCatalog.clear_cache` (method) `cli/exploration.py:379` `def clear_cache(cls)` -- Drop the per-process tool cache (mainly used by tests).
- `TriggerMatcher.__init__` (method) `cli/exploration.py:413` `def __init__(self, current_os)` -- Store the platform used to filter incompatible entries.
- `TriggerMatcher.addons_for_service` (method) `cli/exploration.py:418` `def addons_for_service(self, service, addons)` -- Return addons whose trigger and OS match the given service.
- `TriggerMatcher.tools_for_service` (method) `cli/exploration.py:435` `def tools_for_service(self, service, tools)` -- Return active tools whose trigger and OS match the service.
- `HistoryReader.__init__` (method) `cli/exploration.py:473` `def __init__(self, config)` -- Store the configuration used to locate the transcript file.
- `HistoryReader.executed_commands` (method) `cli/exploration.py:478` `def executed_commands(self)` -- Return the set of unique tool/command names already run.
- `ExplorationEngine.__init__` (method) `cli/exploration.py:510` `def __init__(self, config, current_os)` -- Wire collaborators together using the supplied configuration.
- `ExplorationEngine.services` (method) `cli/exploration.py:525` `def services(self, target)` -- Return the discovered services for the engagement.
- `ExplorationEngine.addons` (method) `cli/exploration.py:530` `def addons(self)` -- Return the parsed lazyaddon catalogue.
- `ExplorationEngine.tools` (method) `cli/exploration.py:535` `def tools(self)` -- Return the parsed ``.tool`` catalogue.
- `ExplorationEngine.history` (method) `cli/exploration.py:540` `def history(self)` -- Return the set of already-executed command names.
- `ExplorationEngine.suggestions_for_target` (method) `cli/exploration.py:545` `def suggestions_for_target(self, target)` -- Group matching addons and tools by service for a target.
- `ExplorationEngine.unexplored_addons` (method) `cli/exploration.py:568` `def unexplored_addons(self, target)` -- Return addons triggered by the scan that have never been run.
- `ExplorationEngine.unexplored_tools` (method) `cli/exploration.py:589` `def unexplored_tools(self, target)` -- Return tools triggered by the scan that have never been run.
- `ExplorationEngine.coverage` (method) `cli/exploration.py:610` `def coverage(self, target)` -- Return an aggregate :class:`CoverageReport` for the engagement.
- `resolve_current_os` (function) `cli/exploration.py:656` `def resolve_current_os(payload)` -- Resolve the current victim platform from a payload-like mapping.
- `normalise_os` (function) `cli/exploration.py:677` `def normalise_os(value, default)` -- Coerce arbitrary YAML/JSON values to a whitelisted OS string.
- `normalise_trigger` (function) `cli/exploration.py:690` `def normalise_trigger(value)` -- Coerce arbitrary YAML/JSON values to a tuple of trigger strings.

## cli/exploration_view.py
Depends on: `cli/exploration.py`, `core/console.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_exploration_and_addons.py`
- `render_exploration` (function) `cli/exploration_view.py:39` `def render_exploration(console, engine, target, history)` -- Render the full ``explore`` view to ``console``.

## cli/fuzzy_match.py
Depends on: `cli/fuzzy_picker.py`
Imported by: `cli/commands/ux.py`
- `suggest` (function) `cli/fuzzy_match.py:28` `def suggest(query, candidates, limit, config)` -- Return up to limit candidate names ranked by relevance to query.
- `did_you_mean` (function) `cli/fuzzy_match.py:56` `def did_you_mean(query, candidates)` -- Return the single best correction for query or None.

## cli/fuzzy_picker.py
Imported by: `cli/fuzzy_match.py`, `lazyown.py`, `tests/test_fuzzy_picker.py`
- `PickerConfig.from_payload` (method) `cli/fuzzy_picker.py:117` `def from_payload(cls, payload)` -- Build a config from a payload.json view, falling back to defaults.
- `MatchScorer.__init__` (method) `cli/fuzzy_picker.py:170` `def __init__(self, config)`
- `MatchScorer.rank` (method) `cli/fuzzy_picker.py:173` `def rank(self, items, query)` -- Return ``items`` ranked by descending relevance against ``query``.
- `PickerView.run` (method) `cli/fuzzy_picker.py:231` `def run(self, items, initial_query)`
- `CursesPickerView.__init__` (method) `cli/fuzzy_picker.py:243` `def __init__(self, config, scorer)`
- `CursesPickerView.run` (method) `cli/fuzzy_picker.py:247` `def run(self, items, initial_query)`
- `FuzzyPicker.__init__` (method) `cli/fuzzy_picker.py:551` `def __init__(self, config, view_factory)`
- `FuzzyPicker.config` (method) `cli/fuzzy_picker.py:562` `def config(self)`
- `FuzzyPicker.pick` (method) `cli/fuzzy_picker.py:565` `def pick(self, items, initial_query)` -- Return the selected item text or ``None`` on cancel / empty input.
- `ReadlineBridge.__init__` (method) `cli/fuzzy_picker.py:592` `def __init__(self, picker)`
- `ReadlineBridge.install` (method) `cli/fuzzy_picker.py:595` `def install(self)` -- Wire the picker into ``readline.set_completion_display_matches_hook``.
- `ReadlineBridge.uninstall` (method) `cli/fuzzy_picker.py:603` `def uninstall(self)` -- Remove the readline display hook installed by :py:meth:`install`.
- `install_fuzzy_completion` (function) `cli/fuzzy_picker.py:645` `def install_fuzzy_completion(shell, payload, config)` -- Install the fuzzy picker into a cmd2 shell.

## cli/graph_advisor.py
Imported by: `cli/commands/misc_migrated.py`, `cli/dashboard_tui.py`, `cli/graph_overlay.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `lazyown.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`, `tests/test_graph_advisor.py`
- `GraphNode.to_summary` (method) `cli/graph_advisor.py:109` `def to_summary(self)` -- Return a small, JSON-safe summary suitable for MCP responses.
- `GraphEdge.to_summary` (method) `cli/graph_advisor.py:132` `def to_summary(self)`
- `GraphLoader.__init__` (method) `cli/graph_advisor.py:156` `def __init__(self, config)`
- `GraphLoader.resolve_path` (method) `cli/graph_advisor.py:160` `def resolve_path(self, override)` -- Resolve which graphify JSON file to load.
- `GraphLoader.load` (method) `cli/graph_advisor.py:184` `def load(self, override)`
- `GraphLoader.clear_cache` (method) `cli/graph_advisor.py:207` `def clear_cache(cls)`
- `GraphIndex.__init__` (method) `cli/graph_advisor.py:214` `def __init__(self, data)`
- `GraphIndex.nodes` (method) `cli/graph_advisor.py:277` `def nodes(self)`
- `GraphIndex.get` (method) `cli/graph_advisor.py:280` `def get(self, node_id)`
- `GraphIndex.neighbors` (method) `cli/graph_advisor.py:283` `def neighbors(self, node_id)`
- `GraphIndex.edges_between` (method) `cli/graph_advisor.py:286` `def edges_between(self, source, target)`
- `GraphIndex.community_members` (method) `cli/graph_advisor.py:289` `def community_members(self, community_id)`
- `GraphIndex.degree` (method) `cli/graph_advisor.py:292` `def degree(self, node_id)`
- `GraphIndex.degree_ranked` (method) `cli/graph_advisor.py:295` `def degree_ranked(self)`
- `GraphScorer.__init__` (method) `cli/graph_advisor.py:304` `def __init__(self, config)`
- `GraphScorer.rank` (method) `cli/graph_advisor.py:307` `def rank(self, nodes, query)`
- `GraphAdvisor.__init__` (method) `cli/graph_advisor.py:362` `def __init__(self, config, loader, index, scorer)`
- `GraphAdvisor.from_path` (method) `cli/graph_advisor.py:375` `def from_path(cls, path, config)`
- `GraphAdvisor.is_available` (method) `cli/graph_advisor.py:384` `def is_available(self)`
- `GraphAdvisor.reload` (method) `cli/graph_advisor.py:387` `def reload(self, path)`
- `GraphAdvisor.summary` (method) `cli/graph_advisor.py:396` `def summary(self)`
- `GraphAdvisor.search` (method) `cli/graph_advisor.py:445` `def search(self, query, limit)`
- `GraphAdvisor.neighbors` (method) `cli/graph_advisor.py:456` `def neighbors(self, node_query, depth, limit)`
- `GraphAdvisor.god_nodes` (method) `cli/graph_advisor.py:505` `def god_nodes(self, limit)`
- `GraphAdvisor.suggest_next` (method) `cli/graph_advisor.py:520` `def suggest_next(self, recent_commands, limit)` -- Suggest next commands by walking the graph outward from recent ones.
- `GraphAdvisor.read_recent_commands` (method) `cli/graph_advisor.py:566` `def read_recent_commands(self, window)` -- Read the last N executed commands from the session transcript.
- `GraphAdvisor.did_you_mean` (method) `cli/graph_advisor.py:591` `def did_you_mean(self, query, limit)`
- `GraphAdvisor.truncate_to_budget` (method) `cli/graph_advisor.py:605` `def truncate_to_budget(self, payload, budget_tokens)` -- Trim list fields in-place so the JSON dump fits a token budget.
- `format_search_table` (function) `cli/graph_advisor.py:691` `def format_search_table(results)` -- Render search results as a fixed-width table for the cmd2 shell.
- `format_neighbors` (function) `cli/graph_advisor.py:706` `def format_neighbors(result)` -- Render a :py:meth:`GraphAdvisor.neighbors` result as plain text.
- `format_god_nodes` (function) `cli/graph_advisor.py:724` `def format_god_nodes(results)`
- `format_suggestions` (function) `cli/graph_advisor.py:734` `def format_suggestions(results)`

## cli/graph_overlay.py
Depends on: `cli/commands/containers.py`, `cli/commands/enum.py`, `cli/graph_advisor.py`, `cli/themes.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_graph_overlay.py`
- `GraphOverlayState.is_available` (method) `cli/graph_overlay.py:77` `def is_available(self)` -- Return ``True`` when the underlying graph advisor has data.
- `GraphOverlayState.set_focus` (method) `cli/graph_overlay.py:87` `def set_focus(self, value)` -- Replace the focus query.
- `GraphOverlayState.toggle_view` (method) `cli/graph_overlay.py:95` `def toggle_view(self)` -- Switch between god-nodes and neighbors-of-focus.
- `GraphOverlayState.snapshot` (method) `cli/graph_overlay.py:102` `def snapshot(self)` -- Return ``(header, items)`` for the current view.
- `build_state` (function) `cli/graph_overlay.py:192` `def build_state(config, advisor_factory)` -- Wire the canonical state used by :func:`launch_overlay`.
- `launch_overlay` (function) `cli/graph_overlay.py:203` `def launch_overlay(payload, state, runner)` -- Open the overlay and return the last-focused node id on exit.
- `_GraphOverlayApp.__init__` (method) `cli/graph_overlay.py:260` `def __init__(self)`
- `_GraphOverlayApp.compose` (method) `cli/graph_overlay.py:265` `def compose(self)`
- `_GraphOverlayApp.on_mount` (method) `cli/graph_overlay.py:273` `def on_mount(self)`
- `_GraphOverlayApp.on_input_changed` (method) `cli/graph_overlay.py:276` `def on_input_changed(self, event)`
- `_GraphOverlayApp.action_toggle_view` (method) `cli/graph_overlay.py:280` `def action_toggle_view(self)`
- `_GraphOverlayApp.action_close` (method) `cli/graph_overlay.py:284` `def action_close(self)`

## cli/headless.py
Imported by: `lazyown.py`
- `load_profile` (function) `cli/headless.py:31` `def load_profile(path)` -- Load a YAML profile that overrides payload.json keys.
- `apply_profile` (function) `cli/headless.py:48` `def apply_profile(config, profile)` -- Merge profile values into config (shallow overlay).
- `HeadlessRunner.__init__` (method) `cli/headless.py:72` `def __init__(self, shell, json_output, profile_path)`
- `HeadlessRunner.run_command` (method) `cli/headless.py:87` `def run_command(self, cmd, timeout)` -- Execute a single command, capture output, return structured result.
- `HeadlessRunner.run_chain` (method) `cli/headless.py:132` `def run_chain(self, commands)` -- Execute multiple commands and emit final summary.

## cli/killchain.py
Depends on: `modules/killchain.py`
Imported by: `cli/dashboard_tui.py`, `tests/test_killchain.py`
- `compute_killchain` (function) `cli/killchain.py:83` `def compute_killchain(events, world, phases)` -- Compute kill-chain progress from daemon events and the world model.

## cli/lazy_monitor.py
Depends on: `cli/commands/containers.py`, `modules/jsonl_tail.py`, `modules/lazy_engine.py`, `modules/lazy_runner.py`, `modules/loop_progress.py`
Imported by: `cli/commands/lazyloop.py`, `modules/lazy_runner.py`, `modules/tools/monitor_smoke.py`
- `PromptModal.__init__` (method) `cli/lazy_monitor.py:66` `def __init__(self, title, placeholder)` -- Store the modal labels.
- `PromptModal.compose` (method) `cli/lazy_monitor.py:72` `def compose(self)` -- Title plus a single input line.
- `PromptModal.on_input_submitted` (method) `cli/lazy_monitor.py:80` `def on_input_submitted(self, event)` -- Dismiss with the typed value.
- `PromptModal.action_dismiss` (method) `cli/lazy_monitor.py:84` `def action_dismiss(self, value)` -- Escape closes with an empty value.
- `LazyMonitorApp.__init__` (method) `cli/lazy_monitor.py:124` `def __init__(self, task_id, engine, config, params)` -- Bind the monitor to a task and optionally embed a live engine.
- `LazyMonitorApp.compose` (method) `cli/lazy_monitor.py:140` `def compose(self)` -- Build the split view: stages, worker panes, audit tabs.
- `LazyMonitorApp.on_mount` (method) `cli/lazy_monitor.py:168` `def on_mount(self)` -- Resolve the task, wire pane logs and start polling.
- `LazyMonitorApp.action_pause` (method) `cli/lazy_monitor.py:409` `def action_pause(self)` -- Pause the task between worker steps.
- `LazyMonitorApp.action_resume` (method) `cli/lazy_monitor.py:417` `def action_resume(self)` -- Resume a paused task.
- `LazyMonitorApp.action_approve` (method) `cli/lazy_monitor.py:425` `def action_approve(self)` -- Approve the first pending intercept.
- `LazyMonitorApp.action_deny` (method) `cli/lazy_monitor.py:429` `def action_deny(self)` -- Deny the first pending intercept.
- `LazyMonitorApp.action_hint` (method) `cli/lazy_monitor.py:445` `def action_hint(self)` -- Inject an operator hint for the next planner round.
- `LazyMonitorApp.action_steer` (method) `cli/lazy_monitor.py:460` `def action_steer(self)` -- Send a mid-run correction to the newest running intent.
- `LazyMonitorApp.action_kill` (method) `cli/lazy_monitor.py:477` `def action_kill(self)` -- Kill the newest running intent.
- `LazyMonitorApp.action_tab_findings` (method) `cli/lazy_monitor.py:489` `def action_tab_findings(self)` -- Focus the findings tab.
- `LazyMonitorApp.action_tab_guard` (method) `cli/lazy_monitor.py:493` `def action_tab_guard(self)` -- Focus the guard tab.
- `LazyMonitorApp.action_tab_traffic` (method) `cli/lazy_monitor.py:497` `def action_tab_traffic(self)` -- Focus the traffic tab.
- `LazyMonitorApp.action_focus_worker` (method) `cli/lazy_monitor.py:508` `def action_focus_worker(self, index)` -- Scroll the matching worker pane into view.
- `LazyMonitorApp.action_next_task` (method) `cli/lazy_monitor.py:518` `def action_next_task(self)` -- Switch the monitor to the next task in the store.
- `run_monitor_command` (function) `cli/lazy_monitor.py:575` `def run_monitor_command(task_id)` -- Attach the monitor to an existing task (never blocks the loop).
- `run_monitor_session` (function) `cli/lazy_monitor.py:589` `def run_monitor_session(engine, config, params)` -- Run the loop inside the monitor (``lazy_loop --view``).

## cli/lazy_orchestrator.py
Depends on: `cli/commands/containers.py`, `cli/orchestrator_assets_tabs.py`, `cli/palette.py`, `cli/tui_forms.py`, `core/param_registry.py`, `modules/jsonl_tail.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/orchestrator_config.py`, `modules/redteam_gym.py`, `modules/verb_catalog.py`
Imported by: `cli/commands/lazyloop.py`, `tests/test_guardrails.py`, `tests/test_lazy_orchestrator.py`, `tests/test_orchestrator_triggers.py`, `tests/test_orchestrator_yaml.py`, `tests/test_param_registry.py`
- `discover_shell_commands` (function) `cli/lazy_orchestrator.py:66` `def discover_shell_commands()` -- Return every routable shell command name.
- `command_descriptions` (function) `cli/lazy_orchestrator.py:99` `def command_descriptions()` -- Return ``{command: summary}`` from the palette index when available.
- `verb_candidates` (function) `cli/lazy_orchestrator.py:113` `def verb_candidates()` -- Return searchable ``(verb, description)`` pairs for the picker.
- `LazyOrchestratorApp.__init__` (method) `cli/lazy_orchestrator.py:174` `def __init__(self, payload_path, task_id, shell, param_root)` -- Bind the console to a payload file and an optional task.
- `LazyOrchestratorApp.compose` (method) `cli/lazy_orchestrator.py:208` `def compose(self)` -- Build the four panes.
- `LazyOrchestratorApp.on_mount` (method) `cli/lazy_orchestrator.py:274` `def on_mount(self)` -- Load the payload into the form and refresh the data tables.
- `LazyOrchestratorApp.toggle_stage` (method) `cli/lazy_orchestrator.py:292` `def toggle_stage(self, name)` -- Flip one pipeline stage on/off and persist it.
- `LazyOrchestratorApp.toggle_verb` (method) `cli/lazy_orchestrator.py:301` `def toggle_verb(self, name)` -- Flip one auto verb on/off and persist it in its owning layer.
- `LazyOrchestratorApp.add_auto_verb` (method) `cli/lazy_orchestrator.py:317` `def add_auto_verb(self, name, keywords, needs_target, description, phases)` -- Register a new operator-defined auto verb.
- `LazyOrchestratorApp.remove_auto_verb` (method) `cli/lazy_orchestrator.py:340` `def remove_auto_verb(self, name)` -- Delete a custom verb, or disable a built-in one.
- `LazyOrchestratorApp.on_button_pressed` (method) `cli/lazy_orchestrator.py:401` `def on_button_pressed(self, event)` -- Handle the config and harness buttons.
- `LazyOrchestratorApp.action_refresh` (method) `cli/lazy_orchestrator.py:454` `def action_refresh(self)` -- Reload tables and form from disk.
- `LazyOrchestratorApp.create_param` (method) `cli/lazy_orchestrator.py:491` `def create_param(self, name, kind, default, description, category)` -- Declare a reusable parameter and publish it to the live shell.
- `LazyOrchestratorApp.update_param` (method) `cli/lazy_orchestrator.py:531` `def update_param(self, name, default, description)` -- Update a declared parameter and repaint the table.
- `LazyOrchestratorApp.delete_param` (method) `cli/lazy_orchestrator.py:563` `def delete_param(self, name)` -- Delete an operator parameter and drop it from the live shell.
- `LazyOrchestratorApp.action_toggle_item` (method) `cli/lazy_orchestrator.py:595` `def action_toggle_item(self)` -- Toggle the selected stage, auto verb, or chain.
- `LazyOrchestratorApp.action_save_config` (method) `cli/lazy_orchestrator.py:625` `def action_save_config(self)` -- Save the form values (keyboard shortcut).
- `LazyOrchestratorApp.action_add_item` (method) `cli/lazy_orchestrator.py:642` `def action_add_item(self)` -- Open the add modal for the active tab.
- `LazyOrchestratorApp.action_edit_item` (method) `cli/lazy_orchestrator.py:874` `def action_edit_item(self)` -- Edit the selected playbook YAML, LLM member priority or parameter.
- `LazyOrchestratorApp.action_delete_item` (method) `cli/lazy_orchestrator.py:953` `def action_delete_item(self)` -- Delete the selected row in the active tab.
- `run_orchestrator_console` (function) `cli/lazy_orchestrator.py:1045` `def run_orchestrator_console(task_id, shell)` -- Launch the admin console (attach mode).

## cli/lazynmap_post.py
Depends on: `cli/exploration.py`, `cli/recon_plan.py`, `modules/killchain.py`
Imported by: `cli/commands/recon.py`, `lazyown.py`, `tests/test_lazynmap_post.py`, `tests/test_single_source_of_truth.py`
- `run_post_scan` (function) `cli/lazynmap_post.py:94` `def run_post_scan(target, payload, console, config, engine_factory, plan_config, clock)` -- Generate the plan, bump the world model and emit an event.

## cli/marketplace_config.py
Depends on: `cli/tui_forms.py`
Imported by: `cli/commands/marketplace.py`, `cli/wizard.py`
- `AddonInfo.from_path` (method) `cli/marketplace_config.py:151` `def from_path(cls, path, kind)` -- Build one entry from its file, tolerating malformed content.
- `AddonInfo.toggleable` (method) `cli/marketplace_config.py:221` `def toggleable(self)` -- Return whether this entry has a persisted enable/disable flag.
- `AddonInfo.read_text` (method) `cli/marketplace_config.py:225` `def read_text(self)` -- Return the raw file text, capped for the in-app editor.
- `AddonInfo.read_data` (method) `cli/marketplace_config.py:229` `def read_data(self)` -- Return the parsed mapping for the entry's format.
- `AddonInfo.validate_text` (method) `cli/marketplace_config.py:238` `def validate_text(self, text)` -- Raise ``ValueError`` when the edited document is not usable.
- `AddonInfo.save_text` (method) `cli/marketplace_config.py:260` `def save_text(self, text)` -- Validate and atomically rewrite the raw entry.
- `AddonInfo.set_enabled` (method) `cli/marketplace_config.py:278` `def set_enabled(self, enabled)` -- Persist the enable/disable flag in the entry's native format.
- `AddonInfo.toggle_enabled` (method) `cli/marketplace_config.py:299` `def toggle_enabled(self)` -- Flip the enabled state on disk.
- `AddonInfo.save_yaml` (method) `cli/marketplace_config.py:303` `def save_yaml(self, data)` -- Rewrite a YAML entry with the given mapping (compatibility helper).
- `AddonRegistry.__init__` (method) `cli/marketplace_config.py:331` `def __init__(self)` -- Start with an empty per-tab cache.
- `AddonRegistry.scan` (method) `cli/marketplace_config.py:342` `def scan(self, tab)` -- Return the cached (or freshly scanned) rows for one tab.
- `AddonRegistry.rescan` (method) `cli/marketplace_config.py:426` `def rescan(self, tab)` -- Drop one tab cache and scan again.
- `AddonRegistry.tab_order` (method) `cli/marketplace_config.py:431` `def tab_order(self)` -- Return the tab order used by the console.
- `AddonRegistry.tab_label` (method) `cli/marketplace_config.py:435` `def tab_label(self, tab)` -- Return the human label for one tab.
- `AddonRegistry.tab_count` (method) `cli/marketplace_config.py:439` `def tab_count(self, tab)` -- Return how many entries one tab holds.
- `AddonRegistry.tab_is_read_only` (method) `cli/marketplace_config.py:443` `def tab_is_read_only(self, tab)` -- Return whether toggles are meaningless for the tab.
- `AddonRegistry.create_addon` (method) `cli/marketplace_config.py:447` `def create_addon(self, tab, name)` -- Create one entry from the tab template.
- `AddonRegistry.delete_addon` (method) `cli/marketplace_config.py:491` `def delete_addon(self, addon)` -- Delete one writable entry confined to its source directory.
- `MarketplaceSettings.is_enabled` (method) `cli/marketplace_config.py:513` `def is_enabled(self, kind, name)` -- Return whether one entry is enabled.
- `MarketplaceSettings.toggle` (method) `cli/marketplace_config.py:517` `def toggle(self, addon)` -- Flip one entry, updating the in-memory view only on success.
- `MarketplaceSettings.enable_all` (method) `cli/marketplace_config.py:529` `def enable_all(self, addons)` -- Enable every toggleable entry; return how many changed.
- `MarketplaceSettings.disable_all` (method) `cli/marketplace_config.py:537` `def disable_all(self, addons)` -- Disable every toggleable entry; return how many changed.
- `MarketplaceConfigApp.__init__` (method) `cli/marketplace_config.py:578` `def __init__(self, config, registry, initial, start_tab)` -- Bind the console to a config, registry and initial state.
- `MarketplaceConfigApp.compose` (method) `cli/marketplace_config.py:593` `def compose(self)` -- Header, filter box, one table per tab and the detail pane.
- `MarketplaceConfigApp.on_mount` (method) `cli/marketplace_config.py:604` `def on_mount(self)` -- Render every table and focus the filter box.
- `MarketplaceConfigApp.on_data_table_row_highlighted` (method) `cli/marketplace_config.py:722` `def on_data_table_row_highlighted(self, event)` -- Refresh the detail pane when the cursor moves.
- `MarketplaceConfigApp.on_input_changed` (method) `cli/marketplace_config.py:732` `def on_input_changed(self, event)` -- Filter the active table as the operator types.
- `MarketplaceConfigApp.on_tabbed_content_tab_activated` (method) `cli/marketplace_config.py:738` `def on_tabbed_content_tab_activated(self, event)` -- Repaint the table that just became visible.
- `MarketplaceConfigApp.action_focus_filter` (method) `cli/marketplace_config.py:747` `def action_focus_filter(self)` -- Move focus to the filter box.
- `MarketplaceConfigApp.action_rescan` (method) `cli/marketplace_config.py:754` `def action_rescan(self)` -- Rescan the active tab and repaint.
- `MarketplaceConfigApp.action_toggle` (method) `cli/marketplace_config.py:761` `def action_toggle(self)` -- Toggle the selected entry when the tab supports it.
- `MarketplaceConfigApp.action_enable_all` (method) `cli/marketplace_config.py:772` `def action_enable_all(self)` -- Enable every toggleable entry in the active tab.
- `MarketplaceConfigApp.action_disable_all` (method) `cli/marketplace_config.py:779` `def action_disable_all(self)` -- Disable every toggleable entry in the active tab.
- `MarketplaceConfigApp.action_create` (method) `cli/marketplace_config.py:786` `def action_create(self)` -- Create one entry in the active tab from its template.
- `MarketplaceConfigApp.action_edit` (method) `cli/marketplace_config.py:811` `def action_edit(self)` -- Open the raw file editor for the selected entry.
- `MarketplaceConfigApp.action_delete` (method) `cli/marketplace_config.py:839` `def action_delete(self)` -- Delete the selected entry after confirmation.
- `MarketplaceConfigApp.action_save` (method) `cli/marketplace_config.py:863` `def action_save(self)` -- Close the console and return the final settings.
- `MarketplaceConfigApp.action_cancel` (method) `cli/marketplace_config.py:867` `def action_cancel(self)` -- Close the console without returning settings.
- `configure_marketplace_interactive` (function) `cli/marketplace_config.py:872` `def configure_marketplace_interactive(config, start_tab)` -- Open the Textual marketplace console.
- `marketplace_summary` (function) `cli/marketplace_config.py:907` `def marketplace_summary(registry)` -- Return a text summary of enabled/disabled addons across all tabs.

## cli/ops_commands.py
Depends on: `core/safe_console.py`, `modules/killchain.py`, `modules/world_model.py`
Imported by: `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `cli/dashboard_tui.py`, `cli/tips_engine.py`, `lazyown.py`, `tests/test_killchain_unified.py`, `tests/test_ops_loot_phase.py`
- `print_ctx` (function) `cli/ops_commands.py:74` `def print_ctx(payload, sessions_dir)` -- Print a single-line operator context summary.
- `tgrep` (function) `cli/ops_commands.py:115` `def tgrep(pattern)` -- Search past command outputs and session logs for ``pattern``.
- `read_phase` (function) `cli/ops_commands.py:279` `def read_phase()` -- Return the current kill-chain phase from the unified killchain module.
- `write_phase` (function) `cli/ops_commands.py:302` `def write_phase(phase)` -- Set the current kill-chain phase via the unified killchain module.
- `print_phase` (function) `cli/ops_commands.py:317` `def print_phase()` -- Print the current phase and the full kill-chain progress bar.
- `phase_progress` (function) `cli/ops_commands.py:393` `def phase_progress(world, sessions_dir)` -- Return per-phase completion ratios from the unified kill-chain progress.
- `note_add` (function) `cli/ops_commands.py:475` `def note_add(text, rhost, phase)` -- Append a timestamped operator note to sessions/notes.jsonl.
- `note_list` (function) `cli/ops_commands.py:500` `def note_list(rhost, limit)` -- Print recent operator notes, optionally filtered by rhost.
- `LootEntry.value` (method) `cli/ops_commands.py:568` `def value(self)` -- Return the canonical ``user:secret`` credential value.
- `gather_loot` (function) `cli/ops_commands.py:578` `def gather_loot(sessions_dir)` -- Parse every credentials*.txt and hash*.txt under ``sessions_dir``.
- `loot_show` (function) `cli/ops_commands.py:621` `def loot_show(sessions_dir)` -- Print a unified table of all captured credentials and hashes.
- `loot_search` (function) `cli/ops_commands.py:693` `def loot_search(query, sessions_dir)` -- Search captured loot for ``query`` across users and secrets.
- `loot_reuse` (function) `cli/ops_commands.py:770` `def loot_reuse(rhost, sessions_dir)` -- Suggest captured credentials worth trying against ``rhost``.
- `loot_graph` (function) `cli/ops_commands.py:854` `def loot_graph(sessions_dir)` -- Render the credential-centric view of the network graph.
- `resolve_cred_value` (function) `cli/ops_commands.py:924` `def resolve_cred_value(selector, entries)` -- Resolve a user/secret ``selector`` to a canonical credential value.
- `loot_mark` (function) `cli/ops_commands.py:952` `def loot_mark(selector, outcome, host, sessions_dir)` -- Record that a credential worked or was rejected against ``host``.
- `pivot_add` (function) `cli/ops_commands.py:994` `def pivot_add(new_ip, via_ip, note)` -- Record a newly discovered pivot target.
- `pivot_list` (function) `cli/ops_commands.py:1020` `def pivot_list()` -- Print the pivot chain discovered so far.
- `tasks_list` (function) `cli/ops_commands.py:1077` `def tasks_list(status_filter, limit)` -- Print tasks from sessions/tasks.json.
- `tasks_add` (function) `cli/ops_commands.py:1132` `def tasks_add(title, operator)` -- Append a new task to sessions/tasks.json.
- `tasks_done` (function) `cli/ops_commands.py:1153` `def tasks_done(task_id)` -- Mark a task as Done.
- `tasks_start` (function) `cli/ops_commands.py:1173` `def tasks_start(task_id)` -- Mark a task as Started.
- `scans_list` (function) `cli/ops_commands.py:1196` `def scans_list(rhost, sessions_dir)` -- List nmap scan files in sessions/, optionally filtered by rhost.
- `sitrep` (function) `cli/ops_commands.py:1249` `def sitrep(payload, sessions_dir)` -- Print a unified operational situation report.

## cli/orchestrator_assets_tabs.py
Depends on: `cli/tui_forms.py`, `core/config.py`, `modules/__init__.py`, `modules/apt_playbooks.py`, `modules/chain_registry.py`, `modules/guardrails/__init__.py`, `modules/gym_registry.py`, `modules/lazy_engine.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`, `modules/playbook_admin.py`, `modules/redteam_gym.py`, `modules/trigger_policy.py`
Imported by: `cli/lazy_orchestrator.py`
- `OrchestratorAssetsMixin.playbook_rows` (method) `cli/orchestrator_assets_tabs.py:71` `def playbook_rows(self)` -- Return one row per playbook file, including invalid ones.
- `OrchestratorAssetsMixin.playbook_preview` (method) `cli/orchestrator_assets_tabs.py:95` `def playbook_preview(self, filename, limit)` -- Return a bounded YAML preview for one playbook file.
- `OrchestratorAssetsMixin.create_playbook_file` (method) `cli/orchestrator_assets_tabs.py:104` `def create_playbook_file(self, filename, name, description, platforms)` -- Create one playbook YAML and repaint the table.
- `OrchestratorAssetsMixin.save_playbook_text` (method) `cli/orchestrator_assets_tabs.py:125` `def save_playbook_text(self, filename, text)` -- Validate and persist raw YAML edited by the operator.
- `OrchestratorAssetsMixin.delete_playbook_file` (method) `cli/orchestrator_assets_tabs.py:137` `def delete_playbook_file(self, filename)` -- Delete one playbook YAML after the operator confirms.
- `OrchestratorAssetsMixin.playbook_candidates` (method) `cli/orchestrator_assets_tabs.py:145` `def playbook_candidates(self)` -- Return ``(engine_key, summary)`` pairs for chain generation.
- `OrchestratorAssetsMixin.gym_rows` (method) `cli/orchestrator_assets_tabs.py:228` `def gym_rows(self)` -- Return one row per gym definition with its active-run count.
- `OrchestratorAssetsMixin.gym_preview` (method) `cli/orchestrator_assets_tabs.py:265` `def gym_preview(self, gym_id, limit)` -- Return a bounded YAML preview for one gym definition.
- `OrchestratorAssetsMixin.start_gym` (method) `cli/orchestrator_assets_tabs.py:333` `def start_gym(self, gym_id, target)` -- Start one gym and repaint the table.
- `OrchestratorAssetsMixin.stop_gym` (method) `cli/orchestrator_assets_tabs.py:341` `def stop_gym(self, selector)` -- Stop one gym (or every gym when selector is empty) and repaint.
- `OrchestratorAssetsMixin.toggle_gym` (method) `cli/orchestrator_assets_tabs.py:349` `def toggle_gym(self, gym_id)` -- Start the selected gym, or stop its active runs when already active.
- `OrchestratorAssetsMixin.profile_rows` (method) `cli/orchestrator_assets_tabs.py:391` `def profile_rows(self)` -- Return one row per orchestrator profile with the active marker.
- `OrchestratorAssetsMixin.activate_profile` (method) `cli/orchestrator_assets_tabs.py:416` `def activate_profile(self, name)` -- Persist one profile as active and repaint the profile table.
- `OrchestratorAssetsMixin.chain_rows` (method) `cli/orchestrator_assets_tabs.py:476` `def chain_rows(self)` -- Return one row per chain file, including disabled ones.
- `OrchestratorAssetsMixin.chain_steps_preview` (method) `cli/orchestrator_assets_tabs.py:485` `def chain_steps_preview(self, name, limit)` -- Return the resolved step lines of a chain for the detail pane.
- `OrchestratorAssetsMixin.toggle_chain` (method) `cli/orchestrator_assets_tabs.py:502` `def toggle_chain(self, name)` -- Flip a chain's enabled flag in its YAML file.
- `OrchestratorAssetsMixin.generate_chain` (method) `cli/orchestrator_assets_tabs.py:513` `def generate_chain(self, playbook_key)` -- Generate chains/apt_<slug>.yaml from a playbook engine key.
- `OrchestratorAssetsMixin.remove_chain` (method) `cli/orchestrator_assets_tabs.py:527` `def remove_chain(self, name)` -- Delete a chain file unless others extend it or it is the base.
- `OrchestratorAssetsMixin.on_data_table_row_highlighted` (method) `cli/orchestrator_assets_tabs.py:583` `def on_data_table_row_highlighted(self, event)` -- Refresh the detail pane when the cursor moves.
- `OrchestratorAssetsMixin.toggle_trigger` (method) `cli/orchestrator_assets_tabs.py:637` `def toggle_trigger(self, trigger_id)` -- Flip one trigger's enabled flag in the store.
- `OrchestratorAssetsMixin.remove_trigger` (method) `cli/orchestrator_assets_tabs.py:647` `def remove_trigger(self, trigger_id)` -- Delete one trigger from the store.
- `OrchestratorAssetsMixin.add_trigger` (method) `cli/orchestrator_assets_tabs.py:655` `def add_trigger(self, kind, every_sec, arg)` -- Add a scheduler trigger entered from the picker form.
- `OrchestratorAssetsMixin.trigger_kind_options` (method) `cli/orchestrator_assets_tabs.py:667` `def trigger_kind_options(self)` -- Return selectable trigger kinds for the add form.
- `OrchestratorAssetsMixin.save_config` (method) `cli/orchestrator_assets_tabs.py:734` `def save_config(self, values)` -- Merge the given keys into the payload and persist it.
- `OrchestratorAssetsMixin.add_model_member` (method) `cli/orchestrator_assets_tabs.py:756` `def add_model_member(self, name, model, priority)` -- Append one LLM chain member; returns the stored name.
- `OrchestratorAssetsMixin.remove_model_member` (method) `cli/orchestrator_assets_tabs.py:764` `def remove_model_member(self, name)` -- Drop one LLM chain member by name.
- `OrchestratorAssetsMixin.set_model_priority` (method) `cli/orchestrator_assets_tabs.py:772` `def set_model_priority(self, name, priority)` -- Change one LLM member's failover rank and repaint the table.
- `OrchestratorAssetsMixin.set_harness` (method) `cli/orchestrator_assets_tabs.py:784` `def set_harness(self, enabled)` -- Toggle the deterministic harness from the orchestrator UI.
- `OrchestratorAssetsMixin.add_guard_rule` (method) `cli/orchestrator_assets_tabs.py:809` `def add_guard_rule(self, pattern, action, reason)` -- Register one guard intercept rule.
- `OrchestratorAssetsMixin.remove_guard_rule` (method) `cli/orchestrator_assets_tabs.py:817` `def remove_guard_rule(self, pattern)` -- Delete one guard rule by exact pattern.
- `OrchestratorAssetsMixin.save_guardrails` (method) `cli/orchestrator_assets_tabs.py:868` `def save_guardrails(self, values)` -- Merge harness settings into payload and reconfigure the harness.
- `OrchestratorAssetsMixin.warm_restart_harness` (method) `cli/orchestrator_assets_tabs.py:914` `def warm_restart_harness(self)` -- Run the harness warm restart and repaint the table.
- `OrchestratorAssetsMixin.rearm_harness` (method) `cli/orchestrator_assets_tabs.py:926` `def rearm_harness(self)` -- Re-arm suspended features and clear advisories.

## cli/output_mode.py
Imported by: `cli/commands/anti_forensics.py`, `cli/commands/ux.py`
- `parse_output_flags` (function) `cli/output_mode.py:43` `def parse_output_flags(args, config)` -- Split output control flags from positional command arguments.
- `strip_ansi` (function) `cli/output_mode.py:65` `def strip_ansi(text)` -- Remove ANSI escape sequences from text.
- `format_output` (function) `cli/output_mode.py:77` `def format_output(data, mode)` -- Render data according to the parsed output mode.
- `dry_run_line` (function) `cli/output_mode.py:98` `def dry_run_line(command)` -- Render the exact shell line that would run without running it.

## cli/palette.py
Imported by: `cli/command_explorer.py`, `cli/command_form.py`, `cli/commands/misc_migrated.py`, `cli/contextual_help.py`, `cli/engagement_hooks.py`, `cli/lazy_orchestrator.py`, `cli/palette_overlay.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_command_palette.py`
- `load_index` (function) `cli/palette.py:30` `def load_index(path)` -- Return the parsed catalogue as a dict.
- `all_commands` (function) `cli/palette.py:55` `def all_commands()` -- Return every command entry, sorted by name.
- `all_phases` (function) `cli/palette.py:72` `def all_phases()` -- Return the sorted list of phase identifiers present in the index.
- `all_categories` (function) `cli/palette.py:77` `def all_categories()` -- Return the sorted list of cmd2 category labels present in the index.
- `filter_by_phase` (function) `cli/palette.py:82` `def filter_by_phase(phase)` -- Return command entries whose ``phase`` matches ``phase``.
- `filter_by_category` (function) `cli/palette.py:92` `def filter_by_category(category)` -- Return command entries with the given cmd2 category label.
- `search` (function) `cli/palette.py:97` `def search(query)` -- Substring search over ``name`` and ``summary`` (case-insensitive).
- `get` (function) `cli/palette.py:114` `def get(name)` -- Return the canonical entry for ``name`` or ``None`` if unknown.
- `duplicates` (function) `cli/palette.py:125` `def duplicates()` -- Return the duplicate-method audit list as stored in the index.
- `totals` (function) `cli/palette.py:130` `def totals()` -- Return the ``totals`` block (counts of methods, unique names, ...).

## cli/palette_command.py
Depends on: `cli/commands/enum.py`, `cli/palette_graph.py`, `cli/palette_telemetry.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/palette_overlay.py`, `lazyc2.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_command_palette.py`
- `PaletteRenderConfig.truncate_summary` (method) `cli/palette_command.py:107` `def truncate_summary(self, summary)` -- Trim ``summary`` to :attr:`summary_max_chars` with marker suffix.
- `PaletteArgumentParser.__init__` (method) `cli/palette_command.py:149` `def __init__(self, config)`
- `PaletteArgumentParser.parse` (method) `cli/palette_command.py:152` `def parse(self, line)` -- Return a :class:`PaletteArgs` for ``line``.
- `PaletteIndexQuery.__init__` (method) `cli/palette_command.py:193` `def __init__(self, index)`
- `PaletteIndexQuery.commands` (method) `cli/palette_command.py:197` `def commands(self)` -- Return canonical (non-duplicate) command entries.
- `PaletteIndexQuery.phases` (method) `cli/palette_command.py:203` `def phases(self)` -- Return the sorted list of phase identifiers in the index.
- `PaletteIndexQuery.phase_counts` (method) `cli/palette_command.py:208` `def phase_counts(self)` -- Return ``{phase: command_count}`` for every phase in the index.
- `PaletteIndexQuery.in_phase` (method) `cli/palette_command.py:213` `def in_phase(self, phase)` -- Return commands whose ``phase`` matches ``phase`` (case-insensitive).
- `PaletteIndexQuery.search` (method) `cli/palette_command.py:218` `def search(self, query)` -- Substring search over ``name`` and ``summary`` (case-insensitive).
- `PaletteIndexQuery.detail` (method) `cli/palette_command.py:234` `def detail(self, target)` -- Return the canonical entry for ``target`` or ``None``.
- `PaletteIndexQuery.next_phase` (method) `cli/palette_command.py:249` `def next_phase(self, current)` -- Return the phase that comes after ``current`` in ``ordering``.
- `PaletteRenderer.__init__` (method) `cli/palette_command.py:285` `def __init__(self, config)`
- `PaletteRenderer.render_overview` (method) `cli/palette_command.py:288` `def render_overview(self, phase_counts)` -- Format the multi-phase overview table.
- `PaletteRenderer.render_phase` (method) `cli/palette_command.py:304` `def render_phase(self, phase, rows)` -- Format a phase listing of ``(name, summary)`` pairs.
- `PaletteRenderer.render_search` (method) `cli/palette_command.py:312` `def render_search(self, query, rows)` -- Format the cross-phase search result table.
- `PaletteRenderer.render_detail` (method) `cli/palette_command.py:320` `def render_detail(self, entry)` -- Format the detail view for a single command entry.
- `PaletteRenderer.render_next` (method) `cli/palette_command.py:360` `def render_next(self, phase, rows)` -- Format the recommended-next-phase listing.
- `render` (function) `cli/palette_command.py:447` `def render(index, line)` -- Top-level entry point used by :class:`LazyOwnShell.do_palette`.
- `PaletteJsonResult.to_dict` (method) `cli/palette_command.py:502` `def to_dict(self)` -- Serialise to a plain ``dict`` suitable for ``json.dumps``.
- `PaletteJsonRenderer.__init__` (method) `cli/palette_command.py:522` `def __init__(self, config)`
- `PaletteJsonRenderer.render_overview` (method) `cli/palette_command.py:525` `def render_overview(self, phase_counts)` -- Build a result document for overview mode.
- `PaletteJsonRenderer.render_phase` (method) `cli/palette_command.py:532` `def render_phase(self, phase, query, rows)` -- Build a result document for phase mode.
- `PaletteJsonRenderer.render_search` (method) `cli/palette_command.py:541` `def render_search(self, query, rows)` -- Build a result document for search mode.
- `PaletteJsonRenderer.render_detail` (method) `cli/palette_command.py:549` `def render_detail(self, target, entry)` -- Build a result document for detail mode.
- `PaletteJsonRenderer.render_next` (method) `cli/palette_command.py:557` `def render_next(self, phase, rows)` -- Build a result document for next-phase mode.
- `render_json` (function) `cli/palette_command.py:566` `def render_json(index, line)` -- Structured-data variant of :func:`render`.
- `build_palette_view` (function) `cli/palette_command.py:619` `def build_palette_view(index)` -- Assemble the template context consumed by the C2 ``/palette`` view.
- `PaletteCompleter.__init__` (method) `cli/palette_command.py:755` `def __init__(self, config)`
- `PaletteCompleter.complete` (method) `cli/palette_command.py:758` `def complete(self, text, line, endidx, index)` -- Return tab-completion candidates given the editor state.

## cli/palette_graph.py
Imported by: `cli/palette_command.py`, `tests/test_command_palette.py`
- `load_graph` (function) `cli/palette_graph.py:127` `def load_graph(path)` -- Return the parsed graph index, cached per resolved path.
- `safe_load_graph` (function) `cli/palette_graph.py:149` `def safe_load_graph(path)` -- Best-effort variant of :func:`load_graph`.
- `callees` (function) `cli/palette_graph.py:179` `def callees(graph, command_name)` -- Return helper-function labels invoked by ``command_name``.
- `related_commands` (function) `cli/palette_graph.py:226` `def related_commands(graph, command_name)` -- Return ``do_*`` commands that share helper functions with this one.
- `enrich_detail` (function) `cli/palette_graph.py:287` `def enrich_detail(graph, entry)` -- Attach ``calls`` and ``related`` lists to a palette detail entry.
- `enrich_commands` (function) `cli/palette_graph.py:309` `def enrich_commands(graph, rows)` -- Enrich every entry of ``rows`` with neighbour data.

## cli/palette_overlay.py
Depends on: `cli/commands/containers.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/palette_telemetry.py`, `cli/themes.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_palette_overlay.py`
- `PaletteOverlayState.set_query` (method) `cli/palette_overlay.py:83` `def set_query(self, value)` -- Replace the active query with ``value`` (trimmed).
- `PaletteOverlayState.rows` (method) `cli/palette_overlay.py:87` `def rows(self)` -- Return the ranked, truncated rows for the current query.
- `build_state` (function) `cli/palette_overlay.py:162` `def build_state(payload, index, recents, config)` -- Wire the canonical state used by :func:`launch_overlay`.
- `launch_overlay` (function) `cli/palette_overlay.py:188` `def launch_overlay(payload, state, runner)` -- Open the Textual overlay and return the selected command verb.
- `_PaletteOverlayApp.__init__` (method) `cli/palette_overlay.py:255` `def __init__(self)`
- `_PaletteOverlayApp.compose` (method) `cli/palette_overlay.py:261` `def compose(self)`
- `_PaletteOverlayApp.on_mount` (method) `cli/palette_overlay.py:269` `def on_mount(self)`
- `_PaletteOverlayApp.on_input_changed` (method) `cli/palette_overlay.py:272` `def on_input_changed(self, event)`
- `_PaletteOverlayApp.on_input_submitted` (method) `cli/palette_overlay.py:276` `def on_input_submitted(self, event)`
- `_PaletteOverlayApp.on_list_view_selected` (method) `cli/palette_overlay.py:279` `def on_list_view_selected(self, event)`
- `_PaletteOverlayApp.action_cancel` (method) `cli/palette_overlay.py:282` `def action_cancel(self)`
- `_PaletteOverlayApp.action_select_current` (method) `cli/palette_overlay.py:285` `def action_select_current(self)`

## cli/palette_telemetry.py
Imported by: `cli/palette_command.py`, `cli/palette_overlay.py`, `tests/test_command_palette.py`
- `load_telemetry` (function) `cli/palette_telemetry.py:186` `def load_telemetry(path)` -- Return the parsed telemetry index, cached per resolved path.
- `safe_load_telemetry` (function) `cli/palette_telemetry.py:204` `def safe_load_telemetry(path)` -- Best-effort variant of :func:`load_telemetry`.
- `command_stats` (function) `cli/palette_telemetry.py:216` `def command_stats(telemetry, command_name)` -- Return aggregated stats for ``command_name`` or ``None`` when unseen.
- `runs_after` (function) `cli/palette_telemetry.py:239` `def runs_after(telemetry, command_name)` -- Return commands that frequently run after ``command_name``.
- `recents` (function) `cli/palette_telemetry.py:259` `def recents(telemetry)` -- Return the most-recently invoked unique ``do_*`` commands.
- `enrich_detail` (function) `cli/palette_telemetry.py:275` `def enrich_detail(telemetry, entry)` -- Attach ``runs``, ``last_seen`` and ``runs_after`` to a detail entry.
- `enrich_commands` (function) `cli/palette_telemetry.py:300` `def enrich_commands(telemetry, rows)` -- Enrich every entry of ``rows`` with telemetry data.

## cli/phase_labels.py
Imported by: `cli/contextual_help.py`, `cli/tips_engine.py`, `tests/test_phase_labels.py`
- `phase_label` (function) `cli/phase_labels.py:29` `def phase_label(phase)` -- Return the human label for a phase, falling back to title case.

## cli/plugin_tiers.py
Imported by: `cli/commands/marketplace.py`, `tests/test_input_fuzz.py`, `tests/test_plugin_tiers.py`
- `load_tier_manifest` (function) `cli/plugin_tiers.py:35` `def load_tier_manifest(manifest)` -- Load explicit tier overrides from a ``tiers.yaml`` manifest.
- `tier_of` (function) `cli/plugin_tiers.py:61` `def tier_of(name, manifest_tiers, metadata_tier)` -- Resolve the tier for a plugin name.
- `rate_plugin` (function) `cli/plugin_tiers.py:98` `def rate_plugin(name, stars, store)` -- Record an operator rating and return the new ``(average, count)``.
- `rating_summary` (function) `cli/plugin_tiers.py:121` `def rating_summary(name, store)` -- Return the ``(average, count)`` rating for a plugin name.
- `format_rating` (function) `cli/plugin_tiers.py:137` `def format_rating(average, count)` -- Render a compact rating label for list and info views.
- `default_store` (function) `cli/plugin_tiers.py:144` `def default_store(base_dir)` -- Return the default ratings file under ``<base_dir>/sessions``.
- `read_metadata_tier` (function) `cli/plugin_tiers.py:149` `def read_metadata_tier(path)` -- Read the optional ``tier:`` field from a plugin YAML file.

## cli/protips.py
Depends on: `cli/noise_verbs.py`, `core/console.py`
Imported by: `lazyown.py`, `tests/test_reactive_hints_expanded.py`
- `get_session_tip` (function) `cli/protips.py:301` `def get_session_tip(ctx)` -- Return a single tip to show at session start.
- `render_contextual_tip` (function) `cli/protips.py:327` `def render_contextual_tip(last_cmd, ctx)` -- Print a single dim tip line when the last command triggers one.
- `print_session_tip` (function) `cli/protips.py:357` `def print_session_tip(ctx)` -- Print the session-start tip (called once after the banner).

## cli/purple_tui.py
Depends on: `cli/commands/containers.py`
Imported by: `cli/commands/purple_team.py`
- `PurpleDashboard.compose` (method) `cli/purple_tui.py:98` `def compose(self)`
- `PurpleDashboard.on_mount` (method) `cli/purple_tui.py:108` `def on_mount(self)`
- `PurpleDashboard.action_refresh` (method) `cli/purple_tui.py:112` `def action_refresh(self)`
- `PurpleDashboard.refresh_data` (method) `cli/purple_tui.py:115` `def refresh_data(self)`
- `launch` (function) `cli/purple_tui.py:233` `def launch()` -- Launch the purple team dashboard TUI.

## cli/reactive_hints.py
Depends on: `cli/graph_advisor.py`, `cli/noise_verbs.py`, `core/console.py`, `core/logging.py`, `core/text_utils.py`
Imported by: `cli/command_chain.py`, `cli/commands/misc_migrated.py`, `cli/dashboard_tui.py`, `cli/recommendation_signals.py`, `cli/status_bar.py`, `cli/tips_engine.py`, `lazyown.py`, `tests/test_evidence_hints.py`, `tests/test_improvements_spec.py`, `tests/test_reactive_hints.py`, `tests/test_reactive_hints_expanded.py`
- `render_inline_hints` (function) `cli/reactive_hints.py:220` `def render_inline_hints(advisor, last_command, limit, enabled)` -- Print a single dim hint line below the command output and return immediately.
- `confidence_from_score` (function) `cli/reactive_hints.py:321` `def confidence_from_score(score)` -- Map an unbounded fused recommendation score to a 0-100 display confidence.
- `build_evidence_hints` (function) `cli/reactive_hints.py:362` `def build_evidence_hints(recommendations, limit)` -- Convert fused recommendations into display-ready evidence hints.
- `render_evidence_hints` (function) `cli/reactive_hints.py:400` `def render_evidence_hints(hints)` -- Print evidence-backed hint lines: verb, confidence, reason, provenance.
- `build_evidence_hint_lines` (function) `cli/reactive_hints.py:416` `def build_evidence_hint_lines(hints)` -- Build evidence-backed hint lines as Rich Text objects.
- `read_run_commands` (function) `cli/reactive_hints.py:443` `def read_run_commands(sessions_dir)` -- Return the set of command names already executed this session.
- `render_command_hints` (function) `cli/reactive_hints.py:514` `def render_command_hints(last_command, phase, sessions_dir, limit, enabled)` -- Print phase-aware, history-filtered command hints after each step.
- `command_hints` (function) `cli/reactive_hints.py:549` `def command_hints(last_command, phase, sessions_dir, limit)` -- Return the top next-step command verbs without printing them.


Next: [API_p5.md](API_p5.md)
