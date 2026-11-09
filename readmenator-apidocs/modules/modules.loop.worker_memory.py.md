# `modules.loop.worker_memory`

> Source: [modules/loop/worker_memory.py:1](../../modules/loop/worker_memory.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

## Contents

- **Classes:** [`WorkerMemoryMixin`](#workermemorymixin)

## Classes

<a id="workermemorymixin"></a>

### `WorkerMemoryMixin`

`class` | [modules/loop/worker_memory.py:6](../../modules/loop/worker_memory.py#L6)

```python
class WorkerMemoryMixin
```

Subclasses: [`Worker`](modules.lazy_loop.py.md#worker)

Durable and in-session memory behaviour for a loop worker.

Groups the worker's failure counters, task-scoped vector memory and
reactive absorption so the executing worker stays a thin coordinator.
Every method binds to the host `[`Worker`](modules.lazy_loop.py.md#worker)` through ``self`` and relies
on the collaborators the worker sets in `[`__init__`](init__.py.md)` (`[`activity`](cli.killchain.py.md#phaseprogress-activity)`,
``store``, ``task_id``) plus ``_target_for`` for target resolution.

---
