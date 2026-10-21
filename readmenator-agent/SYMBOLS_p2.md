# Symbols (page 2 of 44)
Previous: [SYMBOLS.md](SYMBOLS.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_filter_commands` | method | `cli/commands/catalog.py:88` | `def _filter_commands(self, commands, keyword)` |
| `_index` | method | `cli/commands/catalog.py:25` | `def _index(self)` |
| `_print_hits` | method | `cli/commands/catalog.py:95` | `def _print_hits(self, hits, label)` |
| `do_catalog` | method | `cli/commands/catalog.py:33` | `def do_catalog(self, line)` |
| `shlex_split` | function | `cli/commands/catalog.py:111` | `def shlex_split(text)` |
| `CICDCommandSet` | class | `cli/commands/cicd.py:27` | `class CICDCommandSet(LazyOwnCommandSet)` |
| `_extract` | method | `cli/commands/cicd.py:290` | `def _extract(args, flag)` |
| `do_cicd_scan` | method | `cli/commands/cicd.py:34` | `def do_cicd_scan(self, line)` |
| `do_cicd_secrets` | method | `cli/commands/cicd.py:97` | `def do_cicd_secrets(self, line)` |
| `do_gitlab_enum` | method | `cli/commands/cicd.py:185` | `def do_gitlab_enum(self, line)` |
| `do_jenkins_enum` | method | `cli/commands/cicd.py:140` | `def do_jenkins_enum(self, line)` |
| `do_mfa_bypass` | method | `cli/commands/cicd.py:231` | `def do_mfa_bypass(self, line)` |
| `CliAuthCommandSet` | class | `cli/commands/cli_auth.py:27` | `class CliAuthCommandSet(LazyOwnCommandSet)` |
| `do_login` | method | `cli/commands/cli_auth.py:34` | `def do_login(self, line)` |
| `do_logout` | method | `cli/commands/cli_auth.py:191` | `def do_logout(self, line)` |
| `do_register` | method | `cli/commands/cli_auth.py:117` | `def do_register(self, line)` |
| `do_whoami` | method | `cli/commands/cli_auth.py:224` | `def do_whoami(self, line)` |
| `CloudCommandSet` | class | `cli/commands/cloud.py:30` | `class CloudCommandSet(LazyOwnCommandSet)` |
| `_get_cloud_scanner` | method | `cli/commands/cloud.py:36` | `def _get_cloud_scanner(self)` |
| `do_cloud_buckets` | method | `cli/commands/cloud.py:98` | `def do_cloud_buckets(self, line)` |
| `do_cloud_enum` | method | `cli/commands/cloud.py:239` | `def do_cloud_enum(self, line)` |
| `do_cloud_iam` | method | `cli/commands/cloud.py:187` | `def do_cloud_iam(self, _line)` |
| `do_cloud_metadata` | method | `cli/commands/cloud.py:49` | `def do_cloud_metadata(self, _line)` |
| `do_cloud_scan` | method | `cli/commands/cloud.py:148` | `def do_cloud_scan(self, line)` |
| `CloudAttackCommandSet` | class | `cli/commands/cloud_attacks.py:17` | `class CloudAttackCommandSet(LazyOwnCommandSet)` |
| `do_aws_privesc` | method | `cli/commands/cloud_attacks.py:125` | `def do_aws_privesc(self, line)` |
| `do_cross_cloud` | method | `cli/commands/cloud_attacks.py:387` | `def do_cross_cloud(self, line)` |
| `do_entra_attack` | method | `cli/commands/cloud_attacks.py:23` | `def do_entra_attack(self, line)` |
| `do_gcp_privesc` | method | `cli/commands/cloud_attacks.py:215` | `def do_gcp_privesc(self, line)` |
| `do_k8s_attack` | method | `cli/commands/cloud_attacks.py:302` | `def do_k8s_attack(self, line)` |
| `do_saas_enum` | method | `cli/commands/cloud_attacks.py:470` | `def do_saas_enum(self, line)` |
| `CollaborationCommandSet` | class | `cli/commands/collaboration.py:20` | `class CollaborationCommandSet(LazyOwnCommandSet)` |
| `_get_collab` | method | `cli/commands/collaboration.py:26` | `def _get_collab(self)` |
| `_resolve_target` | method | `cli/commands/collaboration.py:38` | `def _resolve_target(self, target)` |
| `do_lock_target` | method | `cli/commands/collaboration.py:48` | `def do_lock_target(self, line)` |
| `do_share_finding` | method | `cli/commands/collaboration.py:199` | `def do_share_finding(self, line)` |
| `do_team_chat` | method | `cli/commands/collaboration.py:169` | `def do_team_chat(self, line)` |
| `do_team_status` | method | `cli/commands/collaboration.py:114` | `def do_team_status(self, line)` |
| `do_unlock_target` | method | `cli/commands/collaboration.py:89` | `def do_unlock_target(self, line)` |
| `CommandAndControlCommandSet` | class | `cli/commands/command_and_control.py:34` | `class CommandAndControlCommandSet(LazyOwnCommandSet)` |
| `do_c2_beacon_cmd` | method | `cli/commands/command_and_control.py:198` | `def do_c2_beacon_cmd(self, line)` |
| `do_c2_beacons` | method | `cli/commands/command_and_control.py:98` | `def do_c2_beacons(self, _line)` |
| `do_c2_implant` | method | `cli/commands/command_and_control.py:233` | `def do_c2_implant(self, line)` |
| `do_c2_keygen` | method | `cli/commands/command_and_control.py:134` | `def do_c2_keygen(self, _line)` |
| `do_c2_quickstart` | method | `cli/commands/command_and_control.py:151` | `def do_c2_quickstart(self, _line)` |
| `do_c2_status` | method | `cli/commands/command_and_control.py:41` | `def do_c2_status(self, _line)` |
| `CommandAndControlMigratedCommandSet` | class | `cli/commands/command_and_control_migrated.py:66` | `class CommandAndControlMigratedCommandSet(LazyOwnCommandSet)` |
| `_ability_to_step` | function | `cli/commands/command_and_control_migrated.py:2608` | `def _ability_to_step(ability)` |
| `_api` | function | `cli/commands/command_and_control_migrated.py:570` | `def _api(method, endpoint, payload)` |
| `_latest_sweep_evidence` | method | `cli/commands/command_and_control_migrated.py:1285` | `def _latest_sweep_evidence(self, target)` |
| `_load_ability` | function | `cli/commands/command_and_control_migrated.py:2601` | `def _load_ability(ability_file)` |
| `chain_file_exists` | function | `cli/commands/command_and_control_migrated.py:1765` | `def chain_file_exists(name)` |
| `do_apt_chain` | method | `cli/commands/command_and_control_migrated.py:1727` | `def do_apt_chain(self, line)` |
| `do_apt_playbook` | method | `cli/commands/command_and_control_migrated.py:2069` | `def do_apt_playbook(self, line)` |
| `do_atomic_agent` | method | `cli/commands/command_and_control_migrated.py:1447` | `def do_atomic_agent(self, line)` |
| `do_atomic_clean` | method | `cli/commands/command_and_control_migrated.py:1353` | `def do_atomic_clean(self, line)` |
| `do_atomic_emulate` | method | `cli/commands/command_and_control_migrated.py:1390` | `def do_atomic_emulate(self, line)` |
| `do_atomic_gen` | method | `cli/commands/command_and_control_migrated.py:1270` | `def do_atomic_gen(self, line)` |
| `do_atomic_shell` | method | `cli/commands/command_and_control_migrated.py:1314` | `def do_atomic_shell(self, line)` |
| `do_atomic_tests` | method | `cli/commands/command_and_control_migrated.py:1249` | `def do_atomic_tests(self, line)` |
| `do_attack_plan` | method | `cli/commands/command_and_control_migrated.py:1550` | `def do_attack_plan(self, line)` |
| `do_automsf` | method | `cli/commands/command_and_control_migrated.py:904` | `def do_automsf(self, line)` |
| `do_c2` | method | `cli/commands/command_and_control_migrated.py:421` | `def do_c2(self, line)` |
| `do_caldera` | method | `cli/commands/command_and_control_migrated.py:2528` | `def do_caldera(self, line)` |
| `do_caldera_export` | method | `cli/commands/command_and_control_migrated.py:2669` | `def do_caldera_export(self, line)` |
| `do_caldera_import` | method | `cli/commands/command_and_control_migrated.py:2577` | `def do_caldera_import(self, line)` |
| `do_chain_distill` | method | `cli/commands/command_and_control_migrated.py:2019` | `def do_chain_distill(self, line)` |
| `do_duckyspark` | method | `cli/commands/command_and_control_migrated.py:984` | `def do_duckyspark(self, line)` |
| `do_emp3r0r` | method | `cli/commands/command_and_control_migrated.py:1185` | `def do_emp3r0r(self, line)` |
| `do_empire` | method | `cli/commands/command_and_control_migrated.py:854` | `def do_empire(self, line)` |
| `do_generate_playbook` | method | `cli/commands/command_and_control_migrated.py:2292` | `def do_generate_playbook(self, line)` |
| `do_iis_webdav_upload_asp` | method | `cli/commands/command_and_control_migrated.py:949` | `def do_iis_webdav_upload_asp(self, line)` |
| `do_listener` | method | `cli/commands/command_and_control_migrated.py:543` | `def do_listener(self, line)` |
| `do_mitre_test` | method | `cli/commands/command_and_control_migrated.py:2189` | `def do_mitre_test(self, line)` |
| `do_msf` | method | `cli/commands/command_and_control_migrated.py:71` | `def do_msf(self, line)` |
| `do_msfrpc` | method | `cli/commands/command_and_control_migrated.py:713` | `def do_msfrpc(self, line)` |
| `do_my_playbook` | method | `cli/commands/command_and_control_migrated.py:2471` | `def do_my_playbook(self, line)` |
| `do_sandbox` | method | `cli/commands/command_and_control_migrated.py:671` | `def do_sandbox(self, line)` |
| `do_sliver_server` | method | `cli/commands/command_and_control_migrated.py:737` | `def do_sliver_server(self, line)` |
| `select_agent_flavour` | function | `cli/commands/command_and_control_migrated.py:43` | `def select_agent_flavour(run_tests, platform)` |
| `ContainerCommandSet` | class | `cli/commands/containers.py:30` | `class ContainerCommandSet(LazyOwnCommandSet)` |
| `do_container_detect` | method | `cli/commands/containers.py:334` | `def do_container_detect(self, _line)` |
| `do_container_escape` | method | `cli/commands/containers.py:169` | `def do_container_escape(self, _line)` |
| `do_docker_enum` | method | `cli/commands/containers.py:37` | `def do_docker_enum(self, _line)` |
| `do_k8s_enum` | method | `cli/commands/containers.py:101` | `def do_k8s_enum(self, _line)` |
| `do_k8s_pods` | method | `cli/commands/containers.py:239` | `def do_k8s_pods(self, line)` |
| `do_k8s_secrets` | method | `cli/commands/containers.py:283` | `def do_k8s_secrets(self, line)` |
| `CredentialAccessCommandSet` | class | `cli/commands/cred.py:23` | `class CredentialAccessCommandSet(LazyOwnCommandSet)` |
| `do_cewl` | method | `cli/commands/cred.py:75` | `def do_cewl(self, line)` |
| `do_creds_py` | method | `cli/commands/cred.py:93` | `def do_creds_py(self, line)` |
| `do_crunch` | method | `cli/commands/cred.py:67` | `def do_crunch(self, line)` |
| `do_hashcat` | method | `cli/commands/cred.py:30` | `def do_hashcat(self, line)` |
| `do_hydra` | method | `cli/commands/cred.py:47` | `def do_hydra(self, line)` |
| `do_john2hash` | method | `cli/commands/cred.py:39` | `def do_john2hash(self, line)` |
| `do_medusa` | method | `cli/commands/cred.py:59` | `def do_medusa(self, line)` |
| `do_spraykatz` | method | `cli/commands/cred.py:98` | `def do_spraykatz(self, line)` |
| `do_sshkey` | method | `cli/commands/cred.py:87` | `def do_sshkey(self, line)` |
| `CredMigratedCommandSet` | class | `cli/commands/cred_migrated.py:30` | `class CredMigratedCommandSet(LazyOwnCommandSet)` |
| `_rotate_existing_credentials` | method | `cli/commands/cred_migrated.py:34` | `def _rotate_existing_credentials(self, credentials_file_path)` |
| `alternate_case` | function | `cli/commands/cred_migrated.py:552` | `def alternate_case(s)` |
| `do_addusers` | method | `cli/commands/cred_migrated.py:706` | `def do_addusers(self, line)` |
| `do_adsso_spray` | method | `cli/commands/cred_migrated.py:1277` | `def do_adsso_spray(self, line)` |
| `do_crack_cisco_7_password` | method | `cli/commands/cred_migrated.py:1017` | `def do_crack_cisco_7_password(self, line)` |
| `do_createcredentials` | method | `cli/commands/cred_migrated.py:116` | `def do_createcredentials(self, line)` |
| `do_createhash` | method | `cli/commands/cred_migrated.py:62` | `def do_createhash(self, line)` |
| `do_createmail` | method | `cli/commands/cred_migrated.py:626` | `def do_createmail(self, line)` |
| `do_createusers_and_hashs` | method | `cli/commands/cred_migrated.py:1162` | `def do_createusers_and_hashs(self, line)` |
| `do_cred` | method | `cli/commands/cred_migrated.py:164` | `def do_cred(self, line)` |
| `do_cubespraying` | method | `cli/commands/cred_migrated.py:1039` | `def do_cubespraying(self, line)` |
| `do_dacledit` | method | `cli/commands/cred_migrated.py:291` | `def do_dacledit(self, line)` |
| `do_generatedic` | method | `cli/commands/cred_migrated.py:361` | `def do_generatedic(self, line)` |
| `do_john2keepas` | method | `cli/commands/cred_migrated.py:904` | `def do_john2keepas(self, line)` |
| `do_john2zip` | method | `cli/commands/cred_migrated.py:1101` | `def do_john2zip(self, line)` |
| `do_keepass` | method | `cli/commands/cred_migrated.py:953` | `def do_keepass(self, line)` |
| `do_passtightvnc` | method | `cli/commands/cred_migrated.py:728` | `def do_passtightvnc(self, line)` |
| `do_passwordspray` | method | `cli/commands/cred_migrated.py:674` | `def do_passwordspray(self, line)` |
| `do_refill_password` | method | `cli/commands/cred_migrated.py:1205` | `def do_refill_password(self, line)` |
| `do_rocky` | method | `cli/commands/cred_migrated.py:1241` | `def do_rocky(self, line)` |
| `do_searchhash` | method | `cli/commands/cred_migrated.py:217` | `def do_searchhash(self, line)` |
| `do_smalldic` | method | `cli/commands/cred_migrated.py:253` | `def do_smalldic(self, list)` |
| `do_transform` | method | `cli/commands/cred_migrated.py:775` | `def do_transform(self, line)` |
| `do_username_anarchy` | method | `cli/commands/cred_migrated.py:803` | `def do_username_anarchy(self, line)` |
| `double_combo` | function | `cli/commands/cred_migrated.py:409` | `def double_combo(name, characters, file, total, flag)` |
| `expand_regex` | function | `cli/commands/cred_migrated.py:568` | `def expand_regex(regex)` |
| `fifth_combo` | function | `cli/commands/cred_migrated.py:484` | `def fifth_combo(name, characters, file, total, flag)` |
| `fourth_combo` | function | `cli/commands/cred_migrated.py:458` | `def fourth_combo(name, characters, file, total, flag)` |
| `intercalate_combo` | function | `cli/commands/cred_migrated.py:536` | `def intercalate_combo(name, characters, file, total, flag)` |
| `single_combo` | function | `cli/commands/cred_migrated.py:386` | `def single_combo(name, characters, file, total, flag)` |
| `sixth_combo` | function | `cli/commands/cred_migrated.py:511` | `def sixth_combo(name, characters, file, total, flag)` |
| `triple_combo` | function | `cli/commands/cred_migrated.py:433` | `def triple_combo(name, characters, file, total, flag)` |
| `CrystalBallCommandSet` | class | `cli/commands/crystal_ball.py:20` | `class CrystalBallCommandSet(LazyOwnCommandSet)` |
| `_auto_detect_enum_file` | function | `cli/commands/crystal_ball.py:119` | `def _auto_detect_enum_file()` |
| `_safe_filename` | function | `cli/commands/crystal_ball.py:151` | `def _safe_filename(name)` |
| `do_crystal_ball` | method | `cli/commands/crystal_ball.py:27` | `def do_crystal_ball(self, line)` |
| `do_privesc_suggest` | method | `cli/commands/crystal_ball.py:110` | `def do_privesc_suggest(self, line)` |
| `DaemonControlCommandSet` | class | `cli/commands/daemon_ctl.py:17` | `class DaemonControlCommandSet(LazyOwnCommandSet)` |
| `do_daemon_approve` | method | `cli/commands/daemon_ctl.py:175` | `def do_daemon_approve(self, line)` |
| `do_daemon_focus` | method | `cli/commands/daemon_ctl.py:141` | `def do_daemon_focus(self, line)` |
| `do_daemon_mode` | method | `cli/commands/daemon_ctl.py:24` | `def do_daemon_mode(self, line)` |
| `do_daemon_pause` | method | `cli/commands/daemon_ctl.py:63` | `def do_daemon_pause(self, line)` |
| `do_daemon_resume` | method | `cli/commands/daemon_ctl.py:82` | `def do_daemon_resume(self, line)` |
| `do_daemon_veto` | method | `cli/commands/daemon_ctl.py:97` | `def do_daemon_veto(self, line)` |
| `do_gatecheck` | method | `cli/commands/daemon_ctl.py:224` | `def do_gatecheck(self, line)` |
| `DatabaseCommandSet` | class | `cli/commands/database.py:26` | `class DatabaseCommandSet(LazyOwnCommandSet)` |
| `_active_workspace` | method | `cli/commands/database.py:40` | `def _active_workspace(self)` |
| `_get_db` | method | `cli/commands/database.py:32` | `def _get_db(self)` |
| `do_db_creds` | method | `cli/commands/database.py:349` | `def do_db_creds(self, line)` |
| `do_db_export` | method | `cli/commands/database.py:509` | `def do_db_export(self, line)` |
| `do_db_hosts` | method | `cli/commands/database.py:124` | `def do_db_hosts(self, line)` |
| `do_db_import` | method | `cli/commands/database.py:471` | `def do_db_import(self, line)` |
| `do_db_init` | method | `cli/commands/database.py:57` | `def do_db_init(self, line)` |
| `do_db_loot` | method | `cli/commands/database.py:393` | `def do_db_loot(self, line)` |
| `do_db_notes` | method | `cli/commands/database.py:433` | `def do_db_notes(self, line)` |
| `do_db_services` | method | `cli/commands/database.py:185` | `def do_db_services(self, line)` |
| `do_db_status` | method | `cli/commands/database.py:543` | `def do_db_status(self, line)` |
| `do_db_vulns` | method | `cli/commands/database.py:213` | `def do_db_vulns(self, line)` |
| `do_db_workspace` | method | `cli/commands/database.py:75` | `def do_db_workspace(self, line)` |
| `do_retest` | method | `cli/commands/database.py:267` | `def do_retest(self, line)` |
| `shlex_split` | function | `cli/commands/database.py:560` | `def shlex_split(text)` |
| `DefaultsCommandSet` | class | `cli/commands/defaults.py:38` | `class DefaultsCommandSet(LazyOwnCommandSet)` |
| `_set` | method | `cli/commands/defaults.py:77` | `def _set(self, name, value)` |
| `_show` | method | `cli/commands/defaults.py:60` | `def _show(self, section)` |
| `do_defaults` | method | `cli/commands/defaults.py:45` | `def do_defaults(self, line)` |
| `DemoCommandSet` | class | `cli/commands/demo.py:22` | `class DemoCommandSet(LazyOwnCommandSet)` |
| `do_demo` | method | `cli/commands/demo.py:29` | `def do_demo(self, line)` |
| `DiagnosticsCommandSet` | class | `cli/commands/diagnostics.py:23` | `class DiagnosticsCommandSet(LazyOwnCommandSet)` |
| `do_sys_payload_keys` | method | `cli/commands/diagnostics.py:41` | `def do_sys_payload_keys(self, _statement)` |
| `do_sys_runtime` | method | `cli/commands/diagnostics.py:30` | `def do_sys_runtime(self, _statement)` |
| `DNSExfilCommandSet` | class | `cli/commands/dns_exfil.py:44` | `class DNSExfilCommandSet(LazyOwnCommandSet)` |
| `ExfilHandler` | class | `cli/commands/dns_exfil.py:227` | `class ExfilHandler(BaseHTTPRequestHandler)` |
| `_extract` | method | `cli/commands/dns_exfil.py:384` | `def _extract(args, flag)` |
| `_sanitize_filename` | function | `cli/commands/dns_exfil.py:36` | `def _sanitize_filename(name)` |
| `do_POST` | method | `cli/commands/dns_exfil.py:228` | `def do_POST(self)` |
| `do_dns_beacon` | method | `cli/commands/dns_exfil.py:51` | `def do_dns_beacon(self, line)` |
| `do_dns_beacon_status` | method | `cli/commands/dns_exfil.py:183` | `def do_dns_beacon_status(self, line)` |
| `do_dns_exfil_listen` | method | `cli/commands/dns_exfil.py:97` | `def do_dns_exfil_listen(self, line)` |
| `do_exfil_start_server` | method | `cli/commands/dns_exfil.py:338` | `def do_exfil_start_server(self, line)` |
| `do_http_exfil_server` | method | `cli/commands/dns_exfil.py:204` | `def do_http_exfil_server(self, line)` |
| `do_smb_exfil` | method | `cli/commands/dns_exfil.py:304` | `def do_smb_exfil(self, line)` |
| `log_message` | method | `cli/commands/dns_exfil.py:289` | `def log_message(self, fmt)` |
| `DPAPICommandSet` | class | `cli/commands/dpapi.py:23` | `class DPAPICommandSet(LazyOwnCommandSet)` |
| `_extract` | method | `cli/commands/dpapi.py:151` | `def _extract(args, flag)` |
| `do_dpapi_blob` | method | `cli/commands/dpapi.py:113` | `def do_dpapi_blob(self, line)` |
| `do_dpapi_harvest` | method | `cli/commands/dpapi.py:30` | `def do_dpapi_harvest(self, line)` |
| `do_dpapi_masterkeys` | method | `cli/commands/dpapi.py:66` | `def do_dpapi_masterkeys(self, line)` |
| `EDRDetectCommandSet` | class | `cli/commands/edr_detect.py:27` | `class EDRDetectCommandSet(LazyOwnCommandSet)` |
| `_extract` | method | `cli/commands/edr_detect.py:173` | `def _extract(args, flag)` |
| `do_edr_detect` | method | `cli/commands/edr_detect.py:34` | `def do_edr_detect(self, line)` |
| `do_edr_profile` | method | `cli/commands/edr_detect.py:84` | `def do_edr_profile(self, line)` |
| `do_edr_script` | method | `cli/commands/edr_detect.py:140` | `def do_edr_script(self, line)` |
| `EncodingCommandSet` | class | `cli/commands/encoding.py:30` | `class EncodingCommandSet(LazyOwnCommandSet)` |
| `apply_obfuscations` | function | `cli/commands/encoding.py:309` | `def apply_obfuscations(cmd)` |
| `do_base64decode` | method | `cli/commands/encoding.py:389` | `def do_base64decode(self, line)` |
| `do_base64encode` | method | `cli/commands/encoding.py:361` | `def do_base64encode(self, line)` |
| `do_decode` | method | `cli/commands/encoding.py:135` | `def do_decode(self, line)` |
| `do_encode` | method | `cli/commands/encoding.py:95` | `def do_encode(self, line)` |
| `do_encoderpayload` | method | `cli/commands/encoding.py:259` | `def do_encoderpayload(self, line)` |
| `do_encodewinbase64` | method | `cli/commands/encoding.py:420` | `def do_encodewinbase64(self, line)` |
| `do_hex_to_plaintext` | method | `cli/commands/encoding.py:509` | `def do_hex_to_plaintext(self, line)` |
| `do_ip2hex` | method | `cli/commands/encoding.py:483` | `def do_ip2hex(self, line)` |
| `do_rot` | method | `cli/commands/encoding.py:173` | `def do_rot(self, line)` |
| `do_rotf` | method | `cli/commands/encoding.py:213` | `def do_rotf(self, line)` |
| `do_urldecode` | method | `cli/commands/encoding.py:66` | `def do_urldecode(self, line)` |
| `do_urlencode` | method | `cli/commands/encoding.py:37` | `def do_urlencode(self, line)` |
| `double_base64_encode` | function | `cli/commands/encoding.py:281` | `def double_base64_encode(cmd)` |
| `EnumCommandSet` | class | `cli/commands/enum.py:31` | `class EnumCommandSet(LazyOwnCommandSet)` |
| `do_enum4linux` | method | `cli/commands/enum.py:528` | `def do_enum4linux(self, line)` |
| `do_getnpusers` | method | `cli/commands/enum.py:345` | `def do_getnpusers(self, line)` |
| `do_psexec` | method | `cli/commands/enum.py:390` | `def do_psexec(self, line)` |
| `do_psexec_py` | method | `cli/commands/enum.py:446` | `def do_psexec_py(self, line)` |
| `do_rpcclient` | method | `cli/commands/enum.py:558` | `def do_rpcclient(self, line)` |
| `do_rpcdump` | method | `cli/commands/enum.py:502` | `def do_rpcdump(self, line)` |
| `do_smbclient` | method | `cli/commands/enum.py:38` | `def do_smbclient(self, line)` |
| `do_smbclient_impacket` | method | `cli/commands/enum.py:108` | `def do_smbclient_impacket(self, line)` |
| `do_smbclient_py` | method | `cli/commands/enum.py:178` | `def do_smbclient_py(self, line)` |
| `do_smbmap` | method | `cli/commands/enum.py:225` | `def do_smbmap(self, line)` |
| `EstoridesCommandSet` | class | `cli/commands/estorides.py:51` | `class EstoridesCommandSet(LazyOwnCommandSet)` |
| `_check_estorides` | method | `cli/commands/estorides.py:57` | `def _check_estorides(self)` |
| `_green` | function | `cli/commands/estorides.py:47` | `def _green(text)` |
| `_preview_entities` | method | `cli/commands/estorides.py:319` | `def _preview_entities(self, entities)` |
| `_yellow` | function | `cli/commands/estorides.py:43` | `def _yellow(text)` |
| `do_estorides_import` | method | `cli/commands/estorides.py:189` | `def do_estorides_import(self, line)` |
| `do_estorides_loop` | method | `cli/commands/estorides.py:337` | `def do_estorides_loop(self, line)` |
| `do_estorides_seed` | method | `cli/commands/estorides.py:73` | `def do_estorides_seed(self, line)` |
| `do_estorides_surface` | method | `cli/commands/estorides.py:441` | `def do_estorides_surface(self, line)` |
| `EvasivePayloadCommandSet` | class | `cli/commands/evasive_payload.py:248` | `class EvasivePayloadCommandSet(LazyOwnCommandSet)` |
| `_apply_bypass` | function | `cli/commands/evasive_payload.py:615` | `def _apply_bypass(shellcode, technique, target_os)` |
| `_auto_select_bypass` | function | `cli/commands/evasive_payload.py:717` | `def _auto_select_bypass(target_os)` |
| `_extract_flag` | function | `cli/commands/evasive_payload.py:736` | `def _extract_flag(args, flag)` |
| `_format_ext` | function | `cli/commands/evasive_payload.py:731` | `def _format_ext(fmt)` |
| `_format_payload` | function | `cli/commands/evasive_payload.py:665` | `def _format_payload(shellcode, fmt, lhost, lport)` |
| `_generate_shellcode` | function | `cli/commands/evasive_payload.py:586` | `def _generate_shellcode(lhost, lport, target_os, arch)` |
| `_print_usage` | method | `cli/commands/evasive_payload.py:514` | `def _print_usage(self, fmt, path, lhost, lport)` |
| `do_detect_edr` | method | `cli/commands/evasive_payload.py:360` | `def do_detect_edr(self, line)` |
| `do_evasion` | method | `cli/commands/evasive_payload.py:533` | `def do_evasion(self, line)` |
| `do_evasive` | method | `cli/commands/evasive_payload.py:415` | `def do_evasive(self, line)` |
| `do_evasive_payload` | method | `cli/commands/evasive_payload.py:255` | `def do_evasive_payload(self, line)` |
| `do_mutate_shellcode` | method | `cli/commands/evasive_payload.py:307` | `def do_mutate_shellcode(self, line)` |
| `ExfiltrationCommandSet` | class | `cli/commands/exfiltration.py:327` | `class ExfiltrationCommandSet(LazyOwnCommandSet)` |
| `_extract_flag` | function | `cli/commands/exfiltration.py:170` | `def _extract_flag(args, flag)` |
| `_read_first_credential` | function | `cli/commands/exfiltration.py:147` | `def _read_first_credential(credentials_file)` |
| `_resolve_dploot_args` | method | `cli/commands/exfiltration.py:1089` | `def _resolve_dploot_args(self, action, domain)` |
| `_send_discord_file` | function | `cli/commands/exfiltration.py:231` | `def _send_discord_file(file_path, webhook_url, filename)` |
| `_send_telegram_file` | function | `cli/commands/exfiltration.py:208` | `def _send_telegram_file(file_path, bot_token, chat_id, caption)` |
| `_sessions_path` | function | `cli/commands/exfiltration.py:142` | `def _sessions_path(base_path)` |
| `_sign` | function | `cli/commands/exfiltration.py:296` | `def _sign(key, msg)` |
| `_split_file` | function | `cli/commands/exfiltration.py:187` | `def _split_file(file_path, output_dir, chunk_size)` |
| `_upload_s3_presigned` | function | `cli/commands/exfiltration.py:251` | `def _upload_s3_presigned(file_path, bucket, object_key, access_key, secret_key, region)` |
| `do_adgetpass` | method | `cli/commands/exfiltration.py:734` | `def do_adgetpass(self, line)` |
| `do_decrypt` | method | `cli/commands/exfiltration.py:361` | `def do_decrypt(self, line)` |
| `do_download_c2` | method | `cli/commands/exfiltration.py:1164` | `def do_download_c2(self, line)` |
| `do_dploot` | method | `cli/commands/exfiltration.py:1043` | `def do_dploot(self, line)` |
| `do_encrypt` | method | `cli/commands/exfiltration.py:334` | `def do_encrypt(self, line)` |
| `do_evidence` | method | `cli/commands/exfiltration.py:593` | `def do_evidence(self, line)` |
| `do_evilwinrm` | method | `cli/commands/exfiltration.py:389` | `def do_evilwinrm(self, line)` |
| `do_exfil_auto` | method | `cli/commands/exfiltration.py:1485` | `def do_exfil_auto(self, line)` |
| `do_exfil_discord` | method | `cli/commands/exfiltration.py:1271` | `def do_exfil_discord(self, line)` |
| `do_exfil_dns` | method | `cli/commands/exfiltration.py:1356` | `def do_exfil_dns(self, line)` |
| `do_exfil_gcs` | method | `cli/commands/exfiltration.py:1314` | `def do_exfil_gcs(self, line)` |
| `do_exfil_http` | method | `cli/commands/exfiltration.py:1415` | `def do_exfil_http(self, line)` |
| `do_exfil_s3` | method | `cli/commands/exfiltration.py:1181` | `def do_exfil_s3(self, line)` |
| `do_exfil_telegram` | method | `cli/commands/exfiltration.py:1226` | `def do_exfil_telegram(self, line)` |
| `do_getadusers` | method | `cli/commands/exfiltration.py:673` | `def do_getadusers(self, line)` |
| `do_getnthash_py` | method | `cli/commands/exfiltration.py:873` | `def do_getnthash_py(self, line)` |
| `do_getuserspns` | method | `cli/commands/exfiltration.py:534` | `def do_getuserspns(self, line)` |
| `do_gitdumper` | method | `cli/commands/exfiltration.py:568` | `def do_gitdumper(self, line)` |
| `do_gmsadumper` | method | `cli/commands/exfiltration.py:1004` | `def do_gmsadumper(self, line)` |
| `do_reg_py` | method | `cli/commands/exfiltration.py:824` | `def do_reg_py(self, line)` |
| `do_rsync` | method | `cli/commands/exfiltration.py:967` | `def do_rsync(self, line)` |
| `do_samdump2` | method | `cli/commands/exfiltration.py:799` | `def do_samdump2(self, line)` |
| `do_secretsdump` | method | `cli/commands/exfiltration.py:460` | `def do_secretsdump(self, line)` |
| `do_stage` | method | `cli/commands/exfiltration.py:1543` | `def do_stage(self, line)` |
| `do_unzip` | method | `cli/commands/exfiltration.py:851` | `def do_unzip(self, line)` |
| `do_upload_gofile` | method | `cli/commands/exfiltration.py:905` | `def do_upload_gofile(self, line)` |
| `download_file_from_c2` | method | `cli/commands/exfiltration.py:1125` | `def download_file_from_c2(self, file_name, clientid)` |
| `ExploitCommandSet` | class | `cli/commands/exploit.py:29` | `class ExploitCommandSet(LazyOwnCommandSet)` |
| `do_commix` | method | `cli/commands/exploit.py:86` | `def do_commix(self, line)` |
| `do_download_exploit` | method | `cli/commands/exploit.py:105` | `def do_download_exploit(self, line)` |
| `do_img2cookie` | method | `cli/commands/exploit.py:126` | `def do_img2cookie(self, line)` |
| `do_kusa` | method | `cli/commands/exploit.py:168` | `def do_kusa(self, line)` |
| `do_lazypwn` | method | `cli/commands/exploit.py:64` | `def do_lazypwn(self, line)` |
| `do_rev` | method | `cli/commands/exploit.py:69` | `def do_rev(self, line)` |
| `do_sqlmap` | method | `cli/commands/exploit.py:39` | `def do_sqlmap(self, line)` |
| `do_ticketer` | method | `cli/commands/exploit.py:178` | `def do_ticketer(self, line)` |
| `do_wrapper` | method | `cli/commands/exploit.py:150` | `def do_wrapper(self, line)` |
| `do_www` | method | `cli/commands/exploit.py:192` | `def do_www(self, line)` |
| `ExploitMigratedCommandSet` | class | `cli/commands/exploit_migrated.py:38` | `class ExploitMigratedCommandSet(LazyOwnCommandSet)` |
| `cacti_exploit` | function | `cli/commands/exploit_migrated.py:536` | `def cacti_exploit(config_file, host)` |
| `do_aclpwn_py` | method | `cli/commands/exploit_migrated.py:1614` | `def do_aclpwn_py(self, line)` |
| `do_adcs_check` | method | `cli/commands/exploit_migrated.py:2582` | `def do_adcs_check(self, line)` |
| `do_addspn_py` | method | `cli/commands/exploit_migrated.py:1662` | `def do_addspn_py(self, line)` |
| `do_autoblody` | method | `cli/commands/exploit_migrated.py:1805` | `def do_autoblody(self, line)` |
| `do_cacti_exploit` | method | `cli/commands/exploit_migrated.py:483` | `def do_cacti_exploit(self, line)` |
| `do_chain` | method | `cli/commands/exploit_migrated.py:2641` | `def do_chain(self, line)` |
| `do_cp` | method | `cli/commands/exploit_migrated.py:43` | `def do_cp(self, line)` |
| `do_createcookie` | method | `cli/commands/exploit_migrated.py:84` | `def do_createcookie(self, line)` |
| `do_createdll` | method | `cli/commands/exploit_migrated.py:344` | `def do_createdll(self, line)` |
| `do_digdug` | method | `cli/commands/exploit_migrated.py:2375` | `def do_digdug(self, line)` |
| `do_downloader` | method | `cli/commands/exploit_migrated.py:892` | `def do_downloader(self, line)` |
| `do_eternal` | method | `cli/commands/exploit_migrated.py:972` | `def do_eternal(self, line)` |
| `do_excelntdonut` | method | `cli/commands/exploit_migrated.py:2502` | `def do_excelntdonut(self, line)` |
| `do_exploit_recommend` | method | `cli/commands/exploit_migrated.py:2771` | `def do_exploit_recommend(self, line)` |
| `do_filtering` | method | `cli/commands/exploit_migrated.py:2220` | `def do_filtering(self, line)` |
| `do_gets4uticket_py` | method | `cli/commands/exploit_migrated.py:1567` | `def do_gets4uticket_py(self, line)` |
| `do_gettgtpkinit_py` | method | `cli/commands/exploit_migrated.py:1516` | `def do_gettgtpkinit_py(self, line)` |
| `do_greatSCT` | method | `cli/commands/exploit_migrated.py:2086` | `def do_greatSCT(self, line)` |
| `do_jwt_tool` | method | `cli/commands/exploit_migrated.py:2176` | `def do_jwt_tool(self, line)` |
| `do_krbrelayx_py` | method | `cli/commands/exploit_migrated.py:1760` | `def do_krbrelayx_py(self, line)` |
| `do_lfi` | method | `cli/commands/exploit_migrated.py:2044` | `def do_lfi(self, line)` |
| `do_lol` | method | `cli/commands/exploit_migrated.py:2246` | `def do_lol(self, line)` |
| `do_ms08_067_netapi` | method | `cli/commands/exploit_migrated.py:1053` | `def do_ms08_067_netapi(self, line)` |
| `do_ntpdate` | method | `cli/commands/exploit_migrated.py:2558` | `def do_ntpdate(self, line)` |
| `do_owneredit` | method | `cli/commands/exploit_migrated.py:1470` | `def do_owneredit(self, line)` |
| `do_padbuster` | method | `cli/commands/exploit_migrated.py:437` | `def do_padbuster(self, line)` |
| `do_powerserver` | method | `cli/commands/exploit_migrated.py:630` | `def do_powerserver(self, line)` |
| `do_printerbug_py` | method | `cli/commands/exploit_migrated.py:1706` | `def do_printerbug_py(self, line)` |
| `do_py3ttyup` | method | `cli/commands/exploit_migrated.py:128` | `def do_py3ttyup(self, line)` |
| `do_pyautomate` | method | `cli/commands/exploit_migrated.py:164` | `def do_pyautomate(self, line)` |
| `do_pyoracle2` | method | `cli/commands/exploit_migrated.py:1962` | `def do_pyoracle2(self, line)` |
| `do_pywhisker` | method | `cli/commands/exploit_migrated.py:1420` | `def do_pywhisker(self, line)` |
| `do_rejetto_hfs_exec` | method | `cli/commands/exploit_migrated.py:1016` | `def do_rejetto_hfs_exec(self, line)` |
| `do_seo` | method | `cli/commands/exploit_migrated.py:402` | `def do_seo(self, line)` |
| `do_sharpshooter` | method | `cli/commands/exploit_migrated.py:724` | `def do_sharpshooter(self, line)` |
| `do_shellfire` | method | `cli/commands/exploit_migrated.py:768` | `def do_shellfire(self, line)` |
| `do_shellshock` | method | `cli/commands/exploit_migrated.py:568` | `def do_shellshock(self, line)` |
| `do_sireprat` | method | `cli/commands/exploit_migrated.py:1247` | `def do_sireprat(self, line)` |
| `do_sqli` | method | `cli/commands/exploit_migrated.py:693` | `def do_sqli(self, line)` |
| `do_sqli_mssql_test` | method | `cli/commands/exploit_migrated.py:1924` | `def do_sqli_mssql_test(self, line)` |
| `do_sqsh` | method | `cli/commands/exploit_migrated.py:2131` | `def do_sqsh(self, line)` |
| `do_sshexploit` | method | `cli/commands/exploit_migrated.py:2433` | `def do_sshexploit(self, line)` |
| `do_template_helper_serializer` | method | `cli/commands/exploit_migrated.py:1135` | `def do_template_helper_serializer(self, line)` |
| `do_unicode_WAFbypass` | method | `cli/commands/exploit_migrated.py:1869` | `def do_unicode_WAFbypass(self, line)` |
| `do_upload_bypass` | method | `cli/commands/exploit_migrated.py:1359` | `def do_upload_bypass(self, line)` |
| `do_utf` | method | `cli/commands/exploit_migrated.py:2331` | `def do_utf(self, line)` |
| `do_winbase64payload` | method | `cli/commands/exploit_migrated.py:215` | `def do_winbase64payload(self, line)` |
| `do_xss` | method | `cli/commands/exploit_migrated.py:1090` | `def do_xss(self, line)` |
| `do_xsstrike` | method | `cli/commands/exploit_migrated.py:1179` | `def do_xsstrike(self, line)` |
| `setup_handler` | function | `cli/commands/exploit_migrated.py:513` | `def setup_handler(config_file, lhost, lport)` |
| `ExploitGymCommandSet` | class | `cli/commands/exploitgym.py:36` | `class ExploitGymCommandSet(LazyOwnCommandSet)` |
| `_egym_docs` | method | `cli/commands/exploitgym.py:289` | `def _egym_docs(self, _args)` |
| `_egym_list` | method | `cli/commands/exploitgym.py:149` | `def _egym_list(self, args)` |
| `_egym_pull` | method | `cli/commands/exploitgym.py:181` | `def _egym_pull(self, args)` |
| `_egym_run` | method | `cli/commands/exploitgym.py:198` | `def _egym_run(self, args)` |
| `_egym_score` | method | `cli/commands/exploitgym.py:258` | `def _egym_score(self, args)` |
| `_egym_setup` | method | `cli/commands/exploitgym.py:120` | `def _egym_setup(self, args)` |
| `_egym_status` | method | `cli/commands/exploitgym.py:90` | `def _egym_status(self, _args)` |
| `_egym_verify` | method | `cli/commands/exploitgym.py:245` | `def _egym_verify(self, args)` |
| `do_exploitgym` | method | `cli/commands/exploitgym.py:43` | `def do_exploitgym(self, line)` |
| `HelpUiCommandSet` | class | `cli/commands/help_ui.py:29` | `class HelpUiCommandSet(LazyOwnCommandSet)` |
| `_save` | function | `cli/commands/help_ui.py:67` | `def _save(key, value)` |
| `do_command_explorer` | method | `cli/commands/help_ui.py:254` | `def do_command_explorer(self, line)` |
| `do_config_status` | method | `cli/commands/help_ui.py:287` | `def do_config_status(self, line)` |
| `do_ctx` | method | `cli/commands/help_ui.py:242` | `def do_ctx(self, line)` |
| `do_ctx_help` | method | `cli/commands/help_ui.py:221` | `def do_ctx_help(self, line)` |
| `do_doctor` | method | `cli/commands/help_ui.py:334` | `def do_doctor(self, line)` |
| `do_help_phase` | method | `cli/commands/help_ui.py:175` | `def do_help_phase(self, line)` |
| `do_help_status` | method | `cli/commands/help_ui.py:208` | `def do_help_status(self, line)` |
| `do_karma` | method | `cli/commands/help_ui.py:369` | `def do_karma(self, line)` |
| `do_killchain` | method | `cli/commands/help_ui.py:455` | `def do_killchain(self, line)` |
| `do_phase` | method | `cli/commands/help_ui.py:421` | `def do_phase(self, line)` |
| `do_tgrep` | method | `cli/commands/help_ui.py:404` | `def do_tgrep(self, line)` |
| `do_tui_theme` | method | `cli/commands/help_ui.py:308` | `def do_tui_theme(self, line)` |
| `do_tutorial` | method | `cli/commands/help_ui.py:151` | `def do_tutorial(self, line)` |
| `do_wizard` | method | `cli/commands/help_ui.py:36` | `def do_wizard(self, line)` |
| `InfraCommandSet` | class | `cli/commands/infra.py:93` | `class InfraCommandSet(LazyOwnCommandSet)` |
| `_ask_provider` | method | `cli/commands/infra.py:326` | `def _ask_provider(self)` |
| `_binary_present` | function | `cli/commands/infra.py:65` | `def _binary_present(name)` |
| `_c2_port` | method | `cli/commands/infra.py:99` | `def _c2_port(self)` |
| `_deploy_cloud` | method | `cli/commands/infra.py:364` | `def _deploy_cloud(self, provider, region)` |
| `_deploy_local` | method | `cli/commands/infra.py:344` | `def _deploy_local(self)` |
| `_infra_deploy` | method | `cli/commands/infra.py:308` | `def _infra_deploy(self, args)` |
| `_infra_destroy` | method | `cli/commands/infra.py:411` | `def _infra_destroy(self, args)` |
| `_infra_redirector` | method | `cli/commands/infra.py:170` | `def _infra_redirector(self, args)` |
| `_infra_status` | method | `cli/commands/infra.py:447` | `def _infra_status(self)` |
| `_load_state` | method | `cli/commands/infra.py:110` | `def _load_state(self)` |
| `_parse_tunnel_urls` | function | `cli/commands/infra.py:77` | `def _parse_tunnel_urls(log_text)` |
| `_redirector_kill` | method | `cli/commands/infra.py:291` | `def _redirector_kill(self, args)` |
| `_redirector_list` | method | `cli/commands/infra.py:262` | `def _redirector_list(self)` |
| `_redirector_spawn` | method | `cli/commands/infra.py:202` | `def _redirector_spawn(self, count, port)` |
| `_run_capture` | function | `cli/commands/infra.py:52` | `def _run_capture(argv, timeout)` |
| `_save_state` | method | `cli/commands/infra.py:123` | `def _save_state(self, state)` |
| `do_infra` | method | `cli/commands/infra.py:136` | `def do_infra(self, line)` |
| `LabCommandSet` | class | `cli/commands/lab.py:81` | `class LabCommandSet(LazyOwnCommandSet)` |
| `_container_ip` | method | `cli/commands/lab.py:118` | `def _container_ip(self, container_name)` |
| `_container_name` | method | `cli/commands/lab.py:114` | `def _container_name(self, scenario)` |
| `_docker_available` | method | `cli/commands/lab.py:87` | `def _docker_available(self)` |
| `_ensure_range_secret` | method | `cli/commands/lab.py:531` | `def _ensure_range_secret(self, profile_dir)` |
| `_lab_ensure_web` | method | `cli/commands/lab.py:140` | `def _lab_ensure_web(self, scenario, container_name)` |
| `_lab_list` | method | `cli/commands/lab.py:248` | `def _lab_list(self)` |
| `_lab_migrate` | method | `cli/commands/lab.py:176` | `def _lab_migrate(self, scenario, container_name)` |
| `_lab_start` | method | `cli/commands/lab.py:262` | `def _lab_start(self, scenario)` |
| `_lab_status` | method | `cli/commands/lab.py:620` | `def _lab_status(self)` |
| `_lab_stop` | method | `cli/commands/lab.py:306` | `def _lab_stop(self, scenario)` |
| `_print_lab_target` | method | `cli/commands/lab.py:155` | `def _print_lab_target(self, scenario, container_name, ports)` |
| `_range_compose` | method | `cli/commands/lab.py:365` | `def _range_compose(self, profile)` |
| `_range_container_ip` | method | `cli/commands/lab.py:561` | `def _range_container_ip(self, container)` |
| `_range_container_state` | method | `cli/commands/lab.py:423` | `def _range_container_state(self, container)` |
| `_range_dispatch` | method | `cli/commands/lab.py:324` | `def _range_dispatch(self, args)` |
| `_range_list` | method | `cli/commands/lab.py:356` | `def _range_list(self)` |
| `_range_start` | method | `cli/commands/lab.py:384` | `def _range_start(self, profile)` |
| `_range_status` | method | `cli/commands/lab.py:608` | `def _range_status(self)` |
| `_range_stop` | method | `cli/commands/lab.py:590` | `def _range_stop(self, profile)` |
| `_range_verify` | method | `cli/commands/lab.py:478` | `def _range_verify(self, profile)` |
| `_range_wait_healthy` | method | `cli/commands/lab.py:446` | `def _range_wait_healthy(self, compose, timeout)` |
| `_running_containers` | method | `cli/commands/lab.py:100` | `def _running_containers(self)` |
| `_tcp_reachable` | method | `cli/commands/lab.py:514` | `def _tcp_reachable(host, port, timeout)` |
| `do_lab` | method | `cli/commands/lab.py:196` | `def do_lab(self, line)` |
| `LateralMovementCommandSet` | class | `cli/commands/lateral.py:24` | `class LateralMovementCommandSet(LazyOwnCommandSet)` |
| `do_chisel` | method | `cli/commands/lateral.py:43` | `def do_chisel(self, line)` |
| `do_ligolo` | method | `cli/commands/lateral.py:79` | `def do_ligolo(self, line)` |
| `do_nc` | method | `cli/commands/lateral.py:91` | `def do_nc(self, line)` |
| `do_ngrok` | method | `cli/commands/lateral.py:72` | `def do_ngrok(self, line)` |
| `do_set_proxychains` | method | `cli/commands/lateral.py:59` | `def do_set_proxychains(self, line)` |
| `do_socat` | method | `cli/commands/lateral.py:31` | `def do_socat(self, line)` |
| `do_ssh` | method | `cli/commands/lateral.py:114` | `def do_ssh(self, line)` |
| `do_wmiexec` | method | `cli/commands/lateral.py:106` | `def do_wmiexec(self, line)` |
| `LateralMigratedCommandSet` | class | `cli/commands/lateral_migrated.py:24` | `class LateralMigratedCommandSet(LazyOwnCommandSet)` |
| `do_addcli` | method | `cli/commands/lateral_migrated.py:1302` | `def do_addcli(self, line)` |
| `do_bloodyAD` | method | `cli/commands/lateral_migrated.py:229` | `def do_bloodyAD(self, line)` |
| `do_dcomexec` | method | `cli/commands/lateral_migrated.py:931` | `def do_dcomexec(self, line)` |
| `do_dominion` | method | `cli/commands/lateral_migrated.py:1317` | `def do_dominion(self, line)` |
| `do_getTGT` | method | `cli/commands/lateral_migrated.py:321` | `def do_getTGT(self, line)` |
| `do_gospherus` | method | `cli/commands/lateral_migrated.py:543` | `def do_gospherus(self, line)` |
| `do_id_rsa` | method | `cli/commands/lateral_migrated.py:101` | `def do_id_rsa(self, line)` |
| `do_lateral_mov_lin` | method | `cli/commands/lateral_migrated.py:1247` | `def do_lateral_mov_lin(self, line)` |
| `do_mssqlcli` | method | `cli/commands/lateral_migrated.py:613` | `def do_mssqlcli(self, line)` |
| `do_penelope` | method | `cli/commands/lateral_migrated.py:666` | `def do_penelope(self, line)` |
| `do_regeorg` | method | `cli/commands/lateral_migrated.py:823` | `def do_regeorg(self, line)` |
| `do_rnc` | method | `cli/commands/lateral_migrated.py:477` | `def do_rnc(self, line)` |
| `do_shadowsocks` | method | `cli/commands/lateral_migrated.py:404` | `def do_shadowsocks(self, line)` |
| `do_sshd` | method | `cli/commands/lateral_migrated.py:172` | `def do_sshd(self, line)` |
| `do_stormbreaker` | method | `cli/commands/lateral_migrated.py:777` | `def do_stormbreaker(self, line)` |
| `do_targetedKerberoas` | method | `cli/commands/lateral_migrated.py:871` | `def do_targetedKerberoas(self, line)` |
| `do_tord` | method | `cli/commands/lateral_migrated.py:369` | `def do_tord(self, line)` |
| `do_upload_c2` | method | `cli/commands/lateral_migrated.py:1002` | `def do_upload_c2(self, line)` |
| `do_vpn` | method | `cli/commands/lateral_migrated.py:29` | `def do_vpn(self, line)` |
| `do_wifipass` | method | `cli/commands/lateral_migrated.py:199` | `def do_wifipass(self, line)` |
| `do_wmiexecpro` | method | `cli/commands/lateral_migrated.py:1031` | `def do_wmiexecpro(self, line)` |
| `install_wmiexecpro` | function | `cli/commands/lateral_migrated.py:1070` | `def install_wmiexecpro()` |
| `LazyQueueCommandSet` | class | `cli/commands/lazyloop.py:29` | `class LazyQueueCommandSet(LazyOwnCommandSet)` |
| `_engine` | function | `cli/commands/lazyloop.py:22` | `def _engine()` |
| `do_lazy_approve` | method | `cli/commands/lazyloop.py:190` | `def do_lazy_approve(self, line)` |
| `do_lazy_delete` | method | `cli/commands/lazyloop.py:71` | `def do_lazy_delete(self, line)` |
| `do_lazy_findings` | method | `cli/commands/lazyloop.py:110` | `def do_lazy_findings(self, line)` |
| `do_lazy_fleet` | method | `cli/commands/lazyloop.py:212` | `def do_lazy_fleet(self, line)` |
| `do_lazy_intents` | method | `cli/commands/lazyloop.py:51` | `def do_lazy_intents(self, line)` |
| `do_lazy_mention` | method | `cli/commands/lazyloop.py:155` | `def do_lazy_mention(self, line)` |
| `do_lazy_orchestrator` | method | `cli/commands/lazyloop.py:277` | `def do_lazy_orchestrator(self, line)` |
| `do_lazy_sync` | method | `cli/commands/lazyloop.py:36` | `def do_lazy_sync(self, line)` |
| `do_lazy_verdict` | method | `cli/commands/lazyloop.py:132` | `def do_lazy_verdict(self, line)` |
| `do_lazy_view` | method | `cli/commands/lazyloop.py:305` | `def do_lazy_view(self, line)` |
| `LazyCommandSet` | class | `cli/commands/lazyops.py:35` | `class LazyCommandSet(LazyOwnCommandSet)` |
| `_agent_main_prompt` | method | `cli/commands/lazyops.py:1657` | `def _agent_main_prompt(self, task_id)` |
| `_agent_main_tools` | method | `cli/commands/lazyops.py:1540` | `def _agent_main_tools(self, task_id)` |
| `_engine` | function | `cli/commands/lazyops.py:28` | `def _engine()` |
| `_free_text` | method | `cli/commands/lazyops.py:62` | `def _free_text(args)` |
| `_require_task` | method | `cli/commands/lazyops.py:54` | `def _require_task(self, args)` |
| `_task_id` | method | `cli/commands/lazyops.py:41` | `def _task_id(self, args)` |
| `add_hint` | function | `cli/commands/lazyops.py:1592` | `def add_hint(text)` |
| `campaign_sitrep` | function | `cli/commands/lazyops.py:1579` | `def campaign_sitrep()` |
| `do_lazy_addon` | method | `cli/commands/lazyops.py:1989` | `def do_lazy_addon(self, line)` |
| `do_lazy_agent` | method | `cli/commands/lazyops.py:1668` | `def do_lazy_agent(self, line)` |
| `do_lazy_archive` | method | `cli/commands/lazyops.py:2470` | `def do_lazy_archive(self, line)` |
| `do_lazy_ask` | method | `cli/commands/lazyops.py:1514` | `def do_lazy_ask(self, line)` |
| `do_lazy_asset` | method | `cli/commands/lazyops.py:820` | `def do_lazy_asset(self, line)` |
| `do_lazy_broadcast` | method | `cli/commands/lazyops.py:608` | `def do_lazy_broadcast(self, line)` |
| `do_lazy_category` | method | `cli/commands/lazyops.py:2532` | `def do_lazy_category(self, line)` |
| `do_lazy_chat` | method | `cli/commands/lazyops.py:2553` | `def do_lazy_chat(self, line)` |
| `do_lazy_compact` | method | `cli/commands/lazyops.py:2369` | `def do_lazy_compact(self, line)` |
| `do_lazy_company` | method | `cli/commands/lazyops.py:1769` | `def do_lazy_company(self, line)` |
| `do_lazy_constraint` | method | `cli/commands/lazyops.py:762` | `def do_lazy_constraint(self, line)` |
| `do_lazy_context` | method | `cli/commands/lazyops.py:298` | `def do_lazy_context(self, line)` |
| `do_lazy_dispatch` | method | `cli/commands/lazyops.py:88` | `def do_lazy_dispatch(self, line)` |
| `do_lazy_enrich` | method | `cli/commands/lazyops.py:861` | `def do_lazy_enrich(self, line)` |
| `do_lazy_evidence` | method | `cli/commands/lazyops.py:1447` | `def do_lazy_evidence(self, line)` |
| `do_lazy_fact` | method | `cli/commands/lazyops.py:1399` | `def do_lazy_fact(self, line)` |
| `do_lazy_finding` | method | `cli/commands/lazyops.py:1195` | `def do_lazy_finding(self, line)` |
| `do_lazy_frontier` | method | `cli/commands/lazyops.py:503` | `def do_lazy_frontier(self, line)` |
| `do_lazy_gate` | method | `cli/commands/lazyops.py:2613` | `def do_lazy_gate(self, line)` |
| `do_lazy_goal` | method | `cli/commands/lazyops.py:723` | `def do_lazy_goal(self, line)` |
| `do_lazy_graph` | method | `cli/commands/lazyops.py:269` | `def do_lazy_graph(self, line)` |
| `do_lazy_guard` | method | `cli/commands/lazyops.py:1094` | `def do_lazy_guard(self, line)` |
| `do_lazy_hint` | method | `cli/commands/lazyops.py:643` | `def do_lazy_hint(self, line)` |
| `do_lazy_install` | method | `cli/commands/lazyops.py:2746` | `def do_lazy_install(self, line)` |
| `do_lazy_intent` | method | `cli/commands/lazyops.py:655` | `def do_lazy_intent(self, line)` |
| `do_lazy_intent_delete` | method | `cli/commands/lazyops.py:680` | `def do_lazy_intent_delete(self, line)` |
| `do_lazy_kill` | method | `cli/commands/lazyops.py:1291` | `def do_lazy_kill(self, line)` |
| `do_lazy_llm` | method | `cli/commands/lazyops.py:2232` | `def do_lazy_llm(self, line)` |
| `do_lazy_loop` | method | `cli/commands/lazyops.py:2658` | `def do_lazy_loop(self, line)` |
| `do_lazy_node` | method | `cli/commands/lazyops.py:1427` | `def do_lazy_node(self, line)` |
| `do_lazy_notify` | method | `cli/commands/lazyops.py:2095` | `def do_lazy_notify(self, line)` |
| `do_lazy_overview` | method | `cli/commands/lazyops.py:2465` | `def do_lazy_overview(self, line)` |
| `do_lazy_pause` | method | `cli/commands/lazyops.py:1303` | `def do_lazy_pause(self, line)` |

Next: [SYMBOLS_p3.md](SYMBOLS_p3.md)
