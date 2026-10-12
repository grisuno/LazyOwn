# `modules.recommender`

> Source: [modules/recommender.py:1](../../modules/recommender.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

LazyOwn Smart Command Recommender =================================== Reads the current session state and asks Groq to rank the best 3-5 next LazyOwn commands, with confidence scores and reasoning.

Output written to: sessions/recommendations/next_actions.json

Public API:
  recommend(state: dict | None, api_key: str) -> list[dict]
      Returns ranked recommendations:
      [{"command": "smbmap", "confidence": 0.95, "reason": "...", "args": "-H {rhost}"}]

  recommend_and_save(api_key: str) -> list[dict]
      Builds state, calls Groq, writes JSON, returns list.

## Contents

- **Functions:** [`recommend`](#recommend), [`recommend_and_save`](#recommend_and_save)
- **Constants:** [`BASE_DIR`](#base_dir), [`SESSIONS`](#sessions), [`RECO_DIR`](#reco_dir), [`NEXT_ACTIONS_FILE`](#next_actions_file), [`PAYLOAD_FILE`](#payload_file)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_recommender_py__recommend_and_save(["recommend_and_save"])
    n_modules_recommender_py__recommend(["recommend"])
    n_modules_recommender_py__recommend_and_save --> n_modules_recommender_py__recommend
```

## Functions

<a id="recommend"></a>

### `recommend`

`function` | [modules/recommender.py:143](../../modules/recommender.py#L143)

```python
def recommend(state: dict, api_key: str) -> list[dict]
```

Return ranked recommendations without writing to disk.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `state` | `dict` |  |  |
| `api_key` | `str` |  |  |

**Returns:** `list[dict]`

*Called by:* [`recommend_and_save`](#recommend_and_save)

---

<a id="recommend_and_save"></a>

### `recommend_and_save`

`function` | [modules/recommender.py:163](../../modules/recommender.py#L163)

```python
def recommend_and_save(api_key: str | None = None) -> list[dict]
```

Build state → call Groq → write JSON → return recommendations.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str \| None` | `None` |  |

**Returns:** `list[dict]`

*Calls:* [`recommend`](#recommend)

---

## Constants

<a id="base_dir"></a>

### `BASE_DIR`

`constant` | [modules/recommender.py:23](../../modules/recommender.py#L23)

```python
BASE_DIR = Path(__file__).parent.parent
```

---

<a id="sessions"></a>

### `SESSIONS`

`constant` | [modules/recommender.py:24](../../modules/recommender.py#L24)

```python
SESSIONS = BASE_DIR / 'sessions'
```

---

<a id="reco_dir"></a>

### `RECO_DIR`

`constant` | [modules/recommender.py:25](../../modules/recommender.py#L25)

```python
RECO_DIR = SESSIONS / 'recommendations'
```

---

<a id="next_actions_file"></a>

### `NEXT_ACTIONS_FILE`

`constant` | [modules/recommender.py:26](../../modules/recommender.py#L26)

```python
NEXT_ACTIONS_FILE = RECO_DIR / 'next_actions.json'
```

---

<a id="payload_file"></a>

### `PAYLOAD_FILE`

`constant` | [modules/recommender.py:27](../../modules/recommender.py#L27)

```python
PAYLOAD_FILE = BASE_DIR / 'payload.json'
```

---
