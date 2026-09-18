# modules

*Community 6 | 17 files | cohesion 0.41*

## Definition

This community groups 17 file(s) rooted at `modules` with dominant language py (cohesion 0.41). Central symbols: `BinaryAttacker`, `BinaryFinder`, `ClaudeMdLoader`, `CompactionResult`, `ContextCompactor`, `DashboardEdge`, `DashboardEngine`, `DashboardNode`. Core file: `tests/test_unified_dashboard.py` (18 symbols). Documented purpose: Autonomous exploitation and LOLBAS command set.  New chingon commands: auto_pwn, rich_tui, lolbas_list, lolbas_use, exploit_chain, stealth..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/pwn.py` | py | utility | 8 | yes |
| `lazygui/__init__.py` | py | presentation | 0 | yes |
| `lazygui/version.py` | py | presentation | 0 | yes |
| `modules/dashboard_engine.py` | py | utility | 16 | yes |
| `modules/exploit_recommender.py` | py | utility | 16 | yes |
| `modules/legacy/lazypwn.py` | py | utility | 15 | no |
| `modules/legacy/lazyvsftp.py` | py | utility | 3 | no |
| `modules/legacy/sql.py` | py | utility | 3 | no |
| `modules/live_surface.py` | py | utility | 7 | yes |
| `modules/rich_tui.py` | py | presentation | 14 | yes |
| `modules/unified_dashboard.py` | py | utility | 15 | yes |
| `skills/lazyown_claudemd.py` | py | utility | 8 | yes |
| `skills/lazyown_context.py` | py | utility | 11 | yes |
| `skills/lazyown_session.py` | py | utility | 14 | yes |
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |
| `tests/test_live_surface.py` | py | testing | 10 | yes |
| `tests/test_unified_dashboard.py` | py | testing | 18 | yes |

## Key Symbols

- `PwnCommandSet` (class, `cli/commands/pwn.py:28`) `class PwnCommandSet(LazyOwnCommandSet)` - Autonomous exploitation, LOLBAS, and advanced attack commands.
- `do_auto_pwn` (method, `cli/commands/pwn.py:35`) `def do_auto_pwn(self, line)` - Run the full autonomous exploitation chain against the target.
- `do_rich_tui` (method, `cli/commands/pwn.py:99`) `def do_rich_tui(self, line)` - Launch the Rich-based live dashboard TUI.
- `do_exploit_chain` (method, `cli/commands/pwn.py:148`) `def do_exploit_chain(self, line)` - AI-driven multi-step exploit chaining with fallback strategies.
- `do_lolbas_list` (method, `cli/commands/pwn.py:235`) `def do_lolbas_list(self, line)` - List available LOLBAS (Living Off The Land) techniques from plugins.
- `do_lolbas_use` (method, `cli/commands/pwn.py:292`) `def do_lolbas_use(self, line)` - Execute a specific LOLBAS technique.
- `do_stealth_on` (method, `cli/commands/pwn.py:384`) `def do_stealth_on(self, line)` - Enable stealth mode for subsequent operations.
- `do_stealth_off` (method, `cli/commands/pwn.py:412`) `def do_stealth_off(self, line)` - Disable stealth mode.
- `_parse_nmap_xml_services` (function, `modules/dashboard_engine.py:31`) `def _parse_nmap_xml_services(sessions_dir)` - Parse all scan_*.nmap.xml files and return {ip: [svc_dicts]}.
- `DashboardNode` (class, `modules/dashboard_engine.py:90`) `class DashboardNode`
- `DashboardEdge` (class, `modules/dashboard_engine.py:102`) `class DashboardEdge`
- `DashboardEngine` (class, `modules/dashboard_engine.py:109`) `class DashboardEngine` - Builds a live dashboard data model from campaign state.
- `__init__` (method, `modules/dashboard_engine.py:130`) `def __init__(self, world_model)`
- `set_world_model` (method, `modules/dashboard_engine.py:139`) `def set_world_model(self, model)`
- `set_exploit_recommender` (method, `modules/dashboard_engine.py:142`) `def set_exploit_recommender(self, recommender)`
- `set_auto_pivot` (method, `modules/dashboard_engine.py:145`) `def set_auto_pivot(self, pivot)`
- `set_evasion_engine` (method, `modules/dashboard_engine.py:148`) `def set_evasion_engine(self, evasion)`
- `build_snapshot` (method, `modules/dashboard_engine.py:151`) `def build_snapshot(self)` - Build a complete dashboard snapshot from all data sources.
- `render_text_map` (method, `modules/dashboard_engine.py:261`) `def render_text_map(self, snapshot)` - Render a text-based network map from a dashboard snapshot.
- `render_ascii_topology` (method, `modules/dashboard_engine.py:343`) `def render_ascii_topology(self, snapshot)` - Render an ASCII-art topology tree from a snapshot.
- `_phase_icon` (method, `modules/dashboard_engine.py:384`) `def _phase_icon(phase)`
- `export_json` (method, `modules/dashboard_engine.py:394`) `def export_json(self, snapshot)` - Export dashboard snapshot as JSON string.
- `persist_snapshot` (method, `modules/dashboard_engine.py:407`) `def persist_snapshot(self, snapshot)` - Persist dashboard snapshot to sessions/dashboard_snapshot.json.
- `format_for_cli` (method, `modules/dashboard_engine.py:424`) `def format_for_cli(self, snapshot)` - Compact single-line status for CLI prompt integration.
- `parse_version` (method, `modules/exploit_recommender.py:24`) `def parse_version(v)`
- `ExploitMatch` (class, `modules/exploit_recommender.py:35`) `class ExploitMatch`
- `ExploitRecommender` (class, `modules/exploit_recommender.py:48`) `class ExploitRecommender` - Matches discovered services against known CVEs and available exploits.
- `__init__` (method, `modules/exploit_recommender.py:118`) `def __init__(self, world_model)`
- `set_world_model` (method, `modules/exploit_recommender.py:127`) `def set_world_model(self, world_model)`
- `set_nvd_api_key` (method, `modules/exploit_recommender.py:130`) `def set_nvd_api_key(self, key)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 25
- Cross-boundary resolved imports (EXTRACTED): 41

## Connections

- [EXTRACTED] depends_on community 0 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/exploit_migrated.py imports modules/exploit_recommender.py.
- [EXTRACTED] depends_on community 6 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/pwn.py imports core/validators.py.
- [EXTRACTED] depends_on community 4 <-> 6 (strength 0.9): Extracted import edge crosses communities: lazyc2.py imports modules/live_surface.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `modules/legacy/lazypwn.py`)? What purpose do they serve?
- What would break if the most connected file in modules changed?
- Should modules be split, given cohesion 0.41?

## Sources

- `cli/commands/pwn.py`
- `lazygui/__init__.py`
- `lazygui/version.py`
- `modules/dashboard_engine.py`
- `modules/exploit_recommender.py`
- `modules/legacy/lazypwn.py`
- `modules/legacy/lazyvsftp.py`
- `modules/legacy/sql.py`
- `modules/live_surface.py`
- `modules/rich_tui.py`
- `modules/unified_dashboard.py`
- `skills/lazyown_claudemd.py`
- `skills/lazyown_context.py`
- `skills/lazyown_session.py`
- `skills/tests/test_harness_e2e.py`
- `tests/test_live_surface.py`
- `tests/test_unified_dashboard.py`
