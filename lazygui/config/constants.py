"""Immutable application constants.

Every numeric or string literal that the GUI relies on lives here. If a value
ever needs tweaking it changes in this file only; nothing downstream should
ever embed a literal of its own.

The class is a frozen dataclass so attempts to mutate it at runtime fail
loudly. User-overridable values belong to :class:`AppSettings` instead.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True, slots=True)
class WindowConstants:
    """Geometry defaults for top-level windows."""

    main_default_width: int = 1600
    main_default_height: int = 980
    main_min_width: int = 1100
    main_min_height: int = 700
    connect_dialog_width: int = 520
    connect_dialog_height: int = 420
    command_palette_width: int = 720
    command_palette_height: int = 420
    dock_min_width: int = 240
    dock_min_height: int = 160


@dataclass(frozen=True, slots=True)
class TimingConstants:
    """Timer intervals expressed in milliseconds."""

    pty_poll_interval_ms: int = 30
    teamserver_poll_interval_ms: int = 2_000
    websocket_reconnect_delay_ms: int = 3_000
    statusbar_clock_interval_ms: int = 1_000
    toast_duration_ms: int = 4_000
    fuzzy_debounce_ms: int = 60


@dataclass(frozen=True, slots=True)
class NetworkConstants:
    """Defaults for HTTP and WebSocket clients."""

    default_teamserver_scheme: str = "https"
    default_teamserver_host: str = "127.0.0.1"
    default_teamserver_port: int = 4444
    default_teamserver_username: str = "operator"
    http_connect_timeout_seconds: float = 5.0
    http_read_timeout_seconds: float = 15.0
    http_user_agent: str = "LazyOwnOperatorConsole/2.0"
    websocket_path: str = "/socket.io/"
    api_data_path: str = "/api/data"
    api_issue_command_path: str = "/issue_command"
    api_run_path: str = "/api/run"
    api_output_path: str = "/api/output"


@dataclass(frozen=True, slots=True)
class PtyConstants:
    """Tunables for the local PTY backend."""

    read_chunk_bytes: int = 4_096
    spawn_executable: str = "/usr/bin/env"
    spawn_argv: tuple[str, ...] = ("bash", "run")
    encoding: str = "utf-8"
    encoding_errors: str = "replace"
    initial_cols: int = 140
    initial_rows: int = 40


@dataclass(frozen=True, slots=True)
class FontConstants:
    """Font family fallbacks (theme tokens decide colours and sizes)."""

    monospace_stack: tuple[str, ...] = (
        "JetBrains Mono",
        "Berkeley Mono",
        "Fira Code",
        "Hack",
        "DejaVu Sans Mono",
        "monospace",
    )
    sans_stack: tuple[str, ...] = (
        "Inter",
        "SF Pro Text",
        "Segoe UI",
        "Cantarell",
        "DejaVu Sans",
        "sans-serif",
    )
    base_pt: int = 10
    title_pt: int = 12
    monospace_pt: int = 11


@dataclass(frozen=True, slots=True)
class KeybindingConstants:
    """Application-wide keyboard shortcuts in Qt sequence notation."""

    command_palette: str = "Ctrl+K"
    cycle_theme: str = "Ctrl+Shift+T"
    toggle_sessions_panel: str = "Ctrl+1"
    toggle_listeners_panel: str = "Ctrl+2"
    toggle_event_log_panel: str = "Ctrl+3"
    toggle_terminal_focus: str = "Ctrl+`"
    quit_application: str = "Ctrl+Q"
    refresh_data: str = "F5"
    open_connect_dialog: str = "Ctrl+Shift+C"


@dataclass(frozen=True, slots=True)
class IdentifierConstants:
    """Stable string identifiers for object names and settings keys."""

    organization_name: str = "LazyOwn"
    organization_domain: str = "lazyown.local"
    application_name: str = "OperatorConsole"
    settings_filename: str = "settings.json"
    layout_filename: str = "layout.bin"
    theme_setting_key: str = "ui/theme"
    last_backend_setting_key: str = "connection/last_backend"
    last_teamserver_url_setting_key: str = "connection/last_teamserver_url"
    last_operator_name_setting_key: str = "connection/last_operator_name"
    geometry_setting_key: str = "ui/geometry"
    state_setting_key: str = "ui/state"


@dataclass(frozen=True, slots=True)
class ThemeConstants:
    """Constants relevant to theme registration."""

    default_palette_id: str = "tactical_green"
    palette_ids: tuple[str, ...] = (
        "tactical_green",
        "tokyo_night",
        "catppuccin_mocha",
        "gruvbox_dark",
        "cobalt_clone",
        "solarized_light",
    )


@dataclass(frozen=True, slots=True)
class BackendConstants:
    """Identifiers for the available backend implementations."""

    local_id: str = "local"
    teamserver_id: str = "teamserver"
    available_ids: tuple[str, ...] = ("local", "teamserver")


@dataclass(frozen=True, slots=True)
class PanelConstants:
    """Identifiers and labels for dockable panels."""

    sessions_id: str = "panel.sessions"
    listeners_id: str = "panel.listeners"
    event_log_id: str = "panel.event_log"
    terminal_id: str = "panel.terminal"
    sessions_label: str = "Sessions"
    listeners_label: str = "Listeners"
    event_log_label: str = "Event Log"
    terminal_label: str = "Console"


@dataclass(frozen=True, slots=True)
class EventLogConstants:
    """Bounds for the event-log ring buffer."""

    max_records: int = 5_000
    default_level_filter: str = "info"
    levels: tuple[str, ...] = ("debug", "info", "warning", "error", "critical")


@dataclass(frozen=True, slots=True)
class CommandPaletteConstants:
    """Tunables for the fuzzy command palette."""

    max_results: int = 12
    min_query_length: int = 0
    placeholder_text: str = "Type a command, session, listener or action..."


@dataclass(frozen=True, slots=True)
class AppConstants:
    """Aggregate view exposing every constant group as attributes."""

    window: WindowConstants = field(default_factory=WindowConstants)
    timing: TimingConstants = field(default_factory=TimingConstants)
    network: NetworkConstants = field(default_factory=NetworkConstants)
    pty: PtyConstants = field(default_factory=PtyConstants)
    font: FontConstants = field(default_factory=FontConstants)
    keys: KeybindingConstants = field(default_factory=KeybindingConstants)
    ids: IdentifierConstants = field(default_factory=IdentifierConstants)
    theme: ThemeConstants = field(default_factory=ThemeConstants)
    backend: BackendConstants = field(default_factory=BackendConstants)
    panel: PanelConstants = field(default_factory=PanelConstants)
    event_log: EventLogConstants = field(default_factory=EventLogConstants)
    palette: CommandPaletteConstants = field(default_factory=CommandPaletteConstants)

    def panel_labels(self) -> Mapping[str, str]:
        """Map panel identifier to human-readable label."""
        return {
            self.panel.sessions_id: self.panel.sessions_label,
            self.panel.listeners_id: self.panel.listeners_label,
            self.panel.event_log_id: self.panel.event_log_label,
            self.panel.terminal_id: self.panel.terminal_label,
        }
