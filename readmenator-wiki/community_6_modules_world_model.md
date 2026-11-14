# modules: world_model

*Community 6 | 99 files | cohesion 0.43*

## Definition

This community groups 99 file(s) rooted at `modules` with dominant language py (cohesion 0.43). Central symbols: `AddonCatalog`, `AddonEntry`, `AdvancePhaseSingleWriterSpec`, `BinaryAttacker`, `BinaryFinder`, `BuildReconPlanContractSpec`, `CVEMapper`, `CalderaCommandSet`. Core file: `modules/world_model.py` (70 symbols). Documented purpose: Command chain registry: explicit prerequisites and dynamic next steps.  The chain answers two questions for both the human operator and the AI:  1. ``prev(cmd)`.

## Files

### `modules` (38 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/attack_surface3d.py` | py | utility | 11 | yes |
| `modules/beacon_recon.py` | py | utility | 6 | yes |
| `modules/compliance.py` | py | utility | 26 | yes |

### `tests` (29 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_asset_gate.py` | py | testing | 16 | yes |
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_beacon_recon_sink.py` | py | testing | 18 | yes |

### `skills/mcp_tools` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/command_next.py` | py | utility | 1 | yes |
| `skills/mcp_tools/command_prev.py` | py | utility | 1 | yes |

### `cli` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/command_chain.py` | py | utility | 22 | yes |
| `cli/exploration.py` | py | utility | 48 | yes |

### `modules/integrations` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |
| `modules/integrations/misp_export.py` | py | utility | 39 | yes |

### `cli/commands` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/caldera.py` | py | utility | 21 | yes |
| `cli/commands/pwn.py` | py | utility | 8 | yes |

### `contrib/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazypwn.py` | py | utility | 15 | no |
| `contrib/legacy/lazyvsftp.py` | py | utility | 3 | no |

### `lazygui` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/__init__.py` | py | utility | 0 | yes |
| `lazygui/version.py` | py | utility | 0 | yes |

### `modules/sinks` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/lazy_intel.py` | py | utility | 3 | yes |
| `modules/sinks/world_model.py` | py | business_logic | 1 | yes |

*... and 79 more files in this community.*


## Key Symbols

