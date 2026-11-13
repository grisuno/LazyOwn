# Subsystem: commands (page 5 of 5)
Previous: [KB_commands_p4.md](KB_commands_p4.md)

## cli/commands/shellsys.py
- Doc: Local shell and system extracted from the miscellaneous cluster.
- Layer: utility
- Language: py
- Symbols:
  - `ShellSysCommandSet` (class, line 24) `class ShellSysCommandSet(LazyOwnCommandSet)`
  - `do_sh` (method, line 31) `def do_sh(self, line)`
  - `do_sys` (method, line 63) `def do_sys(self, line)`
  - `do_pwd` (method, line 111) `def do_pwd(self, line)`
  - `do_nano` (method, line 147) `def do_nano(self, line)`
  - `do_cron` (method, line 171) `def do_cron(self, line)`
  - `do_clean` (method, line 217) `def do_clean(self, line)`
  - `do_fixperm` (method, line 305) `def do_fixperm(self, line)`
  - `do_fixel` (method, line 338) `def do_fixel(self, line)`
  - `do_pop` (method, line 371) `def do_pop(self, line)`
  - `do_tab` (method, line 408) `def do_tab(self, line)`
  - `lazyrun_command` (function, line 206) `def lazyrun_command()`
- Depends on: `cli/commands/_base.py`, `core/safe_exec.py`, `core/session_secrets.py`, `utils.py`
- Imported by: `tests/test_shellsys_command_set.py`

## cli/commands/sidequest.py
- Doc: Side-question CommandSet: read-only review of loop decision checkpoints.
- Layer: utility
- Language: py
- Symbols:
  - `SidequestCommandSet` (class, line 18) `class SidequestCommandSet(LazyOwnCommandSet)`
  - `do_sidequest` (method, line 25) `def do_sidequest(self, statement)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`

## cli/commands/sleep_obfuscation.py
- Doc: Sleep obfuscation CommandSet — beacon memory evasion technique management.
- Layer: utility
- Language: py
- Symbols:
  - `SleepObfuscationCommandSet` (class, line 16) `class SleepObfuscationCommandSet(LazyOwnCommandSet)`
  - `do_sleep_list` (method, line 23) `def do_sleep_list(self, line)`
  - `do_sleep_info` (method, line 50) `def do_sleep_info(self, line)`
  - `do_sleep_configure` (method, line 82) `def do_sleep_configure(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/sleep_obfuscation.py`, `utils.py`

## cli/commands/socks_proxy.py
- Doc: SOCKS proxy CommandSet — beacon tunneling configuration.
- Layer: utility
- Language: py
- Symbols:
  - `SocksProxyCommandSet` (class, line 18) `class SocksProxyCommandSet(LazyOwnCommandSet)`
  - `do_socks_config` (method, line 25) `def do_socks_config(self, line)`
  - `do_socks_sessions` (method, line 75) `def do_socks_sessions(self, line)`
  - `do_socks_export` (method, line 94) `def do_socks_export(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/socks_proxy.py`, `utils.py`

## cli/commands/supply_chain.py
- Doc: Supply Chain Attack command set.
- Layer: utility
- Language: py
- Symbols:
  - `SupplyChainCommandSet` (class, line 88) `class SupplyChainCommandSet(LazyOwnCommandSet)`
  - `_parse_requirements` (function, line 282) `def _parse_requirements(filepath)`
  - `_parse_package_json` (function, line 307) `def _parse_package_json(filepath)`
  - `_parse_gemfile` (function, line 328) `def _parse_gemfile(filepath)`
  - `_parse_cargo_toml` (function, line 348) `def _parse_cargo_toml(filepath)`
  - `_parse_go_mod` (function, line 377) `def _parse_go_mod(filepath)`
  - `_parse_pom_xml` (function, line 397) `def _parse_pom_xml(filepath)`
  - `_pypi_exists` (function, line 425) `def _pypi_exists(package_name)`
  - `is_internal_name` (function, line 450) `def is_internal_name(name)`
  - `_extract_flag` (function, line 475) `def _extract_flag(args, flag)`
  - `do_depconfuse` (method, line 95) `def do_depconfuse(self, line)`
  - `do_package_squat` (method, line 140) `def do_package_squat(self, line)`
  - `do_depscan` (method, line 216) `def do_depscan(self, line)`
