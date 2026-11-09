# `skills.mcp_tools.playbook_generate`

> Source: [skills/mcp_tools/playbook_generate.py:1](../../skills/mcp_tools/playbook_generate.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_playbook_generate`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_playbook_generate_py__handle(["handle"])
    n_modules_playbook_engine_py__PlaybookEngine___init__["playbook_engine.PlaybookEngine.__init__"]
    n_modules_playbook_engine_py__PlaybookEngine_derive["playbook_engine.PlaybookEngine.derive"]
    n_modules_playbook_engine_py__PlaybookEngine_save["playbook_engine.PlaybookEngine.save"]
    n_skills_mcp_tools_playbook_generate_py__handle -.-> n_modules_playbook_engine_py__PlaybookEngine___init__
    n_skills_mcp_tools_playbook_generate_py__handle -.-> n_modules_playbook_engine_py__PlaybookEngine_derive
    n_skills_mcp_tools_playbook_generate_py__handle -.-> n_modules_playbook_engine_py__PlaybookEngine_save
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/playbook_generate.py:52](../../skills/mcp_tools/playbook_generate.py#L52)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_playbook_generate MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`PlaybookEngine.__init__`](modules.playbook_engine.py.md#playbookengine-__init__), [`PlaybookEngine.derive`](modules.playbook_engine.py.md#playbookengine-derive), [`PlaybookEngine.save`](modules.playbook_engine.py.md#playbookengine-save)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/playbook_generate.py:12](../../skills/mcp_tools/playbook_generate.py#L12)

```python
TOOL
```

---
