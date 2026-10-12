# modules: lazy_loop

*Community 4 | 79 files | cohesion 0.58*

## Definition

This community groups 79 file(s) rooted at `tests` with dominant language py (cohesion 0.58). Central symbols: `ADCSCertipyWrapper`, `AIModel`, `ASTToolExtractor`, `ActivityLog`, `AgentBridgeWorker`, `AgentRunner`, `AgentTool`, `AiCommandSet`. Core file: `modules/lazy_loop.py` (440 symbols). Documented purpose: Artificial Intelligence command set.  Covers the ``do_ask``, ``do_groq``, ``do_ai_playbook`` and ``do_ai_toggle`` commands. ``ask`` answers through the configur.

## Files

### `tests` (33 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/conftest.py` | py | testing | 10 | yes |
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_asset_gate.py` | py | testing | 16 | yes |

### `modules` (30 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/agent_runner.py` | py | utility | 37 | yes |
| `modules/ai_model.py` | py | business_logic | 33 | yes |

### `cli/commands` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/ai.py` | py | utility | 8 | yes |
| `cli/commands/exploit_migrated.py` | py | utility | 52 | yes |
| `cli/commands/lazyloop.py` | py | utility | 12 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/autonomous.py` | py | utility | 3 | yes |
| `core/config.py` | py | infrastructure | 17 | yes |
| `core/llm_budget.py` | py | utility | 45 | yes |

### `modules/tools` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/tools/__init__.py` | py | utility | 0 | yes |
| `modules/tools/loop_smoke.py` | py | utility | 10 | yes |
| `modules/tools/monitor_smoke.py` | py | utility | 3 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/lazy_monitor.py` | py | utility | 46 | yes |
| `cli/lazy_orchestrator.py` | py | utility | 40 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyllmchat.py` | py | utility | 30 | no |

*... and 59 more files in this community.*


## Key Symbols

- `AiCommandSet` (class, `cli/commands/ai.py:71`) `class AiCommandSet(LazyOwnCommandSet)` - Pending phase module for the Artificial Intelligence commands.
- `do_ask` (method, `cli/commands/ai.py:78`) `def do_ask(self, line)` - Ask the AI a question with current session context pre-loaded.
- `do_groq` (method, `cli/commands/ai.py:166`) `def do_groq(self, line)` - Generate a single-line command through the Groq backend.
- `do_poolcheck` (method, `cli/commands/ai.py:197`) `def do_poolcheck(self, line)` - Prove the LLM failover pool order with one live prompt.
- `_serve` (function, `cli/commands/ai.py:220`) `def _serve(member_id, backend_name, text)`
- `do_ai_playbook` (method, `cli/commands/ai.py:254`) `def do_ai_playbook(self, line)` - Generate an offensive playbook from Nmap CSV + KB + Ollama.
- `do_ai_toggle` (method, `cli/commands/ai.py:361`) `def do_ai_toggle(self, _arg)` - Toggle the in-process AI assistant on or off.
- `do_llm_budget` (method, `cli/commands/ai.py:378`) `def do_llm_budget(self, line)` - Show the LLM daily cost budget, per call token cap, and current spend.
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 590
- Cross-boundary resolved imports (EXTRACTED): 236

## Connections

- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/aliases.py imports core/config.py.
- [EXTRACTED] depends_on community 7 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 4 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_adapter.py.
- [EXTRACTED] depends_on community 4 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 3 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports core/config.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [cycle] `modules/llm_factory.py` -> `modules/ai_model.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/ai_model.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/ai_model.py` -> `modules/llm_factory.py`
- [cycle] `modules/auto_registry.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [cycle] `modules/lazy_loop.py` -> `modules/custom_tools.py` -> `modules/lazy_loop.py`
- [cycle] `cli/lazy_monitor.py` -> `modules/lazy_runner.py` -> `cli/lazy_monitor.py`

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `contrib/legacy/lazyllmchat.py`)? What purpose do they serve?
- Can the cycle `modules/llm_factory.py` -> `modules/ai_model.py` be broken with an interface?
- What would break if the most connected file in modules: lazy_loop changed?
- Should modules: lazy_loop be split, given cohesion 0.58?

## Sources

- `cli/commands/ai.py`
- `cli/commands/exploit_migrated.py`
- `cli/commands/lazyloop.py`
- `cli/commands/lazyops.py`
- `cli/commands/mcp_bridge.py`
- `cli/lazy_monitor.py`
- `cli/lazy_orchestrator.py`
- `contrib/legacy/lazyllmchat.py`
- `core/autonomous.py`
- `core/config.py`
- `core/llm_budget.py`
- `core/payload_schema.py`
- `core/terminal_guard.py`
- `modules/__init__.py`
- `modules/adcs_attacks.py`
- `modules/agent_runner.py`
- `modules/ai_model.py`
- `modules/auto_registry.py`
- `modules/custom_tools.py`
- `modules/exploit_chain.py`
- *... and 59 more*
