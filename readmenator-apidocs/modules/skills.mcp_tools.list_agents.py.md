# `skills.mcp_tools.list_agents`

> Source: [skills/mcp_tools/list_agents.py:1](../../skills/mcp_tools/list_agents.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_list_agents`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_list_agents_py__handle(["handle"])
    n_modules_mcp_agent_bridge_py__list_agents["mcp_agent_bridge.list_agents"]
    n_skills_mcp_tools_list_agents_py__handle -.-> n_modules_mcp_agent_bridge_py__list_agents
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/list_agents.py:28](../../skills/mcp_tools/list_agents.py#L28)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_list_agents MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`list_agents`](modules.mcp_agent_bridge.py.md#list_agents)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/list_agents.py:12](../../skills/mcp_tools/list_agents.py#L12)

```python
TOOL
```

---
