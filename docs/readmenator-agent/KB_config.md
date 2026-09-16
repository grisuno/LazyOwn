# Subsystem: config

## lazygui/config/__init__.py
- Layer: presentation
- Language: py
- Depends on: `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`

## lazygui/config/c2_credentials.py
- Layer: presentation
- Language: py
- Symbols:
  - `C2Credentials` (class, line 24) `class C2Credentials`
  - `load_c2_credentials_from_file` (method, line 38) `def load_c2_credentials_from_file(file_path)`
  - `load_c2_credentials` (method, line 71) `def load_c2_credentials(project_root)`
  - `empty` (method, line 33) `def empty(cls)`
- Depends on: `core/logging.py`
- Imported by: `lazygui/app.py`, `lazygui/windows/connect_dialog.py`

## lazygui/config/constants.py
- Layer: presentation
- Language: py
- Symbols:
  - `WindowConstants` (class, line 18) `class WindowConstants`
  - `TimingConstants` (class, line 34) `class TimingConstants`
  - `NetworkConstants` (class, line 48) `class NetworkConstants`
  - `PtyConstants` (class, line 86) `class PtyConstants`
  - `FontConstants` (class, line 99) `class FontConstants`
  - `KeybindingConstants` (class, line 124) `class KeybindingConstants`
  - `IdentifierConstants` (class, line 142) `class IdentifierConstants`
  - `ThemeConstants` (class, line 161) `class ThemeConstants`
  - `BackendConstants` (class, line 176) `class BackendConstants`
  - `PanelConstants` (class, line 185) `class PanelConstants`
  - `EventLogConstants` (class, line 205) `class EventLogConstants`
  - `CommandPaletteConstants` (class, line 214) `class CommandPaletteConstants`
  - `AppConstants` (class, line 223) `class AppConstants`
  - `panel_labels` (method, line 239) `def panel_labels(self)`
- Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`, `lazygui/services/event_log.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazygui/theme/qss_builder.py`, `lazygui/widgets/command_palette_list.py`, `lazygui/widgets/event_log_view.py`, `lazygui/widgets/filter_bar.py`, `lazygui/widgets/graph_view.py`, `lazygui/widgets/terminal_view.py`, `lazygui/windows/command_palette_window.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`, `mutants/tests/test_lazygui_backend.py`, `mutants/tests/test_lazygui_backend.py`, `mutants/tests/test_lazygui_graph_widget.py`, `tests/test_lazygui_backend.py`, `tests/test_lazygui_backend.py`, `tests/test_lazygui_graph_widget.py`

## lazygui/config/paths.py
- Layer: presentation
- Language: py
- Symbols:
  - `AppPaths` (class, line 19) `class AppPaths`
  - `_detect_project_root` (method, line 79) `def _detect_project_root()`
  - `config_dir` (method, line 32) `def config_dir(self)`
  - `settings_file` (method, line 39) `def settings_file(self)`
  - `layout_file` (method, line 44) `def layout_file(self)`
  - `project_run_script` (method, line 49) `def project_run_script(self)`
  - `lazyc2_script` (method, line 54) `def lazyc2_script(self)`
  - `c2_credentials_path` (method, line 59) `def c2_credentials_path(self)`
  - `sessions_dir` (method, line 69) `def sessions_dir(self)`
  - `ensure_config_dir` (method, line 73) `def ensure_config_dir(self)`
- Depends on: `lazygui/config/constants.py`
- Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/config/settings.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/windows/connect_dialog.py`

## lazygui/config/settings.py
- Layer: infrastructure
- Language: py
- Symbols:
  - `AppSettings` (class, line 27) `class AppSettings`
  - `load` (method, line 35) `def load(cls, constants, paths)`
  - `save` (method, line 47) `def save(self)`
  - `get` (method, line 55) `def get(self, key, default)`
  - `set` (method, line 59) `def set(self, key, value)`
  - `theme_id` (method, line 64) `def theme_id(self)`
  - `theme_id` (method, line 69) `def theme_id(self, value)`
  - `last_backend_id` (method, line 73) `def last_backend_id(self)`
  - `last_backend_id` (method, line 78) `def last_backend_id(self, value)`
  - `last_teamserver_url` (method, line 84) `def last_teamserver_url(self)`
  - `last_teamserver_url` (method, line 94) `def last_teamserver_url(self, value)`
  - `last_operator_name` (method, line 98) `def last_operator_name(self)`
  - `last_operator_name` (method, line 103) `def last_operator_name(self, value)`
  - `last_teamserver_password` (method, line 107) `def last_teamserver_password(self)`
  - `last_teamserver_password` (method, line 112) `def last_teamserver_password(self, value)`
  - `c2_credentials_loaded` (method, line 116) `def c2_credentials_loaded(self)`
  - `c2_credentials_loaded` (method, line 121) `def c2_credentials_loaded(self, value)`
  - `snapshot` (method, line 124) `def snapshot(self)`
- Depends on: `core/logging.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`
- Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/theme/manager.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`
