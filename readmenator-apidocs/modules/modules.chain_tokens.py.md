# `modules.chain_tokens`

> Source: [modules/chain_tokens.py:1](../../modules/chain_tokens.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Engagement-state tokens for YAML chains.

Chains reference live engagement state through tokens such as
``{ports}``, ``{services}`` and ``{password}``. This module resolves
those tokens from the fact store (`[`skills.lazyown_facts`](skills.lazyown_facts.py.md)`) and from
sessions credential files, so operators never paste discovered data
into YAML by hand. Every produced value is untrusted: the runner keeps
these keys in its quoting set, so raw shell steps re-render them
single-quoted.

## Contents

- **Functions:** [`token_keys`](#token_keys), [`build_tokens`](#build_tokens)

## Functions

<a id="token_keys"></a>

### `token_keys`

`function` | [modules/chain_tokens.py:24](../../modules/chain_tokens.py#L24)

```python
def token_keys() -> tuple[str, ...]
```

Return every engagement token name this module can produce.

**Returns:** `tuple[str, ...]`

---

<a id="build_tokens"></a>

### `build_tokens`

`function` | [modules/chain_tokens.py:29](../../modules/chain_tokens.py#L29)

```python
def build_tokens(target: str, params: dict | None = None) -> dict[str, str]
```

Resolve engagement tokens for one target.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  | E.g. ``172.17.0.2``; empty disables resolution. |
| `params` | `dict \| None` | `None` | Unused today; reserved so callers can extend sources. |

**Returns:** `dict[str, str]` - Mapping with discovered tokens only (unknown facts are absent).
Failures never raise: an unresponsive fact store yields fewer
tokens instead of breaking the chain run.

---
