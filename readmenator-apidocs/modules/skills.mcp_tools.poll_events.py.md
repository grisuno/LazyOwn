# `skills.mcp_tools.poll_events`

> Source: [skills/mcp_tools/poll_events.py:1](../../skills/mcp_tools/poll_events.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_poll_events`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_poll_events_py__handle(["handle"])
    n_modules_event_engine_py__read_events["event_engine.read_events"]
    n_skills_mcp_tools_poll_events_py__handle -.-> n_modules_event_engine_py__read_events
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/poll_events.py:39](../../skills/mcp_tools/poll_events.py#L39)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_poll_events MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`read_events`](modules.event_engine.py.md#read_events)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/poll_events.py:12](../../skills/mcp_tools/poll_events.py#L12)

```python
TOOL
```

---