- `ChainConfig` (class, `cli/command_chain.py:123`) `class ChainConfig` - Centralised constants for the command chain module.
- `NextStep` (class, `cli/command_chain.py:132`) `class NextStep` - A single recommended next command, with provenance for the operator.
- `to_dict` (method, `cli/command_chain.py:139`) `def to_dict(self)` - Return a JSON-friendly representation of the step.
- `_normalise` (function, `cli/command_chain.py:145`) `def _normalise(name)` - Strip an optional ``do_`` prefix and lowercase the verb.
- `PrerequisiteRegistry` (class, `cli/command_chain.py:156`) `class PrerequisiteRegistry` - Static prev-map registry. One reason to change: the prerequisite table.
- `__init__` (method, `cli/command_chain.py:159`) `def __init__(self, config)` - Store the configuration that owns the prerequisite table.
- `prerequisites` (method, `cli/command_chain.py:164`) `def prerequisites(self, cmd)` - Return the ordered list of prerequisite commands for ``cmd``.
- `StaticNextRegistry` (class, `cli/command_chain.py:171`) `class StaticNextRegistry` - Wrapper over the legacy ``_KILL_CHAIN_NEXT`` map (shared source).
- `next_for` (method, `cli/command_chain.py:174`) `def next_for(self, cmd)` - Return the deterministic kill-chain successors of ``cmd``.
- `phase_priority` (method, `cli/command_chain.py:180`) `def phase_priority(self, phase)` - Return the phase-priority verbs used as a fallback.
- `ServiceNextResolver` (class, `cli/command_chain.py:187`) `class ServiceNextResolver` - Map nmap-discovered services to follow-up verbs.
- `__init__` (method, `cli/command_chain.py:190`) `def __init__(self, config)` - Store the configuration providing the service follow-up table.
- `followups` (method, `cli/command_chain.py:195`) `def followups(self, services)` - Return ``(verb, reason)`` pairs for every triggered follow-up.
- `DynamicNextResolver` (class, `cli/command_chain.py:213`) `class DynamicNextResolver` - Compose static, service, and exploration signals into an ordered list.
- `__init__` (method, `cli/command_chain.py:216`) `def __init__(self, config, static_registry, service_resolver, exploration_engine` - Wire collaborators together. All arguments are injectable for tests.
- `resolve` (method, `cli/command_chain.py:230`) `def resolve(self, cmd, params, target, phase, limit)` - Return the ordered, de-duplicated next-step recommendations.
- `_ensure_engine` (method, `cli/command_chain.py:302`) `def _ensure_engine(self, params)`
- `_append` (method, `cli/command_chain.py:312`) `def _append(steps, seen, name, source, reason, history)`
- `CommandChain` (class, `cli/command_chain.py:329`) `class CommandChain` - Facade exposing prev + next to CLI, MCP, and future TUI widgets.
- `__init__` (method, `cli/command_chain.py:332`) `def __init__(self, config, prerequisites, next_resolver)` - Wire collaborators together using the supplied configuration.
- `prev` (method, `cli/command_chain.py:344`) `def prev(self, cmd)` - Return the ordered prerequisite commands for ``cmd``.
- `next` (method, `cli/command_chain.py:349`) `def next(self, cmd, params, target, phase, limit)` - Return ordered next-step recommendations. See :meth:`DynamicNextResolver.resolve`.
- `_resolve_manager` (function, `cli/commands/caldera.py:49`) `def _resolve_manager()`
- `_resolve_coverage` (function, `cli/commands/caldera.py:53`) `def _resolve_coverage()`
- `_resolve_planner` (function, `cli/commands/caldera.py:59`) `def _resolve_planner(shell)`
- `CalderaCommandSet` (class, `cli/commands/caldera.py:66`) `class CalderaCommandSet(LazyOwnCommandSet)` - Operation lifecycle, TTP coverage, and fact-based planner.
- `_shell` (method, `cli/commands/caldera.py:72`) `def _shell(self)`
- `do_op_list` (method, `cli/commands/caldera.py:80`) `def do_op_list(self, line)` - List all operations.
- `do_op_create` (method, `cli/commands/caldera.py:96`) `def do_op_create(self, line)` - Create a new planned operation.
- `do_op_plan` (method, `cli/commands/caldera.py:114`) `def do_op_plan(self, line)` - Populate operation steps from a playbook YAML or via MITRE derive.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 228
- Cross-boundary resolved imports (EXTRACTED): 349

## Connections

- [EXTRACTED] depends_on community 6 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/command_chain.py imports cli/reactive_hints.py.
- [EXTRACTED] depends_on community 10 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 6 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/caldera.py imports cli/commands/_base.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [dataflow UNCHECKED_ALLOC] `cli/lazynmap_post.py:243` `_emit_event` `fd`: Result of allocator stored in `fd` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/estorides_importer.py:811` `_import_to_scope` `cfg`: Result of allocator stored in `cfg` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/estorides_importer.py:863` `get_combined_surface` `cfg`: Result of allocator stored in `cfg` is never checked against NULL.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `contrib/legacy/lazypwn.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` be broken with an interface?
- What would break if the most connected file in modules: world_model changed?
- Should modules: world_model be split, given cohesion 0.43?

## Sources

- `cli/command_chain.py`
- `cli/commands/caldera.py`
- `cli/commands/pwn.py`
- `cli/commands/surface.py`
- `cli/exploration.py`
- `cli/lazynmap_post.py`
- `cli/ops_commands.py`
- `cli/recon_plan.py`
- `cli/surface_graph.py`
- `contrib/legacy/lazypwn.py`
- `contrib/legacy/lazyvsftp.py`
- `contrib/legacy/sql.py`
- `lazygui/__init__.py`
- `lazygui/version.py`
- `modules/attack_surface3d.py`
- `modules/beacon_recon.py`
- `modules/compliance.py`
- `modules/dashboard_engine.py`
- `modules/estorides_fusion.py`
- `modules/estorides_importer.py`
- *... and 79 more*
