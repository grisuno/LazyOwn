# `skills.mcp_tools.lazy_addon`

> Source: [skills/mcp_tools/lazy_addon.py:1](../../skills/mcp_tools/lazy_addon.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_addon``: list or match lazyaddon triggers.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_addon.py:27](../../skills/mcp_tools/lazy_addon.py#L27)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

List addon triggers or return matches for a service as JSON.

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

`constant` | [skills/mcp_tools/lazy_addon.py:13](../../skills/mcp_tools/lazy_addon.py#L13)

```python
TOOL
```

---
