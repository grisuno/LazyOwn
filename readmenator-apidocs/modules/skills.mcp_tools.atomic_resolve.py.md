# `skills.mcp_tools.atomic_resolve`

> Source: [skills/mcp_tools/atomic_resolve.py:1](../../skills/mcp_tools/atomic_resolve.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_atomic_resolve`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_atomic_resolve_py__handle(["handle"])
    n_modules_atomic_resolver_py__get_resolver["atomic_resolver.get_resolver"]
    n_skills_mcp_tools_atomic_resolve_py__handle -.-> n_modules_atomic_resolver_py__get_resolver
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/atomic_resolve.py:49](../../skills/mcp_tools/atomic_resolve.py#L49)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_atomic_resolve MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`get_resolver`](modules.atomic_resolver.py.md#get_resolver)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/atomic_resolve.py:11](../../skills/mcp_tools/atomic_resolve.py#L11)

```python
TOOL
```

---
