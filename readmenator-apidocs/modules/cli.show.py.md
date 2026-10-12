# `cli.show`

> Source: [cli/show.py:1](../../cli/show.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Pretty-print the live payload for the operator.

Tier 2.5 replaces `[`do_show`](cli.commands.session_ops.py.md#sessionopscommandset-do_show)`'s unordered, unaligned dump with a stable,
deterministic rendering. Output is plain text (no ANSI) so the formatter is
easy to test and reusable for logs, reports or the dashboard.

## Contents

- **Functions:** [`format_payload`](#format_payload)

## Functions

<a id="format_payload"></a>

### `format_payload`

`function` | [cli/show.py:14](../../cli/show.py#L14)

```python
def format_payload(params: dict[str, Any], *, keys: Iterable[str] | None = None) -> str
```

Render ``params`` as a sorted, aligned ``key = value`` block.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `params` | `dict[str, Any]` |  | Payload dict. |
| `keys` | `Iterable[str] \| None` | `None` | Optional whitelist; when given, only those keys are rendered (in the same alphabetical order). Missing keys render as empty strings, matching the alias loader's behaviour. |

**Returns:** `str` - A multi-line string. Each line is ``"<key padded>  <value>"``. The
column width is computed from the rendered key set so output stays
aligned regardless of which keys are present.

---
