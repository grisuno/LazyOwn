# `skills.mcp_tools.get_config`

> Source: [skills/mcp_tools/get_config.py:1](../../skills/mcp_tools/get_config.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_get_config``: read the current payload.json config.

First tool migrated out of the ``lazyown_mcp`` god-file into the
one-file-per-tool registry. It is the reference implementation: a `[`TOOL`](#tool)`
schema plus a `[`handle`](#handle)` function that takes its dependencies from the
injected `mcp_tools._context.MCPContext` and imports nothing from
the runtime.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/get_config.py:26](../../skills/mcp_tools/get_config.py#L26)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return the full ``payload.json`` as pretty-printed JSON text.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  | Unused; the tool takes no parameters. |
| `tool_name` | `str` |  | The dispatched tool name, used for the text envelope. |
| `ctx` | `MCPContext` |  | Injected runtime helpers. |

**Returns:** `list` - A one-element ``TextContent`` list holding the config JSON.

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/get_config.py:19](../../skills/mcp_tools/get_config.py#L19)

```python
TOOL
```

---
