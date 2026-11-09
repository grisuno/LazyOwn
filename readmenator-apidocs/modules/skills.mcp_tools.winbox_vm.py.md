# `skills.mcp_tools.winbox_vm`

> Source: [skills/mcp_tools/winbox_vm.py:1](../../skills/mcp_tools/winbox_vm.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_winbox_vm``: drive the WinBox lab VM lifecycle.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_winbox_vm_py__handle(["handle"])
    n_modules_winbox_gym_py__ensure_lab_ready["winbox_gym.ensure_lab_ready"]
    n_modules_winbox_gym_py__run_cli["winbox_gym.run_cli"]
    n_modules_winbox_gym_py__vm_ip["winbox_gym.vm_ip"]
    n_modules_winbox_gym_py__vm_status["winbox_gym.vm_status"]
    n_skills_mcp_tools_winbox_vm_py__handle -.-> n_modules_winbox_gym_py__ensure_lab_ready
    n_skills_mcp_tools_winbox_vm_py__handle -.-> n_modules_winbox_gym_py__run_cli
    n_skills_mcp_tools_winbox_vm_py__handle -.-> n_modules_winbox_gym_py__vm_ip
    n_skills_mcp_tools_winbox_vm_py__handle -.-> n_modules_winbox_gym_py__vm_status
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/winbox_vm.py:36](../../skills/mcp_tools/winbox_vm.py#L36)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Drive WinBox VM lifecycle: bootstrap, up, down, suspend, status.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`ensure_lab_ready`](modules.winbox_gym.py.md#ensure_lab_ready), [`run_cli`](modules.winbox_gym.py.md#run_cli), [`vm_ip`](modules.winbox_gym.py.md#vm_ip), [`vm_status`](modules.winbox_gym.py.md#vm_status)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/winbox_vm.py:12](../../skills/mcp_tools/winbox_vm.py#L12)

```python
TOOL
```

---
