# `skills.mcp_tools.run_agent`

> Source: [skills/mcp_tools/run_agent.py:1](../../skills/mcp_tools/run_agent.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_run_agent`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_run_agent_py__handle(["handle"])
    n_modules_mcp_agent_bridge_py__start_agent["mcp_agent_bridge.start_agent"]
    n_skills_mcp_tools_run_agent_py__handle -.-> n_modules_mcp_agent_bridge_py__start_agent
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/run_agent.py:50](../../skills/mcp_tools/run_agent.py#L50)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_run_agent MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`start_agent`](modules.mcp_agent_bridge.py.md#start_agent)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/run_agent.py:13](../../skills/mcp_tools/run_agent.py#L13)

```python
TOOL
```

---
