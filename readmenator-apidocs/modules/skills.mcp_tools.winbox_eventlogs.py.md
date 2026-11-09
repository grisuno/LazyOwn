# `skills.mcp_tools.winbox_eventlogs`

> Source: [skills/mcp_tools/winbox_eventlogs.py:1](../../skills/mcp_tools/winbox_eventlogs.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_winbox_eventlogs``: query guest Windows event logs.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_winbox_eventlogs_py__handle(["handle"])
    n_modules_winbox_gym_py__run_cli["winbox_gym.run_cli"]
    n_skills_mcp_tools_winbox_eventlogs_py__handle -.-> n_modules_winbox_gym_py__run_cli
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/winbox_eventlogs.py:36](../../skills/mcp_tools/winbox_eventlogs.py#L36)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Query Windows event logs inside the WinBox guest.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`run_cli`](modules.winbox_gym.py.md#run_cli)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/winbox_eventlogs.py:14](../../skills/mcp_tools/winbox_eventlogs.py#L14)

```python
TOOL
```

---
