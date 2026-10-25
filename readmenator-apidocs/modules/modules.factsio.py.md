# `modules.factsio`

> Source: [modules/factsio.py:1](../../modules/factsio.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Canonical reader for the FactStore ``policy_facts.json`` document.

The on-disk truth is host-keyed and written by `[`skills.lazyown_facts`](skills.lazyown_facts.py.md)`
`[`FactStore.save`](skills.lazyown_facts.py.md#factstore-save)`::

    {
        "<ip>": {
            "services": [{"host": ..., "port": ..., "protocol": ...,
                          "service": ..., "product": ..., "version": ...,
                          "state": ...}],
            "credentials": [{"host": ..., "username": ..., "password": ...,
                             "source_file": ..., "hash_value": ...,
                             "hash_type": ...}],
            "vulnerabilities": [{"host": ..., "vuln_id": ..., "severity": ...,
                                 "title": ..., "url": ...}],
            "shares": [...], "access": [...], "paths": [...],
            "raw_files": [...], "os_hint": "..."
        },
        ...
    }

Historically some consumers assumed a wrapped legacy shape
(``{"hosts": {...}, "credentials": [...]}``). Every reader now goes
through [`load_policy_facts`](#load_policy_facts) so both shapes resolve to one
host-keyed canonical form; writers remain FactStore only.

## Contents

- **Functions:** [`load_policy_facts`](#load_policy_facts), [`canonical_policy_facts`](#canonical_policy_facts), [`iter_host_records`](#iter_host_records), [`iter_flat_facts`](#iter_flat_facts)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_factsio_py__load_policy_facts(["load_policy_facts"])
    n_modules_factsio_py__canonical_policy_facts(["canonical_policy_facts"])
    n_modules_factsio_py__load_policy_facts --> n_modules_factsio_py__canonical_policy_facts
```

## Functions

<a id="load_policy_facts"></a>

### `load_policy_facts`

`function` | [modules/factsio.py:39](../../modules/factsio.py#L39)

```python
def load_policy_facts(path: str | Path) -> dict[str, dict[str, Any]]
```

Load ``policy_facts.json`` into canonical host-keyed form.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` |  | Path to the facts document. |

**Returns:** `dict[str, dict[str, Any]]` - ``{ip: host_record}`` with only dict-typed records. Legacy
wrapped documents (``{"hosts": {...}}``) are unwrapped. Returns
an empty dict for missing, unreadable, or non-object documents.

*Calls:* [`canonical_policy_facts`](#canonical_policy_facts)

---

<a id="canonical_policy_facts"></a>

### `canonical_policy_facts`

`function` | [modules/factsio.py:61](../../modules/factsio.py#L61)

```python
def canonical_policy_facts(data: Any) -> dict[str, dict[str, Any]]
```

Project any legacy or canonical facts document to host-keyed form.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `Any` |  | Raw parsed JSON value. |

**Returns:** `dict[str, dict[str, Any]]` - Host-keyed mapping containing only dict-valued host records.
Wrapped documents resolve via their `[`hosts`](modules.state_manager.py.md#sessionsnapshot-hosts)` object first.

*Called by:* [`load_policy_facts`](#load_policy_facts), [`IntelligenceEngine.collect_from_factstore`](modules.intelligence_engine.py.md#intelligenceengine-collect_from_factstore), [`WorldModel.consume_policy_facts`](modules.world_model.py.md#worldmodel-consume_policy_facts)

---

<a id="iter_host_records"></a>

### `iter_host_records`

`function` `generator` | [modules/factsio.py:81](../../modules/factsio.py#L81)

```python
def iter_host_records(host_keyed: dict[str, dict[str, Any]]) -> Iterator[tuple[str, dict[str, Any]]]
```

Yield ``(ip, record)`` pairs from canonical host-keyed facts.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `host_keyed` | `dict[str, dict[str, Any]]` |  | Mapping produced by [`load_policy_facts`](#load_policy_facts). |

**Returns:** `Iterator[tuple[str, dict[str, Any]]]`

**Yields:** Tuples of host IP and its record.

---

<a id="iter_flat_facts"></a>

### `iter_flat_facts`

`function` `generator` | [modules/factsio.py:93](../../modules/factsio.py#L93)

```python
def iter_flat_facts(host_keyed: dict[str, dict[str, Any]]) -> Iterator[dict[str, Any]]
```

Yield one flat record per fact kind found in the host map.

Each record carries ``type`` (``service`` | ``credential`` |
``vulnerability`` | ``share`` | ``access`` | ``path``) and merges
the underlying fact fields. ``observable`` is derived per kind:
service name, ``user:password`` / hash, or `[`vuln_id`](skills.lazyown_facts.py.md#vulnerabilityfact-vuln_id)`.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `host_keyed` | `dict[str, dict[str, Any]]` |  | Mapping produced by [`load_policy_facts`](#load_policy_facts). |

**Returns:** `Iterator[dict[str, Any]]`

**Yields:** Flat fact records suitable for finding-style consumers.

---
