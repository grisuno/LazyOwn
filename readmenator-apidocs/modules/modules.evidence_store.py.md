# `modules.evidence_store`

> Source: [modules/evidence_store.py:1](../../modules/evidence_store.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Durable, content-addressed evidence store independent of disposable traffic.

A finding binds its proof by traffic digest, but the traffic ledger is a
rotating, tail-bounded stream: once enough exchanges accrue, the row a finding
points at scrolls out of the readable window and the proof is gone while the
finding still claims it. This store snapshots the exchange behind a finding
into its own space the moment it is bound, so the proof outlives any traffic
rotation.

Each snapshot is keyed by its traffic digest, which is itself derived from the
command and output, so the store is content-addressed: the same exchange maps
to the same file and a re-bind is idempotent. Garbage collection reaps only
snapshots that are both unreferenced by any live finding and older than a grace
period, keeping a full day's grace so a failed or racing write is never swept
mid-flight. Nothing here imports the loop runtime, keeping the module cycle-free
and testable in isolation.

## Contents

- **Classes:** [`EvidenceStore`](#evidencestore)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_evidence_store_py__EvidenceStore_preserve(["EvidenceStore.preserve"])
    n_core_atomic_store_py__write_text_atomic["atomic_store.write_text_atomic"]
    n_modules_evidence_store_py__EvidenceStore_preserve -.-> n_core_atomic_store_py__write_text_atomic
```

## Classes

<a id="evidencestore"></a>

### `EvidenceStore`

`class` | [modules/evidence_store.py:53](../../modules/evidence_store.py#L53)

```python
class EvidenceStore
```

Persist and retrieve finding evidence beyond the traffic window.

The store lives under ``sessions/evidence/<task>/`` and holds one JSON
snapshot per bound traffic digest. It is append-mostly: snapshots are
written once and read many times, with an explicit grace-aware GC the only
way a file is removed.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#evidencestore-__init__) | constructor | Bind the store to a task, creating its directory lazily on write. |
| [`directory`](#evidencestore-directory) | property | Return the directory this store writes snapshots into. |
| [`has`](#evidencestore-has) | method | Return True when a snapshot for the digest already exists. |
| [`preserve`](#evidencestore-preserve) | method | Snapshot one traffic exchange durably and return its digest. |
| [`fetch`](#evidencestore-fetch) | method | Return the durable snapshot for a digest, or None when absent. |
| [`gc`](#evidencestore-gc) | method | Reap snapshots neither referenced nor within the grace period. |

<a id="evidencestore-__init__"></a>

#### `EvidenceStore.__init__`

`constructor` | [modules/evidence_store.py:62](../../modules/evidence_store.py#L62)

```python
def __init__(self, task_id: str = '', base_dir: Path | None = None) -> None
```

Bind the store to a task, creating its directory lazily on write.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` | `''` | Campaign/task identifier; blank uses a shared stream. |
| `base_dir` | `Path \| None` | `None` | Optional root override for tests. |

<a id="evidencestore-directory"></a>

#### `EvidenceStore.directory`

`property` | [modules/evidence_store.py:73](../../modules/evidence_store.py#L73)

Decorators: `@property`

```python
def directory(self) -> Path
```

Return the directory this store writes snapshots into.

**Returns:** `Path`

<a id="evidencestore-has"></a>

#### `EvidenceStore.has`

`method` | [modules/evidence_store.py:88](../../modules/evidence_store.py#L88)

```python
def has(self, digest: str) -> bool
```

Return True when a snapshot for the digest already exists.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `digest` | `str` |  |  |

**Returns:** `bool`

<a id="evidencestore-preserve"></a>

#### `EvidenceStore.preserve`

`method` | [modules/evidence_store.py:93](../../modules/evidence_store.py#L93)

```python
def preserve(self, record: dict[str, Any]) -> str
```

Snapshot one traffic exchange durably and return its digest.

The write is idempotent: a digest already preserved is left untouched
so re-binding the same evidence never rewrites it. A missing or unsafe
digest, or any I/O failure, returns an empty string rather than raising,
because losing a snapshot must never abort the bind that triggered it.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `record` | `dict[str, Any]` |  | A traffic record carrying at least `[`digest`](modules.loop.decision_log.py.md#digest)`; ``command``, ``output``, `[`preview`](cli.sessions_browser.py.md#sessionsbrowserstate-preview)`, ``bytes`` and `[`meta`](modules.loop_guardrails.py.md#fact-meta)` are preserved when present. |

**Returns:** `str` - The preserved digest, or an empty string on rejection or failure.

*Calls:* [`write_text_atomic`](core.atomic_store.py.md#write_text_atomic)

<a id="evidencestore-fetch"></a>

#### `EvidenceStore.fetch`

`method` | [modules/evidence_store.py:135](../../modules/evidence_store.py#L135)

```python
def fetch(self, digest: str) -> dict[str, Any] | None
```

Return the durable snapshot for a digest, or None when absent.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `digest` | `str` |  | The traffic digest to retrieve. |

**Returns:** `dict[str, Any] | None` - The snapshot document, or None when no snapshot exists or the file
is unreadable.

<a id="evidencestore-gc"></a>

#### `EvidenceStore.gc`

`method` | [modules/evidence_store.py:153](../../modules/evidence_store.py#L153)

```python
def gc(self, referenced: set[str], grace_seconds: float = _DEFAULT_GRACE_SECONDS) -> int
```

Reap snapshots neither referenced nor within the grace period.

A snapshot is removed only when its digest is absent from
``referenced`` and its file is older than ``grace_seconds``, so a
just-written snapshot that a finding has not yet bound is never swept.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `referenced` | `set[str]` |  | Digests still claimed by a live finding. |
| `grace_seconds` | `float` | `_DEFAULT_GRACE_SECONDS` | Minimum snapshot age before it is eligible to reap. |

**Returns:** `int` - The number of snapshots removed.

*Called by:* [`LazyCommandSet.do_lazy_evidence`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_evidence)

---
