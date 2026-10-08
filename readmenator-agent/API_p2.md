# API (page 2 of 20)
Previous: [API.md](API.md)

## cli/commands/daemon_ctl.py
Depends on: `cli/commands/_base.py`, `skills/daemon_control.py`, `utils.py`
Imported by: `tests/test_daemon_ctl_command_set.py`
- `DaemonControlCommandSet.do_daemon_mode` (method) `cli/commands/daemon_ctl.py:24` `def do_daemon_mode(self, line)` -- Switch the autonomous daemon between auto, approval and paused modes.
- `DaemonControlCommandSet.do_daemon_pause` (method) `cli/commands/daemon_ctl.py:61` `def do_daemon_pause(self, line)` -- Pause the autonomous daemon before its next step.
- `DaemonControlCommandSet.do_daemon_resume` (method) `cli/commands/daemon_ctl.py:79` `def do_daemon_resume(self, line)` -- Resume the autonomous daemon (switch mode to auto).
- `DaemonControlCommandSet.do_daemon_veto` (method) `cli/commands/daemon_ctl.py:93` `def do_daemon_veto(self, line)` -- Add or clear vetoed command first-tokens for the autonomous daemon.
- `DaemonControlCommandSet.do_daemon_focus` (method) `cli/commands/daemon_ctl.py:136` `def do_daemon_focus(self, line)` -- Restrict the autonomous daemon to a set of focus targets.
- `DaemonControlCommandSet.do_daemon_approve` (method) `cli/commands/daemon_ctl.py:169` `def do_daemon_approve(self, line)` -- Approve or veto the daemon's currently-pending action.

## cli/commands/database.py
Depends on: `cli/commands/_base.py`, `modules/db.py`, `utils.py`
- `DatabaseCommandSet.do_db_init` (method) `cli/commands/database.py:55` `def do_db_init(self, line)` -- Initialize the database (creates schema if not exists).
- `DatabaseCommandSet.do_db_workspace` (method) `cli/commands/database.py:73` `def do_db_workspace(self, line)` -- Manage workspaces (list, create, switch, delete).
- `DatabaseCommandSet.do_db_hosts` (method) `cli/commands/database.py:122` `def do_db_hosts(self, line)` -- List or add hosts in the active workspace.
- `DatabaseCommandSet.do_db_services` (method) `cli/commands/database.py:183` `def do_db_services(self, line)` -- List all services in the active workspace.
- `DatabaseCommandSet.do_db_vulns` (method) `cli/commands/database.py:211` `def do_db_vulns(self, line)` -- List or add vulnerabilities.
- `DatabaseCommandSet.do_db_creds` (method) `cli/commands/database.py:265` `def do_db_creds(self, line)` -- List or add credentials.
- `DatabaseCommandSet.do_db_loot` (method) `cli/commands/database.py:309` `def do_db_loot(self, line)` -- List or add loot items.
- `DatabaseCommandSet.do_db_notes` (method) `cli/commands/database.py:349` `def do_db_notes(self, line)` -- List or add notes.
- `DatabaseCommandSet.do_db_import` (method) `cli/commands/database.py:387` `def do_db_import(self, line)` -- Import scan results into the database.
- `DatabaseCommandSet.do_db_export` (method) `cli/commands/database.py:425` `def do_db_export(self, line)` -- Export database table to CSV.
- `DatabaseCommandSet.do_db_status` (method) `cli/commands/database.py:459` `def do_db_status(self, line)` -- Show entity counts for the active workspace.
- `DatabaseCommandSet.shlex_split` (method) `cli/commands/database.py:476` `def shlex_split(text)` -- Split text like shlex.split but handle empty strings gracefully.

## cli/commands/demo.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `DemoCommandSet.do_demo` (method) `cli/commands/demo.py:29` `def do_demo(self, line)` -- Run the end-to-end demo: MCP registration, session init, recommend, scan.

## cli/commands/diagnostics.py
Depends on: `cli/commands/_base.py`
Imported by: `tests/test_cli_command_sets.py`
- `DiagnosticsCommandSet.do_lazy_runtime` (method) `cli/commands/diagnostics.py:30` `def do_lazy_runtime(self, _statement)` -- Print interpreter, platform and core LazyOwn paths.
- `DiagnosticsCommandSet.do_lazy_payload_keys` (method) `cli/commands/diagnostics.py:41` `def do_lazy_payload_keys(self, _statement)` -- List the keys currently present in the parent shell's payload.

## cli/commands/dns_exfil.py
Depends on: `cli/commands/_base.py`, `modules/backdoor/server.c`, `modules/dns_beacon.py`, `utils.py`
- `DNSExfilCommandSet.do_dns_beacon` (method) `cli/commands/dns_exfil.py:51` `def do_dns_beacon(self, line)` -- Start a DNS tunneling beacon.
- `DNSExfilCommandSet.do_dns_exfil_listen` (method) `cli/commands/dns_exfil.py:97` `def do_dns_exfil_listen(self, line)` -- Start a DNS exfiltration listener on UDP port 53.
- `DNSExfilCommandSet.do_dns_beacon_status` (method) `cli/commands/dns_exfil.py:183` `def do_dns_beacon_status(self, line)` -- Show status of all DNS beacons.
- `DNSExfilCommandSet.do_http_exfil_server` (method) `cli/commands/dns_exfil.py:204` `def do_http_exfil_server(self, line)` -- Start a minimal HTTP exfiltration receiver.
- `ExfilHandler.do_POST` (method) `cli/commands/dns_exfil.py:228` `def do_POST(self)`
- `ExfilHandler.log_message` (method) `cli/commands/dns_exfil.py:289` `def log_message(self, fmt)`
- `ExfilHandler.do_smb_exfil` (method) `cli/commands/dns_exfil.py:304` `def do_smb_exfil(self, line)` -- Exfiltrate files to an SMB share on the attacker machine.
- `ExfilHandler.do_exfil_start_server` (method) `cli/commands/dns_exfil.py:338` `def do_exfil_start_server(self, line)` -- Start all required exfiltration listeners.

## cli/commands/dpapi.py
Depends on: `cli/commands/_base.py`, `modules/dpapi_harvester.py`, `utils.py`
- `DPAPICommandSet.do_dpapi_harvest` (method) `cli/commands/dpapi.py:30` `def do_dpapi_harvest(self, line)` -- Harvest all DPAPI-protected credentials from the local machine.
- `DPAPICommandSet.do_dpapi_masterkeys` (method) `cli/commands/dpapi.py:66` `def do_dpapi_masterkeys(self, line)` -- List and extract DPAPI master keys.
- `DPAPICommandSet.do_dpapi_blob` (method) `cli/commands/dpapi.py:113` `def do_dpapi_blob(self, line)` -- Decrypt a DPAPI blob offline.

## cli/commands/edr_detect.py
Depends on: `cli/commands/_base.py`, `modules/edr_detector.py`, `utils.py`
- `EDRDetectCommandSet.do_edr_detect` (method) `cli/commands/edr_detect.py:34` `def do_edr_detect(self, line)` -- Detect EDR/AV products on the target.
- `EDRDetectCommandSet.do_edr_profile` (method) `cli/commands/edr_detect.py:84` `def do_edr_profile(self, line)` -- Generate an evasion profile based on detected EDR.
- `EDRDetectCommandSet.do_edr_script` (method) `cli/commands/edr_detect.py:140` `def do_edr_script(self, line)` -- Generate a PowerShell EDR detection script.

## cli/commands/encoding.py
Depends on: `cli/commands/_base.py`, `utils.py`
Imported by: `tests/test_encoding_command_set.py`
- `EncodingCommandSet.do_urlencode` (method) `cli/commands/encoding.py:37` `def do_urlencode(self, line)` -- Encode a string for URL.
- `EncodingCommandSet.do_urldecode` (method) `cli/commands/encoding.py:66` `def do_urldecode(self, line)` -- Decode a URL-encoded string.
- `EncodingCommandSet.do_encode` (method) `cli/commands/encoding.py:95` `def do_encode(self, line)` -- Encodes a string using the specified shift value and substitution key.
- `EncodingCommandSet.do_decode` (method) `cli/commands/encoding.py:135` `def do_decode(self, line)` -- Decode a string using the specified shift value and substitution key.
- `EncodingCommandSet.do_rot` (method) `cli/commands/encoding.py:173` `def do_rot(self, line)` -- Apply a ROT (rotation) substitution cipher to the given string.
- `EncodingCommandSet.do_rotf` (method) `cli/commands/encoding.py:213` `def do_rotf(self, line)` -- Apply a ROT (rotation) substitution cipher to the given extension.
- `EncodingCommandSet.do_encoderpayload` (method) `cli/commands/encoding.py:260` `def do_encoderpayload(self, line)` -- Applies various obfuscations to a given command line string to create multiple obfuscated versions.
- `EncodingCommandSet.double_base64_encode` (method) `cli/commands/encoding.py:281` `def double_base64_encode(cmd)` -- Perform double Base64 encoding on the given command.
- `EncodingCommandSet.apply_obfuscations` (method) `cli/commands/encoding.py:309` `def apply_obfuscations(cmd)` -- Generate a list of obfuscated commands based on the given input command.
- `EncodingCommandSet.do_base64encode` (method) `cli/commands/encoding.py:361` `def do_base64encode(self, line)` -- Encodes a given string into Base64 format.
- `EncodingCommandSet.do_base64decode` (method) `cli/commands/encoding.py:389` `def do_base64decode(self, line)` -- Decodes a Base64 encoded string.
- `EncodingCommandSet.do_encodewinbase64` (method) `cli/commands/encoding.py:420` `def do_encodewinbase64(self, line)` -- Encodes a given payload into a Base64 encoded string suitable for Windows PowerShell execution.
- `EncodingCommandSet.do_ip2hex` (method) `cli/commands/encoding.py:479` `def do_ip2hex(self, line)` -- Convert an IPv4 address into its hexadecimal representation.
- `EncodingCommandSet.do_hex_to_plaintext` (method) `cli/commands/encoding.py:505` `def do_hex_to_plaintext(self, line)` -- Converts hexadecimal data from a file to plain text.

