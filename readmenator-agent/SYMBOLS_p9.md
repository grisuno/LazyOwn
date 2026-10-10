# Symbols (page 9 of 35)
Previous: [SYMBOLS_p8.md](SYMBOLS_p8.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `stop` | method | `lazygui/services/backend.py:108` | `def stop(self)` |
| `EventLog` | class | `lazygui/services/event_log.py:20` | `class EventLog(QObject)` |
| `__init__` | method | `lazygui/services/event_log.py:26` | `def __init__(self, constants, parent)` |
| `append` | method | `lazygui/services/event_log.py:37` | `def append(self, record)` |
| `capacity` | method | `lazygui/services/event_log.py:33` | `def capacity(self)` |
| `clear` | method | `lazygui/services/event_log.py:47` | `def clear(self)` |
| `extend` | method | `lazygui/services/event_log.py:42` | `def extend(self, records)` |
| `snapshot` | method | `lazygui/services/event_log.py:52` | `def snapshot(self, minimum_level)` |
| `BackendFactory` | class | `lazygui/services/factory.py:24` | `class BackendFactory` |
| `create` | method | `lazygui/services/factory.py:42` | `def create(self, kind, parent, credentials)` |
| `create_local` | method | `lazygui/services/factory.py:30` | `def create_local(self, parent)` |
| `create_teamserver` | method | `lazygui/services/factory.py:34` | `def create_teamserver(self, credentials, parent)` |
| `LocalPtyBackend` | class | `lazygui/services/local_backend.py:30` | `class LocalPtyBackend(Backend)` |
| `__init__` | method | `lazygui/services/local_backend.py:38` | `def __init__(self, constants, paths, parent)` |
| `_configure_master_fd` | method | `lazygui/services/local_backend.py:156` | `def _configure_master_fd(self)` |
| `_emit_event` | method | `lazygui/services/local_backend.py:235` | `def _emit_event(self, level, message)` |
| `_exec_child_process` | method | `lazygui/services/local_backend.py:147` | `def _exec_child_process(self)` |
| `_handle_pty_eof` | method | `lazygui/services/local_backend.py:215` | `def _handle_pty_eof(self)` |
| `_install_read_notifier` | method | `lazygui/services/local_backend.py:173` | `def _install_read_notifier(self)` |
| `_install_reaper` | method | `lazygui/services/local_backend.py:180` | `def _install_reaper(self)` |
| `_install_window_size` | method | `lazygui/services/local_backend.py:163` | `def _install_window_size(self)` |
| `_on_master_readable` | method | `lazygui/services/local_backend.py:187` | `def _on_master_readable(self)` |
| `_reap_child` | method | `lazygui/services/local_backend.py:220` | `def _reap_child(self)` |
| `announce_local_operator` | method | `lazygui/services/local_backend.py:249` | `def announce_local_operator(self)` |
| `feed_terminal_input` | method | `lazygui/services/local_backend.py:127` | `def feed_terminal_input(self, data)` |
| `known_listeners` | method | `lazygui/services/local_backend.py:141` | `def known_listeners(self)` |
| `known_sessions` | method | `lazygui/services/local_backend.py:137` | `def known_sessions(self)` |
| `refresh` | method | `lazygui/services/local_backend.py:117` | `def refresh(self)` |
| `resize_terminal` | method | `lazygui/services/local_backend.py:121` | `def resize_terminal(self, columns, rows)` |
| `send_command` | method | `lazygui/services/local_backend.py:112` | `def send_command(self, command, target_session)` |
| `start` | method | `lazygui/services/local_backend.py:62` | `def start(self)` |
| `stop` | method | `lazygui/services/local_backend.py:87` | `def stop(self)` |
| `BackendKind` | class | `lazygui/services/models.py:17` | `class BackendKind(StrEnum)` |
| `BeaconResult` | class | `lazygui/services/models.py:164` | `class BeaconResult` |
| `CampaignSummary` | class | `lazygui/services/models.py:151` | `class CampaignSummary` |
| `DashboardPayload` | class | `lazygui/services/models.py:139` | `class DashboardPayload` |
| `EventLevel` | class | `lazygui/services/models.py:24` | `class EventLevel(StrEnum)` |
| `EventRecord` | class | `lazygui/services/models.py:87` | `class EventRecord` |
| `GraphEdge` | class | `lazygui/services/models.py:115` | `class GraphEdge` |
| `GraphNode` | class | `lazygui/services/models.py:102` | `class GraphNode` |
| `Listener` | class | `lazygui/services/models.py:64` | `class Listener` |
| `Operator` | class | `lazygui/services/models.py:76` | `class Operator` |
| `Session` | class | `lazygui/services/models.py:49` | `class Session` |
| `Topology` | class | `lazygui/services/models.py:126` | `class Topology` |
| `empty` | method | `lazygui/services/models.py:133` | `def empty(cls)` |
| `now` | method | `lazygui/services/models.py:96` | `def now(cls, level, source, message)` |
| `numeric` | method | `lazygui/services/models.py:34` | `def numeric(self)` |
| `TeamserverBackend` | class | `lazygui/services/teamserver_backend.py:48` | `class TeamserverBackend(Backend)` |
| `TeamserverCredentials` | class | `lazygui/services/teamserver_backend.py:39` | `class TeamserverCredentials` |
| `__init__` | method | `lazygui/services/teamserver_backend.py:51` | `def __init__(self, constants, credentials, parent)` |
| `_build_http_session` | method | `lazygui/services/teamserver_backend.py:302` | `def _build_http_session(self)` |
| `_build_topology_from_payload` | method | `lazygui/services/teamserver_backend.py:664` | `def _build_topology_from_payload(self, payload)` |
| `_build_url` | method | `lazygui/services/teamserver_backend.py:312` | `def _build_url(self, path)` |
| `_connect_sio` | method | `lazygui/services/teamserver_backend.py:444` | `def _connect_sio()` |
| `_dispatch_terminal_lines` | method | `lazygui/services/teamserver_backend.py:378` | `def _dispatch_terminal_lines(self, data)` |
| `_emit_event` | method | `lazygui/services/teamserver_backend.py:780` | `def _emit_event(self, level, message)` |
| `_establish_flask_session` | method | `lazygui/services/teamserver_backend.py:285` | `def _establish_flask_session(self)` |
| `_http_get_json` | method | `lazygui/services/teamserver_backend.py:318` | `def _http_get_json(self, path)` |
| `_http_post_form` | method | `lazygui/services/teamserver_backend.py:332` | `def _http_post_form(self, path, payload)` |
| `_install_http_polling` | method | `lazygui/services/teamserver_backend.py:424` | `def _install_http_polling(self)` |
| `_on_connect` | method | `lazygui/services/teamserver_backend.py:487` | `def _on_connect()` |
| `_on_disconnect` | method | `lazygui/services/teamserver_backend.py:491` | `def _on_disconnect()` |
| `_on_output` | method | `lazygui/services/teamserver_backend.py:481` | `def _on_output(data)` |
| `_on_pty_connect` | method | `lazygui/services/teamserver_backend.py:461` | `def _on_pty_connect()` |
| `_on_pty_output` | method | `lazygui/services/teamserver_backend.py:465` | `def _on_pty_output(data)` |
| `_on_terminal_connect` | method | `lazygui/services/teamserver_backend.py:471` | `def _on_terminal_connect()` |
| `_on_terminal_response` | method | `lazygui/services/teamserver_backend.py:475` | `def _on_terminal_response(data)` |
| `_parse_graph_edges` | method | `lazygui/services/teamserver_backend.py:645` | `def _parse_graph_edges(self, payload)` |
| `_parse_graph_nodes` | method | `lazygui/services/teamserver_backend.py:621` | `def _parse_graph_nodes(self, payload)` |
| `_poll_beacon_results` | method | `lazygui/services/teamserver_backend.py:242` | `def _poll_beacon_results(self)` |
| `_post_session_command` | method | `lazygui/services/teamserver_backend.py:346` | `def _post_session_command(self, command, client_id)` |
| `_refresh_dashboard` | method | `lazygui/services/teamserver_backend.py:396` | `def _refresh_dashboard(self)` |
| `_refresh_topology` | method | `lazygui/services/teamserver_backend.py:386` | `def _refresh_topology(self)` |
| `_send_command_via_pty` | method | `lazygui/services/teamserver_backend.py:357` | `def _send_command_via_pty(self, command)` |
| `_start_socketio` | method | `lazygui/services/teamserver_backend.py:443` | `def _start_socketio(self)` |
| `_stop_socketio` | method | `lazygui/services/teamserver_backend.py:520` | `def _stop_socketio(self)` |
| `_update_from_payload` | method | `lazygui/services/teamserver_backend.py:530` | `def _update_from_payload(self, payload)` |
| `_update_listeners` | method | `lazygui/services/teamserver_backend.py:577` | `def _update_listeners(self, payload)` |
| `_update_operator` | method | `lazygui/services/teamserver_backend.py:608` | `def _update_operator(self, payload)` |
| `_update_sessions` | method | `lazygui/services/teamserver_backend.py:537` | `def _update_sessions(self, payload)` |
| `feed_terminal_input` | method | `lazygui/services/teamserver_backend.py:151` | `def feed_terminal_input(self, data)` |
| `known_campaigns` | method | `lazygui/services/teamserver_backend.py:181` | `def known_campaigns(self)` |
| `known_listeners` | method | `lazygui/services/teamserver_backend.py:173` | `def known_listeners(self)` |
| `known_sessions` | method | `lazygui/services/teamserver_backend.py:169` | `def known_sessions(self)` |
| `known_topology` | method | `lazygui/services/teamserver_backend.py:177` | `def known_topology(self)` |
| `refresh` | method | `lazygui/services/teamserver_backend.py:124` | `def refresh(self)` |
| `request_beacon_history` | method | `lazygui/services/teamserver_backend.py:224` | `def request_beacon_history(self, client_id)` |
| `request_beacon_results` | method | `lazygui/services/teamserver_backend.py:185` | `def request_beacon_results(self, client_id)` |
| `request_world_model` | method | `lazygui/services/teamserver_backend.py:210` | `def request_world_model(self)` |
| `resize_terminal` | method | `lazygui/services/teamserver_backend.py:139` | `def resize_terminal(self, columns, rows)` |
| `send_command` | method | `lazygui/services/teamserver_backend.py:112` | `def send_command(self, command, target_session)` |
| `start` | method | `lazygui/services/teamserver_backend.py:80` | `def start(self)` |
| `stop` | method | `lazygui/services/teamserver_backend.py:97` | `def stop(self)` |
| `ThemeManager` | class | `lazygui/theme/manager.py:26` | `class ThemeManager(QObject)` |
| `__init__` | method | `lazygui/theme/manager.py:31` | `def __init__(self, constants, settings, application, palettes, parent)` |
| `_apply_to_application` | method | `lazygui/theme/manager.py:103` | `def _apply_to_application(self, tokens)` |
| `_build_qpalette` | method | `lazygui/theme/manager.py:109` | `def _build_qpalette(tokens)` |
| `active_id` | method | `lazygui/theme/manager.py:64` | `def active_id(self)` |
| `active_tokens` | method | `lazygui/theme/manager.py:57` | `def active_tokens(self)` |
| `apply` | method | `lazygui/theme/manager.py:80` | `def apply(self, identifier)` |
| `apply_initial` | method | `lazygui/theme/manager.py:72` | `def apply_initial(self)` |
| `available` | method | `lazygui/theme/manager.py:68` | `def available(self)` |
| `cycle` | method | `lazygui/theme/manager.py:93` | `def cycle(self)` |
| `builtin_palettes` | function | `lazygui/theme/palettes/__init__.py:23` | `def builtin_palettes()` |
| `QssBuilder` | class | `lazygui/theme/qss_builder.py:16` | `class QssBuilder` |
| `_font_stack` | method | `lazygui/theme/qss_builder.py:39` | `def _font_stack(stack)` |
| `build` | method | `lazygui/theme/qss_builder.py:21` | `def build(self, tokens)` |
| `ThemeTokens` | class | `lazygui/theme/tokens.py:14` | `class ThemeTokens` |
| `BeaconCommandModal` | class | `lazygui/widgets/beacon_command_modal.py:44` | `class BeaconCommandModal(QDialog)` |
| `_HistoryEntry` | class | `lazygui/widgets/beacon_command_modal.py:35` | `class _HistoryEntry` |
| `__init__` | method | `lazygui/widgets/beacon_command_modal.py:53` | `def __init__(self, backend, parent)` |
| `_build_ui` | method | `lazygui/widgets/beacon_command_modal.py:75` | `def _build_ui(self)` |
| `_last_entry` | method | `lazygui/widgets/beacon_command_modal.py:201` | `def _last_entry(self, index)` |
| `_on_beacon_result` | method | `lazygui/widgets/beacon_command_modal.py:209` | `def _on_beacon_result(self, result)` |
| `_on_history_clicked` | method | `lazygui/widgets/beacon_command_modal.py:196` | `def _on_history_clicked(self, item)` |
| `_on_sessions_changed` | method | `lazygui/widgets/beacon_command_modal.py:168` | `def _on_sessions_changed(self, sessions)` |
| `_on_target_changed` | method | `lazygui/widgets/beacon_command_modal.py:127` | `def _on_target_changed(self, _text)` |
| `_reload_history` | method | `lazygui/widgets/beacon_command_modal.py:131` | `def _reload_history(self)` |
| `_selected_target` | method | `lazygui/widgets/beacon_command_modal.py:122` | `def _selected_target(self)` |
| `_send_command` | method | `lazygui/widgets/beacon_command_modal.py:182` | `def _send_command(self)` |
| `focus_input` | method | `lazygui/widgets/beacon_command_modal.py:227` | `def focus_input(self)` |
| `open` | method | `lazygui/widgets/beacon_command_modal.py:216` | `def open(self)` |
| `CommandPaletteAction` | class | `lazygui/widgets/command_palette_list.py:16` | `class CommandPaletteAction` |
| `CommandPaletteList` | class | `lazygui/widgets/command_palette_list.py:28` | `class CommandPaletteList(QListView)` |
| `__init__` | method | `lazygui/widgets/command_palette_list.py:33` | `def __init__(self, constants, actions, parent)` |
| `_fuzzy_score` | method | `lazygui/widgets/command_palette_list.py:99` | `def _fuzzy_score(query, title, subtitle)` |
| `_on_activated` | method | `lazygui/widgets/command_palette_list.py:85` | `def _on_activated(self, _index)` |
| `_populate` | method | `lazygui/widgets/command_palette_list.py:89` | `def _populate(self, actions)` |
| `_token_order_score` | method | `lazygui/widgets/command_palette_list.py:114` | `def _token_order_score(query, haystack, base_offset)` |
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
| `_on_context_menu` | method | `lazygui/widgets/graph_view.py:377` | `def _on_context_menu(nid, pos)` |
| `_on_selected` | method | `lazygui/widgets/graph_view.py:374` | `def _on_selected(nid)` |
| `_resolve_icon_dir` | function | `lazygui/widgets/graph_view.py:47` | `def _resolve_icon_dir()` |
| `_resolve_node_color` | method | `lazygui/widgets/graph_view.py:575` | `def _resolve_node_color(node)` |
| `_resolve_node_radius` | method | `lazygui/widgets/graph_view.py:584` | `def _resolve_node_radius(node)` |
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
| `_apply` | method | `lazygui/windows/main_window.py:314` | `def _apply()` |
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
| `_toggle` | method | `lazygui/windows/main_window.py:303` | `def _toggle()` |
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
| `LazyOwnShell` | class | `lazyown.py:254` | `class LazyOwnShell(Cmd)` |
| `_PayloadSettableProxy` | class | `lazyown.py:227` | `class _PayloadSettableProxy` |
| `__getattr__` | method | `lazyown.py:243` | `def __getattr__(self, name)` |
| `__init__` | method | `lazyown.py:239` | `def __init__(self, params)` |
| `__init__` | method | `lazyown.py:329` | `def __init__(self)` |
| `__setattr__` | method | `lazyown.py:249` | `def __setattr__(self, name, value)` |
| `_build_chain_prompt_engine` | method | `lazyown.py:969` | `def _build_chain_prompt_engine(self)` |
| `_build_command_stack` | method | `lazyown.py:4762` | `def _build_command_stack(self, adversary, r)` |
| `_build_scope_offensive` | method | `lazyown.py:1583` | `def _build_scope_offensive(self)` |
| `_chain_boot_prompt` | method | `lazyown.py:954` | `def _chain_boot_prompt(self)` |
| `_chain_part_exists` | method | `lazyown.py:1555` | `def _chain_part_exists(self, part)` |
| `_chain_perror` | method | `lazyown.py:1510` | `def _chain_perror()` |
| `_chain_resolver` | method | `lazyown.py:994` | `def _chain_resolver(self, cmd, phase)` |
| `_create_strict_yaml_prompt` | method | `lazyown.py:4570` | `def _create_strict_yaml_prompt(self, base_prompt, nmap_services, knowledge_base)` |
| `_did_you_mean` | method | `lazyown.py:1148` | `def _did_you_mean(self, query, limit)` |
| `_display_adversary_info` | method | `lazyown.py:4776` | `def _display_adversary_info(self, adversary, commands)` |
| `_execute_commands` | method | `lazyown.py:4783` | `def _execute_commands(self, confirm, remote_cmds)` |
| `_load_adversaries` | method | `lazyown.py:4729` | `def _load_adversaries(self)` |
| `_load_extended_params` | method | `lazyown.py:690` | `def _load_extended_params(self)` |
| `_maybe_chain_prompt` | method | `lazyown.py:1012` | `def _maybe_chain_prompt(self, cmd, phase)` |
| `_parse_adversary_args` | method | `lazyown.py:4743` | `def _parse_adversary_args(self, line)` |
| `_parse_bool_setting` | function | `lazyown.py:205` | `def _parse_bool_setting(value)` |
| `_patch_template_if_needed` | method | `lazyown.py:4752` | `def _patch_template_if_needed(self, adversary, path, replacements)` |
| `_persist` | method | `lazyown.py:636` | `def _persist(name, _old, _new)` |
| `_read_recent_commands_for_autosuggest` | method | `lazyown.py:1082` | `def _read_recent_commands_for_autosuggest(self, limit)` |
| `_recording_hook` | method | `lazyown.py:1135` | `def _recording_hook(self, data)` |
| `_refresh_autosuggest` | method | `lazyown.py:1109` | `def _refresh_autosuggest(self, executed_command)` |
| `_register_adversary_command` | method | `lazyown.py:2181` | `def _register_adversary_command(self, adv)` |
| `_register_lua_command` | method | `lazyown.py:1947` | `def _register_lua_command(self, command_name, lua_function)` |
| `_register_ux_settables` | method | `lazyown.py:619` | `def _register_ux_settables(self)` |
| `_render_chain_next` | method | `lazyown.py:4209` | `def _render_chain_next(self, raw_args)` |
| `_resolve_offensive` | method | `lazyown.py:1602` | `def _resolve_offensive(self, name)` |
| `_run_and_chain` | method | `lazyown.py:1473` | `def _run_and_chain(self, parts, add_to_history, raise_keyboard_interrupt)` |
| `_run_auto_decrypt` | method | `lazyown.py:1058` | `def _run_auto_decrypt(self)` |
| `_run_auto_encrypt` | method | `lazyown.py:1070` | `def _run_auto_encrypt(self)` |
| `_scope_check` | method | `lazyown.py:1621` | `def _scope_check(self, cmd_name)` |
| `_scope_confirm` | method | `lazyown.py:1668` | `def _scope_confirm(self, decision)` |
| `_scope_entries` | method | `lazyown.py:2546` | `def _scope_entries(self)` |
| `_scope_render` | method | `lazyown.py:2570` | `def _scope_render(self, entries, mode)` |
| `_scope_save` | method | `lazyown.py:2552` | `def _scope_save(self, entries, mode)` |
| `_split_and_chain` | method | `lazyown.py:1428` | `def _split_and_chain(raw_input)` |
| `_sync_c2_credentials` | method | `lazyown.py:4330` | `def _sync_c2_credentials(self)` |
| `_sync_chain_active` | method | `lazyown.py:940` | `def _sync_chain_active(self, tips_engine)` |
| `_toast_hook` | method | `lazyown.py:881` | `def _toast_hook(self, data)` |
| `_ui_hints_level` | method | `lazyown.py:870` | `def _ui_hints_level(self)` |
| `_unified_tips_hook` | method | `lazyown.py:904` | `def _unified_tips_hook(self, data)` |
| `_ux_debug` | function | `lazyown.py:150` | `def _ux_debug(context, exc)` |
| `_wrap_text` | method | `lazyown.py:2259` | `def _wrap_text(self, text, max_width)` |
| `cmd` | method | `lazyown.py:1226` | `def cmd(self, line)` |
| `cmd_wrapper` | method | `lazyown.py:2190` | `def cmd_wrapper(_)` |
| `complete_assign` | method | `lazyown.py:2516` | `def complete_assign(self, text, line, begidx, endidx)` |
| `complete_issue_command_to_c2` | method | `lazyown.py:4393` | `def complete_issue_command_to_c2(self, text, line, begidx, endidx)` |
| `complete_l00t` | method | `lazyown.py:2505` | `def complete_l00t(self, text, line, begidx, endidx)` |
| `complete_loot` | method | `lazyown.py:2511` | `def complete_loot(self, text, line, begidx, endidx)` |
| `complete_palette` | method | `lazyown.py:2584` | `def complete_palette(self, text, line, begidx, endidx)` |
| `complete_phase` | method | `lazyown.py:2500` | `def complete_phase(self, text, line, begidx, endidx)` |
| `complete_scope` | method | `lazyown.py:2533` | `def complete_scope(self, text, line, begidx, endidx)` |
| `complete_upload_c2` | method | `lazyown.py:4273` | `def complete_upload_c2(self, text, line, begidx, endidx)` |
| `completedefault` | method | `lazyown.py:2276` | `def completedefault(self, text, line, begidx, endidx)` |
| `default` | method | `lazyown.py:786` | `def default(self, line)` |
| `display_toastr` | method | `lazyown.py:2197` | `def display_toastr(self, message, type)` |
| `do_event_log` | method | `lazyown.py:4802` | `def do_event_log(self, line)` |
| `do_route` | method | `lazyown.py:4871` | `def do_route(self, line)` |
| `do_set` | method | `lazyown.py:845` | `def do_set(self, line)` |
| `do_state_snapshot` | method | `lazyown.py:4832` | `def do_state_snapshot(self, line)` |
| `download_file_from_c2` | method | `lazyown.py:4301` | `def download_file_from_c2(self, file_name, clientid)` |
| `emptyline` | method | `lazyown.py:1735` | `def emptyline(self)` |
| `get_available_actions` | method | `lazyown.py:4564` | `def get_available_actions(self)` |
| `get_output` | method | `lazyown.py:4242` | `def get_output(self)` |
| `issue_command_to_c2` | method | `lazyown.py:4362` | `def issue_command_to_c2(self, command, client_id)` |
| `list_files_in_directory` | method | `lazyown.py:1784` | `def list_files_in_directory(self, directory)` |
| `load_plugins` | method | `lazyown.py:1974` | `def load_plugins(self)` |
| `load_user_commands` | method | `lazyown.py:1760` | `def load_user_commands(self)` |
| `load_yaml_plugins` | method | `lazyown.py:2004` | `def load_yaml_plugins(self)` |
| `log_command` | method | `lazyown.py:723` | `def log_command(self, cmd_name, cmd_args, start_time, end_time, duration_ms)` |
| `logcsv` | method | `lazyown.py:1189` | `def logcsv(self, line, start_time, end_time, duration_ms)` |
| `main` | method | `lazyown.py:4894` | `def main()` |
| `make_wrapper` | method | `lazyown.py:1849` | `def make_wrapper(cmd_template, tname, default_target)` |
| `one_cmd` | method | `lazyown.py:1689` | `def one_cmd(self, command)` |
| `onecmd_plus_hooks` | method | `lazyown.py:1326` | `def onecmd_plus_hooks(self, statement, add_to_history, raise_keyboard_interrupt, orig_rl_history_length)` |
| `postloop` | method | `lazyown.py:2467` | `def postloop(self)` |
| `postparsing_precmd` | method | `lazyown.py:2439` | `def postparsing_precmd(self, statement)` |
| `preloop` | method | `lazyown.py:2301` | `def preloop(self)` |
| `process_scan_csv` | method | `lazyown.py:4647` | `def process_scan_csv(self, csv_file, ip, port, all_data, processed_ips)` |
| `process_vuln_csv` | method | `lazyown.py:4670` | `def process_vuln_csv(self, csv_file, ip, all_data, processed_ips)` |
| `refresh_prompt` | method | `lazyown.py:834` | `def refresh_prompt(self)` |
| `register_all_adversary_commands` | method | `lazyown.py:2168` | `def register_all_adversary_commands(self)` |
| `register_tool_commands` | method | `lazyown.py:1790` | `def register_tool_commands(self)` |
| `register_yaml_plugin` | method | `lazyown.py:2027` | `def register_yaml_plugin(self, plugin_data)` |
| `run_command` | method | `lazyown.py:4162` | `def run_command(self, command)` |
| `run_lazyarpspoofing` | method | `lazyown.py:3764` | `def run_lazyarpspoofing(self)` |
| `run_lazyaslrcheck` | method | `lazyown.py:4050` | `def run_lazyaslrcheck(self)` |
| `run_lazyattack` | method | `lazyown.py:3818` | `def run_lazyattack(self)` |
| `run_lazybotcli` | method | `lazyown.py:3482` | `def run_lazybotcli(self)` |
| `run_lazybotnet` | method | `lazyown.py:3298` | `def run_lazybotnet(self)` |
| `run_lazyburpfuzzer` | method | `lazyown.py:3588` | `def run_lazyburpfuzzer(self)` |
| `run_lazyftpsniff` | method | `lazyown.py:2922` | `def run_lazyftpsniff(self)` |
| `run_lazygath` | method | `lazyown.py:2826` | `def run_lazygath(self)` |
| `run_lazyhoneypot` | method | `lazyown.py:3019` | `def run_lazyhoneypot(self)` |
| `run_lazylfi2rce` | method | `lazyown.py:3354` | `def run_lazylfi2rce(self)` |
| `run_lazylogpoisoning` | method | `lazyown.py:3435` | `def run_lazylogpoisoning(self)` |
| `run_lazymetaextract0r` | method | `lazyown.py:3136` | `def run_lazymetaextract0r(self)` |
| `run_lazymsfvenom` | method | `lazyown.py:3873` | `def run_lazymsfvenom(self)` |
| `run_lazynetbios` | method | `lazyown.py:2968` | `def run_lazynetbios(self)` |
| `run_lazynmap` | method | `lazyown.py:2704` | `def run_lazynmap(self)` |
| `run_lazynmapdiscovery` | method | `lazyown.py:2858` | `def run_lazynmapdiscovery(self)` |
| `run_lazyown` | method | `lazyown.py:2648` | `def run_lazyown(self)` |
| `run_lazyownrat` | method | `lazyown.py:3237` | `def run_lazyownrat(self)` |
| `run_lazyownratcli` | method | `lazyown.py:3177` | `def run_lazyownratcli(self)` |
| `run_lazypathhijacking` | method | `lazyown.py:4097` | `def run_lazypathhijacking(self)` |
| `run_lazyreverse_shell` | method | `lazyown.py:3714` | `def run_lazyreverse_shell(self)` |
| `run_lazysearch` | method | `lazyown.py:2601` | `def run_lazysearch(self)` |
| `run_lazysearch_bot` | method | `lazyown.py:3085` | `def run_lazysearch_bot(self)` |
| `run_lazysearch_gui` | method | `lazyown.py:2618` | `def run_lazysearch_gui(self)` |
| `run_lazysniff` | method | `lazyown.py:2873` | `def run_lazysniff(self)` |
| `run_lazyssh77enum` | method | `lazyown.py:3538` | `def run_lazyssh77enum(self)` |
| `run_lazywerkzeugdebug` | method | `lazyown.py:2769` | `def run_lazywerkzeugdebug(self)` |
| `run_script` | method | `lazyown.py:4130` | `def run_script(self, script_name)` |
| `run_update_db` | method | `lazyown.py:2674` | `def run_update_db(self)` |
| `save_user_command` | method | `lazyown.py:1772` | `def save_user_command(self, alias, command)` |
| `scripts` | method | `lazyown.py:815` | `def scripts(self)` |
| `show_toastr` | method | `lazyown.py:2254` | `def show_toastr()` |
| `tool_wrapper` | method | `lazyown.py:1850` | `def tool_wrapper(arg)` |
| `upload_file_to_c2` | method | `lazyown.py:4247` | `def upload_file_to_c2(self, file_path, clientid)` |
| `view_code` | method | `lazyown.py:4459` | `def view_code(self, stdscr)` |
| `wrapper` | method | `lazyown.py:1951` | `def wrapper(arg)` |
| `wrapper_yaml` | method | `lazyown.py:2067` | `def wrapper_yaml(arg)` |
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
| `get_suggestions` | method | `modules/LazyOwnExplorer.py:124` | `def get_suggestions(term)` |
| `get_unique_values` | method | `modules/LazyOwnExplorer.py:241` | `def get_unique_values(self)` |
| `is_binary` | method | `modules/LazyOwnExplorer.py:358` | `def is_binary(file_path)` |
| `load_parquet_files` | method | `modules/LazyOwnExplorer.py:181` | `def load_parquet_files(self)` |
| `move_down` | method | `modules/LazyOwnExplorer.py:87` | `def move_down(self, event)` |
| `move_up` | method | `modules/LazyOwnExplorer.py:75` | `def move_up(self, event)` |
| `on_row_double_click` | method | `modules/LazyOwnExplorer.py:278` | `def on_row_double_click(self, event)` |
| `save_new_vector` | method | `modules/LazyOwnExplorer.py:325` | `def save_new_vector()` |
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
| `ASTToolExtractor` | class | `modules/agent_runner.py:133` | `class ASTToolExtractor` |
| `AgentRunner` | class | `modules/agent_runner.py:172` | `class AgentRunner` |
| `AgentTool` | class | `modules/agent_runner.py:65` | `class AgentTool` |
| `CommandMetadata` | class | `modules/agent_runner.py:126` | `class CommandMetadata` |
| `LazyOwnShellWrapper` | class | `modules/agent_runner.py:347` | `class LazyOwnShellWrapper` |
| `VulnBotCLI` | class | `modules/agent_runner.py:424` | `class VulnBotCLI` |
| `__init__` | method | `modules/agent_runner.py:68` | `def __init__(self, name, description, func, parameters, required)` |
| `__init__` | method | `modules/agent_runner.py:175` | `def __init__(self, model, system_prompt, max_iterations)` |
| `__init__` | method | `modules/agent_runner.py:350` | `def __init__(self, script_path)` |
| `__init__` | method | `modules/agent_runner.py:425` | `def __init__(self, provider, mode, debug, script_path)` |
| `_call_model` | method | `modules/agent_runner.py:277` | `def _call_model(self)` |
| `_load_model` | method | `modules/agent_runner.py:437` | `def _load_model(self)` |
| `_load_shell` | method | `modules/agent_runner.py:357` | `def _load_shell(self)` |
| `_manage_memory` | method | `modules/agent_runner.py:192` | `def _manage_memory(self)` |
| `_process_tool_call` | method | `modules/agent_runner.py:302` | `def _process_tool_call(self, tool_call)` |
| `_reset_history` | method | `modules/agent_runner.py:189` | `def _reset_history(self)` |
| `_setup_agent` | method | `modules/agent_runner.py:452` | `def _setup_agent(self)` |
| `configure_logging` | function | `modules/agent_runner.py:59` | `def configure_logging(debug)` |
| `execute` | method | `modules/agent_runner.py:82` | `def execute(self)` |
| `execute_command` | method | `modules/agent_runner.py:380` | `def execute_command(self, command)` |
| `extract_commands_from_file` | method | `modules/agent_runner.py:137` | `def extract_commands_from_file(file_path, prefix)` |
| `get_commands_summary` | method | `modules/agent_runner.py:417` | `def get_commands_summary(self)` |
| `get_tools_for_api` | method | `modules/agent_runner.py:248` | `def get_tools_for_api(self)` |
| `interactive_mode` | method | `modules/agent_runner.py:485` | `def interactive_mode(bot)` |
| `main` | method | `modules/agent_runner.py:519` | `def main()` |
| `make_executor` | method | `modules/agent_runner.py:225` | `def make_executor(cmd_name)` |
| `parse_args` | method | `modules/agent_runner.py:509` | `def parse_args()` |
| `process_request` | method | `modules/agent_runner.py:480` | `def process_request(self, user_input)` |
| `register_tool` | method | `modules/agent_runner.py:200` | `def register_tool(self, tool)` |
| `register_tool_from_instance` | method | `modules/agent_runner.py:203` | `def register_tool_from_instance(self, func)` |
| `register_tools_from_metadata` | method | `modules/agent_runner.py:221` | `def register_tools_from_metadata(self, commands, executor)` |
| `run` | method | `modules/agent_runner.py:253` | `def run(self, user_input)` |
| `target` | method | `modules/agent_runner.py:387` | `def target()` |
| `to_api_format` | method | `modules/agent_runner.py:76` | `def to_api_format(self)` |
| `wrapper` | method | `modules/agent_runner.py:226` | `def wrapper(command)` |
| `AgentTool` | class | `modules/agent_tool.py:7` | `class AgentTool` |
| `__init__` | method | `modules/agent_tool.py:10` | `def __init__(self, name, description, func, parameters, required)` |
| `execute` | method | `modules/agent_tool.py:25` | `def execute(self)` |
| `to_api_format` | method | `modules/agent_tool.py:18` | `def to_api_format(self)` |
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
| `AIResult` | class | `modules/ai_fallback.py:89` | `class AIResult` |
| `_best_ollama_model` | method | `modules/ai_fallback.py:107` | `def _best_ollama_model()` |
| `_groq_call` | method | `modules/ai_fallback.py:183` | `def _groq_call(api_key, system, user, max_tokens, temperature)` |
| `_is_quota_error` | method | `modules/ai_fallback.py:178` | `def _is_quota_error(exc)` |
| `_ollama_available` | method | `modules/ai_fallback.py:99` | `def _ollama_available()` |
| `_ollama_call` | method | `modules/ai_fallback.py:134` | `def _ollama_call(model, system, user, max_tokens, temperature)` |
| `_toposwarm_call` | method | `modules/ai_fallback.py:210` | `def _toposwarm_call(prompt, system)` |
| `call` | method | `modules/ai_fallback.py:238` | `def call(prompt, system, api_key, max_tokens, temperature)` |
| `AIModel` | class | `modules/ai_model.py:41` | `class AIModel(ABC)` |
| `AnthropicModel` | class | `modules/ai_model.py:331` | `class AnthropicModel(AIModel)` |
| `DeepSeekModel` | class | `modules/ai_model.py:387` | `class DeepSeekModel(AIModel)` |
| `GroqModel` | class | `modules/ai_model.py:125` | `class GroqModel(AIModel)` |
| `OllamaModel` | class | `modules/ai_model.py:205` | `class OllamaModel(AIModel)` |
| `OpenAIModel` | class | `modules/ai_model.py:272` | `class OpenAIModel(AIModel)` |
| `_LazyImporter` | class | `modules/ai_model.py:93` | `class _LazyImporter` |
| `__init__` | method | `modules/ai_model.py:133` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:213` | `def __init__(self, model, host)` |
| `__init__` | method | `modules/ai_model.py:278` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:337` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:394` | `def __init__(self, api_key, model)` |
| `anthropic` | method | `modules/ai_model.py:117` | `def anthropic(cls)` |
| `complete` | method | `modules/ai_model.py:59` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:177` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:308` | `def complete(self, system, user, max_tokens, temperature)` |

Next: [SYMBOLS_p10.md](SYMBOLS_p10.md)
