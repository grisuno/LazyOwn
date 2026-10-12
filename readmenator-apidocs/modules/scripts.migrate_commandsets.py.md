# `scripts.migrate_commandsets`

> Source: [scripts/migrate_commandsets.py:1](../../scripts/migrate_commandsets.py#L1) | language `py` | coverage 66.7% | [API index](../index.md)

Merge _migrated.py CommandSet methods into clean phase modules.

Reads each ``*_migrated.py`` file under ``cli/commands/``, identifies
``do_*`` methods not yet present in the corresponding clean ``.py`` file,
and appends them. The clean file keeps its existing base class
(LazyOwnCommandSet or PendingCommandSet) unchanged; only new methods
are added.

Usage:
    python3 scripts/migrate_commandsets.py [--dry-run] [--phase scan]

Without ``--phase``, processes every pending phase.

## Contents

- **Functions:** [`merge_phase`](#merge_phase), [`main`](#main)
- **Constants:** [`CLI_COMMANDS_DIR`](#cli_commands_dir)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_scripts_migrate_commandsets_py__main(["main"])
    n_scripts_migrate_commandsets_py__merge_phase(["merge_phase"])
    n_scripts_migrate_commandsets_py__main --> n_scripts_migrate_commandsets_py__merge_phase
```

## Functions

<a id="merge_phase"></a>

### `merge_phase`

`function` | [scripts/migrate_commandsets.py:117](../../scripts/migrate_commandsets.py#L117)

```python
def merge_phase(phase: str, dry_run: bool = False) -> bool
```

Merge one phase's migrated methods into its clean file.

Returns True if changed.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `phase` | `str` |  |  |
| `dry_run` | `bool` | `False` |  |

**Returns:** `bool`

*Called by:* [`main`](#main)

---

<a id="main"></a>

### `main`

`function` | [scripts/migrate_commandsets.py:158](../../scripts/migrate_commandsets.py#L158)

```python
def main() -> None
```

*Calls:* [`merge_phase`](#merge_phase)

---

## Constants

<a id="cli_commands_dir"></a>

### `CLI_COMMANDS_DIR`

`constant` | [scripts/migrate_commandsets.py:22](../../scripts/migrate_commandsets.py#L22)

```python
CLI_COMMANDS_DIR = os.path.join(os.path.dirname(__file__), '..', 'cli', 'commands')
```

---
