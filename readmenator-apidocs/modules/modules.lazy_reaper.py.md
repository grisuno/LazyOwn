# `modules.lazy_reaper`

> Source: [modules/lazy_reaper.py:1](../../modules/lazy_reaper.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Reaper: expire lazy-loop tasks whose process proves dead.

Lazy re-brand of the broker-verified orphan pattern: a stuck ``running``
row is only harvested when the liveness signal it owns (its heartbeat)
is provably stale — the reaper never closes on absence of evidence. A
heartbeat inside the window, an old-but-paused or queued row stays
untouched; rows that expire get one idempotent terminal stamp and an
abort cause so the retry surfaces can re-enter them deliberately.

State: the operator's own task store (``sessions/lazy/tasks.json``);
audit trail lands in ``sessions/lazy/reaper.jsonl``, bounded per file.

## Contents

- **Functions:** [`reap`](#reap)
- **Constants:** [`REAPER_LOG_FILENAME`](#reaper_log_filename), [`DEFAULT_STALE_SECONDS`](#default_stale_seconds)

## Functions

<a id="reap"></a>

### `reap`

`function` | [modules/lazy_reaper.py:30](../../modules/lazy_reaper.py#L30)

```python
def reap(store: Any, log_path: str | Path | None = None, now: float | None = None, stale_seconds: float = DEFAULT_STALE_SECONDS) -> dict[str, int]
```

Expire tasks whose heartbeat is provably stale.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `store` | `Any` |  | Task store object with ``list()`` rows and ``set_status(task_id, status)``; pass the engine store. |
| `log_path` | `str \| Path \| None` | `None` | Audit trail file; defaults under the lazy store dir. |
| `now` | `float \| None` | `None` | Reference epoch; defaults to current time. |
| `stale_seconds` | `float` | `DEFAULT_STALE_SECONDS` | Heartbeat age that proves death. |

**Returns:** `dict[str, int]` - ``{"examined", "expired", "kept"}`` counts. Store failures are
fail-soft: an unusable store reports ``examined=0`` and nothing
changes.

---

## Constants

<a id="reaper_log_filename"></a>

### `REAPER_LOG_FILENAME`

`constant` | [modules/lazy_reaper.py:21](../../modules/lazy_reaper.py#L21)

```python
REAPER_LOG_FILENAME = 'reaper.jsonl'
```

---

<a id="default_stale_seconds"></a>

### `DEFAULT_STALE_SECONDS`

`constant` | [modules/lazy_reaper.py:22](../../modules/lazy_reaper.py#L22)

```python
DEFAULT_STALE_SECONDS = 45 * 60.0
```

---
