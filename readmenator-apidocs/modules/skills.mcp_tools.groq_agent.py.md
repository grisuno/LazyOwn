# `skills.mcp_tools.groq_agent`

> Source: [skills/mcp_tools/groq_agent.py:1](../../skills/mcp_tools/groq_agent.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_groq_agent`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/groq_agent.py:70](../../skills/mcp_tools/groq_agent.py#L70)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_groq_agent MCP tool.

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

`constant` | [skills/mcp_tools/groq_agent.py:13](../../skills/mcp_tools/groq_agent.py#L13)

```python
TOOL
```

---
