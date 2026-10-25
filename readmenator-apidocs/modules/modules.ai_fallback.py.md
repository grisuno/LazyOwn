# `modules.ai_fallback`

> Source: [modules/ai_fallback.py:1](../../modules/ai_fallback.py#L1) | language `py` | coverage 66.7% | [API index](../index.md)

LazyOwn AI Fallback Chain ========================== Unified LLM caller with automatic fallback:

1. Groq (cloud, fast, requires api_key)
       ↓ on quota / rate-limit error
  2. Ollama (local, requires ollama running + a chat model)
       ↓ if Ollama unreachable or no suitable model
  3. Helpful error message with actionable steps

Used by recommender.py and timeline_narrator.py so fallback
logic lives in exactly one place.

Public API
----------
call(prompt, system, api_key, max_tokens, temperature) -> AIResult

AIResult fields:
  .text     str   — the response text (or error/help message)
  .backend  str   — "groq" | "ollama" | "error"
  .model    str   — model name used
  .error    str   — original error if fallback occurred (else "")

## Contents

- **Classes:** [`AIResult`](#airesult)
- **Functions:** [`call`](#call)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_ai_fallback_py__call(["call"])
    n_modules_ai_fallback_py__AIResult(["AIResult"])
    n_modules_ai_fallback_py__call --> n_modules_ai_fallback_py__AIResult
```

## Classes

<a id="airesult"></a>

### `AIResult`

`class` `dataclass` | [modules/ai_fallback.py:95](../../modules/ai_fallback.py#L95)

Decorators: `@dataclass`

```python
class AIResult
```

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`text`](#airesult-text) | `str` |  |  |
| [`backend`](#airesult-backend) | `str` |  |  |
| [`model`](#airesult-model) | `str` | `''` |  |
| [`error`](#airesult-error) | `str` | `''` |  |

---

## Functions

<a id="call"></a>

### `call`

`function` | [modules/ai_fallback.py:254](../../modules/ai_fallback.py#L254)

```python
def call(prompt: str, system: str = '', api_key: str = '', max_tokens: int = 1024, temperature: float = 0.3) -> AIResult
```

Call Groq → fallback to Ollama → fallback to TopoSwarm local brain → error.

Returns an AIResult with .text, .backend, .model, .error.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `prompt` | `str` |  |  |
| `system` | `str` | `''` |  |
| `api_key` | `str` | `''` |  |
| `max_tokens` | `int` | `1024` |  |
| `temperature` | `float` | `0.3` |  |

**Returns:** `AIResult`

*Calls:* [`AIResult`](#airesult)

---
