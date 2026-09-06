# Subsystem: windows

## lazygui/windows/__init__.py
- Layer: presentation
- Language: py
- Depends on: `lazygui/windows/command_palette_window.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`

## lazygui/windows/command_palette_window.py
- Layer: presentation
- Language: py
- Symbols:
  - `CommandPaletteWindow` (class, line 15) `class CommandPaletteWindow(QWidget)`
  - `__init__` (method, line 18) `def __init__(self, constants, actions, parent)`
  - `set_actions` (method, line 43) `def set_actions(self, actions)`
  - `keyPressEvent` (method, line 48) `def keyPressEvent(self, event)`
  - `showEvent` (method, line 69) `def showEvent(self, event)`
  - `_on_action_invoked` (method, line 75) `def _on_action_invoked(self, action)`
- Depends on: `lazygui/config/constants.py`, `lazygui/widgets/command_palette_list.py`
- Imported by: `lazygui/windows/__init__.py`, `lazygui/windows/main_window.py`

## lazygui/windows/connect_dialog.py
- Layer: presentation
- Language: py
- Symbols:
  - `ConnectionRequest` (class, line 39) `class ConnectionRequest`
  - `ConnectDialog` (class, line 50) `class ConnectDialog(QDialog)`
  - `__init__` (method, line 53) `def __init__(self, constants, settings, paths, parent)`
  - `request` (method, line 106) `def request(self)`
  - `persist_choice` (method, line 121) `def persist_choice(self)`
  - `_build_local_page` (method, line 136) `def _build_local_page(self)`
  - `_build_teamserver_page` (method, line 151) `def _build_teamserver_page(self)`
  - `_restore_last_choice` (method, line 169) `def _restore_last_choice(self)`
  - `_on_kind_changed` (method, line 187) `def _on_kind_changed(self, index)`
- Depends on: `lazygui/config/c2_credentials.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/services/models.py`, `lazygui/services/teamserver_backend.py`
- Imported by: `lazygui/app.py`, `lazygui/windows/__init__.py`

## lazygui/windows/main_window.py
- Layer: presentation
- Language: py
- Symbols:
  - `MainWindow` (class, line 37) `class MainWindow(QMainWindow)`
  - `__init__` (method, line 40) `def __init__(self, constants, settings, theme_manager, backend, event_log, parent)`
  - `closeEvent` (method, line 99) `def closeEvent(self, event)`
  - `_install_layout` (method, line 108) `def _install_layout(self)`
  - `_install_menu_bar` (method, line 131) `def _install_menu_bar(self)`
  - `_install_toolbar` (method, line 171) `def _install_toolbar(self)`
  - `_install_statusbar` (method, line 195) `def _install_statusbar(self)`
  - `_install_shortcuts` (method, line 220) `def _install_shortcuts(self)`
  - `_persist_geometry_and_state` (method, line 244) `def _persist_geometry_and_state(self)`
  - `_restore_geometry_and_state` (method, line 252) `def _restore_geometry_and_state(self)`
  - `_build_palette_actions` (method, line 261) `def _build_palette_actions(self)`
  - `_make_panel_toggle` (method, line 300) `def _make_panel_toggle(self, panel)`
  - `_make_theme_apply` (method, line 311) `def _make_theme_apply(self, identifier)`
  - `_on_operator_changed` (method, line 319) `def _on_operator_changed(self, operator)`
  - `_on_event_logged` (method, line 326) `def _on_event_logged(self, _record)`
  - `_on_theme_changed` (method, line 329) `def _on_theme_changed(self, tokens)`
  - `_on_theme_menu_action` (method, line 337) `def _on_theme_menu_action(self)`
  - `_on_sessions_count_changed` (method, line 345) `def _on_sessions_count_changed(self, sessions)`
  - `_on_dashboard_updated` (method, line 350) `def _on_dashboard_updated(self, dashboard)`
  - `_show_beacon_command_modal` (method, line 354) `def _show_beacon_command_modal(self)`
  - `_show_command_palette` (method, line 361) `def _show_command_palette(self)`
  - `_emit_request_connect` (method, line 372) `def _emit_request_connect(self)`
  - `window_requests_connect` (method, line 376) `def window_requests_connect(self)`
  - `_tick_clock` (method, line 386) `def _tick_clock(self)`
  - `status_badge` (method, line 393) `def status_badge(self)`
  - `panels` (method, line 398) `def panels(self)`
  - `_toggle` (method, line 303) `def _toggle()`
  - `_apply` (method, line 314) `def _apply()`
- Depends on: `lazygui/config/constants.py`, `lazygui/config/settings.py`, `lazygui/panels/registry.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/models.py`, `lazygui/theme/manager.py`, `lazygui/theme/tokens.py`, `lazygui/widgets/beacon_command_modal.py`, `lazygui/widgets/command_palette_list.py`, `lazygui/widgets/status_badge.py`, `lazygui/windows/command_palette_window.py`
- Imported by: `lazygui/app.py`, `lazygui/windows/__init__.py`
