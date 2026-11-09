# modules: world_model

*Community 4 | 91 files | cohesion 0.43*

## Definition

This community groups 91 file(s) rooted at `tests` with dominant language py (cohesion 0.43). Central symbols: `ADCSCertipyWrapper`, `AddonCatalog`, `AddonEntry`, `AdvancePhaseSingleWriterSpec`, `BuildReconPlanContractSpec`, `CategoryResolver`, `CertificateTemplate`, `ChainConfig`. Core file: `modules/world_model.py` (70 symbols). Documented purpose: Command chain registry: explicit prerequisites and dynamic next steps.  The chain answers two questions for both the human operator and the AI:  1. ``prev(cmd)`.

## Files

### `tests` (36 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_beacon_recon_sink.py` | py | testing | 18 | yes |
| `tests/test_chain_list_command.py` | py | testing | 2 | yes |
| `tests/test_command_chain.py` | py | testing | 24 | yes |
| `tests/test_cve_pipeline.py` | py | testing | 11 | yes |

### `modules` (29 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/attack_surface3d.py` | py | utility | 11 | yes |
| `modules/beacon_recon.py` | py | utility | 6 | yes |
| `modules/c2_surfaces.py` | py | utility | 11 | yes |

### `cli` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/command_chain.py` | py | utility | 25 | yes |
| `cli/dashboard_layout.py` | py | presentation | 3 | yes |
| `cli/dashboard_tui.py` | py | utility | 64 | yes |
| `cli/exploration.py` | py | utility | 48 | yes |

### `modules/sinks` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/__init__.py` | py | utility | 0 | yes |
| `modules/sinks/attack_graph.py` | py | utility | 1 | yes |
| `modules/sinks/c2_surfaces.py` | py | utility | 1 | yes |
| `modules/sinks/event_bus.py` | py | infrastructure | 1 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/exploit_migrated.py` | py | utility | 52 | yes |
| `cli/commands/surface.py` | py | utility | 3 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/autonomous.py` | py | utility | 3 | yes |

*... and 71 more files in this community.*


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
- `ExploitMigratedCommandSet` (class, `cli/commands/exploit_migrated.py:38`) `class ExploitMigratedCommandSet(LazyOwnCommandSet)`
- `do_cp` (method, `cli/commands/exploit_migrated.py:43`) `def do_cp(self, line)` - Copies a file from the ExploitDB directory to the sessions directory.
- `do_createcookie` (method, `cli/commands/exploit_migrated.py:84`) `def do_createcookie(self, line)` - Creates a `cookie.txt` file in the `sessions` directory with the specified cookie value.
- `do_py3ttyup` (method, `cli/commands/exploit_migrated.py:128`) `def do_py3ttyup(self, line)` - Copies a Python reverse shell command to the clipboard.
- `do_pyautomate` (method, `cli/commands/exploit_migrated.py:164`) `def do_pyautomate(self, line)` - Automates the execution of pwntomate tools on XML configuration files.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 235
- Cross-boundary resolved imports (EXTRACTED): 351

## Connections

- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/command_chain.py imports cli/reactive_hints.py.
- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.

## Risks

- [cycle] `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_ledger.py` -> `modules/lazy_loop.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_intel.py`
- [dataflow UNCHECKED_ALLOC] `cli/lazynmap_post.py:243` `_emit_event` `fd`: Result of allocator stored in `fd` is never checked against NULL.

## Open Questions

- Can the cycle `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_ledger.py` be broken with an interface?
- What would break if the most connected file in modules: world_model changed?
- Should modules: world_model be split, given cohesion 0.43?

## Sources

- `cli/command_chain.py`
- `cli/commands/exploit_migrated.py`
- `cli/commands/surface.py`
- `cli/dashboard_layout.py`
- `cli/dashboard_tui.py`
- `cli/exploration.py`
- `cli/killchain.py`
- `cli/lazynmap_post.py`
- `cli/ops_commands.py`
- `cli/recommendation.py`
- `cli/recommendation_signals.py`
- `cli/recon_plan.py`
- `cli/surface_graph.py`
- `cli/surface_tui.py`
- `core/autonomous.py`
- `modules/adcs_attacks.py`
- `modules/attack_surface3d.py`
- `modules/beacon_recon.py`
- `modules/c2_surfaces.py`
- `modules/compliance.py`
- *... and 71 more*
