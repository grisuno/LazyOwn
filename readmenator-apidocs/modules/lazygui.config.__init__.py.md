# `lazygui.config`

> Source: [lazygui/config/__init__.py:1](../../lazygui/config/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Configuration layer.

Centralises every tunable parameter so the rest of the package never embeds a
magic number or a hard-coded path. Three concerns are exposed:

* [`lazygui.config.constants.AppConstants`](lazygui.config.constants.py.md#appconstants) - immutable defaults.
* [`lazygui.config.paths.AppPaths`](lazygui.config.paths.py.md#apppaths) - filesystem layout resolver.
* [`lazygui.config.settings.AppSettings`](lazygui.config.settings.py.md#appsettings) - mutable, persisted overrides.
