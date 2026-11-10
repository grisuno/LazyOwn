# `skills.mcp_tools.session_init`

> Source: [skills/mcp_tools/session_init.py:1](../../skills/mcp_tools/session_init.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_session_init`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_session_init_py__handle(["handle"])
    n_modules_killchain_py__KillChain_current_phase["killchain.KillChain.current_phase"]
    n_skills_lazyown_mcp_helpers_py__evidence_freshness["lazyown_mcp_helpers.evidence_freshness"]
    n_skills_lazyown_mcp_helpers_py__take_snapshot["lazyown_mcp_helpers.take_snapshot"]
    n_skills_mcp_tools_session_init_py__handle -.-> n_modules_killchain_py__KillChain_current_phase
    n_skills_mcp_tools_session_init_py__handle -.-> n_skills_lazyown_mcp_helpers_py__evidence_freshness
    n_skills_mcp_tools_session_init_py__handle -.-> n_skills_lazyown_mcp_helpers_py__take_snapshot
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/session_init.py:59](../../skills/mcp_tools/session_init.py#L59)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_session_init MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`KillChain.current_phase`](modules.killchain.py.md#killchain-current_phase), [`evidence_freshness`](skills.lazyown_mcp_helpers.py.md#evidence_freshness), [`take_snapshot`](skills.lazyown_mcp_helpers.py.md#take_snapshot)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/session_init.py:15](../../skills/mcp_tools/session_init.py#L15)

```python
TOOL
```

---
