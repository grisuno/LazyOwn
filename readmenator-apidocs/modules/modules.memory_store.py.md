# `modules.memory_store`

> Source: [modules/memory_store.py:1](../../modules/memory_store.py#L1) | language `py` | coverage 3.4% | [API index](../index.md)

memory_store.py — Episodic memory for the LazyOwn auto_loop.

Stores (command, output, findings, host, tool, success) per session and
retrieves relevant past experiences via SQLite FTS5 keyword search.
Optionally uses numpy for cosine similarity when available.

## Contents

- **Classes:** [`MemoryEntry`](#memoryentry), [`StorageBackend`](#storagebackend), [`SQLiteBackend`](#sqlitebackend), [`MemoryStore`](#memorystore)
- **Functions:** [`get_memory_store`](#get_memory_store), [`remember`](#remember), [`recall`](#recall)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class MemoryEntry
    MemoryEntry : str session_id
    MemoryEntry : str host
    MemoryEntry : str tool
    MemoryEntry : str command
    MemoryEntry : str output_snippet
    MemoryEntry : str findings_json
    MemoryEntry : bool success
    MemoryEntry : float ts
    MemoryEntry : bytes  None embedding
    MemoryEntry : int  None id
    class StorageBackend
    StorageBackend : save()
    StorageBackend : search()
    StorageBackend : by_host()
    StorageBackend : by_service()
    StorageBackend : all_entries()
    StorageBackend : close()
    class SQLiteBackend
    SQLiteBackend : __init__()
    SQLiteBackend : save()
    SQLiteBackend : search()
    SQLiteBackend : by_host()
    SQLiteBackend : by_service()
    SQLiteBackend : all_entries()
    SQLiteBackend : stats_raw()
    SQLiteBackend : close()
    class MemoryStore
    MemoryStore : __init__()
    MemoryStore : remember()
    MemoryStore : recall()
    MemoryStore : recall_by_host()
    MemoryStore : recall_for_service()
    MemoryStore : stats()
    MemoryStore : export_finetuning_dataset()
    StorageBackend <|-- SQLiteBackend
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_memory_store_py__MemoryStore_remember(["MemoryStore.remember"])
    n_modules_memory_store_py__MemoryEntry(["MemoryEntry"])
    n_modules_memory_store_py__get_memory_store(["get_memory_store"])
    n_modules_memory_store_py__MemoryStore___init__(["MemoryStore.__init__"])
    n_modules_memory_store_py__SQLiteBackend___init__(["SQLiteBackend.__init__"])
    n_modules_memory_store_py__remember(["remember"])
    n_modules_memory_store_py__recall(["recall"])
    n_modules_memory_store_py__MemoryStore_remember --> n_modules_memory_store_py__MemoryEntry
    n_modules_memory_store_py__get_memory_store --> n_modules_memory_store_py__MemoryStore___init__
    n_modules_memory_store_py__get_memory_store --> n_modules_memory_store_py__SQLiteBackend___init__
    n_modules_memory_store_py__remember --> n_modules_memory_store_py__get_memory_store
    n_modules_memory_store_py__recall --> n_modules_memory_store_py__get_memory_store
```

## Classes

<a id="memoryentry"></a>

### `MemoryEntry`

`class` `dataclass` | [modules/memory_store.py:81](../../modules/memory_store.py#L81)

Decorators: `@dataclass`

```python
class MemoryEntry
```

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`session_id`](#memoryentry-session_id) | `str` |  |  |
| [`host`](#memoryentry-host) | `str` |  |  |
| [`tool`](#memoryentry-tool) | `str` |  |  |
| [`command`](#memoryentry-command) | `str` |  |  |
| [`output_snippet`](#memoryentry-output_snippet) | `str` |  |  |
| [`findings_json`](#memoryentry-findings_json) | `str` |  |  |
| [`success`](#memoryentry-success) | `bool` |  |  |
| [`ts`](#memoryentry-ts) | `float` |  |  |
| [`embedding`](#memoryentry-embedding) | `bytes \| None` | `field(default=None, repr=False)` |  |
| [`id`](#memoryentry-id) | `int \| None` | `field(default=None, repr=False)` |  |

---

<a id="storagebackend"></a>

### `StorageBackend`

`class` `abstract` | [modules/memory_store.py:94](../../modules/memory_store.py#L94)

```python
class StorageBackend(ABC)
```

Bases: `ABC`

Subclasses: [`SQLiteBackend`](#sqlitebackend)

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`save`](#storagebackend-save) | method |  |
| [`search`](#storagebackend-search) | method |  |
| [`by_host`](#storagebackend-by_host) | method |  |
| [`by_service`](#storagebackend-by_service) | method |  |
| [`all_entries`](#storagebackend-all_entries) | method |  |
| [`close`](#storagebackend-close) | method |  |

<a id="storagebackend-save"></a>

#### `StorageBackend.save`

`method` `abstract` | [modules/memory_store.py:96](../../modules/memory_store.py#L96)

Decorators: `@abstractmethod`

```python
def save(self, entry: MemoryEntry) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entry` | `MemoryEntry` |  |  |

<a id="storagebackend-search"></a>

#### `StorageBackend.search`

`method` `abstract` | [modules/memory_store.py:99](../../modules/memory_store.py#L99)

Decorators: `@abstractmethod`

```python
def search(self, query: str, top_k: int) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  |  |
| `top_k` | `int` |  |  |

**Returns:** `list[MemoryEntry]`

<a id="storagebackend-by_host"></a>

#### `StorageBackend.by_host`

`method` `abstract` | [modules/memory_store.py:102](../../modules/memory_store.py#L102)

Decorators: `@abstractmethod`

```python
def by_host(self, host: str, top_k: int) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `host` | `str` |  |  |
| `top_k` | `int` |  |  |

**Returns:** `list[MemoryEntry]`

<a id="storagebackend-by_service"></a>

#### `StorageBackend.by_service`

`method` `abstract` | [modules/memory_store.py:105](../../modules/memory_store.py#L105)

Decorators: `@abstractmethod`

```python
def by_service(self, service: str, top_k: int) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `service` | `str` |  |  |
| `top_k` | `int` |  |  |

**Returns:** `list[MemoryEntry]`

<a id="storagebackend-all_entries"></a>

#### `StorageBackend.all_entries`

`method` `abstract` | [modules/memory_store.py:108](../../modules/memory_store.py#L108)

Decorators: `@abstractmethod`

```python
def all_entries(self, limit: int) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `limit` | `int` |  |  |

**Returns:** `list[MemoryEntry]`

<a id="storagebackend-close"></a>

#### `StorageBackend.close`

`method` `abstract` | [modules/memory_store.py:111](../../modules/memory_store.py#L111)

Decorators: `@abstractmethod`

```python
def close(self) -> None
```

---

<a id="sqlitebackend"></a>

### `SQLiteBackend`

`class` | [modules/memory_store.py:129](../../modules/memory_store.py#L129)

```python
class SQLiteBackend(StorageBackend)
```

Bases: [`StorageBackend`](#storagebackend)

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#sqlitebackend-__init__) | constructor |  |
| [`save`](#sqlitebackend-save) | method |  |
| [`search`](#sqlitebackend-search) | method |  |
| [`by_host`](#sqlitebackend-by_host) | method |  |
| [`by_service`](#sqlitebackend-by_service) | method |  |
| [`all_entries`](#sqlitebackend-all_entries) | method |  |
| [`stats_raw`](#sqlitebackend-stats_raw) | method |  |
| [`close`](#sqlitebackend-close) | method |  |

<a id="sqlitebackend-__init__"></a>

#### `SQLiteBackend.__init__`

`constructor` | [modules/memory_store.py:130](../../modules/memory_store.py#L130)

```python
def __init__(self, db_path: Path = _DB_PATH) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `db_path` | `Path` | `_DB_PATH` |  |

*Called by:* [`get_memory_store`](#get_memory_store)

<a id="sqlitebackend-save"></a>

#### `SQLiteBackend.save`

`method` | [modules/memory_store.py:145](../../modules/memory_store.py#L145)

```python
def save(self, entry: MemoryEntry) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entry` | `MemoryEntry` |  |  |

<a id="sqlitebackend-search"></a>

#### `SQLiteBackend.search`

`method` | [modules/memory_store.py:177](../../modules/memory_store.py#L177)

```python
def search(self, query: str, top_k: int) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  |  |
| `top_k` | `int` |  |  |

**Returns:** `list[MemoryEntry]`

<a id="sqlitebackend-by_host"></a>

#### `SQLiteBackend.by_host`

`method` | [modules/memory_store.py:189](../../modules/memory_store.py#L189)

```python
def by_host(self, host: str, top_k: int) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `host` | `str` |  |  |
| `top_k` | `int` |  |  |

**Returns:** `list[MemoryEntry]`

<a id="sqlitebackend-by_service"></a>

#### `SQLiteBackend.by_service`

`method` | [modules/memory_store.py:200](../../modules/memory_store.py#L200)

```python
def by_service(self, service: str, top_k: int) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `service` | `str` |  |  |
| `top_k` | `int` |  |  |

**Returns:** `list[MemoryEntry]`

<a id="sqlitebackend-all_entries"></a>

#### `SQLiteBackend.all_entries`

`method` | [modules/memory_store.py:212](../../modules/memory_store.py#L212)

```python
def all_entries(self, limit: int) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `limit` | `int` |  |  |

**Returns:** `list[MemoryEntry]`

<a id="sqlitebackend-stats_raw"></a>

#### `SQLiteBackend.stats_raw`

`method` | [modules/memory_store.py:222](../../modules/memory_store.py#L222)

```python
def stats_raw(self) -> dict
```

**Returns:** `dict`

<a id="sqlitebackend-close"></a>

#### `SQLiteBackend.close`

`method` | [modules/memory_store.py:229](../../modules/memory_store.py#L229)

```python
def close(self) -> None
```

---

<a id="memorystore"></a>

### `MemoryStore`

`class` | [modules/memory_store.py:234](../../modules/memory_store.py#L234)

```python
class MemoryStore
```

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#memorystore-__init__) | constructor |  |
| [`remember`](#memorystore-remember) | method |  |
| [`recall`](#memorystore-recall) | method |  |
| [`recall_by_host`](#memorystore-recall_by_host) | method |  |
| [`recall_for_service`](#memorystore-recall_for_service) | method |  |
| [`stats`](#memorystore-stats) | method |  |
| [`export_finetuning_dataset`](#memorystore-export_finetuning_dataset) | method |  |

<a id="memorystore-__init__"></a>

#### `MemoryStore.__init__`

`constructor` | [modules/memory_store.py:237](../../modules/memory_store.py#L237)

```python
def __init__(self, backend: StorageBackend) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `backend` | `StorageBackend` |  |  |

*Called by:* [`get_memory_store`](#get_memory_store)

<a id="memorystore-remember"></a>

#### `MemoryStore.remember`

`method` | [modules/memory_store.py:240](../../modules/memory_store.py#L240)

```python
def remember(self, session_id: str, host: str, tool: str, command: str, output: str, findings: object, success: bool) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `session_id` | `str` |  |  |
| `host` | `str` |  |  |
| `tool` | `str` |  |  |
| `command` | `str` |  |  |
| `output` | `str` |  |  |
| `findings` | `object` |  |  |
| `success` | `bool` |  |  |

*Calls:* [`MemoryEntry`](#memoryentry)

<a id="memorystore-recall"></a>

#### `MemoryStore.recall`

`method` | [modules/memory_store.py:267](../../modules/memory_store.py#L267)

```python
def recall(self, query: str, top_k: int = 5) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  |  |
| `top_k` | `int` | `5` |  |

**Returns:** `list[MemoryEntry]`

<a id="memorystore-recall_by_host"></a>

#### `MemoryStore.recall_by_host`

`method` | [modules/memory_store.py:270](../../modules/memory_store.py#L270)

```python
def recall_by_host(self, host: str, top_k: int = 10) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `host` | `str` |  |  |
| `top_k` | `int` | `10` |  |

**Returns:** `list[MemoryEntry]`

<a id="memorystore-recall_for_service"></a>

#### `MemoryStore.recall_for_service`

`method` | [modules/memory_store.py:273](../../modules/memory_store.py#L273)

```python
def recall_for_service(self, service_name: str, top_k: int = 5) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `service_name` | `str` |  |  |
| `top_k` | `int` | `5` |  |

**Returns:** `list[MemoryEntry]`

<a id="memorystore-stats"></a>

#### `MemoryStore.stats`

`method` | [modules/memory_store.py:276](../../modules/memory_store.py#L276)

```python
def stats(self) -> dict
```

**Returns:** `dict`

<a id="memorystore-export_finetuning_dataset"></a>

#### `MemoryStore.export_finetuning_dataset`

`method` | [modules/memory_store.py:284](../../modules/memory_store.py#L284)

```python
def export_finetuning_dataset(self, path: Path) -> Path
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `Path` |  |  |

**Returns:** `Path`

---

## Functions

<a id="get_memory_store"></a>

### `get_memory_store`

`function` | [modules/memory_store.py:303](../../modules/memory_store.py#L303)

```python
def get_memory_store() -> MemoryStore
```

**Returns:** `MemoryStore`

*Calls:* [`MemoryStore.__init__`](#memorystore-__init__), [`SQLiteBackend.__init__`](#sqlitebackend-__init__)

*Called by:* [`recall`](#recall), [`remember`](#remember)

---

<a id="remember"></a>

### `remember`

`function` | [modules/memory_store.py:312](../../modules/memory_store.py#L312)

```python
def remember(session_id: str, host: str, tool: str, command: str, output: str, findings: object, success: bool) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `session_id` | `str` |  |  |
| `host` | `str` |  |  |
| `tool` | `str` |  |  |
| `command` | `str` |  |  |
| `output` | `str` |  |  |
| `findings` | `object` |  |  |
| `success` | `bool` |  |  |

*Calls:* [`get_memory_store`](#get_memory_store)

---

<a id="recall"></a>

### `recall`

`function` | [modules/memory_store.py:324](../../modules/memory_store.py#L324)

```python
def recall(query: str, top_k: int = 5) -> list[MemoryEntry]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  |  |
| `top_k` | `int` | `5` |  |

**Returns:** `list[MemoryEntry]`

*Calls:* [`get_memory_store`](#get_memory_store)

---
