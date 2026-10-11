# cli: exploration

*Community 12 | 9 files | cohesion 0.50*

## Definition

This community groups 9 file(s) rooted at `cli` with dominant language py (cohesion 0.50). Central symbols: `AddonCatalog`, `AddonEntry`, `BuildReconPlanContractSpec`, `ChainConfig`, `CommandChain`, `CoverageReport`, `DiscoveredService`, `DynamicNextResolver`. Core file: `cli/exploration.py` (48 symbols). Documented purpose: Command chain registry: explicit prerequisites and dynamic next steps.  The chain answers two questions for both the human operator and the AI:  1. ``prev(cmd)`.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/command_chain.py` | py | utility | 25 | yes |
| `cli/exploration.py` | py | utility | 48 | yes |
| `cli/exploration_view.py` | py | presentation | 6 | yes |
| `cli/lazynmap_post.py` | py | utility | 9 | yes |
| `cli/recon_plan.py` | py | utility | 18 | yes |
| `tests/test_command_chain.py` | py | testing | 24 | yes |
| `tests/test_exploration_and_addons.py` | py | testing | 36 | yes |
| `tests/test_lazynmap_post.py` | py | testing | 16 | yes |
| `tests/test_recon_plan.py` | py | testing | 34 | yes |

## Key Symbols

- `ChainConfig` (class, `cli/command_chain.py:123`) `class ChainConfig` - Centralised constants for the command chain module.
- `NextStep` (class, `cli/command_chain.py:132`) `class NextStep` - A single recommended next command, with provenance for the operator.
- `to_dict` (method, `cli/command_chain.py:139`) `def to_dict(self)` - Return a JSON-friendly representation of the step.
- `_normalise` (method, `cli/command_chain.py:145`) `def _normalise(name)` - Strip an optional ``do_`` prefix and lowercase the verb.
- `PrerequisiteRegistry` (class, `cli/command_chain.py:156`) `class PrerequisiteRegistry` - Static prev-map registry. One reason to change: the prerequisite table.
- `__init__` (method, `cli/command_chain.py:159`) `def __init__(self, config)` - Store the configuration that owns the prerequisite table.
- `prerequisites` (method, `cli/command_chain.py:164`) `def prerequisites(self, cmd)` - Return the ordered list of prerequisite commands for ``cmd``.
- `missing` (method, `cli/command_chain.py:170`) `def missing(self, cmd, history)` - Return prerequisites that have **not** yet appeared in ``history``.
- `StaticNextRegistry` (class, `cli/command_chain.py:177`) `class StaticNextRegistry` - Wrapper over the legacy ``_KILL_CHAIN_NEXT`` map (shared source).
- `next_for` (method, `cli/command_chain.py:180`) `def next_for(self, cmd)` - Return the deterministic kill-chain successors of ``cmd``.
- `phase_priority` (method, `cli/command_chain.py:186`) `def phase_priority(self, phase)` - Return the phase-priority verbs used as a fallback.
- `ServiceNextResolver` (class, `cli/command_chain.py:193`) `class ServiceNextResolver` - Map nmap-discovered services to follow-up verbs.
- `__init__` (method, `cli/command_chain.py:196`) `def __init__(self, config)` - Store the configuration providing the service follow-up table.
- `followups` (method, `cli/command_chain.py:201`) `def followups(self, services)` - Return ``(verb, reason)`` pairs for every triggered follow-up.
- `DynamicNextResolver` (class, `cli/command_chain.py:219`) `class DynamicNextResolver` - Compose static, service, and exploration signals into an ordered list.
- `__init__` (method, `cli/command_chain.py:222`) `def __init__(self, config, static_registry, service_resolver, exploration_engine` - Wire collaborators together. All arguments are injectable for tests.
- `resolve` (method, `cli/command_chain.py:236`) `def resolve(self, cmd, params, target, phase, limit)` - Return the ordered, de-duplicated next-step recommendations.
- `_ensure_engine` (method, `cli/command_chain.py:308`) `def _ensure_engine(self, params)`
- `_append` (method, `cli/command_chain.py:318`) `def _append(steps, seen, name, source, reason, history)`
- `CommandChain` (class, `cli/command_chain.py:335`) `class CommandChain` - Facade exposing prev + next to CLI, MCP, and future TUI widgets.
- `__init__` (method, `cli/command_chain.py:338`) `def __init__(self, config, prerequisites, next_resolver)` - Wire collaborators together using the supplied configuration.
- `prev` (method, `cli/command_chain.py:350`) `def prev(self, cmd)` - Return the ordered prerequisite commands for ``cmd``.
- `missing_prerequisites` (method, `cli/command_chain.py:355`) `def missing_prerequisites(self, cmd, history)` - Return prerequisites of ``cmd`` not present in ``history``.
- `next` (method, `cli/command_chain.py:360`) `def next(self, cmd, params, target, phase, limit)` - Return ordered next-step recommendations. See :meth:`DynamicNextResolver.resolve`.
- `chain` (method, `cli/command_chain.py:372`) `def chain(self, cmd, params, target, phase, limit)` - Return a serialisable ``{prev, next}`` view for the given command.
- `ExplorationConfig` (class, `cli/exploration.py:68`) `class ExplorationConfig` - Centralised constants for the exploration engine.
- `DiscoveredService` (class, `cli/exploration.py:87`) `class DiscoveredService` - A single open port discovered by nmap on a host.
- `label` (method, `cli/exploration.py:98`) `def label(self)` - Return a compact human-readable label such as ``smb:445/tcp``.
- `AddonEntry` (class, `cli/exploration.py:105`) `class AddonEntry` - A parsed lazyaddon YAML file with trigger/OS metadata.
- `ToolEntry` (class, `cli/exploration.py:119`) `class ToolEntry` - A parsed ``.tool`` file from the ``tools/`` directory.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 14
- Cross-boundary resolved imports (EXTRACTED): 18

## Connections

- [EXTRACTED] depends_on community 12 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/command_chain.py imports cli/reactive_hints.py.

## Risks

- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/lazynmap_post.py:244` `_emit_event` `fd`: Result of allocator stored in `fd` is never checked against NULL.

## Open Questions

- What would break if the most connected file in cli: exploration changed?
- Should cli: exploration be split, given cohesion 0.50?

## Sources

- `cli/command_chain.py`
- `cli/exploration.py`
- `cli/exploration_view.py`
- `cli/lazynmap_post.py`
- `cli/recon_plan.py`
- `tests/test_command_chain.py`
- `tests/test_exploration_and_addons.py`
- `tests/test_lazynmap_post.py`
- `tests/test_recon_plan.py`
