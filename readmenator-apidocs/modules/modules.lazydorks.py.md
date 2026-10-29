# `modules.lazydorks`

> Source: [modules/lazydorks.py:1](../../modules/lazydorks.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

LazyDorks: target-aware Google and GitHub dork generator for LazyOwn.

Pure in-memory text generation that renders the classic sensitive-information
dork grammar (backend logins, upload pages, injectable URLs, directory
listings, open redirects, SQL errors, phpinfo, exposed files, leaked cloud
keys and GitHub org secrets) around one target domain. No network, no shell.

**Example**

```pycon
>>> from modules import lazydorks
>>> bool(lazydorks.queries("backend_logins", "example.com")[0])
True
```

## Contents

- **Functions:** [`categories`](#categories), [`queries`](#queries), [`all_queries`](#all_queries), [`write_report`](#write_report)
- **Constants:** [`MAX_QUERIES_PER_CATEGORY`](#max_queries_per_category), [`CATEGORIES`](#categories)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_lazydorks_py__all_queries(["all_queries"])
    n_modules_lazydorks_py__queries(["queries"])
    n_modules_lazydorks_py__write_report(["write_report"])
    n_modules_lazydorks_py__all_queries --> n_modules_lazydorks_py__queries
    n_modules_lazydorks_py__write_report --> n_modules_lazydorks_py__all_queries
```

## Functions

<a id="categories"></a>

### `categories`

`function` | [modules/lazydorks.py:96](../../modules/lazydorks.py#L96)

```python
def categories() -> tuple[str, ...]
```

Return every supported dork category.

**Returns:** `tuple[str, ...]`

---

<a id="queries"></a>

### `queries`

`function` | [modules/lazydorks.py:101](../../modules/lazydorks.py#L101)

```python
def queries(category: str, domain: str, org: str = '') -> tuple[str, ...]
```

Render the dork queries for one category against one target.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `category` | `str` |  | One of the names returned by [`categories`](#categories). |
| `domain` | `str` |  | Target domain to scope with ``site:``. |
| `org` | `str` | `''` | GitHub organisation name for the ``github_org`` category; falls back to ``domain`` when empty. |

**Returns:** `tuple[str, ...]` - Rendered queries capped at `[`MAX_QUERIES_PER_CATEGORY`](#max_queries_per_category)`; empty when
the domain is empty or the category is unknown.

*Called by:* [`LazyDorksCommandSet.do_lazydork`](cli.commands.lazy_dorks.py.md#lazydorkscommandset-do_lazydork), [`all_queries`](#all_queries)

---

<a id="all_queries"></a>

### `all_queries`

`function` | [modules/lazydorks.py:123](../../modules/lazydorks.py#L123)

```python
def all_queries(domain: str, org: str = '') -> dict[str, tuple[str, ...]]
```

Render the full grammar for one target.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `domain` | `str` |  | Target domain to scope with ``site:``. |
| `org` | `str` | `''` | GitHub organisation name; falls back to ``domain``. |

**Returns:** `dict[str, tuple[str, ...]]` - Mapping of category name to rendered queries (only populated sets).

*Calls:* [`queries`](#queries)

*Called by:* [`LazyDorksCommandSet.do_lazydork`](cli.commands.lazy_dorks.py.md#lazydorkscommandset-do_lazydork), [`write_report`](#write_report)

---

<a id="write_report"></a>

### `write_report`

`function` | [modules/lazydorks.py:137](../../modules/lazydorks.py#L137)

```python
def write_report(path: Path | str, domain: str, org: str = '') -> dict[str, Any]
```

Persist the rendered dorks as a markdown playbook.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `Path \| str` |  | Destination file (created/overwritten). |
| `domain` | `str` |  | Target domain. |
| `org` | `str` | `''` | GitHub organisation; falls back to ``domain``. |

**Returns:** `dict[str, Any]` - Mapping with ``written`` (query count), ``path`` and ``error``.

*Calls:* [`all_queries`](#all_queries)

---

## Constants

<a id="max_queries_per_category"></a>

### `MAX_QUERIES_PER_CATEGORY`

`constant` | [modules/lazydorks.py:18](../../modules/lazydorks.py#L18)

```python
MAX_QUERIES_PER_CATEGORY = 12
```

---

<a id="categories"></a>

### `CATEGORIES`

`constant` | [modules/lazydorks.py:20](../../modules/lazydorks.py#L20)

```python
CATEGORIES: tuple[str, ...]
```

---
