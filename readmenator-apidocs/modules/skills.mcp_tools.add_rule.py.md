# `skills.mcp_tools.add_rule`

> Source: [skills/mcp_tools/add_rule.py:1](../../skills/mcp_tools/add_rule.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_add_rule`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_add_rule_py__handle(["handle"])
    n_modules_event_engine_py__add_rule["event_engine.add_rule"]
    n_modules_event_engine_py__load_rules["event_engine.load_rules"]
    n_skills_mcp_tools_add_rule_py__handle -.-> n_modules_event_engine_py__add_rule
    n_skills_mcp_tools_add_rule_py__handle -.-> n_modules_event_engine_py__load_rules
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/add_rule.py:41](../../skills/mcp_tools/add_rule.py#L41)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_add_rule MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`add_rule`](modules.event_engine.py.md#add_rule), [`load_rules`](modules.event_engine.py.md#load_rules)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/add_rule.py:12](../../skills/mcp_tools/add_rule.py#L12)

```python
TOOL
```

---
