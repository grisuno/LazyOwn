# `lazyc2.security.constants`

> Source: [lazyc2/security/constants.py:1](../../lazyc2/security/constants.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Security constants and validation patterns for the LazyOwn C2 web layer.

All regex patterns, length limits, and allowlists are defined here
to ensure single-source-of-truth and eliminate magic numbers.

## Contents

- **Constants:** [`ROUTE_PATH_PATTERN`](#route_path_pattern), [`TEMPLATE_NAME_PATTERN`](#template_name_pattern), [`YAML_FILENAME_PATTERN`](#yaml_filename_pattern), [`MAX_ROUTE_PATH_LENGTH`](#max_route_path_length), [`MAX_TEMPLATE_NAME_LENGTH`](#max_template_name_length), [`MAX_REQUEST_DATA_LENGTH`](#max_request_data_length), [`MAX_UPLOAD_SIZE_BYTES`](#max_upload_size_bytes), [`AES_KEY_SIZE_BYTES`](#aes_key_size_bytes), [`MINIMUM_PASSWORD_LENGTH`](#minimum_password_length), [`ALLOWED_HTML_TAGS`](#allowed_html_tags), [`ALLOWED_HTML_ATTRIBUTES`](#allowed_html_attributes), [`SESSIONS_DIR_NAME`](#sessions_dir_name), [`TEMPLATES_DIR_NAME`](#templates_dir_name), [`UPLOADS_DIR_NAME`](#uploads_dir_name), [`TEMP_UPLOADS_DIR_NAME`](#temp_uploads_dir_name), [`FILE_PERMISSION_OWNER_RW`](#file_permission_owner_rw), [`DIR_PERMISSION_OWNER_RWX`](#dir_permission_owner_rwx), [`MAX_YAML_FILE_SIZE_BYTES`](#max_yaml_file_size_bytes)

## Constants

<a id="route_path_pattern"></a>

### `ROUTE_PATH_PATTERN`

`constant` | [lazyc2/security/constants.py:9](../../lazyc2/security/constants.py#L9)

```python
ROUTE_PATH_PATTERN = re.compile('^[a-zA-Z0-9/_-]+$')
```

---

<a id="template_name_pattern"></a>

### `TEMPLATE_NAME_PATTERN`

`constant` | [lazyc2/security/constants.py:10](../../lazyc2/security/constants.py#L10)

```python
TEMPLATE_NAME_PATTERN = re.compile('^[a-zA-Z0-9_.-]+\\.html$')
```

---

<a id="yaml_filename_pattern"></a>

### `YAML_FILENAME_PATTERN`

`constant` | [lazyc2/security/constants.py:11](../../lazyc2/security/constants.py#L11)

```python
YAML_FILENAME_PATTERN = re.compile('^[a-zA-Z0-9_.-]+\\.(yaml|yml)$')
```

---

<a id="max_route_path_length"></a>

### `MAX_ROUTE_PATH_LENGTH`

`constant` | [lazyc2/security/constants.py:13](../../lazyc2/security/constants.py#L13)

```python
MAX_ROUTE_PATH_LENGTH = 128
```

---

<a id="max_template_name_length"></a>

### `MAX_TEMPLATE_NAME_LENGTH`

`constant` | [lazyc2/security/constants.py:14](../../lazyc2/security/constants.py#L14)

```python
MAX_TEMPLATE_NAME_LENGTH = 128
```

---

<a id="max_request_data_length"></a>

### `MAX_REQUEST_DATA_LENGTH`

`constant` | [lazyc2/security/constants.py:15](../../lazyc2/security/constants.py#L15)

```python
MAX_REQUEST_DATA_LENGTH = 2000
```

---

<a id="max_upload_size_bytes"></a>

### `MAX_UPLOAD_SIZE_BYTES`

`constant` | [lazyc2/security/constants.py:16](../../lazyc2/security/constants.py#L16)

```python
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024
```

---

<a id="aes_key_size_bytes"></a>

### `AES_KEY_SIZE_BYTES`

`constant` | [lazyc2/security/constants.py:17](../../lazyc2/security/constants.py#L17)

```python
AES_KEY_SIZE_BYTES = 32
```

---

<a id="minimum_password_length"></a>

### `MINIMUM_PASSWORD_LENGTH`

`constant` | [lazyc2/security/constants.py:18](../../lazyc2/security/constants.py#L18)

```python
MINIMUM_PASSWORD_LENGTH = 12
```

---

<a id="allowed_html_tags"></a>

### `ALLOWED_HTML_TAGS`

`constant` | [lazyc2/security/constants.py:20](../../lazyc2/security/constants.py#L20)

```python
ALLOWED_HTML_TAGS
```

---

<a id="allowed_html_attributes"></a>

### `ALLOWED_HTML_ATTRIBUTES`

`constant` | [lazyc2/security/constants.py:46](../../lazyc2/security/constants.py#L46)

```python
ALLOWED_HTML_ATTRIBUTES = {'a': ['href', 'title'], '*': ['class']}
```

---

<a id="sessions_dir_name"></a>

### `SESSIONS_DIR_NAME`

`constant` | [lazyc2/security/constants.py:48](../../lazyc2/security/constants.py#L48)

```python
SESSIONS_DIR_NAME = 'sessions'
```

---

<a id="templates_dir_name"></a>

### `TEMPLATES_DIR_NAME`

`constant` | [lazyc2/security/constants.py:49](../../lazyc2/security/constants.py#L49)

```python
TEMPLATES_DIR_NAME = 'templates'
```

---

<a id="uploads_dir_name"></a>

### `UPLOADS_DIR_NAME`

`constant` | [lazyc2/security/constants.py:50](../../lazyc2/security/constants.py#L50)

```python
UPLOADS_DIR_NAME = 'uploads'
```

---

<a id="temp_uploads_dir_name"></a>

### `TEMP_UPLOADS_DIR_NAME`

`constant` | [lazyc2/security/constants.py:51](../../lazyc2/security/constants.py#L51)

```python
TEMP_UPLOADS_DIR_NAME = 'temp_uploads'
```

---

<a id="file_permission_owner_rw"></a>

### `FILE_PERMISSION_OWNER_RW`

`constant` | [lazyc2/security/constants.py:53](../../lazyc2/security/constants.py#L53)

```python
FILE_PERMISSION_OWNER_RW = 384
```

---

<a id="dir_permission_owner_rwx"></a>

### `DIR_PERMISSION_OWNER_RWX`

`constant` | [lazyc2/security/constants.py:54](../../lazyc2/security/constants.py#L54)

```python
DIR_PERMISSION_OWNER_RWX = 448
```

---

<a id="max_yaml_file_size_bytes"></a>

### `MAX_YAML_FILE_SIZE_BYTES`

`constant` | [lazyc2/security/constants.py:56](../../lazyc2/security/constants.py#L56)

```python
MAX_YAML_FILE_SIZE_BYTES = 10 * 1024 * 1024
```

---