- Depends on: `cli/commands/_base.py`, `utils.py`

## cli/commands/surface.py
- Doc: Attack-surface operations: confirmed discovery scans, estorides fusion.
- Layer: utility
- Language: py
- Symbols:
  - `SurfaceCommandSet` (class, line 36) `class SurfaceCommandSet(LazyOwnCommandSet)`
  - `do_scandiscovery` (method, line 43) `def do_scandiscovery(self, line)`
  - `do_estorides_intel` (method, line 86) `def do_estorides_intel(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/attack_surface3d.py`, `modules/estorides_fusion.py`, `modules/surface_ops.py`, `utils.py`

## cli/commands/ux.py
- Doc: Usability commands: hud, undo, config_diff, cheat, suggest.
- Layer: utility
- Language: py
- Symbols:
  - `UxCommandSet` (class, line 39) `class UxCommandSet(LazyOwnCommandSet)`
  - `do_hud` (method, line 46) `def do_hud(self, line)`
  - `do_undo` (method, line 85) `def do_undo(self, line)`
  - `do_config_diff` (method, line 115) `def do_config_diff(self, line)`
  - `do_cheat` (method, line 140) `def do_cheat(self, line)`
  - `do_toast` (method, line 167) `def do_toast(self, line)`
  - `do_suggest` (method, line 261) `def do_suggest(self, line)`
  - `_candidate_commands` (method, line 281) `def _candidate_commands(self)`
  - `_find_cheat_section` (method, line 298) `def _find_cheat_section(query)`
- Depends on: `cli/commands/_base.py`, `cli/config_history.py`, `cli/fuzzy_match.py`, `cli/output_mode.py`, `cli/session_hud.py`, `cli/toast_bus.py`, `core/config.py`, `core/console.py`, `utils.py`

## cli/commands/verb_admin.py
- Doc: Operator administration of the autonomous-loop verb catalog.
- Layer: utility
- Language: py
- Symbols:
  - `VerbAdminConfig` (class, line 23) `class VerbAdminConfig`
  - `_row_text` (function, line 35) `def _row_text(entry)`
  - `VerbCommandSet` (class, line 45) `class VerbCommandSet(LazyOwnCommandSet)`
  - `do_verb` (method, line 52) `def do_verb(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/verb_catalog.py`, `utils.py`

## cli/commands/winbox_gym.py
- Doc: WinBox lab CommandSet — VM lifecycle, guest execution and gym matrix.
- Layer: utility
- Language: py
- Symbols:
  - `WinboxCommandSet` (class, line 44) `class WinboxCommandSet(LazyOwnCommandSet)`
  - `_extract_flag` (function, line 514) `def _extract_flag(args, flag)`
  - `_extract_bool` (function, line 537) `def _extract_bool(args, flag)`
  - `do_winbox` (method, line 51) `def do_winbox(self, line)`
  - `_overview` (method, line 121) `def _overview(self)`
  - `_bootstrap` (method, line 127) `def _bootstrap(self)`
  - `_status` (method, line 151) `def _status(self)`
  - `_lifecycle` (method, line 178) `def _lifecycle(self, action, rest)`
  - `_lab_ready` (method, line 200) `def _lab_ready(self, rest)`
  - `_exec` (method, line 234) `def _exec(self, rest)`
  - `_interactive_passthrough` (method, line 268) `def _interactive_passthrough(self, action, rest)`
  - `_tools` (method, line 281) `def _tools(self, rest)`
  - `_upload` (method, line 292) `def _upload(self, rest)`
  - `_eventlogs` (method, line 302) `def _eventlogs(self, rest)`
  - `_net` (method, line 309) `def _net(self, rest)`
  - `_defense` (method, line 325) `def _defense(self, tool, rest)`
  - `_snapshot` (method, line 341) `def _snapshot(self, rest)`
  - `_resolve` (method, line 363) `def _resolve(self, rest)`
  - `_gym` (method, line 382) `def _gym(self, rest)`
  - `_gym_matrix` (method, line 418) `def _gym_matrix(self, action, rest)`
  - `_confirmed` (method, line 501) `def _confirmed(self, rest)`
  - `_lab_notify` (function, line 215) `def _lab_notify(message)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`

