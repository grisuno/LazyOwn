# `modules.session_cleanup`

> Source: [modules/session_cleanup.py:1](../../modules/session_cleanup.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Ephemeral infrastructure cleanup on shell exit.

Stops disposable assets (cyber range stacks, redirector tunnels, stray
``cloudflared`` processes) when the operator leaves the shell via Ctrl-D,
``quit``, ``qa`` or ``exit``. Everything here is best-effort and bounded:
cleanup must never block or crash the exit path.

## Contents

- **Functions:** [`find_cloudflared_pids`](#find_cloudflared_pids), [`stop_cloudflared_processes`](#stop_cloudflared_processes), [`cleanup_ephemeral_infra`](#cleanup_ephemeral_infra)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_session_cleanup_py__stop_cloudflared_processes(["stop_cloudflared_processes"])
    n_modules_session_cleanup_py__find_cloudflared_pids(["find_cloudflared_pids"])
    n_modules_session_cleanup_py__cleanup_ephemeral_infra(["cleanup_ephemeral_infra"])
    n_modules_session_cleanup_py__stop_cloudflared_processes --> n_modules_session_cleanup_py__find_cloudflared_pids
    n_modules_session_cleanup_py__cleanup_ephemeral_infra --> n_modules_session_cleanup_py__stop_cloudflared_processes
```

## Functions

<a id="find_cloudflared_pids"></a>

### `find_cloudflared_pids`

`function` | [modules/session_cleanup.py:28](../../modules/session_cleanup.py#L28)

```python
def find_cloudflared_pids(ps_output: str) -> list[int]
```

Extract PIDs of ``cloudflared tunnel`` processes from ps output.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ps_output` | `str` |  | Raw stdout of ``ps -eo pid,args``. |

**Returns:** `list[int]` - Matching PIDs excluding the current process.

*Called by:* [`stop_cloudflared_processes`](#stop_cloudflared_processes)

---

<a id="stop_cloudflared_processes"></a>

### `stop_cloudflared_processes`

`function` | [modules/session_cleanup.py:94](../../modules/session_cleanup.py#L94)

```python
def stop_cloudflared_processes() -> int
```

Terminate stray ``cloudflared tunnel`` host processes.

**Returns:** `int` - Number of processes signalled.

*Calls:* [`find_cloudflared_pids`](#find_cloudflared_pids)

*Called by:* [`cleanup_ephemeral_infra`](#cleanup_ephemeral_infra)

---

<a id="cleanup_ephemeral_infra"></a>

### `cleanup_ephemeral_infra`

`function` | [modules/session_cleanup.py:120](../../modules/session_cleanup.py#L120)

```python
def cleanup_ephemeral_infra() -> dict[str, bool]
```

Stop all disposable infrastructure owned by this checkout.

Shuts down every range profile stack, the redirector stack, and stray
``cloudflared`` host processes. Safe to call when Docker is absent.

**Returns:** `dict[str, bool]` - Dict of teardown step name to success flag.

*Calls:* [`stop_cloudflared_processes`](#stop_cloudflared_processes)

*Called by:* [`LazyOwnShell.postloop`](lazyown.py.md#lazyownshell-postloop)

---
