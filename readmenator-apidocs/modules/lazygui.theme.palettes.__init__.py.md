# `lazygui.theme.palettes`

> Source: [lazygui/theme/palettes/__init__.py:1](../../lazygui/theme/palettes/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Built-in palette registry.

Each palette module exposes a ``TOKENS`` instance of [`ThemeTokens`](lazygui.theme.tokens.py.md#themetokens).
[`builtin_palettes`](#builtin_palettes) returns them all in declaration order so callers
need not enumerate filenames manually.

## Contents

- **Functions:** [`builtin_palettes`](#builtin_palettes)

## Functions

<a id="builtin_palettes"></a>

### `builtin_palettes`

`function` | [lazygui/theme/palettes/__init__.py:23](../../lazygui/theme/palettes/__init__.py#L23)

```python
def builtin_palettes() -> Mapping[str, ThemeTokens]
```

Return the built-in palette registry as ``id -> tokens``.

**Returns:** `Mapping[str, ThemeTokens]`

*Called by:* [`ThemeManager.__init__`](lazygui.theme.manager.py.md#thememanager-__init__)

---
