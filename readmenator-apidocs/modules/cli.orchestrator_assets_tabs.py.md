# `cli.orchestrator_assets_tabs`

> Source: [cli/orchestrator_assets_tabs.py:1](../../cli/orchestrator_assets_tabs.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Asset administration tabs for the orchestrator console.

Mixin holding the tab controllers that edit YAML-run assets: Playbooks,
Gyms, Chains and Profiles. Split out of ``cli/lazy_orchestrator.py`` to
keep the Textual app module under the size ceiling while per-tab state
and persistence helpers stay single-responsibility here.

## Contents

- **Classes:** [`ConfigField`](#configfield), [`OrchestratorAssetsMixin`](#orchestratorassetsmixin)
- **Functions:** [`parse_sleeper_windows`](#parse_sleeper_windows), [`format_sleeper_windows`](#format_sleeper_windows), [`parse_edr_pause_ranges`](#parse_edr_pause_ranges), [`format_edr_pause_ranges`](#format_edr_pause_ranges)
- **Constants:** [`CONFIG_FIELDS`](#config_fields), [`PACING_FIELDS`](#pacing_fields)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class ConfigField
    ConfigField : str key
    ConfigField : str label
    ConfigField : str placeholder
    ConfigField : str kind
    class OrchestratorAssetsMixin
    OrchestratorAssetsMixin : playbook_rows()
    OrchestratorAssetsMixin : playbook_preview()
    OrchestratorAssetsMixin : create_playbook_file()
    OrchestratorAssetsMixin : save_playbook_text()
    OrchestratorAssetsMixin : delete_playbook_file()
    OrchestratorAssetsMixin : playbook_candidates()
    OrchestratorAssetsMixin : gym_rows()
    OrchestratorAssetsMixin : gym_preview()
    OrchestratorAssetsMixin : start_gym()
    OrchestratorAssetsMixin : stop_gym()
    OrchestratorAssetsMixin : toggle_gym()
    OrchestratorAssetsMixin : profile_rows()
    OrchestratorAssetsMixin : activate_profile()
    OrchestratorAssetsMixin : bof_rows()
    OrchestratorAssetsMixin : bof_preview()
    OrchestratorAssetsMixin : create_bof_file()
    OrchestratorAssetsMixin : save_bof_text()
    OrchestratorAssetsMixin : delete_bof_file()
    OrchestratorAssetsMixin : stage_bof_file()
    OrchestratorAssetsMixin : chain_rows()
    OrchestratorAssetsMixin : chain_steps_preview()
    OrchestratorAssetsMixin : toggle_chain()
    OrchestratorAssetsMixin : generate_chain()
    OrchestratorAssetsMixin : remove_chain()
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_preview(["OrchestratorAssetsMixin.playbook_preview"])
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_rows(["OrchestratorAssetsMixin.playbook_rows"])
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_toggle_gym(["OrchestratorAssetsMixin.toggle_gym"])
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_gym_rows(["OrchestratorAssetsMixin.gym_rows"])
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_start_gym(["OrchestratorAssetsMixin.start_gym"])
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_stop_gym(["OrchestratorAssetsMixin.stop_gym"])
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_bof_preview(["OrchestratorAssetsMixin.bof_preview"])
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_bof_rows(["OrchestratorAssetsMixin.bof_rows"])
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_save_pacing(["OrchestratorAssetsMixin.save_pacing"])
    n_cli_orchestrator_assets_tabs_py__parse_edr_pause_ranges(["parse_edr_pause_ranges"])
    n_cli_orchestrator_assets_tabs_py__parse_sleeper_windows(["parse_sleeper_windows"])
    n_modules_playbook_admin_py__scan_playbooks["playbook_admin.scan_playbooks"]
    n_modules_playbook_admin_py__preview_playbook["playbook_admin.preview_playbook"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_create_playbook_file(["OrchestratorAssetsMixin.create_playbook_file"])
    n_modules_playbook_admin_py__create_playbook["playbook_admin.create_playbook"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_save_playbook_text(["OrchestratorAssetsMixin.save_playbook_text"])
    n_modules_playbook_admin_py__save_playbook_yaml["playbook_admin.save_playbook_yaml"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_delete_playbook_file(["OrchestratorAssetsMixin.delete_playbook_file"])
    n_modules_playbook_admin_py__delete_playbook["playbook_admin.delete_playbook"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_candidates(["OrchestratorAssetsMixin.playbook_candidates"])
    n_modules_apt_playbooks_py__AptPlaybookEngine___init__["apt_playbooks.AptPlaybookEngine.__init__"]
    n_modules_apt_playbooks_py__AptPlaybookEngine_list_playbooks["apt_playbooks.AptPlaybookEngine.list_playbooks"]
    n_modules_gym_registry_py__scan_definitions["gym_registry.scan_definitions"]
    n_modules_redteam_gym_py__get_active_challenges["redteam_gym.get_active_challenges"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_gym_preview(["OrchestratorAssetsMixin.gym_preview"])
    n_modules_gym_registry_py__definition_path["gym_registry.definition_path"]
    n_modules_redteam_gym_py__start_challenge["redteam_gym.start_challenge"]
    n_modules_redteam_gym_py__stop_challenges["redteam_gym.stop_challenges"]
    n_modules_bof_admin_py__scan_bofs["bof_admin.scan_bofs"]
    n_modules_bof_admin_py__preview_bof["bof_admin.preview_bof"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_create_bof_file(["OrchestratorAssetsMixin.create_bof_file"])
    n_modules_bof_admin_py__create_bof["bof_admin.create_bof"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_save_bof_text(["OrchestratorAssetsMixin.save_bof_text"])
    n_modules_bof_admin_py__save_bof_yaml["bof_admin.save_bof_yaml"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_delete_bof_file(["OrchestratorAssetsMixin.delete_bof_file"])
    n_modules_bof_admin_py__delete_bof["bof_admin.delete_bof"]
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_preview --> n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_rows
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_toggle_gym --> n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_gym_rows
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_toggle_gym --> n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_start_gym
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_toggle_gym --> n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_stop_gym
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_bof_preview --> n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_bof_rows
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_save_pacing --> n_cli_orchestrator_assets_tabs_py__parse_edr_pause_ranges
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_save_pacing --> n_cli_orchestrator_assets_tabs_py__parse_sleeper_windows
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_rows -.-> n_modules_playbook_admin_py__scan_playbooks
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_preview -.-> n_modules_playbook_admin_py__preview_playbook
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_create_playbook_file -.-> n_modules_playbook_admin_py__create_playbook
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_save_playbook_text -.-> n_modules_playbook_admin_py__save_playbook_yaml
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_delete_playbook_file -.-> n_modules_playbook_admin_py__delete_playbook
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_candidates -.-> n_modules_apt_playbooks_py__AptPlaybookEngine___init__
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_playbook_candidates -.-> n_modules_apt_playbooks_py__AptPlaybookEngine_list_playbooks
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_gym_rows -.-> n_modules_gym_registry_py__scan_definitions
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_gym_rows -.-> n_modules_redteam_gym_py__get_active_challenges
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_gym_preview -.-> n_modules_gym_registry_py__definition_path
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_start_gym -.-> n_modules_redteam_gym_py__start_challenge
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_stop_gym -.-> n_modules_redteam_gym_py__stop_challenges
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_bof_rows -.-> n_modules_bof_admin_py__scan_bofs
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_bof_preview -.-> n_modules_bof_admin_py__preview_bof
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_create_bof_file -.-> n_modules_bof_admin_py__create_bof
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_save_bof_text -.-> n_modules_bof_admin_py__save_bof_yaml
    n_cli_orchestrator_assets_tabs_py__OrchestratorAssetsMixin_delete_bof_file -.-> n_modules_bof_admin_py__delete_bof
```

## Classes

<a id="configfield"></a>

### `ConfigField`

`class` `dataclass` | [cli/orchestrator_assets_tabs.py:21](../../cli/orchestrator_assets_tabs.py#L21)

Decorators: `@dataclass(frozen=True)`

```python
class ConfigField
```

One editable payload knob.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`key`](#configfield-key) | `str` |  |  |
| [`label`](#configfield-label) | `str` |  |  |
| [`placeholder`](#configfield-placeholder) | `str` | `''` |  |
| [`kind`](#configfield-kind) | `str` | `'text'` |  |

---

<a id="orchestratorassetsmixin"></a>

### `OrchestratorAssetsMixin`

`class` | [cli/orchestrator_assets_tabs.py:206](../../cli/orchestrator_assets_tabs.py#L206)

```python
class OrchestratorAssetsMixin
```

Subclasses: [`LazyOrchestratorApp`](cli.lazy_orchestrator.py.md#lazyorchestratorapp)

Tab controllers for Playbooks, Gyms, Chains and Profiles tabs.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`playbook_rows`](#orchestratorassetsmixin-playbook_rows) | method | Return one row per playbook file, including invalid ones. |
| [`playbook_preview`](#orchestratorassetsmixin-playbook_preview) | method | Return a bounded YAML preview for one playbook file. |
| [`create_playbook_file`](#orchestratorassetsmixin-create_playbook_file) | method | Create one playbook YAML and repaint the table. |
| [`save_playbook_text`](#orchestratorassetsmixin-save_playbook_text) | method | Validate and persist raw YAML edited by the operator. |
| [`delete_playbook_file`](#orchestratorassetsmixin-delete_playbook_file) | method | Delete one playbook YAML after the operator confirms. |
| [`playbook_candidates`](#orchestratorassetsmixin-playbook_candidates) | method | Return ``(engine_key, summary)`` pairs for chain generation. |
| [`gym_rows`](#orchestratorassetsmixin-gym_rows) | method | Return one row per gym definition with its active-run count. |
| [`gym_preview`](#orchestratorassetsmixin-gym_preview) | method | Return a bounded YAML preview for one gym definition. |
| [`start_gym`](#orchestratorassetsmixin-start_gym) | method | Start one gym and repaint the table. |
| [`stop_gym`](#orchestratorassetsmixin-stop_gym) | method | Stop one gym (or every gym when selector is empty) and repaint. |
| [`toggle_gym`](#orchestratorassetsmixin-toggle_gym) | method | Start the selected gym, or stop its active runs when already active. |
| [`profile_rows`](#orchestratorassetsmixin-profile_rows) | method | Return one row per orchestrator profile with the active marker. |
| [`activate_profile`](#orchestratorassetsmixin-activate_profile) | method | Persist one profile as active and repaint the profile table. |
| [`bof_rows`](#orchestratorassetsmixin-bof_rows) | method | Return one row per BOF YAML configuration file, invalid ones included. |
| [`bof_preview`](#orchestratorassetsmixin-bof_preview) | method | Return a bounded YAML preview for one BOF file. |
| [`create_bof_file`](#orchestratorassetsmixin-create_bof_file) | method | Create one BOF YAML and repaint the table. |
| [`save_bof_text`](#orchestratorassetsmixin-save_bof_text) | method | Validate and persist raw YAML edited by the operator. |
| [`delete_bof_file`](#orchestratorassetsmixin-delete_bof_file) | method | Delete one BOF YAML after the operator confirms. |
| [`stage_bof_file`](#orchestratorassetsmixin-stage_bof_file) | method | Stage the compiled artifact of one BOF for beacon delivery. |
| [`chain_rows`](#orchestratorassetsmixin-chain_rows) | method | Return one row per chain file, including disabled ones. |
| [`chain_steps_preview`](#orchestratorassetsmixin-chain_steps_preview) | method | Return the resolved step lines of a chain for the detail pane. |
| [`toggle_chain`](#orchestratorassetsmixin-toggle_chain) | method | Flip a chain's enabled flag in its YAML file. |
| [`generate_chain`](#orchestratorassetsmixin-generate_chain) | method | Generate chains/apt_<slug>.yaml from a playbook engine key. |
| [`remove_chain`](#orchestratorassetsmixin-remove_chain) | method | Delete a chain file unless others extend it or it is the base. |
| [`on_data_table_row_highlighted`](#orchestratorassetsmixin-on_data_table_row_highlighted) | method | Refresh the detail pane when the cursor moves. |
| [`seed_triggers_from_yaml`](#orchestratorassetsmixin-seed_triggers_from_yaml) | method | Seed triggers from config/orchestrator.yaml into the store. |
| [`toggle_trigger`](#orchestratorassetsmixin-toggle_trigger) | method | Flip one trigger's enabled flag in the store. |
| [`remove_trigger`](#orchestratorassetsmixin-remove_trigger) | method | Delete one trigger from the store. |
| [`add_trigger`](#orchestratorassetsmixin-add_trigger) | method | Add a scheduler trigger entered from the picker form. |
| [`trigger_kind_options`](#orchestratorassetsmixin-trigger_kind_options) | method | Return selectable trigger kinds for the add form. |
| [`save_pacing`](#orchestratorassetsmixin-save_pacing) | method | Validate and persist the Pacing tab fields through set_pacing. |
| [`save_config`](#orchestratorassetsmixin-save_config) | method | Merge the given keys into the payload and persist it. |
| [`add_model_member`](#orchestratorassetsmixin-add_model_member) | method | Append one LLM chain member; returns the stored name. |
| [`remove_model_member`](#orchestratorassetsmixin-remove_model_member) | method | Drop one LLM chain member by name. |
| [`set_model_priority`](#orchestratorassetsmixin-set_model_priority) | method | Change one LLM member's failover rank and repaint the table. |
| [`set_harness`](#orchestratorassetsmixin-set_harness) | method | Toggle the deterministic harness from the orchestrator UI. |
| [`add_guard_rule`](#orchestratorassetsmixin-add_guard_rule) | method | Register one guard intercept rule. |
| [`remove_guard_rule`](#orchestratorassetsmixin-remove_guard_rule) | method | Delete one guard rule by exact pattern. |
| [`save_guardrails`](#orchestratorassetsmixin-save_guardrails) | method | Merge harness settings into payload and reconfigure the harness. |
| [`warm_restart_harness`](#orchestratorassetsmixin-warm_restart_harness) | method | Run the harness warm restart and repaint the table. |
| [`rearm_harness`](#orchestratorassetsmixin-rearm_harness) | method | Re-arm suspended features and clear advisories. |

<a id="orchestratorassetsmixin-playbook_rows"></a>

#### `OrchestratorAssetsMixin.playbook_rows`

`method` | [cli/orchestrator_assets_tabs.py:217](../../cli/orchestrator_assets_tabs.py#L217)

```python
def playbook_rows(self) -> list[dict]
```

Return one row per playbook file, including invalid ones.

**Returns:** `list[dict]`

*Calls:* [`scan_playbooks`](modules.playbook_admin.py.md#scan_playbooks)

*Called by:* [`OrchestratorAssetsMixin.playbook_preview`](#orchestratorassetsmixin-playbook_preview)

<a id="orchestratorassetsmixin-playbook_preview"></a>

#### `OrchestratorAssetsMixin.playbook_preview`

`method` | [cli/orchestrator_assets_tabs.py:241](../../cli/orchestrator_assets_tabs.py#L241)

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

*Calls:* [`OrchestratorAssetsMixin.playbook_rows`](#orchestratorassetsmixin-playbook_rows), [`preview_playbook`](modules.playbook_admin.py.md#preview_playbook)

<a id="orchestratorassetsmixin-create_playbook_file"></a>

#### `OrchestratorAssetsMixin.create_playbook_file`

`method` | [cli/orchestrator_assets_tabs.py:250](../../cli/orchestrator_assets_tabs.py#L250)

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

*Called by:* [`LazyOrchestratorApp.action_add_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_add_item)

<a id="orchestratorassetsmixin-save_playbook_text"></a>

#### `OrchestratorAssetsMixin.save_playbook_text`

`method` | [cli/orchestrator_assets_tabs.py:271](../../cli/orchestrator_assets_tabs.py#L271)

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

<a id="orchestratorassetsmixin-delete_playbook_file"></a>

#### `OrchestratorAssetsMixin.delete_playbook_file`

`method` | [cli/orchestrator_assets_tabs.py:283](../../cli/orchestrator_assets_tabs.py#L283)

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

*Called by:* [`LazyOrchestratorApp.action_delete_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_delete_item)

<a id="orchestratorassetsmixin-playbook_candidates"></a>

#### `OrchestratorAssetsMixin.playbook_candidates`

`method` | [cli/orchestrator_assets_tabs.py:291](../../cli/orchestrator_assets_tabs.py#L291)

```python
def playbook_candidates(self) -> list[tuple[str, str]]
```

Return ``(engine_key, summary)`` pairs for chain generation.

**Returns:** `list[tuple[str, str]]`

*Calls:* [`AptPlaybookEngine.__init__`](modules.apt_playbooks.py.md#aptplaybookengine-__init__), [`AptPlaybookEngine.list_playbooks`](modules.apt_playbooks.py.md#aptplaybookengine-list_playbooks)

*Called by:* [`LazyOrchestratorApp.action_add_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_add_item)

<a id="orchestratorassetsmixin-gym_rows"></a>

#### `OrchestratorAssetsMixin.gym_rows`

`method` | [cli/orchestrator_assets_tabs.py:374](../../cli/orchestrator_assets_tabs.py#L374)

```python
def gym_rows(self) -> list[dict]
```

Return one row per gym definition with its active-run count.

**Returns:** `list[dict]`

*Calls:* [`scan_definitions`](modules.gym_registry.py.md#scan_definitions), [`get_active_challenges`](modules.redteam_gym.py.md#get_active_challenges)

*Called by:* [`OrchestratorAssetsMixin.toggle_gym`](#orchestratorassetsmixin-toggle_gym)

<a id="orchestratorassetsmixin-gym_preview"></a>

#### `OrchestratorAssetsMixin.gym_preview`

`method` | [cli/orchestrator_assets_tabs.py:411](../../cli/orchestrator_assets_tabs.py#L411)

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

<a id="orchestratorassetsmixin-start_gym"></a>

#### `OrchestratorAssetsMixin.start_gym`

`method` | [cli/orchestrator_assets_tabs.py:479](../../cli/orchestrator_assets_tabs.py#L479)

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

*Called by:* [`OrchestratorAssetsMixin.toggle_gym`](#orchestratorassetsmixin-toggle_gym)

<a id="orchestratorassetsmixin-stop_gym"></a>

#### `OrchestratorAssetsMixin.stop_gym`

`method` | [cli/orchestrator_assets_tabs.py:487](../../cli/orchestrator_assets_tabs.py#L487)

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

*Called by:* [`OrchestratorAssetsMixin.toggle_gym`](#orchestratorassetsmixin-toggle_gym)

<a id="orchestratorassetsmixin-toggle_gym"></a>

#### `OrchestratorAssetsMixin.toggle_gym`

`method` | [cli/orchestrator_assets_tabs.py:495](../../cli/orchestrator_assets_tabs.py#L495)

```python
def toggle_gym(self, gym_id: str) -> dict
```

Start the selected gym, or stop its active runs when already active.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `gym_id` | `str` |  |  |

**Returns:** `dict`

*Calls:* [`OrchestratorAssetsMixin.gym_rows`](#orchestratorassetsmixin-gym_rows), [`OrchestratorAssetsMixin.start_gym`](#orchestratorassetsmixin-start_gym), [`OrchestratorAssetsMixin.stop_gym`](#orchestratorassetsmixin-stop_gym)

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_toggle_item)

<a id="orchestratorassetsmixin-profile_rows"></a>

#### `OrchestratorAssetsMixin.profile_rows`

`method` | [cli/orchestrator_assets_tabs.py:537](../../cli/orchestrator_assets_tabs.py#L537)

```python
def profile_rows(self) -> list[dict]
```

Return one row per orchestrator profile with the active marker.

**Returns:** `list[dict]`

<a id="orchestratorassetsmixin-activate_profile"></a>

#### `OrchestratorAssetsMixin.activate_profile`

`method` | [cli/orchestrator_assets_tabs.py:562](../../cli/orchestrator_assets_tabs.py#L562)

```python
def activate_profile(self, name: str) -> bool
```

Persist one profile as active and repaint the profile table.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_toggle_item)

<a id="orchestratorassetsmixin-bof_rows"></a>

#### `OrchestratorAssetsMixin.bof_rows`

`method` | [cli/orchestrator_assets_tabs.py:630](../../cli/orchestrator_assets_tabs.py#L630)

```python
def bof_rows(self) -> list[dict]
```

Return one row per BOF YAML configuration file, invalid ones included.

**Returns:** `list[dict]`

*Calls:* [`scan_bofs`](modules.bof_admin.py.md#scan_bofs)

*Called by:* [`OrchestratorAssetsMixin.bof_preview`](#orchestratorassetsmixin-bof_preview)

<a id="orchestratorassetsmixin-bof_preview"></a>

#### `OrchestratorAssetsMixin.bof_preview`

`method` | [cli/orchestrator_assets_tabs.py:654](../../cli/orchestrator_assets_tabs.py#L654)

```python
def bof_preview(self, filename: str, limit: int = 18) -> str
```

Return a bounded YAML preview for one BOF file.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |
| `limit` | `int` | `18` |  |

**Returns:** `str`

*Calls:* [`OrchestratorAssetsMixin.bof_rows`](#orchestratorassetsmixin-bof_rows), [`preview_bof`](modules.bof_admin.py.md#preview_bof)

<a id="orchestratorassetsmixin-create_bof_file"></a>

#### `OrchestratorAssetsMixin.create_bof_file`

`method` | [cli/orchestrator_assets_tabs.py:663](../../cli/orchestrator_assets_tabs.py#L663)

```python
def create_bof_file(self, filename: str, name: str = '', description: str = '', client: str = 'blacksandbeacon') -> str
```

Create one BOF YAML and repaint the table.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |
| `name` | `str` | `''` |  |
| `description` | `str` | `''` |  |
| `client` | `str` | `'blacksandbeacon'` |  |

**Returns:** `str`

*Calls:* [`create_bof`](modules.bof_admin.py.md#create_bof)

*Called by:* [`LazyOrchestratorApp.action_add_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_add_item)

<a id="orchestratorassetsmixin-save_bof_text"></a>

#### `OrchestratorAssetsMixin.save_bof_text`

`method` | [cli/orchestrator_assets_tabs.py:683](../../cli/orchestrator_assets_tabs.py#L683)

```python
def save_bof_text(self, filename: str, text: str) -> bool
```

Validate and persist raw YAML edited by the operator.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |
| `text` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`save_bof_yaml`](modules.bof_admin.py.md#save_bof_yaml)

<a id="orchestratorassetsmixin-delete_bof_file"></a>

#### `OrchestratorAssetsMixin.delete_bof_file`

`method` | [cli/orchestrator_assets_tabs.py:695](../../cli/orchestrator_assets_tabs.py#L695)

```python
def delete_bof_file(self, filename: str) -> bool
```

Delete one BOF YAML after the operator confirms.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`delete_bof`](modules.bof_admin.py.md#delete_bof)

*Called by:* [`LazyOrchestratorApp.action_delete_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_delete_item)

<a id="orchestratorassetsmixin-stage_bof_file"></a>

#### `OrchestratorAssetsMixin.stage_bof_file`

`method` | [cli/orchestrator_assets_tabs.py:703](../../cli/orchestrator_assets_tabs.py#L703)

```python
def stage_bof_file(self, filename: str) -> bool
```

Stage the compiled artifact of one BOF for beacon delivery.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`stage_bof`](modules.bof_delivery.py.md#stage_bof)

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_toggle_item)

<a id="orchestratorassetsmixin-chain_rows"></a>

#### `OrchestratorAssetsMixin.chain_rows`

`method` | [cli/orchestrator_assets_tabs.py:789](../../cli/orchestrator_assets_tabs.py#L789)

```python
def chain_rows(self) -> list[dict]
```

Return one row per chain file, including disabled ones.

**Returns:** `list[dict]`

*Calls:* [`scan_all`](modules.chain_registry.py.md#scan_all)

<a id="orchestratorassetsmixin-chain_steps_preview"></a>

#### `OrchestratorAssetsMixin.chain_steps_preview`

`method` | [cli/orchestrator_assets_tabs.py:798](../../cli/orchestrator_assets_tabs.py#L798)

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

*Calls:* [`AptPlaybookEngine.get`](modules.apt_playbooks.py.md#aptplaybookengine-get)

<a id="orchestratorassetsmixin-toggle_chain"></a>

#### `OrchestratorAssetsMixin.toggle_chain`

`method` | [cli/orchestrator_assets_tabs.py:815](../../cli/orchestrator_assets_tabs.py#L815)

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

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_toggle_item)

<a id="orchestratorassetsmixin-generate_chain"></a>

#### `OrchestratorAssetsMixin.generate_chain`

`method` | [cli/orchestrator_assets_tabs.py:826](../../cli/orchestrator_assets_tabs.py#L826)

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

*Called by:* [`LazyOrchestratorApp.action_add_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_add_item)

<a id="orchestratorassetsmixin-remove_chain"></a>

#### `OrchestratorAssetsMixin.remove_chain`

`method` | [cli/orchestrator_assets_tabs.py:840](../../cli/orchestrator_assets_tabs.py#L840)

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

*Called by:* [`LazyOrchestratorApp.action_delete_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_delete_item)

<a id="orchestratorassetsmixin-on_data_table_row_highlighted"></a>

#### `OrchestratorAssetsMixin.on_data_table_row_highlighted`

`method` | [cli/orchestrator_assets_tabs.py:896](../../cli/orchestrator_assets_tabs.py#L896)

```python
def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None
```

Refresh the detail pane when the cursor moves.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `event` | `DataTable.RowHighlighted` |  |  |

<a id="orchestratorassetsmixin-seed_triggers_from_yaml"></a>

#### `OrchestratorAssetsMixin.seed_triggers_from_yaml`

`method` | [cli/orchestrator_assets_tabs.py:939](../../cli/orchestrator_assets_tabs.py#L939)

```python
def seed_triggers_from_yaml(self) -> dict
```

Seed triggers from config/orchestrator.yaml into the store.

**Returns:** `dict`

*Calls:* [`TriggerStore.__init__`](modules.loop_triggers.py.md#triggerstore-__init__), [`read_policy`](modules.trigger_policy.py.md#read_policy), [`seed_store`](modules.trigger_policy.py.md#seed_store)

*Called by:* [`LazyOrchestratorApp.action_seed_triggers`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_seed_triggers)

<a id="orchestratorassetsmixin-toggle_trigger"></a>

#### `OrchestratorAssetsMixin.toggle_trigger`

`method` | [cli/orchestrator_assets_tabs.py:969](../../cli/orchestrator_assets_tabs.py#L969)

```python
def toggle_trigger(self, trigger_id: int) -> bool
```

Flip one trigger's enabled flag in the store.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `trigger_id` | `int` |  |  |

**Returns:** `bool`

*Calls:* [`TriggerStore.__init__`](modules.loop_triggers.py.md#triggerstore-__init__), [`TriggerStore.set_enabled`](modules.loop_triggers.py.md#triggerstore-set_enabled), [`export_store`](modules.trigger_policy.py.md#export_store)

*Called by:* [`LazyOrchestratorApp.action_toggle_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_toggle_item)

<a id="orchestratorassetsmixin-remove_trigger"></a>

#### `OrchestratorAssetsMixin.remove_trigger`

`method` | [cli/orchestrator_assets_tabs.py:979](../../cli/orchestrator_assets_tabs.py#L979)

```python
def remove_trigger(self, trigger_id: int) -> bool
```

Delete one trigger from the store.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `trigger_id` | `int` |  |  |

**Returns:** `bool`

*Calls:* [`TriggerStore.__init__`](modules.loop_triggers.py.md#triggerstore-__init__), [`TriggerStore.remove`](modules.loop_triggers.py.md#triggerstore-remove)

*Called by:* [`LazyOrchestratorApp.action_delete_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_delete_item)

<a id="orchestratorassetsmixin-add_trigger"></a>

#### `OrchestratorAssetsMixin.add_trigger`

`method` | [cli/orchestrator_assets_tabs.py:987](../../cli/orchestrator_assets_tabs.py#L987)

```python
def add_trigger(self, kind: str, every_sec: str = '', arg: str = '') -> dict
```

Add a scheduler trigger entered from the picker form.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `kind` | `str` |  |  |
| `every_sec` | `str` | `''` |  |
| `arg` | `str` | `''` |  |

**Returns:** `dict`

*Calls:* [`TriggerStore.__init__`](modules.loop_triggers.py.md#triggerstore-__init__), [`TriggerStore.add`](modules.loop_triggers.py.md#triggerstore-add)

*Called by:* [`LazyOrchestratorApp.action_add_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_add_item)

<a id="orchestratorassetsmixin-trigger_kind_options"></a>

#### `OrchestratorAssetsMixin.trigger_kind_options`

`method` | [cli/orchestrator_assets_tabs.py:999](../../cli/orchestrator_assets_tabs.py#L999)

```python
def trigger_kind_options(self) -> list[tuple[str, str]]
```

Return selectable trigger kinds for the add form.

**Returns:** `list[tuple[str, str]]`

*Called by:* [`LazyOrchestratorApp.action_add_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_add_item)

<a id="orchestratorassetsmixin-save_pacing"></a>

#### `OrchestratorAssetsMixin.save_pacing`

`method` | [cli/orchestrator_assets_tabs.py:1089](../../cli/orchestrator_assets_tabs.py#L1089)

```python
def save_pacing(self, values: dict) -> dict
```

Validate and persist the Pacing tab fields through set_pacing.

Every knob is routed through
[`modules.orchestrator_config.set_pacing`](modules.orchestrator_config.py.md#set_pacing) so the payload,
the active profile view and the loop's EdrPacer stay consistent.
Malformed sleeper windows or pause ranges are rejected and
reported rather than silently coerced.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `values` | `dict` |  | Mapping of dotted pacing keys to raw operator strings. |

**Returns:** `dict` - A summary mapping with `[`saved`](cli.wizard.py.md#wizardresult-saved)` (count) and ``errors`` (list).

*Calls:* [`parse_edr_pause_ranges`](#parse_edr_pause_ranges), [`parse_sleeper_windows`](#parse_sleeper_windows), [`set_pacing`](modules.orchestrator_config.py.md#set_pacing)

<a id="orchestratorassetsmixin-save_config"></a>

#### `OrchestratorAssetsMixin.save_config`

`method` | [cli/orchestrator_assets_tabs.py:1134](../../cli/orchestrator_assets_tabs.py#L1134)

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

*Called by:* [`LazyOrchestratorApp.action_save_config`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_save_config)

<a id="orchestratorassetsmixin-add_model_member"></a>

#### `OrchestratorAssetsMixin.add_model_member`

`method` | [cli/orchestrator_assets_tabs.py:1156](../../cli/orchestrator_assets_tabs.py#L1156)

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

*Called by:* [`LazyOrchestratorApp.action_add_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_add_item)

<a id="orchestratorassetsmixin-remove_model_member"></a>

#### `OrchestratorAssetsMixin.remove_model_member`

`method` | [cli/orchestrator_assets_tabs.py:1164](../../cli/orchestrator_assets_tabs.py#L1164)

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

*Called by:* [`LazyOrchestratorApp.action_delete_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_delete_item)

<a id="orchestratorassetsmixin-set_model_priority"></a>

#### `OrchestratorAssetsMixin.set_model_priority`

`method` | [cli/orchestrator_assets_tabs.py:1172](../../cli/orchestrator_assets_tabs.py#L1172)

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

*Called by:* [`LazyOrchestratorApp.action_edit_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_edit_item)

<a id="orchestratorassetsmixin-set_harness"></a>

#### `OrchestratorAssetsMixin.set_harness`

`method` | [cli/orchestrator_assets_tabs.py:1184](../../cli/orchestrator_assets_tabs.py#L1184)

```python
def set_harness(self, enabled: bool) -> dict
```

Toggle the deterministic harness from the orchestrator UI.

Wired through `modules.orchestrator_config.set_harness`
so payload.json, the active profile and the loop gates stay in
sync.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `enabled` | `bool` |  | True engages the harness, False disables it. |

**Returns:** `dict` - The ``{"harness", "profile", "chain"}`` summary or an error
form with ``{"error": "..."}`` when persistence fails.

<a id="orchestratorassetsmixin-add_guard_rule"></a>

#### `OrchestratorAssetsMixin.add_guard_rule`

`method` | [cli/orchestrator_assets_tabs.py:1209](../../cli/orchestrator_assets_tabs.py#L1209)

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

*Calls:* [`Guard.add_rule`](modules.lazy_loop.py.md#guard-add_rule)

*Called by:* [`LazyOrchestratorApp.action_add_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_add_item)

<a id="orchestratorassetsmixin-remove_guard_rule"></a>

#### `OrchestratorAssetsMixin.remove_guard_rule`

`method` | [cli/orchestrator_assets_tabs.py:1217](../../cli/orchestrator_assets_tabs.py#L1217)

```python
def remove_guard_rule(self, pattern: str) -> bool
```

Delete one guard rule by exact pattern.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pattern` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`Guard.remove_rule`](modules.lazy_loop.py.md#guard-remove_rule)

*Called by:* [`LazyOrchestratorApp.action_delete_item`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-action_delete_item)

<a id="orchestratorassetsmixin-save_guardrails"></a>

#### `OrchestratorAssetsMixin.save_guardrails`

`method` | [cli/orchestrator_assets_tabs.py:1268](../../cli/orchestrator_assets_tabs.py#L1268)

```python
def save_guardrails(self, values: dict) -> dict
```

Merge harness settings into payload and reconfigure the harness.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `values` | `dict` |  | Mapping with optional ``saturation`` and per-tier ``cap_core``/``cap_mission``/``cap_support`` strings. |

**Returns:** `dict` - The persisted guardrails section.

*Calls:* [`save_payload`](core.config.py.md#save_payload), [`global_harness`](modules.guardrails.harness.py.md#global_harness)

<a id="orchestratorassetsmixin-warm_restart_harness"></a>

#### `OrchestratorAssetsMixin.warm_restart_harness`

`method` | [cli/orchestrator_assets_tabs.py:1314](../../cli/orchestrator_assets_tabs.py#L1314)

```python
def warm_restart_harness(self) -> dict
```

Run the harness warm restart and repaint the table.

**Returns:** `dict`

*Calls:* [`global_harness`](modules.guardrails.harness.py.md#global_harness)

*Called by:* [`LazyOrchestratorApp.on_button_pressed`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-on_button_pressed)

<a id="orchestratorassetsmixin-rearm_harness"></a>

#### `OrchestratorAssetsMixin.rearm_harness`

`method` | [cli/orchestrator_assets_tabs.py:1326](../../cli/orchestrator_assets_tabs.py#L1326)

```python
def rearm_harness(self) -> dict
```

Re-arm suspended features and clear advisories.

**Returns:** `dict`

*Calls:* [`global_harness`](modules.guardrails.harness.py.md#global_harness)

*Called by:* [`LazyOrchestratorApp.on_button_pressed`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-on_button_pressed)

---

## Functions

<a id="parse_sleeper_windows"></a>

### `parse_sleeper_windows`

`function` | [cli/orchestrator_assets_tabs.py:92](../../cli/orchestrator_assets_tabs.py#L92)

```python
def parse_sleeper_windows(raw: str) -> tuple[list[str], list[str]]
```

Parse a comma-separated sleeper-window string.

Each window must match ``HH:MM-HH:MM`` (validated against
`modules.orchestrator_config.SLEEPER_WINDOW_RE`). The parser is
lenient on surrounding whitespace and empty entries.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `raw` | `str` |  | Operator text such as ``"22:00-06:00, 12:00-13:00"``. |

**Returns:** `tuple[list[str], list[str]]` - A ``(valid, invalid)`` pair: the accepted windows and the tokens
that failed validation.

*Called by:* [`OrchestratorAssetsMixin.save_pacing`](#orchestratorassetsmixin-save_pacing)

---

<a id="format_sleeper_windows"></a>

### `format_sleeper_windows`

`function` | [cli/orchestrator_assets_tabs.py:121](../../cli/orchestrator_assets_tabs.py#L121)

```python
def format_sleeper_windows(value: object) -> str
```

Render stored sleeper windows as an editable comma-separated string.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `object` |  |  |

**Returns:** `str`

---

<a id="parse_edr_pause_ranges"></a>

### `parse_edr_pause_ranges`

`function` | [cli/orchestrator_assets_tabs.py:128](../../cli/orchestrator_assets_tabs.py#L128)

```python
def parse_edr_pause_ranges(raw: str) -> tuple[dict[int, list[float]], list[str]]
```

Parse ``level:low-high`` pause ranges from a compact string.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `raw` | `str` |  | Operator text such as ``"1:2-5,2:5-15"``. |

**Returns:** `tuple[dict[int, list[float]], list[str]]` - A ``(ranges, invalid)`` pair where `[`ranges`](modules.lazy_feedmatch.py.md#feedentry-ranges)` maps a defense level
to a ``[low, high]`` pair with ``0 <= low <= high`` and ``invalid``
holds the tokens that failed to parse.

*Called by:* [`OrchestratorAssetsMixin.save_pacing`](#orchestratorassetsmixin-save_pacing)

---

<a id="format_edr_pause_ranges"></a>

### `format_edr_pause_ranges`

`function` | [cli/orchestrator_assets_tabs.py:161](../../cli/orchestrator_assets_tabs.py#L161)

```python
def format_edr_pause_ranges(value: object) -> str
```

Render stored EDR pause ranges as an editable compact string.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `object` |  |  |

**Returns:** `str`

---

## Constants

<a id="config_fields"></a>

### `CONFIG_FIELDS`

`constant` | [cli/orchestrator_assets_tabs.py:30](../../cli/orchestrator_assets_tabs.py#L30)

```python
CONFIG_FIELDS
```

---

<a id="pacing_fields"></a>

### `PACING_FIELDS`

`constant` | [cli/orchestrator_assets_tabs.py:54](../../cli/orchestrator_assets_tabs.py#L54)

```python
PACING_FIELDS
```

---
