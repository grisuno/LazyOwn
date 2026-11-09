# `modules.loop.worker_gating`

> Source: [modules/loop/worker_gating.py:1](../../modules/loop/worker_gating.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

## Contents

- **Classes:** [`WorkerGatingMixin`](#workergatingmixin)

## Classes

<a id="workergatingmixin"></a>

### `WorkerGatingMixin`

`class` | [modules/loop/worker_gating.py:6](../../modules/loop/worker_gating.py#L6)

```python
class WorkerGatingMixin
```

Subclasses: [`Worker`](modules.lazy_loop.py.md#worker)

Scope, operating-system and privilege gates for a loop worker.

Groups the policy decisions a worker makes before a command reaches
the shell: explicit and lab-default scope enforcement, OS-mismatch
vetoes, passwordless-sudo skips and whole-command scope checks. Every
method binds to the host `[`Worker`](modules.lazy_loop.py.md#worker)` through ``self`` and uses the
collaborators set in `[`__init__`](init__.py.md)` (`[`activity`](cli.killchain.py.md#phaseprogress-activity)`, ``store``,
``task_id``) plus ``_target_for`` and ``_resolved_command``.

---
