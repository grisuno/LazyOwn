# `contrib.legacy.lazyftpsniff`

> Source: [contrib/legacy/lazyftpsniff.py:1](../../contrib/legacy/lazyftpsniff.py#L1) | language `py` | coverage 0.0% | [API index](../index.md)

## Contents

- **Functions:** [`check_sudo`](#check_sudo), [`signal_handler`](#signal_handler), [`parse_arguments`](#parse_arguments), [`sniffer_ftp`](#sniffer_ftp), [`main`](#main)
- **Constants:** [`BANNER`](#banner)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_contrib_legacy_lazyftpsniff_py__main(["main"])
    n_contrib_legacy_lazyftpsniff_py__parse_arguments(["parse_arguments"])
    n_contrib_legacy_lazyftpsniff_py__main --> n_contrib_legacy_lazyftpsniff_py__parse_arguments
```

## Functions

<a id="check_sudo"></a>

### `check_sudo`

`function` | [contrib/legacy/lazyftpsniff.py:21](../../contrib/legacy/lazyftpsniff.py#L21)

```python
def check_sudo()
```

---

<a id="signal_handler"></a>

### `signal_handler`

`function` | [contrib/legacy/lazyftpsniff.py:34](../../contrib/legacy/lazyftpsniff.py#L34)

```python
def signal_handler(sig, frame)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sig` |  |  |  |
| `frame` |  |  |  |

---

<a id="parse_arguments"></a>

### `parse_arguments`

`function` | [contrib/legacy/lazyftpsniff.py:42](../../contrib/legacy/lazyftpsniff.py#L42)

```python
def parse_arguments()
```

*Called by:* [`main`](#main)

---

<a id="sniffer_ftp"></a>

### `sniffer_ftp`

`function` | [contrib/legacy/lazyftpsniff.py:56](../../contrib/legacy/lazyftpsniff.py#L56)

```python
def sniffer_ftp(pkt)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pkt` |  |  |  |

---

<a id="main"></a>

### `main`

`function` | [contrib/legacy/lazyftpsniff.py:69](../../contrib/legacy/lazyftpsniff.py#L69)

```python
def main()
```

*Calls:* [`parse_arguments`](#parse_arguments)

---

## Constants

<a id="banner"></a>

### `BANNER`

`constant` | [contrib/legacy/lazyftpsniff.py:9](../../contrib/legacy/lazyftpsniff.py#L9)

```python
BANNER
```

---
