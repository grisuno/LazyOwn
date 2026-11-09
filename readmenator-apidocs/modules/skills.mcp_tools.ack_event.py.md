# `skills.mcp_tools.ack_event`

> Source: [skills/mcp_tools/ack_event.py:1](../../skills/mcp_tools/ack_event.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_ack_event``: mark an event as processed.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_ack_event_py__handle(["handle"])
    n_modules_event_engine_py__ack_event["event_engine.ack_event"]
    n_skills_mcp_tools_ack_event_py__handle -.-> n_modules_event_engine_py__ack_event
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/ack_event.py:28](../../skills/mcp_tools/ack_event.py#L28)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Acknowledge one event by id, reporting whether it was found.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`ack_event`](modules.event_engine.py.md#ack_event)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/ack_event.py:12](../../skills/mcp_tools/ack_event.py#L12)

```python
TOOL
```

---
