# `modules.mediation.feedback_mediator`

> Source: [modules/mediation/feedback_mediator.py:1](../../modules/mediation/feedback_mediator.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Specialised mediator for step-ordering feedback coordination.

Owns the `[`modules.lazy_orchestrator_feedback`](modules.lazy_orchestrator_feedback.py.md)` interaction so the loop
planner requests ordering through this mediator instead of importing the
feedback module directly.

## Contents

- **Classes:** [`FeedbackMediator`](#feedbackmediator)

## Classes

<a id="feedbackmediator"></a>

### `FeedbackMediator`

`class` | [modules/mediation/feedback_mediator.py:13](../../modules/mediation/feedback_mediator.py#L13)

```python
class FeedbackMediator
```

Mediate orchestrator feedback used to order loop steps.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`domain`](#feedbackmediator-domain) | `str` | `'loop.feedback'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`describe`](#feedbackmediator-describe) | method | Return mediator metadata for diagnostics. |
| [`order_steps`](#feedbackmediator-order_steps) | method | Reorder worker steps with cross-task priors. |

<a id="feedbackmediator-describe"></a>

#### `FeedbackMediator.describe`

`method` | [modules/mediation/feedback_mediator.py:18](../../modules/mediation/feedback_mediator.py#L18)

```python
def describe(self) -> dict[str, Any]
```

Return mediator metadata for diagnostics.

**Returns:** `dict[str, Any]`

<a id="feedbackmediator-order_steps"></a>

#### `FeedbackMediator.order_steps`

`method` | [modules/mediation/feedback_mediator.py:22](../../modules/mediation/feedback_mediator.py#L22)

```python
def order_steps(self, steps: list[str], stack: str = '') -> list[str]
```

Reorder worker steps with cross-task priors.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `steps` | `list[str]` |  | Command step strings in proposed order. |
| `stack` | `str` | `''` | Target stack fingerprint for priors. |

**Returns:** `list[str]` - Reordered steps, or the input order on failure.

---
