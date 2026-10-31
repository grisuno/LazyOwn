# static/js

*Community 7 | 49 files | cohesion 0.36*

## Definition

This community groups 49 file(s) rooted at `static/js` with dominant language py (cohesion 0.36). Central symbols: `A`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`, `AddonYamlRenderer`, `As`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

### `static/js` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |

### `tests` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_audit_remediation.py` | py | testing | 28 | yes |
| `tests/test_backdoor_random.py` | py | testing | 5 | yes |

### `modules` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/auto_purple.py` | py | utility | 40 | yes |
| `modules/exp.c` | c | utility | 58 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/config.py` | py | infrastructure | 20 | yes |
| `core/param_registry.py` | py | utility | 17 | yes |

### `cli` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/purple_tui.py` | py | utility | 15 | yes |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/params_ops.py` | py | utility | 2 | yes |
| `cli/commands/persist_migrated.py` | py | utility | 29 | yes |

### `lazyc2` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 39 | yes |
| `lazyc2/state.py` | py | utility | 0 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/core_smoke.py` | py | utility | 4 | yes |

*... and 29 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:42`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `ParamCommandSet` (class, `cli/commands/params_ops.py:31`) `class ParamCommandSet(LazyOwnCommandSet)` - Create, inspect and delete the shared parameters.
- `do_param` (method, `cli/commands/params_ops.py:38`) `def do_param(self, line)` - Manage the shared parameter catalog used by addons and aliases.
- `PersistMigratedCommandSet` (class, `cli/commands/persist_migrated.py:32`) `class PersistMigratedCommandSet(LazyOwnCommandSet)`
- `generate_backdoor_username` (method, `cli/commands/persist_migrated.py:37`) `def generate_backdoor_username()` - Generate a random backdoor username (same shape as C2 operators).
- `generate_backdoor_password` (method, `cli/commands/persist_migrated.py:43`) `def generate_backdoor_password()` - Generate a random backdoor password safe for assign, chpasswd and CLIs.
- `resolve_backdoor_creds` (method, `cli/commands/persist_migrated.py:53`) `def resolve_backdoor_creds(params)` - Return configured creds, or fresh random ones when unset.
- `_ensure_backdoor_creds` (method, `cli/commands/persist_migrated.py:68`) `def _ensure_backdoor_creds(self)` - Return usable backdoor creds, generating + persisting when unset.
- `do_pwncat` (method, `cli/commands/persist_migrated.py:91`) `def do_pwncat(self, line)` - Runs `pwncat` with the specified port for listening. SELFINJECT
- `do_ftp` (method, `cli/commands/persist_migrated.py:135`) `def do_ftp(self, line)` - Connects to an ftp host using credentials from a file and a specified port.
- `do_rdp` (method, `cli/commands/persist_migrated.py:194`) `def do_rdp(self, line)` - Reads credentials from a file, encrypts the password, and executes the RDP connection command.
- `do_grisun0` (method, `cli/commands/persist_migrated.py:268`) `def do_grisun0(self, line)` - Creates and copies a shell command to add a new user, assign a password, add the user to the sudo gr
- `do_grisun0w` (method, `cli/commands/persist_migrated.py:312`) `def do_grisun0w(self, line)` - Creates and copies a PowerShell command to add a new user, assign a password, add the user to the Ad
- `do_asprevbase64` (method, `cli/commands/persist_migrated.py:354`) `def do_asprevbase64(self, line)` - Creates a base64 encoded ASP reverse shell payload and copies it to the clipboard.
- `do_weevelygen` (method, `cli/commands/persist_migrated.py:392`) `def do_weevelygen(self, line)` - Generate a PHP backdoor using Weevely, protected with the given password.
- `do_weevely` (method, `cli/commands/persist_migrated.py:432`) `def do_weevely(self, line)` - Connect to PHP backdoor using Weevely, protected with the given password.
- `do_backdoor_factory` (method, `cli/commands/persist_migrated.py:478`) `def do_backdoor_factory(self, line)` - Creates a backdoored executable using `backdoor-factory`.
- `do_msfpc` (method, `cli/commands/persist_migrated.py:524`) `def do_msfpc(self, line)` - Generates payloads using MSFvenom Payload Creator (MSFPC).
- `do_ivy` (method, `cli/commands/persist_migrated.py:605`) `def do_ivy(self, line)` - Generates payloads using Ivy with various options. Ivy is a payload creation framework for the execu
- `do_veil` (method, `cli/commands/persist_migrated.py:705`) `def do_veil(self, line)` - Generates payloads using Veil-Evasion with various options. Veil-Evasion is a payload creation frame
- `do_scarecrow` (method, `cli/commands/persist_migrated.py:779`) `def do_scarecrow(self, line)` - Executes ScareCrow with various options for bypassing EDR solutions and executing shellcode.
- `do_generate_revshell` (method, `cli/commands/persist_migrated.py:897`) `def do_generate_revshell(self, line)` - Generate a reverse shell in various programming languages.
- `do_dr0p1t` (method, `cli/commands/persist_migrated.py:963`) `def do_dr0p1t(self, line)` - Execute the Dr0p1t tool to create a stealthy malware dropper.
- `do_paranoid_meterpreter` (method, `cli/commands/persist_migrated.py:1026`) `def do_paranoid_meterpreter(self, line)` - Creates and deploys a paranoid Meterpreter payload and listener with SSL/TLS pinning and UUID tracki
- `do_setoolKits` (method, `cli/commands/persist_migrated.py:1114`) `def do_setoolKits(self, line)` - Executes the SEToolKit workflow to generate a Meterpreter payload
- `do_darkarmour` (method, `cli/commands/persist_migrated.py:1147`) `def do_darkarmour(self, line)` - Uses the darkarmour tool to generate an undetectable version of a PE executable.
- `do_knokknok` (method, `cli/commands/persist_migrated.py:1215`) `def do_knokknok(self, line)` - Send special string to trigger a reverse shell, with the command 'c2 client_name'
- `do_listener_go` (method, `cli/commands/persist_migrated.py:1250`) `def do_listener_go(self, line)` - Configures and starts a listener for a specified victim.
- `do_listener_py` (method, `cli/commands/persist_migrated.py:1317`) `def do_listener_py(self, line)` - Configures and starts a listener for a specified victim.
- `do_service` (method, `cli/commands/persist_migrated.py:1384`) `def do_service(self, line)` - Creates a systemd service file for a specified binary and generates a script to enable and start the

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 314
- Cross-boundary resolved imports (EXTRACTED): 233

## Connections

- [EXTRACTED] depends_on community 3 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/aliases.py imports core/config.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports core/config.py.
- [EXTRACTED] depends_on community 4 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/param_registry.py` via `subprocess` (4 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/payload_schema.py`

## Open Questions

- Why do 7 file(s) lack file-level docs (e.g. `key.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` be broken with an interface?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.36?

## Sources

- `cli/assign.py`
- `cli/commands/params_ops.py`
- `cli/commands/persist_migrated.py`
- `cli/commands/purple_team.py`
- `cli/commands/session_ops.py`
- `cli/purple_tui.py`
- `cli/session_resumer.py`
- `cli/show.py`
- `core/config.py`
- `core/param_registry.py`
- `core/payload_schema.py`
- `core/process.py`
- `core/prompt.py`
- `key.py`
- `lazyc2/addon_creator.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/auto_purple.py`
- `modules/exp.c`
- `modules/gym_cleanup.py`
- *... and 29 more*
