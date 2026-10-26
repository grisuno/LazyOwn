# modules: lazy_loop

*Community 3 | 126 files | cohesion 0.56*

## Definition

This community groups 126 file(s) rooted at `tests` with dominant language py (cohesion 0.56). Central symbols: `ActivityLog`, `ActivityLogPort`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`, `AddonYamlRenderer`. Core file: `modules/lazy_loop.py` (465 symbols). Documented purpose: Container and Kubernetes attack command set.  Commands for Docker enumeration, Kubernetes cluster reconnaissance, pod escape detection, and container privilege .

## Files

### `tests` (56 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_api_authz.py` | py | testing | 48 | yes |
| `tests/test_asset_gate.py` | py | testing | 16 | yes |

### `modules` (35 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/auto_purple.py` | py | utility | 40 | yes |
| `modules/auto_registry.py` | py | utility | 43 | yes |

### `cli/commands` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/containers.py` | py | infrastructure | 7 | yes |
| `cli/commands/defaults.py` | py | utility | 4 | yes |

### `core` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |
| `core/config.py` | py | infrastructure | 20 | yes |

### `modules/mediation` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/mediation/__init__.py` | py | utility | 0 | yes |
| `modules/mediation/chain_mediator.py` | py | utility | 8 | yes |

### `cli` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/lazy_monitor.py` | py | utility | 46 | yes |
| `cli/lazy_orchestrator.py` | py | utility | 46 | yes |

### `modules/tools` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/tools/__init__.py` | py | utility | 0 | yes |
| `modules/tools/loop_smoke.py` | py | utility | 10 | yes |

### `lazyc2/blueprints` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/api.py` | py | presentation | 10 | yes |
| `lazyc2/blueprints/orchestrator.py` | py | presentation | 17 | yes |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 39 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 6 | yes |

*... and 106 more files in this community.*


## Key Symbols

