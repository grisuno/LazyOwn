# Symbols (page 10 of 42)
Previous: [SYMBOLS_p9.md](SYMBOLS_p9.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_selected_target` | method | `lazygui/widgets/beacon_command_modal.py:122` | `def _selected_target(self)` |
| `_send_command` | method | `lazygui/widgets/beacon_command_modal.py:182` | `def _send_command(self)` |
| `focus_input` | method | `lazygui/widgets/beacon_command_modal.py:227` | `def focus_input(self)` |
| `open` | method | `lazygui/widgets/beacon_command_modal.py:216` | `def open(self)` |
| `CommandPaletteAction` | class | `lazygui/widgets/command_palette_list.py:16` | `class CommandPaletteAction` |
| `CommandPaletteList` | class | `lazygui/widgets/command_palette_list.py:28` | `class CommandPaletteList(QListView)` |
| `__init__` | method | `lazygui/widgets/command_palette_list.py:33` | `def __init__(self, constants, actions, parent)` |
| `_fuzzy_score` | function | `lazygui/widgets/command_palette_list.py:99` | `def _fuzzy_score(query, title, subtitle)` |
| `_on_activated` | method | `lazygui/widgets/command_palette_list.py:85` | `def _on_activated(self, _index)` |
| `_populate` | method | `lazygui/widgets/command_palette_list.py:89` | `def _populate(self, actions)` |
| `_token_order_score` | function | `lazygui/widgets/command_palette_list.py:114` | `def _token_order_score(query, haystack, base_offset)` |
| `apply_filter` | method | `lazygui/widgets/command_palette_list.py:58` | `def apply_filter(self, query)` |
| `invoke_current` | method | `lazygui/widgets/command_palette_list.py:76` | `def invoke_current(self)` |
| `set_actions` | method | `lazygui/widgets/command_palette_list.py:53` | `def set_actions(self, actions)` |
| `EventLogView` | class | `lazygui/widgets/event_log_view.py:20` | `class EventLogView(QTreeWidget)` |
| `__init__` | method | `lazygui/widgets/event_log_view.py:23` | `def __init__(self, constants, event_log, parent)` |
| `_append_record` | method | `lazygui/widgets/event_log_view.py:71` | `def _append_record(self, record)` |
| `_on_record_appended` | method | `lazygui/widgets/event_log_view.py:65` | `def _on_record_appended(self, record)` |
| `minimum_level` | method | `lazygui/widgets/event_log_view.py:61` | `def minimum_level(self)` |
| `set_minimum_level` | method | `lazygui/widgets/event_log_view.py:51` | `def set_minimum_level(self, level)` |
| `FilterBar` | class | `lazygui/widgets/filter_bar.py:11` | `class FilterBar(QWidget)` |
| `__init__` | method | `lazygui/widgets/filter_bar.py:16` | `def __init__(self, constants, placeholder_text, label_text, parent)` |
| `_emit_filter_changed` | method | `lazygui/widgets/filter_bar.py:54` | `def _emit_filter_changed(self)` |
| `_on_text_changed` | method | `lazygui/widgets/filter_bar.py:50` | `def _on_text_changed(self, _value)` |
| `clear` | method | `lazygui/widgets/filter_bar.py:46` | `def clear(self)` |
| `text` | method | `lazygui/widgets/filter_bar.py:42` | `def text(self)` |
| `GraphEdgeItem` | class | `lazygui/widgets/graph_view.py:285` | `class GraphEdgeItem(QGraphicsLineItem)` |
| `GraphNodeItem` | class | `lazygui/widgets/graph_view.py:140` | `class GraphNodeItem(QGraphicsEllipseItem)` |
| `GraphNodeState` | class | `lazygui/widgets/graph_view.py:132` | `class GraphNodeState` |
| `GraphScene` | class | `lazygui/widgets/graph_view.py:334` | `class GraphScene(QGraphicsScene)` |
| `GraphView` | class | `lazygui/widgets/graph_view.py:499` | `class GraphView(QGraphicsView)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:143` | `def __init__(self, node, radius, color, pixmap, on_selected, on_context_menu, label_visible, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:288` | `def __init__(self, edge, source_item, target_item, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:340` | `def __init__(self, constants, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:509` | `def __init__(self, constants, parent)` |
| `_add_edge` | method | `lazygui/widgets/graph_view.py:393` | `def _add_edge(self, edge)` |
| `_add_node` | method | `lazygui/widgets/graph_view.py:369` | `def _add_node(self, node)` |
| `_apply_force_layout` | method | `lazygui/widgets/graph_view.py:402` | `def _apply_force_layout(self)` |
| `_create_label` | method | `lazygui/widgets/graph_view.py:173` | `def _create_label(self)` |
| `_icon_for_node` | function | `lazygui/widgets/graph_view.py:81` | `def _icon_for_node(node)` |
| `_install_physics_timer` | method | `lazygui/widgets/graph_view.py:540` | `def _install_physics_timer(self)` |
| `_load_icon` | function | `lazygui/widgets/graph_view.py:63` | `def _load_icon(name)` |
| `_on_context_menu` | function | `lazygui/widgets/graph_view.py:377` | `def _on_context_menu(nid, pos)` |
| `_on_selected` | function | `lazygui/widgets/graph_view.py:374` | `def _on_selected(nid)` |
| `_resolve_icon_dir` | function | `lazygui/widgets/graph_view.py:47` | `def _resolve_icon_dir()` |
| `_resolve_node_color` | function | `lazygui/widgets/graph_view.py:575` | `def _resolve_node_color(node)` |
| `_resolve_node_radius` | function | `lazygui/widgets/graph_view.py:584` | `def _resolve_node_radius(node)` |
| `_tick_physics` | method | `lazygui/widgets/graph_view.py:548` | `def _tick_physics(self)` |
| `_update_position` | method | `lazygui/widgets/graph_view.py:313` | `def _update_position(self)` |
| `edge_data` | method | `lazygui/widgets/graph_view.py:329` | `def edge_data(self)` |
| `fit_to_content` | method | `lazygui/widgets/graph_view.py:565` | `def fit_to_content(self)` |
| `hoverEnterEvent` | method | `lazygui/widgets/graph_view.py:266` | `def hoverEnterEvent(self, event)` |
| `hoverLeaveEvent` | method | `lazygui/widgets/graph_view.py:273` | `def hoverLeaveEvent(self, event)` |
| `itemChange` | method | `lazygui/widgets/graph_view.py:279` | `def itemChange(self, change, value)` |
| `mousePressEvent` | method | `lazygui/widgets/graph_view.py:248` | `def mousePressEvent(self, event)` |
| `mouseReleaseEvent` | method | `lazygui/widgets/graph_view.py:259` | `def mouseReleaseEvent(self, event)` |
| `node_data` | method | `lazygui/widgets/graph_view.py:186` | `def node_data(self)` |
| `paint` | method | `lazygui/widgets/graph_view.py:190` | `def paint(self, painter, option, widget)` |
| `scene_handle` | method | `lazygui/widgets/graph_view.py:570` | `def scene_handle(self)` |
| `selected_node_id` | method | `lazygui/widgets/graph_view.py:491` | `def selected_node_id(self)` |
| `selected_node_id` | method | `lazygui/widgets/graph_view.py:561` | `def selected_node_id(self)` |
| `set_theme_colors` | method | `lazygui/widgets/graph_view.py:527` | `def set_theme_colors(self, bg_color, edge_color)` |
| `set_topology` | method | `lazygui/widgets/graph_view.py:349` | `def set_topology(self, topology)` |
| `set_topology` | method | `lazygui/widgets/graph_view.py:535` | `def set_topology(self, topology)` |
| `step_physics` | method | `lazygui/widgets/graph_view.py:419` | `def step_physics(self)` |
| `update_position` | method | `lazygui/widgets/graph_view.py:324` | `def update_position(self)` |
| `wheelEvent` | method | `lazygui/widgets/graph_view.py:551` | `def wheelEvent(self, event)` |
| `StatusBadge` | class | `lazygui/widgets/status_badge.py:18` | `class StatusBadge(QLabel)` |
| `__init__` | method | `lazygui/widgets/status_badge.py:21` | `def __init__(self, parent)` |
| `set_status` | method | `lazygui/widgets/status_badge.py:27` | `def set_status(self, status)` |
| `TerminalView` | class | `lazygui/widgets/terminal_view.py:33` | `class TerminalView(QPlainTextEdit)` |
| `__init__` | method | `lazygui/widgets/terminal_view.py:38` | `def __init__(self, constants, parent)` |
| `_sanitize` | method | `lazygui/widgets/terminal_view.py:66` | `def _sanitize(raw)` |
| `_translate_key_event` | method | `lazygui/widgets/terminal_view.py:85` | `def _translate_key_event(event)` |
| `append_output` | method | `lazygui/widgets/terminal_view.py:54` | `def append_output(self, text)` |
| `keyPressEvent` | method | `lazygui/widgets/terminal_view.py:75` | `def keyPressEvent(self, event)` |
| `CommandPaletteWindow` | class | `lazygui/windows/command_palette_window.py:15` | `class CommandPaletteWindow(QWidget)` |
| `__init__` | method | `lazygui/windows/command_palette_window.py:18` | `def __init__(self, constants, actions, parent)` |
| `_on_action_invoked` | method | `lazygui/windows/command_palette_window.py:77` | `def _on_action_invoked(self, action)` |
| `keyPressEvent` | method | `lazygui/windows/command_palette_window.py:48` | `def keyPressEvent(self, event)` |
| `set_actions` | method | `lazygui/windows/command_palette_window.py:43` | `def set_actions(self, actions)` |
| `showEvent` | method | `lazygui/windows/command_palette_window.py:71` | `def showEvent(self, event)` |
| `ConnectDialog` | class | `lazygui/windows/connect_dialog.py:50` | `class ConnectDialog(QDialog)` |
| `ConnectionRequest` | class | `lazygui/windows/connect_dialog.py:39` | `class ConnectionRequest` |
| `__init__` | method | `lazygui/windows/connect_dialog.py:53` | `def __init__(self, constants, settings, paths, parent)` |
| `_build_local_page` | method | `lazygui/windows/connect_dialog.py:135` | `def _build_local_page(self)` |
| `_build_teamserver_page` | method | `lazygui/windows/connect_dialog.py:150` | `def _build_teamserver_page(self)` |
| `_on_kind_changed` | method | `lazygui/windows/connect_dialog.py:186` | `def _on_kind_changed(self, index)` |
| `_restore_last_choice` | method | `lazygui/windows/connect_dialog.py:168` | `def _restore_last_choice(self)` |
| `persist_choice` | method | `lazygui/windows/connect_dialog.py:120` | `def persist_choice(self)` |
| `request` | method | `lazygui/windows/connect_dialog.py:105` | `def request(self)` |
| `MainWindow` | class | `lazygui/windows/main_window.py:37` | `class MainWindow(QMainWindow)` |
| `__init__` | method | `lazygui/windows/main_window.py:40` | `def __init__(self, constants, settings, theme_manager, backend, event_log, parent)` |
| `_apply` | function | `lazygui/windows/main_window.py:314` | `def _apply()` |
| `_build_palette_actions` | method | `lazygui/windows/main_window.py:261` | `def _build_palette_actions(self)` |
| `_emit_request_connect` | method | `lazygui/windows/main_window.py:372` | `def _emit_request_connect(self)` |
| `_install_layout` | method | `lazygui/windows/main_window.py:108` | `def _install_layout(self)` |
| `_install_menu_bar` | method | `lazygui/windows/main_window.py:131` | `def _install_menu_bar(self)` |
| `_install_shortcuts` | method | `lazygui/windows/main_window.py:220` | `def _install_shortcuts(self)` |
| `_install_statusbar` | method | `lazygui/windows/main_window.py:195` | `def _install_statusbar(self)` |
| `_install_toolbar` | method | `lazygui/windows/main_window.py:171` | `def _install_toolbar(self)` |
| `_make_panel_toggle` | method | `lazygui/windows/main_window.py:300` | `def _make_panel_toggle(self, panel)` |
| `_make_theme_apply` | method | `lazygui/windows/main_window.py:311` | `def _make_theme_apply(self, identifier)` |
| `_on_dashboard_updated` | method | `lazygui/windows/main_window.py:350` | `def _on_dashboard_updated(self, dashboard)` |
| `_on_event_logged` | method | `lazygui/windows/main_window.py:326` | `def _on_event_logged(self, _record)` |
| `_on_operator_changed` | method | `lazygui/windows/main_window.py:319` | `def _on_operator_changed(self, operator)` |
| `_on_sessions_count_changed` | method | `lazygui/windows/main_window.py:345` | `def _on_sessions_count_changed(self, sessions)` |
| `_on_theme_changed` | method | `lazygui/windows/main_window.py:329` | `def _on_theme_changed(self, tokens)` |
| `_on_theme_menu_action` | method | `lazygui/windows/main_window.py:337` | `def _on_theme_menu_action(self)` |
| `_persist_geometry_and_state` | method | `lazygui/windows/main_window.py:244` | `def _persist_geometry_and_state(self)` |
| `_restore_geometry_and_state` | method | `lazygui/windows/main_window.py:252` | `def _restore_geometry_and_state(self)` |
| `_show_beacon_command_modal` | method | `lazygui/windows/main_window.py:354` | `def _show_beacon_command_modal(self)` |
| `_show_command_palette` | method | `lazygui/windows/main_window.py:361` | `def _show_command_palette(self)` |
| `_tick_clock` | method | `lazygui/windows/main_window.py:386` | `def _tick_clock(self)` |
| `_toggle` | function | `lazygui/windows/main_window.py:303` | `def _toggle()` |
| `closeEvent` | method | `lazygui/windows/main_window.py:99` | `def closeEvent(self, event)` |
| `panels` | method | `lazygui/windows/main_window.py:398` | `def panels(self)` |
| `status_badge` | method | `lazygui/windows/main_window.py:393` | `def status_badge(self)` |
| `window_requests_connect` | method | `lazygui/windows/main_window.py:376` | `def window_requests_connect(self)` |
| `extract_ips_from_arp` | function | `lazyown-docker/hostdiscover.sh:21` | `` |
| `extract_listening_ips_from_netstat` | function | `lazyown-docker/hostdiscover.sh:26` | `` |
| `build_image` | function | `lazyown-docker/mkdocker.sh:93` | `` |
| `check_docker` | function | `lazyown-docker/mkdocker.sh:41` | `` |
| `check_file` | function | `lazyown-docker/mkdocker.sh:49` | `` |
| `clean_container_and_image` | function | `lazyown-docker/mkdocker.sh:197` | `` |
| `container_exists` | function | `lazyown-docker/mkdocker.sh:58` | `` |
| `get_ports` | function | `lazyown-docker/mkdocker.sh:68` | `` |
| `image_exists` | function | `lazyown-docker/mkdocker.sh:63` | `` |
| `log` | function | `lazyown-docker/mkdocker.sh:36` | `` |
| `run_container` | function | `lazyown-docker/mkdocker.sh:117` | `` |
| `stop_container` | function | `lazyown-docker/mkdocker.sh:187` | `` |
| `usage` | function | `lazyown-docker/mkdocker.sh:23` | `` |
| `validate_payload` | function | `lazyown-docker/mkdocker.sh:109` | `` |
| `LazyOwnShell` | class | `lazyown.py:299` | `class LazyOwnShell(Cmd)` |
| `_PayloadSettableProxy` | class | `lazyown.py:234` | `class _PayloadSettableProxy` |
| `__getattr__` | method | `lazyown.py:250` | `def __getattr__(self, name)` |
| `__init__` | method | `lazyown.py:246` | `def __init__(self, params)` |
| `__init__` | method | `lazyown.py:374` | `def __init__(self)` |
| `__setattr__` | method | `lazyown.py:256` | `def __setattr__(self, name, value)` |
| `_build_chain_prompt_engine` | method | `lazyown.py:1033` | `def _build_chain_prompt_engine(self)` |
| `_build_command_stack` | method | `lazyown.py:4870` | `def _build_command_stack(self, adversary, r)` |
| `_build_scope_offensive` | method | `lazyown.py:1675` | `def _build_scope_offensive(self)` |
| `_chain_boot_prompt` | method | `lazyown.py:1018` | `def _chain_boot_prompt(self)` |
| `_chain_part_exists` | method | `lazyown.py:1647` | `def _chain_part_exists(self, part)` |
| `_chain_perror` | function | `lazyown.py:1602` | `def _chain_perror()` |
| `_chain_resolver` | method | `lazyown.py:1058` | `def _chain_resolver(self, cmd, phase)` |
| `_create_strict_yaml_prompt` | method | `lazyown.py:4678` | `def _create_strict_yaml_prompt(self, base_prompt, nmap_services, knowledge_base)` |
| `_did_you_mean` | method | `lazyown.py:1243` | `def _did_you_mean(self, query, limit)` |
| `_display_adversary_info` | method | `lazyown.py:4884` | `def _display_adversary_info(self, adversary, commands)` |
| `_execute_commands` | method | `lazyown.py:4891` | `def _execute_commands(self, confirm, remote_cmds)` |
| `_handler` | function | `lazyown.py:1139` | `def _handler(received, frame, _signum)` |
| `_install_crypto_signal_handlers` | method | `lazyown.py:1122` | `def _install_crypto_signal_handlers(self)` |
| `_load_adversaries` | method | `lazyown.py:4837` | `def _load_adversaries(self)` |
| `_load_extended_params` | method | `lazyown.py:748` | `def _load_extended_params(self)` |
| `_maybe_chain_prompt` | method | `lazyown.py:1076` | `def _maybe_chain_prompt(self, cmd, phase)` |
| `_parse_adversary_args` | method | `lazyown.py:4851` | `def _parse_adversary_args(self, line)` |
| `_parse_bool_setting` | function | `lazyown.py:212` | `def _parse_bool_setting(value)` |
| `_patch_template_if_needed` | method | `lazyown.py:4860` | `def _patch_template_if_needed(self, adversary, path, replacements)` |
| `_persist` | function | `lazyown.py:694` | `def _persist(name, _old, _new)` |
| `_read_recent_commands_for_autosuggest` | method | `lazyown.py:1177` | `def _read_recent_commands_for_autosuggest(self, limit)` |
| `_recording_hook` | method | `lazyown.py:1230` | `def _recording_hook(self, data)` |
| `_refresh_autosuggest` | method | `lazyown.py:1204` | `def _refresh_autosuggest(self, executed_command)` |
| `_register_adversary_command` | method | `lazyown.py:2278` | `def _register_adversary_command(self, adv)` |
| `_register_lua_command` | method | `lazyown.py:2039` | `def _register_lua_command(self, command_name, lua_function)` |
| `_register_ux_settables` | method | `lazyown.py:677` | `def _register_ux_settables(self)` |
| `_render_chain_next` | method | `lazyown.py:4306` | `def _render_chain_next(self, raw_args)` |
| `_resolve_offensive` | method | `lazyown.py:1694` | `def _resolve_offensive(self, name)` |
| `_run_and_chain` | method | `lazyown.py:1565` | `def _run_and_chain(self, parts, add_to_history, raise_keyboard_interrupt)` |
| `_run_auto_decrypt` | method | `lazyown.py:1148` | `def _run_auto_decrypt(self)` |
| `_run_auto_encrypt` | method | `lazyown.py:1160` | `def _run_auto_encrypt(self)` |
| `_scope_check` | method | `lazyown.py:1713` | `def _scope_check(self, cmd_name)` |
| `_scope_confirm` | method | `lazyown.py:1760` | `def _scope_confirm(self, decision)` |
| `_scope_entries` | method | `lazyown.py:2643` | `def _scope_entries(self)` |
| `_scope_render` | method | `lazyown.py:2667` | `def _scope_render(self, entries, mode)` |
| `_scope_save` | method | `lazyown.py:2649` | `def _scope_save(self, entries, mode)` |
| `_split_and_chain` | method | `lazyown.py:1520` | `def _split_and_chain(raw_input)` |
| `_sync_c2_credentials` | method | `lazyown.py:4430` | `def _sync_c2_credentials(self)` |
| `_sync_chain_active` | method | `lazyown.py:1004` | `def _sync_chain_active(self, tips_engine)` |
| `_toast_hook` | method | `lazyown.py:939` | `def _toast_hook(self, data)` |
| `_ui_hints_level` | method | `lazyown.py:928` | `def _ui_hints_level(self)` |
| `_unified_tips_hook` | method | `lazyown.py:968` | `def _unified_tips_hook(self, data)` |
| `_ux_debug` | function | `lazyown.py:157` | `def _ux_debug(context, exc)` |
| `_wrap_text` | method | `lazyown.py:2356` | `def _wrap_text(self, text, max_width)` |
| `cmd` | method | `lazyown.py:1325` | `def cmd(self, line)` |
| `cmd_wrapper` | function | `lazyown.py:2287` | `def cmd_wrapper(_)` |
| `complete_assign` | method | `lazyown.py:2613` | `def complete_assign(self, text, line, begidx, endidx)` |
| `complete_issue_command_to_c2` | method | `lazyown.py:4501` | `def complete_issue_command_to_c2(self, text, line, begidx, endidx)` |
| `complete_l00t` | method | `lazyown.py:2602` | `def complete_l00t(self, text, line, begidx, endidx)` |
| `complete_loot` | method | `lazyown.py:2608` | `def complete_loot(self, text, line, begidx, endidx)` |
| `complete_palette` | method | `lazyown.py:2681` | `def complete_palette(self, text, line, begidx, endidx)` |
| `complete_phase` | method | `lazyown.py:2597` | `def complete_phase(self, text, line, begidx, endidx)` |
| `complete_scope` | method | `lazyown.py:2630` | `def complete_scope(self, text, line, begidx, endidx)` |
| `complete_upload_c2` | method | `lazyown.py:4370` | `def complete_upload_c2(self, text, line, begidx, endidx)` |
| `completedefault` | method | `lazyown.py:2373` | `def completedefault(self, text, line, begidx, endidx)` |
| `default` | method | `lazyown.py:844` | `def default(self, line)` |
| `display_toastr` | method | `lazyown.py:2294` | `def display_toastr(self, message, type)` |
| `do_event_log` | method | `lazyown.py:4910` | `def do_event_log(self, line)` |
| `do_route` | method | `lazyown.py:4979` | `def do_route(self, line)` |
| `do_set` | method | `lazyown.py:903` | `def do_set(self, line)` |
| `do_state_snapshot` | method | `lazyown.py:4940` | `def do_state_snapshot(self, line)` |
| `download_file_from_c2` | method | `lazyown.py:4398` | `def download_file_from_c2(self, file_name, clientid)` |
| `emptyline` | method | `lazyown.py:1827` | `def emptyline(self)` |
| `get_available_actions` | method | `lazyown.py:4672` | `def get_available_actions(self)` |
| `get_output` | method | `lazyown.py:4339` | `def get_output(self)` |
| `issue_command_to_c2` | method | `lazyown.py:4467` | `def issue_command_to_c2(self, command, client_id)` |
| `list_files_in_directory` | method | `lazyown.py:1876` | `def list_files_in_directory(self, directory)` |
| `load_plugins` | method | `lazyown.py:2066` | `def load_plugins(self)` |
| `load_user_commands` | method | `lazyown.py:1852` | `def load_user_commands(self)` |
| `load_yaml_plugins` | method | `lazyown.py:2096` | `def load_yaml_plugins(self)` |
| `log_command` | method | `lazyown.py:781` | `def log_command(self, cmd_name, cmd_args, start_time, end_time, duration_ms)` |
| `logcsv` | method | `lazyown.py:1284` | `def logcsv(self, line, start_time, end_time, duration_ms)` |
| `main` | function | `lazyown.py:5002` | `def main()` |
| `make_wrapper` | function | `lazyown.py:1941` | `def make_wrapper(cmd_template, tname, default_target)` |
| `one_cmd` | method | `lazyown.py:1781` | `def one_cmd(self, command)` |
| `onecmd_plus_hooks` | method | `lazyown.py:1417` | `def onecmd_plus_hooks(self, statement, add_to_history, raise_keyboard_interrupt, orig_rl_history_length)` |
| `postloop` | method | `lazyown.py:2564` | `def postloop(self)` |
| `postparsing_precmd` | method | `lazyown.py:2536` | `def postparsing_precmd(self, statement)` |
| `preloop` | method | `lazyown.py:2398` | `def preloop(self)` |
| `process_scan_csv` | method | `lazyown.py:4755` | `def process_scan_csv(self, csv_file, ip, port, all_data, processed_ips)` |
| `process_vuln_csv` | method | `lazyown.py:4778` | `def process_vuln_csv(self, csv_file, ip, all_data, processed_ips)` |
| `refresh_prompt` | method | `lazyown.py:892` | `def refresh_prompt(self)` |
| `register_all_adversary_commands` | method | `lazyown.py:2265` | `def register_all_adversary_commands(self)` |
| `register_tool_commands` | method | `lazyown.py:1882` | `def register_tool_commands(self)` |
| `register_yaml_plugin` | method | `lazyown.py:2119` | `def register_yaml_plugin(self, plugin_data)` |
| `run_command` | method | `lazyown.py:4259` | `def run_command(self, command)` |
| `run_lazyarpspoofing` | method | `lazyown.py:3861` | `def run_lazyarpspoofing(self)` |
| `run_lazyaslrcheck` | method | `lazyown.py:4147` | `def run_lazyaslrcheck(self)` |
| `run_lazyattack` | method | `lazyown.py:3915` | `def run_lazyattack(self)` |
| `run_lazybotcli` | method | `lazyown.py:3579` | `def run_lazybotcli(self)` |
| `run_lazybotnet` | method | `lazyown.py:3395` | `def run_lazybotnet(self)` |
| `run_lazyburpfuzzer` | method | `lazyown.py:3685` | `def run_lazyburpfuzzer(self)` |
| `run_lazyftpsniff` | method | `lazyown.py:3019` | `def run_lazyftpsniff(self)` |
| `run_lazygath` | method | `lazyown.py:2923` | `def run_lazygath(self)` |
| `run_lazyhoneypot` | method | `lazyown.py:3116` | `def run_lazyhoneypot(self)` |
| `run_lazylfi2rce` | method | `lazyown.py:3451` | `def run_lazylfi2rce(self)` |
| `run_lazylogpoisoning` | method | `lazyown.py:3532` | `def run_lazylogpoisoning(self)` |
| `run_lazymetaextract0r` | method | `lazyown.py:3233` | `def run_lazymetaextract0r(self)` |
| `run_lazymsfvenom` | method | `lazyown.py:3970` | `def run_lazymsfvenom(self)` |
| `run_lazynetbios` | method | `lazyown.py:3065` | `def run_lazynetbios(self)` |
| `run_lazynmap` | method | `lazyown.py:2801` | `def run_lazynmap(self)` |
| `run_lazynmapdiscovery` | method | `lazyown.py:2955` | `def run_lazynmapdiscovery(self)` |
| `run_lazyown` | method | `lazyown.py:2745` | `def run_lazyown(self)` |
| `run_lazyownrat` | method | `lazyown.py:3334` | `def run_lazyownrat(self)` |
| `run_lazyownratcli` | method | `lazyown.py:3274` | `def run_lazyownratcli(self)` |
| `run_lazypathhijacking` | method | `lazyown.py:4194` | `def run_lazypathhijacking(self)` |
| `run_lazyreverse_shell` | method | `lazyown.py:3811` | `def run_lazyreverse_shell(self)` |
| `run_lazysearch` | method | `lazyown.py:2698` | `def run_lazysearch(self)` |
| `run_lazysearch_bot` | method | `lazyown.py:3182` | `def run_lazysearch_bot(self)` |
| `run_lazysearch_gui` | method | `lazyown.py:2715` | `def run_lazysearch_gui(self)` |
| `run_lazysniff` | method | `lazyown.py:2970` | `def run_lazysniff(self)` |
| `run_lazyssh77enum` | method | `lazyown.py:3635` | `def run_lazyssh77enum(self)` |
| `run_lazywerkzeugdebug` | method | `lazyown.py:2866` | `def run_lazywerkzeugdebug(self)` |
| `run_script` | method | `lazyown.py:4227` | `def run_script(self, script_name)` |
| `run_update_db` | method | `lazyown.py:2771` | `def run_update_db(self)` |
| `save_user_command` | method | `lazyown.py:1864` | `def save_user_command(self, alias, command)` |
| `scripts` | method | `lazyown.py:873` | `def scripts(self)` |
| `show_toastr` | function | `lazyown.py:2351` | `def show_toastr()` |
| `tool_wrapper` | function | `lazyown.py:1942` | `def tool_wrapper(arg)` |
| `upload_file_to_c2` | method | `lazyown.py:4344` | `def upload_file_to_c2(self, file_path, clientid)` |
| `view_code` | method | `lazyown.py:4567` | `def view_code(self, stdscr)` |
| `wrapper` | function | `lazyown.py:2043` | `def wrapper(arg)` |
| `wrapper_yaml` | function | `lazyown.py:2159` | `def wrapper_yaml(arg)` |
| `auth` | function | `modules/49803.py:43` | `def auth()` |
| `connection` | function | `modules/49803.py:106` | `def connection()` |
| `injection` | function | `modules/49803.py:69` | `def injection()` |
| `poc` | function | `modules/CVE-2023-28432.py:12` | `def poc(url)` |
| `AutocompleteEntry` | class | `modules/LazyOwnExplorer.py:30` | `class AutocompleteEntry(Entry)` |
| `LazyOwnGUI` | class | `modules/LazyOwnExplorer.py:104` | `class LazyOwnGUI(Tk)` |
| `__init__` | method | `modules/LazyOwnExplorer.py:31` | `def __init__(self, get_suggestions_func)` |
| `__init__` | method | `modules/LazyOwnExplorer.py:105` | `def __init__(self)` |
| `add_new_attack_vector` | method | `modules/LazyOwnExplorer.py:305` | `def add_new_attack_vector(self)` |
| `changed` | method | `modules/LazyOwnExplorer.py:45` | `def changed(self, name, index, mode)` |
| `comparison` | method | `modules/LazyOwnExplorer.py:99` | `def comparison(self, pattern)` |
| `create_widgets` | method | `modules/LazyOwnExplorer.py:119` | `def create_widgets(self)` |
| `export_to_csv` | method | `modules/LazyOwnExplorer.py:385` | `def export_to_csv(self)` |
| `get_suggestions` | function | `modules/LazyOwnExplorer.py:124` | `def get_suggestions(term)` |
| `get_unique_values` | method | `modules/LazyOwnExplorer.py:241` | `def get_unique_values(self)` |
| `is_binary` | function | `modules/LazyOwnExplorer.py:358` | `def is_binary(file_path)` |
| `load_parquet_files` | method | `modules/LazyOwnExplorer.py:181` | `def load_parquet_files(self)` |
| `move_down` | method | `modules/LazyOwnExplorer.py:87` | `def move_down(self, event)` |
| `move_up` | method | `modules/LazyOwnExplorer.py:75` | `def move_up(self, event)` |
| `on_row_double_click` | method | `modules/LazyOwnExplorer.py:278` | `def on_row_double_click(self, event)` |
| `save_new_vector` | function | `modules/LazyOwnExplorer.py:325` | `def save_new_vector()` |
| `scan_system_for_binaries` | method | `modules/LazyOwnExplorer.py:357` | `def scan_system_for_binaries(self)` |
| `search` | method | `modules/LazyOwnExplorer.py:248` | `def search(self)` |
| `search_in_parquet` | method | `modules/LazyOwnExplorer.py:267` | `def search_in_parquet(self, term)` |
| `selection` | method | `modules/LazyOwnExplorer.py:68` | `def selection(self, event)` |
| `show_row_details` | method | `modules/LazyOwnExplorer.py:283` | `def show_row_details(self, row)` |
| `show_scan_results` | method | `modules/LazyOwnExplorer.py:374` | `def show_scan_results(self, binaries)` |
| `ADCSCertipyWrapper` | class | `modules/adcs_attacks.py:69` | `class ADCSCertipyWrapper` |
| `CertificateTemplate` | class | `modules/adcs_attacks.py:14` | `class CertificateTemplate` |
| `__init__` | method | `modules/adcs_attacks.py:80` | `def __init__(self, certipy_path, timeout)` |
| `_find_certipy` | method | `modules/adcs_attacks.py:85` | `def _find_certipy()` |
| `_parse_ca_output` | method | `modules/adcs_attacks.py:157` | `def _parse_ca_output(output)` |
| `_parse_template_output` | method | `modules/adcs_attacks.py:232` | `def _parse_template_output(self, output)` |
| `_run` | method | `modules/adcs_attacks.py:93` | `def _run(self, args, capture)` |
| `assess_vulnerability` | method | `modules/adcs_attacks.py:411` | `def assess_vulnerability(self, username, password, domain, dc_ip, hashes)` |
| `authenticate_with_certificate` | method | `modules/adcs_attacks.py:367` | `def authenticate_with_certificate(self, cert_file, domain, dc_ip, username)` |
| `enumerate_templates` | method | `modules/adcs_attacks.py:189` | `def enumerate_templates(self, username, password, domain, dc_ip, hashes)` |
| `esc_vulnerabilities` | method | `modules/adcs_attacks.py:35` | `def esc_vulnerabilities(self)` |
| `find_certificate_authorities` | method | `modules/adcs_attacks.py:113` | `def find_certificate_authorities(self, username, password, domain, dc_ip, hashes)` |
| `request_certificate_esc1` | method | `modules/adcs_attacks.py:268` | `def request_certificate_esc1(self, username, password, domain, dc_ip, ca_name, template_name, target_user, output_file)` |
| `request_certificate_esc8` | method | `modules/adcs_attacks.py:322` | `def request_certificate_esc8(self, username, password, domain, dc_ip, ca_server, template_name, output_file)` |
| `AddonUpdateResult` | class | `modules/addon_updater.py:33` | `class AddonUpdateResult` |
| `_audit` | function | `modules/addon_updater.py:315` | `def _audit(summary, path)` |
| `_git` | function | `modules/addon_updater.py:135` | `def _git(path)` |
| `_read_addon` | function | `modules/addon_updater.py:61` | `def _read_addon(path)` |
| `_safe_target` | function | `modules/addon_updater.py:107` | `def _safe_target(install_path, root)` |
| `_worktree_root` | function | `modules/addon_updater.py:150` | `def _worktree_root(path, repository_root)` |
| `load_addons` | function | `modules/addon_updater.py:73` | `def load_addons(lazyaddons_dir)` |
| `to_dict` | method | `modules/addon_updater.py:46` | `def to_dict(self)` |
| `update_addon` | function | `modules/addon_updater.py:166` | `def update_addon(name, lazyaddons_dir, root, dry_run)` |
| `update_all` | function | `modules/addon_updater.py:260` | `def update_all(names, lazyaddons_dir, root, dry_run, audit_path)` |
| `ASTToolExtractor` | class | `modules/agent_runner.py:134` | `class ASTToolExtractor` |
| `AgentRunner` | class | `modules/agent_runner.py:190` | `class AgentRunner` |
| `AgentTool` | class | `modules/agent_runner.py:66` | `class AgentTool` |
| `CommandMetadata` | class | `modules/agent_runner.py:127` | `class CommandMetadata` |
| `LazyOwnShellWrapper` | class | `modules/agent_runner.py:482` | `class LazyOwnShellWrapper` |
| `VulnBotCLI` | class | `modules/agent_runner.py:559` | `class VulnBotCLI` |
| `__init__` | method | `modules/agent_runner.py:69` | `def __init__(self, name, description, func, parameters, required)` |
| `__init__` | method | `modules/agent_runner.py:193` | `def __init__(self, model, system_prompt, max_iterations)` |
| `__init__` | method | `modules/agent_runner.py:485` | `def __init__(self, script_path)` |
| `__init__` | method | `modules/agent_runner.py:560` | `def __init__(self, provider, mode, debug, script_path)` |
| `_call_model` | method | `modules/agent_runner.py:295` | `def _call_model(self)` |
| `_emit_delta` | method | `modules/agent_runner.py:415` | `def _emit_delta(self, kind, text)` |
| `_load_model` | method | `modules/agent_runner.py:572` | `def _load_model(self)` |
| `_load_shell` | method | `modules/agent_runner.py:492` | `def _load_shell(self)` |
| `_manage_memory` | method | `modules/agent_runner.py:210` | `def _manage_memory(self)` |
| `_process_tool_call` | method | `modules/agent_runner.py:434` | `def _process_tool_call(self, tool_call)` |
| `_reset_history` | method | `modules/agent_runner.py:207` | `def _reset_history(self)` |
| `_setup_agent` | method | `modules/agent_runner.py:587` | `def _setup_agent(self)` |
| `_stream_call` | method | `modules/agent_runner.py:341` | `def _stream_call(self, model_name, messages, max_tokens)` |
| `_tool_call_snapshot` | function | `modules/agent_runner.py:173` | `def _tool_call_snapshot(tool_call)` |
| `configure_logging` | function | `modules/agent_runner.py:60` | `def configure_logging(debug)` |
| `execute` | method | `modules/agent_runner.py:83` | `def execute(self)` |
| `execute_command` | method | `modules/agent_runner.py:515` | `def execute_command(self, command)` |
| `extract_commands_from_file` | method | `modules/agent_runner.py:138` | `def extract_commands_from_file(file_path, prefix)` |
| `get_commands_summary` | method | `modules/agent_runner.py:552` | `def get_commands_summary(self)` |
| `get_tools_for_api` | method | `modules/agent_runner.py:266` | `def get_tools_for_api(self)` |
| `interactive_mode` | function | `modules/agent_runner.py:620` | `def interactive_mode(bot)` |
| `main` | function | `modules/agent_runner.py:654` | `def main()` |
| `make_executor` | function | `modules/agent_runner.py:243` | `def make_executor(cmd_name)` |
| `parse_args` | function | `modules/agent_runner.py:644` | `def parse_args()` |
| `process_request` | method | `modules/agent_runner.py:615` | `def process_request(self, user_input)` |
| `register_tool` | method | `modules/agent_runner.py:218` | `def register_tool(self, tool)` |
| `register_tool_from_instance` | method | `modules/agent_runner.py:221` | `def register_tool_from_instance(self, func)` |
| `register_tools_from_metadata` | method | `modules/agent_runner.py:239` | `def register_tools_from_metadata(self, commands, executor)` |
| `run` | method | `modules/agent_runner.py:271` | `def run(self, user_input)` |
| `target` | function | `modules/agent_runner.py:522` | `def target()` |
| `to_api_format` | method | `modules/agent_runner.py:77` | `def to_api_format(self)` |
| `wrapper` | function | `modules/agent_runner.py:244` | `def wrapper(command)` |
| `AIExploitChainer` | class | `modules/ai_exploit_chain.py:247` | `class AIExploitChainer` |
| `ExploitChainContext` | class | `modules/ai_exploit_chain.py:223` | `class ExploitChainContext` |
| `__init__` | method | `modules/ai_exploit_chain.py:259` | `def __init__(self)` |
| `_ensure` | method | `modules/ai_exploit_chain.py:487` | `def _ensure(context, strategy)` |
| `_parse_shell_hints` | method | `modules/ai_exploit_chain.py:492` | `def _parse_shell_hints(self, output, context)` |
| `adapt_chain` | method | `modules/ai_exploit_chain.py:428` | `def adapt_chain(self, context, new_info)` |
| `build_chain_plan` | method | `modules/ai_exploit_chain.py:391` | `def build_chain_plan(self, context)` |
| `estimate_confidence` | method | `modules/ai_exploit_chain.py:349` | `def estimate_confidence(self, strategy, profile)` |
| `evaluate_failure` | method | `modules/ai_exploit_chain.py:306` | `def evaluate_failure(result)` |
| `reason` | method | `modules/ai_exploit_chain.py:285` | `def reason(self, context)` |
| `select_next_strategy` | method | `modules/ai_exploit_chain.py:318` | `def select_next_strategy(self, context)` |
| `AIResult` | class | `modules/ai_fallback.py:95` | `class AIResult` |
| `_best_ollama_model` | function | `modules/ai_fallback.py:113` | `def _best_ollama_model()` |
| `_groq_call` | function | `modules/ai_fallback.py:189` | `def _groq_call(api_key, system, user, max_tokens, temperature)` |
| `_is_quota_error` | function | `modules/ai_fallback.py:184` | `def _is_quota_error(exc)` |
| `_ollama_available` | function | `modules/ai_fallback.py:105` | `def _ollama_available()` |
| `_ollama_call` | function | `modules/ai_fallback.py:140` | `def _ollama_call(model, system, user, max_tokens, temperature)` |
| `_toposwarm_call` | function | `modules/ai_fallback.py:226` | `def _toposwarm_call(prompt, system)` |
| `call` | function | `modules/ai_fallback.py:254` | `def call(prompt, system, api_key, max_tokens, temperature)` |
| `AIModel` | class | `modules/ai_model.py:45` | `class AIModel(ABC)` |
| `AnthropicModel` | class | `modules/ai_model.py:493` | `class AnthropicModel(AIModel)` |
| `DeepSeekModel` | class | `modules/ai_model.py:549` | `class DeepSeekModel(AIModel)` |
| `GroqModel` | class | `modules/ai_model.py:129` | `class GroqModel(AIModel)` |
| `LlamaCppModel` | class | `modules/ai_model.py:313` | `class LlamaCppModel(AIModel)` |
| `OllamaModel` | class | `modules/ai_model.py:244` | `class OllamaModel(AIModel)` |
| `OpenAIModel` | class | `modules/ai_model.py:434` | `class OpenAIModel(AIModel)` |
| `_LazyImporter` | class | `modules/ai_model.py:97` | `class _LazyImporter` |
| `__init__` | method | `modules/ai_model.py:137` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:252` | `def __init__(self, model, host)` |
| `__init__` | method | `modules/ai_model.py:324` | `def __init__(self, model, host)` |
| `__init__` | method | `modules/ai_model.py:440` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:499` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:556` | `def __init__(self, api_key, model)` |
| `_chat` | method | `modules/ai_model.py:341` | `def _chat(self, messages, max_tokens, stream)` |
| `_model_chain` | method | `modules/ai_model.py:141` | `def _model_chain(self)` |
| `anthropic` | method | `modules/ai_model.py:121` | `def anthropic(cls)` |
| `complete` | method | `modules/ai_model.py:63` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:216` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:413` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:470` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:529` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:589` | `def complete(self, system, user, max_tokens, temperature)` |
| `generate` | method | `modules/ai_model.py:56` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:155` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:260` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:362` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:444` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:503` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:563` | `def generate(self, prompt)` |
| `groq` | method | `modules/ai_model.py:105` | `def groq(cls)` |
| `openai` | method | `modules/ai_model.py:113` | `def openai(cls)` |
| `stream_generate` | method | `modules/ai_model.py:60` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:183` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:281` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:382` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:455` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:515` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:574` | `def stream_generate(self, prompt)` |
| `AMS1patch_E_ACCESSDENIED` | function | `modules/amsi.c:274` | `void AMS1patch_E_ACCESSDENIED(HANDLE hproc)` |
| `AMS1patch_E_HANDLE` | function | `modules/amsi.c:326` | `void AMS1patch_E_HANDLE(HANDLE hproc)` |
| `AMS1patch_E_OUTOFMEMORY` | function | `modules/amsi.c:378` | `void AMS1patch_E_OUTOFMEMORY(HANDLE hproc)` |
| `AMS1patch_OpenSession_jne` | function | `modules/amsi.c:66` | `void AMS1patch_OpenSession_jne(HANDLE hproc)` |
| `AMS1patch_OpenSession_ret` | function | `modules/amsi.c:116` | `void AMS1patch_OpenSession_ret(HANDLE hproc)` |
| `AMS1patch_RastaMouse` | function | `modules/amsi.c:215` | `void AMS1patch_RastaMouse(HANDLE hproc)` |
| `AMS1patch_ScanBuffer_ret` | function | `modules/amsi.c:166` | `void AMS1patch_ScanBuffer_ret(HANDLE hproc)` |
| `LoadNtFunctions` | function | `modules/amsi.c:38` | `void LoadNtFunctions()` |
| `NT_SUCCESS` | macro | `modules/amsi.c:11` | `#define NT_SUCCESS(Status)` |
| `main` | function | `modules/amsi.c:428` | `int main(int argc, char** argv)` |
| `BlankAuthResponse` | class | `modules/amt_auth_bypass.py:8` | `class BlankAuthResponse` |
| `request` | method | `modules/amt_auth_bypass.py:11` | `def request(self, flow)` |
| `start` | function | `modules/amt_auth_bypass.py:4` | `def start()` |
| `AptPlaybook` | class | `modules/apt_playbooks.py:65` | `class AptPlaybook` |
| `AptPlaybookEngine` | class | `modules/apt_playbooks.py:111` | `class AptPlaybookEngine` |
| `AtomicTestRef` | class | `modules/apt_playbooks.py:41` | `class AtomicTestRef` |
| `CalderaAbilityRef` | class | `modules/apt_playbooks.py:48` | `class CalderaAbilityRef` |
| `PhaseStep` | class | `modules/apt_playbooks.py:54` | `class PhaseStep` |
| `__init__` | method | `modules/apt_playbooks.py:114` | `def __init__(self, playbook_dir)` |
| `_build_atomic_index` | method | `modules/apt_playbooks.py:199` | `def _build_atomic_index(self, atomic_yaml_path)` |
| `_load_all` | method | `modules/apt_playbooks.py:119` | `def _load_all(self)` |
| `from_dict` | method | `modules/apt_playbooks.py:74` | `def from_dict(cls, data)` |
| `generate_attack_plan` | method | `modules/apt_playbooks.py:213` | `def generate_attack_plan(self, pb, output_path)` |
| `get` | method | `modules/apt_playbooks.py:134` | `def get(self, name)` |
| `list_playbooks` | method | `modules/apt_playbooks.py:131` | `def list_playbooks(self)` |
| `report_json` | method | `modules/apt_playbooks.py:230` | `def report_json(self, pb, output_path)` |
| `to_summary` | method | `modules/apt_playbooks.py:99` | `def to_summary(self)` |
| `validate` | method | `modules/apt_playbooks.py:138` | `def validate(self, pb, atomic_path)` |
| `Anchor` | class | `modules/asset_graph.py:63` | `class Anchor` |
| `AssetGraph` | class | `modules/asset_graph.py:70` | `class AssetGraph` |
| `AssetNode` | class | `modules/asset_graph.py:36` | `class AssetNode` |
| `ExplorationNode` | class | `modules/asset_graph.py:50` | `class ExplorationNode` |
| `GraphConfig` | class | `modules/asset_graph.py:17` | `class GraphConfig` |
| `__init__` | method | `modules/asset_graph.py:73` | `def __init__(self, config)` |
| `add_fact` | method | `modules/asset_graph.py:123` | `def add_fact(self, task_id, text, parent_id, payload)` |
| `add_finding` | method | `modules/asset_graph.py:128` | `def add_finding(self, task_id, text, parent_id, payload)` |
| `add_node` | method | `modules/asset_graph.py:108` | `def add_node(self, task_id, kind, text, parent_id, payload)` |
| `anchor` | method | `modules/asset_graph.py:133` | `def anchor(self, exploration_id, key)` |
| `asset_key` | function | `modules/asset_graph.py:28` | `def asset_key(asset_type, value, parent_key)` |
| `assets_for_node` | method | `modules/asset_graph.py:145` | `def assets_for_node(self, exploration_id)` |
| `coverage` | method | `modules/asset_graph.py:157` | `def coverage(self, task_id)` |
| `coverage_for` | function | `modules/asset_graph.py:214` | `def coverage_for(db, workspace_id, scope)` |
| `mirror_to_campaign` | method | `modules/asset_graph.py:170` | `def mirror_to_campaign(self, db, world_model, workspace_id)` |
| `nodes_for_asset` | method | `modules/asset_graph.py:151` | `def nodes_for_asset(self, key)` |
| `upsert_asset` | method | `modules/asset_graph.py:82` | `def upsert_asset(self, asset_type, value, parent_key, company)` |
| `_load_credentials` | function | `modules/atomic_cli.py:147` | `def _load_credentials(params, non_interactive)` |
| `_print` | function | `modules/atomic_cli.py:107` | `def _print(shell, text)` |
| `_prompt_choice` | function | `modules/atomic_cli.py:171` | `def _prompt_choice(count, prompt, non_interactive)` |
| `_resolver` | function | `modules/atomic_cli.py:99` | `def _resolver()` |
| `_safe_copy` | function | `modules/atomic_cli.py:132` | `def _safe_copy(text)` |
| `_sanitized_script_name` | function | `modules/atomic_cli.py:319` | `def _sanitized_script_name(test_id, extension)` |
| `_wants_interactive` | function | `modules/atomic_cli.py:127` | `def _wants_interactive(non_interactive)` |
| `_warn` | function | `modules/atomic_cli.py:118` | `def _warn(text)` |
| `parse_atomic_line` | function | `modules/atomic_cli.py:37` | `def parse_atomic_line(line)` |
| `run_atomic_gen` | function | `modules/atomic_cli.py:325` | `def run_atomic_gen(params, line, shell)` |
| `run_atomic_tests` | function | `modules/atomic_cli.py:185` | `def run_atomic_tests(params, line, shell)` |
| `_parse_complexity` | function | `modules/atomic_enricher.py:142` | `def _parse_complexity(command)` |
| `_parse_keyword_tags` | function | `modules/atomic_enricher.py:152` | `def _parse_keyword_tags(name, description)` |
| `_parse_platforms` | function | `modules/atomic_enricher.py:122` | `def _parse_platforms(raw)` |
| `_parse_scope` | function | `modules/atomic_enricher.py:135` | `def _parse_scope(name)` |
| `_tactic_prefix` | function | `modules/atomic_enricher.py:164` | `def _tactic_prefix(mitre_id)` |
| `_to_pylist` | function | `modules/atomic_enricher.py:204` | `def _to_pylist(val)` |
| `enrich` | function | `modules/atomic_enricher.py:173` | `def enrich(force)` |
| `load_enriched` | function | `modules/atomic_enricher.py:215` | `def load_enriched()` |
| `query_atomic` | function | `modules/atomic_enricher.py:232` | `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` |
| `ExploitCommand` | class | `modules/atomic_exploit_bridge.py:70` | `class ExploitCommand` |
| `ExploitSpec` | class | `modules/atomic_exploit_bridge.py:78` | `class ExploitSpec` |
| `_ShellSession` | class | `modules/atomic_exploit_bridge.py:585` | `class _ShellSession` |
| `__init__` | method | `modules/atomic_exploit_bridge.py:593` | `def __init__(self, target, port, sock)` |
| `_adopt_live_shell` | function | `modules/atomic_exploit_bridge.py:880` | `def _adopt_live_shell(spec, target, port)` |
| `_destroy_gym` | function | `modules/atomic_exploit_bridge.py:811` | `def _destroy_gym(container)` |
| `_read_until` | method | `modules/atomic_exploit_bridge.py:623` | `def _read_until(self, marker, timeout)` |
| `_string_list` | function | `modules/atomic_exploit_bridge.py:128` | `def _string_list(value)` |
| `_wait_port_closed` | function | `modules/atomic_exploit_bridge.py:896` | `def _wait_port_closed(target, port, timeout)` |
| `alive` | method | `modules/atomic_exploit_bridge.py:602` | `def alive(self, timeout)` |
| `auto` | function | `modules/atomic_exploit_bridge.py:323` | `def auto(target, lhost, max_attempts, stop_on_shell, task_id, exploits_dir, scan_dir)` |
| `build_commands` | function | `modules/atomic_exploit_bridge.py:452` | `def build_commands(spec, rhost, lhost, lport, port)` |
| `cleanup_target` | function | `modules/atomic_exploit_bridge.py:753` | `def cleanup_target(target, lhost, hard, gym_container, exploits_dir, staging_dir)` |
| `close` | method | `modules/atomic_exploit_bridge.py:651` | `def close(self)` |
| `close_sessions` | function | `modules/atomic_exploit_bridge.py:718` | `def close_sessions(target)` |
| `detect_shell` | function | `modules/atomic_exploit_bridge.py:470` | `def detect_shell(spec, output)` |
| `emulate` | function | `modules/atomic_exploit_bridge.py:981` | `def emulate(target, techniques, playbook, platform, lhost, per_technique, exploits_dir, scan_dir, include_manual...` |
| `ensure_session` | function | `modules/atomic_exploit_bridge.py:829` | `def ensure_session(spec, target, lhost)` |
| `interactive_shell` | function | `modules/atomic_exploit_bridge.py:929` | `def interactive_shell(target, lhost, interactive, exploits_dir)` |

Next: [SYMBOLS_p11.md](SYMBOLS_p11.md)
