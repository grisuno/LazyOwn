# Subsystem: widgets

## lazygui/widgets/__init__.py
- Layer: presentation
- Language: py
- Depends on: `lazygui/widgets/command_palette_list.py`, `lazygui/widgets/event_log_view.py`, `lazygui/widgets/filter_bar.py`, `lazygui/widgets/graph_view.py`, `lazygui/widgets/status_badge.py`, `lazygui/widgets/terminal_view.py`

## lazygui/widgets/beacon_command_modal.py
- Layer: presentation
- Language: py
- Symbols:
  - `_HistoryEntry` (class, line 35) `class _HistoryEntry`
  - `BeaconCommandModal` (class, line 44) `class BeaconCommandModal(QDialog)`
  - `__init__` (method, line 53) `def __init__(self, backend, parent)`
  - `_build_ui` (method, line 75) `def _build_ui(self)`
  - `_selected_target` (method, line 122) `def _selected_target(self)`
  - `_on_target_changed` (method, line 127) `def _on_target_changed(self, _text)`
  - `_reload_history` (method, line 131) `def _reload_history(self)`
  - `_on_sessions_changed` (method, line 168) `def _on_sessions_changed(self, sessions)`
  - `_send_command` (method, line 182) `def _send_command(self)`
  - `_on_history_clicked` (method, line 196) `def _on_history_clicked(self, item)`
  - `_last_entry` (method, line 201) `def _last_entry(self, index)`
  - `_on_beacon_result` (method, line 209) `def _on_beacon_result(self, result)`
  - `open` (method, line 218) `def open(self)`
  - `focus_input` (method, line 229) `def focus_input(self)`
- Depends on: `lazygui/services/backend.py`, `lazygui/services/models.py`
- Imported by: `lazygui/windows/main_window.py`

## lazygui/widgets/command_palette_list.py
- Layer: presentation
- Language: py
- Symbols:
  - `CommandPaletteAction` (class, line 16) `class CommandPaletteAction`
  - `CommandPaletteList` (class, line 28) `class CommandPaletteList(QListView)`
  - `_fuzzy_score` (method, line 99) `def _fuzzy_score(query, title, subtitle)`
  - `_token_order_score` (method, line 114) `def _token_order_score(query, haystack, base_offset)`
  - `__init__` (method, line 33) `def __init__(self, constants, actions, parent)`
  - `set_actions` (method, line 53) `def set_actions(self, actions)`
  - `apply_filter` (method, line 58) `def apply_filter(self, query)`
  - `invoke_current` (method, line 76) `def invoke_current(self)`
  - `_on_activated` (method, line 85) `def _on_activated(self, _index)`
  - `_populate` (method, line 89) `def _populate(self, actions)`
- Depends on: `lazygui/config/constants.py`
- Imported by: `lazygui/widgets/__init__.py`, `lazygui/windows/command_palette_window.py`, `lazygui/windows/main_window.py`

## lazygui/widgets/event_log_view.py
- Layer: presentation
- Language: py
- Symbols:
  - `EventLogView` (class, line 20) `class EventLogView(QTreeWidget)`
  - `__init__` (method, line 23) `def __init__(self, constants, event_log, parent)`
  - `set_minimum_level` (method, line 51) `def set_minimum_level(self, level)`
  - `minimum_level` (method, line 61) `def minimum_level(self)`
  - `_on_record_appended` (method, line 65) `def _on_record_appended(self, record)`
  - `_append_record` (method, line 71) `def _append_record(self, record)`
- Depends on: `lazygui/config/constants.py`, `lazygui/services/event_log.py`, `lazygui/services/models.py`
- Imported by: `lazygui/panels/event_log_panel.py`, `lazygui/widgets/__init__.py`

## lazygui/widgets/filter_bar.py
- Layer: presentation
- Language: py
- Symbols:
  - `FilterBar` (class, line 11) `class FilterBar(QWidget)`
  - `__init__` (method, line 16) `def __init__(self, constants, placeholder_text, label_text, parent)`
  - `text` (method, line 42) `def text(self)`
  - `clear` (method, line 46) `def clear(self)`
  - `_on_text_changed` (method, line 50) `def _on_text_changed(self, _value)`
  - `_emit_filter_changed` (method, line 54) `def _emit_filter_changed(self)`
- Depends on: `lazygui/config/constants.py`
- Imported by: `lazygui/panels/listeners_panel.py`, `lazygui/panels/sessions_panel.py`, `lazygui/widgets/__init__.py`

