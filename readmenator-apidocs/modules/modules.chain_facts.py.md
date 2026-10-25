# `modules.chain_facts`

> Source: [modules/chain_facts.py:1](../../modules/chain_facts.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Bridge chain run outputs into the FactStore.

Spools captured step outputs as tool-output text under
``sessions/chain_facts/<run_id>/`` and ingests them through
[`skills.lazyown_facts.FactStore`](skills.lazyown_facts.py.md#factstore) so credentials, shares, access
evidence and paths discovered inside a chain become queryable tokens for
the next chains and for the golden-path solver.

## Contents

- **Functions:** [`spool_chain_outputs`](#spool_chain_outputs)
- **Constants:** [`FACTS_SPOOL_DIRNAME`](#facts_spool_dirname)

## Functions

<a id="spool_chain_outputs"></a>

### `spool_chain_outputs`

`function` | [modules/chain_facts.py:24](../../modules/chain_facts.py#L24)

```python
def spool_chain_outputs(result: ChainRunResult, sessions_dir: str | Path | None = None, fact_store_factory: Callable[[], object] | None = None) -> int
```

Persist one chain run's outputs and ingest them as facts.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `result` | `ChainRunResult` |  | Completed [`ChainRunResult`](modules.chain_runner.py.md#chainrunresult) to bridge. |
| `sessions_dir` | `str \| Path \| None` | `None` | Sessions directory override; defaults to ``sessions/``. |
| `fact_store_factory` | `Callable[[], object] \| None` | `None` | Optional factory returning an object with `[`ingest_text`](skills.lazyown_facts.py.md#factstore-ingest_text)` and ``save``; used for tests to isolate I/O. |

**Returns:** `int` - Total number of facts deduplicated into the FactStore.

*Called by:* [`CommandAndControlMigratedCommandSet.do_apt_chain`](cli.commands.command_and_control_migrated.py.md#commandandcontrolmigratedcommandset-do_apt_chain), [`run_matrix`](modules.gym_matrix_runner.py.md#run_matrix)

---

## Constants

<a id="facts_spool_dirname"></a>

### `FACTS_SPOOL_DIRNAME`

`constant` | [modules/chain_facts.py:21](../../modules/chain_facts.py#L21)

```python
FACTS_SPOOL_DIRNAME = 'chain_facts'
```

---
