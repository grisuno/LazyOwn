# `modules.lazyownserver`

> Source: [modules/lazyownserver.py:1](../../modules/lazyownserver.py#L1) | language `py` | coverage 14.3% | [API index](../index.md)

main.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: AGPL v3

Descripción: Servidor LazyOwn RAT

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

## Contents

- **Functions:** [`signal_handler`](#signal_handler), [`pad`](#pad), [`encrypt`](#encrypt), [`decrypt`](#decrypt), [`handle_client`](#handle_client), [`main`](#main)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_lazyownserver_py__encrypt(["encrypt"])
    n_modules_lazyownserver_py__pad(["pad"])
    n_modules_lazyownserver_py__handle_client(["handle_client"])
    n_modules_lazyownserver_py__decrypt(["decrypt"])
    n_modules_lazyownserver_py__encrypt --> n_modules_lazyownserver_py__pad
    n_modules_lazyownserver_py__handle_client --> n_modules_lazyownserver_py__decrypt
    n_modules_lazyownserver_py__handle_client --> n_modules_lazyownserver_py__encrypt
```

## Functions

<a id="signal_handler"></a>

### `signal_handler`

`function` | [modules/lazyownserver.py:34](../../modules/lazyownserver.py#L34)

```python
def signal_handler(sig, frame)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sig` |  |  |  |
| `frame` |  |  |  |

---

<a id="pad"></a>

### `pad`

`function` | [modules/lazyownserver.py:42](../../modules/lazyownserver.py#L42)

```python
def pad(s)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `s` |  |  |  |

*Called by:* [`encrypt`](#encrypt)

---

<a id="encrypt"></a>

### `encrypt`

`function` | [modules/lazyownserver.py:46](../../modules/lazyownserver.py#L46)

```python
def encrypt(plaintext, key)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `plaintext` |  |  |  |
| `key` |  |  |  |

*Calls:* [`pad`](#pad)

*Called by:* [`handle_client`](#handle_client)

---

<a id="decrypt"></a>

### `decrypt`

`function` | [modules/lazyownserver.py:53](../../modules/lazyownserver.py#L53)

```python
def decrypt(ciphertext, key)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ciphertext` |  |  |  |
| `key` |  |  |  |

*Called by:* [`handle_client`](#handle_client)

---

<a id="handle_client"></a>

### `handle_client`

`function` | [modules/lazyownserver.py:60](../../modules/lazyownserver.py#L60)

```python
def handle_client(conn, addr, key)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `conn` |  |  |  |
| `addr` |  |  |  |
| `key` |  |  |  |

*Calls:* [`decrypt`](#decrypt), [`encrypt`](#encrypt)

---

<a id="main"></a>

### `main`

`function` | [modules/lazyownserver.py:97](../../modules/lazyownserver.py#L97)

```python
def main()
```

**Raises**

- `ValueError`: (raised in the body, not documented)

---
