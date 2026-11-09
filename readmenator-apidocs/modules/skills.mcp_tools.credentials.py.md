# `skills.mcp_tools.credentials`

> Source: [skills/mcp_tools/credentials.py:1](../../skills/mcp_tools/credentials.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_credentials``: aggregate captured credentials.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/credentials.py:32](../../skills/mcp_tools/credentials.py#L32)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Collect, dedupe and format credentials from all session sources.

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

`constant` | [skills/mcp_tools/credentials.py:16](../../skills/mcp_tools/credentials.py#L16)

```python
TOOL
```

---
