# `modules.digest`

> Source: [modules/digest.py:1](../../modules/digest.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Operator digest generation for loop runs.

Digests compress a run into three blocks an operator actually reads:
what ran and how it ended (steps/outcomes), what the run knows
(findings, facts, assets) and what to do next (paths forward: leftover
blocks, pending creds, untested assets). Written as ``digest_<task>.md``
next to the archived graphs so the operator can hand it to the next
shift without reading an activity log.

## Contents

- **Functions:** [`build_engine_digest`](#build_engine_digest), [`write_digest`](#write_digest), [`worker_results_digest`](#worker_results_digest)

## Functions

<a id="build_engine_digest"></a>

### `build_engine_digest`

`function` | [modules/digest.py:20](../../modules/digest.py#L20)

```python
def build_engine_digest(task_id: str, status: str, rounds: int, findings: list[str], facts: list[str], blocks: list[str], reaction_backlog: list[str] | None = None) -> str
```

Render the engine-loop markdown digest.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  | Task this digest describes. |
| `status` | `str` |  | Terminal loop status. |
| `rounds` | `int` |  | Round count executed. |
| `findings` | `list[str]` |  | Finding summaries. |
| `facts` | `list[str]` |  | Recent fact summaries. |
| `blocks` | `list[str]` |  | Blocked bases that burned attempts. |
| `reaction_backlog` | `list[str] \| None` | `None` | Reactive decisions parked but unused. |

**Returns:** `str`

---

<a id="write_digest"></a>

### `write_digest`

`function` | [modules/digest.py:71](../../modules/digest.py#L71)

```python
def write_digest(task_id: str, body: str, root: Path | None = None) -> str
```

Persist the digest beside the archives; returns the written path.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  |  |
| `body` | `str` |  |  |
| `root` | `Path \| None` | `None` |  |

**Returns:** `str`

---

<a id="worker_results_digest"></a>

### `worker_results_digest`

`function` | [modules/digest.py:82](../../modules/digest.py#L82)

```python
def worker_results_digest(rows: list[dict]) -> tuple[list[str], list[str]]
```

Extract displayed step lines and blocked bases from result dicts.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `rows` | `list[dict]` |  |  |

**Returns:** `tuple[list[str], list[str]]`

---
