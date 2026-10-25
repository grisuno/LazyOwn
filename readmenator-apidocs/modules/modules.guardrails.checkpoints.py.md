# `modules.guardrails.checkpoints`

> Source: [modules/guardrails/checkpoints.py:1](../../modules/guardrails/checkpoints.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Checkpoint ledger with warm-restart recovery.

Checkpoints capture the caller's meaningful state snapshot before risky
executions. A warm restart purges non-critical runtime contexts, keeps
core state intact and restores the latest core checkpoint; it never
raises and never resets the whole application.

## Contents

- **Classes:** [`CheckpointLedger`](#checkpointledger)
- **Constants:** [`CHECKPOINT_HISTORY_PER_KEY`](#checkpoint_history_per_key)

## Classes

<a id="checkpointledger"></a>

### `CheckpointLedger`

`class` | [modules/guardrails/checkpoints.py:18](../../modules/guardrails/checkpoints.py#L18)

```python
class CheckpointLedger
```

Bounded per-key checkpoint history with warm-restart restore.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#checkpointledger-__init__) | constructor | Create an empty ledger. |
| [`capture`](#checkpointledger-capture) | method | Store one immutable snapshot for a key. |
| [`restore`](#checkpointledger-restore) | method | Return the latest snapshot for a key, or None when missing. |
| [`keys`](#checkpointledger-keys) | method | Return the tracked checkpoint keys. |
| [`warm_restart`](#checkpointledger-warm_restart) | method | Purge non-core runtime contexts and restore the core snapshot. |
| [`describe`](#checkpointledger-describe) | method | Return the ledger state for the admin console. |

<a id="checkpointledger-__init__"></a>

#### `CheckpointLedger.__init__`

`constructor` | [modules/guardrails/checkpoints.py:21](../../modules/guardrails/checkpoints.py#L21)

```python
def __init__(self, history: int = CHECKPOINT_HISTORY_PER_KEY) -> None
```

Create an empty ledger.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `history` | `int` | `CHECKPOINT_HISTORY_PER_KEY` | Snapshot history retained per key (>= 1). |

*Called by:* [`GuardHarness.__init__`](modules.guardrails.harness.py.md#guardharness-__init__)

<a id="checkpointledger-capture"></a>

#### `CheckpointLedger.capture`

`method` | [modules/guardrails/checkpoints.py:33](../../modules/guardrails/checkpoints.py#L33)

```python
def capture(self, key: str, state: Any) -> bool
```

Store one immutable snapshot for a key.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `key` | `str` |  | Checkpoint identity (for example ``loop.core_round``). |
| `state` | `Any` |  | JSON-serializable snapshot; deep-copied on capture. |

**Returns:** `bool` - True when the snapshot was stored.

*Called by:* [`GuardHarness.run_guarded`](modules.guardrails.harness.py.md#guardharness-run_guarded)

<a id="checkpointledger-restore"></a>

#### `CheckpointLedger.restore`

`method` | [modules/guardrails/checkpoints.py:51](../../modules/guardrails/checkpoints.py#L51)

```python
def restore(self, key: str) -> Any
```

Return the latest snapshot for a key, or None when missing.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `key` | `str` |  |  |

**Returns:** `Any`

<a id="checkpointledger-keys"></a>

#### `CheckpointLedger.keys`

`method` | [modules/guardrails/checkpoints.py:59](../../modules/guardrails/checkpoints.py#L59)

```python
def keys(self) -> list[str]
```

Return the tracked checkpoint keys.

**Returns:** `list[str]`

<a id="checkpointledger-warm_restart"></a>

#### `CheckpointLedger.warm_restart`

`method` | [modules/guardrails/checkpoints.py:64](../../modules/guardrails/checkpoints.py#L64)

```python
def warm_restart(self, core_key: str = '') -> dict[str, Any]
```

Purge non-core runtime contexts and restore the core snapshot.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `core_key` | `str` | `''` | Optional checkpoint key to restore from. |

**Returns:** `dict[str, Any]` - A summary with restored flag, payload and restart counter.

*Called by:* [`GuardHarness.warm_restart`](modules.guardrails.harness.py.md#guardharness-warm_restart)

<a id="checkpointledger-describe"></a>

#### `CheckpointLedger.describe`

`method` | [modules/guardrails/checkpoints.py:92](../../modules/guardrails/checkpoints.py#L92)

```python
def describe(self) -> dict[str, Any]
```

Return the ledger state for the admin console.

**Returns:** `dict[str, Any]`

---

## Constants

<a id="checkpoint_history_per_key"></a>

### `CHECKPOINT_HISTORY_PER_KEY`

`constant` | [modules/guardrails/checkpoints.py:15](../../modules/guardrails/checkpoints.py#L15)

```python
CHECKPOINT_HISTORY_PER_KEY: int = 3
```

---
