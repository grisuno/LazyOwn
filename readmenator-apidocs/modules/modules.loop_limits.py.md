# `modules.loop_limits`

> Source: [modules/loop_limits.py:1](../../modules/loop_limits.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Canonical operating limits for the autonomous loop.

Single source of truth for the CLI parse defaults and hard caps shared
by `[`modules.lazy_runner`](modules.lazy_runner.py.md)` (CLI runner), `[`modules.loop_manager`](modules.loop_manager.py.md)` (C2
dashboard subprocess manager) and the ``auto_loop`` MCP tool. Engine
direct-call defaults are a separate concern and stay in
`[`modules.lazy_loop`](modules.lazy_loop.py.md)` (``ENGINE_DEFAULT_*``).

## Contents

- **Constants:** [`DEFAULT_ROUNDS`](#default_rounds), [`DEFAULT_WORKERS`](#default_workers), [`MAX_ROUNDS`](#max_rounds), [`MAX_WORKERS`](#max_workers)

## Constants

<a id="default_rounds"></a>

### `DEFAULT_ROUNDS`

`constant` | [modules/loop_limits.py:12](../../modules/loop_limits.py#L12)

```python
DEFAULT_ROUNDS = 6
```

---

<a id="default_workers"></a>

### `DEFAULT_WORKERS`

`constant` | [modules/loop_limits.py:13](../../modules/loop_limits.py#L13)

```python
DEFAULT_WORKERS = 2
```

---

<a id="max_rounds"></a>

### `MAX_ROUNDS`

`constant` | [modules/loop_limits.py:14](../../modules/loop_limits.py#L14)

```python
MAX_ROUNDS = 50
```

---

<a id="max_workers"></a>

### `MAX_WORKERS`

`constant` | [modules/loop_limits.py:15](../../modules/loop_limits.py#L15)

```python
MAX_WORKERS = 5
```

---
