# Subsystem: mediation

## modules/mediation/__init__.py
- Doc: Mediation layer for LazyOwn cross-module coordination.
- Layer: utility
- Language: py
- Depends on: `modules/mediation/chain_mediator.py`, `modules/mediation/contracts.py`, `modules/mediation/feedback_mediator.py`, `modules/mediation/hub.py`, `modules/mediation/intel_mediator.py`, `modules/mediation/telemetry_mediator.py`
- Imported by: `cli/apt_chain_support.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `tests/test_mediation.py`

## modules/mediation/chain_mediator.py
- Doc: Specialised mediator for the APT chain pipeline.
- Layer: utility
- Language: py
- Symbols:
  - `LlmPoolPort` (class, line 13) `class LlmPoolPort`
  - `ChainMediator` (class, line 48) `class ChainMediator`
  - `complete` (method, line 16) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 34) `def has_members(self)`
  - `__init__` (method, line 53) `def __init__(self)`
  - `register_llm_port` (method, line 57) `def register_llm_port(self, port)`
  - `llm` (method, line 65) `def llm(self)`
  - `describe` (method, line 73) `def describe(self)`
- Depends on: `modules/lazy_loop.py`
- Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`, `tests/test_guardrails.py`

## modules/mediation/contracts.py
- Doc: Mediation contracts: the abstractions every participant depends on.
- Layer: utility
- Language: py
- Symbols:
  - `MediationDomains` (class, line 12) `class MediationDomains`
  - `ActivityLogPort` (class, line 35) `class ActivityLogPort(Protocol)`
  - `LlmCompletionPort` (class, line 57) `class LlmCompletionPort(Protocol)`
  - `MediatorContract` (class, line 84) `class MediatorContract(Protocol)`
  - `MediationHubContract` (class, line 95) `class MediationHubContract(Protocol)`
  - `resolve` (function, line 103) `def resolve(domain)`
  - `is_known` (method, line 23) `def is_known(cls, domain)`
  - `read` (method, line 44) `def read(self, limit)`
  - `complete` (method, line 60) `def complete(self, prompt, max_tokens, task_id)`
  - `has_members` (method, line 78) `def has_members(self)`
  - `describe` (method, line 89) `def describe(self)`
  - `mediator_for` (method, line 98) `def mediator_for(self, domain)`
- Depends on: `modules/mediation/hub.py`
- Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`

## modules/mediation/feedback_mediator.py
- Doc: Specialised mediator for step-ordering feedback coordination.
- Layer: utility
- Language: py
- Symbols:
  - `FeedbackMediator` (class, line 13) `class FeedbackMediator`
  - `describe` (method, line 18) `def describe(self)`
  - `order_steps` (method, line 22) `def order_steps(self, steps, stack)`
- Depends on: `modules/lazy_orchestrator_feedback.py`
- Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`

## modules/mediation/hub.py
- Doc: Thin routing hub for specialised mediators.
- Layer: utility
- Language: py
- Symbols:
  - `MediationHub` (class, line 19) `class MediationHub`
  - `_build_default` (function, line 55) `def _build_default()`
  - `default_hub` (function, line 73) `def default_hub()`
  - `get_hub` (function, line 78) `def get_hub()`
  - `__init__` (method, line 22) `def __init__(self)`
  - `register` (method, line 26) `def register(self, mediator)`
  - `mediator_for` (method, line 35) `def mediator_for(self, domain)`
  - `snapshot` (method, line 46) `def snapshot(self)`
- Depends on: `modules/mediation/chain_mediator.py`, `modules/mediation/contracts.py`, `modules/mediation/feedback_mediator.py`, `modules/mediation/intel_mediator.py`, `modules/mediation/telemetry_mediator.py`
- Imported by: `modules/mediation/__init__.py`, `modules/mediation/contracts.py`, `tests/test_mediation.py`

## modules/mediation/intel_mediator.py
- Doc: specialised mediator for recon-intel coordination.
- Layer: utility
- Language: py
- Symbols:
  - `IntelMediator` (class, line 13) `class IntelMediator`
  - `__init__` (method, line 18) `def __init__(self)`
  - `register_activity_log_factory` (method, line 22) `def register_activity_log_factory(self, factory)`
  - `describe` (method, line 32) `def describe(self)`
  - `activity_records` (method, line 39) `def activity_records(self, task_id, limit)`
  - `record_routing_decision` (method, line 64) `def record_routing_decision(self, task_id, intent_id, command, intent_text, target, stack)`
  - `record_routing_outcome` (method, line 97) `def record_routing_outcome(self, task_id, intent_id, command, state, facts, findings, stack)`
  - `mask_configured` (method, line 133) `def mask_configured(self, text)`
  - `stack_signature` (method, line 149) `def stack_signature(self, assets)`
- Depends on: `modules/lazy_intel.py`, `modules/lazy_loop.py`
- Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`

## modules/mediation/telemetry_mediator.py
- Doc: Specialised mediator for loop telemetry coordination.
- Layer: utility
- Language: py
- Symbols:
  - `TelemetryMediator` (class, line 14) `class TelemetryMediator`
  - `describe` (method, line 19) `def describe(self)`
  - `publish_event` (method, line 23) `def publish_event(self, task_id, worker, kind, text, severity)`
  - `annotate_detection` (method, line 43) `def annotate_detection(self, command)`
  - `assess_opsec` (method, line 59) `def assess_opsec(self, command, rhost)`
  - `record_outcome_quality` (method, line 77) `def record_outcome_quality(self, worker, intent_summary, facts, findings)`
  - `tool_class_yields` (method, line 93) `def tool_class_yields(self, summaries, phase)`
  - `record_step` (method, line 111) `def record_step(self, task_id, worker, command, output, detection_prob)`
  - `swan_available` (method, line 128) `def swan_available(self)`
  - `swan_consult` (method, line 137) `def swan_consult(self, prompt, task_type, phase, timeout)`
  - `moe_route` (method, line 162) `def moe_route(self, task_type)`
  - `rl_select` (method, line 178) `def rl_select(self, task_type, phase, candidates, deterministic)`
  - `moe_record_outcome` (method, line 203) `def moe_record_outcome(self, expert_id, task_type, reward, detection_prob)`
  - `rl_update` (method, line 219) `def rl_update(self, task_type, phase, action, reward, candidates, detection_prob)`
- Depends on: `modules/loop_ai_bridge.py`
- Imported by: `modules/mediation/__init__.py`, `modules/mediation/hub.py`