## cli/commands/enum.py
Depends on: `cli/commands/_base.py`, `core/validators.py`, `utils.py`
Imported by: `cli/graph_overlay.py`, `cli/palette_command.py`, `cli/scope_guard.py`, `core/errors.py`, `core/payload_schema.py`, `lazyc2/security/command_allowlist.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `modules/bof_registry.py`, `modules/c2_profile_engine.py`, `modules/event_bus.py`, `modules/lazy_rbac.py`, `modules/obs_parser.py`, `modules/operation.py`, `modules/opsec_scorer.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`, `modules/world_model.py`, `skills/claude_md_orchestrator/models.py`, `skills/lazyown_hooks.py`, `skills/lazyown_permissions.py`, `skills/lazyown_policy.py`
- `EnumCommandSet.do_smbclient` (method) `cli/commands/enum.py:38` `def do_smbclient(self, line)` -- Interacts with SMB shares using the `smbclient` command to perform the following operations:
- `EnumCommandSet.do_smbclient_impacket` (method) `cli/commands/enum.py:108` `def do_smbclient_impacket(self, line)` -- Interacts with SMB shares using the `smbclient` command to perform the following operations:
- `EnumCommandSet.do_smbclient_py` (method) `cli/commands/enum.py:178` `def do_smbclient_py(self, line)` -- Interacts with SMB shares using the `smbclient.py` command to perform the following operations:
- `EnumCommandSet.do_smbmap` (method) `cli/commands/enum.py:225` `def do_smbmap(self, line)` -- smbmap -H 10.10.10.3 [OPTIONS] Uses the `smbmap` tool to interact with SMB shares on a remote host:
- `EnumCommandSet.do_getnpusers` (method) `cli/commands/enum.py:345` `def do_getnpusers(self, line)` -- sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt Executes the `impacket-GetNPUsers` command...
- `EnumCommandSet.do_psexec` (method) `cli/commands/enum.py:390` `def do_psexec(self, line)` -- Executes the Impacket PSExec tool to attempt remote execution on the specified target.
- `EnumCommandSet.do_psexec_py` (method) `cli/commands/enum.py:446` `def do_psexec_py(self, line)` -- Executes the Impacket PSExec tool to attempt remote execution on the specified target.
- `EnumCommandSet.do_rpcdump` (method) `cli/commands/enum.py:502` `def do_rpcdump(self, line)` -- Executes the `rpcdump.py` script to dump RPC services from a target host.
- `EnumCommandSet.do_enum4linux` (method) `cli/commands/enum.py:528` `def do_enum4linux(self, line)` -- Performs enumeration of information from a target Linux/Unix system using `enum4linux`.
- `EnumCommandSet.do_rpcclient` (method) `cli/commands/enum.py:558` `def do_rpcclient(self, line)` -- Executes the `rpcclient` command to interact with a remote Windows system over RPC (Remote Procedure Call) using...

## cli/commands/estorides.py
Depends on: `cli/commands/_base.py`, `modules/estorides_importer.py`, `utils.py`
- `EstoridesCommandSet.do_estorides_seed` (method) `cli/commands/estorides.py:72` `def do_estorides_seed(self, line)` -- Feed LazyOwn hosts/domains into Estorides for passive OSINT discovery.
- `EstoridesCommandSet.do_estorides_import` (method) `cli/commands/estorides.py:188` `def do_estorides_import(self, line)` -- Import Estorides-discovered entities into LazyOwn database and scope.
- `EstoridesCommandSet.do_estorides_loop` (method) `cli/commands/estorides.py:319` `def do_estorides_loop(self, line)` -- Run the bidirectional Estorides <-> LazyOwn feedback loop.
- `EstoridesCommandSet.do_estorides_surface` (method) `cli/commands/estorides.py:423` `def do_estorides_surface(self, line)` -- Show the combined active + passive attack surface.

## cli/commands/evasive_payload.py
Depends on: `cli/commands/_base.py`, `modules/evasion_engine.py`, `modules/evasive_payloads.py`, `utils.py`
- `EvasivePayloadCommandSet.do_evasive_payload` (method) `cli/commands/evasive_payload.py:255` `def do_evasive_payload(self, line)` -- Generate an evasive payload with automatic AV/EDR bypass.
- `EvasivePayloadCommandSet.do_mutate_shellcode` (method) `cli/commands/evasive_payload.py:307` `def do_mutate_shellcode(self, line)` -- Apply polymorphic mutation to shellcode for signature evasion.
- `EvasivePayloadCommandSet.do_detect_edr` (method) `cli/commands/evasive_payload.py:360` `def do_detect_edr(self, line)` -- Generate commands to detect EDR/AV on the target.
- `EvasivePayloadCommandSet.do_evasive` (method) `cli/commands/evasive_payload.py:415` `def do_evasive(self, line)` -- Generate detection-evading payloads with multiple obfuscation strategies.
- `EvasivePayloadCommandSet.do_evasion` (method) `cli/commands/evasive_payload.py:533` `def do_evasion(self, line)` -- Generate and manage C2 evasion profiles.

## cli/commands/exfiltration.py
Depends on: `cli/commands/_base.py`, `cli/commands/cloud.py`, `core/crypto.py`, `core/hardening.py`, `utils.py`
- `ExfiltrationCommandSet.do_encrypt` (method) `cli/commands/exfiltration.py:334` `def do_encrypt(self, line)` -- Encrypt a file with XOR using a caller-supplied key.
- `ExfiltrationCommandSet.do_decrypt` (method) `cli/commands/exfiltration.py:361` `def do_decrypt(self, line)` -- Decrypt an XOR-encrypted file using the matching key.
- `ExfiltrationCommandSet.do_evilwinrm` (method) `cli/commands/exfiltration.py:389` `def do_evilwinrm(self, line)` -- Drive Evil-WinRM through password, hash or kerberos-only auth.
- `ExfiltrationCommandSet.do_secretsdump` (method) `cli/commands/exfiltration.py:460` `def do_secretsdump(self, line)` -- Run impacket-secretsdump for SAM, credentials, or NTDS payloads.
- `ExfiltrationCommandSet.do_getuserspns` (method) `cli/commands/exfiltration.py:534` `def do_getuserspns(self, line)` -- Run impacket-GetUserSPNs to request roastable service tickets.
- `ExfiltrationCommandSet.do_gitdumper` (method) `cli/commands/exfiltration.py:568` `def do_gitdumper(self, line)` -- Install ``git-dumper`` if missing and pull a remote ``.git`` tree.
- `ExfiltrationCommandSet.do_evidence` (method) `cli/commands/exfiltration.py:593` `def do_evidence(self, line)` -- Encode the ``sessions/`` tree into a video file or decode one back.
- `ExfiltrationCommandSet.do_getadusers` (method) `cli/commands/exfiltration.py:673` `def do_getadusers(self, line)` -- Run impacket-GetADUsers to enumerate AD accounts on the DC.
- `ExfiltrationCommandSet.do_adgetpass` (method) `cli/commands/exfiltration.py:734` `def do_adgetpass(self, line)` -- Generate a PowerShell script to extract Azure AD Connect credentials.
- `ExfiltrationCommandSet.do_samdump2` (method) `cli/commands/exfiltration.py:799` `def do_samdump2(self, line)` -- Run samdump2 against ``sessions/SYSTEM`` and ``sessions/SAM``.
- `ExfiltrationCommandSet.do_reg_py` (method) `cli/commands/exfiltration.py:824` `def do_reg_py(self, line)` -- Query a remote registry hive with impacket-reg.py over hash auth.
- `ExfiltrationCommandSet.do_unzip` (method) `cli/commands/exfiltration.py:851` `def do_unzip(self, line)` -- Extract a zip archive located under ``sessions/``.
- `ExfiltrationCommandSet.do_getnthash_py` (method) `cli/commands/exfiltration.py:873` `def do_getnthash_py(self, line)` -- Recover the NT hash from a Kerberos U2U TGS via PKINITtools.
- `ExfiltrationCommandSet.do_upload_gofile` (method) `cli/commands/exfiltration.py:905` `def do_upload_gofile(self, line)` -- Upload a file from ``sessions/`` to Gofile via its HTTP API.
- `ExfiltrationCommandSet.do_rsync` (method) `cli/commands/exfiltration.py:967` `def do_rsync(self, line)` -- Push the ``sessions/`` tree to ``rhost`` over SCP with sshpass.
- `ExfiltrationCommandSet.do_gmsadumper` (method) `cli/commands/exfiltration.py:1004` `def do_gmsadumper(self, line)` -- Run gMSADumper to read gMSA password blobs visible to the user.
- `ExfiltrationCommandSet.do_dploot` (method) `cli/commands/exfiltration.py:1043` `def do_dploot(self, line)` -- Run dploot to loot DPAPI-protected secrets.
- `ExfiltrationCommandSet.download_file_from_c2` (method) `cli/commands/exfiltration.py:1125` `def download_file_from_c2(self, file_name, clientid)` -- Download a file from the C2 implant upload queue.
- `ExfiltrationCommandSet.do_download_c2` (method) `cli/commands/exfiltration.py:1164` `def do_download_c2(self, line)` -- Download a file from the C2 implant via the upload command.
- `ExfiltrationCommandSet.do_exfil_s3` (method) `cli/commands/exfiltration.py:1181` `def do_exfil_s3(self, line)` -- Upload a file to an AWS S3 bucket.
- `ExfiltrationCommandSet.do_exfil_telegram` (method) `cli/commands/exfiltration.py:1226` `def do_exfil_telegram(self, line)` -- Exfiltrate a file via Telegram Bot API.
- `ExfiltrationCommandSet.do_exfil_discord` (method) `cli/commands/exfiltration.py:1271` `def do_exfil_discord(self, line)` -- Exfiltrate a file via Discord webhook.
- `ExfiltrationCommandSet.do_exfil_gcs` (method) `cli/commands/exfiltration.py:1314` `def do_exfil_gcs(self, line)` -- Upload a file to Google Cloud Storage.
- `ExfiltrationCommandSet.do_exfil_dns` (method) `cli/commands/exfiltration.py:1356` `def do_exfil_dns(self, line)` -- Exfiltrate data via DNS tunneling.
- `ExfiltrationCommandSet.do_exfil_http` (method) `cli/commands/exfiltration.py:1415` `def do_exfil_http(self, line)` -- Exfiltrate a file via HTTP POST to a controlled server.
- `ExfiltrationCommandSet.do_exfil_auto` (method) `cli/commands/exfiltration.py:1485` `def do_exfil_auto(self, line)` -- Auto-detect flags and sensitive files, then exfiltrate.
- `ExfiltrationCommandSet.do_stage` (method) `cli/commands/exfiltration.py:1543` `def do_stage(self, line)` -- Stage data for exfiltration: compress, encrypt, and split.

## cli/commands/exploit.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `ExploitCommandSet.do_sqlmap` (method) `cli/commands/exploit.py:39` `def do_sqlmap(self, line)` -- Runs SQLMap against the target URL for SQL injection testing.
- `ExploitCommandSet.do_lazypwn` (method) `cli/commands/exploit.py:64` `def do_lazypwn(self, line)` -- Executes the LazyPwn automated exploitation script.
- `ExploitCommandSet.do_rev` (method) `cli/commands/exploit.py:69` `def do_rev(self, line)` -- Copies a reverse shell one-liner to the clipboard.
- `ExploitCommandSet.do_commix` (method) `cli/commands/exploit.py:86` `def do_commix(self, line)` -- Runs commix for command injection testing.
- `ExploitCommandSet.do_download_exploit` (method) `cli/commands/exploit.py:105` `def do_download_exploit(self, line)` -- Downloads and sets up an exploit, optionally serving via HTTP.
- `ExploitCommandSet.do_img2cookie` (method) `cli/commands/exploit.py:126` `def do_img2cookie(self, line)` -- Generates an XSS payload that steals cookies via an image tag.
- `ExploitCommandSet.do_wrapper` (method) `cli/commands/exploit.py:150` `def do_wrapper(self, line)` -- Copies LFI php-wrapper payloads to the clipboard.
- `ExploitCommandSet.do_kusa` (method) `cli/commands/exploit.py:168` `def do_kusa(self, line)` -- Runs the Kusanagi payload generator.
- `ExploitCommandSet.do_ticketer` (method) `cli/commands/exploit.py:178` `def do_ticketer(self, line)` -- Runs Impacket ticketer for golden/silver ticket creation.
- `ExploitCommandSet.do_www` (method) `cli/commands/exploit.py:192` `def do_www(self, line)` -- Starts a simple HTTP server on the configured port to serve payloads.

## cli/commands/exploit_migrated.py
Depends on: `cli/commands/_base.py`, `modules/adcs_attacks.py`, `modules/exploit_chain.py`, `modules/exploit_recommender.py`, `modules/world_model.py`, `utils.py`
- `ExploitMigratedCommandSet.do_cp` (method) `cli/commands/exploit_migrated.py:41` `def do_cp(self, line)` -- Copies a file from the ExploitDB directory to the sessions directory.
- `ExploitMigratedCommandSet.do_createcookie` (method) `cli/commands/exploit_migrated.py:82` `def do_createcookie(self, line)` -- Creates a `cookie.txt` file in the `sessions` directory with the specified cookie value.
- `ExploitMigratedCommandSet.do_py3ttyup` (method) `cli/commands/exploit_migrated.py:128` `def do_py3ttyup(self, line)` -- Copies a Python reverse shell command to the clipboard.
- `ExploitMigratedCommandSet.do_pyautomate` (method) `cli/commands/exploit_migrated.py:166` `def do_pyautomate(self, line)` -- Automates the execution of pwntomate tools on XML configuration files.
- `ExploitMigratedCommandSet.do_winbase64payload` (method) `cli/commands/exploit_migrated.py:207` `def do_winbase64payload(self, line)` -- Creates a base64 encoded payload specifically for Windows to execute a PowerShell command or download a file using...
- `ExploitMigratedCommandSet.do_createdll` (method) `cli/commands/exploit_migrated.py:336` `def do_createdll(self, line)` -- Create a Windows DLL file using MinGW-w64 or a Blazor DLL for Linux.
- `ExploitMigratedCommandSet.do_seo` (method) `cli/commands/exploit_migrated.py:392` `def do_seo(self, line)` -- Performs a web seo fingerprinting scan using `lazyseo.py`.
- `ExploitMigratedCommandSet.do_padbuster` (method) `cli/commands/exploit_migrated.py:427` `def do_padbuster(self, line)` -- Execute the PadBuster command for padding oracle attacks.
- `ExploitMigratedCommandSet.do_cacti_exploit` (method) `cli/commands/exploit_migrated.py:471` `def do_cacti_exploit(self, line)` -- Automates the exploitation of the Cacti version 1.2.26 vulnerability using the multi/http/cacti_package_import_rce...
- `ExploitMigratedCommandSet.setup_handler` (method) `cli/commands/exploit_migrated.py:501` `def setup_handler(config_file, lhost, lport)` -- Sets up a Metasploit multi/handler exploit configuration in the provided config file.
- `ExploitMigratedCommandSet.cacti_exploit` (method) `cli/commands/exploit_migrated.py:524` `def cacti_exploit(config_file, host)` -- Configures an exploit for the Cacti Package Import Remote Code Execution vulnerability in the provided config file.
- `ExploitMigratedCommandSet.do_shellshock` (method) `cli/commands/exploit_migrated.py:556` `def do_shellshock(self, line)` -- Executes a Shellshock attack against a target.
- `ExploitMigratedCommandSet.do_powerserver` (method) `cli/commands/exploit_migrated.py:619` `def do_powerserver(self, line)` -- This function generates a PowerShell script that retrieves reverse shell over http on a Windows system.
- `ExploitMigratedCommandSet.do_sqli` (method) `cli/commands/exploit_migrated.py:682` `def do_sqli(self, line)` -- Asks the user for the URL, database, table, and columns, and then executes the Python script 'modules/lazybsqli.py'...
- `ExploitMigratedCommandSet.do_sharpshooter` (method) `cli/commands/exploit_migrated.py:719` `def do_sharpshooter(self, line)` -- Executes a payload creation framework for the retrieval and execution of arbitrary CSharp source code.
- `ExploitMigratedCommandSet.do_shellfire` (method) `cli/commands/exploit_migrated.py:761` `def do_shellfire(self, line)` -- Runs Shellfire with various options and allows generating payloads.
- `ExploitMigratedCommandSet.do_downloader` (method) `cli/commands/exploit_migrated.py:865` `def do_downloader(self, line)` -- Generate a downloader command for files in the sessions directory.
- `ExploitMigratedCommandSet.do_eternal` (method) `cli/commands/exploit_migrated.py:952` `def do_eternal(self, line)` -- Automates the EternalBlue (MS17-010) exploitation process using Metasploit.
- `ExploitMigratedCommandSet.do_rejetto_hfs_exec` (method) `cli/commands/exploit_migrated.py:997` `def do_rejetto_hfs_exec(self, line)` -- HttpFileServer version 2.3.
- `ExploitMigratedCommandSet.do_ms08_067_netapi` (method) `cli/commands/exploit_migrated.py:1032` `def do_ms08_067_netapi(self, line)` -- SMB CVE-2008-4250.
- `ExploitMigratedCommandSet.do_xss` (method) `cli/commands/exploit_migrated.py:1067` `def do_xss(self, line)` -- Executes the XSS (Cross-Site Scripting) vulnerability testing procedure using user-defined parameters and...
- `ExploitMigratedCommandSet.do_template_helper_serializer` (method) `cli/commands/exploit_migrated.py:1109` `def do_template_helper_serializer(self, line)` -- Handles the creation and serialization of a template helper.
- `ExploitMigratedCommandSet.do_xsstrike` (method) `cli/commands/exploit_migrated.py:1154` `def do_xsstrike(self, line)` -- Command xsstrike: Installs and runs XSStrike for finding XSS vulnerabilities.
- `ExploitMigratedCommandSet.do_sireprat` (method) `cli/commands/exploit_migrated.py:1224` `def do_sireprat(self, line)` -- Command sireprat: Automates the setup and usage of SirepRAT to perform various attacks on a Windows IoT Core device.
- `ExploitMigratedCommandSet.do_upload_bypass` (method) `cli/commands/exploit_migrated.py:1336` `def do_upload_bypass(self, line)` -- Command upload_bypass: Automates the installation and execution of Upload_Bypass for performing file upload bypass...
- `ExploitMigratedCommandSet.do_pywhisker` (method) `cli/commands/exploit_migrated.py:1397` `def do_pywhisker(self, line)` -- Executes the pyWhisker tool for manipulating the msDS-KeyCredentialLink attribute of a target user or computer.
- `ExploitMigratedCommandSet.do_owneredit` (method) `cli/commands/exploit_migrated.py:1447` `def do_owneredit(self, line)` -- Executes the Impacket owneredit tool for manipulating ownership of Active Directory objects.
- `ExploitMigratedCommandSet.do_gettgtpkinit_py` (method) `cli/commands/exploit_migrated.py:1493` `def do_gettgtpkinit_py(self, line)` -- Executes the gettgtpkinit.py tool from PKINITtools to request a TGT using Kerberos PKINIT with a PFX or PEM certificate.
- `ExploitMigratedCommandSet.do_gets4uticket_py` (method) `cli/commands/exploit_migrated.py:1544` `def do_gets4uticket_py(self, line)` -- Executes the gets4uticket.py tool from PKINITtools to request an S4U2Self service ticket using Kerberos.
- `ExploitMigratedCommandSet.do_aclpwn_py` (method) `cli/commands/exploit_migrated.py:1591` `def do_aclpwn_py(self, line)` -- Executes the aclpwn.py tool to find and exploit ACL paths for privilege escalation in an Active Directory environment.
- `ExploitMigratedCommandSet.do_addspn_py` (method) `cli/commands/exploit_migrated.py:1641` `def do_addspn_py(self, line)` -- Executes the addspn.py tool to manage Service Principal Names (SPNs) on Active Directory accounts via LDAP.
- `ExploitMigratedCommandSet.do_printerbug_py` (method) `cli/commands/exploit_migrated.py:1685` `def do_printerbug_py(self, line)` -- Executes the printerbug.py tool to trigger the SpoolService bug via RPC backconnect.
- `ExploitMigratedCommandSet.do_krbrelayx_py` (method) `cli/commands/exploit_migrated.py:1732` `def do_krbrelayx_py(self, line)` -- Executes the krbrelayx.py tool for Kerberos relaying or unconstrained delegation abuse.
- `ExploitMigratedCommandSet.do_autoblody` (method) `cli/commands/exploit_migrated.py:1776` `def do_autoblody(self, line)` -- Executes the autobloody tool for automating Active Directory privilege escalation paths.
- `ExploitMigratedCommandSet.do_unicode_WAFbypass` (method) `cli/commands/exploit_migrated.py:1828` `def do_unicode_WAFbypass(self, line)` -- We open a Netcat listener on port 443 and attempt to exploit NodeJS deserialization by sending the following...
- `ExploitMigratedCommandSet.do_sqli_mssql_test` (method) `cli/commands/exploit_migrated.py:1882` `def do_sqli_mssql_test(self, line)` -- Initiates a reverse MSSQL shell by starting an HTTP server to handle incoming connections and exfiltrate data.
- `ExploitMigratedCommandSet.do_pyoracle2` (method) `cli/commands/exploit_migrated.py:1918` `def do_pyoracle2(self, line)` -- Executes the pyOracle2 tool for performing padding oracle attacks.
- `ExploitMigratedCommandSet.do_lfi` (method) `cli/commands/exploit_migrated.py:2000` `def do_lfi(self, line)` -- Exploits a potential Local File Inclusion (LFI) vulnerability by crafting and sending HTTP GET requests to a...
- `ExploitMigratedCommandSet.do_greatSCT` (method) `cli/commands/exploit_migrated.py:2042` `def do_greatSCT(self, line)` -- Executes the GreatSCT tool for generating payloads that bypass antivirus and application whitelisting solutions.
- `ExploitMigratedCommandSet.do_sqsh` (method) `cli/commands/exploit_migrated.py:2087` `def do_sqsh(self, line)` -- Executes the Impacket sqsh tool for manipulating ownership of Active Directory objects.
- `ExploitMigratedCommandSet.do_jwt_tool` (method) `cli/commands/exploit_migrated.py:2132` `def do_jwt_tool(self, line)` -- Uses the jwt_tool to analyze, tamper, or exploit JSON Web Tokens (JWTs).
- `ExploitMigratedCommandSet.do_filtering` (method) `cli/commands/exploit_migrated.py:2174` `def do_filtering(self, line)` -- Applies various filtering techniques to the given command line by modifying each character or word appropriately.
- `ExploitMigratedCommandSet.do_lol` (method) `cli/commands/exploit_migrated.py:2200` `def do_lol(self, line)` -- Exploits a target by injecting a malicious payload and collecting admin information.
- `ExploitMigratedCommandSet.do_utf` (method) `cli/commands/exploit_migrated.py:2287` `def do_utf(self, line)` -- Encode a given payload into UTF-16 escape sequences.
- `ExploitMigratedCommandSet.do_digdug` (method) `cli/commands/exploit_migrated.py:2326` `def do_digdug(self, line)` -- Executes Dig Dug to inflate the size of an executable file, leveraging pre-configured settings and interactive input...
- `ExploitMigratedCommandSet.do_sshexploit` (method) `cli/commands/exploit_migrated.py:2384` `def do_sshexploit(self, line)` -- Exploits OpenSSH vulnerability CVE-2023-38408 via the PKCS#11 feature of the ssh-agent.
- `ExploitMigratedCommandSet.do_excelntdonut` (method) `cli/commands/exploit_migrated.py:2454` `def do_excelntdonut(self, line)` -- Generates an Excel 4.0 (XLM) macro from a provided C# source file using EXCELntDonut.
- `ExploitMigratedCommandSet.do_ntpdate` (method) `cli/commands/exploit_migrated.py:2510` `def do_ntpdate(self, line)` -- Synchronizes the system clock with a specified NTP server.
- `ExploitMigratedCommandSet.do_adcs_check` (method) `cli/commands/exploit_migrated.py:2534` `def do_adcs_check(self, line)` -- Check Active Directory Certificate Services for ESC1-ESC8 vulnerabilities.
- `ExploitMigratedCommandSet.do_chain` (method) `cli/commands/exploit_migrated.py:2590` `def do_chain(self, line)` -- Run autonomous exploitation chain: recon -> vuln -> exploit -> post-exploit.
- `ExploitMigratedCommandSet.do_exploit_recommend` (method) `cli/commands/exploit_migrated.py:2685` `def do_exploit_recommend(self, line)` -- AI-powered exploit recommendation — matches discovered services to CVEs.

## cli/commands/exploitgym.py
Depends on: `cli/commands/_base.py`, `modules/exploitgym_gym.py`, `utils.py`
Imported by: `tests/test_exploitgym_gym.py`
- `ExploitGymCommandSet.do_exploitgym` (method) `cli/commands/exploitgym.py:43` `def do_exploitgym(self, line)` -- ExploitGym — real-world exploit benchmark via containerised tasks.

## cli/commands/help_ui.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/command_explorer.py`, `cli/commands/_base.py`, `cli/config_status.py`, `cli/contextual_help.py`, `cli/doctor.py`, `cli/engagement_hooks.py`, `cli/ops_commands.py`, `cli/tui_theme.py`, `cli/tutorial.py`, `cli/wizard.py`, `cli/wizard_scope.py`, `core/config.py`, `core/console.py`, `modules/world_model.py`, `utils.py`
Imported by: `tests/test_help_ui_command_set.py`
- `HelpUiCommandSet.do_wizard` (method) `cli/commands/help_ui.py:36` `def do_wizard(self, line)` -- Guided first-run setup wizard — configure rhost, lhost, domain, wordlists and more.
- `HelpUiCommandSet.do_tutorial` (method) `cli/commands/help_ui.py:137` `def do_tutorial(self, line)` -- Interactive tutorial that walks you through the golden path.
- `HelpUiCommandSet.do_help_phase` (method) `cli/commands/help_ui.py:160` `def do_help_phase(self, line)` -- List all commands for a given kill-chain phase.
- `HelpUiCommandSet.do_help_status` (method) `cli/commands/help_ui.py:191` `def do_help_status(self, line)` -- Show which session requirements are met (rhost, creds, domain, OS).
- `HelpUiCommandSet.do_ctx_help` (method) `cli/commands/help_ui.py:203` `def do_ctx_help(self, line)` -- Show contextual help for a command: description, phase, requirements, tips.
- `HelpUiCommandSet.do_ctx` (method) `cli/commands/help_ui.py:223` `def do_ctx(self, line)` -- Print a single-line operator context: rhost, lhost, domain, phase, os, creds.
- `HelpUiCommandSet.do_command_explorer` (method) `cli/commands/help_ui.py:235` `def do_command_explorer(self, line)` -- Interactive command explorer organized by goals and phases.
- `HelpUiCommandSet.do_config_status` (method) `cli/commands/help_ui.py:267` `def do_config_status(self, line)` -- Show configuration status grouped by category with set/missing indicators.
- `HelpUiCommandSet.do_tui_theme` (method) `cli/commands/help_ui.py:287` `def do_tui_theme(self, line)` -- Switch the TUI colour theme used by the splash and styled output.
- `HelpUiCommandSet.do_doctor` (method) `cli/commands/help_ui.py:312` `def do_doctor(self, line)` -- Preflight environment health check — verify the install is ready.
- `HelpUiCommandSet.do_karma` (method) `cli/commands/help_ui.py:347` `def do_karma(self, line)` -- Show ELO score, karma rank and exploration progress for this operator.
- `HelpUiCommandSet.do_tgrep` (method) `cli/commands/help_ui.py:381` `def do_tgrep(self, line)` -- Search across all previous command outputs and session logs.
- `HelpUiCommandSet.do_phase` (method) `cli/commands/help_ui.py:398` `def do_phase(self, line)` -- Get or set the current kill-chain phase.
- `HelpUiCommandSet.do_killchain` (method) `cli/commands/help_ui.py:432` `def do_killchain(self, line)` -- Show the unified kill-chain progress and control auto-refresh.

