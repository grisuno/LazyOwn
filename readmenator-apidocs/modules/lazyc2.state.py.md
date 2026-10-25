# `lazyc2.state`

> Source: [lazyc2/state.py:1](../../lazyc2/state.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Global C2 server state — namespace for shared mutable objects.

Extracted from lazyc2.py to break the circular dependency between
lazyc2.py and lazyc2/blueprints/. Both can import this module safely.

## Contents

- **Constants:** [`MODEL`](#model), [`JSON_FILE_PATH_REPORT`](#json_file_path_report), [`USER_DATA_PATH`](#user_data_path)
- **Variables:** [`shell`](#shell), [`implants`](#implants), [`commands`](#commands), [`results`](#results), [`commands_history`](#commands_history), [`remote_commands_history`](#remote_commands_history), [`connected_clients`](#connected_clients), [`events`](#events), [`counter_events`](#counter_events), [`listener_manager`](#listener_manager), [`login_manager`](#login_manager), [`socketio`](#socketio)

## Constants

<a id="model"></a>

### `MODEL`

`constant` | [lazyc2/state.py:21](../../lazyc2/state.py#L21)

```python
MODEL: Any = None
```

---

<a id="json_file_path_report"></a>

### `JSON_FILE_PATH_REPORT`

`constant` | [lazyc2/state.py:22](../../lazyc2/state.py#L22)

```python
JSON_FILE_PATH_REPORT: str = 'static/body_report.json'
```

---

<a id="user_data_path"></a>

### `USER_DATA_PATH`

`constant` | [lazyc2/state.py:23](../../lazyc2/state.py#L23)

```python
USER_DATA_PATH: str = 'users.json'
```

---

## Variables

<a id="shell"></a>

### `shell`

`variable` | [lazyc2/state.py:9](../../lazyc2/state.py#L9)

```python
shell: Any = None
```

---

<a id="implants"></a>

### `implants`

`variable` | [lazyc2/state.py:10](../../lazyc2/state.py#L10)

```python
implants: dict = None
```

---

<a id="commands"></a>

### `commands`

`variable` | [lazyc2/state.py:11](../../lazyc2/state.py#L11)

```python
commands: dict = None
```

---

<a id="results"></a>

### `results`

`variable` | [lazyc2/state.py:12](../../lazyc2/state.py#L12)

```python
results: dict = None
```

---

<a id="commands_history"></a>

### `commands_history`

`variable` | [lazyc2/state.py:13](../../lazyc2/state.py#L13)

```python
commands_history: dict = None
```

---

<a id="remote_commands_history"></a>

### `remote_commands_history`

`variable` | [lazyc2/state.py:14](../../lazyc2/state.py#L14)

```python
remote_commands_history: dict = None
```

---

<a id="connected_clients"></a>

### `connected_clients`

`variable` | [lazyc2/state.py:15](../../lazyc2/state.py#L15)

```python
connected_clients: set = None
```

---

<a id="events"></a>

### `events`

`variable` | [lazyc2/state.py:16](../../lazyc2/state.py#L16)

```python
events: list = None
```

---

<a id="counter_events"></a>

### `counter_events`

`variable` | [lazyc2/state.py:17](../../lazyc2/state.py#L17)

```python
counter_events: int = 0
```

---

<a id="listener_manager"></a>

### `listener_manager`

`variable` | [lazyc2/state.py:18](../../lazyc2/state.py#L18)

```python
listener_manager: Any = None
```

---

<a id="login_manager"></a>

### `login_manager`

`variable` | [lazyc2/state.py:19](../../lazyc2/state.py#L19)

```python
login_manager: Any = None
```

---

<a id="socketio"></a>

### `socketio`

`variable` | [lazyc2/state.py:20](../../lazyc2/state.py#L20)

```python
socketio: Any = None
```

---
