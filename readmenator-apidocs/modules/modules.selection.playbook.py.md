# `modules.selection.playbook`

> Source: [modules/selection/playbook.py:1](../../modules/selection/playbook.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Playbook selector: run an APT actor emulation named by the objective.

Single contract: when the task goal names a known APT actor (from the
``playbooks/`` library, by actor name, alias or chain slug) and a matching
``apt_<slug>`` chain exists, propose running it end to end via
``apt_chain``. The mapping source of truth is the chain side: every
generated ``apt_<slug>`` chain pins ``defaults.playbook`` to the exact
playbook key, so the selector enumerates chains once and links them to
the playbook summaries through that key. Conservative: abstains unless
the goal clearly names an actor, so it never emulates an actor the
operator did not ask for.

## Contents

- **Classes:** [`PlaybookSelector`](#playbookselector)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_selection_playbook_py__PlaybookSelector_propose(["PlaybookSelector.propose"])
    n_modules_selection_base_py__ActionDecision["base.ActionDecision"]
    n_modules_selection_playbook_py__PlaybookSelector_propose -.-> n_modules_selection_base_py__ActionDecision
```

## Classes

<a id="playbookselector"></a>

### `PlaybookSelector`

`class` | [modules/selection/playbook.py:74](../../modules/selection/playbook.py#L74)

```python
class PlaybookSelector
```

Propose ``apt_chain apt_<slug> <target>`` when the goal names an actor.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`name`](#playbookselector-name) |  | `'playbook'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#playbookselector-__init__) | constructor | Bind the playbook directory for summary loading. |
| [`propose`](#playbookselector-propose) | method | Return an actor-emulation action when the goal names one, else None. |

<a id="playbookselector-__init__"></a>

#### `PlaybookSelector.__init__`

`constructor` | [modules/selection/playbook.py:79](../../modules/selection/playbook.py#L79)

```python
def __init__(self, playbook_dir: str = 'playbooks') -> None
```

Bind the playbook directory for summary loading.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `playbook_dir` | `str` | `'playbooks'` | Playbook directory; relative names anchor to the repo root when the working directory lacks one. |

<a id="playbookselector-propose"></a>

#### `PlaybookSelector.propose`

`method` | [modules/selection/playbook.py:128](../../modules/selection/playbook.py#L128)

```python
def propose(self, ctx: SelectionContext) -> ActionDecision | None
```

Return an actor-emulation action when the goal names one, else None.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ctx` | `SelectionContext` |  | Live engagement snapshot from the runtime. |

**Returns:** `ActionDecision | None` - A ``apt_chain <chain> <target>`` decision when the goal names
an actor with a live chain, else None.

*Calls:* [`ActionDecision`](modules.selection.base.py.md#actiondecision)

---