## cli/commands/infra.py
Depends on: `cli/commands/_base.py`, `cli/confirm.py`, `utils.py`
Imported by: `tests/test_bdd_infra_range_report.py`, `tests/test_infra_disposable.py`
- `InfraCommandSet.do_infra` (method) `cli/commands/infra.py:136` `def do_infra(self, line)` -- Manage disposable C2 infrastructure.

## cli/commands/lab.py
Depends on: `cli/commands/_base.py`, `utils.py`
Imported by: `tests/test_bdd_infra_range_report.py`, `tests/test_infra_disposable.py`
- `LabCommandSet.do_lab` (method) `cli/commands/lab.py:119` `def do_lab(self, line)` -- Manage local CTF practice labs.

## cli/commands/lateral.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `LateralMovementCommandSet.do_socat` (method) `cli/commands/lateral.py:31` `def do_socat(self, line)` -- Run socat for port forwarding.
- `LateralMovementCommandSet.do_chisel` (method) `cli/commands/lateral.py:43` `def do_chisel(self, line)` -- Run chisel for quick tunneling.
- `LateralMovementCommandSet.do_set_proxychains` (method) `cli/commands/lateral.py:59` `def do_set_proxychains(self, line)` -- Configure proxychains for the current session.
- `LateralMovementCommandSet.do_ngrok` (method) `cli/commands/lateral.py:72` `def do_ngrok(self, line)` -- Start ngrok tunnel.
- `LateralMovementCommandSet.do_ligolo` (method) `cli/commands/lateral.py:79` `def do_ligolo(self, line)` -- Run Ligolo-ng for advanced pivoting.
- `LateralMovementCommandSet.do_nc` (method) `cli/commands/lateral.py:91` `def do_nc(self, line)` -- Netcat listener or connect.
- `LateralMovementCommandSet.do_wmiexec` (method) `cli/commands/lateral.py:106` `def do_wmiexec(self, line)` -- Execute commands via WMI.
- `LateralMovementCommandSet.do_ssh` (method) `cli/commands/lateral.py:114` `def do_ssh(self, line)` -- SSH to a remote host (custom port).

