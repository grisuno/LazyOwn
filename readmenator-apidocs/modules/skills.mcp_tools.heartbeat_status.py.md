# `skills.mcp_tools.heartbeat_status`

> Source: [skills/mcp_tools/heartbeat_status.py:1](../../skills/mcp_tools/heartbeat_status.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_heartbeat_status`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_heartbeat_status_py__handle(["handle"])
    n_modules_event_engine_py__load_rules["event_engine.load_rules"]
    n_skills_mcp_tools_heartbeat_status_py__handle -.-> n_modules_event_engine_py__load_rules
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/heartbeat_status.py:20](../../skills/mcp_tools/heartbeat_status.py#L20)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_heartbeat_status MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`load_rules`](modules.event_engine.py.md#load_rules)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/heartbeat_status.py:13](../../skills/mcp_tools/heartbeat_status.py#L13)

```python
TOOL
```

---
