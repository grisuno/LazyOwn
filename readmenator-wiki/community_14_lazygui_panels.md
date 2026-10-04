# lazygui/panels

*Community 14 | 36 files | cohesion 0.77*

## Definition

This community groups 36 file(s) rooted at `lazygui/panels` with dominant language py (cohesion 0.77). Central symbols: `AppConstants`, `Backend`, `BackendConstants`, `BackendDescriptor`, `BackendKind`, `BackendStatus`, `BeaconCommandModal`, `BeaconResult`. Core file: `tests/test_lazygui_backend.py` (59 symbols). Documented purpose: Immutable application constants.  Every numeric or string literal that the GUI relies on lives here. If a value ever needs tweaking it changes in this file only.

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

### `lazygui/services` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/services/backend.py` | py | presentation | 20 | yes |
| `lazygui/services/event_log.py` | py | presentation | 7 | yes |
| `lazygui/services/models.py` | py | business_logic | 15 | yes |

### `lazygui/theme` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/theme/__init__.py` | py | presentation | 0 | yes |
| `lazygui/theme/manager.py` | py | presentation | 10 | yes |
| `lazygui/theme/qss_builder.py` | py | presentation | 3 | yes |

### `lazygui/windows` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/windows/__init__.py` | py | presentation | 0 | yes |
| `lazygui/windows/command_palette_window.py` | py | presentation | 6 | yes |
| `lazygui/windows/main_window.py` | py | presentation | 28 | yes |

### `tests` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_lazygui_backend.py` | py | testing | 59 | yes |
| `tests/test_lazygui_graph_widget.py` | py | testing | 51 | yes |
| `tests/test_lazygui_models.py` | py | testing | 42 | yes |

### `lazygui/config` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/config/constants.py` | py | presentation | 14 | yes |

### `lazygui/theme/palettes` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/theme/palettes/__init__.py` | py | presentation | 1 | yes |

*... and 16 more files in this community.*


## Key Symbols

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
- `CommandPaletteConstants` (class, `lazygui/config/constants.py:214`) `class CommandPaletteConstants` - Tunables for the fuzzy command palette.
- `AppConstants` (class, `lazygui/config/constants.py:223`) `class AppConstants` - Aggregate view exposing every constant group as attributes.
- `panel_labels` (method, `lazygui/config/constants.py:239`) `def panel_labels(self)` - Map panel identifier to human-readable label.
- `PanelBase` (class, `lazygui/panels/base.py:17`) `class PanelBase(QDockWidget)` - Base class enforcing object-name discipline and backend wiring.
- `__init__` (method, `lazygui/panels/base.py:20`) `def __init__(self, constants, backend, identifier, title, parent)` - Initialise the dock widget with stable identifier and title.
- `identifier` (method, `lazygui/panels/base.py:43`) `def identifier(self)` - Stable identifier matching :class:`PanelConstants`.
- `backend` (method, `lazygui/panels/base.py:48`) `def backend(self)` - The currently connected backend instance.
- `CampaignPanel` (class, `lazygui/panels/campaign_panel.py:28`) `class CampaignPanel(PanelBase)` - Dock panel displaying active campaign status.
- `__init__` (method, `lazygui/panels/campaign_panel.py:31`) `def __init__(self, constants, backend, parent)` - Build the campaign list UI.
- `_refresh` (method, `lazygui/panels/campaign_panel.py:99`) `def _refresh(self)`
- `_on_campaigns_changed` (method, `lazygui/panels/campaign_panel.py:102`) `def _on_campaigns_changed(self, campaigns)`
- `_populate_tree` (method, `lazygui/panels/campaign_panel.py:106`) `def _populate_tree(self)`
- `_request_new_campaign` (method, `lazygui/panels/campaign_panel.py:120`) `def _request_new_campaign(self)`
- `_request_view_campaign` (method, `lazygui/panels/campaign_panel.py:123`) `def _request_view_campaign(self)`
- `_request_run_playbook` (method, `lazygui/panels/campaign_panel.py:126`) `def _request_run_playbook(self)`
- `campaign_count` (method, `lazygui/panels/campaign_panel.py:133`) `def campaign_count(self)` - Return the number of active campaigns.
- `CredentialsPanel` (class, `lazygui/panels/credentials_panel.py:27`) `class CredentialsPanel(PanelBase)` - Dock widget displaying captured credentials and loot.
- `__init__` (method, `lazygui/panels/credentials_panel.py:30`) `def __init__(self, constants, backend, parent)`
- `_build_ui` (method, `lazygui/panels/credentials_panel.py:50`) `def _build_ui(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 122
- Cross-boundary resolved imports (EXTRACTED): 36

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [layer strict] `tests/test_lazygui_backend.py` (testing) -> `lazygui/config/constants.py` (presentation)
- [layer strict] `tests/test_lazygui_backend.py` (testing) -> `lazygui/services/backend.py` (presentation)
- [layer strict] `tests/test_lazygui_backend.py` (testing) -> `lazygui/services/teamserver_backend.py` (presentation)
- [layer strict] `tests/test_lazygui_backend.py` (testing) -> `lazygui/config/constants.py` (presentation)
- [layer strict] `tests/test_lazygui_graph_widget.py` (testing) -> `lazygui/config/constants.py` (presentation)
- [layer strict] `tests/test_lazygui_graph_widget.py` (testing) -> `lazygui/widgets/graph_view.py` (presentation)

## Open Questions

- What would break if the most connected file in lazygui/panels changed?
- Should lazygui/panels be split, given cohesion 0.77?

## Sources

- `lazygui/config/constants.py`
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
- `lazygui/panels/terminal_panel.py`
- `lazygui/services/backend.py`
- `lazygui/services/event_log.py`
- `lazygui/services/models.py`
- `lazygui/theme/__init__.py`
- `lazygui/theme/manager.py`
- *... and 16 more*
