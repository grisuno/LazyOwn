# `skills.mcp_tools.eval_quality`

> Source: [skills/mcp_tools/eval_quality.py:1](../../skills/mcp_tools/eval_quality.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_eval_quality`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_eval_quality_py__handle(["handle"])
    n_modules_llm_evaluator_py__get_evaluator["llm_evaluator.get_evaluator"]
    n_skills_mcp_tools_eval_quality_py__handle -.-> n_modules_llm_evaluator_py__get_evaluator
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/eval_quality.py:38](../../skills/mcp_tools/eval_quality.py#L38)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_eval_quality MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`get_evaluator`](modules.llm_evaluator.py.md#get_evaluator)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/eval_quality.py:12](../../skills/mcp_tools/eval_quality.py#L12)

```python
TOOL
```

---
