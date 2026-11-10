# `skills.mcp_tools.session_resume`

> Source: [skills/mcp_tools/session_resume.py:1](../../skills/mcp_tools/session_resume.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_session_resume`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_session_resume_py__handle(["handle"])
    n_skills_lazyown_session_py__SessionTranscript___init__["lazyown_session.SessionTranscript.__init__"]
    n_skills_lazyown_session_py__SessionTranscript_count["lazyown_session.SessionTranscript.count"]
    n_skills_lazyown_session_py__SessionTranscript_get_recent["lazyown_session.SessionTranscript.get_recent"]
    n_skills_mcp_tools_session_resume_py__handle -.-> n_skills_lazyown_session_py__SessionTranscript___init__
    n_skills_mcp_tools_session_resume_py__handle -.-> n_skills_lazyown_session_py__SessionTranscript_count
    n_skills_mcp_tools_session_resume_py__handle -.-> n_skills_lazyown_session_py__SessionTranscript_get_recent
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/session_resume.py:37](../../skills/mcp_tools/session_resume.py#L37)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_session_resume MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`SessionTranscript.__init__`](skills.lazyown_session.py.md#sessiontranscript-__init__), [`SessionTranscript.count`](skills.lazyown_session.py.md#sessiontranscript-count), [`SessionTranscript.get_recent`](skills.lazyown_session.py.md#sessiontranscript-get_recent)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/session_resume.py:11](../../skills/mcp_tools/session_resume.py#L11)

```python
TOOL
```

---
