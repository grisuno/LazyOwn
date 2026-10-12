# `lazygui.theme`

> Source: [lazygui/theme/__init__.py:1](../../lazygui/theme/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Theme subsystem.

Themes are described by [`ThemeTokens`](lazygui.theme.tokens.py.md#themetokens) instances. The
[`QssBuilder`](lazygui.theme.qss_builder.py.md#qssbuilder) translates tokens into a Qt stylesheet, and
[`ThemeManager`](lazygui.theme.manager.py.md#thememanager) registers palettes, applies them to the running
`QApplication`, and emits a Qt signal when the active theme changes so
widgets can react.
