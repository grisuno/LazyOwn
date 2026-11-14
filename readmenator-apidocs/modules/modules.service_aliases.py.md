# `modules.service_aliases`

> Source: [modules/service_aliases.py:1](../../modules/service_aliases.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Service alias knowledge for the matching surfaces.

One home for the alias tables consumed by the exploit chain (canonical
group expansion), the chain family normalizer (alias to canonical) and
the auto-registry trigger matcher (symmetric alias pairs). The three
views have different semantics and are kept as distinct named tables so
each consumer's matching behavior is unchanged while the knowledge
cannot drift between files.

## Contents

- **Constants:** [`CANONICAL_SERVICE_ALIASES`](#canonical_service_aliases), [`ALIAS_TO_CANONICAL`](#alias_to_canonical), [`ALIAS_PAIRS`](#alias_pairs)

## Constants

<a id="canonical_service_aliases"></a>

### `CANONICAL_SERVICE_ALIASES`

`constant` | [modules/service_aliases.py:13](../../modules/service_aliases.py#L13)

```python
CANONICAL_SERVICE_ALIASES: dict[str, list[str]]
```

---

<a id="alias_to_canonical"></a>

### `ALIAS_TO_CANONICAL`

`constant` | [modules/service_aliases.py:26](../../modules/service_aliases.py#L26)

```python
ALIAS_TO_CANONICAL: dict[str, str]
```

---

<a id="alias_pairs"></a>

### `ALIAS_PAIRS`

`constant` | [modules/service_aliases.py:35](../../modules/service_aliases.py#L35)

```python
ALIAS_PAIRS: dict[str, tuple[str, ...]]
```

---