## cli/commands/lateral_migrated.py
Depends on: `cli/commands/_base.py`, `core/hardening.py`, `modules/domain_dominance.py`, `utils.py`
- `LateralMigratedCommandSet.do_vpn` (method) `cli/commands/lateral_migrated.py:29` `def do_vpn(self, line)` -- Connect to a VPN by selecting from available .ovpn files.
- `LateralMigratedCommandSet.do_id_rsa` (method) `cli/commands/lateral_migrated.py:101` `def do_id_rsa(self, line)` -- Create an SSH private key file and connect to a remote host using SSH.
- `LateralMigratedCommandSet.do_sshd` (method) `cli/commands/lateral_migrated.py:172` `def do_sshd(self, line)` -- Starts the SSH service and displays its status.
- `LateralMigratedCommandSet.do_wifipass` (method) `cli/commands/lateral_migrated.py:199` `def do_wifipass(self, line)` -- This function generates a PowerShell script that retrieves saved Wi-Fi passwords on a Windows system.
- `LateralMigratedCommandSet.do_bloodyAD` (method) `cli/commands/lateral_migrated.py:229` `def do_bloodyAD(self, line)` -- Execute the bloodyAD.py command for a specific user or all users listed in the users.txt file.
- `LateralMigratedCommandSet.do_getTGT` (method) `cli/commands/lateral_migrated.py:321` `def do_getTGT(self, line)` -- Requests a Ticket Granting Ticket (TGT) using the Impacket tool with provided credentials.
- `LateralMigratedCommandSet.do_tord` (method) `cli/commands/lateral_migrated.py:369` `def do_tord(self, line)` -- Execute the tor.sh script with the specified port or default to port 80 if no port is provided.
- `LateralMigratedCommandSet.do_shadowsocks` (method) `cli/commands/lateral_migrated.py:404` `def do_shadowsocks(self, line)` -- Execute the Shadowsocks tool to create a secure tunnel for network traffic.
- `LateralMigratedCommandSet.do_rnc` (method) `cli/commands/lateral_migrated.py:477` `def do_rnc(self, line)` -- Runs `nc` with rlwrap  the specified port for listening.
- `LateralMigratedCommandSet.do_gospherus` (method) `cli/commands/lateral_migrated.py:543` `def do_gospherus(self, line)` -- Command gospherus: Clones and uses the Gopherus tool to generate gopher payloads for various services.
- `LateralMigratedCommandSet.do_mssqlcli` (method) `cli/commands/lateral_migrated.py:613` `def do_mssqlcli(self, line)` -- Attempts to connect to an MSSQL server using the mssqlclient.py tool with Windows authentication.
- `LateralMigratedCommandSet.do_penelope` (method) `cli/commands/lateral_migrated.py:666` `def do_penelope(self, line)` -- Command penelope: Installs and runs Penelope for handling reverse and bind shells.
- `LateralMigratedCommandSet.do_stormbreaker` (method) `cli/commands/lateral_migrated.py:777` `def do_stormbreaker(self, line)` -- Command stormbreaker: Automates the installation and usage of Storm-Breaker for performing various network attacks.
- `LateralMigratedCommandSet.do_regeorg` (method) `cli/commands/lateral_migrated.py:823` `def do_regeorg(self, line)` -- Executes the reGeorg tool for HTTP(s) tunneling through a SOCKS proxy.
- `LateralMigratedCommandSet.do_targetedKerberoas` (method) `cli/commands/lateral_migrated.py:871` `def do_targetedKerberoas(self, line)` -- Executes the targetedKerberoast tool for extracting Kerberos service tickets.
- `LateralMigratedCommandSet.do_dcomexec` (method) `cli/commands/lateral_migrated.py:931` `def do_dcomexec(self, line)` -- Executes the Impacket dcomexec tool to run commands on a remote system using DCOM.
- `LateralMigratedCommandSet.do_upload_c2` (method) `cli/commands/lateral_migrated.py:1002` `def do_upload_c2(self, line)` -- upload command in the client using the C2 to upload a file
- `LateralMigratedCommandSet.do_wmiexecpro` (method) `cli/commands/lateral_migrated.py:1031` `def do_wmiexecpro(self, line)` -- Executes wmiexec-pro with various options for WMI operations.
- `LateralMigratedCommandSet.install_wmiexecpro` (method) `cli/commands/lateral_migrated.py:1070` `def install_wmiexecpro()`
- `LateralMigratedCommandSet.do_lateral_mov_lin` (method) `cli/commands/lateral_migrated.py:1247` `def do_lateral_mov_lin(self, line)` -- Perform lateral movement by downloading and installing LazyOwn on a remote Linux machine.
- `LateralMigratedCommandSet.do_addcli` (method) `cli/commands/lateral_migrated.py:1302` `def do_addcli(self, line)` -- Add a client to execute c2 commands
- `LateralMigratedCommandSet.do_dominion` (method) `cli/commands/lateral_migrated.py:1317` `def do_dominion(self, line)` -- Execute a fully automated Active Directory domain takeover.

