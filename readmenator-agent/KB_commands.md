# Subsystem: commands (page 1 of 4)
Pages: [KB_commands.md](KB_commands.md), [KB_commands_p2.md](KB_commands_p2.md), [KB_commands_p3.md](KB_commands_p3.md), [KB_commands_p4.md](KB_commands_p4.md)

## cli/commands/__init__.py
- Doc: Phase-scoped CommandSet modules.
- Layer: utility
- Language: py
- Imported by: `tests/test_improvements_spec.py`

## cli/commands/_base.py
- Doc: Base class for phase-scoped ``CommandSet`` modules.
- Layer: utility
- Language: py
- Symbols:
  - `extract_flag` (function, line 34) `def extract_flag(args, flag)`
  - `LazyOwnCommandSet` (class, line 51) `class LazyOwnCommandSet(CommandSet)`
  - `_resolve_shell` (method, line 65) `def _resolve_shell(self)`
  - `params` (method, line 86) `def params(self)`
  - `payload` (method, line 97) `def payload(self)`
  - `__getattr__` (method, line 110) `def __getattr__(self, name)`
  - `__setattr__` (method, line 162) `def __setattr__(self, name, value)`
- Depends on: `utils.py`
- Imported by: `cli/commands/_dormancy.py`, `cli/commands/active_directory.py`, `cli/commands/ai.py`, `cli/commands/anti_forensics.py`, `cli/commands/applocker_bypass.py`, `cli/commands/audit.py`, `cli/commands/automation.py`, `cli/commands/bitm.py`, `cli/commands/bof_registry.py`, `cli/commands/c2_profile.py`, `cli/commands/caldera.py`, `cli/commands/campaign.py`, `cli/commands/catalog.py`, `cli/commands/cicd.py`, `cli/commands/cli_auth.py`, `cli/commands/cloud.py`, `cli/commands/cloud_attacks.py`, `cli/commands/collaboration.py`, `cli/commands/command_and_control.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/containers.py`, `cli/commands/cred.py`, `cli/commands/cred_migrated.py`, `cli/commands/crystal_ball.py`, `cli/commands/daemon_ctl.py`, `cli/commands/database.py`, `cli/commands/demo.py`, `cli/commands/diagnostics.py`, `cli/commands/dns_exfil.py`, `cli/commands/dpapi.py`, `cli/commands/edr_detect.py`, `cli/commands/encoding.py`, `cli/commands/enum.py`, `cli/commands/estorides.py`, `cli/commands/evasive_payload.py`, `cli/commands/exfiltration.py`, `cli/commands/exploit.py`, `cli/commands/exploit_migrated.py`, `cli/commands/exploitgym.py`, `cli/commands/help_ui.py`, `cli/commands/infra.py`, `cli/commands/lab.py`, `cli/commands/lateral.py`, `cli/commands/lateral_migrated.py`, `cli/commands/marketplace.py`, `cli/commands/mcp_bridge.py`, `cli/commands/misc_migrated.py`, `cli/commands/mobile_macos.py`, `cli/commands/module_manager.py`, `cli/commands/nethelpers.py`, `cli/commands/opsec_cleanup.py`, `cli/commands/orchestration.py`, `cli/commands/payload_arsenal.py`, `cli/commands/payload_generation.py`, `cli/commands/persist.py`, `cli/commands/persist_migrated.py`, `cli/commands/phishing_wizard.py`, `cli/commands/pivoting.py`, `cli/commands/postexp.py`, `cli/commands/postexp_migrated.py`, `cli/commands/privilege_escalation.py`, `cli/commands/purple_team.py`, `cli/commands/pwn.py`, `cli/commands/recon.py`, `cli/commands/recon_migrated.py`, `cli/commands/redteam_gym.py`, `cli/commands/resource_scripting.py`, `cli/commands/scan.py`, `cli/commands/scan_migrated.py`, `cli/commands/security.py`, `cli/commands/session_ops.py`, `cli/commands/shellsys.py`, `cli/commands/sleep_obfuscation.py`, `cli/commands/socks_proxy.py`, `cli/commands/supply_chain.py`, `cli/commands/ux.py`, `tests/test_cli_command_sets.py`, `tests/test_command_set_migration.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_nethelpers_command_set.py`, `tests/test_prompt_refresh.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`

## cli/commands/_dormancy.py
- Doc: Dormancy marker for incrementally migrated command sets.
- Layer: utility
- Language: py
- Symbols:
  - `PendingCommandSet` (class, line 30) `class PendingCommandSet(LazyOwnCommandSet)`
  - `is_pending` (method, line 52) `def is_pending(cs_class)`
