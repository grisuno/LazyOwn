# `skills.mcp_tools.winbox_snapshot`

> Source: [skills/mcp_tools/winbox_snapshot.py:1](../../skills/mcp_tools/winbox_snapshot.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_winbox_snapshot``: manage WinBox lab snapshots.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_winbox_snapshot_py__handle(["handle"])
    n_modules_winbox_gym_py__run_cli["winbox_gym.run_cli"]
    n_skills_mcp_tools_winbox_snapshot_py__handle -.-> n_modules_winbox_gym_py__run_cli
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/winbox_snapshot.py:29](../../skills/mcp_tools/winbox_snapshot.py#L29)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Manage WinBox snapshots: list, create or restore a rollback point.

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

`constant` | [skills/mcp_tools/winbox_snapshot.py:12](../../skills/mcp_tools/winbox_snapshot.py#L12)

```python
TOOL
```

---
