# Subsystem: lazygui

## lazygui/__init__.py
- Layer: presentation
- Language: py
- Depends on: `lazygui/version.py`

## lazygui/__main__.py
- Layer: presentation
- Language: py
- Symbols:
  - `main` (function, line 14) `def main()`
- Depends on: `lazygui/app.py`

## lazygui/app.py
- Layer: presentation
- Language: py
- Symbols:
  - `Application` (class, line 33) `class Application`
  - `__init__` (method, line 36) `def __init__(self, argv)`
  - `run` (method, line 65) `def run(self)`
  - `_discover_credentials` (method, line 73) `def _discover_credentials(self)`
  - `_sync_credentials_to_settings` (method, line 89) `def _sync_credentials_to_settings(self, credentials)`
  - `show_connect_dialog` (method, line 100) `def show_connect_dialog(self)`
  - `_build_initial_backend` (method, line 119) `def _build_initial_backend(self)`
  - `_resolve_teamserver_credentials` (method, line 150) `def _resolve_teamserver_credentials(self)`
  - `_build_backend_from_request` (method, line 167) `def _build_backend_from_request(self, request)`
  - `_swap_backend` (method, line 175) `def _swap_backend(self, new_backend)`
  - `_start_backend` (method, line 194) `def _start_backend(self, backend)`
  - `_configure_qt_attributes` (method, line 213) `def _configure_qt_attributes(self)`
  - `_configure_qt_application_metadata` (method, line 218) `def _configure_qt_application_metadata(self)`
  - `_configure_logging` (method, line 224) `def _configure_logging(self)`
- Depends on: `core/logging.py`, `lazygui/config/c2_credentials.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/factory.py`, `lazygui/services/models.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`
- Imported by: `lazygui/__main__.py`

## lazygui/version.py
- Layer: presentation
- Language: py
- Imported by: `lazygui/__init__.py`, `modules/exploit_recommender.py`, `modules/exploit_recommender.py`
