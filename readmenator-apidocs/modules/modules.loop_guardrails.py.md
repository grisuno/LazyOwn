# `modules.loop_guardrails`

> Source: [modules/loop_guardrails.py:1](../../modules/loop_guardrails.py#L1) | language `py` | coverage 93.1% | [API index](../index.md)

Adaptive guardrails for the autonomous loop.

Four independent primitives, one contract each:

- [`RepeatDetector`](#repeatdetector): sliding window over the last executed
  commands; `[`stuck`](#repeatdetector-stuck)` flips when the window fills with identical
  commands, which is the operator-visible signal that the planner is
  going in circles.
- [`EdrPacer`](#edrpacer): observes per-command duration and output
  anomalies (high latency, connection resets, timeouts) and estimates
  a defense-telemetry level. At higher levels the loop inserts random
  inter-step sleeps and downgrades noisy verbs to quieter variants
  instead of burning bandwidth and blue-team attention.
- [`TargetLimiter`](#targetlimiter): semaphore that caps how many distinct
  targets the loop attacks simultaneously; per-thread re-entrant so a
  worker touching one target across many steps never self-deadlocks.
- [`FactVectorStore`](#factvectorstore): stdlib TF-IDF vector memory. Facts
  (command plus output digests) are embedded on write and retrieved by
  cosine similarity so the LLM context carries only the facts relevant
  to the current query instead of the whole transcript.

All four are persistence-friendly, exception-tolerant and safe to call
from worker threads.

## Contents

- **Classes:** [`RepeatDetector`](#repeatdetector), [`EdrPacer`](#edrpacer), [`TargetLimiter`](#targetlimiter), [`FactVectorStore`](#factvectorstore)
- **Constants:** [`DEFAULT_REPEAT_WINDOW`](#default_repeat_window), [`DEFAULT_TARGET_LIMIT`](#default_target_limit)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class RepeatDetector
    RepeatDetector : __init__()
    RepeatDetector : record()
    RepeatDetector : stuck()
    RepeatDetector : oscillation_pair()
    RepeatDetector : last_commands()
    RepeatDetector : reset()
    class EdrPacer
    EdrPacer : __init__()
    EdrPacer : observe()
    EdrPacer : decay()
    EdrPacer : level()
    EdrPacer : signal()
    EdrPacer : inter_step_delay()
    EdrPacer : quieten()
    class TargetLimiter
    TargetLimiter : __init__()
    TargetLimiter : max_concurrent()
    TargetLimiter : active_targets()
    TargetLimiter : slot()
    class FactVectorStore
    FactVectorStore : __init__()
    FactVectorStore : path()
    FactVectorStore : add()
    FactVectorStore : search()
    FactVectorStore : search_block()
    FactVectorStore : clear()
    FactVectorStore : save()
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_loop_guardrails_py__FactVectorStore_add(["FactVectorStore.add"])
    n_modules_loop_guardrails_py__FactVectorStore_save(["FactVectorStore.save"])
    n_modules_loop_guardrails_py__FactVectorStore_search_block(["FactVectorStore.search_block"])
    n_modules_loop_guardrails_py__FactVectorStore_search(["FactVectorStore.search"])
    n_modules_loop_guardrails_py__FactVectorStore_clear(["FactVectorStore.clear"])
    n_modules_loop_guardrails_py__FactVectorStore_add --> n_modules_loop_guardrails_py__FactVectorStore_save
    n_modules_loop_guardrails_py__FactVectorStore_search_block --> n_modules_loop_guardrails_py__FactVectorStore_search
    n_modules_loop_guardrails_py__FactVectorStore_clear --> n_modules_loop_guardrails_py__FactVectorStore_save
```

## Classes

<a id="repeatdetector"></a>

### `RepeatDetector`

`class` | [modules/loop_guardrails.py:82](../../modules/loop_guardrails.py#L82)

```python
class RepeatDetector
```

Sliding-window detector for identical and alternating repeats.

Two stuck-loop shapes are recognised:

- AAAA: every command in the window is identical.
- ABABAB: the window alternates between exactly two commands with at
  least two repetitions each, the oscillation the legacy loop vetoed.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `window` |  |  | How many recent commands to watch (minimum 6 for the alternating pattern). |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#repeatdetector-__init__) | constructor |  |
| [`record`](#repeatdetector-record) | method | Add one executed command; returns True when the window fills. |
| [`stuck`](#repeatdetector-stuck) | property | True when the loop is visibly not progressing. |
| [`oscillation_pair`](#repeatdetector-oscillation_pair) | method | Return the detected alternating pair, ('', '') when none. |
| [`last_commands`](#repeatdetector-last_commands) | method | Snapshot of the recent command window (oldest first). |
| [`reset`](#repeatdetector-reset) | method | Clear the window (operator intervention acknowledged). |

<a id="repeatdetector-__init__"></a>

#### `RepeatDetector.__init__`

`constructor` | [modules/loop_guardrails.py:98](../../modules/loop_guardrails.py#L98)

```python
def __init__(self, window: int = DEFAULT_REPEAT_WINDOW) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `window` | `int` | `DEFAULT_REPEAT_WINDOW` | How many recent commands to watch (minimum 6 for the alternating pattern). |

*Called by:* [`Worker.__init__`](modules.lazy_loop.py.md#worker-__init__)

<a id="repeatdetector-record"></a>

#### `RepeatDetector.record`

`method` | [modules/loop_guardrails.py:104](../../modules/loop_guardrails.py#L104)

```python
def record(self, command: str) -> bool
```

Add one executed command; returns True when the window fills.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  | Exact command line as executed. |

**Returns:** `bool` - True when a stuck-loop shape fills the window.

*Called by:* [`Worker.execute`](modules.lazy_loop.py.md#worker-execute)

<a id="repeatdetector-stuck"></a>

#### `RepeatDetector.stuck`

`property` | [modules/loop_guardrails.py:139](../../modules/loop_guardrails.py#L139)

Decorators: `@property`

```python
def stuck(self) -> bool
```

True when the loop is visibly not progressing.

Either the window is all one identical command (AAAA), or the
window is at least `_OSCILLATION_MIN` long and holds
exactly two commands alternating (ABABAB).

**Returns:** `bool`

<a id="repeatdetector-oscillation_pair"></a>

#### `RepeatDetector.oscillation_pair`

`method` | [modules/loop_guardrails.py:163](../../modules/loop_guardrails.py#L163)

```python
def oscillation_pair(self) -> tuple[str, str]
```

Return the detected alternating pair, ('', '') when none.

**Returns:** `tuple[str, str]`

<a id="repeatdetector-last_commands"></a>

#### `RepeatDetector.last_commands`

`method` | [modules/loop_guardrails.py:167](../../modules/loop_guardrails.py#L167)

```python
def last_commands(self) -> list[str]
```

Snapshot of the recent command window (oldest first).

**Returns:** `list[str]`

*Called by:* [`Worker.execute`](modules.lazy_loop.py.md#worker-execute)

<a id="repeatdetector-reset"></a>

#### `RepeatDetector.reset`

`method` | [modules/loop_guardrails.py:171](../../modules/loop_guardrails.py#L171)

```python
def reset(self) -> None
```

Clear the window (operator intervention acknowledged).

---

<a id="edrpacer"></a>

### `EdrPacer`

`class` | [modules/loop_guardrails.py:178](../../modules/loop_guardrails.py#L178)

```python
class EdrPacer
```

Defense-aware pacing driven by observed execution anomalies.

The pacer never blocks by itself: it only recommends. `[`observe`](#edrpacer-observe)`
feeds one executed command with its wall-clock duration and output;
the internal score decays over time so a single anomaly does not
permanently slow the loop.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#edrpacer-__init__) | constructor |  |
| [`observe`](#edrpacer-observe) | method | Feed one executed step and update the telemetry estimate. |
| [`decay`](#edrpacer-decay) | method | Cool the estimate down (call once per completed step). |
| [`level`](#edrpacer-level) | property | Current pacing level: 0 calm, 1 cautious, 2 stealth. |
| [`signal`](#edrpacer-signal) | property | Human-readable reason for the current level (may be empty). |
| [`inter_step_delay`](#edrpacer-inter_step_delay) | method | Recommended sleep before the next step at the current level. |
| [`quieten`](#edrpacer-quieten) | method | Return a quieter variant of the command at the current level. |

<a id="edrpacer-__init__"></a>

#### `EdrPacer.__init__`

`constructor` | [modules/loop_guardrails.py:187](../../modules/loop_guardrails.py#L187)

```python
def __init__(self, duration_threshold: float = _EDR_DURATION_THRESHOLD_SEC) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `duration_threshold` | `float` | `_EDR_DURATION_THRESHOLD_SEC` |  |

*Called by:* [`Worker.__init__`](modules.lazy_loop.py.md#worker-__init__)

<a id="edrpacer-observe"></a>

#### `EdrPacer.observe`

`method` | [modules/loop_guardrails.py:193](../../modules/loop_guardrails.py#L193)

```python
def observe(self, command: str, duration_sec: float, output: str) -> None
```

Feed one executed step and update the telemetry estimate.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  | Executed command line. |
| `duration_sec` | `float` |  | Wall-clock seconds the command took. |
| `output` | `str` |  | Captured output (scan for reset/timeout markers). |

*Called by:* [`Worker.execute`](modules.lazy_loop.py.md#worker-execute)

<a id="edrpacer-decay"></a>

#### `EdrPacer.decay`

`method` | [modules/loop_guardrails.py:215](../../modules/loop_guardrails.py#L215)

```python
def decay(self, factor: float = _EDR_DECAY) -> None
```

Cool the estimate down (call once per completed step).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `factor` | `float` | `_EDR_DECAY` |  |

*Called by:* [`Worker.execute`](modules.lazy_loop.py.md#worker-execute)

<a id="edrpacer-level"></a>

#### `EdrPacer.level`

`property` | [modules/loop_guardrails.py:221](../../modules/loop_guardrails.py#L221)

Decorators: `@property`

```python
def level(self) -> int
```

Current pacing level: 0 calm, 1 cautious, 2 stealth.

**Returns:** `int`

<a id="edrpacer-signal"></a>

#### `EdrPacer.signal`

`property` | [modules/loop_guardrails.py:231](../../modules/loop_guardrails.py#L231)

Decorators: `@property`

```python
def signal(self) -> str
```

Human-readable reason for the current level (may be empty).

**Returns:** `str`

*Called by:* [`main`](modules.rootkit.mr.c.md#main)

<a id="edrpacer-inter_step_delay"></a>

#### `EdrPacer.inter_step_delay`

`method` | [modules/loop_guardrails.py:236](../../modules/loop_guardrails.py#L236)

```python
def inter_step_delay(self) -> float
```

Recommended sleep before the next step at the current level.

**Returns:** `float`

*Called by:* [`Worker.execute`](modules.lazy_loop.py.md#worker-execute)

<a id="edrpacer-quieten"></a>

#### `EdrPacer.quieten`

`method` | [modules/loop_guardrails.py:244](../../modules/loop_guardrails.py#L244)

```python
def quieten(self, command: str) -> str
```

Return a quieter variant of the command at the current level.

Applies the first matching downgrade rule whose level threshold
the current level meets; a level of 0 returns the input
unchanged.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  |  |

**Returns:** `str`

*Called by:* [`Worker.execute`](modules.lazy_loop.py.md#worker-execute)

---

<a id="targetlimiter"></a>

### `TargetLimiter`

`class` | [modules/loop_guardrails.py:260](../../modules/loop_guardrails.py#L260)

```python
class TargetLimiter
```

Per-target concurrency cap shared by every loop worker.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `max_concurrent` |  |  | How many distinct targets may be worked at the same time (default 3). |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#targetlimiter-__init__) | constructor |  |
| [`max_concurrent`](#targetlimiter-max_concurrent) | property | Configured upper bound of simultaneous targets. |
| [`active_targets`](#targetlimiter-active_targets) | property | How many distinct targets currently hold a slot. |
| [`slot`](#targetlimiter-slot) | method | Hold one of at most `[`max_concurrent`](#targetlimiter-max_concurrent)` target slots. |

<a id="targetlimiter-__init__"></a>

#### `TargetLimiter.__init__`

`constructor` | [modules/loop_guardrails.py:268](../../modules/loop_guardrails.py#L268)

```python
def __init__(self, max_concurrent: int = DEFAULT_TARGET_LIMIT) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `max_concurrent` | `int` | `DEFAULT_TARGET_LIMIT` | How many distinct targets may be worked at the same time (default 3). |

<a id="targetlimiter-max_concurrent"></a>

#### `TargetLimiter.max_concurrent`

`property` | [modules/loop_guardrails.py:275](../../modules/loop_guardrails.py#L275)

Decorators: `@property`

```python
def max_concurrent(self) -> int
```

Configured upper bound of simultaneous targets.

**Returns:** `int`

<a id="targetlimiter-active_targets"></a>

#### `TargetLimiter.active_targets`

`property` | [modules/loop_guardrails.py:280](../../modules/loop_guardrails.py#L280)

Decorators: `@property`

```python
def active_targets(self) -> int
```

How many distinct targets currently hold a slot.

**Returns:** `int`

<a id="targetlimiter-slot"></a>

#### `TargetLimiter.slot`

`method` `generator` | [modules/loop_guardrails.py:286](../../modules/loop_guardrails.py#L286)

Decorators: `@contextmanager`

```python
def slot(self, target: str)
```

Hold one of at most `[`max_concurrent`](#targetlimiter-max_concurrent)` target slots.

Re-entrant per thread: a worker already holding ``target``
acquires nothing new, so sequencing many commands against one
target never blocks on itself.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target` | `str` |  | Target identifier (empty target bypasses the cap). |

---

<a id="factvectorstore"></a>

### `FactVectorStore`

`class` | [modules/loop_guardrails.py:330](../../modules/loop_guardrails.py#L330)

```python
class FactVectorStore
```

JSON-persisted TF-IDF fact memory with cosine retrieval.

Pure stdlib: no chromadb, no FAISS, no embeddings service. Facts
dedupe by content hash, persist atomically and trim to
``max_facts`` oldest-first.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#factvectorstore-__init__) | constructor |  |
| [`path`](#factvectorstore-path) | property | Backing file path. |
| [`add`](#factvectorstore-add) | method | Embed and store one fact; returns False for duplicates. |
| [`search`](#factvectorstore-search) | method | Return the ``k`` facts most similar to the query. |
| [`search_block`](#factvectorstore-search_block) | method | Render retrieved facts as a prompt-ready block (may be empty). |
| [`clear`](#factvectorstore-clear) | method | Drop every fact (manual reset path). |
| [`save`](#factvectorstore-save) | method | Persist atomically; I/O errors never surface to the loop. |

<a id="factvectorstore-__init__"></a>

#### `FactVectorStore.__init__`

`constructor` | [modules/loop_guardrails.py:338](../../modules/loop_guardrails.py#L338)

```python
def __init__(self, path: str | Path, max_facts: int = DEFAULT_MAX_FACTS) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` |  |  |
| `max_facts` | `int` | `DEFAULT_MAX_FACTS` |  |

<a id="factvectorstore-path"></a>

#### `FactVectorStore.path`

`property` | [modules/loop_guardrails.py:346](../../modules/loop_guardrails.py#L346)

Decorators: `@property`

```python
def path(self) -> Path
```

Backing file path.

**Returns:** `Path`

<a id="factvectorstore-add"></a>

#### `FactVectorStore.add`

`method` | [modules/loop_guardrails.py:367](../../modules/loop_guardrails.py#L367)

```python
def add(self, text: str, meta: dict | None = None) -> bool
```

Embed and store one fact; returns False for duplicates.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `text` | `str` |  | Fact content (command plus output digest). |
| `meta` | `dict \| None` | `None` | Optional metadata attached to the fact. |

**Returns:** `bool` - True when a new fact was stored.

*Calls:* [`FactVectorStore.save`](#factvectorstore-save)

<a id="factvectorstore-search"></a>

#### `FactVectorStore.search`

`method` | [modules/loop_guardrails.py:401](../../modules/loop_guardrails.py#L401)

```python
def search(self, query: str, k: int = DEFAULT_SEARCH_RESULTS) -> list[dict]
```

Return the ``k`` facts most similar to the query.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  | Current goal or step context. |
| `k` | `int` | `DEFAULT_SEARCH_RESULTS` | Maximum results. |

**Returns:** `list[dict]` - List of ``{"text", "meta", "score"}`` dicts, best first.

*Called by:* [`FactVectorStore.search_block`](#factvectorstore-search_block)

<a id="factvectorstore-search_block"></a>

#### `FactVectorStore.search_block`

`method` | [modules/loop_guardrails.py:431](../../modules/loop_guardrails.py#L431)

```python
def search_block(self, query: str, k: int = DEFAULT_SEARCH_RESULTS, max_chars: int = 1200) -> str
```

Render retrieved facts as a prompt-ready block (may be empty).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  |  |
| `k` | `int` | `DEFAULT_SEARCH_RESULTS` |  |
| `max_chars` | `int` | `1200` |  |

**Returns:** `str`

*Calls:* [`FactVectorStore.search`](#factvectorstore-search)

<a id="factvectorstore-clear"></a>

#### `FactVectorStore.clear`

`method` | [modules/loop_guardrails.py:440](../../modules/loop_guardrails.py#L440)

```python
def clear(self) -> None
```

Drop every fact (manual reset path).

*Calls:* [`FactVectorStore.save`](#factvectorstore-save)

<a id="factvectorstore-save"></a>

#### `FactVectorStore.save`

`method` | [modules/loop_guardrails.py:446](../../modules/loop_guardrails.py#L446)

```python
def save(self) -> None
```

Persist atomically; I/O errors never surface to the loop.

*Called by:* [`FactVectorStore.add`](#factvectorstore-add), [`FactVectorStore.clear`](#factvectorstore-clear)

---

## Constants

<a id="default_repeat_window"></a>

### `DEFAULT_REPEAT_WINDOW`

`constant` | [modules/loop_guardrails.py:42](../../modules/loop_guardrails.py#L42)

```python
DEFAULT_REPEAT_WINDOW = 5
```

---

<a id="default_target_limit"></a>

### `DEFAULT_TARGET_LIMIT`

`constant` | [modules/loop_guardrails.py:43](../../modules/loop_guardrails.py#L43)

```python
DEFAULT_TARGET_LIMIT = 3
```

---
