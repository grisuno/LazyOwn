# Subsystem: selection

## modules/selection/__init__.py
- Doc: Shared action-selection brain for the unified autonomous loop.
- Layer: utility
- Language: py
- Depends on: `modules/selection/adversary.py`, `modules/selection/atomic.py`, `modules/selection/base.py`, `modules/selection/chain.py`, `modules/selection/cred_spray.py`, `modules/selection/playbook.py`, `modules/selection/registry.py`
- Imported by: `tests/test_intel_selector.py`, `tests/test_loop_fire_pending.py`

## modules/selection/adversary.py
- Doc: Adversary selector: run a custom adversary emulation named by the objective.
- Layer: utility
- Language: py
- Symbols:
  - `load_profiles` (function, line 25) `def load_profiles(adversaries_dir)`
  - `_goal_tokens` (function, line 74) `def _goal_tokens(goal)`
  - `resolve_profile` (function, line 79) `def resolve_profile(goal, adversaries_dir)`
  - `AdversarySelector` (class, line 117) `class AdversarySelector`
  - `__init__` (method, line 122) `def __init__(self, adversaries_dir, confirm)`
  - `propose` (method, line 135) `def propose(self, ctx)`
- Depends on: `modules/selection/base.py`
- Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_selectors_capabilities.py`

## modules/selection/atomic.py
- Doc: Atomic selector: emulate named MITRE ATT&CK techniques with atomic tests.
- Layer: utility
- Language: py
- Symbols:
  - `AtomicSelector` (class, line 20) `class AtomicSelector`
  - `propose` (method, line 25) `def propose(self, ctx)`
- Depends on: `modules/selection/base.py`
- Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_selectors_capabilities.py`

## modules/selection/base.py
- Doc: The one shared contract for autonomous action selection.
- Layer: utility
- Language: py
- Symbols:
  - `SelectionContext` (class, line 20) `class SelectionContext`
  - `ActionDecision` (class, line 44) `class ActionDecision`
  - `Selector` (class, line 63) `class Selector(Protocol)`
  - `propose` (method, line 73) `def propose(self, ctx)`
- Imported by: `modules/lazy_loop.py`, `modules/selection/__init__.py`, `modules/selection/adversary.py`, `modules/selection/atomic.py`, `modules/selection/chain.py`, `modules/selection/cred_spray.py`, `modules/selection/intel.py`, `modules/selection/playbook.py`, `modules/selection/registry.py`, `skills/autonomous_daemon.py`, `tests/test_intel_selector.py`, `tests/test_loop_fire_pending.py`, `tests/test_selection_wiring.py`, `tests/test_selectors_base.py`, `tests/test_selectors_capabilities.py`

## modules/selection/chain.py
- Doc: Chain selector: propose a vetted ``apt_chain`` when one fits the state.
- Layer: utility
- Language: py
- Symbols:
  - `ChainSelector` (class, line 13) `class ChainSelector`
  - `__init__` (method, line 18) `def __init__(self, allow_lab)`
  - `propose` (method, line 27) `def propose(self, ctx)`
- Depends on: `modules/chain_match.py`, `modules/selection/base.py`
- Imported by: `modules/exp.c`, `modules/selection/__init__.py`, `modules/selection/registry.py`, `skills/autonomous_daemon.py`, `tests/test_selectors_base.py`

## modules/selection/cred_spray.py
- Doc: Credential-spray selector: reuse known credentials against open services.
- Layer: utility
- Language: py
- Symbols:
  - `CredentialSpraySelector` (class, line 32) `class CredentialSpraySelector`
  - `propose` (method, line 37) `def propose(self, ctx)`
- Depends on: `modules/selection/base.py`
- Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `skills/autonomous_daemon.py`, `tests/test_selectors_capabilities.py`

## modules/selection/intel.py
- Doc: Intel selector: feed exploitation intelligence into the autonomous loop.
- Layer: utility
- Language: py
- Symbols:
  - `intel_report_path` (function, line 32) `def intel_report_path(target)`
  - `load_report` (function, line 44) `def load_report(target)`
  - `pending_fires` (function, line 60) `def pending_fires(target)`
  - `_intelligence_sources_ready` (function, line 84) `def _intelligence_sources_ready()`
  - `_covered_cves` (function, line 98) `def _covered_cves(target)`
  - `IntelSelector` (class, line 112) `class IntelSelector`
  - `propose` (method, line 117) `def propose(self, ctx)`
- Depends on: `modules/selection/base.py`
- Imported by: `modules/selection/registry.py`, `tests/test_intel_selector.py`, `tests/test_loop_fire_pending.py`

## modules/selection/playbook.py
- Doc: Playbook selector: run an APT actor emulation named by the objective.
- Layer: utility
- Language: py
- Symbols:
  - `_goal_tokens` (function, line 26) `def _goal_tokens(goal)`
  - `_summary_words` (function, line 38) `def _summary_words(summary)`
  - `_matches` (function, line 53) `def _matches(tokens, words)`
  - `PlaybookSelector` (class, line 74) `class PlaybookSelector`
  - `__init__` (method, line 79) `def __init__(self, playbook_dir)`
  - `_summaries_with_binding` (method, line 88) `def _summaries_with_binding(self)`
  - `propose` (method, line 128) `def propose(self, ctx)`
- Depends on: `modules/apt_playbooks.py`, `modules/chain_registry.py`, `modules/selection/base.py`
- Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_selectors_capabilities.py`

## modules/selection/registry.py
- Doc: Assemble and run the shared selector cascade.
- Layer: utility
- Language: py
- Symbols:
  - `all_selectors` (function, line 25) `def all_selectors()`
  - `default_selectors` (function, line 46) `def default_selectors()`
  - `propose_next` (function, line 61) `def propose_next(ctx, selectors)`
- Depends on: `modules/__init__.py`, `modules/selection/adversary.py`, `modules/selection/atomic.py`, `modules/selection/base.py`, `modules/selection/chain.py`, `modules/selection/cred_spray.py`, `modules/selection/intel.py`, `modules/selection/playbook.py`
- Imported by: `modules/lazy_loop.py`, `modules/selection/__init__.py`, `skills/autonomous_daemon.py`, `tests/test_selection_wiring.py`, `tests/test_selectors_base.py`, `tests/test_selectors_capabilities.py`
