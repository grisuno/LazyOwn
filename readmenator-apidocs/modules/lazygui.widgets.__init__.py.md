# `lazygui.widgets`

> Source: [lazygui/widgets/__init__.py:1](../../lazygui/widgets/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Reusable widgets.

Each widget is owned by a single concern and accepts the global
[`AppConstants`](lazygui.config.constants.py.md#appconstants) plus the active [`ThemeTokens`](lazygui.theme.tokens.py.md#themetokens) so it can render
itself consistently with the rest of the application without depending on
panels, windows, or backends.
