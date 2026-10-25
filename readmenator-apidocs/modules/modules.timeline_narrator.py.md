# `modules.timeline_narrator`

> Source: [modules/timeline_narrator.py:1](../../modules/timeline_narrator.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

LazyOwn Timeline Narrator ========================== Reads events.jsonl, groups them into time windows, and asks Groq to generate a concise red-team prose narrative.

Writes sessions/timeline.md.

The narrative reads like a penetration test report timeline:
  "10:32 — Initial reconnaissance revealed an open HTTP port on 10.10.11.78.
   10:35 — SMB enumeration was initiated after detecting port 445 ..."

Public API:
  narrate(api_key: str | None, force: bool) -> str
      Builds and returns the narrative text, writes timeline.md.
      Set force=True to regenerate even if file is fresh (< 5 min old).

  load_timeline() -> str
      Return the last written timeline.md, or empty string.

## Contents

- **Functions:** [`narrate`](#narrate), [`load_timeline`](#load_timeline)
- **Constants:** [`BASE_DIR`](#base_dir), [`SESSIONS`](#sessions), [`EVENTS_FILE`](#events_file), [`TIMELINE_FILE`](#timeline_file), [`PAYLOAD_FILE`](#payload_file)

## Functions

<a id="narrate"></a>

### `narrate`

`function` | [modules/timeline_narrator.py:130](../../modules/timeline_narrator.py#L130)

```python
def narrate(api_key: str | None = None, force: bool = False) -> str
```

Generate and return the timeline narrative.

Writes timeline.md.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str \| None` | `None` |  |
| `force` | `bool` | `False` |  |

**Returns:** `str`

---

<a id="load_timeline"></a>

### `load_timeline`

`function` | [modules/timeline_narrator.py:165](../../modules/timeline_narrator.py#L165)

```python
def load_timeline() -> str
```

Return the last written timeline.md or empty string.

**Returns:** `str`

---

## Constants

<a id="base_dir"></a>

### `BASE_DIR`

`constant` | [modules/timeline_narrator.py:25](../../modules/timeline_narrator.py#L25)

```python
BASE_DIR = Path(__file__).parent.parent
```

---

<a id="sessions"></a>

### `SESSIONS`

`constant` | [modules/timeline_narrator.py:26](../../modules/timeline_narrator.py#L26)

```python
SESSIONS = BASE_DIR / 'sessions'
```

---

<a id="events_file"></a>

### `EVENTS_FILE`

`constant` | [modules/timeline_narrator.py:27](../../modules/timeline_narrator.py#L27)

```python
EVENTS_FILE = SESSIONS / 'events.jsonl'
```

---

<a id="timeline_file"></a>

### `TIMELINE_FILE`

`constant` | [modules/timeline_narrator.py:28](../../modules/timeline_narrator.py#L28)

```python
TIMELINE_FILE = SESSIONS / 'timeline.md'
```

---

<a id="payload_file"></a>

### `PAYLOAD_FILE`

`constant` | [modules/timeline_narrator.py:29](../../modules/timeline_narrator.py#L29)

```python
PAYLOAD_FILE = BASE_DIR / 'payload.json'
```

---
