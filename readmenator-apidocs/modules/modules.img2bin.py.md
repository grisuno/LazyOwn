# `modules.img2bin`

> Source: [modules/img2bin.py:1](../../modules/img2bin.py#L1) | language `py` | coverage 0.0% | [API index](../index.md)

## Contents

- **Functions:** [`imagen_a_binario`](#imagen_a_binario), [`main`](#main)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_img2bin_py__main(["main"])
    n_modules_img2bin_py__imagen_a_binario(["imagen_a_binario"])
    n_modules_img2bin_py__main --> n_modules_img2bin_py__imagen_a_binario
```

## Functions

<a id="imagen_a_binario"></a>

### `imagen_a_binario`

`function` | [modules/img2bin.py:7](../../modules/img2bin.py#L7)

```python
def imagen_a_binario(imagen_input, binario_output, block_size=4)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `imagen_input` |  |  |  |
| `binario_output` |  |  |  |
| `block_size` |  | `4` |  |

*Called by:* [`main`](#main)

---

<a id="main"></a>

### `main`

`function` | [modules/img2bin.py:43](../../modules/img2bin.py#L43)

```python
def main()
```

*Calls:* [`imagen_a_binario`](#imagen_a_binario)

---
