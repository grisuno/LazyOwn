# `modules.intel_fusion`

> Source: [modules/intel_fusion.py:1](../../modules/intel_fusion.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Sessions attack-intel fusion: data -> information -> intelligence.

Reads every campaign artefact under ``sessions/`` (world model, lazy loop
graphs, objectives, scans, event logs) and fuses them into ONE heterogeneous
graph centred on the LazyOwn C2: hosts, ports/services, findings, loop
tasks and objectives. Every node carries a deterministic id
(``sha1(kind:value)``) and every edge an ``evidence`` string naming the
source artefact, so each relation is traceable like a provenance-tracked
research graph.

Payload shape mirrors ReadMenator ``ForceGraphRenderer.build_payload`` so
``templates/intel.html`` (a clone of ReadMenator ``_forcegraph_page``) can
reuse the exact same engine, physics sizes, glyphs, colors, legend and
inspector: file nodes carry ``family``/``layer``/``language``/`[`rank`](modules.atomic_exploit_bridge.py.md#rank)`/
``doc``/``symbol_list``; community and layer hub nodes plus `[`member_of`](modules.kerberoasting.py.md#kerberoasttarget-member_of)` /
``layered_as`` structural edges are appended automatically.

## Contents

- **Functions:** [`node_id`](#node_id), [`build_intel_graph`](#build_intel_graph), [`group_colors`](#group_colors), [`page_settings`](#page_settings), [`build_analytics`](#build_analytics), [`build_bundle_payload`](#build_bundle_payload), [`bundle_settings`](#bundle_settings), [`assign_layout`](#assign_layout), [`svg_selection`](#svg_selection), [`relations_svg`](#relations_svg), [`write_summary`](#write_summary)
- **Constants:** [`NODE_COLORS`](#node_colors), [`EDGE_COLORS`](#edge_colors)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_intel_fusion_py__build_intel_graph(["build_intel_graph"])
    n_modules_intel_fusion_py__node_id(["node_id"])
    n_modules_intel_fusion_py__page_settings(["page_settings"])
    n_modules_intel_fusion_py__group_colors(["group_colors"])
    n_modules_intel_fusion_py__bundle_settings(["bundle_settings"])
    n_modules_intel_fusion_py__relations_svg(["relations_svg"])
    n_modules_intel_fusion_py__svg_selection(["svg_selection"])
    n_modules_lazy_loop_py__ExplorationGraph_add_edge["lazy_loop.ExplorationGraph.add_edge"]
    n_modules_world_model_py__read_state_dict["world_model.read_state_dict"]
    n_modules_intel_fusion_py__build_intel_graph --> n_modules_intel_fusion_py__node_id
    n_modules_intel_fusion_py__page_settings --> n_modules_intel_fusion_py__group_colors
    n_modules_intel_fusion_py__bundle_settings --> n_modules_intel_fusion_py__group_colors
    n_modules_intel_fusion_py__relations_svg --> n_modules_intel_fusion_py__svg_selection
    n_modules_intel_fusion_py__build_intel_graph -.-> n_modules_lazy_loop_py__ExplorationGraph_add_edge
    n_modules_intel_fusion_py__build_intel_graph -.-> n_modules_world_model_py__read_state_dict
```

## Functions

<a id="node_id"></a>

### `node_id`

`function` | [modules/intel_fusion.py:192](../../modules/intel_fusion.py#L192)

```python
def node_id(kind: str, value: str) -> str
```

Deterministic node id from kind + normalized value.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `kind` | `str` |  |  |
| `value` | `str` |  |  |

**Returns:** `str`

*Called by:* [`build_intel_graph`](#build_intel_graph)

---

<a id="build_intel_graph"></a>

### `build_intel_graph`

`function` | [modules/intel_fusion.py:260](../../modules/intel_fusion.py#L260)

```python
def build_intel_graph(sessions_dir: str | Path = SESSIONS_DIR, est_cap: int = 300) -> dict
```

Fuse all session artefacts into one C2-centred intel graph.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sessions_dir` | `str \| Path` | `SESSIONS_DIR` |  |
| `est_cap` | `int` | `300` |  |

**Returns:** `dict`

*Calls:* [`node_id`](#node_id), [`ExplorationGraph.add_edge`](modules.lazy_loop.py.md#explorationgraph-add_edge), [`read_state_dict`](modules.world_model.py.md#read_state_dict)

*Called by:* [`build_attack_graph`](modules.attack_surface3d.py.md#build_attack_graph), [`apply`](modules.sinks.intel_graph.py.md#apply)

---

<a id="group_colors"></a>

### `group_colors`

`function` | [modules/intel_fusion.py:714](../../modules/intel_fusion.py#L714)

```python
def group_colors(graph: dict) -> dict
```

Stable colors for layer/language groupings (ReadMenator contract).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict` |  |  |

**Returns:** `dict`

*Called by:* [`bundle_settings`](#bundle_settings), [`page_settings`](#page_settings)

---

<a id="page_settings"></a>

### `page_settings`

`function` | [modules/intel_fusion.py:730](../../modules/intel_fusion.py#L730)

```python
def page_settings(graph: dict | None = None) -> dict
```

Explorer page settings with ReadMenator physics sizes (exact values).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict \| None` | `None` |  |

**Returns:** `dict`

*Calls:* [`group_colors`](#group_colors)

---

<a id="build_analytics"></a>

### `build_analytics`

`function` | [modules/intel_fusion.py:787](../../modules/intel_fusion.py#L787)

```python
def build_analytics(graph: dict, summary: dict | None = None) -> dict
```

Side-panel analytics (attribution funnel + intel summary).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict` |  |  |
| `summary` | `dict \| None` | `None` |  |

**Returns:** `dict`

---

<a id="build_bundle_payload"></a>

### `build_bundle_payload`

`function` | [modules/intel_fusion.py:874](../../modules/intel_fusion.py#L874)

```python
def build_bundle_payload(graph: dict) -> dict
```

Derive the circular/spherical bundle payload from a fused graph.

Communities keep size order (largest first); ``misc`` nodes form a
trailing unassigned group. Inside a group files are ordered by rank,
so hubs sit at the center of their arc and cap. Edges are distinct
directed file index pairs.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict` |  |  |

**Returns:** `dict`

---

<a id="bundle_settings"></a>

### `bundle_settings`

`function` | [modules/intel_fusion.py:990](../../modules/intel_fusion.py#L990)

```python
def bundle_settings(graph: dict | None = None) -> dict
```

Bundle page settings with ReadMenator sizes (exact values).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict \| None` | `None` |  |

**Returns:** `dict`

*Calls:* [`group_colors`](#group_colors)

---

<a id="assign_layout"></a>

### `assign_layout`

`function` | [modules/intel_fusion.py:1021](../../modules/intel_fusion.py#L1021)

```python
def assign_layout(graph: dict, mode: str = 'force') -> dict
```

Attach x/y/z for radial/spherical modes; force modes stay free.

Accepts ReadMenator layout names (`[`force`](cli.output_mode.py.md#outputmode-force)`, ``cluster``, ``radial``,
``dag``) plus legacy intel names (``force2d``, ``force3d``,
``circular``, ``spherical``). Force-family modes return without preset
positions so the client physics (charge -300, distance 120, 400 ticks
+ fit-to-view) places every graph on screen.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict` |  |  |
| `mode` | `str` | `'force'` |  |

**Returns:** `dict`

---

<a id="svg_selection"></a>

### `svg_selection`

`function` | [modules/intel_fusion.py:1147](../../modules/intel_fusion.py#L1147)

```python
def svg_selection(graph: dict, cap_nodes: int = SVG_NODE_CAP) -> list[str]
```

Return the node ids a bounded snapshot keeps, most important first.

The lightest intel snapshot for static rendering: the c2 hub, then the
hottest CVE matches, then the most connected nodes. Args: `[`graph`](lazyc2.py.md#graph)`
intel payload, ``cap_nodes`` maximum selected ids.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict` |  |  |
| `cap_nodes` | `int` | `SVG_NODE_CAP` |  |

**Returns:** `list[str]` - Selected node ids in placement order.

*Called by:* [`relations_svg`](#relations_svg)

---

<a id="relations_svg"></a>

### `relations_svg`

`function` | [modules/intel_fusion.py:1187](../../modules/intel_fusion.py#L1187)

```python
def relations_svg(graph: dict, cap_nodes: int = SVG_NODE_CAP) -> str
```

Render a static svg snapshot of the intel graph for documents.

Pure, bounded and XML-escaped: circles per selected node (fill by
kind, ring by heat on CVE nodes), lines only between rendered nodes
and a legend row. Scan-derived values never reach the markup raw, so
the output is safe to embed with ``| safe``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict` |  | Intel graph payload from [`build_intel_graph`](#build_intel_graph). |
| `cap_nodes` | `int` | `SVG_NODE_CAP` | Maximum rendered nodes. |

**Returns:** `str` - SVG markup, or "" when the graph has no renderable nodes.

*Calls:* [`svg_selection`](#svg_selection)

---

<a id="write_summary"></a>

### `write_summary`

`function` | [modules/intel_fusion.py:1296](../../modules/intel_fusion.py#L1296)

```python
def write_summary(graph: dict, sessions_dir: str | Path = SESSIONS_DIR) -> dict
```

Score host exposure with a normalized, per-component breakdown.

The score is bounded 0..100 with capped components, and every point
carries a label so the planner and the operator can read why one
host outranks another:

- heat: hottest CVE candidate matched on the host (hot 40, warm 20,
  cold 5), capped at 50;
- findings: severity-weighted findings attached to the host
  (critical/high 25, medium 10, low 3), capped at 25;
- controlled: the C2 owns the host (10);
- connectivity: capped node degree (10);
- activity: recent log mentions (5);
- recency: the host changed this week in the world change log (10);
- ghost: the host answers on its last address without resolving (15).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `graph` | `dict` |  | Intel graph from [`build_intel_graph`](#build_intel_graph). |
| `sessions_dir` | `str \| Path` | `SESSIONS_DIR` | Sessions directory for ``intel_summary.json``. |

**Returns:** `dict` - Summary dict; ``top_exposed`` rows gain ``score_detail``.

*Called by:* [`refresh_summary`](modules.attack_surface3d.py.md#refresh_summary), [`apply`](modules.sinks.intel_graph.py.md#apply)

---

## Constants

<a id="node_colors"></a>

### `NODE_COLORS`

`constant` | [modules/intel_fusion.py:32](../../modules/intel_fusion.py#L32)

```python
NODE_COLORS
```

---

<a id="edge_colors"></a>

### `EDGE_COLORS`

`constant` | [modules/intel_fusion.py:45](../../modules/intel_fusion.py#L45)

```python
EDGE_COLORS
```

---
