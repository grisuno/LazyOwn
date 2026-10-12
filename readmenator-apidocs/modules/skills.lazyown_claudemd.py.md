# `skills.lazyown_claudemd`

> Source: [skills/lazyown_claudemd.py:1](../../skills/lazyown_claudemd.py#L1) | language `py` | coverage 77.8% | [API index](../index.md)

LazyOwn CLAUDE.md Hierarchical Loader (Claude Code style)

4-level hierarchy (highest → lowest priority):
  1. managed  — /etc/lazyown/CLAUDE.md         (system policy, read-only)
  2. user     — ~/.lazyown/CLAUDE.md            (user preferences)
  3. project  — ./CLAUDE.md, ./.lazyown/CLAUDE.md, ./.lazyown/rules/*.md
  4. local    — ./CLAUDE.local.md               (gitignored, machine-specific)

All levels are merged into a single instructions string passed to the LLM.
Only project and local files are scanned per session (path-sensitive).

## Contents

- **Classes:** [`ClaudeMdLoader`](#claudemdloader)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_lazyown_claudemd_py__ClaudeMdLoader_status_text(["ClaudeMdLoader.status_text"])
    n_skills_lazyown_claudemd_py__ClaudeMdLoader_list_files(["ClaudeMdLoader.list_files"])
    n_skills_lazyown_claudemd_py__ClaudeMdLoader_status_text --> n_skills_lazyown_claudemd_py__ClaudeMdLoader_list_files
```

## Classes

<a id="claudemdloader"></a>

### `ClaudeMdLoader`

`class` | [skills/lazyown_claudemd.py:24](../../skills/lazyown_claudemd.py#L24)

```python
class ClaudeMdLoader
```

Load and merge CLAUDE.md instructions from all hierarchy levels.

Lazy-loads rules directory only when the current working directory
contains it (avoids scanning unrelated paths).

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#claudemdloader-__init__) | constructor |  |
| [`load`](#claudemdloader-load) | method | Return merged instructions string from all applicable levels. |
| [`list_files`](#claudemdloader-list_files) | method | Return metadata for all CLAUDE.md files that exist. |
| [`create_user_file`](#claudemdloader-create_user_file) | method | Create/overwrite ~/.lazyown/CLAUDE.md. |
| [`create_project_file`](#claudemdloader-create_project_file) | method | Create CLAUDE.md (or CLAUDE.local.md) in cwd. |
| [`add_rule`](#claudemdloader-add_rule) | method | Add a named rule file to .lazyown/rules/. |
| [`status_text`](#claudemdloader-status_text) | method |  |

<a id="claudemdloader-__init__"></a>

#### `ClaudeMdLoader.__init__`

`constructor` | [skills/lazyown_claudemd.py:32](../../skills/lazyown_claudemd.py#L32)

```python
def __init__(self, cwd: Path | None = None)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `cwd` | `Path \| None` | `None` |  |

<a id="claudemdloader-load"></a>

#### `ClaudeMdLoader.load`

`method` | [skills/lazyown_claudemd.py:35](../../skills/lazyown_claudemd.py#L35)

```python
def load(self) -> str
```

Return merged instructions string from all applicable levels.

**Returns:** `str`

<a id="claudemdloader-list_files"></a>

#### `ClaudeMdLoader.list_files`

`method` | [skills/lazyown_claudemd.py:90](../../skills/lazyown_claudemd.py#L90)

```python
def list_files(self) -> list[dict]
```

Return metadata for all CLAUDE.md files that exist.

**Returns:** `list[dict]`

*Called by:* [`ClaudeMdLoader.status_text`](#claudemdloader-status_text)

<a id="claudemdloader-create_user_file"></a>

#### `ClaudeMdLoader.create_user_file`

`method` | [skills/lazyown_claudemd.py:115](../../skills/lazyown_claudemd.py#L115)

```python
def create_user_file(self, content: str) -> str
```

Create/overwrite ~/.lazyown/CLAUDE.md.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `content` | `str` |  |  |

**Returns:** `str`

<a id="claudemdloader-create_project_file"></a>

#### `ClaudeMdLoader.create_project_file`

`method` | [skills/lazyown_claudemd.py:121](../../skills/lazyown_claudemd.py#L121)

```python
def create_project_file(self, content: str, local: bool = False) -> str
```

Create CLAUDE.md (or CLAUDE.local.md) in cwd.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `content` | `str` |  |  |
| `local` | `bool` | `False` |  |

**Returns:** `str`

<a id="claudemdloader-add_rule"></a>

#### `ClaudeMdLoader.add_rule`

`method` | [skills/lazyown_claudemd.py:127](../../skills/lazyown_claudemd.py#L127)

```python
def add_rule(self, rule_name: str, content: str) -> str
```

Add a named rule file to .lazyown/rules/.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `rule_name` | `str` |  |  |
| `content` | `str` |  |  |

**Returns:** `str`

<a id="claudemdloader-status_text"></a>

#### `ClaudeMdLoader.status_text`

`method` | [skills/lazyown_claudemd.py:135](../../skills/lazyown_claudemd.py#L135)

```python
def status_text(self) -> str
```

**Returns:** `str`

*Calls:* [`ClaudeMdLoader.list_files`](#claudemdloader-list_files)

---
