# `skills.lazyown_daemon`

> Source: [skills/lazyown_daemon.py:1](../../skills/lazyown_daemon.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

LazyOwn Unified Daemon ====================== Replaces three separate background processes with a single asyncio daemon:

Role 1 — File Watcher     (was: sessions_watcher.py)
    Watches sessions/ for new/modified files:
    - scan_*.nmap     → generate plan.txt via Ollama, inject PLAN_READY objective
    - scan_*.nmap.xml → ingest into FactStore, update soul.md OS hint
    - sessions/<ip>/<port>/<tool>/*.txt → ingest into FactStore, update soul.md creds
    - sessions/plan.txt → emit PLAN_UPDATED event

  Role 2 — Event Engine Poll (was: heartbeat.py + event_engine CSV tail)
    Every N seconds: tail LazyOwn_session_report.csv for new rows →
    run rule matching → emit matched events to events.jsonl

  Role 3 — Heartbeat        (was: heartbeat.py)
    Every 30 seconds: emit a HEARTBEAT event so the MCP can verify the daemon
    is alive; update sessions/daemon_status.json with uptime and stats.

Communication:
  All roles share a single asyncio.Queue for internal events.
  External consumers (MCP) read sessions/events.jsonl as before — no interface change.

Management:
  python3 skills/lazyown_daemon.py start    # fork and detach
  python3 skills/lazyown_daemon.py stop     # kill via PID file
  python3 skills/lazyown_daemon.py status   # print status from daemon_status.json
  python3 skills/lazyown_daemon.py run      # run in foreground (for debugging)

PID file: sessions/daemon.pid
Status file: sessions/daemon_status.json

## Contents

- **Functions:** [`file_watcher_loop`](#file_watcher_loop), [`file_event_consumer`](#file_event_consumer), [`event_engine_loop`](#event_engine_loop), [`heartbeat_loop`](#heartbeat_loop), [`toposwarm_keepalive_loop`](#toposwarm_keepalive_loop), [`cmd_run`](#cmd_run), [`cmd_start`](#cmd_start), [`cmd_stop`](#cmd_stop), [`cmd_status`](#cmd_status)
- **Constants:** [`BASE_DIR`](#base_dir), [`SESSIONS_DIR`](#sessions_dir), [`SKILLS_DIR`](#skills_dir), [`MODULES_DIR`](#modules_dir), [`PID_FILE`](#pid_file), [`STATUS_FILE`](#status_file), [`ENGINE_INTERVAL_S`](#engine_interval_s), [`WATCHER_POLL_S`](#watcher_poll_s), [`HEARTBEAT_INTERVAL_S`](#heartbeat_interval_s), [`STATE_EVERY_N`](#state_every_n), [`NARRATE_EVERY_N`](#narrate_every_n)

## Functions

<a id="file_watcher_loop"></a>

### `file_watcher_loop`

`function` `async` | [skills/lazyown_daemon.py:150](../../skills/lazyown_daemon.py#L150)

```python
async def file_watcher_loop(queue: asyncio.Queue) -> None
```

Watch sessions/ for new/modified files and dispatch handlers.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `queue` | `asyncio.Queue` |  |  |

---

<a id="file_event_consumer"></a>

### `file_event_consumer`

`function` `async` | [skills/lazyown_daemon.py:223](../../skills/lazyown_daemon.py#L223)

```python
async def file_event_consumer(queue: asyncio.Queue) -> None
```

Consume FILE events from the queue and call _dispatch in executor.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `queue` | `asyncio.Queue` |  |  |

---

<a id="event_engine_loop"></a>

### `event_engine_loop`

`function` `async` | [skills/lazyown_daemon.py:240](../../skills/lazyown_daemon.py#L240)

```python
async def event_engine_loop() -> None
```

Tail CSV, match rules, emit events — every ENGINE_INTERVAL_S seconds.

---

<a id="heartbeat_loop"></a>

### `heartbeat_loop`

`function` `async` | [skills/lazyown_daemon.py:280](../../skills/lazyown_daemon.py#L280)

```python
async def heartbeat_loop() -> None
```

Emit HEARTBEAT event and write daemon_status.json every 30 seconds.

---

<a id="toposwarm_keepalive_loop"></a>

### `toposwarm_keepalive_loop`

`function` `async` | [skills/lazyown_daemon.py:332](../../skills/lazyown_daemon.py#L332)

```python
async def toposwarm_keepalive_loop() -> None
```

Keeps the TopoSwarm MCP server alive as a subprocess.

Starts toposwarm_lazyown_orchestrator.py --mcp in stdio mode so LazyOwn
can use it as a local brain without cloud APIs.  If it crashes, restarts
after 10 s with exponential backoff up to 120 s.

---

<a id="cmd_run"></a>

### `cmd_run`

`function` | [skills/lazyown_daemon.py:453](../../skills/lazyown_daemon.py#L453)

```python
def cmd_run() -> None
```

Run in foreground.

---

<a id="cmd_start"></a>

### `cmd_start`

`function` | [skills/lazyown_daemon.py:462](../../skills/lazyown_daemon.py#L462)

```python
def cmd_start() -> None
```

Fork, detach, and run in background.

---

<a id="cmd_stop"></a>

### `cmd_stop`

`function` | [skills/lazyown_daemon.py:495](../../skills/lazyown_daemon.py#L495)

```python
def cmd_stop() -> None
```

Send SIGTERM to the running daemon.

---

<a id="cmd_status"></a>

### `cmd_status`

`function` | [skills/lazyown_daemon.py:513](../../skills/lazyown_daemon.py#L513)

```python
def cmd_status() -> None
```

Print status from daemon_status.json.

---

## Constants

<a id="base_dir"></a>

### `BASE_DIR`

`constant` | [skills/lazyown_daemon.py:50](../../skills/lazyown_daemon.py#L50)

```python
BASE_DIR = Path(__file__).parent.parent
```

---

<a id="sessions_dir"></a>

### `SESSIONS_DIR`

`constant` | [skills/lazyown_daemon.py:51](../../skills/lazyown_daemon.py#L51)

```python
SESSIONS_DIR = BASE_DIR / 'sessions'
```

---

<a id="skills_dir"></a>

### `SKILLS_DIR`

`constant` | [skills/lazyown_daemon.py:52](../../skills/lazyown_daemon.py#L52)

```python
SKILLS_DIR = Path(__file__).parent
```

---

<a id="modules_dir"></a>

### `MODULES_DIR`

`constant` | [skills/lazyown_daemon.py:53](../../skills/lazyown_daemon.py#L53)

```python
MODULES_DIR = BASE_DIR / 'modules'
```

---

<a id="pid_file"></a>

### `PID_FILE`

`constant` | [skills/lazyown_daemon.py:55](../../skills/lazyown_daemon.py#L55)

```python
PID_FILE = SESSIONS_DIR / 'daemon.pid'
```

---

<a id="status_file"></a>

### `STATUS_FILE`

`constant` | [skills/lazyown_daemon.py:56](../../skills/lazyown_daemon.py#L56)

```python
STATUS_FILE = SESSIONS_DIR / 'daemon_status.json'
```

---

<a id="engine_interval_s"></a>

### `ENGINE_INTERVAL_S`

`constant` | [skills/lazyown_daemon.py:132](../../skills/lazyown_daemon.py#L132)

```python
ENGINE_INTERVAL_S = float(os.environ.get('DAEMON_ENGINE_INTERVAL', '5'))
```

---

<a id="watcher_poll_s"></a>

### `WATCHER_POLL_S`

`constant` | [skills/lazyown_daemon.py:133](../../skills/lazyown_daemon.py#L133)

```python
WATCHER_POLL_S = float(os.environ.get('DAEMON_WATCHER_POLL', '3'))
```

---

<a id="heartbeat_interval_s"></a>

### `HEARTBEAT_INTERVAL_S`

`constant` | [skills/lazyown_daemon.py:134](../../skills/lazyown_daemon.py#L134)

```python
HEARTBEAT_INTERVAL_S = float(os.environ.get('DAEMON_HEARTBEAT_INTERVAL', '30'))
```

---

<a id="state_every_n"></a>

### `STATE_EVERY_N`

`constant` | [skills/lazyown_daemon.py:135](../../skills/lazyown_daemon.py#L135)

```python
STATE_EVERY_N = int(os.environ.get('DAEMON_STATE_EVERY', '3'))
```

---

<a id="narrate_every_n"></a>

### `NARRATE_EVERY_N`

`constant` | [skills/lazyown_daemon.py:136](../../skills/lazyown_daemon.py#L136)

```python
NARRATE_EVERY_N = int(os.environ.get('DAEMON_NARRATE_EVERY', '12'))
```

---
