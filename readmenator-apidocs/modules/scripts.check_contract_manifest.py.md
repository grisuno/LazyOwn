# `scripts.check_contract_manifest`

> Source: [scripts/check_contract_manifest.py:1](../../scripts/check_contract_manifest.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Verify that documented contracts still exist on disk.

The repository publishes contract tables and public import examples in its
markdown. Markdown drifts silently when a module is renamed or a test file
is deleted. This script reads the contract tables and the public import
examples and fails when a documented module, test, or public symbol is
missing.

The check is intentionally conservative. It ignores globs, brace
expansions, placeholders, URLs, and session artefacts, because those are
patterns rather than concrete paths.

Usage:
    python3 scripts/check_contract_manifest.py
    python3 scripts/check_contract_manifest.py --verbose

## Contents

- **Classes:** [`ManifestConfig`](#manifestconfig)
- **Functions:** [`check_manifest`](#check_manifest), [`main`](#main)
- **Constants:** [`BACKTICK_RE`](#backtick_re), [`IMPORT_RE`](#import_re), [`DOTNAME_RE`](#dotname_re), [`IMPORT_NAME_RE`](#import_name_re), [`DEFAULT_CONFIG`](#default_config)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_scripts_check_contract_manifest_py__main(["main"])
    n_scripts_check_contract_manifest_py__check_manifest(["check_manifest"])
    n_scripts_check_contract_manifest_py__main --> n_scripts_check_contract_manifest_py__check_manifest
```

## Classes

<a id="manifestconfig"></a>

### `ManifestConfig`

`class` `dataclass` | [scripts/check_contract_manifest.py:34](../../scripts/check_contract_manifest.py#L34)

Decorators: `@dataclass`

```python
class ManifestConfig
```

Configuration for the contract manifest check.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`repo_root`](#manifestconfig-repo_root) | `Path` | `field(default_factory=lambda: Path(__file__).resolve().parent.parent)` | Root of the checkout. |
| [`docs_with_tables`](#manifestconfig-docs_with_tables) | `tuple[Path, ...]` | `()` | Markdown files whose tables cite modules and tests. |
| [`core_md`](#manifestconfig-core_md) | `Path` | `Path('CORE.md')` | Consumer document whose import examples are the public API. |
| [`path_extensions`](#manifestconfig-path_extensions) | `tuple[str, ...]` | `('.py', '.yaml', '.yml', '.json', '.html', '.md', '.sh', '.lua', '.tool', '.ls')` | File suffixes treated as concrete path references. |
| [`skip_substrings`](#manifestconfig-skip_substrings) | `tuple[str, ...]` | `('*', '?', '{', '}', '<', '>', '[', ']', ' ', '://')` | Fragments that mark a token as a pattern, not a path. |
| [`skip_prefixes`](#manifestconfig-skip_prefixes) | `tuple[str, ...]` | `('sessions/', 'external/', 'mutants/')` | Repo-relative prefixes that are runtime state. |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__post_init__`](#manifestconfig-__post_init__) | method | Resolve relative paths against the repository root. |

<a id="manifestconfig-__post_init__"></a>

#### `ManifestConfig.__post_init__`

`method` | [scripts/check_contract_manifest.py:53](../../scripts/check_contract_manifest.py#L53)

```python
def __post_init__(self) -> None
```

Resolve relative paths against the repository root.

---

## Functions

<a id="check_manifest"></a>

### `check_manifest`

`function` | [scripts/check_contract_manifest.py:176](../../scripts/check_contract_manifest.py#L176)

```python
def check_manifest(config: ManifestConfig = DEFAULT_CONFIG) -> list[str]
```

Return the list of documented contracts that are missing on disk.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `config` | `ManifestConfig` | `DEFAULT_CONFIG` | Active check configuration. |

**Returns:** `list[str]` - Human readable drift messages. An empty list means the manifest is
consistent with the source.

*Called by:* [`main`](#main)

---

<a id="main"></a>

### `main`

`function` | [scripts/check_contract_manifest.py:229](../../scripts/check_contract_manifest.py#L229)

```python
def main(argv: list[str] | None = None) -> int
```

Run the manifest check and return the process exit code.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `argv` | `list[str] \| None` | `None` | Optional argument vector. Defaults to ``sys.argv``. |

**Returns:** `int` - 0 when the manifest is consistent, 1 when drift is detected.

*Calls:* [`check_manifest`](#check_manifest)

---

## Constants

<a id="backtick_re"></a>

### `BACKTICK_RE`

`constant` | [scripts/check_contract_manifest.py:27](../../scripts/check_contract_manifest.py#L27)

```python
BACKTICK_RE = re.compile('`([^`]+)`')
```

---

<a id="import_re"></a>

### `IMPORT_RE`

`constant` | [scripts/check_contract_manifest.py:28](../../scripts/check_contract_manifest.py#L28)

```python
IMPORT_RE = re.compile('^\\s*from\\s+([A-Za-z_][\\w.]*)\\s+import\\s+(.+)$')
```

---

<a id="dotname_re"></a>

### `DOTNAME_RE`

`constant` | [scripts/check_contract_manifest.py:29](../../scripts/check_contract_manifest.py#L29)

```python
DOTNAME_RE = re.compile('^[A-Za-z_][\\w]*(\\.[A-Za-z_][\\w]*)+$')
```

---

<a id="import_name_re"></a>

### `IMPORT_NAME_RE`

`constant` | [scripts/check_contract_manifest.py:30](../../scripts/check_contract_manifest.py#L30)

```python
IMPORT_NAME_RE = re.compile('[A-Za-z_][\\w]*')
```

---

<a id="default_config"></a>

### `DEFAULT_CONFIG`

`constant` | [scripts/check_contract_manifest.py:63](../../scripts/check_contract_manifest.py#L63)

```python
DEFAULT_CONFIG
```

---
