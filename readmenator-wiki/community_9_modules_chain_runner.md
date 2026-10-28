# modules: chain_runner

*Community 9 | 38 files | cohesion 0.54*

## Definition

This community groups 38 file(s) rooted at `tests` with dominant language py (cohesion 0.54). Central symbols: `Chain`, `ChainArgs`, `ChainFactsSpoolSpec`, `ChainRunResult`, `ChainRunner`, `ChainStep`, `CommandAndControlMigratedCommandSet`, `Comparison`. Core file: `modules/chain_runner.py` (41 symbols). Documented purpose: Parsing, printing and replanning support for the ``apt_chain`` CLI.  Keeps ``cli.commands.command_and_control_migrated`` thin: argument parsing, step selection,.

## Files

### `tests` (18 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_apt_chain_admin.py` | py | testing | 22 | yes |
| `tests/test_apt_chain_integration.py` | py | testing | 6 | yes |
| `tests/test_chain_distill.py` | py | testing | 15 | yes |
| `tests/test_chain_evidence.py` | py | testing | 27 | yes |
| `tests/test_chain_parallel_fallback.py` | py | testing | 26 | yes |
| `tests/test_chain_registry.py` | py | testing | 9 | yes |
| `tests/test_chain_runner.py` | py | testing | 39 | yes |
| `tests/test_chain_synth.py` | py | testing | 10 | yes |

### `modules` (16 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/atomic_cli.py` | py | utility | 11 | yes |
| `modules/chain_distill.py` | py | utility | 19 | yes |
| `modules/chain_facts.py` | py | utility | 3 | yes |
| `modules/chain_registry.py` | py | utility | 17 | yes |
| `modules/chain_runner.py` | py | utility | 41 | yes |
| `modules/chain_state.py` | py | utility | 5 | yes |
| `modules/chain_synth.py` | py | utility | 6 | yes |
| `modules/closedloop.py` | py | utility | 7 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/apt_chain_support.py` | py | utility | 17 | yes |
| `cli/retry_support.py` | py | utility | 10 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/command_and_control_migrated.py` | py | utility | 34 | yes |
| `cli/commands/retry_ops.py` | py | utility | 8 | yes |

*... and 18 more files in this community.*


## Key Symbols

