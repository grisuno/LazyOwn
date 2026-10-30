# `modules.orchestrator_config`

> Source: [modules/orchestrator_config.py:1](../../modules/orchestrator_config.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Operator configuration for the loop core: profiles, stages and auto verbs.

YAML is the default source of truth. ``config/orchestrator.yaml`` declares
profiles, pipeline stages, numeric limits, budgets, default chain/playbook
and outcome sink toggles. ``payload.json`` keeps runtime overrides under
``orchestrator``; an override always wins over YAML.

The module exposes one merged view so the TUI, the runner and the engine
read the same values. A missing or invalid YAML never stops the loop: the
built-in fallback table keeps it running.

## Contents

- **Functions:** [`reload`](#reload), [`profiles`](#profiles), [`active_profile`](#active_profile), [`profile_config`](#profile_config), [`set_profile`](#set_profile), [`limits`](#limits), [`budget`](#budget), [`findings_config`](#findings_config), [`progress_config`](#progress_config), [`engagement_mode`](#engagement_mode), [`set_engagement_mode`](#set_engagement_mode), [`chain_defaults`](#chain_defaults), [`sinks`](#sinks), [`stages`](#stages), [`stage_enabled`](#stage_enabled), [`stage_params`](#stage_params), [`set_stage`](#set_stage), [`effective_verbs`](#effective_verbs), [`verb_config`](#verb_config), [`verb_enabled`](#verb_enabled), [`upsert_verb`](#upsert_verb), [`remove_verb`](#remove_verb), [`reset`](#reset), [`validate_config`](#validate_config)
- **Constants:** [`ORCHESTRATOR_YAML_PATH`](#orchestrator_yaml_path), [`STAGE_DEFS`](#stage_defs), [`FALLBACK_STAGES`](#fallback_stages), [`FALLBACK_LIMITS`](#fallback_limits), [`FALLBACK_BUDGET`](#fallback_budget), [`FALLBACK_FINDINGS`](#fallback_findings), [`FALLBACK_PROGRESS`](#fallback_progress), [`FALLBACK_MODE`](#fallback_mode), [`ENGAGEMENT_MODES`](#engagement_modes), [`FALLBACK_SINKS`](#fallback_sinks), [`DEFAULT_STAGES`](#default_stages)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_orchestrator_config_py__active_profile(["active_profile"])
    n_modules_orchestrator_config_py__profiles(["profiles"])
    n_modules_orchestrator_config_py__profile_config(["profile_config"])
    n_modules_orchestrator_config_py__set_profile(["set_profile"])
    n_modules_orchestrator_config_py__limits(["limits"])
    n_modules_orchestrator_config_py__budget(["budget"])
    n_modules_orchestrator_config_py__findings_config(["findings_config"])
    n_modules_orchestrator_config_py__progress_config(["progress_config"])
    n_modules_orchestrator_config_py__engagement_mode(["engagement_mode"])
    n_modules_orchestrator_config_py__chain_defaults(["chain_defaults"])
    n_modules_orchestrator_config_py__sinks(["sinks"])
    n_modules_orchestrator_config_py__stages(["stages"])
    n_modules_orchestrator_config_py__stage_enabled(["stage_enabled"])
    n_modules_orchestrator_config_py__stage_params(["stage_params"])
    n_modules_orchestrator_config_py__set_stage(["set_stage"])
    n_modules_orchestrator_config_py__verb_config(["verb_config"])
    n_modules_orchestrator_config_py__effective_verbs(["effective_verbs"])
    n_modules_orchestrator_config_py__verb_enabled(["verb_enabled"])
    n_modules_orchestrator_config_py__upsert_verb(["upsert_verb"])
    n_modules_orchestrator_config_py__remove_verb(["remove_verb"])
    n_modules_orchestrator_config_py__validate_config(["validate_config"])
    n_modules_trigger_policy_py__validate_triggers["trigger_policy.validate_triggers"]
    n_modules_orchestrator_config_py__active_profile --> n_modules_orchestrator_config_py__profiles
    n_modules_orchestrator_config_py__profile_config --> n_modules_orchestrator_config_py__active_profile
    n_modules_orchestrator_config_py__profile_config --> n_modules_orchestrator_config_py__profiles
    n_modules_orchestrator_config_py__set_profile --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__set_profile --> n_modules_orchestrator_config_py__profiles
    n_modules_orchestrator_config_py__limits --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__budget --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__findings_config --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__progress_config --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__engagement_mode --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__chain_defaults --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__sinks --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__stages --> n_modules_orchestrator_config_py__profile_config
    n_modules_orchestrator_config_py__stage_enabled --> n_modules_orchestrator_config_py__stages
    n_modules_orchestrator_config_py__stage_params --> n_modules_orchestrator_config_py__stages
    n_modules_orchestrator_config_py__set_stage --> n_modules_orchestrator_config_py__stages
    n_modules_orchestrator_config_py__verb_config --> n_modules_orchestrator_config_py__effective_verbs
    n_modules_orchestrator_config_py__verb_enabled --> n_modules_orchestrator_config_py__verb_config
    n_modules_orchestrator_config_py__upsert_verb --> n_modules_orchestrator_config_py__verb_config
    n_modules_orchestrator_config_py__remove_verb --> n_modules_orchestrator_config_py__upsert_verb
    n_modules_orchestrator_config_py__remove_verb --> n_modules_orchestrator_config_py__verb_config
    n_modules_orchestrator_config_py__validate_config -.-> n_modules_trigger_policy_py__validate_triggers
```

## Functions

<a id="reload"></a>

### `reload`

`function` | [modules/orchestrator_config.py:137](../../modules/orchestrator_config.py#L137)

```python
def reload() -> None
```

Invalidate every merged view after an external configuration change.

---

<a id="profiles"></a>

### `profiles`

`function` | [modules/orchestrator_config.py:256](../../modules/orchestrator_config.py#L256)

```python
def profiles() -> dict[str, dict]
```

Return every resolved profile, including inherited values.

**Returns:** `dict[str, dict]`

*Called by:* [`active_profile`](#active_profile), [`profile_config`](#profile_config), [`set_profile`](#set_profile)

---

<a id="active_profile"></a>

### `active_profile`

`function` | [modules/orchestrator_config.py:281](../../modules/orchestrator_config.py#L281)

```python
def active_profile() -> str
```

Return the profile selected by the payload, falling back safely.

**Returns:** `str`

*Calls:* [`profiles`](#profiles)

*Called by:* [`harness_enabled`](modules.harness.py.md#harness_enabled), [`profile_config`](#profile_config)

---

<a id="profile_config"></a>

### `profile_config`

`function` | [modules/orchestrator_config.py:293](../../modules/orchestrator_config.py#L293)

```python
def profile_config(name: str = '') -> dict
```

Return one resolved profile by name, or the active profile.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | `''` |  |

**Returns:** `dict`

*Calls:* [`active_profile`](#active_profile), [`profiles`](#profiles)

*Called by:* [`resolve_loop_defaults`](modules.lazy_runner.py.md#resolve_loop_defaults), [`budget`](#budget), [`chain_defaults`](#chain_defaults), [`engagement_mode`](#engagement_mode), [`findings_config`](#findings_config), [`limits`](#limits), [`progress_config`](#progress_config), [`set_profile`](#set_profile), [`sinks`](#sinks), [`stages`](#stages)

---

<a id="set_profile"></a>

### `set_profile`

`function` | [modules/orchestrator_config.py:300](../../modules/orchestrator_config.py#L300)

```python
def set_profile(name: str) -> dict
```

Persist the active profile name.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  | Profile declared in the YAML or the fallback table. |

**Returns:** `dict` - The resolved profile after persisting.

**Raises**

- `KeyError`: Unknown profile name.

*Calls:* [`profile_config`](#profile_config), [`profiles`](#profiles)

---

<a id="limits"></a>

### `limits`

`function` | [modules/orchestrator_config.py:356](../../modules/orchestrator_config.py#L356)

```python
def limits() -> dict
```

Return resolved numeric limits for the active profile.

**Returns:** `dict`

*Calls:* [`profile_config`](#profile_config)

---

<a id="budget"></a>

### `budget`

`function` | [modules/orchestrator_config.py:363](../../modules/orchestrator_config.py#L363)

```python
def budget() -> dict
```

Return resolved budgets for the active profile.

**Returns:** `dict`

*Calls:* [`profile_config`](#profile_config)

---

<a id="findings_config"></a>

### `findings_config`

`function` | [modules/orchestrator_config.py:370](../../modules/orchestrator_config.py#L370)

```python
def findings_config() -> dict[str, Any]
```

Return resolved findings-ledger settings for the active profile.

Merges precedence: module fallbacks < YAML profile ``findings`` <
payload ``orchestrator.findings``. Boolean fields coerce to bool so a
YAML string can never disable redaction by accident.

**Returns:** `dict[str, Any]` - Mapping with min evidence length, caps and the redaction toggle.

*Calls:* [`profile_config`](#profile_config)

*Called by:* [`LazyCommandSet.do_lazy_mode`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_mode), [`limits_for`](modules.sinks.findings.py.md#limits_for)

---

<a id="progress_config"></a>

### `progress_config`

`function` | [modules/orchestrator_config.py:392](../../modules/orchestrator_config.py#L392)

```python
def progress_config() -> dict[str, Any]
```

Return resolved goal-progress strikethreshold settings.

`[`max_strikes`](modules.progress_ledger.py.md#strikepolicy-max_strikes)` counts consecutive rounds without objective progress
(facts/findings/verdicts/goals); reaching it stops the loop with a
handoff instead of burning rounds. Exploit classes list the outcome
kinds that count as objective progress when they succeed.

**Returns:** `dict[str, Any]` - Mapping with max_strikes, handoff toggle and exploit classes.

*Calls:* [`profile_config`](#profile_config)

*Called by:* [`LazyCommandSet.do_lazy_mode`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_mode)

---

<a id="engagement_mode"></a>

### `engagement_mode`

`function` | [modules/orchestrator_config.py:419](../../modules/orchestrator_config.py#L419)

```python
def engagement_mode() -> str
```

Return the active engagement mode (pentest | redteam | ctf).

Precedence: payload ``orchestrator.mode`` < YAML profile ``mode`` <
module fallback. Unknown names fall back to the module default so a
typo can never switch the loop into unrestricted deep compromise.

**Returns:** `str` - One mode string from [`ENGAGEMENT_MODES`](#engagement_modes).

*Calls:* [`profile_config`](#profile_config)

*Called by:* [`LazyCommandSet.do_lazy_mode`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_mode)

---

<a id="set_engagement_mode"></a>

### `set_engagement_mode`

`function` | [modules/orchestrator_config.py:437](../../modules/orchestrator_config.py#L437)

```python
def set_engagement_mode(mode: str) -> str
```

Persist the engagement mode in the payload.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` |  | One of [`ENGAGEMENT_MODES`](#engagement_modes). |

**Returns:** `str` - The persisted mode string.

**Raises**

- `KeyError`: Unknown mode name.

*Called by:* [`LazyCommandSet.do_lazy_mode`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_mode)

---

<a id="chain_defaults"></a>

### `chain_defaults`

`function` | [modules/orchestrator_config.py:460](../../modules/orchestrator_config.py#L460)

```python
def chain_defaults() -> dict
```

Return the default chain and playbook for the active profile.

**Returns:** `dict`

*Calls:* [`profile_config`](#profile_config)

---

<a id="sinks"></a>

### `sinks`

`function` | [modules/orchestrator_config.py:469](../../modules/orchestrator_config.py#L469)

```python
def sinks() -> dict
```

Return outcome sink toggles for the active profile plus payload overrides.

**Returns:** `dict`

*Calls:* [`profile_config`](#profile_config)

---

<a id="stages"></a>

### `stages`

`function` | [modules/orchestrator_config.py:506](../../modules/orchestrator_config.py#L506)

```python
def stages() -> dict[str, dict]
```

Merged stage view: enabled flag, label, firing condition and params.

**Returns:** `dict[str, dict]`

*Calls:* [`profile_config`](#profile_config)

*Called by:* [`LazyCommandSet.do_lazy_stage`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_stage), [`stage_names`](lazyc2.blueprints.orchestrator.py.md#stage_names), [`set_stage`](#set_stage), [`stage_enabled`](#stage_enabled), [`stage_params`](#stage_params)

---

<a id="stage_enabled"></a>

### `stage_enabled`

`function` | [modules/orchestrator_config.py:536](../../modules/orchestrator_config.py#L536)

```python
def stage_enabled(name: str) -> bool
```

Return whether one pipeline stage is enabled (unknown = enabled).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`stages`](#stages)

*Called by:* [`LazyOrchestratorApp.toggle_stage`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-toggle_stage), [`stages_toggle`](lazyc2.blueprints.orchestrator.py.md#stages_toggle)

---

<a id="stage_params"></a>

### `stage_params`

`function` | [modules/orchestrator_config.py:542](../../modules/orchestrator_config.py#L542)

```python
def stage_params(name: str) -> dict
```

Return the resolved parameter mapping of one stage.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `dict`

*Calls:* [`stages`](#stages)

---

<a id="set_stage"></a>

### `set_stage`

`function` | [modules/orchestrator_config.py:547](../../modules/orchestrator_config.py#L547)

```python
def set_stage(name: str, enabled: bool) -> dict
```

Persist the enabled flag of one stage.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  | Stage identifier from the active profile. |
| `enabled` | `bool` |  | New flag. |

**Returns:** `dict` - The updated merged stage view for that stage.

**Raises**

- `KeyError`: Unknown stage name.

*Calls:* [`stages`](#stages)

*Called by:* [`LazyCommandSet.do_lazy_stage`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_stage), [`LazyOrchestratorApp.toggle_stage`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-toggle_stage), [`stages_toggle`](lazyc2.blueprints.orchestrator.py.md#stages_toggle)

---

<a id="effective_verbs"></a>

### `effective_verbs`

`function` | [modules/orchestrator_config.py:572](../../modules/orchestrator_config.py#L572)

```python
def effective_verbs() -> list[dict]
```

Merged auto-verb view: built-ins plus operator overrides, additions and catalog.

**Returns:** `list[dict]`

*Called by:* [`LazyCommandSet.do_lazy_verb`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_verb), [`verb_config`](#verb_config)

---

<a id="verb_config"></a>

### `verb_config`

`function` | [modules/orchestrator_config.py:664](../../modules/orchestrator_config.py#L664)

```python
def verb_config(name: str) -> dict | None
```

Return the merged configuration of one auto verb, or None.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `dict | None`

*Calls:* [`effective_verbs`](#effective_verbs)

*Called by:* [`remove_verb`](#remove_verb), [`upsert_verb`](#upsert_verb), [`verb_enabled`](#verb_enabled)

---

<a id="verb_enabled"></a>

### `verb_enabled`

`function` | [modules/orchestrator_config.py:673](../../modules/orchestrator_config.py#L673)

```python
def verb_enabled(name: str) -> bool
```

Return whether one auto verb may be proposed or executed.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`verb_config`](#verb_config)

*Called by:* [`LazyOrchestratorApp.toggle_verb`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-toggle_verb)

---

<a id="upsert_verb"></a>

### `upsert_verb`

`function` | [modules/orchestrator_config.py:679](../../modules/orchestrator_config.py#L679)

```python
def upsert_verb(name: str, *, enabled: bool | None = None, keywords: list[str] | None = None, phases: list[str] | None = None, needs_target: bool | None = None, extra_args: str | None = None, description: str | None = None, custom: bool = False) -> dict
```

Create or update one auto-verb override in the payload.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  | Verb (must match an existing shell command when custom). |
| `enabled` | `bool \| None` | `None` | New enabled flag. |
| `keywords` | `list[str] \| None` | `None` | Intent/goal signals selecting the verb. |
| `phases` | `list[str] \| None` | `None` | Kill-chain phases the verb serves. |
| `needs_target` | `bool \| None` | `None` | Whether the built line carries the loop target. |
| `extra_args` | `str \| None` | `None` | Fixed tail args appended after the target. |
| `description` | `str \| None` | `None` | Operator-facing note. |
| `custom` | `bool` | `False` | Mark as a new operator-defined verb. |

**Returns:** `dict` - The merged entry after persisting.

**Raises**

- `ValueError`: Empty verb name.

*Calls:* [`verb_config`](#verb_config)

*Called by:* [`LazyCommandSet.do_lazy_verb`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_verb), [`LazyOrchestratorApp.add_auto_verb`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-add_auto_verb), [`LazyOrchestratorApp.toggle_verb`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-toggle_verb), [`remove_verb`](#remove_verb)

---

<a id="remove_verb"></a>

### `remove_verb`

`function` | [modules/orchestrator_config.py:736](../../modules/orchestrator_config.py#L736)

```python
def remove_verb(name: str) -> bool
```

Remove a custom verb, or disable a built-in one.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `bool`

*Calls:* [`upsert_verb`](#upsert_verb), [`verb_config`](#verb_config)

*Called by:* [`LazyCommandSet.do_lazy_verb`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_verb), [`LazyOrchestratorApp.remove_auto_verb`](cli.lazy_orchestrator.py.md#lazyorchestratorapp-remove_auto_verb)

---

<a id="reset"></a>

### `reset`

`function` | [modules/orchestrator_config.py:757](../../modules/orchestrator_config.py#L757)

```python
def reset() -> None
```

Drop every orchestrator override (back to YAML defaults).

*Called by:* [`LazyCommandSet.do_lazy_stage`](cli.commands.lazyops.py.md#lazycommandset-do_lazy_stage)

---

<a id="validate_config"></a>

### `validate_config`

`function` | [modules/orchestrator_config.py:764](../../modules/orchestrator_config.py#L764)

```python
def validate_config(data: Any) -> list[str]
```

Validate one raw orchestration mapping.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `Any` |  | Parsed YAML document. |

**Returns:** `list[str]` - Human-readable errors; an empty list means the document is valid.

*Calls:* [`validate_triggers`](modules.trigger_policy.py.md#validate_triggers)

---

## Constants

<a id="orchestrator_yaml_path"></a>

### `ORCHESTRATOR_YAML_PATH`

`constant` | [modules/orchestrator_config.py:30](../../modules/orchestrator_config.py#L30)

```python
ORCHESTRATOR_YAML_PATH = BASE_DIR / 'config' / 'orchestrator.yaml'
```

---

<a id="stage_defs"></a>

### `STAGE_DEFS`

`constant` | [modules/orchestrator_config.py:33](../../modules/orchestrator_config.py#L33)

```python
STAGE_DEFS
```

---

<a id="fallback_stages"></a>

### `FALLBACK_STAGES`

`constant` | [modules/orchestrator_config.py:63](../../modules/orchestrator_config.py#L63)

```python
FALLBACK_STAGES: dict[str, dict[str, Any]]
```

---

<a id="fallback_limits"></a>

### `FALLBACK_LIMITS`

`constant` | [modules/orchestrator_config.py:73](../../modules/orchestrator_config.py#L73)

```python
FALLBACK_LIMITS: dict[str, int | float]
```

---

<a id="fallback_budget"></a>

### `FALLBACK_BUDGET`

`constant` | [modules/orchestrator_config.py:89](../../modules/orchestrator_config.py#L89)

```python
FALLBACK_BUDGET: dict[str, int] = {'max_rounds': 10, 'max_toolcalls': 200, 'max_findings': 50}
```

---

<a id="fallback_findings"></a>

### `FALLBACK_FINDINGS`

`constant` | [modules/orchestrator_config.py:91](../../modules/orchestrator_config.py#L91)

```python
FALLBACK_FINDINGS: dict[str, Any]
```

---

<a id="fallback_progress"></a>

### `FALLBACK_PROGRESS`

`constant` | [modules/orchestrator_config.py:99](../../modules/orchestrator_config.py#L99)

```python
FALLBACK_PROGRESS: dict[str, Any]
```

---

<a id="fallback_mode"></a>

### `FALLBACK_MODE`

`constant` | [modules/orchestrator_config.py:105](../../modules/orchestrator_config.py#L105)

```python
FALLBACK_MODE: str = 'redteam'
```

---

<a id="engagement_modes"></a>

### `ENGAGEMENT_MODES`

`constant` | [modules/orchestrator_config.py:107](../../modules/orchestrator_config.py#L107)

```python
ENGAGEMENT_MODES: tuple[str, ...] = ('pentest', 'redteam', 'ctf')
```

---

<a id="fallback_sinks"></a>

### `FALLBACK_SINKS`

`constant` | [modules/orchestrator_config.py:109](../../modules/orchestrator_config.py#L109)

```python
FALLBACK_SINKS: dict[str, bool]
```

---

<a id="default_stages"></a>

### `DEFAULT_STAGES`

`constant` | [modules/orchestrator_config.py:122](../../modules/orchestrator_config.py#L122)

```python
DEFAULT_STAGES: dict[str, bool] = {name: bool(data['enabled']) for name, data in FALLBACK_STAGES.items()}
```

---
