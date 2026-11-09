# `skills.mcp_tools.list_params`

> Source: [skills/mcp_tools/list_params.py:1](../../skills/mcp_tools/list_params.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_list_params`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_list_params_py__handle(["handle"])
    n_core_param_registry_py__list_params["param_registry.list_params"]
    n_skills_mcp_tools_list_params_py__handle -.-> n_core_param_registry_py__list_params
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/list_params.py:36](../../skills/mcp_tools/list_params.py#L36)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_list_params MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`list_params`](core.param_registry.py.md#list_params)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/list_params.py:10](../../skills/mcp_tools/list_params.py#L10)

```python
TOOL
```

---
