"""Dormancy marker for incrementally migrated command sets.

During the staged migration of the ``do_*`` methods from ``lazyown.py`` into
phase-scoped ``CommandSet`` modules under ``cli/commands/``, both sources
temporarily coexist:

* ``LazyOwnShell`` in ``lazyown.py`` still owns the canonical methods.
* The new phase modules carry a parallel copy ready for activation.

If the new modules registered immediately, ``cmd2.register_command_set``
would raise ``CommandSetRegistrationError`` for every method that collides
with an attribute already bound to the shell. To avoid that without
sacrificing discoverability or test coverage, migrated sets inherit from
:class:`PendingCommandSet`. ``cli.registry.register_command_sets`` skips
any class flagged this way; once the originals are deleted from
``lazyown.py`` the base class is swapped to :class:`LazyOwnCommandSet`
and the set joins the active registry on the next shell start.

Discovery (``iter_command_sets``) still yields pending sets so tests can
validate their structure independently of activation.
"""

from __future__ import annotations

from cli.commands._base import LazyOwnCommandSet

PENDING_FLAG_ATTRIBUTE = "__lazyown_pending__"


class PendingCommandSet(LazyOwnCommandSet):
    """Base class for migrated-but-not-yet-active phase command sets.

    Subclasses are discovered by :func:`cli.registry.iter_command_sets` but
    excluded from :func:`cli.registry.register_command_sets`, so the
    framework boots without colliding with the equivalent ``do_*`` methods
    still defined on :class:`LazyOwnShell`.

    Activation procedure:
        1. Remove the equivalent ``do_*`` methods from ``lazyown.py``.
        2. Change the subclass base from :class:`PendingCommandSet` to
           :class:`LazyOwnCommandSet`.
        3. Restart the shell (``./run``) or the MCP server
           (``bash skills/mcp_restart.sh``).

    The marker is read via ``getattr(cls, '__lazyown_pending__', False)``
    so non-marker subclasses always opt out by absence.
    """

    __lazyown_pending__: bool = True


def is_pending(cs_class: type) -> bool:
    """Return ``True`` when ``cs_class`` is flagged as a pending migration.

    Args:
        cs_class: A ``CommandSet`` subclass discovered by the registry.

    Returns:
        ``True`` when the class declares ``__lazyown_pending__ = True``,
        either directly or through inheritance from :class:`PendingCommandSet`.
        ``False`` for active sets and for non-class inputs.
    """
    if not isinstance(cs_class, type):
        return False
    return bool(getattr(cs_class, PENDING_FLAG_ATTRIBUTE, False))


__all__ = ["PendingCommandSet", "PENDING_FLAG_ATTRIBUTE", "is_pending"]
