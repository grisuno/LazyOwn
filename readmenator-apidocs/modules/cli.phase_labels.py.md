# `cli.phase_labels`

> Source: [cli/phase_labels.py:1](../../cli/phase_labels.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Canonical human-readable labels for kill-chain command phases.

Single source of truth for the phase display names used by the CLI hint
system. The keys mirror the ``phase_to_commands`` buckets of
``cli/command_index.json`` (produced by ``scripts/build_command_index.py``)
so every consumer renders the same label for the same phase key.

## Contents

- **Functions:** [`phase_label`](#phase_label)
- **Constants:** [`PHASE_LABELS`](#phase_labels)

## Functions

<a id="phase_label"></a>

### `phase_label`

`function` | [cli/phase_labels.py:29](../../cli/phase_labels.py#L29)

```python
def phase_label(phase: str) -> str
```

Return the human label for a phase, falling back to title case.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `phase` | `str` |  | Canonical phase key (e.g. ``recon``). |

**Returns:** `str` - The display label, or the title-cased key when unknown.

---

## Constants

<a id="phase_labels"></a>

### `PHASE_LABELS`

`constant` | [cli/phase_labels.py:11](../../cli/phase_labels.py#L11)

```python
PHASE_LABELS: dict[str, str]
```

---
