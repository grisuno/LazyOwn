# `skills.mcp_tools.winbox_status`

> Source: [skills/mcp_tools/winbox_status.py:1](../../skills/mcp_tools/winbox_status.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_winbox_status``: report WinBox lab readiness.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_winbox_status_py__handle(["handle"])
    n_modules_winbox_gym_py__attack_readiness["winbox_gym.attack_readiness"]
    n_skills_mcp_tools_winbox_status_py__handle -.-> n_modules_winbox_gym_py__attack_readiness
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/winbox_status.py:22](../../skills/mcp_tools/winbox_status.py#L22)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Report WinBox lab readiness, VM state and autonomous-loop attackability.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`attack_readiness`](modules.winbox_gym.py.md#attack_readiness)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/winbox_status.py:12](../../skills/mcp_tools/winbox_status.py#L12)

```python
TOOL
```

---
