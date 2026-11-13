# `modules.guard_rules`

> Source: [modules/guard_rules.py:1](../../modules/guard_rules.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Seeded guard rules that arm the planner filter before any attribution data.

Failure attribution only demotes a verb after the target has already refused it
several times, so the first rounds of a loop re-propose known-unsafe commands
until the evidence accrues. This store seeds the planner's filter from round
zero with a persisted baseline of rules an unattended loop must never emit
regardless of attribution: destructive-to-self commands that would wreck the
operator host or the engagement.

The baseline is a built-in safety floor merged with an operator override from
``payload.json:loop_guard_rules`` and persisted once to
``sessions/guard_rules_<task>.json`` so it is visible and auditable. Matching
is argv-based, not substring: a command is tokenised, shell and privilege
wrappers (``sudo``, ``env``, ``bash -c`` and friends) are peeled to reach the
real verb, and destructive forms are recognised by structure (recursive-force
``rm`` on a system path, ``dd`` onto a block device) so that ``rm -fr /`` and
``rm --recursive --force /`` are caught as surely as ``rm -rf /``. Every read
fails open to the built-in floor, never an empty set, so a malformed override
can only ever add safety, not remove it. Nothing here imports the loop runtime,
keeping the module cycle-free.

## Contents

- **Classes:** [`GuardRules`](#guardrules)
- **Functions:** [`guard_rules`](#guard_rules)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_guard_rules_py__guard_rules(["guard_rules"])
    n_modules_guard_rules_py__GuardRules___init__(["GuardRules.__init__"])
    n_modules_guard_rules_py__guard_rules --> n_modules_guard_rules_py__GuardRules___init__
```

## Classes

<a id="guardrules"></a>

### `GuardRules`

`class` | [modules/guard_rules.py:174](../../modules/guard_rules.py#L174)

```python
class GuardRules
```

Load, persist and query the seeded planner guard rules for a task.

The ruleset is the built-in floor unioned with the operator override; it is
written once to ``sessions/guard_rules_<task>.json`` (and only when its
content changes) so the active rules are inspectable without rewriting the
file on every construction.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#guardrules-__init__) | constructor | Assemble the ruleset and persist it once, failing open to the floor. |
| [`blocked_verbs`](#guardrules-blocked_verbs) | method | Return the verbs the planner must never propose for this task. |
| [`blocks_command`](#guardrules-blocks_command) | method | Return True when a command is seeded-unsafe for an unattended loop. |

<a id="guardrules-__init__"></a>

#### `GuardRules.__init__`

`constructor` | [modules/guard_rules.py:183](../../modules/guard_rules.py#L183)

```python
def __init__(self, task_id: str = '', base_dir: Path | None = None, override: object | None = None) -> None
```

Assemble the ruleset and persist it once, failing open to the floor.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` | `''` | Campaign/task identifier; blank uses a shared file. |
| `base_dir` | `Path \| None` | `None` | Optional directory override for tests. |
| `override` | `object \| None` | `None` | Explicit override for tests; when None the value is read from ``payload.json:loop_guard_rules``. |

*Called by:* [`guard_rules`](#guard_rules)

<a id="guardrules-blocked_verbs"></a>

#### `GuardRules.blocked_verbs`

`method` | [modules/guard_rules.py:238](../../modules/guard_rules.py#L238)

```python
def blocked_verbs(self) -> set[str]
```

Return the verbs the planner must never propose for this task.

**Returns:** `set[str]`

<a id="guardrules-blocks_command"></a>

#### `GuardRules.blocks_command`

`method` | [modules/guard_rules.py:242](../../modules/guard_rules.py#L242)

```python
def blocks_command(self, command: str) -> bool
```

Return True when a command is seeded-unsafe for an unattended loop.

The command is tokenised and unwrapped to its real verb before any
decision, so privilege and shell wrappers cannot hide a blocked verb.
A blocked verb, a structurally destructive ``rm`` or ``dd``, or a seeded
substring pattern each block the command.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  | The candidate command line. |

**Returns:** `bool` - True when the command matches a seeded verb, a destructive form, or
a seeded substring pattern.

---

## Functions

<a id="guard_rules"></a>

### `guard_rules`

`function` | [modules/guard_rules.py:274](../../modules/guard_rules.py#L274)

```python
def guard_rules(task_id: str = '') -> GuardRules
```

Return a cached [`GuardRules`](#guardrules) for a task, built at most once.

Caching keeps repeated planner rounds from re-reading config and rewriting
the ruleset file; the first call for a task assembles and persists it, later
calls reuse the instance.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` | `''` | Campaign/task identifier. |

**Returns:** `GuardRules` - The shared guard ruleset for the task.

*Calls:* [`GuardRules.__init__`](#guardrules-__init__)

---
