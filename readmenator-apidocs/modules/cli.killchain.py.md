# `cli.killchain`

> Source: [cli/killchain.py:1](../../cli/killchain.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Backward-compat kill-chain progress types for the dashboard TUI.

The canonical phase definitions and progress computation live in
`[`modules.killchain.KillChain`](modules.killchain.py.md#killchain)`, which already wraps `[`WorldModel`](modules.world_model.py.md#worldmodel)` and
raw ``world_model.json``. Consumers should migrate there. What remains
here is only the [`PhaseProgress`](#phaseprogress) dataclass the TUI imports.

## Contents

- **Classes:** [`PhaseProgress`](#phaseprogress)
- **Constants:** [`STATE_DONE`](#state_done), [`STATE_ACTIVE`](#state_active), [`STATE_PENDING`](#state_pending)

## Classes

<a id="phaseprogress"></a>

### `PhaseProgress`

`class` `dataclass` | [cli/killchain.py:19](../../cli/killchain.py#L19)

Decorators: `@dataclass(frozen=True)`

```python
class PhaseProgress
```

Computed progress for a single kill-chain phase.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`key`](#phaseprogress-key) | `str` |  | Canonical phase identifier (e.g. ``recon``). |
| [`label`](#phaseprogress-label) | `str` |  | Human-readable phase label (e.g. ``Recon``). |
| [`state`](#phaseprogress-state) | `str` |  | One of [`STATE_DONE`](#state_done), [`STATE_ACTIVE`](#state_active), [`STATE_PENDING`](#state_pending). |
| [`activity`](#phaseprogress-activity) | `int` |  | Number of daemon step events observed in this phase. |
| [`reward`](#phaseprogress-reward) | `float` |  | Sum of step rewards recorded in this phase. |

---

## Constants

<a id="state_done"></a>

### `STATE_DONE`

`constant` | [cli/killchain.py:13](../../cli/killchain.py#L13)

```python
STATE_DONE: str = 'done'
```

---

<a id="state_active"></a>

### `STATE_ACTIVE`

`constant` | [cli/killchain.py:14](../../cli/killchain.py#L14)

```python
STATE_ACTIVE: str = 'active'
```

---

<a id="state_pending"></a>

### `STATE_PENDING`

`constant` | [cli/killchain.py:15](../../cli/killchain.py#L15)

```python
STATE_PENDING: str = 'pending'
```

---
