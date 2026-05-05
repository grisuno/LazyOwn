"""Factory for backend instances.

Encapsulates the construction logic so the rest of the GUI never imports a
concrete backend class. The factory keeps the GUI honoring the
Open/Closed principle: adding a new backend means writing a new class and
registering it here, not editing the windows or panels.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QObject

from lazygui.config.constants import AppConstants
from lazygui.config.paths import AppPaths
from lazygui.services.backend import Backend
from lazygui.services.local_backend import LocalPtyBackend
from lazygui.services.models import BackendKind
from lazygui.services.teamserver_backend import TeamserverBackend, TeamserverCredentials


@dataclass(frozen=True, slots=True)
class BackendFactory:
    """Build :class:`Backend` instances from runtime parameters."""

    constants: AppConstants
    paths: AppPaths

    def create_local(self, parent: QObject | None = None) -> LocalPtyBackend:
        """Construct a local PTY-based backend."""
        return LocalPtyBackend(constants=self.constants, paths=self.paths, parent=parent)

    def create_teamserver(
        self,
        credentials: TeamserverCredentials,
        parent: QObject | None = None,
    ) -> TeamserverBackend:
        """Construct a teamserver-based backend with the given credentials."""
        return TeamserverBackend(constants=self.constants, credentials=credentials, parent=parent)

    def create(
        self,
        kind: BackendKind,
        parent: QObject | None = None,
        credentials: TeamserverCredentials | None = None,
    ) -> Backend:
        """Convenience dispatch by :class:`BackendKind`."""
        if kind is BackendKind.LOCAL:
            return self.create_local(parent=parent)
        if kind is BackendKind.TEAMSERVER:
            if credentials is None:
                raise ValueError("Teamserver backend requires credentials.")
            return self.create_teamserver(credentials=credentials, parent=parent)
        raise ValueError(f"Unsupported backend kind: {kind!r}")
