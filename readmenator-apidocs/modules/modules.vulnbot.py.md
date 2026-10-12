# `modules.vulnbot`

> Source: [modules/vulnbot.py:1](../../modules/vulnbot.py#L1) | language `py` | coverage 8.3% | [API index](../index.md)

vulnbot.py

## Contents

- **Classes:** [`VulnBotCLI`](#vulnbotcli)
- **Constants:** [`BANNER`](#banner)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_vulnbot_py__VulnBotCLI_get_relevant_knowledge(["VulnBotCLI.get_relevant_knowledge"])
    n_modules_vulnbot_py__VulnBotCLI_load_knowledge_base(["VulnBotCLI.load_knowledge_base"])
    n_modules_vulnbot_py__VulnBotCLI_process_with_context(["VulnBotCLI.process_with_context"])
    n_modules_vulnbot_py__VulnBotCLI_create_complex_prompt(["VulnBotCLI.create_complex_prompt"])
    n_modules_vulnbot_py__VulnBotCLI_read_file_content(["VulnBotCLI.read_file_content"])
    n_modules_vulnbot_py__VulnBotCLI_stream_response(["VulnBotCLI.stream_response"])
    n_modules_vulnbot_py__VulnBotCLI_add_to_knowledge_base(["VulnBotCLI.add_to_knowledge_base"])
    n_modules_vulnbot_py__VulnBotCLI_save_knowledge_base(["VulnBotCLI.save_knowledge_base"])
    n_modules_vulnbot_py__VulnBotCLI___init__(["VulnBotCLI.__init__"])
    n_modules_logging_config_py__configure["logging_config.configure"]
    n_modules_ai_model_py__AIModel_generate["ai_model.AIModel.generate"]
    n_modules_vulnbot_py__VulnBotCLI_get_relevant_knowledge --> n_modules_vulnbot_py__VulnBotCLI_load_knowledge_base
    n_modules_vulnbot_py__VulnBotCLI_process_with_context --> n_modules_vulnbot_py__VulnBotCLI_create_complex_prompt
    n_modules_vulnbot_py__VulnBotCLI_process_with_context --> n_modules_vulnbot_py__VulnBotCLI_get_relevant_knowledge
    n_modules_vulnbot_py__VulnBotCLI_process_with_context --> n_modules_vulnbot_py__VulnBotCLI_read_file_content
    n_modules_vulnbot_py__VulnBotCLI_process_with_context --> n_modules_vulnbot_py__VulnBotCLI_stream_response
    n_modules_vulnbot_py__VulnBotCLI_add_to_knowledge_base --> n_modules_vulnbot_py__VulnBotCLI_load_knowledge_base
    n_modules_vulnbot_py__VulnBotCLI_add_to_knowledge_base --> n_modules_vulnbot_py__VulnBotCLI_save_knowledge_base
    n_modules_vulnbot_py__VulnBotCLI___init__ -.-> n_modules_logging_config_py__configure
    n_modules_vulnbot_py__VulnBotCLI_stream_response -.-> n_modules_ai_model_py__AIModel_generate
```

## Classes

<a id="vulnbotcli"></a>

### `VulnBotCLI`

`class` | [modules/vulnbot.py:29](../../modules/vulnbot.py#L29)

```python
class VulnBotCLI
```

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#vulnbotcli-__init__) | constructor |  |
| [`load_knowledge_base`](#vulnbotcli-load_knowledge_base) | method |  |
| [`save_knowledge_base`](#vulnbotcli-save_knowledge_base) | method |  |
| [`get_relevant_knowledge`](#vulnbotcli-get_relevant_knowledge) | method |  |
| [`create_complex_prompt`](#vulnbotcli-create_complex_prompt) | method |  |
| [`read_file_content`](#vulnbotcli-read_file_content) | method |  |
| [`load_event_config`](#vulnbotcli-load_event_config) | method |  |
| [`process_with_context`](#vulnbotcli-process_with_context) | method |  |
| [`stream_response`](#vulnbotcli-stream_response) | method |  |
| [`add_to_knowledge_base`](#vulnbotcli-add_to_knowledge_base) | method |  |

<a id="vulnbotcli-__init__"></a>

#### `VulnBotCLI.__init__`

`constructor` | [modules/vulnbot.py:30](../../modules/vulnbot.py#L30)

```python
def __init__(self, provider: str = 'groq', mode: str = 'console', debug: bool = False, script_path: str = 'lazyown.py')
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `provider` | `str` | `'groq'` |  |
| `mode` | `str` | `'console'` |  |
| `debug` | `bool` | `False` |  |
| `script_path` | `str` | `'lazyown.py'` |  |

*Calls:* [`configure`](modules.logging_config.py.md#configure)

*Called by:* [`main`](modules.vuln_bot_cli.py.md#main)

<a id="vulnbotcli-load_knowledge_base"></a>

#### `VulnBotCLI.load_knowledge_base`

`method` | [modules/vulnbot.py:145](../../modules/vulnbot.py#L145)

```python
def load_knowledge_base(self) -> dict
```

**Returns:** `dict`

*Called by:* [`VulnBotCLI.add_to_knowledge_base`](#vulnbotcli-add_to_knowledge_base), [`VulnBotCLI.get_relevant_knowledge`](#vulnbotcli-get_relevant_knowledge)

<a id="vulnbotcli-save_knowledge_base"></a>

#### `VulnBotCLI.save_knowledge_base`

`method` | [modules/vulnbot.py:151](../../modules/vulnbot.py#L151)

```python
def save_knowledge_base(self, kb: dict) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `kb` | `dict` |  |  |

*Called by:* [`VulnBotCLI.add_to_knowledge_base`](#vulnbotcli-add_to_knowledge_base)

<a id="vulnbotcli-get_relevant_knowledge"></a>

#### `VulnBotCLI.get_relevant_knowledge`

`method` | [modules/vulnbot.py:155](../../modules/vulnbot.py#L155)

```python
def get_relevant_knowledge(self, prompt: str) -> str
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `prompt` | `str` |  |  |

**Returns:** `str`

*Calls:* [`VulnBotCLI.load_knowledge_base`](#vulnbotcli-load_knowledge_base)

*Called by:* [`VulnBotCLI.process_with_context`](#vulnbotcli-process_with_context)

<a id="vulnbotcli-create_complex_prompt"></a>

#### `VulnBotCLI.create_complex_prompt`

`method` | [modules/vulnbot.py:160](../../modules/vulnbot.py#L160)

```python
def create_complex_prompt(self, base_prompt: str, history: str = '', knowledge: str = '') -> str
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_prompt` | `str` |  |  |
| `history` | `str` | `''` |  |
| `knowledge` | `str` | `''` |  |

**Returns:** `str`

*Called by:* [`VulnBotCLI.process_with_context`](#vulnbotcli-process_with_context)

<a id="vulnbotcli-read_file_content"></a>

#### `VulnBotCLI.read_file_content`

`method` | [modules/vulnbot.py:176](../../modules/vulnbot.py#L176)

```python
def read_file_content(self, file_path: str) -> str
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `file_path` | `str` |  |  |

**Returns:** `str`

**Raises**

- `FileNotFoundError`: (raised in the body, not documented)

*Called by:* [`VulnBotCLI.process_with_context`](#vulnbotcli-process_with_context)

<a id="vulnbotcli-load_event_config"></a>

#### `VulnBotCLI.load_event_config`

`method` | [modules/vulnbot.py:182](../../modules/vulnbot.py#L182)

```python
def load_event_config(self) -> dict
```

**Returns:** `dict`

<a id="vulnbotcli-process_with_context"></a>

#### `VulnBotCLI.process_with_context`

`method` | [modules/vulnbot.py:190](../../modules/vulnbot.py#L190)

```python
def process_with_context(self, file_path: str, event: str = None) -> str
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `file_path` | `str` |  |  |
| `event` | `str` | `None` |  |

**Returns:** `str`

*Calls:* [`VulnBotCLI.create_complex_prompt`](#vulnbotcli-create_complex_prompt), [`VulnBotCLI.get_relevant_knowledge`](#vulnbotcli-get_relevant_knowledge), [`VulnBotCLI.read_file_content`](#vulnbotcli-read_file_content), [`VulnBotCLI.stream_response`](#vulnbotcli-stream_response)

*Called by:* [`main`](modules.vuln_bot_cli.py.md#main)

<a id="vulnbotcli-stream_response"></a>

#### `VulnBotCLI.stream_response`

`method` | [modules/vulnbot.py:206](../../modules/vulnbot.py#L206)

```python
def stream_response(self, prompt: str) -> Response
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `prompt` | `str` |  |  |

**Returns:** `Response`

*Calls:* [`AIModel.generate`](modules.ai_model.py.md#aimodel-generate)

*Called by:* [`VulnBotCLI.process_with_context`](#vulnbotcli-process_with_context)

<a id="vulnbotcli-add_to_knowledge_base"></a>

#### `VulnBotCLI.add_to_knowledge_base`

`method` | [modules/vulnbot.py:212](../../modules/vulnbot.py#L212)

```python
def add_to_knowledge_base(self, prompt: str, response: str)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `prompt` | `str` |  |  |
| `response` | `str` |  |  |

*Calls:* [`VulnBotCLI.load_knowledge_base`](#vulnbotcli-load_knowledge_base), [`VulnBotCLI.save_knowledge_base`](#vulnbotcli-save_knowledge_base)

*Called by:* [`main`](modules.vuln_bot_cli.py.md#main)

---

## Constants

<a id="banner"></a>

### `BANNER`

`constant` | [modules/vulnbot.py:24](../../modules/vulnbot.py#L24)

```python
BANNER = '\n[*] Starting: LazyOwn GPT One Liner CLI Assistant [;,;]\n'
```

---
