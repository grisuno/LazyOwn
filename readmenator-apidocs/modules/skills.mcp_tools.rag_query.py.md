# `skills.mcp_tools.rag_query`

> Source: [skills/mcp_tools/rag_query.py:1](../../skills/mcp_tools/rag_query.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_rag_query`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/rag_query.py:39](../../skills/mcp_tools/rag_query.py#L39)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_rag_query MCP tool.

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

`constant` | [skills/mcp_tools/rag_query.py:12](../../skills/mcp_tools/rag_query.py#L12)

```python
TOOL
```

---
