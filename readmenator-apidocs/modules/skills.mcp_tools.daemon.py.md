# `skills.mcp_tools.daemon`

> Source: [skills/mcp_tools/daemon.py:1](../../skills/mcp_tools/daemon.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_daemon`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/daemon.py:34](../../skills/mcp_tools/daemon.py#L34)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_daemon MCP tool.

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

`constant` | [skills/mcp_tools/daemon.py:13](../../skills/mcp_tools/daemon.py#L13)

```python
TOOL
```

---
