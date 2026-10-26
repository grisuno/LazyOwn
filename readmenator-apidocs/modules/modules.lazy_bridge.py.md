# `modules.lazy_bridge`

> Source: [modules/lazy_bridge.py:1](../../modules/lazy_bridge.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Bidirectional LAZY <-> LazyOwn bridge.

LAZY runs standalone under sessions/lazy with its own tasks, assets,
experiment graphs, activity transcripts, traffic logs and guard audits.
This bridge syncs that universe with LazyOwn world_model, objectives,
evidence vault, traffic recorder, finding lifecycle and campaign DB in
both directions without touching LAZY runtime files.

## Contents

- **Functions:** [`lazy_tasks`](#lazy_tasks), [`lazy_assets`](#lazy_assets), [`lazy_graph`](#lazy_graph), [`lazy_activity`](#lazy_activity), [`lazy_traffic`](#lazy_traffic), [`lazy_guard_audit`](#lazy_guard_audit), [`bridge_status`](#bridge_status), [`pull_to_world_model`](#pull_to_world_model), [`pull_to_objectives`](#pull_to_objectives), [`pull_findings_to_lifecycle`](#pull_findings_to_lifecycle), [`pull_traffic_to_recorder`](#pull_traffic_to_recorder), [`push_objective_to_lazy`](#push_objective_to_lazy), [`push_tasks_to_c2`](#push_tasks_to_c2), [`sync_all`](#sync_all)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_lazy_bridge_py__bridge_status(["bridge_status"])
    n_modules_lazy_bridge_py__lazy_activity(["lazy_activity"])
    n_modules_lazy_bridge_py__lazy_assets(["lazy_assets"])
    n_modules_lazy_bridge_py__lazy_graph(["lazy_graph"])
    n_modules_lazy_bridge_py__lazy_guard_audit(["lazy_guard_audit"])
    n_modules_lazy_bridge_py__lazy_tasks(["lazy_tasks"])
    n_modules_lazy_bridge_py__lazy_traffic(["lazy_traffic"])
    n_modules_lazy_bridge_py__pull_to_world_model(["pull_to_world_model"])
    n_modules_lazy_bridge_py__pull_to_objectives(["pull_to_objectives"])
    n_modules_lazy_bridge_py__pull_findings_to_lifecycle(["pull_findings_to_lifecycle"])
    n_modules_lazy_bridge_py__pull_traffic_to_recorder(["pull_traffic_to_recorder"])
    n_modules_lazy_bridge_py__push_tasks_to_c2(["push_tasks_to_c2"])
    n_modules_lazy_bridge_py__sync_all(["sync_all"])
    n_modules_lazy_bridge_py__bridge_status --> n_modules_lazy_bridge_py__lazy_activity
    n_modules_lazy_bridge_py__bridge_status --> n_modules_lazy_bridge_py__lazy_assets
    n_modules_lazy_bridge_py__bridge_status --> n_modules_lazy_bridge_py__lazy_graph
    n_modules_lazy_bridge_py__bridge_status --> n_modules_lazy_bridge_py__lazy_guard_audit
    n_modules_lazy_bridge_py__bridge_status --> n_modules_lazy_bridge_py__lazy_tasks
    n_modules_lazy_bridge_py__bridge_status --> n_modules_lazy_bridge_py__lazy_traffic
    n_modules_lazy_bridge_py__pull_to_world_model --> n_modules_lazy_bridge_py__lazy_assets
    n_modules_lazy_bridge_py__pull_to_world_model --> n_modules_lazy_bridge_py__lazy_graph
    n_modules_lazy_bridge_py__pull_to_world_model --> n_modules_lazy_bridge_py__lazy_tasks
    n_modules_lazy_bridge_py__pull_to_objectives --> n_modules_lazy_bridge_py__lazy_tasks
    n_modules_lazy_bridge_py__pull_findings_to_lifecycle --> n_modules_lazy_bridge_py__lazy_graph
    n_modules_lazy_bridge_py__pull_findings_to_lifecycle --> n_modules_lazy_bridge_py__lazy_tasks
    n_modules_lazy_bridge_py__pull_traffic_to_recorder --> n_modules_lazy_bridge_py__lazy_tasks
    n_modules_lazy_bridge_py__push_tasks_to_c2 --> n_modules_lazy_bridge_py__lazy_tasks
    n_modules_lazy_bridge_py__sync_all --> n_modules_lazy_bridge_py__pull_findings_to_lifecycle
    n_modules_lazy_bridge_py__sync_all --> n_modules_lazy_bridge_py__pull_to_objectives
    n_modules_lazy_bridge_py__sync_all --> n_modules_lazy_bridge_py__pull_to_world_model
    n_modules_lazy_bridge_py__sync_all --> n_modules_lazy_bridge_py__pull_traffic_to_recorder
    n_modules_lazy_bridge_py__sync_all --> n_modules_lazy_bridge_py__push_tasks_to_c2
```

## Functions

<a id="lazy_tasks"></a>

### `lazy_tasks`

`function` | [modules/lazy_bridge.py:92](../../modules/lazy_bridge.py#L92)

```python
def lazy_tasks() -> dict
```

Load LAZY task registry.

**Returns:** `dict` - Task map keyed by task id.

*Called by:* [`bridge_status`](#bridge_status), [`pull_findings_to_lifecycle`](#pull_findings_to_lifecycle), [`pull_to_objectives`](#pull_to_objectives), [`pull_to_world_model`](#pull_to_world_model), [`pull_traffic_to_recorder`](#pull_traffic_to_recorder), [`push_tasks_to_c2`](#push_tasks_to_c2)

---

<a id="lazy_assets"></a>

### `lazy_assets`

`function` | [modules/lazy_bridge.py:103](../../modules/lazy_bridge.py#L103)

```python
def lazy_assets() -> list[dict]
```

Load LAZY asset nodes.

**Returns:** `list[dict]` - Asset node list.

*Called by:* [`bridge_status`](#bridge_status), [`pull_to_world_model`](#pull_to_world_model)

---

<a id="lazy_graph"></a>

### `lazy_graph`

`function` | [modules/lazy_bridge.py:114](../../modules/lazy_bridge.py#L114)

```python
def lazy_graph(task_id: str) -> dict
```

Load experiment graph for a task.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  | LAZY task id. |

**Returns:** `dict` - Graph dict with nodes, edges and anchors.

*Called by:* [`bridge_status`](#bridge_status), [`pull_findings_to_lifecycle`](#pull_findings_to_lifecycle), [`pull_to_world_model`](#pull_to_world_model)

---

<a id="lazy_activity"></a>

### `lazy_activity`

`function` | [modules/lazy_bridge.py:127](../../modules/lazy_bridge.py#L127)

```python
def lazy_activity(task_id: str) -> list[dict]
```

Load activity transcript for a task.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  | LAZY task id. |

**Returns:** `list[dict]` - Activity row list.

*Called by:* [`bridge_status`](#bridge_status)

---

<a id="lazy_traffic"></a>

### `lazy_traffic`

`function` | [modules/lazy_bridge.py:139](../../modules/lazy_bridge.py#L139)

```python
def lazy_traffic(task_id: str) -> list[dict]
```

Load traffic log for a task.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  | LAZY task id. |

**Returns:** `list[dict]` - Traffic row list.

*Called by:* [`bridge_status`](#bridge_status)

---

<a id="lazy_guard_audit"></a>

### `lazy_guard_audit`

`function` | [modules/lazy_bridge.py:151](../../modules/lazy_bridge.py#L151)

```python
def lazy_guard_audit(task_id: str) -> list[dict]
```

Load guard audit for a task.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  | LAZY task id. |

**Returns:** `list[dict]` - Guard audit row list.

*Called by:* [`bridge_status`](#bridge_status)

---

<a id="bridge_status"></a>

### `bridge_status`

`function` | [modules/lazy_bridge.py:163](../../modules/lazy_bridge.py#L163)

```python
def bridge_status() -> dict
```

Summarize LAZY universe and last sync cursor.

**Returns:** `dict` - Status dict with counts per task.

*Calls:* [`lazy_activity`](#lazy_activity), [`lazy_assets`](#lazy_assets), [`lazy_graph`](#lazy_graph), [`lazy_guard_audit`](#lazy_guard_audit), [`lazy_tasks`](#lazy_tasks), [`lazy_traffic`](#lazy_traffic)

---

<a id="pull_to_world_model"></a>

### `pull_to_world_model`

`function` | [modules/lazy_bridge.py:221](../../modules/lazy_bridge.py#L221)

```python
def pull_to_world_model() -> dict
```

Sync LAZY graphs and assets into LazyOwn world model.

Hosts, services (with the version nmap captured), finding CVE ids
and OS hints all land on the world model, which feeds the intel
graph, the attack graph and the exposure scoring.

**Returns:** `dict` - Summary with hosts, services, vulnerabilities and facts synced.

*Calls:* [`lazy_assets`](#lazy_assets), [`lazy_graph`](#lazy_graph), [`lazy_tasks`](#lazy_tasks)

*Called by:* [`sync_all`](#sync_all)

---

<a id="pull_to_objectives"></a>

### `pull_to_objectives`

`function` | [modules/lazy_bridge.py:298](../../modules/lazy_bridge.py#L298)

```python
def pull_to_objectives() -> dict
```

Inject open LAZY tasks as LazyOwn objectives without duplicates.

**Returns:** `dict` - Summary with injected count.

*Calls:* [`lazy_tasks`](#lazy_tasks)

*Called by:* [`sync_all`](#sync_all)

---

<a id="pull_findings_to_lifecycle"></a>

### `pull_findings_to_lifecycle`

`function` | [modules/lazy_bridge.py:333](../../modules/lazy_bridge.py#L333)

```python
def pull_findings_to_lifecycle() -> dict
```

Confirm LAZY finding nodes in LazyOwn finding lifecycle.

**Returns:** `dict` - Summary with confirmed count.

*Calls:* [`lazy_graph`](#lazy_graph), [`lazy_tasks`](#lazy_tasks)

*Called by:* [`sync_all`](#sync_all)

---

<a id="pull_traffic_to_recorder"></a>

### `pull_traffic_to_recorder`

`function` | [modules/lazy_bridge.py:408](../../modules/lazy_bridge.py#L408)

```python
def pull_traffic_to_recorder(progress=None) -> dict
```

Mirror new LAZY traffic rows into the LazyOwn recorder index.

The byte offset per task is persisted in ``lazy_bridge_sync.json`` so
repeated syncs stay proportional to new activity instead of replaying
the whole transcript (which used to stall the loop watchdog).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `progress` |  | `None` | Optional callback receiving short progress strings. |

**Returns:** `dict` - Summary with mirrored count and byte offsets committed.

*Calls:* [`lazy_tasks`](#lazy_tasks)

*Called by:* [`sync_all`](#sync_all)

---

<a id="push_objective_to_lazy"></a>

### `push_objective_to_lazy`

`function` | [modules/lazy_bridge.py:476](../../modules/lazy_bridge.py#L476)

```python
def push_objective_to_lazy(goal: str, scope: list[str] | None = None) -> dict
```

Export a LazyOwn objective as an LAZY-compatible task draft.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `goal` | `str` |  | Objective text. |
| `scope` | `list[str] \| None` | `None` | Scope ip list. |

**Returns:** `dict` - Draft task record written under sessions/lazy_drafts/.

---

<a id="push_tasks_to_c2"></a>

### `push_tasks_to_c2`

`function` | [modules/lazy_bridge.py:501](../../modules/lazy_bridge.py#L501)

```python
def push_tasks_to_c2(only: list[str] | None = None) -> dict
```

Mirror loop tasks into the lazyc2 Kanban board (sessions/tasks.json).

One C2 card per loop task, upserted through a persisted id map so
repeated syncs update the card instead of duplicating it. Statuses
follow the C2 vocabulary (New/Started/Blocked/Review/Done).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `only` | `list[str] \| None` | `None` | Optional task id subset to sync. |

**Returns:** `dict` - Dict with created/updated counts.

*Calls:* [`lazy_tasks`](#lazy_tasks)

*Called by:* [`sync_all`](#sync_all)

---

<a id="sync_all"></a>

### `sync_all`

`function` | [modules/lazy_bridge.py:566](../../modules/lazy_bridge.py#L566)

```python
def sync_all(progress=None) -> dict
```

Run full bidirectional pull plus lifecycle, traffic and board mirror.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `progress` |  | `None` | Optional callback receiving one short string before each stage and during traffic mirroring so the loop watchdog sees progress on large stores. |

**Returns:** `dict` - Combined sync summary.

*Calls:* [`pull_findings_to_lifecycle`](#pull_findings_to_lifecycle), [`pull_to_objectives`](#pull_to_objectives), [`pull_to_world_model`](#pull_to_world_model), [`pull_traffic_to_recorder`](#pull_traffic_to_recorder), [`push_tasks_to_c2`](#push_tasks_to_c2)

*Called by:* [`LazyQueueCommandSet.do_lazy_sync`](cli.commands.lazyloop.py.md#lazyqueuecommandset-do_lazy_sync)

---
