"""Command & Control command set.

Phase-scoped home for the C2 / beacon operator commands (category
``10. Command & Control``). This module is intentionally an empty, active
``CommandSet`` scaffold: migrate one ``do_*`` method at a time out of
``lazyown.py`` into this class.

Migration rule
--------------
When you paste a ``do_<name>`` method here you MUST delete the original copy
from ``lazyown.py`` in the same change. Registering the same command name on
both the shell and an active ``CommandSet`` raises a duplicate-command error
at startup. Decorate migrated methods with
``@cmd2.with_category(command_and_control_category)`` so they keep their help
grouping, and rely on :class:`cli.commands._base.LazyOwnCommandSet` to forward
``self.params`` / ``self.cmd`` / other shell state once registered.

Discovery is automatic: :func:`cli.registry.register_command_sets` finds this
class at startup, so no wiring change is needed as commands are added.
"""

from __future__ import annotations

from cli.commands._base import LazyOwnCommandSet
from utils import command_and_control_category


class CommandAndControlCommandSet(LazyOwnCommandSet):
    """Command & Control phase commands (migrate ``do_*`` here one at a time)."""

    phase = "c2"
    category = command_and_control_category


__all__ = ["CommandAndControlCommandSet"]
