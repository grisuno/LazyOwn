# `skills.mcp_tools.lazy_delete`

> Source: [skills/mcp_tools/lazy_delete.py:1](../../skills/mcp_tools/lazy_delete.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_delete``: soft/hard delete a task intent.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_delete.py:33](../../skills/mcp_tools/lazy_delete.py#L33)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Delete or preview-delete an intent and return the result as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/lazy_delete.py:13](../../skills/mcp_tools/lazy_delete.py#L13)

```python
TOOL
```

---
