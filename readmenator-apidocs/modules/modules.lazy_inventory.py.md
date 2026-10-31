# `modules.lazy_inventory`

> Source: [modules/lazy_inventory.py:1](../../modules/lazy_inventory.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Host-reported inventory for LazyOwn.

The honest version source: the host itself lists the packages it runs.
This contract renders one read-only collector blob per platform (posix
``sh`` and Windows PowerShell), parses its plain output back into
package/version entries, and promotes them to [`Sighting`](modules.lazy_feedmatch.py.md#sighting) rows with
``source: "host"`` so the feed matcher can grade services with evidence
no banner could give (a distro backport never changes the banner, the
package table does).

The blob never mutates the host: every command is a read-only query.

## Contents

- **Functions:** [`inventory_blob`](#inventory_blob), [`parse_blob_output`](#parse_blob_output), [`to_sightings`](#to_sightings), [`os_platform_of`](#os_platform_of)
- **Constants:** [`SPOOL_DIR`](#spool_dir), [`SOURCE_HOST`](#source_host), [`LINUX_BLOB`](#linux_blob), [`WINDOWS_BLOB`](#windows_blob), [`MAX_ENTRIES`](#max_entries)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_lazy_inventory_py__to_sightings(["to_sightings"])
    n_modules_lazy_feedmatch_py__Sighting["lazy_feedmatch.Sighting"]
    n_modules_lazy_inventory_py__to_sightings -.-> n_modules_lazy_feedmatch_py__Sighting
```

## Functions

<a id="inventory_blob"></a>

### `inventory_blob`

`function` | [modules/lazy_inventory.py:49](../../modules/lazy_inventory.py#L49)

```python
def inventory_blob(platform: str = 'linux') -> str
```

Return the read-only collector blob for one platform.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `platform` | `str` | `'linux'` | ``linux`` (default) or ``windows``. |

**Returns:** `str` - The blob text; an empty string for an unknown platform.

---

<a id="parse_blob_output"></a>

### `parse_blob_output`

`function` | [modules/lazy_inventory.py:61](../../modules/lazy_inventory.py#L61)

```python
def parse_blob_output(text: str, platform: str = 'linux') -> list[dict]
```

Parse the collector output into package entries.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `text` | `str` |  | Raw stdout captured from the blob. |
| `platform` | `str` | `'linux'` | ``linux`` or ``windows``. |

**Returns:** `list[dict]` - ``[{"product", "version", "source": "host"}]`` entries, capped at
[`MAX_ENTRIES`](#max_entries). Garbage lines are skipped silently; a done
marker stops parsing to ignore anything the shell appended.

---

<a id="to_sightings"></a>

### `to_sightings`

`function` | [modules/lazy_inventory.py:133](../../modules/lazy_inventory.py#L133)

```python
def to_sightings(entries: list[dict], host: str = '') -> list[Sighting]
```

Project package entries into host-source sightings.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entries` | `list[dict]` |  | Parsed package rows from [`parse_blob_output`](#parse_blob_output). |
| `host` | `str` | `''` | Address reporting the inventory. |

**Returns:** `list[Sighting]` - One [`Sighting`](modules.lazy_feedmatch.py.md#sighting) per entry with ``source`` set to
``"host"``, port zero (packages are not endpoints).

*Calls:* [`Sighting`](modules.lazy_feedmatch.py.md#sighting)

---

<a id="os_platform_of"></a>

### `os_platform_of`

`function` | [modules/lazy_inventory.py:157](../../modules/lazy_inventory.py#L157)

```python
def os_platform_of(entries: list[dict]) -> str
```

Detect the inventory platform from the entries' own os tag.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entries` | `list[dict]` |  | Parsed package rows. |

**Returns:** `str` - ``linux`` or ``windows`` (default ``linux``).

---

## Constants

<a id="spool_dir"></a>

### `SPOOL_DIR`

`constant` | [modules/lazy_inventory.py:21](../../modules/lazy_inventory.py#L21)

```python
SPOOL_DIR = BASE_DIR / 'sessions' / 'inventory'
```

---

<a id="source_host"></a>

### `SOURCE_HOST`

`constant` | [modules/lazy_inventory.py:22](../../modules/lazy_inventory.py#L22)

```python
SOURCE_HOST = 'host'
```

---

<a id="linux_blob"></a>

### `LINUX_BLOB`

`constant` | [modules/lazy_inventory.py:24](../../modules/lazy_inventory.py#L24)

```python
LINUX_BLOB
```

---

<a id="windows_blob"></a>

### `WINDOWS_BLOB`

`constant` | [modules/lazy_inventory.py:34](../../modules/lazy_inventory.py#L34)

```python
WINDOWS_BLOB
```

---

<a id="max_entries"></a>

### `MAX_ENTRIES`

`constant` | [modules/lazy_inventory.py:46](../../modules/lazy_inventory.py#L46)

```python
MAX_ENTRIES = 5000
```

---
