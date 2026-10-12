# `lazygui.panels`

> Source: [lazygui/panels/__init__.py:1](../../lazygui/panels/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Dockable panels assembled from the reusable widgets.

Each panel is a thin `QDockWidget` that owns a single concern
(sessions, listeners, console, event log) and connects itself to the
backend signals it needs. The [`PanelRegistry`](lazygui.panels.registry.py.md#panelregistry) exposes them by
identifier so the main window can wire menu actions and keyboard
shortcuts polymorphically.
