# `skills.sessions_watcher`

> Source: [skills/sessions_watcher.py:1](../../skills/sessions_watcher.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

LazyOwn Sessions Watcher ======================== Watchdog daemon over sessions/.

When new or modified files appear, it:

  scan_*.nmap (nmap text output)
    → calls VulnBot (or local Ollama fallback) to generate sessions/plan.txt
    → injects a PLAN_READY objective into objectives.jsonl
    → emits PLAN_READY event to events.jsonl

  scan_*.nmap.xml (nmap XML)
    → calls FactStore.ingest_xml()
    → emits SCAN_XML_READY event

  sessions/<ip>/<port>/<tool>/*.txt  (pwntomate tool output)
    → calls FactStore.ingest_text()
    → emits TOOL_OUTPUT_READY event
    → injects a factual objective: "Review <tool> output for <ip>:<port>"

  sessions/plan.txt  (VulnBot or manual plan)
    → emits PLAN_UPDATED event with first 500 chars as preview

This closes the OpenClaw-style loop:
  lazynmap → watcher → plan.txt → objective injected →
  Claude Code polls → reasons → acts → new output → watcher fires again

Usage (background daemon):
    python3 skills/sessions_watcher.py &

    or via MCP:  lazyown_run_command("python3 skills/sessions_watcher.py &")

Stop:  kill $(pgrep -f sessions_watcher.py)

## Contents

- **Functions:** [`main`](#main)
- **Constants:** [`BASE_DIR`](#base_dir), [`SESSIONS_DIR`](#sessions_dir), [`SKILLS_DIR`](#skills_dir), [`OLLAMA_HOST`](#ollama_host), [`OLLAMA_PORT`](#ollama_port), [`OLLAMA_MODEL`](#ollama_model), [`POLL_INTERVAL_S`](#poll_interval_s), [`MAX_PLAN_CHARS`](#max_plan_chars)

## Functions

<a id="main"></a>

### `main`

`function` | [skills/sessions_watcher.py:430](../../skills/sessions_watcher.py#L430)

```python
def main() -> None
```

---

## Constants

<a id="base_dir"></a>

### `BASE_DIR`

`constant` | [skills/sessions_watcher.py:58](../../skills/sessions_watcher.py#L58)

```python
BASE_DIR = Path(__file__).parent.parent
```

---

<a id="sessions_dir"></a>

### `SESSIONS_DIR`

`constant` | [skills/sessions_watcher.py:59](../../skills/sessions_watcher.py#L59)

```python
SESSIONS_DIR = BASE_DIR / 'sessions'
```

---

<a id="skills_dir"></a>

### `SKILLS_DIR`

`constant` | [skills/sessions_watcher.py:60](../../skills/sessions_watcher.py#L60)

```python
SKILLS_DIR = Path(__file__).parent
```

---

<a id="ollama_host"></a>

### `OLLAMA_HOST`

`constant` | [skills/sessions_watcher.py:101](../../skills/sessions_watcher.py#L101)

```python
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', '127.0.0.1')
```

---

<a id="ollama_port"></a>

### `OLLAMA_PORT`

`constant` | [skills/sessions_watcher.py:102](../../skills/sessions_watcher.py#L102)

```python
OLLAMA_PORT = int(os.environ.get('OLLAMA_PORT', '11434'))
```

---

<a id="ollama_model"></a>

### `OLLAMA_MODEL`

`constant` | [skills/sessions_watcher.py:103](../../skills/sessions_watcher.py#L103)

```python
OLLAMA_MODEL = os.environ.get('OLLAMA_SMALL_MODEL', 'qwen3.5:0.8b')
```

---

<a id="poll_interval_s"></a>

### `POLL_INTERVAL_S`

`constant` | [skills/sessions_watcher.py:105](../../skills/sessions_watcher.py#L105)

```python
POLL_INTERVAL_S = float(os.environ.get('WATCHER_POLL_INTERVAL', '3'))
```

---

<a id="max_plan_chars"></a>

### `MAX_PLAN_CHARS`

`constant` | [skills/sessions_watcher.py:106](../../skills/sessions_watcher.py#L106)

```python
MAX_PLAN_CHARS = int(os.environ.get('WATCHER_MAX_PLAN_CHARS', '6000'))
```

---
