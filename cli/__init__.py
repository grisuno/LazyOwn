"""LazyOwn CLI infrastructure.

Tier 2 introduces a declarative, modular layer above ``lazyown.py``:

- ``cli/aliases.yaml`` and :func:`cli.aliases.load_aliases` provide cmd2
  aliases as data instead of f-strings hard-coded in the shell class.
- ``cli/registry.py`` mounts ``cmd2.CommandSet`` instances onto the running
  ``LazyOwnShell``, opening the door to phase-based command modules
  (``cli/commands/recon.py``, ``cli/commands/exploit.py``, ...) without
  touching the 27k-LOC monolith.
"""

from cli.aliases import load_aliases
from cli.registry import iter_command_sets, register_command_sets

__all__ = ["load_aliases", "iter_command_sets", "register_command_sets"]
