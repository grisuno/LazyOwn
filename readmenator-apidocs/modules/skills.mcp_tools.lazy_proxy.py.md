# `skills.mcp_tools.lazy_proxy`

> Source: [skills/mcp_tools/lazy_proxy.py:1](../../skills/mcp_tools/lazy_proxy.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_proxy``: control the lazy-engine proxy.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_lazy_proxy_py__handle(["handle"])
    n_modules_lazy_engine_py__LazyEngine["lazy_engine.LazyEngine"]
    n_modules_lazy_loop_py__LazyLoopEngine_proxy_env["lazy_loop.LazyLoopEngine.proxy_env"]
    n_modules_lazy_loop_py__LazyLoopEngine_proxy_start["lazy_loop.LazyLoopEngine.proxy_start"]
    n_modules_lazy_loop_py__LazyLoopEngine_proxy_status["lazy_loop.LazyLoopEngine.proxy_status"]
    n_skills_mcp_tools_lazy_proxy_py__handle -.-> n_modules_lazy_engine_py__LazyEngine
    n_skills_mcp_tools_lazy_proxy_py__handle -.-> n_modules_lazy_loop_py__LazyLoopEngine_proxy_env
    n_skills_mcp_tools_lazy_proxy_py__handle -.-> n_modules_lazy_loop_py__LazyLoopEngine_proxy_start
    n_skills_mcp_tools_lazy_proxy_py__handle -.-> n_modules_lazy_loop_py__LazyLoopEngine_proxy_status
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_proxy.py:39](../../skills/mcp_tools/lazy_proxy.py#L39)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Dispatch the proxy action and return its status as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`LazyEngine`](modules.lazy_engine.py.md#lazyengine), [`LazyLoopEngine.proxy_env`](modules.lazy_loop.py.md#lazyloopengine-proxy_env), [`LazyLoopEngine.proxy_start`](modules.lazy_loop.py.md#lazyloopengine-proxy_start), [`LazyLoopEngine.proxy_status`](modules.lazy_loop.py.md#lazyloopengine-proxy_status)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/lazy_proxy.py:15](../../skills/mcp_tools/lazy_proxy.py#L15)

```python
TOOL
```

---