## cli/commands/marketplace.py
Depends on: `cli/commands/_base.py`, `cli/marketplace_config.py`, `cli/plugin_tiers.py`, `modules/module_registry.py`, `utils.py`
- `MarketplaceCommandSet.do_marketplace` (method) `cli/commands/marketplace.py:104` `def do_marketplace(self, line)` -- Discover and install community plugins, addons, and tools.
- `MarketplaceCommandSet.do_marketplace_config` (method) `cli/commands/marketplace.py:426` `def do_marketplace_config(self, line)` -- Interactive marketplace manager (curses TUI).

## cli/commands/mcp_bridge.py
Depends on: `cli/aliases.py`, `cli/commands/_base.py`, `core/config.py`, `modules/intelligence_engine.py`, `modules/playbook_engine.py`, `modules/session_rag.py`, `modules/threat_model.py`, `modules/world_model.py`, `skills/lazyown_facts.py`, `skills/lazyown_parquet_db.py`, `utils.py`
- `McpBridgeCommandSet.do_auto_populate` (method) `cli/commands/mcp_bridge.py:146` `def do_auto_populate(self, args)` -- Parse the latest nmap XML scan and auto-populate payload context.
- `McpBridgeCommandSet.do_facts_show` (method) `cli/commands/mcp_bridge.py:253` `def do_facts_show(self, args)` -- Show structured facts extracted from nmap scans and tool output.
- `McpBridgeCommandSet.do_rag_query` (method) `cli/commands/mcp_bridge.py:278` `def do_rag_query(self, args)` -- Semantic search over session artefacts (scans, logs, notes).
- `McpBridgeCommandSet.do_parquet_query` (method) `cli/commands/mcp_bridge.py:308` `def do_parquet_query(self, args)` -- Query the parquet knowledge bases (GTFOBins, LOLBas, ATT&CK, sessions).
- `McpBridgeCommandSet.do_threat_model` (method) `cli/commands/mcp_bridge.py:370` `def do_threat_model(self, args)` -- Build or inspect the threat model derived from session events.
- `McpBridgeCommandSet.do_playbook_run` (method) `cli/commands/mcp_bridge.py:423` `def do_playbook_run(self, args)` -- Execute a generated YAML playbook step by step through the shell.
- `McpBridgeCommandSet.do_auto_loop` (method) `cli/commands/mcp_bridge.py:481` `def do_auto_loop(self, line)` -- Run a goal through the autonomous daemon orchestrator backend.
- `McpBridgeCommandSet.do_session_state` (method) `cli/commands/mcp_bridge.py:499` `def do_session_state(self, line)` -- Alias of ``sitrep`` kept for MCP verb parity (lazyown_session_state).
- `McpBridgeCommandSet.do_campaign_sitrep` (method) `cli/commands/mcp_bridge.py:504` `def do_campaign_sitrep(self, line)` -- Alias of ``sitrep`` kept for MCP verb parity (lazyown_campaign_sitrep).
- `McpBridgeCommandSet.do_timeline` (method) `cli/commands/mcp_bridge.py:509` `def do_timeline(self, line)` -- Alias of ``timeline_browser`` kept for MCP verb parity (lazyown_timeline).

