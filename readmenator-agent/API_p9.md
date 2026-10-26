# API (page 9 of 24)
Previous: [API_p8.md](API_p8.md)

## lazygui/widgets/event_log_view.py
Depends on: `lazygui/config/constants.py`, `lazygui/services/event_log.py`, `lazygui/services/models.py`
Imported by: `lazygui/panels/event_log_panel.py`, `lazygui/widgets/__init__.py`
- `EventLogView.__init__` (method) `lazygui/widgets/event_log_view.py:23` `def __init__(self, constants, event_log, parent)` -- Bind the view to ``event_log`` and configure columns/headers.
- `EventLogView.set_minimum_level` (method) `lazygui/widgets/event_log_view.py:51` `def set_minimum_level(self, level)` -- Filter view to records of severity >= ``level`` and reload.
- `EventLogView.minimum_level` (method) `lazygui/widgets/event_log_view.py:61` `def minimum_level(self)` -- Currently active severity filter.

## lazygui/widgets/filter_bar.py
Depends on: `lazygui/config/constants.py`
Imported by: `lazygui/panels/listeners_panel.py`, `lazygui/panels/sessions_panel.py`, `lazygui/widgets/__init__.py`
- `FilterBar.__init__` (method) `lazygui/widgets/filter_bar.py:16` `def __init__(self, constants, placeholder_text, label_text, parent)` -- Lay out a label + line edit and wire up debounce timing.
- `FilterBar.text` (method) `lazygui/widgets/filter_bar.py:42` `def text(self)` -- Current filter text.
- `FilterBar.clear` (method) `lazygui/widgets/filter_bar.py:46` `def clear(self)` -- Reset the filter to an empty string.

## lazygui/widgets/graph_view.py
Depends on: `lazygui/config/constants.py`, `lazygui/services/models.py`
Imported by: `lazygui/panels/graph_panel.py`, `lazygui/widgets/__init__.py`, `tests/test_lazygui_graph_widget.py`
- `GraphNodeItem.__init__` (method) `lazygui/widgets/graph_view.py:143` `def __init__(self, node, radius, color, pixmap, on_selected, on_context_menu, label_visible, parent)`
- `GraphNodeItem.node_data` (method) `lazygui/widgets/graph_view.py:186` `def node_data(self)` -- Return the immutable node data associated with this item.
- `GraphNodeItem.paint` (method) `lazygui/widgets/graph_view.py:190` `def paint(self, painter, option, widget)`
- `GraphNodeItem.mousePressEvent` (method) `lazygui/widgets/graph_view.py:248` `def mousePressEvent(self, event)`
- `GraphNodeItem.mouseReleaseEvent` (method) `lazygui/widgets/graph_view.py:259` `def mouseReleaseEvent(self, event)`
- `GraphNodeItem.hoverEnterEvent` (method) `lazygui/widgets/graph_view.py:266` `def hoverEnterEvent(self, event)`
- `GraphNodeItem.hoverLeaveEvent` (method) `lazygui/widgets/graph_view.py:273` `def hoverLeaveEvent(self, event)`
- `GraphNodeItem.itemChange` (method) `lazygui/widgets/graph_view.py:279` `def itemChange(self, change, value)`
- `GraphEdgeItem.__init__` (method) `lazygui/widgets/graph_view.py:288` `def __init__(self, edge, source_item, target_item, parent)`
- `GraphEdgeItem.update_position` (method) `lazygui/widgets/graph_view.py:324` `def update_position(self)` -- Recalculate the line endpoints from source and target positions.
- `GraphEdgeItem.edge_data` (method) `lazygui/widgets/graph_view.py:329` `def edge_data(self)` -- Return the immutable edge data.
- `GraphScene.__init__` (method) `lazygui/widgets/graph_view.py:340` `def __init__(self, constants, parent)`
- `GraphScene.set_topology` (method) `lazygui/widgets/graph_view.py:349` `def set_topology(self, topology)` -- Replace the current graph with a new topology using force layout.
- `GraphScene.step_physics` (method) `lazygui/widgets/graph_view.py:419` `def step_physics(self)` -- Run one iteration of force-directed layout.
- `GraphScene.selected_node_id` (method) `lazygui/widgets/graph_view.py:491` `def selected_node_id(self)` -- Return the identifier of the first selected node, or None.
- `GraphView.__init__` (method) `lazygui/widgets/graph_view.py:509` `def __init__(self, constants, parent)`
- `GraphView.set_theme_colors` (method) `lazygui/widgets/graph_view.py:527` `def set_theme_colors(self, bg_color, edge_color)` -- Update graph background and default edge colour from theme tokens.
- `GraphView.set_topology` (method) `lazygui/widgets/graph_view.py:535` `def set_topology(self, topology)` -- Render a new graph topology.
- `GraphView.wheelEvent` (method) `lazygui/widgets/graph_view.py:551` `def wheelEvent(self, event)`
- `GraphView.selected_node_id` (method) `lazygui/widgets/graph_view.py:561` `def selected_node_id(self)` -- Return the identifier of the currently selected node.
- `GraphView.fit_to_content` (method) `lazygui/widgets/graph_view.py:565` `def fit_to_content(self)` -- Zoom to fit all graph content.
- `GraphView.scene_handle` (method) `lazygui/widgets/graph_view.py:570` `def scene_handle(self)` -- Return the underlying graph scene.

## lazygui/widgets/status_badge.py
Depends on: `lazygui/services/backend.py`
Imported by: `lazygui/widgets/__init__.py`, `lazygui/windows/main_window.py`
- `StatusBadge.__init__` (method) `lazygui/widgets/status_badge.py:21` `def __init__(self, parent)` -- Create the badge in the disconnected state.
- `StatusBadge.set_status` (method) `lazygui/widgets/status_badge.py:27` `def set_status(self, status)` -- Update label text and the object name driving QSS colour.

## lazygui/widgets/terminal_view.py
Depends on: `lazygui/config/constants.py`
Imported by: `lazygui/panels/terminal_panel.py`, `lazygui/widgets/__init__.py`
- `TerminalView.__init__` (method) `lazygui/widgets/terminal_view.py:38` `def __init__(self, constants, parent)` -- Configure the widget for log-style append-only behaviour.
- `TerminalView.append_output` (method) `lazygui/widgets/terminal_view.py:54` `def append_output(self, text)` -- Append ``text`` after stripping ANSI control codes and control chars.
- `TerminalView.keyPressEvent` (method) `lazygui/widgets/terminal_view.py:75` `def keyPressEvent(self, event)` -- Forward keystrokes to listeners instead of mutating the buffer.

## lazygui/windows/command_palette_window.py
Depends on: `lazygui/config/constants.py`, `lazygui/widgets/command_palette_list.py`
Imported by: `lazygui/windows/__init__.py`, `lazygui/windows/main_window.py`
- `CommandPaletteWindow.__init__` (method) `lazygui/windows/command_palette_window.py:18` `def __init__(self, constants, actions, parent)` -- Build the search input plus the result list.
- `CommandPaletteWindow.set_actions` (method) `lazygui/windows/command_palette_window.py:43` `def set_actions(self, actions)` -- Replace the action set on the underlying list.
- `CommandPaletteWindow.keyPressEvent` (method) `lazygui/windows/command_palette_window.py:48` `def keyPressEvent(self, event)` -- Intercept Enter and Esc, otherwise delegate to the search box.
- `CommandPaletteWindow.showEvent` (method) `lazygui/windows/command_palette_window.py:71` `def showEvent(self, event)` -- Move keyboard focus into the search box on every open.

## lazygui/windows/connect_dialog.py
Depends on: `lazygui/config/c2_credentials.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/services/models.py`, `lazygui/services/teamserver_backend.py`
Imported by: `lazygui/app.py`, `lazygui/windows/__init__.py`
- `ConnectDialog.__init__` (method) `lazygui/windows/connect_dialog.py:53` `def __init__(self, constants, settings, paths, parent)` -- Build the form and pre-fill from persisted settings + credentials file.
- `ConnectDialog.request` (method) `lazygui/windows/connect_dialog.py:105` `def request(self)` -- Translate current widget state into a :class:`ConnectionRequest`.
- `ConnectDialog.persist_choice` (method) `lazygui/windows/connect_dialog.py:120` `def persist_choice(self)` -- Save the picked values back into :class:`AppSettings`.