- Depends on: `cli/commands/_base.py`
- Imported by: `cli/registry.py`, `tests/test_command_set_migration.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_improvements_spec.py`, `tests/test_nethelpers_command_set.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`

## cli/commands/active_directory.py
- Doc: Active Directory attack commands — Kerberos, tickets, delegation, DACL, GPO, kerberoasting.
- Layer: utility
- Language: py
- Symbols:
  - `ActiveDirectoryCommandSet` (class, line 18) `class ActiveDirectoryCommandSet(LazyOwnCommandSet)`
  - `do_kerberos_ticket` (method, line 24) `def do_kerberos_ticket(self, line)`
  - `do_delegation_enum` (method, line 139) `def do_delegation_enum(self, line)`
  - `do_delegation_attack` (method, line 175) `def do_delegation_attack(self, line)`
  - `do_dacl_abuse` (method, line 199) `def do_dacl_abuse(self, line)`
  - `do_gpo_abuse` (method, line 233) `def do_gpo_abuse(self, line)`
  - `do_kerberoast` (method, line 277) `def do_kerberoast(self, line)`
  - `do_adcs_esc` (method, line 324) `def do_adcs_esc(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/dacl_abuse.py`, `modules/delegation_attacks.py`, `modules/gpo_abuse.py`, `modules/kerberoasting.py`, `modules/kerberos_tickets.py`

## cli/commands/ai.py
- Doc: Artificial Intelligence command set.
- Layer: utility
- Language: py
- Symbols:
  - `AiCommandSet` (class, line 70) `class AiCommandSet(LazyOwnCommandSet)`
  - `do_ask` (method, line 77) `def do_ask(self, line)`
  - `do_groq` (method, line 146) `def do_groq(self, line)`
  - `do_ai_playbook` (method, line 177) `def do_ai_playbook(self, line)`
  - `do_ai_toggle` (method, line 284) `def do_ai_toggle(self, _arg)`
  - `do_llm_budget` (method, line 301) `def do_llm_budget(self, line)`
- Depends on: `cli/commands/_base.py`, `cli/confirm.py`, `core/llm_budget.py`, `modules/killchain.py`, `modules/llm_adapter.py`, `modules/llm_factory.py`, `modules/llm_prompts.py`, `utils.py`
- Imported by: `tests/test_ai_commands_llm.py`

## cli/commands/anti_forensics.py
- Doc: Anti-Forensics command set.
- Layer: utility
- Language: py
- Symbols:
  - `AntiForensicsCommandSet` (class, line 31) `class AntiForensicsCommandSet(LazyOwnCommandSet)`
  - `do_wipe_logs` (method, line 38) `def do_wipe_logs(self, line)`
  - `do_wipe_timeline` (method, line 103) `def do_wipe_timeline(self, line)`
  - `do_shred` (method, line 150) `def do_shred(self, line)`
  - `do_wipe_free` (method, line 205) `def do_wipe_free(self, line)`
  - `do_clean_ad` (method, line 242) `def do_clean_ad(self, line)`
  - `do_cover_tracks` (method, line 303) `def do_cover_tracks(self, line)`
- Depends on: `cli/commands/_base.py`, `cli/confirm.py`, `cli/output_mode.py`, `core/hardening.py`, `utils.py`

## cli/commands/applocker_bypass.py
- Doc: AppLocker and WDAC bypass command set.
- Layer: utility
- Language: py
- Symbols:
  - `AppLockerBypassCommandSet` (class, line 99) `class AppLockerBypassCommandSet(LazyOwnCommandSet)`
  - `_get_lh` (method, line 105) `def _get_lh(self)`
  - `do_applocker_installutil` (method, line 109) `def do_applocker_installutil(self, line)`
  - `do_applocker_msbuild` (method, line 146) `def do_applocker_msbuild(self, line)`
  - `do_applocker_regsvcs` (method, line 173) `def do_applocker_regsvcs(self, line)`
  - `do_applocker_csc` (method, line 209) `def do_applocker_csc(self, line)`
  - `do_applocker_mshta` (method, line 240) `def do_applocker_mshta(self, line)`
  - `do_applocker_rundll32` (method, line 269) `def do_applocker_rundll32(self, line)`
  - `do_applocker_presentation` (method, line 298) `def do_applocker_presentation(self, line)`
- Depends on: `cli/commands/_base.py`, `utils.py`

