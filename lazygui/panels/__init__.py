"""Dockable panels assembled from the reusable widgets.

Each panel is a thin :class:`QDockWidget` that owns a single concern
(sessions, listeners, console, event log) and connects itself to the
backend signals it needs. The :class:`PanelRegistry` exposes them by
identifier so the main window can wire menu actions and keyboard
shortcuts polymorphically.
"""

from lazygui.panels.base import PanelBase
from lazygui.panels.event_log_panel import EventLogPanel
from lazygui.panels.listeners_panel import ListenersPanel
from lazygui.panels.registry import PanelRegistry
from lazygui.panels.sessions_panel import SessionsPanel
from lazygui.panels.terminal_panel import TerminalPanel

__all__ = [
    "EventLogPanel",
    "ListenersPanel",
    "PanelBase",
    "PanelRegistry",
    "SessionsPanel",
    "TerminalPanel",
]
