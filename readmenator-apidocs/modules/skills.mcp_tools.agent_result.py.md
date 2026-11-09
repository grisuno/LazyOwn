# `skills.mcp_tools.agent_result`

> Source: [skills/mcp_tools/agent_result.py:1](../../skills/mcp_tools/agent_result.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_agent_result`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_agent_result_py__handle(["handle"])
    n_modules_mcp_agent_bridge_py__get_agent_result["mcp_agent_bridge.get_agent_result"]
    n_skills_mcp_tools_agent_result_py__handle -.-> n_modules_mcp_agent_bridge_py__get_agent_result
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/agent_result.py:31](../../skills/mcp_tools/agent_result.py#L31)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_agent_result MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`get_agent_result`](modules.mcp_agent_bridge.py.md#get_agent_result)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/agent_result.py:12](../../skills/mcp_tools/agent_result.py#L12)

```python
TOOL
```

---
