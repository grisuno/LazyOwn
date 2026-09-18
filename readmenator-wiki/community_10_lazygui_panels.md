# lazygui/panels

*Community 10 | 43 files | cohesion 0.91*

## Definition

This community groups 43 file(s) rooted at `lazygui/panels` with dominant language py (cohesion 0.91). Central symbols: `AppConstants`, `AppPaths`, `AppSettings`, `Application`, `Backend`, `BackendConstants`, `BackendDescriptor`, `BackendFactory`. Core file: `tests/test_lazygui_backend.py` (59 symbols). Documented purpose: Entry point for ``python -m lazygui``.  Delegates to :class:`lazygui.app.Application` so command-line invocation and programmatic embedding share the same boots.

## Files

### `lazygui/panels` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/panels/__init__.py` | py | presentation | 0 | yes |
| `lazygui/panels/base.py` | py | presentation | 4 | yes |
| `lazygui/panels/campaign_panel.py` | py | presentation | 9 | yes |

### `lazygui/widgets` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/widgets/__init__.py` | py | presentation | 0 | yes |
| `lazygui/widgets/beacon_command_modal.py` | py | presentation | 14 | yes |
| `lazygui/widgets/command_palette_list.py` | py | presentation | 10 | yes |

### `lazygui/services` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/services/__init__.py` | py | presentation | 0 | yes |
| `lazygui/services/backend.py` | py | presentation | 20 | yes |
| `lazygui/services/event_log.py` | py | presentation | 7 | yes |

### `lazygui/config` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/config/__init__.py` | py | presentation | 0 | yes |
| `lazygui/config/c2_credentials.py` | py | presentation | 4 | yes |
| `lazygui/config/constants.py` | py | presentation | 14 | yes |

### `lazygui/windows` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/windows/__init__.py` | py | presentation | 0 | yes |
| `lazygui/windows/command_palette_window.py` | py | presentation | 6 | yes |
| `lazygui/windows/connect_dialog.py` | py | presentation | 9 | yes |

### `tests` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_lazygui_backend.py` | py | testing | 59 | yes |
| `tests/test_lazygui_graph_widget.py` | py | testing | 51 | yes |
| `tests/test_lazygui_models.py` | py | testing | 42 | yes |

### `lazygui` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/__main__.py` | py | presentation | 1 | yes |
| `lazygui/app.py` | py | presentation | 14 | yes |

*... and 23 more files in this community.*


## Key Symbols

