# modules: lazy_loop

*Community 3 | 110 files | cohesion 0.58*

## Definition

This community groups 110 file(s) rooted at `tests` with dominant language py (cohesion 0.58). Central symbols: `ADCSCertipyWrapper`, `ActivityLog`, `AssetGate`, `AssetGraph`, `AssetNode`, `AutoVerb`, `Budget`, `CertificateAuthority`. Core file: `modules/lazy_loop.py` (453 symbols). Documented purpose: Container and Kubernetes attack command set.  Commands for Docker enumeration, Kubernetes cluster reconnaissance, pod escape detection, and container privilege .

## Files

### `tests` (47 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_registry.py` | py | testing | 20 | yes |
| `tests/test_chain_list_command.py` | py | testing | 2 | yes |
| `tests/test_gym_cli.py` | py | testing | 8 | yes |

### `modules` (39 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/atomic_exploit_bridge.py` | py | utility | 37 | yes |

### `modules/sinks` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/attack_graph.py` | py | utility | 1 | yes |
| `modules/sinks/c2_surfaces.py` | py | utility | 1 | yes |
| `modules/sinks/intel_graph.py` | py | utility | 1 | yes |

### `cli/commands` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/containers.py` | py | infrastructure | 7 | yes |
| `cli/commands/exploit_migrated.py` | py | utility | 52 | yes |
| `cli/commands/lazyloop.py` | py | utility | 12 | yes |

### `cli` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/lazy_monitor.py` | py | utility | 46 | yes |
| `cli/lazy_orchestrator.py` | py | utility | 36 | yes |
| `cli/orchestrator_assets_tabs.py` | py | utility | 56 | yes |

### `modules/tools` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/tools/__init__.py` | py | utility | 0 | yes |
| `modules/tools/loop_smoke.py` | py | utility | 10 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/autonomous.py` | py | utility | 3 | yes |
| `core/terminal_guard.py` | py | utility | 8 | yes |

### `lazyc2/blueprints` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/orchestrator.py` | py | presentation | 17 | yes |

*... and 90 more files in this community.*


## Key Symbols

- `ContainerCommandSet` (class, `cli/commands/containers.py:30`) `class ContainerCommandSet(LazyOwnCommandSet)` - Container and Kubernetes attack commands.
- `do_docker_enum` (method, `cli/commands/containers.py:37`) `def do_docker_enum(self, _line)` - Enumerate Docker host: containers, images, privileges, mounts.
- `do_k8s_enum` (method, `cli/commands/containers.py:101`) `def do_k8s_enum(self, _line)` - Enumerate Kubernetes cluster: pods, secrets, SAs, RBAC.
- `do_container_escape` (method, `cli/commands/containers.py:169`) `def do_container_escape(self, _line)` - Check current container for known escape vectors.
- `do_k8s_pods` (method, `cli/commands/containers.py:239`) `def do_k8s_pods(self, line)` - List Kubernetes pods with security-relevant details.
- `do_k8s_secrets` (method, `cli/commands/containers.py:283`) `def do_k8s_secrets(self, line)` - List and decode Kubernetes secrets.
- `do_container_detect` (method, `cli/commands/containers.py:334`) `def do_container_detect(self, _line)` - Auto-detect container runtime and escape primitives.
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
- `do_ms08_067_netapi` (method, `cli/commands/exploit_migrated.py:1053`) `def do_ms08_067_netapi(self, line)` - SMB CVE-2008-4250. Vulnerable using the module ms08_067_netapi of metasploit
- `do_xss` (method, `cli/commands/exploit_migrated.py:1090`) `def do_xss(self, line)` - Executes the XSS (Cross-Site Scripting) vulnerability testing procedure
- `do_template_helper_serializer` (method, `cli/commands/exploit_migrated.py:1135`) `def do_template_helper_serializer(self, line)` - Handles the creation and serialization of a template helper.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 778
- Cross-boundary resolved imports (EXTRACTED): 394

## Connections

- [EXTRACTED] depends_on community 2 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/command_form.py imports cli/commands/containers.py.
- [EXTRACTED] depends_on community 5 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 7 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/atomic_exploit_bridge.py.
- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/containers.py imports cli/commands/_base.py.

## Risks

- [cycle] `modules/auto_registry.py` -> `modules/orchestrator_config.py` -> `modules/trigger_policy.py` -> `modules/loop_triggers.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/orchestrator_config.py` -> `modules/trigger_policy.py` -> `modules/loop_triggers.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/auto_registry.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/lazy_mentions.py` -> `modules/lazy_loop.py`
- [cycle] `modules/auto_registry.py` -> `modules/orchestrator_config.py` -> `modules/trigger_policy.py` -> `modules/loop_triggers.py` -> `modules/lazy_loop.py` -> `modules/lazy_installer.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/orchestrator_config.py` -> `modules/trigger_policy.py` -> `modules/loop_triggers.py` -> `modules/lazy_loop.py` -> `modules/custom_tools.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/orchestrator_config.py` -> `modules/trigger_policy.py` -> `modules/loop_triggers.py` -> `modules/lazy_loop.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/orchestrator_config.py` -> `modules/trigger_policy.py` -> `modules/loop_triggers.py` -> `modules/lazy_loop.py` -> `modules/auto_registry.py`
- [cycle] `modules/orchestrator_config.py` -> `modules/trigger_policy.py` -> `modules/loop_triggers.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py`

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `modules/__init__.py`)? What purpose do they serve?
- Can the cycle `modules/auto_registry.py` -> `modules/orchestrator_config.py` -> `modules/trigger_policy.py` -> `modules/loop_triggers.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` be broken with an interface?
- What would break if the most connected file in modules: lazy_loop changed?
- Should modules: lazy_loop be split, given cohesion 0.58?

## Sources

- `cli/commands/containers.py`
- `cli/commands/exploit_migrated.py`
- `cli/commands/lazyloop.py`
- `cli/commands/lazyops.py`
- `cli/commands/redteam_gym.py`
- `cli/commands/retry_ops.py`
- `cli/lazy_monitor.py`
- `cli/lazy_orchestrator.py`
- `cli/orchestrator_assets_tabs.py`
- `cli/session_brief.py`
- `cli/tui_forms.py`
- `core/autonomous.py`
- `core/terminal_guard.py`
- `lazyc2/blueprints/orchestrator.py`
- `modules/__init__.py`
- `modules/adcs_attacks.py`
- `modules/atomic_exploit_bridge.py`
- `modules/auto_registry.py`
- `modules/custom_tools.py`
- `modules/exploit_chain.py`
- *... and 90 more*
