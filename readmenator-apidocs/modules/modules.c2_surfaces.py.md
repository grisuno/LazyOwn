# `modules.c2_surfaces`

> Source: [modules/c2_surfaces.py:1](../../modules/c2_surfaces.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

C2 dashboard surfaces fed by the autonomous loop and APT chains.

Single chokepoint (same philosophy as ``chain_registry`` and the
exploit catalogue): every automated write to operator-visible C2
state — banners, CVEs, notes, event rules, session reports — goes
through here. Reads mirror lazyc2's own formats exactly
(``sessions/banners.json``, ``sessions/cves.json``,
``sessions/notes.txt``, ``event_config.json``) so the dashboard needs
zero changes.

Security invariants:
    1. Appends and dedupes only; never deletes operator content.
    2. Every write is atomic (tmp + replace) and capped in size.
    3. Every public function is best-effort and never raises — a full
       disk or a corrupt JSON must not break an engagement loop.
    4. No network, no shell, no credentials handled here.

## Contents

- **Functions:** [`publish_banner`](#publish_banner), [`publish_cve`](#publish_cve), [`append_note`](#append_note), [`register_loot_event`](#register_loot_event), [`refresh_session_report`](#refresh_session_report), [`severity_to_risk`](#severity_to_risk), [`group_tasks_for_display`](#group_tasks_for_display)

## Functions

<a id="publish_banner"></a>

### `publish_banner`

`function` | [modules/c2_surfaces.py:73](../../modules/c2_surfaces.py#L73)

```python
def publish_banner(hostname: str = '', port: str | int = '', protocol: str = 'tcp', service: str = '', extra: str = '', sessions_dir: Path | str = _SESSIONS_DIR) -> bool
```

Append a service banner to sessions/banners.json (deduplicated).

Matches the ``/banners`` table columns (Hostname, Port, Protocol,
Extra, Service). Returns True when stored (or already present).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `hostname` | `str` | `''` |  |
| `port` | `str \| int` | `''` |  |
| `protocol` | `str` | `'tcp'` |  |
| `service` | `str` | `''` |  |
| `extra` | `str` | `''` |  |
| `sessions_dir` | `Path \| str` | `_SESSIONS_DIR` |  |

**Returns:** `bool`

*Called by:* [`apply`](modules.sinks.c2_surfaces.py.md#apply)

---

<a id="publish_cve"></a>

### `publish_cve`

`function` | [modules/c2_surfaces.py:115](../../modules/c2_surfaces.py#L115)

```python
def publish_cve(title: str, description: str = '', operator: str = 'autonomous_loop', risk: str = 'HIGH', sessions_dir: Path | str = _SESSIONS_DIR) -> bool
```

Append a CVE finding to sessions/cves.json (deduplicated by title).

``risk`` must be one of CRITICAL/HIGH/MEDIUM/LOW/INFORMATIONAL
(mirrors the /cves form validation). Returns True when stored or
already present.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `title` | `str` |  |  |
| `description` | `str` | `''` |  |
| `operator` | `str` | `'autonomous_loop'` |  |
| `risk` | `str` | `'HIGH'` |  |
| `sessions_dir` | `Path \| str` | `_SESSIONS_DIR` |  |

**Returns:** `bool`

*Called by:* [`apply`](modules.sinks.c2_surfaces.py.md#apply)

---

<a id="append_note"></a>

### `append_note`

`function` | [modules/c2_surfaces.py:155](../../modules/c2_surfaces.py#L155)

```python
def append_note(line: str, sessions_dir: Path | str = _SESSIONS_DIR) -> bool
```

Append one timestamped line to sessions/notes.txt (never overwrites).

The dashboard stores a single ``{"content": ...}`` blob; appending
preserves operator notes while surfacing loop/loot events.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` | `str` |  |  |
| `sessions_dir` | `Path \| str` | `_SESSIONS_DIR` |  |

**Returns:** `bool`

*Called by:* [`apply`](modules.sinks.c2_surfaces.py.md#apply)

---

<a id="register_loot_event"></a>

### `register_loot_event`

`function` | [modules/c2_surfaces.py:184](../../modules/c2_surfaces.py#L184)

```python
def register_loot_event(name: str, path_glob: str, description: str = '', event_config: Path | str = _EVENT_CONFIG) -> bool
```

Register an event_config.json rule watching an artefact glob.

Lets the C2 event engine track loop-produced artefacts (loot,
emulation reports) like any operator-defined rule. Dedupes by rule
name. Returns True when stored or already present.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `path_glob` | `str` |  |  |
| `description` | `str` | `''` |  |
| `event_config` | `Path \| str` | `_EVENT_CONFIG` |  |

**Returns:** `bool`

---

<a id="refresh_session_report"></a>

### `refresh_session_report`

`function` | [modules/c2_surfaces.py:229](../../modules/c2_surfaces.py#L229)

```python
def refresh_session_report(timeout: int = 120) -> bool
```

Regenerate sessions/sessionLazyOwn.json via modules/session_state.py.

This is what the legacy ``/report`` page renders. Best-effort
subprocess with a timeout; never raises.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `timeout` | `int` | `120` |  |

**Returns:** `bool`

---

<a id="severity_to_risk"></a>

### `severity_to_risk`

`function` | [modules/c2_surfaces.py:251](../../modules/c2_surfaces.py#L251)

```python
def severity_to_risk(severity: str) -> str
```

Map exploit severity words to /cves risk levels.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `severity` | `str` |  |  |

**Returns:** `str`

*Called by:* [`apply`](modules.sinks.c2_surfaces.py.md#apply)

---

<a id="group_tasks_for_display"></a>

### `group_tasks_for_display`

`function` | [modules/c2_surfaces.py:261](../../modules/c2_surfaces.py#L261)

```python
def group_tasks_for_display(tasks: list) -> tuple[list, int]
```

Group tasks for the /tasks page: unique hits with counts + noise tally.

Uses the shared `[`audit_tasks`](skills.lazyown_mcp_helpers.py.md#audit_tasks)` classifier when importable (drops
timestamp/URL bogus credentials and duplicate titles); falls back to
plain title grouping otherwise. Never raises — worst case returns
every task as its own group. Returns (groups, noise_count) where
each group is {"task": first_task_dict, "count": n}.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `tasks` | `list` |  |  |

**Returns:** `tuple[list, int]`

---
