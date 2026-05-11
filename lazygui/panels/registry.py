"""Registry that owns all dock panels.

Centralising panel instances makes the main window straightforward: it
asks the registry for an iterable to attach as docks, looks panels up by
identifier when wiring shortcuts, and forwards visibility toggles
polymorphically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from PySide6.QtWidgets import QWidget

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.panels.event_log_panel import EventLogPanel
from lazygui.panels.listeners_panel import ListenersPanel
from lazygui.panels.sessions_panel import SessionsPanel
from lazygui.panels.terminal_panel import TerminalPanel
from lazygui.services.backend import Backend
from lazygui.services.event_log import EventLog


@dataclass(slots=True)
class PanelRegistry:
    """Holds the canonical panel instances bound to the active backend."""

    constants: AppConstants
    backend: Backend
    event_log: EventLog
    sessions: SessionsPanel
    listeners: ListenersPanel
    event_log_panel: EventLogPanel
    terminal: TerminalPanel

    @classmethod
    def build(
        cls,
        constants: AppConstants,
        backend: Backend,
        event_log: EventLog,
        parent: QWidget | None = None,
    ) -> PanelRegistry:
        """Construct every dock panel and return them as a registry."""
        return cls(
            constants=constants,
            backend=backend,
            event_log=event_log,
            sessions=SessionsPanel(constants=constants, backend=backend, parent=parent),
            listeners=ListenersPanel(constants=constants, backend=backend, parent=parent),
            event_log_panel=EventLogPanel(
                constants=constants,
                backend=backend,
                event_log=event_log,
                parent=parent,
            ),
            terminal=TerminalPanel(constants=constants, backend=backend, parent=parent),
        )

    def all_panels(self) -> tuple[PanelBase, ...]:
        """Return panels in canonical layout order."""
        return (self.sessions, self.listeners, self.terminal, self.event_log_panel)

    def by_identifier(self, identifier: str) -> PanelBase:
        """Look up a panel by its stable identifier."""
        for panel in self.all_panels():
            if panel.identifier == identifier:
                return panel
        raise KeyError(f"Unknown panel identifier: {identifier!r}")

    def __iter__(self) -> Iterator[PanelBase]:
        """Iterate over panels in canonical order."""
        return iter(self.all_panels())
