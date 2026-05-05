"""Common :class:`QDockWidget` base for every panel.

Centralises ``objectName`` assignment (required for ``QMainWindow.saveState``
to round-trip) and exposes a hook so subclasses can perform backend wiring
in a uniform way.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QWidget

from lazygui.config.constants import AppConstants
from lazygui.services.backend import Backend


class PanelBase(QDockWidget):
    """Base class enforcing object-name discipline and backend wiring."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        identifier: str,
        title: str,
        parent: QWidget | None = None,
    ) -> None:
        """Initialise the dock widget with stable identifier and title."""
        super().__init__(title, parent)
        self._constants = constants
        self._backend = backend
        self._identifier = identifier
        self.setObjectName(identifier)
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable
            | QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.setMinimumSize(constants.window.dock_min_width, constants.window.dock_min_height)

    @property
    def identifier(self) -> str:
        """Stable identifier matching :class:`PanelConstants`."""
        return self._identifier

    @property
    def backend(self) -> Backend:
        """The currently connected backend instance."""
        return self._backend
