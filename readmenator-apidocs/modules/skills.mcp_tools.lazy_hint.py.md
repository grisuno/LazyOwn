# `skills.mcp_tools.lazy_hint`

> Source: [skills/mcp_tools/lazy_hint.py:1](../../skills/mcp_tools/lazy_hint.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_hint``: add a hint node to a task.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_lazy_hint_py__handle(["handle"])
    n_modules_lazy_engine_py__LazyEngine["lazy_engine.LazyEngine"]
    n_modules_lazy_loop_py__LazyLoopEngine_add_hint["lazy_loop.LazyLoopEngine.add_hint"]
    n_skills_mcp_tools_lazy_hint_py__handle -.-> n_modules_lazy_engine_py__LazyEngine
    n_skills_mcp_tools_lazy_hint_py__handle -.-> n_modules_lazy_loop_py__LazyLoopEngine_add_hint
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_hint.py:26](../../skills/mcp_tools/lazy_hint.py#L26)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Create a hint node and return its record as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`LazyEngine`](modules.lazy_engine.py.md#lazyengine), [`LazyLoopEngine.add_hint`](modules.lazy_loop.py.md#lazyloopengine-add_hint)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/lazy_hint.py:12](../../skills/mcp_tools/lazy_hint.py#L12)

```python
TOOL
```

---
