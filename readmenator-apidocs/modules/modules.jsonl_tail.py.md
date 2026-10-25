# `modules.jsonl_tail`

> Source: [modules/jsonl_tail.py:1](../../modules/jsonl_tail.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Incremental JSONL reader shared by the monitor TUI and the loop runner.

The activity log only ever appends, so a byte offset is a stable cursor:
each reader keeps its own offset and returns only complete records,
tolerating a partially written final line.

## Contents

- **Classes:** [`JsonlTail`](#jsonltail)

## Classes

<a id="jsonltail"></a>

### `JsonlTail`

`class` | [modules/jsonl_tail.py:14](../../modules/jsonl_tail.py#L14)

```python
class JsonlTail
```

Incremental JSONL reader that tolerates partially-written lines.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#jsonltail-__init__) | constructor | Bind the tail to one file path. |
| [`read_new`](#jsonltail-read_new) | method | Return new complete records since the last call. |

<a id="jsonltail-__init__"></a>

#### `JsonlTail.__init__`

`constructor` | [modules/jsonl_tail.py:17](../../modules/jsonl_tail.py#L17)

```python
def __init__(self, path: str | Path) -> None
```

Bind the tail to one file path.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` |  |  |

<a id="jsonltail-read_new"></a>

#### `JsonlTail.read_new`

`method` | [modules/jsonl_tail.py:22](../../modules/jsonl_tail.py#L22)

```python
def read_new(self, limit: int = 500) -> list[dict]
```

Return new complete records since the last call.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `limit` | `int` | `500` |  |

**Returns:** `list[dict]`

---
