# `skills.mcp_tools.run_command_async`

> Source: [skills/mcp_tools/run_command_async.py:1](../../skills/mcp_tools/run_command_async.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_run_command_async`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_run_command_async_py__handle(["handle"])
    n_skills_lazyown_mcp_helpers_py__needs_confirmation["lazyown_mcp_helpers.needs_confirmation"]
    n_skills_mcp_tools_run_command_async_py__handle -.-> n_skills_lazyown_mcp_helpers_py__needs_confirmation
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/run_command_async.py:39](../../skills/mcp_tools/run_command_async.py#L39)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_run_command_async MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`needs_confirmation`](skills.lazyown_mcp_helpers.py.md#needs_confirmation)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/run_command_async.py:13](../../skills/mcp_tools/run_command_async.py#L13)

```python
TOOL
```

---
