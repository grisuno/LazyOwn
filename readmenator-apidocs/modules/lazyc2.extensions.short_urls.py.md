# `lazyc2.extensions.short_urls`

> Source: [lazyc2/extensions/short_urls.py:1](../../lazyc2/extensions/short_urls.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Short URL management utilities for the C2 phishing module.

Provides load/save/validation helpers for short URL redirection
and phishing campaign tracking. Intended for internal use by
[`lazyc2.blueprints.phishing`](lazyc2.blueprints.phishing.py.md).

## Contents

- **Functions:** [`configure`](#configure), [`load_short_urls`](#load_short_urls), [`save_short_urls`](#save_short_urls), [`is_valid_url`](#is_valid_url)
- **Constants:** [`SHORT_URLS_FILE`](#short_urls_file), [`ALLOWED_BASE_DIR`](#allowed_base_dir)

## Functions

<a id="configure"></a>

### `configure`

`function` | [lazyc2/extensions/short_urls.py:21](../../lazyc2/extensions/short_urls.py#L21)

```python
def configure(sessions_phishing_dir: str) -> None
```

Set the phishing directory where short_urls.json lives.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sessions_phishing_dir` | `str` |  | Absolute or relative path to the phishing session directory. |

---

<a id="load_short_urls"></a>

### `load_short_urls`

`function` | [lazyc2/extensions/short_urls.py:33](../../lazyc2/extensions/short_urls.py#L33)

```python
def load_short_urls() -> dict
```

Load short URLs from JSON file, creating it if it doesn't exist.

**Returns:** `dict` - A dict mapping short URL keys to their metadata (original_url,
active, created_at).

*Called by:* [`create_short_url`](lazyc2.blueprints.phishing.py.md#create_short_url), [`download_files`](lazyc2.blueprints.phishing.py.md#download_files), [`redirect_to_file`](lazyc2.blueprints.phishing.py.md#redirect_to_file), [`track_interaction`](lazyc2.blueprints.phishing.py.md#track_interaction), [`update_short_url`](lazyc2.blueprints.phishing.py.md#update_short_url)

---

<a id="save_short_urls"></a>

### `save_short_urls`

`function` | [lazyc2/extensions/short_urls.py:59](../../lazyc2/extensions/short_urls.py#L59)

```python
def save_short_urls(data: dict) -> None
```

Save short URLs to JSON file.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `dict` |  | Dict mapping short URL keys to their metadata. |

*Called by:* [`create_short_url`](lazyc2.blueprints.phishing.py.md#create_short_url), [`update_short_url`](lazyc2.blueprints.phishing.py.md#update_short_url)

---

<a id="is_valid_url"></a>

### `is_valid_url`

`function` | [lazyc2/extensions/short_urls.py:104](../../lazyc2/extensions/short_urls.py#L104)

```python
def is_valid_url(url: str) -> bool
```

Validate if the input is a valid URL or existing local file path.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `url` | `str` |  | URL string or local file path to validate. |

**Returns:** `bool` - ``True`` when the value is a valid web URL or an existing local
file under the allowed base directory.

*Called by:* [`create_short_url`](lazyc2.blueprints.phishing.py.md#create_short_url), [`update_short_url`](lazyc2.blueprints.phishing.py.md#update_short_url)

---

## Constants

<a id="short_urls_file"></a>

### `SHORT_URLS_FILE`

`constant` | [lazyc2/extensions/short_urls.py:17](../../lazyc2/extensions/short_urls.py#L17)

```python
SHORT_URLS_FILE: str = ''
```

---

<a id="allowed_base_dir"></a>

### `ALLOWED_BASE_DIR`

`constant` | [lazyc2/extensions/short_urls.py:18](../../lazyc2/extensions/short_urls.py#L18)

```python
ALLOWED_BASE_DIR: str = ''
```

---
