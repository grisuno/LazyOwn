# `poc_tui.config`

> Source: [poc_tui/config.py:1](../../poc_tui/config.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

Payload.json configuration manager for the TUI shell.

## Contents

- **Classes:** [`PayloadConfig`](#payloadconfig)

## Classes

<a id="payloadconfig"></a>

### `PayloadConfig`

`class` `dataclass` | [poc_tui/config.py:12](../../poc_tui/config.py#L12)

Decorators: `@dataclass`

```python
class PayloadConfig
```

Read/write access to payload.json settings.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`path`](#payloadconfig-path) | `Path` |  |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`reload`](#payloadconfig-reload) | method | Re-read payload.json from disk. |
| [`save`](#payloadconfig-save) | method | Persist current state back to payload.json. |
| [`get`](#payloadconfig-get) | method |  |
| [`set`](#payloadconfig-set) | method |  |
| [`keys`](#payloadconfig-keys) | method |  |
| [`items`](#payloadconfig-items) | method |  |

<a id="payloadconfig-reload"></a>

#### `PayloadConfig.reload`

`method` | [poc_tui/config.py:21](../../poc_tui/config.py#L21)

```python
def reload(self) -> None
```

Re-read payload.json from disk.

<a id="payloadconfig-save"></a>

#### `PayloadConfig.save`

`method` | [poc_tui/config.py:28](../../poc_tui/config.py#L28)

```python
def save(self) -> None
```

Persist current state back to payload.json.

<a id="payloadconfig-get"></a>

#### `PayloadConfig.get`

`method` | [poc_tui/config.py:35](../../poc_tui/config.py#L35)

```python
def get(self, key: str, default: Any = None) -> Any
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `key` | `str` |  |  |
| `default` | `Any` | `None` |  |

**Returns:** `Any`

<a id="payloadconfig-set"></a>

#### `PayloadConfig.set`

`method` | [poc_tui/config.py:38](../../poc_tui/config.py#L38)

```python
def set(self, key: str, value: Any) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `key` | `str` |  |  |
| `value` | `Any` |  |  |

<a id="payloadconfig-keys"></a>

#### `PayloadConfig.keys`

`method` | [poc_tui/config.py:41](../../poc_tui/config.py#L41)

```python
def keys(self)
```

<a id="payloadconfig-items"></a>

#### `PayloadConfig.items`

`method` | [poc_tui/config.py:44](../../poc_tui/config.py#L44)

```python
def items(self)
```

---
