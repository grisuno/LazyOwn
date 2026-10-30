# modules: world_model

*Community 3 | 113 files | cohesion 0.45*

## Definition

This community groups 113 file(s) rooted at `tests` with dominant language py (cohesion 0.45). Central symbols: `AdLabCaptureSpec`, `AdLabCatalogueSpec`, `AdLabGymDefinitionsSpec`, `AdLabRuntimeSpec`, `BuildAgentProfiles`, `CategorySpec`, `ClientIdProfiles`, `Completed`. Core file: `modules/world_model.py` (70 symbols). Documented purpose: Container and Kubernetes attack command set.  Commands for Docker enumeration, Kubernetes cluster reconnaissance, pod escape detection, and container privilege .

## Files

### `tests` (50 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_ad_lab_gym.py` | py | testing | 25 | yes |
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_bdd_infra_range_report.py` | py | testing | 5 | yes |

### `modules` (29 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/attack_surface3d.py` | py | utility | 11 | yes |
| `modules/beacon_recon.py` | py | utility | 6 | yes |

### `cli/commands` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/containers.py` | py | infrastructure | 7 | yes |
| `cli/commands/golden_paths.py` | py | utility | 5 | yes |
| `cli/commands/gym_matrix.py` | py | utility | 9 | yes |

### `cli` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/lazy_orchestrator.py` | py | utility | 46 | yes |
| `cli/orchestrator_assets_tabs.py` | py | utility | 62 | yes |
| `cli/session_brief.py` | py | utility | 10 | yes |

### `modules/sinks` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/attack_graph.py` | py | utility | 1 | yes |
| `modules/sinks/beacon_dispatch.py` | py | utility | 3 | yes |
| `modules/sinks/c2_surfaces.py` | py | utility | 1 | yes |

### `poc_tui` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | utility | 0 | yes |
| `poc_tui/app.py` | py | utility | 47 | yes |
| `poc_tui/run.py` | py | utility | 1 | yes |

### `lazyc2/blueprints` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/orchestrator.py` | py | presentation | 17 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 6 | yes |

*... and 93 more files in this community.*


## Key Symbols

