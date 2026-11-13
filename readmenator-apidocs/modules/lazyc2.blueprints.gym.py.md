# `lazyc2.blueprints.gym`

> Source: [lazyc2/blueprints/gym.py:1](../../lazyc2/blueprints/gym.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Gym blueprint — Red Team Gym lab lifecycle for the dashboard.

Exposes the operator endpoints that launch, inspect and stop the
framework's training gyms (Metasploitable2, AD lab, Juice Shop, ...)
backed by [`modules.lab_runtime`](modules.lab_runtime.py.md). The viz.js node graph reads
``/api/gym/nodes`` to draw every running gym as its own node, and the
node context menu drives ``/api/gym/stop`` so a gym can be torn down
with one click from the graph.

Every route requires an authenticated operator session and every
mutating route enforces the same CSRF policy as the rest of the C2
(the shared [`lazyc2.security.csrf.CSRFPolicy`](lazyc2.security.csrf.py.md#csrfpolicy) instance is read
from ``app.config``), so this blueprint adds no new auth surface.

## Contents

- **Constants:** [`GYM_NODE_PREFIX`](#gym_node_prefix)

## Constants

<a id="gym_node_prefix"></a>

### `GYM_NODE_PREFIX`

`constant` | [lazyc2/blueprints/gym.py:30](../../lazyc2/blueprints/gym.py#L30)

```python
GYM_NODE_PREFIX = 'gym-'
```

---
