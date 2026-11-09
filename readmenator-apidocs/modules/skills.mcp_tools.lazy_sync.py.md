# `skills.mcp_tools.lazy_sync`

> Source: [skills/mcp_tools/lazy_sync.py:1](../../skills/mcp_tools/lazy_sync.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_sync``: sync all lazy-bridge sources.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_sync.py:19](../../skills/mcp_tools/lazy_sync.py#L19)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Run a full lazy-bridge sync and return its result as JSON.

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

`constant` | [skills/mcp_tools/lazy_sync.py:12](../../skills/mcp_tools/lazy_sync.py#L12)

```python
TOOL
```

---
