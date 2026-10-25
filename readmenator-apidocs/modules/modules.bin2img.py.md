# `modules.bin2img`

> Source: [modules/bin2img.py:1](../../modules/bin2img.py#L1) | language `py` | coverage 0.0% | [API index](../index.md)

## Contents

- **Functions:** [`binario_a_imagen`](#binario_a_imagen), [`main`](#main)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_bin2img_py__main(["main"])
    n_modules_bin2img_py__binario_a_imagen(["binario_a_imagen"])
    n_modules_bin2img_py__main --> n_modules_bin2img_py__binario_a_imagen
```

## Functions

<a id="binario_a_imagen"></a>

### `binario_a_imagen`

`function` | [modules/bin2img.py:7](../../modules/bin2img.py#L7)

```python
def binario_a_imagen(binario, imagen_input, imagen_output, block_size=4)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `binario` |  |  |  |
| `imagen_input` |  |  |  |
| `imagen_output` |  |  |  |
| `block_size` |  | `4` |  |

*Called by:* [`main`](#main)

---

<a id="main"></a>

### `main`

`function` | [modules/bin2img.py:54](../../modules/bin2img.py#L54)

```python
def main()
```

*Calls:* [`binario_a_imagen`](#binario_a_imagen)

---
