# `modules.module_registry`

> Source: [modules/module_registry.py:1](../../modules/module_registry.py#L1) | language `py` | coverage 87.5% | [API index](../index.md)

Unified module registry for LazyOwn — catalog, search, use/run workflow.

Scans ``lazyaddons/`` (YAML), ``plugins/`` (Lua + YAML), ``modules/``
(Python), ``tools/`` (pwntomate), and ``playbooks/`` for all discoverable
modules. Every module is indexed with its metadata (name, author, version,
category, description, params) for ``show exploits`` / ``search`` /
``info`` / ``use`` / ``run``.

## Contents

- **Classes:** [`ModuleInfo`](#moduleinfo), [`ModuleRegistry`](#moduleregistry)
- **Functions:** [`format_module_table`](#format_module_table), [`format_module_detail`](#format_module_detail)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class ModuleInfo
    ModuleInfo : __init__()
    ModuleInfo : to_dict()
    class ModuleRegistry
    ModuleRegistry : __init__()
    ModuleRegistry : get_instance()
    ModuleRegistry : scan()
    ModuleRegistry : rescan()
    ModuleRegistry : get()
    ModuleRegistry : search()
    ModuleRegistry : deprecated_modules()
    ModuleRegistry : by_type()
    ModuleRegistry : summary()
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_module_registry_py__ModuleRegistry_rescan(["ModuleRegistry.rescan"])
    n_modules_module_registry_py__ModuleRegistry_scan(["ModuleRegistry.scan"])
    n_modules_module_registry_py__ModuleRegistry_get(["ModuleRegistry.get"])
    n_modules_module_registry_py__ModuleRegistry_search(["ModuleRegistry.search"])
    n_modules_module_registry_py__ModuleRegistry_deprecated_modules(["ModuleRegistry.deprecated_modules"])
    n_modules_module_registry_py__ModuleRegistry_by_type(["ModuleRegistry.by_type"])
    n_modules_module_registry_py__ModuleRegistry_summary(["ModuleRegistry.summary"])
    n_modules_module_registry_py__ModuleRegistry_rescan --> n_modules_module_registry_py__ModuleRegistry_scan
    n_modules_module_registry_py__ModuleRegistry_get --> n_modules_module_registry_py__ModuleRegistry_scan
    n_modules_module_registry_py__ModuleRegistry_search --> n_modules_module_registry_py__ModuleRegistry_scan
    n_modules_module_registry_py__ModuleRegistry_deprecated_modules --> n_modules_module_registry_py__ModuleRegistry_scan
    n_modules_module_registry_py__ModuleRegistry_by_type --> n_modules_module_registry_py__ModuleRegistry_search
    n_modules_module_registry_py__ModuleRegistry_summary --> n_modules_module_registry_py__ModuleRegistry_scan
```

## Classes

<a id="moduleinfo"></a>

### `ModuleInfo`

`class` | [modules/module_registry.py:150](../../modules/module_registry.py#L150)

```python
class ModuleInfo
```

Metadata for a single discoverable module.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#moduleinfo-__init__) | constructor |  |
| [`to_dict`](#moduleinfo-to_dict) | method |  |

<a id="moduleinfo-__init__"></a>

#### `ModuleInfo.__init__`

`constructor` | [modules/module_registry.py:172](../../modules/module_registry.py#L172)

```python
def __init__(self, name: str, module_type: str = 'auxiliary', author: str = '', version: str = '', description: str = '', category: str = '', path: str = '', source: str = 'yaml', params: list[dict[str, Any]] | None = None, enabled: bool = True, deprecated: bool = False, replaced_by: str = '', deprecation_message: str = '') -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `module_type` | `str` | `'auxiliary'` |  |
| `author` | `str` | `''` |  |
| `version` | `str` | `''` |  |
| `description` | `str` | `''` |  |
| `category` | `str` | `''` |  |
| `path` | `str` | `''` |  |
| `source` | `str` | `'yaml'` |  |
| `params` | `list[dict[str, Any]] \| None` | `None` |  |
| `enabled` | `bool` | `True` |  |
| `deprecated` | `bool` | `False` |  |
| `replaced_by` | `str` | `''` |  |
| `deprecation_message` | `str` | `''` |  |

<a id="moduleinfo-to_dict"></a>

#### `ModuleInfo.to_dict`

`method` | [modules/module_registry.py:202](../../modules/module_registry.py#L202)

```python
def to_dict(self) -> dict[str, Any]
```

**Returns:** `dict[str, Any]`

---

<a id="moduleregistry"></a>

### `ModuleRegistry`

`class` | [modules/module_registry.py:223](../../modules/module_registry.py#L223)

```python
class ModuleRegistry
```

Scans and indexes all discoverable modules in the framework.

The registry is a singleton per process — call
[`ModuleRegistry.get_instance`](#moduleregistry-get_instance) or just construct one and reuse it.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_dir` |  |  | Root directory of the LazyOwn project. |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#moduleregistry-__init__) | constructor |  |
| [`get_instance`](#moduleregistry-get_instance) | classmethod | Return the singleton registry instance. |
| [`scan`](#moduleregistry-scan) | method | Scan all module directories and return the full list. |
| [`rescan`](#moduleregistry-rescan) | method | Force a full rescan and return modules. |
| [`get`](#moduleregistry-get) | method | Get a module by name. |
| [`search`](#moduleregistry-search) | method | Search indexed modules. |
| [`deprecated_modules`](#moduleregistry-deprecated_modules) | method | Return all deprecated modules. |
| [`by_type`](#moduleregistry-by_type) | method | Shorthand for ``search(module_type=module_type)``. |
| [`summary`](#moduleregistry-summary) | method | Return counts by module type. |

<a id="moduleregistry-__init__"></a>

#### `ModuleRegistry.__init__`

`constructor` | [modules/module_registry.py:235](../../modules/module_registry.py#L235)

```python
def __init__(self, base_dir: str | Path | None = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_dir` | `str \| Path \| None` | `None` | Root directory of the LazyOwn project. |

<a id="moduleregistry-get_instance"></a>

#### `ModuleRegistry.get_instance`

`classmethod` | [modules/module_registry.py:241](../../modules/module_registry.py#L241)

Decorators: `@classmethod`

```python
def get_instance(cls, base_dir: str | Path | None = None) -> ModuleRegistry
```

Return the singleton registry instance.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_dir` | `str \| Path \| None` | `None` |  |

**Returns:** `ModuleRegistry`

<a id="moduleregistry-scan"></a>

#### `ModuleRegistry.scan`

`method` | [modules/module_registry.py:247](../../modules/module_registry.py#L247)

```python
def scan(self) -> list[ModuleInfo]
```

Scan all module directories and return the full list.

**Returns:** `list[ModuleInfo]`

*Called by:* [`ModuleRegistry.deprecated_modules`](#moduleregistry-deprecated_modules), [`ModuleRegistry.get`](#moduleregistry-get), [`ModuleRegistry.rescan`](#moduleregistry-rescan), [`ModuleRegistry.search`](#moduleregistry-search), [`ModuleRegistry.summary`](#moduleregistry-summary)

<a id="moduleregistry-rescan"></a>

#### `ModuleRegistry.rescan`

`method` | [modules/module_registry.py:260](../../modules/module_registry.py#L260)

```python
def rescan(self) -> list[ModuleInfo]
```

Force a full rescan and return modules.

**Returns:** `list[ModuleInfo]`

*Calls:* [`ModuleRegistry.scan`](#moduleregistry-scan)

<a id="moduleregistry-get"></a>

#### `ModuleRegistry.get`

`method` | [modules/module_registry.py:269](../../modules/module_registry.py#L269)

```python
def get(self, name: str) -> ModuleInfo | None
```

Get a module by name.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `ModuleInfo | None`

*Calls:* [`ModuleRegistry.scan`](#moduleregistry-scan)

<a id="moduleregistry-search"></a>

#### `ModuleRegistry.search`

`method` | [modules/module_registry.py:275](../../modules/module_registry.py#L275)

```python
def search(self, query: str = '', module_type: str | None = None, category: str | None = None, enabled_only: bool = True, include_deprecated: bool = False) -> list[ModuleInfo]
```

Search indexed modules.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | `''` | Free-text search in name, description, author. |
| `module_type` | `str \| None` | `None` | Filter by type (``exploit``, `[`scanner`](contrib.legacy.lazycam.py.md#rtspscanner-scanner)`, ...). |
| `category` | `str \| None` | `None` | Filter by kill-chain category. |
| `enabled_only` | `bool` | `True` | Only return enabled modules. |
| `include_deprecated` | `bool` | `False` | Include deprecated modules in results. |

**Returns:** `list[ModuleInfo]` - List of matching [`ModuleInfo`](#moduleinfo).

*Calls:* [`ModuleRegistry.scan`](#moduleregistry-scan)

*Called by:* [`ModuleRegistry.by_type`](#moduleregistry-by_type)

<a id="moduleregistry-deprecated_modules"></a>

#### `ModuleRegistry.deprecated_modules`

`method` | [modules/module_registry.py:315](../../modules/module_registry.py#L315)

```python
def deprecated_modules(self) -> list[ModuleInfo]
```

Return all deprecated modules.

**Returns:** `list[ModuleInfo]`

*Calls:* [`ModuleRegistry.scan`](#moduleregistry-scan)

<a id="moduleregistry-by_type"></a>

#### `ModuleRegistry.by_type`

`method` | [modules/module_registry.py:321](../../modules/module_registry.py#L321)

```python
def by_type(self, module_type: str) -> list[ModuleInfo]
```

Shorthand for ``search(module_type=module_type)``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `module_type` | `str` |  |  |

**Returns:** `list[ModuleInfo]`

*Calls:* [`ModuleRegistry.search`](#moduleregistry-search)

<a id="moduleregistry-summary"></a>

#### `ModuleRegistry.summary`

`method` | [modules/module_registry.py:325](../../modules/module_registry.py#L325)

```python
def summary(self) -> dict[str, int]
```

Return counts by module type.

**Returns:** `dict[str, int]`

*Calls:* [`ModuleRegistry.scan`](#moduleregistry-scan)

---

## Functions

<a id="format_module_table"></a>

### `format_module_table`

`function` | [modules/module_registry.py:542](../../modules/module_registry.py#L542)

```python
def format_module_table(modules: list[ModuleInfo], cols: tuple[str, ...] = ('name', 'type', 'author', 'description')) -> str
```

Format a list of modules as an aligned text table.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `modules` | `list[ModuleInfo]` |  | Module list to format. |
| `cols` | `tuple[str, ...]` | `('name', 'type', 'author', 'description')` | Column keys to include (in order). Valid keys: ``id``, ``name``, ``type``, ``author``, ``version``, ``description``. |

**Returns:** `str` - Multi-line string with aligned columns.

*Called by:* [`ModuleManagerCommandSet.do_search`](cli.commands.module_manager.py.md#modulemanagercommandset-do_search)

---

<a id="format_module_detail"></a>

### `format_module_detail`

`function` | [modules/module_registry.py:589](../../modules/module_registry.py#L589)

```python
def format_module_detail(m: ModuleInfo) -> str
```

Format a single module's full metadata.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `m` | `ModuleInfo` |  |  |

**Returns:** `str`

*Called by:* [`ModuleManagerCommandSet.do_use`](cli.commands.module_manager.py.md#modulemanagercommandset-do_use)

---
