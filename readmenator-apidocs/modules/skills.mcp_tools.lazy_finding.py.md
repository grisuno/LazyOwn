# `skills.mcp_tools.lazy_finding`

> Source: [skills/mcp_tools/lazy_finding.py:1](../../skills/mcp_tools/lazy_finding.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lazy_finding``: report a finding into the loop engine.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_lazy_finding_py__handle(["handle"])
    n_modules_lazy_engine_py__LazyEngine["lazy_engine.LazyEngine"]
    n_modules_lazy_loop_py__ActivityLog___init__["lazy_loop.ActivityLog.__init__"]
    n_modules_lazy_loop_py__ExplorationGraph___init__["lazy_loop.ExplorationGraph.__init__"]
    n_modules_lazy_loop_py__FindingService___init__["lazy_loop.FindingService.__init__"]
    n_modules_lazy_loop_py__FindingService_report["lazy_loop.FindingService.report"]
    n_skills_mcp_tools_lazy_finding_py__handle -.-> n_modules_lazy_engine_py__LazyEngine
    n_skills_mcp_tools_lazy_finding_py__handle -.-> n_modules_lazy_loop_py__ActivityLog___init__
    n_skills_mcp_tools_lazy_finding_py__handle -.-> n_modules_lazy_loop_py__ExplorationGraph___init__
    n_skills_mcp_tools_lazy_finding_py__handle -.-> n_modules_lazy_loop_py__FindingService___init__
    n_skills_mcp_tools_lazy_finding_py__handle -.-> n_modules_lazy_loop_py__FindingService_report
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lazy_finding.py:34](../../skills/mcp_tools/lazy_finding.py#L34)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Persist a finding node and return its record as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`LazyEngine`](modules.lazy_engine.py.md#lazyengine), [`ActivityLog.__init__`](modules.lazy_loop.py.md#activitylog-__init__), [`ExplorationGraph.__init__`](modules.lazy_loop.py.md#explorationgraph-__init__), [`FindingService.__init__`](modules.lazy_loop.py.md#findingservice-__init__), [`FindingService.report`](modules.lazy_loop.py.md#findingservice-report)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/lazy_finding.py:16](../../skills/mcp_tools/lazy_finding.py#L16)

```python
TOOL
```

---