## cli/commands/audit.py
- Doc: Audit-mode CommandSet: fuzzy finder, forms, status tail, transcript grep.
- Layer: utility
- Language: py
- Symbols:
  - `AuditCommandSet` (class, line 92) `class AuditCommandSet(LazyOwnCommandSet)`
  - `_read_credentials` (method, line 304) `def _read_credentials(shell)`
  - `__init__` (method, line 101) `def __init__(self)`
  - `_ensure_fuzzy` (method, line 110) `def _ensure_fuzzy(self)`
  - `_ensure_completer` (method, line 117) `def _ensure_completer(self)`
  - `_ensure_transcript` (method, line 138) `def _ensure_transcript(self)`
  - `_ensure_hot_reloader` (method, line 145) `def _ensure_hot_reloader(self)`
  - `do_fz` (method, line 160) `def do_fz(self, statement)`
  - `do_form` (method, line 178) `def do_form(self, statement)`
  - `do_status_tail` (method, line 196) `def do_status_tail(self, statement)`
  - `do_grep_log` (method, line 234) `def do_grep_log(self, statement)`
  - `do_reload_addons` (method, line 263) `def do_reload_addons(self, _statement)`
  - `do_audit_complete_keys` (method, line 288) `def do_audit_complete_keys(self, statement)`
- Depends on: `cli/cli_enhancements.py`, `cli/commands/_base.py`
- Imported by: `tests/test_cli_enhancements.py`

## cli/commands/automation.py
- Doc: Automation command set — credential reuse, conditional hooks, operator profiles.
- Layer: utility
- Language: py
- Symbols:
  - `AutomationCommandSet` (class, line 17) `class AutomationCommandSet(LazyOwnCommandSet)`
  - `do_cred_reuse` (method, line 24) `def do_cred_reuse(self, line)`
  - `do_cred_mark_failed` (method, line 57) `def do_cred_mark_failed(self, line)`
  - `do_hooks_list` (method, line 78) `def do_hooks_list(self, line)`
  - `do_hooks_enable` (method, line 101) `def do_hooks_enable(self, line)`
  - `do_hooks_add` (method, line 129) `def do_hooks_add(self, line)`
  - `do_hooks_remove` (method, line 150) `def do_hooks_remove(self, line)`
  - `do_hooks_fire` (method, line 172) `def do_hooks_fire(self, line)`
  - `do_operators` (method, line 202) `def do_operators(self, line)`
  - `do_operator_create` (method, line 229) `def do_operator_create(self, line)`
  - `do_operator_load` (method, line 264) `def do_operator_load(self, line)`
  - `do_operator_delete` (method, line 292) `def do_operator_delete(self, line)`
  - `do_hooks` (method, line 314) `def do_hooks(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/categories.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/operator_profiles.py`, `modules/state_manager.py`

## cli/commands/bitm.py
- Doc: Browser-in-the-Middle CLI command set.
- Layer: utility
- Language: py
- Symbols:
  - `BitMCommandSet` (class, line 24) `class BitMCommandSet(LazyOwnCommandSet)`
  - `do_bitm` (method, line 31) `def do_bitm(self, line)`
  - `_bitm_start` (method, line 94) `def _bitm_start(self, args)`
  - `_bitm_stop` (method, line 168) `def _bitm_stop(self)`
  - `_bitm_status` (method, line 191) `def _bitm_status(self)`
  - `_bitm_inject` (method, line 214) `def _bitm_inject(self, args)`
  - `_bitm_harvest` (method, line 239) `def _bitm_harvest(self)`
  - `_bitm_cleanup` (method, line 257) `def _bitm_cleanup(self)`
- Depends on: `cli/commands/_base.py`, `modules/bitm_engine.py`, `utils.py`

## cli/commands/bof_registry.py
- Doc: BOF marketplace CommandSet — Beacon Object File discovery, install, and execution.
- Layer: utility
- Language: py
- Symbols:
  - `BofMarketplaceCommandSet` (class, line 29) `class BofMarketplaceCommandSet(LazyOwnCommandSet)`
  - `_ensure_staging_dir` (method, line 36) `def _ensure_staging_dir()`
  - `_find_bof_object` (method, line 42) `def _find_bof_object(bof_name)`
  - `_stage_bof` (method, line 71) `def _stage_bof(self, bof_name)`
  - `_queue_command_on_c2` (method, line 89) `def _queue_command_on_c2(self, client_id, command)`
  - `do_bof_search` (method, line 142) `def do_bof_search(self, line)`
  - `do_bof_info` (method, line 163) `def do_bof_info(self, line)`
  - `do_bof_install` (method, line 196) `def do_bof_install(self, line)`
  - `do_bof_run` (method, line 226) `def do_bof_run(self, line)`
  - `do_bof_uninstall` (method, line 267) `def do_bof_uninstall(self, line)`
  - `do_bof_list` (method, line 289) `def do_bof_list(self, line)`
  - `do_bof_catalog` (method, line 321) `def do_bof_catalog(self, line)`
