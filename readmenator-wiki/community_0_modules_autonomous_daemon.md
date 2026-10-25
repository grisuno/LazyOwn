# modules: autonomous_daemon

*Community 0 | 184 files | cohesion 0.57*

## Definition

This community groups 184 file(s) rooted at `modules` with dominant language py (cohesion 0.57). Central symbols: `ACIEngine`, `ACIGoal`, `ACIPlan`, `ACIPlanner`, `ACIReflector`, `AIExploitChainer`, `AIModel`, `AIResult`. Core file: `skills/autonomous_daemon.py` (150 symbols). Documented purpose: Caldera-style command set — operation lifecycle, TTP coverage, and planner.  Wires the new ``modules/operation``, ``modules/planner``, and ``modules/ttp_coverag.

## Files

### `modules` (76 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_runner.py` | py | utility | 38 | yes |
| `modules/ai_exploit_chain.py` | py | utility | 11 | yes |

### `tests` (48 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/conftest.py` | py | testing | 10 | yes |
| `tests/integration_autonomous_flow.py` | py | testing | 1 | no |

### `skills` (26 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/aci_planner.py` | py | utility | 42 | yes |
| `skills/autonomous_daemon.py` | py | utility | 150 | yes |

### `cli/commands` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/caldera.py` | py | utility | 21 | yes |
| `cli/commands/collaboration.py` | py | utility | 8 | yes |

### `contrib/legacy` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyaddon_creator.py` | py | utility | 14 | yes |
| `contrib/legacy/lazyhoneypot.py` | py | utility | 15 | yes |

### `skills/tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_autonomous_daemon.py` | py | testing | 88 | yes |
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

### `modules/integrations` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |
| `modules/integrations/misp_export.py` | py | utility | 39 | yes |

### `core` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/executor.py` | py | utility | 6 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/recommendation.py` | py | utility | 22 | yes |

### `lazyc2/blueprints` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/api_v1.py` | py | presentation | 12 | yes |

### `lazyc2/extensions` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/short_urls.py` | py | infrastructure | 5 | yes |

### `modules/sinks` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/campaign_db.py` | py | utility | 1 | yes |

### `scripts` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/lazy_opencode_config.py` | py | infrastructure | 6 | yes |

*... and 164 more files in this community.*


## Key Symbols

