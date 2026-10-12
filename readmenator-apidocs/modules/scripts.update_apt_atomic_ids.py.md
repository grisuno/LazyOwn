# `scripts.update_apt_atomic_ids`

> Source: [scripts/update_apt_atomic_ids.py:1](../../scripts/update_apt_atomic_ids.py#L1) | language `py` | coverage 66.7% | [API index](../index.md)

Update APT playbooks with real Atomic Red Team test IDs.

Scans the Atomic Red Team repository (already cloned by the user) and maps
MITRE technique IDs to actual ``auto_generated_guid`` values, then patches
``playbooks/apt_*.yaml`` in place.

Usage::

    python3 scripts/update_apt_atomic_ids.py [path/to/atomic-red-team/atomics]

If no path is given it defaults to ``external/.exploit/atomic-red-team/atomics``.

## Contents

- **Functions:** [`build_technique_index`](#build_technique_index), [`update_playbooks`](#update_playbooks)

## Functions

<a id="build_technique_index"></a>

### `build_technique_index`

`function` | [scripts/update_apt_atomic_ids.py:22](../../scripts/update_apt_atomic_ids.py#L22)

```python
def build_technique_index(atomics_path: str) -> dict[str, list[dict]]
```

Map technique_id -> list of {atomic_id, name, description}.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `atomics_path` | `str` |  |  |

**Returns:** `dict[str, list[dict]]`

---

<a id="update_playbooks"></a>

### `update_playbooks`

`function` | [scripts/update_apt_atomic_ids.py:46](../../scripts/update_apt_atomic_ids.py#L46)

```python
def update_playbooks(index: dict[str, list[dict]], playbook_dir: str = 'playbooks') -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `index` | `dict[str, list[dict]]` |  |  |
| `playbook_dir` | `str` | `'playbooks'` |  |

---
