# `lazyc2.security.validators`

> Source: [lazyc2/security/validators.py:1](../../lazyc2/security/validators.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Input validators for the LazyOwn C2 web layer.

All validation functions are pure, stateless, and operate only on
primitive types. They return ``(bool, str)`` tuples to enable
detailed error messages without raising exceptions.

## Contents

- **Functions:** [`validate_route_path`](#validate_route_path), [`validate_template_name`](#validate_template_name), [`validate_yaml_filename`](#validate_yaml_filename), [`validate_request_data`](#validate_request_data), [`validate_aes_key`](#validate_aes_key), [`validate_password_length`](#validate_password_length), [`validate_upload_size`](#validate_upload_size), [`validate_file_path_within_base`](#validate_file_path_within_base), [`resolve_contained_file_path`](#resolve_contained_file_path)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_lazyc2_security_validators_py__resolve_contained_file_path(["resolve_contained_file_path"])
    n_lazyc2_security_validators_py__validate_file_path_within_base(["validate_file_path_within_base"])
    n_lazyc2_security_validators_py__resolve_contained_file_path --> n_lazyc2_security_validators_py__validate_file_path_within_base
```

## Functions

<a id="validate_route_path"></a>

### `validate_route_path`

`function` | [lazyc2/security/validators.py:24](../../lazyc2/security/validators.py#L24)

```python
def validate_route_path(route_path: str) -> tuple[bool, str]
```

Validate a dynamic route path segment.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `route_path` | `str` |  | The route path to validate. |

**Returns:** `tuple[bool, str]` - A tuple of (is_valid, error_message).

---

<a id="validate_template_name"></a>

### `validate_template_name`

`function` | [lazyc2/security/validators.py:46](../../lazyc2/security/validators.py#L46)

```python
def validate_template_name(template_name: str) -> tuple[bool, str]
```

Validate a Jinja2 template filename.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `template_name` | `str` |  | The template name to validate. |

**Returns:** `tuple[bool, str]` - A tuple of (is_valid, error_message).

---

<a id="validate_yaml_filename"></a>

### `validate_yaml_filename`

`function` | [lazyc2/security/validators.py:68](../../lazyc2/security/validators.py#L68)

```python
def validate_yaml_filename(filename: str) -> tuple[bool, str]
```

Validate a YAML filename for safe loading.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  | The filename to validate. |

**Returns:** `tuple[bool, str]` - A tuple of (is_valid, error_message).

---

<a id="validate_request_data"></a>

### `validate_request_data`

`function` | [lazyc2/security/validators.py:86](../../lazyc2/security/validators.py#L86)

```python
def validate_request_data(data: str) -> tuple[bool, str]
```

Validate request data length to prevent buffer abuse.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `str` |  | The data string to validate. |

**Returns:** `tuple[bool, str]` - A tuple of (is_valid, error_message).

---

<a id="validate_aes_key"></a>

### `validate_aes_key`

`function` | [lazyc2/security/validators.py:102](../../lazyc2/security/validators.py#L102)

```python
def validate_aes_key(key: bytes) -> tuple[bool, str]
```

Validate AES key length.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `key` | `bytes` |  | The AES key bytes to validate. |

**Returns:** `tuple[bool, str]` - A tuple of (is_valid, error_message).

*Called by:* [`AESKeyManager.get_or_generate`](lazyc2.security.services.py.md#aeskeymanager-get_or_generate)

---

<a id="validate_password_length"></a>

### `validate_password_length`

`function` | [lazyc2/security/validators.py:118](../../lazyc2/security/validators.py#L118)

```python
def validate_password_length(password: str) -> tuple[bool, str]
```

Validate password meets minimum length requirement.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `password` | `str` |  | The password to validate. |

**Returns:** `tuple[bool, str]` - A tuple of (is_valid, error_message).

---

<a id="validate_upload_size"></a>

### `validate_upload_size`

`function` | [lazyc2/security/validators.py:134](../../lazyc2/security/validators.py#L134)

```python
def validate_upload_size(content_length: int | None) -> tuple[bool, str]
```

Validate upload size against maximum allowed.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `content_length` | `int \| None` |  | The content length header value. |

**Returns:** `tuple[bool, str]` - A tuple of (is_valid, error_message).

---

<a id="validate_file_path_within_base"></a>

### `validate_file_path_within_base`

`function` | [lazyc2/security/validators.py:150](../../lazyc2/security/validators.py#L150)

```python
def validate_file_path_within_base(file_path: Path, base_dir: Path) -> tuple[bool, str]
```

Validate that a resolved file path is within a base directory.

Uses Path.resolve() to canonicalize paths and Path.relative_to()
to detect traversal. This is safer than string-based checks.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `file_path` | `Path` |  | The path to validate (may contain traversal). |
| `base_dir` | `Path` |  | The allowed base directory. |

**Returns:** `tuple[bool, str]` - A tuple of (is_valid, error_message).

*Called by:* [`resolve_contained_file_path`](#resolve_contained_file_path)

---

<a id="resolve_contained_file_path"></a>

### `resolve_contained_file_path`

`function` | [lazyc2/security/validators.py:174](../../lazyc2/security/validators.py#L174)

```python
def resolve_contained_file_path(raw_url: str, base_dir: Path) -> Path | None
```

Resolve a short-URL target to a file path contained in ``base_dir``.

Accepts ``file://`` URLs and bare filesystem paths. Remote ``http`` /
``https`` targets are not files, so this returns ``None`` for them and
the caller falls back to an HTTP redirect. Symlinks are resolved
before the containment check, so a link inside the base directory
pointing outside is rejected.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `raw_url` | `str` |  | Short-URL target as stored in the registry. |
| `base_dir` | `Path` |  | Allowed base directory (sessions directory). |

**Returns:** `Path | None` - Resolved absolute path when contained, else None.

*Calls:* [`validate_file_path_within_base`](#validate_file_path_within_base)

*Called by:* [`redirect_to_file`](lazyc2.blueprints.phishing.py.md#redirect_to_file)

---
