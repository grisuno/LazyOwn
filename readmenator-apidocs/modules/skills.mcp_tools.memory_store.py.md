# `skills.mcp_tools.memory_store`

> Source: [skills/mcp_tools/memory_store.py:1](../../skills/mcp_tools/memory_store.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_memory_store`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_memory_store_py__handle(["handle"])
    n_modules_memory_store_py__get_memory_store["memory_store.get_memory_store"]
    n_skills_mcp_tools_memory_store_py__handle -.-> n_modules_memory_store_py__get_memory_store
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/memory_store.py:32](../../skills/mcp_tools/memory_store.py#L32)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_memory_store MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`get_memory_store`](modules.memory_store.py.md#get_memory_store)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/memory_store.py:11](../../skills/mcp_tools/memory_store.py#L11)

```python
TOOL
```

---
