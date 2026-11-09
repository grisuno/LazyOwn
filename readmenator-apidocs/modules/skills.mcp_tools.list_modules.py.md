# `skills.mcp_tools.list_modules`

> Source: [skills/mcp_tools/list_modules.py:1](../../skills/mcp_tools/list_modules.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_list_modules``: list modules and scripts in modules/.

Migrated out of the ``lazyown_mcp`` god-file. Demonstrates a tool that
needs a repo-relative resource: it takes the repository root from the
injected `mcp_tools._context.MCPContext` rather than importing the
runtime.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_list_modules_py__handle(["handle"])
    n_modules_module_registry_py__ModuleRegistry_get_instance["module_registry.ModuleRegistry.get_instance"]
    n_skills_mcp_tools_list_modules_py__handle -.-> n_modules_module_registry_py__ModuleRegistry_get_instance
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/list_modules.py:27](../../skills/mcp_tools/list_modules.py#L27)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return discovered modules as JSON, optionally filtered by type.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  | May carry a ``type`` key to filter by module type. |
| `tool_name` | `str` |  | The dispatched tool name, used for the text envelope. |
| `ctx` | `MCPContext` |  | Injected runtime helpers, including the repository root. |

**Returns:** `list` - A one-element ``TextContent`` list holding the module summaries.

*Calls:* [`ModuleRegistry.get_instance`](modules.module_registry.py.md#moduleregistry-get_instance)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/list_modules.py:20](../../skills/mcp_tools/list_modules.py#L20)

```python
TOOL
```

---
