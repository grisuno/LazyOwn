# `modules.asset_graph`

> Source: [modules/asset_graph.py:1](../../modules/asset_graph.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Campaign scope coverage query for the autonomous loop.

The dual-graph asset store that used to live here retired with the
ad-hoc engine: production reads and writes assets through
`[`modules.lazy_loop.AssetGraph`](modules.lazy_loop.py.md#assetgraph)`. What remains is the single
db-backed coverage query consumed by the autonomous daemon.

## Contents

- **Functions:** [`coverage_for`](#coverage_for)

## Functions

<a id="coverage_for"></a>

### `coverage_for`

`function` | [modules/asset_graph.py:12](../../modules/asset_graph.py#L12)

```python
def coverage_for(db: object, workspace_id: int, scope: list[str]) -> dict
```

Report tested scope assets versus total scope from the campaign db.

The scope is the explicit target list (never inferred). An address
counts as tested when present in the workspace hosts.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `db` | `object` |  | Campaign database exposing `[`host_list`](modules.db.py.md#lazyowndb-host_list)`. |
| `workspace_id` | `int` |  | Workspace whose hosts define the tested set. |
| `scope` | `list[str]` |  | Explicit target addresses (never inferred). |

**Returns:** `dict` - Mapping with ``scope``, ``total``, ``tested``, ``untested``
and the tested/total ``ratio``.

---
