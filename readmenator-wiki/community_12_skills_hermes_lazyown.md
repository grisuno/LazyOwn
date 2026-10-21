# skills/hermes-lazyown

*Community 12 | 13 files | cohesion 0.44*

## Definition

This community groups 13 file(s) rooted at `skills/hermes-lazyown` with dominant language py (cohesion 0.44). Central symbols: `CheckpointSerializer`, `CompactionResult`, `CompactionStrategy`, `ConfigBridge`, `ConfigBridgeError`, `ConfigKeys`, `DefaultCompaction`, `Defaults`. Core file: `tests/test_killchain_unified_v2.py` (43 symbols). Documented purpose: Self-populating kill-chain progress derived from the daemon event stream.  This module exists for backward compatibility. The canonical phase definitions and pr.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/killchain.py` | py | utility | 4 | yes |
| `modules/kill_chain_viz.py` | py | utility | 5 | yes |
| `modules/killchain.py` | py | utility | 21 | yes |
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |
| `skills/hermes-lazyown/constants.py` | py | utility | 15 | yes |
| `skills/hermes-lazyown/executor.py` | py | utility | 13 | yes |
| `skills/hermes-lazyown/hermes_sync.py` | py | utility | 14 | yes |
| `skills/hermes-lazyown/mcp_server.py` | py | utility | 28 | yes |
| `skills/hermes-lazyown/output_compactor.py` | py | utility | 20 | yes |
| `tests/test_killchain.py` | py | testing | 9 | yes |
| `tests/test_killchain_snapshot.py` | py | testing | 12 | yes |
| `tests/test_killchain_unified_v2.py` | py | testing | 43 | yes |

## Key Symbols

- `PhaseProgress` (class, `cli/killchain.py:29`) `class PhaseProgress` - Computed progress for a single kill-chain phase.
- `_phase_from_event` (function, `cli/killchain.py:48`) `def _phase_from_event(event)` - Return the phase an event belongs to, empty string if absent.
- `_detect_current_phase` (function, `cli/killchain.py:58`) `def _detect_current_phase(events, world, phase_keys)` - Resolve the active phase from events, falling back to the world model.
- `compute_killchain` (function, `cli/killchain.py:83`) `def compute_killchain(events, world, phases)` - Compute kill-chain progress from daemon events and the world model.
- `_load_phases` (function, `modules/kill_chain_viz.py:20`) `def _load_phases(sessions)` - Return a list of phase dicts suitable for SVG/HTML rendering.
- `_read_target` (function, `modules/kill_chain_viz.py:27`) `def _read_target()`
- `_build_svg` (function, `modules/kill_chain_viz.py:34`) `def _build_svg(phases)`
- `generate_html` (function, `modules/kill_chain_viz.py:69`) `def generate_html(target, sessions)`
- `generate_svg` (function, `modules/kill_chain_viz.py:102`) `def generate_svg(target, sessions)`
- `KillChainConfig` (class, `modules/killchain.py:38`) `class KillChainConfig` - Centralised constants for the unified kill-chain.
- `world_model_path` (method, `modules/killchain.py:116`) `def world_model_path(self)` - Return the resolved path to world_model.json.
- `phase_index` (method, `modules/killchain.py:120`) `def phase_index(self, phase)` - Return the positional index of a canonical phase in the kill chain.
- `is_valid_phase` (method, `modules/killchain.py:127`) `def is_valid_phase(self, phase)` - Return True when ``phase`` is a recognised canonical phase.
- `PhaseStatus` (class, `modules/killchain.py:136`) `class PhaseStatus` - Progress for a single kill-chain phase.
- `KillChain` (class, `modules/killchain.py:145`) `class KillChain` - Unified kill-chain operations consumed by every display surface.
- `config` (method, `modules/killchain.py:154`) `def config()` - Return the centralised configuration.
- `phases` (method, `modules/killchain.py:159`) `def phases()` - Return the canonical 8-phase tuple.
- `phase_labels` (method, `modules/killchain.py:164`) `def phase_labels()` - Return the canonical phase label mapping.
- `phase_colors` (method, `modules/killchain.py:169`) `def phase_colors()` - Return the canonical phase hex-color mapping.
- `phase_rich_colors` (method, `modules/killchain.py:174`) `def phase_rich_colors()` - Return the canonical phase rich-terminal color mapping.
- `engagement_phase_to_cli` (method, `modules/killchain.py:179`) `def engagement_phase_to_cli(engagement_value)` - Map a ``WorldModel.EngagementPhase`` value to the CLI phase key.
- `cli_phase_to_host_state` (method, `modules/killchain.py:191`) `def cli_phase_to_host_state(phase)` - Map a CLI phase to a ``WorldModel.HostState`` value.
- `current_phase` (method, `modules/killchain.py:204`) `def current_phase(world_model_path)` - Derive the current kill-chain phase.
- `advance_phase` (method, `modules/killchain.py:251`) `def advance_phase(new_phase, world_model_path, host)` - Advance the kill-chain phase for connected surfaces.
- `get_progress` (method, `modules/killchain.py:328`) `def get_progress(world_model_path)` - Return the current kill-chain progress as a list of status objects.
- `compact_progress` (method, `modules/killchain.py:377`) `def compact_progress(current_phase, phases_entered)` - Return a compact single-line progress indicator ``[R>E>X>P>L]``.
- `phases_for_display` (method, `modules/killchain.py:397`) `def phases_for_display()` - Return an ordered ``(key, label, hex_color)`` triple for every phase.
- `phase_index` (method, `modules/killchain.py:408`) `def phase_index(phase)` - Return the zero-based index of a canonical phase.
- `snapshot` (method, `modules/killchain.py:413`) `def snapshot(world_model_path)` - Return a single, render-agnostic snapshot of the whole kill-chain.
- `get_killchain` (function, `modules/killchain.py:453`) `def get_killchain()` - Return the ``KillChain`` class as a module-level entry point.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 17
- Cross-boundary resolved imports (EXTRACTED): 61

## Connections

- [EXTRACTED] depends_on community 9 <-> 12 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in skills/hermes-lazyown changed?
- Should skills/hermes-lazyown be split, given cohesion 0.44?

## Sources

- `cli/killchain.py`
- `modules/kill_chain_viz.py`
- `modules/killchain.py`
- `skills/hermes-lazyown/claudemd_rules.py`
- `skills/hermes-lazyown/config_bridge.py`
- `skills/hermes-lazyown/constants.py`
- `skills/hermes-lazyown/executor.py`
- `skills/hermes-lazyown/hermes_sync.py`
- `skills/hermes-lazyown/mcp_server.py`
- `skills/hermes-lazyown/output_compactor.py`
- `tests/test_killchain.py`
- `tests/test_killchain_snapshot.py`
- `tests/test_killchain_unified_v2.py`
