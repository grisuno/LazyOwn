# `modules.reaction_bridge`

> Source: [modules/reaction_bridge.py:1](../../modules/reaction_bridge.py#L1) | language `py` | coverage 83.3% | [API index](../index.md)

Reaction bridge between the reactive engine and the loop planner.

Two products:

- Saved reactive decisions: after each worker step fails or reveals a
  fresh opportunity, the reactive engine's top decisions are parked in a
  per-task JSON buffer. The next planning round drains them as
  ``reaction`` triggers so the loop reacts instead of observing. One-shot
  consumption, dedupe by command, bounded size.
- Credential reuse: worker outputs that plainly contain login pairs
  (``user:pass`` lines, hash strings) feed back into the autonomous
  exploit engine's credential retry so a captured cred is tried in the
  same session, not next shift. Placeholder values (CHANGE_ME, admin...)
  are rejected loudly, not silently guessed.

## Contents

- **Classes:** [`ReactionPick`](#reactionpick)
- **Functions:** [`save_decisions`](#save_decisions), [`load_reaction_triggers`](#load_reaction_triggers), [`find_credentials`](#find_credentials)

## Classes

<a id="reactionpick"></a>

### `ReactionPick`

`class` | [modules/reaction_bridge.py:66](../../modules/reaction_bridge.py#L66)

```python
class ReactionPick
```

One reactive-engine decision parked for the next planning round.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#reactionpick-__init__) | constructor |  |

<a id="reactionpick-__init__"></a>

#### `ReactionPick.__init__`

`constructor` | [modules/reaction_bridge.py:69](../../modules/reaction_bridge.py#L69)

```python
def __init__(self, command: str, reason: str = '', priority: int = 3, mitre: str = '') -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `command` | `str` |  |  |
| `reason` | `str` | `''` |  |
| `priority` | `int` | `3` |  |
| `mitre` | `str` | `''` |  |

---

## Functions

<a id="save_decisions"></a>

### `save_decisions`

`function` | [modules/reaction_bridge.py:80](../../modules/reaction_bridge.py#L80)

```python
def save_decisions(task_id: str, decisions: list[ReactionPick]) -> int
```

Park picks into the per-task buffer; returns the saved count.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  |  |
| `decisions` | `list[ReactionPick]` |  |  |

**Returns:** `int`

---

<a id="load_reaction_triggers"></a>

### `load_reaction_triggers`

`function` | [modules/reaction_bridge.py:108](../../modules/reaction_bridge.py#L108)

```python
def load_reaction_triggers(task_id: str, consumer: str = '') -> list[dict]
```

Drain the buffer into planner trigger dicts (one-shot, one per round).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `task_id` | `str` |  |  |
| `consumer` | `str` | `''` |  |

**Returns:** `list[dict]`

---

<a id="find_credentials"></a>

### `find_credentials`

`function` | [modules/reaction_bridge.py:159](../../modules/reaction_bridge.py#L159)

```python
def find_credentials(output: str) -> list[dict]
```

Extract user:pass pairs and hashes; placeholder values are dropped.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `output` | `str` |  |  |

**Returns:** `list[dict]`

---
