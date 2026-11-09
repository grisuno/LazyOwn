# `skills.mcp_tools.target_context`

> Source: [skills/mcp_tools/target_context.py:1](../../skills/mcp_tools/target_context.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_target_context`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_target_context_py__handle(["handle"])
    n_skills_lazyown_mcp_helpers_py__build_target_context["lazyown_mcp_helpers.build_target_context"]
    n_skills_mcp_tools_target_context_py__handle -.-> n_skills_lazyown_mcp_helpers_py__build_target_context
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/target_context.py:37](../../skills/mcp_tools/target_context.py#L37)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_target_context MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`build_target_context`](skills.lazyown_mcp_helpers.py.md#build_target_context)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/target_context.py:12](../../skills/mcp_tools/target_context.py#L12)

```python
TOOL
```

---
