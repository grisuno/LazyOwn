"""Base class for phase-scoped ``CommandSet`` modules.

``LazyOwnCommandSet`` extends :class:`cmd2.CommandSet` with the affordances
that the legacy ``do_*`` methods rely on when they are lifted out of
``LazyOwnShell`` and into per-phase modules under ``cli/commands/``.

Two design constraints shape this base class:

1. The migrated methods must execute verbatim. They reference shell
   attributes such as ``self.params``, ``self.scripts``, ``self.c2_url``
   and instance helpers like ``self.run_script``. Rewriting hundreds of
   call sites is unsafe; instead this base forwards unknown attribute
   reads to the bound shell once ``cmd2`` injects it through
   ``register_command_set``.

2. Forwarding must remain inert before registration. Tests instantiate
   sets directly to assert structure (method presence, decorators); those
   instances have no parent shell, so unknown attribute access must raise
   :class:`AttributeError` exactly as a plain class would.
"""

from __future__ import annotations

from typing import Any

from cmd2 import CommandSet
from cmd2.exceptions import CommandSetRegistrationError

SHELL_INJECTION_ATTRIBUTE = "_cmd"


class LazyOwnCommandSet(CommandSet):
    """Base class for every phase ``CommandSet`` defined under ``cli.commands``.

    Attributes:
        phase: Kill-chain phase identifier (``recon``, ``enum``, ...). Used
            by tooling such as ``lazyown_phase_guide`` and the autonomous
            daemon to filter commands by phase.
        category: cmd2 help category label. Defaults to a Title-Case form
            of ``phase`` when not set explicitly.
    """

    phase: str = ""
    category: str = ""

    def _resolve_shell(self) -> Any:
        """Return the bound parent shell, or ``None`` before registration.

        ``cmd2`` stores the parent shell in a name-mangled private attribute
        and exposes it through the :attr:`cmd2.CommandSet._cmd` property, which
        raises :class:`CommandSetRegistrationError` until the set is
        registered. This helper centralises that access so the migrated
        ``do_*`` methods can forward attribute reads without leaking the cmd2
        registration exception or depending on cmd2 internals.

        Returns:
            The parent ``LazyOwnShell`` instance once the set is registered,
            otherwise ``None``.
        """
        try:
            shell = self._cmd
        except CommandSetRegistrationError:
            return None
        return shell if shell is not self else None

    @property
    def params(self) -> dict[str, Any]:
        """Return the live ``params`` dict owned by the parent shell.

        Returns:
            The same dict object that ``LazyOwnShell.params`` exposes when
            the set is registered, or an empty dict when it is not.
        """
        shell = self._resolve_shell()
        return getattr(shell, "params", {}) if shell is not None else {}

    @property
    def payload(self) -> Any:
        """Return the parent shell's ``Config`` wrapper when available.

        Returns:
            ``LazyOwnShell.config`` when the shell publishes it, otherwise
            ``LazyOwnShell.params`` so callers always receive a mapping-
            like object. Falls back to an empty dict before registration.
        """
        shell = self._resolve_shell()
        if shell is None:
            return {}
        return getattr(shell, "config", None) or getattr(shell, "params", {})

    def __getattr__(self, name: str) -> Any:
        """Forward unknown attribute access to the bound shell.

        ``cmd2`` binds the parent shell to ``self._cmd`` when the
        ``CommandSet`` is registered. Migrated methods reference shell
        state directly (``self.run_script``, ``self.c2_url``, ...) so this
        forwarder lets them execute unmodified once they are wired in.

        Args:
            name: Attribute name requested by the caller.

        Returns:
            The attribute value resolved on the bound shell.

        Raises:
            AttributeError: When ``name`` starts with an underscore, when
                the shell is not yet bound, or when the shell itself does
                not expose ``name``.
        """
        if name.startswith("_"):
            raise AttributeError(name)
        shell = self._resolve_shell()
        if shell is None:
            raise AttributeError(name)
        return getattr(shell, name)


__all__ = ["LazyOwnCommandSet", "SHELL_INJECTION_ATTRIBUTE"]
