# `lazyc2.blueprints.loops`

> Source: [lazyc2/blueprints/loops.py:1](../../lazyc2/blueprints/loops.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Loops blueprint — autonomous loop control API for the dashboard.

Owns the whole ``/api/loops`` surface: starting an ``auto_loop`` or a
``lazynmap`` scan as an isolated subprocess, listing every loop, reading
one loop's output log and stopping a loop. This is one responsibility
sliced out of the former ``lazyc2.py`` god object; the loop manager
singleton and validation helpers come from [`modules.loop_manager`](modules.loop_manager.py.md)
so the CLI and the dashboard share the same contract.

The blueprint is wired lazily through [`init_loops_bp`](#init_loops_bp), which binds
the main application's auth, CSRF and rate-limiter decorators after that
module has finished loading, avoiding a circular import at module load.

## Contents

- **Functions:** [`init_loops_bp`](#init_loops_bp)

## Functions

<a id="init_loops_bp"></a>

### `init_loops_bp`

`function` | [lazyc2/blueprints/loops.py:179](../../lazyc2/blueprints/loops.py#L179)

```python
def init_loops_bp(limiter=None, guard=None) -> None
```

Bind the loop routes with the host application's guard decorators.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `limiter` |  | `None` | The application rate limiter; when provided each route is decorated with the same limits the former god object used. |
| `guard` |  | `None` | Callable ``(view, needs_csrf) -> view`` wrapping each route with auth (and CSRF when ``needs_csrf``). Defaults to a strict operator-session guard when the host application does not inject one. |

*Called by:* [`create_app`](lazyc2.app_factory.py.md#create_app)

---
