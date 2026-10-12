# API (page 4 of 22)
Previous: [API_p3.md](API_p3.md)

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
Depends on: `cli/commands/containers.py`, `core/config.py`, `modules/jsonl_tail.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/orchestrator_config.py`
Imported by: `cli/commands/lazyloop.py`, `tests/test_lazy_orchestrator.py`
- `FormModal.__init__` (method) `cli/lazy_orchestrator.py:86` `def __init__(self, title, fields)` -- Store the title and (id, label, placeholder) field specs.
- `FormModal.compose` (method) `cli/lazy_orchestrator.py:92` `def compose(self)` -- One labeled input per field plus a save button.
- `FormModal.on_button_pressed` (method) `cli/lazy_orchestrator.py:101` `def on_button_pressed(self, event)` -- Collect the values and close the modal.
- `FormModal.on_input_submitted` (method) `cli/lazy_orchestrator.py:110` `def on_input_submitted(self, event)` -- Enter commits the form like the save button.
- `LazyOrchestratorApp.__init__` (method) `cli/lazy_orchestrator.py:141` `def __init__(self, payload_path, task_id)` -- Bind the console to a payload file and an optional task.
- `LazyOrchestratorApp.compose` (method) `cli/lazy_orchestrator.py:151` `def compose(self)` -- Build the four panes.
- `LazyOrchestratorApp.on_mount` (method) `cli/lazy_orchestrator.py:176` `def on_mount(self)` -- Load the payload into the form and refresh the data tables.
- `LazyOrchestratorApp.toggle_stage` (method) `cli/lazy_orchestrator.py:186` `def toggle_stage(self, name)` -- Flip one pipeline stage on/off and persist it.
- `LazyOrchestratorApp.toggle_verb` (method) `cli/lazy_orchestrator.py:195` `def toggle_verb(self, name)` -- Flip one auto verb on/off and persist it.
- `LazyOrchestratorApp.add_auto_verb` (method) `cli/lazy_orchestrator.py:204` `def add_auto_verb(self, name, keywords, needs_target, description)` -- Register a new operator-defined auto verb.
- `LazyOrchestratorApp.remove_auto_verb` (method) `cli/lazy_orchestrator.py:219` `def remove_auto_verb(self, name)` -- Delete a custom verb, or disable a built-in one.
- `LazyOrchestratorApp.save_config` (method) `cli/lazy_orchestrator.py:288` `def save_config(self, values)` -- Merge the given keys into the payload and persist it.
- `LazyOrchestratorApp.add_model_member` (method) `cli/lazy_orchestrator.py:310` `def add_model_member(self, name, model, priority)` -- Append one LLM chain member; returns the stored name.
- `LazyOrchestratorApp.remove_model_member` (method) `cli/lazy_orchestrator.py:318` `def remove_model_member(self, name)` -- Drop one LLM chain member by name.
- `LazyOrchestratorApp.add_guard_rule` (method) `cli/lazy_orchestrator.py:326` `def add_guard_rule(self, pattern, action, reason)` -- Register one guard intercept rule.
- `LazyOrchestratorApp.remove_guard_rule` (method) `cli/lazy_orchestrator.py:334` `def remove_guard_rule(self, pattern)` -- Delete one guard rule by exact pattern.
- `LazyOrchestratorApp.on_button_pressed` (method) `cli/lazy_orchestrator.py:438` `def on_button_pressed(self, event)` -- Handle the config save button.
- `LazyOrchestratorApp.action_refresh` (method) `cli/lazy_orchestrator.py:456` `def action_refresh(self)` -- Reload tables and form from disk.
- `LazyOrchestratorApp.action_toggle_item` (method) `cli/lazy_orchestrator.py:473` `def action_toggle_item(self)` -- Toggle the selected stage or auto verb.
- `LazyOrchestratorApp.action_save_config` (method) `cli/lazy_orchestrator.py:485` `def action_save_config(self)` -- Save the form values (keyboard shortcut).
- `LazyOrchestratorApp.action_add_item` (method) `cli/lazy_orchestrator.py:502` `def action_add_item(self)` -- Open the add modal for the active tab.
- `LazyOrchestratorApp.action_delete_item` (method) `cli/lazy_orchestrator.py:563` `def action_delete_item(self)` -- Delete the selected row in the active tab.
- `run_orchestrator_console` (function) `cli/lazy_orchestrator.py:605` `def run_orchestrator_console(task_id)` -- Launch the admin console (attach mode).

