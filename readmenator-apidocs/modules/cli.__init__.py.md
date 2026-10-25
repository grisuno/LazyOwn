# `cli`

> Source: [cli/__init__.py:1](../../cli/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

LazyOwn CLI infrastructure.

Tier 2 introduces a declarative, modular layer above ``lazyown.py``:

- ``cli/aliases.yaml`` and [`cli.aliases.load_aliases`](cli.aliases.py.md#load_aliases) provide cmd2
  aliases as data instead of f-strings hard-coded in the shell class.
- ``cli/registry.py`` mounts ``cmd2.CommandSet`` instances onto the running
  `[`LazyOwnShell`](lazyown.py.md#lazyownshell)`, opening the door to phase-based command modules
  (``cli/commands/recon.py``, ``cli/commands/exploit.py``, ...) without
  touching the 27k-LOC monolith.