## lazygui/windows/main_window.py
Depends on: `lazygui/config/constants.py`, `lazygui/config/settings.py`, `lazygui/panels/registry.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/models.py`, `lazygui/theme/manager.py`, `lazygui/theme/tokens.py`, `lazygui/widgets/beacon_command_modal.py`, `lazygui/widgets/command_palette_list.py`, `lazygui/widgets/status_badge.py`, `lazygui/windows/command_palette_window.py`
Imported by: `lazygui/app.py`, `lazygui/windows/__init__.py`
- `MainWindow.__init__` (method) `lazygui/windows/main_window.py:40` `def __init__(self, constants, settings, theme_manager, backend, event_log, parent)` -- Wire the dependencies and build the full layout.
- `MainWindow.closeEvent` (method) `lazygui/windows/main_window.py:99` `def closeEvent(self, event)` -- Persist geometry, layout and theme before closing.
- `MainWindow.window_requests_connect` (method) `lazygui/windows/main_window.py:376` `def window_requests_connect(self)` -- Hook overridden by :class:`Application` to swap backend at runtime.
- `MainWindow.status_badge` (method) `lazygui/windows/main_window.py:393` `def status_badge(self)` -- Expose the badge so the application can update it on backend swaps.
- `MainWindow.panels` (method) `lazygui/windows/main_window.py:398` `def panels(self)` -- Expose the panel registry for backend swaps.

## lazyown-docker/hostdiscover.sh
- `extract_ips_from_arp` (function) `lazyown-docker/hostdiscover.sh:21`
- `extract_listening_ips_from_netstat` (function) `lazyown-docker/hostdiscover.sh:26`

## lazyown-docker/mkdocker.sh
- `usage` (function) `lazyown-docker/mkdocker.sh:23` -- Help message
- `log` (function) `lazyown-docker/mkdocker.sh:36` -- Log function
- `check_docker` (function) `lazyown-docker/mkdocker.sh:41` -- Check if Docker is running
- `check_file` (function) `lazyown-docker/mkdocker.sh:49` -- Check if file exists
- `container_exists` (function) `lazyown-docker/mkdocker.sh:58` -- Check if container exists
- `image_exists` (function) `lazyown-docker/mkdocker.sh:63` -- Check if image exists
- `get_ports` (function) `lazyown-docker/mkdocker.sh:68` -- Get ports from payload.json
- `build_image` (function) `lazyown-docker/mkdocker.sh:93` -- Build Docker image
- `validate_payload` (function) `lazyown-docker/mkdocker.sh:109` -- Validate payload.json exists
- `run_container` (function) `lazyown-docker/mkdocker.sh:117` -- Run container
- `stop_container` (function) `lazyown-docker/mkdocker.sh:187` -- Stop container
- `clean_container_and_image` (function) `lazyown-docker/mkdocker.sh:197` -- Clean container and image