- `main` (function, `lazygui/__main__.py:14`) `def main()` - Bootstrap the GUI and run the Qt event loop.
- `Application` (class, `lazygui/app.py:33`) `class Application` - Owns the QApplication instance and the lifetime of every subsystem.
- `__init__` (method, `lazygui/app.py:36`) `def __init__(self, argv)` - Build constants/settings/theme/backend/main-window.
- `run` (method, `lazygui/app.py:65`) `def run(self)` - Show the main window, start the backend, and run the event loop.
- `_discover_credentials` (method, `lazygui/app.py:73`) `def _discover_credentials(self)` - Attempt to load auto-generated credentials from the project root.
- `_sync_credentials_to_settings` (method, `lazygui/app.py:89`) `def _sync_credentials_to_settings(self, credentials)` - Persist auto-discovered credentials into settings.
- `show_connect_dialog` (method, `lazygui/app.py:100`) `def show_connect_dialog(self)` - Open the connection dialog and swap backends if accepted.
- `_build_initial_backend` (method, `lazygui/app.py:119`) `def _build_initial_backend(self)` - Instantiate the backend remembered in settings or auto-discovered.
- `_resolve_teamserver_credentials` (method, `lazygui/app.py:150`) `def _resolve_teamserver_credentials(self)` - Return ``(username, password)`` from the best available source.
- `_build_backend_from_request` (method, `lazygui/app.py:167`) `def _build_backend_from_request(self, request)` - Instantiate a backend based on the dialog return value.
- `_swap_backend` (method, `lazygui/app.py:175`) `def _swap_backend(self, new_backend)` - Tear down the previous backend and rebuild the panels around the new one.
- `_start_backend` (method, `lazygui/app.py:194`) `def _start_backend(self, backend)` - Connect signal handlers and call ``start()`` on the backend.
- `_configure_qt_attributes` (method, `lazygui/app.py:213`) `def _configure_qt_attributes(self)` - Set high-DPI policy before instantiating QApplication.
- `_configure_qt_application_metadata` (method, `lazygui/app.py:218`) `def _configure_qt_application_metadata(self)` - Populate organization/application metadata used by ``QSettings``.
- `_configure_logging` (method, `lazygui/app.py:224`) `def _configure_logging(self)` - Install a basic log configuration directing INFO+ to stderr.
- `C2Credentials` (class, `lazygui/config/c2_credentials.py:24`) `class C2Credentials` - Parsed credentials from the auto-generated file.
- `empty` (method, `lazygui/config/c2_credentials.py:33`) `def empty(cls)` - Return a sentinel representing no credentials available.
- `load_c2_credentials_from_file` (method, `lazygui/config/c2_credentials.py:38`) `def load_c2_credentials_from_file(file_path)` - Parse ``.c2_credentials.txt`` and return username + password.
- `load_c2_credentials` (method, `lazygui/config/c2_credentials.py:71`) `def load_c2_credentials(project_root)` - Resolve and parse the credentials file relative to ``project_root``.
- `WindowConstants` (class, `lazygui/config/constants.py:18`) `class WindowConstants` - Geometry defaults for top-level windows.
- `TimingConstants` (class, `lazygui/config/constants.py:34`) `class TimingConstants` - Timer intervals expressed in milliseconds.
- `NetworkConstants` (class, `lazygui/config/constants.py:48`) `class NetworkConstants` - Defaults for HTTP and WebSocket clients.
- `PtyConstants` (class, `lazygui/config/constants.py:86`) `class PtyConstants` - Tunables for the local PTY backend.
- `FontConstants` (class, `lazygui/config/constants.py:99`) `class FontConstants` - Font family fallbacks (theme tokens decide colours and sizes).
- `KeybindingConstants` (class, `lazygui/config/constants.py:124`) `class KeybindingConstants` - Application-wide keyboard shortcuts in Qt sequence notation.
- `IdentifierConstants` (class, `lazygui/config/constants.py:142`) `class IdentifierConstants` - Stable string identifiers for object names and settings keys.
- `ThemeConstants` (class, `lazygui/config/constants.py:161`) `class ThemeConstants` - Constants relevant to theme registration.
- `BackendConstants` (class, `lazygui/config/constants.py:176`) `class BackendConstants` - Identifiers for the available backend implementations.
- `PanelConstants` (class, `lazygui/config/constants.py:185`) `class PanelConstants` - Identifiers and labels for dockable panels.
- `EventLogConstants` (class, `lazygui/config/constants.py:205`) `class EventLogConstants` - Bounds for the event-log ring buffer.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 161
- Cross-boundary resolved imports (EXTRACTED): 18

## Connections

- [EXTRACTED] depends_on community 10 <-> 4 (strength 0.9): Extracted import edge crosses communities: lazygui/app.py imports core/logging.py.
- [EXTRACTED] depends_on community 10 <-> 1 (strength 0.9): Extracted import edge crosses communities: lazygui/panels/killchain_panel.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 10 <-> 11 (strength 0.9): Extracted import edge crosses communities: lazygui/windows/main_window.py imports lazygui/theme/tokens.py.

## Risks

- [layer strict] `tests/test_lazygui_backend.py` (testing) -> `lazygui/config/constants.py` (presentation)
- [layer strict] `tests/test_lazygui_backend.py` (testing) -> `lazygui/services/backend.py` (presentation)
- [layer strict] `tests/test_lazygui_backend.py` (testing) -> `lazygui/services/teamserver_backend.py` (presentation)
- [layer strict] `tests/test_lazygui_backend.py` (testing) -> `lazygui/config/constants.py` (presentation)
- [layer strict] `tests/test_lazygui_graph_widget.py` (testing) -> `lazygui/config/constants.py` (presentation)
- [layer strict] `tests/test_lazygui_graph_widget.py` (testing) -> `lazygui/widgets/graph_view.py` (presentation)

## Open Questions

- What would break if the most connected file in lazygui/panels changed?
- Should lazygui/panels be split, given cohesion 0.91?

## Sources

- `lazygui/__main__.py`
- `lazygui/app.py`
- `lazygui/config/__init__.py`
- `lazygui/config/c2_credentials.py`
- `lazygui/config/constants.py`
- `lazygui/config/paths.py`
- `lazygui/config/settings.py`
- `lazygui/panels/__init__.py`
- `lazygui/panels/base.py`
- `lazygui/panels/campaign_panel.py`
- `lazygui/panels/credentials_panel.py`
- `lazygui/panels/cve_panel.py`
- `lazygui/panels/event_log_panel.py`
- `lazygui/panels/graph_panel.py`
- `lazygui/panels/history_panel.py`
- `lazygui/panels/killchain_panel.py`
- `lazygui/panels/listeners_panel.py`
- `lazygui/panels/marketplace_panel.py`
- `lazygui/panels/registry.py`
- `lazygui/panels/sessions_panel.py`
- *... and 23 more*
