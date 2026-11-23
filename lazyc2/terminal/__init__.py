"""Terminal namespaces for the C2 server.

Owns the Socket.IO terminal glue: the ``/listener``, ``/pty`` and
``/terminal`` namespaces plus the ``/terminal`` HTTP page. All handlers
are registered through :func:`register_terminal_glue` so ``lazyc2.py``
keeps only the wiring call.
"""

from lazyc2.terminal.glue import register_terminal_glue

__all__ = ["register_terminal_glue"]
