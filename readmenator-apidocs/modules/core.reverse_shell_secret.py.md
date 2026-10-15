# `core.reverse_shell_secret`

> Source: [core/reverse_shell_secret.py:1](../../core/reverse_shell_secret.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Reverse-shell fallback secret — sealed persistence contract.

Single-responsibility home for the C2 ``/lazyos`` fallback password so the
logic is importable without the heavy `[`lazyc2`](lazyc2.__init__.py.md)` dependency chain (Flask,
dnslib, yagmail). ``lazyc2.py`` delegates to these helpers; tests target
this module directly.

Secrets are sealed with [`core.hardening.seal_secret`](core.hardening.py.md#seal_secret) (Fernet,
AES-128-CBC + HMAC, key from the shared ``key.aes`` resolver) and files
are written owner-only (0700 dir / 0600 file). Legacy plaintext files
still load so existing operator stores keep working.

## Contents

- **Functions:** [`seal_reverse_shell_password`](#seal_reverse_shell_password), [`load_reverse_shell_password`](#load_reverse_shell_password), [`generate_reverse_shell_password`](#generate_reverse_shell_password), [`is_configured_password_valid`](#is_configured_password_valid)
- **Constants:** [`REVERSE_SHELL_SECRET_FILENAME`](#reverse_shell_secret_filename), [`REVERSE_SHELL_PASSWORD_MIN_LENGTH`](#reverse_shell_password_min_length), [`REVERSE_SHELL_TOKEN_HEX_BYTES`](#reverse_shell_token_hex_bytes)

## Functions

<a id="seal_reverse_shell_password"></a>

### `seal_reverse_shell_password`

`function` | [core/reverse_shell_secret.py:24](../../core/reverse_shell_secret.py#L24)

```python
def seal_reverse_shell_password(plaintext: str) -> str
```

Seal a fallback password for storage.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `plaintext` | `str` |  | Generated fallback password. |

**Returns:** `str` - Sealed value when sealing resolves, else plaintext.

---

<a id="load_reverse_shell_password"></a>

### `load_reverse_shell_password`

`function` | [core/reverse_shell_secret.py:41](../../core/reverse_shell_secret.py#L41)

```python
def load_reverse_shell_password(secret_path: str | Path) -> str
```

Load a persisted fallback password, unsealing vault values.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `secret_path` | `str \| Path` |  | Path of the persisted fallback secret. |

**Returns:** `str` - Stored password, or empty string when unreadable.

---

<a id="generate_reverse_shell_password"></a>

### `generate_reverse_shell_password`

`function` | [core/reverse_shell_secret.py:65](../../core/reverse_shell_secret.py#L65)

```python
def generate_reverse_shell_password() -> str
```

Generate a fresh cryptographically random fallback password.

**Returns:** `str` - 64-character hex token (32 random bytes).

---

<a id="is_configured_password_valid"></a>

### `is_configured_password_valid`

`function` | [core/reverse_shell_secret.py:74](../../core/reverse_shell_secret.py#L74)

```python
def is_configured_password_valid(candidate: str, minimum_length: int = REVERSE_SHELL_PASSWORD_MIN_LENGTH) -> bool
```

Return True when an operator-configured password meets the floor.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `candidate` | `str` |  | Configured ``c2_reverse_shell_password`` value. |
| `minimum_length` | `int` | `REVERSE_SHELL_PASSWORD_MIN_LENGTH` | Minimum accepted length. |

**Returns:** `bool` - True when non-empty and at least ``minimum_length`` chars.

---

## Constants

<a id="reverse_shell_secret_filename"></a>

### `REVERSE_SHELL_SECRET_FILENAME`

`constant` | [core/reverse_shell_secret.py:19](../../core/reverse_shell_secret.py#L19)

```python
REVERSE_SHELL_SECRET_FILENAME = '.reverse_shell_password'
```

---

<a id="reverse_shell_password_min_length"></a>

### `REVERSE_SHELL_PASSWORD_MIN_LENGTH`

`constant` | [core/reverse_shell_secret.py:20](../../core/reverse_shell_secret.py#L20)

```python
REVERSE_SHELL_PASSWORD_MIN_LENGTH = 12
```

---

<a id="reverse_shell_token_hex_bytes"></a>

### `REVERSE_SHELL_TOKEN_HEX_BYTES`

`constant` | [core/reverse_shell_secret.py:21](../../core/reverse_shell_secret.py#L21)

```python
REVERSE_SHELL_TOKEN_HEX_BYTES = 32
```

---
