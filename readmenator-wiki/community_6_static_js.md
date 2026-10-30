# static/js

*Community 6 | 64 files | cohesion 0.40*

## Definition

This community groups 64 file(s) rooted at `tests` with dominant language py (cohesion 0.40). Central symbols: `A`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`, `AddonYamlRenderer`, `As`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

### `tests` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_audit_remediation.py` | py | testing | 28 | yes |
| `tests/test_cli_assign.py` | py | testing | 44 | yes |

### `static/js` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |

### `modules` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/auto_purple.py` | py | utility | 40 | yes |
| `modules/c2_builder.py` | py | infrastructure | 23 | yes |

### `core` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/config.py` | py | infrastructure | 20 | yes |
| `core/credential_vault.py` | py | utility | 8 | yes |

### `cli/commands` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/defaults.py` | py | utility | 4 | yes |
| `cli/commands/opsec_cleanup.py` | py | utility | 9 | yes |

### `cli` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/purple_tui.py` | py | utility | 15 | yes |

### `lazyc2` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 39 | yes |
| `lazyc2/state.py` | py | utility | 0 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `lazyc2/blueprints` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/api.py` | py | presentation | 10 | yes |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

*... and 44 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:42`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `DefaultsCommandSet` (class, `cli/commands/defaults.py:38`) `class DefaultsCommandSet(LazyOwnCommandSet)` - Inspect and override build-time default constants.
- `do_defaults` (method, `cli/commands/defaults.py:45`) `def do_defaults(self, line)` - Show or override build-time defaults (TOML + payload.json).
- `_show` (method, `cli/commands/defaults.py:60`) `def _show(self, section)` - Print TOML defaults alongside live payload values.
- `_set` (method, `cli/commands/defaults.py:77`) `def _set(self, name, value)` - Persist an override into payload.json via the assign path.
- `OpsecCleanupCommandSet` (class, `cli/commands/opsec_cleanup.py:19`) `class OpsecCleanupCommandSet(LazyOwnCommandSet)` - OPSEC scoring, log tampering, forensic cleaning, timestomping, memory/network OPSEC.
- `do_opsec_score` (method, `cli/commands/opsec_cleanup.py:25`) `def do_opsec_score(self, line)` - Real-time OPSEC risk assessment with contextual action gating (v2).
- `do_log_tamper` (method, `cli/commands/opsec_cleanup.py:97`) `def do_log_tamper(self, line)` - Cross-platform log clearing commands.
- `do_forensic_clean` (method, `cli/commands/opsec_cleanup.py:162`) `def do_forensic_clean(self, line)` - Clean forensic artifacts — Prefetch, Shimcache, Amcache, Jump Lists, etc.
- `do_timestomp` (method, `cli/commands/opsec_cleanup.py:219`) `def do_timestomp(self, line)` - Manipulate file MACB timestamps to evade forensic timeline analysis.
- `do_memory_clean` (method, `cli/commands/opsec_cleanup.py:288`) `def do_memory_clean(self, line)` - Clean memory artifacts — Kerberos tickets, clipboard, env vars, credentials.
- `do_network_opsec` (method, `cli/commands/opsec_cleanup.py:342`) `def do_network_opsec(self, line)` - Network OPSEC — proxy chains, DoH, canary detection, traffic analysis.
- `do_auditd_disable` (method, `cli/commands/opsec_cleanup.py:445`) `def do_auditd_disable(self, line)` - Generate commands to disable Linux auditd.
- `do_sysmon_disable` (method, `cli/commands/opsec_cleanup.py:468`) `def do_sysmon_disable(self, line)` - Generate commands to disable Windows Sysmon.
- `ParamCommandSet` (class, `cli/commands/params_ops.py:31`) `class ParamCommandSet(LazyOwnCommandSet)` - Create, inspect and delete the shared parameters.
- `do_param` (method, `cli/commands/params_ops.py:38`) `def do_param(self, line)` - Manage the shared parameter catalog used by addons and aliases.
- `_build_exec_parser` (function, `cli/commands/purple_team.py:29`) `def _build_exec_parser()`
- `_build_test_parser` (function, `cli/commands/purple_team.py:67`) `def _build_test_parser()`
- `_build_config_parser` (function, `cli/commands/purple_team.py:92`) `def _build_config_parser()`
- `_build_history_parser` (function, `cli/commands/purple_team.py:106`) `def _build_history_parser()`
- `PurpleTeamCommandSet` (class, `cli/commands/purple_team.py:124`) `class PurpleTeamCommandSet(LazyOwnCommandSet)` - Purple team orchestration commands for the LazyOwn shell.
- `_get_loop` (method, `cli/commands/purple_team.py:130`) `def _get_loop(self)` - Build a PurpleTeamLoop from payload.json config.
- `do_purple_exec` (method, `cli/commands/purple_team.py:144`) `def do_purple_exec(self, line)` - Execute a red action and measure if LazyOwnBT detects it.
- `do_purple_test` (method, `cli/commands/purple_team.py:203`) `def do_purple_test(self, args)` - Test if LazyOwnBT would detect a command (no execution).
- `do_purple_score` (method, `cli/commands/purple_team.py:223`) `def do_purple_score(self, line)` - Show current engagement detection score.
- `do_purple_report` (method, `cli/commands/purple_team.py:271`) `def do_purple_report(self, line)` - Generate full engagement report with datasets.
- `do_purple_methods` (method, `cli/commands/purple_team.py:285`) `def do_purple_methods(self, line)` - List available LazyOwnBT detection methods.
- `do_purple_config` (method, `cli/commands/purple_team.py:297`) `def do_purple_config(self, args)` - Show or update purple team configuration (payload.json).
- `do_purple_dashboard` (method, `cli/commands/purple_team.py:350`) `def do_purple_dashboard(self, line)` - Launch the Purple Team TUI dashboard.
- `do_purple_history` (method, `cli/commands/purple_team.py:367`) `def do_purple_history(self, args)` - Show recent purple team action results.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 351
- Cross-boundary resolved imports (EXTRACTED): 236

## Connections

- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/aliases.py imports core/config.py.
- [EXTRACTED] depends_on community 9 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports core/config.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/param_registry.py` via `subprocess` (4 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/payload_schema.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `modules/opsec_scorer.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`

## Open Questions

- Why do 9 file(s) lack file-level docs (e.g. `key.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` be broken with an interface?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.40?

## Sources

- `cli/assign.py`
- `cli/commands/defaults.py`
- `cli/commands/opsec_cleanup.py`
- `cli/commands/params_ops.py`
- `cli/commands/purple_team.py`
- `cli/commands/security.py`
- `cli/commands/session_ops.py`
- `cli/purple_tui.py`
- `cli/session_resumer.py`
- `cli/show.py`
- `cli/style.py`
- `core/config.py`
- `core/credential_vault.py`
- `core/defaults.py`
- `core/param_registry.py`
- `core/payload_schema.py`
- `core/prompt.py`
- `core/session_secrets.py`
- `key.py`
- `lazyc2/addon_creator.py`
- *... and 44 more*
