# `modules.bof_registry`

> Source: [modules/bof_registry.py:1](../../modules/bof_registry.py#L1) | language `py` | coverage 95.9% | [API index](../index.md)

Beacon Object File (BOF) registry and marketplace for LazyOwn.

Catalogs, indexes, and manages BOFs compatible with the TrustedSec
SA BOF API. Supports both Windows COFF BOFs (Cobalt Strike compatible)
and Linux ELF BOFs (BlacksandBeacon). Provides search, install, info,
and update operations against a curated catalog.

The catalog is a static index of known BOFs with metadata: name,
description, author, repository URL, compatible platforms, required
arguments, MITRE ATT&CK technique references, and SHA-256 hashes.

Contracts:
    - BofEntry: immutable dataclass representing one BOF
    - BofCatalog: curated catalog of known BOFs
    - BofRegistry: manages installed BOFs on disk with version tracking
    - BofMarketplace: search/install/uninstall/info operations
    - BofValidator: validates BOF integrity (hash check, platform compatibility)

Design (SOLID):
    - Single Responsibility: catalog, registry, marketplace, and validation
      are separate classes with distinct concerns.
    - Open/Closed: new BOFs added via BofCatalog.register() without modifying
      the marketplace class.
    - Liskov: disk registry and in-memory catalog share no interface contract.
    - Interface Segregation: search, install, and validate are separate concerns.
    - Dependency Inversion: marketplace depends on catalog + registry abstractions.

Usage:
    from modules.bof_registry import BofMarketplace

    mp = BofMarketplace(sessions_dir="sessions")
    results = mp.search("ldap")
    for entry in results:
        print(entry.name, entry.description)
    mp.install("ldap_enum")
    mp.info("ldap_enum")
    mp.uninstall("ldap_enum")

## Contents

- **Classes:** [`BofEntry`](#bofentry), [`BofCatalog`](#bofcatalog), [`BofYamlStore`](#bofyamlstore), [`BofValidator`](#bofvalidator), [`BofRegistry`](#bofregistry), [`BofMarketplace`](#bofmarketplace)
- **Enums:** [`BofPlatform`](#bofplatform), [`BofCategory`](#bofcategory)
- **Functions:** [`find_client_artifact`](#find_client_artifact), [`client_addon_install_path`](#client_addon_install_path), [`stage_entry_bof`](#stage_entry_bof)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class BofPlatform
    <<enum>> BofPlatform
    BofPlatform : WINDOWS
    BofPlatform : LINUX
    class BofCategory
    <<enum>> BofCategory
    BofCategory : RECON
    BofCategory : ENUM
    BofCategory : CRED
    BofCategory : PERSIST
    BofCategory : PRIVESC
    BofCategory : LAT
    BofCategory : EVASION
    BofCategory : EXEC
    BofCategory : COLLECTION
    BofCategory : EXFIL
    BofCategory : GENERAL
    class BofEntry
    BofEntry : str name
    BofEntry : str description
    BofEntry : str author
    BofEntry : str url
    BofEntry : str source_file
    BofEntry : BofPlatform platform
    BofEntry : BofCategory category
    BofEntry : list[str] required_args
    BofEntry : list[str] optional_args
    BofEntry : str mitre_technique
    BofEntry : str sha256
    BofEntry : str min_beacon_version
    BofEntry : list[str] dependencies
    BofEntry : str client
    BofEntry : str client_artifact
    BofEntry : to_dict()
    BofEntry : from_dict()
    class BofCatalog
    BofCatalog : dict[str, BofEntry] entries
    BofCatalog : register()
    BofCatalog : register_many()
    BofCatalog : get()
    BofCatalog : search()
    BofCatalog : list_by_category()
    BofCatalog : list_by_platform()
    BofCatalog : list_all()
    BofCatalog : to_dict()
    BofCatalog : from_dict()
    BofCatalog : load()
    BofCatalog : save()
    class BofYamlStore
    BofYamlStore : __init__()
    BofYamlStore : directory()
    BofYamlStore : load_entries()
    BofYamlStore : load_catalog()
    class BofValidator
    BofValidator : compute_sha256()
    BofValidator : verify_entry()
    BofValidator : validate_args()
    class BofRegistry
    BofRegistry : __init__()
    BofRegistry : install_dir()
    BofRegistry : is_installed()
    BofRegistry : install()
    BofRegistry : uninstall()
    BofRegistry : list_installed()
    BofRegistry : get_install_info()
    class BofMarketplace
    BofMarketplace : __init__()
    BofMarketplace : catalog()
    BofMarketplace : registry()
    BofMarketplace : search()
    BofMarketplace : info()
    BofMarketplace : install()
    BofMarketplace : uninstall()
    BofMarketplace : list_installed()
    BofMarketplace : list_missing_dependencies()
    BofMarketplace : bulk_install()
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_bof_registry_py__BofEntry_from_dict(["BofEntry.from_dict"])
    n_modules_bof_registry_py__BofCategory(["BofCategory"])
    n_modules_bof_registry_py__BofPlatform(["BofPlatform"])
    n_modules_bof_registry_py__BofCatalog_register_many(["BofCatalog.register_many"])
    n_modules_bof_registry_py__BofCatalog_register(["BofCatalog.register"])
    n_modules_bof_registry_py__BofCatalog_from_dict(["BofCatalog.from_dict"])
    n_modules_bof_registry_py__BofCatalog_load(["BofCatalog.load"])
    n_modules_bof_registry_py__BofCatalog_save(["BofCatalog.save"])
    n_modules_bof_registry_py__BofCatalog_to_dict(["BofCatalog.to_dict"])
    n_modules_bof_registry_py__BofYamlStore_load_entries(["BofYamlStore.load_entries"])
    n_modules_bof_registry_py__BofEntry(["BofEntry"])
    n_modules_bof_registry_py__BofYamlStore_load_catalog(["BofYamlStore.load_catalog"])
    n_modules_bof_registry_py__BofCatalog(["BofCatalog"])
    n_modules_bof_registry_py__find_client_artifact(["find_client_artifact"])
    n_modules_bof_registry_py__client_addon_install_path(["client_addon_install_path"])
    n_modules_bof_registry_py__stage_entry_bof(["stage_entry_bof"])
    n_modules_bof_registry_py__BofValidator_verify_entry(["BofValidator.verify_entry"])
    n_modules_bof_registry_py__BofValidator_compute_sha256(["BofValidator.compute_sha256"])
    n_modules_bof_registry_py__BofMarketplace___init__(["BofMarketplace.__init__"])
    n_modules_bof_registry_py__BofRegistry___init__(["BofRegistry.__init__"])
    n_modules_bof_registry_py__BofValidator(["BofValidator"])
    n_modules_bof_registry_py__BofMarketplace_search(["BofMarketplace.search"])
    n_modules_bof_registry_py__BofRegistry_list_installed(["BofRegistry.list_installed"])
    n_modules_bof_registry_py__BofMarketplace_info(["BofMarketplace.info"])
    n_modules_bof_registry_py__BofRegistry_get_install_info(["BofRegistry.get_install_info"])
    n_modules_bof_registry_py__BofMarketplace_install(["BofMarketplace.install"])
    n_modules_bof_registry_py__BofRegistry_install(["BofRegistry.install"])
    n_modules_bof_registry_py__BofRegistry_is_installed(["BofRegistry.is_installed"])
    n_modules_bof_registry_py__BofMarketplace_uninstall(["BofMarketplace.uninstall"])
    n_modules_bof_registry_py__BofRegistry_uninstall(["BofRegistry.uninstall"])
    n_modules_bof_registry_py__BofMarketplace_list_installed(["BofMarketplace.list_installed"])
    n_modules_bof_registry_py__BofEntry_from_dict --> n_modules_bof_registry_py__BofCategory
    n_modules_bof_registry_py__BofEntry_from_dict --> n_modules_bof_registry_py__BofPlatform
    n_modules_bof_registry_py__BofCatalog_register_many --> n_modules_bof_registry_py__BofCatalog_register
    n_modules_bof_registry_py__BofCatalog_from_dict --> n_modules_bof_registry_py__BofEntry_from_dict
    n_modules_bof_registry_py__BofCatalog_load --> n_modules_bof_registry_py__BofCatalog_from_dict
    n_modules_bof_registry_py__BofCatalog_save --> n_modules_bof_registry_py__BofCatalog_to_dict
    n_modules_bof_registry_py__BofYamlStore_load_entries --> n_modules_bof_registry_py__BofCategory
    n_modules_bof_registry_py__BofYamlStore_load_entries --> n_modules_bof_registry_py__BofEntry
    n_modules_bof_registry_py__BofYamlStore_load_entries --> n_modules_bof_registry_py__BofPlatform
    n_modules_bof_registry_py__BofYamlStore_load_catalog --> n_modules_bof_registry_py__BofCatalog
    n_modules_bof_registry_py__BofYamlStore_load_catalog --> n_modules_bof_registry_py__BofCatalog_register_many
    n_modules_bof_registry_py__BofYamlStore_load_catalog --> n_modules_bof_registry_py__BofYamlStore_load_entries
    n_modules_bof_registry_py__find_client_artifact --> n_modules_bof_registry_py__client_addon_install_path
    n_modules_bof_registry_py__stage_entry_bof --> n_modules_bof_registry_py__find_client_artifact
    n_modules_bof_registry_py__BofValidator_verify_entry --> n_modules_bof_registry_py__BofValidator_compute_sha256
    n_modules_bof_registry_py__BofMarketplace___init__ --> n_modules_bof_registry_py__BofRegistry___init__
    n_modules_bof_registry_py__BofMarketplace___init__ --> n_modules_bof_registry_py__BofValidator
    n_modules_bof_registry_py__BofMarketplace_search --> n_modules_bof_registry_py__BofRegistry_list_installed
    n_modules_bof_registry_py__BofMarketplace_info --> n_modules_bof_registry_py__BofRegistry_get_install_info
    n_modules_bof_registry_py__BofMarketplace_install --> n_modules_bof_registry_py__BofRegistry_install
    n_modules_bof_registry_py__BofMarketplace_install --> n_modules_bof_registry_py__BofRegistry_is_installed
    n_modules_bof_registry_py__BofMarketplace_uninstall --> n_modules_bof_registry_py__BofRegistry_is_installed
    n_modules_bof_registry_py__BofMarketplace_uninstall --> n_modules_bof_registry_py__BofRegistry_uninstall
    n_modules_bof_registry_py__BofMarketplace_list_installed --> n_modules_bof_registry_py__BofRegistry_list_installed
```

## Classes

<a id="bofentry"></a>

### `BofEntry`

`class` `dataclass` | [modules/bof_registry.py:95](../../modules/bof_registry.py#L95)

Decorators: `@dataclass(frozen=True)`

```python
class BofEntry
```

Immutable catalog entry for a single Beacon Object File.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`name`](#bofentry-name) | `str` |  | Unique identifier (e.g., 'ldap_enum'). |
| [`description`](#bofentry-description) | `str` |  | Human-readable description. |
| [`author`](#bofentry-author) | `str` |  | Author or organization. |
| [`url`](#bofentry-url) | `str` |  | Repository URL. |
| [`source_file`](#bofentry-source_file) | `str` |  | Relative path to the C source file in the repo. |
| [`platform`](#bofentry-platform) | `BofPlatform` | `BofPlatform.WINDOWS` | Target platform for the compiled BOF. |
| [`category`](#bofentry-category) | `BofCategory` | `BofCategory.GENERAL` | Functional category. |
| [`required_args`](#bofentry-required_args) | `list[str]` | `field(default_factory=list)` | List of required argument names. |
| [`optional_args`](#bofentry-optional_args) | `list[str]` | `field(default_factory=list)` | List of optional argument names. |
| [`mitre_technique`](#bofentry-mitre_technique) | `str` | `''` | MITRE ATT&CK technique ID (e.g., 'T1018'). |
| [`sha256`](#bofentry-sha256) | `str` | `''` | SHA-256 hash of the canonical source file (empty until audited). |
| [`min_beacon_version`](#bofentry-min_beacon_version) | `str` | `'1.0'` | Minimum beacon version required. |
| [`dependencies`](#bofentry-dependencies) | `list[str]` | `field(default_factory=list)` | List of dependency BOF names. |
| [`client`](#bofentry-client) | `str` | `''` |  |
| [`client_artifact`](#bofentry-client_artifact) | `str` | `''` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`to_dict`](#bofentry-to_dict) | method | Serialize to dictionary. |
| [`from_dict`](#bofentry-from_dict) | classmethod | Build from a dictionary. |

<a id="bofentry-to_dict"></a>

#### `BofEntry.to_dict`

`method` | [modules/bof_registry.py:130](../../modules/bof_registry.py#L130)

```python
def to_dict(self) -> dict[str, Any]
```

Serialize to dictionary.

**Returns:** `dict[str, Any]`

<a id="bofentry-from_dict"></a>

#### `BofEntry.from_dict`

`classmethod` | [modules/bof_registry.py:151](../../modules/bof_registry.py#L151)

Decorators: `@classmethod`

```python
def from_dict(cls, raw: dict[str, Any]) -> BofEntry
```

Build from a dictionary.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `raw` | `dict[str, Any]` |  |  |

**Returns:** `BofEntry`

*Calls:* [`BofCategory`](#bofcategory), [`BofPlatform`](#bofplatform)

*Called by:* [`BofCatalog.from_dict`](#bofcatalog-from_dict)

---

<a id="bofcatalog"></a>

### `BofCatalog`

`class` `dataclass` | [modules/bof_registry.py:173](../../modules/bof_registry.py#L173)

Decorators: `@dataclass`

```python
class BofCatalog
```

Curated catalog of known Beacon Object Files.

The catalog is a static index maintained by the LazyOwn team. Entries
are added via ``register()`` and persisted to disk as JSON for sharing
between operator sessions.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`entries`](#bofcatalog-entries) | `dict[str, BofEntry]` | `field(default_factory=dict)` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`register`](#bofcatalog-register) | method | Register a BOF entry in the catalog. |
| [`register_many`](#bofcatalog-register_many) | method | Register multiple BOF entries at once. |
| [`get`](#bofcatalog-get) | method | Retrieve a BOF entry by name. |
| [`search`](#bofcatalog-search) | method | Search catalog by keyword across name, description, and technique. |
| [`list_by_category`](#bofcatalog-list_by_category) | method | Return all BOFs in a specific category. |
| [`list_by_platform`](#bofcatalog-list_by_platform) | method | Return all BOFs for a specific platform. |
| [`list_all`](#bofcatalog-list_all) | method | Return all catalog entries sorted by name. |
| [`to_dict`](#bofcatalog-to_dict) | method | Serialize the entire catalog to a dictionary. |
| [`from_dict`](#bofcatalog-from_dict) | classmethod | Build a catalog from a dictionary. |
| [`load`](#bofcatalog-load) | classmethod | Load a catalog from a JSON file. |
| [`save`](#bofcatalog-save) | method | Save the catalog to a JSON file. |

<a id="bofcatalog-register"></a>

#### `BofCatalog.register`

`method` | [modules/bof_registry.py:183](../../modules/bof_registry.py#L183)

```python
def register(self, entry: BofEntry) -> None
```

Register a BOF entry in the catalog.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entry` | `BofEntry` |  |  |

*Called by:* [`BofCatalog.register_many`](#bofcatalog-register_many)

<a id="bofcatalog-register_many"></a>

#### `BofCatalog.register_many`

`method` | [modules/bof_registry.py:188](../../modules/bof_registry.py#L188)

```python
def register_many(self, entries: list[BofEntry]) -> None
```

Register multiple BOF entries at once.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entries` | `list[BofEntry]` |  |  |

*Calls:* [`BofCatalog.register`](#bofcatalog-register)

*Called by:* [`BofYamlStore.load_catalog`](#bofyamlstore-load_catalog)

<a id="bofcatalog-get"></a>

#### `BofCatalog.get`

`method` | [modules/bof_registry.py:193](../../modules/bof_registry.py#L193)

```python
def get(self, name: str) -> BofEntry
```

Retrieve a BOF entry by name.

Raises KeyError if not found.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `BofEntry`

**Raises**

- `KeyError`: (raised in the body, not documented)

<a id="bofcatalog-search"></a>

#### `BofCatalog.search`

`method` | [modules/bof_registry.py:204](../../modules/bof_registry.py#L204)

```python
def search(self, query: str) -> list[BofEntry]
```

Search catalog by keyword across name, description, and technique.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  | Case-insensitive search keyword. |

**Returns:** `list[BofEntry]` - List of matching BofEntry objects, sorted by relevance.

<a id="bofcatalog-list_by_category"></a>

#### `BofCatalog.list_by_category`

`method` | [modules/bof_registry.py:237](../../modules/bof_registry.py#L237)

```python
def list_by_category(self, category: BofCategory) -> list[BofEntry]
```

Return all BOFs in a specific category.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `category` | `BofCategory` |  |  |

**Returns:** `list[BofEntry]`

<a id="bofcatalog-list_by_platform"></a>

#### `BofCatalog.list_by_platform`

`method` | [modules/bof_registry.py:241](../../modules/bof_registry.py#L241)

```python
def list_by_platform(self, platform: BofPlatform) -> list[BofEntry]
```

Return all BOFs for a specific platform.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `platform` | `BofPlatform` |  |  |

**Returns:** `list[BofEntry]`

<a id="bofcatalog-list_all"></a>

#### `BofCatalog.list_all`

`method` | [modules/bof_registry.py:245](../../modules/bof_registry.py#L245)

```python
def list_all(self) -> list[BofEntry]
```

Return all catalog entries sorted by name.

**Returns:** `list[BofEntry]`

<a id="bofcatalog-to_dict"></a>

#### `BofCatalog.to_dict`

`method` | [modules/bof_registry.py:249](../../modules/bof_registry.py#L249)

```python
def to_dict(self) -> dict[str, Any]
```

Serialize the entire catalog to a dictionary.

**Returns:** `dict[str, Any]`

*Called by:* [`BofCatalog.save`](#bofcatalog-save)

<a id="bofcatalog-from_dict"></a>

#### `BofCatalog.from_dict`

`classmethod` | [modules/bof_registry.py:257](../../modules/bof_registry.py#L257)

Decorators: `@classmethod`

```python
def from_dict(cls, raw: dict[str, Any]) -> BofCatalog
```

Build a catalog from a dictionary.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `raw` | `dict[str, Any]` |  |  |

**Returns:** `BofCatalog`

*Calls:* [`BofEntry.from_dict`](#bofentry-from_dict)

*Called by:* [`BofCatalog.load`](#bofcatalog-load)

<a id="bofcatalog-load"></a>

#### `BofCatalog.load`

`classmethod` | [modules/bof_registry.py:265](../../modules/bof_registry.py#L265)

Decorators: `@classmethod`

```python
def load(cls, path: str | Path) -> BofCatalog
```

Load a catalog from a JSON file.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` |  |  |

**Returns:** `BofCatalog`

*Calls:* [`BofCatalog.from_dict`](#bofcatalog-from_dict)

<a id="bofcatalog-save"></a>

#### `BofCatalog.save`

`method` | [modules/bof_registry.py:273](../../modules/bof_registry.py#L273)

```python
def save(self, path: str | Path) -> None
```

Save the catalog to a JSON file.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` |  |  |

*Calls:* [`BofCatalog.to_dict`](#bofcatalog-to_dict)

---

<a id="bofyamlstore"></a>

### `BofYamlStore`

`class` | [modules/bof_registry.py:281](../../modules/bof_registry.py#L281)

```python
class BofYamlStore
```

Load BOF catalog entries from the ``bofs/*.yaml`` configuration files.

Every YAML file is one delivery contract: the BOF capability plus the
lazyaddon beacon client (``beacon`` or ``blacksandbeacon``) that
delivers it. Invalid files are skipped with a logged warning so a
broken draft can never empty the operator's catalog.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#bofyamlstore-__init__) | constructor | Bind the store to a directory. |
| [`directory`](#bofyamlstore-directory) | property | Return the directory bound to this store. |
| [`load_entries`](#bofyamlstore-load_entries) | method | Parse every YAML file into [`BofEntry`](#bofentry) objects. |
| [`load_catalog`](#bofyamlstore-load_catalog) | method | Build a [`BofCatalog`](#bofcatalog) from the YAML configuration files. |

<a id="bofyamlstore-__init__"></a>

#### `BofYamlStore.__init__`

`constructor` | [modules/bof_registry.py:290](../../modules/bof_registry.py#L290)

```python
def __init__(self, directory: str | Path = BOFS_DIR) -> None
```

Bind the store to a directory.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `directory` | `str \| Path` | `BOFS_DIR` | Root folder with one ``.yaml`` file per BOF. |

<a id="bofyamlstore-directory"></a>

#### `BofYamlStore.directory`

`property` | [modules/bof_registry.py:299](../../modules/bof_registry.py#L299)

Decorators: `@property`

```python
def directory(self) -> Path
```

Return the directory bound to this store.

**Returns:** `Path`

<a id="bofyamlstore-load_entries"></a>

#### `BofYamlStore.load_entries`

`method` | [modules/bof_registry.py:303](../../modules/bof_registry.py#L303)

```python
def load_entries(self) -> list[BofEntry]
```

Parse every YAML file into [`BofEntry`](#bofentry) objects.

**Returns:** `list[BofEntry]` - Ordered entries; unreadable or invalid files are skipped.

*Calls:* [`load_bof`](modules.bof_admin.py.md#load_bof), [`validate_bof`](modules.bof_admin.py.md#validate_bof), [`BofCategory`](#bofcategory), [`BofEntry`](#bofentry), [`BofPlatform`](#bofplatform)

*Called by:* [`BofYamlStore.load_catalog`](#bofyamlstore-load_catalog)

<a id="bofyamlstore-load_catalog"></a>

#### `BofYamlStore.load_catalog`

`method` | [modules/bof_registry.py:342](../../modules/bof_registry.py#L342)

```python
def load_catalog(self) -> BofCatalog
```

Build a [`BofCatalog`](#bofcatalog) from the YAML configuration files.

**Returns:** `BofCatalog`

*Calls:* [`BofCatalog`](#bofcatalog), [`BofCatalog.register_many`](#bofcatalog-register_many), [`BofYamlStore.load_entries`](#bofyamlstore-load_entries)

---

<a id="bofvalidator"></a>

### `BofValidator`

`class` | [modules/bof_registry.py:474](../../modules/bof_registry.py#L474)

```python
class BofValidator
```

Validates BOF integrity and compatibility.

Checks SHA-256 hashes of downloaded source files against the
catalog, verifies platform compatibility, and validates that
required arguments are supplied.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`compute_sha256`](#bofvalidator-compute_sha256) | staticmethod | Compute the SHA-256 hash of a file. |
| [`verify_entry`](#bofvalidator-verify_entry) | staticmethod | Verify the SHA-256 of a downloaded BOF source matches the catalog. |
| [`validate_args`](#bofvalidator-validate_args) | staticmethod | Validate that all required arguments are supplied. |

<a id="bofvalidator-compute_sha256"></a>

#### `BofValidator.compute_sha256`

`staticmethod` | [modules/bof_registry.py:483](../../modules/bof_registry.py#L483)

Decorators: `@staticmethod`

```python
def compute_sha256(filepath: str | Path) -> str
```

Compute the SHA-256 hash of a file.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filepath` | `str \| Path` |  |  |

**Returns:** `str`

*Called by:* [`BofValidator.verify_entry`](#bofvalidator-verify_entry)

<a id="bofvalidator-verify_entry"></a>

#### `BofValidator.verify_entry`

`staticmethod` | [modules/bof_registry.py:492](../../modules/bof_registry.py#L492)

Decorators: `@staticmethod`

```python
def verify_entry(entry: BofEntry, filepath: str | Path) -> tuple[bool, str]
```

Verify the SHA-256 of a downloaded BOF source matches the catalog.

Returns (ok, reason). If entry.sha256 is empty, verification is
skipped with an informational message.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entry` | `BofEntry` |  |  |
| `filepath` | `str \| Path` |  |  |

**Returns:** `tuple[bool, str]`

*Calls:* [`BofValidator.compute_sha256`](#bofvalidator-compute_sha256)

<a id="bofvalidator-validate_args"></a>

#### `BofValidator.validate_args`

`staticmethod` | [modules/bof_registry.py:508](../../modules/bof_registry.py#L508)

Decorators: `@staticmethod`

```python
def validate_args(entry: BofEntry, args: dict[str, str]) -> list[str]
```

Validate that all required arguments are supplied.

Returns a list of missing argument names (empty = valid).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entry` | `BofEntry` |  |  |
| `args` | `dict[str, str]` |  |  |

**Returns:** `list[str]`

---

<a id="bofregistry"></a>

### `BofRegistry`

`class` | [modules/bof_registry.py:520](../../modules/bof_registry.py#L520)

```python
class BofRegistry
```

Manages BOF installations on disk with version tracking.

Each installed BOF is tracked in a manifest JSON file with the
installation timestamp, BOF version, and source URL.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#bofregistry-__init__) | constructor |  |
| [`install_dir`](#bofregistry-install_dir) | property | Return the BOF installation directory. |
| [`is_installed`](#bofregistry-is_installed) | method | Return True if a BOF is installed. |
| [`install`](#bofregistry-install) | method | Register a BOF as installed with current timestamp. |
| [`uninstall`](#bofregistry-uninstall) | method | Unregister a BOF from the manifest and optionally remove its files. |
| [`list_installed`](#bofregistry-list_installed) | method | Return a list of all installed BOFs with metadata. |
| [`get_install_info`](#bofregistry-get_install_info) | method | Return installation metadata for a BOF, or None if not installed. |

<a id="bofregistry-__init__"></a>

#### `BofRegistry.__init__`

`constructor` | [modules/bof_registry.py:527](../../modules/bof_registry.py#L527)

```python
def __init__(self, sessions_dir: str | Path) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sessions_dir` | `str \| Path` |  |  |

*Called by:* [`BofMarketplace.__init__`](#bofmarketplace-__init__)

<a id="bofregistry-install_dir"></a>

#### `BofRegistry.install_dir`

`property` | [modules/bof_registry.py:533](../../modules/bof_registry.py#L533)

Decorators: `@property`

```python
def install_dir(self) -> Path
```

Return the BOF installation directory.

**Returns:** `Path`

<a id="bofregistry-is_installed"></a>

#### `BofRegistry.is_installed`

`method` | [modules/bof_registry.py:553](../../modules/bof_registry.py#L553)

```python
def is_installed(self, name: str) -> bool
```

Return True if a BOF is installed.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Called by:* [`BofMarketplace.install`](#bofmarketplace-install), [`BofMarketplace.list_missing_dependencies`](#bofmarketplace-list_missing_dependencies), [`BofMarketplace.uninstall`](#bofmarketplace-uninstall)

<a id="bofregistry-install"></a>

#### `BofRegistry.install`

`method` | [modules/bof_registry.py:558](../../modules/bof_registry.py#L558)

```python
def install(self, entry: BofEntry) -> Path
```

Register a BOF as installed with current timestamp.

Returns the install directory for this BOF.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entry` | `BofEntry` |  |  |

**Returns:** `Path`

*Called by:* [`BofMarketplace.install`](#bofmarketplace-install)

<a id="bofregistry-uninstall"></a>

#### `BofRegistry.uninstall`

`method` | [modules/bof_registry.py:579](../../modules/bof_registry.py#L579)

```python
def uninstall(self, name: str, remove_files: bool = True) -> bool
```

Unregister a BOF from the manifest and optionally remove its files.

Returns True if the BOF was installed and successfully removed.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `remove_files` | `bool` | `True` |  |

**Returns:** `bool`

*Called by:* [`BofMarketplace.uninstall`](#bofmarketplace-uninstall)

<a id="bofregistry-list_installed"></a>

#### `BofRegistry.list_installed`

`method` | [modules/bof_registry.py:596](../../modules/bof_registry.py#L596)

```python
def list_installed(self) -> list[dict[str, Any]]
```

Return a list of all installed BOFs with metadata.

**Returns:** `list[dict[str, Any]]`

*Called by:* [`BofMarketplace.list_installed`](#bofmarketplace-list_installed), [`BofMarketplace.search`](#bofmarketplace-search)

<a id="bofregistry-get_install_info"></a>

#### `BofRegistry.get_install_info`

`method` | [modules/bof_registry.py:601](../../modules/bof_registry.py#L601)

```python
def get_install_info(self, name: str) -> dict[str, Any] | None
```

Return installation metadata for a BOF, or None if not installed.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `dict[str, Any] | None`

*Called by:* [`BofMarketplace.info`](#bofmarketplace-info)

---

<a id="bofmarketplace"></a>

### `BofMarketplace`

`class` | [modules/bof_registry.py:607](../../modules/bof_registry.py#L607)

```python
class BofMarketplace
```

BOF discovery, installation, and management interface.

Composes a BofCatalog (curated index) and a BofRegistry (disk
state) to provide search/install/uninstall/info operations.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#bofmarketplace-__init__) | constructor |  |
| [`catalog`](#bofmarketplace-catalog) | property | Return the catalog. |
| [`registry`](#bofmarketplace-registry) | property | Return the registry. |
| [`search`](#bofmarketplace-search) | method | Search the catalog and return enriched results with install status. |
| [`info`](#bofmarketplace-info) | method | Get detailed information about a BOF by name. |
| [`install`](#bofmarketplace-install) | method | Install a BOF from the catalog by name. |
| [`uninstall`](#bofmarketplace-uninstall) | method | Uninstall a BOF by name. |
| [`list_installed`](#bofmarketplace-list_installed) | method | List all installed BOFs with catalog enrichment. |
| [`list_missing_dependencies`](#bofmarketplace-list_missing_dependencies) | method | Return a list of dependencies for a BOF that are not installed. |
| [`bulk_install`](#bofmarketplace-bulk_install) | method | Install multiple BOFs at once. |

<a id="bofmarketplace-__init__"></a>

#### `BofMarketplace.__init__`

`constructor` | [modules/bof_registry.py:619](../../modules/bof_registry.py#L619)

```python
def __init__(self, sessions_dir: str | Path = 'sessions', catalog: BofCatalog | None = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sessions_dir` | `str \| Path` | `'sessions'` |  |
| `catalog` | `BofCatalog \| None` | `None` |  |

*Calls:* [`BofRegistry.__init__`](#bofregistry-__init__), [`BofValidator`](#bofvalidator)

*Called by:* [`BofMarketplaceCommandSet.do_bof_catalog`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_catalog), [`BofMarketplaceCommandSet.do_bof_info`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_info), [`BofMarketplaceCommandSet.do_bof_install`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_install), [`BofMarketplaceCommandSet.do_bof_list`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_list), [`BofMarketplaceCommandSet.do_bof_search`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_search), [`BofMarketplaceCommandSet.do_bof_stage`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_stage), [`BofMarketplaceCommandSet.do_bof_uninstall`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_uninstall), [`stage_bof`](modules.bof_delivery.py.md#stage_bof)

<a id="bofmarketplace-catalog"></a>

#### `BofMarketplace.catalog`

`property` | [modules/bof_registry.py:630](../../modules/bof_registry.py#L630)

Decorators: `@property`

```python
def catalog(self) -> BofCatalog
```

Return the catalog.

**Returns:** `BofCatalog`

<a id="bofmarketplace-registry"></a>

#### `BofMarketplace.registry`

`property` | [modules/bof_registry.py:635](../../modules/bof_registry.py#L635)

Decorators: `@property`

```python
def registry(self) -> BofRegistry
```

Return the registry.

**Returns:** `BofRegistry`

<a id="bofmarketplace-search"></a>

#### `BofMarketplace.search`

`method` | [modules/bof_registry.py:639](../../modules/bof_registry.py#L639)

```python
def search(self, query: str) -> list[dict[str, Any]]
```

Search the catalog and return enriched results with install status.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  | Search keyword (name, description, technique, category). |

**Returns:** `list[dict[str, Any]]` - List of dicts with BOF metadata plus `installed` flag.

*Calls:* [`BofRegistry.list_installed`](#bofregistry-list_installed)

*Called by:* [`BofMarketplaceCommandSet.do_bof_search`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_search)

<a id="bofmarketplace-info"></a>

#### `BofMarketplace.info`

`method` | [modules/bof_registry.py:658](../../modules/bof_registry.py#L658)

```python
def info(self, name: str) -> dict[str, Any]
```

Get detailed information about a BOF by name.

Includes catalog metadata plus install state.
Returns a dict with 'error' key if not found.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `dict[str, Any]`

*Calls:* [`BofRegistry.get_install_info`](#bofregistry-get_install_info)

*Called by:* [`BofMarketplaceCommandSet.do_bof_info`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_info)

<a id="bofmarketplace-install"></a>

#### `BofMarketplace.install`

`method` | [modules/bof_registry.py:675](../../modules/bof_registry.py#L675)

```python
def install(self, name: str) -> dict[str, Any]
```

Install a BOF from the catalog by name.

Registers the BOF in the disk manifest. Does NOT clone
the source repository; the operator is expected to have
the catalog repository already cloned, or use a separate
install step for source retrieval.

Returns a dict with status information.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `dict[str, Any]`

*Calls:* [`BofRegistry.install`](#bofregistry-install), [`BofRegistry.is_installed`](#bofregistry-is_installed)

*Called by:* [`BofMarketplaceCommandSet.do_bof_install`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_install), [`BofMarketplaceCommandSet.do_bof_stage`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_stage), [`BofMarketplace.bulk_install`](#bofmarketplace-bulk_install)

<a id="bofmarketplace-uninstall"></a>

#### `BofMarketplace.uninstall`

`method` | [modules/bof_registry.py:704](../../modules/bof_registry.py#L704)

```python
def uninstall(self, name: str) -> dict[str, Any]
```

Uninstall a BOF by name.

Returns a dict with uninstall status.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `dict[str, Any]`

*Calls:* [`BofRegistry.is_installed`](#bofregistry-is_installed), [`BofRegistry.uninstall`](#bofregistry-uninstall)

*Called by:* [`BofMarketplaceCommandSet.do_bof_uninstall`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_uninstall)

<a id="bofmarketplace-list_installed"></a>

#### `BofMarketplace.list_installed`

`method` | [modules/bof_registry.py:717](../../modules/bof_registry.py#L717)

```python
def list_installed(self) -> list[dict[str, Any]]
```

List all installed BOFs with catalog enrichment.

**Returns:** `list[dict[str, Any]]`

*Calls:* [`BofRegistry.list_installed`](#bofregistry-list_installed)

*Called by:* [`BofMarketplaceCommandSet.do_bof_list`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_list)

<a id="bofmarketplace-list_missing_dependencies"></a>

#### `BofMarketplace.list_missing_dependencies`

`method` | [modules/bof_registry.py:729](../../modules/bof_registry.py#L729)

```python
def list_missing_dependencies(self, name: str) -> list[str]
```

Return a list of dependencies for a BOF that are not installed.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `list[str]`

*Calls:* [`BofRegistry.is_installed`](#bofregistry-is_installed)

<a id="bofmarketplace-bulk_install"></a>

#### `BofMarketplace.bulk_install`

`method` | [modules/bof_registry.py:737](../../modules/bof_registry.py#L737)

```python
def bulk_install(self, names: list[str]) -> dict[str, dict[str, Any]]
```

Install multiple BOFs at once.

Returns a dict mapping BOF name to result dict.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `names` | `list[str]` |  |  |

**Returns:** `dict[str, dict[str, Any]]`

*Calls:* [`BofMarketplace.install`](#bofmarketplace-install)

---

## Enums

<a id="bofplatform"></a>

### `BofPlatform`

`enum` | [modules/bof_registry.py:71](../../modules/bof_registry.py#L71)

```python
class BofPlatform(str, Enum)
```

Bases: `str`, `Enum`

Target platform for a Beacon Object File.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`WINDOWS`](#bofplatform-windows) |  | `'windows'` |  |
| [`LINUX`](#bofplatform-linux) |  | `'linux'` |  |

---

<a id="bofcategory"></a>

### `BofCategory`

`enum` | [modules/bof_registry.py:78](../../modules/bof_registry.py#L78)

```python
class BofCategory(str, Enum)
```

Bases: `str`, `Enum`

Functional category of a BOF.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`RECON`](#bofcategory-recon) |  | `'reconnaissance'` |  |
| [`ENUM`](#bofcategory-enum) |  | `'enumeration'` |  |
| [`CRED`](#bofcategory-cred) |  | `'credential_access'` |  |
| [`PERSIST`](#bofcategory-persist) |  | `'persistence'` |  |
| [`PRIVESC`](#bofcategory-privesc) |  | `'privilege_escalation'` |  |
| [`LAT`](#bofcategory-lat) |  | `'lateral_movement'` |  |
| [`EVASION`](#bofcategory-evasion) |  | `'evasion'` |  |
| [`EXEC`](#bofcategory-exec) |  | `'execution'` |  |
| [`COLLECTION`](#bofcategory-collection) |  | `'collection'` |  |
| [`EXFIL`](#bofcategory-exfil) |  | `'exfiltration'` |  |
| [`GENERAL`](#bofcategory-general) |  | `'general'` |  |

---

## Functions

<a id="find_client_artifact"></a>

### `find_client_artifact`

`function` | [modules/bof_registry.py:362](../../modules/bof_registry.py#L362)

```python
def find_client_artifact(entry: BofEntry, *, external_root: str | Path = 'external/.exploit') -> str | None
```

Resolve the compiled object file of a BOF across all known source trees.

Resolution order:
    1. The client lazyaddon's ``tool.install_path`` (repo-relative
       checkout) joined with the entry's `[`client_artifact`](#bofentry-client_artifact)`.
    2. The client's canonical compiled layout
       (``<checkout>/build/bof/<name>.x64.o``, ``.o``).
    3. A repository-wide search under ``external/.exploit`` (plus the
       Windows beacon canonical ``bof`` layouts).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entry` | `BofEntry` |  | Catalog entry (client and client_artifact honoured). |
| `external_root` | `str \| Path` | `'external/.exploit'` | Repository root holding the checked-out beacons. |

**Returns:** `str | None` - The path to the compiled object, or None when none is found.

*Calls:* [`client_addon_install_path`](#client_addon_install_path)

*Called by:* [`stage_entry_bof`](#stage_entry_bof)

---

<a id="client_addon_install_path"></a>

### `client_addon_install_path`

`function` | [modules/bof_registry.py:415](../../modules/bof_registry.py#L415)

```python
def client_addon_install_path(client: str, addons_dir: str | Path = 'lazyaddons') -> str | None
```

Read the ``tool.install_path`` of one beacon client lazyaddon.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` | `str` |  | Lazyaddon name (``beacon`` or ``blacksandbeacon``). |
| `addons_dir` | `str \| Path` | `'lazyaddons'` | Directory with the lazyaddon YAML manifests. |

**Returns:** `str | None` - The relative install path, or None when the addon is missing.

*Called by:* [`find_client_artifact`](#find_client_artifact)

---

<a id="stage_entry_bof"></a>

### `stage_entry_bof`

`function` | [modules/bof_registry.py:441](../../modules/bof_registry.py#L441)

```python
def stage_entry_bof(entry: BofEntry, sessions_dir: str | Path = 'sessions') -> str | None
```

Stage a compiled BOF object for beacon delivery.

Copies the resolved artifact to ``<sessions>/temp_uploads/bofs/<name>``
where the C2 ``/bof/<name>`` endpoint serves it to beacons (raw
base64 object, the upstream wire format).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entry` | `BofEntry` |  | Catalog entry to stage. |
| `sessions_dir` | `str \| Path` | `'sessions'` | State root holding ``temp_uploads/``. |

**Returns:** `str | None` - The staged path, or None when no compiled object exists.

*Calls:* [`find_client_artifact`](#find_client_artifact)

*Called by:* [`stage_bof`](modules.bof_delivery.py.md#stage_bof)

---
