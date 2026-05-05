"""LazyOwn Operator Console.

A PySide6-based desktop client for the LazyOwn red-team framework. Supports
two operating modes:

* Local mode: spawns the cmd2 console (``lazyown.py``) over a PTY.
* Teamserver mode: communicates with the Flask backend (``lazyc2.py``) via
  HTTP and WebSocket, allowing multi-operator workflows.

The package is organised following SOLID principles. Cross-cutting concerns
live in dedicated subpackages:

* :mod:`lazygui.config`   - tunable constants, paths, user-settings.
* :mod:`lazygui.theme`    - theme tokens, QSS builder, palette registry.
* :mod:`lazygui.services` - backend abstraction and domain models.
* :mod:`lazygui.widgets`  - reusable Qt widgets.
* :mod:`lazygui.panels`   - dockable panels composed in the main window.
* :mod:`lazygui.windows`  - top-level windows and dialogs.
"""

from lazygui.version import VERSION as __version__

__all__ = ["__version__"]
