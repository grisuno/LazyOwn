# `skills.mcp_tools.recommend_next`

> Source: [skills/mcp_tools/recommend_next.py:1](../../skills/mcp_tools/recommend_next.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_recommend_next`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_recommend_next_py__handle(["handle"])
    n_cli_recommendation_signals_py__build_context["recommendation_signals.build_context"]
    n_cli_recommendation_signals_py__build_default_engine["recommendation_signals.build_default_engine"]
    n_skills_mcp_tools_recommend_next_py__handle -.-> n_cli_recommendation_signals_py__build_context
    n_skills_mcp_tools_recommend_next_py__handle -.-> n_cli_recommendation_signals_py__build_default_engine
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/recommend_next.py:25](../../skills/mcp_tools/recommend_next.py#L25)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_recommend_next MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`build_context`](cli.recommendation_signals.py.md#build_context), [`build_default_engine`](cli.recommendation_signals.py.md#build_default_engine)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/recommend_next.py:13](../../skills/mcp_tools/recommend_next.py#L13)

```python
TOOL
```

---
