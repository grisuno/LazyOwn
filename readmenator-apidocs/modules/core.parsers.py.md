# `core.parsers`

> Source: [core/parsers.py:1](../../core/parsers.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Shared text kernel for the LazyOwn framework.

Single-implementation rule: the live helpers live in `[`utils`](utils.py.md)` (used
by the CLI and C2). This module keeps only `[`strip_ansi`](#strip_ansi)`, the one
extraction the framework actually imports. The rest of the historic
``utils.py`` fork was removed because every copy had diverged and
zero callers (see ``tests/test_single_implementation.py``).

## Contents

- **Functions:** [`strip_ansi`](#strip_ansi)

## Functions

<a id="strip_ansi"></a>

### `strip_ansi`

`function` | [core/parsers.py:15](../../core/parsers.py#L15)

```python
def strip_ansi(text: str) -> str
```

Remove ANSI escape sequences and readline markers from a string.

Handles standard escape codes (``[...m``), extended unicode
escape initiators (````, ````), CSI sequences, and the
````/```` (SOH/STX) delimiters that ``render_prompt`` emits
so readline can measure prompt width.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `text` | `str` |  | Raw terminal output. |

**Returns:** `str` - Clean text without ANSI codes or readline control markers.

*Called by:* [`exce_cmd`](discord_c2.py.md#exce_cmd), [`aicmd_deepseek`](lazyc2.py.md#aicmd_deepseek), [`cmd_download`](slack_c2_bot.py.md#cmd_download), [`handle_message`](slack_c2_bot.py.md#handle_message), [`exce_cmd`](telegram_c2.py.md#exce_cmd), [`cron_schedule_cmd`](telegram_hermes.py.md#cron_schedule_cmd), [`delegate_task_cmd`](telegram_hermes.py.md#delegate_task_cmd), [`execute_command`](telegram_hermes.py.md#execute_command), [`run_agent`](telegram_hermes.py.md#run_agent), [`sitrep`](telegram_hermes.py.md#sitrep), [`status_cmd`](telegram_hermes.py.md#status_cmd), [`stop_daemon_cmd`](telegram_hermes.py.md#stop_daemon_cmd) and 1 more

---