- `ContainerCommandSet` (class, `cli/commands/containers.py:30`) `class ContainerCommandSet(LazyOwnCommandSet)` - Container and Kubernetes attack commands.
- `do_docker_enum` (method, `cli/commands/containers.py:37`) `def do_docker_enum(self, _line)` - Enumerate Docker host: containers, images, privileges, mounts.
- `do_k8s_enum` (method, `cli/commands/containers.py:101`) `def do_k8s_enum(self, _line)` - Enumerate Kubernetes cluster: pods, secrets, SAs, RBAC.
- `do_container_escape` (method, `cli/commands/containers.py:169`) `def do_container_escape(self, _line)` - Check current container for known escape vectors.
- `do_k8s_pods` (method, `cli/commands/containers.py:239`) `def do_k8s_pods(self, line)` - List Kubernetes pods with security-relevant details.
- `do_k8s_secrets` (method, `cli/commands/containers.py:283`) `def do_k8s_secrets(self, line)` - List and decode Kubernetes secrets.
- `do_container_detect` (method, `cli/commands/containers.py:334`) `def do_container_detect(self, _line)` - Auto-detect container runtime and escape primitives.
- `GoldenPathsCommandSet` (class, `cli/commands/golden_paths.py:35`) `class GoldenPathsCommandSet(LazyOwnCommandSet)` - Deterministic attack-path solver commands.
- `do_golden_paths` (method, `cli/commands/golden_paths.py:42`) `def do_golden_paths(self, line)` - Build, show, or push attack paths from the world model.
- `_build` (method, `cli/commands/golden_paths.py:65`) `def _build(self, top_k)` - Solve paths from the live world model and persist them.
- `_show` (method, `cli/commands/golden_paths.py:86`) `def _show(self)` - Render the persisted attack-path artifact.
- `_push` (method, `cli/commands/golden_paths.py:100`) `def _push(self)` - Push the persisted paths into sessions/objectives.jsonl.
- `_extract_flag` (function, `cli/commands/gym_matrix.py:34`) `def _extract_flag(args, flag)` - Extract ``--flag <value>`` from tokenised arguments.
- `_extract_bool` (function, `cli/commands/gym_matrix.py:55`) `def _extract_bool(args, flag)` - Extract a boolean flag from tokenised arguments.
- `GymMetasploitableCommandSet` (class, `cli/commands/gym_matrix.py:72`) `class GymMetasploitableCommandSet(LazyOwnCommandSet)` - MS2 gym matrix: plan, run and report deterministic attack paths.
- `do_gym_metasploitable` (method, `cli/commands/gym_matrix.py:79`) `def do_gym_metasploitable(self, line)` - Plan, run, and report the Metasploitable 2 gym matrix.
- `_plan` (method, `cli/commands/gym_matrix.py:111`) `def _plan(self, top_k, only)` - Render the ordered execution plan.
- `_run` (method, `cli/commands/gym_matrix.py:135`) `def _run(self, top_k, only, dry_run)` - Execute the matrix and verify CTF captures.
- `_report` (method, `cli/commands/gym_matrix.py:165`) `def _report(self)` - Show the aggregated CTF capture summary.
- `_verify` (method, `cli/commands/gym_matrix.py:181`) `def _verify(self, rest)` - Print the stored record of one vulnerability.
- `_target` (method, `cli/commands/gym_matrix.py:200`) `def _target(self)` - Return the configured victim host.
- `LabCommandSet` (class, `cli/commands/lab.py:27`) `class LabCommandSet(LazyOwnCommandSet)` - Manage local CTF lab environments via Docker.
- `_docker_available` (method, `cli/commands/lab.py:33`) `def _docker_available(self)` - Check if Docker is installed and the daemon is reachable.
- `_running_containers` (method, `cli/commands/lab.py:37`) `def _running_containers(self)` - Return list of running lab container names.
- `_running_range_containers` (method, `cli/commands/lab.py:41`) `def _running_range_containers(self)` - Return list of running cyber range container names.
- `_container_name` (method, `cli/commands/lab.py:45`) `def _container_name(self, scenario)` - Return the container name for a given scenario.
- `_container_ip` (method, `cli/commands/lab.py:49`) `def _container_ip(self, container_name)` - Resolve a lab container IP on its Docker network.
- `_lab_ensure_web` (method, `cli/commands/lab.py:53`) `def _lab_ensure_web(self, scenario, container_name)` - Bring the lab web stack up when the image booted without it.
- `_print_lab_target` (method, `cli/commands/lab.py:57`) `def _print_lab_target(self, scenario, container_name, ports)` - Print the target IP and the host-mapped ports for one lab.
- `_lab_migrate` (method, `cli/commands/lab.py:78`) `def _lab_migrate(self, scenario, container_name)` - Apply gym migrations to the metasploitable lab container.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 377
- Cross-boundary resolved imports (EXTRACTED): 482

## Connections

- [EXTRACTED] depends_on community 7 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/__init__.py.
- [EXTRACTED] depends_on community 2 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/command_form.py imports cli/commands/containers.py.
- [EXTRACTED] depends_on community 1 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/campaign.py imports modules/world_model.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/mcp_agent_bridge.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `modules/__init__.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` be broken with an interface?
- What would break if the most connected file in modules: world_model changed?
- Should modules: world_model be split, given cohesion 0.45?

## Sources

- `cli/commands/containers.py`
- `cli/commands/golden_paths.py`
- `cli/commands/gym_matrix.py`
- `cli/commands/lab.py`
- `cli/commands/lazy_creds.py`
- `cli/commands/lazy_dorks.py`
- `cli/commands/lazy_oob.py`
- `cli/commands/lazy_passgen.py`
- `cli/commands/netattack.py`
- `cli/commands/redteam_gym.py`
- `cli/commands/surface.py`
- `cli/commands/winbox_gym.py`
- `cli/lazy_orchestrator.py`
- `cli/orchestrator_assets_tabs.py`
- `cli/session_brief.py`
- `cli/sessions_browser.py`
- `cli/surface_graph.py`
- `cli/surface_tui.py`
- `cli/timeline_browser.py`
- `cli/tui_forms.py`
- *... and 93 more*
