# `skills.mcp_tools.get_llm_budget`

> Source: [skills/mcp_tools/get_llm_budget.py:1](../../skills/mcp_tools/get_llm_budget.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_get_llm_budget``: read the LLM cost budget status.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_get_llm_budget_py__handle(["handle"])
    n_core_llm_budget_py__read_budget_status["llm_budget.read_budget_status"]
    n_skills_mcp_tools_get_llm_budget_py__handle -.-> n_core_llm_budget_py__read_budget_status
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/get_llm_budget.py:26](../../skills/mcp_tools/get_llm_budget.py#L26)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return the LLM budget status, or an unavailable marker on failure.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`read_budget_status`](core.llm_budget.py.md#read_budget_status)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/get_llm_budget.py:12](../../skills/mcp_tools/get_llm_budget.py#L12)

```python
TOOL
```

---
