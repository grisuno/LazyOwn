# `modules.config_store`

> Source: [modules/config_store.py:1](../../modules/config_store.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Thread-safe singleton facade over core.config for payload.json.

Contract: preserves the get_config/set_config/reload_config API while
delegating all file parsing and atomic persistence to core.config. This
removes the duplicated JSON load and dump logic without changing behavior.

## Contents

- **Functions:** [`init`](#init), [`get_config`](#get_config), [`set_config`](#set_config), [`set_config_dict`](#set_config_dict), [`reload_config`](#reload_config), [`stop_watcher`](#stop_watcher)

## Functions

<a id="init"></a>

### `init`

`function` | [modules/config_store.py:36](../../modules/config_store.py#L36)

```python
def init(path: str | Path = _DEFAULT_PATH, watch: bool = False) -> None
```

Initialise the config store (idempotent).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` | `_DEFAULT_PATH` |  |
| `watch` | `bool` | `False` |  |

---

<a id="get_config"></a>

### `get_config`

`function` | [modules/config_store.py:53](../../modules/config_store.py#L53)

```python
def get_config(key: str = '', default: Any = None) -> Any
```

Return a config value (or the full dict when *key* is empty).

Always returns a deep copy so callers cannot mutate the cache.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `key` | `str` | `''` |  |
| `default` | `Any` | `None` |  |

**Returns:** `Any`

---

<a id="set_config"></a>

### `set_config`

`function` | [modules/config_store.py:66](../../modules/config_store.py#L66)

```python
def set_config(**kwargs: Any) -> None
```

Update one or more keys and persist to disk atomically.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `**kwargs` | `Any` |  |  |

**Example**

```python
set_config(rhost="10.10.10.10", lport=4444)
```

---

<a id="set_config_dict"></a>

### `set_config_dict`

`function` | [modules/config_store.py:80](../../modules/config_store.py#L80)

```python
def set_config_dict(updates: dict[str, Any]) -> None
```

Bulk-update from a dict and persist to disk.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `updates` | `dict[str, Any]` |  |  |

---

<a id="reload_config"></a>

### `reload_config`

`function` | [modules/config_store.py:90](../../modules/config_store.py#L90)

```python
def reload_config() -> None
```

Force reload from disk (discards in-memory changes).

---

<a id="stop_watcher"></a>

### `stop_watcher`

`function` | [modules/config_store.py:96](../../modules/config_store.py#L96)

```python
def stop_watcher() -> None
```

Stop the file-watcher background thread (if running).

---