## lazygui/widgets/graph_view.py
- Layer: presentation
- Language: py
- Symbols:
  - `_resolve_icon_dir` (function, line 47) `def _resolve_icon_dir()`
  - `_load_icon` (function, line 63) `def _load_icon(name)`
  - `_icon_for_node` (function, line 81) `def _icon_for_node(node)`
  - `GraphNodeState` (class, line 131) `class GraphNodeState`
  - `GraphNodeItem` (class, line 139) `class GraphNodeItem(QGraphicsEllipseItem)`
  - `GraphEdgeItem` (class, line 284) `class GraphEdgeItem(QGraphicsLineItem)`
  - `GraphScene` (class, line 333) `class GraphScene(QGraphicsScene)`
  - `GraphView` (class, line 495) `class GraphView(QGraphicsView)`
  - `_resolve_node_color` (method, line 571) `def _resolve_node_color(node)`
  - `_resolve_node_radius` (method, line 580) `def _resolve_node_radius(node)`
  - `__init__` (method, line 142) `def __init__(self, node, radius, color, pixmap, on_selected, on_context_menu, label_visible, parent)`
  - `_create_label` (method, line 172) `def _create_label(self)`
  - `node_data` (method, line 185) `def node_data(self)`
  - `paint` (method, line 189) `def paint(self, painter, option, widget)`
  - `mousePressEvent` (method, line 247) `def mousePressEvent(self, event)`
  - `mouseReleaseEvent` (method, line 258) `def mouseReleaseEvent(self, event)`
  - `hoverEnterEvent` (method, line 265) `def hoverEnterEvent(self, event)`
  - `hoverLeaveEvent` (method, line 272) `def hoverLeaveEvent(self, event)`
  - `itemChange` (method, line 278) `def itemChange(self, change, value)`
  - `__init__` (method, line 287) `def __init__(self, edge, source_item, target_item, parent)`
  - `_update_position` (method, line 312) `def _update_position(self)`
  - `update_position` (method, line 323) `def update_position(self)`
  - `edge_data` (method, line 328) `def edge_data(self)`
  - `__init__` (method, line 339) `def __init__(self, constants, parent)`
  - `set_topology` (method, line 348) `def set_topology(self, topology)`
  - `_add_node` (method, line 368) `def _add_node(self, node)`
  - `_add_edge` (method, line 389) `def _add_edge(self, edge)`
  - `_apply_force_layout` (method, line 398) `def _apply_force_layout(self)`
  - `step_physics` (method, line 415) `def step_physics(self)`
  - `selected_node_id` (method, line 487) `def selected_node_id(self)`
  - `__init__` (method, line 505) `def __init__(self, constants, parent)`
  - `set_theme_colors` (method, line 523) `def set_theme_colors(self, bg_color, edge_color)`
  - `set_topology` (method, line 531) `def set_topology(self, topology)`
  - `_install_physics_timer` (method, line 536) `def _install_physics_timer(self)`
  - `_tick_physics` (method, line 544) `def _tick_physics(self)`
  - `wheelEvent` (method, line 547) `def wheelEvent(self, event)`
  - `selected_node_id` (method, line 557) `def selected_node_id(self)`
  - `fit_to_content` (method, line 561) `def fit_to_content(self)`
  - `scene_handle` (method, line 566) `def scene_handle(self)`
  - `_on_selected` (method, line 373) `def _on_selected(nid)`
  - `_on_context_menu` (method, line 376) `def _on_context_menu(nid, pos)`
- Depends on: `lazygui/config/constants.py`, `lazygui/services/models.py`
- Imported by: `lazygui/panels/graph_panel.py`, `lazygui/widgets/__init__.py`, `mutants/tests/test_lazygui_graph_widget.py`, `tests/test_lazygui_graph_widget.py`

## lazygui/widgets/status_badge.py
- Layer: presentation
- Language: py
- Symbols:
  - `StatusBadge` (class, line 18) `class StatusBadge(QLabel)`
  - `__init__` (method, line 21) `def __init__(self, parent)`
  - `set_status` (method, line 27) `def set_status(self, status)`
- Depends on: `lazygui/services/backend.py`
- Imported by: `lazygui/widgets/__init__.py`, `lazygui/windows/main_window.py`

## lazygui/widgets/terminal_view.py
- Layer: presentation
- Language: py
- Symbols:
  - `TerminalView` (class, line 33) `class TerminalView(QPlainTextEdit)`
  - `__init__` (method, line 38) `def __init__(self, constants, parent)`
  - `append_output` (method, line 54) `def append_output(self, text)`
  - `_sanitize` (method, line 66) `def _sanitize(raw)`
  - `keyPressEvent` (method, line 75) `def keyPressEvent(self, event)`
  - `_translate_key_event` (method, line 85) `def _translate_key_event(event)`
- Depends on: `lazygui/config/constants.py`
- Imported by: `lazygui/panels/terminal_panel.py`, `lazygui/widgets/__init__.py`