## cli/lazynmap_post.py
Depends on: `cli/exploration.py`, `cli/recon_plan.py`
Imported by: `cli/commands/recon.py`, `lazyown.py`, `tests/test_lazynmap_post.py`
- `run_post_scan` (function) `cli/lazynmap_post.py:94` `def run_post_scan(target, payload, console, config, engine_factory, plan_config, clock)` -- Generate the plan, bump the world model and emit an event.

## cli/marketplace_config.py
Imported by: `cli/commands/marketplace.py`, `cli/wizard.py`
- `AddonInfo.from_yaml` (method) `cli/marketplace_config.py:144` `def from_yaml(cls, path)`
- `AddonInfo.toggle_enabled` (method) `cli/marketplace_config.py:164` `def toggle_enabled(self)` -- Flip the enabled state on disk.
- `AddonInfo.set_enabled` (method) `cli/marketplace_config.py:168` `def set_enabled(self, enabled)` -- Set the enabled state and persist to disk.
- `AddonInfo.save_yaml` (method) `cli/marketplace_config.py:185` `def save_yaml(self, data)` -- Rewrite the YAML file with the given data dictionary.
- `AddonRegistry.__init__` (method) `cli/marketplace_config.py:220` `def __init__(self)`
- `AddonRegistry.scan` (method) `cli/marketplace_config.py:235` `def scan(self, tab)`
- `AddonRegistry.rescan` (method) `cli/marketplace_config.py:334` `def rescan(self, tab)`
- `AddonRegistry.tab_order` (method) `cli/marketplace_config.py:338` `def tab_order(self)`
- `AddonRegistry.tab_label` (method) `cli/marketplace_config.py:341` `def tab_label(self, tab)`
- `AddonRegistry.tab_count` (method) `cli/marketplace_config.py:344` `def tab_count(self, tab)`
- `MarketplaceSettings.is_enabled` (method) `cli/marketplace_config.py:354` `def is_enabled(self, kind, name)`
- `MarketplaceSettings.toggle` (method) `cli/marketplace_config.py:357` `def toggle(self, addon)`
- `MarketplaceSettings.enable_all` (method) `cli/marketplace_config.py:367` `def enable_all(self, addons)`
- `MarketplaceSettings.disable_all` (method) `cli/marketplace_config.py:372` `def disable_all(self, addons)`
- `MarketplaceConfigurator.__init__` (method) `cli/marketplace_config.py:381` `def __init__(self, config, registry, initial)`
- `MarketplaceConfigurator.run` (method) `cli/marketplace_config.py:395` `def run(self, start_tab)`
- `configure_marketplace_interactive` (function) `cli/marketplace_config.py:751` `def configure_marketplace_interactive(config, start_tab)` -- Open the multi-tab curses wizard for marketplace management.
- `marketplace_summary` (function) `cli/marketplace_config.py:784` `def marketplace_summary(registry)` -- Return a text summary of enabled/disabled addons across all tabs.

