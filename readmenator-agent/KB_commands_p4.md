# Subsystem: commands (page 4 of 4)
Previous: [KB_commands_p3.md](KB_commands_p3.md)

## cli/commands/security.py
- Doc: OPSEC and security commands — risk scoring, credential sealing, rotation.
- Layer: utility
- Language: py
- Symbols:
  - `SecurityCommandSet` (class, line 20) `class SecurityCommandSet(LazyOwnCommandSet)`
  - `do_opsec` (method, line 26) `def do_opsec(self, line)`
  - `do_seal_credentials` (method, line 106) `def do_seal_credentials(self, _line)`
  - `do_rotate_aes` (method, line 127) `def do_rotate_aes(self, _line)`
  - `do_unseal_credentials` (method, line 150) `def do_unseal_credentials(self, _line)`
  - `do_crack_hashes` (method, line 170) `def do_crack_hashes(self, line)`
  - `complete_opsec` (method, line 267) `def complete_opsec(self, text, line, begidx, endidx)`
  - `complete_crack_hashes` (method, line 276) `def complete_crack_hashes(self, text, line, begidx, endidx)`
- Depends on: `cli/commands/_base.py`, `core/config.py`, `core/console.py`, `core/credential_vault.py`, `modules/hash_cracker.py`, `modules/opsec_scorer.py`

## cli/commands/session_ops.py
- Doc: Session and campaign operations extracted from the miscellaneous cluster.
- Layer: utility
- Language: py
- Symbols:
  - `SessionOpsCommandSet` (class, line 72) `class SessionOpsCommandSet(LazyOwnCommandSet)`
  - `do_note` (method, line 79) `def do_note(self, line)`
  - `do_l00t` (method, line 104) `def do_l00t(self, line)`
  - `do_loot` (method, line 153) `def do_loot(self, line)`
  - `do_pivot` (method, line 161) `def do_pivot(self, line)`
  - `do_tasks` (method, line 186) `def do_tasks(self, line)`
  - `do_scans` (method, line 219) `def do_scans(self, line)`
  - `do_sitrep` (method, line 236) `def do_sitrep(self, line)`
  - `do_assign` (method, line 253) `def do_assign(self, line)`
  - `do_tenant` (method, line 306) `def do_tenant(self, line)`
  - `do_scope` (method, line 379) `def do_scope(self, line)`
  - `do_show` (method, line 445) `def do_show(self, line)`
  - `do_list` (method, line 521) `def do_list(self, line)`
  - `do_run` (method, line 550) `def do_run(self, line)`
  - `do_payload` (method, line 589) `def do_payload(self, line)`
  - `do_next` (method, line 640) `def do_next(self, line)`
  - `do_chainmode` (method, line 684) `def do_chainmode(self, line)`
  - `do_engage` (method, line 735) `def do_engage(self, line)`
  - `do_pipeline` (method, line 862) `def do_pipeline(self, line)`
  - `do_lazyscript` (method, line 953) `def do_lazyscript(self, line)`
  - `do_hunt` (method, line 985) `def do_hunt(self, line)`
  - `do_resume` (method, line 1067) `def do_resume(self, line)`
  - `do_getseclist` (method, line 1089) `def do_getseclist(self, line)`
  - `do_download_resources` (method, line 1127) `def do_download_resources(self, line)`
  - `do_collab_join` (method, line 1160) `def do_collab_join(self, line)`
  - `do_kick` (method, line 1191) `def do_kick(self, line)`
  - `do_qa` (method, line 1240) `def do_qa(self, line)`
  - `do_clock` (method, line 1281) `def do_clock(self, line)`
  - `do_gencert` (method, line 1329) `def do_gencert(self, line)`
  - `do_load_session` (method, line 1341) `def do_load_session(self, line)`
  - `do_clone_site` (method, line 1391) `def do_clone_site(self, line)`
  - `do_msfshellcoder` (method, line 1437) `def do_msfshellcoder(self, line)`
  - `_flag_value` (method, line 799) `def _flag_value(flag_name)`
  - `_flag_value` (method, line 911) `def _flag_value(flag_name)`
- Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/autosuggest.py`, `cli/chain_mode.py`, `cli/commands/_base.py`, `cli/config_history.py`, `cli/ops_commands.py`, `cli/session_resumer.py`, `cli/show.py`, `core/config.py`, `modules/autonomous_exploit_engine.py`, `modules/lazy_rbac.py`, `modules/module_registry.py`, `modules/payload_factory.py`, `modules/pipeline_engine.py`, `skills/autonomous_daemon.py`, `utils.py`
- Imported by: `tests/test_session_ops_command_set.py`

## cli/commands/shellsys.py
- Doc: Local shell and system extracted from the miscellaneous cluster.
- Layer: utility
- Language: py
- Symbols:
  - `ShellSysCommandSet` (class, line 23) `class ShellSysCommandSet(LazyOwnCommandSet)`
  - `do_sh` (method, line 30) `def do_sh(self, line)`
  - `do_sys` (method, line 62) `def do_sys(self, line)`
  - `do_pwd` (method, line 110) `def do_pwd(self, line)`
  - `do_nano` (method, line 146) `def do_nano(self, line)`
  - `do_cron` (method, line 170) `def do_cron(self, line)`
  - `do_clean` (method, line 216) `def do_clean(self, line)`
  - `do_fixperm` (method, line 303) `def do_fixperm(self, line)`
  - `do_fixel` (method, line 336) `def do_fixel(self, line)`
  - `do_pop` (method, line 369) `def do_pop(self, line)`
  - `do_tab` (method, line 406) `def do_tab(self, line)`
  - `lazyrun_command` (method, line 205) `def lazyrun_command()`
- Depends on: `cli/commands/_base.py`, `core/safe_exec.py`, `utils.py`
- Imported by: `tests/test_shellsys_command_set.py`

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
  - `_parse_requirements` (method, line 282) `def _parse_requirements(filepath)`
  - `_parse_package_json` (method, line 307) `def _parse_package_json(filepath)`
  - `_parse_gemfile` (method, line 328) `def _parse_gemfile(filepath)`
  - `_parse_cargo_toml` (method, line 348) `def _parse_cargo_toml(filepath)`
  - `_parse_go_mod` (method, line 377) `def _parse_go_mod(filepath)`
  - `_parse_pom_xml` (method, line 397) `def _parse_pom_xml(filepath)`
  - `_pypi_exists` (method, line 425) `def _pypi_exists(package_name)`
  - `is_internal_name` (method, line 450) `def is_internal_name(name)`
  - `_extract_flag` (method, line 475) `def _extract_flag(args, flag)`
  - `do_depconfuse` (method, line 95) `def do_depconfuse(self, line)`
  - `do_package_squat` (method, line 140) `def do_package_squat(self, line)`
  - `do_depscan` (method, line 216) `def do_depscan(self, line)`
- Depends on: `cli/commands/_base.py`, `utils.py`

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
  - `do_suggest` (method, line 235) `def do_suggest(self, line)`
  - `_candidate_commands` (method, line 255) `def _candidate_commands(self)`
  - `_find_cheat_section` (method, line 272) `def _find_cheat_section(query)`
- Depends on: `cli/commands/_base.py`, `cli/config_history.py`, `cli/fuzzy_match.py`, `cli/output_mode.py`, `cli/session_hud.py`, `cli/toast_bus.py`, `core/config.py`, `core/console.py`, `utils.py`

