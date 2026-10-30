# modules: lazyown_facts

*Community 5 | 64 files | cohesion 0.49*

## Definition

This community groups 64 file(s) rooted at `tests` with dominant language py (cohesion 0.49). Central symbols: `AccessFact`, `AptPlaybook`, `AptPlaybookEngine`, `AtomicResolver`, `AtomicTest`, `AtomicTestRef`, `BackendSelection`, `Broken`. Core file: `skills/lazyown_facts.py` (79 symbols). Documented purpose: Parsing, printing and replanning support for the ``apt_chain`` CLI.  Keeps ``cli.commands.command_and_control_migrated`` thin: argument parsing, step selection,.

## Files

### `tests` (29 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_apt_chain_admin.py` | py | testing | 22 | yes |
| `tests/test_apt_chain_integration.py` | py | testing | 6 | yes |
| `tests/test_atomic_exploit_bridge.py` | py | testing | 38 | yes |
| `tests/test_atomic_loop.py` | py | testing | 17 | yes |
| `tests/test_atomic_resolver.py` | py | testing | 9 | yes |
| `tests/test_c2_surfaces.py` | py | testing | 12 | yes |

### `modules` (27 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/ad_gym.py` | py | utility | 10 | yes |
| `modules/apt_playbooks.py` | py | utility | 15 | yes |
| `modules/atomic_cli.py` | py | utility | 11 | yes |
| `modules/atomic_exploit_bridge.py` | py | utility | 39 | yes |
| `modules/atomic_resolver.py` | py | utility | 27 | yes |
| `modules/c2_agent.py` | py | utility | 20 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/apt_chain_support.py` | py | utility | 17 | yes |
| `cli/retry_support.py` | py | utility | 10 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/c2_session.py` | py | utility | 10 | yes |
| `cli/commands/command_and_control_migrated.py` | py | utility | 34 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/safe_exec.py` | py | utility | 14 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_facts.py` | py | utility | 79 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_facts.py` | py | testing | 37 | yes |

*... and 44 more files in this community.*


## Key Symbols

- `_token_name_ok` (function, `cli/apt_chain_support.py:44`) `def _token_name_ok(name)` - True when a name matches the chain token grammar.
- `ChainArgs` (class, `cli/apt_chain_support.py:50`) `class ChainArgs` - Parsed ``apt_chain`` invocation.
- `parse_chain_args` (function, `cli/apt_chain_support.py:74`) `def parse_chain_args(line)` - Parse one ``apt_chain`` command line into structured args.
- `_set_value` (function, `cli/apt_chain_support.py:143`) `def _set_value(args, flag, value)` - Assign one valued option onto the args struct.
- `resolve_admin` (function, `cli/apt_chain_support.py:171`) `def resolve_admin(args)` - Execute an admin action against the registry and checkpoint store.
- `select_step_ids` (function, `cli/apt_chain_support.py:290`) `def select_step_ids(chain, args)` - Resolve --step/--from-step/--to-step into one id set.
- `adversarial_continue` (function, `cli/apt_chain_support.py:322`) `def adversarial_continue(chain)` - Return a copy of the chain where every step continues on error.
- `render_result` (function, `cli/apt_chain_support.py:330`) `def render_result(result)` - Render one chain result as operator lines (JSON mode prints dict).
- `build_cli_approver` (function, `cli/apt_chain_support.py:363`) `def build_cli_approver(printer, input_fn)` - Return an approver baked for interactive operators.
- `approve` (function, `cli/apt_chain_support.py:371`) `def approve(step_id, command)`
- `build_reactive_replanner` (function, `cli/apt_chain_support.py:385`) `def build_reactive_replanner()` - Return a replanner driven by ``modules.reactive_engine``.
- `replan` (function, `cli/apt_chain_support.py:388`) `def replan(context)`
- `_decision_command` (function, `cli/apt_chain_support.py:410`) `def _decision_command(decision)` - Extract one actionable command from a reactive decision.
- `_step_from_decision` (function, `cli/apt_chain_support.py:419`) `def _step_from_decision(command, outcome, executed_count)` - Build one safe replan step from a suggested command.
- `_recent_changes_block` (function, `cli/apt_chain_support.py:441`) `def _recent_changes_block(target)` - Recent world changes on the target for one LLM recovery prompt.
- `build_llm_recovery_chain` (function, `cli/apt_chain_support.py:469`) `def build_llm_recovery_chain(result, target, task_id)` - Ask the LLM pool for a temporary recovery chain after a failed run.
- `_platform` (function, `cli/apt_chain_support.py:543`) `def _platform()` - Guess the loop platform from the payload configuration.
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
- `select_agent_flavour` (function, `cli/commands/command_and_control_migrated.py:43`) `def select_agent_flavour(run_tests, platform)` - Pick the agent script extension from the tests of the current run.
- `CommandAndControlMigratedCommandSet` (class, `cli/commands/command_and_control_migrated.py:66`) `class CommandAndControlMigratedCommandSet(LazyOwnCommandSet)`
- `do_msf` (method, `cli/commands/command_and_control_migrated.py:71`) `def do_msf(self, line)` - Automates various Metasploit tasks including scanning for vulnerabilities, setting up reverse shells

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 248
- Cross-boundary resolved imports (EXTRACTED): 180

## Connections

- [EXTRACTED] depends_on community 5 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.
- [EXTRACTED] depends_on community 5 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/reactive_engine.py.
- [EXTRACTED] depends_on community 5 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/__init__.py.
- [EXTRACTED] depends_on community 5 <-> 10 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 1 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/safe_exec.py.
- [EXTRACTED] depends_on community 5 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 5 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/listener_manager.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [layer strict] `tests/test_c2_surfaces.py` (testing) -> `contrib/legacy/lazydeepseekcli.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:204` `validate_client_id` `ct`: Result of allocator stored in `ct` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:256` `validate_client_id` `data`: Result of allocator stored in `data` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:303` `validate_client_id` `_dn`: Result of allocator stored in `_dn` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:769` `start` `log_file`: Result of allocator stored in `log_file` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/command_executor.py:224` `run_tee` `handle`: Result of allocator stored in `handle` is never checked against NULL.

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` be broken with an interface?
- What would break if the most connected file in modules: lazyown_facts changed?
- Should modules: lazyown_facts be split, given cohesion 0.49?

## Sources

- `cli/apt_chain_support.py`
- `cli/commands/c2_session.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/retry_support.py`
- `contrib/legacy/lazydeepseekcli.py`
- `core/safe_exec.py`
- `modules/ad_gym.py`
- `modules/apt_playbooks.py`
- `modules/atomic_cli.py`
- `modules/atomic_exploit_bridge.py`
- `modules/atomic_resolver.py`
- `modules/c2_agent.py`
- `modules/c2_surfaces.py`
- `modules/chain_approval.py`
- `modules/chain_distill.py`
- `modules/chain_facts.py`
- `modules/chain_registry.py`
- `modules/chain_runner.py`
- `modules/chain_state.py`
- `modules/chain_synth.py`
- *... and 44 more*
