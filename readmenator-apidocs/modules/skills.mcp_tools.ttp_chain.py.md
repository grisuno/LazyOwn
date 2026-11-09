# `skills.mcp_tools.ttp_chain`

> Source: [skills/mcp_tools/ttp_chain.py:1](../../skills/mcp_tools/ttp_chain.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_ttp_chain`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_ttp_chain_py__handle(["handle"])
    n_modules_atomic_resolver_py__get_resolver["atomic_resolver.get_resolver"]
    n_modules_ttpscope_bridge_py__do_chain["ttpscope_bridge.do_chain"]
    n_skills_mcp_tools_ttp_chain_py__handle -.-> n_modules_atomic_resolver_py__get_resolver
    n_skills_mcp_tools_ttp_chain_py__handle -.-> n_modules_ttpscope_bridge_py__do_chain
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/ttp_chain.py:47](../../skills/mcp_tools/ttp_chain.py#L47)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_ttp_chain MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`get_resolver`](modules.atomic_resolver.py.md#get_resolver), [`do_chain`](modules.ttpscope_bridge.py.md#do_chain)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/ttp_chain.py:12](../../skills/mcp_tools/ttp_chain.py#L12)

```python
TOOL
```

---
