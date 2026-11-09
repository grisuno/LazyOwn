# `skills.mcp_tools.lazy_status`

> Source: [skills/mcp_tools/lazy_status.py:1](../../skills/mcp_tools/lazy_status.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_status``: report lazy-bridge status.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_status.py:19](../../skills/mcp_tools/lazy_status.py#L19)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return the lazy-bridge status snapshot as JSON.

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

`constant` | [skills/mcp_tools/lazy_status.py:12](../../skills/mcp_tools/lazy_status.py#L12)

```python
TOOL
```

---
