# `cli.lazy_orchestrator`

> Source: [cli/lazy_orchestrator.py:1](../../cli/lazy_orchestrator.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Orchestrator admin console for the autonomous loop.

A Textual TUI in the spirit of the marketplace configurator:

- Now: what the loop is executing right now (task, stages, live activity
  tail, per-worker current command);
- Config: every payload knob the runner reads (rounds, workers,
  heartbeat, verb timeout, agentic flags, NOA, proxy);
- Models: the LLM failover chain (add/remove members);
- Guard: the intercept rules (add/remove).

Edits persist straight to ``payload.json`` (or a sandbox path in tests)
through `[`core.config`](core.config.py.md)`; nothing else mutates global state.

## Contents

- **Classes:** [`FormModal`](#formmodal), [`LazyOrchestratorApp`](#lazyorchestratorapp)
- **Functions:** [`run_orchestrator_console`](#run_orchestrator_console)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class FormModal
    FormModal : BINDINGS
    FormModal : __init__()
    FormModal : compose()
    FormModal : on_button_pressed()
    FormModal : on_input_submitted()
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
    LazyOrchestratorApp : save_config()
    LazyOrchestratorApp : add_model_member()
    LazyOrchestratorApp : remove_model_member()
    LazyOrchestratorApp : add_guard_rule()
    LazyOrchestratorApp : remove_guard_rule()
    LazyOrchestratorApp : on_button_pressed()
    LazyOrchestratorApp : action_refresh()
    LazyOrchestratorApp : action_toggle_item()
    LazyOrchestratorApp : action_save_config()
    LazyOrchestratorApp : action_add_item()
    LazyOrchestratorApp : action_delete_item()
    class App
    App <|-- LazyOrchestratorApp
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_on_button_pressed(["LazyOrchestratorApp.on_button_pressed"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_save_config(["LazyOrchestratorApp.save_config"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item(["LazyOrchestratorApp.action_toggle_item"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_stage(["LazyOrchestratorApp.toggle_stage"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_verb(["LazyOrchestratorApp.toggle_verb"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_save_config(["LazyOrchestratorApp.action_save_config"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item(["LazyOrchestratorApp.action_add_item"])
    n_cli_lazy_orchestrator_py__FormModal___init__(["FormModal.__init__"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_auto_verb(["LazyOrchestratorApp.add_auto_verb"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_guard_rule(["LazyOrchestratorApp.add_guard_rule"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_model_member(["LazyOrchestratorApp.add_model_member"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item(["LazyOrchestratorApp.action_delete_item"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_auto_verb(["LazyOrchestratorApp.remove_auto_verb"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_guard_rule(["LazyOrchestratorApp.remove_guard_rule"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_model_member(["LazyOrchestratorApp.remove_model_member"])
    n_cli_lazy_orchestrator_py__run_orchestrator_console(["run_orchestrator_console"])
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp___init__(["LazyOrchestratorApp.__init__"])
    n_modules_orchestrator_config_py__set_stage["orchestrator_config.set_stage"]
    n_modules_orchestrator_config_py__stage_enabled["orchestrator_config.stage_enabled"]
    n_modules_orchestrator_config_py__upsert_verb["orchestrator_config.upsert_verb"]
    n_modules_orchestrator_config_py__verb_enabled["orchestrator_config.verb_enabled"]
    n_modules_orchestrator_config_py__remove_verb["orchestrator_config.remove_verb"]
    n_core_config_py__save_payload["config.save_payload"]
    n_modules_lazy_loop_py__LlmPool___init__["lazy_loop.LlmPool.__init__"]
    n_modules_lazy_loop_py__LlmPool_add_member["lazy_loop.LlmPool.add_member"]
    n_modules_lazy_loop_py__LlmPool_remove_member["lazy_loop.LlmPool.remove_member"]
    n_modules_lazy_loop_py__Guard___init__["lazy_loop.Guard.__init__"]
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_on_button_pressed --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_save_config
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_stage
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_toggle_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_save_config --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_save_config
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__FormModal___init__
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_auto_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_guard_rule
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_add_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_model_member
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_auto_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_guard_rule
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_action_delete_item --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_model_member
    n_cli_lazy_orchestrator_py__run_orchestrator_console --> n_cli_lazy_orchestrator_py__LazyOrchestratorApp___init__
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_stage -.-> n_modules_orchestrator_config_py__set_stage
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_stage -.-> n_modules_orchestrator_config_py__stage_enabled
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_verb -.-> n_modules_orchestrator_config_py__upsert_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_toggle_verb -.-> n_modules_orchestrator_config_py__verb_enabled
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_auto_verb -.-> n_modules_orchestrator_config_py__upsert_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_auto_verb -.-> n_modules_orchestrator_config_py__remove_verb
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_save_config -.-> n_core_config_py__save_payload
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_model_member -.-> n_modules_lazy_loop_py__LlmPool___init__
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_model_member -.-> n_modules_lazy_loop_py__LlmPool_add_member
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_model_member -.-> n_modules_lazy_loop_py__LlmPool___init__
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_remove_model_member -.-> n_modules_lazy_loop_py__LlmPool_remove_member
    n_cli_lazy_orchestrator_py__LazyOrchestratorApp_add_guard_rule -.-> n_modules_lazy_loop_py__Guard___init__
```

## Classes

<a id="formmodal"></a>

### `FormModal`

`class` | [cli/lazy_orchestrator.py:81](../../cli/lazy_orchestrator.py#L81)

```python
class FormModal(ModalScreen[dict])
```

Bases: `ModalScreen[dict]`

Generic key/value modal used for models and guard rules.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`BINDINGS`](#formmodal-bindings) |  | `[('escape', 'dismiss(None)', 'cancel')]` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#formmodal-__init__) | constructor | Store the title and (id, label, placeholder) field specs. |
| [`compose`](#formmodal-compose) | method | One labeled input per field plus a save button. |
| [`on_button_pressed`](#formmodal-on_button_pressed) | method | Collect the values and close the modal. |
| [`on_input_submitted`](#formmodal-on_input_submitted) | method | Enter commits the form like the save button. |

<a id="formmodal-__init__"></a>

#### `FormModal.__init__`

`constructor` | [cli/lazy_orchestrator.py:86](../../cli/lazy_orchestrator.py#L86)

```python
def __init__(self, title: str, fields: list[tuple[str, str, str]]) -> None
```

Store the title and (id, label, placeholder) field specs.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `title` | `str` |  |  |
| `fields` | `list[tuple[str, str, str]]` |  |  |

*Called by:* [`LazyOrchestratorApp.action_add_item`](#lazyorchestratorapp-action_add_item)

<a id="formmodal-compose"></a>

#### `FormModal.compose`

`method` `generator` | [cli/lazy_orchestrator.py:92](../../cli/lazy_orchestrator.py#L92)

```python
def compose(self) -> ComposeResult
```

One labeled input per field plus a save button.

**Returns:** `ComposeResult`

<a id="formmodal-on_button_pressed"></a>

#### `FormModal.on_button_pressed`

`method` | [cli/lazy_orchestrator.py:101](../../cli/lazy_orchestrator.py#L101)

```python
def on_button_pressed(self, event: Button.Pressed) -> None
```

Collect the values and close the modal.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `Button.Pressed` |  |  |

<a id="formmodal-on_input_submitted"></a>

#### `FormModal.on_input_submitted`

`method` | [cli/lazy_orchestrator.py:110](../../cli/lazy_orchestrator.py#L110)

```python
def on_input_submitted(self, event: Input.Submitted) -> None
```

Enter commits the form like the save button.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `Input.Submitted` |  |  |

---

<a id="lazyorchestratorapp"></a>

### `LazyOrchestratorApp`

`class` | [cli/lazy_orchestrator.py:118](../../cli/lazy_orchestrator.py#L118)

```python
class LazyOrchestratorApp(App[None])
```

Bases: [`App[None]`](lazy_sentinel4.py.md#app)

Admin console: Now / Config / Models / Guard.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`CSS`](#lazyorchestratorapp-css) |  | `'\n #now-status { height: 6; border: round $accent; padding: 0 1; }\n #now-log { height: 1fr; border: round $primary; }\n #config-status { height: 3; color: $text-muted; }\n DataTable { height: 1fr; }\n .modal-box { width: 70; height: auto; padding: 1 2; background: $surface;\n border: round $accent; }\n .modal-title { text-style: bold; padding-bottom: 1; }\n .modal-label { padding-top: 1; }\n '` |  |
| [`BINDINGS`](#lazyorchestratorapp-bindings) |  | `[Binding('q', 'quit', 'Quit'), Binding('r', 'refresh', 'Refresh'), Binding('s', 'save_config', 'Save config'), Binding('space', 'toggle_item', 'Toggle'), Binding('a', 'add_item', 'Add'), Binding('d', 'delete_item', 'Delete')]` |  |

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
| [`save_config`](#lazyorchestratorapp-save_config) | method | Merge the given keys into the payload and persist it. |
| [`add_model_member`](#lazyorchestratorapp-add_model_member) | method | Append one LLM chain member; returns the stored name. |
| [`remove_model_member`](#lazyorchestratorapp-remove_model_member) | method | Drop one LLM chain member by name. |
| [`add_guard_rule`](#lazyorchestratorapp-add_guard_rule) | method | Register one guard intercept rule. |
| [`remove_guard_rule`](#lazyorchestratorapp-remove_guard_rule) | method | Delete one guard rule by exact pattern. |
| [`on_button_pressed`](#lazyorchestratorapp-on_button_pressed) | method | Handle the config save button. |
| [`action_refresh`](#lazyorchestratorapp-action_refresh) | method | Reload tables and form from disk. |
| [`action_toggle_item`](#lazyorchestratorapp-action_toggle_item) | method | Toggle the selected stage or auto verb. |
| [`action_save_config`](#lazyorchestratorapp-action_save_config) | method | Save the form values (keyboard shortcut). |
| [`action_add_item`](#lazyorchestratorapp-action_add_item) | method | Open the add modal for the active tab. |
| [`action_delete_item`](#lazyorchestratorapp-action_delete_item) | method | Delete the selected row in the active tab. |

<a id="lazyorchestratorapp-__init__"></a>

#### `LazyOrchestratorApp.__init__`

`constructor` | [cli/lazy_orchestrator.py:141](../../cli/lazy_orchestrator.py#L141)

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

`method` `generator` | [cli/lazy_orchestrator.py:151](../../cli/lazy_orchestrator.py#L151)

```python
def compose(self) -> ComposeResult
```

Build the four panes.

**Returns:** `ComposeResult`

<a id="lazyorchestratorapp-on_mount"></a>

#### `LazyOrchestratorApp.on_mount`

`method` | [cli/lazy_orchestrator.py:176](../../cli/lazy_orchestrator.py#L176)

```python
def on_mount(self) -> None
```

Load the payload into the form and refresh the data tables.

<a id="lazyorchestratorapp-toggle_stage"></a>

#### `LazyOrchestratorApp.toggle_stage`

`method` | [cli/lazy_orchestrator.py:186](../../cli/lazy_orchestrator.py#L186)

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

`method` | [cli/lazy_orchestrator.py:195](../../cli/lazy_orchestrator.py#L195)

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

`method` | [cli/lazy_orchestrator.py:204](../../cli/lazy_orchestrator.py#L204)

```python
def add_auto_verb(self, name: str, keywords: str = '', needs_target: str = 'true', description: str = '') -> dict
```

Register a new operator-defined auto verb.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `keywords` | `str` | `''` |  |
| `needs_target` | `str` | `'true'` |  |
| `description` | `str` | `''` |  |

**Returns:** `dict`

*Calls:* [`upsert_verb`](modules.orchestrator_config.py.md#upsert_verb)

*Called by:* [`LazyOrchestratorApp.action_add_item`](#lazyorchestratorapp-action_add_item)

<a id="lazyorchestratorapp-remove_auto_verb"></a>

#### `LazyOrchestratorApp.remove_auto_verb`

`method` | [cli/lazy_orchestrator.py:219](../../cli/lazy_orchestrator.py#L219)

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

<a id="lazyorchestratorapp-save_config"></a>

#### `LazyOrchestratorApp.save_config`

`method` | [cli/lazy_orchestrator.py:288](../../cli/lazy_orchestrator.py#L288)

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

`method` | [cli/lazy_orchestrator.py:310](../../cli/lazy_orchestrator.py#L310)

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

`method` | [cli/lazy_orchestrator.py:318](../../cli/lazy_orchestrator.py#L318)

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

<a id="lazyorchestratorapp-add_guard_rule"></a>

#### `LazyOrchestratorApp.add_guard_rule`

`method` | [cli/lazy_orchestrator.py:326](../../cli/lazy_orchestrator.py#L326)

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

`method` | [cli/lazy_orchestrator.py:334](../../cli/lazy_orchestrator.py#L334)

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

`method` | [cli/lazy_orchestrator.py:438](../../cli/lazy_orchestrator.py#L438)

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

`method` | [cli/lazy_orchestrator.py:456](../../cli/lazy_orchestrator.py#L456)

```python
def action_refresh(self) -> None
```

Reload tables and form from disk.

<a id="lazyorchestratorapp-action_toggle_item"></a>

#### `LazyOrchestratorApp.action_toggle_item`

`method` | [cli/lazy_orchestrator.py:473](../../cli/lazy_orchestrator.py#L473)

```python
def action_toggle_item(self) -> None
```

Toggle the selected stage or auto verb.

*Calls:* [`LazyOrchestratorApp.toggle_stage`](#lazyorchestratorapp-toggle_stage), [`LazyOrchestratorApp.toggle_verb`](#lazyorchestratorapp-toggle_verb)

<a id="lazyorchestratorapp-action_save_config"></a>

#### `LazyOrchestratorApp.action_save_config`

`method` | [cli/lazy_orchestrator.py:485](../../cli/lazy_orchestrator.py#L485)

```python
def action_save_config(self) -> None
```

Save the form values (keyboard shortcut).

*Calls:* [`LazyOrchestratorApp.save_config`](#lazyorchestratorapp-save_config)

<a id="lazyorchestratorapp-action_add_item"></a>

#### `LazyOrchestratorApp.action_add_item`

`method` | [cli/lazy_orchestrator.py:502](../../cli/lazy_orchestrator.py#L502)

```python
def action_add_item(self) -> None
```

Open the add modal for the active tab.

*Calls:* [`FormModal.__init__`](#formmodal-__init__), [`LazyOrchestratorApp.add_auto_verb`](#lazyorchestratorapp-add_auto_verb), [`LazyOrchestratorApp.add_guard_rule`](#lazyorchestratorapp-add_guard_rule), [`LazyOrchestratorApp.add_model_member`](#lazyorchestratorapp-add_model_member)

<a id="lazyorchestratorapp-action_delete_item"></a>

#### `LazyOrchestratorApp.action_delete_item`

`method` | [cli/lazy_orchestrator.py:563](../../cli/lazy_orchestrator.py#L563)

```python
def action_delete_item(self) -> None
```

Delete the selected row in the active tab.

*Calls:* [`LazyOrchestratorApp.remove_auto_verb`](#lazyorchestratorapp-remove_auto_verb), [`LazyOrchestratorApp.remove_guard_rule`](#lazyorchestratorapp-remove_guard_rule), [`LazyOrchestratorApp.remove_model_member`](#lazyorchestratorapp-remove_model_member)

---

## Functions

<a id="run_orchestrator_console"></a>

### `run_orchestrator_console`

`function` | [cli/lazy_orchestrator.py:605](../../cli/lazy_orchestrator.py#L605)

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
