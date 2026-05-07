"""Base utilities shared by phase ``CommandSet`` modules.

``LazyOwnCommandSet`` extends ``cmd2.CommandSet`` with two affordances:

- ``self.params`` — convenience accessor that mirrors ``self._cmd.params`` so
  command implementations do not have to dereference the parent shell.
- ``self.payload`` — the live ``payload.json`` snapshot; ``Config``-wrapped if
  the parent exposes one.

Subclasses define ``do_<name>`` methods exactly like they would on
``LazyOwnShell``; the cmd2 dispatcher routes calls transparently once the set
is registered.
"""

from __future__ import annotations

from typing import Any

from cmd2 import CommandSet


class LazyOwnCommandSet(CommandSet):
    """Base for every Tier-2 phase CommandSet.

    Attributes:
        phase: Kill-chain phase identifier (``recon``, ``enum``, ...). Used by
            tooling such as ``lazyown_phase_guide`` and the autonomous daemon
            to filter commands by phase.
        category: cmd2 help category label. Defaults to a Title-Case form of
            ``phase`` if not set explicitly.
    """

    phase: str = ""
    category: str = ""

    @property
    def params(self) -> dict[str, Any]:
        """Live ``params`` dict from the parent shell."""
        shell = getattr(self, "_cmd", None)
        return getattr(shell, "params", {}) if shell is not None else {}

    @property
    def payload(self) -> Any:
        """Parent shell's ``Config`` wrapper if available, else ``params``."""
        shell = getattr(self, "_cmd", None)
        if shell is None:
            return {}
        return getattr(shell, "config", None) or getattr(shell, "params", {})


__all__ = ["LazyOwnCommandSet"]