- Depends on: `cli/commands/_base.py`, `core/config.py`, `modules/beacon_config_builder.py`, `modules/bof_registry.py`, `utils.py`

## cli/commands/c2_profile.py
- Doc: C2 profile CommandSet — extended malleable C2 profiles (TLS, DNS, SMB, WS).
- Layer: utility
- Language: py
- Symbols:
  - `C2ProfileCommandSet` (class, line 18) `class C2ProfileCommandSet(LazyOwnCommandSet)`
  - `do_c2_profiles` (method, line 25) `def do_c2_profiles(self, line)`
  - `do_c2_tls` (method, line 50) `def do_c2_tls(self, line)`
  - `do_c2_dns` (method, line 69) `def do_c2_dns(self, line)`
  - `do_c2_rotate` (method, line 90) `def do_c2_rotate(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/c2_profile_engine.py`, `utils.py`

## cli/commands/caldera.py
- Doc: Caldera-style command set — operation lifecycle, TTP coverage, and planner.
- Layer: utility
- Language: py
- Symbols:
  - `_resolve_manager` (function, line 49) `def _resolve_manager()`
  - `_resolve_coverage` (function, line 53) `def _resolve_coverage()`
  - `_resolve_planner` (function, line 59) `def _resolve_planner(shell)`
  - `CalderaCommandSet` (class, line 66) `class CalderaCommandSet(LazyOwnCommandSet)`
  - `_shell` (method, line 72) `def _shell(self)`
  - `do_op_list` (method, line 80) `def do_op_list(self, line)`
  - `do_op_create` (method, line 96) `def do_op_create(self, line)`
  - `do_op_plan` (method, line 114) `def do_op_plan(self, line)`
  - `do_op_start` (method, line 141) `def do_op_start(self, line)`
  - `do_op_pause` (method, line 166) `def do_op_pause(self, line)`
  - `do_op_resume` (method, line 183) `def do_op_resume(self, line)`
  - `do_op_stop` (method, line 200) `def do_op_stop(self, line)`
  - `do_op_status` (method, line 217) `def do_op_status(self, line)`
  - `do_op_timeline` (method, line 249) `def do_op_timeline(self, line)`
  - `do_op_report` (method, line 272) `def do_op_report(self, line)`
  - `do_ttp_matrix` (method, line 290) `def do_ttp_matrix(self, line)`
  - `do_ttp_rebuild` (method, line 299) `def do_ttp_rebuild(self, line)`
  - `do_ttp_show` (method, line 309) `def do_ttp_show(self, line)`
  - `do_plan` (method, line 336) `def do_plan(self, line)`
  - `do_plan_detail` (method, line 364) `def do_plan_detail(self, line)`
  - `do_plan_apply` (method, line 391) `def do_plan_apply(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/ttp_coverage.py`, `utils.py`

## cli/commands/campaign.py
- Doc: Campaign export/import commands — portable engagement packages.
- Layer: utility
- Language: py
- Symbols:
  - `CampaignCommandSet` (class, line 36) `class CampaignCommandSet(LazyOwnCommandSet)`
  - `do_campaign` (method, line 43) `def do_campaign(self, line)`
  - `_gather_campaign_manifest` (method, line 92) `def _gather_campaign_manifest(self, name)`
  - `_campaign_export` (method, line 134) `def _campaign_export(self, name)`
  - `_campaign_import` (method, line 183) `def _campaign_import(self, package_path)`
  - `_campaign_list` (method, line 308) `def _campaign_list(self)`
  - `_campaign_status` (method, line 340) `def _campaign_status(self)`
- Depends on: `cli/commands/_base.py`, `modules/db.py`, `utils.py`

## cli/commands/catalog.py
- Doc: Command catalog — browse all registered commands by keyword, phase or category.
- Layer: utility
- Language: py
- Symbols:
  - `CatalogCommandSet` (class, line 19) `class CatalogCommandSet(LazyOwnCommandSet)`
  - `shlex_split` (method, line 111) `def shlex_split(text)`
  - `_index` (method, line 25) `def _index(self)`
  - `do_catalog` (method, line 33) `def do_catalog(self, line)`
  - `_filter_commands` (method, line 88) `def _filter_commands(self, commands, keyword)`
  - `_print_hits` (method, line 95) `def _print_hits(self, hits, label)`
