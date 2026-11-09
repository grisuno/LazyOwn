# `skills.mcp_tools.dashboard_snapshot`

> Source: [skills/mcp_tools/dashboard_snapshot.py:1](../../skills/mcp_tools/dashboard_snapshot.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_dashboard_snapshot``: render the live network map.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_dashboard_snapshot_py__handle(["handle"])
    n_modules_dashboard_engine_py__DashboardEngine___init__["dashboard_engine.DashboardEngine.__init__"]
    n_modules_dashboard_engine_py__DashboardEngine_build_snapshot["dashboard_engine.DashboardEngine.build_snapshot"]
    n_modules_dashboard_engine_py__DashboardEngine_persist_snapshot["dashboard_engine.DashboardEngine.persist_snapshot"]
    n_modules_dashboard_engine_py__DashboardEngine_render_ascii_topology["dashboard_engine.DashboardEngine.render_ascii_topology"]
    n_modules_dashboard_engine_py__DashboardEngine_render_text_map["dashboard_engine.DashboardEngine.render_text_map"]
    n_modules_dashboard_engine_py__DashboardEngine_set_exploit_recommender["dashboard_engine.DashboardEngine.set_exploit_recommender"]
    n_modules_exploit_recommender_py__ExploitRecommender___init__["exploit_recommender.ExploitRecommender.__init__"]
    n_modules_world_model_py__WorldModel___init__["world_model.WorldModel.__init__"]
    n_skills_mcp_tools_dashboard_snapshot_py__handle -.-> n_modules_dashboard_engine_py__DashboardEngine___init__
    n_skills_mcp_tools_dashboard_snapshot_py__handle -.-> n_modules_dashboard_engine_py__DashboardEngine_build_snapshot
    n_skills_mcp_tools_dashboard_snapshot_py__handle -.-> n_modules_dashboard_engine_py__DashboardEngine_persist_snapshot
    n_skills_mcp_tools_dashboard_snapshot_py__handle -.-> n_modules_dashboard_engine_py__DashboardEngine_render_ascii_topology
    n_skills_mcp_tools_dashboard_snapshot_py__handle -.-> n_modules_dashboard_engine_py__DashboardEngine_render_text_map
    n_skills_mcp_tools_dashboard_snapshot_py__handle -.-> n_modules_dashboard_engine_py__DashboardEngine_set_exploit_recommender
    n_skills_mcp_tools_dashboard_snapshot_py__handle -.-> n_modules_exploit_recommender_py__ExploitRecommender___init__
    n_skills_mcp_tools_dashboard_snapshot_py__handle -.-> n_modules_world_model_py__WorldModel___init__
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/dashboard_snapshot.py:28](../../skills/mcp_tools/dashboard_snapshot.py#L28)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Build and persist a dashboard snapshot, returning map and topology.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`DashboardEngine.__init__`](modules.dashboard_engine.py.md#dashboardengine-__init__), [`DashboardEngine.build_snapshot`](modules.dashboard_engine.py.md#dashboardengine-build_snapshot), [`DashboardEngine.persist_snapshot`](modules.dashboard_engine.py.md#dashboardengine-persist_snapshot), [`DashboardEngine.render_ascii_topology`](modules.dashboard_engine.py.md#dashboardengine-render_ascii_topology), [`DashboardEngine.render_text_map`](modules.dashboard_engine.py.md#dashboardengine-render_text_map), [`DashboardEngine.set_exploit_recommender`](modules.dashboard_engine.py.md#dashboardengine-set_exploit_recommender), [`ExploitRecommender.__init__`](modules.exploit_recommender.py.md#exploitrecommender-__init__), [`WorldModel.__init__`](modules.world_model.py.md#worldmodel-__init__)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/dashboard_snapshot.py:13](../../skills/mcp_tools/dashboard_snapshot.py#L13)

```python
TOOL
```

---
