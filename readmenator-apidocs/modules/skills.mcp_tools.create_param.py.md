# `skills.mcp_tools.create_param`

> Source: [skills/mcp_tools/create_param.py:1](../../skills/mcp_tools/create_param.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_create_param`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_create_param_py__handle(["handle"])
    n_core_param_registry_py__create_param["param_registry.create_param"]
    n_skills_mcp_tools_create_param_py__handle -.-> n_core_param_registry_py__create_param
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/create_param.py:47](../../skills/mcp_tools/create_param.py#L47)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_create_param MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`create_param`](core.param_registry.py.md#create_param)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/create_param.py:10](../../skills/mcp_tools/create_param.py#L10)

```python
TOOL
```

---
