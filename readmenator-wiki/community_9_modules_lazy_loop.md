# modules: lazy_loop

*Community 9 | 25 files | cohesion 0.51*

## Definition

This community groups 25 file(s) rooted at `modules` with dominant language py (cohesion 0.51). Central symbols: `ActivityLog`, `AssetGate`, `AssetGraph`, `AssetNode`, `AutoVerb`, `Budget`, `ColdCompactor`, `CompanyScope`. Core file: `modules/lazy_loop.py` (263 symbols). Documented purpose: Database commands — workspace isolation, host/service/vuln management, nmap import, export, and status reporting.  Mirrors the Metasploit ``db_*`` workflow. The.

## Files

### `modules` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/attack_surface3d.py` | py | utility | 11 | yes |
| `modules/auto_registry.py` | py | utility | 10 | yes |
| `modules/estorides_fusion.py` | py | utility | 8 | yes |
| `modules/finding_lifecycle.py` | py | utility | 10 | yes |
| `modules/intel_fusion.py` | py | utility | 23 | yes |
| `modules/lazy_engine.py` | py | utility | 1 | yes |
| `modules/lazy_loop.py` | py | utility | 263 | yes |

### `tests` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_asset_gate.py` | py | testing | 16 | yes |
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_auto_registry.py` | py | testing | 14 | yes |
| `tests/test_estorides_fusion.py` | py | testing | 12 | yes |
| `tests/test_finding_lifecycle.py` | py | testing | 10 | yes |
| `tests/test_intel_fusion.py` | py | testing | 7 | yes |
| `tests/test_lazy_engine.py` | py | testing | 9 | yes |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/database.py` | py | data_access | 16 | yes |
| `cli/commands/lazyops.py` | py | utility | 49 | yes |
| `cli/commands/mcp_bridge.py` | py | utility | 24 | yes |
| `cli/commands/surface.py` | py | utility | 3 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/surface_graph.py` | py | utility | 33 | yes |
| `cli/surface_tui.py` | py | utility | 19 | yes |

*... and 5 more files in this community.*


## Key Symbols

- `DatabaseCommandSet` (class, `cli/commands/database.py:27`) `class DatabaseCommandSet(LazyOwnCommandSet)` - Database commands for campaign state management.
- `_get_db` (method, `cli/commands/database.py:33`) `def _get_db(self)`
- `_active_workspace` (method, `cli/commands/database.py:41`) `def _active_workspace(self)`
- `do_db_init` (method, `cli/commands/database.py:58`) `def do_db_init(self, line)` - Initialize the database (creates schema if not exists).
- `do_db_workspace` (method, `cli/commands/database.py:76`) `def do_db_workspace(self, line)` - Manage workspaces (list, create, switch, delete).
- `do_db_hosts` (method, `cli/commands/database.py:125`) `def do_db_hosts(self, line)` - List or add hosts in the active workspace.
- `do_db_services` (method, `cli/commands/database.py:186`) `def do_db_services(self, line)` - List all services in the active workspace.
- `do_db_vulns` (method, `cli/commands/database.py:214`) `def do_db_vulns(self, line)` - List or add vulnerabilities.
- `do_retest` (method, `cli/commands/database.py:268`) `def do_retest(self, line)` - Re-verify a finding in an isolated session (LAZY retester).
- `do_db_creds` (method, `cli/commands/database.py:351`) `def do_db_creds(self, line)` - List or add credentials.
- `do_db_loot` (method, `cli/commands/database.py:395`) `def do_db_loot(self, line)` - List or add loot items.
- `do_db_notes` (method, `cli/commands/database.py:435`) `def do_db_notes(self, line)` - List or add notes.
- `do_db_import` (method, `cli/commands/database.py:473`) `def do_db_import(self, line)` - Import scan results into the database.
- `do_db_export` (method, `cli/commands/database.py:511`) `def do_db_export(self, line)` - Export database table to CSV.
- `do_db_status` (method, `cli/commands/database.py:545`) `def do_db_status(self, line)` - Show entity counts for the active workspace.
- `shlex_split` (method, `cli/commands/database.py:562`) `def shlex_split(text)` - Split text like shlex.split but handle empty strings gracefully.
- `_engine` (function, `cli/commands/lazyops.py:26`) `def _engine()` - Import LazyEngine lazily so the shell boots without it.
- `LazyCommandSet` (class, `cli/commands/lazyops.py:33`) `class LazyCommandSet(LazyOwnCommandSet)` - Lazy double-graph autonomous loop: planner, workers, guard, retest.
- `_task_id` (method, `cli/commands/lazyops.py:39`) `def _task_id(self, args)` - Resolve --task flag or fall back to the newest task.
- `_require_task` (method, `cli/commands/lazyops.py:52`) `def _require_task(self, args)` - Return task id or print usage error and empty string.
- `_free_text` (method, `cli/commands/lazyops.py:60`) `def _free_text(args)` - Return positional words with flag values stripped.
- `do_lazy_task` (method, `cli/commands/lazyops.py:76`) `def do_lazy_task(self, line)` - Create/list/show/pause/resume/delete tasks. Usage: lazy_task create <goal> \| lazy_task list \| lazy_t
- `do_lazy_graph` (method, `cli/commands/lazyops.py:118`) `def do_lazy_graph(self, line)` - Show planner-facing graph overview. Usage: lazy_graph [--task T]
- `do_lazy_planner` (method, `cli/commands/lazyops.py:137`) `def do_lazy_planner(self, line)` - Run one planner wakeup (emits 0..N intents). Usage: lazy_planner [--task T]
- `do_lazy_frontier` (method, `cli/commands/lazyops.py:156`) `def do_lazy_frontier(self, line)` - Show pending intent queue. Usage: lazy_frontier [--task T]
- `do_lazy_worker` (method, `cli/commands/lazyops.py:168`) `def do_lazy_worker(self, line)` - Claim ONE intent and execute it with real tools. Usage: lazy_worker [--task T] [--intent N]
- `do_lazy_trace` (method, `cli/commands/lazyops.py:197`) `def do_lazy_trace(self, line)` - Worker trace exchange. Usage: lazy_trace list\|search <q>\|get <intent> [--task T]
- `do_lazy_hint` (method, `cli/commands/lazyops.py:227`) `def do_lazy_hint(self, line)` - Inject steering hint. Usage: lazy_hint <text> [--task T]
- `do_lazy_intent` (method, `cli/commands/lazyops.py:239`) `def do_lazy_intent(self, line)` - Inject high-priority intent. Usage: lazy_intent <summary> [--task T] [--priority N]
- `do_lazy_goal` (method, `cli/commands/lazyops.py:263`) `def do_lazy_goal(self, line)` - Goals: list\|set <t1;t2>\|edit <id> <text>\|delete <id>\|prove <goal> <evidence> <reason>\|met <reason>.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 94
- Cross-boundary resolved imports (EXTRACTED): 47

## Connections

- [EXTRACTED] depends_on community 9 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 9 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.
- [EXTRACTED] depends_on community 9 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports skills/autonomous_daemon.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: lazy_loop changed?
- Should modules: lazy_loop be split, given cohesion 0.51?

## Sources

- `cli/commands/database.py`
- `cli/commands/lazyops.py`
- `cli/commands/mcp_bridge.py`
- `cli/commands/surface.py`
- `cli/surface_graph.py`
- `cli/surface_tui.py`
- `modules/attack_surface3d.py`
- `modules/auto_registry.py`
- `modules/estorides_fusion.py`
- `modules/finding_lifecycle.py`
- `modules/intel_fusion.py`
- `modules/lazy_engine.py`
- `modules/lazy_loop.py`
- `modules/loop_progress.py`
- `modules/osint_enrich.py`
- `modules/surface_ops.py`
- `tests/test_asset_gate.py`
- `tests/test_attack_surface3d.py`
- `tests/test_auto_registry.py`
- `tests/test_estorides_fusion.py`
- *... and 5 more*
