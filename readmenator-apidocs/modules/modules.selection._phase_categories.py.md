# `modules.selection._phase_categories`

> Source: [modules/selection/_phase_categories.py:1](../../modules/selection/_phase_categories.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Shared kill-chain-phase to lookup-category mapping.

History- and catalog-driven selectors (``parquet``, ``bridge``) group their
lookups by coarse category rather than by the exact kill-chain phase, so a
``privesc`` phase also mines ``credential`` history and an ``exploit`` phase
also mines ``intrusion`` and ``brute_force``. The mapping lived privately in
the daemon; it is shared here so both runtimes resolve categories identically.
Unknown phases fall back to ``["other"]`` via [`categories_for`](#categories_for).

## Contents

- **Functions:** [`categories_for`](#categories_for)
- **Constants:** [`PHASE_CATEGORIES`](#phase_categories)

## Functions

<a id="categories_for"></a>

### `categories_for`

`function` | [modules/selection/_phase_categories.py:23](../../modules/selection/_phase_categories.py#L23)

```python
def categories_for(phase: str) -> list[str]
```

Return the lookup categories for a kill-chain phase.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `phase` | `str` |  | Canonical kill-chain phase name. |

**Returns:** `list[str]` - The ordered categories to mine, or ``["other"]`` when the phase is
unknown so a selector always has at least one category to try.

*Called by:* [`BridgeSelector.propose`](modules.selection.bridge.py.md#bridgeselector-propose), [`ParquetSelector.propose`](modules.selection.parquet.py.md#parquetselector-propose)

---

## Constants

<a id="phase_categories"></a>

### `PHASE_CATEGORIES`

`constant` | [modules/selection/_phase_categories.py:13](../../modules/selection/_phase_categories.py#L13)

```python
PHASE_CATEGORIES: dict[str, list[str]]
```

---
