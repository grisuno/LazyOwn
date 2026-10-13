# modules: surface_graph

*Community 10 | 15 files | cohesion 0.53*

## Definition

This community groups 15 file(s) rooted at `modules` with dominant language py (cohesion 0.53). Central symbols: `DatabaseCommandSet`, `FindingRecord`, `RetestRecord`, `SurfaceCommandSet`, `SurfaceEdge`, `SurfaceExplorer`, `SurfaceGraph`, `SurfaceGraphBuilder`. Core file: `cli/surface_graph.py` (33 symbols). Documented purpose: Database commands — workspace isolation, host/service/vuln management, nmap import, export, and status reporting.  Mirrors the Metasploit ``db_*`` workflow. The.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/database.py` | py | data_access | 16 | yes |
| `cli/commands/surface.py` | py | utility | 3 | yes |
| `cli/surface_graph.py` | py | utility | 33 | yes |
| `cli/surface_tui.py` | py | utility | 19 | yes |
| `modules/attack_surface3d.py` | py | utility | 11 | yes |
| `modules/estorides_fusion.py` | py | utility | 11 | yes |
| `modules/finding_lifecycle.py` | py | utility | 26 | yes |
| `modules/intel_fusion.py` | py | utility | 23 | yes |
| `modules/osint_enrich.py` | py | utility | 13 | yes |
| `modules/surface_ops.py` | py | utility | 4 | yes |
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_estorides_fusion.py` | py | testing | 12 | yes |
| `tests/test_finding_lifecycle.py` | py | testing | 10 | yes |
| `tests/test_intel_fusion.py` | py | testing | 7 | yes |
| `tests/test_surface_graph.py` | py | testing | 13 | yes |

## Key Symbols

- `DatabaseCommandSet` (class, `cli/commands/database.py:26`) `class DatabaseCommandSet(LazyOwnCommandSet)` - Database commands for campaign state management.
- `_get_db` (method, `cli/commands/database.py:32`) `def _get_db(self)`
- `_active_workspace` (method, `cli/commands/database.py:40`) `def _active_workspace(self)`
- `do_db_init` (method, `cli/commands/database.py:57`) `def do_db_init(self, line)` - Initialize the database (creates schema if not exists).
- `do_db_workspace` (method, `cli/commands/database.py:75`) `def do_db_workspace(self, line)` - Manage workspaces (list, create, switch, delete).
- `do_db_hosts` (method, `cli/commands/database.py:124`) `def do_db_hosts(self, line)` - List or add hosts in the active workspace.
- `do_db_services` (method, `cli/commands/database.py:185`) `def do_db_services(self, line)` - List all services in the active workspace.
- `do_db_vulns` (method, `cli/commands/database.py:213`) `def do_db_vulns(self, line)` - List or add vulnerabilities.
- `do_retest` (method, `cli/commands/database.py:267`) `def do_retest(self, line)` - Re-verify a finding in an isolated session (LAZY retester).
- `do_db_creds` (method, `cli/commands/database.py:349`) `def do_db_creds(self, line)` - List or add credentials.
- `do_db_loot` (method, `cli/commands/database.py:393`) `def do_db_loot(self, line)` - List or add loot items.
- `do_db_notes` (method, `cli/commands/database.py:433`) `def do_db_notes(self, line)` - List or add notes.
- `do_db_import` (method, `cli/commands/database.py:471`) `def do_db_import(self, line)` - Import scan results into the database.
- `do_db_export` (method, `cli/commands/database.py:509`) `def do_db_export(self, line)` - Export database table to CSV.
- `do_db_status` (method, `cli/commands/database.py:543`) `def do_db_status(self, line)` - Show entity counts for the active workspace.
- `shlex_split` (function, `cli/commands/database.py:560`) `def shlex_split(text)` - Split text like shlex.split but handle empty strings gracefully.
- `SurfaceCommandSet` (class, `cli/commands/surface.py:36`) `class SurfaceCommandSet(LazyOwnCommandSet)` - Discovery scans and OSINT fusion for the attack surface.
- `do_scandiscovery` (method, `cli/commands/surface.py:43`) `def do_scandiscovery(self, line)` - Scan every discovery IP with operator confirmation.
- `do_estorides_intel` (method, `cli/commands/surface.py:86`) `def do_estorides_intel(self, line)` - Fuse estorides OSINT entities into the campaign intel graphs.
- `_slug_host` (function, `cli/surface_graph.py:75`) `def _slug_host(ip)` - Return the canonical ``host-<dotted-ip>`` id used by the web graph.
- `_slug_port` (function, `cli/surface_graph.py:80`) `def _slug_port(host_id, port, protocol)` - Return a stable port-node id rooted at ``host_id``.
- `SurfaceNode` (class, `cli/surface_graph.py:87`) `class SurfaceNode` - A node in the network surface graph.
- `to_dict` (method, `cli/surface_graph.py:102`) `def to_dict(self)` - Return a JSON-serialisable view of the node.
- `SurfaceEdge` (class, `cli/surface_graph.py:113`) `class SurfaceEdge` - A directed edge between two surface nodes.
- `to_dict` (method, `cli/surface_graph.py:120`) `def to_dict(self)` - Return a JSON-serialisable view of the edge.
- `SurfaceGraph` (class, `cli/surface_graph.py:126`) `class SurfaceGraph` - Aggregate snapshot of nodes + edges discovered on disk.
- `to_dict` (method, `cli/surface_graph.py:135`) `def to_dict(self)` - Return a JSON-serialisable view (mirrors the web UI payload).
- `stats` (method, `cli/surface_graph.py:146`) `def stats(self)` - Return per-kind node counts plus edge count.
- `children_of` (method, `cli/surface_graph.py:153`) `def children_of(self, node_id)` - Return nodes that ``node_id`` points to via an outgoing edge.
- `get` (method, `cli/surface_graph.py:165`) `def get(self, node_id)` - Return the node with ``node_id`` or ``None``.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 29
- Cross-boundary resolved imports (EXTRACTED): 26

## Connections

- [EXTRACTED] depends_on community 10 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 10 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.
- [EXTRACTED] depends_on community 10 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports skills/autonomous_daemon.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: surface_graph changed?
- Should modules: surface_graph be split, given cohesion 0.53?

## Sources

- `cli/commands/database.py`
- `cli/commands/surface.py`
- `cli/surface_graph.py`
- `cli/surface_tui.py`
- `modules/attack_surface3d.py`
- `modules/estorides_fusion.py`
- `modules/finding_lifecycle.py`
- `modules/intel_fusion.py`
- `modules/osint_enrich.py`
- `modules/surface_ops.py`
- `tests/test_attack_surface3d.py`
- `tests/test_estorides_fusion.py`
- `tests/test_finding_lifecycle.py`
- `tests/test_intel_fusion.py`
- `tests/test_surface_graph.py`
