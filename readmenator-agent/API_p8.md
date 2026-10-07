# API (page 8 of 20)
Previous: [API_p7.md](API_p7.md)

## lazygui/config/settings.py
Depends on: `core/logging.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`
Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/theme/manager.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`
- `AppSettings.load` (method) `lazygui/config/settings.py:35` `def load(cls, constants, paths)` -- Load settings from disk, returning empty defaults if absent.
- `AppSettings.save` (method) `lazygui/config/settings.py:47` `def save(self)` -- Persist the current document to disk atomically.
- `AppSettings.get` (method) `lazygui/config/settings.py:55` `def get(self, key, default)` -- Generic accessor for a slash-separated settings key.
- `AppSettings.set` (method) `lazygui/config/settings.py:59` `def set(self, key, value)` -- Assign ``value`` to ``key`` without persisting; call :meth:`save`.
- `AppSettings.theme_id` (method) `lazygui/config/settings.py:64` `def theme_id(self)` -- Currently selected theme identifier.
- `AppSettings.theme_id` (method) `lazygui/config/settings.py:69` `def theme_id(self, value)`
- `AppSettings.last_backend_id` (method) `lazygui/config/settings.py:73` `def last_backend_id(self)` -- Backend identifier last used in the connect dialog.
- `AppSettings.last_backend_id` (method) `lazygui/config/settings.py:78` `def last_backend_id(self, value)`
- `AppSettings.last_teamserver_url` (method) `lazygui/config/settings.py:84` `def last_teamserver_url(self)` -- Last URL typed in the teamserver connection form.
- `AppSettings.last_teamserver_url` (method) `lazygui/config/settings.py:94` `def last_teamserver_url(self, value)`
- `AppSettings.last_operator_name` (method) `lazygui/config/settings.py:98` `def last_operator_name(self)` -- Operator handle the user typed last.
- `AppSettings.last_operator_name` (method) `lazygui/config/settings.py:103` `def last_operator_name(self, value)`
- `AppSettings.last_teamserver_password` (method) `lazygui/config/settings.py:107` `def last_teamserver_password(self)` -- Last teamserver password (stored in settings, derived from credentials file).
- `AppSettings.last_teamserver_password` (method) `lazygui/config/settings.py:112` `def last_teamserver_password(self, value)`
- `AppSettings.c2_credentials_loaded` (method) `lazygui/config/settings.py:116` `def c2_credentials_loaded(self)` -- Whether the last credentials were loaded from the C2 auto-generated file.
- `AppSettings.c2_credentials_loaded` (method) `lazygui/config/settings.py:121` `def c2_credentials_loaded(self, value)`
- `AppSettings.snapshot` (method) `lazygui/config/settings.py:124` `def snapshot(self)` -- Return a defensive read-only copy of the underlying document.

## lazygui/panels/base.py
Depends on: `lazygui/config/constants.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`
- `PanelBase.__init__` (method) `lazygui/panels/base.py:20` `def __init__(self, constants, backend, identifier, title, parent)` -- Initialise the dock widget with stable identifier and title.
- `PanelBase.identifier` (method) `lazygui/panels/base.py:43` `def identifier(self)` -- Stable identifier matching :class:`PanelConstants`.
- `PanelBase.backend` (method) `lazygui/panels/base.py:48` `def backend(self)` -- The currently connected backend instance.

## lazygui/panels/campaign_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `CampaignPanel.__init__` (method) `lazygui/panels/campaign_panel.py:31` `def __init__(self, constants, backend, parent)` -- Build the campaign list UI.
- `CampaignPanel.campaign_count` (method) `lazygui/panels/campaign_panel.py:133` `def campaign_count(self)` -- Return the number of active campaigns.

## lazygui/panels/credentials_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `CredentialsPanel.__init__` (method) `lazygui/panels/credentials_panel.py:30` `def __init__(self, constants, backend, parent)`

## lazygui/panels/cve_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `CVEPanel.__init__` (method) `lazygui/panels/cve_panel.py:31` `def __init__(self, constants, backend, parent)` -- Build the CVE list UI with severity filter.
- `CVEPanel.cve_count` (method) `lazygui/panels/cve_panel.py:173` `def cve_count(self)` -- Return the number of loaded CVEs.

## lazygui/panels/event_log_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/models.py`, `lazygui/widgets/event_log_view.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `EventLogPanel.__init__` (method) `lazygui/panels/event_log_panel.py:27` `def __init__(self, constants, backend, event_log, parent)` -- Compose the toolbar (level filter + clear) and the log view.

## lazygui/panels/graph_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/graph_view.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `GraphPanel.__init__` (method) `lazygui/panels/graph_panel.py:23` `def __init__(self, constants, backend, parent)` -- Build the graph view and connect to backend topology updates.
- `GraphPanel.graph_view` (method) `lazygui/panels/graph_panel.py:118` `def graph_view(self)` -- Return the underlying graph view for layout management.

## lazygui/panels/history_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `HistoryPanel.__init__` (method) `lazygui/panels/history_panel.py:33` `def __init__(self, constants, backend, parent)` -- Build the history viewer UI.

## lazygui/panels/killchain_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `modules/killchain.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `KillChainPanel.__init__` (method) `lazygui/panels/killchain_panel.py:37` `def __init__(self, constants, backend, parent)`

## lazygui/panels/listeners_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/filter_bar.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `ListenersPanel.__init__` (method) `lazygui/panels/listeners_panel.py:24` `def __init__(self, constants, backend, parent)` -- Build the layout and subscribe to backend listener updates.

## lazygui/panels/marketplace_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `MarketplacePanel.__init__` (method) `lazygui/panels/marketplace_panel.py:32` `def __init__(self, constants, backend, parent)` -- Build the tabbed marketplace UI.

## lazygui/panels/registry.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/windows/main_window.py`
- `PanelRegistry.build` (method) `lazygui/panels/registry.py:53` `def build(cls, constants, backend, event_log, parent)` -- Construct every dock panel and return them as a registry.
- `PanelRegistry.all_panels` (method) `lazygui/panels/registry.py:83` `def all_panels(self)` -- Return panels in canonical layout order.
- `PanelRegistry.by_identifier` (method) `lazygui/panels/registry.py:91` `def by_identifier(self, identifier)` -- Look up a panel by its stable identifier.

## lazygui/panels/sessions_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/filter_bar.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `SessionsPanel.__init__` (method) `lazygui/panels/sessions_panel.py:45` `def __init__(self, constants, backend, parent)` -- Build the layout and subscribe to backend session updates.

