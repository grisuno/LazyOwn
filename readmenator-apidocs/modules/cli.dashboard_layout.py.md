# `cli.dashboard_layout`

> Source: [cli/dashboard_layout.py:1](../../cli/dashboard_layout.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Responsive layout decisions for the Textual operator dashboard.

Small terminals crush the fixed three-column layout. This module keeps
the width thresholds and panel visibility rules in one testable place;
the dashboard app only toggles CSS classes based on these answers.

## Contents

- **Classes:** [`DashboardLayoutConfig`](#dashboardlayoutconfig)
- **Functions:** [`layout_mode`](#layout_mode), [`hidden_panels`](#hidden_panels)
- **Constants:** [`DEFAULT_LAYOUT_CONFIG`](#default_layout_config), [`LAYOUT_WIDE`](#layout_wide), [`LAYOUT_NARROW`](#layout_narrow), [`LAYOUT_COMPACT`](#layout_compact)

## Classes

<a id="dashboardlayoutconfig"></a>

### `DashboardLayoutConfig`

`class` `dataclass` | [cli/dashboard_layout.py:14](../../cli/dashboard_layout.py#L14)

Decorators: `@dataclass(frozen=True)`

```python
class DashboardLayoutConfig
```

Centralized knobs for responsive breakpoints.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`narrow_width`](#dashboardlayoutconfig-narrow_width) | `int` | `120` |  |
| [`compact_width`](#dashboardlayoutconfig-compact_width) | `int` | `80` |  |

---

## Functions

<a id="layout_mode"></a>

### `layout_mode`

`function` | [cli/dashboard_layout.py:28](../../cli/dashboard_layout.py#L28)

```python
def layout_mode(width: int, config: DashboardLayoutConfig = DEFAULT_LAYOUT_CONFIG) -> str
```

Return the layout bucket for a terminal width.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `width` | `int` |  | Terminal width in columns. |
| `config` | `DashboardLayoutConfig` | `DEFAULT_LAYOUT_CONFIG` | Breakpoint configuration. |

**Returns:** `str` - wide, narrow or compact.

*Called by:* [`LazyOwnDashboard.action_toggle_compact`](cli.dashboard_tui.py.md#lazyowndashboard-action_toggle_compact)

---

<a id="hidden_panels"></a>

### `hidden_panels`

`function` | [cli/dashboard_layout.py:45](../../cli/dashboard_layout.py#L45)

```python
def hidden_panels(mode: str) -> tuple[str, ...]
```

Return panel ids hidden in the given layout mode.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` |  | One of wide, narrow or compact. |

**Returns:** `tuple[str, ...]` - Tuple of widget ids to hide. Wide hides nothing, narrow hides
the reasoning panel, compact additionally hides the right column.

---

## Constants

<a id="default_layout_config"></a>

### `DEFAULT_LAYOUT_CONFIG`

`constant` | [cli/dashboard_layout.py:21](../../cli/dashboard_layout.py#L21)

```python
DEFAULT_LAYOUT_CONFIG = DashboardLayoutConfig()
```

---

<a id="layout_wide"></a>

### `LAYOUT_WIDE`

`constant` | [cli/dashboard_layout.py:23](../../cli/dashboard_layout.py#L23)

```python
LAYOUT_WIDE = 'wide'
```

---

<a id="layout_narrow"></a>

### `LAYOUT_NARROW`

`constant` | [cli/dashboard_layout.py:24](../../cli/dashboard_layout.py#L24)

```python
LAYOUT_NARROW = 'narrow'
```

---

<a id="layout_compact"></a>

### `LAYOUT_COMPACT`

`constant` | [cli/dashboard_layout.py:25](../../cli/dashboard_layout.py#L25)

```python
LAYOUT_COMPACT = 'compact'
```

---
