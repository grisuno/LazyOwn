# modules: finding_lifecycle

*Community 11 | 12 files | cohesion 0.50*

## Definition

This community groups 12 file(s) rooted at `modules` with dominant language py (cohesion 0.50). Central symbols: `DatabaseCommandSet`, `FindingRecord`, `RetestRecord`, `SurfaceCommandSet`, `_active_workspace`, `_base_nodes`, `_boom`, `_cache_load`. Core file: `modules/finding_lifecycle.py` (26 symbols). Documented purpose: Database commands — workspace isolation, host/service/vuln management, nmap import, export, and status reporting.  Mirrors the Metasploit ``db_*`` workflow. The.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/database.py` | py | data_access | 16 | yes |
| `cli/commands/surface.py` | py | utility | 3 | yes |
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
- `_family_color` (function, `modules/attack_surface3d.py:100`) `def _family_color(name)` - Stable dusty HSL color from a community name (djb2, ReadMenator).
- `_pagerank` (function, `modules/attack_surface3d.py:111`) `def _pagerank(ids, pairs, alpha, max_iter, tol)` - PageRank over node ids (same contract as ReadMenator rank).
- `_host_of` (function, `modules/attack_surface3d.py:141`) `def _host_of(node)` - Return the dotted IP a surface node belongs to, or "".
- `build_attack_graph` (function, `modules/attack_surface3d.py:147`) `def build_attack_graph(sessions_dir, payload_path, est_cap)` - Fuse surface scans with campaign intel into one C2-centred graph.
- `add_edge` (function, `modules/attack_surface3d.py:155`) `def add_edge(src, dst, kind, evidence, weight)` - Append one provenance-tagged relation between known nodes.
- `tag` (function, `modules/attack_surface3d.py:166`) `def tag(nid, source)` - Record a corroborating artefact on a node, deduped.
- `_intel_id_map` (function, `modules/attack_surface3d.py:315`) `def _intel_id_map(intel, key_to_id)` - Map every intel node id to its merged attack-graph id.
- `_doc` (function, `modules/attack_surface3d.py:327`) `def _doc(node)` - Bounded purpose string for the inspector.
- `_symbols` (function, `modules/attack_surface3d.py:346`) `def _symbols(node)` - Compact symbol records for the inspector (max 40).
- `_enrich` (function, `modules/attack_surface3d.py:365`) `def _enrich(nodes, edges)` - Add ReadMenator explorer fields in place (type/layer/rank/doc).
- `refresh_summary` (function, `modules/attack_surface3d.py:460`) `def refresh_summary(graph, sessions_dir)` - Score exposure into intel_summary.json for the autonomous loop.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 26
- Cross-boundary resolved imports (EXTRACTED): 22

## Connections

- [EXTRACTED] depends_on community 11 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 11 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.
- [EXTRACTED] depends_on community 11 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports skills/autonomous_daemon.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: finding_lifecycle changed?
- Should modules: finding_lifecycle be split, given cohesion 0.50?

## Sources

- `cli/commands/database.py`
- `cli/commands/surface.py`
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