- `_resolve_manager` (function, `cli/commands/caldera.py:49`) `def _resolve_manager()`
- `_resolve_coverage` (function, `cli/commands/caldera.py:53`) `def _resolve_coverage()`
- `_resolve_planner` (function, `cli/commands/caldera.py:59`) `def _resolve_planner(shell)`
- `CalderaCommandSet` (class, `cli/commands/caldera.py:66`) `class CalderaCommandSet(LazyOwnCommandSet)` - Operation lifecycle, TTP coverage, and fact-based planner.
- `_shell` (method, `cli/commands/caldera.py:72`) `def _shell(self)`
- `do_op_list` (method, `cli/commands/caldera.py:80`) `def do_op_list(self, line)` - List all operations.
- `do_op_create` (method, `cli/commands/caldera.py:96`) `def do_op_create(self, line)` - Create a new planned operation.
- `do_op_plan` (method, `cli/commands/caldera.py:114`) `def do_op_plan(self, line)` - Populate operation steps from a playbook YAML or via MITRE derive.
- `do_op_start` (method, `cli/commands/caldera.py:141`) `def do_op_start(self, line)` - Start (or resume) an operation.
- `do_op_pause` (method, `cli/commands/caldera.py:166`) `def do_op_pause(self, line)` - Pause a running operation.
- `do_op_resume` (method, `cli/commands/caldera.py:183`) `def do_op_resume(self, line)` - Resume a paused operation.
- `do_op_stop` (method, `cli/commands/caldera.py:200`) `def do_op_stop(self, line)` - Stop a running operation.
- `do_op_status` (method, `cli/commands/caldera.py:217`) `def do_op_status(self, line)` - Show the status of an operation.
- `do_op_timeline` (method, `cli/commands/caldera.py:249`) `def do_op_timeline(self, line)` - Show the event timeline of an operation.
- `do_op_report` (method, `cli/commands/caldera.py:272`) `def do_op_report(self, line)` - Generate a full report for an operation.
- `do_ttp_matrix` (method, `cli/commands/caldera.py:290`) `def do_ttp_matrix(self, line)` - Render the MITRE ATT&CK coverage matrix across all operations.
- `do_ttp_rebuild` (method, `cli/commands/caldera.py:299`) `def do_ttp_rebuild(self, line)` - Re-walk the operations directory to refresh the coverage matrix.
- `do_ttp_show` (method, `cli/commands/caldera.py:309`) `def do_ttp_show(self, line)` - Show details for a single MITRE technique.
- `do_plan` (method, `cli/commands/caldera.py:336`) `def do_plan(self, line)` - Pick the next best technique to run for a target.
- `do_plan_detail` (method, `cli/commands/caldera.py:364`) `def do_plan_detail(self, line)` - Show the full ranked plan (all candidates) for a target.
- `do_plan_apply` (method, `cli/commands/caldera.py:391`) `def do_plan_apply(self, line)` - Run the planner, then auto-create and start an operation.
- `CollaborationCommandSet` (class, `cli/commands/collaboration.py:20`) `class CollaborationCommandSet(LazyOwnCommandSet)` - Multi-operator collaboration commands for the CLI.
- `_get_collab` (method, `cli/commands/collaboration.py:26`) `def _get_collab(self)` - Lazy-load collaboration singletons from modules.collab_bp.
- `_resolve_target` (method, `cli/commands/collaboration.py:38`) `def _resolve_target(self, target)` - Resolve a target argument: explicit IP or rhost from payload.
- `do_lock_target` (method, `cli/commands/collaboration.py:48`) `def do_lock_target(self, line)` - Acquire an advisory lock on a target to prevent tool collisions.
- `do_unlock_target` (method, `cli/commands/collaboration.py:89`) `def do_unlock_target(self, line)` - Release an advisory lock on a target.
- `do_team_status` (method, `cli/commands/collaboration.py:114`) `def do_team_status(self, line)` - Show active operators and target locks.
- `do_team_chat` (method, `cli/commands/collaboration.py:169`) `def do_team_chat(self, line)` - Send a message to all connected operators.
- `do_share_finding` (method, `cli/commands/collaboration.py:199`) `def do_share_finding(self, line)` - Share a finding or credential discovery with the team.
- `DaemonControlCommandSet` (class, `cli/commands/daemon_ctl.py:17`) `class DaemonControlCommandSet(LazyOwnCommandSet)` - Autonomous daemon control commands.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1003
- Cross-boundary resolved imports (EXTRACTED): 462

## Connections

- [EXTRACTED] depends_on community 7 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/reactive_engine.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 10 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_factory.py.
- [EXTRACTED] depends_on community 0 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/caldera.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `modules/ai_model.py` via `subprocess` (5 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_client.py` via `subprocess` (5 hops)
- [taint high] `cli/banner_config.py` -> `modules/toposwarm_bridge.py` via `subprocess` (5 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/mcp_agent_bridge.py` -> `modules/llm_factory.py`

## Open Questions

- Why do 5 file(s) lack file-level docs (e.g. `contrib/legacy/lazyllmchat.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- What would break if the most connected file in modules: autonomous_daemon changed?
- Should modules: autonomous_daemon be split, given cohesion 0.57?

## Sources

- `cli/commands/caldera.py`
- `cli/commands/collaboration.py`
- `cli/commands/daemon_ctl.py`
- `cli/commands/database.py`
- `cli/commands/enum.py`
- `cli/commands/estorides.py`
- `cli/recommendation.py`
- `cli/recommendation_signals.py`
- `contrib/legacy/lazyaddon_creator.py`
- `contrib/legacy/lazyhoneypot.py`
- `contrib/legacy/lazyllmchat.py`
- `contrib/legacy/lazyopenssh77enum2.py`
- `contrib/legacy/lazysearch_bot.py`
- `contrib/legacy/lazyssh.py`
- `core/executor.py`
- `core/logging.py`
- `core/scheduler.py`
- `core/security.py`
- `lazyc2/blueprints/api_v1.py`
- `lazyc2/blueprints/phishing.py`
- *... and 164 more*
