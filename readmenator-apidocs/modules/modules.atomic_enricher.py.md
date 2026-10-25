# `modules.atomic_enricher`

> Source: [modules/atomic_enricher.py:1](../../modules/atomic_enricher.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

atomic_enricher.py — Enrich techniques.parquet with structured derived columns.

Reads  parquets/techniques.parquet  (1690 Atomic Red Team tests, already present)
Writes parquets/techniques_enriched.parquet  (same rows + 6 new columns)

New columns
-----------
platform_list : List[str]   normalised platform list  ['linux','windows','macos',...]
scope         : str          'local' | 'remote' | 'elevated' | 'any'
has_prereqs   : bool         prereq_command is non-empty
complexity    : str          'low' | 'medium' | 'high'  (from command line count)
tactic_prefix : str          'T1003' extracted from mitre_id 'T1003.007'
keyword_tags  : List[str]    top meaningful tokens from name (stop-words removed)

Public API
----------
enrich()        -> pd.DataFrame   build enriched dataframe + save
load_enriched() -> pd.DataFrame   load existing enriched parquet (build if missing)

## Contents

- **Functions:** [`enrich`](#enrich), [`load_enriched`](#load_enriched), [`query_atomic`](#query_atomic)
- **Constants:** [`PARQUETS_DIR`](#parquets_dir), [`SRC_PARQUET`](#src_parquet), [`DST_PARQUET`](#dst_parquet)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_atomic_enricher_py__load_enriched(["load_enriched"])
    n_modules_atomic_enricher_py__enrich(["enrich"])
    n_modules_atomic_enricher_py__query_atomic(["query_atomic"])
    n_modules_atomic_enricher_py__load_enriched --> n_modules_atomic_enricher_py__enrich
    n_modules_atomic_enricher_py__query_atomic --> n_modules_atomic_enricher_py__load_enriched
```

## Functions

<a id="enrich"></a>

### `enrich`

`function` | [modules/atomic_enricher.py:173](../../modules/atomic_enricher.py#L173)

```python
def enrich(force: bool = False) -> pd.DataFrame
```

Build enriched parquet.

Skips if DST_PARQUET already exists (use force=True to rebuild). Returns the enriched DataFrame.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `force` | `bool` | `False` |  |

**Returns:** `pd.DataFrame`

**Raises**

- `FileNotFoundError`: (raised in the body, not documented)
- `ImportError`: (raised in the body, not documented)

*Called by:* [`load_enriched`](#load_enriched)

---

<a id="load_enriched"></a>

### `load_enriched`

`function` | [modules/atomic_enricher.py:215](../../modules/atomic_enricher.py#L215)

```python
def load_enriched() -> pd.DataFrame
```

Load enriched parquet, building it first if it doesn't exist.

Normalises list columns to plain Python lists after loading.

**Returns:** `pd.DataFrame`

**Raises**

- `ImportError`: (raised in the body, not documented)

*Calls:* [`enrich`](#enrich)

*Called by:* [`query_atomic`](#query_atomic)

---

<a id="query_atomic"></a>

### `query_atomic`

`function` | [modules/atomic_enricher.py:232](../../modules/atomic_enricher.py#L232)

```python
def query_atomic(keyword: str = '', mitre_id: str = '', platform: str = '', scope: str = '', has_prereqs: bool | None = None, complexity: str = '', limit: int = 10, include_command: bool = False) -> list[dict[str, Any]]
```

Structured query over the enriched Atomic Red Team technique catalogue.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `keyword` | `str` | `''` |  |
| `mitre_id` | `str` | `''` |  |
| `platform` | `str` | `''` |  |
| `scope` | `str` | `''` |  |
| `has_prereqs` | `bool \| None` | `None` |  |
| `complexity` | `str` | `''` |  |
| `limit` | `int` | `10` |  |
| `include_command` | `bool` | `False` |  |

**Returns:** `list[dict[str, Any]]` - id, name, mitre_id, tactic_prefix, platform_list, scope,
complexity, has_prereqs, keyword_tags,
description_preview (first 200 chars),
command_preview     (first 300 chars, only if include_command=True)

*Calls:* [`load_enriched`](#load_enriched)

---

## Constants

<a id="parquets_dir"></a>

### `PARQUETS_DIR`

`constant` | [modules/atomic_enricher.py:39](../../modules/atomic_enricher.py#L39)

```python
PARQUETS_DIR = Path(__file__).parent.parent / 'parquets'
```

---

<a id="src_parquet"></a>

### `SRC_PARQUET`

`constant` | [modules/atomic_enricher.py:40](../../modules/atomic_enricher.py#L40)

```python
SRC_PARQUET = PARQUETS_DIR / 'techniques.parquet'
```

---

<a id="dst_parquet"></a>

### `DST_PARQUET`

`constant` | [modules/atomic_enricher.py:41](../../modules/atomic_enricher.py#L41)

```python
DST_PARQUET = PARQUETS_DIR / 'techniques_enriched.parquet'
```

---