## cli/ops_commands.py
Depends on: `core/safe_console.py`, `modules/killchain.py`, `modules/world_model.py`
Imported by: `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `cli/dashboard_tui.py`, `cli/tips_engine.py`, `lazyown.py`, `tests/test_killchain_unified.py`, `tests/test_ops_loot_phase.py`
- `print_ctx` (function) `cli/ops_commands.py:74` `def print_ctx(payload, sessions_dir)` -- Print a single-line operator context summary.
- `tgrep` (function) `cli/ops_commands.py:115` `def tgrep(pattern)` -- Search past command outputs and session logs for ``pattern``.
- `read_phase` (function) `cli/ops_commands.py:279` `def read_phase()` -- Return the current kill-chain phase from the unified killchain module.
- `write_phase` (function) `cli/ops_commands.py:302` `def write_phase(phase)` -- Set the current kill-chain phase via the unified killchain module.
- `print_phase` (function) `cli/ops_commands.py:317` `def print_phase()` -- Print the current phase and the full kill-chain progress bar.
- `phase_progress` (function) `cli/ops_commands.py:393` `def phase_progress(world, sessions_dir)` -- Return per-phase completion ratios from the unified kill-chain progress.
- `note_add` (function) `cli/ops_commands.py:468` `def note_add(text, rhost, phase)` -- Append a timestamped operator note to sessions/notes.jsonl.
- `note_list` (function) `cli/ops_commands.py:493` `def note_list(rhost, limit)` -- Print recent operator notes, optionally filtered by rhost.
- `LootEntry.value` (method) `cli/ops_commands.py:561` `def value(self)` -- Return the canonical ``user:secret`` credential value.
- `gather_loot` (function) `cli/ops_commands.py:571` `def gather_loot(sessions_dir)` -- Parse every credentials*.txt and hash*.txt under ``sessions_dir``.
- `loot_show` (function) `cli/ops_commands.py:614` `def loot_show(sessions_dir)` -- Print a unified table of all captured credentials and hashes.
- `loot_search` (function) `cli/ops_commands.py:686` `def loot_search(query, sessions_dir)` -- Search captured loot for ``query`` across users and secrets.
- `loot_reuse` (function) `cli/ops_commands.py:763` `def loot_reuse(rhost, sessions_dir)` -- Suggest captured credentials worth trying against ``rhost``.
- `loot_graph` (function) `cli/ops_commands.py:847` `def loot_graph(sessions_dir)` -- Render the credential-centric view of the network graph.
- `resolve_cred_value` (function) `cli/ops_commands.py:917` `def resolve_cred_value(selector, entries)` -- Resolve a user/secret ``selector`` to a canonical credential value.
- `loot_mark` (function) `cli/ops_commands.py:945` `def loot_mark(selector, outcome, host, sessions_dir)` -- Record that a credential worked or was rejected against ``host``.
- `pivot_add` (function) `cli/ops_commands.py:987` `def pivot_add(new_ip, via_ip, note)` -- Record a newly discovered pivot target.
- `pivot_list` (function) `cli/ops_commands.py:1013` `def pivot_list()` -- Print the pivot chain discovered so far.
- `tasks_list` (function) `cli/ops_commands.py:1070` `def tasks_list(status_filter, limit)` -- Print tasks from sessions/tasks.json.
- `tasks_add` (function) `cli/ops_commands.py:1125` `def tasks_add(title, operator)` -- Append a new task to sessions/tasks.json.
- `tasks_done` (function) `cli/ops_commands.py:1146` `def tasks_done(task_id)` -- Mark a task as Done.
- `tasks_start` (function) `cli/ops_commands.py:1166` `def tasks_start(task_id)` -- Mark a task as Started.
- `scans_list` (function) `cli/ops_commands.py:1189` `def scans_list(rhost, sessions_dir)` -- List nmap scan files in sessions/, optionally filtered by rhost.
- `sitrep` (function) `cli/ops_commands.py:1242` `def sitrep(payload, sessions_dir)` -- Print a unified operational situation report.

## cli/output_mode.py
Imported by: `cli/commands/anti_forensics.py`, `cli/commands/ux.py`
- `parse_output_flags` (function) `cli/output_mode.py:43` `def parse_output_flags(args, config)` -- Split output control flags from positional command arguments.
- `strip_ansi` (function) `cli/output_mode.py:65` `def strip_ansi(text)` -- Remove ANSI escape sequences from text.
- `format_output` (function) `cli/output_mode.py:77` `def format_output(data, mode)` -- Render data according to the parsed output mode.
- `dry_run_line` (function) `cli/output_mode.py:98` `def dry_run_line(command)` -- Render the exact shell line that would run without running it.

## cli/palette.py
Imported by: `cli/command_explorer.py`, `cli/command_form.py`, `cli/commands/misc_migrated.py`, `cli/contextual_help.py`, `cli/engagement_hooks.py`, `cli/palette_overlay.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_command_palette.py`
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

## cli/reasoning_stream.py
Depends on: `core/text_utils.py`
Imported by: `cli/commands/orchestration.py`, `cli/dashboard_tui.py`, `tests/test_engage_gates.py`, `tests/test_reasoning_stream.py`
- `read_raw_events` (function) `cli/reasoning_stream.py:91` `def read_raw_events(path, limit)` -- Return the last ``limit`` well-formed events from the JSONL log.
- `event_to_entry` (function) `cli/reasoning_stream.py:183` `def event_to_entry(event)` -- Convert a raw daemon event into a :class:`ReasoningEntry`.
- `latest_reasoning` (function) `cli/reasoning_stream.py:216` `def latest_reasoning(path, limit)` -- Return the most recent daemon decisions as reasoning entries.
- `latest_hint` (function) `cli/reasoning_stream.py:229` `def latest_hint(events_path)` -- Return the newest human-readable reasoning line for spinners.

## cli/recommendation.py
Imported by: `cli/commands/misc_migrated.py`, `cli/recommendation_signals.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_gap_signal.py`, `tests/test_recommendation.py`
- `RecommendationSignal.propose` (method) `cli/recommendation.py:187` `def propose(self, ctx)` -- Return zero or more :class:`Proposal` objects for ``ctx``.
- `CategoryResolver.__init__` (method) `cli/recommendation.py:201` `def __init__(self, index_path, loader)` -- Build the resolver from the command index.
- `CategoryResolver.category_for` (method) `cli/recommendation.py:227` `def category_for(self, action)` -- Return the kill-chain category for ``action`` or an empty string.
- `RecommendationEngine.__init__` (method) `cli/recommendation.py:240` `def __init__(self, signals, resolver, weights)` -- Wire the engine with its signals and fusion parameters.
- `RecommendationEngine.recommend` (method) `cli/recommendation.py:258` `def recommend(self, ctx)` -- Return the fused, ranked recommendations for ``ctx``.
- `_Accumulator.add` (method) `cli/recommendation.py:374` `def add(self, source, contribution, proposal)` -- Fold one signal's proposal into the running total.
- `_Accumulator.build` (method) `cli/recommendation.py:386` `def build(self)` -- Freeze the slot into an immutable :class:`Recommendation`.

## cli/recommendation_signals.py
Depends on: `cli/exploration.py`, `cli/graph_advisor.py`, `cli/reactive_hints.py`, `cli/recommendation.py`, `cli/recon_plan.py`, `core/logging.py`, `modules/apt_playbooks.py`, `skills/lazyown_policy.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/dashboard_tui.py`, `cli/tips_engine.py`, `modules/engage_summary.py`, `skills/lazyown_mcp.py`, `tests/test_evidence_hints.py`, `tests/test_killchain_gap_signal.py`, `tests/test_phase1_data_gaps.py`, `tests/test_recommendation.py`
- `GraphSignal.__init__` (method) `cli/recommendation_signals.py:115` `def __init__(self, advisor)` -- Store the graph advisor facade.
- `GraphSignal.propose` (method) `cli/recommendation_signals.py:125` `def propose(self, ctx)` -- Return graph-adjacent command proposals for ``ctx``.
- `PolicySignal.__init__` (method) `cli/recommendation_signals.py:153` `def __init__(self, policy)` -- Store the policy integration facade.
- `PolicySignal.propose` (method) `cli/recommendation_signals.py:162` `def propose(self, ctx)` -- Return category-prior proposals for ``ctx``.
- `ReconPlanSignal.__init__` (method) `cli/recommendation_signals.py:190` `def __init__(self, engine, builder)` -- Store the exploration engine and the plan builder callable.
- `ReconPlanSignal.propose` (method) `cli/recommendation_signals.py:200` `def propose(self, ctx)` -- Return trigger-matched addon/tool/command proposals for ``ctx``.
- `KillChainSignal.__init__` (method) `cli/recommendation_signals.py:229` `def __init__(self, next_table, phase_table)` -- Store the adjacency and phase-priority tables.
- `KillChainSignal.propose` (method) `cli/recommendation_signals.py:243` `def propose(self, ctx)` -- Return adjacency- and phase-derived proposals for ``ctx``.
- `read_recent_commands` (function) `cli/recommendation_signals.py:275` `def read_recent_commands(sessions_dir, window)` -- Return the last ``window`` command verbs from the session transcript.
- `build_context` (function) `cli/recommendation_signals.py:308` `def build_context(payload, sessions_dir, target, limit)` -- Assemble a :class:`RecommendationContext` from live engagement state.
- `PlaybookSignal.__init__` (method) `cli/recommendation_signals.py:346` `def __init__(self, playbook_engine)` -- Store an optional playbook engine facade.
- `PlaybookSignal.propose` (method) `cli/recommendation_signals.py:355` `def propose(self, ctx)` -- Return playbook-based proposals for the current context.
- `KillchainGapSignal.__init__` (method) `cli/recommendation_signals.py:406` `def __init__(self, sessions_dir)`
- `KillchainGapSignal.propose` (method) `cli/recommendation_signals.py:409` `def propose(self, ctx)` -- Return gap-detection proposals for ``ctx``.
- `GraphTopologySignal.__init__` (method) `cli/recommendation_signals.py:542` `def __init__(self, sessions_dir)`
- `GraphTopologySignal.propose` (method) `cli/recommendation_signals.py:545` `def propose(self, ctx)` -- Return lateral movement and topology proposals from network graph.
- `build_default_engine` (function) `cli/recommendation_signals.py:649` `def build_default_engine(payload, sessions_dir, graph_path, command_index_path, weights)` -- Wire every available deterministic signal into one engine.
- `recommend_with_evidence` (function) `cli/recommendation_signals.py:705` `def recommend_with_evidence(payload, sessions_dir, target, phase, limit, engine)` -- Return fused, ranked recommendations carrying reason and score for display.

## cli/recon_plan.py
Depends on: `cli/exploration.py`, `modules/killchain.py`
Imported by: `cli/lazynmap_post.py`, `cli/recommendation_signals.py`, `tests/test_lazynmap_post.py`, `tests/test_recon_plan.py`
- `ReconPlan.is_empty` (method) `cli/recon_plan.py:139` `def is_empty(self)` -- Return ``True`` when the plan carries no actionable items.
- `build_recon_plan` (function) `cli/recon_plan.py:144` `def build_recon_plan(target, engine, payload, config, command_index_loader, clock)` -- Assemble a :class:`ReconPlan` for ``target`` using ``engine``.
- `render_markdown` (function) `cli/recon_plan.py:207` `def render_markdown(plan)` -- Render ``plan`` as a Markdown document suitable for sessions/.
- `write_plan` (function) `cli/recon_plan.py:257` `def write_plan(plan, sessions_dir, config)` -- Persist ``plan`` to ``sessions/recon_plan_<target>.md`` atomically.
- `render_rich` (function) `cli/recon_plan.py:299` `def render_rich(plan, console)` -- Render ``plan`` to the supplied Rich console.

## cli/registry.py
Depends on: `cli/commands/_dormancy.py`
Imported by: `cli/__init__.py`, `lazyown.py`, `tests/test_cli_command_sets.py`, `tests/test_command_set_migration.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_improvements_spec.py`, `tests/test_nethelpers_command_set.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`
- `iter_command_sets` (function) `cli/registry.py:41` `def iter_command_sets(include_pending)` -- Yield every ``CommandSet`` subclass found under ``cli.commands.*``.
- `register_command_sets` (function) `cli/registry.py:77` `def register_command_sets(shell)` -- Instantiate and register every active ``CommandSet`` on ``shell``.

## cli/scope_guard.py
Depends on: `cli/commands/enum.py`
Imported by: `lazyown.py`, `tests/test_scope_guard.py`
- `ScopeMode.from_value` (method) `cli/scope_guard.py:105` `def from_value(cls, value)` -- Coerce an arbitrary payload value into a :class:`ScopeMode`.
- `build_offensive_commands` (function) `cli/scope_guard.py:147` `def build_offensive_commands(command_categories)` -- Select the command names whose category is offensive.
- `normalize_scope` (function) `cli/scope_guard.py:163` `def normalize_scope(entries)` -- Coerce a scope specification into a tuple of entry strings.
- `target_in_scope` (function) `cli/scope_guard.py:218` `def target_in_scope(target, entries)` -- Return whether *target* falls within any of the scope *entries*.
- `ScopeGuard.__init__` (method) `cli/scope_guard.py:263` `def __init__(self, scope_entries, mode, is_offensive)` -- Initialise the guard.
- `ScopeGuard.evaluate` (method) `cli/scope_guard.py:283` `def evaluate(self, command, target)` -- Evaluate a single command against the active target.

## cli/session_hud.py
Depends on: `cli/engagement_hooks.py`
Imported by: `cli/commands/ux.py`
- `count_lines_in_globs` (function) `cli/session_hud.py:62` `def count_lines_in_globs(root, patterns)` -- Count non-empty lines across every file matching the patterns.
- `count_csv_rows` (function) `cli/session_hud.py:83` `def count_csv_rows(path)` -- Count data rows in a CSV file without loading it fully.
- `format_elapsed` (function) `cli/session_hud.py:100` `def format_elapsed(seconds)` -- Format a duration as HH:MM:SS.
- `phase_bar` (function) `cli/session_hud.py:115` `def phase_bar(phase, width)` -- Render kill-chain progress as filled and empty blocks.
- `build_snapshot` (function) `cli/session_hud.py:155` `def build_snapshot(params, config)` -- Build a snapshot from live params, engagement state and session files.
- `render_snapshot` (function) `cli/session_hud.py:180` `def render_snapshot(snapshot, config)` -- Render the session counters as two plain lines.

## cli/session_resumer.py
Depends on: `core/console.py`, `core/logging.py`
Imported by: `cli/commands/session_ops.py`
- `SessionResumer.__init__` (method) `cli/session_resumer.py:58` `def __init__(self, config)`
- `SessionResumer.render_startup_panel` (method) `cli/session_resumer.py:129` `def render_startup_panel(self)` -- Render the resume panel and return the selected target IP, or None.

## cli/sessions_browser.py
Depends on: `cli/commands/containers.py`, `cli/themes.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_sessions_browser.py`
- `SessionsIndex.__init__` (method) `cli/sessions_browser.py:88` `def __init__(self, config, root)` -- Bind to config and resolve the sessions root.
- `SessionsIndex.root` (method) `cli/sessions_browser.py:100` `def root(self)` -- Return the resolved sessions root.
- `SessionsIndex.categories` (method) `cli/sessions_browser.py:104` `def categories(self)` -- Return a mapping ``category_identifier -> [SessionEntry, ...]``.
- `SessionPreview.__init__` (method) `cli/sessions_browser.py:188` `def __init__(self, config, root)` -- Bind to config and the sessions root.
- `SessionPreview.read` (method) `cli/sessions_browser.py:193` `def read(self, relative)` -- Return ``relative`` as text, capped at ``max_preview_bytes``.
- `SessionsBrowserState.grouped_entries` (method) `cli/sessions_browser.py:233` `def grouped_entries(self)` -- Return classified entries, optionally filtered by :attr:`filter_query`.
- `SessionsBrowserState.category_label` (method) `cli/sessions_browser.py:248` `def category_label(self, identifier)` -- Return the human-readable label for ``identifier``.
- `build_state` (function) `cli/sessions_browser.py:258` `def build_state(payload, sessions_dir, config)` -- Wire the canonical state used by :func:`launch_browser`.
- `launch_browser` (function) `cli/sessions_browser.py:281` `def launch_browser(payload, state, runner)` -- Open the Textual browser and return the last-viewed relative path.
- `_SessionsBrowserApp.__init__` (method) `cli/sessions_browser.py:340` `def __init__(self)`
- `_SessionsBrowserApp.compose` (method) `cli/sessions_browser.py:346` `def compose(self)`
- `_SessionsBrowserApp.on_mount` (method) `cli/sessions_browser.py:356` `def on_mount(self)`
- `_SessionsBrowserApp.on_input_changed` (method) `cli/sessions_browser.py:359` `def on_input_changed(self, event)`
- `_SessionsBrowserApp.on_tree_node_selected` (method) `cli/sessions_browser.py:363` `def on_tree_node_selected(self, event)`
- `_SessionsBrowserApp.action_refresh` (method) `cli/sessions_browser.py:370` `def action_refresh(self)`
- `_SessionsBrowserApp.action_close` (method) `cli/sessions_browser.py:373` `def action_close(self)`

## cli/show.py
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `static/js/bootstrap-4.5.2.min.js`, `static/js/bootstrap-5.3.0.bundle.min.js`, `static/js/chart.min.js`, `static/js/jquery-3.5.1.slim.min.js`, `static/js/quill-2.0.3.js`, `static/js/tippy-6.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `tests/test_cli_assign.py`
- `format_payload` (function) `cli/show.py:14` `def format_payload(params)` -- Render ``params`` as a sorted, aligned ``key = value`` block.

## cli/splash.py
Depends on: `cli/style.py`, `core/console.py`
Imported by: `lazyown.py`, `tests/test_tui_splash.py`
- `SplashEffect.render` (method) `cli/splash.py:71` `def render(self, console, lines, tokens, config)`
- `TypewriterEffect.render` (method) `cli/splash.py:90` `def render(self, console, lines, tokens, config)`
- `InstantEffect.render` (method) `cli/splash.py:150` `def render(self, console, lines, tokens, config)`
- `render_splash` (function) `cli/splash.py:166` `def render_splash(console, lines, payload, config, effect_name)` -- Render the splash overlay and optionally clear the screen.


Next: [API_p5.md](API_p5.md)
