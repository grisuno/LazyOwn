# `skills.mcp_tools.llm_ask`

> Source: [skills/mcp_tools/llm_ask.py:1](../../skills/mcp_tools/llm_ask.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_llm_ask`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/llm_ask.py:67](../../skills/mcp_tools/llm_ask.py#L67)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_llm_ask MCP tool.

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

`constant` | [skills/mcp_tools/llm_ask.py:13](../../skills/mcp_tools/llm_ask.py#L13)

```python
TOOL
```

---
