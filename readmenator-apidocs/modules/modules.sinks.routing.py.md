# `modules.sinks.routing`

> Source: [modules/sinks/routing.py:1](../../modules/sinks/routing.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Routing-prior sink: learn from terminal outcomes.

## Contents

- **Functions:** [`apply`](#apply)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_sinks_routing_py__apply(["apply"])
    n_modules_lazy_intel_py__record_routing_outcome["lazy_intel.record_routing_outcome"]
    n_modules_sinks_routing_py__apply -.-> n_modules_lazy_intel_py__record_routing_outcome
```

## Functions

<a id="apply"></a>

### `apply`

`function` | [modules/sinks/routing.py:9](../../modules/sinks/routing.py#L9)

```python
def apply(event: OutcomeEvent) -> bool
```

Record one routing outcome for cross-task priors.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `OutcomeEvent` |  | Outcome to learn from. |

**Returns:** `bool` - True when the record was appended.

*Calls:* [`record_routing_outcome`](modules.lazy_intel.py.md#record_routing_outcome)

---
