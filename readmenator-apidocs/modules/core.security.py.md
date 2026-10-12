# `core.security`

> Source: [core/security.py:1](../../core/security.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Security helpers for LazyOwn — anti-debug, certificate generation.

Extracted from ``utils.py`` to break the giant monolith and keep
security-critical code in one auditable location.

## Contents

- **Functions:** [`anti_debug`](#anti_debug), [`generate_certificates`](#generate_certificates)

## Functions

<a id="anti_debug"></a>

### `anti_debug`

`function` | [core/security.py:18](../../core/security.py#L18)

```python
def anti_debug() -> None
```

Check for debugger attachment and exit if found.

Reads ``/proc/self/status`` for ``TracerPid``. If a tracer is
attached and we are not running under a legitimate dev tool
(gdb, strace, ltrace will show), the process exits immediately.

This is called at import time by both ``lazyown.py`` and
``lazyc2.py``.

---

<a id="generate_certificates"></a>

### `generate_certificates`

`function` | [core/security.py:58](../../core/security.py#L58)

```python
def generate_certificates(output_dir: str | None = None) -> tuple[str, str]
```

Generate a self-signed CA certificate and key pair.

Creates ``cert.pem`` and ``key.pem`` in the current directory (or
``output_dir`` if specified). Uses OpenSSL with 4096-bit RSA and
a 3650-day validity period.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `output_dir` | `str \| None` | `None` | Optional directory to write the certificate files into. Defaults to the current working directory. |

**Returns:** `tuple[str, str]` - Tuple of ``(cert_path, key_path)`` absolute paths.

---
