# `skills.mcp_tools.lazy_trace`

> Source: [skills/mcp_tools/lazy_trace.py:1](../../skills/mcp_tools/lazy_trace.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_trace``: search a task activity log.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_lazy_trace_py__handle(["handle"])
    n_modules_lazy_loop_py__ActivityLog___init__["lazy_loop.ActivityLog.__init__"]
    n_modules_lazy_loop_py__ActivityLog_search_all["lazy_loop.ActivityLog.search_all"]
    n_skills_mcp_tools_lazy_trace_py__handle -.-> n_modules_lazy_loop_py__ActivityLog___init__
    n_skills_mcp_tools_lazy_trace_py__handle -.-> n_modules_lazy_loop_py__ActivityLog_search_all
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_trace.py:29](../../skills/mcp_tools/lazy_trace.py#L29)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return up to the hit cap of matching activity-log entries as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`ActivityLog.__init__`](modules.lazy_loop.py.md#activitylog-__init__), [`ActivityLog.search_all`](modules.lazy_loop.py.md#activitylog-search_all)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/lazy_trace.py:15](../../skills/mcp_tools/lazy_trace.py#L15)

```python
TOOL
```

---
