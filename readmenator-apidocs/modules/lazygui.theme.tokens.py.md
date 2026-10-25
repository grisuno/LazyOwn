# `lazygui.theme.tokens`

> Source: [lazygui/theme/tokens.py:1](../../lazygui/theme/tokens.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Design tokens describing a single theme.

Tokens are immutable. They cover colours, typography sizes and corner radii.
Anything that should differ between themes must be expressed here so the QSS
builder can render it without consulting any other source of truth.

## Contents

- **Classes:** [`ThemeTokens`](#themetokens)

## Classes

<a id="themetokens"></a>

### `ThemeTokens`

`class` `dataclass` | [lazygui/theme/tokens.py:14](../../lazygui/theme/tokens.py#L14)

Decorators: `@dataclass(frozen=True, slots=True)`

```python
class ThemeTokens
```

Atomic design tokens for one theme variant.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`identifier`](#themetokens-identifier) | `str` |  |  |
| [`display_name`](#themetokens-display_name) | `str` |  |  |
| [`is_dark`](#themetokens-is_dark) | `bool` |  |  |
| [`background_base`](#themetokens-background_base) | `str` |  |  |
| [`background_elevated`](#themetokens-background_elevated) | `str` |  |  |
| [`background_overlay`](#themetokens-background_overlay) | `str` |  |  |
| [`background_terminal`](#themetokens-background_terminal) | `str` |  |  |
| [`surface_subtle`](#themetokens-surface_subtle) | `str` |  |  |
| [`surface_strong`](#themetokens-surface_strong) | `str` |  |  |
| [`border_subtle`](#themetokens-border_subtle) | `str` |  |  |
| [`border_strong`](#themetokens-border_strong) | `str` |  |  |
| [`border_focus`](#themetokens-border_focus) | `str` |  |  |
| [`text_primary`](#themetokens-text_primary) | `str` |  |  |
| [`text_secondary`](#themetokens-text_secondary) | `str` |  |  |
| [`text_muted`](#themetokens-text_muted) | `str` |  |  |
| [`text_inverse`](#themetokens-text_inverse) | `str` |  |  |
| [`text_on_accent`](#themetokens-text_on_accent) | `str` |  |  |
| [`accent`](#themetokens-accent) | `str` |  |  |
| [`accent_hover`](#themetokens-accent_hover) | `str` |  |  |
| [`accent_pressed`](#themetokens-accent_pressed) | `str` |  |  |
| [`success`](#themetokens-success) | `str` |  |  |
| [`warning`](#themetokens-warning) | `str` |  |  |
| [`danger`](#themetokens-danger) | `str` |  |  |
| [`info`](#themetokens-info) | `str` |  |  |
| [`selection_background`](#themetokens-selection_background) | `str` |  |  |
| [`selection_foreground`](#themetokens-selection_foreground) | `str` |  |  |
| [`scrollbar_track`](#themetokens-scrollbar_track) | `str` |  |  |
| [`scrollbar_thumb`](#themetokens-scrollbar_thumb) | `str` |  |  |
| [`scrollbar_thumb_hover`](#themetokens-scrollbar_thumb_hover) | `str` |  |  |
| [`radius_small_px`](#themetokens-radius_small_px) | `int` |  |  |
| [`radius_medium_px`](#themetokens-radius_medium_px) | `int` |  |  |
| [`radius_large_px`](#themetokens-radius_large_px) | `int` |  |  |
| [`spacing_unit_px`](#themetokens-spacing_unit_px) | `int` |  |  |

---
