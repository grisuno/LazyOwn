# `skills.mcp_tools.get_beacons`

> Source: [skills/mcp_tools/get_beacons.py:1](../../skills/mcp_tools/get_beacons.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_get_beacons``: list connected C2 beacons.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/get_beacons.py:20](../../skills/mcp_tools/get_beacons.py#L20)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Query the C2 for connected clients and return the JSON list.

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

`constant` | [skills/mcp_tools/get_beacons.py:13](../../skills/mcp_tools/get_beacons.py#L13)

```python
TOOL
```

---
