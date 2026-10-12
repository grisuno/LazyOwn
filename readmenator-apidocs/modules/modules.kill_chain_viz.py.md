# `modules.kill_chain_viz`

> Source: [modules/kill_chain_viz.py:1](../../modules/kill_chain_viz.py#L1) | language `py` | coverage 33.3% | [API index](../index.md)

SVG / HTML kill-chain visualizer — generates standalone HTML with embedded SVG.

Reads `[`modules.killchain.KillChain`](modules.killchain.py.md#killchain)` as the single source of truth.

## Contents

- **Functions:** [`generate_html`](#generate_html), [`generate_svg`](#generate_svg)

## Functions

<a id="generate_html"></a>

### `generate_html`

`function` | [modules/kill_chain_viz.py:69](../../modules/kill_chain_viz.py#L69)

```python
def generate_html(target: str = '', sessions: Path | None = None) -> str
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` | `''` |  |
| `sessions` | `Path \| None` | `None` |  |

**Returns:** `str`

---

<a id="generate_svg"></a>

### `generate_svg`

`function` | [modules/kill_chain_viz.py:102](../../modules/kill_chain_viz.py#L102)

```python
def generate_svg(target: str = '', sessions: Path | None = None) -> str
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` | `''` |  |
| `sessions` | `Path \| None` | `None` |  |

**Returns:** `str`

---
