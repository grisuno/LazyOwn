# `modules.categories`

> Source: [modules/categories.py:1](../../modules/categories.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

modules/categories.py ===================== cmd2 command category strings for LazyOwn.

Extracted from utils.py so they can be imported independently
without pulling in the full utils dependency tree.

Usage:
    from modules.categories import recon_category, scanning_category

## Contents

- **Constants:** [`ALL_CATEGORIES`](#all_categories), [`SHORT_TO_CATEGORY`](#short_to_category), [`CATEGORY_TO_SHORT`](#category_to_short)

## Constants

<a id="all_categories"></a>

### `ALL_CATEGORIES`

`constant` | [modules/categories.py:34](../../modules/categories.py#L34)

```python
ALL_CATEGORIES
```

---

<a id="short_to_category"></a>

### `SHORT_TO_CATEGORY`

`constant` | [modules/categories.py:56](../../modules/categories.py#L56)

```python
SHORT_TO_CATEGORY
```

---

<a id="category_to_short"></a>

### `CATEGORY_TO_SHORT`

`constant` | [modules/categories.py:73](../../modules/categories.py#L73)

```python
CATEGORY_TO_SHORT = {v: k for k, v in SHORT_TO_CATEGORY.items()}
```

---
