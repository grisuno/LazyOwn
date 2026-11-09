# `skills.mcp_tools.auto_loop`

> Source: [skills/mcp_tools/auto_loop.py:1](../../skills/mcp_tools/auto_loop.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_auto_loop`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_auto_loop_py__handle(["handle"])
    n_modules_lazy_runner_py__bind_target_authority["lazy_runner.bind_target_authority"]
    n_skills_mcp_tools_auto_loop_py__handle -.-> n_modules_lazy_runner_py__bind_target_authority
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/auto_loop.py:48](../../skills/mcp_tools/auto_loop.py#L48)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_auto_loop MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`bind_target_authority`](modules.lazy_runner.py.md#bind_target_authority)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/auto_loop.py:10](../../skills/mcp_tools/auto_loop.py#L10)

```python
TOOL
```

---
