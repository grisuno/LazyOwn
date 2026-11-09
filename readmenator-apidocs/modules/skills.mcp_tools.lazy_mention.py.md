# `skills.mcp_tools.lazy_mention`

> Source: [skills/mcp_tools/lazy_mention.py:1](../../skills/mcp_tools/lazy_mention.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_mention``: search mention sources, paginated.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_mention.py:28](../../skills/mcp_tools/lazy_mention.py#L28)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return one page of mention items plus the next cursor as JSON.

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

`constant` | [skills/mcp_tools/lazy_mention.py:13](../../skills/mcp_tools/lazy_mention.py#L13)

```python
TOOL
```

---
