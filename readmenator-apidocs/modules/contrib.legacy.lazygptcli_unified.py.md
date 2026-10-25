# `contrib.legacy.lazygptcli_unified`

> Source: [contrib/legacy/lazygptcli_unified.py:1](../../contrib/legacy/lazygptcli_unified.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Unified Groq LLM client for LazyOwn — merges lazygptcli2/3/4/5 + lazyagentAi + lazygpttask + lazygptvulns + lazyredopgpt.

All original ``process_prompt_*`` function signatures are preserved for
backward compatibility (used by ``llm_adapter.py`` and the C2 dashboard).

Shared utility functions (knowledge-base CRUD, truncation, logging)
are defined once and reused across all task variants.

Usage::

    from modules.legacy.lazygptcli import (
        Groq, process_prompt, process_prompt_script, process_prompt_adversary,
        process_prompt_general, process_prompt_search, process_prompt_task,
        process_prompt_vuln, process_prompt_redop,
    )

## Contents

- **Functions:** [`process_prompt`](#process_prompt), [`process_prompt_script`](#process_prompt_script), [`process_prompt_adversary`](#process_prompt_adversary), [`process_prompt_general`](#process_prompt_general), [`process_prompt_search`](#process_prompt_search), [`process_prompt_task`](#process_prompt_task), [`process_prompt_vuln`](#process_prompt_vuln), [`process_prompt_redop`](#process_prompt_redop)

## Functions

<a id="process_prompt"></a>

### `process_prompt`

`function` | [contrib/legacy/lazygptcli_unified.py:318](../../contrib/legacy/lazygptcli_unified.py#L318)

```python
def process_prompt(client, prompt: str, debug: bool = False) -> str
```

Generate a single-line shell command from a user prompt.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` |  |  |  |
| `prompt` | `str` |  |  |
| `debug` | `bool` | `False` |  |

**Returns:** `str`

---

<a id="process_prompt_script"></a>

### `process_prompt_script`

`function` | [contrib/legacy/lazygptcli_unified.py:323](../../contrib/legacy/lazygptcli_unified.py#L323)

```python
def process_prompt_script(client, prompt: str, debug: bool = False) -> str
```

Generate a full script from a user prompt.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` |  |  |  |
| `prompt` | `str` |  |  |
| `debug` | `bool` | `False` |  |

**Returns:** `str`

---

<a id="process_prompt_adversary"></a>

### `process_prompt_adversary`

`function` | [contrib/legacy/lazygptcli_unified.py:328](../../contrib/legacy/lazygptcli_unified.py#L328)

```python
def process_prompt_adversary(client, prompt: str, debug: bool = False) -> str
```

Answer questions about MITRE ATT&CK techniques and Atomic Red Team.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` |  |  |  |
| `prompt` | `str` |  |  |
| `debug` | `bool` | `False` |  |

**Returns:** `str`

---

<a id="process_prompt_general"></a>

### `process_prompt_general`

`function` | [contrib/legacy/lazygptcli_unified.py:333](../../contrib/legacy/lazygptcli_unified.py#L333)

```python
def process_prompt_general(client, prompt: str, debug: bool = False) -> str
```

General red team assistant with payload.json context and DeepSeek fallback.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` |  |  |  |
| `prompt` | `str` |  |  |
| `debug` | `bool` | `False` |  |

**Returns:** `str`

---

<a id="process_prompt_search"></a>

### `process_prompt_search`

`function` | [contrib/legacy/lazygptcli_unified.py:341](../../contrib/legacy/lazygptcli_unified.py#L341)

```python
def process_prompt_search(client, prompt: str, debug: bool = False) -> str
```

Research and threat intelligence analysis.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` |  |  |  |
| `prompt` | `str` |  |  |
| `debug` | `bool` | `False` |  |

**Returns:** `str`

---

<a id="process_prompt_task"></a>

### `process_prompt_task`

`function` | [contrib/legacy/lazygptcli_unified.py:346](../../contrib/legacy/lazygptcli_unified.py#L346)

```python
def process_prompt_task(client, prompt: str, debug: bool = False) -> str
```

Analyze task assessment JSON for completion status and next commands.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` |  |  |  |
| `prompt` | `str` |  |  |
| `debug` | `bool` | `False` |  |

**Returns:** `str`

---

<a id="process_prompt_vuln"></a>

### `process_prompt_vuln`

`function` | [contrib/legacy/lazygptcli_unified.py:356](../../contrib/legacy/lazygptcli_unified.py#L356)

```python
def process_prompt_vuln(client, prompt: str, debug: bool = False, event: str = '') -> str
```

Analyze Nmap output for vulnerabilities and generate penetration test action plan.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` |  |  |  |
| `prompt` | `str` |  |  |
| `debug` | `bool` | `False` |  |
| `event` | `str` | `''` |  |

**Returns:** `str`

---

<a id="process_prompt_redop"></a>

### `process_prompt_redop`

`function` | [contrib/legacy/lazygptcli_unified.py:382](../../contrib/legacy/lazygptcli_unified.py#L382)

```python
def process_prompt_redop(client, prompt: str, debug: bool = False) -> str
```

Evaluate Red Team operation status from JSON database params.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client` |  |  |  |
| `prompt` | `str` |  |  |
| `debug` | `bool` | `False` |  |

**Returns:** `str`

---
