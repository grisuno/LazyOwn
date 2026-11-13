# `modules.wire_capture`

> Source: [modules/wire_capture.py:1](../../modules/wire_capture.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Durable byte-for-byte capture of a traffic exchange's raw output.

The traffic ledger keeps only a truncated head of each exchange inline, enough
to preview but not to reproduce: once an output runs past the inline cutoff the
tail is gone, so a finding bound to that digest can never be replayed exactly.
This store snapshots the full, unmodified output beside the evidence store the
moment it is produced, keyed by the same traffic digest, so the proof can be
reconstructed to the byte regardless of how far the ledger has rotated.

Capture is content-addressed and idempotent: the digest already derives from
command and output, so the same exchange maps to the same file and a re-capture
is a no-op. Writes are bounded and atomic, and any failure degrades to the
truncated inline copy rather than raising, because losing the raw wire must
never abort the execution that produced it. Nothing here imports the loop
runtime, keeping the module cycle-free.

## Contents

- **Classes:** [`WireStore`](#wirestore)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_wire_capture_py__WireStore_capture(["WireStore.capture"])
    n_core_atomic_store_py__write_bytes_atomic["atomic_store.write_bytes_atomic"]
    n_modules_wire_capture_py__WireStore_capture -.-> n_core_atomic_store_py__write_bytes_atomic
```

## Classes

<a id="wirestore"></a>

### `WireStore`

`class` | [modules/wire_capture.py:47](../../modules/wire_capture.py#L47)

```python
class WireStore
```

Persist and retrieve the full raw output of a traffic exchange.

The store lives under ``sessions/wire/<task>/`` and holds one blob per
captured traffic digest. It is append-mostly: a blob is written once and
read many times, and is only ever removed by the evidence garbage collector
that owns the same digests.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#wirestore-__init__) | constructor | Bind the store to a task, creating its directory lazily on write. |
| [`directory`](#wirestore-directory) | property | Return the directory this store writes blobs into. |
| [`has`](#wirestore-has) | method | Return True when a raw blob for the digest already exists. |
| [`capture`](#wirestore-capture) | method | Snapshot the full raw output for a digest, idempotently. |
| [`truncated`](#wirestore-truncated) | method | Return True when a captured blob was clipped below its full size. |
| [`fetch`](#wirestore-fetch) | method | Return the full raw output for a digest, or None when absent. |

<a id="wirestore-__init__"></a>

#### `WireStore.__init__`

`constructor` | [modules/wire_capture.py:56](../../modules/wire_capture.py#L56)

```python
def __init__(self, task_id: str = '', base_dir: Path | None = None) -> None
```

Bind the store to a task, creating its directory lazily on write.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` | `''` | Campaign/task identifier; blank uses a shared stream. |
| `base_dir` | `Path \| None` | `None` | Optional root override for tests. |

<a id="wirestore-directory"></a>

#### `WireStore.directory`

`property` | [modules/wire_capture.py:67](../../modules/wire_capture.py#L67)

Decorators: `@property`

```python
def directory(self) -> Path
```

Return the directory this store writes blobs into.

**Returns:** `Path`

<a id="wirestore-has"></a>

#### `WireStore.has`

`method` | [modules/wire_capture.py:82](../../modules/wire_capture.py#L82)

```python
def has(self, digest: str) -> bool
```

Return True when a raw blob for the digest already exists.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `digest` | `str` |  |  |

**Returns:** `bool`

<a id="wirestore-capture"></a>

#### `WireStore.capture`

`method` | [modules/wire_capture.py:87](../../modules/wire_capture.py#L87)

```python
def capture(self, digest: str, raw: str, max_bytes: int = _MAX_WIRE_BYTES) -> str
```

Snapshot the full raw output for a digest, idempotently.

A digest already captured is left untouched so re-executing the same
exchange never rewrites it. A missing or unsafe digest, or any I/O
failure, returns an empty string rather than raising.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `digest` | `str` |  | The traffic digest keying this exchange. |
| `raw` | `str` |  | The full, unmodified output to preserve. |
| `max_bytes` | `int` | `_MAX_WIRE_BYTES` | Upper bound on bytes written, guarding against an unbounded capture flooding the store. |

**Returns:** `str` - The captured digest, or an empty string on rejection or failure.

*Calls:* [`write_bytes_atomic`](core.atomic_store.py.md#write_bytes_atomic)

<a id="wirestore-truncated"></a>

#### `WireStore.truncated`

`method` | [modules/wire_capture.py:129](../../modules/wire_capture.py#L129)

```python
def truncated(self, digest: str) -> bool
```

Return True when a captured blob was clipped below its full size.

The store promises byte-for-byte reproduction, so a blob clipped at the
cap must advertise it rather than pass as complete.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `digest` | `str` |  | The traffic digest to check. |

**Returns:** `bool` - True when the blob for the digest was truncated on capture.

<a id="wirestore-fetch"></a>

#### `WireStore.fetch`

`method` | [modules/wire_capture.py:146](../../modules/wire_capture.py#L146)

```python
def fetch(self, digest: str) -> str | None
```

Return the full raw output for a digest, or None when absent.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `digest` | `str` |  | The traffic digest to retrieve. |

**Returns:** `str | None` - The decoded raw output, or None when no blob exists or it is
unreadable.

---
