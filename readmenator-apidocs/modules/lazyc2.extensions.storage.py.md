# `lazyc2.extensions.storage`

> Source: [lazyc2/extensions/storage.py:1](../../lazyc2/extensions/storage.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

JSON-file storage helpers for the C2 web interface.

Provides load/save helpers for tasks, CVEs, notes, events,
notifications, banners, and dynamic routes. All files live under
``sessions/`` and are managed with atomic write patterns.

## Contents

- **Functions:** [`configure`](#configure), [`load_tasks`](#load_tasks), [`save_tasks`](#save_tasks), [`load_cves`](#load_cves), [`save_cves`](#save_cves), [`load_note`](#load_note), [`save_note`](#save_note), [`load_event_config`](#load_event_config), [`load_notifications`](#load_notifications), [`load_banners`](#load_banners), [`load_routes`](#load_routes), [`save_routes`](#save_routes)
- **Constants:** [`SESSION_DIR`](#session_dir)

## Functions

<a id="configure"></a>

### `configure`

`function` | [lazyc2/extensions/storage.py:18](../../lazyc2/extensions/storage.py#L18)

```python
def configure(sessions_dir: str = 'sessions') -> None
```

Set the session directory path.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sessions_dir` | `str` | `'sessions'` | Path to the session storage directory. |

---

<a id="load_tasks"></a>

### `load_tasks`

`function` | [lazyc2/extensions/storage.py:31](../../lazyc2/extensions/storage.py#L31)

```python
def load_tasks() -> list[dict]
```

Load tasks from ``sessions/tasks.json``.

**Returns:** `list[dict]` - A list of task dicts.

*Called by:* [`edit_task`](lazyc2.blueprints.operations.py.md#edit_task), [`get_tasks`](lazyc2.blueprints.operations.py.md#get_tasks), [`task_detail`](lazyc2.blueprints.operations.py.md#task_detail), [`tasks`](lazyc2.blueprints.operations.py.md#tasks)

---

<a id="save_tasks"></a>

### `save_tasks`

`function` | [lazyc2/extensions/storage.py:45](../../lazyc2/extensions/storage.py#L45)

```python
def save_tasks(tasks: list[dict]) -> None
```

Persist tasks to ``sessions/tasks.json``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `tasks` | `list[dict]` |  | List of task dicts. |

*Called by:* [`edit_task`](lazyc2.blueprints.operations.py.md#edit_task)

---

<a id="load_cves"></a>

### `load_cves`

`function` | [lazyc2/extensions/storage.py:59](../../lazyc2/extensions/storage.py#L59)

```python
def load_cves() -> list[dict]
```

Load CVEs from ``sessions/cves.json``.

**Returns:** `list[dict]` - A list of CVE dicts.

*Called by:* [`cve_detail`](lazyc2.blueprints.operations.py.md#cve_detail), [`cves`](lazyc2.blueprints.operations.py.md#cves), [`edit_cve`](lazyc2.blueprints.operations.py.md#edit_cve)

---

<a id="save_cves"></a>

### `save_cves`

`function` | [lazyc2/extensions/storage.py:73](../../lazyc2/extensions/storage.py#L73)

```python
def save_cves(cves: list[dict]) -> None
```

Persist CVEs to ``sessions/cves.json``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `cves` | `list[dict]` |  | List of CVE dicts. |

*Called by:* [`cves`](lazyc2.blueprints.operations.py.md#cves), [`edit_cve`](lazyc2.blueprints.operations.py.md#edit_cve)

---

<a id="load_note"></a>

### `load_note`

`function` | [lazyc2/extensions/storage.py:87](../../lazyc2/extensions/storage.py#L87)

```python
def load_note() -> dict
```

Load the operator note from ``sessions/notes.txt``.

**Returns:** `dict` - A dict with a single `[`content`](skills.lazyown_context.py.md#compactionresult-content)` key.

*Called by:* [`edit_notes`](lazyc2.blueprints.operations.py.md#edit_notes), [`get_notes`](lazyc2.blueprints.operations.py.md#get_notes), [`view_note`](lazyc2.blueprints.operations.py.md#view_note)

---

<a id="save_note"></a>

### `save_note`

`function` | [lazyc2/extensions/storage.py:107](../../lazyc2/extensions/storage.py#L107)

```python
def save_note(content: str) -> None
```

Persist the operator note to ``sessions/notes.txt``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `content` | `str` |  | Note body string. |

*Called by:* [`edit_notes`](lazyc2.blueprints.operations.py.md#edit_notes)

---

<a id="load_event_config"></a>

### `load_event_config`

`function` | [lazyc2/extensions/storage.py:121](../../lazyc2/extensions/storage.py#L121)

```python
def load_event_config() -> dict
```

Load event configuration from ``event_config.json``.

**Returns:** `dict` - A dict with an ``events`` list, or an empty config.

*Called by:* [`event_config`](lazyc2.blueprints.operations.py.md#event_config), [`event_config_view`](lazyc2.blueprints.operations.py.md#event_config_view), [`events`](lazyc2.blueprints.operations.py.md#events)

---

<a id="load_notifications"></a>

### `load_notifications`

`function` | [lazyc2/extensions/storage.py:137](../../lazyc2/extensions/storage.py#L137)

```python
def load_notifications() -> list[dict]
```

Load notifications from ``sessions/notifications.json``.

**Returns:** `list[dict]` - A list of notification dicts.

---

<a id="load_banners"></a>

### `load_banners`

`function` | [lazyc2/extensions/storage.py:154](../../lazyc2/extensions/storage.py#L154)

```python
def load_banners() -> list | None
```

Load banners from ``sessions/banners.json``.

**Returns:** `list | None` - A list of banner dicts, or ``None`` when the file is absent.

---

<a id="load_routes"></a>

### `load_routes`

`function` | [lazyc2/extensions/storage.py:179](../../lazyc2/extensions/storage.py#L179)

```python
def load_routes() -> dict
```

Load dynamic routes from ``sessions/routes_to_templates.json``.

**Returns:** `dict` - A dict mapping route paths to template names.

---

<a id="save_routes"></a>

### `save_routes`

`function` | [lazyc2/extensions/storage.py:194](../../lazyc2/extensions/storage.py#L194)

```python
def save_routes(routes: dict) -> None
```

Persist dynamic routes with atomic write and safe permissions.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `routes` | `dict` |  | Dict mapping route paths to template names. |

---

## Constants

<a id="session_dir"></a>

### `SESSION_DIR`

`constant` | [lazyc2/extensions/storage.py:15](../../lazyc2/extensions/storage.py#L15)

```python
SESSION_DIR = 'sessions'
```

---
