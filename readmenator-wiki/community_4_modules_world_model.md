# modules: world_model

*Community 4 | 62 files | cohesion 0.41*

## Definition

This community groups 62 file(s) rooted at `modules` with dominant language py (cohesion 0.41). Central symbols: `ADCSCertipyWrapper`, `BinaryAttacker`, `BinaryFinder`, `C2Server`, `C2SessionCommandSet`, `CertificateTemplate`, `ChainResult`, `CredentialEntry`. Core file: `modules/world_model.py` (70 symbols). Documented purpose: C2 session CommandSet — headless server, agent deploy, exec, loot.  Every command is non-interactive and loop-routable: explicit arguments, JSON-able results on.

## Files

### `modules` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/atomic_exploit_bridge.py` | py | utility | 37 | yes |
| `modules/attack_surface3d.py` | py | utility | 11 | yes |

### `tests` (17 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_beacon_recon_sink.py` | py | testing | 18 | yes |
| `tests/test_c2_surfaces.py` | py | testing | 12 | yes |

### `modules/sinks` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/attack_graph.py` | py | utility | 1 | yes |
| `modules/sinks/c2_surfaces.py` | py | utility | 1 | yes |
| `modules/sinks/intel_graph.py` | py | utility | 1 | yes |

### `cli/commands` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/c2_session.py` | py | utility | 10 | yes |
| `cli/commands/exploit_migrated.py` | py | utility | 52 | yes |
| `cli/commands/exploitgym.py` | py | utility | 10 | yes |