## lazygui/panels/terminal_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/widgets/terminal_view.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `TerminalPanel.__init__` (method) `lazygui/panels/terminal_panel.py:25` `def __init__(self, constants, backend, parent)` -- Compose the terminal view, session selector and command bar.
- `TerminalPanel.focus_terminal` (method) `lazygui/panels/terminal_panel.py:78` `def focus_terminal(self)` -- Move keyboard focus into the terminal text area.
- `TerminalPanel.set_target_session` (method) `lazygui/panels/terminal_panel.py:82` `def set_target_session(self, session_id)` -- Select a specific beacon in the dropdown.

## lazygui/services/backend.py
Depends on: `cli/commands/enum.py`, `lazygui/services/models.py`
Imported by: `lazygui/app.py`, `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`, `lazygui/services/__init__.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/widgets/beacon_command_modal.py`, `lazygui/widgets/status_badge.py`, `lazygui/windows/main_window.py`, `tests/test_lazygui_backend.py`
- `Backend.__init__` (method) `lazygui/services/backend.py:81` `def __init__(self, descriptor, parent)` -- Store the descriptor that uniquely identifies this backend.
- `Backend.descriptor` (method) `lazygui/services/backend.py:88` `def descriptor(self)` -- Read-only identification for connection dialogs.
- `Backend.status` (method) `lazygui/services/backend.py:93` `def status(self)` -- Current connection lifecycle state.
- `Backend.start` (method) `lazygui/services/backend.py:104` `def start(self)` -- Establish whatever underlying transport this backend uses.
- `Backend.stop` (method) `lazygui/services/backend.py:108` `def stop(self)` -- Tear the underlying transport down cleanly.
- `Backend.send_command` (method) `lazygui/services/backend.py:112` `def send_command(self, command, target_session)` -- Submit ``command``, optionally scoped to ``target_session``.
- `Backend.refresh` (method) `lazygui/services/backend.py:116` `def refresh(self)` -- Force a re-fetch of sessions, listeners and operator info.
- `Backend.resize_terminal` (method) `lazygui/services/backend.py:120` `def resize_terminal(self, columns, rows)` -- Inform the backend the terminal area was resized.
- `Backend.feed_terminal_input` (method) `lazygui/services/backend.py:124` `def feed_terminal_input(self, data)` -- Feed raw keystrokes typed by the operator into the terminal.
- `Backend.known_sessions` (method) `lazygui/services/backend.py:128` `def known_sessions(self)` -- Return the most recent snapshot of sessions, never ``None``.
- `Backend.known_listeners` (method) `lazygui/services/backend.py:132` `def known_listeners(self)` -- Return the most recent snapshot of listeners, never ``None``.
- `Backend.known_topology` (method) `lazygui/services/backend.py:136` `def known_topology(self)` -- Return the most recent graph topology.
- `Backend.known_campaigns` (method) `lazygui/services/backend.py:140` `def known_campaigns(self)` -- Return the most recent snapshot of campaigns.
- `Backend.request_world_model` (method) `lazygui/services/backend.py:144` `def request_world_model(self)` -- Request the current world model state as a dict.
- `Backend.request_beacon_history` (method) `lazygui/services/backend.py:157` `def request_beacon_history(self, client_id)` -- Return the persistent command/result history for a beacon.
- `Backend.request_session_state` (method) `lazygui/services/backend.py:171` `def request_session_state(self)` -- Request the current session state (creds, hashes, loot) as a dict.

## lazygui/services/event_log.py
Depends on: `lazygui/config/constants.py`, `lazygui/services/models.py`
Imported by: `lazygui/app.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/registry.py`, `lazygui/services/__init__.py`, `lazygui/widgets/event_log_view.py`, `lazygui/windows/main_window.py`
- `EventLog.__init__` (method) `lazygui/services/event_log.py:26` `def __init__(self, constants, parent)` -- Initialise the buffer using ``constants.event_log.max_records``.
- `EventLog.capacity` (method) `lazygui/services/event_log.py:33` `def capacity(self)` -- Maximum number of records retained before the oldest is dropped.
- `EventLog.append` (method) `lazygui/services/event_log.py:37` `def append(self, record)` -- Append ``record`` and emit ``record_appended``.
- `EventLog.extend` (method) `lazygui/services/event_log.py:42` `def extend(self, records)` -- Append every entry in ``records`` in iteration order.
- `EventLog.clear` (method) `lazygui/services/event_log.py:47` `def clear(self)` -- Drop all stored records and emit ``cleared``.
- `EventLog.snapshot` (method) `lazygui/services/event_log.py:52` `def snapshot(self, minimum_level)` -- Return a defensive tuple, optionally filtered by ``minimum_level``.

## lazygui/services/factory.py
Depends on: `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/services/backend.py`, `lazygui/services/local_backend.py`, `lazygui/services/models.py`, `lazygui/services/teamserver_backend.py`
Imported by: `lazygui/app.py`, `lazygui/services/__init__.py`, `static/js/html2pdf.bundle.min.js`
- `BackendFactory.create_local` (method) `lazygui/services/factory.py:30` `def create_local(self, parent)` -- Construct a local PTY-based backend.
- `BackendFactory.create_teamserver` (method) `lazygui/services/factory.py:34` `def create_teamserver(self, credentials, parent)` -- Construct a teamserver-based backend with the given credentials.
- `BackendFactory.create` (method) `lazygui/services/factory.py:42` `def create(self, kind, parent, credentials)` -- Convenience dispatch by :class:`BackendKind`.

## lazygui/services/local_backend.py
Depends on: `core/logging.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`
Imported by: `lazygui/services/__init__.py`, `lazygui/services/factory.py`
- `LocalPtyBackend.__init__` (method) `lazygui/services/local_backend.py:38` `def __init__(self, constants, paths, parent)` -- Initialise the backend with the shared constants and paths.
- `LocalPtyBackend.start` (method) `lazygui/services/local_backend.py:62` `def start(self)` -- Fork-exec the cmd2 console behind a PTY.
- `LocalPtyBackend.stop` (method) `lazygui/services/local_backend.py:87` `def stop(self)` -- Send ``SIGTERM`` to the child and tear down notifiers.
- `LocalPtyBackend.send_command` (method) `lazygui/services/local_backend.py:112` `def send_command(self, command, target_session)` -- Write ``command`` followed by a newline to the PTY.
- `LocalPtyBackend.refresh` (method) `lazygui/services/local_backend.py:117` `def refresh(self)` -- No-op for the local backend; the operator drives data from cmd2.
- `LocalPtyBackend.resize_terminal` (method) `lazygui/services/local_backend.py:121` `def resize_terminal(self, columns, rows)` -- Propagate the new size to the PTY using ``TIOCSWINSZ``.
- `LocalPtyBackend.feed_terminal_input` (method) `lazygui/services/local_backend.py:127` `def feed_terminal_input(self, data)` -- Encode ``data`` and write it to the master end of the PTY.
- `LocalPtyBackend.known_sessions` (method) `lazygui/services/local_backend.py:137` `def known_sessions(self)` -- Local backend does not enumerate sessions.
- `LocalPtyBackend.known_listeners` (method) `lazygui/services/local_backend.py:141` `def known_listeners(self)` -- Local backend does not enumerate listeners.
- `LocalPtyBackend.announce_local_operator` (method) `lazygui/services/local_backend.py:249` `def announce_local_operator(self)` -- Emit a synthetic :class:`Operator` describing the local user.