- `_token_name_ok` (function, `cli/apt_chain_support.py:42`) `def _token_name_ok(name)` - True when a name matches the chain token grammar.
- `ChainArgs` (class, `cli/apt_chain_support.py:48`) `class ChainArgs` - Parsed ``apt_chain`` invocation.
- `parse_chain_args` (function, `cli/apt_chain_support.py:72`) `def parse_chain_args(line)` - Parse one ``apt_chain`` command line into structured args.
- `_set_value` (function, `cli/apt_chain_support.py:141`) `def _set_value(args, flag, value)` - Assign one valued option onto the args struct.
- `resolve_admin` (function, `cli/apt_chain_support.py:169`) `def resolve_admin(args)` - Execute an admin action against the registry and checkpoint store.
- `select_step_ids` (function, `cli/apt_chain_support.py:257`) `def select_step_ids(chain, args)` - Resolve --step/--from-step/--to-step into one id set.
- `adversarial_continue` (function, `cli/apt_chain_support.py:289`) `def adversarial_continue(chain)` - Return a copy of the chain where every step continues on error.
- `render_result` (function, `cli/apt_chain_support.py:297`) `def render_result(result)` - Render one chain result as operator lines (JSON mode prints dict).
- `build_cli_approver` (function, `cli/apt_chain_support.py:330`) `def build_cli_approver(printer, input_fn)` - Return an approver baked for interactive operators.
- `approve` (function, `cli/apt_chain_support.py:338`) `def approve(step_id, command)`
- `build_reactive_replanner` (function, `cli/apt_chain_support.py:352`) `def build_reactive_replanner()` - Return a replanner driven by ``modules.reactive_engine``.
- `replan` (function, `cli/apt_chain_support.py:355`) `def replan(context)`
- `_decision_command` (function, `cli/apt_chain_support.py:377`) `def _decision_command(decision)` - Extract one actionable command from a reactive decision.
- `_step_from_decision` (function, `cli/apt_chain_support.py:386`) `def _step_from_decision(command, outcome, executed_count)` - Build one safe replan step from a suggested command.
- `_recent_changes_block` (function, `cli/apt_chain_support.py:408`) `def _recent_changes_block(target)` - Recent world changes on the target for one LLM recovery prompt.
- `build_llm_recovery_chain` (function, `cli/apt_chain_support.py:436`) `def build_llm_recovery_chain(result, target, task_id)` - Ask the LLM pool for a temporary recovery chain after a failed run.
- `_platform` (function, `cli/apt_chain_support.py:510`) `def _platform()` - Guess the loop platform from the payload configuration.
- `select_agent_flavour` (function, `cli/commands/command_and_control_migrated.py:43`) `def select_agent_flavour(run_tests, platform)` - Pick the agent script extension from the tests of the current run.
- `CommandAndControlMigratedCommandSet` (class, `cli/commands/command_and_control_migrated.py:66`) `class CommandAndControlMigratedCommandSet(LazyOwnCommandSet)`
- `do_msf` (method, `cli/commands/command_and_control_migrated.py:71`) `def do_msf(self, line)` - Automates various Metasploit tasks including scanning for vulnerabilities, setting up reverse shells
- `do_c2` (method, `cli/commands/command_and_control_migrated.py:421`) `def do_c2(self, line)` - Handle C2 server setup and agent compilation.
- `do_listener` (method, `cli/commands/command_and_control_migrated.py:543`) `def do_listener(self, line)` - Manage C2 listeners: list, add, start, stop, remove.
- `_api` (function, `cli/commands/command_and_control_migrated.py:570`) `def _api(method, endpoint, payload)`
- `do_sandbox` (method, `cli/commands/command_and_control_migrated.py:671`) `def do_sandbox(self, line)` - Toggle or query Docker sandbox mode.
- `do_msfrpc` (method, `cli/commands/command_and_control_migrated.py:713`) `def do_msfrpc(self, line)` - Connects to the msfrpcd daemon and allows remote control of Metasploit.
- `do_sliver_server` (method, `cli/commands/command_and_control_migrated.py:737`) `def do_sliver_server(self, line)` - Starts the Sliver server and generates a client configuration file for connecting clients.
- `do_empire` (method, `cli/commands/command_and_control_migrated.py:854`) `def do_empire(self, line)` - Generates payloads using PowerShell Empire with various options.
- `do_automsf` (method, `cli/commands/command_and_control_migrated.py:904`) `def do_automsf(self, line)` - Try to check if Vulnerable using the module passed by argument of lazyown example automsf exploit/wi
- `do_iis_webdav_upload_asp` (method, `cli/commands/command_and_control_migrated.py:949`) `def do_iis_webdav_upload_asp(self, line)` - (CVE-2017-7269). Vulnerable using the module iis_webdav_upload_asp of metasploit
- `do_duckyspark` (method, `cli/commands/command_and_control_migrated.py:984`) `def do_duckyspark(self, line)` - duckyspark Compiles and uploads an .ino sketch to a Digispark device using Arduino CLI and Micronucl

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 107
- Cross-boundary resolved imports (EXTRACTED): 86

## Connections

- [EXTRACTED] depends_on community 9 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.
- [EXTRACTED] depends_on community 9 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/reactive_engine.py.
- [EXTRACTED] depends_on community 9 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 9 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 9 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 9 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/atomic_exploit_bridge.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: chain_runner changed?
- Should modules: chain_runner be split, given cohesion 0.54?

## Sources

- `cli/apt_chain_support.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/commands/retry_ops.py`
- `cli/retry_support.py`
- `modules/atomic_cli.py`
- `modules/chain_distill.py`
- `modules/chain_facts.py`
- `modules/chain_registry.py`
- `modules/chain_runner.py`
- `modules/chain_state.py`
- `modules/chain_synth.py`
- `modules/closedloop.py`
- `modules/defense_eval.py`
- `modules/defense_stages.py`
- `modules/gym_matrix_runner.py`
- `modules/gym_winbox_runner.py`
- `modules/hunt_verify.py`
- `modules/listener_manager.py`
- `modules/retry_session.py`
- `modules/verb_manifest.py`
- *... and 18 more*