- Depends on: `cli/commands/_base.py`, `utils.py`

## cli/commands/cicd.py
- Doc: CI/CD Enumeration command set.
- Layer: utility
- Language: py
- Symbols:
  - `CICDCommandSet` (class, line 27) `class CICDCommandSet(LazyOwnCommandSet)`
  - `do_cicd_scan` (method, line 34) `def do_cicd_scan(self, line)`
  - `do_cicd_secrets` (method, line 97) `def do_cicd_secrets(self, line)`
  - `do_jenkins_enum` (method, line 140) `def do_jenkins_enum(self, line)`
  - `do_gitlab_enum` (method, line 185) `def do_gitlab_enum(self, line)`
  - `do_mfa_bypass` (method, line 231) `def do_mfa_bypass(self, line)`
  - `_extract` (method, line 290) `def _extract(args, flag)`
- Depends on: `cli/commands/_base.py`, `modules/cicd_enumerator.py`, `modules/mfa_bypass.py`, `utils.py`

## cli/commands/cli_auth.py
- Doc: CLI authentication command set — login/logout/whoami.
- Layer: utility
- Language: py
- Symbols:
  - `CliAuthCommandSet` (class, line 27) `class CliAuthCommandSet(LazyOwnCommandSet)`
  - `do_login` (method, line 34) `def do_login(self, line)`
  - `do_register` (method, line 117) `def do_register(self, line)`
  - `do_logout` (method, line 191) `def do_logout(self, line)`
  - `do_whoami` (method, line 224) `def do_whoami(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/cli_auth.py`, `utils.py`

## cli/commands/cloud.py
- Doc: Cloud attack command set.
- Layer: utility
- Language: py
- Symbols:
  - `CloudCommandSet` (class, line 30) `class CloudCommandSet(LazyOwnCommandSet)`
  - `_get_cloud_scanner` (method, line 36) `def _get_cloud_scanner(self)`
  - `do_cloud_metadata` (method, line 49) `def do_cloud_metadata(self, _line)`
  - `do_cloud_buckets` (method, line 98) `def do_cloud_buckets(self, line)`
  - `do_cloud_scan` (method, line 148) `def do_cloud_scan(self, line)`
  - `do_cloud_iam` (method, line 187) `def do_cloud_iam(self, _line)`
  - `do_cloud_enum` (method, line 239) `def do_cloud_enum(self, line)`
- Depends on: `cli/commands/_base.py`, `cli/confirm.py`, `core/hardening.py`, `modules/cloud_enum.py`, `modules/lazycloud.py`, `utils.py`
- Imported by: `cli/commands/exfiltration.py`

## cli/commands/cloud_attacks.py
- Doc: Cloud attack commands — Azure AD/Entra ID, AWS, GCP, Kubernetes, cross-cloud, SaaS.
- Layer: utility
- Language: py
- Symbols:
  - `CloudAttackCommandSet` (class, line 17) `class CloudAttackCommandSet(LazyOwnCommandSet)`
  - `do_entra_attack` (method, line 23) `def do_entra_attack(self, line)`
  - `do_aws_privesc` (method, line 125) `def do_aws_privesc(self, line)`
  - `do_gcp_privesc` (method, line 215) `def do_gcp_privesc(self, line)`
  - `do_k8s_attack` (method, line 302) `def do_k8s_attack(self, line)`
  - `do_cross_cloud` (method, line 387) `def do_cross_cloud(self, line)`
  - `do_saas_enum` (method, line 470) `def do_saas_enum(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/aws_attacks.py`, `modules/cross_cloud.py`, `modules/entra_id_attacks.py`, `modules/gcp_attacks.py`, `modules/k8s_attacks.py`, `modules/saas_attacks.py`

## cli/commands/collaboration.py
- Doc: Collaboration CLI commands — multi-operator teamwork from the shell.
- Layer: utility
- Language: py
- Symbols:
  - `CollaborationCommandSet` (class, line 20) `class CollaborationCommandSet(LazyOwnCommandSet)`
  - `_get_collab` (method, line 26) `def _get_collab(self)`
  - `_resolve_target` (method, line 38) `def _resolve_target(self, target)`
  - `do_lock_target` (method, line 48) `def do_lock_target(self, line)`
  - `do_unlock_target` (method, line 89) `def do_unlock_target(self, line)`
  - `do_team_status` (method, line 114) `def do_team_status(self, line)`
  - `do_team_chat` (method, line 169) `def do_team_chat(self, line)`
  - `do_share_finding` (method, line 199) `def do_share_finding(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/collab_bp.py`, `modules/db.py`, `utils.py`

