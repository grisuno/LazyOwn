# modules: autonomous_daemon

*Community 1 | 114 files | cohesion 0.58*

## Definition

This community groups 114 file(s) rooted at `modules` with dominant language py (cohesion 0.58). Central symbols: `AIExploitChainer`, `AIResult`, `AVBlockedMatcher`, `AbstractReader`, `AbstractSelector`, `AbstractSignalMatcher`, `AccessFact`, `ActionCategory`. Core file: `skills/autonomous_daemon.py` (148 symbols). Documented purpose: Caldera-style command set — operation lifecycle, TTP coverage, and planner.  Wires the new ``modules/operation``, ``modules/planner``, and ``modules/ttp_coverag.

## Files

### `modules` (44 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/ai_exploit_chain.py` | py | utility | 11 | yes |
| `modules/ai_fallback.py` | py | utility | 8 | yes |

### `tests` (29 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/integration_autonomous_flow.py` | py | testing | 1 | no |
| `tests/test_autonomous_ops.py` | py | testing | 17 | yes |
| `tests/test_autonomous_replay.py` | py | testing | 18 | yes |

### `skills` (25 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/autonomous_daemon.py` | py | utility | 148 | yes |
| `skills/autonomous_replay.py` | py | utility | 19 | yes |
| `skills/daemon_control.py` | py | utility | 27 | yes |

### `skills/tests` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_autonomous_daemon.py` | py | testing | 88 | yes |
| `skills/tests/test_facts.py` | py | testing | 37 | yes |
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

### `cli/commands` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/caldera.py` | py | utility | 21 | yes |
| `cli/commands/enum.py` | py | utility | 11 | yes |
| `cli/commands/exploitgym.py` | py | utility | 10 | yes |

### `modules/integrations` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |
| `modules/integrations/misp_export.py` | py | utility | 38 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyaddon_creator.py` | py | utility | 14 | yes |

### `lazyc2/security` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/chart.min.js` | js | utility | 88 | yes |

*... and 94 more files in this community.*


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
- `EnumCommandSet` (class, `cli/commands/enum.py:31`) `class EnumCommandSet(LazyOwnCommandSet)` - Enumeration phase commands.
- `do_smbclient` (method, `cli/commands/enum.py:38`) `def do_smbclient(self, line)` - Interacts with SMB shares using the `smbclient` command to perform the following operations:
- `do_smbclient_impacket` (method, `cli/commands/enum.py:108`) `def do_smbclient_impacket(self, line)` - Interacts with SMB shares using the `smbclient` command to perform the following operations:
- `do_smbclient_py` (method, `cli/commands/enum.py:178`) `def do_smbclient_py(self, line)` - Interacts with SMB shares using the `smbclient.py` command to perform the following operations:
- `do_smbmap` (method, `cli/commands/enum.py:225`) `def do_smbmap(self, line)` - smbmap -H 10.10.10.3 [OPTIONS]
- `do_getnpusers` (method, `cli/commands/enum.py:345`) `def do_getnpusers(self, line)` - sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt
- `do_psexec` (method, `cli/commands/enum.py:390`) `def do_psexec(self, line)` - Executes the Impacket PSExec tool to attempt remote execution on the specified target.
- `do_psexec_py` (method, `cli/commands/enum.py:446`) `def do_psexec_py(self, line)` - Executes the Impacket PSExec tool to attempt remote execution on the specified target.
- `do_rpcdump` (method, `cli/commands/enum.py:502`) `def do_rpcdump(self, line)` - Executes the `rpcdump.py` script to dump RPC services from a target host.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 636
- Cross-boundary resolved imports (EXTRACTED): 292

## Connections

- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_pool.py.
- [EXTRACTED] depends_on community 0 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports modules/bof_registry.py.
- [EXTRACTED] depends_on community 9 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports skills/autonomous_daemon.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [cycle] `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- [cycle] `modules/detection_oracle.py` -> `modules/detection_feed.py` -> `modules/detection_oracle.py`
- [cycle] `skills/lazyown_mcp.py` -> `skills/lazyown_llm.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `modules/__init__.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in modules: autonomous_daemon changed?
- Should modules: autonomous_daemon be split, given cohesion 0.58?

## Sources

- `cli/commands/caldera.py`
- `cli/commands/enum.py`
- `cli/commands/exploitgym.py`
- `contrib/legacy/lazyaddon_creator.py`
- `lazyc2/security/command_allowlist.py`
- `modules/__init__.py`
- `modules/ai_exploit_chain.py`
- `modules/ai_fallback.py`
- `modules/asset_graph.py`
- `modules/atomic_enricher.py`
- `modules/auto_pivot.py`
- `modules/autonomous_exploit_engine.py`
- `modules/bof_registry.py`
- `modules/config_store.py`
- `modules/cve_matcher.py`
- `modules/dashboard_bp.py`
- `modules/detection_feed.py`
- `modules/detection_oracle.py`
- `modules/engage_summary.py`
- `modules/enrich.py`
- *... and 94 more*
