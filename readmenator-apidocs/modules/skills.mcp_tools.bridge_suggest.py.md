# `skills.mcp_tools.bridge_suggest`

> Source: [skills/mcp_tools/bridge_suggest.py:1](../../skills/mcp_tools/bridge_suggest.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_bridge_suggest`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_bridge_suggest_py__handle(["handle"])
    n_modules_world_model_py__WorldModel___init__["world_model.WorldModel.__init__"]
    n_modules_world_model_py__WorldModel_snapshot["world_model.WorldModel.snapshot"]
    n_skills_mcp_tools_bridge_suggest_py__handle -.-> n_modules_world_model_py__WorldModel___init__
    n_skills_mcp_tools_bridge_suggest_py__handle -.-> n_modules_world_model_py__WorldModel_snapshot
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/bridge_suggest.py:104](../../skills/mcp_tools/bridge_suggest.py#L104)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_bridge_suggest MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`WorldModel.__init__`](modules.world_model.py.md#worldmodel-__init__), [`WorldModel.snapshot`](modules.world_model.py.md#worldmodel-snapshot)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/bridge_suggest.py:11](../../skills/mcp_tools/bridge_suggest.py#L11)

```python
TOOL
```

---
