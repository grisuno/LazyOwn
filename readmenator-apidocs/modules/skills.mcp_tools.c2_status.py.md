# `skills.mcp_tools.c2_status`

> Source: [skills/mcp_tools/c2_status.py:1](../../skills/mcp_tools/c2_status.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_c2_status``: check C2 reachability and dashboard data.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/c2_status.py:20](../../skills/mcp_tools/c2_status.py#L20)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Query the C2 dashboard endpoint and return its JSON.

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

`constant` | [skills/mcp_tools/c2_status.py:13](../../skills/mcp_tools/c2_status.py#L13)

```python
TOOL
```

---
