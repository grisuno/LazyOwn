# `lazygui`

> Source: [lazygui/__init__.py:1](../../lazygui/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

LazyOwn Operator Console.

A PySide6-based desktop client for the LazyOwn red-team framework. Supports
two operating modes:

* Local mode: spawns the cmd2 console (``lazyown.py``) over a PTY.
* Teamserver mode: communicates with the Flask backend (``lazyc2.py``) via
  HTTP and WebSocket, allowing multi-operator workflows.

The package is organised following SOLID principles. Cross-cutting concerns
live in dedicated subpackages:

* [`lazygui.config`](lazygui.config.__init__.py.md)   - tunable constants, paths, user-settings.
* [`lazygui.theme`](lazygui.theme.__init__.py.md)    - theme tokens, QSS builder, palette registry.
* [`lazygui.services`](lazygui.services.__init__.py.md) - backend abstraction and domain models.
* [`lazygui.widgets`](lazygui.widgets.__init__.py.md)  - reusable Qt widgets.
* [`lazygui.panels`](lazygui.panels.__init__.py.md)   - dockable panels composed in the main window.
* [`lazygui.windows`](lazygui.windows.__init__.py.md)  - top-level windows and dialogs.
