# `modules.mediation.telemetry_mediator`

> Source: [modules/mediation/telemetry_mediator.py:1](../../modules/mediation/telemetry_mediator.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Specialised mediator for loop telemetry coordination.

Owns every `[`modules.loop_ai_bridge`](modules.loop_ai_bridge.py.md)` interaction: loop event publish,
detection annotation, step recording, MoE/RL member selection, and SWAN
consultation. Consumers request these through the mediator instead of
importing the bridge directly.

## Contents

- **Classes:** [`TelemetryMediator`](#telemetrymediator)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_mediation_telemetry_mediator_py__TelemetryMediator_publish_event(["TelemetryMediator.publish_event"])
    n_modules_loop_ai_bridge_py__publish_loop_event["loop_ai_bridge.publish_loop_event"]
    n_modules_mediation_telemetry_mediator_py__TelemetryMediator_publish_event -.-> n_modules_loop_ai_bridge_py__publish_loop_event
```

## Classes

<a id="telemetrymediator"></a>

### `TelemetryMediator`

`class` | [modules/mediation/telemetry_mediator.py:14](../../modules/mediation/telemetry_mediator.py#L14)

```python
class TelemetryMediator
```

Mediate learning and event telemetry for the autonomous loop.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`domain`](#telemetrymediator-domain) | `str` | `'loop.telemetry'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`describe`](#telemetrymediator-describe) | method | Return mediator metadata for diagnostics. |
| [`publish_event`](#telemetrymediator-publish_event) | method | Publish one loop activity event to listeners. |
| [`annotate_detection`](#telemetrymediator-annotate_detection) | method | Return the detection annotation for one command. |
| [`assess_opsec`](#telemetrymediator-assess_opsec) | method | Return the pre-execution OPSEC gate assessment for one command. |
| [`record_outcome_quality`](#telemetrymediator-record_outcome_quality) | method | Record one intent's net yield as a decision-quality reward. |
| [`tool_class_yields`](#telemetrymediator-tool_class_yields) | method | Return learned decision-quality yields for candidate summaries. |
| [`record_step`](#telemetrymediator-record_step) | method | Record one executed step for learning stores. |
| [`swan_available`](#telemetrymediator-swan_available) | method | Return True when the SWAN ensemble is ready. |
| [`swan_consult`](#telemetrymediator-swan_consult) | method | Consult the SWAN ensemble with one prompt. |
| [`moe_route`](#telemetrymediator-moe_route) | method | Return the preferred MoE expert for a task type. |
| [`rl_select`](#telemetrymediator-rl_select) | method | Return the RL-preferred candidate name. |
| [`moe_record_outcome`](#telemetrymediator-moe_record_outcome) | method | Record one MoE outcome for learning. |
| [`rl_update`](#telemetrymediator-rl_update) | method | Apply one Q-learning update for an executed action. |

<a id="telemetrymediator-describe"></a>

#### `TelemetryMediator.describe`

`method` | [modules/mediation/telemetry_mediator.py:19](../../modules/mediation/telemetry_mediator.py#L19)

```python
def describe(self) -> dict[str, Any]
```

Return mediator metadata for diagnostics.

**Returns:** `dict[str, Any]`

<a id="telemetrymediator-publish_event"></a>

#### `TelemetryMediator.publish_event`

`method` | [modules/mediation/telemetry_mediator.py:23](../../modules/mediation/telemetry_mediator.py#L23)

```python
def publish_event(self, task_id: str, worker: str, kind: str, text: str, severity: str = 'info') -> None
```

Publish one loop activity event to listeners.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  | Loop task identifier. |
| `worker` | `str` |  | Emitting worker name. |
| `kind` | `str` |  | Event kind. |
| `text` | `str` |  | Cleaned event text. |
| `severity` | `str` | `'info'` | Severity label. |

*Calls:* [`publish_loop_event`](modules.loop_ai_bridge.py.md#publish_loop_event)

<a id="telemetrymediator-annotate_detection"></a>

#### `TelemetryMediator.annotate_detection`

`method` | [modules/mediation/telemetry_mediator.py:43](../../modules/mediation/telemetry_mediator.py#L43)

```python
def annotate_detection(self, command: str) -> dict
```

Return the detection annotation for one command.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  | Shell command line. |

**Returns:** `dict` - Annotation mapping, empty dict when unavailable.

<a id="telemetrymediator-assess_opsec"></a>

#### `TelemetryMediator.assess_opsec`

`method` | [modules/mediation/telemetry_mediator.py:59](../../modules/mediation/telemetry_mediator.py#L59)

```python
def assess_opsec(self, command: str, rhost: str = '') -> dict | None
```

Return the pre-execution OPSEC gate assessment for one command.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  | Shell command line. |
| `rhost` | `str` | `''` | Target host for sensitivity context. |

**Returns:** `dict | None` - Gate mapping (gate/noise/risk_label/explanation/mitigations),
or None when the stage is disabled or scoring failed.

<a id="telemetrymediator-record_outcome_quality"></a>

#### `TelemetryMediator.record_outcome_quality`

`method` | [modules/mediation/telemetry_mediator.py:77](../../modules/mediation/telemetry_mediator.py#L77)

```python
def record_outcome_quality(self, worker: str, intent_summary: str, facts: int, findings: int) -> None
```

Record one intent's net yield as a decision-quality reward.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `worker` | `str` |  | Emitting worker name. |
| `intent_summary` | `str` |  | Summary of the finished intent. |
| `facts` | `int` |  | Facts persisted by the intent's writeback. |
| `findings` | `int` |  | Findings persisted by the intent's writeback. |

<a id="telemetrymediator-tool_class_yields"></a>

#### `TelemetryMediator.tool_class_yields`

`method` | [modules/mediation/telemetry_mediator.py:93](../../modules/mediation/telemetry_mediator.py#L93)

```python
def tool_class_yields(self, summaries: list[str], phase: str = 'engage') -> dict[str, float]
```

Return learned decision-quality yields for candidate summaries.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `summaries` | `list[str]` |  | Candidate summaries the planner is about to rank. |
| `phase` | `str` | `'engage'` | Engagement phase key the reward was recorded under. |

**Returns:** `dict[str, float]` - Mapping of summary to its tool-class Q-value, empty when the
stage is off or the trainer is unavailable.

<a id="telemetrymediator-record_step"></a>

#### `TelemetryMediator.record_step`

`method` | [modules/mediation/telemetry_mediator.py:111](../../modules/mediation/telemetry_mediator.py#L111)

```python
def record_step(self, task_id: str, worker: str, command: str, output: str, detection_prob: float = 0.0) -> None
```

Record one executed step for learning stores.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  | Loop task identifier. |
| `worker` | `str` |  | Emitting worker name. |
| `command` | `str` |  | Executed command. |
| `output` | `str` |  | Command output extract. |
| `detection_prob` | `float` | `0.0` | Detection likelihood of the command. |

<a id="telemetrymediator-swan_available"></a>

#### `TelemetryMediator.swan_available`

`method` | [modules/mediation/telemetry_mediator.py:128](../../modules/mediation/telemetry_mediator.py#L128)

```python
def swan_available(self) -> bool
```

Return True when the SWAN ensemble is ready.

**Returns:** `bool`

<a id="telemetrymediator-swan_consult"></a>

#### `TelemetryMediator.swan_consult`

`method` | [modules/mediation/telemetry_mediator.py:137](../../modules/mediation/telemetry_mediator.py#L137)

```python
def swan_consult(self, prompt: str, task_type: str = 'recon', phase: str = 'enumeration', timeout: float = 120.0) -> str
```

Consult the SWAN ensemble with one prompt.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `prompt` | `str` |  | Question text. |
| `task_type` | `str` | `'recon'` | Task typing for routing. |
| `phase` | `str` | `'enumeration'` | Kill-chain phase label. |
| `timeout` | `float` | `120.0` | Seconds before giving up. |

**Returns:** `str` - Ensemble reply, or an empty string when unavailable.

<a id="telemetrymediator-moe_route"></a>

#### `TelemetryMediator.moe_route`

`method` | [modules/mediation/telemetry_mediator.py:162](../../modules/mediation/telemetry_mediator.py#L162)

```python
def moe_route(self, task_type: str) -> Any
```

Return the preferred MoE expert for a task type.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_type` | `str` |  | Task typing for routing. |

**Returns:** `Any` - Expert object or None when routing is unavailable.

<a id="telemetrymediator-rl_select"></a>

#### `TelemetryMediator.rl_select`

`method` | [modules/mediation/telemetry_mediator.py:178](../../modules/mediation/telemetry_mediator.py#L178)

```python
def rl_select(self, task_type: str, phase: str, candidates: list[str], deterministic: bool = False) -> str
```

Return the RL-preferred candidate name.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_type` | `str` |  | Task typing for routing. |
| `phase` | `str` |  | Kill-chain phase label. |
| `candidates` | `list[str]` |  | Member name candidates. |
| `deterministic` | `bool` | `False` | Force deterministic selection. |

**Returns:** `str` - Preferred candidate name, empty when unavailable.

<a id="telemetrymediator-moe_record_outcome"></a>

#### `TelemetryMediator.moe_record_outcome`

`method` | [modules/mediation/telemetry_mediator.py:203](../../modules/mediation/telemetry_mediator.py#L203)

```python
def moe_record_outcome(self, expert_id: str, task_type: str, reward: float, detection_prob: float = 0.0) -> None
```

Record one MoE outcome for learning.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `expert_id` | `str` |  | Member name. |
| `task_type` | `str` |  | Task typing for routing. |
| `reward` | `float` |  | Reward signal. |
| `detection_prob` | `float` | `0.0` | Detection likelihood. |

<a id="telemetrymediator-rl_update"></a>

#### `TelemetryMediator.rl_update`

`method` | [modules/mediation/telemetry_mediator.py:219](../../modules/mediation/telemetry_mediator.py#L219)

```python
def rl_update(self, task_type: str, phase: str, action: str, reward: float, candidates: list[str], detection_prob: float = 0.0) -> None
```

Apply one Q-learning update for an executed action.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_type` | `str` |  | Task typing for routing. |
| `phase` | `str` |  | Kill-chain phase label. |
| `action` | `str` |  | Executed member name. |
| `reward` | `float` |  | Reward signal. |
| `candidates` | `list[str]` |  | Member name candidates. |
| `detection_prob` | `float` | `0.0` | Detection likelihood. |

---
