# static/js

*Community 9 | 29 files | cohesion 0.41*

## Definition

This community groups 29 file(s) rooted at `static/js` with dominant language js (cohesion 0.41). Central symbols: `A`, `As`, `B`, `BUFFER`, `BackgroundSize`, `Be`, `BezierCurve`, `Bk`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

### `static/js` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |
| `static/js/chart.min.js` | js | utility | 88 | yes |
| `static/js/force-graph-1.43.5.min.js` | js | utility | 31 | yes |

### `cli` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/session_resumer.py` | py | utility | 6 | yes |
| `cli/show.py` | py | utility | 1 | yes |
| `cli/style.py` | py | utility | 4 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/process.py` | py | business_logic | 12 | yes |
| `core/prompt.py` | py | utility | 8 | yes |

### `modules` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/exp.c` | c | utility | 58 | yes |
| `modules/search.py` | py | utility | 0 | yes |

### `tests` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_cli_assign.py` | py | testing | 44 | yes |
| `tests/test_payload_schema.py` | py | testing | 53 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/session_ops.py` | py | utility | 37 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazybinenc.py` | py | utility | 2 | no |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/state.py` | py | utility | 0 | yes |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

*... and 9 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:42`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `_strip_shell_quotes` (function, `cli/commands/session_ops.py:72`) `def _strip_shell_quotes(value)` - Drop one pair of matching wrapping quotes kept by ``posix=False`` parsing.
- `SessionOpsCommandSet` (class, `cli/commands/session_ops.py:86`) `class SessionOpsCommandSet(LazyOwnCommandSet)` - Session and campaign operations.
- `do_note` (method, `cli/commands/session_ops.py:93`) `def do_note(self, line)` - Capture a quick operator note attached to the current target and phase.
- `do_l00t` (method, `cli/commands/session_ops.py:118`) `def do_l00t(self, line)` - Unified loot: show, search, reuse, graph, and mark credentials.
- `do_loot` (method, `cli/commands/session_ops.py:167`) `def do_loot(self, line)` - Alias for ``l00t`` — unified loot (show/search/reuse/graph/mark).
- `do_pivot` (method, `cli/commands/session_ops.py:175`) `def do_pivot(self, line)` - Record a newly discovered pivot target or show the pivot chain.
- `do_tasks` (method, `cli/commands/session_ops.py:200`) `def do_tasks(self, line)` - View and manage the task queue from sessions/tasks.json.
- `do_scans` (method, `cli/commands/session_ops.py:233`) `def do_scans(self, line)` - List nmap scan files in sessions/ with age, size, and open ports.
- `do_sitrep` (method, `cli/commands/session_ops.py:250`) `def do_sitrep(self, line)` - Print a unified operational situation report.
- `do_assign` (method, `cli/commands/session_ops.py:267`) `def do_assign(self, line)` - assign a parameter value, persist to payload.json and refresh aliases.
- `do_tenant` (method, `cli/commands/session_ops.py:332`) `def do_tenant(self, line)` - Manage multi-tenancy: list, switch, or create engagement tenants.
- `do_scope` (method, `cli/commands/session_ops.py:405`) `def do_scope(self, line)` - Manage the authorized engagement scope and the scope-guard posture.
- `do_show` (method, `cli/commands/session_ops.py:471`) `def do_show(self, line)` - Show params, modules, payloads, or active module options.
- `do_list` (method, `cli/commands/session_ops.py:547`) `def do_list(self, line)` - Lists all available scripts in the modules directory.
- `do_run` (method, `cli/commands/session_ops.py:576`) `def do_run(self, line)` - Runs a specific LazyOwn script or active module.
- `do_payload` (method, `cli/commands/session_ops.py:615`) `def do_payload(self, line)` - Load parameters from a specified payload JSON file.
- `do_next` (method, `cli/commands/session_ops.py:666`) `def do_next(self, line)` - Show next-step recommendations or execute the active autosuggest.
- `do_frontier` (method, `cli/commands/session_ops.py:710`) `def do_frontier(self, line)` - Preview the planner intents the autonomous loops would run next.
- `do_traces` (method, `cli/commands/session_ops.py:754`) `def do_traces(self, line)` - Show recent autonomous step traces with evidence and traffic ids.
- `do_chainmode` (method, `cli/commands/session_ops.py:835`) `def do_chainmode(self, line)` - Toggle interactive kill-chain chaining after every command.
- `do_engage` (method, `cli/commands/session_ops.py:886`) `def do_engage(self, line)` - Drive a single target through the full kill-chain in one command.
- `_flag_value` (function, `cli/commands/session_ops.py:950`) `def _flag_value(flag_name)`
- `do_pipeline` (method, `cli/commands/session_ops.py:1013`) `def do_pipeline(self, line)` - Declarative composition layer: run a YAML pipeline of LazyOwn commands.
- `_flag_value` (function, `cli/commands/session_ops.py:1062`) `def _flag_value(flag_name)`
- `do_lazyscript` (method, `cli/commands/session_ops.py:1104`) `def do_lazyscript(self, line)` - Executes commands defined in a lazyscript file.
- `do_hunt` (method, `cli/commands/session_ops.py:1136`) `def do_hunt(self, line)` - Run an autonomous exploitation chain against a target.
- `do_resume` (method, `cli/commands/session_ops.py:1227`) `def do_resume(self, line)` - Browse previous sessions and load a target from a past engagement.
- `do_getseclist` (method, `cli/commands/session_ops.py:1249`) `def do_getseclist(self, line)` - Get the SecLists wordlist from GitHub.
- `do_download_resources` (method, `cli/commands/session_ops.py:1287`) `def do_download_resources(self, line)` - Downloads resources into the `sessions` directory.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 256
- Cross-boundary resolved imports (EXTRACTED): 94

## Connections

- [EXTRACTED] depends_on community 9 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 7 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 1 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/commands/defaults.py imports cli/assign.py.
- [EXTRACTED] depends_on community 2 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports cli/assign.py.

## Risks

- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:371` `set_stable_table_and_set` `seq`: `seq` assigned at line 371 but never read afterwards.

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `contrib/legacy/lazybinenc.py`)? What purpose do they serve?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.41?

## Sources

- `cli/assign.py`
- `cli/commands/session_ops.py`
- `cli/session_resumer.py`
- `cli/show.py`
- `cli/style.py`
- `contrib/legacy/lazybinenc.py`
- `core/process.py`
- `core/prompt.py`
- `key.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/exp.c`
- `modules/search.py`
- `static/js/3d-force-graph-1.73.4.min.js`
- `static/js/bootstrap-4.5.2.min.js`
- `static/js/bootstrap-5.3.0.bundle.min.js`
- `static/js/chart.min.js`
- `static/js/force-graph-1.43.5.min.js`
- `static/js/html2pdf.bundle.min.js`
- `static/js/jquery-3.5.1.slim.min.js`
- *... and 9 more*
