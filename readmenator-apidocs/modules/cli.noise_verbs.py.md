# `cli.noise_verbs`

> Source: [cli/noise_verbs.py:1](../../cli/noise_verbs.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Canonical non-actionable verb registry for post-command surfaces.

The inline hints, the unified tips engine, and the interactive chain
prompt each skip a near-identical list of verbs that produce no
engagement progress (help, history, navigation, and configuration
commands). This module is the single source of truth for that
vocabulary so the three surfaces can never drift apart again.

Each surface composes its own exported set from the shared base plus
its surface-specific extras, keeping backwards-compatible names:

- `[`cli.reactive_hints.SKIP_COMMANDS`](cli.reactive_hints.py.md#skip_commands)` = base + graph hints extras
- `[`cli.tips_engine.SKIP_COMMANDS`](cli.tips_engine.py.md#skip_commands)` = base + tips extras
- `[`cli.chain_mode.CHAIN_SKIP_VERBS`](cli.chain_mode.py.md#chain_skip_verbs)` = base + chain extras

## Contents

- **Constants:** [`BASE_NOISE_VERBS`](#base_noise_verbs), [`HINTS_EXTRA_VERBS`](#hints_extra_verbs), [`TIPS_EXTRA_VERBS`](#tips_extra_verbs), [`CHAIN_EXTRA_VERBS`](#chain_extra_verbs)

## Constants

<a id="base_noise_verbs"></a>

### `BASE_NOISE_VERBS`

`constant` | [cli/noise_verbs.py:19](../../cli/noise_verbs.py#L19)

```python
BASE_NOISE_VERBS: frozenset[str]
```

---

<a id="hints_extra_verbs"></a>

### `HINTS_EXTRA_VERBS`

`constant` | [cli/noise_verbs.py:45](../../cli/noise_verbs.py#L45)

```python
HINTS_EXTRA_VERBS: frozenset[str] = frozenset({'suggest_next', 'graph_search', 'neighbors', 'god_nodes'})
```

---

<a id="tips_extra_verbs"></a>

### `TIPS_EXTRA_VERBS`

`constant` | [cli/noise_verbs.py:54](../../cli/noise_verbs.py#L54)

```python
TIPS_EXTRA_VERBS: frozenset[str]
```

---

<a id="chain_extra_verbs"></a>

### `CHAIN_EXTRA_VERBS`

`constant` | [cli/noise_verbs.py:72](../../cli/noise_verbs.py#L72)

```python
CHAIN_EXTRA_VERBS: frozenset[str]
```

---