## lazygui/services/models.py
Depends on: `cli/commands/enum.py`
Imported by: `lazygui/app.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/sessions_panel.py`, `lazygui/services/__init__.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/widgets/beacon_command_modal.py`, `lazygui/widgets/event_log_view.py`, `lazygui/widgets/graph_view.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`, `tests/test_lazygui_backend.py`, `tests/test_lazygui_graph_widget.py`, `tests/test_lazygui_models.py`
- `EventLevel.numeric` (method) `lazygui/services/models.py:34` `def numeric(self)` -- Numeric rank used to compare severity.
- `EventRecord.now` (method) `lazygui/services/models.py:96` `def now(cls, level, source, message)` -- Construct a record stamped with the current UTC time.
- `Topology.empty` (method) `lazygui/services/models.py:133` `def empty(cls)` -- Return an empty topology.

## lazygui/services/teamserver_backend.py
Depends on: `core/logging.py`, `lazyc2/blueprints/auth.py`, `lazygui/config/constants.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`
Imported by: `lazygui/app.py`, `lazygui/services/__init__.py`, `lazygui/services/factory.py`, `lazygui/windows/connect_dialog.py`, `tests/test_lazygui_backend.py`
- `TeamserverBackend.__init__` (method) `lazygui/services/teamserver_backend.py:51` `def __init__(self, constants, credentials, parent)` -- Store ``credentials`` and prepare polling timers and Socket.IO client.
- `TeamserverBackend.start` (method) `lazygui/services/teamserver_backend.py:80` `def start(self)` -- Begin polling and establish Socket.IO connection.
- `TeamserverBackend.stop` (method) `lazygui/services/teamserver_backend.py:97` `def stop(self)` -- Tear down all timers and Socket.IO connection.
- `TeamserverBackend.send_command` (method) `lazygui/services/teamserver_backend.py:112` `def send_command(self, command, target_session)` -- Submit ``command`` via Socket.IO PTY (global) or ``/issue_command`` (beacon).
- `TeamserverBackend.refresh` (method) `lazygui/services/teamserver_backend.py:124` `def refresh(self)` -- Pull consolidated state JSON and emit derived signals.
- `TeamserverBackend.resize_terminal` (method) `lazygui/services/teamserver_backend.py:139` `def resize_terminal(self, columns, rows)` -- Forward resize to Socket.IO PTY namespace when connected.
- `TeamserverBackend.feed_terminal_input` (method) `lazygui/services/teamserver_backend.py:151` `def feed_terminal_input(self, data)` -- Feed keystrokes to the PTY via Socket.IO, falling back to HTTP commands.
- `TeamserverBackend.known_sessions` (method) `lazygui/services/teamserver_backend.py:169` `def known_sessions(self)` -- Most recent snapshot delivered by the last poll.
- `TeamserverBackend.known_listeners` (method) `lazygui/services/teamserver_backend.py:173` `def known_listeners(self)` -- Most recent snapshot delivered by the last poll.
- `TeamserverBackend.known_topology` (method) `lazygui/services/teamserver_backend.py:177` `def known_topology(self)` -- Most recent graph topology snapshot.
- `TeamserverBackend.known_campaigns` (method) `lazygui/services/teamserver_backend.py:181` `def known_campaigns(self)` -- Most recent campaign snapshot.
- `TeamserverBackend.request_beacon_results` (method) `lazygui/services/teamserver_backend.py:185` `def request_beacon_results(self, client_id)` -- Fetch stored command results for a specific beacon.
- `TeamserverBackend.request_world_model` (method) `lazygui/services/teamserver_backend.py:210` `def request_world_model(self)` -- Fetch the unified kill-chain snapshot from the teamserver REST API.
- `TeamserverBackend.request_beacon_history` (method) `lazygui/services/teamserver_backend.py:224` `def request_beacon_history(self, client_id)` -- Fetch the persistent ordered command/result history for a beacon.

## lazygui/theme/manager.py
Depends on: `core/logging.py`, `lazygui/config/constants.py`, `lazygui/config/settings.py`, `lazygui/theme/palettes/__init__.py`, `lazygui/theme/qss_builder.py`, `lazygui/theme/tokens.py`
Imported by: `lazygui/app.py`, `lazygui/theme/__init__.py`, `lazygui/windows/main_window.py`
- `ThemeManager.__init__` (method) `lazygui/theme/manager.py:31` `def __init__(self, constants, settings, application, palettes, parent)` -- Initialise the manager.
- `ThemeManager.active_tokens` (method) `lazygui/theme/manager.py:57` `def active_tokens(self)` -- Currently active :class:`ThemeTokens`.
- `ThemeManager.active_id` (method) `lazygui/theme/manager.py:64` `def active_id(self)` -- Identifier of the active palette.
- `ThemeManager.available` (method) `lazygui/theme/manager.py:68` `def available(self)` -- Yield all registered palettes in registration order.
- `ThemeManager.apply_initial` (method) `lazygui/theme/manager.py:72` `def apply_initial(self)` -- Load the saved theme identifier and apply it.
- `ThemeManager.apply` (method) `lazygui/theme/manager.py:80` `def apply(self, identifier)` -- Activate the palette with ``identifier`` and persist the choice.
- `ThemeManager.cycle` (method) `lazygui/theme/manager.py:93` `def cycle(self)` -- Switch to the next palette, wrapping at the end of the registry.

## lazygui/theme/palettes/__init__.py
Depends on: `lazygui/theme/tokens.py`
Imported by: `lazygui/theme/manager.py`
- `builtin_palettes` (function) `lazygui/theme/palettes/__init__.py:23` `def builtin_palettes()` -- Return the built-in palette registry as ``id -> tokens``.

