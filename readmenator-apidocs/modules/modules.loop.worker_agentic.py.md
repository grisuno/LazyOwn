# `modules.loop.worker_agentic`

> Source: [modules/loop/worker_agentic.py:1](../../modules/loop/worker_agentic.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

## Contents

- **Classes:** [`WorkerAgenticMixin`](#workeragenticmixin)

## Classes

<a id="workeragenticmixin"></a>

### `WorkerAgenticMixin`

`class` | [modules/loop/worker_agentic.py:225](../../modules/loop/worker_agentic.py#L225)

```python
class WorkerAgenticMixin
```

Subclasses: [`Worker`](modules.lazy_loop.py.md#worker)

Tool-calling agent loop and LLM step planning for a loop worker.

Groups the agentic path: the guard-enforced tool catalogue handed to
the model, the invariant system prompt, the multi-attempt agent
session, operator steer drainage, stop-reason checkpoints and the
deterministic LLM step suggestions used when tool-calling is off.
Every method binds to the host `[`Worker`](modules.lazy_loop.py.md#worker)` through ``self``.

---
