# `modules.loop.worker_execution`

> Source: [modules/loop/worker_execution.py:1](../../modules/loop/worker_execution.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

## Contents

- **Classes:** [`WorkerExecutionMixin`](#workerexecutionmixin)

## Classes

<a id="workerexecutionmixin"></a>

### `WorkerExecutionMixin`

`class` | [modules/loop/worker_execution.py:10](../../modules/loop/worker_execution.py#L10)

```python
class WorkerExecutionMixin
```

Subclasses: [`Worker`](modules.lazy_loop.py.md#worker)

Command execution, background jobs and persistent-shell lifecycle for a loop worker.

Groups the mechanics of actually running a step: dispatch through the
injected executor or the LazyOwn registry, tracked background jobs, a
persistent bash session, alias resolution and the small admissibility
helpers (deny constraints, auto-approval, missing binaries). Every
method binds to the host `[`Worker`](modules.lazy_loop.py.md#worker)` through ``self`` and relies on the
collaborators set in `[`__init__`](init__.py.md)` (`[`activity`](cli.killchain.py.md#phaseprogress-activity)`, ``store``, `[`shell`](lazyc2.state.py.md#shell)`,
``_jobs``, ``_shell_session``, ``_shell_queue``).

---