## cli/commands/command_and_control.py
- Doc: Command & Control command set.
- Layer: utility
- Language: py
- Symbols:
  - `CommandAndControlCommandSet` (class, line 34) `class CommandAndControlCommandSet(LazyOwnCommandSet)`
  - `do_c2_status` (method, line 41) `def do_c2_status(self, _line)`
  - `do_c2_beacons` (method, line 98) `def do_c2_beacons(self, _line)`
  - `do_c2_keygen` (method, line 134) `def do_c2_keygen(self, _line)`
  - `do_c2_quickstart` (method, line 151) `def do_c2_quickstart(self, _line)`
  - `do_c2_beacon_cmd` (method, line 198) `def do_c2_beacon_cmd(self, line)`
  - `do_c2_implant` (method, line 233) `def do_c2_implant(self, line)`
- Depends on: `cli/commands/_base.py`, `utils.py`

## cli/commands/command_and_control_migrated.py
- Doc: command_and_control commands migrated from lazyown.py.
- Layer: utility
- Language: py
- Symbols:
  - `CommandAndControlMigratedCommandSet` (class, line 37) `class CommandAndControlMigratedCommandSet(LazyOwnCommandSet)`
  - `do_msf` (method, line 42) `def do_msf(self, line)`
  - `do_c2` (method, line 392) `def do_c2(self, line)`
  - `do_listener` (method, line 514) `def do_listener(self, line)`
  - `do_sandbox` (method, line 642) `def do_sandbox(self, line)`
  - `do_msfrpc` (method, line 684) `def do_msfrpc(self, line)`
  - `do_sliver_server` (method, line 708) `def do_sliver_server(self, line)`
  - `do_empire` (method, line 825) `def do_empire(self, line)`
  - `do_automsf` (method, line 875) `def do_automsf(self, line)`
  - `do_iis_webdav_upload_asp` (method, line 911) `def do_iis_webdav_upload_asp(self, line)`
  - `do_duckyspark` (method, line 946) `def do_duckyspark(self, line)`
  - `do_emp3r0r` (method, line 1147) `def do_emp3r0r(self, line)`
  - `do_atomic_tests` (method, line 1211) `def do_atomic_tests(self, line)`
  - `do_atomic_gen` (method, line 1371) `def do_atomic_gen(self, line)`
  - `do_atomic_agent` (method, line 1555) `def do_atomic_agent(self, line)`
  - `do_attack_plan` (method, line 1655) `def do_attack_plan(self, line)`
  - `do_apt_playbook` (method, line 1779) `def do_apt_playbook(self, line)`
  - `do_mitre_test` (method, line 1899) `def do_mitre_test(self, line)`
  - `do_generate_playbook` (method, line 2002) `def do_generate_playbook(self, line)`
  - `do_my_playbook` (method, line 2181) `def do_my_playbook(self, line)`
  - `do_caldera` (method, line 2238) `def do_caldera(self, line)`
  - `do_caldera_import` (method, line 2287) `def do_caldera_import(self, line)`
  - `do_caldera_export` (method, line 2379) `def do_caldera_export(self, line)`
  - `_api` (method, line 541) `def _api(method, endpoint, payload)`
  - `_load_ability` (method, line 2311) `def _load_ability(ability_file)`
  - `_ability_to_step` (method, line 2318) `def _ability_to_step(ability)`
- Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/commands/_base.py`, `core/config.py`, `core/hardening.py`, `modules/apt_playbooks.py`, `modules/c2_builder.py`, `modules/listener_manager.py`, `utils.py`

## cli/commands/containers.py
- Doc: Container and Kubernetes attack command set.
- Layer: infrastructure
- Language: py
- Symbols:
  - `ContainerCommandSet` (class, line 30) `class ContainerCommandSet(LazyOwnCommandSet)`
  - `do_docker_enum` (method, line 37) `def do_docker_enum(self, _line)`
  - `do_k8s_enum` (method, line 101) `def do_k8s_enum(self, _line)`
  - `do_container_escape` (method, line 169) `def do_container_escape(self, _line)`
  - `do_k8s_pods` (method, line 239) `def do_k8s_pods(self, line)`
  - `do_k8s_secrets` (method, line 283) `def do_k8s_secrets(self, line)`
  - `do_container_detect` (method, line 334) `def do_container_detect(self, _line)`
- Depends on: `cli/commands/_base.py`, `modules/lazyk8s.py`, `utils.py`
- Imported by: `cli/command_form.py`, `cli/dashboard_tui.py`, `cli/graph_overlay.py`, `cli/palette_overlay.py`, `cli/purple_tui.py`, `cli/sessions_browser.py`, `cli/surface_tui.py`, `cli/timeline_browser.py`, `poc_tui/app.py`

## cli/commands/cred.py
- Doc: Credential Access command set (pending).
- Layer: utility
- Language: py
- Symbols:
  - `CredentialAccessCommandSet` (class, line 23) `class CredentialAccessCommandSet(LazyOwnCommandSet)`
  - `do_hashcat` (method, line 30) `def do_hashcat(self, line)`
  - `do_john2hash` (method, line 39) `def do_john2hash(self, line)`
  - `do_hydra` (method, line 47) `def do_hydra(self, line)`
  - `do_medusa` (method, line 59) `def do_medusa(self, line)`
  - `do_crunch` (method, line 67) `def do_crunch(self, line)`
  - `do_cewl` (method, line 75) `def do_cewl(self, line)`
  - `do_sshkey` (method, line 87) `def do_sshkey(self, line)`
  - `do_creds_py` (method, line 93) `def do_creds_py(self, line)`
  - `do_spraykatz` (method, line 98) `def do_spraykatz(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`

## cli/commands/cred_migrated.py
- Doc: cred commands migrated from lazyown.py.
- Layer: utility
- Language: py
- Symbols:
  - `CredMigratedCommandSet` (class, line 29) `class CredMigratedCommandSet(LazyOwnCommandSet)`
  - `_rotate_existing_credentials` (method, line 33) `def _rotate_existing_credentials(self, credentials_file_path)`
  - `do_createhash` (method, line 61) `def do_createhash(self, line)`
  - `do_createcredentials` (method, line 115) `def do_createcredentials(self, line)`
  - `do_cred` (method, line 163) `def do_cred(self, line)`
  - `do_searchhash` (method, line 216) `def do_searchhash(self, line)`
  - `do_smalldic` (method, line 252) `def do_smalldic(self, list)`
  - `do_dacledit` (method, line 290) `def do_dacledit(self, line)`
  - `do_generatedic` (method, line 360) `def do_generatedic(self, line)`
  - `do_createmail` (method, line 625) `def do_createmail(self, line)`
  - `do_passwordspray` (method, line 673) `def do_passwordspray(self, line)`
  - `do_addusers` (method, line 705) `def do_addusers(self, line)`
  - `do_passtightvnc` (method, line 727) `def do_passtightvnc(self, line)`
  - `do_transform` (method, line 774) `def do_transform(self, line)`
  - `do_username_anarchy` (method, line 802) `def do_username_anarchy(self, line)`
  - `do_john2keepas` (method, line 903) `def do_john2keepas(self, line)`
  - `do_keepass` (method, line 952) `def do_keepass(self, line)`
  - `do_crack_cisco_7_password` (method, line 1016) `def do_crack_cisco_7_password(self, line)`
  - `do_cubespraying` (method, line 1038) `def do_cubespraying(self, line)`
  - `do_john2zip` (method, line 1100) `def do_john2zip(self, line)`
  - `do_createusers_and_hashs` (method, line 1161) `def do_createusers_and_hashs(self, line)`
  - `do_refill_password` (method, line 1204) `def do_refill_password(self, line)`
  - `do_rocky` (method, line 1240) `def do_rocky(self, line)`
  - `do_adsso_spray` (method, line 1276) `def do_adsso_spray(self, line)`
  - `single_combo` (method, line 385) `def single_combo(name, characters, file, total, flag)`
  - `double_combo` (method, line 408) `def double_combo(name, characters, file, total, flag)`
  - `triple_combo` (method, line 432) `def triple_combo(name, characters, file, total, flag)`
  - `fourth_combo` (method, line 457) `def fourth_combo(name, characters, file, total, flag)`
  - `fifth_combo` (method, line 483) `def fifth_combo(name, characters, file, total, flag)`
  - `sixth_combo` (method, line 510) `def sixth_combo(name, characters, file, total, flag)`
  - `intercalate_combo` (method, line 535) `def intercalate_combo(name, characters, file, total, flag)`
  - `expand_regex` (method, line 567) `def expand_regex(regex)`
  - `alternate_case` (method, line 551) `def alternate_case(s)`
- Depends on: `cli/commands/_base.py`, `utils.py`
- Imported by: `tests/test_credentials_rotation.py`

## cli/commands/crystal_ball.py
- Doc: Crystal Ball CLI command set — privilege escalation vector prediction.
- Layer: utility
- Language: py
- Symbols:
  - `CrystalBallCommandSet` (class, line 20) `class CrystalBallCommandSet(LazyOwnCommandSet)`
  - `_auto_detect_enum_file` (method, line 119) `def _auto_detect_enum_file()`
  - `_safe_filename` (method, line 151) `def _safe_filename(name)`
  - `do_crystal_ball` (method, line 27) `def do_crystal_ball(self, line)`
  - `do_privesc_suggest` (method, line 110) `def do_privesc_suggest(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/privesc_predictor.py`, `utils.py`

## cli/commands/daemon_ctl.py
- Doc: Autonomous daemon control extracted from the miscellaneous cluster.
- Layer: utility
- Language: py
- Symbols:
  - `DaemonControlCommandSet` (class, line 17) `class DaemonControlCommandSet(LazyOwnCommandSet)`
  - `do_daemon_mode` (method, line 24) `def do_daemon_mode(self, line)`
  - `do_daemon_pause` (method, line 61) `def do_daemon_pause(self, line)`
  - `do_daemon_resume` (method, line 79) `def do_daemon_resume(self, line)`
  - `do_daemon_veto` (method, line 93) `def do_daemon_veto(self, line)`
  - `do_daemon_focus` (method, line 136) `def do_daemon_focus(self, line)`
  - `do_daemon_approve` (method, line 169) `def do_daemon_approve(self, line)`
- Depends on: `cli/commands/_base.py`, `skills/daemon_control.py`, `utils.py`
- Imported by: `tests/test_daemon_ctl_command_set.py`

## cli/commands/database.py
- Doc: Database commands — workspace isolation, host/service/vuln management, nmap import, export, and...
- Layer: data_access
- Language: py
- Symbols:
  - `DatabaseCommandSet` (class, line 24) `class DatabaseCommandSet(LazyOwnCommandSet)`
  - `shlex_split` (method, line 476) `def shlex_split(text)`
  - `_get_db` (method, line 30) `def _get_db(self)`
  - `_active_workspace` (method, line 38) `def _active_workspace(self)`
  - `do_db_init` (method, line 55) `def do_db_init(self, line)`
  - `do_db_workspace` (method, line 73) `def do_db_workspace(self, line)`
  - `do_db_hosts` (method, line 122) `def do_db_hosts(self, line)`
  - `do_db_services` (method, line 183) `def do_db_services(self, line)`
  - `do_db_vulns` (method, line 211) `def do_db_vulns(self, line)`
  - `do_db_creds` (method, line 265) `def do_db_creds(self, line)`
  - `do_db_loot` (method, line 309) `def do_db_loot(self, line)`
  - `do_db_notes` (method, line 349) `def do_db_notes(self, line)`
  - `do_db_import` (method, line 387) `def do_db_import(self, line)`
  - `do_db_export` (method, line 425) `def do_db_export(self, line)`
  - `do_db_status` (method, line 459) `def do_db_status(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/db.py`, `utils.py`

## cli/commands/demo.py
- Doc: End-to-end demo command — MCP registration plus the golden path.
- Layer: utility
- Language: py
- Symbols:
  - `DemoCommandSet` (class, line 22) `class DemoCommandSet(LazyOwnCommandSet)`
  - `do_demo` (method, line 29) `def do_demo(self, line)`
- Depends on: `cli/commands/_base.py`, `utils.py`

## cli/commands/diagnostics.py
- Doc: Diagnostics CommandSet (Tier 2 pilot).
- Layer: utility
- Language: py
- Symbols:
  - `DiagnosticsCommandSet` (class, line 23) `class DiagnosticsCommandSet(LazyOwnCommandSet)`
  - `do_lazy_runtime` (method, line 30) `def do_lazy_runtime(self, _statement)`
  - `do_lazy_payload_keys` (method, line 41) `def do_lazy_payload_keys(self, _statement)`
- Depends on: `cli/commands/_base.py`
- Imported by: `tests/test_cli_command_sets.py`


Next: [KB_commands_p2.md](KB_commands_p2.md)