## cli/commands/misc_migrated.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/autosuggest.py`, `cli/banner_config.py`, `cli/command_chain.py`, `cli/commands/_base.py`, `cli/dashboard_tui.py`, `cli/exploration.py`, `cli/exploration_view.py`, `cli/graph_advisor.py`, `cli/graph_overlay.py`, `cli/ops_commands.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/palette_overlay.py`, `cli/reactive_hints.py`, `cli/recommendation.py`, `cli/recommendation_signals.py`, `cli/sessions_browser.py`, `cli/show.py`, `cli/timeline_browser.py`, `cli/toast_bus.py`, `cli/wizard.py`, `core/config.py`, `core/console.py`, `core/process.py`, `core/safe_exec.py`, `modules/module_registry.py`, `modules/payload_factory.py`, `utils.py`
Imported by: `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_nethelpers_command_set.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`
- `MiscMigratedCommandSet.do_notify` (method) `cli/commands/misc_migrated.py:91` `def do_notify(self, arg)` -- Command to trigger a toastr-like notification.
- `MiscMigratedCommandSet.do_EOF` (method) `cli/commands/misc_migrated.py:110` `def do_EOF(self, line)` -- Handle the end-of-file (EOF) condition.
- `MiscMigratedCommandSet.do_palette` (method) `cli/commands/misc_migrated.py:190` `def do_palette(self, line)` -- Browse the operator command catalogue grouped by kill-chain phase.
- `MiscMigratedCommandSet.do_graph_search` (method) `cli/commands/misc_migrated.py:215` `def do_graph_search(self, line)` -- Fuzzy search the graphify knowledge graph for nodes by label.
- `MiscMigratedCommandSet.do_neighbors` (method) `cli/commands/misc_migrated.py:243` `def do_neighbors(self, line)` -- Show graph neighbors of a node or command from the graphify graph.
- `MiscMigratedCommandSet.do_god_nodes` (method) `cli/commands/misc_migrated.py:270` `def do_god_nodes(self, line)` -- Show the most-connected nodes ("god nodes") from the graph.
- `MiscMigratedCommandSet.do_suggest_next` (method) `cli/commands/misc_migrated.py:289` `def do_suggest_next(self, line)` -- Suggest next commands by walking the graph from recent activity.
- `MiscMigratedCommandSet.do_recommend_next` (method) `cli/commands/misc_migrated.py:415` `def do_recommend_next(self, line)` -- Recommend the next action via the unified recommendation engine.
- `MiscMigratedCommandSet.do_explore` (method) `cli/commands/misc_migrated.py:472` `def do_explore(self, line)` -- Show exploration coverage and addon/tool suggestions per service.
- `MiscMigratedCommandSet.do_prev` (method) `cli/commands/misc_migrated.py:503` `def do_prev(self, line)` -- Show prerequisite commands for a verb (the chain's ``prev`` arrow).
- `MiscMigratedCommandSet.do_dashboard` (method) `cli/commands/misc_migrated.py:538` `def do_dashboard(self, line)` -- Launch the full-screen LazyOwn operator dashboard (Textual TUI).
- `MiscMigratedCommandSet.do_palette_k` (method) `cli/commands/misc_migrated.py:575` `def do_palette_k(self, line)` -- Open the fuzzy Command-K palette overlay.
- `MiscMigratedCommandSet.do_browse` (method) `cli/commands/misc_migrated.py:604` `def do_browse(self, line)` -- Open the sessions/ TUI browser.
- `MiscMigratedCommandSet.do_timeline_browser` (method) `cli/commands/misc_migrated.py:626` `def do_timeline_browser(self, line)` -- Open the timeline scrubber over the session report CSV.
- `MiscMigratedCommandSet.do_graph_overlay` (method) `cli/commands/misc_migrated.py:645` `def do_graph_overlay(self, line)` -- Open the graph overlay over the graphify knowledge graph.
- `MiscMigratedCommandSet.do_toast_clear` (method) `cli/commands/misc_migrated.py:665` `def do_toast_clear(self, line)` -- Mark every pending toast event as seen without printing them.
- `MiscMigratedCommandSet.do_exit` (method) `cli/commands/misc_migrated.py:691` `def do_exit(self, arg)` -- Exit the command line interface.
- `MiscMigratedCommandSet.do_banner` (method) `cli/commands/misc_migrated.py:768` `def do_banner(self, line)` -- Show the banner
- `MiscMigratedCommandSet.do_config_banner` (method) `cli/commands/misc_migrated.py:780` `def do_config_banner(self, line)` -- Open a Powerlevel10k-style wizard to toggle prompt segments.
- `MiscMigratedCommandSet.do_aliass` (method) `cli/commands/misc_migrated.py:839` `def do_aliass(self, line)` -- Prints all configured aliases and their associated commands.
- `MiscMigratedCommandSet.do_graph` (method) `cli/commands/misc_migrated.py:875` `def do_graph(self, line)` -- Generates a graph from JSON payload files containing URL, RHOST, and RPORT.
- `MiscMigratedCommandSet.do_h` (method) `cli/commands/misc_migrated.py:936` `def do_h(self, arg)` -- Open a new window within a tmux session using the LazyOwn RedTeam Framework.
- `MiscMigratedCommandSet.do_v` (method) `cli/commands/misc_migrated.py:982` `def do_v(self, arg)` -- Open a new window within a tmux session using the LazyOwn RedTeam Framework.
- `MiscMigratedCommandSet.do_links` (method) `cli/commands/misc_migrated.py:1032` `def do_links(self, line)` -- Displays a list of useful links and allows the user to select and copy a link to the clipboard.
- `MiscMigratedCommandSet.do_news` (method) `cli/commands/misc_migrated.py:1095` `def do_news(self, line)` -- Show the Hacker News in the terminal.
- `MiscMigratedCommandSet.do_check_update` (method) `cli/commands/misc_migrated.py:1108` `def do_check_update(self, line)` -- Checks for updates by comparing the local version with the remote version.
- `MiscMigratedCommandSet.do_addalias` (method) `cli/commands/misc_migrated.py:1157` `def do_addalias(self, arglist)` -- Add a new alias with support for placeholders like {rhost}, {lhost}, {lport}, etc.
- `MiscMigratedCommandSet.do_listaliases` (method) `cli/commands/misc_migrated.py:1206` `def do_listaliases(self, _)` -- List all available aliases.

## cli/commands/mobile_macos.py
Depends on: `cli/commands/_base.py`, `core/process.py`, `core/validators.py`, `utils.py`
- `MobileMacOSCommandSet.do_android_enum` (method) `cli/commands/mobile_macos.py:103` `def do_android_enum(self, line)` -- Enumerate an Android device connected via ADB.
- `MobileMacOSCommandSet.do_android_apk` (method) `cli/commands/mobile_macos.py:171` `def do_android_apk(self, line)` -- Generate a malicious APK with reverse shell payload.
- `MobileMacOSCommandSet.do_macos_persist` (method) `cli/commands/mobile_macos.py:216` `def do_macos_persist(self, line)` -- Generate macOS persistence via LaunchAgent.
- `MobileMacOSCommandSet.do_macos_keychain` (method) `cli/commands/mobile_macos.py:274` `def do_macos_keychain(self, line)` -- Extract secrets from the macOS Keychain.
- `MobileMacOSCommandSet.do_macos_tcc` (method) `cli/commands/mobile_macos.py:323` `def do_macos_tcc(self, line)` -- Generate macOS TCC (Transparency, Consent, Control) bypass.
- `MobileMacOSCommandSet.is_binary_present` (method) `cli/commands/mobile_macos.py:374` `def is_binary_present(name)` -- Check if a binary is available on PATH, delegates to core.

## cli/commands/module_manager.py
Depends on: `cli/commands/_base.py`, `modules/module_registry.py`, `utils.py`
- `ModuleManagerCommandSet.do_search` (method) `cli/commands/module_manager.py:71` `def do_search(self, line)` -- Search for modules by name, description, or author.
- `ModuleManagerCommandSet.do_use` (method) `cli/commands/module_manager.py:111` `def do_use(self, line)` -- Select a module to work with.
- `ModuleManagerCommandSet.do_back` (method) `cli/commands/module_manager.py:162` `def do_back(self, line)` -- Leave the current module context.

## cli/commands/nethelpers.py
Depends on: `cli/commands/_base.py`, `core/hardening.py`, `utils.py`
Imported by: `tests/test_nethelpers_command_set.py`
- `NetworkHelpersCommandSet.do_ip` (method) `cli/commands/nethelpers.py:38` `def do_ip(self, line)` -- Displays IP addresses of network interfaces and copies the IP address from the `tun0` interface to the clipboard.
- `NetworkHelpersCommandSet.do_ipp` (method) `cli/commands/nethelpers.py:114` `def do_ipp(self, line)` -- Displays IP addresses of network interfaces and prints the IP address from the `tun0` interface.
- `NetworkHelpersCommandSet.do_rhost` (method) `cli/commands/nethelpers.py:190` `def do_rhost(self, line)` -- Copies the remote host (self.params['rhost']) to the clipboard and updates the command prompt.
- `NetworkHelpersCommandSet.do_rrhost` (method) `cli/commands/nethelpers.py:242` `def do_rrhost(self, line)` -- Updates the command prompt to include the remote host (self.params['rhost']) and current working directory.
- `NetworkHelpersCommandSet.do_addhosts` (method) `cli/commands/nethelpers.py:283` `def do_addhosts(self, line)` -- Adds an entry to the `/etc/hosts` file, mapping an IP address to a domain name.
- `NetworkHelpersCommandSet.do_ip2asn` (method) `cli/commands/nethelpers.py:307` `def do_ip2asn(self, line)` -- Command to get ASN for a given IP address.
- `NetworkHelpersCommandSet.do_ignorearp` (method) `cli/commands/nethelpers.py:337` `def do_ignorearp(self, line)` -- Configures the system to ignore ARP requests by setting a kernel parameter.
- `NetworkHelpersCommandSet.do_ignoreicmp` (method) `cli/commands/nethelpers.py:374` `def do_ignoreicmp(self, line)` -- Configures the system to ignore ICMP echo requests by setting a kernel parameter.
- `NetworkHelpersCommandSet.do_acknowledgearp` (method) `cli/commands/nethelpers.py:411` `def do_acknowledgearp(self, line)` -- Configures the system to acknowledge ARP requests by setting a kernel parameter.
- `NetworkHelpersCommandSet.do_acknowledgeicmp` (method) `cli/commands/nethelpers.py:448` `def do_acknowledgeicmp(self, line)` -- Configures the system to respond to ICMP echo requests by setting a kernel parameter.

## cli/commands/opsec_cleanup.py
Depends on: `cli/commands/_base.py`, `modules/forensic_cleaner.py`, `modules/log_tamper.py`, `modules/memory_cleaner.py`, `modules/network_opsec.py`, `modules/opsec_scorer.py`, `modules/timestomper.py`
- `OpsecCleanupCommandSet.do_opsec_score` (method) `cli/commands/opsec_cleanup.py:25` `def do_opsec_score(self, line)` -- Real-time OPSEC risk assessment with contextual action gating (v2).
- `OpsecCleanupCommandSet.do_log_tamper` (method) `cli/commands/opsec_cleanup.py:97` `def do_log_tamper(self, line)` -- Cross-platform log clearing commands.
- `OpsecCleanupCommandSet.do_forensic_clean` (method) `cli/commands/opsec_cleanup.py:162` `def do_forensic_clean(self, line)` -- Clean forensic artifacts — Prefetch, Shimcache, Amcache, Jump Lists, etc.
- `OpsecCleanupCommandSet.do_timestomp` (method) `cli/commands/opsec_cleanup.py:219` `def do_timestomp(self, line)` -- Manipulate file MACB timestamps to evade forensic timeline analysis.
- `OpsecCleanupCommandSet.do_memory_clean` (method) `cli/commands/opsec_cleanup.py:288` `def do_memory_clean(self, line)` -- Clean memory artifacts — Kerberos tickets, clipboard, env vars, credentials.
- `OpsecCleanupCommandSet.do_network_opsec` (method) `cli/commands/opsec_cleanup.py:342` `def do_network_opsec(self, line)` -- Network OPSEC — proxy chains, DoH, canary detection, traffic analysis.
- `OpsecCleanupCommandSet.do_auditd_disable` (method) `cli/commands/opsec_cleanup.py:445` `def do_auditd_disable(self, line)` -- Generate commands to disable Linux auditd.
- `OpsecCleanupCommandSet.do_sysmon_disable` (method) `cli/commands/opsec_cleanup.py:468` `def do_sysmon_disable(self, line)` -- Generate commands to disable Windows Sysmon.

## cli/commands/orchestration.py
Depends on: `cli/commands/_base.py`
Imported by: `tests/test_improvements_spec.py`
- `OrchestrationCommandSet.do_status_bar` (method) `cli/commands/orchestration.py:125` `def do_status_bar(self, args)` -- Inspect, toggle and refresh the prompt status bar.
- `OrchestrationCommandSet.do_orchestrate` (method) `cli/commands/orchestration.py:151` `def do_orchestrate(self, args)` -- Route a goal through the unified orchestrator and print the result.

## cli/commands/payload_arsenal.py
Depends on: `cli/commands/_base.py`, `modules/dotnet_payload.py`, `modules/linux_advanced_payloads.py`, `modules/macos_payloads.py`, `modules/polymorphic_engine.py`, `modules/staged_delivery.py`
- `PayloadArsenalCommandSet.do_dotnet_payload` (method) `cli/commands/payload_arsenal.py:29` `def do_dotnet_payload(self, line)` -- Generate a .NET/C# payload.
- `PayloadArsenalCommandSet.do_arsenal_show` (method) `cli/commands/payload_arsenal.py:114` `def do_arsenal_show(self, line)` -- Show payload arsenal items.
- `PayloadArsenalCommandSet.do_staged_delivery` (method) `cli/commands/payload_arsenal.py:172` `def do_staged_delivery(self, line)` -- Generate staged delivery artifacts (HTA, VBA, LNK, ISO, VHD).
- `PayloadArsenalCommandSet.do_polymorphic` (method) `cli/commands/payload_arsenal.py:261` `def do_polymorphic(self, line)` -- Apply polymorphic mutation to shellcode.
- `PayloadArsenalCommandSet.do_macos_payload` (method) `cli/commands/payload_arsenal.py:328` `def do_macos_payload(self, line)` -- Generate macOS payloads (.app bundles, persistence, TCC bypass).
- `PayloadArsenalCommandSet.do_linux_advanced_payload` (method) `cli/commands/payload_arsenal.py:401` `def do_linux_advanced_payload(self, line)` -- Generate advanced Linux payloads (LD_PRELOAD, eBPF, PAM, kernel module).

## cli/commands/payload_generation.py
Depends on: `cli/commands/_base.py`, `modules/payload_factory.py`, `utils.py`
- `PayloadCommandSet.do_generate` (method) `cli/commands/payload_generation.py:37` `def do_generate(self, line)` -- Generate a payload.

## cli/commands/persist.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `PersistenceCommandSet.do_createwebshell` (method) `cli/commands/persist.py:33` `def do_createwebshell(self, line)` -- Create web shells (JPG-disguised PHP, p0wny-shell, ASP).
- `PersistenceCommandSet.do_createrevshell` (method) `cli/commands/persist.py:47` `def do_createrevshell(self, line)` -- Create a bash reverse shell script in sessions/.
- `PersistenceCommandSet.do_createwinrevshell` (method) `cli/commands/persist.py:61` `def do_createwinrevshell(self, line)` -- Create a Windows reverse shell (PowerShell).
- `PersistenceCommandSet.do_conptyshell` (method) `cli/commands/persist.py:73` `def do_conptyshell(self, line)` -- Download ConPtyShell and prepare a PowerShell run command.
- `PersistenceCommandSet.do_pwncatcs` (method) `cli/commands/persist.py:89` `def do_pwncatcs(self, line)` -- Start a pwncat-cs reverse shell listener.
- `PersistenceCommandSet.do_revwin` (method) `cli/commands/persist.py:99` `def do_revwin(self, line)` -- Create a Windows reverse shell executable.
- `PersistenceCommandSet.do_wmi_persist` (method) `cli/commands/persist.py:112` `def do_wmi_persist(self, line)` -- Create WMI Event Subscription persistence (fileless, no disk write).
- `PersistenceCommandSet.do_wmi_lateral` (method) `cli/commands/persist.py:170` `def do_wmi_lateral(self, line)` -- Execute a command on a remote host via WMI.
- `PersistenceCommandSet.do_wmi_scheduled_task` (method) `cli/commands/persist.py:209` `def do_wmi_scheduled_task(self, line)` -- Create a scheduled task for persistence via WMI.

## cli/commands/persist_migrated.py
Depends on: `cli/commands/_base.py`, `core/hardening.py`, `modules/traffic_morpher.py`, `utils.py`
- `PersistMigratedCommandSet.do_pwncat` (method) `cli/commands/persist_migrated.py:33` `def do_pwncat(self, line)` -- Runs `pwncat` with the specified port for listening.
- `PersistMigratedCommandSet.do_ftp` (method) `cli/commands/persist_migrated.py:77` `def do_ftp(self, line)` -- Connects to an ftp host using credentials from a file and a specified port.
- `PersistMigratedCommandSet.do_rdp` (method) `cli/commands/persist_migrated.py:136` `def do_rdp(self, line)` -- Reads credentials from a file, encrypts the password, and executes the RDP connection command.
- `PersistMigratedCommandSet.do_grisun0` (method) `cli/commands/persist_migrated.py:211` `def do_grisun0(self, line)` -- Creates and copies a shell command to add a new user, assign a password, add the user to the sudo group, and switch...
- `PersistMigratedCommandSet.do_grisun0w` (method) `cli/commands/persist_migrated.py:257` `def do_grisun0w(self, line)` -- Creates and copies a PowerShell command to add a new user, assign a password, add the user to the Administrators...
- `PersistMigratedCommandSet.do_asprevbase64` (method) `cli/commands/persist_migrated.py:301` `def do_asprevbase64(self, line)` -- Creates a base64 encoded ASP reverse shell payload and copies it to the clipboard.
- `PersistMigratedCommandSet.do_weevelygen` (method) `cli/commands/persist_migrated.py:339` `def do_weevelygen(self, line)` -- Generate a PHP backdoor using Weevely, protected with the given password.
- `PersistMigratedCommandSet.do_weevely` (method) `cli/commands/persist_migrated.py:379` `def do_weevely(self, line)` -- Connect to PHP backdoor using Weevely, protected with the given password.
- `PersistMigratedCommandSet.do_backdoor_factory` (method) `cli/commands/persist_migrated.py:425` `def do_backdoor_factory(self, line)` -- Creates a backdoored executable using `backdoor-factory`.
- `PersistMigratedCommandSet.do_msfpc` (method) `cli/commands/persist_migrated.py:471` `def do_msfpc(self, line)` -- Generates payloads using MSFvenom Payload Creator (MSFPC).
- `PersistMigratedCommandSet.do_ivy` (method) `cli/commands/persist_migrated.py:552` `def do_ivy(self, line)` -- Generates payloads using Ivy with various options.
- `PersistMigratedCommandSet.do_veil` (method) `cli/commands/persist_migrated.py:652` `def do_veil(self, line)` -- Generates payloads using Veil-Evasion with various options.
- `PersistMigratedCommandSet.do_scarecrow` (method) `cli/commands/persist_migrated.py:726` `def do_scarecrow(self, line)` -- Executes ScareCrow with various options for bypassing EDR solutions and executing shellcode. to create the...
- `PersistMigratedCommandSet.do_generate_revshell` (method) `cli/commands/persist_migrated.py:844` `def do_generate_revshell(self, line)` -- Generate a reverse shell in various programming languages.
- `PersistMigratedCommandSet.do_dr0p1t` (method) `cli/commands/persist_migrated.py:910` `def do_dr0p1t(self, line)` -- Execute the Dr0p1t tool to create a stealthy malware dropper.
- `PersistMigratedCommandSet.do_paranoid_meterpreter` (method) `cli/commands/persist_migrated.py:973` `def do_paranoid_meterpreter(self, line)` -- Creates and deploys a paranoid Meterpreter payload and listener with SSL/TLS pinning and UUID tracking.
- `PersistMigratedCommandSet.do_setoolKits` (method) `cli/commands/persist_migrated.py:1061` `def do_setoolKits(self, line)` -- Executes the SEToolKit workflow to generate a Meterpreter payload and configure the multi-handler using LHOST and...
- `PersistMigratedCommandSet.do_darkarmour` (method) `cli/commands/persist_migrated.py:1094` `def do_darkarmour(self, line)` -- Uses the darkarmour tool to generate an undetectable version of a PE executable.
- `PersistMigratedCommandSet.do_knokknok` (method) `cli/commands/persist_migrated.py:1162` `def do_knokknok(self, line)` -- Send special string to trigger a reverse shell, with the command 'c2 client_name' create a listener shell script to...
- `PersistMigratedCommandSet.do_listener_go` (method) `cli/commands/persist_migrated.py:1197` `def do_listener_go(self, line)` -- Configures and starts a listener for a specified victim.
- `PersistMigratedCommandSet.do_listener_py` (method) `cli/commands/persist_migrated.py:1264` `def do_listener_py(self, line)` -- Configures and starts a listener for a specified victim.
- `PersistMigratedCommandSet.do_service` (method) `cli/commands/persist_migrated.py:1331` `def do_service(self, line)` -- Creates a systemd service file for a specified binary and generates a script to enable and start the service.
- `PersistMigratedCommandSet.do_toctoc` (method) `cli/commands/persist_migrated.py:1404` `def do_toctoc(self, line)` -- Sends a magic packet to the Chinese malware.
- `PersistMigratedCommandSet.do_beaconcfg` (method) `cli/commands/persist_migrated.py:1427` `def do_beaconcfg(self, line)` -- Generate a C2 beacon profile with traffic morphing and domain fronting.

## cli/commands/phishing_wizard.py
Depends on: `cli/commands/_base.py`, `modules/backdoor/server.c`, `modules/phishing_orchestrator.py`, `utils.py`
- `PhishingWizardCommandSet.do_phish_wizard` (method) `cli/commands/phishing_wizard.py:190` `def do_phish_wizard(self, line)` -- Interactive end-to-end phishing campaign wizard.
- `PhishingWizardCommandSet.do_phish_serve` (method) `cli/commands/phishing_wizard.py:361` `def do_phish_serve(self, line)` -- Start a lightweight HTTP server for phishing landing pages.
- `PhishingHandler.log_message` (method) `cli/commands/phishing_wizard.py:389` `def log_message(self, format)`
- `PhishingHandler.do_GET` (method) `cli/commands/phishing_wizard.py:392` `def do_GET(self)`
- `PhishingHandler.do_POST` (method) `cli/commands/phishing_wizard.py:407` `def do_POST(self)`
- `PhishingHandler.do_OPTIONS` (method) `cli/commands/phishing_wizard.py:427` `def do_OPTIONS(self)`
- `PhishingHandler.do_phish_report` (method) `cli/commands/phishing_wizard.py:443` `def do_phish_report(self, line)` -- Show campaign results and captured credentials.
- `PhishingHandler.do_phisher` (method) `cli/commands/phishing_wizard.py:637` `def do_phisher(self, line)` -- Launch a phishing campaign against a target domain.

## cli/commands/pivoting.py
Depends on: `cli/commands/_base.py`, `core/hardening.py`, `utils.py`
- `PivotingCommandSet.do_autopivot` (method) `cli/commands/pivoting.py:43` `def do_autopivot(self, line)` -- Auto-detect internal networks and set up pivot tunnels.
- `PivotingCommandSet.do_pivot_status` (method) `cli/commands/pivoting.py:100` `def do_pivot_status(self, line)` -- Show the current pivot chain state.
- `PivotingCommandSet.do_pivot_kill` (method) `cli/commands/pivoting.py:119` `def do_pivot_kill(self, line)` -- Kill all pivot tunnels and clean up.
- `PivotingCommandSet.do_pivot_scan` (method) `cli/commands/pivoting.py:153` `def do_pivot_scan(self, line)` -- Scan internal networks through the current pivot chain.
- `PivotingCommandSet.do_pivot_proxy` (method) `cli/commands/pivoting.py:206` `def do_pivot_proxy(self, line)` -- Start a local SOCKS proxy through the pivot chain.

## cli/commands/postexp.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `PostExploitationCommandSet.do_lazywebshell` (method) `cli/commands/postexp.py:32` `def do_lazywebshell(self, line)` -- Run LazyOwn webshell server on port 8888.
- `PostExploitationCommandSet.do_disableav` (method) `cli/commands/postexp.py:45` `def do_disableav(self, line)` -- Create a VBS script to attempt disabling Windows Defender.
- `PostExploitationCommandSet.do_mimikatzpy` (method) `cli/commands/postexp.py:59` `def do_mimikatzpy(self, line)` -- Run Mimikatz over Python (impacket style).
- `PostExploitationCommandSet.do_scavenger` (method) `cli/commands/postexp.py:64` `def do_scavenger(self, line)` -- Run the Scavenger post-exploitation data collector.
- `PostExploitationCommandSet.do_follina` (method) `cli/commands/postexp.py:69` `def do_follina(self, line)` -- Run the Follina (CVE-2022-30190) exploit setup.
- `PostExploitationCommandSet.do_shellcode` (method) `cli/commands/postexp.py:74` `def do_shellcode(self, line)` -- Generate and manage shellcode.
- `PostExploitationCommandSet.do_ofuscatorps1` (method) `cli/commands/postexp.py:82` `def do_ofuscatorps1(self, line)` -- Obfuscate a PowerShell script.
- `PostExploitationCommandSet.do_atomic_lazyown` (method) `cli/commands/postexp.py:87` `def do_atomic_lazyown(self, line)` -- Execute atomic red-team tests via LazyOwn.

## cli/commands/postexp_migrated.py
Depends on: `cli/commands/_base.py`, `modules/yara_scanner.py`, `utils.py`
- `PostexpMigratedCommandSet.do_find` (method) `cli/commands/postexp_migrated.py:36` `def do_find(self, line)` -- Automates command execution based on a list of aliases and commands.
- `PostexpMigratedCommandSet.do_cports` (method) `cli/commands/postexp_migrated.py:305` `def do_cports(self, line)` -- Generates a command to display TCP and UDP ports and copies it to the clipboard.
- `PostexpMigratedCommandSet.do_rubeus` (method) `cli/commands/postexp_migrated.py:350` `def do_rubeus(self, line)` -- Copies a command to the clipboard for downloading and running Rubeus.
- `PostexpMigratedCommandSet.do_sessionsshstrace` (method) `cli/commands/postexp_migrated.py:390` `def do_sessionsshstrace(self, line)` -- Attach strace to a running process and log output to a file.
- `PostexpMigratedCommandSet.do_powershell_cmd_stager` (method) `cli/commands/postexp_migrated.py:441` `def do_powershell_cmd_stager(self, line)` -- Generate and execute a PowerShell command stager to run a .ps1 script.
- `PostexpMigratedCommandSet.do_shellcode_search` (method) `cli/commands/postexp_migrated.py:478` `def do_shellcode_search(self, line)` -- Search the shell-storm API for shellcodes using the provided keywords.
- `PostexpMigratedCommandSet.do_shellcode2sylk` (method) `cli/commands/postexp_migrated.py:526` `def do_shellcode2sylk(self, line)` -- Converts shellcode to SYLK format and saves the result to a file.
- `PostexpMigratedCommandSet.do_pezorsh` (method) `cli/commands/postexp_migrated.py:571` `def do_pezorsh(self, line)` -- Executes the PEzor tool to pack executables or shellcode with custom configurations.
- `PostexpMigratedCommandSet.do_pip_repo` (method) `cli/commands/postexp_migrated.py:642` `def do_pip_repo(self, line)` -- Sets up a local pip repository to serve Python packages for installation on a compromised machine without internet...
- `PostexpMigratedCommandSet.do_apt_repo` (method) `cli/commands/postexp_migrated.py:727` `def do_apt_repo(self, line)` -- Creates a comprehensive local APT repository with enhanced dependency resolution.
- `PostexpMigratedCommandSet.resolve_and_download_dependencies` (method) `cli/commands/postexp_migrated.py:773` `def resolve_and_download_dependencies(package_name)` -- Recursively resolve and download package dependencies with enhanced checks
- `PostexpMigratedCommandSet.do_createpayload` (method) `cli/commands/postexp_migrated.py:925` `def do_createpayload(self, line)` -- Generates an obfuscated payload to evade AV detection using the payloadGenerator tool. thanks to smokeme
- `PostexpMigratedCommandSet.do_bin2shellcode` (method) `cli/commands/postexp_migrated.py:975` `def do_bin2shellcode(self, line)` -- Converts a binary file to a shellcode string in C or Nim format.
- `PostexpMigratedCommandSet.do_exe2bin` (method) `cli/commands/postexp_migrated.py:1066` `def do_exe2bin(self, line)` -- Trasnform file .exe into binary file.
- `PostexpMigratedCommandSet.do_exe2donutbin` (method) `cli/commands/postexp_migrated.py:1093` `def do_exe2donutbin(self, line)` -- Trasnform file .exe into donut binary file.
- `PostexpMigratedCommandSet.do_issue_command_to_c2` (method) `cli/commands/postexp_migrated.py:1117` `def do_issue_command_to_c2(self, line)` -- Exec command in the client using the C2. download: command you must put the file in sessions/temp_upload or use...
- `PostexpMigratedCommandSet.do_d3monizedshell` (method) `cli/commands/postexp_migrated.py:1141` `def do_d3monizedshell(self, line)` -- Executes the D3m0n1z3dShell tool for persistence in Linux.
- `PostexpMigratedCommandSet.do_scp` (method) `cli/commands/postexp_migrated.py:1174` `def do_scp(self, line)` -- Copies the local "sessions" directory to a remote host using scp, leveraging sshpass for automated authentication.
- `PostexpMigratedCommandSet.do_apt_proxy` (method) `cli/commands/postexp_migrated.py:1265` `def do_apt_proxy(self, line)` -- Configures the local machine with internet access to act as an APT proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_pip_proxy` (method) `cli/commands/postexp_migrated.py:1322` `def do_pip_proxy(self, line)` -- Configures the local machine with internet access to act as a pip proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_internet_proxy` (method) `cli/commands/postexp_migrated.py:1378` `def do_internet_proxy(self, line)` -- Configures the local machine with internet access to act as a proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_shellcode2elf` (method) `cli/commands/postexp_migrated.py:1439` `def do_shellcode2elf(self, line)` -- Convert shellcode into an ELF file and infect it.
- `PostexpMigratedCommandSet.do_ssh_cmd` (method) `cli/commands/postexp_migrated.py:1522` `def do_ssh_cmd(self, line)` -- Perform Remote Execution Command through SSH using configured start_user.
- `PostexpMigratedCommandSet.do_service_ssh` (method) `cli/commands/postexp_migrated.py:1551` `def do_service_ssh(self, line)` -- Creates a systemd service file for a specified binary and generates a script to enable and start the service.
- `PostexpMigratedCommandSet.do_ofuscatesh` (method) `cli/commands/postexp_migrated.py:1625` `def do_ofuscatesh(self, line)` -- Obfuscates a shell script by encoding it in Base64 and prepares a command to decode and execute it.
- `PostexpMigratedCommandSet.do_ofuscate_payload` (method) `cli/commands/postexp_migrated.py:1655` `def do_ofuscate_payload(self, line)` -- Obfuscates a shell script by encoding it in Base64 and prepares a command to decode and execute it.
- `PostexpMigratedCommandSet.do_adversary` (method) `cli/commands/postexp_migrated.py:1684` `def do_adversary(self, line)` -- LazyOwn RedTeam Adversary Emulator, you can configure your own adversaries in adversary.json
- `PostexpMigratedCommandSet.do_ofuscate_string` (method) `cli/commands/postexp_migrated.py:1825` `def do_ofuscate_string(self, line)` -- Ofuscate a string into Go code.
- `PostexpMigratedCommandSet.do_path2hex` (method) `cli/commands/postexp_migrated.py:1867` `def do_path2hex(self, line)` -- Convert a binary path to x64 little-endian hex code for shellcode injection.
- `PostexpMigratedCommandSet.do_hex2shellcode` (method) `cli/commands/postexp_migrated.py:1914` `def do_hex2shellcode(self, line)` -- Convert raw hex payload from msfvenom into NASM-compatible shellcode format.
- `PostexpMigratedCommandSet.do_create_synthetic` (method) `cli/commands/postexp_migrated.py:1971` `def do_create_synthetic(self, line)` -- Create a basic synthetic playbook from Nmap CSV when LLM fails.
- `PostexpMigratedCommandSet.do_extract_yaml` (method) `cli/commands/postexp_migrated.py:2022` `def do_extract_yaml(self, line)` -- Extract YAML from an existing debug file and try to create a playbook.
- `PostexpMigratedCommandSet.do_convert_remcomsvc_from_file` (method) `cli/commands/postexp_migrated.py:2083` `def do_convert_remcomsvc_from_file(self, arg)` -- Converts the Python REMCOMSVC byte string from remcomsvc.py to Golang byte slice format, prints a sample, and saves...
- `PostexpMigratedCommandSet.do_adversary_yaml` (method) `cli/commands/postexp_migrated.py:2115` `def do_adversary_yaml(self, line)` -- Execute adversary from YAML in lazyadversaries/*.yaml Syntax: adversary [id] [l|r|n]
- `PostexpMigratedCommandSet.do_add2find` (method) `cli/commands/postexp_migrated.py:2197` `def do_add2find(self, line)` -- Add a new custom command to the 'find' system, saved in user_commands.json.
- `PostexpMigratedCommandSet.do_rmfromfind` (method) `cli/commands/postexp_migrated.py:2225` `def do_rmfromfind(self, line)` -- Remove a custom command by index (as shown in 'find').
- `PostexpMigratedCommandSet.do_aes_pe` (method) `cli/commands/postexp_migrated.py:2254` `def do_aes_pe(self, line)` -- Encrypt with AES and random key to PE EXE file, to usage with loaders.
- `PostexpMigratedCommandSet.do_yara_scan` (method) `cli/commands/postexp_migrated.py:2281` `def do_yara_scan(self, line)` -- Scan files or directories with YARA rules for malware/IOCs.


Next: [API_p3.md](API_p3.md)
