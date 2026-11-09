# `skills.mcp_tools.facts_show`

> Source: [skills/mcp_tools/facts_show.py:1](../../skills/mcp_tools/facts_show.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_facts_show``: show structured facts from the session.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_facts_show_py__handle(["handle"])
    n_skills_lazyown_facts_py__FactStore___init__["lazyown_facts.FactStore.__init__"]
    n_skills_mcp_tools_facts_show_py__handle -.-> n_skills_lazyown_facts_py__FactStore___init__
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/facts_show.py:39](../../skills/mcp_tools/facts_show.py#L39)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return the fact-store summary for a target, optionally re-parsing first.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`FactStore.__init__`](skills.lazyown_facts.py.md#factstore-__init__)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/facts_show.py:12](../../skills/mcp_tools/facts_show.py#L12)

```python
TOOL
```

---
