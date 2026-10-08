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
| `_build_topology_from_payload` | method | `lazygui/services/teamserver_backend.py:666` | `def _build_topology_from_payload(self, payload)` |
| `_build_url` | method | `lazygui/services/teamserver_backend.py:312` | `def _build_url(self, path)` |
| `_connect_sio` | method | `lazygui/services/teamserver_backend.py:444` | `def _connect_sio()` |
| `_dispatch_terminal_lines` | method | `lazygui/services/teamserver_backend.py:378` | `def _dispatch_terminal_lines(self, data)` |
| `_emit_event` | method | `lazygui/services/teamserver_backend.py:774` | `def _emit_event(self, level, message)` |
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
| `_parse_graph_edges` | method | `lazygui/services/teamserver_backend.py:647` | `def _parse_graph_edges(self, payload)` |
| `_parse_graph_nodes` | method | `lazygui/services/teamserver_backend.py:623` | `def _parse_graph_nodes(self, payload)` |
| `_poll_beacon_results` | method | `lazygui/services/teamserver_backend.py:244` | `def _poll_beacon_results(self)` |
| `_post_session_command` | method | `lazygui/services/teamserver_backend.py:346` | `def _post_session_command(self, command, client_id)` |
| `_refresh_dashboard` | method | `lazygui/services/teamserver_backend.py:396` | `def _refresh_dashboard(self)` |
| `_refresh_topology` | method | `lazygui/services/teamserver_backend.py:386` | `def _refresh_topology(self)` |
| `_send_command_via_pty` | method | `lazygui/services/teamserver_backend.py:357` | `def _send_command_via_pty(self, command)` |
| `_start_socketio` | method | `lazygui/services/teamserver_backend.py:443` | `def _start_socketio(self)` |
| `_stop_socketio` | method | `lazygui/services/teamserver_backend.py:522` | `def _stop_socketio(self)` |
| `_update_from_payload` | method | `lazygui/services/teamserver_backend.py:532` | `def _update_from_payload(self, payload)` |
| `_update_listeners` | method | `lazygui/services/teamserver_backend.py:579` | `def _update_listeners(self, payload)` |
| `_update_operator` | method | `lazygui/services/teamserver_backend.py:610` | `def _update_operator(self, payload)` |
| `_update_sessions` | method | `lazygui/services/teamserver_backend.py:539` | `def _update_sessions(self, payload)` |
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
| `focus_input` | method | `lazygui/widgets/beacon_command_modal.py:229` | `def focus_input(self)` |
| `open` | method | `lazygui/widgets/beacon_command_modal.py:218` | `def open(self)` |
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
| `GraphEdgeItem` | class | `lazygui/widgets/graph_view.py:284` | `class GraphEdgeItem(QGraphicsLineItem)` |
| `GraphNodeItem` | class | `lazygui/widgets/graph_view.py:139` | `class GraphNodeItem(QGraphicsEllipseItem)` |
| `GraphNodeState` | class | `lazygui/widgets/graph_view.py:131` | `class GraphNodeState` |
| `GraphScene` | class | `lazygui/widgets/graph_view.py:333` | `class GraphScene(QGraphicsScene)` |
| `GraphView` | class | `lazygui/widgets/graph_view.py:495` | `class GraphView(QGraphicsView)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:142` | `def __init__(self, node, radius, color, pixmap, on_selected, on_context_menu, label_visible, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:287` | `def __init__(self, edge, source_item, target_item, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:339` | `def __init__(self, constants, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:505` | `def __init__(self, constants, parent)` |
| `_add_edge` | method | `lazygui/widgets/graph_view.py:389` | `def _add_edge(self, edge)` |
| `_add_node` | method | `lazygui/widgets/graph_view.py:368` | `def _add_node(self, node)` |
| `_apply_force_layout` | method | `lazygui/widgets/graph_view.py:398` | `def _apply_force_layout(self)` |
| `_create_label` | method | `lazygui/widgets/graph_view.py:172` | `def _create_label(self)` |
| `_icon_for_node` | function | `lazygui/widgets/graph_view.py:81` | `def _icon_for_node(node)` |
| `_install_physics_timer` | method | `lazygui/widgets/graph_view.py:536` | `def _install_physics_timer(self)` |
| `_load_icon` | function | `lazygui/widgets/graph_view.py:63` | `def _load_icon(name)` |
| `_on_context_menu` | method | `lazygui/widgets/graph_view.py:376` | `def _on_context_menu(nid, pos)` |
| `_on_selected` | method | `lazygui/widgets/graph_view.py:373` | `def _on_selected(nid)` |
| `_resolve_icon_dir` | function | `lazygui/widgets/graph_view.py:47` | `def _resolve_icon_dir()` |
| `_resolve_node_color` | method | `lazygui/widgets/graph_view.py:571` | `def _resolve_node_color(node)` |
| `_resolve_node_radius` | method | `lazygui/widgets/graph_view.py:580` | `def _resolve_node_radius(node)` |
| `_tick_physics` | method | `lazygui/widgets/graph_view.py:544` | `def _tick_physics(self)` |
| `_update_position` | method | `lazygui/widgets/graph_view.py:312` | `def _update_position(self)` |
| `edge_data` | method | `lazygui/widgets/graph_view.py:328` | `def edge_data(self)` |
| `fit_to_content` | method | `lazygui/widgets/graph_view.py:561` | `def fit_to_content(self)` |
| `hoverEnterEvent` | method | `lazygui/widgets/graph_view.py:265` | `def hoverEnterEvent(self, event)` |
| `hoverLeaveEvent` | method | `lazygui/widgets/graph_view.py:272` | `def hoverLeaveEvent(self, event)` |
| `itemChange` | method | `lazygui/widgets/graph_view.py:278` | `def itemChange(self, change, value)` |
| `mousePressEvent` | method | `lazygui/widgets/graph_view.py:247` | `def mousePressEvent(self, event)` |
| `mouseReleaseEvent` | method | `lazygui/widgets/graph_view.py:258` | `def mouseReleaseEvent(self, event)` |
| `node_data` | method | `lazygui/widgets/graph_view.py:185` | `def node_data(self)` |
| `paint` | method | `lazygui/widgets/graph_view.py:189` | `def paint(self, painter, option, widget)` |
| `scene_handle` | method | `lazygui/widgets/graph_view.py:566` | `def scene_handle(self)` |
| `selected_node_id` | method | `lazygui/widgets/graph_view.py:487` | `def selected_node_id(self)` |
| `selected_node_id` | method | `lazygui/widgets/graph_view.py:557` | `def selected_node_id(self)` |
| `set_theme_colors` | method | `lazygui/widgets/graph_view.py:523` | `def set_theme_colors(self, bg_color, edge_color)` |
| `set_topology` | method | `lazygui/widgets/graph_view.py:348` | `def set_topology(self, topology)` |
| `set_topology` | method | `lazygui/widgets/graph_view.py:531` | `def set_topology(self, topology)` |
| `step_physics` | method | `lazygui/widgets/graph_view.py:415` | `def step_physics(self)` |
| `update_position` | method | `lazygui/widgets/graph_view.py:323` | `def update_position(self)` |
| `wheelEvent` | method | `lazygui/widgets/graph_view.py:547` | `def wheelEvent(self, event)` |
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
| `_on_action_invoked` | method | `lazygui/windows/command_palette_window.py:75` | `def _on_action_invoked(self, action)` |
| `keyPressEvent` | method | `lazygui/windows/command_palette_window.py:48` | `def keyPressEvent(self, event)` |
| `set_actions` | method | `lazygui/windows/command_palette_window.py:43` | `def set_actions(self, actions)` |
| `showEvent` | method | `lazygui/windows/command_palette_window.py:69` | `def showEvent(self, event)` |
| `ConnectDialog` | class | `lazygui/windows/connect_dialog.py:50` | `class ConnectDialog(QDialog)` |
| `ConnectionRequest` | class | `lazygui/windows/connect_dialog.py:39` | `class ConnectionRequest` |
| `__init__` | method | `lazygui/windows/connect_dialog.py:53` | `def __init__(self, constants, settings, paths, parent)` |
| `_build_local_page` | method | `lazygui/windows/connect_dialog.py:136` | `def _build_local_page(self)` |
| `_build_teamserver_page` | method | `lazygui/windows/connect_dialog.py:151` | `def _build_teamserver_page(self)` |
| `_on_kind_changed` | method | `lazygui/windows/connect_dialog.py:187` | `def _on_kind_changed(self, index)` |
| `_restore_last_choice` | method | `lazygui/windows/connect_dialog.py:169` | `def _restore_last_choice(self)` |
| `persist_choice` | method | `lazygui/windows/connect_dialog.py:121` | `def persist_choice(self)` |
| `request` | method | `lazygui/windows/connect_dialog.py:106` | `def request(self)` |
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
| `LazyOwnShell` | class | `lazyown.py:253` | `class LazyOwnShell(Cmd)` |
| `_PayloadSettableProxy` | class | `lazyown.py:226` | `class _PayloadSettableProxy` |
| `__getattr__` | method | `lazyown.py:242` | `def __getattr__(self, name)` |
| `__init__` | method | `lazyown.py:238` | `def __init__(self, params)` |
| `__init__` | method | `lazyown.py:328` | `def __init__(self)` |
| `__setattr__` | method | `lazyown.py:248` | `def __setattr__(self, name, value)` |
| `_build_chain_prompt_engine` | method | `lazyown.py:968` | `def _build_chain_prompt_engine(self)` |
| `_build_command_stack` | method | `lazyown.py:4771` | `def _build_command_stack(self, adversary, r)` |
| `_build_scope_offensive` | method | `lazyown.py:1571` | `def _build_scope_offensive(self)` |
| `_chain_boot_prompt` | method | `lazyown.py:953` | `def _chain_boot_prompt(self)` |
| `_chain_part_exists` | method | `lazyown.py:1543` | `def _chain_part_exists(self, part)` |
| `_chain_perror` | method | `lazyown.py:1497` | `def _chain_perror()` |
| `_chain_resolver` | method | `lazyown.py:993` | `def _chain_resolver(self, cmd, phase)` |
| `_create_strict_yaml_prompt` | method | `lazyown.py:4592` | `def _create_strict_yaml_prompt(self, base_prompt, nmap_services, knowledge_base)` |
| `_did_you_mean` | method | `lazyown.py:1149` | `def _did_you_mean(self, query, limit)` |
| `_display_adversary_info` | method | `lazyown.py:4785` | `def _display_adversary_info(self, adversary, commands)` |
| `_execute_commands` | method | `lazyown.py:4792` | `def _execute_commands(self, confirm, remote_cmds)` |
| `_load_adversaries` | method | `lazyown.py:4738` | `def _load_adversaries(self)` |
| `_load_extended_params` | method | `lazyown.py:681` | `def _load_extended_params(self)` |
| `_maybe_chain_prompt` | method | `lazyown.py:1013` | `def _maybe_chain_prompt(self, cmd, phase)` |
| `_parse_adversary_args` | method | `lazyown.py:4752` | `def _parse_adversary_args(self, line)` |
| `_parse_bool_setting` | function | `lazyown.py:202` | `def _parse_bool_setting(value)` |
| `_patch_template_if_needed` | method | `lazyown.py:4761` | `def _patch_template_if_needed(self, adversary, path, replacements)` |
| `_persist` | method | `lazyown.py:627` | `def _persist(name, _old, _new)` |
| `_read_recent_commands_for_autosuggest` | method | `lazyown.py:1083` | `def _read_recent_commands_for_autosuggest(self, limit)` |
| `_recording_hook` | method | `lazyown.py:1136` | `def _recording_hook(self, data)` |
| `_refresh_autosuggest` | method | `lazyown.py:1110` | `def _refresh_autosuggest(self, executed_command)` |
| `_register_adversary_command` | method | `lazyown.py:2164` | `def _register_adversary_command(self, adv)` |
| `_register_lua_command` | method | `lazyown.py:1938` | `def _register_lua_command(self, command_name, lua_function)` |
| `_register_ux_settables` | method | `lazyown.py:610` | `def _register_ux_settables(self)` |
| `_render_chain_next` | method | `lazyown.py:4217` | `def _render_chain_next(self, raw_args)` |
| `_resolve_offensive` | method | `lazyown.py:1592` | `def _resolve_offensive(self, name)` |
| `_run_and_chain` | method | `lazyown.py:1460` | `def _run_and_chain(self, parts, add_to_history, raise_keyboard_interrupt)` |
| `_run_auto_decrypt` | method | `lazyown.py:1059` | `def _run_auto_decrypt(self)` |
| `_run_auto_encrypt` | method | `lazyown.py:1071` | `def _run_auto_encrypt(self)` |
| `_scope_check` | method | `lazyown.py:1611` | `def _scope_check(self, cmd_name)` |
| `_scope_confirm` | method | `lazyown.py:1658` | `def _scope_confirm(self, decision)` |
| `_scope_entries` | method | `lazyown.py:2533` | `def _scope_entries(self)` |
| `_scope_render` | method | `lazyown.py:2557` | `def _scope_render(self, entries, mode)` |
| `_scope_save` | method | `lazyown.py:2539` | `def _scope_save(self, entries, mode)` |
| `_split_and_chain` | method | `lazyown.py:1415` | `def _split_and_chain(raw_input)` |
| `_sync_c2_credentials` | method | `lazyown.py:4342` | `def _sync_c2_credentials(self)` |
| `_sync_chain_active` | method | `lazyown.py:939` | `def _sync_chain_active(self, tips_engine)` |
| `_toast_hook` | method | `lazyown.py:875` | `def _toast_hook(self, data)` |
| `_ui_hints_level` | method | `lazyown.py:864` | `def _ui_hints_level(self)` |
| `_unified_tips_hook` | method | `lazyown.py:901` | `def _unified_tips_hook(self, data)` |
| `_ux_debug` | function | `lazyown.py:150` | `def _ux_debug(context, exc)` |
| `_wrap_text` | method | `lazyown.py:2239` | `def _wrap_text(self, text, max_width)` |
| `cmd` | method | `lazyown.py:1224` | `def cmd(self, line)` |
| `cmd_wrapper` | method | `lazyown.py:2173` | `def cmd_wrapper(_)` |
| `complete_assign` | method | `lazyown.py:2502` | `def complete_assign(self, text, line, begidx, endidx)` |
| `complete_issue_command_to_c2` | method | `lazyown.py:4404` | `def complete_issue_command_to_c2(self, text, line, begidx, endidx)` |
| `complete_l00t` | method | `lazyown.py:2489` | `def complete_l00t(self, text, line, begidx, endidx)` |
| `complete_loot` | method | `lazyown.py:2496` | `def complete_loot(self, text, line, begidx, endidx)` |
| `complete_palette` | method | `lazyown.py:2572` | `def complete_palette(self, text, line, begidx, endidx)` |
| `complete_phase` | method | `lazyown.py:2483` | `def complete_phase(self, text, line, begidx, endidx)` |
| `complete_scope` | method | `lazyown.py:2520` | `def complete_scope(self, text, line, begidx, endidx)` |
| `complete_upload_c2` | method | `lazyown.py:4283` | `def complete_upload_c2(self, text, line, begidx, endidx)` |
| `completedefault` | method | `lazyown.py:2257` | `def completedefault(self, text, line, begidx, endidx)` |
| `default` | method | `lazyown.py:777` | `def default(self, line)` |
| `display_toastr` | method | `lazyown.py:2180` | `def display_toastr(self, message, type)` |
| `do_event_log` | method | `lazyown.py:4809` | `def do_event_log(self, line)` |
| `do_route` | method | `lazyown.py:4870` | `def do_route(self, line)` |
| `do_set` | method | `lazyown.py:839` | `def do_set(self, line)` |
| `do_state_snapshot` | method | `lazyown.py:4838` | `def do_state_snapshot(self, line)` |
| `download_file_from_c2` | method | `lazyown.py:4313` | `def download_file_from_c2(self, file_name, clientid)` |
| `emptyline` | method | `lazyown.py:1728` | `def emptyline(self)` |
| `get_available_actions` | method | `lazyown.py:4585` | `def get_available_actions(self)` |
| `get_output` | method | `lazyown.py:4252` | `def get_output(self)` |
| `issue_command_to_c2` | method | `lazyown.py:4372` | `def issue_command_to_c2(self, command, client_id)` |
| `list_files_in_directory` | method | `lazyown.py:1777` | `def list_files_in_directory(self, directory)` |
| `load_plugins` | method | `lazyown.py:1963` | `def load_plugins(self)` |
| `load_user_commands` | method | `lazyown.py:1753` | `def load_user_commands(self)` |
| `load_yaml_plugins` | method | `lazyown.py:1993` | `def load_yaml_plugins(self)` |
| `log_command` | method | `lazyown.py:714` | `def log_command(self, cmd_name, cmd_args, start_time, end_time, duration_ms)` |
| `logcsv` | method | `lazyown.py:1189` | `def logcsv(self, line, start_time, end_time, duration_ms)` |
| `main` | method | `lazyown.py:4892` | `def main()` |
| `make_wrapper` | method | `lazyown.py:1842` | `def make_wrapper(cmd_template, tname, default_target)` |
| `one_cmd` | method | `lazyown.py:1682` | `def one_cmd(self, command)` |
| `onecmd_plus_hooks` | method | `lazyown.py:1321` | `def onecmd_plus_hooks(self, statement, add_to_history, raise_keyboard_interrupt, orig_rl_history_length)` |
| `postloop` | method | `lazyown.py:2449` | `def postloop(self)` |
| `postparsing_precmd` | method | `lazyown.py:2423` | `def postparsing_precmd(self, statement)` |
| `preloop` | method | `lazyown.py:2285` | `def preloop(self)` |
| `process_scan_csv` | method | `lazyown.py:4668` | `def process_scan_csv(self, csv_file, ip, port, all_data, processed_ips)` |
| `process_vuln_csv` | method | `lazyown.py:4691` | `def process_vuln_csv(self, csv_file, ip, all_data, processed_ips)` |
| `refresh_prompt` | method | `lazyown.py:828` | `def refresh_prompt(self)` |
| `register_all_adversary_commands` | method | `lazyown.py:2151` | `def register_all_adversary_commands(self)` |
| `register_tool_commands` | method | `lazyown.py:1783` | `def register_tool_commands(self)` |
| `register_yaml_plugin` | method | `lazyown.py:2016` | `def register_yaml_plugin(self, plugin_data)` |
| `run_command` | method | `lazyown.py:4167` | `def run_command(self, command)` |
| `run_lazyarpspoofing` | method | `lazyown.py:3768` | `def run_lazyarpspoofing(self)` |
| `run_lazyaslrcheck` | method | `lazyown.py:4050` | `def run_lazyaslrcheck(self)` |
| `run_lazyattack` | method | `lazyown.py:3822` | `def run_lazyattack(self)` |
| `run_lazybotcli` | method | `lazyown.py:3482` | `def run_lazybotcli(self)` |
| `run_lazybotnet` | method | `lazyown.py:3291` | `def run_lazybotnet(self)` |
| `run_lazyburpfuzzer` | method | `lazyown.py:3590` | `def run_lazyburpfuzzer(self)` |
| `run_lazyftpsniff` | method | `lazyown.py:2916` | `def run_lazyftpsniff(self)` |
| `run_lazygath` | method | `lazyown.py:2819` | `def run_lazygath(self)` |
| `run_lazyhoneypot` | method | `lazyown.py:3013` | `def run_lazyhoneypot(self)` |
| `run_lazylfi2rce` | method | `lazyown.py:3347` | `def run_lazylfi2rce(self)` |
| `run_lazylogpoisoning` | method | `lazyown.py:3435` | `def run_lazylogpoisoning(self)` |
| `run_lazymetaextract0r` | method | `lazyown.py:3129` | `def run_lazymetaextract0r(self)` |
| `run_lazymsfvenom` | method | `lazyown.py:3879` | `def run_lazymsfvenom(self)` |
| `run_lazynetbios` | method | `lazyown.py:2962` | `def run_lazynetbios(self)` |
| `run_lazynmap` | method | `lazyown.py:2692` | `def run_lazynmap(self)` |
| `run_lazynmapdiscovery` | method | `lazyown.py:2851` | `def run_lazynmapdiscovery(self)` |
| `run_lazyown` | method | `lazyown.py:2636` | `def run_lazyown(self)` |
| `run_lazyownrat` | method | `lazyown.py:3230` | `def run_lazyownrat(self)` |
| `run_lazyownratcli` | method | `lazyown.py:3170` | `def run_lazyownratcli(self)` |
| `run_lazypathhijacking` | method | `lazyown.py:4100` | `def run_lazypathhijacking(self)` |
| `run_lazyreverse_shell` | method | `lazyown.py:3716` | `def run_lazyreverse_shell(self)` |
| `run_lazysearch` | method | `lazyown.py:2589` | `def run_lazysearch(self)` |
| `run_lazysearch_bot` | method | `lazyown.py:3078` | `def run_lazysearch_bot(self)` |
| `run_lazysearch_gui` | method | `lazyown.py:2606` | `def run_lazysearch_gui(self)` |
| `run_lazysniff` | method | `lazyown.py:2866` | `def run_lazysniff(self)` |
| `run_lazyssh77enum` | method | `lazyown.py:3538` | `def run_lazyssh77enum(self)` |
| `run_lazywerkzeugdebug` | method | `lazyown.py:2760` | `def run_lazywerkzeugdebug(self)` |
| `run_script` | method | `lazyown.py:4135` | `def run_script(self, script_name)` |
| `run_update_db` | method | `lazyown.py:2662` | `def run_update_db(self)` |
| `save_user_command` | method | `lazyown.py:1765` | `def save_user_command(self, alias, command)` |
| `scripts` | method | `lazyown.py:808` | `def scripts(self)` |
| `show_toastr` | method | `lazyown.py:2234` | `def show_toastr()` |
| `tool_wrapper` | method | `lazyown.py:1843` | `def tool_wrapper(arg)` |
| `upload_file_to_c2` | method | `lazyown.py:4257` | `def upload_file_to_c2(self, file_path, clientid)` |
| `view_code` | method | `lazyown.py:4472` | `def view_code(self, stdscr)` |
| `wrapper` | method | `lazyown.py:1941` | `def wrapper(arg)` |
| `wrapper_yaml` | method | `lazyown.py:2056` | `def wrapper_yaml(arg)` |
| `auth` | function | `modules/49803.py:42` | `def auth()` |
| `connection` | function | `modules/49803.py:84` | `def connection()` |
| `injection` | function | `modules/49803.py:70` | `def injection()` |
| `poc` | function | `modules/CVE-2023-28432.py:10` | `def poc(url)` |
| `AutocompleteEntry` | class | `modules/LazyOwnExplorer.py:29` | `class AutocompleteEntry(Entry)` |
| `LazyOwnGUI` | class | `modules/LazyOwnExplorer.py:101` | `class LazyOwnGUI(Tk)` |
| `__init__` | method | `modules/LazyOwnExplorer.py:30` | `def __init__(self, get_suggestions_func)` |
| `__init__` | method | `modules/LazyOwnExplorer.py:102` | `def __init__(self)` |
| `add_new_attack_vector` | method | `modules/LazyOwnExplorer.py:295` | `def add_new_attack_vector(self)` |
| `changed` | method | `modules/LazyOwnExplorer.py:44` | `def changed(self, name, index, mode)` |
| `comparison` | method | `modules/LazyOwnExplorer.py:98` | `def comparison(self, pattern)` |
| `create_widgets` | method | `modules/LazyOwnExplorer.py:116` | `def create_widgets(self)` |
| `export_to_csv` | method | `modules/LazyOwnExplorer.py:371` | `def export_to_csv(self)` |
| `get_suggestions` | method | `modules/LazyOwnExplorer.py:121` | `def get_suggestions(term)` |
| `get_unique_values` | method | `modules/LazyOwnExplorer.py:235` | `def get_unique_values(self)` |
| `is_binary` | method | `modules/LazyOwnExplorer.py:344` | `def is_binary(file_path)` |
| `load_parquet_files` | method | `modules/LazyOwnExplorer.py:176` | `def load_parquet_files(self)` |
| `move_down` | method | `modules/LazyOwnExplorer.py:86` | `def move_down(self, event)` |
| `move_up` | method | `modules/LazyOwnExplorer.py:74` | `def move_up(self, event)` |
| `on_row_double_click` | method | `modules/LazyOwnExplorer.py:268` | `def on_row_double_click(self, event)` |
| `save_new_vector` | method | `modules/LazyOwnExplorer.py:315` | `def save_new_vector()` |
| `scan_system_for_binaries` | method | `modules/LazyOwnExplorer.py:343` | `def scan_system_for_binaries(self)` |
| `search` | method | `modules/LazyOwnExplorer.py:242` | `def search(self)` |
| `search_in_parquet` | method | `modules/LazyOwnExplorer.py:259` | `def search_in_parquet(self, term)` |
| `selection` | method | `modules/LazyOwnExplorer.py:67` | `def selection(self, event)` |
| `show_row_details` | method | `modules/LazyOwnExplorer.py:273` | `def show_row_details(self, row)` |
| `show_scan_results` | method | `modules/LazyOwnExplorer.py:360` | `def show_scan_results(self, binaries)` |
| `ADCSCertipyWrapper` | class | `modules/adcs_attacks.py:69` | `class ADCSCertipyWrapper` |
| `CertificateTemplate` | class | `modules/adcs_attacks.py:14` | `class CertificateTemplate` |
| `__init__` | method | `modules/adcs_attacks.py:80` | `def __init__(self, certipy_path, timeout)` |
| `_find_certipy` | method | `modules/adcs_attacks.py:85` | `def _find_certipy()` |
| `_parse_ca_output` | method | `modules/adcs_attacks.py:155` | `def _parse_ca_output(output)` |
| `_parse_template_output` | method | `modules/adcs_attacks.py:226` | `def _parse_template_output(self, output)` |
| `_run` | method | `modules/adcs_attacks.py:95` | `def _run(self, args, capture)` |
| `assess_vulnerability` | method | `modules/adcs_attacks.py:400` | `def assess_vulnerability(self, username, password, domain, dc_ip, hashes)` |
| `authenticate_with_certificate` | method | `modules/adcs_attacks.py:361` | `def authenticate_with_certificate(self, cert_file, domain, dc_ip, username)` |
| `enumerate_templates` | method | `modules/adcs_attacks.py:187` | `def enumerate_templates(self, username, password, domain, dc_ip, hashes)` |
| `esc_vulnerabilities` | method | `modules/adcs_attacks.py:35` | `def esc_vulnerabilities(self)` |
| `find_certificate_authorities` | method | `modules/adcs_attacks.py:115` | `def find_certificate_authorities(self, username, password, domain, dc_ip, hashes)` |
| `request_certificate_esc1` | method | `modules/adcs_attacks.py:271` | `def request_certificate_esc1(self, username, password, domain, dc_ip, ca_name, template_name, target_user, output_file)` |
| `request_certificate_esc8` | method | `modules/adcs_attacks.py:320` | `def request_certificate_esc8(self, username, password, domain, dc_ip, ca_server, template_name, output_file)` |
| `ASTToolExtractor` | class | `modules/agent_runner.py:135` | `class ASTToolExtractor` |
| `AgentRunner` | class | `modules/agent_runner.py:177` | `class AgentRunner` |
| `AgentTool` | class | `modules/agent_runner.py:63` | `class AgentTool` |
| `CommandMetadata` | class | `modules/agent_runner.py:129` | `class CommandMetadata` |
| `LazyOwnShellWrapper` | class | `modules/agent_runner.py:357` | `class LazyOwnShellWrapper` |
| `VulnBotCLI` | class | `modules/agent_runner.py:434` | `class VulnBotCLI` |
| `__init__` | method | `modules/agent_runner.py:66` | `def __init__(self, name, description, func, parameters, required)` |
| `__init__` | method | `modules/agent_runner.py:180` | `def __init__(self, model, system_prompt, max_iterations)` |
| `__init__` | method | `modules/agent_runner.py:360` | `def __init__(self, script_path)` |
| `__init__` | method | `modules/agent_runner.py:436` | `def __init__(self, provider, mode, debug, script_path)` |
| `_call_model` | method | `modules/agent_runner.py:283` | `def _call_model(self)` |
| `_load_model` | method | `modules/agent_runner.py:448` | `def _load_model(self)` |
| `_load_shell` | method | `modules/agent_runner.py:367` | `def _load_shell(self)` |
| `_manage_memory` | method | `modules/agent_runner.py:200` | `def _manage_memory(self)` |
| `_process_tool_call` | method | `modules/agent_runner.py:306` | `def _process_tool_call(self, tool_call)` |
| `_reset_history` | method | `modules/agent_runner.py:194` | `def _reset_history(self)` |
| `_setup_agent` | method | `modules/agent_runner.py:463` | `def _setup_agent(self)` |
| `configure_logging` | function | `modules/agent_runner.py:58` | `def configure_logging(debug)` |
| `execute` | method | `modules/agent_runner.py:87` | `def execute(self)` |
| `execute_command` | method | `modules/agent_runner.py:390` | `def execute_command(self, command)` |
| `extract_commands_from_file` | method | `modules/agent_runner.py:139` | `def extract_commands_from_file(file_path, prefix)` |
| `get_commands_summary` | method | `modules/agent_runner.py:427` | `def get_commands_summary(self)` |
| `get_tools_for_api` | method | `modules/agent_runner.py:254` | `def get_tools_for_api(self)` |
| `interactive_mode` | method | `modules/agent_runner.py:499` | `def interactive_mode(bot)` |
| `main` | method | `modules/agent_runner.py:531` | `def main()` |
| `make_executor` | method | `modules/agent_runner.py:232` | `def make_executor(cmd_name)` |
| `parse_args` | method | `modules/agent_runner.py:522` | `def parse_args()` |
| `process_request` | method | `modules/agent_runner.py:494` | `def process_request(self, user_input)` |
| `register_tool` | method | `modules/agent_runner.py:208` | `def register_tool(self, tool)` |
| `register_tool_from_instance` | method | `modules/agent_runner.py:211` | `def register_tool_from_instance(self, func)` |
| `register_tools_from_metadata` | method | `modules/agent_runner.py:229` | `def register_tools_from_metadata(self, commands, executor)` |
| `run` | method | `modules/agent_runner.py:259` | `def run(self, user_input)` |
| `target` | method | `modules/agent_runner.py:397` | `def target()` |
| `to_api_format` | method | `modules/agent_runner.py:77` | `def to_api_format(self)` |
| `wrapper` | method | `modules/agent_runner.py:233` | `def wrapper(command)` |
| `AgentTool` | class | `modules/agent_tool.py:7` | `class AgentTool` |
| `__init__` | method | `modules/agent_tool.py:10` | `def __init__(self, name, description, func, parameters, required)` |
| `execute` | method | `modules/agent_tool.py:32` | `def execute(self)` |
| `to_api_format` | method | `modules/agent_tool.py:21` | `def to_api_format(self)` |
| `AIExploitChainer` | class | `modules/ai_exploit_chain.py:178` | `class AIExploitChainer` |
| `ExploitChainContext` | class | `modules/ai_exploit_chain.py:154` | `class ExploitChainContext` |
| `__init__` | method | `modules/ai_exploit_chain.py:190` | `def __init__(self)` |
| `_ensure` | method | `modules/ai_exploit_chain.py:400` | `def _ensure(context, strategy)` |
| `_parse_shell_hints` | method | `modules/ai_exploit_chain.py:405` | `def _parse_shell_hints(self, output, context)` |
| `adapt_chain` | method | `modules/ai_exploit_chain.py:344` | `def adapt_chain(self, context, new_info)` |
| `build_chain_plan` | method | `modules/ai_exploit_chain.py:311` | `def build_chain_plan(self, context)` |
| `estimate_confidence` | method | `modules/ai_exploit_chain.py:269` | `def estimate_confidence(self, strategy, profile)` |
| `evaluate_failure` | method | `modules/ai_exploit_chain.py:223` | `def evaluate_failure(result)` |
| `reason` | method | `modules/ai_exploit_chain.py:203` | `def reason(self, context)` |
| `select_next_strategy` | method | `modules/ai_exploit_chain.py:235` | `def select_next_strategy(self, context)` |
| `AIResult` | class | `modules/ai_fallback.py:89` | `class AIResult` |
| `_best_ollama_model` | method | `modules/ai_fallback.py:107` | `def _best_ollama_model()` |
| `_groq_call` | method | `modules/ai_fallback.py:183` | `def _groq_call(api_key, system, user, max_tokens, temperature)` |
| `_is_quota_error` | method | `modules/ai_fallback.py:178` | `def _is_quota_error(exc)` |
| `_ollama_available` | method | `modules/ai_fallback.py:99` | `def _ollama_available()` |
| `_ollama_call` | method | `modules/ai_fallback.py:134` | `def _ollama_call(model, system, user, max_tokens, temperature)` |
| `_toposwarm_call` | method | `modules/ai_fallback.py:210` | `def _toposwarm_call(prompt, system)` |
| `call` | method | `modules/ai_fallback.py:238` | `def call(prompt, system, api_key, max_tokens, temperature)` |
| `AIModel` | class | `modules/ai_model.py:41` | `class AIModel(ABC)` |
| `AnthropicModel` | class | `modules/ai_model.py:328` | `class AnthropicModel(AIModel)` |
| `DeepSeekModel` | class | `modules/ai_model.py:384` | `class DeepSeekModel(AIModel)` |
| `GroqModel` | class | `modules/ai_model.py:122` | `class GroqModel(AIModel)` |
| `OllamaModel` | class | `modules/ai_model.py:202` | `class OllamaModel(AIModel)` |
| `OpenAIModel` | class | `modules/ai_model.py:269` | `class OpenAIModel(AIModel)` |
| `_LazyImporter` | class | `modules/ai_model.py:93` | `class _LazyImporter` |
| `__init__` | method | `modules/ai_model.py:130` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:210` | `def __init__(self, model, host)` |
| `__init__` | method | `modules/ai_model.py:275` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:334` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:391` | `def __init__(self, api_key, model)` |
| `anthropic` | method | `modules/ai_model.py:115` | `def anthropic(cls)` |
| `complete` | method | `modules/ai_model.py:59` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:174` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:305` | `def complete(self, system, user, max_tokens, temperature)` |

Next: [SYMBOLS_p10.md](SYMBOLS_p10.md)
