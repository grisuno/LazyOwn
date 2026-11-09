# `skills.mcp_tools.rea`

> Source: [skills/mcp_tools/rea.py:1](../../skills/mcp_tools/rea.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_rea``: reverse-engineer a local artifact via the REA CLI.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/rea.py:95](../../skills/mcp_tools/rea.py#L95)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Run one REA CLI action against a local artifact and return a JSON envelope.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  | action, target, address, query, provider, timeout. |
| `tool_name` | `str` |  | Registered tool name used for the response envelope. |
| `ctx` | `MCPContext` |  | Injected runtime helpers. |

**Returns:** `list` - Single TextContent holding a JSON envelope with the REA result.

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/rea.py:41](../../skills/mcp_tools/rea.py#L41)

```python
TOOL
```

---
