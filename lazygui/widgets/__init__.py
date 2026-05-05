"""Reusable widgets.

Each widget is owned by a single concern and accepts the global
:class:`AppConstants` plus the active :class:`ThemeTokens` so it can render
itself consistently with the rest of the application without depending on
panels, windows, or backends.
"""

from lazygui.widgets.terminal_view import TerminalView
from lazygui.widgets.event_log_view import EventLogView
from lazygui.widgets.status_badge import StatusBadge
from lazygui.widgets.filter_bar import FilterBar
from lazygui.widgets.command_palette_list import CommandPaletteList, CommandPaletteAction

__all__ = [
    "CommandPaletteAction",
    "CommandPaletteList",
    "EventLogView",
    "FilterBar",
    "StatusBadge",
    "TerminalView",
]