- `ContainerCommandSet` (class, `cli/commands/containers.py:30`) `class ContainerCommandSet(LazyOwnCommandSet)` - Container and Kubernetes attack commands.
- `do_docker_enum` (method, `cli/commands/containers.py:37`) `def do_docker_enum(self, _line)` - Enumerate Docker host: containers, images, privileges, mounts.
- `do_k8s_enum` (method, `cli/commands/containers.py:101`) `def do_k8s_enum(self, _line)` - Enumerate Kubernetes cluster: pods, secrets, SAs, RBAC.
- `do_container_escape` (method, `cli/commands/containers.py:169`) `def do_container_escape(self, _line)` - Check current container for known escape vectors.
- `do_k8s_pods` (method, `cli/commands/containers.py:239`) `def do_k8s_pods(self, line)` - List Kubernetes pods with security-relevant details.
- `do_k8s_secrets` (method, `cli/commands/containers.py:283`) `def do_k8s_secrets(self, line)` - List and decode Kubernetes secrets.
- `do_container_detect` (method, `cli/commands/containers.py:334`) `def do_container_detect(self, _line)` - Auto-detect container runtime and escape primitives.
- `DefaultsCommandSet` (class, `cli/commands/defaults.py:38`) `class DefaultsCommandSet(LazyOwnCommandSet)` - Inspect and override build-time default constants.
- `do_defaults` (method, `cli/commands/defaults.py:45`) `def do_defaults(self, line)` - Show or override build-time defaults (TOML + payload.json).
- `_show` (method, `cli/commands/defaults.py:60`) `def _show(self, section)` - Print TOML defaults alongside live payload values.
- `_set` (method, `cli/commands/defaults.py:77`) `def _set(self, name, value)` - Persist an override into payload.json via the assign path.
- `GoldenPathsCommandSet` (class, `cli/commands/golden_paths.py:35`) `class GoldenPathsCommandSet(LazyOwnCommandSet)` - Deterministic attack-path solver commands.
- `do_golden_paths` (method, `cli/commands/golden_paths.py:42`) `def do_golden_paths(self, line)` - Build, show, or push attack paths from the world model.
- `_build` (method, `cli/commands/golden_paths.py:65`) `def _build(self, top_k)` - Solve paths from the live world model and persist them.
- `_show` (method, `cli/commands/golden_paths.py:84`) `def _show(self)` - Render the persisted attack-path artifact.
- `_push` (method, `cli/commands/golden_paths.py:98`) `def _push(self)` - Push the persisted paths into sessions/objectives.jsonl.
- `_extract_flag` (function, `cli/commands/gym_matrix.py:34`) `def _extract_flag(args, flag)` - Extract ``--flag <value>`` from tokenised arguments.
- `_extract_bool` (function, `cli/commands/gym_matrix.py:55`) `def _extract_bool(args, flag)` - Extract a boolean flag from tokenised arguments.
- `GymMetasploitableCommandSet` (class, `cli/commands/gym_matrix.py:72`) `class GymMetasploitableCommandSet(LazyOwnCommandSet)` - MS2 gym matrix: plan, run and report deterministic attack paths.
- `do_gym_metasploitable` (method, `cli/commands/gym_matrix.py:79`) `def do_gym_metasploitable(self, line)` - Plan, run, and report the Metasploitable 2 gym matrix.
- `_plan` (method, `cli/commands/gym_matrix.py:114`) `def _plan(self, top_k, only)` - Render the ordered execution plan.
- `_run` (method, `cli/commands/gym_matrix.py:141`) `def _run(self, top_k, only, dry_run)` - Execute the matrix and verify CTF captures.
- `_report` (method, `cli/commands/gym_matrix.py:172`) `def _report(self)` - Show the aggregated CTF capture summary.
- `_verify` (method, `cli/commands/gym_matrix.py:188`) `def _verify(self, rest)` - Print the stored record of one vulnerability.
- `_target` (method, `cli/commands/gym_matrix.py:207`) `def _target(self)` - Return the configured victim host.
- `_engine` (function, `cli/commands/lazyloop.py:22`) `def _engine()` - Return a fresh engine handle over the persisted lazy store.
- `LazyQueueCommandSet` (class, `cli/commands/lazyloop.py:29`) `class LazyQueueCommandSet(LazyOwnCommandSet)` - Lazy queue controls backed by the loop engine.
- `do_lazy_sync` (method, `cli/commands/lazyloop.py:36`) `def do_lazy_sync(self, line)` - Run bidirectional LAZY sync into world model and objectives.
- `do_lazy_intents` (method, `cli/commands/lazyloop.py:51`) `def do_lazy_intents(self, line)` - List engine intents for a task, optionally filtered by state.
- `do_lazy_delete` (method, `cli/commands/lazyloop.py:71`) `def do_lazy_delete(self, line)` - Delete an engine intent; soft keeps outputs, hard cascades.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 886
- Cross-boundary resolved imports (EXTRACTED): 419

## Connections

- [EXTRACTED] depends_on community 1 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/aliases.py imports core/config.py.
- [EXTRACTED] depends_on community 7 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.
- [EXTRACTED] depends_on community 8 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 2 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/command_form.py imports cli/commands/containers.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/param_registry.py` via `subprocess` (4 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/mcp_agent_bridge.py` -> `modules/llm_factory.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/payload_schema.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `modules/__init__.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- What would break if the most connected file in modules: lazy_loop changed?
- Should modules: lazy_loop be split, given cohesion 0.56?

## Sources

- `cli/commands/containers.py`
- `cli/commands/defaults.py`
- `cli/commands/golden_paths.py`
- `cli/commands/gym_matrix.py`
- `cli/commands/lazyloop.py`
- `cli/commands/lazyops.py`
- `cli/commands/params_ops.py`
- `cli/commands/purple_team.py`
- `cli/lazy_monitor.py`
- `cli/lazy_orchestrator.py`
- `cli/orchestrator_assets_tabs.py`
- `cli/purple_tui.py`
- `cli/session_brief.py`
- `cli/tui_forms.py`
- `core/api_authz.py`
- `core/config.py`
- `core/defaults.py`
- `core/param_registry.py`
- `core/payload_schema.py`
- `core/process.py`
- *... and 106 more*
