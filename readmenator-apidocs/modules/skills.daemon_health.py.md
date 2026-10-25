# `skills.daemon_health`

> Source: [skills/daemon_health.py:1](../../skills/daemon_health.py#L1) | language `py` | coverage 83.3% | [API index](../index.md)

Daemon health monitor — watchdog for the autonomous daemon and C2 listeners.

Writes periodic heartbeat timestamps and provides a simple liveness check
so other components (MCP, C2 API, CLI) can detect a crashed daemon.

Health file: ``sessions/daemon_health.json``

Usage:
    from skills.daemon_health import DaemonHealth, is_daemon_alive

    health = DaemonHealth()
    health.start(interval=5)   # background thread, writes every 5s
    ...
    if is_daemon_alive():
        print("daemon is running")

## Contents

- **Classes:** [`DaemonHealth`](#daemonhealth)
- **Functions:** [`is_daemon_alive`](#is_daemon_alive), [`daemon_status`](#daemon_status)
- **Constants:** [`DEFAULT_HEALTH_FILE`](#default_health_file), [`DEFAULT_INTERVAL`](#default_interval), [`DEFAULT_TIMEOUT`](#default_timeout)

## Classes

<a id="daemonhealth"></a>

### `DaemonHealth`

`class` | [skills/daemon_health.py:94](../../skills/daemon_health.py#L94)

```python
class DaemonHealth
```

Background thread that writes a heartbeat timestamp periodically.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `interval` |  |  | Seconds between heartbeats. |
| `health_file` |  |  | Path to the health JSON file. |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#daemonhealth-__init__) | constructor |  |
| [`error_count`](#daemonhealth-error_count) | property |  |
| [`error_count`](#daemonhealth-error_count) | property |  |
| [`phase`](#daemonhealth-phase) | property |  |
| [`phase`](#daemonhealth-phase) | property |  |
| [`start`](#daemonhealth-start) | method | Launch the heartbeat thread. |
| [`stop`](#daemonhealth-stop) | method | Stop the heartbeat thread. |
| [`record_error`](#daemonhealth-record_error) | method | Increment the error counter. |
| [`set_phase`](#daemonhealth-set_phase) | method | Update the current daemon phase. |
| [`increment_cycles`](#daemonhealth-increment_cycles) | method | Increment the completed cycles counter. |

<a id="daemonhealth-__init__"></a>

#### `DaemonHealth.__init__`

`constructor` | [skills/daemon_health.py:102](../../skills/daemon_health.py#L102)

```python
def __init__(self, interval: int = DEFAULT_INTERVAL, health_file: str | None = None)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `interval` | `int` | `DEFAULT_INTERVAL` | Seconds between heartbeats. |
| `health_file` | `str \| None` | `None` | Path to the health JSON file. |

<a id="daemonhealth-error_count"></a>

#### `DaemonHealth.error_count`

`property` | [skills/daemon_health.py:119](../../skills/daemon_health.py#L119)

Decorators: `@error_count.setter`

```python
def error_count(self, value: int)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `int` |  |  |

<a id="daemonhealth-error_count"></a>

#### `DaemonHealth.error_count`

`property` | [skills/daemon_health.py:119](../../skills/daemon_health.py#L119)

Decorators: `@error_count.setter`

```python
def error_count(self, value: int)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `int` |  |  |

<a id="daemonhealth-phase"></a>

#### `DaemonHealth.phase`

`property` | [skills/daemon_health.py:129](../../skills/daemon_health.py#L129)

Decorators: `@phase.setter`

```python
def phase(self, value: str)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `str` |  |  |

<a id="daemonhealth-phase"></a>

#### `DaemonHealth.phase`

`property` | [skills/daemon_health.py:129](../../skills/daemon_health.py#L129)

Decorators: `@phase.setter`

```python
def phase(self, value: str)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `str` |  |  |

<a id="daemonhealth-start"></a>

#### `DaemonHealth.start`

`method` | [skills/daemon_health.py:155](../../skills/daemon_health.py#L155)

```python
def start(self)
```

Launch the heartbeat thread.

<a id="daemonhealth-stop"></a>

#### `DaemonHealth.stop`

`method` | [skills/daemon_health.py:164](../../skills/daemon_health.py#L164)

```python
def stop(self)
```

Stop the heartbeat thread.

<a id="daemonhealth-record_error"></a>

#### `DaemonHealth.record_error`

`method` | [skills/daemon_health.py:175](../../skills/daemon_health.py#L175)

```python
def record_error(self)
```

Increment the error counter.

<a id="daemonhealth-set_phase"></a>

#### `DaemonHealth.set_phase`

`method` | [skills/daemon_health.py:180](../../skills/daemon_health.py#L180)

```python
def set_phase(self, phase: str)
```

Update the current daemon phase.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `phase` | `str` |  |  |

<a id="daemonhealth-increment_cycles"></a>

#### `DaemonHealth.increment_cycles`

`method` | [skills/daemon_health.py:185](../../skills/daemon_health.py#L185)

```python
def increment_cycles(self)
```

Increment the completed cycles counter.

---

## Functions

<a id="is_daemon_alive"></a>

### `is_daemon_alive`

`function` | [skills/daemon_health.py:36](../../skills/daemon_health.py#L36)

```python
def is_daemon_alive(timeout: int = DEFAULT_TIMEOUT) -> bool
```

Check whether the autonomous daemon wrote a heartbeat recently.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `timeout` | `int` | `DEFAULT_TIMEOUT` | Maximum seconds since last heartbeat before considering dead. |

**Returns:** `bool` - True when a heartbeat exists and was written within ``timeout`` seconds.

---

<a id="daemon_status"></a>

### `daemon_status`

`function` | [skills/daemon_health.py:58](../../skills/daemon_health.py#L58)

```python
def daemon_status(timeout: int = DEFAULT_TIMEOUT) -> dict
```

Return the full daemon health snapshot.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `timeout` | `int` | `DEFAULT_TIMEOUT` | Maximum seconds since last heartbeat. |

**Returns:** `dict` - Dict with ``alive``, ``last_heartbeat``, ``uptime_seconds``,
``pid``, `[`phase`](#daemonhealth-phase)`, `[`error_count`](#daemonhealth-error_count)` keys.

---

## Constants

<a id="default_health_file"></a>

### `DEFAULT_HEALTH_FILE`

`constant` | [skills/daemon_health.py:27](../../skills/daemon_health.py#L27)

```python
DEFAULT_HEALTH_FILE = 'sessions/daemon_health.json'
```

---

<a id="default_interval"></a>

### `DEFAULT_INTERVAL`

`constant` | [skills/daemon_health.py:28](../../skills/daemon_health.py#L28)

```python
DEFAULT_INTERVAL = 5
```

---

<a id="default_timeout"></a>

### `DEFAULT_TIMEOUT`

`constant` | [skills/daemon_health.py:29](../../skills/daemon_health.py#L29)

```python
DEFAULT_TIMEOUT = 30
```

---
