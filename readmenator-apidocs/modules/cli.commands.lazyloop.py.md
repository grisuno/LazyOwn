# `cli.commands.lazyloop`

> Source: [cli/commands/lazyloop.py:1](../../cli/commands/lazyloop.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Lazy queue and misc command set.

Engine-backed operator surface with ``lazy_`` names. Every command here
reads or writes the single `[`modules.lazy_engine`](modules.lazy_engine.py.md)` store, so queue,
findings, verdicts and guard reviews always match what the autonomous
loop (``lazy_loop`` / ``auto_loop``) sees. The per-task engine surface
(status, broadcast, trace, hint, steer, kill, retest) lives in
`[`cli.commands.lazyops`](cli.commands.lazyops.py.md)`; no name is duplicated across both sets.

## Contents

- **Classes:** [`LazyQueueCommandSet`](#lazyqueuecommandset)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class LazyQueueCommandSet
    LazyQueueCommandSet : phase
    LazyQueueCommandSet : category
    LazyQueueCommandSet : do_lazy_sync()
    LazyQueueCommandSet : do_lazy_intents()
    LazyQueueCommandSet : do_lazy_delete()
    LazyQueueCommandSet : do_lazy_findings()
    LazyQueueCommandSet : do_lazy_handoff()
    LazyQueueCommandSet : do_lazy_verdict()
    LazyQueueCommandSet : do_lazy_mention()
    LazyQueueCommandSet : do_lazy_approve()
    LazyQueueCommandSet : do_lazy_fleet()
    LazyQueueCommandSet : do_lazy_orchestrator()
    LazyQueueCommandSet : do_lazy_view()
    LazyQueueCommandSet : do_lazy_monitor
    class LazyOwnCommandSet
    LazyOwnCommandSet <|-- LazyQueueCommandSet
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_handoff(["LazyQueueCommandSet.do_lazy_handoff"])
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_findings(["LazyQueueCommandSet.do_lazy_findings"])
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_sync(["LazyQueueCommandSet.do_lazy_sync"])
    n_core_console_py__print_error["console.print_error"]
    n_core_console_py__print_msg["console.print_msg"]
    n_modules_lazy_bridge_py__sync_all["lazy_bridge.sync_all"]
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_intents(["LazyQueueCommandSet.do_lazy_intents"])
    n_modules_lazy_loop_py__ExplorationGraph___init__["lazy_loop.ExplorationGraph.__init__"]
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_delete(["LazyQueueCommandSet.do_lazy_delete"])
    n_cli_commands__base_py__extract_flag["_base.extract_flag"]
    n_modules_sinks_findings_py__ledger_for["findings.ledger_for"]
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_verdict(["LazyQueueCommandSet.do_lazy_verdict"])
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_mention(["LazyQueueCommandSet.do_lazy_mention"])
    n_modules_lazy_mentions_py__search_mentions_page["lazy_mentions.search_mentions_page"]
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_approve(["LazyQueueCommandSet.do_lazy_approve"])
    n_modules_lazy_loop_py__Guard_audit["lazy_loop.Guard.audit"]
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_fleet(["LazyQueueCommandSet.do_lazy_fleet"])
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_handoff --> n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_findings
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_sync -.-> n_core_console_py__print_error
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_sync -.-> n_core_console_py__print_msg
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_sync -.-> n_modules_lazy_bridge_py__sync_all
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_intents -.-> n_core_console_py__print_error
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_intents -.-> n_core_console_py__print_msg
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_intents -.-> n_modules_lazy_loop_py__ExplorationGraph___init__
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_delete -.-> n_cli_commands__base_py__extract_flag
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_delete -.-> n_core_console_py__print_error
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_delete -.-> n_core_console_py__print_msg
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_findings -.-> n_core_console_py__print_error
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_findings -.-> n_core_console_py__print_msg
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_findings -.-> n_modules_lazy_loop_py__ExplorationGraph___init__
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_findings -.-> n_modules_sinks_findings_py__ledger_for
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_verdict -.-> n_cli_commands__base_py__extract_flag
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_verdict -.-> n_core_console_py__print_error
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_verdict -.-> n_core_console_py__print_msg
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_mention -.-> n_core_console_py__print_error
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_mention -.-> n_core_console_py__print_msg
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_mention -.-> n_modules_lazy_mentions_py__search_mentions_page
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_approve -.-> n_core_console_py__print_error
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_approve -.-> n_core_console_py__print_msg
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_approve -.-> n_modules_lazy_loop_py__Guard_audit
    n_cli_commands_lazyloop_py__LazyQueueCommandSet_do_lazy_fleet -.-> n_core_console_py__print_error
```

## Classes

<a id="lazyqueuecommandset"></a>

### `LazyQueueCommandSet`

`class` | [cli/commands/lazyloop.py:29](../../cli/commands/lazyloop.py#L29)

```python
class LazyQueueCommandSet(LazyOwnCommandSet)
```

Bases: [`LazyOwnCommandSet`](cli.commands._base.py.md#lazyowncommandset)

Lazy queue controls backed by the loop engine.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`phase`](#lazyqueuecommandset-phase) |  | `'exploit'` |  |
| [`category`](#lazyqueuecommandset-category) |  | `'16. Artificial Intelligence'` |  |
| [`do_lazy_monitor`](#lazyqueuecommandset-do_lazy_monitor) |  | `do_lazy_view` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`do_lazy_sync`](#lazyqueuecommandset-do_lazy_sync) | method | Run bidirectional LAZY sync into world model and objectives. |
| [`do_lazy_intents`](#lazyqueuecommandset-do_lazy_intents) | method | List engine intents for a task, optionally filtered by state. |
| [`do_lazy_delete`](#lazyqueuecommandset-do_lazy_delete) | method | Delete an engine intent; soft keeps outputs, hard cascades. |
| [`do_lazy_findings`](#lazyqueuecommandset-do_lazy_findings) | method | List engine findings for a task, optionally filtered by status. |
| [`do_lazy_handoff`](#lazyqueuecommandset-do_lazy_handoff) | method | Print the operator handoff for a finished loop task. |
| [`do_lazy_verdict`](#lazyqueuecommandset-do_lazy_verdict) | method | Record a manual retest verdict on an engine finding. |
| [`do_lazy_mention`](#lazyqueuecommandset-do_lazy_mention) | method | Search @ mention candidates with scroll pagination. |
| [`do_lazy_approve`](#lazyqueuecommandset-do_lazy_approve) | method | List engine guard reviews filtered by decision and source. |
| [`do_lazy_fleet`](#lazyqueuecommandset-do_lazy_fleet) | method | Cross-task fleet: list \| graph <task> \| findings <task> \| traces <task> [query] \| node <task> <id> \| pause <task> \| resume <task> \| report <task> <finding>... |
| [`do_lazy_orchestrator`](#lazyqueuecommandset-do_lazy_orchestrator) | method | Admin console for the loop (Textual TUI). |
| [`do_lazy_view`](#lazyqueuecommandset-do_lazy_view) | method | Attach the live worker monitor to a task (or the newest task). |

<a id="lazyqueuecommandset-do_lazy_sync"></a>

#### `LazyQueueCommandSet.do_lazy_sync`

`method` | [cli/commands/lazyloop.py:36](../../cli/commands/lazyloop.py#L36)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_sync(self, line)
```

Run bidirectional LAZY sync into world model and objectives.

Usage:
    lazy_sync

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg), [`sync_all`](modules.lazy_bridge.py.md#sync_all)

<a id="lazyqueuecommandset-do_lazy_intents"></a>

#### `LazyQueueCommandSet.do_lazy_intents`

`method` | [cli/commands/lazyloop.py:51](../../cli/commands/lazyloop.py#L51)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_intents(self, line)
```

List engine intents for a task, optionally filtered by state.

Usage:
    lazy_intents <task_id> [state]

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg), [`ExplorationGraph.__init__`](modules.lazy_loop.py.md#explorationgraph-__init__)

<a id="lazyqueuecommandset-do_lazy_delete"></a>

#### `LazyQueueCommandSet.do_lazy_delete`

`method` | [cli/commands/lazyloop.py:71](../../cli/commands/lazyloop.py#L71)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_delete(self, line)
```

Delete an engine intent; soft keeps outputs, hard cascades.

Usage:
    lazy_delete <task_id> <intent_id> --reason <text> [--hard] [--yes]

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`extract_flag`](cli.commands._base.py.md#extract_flag), [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg)

<a id="lazyqueuecommandset-do_lazy_findings"></a>

#### `LazyQueueCommandSet.do_lazy_findings`

`method` | [cli/commands/lazyloop.py:110](../../cli/commands/lazyloop.py#L110)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_findings(self, line)
```

List engine findings for a task, optionally filtered by status.

Usage:
    lazy_findings <task_id> [status]   - graph findings (status filter)
    lazy_findings <task_id> ledger     - durable engagement ledger rows
    lazy_findings <task_id> handoff    - operator handoff from the ledger

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg), [`ExplorationGraph.__init__`](modules.lazy_loop.py.md#explorationgraph-__init__), [`ledger_for`](modules.sinks.findings.py.md#ledger_for)

*Called by:* [`LazyQueueCommandSet.do_lazy_handoff`](#lazyqueuecommandset-do_lazy_handoff)

<a id="lazyqueuecommandset-do_lazy_handoff"></a>

#### `LazyQueueCommandSet.do_lazy_handoff`

`method` | [cli/commands/lazyloop.py:180](../../cli/commands/lazyloop.py#L180)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_handoff(self, line)
```

Print the operator handoff for a finished loop task.

Usage:
    lazy_handoff <task_id>

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`LazyQueueCommandSet.do_lazy_findings`](#lazyqueuecommandset-do_lazy_findings)

<a id="lazyqueuecommandset-do_lazy_verdict"></a>

#### `LazyQueueCommandSet.do_lazy_verdict`

`method` | [cli/commands/lazyloop.py:190](../../cli/commands/lazyloop.py#L190)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_verdict(self, line)
```

Record a manual retest verdict on an engine finding.

Usage:
    lazy_verdict <task_id> <finding_id> <reproduced|fixed|inconclusive> [--note <text>]

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`extract_flag`](cli.commands._base.py.md#extract_flag), [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg)

<a id="lazyqueuecommandset-do_lazy_mention"></a>

#### `LazyQueueCommandSet.do_lazy_mention`

`method` | [cli/commands/lazyloop.py:213](../../cli/commands/lazyloop.py#L213)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_mention(self, line)
```

Search @ mention candidates with scroll pagination.

Usage:
    lazy_mention [kind] [query] [--cursor C]

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg), [`search_mentions_page`](modules.lazy_mentions.py.md#search_mentions_page)

<a id="lazyqueuecommandset-do_lazy_approve"></a>

#### `LazyQueueCommandSet.do_lazy_approve`

`method` | [cli/commands/lazyloop.py:248](../../cli/commands/lazyloop.py#L248)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_approve(self, line)
```

List engine guard reviews filtered by decision and source.

Usage:
    lazy_approve <task_id> [ALLOW|ASK|DENY] [source]

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg), [`Guard.audit`](modules.lazy_loop.py.md#guard-audit)

<a id="lazyqueuecommandset-do_lazy_fleet"></a>

#### `LazyQueueCommandSet.do_lazy_fleet`

`method` | [cli/commands/lazyloop.py:270](../../cli/commands/lazyloop.py#L270)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_fleet(self, line)
```

Cross-task fleet: list | graph <task> | findings <task> | traces <task> [query] | node <task> <id> | pause <task> | resume <task> | report <task> <finding> <text...>

Usage:
    lazy_fleet list
    lazy_fleet graph t0001
    lazy_fleet findings t0001
    lazy_fleet traces t0001 ssh
    lazy_fleet node t0001 12
    lazy_fleet pause t0001
    lazy_fleet report t0001 7 ## Summary ...

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg)

<a id="lazyqueuecommandset-do_lazy_orchestrator"></a>

#### `LazyQueueCommandSet.do_lazy_orchestrator`

`method` | [cli/commands/lazyloop.py:335](../../cli/commands/lazyloop.py#L335)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_orchestrator(self, line)
```

Admin console for the loop (Textual TUI).

Tabs: Now (what the orchestrator is executing right now, live
activity tail and per-worker current command), Config (payload
knobs the runner reads), Verbs (searchable command picker when
adding a verb), Playbooks (full CRUD over playbooks/*.yaml with
preview and raw YAML editing), Gyms (YAML catalogue plus
persistent active runs; space starts or stops the selected gym),
Chains (APT chain YAML administration: preview, enable/disable,
generate from playbook, delete), Profiles (activate orchestration
profiles), Models (LLM failover chain add/remove), Params (shared
parameter catalog: declare a reusable parameter once and use it in
every addon), Guard (intercept rules add/remove). Keys: r refresh,
s save config, a add, e edit, d delete, space toggle, q quit.

Usage:
    lazy_orchestrator [task_id]

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`run_orchestrator_console`](cli.lazy_orchestrator.py.md#run_orchestrator_console), [`print_error`](core.console.py.md#print_error)

<a id="lazyqueuecommandset-do_lazy_view"></a>

#### `LazyQueueCommandSet.do_lazy_view`

`method` | [cli/commands/lazyloop.py:364](../../cli/commands/lazyloop.py#L364)

Decorators: `@cmd2.with_category(exploitation_category)`

```python
def do_lazy_view(self, line)
```

Attach the live worker monitor to a task (or the newest task).

Split panes per worker plus audit tabs (activity, guard,
traffic, findings) and operator keys: q quit, p/r pause/resume,
a/d approve/deny first pending intercept, h hint, s steer,
k kill. Works from a second terminal while ``lazy_loop`` runs.

Usage:
    lazy_view [task_id]

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`run_monitor_command`](cli.lazy_monitor.py.md#run_monitor_command), [`print_error`](core.console.py.md#print_error)

---
