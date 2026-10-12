# `core.text_utils`

> Source: [core/text_utils.py:1](../../core/text_utils.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Shared text helpers for terminal surfaces.

Single source of truth for truncating display strings. Replaces eight
near-identical ``_truncate`` copies across ``cli/``.

## Contents

- **Functions:** [`truncate_text`](#truncate_text)

## Functions

<a id="truncate_text"></a>

### `truncate_text`

`function` | [core/text_utils.py:10](../../core/text_utils.py#L10)

```python
def truncate_text(value: str | None, max_len: int, marker: str = '…') -> str
```

Truncate value to max_len using marker.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `str \| None` |  | Text to truncate. None becomes empty string. |
| `max_len` | `int` |  | Maximum output length including marker. |
| `marker` | `str` | `'…'` | Suffix appended when truncation occurs. |

**Returns:** `str` - Truncated string of at most max_len characters.

*Called by:* [`PaletteRenderConfig.truncate_summary`](cli.palette_command.py.md#paletterenderconfig-truncate_summary)

---
