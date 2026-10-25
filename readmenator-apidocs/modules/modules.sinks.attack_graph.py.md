# `modules.sinks.attack_graph`

> Source: [modules/sinks/attack_graph.py:1](../../modules/sinks/attack_graph.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Attack-graph sink: rebuild the attack surface after meaningful outcomes.

## Contents

- **Functions:** [`apply`](#apply)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_sinks_attack_graph_py__apply(["apply"])
    n_modules_attack_surface3d_py__build_attack_graph["attack_surface3d.build_attack_graph"]
    n_modules_attack_surface3d_py__refresh_summary["attack_surface3d.refresh_summary"]
    n_modules_sinks_attack_graph_py__apply -.-> n_modules_attack_surface3d_py__build_attack_graph
    n_modules_sinks_attack_graph_py__apply -.-> n_modules_attack_surface3d_py__refresh_summary
```

## Functions

<a id="apply"></a>

### `apply`

`function` | [modules/sinks/attack_graph.py:13](../../modules/sinks/attack_graph.py#L13)

```python
def apply(event: OutcomeEvent) -> bool
```

Rebuild the attack graph and its exposure summary.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `OutcomeEvent` |  | Outcome that may change the graph. |

**Returns:** `bool` - True when the graph was rebuilt.

*Calls:* [`build_attack_graph`](modules.attack_surface3d.py.md#build_attack_graph), [`refresh_summary`](modules.attack_surface3d.py.md#refresh_summary)

---
