# `modules.gym_cleanup`

> Source: [modules/gym_cleanup.py:1](../../modules/gym_cleanup.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Gym machine cleanup on LazyOwn exit.

Lab scenario containers (``lazyown-lab-*``) and cyber range containers
(``lazyown-range-*``) hold real memory and CPU on the operator host.
When an interactive operator shell closes through any path (quit, EOF,
SIGTERM, SIGHUP, atexit) every running gym machine is stopped so
nothing keeps leasing resources after the session. This is OPT-IN:
``"gym_cleanup_on_exit": true`` in ``payload.json`` enables it.

Autonomous and headless processes (dashboard loop subprocesses,
``-c`` runs, MCP workers) never stop gym machines — a loop subprocess
exiting used to kill the gym out from under the next run, which is why
operators kept finding the lab down after every auto_loop.

## Contents

- **Functions:** [`cleanup_enabled`](#cleanup_enabled), [`cleanup_gym_machines`](#cleanup_gym_machines)
- **Constants:** [`CONFIG_KEY`](#config_key)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_gym_cleanup_py__cleanup_gym_machines(["cleanup_gym_machines"])
    n_modules_gym_cleanup_py__cleanup_enabled(["cleanup_enabled"])
    n_core_config_py__load_payload["config.load_payload"]
    n_modules_lab_runtime_py__stop_ranges["lab_runtime.stop_ranges"]
    n_modules_gym_cleanup_py__cleanup_gym_machines --> n_modules_gym_cleanup_py__cleanup_enabled
    n_modules_gym_cleanup_py__cleanup_enabled -.-> n_core_config_py__load_payload
    n_modules_gym_cleanup_py__cleanup_gym_machines -.-> n_modules_lab_runtime_py__stop_ranges
```

## Functions

<a id="cleanup_enabled"></a>

### `cleanup_enabled`

`function` | [modules/gym_cleanup.py:28](../../modules/gym_cleanup.py#L28)

```python
def cleanup_enabled() -> bool
```

Return whether exit cleanup is enabled (default off, opt-in).

**Returns:** `bool`

*Calls:* [`load_payload`](core.config.py.md#load_payload)

*Called by:* [`cleanup_gym_machines`](#cleanup_gym_machines)

---

<a id="cleanup_gym_machines"></a>

### `cleanup_gym_machines`

`function` | [modules/gym_cleanup.py:44](../../modules/gym_cleanup.py#L44)

```python
def cleanup_gym_machines(verbose: bool = False) -> dict[str, Any]
```

Stop every running lab and range machine.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `verbose` | `bool` | `False` | When True, print one line per stopped machine group. |

**Returns:** `dict[str, Any]` - Mapping with ``enabled``, ``labs`` and `[`ranges`](modules.lazy_feedmatch.py.md#feedentry-ranges)` stop results.

*Calls:* [`cleanup_enabled`](#cleanup_enabled), [`stop_ranges`](modules.lab_runtime.py.md#stop_ranges)

---

## Constants

<a id="config_key"></a>

### `CONFIG_KEY`

`constant` | [modules/gym_cleanup.py:24](../../modules/gym_cleanup.py#L24)

```python
CONFIG_KEY = 'gym_cleanup_on_exit'
```

---
