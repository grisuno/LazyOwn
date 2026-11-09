# `skills.mcp_tools.misp_export`

> Source: [skills/mcp_tools/misp_export.py:1](../../skills/mcp_tools/misp_export.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_misp_export`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/misp_export.py:38](../../skills/mcp_tools/misp_export.py#L38)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_misp_export MCP tool.

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

`constant` | [skills/mcp_tools/misp_export.py:12](../../skills/mcp_tools/misp_export.py#L12)

```python
TOOL
```

---
