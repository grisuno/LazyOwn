# `skills.mcp_tools.lazy_workspace`

> Source: [skills/mcp_tools/lazy_workspace.py:1](../../skills/mcp_tools/lazy_workspace.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_workspace``: list/read/write workspace files.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_workspace.py:30](../../skills/mcp_tools/lazy_workspace.py#L30)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Dispatch the workspace action and return its result as JSON.

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

`constant` | [skills/mcp_tools/lazy_workspace.py:13](../../skills/mcp_tools/lazy_workspace.py#L13)

```python
TOOL
```

---
