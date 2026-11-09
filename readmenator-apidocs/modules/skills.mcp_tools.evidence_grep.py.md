# `skills.mcp_tools.evidence_grep`

> Source: [skills/mcp_tools/evidence_grep.py:1](../../skills/mcp_tools/evidence_grep.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_evidence_grep`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_evidence_grep_py__handle(["handle"])
    n_skills_lazyown_mcp_helpers_py__evidence_grep["lazyown_mcp_helpers.evidence_grep"]
    n_skills_mcp_tools_evidence_grep_py__handle -.-> n_skills_lazyown_mcp_helpers_py__evidence_grep
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/evidence_grep.py:47](../../skills/mcp_tools/evidence_grep.py#L47)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_evidence_grep MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`evidence_grep`](skills.lazyown_mcp_helpers.py.md#evidence_grep)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/evidence_grep.py:12](../../skills/mcp_tools/evidence_grep.py#L12)

```python
TOOL
```

---
