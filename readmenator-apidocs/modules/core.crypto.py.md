# `core.crypto`

> Source: [core/crypto.py:1](../../core/crypto.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Symmetric primitives used by the framework.

XOR (legacy), AES-256-GCM, key generation, and file-dropping utilities
extracted from ``utils.py``.

## Contents

- **Functions:** [`xor_encrypt_decrypt`](#xor_encrypt_decrypt), [`generate_xor_key`](#generate_xor_key), [`AESencrypt`](#aesencrypt), [`AESdecrypt`](#aesdecrypt), [`dropFile`](#dropfile)

## Functions

<a id="xor_encrypt_decrypt"></a>

### `xor_encrypt_decrypt`

`function` | [core/crypto.py:67](../../core/crypto.py#L67)

```python
def xor_encrypt_decrypt(data: ByteLike, key: str) -> bytearray
```

Return ``bytearray`` produced by XOR-ing each byte of ``data`` with `[`key`](key.py.md)`.

XOR is symmetric, so the same call encrypts and decrypts. The key is
cycled byte-by-byte over the data. `[`key`](key.py.md)` must be a non-empty string.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `ByteLike` |  |  |
| `key` | `str` |  |  |

**Returns:** `bytearray`

**Raises**

- `ValueError`: if `[`key`](key.py.md)` is empty.

*Called by:* [`ExfiltrationCommandSet.do_decrypt`](cli.commands.exfiltration.py.md#exfiltrationcommandset-do_decrypt), [`ExfiltrationCommandSet.do_encrypt`](cli.commands.exfiltration.py.md#exfiltrationcommandset-do_encrypt), [`ExfiltrationCommandSet.do_stage`](cli.commands.exfiltration.py.md#exfiltrationcommandset-do_stage)

---

<a id="generate_xor_key"></a>

### `generate_xor_key`

`function` | [core/crypto.py:83](../../core/crypto.py#L83)

```python
def generate_xor_key(length: int) -> str
```

Generate a random XOR key of the given length as a hex string.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `length` | `int` |  | Length of the XOR key in bytes. |

**Returns:** `str` - Hex-encoded key string.

**Raises**

- `ValueError`: (raised in the body, not documented)

*Called by:* [`PostexpMigratedCommandSet.do_createpayload`](cli.commands.postexp_migrated.py.md#postexpmigratedcommandset-do_createpayload)

---

<a id="aesencrypt"></a>

### `AESencrypt`

`function` | [core/crypto.py:98](../../core/crypto.py#L98)

```python
def AESencrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]
```

Encrypt `[`plaintext`](modules.domain_dominance.py.md#credentialstash-plaintext)` with AES-256-GCM using a random nonce.

Output format is ``nonce (12 bytes) || ciphertext || tag (16 bytes)``
so that `[`AESdecrypt`](#aesdecrypt)` can extract all three components.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `plaintext` | `bytes` |  | Data to encrypt. |
| `key` | `bytes` |  | Raw key material (SHA-256 hashed before use). |

**Returns:** `tuple[bytes, bytes]` - ``(ciphertext, key)`` tuple where ``ciphertext`` includes the
nonce and authentication tag prepended/appended.

*Called by:* [`PostexpMigratedCommandSet.do_aes_pe`](cli.commands.postexp_migrated.py.md#postexpmigratedcommandset-do_aes_pe), [`seal_value`](core.credential_vault.py.md#seal_value)

---

<a id="aesdecrypt"></a>

### `AESdecrypt`

`function` | [core/crypto.py:123](../../core/crypto.py#L123)

```python
def AESdecrypt(data: bytes, key: bytes) -> bytes
```

Decrypt data produced by `[`AESencrypt`](#aesencrypt)`.

Expects ``nonce (12 bytes) || ciphertext || tag (16 bytes)``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `bytes` |  | Encrypted payload with embedded nonce and tag. |
| `key` | `bytes` |  | The same key used during encryption. |

**Returns:** `bytes` - Decrypted plaintext.

**Raises**

- `ValueError`: If the authentication tag does not verify (data tampered or wrong key).

*Called by:* [`unseal_value`](core.credential_vault.py.md#unseal_value)

---

<a id="dropfile"></a>

### `dropFile`

`function` | [core/crypto.py:154](../../core/crypto.py#L154)

```python
def dropFile(key: bytes, ciphertext: bytes) -> None
```

Write AES key and ciphertext to ``sessions/cipher.bin`` and ``sessions/key.bin``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `key` | `bytes` |  | AES key bytes. |
| `ciphertext` | `bytes` |  | Encrypted payload bytes (includes nonce + tag). |

*Called by:* [`PostexpMigratedCommandSet.do_aes_pe`](cli.commands.postexp_migrated.py.md#postexpmigratedcommandset-do_aes_pe)

---
