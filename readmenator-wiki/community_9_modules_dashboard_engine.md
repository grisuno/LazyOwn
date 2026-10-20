# modules: dashboard_engine

*Community 9 | 13 files | cohesion 0.39*

## Definition

This community groups 13 file(s) rooted at `modules` with dominant language py (cohesion 0.39). Central symbols: `BinaryAttacker`, `BinaryFinder`, `DashboardEdge`, `DashboardEngine`, `DashboardNode`, `ExploitMatch`, `ExploitRecommender`, `PwnCommandSet`. Core file: `tests/test_unified_dashboard.py` (18 symbols). Documented purpose: Autonomous exploitation and LOLBAS command set.  New chingon commands: auto_pwn, rich_tui, lolbas_list, lolbas_use, exploit_chain, stealth..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/pwn.py` | py | utility | 8 | yes |
| `contrib/legacy/lazypwn.py` | py | utility | 15 | no |
| `contrib/legacy/lazyvsftp.py` | py | utility | 3 | no |
| `contrib/legacy/sql.py` | py | utility | 3 | no |
| `lazygui/__init__.py` | py | utility | 0 | yes |
| `lazygui/version.py` | py | utility | 0 | yes |
| `modules/dashboard_engine.py` | py | utility | 16 | yes |
| `modules/exploit_recommender.py` | py | utility | 16 | yes |
| `modules/live_surface.py` | py | utility | 7 | yes |
| `modules/rich_tui.py` | py | utility | 14 | yes |
| `modules/unified_dashboard.py` | py | utility | 15 | yes |
| `tests/test_live_surface.py` | py | testing | 10 | yes |
| `tests/test_unified_dashboard.py` | py | testing | 18 | yes |

## Key Symbols

- `PwnCommandSet` (class, `cli/commands/pwn.py:28`) `class PwnCommandSet(LazyOwnCommandSet)` - Autonomous exploitation, LOLBAS, and advanced attack commands.
- `do_auto_pwn` (method, `cli/commands/pwn.py:35`) `def do_auto_pwn(self, line)` - Run the full autonomous exploitation chain against the target.
- `do_rich_tui` (method, `cli/commands/pwn.py:109`) `def do_rich_tui(self, line)` - Launch the Rich-based live dashboard TUI.
- `do_exploit_chain` (method, `cli/commands/pwn.py:158`) `def do_exploit_chain(self, line)` - AI-driven multi-step exploit chaining with fallback strategies.
- `do_lolbas_list` (method, `cli/commands/pwn.py:245`) `def do_lolbas_list(self, line)` - List available LOLBAS (Living Off The Land) techniques from plugins.
- `do_lolbas_use` (method, `cli/commands/pwn.py:302`) `def do_lolbas_use(self, line)` - Execute a specific LOLBAS technique.
- `do_stealth_on` (method, `cli/commands/pwn.py:394`) `def do_stealth_on(self, line)` - Enable stealth mode for subsequent operations.
- `do_stealth_off` (method, `cli/commands/pwn.py:422`) `def do_stealth_off(self, line)` - Disable stealth mode.
- `BinaryFinder` (class, `contrib/legacy/lazypwn.py:24`) `class BinaryFinder`
- `__init__` (method, `contrib/legacy/lazypwn.py:25`) `def __init__(self)`
- `find_suid_binaries` (method, `contrib/legacy/lazypwn.py:28`) `def find_suid_binaries(self)`
- `find_capabilities_binaries` (method, `contrib/legacy/lazypwn.py:36`) `def find_capabilities_binaries(self)`
- `find_executable_binaries` (method, `contrib/legacy/lazypwn.py:44`) `def find_executable_binaries(self)`
- `find_specific_name_binaries` (method, `contrib/legacy/lazypwn.py:52`) `def find_specific_name_binaries(self, names)`
- `process_output` (method, `contrib/legacy/lazypwn.py:61`) `def process_output(self, output)`
- `get_found_binaries` (method, `contrib/legacy/lazypwn.py:67`) `def get_found_binaries(self)`
- `BinaryAttacker` (class, `contrib/legacy/lazypwn.py:70`) `class BinaryAttacker`
- `__init__` (method, `contrib/legacy/lazypwn.py:71`) `def __init__(self, binary_path)`
- `analyze_with_ltrace` (method, `contrib/legacy/lazypwn.py:76`) `def analyze_with_ltrace(self)`
- `extract_strings` (method, `contrib/legacy/lazypwn.py:83`) `def extract_strings(self)`
- `prepare_attack` (method, `contrib/legacy/lazypwn.py:90`) `def prepare_attack(self)`
- `exploit_with_pwntools` (method, `contrib/legacy/lazypwn.py:170`) `def exploit_with_pwntools(self)`
- `main` (function, `contrib/legacy/lazypwn.py:181`) `def main()`
- `connect` (function, `contrib/legacy/lazyvsftp.py:7`) `def connect(host, port)`
- `exploit` (function, `contrib/legacy/lazyvsftp.py:16`) `def exploit(host, port)`
- `handle_backdoor` (function, `contrib/legacy/lazyvsftp.py:61`) `def handle_backdoor(s)`
- `def_handler` (function, `contrib/legacy/sql.py:8`) `def def_handler(sig, frame)`
- `getUnicode` (function, `contrib/legacy/sql.py:15`) `def getUnicode(sqli)`
- `makeRequest` (function, `contrib/legacy/sql.py:22`) `def makeRequest(sqli_modified)`
- `_parse_nmap_xml_services` (function, `modules/dashboard_engine.py:39`) `def _parse_nmap_xml_services(sessions_dir)` - Parse all scan_*.nmap.xml files and return {ip: [svc_dicts]}.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 17
- Cross-boundary resolved imports (EXTRACTED): 31

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [cycle] `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/unified_dashboard.py` -> `skills/hive_mind.py`

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `contrib/legacy/lazypwn.py`)? What purpose do they serve?
- Can the cycle `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/unified_dashboard.py` be broken with an interface?
- What would break if the most connected file in modules: dashboard_engine changed?
- Should modules: dashboard_engine be split, given cohesion 0.39?

## Sources

- `cli/commands/pwn.py`
- `contrib/legacy/lazypwn.py`
- `contrib/legacy/lazyvsftp.py`
- `contrib/legacy/sql.py`
- `lazygui/__init__.py`
- `lazygui/version.py`
- `modules/dashboard_engine.py`
- `modules/exploit_recommender.py`
- `modules/live_surface.py`
- `modules/rich_tui.py`
- `modules/unified_dashboard.py`
- `tests/test_live_surface.py`
- `tests/test_unified_dashboard.py`