## lazyown.py
Depends on: `cli/aliases.py`, `cli/auto_crypto.py`, `cli/autosuggest.py`, `cli/chain_mode.py`, `cli/cli_enhancements.py`, `cli/command_chain.py`, `cli/engagement_hooks.py`, `cli/exploration.py`, `cli/fuzzy_picker.py`, `cli/graph_advisor.py`, `cli/headless.py`, `cli/lazynmap_post.py`, `cli/ops_commands.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/protips.py`, `cli/reactive_hints.py`, `cli/registry.py`, `cli/scope_guard.py`, `cli/session_brief.py`, `cli/splash.py`, `cli/status_bar.py`, `cli/tips_engine.py`, `cli/toast_bus.py`, `core/autonomous.py`, `core/config.py`, `core/console.py`, `core/credential_vault.py`, `core/defaults.py`, `core/hardening.py`, `core/logging.py`, `core/param_registry.py`, `modules/cli_auth.py`, `modules/command_executor.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/gym_cleanup.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/logging_config.py`, `modules/metrics.py`, `modules/payload_factory.py`, `modules/session_cleanup.py`, `modules/state_manager.py`, `modules/unified_bridge.py`, `skills/unified_orchestrator.py`, `utils.py`
Imported by: `core/command_bridge.py`, `discord_c2.py`, `lazyc2.py`, `poc_tui/app.py`, `scripts/devtools/command_audit.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_c2_agent.py`, `tests/test_scope_guard_integration.py`
- `_PayloadSettableProxy.__init__` (method) `lazyown.py:244` `def __init__(self, params)` -- Bind the proxy to a live ``params`` dictionary.
- `LazyOwnShell.__init__` (method) `lazyown.py:372` `def __init__(self)` -- Initializer for the LazyOwnShell class.
- `LazyOwnShell.log_command` (method) `lazyown.py:786` `def log_command(self, cmd_name, cmd_args, start_time, end_time, duration_ms)` -- Logs the command execution details to a CSV file.
- `LazyOwnShell.default` (method) `lazyown.py:849` `def default(self, line)` -- Handles undefined commands, including aliases.
- `LazyOwnShell.scripts` (method) `lazyown.py:878` `def scripts(self)` -- Auto-discovered list of runnable script names.
- `LazyOwnShell.refresh_prompt` (method) `lazyown.py:897` `def refresh_prompt(self)` -- Recompute the Neon Box prompt from the live payload.
- `LazyOwnShell.do_set` (method) `lazyown.py:908` `def do_set(self, line)` -- Set a parameter — the unified ``set``/``assign`` surface.
- `LazyOwnShell.logcsv` (method) `lazyown.py:1301` `def logcsv(self, line, start_time, end_time, duration_ms)` -- Forward a command line to :meth:`log_command` for CSV persistence.
- `LazyOwnShell.cmd` (method) `lazyown.py:1342` `def cmd(self, line)` -- Internal function to execute commands.
- `LazyOwnShell.onecmd_plus_hooks` (method) `lazyown.py:1434` `def onecmd_plus_hooks(self, statement, add_to_history, raise_keyboard_interrupt, orig_rl_history_length)` -- Dispatch a command, expanding payload placeholders in custom aliases.
- `LazyOwnShell.one_cmd` (method) `lazyown.py:1798` `def one_cmd(self, command)` -- Internal function to execute commands.
- `LazyOwnShell.emptyline` (method) `lazyown.py:1844` `def emptyline(self)` -- Handle the case where the user enters an empty line.
- `LazyOwnShell.load_user_commands` (method) `lazyown.py:1869` `def load_user_commands(self)` -- Carga los comandos personalizados desde user_commands.json
- `LazyOwnShell.save_user_command` (method) `lazyown.py:1881` `def save_user_command(self, alias, command)` -- Guarda un nuevo comando en user_commands.json
- `LazyOwnShell.list_files_in_directory` (method) `lazyown.py:1893` `def list_files_in_directory(self, directory)` -- Lista todos los archivos en un directorio dado.
- `LazyOwnShell.register_tool_commands` (method) `lazyown.py:1899` `def register_tool_commands(self)` -- Register every active ``tools/*.tool`` as a ``do_<toolname>`` command.
- `make_wrapper` (function) `lazyown.py:1958` `def make_wrapper(cmd_template, tname, default_target)`
- `tool_wrapper` (function) `lazyown.py:1959` `def tool_wrapper(arg)`
- `wrapper` (function) `lazyown.py:2060` `def wrapper(arg)`
- `LazyOwnShell.load_plugins` (method) `lazyown.py:2083` `def load_plugins(self)` -- Load every Lua plugin from the 'plugins/' directory.
- `LazyOwnShell.load_yaml_plugins` (method) `lazyown.py:2113` `def load_yaml_plugins(self)` -- Loads all YAML plugins from the 'lazyaddons/' directory.
- `LazyOwnShell.register_yaml_plugin` (method) `lazyown.py:2136` `def register_yaml_plugin(self, plugin_data)` -- Register a YAML addon as a shell command.
- `wrapper_yaml` (function) `lazyown.py:2176` `def wrapper_yaml(arg)`
- `LazyOwnShell.register_all_adversary_commands` (method) `lazyown.py:2282` `def register_all_adversary_commands(self)`
- `cmd_wrapper` (function) `lazyown.py:2304` `def cmd_wrapper(_)`
- `LazyOwnShell.display_toastr` (method) `lazyown.py:2311` `def display_toastr(self, message, type)` -- Display the unified toastr panel from the shared toast bus.
- `LazyOwnShell.completedefault` (method) `lazyown.py:2324` `def completedefault(self, text, line, begidx, endidx)` -- Fall through to the payload-aware completer for unhandled commands.
- `LazyOwnShell.preloop` (method) `lazyown.py:2349` `def preloop(self)` -- Print a session-start pro tip and handle first-run setup.
- `LazyOwnShell.postparsing_precmd` (method) `lazyown.py:2493` `def postparsing_precmd(self, statement)` -- Gate unauthenticated commands — anonymous operators can only run ``register``, ``login``, ``logout``, ``whoami``...
- `LazyOwnShell.postloop` (method) `lazyown.py:2521` `def postloop(self)` -- Handle operations to perform after exiting the command loop.
- `LazyOwnShell.complete_phase` (method) `lazyown.py:2554` `def complete_phase(self, text, line, begidx, endidx)` -- Tab-complete phase names.
- `LazyOwnShell.complete_l00t` (method) `lazyown.py:2559` `def complete_l00t(self, text, line, begidx, endidx)` -- Tab-complete l00t subcommands.
- `LazyOwnShell.complete_loot` (method) `lazyown.py:2565` `def complete_loot(self, text, line, begidx, endidx)` -- Tab-complete loot subcommands (delegates to l00t).
- `LazyOwnShell.complete_assign` (method) `lazyown.py:2570` `def complete_assign(self, text, line, begidx, endidx)` -- Tab-complete the parameter name from the live payload keys.
- `LazyOwnShell.complete_scope` (method) `lazyown.py:2587` `def complete_scope(self, text, line, begidx, endidx)` -- Tab-complete the scope subcommands.
- `LazyOwnShell.complete_palette` (method) `lazyown.py:2638` `def complete_palette(self, text, line, begidx, endidx)` -- Tab-complete the palette command using the live command index.
- `LazyOwnShell.run_lazysearch` (method) `lazyown.py:2655` `def run_lazysearch(self)` -- Runs the internal module `modules/lazysearch.py`.
- `LazyOwnShell.run_lazysearch_gui` (method) `lazyown.py:2672` `def run_lazysearch_gui(self)` -- Run the internal module located at `modules/LazyOwnExplorer.py`.
- `LazyOwnShell.run_lazyown` (method) `lazyown.py:2702` `def run_lazyown(self)` -- Run the internal module located at `modules/lazyown_parquet_tool.py`.
- `LazyOwnShell.run_update_db` (method) `lazyown.py:2728` `def run_update_db(self)` -- Run the internal module located at `modules/update_db.sh`.
- `LazyOwnShell.run_lazynmap` (method) `lazyown.py:2758` `def run_lazynmap(self)` -- Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.
- `LazyOwnShell.run_lazywerkzeugdebug` (method) `lazyown.py:2823` `def run_lazywerkzeugdebug(self)` -- Run the internal module located at `modules/legacy/lazywerkzeug.py` in debug mode.
- `LazyOwnShell.run_lazygath` (method) `lazyown.py:2880` `def run_lazygath(self)` -- Run the internal module located at `modules/lazygat.sh`. to gathering the sistem :)
- `LazyOwnShell.run_lazynmapdiscovery` (method) `lazyown.py:2912` `def run_lazynmapdiscovery(self)` -- Runs the internal module `modules/lazynmap.sh` with discovery mode.
- `LazyOwnShell.run_lazysniff` (method) `lazyown.py:2927` `def run_lazysniff(self)` -- Run the sniffer internal module located at `modules/legacy/lazysniff.py` with the specified parameters.
- `LazyOwnShell.run_lazyftpsniff` (method) `lazyown.py:2976` `def run_lazyftpsniff(self)` -- Run the sniffer ftp internal module located at `modules/legacy/lazyftpsniff.py` with the specified parameters.
- `LazyOwnShell.run_lazynetbios` (method) `lazyown.py:3022` `def run_lazynetbios(self)` -- Run the internal module to search netbios vuln victims, located at `modules/legacy/lazynetbios.py` with the...
- `LazyOwnShell.run_lazyhoneypot` (method) `lazyown.py:3073` `def run_lazyhoneypot(self)` -- Run the internal module located at `modules/legacy/lazyhoneypot.py` with the specified parameters.
- `LazyOwnShell.run_lazysearch_bot` (method) `lazyown.py:3139` `def run_lazysearch_bot(self)` -- Run the internal module GROQ AI located at `modules/legacy/lazysearch_bot.py` with the specified parameters.
- `LazyOwnShell.run_lazymetaextract0r` (method) `lazyown.py:3190` `def run_lazymetaextract0r(self)` -- Run the Metadata extractor internal module located at `modules/lazyown_metaextract0r.py` with the specified parameters.
- `LazyOwnShell.run_lazylfi2rce` (method) `lazyown.py:3231` `def run_lazylfi2rce(self)` -- Run the internal module located at `modules/legacy/lazylfi2rce.py` with the specified parameters.
- `LazyOwnShell.run_lazylogpoisoning` (method) `lazyown.py:3312` `def run_lazylogpoisoning(self)` -- Run the internal module located at `modules/legacy/lazylogpoisoning.py` with the specified parameters.
- `LazyOwnShell.run_lazyssh77enum` (method) `lazyown.py:3359` `def run_lazyssh77enum(self)` -- Run the internal module located at `modules/lazybrutesshuserenum.py` with the specified parameters.
- `LazyOwnShell.run_lazyburpfuzzer` (method) `lazyown.py:3409` `def run_lazyburpfuzzer(self)` -- Run the internal module located at `modules/lazyown_burpfuzzer.py` with the specified parameters.
- `LazyOwnShell.run_lazyreverse_shell` (method) `lazyown.py:3535` `def run_lazyreverse_shell(self)` -- Run the internal module located at `modules/lazyreverse_shell.sh` with the specified parameters.
- `LazyOwnShell.run_lazyarpspoofing` (method) `lazyown.py:3585` `def run_lazyarpspoofing(self)` -- Run the internal module located at `modules/legacy/lazyarpspoofing.py` with the specified parameters.
- `LazyOwnShell.run_lazyattack` (method) `lazyown.py:3639` `def run_lazyattack(self)` -- Run the internal module located at `modules/lazyatack.sh` with the specified parameters.
- `LazyOwnShell.run_lazymsfvenom` (method) `lazyown.py:3694` `def run_lazymsfvenom(self)` -- Executes the `msfvenom` tool to generate a variety of payloads based on user input.
- `LazyOwnShell.run_lazyaslrcheck` (method) `lazyown.py:3871` `def run_lazyaslrcheck(self)` -- Creates a path hijacking attack by performing the following steps:
- `LazyOwnShell.run_lazypathhijacking` (method) `lazyown.py:3918` `def run_lazypathhijacking(self)` -- Creates a path hijacking attack by performing the following steps:
- `LazyOwnShell.run_script` (method) `lazyown.py:3951` `def run_script(self, script_name)` -- Run a script with the given arguments
- `LazyOwnShell.run_command` (method) `lazyown.py:3983` `def run_command(self, command)` -- Run a command and print output in real-time
- `LazyOwnShell.get_output` (method) `lazyown.py:4063` `def get_output(self)` -- Devuelve la salida acumulada
- `LazyOwnShell.upload_file_to_c2` (method) `lazyown.py:4068` `def upload_file_to_c2(self, file_path, clientid)` -- Sube un archivo al C2.
- `LazyOwnShell.complete_upload_c2` (method) `lazyown.py:4094` `def complete_upload_c2(self, text, line, begidx, endidx)` -- Autocomplete implant names from implant_config_*.json files in sessions/ directory
- `LazyOwnShell.download_file_from_c2` (method) `lazyown.py:4122` `def download_file_from_c2(self, file_name, clientid)` -- Descarga un archivo desde el C2.
- `LazyOwnShell.issue_command_to_c2` (method) `lazyown.py:4191` `def issue_command_to_c2(self, command, client_id)` -- Ejecuta un comando en el cliente usando el C2.
- `LazyOwnShell.complete_issue_command_to_c2` (method) `lazyown.py:4225` `def complete_issue_command_to_c2(self, text, line, begidx, endidx)` -- Autocomplete: 1st arg = implant name, 2nd arg = beacon command (with : if needed)
- `LazyOwnShell.view_code` (method) `lazyown.py:4291` `def view_code(self, stdscr)` -- Display C and ASM code side by side in a curses-based interface.
- `LazyOwnShell.get_available_actions` (method) `lazyown.py:4396` `def get_available_actions(self)` -- Returns a list of available actions using cmd2 introspection.
- `LazyOwnShell.process_scan_csv` (method) `lazyown.py:4479` `def process_scan_csv(self, csv_file, ip, port, all_data, processed_ips)` -- Processes a single scan CSV file.
- `LazyOwnShell.process_vuln_csv` (method) `lazyown.py:4502` `def process_vuln_csv(self, csv_file, ip, all_data, processed_ips)` -- Processes a single vulnerability CSV file.
- `LazyOwnShell.do_event_log` (method) `lazyown.py:4634` `def do_event_log(self, line)` -- Show recent EventBus events.
- `LazyOwnShell.do_state_snapshot` (method) `lazyown.py:4664` `def do_state_snapshot(self, line)` -- Show unified StateManager snapshot (DB + JSON caches).
- `LazyOwnShell.do_route` (method) `lazyown.py:4703` `def do_route(self, line)` -- Route a natural-language prompt to a LazyOwn tool.
- `main` (function) `lazyown.py:4726` `def main()`

## modules/49803.py
- `auth` (function) `modules/49803.py:43` `def auth()`
- `injection` (function) `modules/49803.py:69` `def injection()`
- `connection` (function) `modules/49803.py:106` `def connection()`

## modules/CVE-2023-28432.py
- `poc` (function) `modules/CVE-2023-28432.py:12` `def poc(url)`

## modules/LazyOwnExplorer.py
- `AutocompleteEntry.__init__` (method) `modules/LazyOwnExplorer.py:31` `def __init__(self, get_suggestions_func)`
- `AutocompleteEntry.changed` (method) `modules/LazyOwnExplorer.py:45` `def changed(self, name, index, mode)`
- `AutocompleteEntry.selection` (method) `modules/LazyOwnExplorer.py:68` `def selection(self, event)`
- `AutocompleteEntry.move_up` (method) `modules/LazyOwnExplorer.py:75` `def move_up(self, event)`
- `AutocompleteEntry.move_down` (method) `modules/LazyOwnExplorer.py:87` `def move_down(self, event)`
- `AutocompleteEntry.comparison` (method) `modules/LazyOwnExplorer.py:99` `def comparison(self, pattern)`
- `LazyOwnGUI.__init__` (method) `modules/LazyOwnExplorer.py:105` `def __init__(self)`
- `LazyOwnGUI.create_widgets` (method) `modules/LazyOwnExplorer.py:119` `def create_widgets(self)`
- `get_suggestions` (function) `modules/LazyOwnExplorer.py:124` `def get_suggestions(term)`
- `LazyOwnGUI.load_parquet_files` (method) `modules/LazyOwnExplorer.py:181` `def load_parquet_files(self)`
- `LazyOwnGUI.get_unique_values` (method) `modules/LazyOwnExplorer.py:241` `def get_unique_values(self)`
- `LazyOwnGUI.search` (method) `modules/LazyOwnExplorer.py:248` `def search(self)`
- `LazyOwnGUI.search_in_parquet` (method) `modules/LazyOwnExplorer.py:267` `def search_in_parquet(self, term)`
- `LazyOwnGUI.on_row_double_click` (method) `modules/LazyOwnExplorer.py:278` `def on_row_double_click(self, event)`
- `LazyOwnGUI.show_row_details` (method) `modules/LazyOwnExplorer.py:283` `def show_row_details(self, row)`
- `LazyOwnGUI.add_new_attack_vector` (method) `modules/LazyOwnExplorer.py:305` `def add_new_attack_vector(self)`
- `save_new_vector` (function) `modules/LazyOwnExplorer.py:325` `def save_new_vector()`
- `LazyOwnGUI.scan_system_for_binaries` (method) `modules/LazyOwnExplorer.py:357` `def scan_system_for_binaries(self)`
- `is_binary` (function) `modules/LazyOwnExplorer.py:358` `def is_binary(file_path)`
- `LazyOwnGUI.show_scan_results` (method) `modules/LazyOwnExplorer.py:374` `def show_scan_results(self, binaries)`
- `LazyOwnGUI.export_to_csv` (method) `modules/LazyOwnExplorer.py:385` `def export_to_csv(self)`

## modules/adcs_attacks.py
Imported by: `cli/commands/exploit_migrated.py`
- `CertificateTemplate.esc_vulnerabilities` (method) `modules/adcs_attacks.py:35` `def esc_vulnerabilities(self)` -- Determine which ESC attack paths apply to this template.
- `ADCSCertipyWrapper.__init__` (method) `modules/adcs_attacks.py:80` `def __init__(self, certipy_path, timeout)`
- `ADCSCertipyWrapper.find_certificate_authorities` (method) `modules/adcs_attacks.py:113` `def find_certificate_authorities(self, username, password, domain, dc_ip, hashes)` -- Enumerate certificate authorities in an Active Directory domain.
- `ADCSCertipyWrapper.enumerate_templates` (method) `modules/adcs_attacks.py:189` `def enumerate_templates(self, username, password, domain, dc_ip, hashes)` -- Enumerate vulnerable certificate templates.
- `ADCSCertipyWrapper.request_certificate_esc1` (method) `modules/adcs_attacks.py:268` `def request_certificate_esc1(self, username, password, domain, dc_ip, ca_name, template_name, target_user, output_file)` -- ESC1: Request a certificate with a user-supplied subject alternative name.
- `ADCSCertipyWrapper.request_certificate_esc8` (method) `modules/adcs_attacks.py:322` `def request_certificate_esc8(self, username, password, domain, dc_ip, ca_server, template_name, output_file)` -- ESC8: HTTP-based certificate enrollment (NTLM relay to AD CS).
- `ADCSCertipyWrapper.authenticate_with_certificate` (method) `modules/adcs_attacks.py:367` `def authenticate_with_certificate(self, cert_file, domain, dc_ip, username)` -- Authenticate to the domain using a certificate and retrieve NT hash.
- `ADCSCertipyWrapper.assess_vulnerability` (method) `modules/adcs_attacks.py:411` `def assess_vulnerability(self, username, password, domain, dc_ip, hashes)` -- Run a full AD CS vulnerability assessment.

## modules/addon_updater.py
Depends on: `core/logging.py`
Imported by: `cli/commands/lazyops.py`, `cli/commands/marketplace.py`, `tests/test_addon_updater.py`
- `AddonUpdateResult.to_dict` (method) `modules/addon_updater.py:46` `def to_dict(self)` -- Return a JSON-serializable view.
- `load_addons` (function) `modules/addon_updater.py:73` `def load_addons(lazyaddons_dir)` -- Load every lazyaddon with its update metadata.
- `update_addon` (function) `modules/addon_updater.py:166` `def update_addon(name, lazyaddons_dir, root, dry_run)` -- Update one addon through ``git pull --ff-only``.
- `update_all` (function) `modules/addon_updater.py:260` `def update_all(names, lazyaddons_dir, root, dry_run, audit_path)` -- Update every opted-in addon or an explicit name list.

## modules/agent_runner.py
Depends on: `core/logging.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
Imported by: `modules/lazy_agent.py`, `modules/vulnbot.py`, `tests/test_lazy_streaming.py`
- `configure_logging` (function) `modules/agent_runner.py:60` `def configure_logging(debug)`
- `AgentTool.__init__` (method) `modules/agent_runner.py:69` `def __init__(self, name, description, func, parameters, required)`
- `AgentTool.to_api_format` (method) `modules/agent_runner.py:77` `def to_api_format(self)`
- `AgentTool.execute` (method) `modules/agent_runner.py:83` `def execute(self)` -- Execute with argument validation and clear formatting.
- `ASTToolExtractor.extract_commands_from_file` (method) `modules/agent_runner.py:138` `def extract_commands_from_file(file_path, prefix)`
- `AgentRunner.__init__` (method) `modules/agent_runner.py:193` `def __init__(self, model, system_prompt, max_iterations)`
- `AgentRunner.register_tool` (method) `modules/agent_runner.py:218` `def register_tool(self, tool)`
- `AgentRunner.register_tool_from_instance` (method) `modules/agent_runner.py:221` `def register_tool_from_instance(self, func)` -- Wrap a plain function as an AgentTool using its signature and docstring.
- `AgentRunner.register_tools_from_metadata` (method) `modules/agent_runner.py:239` `def register_tools_from_metadata(self, commands, executor)`
- `make_executor` (function) `modules/agent_runner.py:243` `def make_executor(cmd_name)`
- `wrapper` (function) `modules/agent_runner.py:244` `def wrapper(command)`
- `AgentRunner.get_tools_for_api` (method) `modules/agent_runner.py:266` `def get_tools_for_api(self)`
- `AgentRunner.run` (method) `modules/agent_runner.py:271` `def run(self, user_input)`
- `LazyOwnShellWrapper.__init__` (method) `modules/agent_runner.py:485` `def __init__(self, script_path)`
- `LazyOwnShellWrapper.execute_command` (method) `modules/agent_runner.py:515` `def execute_command(self, command)` -- Execute a command with a timeout using threading.
- `target` (function) `modules/agent_runner.py:522` `def target()`
- `LazyOwnShellWrapper.get_commands_summary` (method) `modules/agent_runner.py:552` `def get_commands_summary(self)`
- `VulnBotCLI.__init__` (method) `modules/agent_runner.py:560` `def __init__(self, provider, mode, debug, script_path)`
- `VulnBotCLI.process_request` (method) `modules/agent_runner.py:615` `def process_request(self, user_input)`
- `interactive_mode` (function) `modules/agent_runner.py:620` `def interactive_mode(bot)`
- `parse_args` (function) `modules/agent_runner.py:644` `def parse_args()`
- `main` (function) `modules/agent_runner.py:654` `def main()`

## modules/ai_exploit_chain.py
Depends on: `modules/autonomous_exploit_engine.py`
Imported by: `cli/commands/pwn.py`, `skills/lazyown_mcp.py`
- `AIExploitChainer.__init__` (method) `modules/ai_exploit_chain.py:259` `def __init__(self)`
- `AIExploitChainer.reason` (method) `modules/ai_exploit_chain.py:285` `def reason(self, context)` -- Analyze context failures and produce the next best exploit candidate.
- `AIExploitChainer.evaluate_failure` (method) `modules/ai_exploit_chain.py:306` `def evaluate_failure(result)` -- Classify the reason for an exploit failure by output pattern matching.
- `AIExploitChainer.select_next_strategy` (method) `modules/ai_exploit_chain.py:318` `def select_next_strategy(self, context)` -- Select the next strategy to attempt based on context and failures.
- `AIExploitChainer.estimate_confidence` (method) `modules/ai_exploit_chain.py:349` `def estimate_confidence(self, strategy, profile)` -- Estimate confidence (0.0-1.0) for a strategy against a target profile.
- `AIExploitChainer.build_chain_plan` (method) `modules/ai_exploit_chain.py:391` `def build_chain_plan(self, context)` -- Build a full multi-step exploitation plan following the kill chain.
- `AIExploitChainer.adapt_chain` (method) `modules/ai_exploit_chain.py:428` `def adapt_chain(self, context, new_info)` -- Adapt the chain plan based on newly discovered information.

## modules/ai_fallback.py
Depends on: `modules/llm_factory.py`, `modules/toposwarm_bridge.py`
Imported by: `modules/recommender.py`, `modules/timeline_narrator.py`
- `call` (function) `modules/ai_fallback.py:254` `def call(prompt, system, api_key, max_tokens, temperature)` -- Call Groq → fallback to Ollama → fallback to TopoSwarm local brain → error.

## modules/ai_model.py
Depends on: `core/logging.py`, `modules/llm_factory.py`
Imported by: `contrib/legacy/lazyllmchat.py`, `modules/agent_runner.py`, `modules/llm_client.py`, `modules/llm_factory.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`
- `AIModel.generate` (method) `modules/ai_model.py:56` `def generate(self, prompt)` -- Return a non-streaming completion for ``prompt``.
- `AIModel.stream_generate` (method) `modules/ai_model.py:60` `def stream_generate(self, prompt)` -- Yield streaming completion chunks for ``prompt``.
- `AIModel.complete` (method) `modules/ai_model.py:63` `def complete(self, system, user, max_tokens, temperature)` -- Return a completion conforming to ``core.protocols.LLMBackend``.
- `_LazyImporter.groq` (method) `modules/ai_model.py:105` `def groq(cls)`
- `_LazyImporter.openai` (method) `modules/ai_model.py:113` `def openai(cls)`
- `_LazyImporter.anthropic` (method) `modules/ai_model.py:121` `def anthropic(cls)`
- `GroqModel.__init__` (method) `modules/ai_model.py:137` `def __init__(self, api_key, model)`
- `GroqModel.generate` (method) `modules/ai_model.py:155` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `GroqModel.stream_generate` (method) `modules/ai_model.py:183` `def stream_generate(self, prompt)` -- Yield streamed completion chunks for ``prompt``.
- `GroqModel.complete` (method) `modules/ai_model.py:216` `def complete(self, system, user, max_tokens, temperature)` -- Return a chat completion using native role separation.
- `OllamaModel.__init__` (method) `modules/ai_model.py:252` `def __init__(self, model, host)`
- `OllamaModel.generate` (method) `modules/ai_model.py:260` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `OllamaModel.stream_generate` (method) `modules/ai_model.py:281` `def stream_generate(self, prompt)` -- Yield streamed completion chunks for ``prompt``.
- `LlamaCppModel.__init__` (method) `modules/ai_model.py:324` `def __init__(self, model, host)`
- `LlamaCppModel.generate` (method) `modules/ai_model.py:362` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `LlamaCppModel.stream_generate` (method) `modules/ai_model.py:382` `def stream_generate(self, prompt)` -- Yield streamed completion deltas for ``prompt``.
- `LlamaCppModel.complete` (method) `modules/ai_model.py:413` `def complete(self, system, user, max_tokens, temperature)` -- Role-aware completion through the chat endpoint.
- `OpenAIModel.__init__` (method) `modules/ai_model.py:440` `def __init__(self, api_key, model)`
- `OpenAIModel.generate` (method) `modules/ai_model.py:444` `def generate(self, prompt)`
- `OpenAIModel.stream_generate` (method) `modules/ai_model.py:455` `def stream_generate(self, prompt)`
- `OpenAIModel.complete` (method) `modules/ai_model.py:470` `def complete(self, system, user, max_tokens, temperature)`
- `AnthropicModel.__init__` (method) `modules/ai_model.py:499` `def __init__(self, api_key, model)`
- `AnthropicModel.generate` (method) `modules/ai_model.py:503` `def generate(self, prompt)`
- `AnthropicModel.stream_generate` (method) `modules/ai_model.py:515` `def stream_generate(self, prompt)`
- `AnthropicModel.complete` (method) `modules/ai_model.py:529` `def complete(self, system, user, max_tokens, temperature)`
- `DeepSeekModel.__init__` (method) `modules/ai_model.py:556` `def __init__(self, api_key, model)`
- `DeepSeekModel.generate` (method) `modules/ai_model.py:563` `def generate(self, prompt)`
- `DeepSeekModel.stream_generate` (method) `modules/ai_model.py:574` `def stream_generate(self, prompt)`
- `DeepSeekModel.complete` (method) `modules/ai_model.py:589` `def complete(self, system, user, max_tokens, temperature)`

## modules/amsi.c
- `LoadNtFunctions` (function) `modules/amsi.c:38` `void LoadNtFunctions()` -- Función para cargar las funciones dinámicamente
- `AMS1patch_OpenSession_jne` (function) `modules/amsi.c:66` `void AMS1patch_OpenSession_jne(HANDLE hproc)` -- Técnica de Saad, también conocido como @D1rkMtr (https://twitter.com/D1rkMtr/)...
- `AMS1patch_OpenSession_ret` (function) `modules/amsi.c:116` `void AMS1patch_OpenSession_ret(HANDLE hproc)`
- `AMS1patch_ScanBuffer_ret` (function) `modules/amsi.c:166` `void AMS1patch_ScanBuffer_ret(HANDLE hproc)`
- `AMS1patch_RastaMouse` (function) `modules/amsi.c:215` `void AMS1patch_RastaMouse(HANDLE hproc)`
- `AMS1patch_E_ACCESSDENIED` (function) `modules/amsi.c:274` `void AMS1patch_E_ACCESSDENIED(HANDLE hproc)`
- `AMS1patch_E_HANDLE` (function) `modules/amsi.c:326` `void AMS1patch_E_HANDLE(HANDLE hproc)`
- `AMS1patch_E_OUTOFMEMORY` (function) `modules/amsi.c:378` `void AMS1patch_E_OUTOFMEMORY(HANDLE hproc)`
- `main` (function) `modules/amsi.c:428` `int main(int argc, char** argv)`

## modules/amt_auth_bypass.py
- `start` (function) `modules/amt_auth_bypass.py:4` `def start()`
- `BlankAuthResponse.request` (method) `modules/amt_auth_bypass.py:11` `def request(self, flow)`

## modules/apt_playbooks.py
Depends on: `core/console.py`, `modules/atomic_resolver.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `cli/orchestrator_assets_tabs.py`, `cli/recommendation_signals.py`, `modules/emulation_runner.py`, `modules/operation.py`, `tests/test_atomic_loop.py`, `tests/test_emulation_runner.py`
- `AptPlaybook.from_dict` (method) `modules/apt_playbooks.py:74` `def from_dict(cls, data)`
- `AptPlaybook.to_summary` (method) `modules/apt_playbooks.py:99` `def to_summary(self)`
- `AptPlaybookEngine.__init__` (method) `modules/apt_playbooks.py:114` `def __init__(self, playbook_dir)`
- `AptPlaybookEngine.list_playbooks` (method) `modules/apt_playbooks.py:131` `def list_playbooks(self)`
- `AptPlaybookEngine.get` (method) `modules/apt_playbooks.py:134` `def get(self, name)`
- `AptPlaybookEngine.validate` (method) `modules/apt_playbooks.py:138` `def validate(self, pb, atomic_path)` -- Validate that all referenced atomic tests exist locally.
- `AptPlaybookEngine.generate_attack_plan` (method) `modules/apt_playbooks.py:213` `def generate_attack_plan(self, pb, output_path)` -- Generate a legacy ``attack_plan.yaml`` from an enriched APT playbook.
- `AptPlaybookEngine.report_json` (method) `modules/apt_playbooks.py:230` `def report_json(self, pb, output_path)` -- Write a structured JSON report of the playbook for the operator.

## modules/asset_graph.py
Imported by: `skills/autonomous_daemon.py`, `tests/test_autonomous_ops.py`
- `asset_key` (function) `modules/asset_graph.py:28` `def asset_key(asset_type, value, parent_key)` -- Compute the stable deduplication key for an asset.
- `AssetGraph.__init__` (method) `modules/asset_graph.py:73` `def __init__(self, config)` -- Initialize empty graphs and anchor indexes.
- `AssetGraph.upsert_asset` (method) `modules/asset_graph.py:82` `def upsert_asset(self, asset_type, value, parent_key, company)` -- Insert or refresh an asset and return the canonical node.
- `AssetGraph.add_node` (method) `modules/asset_graph.py:108` `def add_node(self, task_id, kind, text, parent_id, payload)` -- Append an exploration node to a task chain.
- `AssetGraph.add_fact` (method) `modules/asset_graph.py:123` `def add_fact(self, task_id, text, parent_id, payload)` -- Append a fact node to a task chain.
- `AssetGraph.add_finding` (method) `modules/asset_graph.py:128` `def add_finding(self, task_id, text, parent_id, payload)` -- Append a finding node to a task chain.
- `AssetGraph.anchor` (method) `modules/asset_graph.py:133` `def anchor(self, exploration_id, key)` -- Link an exploration node to an asset key.
- `AssetGraph.assets_for_node` (method) `modules/asset_graph.py:145` `def assets_for_node(self, exploration_id)` -- List assets anchored to one exploration node.
- `AssetGraph.nodes_for_asset` (method) `modules/asset_graph.py:151` `def nodes_for_asset(self, key)` -- List exploration nodes anchored to one asset.
- `AssetGraph.coverage` (method) `modules/asset_graph.py:157` `def coverage(self, task_id)` -- Report tested versus total assets for a task.
- `AssetGraph.mirror_to_campaign` (method) `modules/asset_graph.py:170` `def mirror_to_campaign(self, db, world_model, workspace_id)` -- Mirror graph assets into the campaign database and world model.
- `coverage_for` (function) `modules/asset_graph.py:214` `def coverage_for(db, workspace_id, scope)` -- Report tested scope assets versus total scope from the campaign db.

## modules/atomic_cli.py
Depends on: `core/console.py`, `core/hardening.py`, `core/logging.py`, `modules/atomic_resolver.py`, `utils.py`
Imported by: `cli/commands/command_and_control_migrated.py`
- `parse_atomic_line` (function) `modules/atomic_cli.py:37` `def parse_atomic_line(line)` -- Parse free-form CLI args into a structured request.
- `run_atomic_tests` (function) `modules/atomic_cli.py:185` `def run_atomic_tests(params, line, shell)` -- Execute the atomic_tests workflow (secure + agent-safe).
- `run_atomic_gen` (function) `modules/atomic_cli.py:325` `def run_atomic_gen(params, line, shell)` -- Generate test + cleanup scripts for one technique or GUID.

## modules/atomic_enricher.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `tests/test_core_modules.py`
- `enrich` (function) `modules/atomic_enricher.py:173` `def enrich(force)` -- Build enriched parquet.
- `load_enriched` (function) `modules/atomic_enricher.py:215` `def load_enriched()` -- Load enriched parquet, building it first if it doesn't exist.
- `query_atomic` (function) `modules/atomic_enricher.py:232` `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` -- Structured query over the enriched Atomic Red Team technique catalogue.

## modules/atomic_exploit_bridge.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/__init__.py`, `modules/c2_surfaces.py`, `modules/emulation_runner.py`, `modules/lazy_cve_feed.py`, `modules/lazy_heat.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `modules/autonomous_exploit_engine.py`, `modules/c2_agent.py`, `modules/emulation_runner.py`, `modules/metasploitable_gym.py`, `modules/redteam_gym.py`, `skills/lazyown_mcp.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_c2_surfaces.py`, `tests/test_emulation_runner.py`, `tests/test_gym_cli.py`, `tests/test_metasploitable_gym.py`, `tests/test_outcome_bus.py`
- `ExploitSpec.severity_rank` (method) `modules/atomic_exploit_bridge.py:117` `def severity_rank(self)` -- Return numeric severity for ranking (mirrors the engine).
- `ExploitSpec.to_dict` (method) `modules/atomic_exploit_bridge.py:121` `def to_dict(self)` -- Return a JSON-serializable view.
- `validate_spec` (function) `modules/atomic_exploit_bridge.py:150` `def validate_spec(data, filename)` -- Validate raw YAML data against the exploit schema.
- `load_all` (function) `modules/atomic_exploit_bridge.py:226` `def load_all(exploits_dir)` -- Load every enabled, valid exploit YAML (skips the rest loudly).
- `match_score` (function) `modules/atomic_exploit_bridge.py:281` `def match_score(spec, service, product, version, os_hint)` -- Score a spec against one discovered service (0 when no match).
- `parse_scan_xml` (function) `modules/atomic_exploit_bridge.py:314` `def parse_scan_xml(xml_path)` -- Parse open TCP ports from a lazynmap XML file (stdlib only).
- `auto` (function) `modules/atomic_exploit_bridge.py:351` `def auto(target, lhost, max_attempts, stop_on_shell, task_id, exploits_dir, scan_dir)` -- Pwntomate-style sweep: triggers from scan XML, ranked, stop on SHELL.
- `rank` (function) `modules/atomic_exploit_bridge.py:456` `def rank(services, exploits_dir, os_hint)` -- Rank every spec against discovered services (severity, then confidence).
- `build_commands` (function) `modules/atomic_exploit_bridge.py:511` `def build_commands(spec, rhost, lhost, lport, port)` -- Substitute ``{tokens}`` into a spec's commands (no shell involved).
- `detect_shell` (function) `modules/atomic_exploit_bridge.py:529` `def detect_shell(spec, output)` -- Return True when output carries any shell indicator.
- `run_spec` (function) `modules/atomic_exploit_bridge.py:571` `def run_spec(spec, rhost, lhost, lport, port)` -- Execute a spec's commands in order; stop at the first SHELL hit.
- `open_shell` (function) `modules/atomic_exploit_bridge.py:651` `def open_shell(target, services, lhost, exploits_dir, attempts, privilege)` -- Return the first exec-capable spec with a live multiplexed session.
- `_ShellSession.__init__` (method) `modules/atomic_exploit_bridge.py:715` `def __init__(self, target, port, sock, owner)`
- `_ShellSession.alive` (method) `modules/atomic_exploit_bridge.py:725` `def alive(self, timeout)` -- Return True when the session answers a no-op probe.
- `_ShellSession.run` (method) `modules/atomic_exploit_bridge.py:732` `def run(self, command, timeout)` -- Run one command, return stdout+stderr (never raises).
- `_ShellSession.close` (method) `modules/atomic_exploit_bridge.py:774` `def close(self)` -- End the remote shell cleanly so its listener dies too.
- `record_shell_outcome` (function) `modules/atomic_exploit_bridge.py:825` `def record_shell_outcome(target, via)` -- Mark one target as compromised after an operator obtains a shell.
- `live_sessions` (function) `modules/atomic_exploit_bridge.py:854` `def live_sessions()` -- Return in-process shell sessions without probing the target.
- `close_sessions` (function) `modules/atomic_exploit_bridge.py:873` `def close_sessions(target)` -- Close cached sessions (all, or one target).
- `cleanup_target` (function) `modules/atomic_exploit_bridge.py:915` `def cleanup_target(target, lhost, hard, gym_container, exploits_dir, staging_dir)` -- Clean up after an engagement (soft default, hard on request).
- `ensure_session` (function) `modules/atomic_exploit_bridge.py:992` `def ensure_session(spec, target, lhost)` -- Return a live multiplexed session, establishing it when needed.
- `remote_exec` (function) `modules/atomic_exploit_bridge.py:1088` `def remote_exec(spec, target, command, lhost)` -- Run one command through the persistent multiplexed session.
- `interactive_shell` (function) `modules/atomic_exploit_bridge.py:1106` `def interactive_shell(target, lhost, interactive, exploits_dir)` -- Open a multiplexed session; drop into a REPL only when allowed.
- `emulate` (function) `modules/atomic_exploit_bridge.py:1161` `def emulate(target, techniques, playbook, platform, lhost, per_technique, exploits_dir, scan_dir, include_manual...` -- Execute emulation tests on the target through one working shell.
- `record_outcome` (function) `modules/atomic_exploit_bridge.py:1195` `def record_outcome(spec, target, shell, output, task_id, intent_id, surfaces_dir, port, service, product, version...` -- Feed one exploit outcome to every shared surface through the bus.
- `main` (function) `modules/atomic_exploit_bridge.py:1283` `def main()` -- CLI: validate | list | rank | run (used by the addon and operators).

## modules/atomic_resolver.py
Depends on: `core/logging.py`, `core/safe_exec.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `modules/apt_playbooks.py`, `modules/atomic_cli.py`, `modules/emulation_runner.py`, `modules/ttpscope_bridge.py`, `skills/lazyown_mcp.py`, `tests/test_atomic_loop.py`, `tests/test_atomic_resolver.py`
- `normalize_mitre_id` (function) `modules/atomic_resolver.py:66` `def normalize_mitre_id(raw)` -- Normalize and validate a MITRE technique ID.
- `is_mitre_id` (function) `modules/atomic_resolver.py:84` `def is_mitre_id(raw)` -- Return True when *raw* looks like a MITRE technique ID.
- `normalize_guid` (function) `modules/atomic_resolver.py:93` `def normalize_guid(raw)` -- Normalize and validate an Atomic test GUID.
- `is_guid` (function) `modules/atomic_resolver.py:109` `def is_guid(raw)` -- Return True when *raw* looks like an Atomic test GUID.
- `normalize_platform` (function) `modules/atomic_resolver.py:118` `def normalize_platform(raw)` -- Validate a platform against the allowlist.
- `AtomicTest.mitre_url` (method) `modules/atomic_resolver.py:147` `def mitre_url(self)` -- Return the ATT&CK URL for this test.
- `AtomicTest.to_dict` (method) `modules/atomic_resolver.py:151` `def to_dict(self)` -- Return a JSON-serializable view.
- `AtomicResolver.__init__` (method) `modules/atomic_resolver.py:226` `def __init__(self, atomics_dir)`
- `AtomicResolver.available` (method) `modules/atomic_resolver.py:233` `def available(self)` -- Return True when the atomics directory exists.
- `AtomicResolver.ensure_repo` (method) `modules/atomic_resolver.py:237` `def ensure_repo(self)` -- Clone or pull the Atomic Red Team repo without shell.
- `AtomicResolver.build_index` (method) `modules/atomic_resolver.py:265` `def build_index(self, force)` -- Build the MITRE -> [GUID] index (cached unless *force*).
- `AtomicResolver.guids_for_technique` (method) `modules/atomic_resolver.py:305` `def guids_for_technique(self, mitre_id)` -- Return GUIDs registered for a technique ID (empty when unknown).
- `AtomicResolver.get_by_guid` (method) `modules/atomic_resolver.py:311` `def get_by_guid(self, guid)` -- Return the test for a GUID, or None when unknown.
- `AtomicResolver.list_for_technique` (method) `modules/atomic_resolver.py:317` `def list_for_technique(self, mitre_id, platform)` -- List tests for a technique, optionally filtered by platform.
- `AtomicResolver.resolve` (method) `modules/atomic_resolver.py:334` `def resolve(self, query, platform)` -- Resolve a MITRE ID, GUID, or prefix to matching tests.
- `AtomicResolver.chain` (method) `modules/atomic_resolver.py:380` `def chain(self, techniques, platform, first_match_only)` -- Translate an ordered APT technique chain to concrete tests.
- `AtomicResolver.stats` (method) `modules/atomic_resolver.py:415` `def stats(self)` -- Return index counters.
- `get_resolver` (function) `modules/atomic_resolver.py:424` `def get_resolver(atomics_dir)` -- Return the module-level resolver singleton.
- `resolve_technique` (function) `modules/atomic_resolver.py:432` `def resolve_technique(mitre_id, platform, atomics_dir)` -- Resolve a technique to JSON-serializable test dicts.
- `resolve_chain` (function) `modules/atomic_resolver.py:442` `def resolve_chain(techniques, platform, atomics_dir)` -- Translate a technique chain to JSON-serializable test dicts.
- `build_variables` (function) `modules/atomic_resolver.py:452` `def build_variables(test, rhost, domain, rport, username, password)` -- Build #{variable} substitution map for a test.
- `render_command` (function) `modules/atomic_resolver.py:488` `def render_command(template, variables)` -- Substitute #{variables} without shell interpretation.
- `technique_env_override` (function) `modules/atomic_resolver.py:496` `def technique_env_override()` -- Return atomics dir override from env (empty when unset).

## modules/attack_surface3d.py
Depends on: `cli/surface_graph.py`, `modules/__init__.py`, `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`, `modules/intel_fusion.py`
Imported by: `cli/commands/surface.py`, `lazyc2.py`, `modules/sinks/attack_graph.py`, `tests/test_attack_surface3d.py`
- `build_attack_graph` (function) `modules/attack_surface3d.py:148` `def build_attack_graph(sessions_dir, payload_path, est_cap)` -- Fuse surface scans with campaign intel into one C2-centred graph.
- `add_edge` (function) `modules/attack_surface3d.py:156` `def add_edge(src, dst, kind, evidence, weight)` -- Append one provenance-tagged relation between known nodes.
- `tag` (function) `modules/attack_surface3d.py:167` `def tag(nid, source)` -- Record a corroborating artefact on a node, deduped.
- `refresh_summary` (function) `modules/attack_surface3d.py:480` `def refresh_summary(graph, sessions_dir)` -- Score exposure into intel_summary.json for the autonomous loop.

## modules/auto_loop_memory.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_auto_loop_memory.py`
- `FailureMemory.__init__` (method) `modules/auto_loop_memory.py:56` `def __init__(self, filepath)`
- `FailureMemory.path` (method) `modules/auto_loop_memory.py:63` `def path(self)` -- Backing file path for administrative inspection.
- `FailureMemory.make_key` (method) `modules/auto_loop_memory.py:68` `def make_key(target, category, command)` -- Build the storage key; raises on empty target or command.
- `FailureMemory.base_of` (method) `modules/auto_loop_memory.py:75` `def base_of(command)` -- Extract the base command from a full command string.
- `FailureMemory.record_failure` (method) `modules/auto_loop_memory.py:79` `def record_failure(self, target, category, command)` -- Increment and persist the failure count; returns the new count.
- `FailureMemory.failure_count` (method) `modules/auto_loop_memory.py:89` `def failure_count(self, target, category, command)` -- Current persisted failure count for the combination.
- `FailureMemory.count_for_base` (method) `modules/auto_loop_memory.py:94` `def count_for_base(self, target, base_command)` -- Failure hits aggregated across exact keys whose base matches.
- `FailureMemory.veto_base` (method) `modules/auto_loop_memory.py:105` `def veto_base(self, target, base_command)` -- Mark a base command as blocked by the stuck-loop detector.
- `FailureMemory.is_blocked` (method) `modules/auto_loop_memory.py:115` `def is_blocked(self, target, base_command, bonus_key)` -- True when the base is vetoed or its failure count hit the threshold.
- `FailureMemory.failure_count_strict` (method) `modules/auto_loop_memory.py:123` `def failure_count_strict(self, target, key)` -- Failure count for a raw storage key already containing separators.
- `FailureMemory.blocked_bases` (method) `modules/auto_loop_memory.py:128` `def blocked_bases(self, target)` -- All blocked base commands for the target (vetoed plus past threshold).
- `FailureMemory.clear_target` (method) `modules/auto_loop_memory.py:140` `def clear_target(self, target)` -- Forget every record for a target (manual reset path).
- `FailureMemory.sanctioned_bases` (method) `modules/auto_loop_memory.py:146` `def sanctioned_bases(self, target)` -- Administrative view: counts above threshold with their last timestamp.
- `FailureMemory.save` (method) `modules/auto_loop_memory.py:166` `def save(self)`
- `DecisionPersistence.__init__` (method) `modules/auto_loop_memory.py:215` `def __init__(self, filepath)`
- `DecisionPersistence.push` (method) `modules/auto_loop_memory.py:220` `def push(self, command, reason)` -- Park one decision for later consumption (newest first).
- `DecisionPersistence.pop` (method) `modules/auto_loop_memory.py:229` `def pop(self)` -- Consume and persist-removal of the newest parked decision.
- `DecisionPersistence.peek` (method) `modules/auto_loop_memory.py:237` `def peek(self)` -- Newest parked decision without consuming it.
- `DecisionPersistence.save` (method) `modules/auto_loop_memory.py:244` `def save(self)`

## modules/auto_pivot.py
Imported by: `modules/autonomous_exploit_engine.py`, `skills/lazyown_mcp.py`
- `AutoPivotEngine.__init__` (method) `modules/auto_pivot.py:73` `def __init__(self, config)`
- `AutoPivotEngine.set_config` (method) `modules/auto_pivot.py:82` `def set_config(self, config)`
- `AutoPivotEngine.add_pivot_node` (method) `modules/auto_pivot.py:90` `def add_pivot_node(self, ip, access_type, credential_id, hostname)`
- `AutoPivotEngine.remove_pivot_node` (method) `modules/auto_pivot.py:120` `def remove_pivot_node(self, ip)`
- `AutoPivotEngine.discover_subnets` (method) `modules/auto_pivot.py:128` `def discover_subnets(self, node_ip, command_output)`
- `AutoPivotEngine.build_chain` (method) `modules/auto_pivot.py:146` `def build_chain(self, target_ip, via_nodes, subnet)`
- `AutoPivotEngine.generate_proxychains_config` (method) `modules/auto_pivot.py:177` `def generate_proxychains_config(self, chain_id)`
- `AutoPivotEngine.generate_sshuttle_command` (method) `modules/auto_pivot.py:203` `def generate_sshuttle_command(self, node_ip, subnet)`
- `AutoPivotEngine.generate_chisel_command` (method) `modules/auto_pivot.py:206` `def generate_chisel_command(self, target_ip, local_port)`
- `AutoPivotEngine.generate_ssh_socks_command` (method) `modules/auto_pivot.py:212` `def generate_ssh_socks_command(self, node_ip, local_port)`
- `AutoPivotEngine.health_check` (method) `modules/auto_pivot.py:216` `def health_check(self, node_ip)`
- `AutoPivotEngine.health_check_all` (method) `modules/auto_pivot.py:237` `def health_check_all(self)`
- `AutoPivotEngine.get_active_routes` (method) `modules/auto_pivot.py:243` `def get_active_routes(self)`
- `AutoPivotEngine.get_reachable_hosts` (method) `modules/auto_pivot.py:259` `def get_reachable_hosts(self, node_ip)`
- `AutoPivotEngine.set_reachable_hosts` (method) `modules/auto_pivot.py:267` `def set_reachable_hosts(self, node_ip, hosts)`
- `AutoPivotEngine.set_route_priority` (method) `modules/auto_pivot.py:272` `def set_route_priority(self, node_ip, priority)`
- `AutoPivotEngine.suggest_next_pivot` (method) `modules/auto_pivot.py:352` `def suggest_next_pivot(self)`

## modules/auto_purple.py
Depends on: `core/config.py`, `core/logging.py`, `core/process.py`, `modules/detection_oracle.py`
Imported by: `cli/commands/purple_team.py`
- `PurpleResult.to_csv_row` (method) `modules/auto_purple.py:146` `def to_csv_row(self)` -- Serialize to a flat dict suitable for CSV writer.
- `PurpleResult.to_dict` (method) `modules/auto_purple.py:160` `def to_dict(self)`
- `IPurpleLoop.execute_and_measure` (method) `modules/auto_purple.py:185` `def execute_and_measure(self, command, args, category)`
- `IPurpleLoop.measure_only` (method) `modules/auto_purple.py:193` `def measure_only(self, command, args, category)`
- `IPurpleLoop.engagement_score` (method) `modules/auto_purple.py:201` `def engagement_score(self)`
- `IPurpleLoop.export_dataset` (method) `modules/auto_purple.py:204` `def export_dataset(self)`
- `IPurpleLoop.export_report` (method) `modules/auto_purple.py:207` `def export_report(self)`
- `IPurpleEvaluator.last_results` (method) `modules/auto_purple.py:214` `def last_results(self, n)`
- `IPurpleEvaluator.category_accuracy` (method) `modules/auto_purple.py:217` `def category_accuracy(self, category)`
- `PurpleTeamLoop.__init__` (method) `modules/auto_purple.py:414` `def __init__(self, bt_path, detection_delay, methods, auto_feedback, session_id)`
- `PurpleTeamLoop.execute_and_measure` (method) `modules/auto_purple.py:443` `def execute_and_measure(self, command, args, category)` -- Execute a red action and measure if LazyOwnBT detects it.
- `PurpleTeamLoop.measure_only` (method) `modules/auto_purple.py:493` `def measure_only(self, command, args, category)` -- Measure without executing — test if BT would detect the command.
- `PurpleTeamLoop.engagement_score` (method) `modules/auto_purple.py:529` `def engagement_score(self)` -- Aggregate detection score from all results in this session.
- `PurpleTeamLoop.export_dataset` (method) `modules/auto_purple.py:567` `def export_dataset(self)` -- Return the path to the CSV dataset file.
- `PurpleTeamLoop.export_report` (method) `modules/auto_purple.py:571` `def export_report(self)` -- Generate a full engagement report.
- `PurpleTeamLoop.last_results` (method) `modules/auto_purple.py:596` `def last_results(self, n)`
- `PurpleTeamLoop.category_accuracy` (method) `modules/auto_purple.py:599` `def category_accuracy(self, category)`
- `get_loop` (function) `modules/auto_purple.py:772` `def get_loop(bt_path, detection_delay, methods, auto_feedback)` -- Return (or create) the module-level PurpleTeamLoop singleton.
- `load_config_from_payload` (function) `modules/auto_purple.py:790` `def load_config_from_payload(params)` -- Extract purple_team config from payload.json params dict.


Next: [API_p10.md](API_p10.md)
