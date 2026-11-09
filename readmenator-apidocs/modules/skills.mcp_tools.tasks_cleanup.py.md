# `skills.mcp_tools.tasks_cleanup`

> Source: [skills/mcp_tools/tasks_cleanup.py:1](../../skills/mcp_tools/tasks_cleanup.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_tasks_cleanup`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_tasks_cleanup_py__handle(["handle"])
    n_skills_lazyown_mcp_helpers_py__audit_tasks["lazyown_mcp_helpers.audit_tasks"]
    n_skills_mcp_tools_tasks_cleanup_py__handle -.-> n_skills_lazyown_mcp_helpers_py__audit_tasks
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/tasks_cleanup.py:37](../../skills/mcp_tools/tasks_cleanup.py#L37)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_tasks_cleanup MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`audit_tasks`](skills.lazyown_mcp_helpers.py.md#audit_tasks)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/tasks_cleanup.py:12](../../skills/mcp_tools/tasks_cleanup.py#L12)

```python
TOOL
```

---
