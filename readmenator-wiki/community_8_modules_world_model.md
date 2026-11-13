# modules: world_model

*Community 8 | 65 files | cohesion 0.39*

## Definition

This community groups 65 file(s) rooted at `tests` with dominant language py (cohesion 0.39). Central symbols: `AddonCatalog`, `AddonEntry`, `AdvancePhaseSingleWriterSpec`, `ArtifactSpec`, `BinaryAttacker`, `BinaryFinder`, `BuildReconPlanContractSpec`, `CVEMapper`. Core file: `modules/world_model.py` (70 symbols). Documented purpose: Command chain registry: explicit prerequisites and dynamic next steps.  The chain answers two questions for both the human operator and the AI:  1. ``prev(cmd)`.

## Files

### `tests` (20 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_command_chain.py` | py | testing | 24 | yes |
| `tests/test_dashboard_tui.py` | py | testing | 23 | yes |
| `tests/test_golden_path.py` | py | testing | 14 | yes |

### `modules` (17 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/compliance.py` | py | utility | 26 | yes |
| `modules/dashboard_engine.py` | py | utility | 16 | yes |
| `modules/estorides_importer.py` | py | utility | 47 | yes |

### `cli` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/command_chain.py` | py | utility | 25 | yes |
| `cli/dashboard_layout.py` | py | presentation | 3 | yes |
| `cli/dashboard_tui.py` | py | utility | 64 | yes |

### `skills/mcp_tools` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/command_next.py` | py | utility | 1 | yes |
| `skills/mcp_tools/command_prev.py` | py | utility | 1 | yes |
| `skills/mcp_tools/dashboard_snapshot.py` | py | utility | 1 | yes |

### `modules/integrations` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |
| `modules/integrations/misp_export.py` | py | utility | 39 | yes |
| `modules/integrations/nuclei_bridge.py` | py | utility | 29 | yes |

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

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/pwn.py` | py | utility | 8 | yes |

*... and 45 more files in this community.*


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
- `PwnCommandSet` (class, `cli/commands/pwn.py:28`) `class PwnCommandSet(LazyOwnCommandSet)` - Autonomous exploitation, LOLBAS, and advanced attack commands.
- `do_auto_pwn` (method, `cli/commands/pwn.py:35`) `def do_auto_pwn(self, line)` - Run the full autonomous exploitation chain against the target.
- `do_rich_tui` (method, `cli/commands/pwn.py:132`) `def do_rich_tui(self, line)` - Launch the Rich-based live dashboard TUI.
- `do_exploit_chain` (method, `cli/commands/pwn.py:181`) `def do_exploit_chain(self, line)` - AI-driven multi-step exploit chaining with fallback strategies.
- `do_lolbas_list` (method, `cli/commands/pwn.py:268`) `def do_lolbas_list(self, line)` - List available LOLBAS (Living Off The Land) techniques from plugins.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 172
- Cross-boundary resolved imports (EXTRACTED): 263

## Connections

- [EXTRACTED] depends_on community 8 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/command_chain.py imports cli/reactive_hints.py.
- [EXTRACTED] depends_on community 11 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/campaign.py imports modules/world_model.py.

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
- Should modules: world_model be split, given cohesion 0.39?

## Sources

- `cli/command_chain.py`
- `cli/commands/pwn.py`
- `cli/dashboard_layout.py`
- `cli/dashboard_tui.py`
- `cli/exploration.py`
- `cli/killchain.py`
- `cli/lazynmap_post.py`
- `cli/ops_commands.py`
- `cli/recommendation.py`
- `cli/recommendation_signals.py`
- `cli/recon_plan.py`
- `contrib/legacy/lazypwn.py`
- `contrib/legacy/lazyvsftp.py`
- `contrib/legacy/sql.py`
- `lazygui/__init__.py`
- `lazygui/version.py`
- `modules/compliance.py`
- `modules/dashboard_engine.py`
- `modules/estorides_importer.py`
- `modules/exploit_recommender.py`
- *... and 45 more*
