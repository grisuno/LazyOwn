# `skills.mcp_tools.unified_dashboard`

> Source: [skills/mcp_tools/unified_dashboard.py:1](../../skills/mcp_tools/unified_dashboard.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_unified_dashboard``: combined campaign dashboard.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_unified_dashboard_py__handle(["handle"])
    n_modules_unified_dashboard_py__UnifiedDashboard___init__["unified_dashboard.UnifiedDashboard.__init__"]
    n_modules_unified_dashboard_py__UnifiedDashboard_export_json["unified_dashboard.UnifiedDashboard.export_json"]
    n_modules_unified_dashboard_py__UnifiedDashboard_render_unified["unified_dashboard.UnifiedDashboard.render_unified"]
    n_skills_mcp_tools_unified_dashboard_py__handle -.-> n_modules_unified_dashboard_py__UnifiedDashboard___init__
    n_skills_mcp_tools_unified_dashboard_py__handle -.-> n_modules_unified_dashboard_py__UnifiedDashboard_export_json
    n_skills_mcp_tools_unified_dashboard_py__handle -.-> n_modules_unified_dashboard_py__UnifiedDashboard_render_unified
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/unified_dashboard.py:34](../../skills/mcp_tools/unified_dashboard.py#L34)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Render the unified dashboard as text, or JSON when requested.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`UnifiedDashboard.__init__`](modules.unified_dashboard.py.md#unifieddashboard-__init__), [`UnifiedDashboard.export_json`](modules.unified_dashboard.py.md#unifieddashboard-export_json), [`UnifiedDashboard.render_unified`](modules.unified_dashboard.py.md#unifieddashboard-render_unified)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/unified_dashboard.py:12](../../skills/mcp_tools/unified_dashboard.py#L12)

```python
TOOL
```

---
