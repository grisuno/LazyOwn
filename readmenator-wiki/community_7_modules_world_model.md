# modules: world_model

*Community 7 | 60 files | cohesion 0.38*

## Definition

This community groups 60 file(s) rooted at `tests` with dominant language py (cohesion 0.38). Central symbols: `ADCSCertipyWrapper`, `AddonCatalog`, `AddonEntry`, `AdvancePhaseSingleWriterSpec`, `BuildReconPlanContractSpec`, `CategoryResolver`, `CertificateTemplate`, `ChainConfig`. Core file: `modules/world_model.py` (70 symbols). Documented purpose: Command chain registry: explicit prerequisites and dynamic next steps.  The chain answers two questions for both the human operator and the AI:  1. ``prev(cmd)`.

## Files

### `tests` (22 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_chain_list_command.py` | py | testing | 2 | yes |
| `tests/test_command_chain.py` | py | testing | 24 | yes |
| `tests/test_cve_pipeline.py` | py | testing | 11 | yes |

### `modules` (16 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/attack_surface3d.py` | py | utility | 11 | yes |
| `modules/compliance.py` | py | utility | 26 | yes |
| `modules/estorides_fusion.py` | py | utility | 11 | yes |

### `cli` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/command_chain.py` | py | utility | 25 | yes |
| `cli/dashboard_layout.py` | py | presentation | 3 | yes |
| `cli/dashboard_tui.py` | py | utility | 64 | yes |
| `cli/exploit_advisor.py` | py | utility | 11 | yes |

### `cli/commands` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/database.py` | py | data_access | 16 | yes |
| `cli/commands/estorides.py` | py | utility | 9 | yes |
| `cli/commands/exploit_migrated.py` | py | utility | 52 | yes |

### `lazygui` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/__init__.py` | py | utility | 0 | yes |
| `lazygui/version.py` | py | utility | 0 | yes |

### `modules/integrations` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/nuclei_bridge.py` | py | utility | 29 | yes |
| `modules/integrations/nuclei_parser.py` | py | utility | 17 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/autonomous.py` | py | utility | 3 | yes |

*... and 40 more files in this community.*


## Key Symbols

- `ChainConfig` (class, `cli/command_chain.py:123`) `class ChainConfig` - Centralised constants for the command chain module.
- `NextStep` (class, `cli/command_chain.py:132`) `class NextStep` - A single recommended next command, with provenance for the operator.
- `to_dict` (method, `cli/command_chain.py:139`) `def to_dict(self)` - Return a JSON-friendly representation of the step.
- `_normalise` (function, `cli/command_chain.py:145`) `def _normalise(name)` - Strip an optional ``do_`` prefix and lowercase the verb.
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
- `DatabaseCommandSet` (class, `cli/commands/database.py:26`) `class DatabaseCommandSet(LazyOwnCommandSet)` - Database commands for campaign state management.
- `_get_db` (method, `cli/commands/database.py:32`) `def _get_db(self)`
- `_active_workspace` (method, `cli/commands/database.py:40`) `def _active_workspace(self)`
- `do_db_init` (method, `cli/commands/database.py:57`) `def do_db_init(self, line)` - Initialize the database (creates schema if not exists).
- `do_db_workspace` (method, `cli/commands/database.py:75`) `def do_db_workspace(self, line)` - Manage workspaces (list, create, switch, delete).

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 168
- Cross-boundary resolved imports (EXTRACTED): 275

## Connections

- [EXTRACTED] depends_on community 7 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/command_chain.py imports cli/reactive_hints.py.
- [EXTRACTED] depends_on community 9 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/campaign.py imports modules/world_model.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/commands/recon.py:603` `_run_single_search` `_s`: Result of allocator stored in `_s` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `cli/lazynmap_post.py:243` `_emit_event` `fd`: Result of allocator stored in `fd` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/estorides_importer.py:811` `_import_to_scope` `cfg`: Result of allocator stored in `cfg` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/estorides_importer.py:863` `get_combined_surface` `cfg`: Result of allocator stored in `cfg` is never checked against NULL.

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` be broken with an interface?
- What would break if the most connected file in modules: world_model changed?
- Should modules: world_model be split, given cohesion 0.38?

## Sources

- `cli/command_chain.py`
- `cli/commands/database.py`
- `cli/commands/estorides.py`
- `cli/commands/exploit_migrated.py`
- `cli/commands/recon.py`
- `cli/commands/surface.py`
- `cli/dashboard_layout.py`
- `cli/dashboard_tui.py`
- `cli/exploit_advisor.py`
- `cli/exploration.py`
- `cli/exploration_view.py`
- `cli/killchain.py`
- `cli/lazynmap_post.py`
- `cli/ops_commands.py`
- `cli/recommendation.py`
- `cli/recommendation_signals.py`
- `cli/recon_plan.py`
- `core/autonomous.py`
- `lazygui/__init__.py`
- `lazygui/version.py`
- *... and 40 more*
