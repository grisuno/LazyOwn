# `skills.mcp_tools.lazy_compact`

> Source: [skills/mcp_tools/lazy_compact.py:1](../../skills/mcp_tools/lazy_compact.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_compact``: manage cold-compaction digests.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_compact.py:35](../../skills/mcp_tools/lazy_compact.py#L35)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Dispatch the compaction action and return its result as JSON.

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

`constant` | [skills/mcp_tools/lazy_compact.py:15](../../skills/mcp_tools/lazy_compact.py#L15)

```python
TOOL
```

---
