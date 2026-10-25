# modules: defense_eval

*Community 12 | 8 files | cohesion 0.64*

## Definition

This community groups 8 file(s) rooted at `modules` with dominant language py (cohesion 0.64). Central symbols: `Comparison`, `Condition`, `DatasetSummary`, `Evaluation`, `EventRecord`, `Observation`, `RuleEvaluationError`, `RuleMetrics`. Core file: `modules/defense_eval.py` (17 symbols). Documented purpose: Closed-loop detection rule tuning: baseline vs candidate comparison.  Given a baseline rule and a candidate rule plus the same attack (target) and benign (contr.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/closedloop.py` | py | utility | 7 | yes |
| `modules/defense_eval.py` | py | utility | 17 | yes |
| `modules/defense_stages.py` | py | utility | 11 | yes |
| `modules/hunt_verify.py` | py | utility | 16 | yes |
| `tests/test_closedloop.py` | py | testing | 6 | yes |
| `tests/test_defense_eval.py` | py | testing | 10 | yes |
| `tests/test_defense_stages.py` | py | testing | 8 | yes |
| `tests/test_hunt_verify.py` | py | testing | 12 | yes |

## Key Symbols

- `RuleMetrics` (class, `modules/closedloop.py:32`) `class RuleMetrics` - Confusion-style metrics for one replayed rule.
- `to_dict` (method, `modules/closedloop.py:42`) `def to_dict(self)` - Return a JSON-serializable view.
- `Comparison` (class, `modules/closedloop.py:55`) `class Comparison` - Outcome of comparing a candidate rule against a baseline.
- `to_dict` (method, `modules/closedloop.py:66`) `def to_dict(self)` - Return a JSON-serializable view.
- `_metrics_for` (function, `modules/closedloop.py:77`) `def _metrics_for(result)` - Convert one replay result into confusion-style metrics.
- `compare_rules` (function, `modules/closedloop.py:90`) `def compare_rules(baseline_rule, candidate_rule, target_logs, control_logs)` - Replay baseline and candidate rules over identical datasets.
- `suggest_tuning` (function, `modules/closedloop.py:136`) `def suggest_tuning(candidate, baseline)` - Return deterministic tuning suggestions from replay evidence.
- `RuleEvaluationError` (class, `modules/defense_eval.py:39`) `class RuleEvaluationError(ValueError)` - Raised when rule text or log data is invalid or oversized.
- `Condition` (class, `modules/defense_eval.py:44`) `class Condition` - One rule condition: field, operator and expected value.
- `Evaluation` (class, `modules/defense_eval.py:53`) `class Evaluation` - Outcome of applying the rule to one event.
- `to_dict` (method, `modules/defense_eval.py:62`) `def to_dict(self)` - Return a JSON-serializable view.
- `DatasetSummary` (class, `modules/defense_eval.py:74`) `class DatasetSummary` - Per-dataset match counts.
- `to_dict` (method, `modules/defense_eval.py:82`) `def to_dict(self)` - Return a JSON-serializable view.
- `RuleResult` (class, `modules/defense_eval.py:93`) `class RuleResult` - Verdict of one rule replay across target and control datasets.
- `to_dict` (method, `modules/defense_eval.py:103`) `def to_dict(self)` - Return a JSON-serializable view.
- `parse_rule` (function, `modules/defense_eval.py:115`) `def parse_rule(rule_text)` - Parse the rule JSON document into a condition list.
- `_lookup` (function, `modules/defense_eval.py:167`) `def _lookup(fields, field_name)` - Resolve one field: root dotted key first, then nested traversal.
- `_canonical_number` (function, `modules/defense_eval.py:179`) `def _canonical_number(value)` - Normalize a decimal literal so 1, 1.0 and 10e-1 compare equal.
- `_compare` (function, `modules/defense_eval.py:194`) `def _compare(actual, expected, op)` - Compare one field value; returns (matched, evaluable).
- `_scalar_present` (function, `modules/defense_eval.py:223`) `def _scalar_present(value)` - Return whether one JSON value is a present scalar.
- `evaluate_event` (function, `modules/defense_eval.py:234`) `def evaluate_event(conditions, fields)` - Apply every condition to one event.
- `_parse_logs` (function, `modules/defense_eval.py:269`) `def _parse_logs(text, dataset, max_events)` - Parse one log dataset as JSON array or JSON lines.
- `evaluate_rule` (function, `modules/defense_eval.py:322`) `def evaluate_rule(rule_text, target_logs, control_logs)` - Replay one rule against target and control datasets.
- `metrics` (function, `modules/defense_eval.py:380`) `def metrics(result)` - Return tp/fn/fp/tn metrics for one replay result.
- `_activity` (function, `modules/defense_stages.py:28`) `def _activity(task_id)` - Return the task activity log, or a no-op stub.
- `_Stub` (class, `modules/defense_stages.py:35`) `class _Stub`
- `emit` (method, `modules/defense_stages.py:36`) `def emit(self)` - Swallow emissions when no activity log exists.
- `_params` (function, `modules/defense_stages.py:42`) `def _params(stage)` - Return one stage's resolved parameters.
- `_render` (function, `modules/defense_stages.py:52`) `def _render(value, task_id)` - Render the ``{task}`` placeholder in one path template.
- `_read_text` (function, `modules/defense_stages.py:57`) `def _read_text(path)` - Return one file's text or an empty string when absent.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 9
- Cross-boundary resolved imports (EXTRACTED): 7

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [cycle] `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/defense_stages.py` -> `modules/orchestrator_config.py`

## Open Questions

- Can the cycle `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/defense_stages.py` be broken with an interface?
- What would break if the most connected file in modules: defense_eval changed?
- Should modules: defense_eval be split, given cohesion 0.64?

## Sources

- `modules/closedloop.py`
- `modules/defense_eval.py`
- `modules/defense_stages.py`
- `modules/hunt_verify.py`
- `tests/test_closedloop.py`
- `tests/test_defense_eval.py`
- `tests/test_defense_stages.py`
- `tests/test_hunt_verify.py`
