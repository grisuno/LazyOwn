# `telegram_hermes`

> Source: [telegram_hermes.py:1](../../telegram_hermes.py#L1) | language `py` | coverage 10.0% | [API index](../index.md)

telegram_hermes.py LazyOwn Telegram Bot with Hermes Gateway Integration

This bot bridges Telegram to the full LazyOwn framework via the MCP layer
and Hermes gateway for autonomous task execution. It supports:
- Direct LazyOwn shell command execution
- Autonomous agent delegation (Groq/Ollama)
- Cron-scheduled tasks
- C2 beacon interaction
- Cross-platform messaging via Hermes gateway

Usage:
    python3 telegram_hermes.py

Configuration (payload.json keys):
    telegram_token       - Telegram bot token from @BotFather
    c2_pass              - Authentication secret for /start
    enable_ia            - Enable Groq AI processing (default: false)
    api_key              - Groq API key (if enable_ia is true)
    lhost, c2_port       - C2 server coordinates

## Contents

- **Classes:** [`SecureSessionManager`](#securesessionmanager)
- **Functions:** [`run_lazyown_command`](#run_lazyown_command), [`c2_request`](#c2_request), [`load_payload`](#load_payload), [`start`](#start), [`help_cmd`](#help_cmd), [`execute_command`](#execute_command), [`sitrep`](#sitrep), [`config_cmd`](#config_cmd), [`add_cli`](#add_cli), [`list_clients`](#list_clients), [`c2_command`](#c2_command), [`run_agent`](#run_agent), [`delegate_task_cmd`](#delegate_task_cmd), [`cron_schedule_cmd`](#cron_schedule_cmd), [`status_cmd`](#status_cmd), [`stop_daemon_cmd`](#stop_daemon_cmd), [`download_file_cmd`](#download_file_cmd), [`handle_file_upload`](#handle_file_upload), [`text_command`](#text_command), [`main`](#main)
- **Constants:** [`LAZYOWN_DIR`](#lazyown_dir), [`SESSIONS_DIR`](#sessions_dir), [`PAYLOAD_FILE`](#payload_file), [`SESSION_TIMEOUT`](#session_timeout), [`MAX_FAILED_ATTEMPTS`](#max_failed_attempts), [`RATE_LIMIT`](#rate_limit)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_telegram_hermes_py__execute_command(["execute_command"])
    n_telegram_hermes_py__run_lazyown_command(["run_lazyown_command"])
    n_telegram_hermes_py__sitrep(["sitrep"])
    n_telegram_hermes_py__config_cmd(["config_cmd"])
    n_telegram_hermes_py__load_payload(["load_payload"])
    n_telegram_hermes_py__list_clients(["list_clients"])
    n_telegram_hermes_py__c2_request(["c2_request"])
    n_telegram_hermes_py__c2_command(["c2_command"])
    n_telegram_hermes_py__run_agent(["run_agent"])
    n_telegram_hermes_py__delegate_task_cmd(["delegate_task_cmd"])
    n_telegram_hermes_py__cron_schedule_cmd(["cron_schedule_cmd"])
    n_telegram_hermes_py__status_cmd(["status_cmd"])
    n_telegram_hermes_py__stop_daemon_cmd(["stop_daemon_cmd"])
    n_telegram_hermes_py__handle_file_upload(["handle_file_upload"])
    n_telegram_hermes_py__text_command(["text_command"])
    n_core_parsers_py__strip_ansi["parsers.strip_ansi"]
    n_telegram_hermes_py__execute_command --> n_telegram_hermes_py__run_lazyown_command
    n_telegram_hermes_py__sitrep --> n_telegram_hermes_py__run_lazyown_command
    n_telegram_hermes_py__config_cmd --> n_telegram_hermes_py__load_payload
    n_telegram_hermes_py__list_clients --> n_telegram_hermes_py__c2_request
    n_telegram_hermes_py__c2_command --> n_telegram_hermes_py__c2_request
    n_telegram_hermes_py__run_agent --> n_telegram_hermes_py__run_lazyown_command
    n_telegram_hermes_py__delegate_task_cmd --> n_telegram_hermes_py__run_lazyown_command
    n_telegram_hermes_py__cron_schedule_cmd --> n_telegram_hermes_py__run_lazyown_command
    n_telegram_hermes_py__status_cmd --> n_telegram_hermes_py__run_lazyown_command
    n_telegram_hermes_py__stop_daemon_cmd --> n_telegram_hermes_py__run_lazyown_command
    n_telegram_hermes_py__handle_file_upload --> n_telegram_hermes_py__c2_request
    n_telegram_hermes_py__text_command --> n_telegram_hermes_py__c2_request
    n_telegram_hermes_py__text_command --> n_telegram_hermes_py__run_lazyown_command
    n_telegram_hermes_py__execute_command -.-> n_core_parsers_py__strip_ansi
    n_telegram_hermes_py__sitrep -.-> n_core_parsers_py__strip_ansi
    n_telegram_hermes_py__run_agent -.-> n_core_parsers_py__strip_ansi
    n_telegram_hermes_py__delegate_task_cmd -.-> n_core_parsers_py__strip_ansi
    n_telegram_hermes_py__cron_schedule_cmd -.-> n_core_parsers_py__strip_ansi
    n_telegram_hermes_py__status_cmd -.-> n_core_parsers_py__strip_ansi
    n_telegram_hermes_py__stop_daemon_cmd -.-> n_core_parsers_py__strip_ansi
    n_telegram_hermes_py__text_command -.-> n_core_parsers_py__strip_ansi
```

## Classes

<a id="securesessionmanager"></a>

### `SecureSessionManager`

`class` | [telegram_hermes.py:186](../../telegram_hermes.py#L186)

```python
class SecureSessionManager
```

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#securesessionmanager-__init__) | constructor |  |
| [`register_failed_attempt`](#securesessionmanager-register_failed_attempt) | method |  |
| [`check_lockout`](#securesessionmanager-check_lockout) | method |  |
| [`check_rate_limit`](#securesessionmanager-check_rate_limit) | method |  |
| [`create_session`](#securesessionmanager-create_session) | method |  |
| [`validate_session`](#securesessionmanager-validate_session) | method |  |
| [`get_client_id`](#securesessionmanager-get_client_id) | method |  |
| [`set_client_id`](#securesessionmanager-set_client_id) | method |  |

<a id="securesessionmanager-__init__"></a>

#### `SecureSessionManager.__init__`

`constructor` | [telegram_hermes.py:187](../../telegram_hermes.py#L187)

```python
def __init__(self)
```

<a id="securesessionmanager-register_failed_attempt"></a>

#### `SecureSessionManager.register_failed_attempt`

`method` | [telegram_hermes.py:192](../../telegram_hermes.py#L192)

```python
def register_failed_attempt(self, user_id: int)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `user_id` | `int` |  |  |

<a id="securesessionmanager-check_lockout"></a>

#### `SecureSessionManager.check_lockout`

`method` | [telegram_hermes.py:199](../../telegram_hermes.py#L199)

```python
def check_lockout(self, user_id: int) -> bool
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `user_id` | `int` |  |  |

**Returns:** `bool`

<a id="securesessionmanager-check_rate_limit"></a>

#### `SecureSessionManager.check_rate_limit`

`method` | [telegram_hermes.py:208](../../telegram_hermes.py#L208)

```python
def check_rate_limit(self, user_id: int) -> bool
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `user_id` | `int` |  |  |

**Returns:** `bool`

<a id="securesessionmanager-create_session"></a>

#### `SecureSessionManager.create_session`

`method` | [telegram_hermes.py:221](../../telegram_hermes.py#L221)

```python
def create_session(self, user_id: int, client_id: str | None = None)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `user_id` | `int` |  |  |
| `client_id` | `str \| None` | `None` |  |

<a id="securesessionmanager-validate_session"></a>

#### `SecureSessionManager.validate_session`

`method` | [telegram_hermes.py:229](../../telegram_hermes.py#L229)

```python
def validate_session(self, user_id: int) -> bool
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `user_id` | `int` |  |  |

**Returns:** `bool`

<a id="securesessionmanager-get_client_id"></a>

#### `SecureSessionManager.get_client_id`

`method` | [telegram_hermes.py:241](../../telegram_hermes.py#L241)

```python
def get_client_id(self, user_id: int) -> str | None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `user_id` | `int` |  |  |

**Returns:** `str | None`

<a id="securesessionmanager-set_client_id"></a>

#### `SecureSessionManager.set_client_id`

`method` | [telegram_hermes.py:245](../../telegram_hermes.py#L245)

```python
def set_client_id(self, user_id: int, client_id: str)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `user_id` | `int` |  |  |
| `client_id` | `str` |  |  |

---

## Functions

<a id="run_lazyown_command"></a>

### `run_lazyown_command`

`function` | [telegram_hermes.py:61](../../telegram_hermes.py#L61)

```python
def run_lazyown_command(command: str, timeout: int = 30) -> str
```

Execute one or more LazyOwn shell commands non-interactively via PTY.

Replicates the MCP server's _run_lazyown_command logic.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  |  |
| `timeout` | `int` | `30` |  |

**Returns:** `str`

*Called by:* [`cron_schedule_cmd`](#cron_schedule_cmd), [`delegate_task_cmd`](#delegate_task_cmd), [`execute_command`](#execute_command), [`run_agent`](#run_agent), [`sitrep`](#sitrep), [`status_cmd`](#status_cmd), [`stop_daemon_cmd`](#stop_daemon_cmd), [`text_command`](#text_command)

---

<a id="c2_request"></a>

### `c2_request`

`function` | [telegram_hermes.py:145](../../telegram_hermes.py#L145)

```python
def c2_request(path: str, method: str = 'GET', body: dict | None = None) -> dict
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str` |  |  |
| `method` | `str` | `'GET'` |  |
| `body` | `dict \| None` | `None` |  |

**Returns:** `dict`

*Called by:* [`c2_command`](#c2_command), [`handle_file_upload`](#handle_file_upload), [`list_clients`](#list_clients), [`text_command`](#text_command)

---

<a id="load_payload"></a>

### `load_payload`

`function` | [telegram_hermes.py:177](../../telegram_hermes.py#L177)

```python
def load_payload() -> dict
```

**Returns:** `dict`

*Called by:* [`config_cmd`](#config_cmd)

---

<a id="start"></a>

### `start`

`function` `async` | [telegram_hermes.py:255](../../telegram_hermes.py#L255)

```python
async def start(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

---

<a id="help_cmd"></a>

### `help_cmd`

`function` `async` | [telegram_hermes.py:278](../../telegram_hermes.py#L278)

```python
async def help_cmd(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

---

<a id="execute_command"></a>

### `execute_command`

`function` `async` | [telegram_hermes.py:306](../../telegram_hermes.py#L306)

```python
async def execute_command(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`strip_ansi`](core.parsers.py.md#strip_ansi), [`run_lazyown_command`](#run_lazyown_command)

---

<a id="sitrep"></a>

### `sitrep`

`function` `async` | [telegram_hermes.py:337](../../telegram_hermes.py#L337)

```python
async def sitrep(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`strip_ansi`](core.parsers.py.md#strip_ansi), [`run_lazyown_command`](#run_lazyown_command)

---

<a id="config_cmd"></a>

### `config_cmd`

`function` `async` | [telegram_hermes.py:373](../../telegram_hermes.py#L373)

```python
async def config_cmd(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`load_payload`](#load_payload)

---

<a id="add_cli"></a>

### `add_cli`

`function` `async` | [telegram_hermes.py:422](../../telegram_hermes.py#L422)

```python
async def add_cli(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

---

<a id="list_clients"></a>

### `list_clients`

`function` `async` | [telegram_hermes.py:437](../../telegram_hermes.py#L437)

```python
async def list_clients(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`c2_request`](#c2_request)

---

<a id="c2_command"></a>

### `c2_command`

`function` `async` | [telegram_hermes.py:464](../../telegram_hermes.py#L464)

```python
async def c2_command(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`c2_request`](#c2_request)

---

<a id="run_agent"></a>

### `run_agent`

`function` `async` | [telegram_hermes.py:504](../../telegram_hermes.py#L504)

```python
async def run_agent(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`strip_ansi`](core.parsers.py.md#strip_ansi), [`run_lazyown_command`](#run_lazyown_command)

---

<a id="delegate_task_cmd"></a>

### `delegate_task_cmd`

`function` `async` | [telegram_hermes.py:533](../../telegram_hermes.py#L533)

```python
async def delegate_task_cmd(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`strip_ansi`](core.parsers.py.md#strip_ansi), [`run_lazyown_command`](#run_lazyown_command)

---

<a id="cron_schedule_cmd"></a>

### `cron_schedule_cmd`

`function` `async` | [telegram_hermes.py:564](../../telegram_hermes.py#L564)

```python
async def cron_schedule_cmd(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`strip_ansi`](core.parsers.py.md#strip_ansi), [`run_lazyown_command`](#run_lazyown_command)

---

<a id="status_cmd"></a>

### `status_cmd`

`function` `async` | [telegram_hermes.py:597](../../telegram_hermes.py#L597)

```python
async def status_cmd(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`strip_ansi`](core.parsers.py.md#strip_ansi), [`run_lazyown_command`](#run_lazyown_command)

---

<a id="stop_daemon_cmd"></a>

### `stop_daemon_cmd`

`function` `async` | [telegram_hermes.py:630](../../telegram_hermes.py#L630)

```python
async def stop_daemon_cmd(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`strip_ansi`](core.parsers.py.md#strip_ansi), [`run_lazyown_command`](#run_lazyown_command)

---

<a id="download_file_cmd"></a>

### `download_file_cmd`

`function` `async` | [telegram_hermes.py:647](../../telegram_hermes.py#L647)

```python
async def download_file_cmd(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

---

<a id="handle_file_upload"></a>

### `handle_file_upload`

`function` `async` | [telegram_hermes.py:675](../../telegram_hermes.py#L675)

```python
async def handle_file_upload(update: Update, context: CallbackContext) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`c2_request`](#c2_request)

---

<a id="text_command"></a>

### `text_command`

`function` `async` | [telegram_hermes.py:712](../../telegram_hermes.py#L712)

```python
async def text_command(update: Update, context: CallbackContext) -> None
```

Handle any text message as a direct LazyOwn command.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `update` | `Update` |  |  |
| `context` | `CallbackContext` |  |  |

*Calls:* [`strip_ansi`](core.parsers.py.md#strip_ansi), [`c2_request`](#c2_request), [`run_lazyown_command`](#run_lazyown_command)

---

<a id="main"></a>

### `main`

`function` `async` | [telegram_hermes.py:772](../../telegram_hermes.py#L772)

```python
async def main() -> None
```

---

## Constants

<a id="lazyown_dir"></a>

### `LAZYOWN_DIR`

`constant` | [telegram_hermes.py:52](../../telegram_hermes.py#L52)

```python
LAZYOWN_DIR = Path(__file__).parent.resolve()
```

---

<a id="sessions_dir"></a>

### `SESSIONS_DIR`

`constant` | [telegram_hermes.py:53](../../telegram_hermes.py#L53)

```python
SESSIONS_DIR = LAZYOWN_DIR / 'sessions'
```

---

<a id="payload_file"></a>

### `PAYLOAD_FILE`

`constant` | [telegram_hermes.py:54](../../telegram_hermes.py#L54)

```python
PAYLOAD_FILE = LAZYOWN_DIR / 'payload.json'
```

---

<a id="session_timeout"></a>

### `SESSION_TIMEOUT`

`constant` | [telegram_hermes.py:805](../../telegram_hermes.py#L805)

```python
SESSION_TIMEOUT = 1800
```

---

<a id="max_failed_attempts"></a>

### `MAX_FAILED_ATTEMPTS`

`constant` | [telegram_hermes.py:806](../../telegram_hermes.py#L806)

```python
MAX_FAILED_ATTEMPTS = 3
```

---

<a id="rate_limit"></a>

### `RATE_LIMIT`

`constant` | [telegram_hermes.py:807](../../telegram_hermes.py#L807)

```python
RATE_LIMIT = 5
```

---
