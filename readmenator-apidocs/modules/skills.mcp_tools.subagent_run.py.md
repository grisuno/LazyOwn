# `skills.mcp_tools.subagent_run`

> Source: [skills/mcp_tools/subagent_run.py:1](../../skills/mcp_tools/subagent_run.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_subagent_run`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_subagent_run_py__handle(["handle"])
    n_modules_mcp_agent_bridge_py__start_agent["mcp_agent_bridge.start_agent"]
    n_skills_lazyown_session_py__SessionTranscript___init__["lazyown_session.SessionTranscript.__init__"]
    n_skills_lazyown_session_py__SessionTranscript_append["lazyown_session.SessionTranscript.append"]
    n_skills_mcp_tools_subagent_run_py__handle -.-> n_modules_mcp_agent_bridge_py__start_agent
    n_skills_mcp_tools_subagent_run_py__handle -.-> n_skills_lazyown_session_py__SessionTranscript___init__
    n_skills_mcp_tools_subagent_run_py__handle -.-> n_skills_lazyown_session_py__SessionTranscript_append
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/subagent_run.py:45](../../skills/mcp_tools/subagent_run.py#L45)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_subagent_run MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`start_agent`](modules.mcp_agent_bridge.py.md#start_agent), [`SessionTranscript.__init__`](skills.lazyown_session.py.md#sessiontranscript-__init__), [`SessionTranscript.append`](skills.lazyown_session.py.md#sessiontranscript-append)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/subagent_run.py:13](../../skills/mcp_tools/subagent_run.py#L13)

```python
TOOL
```

---
