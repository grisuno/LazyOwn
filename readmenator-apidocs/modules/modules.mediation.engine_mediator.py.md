# `modules.mediation.engine_mediator`

> Source: [modules/mediation/engine_mediator.py:1](../../modules/mediation/engine_mediator.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Engine mediator: the loop's single coordination point to the engines.

Domain ``loop.engines``. The unified autonomous loop (`[`LazyLoopEngine`](modules.lazy_loop.py.md#lazyloopengine)`)
and the CLI/MCP exploit surfaces used to import the exploit engines
directly (`[`modules.autonomous_exploit_engine`](modules.autonomous_exploit_engine.py.md)`,
`[`modules.reactive_engine`](modules.reactive_engine.py.md)`, `[`modules.ai_exploit_chain`](modules.ai_exploit_chain.py.md)`), which couples
the loop god file to every engine implementation. This mediator owns that
edge instead: consumers ask for a port, the mediator lazily resolves the
concrete engine at call time, so monkeypatching an engine stays effective
and import cycles die.

Ports:

- [`ExploitRetryPort`](#exploitretryport) — feed captured credentials back into the
  autonomous exploit engine's retry queue (credential reuse).
- [`ReactionPort`](#reactionport) — reactive-engine analysis of step output into
  next-action decisions.
- [`ReasoningPort`](#reasoningport) — exploit-chain strategy reasoning (direct,
  brute-force, path-traversal, ...) over a target profile.

Failure semantics: every port call degrades to a no-op answer (empty
list, empty string) when its engine import fails, so a missing engine
never breaks the loop round.

## Contents

- **Classes:** [`EngineMediator`](#enginemediator)
- **Protocols:** [`ExploitRetryPort`](#exploitretryport), [`ReactionPort`](#reactionport), [`ReasoningPort`](#reasoningport)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class ExploitRetryPort
    <<protocol>> ExploitRetryPort
    ExploitRetryPort : retry_with_credentials()
    class ReactionPort
    <<protocol>> ReactionPort
    ReactionPort : analyse()
    class ReasoningPort
    <<protocol>> ReasoningPort
    ReasoningPort : reason()
    class EngineMediator
    EngineMediator : domain
    EngineMediator : describe()
    EngineMediator : retry_with_credentials()
    EngineMediator : analyse()
    EngineMediator : reason()
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_mediation_engine_mediator_py__EngineMediator_retry_with_credentials(["EngineMediator.retry_with_credentials"])
    n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_get_instance["autonomous_exploit_engine.AutonomousExploitEngine.get_instance"]
    n_modules_mediation_engine_mediator_py__EngineMediator_analyse(["EngineMediator.analyse"])
    n_modules_reactive_engine_py__get_engine["reactive_engine.get_engine"]
    n_modules_mediation_engine_mediator_py__EngineMediator_reason(["EngineMediator.reason"])
    n_modules_ai_exploit_chain_py__AIExploitChainer___init__["ai_exploit_chain.AIExploitChainer.__init__"]
    n_modules_ai_exploit_chain_py__AIExploitChainer_build_chain_plan["ai_exploit_chain.AIExploitChainer.build_chain_plan"]
    n_modules_ai_exploit_chain_py__AIExploitChainer_reason["ai_exploit_chain.AIExploitChainer.reason"]
    n_modules_ai_exploit_chain_py__ExploitChainContext["ai_exploit_chain.ExploitChainContext"]
    n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine___init__["autonomous_exploit_engine.AutonomousExploitEngine.__init__"]
    n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_profile["autonomous_exploit_engine.AutonomousExploitEngine.profile"]
    n_modules_mediation_engine_mediator_py__EngineMediator_retry_with_credentials -.-> n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_get_instance
    n_modules_mediation_engine_mediator_py__EngineMediator_analyse -.-> n_modules_reactive_engine_py__get_engine
    n_modules_mediation_engine_mediator_py__EngineMediator_reason -.-> n_modules_ai_exploit_chain_py__AIExploitChainer___init__
    n_modules_mediation_engine_mediator_py__EngineMediator_reason -.-> n_modules_ai_exploit_chain_py__AIExploitChainer_build_chain_plan
    n_modules_mediation_engine_mediator_py__EngineMediator_reason -.-> n_modules_ai_exploit_chain_py__AIExploitChainer_reason
    n_modules_mediation_engine_mediator_py__EngineMediator_reason -.-> n_modules_ai_exploit_chain_py__ExploitChainContext
    n_modules_mediation_engine_mediator_py__EngineMediator_reason -.-> n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine___init__
    n_modules_mediation_engine_mediator_py__EngineMediator_reason -.-> n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_profile
```

## Classes

<a id="enginemediator"></a>

### `EngineMediator`

`class` | [modules/mediation/engine_mediator.py:84](../../modules/mediation/engine_mediator.py#L84)

```python
class EngineMediator
```

Mediate engine access for the autonomous loop and CLI surfaces.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`domain`](#enginemediator-domain) |  | `'loop.engines'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`describe`](#enginemediator-describe) | method | Return introspection metadata for diagnostics. |
| [`retry_with_credentials`](#enginemediator-retry_with_credentials) | method | Queue captured credentials into the exploit engine's retry loop. |
| [`analyse`](#enginemediator-analyse) | method | Run reactive-engine analysis over one step's output. |
| [`reason`](#enginemediator-reason) | method | Return the exploit-chain strategy for a target. |

<a id="enginemediator-describe"></a>

#### `EngineMediator.describe`

`method` | [modules/mediation/engine_mediator.py:89](../../modules/mediation/engine_mediator.py#L89)

```python
def describe(self) -> dict[str, Any]
```

Return introspection metadata for diagnostics.

**Returns:** `dict[str, Any]`

<a id="enginemediator-retry_with_credentials"></a>

#### `EngineMediator.retry_with_credentials`

`method` | [modules/mediation/engine_mediator.py:97](../../modules/mediation/engine_mediator.py#L97)

```python
def retry_with_credentials(self, target: str, credentials: list[dict]) -> int
```

Queue captured credentials into the exploit engine's retry loop.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  | Host the credentials were captured from. |
| `credentials` | `list[dict]` |  | Credential dicts from the reaction bridge. |

**Returns:** `int` - Attempts queued, or 0 when the engine is unavailable.

*Calls:* [`AutonomousExploitEngine.get_instance`](modules.autonomous_exploit_engine.py.md#autonomousexploitengine-get_instance)

<a id="enginemediator-analyse"></a>

#### `EngineMediator.analyse`

`method` | [modules/mediation/engine_mediator.py:118](../../modules/mediation/engine_mediator.py#L118)

```python
def analyse(self, output: str, command: str, platform: str) -> list[Any]
```

Run reactive-engine analysis over one step's output.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `output` | `str` |  | Captured output of the executed command. |
| `command` | `str` |  | Command line that produced the output. |
| `platform` | `str` |  | Target platform hint for decision scoping. |

**Returns:** `list[Any]` - Decision objects, or an empty list when unavailable.

*Calls:* [`get_engine`](modules.reactive_engine.py.md#get_engine)

<a id="enginemediator-reason"></a>

#### `EngineMediator.reason`

`method` | [modules/mediation/engine_mediator.py:136](../../modules/mediation/engine_mediator.py#L136)

```python
def reason(self, target: str) -> Any
```

Return the exploit-chain strategy for a target.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  | Host under test. |

**Returns:** `Any` - The chainer's strategy decision, or None when unavailable.

*Calls:* [`AIExploitChainer.__init__`](modules.ai_exploit_chain.py.md#aiexploitchainer-__init__), [`AIExploitChainer.build_chain_plan`](modules.ai_exploit_chain.py.md#aiexploitchainer-build_chain_plan), [`AIExploitChainer.reason`](modules.ai_exploit_chain.py.md#aiexploitchainer-reason), [`ExploitChainContext`](modules.ai_exploit_chain.py.md#exploitchaincontext), [`AutonomousExploitEngine.__init__`](modules.autonomous_exploit_engine.py.md#autonomousexploitengine-__init__), [`AutonomousExploitEngine.profile`](modules.autonomous_exploit_engine.py.md#autonomousexploitengine-profile)

---

## Protocols

<a id="exploitretryport"></a>

### `ExploitRetryPort`

`protocol` | [modules/mediation/engine_mediator.py:34](../../modules/mediation/engine_mediator.py#L34)

Decorators: `@runtime_checkable`

```python
class ExploitRetryPort(Protocol)
```

Bases: `Protocol`

Request-port for credential reuse through the exploit engine.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`retry_with_credentials`](#exploitretryport-retry_with_credentials) | method | Queue one retry attempt per captured credential pair. |

<a id="exploitretryport-retry_with_credentials"></a>

#### `ExploitRetryPort.retry_with_credentials`

`method` | [modules/mediation/engine_mediator.py:37](../../modules/mediation/engine_mediator.py#L37)

```python
def retry_with_credentials(self, target: str, credentials: list[dict]) -> int
```

Queue one retry attempt per captured credential pair.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  | Host the credentials were captured from. |
| `credentials` | `list[dict]` |  | Captured credential dicts. |

**Returns:** `int` - Number of attempts queued; 0 when the engine is unavailable.

---

<a id="reactionport"></a>

### `ReactionPort`

`protocol` | [modules/mediation/engine_mediator.py:51](../../modules/mediation/engine_mediator.py#L51)

Decorators: `@runtime_checkable`

```python
class ReactionPort(Protocol)
```

Bases: `Protocol`

Request-port for reactive decision analysis.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`analyse`](#reactionport-analyse) | method | Analyse one command's output for next-action decisions. |

<a id="reactionport-analyse"></a>

#### `ReactionPort.analyse`

`method` | [modules/mediation/engine_mediator.py:54](../../modules/mediation/engine_mediator.py#L54)

```python
def analyse(self, output: str, command: str, platform: str) -> list[Any]
```

Analyse one command's output for next-action decisions.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `output` | `str` |  | Captured command output. |
| `command` | `str` |  | The command that produced it. |
| `platform` | `str` |  | Target platform hint. |

**Returns:** `list[Any]` - Decision objects; empty when the engine is unavailable.

---

<a id="reasoningport"></a>

### `ReasoningPort`

`protocol` | [modules/mediation/engine_mediator.py:69](../../modules/mediation/engine_mediator.py#L69)

Decorators: `@runtime_checkable`

```python
class ReasoningPort(Protocol)
```

Bases: `Protocol`

Request-port for exploit-chain strategy reasoning.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`reason`](#reasoningport-reason) | method | Return the next exploit strategy for a target. |

<a id="reasoningport-reason"></a>

#### `ReasoningPort.reason`

`method` | [modules/mediation/engine_mediator.py:72](../../modules/mediation/engine_mediator.py#L72)

```python
def reason(self, target: str) -> Any
```

Return the next exploit strategy for a target.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  | Host under test. |

**Returns:** `Any` - The strategy decision, or None when unavailable.

---