## lazygui/theme/qss_builder.py
Depends on: `lazygui/config/constants.py`, `lazygui/theme/tokens.py`
Imported by: `lazygui/theme/__init__.py`, `lazygui/theme/manager.py`
- `QssBuilder.build` (method) `lazygui/theme/qss_builder.py:21` `def build(self, tokens)` -- Return the full QSS sheet for ``tokens``.

## lazygui/widgets/beacon_command_modal.py
Depends on: `lazygui/services/backend.py`, `lazygui/services/models.py`
Imported by: `lazygui/windows/main_window.py`
- `BeaconCommandModal.__init__` (method) `lazygui/widgets/beacon_command_modal.py:53` `def __init__(self, backend, parent)` -- Initialise the modal with a backend reference.
- `BeaconCommandModal.open` (method) `lazygui/widgets/beacon_command_modal.py:218` `def open(self)` -- Populate sessions before showing.
- `BeaconCommandModal.focus_input` (method) `lazygui/widgets/beacon_command_modal.py:229` `def focus_input(self)` -- Move keyboard focus to the command input.

## lazygui/widgets/command_palette_list.py
Depends on: `lazygui/config/constants.py`
Imported by: `lazygui/widgets/__init__.py`, `lazygui/windows/command_palette_window.py`, `lazygui/windows/main_window.py`
- `CommandPaletteList.__init__` (method) `lazygui/widgets/command_palette_list.py:33` `def __init__(self, constants, actions, parent)` -- Store the action set and prepare the underlying model.
- `CommandPaletteList.set_actions` (method) `lazygui/widgets/command_palette_list.py:53` `def set_actions(self, actions)` -- Replace the entire action registry and reset the filter.
- `CommandPaletteList.apply_filter` (method) `lazygui/widgets/command_palette_list.py:58` `def apply_filter(self, query)` -- Filter the action set using a substring + token-order heuristic.
- `CommandPaletteList.invoke_current` (method) `lazygui/widgets/command_palette_list.py:76` `def invoke_current(self)` -- Invoke whichever action is currently highlighted, if any.

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
- `GraphNodeItem.__init__` (method) `lazygui/widgets/graph_view.py:142` `def __init__(self, node, radius, color, pixmap, on_selected, on_context_menu, label_visible, parent)`
- `GraphNodeItem.node_data` (method) `lazygui/widgets/graph_view.py:185` `def node_data(self)` -- Return the immutable node data associated with this item.
- `GraphNodeItem.paint` (method) `lazygui/widgets/graph_view.py:189` `def paint(self, painter, option, widget)`
- `GraphNodeItem.mousePressEvent` (method) `lazygui/widgets/graph_view.py:247` `def mousePressEvent(self, event)`
- `GraphNodeItem.mouseReleaseEvent` (method) `lazygui/widgets/graph_view.py:258` `def mouseReleaseEvent(self, event)`
- `GraphNodeItem.hoverEnterEvent` (method) `lazygui/widgets/graph_view.py:265` `def hoverEnterEvent(self, event)`
- `GraphNodeItem.hoverLeaveEvent` (method) `lazygui/widgets/graph_view.py:272` `def hoverLeaveEvent(self, event)`
- `GraphNodeItem.itemChange` (method) `lazygui/widgets/graph_view.py:278` `def itemChange(self, change, value)`
- `GraphEdgeItem.__init__` (method) `lazygui/widgets/graph_view.py:287` `def __init__(self, edge, source_item, target_item, parent)`
- `GraphEdgeItem.update_position` (method) `lazygui/widgets/graph_view.py:323` `def update_position(self)` -- Recalculate the line endpoints from source and target positions.
- `GraphEdgeItem.edge_data` (method) `lazygui/widgets/graph_view.py:328` `def edge_data(self)` -- Return the immutable edge data.
- `GraphScene.__init__` (method) `lazygui/widgets/graph_view.py:339` `def __init__(self, constants, parent)`
- `GraphScene.set_topology` (method) `lazygui/widgets/graph_view.py:348` `def set_topology(self, topology)` -- Replace the current graph with a new topology using force layout.
- `GraphScene.step_physics` (method) `lazygui/widgets/graph_view.py:415` `def step_physics(self)` -- Run one iteration of force-directed layout.
- `GraphScene.selected_node_id` (method) `lazygui/widgets/graph_view.py:487` `def selected_node_id(self)` -- Return the identifier of the first selected node, or None.
- `GraphView.__init__` (method) `lazygui/widgets/graph_view.py:505` `def __init__(self, constants, parent)`
- `GraphView.set_theme_colors` (method) `lazygui/widgets/graph_view.py:523` `def set_theme_colors(self, bg_color, edge_color)` -- Update graph background and default edge colour from theme tokens.
- `GraphView.set_topology` (method) `lazygui/widgets/graph_view.py:531` `def set_topology(self, topology)` -- Render a new graph topology.
- `GraphView.wheelEvent` (method) `lazygui/widgets/graph_view.py:547` `def wheelEvent(self, event)`
- `GraphView.selected_node_id` (method) `lazygui/widgets/graph_view.py:557` `def selected_node_id(self)` -- Return the identifier of the currently selected node.
- `GraphView.fit_to_content` (method) `lazygui/widgets/graph_view.py:561` `def fit_to_content(self)` -- Zoom to fit all graph content.
- `GraphView.scene_handle` (method) `lazygui/widgets/graph_view.py:566` `def scene_handle(self)` -- Return the underlying graph scene.

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
- `CommandPaletteWindow.showEvent` (method) `lazygui/windows/command_palette_window.py:69` `def showEvent(self, event)` -- Move keyboard focus into the search box on every open.

