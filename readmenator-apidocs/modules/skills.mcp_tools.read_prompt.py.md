# `skills.mcp_tools.read_prompt`

> Source: [skills/mcp_tools/read_prompt.py:1](../../skills/mcp_tools/read_prompt.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_read_prompt`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/read_prompt.py:41](../../skills/mcp_tools/read_prompt.py#L41)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_read_prompt MCP tool.

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

`constant` | [skills/mcp_tools/read_prompt.py:11](../../skills/mcp_tools/read_prompt.py#L11)

```python
TOOL
```

---
