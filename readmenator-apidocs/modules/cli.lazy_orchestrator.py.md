# `cli.lazy_orchestrator`

> Source: [cli/lazy_orchestrator.py:1](../../cli/lazy_orchestrator.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Orchestrator admin console for the autonomous loop.

A Textual TUI in the spirit of the marketplace configurator:

- Now: what the loop is executing right now (task, stages, live activity
  tail, per-worker current command);
- Config: every payload knob the runner reads (rounds, workers,
  heartbeat, verb timeout, agentic flags, NOA, proxy);
- Verbs: auto-verb registry with a searchable command picker;
- Playbooks: full CRUD over the YAML playbooks under ``playbooks/``;
- Gyms: YAML gym catalogue with persistent runs from the world model;
- Chains: APT chain YAML administration;
- Models: the LLM failover chain (add/remove members);
- Guard: the intercept rules (add/remove).

Edits persist straight to ``payload.json`` (or a sandbox path in tests)
through `[`core.config`](core.config.py.md)`; playbook changes are confined to the playbooks
directory and written atomically.

## Contents

- **Classes:** [`LazyOrchestratorApp`](#lazyorchestratorapp)
- **Functions:** [`run_orchestrator_console`](#run_orchestrator_console)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class LazyOrchestratorApp
    LazyOrchestratorApp : CSS
    LazyOrchestratorApp : BINDINGS
    LazyOrchestratorApp : __init__()
    LazyOrchestratorApp : compose()
    LazyOrchestratorApp : on_mount()
    LazyOrchestratorApp : toggle_stage()
    LazyOrchestratorApp : toggle_verb()
    LazyOrchestratorApp : add_auto_verb()
    LazyOrchestratorApp : remove_auto_verb()
    LazyOrchestratorApp : playbook_rows()
    LazyOrchestratorApp : playbook_preview()
    LazyOrchestratorApp : create_playbook_file()
    LazyOrchestratorApp : save_playbook_text()
    LazyOrchestratorApp : delete_playbook_file()
    LazyOrchestratorApp : playbook_candidates()
    LazyOrchestratorApp : gym_rows()
    LazyOrchestratorApp : gym_preview()
    LazyOrchestratorApp : start_gym()
    LazyOrchestratorApp : stop_gym()
    LazyOrchestratorApp : toggle_gym()
    LazyOrchestratorApp : profile_rows()
    LazyOrchestratorApp : activate_profile()
    LazyOrchestratorApp : chain_rows()
    LazyOrchestratorApp : chain_steps_preview()
    class App
    App <|-- LazyOrchestratorApp
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_playbook_preview(["LazyOrchestratorApp.playbook_preview"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_playbook_rows(["LazyOrchestratorApp.playbook_rows"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_gym(["LazyOrchestratorApp.toggle_gym"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_gym_rows(["LazyOrchestratorApp.gym_rows"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_start_gym(["LazyOrchestratorApp.start_gym"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_stop_gym(["LazyOrchestratorApp.stop_gym"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_on_button_pressed(["LazyOrchestratorApp.on_button_pressed"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_save_config(["LazyOrchestratorApp.save_config"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item(["LazyOrchestratorApp.action_toggle_item"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_activate_profile(["LazyOrchestratorApp.activate_profile"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_chain(["LazyOrchestratorApp.toggle_chain"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_stage(["LazyOrchestratorApp.toggle_stage"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_verb(["LazyOrchestratorApp.toggle_verb"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_save_config(["LazyOrchestratorApp.action_save_config"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item(["LazyOrchestratorApp.action_add_item"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_auto_verb(["LazyOrchestratorApp.add_auto_verb"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_guard_rule(["LazyOrchestratorApp.add_guard_rule"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_model_member(["LazyOrchestratorApp.add_model_member"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_create_playbook_file(["LazyOrchestratorApp.create_playbook_file"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_generate_chain(["LazyOrchestratorApp.generate_chain"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_playbook_candidates(["LazyOrchestratorApp.playbook_candidates"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_edit_item(["LazyOrchestratorApp.action_edit_item"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_set_model_priority(["LazyOrchestratorApp.set_model_priority"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item(["LazyOrchestratorApp.action_delete_item"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_delete_playbook_file(["LazyOrchestratorApp.delete_playbook_file"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_auto_verb(["LazyOrchestratorApp.remove_auto_verb"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_chain(["LazyOrchestratorApp.remove_chain"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_guard_rule(["LazyOrchestratorApp.remove_guard_rule"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_model_member(["LazyOrchestratorApp.remove_model_member"])
    n_cli_lazy_orchestrator_py__run_orchestrator_console(["run_orchestrator_console"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp___init__(["LazyOrchestratorApp.__init__"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_playbook_preview --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_playbook_rows
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_gym --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_gym_rows
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_gym --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_start_gym
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_gym --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_stop_gym
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_on_button_pressed --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_save_config
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_activate_profile
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_chain
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_gym
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_stage
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_save_config --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_save_config
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_auto_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_guard_rule
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_model_member
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_create_playbook_file
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_generate_chain
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_playbook_candidates
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_edit_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_set_model_priority
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_delete_playbook_file
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_auto_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_chain
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_guard_rule
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_model_member
    n_cli_lazy_orchestrator_py__run_orchestrator_console --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp___init__
```

## Classes

<a id="lazyorchestratorapp"></a>

### `LazyOrchestratorApp`

`class` | [cli/lazy_orchestrator.py:170](../../cli/lazy_orchestrator.py#L170)

```python
class LazyOrchestratorApp(App[None])
```

Bases: [`App[None]`](lazy_sentinel4.py.md#app)

Admin console: Now / Config / Verbs / Chains / Models / Guard.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`CSS`](#lazyorchestratorapp-css) |  | `'\n #now-status { height: 6; border: round $accent; padding: 0 1; }\n #now-log { height: 1fr; border: round $primary; }\n #config-status { height: 3; color: $text-muted; }\n #chains-detail, #profiles-detail, #playbooks-detail, #gyms-detail { height: 10;\n border: round $secondary; padding: 0 1; }\n DataTable { height: 1fr; }\n .modal-box { width: 70; height: auto; padding: 1 2; background: $surface;\n border: round $accent; }\n .modal-box-wide { width: 100; height: 38; padding: 1 2; background: $surface;\n border: round $accent; }\n .modal-title { text-style: bold; padding-bottom: 1; }\n .modal-label { padding-top: 1; }\n .modal-hint { color: $text-muted; padding-top: 1; }\n .modal-error { color: $error; padding-top: 1; }\n '` |  |
| [`BINDINGS`](#lazyorchestratorapp-bindings) |  | `[Binding('q', 'quit', 'Quit'), Binding('r', 'refresh', 'Refresh'), Binding('s', 'save_config', 'Save config'), Binding('space', 'toggle_item', 'Toggle'), Binding('a', 'add_item', 'Add'), Binding('e', 'edit_item', 'Edit'), Binding('d', 'delete_item', 'Delete')]` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#lazyorchestratorapp-__init__) | constructor | Bind the console to a payload file and an optional task. |
| [`compose`](#lazyorchestratorapp-compose) | method | Build the four panes. |
| [`on_mount`](#lazyorchestratorapp-on_mount) | method | Load the payload into the form and refresh the data tables. |
| [`toggle_stage`](#lazyorchestratorapp-toggle_stage) | method | Flip one pipeline stage on/off and persist it. |
| [`toggle_verb`](#lazyorchestratorapp-toggle_verb) | method | Flip one auto verb on/off and persist it. |
| [`add_auto_verb`](#lazyorchestratorapp-add_auto_verb) | method | Register a new operator-defined auto verb. |
| [`remove_auto_verb`](#lazyorchestratorapp-remove_auto_verb) | method | Delete a custom verb, or disable a built-in one. |
| [`playbook_rows`](#lazyorchestratorapp-playbook_rows) | method | Return one row per playbook file, including invalid ones. |
| [`playbook_preview`](#lazyorchestratorapp-playbook_preview) | method | Return a bounded YAML preview for one playbook file. |
| [`create_playbook_file`](#lazyorchestratorapp-create_playbook_file) | method | Create one playbook YAML and repaint the table. |
| [`save_playbook_text`](#lazyorchestratorapp-save_playbook_text) | method | Validate and persist raw YAML edited by the operator. |
| [`delete_playbook_file`](#lazyorchestratorapp-delete_playbook_file) | method | Delete one playbook YAML after the operator confirms. |
| [`playbook_candidates`](#lazyorchestratorapp-playbook_candidates) | method | Return ``(engine_key, summary)`` pairs for chain generation. |
| [`gym_rows`](#lazyorchestratorapp-gym_rows) | method | Return one row per gym definition with its active-run count. |
| [`gym_preview`](#lazyorchestratorapp-gym_preview) | method | Return a bounded YAML preview for one gym definition. |
| [`start_gym`](#lazyorchestratorapp-start_gym) | method | Start one gym and repaint the table. |
| [`stop_gym`](#lazyorchestratorapp-stop_gym) | method | Stop one gym (or every gym when selector is empty) and repaint. |
| [`toggle_gym`](#lazyorchestratorapp-toggle_gym) | method | Start the selected gym, or stop its active runs when already active. |
| [`profile_rows`](#lazyorchestratorapp-profile_rows) | method | Return one row per orchestrator profile with the active marker. |
| [`activate_profile`](#lazyorchestratorapp-activate_profile) | method | Persist one profile as active and repaint the profile table. |
| [`chain_rows`](#lazyorchestratorapp-chain_rows) | method | Return one row per chain file, including disabled ones. |
| [`chain_steps_preview`](#lazyorchestratorapp-chain_steps_preview) | method | Return the resolved step lines of a chain for the detail pane. |
| [`toggle_chain`](#lazyorchestratorapp-toggle_chain) | method | Flip a chain's enabled flag in its YAML file. |
| [`generate_chain`](#lazyorchestratorapp-generate_chain) | method | Generate chains/apt_<slug>.yaml from a playbook engine key. |
| [`remove_chain`](#lazyorchestratorapp-remove_chain) | method | Delete a chain file unless others extend it or it is the base. |
| [`on_data_table_row_highlighted`](#lazyorchestratorapp-on_data_table_row_highlighted) | method | Refresh the detail pane when the cursor moves. |
| [`save_config`](#lazyorchestratorapp-save_config) | method | Merge the given keys into the payload and persist it. |
| [`add_model_member`](#lazyorchestratorapp-add_model_member) | method | Append one LLM chain member; returns the stored name. |
| [`remove_model_member`](#lazyorchestratorapp-remove_model_member) | method | Drop one LLM chain member by name. |
| [`set_model_priority`](#lazyorchestratorapp-set_model_priority) | method | Change one LLM member's failover rank and repaint the table. |
| [`add_guard_rule`](#lazyorchestratorapp-add_guard_rule) | method | Register one guard intercept rule. |
| [`remove_guard_rule`](#lazyorchestratorapp-remove_guard_rule) | method | Delete one guard rule by exact pattern. |
| [`on_button_pressed`](#lazyorchestratorapp-on_button_pressed) | method | Handle the config save button. |
| [`action_refresh`](#lazyorchestratorapp-action_refresh) | method | Reload tables and form from disk. |
| [`action_toggle_item`](#lazyorchestratorapp-action_toggle_item) | method | Toggle the selected stage, auto verb, or chain. |
| [`action_save_config`](#lazyorchestratorapp-action_save_config) | method | Save the form values (keyboard shortcut). |
| [`action_add_item`](#lazyorchestratorapp-action_add_item) | method | Open the add modal for the active tab. |
| [`action_edit_item`](#lazyorchestratorapp-action_edit_item) | method | Edit the selected playbook YAML or LLM member priority. |
| [`action_delete_item`](#lazyorchestratorapp-action_delete_item) | method | Delete the selected row in the active tab. |

<a id="lazyorchestratorapp-__init__"></a>

#### `LazyOrchestratorApp.__init__`

`constructor` | [cli/lazy_orchestrator.py:200](../../cli/lazy_orchestrator.py#L200)

```python
def __init__(self, payload_path: str | Path | None = None, task_id: str = '') -> None
```

Bind the console to a payload file and an optional task.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload_path` | `str \| Path \| None` | `None` |  |
| `task_id` | `str` | `''` |  |

*Called by:* [`run_orchestrator_console`](#run_orchestrator_console)

<a id="lazyorchestratorapp-compose"></a>

#### `LazyOrchestratorApp.compose`

`method` `generator` | [cli/lazy_orchestrator.py:212](../../cli/lazy_orchestrator.py#L212)

```python
def compose(self) -> ComposeResult
```

Build the four panes.

**Returns:** `ComposeResult`

<a id="lazyorchestratorapp-on_mount"></a>

#### `LazyOrchestratorApp.on_mount`

`method` | [cli/lazy_orchestrator.py:253](../../cli/lazy_orchestrator.py#L253)

```python
def on_mount(self) -> None
```

Load the payload into the form and refresh the data tables.

<a id="lazyorchestratorapp-toggle_stage"></a>

#### `LazyOrchestratorApp.toggle_stage`

`method` | [cli/lazy_orchestrator.py:267](../../cli/lazy_orchestrator.py#L267)

```python
def toggle_stage(self, name: str) -> bool
```

Flip one pipeline stage on/off and persist it.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`set_stage`](modules.orchestrator_config.py.md#set_stage), [`stage_enabled`](modules.orchestrator_config.py.md#stage_enabled)

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](#lazyorchestratorapp-action_toggle_item)

<a id="lazyorchestratorapp-toggle_verb"></a>

#### `LazyOrchestratorApp.toggle_verb`

`method` | [cli/lazy_orchestrator.py:276](../../cli/lazy_orchestrator.py#L276)

```python
def toggle_verb(self, name: str) -> bool
```

Flip one auto verb on/off and persist it.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`upsert_verb`](modules.orchestrator_config.py.md#upsert_verb), [`verb_enabled`](modules.orchestrator_config.py.md#verb_enabled)

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](#lazyorchestratorapp-action_toggle_item)

<a id="lazyorchestratorapp-add_auto_verb"></a>

#### `LazyOrchestratorApp.add_auto_verb`

`method` | [cli/lazy_orchestrator.py:285](../../cli/lazy_orchestrator.py#L285)

```python
def add_auto_verb(self, name: str, keywords: str = '', needs_target: str = 'true', description: str = '', phases: str = '') -> dict
```

Register a new operator-defined auto verb.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `keywords` | `str` | `''` |  |
| `needs_target` | `str` | `'true'` |  |
| `description` | `str` | `''` |  |
| `phases` | `str` | `''` |  |

**Returns:** `dict`

*Calls:* [`upsert_verb`](modules.orchestrator_config.py.md#upsert_verb)

*Called by:* [`LazyOrchestratorApp.action_add_item`](#lazyorchestratorapp-action_add_item)

<a id="lazyorchestratorapp-remove_auto_verb"></a>

#### `LazyOrchestratorApp.remove_auto_verb`

`method` | [cli/lazy_orchestrator.py:308](../../cli/lazy_orchestrator.py#L308)

```python
def remove_auto_verb(self, name: str) -> bool
```

Delete a custom verb, or disable a built-in one.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`remove_verb`](modules.orchestrator_config.py.md#remove_verb)

*Called by:* [`LazyOrchestratorApp.action_delete_item`](#lazyorchestratorapp-action_delete_item)

<a id="lazyorchestratorapp-playbook_rows"></a>

#### `LazyOrchestratorApp.playbook_rows`

`method` | [cli/lazy_orchestrator.py:324](../../cli/lazy_orchestrator.py#L324)

```python
def playbook_rows(self) -> list[dict]
```

Return one row per playbook file, including invalid ones.

**Returns:** `list[dict]`

*Calls:* [`scan_playbooks`](modules.playbook_admin.py.md#scan_playbooks)

*Called by:* [`LazyOrchestratorApp.playbook_preview`](#lazyorchestratorapp-playbook_preview)

<a id="lazyorchestratorapp-playbook_preview"></a>

#### `LazyOrchestratorApp.playbook_preview`

`method` | [cli/lazy_orchestrator.py:348](../../cli/lazy_orchestrator.py#L348)

```python
def playbook_preview(self, filename: str, limit: int = 18) -> str
```

Return a bounded YAML preview for one playbook file.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |
| `limit` | `int` | `18` |  |

**Returns:** `str`

*Calls:* [`LazyOrchestratorApp.playbook_rows`](#lazyorchestratorapp-playbook_rows), [`preview_playbook`](modules.playbook_admin.py.md#preview_playbook)

<a id="lazyorchestratorapp-create_playbook_file"></a>

#### `LazyOrchestratorApp.create_playbook_file`

`method` | [cli/lazy_orchestrator.py:357](../../cli/lazy_orchestrator.py#L357)

```python
def create_playbook_file(self, filename: str, name: str = '', description: str = '', platforms: str = 'linux') -> str
```

Create one playbook YAML and repaint the table.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |
| `name` | `str` | `''` |  |
| `description` | `str` | `''` |  |
| `platforms` | `str` | `'linux'` |  |

**Returns:** `str`

*Calls:* [`create_playbook`](modules.playbook_admin.py.md#create_playbook)

*Called by:* [`LazyOrchestratorApp.action_add_item`](#lazyorchestratorapp-action_add_item)

<a id="lazyorchestratorapp-save_playbook_text"></a>

#### `LazyOrchestratorApp.save_playbook_text`

`method` | [cli/lazy_orchestrator.py:378](../../cli/lazy_orchestrator.py#L378)

```python
def save_playbook_text(self, filename: str, text: str) -> bool
```

Validate and persist raw YAML edited by the operator.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |
| `text` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`save_playbook_yaml`](modules.playbook_admin.py.md#save_playbook_yaml)

<a id="lazyorchestratorapp-delete_playbook_file"></a>

#### `LazyOrchestratorApp.delete_playbook_file`

`method` | [cli/lazy_orchestrator.py:390](../../cli/lazy_orchestrator.py#L390)

```python
def delete_playbook_file(self, filename: str) -> bool
```

Delete one playbook YAML after the operator confirms.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`delete_playbook`](modules.playbook_admin.py.md#delete_playbook)

*Called by:* [`LazyOrchestratorApp.action_delete_item`](#lazyorchestratorapp-action_delete_item)

<a id="lazyorchestratorapp-playbook_candidates"></a>

#### `LazyOrchestratorApp.playbook_candidates`

`method` | [cli/lazy_orchestrator.py:398](../../cli/lazy_orchestrator.py#L398)

```python
def playbook_candidates(self) -> list[tuple[str, str]]
```

Return ``(engine_key, summary)`` pairs for chain generation.

**Returns:** `list[tuple[str, str]]`

*Calls:* [`AptPlaybookEngine.__init__`](modules.apt_playbooks.py.md#aptplaybookengine-__init__), [`AptPlaybookEngine.list_playbooks`](modules.apt_playbooks.py.md#aptplaybookengine-list_playbooks)

*Called by:* [`LazyOrchestratorApp.action_add_item`](#lazyorchestratorapp-action_add_item)

<a id="lazyorchestratorapp-gym_rows"></a>

#### `LazyOrchestratorApp.gym_rows`

`method` | [cli/lazy_orchestrator.py:481](../../cli/lazy_orchestrator.py#L481)

```python
def gym_rows(self) -> list[dict]
```

Return one row per gym definition with its active-run count.

**Returns:** `list[dict]`

*Calls:* [`scan_definitions`](modules.gym_registry.py.md#scan_definitions), [`get_active_challenges`](modules.redteam_gym.py.md#get_active_challenges)

*Called by:* [`LazyOrchestratorApp.toggle_gym`](#lazyorchestratorapp-toggle_gym)

<a id="lazyorchestratorapp-gym_preview"></a>

#### `LazyOrchestratorApp.gym_preview`

`method` | [cli/lazy_orchestrator.py:518](../../cli/lazy_orchestrator.py#L518)

```python
def gym_preview(self, gym_id: str, limit: int = 16) -> str
```

Return a bounded YAML preview for one gym definition.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `gym_id` | `str` |  |  |
| `limit` | `int` | `16` |  |

**Returns:** `str`

*Calls:* [`definition_path`](modules.gym_registry.py.md#definition_path)

<a id="lazyorchestratorapp-start_gym"></a>

#### `LazyOrchestratorApp.start_gym`

`method` | [cli/lazy_orchestrator.py:586](../../cli/lazy_orchestrator.py#L586)

```python
def start_gym(self, gym_id: str, target: str = '') -> dict
```

Start one gym and repaint the table.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `gym_id` | `str` |  |  |
| `target` | `str` | `''` |  |

**Returns:** `dict`

*Calls:* [`start_challenge`](modules.redteam_gym.py.md#start_challenge)

*Called by:* [`LazyOrchestratorApp.toggle_gym`](#lazyorchestratorapp-toggle_gym)

<a id="lazyorchestratorapp-stop_gym"></a>

#### `LazyOrchestratorApp.stop_gym`

`method` | [cli/lazy_orchestrator.py:594](../../cli/lazy_orchestrator.py#L594)

```python
def stop_gym(self, selector: str = '') -> dict
```

Stop one gym (or every gym when selector is empty) and repaint.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `selector` | `str` | `''` |  |

**Returns:** `dict`

*Calls:* [`stop_challenges`](modules.redteam_gym.py.md#stop_challenges)

*Called by:* [`LazyOrchestratorApp.toggle_gym`](#lazyorchestratorapp-toggle_gym)

<a id="lazyorchestratorapp-toggle_gym"></a>

#### `LazyOrchestratorApp.toggle_gym`

`method` | [cli/lazy_orchestrator.py:602](../../cli/lazy_orchestrator.py#L602)

```python
def toggle_gym(self, gym_id: str) -> dict
```

Start the selected gym, or stop its active runs when already active.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `gym_id` | `str` |  |  |

**Returns:** `dict`

*Calls:* [`LazyOrchestratorApp.gym_rows`](#lazyorchestratorapp-gym_rows), [`LazyOrchestratorApp.start_gym`](#lazyorchestratorapp-start_gym), [`LazyOrchestratorApp.stop_gym`](#lazyorchestratorapp-stop_gym)

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](#lazyorchestratorapp-action_toggle_item)

<a id="lazyorchestratorapp-profile_rows"></a>

#### `LazyOrchestratorApp.profile_rows`

`method` | [cli/lazy_orchestrator.py:644](../../cli/lazy_orchestrator.py#L644)

```python
def profile_rows(self) -> list[dict]
```

Return one row per orchestrator profile with the active marker.

**Returns:** `list[dict]`

<a id="lazyorchestratorapp-activate_profile"></a>

#### `LazyOrchestratorApp.activate_profile`

`method` | [cli/lazy_orchestrator.py:669](../../cli/lazy_orchestrator.py#L669)

```python
def activate_profile(self, name: str) -> bool
```

Persist one profile as active and repaint the profile table.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](#lazyorchestratorapp-action_toggle_item)

<a id="lazyorchestratorapp-chain_rows"></a>

#### `LazyOrchestratorApp.chain_rows`

`method` | [cli/lazy_orchestrator.py:729](../../cli/lazy_orchestrator.py#L729)

```python
def chain_rows(self) -> list[dict]
```

Return one row per chain file, including disabled ones.

**Returns:** `list[dict]`

*Calls:* [`scan_all`](modules.chain_registry.py.md#scan_all)

<a id="lazyorchestratorapp-chain_steps_preview"></a>

#### `LazyOrchestratorApp.chain_steps_preview`

`method` | [cli/lazy_orchestrator.py:738](../../cli/lazy_orchestrator.py#L738)

```python
def chain_steps_preview(self, name: str, limit: int = 10) -> str
```

Return the resolved step lines of a chain for the detail pane.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `limit` | `int` | `10` |  |

**Returns:** `str`

*Calls:* [`get`](cli.palette.py.md#get)

<a id="lazyorchestratorapp-toggle_chain"></a>

#### `LazyOrchestratorApp.toggle_chain`

`method` | [cli/lazy_orchestrator.py:755](../../cli/lazy_orchestrator.py#L755)

```python
def toggle_chain(self, name: str) -> bool
```

Flip a chain's enabled flag in its YAML file.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`scan_all`](modules.chain_registry.py.md#scan_all), [`set_enabled`](modules.chain_registry.py.md#set_enabled)

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](#lazyorchestratorapp-action_toggle_item)

<a id="lazyorchestratorapp-generate_chain"></a>

#### `LazyOrchestratorApp.generate_chain`

`method` | [cli/lazy_orchestrator.py:766](../../cli/lazy_orchestrator.py#L766)

```python
def generate_chain(self, playbook_key: str) -> str
```

Generate chains/apt_<slug>.yaml from a playbook engine key.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `playbook_key` | `str` |  |  |

**Returns:** `str`

*Calls:* [`AptPlaybookEngine.__init__`](modules.apt_playbooks.py.md#aptplaybookengine-__init__), [`AptPlaybookEngine.get`](modules.apt_playbooks.py.md#aptplaybookengine-get), [`generate_for_playbook`](modules.chain_registry.py.md#generate_for_playbook)

*Called by:* [`LazyOrchestratorApp.action_add_item`](#lazyorchestratorapp-action_add_item)

<a id="lazyorchestratorapp-remove_chain"></a>

#### `LazyOrchestratorApp.remove_chain`

`method` | [cli/lazy_orchestrator.py:780](../../cli/lazy_orchestrator.py#L780)

```python
def remove_chain(self, name: str) -> bool
```

Delete a chain file unless others extend it or it is the base.

Returns False (refusing loudly) for the base ``apt_chain`` and
for any parent with children — edit or disable those instead.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`scan_all`](modules.chain_registry.py.md#scan_all)

*Called by:* [`LazyOrchestratorApp.action_delete_item`](#lazyorchestratorapp-action_delete_item)

<a id="lazyorchestratorapp-on_data_table_row_highlighted"></a>

#### `LazyOrchestratorApp.on_data_table_row_highlighted`

`method` | [cli/lazy_orchestrator.py:836](../../cli/lazy_orchestrator.py#L836)

```python
def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None
```

Refresh the detail pane when the cursor moves.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `DataTable.RowHighlighted` |  |  |

<a id="lazyorchestratorapp-save_config"></a>

#### `LazyOrchestratorApp.save_config`

`method` | [cli/lazy_orchestrator.py:917](../../cli/lazy_orchestrator.py#L917)

```python
def save_config(self, values: dict) -> dict
```

Merge the given keys into the payload and persist it.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `values` | `dict` |  | Mapping of payload keys to new values (strings). |

**Returns:** `dict` - The updated payload mapping.

*Calls:* [`save_payload`](core.config.py.md#save_payload)

*Called by:* [`LazyOrchestratorApp.action_save_config`](#lazyorchestratorapp-action_save_config), [`LazyOrchestratorApp.on_button_pressed`](#lazyorchestratorapp-on_button_pressed)

<a id="lazyorchestratorapp-add_model_member"></a>

#### `LazyOrchestratorApp.add_model_member`

`method` | [cli/lazy_orchestrator.py:939](../../cli/lazy_orchestrator.py#L939)

```python
def add_model_member(self, name: str, model: str, priority: str = '0') -> str
```

Append one LLM chain member; returns the stored name.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `model` | `str` |  |  |
| `priority` | `str` | `'0'` |  |

**Returns:** `str`

*Calls:* [`LlmPool.__init__`](modules.lazy_loop.py.md#llmpool-__init__), [`LlmPool.add_member`](modules.lazy_loop.py.md#llmpool-add_member)

*Called by:* [`LazyOrchestratorApp.action_add_item`](#lazyorchestratorapp-action_add_item)

<a id="lazyorchestratorapp-remove_model_member"></a>

#### `LazyOrchestratorApp.remove_model_member`

`method` | [cli/lazy_orchestrator.py:947](../../cli/lazy_orchestrator.py#L947)

```python
def remove_model_member(self, name: str) -> bool
```

Drop one LLM chain member by name.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`LlmPool.__init__`](modules.lazy_loop.py.md#llmpool-__init__), [`LlmPool.remove_member`](modules.lazy_loop.py.md#llmpool-remove_member)

*Called by:* [`LazyOrchestratorApp.action_delete_item`](#lazyorchestratorapp-action_delete_item)

<a id="lazyorchestratorapp-set_model_priority"></a>

#### `LazyOrchestratorApp.set_model_priority`

`method` | [cli/lazy_orchestrator.py:955](../../cli/lazy_orchestrator.py#L955)

```python
def set_model_priority(self, name: str, priority: str = '0') -> bool
```

Change one LLM member's failover rank and repaint the table.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `priority` | `str` | `'0'` |  |

**Returns:** `bool`

*Calls:* [`LlmPool.__init__`](modules.lazy_loop.py.md#llmpool-__init__), [`LlmPool.set_priority`](modules.lazy_loop.py.md#llmpool-set_priority)

*Called by:* [`LazyOrchestratorApp.action_edit_item`](#lazyorchestratorapp-action_edit_item)

<a id="lazyorchestratorapp-add_guard_rule"></a>

#### `LazyOrchestratorApp.add_guard_rule`

`method` | [cli/lazy_orchestrator.py:967](../../cli/lazy_orchestrator.py#L967)

```python
def add_guard_rule(self, pattern: str, action: str = 'ask', reason: str = '') -> bool
```

Register one guard intercept rule.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pattern` | `str` |  |  |
| `action` | `str` | `'ask'` |  |
| `reason` | `str` | `''` |  |

**Returns:** `bool`

*Calls:* [`Guard.__init__`](modules.lazy_loop.py.md#guard-__init__), [`Guard.add_rule`](modules.lazy_loop.py.md#guard-add_rule)

*Called by:* [`LazyOrchestratorApp.action_add_item`](#lazyorchestratorapp-action_add_item)

<a id="lazyorchestratorapp-remove_guard_rule"></a>

#### `LazyOrchestratorApp.remove_guard_rule`

`method` | [cli/lazy_orchestrator.py:975](../../cli/lazy_orchestrator.py#L975)

```python
def remove_guard_rule(self, pattern: str) -> bool
```

Delete one guard rule by exact pattern.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pattern` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`Guard.__init__`](modules.lazy_loop.py.md#guard-__init__), [`Guard.remove_rule`](modules.lazy_loop.py.md#guard-remove_rule)

*Called by:* [`LazyOrchestratorApp.action_delete_item`](#lazyorchestratorapp-action_delete_item)

<a id="lazyorchestratorapp-on_button_pressed"></a>

#### `LazyOrchestratorApp.on_button_pressed`

`method` | [cli/lazy_orchestrator.py:1079](../../cli/lazy_orchestrator.py#L1079)

```python
def on_button_pressed(self, event: Button.Pressed) -> None
```

Handle the config save button.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `Button.Pressed` |  |  |

*Calls:* [`LazyOrchestratorApp.save_config`](#lazyorchestratorapp-save_config)

<a id="lazyorchestratorapp-action_refresh"></a>

#### `LazyOrchestratorApp.action_refresh`

`method` | [cli/lazy_orchestrator.py:1097](../../cli/lazy_orchestrator.py#L1097)

```python
def action_refresh(self) -> None
```

Reload tables and form from disk.

<a id="lazyorchestratorapp-action_toggle_item"></a>

#### `LazyOrchestratorApp.action_toggle_item`

`method` | [cli/lazy_orchestrator.py:1118](../../cli/lazy_orchestrator.py#L1118)

```python
def action_toggle_item(self) -> None
```

Toggle the selected stage, auto verb, or chain.

*Calls:* [`LazyOrchestratorApp.activate_profile`](#lazyorchestratorapp-activate_profile), [`LazyOrchestratorApp.toggle_chain`](#lazyorchestratorapp-toggle_chain), [`LazyOrchestratorApp.toggle_gym`](#lazyorchestratorapp-toggle_gym), [`LazyOrchestratorApp.toggle_stage`](#lazyorchestratorapp-toggle_stage), [`LazyOrchestratorApp.toggle_verb`](#lazyorchestratorapp-toggle_verb)

<a id="lazyorchestratorapp-action_save_config"></a>

#### `LazyOrchestratorApp.action_save_config`

`method` | [cli/lazy_orchestrator.py:1142](../../cli/lazy_orchestrator.py#L1142)

```python
def action_save_config(self) -> None
```

Save the form values (keyboard shortcut).

*Calls:* [`LazyOrchestratorApp.save_config`](#lazyorchestratorapp-save_config)

<a id="lazyorchestratorapp-action_add_item"></a>

#### `LazyOrchestratorApp.action_add_item`

`method` | [cli/lazy_orchestrator.py:1159](../../cli/lazy_orchestrator.py#L1159)

```python
def action_add_item(self) -> None
```

Open the add modal for the active tab.

*Calls:* [`LazyOrchestratorApp.add_auto_verb`](#lazyorchestratorapp-add_auto_verb), [`LazyOrchestratorApp.add_guard_rule`](#lazyorchestratorapp-add_guard_rule), [`LazyOrchestratorApp.add_model_member`](#lazyorchestratorapp-add_model_member), [`LazyOrchestratorApp.create_playbook_file`](#lazyorchestratorapp-create_playbook_file), [`LazyOrchestratorApp.generate_chain`](#lazyorchestratorapp-generate_chain), [`LazyOrchestratorApp.playbook_candidates`](#lazyorchestratorapp-playbook_candidates), [`FormModal.__init__`](cli.tui_forms.py.md#formmodal-__init__), [`SearchSelectModal.__init__`](cli.tui_forms.py.md#searchselectmodal-__init__), [`create_gym`](modules.redteam_gym.py.md#create_gym)

<a id="lazyorchestratorapp-action_edit_item"></a>

#### `LazyOrchestratorApp.action_edit_item`

`method` | [cli/lazy_orchestrator.py:1332](../../cli/lazy_orchestrator.py#L1332)

```python
def action_edit_item(self) -> None
```

Edit the selected playbook YAML or LLM member priority.

*Calls:* [`LazyOrchestratorApp.set_model_priority`](#lazyorchestratorapp-set_model_priority), [`FormModal.__init__`](cli.tui_forms.py.md#formmodal-__init__), [`LlmPool.__init__`](modules.lazy_loop.py.md#llmpool-__init__), [`LlmPool.members`](modules.lazy_loop.py.md#llmpool-members)

<a id="lazyorchestratorapp-action_delete_item"></a>

#### `LazyOrchestratorApp.action_delete_item`

`method` | [cli/lazy_orchestrator.py:1377](../../cli/lazy_orchestrator.py#L1377)

```python
def action_delete_item(self) -> None
```

Delete the selected row in the active tab.

*Calls:* [`LazyOrchestratorApp.delete_playbook_file`](#lazyorchestratorapp-delete_playbook_file), [`LazyOrchestratorApp.remove_auto_verb`](#lazyorchestratorapp-remove_auto_verb), [`LazyOrchestratorApp.remove_chain`](#lazyorchestratorapp-remove_chain), [`LazyOrchestratorApp.remove_guard_rule`](#lazyorchestratorapp-remove_guard_rule), [`LazyOrchestratorApp.remove_model_member`](#lazyorchestratorapp-remove_model_member), [`ConfirmModal.__init__`](cli.tui_forms.py.md#confirmmodal-__init__), [`delete_gym`](modules.redteam_gym.py.md#delete_gym)

---

## Functions

<a id="run_orchestrator_console"></a>

### `run_orchestrator_console`

`function` | [cli/lazy_orchestrator.py:1456](../../cli/lazy_orchestrator.py#L1456)

```python
def run_orchestrator_console(task_id: str = '') -> None
```

Launch the admin console (attach mode).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` | `''` |  |

*Calls:* [`LazyOrchestratorApp.__init__`](#lazyorchestratorapp-__init__)

*Called by:* [`LazyQueueCommandSet.do_lazy_orchestrator`](cli.commands.lazyloop.py.md#lazyqueuecommandset-do_lazy_orchestrator)

---
