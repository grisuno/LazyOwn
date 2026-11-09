# `skills.mcp_tools.collab_publish`

> Source: [skills/mcp_tools/collab_publish.py:1](../../skills/mcp_tools/collab_publish.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_collab_publish`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_collab_publish_py__handle(["handle"])
    n_modules_collab_bp_py__publish_event["collab_bp.publish_event"]
    n_skills_mcp_tools_collab_publish_py__handle -.-> n_modules_collab_bp_py__publish_event
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/collab_publish.py:41](../../skills/mcp_tools/collab_publish.py#L41)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_collab_publish MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`publish_event`](modules.collab_bp.py.md#publish_event)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/collab_publish.py:12](../../skills/mcp_tools/collab_publish.py#L12)

```python
TOOL
```

---
