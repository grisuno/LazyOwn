# `skills.mcp_tools.session_diff`

> Source: [skills/mcp_tools/session_diff.py:1](../../skills/mcp_tools/session_diff.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_session_diff`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_session_diff_py__handle(["handle"])
    n_skills_lazyown_mcp_helpers_py__diff_snapshot["lazyown_mcp_helpers.diff_snapshot"]
    n_skills_lazyown_mcp_helpers_py__take_snapshot["lazyown_mcp_helpers.take_snapshot"]
    n_skills_mcp_tools_session_diff_py__handle -.-> n_skills_lazyown_mcp_helpers_py__diff_snapshot
    n_skills_mcp_tools_session_diff_py__handle -.-> n_skills_lazyown_mcp_helpers_py__take_snapshot
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/session_diff.py:32](../../skills/mcp_tools/session_diff.py#L32)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_session_diff MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`diff_snapshot`](skills.lazyown_mcp_helpers.py.md#diff_snapshot), [`take_snapshot`](skills.lazyown_mcp_helpers.py.md#take_snapshot)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/session_diff.py:12](../../skills/mcp_tools/session_diff.py#L12)

```python
TOOL
```

---
