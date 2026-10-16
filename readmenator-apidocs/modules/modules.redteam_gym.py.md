# `modules.redteam_gym`

> Source: [modules/redteam_gym.py:1](../../modules/redteam_gym.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Red Team Gym — gamified pentest training mode.

Integrates with the existing ELO/karma system in
[`cli.engagement_hooks`](cli.engagement_hooks.py.md) and extends [`cli.commands.lab`](cli.commands.lab.py.md)
Docker scenarios with challenge objectives, scoring, and leaderboards.

Each challenge defines a specific objective, success criteria, a
time-based speed score, a stealth score (based on techniques that
avoid EDR triggers), and a technique-diversity bonus.

Completion awards bonus ELO that is added via the existing
`[`aumentar_elo`](lazyc2.py.md#aumentar_elo)` / ``_award_elo`` pipeline.

## Contents

- **Functions:** [`list_challenges`](#list_challenges), [`start_challenge`](#start_challenge), [`submit_challenge`](#submit_challenge), [`show_leaderboard`](#show_leaderboard), [`get_active_challenge`](#get_active_challenge), [`record_external_attempt`](#record_external_attempt)
- **Constants:** [`GYM_CHALLENGE_DEFINITIONS`](#gym_challenge_definitions)

## Functions

<a id="list_challenges"></a>

### `list_challenges`

`function` | [modules/redteam_gym.py:357](../../modules/redteam_gym.py#L357)

```python
def list_challenges() -> dict[str, dict[str, Any]]
```

Return all defined gym challenges with metadata.

**Returns:** `dict[str, dict[str, Any]]` - Dict mapping challenge ID to definition.

---

<a id="start_challenge"></a>

### `start_challenge`

`function` | [modules/redteam_gym.py:378](../../modules/redteam_gym.py#L378)

```python
def start_challenge(challenge_id: str) -> dict[str, Any]
```

Begin a gym challenge and track start time.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `challenge_id` | `str` |  | ID from GYM_CHALLENGE_DEFINITIONS. |

**Returns:** `dict[str, Any]` - Dict with challenge info and started status.

---

<a id="submit_challenge"></a>

### `submit_challenge`

`function` | [modules/redteam_gym.py:448](../../modules/redteam_gym.py#L448)

```python
def submit_challenge(techniques_used: list[str] | None = None, success: bool = True) -> dict[str, Any]
```

Submit a completed challenge for scoring.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `techniques_used` | `list[str] \| None` | `None` | List of technique identifiers used. |
| `success` | `bool` | `True` | Whether the challenge was completed successfully. |

**Returns:** `dict[str, Any]` - Dict with score breakdown and leaderboard position.

---

<a id="show_leaderboard"></a>

### `show_leaderboard`

`function` | [modules/redteam_gym.py:679](../../modules/redteam_gym.py#L679)

```python
def show_leaderboard(top_n: int = 15) -> list[dict[str, Any]]
```

Return the top N players from the leaderboard.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `top_n` | `int` | `15` | Maximum number of entries to return. |

**Returns:** `list[dict[str, Any]]` - List of leaderboard entries sorted by total_score descending.

---

<a id="get_active_challenge"></a>

### `get_active_challenge`

`function` | [modules/redteam_gym.py:706](../../modules/redteam_gym.py#L706)

```python
def get_active_challenge() -> dict[str, Any] | None
```

Return the currently active challenge for this operator, if any.

**Returns:** `dict[str, Any] | None` - Active challenge dict or None.

---

<a id="record_external_attempt"></a>

### `record_external_attempt`

`function` | [modules/redteam_gym.py:736](../../modules/redteam_gym.py#L736)

```python
def record_external_attempt(challenge_id: str, success: bool, elo_bonus: int = 150, techniques: list[str] | None = None) -> dict[str, Any]
```

Record a scored attempt for a challenge not defined in the catalog.

Lets external modules (for example the ExploitGym integration) feed the
shared ELO/leaderboard pipeline without requiring a challenge
definition or an active in-flight challenge.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `challenge_id` | `str` |  | Identifier recorded on the leaderboard (e.g. ``exploitgym:<task_id>``). |
| `success` | `bool` |  | Whether the attempt succeeded. |
| `elo_bonus` | `int` | `150` | ELO delta to award on success (``0`` on failure). |
| `techniques` | `list[str] \| None` | `None` | Technique identifiers used. |

**Returns:** `dict[str, Any]` - Dict with ``success``, ``challenge``, ``completed``, ``elo_awarded``
and `[`rank`](modules.atomic_exploit_bridge.py.md#rank)`.

*Called by:* [`score_task`](modules.exploitgym_gym.py.md#score_task)

---

## Constants

<a id="gym_challenge_definitions"></a>

### `GYM_CHALLENGE_DEFINITIONS`

`constant` | [modules/redteam_gym.py:30](../../modules/redteam_gym.py#L30)

```python
GYM_CHALLENGE_DEFINITIONS: dict[str, dict[str, Any]]
```

---
