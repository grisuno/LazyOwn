# `skills.mcp_tools.lazy_board`

> Source: [skills/mcp_tools/lazy_board.py:1](../../skills/mcp_tools/lazy_board.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_board``: paginated broadcast board view.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_lazy_board_py__handle(["handle"])
    n_modules_lazy_engine_py__LazyEngine["lazy_engine.LazyEngine"]
    n_modules_lazy_loop_py__LazyLoopEngine_broadcast["lazy_loop.LazyLoopEngine.broadcast"]
    n_skills_mcp_tools_lazy_board_py__handle -.-> n_modules_lazy_engine_py__LazyEngine
    n_skills_mcp_tools_lazy_board_py__handle -.-> n_modules_lazy_loop_py__LazyLoopEngine_broadcast
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_board.py:36](../../skills/mcp_tools/lazy_board.py#L36)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return one page of the broadcast board as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`LazyEngine`](modules.lazy_engine.py.md#lazyengine), [`LazyLoopEngine.broadcast`](modules.lazy_loop.py.md#lazyloopengine-broadcast)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/lazy_board.py:15](../../skills/mcp_tools/lazy_board.py#L15)

```python
TOOL
```

---
