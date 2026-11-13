# `skills.autonomous_daemon`

> Source: [skills/autonomous_daemon.py:1](../../skills/autonomous_daemon.py#L1) | language `py` | coverage 89.2% | [API index](../index.md)

skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon ================================================================== Bridges LazyOwn (Claude-assisted orchestrator) and a fully autonomous OpenClaw/OpenHands-style system.

The daemon runs as an independent process and does NOT need Claude Code
to operate between objectives. Claude remains the Borg Queen for injecting
high-level objectives, but the daemon executes them without intervention.

Architecture (4 concurrent asyncio roles)
------------------------------------------
  Role 1 — ObjectiveLoop    : Watches objectives.jsonl. When a pending
                              objective appears, takes it, plans, executes.
  Role 2 — ExecutionEngine  : Per-step execution loop (equivalent to
                              auto_loop in MCP but without MCP). Uses the
                              same command selection cascade:
                              reactive -> parquet -> bridge -> LLM -> fallback
  Role 3 — WorldModelWatcher: Watches world_model.json. When the phase
                              changes (recon->enum->exploit...) or new
                              hosts/credentials appear, injects derived
                              objectives and notifies hive drones.
  Role 4 — DroneCoordinator : Hive-mind bridge. When recon discovers a
                              host, launches exploit/analyze drones in
                              parallel. When a drone finishes, writes the
                              result to the stream and updates the objective.

Event streams (push, no polling)
----------------------------------
  sessions/autonomous_events.jsonl  — every action, finding, decision
  sessions/autonomous_status.json   — real-time daemon state

Management
-----------
  python3 skills/autonomous_daemon.py start   # fork and detach
  python3 skills/autonomous_daemon.py stop    # terminate by PID
  python3 skills/autonomous_daemon.py run     # foreground (debug)
  python3 skills/autonomous_daemon.py status  # read state
  python3 skills/autonomous_daemon.py inject "Objective" [--priority high]

MCP integration
----------------
  lazyown_autonomous_start(max_steps_per_objective=10, backend="groq")
  lazyown_autonomous_stop()
  lazyown_autonomous_status()
  lazyown_autonomous_inject(text, priority)

## Contents

- **Classes:** [`ICommandRunner`](#icommandrunner), [`MCPCommandRunner`](#mcpcommandrunner), [`PTYCommandRunner`](#ptycommandrunner), [`CommandRunnerChain`](#commandrunnerchain), [`ICommandSelector`](#icommandselector), [`ReactiveSelector`](#reactiveselector), [`LLMSelector`](#llmselector), [`SWANSelector`](#swanselector), [`FallbackSelector`](#fallbackselector), [`MetricsAwareSelector`](#metricsawareselector), [`UnifiedBrainSelector`](#unifiedbrainselector), [`CascadeStrategy`](#cascadestrategy), [`StrategyEngine`](#strategyengine), [`StepResult`](#stepresult), [`IObjectiveHandler`](#iobjectivehandler), [`ExecutionEngine`](#executionengine), [`DroneCoordinator`](#dronecoordinator), [`EnginePhaseStep`](#enginephasestep), [`EnginePhaseResult`](#enginephaseresult), [`IToolFallbackResolver`](#itoolfallbackresolver), [`StaticFallbackResolver`](#staticfallbackresolver), [`BridgeFallbackResolver`](#bridgefallbackresolver), [`EngageOrchestrator`](#engageorchestrator)
- **Functions:** [`compute_decision_seed`](#compute_decision_seed), [`mcp_engage_target`](#mcp_engage_target), [`mcp_engage_status`](#mcp_engage_status), [`mcp_engage_approve`](#mcp_engage_approve), [`mcp_engage_list_pending`](#mcp_engage_list_pending), [`cmd_engage`](#cmd_engage), [`objective_loop`](#objective_loop), [`world_model_watcher`](#world_model_watcher), [`heartbeat_loop`](#heartbeat_loop), [`cmd_run`](#cmd_run), [`cmd_start`](#cmd_start), [`cmd_stop`](#cmd_stop), [`cmd_status`](#cmd_status), [`cmd_inject`](#cmd_inject), [`mcp_autonomous_start`](#mcp_autonomous_start), [`mcp_autonomous_stop`](#mcp_autonomous_stop), [`mcp_autonomous_status`](#mcp_autonomous_status), [`mcp_autonomous_inject`](#mcp_autonomous_inject), [`mcp_autonomous_events`](#mcp_autonomous_events)
- **Constants:** [`SKILLS_DIR`](#skills_dir), [`LAZYOWN_DIR`](#lazyown_dir), [`MODULES_DIR`](#modules_dir), [`SESSIONS_DIR`](#sessions_dir), [`PAYLOAD_FILE`](#payload_file), [`PID_FILE`](#pid_file), [`STATUS_FILE`](#status_file), [`EVENTS_FILE`](#events_file), [`TASKS_FILE`](#tasks_file), [`OBJ_POLL_S`](#obj_poll_s), [`WM_POLL_S`](#wm_poll_s), [`STEP_TIMEOUT_S`](#step_timeout_s), [`STEP_DELAY_S`](#step_delay_s), [`MAX_STEPS_DEFAULT`](#max_steps_default), [`MAX_FAILS_PER_CMD`](#max_fails_per_cmd), [`HIVE_BACKEND`](#hive_backend), [`HIVE_MAX_ITER`](#hive_max_iter), [`HEARTBEAT_S`](#heartbeat_s), [`BLOCKED_ESCALATE_N`](#blocked_escalate_n), [`CONTROL_VETO_MAX_RETRIES`](#control_veto_max_retries), [`CONTROL_APPROVAL_TTL_S`](#control_approval_ttl_s), [`CONTROL_PAUSE_POLL_S`](#control_pause_poll_s), [`CONTROL_PAUSE_MAX_S`](#control_pause_max_s), [`METRICS_BIAS_ENABLED`](#metrics_bias_enabled), [`METRICS_BIAS_WINDOW_S`](#metrics_bias_window_s), [`METRICS_BIAS_MIN_SUCCESS`](#metrics_bias_min_success), [`METRICS_BIAS_MIN_ATTEMPTS`](#metrics_bias_min_attempts), [`METRICS_BIAS_CACHE_TTL_S`](#metrics_bias_cache_ttl_s), [`DECISION_SEED_LENGTH`](#decision_seed_length), [`REWARD_DISPLAY_PRECISION`](#reward_display_precision)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class ICommandRunner
    ICommandRunner : run()
    ICommandRunner : name()
    class MCPCommandRunner
    MCPCommandRunner : name()
    MCPCommandRunner : run()
    class PTYCommandRunner
    PTYCommandRunner : name()
    PTYCommandRunner : run()
    class CommandRunnerChain
    CommandRunnerChain : __init__()
    CommandRunnerChain : name()
    CommandRunnerChain : run()
    class ICommandSelector
    ICommandSelector : select()
    class ReactiveSelector
    ReactiveSelector : __init__()
    ReactiveSelector : register_output()
    ReactiveSelector : select()
    class LLMSelector
    LLMSelector : select()
    class SWANSelector
    SWANSelector : select()
    class FallbackSelector
    FallbackSelector : select()
    class MetricsAwareSelector
    MetricsAwareSelector : __init__()
    MetricsAwareSelector : wrapped()
    MetricsAwareSelector : select()
    class UnifiedBrainSelector
    UnifiedBrainSelector : name
    UnifiedBrainSelector : __init__()
    UnifiedBrainSelector : select()
    class CascadeStrategy
    CascadeStrategy : __init__()
    CascadeStrategy : next_command()
    class StrategyEngine
    StrategyEngine : __init__()
    StrategyEngine : register_output()
    StrategyEngine : next_command()
    class StepResult
    StepResult : int step
    StepResult : str command
    StepResult : str output
    StepResult : bool success
    StepResult : str source
    StepResult : list[dict] findings
    StepResult : str phase
    class IObjectiveHandler
    IObjectiveHandler : handle()
    class ExecutionEngine
    ExecutionEngine : __init__()
    ExecutionEngine : handle()
    ExecutionEngine : run_async()
    class DroneCoordinator
    DroneCoordinator : __init__()
    DroneCoordinator : process_findings()
    class EnginePhaseStep
    EnginePhaseStep : str phase
    EnginePhaseStep : str primary
    EnginePhaseStep : str label
    EnginePhaseStep : int timeout_s
    class EnginePhaseResult
    EnginePhaseResult : EnginePhaseStep step
    EnginePhaseResult : str command_used
    EnginePhaseResult : str output
    EnginePhaseResult : bool success
    EnginePhaseResult : str switched_from
    EnginePhaseResult : str skipped_reason
    EnginePhaseResult : str evidence
    EnginePhaseResult : did_switch()
    class IToolFallbackResolver
    IToolFallbackResolver : next_tool()
    class StaticFallbackResolver
    StaticFallbackResolver : next_tool()
    class BridgeFallbackResolver
    BridgeFallbackResolver : __init__()
    BridgeFallbackResolver : next_tool()
    class EngageOrchestrator
    EngageOrchestrator : DEFAULT_MAX_SWITCHES_PER_STEP
    EngageOrchestrator : __init__()
    EngageOrchestrator : engagement_id()
    EngageOrchestrator : run()
    ICommandRunner <|-- MCPCommandRunner
    ICommandRunner <|-- PTYCommandRunner
    ICommandRunner <|-- CommandRunnerChain
    ICommandSelector <|-- ReactiveSelector
    ICommandSelector <|-- LLMSelector
    ICommandSelector <|-- SWANSelector
    ICommandSelector <|-- FallbackSelector
    ICommandSelector <|-- MetricsAwareSelector
    ICommandSelector <|-- UnifiedBrainSelector
    IObjectiveHandler <|-- ExecutionEngine
    IToolFallbackResolver <|-- StaticFallbackResolver
    IToolFallbackResolver <|-- BridgeFallbackResolver
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_autonomous_daemon_py__StrategyEngine___init__(["StrategyEngine.__init__"])
    n_skills_autonomous_daemon_py__CascadeStrategy___init__(["CascadeStrategy.__init__"])
    n_skills_autonomous_daemon_py__FallbackSelector(["FallbackSelector"])
    n_skills_autonomous_daemon_py__LLMSelector(["LLMSelector"])
    n_skills_autonomous_daemon_py__ReactiveSelector___init__(["ReactiveSelector.__init__"])
    n_skills_autonomous_daemon_py__SWANSelector(["SWANSelector"])
    n_skills_autonomous_daemon_py__UnifiedBrainSelector___init__(["UnifiedBrainSelector.__init__"])
    n_skills_autonomous_daemon_py__StrategyEngine_register_output(["StrategyEngine.register_output"])
    n_skills_autonomous_daemon_py__ReactiveSelector_register_output(["ReactiveSelector.register_output"])
    n_skills_autonomous_daemon_py__StrategyEngine_next_command(["StrategyEngine.next_command"])
    n_skills_autonomous_daemon_py__CascadeStrategy_next_command(["CascadeStrategy.next_command"])
    n_skills_autonomous_daemon_py__BridgeFallbackResolver___init__(["BridgeFallbackResolver.__init__"])
    n_skills_autonomous_daemon_py__StaticFallbackResolver(["StaticFallbackResolver"])
    n_skills_autonomous_daemon_py__BridgeFallbackResolver_next_tool(["BridgeFallbackResolver.next_tool"])
    n_skills_autonomous_daemon_py__StaticFallbackResolver_next_tool(["StaticFallbackResolver.next_tool"])
    n_skills_autonomous_daemon_py__EngageOrchestrator___init__(["EngageOrchestrator.__init__"])
    n_skills_autonomous_daemon_py__EnginePhaseStep(["EnginePhaseStep"])
    n_skills_autonomous_daemon_py__cmd_engage(["cmd_engage"])
    n_skills_autonomous_daemon_py__mcp_engage_target(["mcp_engage_target"])
    n_skills_autonomous_daemon_py__objective_loop(["objective_loop"])
    n_skills_autonomous_daemon_py__DroneCoordinator___init__(["DroneCoordinator.__init__"])
    n_skills_autonomous_daemon_py__DroneCoordinator_process_findings(["DroneCoordinator.process_findings"])
    n_skills_autonomous_daemon_py__ExecutionEngine___init__(["ExecutionEngine.__init__"])
    n_skills_autonomous_daemon_py__ExecutionEngine_run_async(["ExecutionEngine.run_async"])
    n_lazyc2_security_command_allowlist_py__CommandDecision["command_allowlist.CommandDecision"]
    n_skills_autonomous_daemon_py__FallbackSelector_select(["FallbackSelector.select"])
    n_skills_autonomous_daemon_py__UnifiedBrainSelector_select(["UnifiedBrainSelector.select"])
    n_modules_selection_base_py__SelectionContext["base.SelectionContext"]
    n_modules_selection_registry_py__propose_next["registry.propose_next"]
    n_skills_autonomous_daemon_py__StrategyEngine___init__ --> n_skills_autonomous_daemon_py__CascadeStrategy___init__
    n_skills_autonomous_daemon_py__StrategyEngine___init__ --> n_skills_autonomous_daemon_py__FallbackSelector
    n_skills_autonomous_daemon_py__StrategyEngine___init__ --> n_skills_autonomous_daemon_py__LLMSelector
    n_skills_autonomous_daemon_py__StrategyEngine___init__ --> n_skills_autonomous_daemon_py__ReactiveSelector___init__
    n_skills_autonomous_daemon_py__StrategyEngine___init__ --> n_skills_autonomous_daemon_py__SWANSelector
    n_skills_autonomous_daemon_py__StrategyEngine___init__ --> n_skills_autonomous_daemon_py__UnifiedBrainSelector___init__
    n_skills_autonomous_daemon_py__StrategyEngine_register_output --> n_skills_autonomous_daemon_py__ReactiveSelector_register_output
    n_skills_autonomous_daemon_py__StrategyEngine_next_command --> n_skills_autonomous_daemon_py__CascadeStrategy_next_command
    n_skills_autonomous_daemon_py__BridgeFallbackResolver___init__ --> n_skills_autonomous_daemon_py__StaticFallbackResolver
    n_skills_autonomous_daemon_py__BridgeFallbackResolver_next_tool --> n_skills_autonomous_daemon_py__StaticFallbackResolver_next_tool
    n_skills_autonomous_daemon_py__EngageOrchestrator___init__ --> n_skills_autonomous_daemon_py__BridgeFallbackResolver___init__
    n_skills_autonomous_daemon_py__EngageOrchestrator___init__ --> n_skills_autonomous_daemon_py__EnginePhaseStep
    n_skills_autonomous_daemon_py__cmd_engage --> n_skills_autonomous_daemon_py__mcp_engage_target
    n_skills_autonomous_daemon_py__objective_loop --> n_skills_autonomous_daemon_py__DroneCoordinator___init__
    n_skills_autonomous_daemon_py__objective_loop --> n_skills_autonomous_daemon_py__DroneCoordinator_process_findings
    n_skills_autonomous_daemon_py__objective_loop --> n_skills_autonomous_daemon_py__ExecutionEngine___init__
    n_skills_autonomous_daemon_py__objective_loop --> n_skills_autonomous_daemon_py__ExecutionEngine_run_async
    n_skills_autonomous_daemon_py__objective_loop --> n_skills_autonomous_daemon_py__StrategyEngine___init__
    n_skills_autonomous_daemon_py__ReactiveSelector_register_output -.-> n_lazyc2_security_command_allowlist_py__CommandDecision
    n_skills_autonomous_daemon_py__FallbackSelector_select -.-> n_lazyc2_security_command_allowlist_py__CommandDecision
    n_skills_autonomous_daemon_py__UnifiedBrainSelector_select -.-> n_lazyc2_security_command_allowlist_py__CommandDecision
    n_skills_autonomous_daemon_py__UnifiedBrainSelector_select -.-> n_modules_selection_base_py__SelectionContext
    n_skills_autonomous_daemon_py__UnifiedBrainSelector_select -.-> n_modules_selection_registry_py__propose_next
    n_skills_autonomous_daemon_py__CascadeStrategy_next_command -.-> n_lazyc2_security_command_allowlist_py__CommandDecision
```

## Classes

<a id="icommandrunner"></a>

### `ICommandRunner`

`class` `abstract` | [skills/autonomous_daemon.py:423](../../skills/autonomous_daemon.py#L423)

```python
class ICommandRunner(ABC)
```

Bases: `ABC`

Subclasses: [`CommandRunnerChain`](#commandrunnerchain), [`MCPCommandRunner`](#mcpcommandrunner), [`PTYCommandRunner`](#ptycommandrunner)

Contract for executing a LazyOwn shell command.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`run`](#icommandrunner-run) | method | Execute command within timeout seconds. |
| [`name`](#icommandrunner-name) | property | Human-readable identifier for this runner. |

<a id="icommandrunner-run"></a>

#### `ICommandRunner.run`

`method` `abstract` | [skills/autonomous_daemon.py:427](../../skills/autonomous_daemon.py#L427)

Decorators: `@abstractmethod`

```python
def run(self, command: str, timeout: int) -> str
```

Execute command within timeout seconds.

Return text output.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  |  |
| `timeout` | `int` |  |  |

**Returns:** `str`

<a id="icommandrunner-name"></a>

#### `ICommandRunner.name`

`property` `abstract` | [skills/autonomous_daemon.py:432](../../skills/autonomous_daemon.py#L432)

Decorators: `@property`, `@abstractmethod`

```python
def name(self) -> str
```

Human-readable identifier for this runner.

**Returns:** `str`

---

<a id="mcpcommandrunner"></a>

### `MCPCommandRunner`

`class` | [skills/autonomous_daemon.py:476](../../skills/autonomous_daemon.py#L476)

```python
class MCPCommandRunner(ICommandRunner)
```

Bases: [`ICommandRunner`](#icommandrunner)

Delegates to lazyown_mcp._run_lazyown_command when available.

Single Responsibility: MCP import + delegation only.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`name`](#mcpcommandrunner-name) | property | Human-readable identifier for this runner. |
| [`run`](#mcpcommandrunner-run) | method | Try to import and call the MCP runner. |

<a id="mcpcommandrunner-name"></a>

#### `MCPCommandRunner.name`

`property` | [skills/autonomous_daemon.py:483](../../skills/autonomous_daemon.py#L483)

Decorators: `@property`

```python
def name(self) -> str
```

Human-readable identifier for this runner.

**Returns:** `str`

> **Inherited:** Documentation from [`ICommandRunner.name`](#icommandrunner-name) (skills/autonomous_daemon.py:432).

<a id="mcpcommandrunner-run"></a>

#### `MCPCommandRunner.run`

`method` | [skills/autonomous_daemon.py:486](../../skills/autonomous_daemon.py#L486)

```python
def run(self, command: str, timeout: int = STEP_TIMEOUT_S) -> str
```

Try to import and call the MCP runner.

Raises ImportError on failure.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  |  |
| `timeout` | `int` | `STEP_TIMEOUT_S` |  |

**Returns:** `str`

---

<a id="ptycommandrunner"></a>

### `PTYCommandRunner`

`class` | [skills/autonomous_daemon.py:495](../../skills/autonomous_daemon.py#L495)

```python
class PTYCommandRunner(ICommandRunner)
```

Bases: [`ICommandRunner`](#icommandrunner)

Full PTY-based command execution that mirrors _run_lazyown_command in the MCP but has no dependency on lazyown_mcp.

Single Responsibility: PTY subprocess management only.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`name`](#ptycommandrunner-name) | property | Human-readable identifier for this runner. |
| [`run`](#ptycommandrunner-run) | method | Execute command via PTY. |

<a id="ptycommandrunner-name"></a>

#### `PTYCommandRunner.name`

`property` | [skills/autonomous_daemon.py:503](../../skills/autonomous_daemon.py#L503)

Decorators: `@property`

```python
def name(self) -> str
```

Human-readable identifier for this runner.

**Returns:** `str`

> **Inherited:** Documentation from [`ICommandRunner.name`](#icommandrunner-name) (skills/autonomous_daemon.py:432).

<a id="ptycommandrunner-run"></a>

#### `PTYCommandRunner.run`

`method` | [skills/autonomous_daemon.py:506](../../skills/autonomous_daemon.py#L506)

```python
def run(self, command: str, timeout: int = STEP_TIMEOUT_S) -> str
```

Execute command via PTY.

Returns cleaned text output.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  |  |
| `timeout` | `int` | `STEP_TIMEOUT_S` |  |

**Returns:** `str`

---

<a id="commandrunnerchain"></a>

### `CommandRunnerChain`

`class` | [skills/autonomous_daemon.py:584](../../skills/autonomous_daemon.py#L584)

```python
class CommandRunnerChain(ICommandRunner)
```

Bases: [`ICommandRunner`](#icommandrunner)

Tries each runner in order and returns the first successful result.

Falls back to the next runner on any exception.

Chain of Responsibility pattern.
Open/Closed: add new runners without modifying this class.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#commandrunnerchain-__init__) | constructor |  |
| [`name`](#commandrunnerchain-name) | property | Human-readable identifier for this runner. |
| [`run`](#commandrunnerchain-run) | method | Try each runner in sequence. |

<a id="commandrunnerchain-__init__"></a>

#### `CommandRunnerChain.__init__`

`constructor` | [skills/autonomous_daemon.py:593](../../skills/autonomous_daemon.py#L593)

```python
def __init__(self, runners: list[ICommandRunner]) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `runners` | `list[ICommandRunner]` |  |  |

**Raises**

- `ValueError`: (raised in the body, not documented)

<a id="commandrunnerchain-name"></a>

#### `CommandRunnerChain.name`

`property` | [skills/autonomous_daemon.py:599](../../skills/autonomous_daemon.py#L599)

Decorators: `@property`

```python
def name(self) -> str
```

Human-readable identifier for this runner.

**Returns:** `str`

> **Inherited:** Documentation from [`ICommandRunner.name`](#icommandrunner-name) (skills/autonomous_daemon.py:432).

<a id="commandrunnerchain-run"></a>

#### `CommandRunnerChain.run`

`method` | [skills/autonomous_daemon.py:602](../../skills/autonomous_daemon.py#L602)

```python
def run(self, command: str, timeout: int = STEP_TIMEOUT_S) -> str
```

Try each runner in sequence.

Return first successful output.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  |  |
| `timeout` | `int` | `STEP_TIMEOUT_S` |  |

**Returns:** `str`

**Raises**

- `RuntimeError`: (raised in the body, not documented)

---

<a id="icommandselector"></a>

### `ICommandSelector`

`class` `abstract` | [skills/autonomous_daemon.py:677](../../skills/autonomous_daemon.py#L677)

```python
class ICommandSelector(ABC)
```

Bases: `ABC`

Subclasses: [`FallbackSelector`](#fallbackselector), [`LLMSelector`](#llmselector), [`MetricsAwareSelector`](#metricsawareselector), [`ReactiveSelector`](#reactiveselector), [`SWANSelector`](#swanselector), [`UnifiedBrainSelector`](#unifiedbrainselector)

Contract for command selection strategies.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`select`](#icommandselector-select) | method | Return a CommandDecision or None if this selector has no suggestion. |

<a id="icommandselector-select"></a>

#### `ICommandSelector.select`

`method` `abstract` | [skills/autonomous_daemon.py:681](../../skills/autonomous_daemon.py#L681)

Decorators: `@abstractmethod`

```python
def select(self, target: str, phase: str, context: dict) -> CommandDecision | None
```

Return a CommandDecision or None if this selector has no suggestion.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `context` | `dict` |  |  |

**Returns:** `CommandDecision | None`

---

<a id="reactiveselector"></a>

### `ReactiveSelector`

`class` | [skills/autonomous_daemon.py:690](../../skills/autonomous_daemon.py#L690)

```python
class ReactiveSelector(ICommandSelector)
```

Bases: [`ICommandSelector`](#icommandselector)

Returns a pending reactive engine decision if one is available.

Single Responsibility: reactive engine integration only.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#reactiveselector-__init__) | constructor |  |
| [`register_output`](#reactiveselector-register_output) | method | Feed reactive engine with last command output to generate new decisions. |
| [`select`](#reactiveselector-select) | method | Pop and return the pending reactive decision if present. |

<a id="reactiveselector-__init__"></a>

#### `ReactiveSelector.__init__`

`constructor` | [skills/autonomous_daemon.py:696](../../skills/autonomous_daemon.py#L696)

```python
def __init__(self, reactive_engine: Any) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `reactive_engine` | `Any` |  |  |

*Called by:* [`StrategyEngine.__init__`](#strategyengine-__init__)

<a id="reactiveselector-register_output"></a>

#### `ReactiveSelector.register_output`

`method` | [skills/autonomous_daemon.py:700](../../skills/autonomous_daemon.py#L700)

```python
def register_output(self, output: str, command: str, platform: str = 'linux') -> None
```

Feed reactive engine with last command output to generate new decisions.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `output` | `str` |  |  |
| `command` | `str` |  |  |
| `platform` | `str` | `'linux'` |  |

*Calls:* [`CommandDecision`](lazyc2.security.command_allowlist.py.md#commanddecision)

*Called by:* [`StrategyEngine.register_output`](#strategyengine-register_output)

<a id="reactiveselector-select"></a>

#### `ReactiveSelector.select`

`method` | [skills/autonomous_daemon.py:727](../../skills/autonomous_daemon.py#L727)

```python
def select(self, target: str, phase: str, context: dict) -> CommandDecision | None
```

Pop and return the pending reactive decision if present.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `context` | `dict` |  |  |

**Returns:** `CommandDecision | None`

---

<a id="llmselector"></a>

### `LLMSelector`

`class` | [skills/autonomous_daemon.py:754](../../skills/autonomous_daemon.py#L754)

```python
class LLMSelector(ICommandSelector)
```

Bases: [`ICommandSelector`](#icommandselector)

Queries Groq/Ollama for a command suggestion.

Only active when AUTO_USE_LLM=1. Single Responsibility: LLM command recommendation only.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`select`](#llmselector-select) | method | Return an LLM-suggested command with catalog context, or None if disabled. |

<a id="llmselector-select"></a>

#### `LLMSelector.select`

`method` | [skills/autonomous_daemon.py:761](../../skills/autonomous_daemon.py#L761)

```python
def select(self, target: str, phase: str, context: dict) -> CommandDecision | None
```

Return an LLM-suggested command with catalog context, or None if disabled.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `context` | `dict` |  |  |

**Returns:** `CommandDecision | None`

---

<a id="swanselector"></a>

### `SWANSelector`

`class` | [skills/autonomous_daemon.py:854](../../skills/autonomous_daemon.py#L854)

```python
class SWANSelector(ICommandSelector)
```

Bases: [`ICommandSelector`](#icommandselector)

SWAN (Scalable Weighted Adaptive Network) command selector.

Routes the command-recommendation query to the best MoE expert via
Q-learning-guided routing.  Only active when AUTO_USE_SWAN=1.

Single Responsibility : MoE/RL expert routing only — no direct execution.
Open/Closed           : Extend SwanOrchestrator subclasses; this selector
                        never changes to support new experts.
Dependency Inversion  : depends on ICommandSelector interface; imports
                        swan_agent lazily so the daemon starts even without
                        GROQ_API_KEY present.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`select`](#swanselector-select) | method | Ask the best MoE expert for a command recommendation. |

<a id="swanselector-select"></a>

#### `SWANSelector.select`

`method` | [skills/autonomous_daemon.py:885](../../skills/autonomous_daemon.py#L885)

```python
def select(self, target: str, phase: str, context: dict) -> CommandDecision | None
```

Ask the best MoE expert for a command recommendation.

Returns None if disabled.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `context` | `dict` |  |  |

**Returns:** `CommandDecision | None`

---

<a id="fallbackselector"></a>

### `FallbackSelector`

`class` | [skills/autonomous_daemon.py:924](../../skills/autonomous_daemon.py#L924)

```python
class FallbackSelector(ICommandSelector)
```

Bases: [`ICommandSelector`](#icommandselector)

Static map fallback — always returns a CommandDecision, never None.

Selects OS-appropriate commands when the OS is known. Single Responsibility: static fallback map only.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`select`](#fallbackselector-select) | method | Return the static fallback command for this phase. |

<a id="fallbackselector-select"></a>

#### `FallbackSelector.select`

`method` | [skills/autonomous_daemon.py:931](../../skills/autonomous_daemon.py#L931)

```python
def select(self, target: str, phase: str, context: dict) -> CommandDecision | None
```

Return the static fallback command for this phase.

Never returns None.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `context` | `dict` |  |  |

**Returns:** `CommandDecision | None`

*Calls:* [`CommandDecision`](lazyc2.security.command_allowlist.py.md#commanddecision)

---

<a id="metricsawareselector"></a>

### `MetricsAwareSelector`

`class` | [skills/autonomous_daemon.py:947](../../skills/autonomous_daemon.py#L947)

```python
class MetricsAwareSelector(ICommandSelector)
```

Bases: [`ICommandSelector`](#icommandselector)

Decorator that demotes commands with a poor recent track record.

Wraps another [`ICommandSelector`](#icommandselector). When the wrapped selector
proposes a command whose recent `[`success_rate`](modules.llm_evaluator.py.md#qualitymetrics-success_rate)` in
[`modules.metrics.MetricsRecorder`](modules.metrics.py.md#metricsrecorder) is below the configured
threshold and whose attempt count clears
[`METRICS_BIAS_MIN_ATTEMPTS`](#metrics_bias_min_attempts), the decision is dropped (returns
``None``) so the cascade falls through to the next selector. The
rejection itself is logged at debug level and broadcast as a
``METRICS_BIAS_SKIP`` event so operators can audit why the daemon
sidestepped an otherwise valid recommendation.

The fallback selector is intentionally left unwrapped at chain
composition time: when every other selector has been filtered, the
cascade must still converge on *something*.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#metricsawareselector-__init__) | constructor | Initialise the decorator. |
| [`wrapped`](#metricsawareselector-wrapped) | property | Return the underlying selector for introspection in tests. |
| [`select`](#metricsawareselector-select) | method | Honour the [`ICommandSelector`](#icommandselector) contract. |

<a id="metricsawareselector-__init__"></a>

#### `MetricsAwareSelector.__init__`

`constructor` | [skills/autonomous_daemon.py:968](../../skills/autonomous_daemon.py#L968)

```python
def __init__(self, wrapped: ICommandSelector, metrics_source: Any = None, min_success_rate: float = METRICS_BIAS_MIN_SUCCESS, min_attempts: int = METRICS_BIAS_MIN_ATTEMPTS, window_seconds: int = METRICS_BIAS_WINDOW_S, cache_ttl_s: float = METRICS_BIAS_CACHE_TTL_S, clock: Any | None = None) -> None
```

Initialise the decorator.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `wrapped` | `ICommandSelector` |  | The selector whose decisions may be filtered. |
| `metrics_source` | `Any` | `None` | Object exposing ``summarize(window_seconds)``. Defaults to [`modules.metrics.get_recorder`](modules.metrics.py.md#get_recorder) resolved lazily on first use so the module remains importable without the metrics package present. |
| `min_success_rate` | `float` | `METRICS_BIAS_MIN_SUCCESS` | Inclusive lower bound on `[`success_rate`](modules.llm_evaluator.py.md#qualitymetrics-success_rate)`; values strictly below this are considered failing. |
| `min_attempts` | `int` | `METRICS_BIAS_MIN_ATTEMPTS` | Minimum number of recorded attempts before a command can be filtered. Avoids over-reacting to a single failure. |
| `window_seconds` | `int` | `METRICS_BIAS_WINDOW_S` | Aggregation window forwarded to ``summarize``. Set to ``0`` or a negative value to aggregate the whole log. |
| `cache_ttl_s` | `float` | `METRICS_BIAS_CACHE_TTL_S` | Time-to-live for the in-memory summary cache. Repeated calls within the TTL reuse the cached aggregate to avoid re-reading the JSONL log every step. |
| `clock` | `Any \| None` | `None` | Callable returning the current monotonic time. Injected in tests; defaults to `time.monotonic`. |

<a id="metricsawareselector-wrapped"></a>

#### `MetricsAwareSelector.wrapped`

`property` | [skills/autonomous_daemon.py:1014](../../skills/autonomous_daemon.py#L1014)

Decorators: `@property`

```python
def wrapped(self) -> ICommandSelector
```

Return the underlying selector for introspection in tests.

**Returns:** `ICommandSelector`

*Called by:* [`resolve_hostnames`](modules.lazy_timeline.py.md#resolve_hostnames)

<a id="metricsawareselector-select"></a>

#### `MetricsAwareSelector.select`

`method` | [skills/autonomous_daemon.py:1100](../../skills/autonomous_daemon.py#L1100)

```python
def select(self, target: str, phase: str, context: dict) -> CommandDecision | None
```

Honour the [`ICommandSelector`](#icommandselector) contract.

Delegates to the wrapped selector. When the proposed command
fails the success-rate gate, returns ``None`` and emits a
``METRICS_BIAS_SKIP`` event so the rejection is auditable.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `context` | `dict` |  |  |

**Returns:** `CommandDecision | None`

---

<a id="unifiedbrainselector"></a>

### `UnifiedBrainSelector`

`class` | [skills/autonomous_daemon.py:1178](../../skills/autonomous_daemon.py#L1178)

```python
class UnifiedBrainSelector(ICommandSelector)
```

Bases: [`ICommandSelector`](#icommandselector)

Daemon adapter over the one shared selector cascade.

Routes the daemon through `[`modules.selection.registry.propose_next`](modules.selection.registry.py.md#propose_next)` so it
consults the exact same action brain as the LazyLoopEngine planner: chains,
credential reuse, APT playbooks, adversary profiles and MITRE/atomic
techniques, all orchestrator-administered. Replaces the daemon's separate
chain, credential-spray and bridge selectors (now subsumed). Per-run dedupe
is carried as the shared exclude set so a command is proposed at most once,
and the daemon's burned-verb counts are passed as the shared burned set so
history- and catalogue-driven selectors skip verbs that keep failing.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`name`](#unifiedbrainselector-name) |  | `'unified_brain'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#unifiedbrainselector-__init__) | constructor |  |
| [`select`](#unifiedbrainselector-select) | method | Build a SelectionContext and return the cascade's first decision. |

<a id="unifiedbrainselector-__init__"></a>

#### `UnifiedBrainSelector.__init__`

`constructor` | [skills/autonomous_daemon.py:1193](../../skills/autonomous_daemon.py#L1193)

```python
def __init__(self, fail_counts: dict[str, int] | None = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `fail_counts` | `dict[str, int] \| None` | `None` |  |

*Called by:* [`StrategyEngine.__init__`](#strategyengine-__init__)

<a id="unifiedbrainselector-select"></a>

#### `UnifiedBrainSelector.select`

`method` | [skills/autonomous_daemon.py:1197](../../skills/autonomous_daemon.py#L1197)

```python
def select(self, target: str, phase: str, context: dict) -> CommandDecision | None
```

Build a SelectionContext and return the cascade's first decision.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `context` | `dict` |  |  |

**Returns:** `CommandDecision | None`

*Calls:* [`CommandDecision`](lazyc2.security.command_allowlist.py.md#commanddecision), [`SelectionContext`](modules.selection.base.py.md#selectioncontext), [`propose_next`](modules.selection.registry.py.md#propose_next)

---

<a id="cascadestrategy"></a>

### `CascadeStrategy`

`class` | [skills/autonomous_daemon.py:1234](../../skills/autonomous_daemon.py#L1234)

```python
class CascadeStrategy
```

Chains selectors in order and returns the first non-None result.

Open/Closed: extend by adding selectors without modifying existing ones.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#cascadestrategy-__init__) | constructor |  |
| [`next_command`](#cascadestrategy-next_command) | method | Try each selector in order. |

<a id="cascadestrategy-__init__"></a>

#### `CascadeStrategy.__init__`

`constructor` | [skills/autonomous_daemon.py:1241](../../skills/autonomous_daemon.py#L1241)

```python
def __init__(self, selectors: list[ICommandSelector]) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `selectors` | `list[ICommandSelector]` |  |  |

*Called by:* [`StrategyEngine.__init__`](#strategyengine-__init__)

<a id="cascadestrategy-next_command"></a>

#### `CascadeStrategy.next_command`

`method` | [skills/autonomous_daemon.py:1244](../../skills/autonomous_daemon.py#L1244)

```python
def next_command(self, target: str, phase: str, context: dict | None = None) -> CommandDecision
```

Try each selector in order.

The FallbackSelector ensures a result.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `context` | `dict \| None` | `None` |  |

**Returns:** `CommandDecision`

*Calls:* [`CommandDecision`](lazyc2.security.command_allowlist.py.md#commanddecision)

*Called by:* [`StrategyEngine.next_command`](#strategyengine-next_command)

---

<a id="strategyengine"></a>

### `StrategyEngine`

`class` | [skills/autonomous_daemon.py:1265](../../skills/autonomous_daemon.py#L1265)

```python
class StrategyEngine
```

Decides the next command for a (target, phase) pair.

Cascade: reactive engine -> unified brain (the one shared selector
cascade in `[`modules.selection.registry`](modules.selection.registry.py.md)`: credential reuse, intel,
APT playbooks, adversary profiles, atomic techniques, best chain) ->
parquet (successful commands from previous sessions) -> bridge
catalog (commands for the phase/services) -> SWAN -> LLM
(Groq/Ollama if AUTO_USE_LLM=1) -> static fallback.

Dependency Inversion: runner and selectors are injected.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#strategyengine-__init__) | constructor |  |
| [`register_output`](#strategyengine-register_output) | method | Feed the reactive selector with the last command output. |
| [`next_command`](#strategyengine-next_command) | method | Select the next command for target/phase using the cascade. |

<a id="strategyengine-__init__"></a>

#### `StrategyEngine.__init__`

`constructor` | [skills/autonomous_daemon.py:1279](../../skills/autonomous_daemon.py#L1279)

```python
def __init__(self, runner: ICommandRunner, selectors: list[ICommandSelector] | None = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `runner` | `ICommandRunner` |  |  |
| `selectors` | `list[ICommandSelector] \| None` | `None` |  |

*Calls:* [`CascadeStrategy.__init__`](#cascadestrategy-__init__), [`FallbackSelector`](#fallbackselector), [`LLMSelector`](#llmselector), [`ReactiveSelector.__init__`](#reactiveselector-__init__), [`SWANSelector`](#swanselector), [`UnifiedBrainSelector.__init__`](#unifiedbrainselector-__init__)

*Called by:* [`objective_loop`](#objective_loop)

<a id="strategyengine-register_output"></a>

#### `StrategyEngine.register_output`

`method` | [skills/autonomous_daemon.py:1302](../../skills/autonomous_daemon.py#L1302)

```python
def register_output(self, output: str, command: str, platform: str = 'linux', success: bool = True) -> None
```

Feed the reactive selector with the last command output.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `output` | `str` |  |  |
| `command` | `str` |  |  |
| `platform` | `str` | `'linux'` |  |
| `success` | `bool` | `True` |  |

*Calls:* [`ReactiveSelector.register_output`](#reactiveselector-register_output)

<a id="strategyengine-next_command"></a>

#### `StrategyEngine.next_command`

`method` | [skills/autonomous_daemon.py:1316](../../skills/autonomous_daemon.py#L1316)

```python
def next_command(self, target: str, phase: str, services: list[str] | None = None, os_hint: str = 'unknown', goal: str = '') -> CommandDecision
```

Select the next command for target/phase using the cascade.

``goal`` is the objective text, forwarded so the shared selectors that
act on a named capability (APT actor, adversary profile, MITRE
technique) can read it.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `phase` | `str` |  |  |
| `services` | `list[str] \| None` | `None` |  |
| `os_hint` | `str` | `'unknown'` |  |
| `goal` | `str` | `''` |  |

**Returns:** `CommandDecision`

*Calls:* [`CascadeStrategy.next_command`](#cascadestrategy-next_command)

---

<a id="stepresult"></a>

### `StepResult`

`class` `dataclass` | [skills/autonomous_daemon.py:1342](../../skills/autonomous_daemon.py#L1342)

Decorators: `@dataclass`

```python
class StepResult
```

Result of a single execution step.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`step`](#stepresult-step) | `int` |  |  |
| [`command`](#stepresult-command) | `str` |  |  |
| [`output`](#stepresult-output) | `str` |  |  |
| [`success`](#stepresult-success) | `bool` |  |  |
| [`source`](#stepresult-source) | `str` |  |  |
| [`findings`](#stepresult-findings) | `list[dict]` | `field(default_factory=list)` |  |
| [`phase`](#stepresult-phase) | `str` | `''` |  |

---

<a id="iobjectivehandler"></a>

### `IObjectiveHandler`

`class` `abstract` | [skills/autonomous_daemon.py:1354](../../skills/autonomous_daemon.py#L1354)

```python
class IObjectiveHandler(ABC)
```

Bases: `ABC`

Subclasses: [`ExecutionEngine`](#executionengine)

Contract for running an objective to completion.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`handle`](#iobjectivehandler-handle) | method | Execute objective and return a list of step results. |

<a id="iobjectivehandler-handle"></a>

#### `IObjectiveHandler.handle`

`method` `abstract` | [skills/autonomous_daemon.py:1358](../../skills/autonomous_daemon.py#L1358)

Decorators: `@abstractmethod`

```python
def handle(self, objective_id: str, objective_text: str, target: str, context: dict) -> list[StepResult]
```

Execute objective and return a list of step results.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `objective_id` | `str` |  |  |
| `objective_text` | `str` |  |  |
| `target` | `str` |  |  |
| `context` | `dict` |  |  |

**Returns:** `list[StepResult]`

---

<a id="executionengine"></a>

### `ExecutionEngine`

`class` | [skills/autonomous_daemon.py:1368](../../skills/autonomous_daemon.py#L1368)

```python
class ExecutionEngine(IObjectiveHandler)
```

Bases: [`IObjectiveHandler`](#iobjectivehandler)

Implements the per-objective execution loop.

Selects commands, runs them, parses output, updates world model,
emits events. Equivalent to the former _run_objective coroutine but
encapsulated as a class to satisfy Open/Closed (subclass to override
step logic without modifying this class).

Dependency Inversion: strategy (which wraps runner) is injected.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#executionengine-__init__) | constructor |  |
| [`handle`](#executionengine-handle) | method | Synchronous entry point. |
| [`run_async`](#executionengine-run_async) | method | Asyncio entry point used by objective_loop. |

<a id="executionengine-__init__"></a>

#### `ExecutionEngine.__init__`

`constructor` | [skills/autonomous_daemon.py:1380](../../skills/autonomous_daemon.py#L1380)

```python
def __init__(self, strategy: StrategyEngine, max_steps: int = MAX_STEPS_DEFAULT, world_model: Any = None, obs_parser: Any = None, facts: Any = None, loop: asyncio.AbstractEventLoop | None = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `strategy` | `StrategyEngine` |  |  |
| `max_steps` | `int` | `MAX_STEPS_DEFAULT` |  |
| `world_model` | `Any` | `None` |  |
| `obs_parser` | `Any` | `None` |  |
| `facts` | `Any` | `None` |  |
| `loop` | `asyncio.AbstractEventLoop \| None` | `None` |  |

*Called by:* [`objective_loop`](#objective_loop)

<a id="executionengine-handle"></a>

#### `ExecutionEngine.handle`

`method` | [skills/autonomous_daemon.py:1396](../../skills/autonomous_daemon.py#L1396)

```python
def handle(self, objective_id: str, objective_text: str, target: str, context: dict | None = None) -> list[StepResult]
```

Synchronous entry point.

Delegates to _run_sync.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `objective_id` | `str` |  |  |
| `objective_text` | `str` |  |  |
| `target` | `str` |  |  |
| `context` | `dict \| None` | `None` |  |

**Returns:** `list[StepResult]`

<a id="executionengine-run_async"></a>

#### `ExecutionEngine.run_async`

`method` `async` | [skills/autonomous_daemon.py:1406](../../skills/autonomous_daemon.py#L1406)

```python
async def run_async(self, objective_id: str, objective_text: str, target: str) -> list[StepResult]
```

Asyncio entry point used by objective_loop.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `objective_id` | `str` |  |  |
| `objective_text` | `str` |  |  |
| `target` | `str` |  |  |

**Returns:** `list[StepResult]`

*Called by:* [`objective_loop`](#objective_loop)

---

<a id="dronecoordinator"></a>

### `DroneCoordinator`

`class` | [skills/autonomous_daemon.py:2714](../../skills/autonomous_daemon.py#L2714)

```python
class DroneCoordinator
```

Watches ExecutionEngine results and launches hive drones when events worth parallel analysis are detected: - New host discovered  -> recon drone - Exploitable service  -> exploit drone - Hash/credential      -> cred drone

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#dronecoordinator-__init__) | constructor |  |
| [`process_findings`](#dronecoordinator-process_findings) | method | Launch drones for relevant findings. |

<a id="dronecoordinator-__init__"></a>

#### `DroneCoordinator.__init__`

`constructor` | [skills/autonomous_daemon.py:2723](../../skills/autonomous_daemon.py#L2723)

```python
def __init__(self) -> None
```

*Called by:* [`objective_loop`](#objective_loop)

<a id="dronecoordinator-process_findings"></a>

#### `DroneCoordinator.process_findings`

`method` | [skills/autonomous_daemon.py:2728](../../skills/autonomous_daemon.py#L2728)

```python
def process_findings(self, findings: list[dict], target: str, objective_id: str, payload_key: str = '') -> list[str]
```

Launch drones for relevant findings.

Returns list of drone_ids.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `findings` | `list[dict]` |  |  |
| `target` | `str` |  |  |
| `objective_id` | `str` |  |  |
| `payload_key` | `str` | `''` |  |

**Returns:** `list[str]`

*Called by:* [`objective_loop`](#objective_loop)

---

<a id="enginephasestep"></a>

### `EnginePhaseStep`

`class` `dataclass` | [skills/autonomous_daemon.py:3002](../../skills/autonomous_daemon.py#L3002)

Decorators: `@dataclass(frozen=True)`

```python
class EnginePhaseStep
```

One step in the EngageOrchestrator plan.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`phase`](#enginephasestep-phase) | `str` |  | Canonical engagement phase tag (recon, enum, exploit, ...). |
| [`primary`](#enginephasestep-primary) | `str` |  | Preferred LazyOwn shell command for this step. |
| [`label`](#enginephasestep-label) | `str` |  | Operator-facing short description used by the narrator. |
| [`timeout_s`](#enginephasestep-timeout_s) | `int` | `STEP_TIMEOUT_S` | Per-step execution timeout. Defaults to STEP_TIMEOUT_S. |

---

<a id="enginephaseresult"></a>

### `EnginePhaseResult`

`class` `dataclass` | [skills/autonomous_daemon.py:3019](../../skills/autonomous_daemon.py#L3019)

Decorators: `@dataclass(frozen=True)`

```python
class EnginePhaseResult
```

Result of one EnginePhaseStep execution.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`step`](#enginephaseresult-step) | `EnginePhaseStep` |  |  |
| [`command_used`](#enginephaseresult-command_used) | `str` |  |  |
| [`output`](#enginephaseresult-output) | `str` |  |  |
| [`success`](#enginephaseresult-success) | `bool` |  |  |
| [`switched_from`](#enginephaseresult-switched_from) | `str` | `''` |  |
| [`skipped_reason`](#enginephaseresult-skipped_reason) | `str` | `''` |  |
| [`evidence`](#enginephaseresult-evidence) | `str` | `''` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`did_switch`](#enginephaseresult-did_switch) | property | True when the orchestrator used a fallback tool. |

<a id="enginephaseresult-did_switch"></a>

#### `EnginePhaseResult.did_switch`

`property` | [skills/autonomous_daemon.py:3031](../../skills/autonomous_daemon.py#L3031)

Decorators: `@property`

```python
def did_switch(self) -> bool
```

True when the orchestrator used a fallback tool.

**Returns:** `bool`

---

<a id="itoolfallbackresolver"></a>

### `IToolFallbackResolver`

`class` `abstract` | [skills/autonomous_daemon.py:3036](../../skills/autonomous_daemon.py#L3036)

```python
class IToolFallbackResolver(ABC)
```

Bases: `ABC`

Subclasses: [`BridgeFallbackResolver`](#bridgefallbackresolver), [`StaticFallbackResolver`](#staticfallbackresolver)

Contract for choosing a replacement tool after a failure.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`next_tool`](#itoolfallbackresolver-next_tool) | method | Return the next candidate command or None when exhausted. |

<a id="itoolfallbackresolver-next_tool"></a>

#### `IToolFallbackResolver.next_tool`

`method` `abstract` | [skills/autonomous_daemon.py:3040](../../skills/autonomous_daemon.py#L3040)

Decorators: `@abstractmethod`

```python
def next_tool(self, failed_command: str, phase: str, attempt: int) -> str | None
```

Return the next candidate command or None when exhausted.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `failed_command` | `str` |  |  |
| `phase` | `str` |  |  |
| `attempt` | `int` |  |  |

**Returns:** `str | None`

---

<a id="staticfallbackresolver"></a>

### `StaticFallbackResolver`

`class` | [skills/autonomous_daemon.py:3049](../../skills/autonomous_daemon.py#L3049)

```python
class StaticFallbackResolver(IToolFallbackResolver)
```

Bases: [`IToolFallbackResolver`](#itoolfallbackresolver)

Resolver backed by the static `_TOOL_FALLBACK_MAP`.

Used when the bridge catalog is unavailable (eg the lazyown_bridge
module failed to import). Picks the i-th alternative for the given
primary command, returning None once the list is exhausted.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`next_tool`](#staticfallbackresolver-next_tool) | method | Return the next candidate command or None when exhausted. |

<a id="staticfallbackresolver-next_tool"></a>

#### `StaticFallbackResolver.next_tool`

`method` | [skills/autonomous_daemon.py:3057](../../skills/autonomous_daemon.py#L3057)

```python
def next_tool(self, failed_command: str, phase: str, attempt: int) -> str | None
```

Return the next candidate command or None when exhausted.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `failed_command` | `str` |  |  |
| `phase` | `str` |  |  |
| `attempt` | `int` |  |  |

**Returns:** `str | None`

> **Inherited:** Documentation from [`IToolFallbackResolver.next_tool`](#itoolfallbackresolver-next_tool) (skills/autonomous_daemon.py:3040).

*Called by:* [`BridgeFallbackResolver.next_tool`](#bridgefallbackresolver-next_tool)

---

<a id="bridgefallbackresolver"></a>

### `BridgeFallbackResolver`

`class` | [skills/autonomous_daemon.py:3070](../../skills/autonomous_daemon.py#L3070)

```python
class BridgeFallbackResolver(IToolFallbackResolver)
```

Bases: [`IToolFallbackResolver`](#itoolfallbackresolver)

Resolver that asks the bridge catalog for phase-appropriate alternatives.

Falls back to the static map when the bridge cannot answer, so the
orchestrator always converges instead of stalling. The internal
candidate cache is keyed by (phase, primary) so repeated failures
don't re-query the catalog.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#bridgefallbackresolver-__init__) | constructor |  |
| [`next_tool`](#bridgefallbackresolver-next_tool) | method | Return the next candidate command or None when exhausted. |

<a id="bridgefallbackresolver-__init__"></a>

#### `BridgeFallbackResolver.__init__`

`constructor` | [skills/autonomous_daemon.py:3079](../../skills/autonomous_daemon.py#L3079)

```python
def __init__(self, dispatcher: Any = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `dispatcher` | `Any` | `None` |  |

*Calls:* [`StaticFallbackResolver`](#staticfallbackresolver)

*Called by:* [`EngageOrchestrator.__init__`](#engageorchestrator-__init__)

<a id="bridgefallbackresolver-next_tool"></a>

#### `BridgeFallbackResolver.next_tool`

`method` | [skills/autonomous_daemon.py:3104](../../skills/autonomous_daemon.py#L3104)

```python
def next_tool(self, failed_command: str, phase: str, attempt: int) -> str | None
```

Return the next candidate command or None when exhausted.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `failed_command` | `str` |  |  |
| `phase` | `str` |  |  |
| `attempt` | `int` |  |  |

**Returns:** `str | None`

> **Inherited:** Documentation from [`IToolFallbackResolver.next_tool`](#itoolfallbackresolver-next_tool) (skills/autonomous_daemon.py:3040).

*Calls:* [`StaticFallbackResolver.next_tool`](#staticfallbackresolver-next_tool)

---

<a id="engageorchestrator"></a>

### `EngageOrchestrator`

`class` | [skills/autonomous_daemon.py:3209](../../skills/autonomous_daemon.py#L3209)

```python
class EngageOrchestrator
```

Single-target kill-chain orchestrator backing the ``engage`` verb.

Public usage:
    orch = EngageOrchestrator(target="10.10.11.5")
    summary = orch.run()

The orchestrator never raises. Every error path is logged through the
narrator and reflected in the returned summary so the operator (or the
MCP caller) sees the full timeline.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`DEFAULT_MAX_SWITCHES_PER_STEP`](#engageorchestrator-default_max_switches_per_step) |  | `3` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#engageorchestrator-__init__) | constructor |  |
| [`engagement_id`](#engageorchestrator-engagement_id) | property | Stable id for this engagement (correlates events in logs). |
| [`run`](#engageorchestrator-run) | method | Drive the full plan against the configured target. |

<a id="engageorchestrator-__init__"></a>

#### `EngageOrchestrator.__init__`

`constructor` | [skills/autonomous_daemon.py:3223](../../skills/autonomous_daemon.py#L3223)

```python
def __init__(self, target: str, runner: ICommandRunner | None = None, narrator: Any = None, approval_gate: Any = None, fallback_resolver: IToolFallbackResolver | None = None, shell_detector: _ShellDetector | None = None, plan: tuple[EnginePhaseStep, ...] | None = None, max_switches_per_step: int = DEFAULT_MAX_SWITCHES_PER_STEP, safety_guard: Any = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `runner` | `ICommandRunner \| None` | `None` |  |
| `narrator` | `Any` | `None` |  |
| `approval_gate` | `Any` | `None` |  |
| `fallback_resolver` | `IToolFallbackResolver \| None` | `None` |  |
| `shell_detector` | `_ShellDetector \| None` | `None` |  |
| `plan` | `tuple[EnginePhaseStep, ...] \| None` | `None` |  |
| `max_switches_per_step` | `int` | `DEFAULT_MAX_SWITCHES_PER_STEP` |  |
| `safety_guard` | `Any` | `None` |  |

**Raises**

- `ValueError`: (raised in the body, not documented)

*Calls:* [`BridgeFallbackResolver.__init__`](#bridgefallbackresolver-__init__), [`EnginePhaseStep`](#enginephasestep)

<a id="engageorchestrator-engagement_id"></a>

#### `EngageOrchestrator.engagement_id`

`property` | [skills/autonomous_daemon.py:3268](../../skills/autonomous_daemon.py#L3268)

Decorators: `@property`

```python
def engagement_id(self) -> str
```

Stable id for this engagement (correlates events in logs).

**Returns:** `str`

<a id="engageorchestrator-run"></a>

#### `EngageOrchestrator.run`

`method` | [skills/autonomous_daemon.py:3272](../../skills/autonomous_daemon.py#L3272)

```python
def run(self) -> dict[str, Any]
```

Drive the full plan against the configured target.

Returns a summary dict with the engagement_id, target, per-step
results, switch counts, and the final shell-obtained flag.

**Returns:** `dict[str, Any]`

---

## Functions

<a id="compute_decision_seed"></a>

### `compute_decision_seed`

`function` | [skills/autonomous_daemon.py:395](../../skills/autonomous_daemon.py#L395)

```python
def compute_decision_seed(objective_id: str, step_n: int, source: str) -> str
```

Return a deterministic identifier for a daemon decision.

The seed is the truncated SHA-256 of the tuple
``(objective_id, step_n, source)``. Replay tooling uses it to verify
that the recorded selector chain would still produce the recorded
command when fed the same objective and step counter. A mismatch on
replay is surfaced as a divergence, never as an abort.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `objective_id` | `str` |  | Stable identifier of the parent objective. |
| `step_n` | `int` |  | Zero-indexed step counter inside the objective. |
| `source` | `str` |  | Name of the selector that produced the decision. |

**Returns:** `str` - Hex digest truncated to [`DECISION_SEED_LENGTH`](#decision_seed_length) characters.

---

<a id="mcp_engage_target"></a>

### `mcp_engage_target`

`function` | [skills/autonomous_daemon.py:3916](../../skills/autonomous_daemon.py#L3916)

```python
def mcp_engage_target(target: str, max_switches_per_step: int = 3, detach: bool = True, auto: bool = False) -> str
```

Public MCP / CLI entry point for the engage verb.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  | IPv4 dotted-quad or hostname to engage. |
| `max_switches_per_step` | `int` | `3` | Maximum number of fallback tools per phase. |
| `detach` | `bool` | `True` | When True (default) the orchestrator runs in a background thread and the call returns immediately with the engagement id; the operator polls progress via lazyown_engage_status. When False the call blocks until the kill-chain finishes and returns the full summary JSON. |
| `auto` | `bool` | `False` | When True the engagement runs fully unattended. Approval is delegated to a `[`ScopeBoundAutoGate`](skills.lazyown_policy.py.md#scopeboundautogate)` that never prompts a human: it approves in-scope steps, denies out-of-scope steps when `[`scope_enforcement`](lazyown.py.md#lazyownshell-scope_enforcement)` is ``enforce`` (the single fail-closed safety boundary), and a client-ready report is generated when the run finishes. |

**Returns:** `str` - JSON string with `[`engagement_id`](#engageorchestrator-engagement_id)` and ``status`` (started|done)
plus the full result payload when detach is False.

*Called by:* [`cmd_engage`](#cmd_engage)

---

<a id="mcp_engage_status"></a>

### `mcp_engage_status`

`function` | [skills/autonomous_daemon.py:4006](../../skills/autonomous_daemon.py#L4006)

```python
def mcp_engage_status(last_n: int = 20) -> str
```

Return the last N lines of sessions/engagement.log plus pending approvals.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `last_n` | `int` | `20` |  |

**Returns:** `str`

*Calls:* [`list_pending_approvals`](modules.engagement_hooks.py.md#list_pending_approvals)

---

<a id="mcp_engage_approve"></a>

### `mcp_engage_approve`

`function` | [skills/autonomous_daemon.py:4032](../../skills/autonomous_daemon.py#L4032)

```python
def mcp_engage_approve(approval_id: str, decision: str, operator: str = '') -> str
```

Resolve a pending approval. decision must be 'approved' or 'denied'.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `approval_id` | `str` |  |  |
| `decision` | `str` |  |  |
| `operator` | `str` | `''` |  |

**Returns:** `str`

*Calls:* [`resolve_approval`](modules.engagement_hooks.py.md#resolve_approval)

---

<a id="mcp_engage_list_pending"></a>

### `mcp_engage_list_pending`

`function` | [skills/autonomous_daemon.py:4057](../../skills/autonomous_daemon.py#L4057)

```python
def mcp_engage_list_pending() -> str
```

List every pending approval awaiting an operator decision.

**Returns:** `str`

*Calls:* [`list_pending_approvals`](modules.engagement_hooks.py.md#list_pending_approvals)

---

<a id="cmd_engage"></a>

### `cmd_engage`

`function` | [skills/autonomous_daemon.py:4075](../../skills/autonomous_daemon.py#L4075)

```python
def cmd_engage(target: str, max_switches_per_step: int = 3, detach: bool = False) -> None
```

CLI helper bound to the `engage <ip>` daemon subcommand.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  |  |
| `max_switches_per_step` | `int` | `3` |  |
| `detach` | `bool` | `False` |  |

*Calls:* [`mcp_engage_target`](#mcp_engage_target)

---

<a id="objective_loop"></a>

### `objective_loop`

`function` `async` | [skills/autonomous_daemon.py:4151](../../skills/autonomous_daemon.py#L4151)

```python
async def objective_loop(max_steps: int, loop: asyncio.AbstractEventLoop) -> None
```

Root autonomous loop: takes pending objectives from objectives.jsonl and executes them without waiting for Claude input between objectives.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `max_steps` | `int` |  |  |
| `loop` | `asyncio.AbstractEventLoop` |  |  |

*Calls:* [`DroneCoordinator.__init__`](#dronecoordinator-__init__), [`DroneCoordinator.process_findings`](#dronecoordinator-process_findings), [`ExecutionEngine.__init__`](#executionengine-__init__), [`ExecutionEngine.run_async`](#executionengine-run_async), [`StrategyEngine.__init__`](#strategyengine-__init__)

---

<a id="world_model_watcher"></a>

### `world_model_watcher`

`function` `async` | [skills/autonomous_daemon.py:4298](../../skills/autonomous_daemon.py#L4298)

```python
async def world_model_watcher(loop: asyncio.AbstractEventLoop) -> None
```

Watch world_model.json.

When the phase changes, new hosts appear, new service versions are found, or active beacons are detected, auto-inject derived objectives.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `loop` | `asyncio.AbstractEventLoop` |  |  |

*Calls:* [`read_state_dict`](modules.world_model.py.md#read_state_dict)

---

<a id="heartbeat_loop"></a>

### `heartbeat_loop`

`function` `async` | [skills/autonomous_daemon.py:4491](../../skills/autonomous_daemon.py#L4491)

```python
async def heartbeat_loop() -> None
```

Emit heartbeat and write status every HEARTBEAT_S seconds.

---

<a id="cmd_run"></a>

### `cmd_run`

`function` | [skills/autonomous_daemon.py:4618](../../skills/autonomous_daemon.py#L4618)

```python
def cmd_run(max_steps: int = MAX_STEPS_DEFAULT) -> None
```

Run daemon in foreground (debug mode).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `max_steps` | `int` | `MAX_STEPS_DEFAULT` |  |

---

<a id="cmd_start"></a>

### `cmd_start`

`function` | [skills/autonomous_daemon.py:4627](../../skills/autonomous_daemon.py#L4627)

```python
def cmd_start(max_steps: int = MAX_STEPS_DEFAULT) -> None
```

Fork, detach, and run daemon in background.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `max_steps` | `int` | `MAX_STEPS_DEFAULT` |  |

---

<a id="cmd_stop"></a>

### `cmd_stop`

`function` | [skills/autonomous_daemon.py:4657](../../skills/autonomous_daemon.py#L4657)

```python
def cmd_stop() -> None
```

Send SIGTERM to the running daemon.

---

<a id="cmd_status"></a>

### `cmd_status`

`function` | [skills/autonomous_daemon.py:4674](../../skills/autonomous_daemon.py#L4674)

```python
def cmd_status() -> None
```

Print current daemon status to stdout.

---

<a id="cmd_inject"></a>

### `cmd_inject`

`function` | [skills/autonomous_daemon.py:4690](../../skills/autonomous_daemon.py#L4690)

```python
def cmd_inject(text: str, priority: str = 'high') -> None
```

Inject an objective from the CLI, split into verifiable sub-goals.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `text` | `str` |  |  |
| `priority` | `str` | `'high'` |  |

---

<a id="mcp_autonomous_start"></a>

### `mcp_autonomous_start`

`function` | [skills/autonomous_daemon.py:4724](../../skills/autonomous_daemon.py#L4724)

```python
def mcp_autonomous_start(max_steps: int = MAX_STEPS_DEFAULT, backend: str = HIVE_BACKEND) -> str
```

Start the autonomous daemon in a background thread (for MCP calls).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `max_steps` | `int` | `MAX_STEPS_DEFAULT` |  |
| `backend` | `str` | `HIVE_BACKEND` |  |

**Returns:** `str`

---

<a id="mcp_autonomous_stop"></a>

### `mcp_autonomous_stop`

`function` | [skills/autonomous_daemon.py:4766](../../skills/autonomous_daemon.py#L4766)

```python
def mcp_autonomous_stop() -> str
```

Stop the autonomous daemon.

**Returns:** `str`

---

<a id="mcp_autonomous_status"></a>

### `mcp_autonomous_status`

`function` | [skills/autonomous_daemon.py:4782](../../skills/autonomous_daemon.py#L4782)

```python
def mcp_autonomous_status() -> str
```

Current daemon state: objectives, steps, drones, phase.

**Returns:** `str`

---

<a id="mcp_autonomous_inject"></a>

### `mcp_autonomous_inject`

`function` | [skills/autonomous_daemon.py:4795](../../skills/autonomous_daemon.py#L4795)

```python
def mcp_autonomous_inject(text: str, priority: str = 'high', target: str = '') -> str
```

Inject an objective into the daemon queue and into sessions/tasks.json.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `text` | `str` |  |  |
| `priority` | `str` | `'high'` |  |
| `target` | `str` | `''` |  |

**Returns:** `str`

---

<a id="mcp_autonomous_events"></a>

### `mcp_autonomous_events`

`function` | [skills/autonomous_daemon.py:4839](../../skills/autonomous_daemon.py#L4839)

```python
def mcp_autonomous_events(last_n: int = 20) -> str
```

Read the last N events from autonomous_events.jsonl.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `last_n` | `int` | `20` |  |

**Returns:** `str`

---

## Constants

<a id="skills_dir"></a>

### `SKILLS_DIR`

`constant` | [skills/autonomous_daemon.py:72](../../skills/autonomous_daemon.py#L72)

```python
SKILLS_DIR = Path(__file__).parent
```

---

<a id="lazyown_dir"></a>

### `LAZYOWN_DIR`

`constant` | [skills/autonomous_daemon.py:73](../../skills/autonomous_daemon.py#L73)

```python
LAZYOWN_DIR = Path(os.environ.get('LAZYOWN_DIR', str(SKILLS_DIR.parent)))
```

---

<a id="modules_dir"></a>

### `MODULES_DIR`

`constant` | [skills/autonomous_daemon.py:74](../../skills/autonomous_daemon.py#L74)

```python
MODULES_DIR = LAZYOWN_DIR / 'modules'
```

---

<a id="sessions_dir"></a>

### `SESSIONS_DIR`

`constant` | [skills/autonomous_daemon.py:75](../../skills/autonomous_daemon.py#L75)

```python
SESSIONS_DIR = LAZYOWN_DIR / 'sessions'
```

---

<a id="payload_file"></a>

### `PAYLOAD_FILE`

`constant` | [skills/autonomous_daemon.py:76](../../skills/autonomous_daemon.py#L76)

```python
PAYLOAD_FILE = LAZYOWN_DIR / 'payload.json'
```

---

<a id="pid_file"></a>

### `PID_FILE`

`constant` | [skills/autonomous_daemon.py:84](../../skills/autonomous_daemon.py#L84)

```python
PID_FILE = SESSIONS_DIR / 'autonomous_daemon.pid'
```

---

<a id="status_file"></a>

### `STATUS_FILE`

`constant` | [skills/autonomous_daemon.py:85](../../skills/autonomous_daemon.py#L85)

```python
STATUS_FILE = SESSIONS_DIR / 'autonomous_status.json'
```

---

<a id="events_file"></a>

### `EVENTS_FILE`

`constant` | [skills/autonomous_daemon.py:86](../../skills/autonomous_daemon.py#L86)

```python
EVENTS_FILE = SESSIONS_DIR / 'autonomous_events.jsonl'
```

---

<a id="tasks_file"></a>

### `TASKS_FILE`

`constant` | [skills/autonomous_daemon.py:87](../../skills/autonomous_daemon.py#L87)

```python
TASKS_FILE = SESSIONS_DIR / 'tasks.json'
```

---

<a id="obj_poll_s"></a>

### `OBJ_POLL_S`

`constant` | [skills/autonomous_daemon.py:103](../../skills/autonomous_daemon.py#L103)

```python
OBJ_POLL_S = float(os.environ.get('AUTO_OBJ_POLL', '5'))
```

---

<a id="wm_poll_s"></a>

### `WM_POLL_S`

`constant` | [skills/autonomous_daemon.py:104](../../skills/autonomous_daemon.py#L104)

```python
WM_POLL_S = float(os.environ.get('AUTO_WM_POLL', '8'))
```

---

<a id="step_timeout_s"></a>

### `STEP_TIMEOUT_S`

`constant` | [skills/autonomous_daemon.py:105](../../skills/autonomous_daemon.py#L105)

```python
STEP_TIMEOUT_S = int(os.environ.get('AUTO_STEP_TIMEOUT', '60'))
```

---

<a id="step_delay_s"></a>

### `STEP_DELAY_S`

`constant` | [skills/autonomous_daemon.py:106](../../skills/autonomous_daemon.py#L106)

```python
STEP_DELAY_S = float(os.environ.get('AUTO_STEP_DELAY', '3'))
```

---

<a id="max_steps_default"></a>

### `MAX_STEPS_DEFAULT`

`constant` | [skills/autonomous_daemon.py:107](../../skills/autonomous_daemon.py#L107)

```python
MAX_STEPS_DEFAULT = int(os.environ.get('AUTO_MAX_STEPS', '10'))
```

---

<a id="max_fails_per_cmd"></a>

### `MAX_FAILS_PER_CMD`

`constant` | [skills/autonomous_daemon.py:108](../../skills/autonomous_daemon.py#L108)

```python
MAX_FAILS_PER_CMD = int(os.environ.get('AUTO_MAX_FAILS', '2'))
```

---

<a id="hive_backend"></a>

### `HIVE_BACKEND`

`constant` | [skills/autonomous_daemon.py:109](../../skills/autonomous_daemon.py#L109)

```python
HIVE_BACKEND = os.environ.get('AUTO_HIVE_BACKEND', 'groq')
```

---

<a id="hive_max_iter"></a>

### `HIVE_MAX_ITER`

`constant` | [skills/autonomous_daemon.py:110](../../skills/autonomous_daemon.py#L110)

```python
HIVE_MAX_ITER = int(os.environ.get('AUTO_HIVE_MAX_ITER', '8'))
```

---

<a id="heartbeat_s"></a>

### `HEARTBEAT_S`

`constant` | [skills/autonomous_daemon.py:111](../../skills/autonomous_daemon.py#L111)

```python
HEARTBEAT_S = float(os.environ.get('AUTO_HEARTBEAT', '30'))
```

---

<a id="blocked_escalate_n"></a>

### `BLOCKED_ESCALATE_N`

`constant` | [skills/autonomous_daemon.py:112](../../skills/autonomous_daemon.py#L112)

```python
BLOCKED_ESCALATE_N = int(os.environ.get('AUTO_BLOCKED_ESCALATE', '2'))
```

---

<a id="control_veto_max_retries"></a>

### `CONTROL_VETO_MAX_RETRIES`

`constant` | [skills/autonomous_daemon.py:113](../../skills/autonomous_daemon.py#L113)

```python
CONTROL_VETO_MAX_RETRIES = int(os.environ.get('AUTO_VETO_RETRIES', '3'))
```

---

<a id="control_approval_ttl_s"></a>

### `CONTROL_APPROVAL_TTL_S`

`constant` | [skills/autonomous_daemon.py:114](../../skills/autonomous_daemon.py#L114)

```python
CONTROL_APPROVAL_TTL_S = float(os.environ.get('AUTO_APPROVAL_TTL', '30'))
```

---

<a id="control_pause_poll_s"></a>

### `CONTROL_PAUSE_POLL_S`

`constant` | [skills/autonomous_daemon.py:115](../../skills/autonomous_daemon.py#L115)

```python
CONTROL_PAUSE_POLL_S = float(os.environ.get('AUTO_PAUSE_POLL', '1'))
```

---

<a id="control_pause_max_s"></a>

### `CONTROL_PAUSE_MAX_S`

`constant` | [skills/autonomous_daemon.py:116](../../skills/autonomous_daemon.py#L116)

```python
CONTROL_PAUSE_MAX_S = float(os.environ.get('AUTO_PAUSE_MAX', '3600'))
```

---

<a id="metrics_bias_enabled"></a>

### `METRICS_BIAS_ENABLED`

`constant` | [skills/autonomous_daemon.py:118](../../skills/autonomous_daemon.py#L118)

```python
METRICS_BIAS_ENABLED
```

---

<a id="metrics_bias_window_s"></a>

### `METRICS_BIAS_WINDOW_S`

`constant` | [skills/autonomous_daemon.py:120](../../skills/autonomous_daemon.py#L120)

```python
METRICS_BIAS_WINDOW_S = int(os.environ.get('AUTO_METRICS_WINDOW_S', '1800'))
```

---

<a id="metrics_bias_min_success"></a>

### `METRICS_BIAS_MIN_SUCCESS`

`constant` | [skills/autonomous_daemon.py:121](../../skills/autonomous_daemon.py#L121)

```python
METRICS_BIAS_MIN_SUCCESS = float(os.environ.get('AUTO_METRICS_MIN_SUCCESS', '0.25'))
```

---

<a id="metrics_bias_min_attempts"></a>

### `METRICS_BIAS_MIN_ATTEMPTS`

`constant` | [skills/autonomous_daemon.py:122](../../skills/autonomous_daemon.py#L122)

```python
METRICS_BIAS_MIN_ATTEMPTS = int(os.environ.get('AUTO_METRICS_MIN_ATTEMPTS', '3'))
```

---

<a id="metrics_bias_cache_ttl_s"></a>

### `METRICS_BIAS_CACHE_TTL_S`

`constant` | [skills/autonomous_daemon.py:123](../../skills/autonomous_daemon.py#L123)

```python
METRICS_BIAS_CACHE_TTL_S = float(os.environ.get('AUTO_METRICS_CACHE_TTL_S', '5'))
```

---

<a id="decision_seed_length"></a>

### `DECISION_SEED_LENGTH`

`constant` | [skills/autonomous_daemon.py:310](../../skills/autonomous_daemon.py#L310)

```python
DECISION_SEED_LENGTH: int = 16
```

---

<a id="reward_display_precision"></a>

### `REWARD_DISPLAY_PRECISION`

`constant` | [skills/autonomous_daemon.py:311](../../skills/autonomous_daemon.py#L311)

```python
REWARD_DISPLAY_PRECISION: int = 3
```

---
