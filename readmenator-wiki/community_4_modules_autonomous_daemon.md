# modules: autonomous_daemon

*Community 4 | 109 files | cohesion 0.50*

## Definition

This community groups 109 file(s) rooted at `modules` with dominant language py (cohesion 0.50). Central symbols: `AIExploitChainer`, `AVBlockedMatcher`, `AbstractReader`, `AbstractSelector`, `AbstractSignalMatcher`, `ActionCategory`, `Anchor`, `ApprovalDecision`. Core file: `skills/autonomous_daemon.py` (150 symbols). Documented purpose: Caldera-style command set — operation lifecycle, TTP coverage, and planner.  Wires the new ``modules/operation``, ``modules/planner``, and ``modules/ttp_coverag.

## Files

### `modules` (37 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/ai_exploit_chain.py` | py | utility | 11 | yes |
| `modules/asset_graph.py` | py | utility | 17 | yes |
| `modules/atomic_enricher.py` | py | utility | 9 | yes |

### `tests` (30 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/integration_autonomous_flow.py` | py | testing | 1 | no |
| `tests/test_autonomous_ops.py` | py | testing | 17 | yes |
| `tests/test_autonomous_replay.py` | py | testing | 18 | yes |

### `skills` (21 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/autonomous_daemon.py` | py | utility | 150 | yes |
| `skills/autonomous_replay.py` | py | utility | 19 | yes |
| `skills/daemon_control.py` | py | utility | 27 | yes |

### `cli/commands` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/caldera.py` | py | utility | 21 | yes |
| `cli/commands/daemon_ctl.py` | py | utility | 8 | yes |

### `skills/tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_autonomous_daemon.py` | py | testing | 88 | yes |
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

### `cli` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/graph_advisor.py` | py | utility | 52 | yes |
| `cli/recommendation.py` | py | utility | 22 | yes |

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

### `scripts` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/lazy_opencode_config.py` | py | infrastructure | 6 | yes |

*... and 89 more files in this community.*


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
- `DaemonControlCommandSet` (class, `cli/commands/daemon_ctl.py:17`) `class DaemonControlCommandSet(LazyOwnCommandSet)` - Autonomous daemon control commands.
- `do_daemon_mode` (method, `cli/commands/daemon_ctl.py:24`) `def do_daemon_mode(self, line)` - Switch the autonomous daemon between auto, approval and paused modes.
- `do_daemon_pause` (method, `cli/commands/daemon_ctl.py:63`) `def do_daemon_pause(self, line)` - Pause the autonomous daemon before its next step.
- `do_daemon_resume` (method, `cli/commands/daemon_ctl.py:82`) `def do_daemon_resume(self, line)` - Resume the autonomous daemon (switch mode to auto).
- `do_daemon_veto` (method, `cli/commands/daemon_ctl.py:97`) `def do_daemon_veto(self, line)` - Add or clear vetoed command first-tokens for the autonomous daemon.
- `do_daemon_focus` (method, `cli/commands/daemon_ctl.py:141`) `def do_daemon_focus(self, line)` - Restrict the autonomous daemon to a set of focus targets.
- `do_daemon_approve` (method, `cli/commands/daemon_ctl.py:175`) `def do_daemon_approve(self, line)` - Approve or veto the daemon's currently-pending action.
- `do_gatecheck` (method, `cli/commands/daemon_ctl.py:224`) `def do_gatecheck(self, line)` - Dry-run the safety gate against one command line.
- `EnumCommandSet` (class, `cli/commands/enum.py:31`) `class EnumCommandSet(LazyOwnCommandSet)` - Enumeration phase commands.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 659
- Cross-boundary resolved imports (EXTRACTED): 355

## Connections

- [EXTRACTED] depends_on community 6 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_pool.py.
- [EXTRACTED] depends_on community 4 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/caldera.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 10 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports skills/autonomous_daemon.py.
- [EXTRACTED] depends_on community 2 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/exploit_migrated.py imports modules/exploit_recommender.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [cycle] `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/auto_registry.py`
- [cycle] `modules/lazy_intel.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_intel.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `skills/swan_agent.py` -> `skills/hive_mind.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_loop.py`

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `contrib/legacy/lazypwn.py`)? What purpose do they serve?
- Can the cycle `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` be broken with an interface?
- What would break if the most connected file in modules: autonomous_daemon changed?
- Should modules: autonomous_daemon be split, given cohesion 0.50?

## Sources

- `cli/commands/caldera.py`
- `cli/commands/daemon_ctl.py`
- `cli/commands/enum.py`
- `cli/commands/exploitgym.py`
- `cli/commands/pwn.py`
- `cli/commands/session_ops.py`
- `cli/graph_advisor.py`
- `cli/recommendation.py`
- `cli/recommendation_signals.py`
- `contrib/legacy/lazypwn.py`
- `contrib/legacy/lazyvsftp.py`
- `contrib/legacy/sql.py`
- `lazygui/__init__.py`
- `lazygui/version.py`
- `modules/ai_exploit_chain.py`
- `modules/asset_graph.py`
- `modules/atomic_enricher.py`
- `modules/auto_pivot.py`
- `modules/autonomous_exploit_engine.py`
- `modules/config_store.py`
- *... and 89 more*