## lazygui/windows/connect_dialog.py
Depends on: `lazygui/config/c2_credentials.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/services/models.py`, `lazygui/services/teamserver_backend.py`
Imported by: `lazygui/app.py`, `lazygui/windows/__init__.py`
- `ConnectDialog.__init__` (method) `lazygui/windows/connect_dialog.py:53` `def __init__(self, constants, settings, paths, parent)` -- Build the form and pre-fill from persisted settings + credentials file.
- `ConnectDialog.request` (method) `lazygui/windows/connect_dialog.py:106` `def request(self)` -- Translate current widget state into a :class:`ConnectionRequest`.
- `ConnectDialog.persist_choice` (method) `lazygui/windows/connect_dialog.py:121` `def persist_choice(self)` -- Save the picked values back into :class:`AppSettings`.

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
Depends on: `cli/aliases.py`, `cli/auto_crypto.py`, `cli/autosuggest.py`, `cli/chain_mode.py`, `cli/cli_enhancements.py`, `cli/command_chain.py`, `cli/engagement_hooks.py`, `cli/exploration.py`, `cli/fuzzy_picker.py`, `cli/graph_advisor.py`, `cli/headless.py`, `cli/lazynmap_post.py`, `cli/ops_commands.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/protips.py`, `cli/reactive_hints.py`, `cli/registry.py`, `cli/scope_guard.py`, `cli/splash.py`, `cli/status_bar.py`, `cli/tips_engine.py`, `cli/toast_bus.py`, `core/config.py`, `core/console.py`, `core/credential_vault.py`, `core/hardening.py`, `core/logging.py`, `core/safe_exec.py`, `modules/cli_auth.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/llm_factory.py`, `modules/logging_config.py`, `modules/metrics.py`, `modules/payload_factory.py`, `modules/session_cleanup.py`, `modules/state_manager.py`, `modules/unified_bridge.py`, `skills/unified_orchestrator.py`, `utils.py`
Imported by: `core/command_bridge.py`, `discord_c2.py`, `lazyc2.py`, `poc_tui/app.py`, `scripts/devtools/command_audit.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_scope_guard_integration.py`
- `_PayloadSettableProxy.__init__` (method) `lazyown.py:238` `def __init__(self, params)` -- Bind the proxy to a live ``params`` dictionary.
- `LazyOwnShell.__init__` (method) `lazyown.py:328` `def __init__(self)` -- Initializer for the LazyOwnShell class.
- `LazyOwnShell.log_command` (method) `lazyown.py:714` `def log_command(self, cmd_name, cmd_args, start_time, end_time, duration_ms)` -- Logs the command execution details to a CSV file.
- `LazyOwnShell.default` (method) `lazyown.py:777` `def default(self, line)` -- Handles undefined commands, including aliases.
- `LazyOwnShell.scripts` (method) `lazyown.py:808` `def scripts(self)` -- Auto-discovered list of runnable script names.
- `LazyOwnShell.refresh_prompt` (method) `lazyown.py:828` `def refresh_prompt(self)` -- Recompute the Neon Box prompt from the live payload.
- `LazyOwnShell.do_set` (method) `lazyown.py:839` `def do_set(self, line)` -- Set a parameter — the unified ``set``/``assign`` surface.
- `LazyOwnShell.logcsv` (method) `lazyown.py:1189` `def logcsv(self, line, start_time, end_time, duration_ms)` -- Forward a command line to :meth:`log_command` for CSV persistence.
- `LazyOwnShell.cmd` (method) `lazyown.py:1224` `def cmd(self, line)` -- Internal function to execute commands.
- `LazyOwnShell.onecmd_plus_hooks` (method) `lazyown.py:1321` `def onecmd_plus_hooks(self, statement, add_to_history, raise_keyboard_interrupt, orig_rl_history_length)` -- Dispatch a command, expanding payload placeholders in custom aliases.
- `LazyOwnShell.one_cmd` (method) `lazyown.py:1517` `def one_cmd(self, command)` -- Internal function to execute commands.
- `LazyOwnShell.emptyline` (method) `lazyown.py:1563` `def emptyline(self)` -- Handle the case where the user enters an empty line.
- `LazyOwnShell.load_user_commands` (method) `lazyown.py:1588` `def load_user_commands(self)` -- Carga los comandos personalizados desde user_commands.json
- `LazyOwnShell.save_user_command` (method) `lazyown.py:1600` `def save_user_command(self, alias, command)` -- Guarda un nuevo comando en user_commands.json
- `LazyOwnShell.list_files_in_directory` (method) `lazyown.py:1612` `def list_files_in_directory(self, directory)` -- Lista todos los archivos en un directorio dado.
- `LazyOwnShell.register_tool_commands` (method) `lazyown.py:1618` `def register_tool_commands(self)` -- Register every active ``tools/*.tool`` as a ``do_<toolname>`` command.
- `LazyOwnShell.make_wrapper` (method) `lazyown.py:1677` `def make_wrapper(cmd_template, tname, default_target)`
- `LazyOwnShell.tool_wrapper` (method) `lazyown.py:1678` `def tool_wrapper(arg)`
- `LazyOwnShell.wrapper` (method) `lazyown.py:1776` `def wrapper(arg)`
- `LazyOwnShell.load_plugins` (method) `lazyown.py:1798` `def load_plugins(self)` -- Load every Lua plugin from the 'plugins/' directory.
- `LazyOwnShell.load_yaml_plugins` (method) `lazyown.py:1828` `def load_yaml_plugins(self)` -- Loads all YAML plugins from the 'lazyaddons/' directory.
- `LazyOwnShell.register_yaml_plugin` (method) `lazyown.py:1851` `def register_yaml_plugin(self, plugin_data)` -- Register a YAML addon as a shell command.
- `LazyOwnShell.wrapper_yaml` (method) `lazyown.py:1891` `def wrapper_yaml(arg)`
- `LazyOwnShell.register_all_adversary_commands` (method) `lazyown.py:1986` `def register_all_adversary_commands(self)`
- `LazyOwnShell.cmd_wrapper` (method) `lazyown.py:2008` `def cmd_wrapper(_)`
- `LazyOwnShell.display_toastr` (method) `lazyown.py:2015` `def display_toastr(self, message, type)` -- Display a toastr-like notification in the terminal with adaptive sizing.
- `LazyOwnShell.show_toastr` (method) `lazyown.py:2069` `def show_toastr()`
- `LazyOwnShell.completedefault` (method) `lazyown.py:2092` `def completedefault(self, text, line, begidx, endidx)` -- Fall through to the payload-aware completer for unhandled commands.
- `LazyOwnShell.preloop` (method) `lazyown.py:2120` `def preloop(self)` -- Print a session-start pro tip and handle first-run setup.
- `LazyOwnShell.postparsing_precmd` (method) `lazyown.py:2258` `def postparsing_precmd(self, statement)` -- Gate unauthenticated commands — anonymous operators can only run ``register``, ``login``, ``logout``, ``whoami``...
- `LazyOwnShell.postloop` (method) `lazyown.py:2284` `def postloop(self)` -- Handle operations to perform after exiting the command loop.
- `LazyOwnShell.complete_phase` (method) `lazyown.py:2318` `def complete_phase(self, text, line, begidx, endidx)` -- Tab-complete phase names.
- `LazyOwnShell.complete_l00t` (method) `lazyown.py:2324` `def complete_l00t(self, text, line, begidx, endidx)` -- Tab-complete l00t subcommands.
- `LazyOwnShell.complete_loot` (method) `lazyown.py:2331` `def complete_loot(self, text, line, begidx, endidx)` -- Tab-complete loot subcommands (delegates to l00t).
- `LazyOwnShell.complete_assign` (method) `lazyown.py:2337` `def complete_assign(self, text, line, begidx, endidx)` -- Tab-complete the parameter name from the live payload keys.
- `LazyOwnShell.complete_scope` (method) `lazyown.py:2355` `def complete_scope(self, text, line, begidx, endidx)` -- Tab-complete the scope subcommands.
- `LazyOwnShell.complete_palette` (method) `lazyown.py:2407` `def complete_palette(self, text, line, begidx, endidx)` -- Tab-complete the palette command using the live command index.
- `LazyOwnShell.run_lazysearch` (method) `lazyown.py:2424` `def run_lazysearch(self)` -- Runs the internal module `modules/lazysearch.py`.
- `LazyOwnShell.run_lazysearch_gui` (method) `lazyown.py:2441` `def run_lazysearch_gui(self)` -- Run the internal module located at `modules/LazyOwnExplorer.py`.
- `LazyOwnShell.run_lazyown` (method) `lazyown.py:2471` `def run_lazyown(self)` -- Run the internal module located at `modules/lazyown_parquet_tool.py`.
- `LazyOwnShell.run_update_db` (method) `lazyown.py:2497` `def run_update_db(self)` -- Run the internal module located at `modules/update_db.sh`.
- `LazyOwnShell.run_lazynmap` (method) `lazyown.py:2527` `def run_lazynmap(self)` -- Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.
- `LazyOwnShell.run_lazywerkzeugdebug` (method) `lazyown.py:2595` `def run_lazywerkzeugdebug(self)` -- Run the internal module located at `modules/legacy/lazywerkzeug.py` in debug mode.
- `LazyOwnShell.run_lazygath` (method) `lazyown.py:2654` `def run_lazygath(self)` -- Run the internal module located at `modules/lazygat.sh`. to gathering the sistem :)
- `LazyOwnShell.run_lazynmapdiscovery` (method) `lazyown.py:2686` `def run_lazynmapdiscovery(self)` -- Runs the internal module `modules/lazynmap.sh` with discovery mode.
- `LazyOwnShell.run_lazysniff` (method) `lazyown.py:2701` `def run_lazysniff(self)` -- Run the sniffer internal module located at `modules/legacy/lazysniff.py` with the specified parameters.
- `LazyOwnShell.run_lazyftpsniff` (method) `lazyown.py:2751` `def run_lazyftpsniff(self)` -- Run the sniffer ftp internal module located at `modules/legacy/lazyftpsniff.py` with the specified parameters.
- `LazyOwnShell.run_lazynetbios` (method) `lazyown.py:2797` `def run_lazynetbios(self)` -- Run the internal module to search netbios vuln victims, located at `modules/legacy/lazynetbios.py` with the...
- `LazyOwnShell.run_lazyhoneypot` (method) `lazyown.py:2848` `def run_lazyhoneypot(self)` -- Run the internal module located at `modules/legacy/lazyhoneypot.py` with the specified parameters.
- `LazyOwnShell.run_lazysearch_bot` (method) `lazyown.py:2913` `def run_lazysearch_bot(self)` -- Run the internal module GROQ AI located at `modules/legacy/lazysearch_bot.py` with the specified parameters.
- `LazyOwnShell.run_lazymetaextract0r` (method) `lazyown.py:2964` `def run_lazymetaextract0r(self)` -- Run the Metadata extractor internal module located at `modules/lazyown_metaextract0r.py` with the specified parameters.
- `LazyOwnShell.run_lazyownratcli` (method) `lazyown.py:3005` `def run_lazyownratcli(self)` -- Run the internal module located at `modules/lazyownclient.py` with the specified parameters.
- `LazyOwnShell.run_lazyownrat` (method) `lazyown.py:3065` `def run_lazyownrat(self)` -- Run the internal module located at `modules/lazyownserver.py` with the specified parameters.
- `LazyOwnShell.run_lazybotnet` (method) `lazyown.py:3126` `def run_lazybotnet(self)` -- Run the internal module located at `modules/legacy/lazybotnet.py` with the specified parameters.
- `LazyOwnShell.run_lazylfi2rce` (method) `lazyown.py:3182` `def run_lazylfi2rce(self)` -- Run the internal module located at `modules/legacy/lazylfi2rce.py` with the specified parameters.
- `LazyOwnShell.run_lazylogpoisoning` (method) `lazyown.py:3270` `def run_lazylogpoisoning(self)` -- Run the internal module located at `modules/legacy/lazylogpoisoning.py` with the specified parameters.
- `LazyOwnShell.run_lazybotcli` (method) `lazyown.py:3317` `def run_lazybotcli(self)` -- Run the internal module located at `modules/legacy/lazybotcli.py` with the specified parameters.
- `LazyOwnShell.run_lazyssh77enum` (method) `lazyown.py:3373` `def run_lazyssh77enum(self)` -- Run the internal module located at `modules/lazybrutesshuserenum.py` with the specified parameters.
- `LazyOwnShell.run_lazyburpfuzzer` (method) `lazyown.py:3425` `def run_lazyburpfuzzer(self)` -- Run the internal module located at `modules/lazyown_burpfuzzer.py` with the specified parameters.
- `LazyOwnShell.run_lazyreverse_shell` (method) `lazyown.py:3551` `def run_lazyreverse_shell(self)` -- Run the internal module located at `modules/lazyreverse_shell.sh` with the specified parameters.
- `LazyOwnShell.run_lazyarpspoofing` (method) `lazyown.py:3603` `def run_lazyarpspoofing(self)` -- Run the internal module located at `modules/legacy/lazyarpspoofing.py` with the specified parameters.
- `LazyOwnShell.run_lazyattack` (method) `lazyown.py:3657` `def run_lazyattack(self)` -- Run the internal module located at `modules/lazyatack.sh` with the specified parameters.
- `LazyOwnShell.run_lazymsfvenom` (method) `lazyown.py:3714` `def run_lazymsfvenom(self)` -- Executes the `msfvenom` tool to generate a variety of payloads based on user input.
- `LazyOwnShell.run_lazyaslrcheck` (method) `lazyown.py:3885` `def run_lazyaslrcheck(self)` -- Creates a path hijacking attack by performing the following steps:
- `LazyOwnShell.run_lazypathhijacking` (method) `lazyown.py:3935` `def run_lazypathhijacking(self)` -- Creates a path hijacking attack by performing the following steps:
- `LazyOwnShell.run_script` (method) `lazyown.py:3970` `def run_script(self, script_name)` -- Run a script with the given arguments
- `LazyOwnShell.run_command` (method) `lazyown.py:4002` `def run_command(self, command)` -- Run a command and print output in real-time
- `LazyOwnShell.get_output` (method) `lazyown.py:4087` `def get_output(self)` -- Devuelve la salida acumulada
- `LazyOwnShell.upload_file_to_c2` (method) `lazyown.py:4092` `def upload_file_to_c2(self, file_path, clientid)` -- Sube un archivo al C2.
- `LazyOwnShell.complete_upload_c2` (method) `lazyown.py:4118` `def complete_upload_c2(self, text, line, begidx, endidx)` -- Autocomplete implant names from implant_config_*.json files in sessions/ directory
- `LazyOwnShell.download_file_from_c2` (method) `lazyown.py:4148` `def download_file_from_c2(self, file_name, clientid)` -- Descarga un archivo desde el C2.
- `LazyOwnShell.issue_command_to_c2` (method) `lazyown.py:4207` `def issue_command_to_c2(self, command, client_id)` -- Ejecuta un comando en el cliente usando el C2.
- `LazyOwnShell.complete_issue_command_to_c2` (method) `lazyown.py:4239` `def complete_issue_command_to_c2(self, text, line, begidx, endidx)` -- Autocomplete: 1st arg = implant name, 2nd arg = beacon command (with : if needed)
- `LazyOwnShell.view_code` (method) `lazyown.py:4307` `def view_code(self, stdscr)` -- Display C and ASM code side by side in a curses-based interface.
- `LazyOwnShell.get_available_actions` (method) `lazyown.py:4420` `def get_available_actions(self)` -- Returns a list of available actions using cmd2 introspection.
- `LazyOwnShell.process_scan_csv` (method) `lazyown.py:4503` `def process_scan_csv(self, csv_file, ip, port, all_data, processed_ips)` -- Processes a single scan CSV file.
- `LazyOwnShell.process_vuln_csv` (method) `lazyown.py:4526` `def process_vuln_csv(self, csv_file, ip, all_data, processed_ips)` -- Processes a single vulnerability CSV file.
- `LazyOwnShell.do_event_log` (method) `lazyown.py:4644` `def do_event_log(self, line)` -- Show recent EventBus events.
- `LazyOwnShell.do_state_snapshot` (method) `lazyown.py:4673` `def do_state_snapshot(self, line)` -- Show unified StateManager snapshot (DB + JSON caches).
- `LazyOwnShell.do_route` (method) `lazyown.py:4705` `def do_route(self, line)` -- Route a natural-language prompt to a LazyOwn tool.
- `LazyOwnShell.main` (method) `lazyown.py:4727` `def main()`

## modules/49803.py
- `auth` (function) `modules/49803.py:42` `def auth()`
- `injection` (function) `modules/49803.py:70` `def injection()`
- `connection` (function) `modules/49803.py:84` `def connection()`

## modules/CVE-2023-28432.py
- `poc` (function) `modules/CVE-2023-28432.py:10` `def poc(url)`

## modules/LazyOwnExplorer.py
- `AutocompleteEntry.__init__` (method) `modules/LazyOwnExplorer.py:30` `def __init__(self, get_suggestions_func)`
- `AutocompleteEntry.changed` (method) `modules/LazyOwnExplorer.py:44` `def changed(self, name, index, mode)`
- `AutocompleteEntry.selection` (method) `modules/LazyOwnExplorer.py:67` `def selection(self, event)`
- `AutocompleteEntry.move_up` (method) `modules/LazyOwnExplorer.py:74` `def move_up(self, event)`
- `AutocompleteEntry.move_down` (method) `modules/LazyOwnExplorer.py:86` `def move_down(self, event)`
- `AutocompleteEntry.comparison` (method) `modules/LazyOwnExplorer.py:98` `def comparison(self, pattern)`
- `LazyOwnGUI.__init__` (method) `modules/LazyOwnExplorer.py:102` `def __init__(self)`
- `LazyOwnGUI.create_widgets` (method) `modules/LazyOwnExplorer.py:116` `def create_widgets(self)`
- `LazyOwnGUI.get_suggestions` (method) `modules/LazyOwnExplorer.py:121` `def get_suggestions(term)`
- `LazyOwnGUI.load_parquet_files` (method) `modules/LazyOwnExplorer.py:176` `def load_parquet_files(self)`
- `LazyOwnGUI.get_unique_values` (method) `modules/LazyOwnExplorer.py:235` `def get_unique_values(self)`
- `LazyOwnGUI.search` (method) `modules/LazyOwnExplorer.py:242` `def search(self)`
- `LazyOwnGUI.search_in_parquet` (method) `modules/LazyOwnExplorer.py:259` `def search_in_parquet(self, term)`
- `LazyOwnGUI.on_row_double_click` (method) `modules/LazyOwnExplorer.py:268` `def on_row_double_click(self, event)`
- `LazyOwnGUI.show_row_details` (method) `modules/LazyOwnExplorer.py:273` `def show_row_details(self, row)`
- `LazyOwnGUI.add_new_attack_vector` (method) `modules/LazyOwnExplorer.py:295` `def add_new_attack_vector(self)`
- `LazyOwnGUI.save_new_vector` (method) `modules/LazyOwnExplorer.py:315` `def save_new_vector()`
- `LazyOwnGUI.scan_system_for_binaries` (method) `modules/LazyOwnExplorer.py:343` `def scan_system_for_binaries(self)`
- `LazyOwnGUI.is_binary` (method) `modules/LazyOwnExplorer.py:344` `def is_binary(file_path)`
- `LazyOwnGUI.show_scan_results` (method) `modules/LazyOwnExplorer.py:360` `def show_scan_results(self, binaries)`
- `LazyOwnGUI.export_to_csv` (method) `modules/LazyOwnExplorer.py:371` `def export_to_csv(self)`

## modules/adcs_attacks.py
Imported by: `cli/commands/exploit_migrated.py`
- `CertificateTemplate.esc_vulnerabilities` (method) `modules/adcs_attacks.py:35` `def esc_vulnerabilities(self)` -- Determine which ESC attack paths apply to this template.
- `ADCSCertipyWrapper.__init__` (method) `modules/adcs_attacks.py:80` `def __init__(self, certipy_path, timeout)`
- `ADCSCertipyWrapper.find_certificate_authorities` (method) `modules/adcs_attacks.py:115` `def find_certificate_authorities(self, username, password, domain, dc_ip, hashes)` -- Enumerate certificate authorities in an Active Directory domain.
- `ADCSCertipyWrapper.enumerate_templates` (method) `modules/adcs_attacks.py:187` `def enumerate_templates(self, username, password, domain, dc_ip, hashes)` -- Enumerate vulnerable certificate templates.
- `ADCSCertipyWrapper.request_certificate_esc1` (method) `modules/adcs_attacks.py:271` `def request_certificate_esc1(self, username, password, domain, dc_ip, ca_name, template_name, target_user, output_file)` -- ESC1: Request a certificate with a user-supplied subject alternative name.
- `ADCSCertipyWrapper.request_certificate_esc8` (method) `modules/adcs_attacks.py:320` `def request_certificate_esc8(self, username, password, domain, dc_ip, ca_server, template_name, output_file)` -- ESC8: HTTP-based certificate enrollment (NTLM relay to AD CS).
- `ADCSCertipyWrapper.authenticate_with_certificate` (method) `modules/adcs_attacks.py:361` `def authenticate_with_certificate(self, cert_file, domain, dc_ip, username)` -- Authenticate to the domain using a certificate and retrieve NT hash.
- `ADCSCertipyWrapper.assess_vulnerability` (method) `modules/adcs_attacks.py:400` `def assess_vulnerability(self, username, password, domain, dc_ip, hashes)` -- Run a full AD CS vulnerability assessment.

## modules/agent_runner.py
Depends on: `core/logging.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
Imported by: `modules/vuln_agent.py`, `modules/vulnbot.py`
- `configure_logging` (function) `modules/agent_runner.py:58` `def configure_logging(debug)`
- `AgentTool.__init__` (method) `modules/agent_runner.py:66` `def __init__(self, name, description, func, parameters, required)`
- `AgentTool.to_api_format` (method) `modules/agent_runner.py:77` `def to_api_format(self)`
- `AgentTool.execute` (method) `modules/agent_runner.py:87` `def execute(self)` -- Ejecuta con validación de argumentos y formato claro
- `ASTToolExtractor.extract_commands_from_file` (method) `modules/agent_runner.py:139` `def extract_commands_from_file(file_path, prefix)`
- `AgentRunner.__init__` (method) `modules/agent_runner.py:180` `def __init__(self, model, system_prompt, max_iterations)`
- `AgentRunner.register_tool` (method) `modules/agent_runner.py:208` `def register_tool(self, tool)`
- `AgentRunner.register_tool_from_instance` (method) `modules/agent_runner.py:211` `def register_tool_from_instance(self, func)` -- Wrap a plain function as an AgentTool using its signature and docstring.
- `AgentRunner.register_tools_from_metadata` (method) `modules/agent_runner.py:229` `def register_tools_from_metadata(self, commands, executor)`
- `AgentRunner.make_executor` (method) `modules/agent_runner.py:232` `def make_executor(cmd_name)`
- `AgentRunner.wrapper` (method) `modules/agent_runner.py:233` `def wrapper(command)`
- `AgentRunner.get_tools_for_api` (method) `modules/agent_runner.py:254` `def get_tools_for_api(self)`
- `AgentRunner.run` (method) `modules/agent_runner.py:259` `def run(self, user_input)`
- `LazyOwnShellWrapper.__init__` (method) `modules/agent_runner.py:360` `def __init__(self, script_path)`
- `LazyOwnShellWrapper.execute_command` (method) `modules/agent_runner.py:390` `def execute_command(self, command)` -- Ejecuta comando con timeout usando threading
- `LazyOwnShellWrapper.target` (method) `modules/agent_runner.py:397` `def target()`
- `LazyOwnShellWrapper.get_commands_summary` (method) `modules/agent_runner.py:427` `def get_commands_summary(self)`
- `VulnBotCLI.__init__` (method) `modules/agent_runner.py:436` `def __init__(self, provider, mode, debug, script_path)`
- `VulnBotCLI.process_request` (method) `modules/agent_runner.py:494` `def process_request(self, user_input)`
- `VulnBotCLI.interactive_mode` (method) `modules/agent_runner.py:499` `def interactive_mode(bot)`
- `VulnBotCLI.parse_args` (method) `modules/agent_runner.py:522` `def parse_args()`
- `VulnBotCLI.main` (method) `modules/agent_runner.py:531` `def main()`

## modules/agent_tool.py
Depends on: `core/logging.py`
Imported by: `modules/tool_extractor.py`, `modules/vuln_agent.py`
- `AgentTool.__init__` (method) `modules/agent_tool.py:10` `def __init__(self, name, description, func, parameters, required)`
- `AgentTool.to_api_format` (method) `modules/agent_tool.py:21` `def to_api_format(self)` -- Convierte al formato API de LLM (Groq/Ollama)
- `AgentTool.execute` (method) `modules/agent_tool.py:32` `def execute(self)` -- Ejecuta la herramienta con manejo de errores robusto

## modules/ai_exploit_chain.py
Depends on: `modules/autonomous_exploit_engine.py`
Imported by: `cli/commands/pwn.py`, `skills/lazyown_mcp.py`
- `AIExploitChainer.__init__` (method) `modules/ai_exploit_chain.py:190` `def __init__(self)`
- `AIExploitChainer.reason` (method) `modules/ai_exploit_chain.py:203` `def reason(self, context)` -- Analyze context failures and produce the next best exploit candidate.
- `AIExploitChainer.evaluate_failure` (method) `modules/ai_exploit_chain.py:223` `def evaluate_failure(result)` -- Classify the reason for an exploit failure by output pattern matching.
- `AIExploitChainer.select_next_strategy` (method) `modules/ai_exploit_chain.py:235` `def select_next_strategy(self, context)` -- Select the next strategy to attempt based on context and failures.
- `AIExploitChainer.estimate_confidence` (method) `modules/ai_exploit_chain.py:269` `def estimate_confidence(self, strategy, profile)` -- Estimate confidence (0.0-1.0) for a strategy against a target profile.
- `AIExploitChainer.build_chain_plan` (method) `modules/ai_exploit_chain.py:311` `def build_chain_plan(self, context)` -- Build a full multi-step exploitation plan following the kill chain.
- `AIExploitChainer.adapt_chain` (method) `modules/ai_exploit_chain.py:344` `def adapt_chain(self, context, new_info)` -- Adapt the chain plan based on newly discovered information.

## modules/ai_fallback.py
Depends on: `modules/llm_factory.py`, `modules/toposwarm_bridge.py`
Imported by: `modules/recommender.py`, `modules/timeline_narrator.py`
- `AIResult.call` (method) `modules/ai_fallback.py:238` `def call(prompt, system, api_key, max_tokens, temperature)` -- Call Groq → fallback to Ollama → fallback to TopoSwarm local brain → error.


Next: [API_p9.md](API_p9.md)
