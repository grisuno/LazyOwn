# `lazygui.theme.qss_builder`

> Source: [lazygui/theme/qss_builder.py:1](../../lazygui/theme/qss_builder.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Builds a Qt stylesheet string from [`ThemeTokens`](lazygui.theme.tokens.py.md#themetokens).

Centralising the QSS template here keeps widgets ignorant of styling. They
declare ``objectName``s and selectors; the builder owns the visual contract.

## Contents

- **Classes:** [`QssBuilder`](#qssbuilder)

## Classes

<a id="qssbuilder"></a>

### `QssBuilder`

`class` `dataclass` | [lazygui/theme/qss_builder.py:16](../../lazygui/theme/qss_builder.py#L16)

Decorators: `@dataclass(frozen=True, slots=True)`

```python
class QssBuilder
```

Renders a complete QSS sheet for a given theme.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`constants`](#qssbuilder-constants) | `AppConstants` |  |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`build`](#qssbuilder-build) | method | Return the full QSS sheet for ``tokens``. |

<a id="qssbuilder-build"></a>

#### `QssBuilder.build`

`method` | [lazygui/theme/qss_builder.py:21](../../lazygui/theme/qss_builder.py#L21)

```python
def build(self, tokens: ThemeTokens) -> str
```

Return the full QSS sheet for ``tokens``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `tokens` | `ThemeTokens` |  |  |

**Returns:** `str`

---