### `contrib/legacy` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |
| `contrib/legacy/lazypwn.py` | py | utility | 15 | no |
| `contrib/legacy/lazyvsftp.py` | py | utility | 3 | no |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/surface_graph.py` | py | utility | 33 | yes |
| `cli/surface_tui.py` | py | utility | 19 | yes |

### `lazygui` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/__init__.py` | py | utility | 0 | yes |
| `lazygui/version.py` | py | utility | 0 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/autonomous.py` | py | utility | 3 | yes |

*... and 42 more files in this community.*


## Key Symbols

- `_lab_auth` (function, `cli/commands/c2_session.py:24`) `def _lab_auth()` - Return (user, password, https_port, http_port) for the lab C2.
- `_fresh_lab_creds` (function, `cli/commands/c2_session.py:54`) `def _fresh_lab_creds()` - Generate fully random lab operator credentials (no fixed affixes).
- `_server` (function, `cli/commands/c2_session.py:65`) `def _server(user, password, port)` - Build a C2Server bound to lab auth (generates lab creds when needed).
- `_issue` (function, `cli/commands/c2_session.py:83`) `def _issue(client_id, command, auth, https_port)` - POST one command to the C2 issue endpoint (no prompts, ever).
- `C2SessionCommandSet` (class, `cli/commands/c2_session.py:108`) `class C2SessionCommandSet(LazyOwnCommandSet)` - Headless C2 lifecycle + session ops: server, deploy, exec, loot.
- `do_c2_server` (method, `cli/commands/c2_session.py:115`) `def do_c2_server(self, line)` - Manage the headless C2 server (lab use).
- `do_c2_reboot` (method, `cli/commands/c2_session.py:168`) `def do_c2_reboot(self, line)` - Restart the headless C2 server with ROTATED operator credentials.
- `do_c2_deploy` (method, `cli/commands/c2_session.py:249`) `def do_c2_deploy(self, line)` - Deploy the malleable agent to a lab target (needs root shell primitive).
- `do_c2_exec` (method, `cli/commands/c2_session.py:299`) `def do_c2_exec(self, line)` - Run one command on a live C2 session and print its answer.
- `do_c2_loot` (method, `cli/commands/c2_session.py:346`) `def do_c2_loot(self, line)` - Exfiltrate a remote file through a live C2 session into sessions/loot/.
- `ExploitMigratedCommandSet` (class, `cli/commands/exploit_migrated.py:38`) `class ExploitMigratedCommandSet(LazyOwnCommandSet)`
- `do_cp` (method, `cli/commands/exploit_migrated.py:43`) `def do_cp(self, line)` - Copies a file from the ExploitDB directory to the sessions directory.
- `do_createcookie` (method, `cli/commands/exploit_migrated.py:84`) `def do_createcookie(self, line)` - Creates a `cookie.txt` file in the `sessions` directory with the specified cookie value.
- `do_py3ttyup` (method, `cli/commands/exploit_migrated.py:128`) `def do_py3ttyup(self, line)` - Copies a Python reverse shell command to the clipboard.
- `do_pyautomate` (method, `cli/commands/exploit_migrated.py:164`) `def do_pyautomate(self, line)` - Automates the execution of pwntomate tools on XML configuration files.
- `do_winbase64payload` (method, `cli/commands/exploit_migrated.py:215`) `def do_winbase64payload(self, line)` - Creates a base64 encoded payload specifically for Windows to execute a PowerShell command or downloa
- `do_createdll` (method, `cli/commands/exploit_migrated.py:344`) `def do_createdll(self, line)` - Create a Windows DLL file using MinGW-w64 or a Blazor DLL for Linux.
- `do_seo` (method, `cli/commands/exploit_migrated.py:402`) `def do_seo(self, line)` - Performs a web seo fingerprinting scan using `lazyseo.py`.
- `do_padbuster` (method, `cli/commands/exploit_migrated.py:437`) `def do_padbuster(self, line)` - Execute the PadBuster command for padding oracle attacks.
- `do_cacti_exploit` (method, `cli/commands/exploit_migrated.py:483`) `def do_cacti_exploit(self, line)` - Automates the exploitation of the Cacti version 1.2.26 vulnerability
- `setup_handler` (function, `cli/commands/exploit_migrated.py:513`) `def setup_handler(config_file, lhost, lport)` - Sets up a Metasploit multi/handler exploit configuration in the provided config file.
- `cacti_exploit` (function, `cli/commands/exploit_migrated.py:536`) `def cacti_exploit(config_file, host)` - Configures an exploit for the Cacti Package Import Remote Code Execution vulnerability in the provid
- `do_shellshock` (method, `cli/commands/exploit_migrated.py:568`) `def do_shellshock(self, line)` - Executes a Shellshock attack against a target.
- `do_powerserver` (method, `cli/commands/exploit_migrated.py:630`) `def do_powerserver(self, line)` - This function generates a PowerShell script that retrieves reverse shell over http on a Windows syst
- `do_sqli` (method, `cli/commands/exploit_migrated.py:693`) `def do_sqli(self, line)` - Asks the user for the URL, database, table, and columns, and then executes the Python script
- `do_sharpshooter` (method, `cli/commands/exploit_migrated.py:724`) `def do_sharpshooter(self, line)` - Executes a payload creation framework for the retrieval and execution of arbitrary CSharp source cod
- `do_shellfire` (method, `cli/commands/exploit_migrated.py:768`) `def do_shellfire(self, line)` - Runs Shellfire with various options and allows generating payloads.
- `do_downloader` (method, `cli/commands/exploit_migrated.py:892`) `def do_downloader(self, line)` - Generate a downloader command for files in the sessions directory.
- `do_eternal` (method, `cli/commands/exploit_migrated.py:972`) `def do_eternal(self, line)` - Automates the EternalBlue (MS17-010) exploitation process using Metasploit.
- `do_rejetto_hfs_exec` (method, `cli/commands/exploit_migrated.py:1016`) `def do_rejetto_hfs_exec(self, line)` - HttpFileServer version 2.3. Vulnerable using the module rejetto_hfs_exec of metasploit

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 160
- Cross-boundary resolved imports (EXTRACTED): 294

## Connections

- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/c2_session.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 7 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/atomic_exploit_bridge.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_intel.py`
- [cycle] `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/unified_dashboard.py` -> `skills/hive_mind.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [layer strict] `tests/test_c2_surfaces.py` (testing) -> `contrib/legacy/lazydeepseekcli.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:184` `validate_client_id` `ct`: Result of allocator stored in `ct` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:234` `validate_client_id` `data`: Result of allocator stored in `data` is never checked against NULL.

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `contrib/legacy/lazypwn.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- What would break if the most connected file in modules: world_model changed?
- Should modules: world_model be split, given cohesion 0.41?

## Sources

- `cli/commands/c2_session.py`
- `cli/commands/exploit_migrated.py`
- `cli/commands/exploitgym.py`
- `cli/commands/pwn.py`
- `cli/commands/redteam_gym.py`
- `cli/commands/surface.py`
- `cli/surface_graph.py`
- `cli/surface_tui.py`
- `contrib/legacy/lazydeepseekcli.py`
- `contrib/legacy/lazypwn.py`
- `contrib/legacy/lazyvsftp.py`
- `contrib/legacy/sql.py`
- `core/autonomous.py`
- `lazygui/__init__.py`
- `lazygui/version.py`
- `modules/adcs_attacks.py`
- `modules/atomic_exploit_bridge.py`
- `modules/attack_surface3d.py`
- `modules/beacon_recon.py`
- `modules/c2_agent.py`
- *... and 42 more*
