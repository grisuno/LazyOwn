# cli/commands

cli/commands groups 137 files (py) around lazyown_set_config, needs_sudo, sudo_available, _retry_sudo_gate, redact_secrets. Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de...

```mermaid
graph LR
    cli["cli"]
    contrib["contrib"]
    core["core"]
    modules["modules"]
    root["root"]
    tests["tests"]
    cli -- "calls into" --> core
    cli -- "calls into" --> modules
    cli -- "calls into" --> root
    contrib -- "depends on" --> root
    modules -- "depends on" --> cli
    modules -- "calls into" --> core
    modules -- "calls into" --> root
    root -- "calls into" --> cli
    root -- "depends on" --> core
    tests -- "calls into" --> cli
    tests -- "calls into" --> core
    tests -- "calls into" --> modules
    tests -- "calls into" --> root
```

## cli (2.1)

cli groups 83 files (py) around EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap. Configurable Neon Box banner for the LazyOwn interactive shell.

## contrib (2.2)

contrib groups 1 files (py) around check_sudo, start_smb_server, start_smb_relay, CustomSMBRelayServer, __init__.

## core (2.3)

core groups 3 files (py) around check_rhost, check_lhost, check_lport, check_port, require_rhost. Build-time default constants loaded from ``config/defaults.toml``.

## modules (2.4)

modules groups 23 files (py) around ContainerResource, ContainerFinding, DockerEnumerator, __init__, is_socket_accessible. Git update contract for lazyaddons.

## root (2.5)

root groups 2 files (py) around lazyown_set_config, needs_sudo, sudo_available, _retry_sudo_gate, redact_secrets. Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de...

## tests (2.6)

tests groups 25 files (py) around _git, _repo_with_remote, _addon, test_every_shipped_addon_opts_in, test_update_disabled_is_skipped. Lazyaddon update BDD contract: opt-in, path-safe, dirty-tree aware.

**Files**:

- banner.py
- cli/banner_config.py
- cli/commands/_base.py
- cli/commands/ai.py
- cli/commands/anti_forensics.py
- cli/commands/applocker_bypass.py
- cli/commands/bitm.py
- cli/commands/bof_registry.py
- cli/commands/c2_profile.py
- cli/commands/c2_session.py
- cli/commands/caldera.py
- cli/commands/campaign.py
- cli/commands/catalog.py
- cli/commands/cicd.py
- cli/commands/cli_auth.py
- cli/commands/cloud.py
- cli/commands/collaboration.py
- cli/commands/command_and_control.py
- cli/commands/containers.py
- cli/commands/cred.py
- cli/commands/cred_migrated.py
- cli/commands/crystal_ball.py
- cli/commands/database.py
- cli/commands/defaults.py
- cli/commands/demo.py
- cli/commands/dns_exfil.py
- cli/commands/dpapi.py
- cli/commands/edr_detect.py
- cli/commands/encoding.py
- cli/commands/enum.py
- cli/commands/estorides.py
- cli/commands/evasive_payload.py
- cli/commands/exfiltration.py
- cli/commands/exploit.py
- cli/commands/exploitgym.py
- cli/commands/exposure_autofire.py
- cli/commands/exposure_intel.py
- cli/commands/exposure_inventory.py
- cli/commands/exposure_sentinel.py
- cli/commands/exposure_timeline.py
- cli/commands/golden_paths.py
- cli/commands/gym_matrix.py
- cli/commands/infra.py
- cli/commands/lab.py
- cli/commands/lateral.py
- cli/commands/lateral_migrated.py
- cli/commands/lazy_creds.py
- cli/commands/lazy_dorks.py
- cli/commands/lazy_oob.py
- cli/commands/lazy_passgen.py
- cli/commands/marketplace.py
- cli/commands/mobile_macos.py
- cli/commands/module_manager.py
- cli/commands/netattack.py
- cli/commands/nethelpers.py
- cli/commands/payload_generation.py
- cli/commands/persist.py
- cli/commands/phishing_wizard.py
- cli/commands/pivoting.py
- cli/commands/postexp.py
- cli/commands/postexp_migrated.py
- cli/commands/privilege_escalation.py
- cli/commands/purple_team.py
- cli/commands/resource_scripting.py
- cli/commands/retry_ops.py
- cli/commands/scan.py
- cli/commands/scan_migrated.py
- cli/commands/shellsys.py
- cli/commands/sleep_obfuscation.py
- cli/commands/socks_proxy.py
- cli/commands/supply_chain.py
- cli/commands/ux.py
- cli/commands/verb_admin.py
- cli/commands/winbox_gym.py
- cli/config_history.py
- cli/confirm.py
- cli/fuzzy_match.py
- cli/fuzzy_picker.py
- cli/graph_overlay.py
- cli/output_mode.py
- cli/plugin_tiers.py
- cli/purple_tui.py
- cli/scope_guard.py
- cli/session_hud.py
- contrib/legacy/lazysmbrelay.py
- core/defaults.py
- core/safe_import.py
- core/validators.py
- modules/addon_updater.py
- modules/beacon_config_builder.py
- modules/bitm_engine.py
- modules/bof_registry.py
- modules/c2_builder.py
- modules/c2_profile_engine.py
- modules/categories.py
- modules/cicd_enumerator.py
- modules/cloud_enum.py
- modules/dpapi_harvester.py
- modules/edr_detector.py
- modules/evasion_engine.py
- modules/evasive_payloads.py
- modules/exploitgym_gym.py
- modules/lab_runtime.py
- modules/lazycloud.py
- modules/lazyk8s.py
- modules/mfa_bypass.py
- modules/professional_report.py
- modules/sleep_obfuscation.py
- modules/socks_proxy.py
- modules/ttp_coverage.py
- modules/yara_scanner.py
- tests/test_addon_updater.py
- tests/test_api_key_resolution.py
- tests/test_banner_config.py
- tests/test_bdd_infra_range_report.py
- tests/test_beacon_config_builder.py
- tests/test_bof_registry.py
- tests/test_boyscout_contracts.py
- tests/test_c2_profile_engine.py
- tests/test_campaign_import_safety.py
- tests/test_categories.py
- tests/test_credentials_rotation.py
- tests/test_exploitgym_gym.py
- tests/test_fuzzy_picker.py
- tests/test_graph_overlay.py
- tests/test_implant_session_secrets.py
- tests/test_infra_disposable.py
- tests/test_input_fuzz.py
- tests/test_lab_target_visibility.py
- tests/test_plugin_tiers.py
- tests/test_prompt_readline_markers.py
- tests/test_prompt_refresh.py
- tests/test_require_guards.py
- tests/test_scope_guard.py
- tests/test_sleep_obfuscation.py
- tests/test_socks_proxy.py
- utils.py
